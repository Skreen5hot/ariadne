# Semantically Honest Middle Layer (SHML)
## Specification v3.3

**Bridging Realism, Computation, Human Understanding, and Belief-Scoped Reasoning**

**Aaron Damiano** · Fandaws Ontology Service · Ontology of Freedom Initiative

---

| Attribute | Value |
|---|---|
| Version | 3.3 |
| Status | Normative Draft |
| Standards | BFO 2020 (ISO/IEC 21838-2) · CCO 2.0 (v2.0-2024-11-06) |
| Replaces | SHML v3.2 |

---

## Changes in v3.3

**Added**
- **§3.4 Applicability** — when the full three-layer architecture is warranted versus when a provenance-annotated single graph suffices; the four break cases; layered/flat coexistence in one federation.
- **§4.4 Federation and Content-Addressing** — the content-addressing rationale for Assertion Event immutability; the mapping onto IPFS; corroboration, retraction, the Provenance Index as Merkle-DAG, Belief Scopes as CID-lists, and Logic Layer projections as regenerable cache. This is the architecture's federation keystone and was absent from prior versions.
- **§4.3 promoted** from prose to a full subcomponent specification — a `shml:BeliefScope` class, an identity rule, a flat/no-nesting structural policy, cross-scope-only-explicit reasoning, and registry mechanics.
- **§8.5 Projection Output Envelope** and **§8.6 Conflict Emission** — standardized payload schemas for provenance and surfaced conflicts.
- **Appendix B.5 Derived-by-Rule Fields** — a fifth projection-field category for values computed by a declared rule rather than read from a graph pattern.
- The **`[OPEN]`** convention label and the **`shml:`** Middle Layer vocabulary with provisional groundings for `AssertionEvent` and `BeliefScope`.

**Amended**
- **§8.1** reframed around the Scope Declaration as the single source of truth; the JSON-LD context, CONSTRUCT query, forward transform, and conformance test cases are now specified as generated from it. Adds the explicit statement that the JSON-LD context alone is **not** bidirectionally invertible.
- **§5.2** `[DESIGN DECISION]` sharpened — the annotation-property form is a Logic Layer projection shorthand, not a co-equal representation of the Quality.
- **§6.4** corrected — the shared role individual is named as a deliberate departure from strict BFO single-bearer Role semantics, with the downstream consequence for agency attribution flagged.
- **§10.4** downgraded to a forward reference — the confidence metric and aggregation are deferred to a separate confidence-model specification; cross-scope plausibility comparisons MUST NOT be presented as quantitatively grounded until that specification is adopted.

**Cut**
- **C-04's** vacuous exception clause (`unless that instance also types as IBE`) — ICE and IBE occupy disjoint BFO continuant branches, so the exception can never obtain. Replaced with an absolute prohibition plus an axiomatization requirement.

---

## Conventions

This specification uses the following normative language per RFC 2119:

- **MUST** — an absolute requirement of this specification
- **MUST NOT** — an absolute prohibition
- **SHOULD** — recommended; there may be valid reasons to depart but implications must be understood
- **MAY** — permitted but not required
- **[DESIGN DECISION]** — a modeling convention chosen for this architecture; alternative valid approaches exist
- **[ONTOLOGICAL CLAIM]** — a position held to be true about reality, grounded in BFO 2020 or CCO 2.0
- **[OPEN]** — a grounding or design question deliberately left unresolved in this version, with candidate resolutions noted; implementations MUST treat it as provisional

Explanatory commentary is separated from normative requirements by the use of block quotations or labeled sections. Readers implementing this specification should focus on MUST/SHOULD/MAY statements as the conformance contract.

---

## Table of Contents

1. The Problem
2. Design Principle: Semantic Honesty
3. The Three-Layer Architecture
4. The Middle Layer: Canonical Data Model
5. Qualities, Measurements, and Tokens
6. The Role / Quality / Process Decision Rule
7. Information Content Entities, Bearers, and Tokenization
8. The Compression Layer: Projection Contract Specification
9. Assertions as Occurrents
10. Belief-Scoped and Counterfactual Reasoning
11. What This Architecture Refuses
12. System Implementation

Appendix A: Worked Example — Federal Hierarchy Organization  
Appendix B: Projection Loss Model  
Appendix C: Conformance Requirements Summary

---

## 1. The Problem

### 1.1 The Predicate Shortcut

In most semantic systems, a shortcut is taken directly from observation to assertion. Consider an organization status field in a government data source. The source record contains `status: "ACTIVE"`. A predicate-centric system asserts:

```turtle
fh:org_300000057  fh:status  "ACTIVE" .
```

This shortcut collapses critical context: which system produced the reading, which measurement framework was used, when the status was recorded, and who bears responsibility for the conclusion. Recovering this context requires RDF reification, named graphs, or OWL axioms — approaches that degrade performance and readability without resolving the underlying structural problem.

### 1.2 The Fact-First Fallacy

> **The Fact-First Fallacy:** the assumption that semantic systems must begin with facts rather than with the processes that produce them. In reality, facts are outputs of interpretive activity. Treating them as primitives introduces semantic dishonesty at the foundation of the stack.

The SHML rejects this fallacy architecturally. Every assertion in a conformant system is traceable to a producing process. No assertion is primitive.

### 1.3 The Adoption Failure

The failure of semantic technology adoption in the broader developer community is not a failure of ontology. It is the absence of connector tissue between the philosophical commitment and working code. Ontologists produce correct models. Developers produce usable systems. Neither produces the layer that connects them.

The SHML specifies that connector tissue: a compression layer with a defined projection contract, a bidirectional transform, and a loss model. Developers consume flat projections. Ontologists reason over the full graph. The SHML defines what must be true of both and how to move between them.

---

## 2. Design Principle: Semantic Honesty

**Semantic Honesty** is the commitment to never represent a state as a static, global truth if it is in fact the output of a process.

The SHML enforces this principle through four architectural requirements:

1. Every assertion in the Logic Layer is traceable to a producing process in the Middle Layer.
2. Provenance, scope, and temporal validity are preserved where source data supports them.
3. Projections are explicitly bounded — they do not claim to be the full graph.
4. Uncertainty and disagreement are modeled as first-class citizens, not edge cases.

This mirrors the realist distinction in BFO 2020 between Continuants (entities that persist through time) and Occurrents (processes that unfold over time). The SHML treats assertions as belonging to the latter.

> Semantic honesty has a federation consequence the prior versions left implicit: if an assertion is the record of an act that occurred, that record does not later un-occur, and so it can be made immutable and content-addressed. This is the foundation of §4.4 and the reason the Middle Layer federates.

---

## 3. The Three-Layer Architecture

The SHML defines three distinct layers. Each has a defined substrate, scope, and role. Traffic between layers is governed by the Projection Contract (Section 8).

### 3.1 The Reality Layer

| Attribute | Value |
|---|---|
| Domain | Entities, processes, causal powers |
| Substrate | OWL 2 / Turtle RDF |
| Standard | BFO 2020 (ISO/IEC 21838-2) / CCO 2.0 |
| Scope | Universal — no claims about belief or certainty |
| Role | Defines the class hierarchy into which all instances are typed |

The Reality Layer makes no claims about interpretation, belief, or measurement. It defines what kinds of things exist and what kinds of processes can occur.

> **[DESIGN DECISION]** The SHML uses BFO 2020 and CCO 2.0 as the Reality Layer standards. Other realist upper ontologies may be substituted where CCO terms are not available, provided the grounding principles of Sections 5 and 6 are preserved.

