"""Unit tests for E-PC's own scoring functions (coverage, agreement, permutation test, annotation validation).

These are not the four pre-run gates; they pin the arithmetic that analyze.py relies on so that a credited run
cannot be scored by code that has never been exercised.
"""
from __future__ import annotations

import json

import pytest

from epc_helpers import EPC_DIR, epc


def _ann(aid, start, end, text, dtype, bearer, kind="violation", ptype="mf:HarmProcess", gold_id=None, section=None):
    proc = {"id": f"P{aid}", "type": ptype, "kind": kind, "disposition_type": dtype, "bearer": bearer, "label": f"label {aid}"}
    if gold_id:
        proc["gold_id"] = gold_id
    if section:
        proc["section"] = section
    return {"id": aid, "type": "vn-core:ValueEvidenceAnnotation",
            "hasEvidenceSource": {"id": f"S{aid}", "type": "vn-core:TextSpan", "hasTextualSequenceValue": text, "isTextSpanOf": "TR"},
            "hasSelector": {"id": f"SEL{aid}", "type": "vn-core:TextSpanSelector", "hasSourceRepresentation": "TR",
                            "selectsTextSpan": f"S{aid}", "hasStartOffset": start, "hasEndOffset": end},
            "isEvidenceFor": proc}


def _file(annotations, text, role="gold", annotator="adjudicated"):
    return {"schema": "e-pc/annotations/v1",
            "textual_representation": {"id": "TR", "file": "scenarios/clinic-discharge.txt", "sha256": epc.sha256_text(text), "codepoint_length": len(text)},
            "annotator": annotator, "role": role, "date": "2026-09-26", "annotations": annotations}


def test_permutation_test_detects_clear_difference():
    r = epc.permutation_test([0.8, 0.9, 0.85, 0.95, 0.9], [0.5, 0.55, 0.5, 0.6, 0.45], n_perm=2000, seed=1)
    assert r["observed_difference"] > 0.3
    assert r["p_value"] < 0.05
    assert r["cliffs_delta"] == 1.0


def test_permutation_test_no_difference_is_not_significant():
    r = epc.permutation_test([0.6, 0.7, 0.65, 0.6, 0.7], [0.7, 0.6, 0.65, 0.7, 0.6], n_perm=2000, seed=1)
    assert r["p_value"] > 0.2


def test_permutation_test_is_deterministic():
    a = epc.permutation_test([0.7, 0.8, 0.6], [0.5, 0.6, 0.4], n_perm=500, seed=20260926)
    b = epc.permutation_test([0.7, 0.8, 0.6], [0.5, 0.6, 0.4], n_perm=500, seed=20260926)
    assert a == b


def test_coverage_counts_matched_gold_items_once():
    gold = _file([_ann("G1", 0, 5, "x", "mf:CareDisposition", "P-PAT"),
                  _ann("G2", 10, 15, "y", "mf:LibertyDisposition", "P-PAT", ptype="mf:OppressionProcess"),
                  _ann("G3", 20, 25, "z", "folk:AutonomyDisposition", "P-SON", kind="realization", ptype="vn-core:ValueRealizationProcess")], "a" * 30)
    rating = _file([_ann("R1", 0, 5, "x", "mf:CareDisposition", "P-PAT", gold_id="G1", section="Attention"),
                    _ann("R2", 6, 9, "x", "mf:CareDisposition", "P-PAT", gold_id="G1", section="Evaluation"),
                    _ann("R3", 10, 15, "y", "mf:LibertyDisposition", "P-SON", ptype="mf:OppressionProcess", gold_id="G2"),
                    _ann("R4", 20, 25, "z", "folk:AutonomyDisposition", "P-SON", kind="realization", ptype="vn-core:ValueRealizationProcess", gold_id="G9")],
                   "b" * 30, role="rater", annotator="rater")
    c = epc.coverage(gold, rating)
    assert c["gold_items"] == 3
    assert c["covered"] == 1                      # G1 once; G2 bearer mismatch; G9 unknown
    assert c["matched_by_section"] == {"G1": "Attention"}
    assert len(c["invalid"]) == 2
    assert abs(c["coverage"] - 1 / 3) < 1e-9


def test_agreement_span_and_kappa():
    text = "a" * 100
    a = _file([_ann("A1", 0, 10, "x", "mf:CareDisposition", "P-PAT"), _ann("A2", 50, 60, "y", "mf:FairnessDisposition", "P-CM", ptype="mf:CheatingProcess")], text)
    b = _file([_ann("B1", 2, 12, "x", "mf:CareDisposition", "P-PAT"), _ann("B2", 80, 90, "z", "mf:LibertyDisposition", "P-PAT", ptype="mf:OppressionProcess")], text, annotator="other")
    r = epc.agreement(a, b)
    assert r["span_agreement_a_in_b"] == 0.5 and r["span_agreement_b_in_a"] == 0.5
    assert r["process_keys_union"] == 3 and r["process_keys_both"] == 1
    assert -1.0 <= r["process_kappa"] <= 1.0


def test_validate_annotations_accepts_a_correct_span(tmp_path, prose):
    span = "I want my own bed."
    (s, e), = epc.codepoint_offsets(span, prose)
    f = _file([_ann("G1", s, e, span, "folk:AutonomyDisposition", "P-PAT", kind="realization", ptype="vn-core:ValueRealizationProcess")], prose)
    p = tmp_path / "g.json"
    p.write_text(json.dumps(f), encoding="utf-8")
    errs = epc.validate_annotations(p, EPC_DIR / "scenarios" / "clinic-discharge.txt")
    assert errs == [], errs


def test_validate_annotations_rejects_bad_offsets_bearer_and_pairing(tmp_path, prose):
    span = "I want my own bed."
    (s, e), = epc.codepoint_offsets(span, prose)
    bad = _file([_ann("G1", s + 1, e, span, "mf:CareDisposition", "P-PAT"),                  # offsets do not delimit span
                 _ann("G2", s, e, span, "mf:CareDisposition", "P-NOBODY"),                   # bearer not in graph
                 _ann("G3", s, e, span, "mf:FairnessDisposition", "P-PAT")], prose)          # HarmProcess must contravene Care
    p = tmp_path / "g.json"
    p.write_text(json.dumps(bad), encoding="utf-8")
    errs = epc.validate_annotations(p, EPC_DIR / "scenarios" / "clinic-discharge.txt")
    assert any("do not delimit" in x for x in errs)
    assert any("P-NOBODY" in x for x in errs)
    assert any("contravenes mf:CareDisposition" in x for x in errs)


def test_valuenet_names_are_loaded_from_vendored_modules():
    names = epc.valuenet_local_names()
    assert "HarmProcess" in names["mf"] and "CareDisposition" in names["mf"]
    assert "AccountabilityRole" in names["folk"]
    assert "ValueEvidenceAnnotation" in names["vn-core"]


def test_mrc_gate_passes_for_the_frozen_scenario(cfg):
    r = epc.mrc_profile()
    assert r["passed"], r["flags"]
    assert r["all_domains_nonzero"]
