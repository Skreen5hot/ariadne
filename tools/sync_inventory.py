"""Add every repository the owner has on GitHub to docs/05-evidence-audit/inventory.yaml.

Usage:  python tools/sync_inventory.py            (needs the GitHub CLI, signed in: gh auth login)
        python tools/sync_inventory.py --dry-run  (print what would be added)

Only adds; never removes or edits an existing entry. New entries get `role: unsorted` and
`implements: []` until Aaron places them and someone states, with a basis, which spec-index
entries the repository implements. Forks, archived repositories and names under `out_of_scope`
are skipped and listed so the skip is visible. Private repositories are skipped unless already
inventoried: ariadne is public, and personal repositories must not be named in it.
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
    out_of_scope = set(inv.get("out_of_scope") or [])
    skipped = [x["name"] for x in listed if x["isFork"] or x["isArchived"]]
    private = [x for x in listed if x["isPrivate"] and x["name"] not in have]
    new = sorted((x for x in listed if not (x["isFork"] or x["isArchived"] or x["isPrivate"])
                  and x["name"] not in have | out_of_scope), key=lambda x: x["name"].lower())
    lines = []
    for x in new:
        lines += [f"  - name: {x['name']}", "    role: unsorted", "    implements: []",
                  "    mapping_basis: added by sync_inventory; mapping not yet established"]
    print(f"{len(listed)} repositories on GitHub; {len(have)} already inventoried; adding {len(new)}; "
          f"skipped {len(skipped)} forks/archived: {', '.join(skipped) or 'none'}; "
          f"skipped {len(out_of_scope)} out of scope; skipped {len(private)} private, not inventoried "
          "(add by hand if FNSR work)")
    if lines and "--dry-run" not in argv:
        # New entries go at the end of the repos list, before the out_of_scope block.
        text = INVENTORY.read_text(encoding="utf-8")
        marker = "\n# Public repositories that are not part of FNSR."
        cut = text.find(marker)
        head, tail = (text, "") if cut < 0 else (text[:cut], text[cut:])
        head = head.rstrip("\n") + "\n" + "\n".join(lines) + "\n"
        INVENTORY.write_text(head + tail, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
