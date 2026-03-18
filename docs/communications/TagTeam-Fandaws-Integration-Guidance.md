# TagTeam ↔ Fandaws Integration: Architectural Context & Action Items

---

| Attribute | Value |
|-----------|-------|
| **To** | TagTeam Development Team, Fandaws Development Team |
| **From** | ARIADNE (Portfolio Coherence Review) |
| **Date** | February 23, 2026 |
| **Re** | Phase 5 ParseResult Contract — Alignment with FNSR Ecosystem Architecture |
| **Priority** | Action Required Before Phase 5 Finalization |

---

## 1. What This Is

You're building the first real connection between two FNSR services. That makes your Phase 5 work foundational — not just for TagTeam and Fandaws, but for every service that will consume parsed claims downstream. This memo provides the broader architectural context for your integration and identifies four changes to the ParseResult contract that will prevent costly rework later.

**The good news:** your parsing engineering is strong and well-aligned with the thesis. The changes requested here are additive, not corrective — you're not doing anything wrong, you're missing some scaffolding that the broader architecture requires.

---

## 2. The Bigger Picture: Where Your Work Sits

### 2.1 The Epistemic Loop

The FNSR ecosystem's Phase 1 goal is a closed epistemic loop — the minimum viable path from natural language input to trustworthy persistent knowledge:

```
TagTeam  →  HIRI  →  Fandaws
(Perceive)    (Identity)    (Remember)

NL → Claims     Claims → Signed IRIs     IRIs → Persistent A-Box
```

TagTeam extracts structured claims from natural language. HIRI gives each claim a content-addressed identity (a hash-based IRI with cryptographic signature). Fandaws persists claims as knowledge, indexed by their HIRI identifiers.

**The critical architectural constraint:** Fandaws must be built *natively* on HIRI identifiers. If facts are stored without provenance anchors now and HIRI is added later, every early fact either lacks provenance (creating a two-tier knowledge base) or requires migration (breaking referential stability). Since Fandaws is being remade from scratch, this is the one opportunity to get it right from the start.

### 2.2 Your Phase 5 in the Portfolio Timeline

Your internal "Phase 5" maps to **Portfolio Phase 1** (Epistemic Loop + Containment). You're working on the TagTeam → Fandaws connection. HIRI doesn't exist yet as an implementation — it's spec-only. That's fine. You don't need to wait for HIRI. But you do need to **design the contract so HIRI slots in cleanly** when it arrives.

### 2.3 Who Else Will Consume TagTeam Output

Your ParseResult contract feels like a bilateral agreement between TagTeam and Fandaws. It isn't. In later phases, these services will also consume TagTeam's output:

| Service | Phase | What It Needs From TagTeam |
|---------|-------|---------------------------|
| **SIS** (Sanitization) | Phase 2 | Raw claims for input validation |
| **ECCPS** (Claim Validator) | Phase 2 | Structured claims for semantic validation |
| **MDRE** (Reasoning) | Phase 2 | Claims + discourse metadata for modal/deontic inference |
| **HIRI** (Provenance) | Phase 1 | Claims to sign with hash-IRIs |
| **BAM** (Alignment Monitor) | Phase 2 | Claim provenance for alignment tracking |

If the contract is `fandaws:ParseResult` with a `fandaws:` namespace, every future consumer must either depend on Fandaws's schema or reinvent the contract. The FNSR Integration Spec already defines a shared event format for exactly this reason.

---

## 3. What You're Doing Well

Before the action items — recognition for what's already aligned:

| Element | Why It Matters |
|---------|---------------|
| **JSON-LD output** | Matches the ecosystem's JSON-LD canonical requirement. Every service speaks JSON-LD. |
| **Confidence propagation** (minimum-arc approach) | Epistemically honest — propagating the weakest link rather than averaging. This maps directly to `fnsr-confidence`. |
| **Discourse annotations** (speech act, modality, hedging) | MDRE *needs* modality detection to distinguish epistemic ("may") from deontic ("must") claims. IEE needs speech acts to tell assertions from directives. You're building infrastructure that Phase 2+ services will depend on. |
| **CCO references** (`cco:has_part`, `cco:member_of`) | Aligned with the BFO/CCO ontology that W2Fuel will formalize. |
| **Negation detection** (AC-5.14) | Prevents false knowledge commitments. "A whale is not a fish" must not produce `whale subClassOf fish`. This is epistemically critical. |
| **Passive-voice agent resolution** (AC-5.12) | Essential for downstream deontic reasoning — "who obligated whom" requires knowing the true agent, not the surface subject. |
| **Adapter pattern** | Clean separation of concerns. The adapter is exactly where HIRI middleware will insert later. |

