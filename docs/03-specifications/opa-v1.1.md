# Ontological Placement Agent (OPA)
## Functional Specification — Version 1.2

| Field | Value |
|---|---|
| Date | March 2026 |
| Status | HARDENED DRAFT (Pre-Final) |
| Supersedes | v1.1 (March 2026) |
| Component Role | Autonomous Concept Naming and BFO Placement Service |
| Component Scope | Fandaws-internal (see §1.3) |
| Target System | Fandaws v3.4 |
| Primary Upstream | TagTeam.js v3.0+ / Fandaws Type Agent v2.3 |
| Edge-Canonical | Partial — see §2.3 |

---

## Version History

| Version | Date | Change Type | Summary |
|---|---|---|---|
| 1.2 | March 2026 | Portfolio Coherence Review — 6 Advisories | `fandaws-opa:designates` formalized as `rdfs:subPropertyOf IAO:is_about` with definitional note (§5.4). Stage 3 graceful degradation path added (§Stage 3). DefinedClass re-entry workflow specified (§4B.5). FNSR CloudEvents emission added at service boundary (§6.5). KL-003 concurrent race dependency chain clarified. Component scope declared as Fandaws-internal with cross-boundary contract note (§1.3). OPA-CAP-011 added. KL-005 added. |
| 1.1 | March 2026 | SME Review — Realist Ontology Critique | Two-layer output architecture introduced (Universal + ConceptDesignation). Universal Classification Gate added as Stage 4B. DefinedClass route added with forced agent-review policy. §5.3 Universal Classification Rules normative. Output contract §6 completely revised to emit two-node GraphMutations. OPA-CAP-008 through OPA-CAP-010 added. TT-GAP-006 added. |
| 1.0 | March 2026 | Initial Draft | Seven-stage pipeline specified. TagTeam integration contract defined. BFO traversal algorithm specified. Relation correction table normative. Confidence aggregation policy defined. Required gaps in TagTeam and Fandaws formally catalogued. |

---

## SME1 Critique — Resolution Summary

| Risk ID | Risk | Resolved In | Resolution |
|---|---|---|---|
| R1 | Defined-class proliferation — the pipeline produces any concept with a valid genus-differentia without testing whether it represents a natural kind or a mere intersection of accidental properties | §4 Stage 4B, §5.3 | Universal Classification Gate added between Stage 4 and Stage 5. Classifies every candidate as NaturalKind, RoleUniversal, ArtifactType, or DefinedClass. DefinedClass concepts are ineligible for auto-commit and are routed to agent review regardless of PlacementConfidence. |
| R2 | Universal vs. name conflation — confidence scores, reasoning traces, and provenance are properties of a representation of a universal, not of the universal itself. Attaching them to the concept node conflates the entity in reality with the information artifact used to refer to it. | §6, §7, §9 | Two-layer output architecture introduced. Every OPA placement produces two graph nodes: a `fandaws:Universal` (ontology layer — carries only subClassOf, definition, and BFO placement) and a `fandaws:ConceptDesignation` (vocabulary layer — carries all provenance, confidence, reasoning trace, and normative flags, and designates the Universal via `fandaws-opa:designates`). |
| R3 | Implicit punning — the current design allows a single identifier to function simultaneously as an ontology class, a graph node with metadata, and a vocabulary term | §6 | Resolved by R2 separation. The Universal node carries no metadata. The ConceptDesignation node carries no ontological assertions. No node serves dual purposes. |

---

## Portfolio Coherence Review — v1.2 Advisories Addressed

| Advisory | Issue | Resolution | Sections Changed |
|---|---|---|---|
| D1 | `fandaws-opa:designates` is novel — no formal relation to IAO:is_about | Declared `rdfs:subPropertyOf IAO:is_about` with definitional note explaining why specialization is required | §5.4 (new), §6.2 note |
| D2 | No graceful degradation path for Stage 3 when IVNE vocabularies unavailable | Added normative degradation branch: Stage 3 returns `{ found: false, confidence: 0.0 }` when no vocabularies are loaded | §Stage 3 algorithm |
| D3 | DefinedClass → NaturalKind re-entry workflow unspecified | Added §4B.5 Redefinition Re-entry Workflow with RedefinitionRequest contract and pipeline re-entry from Stage 2 | §4B.5 (new) |
| D4 | No FNSR CloudEvents emission at service boundary | Added §6.5 with `fnsr.concept.placed`, `fnsr.concept.review-requested`, and `fnsr.concept.escalated` CloudEvents | §6.5 (new), OPA-CAP-011 |
| D5 | KL-003 concurrent race — dependency between serialized queue and OPA-CAP-010 unclear | Rewritten with explicit dependency chain: serialized Stage 1 is the primary fix, OPA-CAP-010 is defense-in-depth for crash recovery | §KL-003 rewritten |
| D6 | No FNSR spec conventions or component scope declaration | Added §1.3 Component Scope declaring Fandaws-internal status with cross-boundary contract note for IEE, Causal OS Kernel, and BAM | §1.3 (new), header |

---

## 1. Executive Summary

The Ontological Placement Agent (OPA) is the FNSR service that closes the gap between statistical concept detection and formal ontological commitment. It sits between the Fandaws Type Agent and the Fandaws Knowledge Engine, receiving concept nominations from two upstream sources — the Type Agent (which detects convergence from data) and TagTeam.js (which detects universals from text) — and producing fully-formed GraphMutations that commit both a Universal to the ontology layer and a ConceptDesignation to the vocabulary layer.

The OPA's purpose is to eliminate the human steward from the primary concept placement loop. It does this by replicating the cognitive acts a skilled knowledge steward would perform: checking whether the concept already exists, inducing the universal from available evidence, aligning to authoritative external vocabularies, constructing a genus-differentia definition, classifying the candidate's ontological status, and testing the definition against the BFO hierarchy.

The OPA does not guess. Every placement decision is accompanied by a structured reasoning trace attached to the ConceptDesignation, and a confidence score. When confidence falls below the configured threshold, the OPA escalates to a higher-tier reasoning agent rather than committing an uncertain result.

### 1.1 What the OPA Eliminates

| Task Previously Requiring Human Judgment | OPA Mechanism |
|---|---|
| Recognizing that `emp_role`, `employees_title`, and `role` are the same concept | Stage 1: Semantic Existence Search |
| Determining that `engineer` and `manager` are instances of `JobTitle`, not the concept itself | Stage 2: Universal Induction from TagTeam genericity output |
| Checking whether an authoritative standard already names the concept | Stage 3: External Vocabulary Alignment |
| Formulating a genus-differentia definition | Stage 4: Definitional Synthesis |
| Determining whether the candidate represents a real natural kind or a defined class | Stage 4B: Universal Classification Gate |
| Testing which BFO class is the most specific valid parent | Stage 5: BFO Subsumption Traversal |
| Deciding whether confidence is sufficient to commit or escalate | Stage 6: Confidence Aggregation |

### 1.2 What the OPA Does Not Do

The OPA does not perform moral or normative reasoning over the concepts it places. Concepts that participate in domains with normative significance — obligations, rights, agency, harm — are flagged for IEE review post-placement. The placement itself is structural and definitional.

The OPA does not replace the Fandaws semantic firewall for conversationally-created concepts. It operates exclusively on programmatically-detected nominations from the Type Agent or TagTeam.

### 1.3 Component Scope *(new in v1.2)*

The OPA is a **Fandaws-internal component**, not a standalone FNSR service. It does not have its own FNSR service tier, ARIADNE 7-check, or independent deployment unit. It is specified, versioned, and deployed as part of the Fandaws v3.4 subsystem alongside the Type Agent and the Knowledge Engine.

However, the OPA's outputs cross FNSR service boundaries in three ways:

| Cross-Boundary Consumer | Interface | Contract |
|---|---|---|
| **IEE** | `fandaws-opa:normativeFlag: true` on ConceptDesignation; DefinedClass agent-review prompts involving normative domains | OPA-CAP-006 (IEE notification interface). IEE subscribes to `fnsr.concept.placed` CloudEvents where `normativeFlag = true`. |
| **Causal OS Kernel** | Escalation requests for PlacementConfidence < 0.60 | OPA emits `fnsr.concept.escalated` CloudEvent. Causal OS Kernel subscribes. |
| **BAM / IS / other FNSR services** | Concept placement events for behavioral monitoring and interpretability tracking | `fnsr.concept.placed` CloudEvent at the Fandaws service boundary (§6.5). No direct OPA API exposure. |

These cross-boundary interactions use the FNSR CloudEvents contract (§6.5), not direct OPA API calls. External FNSR services never invoke OPA stages directly — they subscribe to events emitted at the Fandaws boundary.

---

## 2. Architectural Position

