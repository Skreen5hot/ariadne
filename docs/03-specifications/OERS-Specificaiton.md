# Ontology-Aware Entity Resolution Service (OERS)

**Version**: 2.1.0  
**Status**: Approved for Development  
**Authors**: Aaron, Claude  
**Date**: 2026-01-27  
**Changelog**: v2.1 finalizes production specification—adds iterative re-blocking for super-clusters, temporal validity intervals, property-level trust overrides, confirms Union-Find for transitive closure

---

## Executive Summary

OERS is an ontology-aware service for identifying candidate co-references across knowledge graphs. Unlike traditional entity resolution systems that treat identity as a string-matching problem, OERS grounds identity in ontological commitments derived from the Basic Formal Ontology (BFO) and Common Core Ontologies (CCO).

### Core Value Proposition

By distinguishing ontological identity conditions from epistemic evidence, OERS produces principled, auditable, and explainable resolution candidates that respect the fundamental nature of the entities involved.

### Ecosystem Position

OERS operates as a **general-purpose entity resolution service** with optional integration points:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     OERS DEPLOYMENT MODES                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  MODE 1: Standalone Graph Resolution                                │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────────────┐ │
│  │ RDF Graphs  │─────▶│    OERS     │─────▶│ Hypothesis Sets     │ │
│  │ (any source)│      │             │      │ (for any consumer)  │ │
│  └─────────────┘      └─────────────┘      └─────────────────────┘ │
│                                                                     │
│  MODE 2: TagTeam + IEE Integration                                  │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐        │
│  │  TagTeam    │─────▶│    OERS     │─────▶│    IEE      │        │
│  │  (ICEs)     │      │  + Bridge   │      │ (Reasoning) │        │
│  └─────────────┘      └─────────────┘      └─────────────┘        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### What's New in v2.1

| Issue | Resolution |
|-------|------------|
| Super-Cluster Risk | Iterative re-blocking with adaptive thresholds |
| Temporal Granularity | Full validity interval structure for history |
| Trust Granularity | Property-level trust overrides per source |
| Algorithm Confirmation | Union-Find mandated for transitive closure |

### What Was Added in v2.0

| Issue | Resolution |
|-------|------------|
| Role Paradox | Dual-function SDC handling (evidence + entity) |
| Temporal Fuzziness | Configurable degradation when timestamps missing |
| Governance Bottleneck | Auto-promotion policies with quarantine rules |
| Canonicalization | Explicit attribute merging strategy |
| Entity Splits | Successor/predecessor modeling |
| Performance | Depth limits and timeout constraints |
| Trust Model | Evidence trust scoring for negations |

---

## 1. Foundational Principles

### 1.1 Normative Commitment: Referents, Not Representations

> **OERS never asserts identity between ICEs, records, or descriptions—only hypotheses about shared referents supported by evidence graphs.**

This commitment is foundational and non-negotiable. Information Content Entities (ICEs) are treated as *evidence* that real-world entities exist, not as the entities themselves.

**Terminological precision** (aligned with Style Guide v3.1):
- **Co-reference**: The relation that holds when two information artifacts denote the same particular
- **Numerical identity**: What OERS hypothesizes—two references pick out the same individual in reality
- **Denotation**: The relation between an ICE and the worldly entity it is about (constrained, not guaranteed)

### 1.2 Ontology as Constraint, Not Feature

The ontology serves as:
1. **Hard constraints**: Disjointness axioms making certain co-references impossible
2. **Identity conditions**: Category-specific criteria for numerical identity
3. **Structural priors**: Domain/range restrictions shaping candidate generation
4. **Temporal semantics**: Persistence conditions governing identity through time

### 1.3 Separation of Epistemic and Ontological Concerns

| Layer | Concern | Example |
|-------|---------|---------|
| **Ontological** | What *would* make two things numerically identical | Same biological organism |
| **Epistemic** | What *evidence* supports co-reference hypothesis | Matching SSN, similar name |

### 1.4 Hypothesis Lifecycle

OERS manages hypotheses through a defined lifecycle:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   CANDIDATE  │────▶│  HYPOTHESIS  │────▶│  PROMOTED    │────▶│  ASSERTION   │
│              │     │              │     │              │     │              │
│  Raw pair    │     │  Scored,     │     │  Auto or     │     │  owl:sameAs  │
│  from        │     │  evidenced,  │     │  human       │     │  (downstream │
│  blocking    │     │  auditable   │     │  approved    │     │   system)    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                            │                    │
                            ▼                    │
                     ┌──────────────┐            │
                     │  QUARANTINE  │◀───────────┘
                     │              │   (conflicting
                     │  Needs human │    evidence)
                     │  review      │
                     └──────────────┘
```

### 1.5 Temporal Semantics

| Category | Temporal Model | Interpretation |
|----------|---------------|----------------|
| **Continuants** | Endurantist | Persist as wholly present at each moment; can have different properties at different times |
| **Occurrents** | Perdurantist | Extend through time with temporal parts; identity grounded in spatiotemporal boundaries |

---

## 2. Goals and Non-Goals

### 2.1 Primary Goals

1. **Ontologically-grounded resolution**: BFO/CCO constraints determine what can co-refer
2. **Probabilistic candidate identification**: Calibrated confidence estimates
3. **Transparency and auditability**: Explainable evidence with counterfactuals
4. **Incremental operation**: Batch, streaming, and query modes
5. **Separation of concerns**: Identification vs. decision vs. assertion
6. **General-purpose applicability**: Works standalone or integrated with TagTeam/IEE

### 2.2 Non-Goals (v2)

- Automated assertion of owl:sameAs (left to downstream governance)
- Cross-ontology alignment (assumes shared upper ontology)
- Natural language extraction (TagTeam's responsibility)

### 2.3 Minimal Viable Implementation

| Component | MVP Choice | Full Implementation |
|-----------|------------|---------------------|
| Input | Resolved RDF graphs | + TagTeam bridge |
| Blocking | Type-constrained sorted neighborhood | + LSH, canopy |
| Scoring | Fellegi-Sunter | + GNN embeddings, PSL |
| Promotion | Manual review | + Auto-promotion policies |
| Output | JSON hypothesis sets | + SPARQL CONSTRUCT |

---

## 3. Inputs

### 3.1 Input Modes

| Mode | Source | Use Case |
|------|--------|----------|
| `resolved_graph` | Triple stores, property graphs | General KG resolution |
| `tagteam_ice` | TagTeam output | NLU pipeline integration |

### 3.2 Resolved Graph Input

**Format**: RDF (Turtle, N-Triples, JSON-LD) or labeled property graph with RDF mapping

**Requirements**:
- Nodes typed with BFO-conformant classes
- Predicates from CCO or CCO-aligned ontology
- Provenance metadata recommended

### 3.3 TagTeam Bridge Layer

When consuming TagTeam output, OERS applies a bridge layer translating discourse-derived ICEs to entity candidates.

#### 3.3.1 The Translation Problem

TagTeam produces ICEs that are *about* entities as introduced in discourse:

```turtle
:dr_001 a :DiscourseReferent ;
    :referentialExpression "the doctor" ;
    :candidateType cco:Physician ;
    :denotationConfidence 0.85 ;
    :actualityStatus :Asserted .
