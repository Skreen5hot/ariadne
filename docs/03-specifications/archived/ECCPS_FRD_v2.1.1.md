> **ARCHIVED:** This document has been superseded by ECCPS Specification v3.1 (`docs/03-specifications/eccps-specification.md`). Retained for historical reference. See ARIADNE finding F-S03-1.

# Functional Requirements Document (FRD) v2.1.1

**System Name:** Epistemically Constrained Claim Processing System (ECCPS)
**Status:** Archived — Superseded by v3.1
**Version Date:** January 2026
**Focus:** Realist Ontology (BFO), Epistemic Friction, and Failure-as-Signal

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.0 | — | — | Initial integrated review draft |
| 2.1 | January 2026 | — | Architecture expansion, feasibility refinements, acceptance criteria |
| 2.1.1 | January 2026 | — | Causal mechanism specification, document mode state persistence, BFO mapping reference |

---

## 1. Purpose & Core Philosophy

The ECCPS is a semantic gatekeeper. It processes natural language to determine if a claim possesses the ontological density and epistemic clarity required for machine-interpretable structure.

The system operates on the principle of **Maximum Traceability**: every structured output must be decomposable back to its original linguistic artifact, with every transformation logged as a discrete epistemic choice.

### 1.1 Problem Statement

Natural language claims vary enormously in their epistemic quality—from precise, verifiable assertions to vague, rhetorical, or unfalsifiable statements. Most NLP systems attempt to extract structure from all inputs indiscriminately, producing brittle knowledge graphs filled with ambiguous or ungrounded claims.

ECCPS inverts this paradigm: rather than maximizing extraction, it maximizes *epistemic integrity* by filtering claims through rigorous ontological and epistemic constraints. The system's primary output is a clear determination of whether a claim *can* be grounded, and if not, *why not*.

### 1.2 Target Use Cases

- Pre-processing pipeline for knowledge graph construction
- Epistemic quality assessment for automated fact-checking systems
- Claim validation layer for semantic web applications
- Training data curation for machine learning systems requiring high-quality assertions
- Regulatory and compliance document analysis

---

## 2. Design Principles

| Principle | Description | Implementation Implication |
|-----------|-------------|---------------------------|
| **Failure is a Success State** | Identifying a claim as "un-groundable" is a high-value output | System must produce structured failure reports with actionable gap analysis |
| **Explicit Traceability** | No transformation shall occur without a preserved link to the source text | Character-offset provenance required for all extracted elements |
| **Ontological Realism** | The system assumes a world of material entities and processes (BFO-aligned) | Grounding validates against realist ontology categories |
| **Epistemic Friction** | The system is intentionally "difficult" to satisfy; it resists smoothing over ambiguity | Conservative defaults; ambiguity triggers failure rather than best-guess interpretation |
| **Bounded Determinism** | Identical inputs + identical configuration = functionally equivalent outputs | Reproducibility within defined tolerance; determinism guarantees specified per component |
| **Graceful Uncertainty** | The system acknowledges confidence gradients rather than forcing binary outcomes | Confidence scores accompany all grounding decisions |

---

## 3. High-Level Functional Architecture

### 3.1 System Context Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ECCPS Boundary                                  │
│                                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐  │
│  │   LAI   │───▶│   CET   │───▶│   OGM   │───▶│   CSV   │───▶│   NAM    │  │
│  │ Intake  │    │Extract  │    │ Ground  │    │Validate │    │Annotate  │  │
│  └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘    └────┬─────┘  │
│       │              │              │              │              │        │
│       │              │              │              │              │        │
│       ▼              ▼              ▼              ▼              ▼        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Provenance & Audit Layer                        │   │
│  │              (Transformation Log, Character Offsets)                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                      │             │
│       ▼                                                      ▼             │
│  ┌──────────┐                                         ┌──────────────┐     │
│  │ Failure  │                                         │   Output     │     │
│  │ Reports  │                                         │   Manager    │     │
│  └──────────┘                                         └──────────────┘     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
        ▲                                                      │
        │                                                      ▼
   ┌─────────┐                                          ┌─────────────┐
   │  Input  │                                          │   Output    │
   │ Sources │                                          │  Consumers  │
   └─────────┘                                          └─────────────┘
