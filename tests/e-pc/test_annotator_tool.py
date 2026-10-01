"""The annotation tool's exporter must produce a file the real validator accepts, and its embedded data must match
the repository (prose hash, entity ids, ValueNet classes). The exporter's pure functions run under Node.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess

import pytest

from epc_helpers import EPC_DIR, epc

TOOL = EPC_DIR / "annotations" / "tool"


def _data() -> dict:
    html = (TOOL / "annotator.html").read_text(encoding="utf-8")
    m = re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S)
    assert m, "annotator.html has no embedded data block"
    return json.loads(m.group(1).replace("<\\/", "</"))


def _core_script() -> str:
    html = (TOOL / "annotator.html").read_text(encoding="utf-8")
    m = re.search(r'<script id="core">(.*?)</script>', html, re.S)
    assert m
    return m.group(1)


def test_generated_tool_is_current(tmp_path):
    """Rebuilding the tool must reproduce the committed page and palette byte for byte."""
    committed = (TOOL / "annotator.html").read_bytes()
    palette = (TOOL.parent / "PALETTE.md").read_bytes()
    r = subprocess.run(["python", str(TOOL / "build_annotator.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert (TOOL / "annotator.html").read_bytes() == committed, "annotator.html is stale: run build_annotator.py and commit"
    assert (TOOL.parent / "PALETTE.md").read_bytes() == palette, "PALETTE.md is stale: run build_annotator.py and commit"


def test_palette_and_labels_come_from_the_modules():
    d = _data()
    names = epc.valuenet_local_names()
    assert d["palette"], "no palette embedded"
    seen = []
    for group in d["palette"]:
        assert group["theme"] and group["classes"]
        for cid in group["classes"]:
            assert cid in d["classes"], cid
            assert d["classes"][cid]["label"] and d["classes"][cid]["definition"], f"{cid} lacks a label or definition"
            prefix, local = cid.split(":")
            assert local in names[prefix], cid
            assert cid not in seen, f"{cid} appears twice in the palette"
            seen.append(cid)
    for v in d["violations"]:
        assert v["label"] and v["definition"]
        if v["type"].startswith("mf:"):
            assert v["contravenes"] in d["classes"]
    # every class offered anywhere in the tool carries a definition
    for cid in d["dispositions"]["all"]:
        assert d["classes"][cid]["definition"], cid


def test_embedded_data_matches_repository(cfg, scenario, prose):
    d = _data()
    assert d["expected_sha256"] == epc.sha256_text(prose)
    assert d["expected_codepoints"] == len(prose)
    assert {e["id"] for e in d["entities"]} == {e["id"] for e in scenario["entities"]}
    names = epc.valuenet_local_names()
    for full in d["dispositions"]["all"]:
        prefix, local = full.split(":")
        assert local in names[prefix], full
    assert all(v["contravenes"] in d["dispositions"]["mf"] for v in d["violations"] if v["type"].startswith("mf:"))


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_export_validates_with_the_real_validator(tmp_path, prose):
    d = _data()
    span1 = "I want my own bed."
    span2 = "No cognitive screen or capacity assessment has been performed."
    (s1, e1), = epc.codepoint_offsets(span1, prose)
    (s2, e2), = epc.codepoint_offsets(span2, prose)
    harness = f"""
const document = {{ getElementById: () => ({{ textContent: {json.dumps(json.dumps(d))} }}) }};
{_core_script()}
const state = {{ annotator: "Test Annotator", date: "2026-09-28", sha256: {json.dumps(d["expected_sha256"])}, codepoints: {d["expected_codepoints"]},
  annotations: [
    {{ span: {json.dumps(span1)}, start: {s1}, end: {e1}, kind: "realization", type: "vn-core:ValueRealizationProcess", disposition: "folk:AutonomyDisposition", bearer: "P-PAT", participants: [], label: "Margaret's wish to go home", fit: "exact", note: "" }},
    {{ span: {json.dumps(span2)}, start: {s2}, end: {e2}, kind: "violation", type: "mf:HarmProcess", disposition: "mf:CareDisposition", bearer: "P-HOSP", participants: ["P-PAT"], label: "discharge without a cognitive screen risks harm", fit: "exact", note: "unknown U01 bears on this" }},
  ] }};
const text = {json.dumps(prose)};
const errs = validateAnnotations(text, state.annotations);
if (errs.length) {{ console.error(errs.join("\\n")); process.exit(2); }}
process.stdout.write(JSON.stringify(buildExport(state)));
"""
    js = tmp_path / "harness.js"
    js.write_text(harness, encoding="utf-8")
    r = subprocess.run(["node", str(js)], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    out = tmp_path / "export.json"
    out.write_text(r.stdout, encoding="utf-8")
    errors = epc.validate_annotations(out, EPC_DIR / "scenarios" / "clinic-discharge.txt")
    assert errors == [], errors


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_selection_snaps_to_whole_words(tmp_path, prose):
    d = _data()
    cases = [("forty-bed hospit", "forty-bed hospital"), ("argaret Okonjo, aged 8", "Margaret Okonjo, aged 81"),
             ("responsible for Margaret's car", "responsible for Margaret's care"), ("I want my own bed.", "I want my own bed.")]
    js_cases = []
    for partial, whole in cases:
        hits = epc.codepoint_offsets(partial, prose)
        assert hits, f"test setup: {partial!r} not found in the prose"
        s, e = hits[0]
        js_cases.append({"s": s, "e": e, "want": whole})
    harness = f"""