```

This is NOT a statement that `:dr_001` IS a physician. It states that text introduced a discourse referent that *may* denote a real physician.

#### 3.3.2 Bridge Configuration

```yaml
input_mode: "tagteam_ice"

tagteam_bridge:
  actuality_filter:
    include: [Asserted]
    exclude: [Questioned]
    special:
      Hypothetical:
        action: "create_as_hypothetical"
        participant_handling: "resolve_against_actual"  # CHANGED in v2
        process_handling: "resolve_only_with_hypothetical"
      Prescribed:
        action: "create_as_planned"
        participant_handling: "resolve_against_actual"  # The doctor in "should treat" is real
        process_handling: "segregate"
  
  confidence_handling:
    floor: 0.5
    tentative_threshold: 0.7
    weight_factor: 0.8
  
  negation_handling:
    negated_existence:
      effect: "suppress_entity_candidate"
    negated_coreference:
      effect: "add_non_coreference_constraint"
      base_confidence: 0.9
      trust_model: "source_weighted"  # NEW in v2
  
  provenance:
    preserve_ice_iri: true
    preserve_document_iri: true
    preserve_span: true
    propagate_grounding_hints: true
```

#### 3.3.3 Hypothetical Participant Resolution (NEW)

**The insight**: "If *Dr. Smith* were to treat *John*..." references **actual** Dr. Smith and **actual** John in a **hypothetical** process.

```yaml
hypothetical_handling:
  # Participants of hypothetical acts resolve against actual entities
  participants:
    resolve_against: "StandardEntity"
    rationale: "Real people can participate in counterfactual scenarios"
  
  # The hypothetical act itself does NOT resolve against actual acts
  processes:
    resolve_against: "HypotheticalEntity"
    rationale: "A described act is not a hypothetical act"
  
  # Output marking
  output:
    participant_resolution: "cross_actuality_allowed"
    process_resolution: "same_actuality_only"
```

### 3.4 Trust Model with Property-Level Overrides (REVISED)

Trust varies not just by source, but by **property within source**.

#### 3.4.1 Source-Level Trust (Base)

```yaml
trust_model:
  source_categories:
    authoritative:
      description: "Government records, biometrics, official registries"
      base_trust: 0.95
      examples: ["SSA", "DMV", "passport_authority"]
      can_override_negation: true
    
    institutional:
      description: "Enterprise systems, HR records, medical records"
      base_trust: 0.85
      examples: ["hospital_ehr", "corporate_hr"]
      can_override_negation: true
    
    extracted:
      description: "NLU-extracted from documents"
      base_trust: 0.70
      examples: ["tagteam_ice"]
      can_override_negation: false
    
    user_reported:
      description: "Self-reported, survey data"
      base_trust: 0.60
      can_override_negation: false
```

#### 3.4.2 Property-Level Trust Overrides (NEW)

```yaml
  property_overrides:
    description: "Override base trust for specific properties within a source"
    
    examples:
      hospital_ehr:
        base_trust: 0.85  # institutional
        overrides:
          # Medical data is highly reliable
          cco:has_medical_condition: 0.95
          cco:has_diagnosis_code: 0.95
          cco:has_procedure_code: 0.95
          # Demographics often stale
          cco:has_address: 0.60
          cco:has_phone_number: 0.55
          cco:has_email_address: 0.50
          # Identity fields reliable
          cco:has_birth_date: 0.90
          cco:has_government_identifier: 0.90
      
      corporate_hr:
        base_trust: 0.85
        overrides:
          cco:has_job_title: 0.92
          cco:has_employer: 0.95
          cco:has_address: 0.70
          cco:has_phone_number: 0.65
      
      dmv:
        base_trust: 0.95  # authoritative
        overrides:
          cco:has_address: 0.85  # Can become stale
          cco:has_drivers_license: 0.99
          cco:has_birth_date: 0.99
    
    resolution:
      rule: "If property override exists, use it; else use base_trust"
      inheritance: "More specific properties inherit from parent if no override"
```

#### 3.4.3 Trust Resolution Algorithm

```python
def resolve_trust(source_id: str, property_iri: str) -> float:
    source_config = trust_model.sources[source_id]
    base_trust = source_config.base_trust
    
    if property_iri in source_config.overrides:
        return source_config.overrides[property_iri]
    
    parent_property = ontology.get_parent_property(property_iri)
    if parent_property and parent_property in source_config.overrides:
        return source_config.overrides[parent_property]
    
    return base_trust
```

### 3.5 Configuration

```yaml
resolution_config:
  input_mode: "resolved_graph"  # or "tagteam_ice"
  
  target_types:
    - cco:Person
    - cco:Organization
    - cco:Artifact
    - bfo:Process
    - bfo:Role
    - bfo:Quality
  
  blocking:
    method: "type_constrained_lsh"
    parameters:
      initial_similarity_threshold: 0.3
      hash_functions: 128
    
    # NEW: Super-cluster handling
    iterative_reblocking:
      enabled: true
      max_block_size: 100
      threshold_increment: 0.15
      max_iterations: 4
  
  scoring:
    method: "fellegi_sunter"
  
  resolution_phases:
    enabled: true
    max_iterations: 5
    stability_threshold: 0.01
  
  temporal:
    fuzziness_handling: "degrade_to_soft"  # NEW
    missing_timestamp_policy: "assume_overlap"  # NEW
  
  performance:  # NEW
    max_graph_depth: 4
    transitive_closure_timeout_ms: 5000
    max_cluster_size: 100
  
  promotion:  # NEW
    policy: "auto_with_quarantine"
    # See Section 4.5 for full policy
  
  output:
    min_confidence: 0.5
    max_candidates_per_node: 100
    include_counterfactuals: true
    include_canonicalized_profile: true
    temporal_format: "validity_interval"  # NEW
