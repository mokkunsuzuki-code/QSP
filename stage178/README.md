# Stage177 — CI/CD Attack Matrix (Continuous Security Evidence)

Stage177 introduces **continuous security verification** into QSP.

On every push or pull request, all defined attack scenarios
(Attack-01..06 + demo) are executed automatically via GitHub Actions.

## What this stage proves

- Security claims are **continuously verified**, not asserted once
- Reproducibility is guaranteed by CI + Docker
- Failures are **fail-closed** and block merges

## Workflow

- GitHub Actions (matrix execution)
- Docker Compose (reproducible runtime)
- Artifacts:
  - Per-attack logs (`ci-attack-*`)
  - Aggregated report (`summary.md`)

## Artifacts

After each CI run, the following artifacts are available:

- `attack-summary` — aggregated PASS/FAIL report
- `ci-attack-01` .. `ci-attack-06`
- `ci-demo`

## Why this matters

> “Can this be reproduced at any time?”

Stage177 answers **Yes**, mechanically.

This directly addresses the first concern of
research institutes and enterprises (e.g. reproducibility and evidence).

## Status

✅ Implemented  
✅ Running on every push  
✅ Fail-closed enforced