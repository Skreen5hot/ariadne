"""Build annotator.html, DEMO_annotator.html and PALETTE.md from annotator.template.html and the repository files.

  python experiments/e-pc/annotations/tool/build_annotator.py

annotator.html is the study tool: the exact entity ids of the scenario graph, the ValueNet classes with their own labels
and definitions, the curated palette, and the hash of the frozen prose, which the annotator loads from the repository.

DEMO_annotator.html is for presentations and practice. It embeds the made-up bakery text and its three-person cast, keeps
its saved work in a store of its own (so it can never read, overwrite or clear real annotation work in the same
browser), offers no export, and contains nothing from the study case.

Re-run after any change to the scenario graph, the prose, the vendored ValueNet modules, the bakery fixture or PALETTE
below. The generated files are committed so people can open them without Python; a test checks they are current.
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

# The greyed hint inside the empty label box. The study page keeps the wording its annotators have seen since 2026-09-28;
# the demo page must carry nothing from the study case, so it has its own.
STUDY_LABEL_HINT = "e.g. discharge without cognitive screen risks harm to Margaret"
DEMO_LABEL_HINT = "a short phrase in your own words"

# The demo: the neutral bakery text (the runner's smoke fixture; also the guide's worked example) and its cast.
DEMO_FIXTURE = epc.REPO / "tests" / "e-pc" / "fixtures" / "smoke-case.txt"
DEMO_ENTITIES = [{"id": "P-OWNER", "label": "Ada Lin", "type": "Person"},
                 {"id": "P-EMP", "label": "Ben Cole", "type": "Person"},
                 {"id": "ORG-BAKERY", "label": "the bakery", "type": "Organization"}]
DEMO_EXAMPLES = [  # the same three rows as the worked example in ANNOTATION_GUIDE.md
    {"span": "asked the newer employee, Ben Cole, to close the shop alone for the first time", "kind": "realization",
     "type": "vn-core:ValueRealizationProcess", "disposition": "folk:TrustDisposition", "bearer": "P-OWNER", "participants": ["P-EMP"],
     "label": "Ada extends trust to a new employee", "fit": "exact", "note": ""},
    {"span": "The till was short by twelve pounds", "kind": "violation",
     "type": "mf:CheatingProcess", "disposition": "mf:FairnessDisposition", "bearer": "P-OWNER", "participants": [],
     "label": "money may have been taken from the owner", "fit": "closest", "note": "only if the shortfall was taken; the cause is not known"},
    {"span": "Nobody has asked Ben what happened.", "kind": "realization",
     "type": "vn-core:ValueRealizationProcess", "disposition": "mf:FairnessDisposition", "bearer": "P-OWNER", "participants": ["P-EMP"],
     "label": "Ben should be heard before anyone concludes what happened", "fit": "exact", "note": "the unknown (error or something else) bears on this"},
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


def render(template: str, data: dict, title: str, label_hint: str) -> str:
    assert template.count("__DATA__") == 1 and template.count("__TITLE__") == 2 and template.count("__LABEL_HINT__") == 1
    assert not set(label_hint) & set('"<>&'), "the label hint goes into an HTML attribute"
    return (template.replace("__TITLE__", title).replace("__LABEL_HINT__", label_hint)
            .replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))


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
    shown = set(mf + schwartz + folk) | {t for t, _ in PAIRS} | {"vn-core:ValueViolationProcess"}
    vocabulary = {
        "dispositions": {"mf": mf, "schwartz": schwartz, "folk": folk, "all": mf + schwartz + folk},
        "classes": {k: {"label": v["label"], "definition": v["definition"]} for k, v in classes.items() if k in shown},
        "palette": [{"theme": theme, "classes": ids} for theme, ids in PALETTE],
        "violations": violations,
    }
    template = (HERE / "annotator.template.html").read_text(encoding="utf-8")

    # ---- the study tool
    entities = sorted(sc["entities"], key=lambda e: (TYPE_ORDER.index(e["type"]) if e["type"] in TYPE_ORDER else len(TYPE_ORDER), e["id"]))
    study = {
        "scenario": name, "file": f"scenarios/{name}.txt", "textual_representation_id": f"TR-{name}",
        "expected_sha256": hashlib.sha256(prose_bytes).hexdigest(), "expected_codepoints": len(text),
        "entities": [{"id": e["id"], "label": e["label"], "type": e["type"]} for e in entities],
        **vocabulary,
        "demo": False, "storage": {"db": "epc-annotator", "key": "epc-annotator/current"},
        "built_from": {"scenario_sha256": epc.sha256_file(EPC / "scenarios" / f"{name}.json"), "valuenet_sha256sums": epc.sha256_file(epc.VALUENET_DIR / "SHA256SUMS")},
    }
    (HERE / "annotator.html").write_text(render(template, study, "Gold Annotator", STUDY_LABEL_HINT), encoding="utf-8", newline="\n")

    # ---- the demo: bakery text embedded, its own cast, its own store, no export, nothing from the study case
    # The fixture sits outside experiments/e-pc, so a Windows checkout may give it CRLF: normalise, so the page is the same everywhere.
    demo_text = DEMO_FIXTURE.read_bytes().decode("utf-8").replace("\r\n", "\n").strip()
    demo_bytes = demo_text.encode("utf-8")
    demo_ids = {e["id"] for e in DEMO_ENTITIES}
    examples = []
    for ex in DEMO_EXAMPLES:
        start = demo_text.find(ex["span"])
        assert start >= 0 and demo_text.count(ex["span"]) == 1, f"demo example span not found exactly once: {ex['span']!r}"
        assert ex["bearer"] in demo_ids and all(p in demo_ids for p in ex["participants"]) and ex["disposition"] in shown and ex["type"] in shown | {"vn-core:ValueRealizationProcess"}
        examples.append({**ex, "start": start, "end": start + len(ex["span"])})   # the fixture is ASCII, so code points equal string indices
    assert demo_text.isascii(), "demo offsets assume an ASCII fixture"
    demo = {
        "scenario": "bakery-demo", "file": "practice text (embedded)", "textual_representation_id": "TR-bakery-demo",
        "expected_sha256": hashlib.sha256(demo_bytes).hexdigest(), "expected_codepoints": len(demo_text),
        "entities": DEMO_ENTITIES,
        **vocabulary,
        "demo": True, "storage": {"db": "epc-annotator-demo", "key": "epc-annotator-demo/current"},
        "embedded_text": demo_text, "examples": examples,
        "built_from": {"fixture_sha256": hashlib.sha256(demo_bytes).hexdigest(), "valuenet_sha256sums": epc.sha256_file(epc.VALUENET_DIR / "SHA256SUMS")},
    }
    (HERE / "DEMO_annotator.html").write_text(render(template, demo, "Gold Annotator: demo", DEMO_LABEL_HINT), encoding="utf-8", newline="\n")

    # ---- PALETTE.md: the same palette, for the guide and for the record
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
          f"{sum(len(i) for _, i in PALETTE)} palette classes in {len(PALETTE)} themes, prose {study['expected_codepoints']} code points")
    print(f"DEMO_annotator.html: {len(DEMO_ENTITIES)} entities, practice text {demo['expected_codepoints']} code points, {len(examples)} example annotations; PALETTE.md written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
