"""Shared helpers and fixtures for the evidence tests (kept out of conftest so the two test packages do not shadow each other)."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "docs" / "02-evidence"
REGISTER = EVIDENCE / "register.yaml"
CITATIONS = EVIDENCE / "citations"

STRENGTHS = {"Strong", "Moderate", "Argued only", "Hypothesis"}
FITS = {"supports", "partially_supports", "neighbouring_claim", "does_not_support", "could_not_assess"}
ACCESS = {"full_text", "abstract_only", "could_not_access", "not_applicable"}
REPL_STATUS = {"replicated", "mixed", "failed", "none_found", "not_applicable"}
RETRACTION = {"clean", "retracted", "expression_of_concern", "not_checked"}
VALUENET_KINDS = {"value_disposition", "value_role", "aimed_good", "constraint", "competency"}
STATUSES = {"unverified", "verified", "ratified"}


def load_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---"), f"{path.name}: no YAML front matter"
    end = text.find("\n---", 3)
    assert end > 0, f"{path.name}: unterminated front matter"
    data = yaml.safe_load(text[3:end])
    assert isinstance(data, dict), f"{path.name}: front matter is not a mapping"
    return data


@pytest.fixture(scope="session")
def register() -> dict:
    return yaml.safe_load(REGISTER.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def records() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(CITATIONS.glob("*.md")) if CITATIONS.exists() else []:
        fm = load_front_matter(p)
        fm["_file"] = p.name
        assert fm.get("id"), f"{p.name}: missing id"
        assert fm["id"] not in out, f"duplicate record id {fm['id']} ({p.name} and {out[fm['id']]['_file']})"
        out[fm["id"]] = fm
    return out
