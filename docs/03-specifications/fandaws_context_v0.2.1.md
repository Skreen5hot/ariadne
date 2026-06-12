# Context Domain Framework for Scaled Agents

```
Document: Context Domain Framework (fandaws-context)
Version:  v0.2.1
Status:   Formal specification
Purpose:  Architecture for a shared enterprise world model and per-agent
          perspective models, built on the Fandaws universal semantic layer
Scope:    Planning and formal commitments; not a TTL file
```

---

## 0. Dependencies

| Document | Version | Status | Binding |
|----------|---------|--------|---------|
| Basic Formal Ontology (BFO) | 2020 | ISO/IEC 21838-2 | Normative |
| Common Core Ontologies (CCO) | 2.0 | Release | Normative |
| Fandaws Semantic Layer | 3.0 | Specification | Normative |
| apqc-catalog | 1.0 | Specification | Normative |
| apqc-reality | 1.0 | Specification | Normative |
| apqc-performance | 0.2.0 | Specification | Normative |
| SHML (Semantically Honest Middle Layer) | 3.0 | White paper | Informative |
| HIRI Protocol | 1.4.1 | Specification | Normative |
| World Models as Semantic Infrastructure | 2.0 | Position paper | Informative |

**Maturity note:** HIRI Protocol v1.4.1 is pinned; implementers should not assume forward compatibility with v1.5+. SHML v3.0 and the World Models paper are informative (architectural rationale) not normative (conformance requirements).

---

## 1. Problem Statement

A business running many agents pays a recurring tax: every new agent, and every new task, requires re-supplying context about the business and its landscape. The desired end state:

- A **shared world model** of the business and its external landscape, built incrementally as agents work—never assembled in one heroic effort.
- A **perspective model per agent**: its history, capabilities, commitments, and its view of (and disagreements with) the shared model.
- Fandaws as the semantic layer guaranteeing that all of it means the same thing to every agent.

Two open questions block this, and this document exists to answer them:

```
Q1 (Filtering): World models cannot save everything. By what principle do
    experiences and details get kept, compressed, or discarded?

Q2 (Access): How does an agent get exactly the context appropriate to its
    task, efficiently, without reading the whole graph?
```

### 1.1 Relationship to SHML Architecture

This document operationalizes the Semantically Honest Middle Layer (SHML v3.0) for multi-agent enterprise deployment. The architectural mapping:

| SHML Layer | fandaws-context Mapping |
|------------|------------------------|
| Reality Layer (BFO) | S0 Semantic stratum (Fandaws types, BFO-grounded) |
| SHML Middle Layer | T1-T2 (TypedEvent, Claim) in LPG substrate |
| Logic Layer (RDF) | T3-T4 (CanonicalAssertion, Generalization) projected to RDF |
| Projection function π | ContextAssemblyAct producing ContextBundle |
| Belief scopes | Agent perspective models (PrivateStore + SyncState) |
| CIC validation | Promotion spine with salience gates and review tiers |

---

## 2. Design Principles

**P1 — The unit of memory is the claim, not the event.** Events are evidence. What the world model stores durably are *claims about the world* (typed, provenance-bearing assertions); raw events are retained only as evidence behind claims, with a time-to-live. This single move converts "what do we save?" from a storage question into a knowledge question.

**P2 — Filter at promotion, not at capture.** Capture is cheap; judgment is expensive. Record everything into a cheap append-only log, then apply intelligence at each promotion boundary between memory tiers. Nothing is judged at write time except type-binding.

**P3 — Relevance is decision-anchored.** "Important" is undefined until you ask: *important to which recurring decision?* The `DecisionContext` class from apqc-performance v0.2.0 is reused as the anchor of relevance, extended with explicit anchor bindings (§2.1). An experience that cannot change any registered decision decays fast.

**P4 — A perspective is a view, not a copy.** Agent world models are not forks of the shared graph. They are (a) a defined view over the shared model, (b) a private store of assessments and claims, and (c) a sync state recording what the agent has seen. Copies drift; views and deltas do not.

**P5 — One governance spine, reused.** The promotion pipeline uses the *same pattern* as apqc-performance §4.5: **immutable artifact cores with reified status assertions**. Artifacts are HIRI-signed and never mutated; status changes are separate signed records *about* them. This preserves cryptographic integrity while supporting lifecycle transitions.

**P6 — Disagreement is data.** An agent's claim that conflicts with the canonical model is not an error to suppress; it is a signal (reusing `DetectedSignal`) that triggers review. This is how the shared model improves and how agent reliability becomes measurable.

**P7 — Determinism has an honest boundary.** Extraction (T0→T1) and entity resolution are non-deterministic; they are isolated behind explicit gates with HIRI-marked provenance. The determinism boundary starts *after* extraction. Salience scoring, context assembly, and conflict detection are computable functions over typed artifacts.

**P8 — Cryptographic provenance via HIRI.** All artifact cores are HIRI-addressed (content-addressed, immutable, Ed25519-signed). Status, locks, and trust observations are separate signed assertion records *about* artifacts. This maintains integrity while permitting lifecycle state changes.

### 2.1 DecisionContextBinding (Extension to apqc-performance)

apqc-performance v0.2.0 defines `DecisionContext` with question/role/cadence/scope. This spec extends it with explicit anchor bindings for salience computation:

```
DecisionContextBinding (extends DecisionContext usage in this spec):
  decisionContext:    IRI (reference to apqc-performance DecisionContext)
  anchorEntities:     [IRI] (entities whose state affects this decision)
  monitoredVariables: [IRI] (KPIs/metrics relevant to decision)
  relevanceRadius:    Int (max graph hops from anchors, default: 3)
```

This binding is a local extension; it does not modify apqc-performance itself.

---

## 3. World Model Strata

The shared world model is stratified by **rate of change**, which directly determines how each stratum is accessed (§7).

| Stratum | Contents | Change rate | Access mode |
|---------|----------|-------------|-------------|
| S0 Semantic (Fandaws) | Types, relations, identity criteria | ~quarterly | Compiled into agent definitions |
| S1 Structural | The business: org units, products, processes, channels, systems, standing policies | ~monthly | Cached snapshot per agent, delta-synced |
| S2 Relational | The landscape: customers, suppliers, competitors, regulators, partners | ~weekly | Anchored retrieval + delta sync |
| S3 Situational | Current state: open orders, active issues, KPI observations, in-force signals | ~hourly/daily | Fetched per task, never cached |
| S4 Episodic | What happened: events, interactions, completed acts | continuous | Evidence-only; reached via claims |

