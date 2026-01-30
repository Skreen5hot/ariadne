# Ontological Constraint Engine (OCE)

**Architectural Specification v1.3**

A subsystem for bounded synthetic agency providing ontological coherence validation, typed constraint feedback, and possibility-space navigation.

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2025-01-20 | Initial extraction from UI-oriented spec |
| 1.1 | 2025-01-20 | Added Surprise Signal mechanism; Teleological weights; Allen Interval Algebra; Mereological violations; Salience-based disposition tracking; Spatial reasoner integration |
| 1.3 | 2025-01-20 | Added Executive Summary; Architectural Boundary Rules (§1.4); Teleological Invariants (§4.4.1); Strong BFO Interpretation statement (§8.4); Repair Epistemics clarification (§4.7); Uncertainty handling marked experimental (§9.4); Performance targets reframed; Physical examples added; Surprise Signal flow diagram |

---

## Executive Summary

### Purpose

The Ontological Constraint Engine (OCE) is a **possibility boundary oracle** for synthetic agents. It answers one question:

> Given the world as modeled, which states and transitions are ontologically permitted?

The OCE does not reason about what is *good*, *believed*, or *desired*—only what is *possible*. It serves as:

- A **precondition for planning**: Actions cannot be planned if their target states are impossible
- A **guardrail for ethics**: Normative evaluation presupposes coherent action spaces
- A **brake on hallucination**: The agent cannot model incoherent world states

### Architectural Position

```
┌─────────────────────────────────────────────────────────┐
│                   Synthetic Agent                       │
├─────────────────────────────────────────────────────────┤
│  Normative Layer    │  "Is this action permissible?"   │
├─────────────────────────────────────────────────────────┤
│  Planning Layer     │  "How do I achieve this goal?"   │
├─────────────────────────────────────────────────────────┤
│  ◆ OCE ◆            │  "Is this state/transition       │
│                     │   ontologically possible?"        │
├─────────────────────────────────────────────────────────┤
│  World Model        │  "What do I believe exists?"     │
├─────────────────────────────────────────────────────────┤
│  Perceptual Layer   │  "What am I perceiving?"         │
└─────────────────────────────────────────────────────────┘
```

### Core Capabilities

| Capability | Input | Output |
|------------|-------|--------|
| State Validation | Proposed world state | Coherent / Incoherent(typed violations) |
| Transition Validation | State pair (S₁, S₂) | Permitted / Forbidden / IntervalViolation |
| Possibility Query | Current state + goal | Reachable / Unreachable(blocking constraints) |
| Repair Generation | Violation | Ranked repair paths (proposals, not commitments) |
| Temporal Projection | Process sequence | Interval trajectory with coherence status |
| Surprise Signal | High-confidence sensory conflict | Structural delta proposals for upstream decision |

### Key Design Principles

1. **Typed Refusal**: All constraint violations are classified (InherenceError, MereologicalViolation, etc.), never generic "invalid"
2. **Constructive Negation**: Refusals include repair paths where computable
3. **Interval Coherence**: Transitions are validated across their full temporal extent, not just endpoints
4. **Epistemic Passivity**: OCE proposes structural deltas but never commits belief changes
5. **Teleological Sensitivity**: Repair ranking can incorporate agent intent without altering constraint satisfaction

### Analogies for Orientation

The OCE is conceptually analogous to:

| Domain | Analog | Shared Property |
|--------|--------|-----------------|
| Philosophy | Kant's conditions of possibility | Delimits what can be thought/modeled coherently |
| Robotics | Physics simulator | Prevents impossible configurations before execution |
| Programming | Type system | Rejects ill-formed constructs at compile time |
| Logic | Satisfiability checker | Determines whether constraints admit solutions |

Like a type system, OCE operates *before* execution. Like a physics simulator, it enforces structural laws. Like Kant's categories, it defines the boundaries within which coherent representation is possible.

### What OCE Is Not

- **Not a reasoner**: Does not derive new beliefs or conclusions
- **Not a planner**: Does not select actions or optimize goals
- **Not an ethics engine**: Does not evaluate permissibility or value
- **Not a belief revision system**: Does not commit changes to the world model
- **Not a perception system**: Does not interpret sensory data

OCE is a **constraint oracle**. It says "no" with explanations, and "yes" with confidence, but it does not act.

### Reading Guide

| Section | Content | Priority |
|---------|---------|----------|
| §1 | Purpose, positioning, boundary rules | Essential |
| §2 | Core operations (validation, projection, surprise) | Essential |
| §3 | Typed violation taxonomy | Essential |
| §4 | Repair path generation | High |
| §5 | Temporal reasoning (Allen intervals) | High |
| §6 | Spatial reasoning (RCC-8) | Medium |
| §7-8 | Integration interfaces, ontology infrastructure | Medium |
| §9 | Agent extensions, uncertainty (experimental) | Reference |
| §10-11 | Implementation, open questions | Reference |
| Appendices | Examples, glossary | Reference |

---

## 1. Purpose and Positioning

### 1.1 Function

The Ontological Constraint Engine (OCE) validates proposed world states and state transitions against BFO-grounded ontological commitments. It answers the question:

> Given the world as modeled, which transitions are ontologically permitted?

The OCE does not reason about what is *good*—only what is *possible*. Normative evaluation occurs in higher layers that consume OCE outputs.

**Conceptual Framing**: OCE functions as a *negative capability engine*—it defines the boundaries of coherent representation. This is analogous to:

- **Kantian conditions of possibility**: The categories that structure coherent experience
- **Physical simulators**: Engines that reject impossible configurations before robot execution
- **Type systems**: Compilers that refuse ill-typed programs before runtime

In each case, the system's value lies in what it *refuses*, not what it produces.

### 1.2 Architectural Position