```

### 3.6 Two-Layer Identity Model

#### 3.6.1 Independent Continuants

```yaml
identity_model:
  cco:Person:
    ontological_basis:
      bfo_category: independent_continuant
      persistence_type: biological_continuant
      identity_grounding: biological_organism
      temporal_model: endurantist
      
      hard_contradictions:
        - property: cco:has_birth_date
          contradiction_type: exact_mismatch
          effect: identity_impossible
          
      soft_contradictions:
        - property: cco:has_biological_sex
          contradiction_type: exact_mismatch
          effect: extreme_penalty  # CHANGED from identity_impossible
          rationale: "Data entry errors common; administrative vs biological distinction"
          penalty: -0.7
        - property: cco:has_death_date
          contradiction_type: one_present_one_absent
          effect: heavy_penalty
          penalty: -0.5
    
    epistemic_evidence:
      high_weight:
        - property: cco:has_government_identifier
          comparator: exact_or_normalized
          m_probability: 0.95
          u_probability: 0.001
        - property: cco:has_birth_date
          comparator: exact
          m_probability: 0.90
          u_probability: 0.027
      medium_weight:
        - property: foaf:name
          comparator: jaro_winkler
          threshold: 0.85
          m_probability: 0.85
          u_probability: 0.10
      structural:
        - relation: cco:affiliated_with
          match_boost: 0.15
          requires_resolved: true
        - relation: bfo:bearer_of  # NEW: Role-as-Evidence
          match_boost: 0.20
          note: "Role types provide evidence for bearer identity"

  cco:Organization:
    ontological_basis:
      bfo_category: independent_continuant
      persistence_type: socially_constructed_continuant
      identity_grounding: legal_continuity
      temporal_model: endurantist
      
      # NEW: Split/Merge handling
      continuity_events:
        split:
          effect: "create_successors"
          original_persists: false
          model: "predecessor_successor"
        merge:
          effect: "create_successor"
          originals_persist: false
          model: "predecessors_successor"
        acquisition:
          effect: "acquired_continues_under_acquirer"
          acquired_persists: false
      
      hard_contradictions:
        - property: cco:has_legal_identifier
          types: [EIN, DUNS, LEI]
          contradiction_type: different_values_same_type
          effect: identity_impossible
    
    epistemic_evidence:
      high_weight:
        - property: cco:has_legal_identifier
          comparator: exact_normalized
          m_probability: 0.99
          u_probability: 0.0001
      medium_weight:
        - property: cco:has_legal_name
          comparator: legal_name_normalizer
          m_probability: 0.90
          u_probability: 0.02

  cco:Artifact:
    ontological_basis:
      bfo_category: independent_continuant
      persistence_type: physical_particular
      identity_grounding: material_continuity
      hard_contradictions:
        - property: cco:has_serial_number
          contradiction_type: exact_mismatch
          effect: identity_impossible
```

#### 3.6.2 Specifically Dependent Continuants (Dual-Function Model) (REVISED)

**The Role Paradox Solution**: SDCs serve two functions:
1. **Role-as-Evidence**: Used in Phase 0 to help resolve bearers
2. **Role-as-Entity**: Resolved in Phase 2 as distinct nodes

```yaml
  bfo:Role:
    # FUNCTION 1: Role-as-Evidence (used in Phase 0)
    evidence_function:
      description: "Role type provides evidence for bearer identity"
      use_in_phase: 0
      mechanism: "Role types extracted as features of bearer candidates"
      example: "'The Attending Physician' → bearer likely has Physician role"
      evidence_contribution:
        same_role_type: +0.15
        compatible_role_types: +0.05
        incompatible_role_types: -0.10  # CEO and Janitor unlikely same person
    
    # FUNCTION 2: Role-as-Entity (resolved in Phase 2)
    entity_function:
      description: "Role instances resolved as distinct SDC nodes"
      resolve_in_phase: 2
      ontological_basis:
        bfo_category: specifically_dependent_continuant
        persistence_type: bearer_dependent
        identity_grounding: bearer_identity_plus_role_universal
        hard_contradictions:
          - condition: different_bearers
            effect: identity_impossible
          - condition: different_role_types_no_subsumption
            effect: identity_impossible
      epistemic_evidence:
        requires_bearer_resolved: true
        high_weight:
          - relation: bfo:inheres_in
            requirement: mandatory_match
          - property: rdf:type
            comparator: subsumption_check

  bfo:Quality:
    evidence_function:
      use_in_phase: 0
      mechanism: "Quality values as features of bearer"
    entity_function:
      resolve_in_phase: 2
      ontological_basis:
        bfo_category: specifically_dependent_continuant
        persistence_type: bearer_dependent
        identity_grounding: bearer_identity_plus_quality_universal_plus_time
        hard_contradictions:
          - condition: different_bearers
            effect: identity_impossible
```

#### 3.6.3 Occurrents

```yaml
  bfo:Process:
    ontological_basis:
      bfo_category: occurrent
      persistence_type: none
      identity_grounding: spatiotemporal_boundary
      temporal_model: perdurantist
      hard_contradictions:
        - property: cco:has_temporal_region
          contradiction_type: non_overlapping
          effect: identity_impossible
          fuzziness_fallback: soft_penalty  # NEW
    epistemic_evidence:
      high_weight:
        - property: cco:has_start_time
          comparator: temporal_overlap
          m_probability: 0.95
          u_probability: 0.10
      structural:
        - relation: cco:has_participant
          match_boost: 0.25
          requires_resolved: true
```

#### 3.6.4 Temporal Identity with Fuzziness Handling (REVISED)

```yaml
temporal_identity:
  continuants:
    model: endurantist
    time_indexed_properties:
      - cco:has_address
      - cco:has_employer
      - cco:has_role
    
    contradiction_rules:
      with_timestamps:
        same_time_different_value: hard_contradiction
        different_time_different_value: expected_normal
      
      # NEW: Handling missing timestamps
      without_timestamps:
        policy: "configurable"
        options:
          assume_overlap:
            description: "Treat as potentially same time; use soft contradiction"
            effect: soft_penalty
            penalty: -0.3
          assume_disjoint:
            description: "Treat as different times; no contradiction"
            effect: no_penalty
          require_timestamp:
            description: "Exclude from time-sensitive comparison"
            effect: feature_unavailable
        default: "assume_overlap"
  
  occurrents:
    model: perdurantist
    overlap_requirement: true
    
    # NEW: Fuzziness handling
    temporal_fuzziness:
      description: "When exact timestamps unavailable"
      extraction_phrases:
        - pattern: "previously"
          interpretation: "before_reference_time"
          precision: "low"
        - pattern: "last week"
          interpretation: "7_days_before_document_date"
          precision: "medium"
        - pattern: "on January 15"
          interpretation: "exact_date"
          precision: "high"
      
      comparison_rules:
        both_precise: "standard_overlap_check"
        one_fuzzy: "expand_window_then_check"
        both_fuzzy: "degrade_to_soft_evidence"
        neither_available: "exclude_temporal_evidence"
      
      window_expansion:
        low_precision: "±30 days"
        medium_precision: "±7 days"
        high_precision: "±1 day"