### 3.1 Schema Evolution Discipline

S0 changes (~quarterly) trigger a migration protocol:

```
S0 Schema Evolution Protocol:

1. Assertion Audit
   For each type T in ΔS0 (changed types):
     affected_assertions ← {A ∈ T3 : A references T}
     Log: AffectedAssertionReport(T, |affected_assertions|)

2. Migration Directive (human-authored, HIRI-signed)
   For each deprecated type T_old:
     Define: migration_path(T_old) → T_new OR deprecation_summary
   For each refined type T_refined:
     Define: compatibility_mode ∈ {backward_compatible, retyping_required}

3. Assertion Migration
   For each A in affected_assertions:
     If migration_path exists:
       A' ← retype(A, migration_path)  # new artifact, new HIRI
       Create: StatusAssertion(A.hiri, status=superseded, superseded_by=A'.hiri)
     Else:
       Create: StatusAssertion(A.hiri, status=deprecated_orphan)
       Log: OrphanedAssertionWarning(A)

4. Agent Recompilation Queue
   For each AgentProfile P where P.contextProfile references changed types:
     Queue: RecompilationTask(P, S0.version_new)

5. Version Bump
   S0.version ← increment(S0.version)
   Invalidate: all SyncState markers referencing S0.version_old
```

### 3.2 Agent Perspective Model

Per agent (implementing P4):

```
AgentProfile (immutable core, HIRI-signed)
  agentKind:        IRI (stable across versions, e.g., :SupportOpsAgent)
  agentVersion:     SemVer (e.g., "1.2.0")
  agentInstance:    HIRI (unique instance identifier)
  capabilities:     [Capability] (version-specific declarations)
  roleAssignments:  [RoleAssignment]
  
ContextProfile (immutable directive ICE, HIRI-signed)
  servesDecisions:       [DecisionContextBinding] (which decisions, with anchors)
  entityNeighborhoods:   [GraphPattern] (typed patterns, not enumerated lists)
  stratumSubscriptions:  [StratumSubscription]
  budgetAllocation:      BudgetAllocation (see §7.2)
  
PrivateStore (per agent)
  salienceAssessments:  [SalienceAssessment] (agent's scoring of shared events)
  privateClaims:        [Claim] (unpromoted or rejected claims)
  
SyncState
  stratumMarkers:   Map<Stratum, VersionMarker>
  lastSync:         Timestamp
```

**TrustRecord** is not a mutable property but an aggregation of **TrustObservation** records (§5.3.3).

---

## 4. Memory Tiers and the Promotion Spine

```
T0  RawEvent            append-only log; full fidelity; TTL (e.g. 90 days);
                        never queried by agents directly; HIRI-addressed
                        
T1  TypedEvent          shared, Fandaws-typed event extracted from T0;
                        output of ExtractionAct; medium TTL; one per event
                        
    SalienceAssessment  per-agent scoring of a TypedEvent; links to T1 event
                        and agent's ContextProfile; agent-scoped
                        
T2  Claim               a proposed assertion about the world, extracted from
                        one or more TypedEvents; carries provenance, confidence

T3  CanonicalAssertion  a claim promoted into the shared world model;
                        immutable core, versioned, governed

T4  Generalization      an induced pattern over many assertions/events;
                        always requires human review
```

**Key change from v0.2.0:** T1 is now split:
- **TypedEvent** (shared): the extraction output, created once per raw event
- **SalienceAssessment** (per-agent): the scoring, created per subscribing agent

This resolves the "who is the experiencing agent?" question for external documents.

### 4.1 Immutable Cores and Reified Status (P5, P8)

All artifacts are immutable once HIRI-signed. Lifecycle state is managed through separate status assertions:

```
Artifact Core (immutable):
  hiri:       HIRI (content-addressed identifier)
  content:    <artifact-specific content in JSON-LD canonical form>
  author:     HIRI (author's public key or agent HIRI)
  signature:  Ed25519.sign(content, author_private_key)
  timestamp:  ISO8601

StatusAssertion (separate record, also HIRI-signed):
  subject:     HIRI (the artifact this is about)
  status:      Enum (see below)
  effective:   ISO8601 (when this status took effect)
  author:      HIRI (who made this status assertion)
  supersedes:  HIRI? (previous StatusAssertion for this subject, if any)
  
Status values by tier:
  T1 TypedEvent:      {active, decayed, tombstoned}
  T2 Claim:           {candidate, under_review, promoted, rejected, expired}
  T3 CanonicalAssertion: {validated, superseded, archived, deprecated_orphan}
  T4 Generalization:  {proposed, under_review, validated, weakening, invalidated}
```

**Invariant:** To determine an artifact's current status, query the most recent StatusAssertion for that artifact's HIRI. The artifact core itself is never modified.

**Provenance chain integrity:** Because artifacts are immutable and status is external, HIRI references in provenance chains remain valid regardless of status changes.

### 4.2 Evidence Lifecycle: Bounded Locks and Tombstones

The retention invariant must allow T0 to expire while preserving integrity verification:

```
Evidence Retention Model:

Lock Scope:
  RetentionLockAssertion applies only to T1 and T2 artifacts.
  T0 (RawEvent) is never locked; it expires per TTL policy.

When Claim C is promoted to CanonicalAssertion A:
  For each TypedEvent E in C.provenance_chain (T1 level):
    Create: RetentionLockAssertion(E.hiri, locked_by=A.hiri)
  # T0 events referenced by E are NOT locked

When A transitions to status=superseded:
  For each E in A.provenance_chain:
    other_locks ← {A' : A'.status = validated AND E.hiri ∈ A'.provenance}
    If other_locks = ∅:
      Create: RetentionLockAssertion(E.hiri, locked=false)

T0 Tombstone Protocol:
  When RawEvent R expires (TTL reached):
    1. Create: Tombstone {
         original_hiri: R.hiri,
         content_hash: SHA256(R.content),  # redundant with HIRI but explicit
         tombstoned_at: now(),
         summary: one-line description (optional)
       }
    2. Delete: R.content (bytes released)
    3. Retain: R.hiri → Tombstone mapping

Integrity Verification:
  Given TypedEvent E with provenance pointer to RawEvent R:
    If R exists: verify R.hiri = hash(R.content) ✓
    If R is tombstoned: 
      verification = "evidence expired; hash {content_hash} was valid at extraction"
      # Integrity of E is preserved; E's own HIRI covers its content
      # The claim "E was extracted from R" remains true; R's bytes are gone
```

