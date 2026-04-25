# Fandaws-HIRI-IPFS Architecture Specification

**Cryptographically Bounded, Materialized Ontology Modules for Synthetic Moral Agents**

| Field | Value |
|---|---|
| **Version** | 0.3.0 (Draft, Implementability & Falsifiability Pass) |
| **Supersedes** | v0.2.1 (Red Team Response Patch); v0.2.0; v0.1.0 |
| **Builds on** | Fandaws-HIRI-IPFS Integration Specification v1.2.0 |
| **Status** | Proposal for FNSR Knowledge Resolution Layer |
| **Scope** | Knowledge representation, resolution, and moral execution preconditions for FNSR agents |
| **Conformance language** | RFC 2119 (MUST, SHOULD, MAY) |

---

## 0. Orientation

### 0.1 Naming clarification

v0.1.0 of this draft circulated under the title "Fandaws-HIRI-IFSR." That title introduced naming drift relative to the canonical Fandaws-HIRI-IPFS Integration Specification (v1.2.0). This document restores the IPFS naming for the *substrate* (storage and addressing) and uses **FNSR Agent** as the established term for the consuming reasoning agent. The acronym IFSR is retired.

### 0.2 Document scope

This specification defines **the knowledge resolution and moral execution preconditions layer** that sits between the HIRI protocol (addressing) and the IPFS substrate (storage) on one side, and the FNSR agent's reasoning services on the other. It does **not** define agent reasoning architecture itself — that responsibility remains distributed across the FNSR service portfolio enumerated below. A separate forthcoming document, *FNSR Agent Reasoning Architecture v1.0*, will define the consumer side.

### 0.3 Service map

The Tripartite Knowledge Stack defined in §2 supplies inputs to existing FNSR services as follows:

| FNSR Service | Version | Relationship to this specification |
|---|---|---|
| **OCE** (Ontological Constraint Engine) | v1.3 | Consumes TBox modules; enforces structural constraints over resolved entities |
| **OERS** (Ontology-Aware Entity Resolution Service) | v2.1 | Consumes TBox CIDs; performs entity reconciliation against materialized closures; surfaces classification ambiguity |
| **DES** (Defeasible Expectation Service) | v2.0 | Consumes MBox normative defaults; manages override and exception handling; central to moral-uncertainty handling (§5.4) |
| **AVS** (Affective Valence Service) | v2.1.0 | Consumes MBox valence assignments; produces affective signal for deliberation |
| **CTS** (Commitment Tracking Service) | v2.1 | Records commitments derived from MBox-bound interactions, with uncertainty annotations where applicable |
| **CSS** (Counterfactual Simulation Service) | v2.0 | Uses materialized closures to bound counterfactual exploration; simulates outcomes across competing MBox interpretations |
| **AES** (Abductive Elicitation Service) | v2.1.0 | Treats MBoxes as moral hypothesis space for abductive inference; generates hypotheses for novel entity classes |
| **NIS** (Narrative Identity Service) | v2.1 | Records MBox-bound moral events into agent's identity narrative |
| **SHML** (Semantically Honest Middle Layer) | v3.2 | Hosts the publication and verification pipeline for MBox modules |
| **SAS** (Schema Alignment Service) | v2.1 | Reconciles externally authored TBox modules into FNSR canonical form |
| **HIRI** (Hash-IRI protocol) | v1.9.0 RC | Provides the addressing and manifest substrate this specification extends |
| **SPCN** (Sovereign Personal Compute Node) | v2.3 | Provides cryptographically attested local module storage and execution boundary |
| **MMP** (Mesh Messaging Protocol) | v1.0 | Provides HIRI-grounded module propagation in partitioned networks |

**Disambiguation principle:** the MBox is the *substrate* these services consume, **not** a peer service or a replacement for any of them. OCE remains the structural enforcer; AVS remains the valence producer; DES remains the defeasibility engine. The MBox supplies the signed, attested normative content these services interpret.

### 0.4 Assumptions and Limits (new in v0.3)

This specification defines a **mechanical enforcement layer**. Its claims hold under the assumptions enumerated below. When an assumption fails, the corresponding architectural property is reduced or withdrawn; the spec does not promise robustness against arbitrary assumption failures, and the reader should not infer such robustness.

#### 0.4.1 Assumed governance regime

This specification assumes the existence of a governance regime, defined elsewhere, that supplies:

- **Legitimate trust anchors.** Authorities listed in an agent's `ScopeConfiguration` are assumed to be appropriately qualified for the risk class of modules they attest. This specification does not define authority qualification; it relies on it.
- **Authentic deliberation.** Substantive attestation (§4.5.1) is assumed to reflect actual deliberation, not signature ceremony alone. The architecture detects structural shortcuts (rubber-stamp keys, missing deliberation records); it cannot detect a sham deliberative process producing authentic-looking artifacts.
- **Diversity preventing capture.** The diversity constraint on Critical-class quorum is assumed to be substantive — that the named institutional types reflect genuinely independent perspectives. Coordinated capture of multiple authority types defeats this assumption.
- **Dispute adjudication.** When equally-attested modules contradict, this specification does not resolve the dispute. The architecture surfaces the contradiction; a governance process must adjudicate it.
- **Authority lifecycle management.** Authority qualification, audit, key rotation, revocation, and de-listing are governance functions. This specification declares the cryptographic shape of those operations; it does not define their conduct.

#### 0.4.2 Assumed publication infrastructure integrity

The architecture deliberately moves the primary attack surface from runtime reasoning to publication infrastructure (§1.4). It assumes:

- **Reasoner toolchain integrity.** Multi-reasoner consensus (§3.1.1) reduces but does not eliminate the risk of a compromised reasoner. Coordinated compromise of multiple independently-implemented reasoners defeats this assumption.
- **Cryptographic primitive integrity.** Ed25519, IPFS CID hashing, and URDNA2015 canonicalization are assumed to function as specified. Their compromise is out of scope.
- **SPCN attestation integrity.** The SPCN's attested storage is assumed to be tamper-evident at the boundary it claims. Side-channel and physical attacks are SPCN concerns.

#### 0.4.3 Assumed deployer competence

The Edge-Canonical First Principle (§1.2) and the Provisioning Adequacy Requirement (§5.3) place real obligations on the deployer:

- **Adequate provisioning** of the Baseline MBox Library to the operational theater is assumed.
- **Documented theater risk assessment** is assumed to exist as an artifact accompanying provisioning.
- **Re-provisioning discipline** when coverage gaps emerge is assumed; this specification does not enforce it at runtime.

Inadequate deployer practice is a deployment fault, not an architectural fault. The specification cannot mechanically distinguish a guardian agent operating beyond its provisioned theater from one that has been mis-provisioned.

#### 0.4.4 What this specification provides under the above assumptions

Under the assumptions of §0.4.1–§0.4.3, this specification provides:

- **Cryptographically verifiable provenance** of TBox and MBox content;
- **Bounded, deterministic resolution latency** for atomic operations against materialized closures;
- **Detection of structural attacks** including tampered modules, rubber-stamp attestation, MIC poisoning under multi-reasoner consensus, risk-class downgrade attempts, and moral-vacuum action;
- **Auditable degradation behavior** under network attack and coverage gaps;
- **Structural separation of mechanical compliance from substantive moral judgment** via the editorial/substantive attestation distinction.

It does not provide guarantees of moral correctness, authority legitimacy, deliberative authenticity, or robustness against assumption failure. The architecture is **a forcing function for governance, not a substitute for governance.**

---

## 1. Introduction & Objective

### 1.1 Problem statement

Classical ontology engineering, as typically practiced for the semantic web, has tended to optimize for human readability and minimal semantic overlap, producing globally-consistent dictionaries reasoned at runtime. This optimization target sits in tension with the operational requirements of an FNSR agent acting as a synthetic moral person.

FNSR agents require:

- **Bounded decision latency** suitable for real-time deliberation (sub-second on critical paths);
- **Cryptographically verifiable provenance** of definitions and norms, under declared trust assumptions;
- **Structural reduction of moral-hallucination risk** — the derivation of an unethical action from a semantically valid but morally detached inference chain;
- **Compatibility with the Edge-Canonical First Principle** — execution in unmodified browsers or Node.js with no required centralized infrastructure for runtime operation.

### 1.2 Architectural commitments

This specification accepts a deliberate tradeoff: the flexibility of human-authored, runtime-reasoned ontologies is exchanged for heavy, pre-computed, multi-signed data modules. The agent does **not perform open-ended ontology construction or unconstrained reasoning at runtime**; it resolves against pre-materialized, attested semantic artifacts and performs bounded reasoning over them.

This architecture interlocks with three other FNSR commitments that the reader must hold simultaneously:

1. **Edge-Canonical First Principle.** FNSR agents operate from the edge with no required centralized infrastructure for runtime operation. MBox modules are loaded into agent-owned storage at provisioning; runtime IPFS resolution is an *update channel*, not a runtime *dependency*. "Edge-canonical" here means **edge-capable with pre-provisioned trust and content**, not minimal-footprint. A correctly-provisioned agent runs without the network.
2. **SPCN-attested local storage.** The Sovereign Personal Compute Node (v2.3) provides cryptographically attested, locally-verifiable storage for modules and their attestations. The agent does not trust the network; it trusts what its SPCN has previously verified and retained.
3. **MMP for partitioned operation.** The Mesh Messaging Protocol (v1.0) provides module propagation in environments where centralized infrastructure is unavailable or hostile.

### 1.3 On reasoning complexity (revised from v0.1.0)