### 2.1 Position in the FNSR Pipeline

```
PATH A — Statistical Detection:
Type Agent (SGW convergence) → OPA Nomination Request (statistical)

PATH B — Definitional Parsing:
TagTeam.js (requiresOntologyResolution: true) → OPA Nomination Request (definitional)

BOTH PATHS →
  Stage 1:  Semantic Existence Search
  Stage 2:  Universal Induction
  Stage 3:  External Vocabulary Alignment
  Stage 4:  Definitional Synthesis
  Stage 4B: Universal Classification Gate        ← NEW in v1.1
  Stage 5:  BFO Subsumption Traversal
  Stage 6:  Confidence Aggregation
       │
       ├── NaturalKind / RoleUniversal / ArtifactType
       │     ├── PlacementConfidence ≥ 0.80  →  GraphMutation: Universal + ConceptDesignation (auto-commit)
       │     ├── PlacementConfidence 0.60–0.80 → ConversationPrompt (agent review)
       │     └── PlacementConfidence < 0.60   →  Causal OS Kernel / IEE escalation
       │
       └── DefinedClass (any confidence)     →  ConversationPrompt (forced agent review)
```

### 2.2 Relationship to Existing FNSR Services

| Service | Relationship to OPA |
|---|---|
| Type Agent v2.3 | Primary statistical upstream. Provides token evidence and convergence metrics. The OPA receives a nomination when PS ≥ autoPromote threshold or when a human has approved a human-hold prompt. All Type Agent outputs carry `fnsr:taintLevel: "L3"` (see Type Agent v2.3 §6.1). |
| TagTeam.js v3.0+ | Primary definitional upstream. The OPA subscribes to TagTeam outputs flagged `requiresOntologyResolution: true`. Provides the strongest definitional evidence available. |
| IVNE | The OPA queries the IVNE-imported class graph for Stage 1 semantic search and Stage 3 external vocabulary alignment. BFO, CCO, IAO, and configured domain vocabularies must be pre-loaded. |
| Fandaws Knowledge Engine | The OPA's sole output consumer. The OPA emits GraphMutations and ConversationPrompts to the OrchestrationAdapter. It never writes to the Fandaws graph directly. |
| Termidium | The OPA's Stage 1 search uses Termidium's deduplication index to detect structural overlap with existing concepts. Read-only. |
| Causal OS Kernel | Escalation target for low-confidence placements and placements involving causal or process-class ambiguity. |
| IEE | Post-placement notification target for concepts flagged as normatively significant. Also receives all DefinedClass agent-review prompts where the definition involves normative domains. |

### 2.3 Edge-Canonical Status

The OPA is **partially** edge-canonical. Stages 1–4B and Stage 6 are implementable as pure in-memory computation over the Fandaws graph snapshot. Stage 5 (BFO Subsumption Traversal) requires an OWL reasoner for full conformance. The reference implementation uses a lightweight structural traversal algorithm (§Stage 5) that does not require a full DL reasoner and is edge-canonical. Full DL reasoning via HermiT or Pellet is an optional server-deployment enhancement. See §9, **OPA-CAP-002**.

---

## 3. Nomination Contracts

### 3.1 Type Agent Nomination

```json
{
  "@type": "fandaws-opa:NominationRequest",
  "fandaws-opa:nominationSource":  "type-agent",
  "fandaws-opa:nominationBasis":   "statistical-convergence",

  "fandaws-opa:statisticalEvidence": {
    "fandaws-ta:sgwId":            "a3f91bc204e87d1a",
    "fandaws-ta:promotionScore":    0.83,
    "fandaws-ta:memberKeys": [
      "hr_database_v1:HRM",
      "finance_db_v2:employees_title",
      "ms_graph_v1:role"
    ],
    "fandaws-ta:centroid": {
      "fandaws-ta:frequentTokens":  ["engineer", "manager", "contractor", "director"],
      "fandaws-ta:entropy":          2.14,
      "fandaws-ta:cardinalityRatio": 0.0056,
      "fandaws-ta:modalSasType":    "viz:NominalType"
    },
    "fandaws-ta:sourceSystemDomains": ["hr", "hr", "directory"]
  },

  "fandaws-opa:requestedAt": "2026-03-14T11:24:00Z",
  "fandaws-opa:policyId":    "fandaws-ta:policy/production-v1"
}
```

> **Gap Note:** `fandaws-ta:sourceSystemDomains` is not in the Type Agent v2.3 ObservedAttribute schema. Must be added. See §10, **TT-GAP-004** and Type Agent gap register **FTA-GAP-001**.

### 3.2 TagTeam Nomination

```json
{
  "@type": "fandaws-opa:NominationRequest",
  "fandaws-opa:nominationSource":  "tagteam",
  "fandaws-opa:nominationBasis":   "definitional-parse",

  "fandaws-opa:tagteamEvidence": {
    "tagteam:entityId":              "inst:Entity_Job_Title_6ee9379ab302",
    "tagteam:nominatedClassLabel":   "Job Title",
    "tagteam:nominationBasis":       "unknown",
    "tagteam:genericityCategory":    "GEN",
    "tagteam:genericityConfidence":   0.75,
    "tagteam:classNominationStatus": "unresolved",

    "tagteam:ibeParsed": {
      "@id":                "inst:Input_Text_IBE_1601cfaa9b6e",
      "has_text_value":     "Job Title is A specific designation of a post within an organization, normally associated with a job description that details the tasks and responsibilities that go with it.",
      "tagteam:isDefinitional": true
    },

    "tagteam:structuralAssertions": [
      {
        "tagteam:pattern":   "predication",
        "tagteam:copula":    "is",
        "assertionSubject":  "inst:Job_Title",
        "assertionObject":   "inst:a_post",
        "assertedRelation":  "member_part_of"
      }
    ],

    "tagteam:conceptualNeighborhood": [
      { "label": "post",                     "relation": "member_part_of" },
      { "label": "organization",             "relation": "nmod" },
      { "label": "job description",          "relation": "associated_with" },
      { "label": "tasks and responsibility", "relation": "details" }
    ]
  },

  "fandaws-opa:requestedAt": "2026-03-14T11:24:00Z"
}
```

---

## 4. The Seven-Stage Pipeline

### Stage 1 — Semantic Existence Search

**Purpose:** Determine whether the nominated concept already exists in the Fandaws graph. If it does, the OPA maps to the existing Universal and exits without creating new nodes.

**Algorithm:**

```
FUNCTION semanticExistenceSearch(nomination, fandawsGraph):

  1. EXACT LABEL SEARCH
     Query fandawsGraph for any fandaws:Universal where:
       rdfs:label = normalize(nomination.nominatedClassLabel) (case-insensitive)
     IF match found WITH confidence >= 0.95:
       RETURN ExistenceResult { found: true, matchedUniversal: IRI,
                                matchType: "exact-label" }

  2. TOKEN OVERLAP SEARCH (type-agent nominations)
     For each existing fandaws:Universal with exemplar tokens:
       score = Jaccard(nomination.centroid.frequentTokens, universal.exemplarTokens)
     IF max(score) >= 0.70:
       RETURN ExistenceResult { found: true, matchedUniversal: IRI,
                                matchType: "token-overlap", confidence: max(score) }

  3. NEIGHBORHOOD ALIGNMENT SEARCH
     Query Termidium deduplication index using conceptual neighborhood labels.
     IF alignment score >= threshold:
       RETURN ExistenceResult { found: true, matchedUniversal: IRI,
                                matchType: "neighborhood-alignment",
                                confidence: alignmentScore }

  4. NO MATCH
     RETURN ExistenceResult { found: false }
```

**On Found:** The OPA emits a `fandaws:GraphMutation` adding a new `fandaws:ConceptDesignation` node that `fandaws-opa:designates` the existing Universal. No new Universal is created. Pipeline exits.

**On Not Found:** Proceed to Stage 2.

---

### Stage 2 — Universal Induction

**Purpose:** Determine what universal the nominated tokens or definition instantiate — the *type*, not the instances. For TagTeam nominations with `genericityCategory: GEN`, this is largely pre-solved. For Type Agent nominations, the OPA induces the universal from token and domain evidence.

#### 2A — TagTeam Path (Definitional)

```
FUNCTION induceUniversalFromDefinition(tagteamEvidence):

  1. USE nominatedClassLabel as candidate universal label.
     Canonicalize: UpperCamelCase singular form.
     "Job Title" → "JobTitle"

  2. EXTRACT genus from IBE text directly when structural assertion
     genus is a nominal modifier rather than the predicate head.
     (Relation correction table §5.2 applied here.)
     "designation of a post" → genus = "designation"

  3. EXTRACT differentia from conceptualNeighborhood minus the genus:
     { organization, job description, tasks and responsibility }

  4. RETURN InductionResult {
       candidateLabel:   "JobTitle",
       genus:            "designation",
       differentia:      [...],
       confidence:       tagteamEvidence.genericityConfidence
     }
```