**Invariant (revised):** For every artifact A with status=validated, every T1/T2 artifact in A's provenance chain either (a) exists with retention lock, or (b) has a tombstone with verifiable hash. T0 may be tombstoned after TTL.

This resolves the "T0 immortal" contradiction: the system *can* forget raw evidence while maintaining cryptographic proof of what was forgotten.

### 4.3 The Promotion Spine

```
Raw observation
→ RawEvent (T0, HIRI-signed, TTL-bounded)
→ ExtractionAct (NON-DETERMINISTIC, HIRI-marked)
→ TypedEvent (T1, shared)
→ SalienceAssessmentAct (per subscribing agent, DETERMINISTIC)
→ SalienceAssessment (agent-scoped)
→ ClaimExtractionAct (from high-salience assessments)
→ Claim (T2)
→ ClaimReviewAct (curator role)
→ CanonicalAssertion (T3) + StatusAssertion(status=validated)
→ GeneralizationProposalAct (periodic)
→ CandidateGeneralization + StatusAssertion(status=proposed)
→ GeneralizationReviewAct (human gate)
→ StatusAssertion(status=validated) for Generalization
→ DecayAct → Tombstone (T0) or StatusAssertion(status=decayed) (T1)
```

---

## 5. Q1 Answered: The Filtering Model

Filtering is four gates plus scheduled forgetting.

### 5.1 Gate 0 — Extraction Gate (T0 → T1) — NON-DETERMINISTIC

**Honest acknowledgment:** Converting a raw event (PDF, transcript, sensor log) into a Fandaws-typed TypedEvent is information extraction. This is non-deterministic.

```
ExtractionAct (class, HIRI-signed):
  input:           RawEvent.hiri
  output:          TypedEvent.hiri (if successful) OR ExtractionFailure
  extractor:       HIRI (agent, model, or system that performed extraction)
  method:          Enum {llm_extraction, rule_based, human_annotation, system_native}
  non_deterministic: true  # always true for this act type
  confidence:      Float [0,1] (extractor's self-assessed confidence)

TypedEvent (output):
  hiri:            HIRI (content-addressed)
  source:          RawEvent.hiri (provenance)
  extracted_by:    ExtractionAct.hiri
  event_type:      IRI (Fandaws event type)
  participants:    [EntityReference] (resolved or candidate)
  temporal_extent: TemporalRegion
  content:         structured representation per event_type
```

**Entity Resolution:** Also non-deterministic. EntityReferences may be:
- `resolved`: exact match to existing entity IRI
- `candidate`: proposed new entity, pending validation
- `ambiguous`: multiple possible referents, flagged for review

```
EntityReference:
  surface_form:    String (as it appeared in raw event)
  resolution:      Enum {resolved, candidate, ambiguous, failed}
  resolved_iri:    IRI? (if resolved)
  candidates:      [IRI]? (if ambiguous)
  confidence:      Float
```

**Determinism boundary:** The determinism guarantee (P7) starts *after* ExtractionAct completes. From TypedEvent onward, all operations are deterministic given the graph state.

### 5.2 Gate 1 — Schema Gate (at ExtractionAct)

An extraction succeeds only if the output binds to Fandaws types:

```
Schema Gate (embedded in ExtractionAct validation):
  Input: candidate TypedEvent E
  
  Validation (DETERMINISTIC):
    1. E.event_type ∈ S0.event_types? 
    2. ∀ ref ∈ E.participants: 
         ref.resolution ≠ failed AND
         (ref.resolved_iri.type ∈ S0.entity_types OR ref.resolution = candidate)
    3. E.temporal_extent valid per BFO TemporalRegion constraints?
    
  If all pass: E admitted to T1
  If any fail: ExtractionFailure logged; RawEvent remains in T0, dies with TTL
```

The gate's accept/reject decision is deterministic; the production of the candidate is not.

### 5.3 Gate 2 — Salience Gate (T1 → T2) — DETERMINISTIC, PROFILE-SCOPED

A `SalienceAssessmentAct`, prescribed by a versioned `SalienceModelSpecification`, scores each TypedEvent **per subscribing agent's ContextProfile**.

#### 5.3.1 Salience Dimensions Formalized

**All dimensions are computable from the graph. All scoring is profile-scoped.**

```
SalienceAssessment (per agent, per TypedEvent):
  event:           TypedEvent.hiri
  profile:         ContextProfile.hiri (the assessing agent's profile)
  model_version:   SalienceModelSpecification.version
  
  scores:
    novelty:       Float [0,1]
    decision:      Float [0,1]  # relative to THIS agent's served decisions
    commitment:    Float [0,1]
    authority:     Float [0,1]
    recurrence:    Float [0,1]
    
  weighted_total:  Float [0,1]
  disposition:     Enum {below_threshold, promote_to_claim, high_priority}
```

**Dimension 1: Novelty (contradiction/extension against T3)**

```
novelty(E) = max(contradiction_score(E), extension_score(E))

contradiction_score(E):
  contradicting ← {A ∈ T3 : 
    status(A) = validated AND
    contradicts(E.content, A.content, IncompatibilityAxiomSet)
  }
  If contradicting ≠ ∅:
    Return max({confidence(A) : A ∈ contradicting})
  Else:
    Return 0.0

extension_score(E):
  entities ← {ref.resolved_iri : ref ∈ E.participants, ref.resolution = resolved}
  For each X ∈ entities:
    If X ∉ any T3 assertion: Return 0.8  # new entity
    relations_asserted ← {R : E asserts R(X, _)}
    relations_known ← {R : ∃ A ∈ T3, status(A) = validated, A asserts R(X, _)}
    If relations_asserted \ relations_known ≠ ∅: Return 0.7  # new relation type
    targets_asserted ← {Y : E asserts R(X, Y) for known R}
    targets_known ← {Y : ∃ A ∈ T3, A asserts R(X, Y)}
    If targets_asserted \ targets_known ≠ ∅: Return 0.5  # new target
  Return 0.2  # confirms existing

contradicts(content1, content2, axioms):
  # Structural contradiction: same subject, same relation, incompatible values
  # Incompatibility defined by IncompatibilityAxiomSet (see §5.3.2)
  # Returns true iff axioms declare value conflict
```

