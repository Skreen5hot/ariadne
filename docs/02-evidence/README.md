# Integral Ethics v2 — Evidence

This directory turns the citations behind *Integral Ethics v2* into verification records. The records are written under delegation. Nothing here changes a claim's standing until Aaron ratifies it. The v1 manuscript (`docs/01-philosophy/integral-ethics.md`) is the historical record and is not edited.

## Status at 2026-09-23: no citation verified

**Not one citation could be opened.** The environment these records were made in allows outbound traffic only to GitHub. Every scholarly host tried was refused by the egress proxy (403 / `EGRESS_BLOCKED`): doi.org, api.crossref.org, api.openalex.org, PubMed, Europe PMC, Semantic Scholar, archive.org, the Stanford Encyclopedia, PhilPapers, publisher sites and author-hosted PDFs. Web-search snippets could be reached. They are not the source, and none was used to fill a field.

So each of the 42 records says `could_not_access` and stops, as ground rule 1 requires. The fields that would describe a source are empty on purpose. The work that did not need source access is done:

- the register, its schema and tests, and the record for every cited item;
- a strength proposal wherever the rules set one without reading a source (philosophical claims, uncited values, H-P6);
- a ValueNet kind for all 23 candidate values, citing ValueNet class IRIs read from the module files;
- v1 reference slips that can be confirmed inside this repository;
- the ratification document (`evidence-delta.md`) and the dispute list (`contested.md`).

To finish the verification, re-run it in an environment whose network policy allows at least `doi.org`, `api.crossref.org`, `api.openalex.org` and `pubmed.ncbi.nlm.nih.gov`, plus the publisher hosts those resolve to. See [the environment docs](https://code.claude.com/docs/en/claude-code-on-the-web) for how network policy is set.

## Files

| File | What it is |
| --- | --- |
| `register.yaml` | The machine-readable register: 19 load-bearing claims and 23 candidate values. The source of truth. |
| `register.md` | Rendered view of `register.yaml`. Regenerate with `python tools/render_evidence_register.py`; a test fails if it is stale. |
| `citations/<ID>-<slug>.md` | One verification record per claim or value. YAML front matter holds the record; a short note follows. |
| `evidence-delta.md` | Proposed status changes, rewordings, v1 reference corrections and ValueNet gaps. **This is the ratification document.** |
| `contested.md` | Known disputes and replication problems to check first, with what was and was not checked. |

## How to read a record

A record keeps two questions apart.

- **`finding`** is what the source reports, in our words, with its location. It is empty unless a source was opened.
- **`fit`** is whether that finding supports the exact claim in our register. A real paper can be a poor fit; `neighbouring_claim` means it supports some other claim, which the `fit_note` names.

Other fields:

- `resolved` is a list with one entry per cited work, since several claims cite more than one. Each entry has its own `access`. `as_given` repeats the citation exactly as the register gives it.
- `access_note` records why a source could not be opened. It is an addition to the task schema.
- `citation_in_v1_references` (candidate values only) copies the matching v1 reference-list line verbatim, with its line number. It was entered from recall and is not evidence of anything.
- `replication.status` is `null` when `searched` is `no`. None of the permitted statuses describes a search that never happened.
- `proposed_strength` is `null` when no rule can set it without reading the source. An access failure is not a downgrade.
- `valuenet_kind`, `valuenet_iri`, `valuenet_related` and `valuenet_kind_note` apply to V01–V23 only. `valuenet_iri` is set only when the candidate *is* the ValueNet class. `valuenet_related` lists classes that aim at it or neighbour it. No equivalence is asserted either way.

## Strength rules

Copied from the task brief. They are the only rules that set `proposed_strength`.

| Grade | Requires |
| --- | --- |
| Strong | A meta-analysis or systematic review, or at least two independent replications, all in a consistent direction, and fit = supports |
| Moderate | One or two primary studies with fit = supports, or a meta-analysis with high heterogeneity, or fit = partially_supports on otherwise strong evidence |
| Argued only | Philosophical or formal argument with no empirical component, or the claim is a presupposition rather than a finding |
| Hypothesis | No source supports the claim as stated; a test is planned |

A citation with fit = `neighbouring_claim` contributes nothing to the stated claim. A reworded claim goes in `evidence-delta.md`, never into the register directly.

## ValueNet

Candidate kinds use the BFO-Aligned ValueNet at [Skreen5hot/ValueNet](https://github.com/Skreen5hot/ValueNet), commit `204259911cd239413e3ed02db84f86b80e507a1d`. The IRIs come from `valuenet-core.ttl`, `valuenet-folk.ttl`, `valuenet-schwartz-values.ttl`, `valuenet-moral-foundations.ttl` and `valuenet-moral-epistemics.ttl`. Every IRI cited was checked against those files when the register was built. ValueNet's mapping annotations (`historicallyCorrespondsTo`, `conceptuallyMatches`) are not used here.

## E-PC (Phase 4) is not built here

The E2 machinery the brief asks E-PC to reuse is in another repository, [Skreen5hot/wrm-e2-independent-library-test](https://github.com/Skreen5hot/wrm-e2-independent-library-test). That includes the multi-relational completeness audit (`src/wrm_e2/mrc.py`), the freeze and hash logic (`freeze.py`, `hashing.py`), the permutation nulls (`nulls.py`, `significance.py`) and the preregistration convention (`preregistration/`). The WRM predecessor is in [Skreen5hot/worldview-realization-model](https://github.com/Skreen5hot/worldview-realization-model). As the brief instructs, `experiments/e-pc/` and `tests/e-pc/` were not created here and E2 was not re-implemented. Aaron needs to decide where E-PC lives.

## Running the tests

```bash
pip install pyyaml pytest
python -m pytest tests/evidence
```
