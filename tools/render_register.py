"""Render docs/02-evidence/register.yaml and the citation records into docs/02-evidence/register.md.

Usage:  python tools/render_register.py            (writes register.md)
        python tools/render_register.py --check    (exit 1 if register.md is stale)

The rendered file is generated; never edit it by hand.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "02-evidence"
REGISTER = EVIDENCE / "register.yaml"
CITATIONS = EVIDENCE / "citations"
OUT = EVIDENCE / "register.md"


def load_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path.name}: no YAML front matter")
    end = text.find("\n---", 3)
    if end < 0:
        raise ValueError(f"{path.name}: unterminated front matter")
    return yaml.safe_load(text[3:end]) or {}


def load_records() -> dict[str, dict]:
    records: dict[str, dict] = {}
    if not CITATIONS.exists():
        return records
    for p in sorted(CITATIONS.glob("*.md")):
        fm = load_front_matter(p)
        fm["_file"] = p.name
        records[fm["id"]] = fm
    return records


def by_claim(records: dict[str, dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for r in records.values():
        out.setdefault(r.get("claim_id", ""), []).append(r)
    for v in out.values():
        v.sort(key=lambda r: r["id"])
    return out


def short_cite(r: dict) -> str:
    res = r.get("resolved") or {}
    authors = str(res.get("authors") or "").split(";")[0].strip()
    year = res.get("year") or ""
    return f"{authors} ({year})".strip() if authors else r.get("citation_as_given", "")


def esc(s: object) -> str:
    return str(s if s is not None else "").replace("|", "\\|").replace("\n", " ").strip()


def render_records_cell(recs: list[dict]) -> str:
    if not recs:
        return "none yet"
    parts = []
    for r in recs:
        parts.append(
            f"[{r['id']}](citations/{r['_file']}) {esc(short_cite(r))}: "
            f"{esc((r.get('resolved') or {}).get('access'))}, fit {esc(r.get('fit'))}, "
            f"proposed {esc(r.get('proposed_strength'))}"
        )
    return "<br>".join(parts)


def render(reg: dict, records: dict[str, dict]) -> str:
    grouped = by_claim(records)
    lines: list[str] = []
    lines.append("# Evidence register (rendered)")
    lines.append("")
    lines.append(
        "Generated from `register.yaml` and `citations/*.md` by `tools/render_register.py`. "
        "Do not edit by hand. Nothing here changes a claim's standing until `ratified` is true."
    )
    lines.append("")
    lines.append(f"Verified on: {reg.get('verified_on')}. Records: {len(records)}.")
    lines.append("")

    # Grade distribution
    dist: dict[str, int] = {}
    for r in records.values():
        g = str(r.get("proposed_strength"))
        dist[g] = dist.get(g, 0) + 1
    if dist:
        lines.append("Proposed strength across records: " + ", ".join(f"{k} {v}" for k, v in sorted(dist.items())) + ".")
        lines.append("")

    lines.append("## Load-bearing claims")
    lines.append("")
    lines.append("| ID | Claim | Kind | Current | Proposed | Status | Ratified | Records |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for c in reg["claims"]:
        recs = grouped.get(c["id"], [])
        lines.append(
            f"| {c['id']} | {esc(c['claim'])} | {esc(c['kind'])} | {esc(c['current_strength'])} | "
            f"{esc(c.get('proposed_strength') or 'pending')} | {esc(c['status'])} | {'yes' if c['ratified'] else 'no'} | "
            f"{render_records_cell(recs)} |"
        )
    lines.append("")

    lines.append("## Candidate values")
    lines.append("")
    lines.append("| ID | Candidate | ValueNet kind | ValueNet IRI | Related (annotation only) | v1 claim | Proposed | Status | Ratified | Records |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for v in reg["values"]:
        recs = grouped.get(v["id"], [])
        lines.append(
            f"| {v['id']} | {esc(v['candidate'])} | {esc(v['valuenet_kind'])} | {esc(v.get('valuenet_iri') or 'none')} | "
            f"{esc(', '.join(v.get('valuenet_related') or []) or 'none')} | {esc(v.get('v1_claim'))} | "
            f"{esc(v.get('proposed_strength') or 'pending')} | {esc(v['status'])} | {'yes' if v['ratified'] else 'no'} | "
            f"{render_records_cell(recs)} |"
        )
    lines.append("")
    lines.append("## Prefixes")
    lines.append("")
    for k, val in (reg.get("valuenet_prefixes") or {}).items():
        lines.append(f"- `{k}:` {val}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    reg = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    text = render(reg, load_records())
    if "--check" in argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print("register.md is stale; run python tools/render_register.py", file=sys.stderr)
            return 1
        return 0
    OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