#### 2B — Type Agent Path (Statistical)

```
FUNCTION induceUniversalFromTokens(statisticalEvidence):

  1. DOMAIN-CONDITIONED CANDIDATE SPACE
     Use sourceSystemDomains to constrain candidate concept space.

  2. EXEMPLAR MATCHING against loaded domain vocabularies.
     Query IVNE-loaded vocabularies for classes whose exemplar values
     overlap with centroid.frequentTokens.

  3. RESOLVE genus from best-matching vocabulary class.

  4. RETURN InductionResult { candidateLabel, genus, differentia, confidence }
```

---

### Stage 3 — External Vocabulary Alignment

**Purpose:** Before minting a new Universal, determine whether an authoritative external vocabulary has already named the concept. Borrow name and definition if available. Cite the alignment.

**Loaded vocabularies (priority order):**

| Priority | Vocabulary | Scope | Alignment Relation |
|---|---|---|---|
| 1 | BFO 2020 | Upper ontology | `rdfs:subClassOf` |
| 2 | CCO | Mid-level | `rdfs:subClassOf` or `skos:exactMatch` |
| 3 | IAO | Information entities | `skos:exactMatch` |
| 4 | O*NET-SOC | Occupational classifications | `skos:closeMatch` |
| 5 | ISCO-08 | International occupation standard | `skos:closeMatch` |
| 6 | Domain vocabularies | Domain-specific | `skos:relatedMatch` |

```
FUNCTION externalVocabularyAlignment(inductionResult, loadedVocabularies):

  // v1.2 — Graceful degradation when IVNE vocabularies are unavailable
  IF loadedVocabularies IS EMPTY OR loadedVocabularies IS UNAVAILABLE:
    LOG "Stage 3 degraded: no vocabularies loaded (OPA-CAP-001 not satisfied)"
    RETURN AlignmentResult { found: false, confidence: 0.0,
                             degraded: true, reason: "no-vocabularies-loaded" }

  FOR EACH vocabulary V (priority order):
    1. Search by label match against inductionResult.candidateLabel.
    2. Search by definition overlap against genus + differentia.
    3. alignmentScore = label_similarity × 0.4 + definition_overlap × 0.6

    IF alignmentScore >= 0.85:
      RETURN AlignmentResult { alignedConcept: IRI, relation: "skos:exactMatch",
                               confidence: alignmentScore, source: V.identifier }

    IF alignmentScore >= 0.65: RECORD as closeMatch candidate, continue.

  IF no exactMatch: RETURN best closeMatch or { found: false }
```

> **Degradation behavior (v1.2 — normative):** When OPA-CAP-001 (vocabulary query API) is not satisfied, Stage 3 returns `{ found: false, confidence: 0.0, degraded: true }` and the pipeline proceeds to Stage 4. The effect on PlacementConfidence is a loss of `w3 × alignmentConfidence` (default: up to 0.25 of the total score). In practice, this means most placements without external vocabulary alignment will score below the 0.80 auto-commit threshold and route to agent review — which is the correct conservative behavior. The `degraded: true` flag is recorded in the ReasoningTrace (§7) so downstream consumers can distinguish "no alignment found" from "alignment not attempted."

> **Future Capability Dependency:** Requires vocabulary query API over IVNE-loaded ontologies. See §9, **OPA-CAP-001**.

---

### Stage 4 — Definitional Synthesis

**Purpose:** Construct a well-formed genus-differentia definition that will drive Stage 4B classification and Stage 5 traversal, and that will be stored on the committed Universal node.

```
FUNCTION definitionalSynthesis(inductionResult, alignmentResult):

  1. DETERMINE GENUS IRI:
     IF alignmentResult.confidence >= 0.85:
       genus = alignmentResult.alignedConcept
     ELSE:
       genus = map via BFO branch lookup table (§5.1)

  2. CONSTRUCT DIFFERENTIA as OWL restrictions:
     "of a post"             → someValuesFrom(opa:designates, fandaws:concept/Post)
     "within an organization"→ someValuesFrom(opa:existsWithin, CCO:Organization)
     "associated with..."    → someValuesFrom(opa:associatedWith, ...)

  3. SYNTHESIZE natural-language definition:
     "[CandidateLabel] is [genus] that [differentia in prose]."

  4. VALIDATE:
     - No fabricated IRIs
     - No circular definitions
     - Non-empty differentia

  5. RETURN DefinitionResult {
       canonicalLabel, displayLabel, genus, differentia,
       definitionText, confidence
     }
```

**Synthesis confidence:**
```
synthConfidence = (genusConfidence × 0.5)
                + (differentiaCompleteness × 0.3)
                + (alignmentConfidence × 0.2)
```

---

### Stage 4B — Universal Classification Gate *(new in v1.1)*

**Purpose:** Before BFO placement, classify the candidate concept into one of four ontological categories. This gate determines whether the candidate represents a genuine universal — a type that exists in reality and supports stable inductive generalizations — or a defined class assembled from accidental property intersections.

Only NaturalKind, RoleUniversal, and ArtifactType are eligible for auto-commit. DefinedClass concepts must be routed to agent review regardless of PlacementConfidence.

#### 4B.1 Universal Category Definitions

| Category | Ontological Description | Examples | Auto-Commit Eligible |
|---|---|---|---|
| `NaturalKind` | A type whose instances share essential properties that are causally or structurally grounded. Supports stable inductive generalizations across instances. | Person, Organization, Process, InformationContentEntity, Disease | Yes |
| `RoleUniversal` | A type that exists relationally — inhering in a bearer by virtue of a contextual relationship. Carries obligations and normative structure. | JobTitle (as ICE), ManagerRole, PatientRole, OfficerRole | Yes, with IEE normative flag |
| `ArtifactType` | A type defined by function and design intent. Instances are created to fulfill a purpose. | Vehicle, MedicalDevice, Document, Specification | Yes |
| `DefinedClass` | A class defined by intersection of accidental properties with no causal or functional grounding. Does not correspond to a natural kind or functional type. | TallRedheadedViolinist, LeftHandedDiabeticFirefighter | **No — forced agent review** |

#### 4B.2 Classification Algorithm

```
FUNCTION classifyUniversal(definitionResult):

  APPLY TESTS IN ORDER:

  TEST 1 — Genus-driven classification (highest priority):
    IF genus ∈ BFO/CCO Role hierarchy:
      RETURN { category: "RoleUniversal", confidence: 0.90 }

    IF genus ∈ IAO/CCO InformationContentEntity hierarchy:
      RETURN { category: "NaturalKind", confidence: 0.85 }
        // ICEs are genuine universals — they are types of information artifacts

    IF genus ∈ CCO Artifact hierarchy:
      RETURN { category: "ArtifactType", confidence: 0.85 }

    IF genus ∈ BFO/CCO Process or Agent or Object hierarchy:
      RETURN { category: "NaturalKind", confidence: 0.80 }

  TEST 2 — Differentia character analysis:
    accidentalCount = count of differentia that are:
      - value restrictions on observable properties (color, height, weight, age)
      - OR arbitrary combinations of properties with no causal connection
      - OR properties that could change without the entity ceasing to be
        that kind of thing

    essentialCount = count of differentia that are:
      - functional properties (what the thing DOES or IS FOR)
      - structural properties (composition, constitution)
      - causal-role properties (what brings it about, what it enables)
      - relational-in-reality properties (BFO relations: inheres_in,
        participates_in, located_in)

    IF accidentalCount > 0 AND essentialCount == 0:
      RETURN { category: "DefinedClass", confidence: 0.85 }

    IF accidentalCount > 0 AND essentialCount > 0:
      RETURN { category: "NaturalKind", confidence: 0.55 }
        // Mixed — lower confidence, likely routes to agent review

  TEST 3 — Default (no genus or no differentia character signal):
    RETURN { category: "NaturalKind", confidence: 0.40 }
      // Very low confidence — will escalate unless other stage scores are high
```

#### 4B.3 DefinedClass Routing Policy

When `category = "DefinedClass"`, the OPA immediately sets the routing decision to `agent-review` regardless of the aggregate PlacementConfidence computed in Stage 6. The ConversationPrompt issued for DefinedClass nominations must:

- Clearly state that the candidate is classified as a defined class, not a natural kind
- Explain the differentia that triggered the classification
- Present the option to: (a) confirm it as a DefinedClass and commit it with reduced ontological status, (b) redefine with essential differentia to qualify as a NaturalKind, or (c) reject the nomination

#### 4B.4 Job Title Classification