The relevant Reality Layer classes for the worked example in this specification include:

| Class | IRI | Role in this spec |
|---|---|---|
| Government Organization | `cco:ont00000408` | Typing all org instances |
| Quality | `obo:BFO_0000019` | Parent of operational status |
| Role | `obo:BFO_0000023` | Parent of org-type role individuals |
| Code Identifier | `cco:ont00000077` | Parent of system-assigned code ICEs |
| Proper Name | `cco:ont00001014` | Parent of org name ICEs |
| Information Content Entity | `cco:ont00000958` | Grandparent of all ICE subclasses |

### 3.2 The Middle Layer

| Attribute | Value |
|---|---|
| Domain | Semantic processes, assertion events, provenance, belief scopes |
| Substrate | Labeled Property Graphs (LPG) — content-addressed when federated (§4.4) |
| Scope | Contextual — records who asserted what, when, why |
| Role | Authoritative event log; source of all Logic Layer projections |

The Middle Layer is the authoritative event log of the system. It records acts of observation, interpretation, and assertion — not the facts themselves. This is the substrate advantage the SHML exploits: Labeled Property Graphs allow properties on relationships, enabling process representation without distorting assertions into artificial nodes or axioms.

The canonical data model of the Middle Layer is specified in Section 4.

### 3.3 The Logic Layer

| Attribute | Value |
|---|---|
| Domain | Computable facts and public interfaces |
| Substrate | RDF Turtle / JSON-LD / SHACL |
| Standard | W3C |
| Scope | Projection-bounded — does not define truth; records commitments |
| Role | Downstream consumer interface |

The Logic Layer is explicitly downstream. It does not define truth; it records commitments derived from the Middle Layer. Multiple Logic Layer projections MAY coexist over the same Middle Layer. Each is internally consistent within its scope. When a Middle Layer assertion event is retracted, all downstream Logic Layer projections derived from that event MUST be regenerated or explicitly marked stale.

### 3.4 Applicability: When the Full Architecture Is Warranted

The three-layer architecture is not the right level for every data set. A single provenance-annotated graph — one entity node carrying its sources and validity intervals directly on itself — is correctly right-sized below a definite threshold. Forcing the full architecture beneath that threshold is ceremony, not rigor.

The full architecture is warranted when one or more of the following **break cases** obtains:

1. **Corroboration with retraction.** Multiple sources assert the same fact, and the system must be able to retract one source's contribution without losing the fact (still corroborated by the others) and without destructively editing a node. A flat graph forces a node rewrite and loses the per-source attribution history.
2. **Source disagreement.** Two or more sources assert conflicting values for the same field, and the system must retain all of them rather than silently choosing. A flat graph forces one of: pick a winner, duplicate the entity, or invent a disambiguation property.
3. **Scope-bounded diverse consumers.** Different consumers require different bounded views of the same graph — different field sets, different source scopes, different conflict policies — with each view contracted, regenerable, and retraction-aware.
4. **Belief-scoped reasoning.** Multiple agents hold internally coherent, mutually divergent interpretations of the same Reality Layer entities, and the system must reason within and across those interpretations without collapsing them. This case **cannot** be reproduced by extending a flat graph, however much provenance is annotated onto it; it requires Belief Scope as a first-class container (§4.3).

Below these cases, a provenance-annotated single graph is sufficient and SHOULD be preferred for its simplicity.

> **[DESIGN DECISION]** Layered and flat representations MAY coexist in a single federation. A node serving a contended, multi-agent A-box runs the full architecture; a node serving a single-source reference data set MAY run a flat provenance-annotated graph. Entity identity across the two is bridged by the HIRI Protocol (§12). Adoption does not require a node to take on the full architecture before it has a break case that needs it. This coexistence is the intended adoption path: partial buy-in at the node level, federated by shared identity.

---

## 4. The Middle Layer: Canonical Data Model

The Middle Layer was described in v3.1 as simultaneously an event log, an assertion substrate, a provenance record, and a belief-scope container. These are related but distinct responsibilities. This section formalizes the Middle Layer into three canonical subcomponents and (in §4.4) specifies how they federate.

### 4.1 Subcomponent 1: The Assertion Event Log

An Assertion Event records a single act of semantic commitment. Every Logic Layer triple is traceable to at least one Assertion Event.

**Canonical LPG structure:**

```
(AssertionEvent_N : AssertionEvent)
  -[:SUBJECT]->      (Entity_X)
  -[:OBJECT]->       (Entity_Y | Literal_Z)
  -[:PREDICATE]->    (Relation_R)
  -[:ACCORDING_TO]-> (EvidenceArtifact_E)    # optional
  -[:ASSERTED_BY]->  (Agent_A)               # optional
  -[:VALID_FROM]->   "timestamp"             # optional
  -[:VALID_UNTIL]->  "timestamp"             # optional
  -[:IN_SCOPE]->     (BeliefScope_B)         # optional
```

**Required properties:** SUBJECT, OBJECT, PREDICATE.  
**Optional properties:** All others. Their presence depends on source data availability.

**Class declaration:**

```turtle
shml:AssertionEvent
    a owl:Class ;
    rdfs:label "Assertion Event"@en ;
    rdfs:comment "An occurrent that produces a single semantic commitment.
                  Every Logic Layer triple is traceable to at least one." .
```

> **[OPEN]** The ontological grounding of `shml:AssertionEvent` is not yet fixed. Candidate parent: a CCO Act subclass under `obo:BFO_0000015` (process / occurrent), since an Assertion Event is an occurrent that produces an information artifact. Resolution is deferred to a dedicated grounding pass. Until it is fixed, implementations MUST NOT build inferences that depend on a specific parent class.

> **[DESIGN DECISION]** The SHML does not mandate specific property labels for the LPG. Implementations MAY use different property names provided the structural semantics — a reified assertion with optional provenance — are preserved.

A published Assertion Event is immutable. The consequences of this requirement, and the reason it is the architecture's federation keystone, are specified in §4.4.

### 4.2 Subcomponent 2: The Provenance Index

The Provenance Index maps each Logic Layer triple to the Assertion Event(s) that produced it. A triple MAY be produced by multiple Assertion Events (corroboration). A triple MUST be removed from the Logic Layer when all producing Assertion Events have been retracted.

The Provenance Index is a first-class data structure, not a derived table. It MUST be updated synchronously with any Assertion Event creation or retraction. When the Middle Layer is federated over content-addressed storage, the Provenance Index takes the form of a verifiable DAG over Assertion Event identifiers (§4.4).

### 4.3 Subcomponent 3: The Belief Scope Registry

A Belief Scope is a coherent, internally consistent set of Assertion Events attributed to a specific agent under a specific interpretive framework over a specific temporal window. Belief Scopes are not competing ontologies; they are different agents' interpretations of the same underlying Reality Layer entities. Disagreement between scopes does not imply contradiction in the Reality Layer. Reality remains singular; interpretations vary.

This subcomponent specifies the Belief Scope as a first-class entity, not a label. Section 10's counterfactual reasoning, probability attribution, and conflict isolation all run on the structure defined here.

**Class.**

```turtle
shml:BeliefScope
    a owl:Class ;
    rdfs:label "Belief Scope"@en ;
    rdfs:comment "A coherent, internally consistent set of Assertion Events
                  attributed to an agent under an interpretive framework over
                  a temporal window." .
```

> **[OPEN]** The ontological grounding of `shml:BeliefScope` is not yet fixed. Candidate parents: a Generically Dependent Continuant subclass (a scope as an information artifact that can be borne by multiple records), or an Information Content Entity framework subclass. Resolution is deferred to a dedicated grounding pass. Implementations MUST treat the grounding as provisional and MUST NOT build inferences that depend on a specific parent class until it is fixed.

