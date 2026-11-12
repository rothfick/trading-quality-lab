# Upstream source baseline

Inspected revision: `7ba5267f7d5d15c352606b3aea6b12ab20223428`. These are source-inspection observations, not executed upstream suite results.

| Area | Observed source | Implication |
|---|---|---|
| Backend | Flask, RESTX resources, services, broker adapters, SQLAlchemy stores | Test boundaries must distinguish HTTP, orchestration, persistence and external effects |
| Frontend | React/TypeScript; Vitest, Testing Library, axe and Playwright configuration | Reuse existing tools; no benefit in rebuilding every framework |
| Validation | `restx_api/place_order.py` uses `OrderSchema.load`; `schemas.py` validates positive quantity and coerces non-crypto whole quantities | First component test has a concrete production caller |
| Import boundary | `restx_api/__init__.py` imports and registers many namespaces | A normal schema import brings in application bootstrap dependencies |
| Analyzer | Sandbox execution can obtain prices through quote services; some upstream tests require a broker session | Analyzer is not automatically deterministic or offline |
| Backend CI | Explicit credential-free subset, worker/concurrency suites; Ruff checks allow errors | Green upstream CI does not imply all backend tests or lint pass |
| Frontend CI | Build, unit tests and Chromium workflow coverage | Configured browser projects are not equivalent to executed coverage |
| Security CI | Bandit and dependency findings can be tolerated; SARIF fallback may contain no findings | Read actual findings and artifacts; do not infer a clean security posture from green CI |

No application defect is confirmed by these observations. The original full test suite, full dependency installation, all brokers, all platforms and hosted GitHub execution have not been verified by this audit. Follow-up findings need a reproducer, expected behavior source, affected revision and actual outcome.