```

---

## 4. Outputs

### 4.1 Co-Reference Hypothesis Sets

```json
{
  "hypothesis_sets": [
    {
      "set_id": "hyp_001",
      "hypothesis_type": "co_reference",
      "lifecycle_status": "hypothesis",
      
      "type_analysis": {
        "asserted_types": {
          "node_a": ["cco:Physician", "cco:Person"],
          "node_b": ["cco:Patient", "cco:Person"]
        },
        "most_specific_common": "cco:Person",
        "type_conflict": false,
        "role_evidence_used": ["cco:Physician", "cco:Patient"],
        "role_compatibility_note": "Same person can hold multiple roles"
      },
      
      "members": [
        {
          "iri": "http://source1.gov/person/12345",
          "source_graph": "graph_a",
          "evidence_role": "anchor"
        },
        {
          "iri": ":entity_candidate_002",
          "source_graph": "tagteam_output",
          "evidence_role": "candidate",
          "source_ice": ":dr_001",
          "source_trust_level": "extracted"
        }
      ],
      
      "confidence": 0.87,
      "confidence_band": "high",
      "internal_coherence": 0.91,
      
      "canonicalized_profile": {
        "strategy": "trust_weighted_union",
        "attributes": {
          "cco:has_birth_date": {
            "value": "1985-03-15",
            "source": "http://source1.gov/person/12345",
            "trust_level": "authoritative",
            "confidence": 0.99
          },
          "foaf:name": {
            "values": ["John Smith", "Jonathan Smith", "J. Smith"],
            "preferred": "John Smith",
            "preferred_source": "http://source1.gov/person/12345",
            "trust_level": "authoritative"
          },
          "cco:has_address": {
            "value": "123 Main St, Buffalo, NY",
            "source": "graph_a",
            "as_of": "2025-06-01",
            "note": "Most recent value used"
          }
        },
        "roles_held": ["cco:Physician", "cco:Patient"],
        "role_note": "Roles are SDC instances, not merged"
      },
      
      "promotion_eligibility": {
        "auto_promotable": false,
        "blocking_reasons": ["confidence_below_threshold"],
        "quarantine_triggers": []
      },
      
      "grounding_hints": ["clinical_ethics"]
    }
  ]
}
```

### 4.2 Temporal Object Structure: Validity Intervals (NEW)

All time-indexed properties use the **validity interval** format:

```yaml
temporal_format:
  name: "validity_interval"
  description: "Full temporal history with explicit validity periods"
  
  structure:
    history:
      type: array
      items:
        value: "The property value"
        valid_from: "ISO 8601 date (inclusive)"
        valid_to: "ISO 8601 date (exclusive), null if current"
        source: "IRI of source node"
        source_category: "Trust category"
        property_trust: "Resolved trust for this property from this source"
        is_current: "Boolean, true if current value"
        precision: "exact | day | month | year | fuzzy"
    
    current_value: "Convenience field: value where is_current=true"
    as_of: "Timestamp when current_value was determined"
  
  rules:
    ordering: "History sorted by valid_from ascending"
    gaps_allowed: true
    overlaps_allowed: false
    null_valid_to: "Indicates current/ongoing"

  example:
    property: "cco:has_employer"
    history:
      - value: "Acme Corp"
        valid_from: "2015-06-01"
        valid_to: "2020-08-31"
        source: "hr_graph_acme"
        property_trust: 0.92
      - value: "TechCo Inc"
        valid_from: "2020-09-15"
        valid_to: null
        source: "hr_graph_techco"
        property_trust: 0.90
        is_current: true
    current_value: "TechCo Inc"
    as_of: "2026-01-27"
```

### 4.3 Confidence Interpretation

```yaml
confidence_bands:
  - range: [0.0, 0.3]
    label: "unlikely"
    description: "Insufficient evidence"
    promotion: "never"
  - range: [0.3, 0.5]
    label: "possible"
    description: "Weak evidence; high uncertainty"
    promotion: "manual_only"
  - range: [0.5, 0.7]
    label: "probable"
    description: "Moderate evidence"
    promotion: "manual_recommended"
  - range: [0.7, 0.9]
    label: "high"
    description: "Strong evidence"
    promotion: "auto_eligible"
  - range: [0.9, 0.98]
    label: "very_high"
    description: "Very strong evidence"
    promotion: "auto_eligible"
  - range: [0.98, 1.0]
    label: "near_certain"
    description: "Overwhelming evidence"
    promotion: "auto_default"

calibration:
  target: "X% confidence means X% true matches"
  method: "isotonic_regression"
  requires: "held_out_labeled_data"
```

### 4.3 Canonicalized Profile Strategy (NEW)

When a hypothesis set forms, OERS produces a **canonicalized profile** for downstream consumers.

```yaml
canonicalization:
  strategy: "trust_weighted_union"
  
  strategies:
    trust_weighted_union:
      description: "Union of all attributes; conflicts resolved by trust level"
      steps:
        1: "Collect all attributes from all members"
        2: "For single-valued properties, select highest-trust source"
        3: "For multi-valued properties, union all values"
        4: "For time-indexed properties, select most recent"
        5: "Mark preferred values and sources"
    
    intersection:
      description: "Only attributes present in all members"
      use_case: "High-precision requirements"
    
    anchor_primary:
      description: "Anchor node's values preferred; others supplemental"
      use_case: "When one source is authoritative"
  
  conflict_resolution:
    single_valued_conflict:
      rule: "Highest trust level wins"
      tie_breaker: "Most recent timestamp"
      document: "Record all values with sources"
    
    multi_valued:
      rule: "Union all distinct values"
      deduplication: "Normalize then dedupe"
  
  special_handling:
    identifiers:
      rule: "Collect all; do not merge"
      rationale: "Different IDs from different systems are all valid"
    
    roles:
      rule: "Collect all; do not merge"
      rationale: "Same person can hold multiple roles"
    
    temporal_properties:
      rule: "Prefer most recent; preserve history"
      output: "Current value + historical values if available"