This is solid work. The four items below build on it.

---

## 4. Action Items

### ACTION 1: Add Provenance and Taint Fields to ParseResult

**Why:** Every claim in the FNSR ecosystem carries two pieces of metadata: its epistemic taint level (how trustworthy is this?) and its provenance anchor (who vouches for it?). Without these fields, downstream services can't assess claim reliability, and HIRI has no insertion point.

**What to do:** Add three fields to the ParseResult schema. They're nullable now and become required when HIRI is operational.

```json
{
  "@type": "fandaws:ParseResult",
  "fandaws:subject": "dog",
  "fandaws:predicate": "is",
  "fandaws:object": "animal",
  "fandaws:verbType": "classification",
  "fandaws:confidence": 0.94,
  "fandaws:parserImplementation": "tagteam-js",
  "fandaws:discourseAnnotations": { ... },

  "fnsr:taintLevel": "L2",
  "fnsr:provenance": null,
  "fnsr:claimIRI": null
}
```

| Field | Now | When HIRI Exists |
|-------|-----|------------------|
| `fnsr:taintLevel` | `"L2"` (unverified parser output) | Promoted based on HIRI signing |
| `fnsr:provenance` | `null` | `"hiri://sha256:abc123..."` |
| `fnsr:claimIRI` | `null` | Content-addressed IRI for this claim |

**Taint levels for reference:**

| Level | Meaning | Example |
|-------|---------|---------|
| L0 | Axiom / formally verified | BFO class definitions |
| L1 | Human-attested | User-confirmed facts |
| L2 | External / unverified | Parser output (this is you) |
| L3 | Speculative / inferred | MDRE reasoning output |
| L4 | Adversarial / untrusted | Unvalidated external input |
| L5 | Quarantined | Flagged by SIS |

TagTeam output is L2 by default — structured extraction from natural language without human verification or cryptographic signing.

**Acceptance criterion to add:**

```
AC-5.16: Taint and Provenance Fields
- GIVEN any valid ParseResult
- THEN fnsr:taintLevel is present and = "L2"
- AND fnsr:provenance is present (null is valid)
- AND fnsr:claimIRI is present (null is valid)
- AND the ParseResult remains valid JSON-LD with these fields
```

---

### ACTION 2: Emit `fnsr.claim.extracted` at the Service Boundary

**Why:** The FNSR Integration Spec (v1.0) defines a CloudEvents-based event contract that all services use to communicate. TagTeam's output event is `fnsr.claim.extracted`. If TagTeam emits only `fandaws:ParseResult`, then every future consumer (SIS, ECCPS, MDRE, BAM) must understand Fandaws's internal schema. If TagTeam emits `fnsr.claim.extracted`, any service can subscribe.

**What to do:** Wrap the ParseResult in a CloudEvents envelope at the service boundary. Fandaws can unwrap it internally into its own ParseResult format — that's fine. But the *published event* should be the shared contract.

```json
{
  "specversion": "1.0",
  "type": "fnsr.claim.extracted",
  "source": "/fnsr/tagteam",
  "id": "evt-uuid-here",
  "time": "2026-02-23T10:30:00Z",
  "datacontenttype": "application/ld+json",

  "fnsr-taint": "L2",
  "fnsr-confidence": 0.94,
  "fnsr-provenance": null,

  "data": {
    "@type": "fnsr:ExtractedClaim",
    "fnsr:subject": "dog",
    "fnsr:predicate": "is",
    "fnsr:object": "animal",
    "fnsr:verbType": "classification",
    "fnsr:parserImplementation": "tagteam-js",
    "fnsr:discourseAnnotations": {
      "speechAct": "assertion",
      "modality": "realis",
      "hedging": false
    }
  }
}
```

**The Fandaws adapter then becomes a consumer of `fnsr.claim.extracted` rather than a direct TagTeam client.** This is a small structural shift with large downstream payoff.

**Acceptance criterion to add:**

```
AC-5.17: FNSR Event Envelope
- GIVEN TagTeamAdapter.parse() produces a ParseResult
- WHEN emitted as a service event
- THEN the event conforms to CloudEvents v1.0
- AND type = "fnsr.claim.extracted"
- AND fnsr-taint, fnsr-confidence headers are present
- AND data payload contains all ParseResult fields
```

---

### ACTION 3: Design the Adapter as the HIRI Insertion Point

**Why:** When HIRI comes online, it needs to sit between TagTeam's output and Fandaws's consumption:

```
Current:   TagTeam → TagTeamAdapter → Fandaws pipeline
Future:    TagTeam → HIRI signing → TagTeamAdapter → Fandaws pipeline
```