**Identity rule.** A Belief Scope is identified by the composite key:

```
(agent, interpretive_framework, temporal_window)
```

Two scopes with the same agent and framework but different temporal windows are **distinct** scopes — this is how an agent's change of position over time is represented without contradiction. Two scopes with the same agent and window but different frameworks are **distinct** scopes.

**Structure.** Belief Scopes are flat. A Belief Scope MUST NOT contain another Belief Scope. There is no scope inheritance. An Assertion Event MAY be a member of more than one scope only by explicit re-assertion — a distinct Assertion Event per scope; membership is never implied by nesting.

**Cross-scope reasoning.** Reasoning MUST NOT cross scope boundaries implicitly. A conclusion that draws on two scopes MUST be represented as its own explicit reasoning process that names both scopes as inputs (§10.3). The default isolation is strict: within a scope, reasoning proceeds normally; across scopes, only an explicit, named comparison process may relate them.

**Registry.** The Belief Scope Registry records every defined scope, its identity key, and its current membership as a set of Assertion Event identifiers (content-addressed when federated — §4.4). The Registry is a first-class data structure, updated synchronously with scope creation and with any Assertion Event's scope assignment.

### 4.4 Federation and Content-Addressing

The immutability of Assertion Events is not a stylistic preference. It is the property that makes the Middle Layer federate. This section states the requirement and its consequences. It is the architectural justification the prior versions omitted, and it is the reason several decisions elsewhere in this specification — event-over-state, retraction-as-new-event, the Provenance Index as a first-class structure — take the form they do.

> **[ONTOLOGICAL CLAIM / engineering]** An Assertion Event records an act that occurred. An act that occurred does not later un-occur. Once published, an Assertion Event therefore MUST NOT be mutated. Correction is achieved by publishing a new Assertion Event, never by editing an existing one.

This maps the Middle Layer onto content-addressed storage (e.g., the Interplanetary File System) natively:

- **Addressing.** Each Assertion Event is addressed by the hash of its content (a CID). Because it never mutates, its address is stable for the life of the federation.
- **Corroboration** is the publication of a new Assertion Event that references the same ICE or Quality instance. No existing node is rewritten; no address is orphaned. Three sources confirming one fact means three Assertion Events pointing at one ICE — not three rewrites of one node.
- **Retraction** is the publication of a new Assertion Event asserting that a prior Assertion Event (by CID) is retracted as of a timestamp. The original is untouched and remains addressable; the retraction is itself a permanent, addressable record. History is never lost.
- **The Provenance Index** (§4.2) is the Merkle-DAG over Assertion Event CIDs. Any node in the federation can verify, by hash, which events produced a given Logic Layer triple and whether any have been retracted.
- **A Belief Scope** (§4.3) is, at the storage layer, a list of Assertion Event CIDs. Scope membership is content-addressed and independently verifiable.
- **Logic Layer projections** are derived and regenerable. They do not require stable CIDs; they are cache over the Middle Layer DAG and MAY be discarded and rematerialized at will.

> **[DESIGN DECISION]** This is why the architecture chooses immutable events over mutable state. A mutable-state graph — an entity node whose properties are edited in place — cannot federate over content-addressed storage without orphaning addresses on every update. At the storage layer, the mutation-per-update pattern is indistinguishable from centralized state. The Assertion Event model is the form that lets the A-box federate across nodes that share no central authority.

This requirement is consistent with the Edge-Canonical First doctrine: event capture and verification occur at the node, require no central infrastructure, and remain valid offline. A node that holds the relevant Assertion Event CIDs can verify provenance and reconstruct any projection without contacting any other node.

**Conformance:**

- A published Assertion Event MUST NOT be mutated. (C-11)
- Retraction MUST be expressed as a new Assertion Event referencing the retracted event, not as deletion or mutation. (C-12)
- The Provenance Index MUST be derivable as a verifiable DAG over Assertion Event identifiers. (C-13)

---

## 5. Qualities, Measurements, and Tokens

This section addresses the fundamental distinction that predicate-centric systems consistently miss: the difference between a Quality that inheres in an entity, the measurement act that observes it, and the token that a measurement system assigns to label it.

### 5.1 The Conceptual Distinction

Three things must be kept separate:

| Concept | Ontological status | Where it lives |
|---|---|---|
| **Quality** | Real, specifically dependent continuant inhering in a bearer | Reality Layer — `obo:BFO_0000019` subclass instance |
| **Measurement act** | Occurrent — a process that observes the Quality | Middle Layer — Assertion Event with measurement provenance |
| **Token** | Representational label assigned by a measurement framework | Logic Layer — `is_tokenized_by` literal |

The Quality is not the token. The token is not the Quality. The measurement act is the process that connects them.

> **[ONTOLOGICAL CLAIM]** Qualities are real. A Quality inheres in its bearer regardless of whether any system has measured or named it. The token "ACTIVE" is the Federal Hierarchy system's label for an organizational state that exists independently of that label.

The analogy: the electromagnetic reflectance of a surface is real. "Red" is the token a human visual system assigns. A dog's visual system assigns a different token. The surface is unchanged. The Quality is unchanged.

### 5.2 The BFO 2020 Grounding

`obo:BFO_0000019` (Quality) is a specifically dependent continuant that:

- inheres in an independent continuant (its bearer)
- cannot exist without its bearer
- is the kind of thing that can change over time

Operational status satisfies all three conditions: it depends entirely on the organization, cannot float free of it, and can change over time. It is therefore a Quality — not an annotation, not an administrative label, not a boolean flag.

> **[DESIGN DECISION]** Representing status as a Quality is an ontological commitment (the [ONTOLOGICAL CLAIM] above), not a stylistic choice. The annotation-property form — a token placed directly on the org node — is **not a co-equal conformant representation of the Quality**. It is a Logic Layer *projection shorthand*: the full Quality instance with `inheres_in` lives in the Reality/Middle Layer and is authoritative; the annotation on the projection is a lossy view of it, recoverable from the graph but not a substitute for it. This is the same asymmetry the specification applies to the ICE/IBE chain in §7.4 — full chain upstream, shorthand in the projection. A projection that carries only the annotation form MUST be understood as a view over a Quality instance that exists upstream, never as the Quality itself.

### 5.3 Normative Pattern: Quality

A conformant Quality representation MUST include:

```turtle
# One class declaration per quality type
fh:FederalOrganizationalOperationalStatus
    a owl:Class ;
    rdfs:subClassOf obo:BFO_0000019 ;
    rdfs:label "Federal Organizational Operational Status"@en ;
    rdfs:comment "A quality inhering in a Government Organization,
                  indicating its operational standing as measured by
                  the U.S. Federal Hierarchy system." .

# One instance per bearer
fh:status_300000057
    a fh:FederalOrganizationalOperationalStatus ;
    obo:RO_0000052 fh:org_300000057 ;               # inheres_in
    cco:ont00001761 "ACTIVE"^^xsd:string .           # is_tokenized_by

# Bearer assertion
fh:org_300000057
    obo:RO_0000053 fh:status_300000057 .             # bearer_of
```

**On history nodes:** `obo:BFO_0000182` (History) nodes MAY be added to ground the temporal extent of the Quality when source data includes timestamps. When source data carries no temporal information, history nodes MUST NOT be asserted. A Quality does not require a timestamp to inhere; it inheres as of the time of transformation. Vacuous history nodes — typed but unpopulated — constitute a semantic honesty violation.

