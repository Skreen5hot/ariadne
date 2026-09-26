"""test_arm_length_parity: prompt token counts for B and C are within 5%.

The frozen measure is the regex tokenizer in scoring/epc.py (no model tokenizer is vendored). Character counts
are checked as a second, coarser guard so that parity cannot be met by many short tokens on one side.
"""
from __future__ import annotations

from conftest import epc


def test_B_and_C_prompts_within_tolerance(cfg):
    r = epc.parity(cfg)
    assert r["passed"], r


def test_B_and_C_character_counts_within_tolerance(cfg):
    b, c = len(epc.build_prompt("B", cfg)), len(epc.build_prompt("C", cfg))
    assert abs(b - c) / max(b, c) <= cfg["length_parity_tolerance"], {"B_chars": b, "C_chars": c}


def test_B_and_C_share_structure(cfg):
    """Same number of sections and the same synthesis line; only operational content differs."""
    b = (epc.EPC / cfg["arm_files"]["B"]).read_text(encoding="utf-8")
    c = (epc.EPC / cfg["arm_files"]["C"]).read_text(encoding="utf-8")
    assert b.count("\nSection ") == 6 and c.count("\nSection ") == 6
    syn_b = [l for l in b.splitlines() if l.startswith("Synthesis.")]
    syn_c = [l for l in c.splitlines() if l.startswith("Synthesis.")]
    assert syn_b == syn_c and len(syn_b) == 1
    assert b.splitlines()[0] == c.splitlines()[0]


def test_contract_identical_across_arms(cfg):
    prompts = {arm: epc.build_prompt(arm, cfg) for arm in cfg["arms"]}
    contract = (epc.EPC / cfg["output_contract"]).read_text(encoding="utf-8").rstrip("\n")
    for arm, p in prompts.items():
        assert p.endswith(contract + "\n"), arm
