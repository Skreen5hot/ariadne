"""Every cited item has a record; no record claims a source without a URL."""
import pytest

from _records import CITATIONS, all_records, load_register

REGISTER = load_register()
ENTRIES = REGISTER["claims"] + REGISTER["candidate_values"]
RECORDS = all_records()

REQUIRED = [
    "id", "claim", "claim_source", "citation_as_given", "resolved", "finding", "fit", "fit_note",
    "replication", "retraction_check", "proposed_strength", "verified_by", "verified_on", "ratified",
]
RESOLVED_FIELDS = ["authors", "year", "title", "venue", "doi", "url_opened", "access"]


def test_every_register_entry_has_exactly_one_record():
    ids = sorted(r["id"] for r in RECORDS.values())
    assert ids == sorted(e["id"] for e in ENTRIES)
    for entry in ENTRIES:
        name = entry["record"].split("/")[-1]
        assert name in RECORDS and RECORDS[name]["id"] == entry["id"]
        assert name.startswith(entry["id"] + "-")


def test_no_orphan_files():
    assert all(p.suffix == ".md" for p in CITATIONS.iterdir())


@pytest.mark.parametrize("name", sorted(RECORDS))
def test_record_schema(name):
    rec = RECORDS[name]
    for field in REQUIRED:
        assert field in rec, f"{name}: missing {field}"
    assert rec["verified_by"] == "agent"
    assert rec["ratified"] is False
    assert rec["retraction_check"] in {"clean", "retracted", "expression_of_concern", "not_checked"}
    rep = rec["replication"]
    assert rep["searched"] in {"yes", "no"}
    if rep["searched"] == "no":
        assert rep["status"] is None and rep["sources"] == []
    else:
        assert rep["status"] in {"replicated", "mixed", "failed", "none_found", "not_applicable"}


@pytest.mark.parametrize("name", sorted(RECORDS))
def test_every_cited_item_is_resolved_or_marked(name):
    rec = RECORDS[name]
    resolved = rec["resolved"]
    assert isinstance(resolved, list)
    if rec["citation_as_given"]:
        assert resolved, f"{name}: citation given but nothing resolved or marked"
    for item in resolved:
        for field in RESOLVED_FIELDS:
            assert field in item, f"{name}: resolved item missing {field}"
        assert item["access"] in {"full_text", "abstract_only", "could_not_access"}


@pytest.mark.parametrize("name", sorted(RECORDS))
def test_no_record_without_a_source_url(name):
    """A record may describe a source only if it names the URL that was opened."""
    rec = RECORDS[name]
    opened = [i for i in rec["resolved"] if i["access"] != "could_not_access"]
    for item in opened:
        assert item["url_opened"], f"{name}: {item.get('as_given')} marked opened with no url_opened"
    if not opened:
        # Nothing was opened, so nothing may be said about any source.
        for item in rec["resolved"]:
            assert all(item[f] is None for f in RESOLVED_FIELDS if f != "access"), name
        assert rec["finding"] is None, f"{name}: finding recorded without an opened source"
        assert rec["fit"] == "could_not_assess", name
        assert rec["retraction_check"] == "not_checked", name


@pytest.mark.parametrize("name", sorted(RECORDS))
def test_quotation_limit(name):
    rec = RECORDS[name]
    quote = rec.get("quotation")
    if quote:
        assert len(quote.split()) <= 25, f"{name}: quotation over 25 words"
