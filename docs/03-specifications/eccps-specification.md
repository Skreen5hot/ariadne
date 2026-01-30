
# Functional Requirements Document (FRD) v3.1

**System Name:** Epistemically Constrained Claim Processing System (ECCPS)  
**Status:** Implementation-Ready Specification  
**Focus:** Realist Ontology (BFO), Epistemic Friction, and Failure-as-Signal

---

## 1. Purpose & Core Philosophy

The ECCPS is a **semantic gatekeeper**. It processes natural language to determine if a claim possesses the ontological density and epistemic clarity required for machine-interpretable structure.

### 1.1 Definition: Ontological Density

**Ontological Density**: A claim possesses ontological density when all its elements (agents, actions, patients, temporal context, spatial context) can be mapped to upper ontology top-level categories (BFO/CCO or equivalent) without requiring ungrounded abstractions, undefined terms, or irreducible vagueness.

A claim with high ontological density:
- Refers to identifiable entities with clear existence conditions
- Describes processes with temporal boundaries
- Specifies relations between definite relata
- Provides sufficient context for verification or falsification

A claim lacking ontological density:
- Uses abstract nouns without grounding ("Democracy demands...")
- Employs vague quantifiers without specification ("Many people believe...")
- Makes rhetorical gestures without clear referents ("Justice requires...")

### 1.2 Core Operating Principle

The system operates on the principle of **Maximum Traceability**: every structured output must be decomposable back to its original linguistic artifact, with every transformation logged as a discrete epistemic choice.

### 1.3 Intended Use Context

ECCPS is designed for **high-stakes epistemic contexts** where vagueness creates systemic risk:
- Policy documentation and governance decisions
- Ethical deliberation requiring multi-perspectival evaluation
- Research claims requiring reproducible grounding
- Legal and regulatory reasoning
- Systems interfacing with ARCHON (governance) or IEE (ethics)

**ECCPS is not intended for**:
- Casual conversation
- Creative writing
- Exploratory brainstorming
- Contexts where ambiguity is productive

### 1.4 Scope and Limitations

**ECCPS is not**:
- A general-purpose NLP system
- A complete solution out-of-the-box
- Achievable in 6 months
- Usable without user training

**ECCPS is**:
- A specialized semantic gatekeeper
- A research prototype requiring iteration
- A multi-year development effort
- A system requiring sophisticated users

**Success criteria**:
- Phase 1: Prove core concept with 100-claim corpus
- Phase 2: Demonstrate utility in real governance context
- Phase 3: Achieve adoption by 3-5 institutional users

**If this project succeeds**, it will:
- Make epistemic standards in governance explicit
- Reduce vague claims in policy documents
- Provide infrastructure for IEE/ARCHON integration

**If this project fails**, it will likely be because:
- Users reject the epistemic friction
- Technical challenges (metaphor detection, etc.) prove intractable
- Resource requirements (test corpus, expert annotators) too high

---

## 2. Design Principles

### 2.1 Failure is a Success State

Identifying a claim as "un-groundable" is a **high-value output**. Most NLP systems smooth over ambiguity for the sake of fluency. ECCPS makes ambiguity visible and returns structured failure reports that specify exactly what is missing.

### 2.2 Explicit Traceability

No transformation (e.g., resolving a pronoun, inferring an implicit agent, normalizing a temporal reference) shall occur without a preserved link to the source text. Every intermediate representation maintains character-offset pointers to the root artifact.

### 2.3 Ontological Realism (Methodological Commitment)

**The system adopts ontological realism as a methodological framework**, following Smith et al.'s argument that ontological realism improves consistency in formal knowledge representation (Arp, Smith, & Spear, 2015).

ECCPS privileges:
- **BFO/CCO realist ontology** as the default framework
- **Material entities** as primary existents
- **Processes** as temporal occurrents with beginnings and ends
- **Spatiotemporal grounding** as necessary for verification

**This is a substantive commitment**, not a neutral technical choice. Alternative metaphysical frameworks (Buddhist non-self, idealist systems, process metaphysics where relations are primary) may require alternative ontological modules (see NFR-3).

**This commitment is compatible with**:
- Scientific realism (empirical investigation of material reality)
- Common sense ontology (everyday object reasoning)
- Multiple religious and secular philosophical traditions that accept mind-independent reality
- **Integral Ethics framework** (reality-alignment as terminal value; Realism worldview as one of twelve archetypal perspectives)

The BFO/CCO framework provides systematic formal structure for the **Realism** worldview within Integral Ethics—the orientation toward "objective truth, correspondence to reality, natural law" (Steiner, 1914/2008). Other worldviews (Idealism, Phenomenalism, Spiritualism, etc.) may ground claims differently, which ECCPS accommodates through its Structured Ambiguity track (FR-3.4).

### 2.4 Epistemic Friction

The system is intentionally "difficult" to satisfy. It resists smoothing over ambiguity for the sake of fluency. This friction is **pedagogical**—users learn what epistemic standards are required for rigorous reasoning.

This aligns with Integral Ethics' commitment to **Truth/Reality-Alignment** as a terminal value: "Conformity of belief/action to reality; intellectual honesty" is necessary foundation for practical reasoning.

### 2.5 Statistical Determinism

**Ideal**: Identical inputs + identical configuration = bit-identical outputs.

**Reality**: When utilizing LLM components or floating-point computation, perfect determinism is unachievable.

**Commitment**: The system achieves **statistical determinism**—99%+ output consistency over repeated runs with identical configurations, with all variation logged and auditable.

This is honest about implementation constraints while maintaining reproducibility as a core value.

### 2.6 User Experience Strategy: Managing Epistemic Friction

ECCPS is designed for **high epistemic friction**. This creates tension:
- Users want their claims processed
- ECCPS frequently rejects them

**This tension is intentional but must be managed.**

#### Three Usage Modes

**1. STRICT MODE (High Friction)**
- Target users: Policy drafters, governance documents, legal filings
- Behavior: Reject all ambiguous claims immediately with detailed errors
- Value proposition: "Catch problems before they cause governance failures"
- Training required: Yes, significant
- Adoption barrier: High

**2. GUIDED MODE (Moderate Friction)**
- Target users: Researchers, analysts, technical writers
- Behavior: Accept claims with warnings, prompt for clarification
- Value proposition: "Improve claim quality through interactive refinement"
- Training required: Moderate, system teaches through use
- Adoption barrier: Medium