**What to do:** Ensure the `TagTeamAdapter.parse()` method can accept a ParseResult with populated provenance fields without breaking. This is mostly a matter of ensuring the adapter doesn't reject or strip unknown fields.

**Acceptance criterion to add:**

```
AC-5.18: HIRI Integration Readiness
- GIVEN a ParseResult where:
  - fnsr:provenance = "hiri://sha256:mock-hash-for-testing"
  - fnsr:claimIRI = "hiri://sha256:mock-claim-iri"
  - fnsr:taintLevel = "L1"
- WHEN processed by TagTeamAdapter
- THEN ParseResult is accepted without error
- AND provenance fields are preserved through the Fandaws pipeline
- AND Fandaws stores the claim with its provenance metadata intact
```

This test costs almost nothing to write now. It's a forward-compatibility guarantee.

---

### ACTION 4: Add a Taint-Aware Confidence Floor for Knowledge Commitments

**Why:** AC-5.5 defines confidence propagation, and AC-5.14 handles negation. But there's a gap: what happens when a low-confidence claim reaches Fandaws? Currently, the pipeline routes by verb type regardless of confidence. A claim with 0.3 confidence and `verbType: "classification"` will create a knowledge commitment just like one with 0.95 confidence.

Fandaws should not commit low-confidence claims as knowledge without marking them appropriately. This connects to the taint architecture: an L2 claim with low confidence should be stored differently from an L2 claim with high confidence.

**What to do:** Define a confidence threshold below which Fandaws flags the claim rather than committing it as knowledge. The exact threshold is a Fandaws design decision, but the contract should make confidence *actionable*, not just informational.

**Acceptance criterion to add:**

```
AC-5.19: Confidence-Gated Knowledge Commitment
- GIVEN a ParseResult with fandaws:confidence < 0.5
- WHEN processed by Fandaws pipeline
- THEN the claim is stored with a provisional/tentative marker
- AND is NOT treated as committed knowledge for downstream reasoning
- AND can be promoted to committed knowledge upon human attestation (L1) or HIRI signing

- GIVEN a ParseResult with fandaws:confidence >= 0.5
- WHEN processed by Fandaws pipeline
- THEN the claim follows normal commitment workflow
```

---

## 5. What NOT to Change

To be explicit about scope — the following elements of your Phase 5 plan are correct and should not be modified:

- **VerbType classification rules** — the routing table is sound
- **Discourse annotation extraction** — speech act, modality, hedging are all needed downstream
- **Passive-voice resolution** — agent identification is correct
- **Copular-to-classification mapping** — CCO relation inference is aligned
- **Adapter capability reporting** — `isAvailable()` and `getCapabilities()` patterns are clean
- **Phase 5 exit criteria** — keep all existing criteria; the items above are *additions*, not replacements
- **Post-Phase 5 domain fine-tuning plan** — appropriate scoping as a separate work package

---

## 6. Summary of New Acceptance Criteria

| AC | Description | Effort | Risk if Skipped |
|----|-------------|--------|-----------------|
| AC-5.16 | Taint and provenance fields in ParseResult | Low | High — no HIRI insertion point; no taint propagation |
| AC-5.17 | CloudEvents `fnsr.claim.extracted` envelope | Medium | High — every future service must understand Fandaws internals |
| AC-5.18 | HIRI integration readiness test | Low | Medium — silent breakage when HIRI arrives |
| AC-5.19 | Confidence-gated knowledge commitment | Medium | Medium — low-confidence claims become false knowledge |

Total estimated additional effort: ~2-3 days of work across both teams. The cost of retrofitting these later, after Fandaws has stored thousands of provenance-less claims, is significantly higher.

---

## 7. Questions? Context?

If any of this is unclear or raises questions about the broader architecture:

- **FNSR Integration Spec v1.0** — defines CloudEvents contracts and event types for all services
- **HIRI Protocol Spec v2.1.0** — defines hash-IRI generation, Ed25519 signing, and manifest structure
- **Portfolio Planning v3.0** — the full phased roadmap showing where all 37 services connect
- **The Plot v0.1 §4** — the component map showing service dependencies

The epistemic loop (TagTeam → HIRI → Fandaws) is the foundation everything else builds on. Your Phase 5 work is building the first segment of that foundation. These four additions ensure the second segment (HIRI) can connect cleanly when it arrives, and that the third segment (Fandaws as persistent knowledge) inherits provenance from day one.

---

*Identity before address. Memory before reasoning.*

*And now: every fact gets a provenance anchor — even if that anchor is "not yet signed."*
