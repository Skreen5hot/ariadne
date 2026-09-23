"""Render docs/02-evidence/register.yaml as docs/02-evidence/register.md.

Usage: python tools/render_evidence_register.py [--check]
With --check, exit 1 if register.md is out of date instead of writing it.
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "docs" / "02-evidence"


def _cell(value):
    if value is None or value == []:
        return "—"
    if isinstance(value, list):
        return "<br>".join(_cell(v) for v in value)
    text = str(value).replace("|", "\\|")
    if text.startswith("https://fandaws.com/ontology/bfo/"):
        module, _, name = text.rpartition("/")[2].partition("#")
        return f"`{module.replace('valuenet-', 'vn-')}:{name}`"
    return text


def render(register):
    out = [
        "# Evidence register (rendered)",
        "",
        "Generated from `register.yaml` by `tools/render_evidence_register.py`. Do not edit by hand.",
        "Nothing in this table changes a claim's standing until Aaron ratifies it.",
        "",
        "## Load-bearing claims",
        "",
        "| ID | Claim | Kind | Citation as given | Current strength | Access | Fit | Proposed strength | Record |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for c in register["claims"]:
        out.append(
            f"| {c['id']} | {_cell(c['claim'])} | {_cell(c['kind'])} | {_cell(c['citation_as_given'])} | "
            f"{_cell(c['current_strength'])} | {_cell(c['access'])} | {_cell(c['fit'])} | "
            f"{_cell(c['proposed_strength'])} | [{c['id']}]({c['record']}) |"
        )
    out += [
        "",
        "## Candidate values",
        "",
        "| ID | Candidate | v1 claim | v1 citation | ValueNet kind | ValueNet class | Related ValueNet classes | Access | Proposed strength | Record |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for v in register["candidate_values"]:
        out.append(
            f"| {v['id']} | {_cell(v['candidate'])} | {_cell(v['v1_claim'])} | {_cell(v['v1_citation'])} | "
            f"{_cell(v['valuenet_kind'])} | {_cell(v['valuenet_iri'])} | {_cell(v['valuenet_related'])} | "
            f"{_cell(v['access'])} | {_cell(v['proposed_strength'])} | [{v['id']}]({v['record']}) |"
        )
    src = register["valuenet_source"]
    out += ["", f"ValueNet classes read from {src['repository']} at commit `{src['commit']}`.", ""]
    return "\n".join(out)


def main(argv):
    register = yaml.safe_load((EVIDENCE / "register.yaml").read_text(encoding="utf-8"))
    text = render(register)
    target = EVIDENCE / "register.md"
    if "--check" in argv:
        if not target.exists() or target.read_text(encoding="utf-8") != text:
            print("register.md is out of date; run python tools/render_evidence_register.py")
            return 1
        return 0
    target.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
