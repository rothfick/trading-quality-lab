# Iteration 01 evidence

## Verified implementation

Implementation commit: `79745a85091702159170e34c2e2568d37f421e2d`.
Upstream: `7ba5267f7d5d15c352606b3aea6b12ab20223428`.
Runtime observed: macOS ARM64, CPython 3.12.16, pytest 9.1.1, Marshmallow 3.26.2, uv 0.13.8.

| Check | Actual result |
|---|---|
| `uv sync --locked` | Dependencies install into an independent environment |
| `ruff check .` and `ruff format --check .` | Pass |
| Bootstrap against existing checkout | Matching pin reused; original source unchanged |
| Doctor | Pin, three component hashes, runtime/dependency versions and profile emitted |
| Unmodified schema | 5 cases pass; no skips, failures or retries |
| Controlled mutation | Exactly `test_limit_order_quantity_boundary[zero-rejected]` fails; other 4 pass |
| Proof command | Exit 0 only after passing baseline and expected mutant detection |
| Offline proof after setup | Pass with `uv run --offline --locked python -m harness.lab prove` |
| Fresh checkout | Temporary clone of the implementation branch, new uv environment, actual upstream fetch by commit, doctor, proof and lint/format all pass |
| Baseline assertion failure | Proof exits 1; does not count as mutation detection |
| Old successful proof summary | Removed before a subsequent failed proof |
| No tests / unexpected skip / fixture error | Each is rejected with exit 1 |
| Remove zero example | Baseline passes, mutant survives, proof correctly exits 1 |
| Change measured upstream file | Doctor rejects the changed component |
| Mismatch manifest commit and existing checkout | Bootstrap rejects it without resetting the checkout |
| Repository boundary | No upstream source, image attachments or databases tracked |
| Local Markdown links | All tracked relative links resolve |

Fresh-checkout and failure-path probes were executed in a disposable clone. The probes replaced only that clone's test file, then restored it; a source-hash probe appended a comment to the clone's constants file and restored its bytes. A commit-mismatch probe temporarily changed the clone's manifest. Both temporary repositories were clean after restoration. The existing working OpenAlgo checkout was never used for these modifications.

Machine-readable local evidence is generated under `quality-lab/reports/generated/`: `baseline.json`, `baseline.xml`, `mutant.xml`, `mutation-proof.json` and the one-time acceptance campaign's `acceptance.json` (17 successful checks/observations). The normal runner regenerates baseline/mutant evidence; acceptance probes are a separate campaign, not a permanent second domain suite. Generated files are ignored; this summary preserves the measured outcomes.

## Pending and limits

- GitHub publication and hosted Actions execution are **not completed**: local `gh` has no authenticated session. The connected GitHub tool can identify the account but cannot create a repository; Safari automation access is unavailable.
- No remote, public repository or PR has been claimed as created. The implementation branch and English PR body are ready; see the publication guide.
- This is component-level schema evidence. HTTP, auth, side effects, full order lifecycle, full upstream suite, Linux runtime and local-LLM execution remain unverified.
- The learner workshop and exercise still need the learner's participation. Passing checks do not establish understanding.
