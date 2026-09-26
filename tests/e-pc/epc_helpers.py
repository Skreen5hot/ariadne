"""Shared helpers for the E-PC gate tests (kept out of conftest so the two test packages do not shadow each other)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
EPC_DIR = ROOT / "experiments" / "e-pc"
sys.path.insert(0, str(EPC_DIR / "scoring"))

import epc  # noqa: E402


@pytest.fixture(scope="session")
def cfg():
    return epc.load_config()


@pytest.fixture(scope="session")
def scenario(cfg):
    return epc.load_scenario(cfg["scenario"])


@pytest.fixture(scope="session")
def prose(cfg):
    return epc.load_prose(cfg["scenario"])


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, stderr=subprocess.DEVNULL).strip()


def arm_output_files() -> list[Path]:
    """Every arm output in the working tree, credited or dev (dev is git-ignored but still an arm output)."""
    res = EPC_DIR / "results"
    if not res.exists():
        return []
    return sorted(p for p in res.glob("*/outputs/*.json"))
