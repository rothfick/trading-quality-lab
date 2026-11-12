# Iteration 01 — foundations and a trustworthy first signal

## Outcome and acceptance

Address R-01 (invalid quantity), R-08 (misleading green results) and R-09 (environment drift). Deliver one real schema component test with five examples, version/dependency pins, provenance, CI definition and a controlled fault proof. Complete when a fresh checkout runs and the weakened zero boundary is detected. Hosted CI and publication are separate verification items; learner understanding is demonstrated interactively, not asserted by tooling.

## Why these decisions

An independent lab makes contributions visible and avoids modifying upstream application files. A tiny component boundary provides fast feedback while avoiding broker credentials and application side effects. The cost is narrow evidence: we do not prove the endpoint or order execution. ADR-001 and ADR-002 document alternatives and tradeoffs.

Input examples cover negative, zero, fractional and positive whole quantities for non-crypto orders. They deliberately do not cover every exchange, field or interaction. Future financial tests need independently reviewed rules; copying implementation arithmetic is not an independent oracle.

## Guided workshop (discussion in Polish)

1. Read `upstream.json`, then ADR-001. Explain why pinning `main` by name would undermine comparison across runs.
2. Run the README quick start. Inspect `doctor` and identify the upstream commit and Marshmallow version.
3. Read the test before the schema. Predict the result of each quantity example and explain what the expected rejection is based on.
4. Run `test`. Inspect the five JUnit cases and the provenance JSON.
5. Run `prove`. Locate the deliberately failing zero case and then `status: killed`. Explain why the outer command returns success while the mutant pytest process returns 1.
6. Trace `restx_api/place_order.py` to `OrderSchema.load`. Explain what bypassing the package initializer excludes from our evidence.

## Exercise

On a separate exercise branch, add a `quantity="1"` example and inspect whether the schema accepts and coerces it. Explain whether that is a desired API requirement or merely observed behavior. Do not change the production schema to make your assumption true. Run the checks and describe the added coverage without claiming end-to-end correctness.

## Interview prompts and discussion points

- **Why not start with a large E2E suite?** This first risk can be isolated cheaply. State/authorization risks still require integration and E2E coverage later.
- **Is this an API test?** No. It executes the real schema directly, with no HTTP transport, authentication or database.
- **How do you know the assertion has value?** A plausible weakened quantity boundary is accepted by the mutant and caught by the zero case; unrelated errors cannot satisfy the proof.
- **Does a killed mutant prove the suite is complete?** No. It measures sensitivity to one selected defect only.
- **Why is Analyzer not enough?** It can still obtain market prices through broker services; we need a controlled feed for repeatable offline integration tests.
- **What makes this useful to developers?** A small documented entry point, reproducible inputs, clear failures and explicit test boundaries make the signal actionable.

## Assistance provenance

The initial strategy, harness, test and documentation were prepared with a coding assistant. Executable verification supports only the outcomes recorded in the iteration report. Learner code review and the workshop remain explicit follow-up activities. This is not a delivered local-LLM testing workflow.
