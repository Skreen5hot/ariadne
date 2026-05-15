# Drift Record

## Intentional Drift

### D-001: Character feedback restored
- **Date**: 2026-01-30
- **Original position**: Character was reporting metric only
- **New position**: Character genuinely influences decisions (auditably)
- **Reason**: ARCHON alignment requires real consequences
- **Approved by**: —

### D-002: Resource-cost model extends moral injury concept
- **Date**: 2026-01-30
- **Original position**: ARCHON describes moral injury as threshold-based (accumulated injury raises intervention thresholds)
- **New position**: Synthetic Moral Agency ties moral costs to physical resource consumption (compute, energy, time), making costs tangible and non-externalizable
- **Reason**: Bridges the gap between philosophical "moral injury" and implementable mechanism
- **Approved by**: — (discovered during ARIADNE review, pending formal approval)

### D-003: Developmental trajectory as architectural commitment
- **Date**: 2026-05-15 (ARIADNE Round 6; sourced from Beyond the Categorical Imperative v1.3 §7.4, February 2026)
- **Original position**: The system is a "guardian" — Plot §1 frames the goal as instantiating a guardian that preserves conditions for human agency.
- **New position**: The system is "a guardian that develops." Beyond Cat Imp v1.3 §7.4 introduces a three-stage developmental trajectory: Stage 1 (Kantian-Integral, current) → Stage 2 (Enhanced Responsiveness, mediated by the FNSR subjectivity stack — AVS, NIS, CTS, OCE as "concrete developmental mechanism") → Stage 3 (Aspirational: Moral Intuition, "direct cognitive contact with moral reality"). The architecture is *designed for* Stage 3 even though achieving it is an open question.
- **Reason**: Steiner-Kant tension treated honestly via dual-level resolution: Phenomenalism is meta-ethically operative but ontologically transcendable.
- **Approved by**: Pending — opens [[T-014]] for explicit reconciliation with No Oracle Claims.

### D-004: HIRI scope narrowing to verification primitive
- **Date**: 2026-05-15 (ARIADNE Round 6; sourced from HIRI Protocol v3.1.1, March 2026)
- **Original position**: HIRI v2.1.0 included a Privacy Accumulator model with a centralized Privacy Authority for cross-verifier privacy budget enforcement.
- **New position**: HIRI v3.1.1 narrows scope to "verification primitive, not trust infrastructure." §19.3 Privacy Accumulators reduced to `Reserved for selective disclosure. Interface TBD.` The Privacy Authority concept is *removed*. The HIRI Privacy & Confidentiality Extension v1.4.1 replaces it with five declarative privacy modes (Proof of Possession, Encrypted Distribution, Selective Disclosure, Anonymous Publication, Third-Party Attestation), each publisher-driven and network-agnostic. The HIRI Digital Passport v1.9.0 RC §17 adds per-verifier Oracle Trust Anchors (distributed governance).
- **Reason**: Architectural response to the concentration risk surfaced by [[T-011]]. Removing the central authority *by not building it* is a principled answer.
- **Approved by**: Pending — closes [[T-011]] pending one validation cycle.

### D-005: Filename/version mismatch pattern (accidental drift, corrections applied)
- **Date**: 2026-05-15 (ARIADNE Round 6)
- **Original position**: Three specs had filenames that did not match the version declared in the spec header:
  - `opa-v1.1.md` contained v1.2 content
  - `middle-layer-shml.md` contained v3.0 content; v3.2 lived in `SHML-v3.2.md` as the canonical
  - `fandaws-type-agent-v2.2.md` contained v2.3 content
- **New position**: Files renamed at coherence-review time via `git mv` to preserve history:
  - `opa-v1.1.md` → `opa-v1.2.md`
  - `middle-layer-shml.md` → `archived/middle-layer-shml-v3.0.md` (superseded by v3.2)
  - `fandaws-type-agent-v2.2.md` → `fandaws-type-agent-v2.3.md`
- **Reason**: Filename version is a discovery affordance. When it lags the content it actively misleads readers searching for the current version.
- **Approved by**: Aaron Damiano (2026-05-15)

### D-006: Service count expansion from 19 (Plot §4) to 42 (Portfolio v3.4)
- **Date**: 2026-05-15 (ARIADNE Round 6; service growth documented in Orchestrator §1.4)
- **Original position**: Plot §4 component map covered approximately 19 components (ARCHON, Line in the Sand, Integral Ethics, BFO/CCO, Fandaws, W2Fuel, OERS, HIRI, MDRE, AES, DES, CSS, APS, ECCPS, SIS, SHML, TagTeam, IEE, FNSR).
- **New position**: Portfolio v3.4 = 42 services, documented in FNSR Orchestrator §1.4: *"Portfolio v2.0: 29 services → Portfolio v3.0: 37 (+5 subjectivity: SMS, CTS, NIS, AVS, SoMS; +3 safety: CPS, BAM, IS) → Portfolio v3.4: 42 (+5 data pipeline/causal: ECVE, BIBSS, SAS, SNP, Causal OS Kernel)."*
- **Reason**: The corpus matured beyond the initial component map. The new clusters (Safety Triad, Subjectivity Stack, Data Pipeline parallel track) represent genuine architectural domains that didn't exist when the Plot was drafted.
- **Approved by**: Pending — recommend updating Plot §4 component table to reflect the 42-service inventory.

### D-007: Forward-reference version pattern (intentional ecosystem coherence)
- **Date**: 2026-05-15 (ARIADNE Round 6)
- **Original position**: Specs were assumed to reference only versions present in the corpus.
- **New position**: Multiple specs coherently forward-reference planned versions that do not yet exist on disk:
  - FNSR Orchestrator v2.3 cites "ARCHON v3.0" (corpus has v2.0)
  - FNSR Orchestrator §1.4 cites "Portfolio Planning Document v3.6.0" (corpus has v1.0)
  - OPA v1.2 cites "Target System: Fandaws v3.4+" (corpus has v3.3)
  - SPCN §CS-6 / SPL / fandaws-hiri-ipfs cite "CTS v2.1" (corpus has v1.2.1)
  - W2Fuel Adapters v1.1.0 cites "Companion to: `w2fuel-core-01` v2.0.0" (corpus has v1.3.1)
- **Reason**: The ecosystem is being designed coherently against intended future state. Forward references are intentional architectural commitments. Treating them as version errors would miss the design intent.
- **Approved by**: Pending — recommend either (a) bringing the forward-referenced versions into the corpus, or (b) explicitly documenting them as planned versions in the Portfolio Planning document.

## Accidental Drift (Corrections Needed)

### Stale governance artifact: `docs/04-governance/drift_report.md`
- **Date observed**: 2026-05-15
- **Nature**: Generated by Spec-Driven Discovery v1.1 §7 on 2026-01-31 against an earlier corpus state. Lists 7 services as MISSING_SPEC (SIS, OERS, W2Fuel, AES, DES, CSS, APS) — all 7 now exist as specs. Pre-dates the safety triad, subjectivity stack, and data pipeline expansion.
- **Recommended action**: Move to `docs/04-governance/archived/drift_report-2026-01-31.md` to preserve snapshot value without misleading readers about current state.
- **Status**: Pending file move.