```

### 3.2 Data Flow Description

1. **Intake (LAI):** Raw text artifacts enter the system, receive unique identifiers, and are segmented into Candidate Claim Units (CCUs).

2. **Extraction (CET):** Each CCU is parsed to extract semantic roles (Agent, Action/Relation, Patient), epistemic modalities, and rhetorical markers. All extractions maintain character-offset provenance.

3. **Grounding (OGM):** Extracted elements are mapped to BFO/CCO ontological categories. Category errors and mapping failures are detected and routed to failure handling.

4. **Validation (CSV):** Grounded claims pass through sufficiency gates that verify causal structure, temporal boundaries, and quantification requirements.

5. **Annotation (NAM):** Validated claims receive normative overlays separating descriptive content from evaluative content.

6. **Output:** Successfully processed claims emit as validated claim graphs; failures emit as structured failure reports with gap analysis.

### 3.3 Module Interfaces

| Interface | From | To | Payload |
|-----------|------|-----|---------|
| I-01 | LAI | CET | CCU with UAID, source offsets, context window |
| I-02 | CET | OGM | Extracted triple with provenance, modality tags |
| I-03 | OGM | CSV | Grounded triple with BFO category assignments |
| I-04 | CSV | NAM | Validated claim with sufficiency attestation |
| I-05 | Any Module | Failure Handler | Failure packet with module ID, error code, context |
| I-06 | NAM | Output Manager | Complete claim graph with normative overlays |

---

## 4. Input Specifications

### 4.1 Supported Input Formats

| Format | Extension | Requirements | Notes |
|--------|-----------|--------------|-------|
| Plain Text | .txt | UTF-8 encoding | Primary supported format |
| Markdown | .md | UTF-8 encoding | Structural markers preserved as metadata |
| HTML | .html | Valid HTML5 | Text extracted; structure preserved as metadata |
| JSON | .json | UTF-8, valid JSON | Expects `text` field or array of text fields |
| PDF | .pdf | Text-extractable | OCR not in scope for v1 |

### 4.2 Input Constraints

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Maximum artifact size | 1 MB | Memory management; larger documents should be chunked |
| Maximum CCU length | 2,000 characters | Extraction accuracy degrades beyond this |
| Minimum CCU length | 10 characters | Below this, insufficient content for claim extraction |
| Character encoding | UTF-8 required | Standardization for offset calculations |
| Language | English (v1) | Multilingual support deferred to v2 |

### 4.3 Input Metadata Schema

```json
{
  "artifact_id": "string (optional, system generates if absent)",
  "source_uri": "string (optional)",
  "author": "string (optional)",
  "timestamp": "ISO 8601 datetime (optional)",
  "domain": "string enum: [general, legal, scientific, journalistic, technical]",
  "processing_hints": {
    "expected_claim_density": "low | medium | high",
    "rhetorical_mode": "declarative | argumentative | narrative"
  }
}
```

---

## 5. Functional Requirements

### 5.1 Module 1: Language Artifact Intake (LAI)

#### Core Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-1.1 | The system SHALL ingest text artifacts and assign a Unique Artifact ID (UAID) | Must | UAID is UUID v4; collision probability < 10^-18 |
| FR-1.2 | The system SHALL preserve the raw source as a "Root Node" for all downstream provenance | Must | Raw source retrievable by UAID; byte-identical to input |
| FR-1.3 | The system SHALL segment text into Candidate Claim Units (CCUs) without stripping context | Must | Each CCU includes ±2 sentence context window |
| FR-1.4 | The system SHALL detect and tag document structure (headings, lists, paragraphs) | Should | Structure tags applied with 95%+ accuracy on well-formed documents |
| FR-1.5 | The system SHALL normalize whitespace while preserving semantic boundaries | Must | Multiple spaces → single space; paragraph breaks preserved |

#### Segmentation Logic (FR-1.3 Detail)

CCU segmentation follows this precedence:

1. **Sentence boundaries** (primary): Determined by terminal punctuation (.!?) followed by whitespace and capital letter, with exceptions for common abbreviations (Mr., Dr., etc.)

2. **Clause boundaries** (secondary): For sentences exceeding 500 characters, segment at coordinating conjunctions (and, but, or) or semicolons when they separate independent clauses

3. **Enumeration handling**: Bulleted or numbered lists generate one CCU per item, with list context preserved as metadata

4. **Quotation handling**: Quoted material remains with its framing sentence; direct quotes are tagged for attribution analysis

### 5.2 Module 2: Claim Extraction & Traceability (CET)

#### Core Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-2.1 | The system SHALL extract semantic roles from CCUs | Must | See Role Extraction specification below |
| FR-2.2 | Every extracted element MUST retain a character-offset pointer to the source artifact | Must | Offset tuple [start, end] valid for source reconstruction |
| FR-2.3 | The system SHALL identify and flag Epistemic Modalities | Must | Modality taxonomy applied; see table below |
| FR-2.4 | Rhetorical devices SHALL be detected and tagged rather than interpreted | Must | Confidence threshold ≥ 0.7 for ST_AMBIG_RHETORIC |
| FR-2.5 | The system SHALL handle n-ary relations beyond simple triples | Should | Support for 4-ary relations (Agent, Action, Patient, Instrument) |
| FR-2.6 | Agent-less claims SHALL be explicitly typed and processed | Must | Meteorological, existential, and passive constructions handled |

#### Role Extraction Specification (FR-2.1 Detail)

The system extracts claims into an extended semantic role structure:

| Role | Definition | Required | Examples |
|------|------------|----------|----------|
| Agent | Entity initiating or causing the action | Conditional | "The committee voted..." → Agent: committee |
| Action | The process, event, or state change | Required | "...voted to approve..." → Action: voted |
| Patient | Entity affected by the action | Conditional | "...approve the proposal" → Patient: proposal |
| Instrument | Means by which action is accomplished | Optional | "...approved via email ballot" → Instrument: email ballot |
| Temporal | When the action occurs | Optional | "...on Tuesday" → Temporal: Tuesday |
| Locative | Where the action occurs | Optional | "...in the main conference room" → Locative: main conference room |
| Manner | How the action is performed | Optional | "...unanimously" → Manner: unanimously |

**Agent-less Claim Types:**

| Type | Pattern | Handling |
|------|---------|----------|
| Meteorological | "It rained yesterday" | Mark Agent as METEOROLOGICAL_NULL; proceed to grounding |
| Existential | "There are three options" | Mark Agent as EXISTENTIAL_NULL; extract Patient as subject |
| Passive (vague) | "The policy was implemented" | Mark Agent as PASSIVE_UNSPECIFIED; flag for gap analysis |
| Generic | "One should always verify" | Mark Agent as GENERIC_REFERENCE; proceed with caution flag |

#### Epistemic Modality Taxonomy (FR-2.3 Detail)

| Code | Label | Markers | Example |
|------|-------|---------|---------|
| MOD_CERTAIN | Certainty | "definitely," "certainly," "undoubtedly" | "This is certainly true" |
| MOD_PROBABLE | Probability | "probably," "likely," "most likely" | "She will probably attend" |
| MOD_POSSIBLE | Possibility | "possibly," "might," "could," "may" | "It could rain tomorrow" |
| MOD_ALLEGED | Attribution | "allegedly," "reportedly," "it is claimed" | "He allegedly committed fraud" |
| MOD_CONDITIONAL | Conditionality | "if," "unless," "provided that" | "If passed, the bill would..." |
| MOD_NECESSITY | Necessity | "must," "have to," "necessarily" | "We must act now" |
| MOD_UNMARKED | No explicit modality | (absence of markers) | "The cat sat on the mat" |

#### Rhetorical Device Detection (FR-2.4 Detail)

| Device | Detection Approach | Confidence Handling |
|--------|-------------------|---------------------|
| Metaphor | Pattern matching + semantic incongruity detection | If confidence < 0.7, tag as ST_POSSIBLE_RHETORIC |
| Hyperbole | Magnitude markers + context analysis | Quantitative claims with extreme values flagged for review |
| Irony/Sarcasm | Sentiment-semantic mismatch | Low-confidence detection; conservative tagging |
| Rhetorical Question | Interrogative form + assertion analysis | Question form conveying assertion tagged |

**Confidence Scoring for Rhetoric:**

```
rhetorical_confidence = weighted_average(
    pattern_match_score * 0.4,
    semantic_incongruity_score * 0.3,
    context_indicator_score * 0.3
)

if rhetorical_confidence >= 0.7:
    tag = ST_AMBIG_RHETORIC
elif rhetorical_confidence >= 0.4:
    tag = ST_POSSIBLE_RHETORIC
else:
    tag = ST_LITERAL (proceed to grounding)
```

### 5.3 Module 3: Ontological Grounding Module (OGM)

#### Core Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-3.1 | The system SHALL map CCU elements to BFO/CCO top-level categories | Must | Mapping accuracy ≥ 80% on benchmark corpus |
| FR-3.2 | The system SHALL detect and reject category errors | Must | See Category Error Detection below |
| FR-3.3 | Claims mapping to "Unknown" or "Vague" SHALL route to Failure Module | Must | Error code ERR_ONT_MAP with gap analysis |
| FR-3.4 | The system SHALL assign confidence scores to all mappings | Must | Confidence in [0.0, 1.0]; threshold configurable |
| FR-3.5 | Low-confidence mappings SHALL be flagged for potential human review | Should | Configurable escalation threshold (default: 0.6) |
| FR-3.6 | The system SHALL support ontology version pinning | Must | BFO version specified in configuration |

#### BFO Category Mapping Table

| BFO Category | Expected Claim Role | Requirement | Examples |
|--------------|---------------------|-------------|----------|
| Material Entity | Agent / Patient | Must be a spatially extended object | person, organization, artifact |
| Object Aggregate | Agent / Patient | Collection of material entities | committee, fleet, population |
| Process | Action / Relation | Must have temporal beginning and end | meeting, election, combustion |
| Process Boundary | Action (instantaneous) | Temporal instant | collision, decision point |
| Disposition | Relation | Describes tendency or potential | fragility, solubility, eligibility |
| Quality | Attribute | Dependent on bearer | color, temperature, age |
| Temporal Region | Context | Defines "when" | Tuesday, Q3 2024, the Renaissance |
| Spatial Region | Context | Defines "where" | the conference room, North America |
| Generically Dependent Continuant | Patient (informational) | Patterns that can be copied | the policy, the algorithm, the law |

#### Category Error Detection (FR-3.2 Detail)

| Error Type | Pattern | Response |
|------------|---------|----------|
| Abstract Agent | Agent maps to Quality or GDC, not Material Entity | ERR_AGENT_ABSTRACT |
| Process as Entity | Patient is a Process treated as Material Entity | ERR_CATEGORY_MISMATCH |
| Quality as Agent | Quality (e.g., "redness") in Agent role | ERR_QUALITY_AGENT |
| Temporal as Patient | Temporal region treated as affected entity | ERR_TEMPORAL_PATIENT |

**Mapping Confidence Calculation:**

```
mapping_confidence = weighted_average(
    lexical_match_score * 0.3,      # Direct term matching to ontology labels
    embedding_similarity * 0.3,     # Semantic similarity to category exemplars
    syntactic_role_fit * 0.2,       # Compatibility of syntactic role with category
    context_coherence * 0.2         # Consistency with other mapped elements
)
```

#### Ontology Configuration (NFR-3 Support)

The OGM implements an abstraction layer to support ontology modularity:

```yaml
ontology_config:
  primary_ontology: "BFO-2020"
  version: "2020-07-21"
  extensions:
    - "CCO-1.5"
    - "domain-specific-ontology.owl"
  
  category_interface:
    # Abstract categories mapped to ontology-specific terms
    SPATIALLY_EXTENDED_ENTITY:
      bfo: "material entity"
      dolce: "physical-object"
    PROCESS:
      bfo: "process"
      dolce: "event"
    TEMPORAL_REGION:
      bfo: "temporal region"
      dolce: "temporal-location"