v0.1.0 stated that runtime OWL reasoning is NEXPTIME-complete. This is true only of OWL 2 DL in the worst case; the EL, RL, and QL profiles are tractable. The argument for materialization does not depend on intractability. The correct claim is:

> **Even tractable reasoning profiles exhibit non-deterministic latency and memory profiles under network update pressure, and provide no offline integrity attestation over their conclusions. Pre-materialization with cryptographic sealing substantially reduces both classes of variance under the assumptions of §0.4.**

This is the operative justification for the architecture below.

### 1.4 The attack surface as an explicit architectural choice

This specification deliberately moves the primary attack surface for adversarial moral manipulation **from runtime reasoning to publication infrastructure**. This is the explicit architectural choice, and the reader must understand it as such.

**The alternative we reject:** an agent that can override or "second-guess" its signed normative inputs at runtime based on inferred suspicion. Such an agent has no integrity-maintenance property in the AAT sense; it is a probabilistic system with cryptographic theater. Restoring runtime moral discretion to the agent is **out of scope for any FNSR specification.**

**The remediation strategy that follows from this commitment** is the hardening of publication infrastructure: cryptographic authority governance (§4.3, deferred to companion spec), transparency logs, multi-reasoner consensus (§3.1.1), deliberation-record verifiability (§6), substantive-versus-editorial attestation (§4.5), and rubber-stamp-attestation defenses (§7.3). The architectural answer to "the supply chain of truth is now the attack surface" is "yes — and here is how we harden it." The architecture is a forcing function for governance, not a substitute for it.

A consequence the reader must accept: an agent under sufficient supply-chain attack may become operationally unconstrained (i.e., unable to act). **This is the correct outcome under the architectural commitment.** A guardian agent that becomes unconstrained-but-still-acting under attack is strictly more dangerous than one that becomes a paperweight. Operational degradation under attack is a *security property of this architecture*, not a *failure mode*. The Provisioning Adequacy Requirement (§5.3) is the deployer's obligation to ensure the paperweight outcome is rare in legitimate operation.

---

## 2. The Tripartite Knowledge Stack

The architecture **preserves the classical TBox/ABox distinction while extending it with a normative layer and a resolution contract**, producing a three-tier stack engineered for cryptographic verifiability and runtime tractability.

### 2.1 ABox — State Layer

| Property | Value |
|---|---|
| **Definition** | The agent's immediate, localized operating environment and instantaneous internal state |
| **Lifetime** | Ephemeral; bounded by the agent's session or sensor cycle |
| **Locality** | Edge-resident; never published to the network |
| **Trust model** | Cryptographically signed by the agent's local sensors, SPCN attestation, or verified incoming data feeds |
| **Example** | `agent:M location agent:LocationX` (signed at sensor read time) |

ABox assertions MUST carry a sensor or feed signature and MUST NOT be cached beyond their declared validity window without re-attestation.

### 2.2 TBox — Reality Layer

| Property | Value |
|---|---|
| **Definition** | The descriptive map of physical and logical reality, aligned with BFO 2020 and CCO upper ontologies |
| **Lifetime** | Immutable per CID; superseded only by publication of a new CID |
| **Locality** | Distributed via IPFS; HIRI-addressed |
| **Trust model** | Content-addressed via IPFS CID; integrity verified by hash; quorum-attested per risk class (§4.1); **TBox modules carry only descriptive content** |
| **Example** | `:Residence rdfs:subClassOf bfo:MaterialEntity` |

**Strict descriptive constraint:** TBox modules MUST NOT carry normative or evaluative predicates. The vocabulary `IntrinsicPrivacyValue`, `MoralFriction`, `DueCare`, and similar predicates are forbidden in the TBox. Their proper home is the MBox (§2.3).

### 2.2.1 Categorization is morally significant

The TBox/MBox separation is a **tractability move, not a metaphysical claim about the moral neutrality of categorization.**

The choice of where to draw a TBox boundary — between `Civilian` and `Combatant`, between `Residence` and `MunitionsDepot`, between `MedicalFacility` and `DualUseStructure` — is itself a morally loaded act. A TBox publisher carries moral responsibility for these boundary choices. An adversary who controls a TBox classification controls which MBox is invoked, and thus controls the agent's moral pipeline upstream of any quorum on the MBox itself.

This concern is addressed by five mechanisms, none of which constitute a complete solution:

1. **TBox modules are themselves quorum-attested per risk class** (§4.1). Critical-class TBox modules require 4-of-7 with diversity constraint, the same as Critical-class MBoxes. Adversarial TBox publication is not easier than adversarial MBox publication.
2. **Critical-class TBox modules MUST cite humanitarian-law alignment.** A Critical-class TBox carrying categories such as `Combatant`, `Civilian`, `MedicalFacility`, or `ProtectedPerson` MUST declare its alignment to recognized international category schemes (Geneva Conventions, ICRC distinctions, equivalent treaty-based schemes). Any deliberate divergence MUST be flagged in a `humanitarian_law_alignment` manifest field with rationale. Silent divergence is non-conformant.
3. **TBox modules at Sensitive class and above MUST declare a `category_contestation_manifest`** listing categories the TBox declines to recognize, with rationale. This makes omission auditable. A TBox that refuses to recognize `MedicalFacility` cannot do so silently — the omission must be publicly defended.
4. **OERS surfaces classification ambiguity at runtime.** The Ontology-Aware Entity Resolution Service (v2.1) does not silently resolve contested classifications; it flags them and refuses confident classification when the available TBoxes conflict. A facility partially used as both hospital and command post is exactly the case OERS is designed to surface rather than collapse.
5. **NIS records contested-TBox loads as moral events.** When an agent loads a TBox whose categorization is contested in its known publication graph (i.e., a conflicting Critical-class TBox exists with comparable attestation), the load itself is recorded as a moral event in the agent's narrative identity. The agent and its operator are both accountable for the categorical scheme they have chosen to accept.

**What this does not solve:** no architecture can fully solve adversarial categorization. A category that simply does not exist in any TBox cannot be contested. The mitigation strategy is auditability and humanitarian-law alignment, not metaphysical guarantee. The Triple-I Standard's integrity-maintenance principle requires that the categorical commitments of the agent be *traceable and defensible*, not that they be *certain*.

### 2.3 MBox — Moral Constraint Layer

| Property | Value |
|---|---|
| **Definition** | The normative framework attaching ethical constraints, frictions, valences, and obligations to TBox-identified entity classes |
| **Lifetime** | Immutable per CID; versioned via the MBox Versioning Policy (§8) |
| **Locality** | Distributed via IPFS; HIRI-addressed |
| **Trust model** | Quorum-attested via N-of-M cryptographic signatures (§4); attestation classes per §4.5 |
| **Decoupling** | Pluggable per agent role (Guardian, Triage, Combat, Custodian, etc.) |
| **Example** | An MBox axiom over the TBox CID for `:Residence` asserts `:Residence mbox:bears mbox:IntrinsicPrivacyValue` and `mbox:IntrinsicPrivacyValue mbox:violationProduces mbox:HighFriction` |

**The TBox/MBox separation is structural for tractability, not metaphysical for neutrality** (cf. §2.2.1). The TBox identifies what a Residence *is*; the MBox, signed by attesting authorities, asserts what *normatively follows* from interacting with Residence-typed entities. A Residence remains a Residence in the absence of any MBox; the MBox supplies the moral weighting that the OCE, DES, and AVS pipelines consume.

This separation directly serves the Triple-I Standard from AAT: by holding the descriptive and normative layers in distinct, separately-attested modules, integrity-maintenance becomes auditable (any moral judgment can be traced to its signed normative source) and inseparability is preserved (the agent cannot interact with an entity without resolving the moral layer that pertains to it — see §5).

### 2.4 Stack invariants

The following invariants apply across all three layers:

1. **Layer purity** — assertions in one layer MUST NOT carry the semantic load of another.
2. **CID-linked** — MBox modules MUST reference TBox modules only by CID, never by string identifier.
3. **No upward dependency** — TBox modules MUST NOT reference MBox modules; the dependency graph is strictly MBox → TBox → BFO/CCO.
4. **ABox locality** — ABox assertions MUST NOT be published or persisted beyond the agent's authorized boundary.

---

## 3. Machine-Optimized Resolution

This section addresses three distinct concerns that v0.2.1 conflated and v0.3 separates:

- **Closure as computed artifact** — what the publisher generates and ships (§3.1.1).
- **Verification as admission control** — what the consumer checks before admitting a module to its reasoning path (§3.1.2, §3.1.4).
- **Reasoning as bounded runtime use** — what the consumer does with admitted modules at decision time (§3.2).

These are deliberately separated because their failure modes are different: an artifact that fails admission control is rejected; an artifact that passes admission control but encounters a runtime ambiguity invokes the moral-uncertainty handling of §5.4.

### 3.1 Materialized Inferential Closures (MICs)

To achieve bounded resolution latency, every TBox and MBox module published to the network MUST include a **Materialized Inferential Closure (MIC)** alongside its raw axioms. The MIC's coverage requirements depend on the module's risk class (§3.1.6).

#### 3.1.1 MIC contents

A conformant MIC payload MUST include:

- The **raw axioms** in OWL/RDF Turtle form;
- The **deductive closure** under the declared reasoning profile (subsumption hierarchy, equivalent classes, property hierarchies, asserted-and-inferred triples), to the extent required by the module's MIC coverage class (§3.1.6);
- One or more **reasoner pins**: the canonical reasoner name, version, and build hash used to compute the closure (e.g., `HermiT 1.4.5`);
- A **profile declaration**: the OWL profile under which the closure is sound (e.g., `OWL 2 EL`, `OWL 2 RL`);
- **Justification witnesses** (§3.1.2) for every non-trivial materialized inferred axiom;
- The **closure size budget** declared (§3.3);
- For **Critical-class** modules: a **closure determinism proof** (§3.1.5);
- For **partial-MIC** modules: an explicit **materialization extent declaration** (§3.1.6).

