# Modal Discourse Reasoning Engine (MDRE)

## Technical Specification v1.3

**Version:** 1.3.0  
**Date:** January 2026  
**Status:** Draft for Implementation Review

---

> *A Semantic Accountability Layer for Modal and Deontic Reasoning over Natural Language Discourse*

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | January 2026 | Initial specification |
| 1.1.0 | January 2026 | Conflict resolution taxonomy, modal predicate ontological status, user tier model |
| 1.2.0 | January 2026 | Confidence bridging protocol, entity resolution layer, temporal performance constraints, dynamic priority calculus, evidence tier system, terminology corrections |
| 1.3.0 | January 2026 | Logical foundations framework, FOL encoding of modal concepts, quantification semantics, decidability guarantees, expressiveness boundaries, upgrade paths to SOL |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Foundational Principles](#2-foundational-principles)
3. [Logical Foundations](#3-logical-foundations)
4. [Formal Ontology](#4-formal-ontology)
5. [Confidence Bridging Protocol](#5-confidence-bridging-protocol)
6. [Entity Resolution Layer](#6-entity-resolution-layer)
7. [Modal and Deontic Predicates](#7-modal-and-deontic-predicates)
8. [Evidence Tier System](#8-evidence-tier-system)
9. [Temporal Semantics](#9-temporal-semantics)
10. [Inference Rules and Conflict Resolution](#10-inference-rules-and-conflict-resolution)
11. [Query System](#11-query-system)
12. [User Interface Semantics](#12-user-interface-semantics)
13. [Integration Architecture](#13-integration-architecture)
14. [Ontological Alignment (BFO/CCO)](#14-ontological-alignment-bfocco)
15. [Security and Trust Model](#15-security-and-trust-model)
16. [Performance Constraints and Benchmarks](#16-performance-constraints-and-benchmarks)
17. [Implementation Roadmap](#17-implementation-roadmap)
18. [Appendices](#appendices)

---

## 1. Executive Summary

The Modal Discourse Reasoning Engine (MDRE) is a formal reasoning system that processes natural language text to extract, represent, and reason over modal and deontic commitments. MDRE integrates TagTeam (a semantic parsing layer) with Tau.js (a Prolog-based inference engine) to provide auditable, epistemically honest reasoning over what has been stated, asserted, or implied in discourse.

### 1.1 Core Design Principle

> **The Prolog knowledge base represents *discourse commitments*, not claims about reality.**

MDRE never asserts or implies:
- Omniscience or complete world knowledge
- Closed-world assumptions about reality
- Unattributed factual truth about the world

Instead, MDRE surfaces:
- What has been asserted in source text
- Under what modal qualification (obligatory, permitted, forbidden, hypothetical, etc.)
- By whom or from what text the assertion derives
- What is logically derivable from those assertions
- The confidence level of extracted claims

### 1.2 The Oracle Problem

MDRE explicitly addresses what we term the **Oracle Problem**: the tendency of AI systems to present extracted or inferred information as objective truth. By grounding the system in discourse commitments rather than objective truth, MDRE provides:

- **Epistemic accountability**: Every claim traces to its source
- **Uncertainty visibility**: Extraction confidence is preserved, not hidden
- **Defeasibility**: Claims can be retracted when evidence changes
- **Non-omniscience**: The system explicitly acknowledges what it does not know

### 1.3 Philosophical Position

MDRE operates within **epistemic modal logic**, not ontology-as-reality modeling. The system's "possible worlds" are *discourse states*, not metaphysical alternatives. This directly addresses the objection that "the system models reality"—it does not. It models what is *said to be* possible, required, or actual.

### 1.4 System Components

| Component | Function |
|-----------|----------|
| **TagTeam** | Semantic parsing layer that extracts structured claims with confidence scores |
| **Confidence Bridge** | Mediates between probabilistic extraction and logical assertion |
| **Entity Resolution Layer** | Resolves cross-document identity and coreference |
| **Tau.js** | Prolog-based inference engine that reasons over promoted assertions |
| **Provenance Layer** | Maintains complete traceability from conclusions to source text |
| **Modal Status Layer** | First-class representation of deontic and alethic modalities |
| **Conflict Resolution Layer** | Distinguishes detection, analysis, and resolution of normative conflicts |
| **Query Interface** | Typed query system with explicit permissibility constraints |

### 1.5 V1.3 Key Additions

This version formalizes the logical foundations of MDRE:

1. **Logical Foundations Framework** (§3): Explicit grounding in multi-sorted first-order logic
2. **FOL Encoding of Modal Concepts** (§3.2): Clarifies relationship between modal logic and implementation
3. **Quantification Semantics** (§3.3): Resolves ambiguities in universal vs. existential quantification
4. **Decidability Guarantees** (§3.4): Documents the decidable fragment MDRE operates within
5. **Expressiveness Boundaries** (§3.5): Explicitly states what cannot be expressed
6. **Upgrade Paths** (§3.6): Future extensibility to second-order logic and hybrid reasoning

---

## 2. Foundational Principles

### 2.1 The Discourse Commitment Principle

MDRE operates on the foundational distinction between **discourse commitments** and **metaphysical claims**. This distinction is not merely terminological but architecturally enforced throughout the system.

| Category | MDRE Represents | MDRE Does Not Represent |
|----------|-----------------|-------------------------|
| Existence | Entities mentioned in discourse | Whether entities exist in reality |
| Events | Actions described or prescribed | Whether actions occurred |
| Obligations | Normative statements from text | Objective moral truths |
| Permissions | Explicitly granted permissions | Default permissibility |
| Identity | Asserted coreference between mentions | Metaphysical identity |

### 2.2 Epistemic Restraint

MDRE enforces epistemic restraint through **architectural constraints** rather than advisory guidelines.

#### 2.2.1 What MDRE Surfaces

- What has been asserted in the source text
- The confidence level of the extraction
- Under what modal qualification the assertion operates
- By whom or from what text the assertion derives
- What is logically derivable from the assertion set
- The confidence of derived conclusions

#### 2.2.2 What MDRE Does Not Surface

- Omniscient knowledge of the world
- Closed-world assumptions about reality
- Unattributed factual claims
- Inference beyond logical derivation from stated premises
- High-confidence conclusions from low-confidence premises (without flagging)

### 2.3 Provenance as Non-Negotiable

Every fact in the MDRE knowledge base must be traceable to its source. This is not a recommended practice but a **hard system constraint**. Facts without provenance cannot be asserted.

### 2.4 Instantiation vs. Asserted Actuality

A critical distinction that MDRE enforces:

> **Instantiation** (creating an entity in the discourse model) is categorically different from **asserted actuality** (claiming the entity exists or an event occurred in the world).

When MDRE creates `act(payment_001)`, it instantiates a *discourse entity*—a representation of something mentioned in text. The predicate `actual(E, Evidence)` is the *only* mechanism for asserting that a discourse entity corresponds to something that occurred in the world, and it requires explicit evidence meeting tier requirements (see §7).

### 2.5 The Probabilistic-Deterministic Interface

> **V1.2 Addition:** MDRE explicitly acknowledges that it operates at the boundary between probabilistic NLP extraction and deterministic logical reasoning.

This boundary is managed through:
- **Confidence thresholds** for automatic promotion
- **Candidate staging** for uncertain extractions
- **Human-in-the-loop review** for borderline cases
- **Confidence propagation** through inference chains

---

## 3. Logical Foundations

> **V1.3 Addition:** This section explicitly defines the logical framework underlying MDRE, addressing the relationship between modal logic concepts and their first-order implementation.

### 3.1 Framework Overview

MDRE employs a **multi-sorted first-order logic (FOL)** with distinguished predicates for modal and deontic operators. This design choice provides:

- The **conceptual expressiveness** of modal and deontic logic
- The **implementation tractability** of first-order logic in Prolog
- **Decidability** within well-defined bounds
- Clear **interoperability paths** with other formal systems

#### 3.1.1 Why Not Pure Modal Logic?

Pure modal logic with full Kripke semantics would require:
- Explicit accessibility relations between possible worlds
- World-indexed evaluation of formulas
- Complex model-theoretic machinery

These are theoretically elegant but:
- Computationally expensive to implement
- Difficult to explain to non-logicians
- Unnecessary for MDRE's core use cases

#### 3.1.2 Why Not Second-Order Logic?

Second-order logic (SOL) allows quantification over predicates:

```
∃P. ∀x. P(x) → Obligatory(x)
```

This would enable:
- Defining norm schemas by structural properties
- Expressing meta-level principles
- Quantifying over resolution strategies

However, SOL is:
- **Undecidable** in general (no complete proof procedure)
- **Computationally intractable** even for decidable fragments
- **Overkill** for most MDRE use cases

SOL capabilities are deferred to V3.0 via hybrid reasoning (see §3.6).

#### 3.1.3 The Chosen Approach: FOL with Modal Predicates

MDRE encodes modal concepts as first-order predicates, preserving the *inspectability* and *queryability* that are core requirements, while remaining within decidable FOL.

This is standard practice in implemented deontic systems and aligns with:
- Standard Modal Logic translations to FOL
- Description Logic foundations (OWL/SWRL)
- Practical legal reasoning systems

### 3.2 Multi-Sorted First-Order Logic

MDRE's logic is organized into distinct **sorts** (types) with sort-specific predicates and functions.

#### 3.2.1 Sort Hierarchy

```
Sort Hierarchy:
├── Entity (top-level)
│   ├── Event
│   │   ├── Act
│   │   └── State
│   ├── Continuant
│   │   ├── Person
│   │   ├── Organization
│   │   └── Artifact
│   ├── InformationEntity
│   │   ├── Norm
│   │   ├── Document
│   │   └── Mention
│   └── Role
├── Temporal
│   ├── TimePoint
│   ├── Duration
│   └── Interval
├── Evidence
│   ├── Observation
│   ├── Record
│   ├── Attestation
│   └── Report
└── Authority
    ├── InstitutionalAuthority
    └── DocumentaryAuthority
```

#### 3.2.2 Sort Declarations

```prolog
% Sort declarations (meta-level, enforced by type checking)
sort(event).
sort(act) :- subsort(act, event).
sort(state) :- subsort(state, event).
sort(continuant).
sort(person) :- subsort(person, continuant).
sort(organization) :- subsort(organization, continuant).
sort(artifact) :- subsort(artifact, continuant).
sort(information_entity).
sort(norm) :- subsort(norm, information_entity).
sort(document) :- subsort(document, information_entity).
sort(mention) :- subsort(mention, information_entity).
sort(role).
sort(temporal).
sort(time_point) :- subsort(time_point, temporal).
sort(duration) :- subsort(duration, temporal).
sort(evidence).
sort(authority).
```

#### 3.2.3 Typed Predicates

All MDRE predicates are typed by their argument sorts:

```prolog
% Predicate type signatures
predicate_signature(act, [event]).
predicate_signature(person, [continuant]).
predicate_signature(agent, [event, continuant]).
predicate_signature(theme, [event, continuant]).
predicate_signature(obligatory, [event]).
predicate_signature(obligatory, [event, norm, authority]).
predicate_signature(obligatory, [event, norm, authority, confidence]).
predicate_signature(derived_from, [entity, text_hash, document, time_point, confidence]).
```

### 3.3 Modal Operators as First-Order Predicates

Rather than implementing full Kripke semantics with accessibility relations, MDRE encodes modal concepts as queryable first-order predicates.

#### 3.3.1 The Encoding

| Modal Concept | Standard Notation | MDRE FOL Encoding | Interpretation |
|---------------|-------------------|-------------------|----------------|
| Necessity | □φ | `necessary(φ)` | "φ follows from the premises" |
| Possibility | ◇φ | `possible(φ)` | "φ is consistent with the premises" |
| Obligation | O(φ) | `obligatory(φ, N, A)` | "Norm N from authority A makes φ obligatory" |
| Permission | P(φ) | `permitted(φ, N, A)` | "Norm N from authority A permits φ" |
| Prohibition | F(φ) | `forbidden(φ, N, A)` | "Norm N from authority A prohibits φ" |
| Actuality | @φ | `actual(φ, E)` | "Evidence E supports φ having occurred" |

#### 3.3.2 What This Encoding Preserves

1. **Inspectability**: Modal status is directly queryable
   ```prolog
   ?- obligatory(E, Norm, Authority).
   ```

2. **Norm Attribution**: Every deontic status is attributed to a specific norm and authority
   ```prolog
   ?- obligatory(pay_001, contract_clause_5, purchase_agreement).
   ```

3. **Conflict Detection**: Modal conflicts are first-order patterns
   ```prolog
   conflict(E) :- obligatory(E, N1, _), forbidden(E, N2, _).
   ```

4. **Provenance**: Modal assertions have the same provenance requirements as other facts

#### 3.3.3 What This Encoding Does Not Preserve

1. **Accessibility Relations**: No explicit modeling of which "worlds" are accessible from which
2. **Nested Modalities**: Limited support for `□◇φ` (necessarily possible) without explicit encoding
3. **Quantified Modal Logic**: No direct support for `□∀x.P(x)` vs `∀x.□P(x)` distinctions

These limitations are acceptable for MDRE's use cases and can be addressed in V3.0 if needed.

### 3.4 Quantification Semantics

MDRE's treatment of quantification is made explicit to avoid ambiguity.

#### 3.4.1 Existential Quantification (Default)

All ground assertions are implicitly existentially quantified at the top level:

```prolog
% This assertion:
obligatory(pay_001, norm_001, contract).

% Means (in FOL):
% ∃e. ∃n. ∃a. (e = pay_001 ∧ n = norm_001 ∧ a = contract ∧ Obligatory(e, n, a))

% Or more simply: "There exists a specific obligation instance"
```

#### 3.4.2 Universal Quantification (Via Rules)

Universal statements require explicit encoding as rules:

```prolog
% "All buyers must pay" is encoded as:
obligatory(Payment, purchase_norm, contract) :-
    act_type(Payment, payment),
    agent_qua_role(Payment, _, buyer).

% This means (in FOL):
% ∀p. (ActType(p, payment) ∧ ∃a,r. AgentQuaRole(p, a, buyer)) 
%     → Obligatory(p, purchase_norm, contract)
```

#### 3.4.3 Scope Disambiguation

When quantifier scope matters, MDRE uses explicit predicate structure:

```prolog
% "Every employee must complete some training" (∀∃ reading)
obligatory(complete_training(Employee, _), hr_policy, hr) :-
    employee(Employee).

% "There is some training that every employee must complete" (∃∀ reading)  
universal_training_requirement(Training) :-
    training(Training),
    required_for_all(Training).

obligatory(complete_training(Employee, Training), hr_policy, hr) :-
    employee(Employee),
    universal_training_requirement(Training).
```

#### 3.4.4 Quantification in Queries

Query variables are existentially quantified by Prolog's semantics:

```prolog
% Query: "Is there any obligation?"
?- obligatory(E, _, _).
% Interpretation: ∃e,n,a. Obligatory(e, n, a)

% Query: "What obligations exist for buyers?"
?- obligatory(E, N, A), agent_qua_role(E, _, buyer).
% Interpretation: ∃e,n,a. (Obligatory(e, n, a) ∧ ∃x. AgentQuaRole(e, x, buyer))
```

### 3.5 Decidability Guarantees

MDRE restricts itself to a decidable fragment of first-order logic.

#### 3.5.1 Datalog Restrictions

The core reasoning stays within **Datalog** (function-free Horn clauses with negation):

| Feature | Datalog | MDRE | Notes |
|---------|---------|------|-------|
| Function symbols | ❌ | Limited | Only for structured terms like `days(30)` |
| Recursion | ✓ | ✓ | Bounded by depth limit |
| Negation | Stratified | Stratified | No unstratified negation |
| Disjunction in heads | ❌ | ❌ | Not supported |

#### 3.5.2 Guaranteed Termination

MDRE queries are guaranteed to terminate under these conditions:

1. **No unbounded recursion**: Inference depth is capped at 10 levels
2. **Stratified negation**: Negative literals only reference lower strata
3. **Finite domains**: All domains are explicitly finite (no function symbol nesting)
4. **Timeout enforcement**: Queries have hard time limits

```prolog
% Recursion depth enforcement
max_inference_depth(10).

infer_bounded(Goal, Depth) :-
    Depth > 0,
    max_inference_depth(Max),
    Depth =< Max,
    NewDepth is Depth - 1,
    call_with_depth(Goal, NewDepth).
```

#### 3.5.3 Complexity Bounds

| Operation | Complexity | Bound |
|-----------|------------|-------|
| Ground query | O(1) | Constant |
| Single-variable query | O(n) | Linear in facts |
| Join query | O(n²) | Quadratic, bounded by timeout |
| Transitive closure | O(n³) | Cubic, depth-limited |
| Temporal constraint | O(n) | Linear, count-limited |

### 3.6 Expressiveness Boundaries

MDRE explicitly documents what it **cannot** express.

#### 3.6.1 Not Expressible in V1.3

| Concept | Why Not | Workaround |
|---------|---------|------------|
| Nested modalities (□◇φ) | Would require world-indexed predicates | Flatten to explicit patterns |
| Quantified modal (∀x.□P(x) vs □∀x.P(x)) | Scope ambiguity | Use explicit rule encoding |
| Norm schemas ("all prohibitions of type T") | Requires SOL | Enumerate or defer to V3.0 |
| Meta-rules ("rules about rules") | Requires reflection | External rule management |
| Counterfactual conditionals | Requires possible world semantics | Mark as `hypothetical` |
| Probabilistic inference | FOL is boolean | Confidence is metadata, not logic |

#### 3.6.2 Design Rationale

These limitations are **intentional constraints** that:

1. **Preserve decidability**: Every query terminates
2. **Enable explanation**: Every conclusion has a traceable proof
3. **Support auditing**: No hidden inference steps
4. **Allow implementation**: Standard Prolog suffices

#### 3.6.3 When These Limitations Matter

| Use Case | Limitation Impact | Mitigation |
|----------|-------------------|------------|
| Contract analysis | Low | Most contracts use simple modalities |
| Regulatory compliance | Low | Regulations are typically first-order |
| Policy conflict detection | Low | Conflicts are first-order patterns |
| Legal meta-reasoning | Medium | May need V3.0 capabilities |
| Norm evolution analysis | High | Requires SOL or external tooling |

### 3.7 Upgrade Paths

MDRE's architecture allows future extension without breaking changes.

#### 3.7.1 Path to Second-Order Logic (V3.0)

For use cases requiring SOL expressiveness:

```
V1.3 Architecture:
┌─────────────────────────────────────┐
│           Tau.js (FOL)              │
│  • Ground facts                     │
│  • First-order rules                │
│  • Decidable queries                │
└─────────────────────────────────────┘

V3.0 Architecture (Proposed):
┌─────────────────────────────────────┐
│        Hybrid Reasoner              │
├─────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  │
│  │  Tau.js     │  │  SOL Solver  │  │
│  │  (FOL core) │◀─│  (fragments) │  │
│  └─────────────┘  └──────────────┘  │
│         │                │          │
│         └────────┬───────┘          │
│                  ▼                  │
│         ┌──────────────┐            │
│         │ Orchestrator │            │
│         └──────────────┘            │
└─────────────────────────────────────┘
```

Candidate SOL fragments for V3.0:
- **Monadic SOL**: Decidable, sufficient for norm classification
- **Guarded SOL**: Decidable fragment with restricted quantification
- **Henkin semantics**: General models, more tractable than full SOL

#### 3.7.2 Path to Hybrid Reasoning

For use cases requiring specialized solvers:

| Capability | External Solver | Integration Pattern |
|------------|-----------------|---------------------|
| Temporal constraints | Allen's algebra solver | Call-out from Tau.js |
| Arithmetic constraints | SMT solver (Z3) | Constraint delegation |
| Probabilistic inference | Bayesian network | Parallel computation |
| Ontology reasoning | OWL reasoner (HermiT) | Import/export |

#### 3.7.3 Compatibility Guarantees

Extensions will maintain:
1. **Backward compatibility**: V1.3 queries work unchanged
2. **Graceful degradation**: Unknown constructs produce informative errors
3. **Explicit opt-in**: New capabilities require explicit activation
4. **Provenance preservation**: Extended reasoning still produces provenance

### 3.8 Formal Semantics Summary

#### 3.8.1 Language Definition

**Syntax:**
```
Term      := Constant | Variable | f(Term, ...)
Atom      := p(Term, ...)
Literal   := Atom | ¬Atom
Clause    := Atom :- Literal, ..., Literal
Query     := ?- Literal, ..., Literal
```

**Sorts:**
- Every term has a sort
- Predicate arguments are sort-restricted
- Sort violations are static errors

**Semantics:**
- Standard Herbrand interpretation
- Minimal model semantics for negation
- Stratified evaluation order

#### 3.8.2 Modal Predicate Axioms

The modal predicates satisfy these axioms (not enforced, but expected):

```prolog
% Deontic consistency (conflict = violation of this)
deontic_inconsistency(E) :-
    obligatory(E, _, _),
    forbidden(E, _, _).

% Obligation implies permission (defeasible)
permitted(E, N, A) :-
    obligatory(E, N, A),
    \+ explicitly_not_permitted(E, N, A).

% Actuality implies possibility
possible(E) :-
    actual(E, _).
```

#### 3.8.3 Soundness and Completeness

- **Soundness**: Every derived fact follows from the rules and base facts
- **Completeness**: Within the decidable fragment, all derivable facts are found
- **Termination**: All queries terminate within configured bounds

---

## 4. Formal Ontology

### 3.1 Entity Declarations

Entity predicates declare existence within the discourse model, not existence in reality.

```prolog
% Core entity types
person(P).              % A person mentioned in discourse
organization(O).        % An organization mentioned
artifact(A).            % An object or artifact mentioned
act(E).                 % An action or event described
role(R).                % An institutional or functional role
document(D).            % A source document
norm(N).                % A normative statement
mention(M).             % A specific textual mention (for entity resolution)
```

**UI Semantics:** "These are entities currently represented in the reasoning model."  
*Not:* "These exist in reality."

### 3.2 Provenance Relations

Every asserted fact must include provenance linking it to source text.

```prolog
% Primary provenance predicate (with confidence)
derived_from(Entity, TextHash, Source, Timestamp, Confidence).

% Inference provenance (with calculated confidence)
inferred_from(Conclusion, Premises, Rule, Timestamp, Confidence).

% Source metadata
source_metadata(Source, Type, Authority, AccessDate, TrustLevel).

% Source typing
source_type(Source, Type).  % document | utterance | attestation | record | observation
```

### 3.3 Event Structure (Davidsonian)

MDRE employs Davidsonian event semantics, reifying events as first-class entities with thematic role attachments.

```prolog
% Thematic roles
agent(Event, Actor).
theme(Event, Object).
recipient(Event, Target).
instrument(Event, Tool).
location(Event, Place).
time_ref(Event, Temporal).      % Renamed from time/2 to avoid conflicts
```

**UI Semantics:** "If this act were realized, these would be the participants."

### 3.4 Role-Qualified Agency

```prolog
% Role-qualified agency
agent_qua_role(Event, Actor, Role).

% Role assignment
holds_role(Actor, Role, Context).
role_authority(Role, Permission, Scope).

% Role activation
role_active(Actor, Role, Event).
```

---

## 5. Confidence Bridging Protocol

> **V1.2 Addition:** This section defines how probabilistic extractions from TagTeam become logical assertions in Tau.js.

### 4.1 The Probabilistic-Deterministic Mismatch

**Problem:** TagTeam outputs confidence scores (0.0-1.0), but Prolog operates on binary logic (succeeds/fails). A naive approach that ignores confidence can propagate extraction errors into logical conclusions.

**Risk Example:** If "shall not" is extracted as "shall" with 60% confidence, the system would enforce the opposite of the text's intent.

### 4.2 Assertion Categories

MDRE introduces three assertion categories based on extraction confidence:

```prolog
% Assertion categories
promoted_fact(Fact).        % High confidence, fully asserted
candidate_fact(Fact).       % Medium confidence, requires review
rejected_fact(Fact).        % Low confidence, not asserted
```

### 4.3 Confidence Thresholds

| Threshold | Value | Result | Action Required |
|-----------|-------|--------|-----------------|
| High | ≥ 0.90 | `promoted_fact` | Auto-promotion to knowledge base |
| Medium | 0.70 - 0.89 | `candidate_fact` | Staged for Tier 2+ review |
| Low | < 0.70 | `rejected_fact` | Logged but not asserted |

**Configuration:** Thresholds are deployment-configurable but defaults are conservative.

```prolog
% Threshold configuration
confidence_threshold(promotion, 0.90).
confidence_threshold(candidacy, 0.70).
confidence_threshold(rejection, 0.70).  % Below this = rejected
```

### 4.4 The Confidence Bridge Process

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   TagTeam   │────▶│ Confidence Bridge │────▶│     Tau.js      │
│ (extraction)│     │   (categorization)│     │ (logical KB)    │
└─────────────┘     └──────────────────┘     └─────────────────┘
      │                      │                        │
      │                      ▼                        │
      │              ┌──────────────┐                │
      │              │  Candidate   │                │
      │              │    Queue     │◀───────────────┘
      │              └──────────────┘      (queries for
      │                      │             review status)
      │                      ▼
      │              ┌──────────────┐
      │              │  Human       │
      │              │  Review (T2+)│
      │              └──────────────┘
```

### 4.5 Candidate Staging

Extractions below the promotion threshold but above rejection are staged as candidates:

```prolog
% Candidate staging
candidate(FactID, Fact, Confidence, Source, Timestamp, Status).
candidate_status(pending).
candidate_status(under_review).
candidate_status(promoted).
candidate_status(rejected).

% Candidate lifecycle
stage_candidate(Fact, Confidence, Source) :-
    confidence_threshold(promotion, PromoteThresh),
    confidence_threshold(candidacy, CandidateThresh),
    Confidence < PromoteThresh,
    Confidence >= CandidateThresh,
    generate_id(FactID),
    get_time(Now),
    assertz(candidate(FactID, Fact, Confidence, Source, Now, pending)).

% Promotion by reviewer
promote_candidate(FactID, Reviewer) :-
    candidate(FactID, Fact, Confidence, Source, _, pending),
    user_tier(Reviewer, Tier),
    Tier >= 2,
    retract(candidate(FactID, Fact, Confidence, Source, _, pending)),
    assertz(candidate(FactID, Fact, Confidence, Source, _, promoted)),
    assertz(Fact),
    assertz(promoted_by(Fact, Reviewer, human_review)).
```

### 4.6 Confidence Propagation in Inference

When facts are combined through inference, confidence propagates:

```prolog
% Confidence calculation for inference
% Using minimum confidence (conservative) or product (probabilistic)

infer_with_confidence(Conclusion, Premises, Rule, Method) :-
    maplist(get_confidence, Premises, Confidences),
    calculate_joint_confidence(Confidences, Method, JointConf),
    get_time(Now),
    assertz(inferred_from(Conclusion, Premises, Rule, Now, JointConf)),
    assertz(Conclusion).

% Calculation methods
calculate_joint_confidence(Confs, minimum, Result) :-
    min_list(Confs, Result).

calculate_joint_confidence(Confs, product, Result) :-
    foldl([C, Acc, NewAcc]>>(NewAcc is Acc * C), Confs, 1.0, Result).

calculate_joint_confidence(Confs, geometric_mean, Result) :-
    length(Confs, N),
    foldl([C, Acc, NewAcc]>>(NewAcc is Acc * C), Confs, 1.0, Product),
    Result is Product ** (1/N).
```

### 4.7 Low-Confidence Chain Flagging

Inference chains that drop below a confidence floor are flagged:

```prolog
% Flag low-confidence conclusions
confidence_floor(0.50).

low_confidence_conclusion(Conclusion) :-
    inferred_from(Conclusion, _, _, _, Conf),
    confidence_floor(Floor),
    Conf < Floor.

% Query for flagged conclusions
?- low_confidence_conclusion(C), inferred_from(C, Premises, Rule, _, Conf).
% Returns conclusions that should be treated with caution
```

### 4.8 UI Integration for Confidence

The UI must surface confidence at every level:

| Element | Confidence Display |
|---------|-------------------|
| Extracted facts | Confidence badge (green ≥0.9, yellow 0.7-0.9, red <0.7) |
| Inferred conclusions | Joint confidence + "derived from N premises" |
| Candidate queue | Sortable by confidence, age, source |
| Query results | Minimum confidence in result chain |

---

## 6. Entity Resolution Layer

> **V1.2 Addition:** This section addresses cross-document coreference—determining when mentions in different documents refer to the same entity.

### 5.1 The Cross-Document Identity Problem

**Problem:** Documents may refer to the same entity using different terms:
- Doc A: "The Buyer must pay..."
- Doc B: "Smith Corp shall transfer funds..."

Without entity resolution, MDRE cannot determine if Smith Corp fulfilling its obligation satisfies the Buyer's requirement.

### 5.2 Mention vs. Entity Architecture

MDRE distinguishes between **mentions** (textual references) and **entities** (resolved discourse objects):

```prolog
% Mention: A specific textual reference
mention(MentionID, Text, Source, Position, EntityType).

% Entity: A resolved discourse object (may have multiple mentions)
entity(EntityID, Type, CanonicalName).

% Mention-to-entity mapping
mention_of(MentionID, EntityID, ResolutionMethod, Confidence).

% Resolution methods
resolution_method(exact_match).
resolution_method(alias_match).
resolution_method(coreference).
resolution_method(manual_link).
resolution_method(external_authority).
```

### 5.3 The `same_as` Predicate

Cross-document identity is explicitly asserted, never assumed:

```prolog
% Identity assertion with evidence
same_as(Entity1, Entity2, Evidence, Confidence, Asserter).

% Evidence types for identity claims
identity_evidence_type(textual_alias).       % "Buyer" and "Smith Corp" declared equivalent in text
identity_evidence_type(external_registry).   % Both resolve to same ID in external system
identity_evidence_type(manual_assertion).    % Human reviewer asserted equivalence
identity_evidence_type(coreference_model).   % NLP coreference resolution

% Symmetry and transitivity (derived, not assumed)
same_as_symmetric(E1, E2, Ev, C, A) :- same_as(E1, E2, Ev, C, A).
same_as_symmetric(E1, E2, Ev, C, A) :- same_as(E2, E1, Ev, C, A).

same_as_transitive(E1, E3, transitive_closure, MinC, system) :-
    same_as_symmetric(E1, E2, _, C1, _),
    same_as_symmetric(E2, E3, _, C2, _),
    E1 \= E3,
    MinC is min(C1, C2).
```

### 5.4 Entity Resolution Strategies

#### 5.4.1 Automatic Resolution (High Confidence)

```prolog
% Exact string match within same document type
auto_resolve_exact(Mention1, Mention2) :-
    mention(Mention1, Text, _, _, Type),
    mention(Mention2, Text, _, _, Type),
    Mention1 \= Mention2,
    assertz(same_as(Mention1, Mention2, exact_match, 0.99, system)).

% Alias table match
alias(Canonical, Alias).
% e.g., alias('Smith Corporation', 'Smith Corp').

auto_resolve_alias(Mention1, Mention2) :-
    mention(Mention1, Text1, _, _, _),
    mention(Mention2, Text2, _, _, _),
    alias(Canonical, Text1),
    alias(Canonical, Text2),
    Mention1 \= Mention2,
    assertz(same_as(Mention1, Mention2, alias_match, 0.95, system)).
```

#### 5.4.2 Suggested Resolution (Medium Confidence)

```prolog
% NLP coreference model suggestions
coreference_suggestion(Mention1, Mention2, ModelConfidence) :-
    mention(Mention1, _, Source1, _, Type),
    mention(Mention2, _, Source2, _, Type),
    Source1 = Source2,  % Same document
    nlp_coreference(Mention1, Mention2, ModelConfidence).

% Stage for review if below threshold
stage_coreference_candidate(M1, M2, Conf) :-
    coreference_suggestion(M1, M2, Conf),
    confidence_threshold(promotion, Thresh),
    Conf < Thresh,
    assertz(resolution_candidate(M1, M2, coreference_model, Conf, pending)).
```

#### 5.4.3 Manual Resolution (Tier 2+ UI)

The UI provides a "Linker" interface where Analysts can:

1. View unresolved mentions grouped by entity type
2. See suggested matches with confidence scores
3. Drag-and-drop to assert `same_as` relationships
4. Provide evidence justification for manual links

```prolog
% Manual resolution by reviewer
manual_resolve(Mention1, Mention2, Justification, Reviewer) :-
    user_tier(Reviewer, Tier),
    Tier >= 2,
    assertz(same_as(Mention1, Mention2, 
                    manual_assertion(Justification), 
                    1.0,  % Human review = full confidence
                    Reviewer)).
```

### 5.5 External Authority Integration

For regulated domains, entities may be resolved against external registries:

```prolog
% External identifier mapping
external_id(EntityID, Registry, ExternalID).
% e.g., external_id(entity_001, lei, '549300EXAMPLE000001').

% Resolution via external authority
resolve_via_registry(Mention1, Mention2, Registry) :-
    mention_of(Mention1, E1, _, _),
    mention_of(Mention2, E2, _, _),
    external_id(E1, Registry, ExtID),
    external_id(E2, Registry, ExtID),
    E1 \= E2,
    assertz(same_as(E1, E2, external_registry(Registry, ExtID), 0.99, system)).
```

### 5.6 Entity Resolution in Obligation Fulfillment

With entity resolution, MDRE can track cross-document obligation fulfillment:

```prolog
% Obligation fulfillment across documents
obligation_potentially_fulfilled(Obligation, FulfillingAct) :-
    obligatory(Obligation, _, _),
    agent_qua_role(Obligation, Obligor, _),
    actual(FulfillingAct, Evidence),
    agent_qua_role(FulfillingAct, Fulfiller, _),
    (Obligor = Fulfiller ; same_as_symmetric(Obligor, Fulfiller, _, _, _)),
    act_type_matches(Obligation, FulfillingAct).
```

### 5.7 UI: Entity Resolution Dashboard

| Section | Function |
|---------|----------|
| **Unresolved Mentions** | List of mentions not yet linked to entities |
| **Resolution Candidates** | Suggested matches with confidence scores |
| **Entity Graph** | Visual representation of resolved entities and their mentions |
| **Conflict Warnings** | Alerts when resolution would create logical conflicts |

---

## 7. Modal and Deontic Predicates

### 6.1 Ontological Status of Modal Predicates

> **Clarification:** In MDRE, modal predicates are *logical encodings* of normative information entities, not direct ontological assertions.

From a BFO perspective, the modal predicates encode information that would be classified as **Generically Dependent Continuants** (specifically, Information Content Entities). The predicates themselves are computational representations of that information content.

### 6.2 Alethic Modalities

```prolog
% Alethic modal predicates
actual(E, Evidence).        % Asserted as having occurred (requires evidence tier)
hypothetical(E).            % Proposed but not asserted as actual
counterfactual(E).          % Contrary to what is asserted
possible(E).                % Consistent with what is known
impossible(E).              % Inconsistent with what is known
necessary(E).               % Follows necessarily from premises

% V1.2: Claimed actuality (for self-reports)
claimed_actual(E, Claimant, ClaimSource).  % Claimed but not verified
```

**Note:** `actual/1` (without evidence) is deprecated. All actuality claims require explicit evidence via `actual/2` meeting evidence tier requirements (see §7).

### 6.3 Deontic Modalities

```prolog
% Basic deontic predicates (detection/query use)
obligatory(E).
permitted(E).
forbidden(E).
optional(E).

% Qualified deontic predicates (full reasoning)
obligatory(E, Norm, Authority).
permitted(E, Norm, Authority).
forbidden(E, Norm, Authority).

% With confidence (V1.2)
obligatory(E, Norm, Authority, Confidence).
permitted(E, Norm, Authority, Confidence).
forbidden(E, Norm, Authority, Confidence).
```

### 6.4 Realization Tracking

```prolog
% Realization predicates
realized(E, Evidence, Timestamp).
violated(E, Evidence, Timestamp).
expired(E, Timestamp).
pending(E).

% Derived status
fulfilled(Obligation) :-
    obligatory(Obligation, _, _),
    realized(Obligation, _, _),
    \+ violated(Obligation, _, _).

breached(Obligation) :-
    obligatory(Obligation, _, _),
    violated(Obligation, _, _).
```

---

## 8. Evidence Tier System

> **V1.2 Addition:** This section prevents "evidence injection" attacks where malicious actors submit self-authored reports to assert actuality.

### 7.1 The Evidence Loophole Problem

**Problem:** If `actual(E, Evidence)` can be asserted from any evidence type, a user could submit a document stating "I paid the bill" and MDRE would accept this as evidence of actual payment.

**Risk:** Self-authored attestations could inject false "truths" into the knowledge base.

### 7.2 Evidence Tier Hierarchy

MDRE defines a strict hierarchy of evidence types with different assertion permissions:

| Tier | Evidence Type | Can Assert `actual/2` | Can Assert `claimed_actual/3` | Trust Requirement |
|------|--------------|----------------------|------------------------------|-------------------|
| 1 | `observation` | Yes | Yes | Verified observer |
| 2 | `record` | Yes | Yes | Official record source |
| 3 | `attestation` | **No** | Yes | Identified attestor |
| 4 | `report` | **No** | Yes | Known reporter |
| 5 | `claim` | **No** | Yes | Any source |

### 7.3 Evidence Type Definitions

```prolog
% Evidence type hierarchy
evidence_tier(observation, 1).
evidence_tier(record, 2).
evidence_tier(attestation, 3).
evidence_tier(report, 4).
evidence_tier(claim, 5).

% Evidence type definitions
evidence_type_def(observation, 
    "Direct observation by a verified observer with no interest in the outcome").
evidence_type_def(record,
    "Official record from an authoritative source (court filing, government database, etc.)").
evidence_type_def(attestation,
    "Formal statement by an identified party, potentially with interest in the outcome").
evidence_type_def(report,
    "Third-party report without official status").
evidence_type_def(claim,
    "Unverified claim from any source").
```

### 7.4 Evidence Assertion Rules

```prolog
% Evidence structure
evidence(EvidenceID, Type, Source, Content, Timestamp, TrustLevel).

% Assertion permission rules
can_assert_actual(EvidenceID) :-
    evidence(EvidenceID, Type, Source, _, _, TrustLevel),
    evidence_tier(Type, Tier),
    Tier =< 2,  % Only observation and record
    TrustLevel >= trusted.

% Attempting to assert actual from lower-tier evidence
assert_actual(Event, EvidenceID) :-
    can_assert_actual(EvidenceID),
    !,
    assertz(actual(Event, EvidenceID)).

assert_actual(Event, EvidenceID) :-
    evidence(EvidenceID, Type, Source, _, _, _),
    \+ can_assert_actual(EvidenceID),
    assertz(claimed_actual(Event, Source, EvidenceID)),
    log_warning(actual_assertion_downgraded, Event, EvidenceID, Type).
```

### 7.5 The `claimed_actual` Predicate

For evidence that doesn't meet the `actual/2` threshold:

```prolog
% Claimed actuality (not verified)
claimed_actual(Event, Claimant, EvidenceSource).

% Query distinction
?- actual(E, _).           % Verified occurrences only
?- claimed_actual(E, _, _). % Unverified claims
?- (actual(E, _) ; claimed_actual(E, _, _)).  % All assertions of occurrence
```

### 7.6 Evidence Source Trust Levels

```prolog
% Trust levels for sources
trust_level(verified).      % Independently verified source
trust_level(trusted).       % Known reliable source
trust_level(provisional).   % Source under evaluation
trust_level(untrusted).     % Unknown or unreliable source

% Source trust assignment (deployment-configured)
source_trust(Source, TrustLevel) :-
    source_metadata(Source, _, _, _, TrustLevel).

% Default trust for unknown sources
source_trust(Source, provisional) :-
    \+ source_metadata(Source, _, _, _, _).
```

### 7.7 Evidence Chain for Actuality

When querying actuality, the full evidence chain is available:

```prolog
% Full evidence chain query
actual_with_evidence_chain(Event, Chain) :-
    actual(Event, EvidenceID),
    evidence(EvidenceID, Type, Source, Content, Time, Trust),
    source_metadata(Source, SourceType, Authority, _, _),
    Chain = chain{
        event: Event,
        evidence_id: EvidenceID,
        evidence_type: Type,
        evidence_tier: Tier,
        source: Source,
        source_type: SourceType,
        authority: Authority,
        trust_level: Trust,
        timestamp: Time
    },
    evidence_tier(Type, Tier).
```

### 7.8 UI: Evidence Indicators

| Indicator | Meaning |
|-----------|---------|
| ✓✓ (double check) | `actual/2` from Tier 1-2 evidence |
| ✓ (single check) | `claimed_actual/3` from Tier 3-5 evidence |
| ⚠️ (warning) | Actuality claim from untrusted source |
| ❓ (question) | No actuality assertion exists |

---

## 9. Temporal Semantics

### 8.1 Temporal Complexity Constraints

> **V1.2 Addition:** This section defines performance bounds for temporal reasoning.

**Problem:** Full Allen's Interval Algebra in Tau.js (JavaScript Prolog) is computationally expensive—O(n²) or worse with constraint propagation.

**Risk:** Deeply nested temporal clauses could cause unacceptable query latency.

### 8.2 V1.2 Temporal Scope

For V1.2, temporal reasoning is limited to:

| Supported | Not Supported (Deferred to V2.0) |
|-----------|----------------------------------|
| Point comparisons (`before`, `after`) | Full interval algebra |
| Duration calculations | Constraint propagation |
| Simple containment (`during`) | Complex interval compositions |
| Deadline checking | Temporal constraint satisfaction |

### 8.3 Point-Based Temporal Model

```prolog
% Time point representation
time_point(PointID, ISO8601String, Granularity).

% Granularity levels
granularity_level(instant).     % Precise moment
granularity_level(day).         % Day-level
granularity_level(week).        % Week-level
granularity_level(month).       % Month-level
granularity_level(year).        % Year-level

% Point comparisons (O(1) operations)
before(T1, T2) :-
    time_point(T1, ISO1, _),
    time_point(T2, ISO2, _),
    ISO1 @< ISO2.

after(T1, T2) :- before(T2, T1).

same_time(T1, T2) :-
    time_point(T1, ISO, _),
    time_point(T2, ISO, _).
```

### 8.4 Duration-Based Reasoning

```prolog
% Duration representation
duration(days(N)).
duration(weeks(N)).
duration(months(N)).
duration(years(N)).

% Duration calculation
duration_between(T1, T2, Duration) :-
    time_point(T1, ISO1, _),
    time_point(T2, ISO2, _),
    parse_iso(ISO1, Stamp1),
    parse_iso(ISO2, Stamp2),
    Diff is Stamp2 - Stamp1,
    Duration = seconds(Diff).

% Deadline checking
deadline_passed(Deadline) :-
    time_point(Deadline, DeadlineISO, _),
    get_current_time(NowISO),
    NowISO @> DeadlineISO.

deadline_approaching(Deadline, WithinDuration) :-
    time_point(Deadline, DeadlineISO, _),
    get_current_time(NowISO),
    NowISO @< DeadlineISO,
    duration_between(now, Deadline, Remaining),
    duration_less_than(Remaining, WithinDuration).
```

### 8.5 Temporally Bounded Obligations

```prolog
% Temporally bounded obligations
obligatory_before(E, Deadline).
obligatory_after(E, StartTime).
obligatory_within(E, Duration, TriggerEvent).

% Deadline status
obligation_overdue(Obligation) :-
    obligatory_before(Obligation, Deadline),
    deadline_passed(Deadline),
    \+ realized(Obligation, _, _).

obligation_upcoming(Obligation, TimeRemaining) :-
    obligatory_before(Obligation, Deadline),
    \+ deadline_passed(Deadline),
    duration_between(now, Deadline, TimeRemaining).
```

### 8.6 Temporal Query Performance Bounds

```prolog
% Performance constraints
max_temporal_constraints(1000).  % Per query
temporal_query_timeout_ms(5000). % 5 second timeout

% Bounded temporal query
bounded_temporal_query(Query, Results) :-
    count_temporal_constraints(Query, Count),
    max_temporal_constraints(Max),
    Count =< Max,
    call_with_timeout(Query, Results, temporal_query_timeout_ms(_)).

bounded_temporal_query(Query, error(too_many_constraints)) :-
    count_temporal_constraints(Query, Count),
    max_temporal_constraints(Max),
    Count > Max.
```

### 8.7 Allen's Interval Algebra (V2.0 Preview)

For V2.0, the following will be implemented via a specialized constraint solver:

```prolog
% V2.0: Full Allen relations (not in V1.2)
% allen_before(I1, I2).
% allen_meets(I1, I2).
% allen_overlaps(I1, I2).
% allen_starts(I1, I2).
% allen_during(I1, I2).
% allen_finishes(I1, I2).
% allen_equals(I1, I2).
```

---

## 10. Inference Rules and Conflict Resolution

### 9.1 Conflict Taxonomy

MDRE distinguishes between conflict *detection*, conflict *analysis*, and conflict *resolution*.

```prolog
% Conflict type classification
conflict_type(direct_modal).     % obligatory(E) ∧ forbidden(E)
conflict_type(resource).         % Two obligations that cannot both be fulfilled
conflict_type(priority).         % Different authorities with conflicting norms
conflict_type(conditional).      % Obligations conflict under certain conditions
conflict_type(temporal).         % Obligations with incompatible time constraints
```

### 9.2 Conflict Detection

Detection rules identify potential conflicts without resolving them:

```prolog
% Direct modal conflict detection
modal_conflict(E, Norm1, Norm2) :-
    obligatory(E, Norm1, Auth1),
    forbidden(E, Norm2, Auth2).

% Resource conflict detection
resource_conflict(E1, E2) :-
    obligatory(E1, _, _),
    obligatory(E2, _, _),
    mutually_exclusive(E1, E2).

% Priority conflict detection (V1.2: handles undefined relationships)
priority_conflict(E, Norm1, Norm2, Reason) :-
    obligatory(E, Norm1, Auth1),
    forbidden(E, Norm2, Auth2),
    \+ authority_comparable(Auth1, Auth2),
    Reason = no_authority_ordering.

priority_conflict(E, Norm1, Norm2, Reason) :-
    obligatory(E, Norm1, Auth1),
    forbidden(E, Norm2, Auth2),
    authority_comparable(Auth1, Auth2),
    authority_equal(Auth1, Auth2),
    Reason = equal_authority.

% Authority comparability check (V1.2 addition)
authority_comparable(Auth1, Auth2) :-
    (authority_ordering(Auth1, Auth2) ; 
     authority_ordering(Auth2, Auth1) ;
     authority_equal(Auth1, Auth2)).
```

### 9.3 Dynamic Priority Calculus

> **V1.2 Enhancement:** Priority is no longer a static integer but a dynamic calculation incorporating specificity.

**Problem:** Static authority levels (statute: 80, regulation: 60) ignore the *lex specialis* principle—a specific regulation often overrides a general statute.

**Solution:** Priority is calculated dynamically from multiple factors.

```prolog
% Priority factors
priority_factor(authority_level).
priority_factor(specificity).
priority_factor(recency).
priority_factor(explicit_override).

% Base authority levels (still relevant but not determinative)
source_authority_base(constitution, 100).
source_authority_base(statute, 80).
source_authority_base(regulation, 60).
source_authority_base(contract, 40).
source_authority_base(policy, 20).

% Specificity scoring
norm_specificity(Norm, Score) :-
    count_conditions(Norm, CondCount),
    count_named_entities(Norm, EntityCount),
    count_temporal_bounds(Norm, TemporalCount),
    Score is (CondCount * 10) + (EntityCount * 5) + (TemporalCount * 3).

% Recency factor
norm_recency_factor(Norm, Factor) :-
    norm_enacted(Norm, EnactedTime),
    get_current_time(Now),
    time_difference_years(EnactedTime, Now, Years),
    Factor is max(0, 10 - Years).  % More recent = higher factor

% Dynamic priority calculation
calculate_priority(Norm, Priority) :-
    norm_source(Norm, Source),
    source_authority_base(Source, BaseAuth),
    norm_specificity(Norm, Specificity),
    norm_recency_factor(Norm, Recency),
    (explicit_override(Norm, _, Bonus) -> OverrideBonus = Bonus ; OverrideBonus = 0),
    Priority is BaseAuth + (Specificity * 2) + Recency + OverrideBonus.
```

### 9.4 Lex Specialis Implementation

```prolog
% Lex specialis: specific overrides general IF hierarchically consistent
lex_specialis_applies(SpecificNorm, GeneralNorm) :-
    norm_specificity(SpecificNorm, SpecScore),
    norm_specificity(GeneralNorm, GenScore),
    SpecScore > GenScore,
    hierarchically_consistent(SpecificNorm, GeneralNorm).

% Hierarchical consistency check
% A regulation can specialize a statute, but not contradict constitutional principles
hierarchically_consistent(LowerNorm, HigherNorm) :-
    norm_source(LowerNorm, LowerSource),
    norm_source(HigherNorm, HigherSource),
    source_authority_base(LowerSource, LowerBase),
    source_authority_base(HigherSource, HigherBase),
    LowerBase =< HigherBase,
    \+ contradicts_principle(LowerNorm, HigherNorm).

% Explicit contradictions cannot be overridden by specificity
contradicts_principle(Norm1, Norm2) :-
    norm_principle(Norm2, Principle),
    principle_inviolable(Principle),
    norm_violates_principle(Norm1, Principle).
```

### 9.5 Conflict Resolution with Dynamic Priority

```prolog
% Resolution using dynamic priority
resolve_conflict(ConflictID, PrevailingNorm, Method) :-
    detected_conflict(ConflictID, _, [Norm1, Norm2]),
    resolve_by_lex_specialis(Norm1, Norm2, Winner, lex_specialis),
    PrevailingNorm = Winner,
    Method = lex_specialis.

resolve_conflict(ConflictID, PrevailingNorm, Method) :-
    detected_conflict(ConflictID, _, [Norm1, Norm2]),
    \+ resolve_by_lex_specialis(Norm1, Norm2, _, _),
    resolve_by_dynamic_priority(Norm1, Norm2, Winner),
    PrevailingNorm = Winner,
    Method = dynamic_priority.

% Lex specialis resolution
resolve_by_lex_specialis(Norm1, Norm2, Norm1, lex_specialis) :-
    lex_specialis_applies(Norm1, Norm2).
resolve_by_lex_specialis(Norm1, Norm2, Norm2, lex_specialis) :-
    lex_specialis_applies(Norm2, Norm1).

% Dynamic priority resolution
resolve_by_dynamic_priority(Norm1, Norm2, Winner) :-
    calculate_priority(Norm1, P1),
    calculate_priority(Norm2, P2),
    P1 > P2,
    Winner = Norm1.
resolve_by_dynamic_priority(Norm1, Norm2, Winner) :-
    calculate_priority(Norm1, P1),
    calculate_priority(Norm2, P2),
    P2 > P1,
    Winner = Norm2.
```

### 9.6 Unresolvable Conflicts

When priorities are equal and no lex specialis applies:

```prolog
% Equal priority = unresolvable without human input
unresolvable_conflict(ConflictID, Reason) :-
    detected_conflict(ConflictID, _, [Norm1, Norm2]),
    calculate_priority(Norm1, P),
    calculate_priority(Norm2, P),
    \+ lex_specialis_applies(Norm1, Norm2),
    \+ lex_specialis_applies(Norm2, Norm1),
    Reason = equal_priority_no_specialis.

unresolvable_conflict(ConflictID, Reason) :-
    priority_conflict(_, Norm1, Norm2, no_authority_ordering),
    detected_conflict(ConflictID, _, [Norm1, Norm2]),
    Reason = incomparable_authorities.
```

### 9.7 Open-World Negation

MDRE explicitly rejects closed-world negation:

```prolog
% Explicit negation required
not_permitted(E) :-
    explicitly_denied(E, Norm, Authority).

% Unknown status (open world)
permission_unknown(E) :-
    \+ permitted(E, _, _),
    \+ forbidden(E, _, _).
```

**Critical Distinction:** "No prohibition found" ≠ "This is permitted."

---

## 11. Query System

### 10.1 Query Classification

| Query Class | Description | Preconditions | Permissibility |
|-------------|-------------|---------------|----------------|
| Inventory | What entities are in scope? | None | Always |
| Modal Status | What is obligatory/permitted/forbidden? | None | Always |
| Responsibility | Who must do what? | None | Always |
| Provenance | Why is this required? | None | Always |
| Confidence | What is the confidence chain? | None | Always |
| Conflict | Are there contradictions? | None | Always |
| Resolution | How is this conflict resolved? | Conflict must exist | Conditional |
| Entity Resolution | Are these the same entity? | None | Always |
| Actuality | Did this happen? | Evidence tier ≤ 2 | Conditional |
| Claimed Actuality | What is claimed to have happened? | None | Always |
| World-Truth | Does X exist in reality? | Never satisfiable | Never |

### 10.2 Confidence-Aware Queries

```prolog
% Query with minimum confidence threshold
query_with_confidence(Query, MinConfidence, Results) :-
    findall(
        result(Bindings, Conf),
        (call(Query), get_result_confidence(Query, Conf), Conf >= MinConfidence),
        Results
    ).

% Get confidence for a result
get_result_confidence(Query, Conf) :-
    extract_facts(Query, Facts),
    maplist(fact_confidence, Facts, Confidences),
    min_list(Confidences, Conf).

fact_confidence(Fact, Conf) :-
    derived_from(Fact, _, _, _, Conf).
fact_confidence(Fact, Conf) :-
    inferred_from(Fact, _, _, _, Conf).
fact_confidence(Fact, 1.0) :-
    \+ derived_from(Fact, _, _, _, _),
    \+ inferred_from(Fact, _, _, _, _).  % Built-in facts
```

### 10.3 Entity Resolution Queries

```prolog
% Are two mentions the same entity?
?- same_as(mention_001, mention_002, Evidence, Conf, _).

% All mentions of an entity
?- same_as_closure(mention_001, AllMentions).

% Unresolved mentions
?- mention(M, _, _, _, _), \+ mention_of(M, _, _, _).
```

### 10.4 Non-Permissible Queries

**Examples of non-permissible queries:**
- "Did this really happen?" — Requires verification beyond discourse
- "Does this person exist?" — Requires metaphysical claims
- "What is the true obligation?" — Assumes objective moral facts

**System Response:**
> "This query requires information beyond the discourse model. MDRE represents what has been stated or inferred from provided text, not independent facts about the world."

---

## 12. User Interface Semantics

### 11.1 User Tier Model

| Tier | Name | Access Level | Use Case |
|------|------|--------------|----------|
| 1 | Observer | Read-only, templates only | Compliance officers, auditors |
| 2 | Analyst | Templates + visible logic + entity linking + candidate review | Legal analysts, policy researchers |
| 3 | Engineer | Raw Prolog access + custom rules + system configuration | System integrators, developers |

### 11.2 Confidence Visualization

| Confidence Range | Badge | Meaning |
|------------------|-------|---------|
| ≥ 0.90 | 🟢 Green | High confidence, auto-promoted |
| 0.70 - 0.89 | 🟡 Yellow | Medium confidence, candidate |
| < 0.70 | 🔴 Red | Low confidence, rejected |

### 11.3 Entity Resolution Interface (Tier 2+)

**Linker Panel:**
- Unresolved mentions list (sortable by type, source, confidence)
- Suggested matches with confidence scores
- Drag-and-drop linking interface
- Justification text field for manual links
- Undo/history for resolution actions

### 11.4 Candidate Review Queue (Tier 2+)

**Queue Panel:**
- Pending candidates sorted by confidence (ascending = most uncertain first)
- Source text preview with highlighted extraction
- Promote/Reject buttons
- Batch operations for similar extractions

### 11.5 Confidence Chain Visualization

For any displayed fact, users can expand to see:
```
Conclusion (confidence: 0.82)
├── Premise 1 (confidence: 0.95) ← derived from Doc A
├── Premise 2 (confidence: 0.88) ← derived from Doc B
└── Rule: responsibility_assignment
    └── Joint confidence: min(0.95, 0.88) = 0.88
        └── × inference discount (0.93) = 0.82
```

---

## 13. Integration Architecture

### 12.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         MDRE System                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌─────────────────┐    ┌──────────────────┐   │
│  │ Documents│───▶│    TagTeam      │───▶│  Confidence      │   │
│  │ (input)  │    │  (extraction)   │    │  Bridge          │   │
│  └──────────┘    │                 │    │                  │   │
│                  │  confidence:0.X │    │  ≥0.9: promote   │   │
│                  └─────────────────┘    │  0.7-0.9: stage  │   │
│                                         │  <0.7: reject    │   │
│                                         └────────┬─────────┘   │
│                                                  │              │
│                    ┌─────────────────────────────┼──────────┐  │
│                    │                             ▼          │  │
│                    │  ┌─────────────────┐  ┌──────────┐    │  │
│                    │  │ Entity          │  │ Candidate│    │  │
│                    │  │ Resolution      │  │ Queue    │    │  │
│                    │  │ Layer           │  └────┬─────┘    │  │
│                    │  └────────┬────────┘       │          │  │
│                    │           │                │          │  │
│                    │           ▼                ▼          │  │
│                    │  ┌─────────────────────────────────┐  │  │
│                    │  │         Tau.js                  │  │  │
│                    │  │    (Prolog Knowledge Base)      │  │  │
│                    │  │                                 │  │  │
│                    │  │  • Promoted facts               │  │  │
│                    │  │  • Entity resolutions           │  │  │
│                    │  │  • Inference rules              │  │  │
│                    │  │  • Conflict detection           │  │  │
│                    │  └─────────────────────────────────┘  │  │
│                    │              Processing Layer         │  │
│                    └───────────────────────────────────────┘  │
│                                         │                     │
│                                         ▼                     │
│                    ┌───────────────────────────────────────┐  │
│                    │           Query Interface             │  │
│                    │  • Typed queries                      │  │
│                    │  • Confidence-aware results           │  │
│                    │  • Provenance chains                  │  │
│                    └───────────────────────────────────────┘  │
│                                         │                     │
└─────────────────────────────────────────┼─────────────────────┘
                                          ▼
                    ┌───────────────────────────────────────┐
                    │              UI Layer                  │
                    │  ┌─────────┐ ┌─────────┐ ┌─────────┐  │
                    │  │Observer │ │ Analyst │ │Engineer │  │
                    │  │ (Tier 1)│ │(Tier 2) │ │(Tier 3) │  │
                    │  └─────────┘ └─────────┘ └─────────┘  │
                    └───────────────────────────────────────┘
```

### 12.2 TagTeam Output Format (V1.2)

```json
{
  "source": {
    "hash": "text_222edc895bb2",
    "text": "The Buyer shall pay the Purchase Price.",
    "document": "contract_v2",
    "timestamp": "2026-01-15T10:30:00Z"
  },
  "extractions": [
    {
      "id": "ext_001",
      "type": "act",
      "predicate": "pay",
      "confidence": 0.94,
      "agent": {
        "mention_id": "mention_001",
        "text": "The Buyer",
        "type": "role",
        "confidence": 0.97
      },
      "theme": {
        "mention_id": "mention_002",
        "text": "the Purchase Price",
        "type": "artifact",
        "confidence": 0.99
      },
      "modality": {
        "type": "deontic",
        "value": "obligatory",
        "marker": "shall",
        "confidence": 0.98
      }
    }
  ],
  "coreference_suggestions": [
    {
      "mention1": "mention_001",
      "mention2": "mention_003",
      "confidence": 0.85,
      "reason": "definite_np_match"
    }
  ],
  "extraction_metadata": {
    "parser_version": "tagteam-2.2.0",
    "extraction_time": "2026-01-15T10:30:05Z",
    "model_confidence_calibration": "isotonic_v2"
  }
}
```

### 12.3 API Specification

#### 12.3.1 Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/ingest` | POST | Submit document for extraction |
| `/api/v1/candidates` | GET | List candidate facts awaiting review |
| `/api/v1/candidates/{id}/promote` | POST | Promote candidate to knowledge base |
| `/api/v1/candidates/{id}/reject` | POST | Reject candidate |
| `/api/v1/entities/resolve` | POST | Assert entity resolution |
| `/api/v1/query` | POST | Execute Prolog query |
| `/api/v1/conflicts` | GET | List detected conflicts |
| `/api/v1/provenance/{id}` | GET | Get provenance chain |

#### 12.3.2 Query Request Format

```json
{
  "query": "obligatory(E), agent_qua_role(E, Actor, Role)",
  "min_confidence": 0.8,
  "include_provenance": true,
  "include_confidence_chain": true,
  "timeout_ms": 5000
}
```

#### 12.3.3 Query Response Format

```json
{
  "success": true,
  "results": [
    {
      "bindings": {
        "E": "act_001",
        "Actor": "buyer_ref",
        "Role": "buyer"
      },
      "confidence": 0.91,
      "confidence_chain": [
        {"fact": "obligatory(act_001, norm_001, contract)", "confidence": 0.94},
        {"fact": "agent_qua_role(act_001, buyer_ref, buyer)", "confidence": 0.97}
      ],
      "provenance": {
        "derived_from": "text_abc123",
        "source": "contract_doc"
      }
    }
  ],
  "warnings": [],
  "query_metadata": {
    "execution_time_ms": 12,
    "result_count": 1,
    "min_result_confidence": 0.91
  }
}
```

---

## 14. Ontological Alignment (BFO/CCO)

### 13.1 BFO Category Mapping

| MDRE Predicate | BFO Category | BFO IRI | Notes |
|----------------|--------------|---------|-------|
| `act(E)` | Process | BFO:0000015 | Occurrents with temporal parts |
| `person(P)` | Object | BFO:0000030 | Independent continuants |
| `organization(O)` | Object Aggregate | BFO:0000027 | Collections of objects |
| `artifact(A)` | Object | BFO:0000030 | Material entities |
| `role(R)` | Role | BFO:0000023 | Realizable entities |
| `norm(N)` | GDC | BFO:0000031 | Information content entities |
| `document(D)` | GDC | BFO:0000031 | Information bearing entities |
| `mention(M)` | GDC | BFO:0000031 | Specific textual reference |

### 13.2 The `references` Predicate (V1.2 Terminology Correction)

> **V1.2 Change:** The predicate `denotes/3` has been replaced with `references/2` to avoid implying that MDRE knows the "real world entity."

**Problem with `denotes`:** The term "denotes" implies a semantic relationship to reality that MDRE cannot verify.

**Solution:** Use `references` to indicate linkage to an external identifier without metaphysical commitment.

```prolog
% V1.1 (deprecated):
% denotes(InformationEntity, RealWorldEntity, Evidence).

% V1.2 (current):
references(InformationEntity, ExternalID).

% External ID structure
external_identifier(ExternalID, Registry, Value).
% e.g., external_identifier(ext_001, lei, '549300EXAMPLE000001').

% The relationship is purely informational
% MDRE does not assert that ExternalID corresponds to a real entity
% Only that the discourse entity is linked to this identifier
```

### 13.3 Information Entity Architecture

MDRE maintains strict separation between information entities and external identifiers:

```prolog
% Information entity (always safe to assert)
information_entity(IE) :-
    derived_from(IE, _, _, _, _).

% External reference (informational linkage only)
has_external_reference(InfoEntity, Registry, ExternalID) :-
    references(InfoEntity, ExtRef),
    external_identifier(ExtRef, Registry, ExternalID).

% This does NOT assert that ExternalID exists in reality
% Only that the discourse mentions something linked to this ID
```

---

## 15. Security and Trust Model

### 14.1 Trust Boundaries

| Source Type | Trust Level | Assertion Permissions |
|-------------|-------------|----------------------|
| Verified Document | High | Full assertion including `actual/2` |
| Official Record | High | `actual/2` with Tier 2 evidence |
| Authenticated User | Medium | `claimed_actual/3`, entity resolution |
| External API | Low | Provisional assertions, flagged |
| Self-Report | Low | `claimed_actual/3` only |
| Unknown | Minimal | Staged as candidate |

### 14.2 Evidence Injection Prevention

The Evidence Tier System (§7) prevents malicious "truth injection":

1. Self-authored documents cannot assert `actual/2`
2. Attestations result in `claimed_actual/3` instead
3. All actuality claims display evidence tier in UI
4. Tier 2+ users can flag suspicious evidence

### 14.3 Audit Trail

```prolog
% Comprehensive audit logging
audit_entry(EntryID, Timestamp, Operation, Subject, Actor, Details).

% Logged operations
audit_operation(fact_promoted).
audit_operation(fact_rejected).
audit_operation(entity_resolved).
audit_operation(conflict_resolved).
audit_operation(evidence_submitted).
audit_operation(query_executed).

% All entries append-only, cryptographically chained
audit_chain(EntryID, PreviousHash, CurrentHash).
```

---

## 16. Performance Constraints and Benchmarks

> **V1.2 Addition:** This section defines performance requirements and testing protocols.

### 15.1 Tau.js Performance Bounds

| Operation | Target Latency | Maximum Latency | Notes |
|-----------|---------------|-----------------|-------|
| Simple query | < 50ms | 200ms | Single predicate, no joins |
| Complex query | < 500ms | 2000ms | Multiple predicates, joins |
| Temporal query | < 200ms | 1000ms | Point comparisons only |
| Conflict detection | < 1000ms | 5000ms | Full scan |
| Entity resolution | < 100ms | 500ms | Per pair |

### 15.2 Constraint Limits

| Constraint | V1.2 Limit | Rationale |
|------------|------------|-----------|
| Temporal constraints per query | 1,000 | Prevent O(n²) explosion |
| Entity resolution candidates | 10,000 | Memory bound |
| Inference chain depth | 10 | Prevent infinite loops |
| Confidence propagation | Product with floor 0.1 | Prevent vanishing confidence |

### 15.3 Benchmark Protocol

Before release, MDRE must pass:

1. **Load Test:** 10,000 facts, 1,000 norms, 100 conflicts
   - All queries complete within bounds
   - No memory leaks over 24-hour run

2. **Temporal Stress Test:** 10,000 temporal constraints
   - Query timeout must trigger, not hang
   - Graceful degradation message

3. **Concurrent Access:** 100 simultaneous users
   - No race conditions in candidate promotion
   - Audit trail integrity maintained

### 15.4 Degradation Strategy

When limits are approached:

```prolog
% Query complexity check
check_query_complexity(Query, Status) :-
    count_predicates(Query, PredCount),
    count_temporal_constraints(Query, TempCount),
    (PredCount > 50 -> Status = warn_complex ;
     TempCount > 500 -> Status = warn_temporal ;
     Status = ok).

% Graceful degradation
execute_with_degradation(Query, Results, Warnings) :-
    check_query_complexity(Query, Status),
    (Status = ok -> 
        execute_query(Query, Results), Warnings = [] ;
     Status = warn_complex ->
        execute_with_timeout(Query, Results, 2000),
        Warnings = [complex_query_may_timeout] ;
     Status = warn_temporal ->
        simplify_temporal(Query, SimpleQuery),
        execute_query(SimpleQuery, Results),
        Warnings = [temporal_constraints_simplified]).
```

---

## 17. Implementation Roadmap

### 17.1 Version History

| Version | Status | Key Features |
|---------|--------|--------------|
| 1.0.0 | Released | Core modal reasoning, provenance, conflict detection |
| 1.1.0 | Released | Conflict taxonomy, user tiers, ontological clarifications |
| 1.2.0 | Released | Confidence bridging, entity resolution, evidence tiers, dynamic priority |
| 1.3.0 | Current | Logical foundations framework, FOL semantics, decidability guarantees |

### 17.2 V1.3 Implementation Checklist

- [ ] Logical Foundations documentation complete
- [ ] Sort hierarchy enforcement in predicate validation
- [ ] Inference depth limiting implementation
- [ ] Quantification semantics documentation
- [ ] Decidability boundary testing
- [ ] Updated developer guide with FOL examples

### 17.3 V2.0 Planned Features

- Full Allen's Interval Algebra (external solver)
- Institutional hierarchy reasoning
- Defeasible logic with explicit defeat
- Multi-party negotiation support
- Cryptographic provenance verification
- Federation across MDRE instances

### 17.4 V3.0 Planned Features (SOL Extensions)

- Hybrid reasoner architecture (see §3.7.1)
- Monadic SOL fragments for norm classification
- SMT solver integration for arithmetic constraints
- OWL reasoner integration for ontology alignment

### 17.5 Validation Criteria

Each release must satisfy:

1. All assertions traceable via provenance
2. No closed-world negation in inference rules
3. UI frames all outputs as discourse-derived
4. Invalid queries produce educational errors
5. **V1.2+:** Confidence visible at all levels
6. **V1.2+:** Entity resolution explicit, never assumed
7. **V1.2+:** Evidence tiers enforced for actuality
8. **V1.2+:** Performance benchmarks pass
9. **V1.3+:** All queries terminate within decidability bounds
10. **V1.3+:** Sort constraints enforced on all predicates

---

## Appendices

### Appendix A: Complete Predicate Reference

#### A.1 Entity Predicates

```prolog
person(P).
organization(O).
artifact(A).
act(E).
role(R).
document(D).
norm(N).
mention(M).
entity(EntityID, Type, CanonicalName).
```

#### A.2 Provenance Predicates

```prolog
derived_from(E, TextHash, Source, Timestamp, Confidence).
inferred_from(Conclusion, Premises, Rule, Timestamp, Confidence).
source_metadata(Source, Type, Authority, AccessDate, TrustLevel).
source_type(Source, Type).
```

#### A.3 Confidence Bridge Predicates

```prolog
promoted_fact(Fact).
candidate_fact(Fact).
rejected_fact(Fact).
candidate(FactID, Fact, Confidence, Source, Timestamp, Status).
confidence_threshold(Type, Value).
promote_candidate(FactID, Reviewer).
reject_candidate(FactID, Reviewer, Reason).
```

#### A.4 Entity Resolution Predicates

```prolog
mention(MentionID, Text, Source, Position, EntityType).
mention_of(MentionID, EntityID, ResolutionMethod, Confidence).
same_as(Entity1, Entity2, Evidence, Confidence, Asserter).
same_as_symmetric(E1, E2, Ev, C, A).
same_as_transitive(E1, E3, Evidence, Confidence, Asserter).
resolution_candidate(M1, M2, Method, Confidence, Status).
```

#### A.5 Modal Predicates

```prolog
% Alethic
actual(E, Evidence).
claimed_actual(E, Claimant, ClaimSource).
hypothetical(E).
counterfactual(E).
possible(E).
impossible(E).
necessary(E).

% Deontic
obligatory(E).
obligatory(E, Norm, Authority).
obligatory(E, Norm, Authority, Confidence).
permitted(E).
permitted(E, Norm, Authority).
permitted(E, Norm, Authority, Confidence).
forbidden(E).
forbidden(E, Norm, Authority).
forbidden(E, Norm, Authority, Confidence).
optional(E).
```

#### A.6 Evidence Predicates

```prolog
evidence(EvidenceID, Type, Source, Content, Timestamp, TrustLevel).
evidence_tier(Type, TierLevel).
evidence_type_def(Type, Definition).
can_assert_actual(EvidenceID).
trust_level(Level).
source_trust(Source, TrustLevel).
```

#### A.7 Temporal Predicates

```prolog
time_point(PointID, ISO8601String, Granularity).
granularity_level(Level).
before(T1, T2).
after(T1, T2).
same_time(T1, T2).
duration(Unit).
duration_between(T1, T2, Duration).
deadline_passed(Deadline).
deadline_approaching(Deadline, WithinDuration).
obligatory_before(E, Deadline).
obligatory_after(E, StartTime).
obligatory_within(E, Duration, TriggerEvent).
obligation_overdue(Obligation).
obligation_upcoming(Obligation, TimeRemaining).
```

#### A.8 Conflict Predicates

```prolog
conflict_type(Type).
modal_conflict(E, Norm1, Norm2).
resource_conflict(E1, E2).
priority_conflict(E, Norm1, Norm2, Reason).
detected_conflict(ConflictID, Type, Entities).
resolved_conflict(ConflictID, Resolution, PrevailingNorm).
unresolved_conflict(ConflictID).
unresolvable_conflict(ConflictID, Reason).
authority_comparable(Auth1, Auth2).
```

#### A.9 Priority Predicates

```prolog
source_authority_base(Source, Level).
norm_specificity(Norm, Score).
norm_recency_factor(Norm, Factor).
calculate_priority(Norm, Priority).
lex_specialis_applies(SpecificNorm, GeneralNorm).
hierarchically_consistent(LowerNorm, HigherNorm).
resolve_conflict(ConflictID, PrevailingNorm, Method).
```

#### A.10 External Reference Predicates

```prolog
references(InformationEntity, ExternalID).
external_identifier(ExternalID, Registry, Value).
has_external_reference(InfoEntity, Registry, ExternalID).
```

---

### Appendix B: Configuration Reference

#### B.1 Confidence Thresholds

```prolog
% Default confidence thresholds (deployment-configurable)
confidence_threshold(promotion, 0.90).
confidence_threshold(candidacy, 0.70).
confidence_threshold(rejection, 0.70).
confidence_floor(0.50).
```

#### B.2 Evidence Tier Configuration

```prolog
% Evidence tier levels (fixed)
evidence_tier(observation, 1).
evidence_tier(record, 2).
evidence_tier(attestation, 3).
evidence_tier(report, 4).
evidence_tier(claim, 5).

% Maximum tier for actual/2 assertion
max_tier_for_actual(2).
```

#### B.3 Performance Limits

```prolog
% Query constraints
max_temporal_constraints(1000).
temporal_query_timeout_ms(5000).
max_inference_depth(10).
max_query_predicates(100).

% System limits
max_candidate_queue_size(10000).
max_resolution_candidates(10000).
```

#### B.4 Authority Base Levels

```prolog
% Deployment-configurable base authority levels
source_authority_base(constitution, 100).
source_authority_base(treaty, 95).
source_authority_base(statute, 80).
source_authority_base(regulation, 60).
source_authority_base(executive_order, 55).
source_authority_base(contract, 40).
source_authority_base(policy, 20).
source_authority_base(guidance, 10).
```

---

### Appendix C: Glossary

| Term | Definition |
|------|------------|
| **Actuality** | The modal status of an event asserted to have occurred, requiring Tier 1-2 evidence. |
| **Candidate Fact** | An extraction with medium confidence (0.70-0.89) staged for human review. |
| **Claimed Actuality** | An assertion of occurrence from Tier 3-5 evidence, not verified. |
| **Confidence Bridge** | The subsystem mediating between probabilistic extraction and logical assertion. |
| **Datalog** | A subset of Prolog without function symbols, ensuring decidability. |
| **Decidability** | The property that all queries terminate with a definite answer. |
| **Discourse Commitment** | A claim extracted from text, without implying world-truth. |
| **Entity Resolution** | The process of determining when mentions refer to the same entity. |
| **Evidence Tier** | Classification of evidence types by reliability for actuality assertion. |
| **First-Order Logic (FOL)** | Logic allowing quantification over individuals but not predicates. |
| **Kripke Semantics** | Modal logic semantics using possible worlds and accessibility relations. |
| **Lex Specialis** | Legal principle that specific rules override general rules. |
| **Mention** | A specific textual reference to an entity in a document. |
| **Multi-Sorted Logic** | Logic with distinct types (sorts) for different kinds of entities. |
| **Oracle Problem** | The tendency of AI systems to present extracted information as objective truth. |
| **Promoted Fact** | An extraction with high confidence (≥0.90) automatically asserted. |
| **References** | Predicate linking discourse entities to external identifiers without metaphysical commitment. |
| **Same_as** | Predicate asserting cross-document entity identity with explicit evidence. |
| **Second-Order Logic (SOL)** | Logic allowing quantification over predicates; generally undecidable. |
| **Sort** | A type category in multi-sorted logic (e.g., Event, Person, Norm). |
| **Stratified Negation** | Negation where negative literals only reference lower "strata" of predicates. |

---

### Appendix D: References

1. Davidson, D. (1967). "The Logical Form of Action Sentences." In *The Logic of Decision and Action*.

2. Arp, R., Smith, B., & Spear, A. D. (2015). *Building Ontologies with Basic Formal Ontology*. MIT Press.

3. Allen, J. F. (1983). "Maintaining Knowledge about Temporal Intervals." *Communications of the ACM*.

4. Kripke, S. (1963). "Semantical Considerations on Modal Logic." *Acta Philosophica Fennica*.

5. von Wright, G. H. (1951). "Deontic Logic." *Mind*.

6. Prakken, H., & Sartor, G. (2015). "Law and Logic: A Review from an Argumentation Perspective." *Artificial Intelligence*.

7. Information Artifact Ontology (IAO). https://github.com/information-artifact-ontology/IAO

8. Common Core Ontologies (CCO). https://github.com/CommonCoreOntology/CommonCoreOntologies

9. Fitting, M., & Mendelsohn, R. L. (1998). *First-Order Modal Logic*. Springer.

10. Ceri, S., Gottlob, G., & Tanca, L. (1989). "What you always wanted to know about Datalog (and never dared to ask)." *IEEE TKDE*.

11. Baader, F., et al. (2003). *The Description Logic Handbook*. Cambridge University Press.

---

### Appendix E: Logical Foundations Quick Reference

#### E.1 FOL Encoding Cheat Sheet

| You Want To Express | Modal Notation | MDRE Encoding |
|---------------------|----------------|---------------|
| "X is obligatory" | O(X) | `obligatory(X, Norm, Auth)` |
| "X is permitted" | P(X) | `permitted(X, Norm, Auth)` |
| "X is forbidden" | F(X) | `forbidden(X, Norm, Auth)` |
| "X actually happened" | @X | `actual(X, Evidence)` |
| "X is possible" | ◇X | `possible(X)` |
| "X is necessary" | □X | `necessary(X)` |
| "All buyers must pay" | ∀x.Buyer(x)→O(Pay(x)) | Rule: `obligatory(P,N,A) :- act_type(P,pay), agent_qua_role(P,_,buyer)` |

#### E.2 Decidability Quick Check

Your query is decidable if:
- ✓ No unbounded recursion
- ✓ All negation is stratified
- ✓ No function symbol nesting
- ✓ Finite domain for all variables

#### E.3 Sort Compatibility Matrix

| Predicate | Arg 1 Sort | Arg 2 Sort | Arg 3 Sort |
|-----------|------------|------------|------------|
| `agent` | Event | Continuant | - |
| `obligatory` | Event | - | - |
| `obligatory` | Event | Norm | Authority |
| `derived_from` | Entity | TextHash | Document |
| `same_as` | Entity | Entity | Evidence |

#### E.4 Common Pitfalls

| Pitfall | Wrong | Right |
|---------|-------|-------|
| Assuming permission | `permitted(X) :- \+ forbidden(X)` | `permission_unknown(X) :- \+ permitted(X), \+ forbidden(X)` |
| Unbounded recursion | `ancestor(X,Z) :- ancestor(X,Y), ancestor(Y,Z)` | Use depth-limited version |
| Unstratified negation | Circular negation references | Layer predicates into strata |

---

## Document Metadata

**Specification:** Modal Discourse Reasoning Engine (MDRE)  
**Version:** 1.3.0  
**Status:** Draft for Implementation Review  
**Classification:** Technical Specification  
**Audience:** Engineering and Research Teams  

**V1.3 Change Summary:**
- Added Logical Foundations section (§3)
- Explicit multi-sorted FOL framework with sort hierarchy
- Modal operators defined as first-order predicates with encoding table
- Quantification semantics clarified (existential default, universal via rules)
- Decidability guarantees documented with Datalog restrictions
- Expressiveness boundaries explicitly stated
- Upgrade paths to SOL and hybrid reasoning defined
- Formal semantics summary with axioms
- Section numbers shifted (Formal Ontology now §4, etc.)

---

*End of Specification*
