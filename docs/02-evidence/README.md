# Evidence program for Integral Ethics v2

This directory holds the verified evidence behind the load-bearing claims of
*Integral Ethics v2* (`docs/01-philosophy/integral-ethics-v2.md`) and the
candidate value citations carried over from v1
(`docs/01-philosophy/integral-ethics.md`, which is the v1 record and is never
edited here).

Nothing in this directory changes a claim's standing on its own. Records are
authored under delegation; Aaron ratifies every change of status. Until a row in
`evidence-delta.md` is ratified, the strength printed in v2 stands.

## How to read it

| File | What it is | Who writes it |
| --- | --- | --- |
| `register.yaml` | Machine-readable register: the 19 load-bearing claims (F1–H-P6) and the 23 candidate values (V01–V23), each with its citations as given, its current strength, the proposed strength derived from the records, and its ValueNet ontological kind | Agent proposes; Aaron ratifies (`ratified: true`) |
| `register.md` | Rendered view of `register.yaml`. Regenerate with `python tools/render_register.py`; never edit by hand | Generated |
| `citations/<ID>-<slug>.md` | One verification record per citation. YAML front matter (schema below) plus optional notes. `<ID>` is the claim id plus a letter when the claim has several citations | Agent |
| `evidence-delta.md` | The ratification document: one row per claim whose proposed strength differs from its current one, or whose wording should change to match its evidence, with the record that justifies it. Also holds the v1 reference corrections and the ValueNet gaps | Agent proposes; Aaron ratifies |
| `contested.md` | Items with a known dispute, formal critique or replication problem | Agent |

## Record schema

Each `citations/*.md` file opens with YAML front matter carrying exactly these keys
(see `tests/evidence/test_citation_records.py` for the enforced subset):

```yaml
id: E8                 # record id (claim id + letter when the claim has several citations)
claim_id: E8
claim: "Asking people beats imagining their view"
claim_source: "Integral Ethics v2, Cognitive perspectives as instruments"
citation_as_given: "Eyal, Steffel & Epley, JPSP (2018)"
resolved:
  authors:
  year:
  title:
  venue:
  doi:
  url_opened:          # the literal URL the verifier fetched to write `finding`
  urls_attempted: []   # everything else tried (mandatory when could_not_access)
  access: full_text | abstract_only | could_not_access | not_applicable
finding: |             # what the source reports, in the verifier's words, with location
fit: supports | partially_supports | neighbouring_claim | does_not_support | could_not_assess
fit_note: |            # why; if neighbouring_claim, what claim it does support
suggested_rewording: "" # for evidence-delta.md only; never applied to the register directly
replication:
  searched: yes | no
  status: replicated | mixed | failed | none_found | not_applicable
  sources: []
retraction_check: clean | retracted | expression_of_concern | not_checked
proposed_strength: Strong | Moderate | Argued only | Hypothesis
contested: ""
verified_by: agent
verified_on: 2026-09-26
ratified: false
```

The two questions a record answers are kept apart on purpose. `finding` says
what the source reports. `fit` says whether that supports the exact claim in
the register. A real paper can be a poor fit, and a poor fit contributes
nothing to the claim's grade.

## Strength rules

These are the only rules that set `proposed_strength`, for a record and for a
claim.

| Grade | Requires |
| --- | --- |
| Strong | A meta-analysis or systematic review, or at least two independent replications, all in a consistent direction, and fit = supports |
| Moderate | One or two primary studies with fit = supports, or a meta-analysis with high heterogeneity, or fit = partially_supports on otherwise strong evidence |
| Argued only | Philosophical or formal argument with no empirical component, or the claim is a presupposition rather than a finding |
| Hypothesis | No source supports the claim as stated; a test is planned |

A claim's proposed strength is the strongest grade its *fitting* records
justify under these rules, never the strongest grade among its records. A
citation with fit = neighbouring_claim is recorded and then set aside.

## Ground rules for verifiers

- No invented sources. Every DOI, URL, page number and quotation comes from a
  source the verifier opened. Otherwise `access: could_not_access` and stop.
- Quote at most 25 words, once per source, only when wording matters.
- Grade conservatively. A wrong "Strong" costs more than a wrong "Moderate".
- Report gaps, never fill them. An empty field is information.
- `docs/01-philosophy/integral-ethics.md` (v1) is never edited. Corrections to
  it are logged in `evidence-delta.md` under "v1 reference corrections".

## ValueNet

The BFO-Aligned ValueNet (<https://skreen5hot.github.io/ValueNet/>, modules
under Downloads; checksums verified against its `SHA256SUMS` on 2026-09-26) is
the ontological pattern for values here. `register.yaml` records, for each
candidate value, a `valuenet_kind` from the set
`value_disposition | value_role | aimed_good | constraint | competency` and the
ValueNet class IRI where one exists. Where no class exists the gap is logged in
`evidence-delta.md`; nothing is invented. ValueNet's own mappings to the
original ValueNet are annotation-only (`historicallyCorrespondsTo`,
`hasRelatedConceptualMatch`) and stay that way here.

## Tests

```bash
python -m pytest tests/evidence -q
```

`test_register_schema.py` validates every register entry. `test_citation_records.py`
checks that every cited item has a record, every record parses, and no record
lacks a source URL.

## Commit convention

One commit per verified citation, message `evidence: verify <ID> — <grade>`.
One pull request per phase (register, candidate values, evidence delta, E-PC
pilot).
