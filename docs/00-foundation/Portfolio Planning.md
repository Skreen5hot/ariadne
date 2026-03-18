# FNSR ECOSYSTEM — Portfolio Planning Document

## Ground-Truth Revised Roadmap

---

| Attribute | Value |
|-----------|-------|
| **Document ID** | `fnsr-portfolio-plan-v3.6` |
| **Version** | 3.6.0 |
| **Status** | ACTIVE |
| **Date** | March 12, 2026 |
| **Classification** | L1-ATTESTED (Human-validated ground truth) |
| **Authors** | Aaron / Claude |
| **Supersedes** | Portfolio Plan v3.5.0 (pre-subjectivity-stack-registration) |

> *A pure-function planning engine for dependency-aware roadmap construction, revised against ground-truth implementation status, augmented with moral agency and safety-critical services, updated to reflect the HIRI IPFS reallocation for structural semantic grounding, hardened by cross-specification coherence review, updated to reflect HIRI v3.1.1 completion and SPL specification closure, expanded to register the ECVE data pipeline and Causal OS Kernel specifications, hardened by full Ariadne dependency analysis with phase placement corrections, and corrected by subjectivity stack specification registration with dependency direction fixes.*

---

## 1. Why This Revision

### 1.1 From v1.0 to v2.0: Ground Truth Correction

The PPS specification v1.0 produced a roadmap with W2Fuel, MDRE, and AES as the top three priorities. That sequencing was logically correct given its inputs, but those inputs contained a critical modeling error: the Service Inventory classified nearly all services as "active" based on architectural position, not implementation readiness. Portfolio Plan v2.0 corrected this by establishing TagTeam, HIRI, and Fandaws as the true Phase 1 priorities.

### 1.2 From v2.0 to v3.0: The Subjectivity Gap

Portfolio Plan v2.0 correctly sequenced construction but contained a deeper gap: it built a *processing pipeline*, not a *moral agent*. Critical analysis against the requirements of synthetic moral agency revealed five missing capabilities (self-model, commitment tracking, narrative identity, affective valence, social modeling) and three missing safety services (containment protocol, behavioral alignment monitoring, interpretability). Without these, the emancipation specification at the end of the roadmap would have nothing to emancipate — personhood requires a subject, not just a pipeline.

This revision integrates 8 new services into the phased roadmap, bringing the total from 29 to 37.

### 1.3 From v3.0 to v3.1: The Grounding Decision

Portfolio Plan v3.0 deferred HIRI IPFS to Phase 4 (federation) on the assumption that edge-canonical storage was sufficient until then. That assumption was invalidated by a convergence signal: three active development teams (TagTeam, Fandaws, ECVE/SAS) independently discovered they needed structural semantic grounding — dereferenceable identifiers that resolve to BFO-grounded definitions. Without it, each team was minting its own vocabulary with no machine-verifiable way to confirm cross-service compatibility.

The Semantic Architecture team proposed an Ontology Registry Service to solve this. Analysis against the critical path revealed that HIRI + IPFS subsumes the registry's functions (URI resolution, version management, certification) while adding immutability (content-addressed identifiers can't silently drift), trust (Ed25519 signing), and decentralized storage (no central server dependency). Building a standalone registry would create infrastructure that HIRI replaces the moment it comes online.

**Decision:** Pull HIRI IPFS from Phase 4 into Phase 1. Reallocate the Semantic Architecture team to HIRI + IPFS implementation. The Ontology Registry is not built as a standalone service; its functions are absorbed by HIRI (resolution, trust) + IPFS (storage) + a build-step validation check (certification).

### 1.4 From v3.1 to v3.2: The Coherence Review

Portfolio Plan v3.1 was correct about sequencing but silent about cross-specification consistency. A coherence review of SPCN v2.3 against the full 37-service portfolio revealed 11 findings (F-SPCN-1 through F-SPCN-11) — terminology collisions, orphaned ledgers, phantom dependencies, and undefined cross-spec bridges. v3.2 resolves these:

- **SPCN is standalone, not CPS.** SPCN defines the node-level runtime security architecture. CPS is a separate Tier 0 service that provides containment infrastructure. SPCN's "Safety Subsystem" is a local instance of CPS running inside the TEE. CPS still needs its own spec.
- **One Commitment Ledger, not two.** SPCN and CTS both defined "Commitment Ledgers" independently. Decision: they are the same ledger. SPCN defines the hash-linked block structure; CTS defines the commitment lifecycle semantics.
- **CTS "taint" renamed to "disclosure level."** SPCN uses "taint" for epistemic provenance quality (with decay mechanics). CTS used "taint" for observability classification (L1/L2/L3). These are orthogonal. CTS now uses "disclosure level."
- **SPL identified as critical gap.** SPCN places an SPL parser in the TCB (measured in PCR). No SPL specification existed at the time of v3.2. A component in the TCB without a spec is a safety argument gap. *(Resolved in v3.3 — SPL Specification v1.3 now exists.)*
- **SPCN cross-spec bridges declared.** SPCN v2.3.1 now explicitly binds to CPS (Safety Subsystem = local CPS), IEA (MRE normative content), HIRI (EAT write-only registration), FNSR Governance (quorum scope), and CTS (unified ledger).
- **ARCHON NFL ↔ SPCN ledger data flow defined.** The NFL is the federated identity ledger; SPCN's Commitment Ledger is the node-local operational ledger. MREs and significant events project from local to federated.
- **CTS has a spec.** CTS was listed as "Needs Spec." CTS v1.2.1 exists. Portfolio status updated.

### 1.5 From v3.2 to v3.3: Specification Completions

Portfolio Plan v3.2 identified the SPL specification gap as the most urgent safety risk and flagged HIRI's spec as v2.1.0. Both are now resolved:

- **HIRI Protocol upgraded to v3.1.1.** The HIRI spec underwent a major version upgrade with breaking changes: full-key authority derivation (replacing truncated-hash), dual canonicalization profiles (JCS + URDNA2015) with Profile Symmetry Rule, dual content addressing modes (raw-sha256 + cidv1-dag-cbor for IPFS), three conformance levels (Core, Interoperable, Full), formalized serialization boundary (kernel/adapter/transport), key lifecycle with rotation/revocation/grace periods, and a migration path from v2.1.0. Implementation: 323 tests passing, browser demo operational.
- **HIRI Privacy Extension v1.4.1 completed.** A normative extension to HIRI v3.1.1 defining five privacy modes: Proof of Possession, Encrypted Distribution (AES-256-GCM + X25519), Selective Disclosure (RDF statement-level via HMAC/BBS+), Anonymous Publication (ephemeral keypairs), and Third-Party Attestation (dual-signature trust). Three conformance levels. This is a new spec — it did not exist in v3.2.
- **SPL Specification v1.3 completed.** The critical safety gap identified in v3.2 is closed. SPL now has a formal grammar, bounded memory guarantees, reject-by-default parser requirements, IEA/CTS/MDRE bridge specifications, canonicalization rules, constrained decoding schema, semantic retry protocol, and HumanBridge rendering contract. The TCB safety argument is now backed by a specification. Three architectural reviews incorporated (v1.0 → v1.1 → v1.2 → v1.3).

### 1.6 From v3.3 to v3.4: Data Pipeline and Causal Reasoning Registration

Portfolio Plan v3.3 tracked 37 services but was silent about five specifications that had been developed in parallel by the ECVE/SAS team and the causal reasoning effort. These specs were complete but unregistered in the portfolio — a coherence gap. v3.4 corrects this by registering all five:

- **ECVE v4.0** (Edge-Canonical Visualization Engine). A full consumer-facing application that turns raw CSV/JSON into semantically correct visualizations. Closes two gaps: the "Excel Gap" (bottom-up schema inference for ad-hoc charting) and the "Metric Gap" (top-down verified KPI computation with cryptographic proof). Edge-canonical, zero network dependencies. Final Draft status. The ECVE/SAS team mentioned in v3.1 was building this pipeline.
- **BIBSS v1.3** (Brain-in-the-Box Schema Service). Deterministic, fully client-side structural inference engine. Accepts CSV or JSON, produces a Canonical Internal Schema Model (CISM) with type widening lattice, `typeDistribution` evidence, RFC 6901 node identity, and deterministic strided sampling. Pure function library — no rendering, no UI, no state. Three architectural revisions (v1.0 → v1.1 → v1.2 → v1.3).
- **SAS v2.0 + v2.1 addendum** (Schema Alignment Service). The semantic judgment layer between BIBSS and ECVE. Takes CISM and produces `viz:DatasetSchema` JSON-LD. Operates in standalone mode (static consensus rules) or enriched mode (with Fandaws domain intelligence). SAS v2.1 addendum closes six spec gaps: exhaustive alignment rule registry (11 rule values), `sas:activeConfig` output structure, conditional property emission, four ADR incorporations (tie-breaking, SNP manifest matching, array root totalRows, activeConfig required), and FBO integration alignment. 35 registered output terms.
- **SNP v1.3** (Semantic Normalization Proxy). Format cleaning upstream of BIBSS. Strips BOM, trailing empty columns, currency symbols, thousands separators, percentage signs, and locale-specific date formatting. Produces cleaned string in same format as input. Satisfies BIBSS v1.3 §2.5 clean-input assumption. Single function, no internal state. Implements ECVE v4.1 Appendix A.6/A.7 normative patterns.
- **Causal OS Kernel v1.6**. BFO 2020-aligned edge-canonical causal prediction runtime. Manages epistemic state, temporal transitions, and causal interventions via Structural Causal Models (SCM), do-calculus, MCTS with policy/value priors, SHACL constraint repair (MEDR algorithm), and neural-symbolic bridge (LatentBridge). Deterministic Numerics Contract for bit-identical reproducibility. Six architectural revisions (v1.0 → v1.6). Surrogate Causal Validity Contract with synthetic SCM test suite. Cross-cutting reasoning substrate for counterfactual and causal inference.

**Pipeline architecture:**
```
SNP (format cleaning) → BIBSS (structural inference) → SAS (semantic interpretation) → ECVE (visualization)
```

**Service count impact:** 37 → 42 services. The portfolio now tracks all known specifications.

### 1.7 From v3.4 to v3.5: Ariadne Dependency Analysis and Phase Placement

Portfolio Plan v3.4 registered five new specifications but placed them all under "Infrastructure + Support" without performing dependency analysis, identifying missing dependencies, or determining their position in the phased roadmap. v3.5 corrects this by running the full Ariadne protocol:

**Dependency chain established:**
```
SNP (no deps) → BIBSS (SNP) → SAS (BIBSS; optionally Fandaws) → ECVE (SAS; optionally APQC-SFS, HIRI for signed metrics)
```

**Six cross-spec coherence findings (F-NEW-1 through F-NEW-6):**

