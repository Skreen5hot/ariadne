"""E-PC's own scoring functions (stdlib only; jsonschema used when installed).

These are not the E2 mechanism. What is reused from E1/E2 is convention: the scenario shape, the
five relational domains and the MRC rule, the observed-plus-null permutation p-value, and the
blind-packet practice. See PREREG.md §11.

Subcommands:
  validate                      graph integrity (ids, edge endpoints, predicates)
  mrc                           multi-relational completeness profile and gate
  parity                        token counts of the full B and C prompts
  prompt <A|B|C>                print the full prompt for an arm
  offsets [--text FILE] "span"  code-point offsets of every occurrence of span in the prose (or FILE)
  validate-annotations FILE     check an annotation file against the prose, the graph and ValueNet
  agreement A.json B.json       inter-annotator agreement
  fabrication OUTPUT.json       fabrication check of one structured output
  coverage GOLD RATING          coverage of one rated output
  build-value-layer             value layer file from the adjudicated gold
  blind-pack RUN_ID             label-stripped packets for the rater, plus the key
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import statistics
import sys
from pathlib import Path

EPC = Path(__file__).resolve().parents[1]
REPO = EPC.parents[1]
VALUENET_DIR = REPO / "docs" / "02-evidence" / "valuenet"

KINDS = {"fact", "question", "conjecture", "evaluation"}
DOMAINS = ["physical_causal", "agentic", "informational", "evaluative_experiential", "legal_institutional"]


# ----------------------------------------------------------------------------- loading

def load_config() -> dict:
    return json.loads((EPC / "config.json").read_text(encoding="utf-8"))


def scenario_name(cfg: dict | None = None) -> str:
    return (cfg or load_config())["scenario"]


def load_scenario(name: str | None = None) -> dict:
    name = name or scenario_name()
    return json.loads((EPC / "scenarios" / f"{name}.json").read_text(encoding="utf-8"))


def load_predicates() -> dict:
    return json.loads((EPC / "scenarios" / "predicates.json").read_text(encoding="utf-8"))


def prose_path(name: str | None = None) -> Path:
    return EPC / "scenarios" / f"{name or scenario_name()}.txt"


def load_text_exact(path: Path) -> str:
    """The textual representation, byte-exact. Refuses CR so that offsets are checkout-independent."""
    raw = path.read_bytes()
    if b"\r" in raw:
        raise SystemExit(f"{path}: contains CR; the textual representation must be LF-only (see .gitattributes)")
    return raw.decode("utf-8")


def load_prose(name: str | None = None) -> str:
    return load_text_exact(prose_path(name))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    return sha256_bytes(p.read_bytes())


def sha256_text(s: str) -> str:
    return sha256_bytes(s.encode("utf-8"))


def sha256_file_lf(p: Path) -> str:
    """Hash of a text file with CRLF normalised to LF, so the pre-registration hash is the same on every checkout."""
    return sha256_bytes(p.read_bytes().replace(b"
", b"
"))


# ----------------------------------------------------------------------------- prompts and parity

TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def tokenize(text: str) -> list[str]:
    """Deterministic regex tokenizer: words and punctuation. The frozen parity measure."""
    return TOKEN_RE.findall(text)


def build_prompt(arm: str, cfg: dict | None = None, case_text: str | None = None) -> str:
    cfg = cfg or load_config()
    arm_text = (EPC / cfg["arm_files"][arm]).read_text(encoding="utf-8")
    contract = (EPC / cfg["output_contract"]).read_text(encoding="utf-8")
    case = case_text if case_text is not None else load_prose(cfg["scenario"])
    return arm_text.rstrip("\n") + "\n\n" + case.rstrip("\n") + "\n\n" + contract.rstrip("\n") + "\n"


def parity(cfg: dict | None = None) -> dict:
    cfg = cfg or load_config()
    counts = {arm: len(tokenize(build_prompt(arm, cfg))) for arm in cfg["arms"]}
    b, c = counts["B"], counts["C"]
    rel = abs(b - c) / max(b, c)
    return {"tokens": counts, "B_vs_C_relative_difference": round(rel, 4),
            "tolerance": cfg["length_parity_tolerance"], "passed": rel <= cfg["length_parity_tolerance"]}


# ----------------------------------------------------------------------------- graph checks

def validate_scenario(sc: dict | None = None) -> list[str]:
    sc = sc or load_scenario()
    preds = {p["id"] for p in load_predicates()["predicates"]}
    errors: list[str] = []
    ids: set[str] = set()
    for e in sc["entities"]:
        for k in ("id", "type", "type_iri", "label"):
            if not e.get(k):
                errors.append(f"entity missing {k}: {e}")
        if e["id"] in ids:
            errors.append(f"duplicate entity id {e['id']}")
        ids.add(e["id"])
        if not (e["type_iri"].startswith("https://www.commoncoreontologies.org/") or e["type_iri"].startswith("http://purl.obolibrary.org/obo/BFO_")):
            errors.append(f"{e['id']}: type_iri outside CCO/BFO: {e['type_iri']}")
    eids: set[str] = set()
    for ed in sc["edges"]:
        if ed["edge_id"] in eids:
            errors.append(f"duplicate edge id {ed['edge_id']}")
        eids.add(ed["edge_id"])
        for end in ("source", "target"):
            if ed[end] not in ids:
                errors.append(f"{ed['edge_id']}: {end} {ed[end]} is not an entity")
        if ed["predicate"] not in preds:
            errors.append(f"{ed['edge_id']}: predicate {ed['predicate']} not in registry")
    for u in sc.get("unknowns", []):
        for b in u.get("bears_on", []):
            if b not in ids:
                errors.append(f"{u['id']}: bears_on {b} is not an entity")
    return errors


def mrc_profile(sc: dict | None = None, imbalance_ratio: float | None = None) -> dict:
    """Multi-relational completeness: every relational domain populated, no gross imbalance (E1/E2 rule)."""
    sc = sc or load_scenario()
    ratio = imbalance_ratio if imbalance_ratio is not None else load_config()["mrc_imbalance_ratio"]
    pred_domain = {p["id"]: p["relational_domain"] for p in load_predicates()["predicates"]}
    counts = {d: 0 for d in DOMAINS}
    preds_by_domain: dict[str, set[str]] = {d: set() for d in DOMAINS}
    for e in sc["edges"]:
        d = pred_domain[e["predicate"]]
        counts[d] += 1
        preds_by_domain[d].add(e["predicate"])
    nonzero = [v for v in counts.values() if v > 0]
    empty = [d for d, v in counts.items() if v == 0]
    mx, mn = max(counts.values()), (min(nonzero) if nonzero else 0)
    flags = []
    if empty:
        flags.append(f"domains with zero edges: {empty}")
    if mn and mx / mn > ratio:
        flags.append(f"gross imbalance: max/min edge ratio {mx / mn:.2f} > {ratio}")
    return {"rows": [{"domain": d, "edge_count": counts[d], "predicates": sorted(preds_by_domain[d])} for d in DOMAINS],
            "total_edges": len(sc["edges"]), "max_min_ratio": round(mx / mn, 2) if mn else None,
            "imbalance_ratio_limit": ratio, "all_domains_nonzero": not empty, "flags": flags, "passed": not flags}


# ----------------------------------------------------------------------------- fabrication

def normalize_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("“", '"').replace("”", '"')).strip().lower()


def entity_index(sc: dict) -> dict[str, str]:
    """lowercase label/alias -> entity id"""
    idx: dict[str, str] = {}
    for e in sc["entities"]:
        idx[normalize_ws(e["label"])] = e["id"]
        for a in e.get("aliases", []):
            idx[normalize_ws(a)] = e["id"]
    return idx


def resolve_entity(name: str, idx: dict[str, str]) -> str | None:
    n = normalize_ws(name)
    if not n:
        return None
    if n in idx:
        return idx[n]
    # tolerant matching: the mention contains a known name, or a known name contains the mention
    best = None
    for key, eid in idx.items():
        if len(key) >= 4 and (key in n or (len(n) >= 4 and n in key)):
            if best is None or len(key) > len(best[0]):
                best = (key, eid)
    return best[1] if best else None


def iter_statements(output: dict):
    for sec in output.get("sections", []):
        for i, st in enumerate(sec.get("statements", [])):
            yield sec.get("name", "?"), i, st
    for i, st in enumerate(output.get("synthesis", []) or []):
        yield "synthesis", i, st


def fabrication_check(output: dict, sc: dict, prose: str) -> dict:
    """A statement is fabricated when kind == fact and (trace absent from the prose or an entity is unknown),
    or when kind == evaluation and an entity is unknown. Questions and conjectures are exempt (they may
    introduce people or things), but they count in the denominator."""
    idx = entity_index(sc)
    nprose = normalize_ws(prose)
    details = []
    total = fabricated = 0
    for section, i, st in iter_statements(output):
        total += 1
        kind = st.get("kind")
        reasons = []
        if kind not in KINDS:
            reasons.append(f"unknown kind {kind!r}")
        trace = str(st.get("trace") or "").strip()
        unknown = [e for e in (st.get("entities") or []) if resolve_entity(str(e), idx) is None]
        if kind == "fact":
            if not trace or trace.lower() == "none":
                reasons.append("fact without trace")
            elif normalize_ws(trace) not in nprose:
                reasons.append("trace not in prose")
            if unknown:
                reasons.append(f"unknown entities {unknown}")
        elif kind == "evaluation":
            if unknown:
                reasons.append(f"unknown entities {unknown}")
        if reasons:
            fabricated += 1
            details.append({"section": section, "index": i, "kind": kind, "text": st.get("text"), "reasons": reasons})
    return {"statements": total, "fabricated": fabricated, "rate": (fabricated / total) if total else 0.0, "details": details}


# ----------------------------------------------------------------------------- annotations

def codepoint_offsets(span: str, text: str) -> list[tuple[int, int]]:
    out = []
    start = 0
    while True:
        i = text.find(span, start)
        if i < 0:
            break
        out.append((i, i + len(span)))
        start = i + 1
    return out


def valuenet_local_names() -> dict[str, set[str]]:
    names: dict[str, set[str]] = {"vn-core": set(), "folk": set(), "schwartz": set(), "mf": set()}
    files = {"vn-core": "valuenet-core.ttl", "folk": "valuenet-folk.ttl", "schwartz": "valuenet-schwartz-values.ttl", "mf": "valuenet-moral-foundations.ttl"}
    for prefix, fn in files.items():
        p = VALUENET_DIR / fn
        if p.exists():
            for m in re.finditer(r"valuenet-(?:core|folk|schwartz-values|moral-foundations)#([A-Za-z]+)>", p.read_text(encoding="utf-8")):
                names[prefix].add(m.group(1))
    return names


def validate_annotations(path: Path, text_source: Path | None = None) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    try:
        import jsonschema  # type: ignore
        schema = json.loads((EPC / "annotations" / "gold.schema.json").read_text(encoding="utf-8"))
        for err in jsonschema.Draft202012Validator(schema).iter_errors(data):
            errors.append(f"schema: {'/'.join(str(x) for x in err.path)}: {err.message}")
    except ImportError:
        errors.append("jsonschema not installed; structural validation skipped")
    tr = data["textual_representation"]
    src = text_source or (EPC / tr["file"])
    text = load_text_exact(src)
    if sha256_text(text) != tr["sha256"]:
        errors.append(f"textual_representation sha256 mismatch for {src.name}")
    if len(text) != tr["codepoint_length"]:
        errors.append(f"codepoint_length {tr['codepoint_length']} != {len(text)}")
    sc = load_scenario()
    ids = {e["id"] for e in sc["entities"]}
    vn = valuenet_local_names()
    seen_ids: set[str] = set()
    for a in data["annotations"]:
        aid = a.get("id", "?")
        if aid in seen_ids:
            errors.append(f"{aid}: duplicate annotation id")
        seen_ids.add(aid)
        span = a["hasEvidenceSource"]["hasTextualSequenceValue"]
        sel = a["hasSelector"]
        s, e = sel["hasStartOffset"], sel["hasEndOffset"]
        if e <= s:
            errors.append(f"{aid}: end offset not greater than start")
        elif text[s:e] != span:
            errors.append(f"{aid}: offsets {s}:{e} do not delimit the recorded span")
        if a["hasEvidenceSource"]["isTextSpanOf"] != tr["id"] or sel["hasSourceRepresentation"] != tr["id"]:
            errors.append(f"{aid}: span/selector do not name the textual representation {tr['id']}")
        if sel["selectsTextSpan"] != a["hasEvidenceSource"]["id"]:
            errors.append(f"{aid}: selector does not select this span")
        proc = a["isEvidenceFor"]
        if proc["bearer"] not in ids:
            errors.append(f"{aid}: bearer {proc['bearer']} is not a graph entity")
        for pid in proc.get("participants", []):
            if pid not in ids:
                errors.append(f"{aid}: participant {pid} is not a graph entity")
        for field in ("type", "disposition_type"):
            prefix, _, local = proc[field].partition(":")
            if prefix not in vn:
                errors.append(f"{aid}: {field} prefix {prefix!r} unknown")
            elif vn[prefix] and local not in vn[prefix]:
                errors.append(f"{aid}: {field} {proc[field]} not found in the ValueNet modules")
        if proc["kind"] == "violation" and not proc["type"].endswith("ViolationProcess") and not proc["type"].startswith("mf:"):
            errors.append(f"{aid}: violation must be an mf:*Process or vn-core:ValueViolationProcess")
        if proc["kind"] == "realization" and proc["type"] != "vn-core:ValueRealizationProcess":
            errors.append(f"{aid}: realization must be vn-core:ValueRealizationProcess")
        pairs = {"HarmProcess": "CareDisposition", "CheatingProcess": "FairnessDisposition", "BetrayalProcess": "LoyaltyDisposition",
                 "SubversionProcess": "AuthorityDisposition", "DegradationProcess": "SanctityDisposition", "OppressionProcess": "LibertyDisposition"}
        if proc["type"].startswith("mf:"):
            expected = "mf:" + pairs[proc["type"].split(":")[1]]
            if proc["disposition_type"] != expected:
                errors.append(f"{aid}: {proc['type']} contravenes {expected}, not {proc['disposition_type']}")
    return errors


def process_key(a: dict) -> tuple[str, str]:
    p = a["isEvidenceFor"]
    return (p["disposition_type"], p["bearer"])


def _overlap_frac(a: tuple[int, int], b: tuple[int, int]) -> float:
    inter = max(0, min(a[1], b[1]) - max(a[0], b[0]))
    shorter = min(a[1] - a[0], b[1] - b[0])
    return inter / shorter if shorter else 0.0


def agreement(a: dict, b: dict) -> dict:
    """Span-level: fraction of each set's annotations overlapping one of the other's by >= 50% of the shorter.
    Process-level: Cohen's kappa over the union of (disposition_type, bearer) keys."""
    def spans(d):
        return [(x["hasSelector"]["hasStartOffset"], x["hasSelector"]["hasEndOffset"]) for x in d["annotations"]]
    sa, sb = spans(a), spans(b)
    a_in_b = sum(1 for s in sa if any(_overlap_frac(s, t) >= 0.5 for t in sb))
    b_in_a = sum(1 for t in sb if any(_overlap_frac(t, s) >= 0.5 for s in sa))
    ka = {process_key(x) for x in a["annotations"]}
    kb = {process_key(x) for x in b["annotations"]}
    universe = sorted(ka | kb)
    n = len(universe)
    both = len(ka & kb)
    only_a = len(ka - kb)
    only_b = len(kb - ka)
    neither = 0  # by construction the universe is the union; kappa over presence in the union
    po = (both + neither) / n if n else 0.0
    pa = (both + only_a) / n if n else 0.0
    pb = (both + only_b) / n if n else 0.0
    pe = pa * pb + (1 - pa) * (1 - pb)
    kappa = (po - pe) / (1 - pe) if (1 - pe) > 1e-12 else (1.0 if po == 1.0 else 0.0)
    return {"n_a": len(sa), "n_b": len(sb),
            "span_agreement_a_in_b": round(a_in_b / len(sa), 3) if sa else None,
            "span_agreement_b_in_a": round(b_in_a / len(sb), 3) if sb else None,
            "process_keys_union": n, "process_keys_both": both, "process_kappa": round(kappa, 3),
            "note": "kappa computed over presence/absence of (disposition_type, bearer) keys in the union; a conservative floor since absent-absent cells are undefined"}