```

**Scope Clarification:** Full ontology swappability (BFO → DOLCE) requires adapter implementation. NFR-3 guarantees interface stability; adapters for non-BFO ontologies are roadmap items.

### 5.4 Module 4: Constraint & Sufficiency Validation (CSV)

#### Core Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-4.1 | The system SHALL apply a Sufficiency Gate to every grounded claim | Must | All claims evaluated; pass/fail/partial status assigned |
| FR-4.2 | Causal claims SHALL require process-level grounding and temporal sequence | Must | Both A and B grounded as Process; temporal order established |
| FR-4.3 | Validation failures MUST be tagged with specific codes | Must | See Failure Taxonomy below |
| FR-4.4 | The system SHALL detect and flag scope ambiguities | Must | Universal/existential quantification; temporal boundaries |
| FR-4.5 | Partial validation SHALL be supported with explicit gap enumeration | Should | Partial pass lists satisfied constraints and remaining gaps |
| FR-4.6 | The system SHALL support configurable mechanism plausibility validation | Should | Domain ontology linkage for causal pathway verification |

#### Sufficiency Gate Definitions

| Gate | Condition | Failure Code |
|------|-----------|--------------|
| Agent Presence | Material Entity or Object Aggregate in Agent role (unless agent-less type) | ERR_AGENT_MISSING |
| Temporal Grounding | Process claims have temporal region specified or inferable | ERR_TEMPORAL_UNGROUNDED |
| Scope Definition | Quantification explicit or default applied | ERR_SCOPE_VAGUE |
| Causal Chain | Causal claims have process-process link with temporal sequence | ERR_CAUSAL_GAP |
| Referent Resolution | Pronouns and definite descriptions resolved to entities | ERR_REFERENT_AMBIGUOUS |
| Mechanism Plausibility | (Optional) Causal pathway linked to domain ontology process | ERR_MECHANISM_UNVERIFIED |

#### Causal Claim Validation (FR-4.2 Detail)

A causal claim "A caused B" requires:

1. **Process Grounding:** Both A and B must map to BFO Process or Process Boundary
2. **Temporal Sequence:** A must temporally precede or coincide with B
3. **Spatial Compatibility:** A and B must be spatially compatible (co-located or within causal reach)
4. **Mechanism Plausibility:** (Optional, configurable) Causal pathway should be ontologically coherent

**Temporal Sequence Detection:**

| Pattern | Detection Method | Confidence |
|---------|------------------|------------|
| Explicit markers | "before," "after," "then," "subsequently" | High |
| Tense sequence | Past perfect → simple past | Medium |
| Discourse order | Narrative sequence assumption | Low (flagged) |
| Simultaneous | "while," "during," "as" | Requires co-occurrence validation |

#### Mechanism Plausibility Specification (FR-4.6 Detail)

When `causal_mechanism_check` is enabled, the system validates that the causal pathway between Process A and Process B is ontologically coherent. This is accomplished through domain ontology linkage.

**Definition of Mechanism:**

A *mechanism* is a sequence of one or more intermediate processes, grounded in a domain-specific ontology, that connects the cause (Process A) to the effect (Process B) through recognized causal relations.

**Mechanism Validation Levels:**

| Level | Name | Requirements | Use Case |
|-------|------|--------------|----------|
| 0 | Disabled | No mechanism check | General-purpose processing |
| 1 | Type Compatibility | A and B belong to causally compatible process types | Default when enabled |
| 2 | Pathway Existence | At least one known pathway connects A-type to B-type in domain ontology | Scientific/technical claims |
| 3 | Full Pathway Grounding | All intermediate processes in pathway are explicitly or inferentially present | High-assurance domains |

**Domain Ontology Integration:**

The mechanism plausibility checker queries registered domain ontologies for causal pathway information:

| Domain | Ontology | Example Pathway |
|--------|----------|-----------------|
| Biomedical | Gene Ontology (GO), Human Disease Ontology (DOID) | gene_expression → protein_synthesis → metabolic_process |
| Legal | Legal Knowledge Graph (LKG) | legislative_action → statutory_enactment → legal_obligation |
| Financial | Financial Industry Business Ontology (FIBO) | transaction_execution → settlement_process → ownership_transfer |
| Manufacturing | Manufacturing Service Description Language (MSDL) | machining_process → material_removal → dimensional_change |
| General | CCO Act of Causing | act_of_causing → process_initiation → process_completion |

**Mechanism Validation Algorithm:**

```
function validate_mechanism(process_a, process_b, level, domain_ontologies):
    if level == 0:
        return PASS  # Mechanism check disabled
    
    type_a = get_process_type(process_a)
    type_b = get_process_type(process_b)
    
    # Level 1: Type Compatibility
    if not are_causally_compatible(type_a, type_b, domain_ontologies):
        return FAIL(ERR_MECHANISM_INCOMPATIBLE, 
                    "Process types {type_a} and {type_b} have no known causal relation")
    
    if level == 1:
        return PASS
    
    # Level 2: Pathway Existence
    pathways = find_causal_pathways(type_a, type_b, domain_ontologies)
    if pathways.empty():
        return FAIL(ERR_MECHANISM_NO_PATHWAY,
                    "No known causal pathway from {type_a} to {type_b}")
    
    if level == 2:
        return PASS_WITH_ANNOTATION(pathways)
    
    # Level 3: Full Pathway Grounding
    for pathway in pathways:
        grounding_result = ground_intermediate_processes(pathway, claim_context)
        if grounding_result.complete:
            return PASS_WITH_GROUNDED_PATHWAY(grounding_result)
    
    return PARTIAL(ERR_MECHANISM_PARTIAL,
                   "Pathway exists but intermediate processes not grounded",
                   candidate_pathways=pathways)
```

**Mechanism Validation Output Schema:**

```json
{
  "mechanism_validation": {
    "level": 2,
    "status": "PASS",
    "cause_process": {
      "extracted": "the drug was administered",
      "type": "GO:0042493",
      "label": "drug metabolic process"
    },
    "effect_process": {
      "extracted": "symptoms subsided",
      "type": "DOID:0001816",
      "label": "disease remission"
    },
    "pathway": {
      "ontology": "GO",
      "intermediate_types": [
        "GO:0017144 (drug catabolic process)",
        "GO:0009056 (cellular metabolic process)",
        "GO:0050896 (response to stimulus)"
      ],
      "pathway_confidence": 0.78,
      "source": "GO-CAM:5f8e9a7b"
    }
  }
}
```

**Configuration:**

```yaml
causal_validation:
  mechanism_check_enabled: true
  mechanism_level: 2  # 0=disabled, 1=type_compat, 2=pathway_exists, 3=full_grounding
  domain_ontologies:
    - id: "GO"
      path: "/ontologies/go.owl"
      causal_relations: ["RO:0002411", "RO:0002304"]  # causally upstream of, causally related to
    - id: "FIBO"
      path: "/ontologies/fibo.owl"
      causal_relations: ["fibo:causes", "fibo:enables"]
  fallback_ontology: "CCO"
  unknown_domain_behavior: "WARN"  # WARN | FAIL | SKIP