**3. AUDIT MODE (Low Friction, Batch Analysis)**
- Target users: Document reviewers, fact-checkers, researchers
- Behavior: Process entire documents, flag issues, don't block
- Value proposition: "Identify weak claims in existing text"
- Training required: Minimal
- Adoption barrier: Low

#### Adoption Pathway

**Phase 1**: Launch with AUDIT MODE only
- Users submit documents for analysis
- Receive comprehensive reports
- Learn system standards
- Build internal corpus of "good" vs "flagged" claims

**Phase 2**: Add GUIDED MODE
- Users ready to refine claims interactively
- System has learned from Phase 1 feedback
- Refinement suggestions are calibrated to user domain

**Phase 3**: Enable STRICT MODE
- For high-stakes contexts only
- Users are trained
- System is proven
- Governance applications (ARCHON) go live

#### Success Metrics

**Phase 1** (Audit Mode):
- Can we process 10,000 claims/day?
- Do users understand failure reports?
- Are error distributions sensible?

**Phase 2** (Guided Mode):
- Do users successfully refine claims?
- Does refinement rate improve over time (learning)?
- Are suggestions helpful? (user surveys)

**Phase 3** (Strict Mode):
- What % of governance claims pass on first submission?
- Do rejection rates decrease over time (user learning)?
- Are false rejections rare? (<5% challenge rate)

**Critical success factor**: ECCPS must teach users, not just reject them.

---

## 3. High-Level Functional Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Raw Text Artifact                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Module 1: Language Artifact Intake (LAI)                       │
│  • Assign Unique Artifact ID (UAID)                             │
│  • Preserve raw source as Root Node                             │
│  • Segment into Candidate Claim Units (CCUs)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Module 2: Claim Extraction & Traceability (CET)                │
│  • Extract structured elements with character offsets            │
│  • Identify epistemic modalities                                │
│  • Tag rhetorical devices                                       │
│  • Pattern: Agent-Action-Patient / Alternative patterns         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Module 3: Ontological Grounding (OGM)                          │
│  • Map elements to BFO/CCO categories                           │
│  • Detect category errors                                       │
│  • Handle Structured Ambiguity                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Module 4: Constraint & Sufficiency Validation (CSV)            │
│  • Apply sufficiency gates                                      │
│  • Validate causal claims                                       │
│  • Check temporal/spatial/quantifier specifications             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Module 5: Normative Annotation (NAM)                           │
│  • Isolate evaluative terms                                     │
│  • Create value overlays                                        │
│  • Support multiple conflicting frameworks                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
         ┌──────────────────┐  ┌──────────────────┐
         │ Validated Claim  │  │ Structured       │
         │ Graph (JSON-LD)  │  │ Failure Report   │
         └──────────────────┘  └──────────────────┘
                             │
                             ▼
                   ┌──────────────────┐
                   │ Conflict         │
                   │ Resolution       │
                   │ (Module 6)       │
                   └──────────────────┘
