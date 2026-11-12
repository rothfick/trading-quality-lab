# ADR-001: Independent lab with a pinned upstream

Status: accepted for iteration 01.

## Context

The portfolio must make lab contributions distinguishable from OpenAlgo and allow repeatable tests without modifying a trader's existing environment. A local upstream checkout already exists.

## Decision

The workspace root is the lab Git repository. `openalgo/` is ignored and fetched from the repository/commit in `upstream.json`. Reuse a matching local checkout without resetting it; reject a mismatched HEAD or changed component hashes. The harness and schema tests use a dedicated uv environment and do not install or start the full application.

Changing the application pin or covered component set requires a dedicated PR with baseline differences, updated hashes and rerun evidence. The pin represents one tested revision, not ongoing upstream compatibility.

## Alternatives and consequences

- A fork would put application changes and lab work together but obscure the independent platform boundary. Use a fork later only for explicit application patches.
- A submodule would encode a commit naturally but adds contributor workflow complexity. The manifest also carries measured component hashes and is simple to inspect.
- Copying upstream code would duplicate maintenance and require managing redistributed notices. Source stays in its own checkout.

The lab now owns bootstrap and compatibility. GitHub and package downloads are required initially. Source pinning does not freeze Python patch versions or all OS behavior; reports record actual runtime versions. The full application environment is deferred to the integration milestone.
