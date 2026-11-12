# Quality strategy v0

## Product and audience

OpenAlgo joins user/API intent, order validation, mode routing, broker adapters, persistent state and asynchronous market data. The lab targets engineers who need reproducible evidence and reusable test infrastructure. Portfolio reviewers should be able to identify the author's decisions and their practical limits.

The primary quality goals are order correctness, authorization and isolation, consistent state, recoverability, diagnosability and fast feedback. This is a quality engineering lab, not an evaluation of trading profitability or suitability for live trading.

## Risk-driven layers

- Component tests cover validation and deterministic calculations quickly.
- Integration tests cover the real service/database boundary with controlled broker and market data adapters.
- API tests verify wire behavior, authorization and observable effects.
- A small E2E suite covers critical workflows through the real UI and backend.
- Focused campaigns cover accessibility, resilience, performance, security, migrations and AI evaluation.

Layer counts follow risk and feedback cost rather than a fixed test-pyramid percentage. Maintain a distinction between a schema component, a service component, a virtualized integration and a real external integration. Passing one layer does not prove another.

## Oracles and data

Use reviewed examples, domain invariants and independent reference calculations. Label characterization tests separately from requirements. Use synthetic identities and instruments, isolated databases, a controlled clock and stable price feeds as later integrations are introduced. Record seeds when randomness is introduced; current examples have no seed.

Analyzer Mode alone is insufficient for offline execution: it can require quotes from a broker session. Full-flow tests need a controlled market-data boundary and a real backend/database. Never report a mocked UI flow as E2E proof.

## Feedback and evidence

Iteration 01 gates on lint, formatting, the five-case schema test and the controlled mutation. Record version pin, component hashes, Python/dependency versions, test outcomes, skips and retries. Expensive campaigns become separate jobs as their scope exists. Establish load and reliability budgets from explicit product objectives and measured baselines, not arbitrary numbers.

The runner rejects zero tests, unexpected skips and setup errors. Mutation proof first requires a passing baseline and then exactly the expected assertion failure. New failures are investigated against the upstream baseline. A green upstream workflow is not sufficient evidence for this lab's risk claims.

## AI and ownership

Use local AI for proposed requirements analysis, test ideas, exploration support, failure triage and report drafting. Evaluate against reviewed tasks with and without AI, including total review time, errors and hallucinations. Inputs are untrusted data; model output is a proposal. The deterministic core must run without an LLM. No model makes release decisions or accesses a live trading account.

Each iteration leaves a developer-facing guide and a Polish workshop. The learner must explain boundaries, alternatives and residual risk before describing the increment as understood. This human learning outcome is not inferred from automated test results.