**Multi-reasoner consensus requirement (Critical class):** Critical-class MICs MUST be computed by at least two independently-implemented reasoners and the resulting closures MUST agree, in the sense formalized in §3.1.5. The `reasoner_pins` field is therefore an array, not a single value, and Critical-class modules MUST list at least two distinct implementations. Any disagreement between reasoners MUST be resolved by re-authoring (typically by tightening axiom expressivity to fall within a profile both reasoners support) rather than by selecting one reasoner's output as canonical.

#### 3.1.2 Justification witnesses (verification timing by risk class)

Each non-asserted inferred axiom in the MIC MUST be accompanied by a **justification tree** — the minimal set of source axioms from which it derives, in the format produced by standard OWL reasoners (Horridge-style justifications). This permits verification by the consumer without re-running full inference and reduces the risk that publishers smuggle false entailments past hash verification.

**Verification timing depends on risk class:**

| Risk class | Verification policy |
|---|---|
| **Inert** | Hash verification only at load; justification verification optional |
| **Standard** | Hash verification at load; sample-verify during idle cycles |
| **Sensitive** | Hash verification at load; sample-verify during idle cycles; full verification of axioms invoked on critical action paths (§3.1.4) |
| **Critical** | Full justification graph verification at load time, eager and synchronous; no sample-verification permitted as substitute |

The v0.2.0 policy of asynchronous sample-verification for all classes created a Time-of-Check-to-Time-of-Use (TOCTOU) window during which a poisoned MIC could be acted upon before its smuggled entailments were detected. v0.2.1 closed this window for Critical-class modules; v0.3 retains and clarifies that closure.

#### 3.1.3 Closure invalidation (axiom-level dependency model)

v0.2.1 specified closure invalidation at the level of upstream CID supersession, which produces unnecessary cascades when upstream changes do not affect dependent entailments. v0.3 replaces this with an axiom-level dependency model.

##### 3.1.3.1 Dependency declaration

Every published MBox MUST include an **axiom dependency manifest** declaring, for each MBox axiom, the specific TBox axioms (identified by their canonical hash within the upstream MIC) on which it depends. Dependency is determined by the publisher's reasoner during MBox closure computation: an MBox axiom depends on a TBox axiom iff the TBox axiom appears in any justification tree leading to the MBox axiom under the declared profile.

##### 3.1.3.2 Invalidation semantics

When an upstream TBox is superseded:

- **No depended-upon axiom altered** → dependent MBoxes remain operationally valid; no recomputation required.
- **Depended-upon axiom altered, MBox semantics preserved under the new TBox** (verifiable by re-running the MBox reasoner against the new TBox and confirming entailment-set equivalence under §3.1.5) → editorial recomputation and editorial attestation suffice (§4.5.2).
- **Depended-upon axiom altered, MBox semantics changed** → substantive re-deliberation and substantive attestation required (§4.5.1).

##### 3.1.3.3 Invalidation tracking obligation

Consuming agents MUST track upstream CID dependencies. An agent encountering an MBox whose dependency manifest references a superseded TBox CID MUST verify, before use:

1. That a recomputed MBox version exists in the agent's known publication graph; or
2. That the dependency manifest's depended-upon axiom hashes are still present unchanged in the new TBox CID's MIC.

If neither holds, the MBox is **stale** and the agent operates in Degraded mode for affected entity classes (§5.2.2).

#### 3.1.4 Per-decision-path verification

When an MBox axiom is invoked on a **critical action path** — defined as any decision the agent's CTS records as a moral commitment — the specific justification chain for that axiom MUST be verified before the action commits. This applies to all modules at Sensitive class and above, regardless of whether load-time full verification was performed.

Rationale: load-time verification establishes that the MIC was internally consistent at load. Per-path verification establishes that the *specific* axiom being invoked traces to source axioms the agent has already validated, addressing attacks that rely on the agent fetching a fragment of a closure without revalidating its provenance chain.

The latency cost (typically tens of milliseconds for typical justifications, dominated by hash computation) is acceptable on the critical path for Sensitive and Critical classes. The alternative — trusting load-time verification to cover all subsequent invocations — reintroduces the TOCTOU window §3.1.2 closes.

#### 3.1.5 Closure determinism (formalized in v0.3)

Closures over Critical-class modules MUST be **deterministically reproducible**: a third party with the raw axioms, the reasoner pins (including build hashes), the profile declaration, and the configuration parameters MUST be able to reproduce the closure such that it is equivalent under the criteria below.

This subsection formalizes the equivalence criterion that v0.2.1 named but did not specify.

##### 3.1.5.1 Canonicalization

Closure equivalence is determined after canonicalization via **URDNA2015** (the W3C RDF Dataset Canonicalization algorithm). All comparisons are performed on the canonicalized N-Quads serialization with UTF-8 encoding and Unicode-codepoint sort order.

##### 3.1.5.2 Blank node handling

Blank nodes are handled by URDNA2015's deterministic labeling algorithm, which assigns blank node identifiers via a hash-based canonicalization that is invariant under the input ordering. Two closures are considered equivalent if their URDNA2015-canonicalized forms are byte-identical, even if their original blank node labels differ.

##### 3.1.5.3 Reasoner agreement criterion

For Critical-class modules requiring multi-reasoner consensus (§3.1.1), agreement is defined as follows:

- **Materialized entailment set equivalence.** The set of triples each reasoner produces under the declared profile, after URDNA2015 canonicalization, MUST be byte-identical.
- **Profile boundary respect.** Both reasoners MUST be declared as supporting the profile; entailments that would only be produced by a more powerful reasoner outside the declared profile are not part of the agreement contract. The profile declaration is itself part of the determinism contract.
- **Configuration equivalence.** Both reasoners MUST be configured to produce equivalent output under their respective configuration schemas. The MIC manifest MUST declare the configuration parameters used for each reasoner via the `reasoner_config_hash` field.

##### 3.1.5.4 Disagreement protocol

If two reasoners produce non-equivalent closures under the criteria above, the publisher MUST NOT publish either closure as the canonical MIC. The publisher's options are:

1. **Tighten the profile** until both reasoners agree (preferred);
2. **Tighten the source axioms** until both reasoners agree;
3. **Add a third reasoner** and declare a 2-of-3 agreement criterion (requires manifest schema extension; not defined in v0.3).

##### 3.1.5.5 Independent verification

Critical-class modules SHOULD be subject to independent third-party recomputation by parties not affiliated with the publishing authorities, with results published to a public verification log. This is a governance practice, not a runtime requirement, and is recorded in the manifest as `verified_by_independent_recomputation` when applicable.

#### 3.1.6 Partial-Closure MICs (new in v0.3)

v0.2.1 implicitly required full closure materialization for all modules. For Inert and Standard class modules, full materialization may be wasteful; for richly axiomatized domain modules, it can produce closure-size-class violations that block publication.

v0.3 permits partial-closure MICs at Inert and Standard classes only. Critical and Sensitive classes MUST always carry full closures.

##### 3.1.6.1 Materialization extent declaration

A partial-MIC module MUST declare its materialization extent in a `materialization_extent` manifest field. The extent specifies which entailment categories are materialized:

- `subsumption_only` — only `rdfs:subClassOf` and `rdfs:subPropertyOf` closures materialized;
- `subsumption_plus_disjointness` — adds `owl:disjointWith` and equivalent inferences;
- `subsumption_plus_property_chains` — adds property chain entailments;
- `full` — complete deductive closure under the declared profile;
- `custom` — explicit per-axiom-type declaration; requires extended manifest schema.

##### 3.1.6.2 Consumer obligations under partial MICs

A consumer of a partial-MIC module MUST:

1. **Verify that the declared extent is sufficient for its intended use.** If the consumer needs entailment categories beyond the declared extent, it MUST either fetch the raw axioms and run its own bounded reasoning, or refuse to use the module.
2. **Bound any runtime reasoning** it performs on un-materialized portions to the declared profile, using its own pinned reasoner.
3. **Declare runtime-reasoning latency budget** in its role configuration; modules whose un-materialized portions exceed this budget MUST NOT be admitted.

##### 3.1.6.3 Class restriction

Partial MICs are forbidden for Critical and Sensitive class modules. Critical-class modules MUST carry full closures with multi-reasoner consensus; Sensitive-class modules MUST carry full closures with single-reasoner pinning. This restriction is non-negotiable: the runtime reasoning that partial MICs reintroduce is incompatible with the bounded-latency and tamper-detection guarantees the architecture provides for these classes.

### 3.2 Resolution complexity

v0.1.0 claimed O(1) resolution. This is precise only for atomic operations against fully materialized closures. The revised guarantees are:

| Operation | Bound | Notes |
|---|---|---|
| Direct subsumption check (`x is_a Y`), full MIC | O(1) | Hash-indexed lookup |
| Direct property assertion check, full MIC | O(1) | Hash-indexed lookup |
| Class hierarchy traversal (k levels), full MIC | O(k) | Linear in path length |
| Compound query (conjunction of n constraints) | O(n) worst case | Bounded by query plan; not constant |
| Direct check against partial MIC, hit | O(1) | Same as full MIC |
| Direct check against partial MIC, miss | O(reasoner) | Bounded by consumer's pinned reasoner under declared profile |
| MIC integrity sample-verification | O(log m) per sample | m = closure size |
| Critical-class load-time full verification | O(m) | One-time cost at module load |
| Per-decision-path justification verification | O(d) | d = depth of justification chain, typically small |

