"""Every register entry validates against the evidence-program schema."""
import re
import subprocess
import sys

import pytest

from _records import EVIDENCE, ROOT, load_register

STRENGTHS = {"Strong", "Moderate", "Argued only", "Hypothesis"}
ACCESS = {"full_text", "abstract_only", "could_not_access", "not_applicable"}
FIT = {"supports", "partially_supports", "neighbouring_claim", "does_not_support", "could_not_assess"}
VN_KINDS = {"value_disposition", "value_role", "aimed_good", "constraint", "competency"}
VN_PREFIX = "https://fandaws.com/ontology/bfo/valuenet-"

REGISTER = load_register()
CLAIMS = REGISTER["claims"]
VALUES = REGISTER["candidate_values"]


def test_expected_ids_present():
    assert [c["id"] for c in CLAIMS] == [
        "F1", "F2", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8",
        "C1", "C4", "C4a", "C5", "C6", "C2", "C7", "C8", "H-P6",
    ]
    assert [v["id"] for v in VALUES] == [f"V{i:02d}" for i in range(1, 24)]


@pytest.mark.parametrize("entry", CLAIMS + VALUES, ids=lambda e: e["id"])
def test_common_fields(entry):
    assert entry["access"] in ACCESS
    assert entry["fit"] in FIT
    assert entry["proposed_strength"] in STRENGTHS | {None}
    assert entry["ratified"] is False, "only Aaron sets ratified: true"
    assert (EVIDENCE / entry["record"]).is_file()


@pytest.mark.parametrize("entry", CLAIMS, ids=lambda e: e["id"])
def test_claim_fields(entry):
    assert entry["current_strength"] in STRENGTHS
    assert entry["claim"] and entry["kind"]


@pytest.mark.parametrize("entry", CLAIMS + VALUES, ids=lambda e: e["id"])
def test_no_grade_without_source_unless_argument_or_hypothesis(entry):
    """An unopened source cannot justify an empirical grade."""
    if entry["access"] in {"could_not_access", "not_applicable"}:
        assert entry["proposed_strength"] in {None, "Argued only", "Hypothesis"}


@pytest.mark.parametrize("entry", VALUES, ids=lambda e: e["id"])
def test_valuenet_kind(entry):
    kind = entry["valuenet_kind"]
    assert kind in VN_KINDS | {None}
    iris = ([entry["valuenet_iri"]] if entry["valuenet_iri"] else []) + entry["valuenet_related"]
    for iri in iris:
        assert iri.startswith(VN_PREFIX) and re.fullmatch(r"[^#\s]+#[A-Za-z]+", iri), iri
    if kind == "value_disposition":
        assert entry["valuenet_iri"] and entry["valuenet_iri"].endswith(("Disposition",)), entry["id"]
    if kind == "value_role":
        assert entry["valuenet_iri"] and entry["valuenet_iri"].endswith("Role"), entry["id"]
    if kind in {"aimed_good", "constraint", "competency"}:
        # No ValueNet class exists for these kinds; an exact IRI would assert a false equivalence.
        assert entry["valuenet_iri"] is None, entry["id"]


def test_rendered_view_is_current():
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "render_evidence_register.py"), "--check"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout
