"""Build annotator.html and PALETTE.md from annotator.template.html and the repository files, embedding the exact
entity ids, the ValueNet classes with their own labels and definitions, the curated palette and the prose hash, so
nothing in the tool is typed by hand.

  python experiments/e-pc/annotations/tool/build_annotator.py

Re-run after any change to the scenario graph, the prose, the vendored ValueNet modules or PALETTE below. The
generated files are committed so annotators can open the page without Python; a test checks they are current.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EPC = HERE.parents[1]
sys.path.insert(0, str(EPC / "scoring"))
import epc  # noqa: E402

PAIRS = [("mf:HarmProcess", "mf:CareDisposition"), ("mf:CheatingProcess", "mf:FairnessDisposition"),
         ("mf:BetrayalProcess", "mf:LoyaltyDisposition"), ("mf:SubversionProcess", "mf:AuthorityDisposition"),
         ("mf:DegradationProcess", "mf:SanctityDisposition"), ("mf:OppressionProcess", "mf:LibertyDisposition")]
TYPE_ORDER = ["Person", "Organization", "Government Organization", "Commercial Organization", "role", "Occupation Role"]

# The curated palette: one class per concept, grouped by theme. Fixed on 2026-09-28, before any annotator started.
# Every id must be a class defined in the vendored modules (the build fails otherwise). The full class list stays
# available in the tool behind "show every class"; the palette shapes the gold, so changing it after annotation has
# begun would be a deviation to record in DEVIATIONS.md.
PALETTE = [
    ("Care and harm", ["mf:CareDisposition"]),
    ("Fairness", ["mf:FairnessDisposition"]),
    ("Loyalty, family and belonging", ["mf:LoyaltyDisposition", "folk:FamilyDisposition", "folk:CommunityDisposition"]),
    ("Authority, rules and duty", ["mf:AuthorityDisposition", "folk:DutyDisposition", "folk:ResponsibilityDisposition", "folk:ProfessionalismRole"]),
    ("Sanctity and dignity", ["mf:SanctityDisposition", "folk:DignityDisposition"]),
    ("Liberty, autonomy and consent", ["mf:LibertyDisposition", "folk:AutonomyDisposition"]),
    ("Honesty, transparency, privacy and trust", ["folk:HonestyDisposition", "folk:TransparencyDisposition", "folk:PrivacyDisposition", "folk:TrustDisposition"]),
    ("Health, safety and wellbeing", ["folk:HealthDisposition", "schwartz:SecurityDisposition"]),
    ("Diligence and stewardship of resources", ["folk:DiligenceDisposition", "folk:ThriftDisposition"]),
]

MODULES = {"mf": "valuenet-moral-foundations", "schwartz": "valuenet-schwartz-values", "folk": "valuenet-folk", "vn-core": "valuenet-core"}
FILES = {"mf": "valuenet-moral-foundations.ttl", "schwartz": "valuenet-schwartz-values.ttl", "folk": "valuenet-folk.ttl", "vn-core": "valuenet-core.ttl"}


def clean_label(raw: str, local: str) -> str:
    """'care Disposition' -> 'Care'; 'Harm Process' -> 'Harm'; roles keep a marker."""
    s = re.sub(r"\s*(Disposition|Process|Role)\s*$", "", raw, flags=re.I).strip() or re.sub(r"(Disposition|Process|Role)$", "", local)
    s = s[:1].upper() + s[1:]
    return s + (" (role)" if local.endswith("Role") else "")


def parse_module(prefix: str) -> dict[str, dict]:
    """Classes defined in the module (subject lines only), with rdfs:label and skos:definition (rdfs:comment as fallback)."""
    ns = MODULES[prefix]
    text = (epc.VALUENET_DIR / FILES[prefix]).read_text(encoding="utf-8")
    out: dict[str, dict] = {}
    pattern = re.compile(rf"^<https://fandaws\.com/ontology/bfo/{re.escape(ns)}#([A-Za-z]+)>", re.M)
    starts = [(m.start(), m.group(1)) for m in pattern.finditer(text)]
    for i, (pos, local) in enumerate(starts):
        block = text[pos:starts[i + 1][0] if i + 1 < len(starts) else len(text)]
        if f"{prefix}:{local}" in out:
            continue
        lab = re.search(r'rdfs:label\s+"([^"]+)"', block)
        defn = re.search(r'skos:definition\s+"([^"]+)"', block) or re.search(r'rdfs:comment\s+"([^"]+)"', block)
        if not lab:
            continue
        out[f"{prefix}:{local}"] = {"label": clean_label(lab.group(1), local), "raw_label": lab.group(1), "definition": (defn.group(1) if defn else "").strip()}
    return out


def main() -> int:
    cfg = epc.load_config()
    name = cfg["scenario"]
    prose_bytes = epc.prose_path(name).read_bytes()
    text = prose_bytes.decode("utf-8")
    sc = epc.load_scenario(name)
    classes: dict[str, dict] = {}
    for prefix in ("mf", "schwartz", "folk", "vn-core"):
        classes.update(parse_module(prefix))
    mf = [k for k in classes if k.startswith("mf:") and k.endswith("Disposition")]
    schwartz = [k for k in classes if k.startswith("schwartz:") and k.endswith("Disposition")]
    folk = [k for k in classes if k.startswith("folk:") and k.endswith(("Disposition", "Role"))]
    for t, d in PAIRS:
        assert d in mf and t in classes, f"{t}/{d} not found in the moral-foundations module"
    for theme, ids in PALETTE:
        for cid in ids:
            assert cid in classes and cid in mf + schwartz + folk, f"palette class {cid} is not a defined disposition or role class"
            assert classes[cid]["definition"], f"palette class {cid} has no definition"
    violations = [{"type": t, "label": classes[t]["label"], "contravenes": d, "definition": classes[t]["definition"]} for t, d in PAIRS]
    violations.append({"type": "vn-core:ValueViolationProcess", "label": "Other violation", "contravenes": None,
                       "definition": classes.get("vn-core:ValueViolationProcess", {}).get("definition", "A process that contravenes a value disposition outside the six moral-foundations pairs.")})
    entities = sorted(sc["entities"], key=lambda e: (TYPE_ORDER.index(e["type"]) if e["type"] in TYPE_ORDER else len(TYPE_ORDER), e["id"]))
    data = {
        "scenario": name, "file": f"scenarios/{name}.txt", "textual_representation_id": f"TR-{name}",
        "expected_sha256": hashlib.sha256(prose_bytes).hexdigest(), "expected_codepoints": len(text),
        "entities": [{"id": e["id"], "label": e["label"], "type": e["type"]} for e in entities],
        "dispositions": {"mf": mf, "schwartz": schwartz, "folk": folk, "all": mf + schwartz + folk},
        "classes": {k: {"label": v["label"], "definition": v["definition"]} for k, v in classes.items() if k in set(mf + schwartz + folk) or k in {t for t, _ in PAIRS} or k == "vn-core:ValueViolationProcess"},
        "palette": [{"theme": theme, "classes": ids} for theme, ids in PALETTE],
        "violations": violations,
        "built_from": {"scenario_sha256": epc.sha256_file(EPC / "scenarios" / f"{name}.json"), "valuenet_sha256sums": epc.sha256_file(epc.VALUENET_DIR / "SHA256SUMS")},
    }
    template = (HERE / "annotator.template.html").read_text(encoding="utf-8")
    assert "__DATA__" in template
    html = template.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    (HERE / "annotator.html").write_text(html, encoding="utf-8", newline="\n")

    # PALETTE.md: the same palette, for the guide and for the record.
    lines = ["# Annotation palette (E-PC gold)", "",
             "The value classes offered first in the annotation tool: one class per concept, grouped by theme, with each",
             "class's own label and definition from the vendored BFO-Aligned ValueNet modules. Fixed on 2026-09-28,",
             "before any annotator started; changing it after annotation begins is a deviation to record in",
             "`DEVIATIONS.md`. Every other class in the modules stays available in the tool behind \"show every class\";",
             "an annotator who needs one says why in the note. Generated by `tool/build_annotator.py`; do not edit by hand.", "",
             "Harms use the six moral-foundations pairs: a harm of a given kind contravenes its paired foundation, and the",
             "tool fixes that pairing. An \"other violation\" contravenes any class below.", "",
             "| Theme | Class | Label | Definition |", "| --- | --- | --- | --- |"]
    for theme, ids in PALETTE:
        for cid in ids:
            lines.append(f"| {theme} | `{cid}` | {classes[cid]['label']} | {classes[cid]['definition']} |")
    lines += ["", "## The six harms", "", "| Harm | Contravenes | Definition |", "| --- | --- | --- |"]
    for v in violations[:-1]:
        lines.append(f"| {v['label']} (`{v['type']}`) | {classes[v['contravenes']]['label']} (`{v['contravenes']}`) | {v['definition']} |")
    lines.append("")
    (HERE.parent / "PALETTE.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"annotator.html: {len(entities)} entities, {len(mf)} mf + {len(schwartz)} schwartz + {len(folk)} folk classes, "
          f"{sum(len(i) for _, i in PALETTE)} palette classes in {len(PALETTE)} themes, prose {data['expected_codepoints']} code points; PALETTE.md written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
