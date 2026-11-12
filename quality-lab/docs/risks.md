# Risk register

Priority is qualitative: consequence and exposure guide ordering; no measured probability is implied. Status describes lab evidence only.

| ID | Risk and impact | Priority | Planned evidence | Current status |
|---|---|---|---|---|
| R-01 | Invalid quantity accepted, producing incorrect order intent | High | Boundaries, schema/API validation, state-effect assertions | Schema only: -1, 0, 0.5, 1, 2; zero-boundary mutation |
| R-02 | Unauthorized operation or cross-user data access | Critical | Auth matrix, negative requests, persisted-effect checks | Planned |
| R-03 | Analyzer/live routing sends intent through the wrong path | Critical | Routing integration and blocked external broker boundary | Planned |
| R-04 | Duplicate execution after retry or ambiguous timeout | Critical | Fault injection and state reconciliation | Planned; no assumed idempotency guarantee |
| R-05 | Order, trade, position and funds disagree | High | Lifecycle integration, accounting invariants, independent oracle | Planned |
| R-06 | Stale/missing/out-of-order prices affect execution | High | Controlled feed, sequence and reconnect scenarios | Planned |
| R-07 | Timezone, calendar or restart causes wrong scheduled action | High | Controlled clock, session edges and recovery | Planned |
| R-08 | Green CI hides missing tests, skips or ineffective assertions | High | No-test/skip gates, JUnit evidence, controlled mutation | Initial gates implemented; broader campaign planned |
| R-09 | Environment drift makes results irreproducible | High | Source pin/hashes, lockfile, fresh-checkout verification | Foundation controls implemented |
| R-10 | AI invents requirements, misses failures or obeys hostile input | High | Reviewed evaluation set, baseline comparison, injection cases | Planned |
| R-11 | UI blocks critical user actions or accessible use | Medium | Real-stack E2E, keyboard and axe checks | Planned |
| R-12 | Overload or migration harms availability or data | High | Load/recovery, upgrade and rollback evidence | Planned |

Residual risk after iteration 01 remains substantial: no HTTP server, authorization, execution, state, resilience or financial arithmetic has been verified. This register is revised as source inspection and experiments reveal new information.
