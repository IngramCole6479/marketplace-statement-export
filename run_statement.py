import json
from src.statement_export import BuyerUpdate, InfraiClient, OrderHandoff, SellerAsset, export_statement


def main() -> None:
    handoff = OrderHandoff(
        order_id="order-1042",
        seller=SellerAsset("seller-7", "Northwind Books"),
        buyer=BuyerUpdate("buyer-19", "Packed and ready for carrier pickup."),
        total="48.00 USD",
    )
    print(json.dumps(export_statement(handoff, InfraiClient()), indent=2))


if __name__ == "__main__":
    main()

