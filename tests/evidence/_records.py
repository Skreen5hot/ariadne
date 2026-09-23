"""Shared loaders for the evidence tests."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "docs" / "02-evidence"
CITATIONS = EVIDENCE / "citations"


def load_register():
    return yaml.safe_load((EVIDENCE / "register.yaml").read_text(encoding="utf-8"))


def load_record(path):
    text = Path(path).read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path}: record must open with YAML front matter"
    front, _, _ = text[4:].partition("\n---\n")
    return yaml.safe_load(front)


def all_records():
    return {p.name: load_record(p) for p in sorted(CITATIONS.glob("*.md"))}