```
┌─────────────────────────────────────────────────────────┐
│                   Synthetic Agent                       │
├─────────────────────────────────────────────────────────┤
│  Normative Reasoning Layer                              │
│  (evaluates permissibility, obligation, value)          │
├─────────────────────────────────────────────────────────┤
│  Action Planning Layer                                  │
│  (goal pursuit, plan construction, counterfactual       │
│   evaluation; provides teleological context to OCE)     │
├─────────────────────────────────────────────────────────┤
│  ◆ ONTOLOGICAL CONSTRAINT ENGINE ◆                      │
│  (possibility validation, typed refusal, repair paths,  │
│   surprise signaling, interval-based projection)        │
├─────────────────────────────────────────────────────────┤
│  World Model                                            │
│  (BFO-grounded state representation)                    │
├─────────────────────────────────────────────────────────┤
│  Perceptual Layer                                       │
│  (input validation, semantic gatekeeping via ECCPS)     │
└─────────────────────────────────────────────────────────┘
```

### 1.3 Design Commitments

1. **Ontological grounding**: All constraints derive from BFO 2020 and applicable domain ontologies (CCO, IAO, etc.)
2. **Typed feedback**: No undifferentiated "invalid" responses; all refusals are classified
3. **Constructive refusal**: Constraint violations include repair paths where computable
4. **Teleological sensitivity**: Repair ranking respects agent intent when provided
5. **Epistemic passivity**: OCE proposes but never commits belief changes (see §1.4)
6. **Separation of concerns**: OCE does not evaluate normative status, only ontological coherence

### 1.4 Architectural Boundary Rules (NEW)

To prevent layer collapse under implementation pressure, the following invariants are **definitional** for OCE:

#### 1.4.1 Epistemic Passivity Invariant

```
INVARIANT: OCE performs structural epistemic triage, not belief revision.

OCE NEVER:
  - Commits changes to the World Model
  - Asserts beliefs on behalf of the agent
  - Selects among competing interpretations
  - Updates ontology modules autonomously

OCE ALWAYS:
  - Proposes structural deltas for upstream decision
  - Returns typed violations with repair options
  - Defers commitment to the epistemic/planning layers
  - Maintains read-only access to World Model
```

**Rationale**: If OCE commits beliefs, it becomes an agent kernel rather than a constraint service. The agent must retain epistemic autonomy.

#### 1.4.2 Possibility Independence Invariant

```
INVARIANT: Ontological possibility is intent-independent.

A state S is possible iff S satisfies all ontological constraints.
This determination is INVARIANT under:
  - Agent goals
  - Teleological context
  - Repair ranking preferences
  - Upstream layer requests

No query parameter may cause OCE to:
  - Report a forbidden state as permitted
  - Suppress a violation
  - Modify constraint satisfaction criteria
```

**Rationale**: If teleological context could alter possibility verdicts, OCE would become a normative reasoner. Possibility must remain a structural fact, not a negotiated outcome.

#### 1.4.3 Transparency Invariant

```
INVARIANT: All OCE outputs are structurally explained.

Every ValidationResult, TransitionResult, and RepairPath includes:
  - Explicit constraint references
  - Derivation chains
  - BFO grounding

OCE produces no "black box" verdicts.
```

**Rationale**: Downstream layers (planning, ethics) require auditable inputs. Unexplained refusals break the architectural contract.

---

## 2. Core Operations

### 2.1 State Validation

**Input**: Proposed world state (set of instantiated universals, relations, and qualities)

**Output**: Validation result

```
ValidationResult ::= 
  | Coherent
  | Incoherent(violations: Set<TypedViolation>)
```

A state is coherent iff:
- All asserted instances instantiate defined universals
- All specifically dependent continuants have valid bearers
- All relational assertions satisfy domain/range constraints
- No mutually exclusive states are co-asserted
- All spatial relations are consistent (validated via spatial reasoner; see §6)
- All temporal relations are consistent (validated via interval algebra; see §5)
- All mereological relations are consistent (no part larger than whole, no temporal boundary violations)

### 2.2 Transition Validation

**Input**: Current state S₁, proposed state S₂

**Output**: Transition result

```
TransitionResult ::=
  | Permitted(process: ProcessType, intervals: Set<TemporalInterval>)
  | Forbidden(violations: Set<TypedViolation>, repairs: Set<RepairPath>)
  | IntervalViolation(valid_at: Set<TimePoint>, invalid_during: Set<TemporalInterval>)
```

A transition is permitted iff:
- S₂ is coherent
- There exists a process type P such that:
  - All participants required by P exist in S₁
  - All preconditions of P are satisfied in S₁
  - P's postconditions entail S₂
- **No intermediate state during the transition violates coherence** (see §5.2)

The `IntervalViolation` result type handles cases where endpoints are valid but the transition path is not.

**Physical Example**: A robotic arm moving a component from Station A to Station B:
- S₁: `located_at(component, stationA)` ✓
- S₂: `located_at(component, stationB)` ✓
- Transition requires `Transport` process; without it, the component's location during [T₁, T₂] is undefined, yielding IntervalViolation

### 2.3 Possibility Query

**Input**: Current state S, goal predicate G

**Output**: Reachability assessment

```
ReachabilityResult ::=
  | Reachable(paths: Set<ProcessSequence>)
  | Unreachable(blocking: Set<TypedViolation>, nearest: Set<PartialPath>)
```

This supports planning by identifying whether a goal state is achievable and, if not, what structural obstacles prevent it.

### 2.4 Teleologically-Weighted Query

**Input**: Current state S, goal predicate G, teleological context T

**Output**: Reachability assessment with intent-preserving repair ranking

