# Third-party notices

This repository redistributes material it did not author. This file
records what that material is, where it came from, and under what terms —
or, where the terms are unknown, says so plainly.

Counts are not written here. Run

    python tools/licensing/disposition.py

for the live figures; a number copied into prose stops tracking what it
counts.

---

## Basic Formal Ontology (BFO)

- **Where:** `ontology/bfo/vendor/bfo/`
- **Upstream:** <https://github.com/BFO-ontology/BFO-2020>
- **Licence:** CC BY 4.0 — [LICENSES/CC-BY-4.0.txt](LICENSES/CC-BY-4.0.txt)
- **Relationship:** vendored unchanged so the suite loads offline without
  fetching an import IRI at parse time.

BFO is the upper ontology every ValueNet class descends from. It is
redistributed under its own terms; nothing in this repository alters it
or claims rights over it.

## Common Core Ontologies (CCO)

- **Where:** `ontology/bfo/vendor/cco/`
- **Upstream:** <https://github.com/CommonCoreOntology/CommonCoreOntologies>
- **Licence:** BSD-3-Clause — [LICENSES/BSD-3-Clause.txt](LICENSES/BSD-3-Clause.txt)
- **Relationship:** a pinned MIREOT-style extract, generated here from
  upstream CCO by `tools/bfo/generate_cco_extract.py`, supplying the
  information-entity terms the evidence chain uses.

The extract is a *selection* from upstream CCO, not a modification of it.
Its provenance manifest sits beside it and records the source, the
selection, and a canonical digest that is checked on every run.

---

## Original ValueNet — licence not identified

- **Where:** `ThatsAllFolks/`, `MFTriggers/`, `vale2024/`, and the
  ValueNet Turtle files at the repository root
- **Upstream:** <https://github.com/StenDoipanni/ValueNet>
- **Licence:** **not identified**
- **Relationship:** the source tradition this work re-expresses. It is the
  mapping target for the BFO-aligned suite.

**No licence has been identified for this material, and this repository
grants no rights over it.**

That statement is deliberate and load-bearing:

- Its presence here is not a representation that it may be reused.
- It is **excluded from the public download bundle** until redistribution
  terms are established.
- It is not relicensed under the project's own terms. Applying CC BY 4.0
  to it would be relicensing somebody else's work by omission, which is
  the opposite of the permissive intent behind the project licences.

By file count this is the **largest** category in the repository. That
reflects where ValueNet came from: the original corpus is substantial and
the BFO-aligned suite is a comparatively small, densely authored layer on
top of it.

Anyone wishing to reuse this material should establish terms with the
upstream authors directly.

### How the boundary is drawn

From recorded provenance plus explicit owner adjudications — not from a
list of filenames.

Each file's origin is read from `config/move-manifest.yaml`, a
provenance record frozen and reviewed before this licensing work began,
which classifies every file as `fork`, `upstream-valuenet`,
`external-bfo`, or `external-cco`. A tracked file absent from that
manifest is confirmed absent from a recorded upstream snapshot before it
is treated as fork-authored.

The snapshot is a commit named in `config/upstream-snapshot.yaml`, not a
remote branch, so the classification does not depend on the state of
anybody else's repository at the moment it runs. It is an ancestor of
this repository's history: a full clone contains it and needs no
`upstream` remote, while a shallow clone does not and is refused rather
than answered.

Where recorded descent and current authorship diverge, the owner rules
on the named file and the ruling is recorded with its evidence. One such
ruling exists: `README.md`, rewritten in full at commit `39a8001`. It
does not generalize. The folk fragments retain most of their upstream
text and remain unresolved, and a test requires every
`upstream-valuenet` file other than the single adjudicated one to stay
excluded.

`tests/licensing/test_disposition.py` requires every tracked file to
fall under exactly one disposition, so a new file cannot land without
one and an overlapping rule fails rather than resolving silently.
