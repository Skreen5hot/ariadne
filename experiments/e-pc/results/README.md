# Results

Empty until a run exists. A credited run creates `results/<run_id>/` with:

| Path | Content |
| --- | --- |
| `manifest.json` | SHA-256 of PREREG.md, config.json, every arm file, the output contract, the scenario graph and prose, the gold, and `scoring/*.py`; model version string; timestamps |
| `raw/<arm>-<i>.request.json`, `raw/<arm>-<i>.response.json` | verbatim request and response bodies |
| `outputs/<arm>-<i>.json` | the parsed structured output (`sections`, `synthesis`) |
| `outputs/<arm>-<i>.txt` | the output's textual representation for rating (the raw text block) |
| `blind/PKT-<hash>.{json,txt}`, `blind/key.json` | label-stripped packets in seeded random order, and the key (opened only after ratings are committed) |
| `ratings/PKT-<hash>.rating.json` | the blind rater's annotations |
| `results.json` | coverage, fabrication, diversity, permutation test, effect sizes, distinct-output counts, `prereg_sha256`, outcome classification |
| `report.md` | the human-readable report |

Development runs (`run_arms.py --dev`) write to `results/dev_<timestamp>/`, which is git-ignored and
never credited. A development run against the real scenario is refused until the gold is committed,
for the same reason a credited one is: no arm output may exist before the gold.
