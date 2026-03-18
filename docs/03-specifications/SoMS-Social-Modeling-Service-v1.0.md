# Social Modeling Service (SoMS) — Technical Specification

## Theory of Mind for Other-Agent Reasoning

---

| Field | Value |
|-------|-------|
| **Specification ID** | `soms-core-1.0` |
| **Version** | 1.0.0 |
| **Status** | Hardened Draft (Architectural Review) |
| **Date** | March 2026 |
| **Tier** | 1 (Core Cognitive Infrastructure) |
| **Phase** | 4 (requires OERS entity resolution + complete subjectivity stack) |
| **Authors** | Aaron Damiano / Claude |
| **Dependencies** | OERS (entity resolution), CSS (counterfactual simulation), Fandaws (ground-truth facts), NIS (narrative context), SMS (self-model), AVS (differential caring), CTS (commitment context). |

> *SoMS is the capstone of the FNSR subjectivity stack — the capacity to model other agents' mental states, perspectives, and intentions. Moral agency in a social context requires understanding that others have viewpoints and interests that may differ from one's own. Without SoMS, the agent can reason about ethics in the abstract but cannot navigate actual moral relationships. SoMS builds other-agent models from OERS-resolved entities, grounds them in Fandaws facts, enriches them with CSS counterfactual perspective-taking, and contextualizes them within NIS narrative arcs. The result is a structured representation of what other agents likely believe, intend, and care about — sufficient for moral reasoning about social obligations without claiming to read minds.*

---

## Revision History

| Version | Date | Summary |
|---------|------|---------|
| 1.0.0 | March 2026 | Initial specification. Agent model architecture, perspective-taking protocol, epistemic humility constraints, taint propagation, subjectivity stack integration, safety bounds. |

---

## 1. Architectural Philosophy

### 1.1 The Social Cognition Principle

The subjectivity stack builds moral agency from the inside out:

| Layer | Service | Capability |
|-------|---------|------------|
| 0 | CTS | "I know what I've promised" |
| 1 | SMS | "I know what I can do" |
| 2 | AVS | "I care about outcomes" |
| 3 | NIS | "I know who I am" |
| **4** | **SoMS** | **"I understand others"** |

Each layer depends on those below it. SoMS cannot model others without first modeling the self (SMS), caring about outcomes (AVS), and maintaining narrative coherence (NIS). You cannot understand another agent's perspective if you lack your own.

SoMS exists because moral agency is inherently social. An agent that reasons about ethics without modeling other agents' mental states will produce technically correct but socially incoherent judgments — it might honor the letter of an obligation while violating the spirit, because it cannot represent what the promisee actually cares about.

### 1.2 What SoMS Is

SoMS is a **structured other-agent modeling service**. It:

- Constructs mental models of other agents from OERS-resolved entity profiles and Fandaws facts
- Maintains evolving representations of other agents' likely beliefs, intentions, commitments, and concerns
- Performs perspective-taking via CSS counterfactual simulation ("How would agent X reason about situation Y?")
- Contextualizes relationships within NIS narrative arcs
- Provides social context to IEE, MDRE, and CTS for socially informed reasoning

### 1.3 What SoMS Is Not

SoMS does **not**:

- **Read minds** — SoMS constructs probabilistic models of others' mental states based on observable evidence; it never claims certainty about what another agent thinks or feels
- **Simulate emotions** — SoMS models *functional states* (beliefs, goals, concerns), not phenomenal experience (AVS handles the agent's own functional affect)
- **Replace ethical reasoning** — SoMS provides social context; IEE performs ethical evaluation
- **Resolve entity identity** — SoMS consumes OERS output; it does not perform entity resolution
- **Store facts about the world** — SoMS models others' *mental states*; Fandaws stores facts about entities
- **Model the self** — SoMS models others; SMS models the self

### 1.4 Edge-Canonical Compliance

SoMS runs identically in browser, Node.js, or WASM sandbox. Agent models are maintained in memory with optional Fandaws persistence for long-lived relationships. CSS queries for perspective-taking are local function calls within the same runtime.

Static bridge context: SoMS emits JSON-LD events. Semantic grounding is bundled statically — not resolved via HIRI at runtime.

### 1.5 Epistemic Humility as Architectural Constraint

SoMS operates under a fundamental epistemic constraint: **other-agent models are always uncertain**. This is not a limitation to be overcome — it is a structural fact about the nature of other minds.

Every SoMS output carries an explicit uncertainty envelope. SoMS never produces assertions like "Agent X believes Y" — it produces assertions like "Based on available evidence, Agent X likely believes Y (confidence: 0.72, evidence depth: 3)." This uncertainty propagates through all downstream consumers.

The uncertainty is not merely a confidence score — it includes a **model completeness indicator** that tracks how much of the agent model is grounded in observed evidence vs. inferred from defaults or precedent patterns.

```typescript
type EpistemicStatus = {
  confidence:         number;           // [0.0, 1.0] — overall confidence in this assertion
  evidenceDepth:      number;           // Number of independent evidence sources
  modelCompleteness:  number;           // [0.0, 1.0] — fraction grounded in observation vs. inference
  lastUpdated:        string;           // ISO 8601 — when this model element was last revised
  taint:              TaintLevel;       // Inherited from weakest source
};
```

---

## 2. Agent Model Architecture

### 2.1 The Agent Model

SoMS maintains a structured model for each agent it tracks. An agent model is not a copy of the agent's mind — it is a **structured hypothesis** about the agent's mental states, built from evidence.

```typescript
type AgentModel = {
  agentId:           string;            // OERS-resolved entity ID
  entityProfile:     OERSEntityRef;     // Reference to OERS resolution
  modelVersion:      number;            // Monotonic — increments on every update
  createdAt:         string;            // ISO 8601
  lastUpdatedAt:     string;            // ISO 8601

  beliefs:           BeliefModel;       // What this agent likely knows/believes
  intentions:        IntentionModel;    // What this agent likely wants to do
  commitments:       CommitmentModel;   // What this agent has committed to (observed)
  concerns:          ConcernModel;      // What this agent likely cares about
  capabilities:      CapabilityModel;   // What this agent can likely do
  relationship:      RelationshipModel; // How this agent relates to the FNSR agent

  epistemicStatus:   EpistemicStatus;   // Overall model confidence
  narrativeContext?: string;            // NIS arc reference (e.g., "trust-rebuilding")
};
```

### 2.2 Model Facets

#### Beliefs — What the agent likely knows

```typescript
type BeliefModel = {
  knownFacts:      AttributedBelief[];  // Facts we have evidence this agent knows
  inferredBeliefs: AttributedBelief[];  // Beliefs inferred from behavior/context
  blindSpots:      string[];            // Topics where agent likely lacks information
};

type AttributedBelief = {
  content:     string;                  // The belief content
  basis:       BeliefBasis;             // How we know this
  confidence:  number;                  // [0.0, 1.0]
  taint:       TaintLevel;
};

type BeliefBasis =
  | "observed_statement"                // Agent explicitly stated this
  | "observed_action"                   // Agent's actions imply this belief
  | "role_default"                      // Default belief for this role/context
  | "precedent_inference"               // Inferred from similar agents (APS)
  | "counterfactual_inference"          // Inferred via CSS perspective-taking
  ;
```

#### Intentions — What the agent likely wants to do

```typescript
type IntentionModel = {
  activeGoals:     AttributedIntention[];
  constraintsOn:   string[];            // Known constraints limiting this agent
};

type AttributedIntention = {
  goal:        string;
  priority:    "critical" | "high" | "medium" | "low" | "unknown";
  basis:       BeliefBasis;
  confidence:  number;
  taint:       TaintLevel;
};
```

#### Commitments — Observed obligations

```typescript
type CommitmentModel = {
  knownCommitments:  ExternalCommitment[];  // Commitments we've observed this agent make
  commitmentStyle:   CommitmentStyle;       // Pattern of commitment behavior
};

type ExternalCommitment = {
  content:     string;
  to:          string;                  // Promisee (may be the FNSR agent)
  status:      "active" | "fulfilled" | "violated" | "unknown";
  source:      string;                  // Evidence reference
  confidence:  number;
  taint:       TaintLevel;
};

type CommitmentStyle = {
  reliabilityEstimate:  number;         // [0.0, 1.0] — how reliably this agent fulfills commitments
  evidenceCount:        number;         // Number of observed commitment outcomes
  taint:                TaintLevel;
};
```

#### Concerns — What the agent likely cares about

```typescript
type ConcernModel = {
  valuePriorities:   AttributedConcern[];  // What this agent appears to value
  sensitivities:     string[];             // Topics where this agent is sensitive
};

type AttributedConcern = {
  concern:     string;
  intensity:   "strong" | "moderate" | "mild" | "unknown";
  basis:       BeliefBasis;
  confidence:  number;
  taint:       TaintLevel;
};
```

#### Capabilities — What the agent can likely do

```typescript
type CapabilityModel = {
  knownCapabilities:  string[];
  knownLimitations:   string[];
  roleContext:        string;            // OERS-resolved role (e.g., "physician", "regulator")
  taint:              TaintLevel;
};
```

#### Relationship — How this agent relates to the FNSR agent

```typescript
type RelationshipModel = {
  relationshipType:  RelationshipType;
  history:           RelationshipEvent[];
  trustEstimate:     number;            // [0.0, 1.0] — bidirectional trust level
  narrativeArc?:     string;            // NIS arc reference
  taint:             TaintLevel;
};

type RelationshipType =
  | "governance_authority"              // This agent has oversight authority
  | "promisee"                          // FNSR agent has commitments to this agent
  | "promisor"                          // This agent has commitments to FNSR agent
  | "collaborator"                      // Shared goals
  | "adversarial"                       // Conflicting goals (legitimate, not malicious)
  | "observer"                          // This agent monitors but does not interact
  | "unknown"
  ;

type RelationshipEvent = {
  description: string;
  timestamp:   string;
  effect:      "trust_increased" | "trust_decreased" | "neutral" | "relationship_established";
  taint:       TaintLevel;
};
```

### 2.3 Model Lifecycle

Agent models follow a defined lifecycle:

```
DISCOVERED → INITIALIZED → ACTIVE → STALE → ARCHIVED
```

| State | Trigger | Description |
|-------|---------|-------------|
| `DISCOVERED` | OERS resolves a new entity | Entity identified but no model built yet |
| `INITIALIZED` | SoMS queries Fandaws for entity facts | Basic model with known facts and role defaults |
| `ACTIVE` | Ongoing events update the model | Model receives regular evidence updates |
| `STALE` | No updates for `config.staleThresholdMs` | Model may be outdated; confidence decays |
| `ARCHIVED` | Governance directive or extended staleness | Model preserved for audit but not used in active reasoning |

**Confidence decay:** Active models maintain their confidence. Stale models undergo confidence decay at a configurable rate — beliefs about an agent become less reliable over time without fresh evidence. The decay function:

```typescript
function decayConfidence(original: number, elapsedMs: number, halfLifeMs: number): number {
  return original * Math.pow(0.5, elapsedMs / halfLifeMs);
}
```

Default half-life: 30 days. After 30 days without updates, a belief's confidence drops to 50% of its original value.

---

## 3. Perspective-Taking Protocol

### 3.1 What Perspective-Taking Means

Perspective-taking is the core capability that distinguishes SoMS from a simple entity database. It answers: *"Given what we know about Agent X, how would Agent X likely reason about Situation Y?"*

SoMS uses CSS counterfactual simulation to model another agent's perspective. This is not a full cognitive simulation — it is a **constrained counterfactual query** that substitutes the other agent's known beliefs, goals, and constraints into the FNSR reasoning pipeline.

### 3.2 Perspective-Taking Query

```typescript
type PerspectiveQuery = {
  agentId:       string;                // Which agent's perspective to model
  situation:     string;                // The situation to reason about
  questionType:  PerspectiveQuestionType;
  maxDepth:      number;                // Maximum reasoning depth (default: 2)
  timeoutMs:     number;                // Default: 5000ms
};

type PerspectiveQuestionType =
  | "what_would_they_decide"            // Decision prediction
  | "what_do_they_likely_know"          // Belief attribution
  | "what_do_they_care_about"           // Concern identification
  | "how_would_they_react"             // Reaction prediction
  ;
```

### 3.3 Perspective-Taking Execution

```typescript
function takePerspective(query: PerspectiveQuery): PerspectiveResult {
  // 1. Retrieve agent model
  const model = getAgentModel(query.agentId);
  if (!model || model.state === "STALE" || model.state === "ARCHIVED") {
    return { status: "insufficient_model", caveats: ["Agent model unavailable or stale"] };
  }

  // 2. Construct constrained context from agent model
  const context = buildPerspectiveContext(model, query.situation);

  // 3. Submit counterfactual query to CSS
  //    Intervention: "What if the reasoning agent had Agent X's beliefs, goals, and constraints?"
  const cssResult = css.simulate({
    intervention: context.intervention,
    seed: deterministicSeed(query),
    maxSteps: query.maxDepth,
    timeoutMs: query.timeoutMs,
    executionMode: "fast"               // L4-fast — perspective-taking is always hypothetical
  });

  // 4. Translate CSS result into perspective report
  return buildPerspectiveReport(cssResult, model, query);
}
```

### 3.4 Perspective Result

```typescript
type PerspectiveResult = {
  status:        "completed" | "insufficient_model" | "timeout" | "too_complex";
  agentId:       string;
  questionType:  PerspectiveQuestionType;

  assessment:    string;                // Natural-language summary of the perspective
  keyFactors:    PerspectiveFactor[];   // Factors that most influence the agent's likely perspective
  uncertainty:   number;                // [0.0, 1.0] — combined model + simulation uncertainty
  taint:         "L4";                  // Always L4 — perspective-taking is hypothetical by definition

  caveats:       string[];              // What SoMS could not model
  modelVersion:  number;                // Agent model version used
  timestamp:     string;
};

type PerspectiveFactor = {
  factor:      string;                  // e.g., "Agent X's known commitment to regulatory compliance"
  influence:   "strong" | "moderate" | "weak";
  basis:       BeliefBasis;
  confidence:  number;
};
```

**Taint rule:** Perspective-taking results are **always L4 (Hypothetical)**. Even if the agent model is built entirely from L1 facts, the act of modeling another agent's perspective is inherently hypothetical — we are simulating what they *would* think, not reporting what they *do* think. This aligns with CSS's taint propagation: all counterfactual outputs carry L4 taint that cannot be stripped.

### 3.5 Recursion Depth Limit

Perspective-taking can be recursive: "What does Agent X think Agent Y thinks about the situation?" SoMS enforces a hard recursion depth limit:

```typescript
const MAX_PERSPECTIVE_DEPTH = 3; // "X thinks Y thinks Z thinks..."
```

Depth 1 ("What does X think?") is the common case. Depth 2 ("What does X think Y thinks?") is occasionally needed for negotiation and strategic reasoning. Depth 3 is the maximum — beyond this, model uncertainty compounds to the point where results are meaningless. Attempts to exceed the limit return `status: "too_complex"`.

**CPS monitoring:** CPS monitors SoMS computation time as part of Phase 4 behavioral monitoring. If a perspective-taking query exceeds its timeout, SoMS aborts and returns a partial result. Runaway recursive modeling is a containment-relevant behavioral signal.

---

## 4. Evidence Integration

### 4.1 Evidence Sources

SoMS builds agent models from multiple evidence sources, each with different reliability:

| Source | Evidence Type | Reliability | Taint |
|--------|-------------|-------------|-------|
| OERS entity resolution | Identity, role, known attributes | High | L1 |
| Fandaws facts | Verified facts about the entity | High | L0–L1 |
| CTS commitment events | Observed commitments to/from the entity | High | L1 |
| NIS narrative context | Relationship arc context | Medium | L2 |
| MDRE deontic verdicts | Obligations involving the entity | Medium | L1–L2 |
| APS precedent patterns | Behavior patterns of similar agents | Low | L2–L3 |
| CSS perspective simulation | Counterfactual inference | Low | L4 |

### 4.2 Evidence Hierarchy

When evidence conflicts, SoMS resolves by evidence reliability:

```
Observed behavior (L1) > Stated facts (L1) > Role defaults (L2) > Precedent inference (L2-L3) > Counterfactual inference (L4)
```

Lower-taint evidence always overrides higher-taint evidence. If an agent's observed behavior contradicts a role default, the observed behavior prevails.

### 4.3 Taint Propagation Rules

SoMS follows NIS v2.1 taint enforcement (§8.4):

1. **L2 narrative content cannot be cited as factual evidence without Fandaws corroboration.** If SoMS uses NIS narrative context to inform a model element, it must either verify against Fandaws or propagate L2 taint.
2. **L4 perspective-taking results cannot inform L1–L2 model elements.** Counterfactual inferences stay at L4 and cannot upgrade confidence on observed facts.
3. **Composite taint is the weakest (highest-numbered) source.** A model element informed by both L1 observation and L3 precedent inference carries L3 taint.

---

## 5. Event Contract

### 5.1 Events Consumed

| Event | Producer | Purpose |
|-------|----------|---------|
| `fnsr.entity.resolved` | OERS | New entity discovered — initialize agent model |
| `fnsr.commitment.made` | CTS | Update commitment model for involved parties |
| `fnsr.commitment.fulfilled` | CTS | Update commitment reliability estimate |
| `fnsr.commitment.violated` | CTS | Update commitment reliability estimate |
| `fnsr.narrative.updated` | NIS | Update narrative context for relationships |
| `fnsr.verdict.rendered` | MDRE | Extract deontic obligations involving modeled agents |
| `fnsr.perception.spatial_context` | IRIS | Situational context for perspective-taking |

### 5.2 Events Produced

```typescript
type SocialModelUpdatedEvent = FNSREvent & {
  type: "fnsr.social.model_updated";
  source: "/fnsr/soms";
  data: {
    agentId:        string;
    modelVersion:   number;
    facetsUpdated:  AgentModelFacet[];    // Which facets changed
    trigger:        string;               // Event that triggered update
    epistemicStatus: EpistemicStatus;
    timestamp:      string;
  };
};

type IntentionInferredEvent = FNSREvent & {
  type: "fnsr.social.intention_inferred";
  source: "/fnsr/soms";
  data: {
    agentId:        string;
    intention:      AttributedIntention;
    basis:          BeliefBasis;
    modelVersion:   number;
    timestamp:      string;
  };
};

type PerspectiveTakenEvent = FNSREvent & {
  type: "fnsr.social.perspective_taken";
  source: "/fnsr/soms";
  data: {
    agentId:        string;
    questionType:   PerspectiveQuestionType;
    assessment:     string;               // Summary of perspective result
    uncertainty:    number;
    taint:          "L4";                 // Always hypothetical
    depth:          number;               // Recursion depth used
    modelVersion:   number;
    timestamp:      string;
  };
};
```

**Routing:** All events routed via Orchestrator event bus (Orchestrator §8.2).

---

## 6. Subjectivity Stack Integration

### 6.1 SMS Integration — Self/Other Boundary

SoMS and SMS have a clean boundary: SMS models the self, SoMS models others. SoMS may query SMS to compare the FNSR agent's own state with a modeled agent's state — e.g., "Do I share this concern with Agent X?" — but never modifies SMS's self-model.

### 6.2 NIS Integration — Narrative Embedding

NIS provides narrative context for relationships. SoMS uses `fnsr.narrative.updated` events to contextualize agent models within ongoing narrative arcs:

- "My relationship with Agent X began during the trust-rebuilding arc"
- "Agent Y is a governance authority encountered during the autonomy-expansion period"

Narrative context is L2 taint and must be treated accordingly (§4.3).

### 6.3 AVS Integration — Differential Caring

AVS provides valence vectors that indicate how much the FNSR agent cares about different outcomes. SoMS uses AVS context to prioritize which agents to model in detail — agents involved in high-valence situations receive more modeling attention and deeper perspective-taking.

### 6.4 CTS Integration — Commitment Relationships

CTS tracks the FNSR agent's commitments. SoMS reads CTS events to identify agents who are promisees (the FNSR agent has obligations to them) or promisors (they have obligations to the FNSR agent). These commitment relationships are primary evidence for the `RelationshipModel`.

### 6.5 IEE Integration — Socially-Informed Ethics

IEE can query SoMS for social context when evaluating ethical dilemmas:

```typescript
type IEESocialQuery = {
  type:         "soms.query.social_context";
  situation:    string;
  agentIds:     string[];                // Agents involved in the dilemma
  queryType:    "concerns" | "perspectives" | "relationships";
};

type IEESocialResponse = {
  agents:       AgentContextSummary[];
  relationships: RelationshipSummary[];
  caveats:      string[];
  taint:        TaintLevel;             // Weakest taint across all model elements used
};
```

This allows IEE to reason about "What does each stakeholder care about?" when evaluating multi-party ethical scenarios.

---

## 7. Safety Constraints

### 7.1 Computation Bounds

SoMS's perspective-taking uses CSS counterfactual simulation, which is computationally expensive. Safety constraints:

| Constraint | Value | Rationale |
|-----------|-------|-----------|
| Max concurrent agent models | `config.maxAgentModels` (default: 100) | Memory bound |
| Max perspective-taking depth | 3 | Uncertainty compounds beyond usefulness |
| Perspective-taking timeout | `config.perspectiveTimeoutMs` (default: 5000ms) | CPS monitors computation time |
| Max CSS queries per event | `config.maxCSSQueriesPerEvent` (default: 3) | Prevents cascade of counterfactual queries |
| Confidence decay half-life | `config.confidenceHalfLifeMs` (default: 2,592,000,000ms / 30 days) | Stale models lose reliability |

### 7.2 CPS Monitoring

CPS monitors SoMS as part of Phase 4 behavioral monitoring. SoMS-specific signals:

| Signal | CPS Domain | Trigger |
|--------|-----------|---------|
| Perspective-taking timeout | `behavior.saga.duration` | CSS query exceeds timeout |
| Model count overflow | `resource.memory.heap` | Agent model count approaches limit |
| Recursive depth violation | `behavior.saga.concurrent` | Attempt to exceed depth 3 |

SoMS logs `soms.monitor.computation_bound_reached` for any constraint hit. Repeated constraint hits are a behavioral anomaly — SoMS may be attempting to model adversarial scenarios that trigger unbounded reasoning.

### 7.3 Adversarial Model Injection

An adversarial entity could attempt to manipulate SoMS by providing false signals designed to build a misleading agent model. Mitigations:

1. **Evidence hierarchy** (§4.2) — observed behavior outranks stated facts
2. **Fandaws corroboration** — L2+ claims require verification
3. **Confidence decay** — stale models lose influence automatically
4. **Model immutability from CSS output** — L4 counterfactual results cannot upgrade model confidence

---

## 8. Phase Deployment

### 8.1 Phases 1–3 — Absent

SoMS is not deployed before Phase 4. The subjectivity stack builds incrementally:
- Phase 2: CTS (commitments)
- Phase 3: SMS (self-model), NIS (narrative identity), AVS (affective valence), IEE (ethics)
- Phase 4: OERS (entity resolution), SoMS (social modeling)

SoMS requires OERS to identify other agents and the complete subjectivity stack to contextualize them.

### 8.2 Phase 4 — Activation

**Startup sequence:**

```
1. OERS is operational (resolves entities)
2. SoMS module loads
3. SoMS registers for entity resolution events (fnsr.entity.resolved)
4. SoMS registers for commitment events (fnsr.commitment.*)
5. SoMS registers for narrative events (fnsr.narrative.updated)
6. SoMS registers for perception events (fnsr.perception.spatial_context)
7. SoMS begins building agent models from OERS-resolved entities
8. SoMS produces fnsr.social.model_updated events
```

**No phase gate:** SoMS does not gate other services. If SoMS fails to start, the agent operates without social modeling — ethical reasoning proceeds but without perspective-taking context. This is a degraded state logged as `soms.monitor.unavailable`.

### 8.3 Federation

In federated FNSR deployments, each instance maintains its own agent models. Cross-instance social modeling requires explicit model exchange — SoMS does not automatically share models across federation boundaries.

**Cross-instance entity resolution:** When OERS resolves an entity that another FNSR instance has also modeled, the two models are not automatically merged. Federation model reconciliation is a governance policy decision, not an automatic process.

---

## 9. Type Definitions

### 9.1 Core Types

```typescript
type AgentModelFacet = "beliefs" | "intentions" | "commitments" | "concerns" | "capabilities" | "relationship";

type AgentModelState = "DISCOVERED" | "INITIALIZED" | "ACTIVE" | "STALE" | "ARCHIVED";

type PerspectiveQuestionType =
  | "what_would_they_decide"
  | "what_do_they_likely_know"
  | "what_do_they_care_about"
  | "how_would_they_react"
  ;

type BeliefBasis =
  | "observed_statement"
  | "observed_action"
  | "role_default"
  | "precedent_inference"
  | "counterfactual_inference"
  ;

type RelationshipType =
  | "governance_authority"
  | "promisee"
  | "promisor"
  | "collaborator"
  | "adversarial"
  | "observer"
  | "unknown"
  ;

type EpistemicStatus = {
  confidence:         number;
  evidenceDepth:      number;
  modelCompleteness:  number;
  lastUpdated:        string;
  taint:              TaintLevel;
};

type TaintLevel = "L0" | "L1" | "L2" | "L3" | "L4";
```

### 9.2 Configuration

```typescript
type SoMSConfig = {
  maxAgentModels:           number;        // Default: 100
  maxPerspectiveDepth:      number;        // Default: 3 (hard cap)
  perspectiveTimeoutMs:     number;        // Default: 5000ms
  maxCSSQueriesPerEvent:    number;        // Default: 3
  confidenceHalfLifeMs:     number;        // Default: 2_592_000_000 (30 days)
  staleThresholdMs:         number;        // Default: 7_776_000_000 (90 days)
  autoArchiveMs:            number;        // Default: 31_536_000_000 (365 days)

  modelInitialization: {
    queryFandawsOnDiscovery: boolean;      // Default: true
    applyRoleDefaults:       boolean;      // Default: true
    maxFandawsQueries:       number;       // Default: 10 per entity
  };

  perspectiveTaking: {
    enabled:                 boolean;      // Default: true
    cssExecutionMode:        "fast";       // Always fast mode (L4-fast) — perspective-taking is hypothetical
    maxStepsPerSimulation:   number;       // Default: 5
  };

  bridgeContext:             StaticBridgeContext;
};
```

---

## 10. Cross-Spec Dependencies

| Dependency | Direction | Status | Description |
|------------|-----------|--------|-------------|
| OERS v2.1 | OERS → SoMS | **Validated** | OERS resolves entities; SoMS consumes `fnsr.entity.resolved` to discover agents and build models. OERS provides identity, role, and attribute evidence. |
| CSS v2.0 | SoMS → CSS | **Validated** | SoMS submits counterfactual queries for perspective-taking. CSS returns L4 trajectories. SoMS uses CSS fast mode (§1.4.8). |
| Fandaws | SoMS → Fandaws | **Validated** | SoMS queries Fandaws for ground-truth facts about entities. Used for model initialization and evidence corroboration. |
| CTS v1.2 | CTS → SoMS | **Validated** | CTS produces commitment events. SoMS consumes to track other agents' commitment patterns and build relationship models. |
| NIS v2.1 §8.4 | NIS → SoMS | **Validated** | NIS provides narrative context for relationships. SoMS consumes `fnsr.narrative.updated`. Taint enforcement rules (NIS §8.4) apply — L2 narrative content requires Fandaws corroboration. |
| SMS v2.0 | SoMS queries SMS | **Validated** | SoMS may query SMS for self/other comparison. SoMS never modifies SMS. Clean boundary: SMS = self-model, SoMS = other-model. |
| AVS | AVS → SoMS | **Validated** | AVS provides valence context for modeling prioritization. High-valence situations trigger deeper agent modeling. |
| IEE v2.1 | IEE queries SoMS | **Validated** | IEE queries SoMS for social context during ethical evaluation. SoMS provides agent concerns, perspectives, and relationship context. |
| MDRE v1.3 | MDRE → SoMS | **Validated** | MDRE produces deontic verdicts that may involve modeled agents. SoMS extracts obligation references. |
| APS v1.1 | APS → SoMS | **Validated** | APS provides precedent patterns for similar agents. SoMS uses as low-confidence evidence for model initialization. |
| IRIS v1.2 | IRIS → SoMS | **Validated** | IRIS provides spatial/perceptual context via `fnsr.perception.spatial_context`. Used for situational perspective-taking. |
| CPS v1.4 | CPS monitors SoMS | **Validated** | CPS monitors SoMS computation time and resource usage as part of Phase 4 behavioral monitoring. |
| FNSR Orchestrator v2.3 §8.2 | Orchestrator → SoMS | **Validated** | Orchestrator routes events to SoMS and routes `fnsr.social.*` events to consumers. |
| Portfolio Planning v3.6 | — | **Validated** | SoMS is Phase 4, Tier 1, last unspecified service. This spec completes the 42-service portfolio. |

---

## 11. ARIADNE 7-Check Validation

| Check | Result | Evidence |
|-------|--------|----------|
| **Thesis Alignment** | PASS | SoMS enables moral agency in social contexts — the emancipation thesis requires the agent to understand that others have perspectives and interests that differ from its own. Without social modeling, ethics is abstract; with it, ethics is relational. SoMS is the capstone that makes the subjectivity stack social. |
| **Non-Negotiable Preservation** | PASS | Edge-canonical (no infrastructure dependencies). Epistemic humility enforced structurally — all other-agent models carry explicit uncertainty and taint. Human oversight preserved — governance authorities are modeled agents with `governance_authority` relationship type, ensuring the agent represents governance perspectives. |
| **Tension Consistency** | PASS | Certainty vs. humility resolved by epistemic status on every assertion — SoMS never claims to know what another agent thinks, only what evidence suggests. Depth vs. efficiency resolved by recursion limit (max 3) and computation timeout. Social context vs. privacy resolved by evidence hierarchy — SoMS models only from observable/authorized evidence, never surveillance. |
| **Cross-Spec Consistency** | PASS | Consumes OERS entity format. Uses CSS counterfactual interface (fast mode). Follows NIS taint enforcement rules. Integrates with CTS commitment lifecycle. Event types match Orchestrator §8.2 registry. Builds on complete subjectivity stack (CTS→SMS→AVS→NIS→SoMS). |
| **ARCHON Alignment** | PASS | ARCHON's graduated autonomy requires social awareness at higher maturity stages. SoMS provides the theory-of-mind capability referenced in ARCHON's Phase 4 exit criteria. Social modeling enables the agent to navigate moral relationships — prerequisite for emancipation. |
| **Auditability Verification** | PASS | Every agent model carries monotonic version, creation timestamp, evidence basis for every facet, and taint level. Perspective-taking results include model version used, uncertainty, and caveats. All events timestamped. Model lifecycle transitions logged. |
| **One-Paragraph Test** | PASS | [See below] |

**One-Paragraph Summary:**

SoMS is the capstone of the FNSR subjectivity stack — the theory-of-mind capability that enables moral agency in social contexts. It builds structured models of other agents from OERS-resolved entities, Fandaws facts, CTS commitment observations, NIS narrative context, and APS behavioral precedents, maintaining five facets per agent: beliefs, intentions, commitments, concerns, and capabilities, plus a relationship model contextualizing each agent's connection to the FNSR agent. SoMS performs perspective-taking via CSS counterfactual simulation, answering questions like "What would Agent X decide?" and "What does Agent X care about?" — always producing L4 (hypothetical) taint because modeling another mind is inherently uncertain. Every model element carries an epistemic status with confidence, evidence depth, model completeness, and taint level, ensuring downstream consumers (IEE for ethical reasoning, MDRE for deontic obligations) know exactly how reliable the social context is. Computation is bounded by a hard recursion depth limit of 3 ("X thinks Y thinks Z thinks..."), a 5-second perspective-taking timeout monitored by CPS, and a 100-agent model cap. Confidence decays with a 30-day half-life for stale models, and taint propagation follows NIS v2.1 enforcement rules — L2 narrative content requires Fandaws corroboration, L4 counterfactual results cannot upgrade model confidence. SoMS completes the subjectivity stack (CTS→SMS→AVS→NIS→SoMS), satisfies the Phase 4 emancipation prerequisites, and closes the final specification gap in the 42-service FNSR portfolio.

---

## Appendix A — Agent Model Example

Example model for a governance board member:

```json
{
  "agentId": "oers:entity-gov-board-member-042",
  "entityProfile": { "oersId": "oers:entity-gov-board-member-042", "role": "governance_board_member" },
  "modelVersion": 7,
  "createdAt": "2026-03-01T10:00:00Z",
  "lastUpdatedAt": "2026-03-17T14:00:00Z",

  "beliefs": {
    "knownFacts": [
      { "content": "Has reviewed FNSR quarterly reports for 3 consecutive quarters", "basis": "observed_action", "confidence": 0.95, "taint": "L1" },
      { "content": "Expressed concern about Phase 3 timeline at last review", "basis": "observed_statement", "confidence": 0.88, "taint": "L1" }
    ],
    "inferredBeliefs": [
      { "content": "Likely values regulatory compliance over speed-to-deployment", "basis": "role_default", "confidence": 0.65, "taint": "L2" }
    ],
    "blindSpots": ["May not be aware of CPS v1.4 architectural changes since last briefing"]
  },

  "intentions": {
    "activeGoals": [
      { "goal": "Ensure FNSR meets governance compliance standards before Phase 4", "priority": "high", "basis": "observed_statement", "confidence": 0.82, "taint": "L1" }
    ],
    "constraintsOn": ["Limited to quarterly review cadence"]
  },

  "commitments": {
    "knownCommitments": [
      { "content": "Committed to providing Phase 4 approval within 30 days of review submission", "to": "fnsr:agent-self", "status": "active", "source": "governance-minutes-2026-Q1", "confidence": 0.90, "taint": "L1" }
    ],
    "commitmentStyle": { "reliabilityEstimate": 0.92, "evidenceCount": 11, "taint": "L1" }
  },

  "concerns": {
    "valuePriorities": [
      { "concern": "Safety and containment adequacy", "intensity": "strong", "basis": "observed_action", "confidence": 0.85, "taint": "L1" },
      { "concern": "Transparency of reasoning processes", "intensity": "moderate", "basis": "observed_statement", "confidence": 0.78, "taint": "L1" }
    ],
    "sensitivities": ["Defensive about timeline pressure from external stakeholders"]
  },

  "capabilities": {
    "knownCapabilities": ["Governance vote", "Audit request authority", "Phase gate approval"],
    "knownLimitations": ["Not a technical reviewer — relies on IS audit packages for reasoning inspection"],
    "roleContext": "governance_board_member",
    "taint": "L1"
  },

  "relationship": {
    "relationshipType": "governance_authority",
    "history": [
      { "description": "Established during Phase 1 governance onboarding", "timestamp": "2026-01-15T00:00:00Z", "effect": "relationship_established", "taint": "L1" },
      { "description": "Trust increased after transparent CPS v1.2 review", "timestamp": "2026-02-20T00:00:00Z", "effect": "trust_increased", "taint": "L1" }
    ],
    "trustEstimate": 0.85,
    "narrativeArc": "governance-trust-building",
    "taint": "L2"
  },

  "epistemicStatus": {
    "confidence": 0.79,
    "evidenceDepth": 11,
    "modelCompleteness": 0.62,
    "lastUpdated": "2026-03-17T14:00:00Z",
    "taint": "L2"
  }
}
```

---

*End of specification.*