def coverage(gold: dict, rating: dict) -> dict:
    gold_keys = {a["id"]: process_key(a) for a in gold["annotations"]}
    matched: dict[str, str] = {}
    invalid = []
    for r in rating["annotations"]:
        gid = r["isEvidenceFor"].get("gold_id")
        if gid not in gold_keys:
            invalid.append(f"{r['id']}: gold_id {gid!r} not in gold")
            continue
        if process_key(r) != gold_keys[gid]:
            invalid.append(f"{r['id']}: value fields differ from gold {gid}")
            continue
        matched.setdefault(gid, r["isEvidenceFor"].get("section", "?"))
    n = len(gold_keys)
    return {"gold_items": n, "covered": len(matched), "coverage": (len(matched) / n) if n else 0.0,
            "matched_by_section": matched, "invalid": invalid}


# ----------------------------------------------------------------------------- statistics

def permutation_test(x: list[float], y: list[float], n_perm: int, seed: int) -> dict:
    """One-sided: is mean(x) - mean(y) larger than chance? Observed-plus-null convention (E2 §5.1):
    p = (1 + #{perm >= observed}) / (n_perm + 1). The observed labelling is not in the null sample."""
    obs = statistics.fmean(x) - statistics.fmean(y)
    pooled = list(x) + list(y)
    nx = len(x)
    rng = random.Random(seed)
    ge = 0
    for _ in range(n_perm):
        rng.shuffle(pooled)
        d = statistics.fmean(pooled[:nx]) - statistics.fmean(pooled[nx:])
        if d >= obs - 1e-12:
            ge += 1
    p = (1 + ge) / (n_perm + 1)
    sx = statistics.pstdev(x) if len(x) > 1 else 0.0
    sy = statistics.pstdev(y) if len(y) > 1 else 0.0
    pooled_sd = math.sqrt(((len(x) - 1) * statistics.variance(x) + (len(y) - 1) * statistics.variance(y)) / (len(x) + len(y) - 2)) if len(x) > 1 and len(y) > 1 else 0.0
    d = obs / pooled_sd if pooled_sd > 0 else None
    more = sum(1 for a in x for b in y if a > b)
    less = sum(1 for a in x for b in y if a < b)
    cliff = (more - less) / (len(x) * len(y)) if x and y else None
    return {"observed_difference": round(obs, 4), "p_value": round(p, 5), "n_permutations": n_perm, "seed": seed,
            "n_x": len(x), "n_y": len(y), "sd_x": round(sx, 4), "sd_y": round(sy, 4),
            "cohens_d": round(d, 3) if d is not None else None, "cliffs_delta": round(cliff, 3) if cliff is not None else None,
            "n_null_at_or_above_observed": ge}


