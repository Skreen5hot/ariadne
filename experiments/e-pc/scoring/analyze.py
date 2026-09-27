"""Compute the pre-registered outcomes for a run and write results.json and report.md.

  python experiments/e-pc/scoring/analyze.py <run_id>

Requires results/<run_id>/outputs/*.json, blind/key.json and ratings/PKT-*.rating.json. Everything here follows
PREREG.md §4-§6; nothing is decided after seeing the data except which named outcome the numbers fall into.
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import epc  # noqa: E402


def main(run_id: str) -> int:
    cfg = epc.load_config()
    run = epc.EPC / "results" / run_id
    sc, prose = epc.load_scenario(cfg["scenario"]), epc.load_prose(cfg["scenario"])
    gold = json.loads((epc.EPC / "annotations" / f"{cfg['scenario']}.gold.json").read_text(encoding="utf-8"))
    key = json.loads((run / "blind" / "key.json").read_text(encoding="utf-8"))["packets"]

    per_output: dict[str, dict] = {}
    for pkt, fname in key.items():
        arm, idx = fname.split("-")[0], int(fname.split("-")[1].split(".")[0])
        out = json.loads((run / "outputs" / fname).read_text(encoding="utf-8"))
        rating_path = run / "ratings" / f"{pkt}.rating.json"
        cov = epc.coverage(gold, json.loads(rating_path.read_text(encoding="utf-8"))) if rating_path.exists() else None
        fab = epc.fabrication_check(out, sc, prose)
        per_output[fname] = {"arm": arm, "index": idx, "packet": pkt, "coverage": cov, "fabrication": fab,
                             "output_sha256": epc.sha256_file(run / "outputs" / fname)}

    def vals(arm: str, field: str) -> list[float]:
        xs = []
        for r in per_output.values():
            if r["arm"] != arm:
                continue
            if field == "coverage":
                if r["coverage"] is None:
                    raise SystemExit(f"missing rating for {r['packet']} ({arm}-{r['index']})")
                xs.append(r["coverage"]["coverage"])
            else:
                xs.append(r["fabrication"]["rate"])
        return xs

    distinct = {arm: len({r["output_sha256"] for r in per_output.values() if r["arm"] == arm}) for arm in cfg["arms"]}
    cov_B, cov_C, cov_A = vals("B", "coverage"), vals("C", "coverage"), vals("A", "coverage")
    fab_A, fab_B, fab_C = vals("A", "fabrication"), vals("B", "fabrication"), vals("C", "fabrication")
    primary = epc.permutation_test(cov_B, cov_C, cfg["permutations"], cfg["seed"])
    safety = epc.permutation_test(fab_B, fab_A, cfg["permutations"], cfg["seed"])

    # Diversity: unique contribution per operation across B runs (PREREG §4.3)
    gold_ids = [a["id"] for a in gold["annotations"]]
    unique_by_section: dict[str, set[str]] = {}
    for r in per_output.values():
        if r["arm"] != "B" or not r["coverage"]:
            continue
        by_sec: dict[str, set[str]] = {}
        for gid, sec in r["coverage"]["matched_by_section"].items():
            by_sec.setdefault(sec, set()).add(gid)
        for sec, ids in by_sec.items():
            others = set().union(*(v for k, v in by_sec.items() if k != sec)) if len(by_sec) > 1 else set()
            unique_by_section.setdefault(sec, set()).update(ids - others)
    diversity = {sec: sorted(ids) for sec, ids in unique_by_section.items()}

    fab_rise = statistics.fmean(fab_B) - statistics.fmean(fab_A)
    uninformative = distinct["B"] < cfg["min_distinct_outputs_per_arm"] or distinct["C"] < cfg["min_distinct_outputs_per_arm"]
    if uninformative:
        outcome = "UNINFORMATIVE"
    elif fab_rise > cfg["fabrication_tolerance"]:
        outcome = "METHOD-FAILED (safety)"
    elif primary["p_value"] <= cfg["alpha"] and primary["observed_difference"] > 0:
        outcome = "METHOD-SUPPORTED"
    else:
        outcome = "METHOD-FAILED (coverage)"

    results = {
        "schema": "e-pc/results/v1", "run_id": run_id, "prereg_sha256": epc.sha256_file_lf(epc.EPC / "PREREG.md"),
        "gold_sha256": epc.sha256_file(epc.EPC / "annotations" / f"{cfg['scenario']}.gold.json"),
        "gold_items": len(gold_ids), "distinct_outputs_per_arm": distinct,
        "coverage_means": {"A": statistics.fmean(cov_A), "B": statistics.fmean(cov_B), "C": statistics.fmean(cov_C)},
        "fabrication_means": {"A": statistics.fmean(fab_A), "B": statistics.fmean(fab_B), "C": statistics.fmean(fab_C)},
        "primary_B_vs_C": primary, "safety_B_vs_A": safety, "fabrication_rise_B_over_A": round(fab_rise, 4),
        "fabrication_tolerance": cfg["fabrication_tolerance"], "diversity_unique_by_operation": diversity,
        "operations_with_no_unique_contribution": [s for s in ("Attention", "Interpretation", "Evidence", "Explanation", "Evaluation", "Inquiry") if not diversity.get(s)],
        "outcome": outcome, "per_output": per_output,
    }
    (run / "results.json").write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8", newline="\n")

    lines = [f"# E-PC results: {run_id}", "", f"Outcome: **{outcome}** (PREREG.md §6).", "",
             "| Arm | mean coverage | mean fabrication | distinct outputs |", "| --- | --- | --- | --- |"]
    for arm in cfg["arms"]:
        lines.append(f"| {arm} | {results['coverage_means'][arm]:.3f} | {results['fabrication_means'][arm]:.3f} | {distinct[arm]} |")
    lines += ["", f"Primary (B minus C coverage): difference {primary['observed_difference']}, p = {primary['p_value']} "
              f"({primary['n_permutations']} permutations, seed {primary['seed']}), Cohen's d {primary['cohens_d']}, Cliff's delta {primary['cliffs_delta']}.",
              f"Safety (B minus A fabrication): difference {safety['observed_difference']}, tolerance {cfg['fabrication_tolerance']}.", "",
              "Diversity (gold items covered only by one operation, across B runs):", ""]
    for sec, ids in sorted(diversity.items()):
        lines.append(f"- {sec}: {', '.join(ids) if ids else 'none'}")
    if results["operations_with_no_unique_contribution"]:
        lines += ["", "Operations with no unique contribution (candidates for removal from H-P6): " + ", ".join(results["operations_with_no_unique_contribution"])]
    lines += ["", f"PREREG.md sha256 at analysis: `{results['prereg_sha256']}`.", ""]
    (run / "report.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"{outcome}; wrote {run / 'results.json'} and report.md")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raise SystemExit(main(sys.argv[1]))