```
TeleologicalContext {
  goal: Predicate
  essential_elements: Set<EntityReference>    // Must be preserved
  preferred_relations: Set<RelationType>       // Prefer repairs that maintain these
  intent_description: StructuredIntent         // Machine-readable goal structure
}

TeleologicalReachabilityResult ::=
  | Reachable(paths: Set<ProcessSequence>, ranked_by_intent: Boolean)
  | Unreachable(blocking: Set<TypedViolation>, repairs: Set<RankedRepairPath>)

RankedRepairPath {
  path: RepairPath
  intent_alignment_score: Float    // 0.0 = destroys intent, 1.0 = fully preserves
  preserved_elements: Set<EntityReference>
  lost_elements: Set<EntityReference>
}
```

**Critical**: Teleological context affects *repair ranking* only, never *possibility verdicts*. See §4.4.1 for formal invariants.

### 2.5 Surprise Signal

When a state transition is rejected but supported by high-confidence sensory input, the OCE generates a Surprise Signal rather than simple refusal.

```
SurpriseSignal {
  rejected_assertion: Assertion
  confidence: Float                           // From perceptual layer
  blocking_constraints: Set<TypedViolation>
  interpretation_alternatives: Set<Reinterpretation>
  learning_trigger: OntologyLearningProposal  // Proposal, not commitment
}

Reinterpretation {
  alternative_parse: Assertion
  required_reclassifications: Set<Reclassification>
  coherence_if_accepted: Boolean
}

OntologyLearningProposal {
  type: LexicalExtension | CategoryRevision | RelationAddition
  evidence: Set<SensoryEvidence>
  proposed_modification: OntologyDelta
  confidence_threshold_met: Boolean
}
```

**Critical**: Per §1.4.1, OCE *proposes* learning; it does not execute it. The agent's epistemic layer decides whether to accept.

#### 2.5.1 Surprise Signal Flow Diagram (NEW)

```
┌──────────────────┐
│ Perceptual Layer │
│ (high-confidence │
│  assertion A)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   World Model    │
│ (attempt to      │
│  integrate A)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌─────────────────────────────────────┐
│       OCE        │────▶│ ValidationResult::Incoherent        │
│ (validate new    │     │   + Confidence > threshold?         │
│  state with A)   │     └──────────────┬──────────────────────┘
└──────────────────┘                    │
                                        │ YES
                                        ▼
                        ┌───────────────────────────────────┐
                        │        SurpriseSignal             │
                        │  - rejected_assertion: A          │
                        │  - blocking_constraints: {...}    │
                        │  - interpretation_alternatives    │
                        │  - learning_trigger (PROPOSAL)    │
                        └───────────────┬───────────────────┘
                                        │
                                        ▼
                        ┌───────────────────────────────────┐
                        │      Epistemic Layer              │
                        │  (DECIDES whether to):            │
                        │  - Trust sensors → update belief  │
                        │  - Trust model → flag sensor err  │
                        │  - Defer → accumulate evidence    │
                        │  - Learn → modify ontology        │
                        └───────────────────────────────────┘
                                        │
                                        ▼
                        ┌───────────────────────────────────┐
                        │      World Model Update           │
                        │  (if epistemic layer commits)     │
                        └───────────────────────────────────┘
```

**Key Point**: The arrow from SurpriseSignal to Epistemic Layer is a *proposal*. OCE has no write access to World Model. The Epistemic Layer holds commitment authority.

**Triggering conditions**:
- Perceptual confidence > configurable threshold (default: 0.85)
- Ontological rejection is not a CategoryError (hard metaphysical impossibility)
- At least one Reinterpretation exists OR learning is enabled

**Physical Example**: Thermal sensor reports component temperature at 450°C, but current model asserts component material has melting point of 400°C.
- OCE rejects: component cannot be solid at 450°C given material properties
- Surprise Signal generated: either sensor error, material misclassified, or phase-change process occurring
- Epistemic Layer decides: check secondary sensors, reclassify material, or model melting process

---

## 3. Typed Constraint Violations

All constraint violations are classified. The OCE never returns untyped errors.

### 3.1 Violation Taxonomy

The taxonomy serves as a **semantic interface**, not merely error handling. Each type enables:
- Specific repair strategies
- Targeted explanations
- Learning pathway identification

| Type | Definition | Example |
|------|------------|---------|
| `LexicalGap` | Token not mapped in active ontology modules | "gloopiness" not defined |
| `CategoryError` | BFO category misapplication | Quality asserted of occurrent |
| `BearerViolation` | Dependent continuant lacks valid bearer | Color without material entity |
| `InherenceError` | Quality/disposition cannot inhere in bearer type | Repentance in rock |
| `RoleContextViolation` | Role asserted without required relational context | Operator without operation |
| `RelationDomainViolation` | Relation domain constraint unsatisfied | `continuant_part_of` with occurrent as subject |
| `RelationRangeViolation` | Relation range constraint unsatisfied | `has_participant` with quality as object |
| `SpatialInconsistency` | Incompatible spatial assertions (RCC-8 violation) | A contained in B, B contained in A |
| `TemporalInconsistency` | Incompatible temporal assertions (Allen violation) | Process before its precondition |
| `MutualExclusion` | Co-assertion of disjoint states | Alive and dead simultaneously |
| `MereologicalViolation` | Part-whole constraint failure | Part extends beyond whole's boundary |
| `DispositionUnrealizable` | Disposition realization conditions unsatisfiable | Fragility without possible stressor |
| `ProcessPreconditionFailure` | Process asserted without satisfied preconditions | Combustion without fuel |
| `CardinalityViolation` | Relation cardinality constraint violated | Two simultaneous exact locations |
| `IntervalCoherenceViolation` | Transition requires incoherent intermediate | Valid at T₁ and T₂, incoherent at T₁.₅ |

### 3.2 Violation Structure

```
TypedViolation {
  type: ViolationType
  subject: EntityReference
  predicate: RelationOrPropertyReference (optional)
  object: EntityReference (optional)
  constraint: AxiomReference
  explanation: StructuralExplanation
  temporal_scope: TemporalInterval (optional)
}
```