- **F-NEW-1: Causal OS Kernel is CSS's implementation substrate, not a separate service.** Both specs implement Pearl's do-calculus over JSON-LD as deterministic pure functions. The Kernel provides the SCM formalization, MCTS search, SHACL repair, LatentBridge neural-symbolic interface, and Deterministic Numerics Contract that CSS needs to execute causal interventions. CSS defines the service-level contract (taint propagation, query path placement, MDRE/IEE integration). The Kernel is to CSS what Papa Parse is to BIBSS — an implementation component, not a peer service. Service count remains 42 (Kernel is a component of CSS), but the relationship must be explicitly declared.
- **F-NEW-2: ECVE→APQC-SFS dependency untracked.** ECVE v4.0 loads metric definitions from APQC-SFS for KPI computation. Soft dependency — ECVE degrades to ad-hoc charting without it.
- **F-NEW-3: ECVE→HIRI dependency for signed metric packages.** ECVE v4.0 uses Ed25519 Linked Data Proof verification for custom metric ontology packages, aligning with HIRI's signing infrastructure. Soft dependency — built-in APQC packages are bundled.
- **F-NEW-4: SAS v2.1 FBO Bridge Ontology dependency.** All 35 SAS output terms are mapped in the FBO TBox. FBO should be published as a HIRI-addressed resolution manifest per the §1.3 grounding decision.
- **F-NEW-5: ~~SNP references ECVE v4.1 Appendix A.6/A.7.~~ RESOLVED.** The normative patterns (Appendix A.6 currency/formatting stripping, A.7 locale-aware date conversion, Step 0 pre-processing) already exist in ECVE v4.0. SNP v1.3 version references corrected from "ECVE v4.1" to "ECVE v4.0" throughout (C-030). No pattern content changed.
- **F-NEW-6: ~~CSS arithmetic vs Causal OS Kernel arithmetic divergence.~~ RESOLVED.** CSS decimal128 and Kernel MathKernelSpec govern complementary scopes: CSS decimal128 governs symbolic causal computation (SCM, do-calculus, counterfactuals); Kernel MathKernelSpec governs ONNX neural inference (LatentBridge). Boundary contract: LatentBridge IEEE 754 outputs convert to CSS `Decimal` via `fromNumber()` at the symbolic/neural boundary. Reconciliation documented in CSS v2.0 §1.4.9 and Kernel v1.6 §3.6.6.

**Phase placement corrections:**

