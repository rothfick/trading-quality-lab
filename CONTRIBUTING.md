# Working agreement

Every increment starts with a product risk and explicit acceptance criteria, then delivers a small reviewable change, evidence, a short explanation and a learner exercise. Documentation, code and pull requests are English; guided discussions are Polish.

## Workflow

1. Choose one outcome from the roadmap; identify affected risks and test boundaries.
2. Work on `iteration/NNN-description`. Keep upstream revisions and application changes in dedicated changesets.
3. Add meaningful checks, run the README commands, and record actual outcomes and limitations.
4. Open a PR describing the problem, resulting behavior, alternatives and validation. Do not claim checks that were not run.
5. Review the code and evidence, complete the workshop, then merge. One-person review is a learning exercise, not independent approval.

Core checks must fail on failures, errors, unexpected skips and no collected tests. Do not hide failures with retries or `continue-on-error`. Quarantining a future flaky test requires an issue, an owner, an expiry date and a visible residual-risk note. Existing upstream findings belong in the baseline rather than being mislabeled as new lab regressions.

Add tooling when an experiment has a hypothesis and an acceptance measure. Prefer small functions, explicit fixtures and dependency adapters. Avoid generic base classes and parallel framework implementations without a comparison question.

## Publication

Iteration 01 uses a minimal bootstrap commit on `main`, then an implementation branch and PR. After the first hosted pass, configure `Lab quality / foundations` as a required check if supported by the account's settings. Never push to the upstream OpenAlgo repository.

If the GitHub CLI is not authenticated, the owner runs `gh auth login` interactively. Do not put tokens in repository files, prompts or chat. Publishing requires an authenticated account with repository-creation permission. An unpushed local branch is not a published PR.

## AI provenance

AI assistance must be attributed in iteration notes. Record what it proposed, what a human reviewed and which executable checks support the change. Until local-model infrastructure and evaluations are delivered, do not claim that using a coding assistant implements the lab's local AI lifecycle.

Never commit credentials, real brokerage data, recruitment messages, screenshots or machine-specific environment files. Synthetic fixtures must be clearly identified.
