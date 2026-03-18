# Semantic Grounding: From Registry to HIRI

---

| Attribute | Value |
|-----------|-------|
| **From** | Aaron Damiano (Portfolio Lead) |
| **To** | Semantic Architecture Team |
| **Date** | March 3, 2026 |
| **Re** | Resource reallocation — HIRI and IPFS, not the Ontology Registry |
| **Priority** | Immediate |

---

## What You Got Right

Your Semantic Grounding Policy correctly identified a systemic problem that extends far beyond SAS. You wrote:

> *"As FNSR grows from 3 services to 15, the number of bridge ontologies grows combinatorially, and every one of them is maintained by social contract."*

The ecosystem actually has **37 services**, not 15. Your instinct about the Tower of Babel was even more urgent than you knew. The policy you wrote — every service declares its semantic grounding in the `@context` block, a certification step enforces term coverage, all bridges converge on BFO — is the correct policy. We are adopting it.

But we are building different infrastructure behind it.

---

## The Decision

We are not building the Ontology Registry as a standalone service. We are building **HIRI** and **HIRI IPFS**. Your team is being reallocated to this effort.

Here's why.

### What the Registry Provides

| Function | Mechanism |
|----------|-----------|
| Dereferenceable IRIs | Static file server at `registry.fnsr.dev` |
| Version management | Registry tracks versions, serves latest |
| Drift prevention | Certification step catches mismatches |
| Trust verification | Not addressed (you noted HIRI as optional enhancement) |
| Storage | Central server to maintain |

### What HIRI + IPFS Provides

| Function | Mechanism |
|----------|-----------|
| Dereferenceable IRIs | Content-addressed — the hash IS the definition |
| Version management | Immutable by construction — old versions never change because the content determines the address |
| Drift prevention | Impossible by design — if the definition changes, the address changes |
| Trust verification | Ed25519 signing built in |
| Storage | IPFS — decentralized, permanent, no single point of failure |

The Registry solves the coordination problem with a central authority you have to maintain. HIRI solves it by making the problem structurally impossible. You can't silently drift when the identifier is a hash of the content.

Your adapter certification function — the most valuable part of the Registry design — becomes a thin build-step check that queries HIRI-resolved definitions against the T-Box. It doesn't need its own service, its own domain, or its own team. It's a validation script that runs at publish time.

---

## What You Need to Know

Your policy document was written from the ECVE/SAS vantage point. Before you start building HIRI, you need the full map. Three things in particular:

### 1. The Ecosystem is 37 Services, Not 8

Your service inventory listed SAS, ECVE, Fandaws, BIBSS, SNP, CTS, NIS, and AVS. The actual ecosystem includes those plus TagTeam, HIRI, W2Fuel, MDRE, SIS, ECCPS, IEE, SHML, IRIS, OERS, AES, DES, CSS, APS, CPS, BAM, IS, SMS, SoMS, the FNSR Orchestrator, and all infrastructure services. Every one of them will emit JSON-LD. Every one of them needs semantic grounding. HIRI is the service that provides it for all 37, not just for ECVE/SAS.

I've attached the **FNSR Master Guide** and the **Portfolio Planning document** to this communication. Read both before you begin. The Master Guide gives you the narrative of what we're building and why. The Portfolio Planning document gives you the service inventory, dependency graph, phased roadmap, and critical path.

### 2. TagTeam Already Has a Working Bridge

TagTeam — our #1 priority service, 80% built — already has a `BridgeOntologyLoader` (Phase 6.5.4, 54 passing tests) that maps TagTeam values to IEE worldviews via `owl:sameAs` and `ethics:mapsToWorldview`. This is the same pattern you proposed in the policy document: the producing service declares its semantic grounding structurally. TagTeam is proof that the pattern works. Use it as reference architecture.

### 3. The Safety Floor Principle

CPS (Containment Protocol Service), BAM (Behavioral Alignment Monitor), and IS (Interpretability Service) are Tier 0 safety services. The Safety Floor Principle states: **safety infrastructure must never depend on services it constrains.** If CPS emits JSON-LD and its semantic grounding depends on HIRI, and CPS needs to contain HIRI if HIRI fails — that's a circular dependency.

Design for this from day one. Tier 0 safety services must be able to bundle their bridge context statically. Their bridge ontologies are still HIRI-addressed and certified, but the resolution doesn't depend on HIRI being operational. This is a firm architectural constraint.

---

## What You're Building

### Minimal Viable HIRI

The HIRI specification (v2.1.0) is comprehensive. You are not building all of it in Phase 1. You are building the core that satisfies your policy's requirements:

