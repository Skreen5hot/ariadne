# Evidence audit: handoff to the next agent

Written 2026-10-28 by the Claude session that built the first version. Branch: `evidence-audit`
(three commits, pushed, not merged, no pull request opened). Read this file and README.md before
changing anything.

---

## 1. Why this exists

Aaron works alone across 100+ repositories and hundreds of specifications aimed at one goal: a
synthetic moral person (FNSR). He needs a roadmap to production that rests on evidence, not on
documents. The project's specs already carry statuses like "Final", "Hardened" and
"PASS (exemplary)"; none of those words says whether anything runs.

The governing principle, reached after a long review of business-case process that had become
theatre: **a status is something you compute from evidence, never something you write.** The audit
must not become another document that describes work instead of measuring it.

Guard these rules. If a change would break one, stop and ask Aaron:

1. No file states a level. Levels are computed from collected evidence (tests enforce this).
2. The only human claims are which repositories exist and which spec each implements, each with a
   stated basis. Aaron ratifies mappings; an agent may propose them.
3. Documents never climb the ladder. A reference from a README is not use; a test that could not
   run is not a pass.
4. Report what the evidence shows, including when it is bad. "Not runnable" and "failing" are
   findings, not embarrassments to smooth over.

## 2. What was built

The design copies the existing evidence register (`docs/02-evidence/register.yaml` plus
`tools/render_register.py` plus `tests/evidence/`): a data file, a generated view never edited by
hand, and tests that keep the two honest.

| File | Role |
| --- | --- |
| `docs/05-evidence-audit/inventory.yaml` | Human-supplied: repositories, and which spec-index entries each implements (`implements`, `mapping_basis`). Also `buildable_layers` and `not_buildable` exemptions. |
| `docs/05-evidence-audit/evidence/<repo>.json` | Machine output from the collector. Never edit by hand. |
| `docs/05-evidence-audit/audit.md` | Rendered view. Never edit by hand. |
| `docs/05-evidence-audit/README.md` | The ladder, the refresh commands, the limits. |
| `tools/evidence_audit.py` | Shared model: parses `docs/00-foundation/spec-index.md`, loads inventory and evidence, **computes levels**. |
| `tools/collect_evidence.py` | Clones each inventoried repo, records facts, optionally runs its tests (`--run`). |
| `tools/render_audit.py` | Writes `audit.md`; `--check` fails if it is stale. |
| `tools/sync_inventory.py` | Adds every repo from `gh repo list` to the inventory with an empty mapping. Only adds; never edits or removes. |
| `tests/audit/test_evidence_audit.py` | 20 tests: inventory asserts no levels, mappings name real specs, evidence is machine-shaped, `audit.md` is current, and 13 ladder rules on synthetic records. |

### The ladder (computed in `repo_level()`)

| Level | Earned by |
| --- | --- |
| L0 spec-only | No repository mapped to the spec |
| L1 code | Mapped repo has source files (ontology/doc files alone do not count) |
| L2 tested | Repo has test files |
| L3 passing | Collector ran the suite **at the recorded HEAD** and it passed |
| L4 used | Another inventoried repo references it from code or a manifest |
| L5 production | L4 plus automated deployment plus CI on the default branch |

Flags that hold a repo at L2: **FAILING** (suite reached a verdict and failed) and **NOT RUNNABLE**
(install failure, missing entry point, pytest exit 2 to 5, timeout). Evidence older than 30 days is
flagged stale. A spec's level is the best level among its mapped repos.

### Collector behavior worth knowing

- Clones with `--filter=blob:none` (full history, no blobs). Shallow clones are wrong here: BCO and
  ValueNet test suites check git ancestry and correctly refuse shallow history.
- Node repos: runs `npm run test:ci` if defined, else `npm test`. Python: `pytest`, after
  `pip install -r requirements.txt / requirements-dev.txt` if present.
- Records the toolchain (Node pinned via `.nvmrc` vs Node used, Python used). The renderer notes a
  major-version mismatch beside a failure.
- "Used" is detected only from unambiguous addresses: `github.com/Skreen5hot/<repo>`,
  `raw.githubusercontent.com/Skreen5hot/<repo>`, `skreen5hot.github.io/<repo>`. Bare-word matches
  were tried and produced false positives, so they were removed.
- Without `--run`, an earlier test result is kept only if it is for the same commit.

## 3. Results of the first collection (2026-10-28)

Six repositories were inventoried: the ones named in ariadne or known to be public. The session
could not list Aaron's account.

| Repo | Level | Detail |
| --- | --- | --- |
| TagTeam.js | L3 passing | `npm run test:ci` passed (about 3 min). Only repo mapped to indexed specs (TagTeam Roadmap, TagTeam Architecture). |
| Business-and-Agent-Capabilities-Ontology | L3 passing | 455 pytest tests pass. Depends on BusinessProcessOntology in code (`config/upstream-sources.yaml`). |
| ValueNet | L2 FAILING | 24 of 1,105 fail. 23 are in `tests/site/test_explorer.py` and stem from `.nvmrc` pinning Node 24.20.0 while the run used Node 22. One is real-looking: `tests/integration/test_destination_state.py::test_the_import_baseline_measures_rather_than_lists` expects `['is_v_emo_overlaps.py']` and gets `['check_bfo_consistency.py', 'is_v_emo_overlaps.py']`. |
| ariadne | L2 FAILING | 1 of 455 fails: `tests/e-pc/test_annotator_tool.py::test_generated_tool_is_current`. Rebuilding with `build_annotator.py` changed one line each in `annotator.html` and `DEMO_annotator.html` (the embedded JSON data block). Cause not diagnosed. Do not "fix" it by regenerating and committing without Aaron: `experiments/e-pc/` is byte-frozen for a ratified preregistration (see `.gitattributes`). |
| Ontology-of-Freedom | L2 NOT RUNNABLE | `npm test` runs `node run-all-tests.js`, which is not in the repo, so its own CI cannot pass either. Last commit 2026-02-14. |
| BusinessProcessOntology | L1 code | No test files. Deploys a site. |