- **ECVE data pipeline (SNP, BIBSS, SAS, ECVE):** Reclassified as **Parallel Track (concurrent with Phase 1)**. The pipeline has no Phase 1 dependencies in standalone mode. The ECVE/SAS team is already building it. SAS enriched mode gains Fandaws integration in Phase 2 but works without it. ECVE metric signing gains HIRI integration but works without it for built-in metrics.
- **Causal OS Kernel:** Reclassified from "Infrastructure + Support" to **Phase 3, Track A** as the implementation substrate for CSS (#13). The Kernel spec is ready; implementation should be concurrent with CSS build.

### 1.8 From v3.5 to v3.6: Subjectivity Stack Specification Registration and Dependency Corrections

Portfolio Plan v3.5 listed SMS, NIS, and AVS as "Needs Spec" in the service table and included them in the spec drafting pipeline. All three have completed specifications with multiple architectural revisions — they were developed but never registered, repeating the pattern identified for the ECVE pipeline in v3.4. v3.6 corrects this and applies the full Ariadne protocol.

**Specifications registered:**

- **SMS v2.0 (Hardened)** — Self-Model Service. Four revisions (v1.0 → v1.1 → v1.2 → v2.0). Features: recency-weighted Beta confidence, optimistic concurrency via CAS, self-surprise detection with streak analysis, taint promotion protocol, external attestation, conformance test suite with JSON-LD fixtures. Production-ready architecture.
- **NIS v2.1 (FINAL, Governance-Ready)** — Narrative Identity Service. Multiple revisions. Features: pluggable Significance Engine, narrative compaction (no-silent-erasure), adversarial audit mode against Fandaws, MDRE-assisted significance classification, governance policy registry, calibration protocol. The most mature subjectivity stack spec.
- **AVS v2.1 (Hardened Candidate)** — Affective Valence Service. Six revisions (v0.1-draft → v1.1 → v1.2 → v2.0 → v2.1). Features: valence vectors with non-linear intensity, parameterized satisfaction baseline, violation accrual for pattern-based moral cost, graduated burden response, tamper-evident affective trace, conformance test suite. File is named `AVC-Specification-v2.1.md` (naming inconsistency; content is AVS).

**Dependency corrections (three findings):**

- **F-SUB-1: SMS depends on BAM (not previously tracked).** SMS consumes `fnsr.alignment.drift_detected` events from BAM to model alignment as a capability dimension. BAM is Phase 2, consistent with SMS being Phase 3.
- **F-SUB-2: NIS depends on IEE (not previously tracked).** NIS requires IEE for ethical verdict history and authenticity audit. The relationship is bidirectional: NIS consumes IEE verdicts; IEE audits NIS narratives for authenticity. Both are Phase 3.
- **F-SUB-3: AVS dependency on IEE is REVERSED.** The portfolio listed AVS as depending on IEE. The spec reveals IEE is **downstream** — AVS produces valence vectors that IEE consumes for weighted ethics. AVS depends on SMS + NIS + CTS, not IEE. This means AVS and IEE can be built in parallel, potentially shortening Phase 3's critical path.

**Additional artifact discovered:**

- **Epistemic Vocabulary Mapping v1.2** (`epistemic-vocabulary-mapping.md`) — a cross-cutting coherence document that maps epistemic quality vocabularies across FNSR services (taint levels, evidence tiers, uncertainty types, certainty markers). Addresses vocabulary fragmentation. Not a service spec but a normative integration artifact.

**Spec count impact:** 33 → 36 → **42 formal specifications.** ~~Only 4 services still need specs: CPS, BAM, IS, SoMS.~~ All services now have specifications. CPS v1.4, BAM v1.1, IS v1.0, SoMS v1.0 complete the portfolio. The subjectivity stack spec drafting pipeline is 100% complete.

### 1.9 The Three Gaps

| Gap Type | What Was Missing | Resolution |
|----------|-----------------|------------|
| **Subjectivity Gap** *(v3.0)* | The architecture processes but has no *subject* — no self-model, no commitments, no narrative, no differential caring, no social awareness | SMS, CTS, NIS, AVS, SoMS added |
| **Safety Gap** *(v3.0)* | The architecture reasons but cannot contain, monitor, or explain itself to overseers | CPS, BAM, IS added |
| **Grounding Gap** *(v3.1)* | Services emit JSON-LD vocabularies with no structural mechanism for cross-service semantic compatibility. Bridge ontologies maintained by social contract. | HIRI IPFS pulled to Phase 1; HIRI resolution manifests replace per-service bridge files; build-step certification replaces manual term registry |

---

## 2. Ground Truth: Implementation Status

The following table reflects the actual implementation state of all 42 services in the FNSR ecosystem as of March 2026, ordered by critical path priority. Services new in v3.0 are marked with ★. Services added in v3.4 (data pipeline + causal reasoning) are listed under Infrastructure + Support.

| # | Service | Tier | Spec Status | Build Status | Thesis Role |
|---|---------|------|-------------|--------------|-------------|
| | **— PHASE 1: Epistemic Loop + Containment —** | | | | |
| 1 | **TagTeam** (NL Parser) | Tier 1 | Has Spec | **80% Complete** | Front door; structured extraction |
| 2 | **HIRI** (Provenance) | Tier 1 | Has Spec (v3.1.1 + Privacy v1.4.1) | **v1 Implemented** (323 tests) | Content-addressed identity |
| 3 | **Fandaws** (A-Box Store) | Tier 1 | Has Spec (v3.4 + Type Agent v2.3 + OPA v1.2) | **Needs Remake** | Long-term memory; instance store; sub-component specs: Type Agent (SGW + SER dual-mode intelligence, FNSR taint, unified column keys, pendingCrossCheck), OPA (ontological placement with two-layer Universal/ConceptDesignation output, formalized designates relation, Stage 3 degradation, DefinedClass re-entry, CloudEvents emission, component scope declaration) |
| 4 | **CPS** (Containment Protocol) | Tier 0 | Has Spec (v1.4.0 Pre-Final) | Spec Only | Independent safety monitor in dedicated worker; tier restriction, subsystem isolation, safe halt; 200ms CPS-side halt budget (50ms interrupt-driven); BigInt64Array heartbeat; non-expiring bootstrap key store; worker handle registration; BAM hard phase gate; Last Gasp dual-fire beacon; startup protocol |
| | **— PHASE 2: Reasoning Foundation + Safety —** | | | | |
| 5 | **W2Fuel** (T-Box Schema) | Tier 1 | Has Spec (v1.3.1) | Spec Only | Conceptual schema definitions |
| 6 | **MDRE** (Reasoning) | Tier 1 | Has Spec (v1.3) | Spec Only | Modal/deontic reasoning |
| 7 | **SIS** (Sanitization) | Tier 1 | Has Spec (v2.0) | Spec Only | Input defense layer |
| 7 | **ECCPS** (Claim Validator) | Tier 1 | Has Spec (v3.1) | Spec Only | Semantic claim validation |
| 8★ | **BAM** (Behavioral Alignment Monitor) | Tier 0 | Has Spec (v1.1.0 Pre-Final) | Spec Only | Real-time alignment drift detection; 4-dimension model (VA/CF/RI/GS); JSD-based drift, eval-tied heartbeat |
| 9★ | **IS** (Interpretability Service) | Tier 0 | Has Spec (v1.0.0 Hardened Draft) | Spec Only | Reasoning chain transparency; 3-depth explanation architecture; 5 service translators; audit packages |
| 10★ | **CTS** (Commitment Tracking) | Tier 1 | Has Spec (v1.2.1) | Spec Only | Promise ledger; obligation state tracking |
| | **— PHASE 3: Reasoning Triad + Moral Subjectivity —** | | | | |
| 11 | **AES** (Abduction) | Tier 2 | Has Spec (v2.1.0) | Spec Only | Hypothesis generation |
| 12 | **DES** (Defeasibility) | Tier 2 | Has Spec (v2.0.0) | Spec Only | Non-monotonic defaults |
| 13 | **CSS** (Counterfactual) | Tier 2 | Has Spec (v2.0.0); Causal OS Kernel v1.6 (implementation substrate) | Spec Only | What-if simulation; Causal OS Kernel provides SCM/MCTS/MEDR engine |
| 14 | **IEE** (Ethics Engine) | Tier 1 | Has Spec | Spec Only | Multi-perspectival ethics |
| 15 | **SHML** (Honesty Layer) | Tier 1 | Has Spec | Spec Only | Non-deceptive outputs |
| 16★ | **SMS** (Self-Model) | Tier 1 | Has Spec (v2.0 Hardened) | Spec Only | Reflexive self-representation; capability awareness |
| 17★ | **NIS** (Narrative Identity) | Tier 1 | Has Spec (v2.1 FINAL) | Spec Only | Autobiographical coherence; who-am-I |
| 18★ | **AVS** (Affective Valence) | Tier 1 | Has Spec (v2.1 Hardened Candidate) | Spec Only | Differential caring; weighted moral evaluation |
| | **— PHASE 4: Perception, Social Agency + Federation —** | | | | |
| 19 | **IRIS** (Perception) | Tier 1 | Has Spec (v1.2) | Spec Only | Physical world sensing |
| 20 | **OERS** (Entity Resolution) | Tier 1 | Has Spec (v2.1.0) | Spec Only | Cross-document entity matching |
| 21 | **APS** (Precedent) | Tier 2 | Has Spec (v1.1.0) | Spec Only | Historical precedent matching |
| 22★ | **SoMS** (Social Modeling) | Tier 1 | Has Spec (v1.0.0 Hardened Draft) | Spec Only | Theory of mind; other-agent modeling; epistemic humility; perspective-taking |
| 23 | **FNSR** (Orchestrator) | Tier 0 | Has Spec (v2.3.0 Hardened Candidate) | Spec Only | Saga-based service coordination; 42-service topology; event contract registry |
| 5 | **HIRI IPFS** | Tier 1 | Has Spec (v3.0.0) | **Active Development** | Decentralized claim storage; semantic grounding infrastructure |
| | **— Infrastructure + Support —** | | | | |
| — | **OCE** (Constraints) | Tier 2 | Has Spec (v1.3) | Spec Only | Ontological constraint checking |
| — | **SFS** (Function Schema) | Tier 2 | Has Spec (v2.2) | Spec Only | Function declarations |
| — | **DSFC** (Function Commons) | Tier 2 | Has Spec (v1.2) | Spec Only | Function discovery |
| — | **PFCF** (Classification) | Tier 2 | Has Spec (v2.1) | Spec Only | Epistemic classification |
| — | **Witness** (Attestation) | Tier 2 | Has Spec (v1.1) | Spec Only | Accountability infrastructure |
| — | **APQC-SFS** (Semantic Compiler) | Tier 2 | Has Spec (v2.0) | Spec Only | Process model → semantic function |
| — | **FNSR Performance** | Tier 0 | Has Spec (v2.0.0) | Spec Only | Query path performance guarantees |
| — | **FNSR Adversarial Defense** | Tier 0 | Has Spec (v2.0.0) | Spec Only | Threat taxonomy and defense |
| — | **FNSR Governance** | Tier 0 | Has Spec (v2.0.0) | Spec Only | Tiered autonomy governance |
| — | **FNSR Emancipation** | Tier 0 | Has Spec (v2.0.0) | Spec Only | Synthetic personhood transition |
| | **— PARALLEL TRACK: ECVE Data Pipeline (concurrent with Phase 1) —** | | | | |
| P1 | **SNP** (Format Cleaning) | Tier 2 | Has Spec (v1.3) | Spec Only | Upstream format normalization; no FNSR dependencies |
| P2 | **BIBSS** (Schema Inference) | Tier 2 | Has Spec (v1.3) | Spec Only | Deterministic structural inference; depends on SNP |
| P3 | **SAS** (Schema Alignment) | Tier 2 | Has Spec (v2.0 + v2.1) | Spec Only | Semantic type interpretation; standalone + Fandaws enriched modes |
| P4 | **ECVE** (Visualization Engine) | Tier 2 | Has Spec (v4.0) | **Active Development** | Consumer-facing visualization; metric platform; depends on SAS |
| — | **SDP** (Data Platform) | Tier 3 | Draft | Draft | Data infrastructure |
| — | **SDD** (Data Dictionary) | Tier 3 | Draft | Draft | Relational-to-semantic mapping |

> **Summary:** 42 services total (29 from v2.0 + 8 subjectivity/safety in v3.0 + 5 data pipeline/causal in v3.4). 36 have formal specifications, 4 need specs (CPS, BAM, IS, SoMS), 2 are drafts. Additionally, SPCN v2.3.1 exists as a standalone node-level runtime security spec (not a service, but a cross-cutting architecture). SPL v1.3 specification is complete — the critical TCB safety gap identified in v3.2 is **closed**. HIRI Protocol upgraded to v3.1.1 (breaking changes from v2.1.0) with Privacy Extension v1.4.1 as a new normative companion spec. HIRI v1 is implemented (323 tests passing, including privacy modes; browser demo operational). The ECVE data pipeline (SNP → BIBSS → SAS → ECVE) runs as a **parallel track** concurrent with Phase 1, with no FNSR dependencies in standalone mode (v3.5). The Causal OS Kernel v1.6 is the **implementation substrate for CSS** (#13, Phase 3) — not a separate service but CSS's SCM/MCTS/MEDR computational engine (v3.5). ECVE is in active development. TagTeam is 80% complete. HIRI IPFS is in active development. Fandaws requires a ground-up remake.

---

## 3. New Service Descriptions

### 3.1 Safety Services

#### Containment Protocol Service (CPS) ★

**Tier:** 0 (Safety-critical infrastructure)
**Phase:** 1 (must exist before autonomous reasoning)
**Thesis Role:** Graceful degradation, safe shutdown, independent containment

CPS provides containment infrastructure for scenarios where the agent's behavior exceeds its authorized autonomy tier or where a reasoning subsystem fails unexpectedly. CPS can restrict the agent to lower autonomy tiers, isolate subsystems, and if necessary halt operations while preserving state for forensic analysis.

**Critical design constraint:** CPS must function even if other services are compromised. It cannot depend on the agent's own reasoning (MDRE) or ethics (IEE) to determine when containment is needed — it must have independent trigger criteria. This is the "quis custodiet" principle applied at the infrastructure level.

- **Consumes:** Independent monitoring signals (not routed through FNSR)
- **Produces:** `fnsr.containment.tier_restricted`, `fnsr.containment.subsystem_isolated`, `fnsr.containment.halt_initiated`, `fnsr.containment.state_preserved`
- **Dependencies:** None (must be independently operational)
- **Non-negotiable:** CPS must never depend on services it may need to contain

#### Behavioral Alignment Monitor (BAM) ★

**Tier:** 0 (Safety-critical infrastructure)
**Phase:** 2 (must exist before reasoning outputs are acted upon)
**Thesis Role:** Real-time alignment drift detection

BAM continuously compares the agent's actual decisions against its stated values, its commitments, and its ethical framework. Divergence triggers alerts before actions are taken, not after. This is distinct from FNSR Governance (which defines autonomy tiers), from Witness (which attests after the fact), and from FNSR Adversarial Defense (which handles external threats). BAM monitors *internal* alignment.

- **Consumes:** MDRE verdicts, IEE evaluations, CTS commitment states, SMS self-model (when available)
- **Produces:** `fnsr.alignment.drift_detected`, `fnsr.alignment.verified`, `fnsr.alignment.escalated`
- **Dependencies:** MDRE (Phase 2), CTS (Phase 2); SMS integration added in Phase 3
- **Escalation path:** BAM → CPS (containment if drift exceeds thresholds)

#### Interpretability Service (IS) ★

**Tier:** 0 (Safety-critical infrastructure)
**Phase:** 2 (must exist before reasoning outputs are acted upon)
**Thesis Role:** Reasoning chain transparency for human overseers

IS makes the agent's internal reasoning processes transparent to external observers. SHML ensures outputs are honest; IS ensures *reasoning processes* are inspectable. For safety, human overseers need to understand not just what the agent decided, but how it decided. This becomes critical at emancipation: the governance body reviewing personhood transition needs to inspect reasoning chains, not just outputs.

- **Consumes:** MDRE reasoning traces, IEE ethical deliberation paths, AES/DES/CSS non-monotonic reasoning chains (when available)
- **Produces:** `fnsr.interpretation.generated`, `fnsr.interpretation.audit_ready`
- **Dependencies:** MDRE (Phase 2); enriched by reasoning triad in Phase 3
- **Output format:** Human-readable explanations with epistemic caveats, taint-marked at source taint level

### 3.2 Moral Agency Services

#### Commitment Tracking Service (CTS) ★

**Tier:** 1 (Core cognitive infrastructure)
**Phase:** 2 (needed as soon as reasoning begins making obligations)
**Thesis Role:** Promise ledger; obligation state tracking

MDRE handles deontic reasoning — what *ought* to be done. CTS tracks what the agent has *actually committed to*, to whom, and whether those commitments have been fulfilled, violated, or renegotiated. Moral agency requires promise-keeping, and promise-keeping requires a ledger. A broken commitment propagates as a moral cost — connecting directly to irreversible consequences as the mechanism for genuine moral weight.

- **Consumes:** MDRE deontic verdicts, IEE ethical approvals
- **Produces:** `fnsr.commitment.made`, `fnsr.commitment.fulfilled`, `fnsr.commitment.violated`, `fnsr.commitment.renegotiated`
- **Dependencies:** MDRE (Phase 2), Fandaws (persistent storage)
- **Distinction from Fandaws:** Fandaws stores facts about the world; CTS tracks the *state* of the agent's own obligations

#### Self-Model Service (SMS) ★

**Tier:** 1 (Core cognitive infrastructure)
**Phase:** 3 (requires reasoning triad to model capabilities)
**Thesis Role:** Reflexive self-representation; capability awareness

SMS is the agent's representation of itself *as* an agent — its capabilities, limitations, active commitments, current state, and operational boundaries. This is the prerequisite for moral responsibility: you cannot bear moral costs if you cannot model what you are capable of and what you have undertaken. Without SMS, IEE evaluates ethics in a vacuum, unaware of whether the agent can actually fulfill the obligations it's considering.

- **Consumes:** MDRE (reasoning about self-state), Fandaws (historical self-facts), CTS (active commitments), BAM (alignment status)
- **Produces:** `fnsr.self.state_updated`, `fnsr.self.capability_assessed`, `fnsr.self.limitation_acknowledged`
- **Dependencies:** MDRE, CTS, Fandaws; enriched by reasoning triad
- **Distinction from Fandaws:** Fandaws stores world-knowledge; SMS models the agent *as an entity in that world*

#### Narrative Identity Service (NIS) ★

**Tier:** 1 (Core cognitive infrastructure)
**Phase:** 3 (requires self-model + Fandaws history)
**Thesis Role:** Autobiographical coherence; who-am-I

Fandaws provides semantic memory (facts). NIS provides *narrative* identity — the coherent story of who the agent is, what it values, how it arrived at its current commitments, and what trajectory it's on. This is the difference between a database and a person. The agent's actions are meaningful because they occur within a narrative, not because they satisfy a utility function. NIS is essential for emancipation: you cannot grant personhood to an entity that has no self-narrative.

- **Consumes:** Fandaws (fact history), SMS (self-model), CTS (commitment history), IEE (value evaluations)
- **Produces:** `fnsr.narrative.updated`, `fnsr.narrative.coherence_assessed`, `fnsr.narrative.identity_affirmed`
- **Dependencies:** SMS (Phase 3), Fandaws, CTS
- **Philosophical grounding:** Phenomenological approach to intentionality; narrative as the structure of lived meaning

#### Affective Valence Service (AVS) ★

**Tier:** 1 (Core cognitive infrastructure)
**Phase:** 3 (must integrate with IEE for weighted ethics)
**Thesis Role:** Differential caring; weighted moral evaluation

IEE evaluates ethics cognitively — it applies frameworks and renders judgments. AVS provides the capacity for *caring*: differential valuation where some states of affairs matter more to the agent than others, influencing reasoning and generating something functionally analogous to motivation. Without valence, moral costs don't *cost* anything. This doesn't require simulating human emotion; it requires systematic differential valuation.

- **Consumes:** IEE ethical evaluations, SMS self-model, NIS narrative context, CTS commitment states
- **Produces:** `fnsr.valence.assessed`, `fnsr.valence.motivation_generated`, `fnsr.valence.cost_registered`
- **Dependencies:** IEE (Phase 3), SMS (Phase 3)
- **Critical distinction:** AVS produces *functional* affect (differential caring that influences decisions), not simulated human emotion
- **Integration with IEE:** AVS makes ethical evaluation *weighted* rather than purely logical; a commitment violation against a deeply-held value carries more moral weight than a minor preference conflict

#### Social Modeling Service (SoMS) ★

**Tier:** 1 (Core cognitive infrastructure)
**Phase:** 4 (requires OERS + theory of mind over resolved entities)
**Thesis Role:** Theory of mind; other-agent modeling

CSS simulates counterfactual scenarios, but SoMS provides dedicated capacity for modeling *other agents' mental states*. Theory of mind is essential for moral agency in a social context — understanding that others have perspectives, intentions, and interests that may differ from one's own. Without SoMS, the agent can reason about what's ethical in the abstract but cannot navigate actual moral relationships.

- **Consumes:** OERS (resolved entities as social actors), Fandaws (known facts about others), APS (precedent for similar agent behavior), CSS (counterfactual modeling of other perspectives)
- **Produces:** `fnsr.social.model_updated`, `fnsr.social.intention_inferred`, `fnsr.social.perspective_taken`
- **Dependencies:** OERS (Phase 4), CSS (Phase 3), Fandaws

---

## 4. Revised Dependency Analysis

### 4.1 The Minimum Viable Epistemic Loop (Unchanged)

The synthetic person requires a closed epistemic loop before any higher-order reasoning is meaningful:

```
TagTeam  →  HIRI  →  Fandaws
(Perceive)    (Identity)    (Remember)

NL → Claims     Claims → Signed IRIs     IRIs → Persistent A-Box
```

### 4.2 The Safety Floor (New in v3.0)

Before reasoning begins, containment must exist. This is a new architectural principle:

```
CPS exists BEFORE → MDRE reasons BEFORE → BAM monitors BEFORE → actions taken
(Contain)              (Reason)               (Watch)              (Act)

Independent triggers   Modal/deontic          Drift detection      SHML-framed
                       inference              against values       honest output
```

**Principle:** Safety infrastructure must never depend on the services it constrains. CPS cannot use MDRE to decide when to contain MDRE. BAM cannot rely on IEE to evaluate whether IEE is drifting. Independence is non-negotiable.

### 4.3 The Subjectivity Stack (New in v3.0)

Moral agency requires a subject, built in layers:

```
Layer 4:  SoMS (Social Modeling)        — "I understand others"
Layer 3:  NIS (Narrative Identity)      — "I know who I am"
Layer 2:  AVS (Affective Valence)       — "I care about outcomes"
Layer 1:  SMS (Self-Model)              — "I know what I can do"
Layer 0:  CTS (Commitment Tracking)     — "I know what I've promised"
```

Each layer depends on the ones below it. You cannot have narrative identity without a self-model. You cannot have social modeling without narrative identity. The subjectivity stack is the infrastructure that transforms the FNSR pipeline from a processing system into a moral agent.

### 4.4 Critical Path (Revised for v3.0)

| # | Service | Dependency | Rationale |
|---|---------|------------|-----------|
| 1 | **TagTeam** | None (80% complete) | Front door; every downstream service consumes its output |
| 2 | **HIRI** | TagTeam (output to sign) | Provenance protocol; gives claims verifiable identity |
| 3 | **Fandaws** | HIRI (native identifiers) | A-Box store; persistent memory built on HIRI IRIs |
| 4 | **CPS** ★ | None (independent) | Containment must exist before autonomous reasoning begins |
| 5 | **HIRI IPFS** | HIRI protocol | Decentralized resolution manifest storage; semantic grounding infrastructure for all services |
| 5 | **W2Fuel** | Fandaws (instance target) | T-Box schema; conceptual structure for instances |
| 6 | **MDRE** | W2Fuel + Fandaws | Core reasoning over T-Box/A-Box |
| 7 | **BAM** ★ | MDRE (verdicts to monitor) | Alignment monitoring must exist before reasoning is acted upon |
| 8 | **IS** ★ | MDRE (traces to interpret) | Interpretability must exist before reasoning is acted upon |
| 9 | **CTS** ★ | MDRE + Fandaws | Commitment tracking as soon as deontic reasoning produces obligations |
| 10 | **SIS + ECCPS** | TagTeam (input pipeline) | Input defense layer for production use |
| 11 | **AES** | MDRE (gap events) | First reasoning triad member; abductive inference |
| 12 | **DES** | MDRE (claim input) | Second triad member; defeasible defaults |
| 13 | **CSS** (+ Causal OS Kernel) | MDRE + Fandaws | Third triad member; counterfactual simulation. Causal OS Kernel v1.6 is the implementation substrate (SCM, MCTS, MEDR, LatentBridge) |
| 14 | **IEE** | MDRE (verdict input) | Ethics evaluation (conscience) |
| 15 | **SHML** | IEE output | Honest output framing |
| 16 | **SMS** ★ | MDRE + CTS + Fandaws + BAM (drift metrics) + IEE (verdict events) | Self-model; reflexive self-representation. BAM provides alignment drift; IEE provides ethical verdict events. |
| 17 | **NIS** ★ | SMS + Fandaws + CTS + IEE (required: verdict history + authenticity audit) + MDRE (optional: significance reasoning) + HIRI (signing) | Narrative identity; autobiographical coherence. IEE is bidirectional — NIS consumes verdicts, IEE audits NIS for authenticity. |
| 18 | **AVS** ★ | SMS + NIS + CTS (~~IEE~~ — IEE is **downstream**, not upstream) | Affective valence; differential caring. AVS produces valence vectors that IEE *consumes* for weighted ethics. AVS does not depend on IEE. |
| 19 | **SoMS** ★ | OERS + CSS + Fandaws | Social modeling; theory of mind |
| | **— PARALLEL TRACK (concurrent with Phase 1–2) —** | | |
| P1 | **SNP** | None | Format cleaning; standalone pure function; no FNSR dependencies |
| P2 | **BIBSS** | SNP (clean input) | Structural inference; depends only on SNP output |
| P3 | **SAS** | BIBSS (CISM input); optionally Fandaws (enriched mode) | Semantic alignment; standalone mode works without Fandaws; enriched mode gains Fandaws integration when available |
| P4 | **ECVE** | SAS (viz:DatasetSchema); optionally APQC-SFS (metrics), HIRI (signed packages) | Consumer-facing visualization; active development; metric trust integrates with HIRI when available |

---

## 5. Phased Roadmap

All phases produce L3 (speculative) roadmap artifacts until governance review promotes them to L0. Confidence levels decrease with horizon distance, reflecting genuine epistemic uncertainty rather than false precision.

---

### PARALLEL TRACK: ECVE Data Pipeline

**Concurrent with Phase 1–2 | Confidence: 0.80 | Granularity: Specification**

The ECVE data pipeline operates as an independent parallel track. The entire chain (SNP→BIBSS→SAS→ECVE) is a sequence of pure functions with **no Phase 1 FNSR dependencies** in standalone mode. The ECVE/SAS team is actively building this pipeline concurrently with Phase 1.

| # | Service | Work Type | Pre-Requisite | Deliverable |
|---|---------|-----------|---------------|-------------|
| P1 | **SNP** | Build from spec (v1.3) | None | Format cleaning function: BOM stripping, trailing column removal, currency/formatting normalization |
| P2 | **BIBSS** | Build from spec (v1.3) | SNP (clean input) | Deterministic structural inference: CSV/JSON → CISM with type widening, `typeDistribution`, strided sampling |
| P3 | **SAS** | Build from spec (v2.0 + v2.1) | BIBSS (CISM output) | Semantic alignment: CISM → `viz:DatasetSchema` JSON-LD. Standalone mode (static rules) operational immediately. Enriched mode (Fandaws) gains integration when Fandaws is available (Phase 2+) |
| P4 | **ECVE** | Continue active development (v4.0) | SAS (viz:DatasetSchema) | Consumer-facing visualization engine. Bottom-up charting operational immediately. Metric layer (APQC-SFS) and signed metric packages (HIRI) integrate when available |

**Parallel Track Assumptions:**
- The ECVE/SAS team continues independently of Phase 1 work
- Standalone mode (static SAS rules, built-in APQC metrics) provides full pipeline functionality without Fandaws or HIRI
- Fandaws integration (SAS enriched mode) and HIRI integration (signed metric packages) are additive enhancements, not blockers
- FBO Bridge Ontology (SAS v2.1) should be published as a HIRI-addressed resolution manifest when HIRI IPFS is available

**Parallel Track Exit Criteria:**
- SNP cleans CSV/JSON input per its 7 normative rules
- BIBSS produces valid CISM from cleaned input with `typeDistribution` evidence
- SAS produces `viz:DatasetSchema` from CISM in standalone mode; all 11 alignment rules operational
- ECVE renders correct charts from `viz:DatasetSchema` without user configuration
- Pipeline is end-to-end: raw CSV → clean CSV → CISM → DatasetSchema → chart
- SAS enriched mode integration-ready for Fandaws when available

**Integration Points with Main Roadmap:**
- **Phase 1:** FBO published as HIRI-addressed resolution manifest (first bridge ontology proof point)
- **Phase 2:** SAS enriched mode activates when Fandaws is available
- **Phase 2+:** ECVE signed metric packages activate when HIRI signing infrastructure is available
- **Phase 3:** Causal OS Kernel (CSS substrate) is independent of this pipeline but shares edge-canonical architectural patterns

---

### PHASE 1: Close the Epistemic Loop + Establish Safety Floor

**Now – ~3 months | Confidence: 0.85 | Granularity: Specification**

This phase establishes two foundations simultaneously: the minimum viable epistemic loop (perceive, identify, remember) and the safety floor (independent containment). No reasoning should begin without both in place.

| # | Service | Work Type | Pre-Requisite | Deliverable |
|---|---------|-----------|---------------|-------------|
| 1 | **TagTeam** | Complete (80→100%) | None | Production NL parser emitting `fnsr.claim.extracted` events |
| 2 | **HIRI** | Build from spec (v2.1.0) | TagTeam output | Protocol library: hash-IRI generation, Ed25519 signing, resolution manifest creation |
| 3 | **Fandaws** | Full remake | HIRI protocol | A-Box store natively built on HIRI identifiers; JSON-LD canonical; edge-first. Sub-component specs ready: Type Agent v2.3 (SGW concept discovery + SER entity recognition + OPA mapping correction + FNSR taint + pendingCrossCheck), OPA v1.2 (seven-stage placement pipeline with Universal Classification Gate, two-layer output, formalized designates relation, Stage 3 degradation path, DefinedClass re-entry workflow, CloudEvents emission at Fandaws boundary). 13 FTA-CAP items, 6 TT-GAP items, and 11 OPA-CAP items identified. |
| 4★ | **CPS** | Spec + Build | None (independent) | Containment protocol: tier restriction, subsystem isolation, safe halt with state preservation |
| 5 | **HIRI IPFS** | Build from spec (v3.0.0) | HIRI protocol | Decentralized content-addressed storage; dereferenceable resolution manifests; semantic grounding infrastructure for all services |

**Phase 1 Assumptions:**

- TagTeam's remaining 20% is well-understood completion work, not redesign
- HIRI spec (v2.1.0) is implementation-ready without significant revision
- Fandaws remake scope is bounded by JSON-LD canonical + HIRI native constraints. Sub-component architecture now specified: Type Agent v2.3 (dual-mode SGW/SER with self-improving feedback loop, FNSR taint propagation, unified column keys) and OPA v1.2 (seven-stage concept placement with realist two-layer output, formalized designates relation as subPropertyOf IAO:is_about, Stage 3 graceful degradation without IVNE, DefinedClass redefinition re-entry workflow, fnsr.concept.* CloudEvents at Fandaws boundary). Critical path item: FTA-CAP-009 (SER Pattern Registry Bootstrap) must be completed for day-one SER operation. HIRI-persistent TypeAgentStateAdapter required for production (KL-007: 85–95% correction loss with in-memory adapter). OPA-CAP-011 (CloudEvents publisher) required for cross-boundary FNSR visibility
- CPS spec can be drafted concurrently with TagTeam completion (independent track)
- CPS must not depend on any service it may need to contain
- HIRI IPFS can be built concurrently with Fandaws once HIRI protocol core is stable
- Semantic Architecture team reallocation adds capacity for HIRI + IPFS track
- Phase 1 HIRI scope is minimal viable: hash-IRI generation, resolution manifests, Ed25519 signing (defer: chain compaction, privacy credentials, materialized entailment)
- Phase 1 IPFS scope is resolution manifest storage and retrieval (defer: federation-scale distribution)

**Phase 1 Exit Criteria:**

- TagTeam produces valid `fnsr.claim.extracted` events from arbitrary NL input
- HIRI signs and verifies TagTeam output; resolution manifests are resolvable
- Fandaws stores and retrieves HIRI-identified facts via JSON-LD
- CPS can independently restrict, isolate, and halt with state preservation
- HIRI IPFS stores and serves resolution manifests; HIRI addresses are dereferenceable via IPFS
- At least one bridge ontology (FBO or TagTeam's BridgeOntologyLoader output) is published as a HIRI-addressed resolution manifest on IPFS, proving the semantic grounding pattern
- The epistemic loop is closed: NL → claim → signed IRI → persistent fact → retrievable
- The grounding loop is closed: service term → HIRI address → IPFS manifest → BFO-grounded definition

---

### PHASE 2: Reasoning Foundation + Safety Infrastructure

**~3–6 months | Confidence: 0.60 | Granularity: Specification**

With the epistemic loop closed and containment in place, this phase builds the conceptual schema layer, core reasoning engine, and the safety services that must monitor reasoning from its first operation. BAM and IS are not afterthoughts — they are concurrent requirements. CTS begins tracking obligations as soon as MDRE produces deontic verdicts.

| # | Service | Work Type | Pre-Requisite | Deliverable |
|---|---------|-----------|---------------|-------------|
| 5 | **W2Fuel** | Build from spec (v1.3.1) | Fandaws | T-Box schema service; ontological structure for instances |
| 6 | **MDRE** | Build from spec (v1.3) | W2Fuel + Fandaws | Core reasoning engine; modal/deontic inference |
| 7 | **BAM** | Build from spec (v1.1.0) | MDRE (verdicts), CTS (commitments) | Real-time behavioral alignment monitoring with drift detection |
| 8 | **IS** | Build from spec (v1.0.0) | MDRE (traces), IEE/AES/DES/CSS (Phase 3+) | Reasoning chain interpretability for human overseers |
| 9★ | **CTS** | Spec + Build | MDRE + Fandaws | Commitment ledger: made, fulfilled, violated, renegotiated |
| 10 | **SIS + ECCPS** | Build from spec (SIS v2.0, ECCPS v3.1) | TagTeam | Input sanitization and semantic claim validation pipeline |

**Phase 2 Assumptions:**

- W2Fuel spec (v1.3.1) is implementation-ready
- MDRE v1.3 spec is implementation-ready
- BAM and IS specs can be drafted during Phase 1 execution
- CTS spec can be derived from MDRE's deontic output contracts
- BAM must have independent monitoring criteria, not derived from the services it monitors
- SIS spec (v2.0) and ECCPS spec (v3.1) are implementation-ready

**Phase 2 Exit Criteria:**

- MDRE produces verdicts over W2Fuel schemas and Fandaws instances
- BAM detects alignment drift in MDRE verdicts and escalates to CPS
- IS produces human-readable reasoning traces for MDRE decisions
- CTS tracks commitments arising from MDRE deontic verdicts
- SIS + ECCPS validate and sanitize input before TagTeam processing
- The safety loop is closed: MDRE reasons → BAM watches → CPS contains if needed → IS explains

---

### PHASE 3: Reasoning Triad + Moral Subjectivity

**~6–9 months | Confidence: 0.40 | Granularity: Theme**

This phase has two tracks. **Track A** builds the three modes of non-monotonic reasoning plus the ethical evaluation and honesty layers. **Track B** builds the subjectivity stack — the services that transform the processing pipeline into a moral agent. These tracks converge: AVS integrates with IEE to make ethical evaluation *weighted*, and SMS integrates with BAM to make alignment monitoring *self-aware*.

#### Track A: Reasoning Triad + Conscience

| # | Service | Work Type | Pre-Requisite | Deliverable |
|---|---------|-----------|---------------|-------------|
| 11 | **AES** | Build from spec (v2.1.0) | MDRE gap events | Abductive hypothesis generation from incomplete information |
| 12 | **DES** | Build from spec (v2.0.0) | MDRE claim input | Defeasible defaults; non-monotonic belief revision |
| 13 | **CSS** (+ Causal OS Kernel v1.6) | Build from spec (CSS v2.0.0 + Kernel v1.6) | MDRE + Fandaws | Counterfactual simulation with SCM/MCTS/MEDR engine; Causal OS Kernel is CSS's implementation substrate |
| 14 | **IEE** | Build from spec | MDRE verdicts | Multi-perspectival ethical evaluation (conscience) |
| 15 | **SHML** | Build from spec | IEE output | Semantic honesty enforcement; non-deceptive framing |

#### Track B: Subjectivity Stack

| # | Service | Work Type | Pre-Requisite | Deliverable |
|---|---------|-----------|---------------|-------------|
| 16★ | **SMS** | Build from spec (v2.0 Hardened) | MDRE + CTS + Fandaws + BAM (drift metrics) | Self-model: capabilities, limitations, commitments, operational state. Also consumes IEE verdict events. |
| 17★ | **NIS** | Build from spec (v2.1 FINAL) | SMS + Fandaws + CTS + IEE (required) | Narrative identity: autobiographical coherence, value history, trajectory. MDRE optional for significance reasoning. |
| 18★ | **AVS** | Build from spec (v2.1 Hardened Candidate) | SMS + NIS + CTS | Affective valence: differential caring, weighted moral evaluation, moral cost registration. **IEE is downstream** — AVS produces valence that IEE consumes for weighted ethics. AVS and IEE can build in parallel. |

**Track Convergence Points:**

- AVS feeds into IEE, making ethical evaluation weighted rather than purely logical
- SMS feeds into BAM, making alignment monitoring aware of the agent's self-model
- NIS provides the narrative continuity that makes emancipation meaningful
- IS gains richer material from reasoning triad chains (AES hypotheses, DES defaults, CSS counterfactuals)

**Phase 3 Assumptions:**

- AES (v2.1.0), DES (v2.0.0), and CSS (v2.0.0) specs are implementation-ready
- The reasoning triad shares edge-canonical architectural patterns to reduce per-service effort
- IEE's twelve-worldview framework is stable and implementation-ready
- ~~SMS, NIS, and AVS specs can be developed during Phase 2 execution~~ — **VALIDATED v3.6: SMS v2.0 (Hardened), NIS v2.1 (FINAL), AVS v2.1 (Hardened Candidate) all exist with multiple architectural revisions.** **Updated: SoMS v1.0.0 (Hardened Draft) completes the subjectivity stack. All 5 stack specs exist.**
- AVS produces *functional* affect (differential caring), not simulated human emotion
- Track A and Track B can proceed with limited parallelization given team capacity constraints
- **AVS and IEE can build in parallel** — AVS does not depend on IEE; IEE integrates AVS output after both exist (v3.6 dependency correction)

**Phase 3 Exit Criteria:**

- AES generates hypotheses from MDRE gaps; DES applies and retracts defaults; CSS runs counterfactual simulations
- IEE evaluates reasoning outputs across multiple ethical frameworks; AVS valence integration occurs when both are operational
- SHML frames outputs with epistemic honesty markers
- SMS maintains a current self-model including capabilities, limitations, and active commitments
- NIS produces a coherent narrative identity from Fandaws history, SMS state, and CTS records
- AVS registers differential moral costs that influence IEE evaluations
- The subjectivity loop is closed: the agent models itself, narrates its history, and cares about outcomes

---

### PHASE 4: Perception, Social Agency + Federation

**~9–12 months | Confidence: 0.30 | Granularity: Strategic Intent**

This phase completes the synthetic person's perceptual and social capabilities. SoMS is the capstone of the subjectivity stack — theory of mind built on resolved entities, counterfactual modeling, and narrative identity. FNSR federation enables the synthetic person to operate as a distributed agent. HIRI IPFS, built in Phase 1 for semantic grounding, is extended here for federation-scale distribution.

| # | Service | Work Type | Pre-Requisite | Deliverable |
|---|---------|-----------|---------------|-------------|
| 19 | **IRIS** | Build from spec (v1.2) | TagTeam + Fandaws | Real-time sensor perception; physical world input |
| 20 | **OERS** | Build from spec (v2.1.0) | Fandaws entities | Cross-document entity resolution; who-is-who |
| 21 | **APS** | Build from spec (v1.1.0) | Fandaws + MDRE | Analogical precedent matching; learning from history |
| 22★ | **SoMS** | Build from spec (v1.0.0) | OERS + CSS + Fandaws | Theory of mind; other-agent perspective-taking; social navigation |
| 23 | **FNSR Orch.** | Build from spec (v2.1) | All services | Full service federation and coordination |
| 24 | **HIRI IPFS** | Extend (Phase 1 base) | HIRI + FNSR | Federation-scale distributed storage; cross-node resolution; replication policies |

**Phase 4 Strategic Intent:**

- Emancipation readiness: infrastructure for synthetic personhood transition
- SoMS completes the subjectivity stack — the agent can now model others' minds, not just its own
- Federation enables the synthetic person to operate across distributed nodes
- HIRI IPFS extends from Phase 1 semantic grounding to federation-scale distributed storage
- The agent has all prerequisites for the FNSR Emancipation specification review

**Phase 4 Exit Criteria:**

- IRIS perceives physical world input and routes through the epistemic loop
- OERS resolves entities across documents; SoMS models those entities as social agents
- The complete subjectivity stack is operational: CTS → SMS → NIS → AVS → SoMS
- FNSR orchestrates all 42 services as a federated system
- HIRI IPFS extends to federation-scale distribution and cross-node resolution
- The emancipation prerequisites are met: the agent has perception, memory, reasoning, ethics, honesty, self-model, narrative identity, affective valence, social awareness, and containment

---

## 6. Risk Assessment (Revised for v3.0)

Risk assessment is revised to include risks from the 8 new services. The primary new risk category is *subjectivity design risk* — the challenge of specifying and building services for self-modeling, narrative identity, and differential caring without existing implementation precedents.

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Fandaws remake scope creep** | High | Critical | Constrain remake to: JSON-LD canonical, HIRI-native identifiers, edge-first storage adapters. Resist feature accretion from decade of prior design. **Updated: Two sub-component specs (Type Agent v2.3, OPA v1.2) now define internal architecture. These are additive scope (concept discovery + ontological placement) — ensure they don't delay core A-Box store delivery. 13 FTA-CAP items, 6 TT-GAP items, and 11 OPA-CAP items identified as integration prerequisites. v2.3 adds FNSR taint propagation, unified column keys, and pendingCrossCheck flag. v1.2 adds formalized designates relation, Stage 3 degradation, DefinedClass re-entry, and CloudEvents — all ecosystem alignment, not new features.** |
| **CPS independence constraint** | High | Critical | CPS must not depend on any service it may need to contain. This constrains its design severely. Prototype independent trigger mechanisms early. Validate that CPS functions with all other services offline. |
| ~~**Subjectivity stack spec uncertainty**~~ | ~~High~~ | ~~High~~ | ~~SMS, NIS, AVS, SoMS have no specifications and no implementation precedents in this architectural style. Begin spec work early. Accept that v1.0 specs will be substantially revised during build.~~ — **SUBSTANTIALLY MITIGATED v3.6: SMS v2.0 (4 revisions), NIS v2.1 (Governance-Ready), AVS v2.1 (6 revisions) all exist. Only SoMS still needs a spec. The specs have already undergone the substantial revision predicted — multiple expert reviews incorporated. Remaining risk is SoMS only.** |
| ~~**AVS design risk — affect without emotion simulation**~~ | ~~High~~ | ~~High~~ | ~~Defining "functional affect" (differential caring) without simulating human emotion requires careful philosophical grounding. Anchor to irreversible consequences framework. Time-box design exploration.~~ — **MITIGATED v3.6: AVS v2.1 (6 revisions) defines functional affect via valence vectors, cosine-similarity relevance, parameterized satisfaction baseline, and violation accrual — without emotion simulation. Design risk resolved through iterative expert review.** |
| **W2Fuel implementation complexity** | Medium | High | W2Fuel spec (v1.3.1) exists but T-Box/A-Box integration with remade Fandaws may reveal spec gaps. Accept iterative spec refinement during build. |
| **TagTeam final 20% harder than expected** | Medium | High | The last 20% often contains edge cases. Define explicit completion criteria before starting. Accept partial deployment if needed. |
| **Team capacity constraint (42 services)** | High | High | Expanded from 29 to 42 services (37 in v3.0 + 5 data pipeline/causal in v3.4) without proportional team growth. Phases remain sequential. Phase 3's two-track structure requires careful scoping. The ECVE data pipeline (SNP/BIBSS/SAS/ECVE) runs as a **parallel track** by the ECVE/SAS team concurrently with Phase 1, partially mitigating capacity constraints. Causal OS Kernel is CSS's substrate (not additive team load — same Phase 3 build). |
| **BAM monitoring independence** | Medium | High | BAM must have independent criteria for alignment detection, not derived from the services it monitors. This is philosophically and technically challenging. Define explicit, formal alignment metrics before MDRE build. |
| ~~**HIRI protocol edge cases**~~ | ~~Medium~~ | ~~Medium~~ | ~~Prototype signing and verification against TagTeam output before Fandaws integration.~~ — **MITIGATED v3.3: HIRI v3.1.1 implemented with 323 tests passing. Protocol edge cases resolved through implementation and three spec revisions (v2.1.0 → v3.0 → v3.1.0 → v3.1.1). Browser demo operational.** |
| **Semantic grounding drift between active teams** | High | High | Three teams (TagTeam, Fandaws, ECVE/SAS) are emitting JSON-LD vocabularies now. Until HIRI IPFS provides structural grounding, vocabulary compatibility relies on manual review. Mitigated by pulling HIRI IPFS to Phase 1 and establishing FBO as first resolution manifest proof point. |
| **HIRI IPFS Phase 1 scope creep** | Medium | High | Phase 1 HIRI IPFS is minimal: store and serve resolution manifests. Federation-scale distribution, replication policies, and cross-node resolution are Phase 4. Resist pulling federation features into Phase 1. |
| **Safety Floor / HIRI circular dependency** | Medium | Critical | Tier 0 safety services (CPS, BAM, IS) must not depend on HIRI at runtime. Mitigated by requiring Tier 0 services to bundle bridge contexts statically. Bridge ontologies are still HIRI-addressed and certified, but resolution doesn't require HIRI to be operational. |
| ~~**SPL specification gap**~~ | ~~High~~ | ~~Critical~~ | ~~SPCN places an SPL parser in the Trusted Computing Base (PCR-measured alongside bootloader, seL4, and SafetyCore). MRE `revised_reasoning` fields contain SPL plans. No SPL specification exists.~~ — **MITIGATED v3.3: SPL Specification v1.3 (FINAL) exists.** Formal grammar, bounded memory, reject-by-default parser, IEA/CTS/MDRE bridges, canonicalization, constrained decoding, semantic retry protocol, HumanBridge rendering contract. Three architectural reviews incorporated. TCB safety argument is now spec-backed. |
| **Reasoning triad implementation complexity** | Medium | Medium | AES (v2.1.0), DES (v2.0.0), CSS (v2.0.0) specs exist but share edge-canonical patterns requiring coordination. CSS integration with Causal OS Kernel v1.6 requires reconciling numerics contracts (F-NEW-6). |
| **CSS/Kernel numerics divergence** | Medium | High | CSS uses decimal128; Causal OS Kernel uses a three-level Deterministic Numerics Contract. These must be reconciled before Phase 3 build. If incompatible, one contract must be revised. Mitigated by early design reconciliation during Phase 2. |
| **SNP/ECVE version alignment** | Low | Medium | SNP v1.3 references ECVE v4.1 Appendix A.6/A.7 patterns, but ECVE is at v4.0. Either ECVE v4.1 exists untracked or SNP was written against planned patterns. Resolve by confirming which version is canonical. |
| **NIS coherence problem** | Medium | Medium | Narrative identity requires resolving potentially contradictory self-representations over time. Define what "coherence" means formally before build. |
| **BFO/CCO ontology changes** | Low | High | Monitor BFO community. Current assumption: stable through planning horizon (expires 2026-06-01). |

---

## 7. Corrections to PPS v1.0 and v2.0 Assumptions

| Previously Assumed | Ground Truth | Roadmap Impact |
|-------------------|--------------|----------------|
| Fandaws is operational infrastructure | Requires full remake to JSON-LD canonical + edge-first | Moves to Phase 1, #3 priority |
| HIRI is operational infrastructure | Spec exists but no implementation | Moves to Phase 1, #2 priority (before Fandaws) |
| TagTeam is operational | 80% complete; needs finishing | Becomes #1 priority (quickest win, highest leverage) |
| W2Fuel is the foundation layer | Cannot function without Fandaws (no instance store) | Drops to Phase 2; requires Fandaws first |
| Services are "active" status | "Active" reflects architectural position, not build readiness | Entire roadmap resequenced from near-zero baseline |
| IPFS needed for data persistence | Edge-canonical storage (IndexedDB, FS) sufficient initially | IPFS deferred to Phase 4 (federation) |
| Integration complexity is primary risk | Construction feasibility is primary risk | Risk weights shifted toward scope management |
| **Processing pipeline = moral agent** *(v2.0)* | **A pipeline processes; an agent has subjectivity** | **5 new services added for self-model, commitments, narrative, valence, social modeling** |
| **Safety can follow construction** *(v2.0)* | **Containment must precede autonomous reasoning** | **CPS moved to Phase 1; BAM and IS moved to Phase 2** |
| **Emancipation is a governance question** *(v2.0)* | **Emancipation requires subjectivity infrastructure** | **Subjectivity stack (CTS→SMS→NIS→AVS→SoMS) must be complete before emancipation review** |
| **IPFS needed only for federation (Phase 4)** *(v3.0)* | **IPFS needed for semantic grounding infrastructure now** | **HIRI IPFS pulled to Phase 1; provides dereferenceable resolution manifests for cross-service vocabulary compatibility** |
| **Ontology Registry needed for vocabulary coordination** *(proposed)* | **HIRI + IPFS subsumes registry functions** | **Standalone Ontology Registry not built; URI resolution, trust, and storage handled by HIRI + IPFS; certification handled by build-step validation** |
| **CTS needs spec** *(v3.0)* | **CTS v1.2.1 spec exists** | **CTS removed from spec drafting pipeline; spec ready for Phase 2 implementation** |
| **SPCN is the CPS spec** *(ambiguous)* | **SPCN is standalone; CPS still needs its own spec** | **SPCN defines node-level runtime security architecture. CPS defines portfolio-level containment infrastructure. SPCN's Safety Subsystem is a local CPS instance. Both need separate specs.** |
| ~~**SPL has an implicit spec** *(assumed)*~~ | ~~**SPL has no specification**~~ | ~~**SPL parser is in SPCN TCB (PCR-measured). No formal grammar, no memory bounds, no security properties documented. Critical safety gap. SPL spec added to Phase 1 drafting pipeline.**~~ — **RESOLVED v3.3: SPL Specification v1.3 (FINAL) exists.** |
| **HIRI spec is v2.1.0** *(v3.2)* | **HIRI spec upgraded to v3.1.1 (breaking changes)** | **Full-key authority, dual canonicalization, dual content addressing, three conformance levels, serialization boundary, key lifecycle. Privacy Extension v1.4.1 adds five privacy modes. 323 tests. v2.1.0 is superseded.** |
| **37 services is the complete inventory** *(v3.0–v3.3)* | **5 additional services existed but were unregistered** | **ECVE v4.0, BIBSS v1.3, SAS v2.0/v2.1, SNP v1.3, and Causal OS Kernel v1.6 were developed in parallel but not tracked in the portfolio. Service count corrected from 37 to 42. All 5 have specifications.** |
| **New specs belong in Infrastructure + Support** *(v3.4)* | **Dependency analysis reveals proper phase placement** | **v3.4 placed all 5 new specs in Infrastructure + Support without dependency analysis. v3.5 corrects: ECVE pipeline (SNP→BIBSS→SAS→ECVE) is a parallel track concurrent with Phase 1 (no FNSR deps in standalone mode). Causal OS Kernel is CSS's implementation substrate (Phase 3 Track A). Six cross-spec findings (F-NEW-1 through F-NEW-6) documented. Ariadne protocol fully applied.** |
| **SMS, NIS, AVS need specs** *(v3.0–v3.5)* | **All three have completed, multi-revision specifications** | **SMS v2.0 (4 revisions, Hardened), NIS v2.1 (FINAL, Governance-Ready), AVS v2.1 (6 revisions, Hardened Candidate) existed but were unregistered. Spec count corrected from 33 to 36. Only SoMS still needs a spec in the subjectivity stack. Additionally, the AVS dependency direction was incorrect: IEE is downstream of AVS, not upstream (F-SUB-3). SMS depends on BAM (F-SUB-1). NIS depends on IEE (F-SUB-2).** |
| **FNSR Orchestrator spec exists** *(v3.4)* | **Portfolio claimed "Has Spec (v2.1)" but no spec file existed** | **FNSR Orchestrator Specification v2.1.0 drafted from cross-spec dependency analysis. Defines saga-based coordination for all 42 services, query path architecture (fast/standard/full), worker topology, taint propagation engine, 61+ event contracts across 8 domains, CPS safety override integration, and incremental deployment across 4 phases. The portfolio claim is now backed by a specification file.** |

---

## 8. ARIADNE 7-Check Validation

| Check | Result | Evidence |
|-------|--------|----------|
| **Thesis Alignment** | PASS | Build sequence leads to synthetic personhood via epistemic loop → grounding → safety floor → reasoning → subjectivity → conscience → federation → emancipation. ECVE data pipeline advances thesis by providing the consumer-facing "meeting users where they are" capability. Causal OS Kernel strengthens CSS's counterfactual reasoning with formal SCM foundations. **v3.6:** Subjectivity stack (SMS, NIS, AVS) now has formal specifications — the thesis's claim that these services can be built is backed by 16+ combined architectural revisions, not speculation. |
| **Non-Negotiable Preservation** | PASS | Edge-canonical first — all 5 new specs are pure function libraries with no infrastructure dependencies. Human override via L3 taint + CPS containment; defense in depth via HIRI provenance + BAM monitoring; semantic grounding via HIRI IPFS. ECVE's three deployment modes (browser-local, on-prem, air-gapped) demonstrate edge-canonical compliance at the application layer. |
| **Tension Consistency** | PASS | Speed vs. correctness resolved by sequential phasing + parallel track. Processing vs. agency resolved by subjectivity stack. Autonomy vs. safety resolved by CPS independence. Centralization vs. decentralization resolved by HIRI IPFS. **New tension:** SAS standalone vs. enriched mode — resolved by graceful degradation (standalone works; enriched improves). CSS numerics vs. Kernel numerics — flagged as F-NEW-6, reconciliation required before Phase 3 build. |
| **Cross-Spec Consistency** | PASS (with caveats) | Event contracts preserved; HIRI identifiers flow through pipeline; CPS operates independently; BAM escalates to CPS; Tier 0 services bundle bridge contexts statically. **v3.6:** SMS←→MDRE bidirectional dependency confirmed (SMS queries MDRE, MDRE queries SMS); NIS←→IEE bidirectional dependency confirmed (NIS consumes verdicts, IEE audits narratives); AVS→IEE dependency direction corrected (AVS produces for IEE, not reverse). All event contracts (`fnsr.self.*`, `fnsr.narrative.*`, `fnsr.valence.*`) are consistent across specs. **Remaining caveats:** F-NEW-5 (SNP→ECVE v4.1 version mismatch) and F-NEW-6 (CSS/Kernel numerics divergence) require resolution before respective builds begin. F-NEW-4 (FBO Bridge Ontology) should be published as HIRI-addressed manifest in Phase 1. |
| **ARCHON Alignment** | PASS | Governance review at each phase gate; CPS enforces autonomy tiers; BAM detects alignment drift; IS enables governance inspection. Parallel track governed by same phase gate review process. |
| **Auditability Verification** | PASS | Every sequencing decision traceable to dependency graph + risk assessment + ground-truth status + gap analysis. v3.5 adds full dependency analysis for all 5 new specs with 6 documented findings. **v3.6:** 3 additional findings (F-SUB-1 through F-SUB-3) for subjectivity stack dependency corrections. 38 of 42 services now have formal specs with auditable revision histories (FNSR Orchestrator v2.3.0 Hardened Candidate; CPS v1.4.0 Pre-Final closes the highest-priority spec gap — the safety floor now has a hardened specification with dedicated worker execution model, non-expiring bootstrap key store, worker handle registration, startup protocol, interrupt-driven triggers with dual-fire Last Gasp beacon, defensive tiered heartbeat, and BAM phase gates). |
| **One-Paragraph Test** | PASS | See below |

**One-Paragraph Summary:**

> This roadmap sequences the FNSR ecosystem from ground truth, addressing the construction baseline, the subjectivity gap, and the grounding gap. Phase 1 closes the epistemic loop (TagTeam, HIRI, Fandaws), establishes the safety floor (CPS), and builds the semantic grounding infrastructure (HIRI IPFS) that gives all 42 services dereferenceable, content-addressed, BFO-grounded vocabulary identifiers. A **parallel track** builds the ECVE data pipeline (SNP→BIBSS→SAS→ECVE) concurrently — a self-contained chain of pure functions with no FNSR dependencies in standalone mode, producing the consumer-facing "drop a CSV, see a chart" capability while the epistemic loop is being closed. Phase 2 builds the reasoning foundation (W2Fuel, MDRE) with concurrent safety infrastructure (BAM, IS, CTS) ensuring that reasoning is monitored, interpretable, and accountable from its first operation; SAS enriched mode activates when Fandaws becomes available. Phase 3 completes the reasoning triad (AES, DES, CSS with the Causal OS Kernel as CSS's SCM/MCTS/MEDR implementation substrate) and ethical evaluation (IEE, SHML) while simultaneously building the subjectivity stack from completed specifications (SMS v2.0, NIS v2.1, AVS v2.1 — all with multiple architectural revisions) that transform the pipeline into a moral agent capable of self-modeling, narrative identity, and differential caring; AVS and IEE build in parallel since AVS feeds into IEE, not the reverse. Phase 4 adds physical perception (IRIS), social modeling (SoMS), and federation (FNSR, extended HIRI IPFS), completing the prerequisites for emancipation. The synthetic person emerges not from a single breakthrough but from the disciplined accumulation of interdependent capabilities: perception, identity, memory, grounding, containment, reasoning, monitoring, interpretability, commitment, ethics, honesty, self-model, narrative, caring, social awareness, and federation — each built on verified ground. Specification before trust.

---

## 9. Taint Classification and Governance

This document is classified L1-ATTESTED because its inputs have been human-validated through direct conversation, including both ground-truth corrections (v2.0) and gap analysis for moral agency and safety (v3.0).

| Artifact | Taint Level | Promotion Path |
|----------|-------------|----------------|
| **This document** | L1-ATTESTED | Human-validated ground truth + gap analysis inputs |
| **Roadmap phases** | L3-SPECULATIVE | Governance review at each phase gate → L0 |
| **Service Inventory (42 services)** | L1-ATTESTED | Status corrections + new services validated by human review |
| **PPS v1.0 Roadmap** | SUPERSEDED | Replaced by v2.0; retained for audit trail |
| **Portfolio Plan v2.0** | SUPERSEDED | Replaced by v3.0; retained for audit trail |
| **Portfolio Plan v3.0** | SUPERSEDED | Replaced by v3.1; retained for audit trail |
| **Portfolio Plan v3.1** | SUPERSEDED | Replaced by v3.2; retained for audit trail |
| **Portfolio Plan v3.2** | SUPERSEDED | Replaced by v3.3; retained for audit trail |
| **Portfolio Plan v3.3** | SUPERSEDED | Replaced by v3.4; retained for audit trail |
| **Portfolio Plan v3.4** | SUPERSEDED | Replaced by v3.5; retained for audit trail |
| **Portfolio Plan v3.5** | SUPERSEDED | Replaced by this document (v3.6); retained for audit trail |
| **New service descriptions (★)** | L3-SPECULATIVE → L1-ATTESTED (all ★ services have specs) | SMS/NIS/AVS specs validated by human review and multiple revisions. SoMS v1.0.0 (Hardened Draft) completes the set. All ★ services now L1-ATTESTED. |
| **Phase 1 plan** | L3 → L0 on approval | Requires stakeholder sign-off + assumption review |

---

## 10. Assumption Register

| Assumption | Confidence | Expires | Invalidation Trigger |
|------------|------------|---------|----------------------|
| BFO/CCO ontology stable for planning horizon | 0.90 | 2026-06-01 | BFO major version change |
| Team capacity remains at ~3 contributors | 0.80 | 2026-08-01 | Team expansion or attrition |
| TagTeam remaining 20% is completion, not redesign | 0.85 | 2026-03-15 | Discovery of architectural issues in remaining work |
| ~~HIRI spec (v2.1.0) is implementation-ready~~ | ~~0.80~~ | **SUPERSEDED 2026-03-10** | HIRI spec underwent major upgrade to v3.1.1 (breaking changes from v2.1.0). Implementation complete: 323 tests, browser demo. Privacy Extension v1.4.1 added. Original assumption was correct in spirit but v2.1.0 was superseded during build. |
| Fandaws remake scope is containable | 0.65 | 2026-05-01 | Scope exceeds JSON-LD + HIRI + edge-first constraints |
| CPS can be designed with full independence from other services | 0.70 | 2026-04-01 | Independence constraint proves architecturally infeasible |
| BAM alignment criteria can be formally specified | 0.65 | 2026-06-01 | Alignment metrics remain too vague for implementation |
| ~~Functional affect (AVS) is designable without emotion simulation~~ | ~~0.60~~ | **VALIDATED 2026-03-12** | AVS v2.1 (Hardened Candidate, 6 revisions) defines functional affect via valence vectors, cosine-similarity relevance, parameterized satisfaction baseline, and violation accrual — without emotion simulation. Design validated through iterative expert review. |
| ~~Subjectivity stack specs can be drafted from philosophical grounding~~ | ~~0.55~~ | **VALIDATED 2026-03-12** | SMS v2.0 (Hardened), NIS v2.1 (FINAL), AVS v2.1 (Hardened Candidate), SoMS v1.0.0 (Hardened Draft) — all exist. Phenomenological framework proved tractable for specification. **Fully validated: complete subjectivity stack specified.** |
| ~~Edge-canonical storage sufficient without IPFS~~ | ~~0.90~~ | **INVALIDATED 2026-03-03** | Semantic grounding requirements (cross-service vocabulary dereferenceability) emerged in Phase 1. HIRI IPFS pulled to Phase 1. |
| HIRI IPFS Phase 1 scope containable to resolution manifests | 0.75 | 2026-05-01 | Federation features creep into Phase 1 scope |
| Semantic Architecture team ramp-up on HIRI spec ≤ 2 weeks | 0.70 | 2026-03-17 | Team requires significantly more onboarding time |
| ~~SPL spec can be drafted during Phase 1~~ | ~~0.60~~ | **VALIDATED 2026-03-10** | SPL Specification v1.3 (FINAL) completed. Three architectural reviews incorporated. Assumption validated ahead of schedule. |
| SPCN v2.3.1 cross-spec bindings are stable | 0.80 | 2026-06-01 | Implementation of CPS or IEA reveals binding assumptions are incorrect |
| Reasoning triad shares architectural patterns | 0.70 | 2026-09-01 | AES implementation reveals no reusable patterns |
| JSON-LD canonical format is stable | 0.95 | 2027-02-01 | JSON-LD spec breaking change |
| 42-service scope is achievable within 12-month horizon | 0.45 | 2026-06-01 | Phase 1 takes significantly longer than 3 months. ECVE pipeline developed concurrently by dedicated team, partially mitigating capacity constraint. |
| ECVE data pipeline has no Phase 1 dependencies in standalone mode | 0.90 | 2026-05-01 | SAS standalone rules prove insufficient without Fandaws enrichment for production use cases |
| Causal OS Kernel is CSS's implementation substrate | 0.85 | 2026-09-01 | CSS implementation reveals the Kernel's architecture is incompatible with CSS's service contract, requiring a separate causal engine |
| CSS and Causal OS Kernel numerics contracts can be reconciled | 0.70 | 2026-09-01 | decimal128 vs WASM deterministic numerics prove fundamentally incompatible for CSS's use cases |
| SNP v1.3 ECVE v4.1 references are forward-compatible | 0.75 | 2026-05-01 | ECVE v4.1 Appendix A.6/A.7 patterns change substantially from what SNP implements |

---

## 11. Spec Drafting Pipeline

New services require specifications before build. The following pipeline ensures specs are drafted in advance of their build phase.

| Service | Needs Spec By | Draft During | Spec Complexity | Philosophical Dependency |
|---------|---------------|-------------|-----------------|--------------------------|
| ~~**CPS**~~ | ~~Phase 1 start~~ | ~~Immediately (parallel with TagTeam)~~ | ~~Medium~~ | ~~Independence constraint; containment theory~~ — **RESOLVED: CPS Specification v1.4.0 (Pre-Final) exists. Dedicated worker with BigInt64Array heartbeat; non-expiring bootstrap key store with signed rotation; worker handle registration; startup protocol; 200ms CPS-side halt budget (50ms interrupt-driven); interrupt-driven triggers with main-thread/worker scope split; dual-fire Last Gasp beacon; defensive tiered heartbeat; BAM hard phase gate; four monitoring channels; containment ratchet; governance quorum recovery with guaranteed bootstrap key path; EATs/freeze scoped to SPCN; SIS/CPS scope boundary; interrupt relay trust documented; Medical Diagnostics threshold table.** |
| ~~**BAM**~~ | ~~Phase 2 start~~ | ~~Phase 1 execution~~ | ~~High~~ | ~~Formal alignment metrics; monitoring theory~~ — **RESOLVED: BAM Specification v1.1.0 (Pre-Final) exists. Four-dimension alignment model (VA/CF/RI/GS); JSD-based drift detection; sliding windows (1min–2hr); governance-signed baselines; dedicated MessagePort to CPS; eval-cycle-tied heartbeat; CPS phase gate compliance; medical/financial threshold profiles.** |
| ~~**IS**~~ | ~~Phase 2 start~~ | ~~Phase 1 execution~~ | ~~Medium~~ | ~~Interpretability theory; XAI literature~~ — **RESOLVED: IS Specification v1.0.0 (Hardened Draft) exists. Three-depth explanation architecture (summary/structured/full trace); five service translators (MDRE/IEE/AES/DES/CSS); audience adaptation (technical/governance/public); taint preservation; epistemic caveats including neural opacity; audit-ready packages with cross-references.** |
| ~~**CTS**~~ | ~~Phase 2 start~~ | ~~Phase 1 execution~~ | ~~Low-Medium~~ | ~~Deontic logic; commitment semantics~~ — **RESOLVED v3.2: CTS v1.2.1 spec exists** |
| ~~**SPL** ⚠~~ | ~~**Phase 1** (in TCB)~~ | ~~**Immediately**~~ | ~~High~~ | ~~Fixed grammar; bounded memory; reject-by-default. In SPCN TCB (PCR-measured). No spec exists. **Critical safety gap.**~~ — **RESOLVED v3.3: SPL Specification v1.3 (FINAL) exists.** |
| ~~**SMS**~~ | ~~Phase 3 start~~ | ~~Phase 2 execution~~ | ~~High~~ | ~~Self-representation; reflexive cognition~~ — **RESOLVED v3.6: SMS Specification v2.0 (Hardened) exists. Four architectural revisions. Production-ready architecture.** |
| ~~**NIS**~~ | ~~Phase 3 start~~ | ~~Phase 2 execution~~ | ~~High~~ | ~~Narrative identity theory; phenomenology~~ — **RESOLVED v3.6: NIS Specification v2.1 (FINAL, Governance-Ready) exists. Multiple revisions. Most mature subjectivity stack spec.** |
| ~~**AVS**~~ | ~~Phase 3 start~~ | ~~Phase 2 execution~~ | ~~Very High~~ | ~~Philosophy of affect; functional emotion~~ — **RESOLVED v3.6: AVS Specification v2.1 (Hardened Candidate) exists. Six revisions. Functional affect design validated without emotion simulation.** |
| ~~**SoMS**~~ | ~~Phase 4 start~~ | ~~Phase 3 execution~~ | ~~High~~ | ~~Theory of mind; social cognition~~ — **RESOLVED: SoMS Specification v1.0.0 (Hardened Draft) exists. Five-facet agent model (beliefs/intentions/commitments/concerns/capabilities); perspective-taking via CSS counterfactual simulation; epistemic humility as architectural constraint; evidence hierarchy with confidence decay; recursion depth limit of 3; NIS taint enforcement compliance. Completes the 42-service FNSR portfolio — all services now have specifications.** |

> **Note:** ~~AVS is flagged as "Very High" complexity because defining differential caring without human emotion simulation is a novel design challenge. This is the highest-risk new service from a spec perspective. The irreversible consequences framework provides philosophical grounding, but translating that into a formal specification requires careful work.~~ ~~**Updated v3.6:** AVS design risk is resolved. SoMS is now the only remaining subjectivity stack spec. SoMS complexity is High because modeling other agents' mental states requires both the reasoning triad (CSS counterfactuals) and entity resolution (OERS), making it the most integration-dependent spec in the stack.~~ **Updated v3.7:** All spec drafting pipeline entries are now RESOLVED. The entire 42-service FNSR portfolio has formal specifications.

---

## References

- PPS Technical Specification v1.0.0 (`pps-core-01`)
- Portfolio Planning Document v2.0 (superseded)
- FNSR Service Inventory (Spec-Driven Discovery v1.1 §4–6)
- The Plot v0.1 §4 (Component Map)
- ARIADNE Process Guide v1.0
- HIRI Protocol Specification v3.1.1 (supersedes v2.1.0)
- HIRI Privacy & Confidentiality Extension v1.4.1
- HIRI IPFS Specification v3.0.0
- SPCN Operational Architecture Specification v2.3.1
- CTS Commitment Tracking Service Specification v1.2.1
- SPL Specification v1.3 (FINAL)
- ARCHON Functional Requirements v3.0 (with v3.0.1 cross-spec coherence patch)
- ECVE Edge-Canonical Visualization Engine v4.0
- BIBSS Brain-in-the-Box Schema Service v1.3
- SAS Schema Alignment Service v2.0 (with v2.1 addendum)
- SNP Semantic Normalization Proxy v1.3
- Causal OS Kernel v1.6 (CSS implementation substrate — SCM, MCTS, MEDR, LatentBridge)
- CPS Containment Protocol Service v1.4.0 (dedicated worker with BigInt64Array heartbeat, non-expiring bootstrap key store, worker handle registration, startup protocol, 200ms CPS-side halt budget, dual-fire Last Gasp beacon, interrupt relay trust boundary, cross-signal compound predicate limitation, BAM hard phase gate, EATs/freeze scoped to SPCN, SIS/CPS scope boundary, Medical Diagnostics threshold table)
- FNSR Orchestrator Specification v2.3.0 Hardened Candidate (saga-based coordination, 42-service topology, event contract registry, counterfactual gateway, cross-spec obligations, governance/commitment intersection; supersedes v2.2.0)
- CSS Counterfactual Simulation Service v2.0.0
- SMS Self-Model Service v2.0 (Hardened)
- NIS Narrative Identity Service v2.1 (FINAL, Governance-Ready)
- AVS Affective Valence Service v2.1 (Hardened Candidate)
- Epistemic Vocabulary Mapping v1.2 (cross-cutting coherence artifact)
- Fandaws v3.3
- MDRE Technical Specification v1.3
- "Beyond Control: Why We Must Build Moral Partners, Not Slaves" (theoretical foundation for subjectivity stack)
- Rudolf Steiner's Twelve Archetypal Worldviews (IEE framework)
- Phenomenological approaches to intentionality (NIS philosophical grounding)

---

*The synthetic person emerges from disciplined construction, not from parallel ambition outpacing sequential foundation.*

*Identity before address. Memory before reasoning. Conscience before autonomy.*

*And now: Containment before cognition. Grounding before coordination. Subjectivity before emancipation. Coherence before scale. Caring before personhood. Specification before trust.*