For Job Title specifically:

```
Genus: CCO:DesignativeInformationContentEntity
  → ∈ IAO/CCO InformationContentEntity hierarchy
  → TEST 1 applies → category: "NaturalKind", confidence: 0.85

Differentia analysis:
  "of a post within an organization" → relational-in-reality (existsWithin) → essential
  "associated with a job description" → functional relationship → essential
  "specifying tasks and responsibilities" → functional content → essential
  accidentalCount = 0, essentialCount = 3
  → TEST 1 result confirmed

RESULT: NaturalKind, confidence: 0.85. Auto-commit eligible.
```

#### 4B.5 Redefinition Re-entry Workflow *(new in v1.2)*

When a DefinedClass candidate is routed to agent review (§4B.3), the reviewing agent has the option to "redefine with essential differentia to qualify as a NaturalKind." This section specifies the re-entry contract for that workflow.

**Re-entry is a new nomination, not a pipeline resume.** The agent does not inject state into a running pipeline mid-stage. Instead, the agent submits a `fandaws-opa:RedefinitionRequest` — a specialized nomination that carries the original nomination's provenance plus the agent's revised definition.

```json
{
  "@type": "fandaws-opa:RedefinitionRequest",
  "fandaws-opa:nominationSource":  "agent-redefinition",
  "fandaws-opa:nominationBasis":   "redefinition",

  "fandaws-opa:originalNominationId": "fandaws-opa:nomination/TallRedheadedViolinist-20260314",
  "fandaws-opa:originalCategory":     "DefinedClass",

  "fandaws-opa:revisedDefinition": {
    "fandaws-opa:candidateLabel":   "StringInstrumentSpecialist",
    "fandaws-opa:genus":            "musician",
    "fandaws-opa:differentia":      ["who specializes in bowed string instruments"],
    "fandaws-opa:definitionText":   "A musician who specializes in the performance of bowed string instruments.",
    "fandaws-opa:redefinitionRationale": "Original candidate combined accidental properties (height, hair color) with functional role. Redefined to capture the essential functional specialization."
  },

  "fandaws-opa:requestedAt": "2026-03-14T12:00:00Z",
  "fandaws-opa:reviewingAgentId": "fandaws:agent/KnowledgeSteward-01"
}
```

**Pipeline re-entry point:** The OPA processes a RedefinitionRequest starting at **Stage 2** (Universal Induction), using the revised definition as input. Stage 1 (Semantic Existence Search) is re-executed first to check whether the revised label already exists — it is possible that the agent's redefinition produces a concept that already has a Universal in the graph.

**Re-entry algorithm:**

```
FUNCTION processRedefinition(redefinitionRequest, fandawsGraph):

  1. STAGE 1 — Semantic Existence Search using revisedDefinition.candidateLabel.
     IF found: emit mapping ConceptDesignation to existing Universal. EXIT.

  2. STAGE 2 — Universal Induction.
     Use revisedDefinition directly as InductionResult.
     Confidence = 0.90 (agent-reviewed definition is high-confidence).

  3. STAGES 3, 4, 4B, 5, 6 — proceed normally.
     Stage 4B will re-classify using the revised differentia.
     IF Stage 4B still returns DefinedClass:
       Route to agent review again with a note that redefinition
       did not resolve the classification.
       INCREMENT redefinitionAttemptCount on the ConversationPrompt.

  4. REASONING TRACE — must record:
     - fandaws-opa:redefinitionOf: originalNominationId
     - fandaws-opa:redefinitionAttempt: N (1-indexed)
     - fandaws-opa:revisedBy: reviewingAgentId
```

**Guardrail:** If `redefinitionAttemptCount >= 3`, the OPA stops issuing redefinition prompts and escalates to IEE with the full redefinition history. This prevents infinite review loops for concepts that resist classification as natural kinds.

---

### Stage 5 — BFO Subsumption Traversal

**Purpose:** Identify the most specific valid parent class in the BFO/CCO hierarchy. The parent must satisfy the subsumption test: every instance of the child necessarily is an instance of the parent.

*This stage is unchanged from v1.0 except that it now receives a `universalCategory` from Stage 4B. RoleUniversal candidates enter the Role branch of BFO; NaturalKind and ArtifactType enter their respective branches per the lookup table.*

**BFO Branch Lookup Table:**

| Genus Term Class | Entry BFO Branch | CCO Entry Point |
|---|---|---|
| `IAO:InformationContentEntity` or subtype | `BFO:GenericallyDependentContinuant` | `IAO:InformationContentEntity` → `CCO:DesignativeInformationContentEntity` |
| `BFO:Role` or `CCO:OrganizationalRole` | `BFO:SpecificallyDependentContinuant → BFO:RealizableEntity → BFO:Role` | `CCO:OrganizationalRole` |
| `BFO:Disposition` | `BFO:SpecificallyDependentContinuant → BFO:RealizableEntity` | `BFO:Disposition` |
| `BFO:Quality` | `BFO:SpecificallyDependentContinuant` | `BFO:Quality` |
| `BFO:Process` or CCO process | `BFO:Occurrent → BFO:Process` | Relevant CCO process class |
| `CCO:Organization` / `CCO:Agent` | `BFO:IndependentContinuant → BFO:MaterialEntity → CCO:Agent` | `CCO:Organization` |
| Unresolved | Full traversal from `BFO:Entity` — lower confidence | — |

**Role-vs-ICE Disambiguation Rule:**

```
SIGNAL 1 — Genus term:
  designation, label, title, name, code, identifier → VOTE ICE branch
  role, position, function, capacity, duty          → VOTE Role branch

SIGNAL 2 — Predication structure (TagTeam nominations):
  copula "is" + assertionObject following prepositional "of"
    → VOTE ICE branch (the concept IS the information, not the referent)

SIGNAL 3 — Token evidence (Type Agent nominations):
  NominalType + human-readable strings → VOTE ICE branch

RESOLVE:
  Majority vote wins. Tie → ICE branch (conservative: ICE less normatively
  committal than Role). Tie applies 0.15 confidence penalty.
```

**Traversal Algorithm:**

```
FUNCTION bfoSubsumptionTraversal(definitionResult, universalCategory, entryBranch):

  1. BEGIN at entryBranch from lookup table above.

  2. FOR EACH class C in CCO/IAO hierarchy under entryBranch,
     most-specific to least-specific (depth-first):

       STRUCTURAL SUBSUMPTION TEST:
         IF all definitionResult.differentia restrictions are consistent
            with C's definition AND no C.axiom contradicts the candidate:
           PASS

         IF any C.axiom (disjointness, property restriction) violated:
           FAIL — mark C invalid, move up

  3. RECORD most specific C that passes.
  4. CHECK for sibling competition; apply 0.10 penalty if ambiguous.

  5. RETURN TraversalResult {
       proposedParent, parentLabel, parentDepth,
       placementChain, siblingAmbiguity, confidence
     }
```

---

### Stage 6 — Confidence Aggregation and Output Routing

**Purpose:** Aggregate stage scores into PlacementConfidence and route to the appropriate output. Stage 4B's universalCategory overrides normal routing for DefinedClass candidates.

#### 6.1 PlacementConfidence Formula

```
PlacementConfidence =
  (w1 × Stage1.confidence)     // Existence search certainty
+ (w2 × Stage2.confidence)     // Universal induction
+ (w3 × Stage3.confidence)     // External vocabulary alignment
+ (w4 × Stage4.confidence)     // Definitional synthesis
+ (w4b × Stage4B.confidence)   // Universal classification
+ (w5 × Stage5.confidence)     // Subsumption traversal
− disambiguationPenalty         // 0.15 if Role-vs-ICE was tied
− siblingAmbiguityPenalty       // 0.10 if multiple valid parents at same depth
```

Default weights:

| Weight | Default | Rationale |
|---|---|---|
| w1 (existence) | 0.05 | Negative evidence |
| w2 (induction) | 0.20 | Core of reasoning |
| w3 (alignment) | 0.25 | External authority |
| w4 (synthesis) | 0.18 | Definitional coherence |
| w4b (classification) | 0.12 | Universal vs. defined class gate |
| w5 (traversal) | 0.20 | Correct BFO placement |

#### 6.2 Output Routing

```
IF Stage4B.category = "DefinedClass":
  FORCED → ConversationPrompt (agent review)
  PlacementConfidence is computed but does not govern routing for DefinedClass.

ELSE:
  IF PlacementConfidence >= 0.80:
    EMIT two-node GraphMutation (auto-commit)

  IF 0.60 <= PlacementConfidence < 0.80:
    EMIT ConversationPrompt (agent review — full placement recommendation)

  IF PlacementConfidence < 0.60:
    EMIT EscalationRequest to Causal OS Kernel / IEE
```

