"""Run the E-PC arms against the model.

  python experiments/e-pc/scoring/run_arms.py --smoke      one request per arm on a neutral fixture text; writes to the
                                                            scratch directory given by --out (default: a temp dir); never the scenario
  python experiments/e-pc/scoring/run_arms.py --dev        the real scenario, results/dev_<ts>/ (git-ignored); refused until the
                                                            gold is committed, because no arm output may exist before the gold
  python experiments/e-pc/scoring/run_arms.py --credited   the credited run; refused unless PREREG.ratified matches PREREG.md,
                                                            the gold is committed and clean, and config.json is committed and clean

The runner sends temperature 0 and thinking disabled exactly as config.json says. If the API rejects a parameter for the
chosen model it stops with the error; it never silently drops a parameter (PREREG.md §12 O-1).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import epc  # noqa: E402

EPC = epc.EPC
REPO = epc.REPO


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO), *args], text=True, stderr=subprocess.DEVNULL).strip()


def is_committed_and_clean(path: Path) -> bool:
    rel = path.relative_to(REPO).as_posix()
    try:
        tracked = git("ls-files", "--error-unmatch", rel)
    except subprocess.CalledProcessError:
        return False
    if not tracked:
        return False
    return git("status", "--porcelain", "--", rel) == ""


def prereg_ratified() -> tuple[bool, str]:
    rat = EPC / "PREREG.ratified"
    if not rat.exists():
        return False, "PREREG.ratified does not exist"
    lines = rat.read_text(encoding="utf-8").splitlines()
    recorded = next((l.split()[1] for l in lines if l.startswith("sha256 ")), None)
    actual = epc.sha256_file_lf(EPC / "PREREG.md")
    if recorded != actual:
        return False, f"PREREG.ratified records {recorded}, PREREG.md is {actual}"
    return True, "ok"


def manifest(cfg: dict, mode: str, model_version: str | None) -> dict:
    files = {
        "PREREG.md": EPC / "PREREG.md", "config.json": EPC / "config.json",
        cfg["output_contract"]: EPC / cfg["output_contract"],
        f"scenarios/{cfg['scenario']}.json": EPC / "scenarios" / f"{cfg['scenario']}.json",
        f"scenarios/{cfg['scenario']}.txt": EPC / "scenarios" / f"{cfg['scenario']}.txt",
        "scenarios/predicates.json": EPC / "scenarios" / "predicates.json",
    }
    for arm, f in cfg["arm_files"].items():
        files[f] = EPC / f
    gold = EPC / "annotations" / f"{cfg['scenario']}.gold.json"
    if gold.exists():
        files[f"annotations/{cfg['scenario']}.gold.json"] = gold
    vl = EPC / "scenarios" / f"{cfg['scenario']}.value-layer.json"
    if vl.exists():
        files[f"scenarios/{cfg['scenario']}.value-layer.json"] = vl
    for p in sorted((EPC / "scoring").glob("*.py")):
        files[f"scoring/{p.name}"] = p
    return {
        "schema": "e-pc/manifest/v1", "mode": mode, "created": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repo_commit": git("rev-parse", "HEAD") if mode != "smoke" else None,
        "prereg_sha256": epc.sha256_file_lf(EPC / "PREREG.md"),
        "files_sha256": {k: epc.sha256_file(v) for k, v in files.items()},
        "model_requested": cfg["model"], "model_version_served": model_version,
        "decoding": {"temperature": cfg["temperature"], "thinking": cfg["thinking"], "max_tokens": cfg["max_tokens"]},
        "runs_per_arm": cfg["runs_per_arm"], "python": sys.version, "platform": platform.platform(),
        "mrc": epc.mrc_profile() if mode != "smoke" else None,
        "parity": epc.parity(cfg),
    }


def extract_text(response) -> str:
    return "".join(b.text for b in response.content if b.type == "text")


def parse_output(text: str) -> dict | None:
    s = text.strip()
    if s.startswith("```"):
        s = s.strip("`")
        if s.lower().startswith("json"):
            s = s[4:]
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        start, end = s.find("{"), s.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(s[start:end + 1])
            except json.JSONDecodeError:
                return None
        return None


def run(mode: str, out_dir: Path, cfg: dict, case_text: str | None, n_runs: int) -> None:
    import anthropic

    client = anthropic.Anthropic()
    (out_dir / "raw").mkdir(parents=True, exist_ok=True)
    (out_dir / "outputs").mkdir(parents=True, exist_ok=True)
    model_version = None
    for arm in cfg["arms"]:
        prompt = epc.build_prompt(arm, cfg, case_text)
        for i in range(n_runs):
            request = {
                "model": cfg["model"], "max_tokens": cfg["max_tokens"], "temperature": cfg["temperature"],
                "thinking": cfg["thinking"], "messages": [{"role": "user", "content": prompt}],
            }
            (out_dir / "raw" / f"{arm}-{i}.request.json").write_text(json.dumps(request, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
            try:
                response = client.messages.create(**request)
            except anthropic.BadRequestError as e:
                raise SystemExit(f"{arm}-{i}: the API rejected the request ({e.message}). Resolve PREREG.md §12 O-1; nothing is dropped silently.")
            model_version = response.model
            (out_dir / "raw" / f"{arm}-{i}.response.json").write_text(json.dumps(response.to_dict(), indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8", newline="\n")
            if response.stop_reason not in ("end_turn", "stop_sequence"):
                print(f"warning: {arm}-{i} stop_reason {response.stop_reason}", file=sys.stderr)
            text = extract_text(response)
            (out_dir / "outputs" / f"{arm}-{i}.txt").write_bytes(text.encode("utf-8"))
            parsed = parse_output(text)
            if parsed is None:
                print(f"warning: {arm}-{i} output is not valid JSON; kept as text only", file=sys.stderr)
                parsed = {"sections": [], "synthesis": [], "_unparsed": True}
            (out_dir / "outputs" / f"{arm}-{i}.json").write_text(json.dumps(parsed, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
            print(f"{arm}-{i}: {response.stop_reason}, {response.usage.output_tokens} output tokens")
    (out_dir / "manifest.json").write_text(json.dumps(manifest(cfg, mode, model_version), indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out_dir}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--smoke", action="store_true")
    g.add_argument("--dev", action="store_true")
    g.add_argument("--credited", action="store_true")
    ap.add_argument("--out", default=None, help="smoke only: output directory (default: temp dir)")
    args = ap.parse_args()
    cfg = epc.load_config()
    gold = EPC / "annotations" / f"{cfg['scenario']}.gold.json"

    if args.smoke:
        fixture = REPO / "tests" / "e-pc" / "fixtures" / "smoke-case.txt"
        out = Path(args.out) if args.out else Path(tempfile.mkdtemp(prefix="epc-smoke-"))
        run("smoke", out, cfg, epc.load_text_exact(fixture), 1)
        return 0

    if not is_committed_and_clean(gold):
        raise SystemExit("refused: the gold annotation is not committed (or has uncommitted changes). No arm output may exist before the gold.")
    errs = epc.validate_annotations(gold)
    if errs:
        raise SystemExit("refused: gold annotation invalid:\n" + "\n".join(errs))
    if not epc.mrc_profile()["passed"]:
        raise SystemExit("refused: MRC gate failed: " + json.dumps(epc.mrc_profile()["flags"]))
    if not epc.parity(cfg)["passed"]:
        raise SystemExit("refused: arm length parity failed")

    if args.dev:
        out = EPC / "results" / ("dev_" + dt.datetime.now().strftime("%Y%m%dT%H%M%S"))
        run("dev", out, cfg, None, cfg["runs_per_arm"])
        return 0

    ok, why = prereg_ratified()
    if not ok:
        raise SystemExit(f"refused: {why}")
    for p in (EPC / "config.json", EPC / "PREREG.md", EPC / "PREREG.ratified", *(EPC / f for f in cfg["arm_files"].values()), EPC / cfg["output_contract"]):
        if not is_committed_and_clean(p):
            raise SystemExit(f"refused: {p.relative_to(REPO)} is not committed and clean")
    run_id = "credited_" + hashlib.sha256((git("rev-parse", "HEAD") + dt.datetime.now(dt.timezone.utc).isoformat()).encode()).hexdigest()[:10]
    out = EPC / "results" / run_id
    if out.exists():
        raise SystemExit("refused: run directory exists")
    run("credited", out, cfg, None, cfg["runs_per_arm"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
