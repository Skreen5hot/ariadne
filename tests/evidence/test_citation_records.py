"""Every cited item has a record; no record without a source URL.

A record is the unit of verification. These tests enforce the parts of the record schema that
protect against contamination: a URL that was actually opened, an access level, a fit judged
against the exact claim, and a proposed strength that the fit and replication fields can bear.
"""
from __future__ import annotations

import re

import pytest

from conftest import ACCESS, CITATIONS, FITS, REPL_STATUS, RETRACTION, STRENGTHS

REQUIRED = {"id", "claim_id", "claim", "claim_source", "citation_as_given", "resolved", "finding",
            "fit", "fit_note", "replication", "retraction_check", "proposed_strength",
            "verified_by", "verified_on", "ratified"}
RESOLVED_REQUIRED = {"authors", "year", "title", "venue", "doi", "url_opened", "access"}
URL_RE = re.compile(r"^https?://\S+$")
ID_RE = re.compile(r"^(F\d|E\d|C\d[a-z]?|H-P6|V\d\d)(-\d|[a-z]|x)?$")


def _scope(register, section: str) -> bool:
    """True when the register declares the section verified; pending sections are skipped visibly."""
    scope = register.get("verification_scope") or {}
    assert scope.get(section) in {"verified", "pending"}, f"register must declare verification_scope.{section}"
    return scope[section] == "verified"


def _cited_ids(register) -> list[tuple[str, str]]:
    out = []
    if _scope(register, "claims"):
        for c in register["claims"]:
            out.append((c["id"], "claim"))
    if _scope(register, "values"):
        for v in register["values"]:
            if v["citations_as_given"]:
                out.append((v["id"], "value"))
    return out


def test_every_cited_item_has_a_record(register, records):
    have = {r["claim_id"] for r in records.values()}
    missing = [cid for cid, _ in _cited_ids(register) if cid not in have]
    assert not missing, f"cited items without a record: {missing}"


def test_record_count_matches_citations(register, records):
    """Each citation string in the register should have at least one record (extra 'x' records allowed)."""
    entries = (register["claims"] if _scope(register, "claims") else []) + (register["values"] if _scope(register, "values") else [])
    if not _scope(register, "values"):
        import warnings
        warnings.warn("register.verification_scope.values is pending: value records not required yet")
    for entry in entries:
        n_cit = len(entry["citations_as_given"])
        n_rec = sum(1 for r in records.values() if r["claim_id"] == entry["id"] and not r["id"].endswith("x"))
        if entry["id"] == "H-P6":
            assert n_rec == 1
            continue
        if n_cit:
            assert n_rec >= n_cit, f"{entry['id']}: {n_cit} citations but {n_rec} records"


def test_no_record_without_a_claim(register, records):
    ids = {c["id"] for c in register["claims"]} | {v["id"] for v in register["values"]}
    orphans = [r["id"] for r in records.values() if r["claim_id"] not in ids]
    assert not orphans, f"records for unknown claims: {orphans}"


@pytest.fixture(params=sorted(p.name for p in CITATIONS.glob("*.md")) if CITATIONS.exists() else [])
def record(request, records):
    name = request.param
    return next(r for r in records.values() if r["_file"] == name)


def test_record_shape(record):
    missing = REQUIRED - set(record)
    assert not missing, f"{record['_file']}: missing {sorted(missing)}"
    assert ID_RE.match(record["id"]), f"{record['_file']}: id {record['id']!r}"
    assert record["_file"].startswith(record["id"] + "-"), f"{record['_file']}: file name must start with id"
    res = record["resolved"]
    assert isinstance(res, dict) and not (RESOLVED_REQUIRED - set(res)), f"{record['_file']}: resolved keys"
    assert res["access"] in ACCESS, record["_file"]
    assert record["fit"] in FITS, record["_file"]
    assert record["proposed_strength"] in STRENGTHS, record["_file"]
    assert record["retraction_check"] in RETRACTION, record["_file"]
    rep = record["replication"]
    assert rep["status"] in REPL_STATUS, record["_file"]
    assert str(rep["searched"]).lower() in {"yes", "no", "true", "false"}, record["_file"]
    assert record["verified_by"] == "agent"
    assert record["ratified"] is False, f"{record['_file']}: only Aaron sets ratified"
    assert str(record["claim"]).strip() and str(record["finding"]).strip()


def test_record_has_source_url(record):
    """No record without a source URL. The one exception is a claim with no citation (H-P6)."""
    res = record["resolved"]
    if res["access"] == "not_applicable":
        assert record["claim_id"] == "H-P6" or record["citation_as_given"].lower().startswith("none"), \
            f"{record['_file']}: not_applicable access is only for uncited claims"
        return
    assert URL_RE.match(str(res["url_opened"])), f"{record['_file']}: url_opened must be an http(s) URL"
    if res["access"] == "could_not_access":
        assert res.get("urls_attempted"), f"{record['_file']}: could_not_access without urls_attempted"
        assert record["fit"] == "could_not_assess", f"{record['_file']}: could_not_access must have fit could_not_assess"


def test_record_quotation_limit(record):
    q = record.get("quotation") or ""
    assert len(str(q).split()) <= 25, f"{record['_file']}: quotation over 25 words"


def test_record_strength_is_borne_by_fit(record):
    """The strength rules: a poor fit cannot yield Strong or Moderate; Strong needs supports plus replication."""
    fit, strength, rep = record["fit"], record["proposed_strength"], record["replication"]
    if fit not in {"supports", "partially_supports"}:
        assert strength in {"Argued only", "Hypothesis"}, \
            f"{record['_file']}: fit {fit} cannot bear {strength}"
    if strength == "Strong":
        assert fit == "supports", f"{record['_file']}: Strong requires fit supports"
        assert str(rep["searched"]).lower() in {"yes", "true"}, f"{record['_file']}: Strong without a replication search"
        assert rep["status"] == "replicated", f"{record['_file']}: Strong with replication status {rep['status']}"
        assert rep.get("sources"), f"{record['_file']}: Strong with no replication sources opened"
    if strength == "Moderate":
        assert fit in {"supports", "partially_supports"}


def test_record_replication_sources_have_urls(record):
    for s in record["replication"].get("sources") or []:
        assert URL_RE.match(str(s.get("url_opened", ""))), f"{record['_file']}: replication source without url_opened"