```

#### Failure Taxonomy (FR-4.3 Detail)

| Code | Description | Gap Analysis Template |
|------|-------------|----------------------|
| ERR_AGENT_MISSING | No material entity found as agent | "Specify who or what performed the action" |
| ERR_AGENT_ABSTRACT | Agent is an abstraction rather than material entity | "Replace abstract agent with concrete entity" |
| ERR_SCOPE_VAGUE | Claim lacks quantification or temporal boundaries | "Specify: all/some/most? Always/sometimes/once?" |
| ERR_CAUSAL_GAP | Causal link lacks process-level grounding | "Identify the mechanism: how did A lead to B?" |
| ERR_TEMPORAL_UNGROUNDED | Process lacks temporal specification | "When did this occur? Provide timeframe" |
| ERR_REFERENT_AMBIGUOUS | Pronoun or definite description unresolved | "Clarify: who/what does '[term]' refer to?" |
| ERR_ONT_MAP | Element cannot be mapped to ontology category | "Term '[term]' is too vague or ambiguous for classification" |
| ERR_CATEGORY_MISMATCH | Semantic role incompatible with ontological category | "A [category] cannot serve as [role]" |
| ERR_MECHANISM_INCOMPATIBLE | Cause and effect process types have no known causal relation | "Process types are not causally related in domain ontology" |
| ERR_MECHANISM_NO_PATHWAY | No causal pathway found between process types | "No known mechanism connects these processes" |
| ERR_MECHANISM_PARTIAL | Pathway exists but intermediate steps not grounded | "Intermediate processes in causal chain not specified" |

### 5.5 Module 5: Normative Annotation Module (NAM)

#### Core Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-5.1 | The system SHALL isolate Evaluative terms from Descriptive content | Must | Evaluative lexicon applied; separation ≥ 90% accurate |
| FR-5.2 | Evaluative terms SHALL be stored as metadata overlays | Must | Underlying triple unmodified by normative content |
| FR-5.3 | The system SHALL support multiple conflicting normative annotations | Must | Same claim can host Framework A: X, Framework B: Y |
| FR-5.4 | The system SHALL preserve evaluative provenance | Should | Which framework/source asserted each evaluation |
| FR-5.5 | The system SHALL detect mixed claims (descriptive + evaluative) | Must | Mixed claims tagged; evaluative portion isolated |

#### Evaluative Term Categories

| Category | Examples | Handling |
|----------|----------|----------|
| Moral | good, evil, just, unjust, right, wrong | Tag + Framework attribution |
| Aesthetic | beautiful, ugly, elegant, crude | Tag + Framework attribution |
| Epistemic | rational, irrational, justified, unfounded | Tag + note epistemic scope |
| Practical | useful, useless, efficient, wasteful | Tag + context dependence noted |
| Social | fair, unfair, appropriate, inappropriate | Tag + Framework attribution |

#### Normative Overlay Schema

```json
{
  "claim_id": "uuid",
  "descriptive_triple": {
    "agent": "...",
    "action": "...",
    "patient": "..."
  },
  "normative_overlays": [
    {
      "framework_id": "utilitarian-v1",
      "evaluation": "positive",
      "evaluative_terms": ["beneficial", "productive"],
      "confidence": 0.75,
      "source": "automated_lexicon"
    },
    {
      "framework_id": "deontological-v1",
      "evaluation": "negative",
      "evaluative_terms": ["rights-violating"],
      "confidence": 0.65,
      "source": "human_annotation"
    }
  ],
  "mixed_claim_flag": true,
  "original_evaluative_content": "...the beneficial but rights-violating policy..."
}
```

---

## 6. Non-Functional Requirements

### 6.1 Determinism & Reproducibility

| ID | Requirement | Specification |
|----|-------------|---------------|
| NFR-1.1 | Rule-based components SHALL produce bit-identical outputs | Hash verification on test suite |
| NFR-1.2 | ML components SHALL produce functionally equivalent outputs | Semantic equivalence within defined tolerance |
| NFR-1.3 | LLM components (if used) SHALL use pinned model versions | Model identifier and hash recorded |
| NFR-1.4 | LLM components SHALL use deterministic inference settings | temperature=0, seed fixed, top_k=1 |
| NFR-1.5 | Output variation tolerance SHALL be configurable | Default: exact match for structured fields; fuzzy match for confidence scores (±0.05) |

**Determinism Verification Protocol:**

```
For each test case in regression suite:
    output_1 = process(input, config)
    output_2 = process(input, config)
    
    assert structured_fields(output_1) == structured_fields(output_2)
    assert |confidence(output_1) - confidence(output_2)| <= tolerance
    
    if using_llm_components:
        log_model_version()
        assert semantic_equivalence(output_1.text, output_2.text)
```

### 6.2 Explainability

| ID | Requirement | Specification |
|----|-------------|---------------|
| NFR-2.1 | Every rejection SHALL cite the specific FR that triggered the gate | FR identifier in failure report |
| NFR-2.2 | Transformation decisions SHALL be logged with rationale | Decision log accessible via API |
| NFR-2.3 | Confidence scores SHALL be decomposable into component factors | Factor breakdown available on request |
| NFR-2.4 | Human-readable explanations SHALL be generatable for all failures | Natural language gap analysis |

### 6.3 Modularity

| ID | Requirement | Specification |
|----|-------------|---------------|
| NFR-3.1 | The OGM SHALL implement a category abstraction interface | See Section 5.3 Ontology Configuration |
| NFR-3.2 | BFO-family ontologies SHALL be swappable without core rewrite | Adapter pattern; shared interface |
| NFR-3.3 | Non-BFO ontologies SHALL be supportable via adapter implementation | Adapter specification documented |
| NFR-3.4 | Module boundaries SHALL enforce interface contracts | Schema validation at each I-xx interface |

### 6.4 Performance

| ID | Requirement | Specification |
|----|-------------|---------------|
| NFR-4.1 | Single CCU processing latency | ≤ 500ms p95 (rule-based); ≤ 2s p95 (with LLM) |
| NFR-4.2 | Throughput (batch mode) | ≥ 100 CCUs/minute (rule-based); ≥ 20 CCUs/minute (with LLM) |
| NFR-4.3 | Memory consumption per CCU | ≤ 50 MB peak |
| NFR-4.4 | Concurrent processing support | Configurable worker pool; default 4 workers |
| NFR-4.5 | Cold start time | ≤ 30 seconds to first CCU processed |

### 6.5 Reliability

| ID | Requirement | Specification |
|----|-------------|---------------|
| NFR-5.1 | Component failure isolation | Single module failure SHALL NOT crash pipeline |
| NFR-5.2 | Graceful degradation | If OGM unavailable, CET outputs raw extractions with warning |
| NFR-5.3 | Retry policy | Transient failures retry 3x with exponential backoff |
| NFR-5.4 | Circuit breaker | After 5 consecutive failures, module enters degraded mode |
| NFR-5.5 | Health check endpoint | /health returns component status |

### 6.6 Observability

| ID | Requirement | Specification |
|----|-------------|---------------|
| NFR-6.1 | Structured logging | JSON logs with correlation IDs |
| NFR-6.2 | Metrics export | Prometheus-compatible metrics endpoint |
| NFR-6.3 | Distributed tracing | OpenTelemetry spans for cross-module tracing |
| NFR-6.4 | Audit trail | Immutable log of all processing decisions |

---

## 7. API & Integration Specifications

### 7.1 REST API Endpoints

#### Process Claim

```
POST /v1/claims/process
Content-Type: application/json

Request:
{
  "artifact": {
    "content": "string (required)",
    "format": "text | markdown | html | json",
    "metadata": { ... }  // See Input Metadata Schema
  },
  "config": {
    "confidence_threshold": 0.6,
    "enable_llm_components": true,
    "ontology_version": "BFO-2020",
    "normative_frameworks": ["utilitarian-v1", "deontological-v1"],
    "causal_mechanism_level": 2
  },
  "options": {
    "include_provenance": true,
    "include_confidence_breakdown": false,
    "return_failures_only": false
  }
}

Response:
{
  "artifact_id": "uuid",
  "processing_timestamp": "ISO 8601",
  "results": [
    {
      "ccu_id": "uuid",
      "status": "GROUNDED | PARTIAL | FAILED",
      "claim_graph": { ... },  // If GROUNDED or PARTIAL
      "failure_report": { ... },  // If FAILED or PARTIAL
      "confidence": 0.85,
      "provenance": { ... }
    }
  ],
  "summary": {
    "total_ccus": 10,
    "grounded": 6,
    "partial": 2,
    "failed": 2
  }
}
```

#### Retrieve Artifact

```
GET /v1/artifacts/{artifact_id}

Response:
{
  "artifact_id": "uuid",
  "raw_content": "string",
  "ccus": [ ... ],
  "processing_history": [ ... ]
}
```

#### Health Check

```
GET /v1/health

Response:
{
  "status": "healthy | degraded | unhealthy",
  "components": {
    "lai": { "status": "healthy", "latency_ms": 12 },
    "cet": { "status": "healthy", "latency_ms": 45 },
    "ogm": { "status": "degraded", "error": "ontology service timeout" },
    "csv": { "status": "healthy", "latency_ms": 23 },
    "nam": { "status": "healthy", "latency_ms": 18 }
  },
  "version": "2.1.1"
}
```

### 7.2 Batch Processing Interface

```
POST /v1/claims/batch
Content-Type: application/json

