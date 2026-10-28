"""Collect machine evidence for every repository in docs/05-evidence-audit/inventory.yaml.

Usage:
  python tools/collect_evidence.py                  collect static evidence for all repos
  python tools/collect_evidence.py --run            also execute each repo's tests
  python tools/collect_evidence.py --run NAME ...   only the named repos
  python tools/collect_evidence.py --workdir DIR    where clones go (default: a temp dir)

For every repository the collector shallow-clones the default branch and records what it
finds into docs/05-evidence-audit/evidence/<repo>.json. Those files are machine output:
never edit them by hand. A level is never written anywhere; it is computed from these
records by tools/evidence_audit.py.

With --run, tests are executed in the clone (pytest for Python, `npm test` for Node).
Run it on a machine where you are willing to execute your own repositories' test suites.
Private repositories need credentials that can clone them (e.g. `gh auth login`).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evidence_audit import EVIDENCE, REPO_SCHEMA, evidence_file, load_inventory  # noqa: E402

COLLECTOR_VERSION = "1.0.0"
OWNER_DEFAULT = "Skreen5hot"

SOURCE_EXT = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".cs",
              ".rb", ".php", ".kt", ".swift", ".c", ".cpp", ".h", ".sh", ".ps1", ".sparql", ".rq",
              ".shacl", ".vue", ".svelte"}
# Ontology and data artifacts are counted separately: an ontology is real work, but it is
# not executable code, so it does not by itself put a repository at L1.
ONTOLOGY_EXT = {".ttl", ".owl", ".rdf", ".jsonld", ".nt", ".nq", ".trig", ".obo", ".shex"}
DOC_EXT = {".md", ".txt", ".rst", ".adoc", ".pdf", ".docx"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__", "vendor",
             "coverage", ".next", "site-packages"}
TEST_PATTERNS = [
    re.compile(r"(^|/)test_[^/]+\.py$"),
    re.compile(r"(^|/)[^/]+_test\.py$"),
    re.compile(r"(^|/)[^/]+\.(test|spec)\.(js|mjs|cjs|ts|tsx|jsx)$"),
    re.compile(r"(^|/)__tests__/[^/]+\.(js|mjs|cjs|ts|tsx|jsx)$"),
    re.compile(r"(^|/)(tests?|spec)/.+\.(js|mjs|cjs|ts|py)$"),
    re.compile(r"(^|/)[^/]+_test\.go$"),
]
NOT_A_TEST = re.compile(r"^(conftest\.py|__init__\.py|.*helpers?\.(py|js|ts)|_?support\.py|fixtures?\.(py|js))$", re.I)
MANIFESTS = {"package.json", "requirements.txt", "pyproject.toml", "setup.py", "setup.cfg",
             "Cargo.toml", "go.mod", "pom.xml", "build.gradle"}


def sh(cmd: list[str], cwd: Path | None = None, timeout: int = 600, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                          env={**os.environ, **(env or {})}, errors="replace")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            p = Path(dirpath) / f
            yield p, p.relative_to(root).as_posix()


def classify_files(root: Path) -> tuple[dict, list[str], list[str]]:
    counts = Counter()
    ext_counts = Counter()
    tests: list[str] = []
    rels: list[str] = []
    for p, rel in walk(root):
        rels.append(rel)
        ext = p.suffix.lower()
        ext_counts[ext or "(none)"] += 1
        if ext in SOURCE_EXT:
            counts["source"] += 1
        elif ext in ONTOLOGY_EXT:
            counts["ontology"] += 1
        elif ext in DOC_EXT:
            counts["docs"] += 1
        else:
            counts["other"] += 1
        if (any(rx.search(rel) for rx in TEST_PATTERNS) and ext in SOURCE_EXT
                and not NOT_A_TEST.search(p.name)):
            tests.append(rel)
    files = {
        "total": len(rels),
        "source": counts["source"],
        "ontology": counts["ontology"],
        "docs": counts["docs"],
        "other": counts["other"],
        "top_extensions": dict(ext_counts.most_common(6)),
    }
    return files, sorted(tests), rels


def npm_test_script(root: Path) -> str | None:
    """The script CI should run: `test:ci` when the repository defines one, else `test`."""
    pkg = root / "package.json"
    if not pkg.exists():
        return None
    try:
        scripts = json.loads(pkg.read_text(encoding="utf-8")).get("scripts") or {}
    except json.JSONDecodeError:
        return None
    for name in ("test:ci", "test"):
        s = scripts.get(name, "")
        if s and "no test specified" not in s:
            return name
    return None


def detect_runner(root: Path, tests: list[str]) -> str:
    if npm_test_script(root):
        return "npm"
    if any(t.endswith(".py") for t in tests):
        return "pytest"
    return "none"


def ci_facts(root: Path, default_branch: str) -> dict:
    wf_dir = root / ".github" / "workflows"
    workflows, deploys, scheduled, on_default = [], False, False, False
    if wf_dir.exists():
        for p in sorted(list(wf_dir.glob("*.yml")) + list(wf_dir.glob("*.yaml"))):
            text = p.read_text(encoding="utf-8", errors="replace")
            workflows.append(p.name)
            low = text.lower()
            if "deploy-pages" in low or "gh-pages" in low or "pages:" in low or re.search(r"\bdeploy", low):
                deploys = True
            if "schedule:" in low or "cron:" in low:
                scheduled = True
            if "push:" in low and (default_branch in text or "branches:" not in low):
                on_default = True
            elif re.search(r"^\s*on:\s*\[?\s*push", text, re.M):
                on_default = True
    return {"workflows": workflows, "deploys": deploys, "scheduled": scheduled,
            "on_default_branch": on_default}


def find_references(root: Path, rels: list[str], self_name: str, others: list[str]) -> list[dict]:
    """References from this repo to other inventoried repos. Only code and manifests count
    toward 'used'; documentation references are recorded separately as kind 'docs'."""
    # Only unambiguous addresses count: a GitHub URL, a raw-content URL, or a Pages URL.
    # A bare word match ("valuenet" in a test string) is not evidence of dependence.
    pats = {o: re.compile(rf"((github|raw\.githubusercontent)\.com/{OWNER_DEFAULT}/{re.escape(o)}(?![\w.-])"
                          rf"|{OWNER_DEFAULT}\.github\.io/{re.escape(o)}(?![\w.-]))", re.I)
            for o in others if o != self_name}
    found: dict[tuple[str, str], str] = {}
    for rel in rels:
        p = root / rel
        name = p.name
        ext = p.suffix.lower()
        if name in MANIFESTS:
            kind = "manifest"
        elif ext in SOURCE_EXT or ext in {".html", ".json", ".yml", ".yaml"}:
            kind = "code"
        elif ext in DOC_EXT:
            kind = "docs"
        else:
            continue
        try:
            if p.stat().st_size > 2_000_000:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for other, rx in pats.items():
            if rx.search(text):
                key = (other, kind)
                found.setdefault(key, rel)
    return [{"repo": r, "kind": k, "file": f} for (r, k), f in sorted(found.items())]


def run_tests(root: Path, runner: str, sha: str) -> dict | None:
    if runner == "none":
        return None
    start = time.time()
    env = {"CI": "true", "PYTHONDONTWRITEBYTECODE": "1"}
    log: list[str] = []
    try:
        if runner == "npm":
            install = ["npm", "ci"] if (root / "package-lock.json").exists() else ["npm", "install"]
            r = sh(install + ["--no-audit", "--no-fund"], cwd=root, timeout=900, env=env)
            log.append(f"$ {' '.join(install)} -> {r.returncode}")
            script = npm_test_script(root)
            if r.returncode != 0:
                return finish(["npm", "run", script], r.returncode, start, sha, (r.stdout + r.stderr),
                              "install failed", setup_failure=True)
            cmd = ["npm", "run", "--silent", script]
        else:
            for req in ("requirements.txt", "requirements-dev.txt"):
                if (root / req).exists():
                    r = sh([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", "-r", req],
                           cwd=root, timeout=900)
                    log.append(f"$ pip install -r {req} -> {r.returncode}")
            cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"]
        r = sh(cmd, cwd=root, timeout=1200, env=env)
        return finish(cmd, r.returncode, start, sha, r.stdout + r.stderr, "; ".join(log))
    except subprocess.TimeoutExpired:
        return finish([runner], 124, start, sha, "", "timed out", setup_failure=True)


def finish(cmd, code, start, sha, output, note, setup_failure=False) -> dict:
    tail = [l[:200] for l in output.strip().splitlines() if l.strip()][-6:]
    # pytest exit codes 2-5 mean interrupted, internal error, usage error or no tests:
    # the suite did not run to a verdict. So does a failed install or a missing entry point.
    not_run = setup_failure
    if "pytest" in " ".join(cmd) and code in (2, 3, 4, 5):
        not_run = True
    if "MODULE_NOT_FOUND" in output or "Cannot find module" in output:
        not_run = True
    outcome = "passed" if code == 0 else ("could_not_run" if not_run else "failed")
    return {"command": " ".join(Path(c).name if i == 0 else c for i, c in enumerate(cmd)),
            "exit_code": code, "outcome": outcome, "duration_s": round(time.time() - start, 1),
            "sha": sha, "at": now_iso(), "summary": tail, "note": note}


def collect(repo: dict, others: list[str], workdir: Path, run: bool) -> dict:
    name = repo["name"]
    owner = repo.get("owner", OWNER_DEFAULT)
    url = f"https://github.com/{owner}/{name}"
    dest = workdir / name
    if dest.exists():
        shutil.rmtree(dest)
    rec: dict = {"schema": REPO_SCHEMA, "repo": name, "url": url, "collected_at": now_iso(),
                 "collector_version": COLLECTOR_VERSION}
    # Full history without blobs: test suites that check ancestry (e.g. a pinned upstream
    # snapshot) need commits a shallow clone would omit, and blob filtering keeps it cheap.
    r = sh(["git", "clone", "--filter=blob:none", "--quiet", url, str(dest)], timeout=900,
           env={"GIT_TERMINAL_PROMPT": "0"})
    if r.returncode != 0:
        rec.update({"reachable": False, "error": (r.stderr.strip().splitlines() or ["clone failed"])[-1][:200]})
        return rec
    rec["reachable"] = True
    head = sh(["git", "log", "-1", "--format=%H%x09%cI%x09%s"], cwd=dest).stdout.strip().split("\t")
    branch = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=dest).stdout.strip()
    heads = sh(["git", "ls-remote", "--heads", url], timeout=120).stdout
    rec["head"] = {"sha": head[0], "date": head[1], "subject": head[2][:120] if len(head) > 2 else ""}
    rec["default_branch"] = branch
    rec["gh_pages_branch"] = "refs/heads/gh-pages" in heads
    files, tests, rels = classify_files(dest)
    rec["files"] = files
    runner = detect_runner(dest, tests)
    rec["tests"] = {"files": len(tests), "runner": runner, "examples": tests[:5]}
    ci = ci_facts(dest, branch)
    if rec["gh_pages_branch"]:
        ci["deploys"] = True
    rec["ci"] = ci
    rec["references"] = find_references(dest, rels, name, others)
    previous = None
    if evidence_file(name).exists():
        previous = json.loads(evidence_file(name).read_text(encoding="utf-8")).get("run")
    if run:
        rec["run"] = run_tests(dest, runner, rec["head"]["sha"])
    else:
        # Keep an earlier test run only if it is for the same commit; otherwise it no longer
        # describes this code and is dropped rather than carried forward.
        rec["run"] = previous if previous and previous.get("sha") == rec["head"]["sha"] else None
    return rec


def main(argv: list[str]) -> int:
    run = "--run" in argv
    workdir = None
    names = []
    it = iter(argv)
    for a in it:
        if a == "--workdir":
            workdir = Path(next(it))
        elif not a.startswith("--"):
            names.append(a)
    inv = load_inventory()
    repos = inv.get("repos") or []
    all_names = [r["name"] for r in repos]
    selected = [r for r in repos if not names or r["name"] in names]
    unknown = set(names) - set(all_names)
    if unknown:
        print(f"not in inventory: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    tmp = None
    if workdir is None:
        tmp = tempfile.mkdtemp(prefix="evidence-audit-")
        workdir = Path(tmp)
    workdir.mkdir(parents=True, exist_ok=True)
    try:
        for repo in selected:
            print(f"collecting {repo['name']} ...", flush=True)
            rec = collect(repo, all_names, workdir, run)
            evidence_file(repo["name"]).write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n",
                                                   encoding="utf-8", newline="\n")
            status = "unreachable" if not rec["reachable"] else (
                f"{rec['files']['source']} src, {rec['tests']['files']} tests"
                + (f", run exit {rec['run']['exit_code']}" if rec.get("run") else ""))
            print(f"  {status}")
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