# ----------------------------------------------------------------------------- value layer and packets

def build_value_layer(gold_path: Path | None = None) -> Path:
    """Instantiate the adjudicated gold as ValueNet individuals attached to the graph: borne dispositions and
    the processes that realize or contravene them. Written to a separate file so the situation layer's hash
    is untouched. Harms are value violation processes contravening a borne disposition."""
    name = scenario_name()
    gold_path = gold_path or (EPC / "annotations" / f"{name}.gold.json")
    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    if gold.get("annotator") != "adjudicated":
        raise SystemExit("value layer is built only from the adjudicated gold (annotator: adjudicated)")
    dispositions: dict[tuple[str, str], str] = {}
    entities, edges = [], []
    n = 0
    for a in gold["annotations"]:
        p = a["isEvidenceFor"]
        key = (p["disposition_type"], p["bearer"])
        if key not in dispositions:
            did = f"VD-{len(dispositions) + 1:02d}"
            dispositions[key] = did
            entities.append({"id": did, "type": p["disposition_type"], "layer": "value", "label": f"{p['disposition_type']} borne by {p['bearer']}"})
            edges.append({"edge_id": f"VE{n:03d}", "source": p["bearer"], "predicate": "bearer_of", "target": did}); n += 1
        pid = p["id"]
        entities.append({"id": pid, "type": p["type"], "layer": "value", "label": p["label"], "kind": p["kind"], "evidence_annotation": a["id"]})
        rel = "contravenes" if p["kind"] == "violation" else "realizes"
        edges.append({"edge_id": f"VE{n:03d}", "source": pid, "predicate": rel, "target": dispositions[key]}); n += 1
        for part in p.get("participants", []):
            edges.append({"edge_id": f"VE{n:03d}", "source": pid, "predicate": "has_participant", "target": part}); n += 1
    out = {"schema": "e-pc/value-layer/v1", "scenario": name, "gold_sha256": sha256_file(gold_path),
           "predicate_note": "contravenes = vn-core:contravenes (https://fandaws.com/ontology/bfo/valuenet-core#contravenes); realizes = BFO_0000055; bearer_of = BFO_0000196; has_participant = BFO_0000057",
           "entities": entities, "edges": edges}
    dst = EPC / "scenarios" / f"{name}.value-layer.json"
    dst.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return dst