Request:
{
  "artifacts": [ ... ],  // Array of artifact objects
  "config": { ... },
  "callback_url": "https://...",  // Optional webhook for completion
  "priority": "normal | high"
}

Response:
{
  "batch_id": "uuid",
  "status": "queued",
  "estimated_completion": "ISO 8601",
  "status_url": "/v1/batches/{batch_id}/status"
}
```

### 7.3 Streaming Interface

For document-level processing with cross-reference resolution:

```
WebSocket: wss://api.eccps.example/v1/stream

Client → Server:
{
  "type": "start_document",
  "document_id": "uuid",
  "config": { ... }
}

{
  "type": "ccu",
  "content": "...",
  "position": 0
}

Server → Client:
{
  "type": "ccu_result",
  "ccu_id": "uuid",
  "status": "GROUNDED",
  "claim_graph": { ... }
}

{
  "type": "cross_reference_resolved",
  "source_ccu": "uuid",
  "target_ccu": "uuid",
  "reference_type": "anaphora"
}
```

---

## 8. Output Specifications

### 8.1 Validated Claim Graph

```json
{
  "@context": {
    "bfo": "http://purl.obolibrary.org/obo/",
    "eccps": "http://eccps.example/ontology/",
    "prov": "http://www.w3.org/ns/prov#"
  },
  "@type": "eccps:ValidatedClaim",
  "@id": "urn:eccps:claim:uuid",
  
  "eccps:extractedFrom": {
    "@type": "eccps:CCU",
    "eccps:sourceArtifact": "urn:eccps:artifact:uuid",
    "eccps:characterOffset": [145, 287],
    "eccps:rawText": "The committee voted unanimously to approve the proposal on Tuesday."
  },
  
  "eccps:semanticStructure": {
    "eccps:agent": {
      "@type": "bfo:ObjectAggregate",
      "rdfs:label": "the committee",
      "eccps:offset": [0, 13],
      "eccps:groundingConfidence": 0.92
    },
    "eccps:action": {
      "@type": "bfo:Process",
      "rdfs:label": "voted to approve",
      "eccps:offset": [14, 36],
      "eccps:groundingConfidence": 0.88
    },
    "eccps:patient": {
      "@type": "bfo:GenericallyDependentContinuant",
      "rdfs:label": "the proposal",
      "eccps:offset": [37, 49],
      "eccps:groundingConfidence": 0.85
    },
    "eccps:temporal": {
      "@type": "bfo:TemporalRegion",
      "rdfs:label": "on Tuesday",
      "eccps:offset": [50, 60],
      "eccps:groundingConfidence": 0.95
    },
    "eccps:manner": {
      "rdfs:label": "unanimously",
      "eccps:offset": [14, 25]
    }
  },
  
  "eccps:epistemicModality": "MOD_UNMARKED",
  "eccps:rhetoricalStatus": "ST_LITERAL",
  
  "eccps:validationStatus": {
    "eccps:status": "GROUNDED",
    "eccps:overallConfidence": 0.89,
    "eccps:gatesPassed": ["AGENT_PRESENCE", "TEMPORAL_GROUNDING", "SCOPE_DEFINITION"],
    "eccps:validatedAt": "2026-01-12T14:30:00Z"
  },
  
  "eccps:normativeOverlays": [],
  
  "prov:wasGeneratedBy": {
    "@type": "prov:Activity",
    "prov:used": "eccps:Pipeline-v2.1.1",
    "prov:endedAtTime": "2026-01-12T14:30:00Z"
  }
}
```

### 8.2 Structured Failure Report

```json
{
  "@type": "eccps:FailureReport",
  "@id": "urn:eccps:failure:uuid",
  
  "eccps:targetCCU": {
    "eccps:id": "urn:eccps:ccu:uuid",
    "eccps:rawText": "Innovation drives success.",
    "eccps:characterOffset": [0, 26]
  },
  
  "eccps:failureCode": "ERR_AGENT_ABSTRACT",
  "eccps:triggeringRequirement": "FR-3.2",
  "eccps:failingModule": "OGM",
  
  "eccps:diagnostics": {
    "eccps:extractedAgent": "innovation",
    "eccps:attemptedMapping": "bfo:Quality",
    "eccps:mappingConfidence": 0.72,
    "eccps:expectedCategory": ["bfo:MaterialEntity", "bfo:ObjectAggregate"],
    "eccps:categoryMismatchReason": "Abstract concept cannot initiate causal processes"
  },
  
  "eccps:gapAnalysis": {
    "eccps:missingInformation": [
      "Concrete agent performing innovative action",
      "Specific process or activity being described"
    ],
    "eccps:suggestedClarification": "Who or what organization is innovating? What specific action constitutes this innovation?",
    "eccps:exampleResolution": "Acme Corp's R&D team developed a new manufacturing process."
  },
  
  "eccps:partialResults": {
    "eccps:action": {
      "rdfs:label": "drives",
      "@type": "bfo:Process",
      "eccps:groundingConfidence": 0.65
    },
    "eccps:patient": {
      "rdfs:label": "success",
      "@type": "bfo:Quality",
      "eccps:note": "Also abstract; would require grounding"
    }
  },
  
  "eccps:resolutionPathway": {
    "eccps:minimumRequired": ["Concrete agent specification"],
    "eccps:recommended": ["Concrete agent", "Specific process", "Temporal grounding"],
    "eccps:retryEndpoint": "/v1/claims/retry/{failure_id}"
  }
}
```

### 8.3 Grounding Result Envelope

```json
{
  "ccu_id": "uuid",
  "status": "GROUNDED | PARTIAL | FAILED",
  "confidence": {
    "overall": 0.82,
    "breakdown": {
      "extraction_confidence": 0.88,
      "grounding_confidence": 0.79,
      "validation_confidence": 0.85
    }
  },
  "uncertainty_sources": [
    {
      "module": "OGM",
      "element": "patient",
      "reason": "Ambiguous between GDC and Quality",
      "impact": "moderate"
    }
  ],
  "claim_graph": { ... },  // Present if GROUNDED or PARTIAL
  "failure_report": { ... }  // Present if FAILED or PARTIAL
}
```

---

## 9. Configuration Schema

### 9.1 System Configuration

```yaml
eccps:
  version: "2.1.1"
  
  intake:
    max_artifact_size_bytes: 1048576  # 1 MB
    max_ccu_length: 2000
    min_ccu_length: 10
    context_window_sentences: 2
    supported_formats:
      - text
      - markdown
      - html
      - json
  
  extraction:
    nlp_backend: "spacy"  # spacy | stanza | custom
    model: "en_core_web_trf"
    use_llm_for_complex_extraction: true
    llm_config:
      provider: "local"  # local | anthropic | openai
      model_id: "llama-3.2-8b"
      model_hash: "sha256:abc123..."
      temperature: 0
      seed: 42
      top_k: 1
    rhetorical_confidence_threshold: 0.7
  
  grounding:
    ontology:
      primary: "BFO-2020"
      version: "2020-07-21"
      extensions:
        - "CCO-1.5"
      local_path: "/ontologies/"
    confidence_threshold: 0.6
    escalation_threshold: 0.5  # Below this, flag for human review
    category_interface_version: "1.0"
  
  validation:
    sufficiency_gates:
      - AGENT_PRESENCE
      - TEMPORAL_GROUNDING
      - SCOPE_DEFINITION
      - CAUSAL_CHAIN
      - REFERENT_RESOLUTION
    enable_partial_validation: true
    causal_mechanism_check: true
    causal_mechanism_level: 2  # 0=disabled, 1=type_compat, 2=pathway_exists, 3=full_grounding
  
  annotation:
    normative_frameworks:
      - id: "utilitarian-v1"
        lexicon_path: "/lexicons/utilitarian.json"
      - id: "deontological-v1"
        lexicon_path: "/lexicons/deontological.json"
    evaluative_lexicon: "/lexicons/evaluative_terms.json"
  
  performance:
    worker_count: 4
    batch_size: 50
    timeout_ms: 5000
    retry_count: 3
    retry_backoff_base_ms: 100
  
  observability:
    log_level: "INFO"
    log_format: "json"
    metrics_enabled: true
    metrics_port: 9090
    tracing_enabled: true
    tracing_endpoint: "http://jaeger:14268/api/traces"