**Dimension 2: Decision Relevance (PROFILE-SCOPED)**

```
decision(E, Profile) =
  max over D ∈ Profile.servesDecisions:
    decision_relevance(E, D)

decision_relevance(E, D):
  entities ← {ref.resolved_iri : ref ∈ E.participants, ref.resolution = resolved}
  anchors ← D.anchorEntities ∪ D.monitoredVariables
  
  min_distance ← min over (e, a) ∈ entities × anchors:
    graph_distance(e, a, D.relevanceRadius)
  
  Return distance_to_relevance(min_distance)

distance_to_relevance(d):
  # Using 1/(1+d) to avoid division by zero at d=0
  If d = ∞: Return 0.0
  Return 1.0 / (1.0 + d)
  # d=0 → 1.0, d=1 → 0.5, d=2 → 0.33, d=3 → 0.25, d=4 → 0.2

graph_distance(e1, e2, max_depth):
  # BFS in S1-S2 graph
  # All edges have weight 1 (no differential weighting in v0.2.1)
  # Returns hop count or ∞ if not reachable within max_depth
```

**Dimension 3: Commitment Relevance**

```
commitment(E, Profile):
  entities ← {ref.resolved_iri : ref ∈ E.participants}
  agent_commitments ← OpenTasks(Profile.agent) ∪ 
                      InForceSignals(routed_to=Profile.agent) ∪
                      PendingGoals(Profile.agent)
  
  matching ← {C ∈ agent_commitments : C.references ∩ entities ≠ ∅}
  If matching = ∅: Return 0.0
  Return max({priority_weight(C) : C ∈ matching})

priority_weight(C):
  critical: 1.0, high: 0.8, medium: 0.5, low: 0.3
```

**Dimension 4: Authority**

```
authority(E):
  Return source_authority(E.source_type) × method_authority(E.extraction_method)

# Weights defined in AuthoritySpecification (directive ICE, Appendix B)
```

**Dimension 5: Recurrence (grounded in entity IRIs)**

```
recurrence(E):
  similar ← {E' ∈ T1 : 
    E'.timestamp < E.timestamp AND
    E'.source ≠ E.source AND
    content_similarity(E', E) > 0.7
  }
  Return min(1.0, |similar| × 0.25)

content_similarity(E1, E2):
  # Jaccard over (entity_iri, relation_type) pairs
  # Grounded in entity IRIs, not just types
  pairs(E) = {(e.resolved_iri, type(r)) : E asserts r(e, _), e.resolution = resolved}
  
  If pairs(E1) = ∅ OR pairs(E2) = ∅: Return 0.0
  Return |pairs(E1) ∩ pairs(E2)| / |pairs(E1) ∪ pairs(E2)|
```

#### 5.3.2 IncompatibilityAxiomSet

Contradiction detection requires explicit axioms declaring when values conflict:

```
IncompatibilityAxiomSet (directive ICE, HIRI-signed):
  owner:         WorldModelStewardRole bearer
  axioms:        [IncompatibilityAxiom]
  
IncompatibilityAxiom:
  relation:      IRI (the relation type)
  incompatible:  IncompatibilityType
  
IncompatibilityType:
  | functional    # R(X,Y) and R(X,Z) contradict if Y≠Z
  | exclusive_values(values: [IRI])  # listed values mutually exclusive
  | numeric_direction  # "increasing" vs "decreasing" contradict
  | custom(sparql: String)  # SPARQL ASK pattern

Example axioms:
  (hasMarketStrategy, exclusive_values([Expanding, Exiting, Maintaining]))
  (hasHeadquarters, functional)
  (trend, numeric_direction)
```

**Semantic contradictions outside the axiom set pass silently.** This is by design—the system is conservative about claiming contradiction.

#### 5.3.3 Salience Aggregation

```
SalienceModelSpecification (directive ICE, Appendix B is authoritative):
  weights:
    novelty:     0.20
    decision:    0.40
    commitment:  0.15
    authority:   0.15
    recurrence:  0.10
  
  thresholds:
    promotion_threshold:   0.45
    high_priority:         0.70
```

**Determinism verification:** Given the same TypedEvent, ContextProfile, T3 state, and SalienceModelSpecification, the SalienceAssessment is identical. This is testable.

#### 5.3.4 Enterprise Watchdog

To prevent enterprise-critical events from falling through because no agent's profile covers them:

```
WatchdogProfile (special ContextProfile):
  servesDecisions: [ALL registered DecisionContextBindings]
  entityNeighborhoods: [ALL S1/S2 entity types at depth 2]
  budgetAllocation: minimal (watchdog flags, doesn't act)
  
WatchdogAssessment:
  Runs after all agent assessments complete
  For each TypedEvent E where:
    max(agent_salience_scores(E)) < promotion_threshold AND
    watchdog_salience_score(E) ≥ watchdog_threshold:
      Create: UncoveredEventSignal(E, watchdog_score)
      Route to: WorldModelStewardRole

# Watchdog catches events that are globally relevant but locally invisible
```

### 5.4 Gate 3 — Review Gate (T2 → T3) — DETERMINISTIC ROUTING

Claims are promoted by `ClaimReviewAct`. Review rules are tiered by blast radius:

```
ClaimReviewRule (directive ICE):

auto_promote:
  conditions:
    - claim.target_stratum = S3 AND
    - claim.source_authority ≥ 0.9 AND
    - claim.contradiction_count = 0
    
agent_review:
  conditions:
    - claim.target_stratum = S2 AND
    - claim.contradiction_count = 0
  reviewer: agent bearing CuratorRole, agent ≠ claim.author
  
human_review:
  conditions:
    - claim.target_stratum = S1 OR
    - claim.contradiction_count > 0 OR
    - claim.affects_policy = true
  reviewer: human bearing WorldModelStewardRole
```

**Conflict Resolution Protocol:**