| Capability | HIRI Spec Reference | Your Policy Requirement It Satisfies |
|-----------|---------------------|--------------------------------------|
| **Hash-IRI generation** | Content-addressed identifier from JSON-LD content | Dereferenceable IRIs (§3.2) |
| **Resolution manifests** | Dereference a HIRI → get semantic definition, provenance, signature | Context document hosting (§4.1) |
| **Ed25519 signing** | Cryptographic trust verification | Trust verification (not addressed in Registry, now built-in) |
| **IPFS publication** | Store manifests on IPFS, permanently dereferenceable | Storage without central server dependency |

What you are NOT building in Phase 1: recursive SNARK chain compaction, privacy credentials, materialized entailment. Those come later.

### The Connection to Your Policy

Your policy document is not discarded. It becomes the **requirements specification** for HIRI's resolution manifest design. Every requirement you wrote maps to a HIRI deliverable:

| Your Policy Requirement | HIRI Deliverable |
|------------------------|------------------|
| Every service declares its grounding in `@context` | Services reference HIRI-addressed bridge contexts in `@context` |
| Bridge contexts are served at stable, versioned URIs | HIRI resolution manifests on IPFS — content-addressed, immutable, permanently dereferenceable |
| Certification verifies term coverage | Build-step check: every emitted term has a valid HIRI resolving to a BFO-grounded definition |
| Version drift detection | Content-addressed: if the definition changes, the address changes — drift is structurally impossible |
| Shared BFO/CCO upper ontology | HIRI manifests include `owl:equivalentClass` declarations grounding terms in BFO/CCO |

### The FBO Bridge Ontology Becomes the First Resolution Manifest

You already have the FBO Bridge Ontology — 35 terms fully mapped to BFO/STATO/IAO/CCO. That TTL file is 90% of the way to a HIRI resolution manifest. The remaining work:

1. Serialize FBO as JSON-LD (from your existing TTL)
2. Generate a HIRI (content hash) for the JSON-LD
3. Sign it with Ed25519
4. Publish to IPFS
5. Reference the HIRI in SAS's `@context` block

The SAS v2.2 `@context` amendment you proposed still happens. One string changes — instead of `https://registry.fnsr.dev/contexts/fbo/v1`, it's a HIRI address that resolves through IPFS to the same semantic content. Zero runtime cost. Self-describing output. Immutable by construction.

---

## Your Team's Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Read the Master Guide and Portfolio Planning document** | Understand the full 37-service ecosystem, the critical path, and where HIRI sits |
| 2 | **Read the HIRI specification v2.1.0** | Focus on: Hash-IRI generation, resolution manifests, Ed25519 signing. Defer: chain compaction, privacy credentials, materialized entailment |
| 3 | **Read the HIRI IPFS specification v3.0.0** | Understand the IPFS storage and resolution layer |
| 4 | **Prototype: FBO → HIRI resolution manifest** | Take the existing FBO Bridge Ontology, serialize as JSON-LD, generate a HIRI, sign it, publish to local IPFS |
| 5 | **Prototype: SAS `@context` with HIRI** | SAS v2.2 amendment with HIRI-addressed FBO context instead of Registry URI |
| 6 | **Design: Safety Floor carve-out** | How Tier 0 services bundle bridge contexts statically without runtime HIRI dependency |
| 7 | **Design: Build-step certification** | A validation script that replaces the Registry's adapter certification: verify every emitted term has a valid HIRI resolving to BFO-grounded definition |

Deliverables 4 and 5 are the proof point. If FBO works as a HIRI resolution manifest and SAS can reference it in `@context`, the pattern is validated for all 37 services.

---

## What This Means for Your Policy Document

Your Semantic Grounding Policy is adopted with one change: replace "Ontology Registry Service" with "HIRI + IPFS" as the infrastructure layer. The consumer-side policy — every service MUST declare its semantic grounding in `@context`, all bridges MUST ground in BFO/CCO, certification MUST verify term coverage — is unchanged. That's the policy. HIRI is the infrastructure that makes it permanent.

You designed the right contract. Now build the right infrastructure behind it.

---

## Attachments

- FNSR Master Guide (`docs/00-foundation/FNSR-Master-Guide.md`)
- Portfolio Planning Document v3.1 (`docs/00-foundation/Portfolio Planning.md`)
- HIRI Protocol Specification v2.1.0
- HIRI IPFS Specification v3.0.0
- TagTeam Roadmap — see Phase 6.5.4 (BridgeOntologyLoader)

---

*Identity before address. Memory before reasoning. And now: structural grounding before social contracts.*