```

### 4.4 Provenance Layers

```json
{
  "provenance": {
    "source_assertions": [
      {
        "layer": "source",
        "graph": "authoritative_registry",
        "trust_level": "authoritative",
        "triple": "reg:p123 cco:has_birth_date '1985-03-15'",
        "timestamp": "2024-01-15T00:00:00Z"
      },
      {
        "layer": "source",
        "graph": "tagteam_output",
        "trust_level": "extracted",
        "triple": ":ec_002 cco:has_birth_date '1985-03-15'",
        "ice_provenance": {
          "source_ice": ":dr_001",
          "source_document": ":doc_001",
          "extraction_confidence": 0.92
        }
      }
    ],
    
    "oers_derivation": {
      "layer": "derived",
      "hypothesis_id": "hyp_001",
      "confidence": 0.87,
      "phases_completed": [0, 1, 2, 3],
      "iterations": 2,
      "model_provenance": {
        "oers_version": "2.0.0",
        "scoring_model": "fellegi_sunter_v1.2.3",
        "identity_profile_version": "v2.0",
        "ontology_iri": "http://example.org/ontology/v3.0"
      }
    },
    
    "promotion": {
      "layer": "promoted",
      "status": "pending",
      "promoted_by": null,
      "promoted_at": null,
      "promotion_type": null
    }
  }
}
```

### 4.5 Promotion Policy (NEW)

```yaml
promotion_policy:
  # Auto-promotion for high-confidence, clean hypotheses
  auto_promote:
    enabled: true
    conditions:
      all_required:
        - confidence_score: ">= 0.98"
        - hard_contradictions: 0
        - soft_contradictions: "<= 1"
        - evidence_sources: ">= 2"
      
      type_specific:
        cco:Person:
          additional: "government_id_match OR (birthdate_match AND name_similarity > 0.9)"
        cco:Organization:
          additional: "legal_id_match"
        cco:Artifact:
          additional: "serial_number_match"
        bfo:Process:
          additional: "temporal_overlap AND participant_overlap"
    
    output:
      lifecycle_status: "promoted"
      promotion_type: "auto"
      audit_note: "Auto-promoted per policy; conditions met"
  
  # Quarantine for conflicting evidence
  quarantine:
    enabled: true
    triggers:
      - condition: "explicit_negation_present AND confidence > 0.7"
        reason: "High confidence conflicts with textual negation"
      - condition: "authoritative_sources_disagree"
        reason: "Multiple authoritative sources with conflicting values"
      - condition: "confidence > 0.9 AND soft_contradiction_count > 2"
        reason: "High confidence despite multiple soft contradictions"
    
    output:
      lifecycle_status: "quarantined"
      requires: "human_review"
      escalation_path: "governance_queue"
  
  # Default for everything else
  default:
    confidence_range: [0.5, 0.98]
    lifecycle_status: "hypothesis"
    promotion_type: "manual"
    
  # Rejection threshold
  rejection:
    confidence_below: 0.3
    lifecycle_status: "rejected"
    retention: "audit_log_only"
