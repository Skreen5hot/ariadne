"""test_gold_blind: gold annotations were committed before any arm output exists (checked in git history).

Rules enforced:
  1. If any arm output exists in the working tree (credited or dev), the gold must be committed.
  2. For every committed arm output, the commit that first added the gold must be an ancestor of the commit
     that first added the output (and not the same commit).
  3. The gold, once committed, is not modified after any output exists.
With no outputs and no gold the test passes vacuously and says so.
"""
from __future__ import annotations

import subprocess

import pytest

from conftest import EPC_DIR, ROOT, arm_output_files, git


def first_add_commit(rel: str) -> str | None:
    out = git("log", "--diff-filter=A", "--format=%H", "--", rel)
    lines = out.splitlines()
    return lines[-1] if lines else None


def is_tracked(rel: str) -> bool:
    try:
        return bool(git("ls-files", "--", rel))
    except subprocess.CalledProcessError:
        return False


def test_gold_committed_before_any_arm_output(cfg):
    gold_rel = f"experiments/e-pc/annotations/{cfg['scenario']}.gold.json"
    outputs = arm_output_files()
    gold_commit = first_add_commit(gold_rel) if is_tracked(gold_rel) else None
    if not outputs:
        if gold_commit is None:
            pytest.skip("no gold and no arm outputs yet: nothing to check")
        return
    assert gold_commit is not None, f"arm outputs exist ({len(outputs)}) but the gold is not committed"
    for p in outputs:
        rel = p.relative_to(ROOT).as_posix()
        if not is_tracked(rel):
            continue  # a dev output; rule 1 already holds
        out_commit = first_add_commit(rel)
        assert out_commit and out_commit != gold_commit, f"{rel} was added in the same commit as the gold"
        anc = subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", gold_commit, out_commit]).returncode
        assert anc == 0, f"gold commit {gold_commit[:10]} is not an ancestor of the commit adding {rel}"


def test_gold_not_modified_after_outputs_exist(cfg):
    gold_rel = f"experiments/e-pc/annotations/{cfg['scenario']}.gold.json"
    outputs = [p for p in arm_output_files() if is_tracked(p.relative_to(ROOT).as_posix())]
    if not outputs or not is_tracked(gold_rel):
        pytest.skip("no committed outputs or no gold")
    gold_commits = git("log", "--format=%H", "--", gold_rel).splitlines()
    earliest_output = min(first_add_commit(p.relative_to(ROOT).as_posix()) for p in outputs)
    for c in gold_commits:
        if c == first_add_commit(gold_rel):
            continue
        later = subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", earliest_output, c]).returncode == 0
        assert not later, f"gold modified in {c[:10]} after an arm output existed"
    assert git("status", "--porcelain", "--", gold_rel) == "", "gold has uncommitted changes while outputs exist"