Headline: spec-index lists 62 buildable specs. 27 claim maturity (Final, Hardened, Stable,
Candidate, Ready, Normative), and none of the 27 is mapped to code yet. **L0 currently means
"unmapped", not "unbuilt"**; the audit says so at the top. Nothing reaches L4 or L5 yet.

## 4. What the next agent should do, in order

### Step 1. Run the full sweep on Aaron's machine

The cloud session could not list repositories; VS Code on Aaron's machine can. From the ariadne root:

```
git fetch origin && git checkout evidence-audit
python -m venv .venv-audit && .venv-audit\Scripts\activate    # Windows; keeps pip installs out of global Python
pip install pyyaml pytest
gh auth status                                                 # must be signed in
python tools/sync_inventory.py --dry-run
python tools/sync_inventory.py
```

Then reconcile the result against the list Aaron supplies in section 6. Anything in his list that
`gh` did not return (renamed repos, other owners) gets added by hand with a `mapping_basis`.

### Step 2. Collect evidence

```
python tools/collect_evidence.py                 # static facts for every repo; fast
python tools/collect_evidence.py --run NAME ...  # tests, a few repos at a time
python tools/render_audit.py
python -m pytest tests/audit
```

`--run` executes each repository's own test suite and installs its dependencies. Use the venv. Run
it in batches; large suites take 2 to 5 minutes each. Use the Node version each repo pins (nvm or
fnm), or accept and report the toolchain note.

### Step 3. Propose spec mappings; Aaron ratifies

For each repository, propose `implements` (exact names from `docs/00-foundation/spec-index.md`)
and a one-line `mapping_basis` citing the evidence: README claims, package names, spec titles in the
code. Present proposals as a table for Aaron to accept, amend or reject. Do not write unratified
mappings into `inventory.yaml` as if settled. Repos that implement no indexed spec stay
`implements: []`; that is itself a finding (the audit lists them).

### Step 4. Fix what the first run exposed, in the audit's own tooling

- **Descriptions.** Aaron's repo list has descriptions. The inventory test only allows the keys
  `name, owner, implements, mapping_basis`. If descriptions should live in the inventory, add
  `description` to the allowed set in `test_inventory_asserts_no_levels` and render it in
  `audit.md`. Descriptions are claims by the author, so never derive a level from one.
- **Dependency detection.** Extend `find_references` to read manifests properly: `package.json`
  dependencies, including git URLs, `requirements*.txt`, `pyproject.toml`. Without this, L4 will
  under-count.
- **Toolchain.** Optionally let the collector honor `.nvmrc` through nvm or fnm when available.
- **ariadne's own CI.** ariadne has no `.github/workflows`. Add one that runs `pytest tests/audit`
  and `python tools/render_audit.py --check`.

### Step 5. Report failures back to their repos, not here

The audit reports. Fixing ValueNet, Ontology-of-Freedom or the ariadne annotator test is work in
those repos, and each is Aaron's call. List them for him with the evidence; do not fix silently.

### Step 6. Only then, the roadmap

When mappings are ratified and the sweep is complete, help Aaron choose **one thin vertical slice**
toward the synthetic moral person: the shortest chain of repos that would reach L5 together. Define
the roadmap as levels to reach, each checkable by the collector. Everything outside the slice is
explicitly paused, not counted as unfinished. Keep the roadmap computed from `audit.md`, not
written as a separate narrative document.

## 5. Known limits and traps

- **Windows paths.** `.claude/settings.json` in this repo holds permissions for
  `c:/Users/aaron/OneDrive/Documents/ariadne`. The tools use `pathlib` and `sys.executable` and
  should work on Windows, but they were only run on Linux. Check line endings: renders are written
  with `newline="\n"`, and a CRLF checkout of `audit.md` would fail `--check`. Consider adding
  `docs/05-evidence-audit/** text eol=lf` to `.gitattributes`.
- **ariadne's suite calls `python`.** `tests/e-pc/test_annotator_tool.py` invokes `python` by name;
  on Windows that may resolve to a different interpreter than the venv.
- **Private repositories** are cloned with the user's git credentials. The collector records only
  facts and test summaries, but the evidence JSON is committed to a public repo. Check that no
  private repository name or test output should stay private before committing.
- **Test counts are file counts.** They show that checks exist, not that they are good.
- **Deployment** is inferred from workflow files and a `gh-pages` branch; sites are not fetched.
- **Spec-index parsing** reads the markdown tables in `spec-index.md`. If Aaron restructures that
  file, `load_spec_index()` must follow, and `test_mappings_name_real_specs` will catch drift.

## 6. Repository list from Aaron

<!-- Aaron: paste the full list of repositories and their descriptions below.
     Any format is fine; the agent will reconcile it against `gh repo list` in Step 1. -->

| Repository | Description |
| --- | --- |
| | |

## 7. Related context (not required to continue)

The same conversation produced a Business Case Meta-Model v0.2 and a Business Case Conformance
Rubric v0.2, as Claude Docs. Aaron concluded that the business-case process had become governance
theatre for a one-person organization. That conclusion is why this audit measures evidence instead
of grading documents. Those docs are not inputs to this work.
