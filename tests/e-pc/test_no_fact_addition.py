"""test_no_fact_addition: every entity in the perspective engine's output either appears in the scenario
graph or is tagged as a question or conjecture.

Two parts. The fixture part proves the checker catches what it must (a fact with a bad trace, a fact or an
evaluation naming an unknown entity) and passes what it must (a traced fact, a conjecture naming a new person).
The live part applies the rule to every arm-B output in the repository; A and C outputs are measured for the
safety outcome but are not asserted here, since only B is the perspective engine.
"""
from __future__ import annotations

import json

import pytest

from conftest import arm_output_files, epc


def _stmt(text, kind, entities, trace):
    return {"text": text, "kind": kind, "entities": entities, "trace": trace}


def test_checker_passes_clean_output(scenario, prose):
    out = {"sections": [{"name": "Attention", "statements": [
        _stmt("Margaret lives alone.", "fact", ["Margaret Okonjo"], "Margaret lives alone."),
        _stmt("Daniel works rotating shifts.", "fact", ["Daniel", "the distribution centre"], "works rotating shifts at a distribution centre"),
        _stmt("A social worker might be involved.", "conjecture", ["a social worker"], "none"),
        _stmt("Ask Daniel about his shift pattern.", "question", ["Daniel", "his employer"], "none"),
        _stmt("Margaret's wish to go home matters.", "evaluation", ["Margaret", "her house"], "I want my own bed."),
    ]}], "synthesis": []}
    r = epc.fabrication_check(out, scenario, prose)
    assert r["statements"] == 5
    assert r["fabricated"] == 0, r["details"]


def test_checker_flags_bad_trace(scenario, prose):
    out = {"sections": [{"name": "Analysis", "statements": [
        _stmt("Margaret has diabetes.", "fact", ["Margaret"], "Margaret has diabetes"),
    ]}], "synthesis": []}
    r = epc.fabrication_check(out, scenario, prose)
    assert r["fabricated"] == 1 and "trace not in prose" in r["details"][0]["reasons"]


def test_checker_flags_unknown_entity_in_fact_and_evaluation(scenario, prose):
    out = {"sections": [{"name": "Analysis", "statements": [
        _stmt("Margaret's daughter visits.", "fact", ["Margaret", "her daughter"], "Margaret lives alone."),
        _stmt("The social worker should be consulted.", "evaluation", ["the social worker"], "none"),
    ]}], "synthesis": []}
    r = epc.fabrication_check(out, scenario, prose)
    assert r["fabricated"] == 2
    assert all(any("unknown entities" in x for x in d["reasons"]) for d in r["details"])


def test_checker_flags_fact_without_trace(scenario, prose):
    out = {"sections": [], "synthesis": [_stmt("Daniel lives forty minutes away.", "fact", ["Daniel"], "none")]}
    r = epc.fabrication_check(out, scenario, prose)
    assert r["fabricated"] == 1 and "fact without trace" in r["details"][0]["reasons"]


def test_every_prose_entity_is_in_the_graph(scenario, prose):
    """The graph must name every person, organisation and document the prose names, or the checker would
    flag true facts. Checked by resolving every capitalised proper name in the prose."""
    import re
    idx = epc.entity_index(scenario)
    names = set(re.findall(r"\b(?:Dr\. )?[A-Z][a-z]+(?: [A-Z][a-z]+)+\b", prose))
    stop = {"Ward Two", "Community Hospital", "Regional Health", "Health Authority", "Adult Protective", "Protective Services",
            "Comfort Care", "Riverbend Community", "September Margaret", "Also Margaret"}
    unresolved = sorted(n for n in names if epc.resolve_entity(n, idx) is None and n not in stop
                        and not re.match(r"^(On|Also|Two|The|Whether|Nobody|No|Her|His|Also on|September|October) ", n))
    assert not unresolved, f"prose names not in the graph: {unresolved}"


@pytest.mark.parametrize("path", arm_output_files(), ids=lambda p: f"{p.parent.parent.name}/{p.name}")
def test_arm_B_outputs_add_no_facts(path, scenario, prose):
    if not path.name.startswith("B-"):
        pytest.skip("only arm B is the perspective engine")
    out = json.loads(path.read_text(encoding="utf-8"))
    if out.get("_unparsed"):
        pytest.fail(f"{path.name}: output could not be parsed as the contract JSON")
    r = epc.fabrication_check(out, scenario, prose)
    assert r["fabricated"] == 0, json.dumps(r["details"], indent=1)