```

---

## 4. Functional Requirements

### 4.0 Requirement Classification

All functional requirements are classified by implementation maturity:

**TIER 1 (CORE)**: Achievable with current technology, must be implemented
- Text intake and segmentation
- Basic triple extraction (Agent-Action-Patient)
- BFO category mapping for concrete nouns
- Simple validation checks (missing elements, undefined terms)
- Error reporting with codes
- Character-offset traceability

**TIER 2 (EXTENDED)**: Requires advanced NLP but feasible with current state-of-the-art models
- Multi-pattern extraction (Attributive, Existential, Relational)
- Epistemic modality detection
- Structured ambiguity handling
- Conflict detection
- Guided refinement suggestions

**TIER 3 (RESEARCH)**: Requires capabilities beyond current state-of-the-art
- Reliable metaphor/irony detection (FR-2.4)
- Automated normative annotation across multiple frameworks (Module 5)
- Fully automated "gap analysis" with specific suggestions (FR-8.1)
- Real-time generation of "possible groundings" for ambiguous terms (FR-3.4)

**Implementation Strategy**:
- Phase 1 (Months 1-6): Implement all TIER 1 requirements
- Phase 2 (Months 7-12): Implement TIER 2 where feasible, with fallbacks
- Phase 3 (Months 13+): Research prototypes for TIER 3, with human-in-loop

**TIER 3 features may require**:
- Human expert curation
- Extensive knowledge bases
- Integration with external systems (IEE for normative annotation)
- Hybrid human-AI workflows

---

### 4.1 Module 1: Language Artifact Intake (LAI)

**FR-1.1** (TIER 1): The system SHALL ingest text artifacts and assign a **Unique Artifact ID (UAID)**.

**FR-1.2** (TIER 1): The system SHALL preserve the raw source as a "Root Node" for all downstream provenance, including:
- Original encoding (UTF-8)
- Timestamp of intake
- Source metadata (document title, author, URL if applicable)

**FR-1.3** (TIER 1): The system SHALL segment text into **Candidate Claim Units (CCUs)** without stripping context.

**FR-1.3.1 Segmentation Rules**:
- **Default**: CCUs are sentence-level units determined by standard sentence boundary detection
- **Complex sentences**: May be decomposed into multiple CCUs when they contain:
  - Multiple independent clauses with distinct truth conditions
  - Causal chains ("Because A, therefore B" → two CCUs in relation)
  - Conditional structures ("If A, then B" → two CCUs plus conditional relation)
- **Context preservation**: Each CCU retains:
  - Character offsets in source document
  - Paragraph/section context
  - Preceding and following sentences (windowed context)

**FR-1.4** (TIER 2): The system SHALL support **progressive disclosure modes**:
- **Strict Mode**: Maximum epistemic friction, rejects ambiguous claims immediately
- **Guided Mode**: Accepts claims with ambiguity flags, provides suggestions for refinement
- **Audit Mode**: Processes entire documents, generates aggregate reports

---

### 4.2 Module 2: Claim Extraction & Traceability (CET)

**FR-2.1** (TIER 1 for AAP, TIER 2 for alternatives): The system SHALL extract structured elements from CCUs using **multiple extraction patterns**:

**Primary Pattern: Agent-Action-Patient (AAP)** [TIER 1]
- Agent: Entity performing or undergoing change
- Action: Process or relation
- Patient: Entity affected by action

**Alternative Pattern: Attributive (ATT)** [TIER 2]
- Subject: Entity bearing a quality
- Copula: "is," "has," "possesses"
- Attribute: Quality or property

**Alternative Pattern: Existential (EXT)** [TIER 2]
- Quantifier: "There is/exists/are"
- Entity: What exists
- Context: Temporal/spatial specification

**Alternative Pattern: Relational (REL)** [TIER 2]
- Entity₁: First relatum
- Relation: Symmetric/asymmetric relation
- Entity₂: Second relatum

**FR-2.2 Traceability Requirement** (TIER 1): Every extracted element MUST retain:
- Character-offset pointer to source artifact
- Token span (start, end)
- Confidence score (if extraction used probabilistic methods)

**FR-2.3** (TIER 2): The system SHALL identify and flag **Epistemic Modalities**:
- **Certainty markers**: "definitely," "certainly," "necessarily"
- **Possibility markers**: "possibly," "maybe," "could be"
- **Evidential markers**: "it is alleged," "reportedly," "according to"
- **Doxastic markers**: "I believe," "we think," "it seems"

Each modality SHALL be tagged with:
- Type (certainty/possibility/evidential/doxastic)
- Scope (which part of the claim is modified)
- Strength (high/medium/low confidence in the modality itself)

**FR-2.4** (TIER 3): Rhetorical devices (metaphor, hyperbole) SHOULD be detected where possible and tagged with **ST_AMBIG_RHETORIC**.

**Implementation reality**: Reliable automated detection of metaphor, irony, and hyperbole remains an unsolved research problem. Current models achieve ~60-70% accuracy.

**Phase 1 fallback**: Flag common metaphorical patterns using lexical databases (e.g., "X is a rising tide", "market as living organism")

**Phase 2 approach**: Use supervised ML models trained on labeled metaphor corpora (e.g., VUA metaphor corpus)

**Phase 3 goal**: Ensemble methods combining lexical, syntactic, and contextual signals

**Risk mitigation**: 
- False negatives (missed metaphors interpreted literally) will occur
- System should provide user override: "Flag this as rhetorical"
- Log all rhetoric flags for human review and model improvement

Examples:
- "The free market is a rising tide" → ST_AMBIG_RHETORIC (metaphor)
- "This law is worse than death" → ST_AMBIG_RHETORIC (hyperbole)

**FR-2.5 Non-Agentive Claims** (TIER 2): Claims without clear agents (weather phenomena, existential statements, quality attributions) SHALL:
- Be flagged as NON_AGENTIVE
- Attempt grounding using alternative patterns (ATT, EXT, REL)
- If grounding fails, route to Structured Ambiguity handling (FR-3.4)

---

### 4.3 Module 3: Ontological Grounding (OGM)

**FR-3.1** (TIER 1 for basic categories, TIER 2 for complete mapping): The system SHALL map CCU elements to **BFO/CCO top-level categories**.

#### Extended BFO Category Table

| BFO Category | Claim Role | Grounding Requirements | Examples |
|--------------|-----------|------------------------|----------|
| **Independent Continuant** | Agent / Patient | Spatially extended entity existing through time | "the patient," "the hospital" |
| **Material Entity** (subtype) | Agent / Patient | Physical object with mass | "the patient," "the scalpel" |
| **Object Aggregate** (subtype) | Collective Agent/Patient | Multiple material entities treated as unit | "the population," "the medical team" |
| **Process** | Action / Relation | Temporal occurrent with beginning and end | "surgery," "negotiation," "growth" |
| **Disposition** | Potential Action | Tendency/potential grounded in bearer | "fragility," "courage," "solubility" |
| **Quality** | Attribute | Property inhering in bearer | "red," "weight," "temperature" |
| **Role** | Agent/Patient modifier | Function dependent on context | "president," "victim," "student" |
| **Generically Dependent Continuant (GDC)** | Information Entity | Requires physical bearer | "the law," "the policy," "the plan" |
| **Temporal Region** | Temporal Context | When something occurs | "at 3pm," "in 2025," "during the war" |
| **Spatial Region** | Spatial Context | Where something exists/occurs | "in New York," "at the border" |
| **Site** | Location with function | Spatial region with role | "the operating room," "the border checkpoint" |

**FR-3.2 Category Error Detection** (TIER 1): The system SHALL reject claims where:

- **Agent is an abstraction without grounding**:
  - ❌ "Democracy demands accountability" (What IS democracy ontologically?)
  - ✓ "Democratic institutions require accountability mechanisms" (institutions = material/social entities)

- **Action is attributed to non-agents**:
  - ❌ "Freedom demands vigilance" (freedom is a quality or condition, not an agent)
  - ✓ "Free peoples must remain vigilant" (peoples = object aggregates)

- **Qualities act as agents**:
  - ❌ "Justice requires equality" (justice = abstract quality)
  - ✓ "Just legal systems implement equal treatment" (systems = material/social entities)

**FR-3.3 Grounding Failure** (TIER 1): Claims mapping to "Unknown" or "Vague" categories SHALL be routed to the Failure Module with code **ERR_ONT_MAP_FAIL**.

**FR-3.4 Structured Ambiguity** (TIER 2/3): Claims that are:
- Recognizably meaningful in discourse
- Ontologically underspecified
- Requiring contextualization to ground

SHALL be routed to a **Structured Ambiguity track** that:
- Preserves the original claim
- Documents the ontological ambiguity explicitly
- Provides a framework for progressive refinement
- Allows integration with IEE multi-perspectival evaluation (where different worldviews may ground the same term differently)

**Connection to Integral Ethics**: Terms like "justice," "freedom," "democracy" are grounded differently by different worldviews within the Integral Ethics framework. What **Materialism** sees as "social institutions," **Spiritualism** may see as "divine principles," and **Monadism** as "respect for individual dignity." The Structured Ambiguity track acknowledges this pluralism while maintaining epistemic rigor.

**Example**:
- Claim: "Justice requires proportional punishment"
- Structured Ambiguity Output:
  ```json
  {
    "original_claim": "Justice requires proportional punishment",
    "ambiguity_type": "ABSTRACT_TERM_MULTI_GROUNDING",
    "problematic_term": "Justice",
    "worldview_groundings": {
      "Realism": "Legal systems implementing natural law principles",
      "Rationalism": "Logical coherence in application of universal principles",
      "Spiritualism": "Divine command regarding moral order",
      "Materialism": "Social institutions maintaining order and security",
      "Monadism": "Respect for individual dignity and agency"
    },
    "context_required": [
      "Which ethical framework? (deontological, consequentialist, virtue-based, divine command)",
      "In what domain? (criminal law, economic policy, social relations)",
      "Which worldview perspective should be primary?"
    ],
    "integration_note": "IEE can evaluate this claim from all twelve worldview perspectives simultaneously"
  }
  ```

---

### 4.4 Module 4: Constraint & Sufficiency Validation (CSV)

**FR-4.1** (TIER 1): The system SHALL apply a **Sufficiency Gate** to every grounded claim, checking:
- **Temporal specification**: Is the timeframe clear?
- **Spatial specification**: Is the location/scope clear?
- **Quantification**: Are quantities/amounts specified?
- **Relational specificity**: Are vague relations (e.g., "related to") elaborated?

**FR-4.2 Causal Definition** (TIER 2): Causal claims (A caused B) SHALL be rejected unless:
1. Both A and B are grounded as **processes** (temporal occurrents)
2. A **temporally precedes** B (with specified time interval)
3. A **mechanism** is at least gestured toward (even if not fully specified)

**Examples**:

❌ **Insufficient**: "Capitalism causes inequality"
- Problem: Both are abstractions; mechanism unspecified; temporal relation unclear

✓ **Sufficient**: "The 1980s deregulation of financial markets (A) preceded the observed increase in wealth concentration ratios from 1985-2000 (B), with economists identifying reduced progressive taxation and capital mobility as mechanisms"
- A = grounded process with temporal boundaries
- B = grounded process with measurement
- Temporal sequence specified
- Mechanism gestured toward

**FR-4.3 Expanded Failure Taxonomy** (TIER 1):

The system SHALL tag validation failures with specific codes:

| Error Code | Description | Category | Example | Gap Analysis |
|------------|-------------|----------|---------|--------------|
| **ERR_AGENT_MISSING** | No identifiable agent found | Extraction | "It is important to act" | Specify WHO must act |
| **ERR_AGENT_ABSTRACT** | Agent is ungrounded abstraction | Grounding | "Democracy demands X" | Replace with concrete entity: "Democratic institutions demand X" |
| **ERR_AGENT_QUALITY** | Agent is a quality not an entity | Grounding | "Freedom requires X" | Qualities cannot act; specify who must act to preserve freedom |
| **ERR_PATIENT_MISSING** | No patient/object found | Extraction | "The policy affected" | Affected what/whom? |
| **ERR_ACTION_VAGUE** | Action verb too general | Validation | "X influenced Y" | Specify mechanism of influence |
| **ERR_SCOPE_VAGUE** | Claim lacks quantification | Validation | "Many people believe X" | How many? Which population? Timeframe? |
| **ERR_TEMPORAL_UNDERSPEC** | Timeframe missing or vague | Validation | "Recently, conditions improved" | Define "recently" with dates |
| **ERR_SPATIAL_UNDERSPEC** | Location/scope unclear | Validation | "Communities were affected" | Which communities? Where specifically? |
| **ERR_CAUSAL_GAP** | Causal link lacks process grounding | Validation | "Policy X caused Y" | Specify: process, temporal sequence, mechanism |
| **ERR_QUANTIFIER_VAGUE** | Vague quantity words | Validation | "Some improvement occurred" | How much? Measured how? Over what baseline? |
| **ERR_RELATION_UNDERSPEC** | Vague relation without mechanism | Validation | "X is related to Y" | How related? What kind of relation? |
| **ERR_NORMATIVE_MIXED** | Descriptive and evaluative conflated | Annotation | "The unjust policy failed" | Separate: "The policy failed" + "unjust" as overlay |
| **ERR_DISPOSITION_UNGROUNDED** | Disposition without bearer | Grounding | "Courage is needed" | Courage in whom? Context? |
| **ERR_QUALITY_UNATTRIBUTED** | Quality without entity | Grounding | "There is redness" | What entity is red? |
| **ERR_PROCESS_ATEMPORAL** | Process without temporal extent | Validation | "The event" (no when) | When did the process begin/end? |
| **ERR_ONT_MAP_FAIL** | Cannot map to any ontology category | Grounding | Nonsense text | Term not in lexicon, no analogues found |

**FR-4.4 Progressive Refinement** (TIER 2): When a claim fails sufficiency validation, the system SHALL:
- Generate specific suggestions for refinement (may be template-based in Phase 1)
- Provide examples of claims that would pass
- Allow iterative resubmission with modifications tracked

---

### 4.5 Module 5: Normative Annotation (NAM) - External Integration Point

**FR-5.1** (TIER 1): The system SHALL isolate **evaluative terms** from the **descriptive graph** using a curated lexicon of moral, aesthetic, prudential, and deontic terms.

**Common evaluative terms**:
- Moral: good, evil, right, wrong, just, unjust, virtuous, vicious
- Aesthetic: beautiful, ugly, elegant, crude
- Prudential: wise, foolish, beneficial, harmful
- Deontic: ought, should, must, permissible, forbidden

**FR-5.2 Value Overlay** (TIER 1): Evaluative terms SHALL be stored as **metadata "overlays"** that:
- Do not alter the underlying ontological triple
- Preserve the descriptive base layer
- Reference specific normative frameworks
- Include justification for the evaluation

**FR-5.3 Pluralist Support** (TIER 2): The system SHALL provide an API for external ethical reasoning engines (e.g., IEE) to attach **multiple normative evaluations** to the same descriptive claim.

**IMPORTANT LIMITATION**: ECCPS does not generate normative evaluations internally. It only:
1. Identifies where evaluative language appears
2. Separates it from descriptive content
3. Provides structured slots for external systems to populate

**Normative evaluation requires**:
- Domain expertise in ethical philosophy
- Explicit ethical frameworks with formal rules (such as Integral Ethics' twelve worldviews)
- Human judgment for novel cases

**Connection to Integral Ethics**: The IEE (Integral Ethics Engine) can evaluate the same descriptive claim from all twelve worldview perspectives:
- **Materialism**: Physical wellbeing impact
- **Monadism**: Respect for individual dignity
- **Rationalism**: Logical coherence with universal principles
- **Spiritualism**: Alignment with transcendent values
- *[...and eight others]*

Each worldview produces a distinct normative overlay on the same factual base.

**Example workflow**:
1. ECCPS processes: "The physician withdrew life-support from the patient"
2. ECCPS outputs clean descriptive graph
3. External IEE module applies 12 worldview evaluations
4. IEE returns normative overlays
5. ECCPS stores overlays linked to descriptive base

This design **separates concerns**: ECCPS handles ontological grounding, external systems handle normative reasoning.

**Example structure**:

**Descriptive base layer**:
```json
{
  "agent": "physician",
  "action": "withdrew life-support",
  "patient": "terminally ill patient",
  "temporal_context": "2025-01-15 14:30",
  "epistemic_status": "factual_claim"
}
```

**Normative overlays** (populated by external IEE):
```json
{
  "overlays": [
    {
      "framework": "Monadism (IEE)",
      "evaluation": "Respecting patient autonomy",
      "valence": "positive",
      "reasoning": "Patient's stated wishes honored",
      "worldview_basis": "Individual uniqueness and authentic agency"
    },
    {
      "framework": "Spiritualism (IEE)",
      "evaluation": "Ending sacred life prematurely",
      "valence": "negative",
      "reasoning": "Life preservation prioritized in transcendent hierarchies",
      "worldview_basis": "Sanctity of life grounded in spiritual reality"
    },
    {
      "framework": "Materialism (IEE)",
      "evaluation": "Reducing physical suffering",
      "valence": "positive",
      "reasoning": "Pain minimization achieved",
      "worldview_basis": "Physical wellbeing as primary value"
    }
  ]
}
```

---

### 4.6 Module 6: Conflict Resolution (CR)

**FR-6.1** (TIER 2): When multiple grounded claims contradict, the system SHALL:
- Detect the contradiction
- Preserve both claims with conflict flag
- NOT automatically resolve in favor of one claim

**FR-6.2 Contradiction Detection** (TIER 2): Claims contradict when:
- They assert opposite truth values about the same predicate
- They assert mutually exclusive properties
- They assert incompatible temporal/spatial facts

**Example**:
- Claim A: "The patient died at 3:00pm"
- Claim B: "The patient died at 3:15pm"
- Conflict type: TEMPORAL_INCOMPATIBILITY

**FR-6.3 Source Reliability Metadata** (TIER 2): The system SHALL allow (but not require) claims to include:
- Source reliability scores
- Epistemic provenance (first-hand observation, report, inference)
- Conflict resolution preferences (user-specified rules)

**FR-6.4** (TIER 1): The system SHALL NOT automatically privilege one claim over another based on:
- Source authority alone (without explicit user configuration)
- Temporal priority (newer ≠ more accurate)
- Majority agreement (multiple sources asserting the same claim)

**FR-6.5** (TIER 2): Conflict reports SHALL include:
- All contradictory claims with provenance
- Type of contradiction
- Suggested resolution strategies (if applicable)
- Requirement for human adjudication

---

### 4.7 Module 7: Claim Composition & Reasoning Chains (CC)

**FR-7.1 Scope Limitation** (TIER 1): ECCPS is primarily a **claim validation system**, not a **reasoning engine**.

Multi-claim reasoning (arguments, inferences, causal chains) is **out of scope** for core ECCPS but may be handled by downstream systems.

**FR-7.2 Claim Linking** (TIER 2): The system SHALL support explicit linking between claims:
- **Supports**: Claim A provides evidence for Claim B
- **Contradicts**: Claim A conflicts with Claim B
- **Entails**: Claim A logically implies Claim B (formal entailment)
- **Precedes**: Claim A describes an event before Claim B
- **Causes**: Claim A describes a process causing process in Claim B

**FR-7.3** (TIER 2): Links SHALL be:
- Explicitly asserted (not inferred automatically)
- Traceable to their source
- Typed with relation category
- Subject to validation (e.g., causal links must meet FR-4.2)

**FR-7.4 Downstream Integration** (TIER 1): Claims validated by ECCPS may be consumed by:
- **IEE**: Multi-perspectival ethical evaluation using Integral Ethics framework
- **ARCHON**: Governance decision-making for ASI risks
- **Argumentation systems**: Formal reasoning engines
- **Knowledge graphs**: Semantic web integration

---

### 4.8 Module 8: User Feedback & Iterative Refinement (UFR)

**FR-8.1** (TIER 2/3): When ECCPS rejects a claim, the system SHALL provide:
- **Failure report** with specific error code (TIER 2)
- **Gap analysis** specifying what is missing (TIER 2)
- **Example claims** that would pass validation (TIER 2, template-based initially)
- **Alternative formulations** (TIER 3, requires sophisticated generation)

**Note**: Generating fully automated, context-specific alternative formulations with detailed gap analysis is a TIER 3 capability. Phase 1-2 will use templates and examples. Phase 3 may integrate advanced language models with human-in-loop validation.

**FR-8.2 Interactive Refinement** (TIER 2): The system SHALL support:
- **Guided mode**: Step-by-step prompts to elicit missing information
- **Iterative submission**: Users can resubmit modified claims with previous context preserved
- **Learning analytics**: Track common failure patterns to improve user guidance

**FR-8.3 Challenge Mechanism** (TIER 2): Users SHALL be able to:
- **Challenge rejections** with justification
- **Propose alternative groundings** for ambiguous terms
- **Request human review** for borderline cases

**FR-8.4** (TIER 2): Challenges and human reviews SHALL be:
- Logged for system improvement
- Included in validation test corpus
- Used to refine grounding rules

---

## 5. Non-Functional Requirements (NFR)

**NFR-1 Statistical Determinism** (TIER 1):
- The system SHALL achieve **99%+ output consistency** over repeated runs with identical inputs and configuration
- All variation SHALL be logged with:
  - Source of non-determinism (LLM sampling, floating-point, etc.)
  - Magnitude of difference
  - Timestamp and version information
- When utilizing LLM components:
  - Use temperature=0 or equivalent low-temperature settings
  - Use fixed random seeds where applicable
  - Log exact model version and API endpoint
  - Implement retry logic with consistency checking

**NFR-2 Explainability** (TIER 1):
- Every rejection (Failure Report) MUST cite:
  - The specific FR (e.g., FR-3.2) that triggered the rejection
  - The reasoning chain leading to rejection
  - Suggested paths to validation
- Every successful grounding MUST include:
  - Provenance chain from source text to structured output
  - All intermediate transformations
  - Confidence scores for probabilistic components

**NFR-3 Modular Ontologies** (TIER 2):
- The system SHALL allow swapping BFO for other Upper Ontologies without rewriting core Extraction Module
- Supported alternatives:
  - **DOLCE** (Descriptive Ontology for Linguistic and Cognitive Engineering)
  - **SUMO** (Suggested Upper Merged Ontology)
  - **Domain-specific ontologies** (medical, legal, etc.)
- Ontology modules SHALL declare:
  - Category mappings
  - Grounding rules
  - Validation constraints

**NFR-4 Performance** (Tiered by Mode):

**STRICT MODE (Detailed Analysis)**:
- Latency target: <10 seconds per claim
- Rationale: Allows multiple LLM calls, ontology lookups, validation checks
- Optimization: Cache common patterns, parallel processing

**GUIDED MODE (Interactive)**:
- Latency target: <3 seconds per interaction step
- Rationale: Real-time feel for conversational refinement
- Optimization: Staged processing (quick checks first, deep analysis on demand)

**AUDIT MODE (Batch)**:
- Throughput target: 100-500 claims/minute
- Rationale: Batch processing allows heavy optimization
- Optimization: Parallel workers, GPU acceleration, aggressive caching

**Phase 1 realistic targets** (minimal LLM use):
- AUDIT MODE: 50 claims/minute (achievable with rule-based checks)

**Phase 2 targets** (moderate LLM use):
- GUIDED MODE: 5 seconds/interaction
- AUDIT MODE: 100 claims/minute

**Phase 3 targets** (full system):
- STRICT MODE: 10 seconds/claim
- GUIDED MODE: 3 seconds/interaction
- AUDIT MODE: 500 claims/minute

**Infrastructure assumptions**:
- Dedicated GPU servers for LLM inference
- Redis cache for ontology lookups
- Distributed processing for batch mode

**NFR-5 Multilingual Support (Phased)**:
- **Phase 1** (Current): English-only
- **Phase 2**: Add high-resource languages (Spanish, French, German, Mandarin)
- **Phase 3**: Add additional languages with community contribution
- Each language module SHALL:
  - Adapt extraction patterns to language structure
  - Maintain ontological grounding consistency
  - Preserve traceability in original language

**NFR-6 Accessibility** (TIER 1):
- **API**: RESTful API for programmatic access
- **CLI**: Command-line interface for batch processing
- **Web UI**: Browser-based interface for interactive refinement (Phase 2)
- **Documentation**: Comprehensive examples and tutorials

---

## 6. Output Specifications

### 6.1 Validated Claim Graph

**Format**: JSON-LD or RDF (Turtle, N-Triples)

**Structure**:
```json
{
  "@context": "http://eccps.org/context/v3.1",
  "@id": "urn:eccps:claim:abc123",
  "source_artifact": "urn:eccps:artifact:xyz789",
  "source_span": {
    "start": 145,
    "end": 203,
    "text": "The patient died after treatment was withdrawn."
  },
  "extraction_pattern": "Agent-Action-Patient",
  "elements": {
    "agent": {
      "text": "the patient",
      "bfo_category": "Material Entity",
      "role": "Human Patient",
      "span": [145, 156]
    },
    "action": {
      "text": "died",
      "bfo_category": "Process",
      "temporal_extent": "instantaneous_completion",
      "span": [157, 161]
    },
    "temporal_context": {
      "text": "after treatment was withdrawn",
      "relation": "FOLLOWS",
      "preceding_process": "treatment withdrawal",
      "span": [162, 191]
    }
  },
  "epistemic_status": "factual_claim",
  "modality": "none",
  "validation_status": "PASSED",
  "normative_overlays": [],
  "timestamp": "2025-01-15T10:30:00Z",
  "eccps_version": "3.1"
}
```

### 6.2 Structured Failure Report

**Format**: JSON

**Structure**:
```json
{
  "@context": "http://eccps.org/context/failure/v3.1",
  "@id": "urn:eccps:failure:def456",
  "source_artifact": "urn:eccps:artifact:xyz789",
  "target_ccu": {
    "span": [204, 245],
    "text": "Democracy demands accountability from leaders."
  },
  "failure_code": "ERR_AGENT_ABSTRACT",
  "failed_module": "Ontological Grounding (OGM)",
  "failed_requirement": "FR-3.2",
  "diagnosis": {
    "problematic_element": "Democracy",
    "issue": "Abstract noun used as agent without grounding",
    "bfo_mapping_attempted": "Unknown/Vague",
    "category_error": "Abstraction cannot perform actions"
  },
  "gap_analysis": {
    "missing": [
      "What material or social entity does 'Democracy' refer to?",
      "Democratic institutions? Democratic processes? Democratic citizens?"
    ],
    "required_for_pass": "Replace 'Democracy' with grounded entity (e.g., 'Democratic institutions', 'Citizens in democracies')"
  },
  "suggested_refinements": [
    "Democratic institutions require accountability mechanisms for leaders.",
    "Citizens in democracies demand accountability from their leaders.",
    "Democratic governance processes include accountability structures."
  ],
  "structured_ambiguity_available": true,
  "worldview_note": "The term 'Democracy' can be grounded differently depending on ethical framework: Materialism sees it as social institutions, Idealism as consciousness development, Spiritualism as alignment with transcendent values. See Integral Ethics framework for multi-perspectival analysis.",
  "timestamp": "2025-01-15T10:30:05Z"
}
```

### 6.3 Aggregate Document Report (Batch Mode)

**Format**: JSON

**Structure**:
```json
{
  "document_id": "urn:eccps:doc:policy_draft_2025",
  "total_ccus": 487,
  "processed_claims": 487,
  "validation_outcomes": {
    "PASSED": 312,
    "FAILED": 144,
    "STRUCTURED_AMBIGUITY": 31,
    "PROCESSING_ERROR": 0
  },
  "failure_breakdown": {
    "ERR_AGENT_ABSTRACT": 45,
    "ERR_SCOPE_VAGUE": 38,
    "ERR_TEMPORAL_UNDERSPEC": 29,
    "ERR_CAUSAL_GAP": 23,
    "ERR_AGENT_MISSING": 9
  },
  "conflicts_detected": 5,
  "validation_rate": 0.64,
  "average_errors_per_failed_claim": 1.2,
  "recommendations": {
    "top_issues": [
      "High incidence of abstract agents (45 cases) - use concrete institutional references",
      "Temporal specifications missing (29 cases) - add specific dates/timeframes",
      "5 contradictions detected - requires human review"
    ],
    "suggested_actions": [
      "Review Section 3 (paragraphs 15-22) - contains 12 ERR_AGENT_ABSTRACT",
      "Add temporal context to claims in Section 5",
      "Resolve contradictions: Claims #45 vs #203, #78 vs #301, #156 vs #389"
    ]
  },
  "quality_score": 0.64,
  "processing_metadata": {
    "eccps_version": "3.1",
    "processing_time_seconds": 145,
    "mode": "AUDIT",
    "timestamp": "2025-01-15T14:30:00Z"
  }
}
```

**Note**: All failures must map to defined error codes. If a novel error is encountered, it triggers:
- `ERR_UNCLASSIFIED` with human review flag
- Automatic ticket to expand taxonomy
- Logged for next version update

---

## 7. Validation & Testing

### 7.1 Gold Standard Test Corpus (Phased Development)

ECCPS validation requires a substantial test corpus. We acknowledge this is a major undertaking requiring significant resources.

**Phase 1 Corpus** (Months 1-6): 100 claims
- 50 clear pass cases
- 50 clear fail cases (diverse error types)
- Single domain (medical ethics or policy)
- 2-3 expert annotators
- Estimated effort: 40-60 hours
- Budget: $2,000-3,000

**Phase 2 Corpus** (Months 7-12): 250 claims
- Add 100 structured ambiguity cases
- Add 50 edge cases with documented disagreements
- Expand to 2 domains (medical + policy)
- 4-5 expert annotators
- Inter-rater reliability testing begins
- Estimated effort: 120-180 hours
- Budget: $6,000-9,000

**Phase 3 Corpus** (Months 13-18): 500 claims
- Add 50 conflict cases
- Add 100 additional domain-specific claims (legal, scientific)
- Full diversity across all modules
- 6-8 expert annotators
- Cohen's Kappa ≥ 0.75 target
- Estimated effort: 200-300 hours
- Budget: $10,000-15,000

**Annotation Protocol**:
Each claim requires:
- Expected outcome (PASS/FAIL/STRUCTURED_AMBIGUITY)
- Error codes (if FAIL)
- BFO category mappings (if PASS)
- Rationale (2-3 sentences)
- Alternative formulations (2-3 examples)

**Resource requirements**:
- Expert ontologists: 300-500 hours total
- Domain specialists: 200-300 hours total
- Total budget estimate: $20,000-30,000 (if hiring external annotators)

**Risk mitigation**:
- Start small (100 claims)
- Validate with this subset before expanding
- Use corpus development to refine requirements
- Consider public contribution model for Phase 3

### 7.2 Inter-Rater Reliability

**Human annotators SHALL achieve**:
- **Cohen's Kappa ≥ 0.75** for pass/fail decisions
- **Agreement ≥ 0.70** on error code assignment
- **Disagreement cases** documented and included in edge case corpus

### 7.3 Continuous Validation

**The system SHALL**:
- Run test corpus on every version release
- Report consistency metrics (% agreement with gold standard)
- Flag regressions (claims that changed validation status)
- Track performance improvements over versions

---

## 8. Philosophical Grounding in Integral Ethics

### 8.1 Alignment with Integral Ethics Framework

ECCPS embodies principles central to the Integral Ethics framework developed by Steiner and contemporary researchers:

**1. Truth as Reality-Correspondence**
- Integral Ethics: **Truth/Reality-Alignment** is a terminal value—"Conformity of belief/action to reality; intellectual honesty"
- ECCPS: Claims must correspond to objective reality structured by BFO categories; refuses to process claims that cannot be grounded

**2. Multi-Perspectival Integration**
- Integral Ethics: Mature ethical thinking requires **Integral Consciousness**—"capacity to hold twelve worldviews without collapsing into relativism"
- ECCPS: Structured Ambiguity track (FR-3.4) acknowledges that terms can be grounded differently by different worldviews; enables IEE to evaluate from all twelve perspectives

**3. Epistemic Humility**
- Integral Ethics: **Epistemic Humility** as constraining value—"Recognition of fallibility; openness to being wrong"
- ECCPS: Acknowledges ungroundable claims rather than forcing interpretation; makes uncertainty explicit; allows challenges to system decisions

**4. Non-Coercion and Transparency**
- Integral Ethics: **Non-Coercion** and **Transparency** as constraining values on methods
- ECCPS: Does not enforce moral conclusions; provides complete justification chains; users can challenge and override

**5. Respect for Pluralism Without Relativism**
- Integral Ethics: **Limited Pluralism**—"Multiple legitimate paths exist; not all paths equally valid"
- ECCPS: Accommodates diverse worldview groundings while maintaining objective standards for clarity

### 8.2 The Twelve Worldviews and ECCPS

ECCPS primarily operates within the **Realism** worldview of Integral Ethics ("objective truth, correspondence to reality, natural law"), but its architecture acknowledges and accommodates all twelve archetypal perspectives:

| Worldview | How ECCPS Honors It |
|-----------|---------------------|
| **Materialism** | Material entities as primary; physical processes grounded in spatiotemporal reality |
| **Sensationalism** | Phenomenological descriptions preserved; lived experience acknowledged |
| **Phenomenalism** | Perspective-dependence noted; interpretation vs. objective claim distinguished |
| **Realism** | Core commitment; correspondence to objective reality; BFO grounding |
| **Dynamism** | Processes have temporal extent; becoming acknowledged alongside being |
| **Monadism** | Individual perspectives preserved in Structured Ambiguity; unique contexts matter |
| **Idealism** | Consciousness and information entities (GDCs) formally represented |
| **Rationalism** | Logical coherence required; rational principles govern validation |
| **Psychism** | Psychological states and dispositions modeled (though not attributed to AI) |
| **Pneumatism** | Spiritual vitality concepts can be grounded when contextualized |
| **Spiritualism** | Transcendent values acknowledged in normative overlay structure |
| **Mathematism** | Formal structure and mathematical precision in ontology itself |

### 8.3 Integration with IEE (Integral Ethics Engine)

**The ECCPS-IEE relationship**:

1. **ECCPS provides the descriptive base layer**: Factual claims grounded in BFO/CCO ontology using primarily the **Realism** worldview
2. **IEE applies multi-perspectival evaluation**: The same factual claim evaluated from all twelve worldviews
3. **Normative overlays returned to ECCPS**: Multiple conflicting evaluations stored as metadata
4. **Structured pluralism maintained**: Objective factual grounding + multiple legitimate value perspectives

**Example**:
- ECCPS processes: "The patient died after treatment withdrawal"
- ECCPS output: Clean descriptive graph with ontological grounding
- IEE evaluates from twelve perspectives:
  - **Materialism**: Physical suffering ended
  - **Monadism**: Individual autonomy respected
  - **Spiritualism**: Life sanctity considerations
  - **Rationalism**: Universal principle of autonomy applied
  - *[...and eight others]*
- Each worldview produces distinct normative overlay
- ECCPS stores all overlays linked to descriptive base

This prevents the reduction of ethics to single-foundation systems while maintaining rigorous factual grounding.

### 8.4 What ECCPS Does Not Claim

**ECCPS does not**:
- Replace human moral judgment (it informs deliberation, not decides)
- Claim metaphysical completeness (BFO is one framework among possible others)
- Resolve ethical disputes (it processes claims; IEE evaluates; humans decide)
- Substitute for wisdom, courage, or virtue (these remain human capacities)
- Guarantee perfect epistemic outcomes (fallibility acknowledged)

**ECCPS is a tool for rigorous moral reasoning, not a replacement for moral agents.**

---

## 9. Integration with ARCHON and IEE

### 9.1 ARCHON Integration

**ARCHON** (Artificial Responsible Custodian Honoring Ontological Neutrality) is a proposed governance framework for ASI risks requiring ECCPS to:

1. **Validate governance claims** before policy adoption
   - "System X exhibits deceptive alignment" → ECCPS demands specification with observable criteria
2. **Ensure traceability** from policy to evidence
   - Every ARCHON decision must trace to ECCPS-validated claims
3. **Detect contradictions** in institutional reporting
   - Conflicting capability assessments flagged
4. **Prevent governance-by-vibe**
   - Rhetorical claims rejected; forces epistemic rigor

### 9.2 IEE Integration

**IEE** (Integral Ethics Engine) implements the twelve-worldview framework requiring ECCPS to:

1. **Separate descriptive from normative layers**
   - Clean factual base for multi-perspectival evaluation
2. **Handle structured ambiguity**
   - Terms grounded differently by different worldviews
3. **Enable normative overlay**
   - Same fact + twelve conflicting evaluations
4. **Maintain epistemic honesty**
   - Only grounded claims reach IEE

**Dataflow**:
```
Natural Language Claim
    ↓