```

### 9.2 Tunable Parameters

| Parameter | Default | Range | Impact |
|-----------|---------|-------|--------|
| confidence_threshold | 0.6 | 0.0-1.0 | Higher = stricter grounding; more failures |
| rhetorical_confidence_threshold | 0.7 | 0.0-1.0 | Higher = fewer rhetorical tags; more literal interpretation |
| escalation_threshold | 0.5 | 0.0-1.0 | Below this, flag for human review |
| context_window_sentences | 2 | 0-5 | More context = better resolution; higher memory |
| enable_partial_validation | true | boolean | If false, partial = failed |
| causal_mechanism_check | false | boolean | If true, stricter causal validation |
| causal_mechanism_level | 2 | 0-3 | Higher = stricter mechanism verification |

---

## 10. Failure-to-Resolution Pathway

### 10.1 Resolution Workflow

```
┌─────────────────┐
│ Failure Report  │
│   Generated     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gap Analysis   │
│   Structured    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│   Automated     │────▶│   Resolution    │
│   Resolution?   │ No  │   Prompt Gen    │
└────────┬────────┘     └────────┬────────┘
         │ Yes                   │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  Apply Default  │     │  Human/Agent    │
│   Resolution    │     │    Provides     │
└────────┬────────┘     │  Clarification  │
         │              └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────┐
│            Retry Processing             │
│    POST /v1/claims/retry/{failure_id}   │
└─────────────────────────────────────────┘
```

### 10.2 Resolution Prompt Templates

| Failure Code | Prompt Template |
|--------------|-----------------|
| ERR_AGENT_MISSING | "The claim '{raw_text}' lacks a clear agent. Who or what performed the action '{action}'?" |
| ERR_AGENT_ABSTRACT | "'{agent}' is an abstract concept. Which specific person, organization, or entity is meant?" |
| ERR_SCOPE_VAGUE | "The claim '{raw_text}' is ambiguous in scope. Does this apply to all {patient}, some {patient}, or a specific instance?" |
| ERR_CAUSAL_GAP | "The claim asserts that '{agent}' caused '{patient}'. What is the mechanism or process connecting them?" |
| ERR_TEMPORAL_UNGROUNDED | "When did '{action}' occur? Please specify a date, time period, or relative temporal reference." |
| ERR_MECHANISM_INCOMPATIBLE | "The claimed causal relation between '{process_a}' and '{process_b}' is not recognized. Please specify the causal pathway." |
| ERR_MECHANISM_NO_PATHWAY | "No known mechanism connects '{process_a}' to '{process_b}'. Please describe the intermediate steps or processes." |

### 10.3 Retry API

```
POST /v1/claims/retry/{failure_id}
Content-Type: application/json

Request:
{
  "clarifications": {
    "agent": "Acme Corporation's board of directors",
    "temporal": "Q4 2025"
  },
  "additional_context": "This refers to the merger announcement from their press release.",
  "source": "human_clarification"  // human_clarification | automated_resolution | llm_inference
}

Response:
{
  "original_failure_id": "uuid",
  "retry_result": {
    "status": "GROUNDED",
    "claim_graph": { ... },
    "resolution_applied": {
      "agent": "Acme Corporation's board of directors",
      "temporal": "Q4 2025"
    }
  }
}
```

### 10.4 Feedback Loop

Resolved failures contribute to system improvement:

1. **Successful resolutions** are logged with the clarification provided
2. **Pattern detection** identifies recurring failure types
3. **Lexicon updates** incorporate new terms from successful groundings
4. **Model fine-tuning** (if applicable) uses resolved cases as training signal

---

## 11. Processing Modes

### 11.1 Atomic Mode (Default)

Each CCU is processed independently. Cross-references ("as mentioned above") are flagged but not resolved.

**Use case:** High-throughput processing; claims that are self-contained.

### 11.2 Document Mode

The system maintains document-level context for cross-reference resolution.

**Capabilities:**
- Anaphora resolution ("it," "they," "this policy")
- Cataphora handling ("The following proposal...")
- Section reference resolution ("As stated in Section 3...")

#### State Persistence Architecture

Document mode introduces stateful processing. The system maintains document context across CCUs through a dedicated state persistence layer.

**State Components:**

| Component | Content | Lifecycle |
|-----------|---------|-----------|
| Entity Registry | Resolved entities with aliases and coreference chains | Document duration |
| Section Index | Document structure with heading hierarchy | Document duration |
| Anaphora Stack | Recently mentioned entities for pronoun resolution | Rolling window (configurable) |
| Grounded Claims Cache | Previously processed CCUs and their grounding results | Document duration |
| Cross-Reference Queue | Pending references awaiting resolution | Until resolved or document end |

**Persistence Options:**

| Option | Technology | Use Case | Latency | Durability |
|--------|------------|----------|---------|------------|
| In-Memory | Local HashMap | Short documents (<100 CCUs) | <1ms | None (process-bound) |
| Redis | Redis 7.x with RedisJSON | Medium documents, distributed processing | 1-5ms | Configurable (RDB/AOF) |
| Graph DB | Neo4j / Amazon Neptune | Large documents, complex cross-references | 5-20ms | Full persistence |
| Hybrid | Redis + Graph DB | Production systems | 1-5ms (hot) / 5-20ms (cold) | Full persistence |

**State Schema (Redis Implementation):**

```
# Document session key structure
eccps:doc:{document_id}:meta          # Document metadata (JSON)
eccps:doc:{document_id}:entities      # Entity registry (JSON)
eccps:doc:{document_id}:sections      # Section index (JSON)
eccps:doc:{document_id}:anaphora      # Anaphora stack (List)
eccps:doc:{document_id}:claims        # Grounded claims cache (Hash)
eccps:doc:{document_id}:pending       # Cross-reference queue (Sorted Set)

# TTL: Configurable, default 1 hour after last access
```

**Entity Registry Schema:**

```json
{
  "document_id": "uuid",
  "entities": [
    {
      "entity_id": "ent_001",
      "canonical_form": "Acme Corporation",
      "aliases": ["Acme", "the company", "it", "they"],
      "type": "bfo:ObjectAggregate",
      "first_mention": {
        "ccu_id": "uuid",
        "offset": [0, 16]
      },
      "coreference_chain": ["ccu_001:0-16", "ccu_003:45-47", "ccu_007:0-11"]
    }
  ],
  "last_updated": "ISO 8601"
}
```

**Cross-Reference Resolution Flow:**

```
┌─────────────────┐
│   New CCU       │
│   Received      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Check for      │
│  Anaphora       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────────────┐
│ None  │ │ Anaphora      │
│ Found │ │ Detected      │
└───┬───┘ └───────┬───────┘
    │             │
    │             ▼
    │     ┌───────────────┐
    │     │ Query Entity  │
    │     │ Registry      │
    │     └───────┬───────┘
    │             │
    │        ┌────┴────┐
    │        │         │
    │        ▼         ▼
    │    ┌───────┐ ┌───────────┐
    │    │Resolved│ │Unresolved │
    │    └───┬───┘ └─────┬─────┘
    │        │           │
    │        │           ▼
    │        │   ┌───────────────┐
    │        │   │ Add to        │
    │        │   │ Pending Queue │
    │        │   └───────────────┘
    │        │
    └────────┴───────────┐
                         │
                         ▼
              ┌─────────────────┐
              │ Continue        │
              │ Processing      │
              └─────────────────┘
```

**Configuration:**

```yaml
document_mode:
  enabled: true
  state_persistence:
    backend: "redis"  # inmemory | redis | neo4j | hybrid
    redis:
      host: "localhost"
      port: 6379
      db: 0
      password_secret: "redis-password"
      ssl: true
      connection_pool_size: 10
    neo4j:
      uri: "bolt://localhost:7687"
      user: "neo4j"
      password_secret: "neo4j-password"
  
  session:
    ttl_seconds: 3600  # 1 hour
    max_entities_per_document: 10000
    anaphora_window_size: 5  # CCUs to consider for pronoun resolution
  
  coreference:
    model: "spanbert-coref"
    confidence_threshold: 0.7
    allow_cataphora: true
  
  section_tracking:
    enabled: true
    heading_detection: "rule_based"  # rule_based | ml_based