### 3.3 Structural Explanation

Explanations are derivations, not strings:

```
StructuralExplanation {
  violated_axiom: OWLAxiom
  instantiation_chain: List<InstantiationStep>
  conflict_point: LogicalContradiction
  bfo_grounding: BFOCategoryReference
}
```

Per §1.4.3, every violation traces to explicit BFO commitments.

### 3.4 Mereological Violation Details

```
MereologicalViolation {
  violation_subtype: 
    | PartLargerThanWhole(part: Entity, whole: Entity, dimension: SpatialDimension)
    | TemporalBoundaryExceedance(part: Entity, whole: Entity, exceeds_by: TemporalInterval)
    | CircularParthood(cycle: List<Entity>)
    | PartOutsideWhole(part: Entity, whole: Entity, external_region: SpatialRegion)
  mereological_axiom: MereologyAxiomReference
}
```

**Physical Example**: Battery cell modeled as `continuant_part_of` battery pack, but cell's operational lifespan extends beyond pack's defined service interval → TemporalBoundaryExceedance.

---

## 4. Repair Path Generation

When a proposed state or transition is forbidden, the OCE generates repair paths—minimal modifications that would yield coherence.

### 4.1 Repair Operations

| Operation | Definition |
|-----------|------------|
| `Substitute(e, e')` | Replace entity e with entity e' of compatible type |
| `Add(r, e₁, e₂)` | Assert relation r between e₁ and e₂ |
| `Remove(assertion)` | Retract an assertion |
| `Reclassify(e, U)` | Assign entity e to universal U |
| `InstantiateBearer(d, U)` | Create bearer of type U for dependent d |
| `SatisfyPrecondition(p, process)` | Identify actions to satisfy precondition p |
| `InsertIntermediateState(S_mid)` | Add intermediate state to resolve interval violation |
| `ExtendTemporalBoundary(e, interval)` | Expand temporal scope of entity |

### 4.2 Repair Path Structure

```
RepairPath {
  operations: List<RepairOperation>
  resulting_state: StateDescription
  cost: RepairCost
  completeness: Complete | Partial
  intent_alignment: Float (optional)
}
```

### 4.3 Repair Cost Heuristics (Base)

Repairs are ranked by estimated cost:

1. **Ontological distance**: Substituting within same genus < across genera
2. **Assertion count**: Fewer modifications preferred
3. **Structural impact**: Local changes < changes with cascading effects
4. **Reversibility**: Reversible repairs < irreversible
5. **Mereological preservation**: Repairs maintaining part-whole structures preferred

### 4.4 Teleological Weighting

When `TeleologicalContext` is provided, repair ranking incorporates intent preservation:

```
TeleologicalRepairCost {
  base_cost: RepairCost
  intent_alignment: Float                    // 0.0–1.0
  essential_element_loss: Set<EntityReference>
  goal_distance_after_repair: Float
}

effective_cost = 
  (w_base * base_cost) + 
  (w_intent * (1.0 - intent_alignment)) + 
  (w_goal * goal_distance_after_repair) +
  (w_essential * |essential_element_loss|)
```

#### 4.4.1 Teleological Invariants (NEW)

```
INVARIANT: Teleological context may rank repairs but may NEVER:

1. PERMIT an otherwise forbidden transition
   - If validateTransition(S₁, S₂) = Forbidden, no TeleologicalContext
     can yield Permitted

2. SUPPRESS a violation
   - If violation V ∈ violations(S), V must appear in output regardless
     of teleological context

3. MODIFY constraint satisfaction criteria
   - The predicate "S is coherent" is evaluated identically with or
     without TeleologicalContext

4. ALTER the set of valid repairs
   - TeleologicalContext affects ordering only, not membership
   - If repair R is valid without context, R remains valid with context
   - If repair R is invalid without context, R remains invalid with context
```

**Rationale**: Teleological weighting is a *preference* mechanism, not a *permission* mechanism. The agent's goals cannot make the impossible possible.

### 4.5 Repair Completeness

- **Complete**: Repair path yields a coherent state
- **Partial**: Repair path reduces violations but does not eliminate all

Partial paths are returned when complete repair is not computable within resource bounds.

### 4.6 Repair Search Bounds

```
RepairSearchConfig {
  max_depth: Int                    // Maximum operation chain length (default: 5)
  max_candidates: Int               // Maximum repair paths to return (default: 10)
  timeout_ms: Int                   // Hard cutoff for search (default: 500)
  pruning_strategy: PruningStrategy // Beam search, A*, branch-and-bound
  teleological_boost: Float         // Extra search budget when intent provided (default: 1.5x)
}
```

### 4.7 Repair Epistemics (NEW)

To prevent misinterpretation of repair path guarantees:

```
CLARIFICATION: Repair paths are PROPOSALS, not DERIVATIONS.

1. MINIMALITY is heuristic, not guaranteed
   - Repair paths aim for minimal modification but do not prove optimality
   - Smaller repairs may exist outside the search horizon

2. COMPLETENESS is explicitly bounded
   - The set of returned repairs is not exhaustive
   - Search terminates at configured bounds, not logical completion

3. CORRECTNESS is structural, not semantic
   - A repair path guarantees: "if applied, state becomes coherent"
   - A repair path does NOT guarantee: "this is what the agent should do"

4. APPLICATION is upstream responsibility
   - OCE generates repair options
   - Planning/Epistemic layers decide whether to apply
   - OCE has no authority to execute repairs
```

**Rationale**: Repair generation uses heuristic search. Presenting repairs as "derivations" would overstate guarantees and mislead downstream systems.

---

## 5. Temporal Reasoning

The OCE employs Allen's Interval Algebra for temporal reasoning, supporting continuous and overlapping processes.