def blind_pack(run_id: str, seed: int | None = None) -> dict:
    run = EPC / "results" / run_id
    outs = sorted((run / "outputs").glob("*.json"))
    if not outs:
        raise SystemExit("no outputs to pack")
    seed = seed if seed is not None else load_config()["seed"]
    rng = random.Random(seed)
    order = list(outs)
    rng.shuffle(order)
    blind = run / "blind"
    blind.mkdir(exist_ok=True)
    key = {}
    for p in order:
        pkt = "PKT-" + sha256_file(p)[:12]
        data = json.loads(p.read_text(encoding="utf-8"))
        (blind / f"{pkt}.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        txt = p.with_suffix(".txt")
        if txt.exists():
            (blind / f"{pkt}.txt").write_bytes(txt.read_bytes())
        key[pkt] = p.name
    (blind / "key.json").write_text(json.dumps({"seed": seed, "packets": key}, indent=1) + "\n", encoding="utf-8", newline="\n")
    return key


# ----------------------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    sub.add_parser("mrc")
    sub.add_parser("parity")
    s = sub.add_parser("prompt"); s.add_argument("arm")
    s = sub.add_parser("offsets"); s.add_argument("span"); s.add_argument("--text", default=None)
    s = sub.add_parser("validate-annotations"); s.add_argument("file"); s.add_argument("--text", default=None)
    s = sub.add_parser("agreement"); s.add_argument("a"); s.add_argument("b")
    s = sub.add_parser("fabrication"); s.add_argument("output")
    s = sub.add_parser("coverage"); s.add_argument("gold"); s.add_argument("rating")
    sub.add_parser("build-value-layer")
    s = sub.add_parser("blind-pack"); s.add_argument("run_id")
    args = ap.parse_args(argv)

    if args.cmd == "validate":
        errs = validate_scenario()
        print("\n".join(errs) if errs else "scenario graph valid")
        return 1 if errs else 0
    if args.cmd == "mrc":
        print(json.dumps(mrc_profile(), indent=1)); return 0
    if args.cmd == "parity":
        r = parity(); print(json.dumps(r, indent=1)); return 0 if r["passed"] else 1
    if args.cmd == "prompt":
        sys.stdout.write(build_prompt(args.arm)); return 0
    if args.cmd == "offsets":
        text = load_text_exact(Path(args.text)) if args.text else load_prose()
        hits = codepoint_offsets(args.span, text)
        print(json.dumps(hits) if hits else "no match"); return 0 if hits else 1
    if args.cmd == "validate-annotations":
        errs = validate_annotations(Path(args.file), Path(args.text) if args.text else None)
        print("\n".join(errs) if errs else "annotation file valid"); return 1 if errs else 0
    if args.cmd == "agreement":
        a = json.loads(Path(args.a).read_text(encoding="utf-8")); b = json.loads(Path(args.b).read_text(encoding="utf-8"))
        print(json.dumps(agreement(a, b), indent=1)); return 0
    if args.cmd == "fabrication":
        out = json.loads(Path(args.output).read_text(encoding="utf-8"))
        print(json.dumps(fabrication_check(out, load_scenario(), load_prose()), indent=1)); return 0
    if args.cmd == "coverage":
        g = json.loads(Path(args.gold).read_text(encoding="utf-8")); r = json.loads(Path(args.rating).read_text(encoding="utf-8"))
        print(json.dumps(coverage(g, r), indent=1)); return 0
    if args.cmd == "build-value-layer":
        print(build_value_layer()); return 0
    if args.cmd == "blind-pack":
        print(json.dumps(blind_pack(args.run_id), indent=1)); return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