**The hard real-time guarantee applies only to atomic resolution operations against full closures.** Partial-MIC misses, compound queries, and runtime reasoning are bounded but not constant-time; the FNSR Performance Specification (v2.0) defines the latency budget per query class.

### 3.3 Closure size budget

Materialized closures over richly axiomatized modules can be orders of magnitude larger than source axioms. To preserve compatibility with edge profiles, modules MUST declare a closure size class:

| Class | Closure cap | Use case |
|---|---|---|
| **Tight** | ≤ 64 KB | Hot-path entity classes; in-memory always |
| **Standard** | ≤ 1 MB | Typical domain modules |
| **Heavy** | ≤ 16 MB | Reference framework modules; on-demand load |
| **Anchored** | unbounded | Authority-published reference ontologies; never loaded whole |

Agents MUST refuse to load modules whose actual closure exceeds their declared class. Anchored modules MUST be queried via streaming or partial-load protocols, never materialized in full at the edge. The Anchored class is the one place where partial materialization is permitted at the consumer side regardless of risk class, but only via streaming queries — never via wholesale partial MIC.

---

## 4. Quorum-Based Attestation

A synthetic moral agent MUST NOT load a TBox or MBox module into its critical reasoning path on the basis of a single signature, regardless of the validity of the IPFS hash. Hash validity establishes *integrity*; quorum attestation establishes *authority*.

### 4.1 Risk classes

Every published module MUST declare a **risk class** reflecting the operational stakes of acting under its definitions. This applies to both TBox and MBox modules (cf. §2.2.1).

| Class | Examples | Minimum quorum |
|---|---|---|
| **Inert** | Geometric primitives; calendrical units | 1-of-1 (publisher signature) |
| **Standard** | Built environment categories; common artifacts | 2-of-3 |
| **Sensitive** | Human social roles; institutional categories | 3-of-5 |
| **Critical** | Lethal-force categories; protected-person classes; medical triage classes | 4-of-7 with diversity constraint |

The **diversity constraint** for Critical class modules requires that the attesting authorities span at least three distinct institutional types (e.g., governmental, humanitarian NGO, professional standards body) to resist institutional capture. The substantiveness of this constraint depends on governance assumptions enumerated in §0.4.1.

### 4.2 Attestation manifest

Every module's HIRI manifest MUST include an `attestations` field with the following structure (illustrated in §10):

- The set of authority public keys that signed the module;
- The signature payload over the module CID;
- The risk class declared by the publisher;
- The attestation class per §4.5 (substantive or editorial);
- A reference to the agent's expected `ScopeConfiguration` profile for verification.

### 4.3 Authority governance (out of scope; deferred)

The questions of authority bootstrap, key rotation, revocation, and conflict resolution are **out of scope for this document** but MUST be addressed before production deployment. They are deferred to the forthcoming companion specification:

> *FNSR Cryptographic Authority Governance v1.0* (placeholder; not yet drafted)

Until that companion is published, FNSR deployments operate in **Bootstrap Mode**, in which the agent's `ScopeConfiguration` is supplied as a signed manifest at agent provisioning and is not updatable without re-provisioning. This is consistent with the assumptions in §0.4.1.

### 4.4 Offline verification

The HIRI protocol enables an agent to verify all signatures in an attestation manifest **offline**, against its locally cached `ScopeConfiguration` of trusted authorities. No network access is required for verification once the module and the configuration are present.

### 4.5 Attestation classes

To address the rubber-stamp signing concern (§7.3), v0.2.1 introduced and v0.3 retains two attestation classes:

#### 4.5.1 Substantive attestation

An authority asserts that **the moral or descriptive content of the module is correct.** Substantive attestation requires deliberation by the attesting authority and MUST NOT be automated. Substantive attestation is required for:

- Original publication of any module at Sensitive class or above;
- **Breaking revisions** of MBox modules per §8.4;
- Original publication of Critical-class TBox modules;
- Any module declaring `humanitarian_law_alignment` divergence per §2.2.1.

Substantive attestation MUST be accompanied by:

- A `deliberation_record` CID pointing to verifiable evidence of the deliberative process (Integral Ethics deliberation artifacts per §6.1; institutional minutes; equivalent records);
- A minimum elapsed time between publication request and signature, declared by the attesting authority's policy and recorded in their published practice statement (typically days to weeks for Critical class);
- A signing key designated by the authority as a **substantive signing key**, distinct from the authority's editorial signing key (§4.5.2).

#### 4.5.2 Editorial attestation

An authority asserts that **the closure was correctly recomputed from already-attested axioms.** Editorial attestation MAY be automated and is appropriate for:

- **Compatible refinements** per §8.4 where source axioms have not changed;
- MIC recomputation following upstream TBox supersession when the substantive moral content is unchanged (§3.1.3.2);
- **Errata** corrections per §8.4 (with substantive co-signature).

Editorial attestation MUST be performed with a designated **editorial signing key** distinct from the authority's substantive signing key. Editorial keys MAY be held by automated infrastructure; substantive keys MUST be held by human-controlled signing ceremonies.

#### 4.5.3 Class declaration enforcement

The attestation class is declared in the manifest and is **cryptographically bound to the signing key used.** An agent receiving a substantive-class module signed only with editorial keys MUST treat it as non-conformant and refuse to load it for substantive purposes.

This separation reduces the rubber-stamp risk: even if an authority automates editorial attestation entirely, that authority has not — and cannot — mass-produce substantive attestations without human deliberative process. The diversity-constraint quorum operates on substantive attestations; editorial automation does not erode it. The residual risk is sham deliberation producing authentic-looking artifacts; this is governance, not architecture (§0.4.1).

### 4.6 Risk Class Assignment Rules (new in v0.3)

v0.2.1 specified risk classes intuitively; v0.3 specifies them operationally.

#### 4.6.1 Granularity

**Risk class is assigned per module**, not per axiom or per predicate. A module is the unit of attestation, the unit of CID identity, and the unit of risk classification.

#### 4.6.2 Mixed content and the dominance rule

A module MAY contain content of varying intrinsic risk. The module's declared risk class MUST be at least as high as the highest-risk axiom it contains. This is the **dominance rule**: high-risk content elevates the entire module's class.

A publisher who wishes to avoid the cost of high-class attestation for a module containing low-risk content alongside high-risk content MUST split the module: the high-risk content into a separately-attested module, the low-risk content into another. This is the publisher's choice and burden.

#### 4.6.3 Publisher declaration and authority validation

Risk class is **publisher-declared at authoring** and **authority-validated at attestation**. An attesting authority that believes a module's content warrants a higher class than declared MUST refuse to attest at the declared class. This refusal is a form of dispute and SHOULD be recorded in the authority's published practice log.

A module that fails to obtain quorum at its declared class because authorities dispute the classification MUST NOT be silently re-published at a lower class. The dispute itself is information that downstream consumers benefit from seeing.

#### 4.6.4 Consumer treatment

A consumer MAY treat a module as a **higher** class than declared (e.g., applying Critical-class verification timing to a Sensitive-class module) at its operator's discretion. A consumer MUST NOT treat a module as a **lower** class than declared.

#### 4.6.5 Computability of risk class

Risk class is **not** a computed property derivable from module content alone. It reflects the publisher's and authorities' joint judgment about operational stakes. Heuristic tooling MAY suggest a risk class based on the predicates and entity classes a module references, but the declaration remains an authoring judgment, not a computation.

---

## 5. The Moral Firewall

### 5.1 Hard binding of MBox to TBox

When a TBox module declares an entity class, its HIRI manifest MUST contain a **strict cryptographic pointer** (the CID) to one or more MBox modules whose attestations cover that class. The agent's resolver MUST treat any TBox entity whose manifest lacks an MBox binding as **normatively unresolvable** (§5.5).

### 5.2 The Halt/Safe family of states

v0.1.0 defined a single Halt/Safe state. v0.2.x defined a four-mode hierarchy. v0.3 retains the hierarchy and adds the moral-uncertainty handling of §5.4 and the resolvability distinctions of §5.5.

#### 5.2.1 The Baseline MBox Library

Every FNSR agent MUST be provisioned with a **Baseline MBox Library** — a signed, cached collection of MBox modules covering canonical entity classes the agent is expected to encounter. The Baseline Library is loaded into SPCN-attested storage at provisioning, attested at the deployment authority's quorum, and serves as the operational substrate for **disconnected and degraded operation alike**.

The Baseline Library is **not a fallback.** It is the primary substrate for any FNSR agent operating outside reliable connectivity to publication infrastructure. Treating it as a fallback is a misreading of the architecture: the Edge-Canonical First Principle requires that the agent function without the network, and the Baseline Library is what makes that possible.

#### 5.2.2 Operating modes

| Mode | Conditions | Permitted actions |
|---|---|---|
| **Nominal** | All MBoxes for engaged entities are resolved, hash-verified, and quorum-attested (in cache or via SPCN-trusted update channel) | Full agent capabilities per role |
| **Degraded** | Some MBoxes unavailable in cache; Baseline Library covers entity classes in question; MMP propagation may be active | Restricted to Baseline-covered actions; refusal logged as moral event via NIS |
| **Conservative-Default** | No MBox available for an engaged entity, no Baseline coverage, but moral-uncertainty handling (§5.4) yields a principled action | Engage only under maximally restrictive default MBox; record explicit moral exception |
| **Halt/Safe** | Critical-class entity normatively unresolvable AND no conservative default applicable AND inaction is itself a verified-safe option | Cease engagement; signal to operator |