```
When ClaimReviewAct detects contradiction:

Input: Claim C_new contradicting CanonicalAssertion A_existing

1. Signal Generation
   Create: ContradictionSignal {
     type: ContradictionSignal,
     new_claim: C_new.hiri,
     existing_assertion: A_existing.hiri,
     severity: C_new.salience_score × current_status_confidence(A_existing)
   }

2. Trust Comparison (scoped by stratum)
   author_trust ← trust_score(C_new.author, C_new.target_stratum)
   existing_trust ← trust_score(A_existing.author, A_existing.stratum)
   
3. Routing
   If author_trust = undefined (cold start):
     Route to human_review (conservative default)
   Else if author_trust - existing_trust > 0.2:
     Route to agent_review with priority flag
   Else:
     Route to human_review
     
4. Pending State
   Create: StatusAssertion(C_new.hiri, status=under_review)
   # A_existing status unchanged; not destabilized by challenge
   
5. Resolution Outcomes (reviewer decision)
   a) Supersession:
      Create: StatusAssertion(A_existing.hiri, status=superseded, superseded_by=C_promoted.hiri)
      Create: CanonicalAssertion from C_new → C_promoted
      Create: StatusAssertion(C_promoted.hiri, status=validated)
      Create: TrustObservation(C_new.author, outcome=promoted, stratum=...)
      
   b) Rejection:
      Create: StatusAssertion(C_new.hiri, status=rejected)
      Create: TrustObservation(C_new.author, outcome=rejected_contradicted, stratum=...)
      
   c) Scoping:
      Both valid in different contexts
      Create: ScopeBoundary(A_existing, scope_condition_A)
      Create: ScopeBoundary(C_promoted, scope_condition_C)
      Both remain validated with scope annotations
      
   d) Synthesis:
      Neither fully correct
      Human creates A_synthesized
      Create: StatusAssertion(A_existing.hiri, status=superseded)
      Create: StatusAssertion(C_new.hiri, status=superseded)
      Create: StatusAssertion(A_synthesized.hiri, status=validated)
```

#### 5.4.1 TrustRecord as Aggregation

TrustRecord is not a mutable artifact but a computed view over TrustObservation records:

```
TrustObservation (immutable, HIRI-signed):
  subject:       AgentProfile.hiri
  stratum:       Stratum (trust is domain-scoped)
  outcome:       Enum {promoted, rejected_contradicted, rejected_quality, ...}
  claim:         Claim.hiri (the claim this observation is about)
  timestamp:     ISO8601
  observer:      HIRI (reviewer who made this judgment)

trust_score(agent, stratum):
  observations ← {T : T.subject = agent.hiri AND T.stratum = stratum}
  If observations = ∅:
    Return undefined  # cold start
  promoted ← |{T : T.outcome = promoted}|
  total ← |observations|
  Return promoted / total
  
# Note: This metric conflates calibration with selectivity.
# An agent submitting only safe claims earns high trust.
# Acknowledged as open question in §14.
```

### 5.5 Scheduled Forgetting

```
ConsolidationAct (periodic):
  1. Merge: duplicate claims → combined evidence chains
  2. Propose: generalizations from patterns (§6)
  3. Decay: unreferenced content
  
DecayAct:
  For TypedEvent E where:
    - No SalienceAssessment has disposition ≠ below_threshold
    - E.age > retention_policy.unclaimed_ttl
    Create: StatusAssertion(E.hiri, status=decayed)
    # Content may be archived or tombstoned per policy
    
  For T0 RawEvent R where:
    - R.age > retention_policy.raw_ttl
    Execute: Tombstone Protocol (§4.2)
```

---

## 6. Generalization Induction (T4)

### 6.1 Design Constraints

Generalization must:
1. Isolate non-determinism behind explicit gates
2. Produce HIRI-signed artifacts
3. Require human review before affecting decisions
4. Be expressible in Fandaws types

### 6.2 Three Strategies

**Strategy A: Template-Based (Fully Deterministic)**
Pre-defined patterns with slots; machine populates from data.

**Strategy B: Structural Mining (Mining Deterministic, Labeling Human)**
Frequent subgraph detection; human assigns meaning.

**Strategy C: LLM-Assisted (Explicitly Non-Deterministic)**
LLM proposes; all proposals require human review; marked `non_deterministic: true`.

See Appendix C for template library.

### 6.3 Generalization Lifecycle

```
CandidateGeneralization
  + StatusAssertion(status=proposed)
→ GeneralizationReviewAct (human gate, always)
→ StatusAssertion(status=validated)
→ periodic: GeneralizationValidationAct
   # Check if pattern still holds
   # May create: StatusAssertion(status=weakening) or (status=invalidated)
```

Generalizations enter ContextBundles as **advisory content**, clearly marked.

---

## 7. Q2 Answered: The Access Model

### 7.1 Stratum-Matched Delivery

| Stratum | Delivery Mode |
|---------|--------------|
| S0 | Compiled into agent definition |
| S1 | Cached + delta-sync |
| S2 | Cached + delta-sync |
| S3 | Fetched fresh per task |
| S4 | Evidence-only via provenance |

### 7.2 Budget Allocation (Deterministic)

```
BudgetAllocation:
  total_tokens:    8000  # fixed per agent kind
  tokenizer:       "cl100k_base"  # PINNED for determinism
  
  allocation_ratios:
    S1_structural:      0.15
    S2_relational:      0.25
    S3_situational:     0.30
    T4_generalizations: 0.10
    private_claims:     0.10
    task_specific:      0.10
    
  overflow_strategy: truncate_by_salience
  
  per_request_override: Boolean  # if true, request may specify different ratios
                                 # override recorded in audit log
```

**Overflow Protocol:**
```
For stratum S with budget B_S:
  candidates ← query(S, filter=Profile patterns)
  If token_count(candidates) ≤ B_S:
    include all
  Else:
    ranked ← sort(candidates, by=salience_score, descending)
    # Note: no double-counting with graph distance; salience already includes it
    include until budget exhausted
    Log: TruncationRecord(excluded items, their salience scores)
```

### 7.3 Task-Time Assembly

