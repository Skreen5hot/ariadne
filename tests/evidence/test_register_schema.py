"""Every register entry validates.

The register is the machine-readable list of the 19 load-bearing claims of Integral Ethics v2
and the 23 candidate values. These tests pin its shape so that a proposed strength can never
appear without records, and a ratified flag can never appear without a status to match.
"""
from __future__ import annotations

import re

import pytest

from conftest import CITATIONS, STATUSES, STRENGTHS, VALUENET_KINDS

CLAIM_IDS = ["F1", "F2", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8",
             "C1", "C4", "C4a", "C5", "C6", "C2", "C7", "C8", "H-P6"]
VALUE_IDS = [f"V{i:02d}" for i in range(1, 24)]

CLAIM_KEYS = {"id", "claim", "claim_source", "kind", "citations_as_given", "current_strength",
              "proposed_strength", "records", "status", "ratified"}
VALUE_KEYS = {"id", "candidate", "v1_tier", "first_pass_role", "v1_claim", "citations_as_given",
              "valuenet_kind", "valuenet_iri", "valuenet_related", "valuenet_note",
              "proposed_strength", "records", "status", "ratified"}

IRI_RE = re.compile(r"^(vn-core|folk|schwartz|mf):[A-Za-z]+$")


def test_register_header(register):
    assert register["schema"] == "ariadne-evidence/register/v1"
    assert set(register["verification_scope"]) == {"claims", "values"}
    assert all(v in {"verified", "pending"} for v in register["verification_scope"].values())
    assert set(register["valuenet_prefixes"]) == {"vn-core", "folk", "schwartz", "mf"}
    for v in register["valuenet_prefixes"].values():
        assert v.startswith("https://fandaws.com/ontology/bfo/valuenet-")


def test_claim_ids_exact(register):
    assert [c["id"] for c in register["claims"]] == CLAIM_IDS


def test_value_ids_exact(register):
    assert [v["id"] for v in register["values"]] == VALUE_IDS


def _common_checks(entry: dict, keys: set[str]):
    missing = keys - set(entry)
    extra = set(entry) - keys
    assert not missing, f"{entry.get('id')}: missing keys {sorted(missing)}"
    assert not extra, f"{entry.get('id')}: unexpected keys {sorted(extra)}"
    assert isinstance(entry["citations_as_given"], list)
    assert all(isinstance(c, str) and c.strip() for c in entry["citations_as_given"])
    assert entry["status"] in STATUSES, entry["id"]
    assert isinstance(entry["ratified"], bool), entry["id"]
    ps = entry["proposed_strength"]
    assert ps is None or ps in STRENGTHS, f"{entry['id']}: proposed_strength {ps!r}"
    assert isinstance(entry["records"], list)
    if ps is not None:
        if entry["citations_as_given"]:
            assert entry["records"], f"{entry['id']}: proposed_strength set without records"
        else:
            # An uncited item is Argued only by rule; it has no records to point at.
            assert ps in {"Argued only", "Hypothesis"}, f"{entry['id']}: uncited item proposed {ps}"
        assert entry["status"] in {"verified", "ratified"}, f"{entry['id']}: proposed_strength set but status {entry['status']}"
    if entry["ratified"]:
        assert entry["status"] == "ratified", f"{entry['id']}: ratified without status ratified"
        assert ps is not None, f"{entry['id']}: ratified without proposed_strength"
    for rid in entry["records"]:
        matches = list(CITATIONS.glob(f"{rid}-*.md"))
        assert len(matches) == 1, f"{entry['id']}: record {rid} has {len(matches)} files"


@pytest.mark.parametrize("idx", range(len(CLAIM_IDS)))
def test_claim_entry(register, records, idx):
    c = register["claims"][idx]
    _common_checks(c, CLAIM_KEYS)
    assert c["current_strength"] in STRENGTHS, c["id"]
    assert c["claim"].strip() and c["claim_source"].strip() and c["kind"].strip()
    if c["id"] == "H-P6":
        assert c["citations_as_given"] == []
        assert c["current_strength"] == "Hypothesis"
    else:
        assert c["citations_as_given"], f"{c['id']}: no citations"
    for rid in c["records"]:
        assert rid in records, f"{c['id']}: record {rid} not parsed"
        assert records[rid]["claim_id"] == c["id"], f"{rid} belongs to {records[rid]['claim_id']}, listed under {c['id']}"


@pytest.mark.parametrize("idx", range(len(VALUE_IDS)))
def test_value_entry(register, records, idx):
    v = register["values"][idx]
    _common_checks(v, VALUE_KEYS)
    assert v["valuenet_kind"] in VALUENET_KINDS, v["id"]
    iri = v["valuenet_iri"]
    assert iri is None or IRI_RE.match(iri), f"{v['id']}: valuenet_iri {iri!r} must be null or prefix:LocalName"
    assert isinstance(v["valuenet_related"], list)
    for rel in v["valuenet_related"]:
        assert IRI_RE.match(rel), f"{v['id']}: related {rel!r}"
    # A disposition or role must name its class; a good, constraint or competency must not claim one.
    if v["valuenet_kind"] in {"value_disposition", "value_role"}:
        assert iri is not None, f"{v['id']}: {v['valuenet_kind']} without a ValueNet class"
    else:
        assert iri is None, f"{v['id']}: {v['valuenet_kind']} must not claim a ValueNet class as identity"
    if not v["citations_as_given"]:
        # Uncited values are Argued only by rule; nothing else may be proposed.
        assert v["proposed_strength"] in (None, "Argued only"), v["id"]
    for rid in v["records"]:
        assert rid in records, f"{v['id']}: record {rid} not parsed"
        assert records[rid]["claim_id"] == v["id"]


def test_valuenet_iris_exist_in_modules(register):
    """Every IRI the register names must be a class in the downloaded ValueNet modules
    (docs/02-evidence/valuenet/*.ttl, pinned by SHA256SUMS)."""
    from conftest import EVIDENCE
    vn = EVIDENCE / "valuenet"
    if not vn.exists():
        pytest.skip("ValueNet modules not vendored")
    corpus = "\n".join(p.read_text(encoding="utf-8") for p in vn.glob("*.ttl"))
    prefixes = register["valuenet_prefixes"]
    names = []
    for v in register["values"]:
        if v["valuenet_iri"]:
            names.append(v["valuenet_iri"])
        names.extend(v["valuenet_related"])
    for n in names:
        p, local = n.split(":", 1)
        full = f"<{prefixes[p]}{local}>"
        assert full in corpus, f"{n} not found in ValueNet modules"
