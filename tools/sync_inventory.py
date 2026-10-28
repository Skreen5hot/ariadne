"""Add every repository the owner has on GitHub to docs/05-evidence-audit/inventory.yaml.

Usage:  python tools/sync_inventory.py            (needs the GitHub CLI, signed in: gh auth login)
        python tools/sync_inventory.py --dry-run  (print what would be added)

Only adds; never removes or edits an existing entry. New entries get `implements: []`
until someone states, with a basis, which spec-index entries the repository implements.
Forks and archived repositories are skipped and listed so the skip is visible.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from evidence_audit import INVENTORY, load_inventory  # noqa: E402


def main(argv: list[str]) -> int:
    inv = load_inventory()
    owner = inv.get("owner", "Skreen5hot")
    r = subprocess.run(["gh", "repo", "list", owner, "--limit", "1000", "--json",
                        "name,isFork,isArchived,isPrivate,pushedAt"], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr.strip() or "gh repo list failed", file=sys.stderr)
        return 1
    listed = json.loads(r.stdout)
    have = {x["name"] for x in inv.get("repos") or []}
    skipped = [x["name"] for x in listed if x["isFork"] or x["isArchived"]]
    new = sorted((x for x in listed if not (x["isFork"] or x["isArchived"]) and x["name"] not in have),
                 key=lambda x: x["name"].lower())
    lines = []
    for x in new:
        basis = "added by sync_inventory; mapping not yet established" + (" (private)" if x["isPrivate"] else "")
        lines += [f"  - name: {x['name']}", "    implements: []", f"    mapping_basis: {basis}"]
    print(f"{len(listed)} repositories on GitHub; {len(have)} already inventoried; adding {len(new)}; "
          f"skipped {len(skipped)} forks/archived: {', '.join(skipped) or 'none'}")
    if lines and "--dry-run" not in argv:
        text = INVENTORY.read_text(encoding="utf-8")
        if not text.endswith("\n"):
            text += "\n"
        INVENTORY.write_text(text + "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
