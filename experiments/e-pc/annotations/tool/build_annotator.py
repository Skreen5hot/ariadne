"""Build annotator.html from annotator.template.html, embedding the exact entity ids, ValueNet classes and prose
hash from the repository files, so nothing in the tool is typed by hand.

  python experiments/e-pc/annotations/tool/build_annotator.py

Re-run after any change to the scenario graph, the prose or the vendored ValueNet modules. The generated file is
committed so annotators can open it without Python.
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


def defined_classes(ttl: Path, ns: str) -> list[str]:
    """Local names of subjects defined in the module (subject lines only, not references)."""
    names = []
    for line in ttl.read_text(encoding="utf-8").splitlines():
        m = re.match(rf"^<https://fandaws\.com/ontology/bfo/{re.escape(ns)}#([A-Za-z]+)>", line)
        if m and m.group(1) not in names:
            names.append(m.group(1))
    return names


def main() -> int:
    cfg = epc.load_config()
    name = cfg["scenario"]
    prose_bytes = epc.prose_path(name).read_bytes()
    text = prose_bytes.decode("utf-8")
    sc = epc.load_scenario(name)
    vn = epc.VALUENET_DIR
    mf = [f"mf:{n}" for n in defined_classes(vn / "valuenet-moral-foundations.ttl", "valuenet-moral-foundations") if n.endswith("Disposition")]
    schwartz = [f"schwartz:{n}" for n in defined_classes(vn / "valuenet-schwartz-values.ttl", "valuenet-schwartz-values") if n.endswith("Disposition")]
    folk = [f"folk:{n}" for n in defined_classes(vn / "valuenet-folk.ttl", "valuenet-folk") if n.endswith(("Disposition", "Role"))]
    for t, d in PAIRS:
        assert d in mf, f"{d} not found in the moral-foundations module"
    entities = sorted(sc["entities"], key=lambda e: (TYPE_ORDER.index(e["type"]) if e["type"] in TYPE_ORDER else len(TYPE_ORDER), e["id"]))
    data = {
        "scenario": name, "file": f"scenarios/{name}.txt", "textual_representation_id": f"TR-{name}",
        "expected_sha256": hashlib.sha256(prose_bytes).hexdigest(), "expected_codepoints": len(text),
        "entities": [{"id": e["id"], "label": e["label"], "type": e["type"]} for e in entities],
        "dispositions": {"mf": mf, "schwartz": schwartz, "folk": folk, "all": mf + schwartz + folk},
        "violations": [{"type": t, "contravenes": d} for t, d in PAIRS] + [{"type": "vn-core:ValueViolationProcess", "contravenes": None}],
        "built_from": {"scenario_sha256": epc.sha256_file(EPC / "scenarios" / f"{name}.json"), "valuenet_sha256sums": epc.sha256_file(vn / "SHA256SUMS")},
    }
    template = (HERE / "annotator.template.html").read_text(encoding="utf-8")
    assert "__DATA__" in template
    html = template.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    (HERE / "annotator.html").write_text(html, encoding="utf-8", newline="\n")
    print(f"annotator.html: {len(entities)} entities, {len(mf)} mf + {len(schwartz)} schwartz + {len(folk)} folk classes, prose {data['expected_codepoints']} code points")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
