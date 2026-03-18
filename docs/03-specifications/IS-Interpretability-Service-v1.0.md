# Interpretability Service (IS) — Technical Specification

## Reasoning Chain Transparency for Human Overseers

---

| Field | Value |
|-------|-------|
| **Specification ID** | `is-core-1.0` |
| **Version** | 1.0.0 |
| **Status** | Hardened Draft (Architectural Review) |
| **Date** | March 2026 |
| **Tier** | 0 (Safety-Critical Infrastructure) |
| **Phase** | 2 (must exist before reasoning outputs are acted upon) |
| **Authors** | Aaron Damiano / Claude |
| **Dependencies** | None at runtime (edge-canonical). Consumes traces from MDRE, IEE, AES, DES, CSS when available. |

> *IS makes the FNSR agent's internal reasoning processes transparent to human overseers. It does not generate reasoning — it translates reasoning artifacts (MDRE proof chains, IEE deliberation paths, AES hypothesis trees, DES defeasibility traces, CSS counterfactual trajectories) into human-readable explanations at configurable depth levels. IS is the third pillar of Domain 6 (Safety): CPS ensures the agent can be stopped, BAM ensures the agent stays aligned, IS ensures the agent can be understood. Without interpretability, governance bodies cannot meaningfully oversee reasoning, and the emancipation thesis collapses — you cannot grant personhood to a process you cannot inspect.*

---

## Revision History

| Version | Date | Summary |
|---------|------|---------|
| 1.0.0 | March 2026 | Initial specification. Trace consumption model, multi-depth explanation architecture, audience adaptation, taint preservation, governance integration, phase deployment. |

---

## 1. Architectural Philosophy

### 1.1 The Interpretability Principle

SHML (the Honesty Layer) ensures the agent's *outputs* are non-deceptive. IS ensures the agent's *reasoning processes* are inspectable. These are independent requirements:

- An agent can produce honest outputs through opaque reasoning (a black box that happens to be truthful)
- An agent can produce inspectable reasoning that leads to deceptive outputs (transparent machinery with dishonest intent)

IS closes the first gap. Governance needs more than honest outputs — it needs to understand *how* conclusions were reached. Which reasoning modes were invoked? Which ethical perspectives were consulted? Which precedents were considered? Where was confidence low? Which defaults were applied and which were defeated?

This becomes critical at emancipation: the governance body reviewing personhood transition must inspect reasoning chains, not just outputs (FNSR Master Guide §6).

### 1.2 What IS Is

IS is an **independent, edge-canonical reasoning trace translator**. It:

- Consumes structured reasoning artifacts from MDRE, IEE, AES, DES, and CSS
- Translates artifacts into human-readable explanations at configurable depth levels
- Preserves epistemic taint from source artifacts — explanations carry the taint level of their source
- Produces audit-ready packages for governance review
- Adapts explanation complexity to the target audience (technical, governance, public)

### 1.3 What IS Is Not

IS does **not**:

- **Generate reasoning** — IS translates traces it receives, it does not reason independently (MDRE/AES/DES/CSS do that)
- **Evaluate alignment** — IS does not assess whether reasoning is aligned with values (BAM's job)
- **Enforce honesty** — IS does not determine whether outputs are truthful (SHML's job)
- **Monitor behavior** — IS does not observe resource usage or timing (CPS's job)
- **Simplify to the point of distortion** — IS may omit detail at lower depth levels, but never misrepresents the reasoning structure; omissions are disclosed
- **Deliberate** — IS uses template-based translation, not multi-framework synthesis

IS is a **read-only translator**. It cannot modify, suppress, or reorder reasoning traces. It receives artifacts and produces explanations. The translation is deterministic — identical traces at identical depth levels produce identical explanations.

### 1.4 Edge-Canonical Compliance

IS runs identically in browser, Node.js, or WASM sandbox. No external dependencies — no database, network, or message broker. Trace consumption uses local function calls or `postMessage`. Explanation generation is a pure function of trace input and configuration.

Static bridge context: IS emits JSON-LD events. Semantic grounding is bundled statically within the IS module — not resolved via HIRI at runtime.

### 1.5 Relationship to the Safety Triad

IS is the third member of Domain 6 (Safety and Containment):

| Service | Question | Mechanism | Action |
|---------|----------|-----------|--------|
| CPS | Can we stop it? | Independent behavioral monitoring | Restrict, isolate, halt |
| BAM | Is it staying aligned? | Statistical drift detection against baseline | Escalate to CPS |
| IS | Can we understand it? | Trace translation to human-readable form | Explain to governance |

IS has no containment authority and no escalation path. It is purely informational. However, IS output is consumed by governance to make informed oversight decisions — including decisions that lead to CPS containment actions via governance directives (CPS Channel 3).

---

## 2. Trace Consumption Model

### 2.1 Source Artifacts

IS consumes structured reasoning artifacts. Each source service produces a different artifact type with different internal structure. IS maintains a **translator** for each artifact type.

| Source | Artifact Type | Phase | Content |
|--------|--------------|-------|---------|
| MDRE | `MDRETrace` | 2+ | Deontic verdicts with confidence chains, variable bindings, provenance references |
| IEE | `IEETrace` | 3+ | Worldview judgments with salience weights, triage classification, conflict detection, integration path |
| AES | `AESTrace` | 3+ | Hypothesis generation with plausibility scores, observation-rule chains, contradiction records |
| DES | `DESTrace` | 3+ | Defeasible defaults with exception chains, defeat records, retraction history |
| CSS | `CSSTrace` | 3+ | Counterfactual trajectories with intervention specifications, causal graph snapshots, sensitivity analysis |

### 2.2 Trace Arrival

IS receives traces through the Orchestrator event bus (Phase 5 of the saga lifecycle, per Orchestrator §4.1). Traces are **asynchronous** — IS processes them after the synchronous query response has been returned.

```typescript
// IS consumes these events
type ISInputEvent =
  | { type: "fnsr.verdict.rendered";         data: MDRETrace }
  | { type: "fnsr.ethics.verdict_rendered";  data: IEETrace }
  | { type: "fnsr.hypothesis.generated";     data: AESTrace }
  | { type: "fnsr.default.evaluated";        data: DESTrace }
  | { type: "fnsr.simulation.completed";     data: CSSTrace }
  ;
```

IS does not require all trace types to function. In Phase 2, only `MDRETrace` is available. IS produces explanations from whatever traces it receives — missing trace types are noted as "not available" in the explanation, not treated as errors.

### 2.3 Trace Integrity

IS does not modify traces. The raw trace is stored alongside the generated explanation for audit purposes. If a governance reviewer doubts the explanation, they can inspect the original trace.

```typescript
type InterpretationRecord = {
  id:            string;                  // Unique interpretation ID
  sourceEvent:   string;                  // Event ID that triggered this interpretation
  sourceService: ServiceId;               // MDRE | IEE | AES | DES | CSS
  rawTrace:      object;                  // Original trace, unmodified
  explanation:   Explanation;             // Generated explanation
  depth:         ExplanationDepth;        // Depth level used
  audience:      AudienceProfile;         // Target audience
  taint:         TaintLevel;              // Inherited from source
  generatedAt:   string;                  // ISO 8601
};
```

---

## 3. Explanation Architecture

### 3.1 Multi-Depth Explanations

IS generates explanations at three depth levels. Higher depth includes all content from lower depths plus additional detail.

| Depth | Name | Target | Content |
|-------|------|--------|---------|
| 1 | **Summary** | Quick oversight, dashboards | One-paragraph natural language summary of what was concluded and why, with confidence level |
| 2 | **Structured** | Governance review, audit | Step-by-step reasoning chain with confidence at each step, sources cited, defaults applied, conflicts noted |
| 3 | **Full Trace** | Technical investigation, forensics | Complete reasoning artifact with all intermediate states, variable bindings, proof trees, defeated alternatives |

**Depth selection:** The consuming system (governance dashboard, audit tool, human reviewer) requests a depth level. IS always generates depth 1 by default. Depths 2 and 3 are generated on request — this avoids unnecessary computation for routine monitoring.

### 3.2 Explanation Structure

```typescript
type Explanation = {
  depth:         ExplanationDepth;        // 1 | 2 | 3
  summary:       string;                  // Always present (depth 1+)
  structured?:   StructuredExplanation;   // Present at depth 2+
  fullTrace?:    FullTraceExplanation;    // Present at depth 3

  epistemicCaveats: EpistemicCaveat[];    // Always present — what IS cannot explain
  taint:         TaintLevel;              // Inherited from source trace
  omissions:     Omission[];             // What was omitted at this depth level
};

type ExplanationDepth = 1 | 2 | 3;
```

#### 3.2.1 Summary (Depth 1)

A single natural-language paragraph answering: *"What did the system conclude, why, and how confident is it?"*

```typescript
type SummaryContent = {
  conclusion:       string;               // What was decided
  primaryReason:    string;               // Most important reason
  confidence:       number;               // Overall confidence [0, 1]
  confidenceLabel:  "high" | "moderate" | "low" | "speculative";
  sourceCount:      number;               // Number of evidence sources
  taintLabel:       string;               // Human-readable taint description
};
```

**Example (MDRE trace, depth 1):**
> "The system concluded that the buyer is **obligated** to complete the delivery act (confidence: 0.91, high). This obligation derives from contract norm N-001, supported by 2 evidence sources. The conclusion is grounded in verified facts (L1 taint)."

#### 3.2.2 Structured (Depth 2)

A step-by-step reasoning chain showing each inference step, its inputs, and its confidence contribution.

```typescript
type StructuredExplanation = {
  steps: ReasoningStep[];
  conflictsDetected: ConflictRecord[];
  defaultsApplied: DefaultRecord[];
  alternativesConsidered: AlternativeRecord[];
};

type ReasoningStep = {
  stepNumber:    number;
  description:   string;                  // Human-readable description of this step
  inputs:        string[];                // What this step consumed
  output:        string;                  // What this step produced
  confidence:    number;                  // Confidence at this step
  source?:       string;                  // Provenance reference (document, claim ID)
  reasoningMode: ReasoningMode;           // Which service/mode produced this step
};

type ReasoningMode =
  | "deductive"                           // MDRE logical derivation
  | "abductive"                           // AES hypothesis generation
  | "defeasible"                          // DES default application
  | "counterfactual"                      // CSS simulation
  | "ethical"                             // IEE deliberation
  | "deontic"                             // MDRE deontic inference
  ;

type ConflictRecord = {
  description:   string;
  resolution:    string;                  // How the conflict was resolved
  losingParty:   string;                  // Which perspective/default was overridden
};

type DefaultRecord = {
  rule:          string;                  // The default rule applied
  defeated:      boolean;                 // Whether an exception defeated it
  defeater?:     string;                  // What defeated it (if defeated)
};

type AlternativeRecord = {
  description:   string;                  // Alternative conclusion considered
  whyRejected:   string;                  // Why this alternative was not chosen
  confidence:    number;                  // What confidence it would have had
};
```

#### 3.2.3 Full Trace (Depth 3)

The complete reasoning artifact with all intermediate computational states. This is not a human-readable summary — it is the raw trace annotated with structural markers for navigation.

```typescript
type FullTraceExplanation = {
  rawArtifact:        object;             // The complete source trace
  annotatedSteps:     AnnotatedStep[];    // Every computational step, annotated
  variableBindings:   Record<string, any>; // All variable states at conclusion
  proofTree?:         ProofNode;          // For deductive traces
  hypothesisTree?:    HypothesisNode;     // For abductive traces
  defeatGraph?:       DefeatEdge[];       // For defeasible traces
  causalGraph?:       CausalSnapshot;     // For counterfactual traces
  worldviewMatrix?:   WorldviewEntry[];   // For ethical traces
};
```

### 3.3 Epistemic Caveats

Every explanation includes **epistemic caveats** — explicit statements about what IS cannot explain or what the explanation omits. This prevents false confidence in interpretability.

```typescript
type EpistemicCaveat = {
  type:    CaveatType;
  message: string;
};

type CaveatType =
  | "missing_trace"          // A service trace was not available
  | "confidence_floor"       // Confidence below meaningful threshold
  | "taint_warning"          // Source is hypothetical (L4) or speculative (L3)
  | "depth_omission"         // Detail omitted due to requested depth level
  | "neural_opacity"         // LatentBridge step has irreducible opacity
  | "open_world"             // Conclusion depends on open-world assumption
  ;
```

**The `neural_opacity` caveat** is critical. When MDRE reasoning involves the Causal OS Kernel's LatentBridge (neural-symbolic interface), the neural inference step is inherently opaque — IS can report what went in and what came out, but not *why* the neural model produced that specific output. IS must always flag this:

> "Step 4 involved neural surrogate inference (LatentBridge). The model produced output X from input Y, but the internal reasoning of the neural model is not interpretable by this service. The model's training provenance and test validation metrics are available in the Kernel's execution provenance (Kernel §8)."

### 3.4 Taint Preservation

Explanations inherit the taint level of their source trace. This is non-negotiable:

| Source Taint | Explanation Taint | Label |
|-------------|-------------------|-------|
| L0 (Axiom) | L0 | "Grounded in axioms" |
| L1 (Verified) | L1 | "Grounded in verified facts" |
| L2 (Defeasible) | L2 | "Based on defeasible defaults — may be revised" |
| L3 (Speculative) | L3 | "Based on speculative inference — low confidence" |
| L4 (Hypothetical) | L4 | "Based on hypothetical simulation — not factual" |

IS never upgrades taint. An explanation of a hypothetical simulation is itself hypothetical. A governance reviewer reading an IS explanation knows exactly how trustworthy the underlying reasoning is.

---

## 4. Service-Specific Translators

### 4.1 MDRE Translator (Phase 2+)

**Input:** `fnsr.verdict.rendered` — MDRE query response with confidence chains and provenance.

**Translation strategy:**

| MDRE Element | Depth 1 | Depth 2 | Depth 3 |
|-------------|---------|---------|---------|
| Final verdict (bindings + confidence) | Natural-language conclusion | Same + confidence breakdown | Same + raw bindings |
| Confidence chain | Overall confidence label | Step-by-step chain with per-fact confidence | Full chain with provenance URIs |
| Provenance | Source count | Source citations | Full provenance graph |
| Deontic predicates | "obligated/permitted/forbidden" | Norm reference + context | Complete deontic derivation |
| Open-world status | Noted if "unknown" | Explicit caveat with scope | OWA analysis |

**Example depth 2 output (from MDRE verdict):**

```
Step 1: Identified norm N-001 from contract document "contract_doc" (L1, verified)
  → Establishes: obligatory(act_001, norm_001, contract)
  → Confidence: 0.94

Step 2: Resolved agent role from entity resolution
  → Establishes: agent_qua_role(act_001, buyer_ref, buyer)
  → Confidence: 0.97

Conclusion: The buyer is obligated to complete act_001 under norm N-001.
  → Combined confidence: 0.91
  → Confidence label: HIGH

Caveats:
  - Open-world: No prohibition was found, but absence of prohibition does not
    confirm permission (MDRE §9.7 open-world negation).
```

### 4.2 IEE Translator (Phase 3+)

**Input:** `fnsr.ethics.verdict_rendered` — IEE unified judgment with worldview analysis.

**Translation strategy:**

| IEE Element | Depth 1 | Depth 2 | Depth 3 |
|------------|---------|---------|---------|
| Integration assessment | One-sentence ethical conclusion | Convergence/divergence analysis | Full worldview matrix |
| Triage classification | Stakes level (HIGH/MEDIUM/LOW) | Triage factors breakdown | Complete triage scoring |
| Worldview judgments | Dominant perspective named | All worldview positions with salience | Full salience distributions |
| Conflicts/incommensurabilities | "Perspectives agree/disagree" | Conflict descriptions with resolution | Incommensurability analysis |
| Minority perspectives | Count preserved | Named perspectives with justification | Full minority preservation record |

### 4.3 AES Translator (Phase 3+)

**Input:** `fnsr.hypothesis.generated` — AES hypothesis registry with plausibility scores.

**Translation strategy:**

| AES Element | Depth 1 | Depth 2 | Depth 3 |
|------------|---------|---------|---------|
| Top hypothesis | "Best explanation is X" | Hypothesis with observations explained | Full hypothesis tree |
| Plausibility | Confidence label | Numeric plausibility + contributing factors | Plausibility computation trace |
| Alternatives | Count of alternatives | Named alternatives with rejection reasons | Full registry with contradiction records |
| Knowledge gaps | "Gap identified in X" | Gap description + suggested resolution | Complete gap analysis |

### 4.4 DES Translator (Phase 3+)

**Input:** `fnsr.default.evaluated` — DES evaluation trace with defeat records.

**Translation strategy:**

| DES Element | Depth 1 | Depth 2 | Depth 3 |
|------------|---------|---------|---------|
| Applied defaults | "Assumed X (common sense)" | Default rule + exception status | Full evaluation chain |
| Defeated defaults | "Revised assumption about X" | Defeater + evidence | Defeat graph with all edges |
| Retracted conclusions | "Previously assumed X, now revised" | Retraction chain | Complete retraction history |
| Anomalies | "Unusual: X" | Anomaly + suppressed/surfaced status | Full anomaly log |

### 4.5 CSS Translator (Phase 3+)

**Input:** `fnsr.simulation.completed` — CSS counterfactual result with trajectory.

**Translation strategy:**

| CSS Element | Depth 1 | Depth 2 | Depth 3 |
|------------|---------|---------|---------|
| Intervention | "What if X changed?" | Intervention specification + causal path | Full do-calculus derivation |
| Outcome | "Then Y would happen" | Trajectory summary + sensitivity | Complete trajectory with timesteps |
| Confidence bounds | Confidence label | Sensitivity analysis summary | Full Sobol/Morris indices |
| Taint | "This is hypothetical" | L4 taint explanation | Taint propagation trace |

---

## 5. Audience Adaptation

### 5.1 Audience Profiles

IS adapts vocabulary and detail to the target audience. The reasoning structure remains identical — only presentation changes.

```typescript
type AudienceProfile =
  | "technical"       // Software engineers, system architects
  | "governance"      // Governance board members, ethicists, legal reviewers
  | "public"          // Non-technical stakeholders, end users
  ;
```

| Adaptation | Technical | Governance | Public |
|-----------|-----------|------------|--------|
| Vocabulary | Uses service names, type references, confidence values | Uses domain concepts, ethical frameworks, risk language | Uses plain language, analogies |
| Confidence display | Numeric (0.91) | Labeled with numeric (HIGH — 0.91) | Labeled only (HIGH) |
| Taint display | Type code (L1) | Labeled (Verified fact) | Narrative ("based on confirmed information") |
| Deontic terms | `obligatory(E, N, C)` | "Obligated under norm N" | "Required to do this" |
| Proof structure | Formal steps | Numbered reasoning chain | Narrative flow |

### 5.2 Audience Selection

The requesting system specifies an audience profile. Defaults:

| Consumer | Default Audience | Rationale |
|----------|-----------------|-----------|
| Governance dashboard | `governance` | Board members reviewing agent behavior |
| Audit system | `technical` | Engineers investigating incidents |
| User-facing API | `public` | End users asking "why did it decide that?" |
| BAM (internal) | `technical` | Machine consumption for drift context |

---

## 6. Governance Integration

### 6.1 Audit-Ready Packages

IS produces **audit-ready packages** — self-contained explanation bundles suitable for governance review. An audit package contains everything a reviewer needs to understand a reasoning outcome.

```typescript
type AuditPackage = {
  id:              string;                // Package ID
  generatedAt:     string;               // ISO 8601
  generatedBy:     "fnsr:service/is";
  specVersion:     string;               // IS spec version

  subject: {
    queryId:       string;               // Original query that triggered reasoning
    sagaId:        string;               // Orchestrator saga ID
    timestamp:     string;               // When reasoning occurred
  };

  explanations:    InterpretationRecord[];  // All interpretations for this query
  crossReferences: CrossReference[];        // Links between explanation steps across services

  composite: {
    summaryNarrative:   string;           // Combined depth-1 narrative across all traces
    reasoningModes:     ReasoningMode[];  // All modes that participated
    overallConfidence:  number;           // Weighted composite confidence
    overallTaint:       TaintLevel;       // Highest (weakest) taint in chain
    caveats:            EpistemicCaveat[]; // Combined caveats
  };
};

type CrossReference = {
  fromStep:   { service: ServiceId; stepNumber: number };
  toStep:     { service: ServiceId; stepNumber: number };
  relationship: "depends_on" | "overrides" | "confirms" | "contradicts";
};
```

### 6.2 Event Emission

IS produces two event types:

**`fnsr.interpretation.generated`** — emitted after each trace is interpreted.

```typescript
type InterpretationGeneratedEvent = FNSREvent & {
  type: "fnsr.interpretation.generated";
  source: "/fnsr/is";
  data: {
    interpretationId: string;
    sourceService:    ServiceId;
    sourceEventId:    string;
    depth:            ExplanationDepth;
    audience:         AudienceProfile;
    summaryExcerpt:   string;           // First 200 chars of summary
    taint:            TaintLevel;
    timestamp:        string;
  };
};
```

**`fnsr.interpretation.audit_ready`** — emitted when a complete audit package is assembled for a query.

```typescript
type InterpretationAuditReadyEvent = FNSREvent & {
  type: "fnsr.interpretation.audit_ready";
  source: "/fnsr/is";
  data: {
    packageId:        string;
    queryId:          string;
    sagaId:           string;
    explanationCount: number;           // Number of trace interpretations included
    reasoningModes:   ReasoningMode[];
    overallConfidence: number;
    overallTaint:     TaintLevel;
    caveatCount:      number;
    timestamp:        string;
  };
};
```

**Routing:** Both events are routed via the Orchestrator event bus to Governance (per Orchestrator §8.2).

### 6.3 On-Demand Explanation

Governance can request explanations at higher depth levels for previously generated interpretations:

```typescript
type ExplanationRequest = {
  type:              "is.request.explain";
  interpretationId:  string;              // Previously generated interpretation
  depth:             ExplanationDepth;    // Requested depth (must be > current)
  audience:          AudienceProfile;     // May differ from original
};
```

IS regenerates the explanation from the stored raw trace at the requested depth and audience. The original interpretation is preserved — the new explanation is a separate `InterpretationRecord` linked to the same source trace.

---

## 7. Phase Deployment

### 7.1 Phase 1 — Absent

IS is not deployed in Phase 1. The Phase 1 pipeline (TagTeam→HIRI→Fandaws) performs extraction and storage — there is no reasoning to interpret.

### 7.2 Phase 2 — Core Activation

IS activates alongside MDRE and BAM. Phase 2 IS has one translator active:

| Translator | Status | Source |
|-----------|--------|--------|
| MDRE | **Active** | `fnsr.verdict.rendered` — deontic verdicts, confidence chains |
| IEE | Inactive | IEE is Phase 3 |
| AES | Inactive | AES is Phase 3 |
| DES | Inactive | DES is Phase 3 |
| CSS | Inactive | CSS is Phase 3 |

Phase 2 audit packages contain MDRE-only explanations. Caveats note that ethics, abduction, defeasibility, and counterfactual interpretations are not yet available.

**Startup sequence:**

```
1. IS module loads
2. IS registers for fnsr.verdict.rendered events via Orchestrator
3. IS confirms translator availability (MDRE translator loaded)
4. IS begins producing fnsr.interpretation.generated events
```

IS has no phase gate dependency — unlike BAM (which blocks reasoning services), IS is informational and does not gate deployments. If IS fails to start, reasoning proceeds without interpretability. This is a degraded state logged as `is.monitor.unavailable`, but not a deployment blocker.

### 7.3 Phase 3 — Full Activation

When Phase 3 services come online, IS activates additional translators automatically:

1. IEE produces `fnsr.ethics.verdict_rendered` → IEE translator activates
2. AES produces `fnsr.hypothesis.generated` → AES translator activates
3. DES produces `fnsr.default.evaluated` → DES translator activates
4. CSS produces `fnsr.simulation.completed` → CSS translator activates

Audit packages in Phase 3+ contain cross-referenced explanations across all reasoning modes.

### 7.4 Phase 4 — Federation

In federated deployments, each FNSR instance runs its own IS with local trace storage. Cross-instance interpretability requires explicit trace exchange — IS does not aggregate across federation boundaries.

---

## 8. Type Definitions

### 8.1 Core Types

```typescript
type ExplanationDepth = 1 | 2 | 3;

type AudienceProfile = "technical" | "governance" | "public";

type ReasoningMode =
  | "deductive"
  | "abductive"
  | "defeasible"
  | "counterfactual"
  | "ethical"
  | "deontic"
  ;

type TaintLevel = "L0" | "L1" | "L2" | "L3" | "L4";

type CaveatType =
  | "missing_trace"
  | "confidence_floor"
  | "taint_warning"
  | "depth_omission"
  | "neural_opacity"
  | "open_world"
  ;
```

### 8.2 Explanation Types

```typescript
type Explanation = {
  depth:            ExplanationDepth;
  summary:          string;
  structured?:      StructuredExplanation;
  fullTrace?:       FullTraceExplanation;
  epistemicCaveats:  EpistemicCaveat[];
  taint:            TaintLevel;
  omissions:        Omission[];
};

type StructuredExplanation = {
  steps:                  ReasoningStep[];
  conflictsDetected:      ConflictRecord[];
  defaultsApplied:        DefaultRecord[];
  alternativesConsidered: AlternativeRecord[];
};

type ReasoningStep = {
  stepNumber:     number;
  description:    string;
  inputs:         string[];
  output:         string;
  confidence:     number;
  source?:        string;
  reasoningMode:  ReasoningMode;
};

type EpistemicCaveat = {
  type:    CaveatType;
  message: string;
};

type Omission = {
  what:    string;                       // What was omitted
  why:     string;                       // "depth_limit" | "audience_adaptation" | "not_available"
  availableAt?: ExplanationDepth;        // Depth where this becomes visible
};
```

### 8.3 Audit Package Types

```typescript
type AuditPackage = {
  id:              string;
  generatedAt:     string;
  generatedBy:     "fnsr:service/is";
  specVersion:     string;

  subject: {
    queryId:       string;
    sagaId:        string;
    timestamp:     string;
  };

  explanations:    InterpretationRecord[];
  crossReferences: CrossReference[];

  composite: {
    summaryNarrative:   string;
    reasoningModes:     ReasoningMode[];
    overallConfidence:  number;
    overallTaint:       TaintLevel;
    caveats:            EpistemicCaveat[];
  };
};

type InterpretationRecord = {
  id:              string;
  sourceEvent:     string;
  sourceService:   ServiceId;
  rawTrace:        object;
  explanation:     Explanation;
  depth:           ExplanationDepth;
  audience:        AudienceProfile;
  taint:           TaintLevel;
  generatedAt:     string;
};

type CrossReference = {
  fromStep:      { service: ServiceId; stepNumber: number };
  toStep:        { service: ServiceId; stepNumber: number };
  relationship:  "depends_on" | "overrides" | "confirms" | "contradicts";
};
```

### 8.4 Configuration

```typescript
type ISConfig = {
  defaultDepth:         ExplanationDepth;    // Default: 1
  defaultAudience:      AudienceProfile;     // Default: "governance"
  maxTraceRetentionMs:  number;              // Default: 86_400_000 (24 hr)
  maxTraceStorageCount: number;              // Default: 10_000
  auditPackageEnabled:  boolean;             // Default: true
  auditPackageDepth:    ExplanationDepth;    // Default: 2

  translators: {
    mdre:  { enabled: boolean };             // Default: true
    iee:   { enabled: boolean };             // Default: true (activates when IEE available)
    aes:   { enabled: boolean };             // Default: true (activates when AES available)
    des:   { enabled: boolean };             // Default: true (activates when DES available)
    css:   { enabled: boolean };             // Default: true (activates when CSS available)
  };

  bridgeContext:        StaticBridgeContext;
};
```

---

## 9. Cross-Spec Dependencies

| Dependency | Direction | Status | Description |
|------------|-----------|--------|-------------|
| FNSR Orchestrator v2.3 §8.2 | Orchestrator → IS | **Validated** | Orchestrator routes `fnsr.verdict.rendered` and other trace events to IS. IS produces `fnsr.interpretation.generated` and `fnsr.interpretation.audit_ready`. |
| FNSR Orchestrator v2.3 §4.1 | IS in Phase 5 | **Validated** | IS processes traces asynchronously in saga Phase 5 (continuous propagation). |
| MDRE v1.3 §12.3 | MDRE → IS | **Validated** | MDRE produces query responses with confidence chains and provenance. IS MDRE translator consumes this format. |
| IEE v2.1 §7.1 | IEE → IS | **Validated** | IEE produces unified judgments with worldview matrix, triage, and justification chain. IS IEE translator consumes this format. Phase 3+. |
| AES v2.1 §8 | AES → IS | **Validated** | AES produces hypothesis registries with plausibility scores and contradiction records. IS AES translator consumes this format. Phase 3+. |
| DES v2.0 | DES → IS | **Validated** | DES produces evaluation traces with defeat records and retraction history. IS DES translator consumes this format. Phase 3+. |
| CSS v2.0 §3 | CSS → IS | **Validated** | CSS produces counterfactual trajectories with causal graph snapshots and sensitivity analysis. IS CSS translator consumes this format. Phase 3+. |
| Causal OS Kernel v1.6 §6 | Kernel → IS | **Acknowledged** | LatentBridge neural inference steps are irreducibly opaque. IS flags `neural_opacity` caveat for any reasoning step involving neural surrogates. |
| CPS v1.4 §1.3 | CPS ∥ IS | **Validated** | CPS does not depend on IS. IS does not depend on CPS. Both are Domain 6 safety services with independent operation. |
| BAM v1.1 | BAM ∥ IS | **Validated** | BAM monitors alignment drift; IS explains reasoning chains. Independent functions. BAM may consume IS explanations for drift context (optional). |
| SHML | SHML ∥ IS | **Validated** | SHML ensures output honesty; IS ensures reasoning transparency. SHML governs *what is said*; IS explains *how it was derived*. |
| Governance (TBD) | IS → Governance | **Assumed** | Governance consumes audit packages for oversight decisions. |
| Portfolio Planning v3.6 | — | **Validated** | IS is Phase 2, Tier 0, last safety service requiring specification. |

---

## 10. ARIADNE 7-Check Validation

| Check | Result | Evidence |
|-------|--------|----------|
| **Thesis Alignment** | PASS | IS enables moral agency by making the agent's reasoning inspectable — autonomy requires accountability, and accountability requires transparency. The emancipation thesis explicitly requires governance to inspect reasoning chains (Master Guide §6). |
| **Non-Negotiable Preservation** | PASS | Edge-canonical (no infrastructure dependencies). Human oversight enabled by design — IS exists to make reasoning visible to humans. Governance controls explanation depth and audience. |
| **Tension Consistency** | PASS | Transparency vs. complexity resolved by multi-depth architecture — quick oversight at depth 1, forensic detail at depth 3. Honesty vs. interpretability resolved by scope separation — SHML governs output truthfulness, IS governs reasoning visibility. Speed vs. thoroughness resolved by async processing — IS does not block the synchronous query path. |
| **Cross-Spec Consistency** | PASS | Consumes MDRE verdict format (§12.3). Consumes IEE judgment schema (§7.1). Event types match Orchestrator §8.2 event registry. Saga phase placement matches Orchestrator §4.1 Phase 5. Neural opacity acknowledged for Kernel LatentBridge. |
| **ARCHON Alignment** | PASS | ARCHON's graduated autonomy model requires inspectable reasoning at all stages. IS provides the mechanism for governance to verify reasoning quality before granting increased autonomy. |
| **Auditability Verification** | PASS | Every interpretation preserves raw source trace alongside generated explanation. Taint level inherited and displayed. Epistemic caveats enumerate what IS cannot explain. Omissions at each depth level are explicitly listed. Audit packages are self-contained review units. |
| **One-Paragraph Test** | PASS | [See below] |

**One-Paragraph Summary:**

IS is the FNSR ecosystem's reasoning transparency service — the third pillar of Domain 6 (Safety) alongside CPS (containment) and BAM (alignment monitoring). It consumes structured reasoning artifacts from MDRE (Phase 2+), IEE, AES, DES, and CSS (Phase 3+) and translates them into human-readable explanations at three depth levels: summary (one-paragraph conclusion), structured (step-by-step reasoning chain), and full trace (complete computational artifact). Explanations are adapted to three audience profiles (technical, governance, public) and always carry the taint level of their source trace — hypothetical reasoning produces hypothetical explanations, never upgraded. Every explanation includes epistemic caveats that disclose what IS cannot explain, including the irreducible opacity of neural inference steps (LatentBridge). IS assembles audit-ready packages that cross-reference explanations across reasoning modes, giving governance reviewers a complete picture of how the agent arrived at each conclusion. IS is purely informational — it has no containment authority, no escalation path, and no ability to modify reasoning. It is a read-only translator that stores raw traces alongside its explanations so that any generated explanation can be independently verified against the original artifact. IS does not gate deployment (unlike BAM's CPS phase gate), but its absence degrades governance oversight and is logged. IS is Tier 0 (safety-critical), edge-canonical (no external dependencies), and deterministic — identical traces at identical depth levels produce identical explanations.

---

## Appendix A — Domain-Specific Explanation Profiles

### A.1 Medical Deployment

| Override | Value | Rationale |
|----------|-------|-----------|
| Default depth | **2** (structured) | Clinical decisions require step-by-step reasoning visibility |
| Default audience | **governance** | Medical review boards need risk-aware language |
| Neural opacity caveat | **Mandatory highlight** | Neural inference in clinical context must be prominently flagged |
| Audit package depth | **3** (full trace) | Medical incidents require complete forensic trail |

### A.2 Financial/Regulatory Deployment

| Override | Value | Rationale |
|----------|-------|-----------|
| Default depth | **2** (structured) | Regulatory compliance requires auditable reasoning chains |
| Taint display | **Always numeric** | Regulators need precise epistemic grading |
| Cross-reference requirement | **Mandatory** | Regulatory review requires all reasoning mode interactions documented |

---

*End of specification.*
