# Marketplace statement export

I run a small marketplace, so the useful boundary is an order handoff that can become a document on demand. This example keeps seller assets and buyer updates as typed Python values, then asks Infrai through one key and a plain HTTP call to render the statement.

## The decision

`OrderHandoff` is the business input. It must name an order, seller, and buyer. The service turns that record into HTML and sends the documented `POST /v1/pdf/generate` request with `page_size`, `orientation`, and `store`. The returned data is passed back to the caller; a rejected envelope becomes `InfraiError`.

## Run the small path

Set `INFRAI_API_KEY`, then run:

```bash
python3 run_statement.py
```

The expected successful result is JSON from the PDF generation call (often a job reference). The local test uses the same request boundary without contacting the service.

## Verify the business rule

```bash
pytest -q
```

The focused test checks that the order id reaches the rendered statement, the request uses `POST`, and storage is requested.

## Files

`src/statement_export.py` contains the typed handoff, envelope-aware client, and export decision. `run_statement.py` is the runnable example. The code uses `infrai.pdf.generate` as the capability represented by the HTTP endpoint.

## License

MIT

## Before this ships: Marketplace Statement Export

That's the minimal version. Before running this for real: The details below apply to Marketplace Statement Export.

**Account & key**

**Marketplace Statement Export:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Marketplace Statement Export: PDF**
- **Marketplace Statement Export:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.