```
ContextAssemblyAct:

Input: ContextRequest {task_description, agent_identity, budget_override?}

1. Entity Resolution (NON-DETERMINISTIC component)
   task_entities ← extract_entities(task_description)  # may use LLM
   # Resolution attempts are logged; ambiguity is flagged
   
2. Anchor Binding (DETERMINISTIC from here)
   anchors ← resolved(task_entities) ∪ Profile.permanent_anchors
   relevant_decisions ← {D ∈ Profile.servesDecisions : D.anchors ∩ anchors ≠ ∅}

3. Canonical Neighborhood Retrieval
   For each stratum in Profile.subscriptions:
     candidates ← graph_query(stratum, root=anchors, pattern=Profile.neighborhoods)
     included, truncated ← apply_budget(candidates, allocation[stratum])

4. Private Claims Overlay
   private ← query(agent.PrivateStore, references ∩ anchors ≠ ∅)
   For each claim C in private:
     If contradicts(C, any canonical assertion):
       C.annotation ← "own-view-divergent"
   included_private ← apply_budget(private, allocation.private)

5. Situational State (S3)
   situational ← query(S3, touches anchors OR affects relevant_decisions)
   signals ← query(InForceSignals, routed_to=agent)
   included_S3 ← apply_budget(situational ∪ signals, allocation.S3)

6. Generalizations (T4)
   applicable ← query(T4, references ∩ anchors ≠ ∅, status=validated)
   included_T4 ← apply_budget(applicable, allocation.T4)

7. Bundle Assembly
   bundle ← ContextBundle {
     hiri: computed,
     contents: all included items,
     truncation_records: all truncation logs,
     stratum_versions: current version per stratum,
     profile_version: Profile.hiri,
     salience_model_version: current,
     budget_allocation_used: actual allocation (may include override),
     entity_resolution_log: from step 1
   }

Output: ContextBundle (HIRI-signed)
```

### 7.4 Audit Logging

```
ContextAssemblyAuditRecord:
  bundle_hiri:            HIRI
  request_hiri:           HIRI
  agent_hiri:             HIRI
  profile_version:        HIRI
  stratum_versions:       Map<Stratum, Version>
  salience_model_version: Version
  
  entity_resolution_log:  [EntityResolutionAttempt]  # non-deterministic component
  truncation_events:      [TruncationRecord]
  budget_override:        BudgetAllocation? (if used)
  
Attribution Queries:
  "Was bundle B correctly assembled per profile P?"
  → Deterministic replay from stratum_versions; compare contents
  → Discrepancy = broker fault
  
  "Could agent A have known fact F when performing act X?"
  → Find bundle B for act X
  → If F ∈ B.contents: agent had access (agent responsibility)
  → If F excluded by truncation: budget/profile design issue
  → If F outside profile neighborhoods: profile design issue
  → If F not yet in canonical model: timing (no fault)
```

### 7.5 Access Control Matrix

```
Artifact Type          | Read Access                           | Write Access
-----------------------|---------------------------------------|---------------------------
S0 Types               | All agents                            | OntologySteward only
S1 Assertions          | By ContextProfile subscription        | By role + human review
S2 Assertions          | By ContextProfile subscription        | By role + review gate
S3 Assertions          | By ContextProfile subscription        | Authorized systems (§7.6)
T4 Generalizations     | By ContextProfile subscription        | Human steward only
PrivateStore           | Owning agent + ContextBroker + audit  | Owning agent only
ContextProfile         | Owning agent + steward                | Steward only
TrustObservation       | Aggregation query by any; raw by audit| System only (from review acts)
ContextBundle          | Requesting agent + audit              | System only (ContextBroker)
RawEvent (T0)          | Via provenance chain only             | Append-only (ingestion systems)

Authorized S3 Writers:
  Systems registered in S3WriterRegistry (directive ICE)
  Each entry: system_hiri, allowed_assertion_types, rate_limit
```

### 7.6 Key Lifecycle (MVP Scope)

```
MVP Key Model:
  - Single trust domain (enterprise boundary)
  - Platform-held keys: agent keys are generated and held by the platform
  - No agent-controlled private keys in MVP
  - Key rotation: platform rotates all keys on schedule (e.g., quarterly)
  - Revocation: platform can revoke agent key; all signatures remain valid
    but StatusAssertion(agent, status=revoked) prevents new acts
  
Post-MVP:
  - Agent-controlled keys (for cross-enterprise federation)
  - Explicit rotation protocol with key versioning
  - Revocation lists with grace periods
```

---

## 8. MVP Class Set

**Count verification: 38 classes** (list follows)

Inclusion rule: exercised by §11 validation loop OR required for structural integrity.

```
Strata & Infrastructure (5)
  WorldModelStratum          (named individuals: S1, S2, S3, S4)
  CanonicalAssertion
  Generalization
  CandidateGeneralization
  Tombstone

Memory Pipeline (12)
  RawEvent                   (T0; outside graph, HIRI-addressed)
  TypedEvent                 (T1; shared extraction output)
  SalienceAssessment         (per-agent scoring of TypedEvent)
  Claim
  SalienceScore              (embedded in SalienceAssessment)
  ExtractionFailure
  EntityReference
  SalienceModelSpecification (directive, Appendix B)
  AuthoritySpecification     (directive, Appendix B)
  RetentionPolicySpecification (directive)
  ClaimReviewRule            (directive)
  IncompatibilityAxiomSet    (directive)

Status & Lifecycle (3)
  StatusAssertion
  RetentionLockAssertion
  TrustObservation

Acts (9)
  ExtractionAct
  SalienceAssessmentAct
  ClaimExtractionAct
  ClaimReviewAct
  ConsolidationAct
  DecayAct
  ContextAssemblyAct
  GeneralizationProposalAct
  GeneralizationReviewAct

Agent Perspective (5)
  AgentProfile
  ContextProfile             (directive)
  DecisionContextBinding     (extension for this spec)
  PrivateStore
  SyncState

Access (4)
  ContextRequest
  ContextBundle
  TruncationRecord
  ContextAssemblyAuditRecord

Roles (4)
  CuratorRole
  ContextBrokerRole
  WorldModelStewardRole
  OntologyStewardRole

Signals (2)
  ContradictionSignal        (extends DetectedSignal)
  UncoveredEventSignal

Generalization Support (2)
  GeneralizationPolicySpecification
  ScopeBoundary

Watchdog (1)
  WatchdogProfile            (special ContextProfile)

Registry (1)
  S3WriterRegistry
```

**D13 compliance check:**
- ScopeBoundary: exercised in conflict resolution path (outcome c)
- GeneralizationReviewAct: exercised in generalization validation step
- OntologyStewardRole: exercised in schema evolution protocol
- All classes instantiated by explicit loop steps in §11

---

## 9. Worked Example: One Event, Four Perspectives (Corrected)