---

## 5. Normative Algorithms and Tables

### 5.1 Genus-to-BFO Mapping Table

*(Normative — unchanged from v1.0)*

| Genus Pattern | BFO Branch | CCO Entry Point |
|---|---|---|
| designation, label, title, name, appellation, identifier, code, descriptor | `BFO:GenericallyDependentContinuant` | `IAO:InformationContentEntity` → `CCO:DesignativeInformationContentEntity` |
| document, record, report, specification, plan | `BFO:GenericallyDependentContinuant` | `IAO:InformationContentEntity` → `CCO:DirectiveInformationContentEntity` |
| role, position, function, capacity, status | `BFO:SpecificallyDependentContinuant` | `BFO:RealizableEntity → BFO:Role → CCO:OrganizationalRole` |
| disposition, tendency, capability, power | `BFO:SpecificallyDependentContinuant` | `BFO:RealizableEntity → BFO:Disposition` |
| quality, property, attribute, characteristic | `BFO:SpecificallyDependentContinuant` | `BFO:Quality` |
| process, activity, action, event, procedure | `BFO:Occurrent` | `BFO:Process` → relevant CCO process class |
| person, individual, agent, actor | `BFO:IndependentContinuant` | `CCO:Person` |
| organization, institution, agency, body | `BFO:IndependentContinuant` | `CCO:Organization` |
| object, artifact, device, instrument | `BFO:IndependentContinuant` | `BFO:MaterialEntity → CCO:Artifact` |
| site, location, place, region | `BFO:IndependentContinuant` | `BFO:SpatialRegion` or `CCO:GeopoliticalOrganization` |

### 5.2 Relation Correction Table

*(Normative — unchanged from v1.0)*

| TagTeam Relation | Context | Corrected Relation | Rationale |
|---|---|---|---|
| `member_part_of` | ICE-type genus + object is the referent | `opa:designates` or `IAO:is_about` | ICEs are *about* their referents, not *part of* them |
| `member_part_of` | Role-type genus + bearer entity | `BFO:inheres_in` | Roles inhere in bearers, not mereological parts |
| `nmod` (bare) | Definitional predication | `opa:characterizes` (default) | Bare nominal modifiers in definitions express characterization |
| `conj` (confidence < 0.50) | Any structural assertion | Discard | Low-confidence conjunct attachments unreliable for ontological inference |

### 5.3 Universal Classification Rules *(new in v1.1)*

These rules define what counts as an essential versus accidental differentia for the purposes of Stage 4B classification. They are normative — implementations must apply them in the order listed.

**Essential property indicators (count toward essentialCount):**

- The differentia describes what the entity *does* or what it is *for* — a functional role or purpose
- The differentia describes how the entity is *composed* or *constituted*
- The differentia describes a causal relationship — what the entity produces, enables, or depends on
- The differentia uses a BFO relation: `inheres_in`, `participates_in`, `located_in`, `has_participant`, `realizes`
- The differentia describes membership in or participation with another genuine universal (not a defined class)

**Accidental property indicators (count toward accidentalCount):**

- The differentia restricts a value that the entity could lose while remaining the same *kind* of thing (color, size, geographic location, owner, age)
- The differentia is an arbitrary conjunction of properties from unrelated domains with no causal or functional connection between them
- The differentia describes a currently-observed statistical regularity rather than a necessary feature

**Boundary cases:**

- `hasNationality some French` — accidental (nationality can change)
- `hasFunction some Measuring` — essential (instruments are defined by function)
- `performsRole some Manager` — essential (role is constitutive in context)
- `hasColor some Red` — accidental
- `designates some OrganizationalPost` — essential (the designative relationship is constitutive of this ICE type)

**The DefinedClass trigger:** A candidate triggers DefinedClass routing when its differentia set consists *entirely* of accidental properties and the genus is not itself a functional or role type. Mixed cases (some accidental, some essential) receive lower confidence but do not trigger forced agent review.

### 5.4 The `fandaws-opa:designates` Relation *(new in v1.2)*

The `fandaws-opa:designates` relation is the key link between a `fandaws:ConceptDesignation` node and the `fandaws:Universal` node it refers to. This relation is formally declared as a specialization of `IAO:is_about`:

```
fandaws-opa:designates  rdf:type           owl:ObjectProperty .
fandaws-opa:designates  rdfs:subPropertyOf IAO:is_about .
fandaws-opa:designates  rdfs:domain        fandaws:ConceptDesignation .
fandaws-opa:designates  rdfs:range         fandaws:Universal .
```

**Why `IAO:is_about` is insufficient on its own:**

`IAO:is_about` is a general-purpose relation between any information content entity and any entity in the domain of discourse. A journal article is about a disease; a measurement datum is about a quality. The `designates` specialization carries three additional commitments that `is_about` alone does not enforce:

1. **Cardinality:** Every ConceptDesignation designates exactly one Universal. `IAO:is_about` permits many-to-many.
2. **Vocabulary-layer semantics:** The subject of `designates` is specifically a vocabulary-layer artifact (a ConceptDesignation), not an arbitrary ICE. The domain restriction to `fandaws:ConceptDesignation` is normative.
3. **Naming function:** `designates` asserts that the ConceptDesignation *names and refers to* the Universal — it doesn't merely describe, discuss, or analyze it. This is the distinction between a vocabulary entry (which designates a universal) and a research paper (which is about a universal).

Implementations that cannot register custom properties may use `IAO:is_about` as a fallback, but must enforce the domain, range, and cardinality constraints at the application layer.

> **Relation Correction Note:** The §5.2 relation correction table corrects TagTeam's `member_part_of` to `IAO:is_about` for ICE-type genus. The `designates` relation is the *further* specialization applied when the OPA creates a ConceptDesignation → Universal link. These are two distinct correction steps: first from `member_part_of` to `is_about` (parser correction), then from `is_about` to `designates` (OPA output-layer specialization).

---

## 6. Output Contract — Two-Layer Architecture *(revised in v1.1)*

Every OPA placement emits a GraphMutation containing **two nodes**: a `fandaws:Universal` and a `fandaws:ConceptDesignation`. These nodes are distinct entities serving distinct purposes. No single node carries both ontological assertions and computational metadata.

### 6.1 The Universal Node (Ontology Layer)

The Universal node represents the type as it exists in reality. It carries only:
- Its identity in the ontology (`rdfs:subClassOf`)
- Its definition
- Its placement chain
- External vocabulary alignments (which are ontological claims, not metadata)

It carries **no** confidence scores, reasoning traces, provenance timestamps, or nomination metadata. These belong to the representation of the universal, not to the universal itself.

```json
{
  "@id":   "fandaws:universal/JobTitle",
  "@type": ["fandaws:Universal", "owl:Class"],

  "rdfs:subClassOf":       "cco:DesignativeInformationContentEntity",
  "rdfs:label":            "JobTitle",
  "fandaws:definition":    "An information content entity that designates a post within an organization, associated with a job description specifying the tasks and responsibilities of that post.",

  "fandaws-opa:universalClassification": "NaturalKind",
  "fandaws-opa:placementChain": [
    "BFO:Entity",
    "BFO:Continuant",
    "BFO:GenericallyDependentContinuant",
    "IAO:InformationContentEntity",
    "CCO:DesignativeInformationContentEntity"
  ],

  "skos:exactMatch":  "cco:DesignativeInformationContentEntity",
  "skos:closeMatch":  "iao:InformationContentEntity"
}
```

### 6.2 The ConceptDesignation Node (Vocabulary Layer)

The ConceptDesignation node is an information artifact that *refers to* the Universal. It carries all computational metadata, provenance, confidence scores, and reasoning traces. It is itself an instance of `IAO:InformationContentEntity` — specifically, a designative ICE that is *about* the Universal it designates.

> **Relation declaration (v1.2):** The `fandaws-opa:designates` relation linking ConceptDesignation to Universal is formally declared as `rdfs:subPropertyOf IAO:is_about` with domain, range, and cardinality constraints. See §5.4 for the full formal declaration and rationale.

