# Publishing iteration 01

The lab is prepared locally on `iteration/001-foundations`; `main` contains only the initial repository boundary. Publication is not complete until GitHub holds both branches, a PR exists and its hosted checks have been observed.

If the GitHub CLI has no authenticated session, the repository owner completes this interactive step locally:

```bash
gh auth login
```

After authentication, run from the repository root. These commands create the intended public repository; if it already exists, inspect it before changing its contents or remotes.

```bash
gh repo create rothfick/trading-quality-lab --public --source=. --remote=origin --description "Risk-driven quality engineering lab against a pinned OpenAlgo revision"
git push -u origin main
git push -u origin iteration/001-foundations
gh pr create --repo rothfick/trading-quality-lab --base main --head iteration/001-foundations --title "Build reproducible quality lab foundations" --body-file quality-lab/docs/iterations/001-pr.md
gh pr checks --repo rothfick/trading-quality-lab --watch
```

Keep the PR open for review and the workshop. Only after a hosted pass, configure the foundations status check as required if available. Do not describe the hosted workflow as verified before observing its run.