```

### 4.6 Entity Continuity Events (NEW)

For organizations that split, merge, or are acquired:

```json
{
  "continuity_events": [
    {
      "event_type": "split",
      "event_date": "2025-06-01",
      "predecessor": {
        "iri": "http://example.org/org/acme_corp",
        "name": "Acme Corporation"
      },
      "successors": [
        {
          "iri": "http://example.org/org/acme_east",
          "name": "Acme East LLC",
          "portion": "eastern_operations"
        },
        {
          "iri": "http://example.org/org/acme_west",
          "name": "Acme West LLC",
          "portion": "western_operations"
        }
      ],
      "identity_note": "Predecessor no longer exists as legal entity; successors are new entities with provenance link",
      "resolution_guidance": {
        "references_before_split": "resolve_to_predecessor",
        "references_after_split": "resolve_to_appropriate_successor",
        "ambiguous_references": "flag_for_review"
      }
    },
    {
      "event_type": "merge",
      "event_date": "2025-09-01",
      "predecessors": [
        {"iri": "http://example.org/org/company_a"},
        {"iri": "http://example.org/org/company_b"}
      ],
      "successor": {
        "iri": "http://example.org/org/merged_co",
        "name": "Merged Company Inc."
      }
    }
  ]
}
```

### 4.7 Non-Coreference Constraints

```json
{
  "non_coreference_constraints": [
    {
      "node_a": ":dr_001_candidate",
      "node_b": ":dr_smith_candidate",
      "constraint_type": "explicit_negation",
      "source": "tagteam_negation",
      "source_text": "The doctor was not Dr. Smith",
      "source_trust_level": "extracted",
      "base_confidence": 0.9,
      "override_status": {
        "overridable": true,
        "override_requires": "authoritative_evidence_confidence > 0.90",
        "current_override_evidence": null
      }
    }
  ]
}
```

---

## 5. Architecture

### 5.1 High-Level Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              OERS v2.0                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                        INPUT LAYER                                    │ │
│  │  ┌─────────────────┐         ┌─────────────────────────────────────┐ │ │
│  │  │  Resolved Graph │         │      TagTeam Bridge Layer           │ │ │
│  │  │  Ingestion      │         │  • Actuality filter                 │ │ │
│  │  │                 │         │  • Hypothetical participant logic   │ │ │
│  │  │                 │         │  • Trust level assignment           │ │ │
│  │  │                 │         │  • Negation with override model     │ │ │
│  │  └────────┬────────┘         └──────────────┬──────────────────────┘ │ │
│  │           └──────────────┬───────────────────┘                        │ │
│  │                          ▼                                            │ │
│  │              ┌───────────────────────┐                                │ │
│  │              │   Entity Candidate    │                                │ │
│  │              │   Pool + Trust Scores │                                │ │
│  │              └───────────────────────┘                                │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                          │                                                  │
│                          ▼                                                  │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                 PHASED RESOLUTION CONTROLLER                          │ │
│  │                                                                        │ │
│  │  Phase 0              Phase 1           Phase 2          Phase N      │ │
│  │  ┌──────────────┐   ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │ │
│  │  │ Continuants  │──▶│  Occurrents  │─▶│    SDCs      │─▶│ Iterate  │ │ │
│  │  │ + Role-as-   │   │  (Process)   │  │  (Role-as-   │  │ until    │ │ │
│  │  │   Evidence   │   │              │  │    Entity)   │  │ stable   │ │ │
│  │  └──────────────┘   └──────────────┘  └──────────────┘  └──────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                        CORE SERVICES                                  │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │ │
│  │  │  Blocking   │  │  Feature    │  │  Scoring    │  │  Temporal   │ │ │
│  │  │  Engine     │  │  Extraction │  │  Engine     │  │  Fuzziness  │ │ │
│  │  │             │  │  + Role     │  │             │  │  Handler    │ │ │
│  │  │             │  │  Evidence   │  │             │  │             │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                     ONTOLOGY SERVICES                                 │ │
│  │  ┌────────────┐ ┌──────────────┐ ┌────────────┐ ┌──────────────────┐ │ │
│  │  │   Type     │ │ Disjointness │ │ Continuity │ │  Identity Model  │ │ │
│  │  │  Checker   │ │   Enforcer   │ │  Events    │ │    Resolver      │ │ │
│  │  └────────────┘ └──────────────┘ └────────────┘ └──────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                   NEGATIVE EVIDENCE ENGINE                            │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐  │ │
│  │  │ Ontological     │  │ Temporal        │  │ Trust-Weighted      │  │ │
│  │  │ Contradiction   │  │ Contradiction   │  │ Negation Override   │  │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                    OUTPUT & PROMOTION                                 │ │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────────────┐ │ │
│  │  │ Transitive │ │ Canonical- │ │ Promotion  │ │ Output Formatter   │ │ │
│  │  │ Closure    │ │ ization    │ │ Policy     │ │ + IEE Contract     │ │ │
│  │  │ (bounded)  │ │ Engine     │ │ Engine     │ │                    │ │ │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Phased Resolution (Revised)

```
Phase 0: Independent Continuants + Role-as-Evidence
├── Input: Entity candidates with trust scores
├── Scope: Persons, Organizations, Artifacts
├── Evidence: 
│   ├── Direct attributes
│   └── Role types as features (SDC evidence function)  # NEW
├── Output: Frozen continuant hypotheses
│
Phase 1: Occurrents
├── Input: Candidates + Phase 0 hypotheses
├── Scope: Processes, Events
├── Evidence: Attributes + resolved participants
├── Temporal: Fuzziness handling applied
├── Output: Frozen occurrent hypotheses
│
Phase 2: SDCs as Entities
├── Input: Candidates + Phase 0 + Phase 1 hypotheses
├── Scope: Roles, Qualities (as distinct nodes)
├── Constraint: Bearer must be resolved
├── Output: Frozen SDC hypotheses
│
Phase N: Iterate with Structural Evidence
├── Re-score all with full structural evidence
├── Stability: max(|score_delta|) < ε
├── Timeout: max_iterations reached
├── Output: Final hypothesis sets
│
Post-Processing:
├── Apply promotion policy
├── Generate canonicalized profiles
├── Format for downstream consumers
```

### 5.3 Performance Architecture

#### 5.3.1 Iterative Re-Blocking for Super-Clusters (NEW)

**Problem**: Common entities (e.g., "John Smith") can form blocking clusters of thousands, exceeding computational limits.

**Solution**: Adaptive threshold re-blocking that fractures super-clusters without losing true matches.

```yaml
iterative_reblocking:
  algorithm:
    initial_threshold: 0.3
    max_block_size: 100
    threshold_increment: 0.15
    max_iterations: 4
    final_threshold_cap: 0.75
  
  pseudocode: |
    function block_with_reblocking(candidates, type):
      threshold = 0.3
      blocks = initial_blocking(candidates, type, threshold)
      
      for iteration in 1..4:
        oversized = [b for b in blocks if size(b) > 100]
        if not oversized:
          return blocks
        
        for block in oversized:
          threshold_local = threshold + (0.15 * iteration)
          if threshold_local > 0.75:
            # Cannot fracture further; sample or flag
            blocks.append(sample_block(block, 100))
            blocks.append(flag_for_review(block))
          else:
            sub_blocks = reblock(block, threshold_local)
            blocks.remove(block)
            blocks.extend(sub_blocks)
      
      return blocks
  
  fallback:
    description: "When max iterations reached and blocks still oversized"
    options:
      sample: "Random sample 100 candidates; flag as sampled_super_cluster"
      review: "Flag entire block for manual review"
      hybrid: "Sample for auto-processing; queue full block for batch review"
    default: hybrid
  
  example:
    scenario: "5000 'John Smith' candidates"
    iteration_1: {threshold: 0.3, result: "1 block of 5000"}
    iteration_2: {threshold: 0.45, result: "12 blocks averaging 400"}
    iteration_3: {threshold: 0.60, result: "48 blocks averaging 100"}
    iteration_4: {threshold: 0.75, result: "Most under 100; 3 flagged for review"}
```

#### 5.3.2 Transitive Closure with Union-Find (MANDATORY)

```yaml
transitive_closure:
  algorithm: "disjoint_set_union_find"
  implementation: "union_by_rank_with_path_compression"
  
  complexity:
    per_operation: "O(α(N))"
    total: "O(N × α(N)) ≈ O(N)"
    note: "α is inverse Ackermann; ≤4 for any practical N"
  
  pseudocode: |
    class DisjointSet:
      def find(self, x):
        if self.parent[x] != x:
          self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
      
      def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.size[px] + self.size[py] > MAX_CLUSTER_SIZE:
          return False  # Refuse merge; flag for review
        # Union by rank
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        return True
  
  constraints:
    max_cluster_size: 100
    timeout_ms: 5000
    on_size_exceeded: "refuse_merge_and_flag"
    on_timeout: "return_partial_with_warning"
  
  rationale: |
    Naive BFS/DFS approaches have O(N²) worst case.
    Union-Find achieves near-linear time, essential for Phase 3 re-scoring.
```

#### 5.3.3 Performance Constraints Summary

```yaml
performance:
  blocking:
    max_block_size: 10000
    timeout_ms: 2000
  
  scoring:
    batch_size: 1000
    timeout_per_pair_ms: 50
  
  transitive_closure:
    algorithm: "union_find"  # O(α(n)) per operation
    max_cluster_size: 100
    timeout_ms: 5000
    depth_limit: 4
    on_timeout: "return_partial_with_warning"
  
  phased_resolution:
    max_iterations: 5
    max_phase_time_ms: 30000
    on_timeout: "freeze_current_state"
  
  memory:
    max_candidates_in_memory: 1000000
    spill_to_disk_threshold: 0.8