```

**Scaling Considerations:**

| Document Size | Recommended Backend | Worker Allocation | Memory Budget |
|---------------|--------------------|--------------------|---------------|
| Small (<50 CCUs) | In-Memory | Single worker | 256 MB |
| Medium (50-500 CCUs) | Redis | 2-4 workers | 1 GB |
| Large (500-5000 CCUs) | Redis + Graph DB | 4-8 workers | 4 GB |
| Very Large (>5000 CCUs) | Distributed Graph DB | Horizontal scaling | Cluster-dependent |

**Cleanup and Garbage Collection:**

```yaml
state_cleanup:
  strategy: "ttl_with_explicit"  # ttl_only | explicit_only | ttl_with_explicit
  orphan_detection_interval_seconds: 300
  force_cleanup_threshold_mb: 1024  # Trigger cleanup if state exceeds this
```

### 11.3 Conversational Mode

For processing dialogue or multi-turn exchanges where speaker attribution matters.

**Capabilities:**
- Speaker tracking
- Turn-taking analysis
- Claim attribution to speakers

---

## 12. Acceptance Criteria Summary

### 12.1 Module Acceptance Criteria

| Module | Criterion | Measurement |
|--------|-----------|-------------|
| LAI | CCU segmentation accuracy | ≥ 95% on benchmark corpus |
| LAI | UAID uniqueness | Zero collisions in 10M artifacts |
| CET | Triple extraction F1 | ≥ 0.80 on semantic role labeling benchmark |
| CET | Provenance accuracy | 100% offset validity (reconstructable) |
| OGM | BFO mapping accuracy | ≥ 80% on manually annotated test set |
| OGM | Category error detection | ≥ 90% precision, ≥ 85% recall |
| CSV | Sufficiency gate accuracy | ≥ 95% agreement with human judgment |
| CSV | Mechanism validation accuracy | ≥ 85% on domain-specific test set |
| NAM | Evaluative term isolation | ≥ 90% precision, ≥ 85% recall |

### 12.2 System-Level Acceptance Criteria

| Criterion | Target | Verification Method |
|-----------|--------|---------------------|
| End-to-end latency (rule-based) | p95 ≤ 500ms per CCU | Load testing |
| End-to-end latency (with LLM) | p95 ≤ 2s per CCU | Load testing |
| Throughput | ≥ 100 CCUs/min (rule-based) | Sustained load test |
| Determinism | 100% for rule-based; semantic equiv for LLM | Regression suite |
| Failure report completeness | 100% include FR citation and gap analysis | Audit |
| Uptime | 99.5% availability | Monitoring |
| Document mode state consistency | Zero data loss on worker failure | Chaos testing |

---

## 13. Glossary

| Term | Definition |
|------|------------|
| **BFO** | Basic Formal Ontology; a top-level realist ontology |
| **CCO** | Common Core Ontologies; mid-level extension of BFO |
| **CCU** | Candidate Claim Unit; a segmented text unit for processing |
| **Epistemic Friction** | Design principle that resists easy/ambiguous interpretations |
| **GDC** | Generically Dependent Continuant; BFO category for information entities |
| **Grounding** | The process of mapping linguistic elements to ontological categories |
| **Mechanism** | A sequence of intermediate processes connecting cause to effect |
| **UAID** | Unique Artifact ID; identifier for input documents |

---

## 14. Appendices

### Appendix A: BFO 2020 Category Hierarchy (Relevant Subset)

```
Entity
├── Continuant
│   ├── Independent Continuant
│   │   ├── Material Entity
│   │   │   ├── Object
│   │   │   ├── Object Aggregate
│   │   │   └── Fiat Object Part
│   │   └── Immaterial Entity
│   │       └── Spatial Region
│   └── Dependent Continuant
│       ├── Generically Dependent Continuant
│       └── Specifically Dependent Continuant
│           ├── Quality
│           └── Realizable Entity
│               ├── Disposition
│               └── Role
└── Occurrent
    ├── Process
    ├── Process Boundary
    └── Temporal Region