```json
{
  "@id":   "fandaws:designation/JobTitle-20260314",
  "@type": ["fandaws:ConceptDesignation", "IAO:InformationContentEntity"],

  "fandaws-opa:designates":        "fandaws:universal/JobTitle",
  "fandaws:canonicalLabel":        "JobTitle",
  "fandaws:displayLabel":          "Job Title",
  "fandaws:alternativeLabels":     ["Job Role", "Employment Title", "Position Title"],

  "shml:epistemicStatus":          "auto-promoted",
  "fandaws-opa:placementConfidence": 0.82,
  "fandaws-opa:nominationSource":  "tagteam",
  "fandaws-opa:normativeFlag":     false,
  "fandaws-opa:reasoningTrace":    "fandaws-opa:trace/JobTitle-20260314",

  "fandaws-opa:validatedBy": {
    "@type":                       "fandaws-opa:OPAProvenance",
    "fandaws-opa:agentId":         "fandaws-opa:OntologicalPlacementAgent",
    "fandaws-opa:policyId":        "fandaws-opa:policy/production-v1",
    "fandaws-opa:universalCategory": "NaturalKind",
    "fandaws-opa:stageScores": {
      "stage1_existence":     0.0,
      "stage2_induction":     0.75,
      "stage3_alignment":     0.90,
      "stage4_synthesis":     0.84,
      "stage4b_classification": 0.85,
      "stage5_traversal":     0.88
    },
    "fandaws-opa:emittedAt":       "2026-03-14T11:25:00Z"
  }
}
```

### 6.3 Complete GraphMutation

```json
{
  "@type": "fandaws:GraphMutation",
  "fandaws:additions": [
    {
      "@id":   "fandaws:universal/JobTitle",
      "@type": ["fandaws:Universal", "owl:Class"],
      "rdfs:subClassOf":    "cco:DesignativeInformationContentEntity",
      "rdfs:label":         "JobTitle",
      "fandaws:definition": "An information content entity that designates a post within an organization, associated with a job description specifying the tasks and responsibilities of that post.",
      "fandaws-opa:universalClassification": "NaturalKind",
      "fandaws-opa:placementChain": [
        "BFO:Entity", "BFO:Continuant",
        "BFO:GenericallyDependentContinuant",
        "IAO:InformationContentEntity",
        "CCO:DesignativeInformationContentEntity"
      ],
      "skos:exactMatch": "cco:DesignativeInformationContentEntity",
      "skos:closeMatch": "iao:InformationContentEntity"
    },
    {
      "@id":   "fandaws:designation/JobTitle-20260314",
      "@type": ["fandaws:ConceptDesignation", "IAO:InformationContentEntity"],
      "fandaws-opa:designates":          "fandaws:universal/JobTitle",
      "fandaws:canonicalLabel":          "JobTitle",
      "fandaws:displayLabel":            "Job Title",
      "shml:epistemicStatus":            "auto-promoted",
      "fandaws-opa:placementConfidence":  0.82,
      "fandaws-opa:nominationSource":    "tagteam",
      "fandaws-opa:normativeFlag":       false,
      "fandaws-opa:reasoningTrace":      "fandaws-opa:trace/JobTitle-20260314",
      "fandaws-opa:validatedBy": {
        "@type":                   "fandaws-opa:OPAProvenance",
        "fandaws-opa:agentId":     "fandaws-opa:OntologicalPlacementAgent",
        "fandaws-opa:policyId":    "fandaws-opa:policy/production-v1",
        "fandaws-opa:universalCategory": "NaturalKind",
        "fandaws-opa:stageScores": {
          "stage1_existence": 0.0, "stage2_induction": 0.75,
          "stage3_alignment": 0.90, "stage4_synthesis": 0.84,
          "stage4b_classification": 0.85, "stage5_traversal": 0.88
        },
        "fandaws-opa:emittedAt": "2026-03-14T11:25:00Z"
      }
    }
  ],

  "fandaws:reason": "OPA autonomous placement. Two-layer commit: Universal + ConceptDesignation. PlacementConfidence: 0.82. UniversalCategory: NaturalKind. Genus: CCO:DesignativeInformationContentEntity.",

  "fandaws:validatedBy": {
    "@type": "fandaws-opa:OPAProvenance",
    "fandaws-opa:agentId": "fandaws-opa:OntologicalPlacementAgent"
  }
}
```

### 6.4 Stage 1 Exit: Mapping an Existing Universal

When Stage 1 finds an existing Universal, the OPA does not create a new Universal. It creates only a new ConceptDesignation that designates the existing one. This allows the same underlying universal to have multiple designations from different source contexts — for example, `JobTitle` from the definitional parse and a second designation from the Type Agent's SGW convergence pointing to the same Universal IRI.

```json
{
  "@type": "fandaws:GraphMutation",
  "fandaws:additions": [
    {
      "@id":   "fandaws:designation/HRM-sgw-20260314",
      "@type": ["fandaws:ConceptDesignation", "IAO:InformationContentEntity"],
      "fandaws-opa:designates":   "fandaws:universal/JobTitle",
      "fandaws:displayLabel":     "HRM (mapped)",
      "fandaws-opa:mappingBasis": "token-overlap",
      "fandaws-opa:mappingScore": 0.78,
      "fandaws-opa:sourceKeys":   ["hr_database_v1:HRM", "finance_db_v2:employees_title"]
    }
  ],
  "fandaws:reason": "Stage 1 match. Existing Universal identified. New ConceptDesignation added."
}
```

### 6.5 FNSR CloudEvents Emission *(new in v1.2)*

The OPA emits CloudEvents at the Fandaws service boundary for every placement outcome. These events are the mechanism by which external FNSR services (BAM, IS, IEE, Causal OS Kernel) observe OPA activity without coupling to Fandaws internals. This aligns with the TagTeam-Fandaws Integration Guidance ACTION 2 (CloudEvents `fnsr.*` envelope).

**Event types:**

| Event Type | Emitted When | Key Payload Fields |
|---|---|---|
| `fnsr.concept.placed` | GraphMutation auto-committed (PlacementConfidence ≥ 0.80, category ≠ DefinedClass) | `universalIRI`, `designationIRI`, `universalCategory`, `placementConfidence`, `nominationSource`, `normativeFlag` |
| `fnsr.concept.review-requested` | ConversationPrompt issued (agent review — confidence 0.60–0.80, or DefinedClass forced review) | `designationIRI`, `universalCategory`, `placementConfidence`, `reviewReason` (`"low-confidence"` or `"defined-class"`), `redefinitionAttempt` (if applicable) |
| `fnsr.concept.escalated` | EscalationRequest issued (PlacementConfidence < 0.60) | `nominationId`, `placementConfidence`, `escalationTarget`, `nominationSource` |

**CloudEvent envelope:**

```json
{
  "specversion": "1.0",
  "type": "fnsr.concept.placed",
  "source": "fandaws/opa",
  "id": "opa-evt-20260314T112500Z-a3f91bc2",
  "time": "2026-03-14T11:25:00Z",
  "datacontenttype": "application/json",
  "fnsr.taintLevel": "L3",
  "data": {
    "universalIRI":       "fandaws:universal/JobTitle",
    "designationIRI":     "fandaws:designation/JobTitle-20260314",
    "universalCategory":  "NaturalKind",
    "placementConfidence": 0.82,
    "nominationSource":   "tagteam",
    "normativeFlag":      false,
    "stage3Degraded":     false
  }
}
```

> **Taint level:** All OPA CloudEvents carry `fnsr.taintLevel: "L3"` (inferred). A placement is promotable to L2 when the reviewing agent confirms it, and to L1 on human attestation. The taint level applies to the *event's claims*, not to the Universal itself (which has no taint — it is an ontological entity, not an information artifact). The ConceptDesignation carries taint metadata as part of its provenance.

**Emission points:** CloudEvents are emitted *after* the GraphMutation or ConversationPrompt has been successfully delivered to the OrchestrationAdapter. If the mutation fails, no event is emitted. This ensures that external subscribers never receive events for placements that did not actually occur.

> **Capability dependency:** Emission requires OPA-CAP-011 (CloudEvents publisher endpoint). Without it, OPA operates normally but external FNSR services have no visibility into placement activity. See §9.

---

## 7. OPA Reasoning Trace *(updated in v1.1)*

The reasoning trace is stored as a separate node in the Fandaws graph. It is referenced by the ConceptDesignation, never by the Universal. Traces are immutable.