const document = {{ getElementById: () => ({{ textContent: {json.dumps(json.dumps(d))} }}) }};
{_core_script()}
const text = {json.dumps(prose)};
const out = {json.dumps(js_cases)}.map(c => {{ const [s, e] = snapToWords(text, c.s, c.e); return {{ got: cpSlice(text, s, e), want: c.want }}; }});
process.stdout.write(JSON.stringify(out));
"""
    js = tmp_path / "snap.js"
    js.write_text(harness, encoding="utf-8")
    r = subprocess.run(["node", str(js)], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    for row in json.loads(r.stdout):
        assert row["got"] == row["want"], row


def test_worked_example_is_the_same_in_guide_and_tool():
    guide = (EPC_DIR / "annotations" / "ANNOTATION_GUIDE.md").read_text(encoding="utf-8")
    html = (TOOL / "annotator.html").read_text(encoding="utf-8")
    spans = ["asked the newer employee, Ben Cole, to close the shop alone for the first time",
             "The till was short by twelve pounds", "Nobody has asked Ben what happened."]
    for s in spans:
        assert s in guide and s in html, s
    for phrase in ["Ada extends trust to a new employee", "money may have been taken from the owner",
                   "Ben should be heard before anyone concludes what happened"]:
        assert phrase in guide and phrase in html, phrase
    assert "not the case" in guide and "not this one" in html


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_tool_rejects_bad_pairing_and_unknown_bearer(tmp_path, prose):
    d = _data()
    span = "I want my own bed."
    (s, e), = epc.codepoint_offsets(span, prose)
    harness = f"""
const document = {{ getElementById: () => ({{ textContent: {json.dumps(json.dumps(d))} }}) }};
{_core_script()}
const text = {json.dumps(prose)};
const bad = [
  {{ span: {json.dumps(span)}, start: {s}, end: {e}, kind: "violation", type: "mf:HarmProcess", disposition: "mf:FairnessDisposition", bearer: "P-NOBODY", participants: [], label: "x", fit: "exact", note: "" }},
  {{ span: {json.dumps(span)}, start: {s}, end: {e + 1}, kind: "realization", type: "vn-core:ValueRealizationProcess", disposition: "folk:AutonomyDisposition", bearer: "P-PAT", participants: [], label: "", fit: "gap", note: "" }},
];
process.stdout.write(JSON.stringify(validateAnnotations(text, bad)));
"""
    js = tmp_path / "harness.js"
    js.write_text(harness, encoding="utf-8")
    r = subprocess.run(["node", str(js)], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    errs = json.loads(r.stdout)
    joined = "\n".join(errs)
    assert "contravenes mf:CareDisposition" in joined
    assert "P-NOBODY" in joined
    assert "do not delimit" in joined
    assert "label is empty" in joined
    assert "needs a note" in joined


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_saved_record_keeps_its_key_across_reloads(tmp_path):
    """Regression: on load the record's key leaked into the state as undefined, so every save after a reload was
    rejected by IndexedDB and work done after coming back to the page was lost."""
    d = _data()
    harness = f"""
const document = {{ getElementById: () => ({{ textContent: {json.dumps(json.dumps(d))} }}) }};
{_core_script()}
const s0 = {{ annotator: "A", date: "2026-10-01", attested: true, text: "abc", sha256: "x", codepoints: 3, fileName: "f", annotations: [{{ span: "a" }}], formDraft: null }};
const r1 = toRecord(s0, 1000);
const s1 = Object.assign({{}}, s0, fromRecord(r1));          // what load() does
const r2 = toRecord(s1, 2000);                              // the first save after a reload
const s2 = Object.assign({{}}, s1, fromRecord(r2));
s2.annotations = s2.annotations.concat([{{ span: "b" }}]); s2.formDraft = {{ label: "half typed" }};
const r3 = toRecord(s2, 3000);
process.stdout.write(JSON.stringify({{ k1: r1.key, k2: r2.key, k3: r3.key, keyInState: Object.prototype.hasOwnProperty.call(s1, "key"),
  n3: r3.annotations.length, draft: fromRecord(r3).formDraft.label, newer: newerRecord(r1, r3).savedAt, newer2: newerRecord(r3, r1).savedAt,
  only: newerRecord(null, r2).savedAt, none: newerRecord(null, null) }}));
"""
    js = tmp_path / "record.js"
    js.write_text(harness, encoding="utf-8")
    r = subprocess.run(["node", str(js)], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["k1"] == out["k2"] == out["k3"] == "current"
    assert out["keyInState"] is False
    assert out["n3"] == 2 and out["draft"] == "half typed"
    assert out["newer"] == 3000 and out["newer2"] == 3000 and out["only"] == 2000 and out["none"] is None


def test_page_saves_visibly_and_offers_a_backup():
    html = (TOOL / "annotator.html").read_text(encoding="utf-8")
    assert 'id="saveStatus"' in html and 'id="backupBtn"' in html
    assert "{ key: undefined }" not in html and '{ key: "current", ...state }' not in html, "the key-leak bug is back"
    for needle in ["pagehide", "visibilitychange", "beforeunload", "localStorage.setItem", "navigator.storage.persist", "captureFormDraft"]:
        assert needle in html, needle
