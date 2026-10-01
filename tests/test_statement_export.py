import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.statement_export import BuyerUpdate, InfraiClient, OrderHandoff, SellerAsset, export_statement


class Response:
    status = 200
    headers = {}

    def read(self):
        return json.dumps({"ok": True, "data": {"job_id": "job-1"}, "error": None, "metadata": {}}).encode()


def test_export_preserves_order_handoff_in_pdf_request():
    seen = {}

    def opener(request):
        seen["method"] = request.get_method()
        seen["body"] = json.loads(request.data)
        return Response()

    handoff = OrderHandoff("o-1", SellerAsset("s-1", "Acme"), BuyerUpdate("b-1", "Shipped"), "12 USD")
    result = export_statement(handoff, InfraiClient("test-key", opener))
    assert result["job_id"] == "job-1"
    assert seen["method"] == "POST"
    assert "Order o-1" in seen["body"]["html"]
    assert seen["body"]["store"] is True