```json
{
  "@id": "fandaws-opa:trace/JobTitle-20260314",
  "@type": "fandaws-opa:ReasoningTrace",

  "fandaws-opa:forDesignation":    "fandaws:designation/JobTitle-20260314",
  "fandaws-opa:forUniversal":      "fandaws:universal/JobTitle",
  "fandaws-opa:nominatedLabel":    "Job Title",
  "fandaws-opa:resolvedLabel":     "JobTitle",
  "fandaws-opa:placedUnder":       "cco:DesignativeInformationContentEntity",

  "fandaws-opa:stage1": {
    "result": "no-match", "confidence": 0.0
  },
  "fandaws-opa:stage2": {
    "result": "GEN-confirmed", "genus": "designation",
    "differentia": ["of a post", "within an organization", "associated with job description"],
    "confidence": 0.75
  },
  "fandaws-opa:stage3": {
    "result": "close-match", "alignedVocabulary": "CCO",
    "alignedClass": "cco:DesignativeInformationContentEntity",
    "confidence": 0.90
  },
  "fandaws-opa:stage4": {
    "result": "synthesized", "genusIRI": "cco:DesignativeInformationContentEntity",
    "relationsApplied": ["member_part_of → is_about (§5.2)"],
    "confidence": 0.84
  },
  "fandaws-opa:stage4b": {
    "result": "NaturalKind",
    "test1_triggered": true,
    "genusInICEHierarchy": true,
    "accidentalCount": 0,
    "essentialCount": 3,
    "confidence": 0.85
  },
  "fandaws-opa:stage5": {
    "result": "placed", "proposedParent": "cco:DesignativeInformationContentEntity",
    "siblingAmbiguity": false, "confidence": 0.88
  },
  "fandaws-opa:stage6": {
    "placementConfidence": 0.82, "penalties": [],
    "universalCategory": "NaturalKind",
    "routing": "auto-commit"
  }
}
```

---

## 8. OPA Policy

```json
{
  "@type":  "fandaws-opa:OPAPolicy",
  "@id":    "fandaws-opa:policy/production-v1",

  "fandaws-opa:weights": {
    "w1_existence":        0.05,
    "w2_induction":        0.20,
    "w3_alignment":        0.25,
    "w4_synthesis":        0.18,
    "w4b_classification":  0.12,
    "w5_traversal":        0.20
  },

  "fandaws-opa:thresholds": {
    "autoCommit":    0.80,
    "agentReview":   0.60
  },

  "fandaws-opa:exactLabelMatchThreshold":    0.95,
  "fandaws-opa:tokenOverlapMatchThreshold":  0.70,
  "fandaws-opa:externalAlignmentThreshold":  0.65,
  "fandaws-opa:defaultIceOverRoleTieBreak":  true,
  "fandaws-opa:definedClassForcedReview":    true,

  "fandaws-opa:normativeFlagDomains": [
    "obligation", "right", "duty", "agency", "consent",
    "liability", "harm", "benefit", "identity"
  ],

  "fandaws-opa:escalationTarget": "fandaws:service/CausalOSKernel"
}
```

---

## 9. Required Capabilities — Fandaws and FNSR

| Cap ID | Capability | Stage Required | Degradation Without It |
|---|---|---|---|
| OPA-CAP-001 | Vocabulary query API over IVNE-loaded ontologies for label and semantic proximity search | Stage 3 | Stage 3 returns `{ found: false, confidence: 0.0, degraded: true }` (§Stage 3 degradation path). Placements produced without external authority citations. Most placements route to agent review due to reduced PlacementConfidence. |
| OPA-CAP-002 | Optional DL reasoner (HermiT/Pellet) for full OWL satisfiability checking | Stage 5 | Structural graph checks only. Cross-branch contradictions undetectable. |
| OPA-CAP-003 | `fandaws:Universal` node type added to Fandaws schema with `rdfs:subClassOf`, `fandaws:definition`, `fandaws-opa:universalClassification`, `fandaws-opa:placementChain` | Output §6 | Without this, the Universal cannot be committed as a distinct ontology-layer node. Two-layer architecture collapses back to single-node, reintroducing punning. |
| OPA-CAP-004 | `fandaws:ConceptDesignation` node type added to Fandaws schema with `fandaws-opa:designates` relation, `fandaws:canonicalLabel`, `fandaws:displayLabel`, and metadata fields | Output §6 | Without this, the vocabulary layer cannot exist separately from the ontology layer. |
| OPA-CAP-005 | `fandaws-opa:ReasoningTrace` namespace and schema registered in Fandaws namespace registry | Audit trail §7 | System functions but violates namespace governance. |
| OPA-CAP-006 | IEE notification interface for normatively significant concepts | Stage 6 routing | RoleUniversal concepts committed without IEE awareness. |
| OPA-CAP-007 | `shml:epistemicStatus` value `"auto-promoted"` on the Fandaws SHML vocabulary | Output §6 | Shared with FTA-CAP-001. Auto-promoted concepts use `"imported"` status by default. |
| OPA-CAP-008 | `fandaws-opa:universalClassification` controlled vocabulary (`NaturalKind`, `RoleUniversal`, `ArtifactType`, `DefinedClass`) registered in Fandaws namespace | Stage 4B and Universal node | Without this, the universalClassification field uses unregistered values. System functions but downstream consumers cannot reliably interpret the classification. |
| OPA-CAP-009 | Fandaws query API to retrieve the ConceptDesignation(s) for a given Universal IRI | Post-placement navigation | Without this, consumers who hold a Universal IRI cannot discover its designations (labels, provenance, confidence) without a full graph scan. The inverse navigation — from Universal to Designation — must be supported by an index or query endpoint. |
| OPA-CAP-010 | GraphMutation schema extended to support multi-addition arrays containing both Universal and ConceptDesignation nodes in a single atomic transaction | Output §6 | Without atomic two-node commit, a race condition exists between Universal creation and ConceptDesignation creation. If the first succeeds and the second fails, the Universal is committed with no designation — an orphaned ontology-layer node with no vocabulary-layer referent. Layer 2 defense-in-depth for KL-003. |
| OPA-CAP-011 | CloudEvents publisher endpoint for `fnsr.concept.*` events at the Fandaws service boundary | §6.5 | Without this, external FNSR services (BAM, IS, IEE, Causal OS Kernel) have no visibility into OPA placement activity. Cross-boundary consumers must poll or depend on Fandaws internals. |

---

## 10. Required Enhancements — TagTeam

| Gap ID | Enhancement | Stage Affected | Impact Without It |
|---|---|---|---|
| TT-GAP-001 | `tagteam:isDefinitional` boolean flag on InformationBearingEntity nodes | Stage 2, Stage 4 | OPA cannot distinguish a definition from a usage sentence. |
| TT-GAP-002 | Relation correction for `of` in definitional predication contexts — `member_part_of` → `is_about` for ICE-type genus | Stage 4 relation correction | OPA must apply §5.2 correction table as a mitigation. |
| TT-GAP-003 | `tagteam:nominationBasis` value `"definition_predication"` for GEN universals detected via definitional copular sentence | Stage 2 confidence | All definitional detections receive same confidence as weaker genericity signals. |
| TT-GAP-004 | `tagteam:sourceDomain` field on InformationBearingEntity (controlled vocabulary: `hr`, `finance`, `clinical`, `legal`, `operations`, `general`) | Stage 5 BFO branch selection | OPA traverses more branches before finding entry point. |
| TT-GAP-005 | Pronoun coreference resolution for definitional sentences | Stage 4 differentia synthesis | Incomplete differentia chain for pronoun-using definitions. ~0.10 confidence reduction per unresolved pronoun. |
| TT-GAP-006 | `tagteam:universalClassificationHint` optional field on Tier 2 entity nodes with GEN/UNIV genericityCategory. Values: `natural-kind`, `role`, `artifact-type`, `possible-defined-class`. TagTeam can provide a preliminary signal — e.g., if the copular predicate in a definitional sentence contains words like "intersection", "combination", "anyone who", or arbitrary property lists — to pre-populate the Stage 4B classification and reduce OPA computation. | Stage 4B Universal Classification Gate | Without this, Stage 4B operates entirely from genus and differentia analysis. This is sufficient but a TagTeam hint would improve confidence on borderline cases and reduce the incidence of mixed-signal uncertain classifications. |

---

## 11. Conformance Checklist

### 11.1 Pipeline

- Implements all seven stages in order (Stages 1, 2, 3, 4, 4B, 5, 6). Stage 4B must not be skipped.
- Stage 1 exact label match at confidence ≥ 0.95 exits the pipeline and emits a mapping-only mutation (new ConceptDesignation designating the existing Universal).
- Stage 2 applies the correct induction path (2A for TagTeam, 2B for Type Agent).
- Stage 4 applies the relation correction table (§5.2) before constructing OWL restrictions.
- Stage 4B applies all three tests in order and records `accidentalCount`, `essentialCount`, `category`, and `confidence`.
- Stage 4B result of `DefinedClass` forces routing to agent-review regardless of Stage 6 PlacementConfidence.
- Stage 5 uses the BFO branch lookup table (§5.1) as the entry point and applies the Role-vs-ICE disambiguation rule.
- Stage 6 aggregates confidence using the seven-weight formula with the OPAPolicy weights.
- *(v1.2)* Stage 3 returns `{ found: false, confidence: 0.0, degraded: true }` when no vocabularies are loaded, and the pipeline proceeds to Stage 4.
- *(v1.2)* RedefinitionRequests re-enter the pipeline at Stage 1 (existence check) then Stage 2 (induction from revised definition). Stage 4B re-classifies using revised differentia.
- *(v1.2)* Redefinition attempts are capped at 3 before IEE escalation.

