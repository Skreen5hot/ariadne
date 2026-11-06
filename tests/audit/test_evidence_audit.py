"""The evidence audit stays honest.

These tests pin three rules:
  1. Levels are computed, never asserted: no inventory entry or evidence record may carry one.
  2. The only human claims (which repo implements which spec) must name real spec-index entries.
  3. The ladder cannot be climbed by documents: docs-only code, failing tests, a test run from
     another commit, or a reference from documentation never earn the next level.
"""
from __future__ import annotations

import copy
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import evidence_audit as ea  # noqa: E402
import render_audit  # noqa: E402

FORBIDDEN = {"level", "status", "done", "production", "complete", "ready", "passing"}


@pytest.fixture(scope="module")
def inventory():
    return ea.load_inventory()


@pytest.fixture(scope="module")
def specs():
    return {s.name for s in ea.load_spec_index()}


@pytest.fixture(scope="module")
def evidence():
    return ea.load_evidence()


def test_inventory_header(inventory):
    assert inventory["schema"] == ea.INVENTORY_SCHEMA
    assert set(inventory["buildable_layers"]) <= {"Architecture", "Specifications", "Governance",
                                                  "Philosophy", "Foundation", "Communications"}


def test_inventory_asserts_no_levels(inventory):
    for r in inventory["repos"]:
        assert set(r) <= {"name", "owner", "role", "implements", "mapping_basis"}, r["name"]
        assert not FORBIDDEN & set(r), r["name"]
        assert r.get("mapping_basis"), f"{r['name']}: a mapping needs a stated basis"
        assert r.get("role") in ea.ROLES, f"{r['name']}: role must be one of {ea.ROLES}"


def test_repo_names_unique(inventory):
    names = [r["name"] for r in inventory["repos"]] + list(inventory.get("out_of_scope") or [])
    assert len(names) == len(set(names))


def test_mappings_name_real_specs(inventory, specs):
    for r in inventory["repos"]:
        for s in r.get("implements") or []:
            assert s in specs, f"{r['name']}: '{s}' is not in spec-index.md"
    for e in inventory.get("not_buildable") or []:
        assert e["spec"] in specs, f"not_buildable '{e['spec']}' is not in spec-index.md"
        assert e.get("reason")


def test_evidence_records_are_machine_shaped(inventory, evidence):
    names = {r["name"] for r in inventory["repos"]}
    for name, rec in evidence.items():
        assert rec["schema"] == ea.REPO_SCHEMA
        assert name in names, f"evidence for {name} but it is not inventoried"
        assert "level" not in rec, f"{name}: evidence may not carry a level"
        if rec.get("reachable", True):
            for key in ("head", "files", "tests", "ci", "references", "collected_at"):
                assert key in rec, f"{name}: missing {key}"
            run = rec.get("run")
            if run:
                assert run["sha"] and isinstance(run["exit_code"], int) and run["at"]


def test_rendered_audit_is_current():
    assert render_audit.main(["--check"]) == 0, "run: python tools/render_audit.py"


# ---------------------------------------------------------------- ladder rules on synthetic records

TODAY = date(2026, 10, 28)


def rec(name="x", source=10, tests=3, run_exit=0, run_sha="abc", refs=(), deploys=True, on_default=True):
    r = {
        "schema": ea.REPO_SCHEMA, "repo": name, "reachable": True,
        "collected_at": "2026-10-28T00:00:00+00:00",
        "head": {"sha": "abc", "date": "2026-10-27T00:00:00+00:00", "subject": ""},
        "files": {"source": source, "total": source + 5, "ontology": 0, "docs": 5, "other": 0},
        "tests": {"files": tests, "runner": "pytest", "examples": []},
        "ci": {"workflows": ["ci.yml"], "deploys": deploys, "scheduled": False, "on_default_branch": on_default},
        "references": list(refs),
        "run": None if run_exit is None else {"sha": run_sha, "exit_code": run_exit, "at": "2026-10-28T00:00:00+00:00",
                                              "command": "pytest", "duration_s": 1.0, "summary": [], "note": ""},
    }
    return r


def lvl(records, name="x"):
    return ea.repo_level(name, {r["repo"]: r for r in records}, TODAY)


def test_not_collected_is_l0():
    lv = ea.repo_level("ghost", {}, TODAY)
    assert lv.level == 0 and lv.missing


def test_documents_only_is_l0():
    assert lvl([rec(source=0)]).level == 0


def test_code_without_tests_is_l1():
    assert lvl([rec(tests=0)]).level == 1


def test_unrun_tests_are_l2():
    assert lvl([rec(run_exit=None)]).level == 2


def test_failing_tests_hold_at_l2():
    lv = lvl([rec(run_exit=1)])
    assert lv.level == 2 and lv.failing


def test_unrunnable_suite_is_l2_not_failing():
    r = rec(run_exit=1)
    r["run"]["outcome"] = "could_not_run"
    lv = lvl([r])
    assert lv.level == 2 and lv.not_runnable and not lv.failing


def test_run_from_another_commit_does_not_count():
    lv = lvl([rec(run_sha="old")])
    assert lv.level == 2 and not lv.failing


def test_passing_without_consumers_is_l3():
    assert lvl([rec()]).level == 3


def test_documentation_reference_is_not_use():
    consumer = rec(name="y", refs=[{"repo": "x", "kind": "docs", "file": "README.md"}])
    assert lvl([rec(), consumer]).level == 3


def test_code_reference_is_use():
    consumer = rec(name="y", refs=[{"repo": "x", "kind": "code", "file": "src/a.py"}])
    lv = lvl([rec(deploys=False), consumer])
    assert lv.level == 4 and lv.used_by == ["y"]


def test_production_needs_deploy_and_ci():
    consumer = rec(name="y", refs=[{"repo": "x", "kind": "manifest", "file": "package.json"}])
    assert lvl([rec(), consumer]).level == 5
    assert lvl([rec(on_default=False), consumer]).level == 4


def test_stale_evidence_is_flagged_not_hidden():
    old = rec()
    old["collected_at"] = "2026-01-01T00:00:00+00:00"
    lv = lvl([old])
    assert lv.stale and lv.level == 3


def test_unreachable_is_l0():
    lv = ea.repo_level("p", {"p": {"repo": "p", "reachable": False, "error": "auth"}}, TODAY)
    assert lv.level == 0 and lv.unreachable


def test_spec_takes_best_repo(inventory):
    inv = copy.deepcopy(inventory)
    inv["repos"] = [{"name": "a", "implements": ["S"]}, {"name": "b", "implements": ["S"]}]
    ev = {"a": rec(name="a", tests=0), "b": rec(name="b")}
    level, reps = ea.spec_level("S", inv, ev, TODAY)
    assert level == 3 and len(reps) == 2


def test_plain_node_tests_get_a_runner(tmp_path):
    import collect_evidence as ce
    tests = ["test/_assert.mjs", "test/M01.test.mjs", "test/M02.test.mjs"]
    assert ce.detect_runner(tmp_path, tests) == "node-test"
    assert ce.node_test_files(tests) == ["test/M01.test.mjs", "test/M02.test.mjs"]
    assert ce.detect_runner(tmp_path, ["docs/notes.md"]) == "none"
