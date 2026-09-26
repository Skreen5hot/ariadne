"""test_prereg_frozen: PREREG.md hash matches the hash recorded in the results file.

Also: if PREREG.ratified exists, it must match PREREG.md (a ratified protocol is never edited), and every
results.json and manifest.json must carry that same hash.
"""
from __future__ import annotations

import json

import pytest

from conftest import EPC_DIR, epc


def prereg_hash() -> str:
    return epc.sha256_file_lf(EPC_DIR / "PREREG.md")


def ratified_hash() -> str | None:
    rat = EPC_DIR / "PREREG.ratified"
    if not rat.exists():
        return None
    for line in rat.read_text(encoding="utf-8").splitlines():
        if line.startswith("sha256 "):
            return line.split()[1]
    pytest.fail("PREREG.ratified exists but has no 'sha256 <hash>' line")


def test_ratified_hash_matches_prereg():
    h = ratified_hash()
    if h is None:
        pytest.skip("PREREG.md not yet ratified (no PREREG.ratified)")
    assert h == prereg_hash(), "PREREG.md was edited after ratification"


def test_results_record_current_prereg_hash():
    results = sorted((EPC_DIR / "results").glob("*/results.json"))
    manifests = sorted((EPC_DIR / "results").glob("*/manifest.json"))
    if not results and not manifests:
        pytest.skip("no results yet")
    h = prereg_hash()
    for r in results:
        data = json.loads(r.read_text(encoding="utf-8"))
        assert data.get("prereg_sha256") == h, f"{r.parent.name}: results.json prereg_sha256 differs from PREREG.md"
    for m in manifests:
        data = json.loads(m.read_text(encoding="utf-8"))
        if data.get("mode") == "smoke":
            continue
        assert data.get("prereg_sha256") == h, f"{m.parent.name}: manifest prereg_sha256 differs from PREREG.md"
        if data.get("mode") == "credited":
            assert ratified_hash() == h, f"{m.parent.name}: credited run without a matching PREREG.ratified"