### 5.4 Boundary: What Is in the Ontology vs. What Is a Projection Artifact

To be explicit about which artifacts belong where:

| Artifact | Belongs in ontology | Belongs in projection only |
|---|---|---|
| Quality class declaration | ✅ | — |
| Quality instance with `inheres_in` | ✅ | — |
| `is_tokenized_by` literal on Quality instance | ✅ | — |
| Flat `fh:flat_status "ACTIVE"` triple | — | ✅ |
| History node without timestamps | — | Neither |

---

## 6. The Role / Quality / Process Decision Rule

The SHML uses three different patterns for what might superficially appear to be "properties" of an entity. This section provides a decision rule for choosing between them.

### 6.1 The Three Patterns

| Pattern | What it models | BFO parent | Example |
|---|---|---|---|
| **Role individual** | A contextual function an entity bears in a governance or social context | `obo:BFO_0000023` Role | Org type (Department, Sub-Tier, Office) |
| **Quality instance** | A real state that inheres in an entity and depends on it for existence | `obo:BFO_0000019` Quality | Operational status (Active, Inactive) |
| **Assertion Event** | A claim that a relationship or state obtains, produced by an agent | Middle Layer | Employment, residency, membership |

### 6.2 The Decision Rule

Apply the following tests in order:

**Test 1 — Is this a state that depends on the entity for existence and cannot be reassigned to another entity without ceasing to be the same state?**

- Yes → **Quality**
- No → continue to Test 2

**Test 2 — Is this a function or standing the entity bears within a specific social, legal, or institutional framework, where the function could in principle be transferred or lost without the entity ceasing to exist?**

- Yes → **Role individual** (if the role type is stable and reused) or **Assertion Event** (if the role-bearing is itself a claim requiring provenance)
- No → continue to Test 3

**Test 3 — Is this a claim made by an agent about a relationship between two entities, where the claim may be contested, retracted, or held by some agents but not others?**

- Yes → **Assertion Event** in the Middle Layer
- No → reassess whether this should be modeled at all

### 6.3 Application to the Worked Example

| Field | Test result | Pattern |
|---|---|---|
| `status: "ACTIVE"` | Test 1: Yes — depends on org, cannot be reassigned | Quality |
| `fhorgtype: "Department/Ind. Agency"` | Test 2: Yes — institutional function, stable, reused across orgs | Role individual |
| `fhorgname` | Neither Test 1 nor 2 — it designates, it does not inhere | ICE (Proper Name) |
| `fhorgid`, `agencycode`, `cgac` | Neither — system-assigned codes that identify | ICE (Code Identifier) |
| `children` (hierarchy) | Hierarchy is a structural relationship — part_of | `obo:BFO_0000050` direct assertion |

### 6.4 Role Individual Identity Management

Role individuals in the SHML are **named individuals**, not classes. A single role individual is declared once and shared across all instances that bear that role.