### 11.2 Output

- Every GraphMutation that creates a new concept emits **two** nodes atomically: one `fandaws:Universal` and one `fandaws:ConceptDesignation`.
- The Universal node carries: `rdfs:subClassOf`, `rdfs:label`, `fandaws:definition`, `fandaws-opa:universalClassification`, `fandaws-opa:placementChain`, and any `skos:exactMatch`/`skos:closeMatch` alignments.
- The Universal node carries **no** confidence scores, reasoning traces, provenance timestamps, or nomination metadata.
- The ConceptDesignation node carries: `fandaws-opa:designates` (pointing to the Universal), `fandaws:canonicalLabel`, `fandaws:displayLabel`, `shml:epistemicStatus`, `fandaws-opa:placementConfidence`, `fandaws-opa:reasoningTrace`, `fandaws-opa:validatedBy`, and `fandaws-opa:normativeFlag`.
- Stage 1 exit mutations emit only a ConceptDesignation — no new Universal.
- `fandaws-opa:normativeFlag: true` is set on any ConceptDesignation whose `canonicalLabel` or `displayLabel` matches an OPAPolicy `normativeFlagDomain` term.
- *(v1.2)* `fandaws-opa:designates` is declared as `rdfs:subPropertyOf IAO:is_about` with domain `fandaws:ConceptDesignation` and range `fandaws:Universal`.
- *(v1.2)* Every placement outcome (auto-commit, agent review, escalation) emits a corresponding `fnsr.concept.*` CloudEvent at the Fandaws service boundary (§6.5).
- *(v1.2)* CloudEvents carry `fnsr.taintLevel: "L3"` and are emitted only after successful delivery of the GraphMutation or ConversationPrompt.

### 11.3 Reasoning Trace

- A ReasoningTrace is stored for every placement regardless of routing.
- The trace includes Stage 4B results: `category`, `accidentalCount`, `essentialCount`, all applied test results.
- The trace's `fandaws-opa:forDesignation` points to the ConceptDesignation, not the Universal.
- Traces are immutable. Re-evaluation produces a new trace with a new IRI.
- *(v1.2)* Traces for degraded Stage 3 record `degraded: true` and `reason: "no-vocabularies-loaded"`.
- *(v1.2)* Traces for redefinition re-entry record `redefinitionOf`, `redefinitionAttempt`, and `revisedBy`.

### 11.4 TagTeam Integration

- OPA subscribes to TagTeam output graphs via the OrchestrationAdapter.
- Any TagTeam graph with a node carrying `tagteam:requiresOntologyResolution: true` triggers Stage 1.
- On successful placement, the OPA updates the TagTeam node's `tagteam:classNominationStatus` to `"resolved"` and adds `tagteam:resolvedUniversalIRI` (pointing to the Universal) and `tagteam:resolvedDesignationIRI` (pointing to the ConceptDesignation).
- On DefinedClass routing, the OPA sets `tagteam:classNominationStatus` to `"pending-review"`.
- On escalation, the OPA sets `tagteam:classNominationStatus` to `"escalated"`.

---

## 12. Known Limitations

### KL-001: Statistical Nominations Without Definitional Text Produce Lower Confidence

Type Agent nominations without an associated TagTeam definitional parse rely on token evidence alone for Stage 2 and Stage 4. This systematically produces lower confidence scores, increasing agent-review routing.

**Mitigation:** The OPA should query the IVNE vocabulary index or an external dictionary for a definition of the nominated label before proceeding with token-only induction. This partially converts a statistical nomination to a definitional one.

**Resolution Path:** OPA-CAP-001 (vocabulary query API) partially addresses this. A future enhancement closes the loop fully: Type Agent detects → OPA retrieves definition → OPA requests TagTeam parse → OPA runs full pipeline. No human required at any step.

### KL-002: The OPA Cannot Detect Cross-Branch Ambiguity Without a Full DL Reasoner

The structural subsumption test cannot detect cases where a definition is simultaneously consistent with two disjoint BFO branches. This would require full DL satisfiability checking.

**Mitigation:** The Role-vs-ICE disambiguation rule (§5.2) handles the most common ambiguity in organizational domains. Sibling ambiguity penalty reduces confidence and increases agent-review routing for ambiguous cases.

**Resolution Path:** OPA-CAP-002 (DL reasoner) resolves fully.

### KL-003: Concurrent Nominations May Race at Stage 1 *(rewritten in v1.2)*

Two concurrent nominations for concepts that should map to the same Universal may each pass Stage 1 independently, producing duplicate Universal nodes that Termidium must reconcile post-commit.

**Root cause:** Stage 1's Semantic Existence Search reads the graph snapshot at query time. If two nominations for "JobTitle" arrive simultaneously, both see "no existing Universal" and both proceed to create one.

**Two-layer mitigation (explicit dependency chain):**

| Layer | Mechanism | What It Prevents | Prerequisite |
|---|---|---|---|
| **Layer 1 (primary):** Serialized nomination queue | All NominationRequests are enqueued and processed sequentially. Stage 1 of nomination N+1 does not begin until the GraphMutation (or ConversationPrompt) of nomination N has been committed to the graph. | Duplicate creation during normal operation. Two nominations for the same concept will be serialized — the second one's Stage 1 search will find the Universal created by the first. | None — implementable today as an in-memory queue within the OPA. |
| **Layer 2 (defense-in-depth):** OPA-CAP-010 atomic two-node commit | The GraphMutation containing both Universal and ConceptDesignation is committed atomically. | Orphaned nodes on crash. If the OPA crashes between committing the Universal and committing the ConceptDesignation, the partial commit is rolled back. Without atomicity, the serialized queue alone leaves a crash-recovery gap: nomination N's Universal is committed, the OPA crashes before the ConceptDesignation is written, and nomination N+1 finds an orphaned Universal with no designation. | Fandaws Knowledge Engine must support multi-node atomic transactions (OPA-CAP-010). |

**Dependency:** Layer 1 (serialized queue) is sufficient for correctness during normal operation and does **not** require OPA-CAP-010. Layer 2 (atomic commit) is defense-in-depth for crash recovery and is independently valuable. Neither layer requires the other, but both together eliminate the race window entirely — including under crash conditions.

**Residual risk without Layer 2:** If the OPA crashes between Universal commit and ConceptDesignation commit, the graph contains an orphaned Universal. Termidium's deduplication index will detect this on the next nomination for the same concept (Stage 1 will find the orphaned Universal), but the orphaned Universal will lack a ConceptDesignation until manually reconciled or until a second nomination triggers Stage 1 mapping.

**Implementation status:** Layer 1 targeted for v1.2. Layer 2 depends on OPA-CAP-010 (Fandaws schema change).

### KL-004: DefinedClass Route Requires Human or Agent Judgment That OPA Cannot Supply

The DefinedClass ConversationPrompt asks a reviewing agent to determine whether the candidate should be: (a) committed as a DefinedClass with reduced ontological status, (b) redefined with essential differentia to qualify as a NaturalKind, or (c) rejected. The OPA cannot determine which of these outcomes is correct — that requires understanding whether the concept has genuine utility in the knowledge graph independent of whether it is ontologically a natural kind.

**Mitigation:** The ConversationPrompt carries the full Stage 4B analysis, including the accidental differentia that triggered the classification, so the reviewing agent has all evidence needed to make an informed decision.

**Resolution Path:** The IEE's twelve-worldview deliberation framework may be capable of providing a reasoned recommendation on DefinedClass cases where the decision has normative implications. This integration is deferred pending IEE specification maturity.

### KL-005: CloudEvents Emission Requires Cross-Component Coordination *(new in v1.2)*

The `fnsr.concept.*` CloudEvents (§6.5) are emitted at the Fandaws service boundary, not directly by the OPA. The OPA produces GraphMutations and ConversationPrompts; the Fandaws OrchestrationAdapter (or a boundary-layer event publisher) is responsible for translating these into CloudEvents.

This means the OPA specification defines the *content* of the events but cannot guarantee their emission — that depends on the Fandaws boundary layer implementing OPA-CAP-011. If the boundary layer does not emit events, or emits them with incorrect payload structure, external FNSR subscribers will have stale or missing data.

**Mitigation:** The OPA attaches a `fandaws-opa:eventHint` field to every GraphMutation and ConversationPrompt, specifying the intended CloudEvent type and payload. The boundary layer can use this hint to construct the event without needing to understand OPA internals.

**Resolution Path:** OPA-CAP-011 implementation. The Fandaws v3.4 OrchestrationAdapter specification should include a CloudEvents emission contract that consumes `eventHint` fields from all Fandaws-internal components (OPA, Type Agent).