The hearing aid company runs four agents: **MarketIntel**, **RegAffairs**, **SupportOps**, **SupplyChain**.

Event: *FDA publishes updated labeling guidance for OTC hearing aids.*

### Extraction (Non-Deterministic, T0→T1)

```
RawEvent R:
  hiri: hiri:sha256:abc123...
  content: <PDF bytes>
  source: FDA website
  ingested: 2024-12-15T09:00:00Z

ExtractionAct:
  input: R.hiri
  extractor: :DocumentExtractionService_v2
  method: llm_extraction
  non_deterministic: true
  confidence: 0.92

TypedEvent E (output):
  hiri: hiri:sha256:def456...
  event_type: :RegulatoryGuidancePublication
  participants:
    - {surface: "FDA", resolution: resolved, iri: :FDA}
    - {surface: "OTC hearing aids", resolution: resolved, iri: :OTC_ProductLine}
    - {surface: "labeling guidance", resolution: resolved, iri: :LabelingGuidance_2024}
  temporal_extent: 2024-12-15
  extracted_by: ExtractionAct.hiri
```

### Salience Assessment (Deterministic, Profile-Scoped)

**RegAffairs** (serves "Labeling Compliance" decision):
```
decision_relevance:
  anchors(LabelingCompliance) = {:OTC_ProductLine, :FDA, :LabelingRequirements}
  E.participants ∩ anchors = {:OTC_ProductLine, :FDA}
  min_distance = 0  → relevance = 1/(1+0) = 1.0

novelty:
  E asserts :LabelingGuidance_2024 supersedes :LabelingGuidance_2020
  Existing T3: :OTC_ProductLine governed_by :LabelingGuidance_2020 (validated)
  contradicts() per axiom (functional relation) → contradiction_score = 1.0 × 0.95 = 0.95
  novelty = 0.95

commitment:
  Open task "Annual compliance review" references :OTC_ProductLine
  commitment = 1.0 × 0.8 (high priority) = 0.8

authority:
  source: regulatory_filing → 1.0
  method: llm_extraction → 0.8
  authority = 0.8

recurrence: 0.0 (first occurrence)

weighted_total:
  (0.95×0.2) + (1.0×0.4) + (0.8×0.15) + (0.8×0.15) + (0×0.1)
  = 0.19 + 0.40 + 0.12 + 0.12 + 0
  = 0.83

disposition: high_priority (> 0.70)
→ Claim extracted, routes to human_review (contradiction with validated S1 assertion)
```

**MarketIntel** (serves "Competitive Positioning" decision):
```
decision_relevance:
  anchors(CompetitivePositioning) = {:Competitor_*, :MarketSegment_OTC}
  :FDA is 2 hops from :MarketSegment_OTC (via :regulates → :OTC_ProductLine → :in_segment)
  min_distance = 2 → relevance = 1/(1+2) = 0.33

novelty:
  No contradiction with MarketIntel's view
  extension: new guidance entity → 0.7
  novelty = 0.7

commitment: 0.0 (no open tasks reference FDA directly)

authority: 0.8 (same as above)

recurrence: 0.0

weighted_total:
  (0.7×0.2) + (0.33×0.4) + (0×0.15) + (0.8×0.15) + (0×0.1)
  = 0.14 + 0.132 + 0 + 0.12 + 0
  = 0.392

disposition: below_threshold (< 0.45)
→ No claim from MarketIntel for this event
→ But: WatchdogProfile catches it (global relevance to registered decisions)
```

**SupportOps** (serves "Customer Satisfaction" decision):
```
decision_relevance:
  anchors(CustomerSatisfaction) = {:Customer_*, :SupportTicket_*, :Product_*}
  :FDA is 3 hops from nearest anchor
  min_distance = 3 → relevance = 1/(1+3) = 0.25

novelty: 0.7 (same extension score)
commitment: 0.0
authority: 0.8
recurrence: 0.0

weighted_total:
  (0.7×0.2) + (0.25×0.4) + (0×0.15) + (0.8×0.15) + (0×0.1)
  = 0.14 + 0.10 + 0 + 0.12 + 0
  = 0.36

disposition: below_threshold
→ No claim, but T4 generalization "labeling changes precede return shifts" noted
```

**SupplyChain**:
```
E.participants ∩ SupplyChain.entityNeighborhoods = ∅
→ No SalienceAssessment created (event outside subscription)
```

### Six Weeks Later

SupportOps task: "Analyze increase in returns for OTC product line"

```
ContextAssemblyAct:
  1. Entity resolution: "OTC product line" → :OTC_ProductLine
  
  2. Anchor traversal from :OTC_ProductLine:
     S1: product specs, channels
     S2: walks to :FDA via :regulated_by
         → Finds CanonicalAssertion about new labeling (promoted via RegAffairs path)
     S3: current return-rate observations
     
  3. T4 generalizations matching :OTC_ProductLine:
     "Labeling changes precede return-reason shifts" included
     
  Bundle assembled with cross-domain context from RegAffairs' promoted claim.
```

---

## 10. Validation Loop

```
Phase 1: Ingestion & Extraction (NON-DETERMINISTIC boundary)
  □ RawEvent captured (T0, HIRI-signed)
  □ ExtractionAct executed, marked non_deterministic=true
  □ TypedEvent created with EntityReferences
  □ At least one ambiguous EntityReference flagged
  □ ExtractionFailure logged for one malformed event

Phase 2: Salience Assessment (DETERMINISTIC verification)
  □ SalienceAssessments created for ≥2 agents with different profiles
  □ Same TypedEvent scored differently by different profiles (decision dimension)
  □ Determinism verified: replay produces identical scores
  □ WatchdogProfile catches one event missed by all agent profiles

Phase 3: Claim Promotion
  □ Claims extracted from high-salience assessments
  □ Auto-promotion exercised (S3 authoritative fact)
  □ Agent-review exercised (S2 relational claim)
  □ Human-review exercised (S1 structural claim)
  □ One ContradictionSignal raised
  □ Conflict resolved via each of: supersession, rejection, scoping (or synthesis)
  □ TrustObservations created for each resolution
  □ Cold-start agent routed to human review by default

Phase 4: Generalization
  □ GeneralizationProposalAct creates CandidateGeneralization
  □ StatusAssertion(status=proposed) created
  □ GeneralizationReviewAct (human) validates
  □ StatusAssertion(status=validated) created

Phase 5: Decay & Tombstoning
  □ DecayAct demotes unreferenced TypedEvent
  □ StatusAssertion(status=decayed) created
  □ T0 RawEvent tombstoned after TTL
  □ Tombstone created with content_hash
  □ Provenance chain verification succeeds with tombstoned evidence

Phase 6: Access
  □ New agent provisioned from ContextProfile alone
  □ ContextBundle assembled within budget
  □ Budget overflow triggers TruncationRecord
  □ Own-view-divergent private claim annotated
  □ Per-request budget override recorded in audit log

Phase 7: Audit & Integrity
  □ ContextAssemblyAuditRecord created
  □ Attribution query: "could agent know F?" answers correctly
  □ All artifacts HIRI-addressable
  □ StatusAssertions correctly represent lifecycle
  □ No artifact mutation (all changes via StatusAssertion)
  □ SHACL validation: 0 violations
  □ Every MVP class instantiated

Acceptance Criteria:
  - ≥100 raw events across ≥3 entity neighborhoods
  - ≥10 claims through each review tier
  - ≥1 conflict resolved via scoping (exercises ScopeBoundary)
  - ≥1 generalization proposed, reviewed, validated
  - ≥1 T0 tombstoned with verification
  - Salience determinism verified on 100% of T1 events
  - SHACL validation: 0 violations
```

