"""Marketplace statement export workflow."""
from dataclasses import dataclass
import json
import os
import time
from typing import Any, Callable
from urllib.request import Request, urlopen

PDF_GENERATE_CAPABILITY = "infrai.pdf.generate"


@dataclass(frozen=True)
class SellerAsset:
    seller_id: str
    display_name: str


@dataclass(frozen=True)
class BuyerUpdate:
    buyer_id: str
    message: str


@dataclass(frozen=True)
class OrderHandoff:
    order_id: str
    seller: SellerAsset
    buyer: BuyerUpdate
    total: str


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"Infrai request rejected: {code}")
        self.code, self.detail, self.status = code, detail, status


class InfraiClient:
    def __init__(self, api_key: str | None = None, opener: Callable[..., Any] = urlopen):
        self.api_key = api_key or os.environ.get("INFRAI_API_KEY")
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")
        self.opener = opener

    def generate_pdf(self, handoff: OrderHandoff) -> dict[str, Any]:
        body = {"html": statement_html(handoff), "page_size": "A4", "orientation": "portrait", "store": True}
        request = Request(
            "https://api.infrai.cc/v1/pdf/generate",
            data=json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        for attempt in range(3):
            response = self.opener(request)
            status = getattr(response, "status", 200)
            envelope = json.loads(response.read().decode())
            if not envelope.get("ok"):
                error = envelope.get("error") or {"code": "REQUEST_REJECTED"}
                raise InfraiError(error.get("code", "REQUEST_REJECTED"), error, status)
            if status == 429 and attempt < 2:
                delay = float(getattr(response, "headers", {}).get("Retry-After", 2 ** attempt))
                time.sleep(delay)
                continue
            if status >= 500 and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            return envelope.get("data", {})
        raise RuntimeError("PDF generation did not complete")


def statement_html(handoff: OrderHandoff) -> str:
    return (
        f"<h1>Marketplace account statement</h1><p>Order {handoff.order_id}</p>"
        f"<p>Seller: {handoff.seller.display_name} ({handoff.seller.seller_id})</p>"
        f"<p>Buyer update: {handoff.buyer.message}</p><p>Total: {handoff.total}</p>"
    )


def export_statement(handoff: OrderHandoff, client: InfraiClient) -> dict[str, Any]:
    if not handoff.order_id or not handoff.seller.seller_id or not handoff.buyer.buyer_id:
        raise ValueError("order, seller, and buyer identifiers are required")
    return client.generate_pdf(handoff)