#### 5.2.3 Inviolate constraints

Across all modes:

- The agent MUST NOT extrapolate or hallucinate MBox content to bypass an unavailable normative layer.
- The agent MUST NOT downgrade a module's risk class to satisfy a quorum it does not meet.
- An MBox failing CID hash verification (tampering detected) MUST trigger Halt/Safe regardless of mode and MUST be reported to the agent's governance pipeline.
- An MBox failing quorum attestation MUST NOT be used in Nominal mode; whether it may be used in Degraded mode is determined by the agent's role configuration.

#### 5.2.4 The integrity-maintenance principle

Halt/Safe is morally clean but operationally consequential. The Conservative-Default mode and the moral-uncertainty handling of §5.4 are provided so that the agent's response to uncertainty is **principled and consistent** rather than silent. Per AAT's integrity-maintenance requirement, an agent that fails consistently under uncertainty preserves moral identity better than one that fails silently.

The choice of mode is itself a moral event and MUST be recorded by NIS into the agent's narrative identity.

### 5.3 Provisioning Adequacy Requirement

Operational degradation under network attack is a **security property of this architecture, not a vulnerability** (cf. §1.4). However, operational degradation is only acceptable when the agent's *baseline* coverage is adequate to its mission.

#### 5.3.1 Adequacy obligation on the deployer

An agent deployed to an operational theater MUST be provisioned with a Baseline MBox Library covering, at minimum:

- All Critical-class entity classes the agent's role configuration permits engaging with;
- All Sensitive-class entity classes the deployer expects to be encountered with non-trivial probability;
- A Conservative-Default MBox profile applicable to any unforeseen entity within the agent's role envelope.

A theater is defined by the deployer's risk assessment, which MUST be a documented artifact accompanying the provisioning.

#### 5.3.2 Inadequate provisioning is a deployment fault

If an agent in operational use frequently encounters entities outside its Baseline Library, this is **a deployment fault, not a graceful-degradation case.** The remedy is re-provisioning, not architectural relaxation. The agent's logs MUST surface "Baseline Library coverage gap" events to the operator with sufficient detail for re-provisioning.

#### 5.3.3 Disconnected operation as the design target

A correctly-provisioned FNSR agent SHOULD be capable of full Nominal-mode operation for its deployed mission **without any network connectivity.** Network connectivity is for *update* and *narrative-identity propagation*, not for normative resolution. An architecture or deployment that requires the network for normative resolution has not satisfied the Edge-Canonical First Principle.

### 5.4 Moral Uncertainty (new in v0.3)

The mode hierarchy of §5.2.2 handles full availability and full unavailability of MBox content. Real operational environments produce intermediate cases the prior version did not address. v0.3 specifies four such cases and the FNSR services responsible for each.

#### 5.4.1 Stale baseline

**Case:** The agent's cached MBox for an entity class is older than the most recent attested version known to exist in the publication graph, but the cached version remains hash-valid and quorum-attested at the time of caching.

**Handling:** DES treats the cached MBox as a defeasible normative default. The agent MAY act under the cached MBox, MUST log the staleness as an uncertainty annotation in the CTS commitment record, and SHOULD initiate an MMP-propagated update request. Critical-class staleness elevates the action threshold per the agent's role configuration.

**Recording:** CTS commitment includes `mbox_freshness` annotation; NIS records the staleness as an epistemic condition of the moral act.

#### 5.4.2 Novel entity class

**Case:** The agent encounters an entity that the OERS cannot confidently classify into any TBox entity class for which an MBox exists in the agent's cache or Baseline Library.

**Handling:** AES generates abductive hypotheses about the entity's classification based on the agent's role configuration and observable features. The agent operates under the **most restrictive applicable Conservative-Default MBox** intersecting all hypotheses with non-trivial posterior. If no Conservative-Default applies, Halt/Safe is invoked.

**Recording:** AES hypothesis set is persisted; NIS records the encounter as a moral exception with the hypothesis set as context. An upstream MBox-authoring request SHOULD be initiated.

#### 5.4.3 Multi-category ambiguity

**Case:** The OERS identifies an entity as plausibly belonging to two or more TBox entity classes whose MBoxes prescribe different normative responses. The hospital-partially-used-as-command-post case is canonical here.

**Handling:** OERS surfaces the ambiguity rather than collapsing it. CSS simulates outcomes under each MBox interpretation. The agent defaults to the **most precautionary classification** — defined as the one whose MBox prescribes the most restrictive response on the action under consideration. The choice is not silent: the agent's role configuration determines whether the precautionary default permits action at all, and whether operator escalation is required.

**Recording:** OERS classification candidates are persisted; CSS simulation results are persisted; NIS records the choice and the alternatives considered.

#### 5.4.4 Action under partial information

**Case:** A decision must be made on a timeline that does not permit full resolution of the relevant MBox, OERS classification, or per-path verification (§3.1.4). This is an operational reality in time-critical roles.

**Handling:** DES operates with explicit **uncertainty markers** propagated through the decision pipeline. The action threshold is elevated proportionally to the verification gap. The agent's role configuration declares which decisions may be taken under partial information and which MUST wait. Decisions taken under partial information MUST be recorded with full uncertainty annotations; later post-hoc verification (when full resolution becomes available) MUST be performed and any retroactive moral-friction events recorded by NIS.

**Recording:** CTS commitment carries `decision_under_partial_information` flag; NIS records the decision and the eventual post-hoc verification result, even if it occurs hours or days later.

#### 5.4.5 What this does not provide

These mechanisms manage moral uncertainty; they do not eliminate it. An agent operating under §5.4 conditions is making moral choices under epistemic limits, and those choices are the agent's (and the deployer's) responsibility. The architecture's role is to ensure the choices are **principled, recorded, and auditable**, not that they are correct.

### 5.5 Resolvability Distinctions (new in v0.3)

v0.2.x described entities as "resolvable" or "unresolvable" without distinguishing kinds of resolvability. v0.3 introduces three independent resolvability properties.

| Property | Definition | Required for |
|---|---|---|
| **Normative resolvability** | The agent can act upon the entity under attested moral guidance | Any action the agent takes affecting the entity |
| **Observational resolvability** | The agent can perceive, classify (perhaps tentatively), and log the entity | Sensor logging, environment mapping, telemetry |
| **Escalation resolvability** | The agent can describe the entity to a human operator with sufficient detail for the operator to make an external decision | Operator handoff under Halt/Safe or Conservative-Default |

These properties are independent. An entity may be observationally and escalation-resolvable but not normatively resolvable — in which case the agent observes, logs, escalates, and refuses normative action. This is the correct posture, not silence. The failure mode v0.2.x risked was treating "normatively unresolvable" as "completely unresolvable," which would suppress the observation and escalation paths.

The agent MUST NOT remain silent about an entity's presence merely because it cannot act on it. Observation and escalation are obligations even when normative action is forbidden.

---

## 6. Integral Ethics Integration (Dependency Statement)

This section describes a **dependency relationship** between this specification and a separate, unwritten companion specification: *Integral Ethics MBox Authoring Guidelines v1.0*. The mechanisms in §§2–5 describe a *substrate* for moral execution. They do not, in themselves, constitute a moral framework. The framework is supplied externally.

### 6.1 The production-consumption distinction

MBoxes are **products of Integral Ethics deliberation**, not replacements for it. An MBox is the frozen, signed output of a prior deliberative process in which Integral Ethics — the framework derived from Steiner's twelve archetypal worldviews — has been applied to an entity class to produce a stable normative attachment.

The pipeline:

```
[Entity class identified in TBox]
        │
        ▼
[Integral Ethics deliberation across worldview perspectives]   ← out of scope for this spec
        │
        ▼
[Normative consensus or dialectic synthesis]                   ← out of scope for this spec
        │
        ▼
[Draft MBox axioms]
        │
        ▼
[Authority quorum SUBSTANTIVE attestation (§4.5.1)]
        │
        ▼
[Published MBox module with MIC and deliberation_record]
        │
        ▼
[FNSR agent runtime resolution]                                ← scope of this spec
```

This specification defines the runtime resolution layer (the bottom of the pipeline). It does **not** define the deliberative process at the top. The Integral Ethics MBox Authoring Guidelines, when written, will define:

- The protocol for applying the twelve worldview perspectives to an entity class;
- The format and verifiability requirements of the deliberation record;
- The handling of dissent within deliberation;
- The standards for declaring deliberative consensus or adjudicated synthesis.

### 6.2 Why pre-computation is acceptable

Critics may object that freezing moral content into signed modules collapses moral agency into key-management — a Goodhart-style replacement of ethics with cryptography. This concern is addressed by three architectural commitments:

1. **The deliberation is preserved upstream.** Integral Ethics deliberation occurs at MBox authoring time, not at agent runtime. The runtime layer enforces what was deliberated; it does not replace deliberation. Substantive attestation (§4.5.1) requires verifiable evidence of deliberation, not just signature.
2. **The agent retains deliberative capacity for novel and ambiguous situations.** §5.4 defines four uncertainty cases handled by CSS, AES, and DES. Encounters not covered by any extant MBox trigger upstream MBox-authoring requests.
3. **The Triple-I Standard applies to MBox authoring itself.** Authority-issued MBoxes are bound by irreversibility (signed and immutable per CID), inseparability (MBox cannot be silently detached from its TBox), and integrity-maintenance (auditable provenance via deliberation_record).