```

### 5.4 Negative Evidence with Trust Override (REVISED)

```yaml
negative_evidence:
  ontological_contradiction:
    description: "Impossible per BFO/CCO"
    effect: "confidence = 0"
    override: "never"
  
  temporal_contradiction:
    description: "Same property, same time, different values"
    with_precise_timestamps:
      effect: "confidence = 0"
    with_fuzzy_timestamps:
      effect: "soft_penalty"
      penalty: -0.4
  
  explicit_negation:
    description: "Text states non-identity"
    base_effect: "hard_constraint"
    
    trust_override:  # NEW
      enabled: true
      rule: "Authoritative evidence can override extracted negation"
      conditions:
        - override_source_trust: "authoritative"
        - override_evidence_confidence: ">= 0.90"
        - negation_source_trust: ["extracted", "user_reported"]
      
      example:
        scenario: "Witness says 'I was not there'"
        negation_source: "extracted"
        override: "Biometric places person at scene"
        override_source: "authoritative"
        result: "Negation constraint removed; flag for review"
      
      output:
        override_applied: true
        original_constraint: "non_coreference"
        override_evidence: "biometric_id_abc123"
        review_flag: true
```

---

## 6. IEE Integration

### 6.1 Integration Contract

OERS provides IEE with resolved scenarios:

```json
{
  "resolved_scenario": {
    "scenario_id": "scn_001",
    "resolution_confidence": 0.88,
    
    "entities": [
      {
        "unified_id": "person_001",
        "canonical_type": "cco:Person",
        "hypothesis_confidence": 0.92,
        "lifecycle_status": "promoted",
        "canonicalized_profile": {
          "name": "Dr. John Smith",
          "roles": ["cco:Physician"],
          "identifiers": ["NPI:1234567890"]
        },
        "source_nodes": [":dr_001", ":physician_002"],
        "grounding_hints": ["medical_ethics", "clinical_practice"]
      }
    ],
    
    "processes": [
      {
        "unified_id": "process_001",
        "canonical_type": "cco:ActOfCaregiving",
        "hypothesis_confidence": 0.85,
        "lifecycle_status": "hypothesis",
        "participants": {
          "agent": "person_001",
          "patient": "person_002"
        },
        "temporal": {
          "start": "2026-01-15T10:00:00Z",
          "precision": "high"
        },
        "grounding_hints": ["informed_consent", "duty_of_care"]
      }
    ],
    
    "unresolved_entities": [],
    "continuity_events": [],
    
    "iee_guidance": {
      "primary_frameworks": ["medical_ethics", "clinical_practice"],
      "scenario_type": "treatment_decision",
      "confidence_note": "One process still at hypothesis level"
    }
  }
}
```

### 6.2 Grounding Hint Propagation

```yaml
grounding_propagation:
  source: "tagteam_ice.groundingFrameworkHints"
  aggregation: "union_across_hypothesis_set"
  priority: "frequency_weighted"
  
  output:
    hypothesis_level: "grounding_hints"
    scenario_level: "iee_guidance.primary_frameworks"
  
  framework_mapping:
    clinical_ethics: ["medical_ethics", "informed_consent", "duty_of_care"]
    legal_compliance: ["regulatory", "liability"]
    business_ethics: ["fiduciary_duty", "stakeholder_interests"]
```

---

## 7. Processing Modes

### 7.1 Batch Mode
- Full graph consumption
- All phases executed
- Complete hypothesis generation
- Promotion policy applied

### 7.2 Incremental Mode
- Streaming entity candidates
- Blocking against existing index
- Delta hypothesis output
- Auto-promotion for streaming efficiency

### 7.3 Query Mode
- Single node lookup
- Find co-reference candidates
- Low-latency response
- Uses frozen context from last batch

---

## 8. API Specification

```yaml
openapi: 3.0.0
info:
  title: OERS API
  version: 2.0.0

paths:
  /resolve/batch:
    post:
      summary: Submit graphs or ICEs for batch resolution
      requestBody:
        content:
          application/n-triples: {}
          application/ld+json: {}
          application/x-tagteam-ice: {}
      responses:
        202:
          description: Job accepted
          
  /resolve/stream:
    post:
      summary: Stream entity candidates for incremental resolution
      description: WebSocket endpoint for continuous resolution
          
  /resolve/query:
    post:
      summary: Find candidates for specific node
      requestBody:
        content:
          application/json:
            schema:
              properties:
                node_iri: {type: string}
                include_canonicalized: {type: boolean, default: true}
                include_counterfactuals: {type: boolean, default: true}
                
  /hypotheses/{hypothesis_id}/promote:
    post:
      summary: Manually promote hypothesis to assertion
      
  /hypotheses/{hypothesis_id}/reject:
    post:
      summary: Reject hypothesis
      
  /continuity-events:
    post:
      summary: Register entity split/merge/acquisition
      
  /ontology/validate:
    post:
      summary: Check ontology quality
      
  /health:
    get:
      summary: Service health including phase timing
```

---

## 9. Ontology Quality and Failure Modes

### 9.1 Required Properties

| Property | Requirement | Failure Mode |
|----------|-------------|--------------|
| Disjointness | Complete for resolution types | False cross-type candidates |
| Domain/range | Accurate | Wrong feature extraction |
| SDC relations | Explicit inheres_in/bearer_of | SDC resolution fails |
| Temporal properties | Marked as time-indexed | Incorrect contradiction detection |

### 9.2 Graceful Degradation

| Condition | Behavior |
|-----------|----------|
| Missing disjointness | Proceed; flag cross-sibling candidates |
| Missing timestamps | Apply fuzziness policy |
| SDC without bearer | Defer; flag if unresolved after Phase 2 |
| Timeout | Return partial results with warning |

---

## 10. Security and Privacy

### 10.1 Sensitive Attributes

```yaml
sensitivity:
  critical:
    properties: [has_ssn, has_passport_number]
    handling: "hash_comparison"
    logging: "never_log_values"
  high:
    properties: [has_birth_date, has_government_id]
    handling: "encrypted_at_rest"
  moderate:
    properties: [has_address, has_email]
    handling: "standard"
```

### 10.2 Access Control

- Role-based access to hypothesis sets
- Audit logging of all promotions
- Configurable retention policies

---

## 11. Worked Example: Full Pipeline

### 11.1 Source Documents

**Document A**: "The attending physician treated the patient for hypertension."
**Document B**: "Dr. Smith administered care to John Doe on 2026-01-15."

### 11.2 TagTeam Output

```turtle
# Document A
:dr_001 a :DiscourseReferent ;
    :candidateType cco:Physician ;
    :denotationConfidence 0.80 ;
    :actualityStatus :Asserted ;
    :hasRole cco:AttendingPhysician .  # Role evidence