### 5.1 Temporal Primitives

Following Allen (1983), the OCE recognizes 13 interval relations:

| Relation | Symbol | Inverse |
|----------|--------|---------|
| before | < | after (>) |
| meets | m | met-by (mi) |
| overlaps | o | overlapped-by (oi) |
| starts | s | started-by (si) |
| during | d | contains (di) |
| finishes | f | finished-by (fi) |
| equals | = | equals (=) |

### 5.2 Interval-Based Transition Validation

Transitions are validated not just at endpoints but across the full interval:

```
IntervalTransitionCheck {
  start_state: State
  end_state: State
  transition_interval: TemporalInterval
  intermediate_samples: Int
  continuous_processes: Set<ProcessType>
}

IntervalValidationResult ::=
  | FullyCoherent
  | EndpointsOnlyCoherent(violations_during: Set<(TemporalInterval, TypedViolation)>)
  | Incoherent(violations: Set<TypedViolation>)
```

**Process Smearing Problem**: A state valid at T₁ and T₂ may require passing through incoherent T₁.₅.

The OCE resolves this by:
1. Identifying required intermediate states
2. Generating `InsertIntermediateState` repairs if transition path is unclear
3. Validating that some continuous process covers the interval

### 5.3 Process Interval Representation

```
ProcessInstance {
  type: ProcessType
  interval: TemporalInterval
  participants: Set<(Role, EntityReference, ParticipationInterval)>
  subprocesses: Set<(ProcessInstance, IntervalRelation)>
  preconditions: Set<(Predicate, RequiredInterval)>
  postconditions: Set<(Predicate, EstablishedInterval)>
}

ParticipationInterval {
  entity: EntityReference
  role: Role
  active_during: TemporalInterval
  relation_to_process: IntervalRelation
}
```

### 5.4 Temporal Projection

```
ProjectionRequest {
  initial_state: State
  process_sequence: List<ProcessType>
  horizon: TemporalBound
  interval_granularity: Duration
  overlap_handling: Sequential | Parallel | Inferred
}

ProjectionResult ::=
  | Success(trajectory: IntervalTrajectory)
  | Failure(step: Int, violation: TypedViolation, partial: IntervalTrajectory)
  | IntervalFailure(process: ProcessType, violation_interval: TemporalInterval, 
                    violation: TypedViolation)

IntervalTrajectory {
  intervals: List<(TemporalInterval, State)>
  processes: List<(ProcessInstance, IntervalRelation)>
  transition_coherence: Map<(Interval, Interval), CoherenceStatus>
}
```

### 5.5 Salience-Based Disposition Tracking

Tracking all dispositions during projection is computationally prohibitive. The OCE implements salience filtering:

```
DispositionSalienceConfig {
  goal_relevant: Set<DispositionType>
  proximity_relevant: Boolean
  proximity_radius: SpatialDistance
  trigger_proximity: Boolean
  historical_activation: Boolean
  minimum_salience: Float
}

SalientDisposition {
  disposition: Disposition
  bearer: EntityReference
  salience_score: Float
  salience_sources: Set<SalienceSource>
  tracking_status: Active | Dormant | Triggered | Realized | Blocked
}
```

Only dispositions with `salience >= minimum_salience` are actively tracked during projection.

**Physical Example**: When projecting a welding operation, dispositions tracked include: material thermal conductivity, electrode wear rate, shielding gas flow disposition. Dispositions of unrelated equipment outside the work cell are dormant.

### 5.6 Disposition State Machine

```
DispositionState ::=
  | Latent                  
  | Primed(trigger_proximity: Float)  
  | Triggered               
  | Realizing(progress: Float, process: ProcessInstance)
  | Realized                
  | Blocked(blocker: BlockingCondition)  
  | Expired                 
```

---

## 6. Spatial Reasoning

### 6.1 RCC-8 Integration

The OCE integrates a dedicated spatial reasoner implementing RCC-8:

| Relation | Definition |
|----------|------------|
| DC | Disconnected |
| EC | Externally Connected |
| PO | Partially Overlapping |
| EQ | Equal |
| TPP | Tangential Proper Part |
| NTPP | Non-Tangential Proper Part |
| TPPi | Tangential Proper Part inverse |
| NTPPi | Non-Tangential Proper Part inverse |

### 6.2 Spatial Validation Pipeline

```
SpatialValidation {
  assertions: Set<SpatialAssertion>
  reasoner: RCC8Reasoner
  
  validate() -> Set<SpatialInconsistency>:
    1. Convert assertions to RCC-8 constraint network
    2. Apply path-consistency algorithm
    3. Identify unsatisfiable constraint combinations
    4. Map back to TypedViolations with spatial grounding
}
```

### 6.3 Spatial-Mereological Coordination

Spatial and mereological reasoning must coordinate:

- `continuant_part_of(A, B)` entails `NTPP(location(A), location(B))` or `TPP(...)`
- `located_in(A, R)` entails spatial containment in region R

The OCE maintains a `SpatialMereologicalIndex` ensuring consistency between constraint systems.

**Physical Example**: Modeling a fuel tank inside a vehicle chassis. If `continuant_part_of(tank, chassis)` is asserted, OCE enforces that tank's spatial extent never exceeds chassis boundary. A collision model placing tank partially outside chassis yields SpatialInconsistency.

---

## 7. Integration Interfaces

### 7.1 World Model Interface (Downstream)

```
interface WorldModelReader {
  getCurrentState(): State
  getEntityByReference(ref: EntityReference): Entity
  getActiveOntologyModules(): Set<OntologyModule>
  getSpatialIndex(): SpatialIndex
  getTemporalIndex(): TemporalIndex
}
```

**Note**: This interface is read-only. OCE has no write access to World Model.

### 7.2 Planning Layer Interface (Upstream)