```

### Appendix B: Error Code Quick Reference

| Code | Module | Severity | Auto-Resolvable |
|------|--------|----------|-----------------|
| ERR_AGENT_MISSING | CSV | High | Sometimes (passive → active conversion) |
| ERR_AGENT_ABSTRACT | OGM | High | No |
| ERR_SCOPE_VAGUE | CSV | Medium | Sometimes (default quantification) |
| ERR_CAUSAL_GAP | CSV | High | No |
| ERR_TEMPORAL_UNGROUNDED | CSV | Medium | Sometimes (context inference) |
| ERR_REFERENT_AMBIGUOUS | CET | Medium | Sometimes (coreference resolution) |
| ERR_ONT_MAP | OGM | High | No |
| ERR_CATEGORY_MISMATCH | OGM | High | No |
| ERR_MECHANISM_INCOMPATIBLE | CSV | High | No |
| ERR_MECHANISM_NO_PATHWAY | CSV | High | No |
| ERR_MECHANISM_PARTIAL | CSV | Medium | Sometimes (context inference) |

### Appendix C: Sample Test Cases

**Test Case 1: Clean Grounding**
```
Input: "Acme Corporation acquired Beta Industries on March 15, 2025."
Expected: GROUNDED
Agent: Acme Corporation (ObjectAggregate)
Action: acquired (Process)
Patient: Beta Industries (ObjectAggregate)
Temporal: March 15, 2025 (TemporalRegion)
```

**Test Case 2: Abstract Agent Failure**
```
Input: "Innovation drives economic growth."
Expected: FAILED
Code: ERR_AGENT_ABSTRACT
Gap: "innovation" is Quality, not MaterialEntity
```

**Test Case 3: Partial Grounding**
```
Input: "The policy was implemented successfully."
Expected: PARTIAL
Grounded: action (implemented), manner (successfully)
Gap: ERR_AGENT_MISSING (passive voice, agent unspecified)
```

**Test Case 4: Mechanism Validation (Level 2)**
```
Input: "The antibiotic eliminated the infection."
Expected: GROUNDED (with mechanism annotation)
Mechanism Pathway: GO:0042493 → GO:0009056 → GO:0050896
```

**Test Case 5: Mechanism Failure**
```
Input: "The spreadsheet caused world peace."
Expected: FAILED
Code: ERR_MECHANISM_INCOMPATIBLE
Gap: No causal pathway between "data_processing" and "geopolitical_state"
```

### Appendix D: BFO-Mapping Reference Sheet for Common Claim-Actions

This reference sheet provides the 50 most common claim-actions (verbs) and their corresponding BFO/CCO class paths, along with mapping notes for the OGM module.

#### D.1 Process Categories Overview

| BFO/CCO Category | Description | Verb Characteristics |
|------------------|-------------|----------------------|
| **bfo:Process** | Generic occurrent with temporal extension | Default for most action verbs |
| **cco:ActOfCommunication** | Information transfer between agents | say, tell, inform, announce |
| **cco:ActOfArtifactProcessing** | Manipulation of artifacts | create, build, modify, repair |
| **cco:ActOfMeasuring** | Quantification activities | measure, count, evaluate, assess |
| **cco:ActOfAppraisal** | Judgment or evaluation | approve, reject, review, rate |
| **cco:ActOfTransfer** | Movement of entities or rights | give, sell, transfer, donate |
| **cco:ActOfAcquiring** | Obtaining entities or rights | buy, acquire, receive, obtain |

#### D.2 Verb-to-BFO/CCO Mapping Table

| # | Verb | Primary BFO/CCO Class | Secondary Class | Notes |
|---|------|----------------------|-----------------|-------|
| 1 | **create** | cco:ActOfArtifactProcessing | cco:ActOfCreating | Patient must be artifact or GDC |
| 2 | **destroy** | cco:ActOfArtifactProcessing | cco:ActOfDestroying | Patient ceases to exist |
| 3 | **modify** | cco:ActOfArtifactProcessing | cco:ActOfModifying | Patient persists with changed qualities |
| 4 | **build** | cco:ActOfArtifactProcessing | cco:ActOfAssembling | Patient is assembled artifact |
| 5 | **repair** | cco:ActOfArtifactProcessing | cco:ActOfRepairing | Patient returns to functional state |
| 6 | **inform** | cco:ActOfCommunication | cco:ActOfInforming | Requires agent and recipient |
| 7 | **announce** | cco:ActOfCommunication | cco:ActOfAnnouncing | Broadcast communication |
| 8 | **tell** | cco:ActOfCommunication | cco:ActOfInforming | Directed communication |
| 9 | **ask** | cco:ActOfCommunication | cco:ActOfRequesting | Information-seeking |
| 10 | **report** | cco:ActOfCommunication | cco:ActOfReporting | Formal information transfer |
| 11 | **approve** | cco:ActOfAppraisal | cco:ActOfApproving | Positive judgment |
| 12 | **reject** | cco:ActOfAppraisal | cco:ActOfRejecting | Negative judgment |
| 13 | **review** | cco:ActOfAppraisal | cco:ActOfReviewing | Evaluation without judgment |
| 14 | **assess** | cco:ActOfAppraisal | cco:ActOfAssessing | Formal evaluation |
| 15 | **evaluate** | cco:ActOfAppraisal | cco:ActOfEvaluating | General evaluation |
| 16 | **buy** | cco:ActOfAcquiring | cco:ActOfPurchasing | Commercial acquisition |
| 17 | **acquire** | cco:ActOfAcquiring | — | General acquisition |
| 18 | **receive** | cco:ActOfAcquiring | cco:ActOfReceiving | Passive acquisition |
| 19 | **obtain** | cco:ActOfAcquiring | — | General acquisition |
| 20 | **inherit** | cco:ActOfAcquiring | cco:ActOfInheriting | Legal/familial transfer |
| 21 | **sell** | cco:ActOfTransfer | cco:ActOfSelling | Commercial transfer |
| 22 | **give** | cco:ActOfTransfer | cco:ActOfGiving | Non-commercial transfer |
| 23 | **transfer** | cco:ActOfTransfer | — | General transfer |
| 24 | **donate** | cco:ActOfTransfer | cco:ActOfDonating | Charitable transfer |
| 25 | **send** | cco:ActOfTransfer | cco:ActOfSending | Spatial transfer |
| 26 | **measure** | cco:ActOfMeasuring | — | Quantification |
| 27 | **count** | cco:ActOfMeasuring | cco:ActOfCounting | Discrete quantification |
| 28 | **weigh** | cco:ActOfMeasuring | cco:ActOfWeighing | Mass measurement |
| 29 | **calculate** | cco:ActOfMeasuring | cco:ActOfCalculating | Derived measurement |
| 30 | **estimate** | cco:ActOfMeasuring | cco:ActOfEstimating | Approximate measurement |
| 31 | **decide** | bfo:ProcessBoundary | cco:ActOfDeciding | Instantaneous determination |
| 32 | **choose** | bfo:ProcessBoundary | cco:ActOfChoosing | Selection point |
| 33 | **agree** | bfo:ProcessBoundary | cco:ActOfAgreeing | Consensus point |
| 34 | **sign** | bfo:ProcessBoundary | cco:ActOfSigning | Documentary action |
| 35 | **vote** | bfo:ProcessBoundary | cco:ActOfVoting | Formal choice |
| 36 | **move** | bfo:Process | cco:ActOfLocomotion | Spatial translation |
| 37 | **transport** | bfo:Process | cco:ActOfTransporting | Agent-caused movement |
| 38 | **travel** | bfo:Process | cco:ActOfTraveling | Self-locomotion |
| 39 | **arrive** | bfo:ProcessBoundary | cco:ActOfArriving | End of travel |
| 40 | **depart** | bfo:ProcessBoundary | cco:ActOfDeparting | Start of travel |
| 41 | **start** | bfo:ProcessBoundary | — | Process initiation |
| 42 | **stop** | bfo:ProcessBoundary | — | Process termination |
| 43 | **begin** | bfo:ProcessBoundary | — | Process initiation (formal) |
| 44 | **end** | bfo:ProcessBoundary | — | Process termination (formal) |
| 45 | **continue** | bfo:Process | — | Process persistence |
| 46 | **cause** | bfo:Process | cco:ActOfCausing | Causal relation (requires mechanism) |
| 47 | **prevent** | bfo:Process | cco:ActOfPreventing | Counterfactual causal |
| 48 | **enable** | bfo:Process | cco:ActOfEnabling | Dispositional activation |
| 49 | **prohibit** | cco:ActOfCommunication | cco:ActOfProhibiting | Normative constraint |
| 50 | **require** | cco:ActOfCommunication | cco:ActOfRequiring | Normative obligation |

#### D.3 Special Handling Cases

**Stative Verbs (Non-Processes):**

These verbs do not map to bfo:Process and require special handling:

| Verb | Mapping | Handling |
|------|---------|----------|
| be | bfo:Quality (attribute assertion) | Extract as quality attribution |
| have | bfo:Quality or bfo:Role | Possession or role assignment |
| exist | bfo:MaterialEntity (assertion) | Existential claim |
| contain | bfo:SpatialRelation | Spatial containment |
| belong | bfo:Role | Role or ownership relation |

**Ambiguous Verbs (Context-Dependent):**

| Verb | Context A | Context B |
|------|-----------|-----------|
| run | ActOfLocomotion ("he ran") | ActOfOperating ("run the machine") |
| make | ActOfCreating ("make a cake") | ActOfCausing ("make him happy") |
| take | ActOfAcquiring ("take the book") | ActOfDuration ("take an hour") |
| get | ActOfAcquiring ("get a job") | ActOfBecoming ("get sick") |
| set | ActOfPositioning ("set the table") | ActOfConfiguring ("set the value") |

**Phrasal Verbs:**

| Phrasal Verb | Mapping | Note |
|--------------|---------|------|
| carry out | cco:ActOfExecuting | Process execution |
| bring about | cco:ActOfCausing | Causation |
| set up | cco:ActOfEstablishing | Initialization |
| break down | cco:ActOfDecomposing | Analysis or destruction |
| take over | cco:ActOfAcquiring | Control transfer |

#### D.4 Mapping Confidence Heuristics

| Condition | Confidence Modifier |
|-----------|-------------------|
| Verb appears in CCO lexicon exactly | +0.20 |
| Verb has single unambiguous mapping | +0.15 |
| Context matches expected semantic roles | +0.10 |
| Verb requires disambiguation | -0.15 |
| Verb is phrasal or idiomatic | -0.10 |
| Domain ontology provides specific mapping | +0.25 |

#### D.5 Implementation Notes

1. **Lexicon Priority:** Domain-specific ontologies override CCO mappings when domain is specified in input metadata.

2. **Disambiguation Strategy:** For ambiguous verbs, use semantic role pattern matching:
   - If Patient is artifact → prefer ActOfArtifactProcessing
   - If Patient is information → prefer ActOfCommunication
   - If Patient is agent → prefer ActOfInfluencing

3. **Nominalization Handling:** Noun forms of verbs (e.g., "creation," "approval") should be mapped to the same process class as the verb form.

4. **Negation Handling:** Negated verbs ("did not approve") retain their process mapping but receive a MOD_NEGATED epistemic tag.

5. **Tense Invariance:** Process mappings are tense-invariant; temporal grounding is handled separately in the Temporal Region slot.

---

## 15. Document Revision History

| Section | v2.1.1 Changes |
|---------|----------------|
| §5.4 | Added FR-4.6 for mechanism plausibility; full mechanism specification |
| §5.4 | Added ERR_MECHANISM_* error codes to failure taxonomy |
| §9.1 | Added causal_validation configuration block |
| §10.2 | Added mechanism-related resolution prompt templates |
| §11.2 | NEW: Complete state persistence architecture for document mode |
| §11.2 | Added Redis/Neo4j/Hybrid persistence options with schemas |
| §11.2 | Added entity registry, cross-reference resolution flow |
| §12.1 | Added CSV mechanism validation accuracy criterion |
| §12.2 | Added document mode state consistency criterion |
| App. B | Added mechanism-related error codes |
| App. C | Added mechanism validation test cases |
| App. D | NEW: BFO-Mapping Reference Sheet (50 common verbs) |

---

*End of Document*