> **[DESIGN DECISION]** Strict BFO 2020 treats a Role as a specifically dependent continuant that inheres in exactly one independent continuant; on the strict reading, the role borne by Organization A is not numerically identical to the role borne by Organization B, even when both are of the same role type. The SHML deliberately departs from this: it models one named role *individual* shared across all bearers of that type. This pattern — **role-type-as-named-individual** — is chosen for federation and reuse economy: one addressable role node, many `bearer_of` assertions, rather than a per-bearer role instance multiplied across the A-box. The departure is sound for governance-role typing, where the role *type* is what matters and per-bearer role identity carries no information. It is **not** appropriate where per-bearer role identity is itself a subject of reasoning. Downstream consumers that attribute standing or agency on the basis of role-bearing (e.g., Architectonic Agency Theory's use of role realization) MUST treat "bears the same role individual" as "bears the same role *type*," not as any stronger identity claim, and MUST recover per-bearer role-bearing from the `bearer_of` assertion, not from the shared role node.

Implementers MUST be aware of three implications:

1. **Identity scope:** A role individual is specific to the governance framework that defines it. `fh:FederalDepartmentOrIndependentAgencyRole` is defined by and scoped to the FH system. It MUST NOT be equated with a DoD role or a CCO role without an explicit alignment assertion.
2. **Reuse boundaries:** If two organizations bear the same role, they share the same role individual. This is correct under the role-type-as-named-individual pattern — they are both playing the same institutional role type. It does not imply they are the same organization.
3. **Role vs. role-bearing:** The role individual represents the role type. The `bearer_of` assertion on the org represents the role-bearing. These are separate things. The role individual does not change when the org changes; a new `bearer_of` assertion may be added if the org takes on a new role.

---

## 7. Information Content Entities, Bearers, and Tokenization

### 7.1 The Full Staircase

CCO 2.0 distinguishes between:

- **Information Content Entity (ICE)** — the abstract informational content (`cco:ont00000958`)
- **Information Bearing Entity (IBE)** — the physical object upon which that content generically depends (`cco:ont00000253`)

The full chain for a name is:

```
Person
  → [obo:IAO_0000235 designated_by]
    → Name ICE (cco:ont00001014)
      → [obo:BFO_0000101 is_generically_dependent_on]
        → Record IBE (cco:ont00000253)
          → [cco:ont00001765 has_text_value]
            → "Aaron Damiano"^^xsd:string
```

**Inferential commitments of the full chain:**
- The person is designated by a name concept, not a string
- The name concept is concretized in a specific physical record (a database row, a birth certificate)
- The physical record bears the string value
- If the physical record is destroyed, the ICE may still exist and be concretized elsewhere

**Inferential commitments dropped by the projection shorthand (Section 7.3):**
- Identity of the physical carrier
- Provenance of which record bears the name
- The ICE/IBE dependency relationship

### 7.2 The Domain Violation

`cco:ont00001765` (`has_text_value`) has `rdfs:domain = cco:ont00000253` (Information Bearing Entity).

Asserting `has_text_value` directly on an ICE instance is a domain violation. Under OWL semantics, a reasoner will infer that anything bearing `has_text_value` is an IBE — which is incorrect when the subject is an ICE typed as a subclass of `cco:ont00000958`. This error is silent in many toolchains but produces incorrect inferences under formal reasoning.

A conformant implementation MUST NOT assert `cco:ont00001765` on any instance whose type is a subclass of `cco:ont00000958`. ICE and IBE occupy disjoint branches of the BFO continuant hierarchy (generically dependent continuant versus independent continuant); the prohibition is absolute, and the exception entertained in earlier versions can never obtain. See C-04 for the axiomatization requirement.

### 7.3 The Canonical Compression: `is_tokenized_by`

`cco:ont00001761` (`is_tokenized_by`) is an `owl:AnnotationProperty`. Annotation properties carry no `rdfs:domain` or `rdfs:range` constraints in OWL. CCO explicitly designed `is_tokenized_by` for the case where an ICE is linked to a widely used token expressing it — without requiring full IBE instantiation.

> **[DESIGN DECISION]** Using `is_tokenized_by` on the ICE directly is the CCO-intended pattern for Logic Layer projections. It is not a workaround. The full ICE + IBE chain belongs in the Middle Layer. The Logic Layer projection uses `is_tokenized_by`.

```turtle
# CORRECT — Logic Layer projection
fh:name_300000057
    a fh:FederalOrganizationProperName ;           # subClassOf cco:ont00001014
    cco:ont00001761 "ADMINISTRATIVE CONFERENCE..."^^xsd:string .

# INCORRECT — domain violation
fh:name_300000057
    a fh:FederalOrganizationProperName ;
    cco:ont00001765 "ADMINISTRATIVE CONFERENCE..."^^xsd:string .  # domain=IBE — WRONG
```

### 7.4 When to Use the Full IBE Chain

The full ICE + IBE chain SHOULD be instantiated when:

- The physical carrier is itself a subject of interest (which database row, which document)
- Provenance of the bearer is required for audit or legal purposes
- The Middle Layer LPG is being populated (full chain always preferred there)

The `is_tokenized_by` shorthand MAY be used when:

- The Logic Layer projection is the target and IBE provenance is not required by the consuming system
- The source data does not identify the physical carrier
- Graph node count is a performance concern and the full provenance chain is preserved in the Middle Layer

---

## 8. The Compression Layer: Projection Contract Specification

The Compression Layer defines the bidirectional contract between the full ontological graph and the flat developer-facing representation.

### 8.1 The Contract Artifacts

The contract has one **authored** artifact and a set of **generated** artifacts.

| Artifact | Authored / Generated | Direction | Role |
|---|---|---|---|
| **Scope Declaration** | Authored — source of truth | — | Declares bounded scopes, captured fields, selection rules, collision policy, omissions |
| JSON-LD Context | Generated | Flat → Graph (framing) | Maps developer keys to ontological IRIs |
| SPARQL CONSTRUCT query | Generated | Graph → Flat | Materializes the projection |
| Forward transform | Generated | Flat → Graph (generation) | Expands flat records to full Turtle, disambiguating ICE type per field |
| Conformance test cases | Generated | — | The projection's promise: rendered output for the clean case and each conflict case |

> **[DESIGN DECISION]** The Scope Declaration is the single source of truth. The JSON-LD context, the CONSTRUCT query, the forward transform, and the conformance test cases MUST be derivable from it by a generator. An implementation conforms by authoring one declaration, not by hand-writing the downstream artifacts. Hand-authoring the generated artifacts is permitted but discouraged: it reintroduces the drift the single-source-of-truth model exists to prevent. (C-16)

**Invertibility.** The JSON-LD context alone is **not** bidirectionally invertible. Multiple scalar fields map to the same `cco:ont00001761` (`is_tokenized_by`) IRI and are distinguishable only by the ICE type of the node the annotation sits on — which the context does not carry. The context is therefore sufficient for graph → flat framing only. Flat → graph reconstruction REQUIRES the forward transform, which holds the field-to-ICE-type mapping. Any claim that a flat payload round-trips to the graph via the context alone is false for this contract shape.

### 8.2 The JSON-LD Context

The JSON-LD context is the developer-facing framing artifact. Each key maps to exactly one ontological IRI or pattern. The mapping type MUST be specified for each key. Per §8.1, it is generated from the Scope Declaration and is sufficient for graph → flat framing only.

```json
{
  "@context": {
    "@base":      "https://ontology.example.gov/fh#",
    "cco":        "https://www.commoncoreontologies.org/",
    "obo":        "http://purl.obolibrary.org/obo/",
    "fh":         "https://ontology.example.gov/fh#",
    "xsd":        "http://www.w3.org/2001/XMLSchema#",
    "skos":       "http://www.w3.org/2004/02/skos/core#",

    "fhorgid": {
      "@id":   "cco:ont00001761",
      "@type": "xsd:integer",
      "_mapNote": "Annotation on FhOrgIdentifier ICE — is_tokenized_by pattern"
    },
    "fhorgname": {
      "@id":   "cco:ont00001761",
      "@type": "xsd:string",
      "_mapNote": "Annotation on FederalOrganizationProperName ICE"
    },
    "agencycode": {
      "@id":   "cco:ont00001761",
      "@type": "xsd:string",
      "_mapNote": "Annotation on AgencyCode ICE"
    },
    "cgac": {
      "@id":   "cco:ont00001761",
      "@type": "xsd:string",
      "_mapNote": "Annotation on CommonGovernmentAccountingClassificationCode ICE"
    },
    "status": {
      "@id":   "cco:ont00001761",
      "@type": "xsd:string",
      "_mapNote": "Annotation on FederalOrganizationalOperationalStatus Quality instance"
    },
    "fhorgtype": {
      "@id":      "skos:altLabel",
      "_mapNote": "Maps to skos:altLabel on the Role individual — not a class assertion"
    },
    "children": {
      "@id":      "obo:BFO_0000050",
      "@reverse": true,
      "_mapNote": "Reverse of part_of: child is part_of parent"
    }
  }
}
```

> **Mapping rationale:** All five scalar fields (`fhorgid`, `fhorgname`, `agencycode`, `cgac`, `status`) map to `cco:ont00001761` (`is_tokenized_by`). This is semantically correct because in the full graph each field is an `is_tokenized_by` annotation on a distinct typed ICE or Quality instance. The JSON-LD context collapses the ICE node, making `is_tokenized_by` appear directly on the parent key. This is a projection convenience, not a semantic claim that all five fields are the same kind of thing. Their distinct ontological types are preserved in the full graph, not in the context — which is exactly why the context alone cannot invert the projection (§8.1).

> `fhorgtype` maps to `skos:altLabel` on the Role individual, not to a class IRI, because `fhorgtype` values are institutional labels for roles, not class names. This preserves round-trip fidelity — the original string is recoverable from the graph.

> `children` maps as a reverse of `obo:BFO_0000050` (`part_of`). The child org is `part_of` the parent; the `@reverse` flag inverts the direction so the tree structure of the source JSON is preserved in the context.

### 8.3 The SPARQL CONSTRUCT Query (Graph → Flat)

```sparql
PREFIX fh:   <https://ontology.example.gov/fh#>
PREFIX cco:  <https://www.commoncoreontologies.org/>
PREFIX obo:  <http://purl.obolibrary.org/obo/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

CONSTRUCT {
  ?org  fh:flat_fhorgid    ?idVal .
  ?org  fh:flat_fhorgname  ?nameVal .
  ?org  fh:flat_agencycode ?agencyVal .
  ?org  fh:flat_cgac       ?cgacVal .
  ?org  fh:flat_status     ?statusVal .
  ?org  fh:flat_fhorgtype  ?typeLabel .
  ?org  obo:BFO_0000050    ?parent .
}
WHERE {
  ?org a cco:ont00000408 .

  ?org obo:IAO_0000235 ?idICE .
  ?idICE a fh:FhOrgIdentifier ;
         cco:ont00001761 ?idVal .

  ?org obo:IAO_0000235 ?nameICE .
  ?nameICE a fh:FederalOrganizationProperName ;
           cco:ont00001761 ?nameVal .

  ?org obo:IAO_0000235 ?agencyICE .
  ?agencyICE a fh:AgencyCode ;
             cco:ont00001761 ?agencyVal .

  ?org obo:IAO_0000235 ?cgacICE .
  ?cgacICE a fh:CommonGovernmentAccountingClassificationCode ;
           cco:ont00001761 ?cgacVal .

  ?org obo:RO_0000053 ?statusNode .
  ?statusNode a fh:FederalOrganizationalOperationalStatus ;
              cco:ont00001761 ?statusVal .

  ?org obo:RO_0000053 ?roleNode .
  ?roleNode a obo:BFO_0000023 ;
            skos:altLabel ?typeLabel .

  OPTIONAL { ?org obo:BFO_0000050 ?parent }
}
```

The `level` field present in the source JSON is intentionally omitted from the CONSTRUCT. `level` is derivable from the depth of the `part_of` chain and carries no information not already present in the graph. See Appendix B for the full projection loss model.

### 8.4 Projection Consistency

A conformant projection MUST satisfy:

1. **Scope declaration:** Each projection MUST declare its scope — the set of graph patterns it captures and the fields it intentionally omits. (This declaration is the source-of-truth artifact of §8.1.)
2. **Retraction propagation:** When a Middle Layer assertion event is retracted, the Provenance Index (Section 4.2) MUST trigger regeneration of all projections derived from that event. Projections that persist after their producing assertion is retracted are a semantic honesty violation.
3. **Collision handling:** When two Assertion Events produce conflicting values for the same projection field, the projection MUST NOT silently choose one. It MUST either surface the conflict (§8.6) or be explicitly scoped to a specific Belief Scope (Section 10).
4. **Non-singleton fields:** Where the graph contains multiple values for a field that the projection represents as singular (e.g., multiple names for one org), the projection MUST define its selection rule explicitly.

### 8.5 Projection Output Envelope

Every emitted projection MUST carry a provenance envelope alongside its data fields. The envelope is not optional metadata; it is what makes the projection retraction-aware and auditable (§3.3, §4.4).

Required envelope fields:

| Field | Content |
|---|---|
| `_contract` | Identifier of the producing Scope Declaration |
| `_generated_at` | Timestamp of materialization |
| `_derived_from` | List of Assertion Event identifiers (CIDs, §4.4) that produced the emitted fields |
| `_scope_bounded_to` | The scopes this projection is bounded to |
| `_excluded_scopes` | Scopes deliberately excluded, with the projection still well-defined |
| `_conflicts` | Conflict block (§8.6); empty list when no conflict |

Corroboration MAY be surfaced with a per-field `_<field>_corroborated_by` listing the agents whose Assertion Events agree on the emitted value. (C-17)

### 8.6 Conflict Emission

§8.4(3) requires that conflicting values MUST be surfaced rather than silently chosen. "Surfaced" has a defined payload shape. When two or more Assertion Events within the bounded scope set produce distinct tokens for a single projection field after the declared normalization, the projection:

- MUST emit the field value as `null`;
- MUST populate `_conflicts` with an entry for the field;
- MUST NOT choose a value.

Each `_conflicts` entry:

```json
{
  "field":  "<field name>",
  "reason": "<why this is a conflict>",
  "candidates": [
    { "value": "...", "scope": "...", "asserted_by": "...", "via": "<AE id>" }
  ]
}
```

A consuming system that requires a single value MUST resolve the conflict by selecting a scope (narrowing the projection's bounded set) or by applying a declared selection rule — never by reading one candidate arbitrarily from the conflict block. (C-18)

---

## 9. Assertions as Occurrents

### 9.1 Principle

In the SHML, assertions are events. They are not properties, attributes, or predicates. Every Logic Layer triple is traceable to at least one Middle Layer Assertion Event.

This is not presented as an ontological necessity of BFO. It is a **design decision** that produces the following engineering benefits: temporal validity is representable without reification; provenance is first-class; retraction is unambiguous; disagreement between agents does not require contradiction in the data model; and — as specified in §4.4 — the event log federates over content-addressed storage without orphaning addresses.

### 9.2 The Residency Example

**Traditional:**
```turtle
Person_Aaron  fh:livesAt  House_123 .
```

**Middle Layer (LPG):**
```
(AssertionEvent_001 : ResidencyAssertion)
  -[:SUBJECT]->      (Person_Aaron)
  -[:OBJECT]->       (House_123)
  -[:PREDICATE]->    (fh:livesAt)
  -[:ACCORDING_TO]-> (LeaseAgreement_PDF)
  -[:VALID_FROM]->   "2024-01-01"
  -[:ASSERTED_BY]->  (PropertyManager_Agent)
```

**Logic Layer projection (emitted from Middle Layer):**
```turtle
Person_Aaron  fh:livesAt  House_123 .
```

The triple is identical. The difference is that in the SHML, it is derived, not primitive. If the Property Manager retracts the assertion, the triple is removed and the retraction is recorded in the Assertion Event Log as a new event (§4.4), never as a deletion.

### 9.3 The Name Designation

A name does not inhere in a person. It is an Information Content Entity used to designate a person. This distinction matters when names change, are disputed, or are assigned by different authorities.

| Layer | Entity | Notes |
|---|---|---|
| Reality | The person | Independent continuant |
| Middle Layer | Name ICE + IBE + Assertion Event | Full provenance chain |
| Logic Layer | Name ICE + `is_tokenized_by` | IBE omitted per Section 7.3 |
| Developer view | `fhorgname: "ADMINISTRATIVE CONFERENCE..."` | Flat projection |

If the organization is renamed, the person/org does not change. The original Name ICE may be deprecated. A new ICE is created. A new Assertion Event is recorded. The projection is regenerated. The history of the name change is preserved in the Assertion Event Log.

---

## 10. Belief-Scoped and Counterfactual Reasoning

### 10.1 Distinguishing Quality from Belief

The Quality pattern (Section 5) and belief-scoped reasoning address different cases. The distinction is critical:

| Case | Question | Mechanism |
|---|---|---|
| Quality measurement | Which token does this measurement framework assign to this real Quality? | Quality instance + `is_tokenized_by` |
| Belief scope | Does agent A assert X while agent B asserts not-X? | Separate Assertion Events in different Belief Scopes |
| Contested fact | Is the underlying state of affairs itself uncertain? | Probability on the Belief Process (Section 10.4) |

A status of "ACTIVE" is not a belief. It is a Quality token produced by the FH measurement framework. A different regulatory framework might produce a different token for the same Quality. Neither framework's token is a belief; both are measurements.

An agent asserting "Organization X is government-controlled" while another asserts "Organization X is private" is a belief-scoped case. The disagreement is epistemic.

### 10.2 Beliefs as Semantic Processes

Beliefs are interpretive processes that generate Assertion Events. In the SHML:

- Different agents hold different Belief Scopes
- Each Belief Scope corresponds to a coherent set of Assertion Events in the Middle Layer (§4.3)
- Disagreement between scopes does not imply contradiction in the Reality Layer
- Reality remains singular; beliefs vary

### 10.3 Conditional Reasoning

The system can reason counterfactually across Belief Scopes without crossing them:

- *If Belief Scope A is correct → Conclusion X*
- *If Belief Scope B is correct → Conclusion Y*

Reasoning MUST NOT cross scope boundaries unless the cross-scope comparison is made explicit as a separate reasoning process (§4.3). That explicit process names both scopes as inputs and is itself the only construct permitted to relate them.

### 10.4 Probability and Plausibility

Probability is attached to Belief Processes, not to Reality Layer entities. A Belief Scope MAY carry a confidence value, and conclusions of the comparative form are the goal:

> "If the sensor-based interpretation is correct, shutdown is recommended. If the technician's assessment is correct, continued operation is safe. Based on confidence metrics, the technician's assessment is currently more plausible."

This comparative form requires a **common confidence metric** across the scopes being compared, and an aggregation method over the factors that inform confidence (source reliability, corroboration count, recency, method of inference).

> **[OPEN]** This specification does not define the confidence metric or its aggregation. It establishes only (a) that probability attaches to the Belief Process, never to the Reality Layer entity, and (b) that cross-scope plausibility comparison presupposes a shared metric. The metric and aggregation — candidate: a value in [0,1] with named operators (e.g., noisy-OR over independent corroboration, decay over recency) — are specified in a separate confidence-model specification. Until that specification is adopted, an implementation MUST NOT present cross-scope plausibility comparisons as quantitatively grounded; it MAY present them as qualitative only.

This form of reasoning is not representable in predicate-centric logic without collapsing the distinction between the quality, the measurement, and the agent's confidence in it.

---

## 11. What This Architecture Refuses

A conformant implementation MUST NOT:

1. **Assert `has_text_value` (`cco:ont00001765`) on ICE instances.** The domain of `has_text_value` is IBE (`cco:ont00000253`). Use `is_tokenized_by` (`cco:ont00001761`) for Logic Layer projections.

2. **Create subclasses for administrative categories.** Org type, status, and classification are roles or qualities, not universals. A class represents a real kind of thing in the world. "Department/Ind. Agency" is a governance label, not a natural kind.

3. **Assert history nodes without timestamp data.** `obo:BFO_0000182` history nodes MUST carry at least one populated temporal instant. Vacuous history nodes — typed but unpopulated — are a semantic honesty violation.

4. **Treat Logic Layer triples as ontological primitives.** Every triple in the Logic Layer is a projection, not a fact. It is traceable to a producing Assertion Event.

5. **Collapse belief into truth.** An agent's assertion is always scoped to that agent's Belief Process. A belief is not a global truth claim.

6. **Encode uncertainty as weakened facts.** Uncertainty belongs on the Belief Process (as a confidence measure), not on the predicate.

7. **Allow stale projections to persist after retraction.** When a producing Assertion Event is retracted, the downstream projection MUST be regenerated or marked stale.

8. **Silently collapse conflicting projection values.** Conflicts between Assertion Events that produce different values for the same projection field MUST be surfaced (§8.6) or scoped to a specific Belief Scope.

9. **Emit a rule-derived field without declaring its rule.** A projection field computed by a rule rather than read from a graph pattern (e.g., a status computed by a state machine over process membership) MUST declare the rule in its Scope Declaration, and the field's value MUST be traceable to that rule and to the Assertion Events the rule consumed. A rule-derived field presented as if read directly from the graph is a semantic honesty violation (Appendix B.5).

10. **Mutate a published Assertion Event.** Correction and retraction are new Assertion Events, never edits or deletions (§4.4). A mutated event breaks content-addressed federation and erases history.

---

## 12. System Implementation

The principles of the SHML are realized through the following technical specifications within the Fandaws Ontology Service ecosystem:

| Component | Role |
|---|---|
| **Fandaws 3.0** | Runtime negotiation — dynamic grounding of terms between layers |
| **Semantic Data Dictionaries v2.0** | Data mapping — operationalizes the forward transform from source records to Assertion Events |
| **Generative Concretization v2.0** | AI integration — treats LLM outputs as candidate content within the Middle Layer, subject to Assertion Event provenance requirements |
| **FNSR Inter-Service Protocol (ISP)** | Transport — governs how Assertion Events move between services in the federated network |
| **HIRI Protocol** | Identity — grounds entity identity across the three layers, and across federated layered/flat nodes (§3.4), via cryptographic key documents |
| **Content-Addressed Storage (IPFS)** | Federation — Assertion Events as immutable CID-addressable records; the Provenance Index as a Merkle-DAG (§4.4) |

---

## Appendix A: Worked Example — Federal Hierarchy Organization

This appendix demonstrates the full SHML architecture applied to a real government data record. All CCO 2.0 IRIs are verified against `CommonCoreOntologiesMerged.ttl` v2.0-2024-11-06.

### A.1 Source Record

```json
{
  "fhorgid":    300000057,
  "fhorgname":  "ADMINISTRATIVE CONFERENCE OF THE U. S.",
  "fhorgtype":  "Department/Ind. Agency",
  "agencycode": "9515",
  "cgac":       "302",
  "status":     "ACTIVE",
  "level":      0,
  "children":   [ { "fhorgid": 300000368, "..." : "..." } ]
}
```

### A.2 Verified CCO 2.0 IRI Map

| CCO 1.x label | CCO 2.0 IRI | `rdfs:label` | Notes |
|---|---|---|---|
| `GovernmentOrganization` | `cco:ont00000408` | "Government Organization" | Direct match |
| `InformationContentEntity` | `cco:ont00000958` | "Information Content Entity" | Direct match |
| N/A | `cco:ont00000649` | "Non-Name Identifier" | Grandparent of code identifiers |
| N/A | `cco:ont00000077` | "Code Identifier" | Direct parent of FhOrgId, AgencyCode, CGAC |
| `ProperName` | `cco:ont00001014` | "Proper Name" | Parent of FederalOrganizationProperName |
| `has_text_value` | `cco:ont00001765` | "has text value" | `domain=IBE` — MUST NOT use on ICE |
| `is_tokenized_by` | `cco:ont00001761` | "is tokenized by" | `AnnotationProperty` — use this instead |

> **Note:** `IdentifierInformationContentEntity` does not exist in CCO 2.0. The correct parent for system-assigned code identifiers is `cco:ont00000077` (Code Identifier), which subclasses `cco:ont00000649` (Non-Name Identifier).

### A.3 Class Declarations (T-Box)

```turtle
# Identifier subclasses
fh:FhOrgIdentifier
    a owl:Class ;
    rdfs:subClassOf cco:ont00000077 ;
    rdfs:label "Federal Hierarchy Organization Identifier"@en .

fh:AgencyCode
    a owl:Class ;
    rdfs:subClassOf cco:ont00000077 ;
    rdfs:label "Agency Code"@en .

fh:CommonGovernmentAccountingClassificationCode
    a owl:Class ;
    rdfs:subClassOf cco:ont00000077 ;
    rdfs:label "Common Government-wide Accounting Classification Code"@en ;
    skos:altLabel "CGAC"@en .

# Name subclass
fh:FederalOrganizationProperName
    a owl:Class ;
    rdfs:subClassOf cco:ont00001014 ;
    rdfs:label "Federal Organization Proper Name"@en .

# Status Quality
fh:FederalOrganizationalOperationalStatus
    a owl:Class ;
    rdfs:subClassOf obo:BFO_0000019 ;
    rdfs:label "Federal Organizational Operational Status"@en .
```

### A.4 Role Individuals (A-Box, shared)

```turtle
# One individual per governance role — declared once, shared across all org instances
fh:FederalDepartmentOrIndependentAgencyRole
    a obo:BFO_0000023 ;
    rdfs:label "Federal Department or Independent Agency Role"@en ;
    skos:altLabel "Department/Ind. Agency"@en .

fh:FederalSubTierOrganizationRole
    a obo:BFO_0000023 ;
    rdfs:label "Federal Sub-Tier Organization Role"@en ;
    skos:altLabel "Sub-Tier"@en .

fh:FederalOrganizationalOfficeRole
    a obo:BFO_0000023 ;
    rdfs:label "Federal Organizational Office Role"@en ;
    skos:altLabel "OFFICE"@en .
```

> **Identity scope reminder:** These individuals are scoped to the FH governance framework. They MUST NOT be equated with role individuals from other governance frameworks without an explicit alignment assertion. See §6.4 on the role-type-as-named-individual pattern: sharing a role individual means sharing a role *type*, not any stronger identity.

### A.5 Logic Layer Output (A-Box, per org)

```turtle
# Org instance
fh:org_300000057
    a cco:ont00000408 ;
    obo:RO_0000053 fh:FederalDepartmentOrIndependentAgencyRole ;
    obo:RO_0000053 fh:status_300000057 ;
    obo:IAO_0000235 fh:name_300000057 ;
    obo:IAO_0000235 fh:fhorgid_300000057 ;
    obo:IAO_0000235 fh:agencycode_300000057 ;
    obo:IAO_0000235 fh:cgac_300000057 .

# Status Quality — inheres in org
fh:status_300000057
    a fh:FederalOrganizationalOperationalStatus ;
    obo:RO_0000052 fh:org_300000057 ;
    cco:ont00001761 "ACTIVE"^^xsd:string .

# Name ICE
fh:name_300000057
    a fh:FederalOrganizationProperName ;
    cco:ont00001761 "ADMINISTRATIVE CONFERENCE OF THE U. S."^^xsd:string .

# FhOrgId ICE
fh:fhorgid_300000057
    a fh:FhOrgIdentifier ;
    cco:ont00001761 "300000057"^^xsd:integer .

# AgencyCode ICE
fh:agencycode_300000057
    a fh:AgencyCode ;
    cco:ont00001761 "9515"^^xsd:string .

# CGAC ICE
fh:cgac_300000057
    a fh:CommonGovernmentAccountingClassificationCode ;
    cco:ont00001761 "302"^^xsd:string .
```

### A.6 Node Count

| Node | Type | Count |
|---|---|---|
| `fh:org_X` | `cco:ont00000408` | 1 per org |
| `fh:status_X` | `fh:FederalOrganizationalOperationalStatus` | 1 per org |
| `fh:name_X` | `fh:FederalOrganizationProperName` | 1 per org |
| `fh:fhorgid_X` | `fh:FhOrgIdentifier` | 1 per org |
| `fh:agencycode_X` | `fh:AgencyCode` | 1 per org |
| `fh:cgac_X` | `fh:CommonGovtAccountingClassCode` | 1 per org |
| Role individuals | `obo:BFO_0000023` | 3 total (shared) |
| **Total per org** | | **6** |

---

## Appendix B: Projection Loss Model

A projection is lossless within its declared scope. "Lossless within scope" is not a vague claim — it requires an explicit accounting of what is preserved and what is intentionally dropped.

### B.1 Fields Preserved in the Forward Projection

| Source field | Preserved as | Recovery via CONSTRUCT |
|---|---|---|
| `fhorgid` | `fh:FhOrgIdentifier` ICE with `is_tokenized_by` | ✅ Full recovery |
| `fhorgname` | `fh:FederalOrganizationProperName` ICE with `is_tokenized_by` | ✅ Full recovery |
| `fhorgtype` | `skos:altLabel` on Role individual | ✅ Full recovery |
| `agencycode` | `fh:AgencyCode` ICE with `is_tokenized_by` | ✅ Full recovery |
| `cgac` | `fh:CommonGovtAccountingClassCode` ICE with `is_tokenized_by` | ✅ Full recovery |
| `status` | `fh:FederalOrganizationalOperationalStatus` Quality with `is_tokenized_by` | ✅ Full recovery |
| `children` (hierarchy) | `obo:BFO_0000050` (part_of) | ✅ Full recovery (via reverse query) |

### B.2 Fields Intentionally Dropped

| Source field | Reason for omission | Derivable from graph |
|---|---|---|
| `level` | Integer depth in source hierarchy. Carries no information not present in the `part_of` chain. | ✅ Computable via SPARQL depth query |

### B.3 Information Not in Source Data (Not Assertable)

| Information | Why not asserted |
|---|---|
| Temporal extent of status | Source data carries no timestamps. History nodes MUST NOT be asserted without this data. |
| Physical carrier of name/code strings | Source data identifies no IBE. Full ICE+IBE chain not constructable. |
| Agent of assertion | Transform is automated; no human agent is identified in the source. |

### B.4 Collision Rules

The source data as structured contains one value per field per org. No collision rules are triggered in the baseline case. If future versions of the source data introduce multiple values for a single field, the following rules apply:

- Multiple names: all are asserted as separate `fh:FederalOrganizationProperName` instances; the projection MUST declare a selection rule (e.g., most recent, preferred)
- Multiple status values: treated as a conflict requiring Belief Scope assignment before projection (emitted per §8.6)

### B.5 Derived-by-Rule Fields

Beyond fields that are preserved, dropped, or derivable by query, a projection MAY emit fields that are **computed by a declared rule** and are present in neither the source data nor any single graph pattern.

| Example field | Rule | Inputs |
|---|---|---|
| `status: "In Transit"` | State machine over process membership: a shipment is *In Transit* when its transport process has started and its receiving process has not | The Assertion Events asserting the relevant process memberships |

These are the most dangerous fields in a projection: they carry the appearance of a directly-observed value while in fact being the output of a rule that exists outside the graph. Requirement:

- The rule MUST be declared in the Scope Declaration.
- The emitted value MUST be traceable to the rule and to the Assertion Events the rule consumed (via `_derived_from`, §8.5).
- A rule-derived field MUST NOT be presented as if read directly from a graph pattern.

A projection that emits a rule-derived field without a declared rule is non-conformant (C-15, §11(9)).

---

## Appendix C: Conformance Requirements Summary

A conformant SHML implementation MUST satisfy the following requirements:

| ID | Section | Requirement |
|---|---|---|
| C-01 | 3.3 | Logic Layer projections MUST be regenerated or marked stale when producing Assertion Events are retracted |
| C-02 | 5.3 | History nodes MUST NOT be asserted without populated temporal instant data |
| C-03 | 5.3 | Status MUST be modeled as a `obo:BFO_0000019` Quality subclass instance inhering in the org |
| C-04 | 7.2 | `cco:ont00001765` MUST NOT be asserted on any instance typed as a subclass of `cco:ont00000958`. ICE and IBE occupy disjoint BFO continuant branches; the prohibition is absolute. If the deployed CCO does not axiomatize this disjointness, the implementation MUST add the disjointness axiom so the prohibition is reasoner-enforced. |
| C-05 | 7.3 | `cco:ont00001761` MUST be used for literal values on ICE and Quality instances in Logic Layer projections |
| C-06 | 8.4 | Each projection MUST declare its scope — the patterns it captures and the fields it intentionally omits |
| C-07 | 8.4 | Projection collision rules MUST be explicit and documented |
| C-08 | 6.4 | Role individuals MUST declare identity scope; cross-framework equivalence MUST use explicit alignment assertions |
| C-09 | 10.1 | Belief-scoped assertions MUST NOT be collapsed with Quality measurements |
| C-10 | 11 | Subclasses MUST NOT be created for administrative categories; use Role individuals or Quality instances |
| C-11 | 4.4 | A published Assertion Event MUST NOT be mutated |
| C-12 | 4.4 | Retraction MUST be expressed as a new Assertion Event referencing the retracted event, not as deletion or mutation |
| C-13 | 4.4 | The Provenance Index MUST be derivable as a verifiable DAG over Assertion Event identifiers |
| C-14 | 4.3 | A Belief Scope MUST be identified by (agent, interpretive framework, temporal window); scopes MUST be flat (no nesting); cross-scope reasoning MUST be an explicit, named process |
| C-15 | B.5 | Rule-derived projection fields MUST declare their rule and be traceable to it and to the Assertion Events it consumed |
| C-16 | 8.1 | The Scope Declaration is the source of truth; the JSON-LD context, CONSTRUCT query, forward transform, and conformance test cases MUST be derivable from it |
| C-17 | 8.5 | Every emitted projection MUST carry the provenance envelope |
| C-18 | 8.6 | Conflicting field values MUST be emitted as `null` with a populated `_conflicts` block; they MUST NOT be silently chosen |

---

*End of SHML Specification v3.3 · Fandaws Ontology Service · Ontology of Freedom Initiative*