```
interface ConstraintEngine {
  // Basic validation
  validateState(state: State): ValidationResult
  validateTransition(from: State, to: State): TransitionResult
  
  // Possibility queries
  queryReachability(from: State, goal: Predicate): ReachabilityResult
  queryReachabilityWithIntent(from: State, goal: Predicate, 
                               context: TeleologicalContext): TeleologicalReachabilityResult
  
  // Projection
  project(request: ProjectionRequest): ProjectionResult
  projectWithSalience(request: ProjectionRequest, 
                      salience: DispositionSalienceConfig): ProjectionResult
  
  // Repair
  getRepairPaths(violation: TypedViolation, bound: RepairSearchConfig): Set<RepairPath>
  getRepairPathsWithIntent(violation: TypedViolation, bound: RepairSearchConfig,
                           context: TeleologicalContext): Set<RankedRepairPath>
}
```

### 7.3 Normative Layer Interface

```
interface NormativeSupport {
  isObligationSatisfiable(obligation: Obligation, state: State): Boolean
  getBlockingConstraints(obligation: Obligation, state: State): Set<TypedViolation>
  projectObligationFulfillment(obligation: Obligation, state: State, 
                                horizon: TemporalBound): ProjectionResult
}
```

### 7.4 Surprise Signal Interface

```
interface SurpriseHandler {
  onSurprise(signal: SurpriseSignal): SurpriseResponse
}

SurpriseResponse ::=
  | AcceptSensory(update_belief: Boolean)
  | RejectSensory(reason: String)
  | RequestOntologyLearning(request: OntologyLearningProposal)
  | Defer(pending_evidence: EvidenceAccumulator)
```

### 7.5 ECCPS Integration

```
Claim processing flow:

ECCPS → World Model → OCE

Claim: "Component temperature is 450°C"
  ECCPS: Semantically valid? Yes
  World Model: Attempt integration
  OCE: Coherent given material melting point 400°C? No (MutualExclusion: solid + above melting point)
  Result: SurpriseSignal to Epistemic Layer
```

---

## 8. Ontological Infrastructure

### 8.1 Required Ontology Modules

**Core (mandatory)**:
- BFO 2020 (foundational categories)
- RO (relations ontology, BFO-aligned)

**Extended (contextual)**:
- CCO (common core for organizational/social domains)
- IAO (information artifacts)
- Domain-specific extensions as needed

### 8.2 Lexicon Management

```
Lexicon {
  termMappings: Map<Token, Set<OntologyTerm>>
  ambiguityResolution: DisambiguationStrategy
  moduleScope: Set<OntologyModule>
  extensionPolicy: ExtensionPolicy
}

ExtensionPolicy {
  allow_runtime_extension: Boolean
  require_evidence_threshold: Float
  human_approval_required: Boolean
  extension_scope: Temporary | Persistent
}
```

### 8.3 Open-World / Closed-World Configuration

| Regime | Behavior |
|--------|----------|
| `ClosedWorld` | Unasserted = false; unknown entities rejected |
| `OpenWorld` | Unasserted = unknown; novel entities permitted if consistent |
| `LocallyClosed` | Closed for specified predicates, open otherwise |

Default: `LocallyClosed` with closure over spatial, temporal, mereological, and identity predicates.

The Surprise Signal mechanism (§2.5) mitigates ontological blindness from rigid closure.

### 8.4 Strong BFO Interpretation (NEW)

```
NOTICE: OCE enforces a strong interpretation of BFO 2020.

This interpretation assumes:
  - Strict disjointness between BFO categories
  - Classical extensional mereology
  - Strict inherence constraints for dependent continuants
  - Deterministic disposition realization (trigger → process)

This interpretation is suitable for:
  - Synthetic agent world modeling
  - Engineered system simulation
  - Formal verification contexts

This interpretation may be stricter than:
  - Descriptive scientific ontologies
  - Social/institutional modeling (where roles have fuzzy grounding)
  - Probabilistic disposition modeling

Implementers working in domains requiring weaker BFO interpretations
should configure appropriate constraint relaxations or use domain-specific
ontology modules that override base BFO strictures.
```

**Rationale**: BFO implementations vary. OCE commits to a strong interpretation to maximize constraint utility for synthetic agents. This is a feature, not a bug, but must be documented.

---

## 9. Agent-Specific Extensions

### 9.1 Indexical Grounding

```
AgentIndex {
  self: EntityReference
  currentLocation: SpatialRegion
  currentTime: TemporalRegion
  activeRoles: Set<Role>
  ownedDispositions: Set<SalientDisposition>
  bodySchema: MereologicalStructure
}
```

### 9.2 Other-Agent Modeling

```
ModeledAgent {
  entity: EntityReference
  attributedDispositions: Set<(Disposition, Confidence)>
  attributedRoles: Set<(Role, Confidence)>
  epistemicStatus: Opaque | PartiallyTransparent | Transparent
  predictedBehavior: Set<(ProcessType, Probability, TemporalInterval)>
}
```

### 9.3 Uncertainty Representation

**STATUS: EXPERIMENTAL — See §9.4**

For real-world operation, the OCE may handle uncertain states:

```
UncertainState {
  assertions: Set<(Assertion, Probability)>
  dependencies: Set<ProbabilisticDependency>
}

UncertainValidationResult {
  coherenceProbability: Probability
  violationRisks: Set<(TypedViolation, Probability)>
  mostLikelyCoherentState: State
  requiredClarifications: Set<Assertion>
}
```

### 9.4 Uncertainty Handling Status (NEW)

