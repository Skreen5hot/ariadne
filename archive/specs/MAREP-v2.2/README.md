# MAREP v2.2 + Integration Spec — v3.0 Design Artifacts

**Status:** Design artifacts for Barcode substrate v3.0
**Drafted:** 2026-05-18
**Provenance:** Iterated from MAREP v2.1 against Aaron's adjudications; normalized to Barcode substrate v2.8.0 conventions.

---

## What's here

This directory contains two related specifications that together define the retro-surface integration for Barcode substrate v3.0.

### `MAREP_v2.2.md` — The retro-surface specification

The Multi-Agent Retrospective Execution Protocol, normalized to the Barcode substrate conventions established through v2.8.0. Twenty-one sections specifying canonical state, agent roles, phase workflow, locking, consensus protocol, memory boundaries, anti-pattern enforcement, and substrate integration requirements.

Key normalizations from v2.1:
- Orchestrator clarified as LLM worker agent (Bounded-Authority Orchestrator pattern)
- Canonical state file renamed `.yaml` → `.jsonld`; outputs normalized to JSON envelopes
- Three-stage permitted_sections safety: static AGENTS.md + per-turn requested_sections + deterministic substrate validation
- Memory rules fully specified (working / episodic / semantic with explicit promotion + demotion rules)
- Anti-pattern detection mapped to substrate CPS surface
- Compression specified as logical relocation preserving append-only invariant
- Spec relocated under `surfaces/retro/` per FNSR Spec 01 surface-registry primitive

### `MAREP_INTEGRATION_SPEC.md` — Daemon Team implementation companion

Specifies the substrate-side implementation required for full MAREP conformance. Six net-new substrate primitives + three operator surface additions; estimated ~1500 LOC + ~80 tests across three checkpoints in v3.0.

Sequenced into v3.0 alongside the original build-order pieces:
- v3.0-alpha.1: BAO pattern formalization + generalized synthesist + MAREP `surfaces/retro/` foundation
- v3.0-alpha.2: MAREP substrate primitives + phase-complete-declaration
- v3.0: phase-exit retro end-to-end + `state_admin retro` family + Episodic→Semantic + final v3.0 tag

The integration spec includes seven open questions adjudicated by Aaron (BAO naming, JSONPath subset, redundant-affirmation threshold, forbidden-connectives list, mid-retro amendment semantics, surface attribution mechanism, vote-record URN convention) plus three FNSR-load-bearing pattern formalizations (BAO; Episodic→Semantic promotion discipline; substrate-mechanical anti-pattern enforcement framework).

---

## Convention pattern

This directory establishes the FNSR archive convention for design specifications: `archive/specs/<spec-name>-<version>/`. Each spec lives in its own versioned subdirectory with a README marking status, drafted date, and provenance. Future specs (v3.1+ generalized-synthesist refinements, eventual `surface_audience`, FNSR moral-person substrate work) follow the same layout.

Adjacent to `archive/retrospectives/` (which uses `YYYY-MM-topic-vX.Y.Z-to-vX.Y.Z.md` flat-file convention for sealed retrospectives). The two conventions are complementary: retrospectives capture what happened; specs capture what will happen.

---

## Relationship to the FNSR Protocol Specifications bundle

The v1.1 FNSR Protocol Specifications bundle (Specs 01–07; Logic-Team-authored; previously delivered to GraphWrite at `project/Routing/`) is the substrate's normative spec layer. MAREP v2.2 + Integration Spec are downstream — they implement Spec 01's surface-registry primitive for the retro surface, reuse Spec 07's forward-track mechanism for Episodic→Semantic promotion, and inherit the chain-hashed audit invariant from substrate v2.8.0.

Treat the v1.1 FNSR bundle as the substrate-canonical normative layer; MAREP as one instance of how that normative layer instantiates a specific surface. Future substrate-instance specs (e.g., specs for the cycle, commit, or bankings surfaces if those need formal specifications beyond what FNSR Specs 04/05 already provide) follow the same downstream pattern.

---

## Status

These specs are **design artifacts for v3.0 implementation**, not yet substrate-canonical. They become substrate-canonical when v3.0 ships with the implementation. Until then, they're the authoritative blueprint the Daemon Team works from.

If substantive revisions are needed before v3.0 implementation begins, they're applied to the spec files in this directory; the GraphWrite working copies have been removed to avoid drift between two locations.
