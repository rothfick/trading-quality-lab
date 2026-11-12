# ADR-002: Load the real schema without API bootstrap

Status: accepted for iteration 01.

## Context

`restx_api/place_order.py` calls `OrderSchema.load` before dispatching to the service. Importing `restx_api.schemas` normally first executes `restx_api/__init__.py`, which registers many namespaces and imports application services. That is an unsuitable boundary for the first isolated validation test.

## Decision

Load the complete, unmodified `restx_api/schemas.py` using Python's file-module loader under a lab-specific module name. Import its actual `utils.constants` from the pinned checkout; `utils/__init__.py` is empty and hash-verified. Install the real upstream Marshmallow version. Do not stub dependencies or reimplement the schema.

The test measures `OrderSchema.load` only. It does not measure the service wrapper's extra validation, request parsing, route registration, authorization, response mapping or persisted side effects. Add normal full-application imports and HTTP tests when the integration harness exists.

## Sensitivity proof

Require a passing baseline, then copy the schema into a temporary directory and replace only `OrderSchema.quantity`'s `min_inclusive=False` with `True`. Execute the same test module in a separate process. Require exactly the zero-quantity case to fail with an assertion, no errors or skips. Keep the original source untouched and verify its hashes again.

This proves sensitivity to one plausible boundary defect. It is not a mutation score, evidence of all invalid-input coverage or a full mutation-testing framework.

## Alternatives and costs

Starting Flask would require substantially more dependencies and configuration. Mocking the schema would not test upstream behavior. Extracting and rewriting the schema would risk testing a copy. File loading retains real module code but bypasses application import behavior, a deliberate limitation that higher layers must cover.
