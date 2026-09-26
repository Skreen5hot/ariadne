# E-PC: Perspective Coverage Experiment (pilot)

The first real test of the perspective method of *Integral Ethics v2*. Read `PREREG.md` first;
it is the protocol and nothing here overrides it.

**State:** built, not run. `PREREG.md` is a draft until Aaron ratifies it (`PREREG.ratified`). The
gold annotation does not exist yet; it is produced by Aaron and an independent annotator, blind to
the arms, following `annotations/ANNOTATION_GUIDE.md`. No arm may be run credited before both.

## Layout

| Path | Content |
| --- | --- |
| `PREREG.md` | Pre-registration: hypothesis, materials, arms, outcomes, analysis, kill conditions, open items |
| `PREREG.ratified` | Written by Aaron at ratification: the SHA-256 of `PREREG.md`. Absent until then |
| `config.json` | Frozen run parameters (model, decoding, N, permutations, seed) |
| `scenarios/clinic-discharge.json` | Situation graph S=(E,R) in the E1 convention, plus explicit unknowns |
| `scenarios/clinic-discharge.txt` | The prose the arms see; the exact textual representation all offsets refer to |
| `scenarios/predicates.json` | The 20-predicate registry with relational domains, reused from E1 with provenance |
| `annotations/ANNOTATION_GUIDE.md` | How to produce the gold; the ValueNet annotation form |
| `annotations/gold.schema.json` | JSON Schema for gold and rater annotation files |
| `annotations/clinic-discharge.gold.json` | The adjudicated gold (absent until produced) |
| `arms/` | Frozen prompts A, B, C and the shared output contract |
| `scoring/epc.py` | E-PC's own functions: prompt assembly, tokenizer, MRC audit, fabrication check, coverage, agreement, permutation test, blind packing |
| `scoring/run_arms.py` | Runs the arms against the model; refuses a credited run without ratification |
| `scoring/analyze.py` | Computes outcomes and writes `results/<run_id>/results.json` and `report.md` |
| `scoring/RUBRIC.md` | The blind rater's instructions |
| `results/` | One directory per run; empty until a run exists |
| `../../tests/e-pc/` | The four pre-run tests named in the brief |

## Commands

```bash
python -m pytest tests/e-pc -q                                  # the four gates
python experiments/e-pc/scoring/epc.py mrc                      # multi-relational completeness profile
python experiments/e-pc/scoring/epc.py parity                   # B vs C prompt length
python experiments/e-pc/scoring/epc.py agreement A.json B.json  # inter-annotator agreement
python experiments/e-pc/scoring/epc.py build-value-layer        # value layer from the adjudicated gold
python experiments/e-pc/scoring/run_arms.py --dev               # development run (results/dev_<ts>/), never credited
python experiments/e-pc/scoring/run_arms.py --credited          # refuses without PREREG.ratified and a committed gold
python experiments/e-pc/scoring/epc.py blind-pack <run_id>      # strip labels, shuffle, write key
python experiments/e-pc/scoring/analyze.py <run_id>             # outcomes, permutation test, report
```

## Where E2 lives

The E2 machinery is not in this repository. It is in `Skreen5hot/wrm-e2-independent-library-test`
(code, `src/wrm_e2/`) and `Skreen5hot/worldview-realization-model` (E1 and the frozen scenario).
E-PC reuses their conventions and copies one data file (the predicate registry) with provenance.
It does not re-implement their code; see `PREREG.md` §11.