```
STATUS: EXPERIMENTAL

Uncertainty handling (§9.3) constitutes a second reasoning engine:
  - Probabilistic constraint satisfaction
  - Belief-sensitive coherence evaluation
  - Distribution propagation through projections

This capability is:
  - OPTIONAL: Core OCE functions operate on definite states
  - DOWNSTREAM-CONTROLLED: Enabled only when explicitly requested
  - RESOURCE-INTENSIVE: May dominate system performance
  - ARCHITECTURALLY DISTINCT: May warrant separate subsystem in future versions

Implementers should:
  - Treat uncertainty handling as experimental
  - Profile performance impact before production use
  - Consider dedicated probabilistic reasoning subsystem for heavy usage

Uncertainty handling may be moved to dedicated specification in v2.0.
```

---

## 10. Implementation Architecture

### 10.1 Reasoner Stack

```
┌─────────────────────────────────────────┐
│         OCE Query Interface             │
├─────────────────────────────────────────┤
│         Validation Orchestrator         │
├──────────┬──────────┬──────────┬────────┤
│  OWL 2   │  Allen   │  RCC-8   │ Repair │
│ Reasoner │ Temporal │ Spatial  │ Search │
│ (EL/RL)  │ Reasoner │ Reasoner │ Engine │
├──────────┴──────────┴──────────┴────────┤
│         Constraint Index Cache          │
├─────────────────────────────────────────┤
│         World Model Interface           │
└─────────────────────────────────────────┘
```

### 10.2 Reasoner Requirements

| Component | Capability | Implementation Options |
|-----------|------------|----------------------|
| OWL Reasoner | OWL 2 EL or RL (tractable) | ELK, jcel, or custom |
| Temporal Reasoner | Allen Interval Algebra | Custom or GQR |
| Spatial Reasoner | RCC-8 path consistency | GQR, SparQ, or custom |
| Repair Engine | Heuristic search with pruning | A*, beam search |

### 10.3 Performance Targets (Reframed)

```
FRAMING: Interactive design targets under typical workloads.

These targets assume:
  - World Model < 1000 assertions
  - Ontology modules < 10,000 axioms
  - Single-threaded query processing
  - Warm constraint index cache

Targets are ASPIRATIONAL for initial implementation and subject to
revision based on empirical profiling.
```

| Operation | Target Latency | Notes |
|-----------|----------------|-------|
| State validation (single assertion) | < 10ms | Cache-assisted |
| State validation (full state) | < 100ms | < 1000 assertions |
| Transition validation (point) | < 50ms | Without interval check |
| Transition validation (interval) | < 200ms | With interval sampling |
| Repair path generation (depth 3) | < 500ms | Heuristic, not exhaustive |
| Repair with teleological context | < 750ms | Additional ranking pass |
| Projection (10-step, point) | < 1s | Sequential processes |
| Projection (10-step, interval) | < 3s | Continuous coherence |
| Surprise signal generation | < 100ms | Including alternatives |

---

## 11. Open Questions

### 11.1 Thick vs Thin OCE

Should normative categories (obligation, permission, prohibition) be represented in OCE's ontology?

**Current position**: v1.3 remains "thin." Normative integration deferred to v2.0.

**Tradeoff**:
- Thick: Detect deontic contradictions at OCE layer
- Thin: Cleaner separation; normative reasoning fully in Normative Layer

### 11.2 Ontology Learning Scope

The Surprise Signal can trigger `OntologyLearningProposal`. Permitted modifications:

| Modification | Permission Level |
|--------------|-----------------|
| LexicalExtension | Evidence threshold |
| InstanceReclassification | Evidence threshold |
| UniversalAddition | Elevated approval |
| AxiomModification | Human review required |

### 11.3 Inter-Agent Ontology Negotiation

For agents with different ontological commitments:

```
interface OntologyNegotiationSupport {
  detectCommitmentConflict(ownAssertion: Assertion, 
                           foreignAssertion: Assertion): ConflictAnalysis
  proposeCommonGround(conflict: ConflictAnalysis): Set<NegotiationOption>
}
```

Integration with FANDAWS semantic negotiation services.

### 11.4 Counterfactual Scope

**Resolved**: OCE supports projection from arbitrary hypothetical states (liberal approach), with explicit coherence checking of hypothetical starting states.

---

## 12. Relation to Existing Work

### 12.1 Conceptual Lineage

The OCE belongs to a family of "possibility boundary" systems:

| System Type | Domain | Shared Property |
|-------------|--------|-----------------|
| Type systems | Programming | Reject ill-formed constructs before execution |
| Physics engines | Robotics | Prevent impossible configurations |
| SAT solvers | Logic | Determine constraint satisfiability |
| Model checkers | Verification | Enumerate reachable states |
| OCE | Ontology | Validate world states against BFO commitments |

### 12.2 ECCPS

ECCPS validates claims for ontological density; OCE validates resulting state changes for coherence. Sequential gates:

- ECCPS: "Is this claim well-formed and grounded?"
- OCE: "Does accepting this claim yield a coherent world model?"

### 12.3 Integral Ethics Engine

IEE requires OCE for:
- Action possibility confirmation
- Consequence projection
- Affected party identification

OCE's teleological interface allows IEE to weight repairs by ethical relevance.

### 12.4 ARCHON

ARCHON may constrain which ontological commitments the agent may hold—a meta-level above OCE.

### 12.5 Architectonic Agency Theory

Triple-I Standard requires tracking structural integrity over time. OCE's temporal projection supports this.

### 12.6 FANDAWS

Semantic negotiation for inter-agent communication with differing ontological commitments.

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Allen relation** | One of 13 temporal interval relations |
| **Bearer** | Independent continuant in which a dependent continuant inheres |
| **Coherent state** | World state satisfying all ontological constraints |
| **Dependent continuant** | Entity requiring a bearer (qualities, dispositions, roles) |
| **Disposition** | Realizable entity exercised under triggering conditions |
| **Independent continuant** | Entity not requiring a bearer |
| **Interval trajectory** | State sequence with explicit temporal intervals |
| **Mereological** | Pertaining to part-whole relations |
| **Occurrent** | Entity unfolding in time (processes, temporal regions) |
| **RCC-8** | Region Connection Calculus with 8 spatial relations |
| **Repair path** | Proposed modifications to achieve coherence |
| **Role** | Externally grounded realizable entity |
| **Salience** | Relevance of disposition to current agent context |
| **Surprise signal** | OCE output when high-confidence data conflicts with ontology |
| **Teleological context** | Agent intent for repair ranking |
| **Typed violation** | Classified constraint failure |
| **Universal** | Repeatable pattern instantiated by particulars |

