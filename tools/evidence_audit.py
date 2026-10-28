"""Shared model for the evidence audit (docs/05-evidence-audit).

The audit answers one question per specification and per repository: what does running
evidence show, as opposed to what a document says? Levels are COMPUTED here from the
machine-collected records in docs/05-evidence-audit/evidence/*.json. Nothing in the
inventory or the rendered view may assert a level; it can only be derived.

Evidence ladder (each level requires every level below it):

  L0 spec-only   a specification exists; no repository is mapped to it
  L1 code        a mapped repository contains source code (not only documents)
  L2 tested      the repository contains test files
  L3 passing     the collector ran the tests at a recorded commit and they passed
  L4 used        another inventoried repository depends on it in code or a manifest
                 (a reference from documentation does not count)
  L5 production  passing + used + deployed by automation + CI runs on the default branch

A repository whose tests ran and failed is held at L2 and marked FAILING. One whose suite
could not reach a verdict in a clean checkout (install failure, missing entry point, collection
error, timeout) is held at L2 and marked NOT RUNNABLE.
Evidence older than STALE_DAYS is shown as stale; the level still stands, flagged.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "05-evidence-audit"
INVENTORY = AUDIT / "inventory.yaml"
EVIDENCE = AUDIT / "evidence"
SPEC_INDEX = ROOT / "docs" / "00-foundation" / "spec-index.md"
OUT = AUDIT / "audit.md"

STALE_DAYS = 30
REPO_SCHEMA = "ariadne-evidence-audit/repo/v1"
INVENTORY_SCHEMA = "ariadne-evidence-audit/inventory/v1"

LEVELS = ["L0 spec-only", "L1 code", "L2 tested", "L3 passing", "L4 used", "L5 production"]


# ---------------------------------------------------------------- spec index

@dataclass
class Spec:
    name: str
    layer: str
    version: str
    status: str
    review: str


def load_spec_index(path: Path = SPEC_INDEX) -> list[Spec]:
    """Parse the hand-maintained spec-index.md tables. The index stays the single owner
    of spec names, versions and document status; the audit only reads it."""
    specs: list[Spec] = []
    layer = ""
    header: list[str] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## "):
            layer = line[3:].strip()
            header = None
            continue
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if set(line.replace("|", "").strip()) <= set("-: "):
            continue
        if layer.lower().startswith("thesis") or not header:
            continue
        row = dict(zip(header, cells))
        name = row.get("spec") or row.get("artifact")
        if not name:
            continue
        specs.append(Spec(
            name=name,
            layer=layer.replace(" Layer", ""),
            version=row.get("version", row.get("date", "")),
            status=row.get("status", row.get("purpose", "")),
            review=row.get("review result", ""),
        ))
    return specs


# ---------------------------------------------------------------- inventory + evidence

def load_inventory(path: Path = INVENTORY) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_evidence(directory: Path = EVIDENCE) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if directory.exists():
        for p in sorted(directory.glob("*.json")):
            rec = json.loads(p.read_text(encoding="utf-8"))
            out[rec["repo"]] = rec
    return out


def evidence_file(repo: str) -> Path:
    return EVIDENCE / f"{repo}.json"


# ---------------------------------------------------------------- level computation

@dataclass
class RepoLevel:
    repo: str
    level: int
    failing: bool = False
    not_runnable: bool = False     # suite exists but did not reach a verdict
    stale: bool = False
    missing: bool = False          # inventoried but never collected
    unreachable: bool = False      # collector could not read it
    used_by: list[str] = field(default_factory=list)
    why: list[str] = field(default_factory=list)


def _age_days(iso: str, today: date) -> int:
    d = datetime.fromisoformat(iso.replace("Z", "+00:00")).date()
    return (today - d).days


def consumers(evidence: dict[str, dict]) -> dict[str, list[str]]:
    """repo -> repos that reference it from code or a manifest (never from docs)."""
    out: dict[str, list[str]] = {}
    for src, rec in evidence.items():
        for ref in rec.get("references") or []:
            if ref["kind"] in {"code", "manifest"} and ref["repo"] != src:
                out.setdefault(ref["repo"], [])
                if src not in out[ref["repo"]]:
                    out[ref["repo"]].append(src)
    return {k: sorted(v) for k, v in out.items()}


def repo_level(repo: str, evidence: dict[str, dict], today: date | None = None) -> RepoLevel:
    today = today or datetime.now(timezone.utc).date()
    rec = evidence.get(repo)
    if rec is None:
        return RepoLevel(repo, 0, missing=True, why=["no evidence collected yet"])
    if not rec.get("reachable", True):
        return RepoLevel(repo, 0, unreachable=True, why=[rec.get("error", "collector could not read the repository")])
    lv = RepoLevel(repo, 0)
    lv.stale = _age_days(rec["collected_at"], today) > STALE_DAYS
    files = rec["files"]
    if files["source"] == 0:
        lv.why.append("no source files (documents only)")
        return lv
    lv.level = 1
    lv.why.append(f"{files['source']} source files")
    tests = rec["tests"]
    if tests["files"] == 0:
        lv.why.append("no test files")
        return lv
    lv.level = 2
    lv.why.append(f"{tests['files']} test files")
    run = rec.get("run")
    if not run:
        lv.why.append("tests not executed by the collector")
        return lv
    if run["sha"] != rec["head"]["sha"]:
        lv.why.append("test run is from an older commit")
        return lv
    outcome = run.get("outcome") or ("passed" if run["exit_code"] == 0 else "failed")
    if outcome == "could_not_run":
        lv.not_runnable = True
        lv.why.append("test suite could not run in a clean checkout")
        return lv
    if outcome != "passed":
        lv.failing = True
        lv.why.append("tests FAILED")
        tc = rec.get("toolchain") or {}
        pin, used = tc.get("node_pinned"), tc.get("node_used")
        if pin and used and pin.split(".")[0] != used.split(".")[0]:
            lv.why.append(f"collector ran Node {used}; repository pins {pin}, so some failures may be toolchain-only")
        return lv
    lv.level = 3
    lv.why.append(f"tests passed at {run['sha'][:7]} ({run['at'][:10]})")
    used_by = consumers(evidence).get(repo, [])
    lv.used_by = used_by
    if not used_by:
        lv.why.append("no inventoried repository depends on it in code")
        return lv
    lv.level = 4
    lv.why.append("used by " + ", ".join(used_by))
    ci = rec["ci"]
    if ci["deploys"] and ci["on_default_branch"]:
        lv.level = 5
        lv.why.append("deployed by automation; CI on default branch")
    else:
        lv.why.append("no automated deployment with CI on the default branch")
    return lv


def spec_level(spec_name: str, inventory: dict, evidence: dict[str, dict], today: date | None = None) -> tuple[int, list[RepoLevel]]:
    repos = [r["name"] for r in inventory.get("repos", []) if spec_name in (r.get("implements") or [])]
    levels = [repo_level(r, evidence, today) for r in repos]
    return (max((l.level for l in levels), default=0), levels)


def label(lv: RepoLevel) -> str:
    if lv.missing:
        return "not collected"
    if lv.unreachable:
        return "unreachable"
    s = LEVELS[lv.level]
    if lv.failing:
        s += " · FAILING"
    if lv.not_runnable:
        s += " · NOT RUNNABLE"
    if lv.stale:
        s += " · stale"
    return s


SLUG_RE = re.compile(r"[^A-Za-z0-9._-]")