# Document B  
:dr_002 a :DiscourseReferent ;
    :candidateType cco:Physician ;
    :denotationConfidence 0.95 ;
    :has_name "Dr. Smith" .
```

### 11.3 OERS Processing

**Phase 0 (with Role-as-Evidence)**:
- Both candidates typed Physician
- Role evidence: `:dr_001` has AttendingPhysician role
- Name evidence: `:dr_002` has "Dr. Smith"
- Role compatibility: AttendingPhysician compatible with generic Physician
- **Phase 0 confidence**: 0.55 (moderate—name difference, role compatible)

**Phase 1 (Processes)**:
- Treatment and care event have temporal overlap (fuzzy: "previously" vs "2026-01-15")
- Participant overlap depends on person resolution
- **Phase 1 confidence**: 0.60

**Phase 3 (Re-score)**:
- Structural evidence: both doctors participate in similar care events
- **Final confidence**: 0.78

### 11.4 Output

```json
{
  "hypothesis_sets": [{
    "set_id": "hyp_001",
    "confidence": 0.78,
    "lifecycle_status": "hypothesis",
    "promotion_eligibility": {
      "auto_promotable": false,
      "reason": "confidence < 0.98"
    },
    "canonicalized_profile": {
      "name": {"preferred": "Dr. Smith", "alternatives": ["the attending physician"]},
      "roles": ["cco:Physician", "cco:AttendingPhysician"]
    }
  }]
}
```

---

## 12. Closed Questions

| Question | Resolution |
|----------|------------|
| Role Paradox | Dual-function SDC model |
| Temporal Fuzziness | Configurable degradation |
| Governance Bottleneck | Auto-promotion with quarantine |
| Canonicalization | Trust-weighted union with validity intervals |
| Entity Splits | Predecessor/successor model |
| Negation Trust | Source-weighted override |
| **Super-Clusters** | **Iterative re-blocking (v2.1)** |
| **Trust Granularity** | **Property-level overrides (v2.1)** |
| **Temporal History** | **Validity interval structure (v2.1)** |
| **Closure Algorithm** | **Union-Find mandated (v2.1)** |

## 13. Open Questions

1. **Cross-ontology operation**: How to handle graphs with different ontologies?
2. **Human feedback loop**: How do reviewer decisions update m/u probabilities?
3. **Federated resolution**: Resolution across organizational boundaries?
4. **Versioned identity**: How to track identity through time in append-only stores?

---

## Appendix A: BFO Category Summary

| Category | Persistence | Identity | Phase |
|----------|-------------|----------|-------|
| Person | Biological | Organism | 0 |
| Organization | Legal | Continuity | 0 |
| Artifact | Physical | Material | 0 |
| Process | None | Spatiotemporal | 1 |
| Role | Bearer-dependent | Bearer + type | 0 (evidence), 2 (entity) |
| Quality | Bearer-dependent | Bearer + type + time | 0 (evidence), 2 (entity) |

## Appendix B: Glossary

- **Auto-promotion**: Policy-based promotion of hypothesis to assertion without human review
- **Canonicalized profile**: Merged attribute set from hypothesis members with trust-weighted conflict resolution
- **Continuity event**: Split, merge, or acquisition of an organization
- **Iterative re-blocking**: Technique to fracture oversized blocking clusters by progressively increasing similarity threshold
- **Lifecycle status**: candidate → hypothesis → promoted/quarantined → assertion
- **Property-level trust**: Trust score specific to a property from a specific source, overriding base source trust
- **Role-as-Evidence**: Using role types as features in bearer resolution (Phase 0)
- **Role-as-Entity**: Resolving role instances as distinct SDC nodes (Phase 2)
- **Trust level**: Source reliability category (authoritative, institutional, extracted, user_reported)
- **Union-Find**: Disjoint-set data structure for efficient transitive closure with near-linear complexity
- **Validity interval**: Temporal structure with explicit valid_from/valid_to boundaries for time-indexed properties

## Appendix D: Implementation Checklist

### Phase 1: MVP (Minimal Viable OERS)
- [ ] Resolved graph ingestion (RDF parsing)
- [ ] Type-constrained blocking (sorted neighborhood)
- [ ] Fellegi-Sunter scoring engine
- [ ] Union-Find transitive closure
- [ ] JSON output format
- [ ] Basic audit logging

### Phase 2: Production Hardening
- [ ] Iterative re-blocking for super-clusters
- [ ] Property-level trust configuration
- [ ] Validity interval history builder
- [ ] Auto-promotion policy engine
- [ ] Quarantine workflow
- [ ] Performance monitoring

### Phase 3: Integration
- [ ] TagTeam bridge layer
- [ ] IEE output contract
- [ ] Streaming/incremental mode
- [ ] REST API endpoints
- [ ] SHACL shape validation

### Phase 4: Advanced Features
- [ ] GNN embeddings (optional)
- [ ] PSL rules (optional)
- [ ] Continuity event handling
- [ ] Human feedback loop
- [ ] Cross-ontology alignment

---

*End of Specification*

### v2.1.0 (2026-01-27) - CURRENT
- **Super-Cluster Handling**: Iterative re-blocking with adaptive thresholds (Section 5.3.1)
- **Temporal History**: Full validity interval structure for time-indexed properties (Section 4.2)
- **Property-Level Trust**: Trust overrides by property within source (Section 3.4.2)
- **Union-Find Mandate**: Confirmed as required algorithm for transitive closure (Section 5.3.2)
- **Status**: Approved for Development

### v2.0.0 (2026-01-27)
- **Role Paradox**: Dual-function SDC model (evidence in Phase 0, entity in Phase 2)
- **Temporal Fuzziness**: Configurable degradation when timestamps missing/imprecise
- **Governance Bottleneck**: Auto-promotion policies with quarantine rules
- **Canonicalization**: Trust-weighted union strategy for merged profiles
- **Entity Splits**: Predecessor/successor model for org restructuring
- **Trust Model**: Source-weighted evidence with negation override
- **Performance**: Bounded traversal, timeouts, depth limits
- **Biological Sex**: Downgraded from hard to soft contradiction
- **Hypothetical Participants**: Can resolve against actual entities

### v1.2.0 (2026-01-27)
- TagTeam bridge layer
- SDC identity model
- Temporal semantics
- IEE integration

### v1.1.0 (2026-01-27)
- Two-layer identity model
- Phased resolution
- Negative evidence classification

### v1.0.0 (2026-01-27)
- Initial specification
