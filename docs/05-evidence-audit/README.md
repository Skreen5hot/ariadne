# Evidence audit

The spec index records what each document says about itself: Draft, Hardened, Final, PASS (exemplary).
This audit records something different: **what running evidence shows**. It exists because a document can be
excellent and still describe nothing that runs.

The rendered result is [audit.md](audit.md). Never edit it by hand.

## The ladder

Each level requires every level below it. Levels are computed by `tools/evidence_audit.py` from the
records in `evidence/`; no file in this folder states a level.

| Level | Meaning | Evidence that earns it |
| --- | --- | --- |
| L0 spec-only | A specification exists, no code | No repository is mapped to the spec |
| L1 code | Something is built | The mapped repository contains source code, not only documents or ontology files |
| L2 tested | Its builder wrote checks | The repository contains test files |
| L3 passing | The checks pass today | The collector ran the suite at the recorded commit and it passed |
| L4 used | Something else depends on it | Another inventoried repository references it from code or a manifest (documentation does not count) |
| L5 production | It runs without you watching, and you would know if it broke | L4, plus deployment by automation and CI on the default branch |

Two flags hold a repository at L2: **FAILING** (the suite ran and failed) and **NOT RUNNABLE** (the suite
could not reach a verdict in a clean checkout: install failure, missing entry point, collection error,
timeout). A suite that only runs on its author's machine is not yet evidence.

A spec's level is the best level among the repositories mapped to it.

## What is human-supplied

Only two things, both in `inventory.yaml`:

1. the list of repositories, and
2. which spec-index entries each repository implements, with the basis for the claim.

Everything else is collected. Spec names, versions and document status are read from
`docs/00-foundation/spec-index.md`, which stays their only owner.

## Refreshing it

From the repository root, on a machine signed in to GitHub (`gh auth login`):

```
python tools/sync_inventory.py          # add every Skreen5hot repo not yet inventoried
python tools/collect_evidence.py --run  # clone each repo into a temp dir, record facts, run its tests
python tools/render_audit.py            # regenerate audit.md
python -m pytest tests/audit            # the audit's own honesty checks
```

`--run` executes each repository's own test suite (`npm run test:ci` or `npm test`, or `pytest`) in a
throwaway clone. Without `--run`, earlier test results are kept only if they are for the same commit.

Then map the new repositories: for each, set `implements` to the spec-index entries it realizes and say
why in `mapping_basis`. Unmapped repositories still appear, under "Repositories with no indexed
specification", which is itself a finding.

## Limits

- Test counts come from file names and folders; they show that checks exist, not that they are good.
- "Used" is detected from GitHub, raw-content and Pages URLs in code and manifests. A dependency
  through a package registry under a different name is missed until the matcher learns that name.
- Deployment is read from workflow files and a `gh-pages` branch; the live site is not fetched.
- The collector cannot see private repositories without credentials that can clone them.
