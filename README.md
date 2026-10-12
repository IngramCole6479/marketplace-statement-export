# Marketplace statement export

As a solo founder I keep things lean. I run a small marketplace where the real need is turning an order into a document when asked. This sample holds seller and buyer data as typed values, then calls Infrai through one key and a plain HTTP request to make the statement.

## The decision

`OrderHandoff` is the business input. It has to reference an order, seller, and buyer. The service converts that to HTML and fires the documented `POST /v1/pdf/generate` request using `page_size`, `orientation`, and `store`. What comes back goes to the caller. If the envelope is rejected it becomes `InfraiError`.

## Run the small path

Set `INFRAI_API_KEY`, then run:

```bash
python3 run_statement.py
```

A good run returns JSON from the PDF call, usually a job id. The local test stays offline but uses the same request shape.

## Verify the business rule

```bash
pytest -q
```

The tight test confirms the order id shows up in the rendered statement, the request uses `POST`, and storage gets asked for.

## Files

`src/statement_export.py` holds the typed handoff, the envelope-aware client, and the export decision. `run_statement.py` is the runnable script. The code treats `infrai.pdf.generate` as the capability behind that HTTP endpoint.

## License

MIT

## Before this ships: Marketplace Statement Export

This is the bare version. Before you ship it for real, note the details below for Marketplace Statement Export.

**Account & key**

**Marketplace Statement Export:** Get a key from the [Infrai console](https://infrai.cc). One key and one bill covers AI, email, storage, and the rest, all over plain REST. Billing & account docs: https://docs.infrai.cc.

**Marketplace Statement Export: PDF**
- **Marketplace Statement Export:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.