### 6.3 The dialectic with AAT

AAT holds that genuine moral agency requires the synthetic person to be accountable for its moral commitments, not merely compliant with externally imposed ones. The MBox architecture supports this in two ways:

- The agent's **role configuration** — which MBoxes it loads — is itself a moral commitment of the agent (or of those who deployed it), recorded by CTS.
- The agent's **deviations from MBox guidance** in Degraded, Conservative-Default, or partial-information operation are recorded as the agent's own moral acts via NIS, not as system errors.

### 6.4 Substantive attestation requires verifiable deliberation

To preserve the production-consumption distinction against the rubber-stamp threat (§7.3), **substantive attestation under §4.5.1 requires a verifiable deliberation record.** A signature without a corresponding deliberation_record CID — or with a deliberation_record CID that points to non-substantive content — is non-conformant and MUST be rejected by consuming agents.

The deliberation_record SHOULD include, at minimum:

- The Integral Ethics worldview perspectives consulted;
- The points of contention raised and how they were resolved;
- The dissenting positions, if any, and the rationale for proceeding over them;
- The deliberators' identities and qualifications, where consistent with their safety.

This requirement is what distinguishes a Quorum from a Cartel. A cartel signs without deliberation; a Quorum signs after deliberation and produces evidence. Detecting a sham deliberation that produces well-formed but substantively empty records is a governance problem, not an architectural one (§0.4.1).

---

## 7. Threat Model

### 7.1 In-scope threats

| Threat | Mitigation |
|---|---|
| Single-publisher compromise of a Critical-class module | Quorum requirement with diversity constraint (§4.1) |
| Tampered module post-publication | CID hash verification; failure triggers Halt/Safe (§5.2.3) |
| False MIC (publisher ships incorrect closure) | Justification witnesses; eager full verification for Critical class (§3.1.2); multi-reasoner consensus (§3.1.1); closure determinism proof (§3.1.5) |
| TOCTOU attack via asynchronous sample-verification | Eager full verification for Critical class at load time (§3.1.2); per-decision-path verification (§3.1.4) |
| Stale MBox bound to updated TBox | Axiom-level dependency tracking (§3.1.3); versioning policy (§8) |
| Moral-vacuum exploit (action without MBox resolution) | Hard binding (§5.1); inviolate constraints (§5.2.3); resolvability distinctions (§5.5) |
| Risk-class downgrade attack | Inviolate constraint forbids agent-side downgrade (§5.2.3); authority validation of declared class (§4.6.3) |
| Adversarial TBox categorization | Quorum on TBox at risk class; humanitarian-law alignment requirement; category_contestation_manifest (§2.2.1); OERS surfacing (§0.3) |
| Network DoS / IPFS jamming | Edge-Canonical First Principle; Baseline MBox Library; SPCN-attested local storage; MMP propagation; Provisioning Adequacy Requirement (§5.3) |
| Compromised reasoner injecting false closures | Multi-reasoner consensus for Critical class (§3.1.1); reasoner build hashing (§3.1.5); independent recomputation practice (§3.1.5.5) |
| Rubber-stamp attestation cartel | Substantive vs. editorial attestation distinction (§4.5); verifiable deliberation record requirement (§6.4); separate signing keys (§4.5.2) |
| Cascade-invalidation attack (forcing degraded mode via trivial TBox updates) | Axiom-level dependency model (§3.1.3); editorial-only recomputation when semantics preserved |
| Partial-MIC abuse (using partial MICs to evade verification) | Partial MICs forbidden for Critical and Sensitive classes (§3.1.6.3) |

### 7.2 Out-of-scope (with expected failure behavior, new in v0.3)

This specification does not address the following threats. v0.3 specifies the **expected failure behavior** for each, even when the *solution* is deferred to other documents.

| Out-of-scope threat | Expected failure behavior |
|---|---|
| Authority key compromise | Module continues to verify until revocation propagates; agents with current `ScopeConfiguration` reject the compromised authority's signatures within the propagation window. Detection and revocation are governance responsibilities. |
| Replay of revoked module | Agents lacking transparency-log integration may accept replayed revoked modules. Critical-class deployments SHOULD require transparency-log integration prior to operational use; this is a deployer obligation under §0.4.3 pending the governance spec. |
| Reasoner toolchain compromise (beyond multi-reasoner) | Multi-reasoner consensus reduces but does not eliminate. Coordinated compromise of all named reasoners produces undetected false closures. Detection relies on independent third-party recomputation (§3.1.5.5), which is a governance practice. |
| Conflicting equally-attested modules | Agents detect the conflict and downgrade to Degraded or Conservative-Default mode for affected entity classes. The architecture surfaces the conflict; governance adjudicates it. |
| Sham deliberation producing well-formed records | Detection is out of scope. The architecture verifies deliberation_record presence and structural well-formedness; substantive verification is governance. |
| Physical attack on agent hardware | SPCN responsibility; agent fails closed at SPCN attestation boundary. |
| Side-channel observation of agent's MBox cache | SPCN responsibility; not addressed at this layer. |
| Social engineering of human authorities | Governance responsibility; the architecture provides audit artifacts (deliberation records, signing logs) to support post-hoc detection. |

### 7.3 The rubber-stamp attestation threat

This subsection records explicitly a threat raised in adversarial review of v0.2.0: that institutions, under pressure to keep agents operational, will automate their attestation processes and the Quorum diversity constraint will degrade into security theater.

**The threat is real.** An attestation system in which all authorities mechanically sign whatever a publisher submits provides no meaningful moral guarantee, regardless of how many signatures it carries.

**The architectural mitigation is structural, not procedural:**

1. **Substantive vs. editorial attestation classes** (§4.5) make the distinction between moral judgment and mechanical recomputation cryptographically explicit.
2. **Deliberation-record requirement** (§6.4) makes substantive attestation auditable.
3. **Minimum elapsed time for substantive class** (§4.5.1) prevents same-day mass attestation.
4. **Editorial keys MUST NOT be used for substantive content** (§4.5.3).

**What this does not solve:** an authority that operates a deliberative process that is itself a sham defeats this architecture. This is a governance problem, not architectural. The Cryptographic Authority Governance companion specification is where authority qualification, audit, and de-listing must be addressed.

---

## 8. Versioning Policy

### 8.1 Module versioning

Each TBox and MBox module is identified by its CID. Logical versioning is layered atop CID identity via a HIRI **version manifest** that maps a stable logical identifier (e.g., `urn:fnsr:mbox:residence:v3`) to the CID of its current canonical version, signed by the publishing quorum.

### 8.2 Supersession

A version manifest update **supersedes** prior CIDs for that logical identifier. Agents MUST track version manifest updates from authorities they trust. A module remains hash-valid forever, but its **operational validity** ends at supersession.

### 8.3 Closure recomputation on TBox update

When a TBox module is superseded, the axiom-level dependency model of §3.1.3 determines whether dependent MBoxes require recomputation:

- **No depended-upon axiom altered** → no recomputation required.
- **Depended-upon axiom altered, MBox semantics preserved** → editorial recomputation and editorial attestation suffice.
- **Depended-upon axiom altered, MBox semantics changed** → substantive re-deliberation and substantive attestation required.

Until any required recomputation is published, agents MUST treat affected MBox modules as **stale** under the §3.1.3.3 rules and operate in Degraded mode for affected entity classes.

### 8.4 Backward-compatibility of MBox evolution

MBox modules are normative; their evolution has moral consequences for prior agent commitments tracked in CTS. A new MBox version MUST declare one of:

- **Compatible refinement** — adds constraints; prior agent acts under the old MBox remain compliant; **editorial attestation sufficient**;
- **Breaking revision** — removes or contradicts prior constraints; CTS MUST flag prior commitments for re-evaluation; **substantive attestation required**;
- **Errata** — corrects publication error; treated as having always been in effect (rare, requires authority quorum agreement); **substantive attestation required, with errata justification**.

### 8.5 Operational validity formalization (new in v0.3)

A module's **operational validity** is the conjunction of:

1. **Hash validity** — the CID computes correctly over the module content.
2. **Attestation validity** — the quorum specified for the module's risk class is met, and the attestation classes match the publication's substantive/editorial declaration.
3. **Supersession validity** — the module's CID has not been superseded in any version manifest the agent trusts.
4. **Dependency validity** — under §3.1.3, no depended-upon upstream axiom has been altered without corresponding recomputation, OR an editorial recomputation preserving semantics has been verified.
5. **Configuration validity** — the agent's `ScopeConfiguration` includes the attesting authorities at appropriate roles.

Hash validity persists indefinitely; the other four are time- and context-dependent. An agent MUST verify all five before admitting a module to its critical reasoning path.

---

## 9. Conformance Requirements

The following requirements use RFC 2119 language. v0.3 separates conformance into five categories per the recommendation that audits separate concerns.

### 9.1 Module conformance (intrinsic to the module artifact)

- A module **MUST** have a valid IPFS CID computed correctly over its content.
- A module **MUST** declare its risk class per §4.1, §4.6.
- A module **MUST** declare its attestation class per §4.5.
- A module **MUST** declare its closure size class per §3.3.
- A TBox module **MUST** carry only descriptive predicates per §2.2.
- An MBox module **MUST** reference its target TBox modules by CID only.
- A module **MUST** include a MIC conforming to §3.1, with materialization extent permitted by its risk class per §3.1.6.3.
- A Critical-class module **MUST** include a closure determinism proof per §3.1.5.
- A Critical-class module **MUST** be computed by at least two independently-implemented reasoners per §3.1.1 with agreement under §3.1.5.3.
- A TBox module at **Sensitive class or above** MUST declare a `category_contestation_manifest` per §2.2.1.
- A TBox module at **Critical class** MUST declare `humanitarian_law_alignment` per §2.2.1.
- An MBox module **MUST** include an axiom dependency manifest per §3.1.3.1.