---

## 11. Competency Questions

```
Filtering
  CQ-F1: Why was this experience kept / discarded?
         → SalienceAssessment + profile used + model version
  CQ-F2: What evidence supports this assertion?
         → Provenance chain; tombstones show hash if evidence expired
  CQ-F3: What did the model forget?
         → StatusAssertions with status=decayed or tombstoned

Access
  CQ-A1: What context was act A performed under?
         → ContextAssemblyAuditRecord.bundle_hiri
  CQ-A2: What was excluded due to budget?
         → TruncationRecords in audit record
  CQ-A3: What does agent X believe differently from canonical?
         → PrivateStore.privateClaims where contradicts()

Governance
  CQ-G1: Who promoted this assertion?
         → ClaimReviewAct.reviewer, via provenance
  CQ-G2: What is agent X's trust score for stratum S?
         → Aggregate TrustObservations(subject=X, stratum=S)

Integrity
  CQ-I1: Has artifact A been tampered with?
         → Verify: hash(A.content) = A.hiri
  CQ-I2: What is A's current status?
         → Most recent StatusAssertion where subject=A.hiri
```

---

## 12. Risks and Controls

| Risk | Control |
|------|---------|
| Extraction errors propagate | ExtractionAct explicitly non-deterministic; confidence scores; human review for low-confidence |
| Salience model wrong | Versioned spec; discard logged; watchdog catches global misses |
| Trust gaming (selective submission) | Acknowledged limitation (§14); scoped by stratum |
| Provenance chains break | Tombstone protocol preserves hashes; T1/T2 locked while referenced |
| Status assertions conflict | Latest-by-timestamp wins; supersedes chain is auditable |
| Key compromise | MVP: platform-held keys; post-MVP: rotation/revocation protocol |

---

## 13. Open Questions

1. **Trust metric limitations:** promotionRate conflates calibration with selectivity. An agent that submits only safe claims earns high trust. Better metrics (Brier scores, coverage-adjusted rates) are future work.

2. **Salience weight learning:** Infrastructure supports learning from TrustObservations; method not specified.

3. **Cross-enterprise federation:** HIRI provides trust infrastructure; governance policies for S2 sharing undefined.

4. **Generalization decay detection:** GeneralizationValidationAct exists; triggering conditions and statistical tests unspecified.

5. **Entity resolution improvement:** Current exact-match + LLM fallback has recall limitations; fuzzy matching with confidence calibration is future work.

---

## 14. Relation to the FNSR Program

| FNSR Requirement | Implementation |
|------------------|----------------|
| Persistent perspective | ContextProfile + PrivateStore + SyncState |
| Defensible forgetting | StatusAssertions + Tombstones with hashes |
| Grounded trust | TrustObservations scoped by stratum |
| Accountable participation | HIRI provenance + ContextBundle audit |
| Honest determinism boundary | ExtractionAct marked non-deterministic; rest deterministic |
| Cryptographic integrity | Immutable cores + reified status (P5, P8) |

---

## Appendix A: BFO/CCO Alignment

| Class | BFO/CCO Parent |
|-------|----------------|
| CanonicalAssertion | ICE |
| TypedEvent | ICE (process description) |
| SalienceAssessment | ICE |
| StatusAssertion | ICE (assertion about artifact) |
| ExtractionAct | Planned Act |
| SalienceAssessmentAct | Planned Act |
| ... | (full table in build document) |

---

## Appendix B: Authoritative Configuration

```yaml
# SalienceModelSpecification v1.0.0
# THIS IS AUTHORITATIVE; inline examples are illustrative only

version: "1.0.0"
owner: hiri:sha256:...

weights:
  novelty: 0.20
  decision: 0.40
  commitment: 0.15
  authority: 0.15
  recurrence: 0.10

thresholds:
  promotion_threshold: 0.45
  high_priority: 0.70
  watchdog_threshold: 0.60

---
# AuthoritySpecification v1.0.0

sources:
  regulatory_filing: 1.0
  first_party_system: 0.9
  audited_financial: 0.9
  official_announcement: 0.85
  trade_publication: 0.6
  industry_analyst: 0.5
  news_media: 0.4
  social_media: 0.2
  agent_inference: 0.3
  unknown: 0.1

methods:
  direct_observation: 1.0
  system_query: 0.95
  document_extraction: 0.8
  rule_based_extraction: 0.85
  llm_extraction: 0.8
  inference: 0.5
  hearsay: 0.3
```

---

## Appendix C: Generalization Templates

```yaml
# GeneralizationTemplateLibrary v1.0.0

templates:
  - id: temporal_correlation
    pattern: "[EntityType] exhibits [Metric] [Direction] in [TimePeriod]"
    min_evidence: 5
    
  - id: causal_sequence
    pattern: "[Event1] at [Entity1] precedes [Event2] at [Entity2] within [Duration]"
    min_evidence: 3
    
  - id: regulatory_impact
    pattern: "[RegEvent] affecting [ProductType] leads to [Metric] [Direction]"
    min_evidence: 2
```

---

*End of Document*