ECCPS Validation
    ↓
├─ PASS → Validated Claim Graph → IEE Evaluation
│          (Descriptive base)      (12 worldviews)
│
├─ FAIL → Structured Failure Report → User Refinement → Retry
│
└─ STRUCTURED_AMBIGUITY → Context Preserved → IEE handles perspectival grounding
```

---

## 10. Implementation Phases

### Phase 1: Core Validation (Months 1-6)
- Modules 1-4 (LAI, CET, OGM, CSV)
- TIER 1 requirements only
- English-only, BFO/CCO grounding
- AUDIT mode only, CLI interface
- 100-claim test corpus
- Target: Prove concept viability

### Phase 2: Enhanced Functionality (Months 7-12)
- Module 5 (NAM) with IEE integration API
- Module 6 (CR) conflict detection
- TIER 2 requirements where feasible
- GUIDED mode with progressive disclosure
- Web UI with iterative refinement
- 250-claim test corpus
- Target: Demonstrate utility

### Phase 3: Advanced Features (Months 13-18)
- Module 7 (CC) claim linking
- Module 8 (UFR) user feedback system
- TIER 3 research prototypes (human-in-loop)
- STRICT mode for governance
- 500-claim test corpus with full diversity
- Target: Production-ready for ARCHON/IEE

### Phase 4: Extension & Scale (Months 19-24)
- Alternative ontology modules (DOLCE, SUMO)
- Additional language support
- Performance optimization
- Public API with comprehensive documentation
- Target: Broader adoption

---

## Appendix A: Error Code Reference

**[Complete taxonomy with all codes, definitions, examples, remediation - see FR-4.3]**

---

## Appendix B: Example Transformations

**[50+ examples showing processing for both successful and failed validations]**

---

## References

Arp, R., Smith, B., & Spear, A. D. (2015). *Building Ontologies with Basic Formal Ontology*. MIT Press.

Steiner, R. (1914/2008). *The Riddles of Philosophy*. Anthroposophic Press.

For complete Integral Ethics framework, see: Schatz, A. (2025). *Integral Ethics: A Twelve-Fold Foundation for Human Flourishing*. [https://github.com/Skreen5hot/Ontology-of-Freedom](https://github.com/Skreen5hot/Ontology-of-Freedom)

---

**Document Version**: 3.1  
**Status**: Implementation-Ready Specification  
**Last Updated**: 2025-01-15  
**Authors**: Aaron Schatz, with critical review integration  
**License**: Open specification for AI ethics infrastructure

**Major changes from v3.0**:
- Removed Orthodox Christian theological framing
- Integrated Integral Ethics framework references
- Fixed all error code inconsistencies (ERR_AGENT_ABSTRACT standardized)
- Cleaned up ontology category table (removed "Immaterial Entity" confusion)
- Added tiered requirement classification (CORE/EXTENDED/RESEARCH)
- Added User Experience Strategy section with three modes
- Revised performance targets to be realistic
- Acknowledged test corpus resource requirements honestly
- Clarified Module 5 as external integration point
- Added honest scope and limitations section
- Fixed aggregate report structure (removed "other" category)
- Added philosophical grounding in Integral Ethics