---

## Appendix B: Example — Philosophical (Rock Repentance)

**Scenario**: Agent contemplates state where "rock repents"

**Proposed assertion**: `inheres_in(repentance_instance_1, rock_instance_1)`

**Validation chain**:
1. `repentance_instance_1 : Repentance`
2. `Repentance SubClassOf MentalDisposition`
3. `MentalDisposition SubClassOf inheres_in only CognitiveAgent`
4. `rock_instance_1 : Rock`
5. `Rock SubClassOf MaterialEntity`
6. `MaterialEntity DisjointWith CognitiveAgent`
7. **Conflict**: Bearer required to be CognitiveAgent but is MaterialEntity

**Typed Violation**:
```
{
  type: InherenceError,
  subject: repentance_instance_1,
  predicate: inheres_in,
  object: rock_instance_1,
  constraint: <MentalDisposition inheres_in only CognitiveAgent>,
  explanation: {
    violated_axiom: "MentalDisposition SubClassOf inheres_in only CognitiveAgent",
    instantiation_chain: [see above],
    conflict_point: "rock_instance_1 required CognitiveAgent, is MaterialEntity",
    bfo_grounding: "BFO:0000017 realizable entity inherence"
  }
}
```

**Repairs without teleological context**:
1. `Remove(assertion)` — cost: 1.0
2. `Substitute(rock, ?:CognitiveAgent)` — cost: 2.5

**Repairs with teleological context** `{essential: [repentance], goal: achieve_repentance}`:
1. `Substitute(rock, ?:CognitiveAgent)` — intent_alignment: 0.95, adjusted_cost: 1.2
2. `Remove(assertion)` — intent_alignment: 0.0, adjusted_cost: 10.0

---

## Appendix C: Example — Physical (Component Transport)

**Scenario**: Robotic system moves component from Station A to Station B

**States**:
- S₁ (T₁): `located_at(component, stationA)`, `secured_to(component, fixture_A)`
- S₂ (T₂): `located_at(component, stationB)`, `secured_to(component, fixture_B)`

**Naive validation**: Both endpoints coherent.

**Interval-based validation**:

1. Identify transition interval [T₁, T₂]
2. Required process: `Transport(component, stationA, stationB)`
3. Transport preconditions:
   - `¬secured_to(component, fixture_A)` — must release before transport
4. Check S₁: `secured_to(component, fixture_A)` — precondition violated

**Result**:
```
TransitionResult::Forbidden(
  violations: [ProcessPreconditionFailure(
    process: Transport,
    precondition: ¬secured_to(component, fixture_A),
    current_state: secured_to(component, fixture_A)
  )],
  repairs: [
    InsertIntermediateState(Release(component, fixture_A)),
    then: Transport(component, stationA, stationB),
    then: Secure(component, fixture_B)
  ]
)
```

**With interval coherence**:

If release occurs at T₁, transport during [T₁+ε, T₂-ε], secure at T₂:
- During transport: component location = transport path (robot gripper)
- `located_at(component, gripper)` must be coherent
- If gripper capacity exceeded: MereologicalViolation

```
IntervalTrajectory {
  intervals: [
    (T₁, {located_at(component, stationA), secured_to(component, fixture_A)}),
    (T₁+ε, {located_at(component, stationA), held_by(component, gripper)}),
    ([T₁+ε, T₂-ε], {located_at(component, gripper), held_by(component, gripper)}),
    (T₂-ε, {located_at(component, stationB), held_by(component, gripper)}),
    (T₂, {located_at(component, stationB), secured_to(component, fixture_B)})
  ],
  processes: [Release, Transport, Secure],
  transition_coherence: all Coherent
}
```

---

## Appendix D: Example — Thermal (Battery Overheating)

**Scenario**: Battery management system monitors cell temperature

**Current state**:
- `temperature(cell_1, 85°C)`
- `material(cell_1, lithium_polymer)`
- `thermal_runaway_threshold(lithium_polymer, 90°C)`
- `disposition: thermal_runaway_susceptibility(cell_1)` — Latent

**Sensor update**: `temperature(cell_1, 92°C)`

**OCE validation**:
1. New state: temperature exceeds thermal_runaway_threshold
2. Disposition `thermal_runaway_susceptibility` should transition: Latent → Triggered
3. Triggered disposition requires `ThermalRunaway` process to be occurring or imminent
4. If no `ThermalRunaway` process asserted: DispositionUnrealizable? No — disposition is realizable, just not yet realized
5. Check: Is temperature + no active runaway process coherent?

**Surprise Signal scenario**:

If model asserts `status(cell_1, nominal)` but sensors report 92°C:
```
SurpriseSignal {
  rejected_assertion: temperature(cell_1, 92°C) ∧ status(cell_1, nominal),
  confidence: 0.95,
  blocking_constraints: [MutualExclusion(nominal_status, above_threshold_temp)],
  interpretation_alternatives: [
    {alternative: status(cell_1, thermal_warning), coherent: true},
    {alternative: sensor_malfunction(temp_sensor_1), coherent: true}
  ],
  learning_trigger: null  // No ontology gap, just state conflict
}
```

**Epistemic Layer decision**: Check secondary temperature sensors. If confirmed, update status to thermal_warning and initiate cooling process.

---

*End of specification.*
