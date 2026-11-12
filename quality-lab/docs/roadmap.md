# Delivery roadmap

Each milestone may take multiple PRs. Sequence follows dependencies and risks, not a fixed calendar. Iteration 01 implements only the foundations; later rows are a backlog, not delivered capabilities.

| Milestone | Deliverable | Exit evidence |
|---|---|---|
| 0 — Discovery | Source baseline, risk register, competency map, strategy, ADRs | Claims trace to inspected source; limitations explicit |
| 1 — Reproducibility | Version pin, dedicated environment, harness, CI | Fresh checkout runs; controlled fault is detected |
| 2 — First vertical slice | LIMIT create → list → cancel with real backend/database and controlled quotes | Valid lifecycle, invalid/auth failures without effects, clean reruns, quote failures diagnosed |
| 3 — Test design | Boundaries, equivalence partitions, decision tables, states, exploratory charters, selected BDD | Each technique justified against a risk; no duplicate prose-only test bureaucracy |
| 4 — Finance | Quantity/tick rules, precision, margin, funds, positions, P&L, calendars | Reviewed domain examples and independent calculation oracles |
| 5 — Generative techniques | Hypothesis properties/state machines, metamorphic checks, targeted mutation campaign | Reproducible counterexamples, defined invariants and interpreted mutation survivors |
| 6 — Contracts | API inventory, schema-based generation, adapter capability matrix and conformance suite | Drift caught; unsupported capabilities distinguished from defects |
| 7 — User experience | TypeScript Playwright critical flows, axe, keyboard, stable visual comparisons | Real-stack evidence; browser matrix expanded by risk |
| 8 — Resilience | WebSocket, reconnect, duplicate/out-of-order data, ambiguous writes, restart | State reconciliation and resource-cleanup evidence |
| 9 — Performance | k6 baseline/load/spike/soak and correlated diagnostics | Workload, environment and derived budgets recorded |
| 10 — Security/delivery | Threat model, auth/session tests, static/dependency scans, local DAST, migration/rollback | Reproductions, triage and release-impact evidence |
| 11 — Local AI | Ollama workflows for analysis/design/triage/reporting; structured output and injection evaluations | Measured comparison against reviewed non-AI tasks including review cost |
| 12 — Enablement | Developer guide, second-app adoption exercise, demo and architectural interview | Another engineer can add a test and explain the boundaries |

## Next iteration: integration environment design

Trace the LIMIT order path, database/session initialization, user/API-key setup, Analyzer routing and quote-fetch boundary. Design the smallest controlled price/broker adapter and an isolated real application environment. Write an ADR before choosing the injection mechanism. Do not claim a simulated order lifecycle using only the current schema tests.

## Experiment protocol

Every experiment states a question, alternatives, a fixed representative workload, measurements, result and adoption decision. Compare tools in `experiments/` without adding all of them to mandatory CI. Examples: schema-based API generation versus handpicked tests; polling versus event-driven synchronization; Page Objects versus task abstractions; local model recommendations versus reviewed human baselines.

## AI defaults

Use local inference only. Choose and pin an Ollama model after a representative benchmark on the available machine; measure memory, latency and quality. Do not add an LLM to the deterministic CI path. Record prompts, model identity, parameters and evaluation inputs; validate structured outputs and inspect semantic correctness independently. No autonomous live trading.
