# Repository Guidance

## API Client Artifact

`openapi.json` is the canonical API testing and client artifact for this repository.

Do not file the lack of a Postman collection as a gap. OpenAPI is the vendor-neutral standard, and Postman supports importing OpenAPI specs. Manual Postman collections are intentionally avoided because they can drift from the implementation and create vendor lock-in.

If reviewing One2N SRE Bootcamp requirements, treat `openapi.json` plus `scripts/generate_openapi.py` and README import instructions as satisfying the API collection/testing artifact requirement unless an evaluator explicitly requires a proprietary Postman export.