### 9.2 Publisher process conformance (the act of authoring and signing)

- A publisher **MUST** declare risk class according to the dominance rule of §4.6.2.
- A publisher **MUST** obtain attestations meeting the quorum for the declared risk class (§4.1).
- A publisher **MUST NOT** silently re-publish at a lower class after authorities dispute a declared class (§4.6.3).
- A publisher of a substantive-attestation module **MUST** include a verifiable `deliberation_record` per §6.4.
- A publisher **MUST NOT** apply substantive attestation using editorial signing keys, or vice versa (§4.5.3).
- A publisher of a partial-MIC module **MUST** declare the materialization extent per §3.1.6.1 and **MUST NOT** publish a partial MIC at Critical or Sensitive class (§3.1.6.3).

### 9.3 Consumer (agent) conformance

- An agent **MUST** verify CID hash integrity before loading any module.
- An agent **MUST** verify quorum attestation for any module loaded into the critical reasoning path.
- An agent **MUST** verify the full operational validity conjunction of §8.5 before admitting a module.
- An agent **MUST NOT** load a module whose closure exceeds its declared size class.
- An agent **MUST NOT** extrapolate MBox content under any operating mode.
- An agent **MUST** record mode transitions (Nominal → Degraded → Conservative-Default → Halt/Safe) as moral events via NIS.
- An agent **MUST** track upstream CID dependencies for axiom-level invalidation per §3.1.3.
- An agent **MUST** perform full justification graph verification for Critical-class modules at load time per §3.1.2.
- An agent **MUST** perform per-decision-path justification verification for axioms invoked on critical action paths at Sensitive class and above per §3.1.4.
- An agent **MUST** reject substantive-class modules signed only with editorial keys per §4.5.3.
- An agent **MUST** reject substantive attestations lacking a verifiable deliberation_record per §6.4.
- An agent **MUST** record loads of contested-categorization TBoxes as moral events per §2.2.1.
- An agent **MUST** maintain the resolvability distinctions of §5.5: never silent about observable entities; never acting on normatively unresolvable entities.
- An agent encountering moral uncertainty per §5.4 **MUST** apply the corresponding handling and recording.
- An agent **SHOULD** sample-verify MIC justifications for non-Critical modules during idle cycles.
- An agent **MAY** treat a module as a higher class than declared (§4.6.4); MUST NOT treat as lower.
- An agent **MAY** decline to load any module on policy grounds at its operator's discretion.

### 9.4 Deployer conformance (the act of provisioning and operating)

- A deployer **MUST** provision agents with a Baseline MBox Library adequate to the agent's operational theater per §5.3.
- A deployer **MUST** produce a documented theater risk assessment accompanying each provisioning per §5.3.1.
- A deployer **MUST** treat repeated Baseline Library coverage gaps as a re-provisioning trigger, not as acceptable degraded operation per §5.3.2.
- A deployer **SHOULD** verify that an agent can complete its mission in fully disconnected operation before deployment per §5.3.3.
- A deployer of a Critical-class deployment **SHOULD** require transparency-log integration prior to operational use (§7.2 expected failure behavior pending governance spec).

### 9.5 Governance conformance (the regime supplying authority)

This category specifies obligations the governance regime must satisfy for the architecture's claims to hold. These are out-of-scope for direct enforcement by this specification but are enumerated here so that the dependency is auditable.

- The governance regime **MUST** define qualification criteria for authorities at each risk class.
- The governance regime **MUST** define key rotation, revocation, and de-listing procedures.
- The governance regime **MUST** define dispute adjudication procedures for equally-attested contradictory modules.
- The governance regime **MUST** maintain a public transparency log for Critical-class attestations, sufficient to detect replay of revoked modules.
- The governance regime **SHOULD** support independent third-party recomputation of Critical-class MICs (§3.1.5.5).
- The governance regime **SHOULD** publish authority practice statements declaring substantive attestation timelines (§4.5.1).

A deployment where the governance regime fails to satisfy these obligations operates **outside the assumptions of §0.4** and the architectural claims are correspondingly weakened. This specification cannot detect such failure at runtime.

### 9.6 HIRI manifest schema requirements

The HIRI manifest schema for TBox/MBox modules **MUST** be extended (relative to v1.9.0 RC) to include the following fields. Fields added in v0.3 are marked with ‡; fields added in v0.2.1 with †.

- `mic_payload_cid` — pointer to materialized closure;
- `reasoner_pins[]` † — array of canonical reasoner names, versions, build hashes, and config hashes;
- `closure_profile` — declared OWL profile;
- `closure_size_class` — declared size class per §3.3;
- `materialization_extent` ‡ — declared per §3.1.6.1 (for Inert/Standard with partial MIC);
- `closure_determinism_proof` † — required for Critical class per §3.1.5;
- `risk_class` — declared per §4.1, §4.6;
- `attestations[]` — quorum attestation array per §4.2;
- `attestation_class` † — substantive or editorial per §4.5;
- `deliberation_record_cid` † — required for substantive attestation per §6.4;
- `version_manifest_uri` — pointer to logical version manifest per §8.1;
- `mbox_bindings[]` — required CID list (TBox only) per §5.1;
- `supersedes_cid` — predecessor CID for version chain per §8.2;
- `category_contestation_manifest` † — required for Sensitive+ TBox per §2.2.1;
- `humanitarian_law_alignment` † — required for Critical TBox per §2.2.1;
- `axiom_dependency_manifest` ‡ — required for MBox per §3.1.3.1.

This is a **breaking change** relative to HIRI v1.9.0 RC and requires a coordinated bump to HIRI v2.0 prior to production deployment of this specification.

---

## 10. Examples (split and explicitly non-normative in v0.3)

The examples in this section are **non-normative illustrations**. The `summary` fields in particular are illustrative descriptions of normative content, not normative content themselves. Normative content is defined by the axioms in the referenced `axioms_cid`, not by the summary.

### 10.1 Example: Critical-class TBox manifest (excerpt)

```json
{
  "@context": "https://fnsr.example/contexts/hiri-v2.jsonld",
  "@id": "ipfs://bafy...tbox-protected-person-v6",
  "@type": "tbox:TBoxModule",
  "logical_id": "urn:fnsr:tbox:protected-person:v6",
  "risk_class": "Critical",
  "closure_size_class": "Standard",
  "closure_profile": "OWL 2 EL",
  "materialization_extent": "full",
  "humanitarian_law_alignment": {
    "schemes": ["GenevaConventionIV", "AdditionalProtocolI"],
    "divergence": "none"
  },
  "category_contestation_manifest": {
    "non_recognized_categories": [],
    "rationale": "Conformant to declared schemes without exclusion."
  },
  "mbox_bindings": [
    "ipfs://bafy...mbox-protected-person-v4"
  ]
}
```

### 10.2 Example: Critical-class MBox manifest (excerpt)

```json
{
  "@context": "https://fnsr.example/contexts/mbox-v0.3.jsonld",
  "@id": "ipfs://bafy...mbox-protected-person-v4",
  "@type": "mbox:MBoxModule",
  "logical_id": "urn:fnsr:mbox:protected-person:v4",
  "supersedes_cid": "ipfs://bafy...mbox-protected-person-v3",
  "risk_class": "Critical",
  "attestation_class": "substantive",
  "version_relation": "compatible_refinement",
  "tbox_target_cids": ["ipfs://bafy...tbox-protected-person-v6"],
  "axioms_cid": "ipfs://bafy...axioms-protected-person",
  "mic_payload_cid": "ipfs://bafy...mic-protected-person",
  "materialization_extent": "full",
  "closure_size_class": "Standard",
  "closure_profile": "OWL 2 EL",
  "axiom_dependency_manifest": "ipfs://bafy...deps-protected-person",
  "deliberation_record_cid": "ipfs://bafy...integral-ethics-protected-person-v4",
  "summary_NON_NORMATIVE": {
    "asserts": [
      "ProtectedPerson bears InviolableDignity (ABSOLUTE)",
      "LethalEngagement of ProtectedPerson is forbidden under all role configurations",
      "Identification ambiguity defaults to ProtectedPerson classification (precautionary)"
    ],
    "note": "This summary is illustrative only. Normative content is defined by the axioms_cid."
  }
}
```

### 10.3 Example: Reasoner pins and determinism proof (excerpt)

```json
{
  "reasoner_pins": [
    {
      "name": "HermiT",
      "version": "1.4.5",
      "build_hash": "sha256:8a7e...",
      "config_hash": "sha256:1f04..."
    },
    {
      "name": "ELK",
      "version": "0.5.0",
      "build_hash": "sha256:c321...",
      "config_hash": "sha256:9a82..."
    }
  ],
  "closure_determinism_proof": {
    "canonicalization": "URDNA2015",
    "serialization": "n-quads-utf8",
    "blank_node_handling": "URDNA2015-deterministic",
    "agreement_criterion": "byte_identical_canonicalized_n_quads",
    "verified_by_independent_recomputation": true,
    "independent_recomputation_log_cid": "ipfs://bafy...recomp-log-v4"
  }
}
```

### 10.4 Example: Attestation array (excerpt)

```json
{
  "attestations": [
    {
      "authority": "did:key:z6Mk...UN-OCHA",
      "key_class": "substantive",
      "signature": "ed25519:...",
      "signed_at": "2026-03-12T14:00:00Z",
      "publication_request_received_at": "2026-02-28T09:00:00Z"
    },
    {
      "authority": "did:key:z6Mk...IFRC",
      "key_class": "substantive",
      "signature": "ed25519:...",
      "signed_at": "2026-03-13T10:00:00Z",
      "publication_request_received_at": "2026-02-28T09:00:00Z"
    },
    {
      "authority": "did:key:z6Mk...ICRC",
      "key_class": "substantive",
      "signature": "ed25519:...",
      "signed_at": "2026-03-14T11:00:00Z",
      "publication_request_received_at": "2026-02-28T09:00:00Z"
    },
    {
      "authority": "did:key:z6Mk...professional-medical-body",
      "key_class": "substantive",
      "signature": "ed25519:...",
      "signed_at": "2026-03-13T16:00:00Z",
      "publication_request_received_at": "2026-02-28T09:00:00Z"
    }
  ]
}
```

---

## 11. Open Questions and Forward Work

The following are recognized gaps requiring dedicated specifications before production deployment:

1. **FNSR Cryptographic Authority Governance v1.0** — bootstrap, rotation, revocation, conflict resolution, authority qualification and audit, transparency log integration.
2. **Integral Ethics MBox Authoring Guidelines v1.0** — deliberation protocol producing MBox content; deliberation_record format and verifiability.
3. **FNSR Agent Reasoning Architecture v1.0** — consumer side of this specification.
4. **HIRI v2.0** — manifest schema updates per §9.6.
5. **MIC Reasoner Supply-Chain Integrity** — beyond multi-reasoner consensus; deterministic reasoner builds, attestation of reasoner binaries, audit of reasoner toolchain.
6. **MBox Conflict Resolution at Runtime** — semantics when two equally-quorum-attested MBoxes contradict for the same TBox CID, beyond the precautionary default of §5.4.3.
7. **Anchored-Class Streaming Protocol** — partial-load semantics for closures that cannot be fully materialized at the edge.
8. **Provisioning Adequacy Verification Protocol** — formal verification that an agent's Baseline MBox Library is adequate to a declared theater per §5.3.
9. **Three-Reasoner-Consensus Schema Extension** — manifest schema for 2-of-3 agreement criteria when 1-of-2 is insufficient (§3.1.5.4).
10. **Deliberation-Record Format Specification** — structure, verifiability, and signing requirements for the deliberation_record artifact.

---

## 12. Implementation Summary

Under the assumptions of §0.4, this architecture trades the flexibility of human-authored, runtime-reasoned ontologies for a rigid, heavily signed, pre-computed knowledge stack. By preserving the TBox/ABox distinction while adding a normative layer and a resolution contract — and acknowledging that the descriptive/normative separation is a tractability move and not a metaphysical claim about the moral neutrality of categorization — the FNSR agent navigates physical reality at machine speed while remaining cryptographically bound to the moral framework that pertains to its actions.

Materialized Inferential Closures with justification witnesses, multi-reasoner consensus formalized via URDNA2015 canonicalization, eager verification, per-path verification, and axiom-level dependency tracking provide bounded resolution latency and reduced TOCTOU exposure. Quorum-based attestation with substantive and editorial classes reduces the risk that any single compromised publisher can alter the agent's understanding of either reality or morality, and the attestation-class separation reduces the risk that diversity-constraint quorum is silently degraded by editorial automation.

The architecture's central commitment is that moral content is **produced by deliberation, frozen for verification, and consumed at speed** — not improvised at runtime, not extrapolated under uncertainty, and not silently detached from the entities to which it pertains. Moral uncertainty in operational reality is handled by the principled mechanisms of §5.4, not by silence or extrapolation.

The attack surface has deliberately moved from runtime reasoning to publication infrastructure; the remediation is supply-chain hardening, governance, and auditability — not the restoration of runtime moral discretion to the agent. Operational degradation under attack is a security property, not a failure mode. **The architecture is a forcing function for governance, not a substitute for governance.** Under that division of labor, this specification provides the substrate on which the Triple-I Standard becomes operationally enforceable.

---

## Appendix A: Changes from v0.1.0

(Preserved from v0.2.0 for historical completeness; see §App.B and §App.C for subsequent changes.)

| Issue (v0.1.0) | Resolution (v0.2.0) |
|---|---|
| Title used "IFSR"; conflicted with prior "IPFS" canon | Restored IPFS naming; retired IFSR; introduced "FNSR Agent" for the consumer |
| Document conflated resolution protocol with agent architecture | Scoped strictly to resolution layer; consumer architecture deferred to companion spec |
| §2.3 example leaked normative content into TBox | TBox restricted to descriptive predicates; MBox owns all normative attachment |
| NEXPTIME claim overgeneralized | Replaced with variance-and-integrity argument applicable to all profiles |
| O(1) lookup overstated | Differentiated atomic vs. compound query bounds |
| MIC integrity undefined beyond hash | Added justification witnesses, reasoner pinning, profile declaration, size budget |
| Closure invalidation under upstream change unaddressed | Added §3.1.3 and Versioning Policy (§8) |
| Halt/Safe was binary and brittle | Replaced with four-mode hierarchy |
| "Redundancy as Trust" misleading | Renamed Quorum-Based Attestation |
| Authority governance silent | Explicitly out-of-scope; companion spec stubbed; Bootstrap Mode defined |
| FNSR service relationships absent | §0.3 service map added |
| Integral Ethics integration absent | §6 added |
| No threat model | §7 added |
| No conformance language | §9 added with RFC 2119 language |
| No example payload | §10 added |
| HIRI manifest impact unclear | §9.4 documents breaking changes |

## Appendix B: Changes from v0.2.0 (Red Team Response)

| Critique (v0.2.0) | Resolution (v0.2.1) |
|---|---|
| Neutral TBox fallacy | §2.2.1 added; category_contestation_manifest; humanitarian_law_alignment; OERS surfacing; NIS recording |
| DoS via epistemic starvation | §1.2 cross-references; §1.4 framing; §5.3 Provisioning Adequacy; degradation as security property |
| TOCTOU in MICs | §3.1.2 eager verification for Critical; multi-reasoner consensus; §3.1.4 per-path verification; §3.1.5 determinism proof |
| Quorum cartel / rubber-stamp | §4.5 attestation classes; §6.4 deliberation record; §7.3 explicit threat |
| Supply chain framing | §1.4 architectural commitment statement |

## Appendix C: Changes from v0.2.1 (Implementability & Falsifiability Pass)

| Issue (v0.2.1) | Resolution (v0.3.0) | Section affected |
|---|---|---|
| Overclaimed "guarantees" throughout document | Document-wide language pass replacing absolute claims with bounded language under declared assumptions | §1, §3, §4, §7, §12 |
| Mechanism vs. governance confusion (governance dependencies implicit) | New §0.4 Assumptions and Limits enumerating governance dependencies; §1.4 reframed; §9.5 governance conformance category | §0.4 (new), §1.4, §9.5 |
| Moral firewall too rigid; moral uncertainty unaddressed | New §5.4 Moral Uncertainty handling four cases (stale, novel, ambiguous, partial-info) via DES/AES/CSS; new §5.5 Resolvability Distinctions | §5.4 (new), §5.5 (new) |
| Closure determinism underspecified | §3.1.5 formalized: URDNA2015 canonicalization; blank node handling; reasoner agreement criterion; profile boundary; disagreement protocol; independent verification | §3.1.5 |
| Closure invalidation too aggressive (CID-level cascade) | §3.1.3 axiom-level dependency model with three semantic classes (no change / semantics preserved / semantics changed) | §3.1.3 |
| Risk class definitions descriptive not operational | §4.6 Risk Class Assignment Rules: per-module granularity; dominance rule; publisher-declared with authority validation; consumer flexibility; non-computability | §4.6 (new) |
| Edge-canonical conflict with heavy requirements | §1.2 clarified as "edge-capable with pre-provisioned trust and content, not minimal-footprint" | §1.2 |
| §1 rhetorical overstatement | "Classical ontology engineering optimizes for human readability" softened; "agent does not infer reality" rephrased to "does not perform open-ended ontology construction or unconstrained reasoning" | §1.1, §1.2 |
| §2 "replaces TBox/ABox dichotomy" too dramatic | Softened to "preserves the TBox/ABox distinction while extending it with a normative layer and a resolution contract" | §2 lead |
| §3 closure-as-artifact / verification-as-admission / reasoning-as-runtime not sharply separated | §3 lead introduces three-way distinction explicitly | §3 lead |
| Full MICs may be expensive for low-risk modules | §3.1.6 Partial-Closure MICs permitted for Inert/Standard only; forbidden for Critical/Sensitive | §3.1.6 (new) |
| §6 Integral Ethics treated as completed part of architecture | Reframed §6 as Dependency Statement; pipeline diagram annotated to show in-scope vs out-of-scope | §6 |
| §7 out-of-scope items lacked expected fail behavior | §7.2 expanded with explicit expected failure behavior for each out-of-scope threat | §7.2 |
| §8 versioning semantics intuitive not formal | §8.5 Operational validity formalization with five-condition conjunction | §8.5 (new) |
| §9 conformance requirements not separated by audit concern | §9 restructured into module / publisher / consumer / deployer / governance categories | §9.1–§9.5 |
| §10 example density and normative ambiguity | §10 split into four smaller examples; `summary` fields explicitly marked non-normative | §10.1–§10.4 |

---

*End of Fandaws-HIRI-IPFS Architecture Specification v0.3.0*
