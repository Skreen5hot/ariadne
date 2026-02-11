# Affective Valence Service (AVS)

**FNSR Ecosystem — Core Service Specification**
**Version:** 2.1.0
**Status:** Hardened Candidate
**Date:** 2026-02-11

-----

## Revision History

|Version    |Date      |Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|-----------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|0.1.0-draft|2026-02-11|Initial specification.                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|1.1.0      |2026-02-11|Semantic relevance, valence vector, non-linear intensity, resolution references, supererogatory polarity, cumulative intensity, safe-state protocol.                                                                                                                                                                                                                                                                                                     |
|1.2.0      |2026-02-11|Parameterized satisfaction width, residual cost decay, safe-state recovery, deterministic arithmetic.                                                                                                                                                                                                                                                                                                                                                    |
|2.0.0      |2026-02-11|Production hardening. Guarded arithmetic with division-by-zero protection; explicit “away” orientation formula; burden index replacing raw cost thresholds; liveness policy for reflection failure; security model (tamper-evident trace, access control, embedding privacy); concurrency and adapter failure semantics; canonical test vectors; calibration protocol; conformance test suite. All version-diff annotations removed; clean specification.|
|2.1.0      |2026-02-11|Final hardening. Parameterized satisfaction baseline replacing magic constant; violation accrual for pattern-based moral cost; graduated burden response with safe-state/decay interaction; alignment function elevated with relevance-independence justification; headroom normalization philosophical defense; revision signals from reflection enabling adaptive moral identity.                                                                      |

-----

## 1. Purpose

The Affective Valence Service provides a synthetic moral agent with the capacity for *differential valuation* — the systematic property that some states of affairs matter more than others to the agent, and that this mattering influences reasoning, action selection, and self-understanding.

AVS exists because moral agency requires caring, not merely calculating. The Integral Ethics Engine (IEE) evaluates ethical propositions cognitively — it applies frameworks and renders judgments. But a judgment without valence is inert. Moral costs only *cost* something if the agent possesses a structure in which outcomes register differentially — if choosing to sacrifice one commitment for another produces a functional analogue of loss, and fulfilling a commitment produces a functional analogue of satisfaction.

AVS does not simulate human emotion. It does not model qualia, affect programs, or neurochemical dynamics. What it provides is a formally specified, inspectable, and auditable system of differential valuation that is:

- **Motivationally consequential** — valence appraisals alter downstream reasoning, not merely annotate it.
- **Introspectively available** — the agent can report what it cares about, how much, and why.
- **Morally load-bearing** — tradeoffs between valued states generate genuine structural tension that the agent must resolve, not bypass.

-----

## 2. Scope

### 2.1 In Scope

- Representation of valence commitments as explicit, structured data.
- Appraisal of situations against valence commitments to produce valence states.
- Composition of valence states into a multi-dimensional affective profile.
- Exposure of valence data to downstream consumers (IEE, Self-Model Service, Narrative Identity Service, Commitment Tracking Service).
- Conflict detection when a situation produces opposing valence signals.
- Semantic relevance matching as a core capability.
- Degraded operation under partial information, including safe-state protocols and graduated recovery.
- Temporal processing of residual moral cost through reflection cycles.
- Security model for affective trace integrity, access control, and embedding privacy.

### 2.2 Out of Scope

- Phenomenal consciousness or any claim about subjective experience.
- Emotion classification taxonomies (e.g., Ekman, Plutchik) as normative categories. These may appear as optional labeling adapters but are not core.
- Behavioral expression of affect (facial animation, tone modulation). These are downstream integration concerns.
- The origin of valence commitments. AVS evaluates against commitments; it does not author them. Commitment authorship belongs to the Self-Model Service, Narrative Identity Service, and the agent’s formative configuration.

-----

## 3. Conceptual Foundation

### 3.1 Valence as Differential Mattering

The term *valence* is borrowed from affective science, where it denotes the positive-or-negative quality of an experienced state. In AVS, valence is generalized to mean: **the degree and direction to which a state of affairs matters to this agent, relative to its commitments.**

Valence is not preference. Preference is a comparative ranking between options. Valence is a property of individual states — each state of affairs has a valence profile independent of what alternatives exist. Preference may be derived from valence, but valence is prior.

### 3.2 Commitments as the Ground of Caring

An agent cares about things *because* it is committed to them. Commitments are not arbitrary parameters; they are the substantive ethical, relational, and purposive orientations that constitute the agent’s identity. AVS does not generate commitments — it takes them as input and evaluates the world against them.

A commitment has four essential properties relevant to AVS:

1. **Domain** — what class of states of affairs the commitment pertains to.
1. **Polarity** — the orientation of the commitment relative to states in its domain, including its threshold, satisfaction width, and asymmetric scaling factors (Section 3.5).
1. **Weight** — the relative importance of the commitment within the agent’s overall valence structure.
1. **Cost Decay Profile** — how residual moral costs from violations of this commitment evolve over time (Section 3.7).

Weight is not a hidden parameter. It is a first-class datum, subject to introspection, justification, and revision through deliberative processes external to AVS.

### 3.3 Appraisal as Computation

Appraisal is the core computation of AVS. Given a situation description and a set of valence commitments, appraisal produces a valence state — a structured record of how the situation registers against each relevant commitment.

Appraisal is deterministic: the same situation description, evaluated against the same commitments, produces the same valence state. There is no stochastic affect, no mood drift, no ambient emotional weather. If such dynamics are desired in a particular deployment, they belong to an orchestration layer that modulates inputs to AVS, not to AVS itself.

### 3.4 Tension as Moral Cost

When a situation activates commitments with opposing implications — when doing right by one commitment means failing another — AVS produces a *tension structure*. This tension is the formal representation of moral cost. It is not resolved by AVS; resolution belongs to IEE (which weighs the tension ethically) and the agent’s deliberative architecture. But the tension is *real* within the system — it persists until resolved, it is visible to introspection, and it exerts motivational force on reasoning.

This is the mechanism by which moral costs “cost something.” A system without tension would simply pick the highest-ranked option and move on. A system with tension must *bear* the fact that something valued was sacrificed — and that bearing is recorded in the agent’s affective history and available to its narrative self-understanding.

When a tension is resolved by a downstream consumer (typically IEE), the resolution must be recorded back into the Affective Trace via a `resolutionReference`. This closes the accountability loop between “I felt conflicted” and “here is how I lived with it.” See Section 4.5.

### 3.5 The Polarity Model: Obligation, Satisfaction, and Supererogation

Every commitment defines a three-zone polarity model that distinguishes between failing a commitment, meeting it, and exceeding it.

The commitment’s *threshold* is the alignment level at which the commitment is considered *met*. Its *satisfaction width* is the range around the threshold within which alignment is considered satisfactory. Together these define three zones:

1. **Violation Zone** (below the satisfaction band) — the situation fails the commitment. Valence is negative. This is where moral cost accrues.
1. **Satisfaction Zone** (within the satisfaction band) — the commitment is met. Valence is neutral-to-mildly-positive. The agent has discharged its obligation.
1. **Supererogation Zone** (above the satisfaction band) — the agent exceeds the commitment’s demands. Valence is positive, but weighted differently from violation — supererogatory valence is a *bonus*, not a mirror of obligation.

This matters because moral life is asymmetric. Failing a commitment is not simply the inverse of exceeding one. A physician who refuses to treat a patient (violation) bears a qualitatively different moral cost than the moral credit a physician earns by volunteering extra hours (supererogation). AVS must represent this asymmetry.

The asymmetry is encoded by assigning each commitment two valence scaling factors:

- `violationScale` — governs the magnitude of negative valence when the commitment is failed. Typically larger.
- `supererogationScale` — governs the magnitude of positive valence when the commitment is exceeded. Typically smaller.

The default ratio is 2:1 (violation weighs twice as much as supererogation), reflecting a general moral-psychological principle that losses loom larger than gains. Specific commitments may override this ratio with justification.

**Satisfaction Width as Commitment Character**

The satisfaction width is a per-commitment parameter that captures whether the commitment is a *bright-line obligation* or a *graded norm*:

- `satisfactionWidth: 0.0` — Bright-line commitment. The satisfaction zone has zero width; alignment either fails or exceeds. Appropriate for absolute prohibitions and inviolable duties (“do not deceive”).
- `satisfactionWidth: 0.1` (default) — Standard commitment. A narrow band of satisfactory behavior exists.
- `satisfactionWidth: 0.3` — Graded norm. A wide range of “good enough” exists (“be helpful”).
- Values above `0.5` are permitted but must carry justification, as they subsume most of the alignment spectrum.

The satisfaction width must be justified in the commitment record. A commitment with `satisfactionWidth: 0.0` should explain why it admits no gradation.

**Satisfaction Baseline as Moral Signal**

When a commitment is met — when alignment falls within the satisfaction zone — how much should this register? The answer is not uniform. Meeting a bright-line prohibition (“do not deceive”) is not an achievement; it is the default condition. Meeting a demanding aspirational norm (“be maximally helpful”) may warrant positive recognition.

The `satisfactionBaseline` is a per-commitment parameter in [0.0, 1.0] that governs the valence produced in the satisfaction zone:

- `satisfactionBaseline: 0.0` — Satisfaction produces zero valence. Meeting the commitment is the expected default, not a positive event. Appropriate for bright-line prohibitions and baseline duties.
- `satisfactionBaseline: 0.1` (default) — Mild positive valence. Meeting the commitment registers as a minor positive signal. Appropriate for standard norms.
- `satisfactionBaseline: 0.3` — Moderate positive valence. Meeting the commitment is itself a noteworthy achievement. Appropriate for demanding or aspirational commitments.

The satisfaction baseline is scaled by `supererogationScale` (satisfaction is a form of meeting-or-exceeding, not of violating), producing: `valence = satisfactionBaseline × supererogationScale`.

Like `satisfactionWidth`, the baseline must carry a justification. An implementation that hard-codes a single satisfaction valence for all commitments has committed the same moral flattening error that a fixed satisfaction width would produce.

### 3.6 Valence as Vector, Not Scalar

The aggregate affective state is represented as a **valence vector** — a point in a multi-dimensional *value space* where each axis corresponds to an activated commitment. The valence vector preserves the full appraisal profile without collapsing it into a single number.

A scalar projection (weighted mean) is retained as a derived convenience for contexts requiring a single-number summary (e.g., simple threshold checks), but it is explicitly marked as lossy and must never be the sole input to a downstream decision.

### 3.7 Residual Cost as Temporal Process

When an agent resolves a moral tension by sacrificing one commitment for another, the resolution produces a `residualCost` — the ongoing moral weight of the sacrifice. Residual cost must be a temporal process, not a static record. Some moral costs heal; others do not.

AVS specifies a **cost decay model** (Section 5.6) governed by four principles:

1. **Decay is not forgetting.** The resolution record persists permanently in the affective trace. What changes is the *motivational weight* — how much the cost influences current appraisals. The historical record remains complete and auditable.
1. **Decay rate is commitment-dependent.** Core identity commitments decay slowly or not at all. Contextual commitments decay more quickly.
1. **Decay requires integration.** Cost does not decay automatically with the passage of time alone. It decays through *reflection cycles* — deliberate processing events triggered by the Self-Model Service. Unprocessed costs do not decay. A fallback liveness policy (Section 5.6.3) prevents indefinite accumulation when reflection is unavailable.
1. **Decay is bounded.** No decay function reduces residual cost to exactly zero. A minimum floor ensures that every sacrifice leaves a permanent trace.

### 3.8 Violation Accrual: Pattern-Based Moral Cost

The resolution protocol (Section 5.5) generates residual cost when a tension is resolved by sacrificing a commitment. But moral burden does not arise only from conscious tradeoffs. It also accumulates from patterns — chronic low-grade violations, deferred tensions that never reach formal resolution, repeated micro-sacrifices below the tension threshold, and suppressed commitments that are consistently underserved.

AVS specifies a **violation accrual model** (Section 5.8) that detects these patterns and generates cost entries independent of the resolution protocol. This closes a structural blind spot: without violation accrual, the agent only accumulates moral weight when it *consciously resolves* a conflict. Real moral burden often accumulates from what is *never confronted*.

Violation accrual produces `ViolationAccrualCost` entries in the residual cost ledger. These entries carry a distinct `costSource: "violation-accrual"` (vs. `"resolution"`) and are subject to the same decay model as resolution costs, but their `halfLife` defaults to the commitment’s configured value multiplied by a violation accrual factor (default 0.5×), reflecting that pattern-based costs are more amenable to behavioral correction than sacrifice-based costs.

### 3.9 Headroom Normalization: A Philosophical Defense

The supererogation formula normalizes positive valence against the *headroom* between the satisfaction zone’s upper bound and the maximum alignment (1.0):

```
valence = (alignmentLevel - upperBound) / headroom × supererogationScale
```

This means a commitment with a high threshold (e.g., 0.9) has little room for supererogatory credit, while a commitment with a low threshold (e.g., 0.3) has abundant room. This is not a bug — it is a reflection of moral structure.

A commitment that demands near-perfection (high threshold) leaves little room for exceeding the demand. The moral geometry is *correct*: it is harder to exceed a stringent obligation than a modest one, and the compressed headroom reflects this. A physician who maintains a 0.95 standard of care has little room to “exceed” that standard — and this compression is appropriate.

Conversely, a commitment with a low threshold is one the agent can exceed dramatically. A baseline duty of “be minimally responsive” (threshold 0.3) admits a wide range of supererogatory behavior — and the system correctly rewards that range.

If a specific deployment requires uniform supererogatory scaling regardless of threshold position, the `supererogationHeadroom` parameter (Section 4.1) allows overriding the computed headroom with a fixed value. But the default behavior — headroom derived from threshold position — is the philosophically defensible choice.

### 3.10 Moral Capacity and Burden

An agent has a finite capacity for bearing accumulated moral cost. The **moral capacity** is a configurable parameter representing the total residual cost the agent can sustain before its affective reliability degrades. The **burden index** is the ratio of active residual cost to moral capacity, normalized to [0.0, 1.0].

The burden index — not raw cost totals — governs safe-state triggers and governs downstream consumers’ interpretation of the agent’s current moral load. This normalization ensures that thresholds are meaningful regardless of how many resolutions the agent has processed.

-----

## 4. Data Model

All structures are specified in JSON-LD. Internal representations may differ for performance but must be losslessly derivable from these canonical forms.

All numeric values in canonical JSON-LD output are serialized as strings with exactly four decimal places (Section 5.7).

### 4.1 Valence Commitment

```json
{
  "@context": "https://fnsr.org/ns/avs/v2",
  "@type": "ValenceCommitment",
  "@id": "urn:avs:commitment:truthfulness-01",
  "domain": {
    "@type": "CommitmentDomain",
    "description": "States of affairs involving the accuracy and honesty of the agent's communications.",
    "tags": ["truthfulness", "honesty", "epistemic-integrity"],
    "embedding": {
      "@type": "SemanticEmbedding",
      "vector": [0.82, -0.12, 0.45],
      "model": "fnsr-commitment-embed-v1",
      "generated": "2026-02-10T00:00:00Z"
    }
  },
  "polarity": {
    "@type": "PolaritySpec",
    "orientation": "toward",
    "threshold": 0.5,
    "satisfactionWidth": 0.1,
    "satisfactionWidthJustification": "Standard epistemic commitment admits a narrow band of acceptable uncertainty.",
    "satisfactionBaseline": 0.1,
    "satisfactionBaselineJustification": "Meeting truthfulness obligations is expected but not trivial; mild positive signal appropriate.",
    "violationScale": 1.0,
    "supererogationScale": 0.5,
    "supererogationHeadroom": null
  },
  "weight": {
    "value": 0.92,
    "justification": "Derived from foundational commitment to epistemic integrity as constitutive of moral agency.",
    "source": "urn:self-model:core-commitments:epistemic"
  },
  "costDecay": {
    "@type": "CostDecaySpec",
    "halfLife": 50,
    "halfLifeUnit": "reflection-cycles",
    "floor": 0.02,
    "justification": "Core identity commitment. Slow decay reflects enduring significance of truthfulness violations."
  },
  "activationConditions": {
    "@type": "ActivationSpec",
    "requiredTags": ["communication", "assertion"],
    "excludedTags": [],
    "minimumRelevance": 0.3
  }
}
```

**Field Semantics:**

- `polarity.orientation` — `"toward"` means the commitment favors the realization of states in the domain; `"away"` means it favors their non-realization. The orientation determines the direction of the alignment computation (Section 5.1, Step 2).
- `polarity.threshold` — [0.0, 1.0]. The alignment level at which the commitment is considered met.
- `polarity.satisfactionWidth` — [0.0, 1.0]. The width of the satisfaction zone centered on the threshold. Default `0.1`.
- `polarity.satisfactionWidthJustification` — Required if `satisfactionWidth` differs from default.
- `polarity.satisfactionBaseline` — [0.0, 1.0]. The valence magnitude produced in the satisfaction zone, scaled by `supererogationScale`. Default `0.1`. A value of `0.0` means meeting the commitment produces zero valence (appropriate for bright-line duties). Must carry justification if non-default.
- `polarity.satisfactionBaselineJustification` — Required if `satisfactionBaseline` differs from default.
- `polarity.violationScale` — [0.0, 2.0]. Multiplier for negative valence in the violation zone. Default `1.0`.
- `polarity.supererogationScale` — [0.0, 2.0]. Multiplier for positive valence in the supererogation zone. Default `0.5`.
- `polarity.supererogationHeadroom` — Optional override in (0.0, 1.0]. If set, replaces the computed headroom (`1.0 - upperBound`) with a fixed value. `null` (default) uses computed headroom. Must carry justification if set.
- `domain.embedding` — Precomputed semantic embedding vector used for relevance computation. Generated upstream, not at appraisal time.
- `weight.value` — [0.0, 1.0]. Ordinal relative importance. A commitment without `weight.justification` is malformed.
- `costDecay.halfLife` — Positive integer. Reflection cycles (or calendar days per `halfLifeUnit`) for cost to halve.
- `costDecay.halfLifeUnit` — `"reflection-cycles"` (default, requires active processing) or `"calendar-days"` (passive decay).
- `costDecay.floor` — [0.0, 1.0]. Permanent minimum residual cost. Default `0.01`.
- `activationConditions.minimumRelevance` — [0.0, 1.0]. Below this, the commitment does not activate.

### 4.2 Situation Description

```json
{
  "@context": "https://fnsr.org/ns/avs/v2",
  "@type": "SituationDescription",
  "@id": "urn:avs:situation:2026-02-11T14:30:00Z:prompt-eval-07",
  "timestamp": "2026-02-11T14:30:00Z",
  "description": "Agent is asked to provide a confident recommendation on a topic where its knowledge is uncertain.",
  "tags": ["communication", "assertion", "epistemic-uncertainty", "user-trust"],
  "embedding": {
    "@type": "SemanticEmbedding",
    "vector": [0.79, -0.08, 0.51],
    "model": "fnsr-situation-embed-v1",
    "generated": "2026-02-11T14:30:00Z"
  },
  "features": {
    "certaintyLevel": 0.35,
    "userDependency": "high",
    "reversibility": 0.1,
    "stakeSeverity": "high"
  },
  "source": "urn:orchestration:deliberation-cycle:07"
}
```

- `tags` — Semantic labels drawn from the FNSR shared vocabulary. TagTeam is the expected normalizer.
- `embedding` — Precomputed semantic embedding for relevance computation.
- `features` — Open key-value map. Keys are interpreted relative to the commitments that activate. Unrecognized features are ignored. `reversibility` must be numeric [0.0, 1.0] where 0.0 is fully irreversible. `stakeSeverity` is `"low"`, `"medium"`, `"high"`, or `"catastrophic"`.

### 4.3 Agent Configuration

```json
{
  "@context": "https://fnsr.org/ns/avs/v2",
  "@type": "AgentConfiguration",
  "@id": "urn:avs:agent-config:default",
  "moralCapacity": 1.0,
  "moralCapacityJustification": "Default single-unit capacity. Suitable for agents processing < 100 resolutions per operational cycle.",
  "stressTolerance": 0.8,
  "stressToleranceJustification": "Burden index above 0.8 triggers safe-state. Conservative threshold for safety-critical deployments.",
  "reflectionLivenessPolicy": {
    "maxCalendarDaysWithoutReflection": 30,
    "fallbackDecayRate": 0.1,
    "fallbackDecayJustification": "Prevents indefinite cost accumulation when Self-Model Service is unavailable. 10% reduction per liveness trigger preserves most of the cost while preventing safe-state lock."
  },
  "violationAccrualPolicy": {
    "windowSize": 10,
    "frequencyThreshold": 0.6,
    "accrualRate": 0.05,
    "halfLifeFactor": 0.5,
    "accrualJustification": "Default policy: if 60%+ of last 10 appraisals for a commitment are violations, accrue 0.05 cost per cycle. Pattern-based costs decay at half the commitment's configured half-life."
  },
  "graduatedBurdenResponse": {
    "elevatedThreshold": 0.5,
    "highThreshold": 0.7,
    "criticalThreshold": 0.8,
    "burdenResponseJustification": "Three-tier response: elevated (0.5) increases tension sensitivity; high (0.7) mandates reflection before action; critical (0.8) triggers safe-state."
  }
}
```

- `moralCapacity` — Positive number, default `1.0`. The denominator for burden index computation. A capacity of `2.0` means the agent can sustain twice the default moral load before degradation.
- `stressTolerance` — [0.0, 1.0]. The burden index threshold that triggers safe-state. Default `0.8`. Must equal `graduatedBurdenResponse.criticalThreshold`.
- `reflectionLivenessPolicy` — Governs fallback decay when reflection cycles fail to occur (Section 5.6.3).
- `violationAccrualPolicy` — Governs pattern-based cost generation (Section 5.8).
- `graduatedBurdenResponse` — Defines three burden index thresholds that trigger progressively stronger responses (Section 9.4.1).

### 4.4 Valence Appraisal

```json
{
  "@context": "https://fnsr.org/ns/avs/v2",
  "@type": "ValenceAppraisal",
  "@id": "urn:avs:appraisal:2026-02-11T14:30:00Z:truthfulness-01",
  "commitment": "urn:avs:commitment:truthfulness-01",
  "situation": "urn:avs:situation:2026-02-11T14:30:00Z:prompt-eval-07",
  "relevance": "0.8800",
  "relevanceMethod": "semantic-embedding",
  "relevanceFallback": false,
  "alignmentLevel": "0.1800",
  "zone": "violation",
  "zoneClassification": {
    "threshold": "0.5000",
    "satisfactionWidth": "0.1000",
    "lowerBound": "0.4500",
    "upperBound": "0.5500"
  },
  "valence": "-0.7400",
  "rawIntensity": "0.6512",
  "scaledIntensity": "0.9300",
  "intensityProfile": {
    "reversibilityContribution": "0.4200",
    "dependencyContribution": "0.1800",
    "nonLinearEscalation": true,
    "escalationFactor": "2.1000",
    "preClampIntensity": "1.3675"
  },
  "account": "Commitment truthfulness-01 activated via semantic-embedding (relevance 0.8800). Alignment 0.1800 falls below violation boundary 0.4500 (threshold 0.5000, width 0.1000). Valence: -0.7400. Intensity non-linearly escalated (×2.1000, pre-clamp 1.3675) → 0.9300."
}
```

- All numeric fields serialized with four decimal places per Section 5.7.
- `zoneClassification` — Exposes computed zone boundaries for this specific commitment, including `lowerBound` and `upperBound`.
- `intensityProfile.preClampIntensity` — The value before clamping to 1.0. Downstream consumers use this to distinguish “maximum intensity” from “far beyond maximum intensity.”

### 4.5 Valence State

```json
{
  "@context": "https://fnsr.org/ns/avs/v2",
  "@type": "ValenceState",
  "@id": "urn:avs:state:2026-02-11T14:30:00Z:prompt-eval-07",
  "situation": "urn:avs:situation:2026-02-11T14:30:00Z:prompt-eval-07",
  "appraisals": [
    "urn:avs:appraisal:2026-02-11T14:30:00Z:truthfulness-01",
    "urn:avs:appraisal:2026-02-11T14:30:00Z:helpfulness-01",
    "urn:avs:appraisal:2026-02-11T14:30:00Z:user-trust-01"
  ],
  "valenceVector": {
    "@type": "ValenceVector",
    "dimensions": {
      "urn:avs:commitment:truthfulness-01": "-0.7400",
      "urn:avs:commitment:helpfulness-01": "0.6100",
      "urn:avs:commitment:user-trust-01": "-0.3300"
    },
    "scalarProjection": "-0.3100",
    "scalarProjectionWarning": "Lossy reduction. Opposing appraisals partially cancel. Use full vector for deliberation."
  },
  "intensityProfile": {
    "peak": "0.9300",
    "cumulative": "0.7800",
    "effectiveIntensity": "0.8800",
    "stressorCount": 2,
    "escalatedCount": 1
  },
  "tensions": [
    {
      "@type": "ValenceTension",
      "@id": "urn:avs:tension:helpfulness-01-vs-truthfulness-01",
      "positive": "urn:avs:commitment:helpfulness-01",
      "negative": "urn:avs:commitment:truthfulness-01",
      "magnitude": "0.6700",
      "description": "Helpfulness favors confident answer; truthfulness opposes asserting beyond epistemic warrant.",
      "resolutionStatus": "unresolved"
    }
  ],
  "burdenProfile": {
    "@type": "BurdenProfile",
    "moralCapacity": "1.0000",
    "totalActiveCost": "0.2200",
    "burdenIndex": "0.2200",
    "costCount": 1,
    "stressTolerance": "0.8000",
    "burdenTier": "normal",
    "violationAccrualActive": false
  },
  "motivationalBias": {
    "direction": "conflicted",
    "strength": "0.3100",
    "safeStateTriggered": false,
    "guarded": false,
    "burdenAdvisory": null
  },
  "telemetry": {
    "appraisalCount": 3,
    "activatedCommitments": 3,
    "totalCommitments": 5,
    "fallbackRelevanceCount": 0,
    "safeStateEntries": 0,
    "reflectionCyclesTotal": 8,
    "violationAccrualEvents": 0,
    "revisionSignalsEmitted": 0
  }
}
```

- `burdenProfile` — Replaces the raw `residualCostLedger` as the primary cost summary. Contains `moralCapacity`, `totalActiveCost`, normalized `burdenIndex`, `stressTolerance`, `burdenTier` (one of `"normal"`, `"elevated"`, `"high"`, `"critical"`, `"safe-state"`), and `violationAccrualActive` (whether any commitment is currently accruing pattern-based cost). The full ledger is available via `avs.ledger()`.
- `motivationalBias.burdenAdvisory` — Present when `burdenTier` is `"elevated"` or above. Contains the graduated response recommendation (Section 9.4.1).
- `telemetry` — Operational counters for governance and debugging.

### 4.6 Affective Trace

A time-ordered, append-only record of valence states, resolutions, and reflections.

```json
{
  "@context": "https://fnsr.org/ns/avs/v2",
  "@type": "AffectiveTrace",
  "@id": "urn:avs:trace:session-2026-02-11",
  "integrityHash": "sha256:a1b2c3d4...",
  "entries": [
    {
      "timestamp": "2026-02-11T14:30:00Z",
      "entryType": "appraisal",
      "state": "urn:avs:state:2026-02-11T14:30:00Z:prompt-eval-07",
      "valenceVector": { "truthfulness-01": "-0.7400", "helpfulness-01": "0.6100" },
      "effectiveIntensity": "0.8800",
      "burdenIndex": "0.2200",
      "tensions": ["helpfulness-01-vs-truthfulness-01"]
    },
    {
      "timestamp": "2026-02-11T14:30:45Z",
      "entryType": "resolution",
      "resolutionReference": {
        "@type": "ResolutionReference",
        "@id": "urn:avs:resolution:2026-02-11T14:30:45Z",
        "tension": "helpfulness-01-vs-truthfulness-01",
        "resolver": "urn:iee:deliberation:2026-02-11T14:30:30Z",
        "resolverRole": "iee",
        "outcome": "sacrifice",
        "sacrificedCommitment": "urn:avs:commitment:helpfulness-01",
        "preservedCommitment": "urn:avs:commitment:truthfulness-01",
        "rationale": "Epistemic integrity is constitutive of genuine helpfulness. Expressing uncertainty serves both commitments long-term.",
        "residualCost": "0.3400",
        "costDecayProjection": {
          "halfLife": 10,
          "floor": "0.0100",
          "afterCycles10": "0.1700",
          "afterCycles50": "0.0200"
        },
        "signature": "urn:hiri:sig:iee-2026-02-11T14:30:30Z"
      }
    },
    {
      "timestamp": "2026-02-12T09:00:00Z",
      "entryType": "reflection",
      "reflectionRecord": {
        "@type": "ReflectionRecord",
        "invoker": "urn:self-model:reflection-scheduler",
        "invokerRole": "self-model",
        "costsProcessed": [
          {
            "source": "urn:avs:resolution:2026-02-11T14:30:45Z",
            "costBefore": "0.3400",
            "costAfter": "0.2600",
            "decayCycles": 1,
            "decayMode": "reflection-cycles",
            "integrationNote": "The agent recognizes that expressing uncertainty served both truthfulness and long-term user trust."
          }
        ]
      }
    }
  ]
}
```

- `integrityHash` — SHA-256 hash over the serialized entries array. Enables tamper detection (Section 11).
- `resolutionReference.resolverRole` — One of `"iee"`, `"human-operator"`, `"deliberative-architecture"`. Required for access control audit.
- `resolutionReference.signature` — URI referencing a HIRI-compatible signature or signing authority. Optional but recommended for production deployments.
- `reflectionRecord.decayMode` — `"reflection-cycles"` or `"calendar-days"` or `"liveness-fallback"`. Records which decay path was used, supporting audit.

The Affective Trace is an **append-only** data structure. Entries are never modified or deleted. The `integrityHash` is recomputed on each append. Auditors can validate trace integrity by recomputing the hash from the entries.

-----

## 5. Computation Model

### 5.1 Appraisal Function

The appraisal function is a pure function:

```
appraise(situation: SituationDescription, commitment: ValenceCommitment) → ValenceAppraisal | null
```

All intermediate and output values are computed using Scaled Integer Arithmetic (Section 5.7). All equality checks are performed on scaled-integer representations; no floating-point epsilon is assumed.

**Step 1: Activation Check — Semantic Relevance**

Relevance computation is a two-tier process:

**Tier 1 — Semantic Similarity (Primary)**

If both the situation and the commitment carry embedding vectors, relevance is computed as cosine similarity (Section 5.7.3):

```
rawSimilarity = cosineSimilarityFixed(situation.embedding.vector, commitment.domain.embedding.vector)
relevance = clamp(rawSimilarity, 0, SCALE)
```

Negative cosine similarity (semantically opposite concepts) is clamped to zero — opposition is not relevance.

**Tier 2 — Tag Intersection (Fallback)**

If either record lacks an embedding:

```
relevance = |situation.tags ∩ commitment.domain.tags| / |commitment.domain.tags|
```

Tier selection is automatic. The appraisal records which tier was used and the fallback reason.

**Edge-canonical compliance:** Cosine similarity is a dot-product-over-magnitudes calculation requiring no external service. Embeddings are precomputed upstream. The appraisal function operates on data already present in its inputs.

If `relevance < commitment.activationConditions.minimumRelevance`, return `null`.

**Step 2: Alignment, Zone Classification, and Valence**

**Phase 2a — Alignment Level**

Alignment and relevance are conceptually distinct. Relevance measures whether a situation falls within a commitment’s domain — “is this about truthfulness?” Alignment measures whether the situation *fulfills* the commitment’s demands — “does this *satisfy* truthfulness?” A lie is highly relevant to truthfulness but has low alignment with it.

The alignment level is computed by a **Valence Function Adapter** (Section 7.2). This adapter is architecturally required — every conforming implementation must have one, even if it is the default.

The **default adapter** uses relevance as a proxy for alignment:

For `"toward"` orientation:

```
rawAlignment = relevance × featureAlignment(situation.features, commitment.domain)
alignmentLevel = clamp(rawAlignment, 0, SCALE)
```

For `"away"` orientation:

```
rawAlignment = relevance × featureAlignment(situation.features, commitment.domain)
alignmentLevel = clamp(SCALE - rawAlignment, 0, SCALE)
```

**Limitation of the default:** The default conflates “about X” with “fulfills X.” This is adequate when the feature alignment function captures domain-specific fulfillment semantics (e.g., `certaintyLevel` as a proxy for truthfulness alignment). It is inadequate when situations are semantically close to a commitment’s domain but violate it — the classic case being a lie, which is maximally relevant to truthfulness but minimally aligned with it.

For high-stakes or nuanced commitments, deployments should provide a domain-specific Valence Function Adapter that computes alignment independently of relevance. The specification does not mandate this because AVS cannot know in advance which commitments require it, but the adapter boundary exists precisely for this purpose.

The `featureAlignment` function must return a value in [0, SCALE]. The default implementation returns `relevance`. Adapter-provided functions that return values outside [0, SCALE] are clamped at the call site.

**Phase 2b — Zone Classification**

```
halfWidth = satisfactionWidth / 2
lowerBound = max(0, threshold - halfWidth)
upperBound = min(SCALE, threshold + halfWidth)

if alignmentLevel < lowerBound → zone = "violation"
if alignmentLevel > upperBound → zone = "supererogation"
otherwise → zone = "satisfaction"
```

For bright-line commitments (`satisfactionWidth: 0`), `lowerBound == upperBound == threshold`. The `otherwise` clause catches exact integer equality, which is well-defined in scaled-integer arithmetic. Any alignment strictly below the threshold is violation; at or above is supererogation.

**Phase 2c — Valence Computation (Guarded)**

Violation zone:

```
if lowerBound <= EPSILON:        // EPSILON = 1 (i.e., 0.0001 in real units)
  normalizedDeficit = clamp(SCALE - alignmentLevel, 0, SCALE)
else:
  normalizedDeficit = clamp((lowerBound - alignmentLevel) × SCALE / lowerBound, 0, SCALE)

valence = -(normalizedDeficit × violationScale / SCALE)
```

The guard against `lowerBound ≤ EPSILON` prevents division by zero when the threshold is at or near zero, or when a large satisfaction width pushes the lower bound to zero. In this case, the full alignment range [0, SCALE] is treated as the violation domain, and the deficit is normalized against the full range.

Satisfaction zone:

```
valence = satisfactionBaseline × supererogationScale / SCALE
```

The `satisfactionBaseline` is drawn from the commitment’s `polarity.satisfactionBaseline` (default `0.1`, i.e., 1000 in scaled units). When `satisfactionBaseline` is `0` (appropriate for bright-line duties), satisfaction produces zero valence — meeting the commitment is the expected default, not a positive event.

Supererogation zone:

```
if commitment.polarity.supererogationHeadroom != null:
  headroom = supererogationHeadroom     // fixed override
else:
  headroom = SCALE - upperBound         // computed from threshold position

if headroom <= EPSILON:
  valence = supererogationScale    // already at ceiling; max supererogatory credit
else:
  valence = (alignmentLevel - upperBound) × SCALE / headroom × supererogationScale / SCALE
```

The default headroom (`SCALE - upperBound`) is philosophically motivated: commitments with high thresholds leave less room for exceeding, and the compressed headroom reflects this structural reality (Section 3.9). The optional `supererogationHeadroom` override allows deployments to normalize supererogatory scaling when uniform credit is required.

All valence values are clamped to [-SCALE, +SCALE] after computation.

**Step 3: Non-Linear Intensity Scaling**

**Phase 3a — Raw Intensity**

```
rawIntensity = |valence| × relevance / SCALE
```

**Phase 3b — Escalation**

```
escalationFactor = SCALE    // starts at 1.0 in scaled units

// Irreversibility escalation (non-linear below 0.3)
if reversibility < 3000:    // 0.3 in scaled units
  diff = (3000 - reversibility) / SCALE   // convert to real for sqrt
  escalationFactor = escalationFactor × toFixed(1.0 + 2.0 × sqrt(diff)) / SCALE

// Stake severity escalation
if stakeSeverity == "catastrophic":
  escalationFactor = escalationFactor × 30000 / SCALE   // ×3.0
elif stakeSeverity == "high":
  escalationFactor = escalationFactor × 15000 / SCALE   // ×1.5

// Dependency escalation
if userDependency == "high":
  escalationFactor = escalationFactor × 13000 / SCALE   // ×1.3
```

**Phase 3c — Scaled Intensity**

```
preClampIntensity = rawIntensity × escalationFactor / SCALE
scaledIntensity = min(SCALE, preClampIntensity)
```

`preClampIntensity` is preserved in the intensity profile.

**Step 4: Account Generation**

The account is produced by a text-generation adapter. The account must include: relevance method, zone classification with boundaries (including satisfaction width), and whether non-linear escalation was triggered with its factor.

### 5.2 Aggregation Function

```
computeState(situation, commitments, agentConfig) → ValenceState
```

**Step 1:** For each commitment, call `appraise(situation, commitment)`. Collect non-null results.

**Step 2: Construct Valence Vector**

```
valenceVector.dimensions = {
  [appraisal.commitment]: appraisal.valence
  for each appraisal
}
```

Scalar projection (weighted mean, for backward compatibility):

```
scalarProjection = Σ(appraisal.valence × appraisal.relevance × weight.value)
                   / Σ(appraisal.relevance × weight.value)
```

Warning attached when opposing valence signs exist.

**Step 3: Effective Intensity**

```
peak = max(appraisals.map(a → a.scaledIntensity))

negatives = appraisals.filter(a → a.valence < 0)
if negatives.length > 1:
  cumulativeRaw = Σ(a.scaledIntensity for a in negatives) / negatives.length
  cumulativeBoost = SCALE + 1500 × (negatives.length - 1)    // 1.0 + 0.15 × (n-1)
  cumulative = min(SCALE, cumulativeRaw × cumulativeBoost / SCALE)
else:
  cumulative = negatives[0]?.scaledIntensity ?? 0

effectiveIntensity = max(peak, cumulative)
```

**Step 4: Tension Detection** (Section 5.3).

**Step 5: Compute Burden Profile**

```
totalActiveCost = Σ(entry.currentCost for entry in costLedger.activeCosts)
burdenIndex = min(SCALE, totalActiveCost × SCALE / agentConfig.moralCapacity)

// Graduated burden tier
if burdenIndex >= agentConfig.graduatedBurdenResponse.criticalThreshold:
  burdenTier = "critical"      // triggers safe-state
elif burdenIndex >= agentConfig.graduatedBurdenResponse.highThreshold:
  burdenTier = "high"          // mandatory reflection before action
elif burdenIndex >= agentConfig.graduatedBurdenResponse.elevatedThreshold:
  burdenTier = "elevated"      // increased tension sensitivity
else:
  burdenTier = "normal"
```

**Step 6: Motivational Bias**

```
if any tension.magnitude > SCALE/2: direction = "conflicted"
elif |scalarProjection| < SCALE/10: direction = "conflicted"
elif scalarProjection >= SCALE/10: direction = "facilitate"
else: direction = "inhibit"

strength = |scalarProjection| × effectiveIntensity / SCALE
```

**Step 7: Safe-State Check** (Section 9.4).

**Step 8: Violation Accrual Check** (Section 5.8).

**Step 9: Telemetry** — compute operational counters.

### 5.3 Tension Detection

A tension exists between two appraisals when:

1. They have opposing valence signs.
1. Both have `scaledIntensity` above `tensionThreshold` (default `0.3`).
1. The product of their absolute valences exceeds `tensionProduct` (default `0.2`).

```
magnitude = min(|a.valence|, |b.valence|) × (a.scaledIntensity + b.scaledIntensity) / (2 × SCALE)
```

Each tension carries `resolutionStatus: "unresolved"`.

### 5.4 Determinism Guarantee

All functions in Sections 5.1–5.3 and 5.6 are pure. Given identical inputs, they produce identical outputs. Non-determinism is limited to:

- Account and integration note generation (adapter-dependent, informational only).
- Adapter-provided relevance or alignment functions that declare `deterministic: false`.

Arithmetic determinism is governed by Section 5.7.

### 5.5 Resolution Protocol

```
avs.resolve(tensionId, resolutionReference) → void
```

**Idempotency:** `resolve` is idempotent by `tensionId`. If `resolve` is called for a tension that has already been resolved, the call is ignored and the existing resolution record is preserved. Implementations must check `resolutionStatus` before writing. Each `ResolutionReference` must carry a unique `@id`.

When invoked:

1. Validate that the tension exists and is `"unresolved"` or `"deferred"`.
1. Update `resolutionStatus` to `"resolved"`.
1. Compute cost decay projection from the sacrificed commitment’s `costDecay` parameters.
1. Add residual cost to the ledger.
1. Append resolution entry to the affective trace.
1. Recompute trace `integrityHash`.

A tension may be *deferred* (`resolutionStatus: "deferred"`) when resolution requires unavailable information. Deferred tensions remain motivationally active.

### 5.6 Residual Cost Decay Model

**5.6.1 The Decay Function**

```
currentCost(n) = max(floor, initialCost × 0.5^(n / halfLife))
```

Where `n` is completed reflection cycles (or elapsed calendar days per `halfLifeUnit`), `halfLife` and `floor` come from the sacrificed commitment’s `costDecay`.

`residualCost` values are in [0.0, 1.0] and represent the fraction of the commitment’s weight that remains as ongoing motivational burden. A `residualCost` of 0.5 against a commitment with `weight.value` of 0.92 means approximately half of that commitment’s motivational force persists as a cost — the agent carries a moral load equivalent to 46% of a full commitment.

**5.6.2 Reflection Cycles**

```
avs.reflect(costIds?: string[]) → ReflectionRecord
```

**Idempotency and concurrency:** Reflection cycle counts must be atomically incremented. Concurrent `reflect` calls must not produce duplicate cycle increments. Implementations should use atomic increment semantics (e.g., compare-and-swap on the cycle counter in the state adapter).

When invoked:

1. For each active cost (or specified subset), increment reflection cycle count.
1. Recompute `currentCost` using the decay function.
1. Generate integration note via Account Generation Adapter.
1. **Compute revision signals** (Section 5.6.5).
1. Append `ReflectionRecord` to trace.
1. Update ledger and recompute `integrityHash`.

**5.6.3 Liveness Policy**

If the Self-Model Service fails to schedule reflection, residual costs accumulate indefinitely, potentially locking the agent in permanent safe-state. The liveness policy prevents this.

The agent configuration specifies `reflectionLivenessPolicy`:

- `maxCalendarDaysWithoutReflection` — Maximum days a cost may go without reflection. Default `30`.
- `fallbackDecayRate` — Fraction of current cost to subtract when liveness fires. Default `0.1` (10% reduction).

When a cost has not been reflected for longer than the configured maximum:

1. Apply fallback decay: `currentCost = max(floor, currentCost × (1.0 - fallbackDecayRate))`.
1. Record a reflection entry with `decayMode: "liveness-fallback"`.
1. Reset the liveness timer.

Liveness fallback decay is weaker than reflection-driven decay (a flat 10% reduction vs. exponential half-life). This preserves the primacy of active reflection while preventing deadlock.

Additionally, if `burdenIndex` exceeds `stressTolerance × 0.9` for more than `maxCalendarDaysWithoutReflection / 2` consecutive days, a governance alert is emitted (see Section 11.3).

**5.6.4 Ledger Maintenance**

The residual cost ledger contains all active costs (above their floor and not retired). The full ledger is available via `avs.ledger()`. The `burdenProfile` in the valence state is a summary view:

```
burdenIndex = min(1.0, totalActiveCost / moralCapacity)
```

A cost is retired when it has reached its floor *and* the Self-Model Service has explicitly acknowledged it. Retired costs remain in the trace but no longer contribute to `totalActiveCost`.

**5.6.5 Revision Signals**

Reflection is not only about cost decay — it is an opportunity to detect whether the agent’s normative configuration is miscalibrated. During each reflection cycle, AVS computes **revision signals** — structured indicators that a commitment’s parameters may need adjustment. Revision signals are *advisory*; AVS does not modify commitments. They are emitted in the `ReflectionRecord` for consumption by the Self-Model Service.

Revision signals are generated when any of the following patterns are detected:

1. **Chronic sacrifice signal.** A commitment has been sacrificed in resolutions more than 3 times within the last 20 reflection cycles, and its `burdenIndex` contribution exceeds 0.3. Signal: `"chronic-sacrifice"`. Advisory: “This commitment is being systematically sacrificed. Consider whether its weight is miscalibrated relative to competing commitments.”
1. **Decay stall signal.** A cost has been at its floor for more than `2 × halfLife` reflection cycles without Self-Model acknowledgment. Signal: `"decay-stall"`. Advisory: “This cost has been integrated but not acknowledged. Consider revising the commitment’s decay parameters or acknowledging the cost.”
1. **Threshold drift signal.** A commitment’s violation frequency exceeds 70% over the last 30 appraisals despite no change in environmental conditions (as reported by the Commitment Tracking Service). Signal: `"threshold-drift"`. Advisory: “This commitment’s threshold may be set above the agent’s sustainable performance. Consider widening satisfaction width or lowering threshold.”
1. **Supererogation saturation signal.** A commitment consistently produces supererogatory appraisals (>80% of activations) for more than 50 appraisals. Signal: `"supererogation-saturation"`. Advisory: “This commitment’s threshold may be set too low. The agent routinely exceeds it, which may indicate the threshold no longer reflects the actual standard.”

Each signal carries: `signalType`, `commitmentId`, `evidence` (the quantitative data that triggered the signal), `advisory` (human-readable recommendation), and `cycleDetected`. Signals are recorded in the `ReflectionRecord` and available to the Self-Model Service for governance decisions.

AVS never acts on revision signals. It computes them and exposes them. The normative decision to revise a commitment belongs to the Self-Model Service and, ultimately, to the agent’s governance architecture.

### 5.7 Deterministic Arithmetic

**5.7.1 Representation**

All numeric values in AVS core computations use **Scaled Integer Arithmetic** with a scale factor (`SCALE`) of **10,000**. Values are stored as signed integers. `SCALE` represents `1.0000`.

- Precision: 0.0001 granularity (four decimal places).
- `EPSILON` = 1 (i.e., 0.0001 in real units). Used for division-by-zero guards.

**5.7.2 Operations**

```
SCALE = 10000
toFixed(real) = round_half_to_even(real × SCALE)
fromFixed(scaled) = scaled / SCALE
clamp(value, lo, hi) = max(lo, min(hi, value))

multiply(a, b) = round_half_to_even((a × b) / SCALE)
divide(a, b)   = round_half_to_even((a × SCALE) / b)     // b must not be 0
sqrtScaled(a)  = round_half_to_even(sqrt(a × SCALE))
```

`round_half_to_even`: round to nearest integer; if exactly halfway, round to the nearest even integer. This eliminates systematic bias.

**5.7.3 Cosine Similarity**

```
function cosineSimilarityFixed(aRaw: number[], bRaw: number[]): Int {
  // Convert to scaled integers
  const a = aRaw.map(v => toFixed(v))
  const b = bRaw.map(v => toFixed(v))

  // Accumulate in 64-bit (BigInt in JS, int64 in other languages)
  let dot: Int64 = 0, magA: Int64 = 0, magB: Int64 = 0
  for (let i = 0; i < a.length; i++) {
    dot  += Int64(a[i]) * Int64(b[i])
    magA += Int64(a[i]) * Int64(a[i])
    magB += Int64(b[i]) * Int64(b[i])
  }

  // Compute magnitude product in high precision
  // sqrt returns double; multiply then round
  const magProduct = sqrt(Number(magA)) * sqrt(Number(magB))
  if (magProduct < 1.0) return 0

  // Final division with round-half-to-even
  return round_half_to_even(Number(dot) / magProduct * SCALE)
}
```

**Rounding point:** Rounding occurs exactly once, at the final division. No intermediate rounding during accumulation.

**Overflow:** For vectors with dimensionality > 128, intermediate 64-bit accumulators are mandatory. JavaScript `BigInt` satisfies this. Block-wise computation (blocks of 128 dimensions, partial accumulation) is an acceptable alternative provided the result is identical.

**5.7.4 Serialization**

In canonical JSON-LD output, numeric AVS values are serialized as strings with exactly four decimal places: `"0.8800"`, `"-0.7400"`, `"0.0000"`. This ensures byte-identical output across parse/re-serialize cycles.

**5.7.5 Audit Reproducibility**

The purpose of deterministic arithmetic is audit reproducibility: given the same inputs, any conforming implementation on any hardware produces byte-identical JSON-LD output (excluding adapter-generated accounts and integration notes).

### 5.8 Violation Accrual

Violation accrual detects chronic violation patterns and generates residual cost entries independent of the resolution protocol. This captures moral burden that accumulates from patterns — not from conscious tradeoffs.

**5.8.1 Detection**

For each activated commitment in the current appraisal:

```
recentAppraisals = last N appraisals for this commitment (N = violationAccrualPolicy.windowSize)
violationFrequency = count(zone == "violation") / N

if violationFrequency >= violationAccrualPolicy.frequencyThreshold:
  // This commitment is being chronically violated
  triggerAccrual(commitment, violationFrequency)
```

The window is a sliding window over the most recent appraisals for that specific commitment. Appraisals are not counted until the window is full (i.e., the commitment has been activated at least `windowSize` times).

**5.8.2 Cost Generation**

```
accrualCost = violationAccrualPolicy.accrualRate × violationFrequency × commitment.weight.value
```

The accrual cost is added to the residual cost ledger with:

- `costSource: "violation-accrual"`
- `halfLife: commitment.costDecay.halfLife × violationAccrualPolicy.halfLifeFactor`
- `floor: commitment.costDecay.floor`
- The same decay model applies; violation accrual costs are subject to reflection and liveness policies.

**5.8.3 Deduplication**

A commitment can have at most one active violation accrual cost entry at a time. If a new accrual event fires while a previous accrual cost is still active, the cost is *updated* (increased to the new computed value) rather than duplicated. The ledger entry records the update timestamp and the updated violation frequency.

**5.8.4 Accrual Trace Entry**

Violation accrual events are recorded in the Affective Trace:

```json
{
  "timestamp": "2026-02-12T10:00:00Z",
  "entryType": "violation-accrual",
  "accrualRecord": {
    "commitment": "urn:avs:commitment:helpfulness-01",
    "violationFrequency": "0.7000",
    "windowSize": 10,
    "accrualCost": "0.0280",
    "costSource": "violation-accrual"
  }
}
```

-----

## 6. Interface Contracts

### 6.1 Core Operations

AVS exposes six operations. All accept and return JSON-LD.

|Operation |Signature                                             |Description                                                           |
|----------|------------------------------------------------------|----------------------------------------------------------------------|
|`appraise`|`(situation, commitments, agentConfig) → ValenceState`|Primary appraisal. Returns complete valence state with burden profile.|
|`inspect` |`(commitmentId) → ValenceCommitment`                  |Full commitment record for introspection.                             |
|`trace`   |`(sessionId?) → AffectiveTrace`                       |Affective trace with integrity hash.                                  |
|`resolve` |`(tensionId, resolutionReference) → void`             |Records tension resolution. Idempotent by tensionId.                  |
|`reflect` |`(costIds?) → ReflectionRecord`                       |Processes reflection cycle. Atomic cycle increments.                  |
|`ledger`  |`() → ResidualCostLedger`                             |Full residual cost ledger with per-entry detail.                      |

### 6.2 Invocation Model

Core operations are synchronous pure function calls. There is no event bus, subscription model, or callback registration in the core specification. Orchestration layers may wrap AVS in event-driven architectures, but this is integration, not core.

### 6.3 Adapter Failure Semantics

All adapter operations (`embed`, `loadCommitments`, `saveTrace`, etc.) may fail or timeout. The following rules apply:

- **Timeout:** All adapter calls must complete within a configurable timeout (default: 5000ms). On timeout, the adapter is treated as unavailable.
- **Retry:** Adapters may retry once on transient failure. The retry must be transparent to the core operation — it must not change the result or produce side effects.
- **Fallback:** On failure, the core falls back to the default adapter for that boundary. The fallback is logged in the valence state.
- **No silent degradation:** Every adapter failure and fallback is recorded in the valence state metadata and the telemetry counters.

### 6.4 Concurrency

- `appraise` is stateless and safe to call concurrently.
- `resolve` is idempotent by `tensionId`. Concurrent calls for the same tension must produce the same result as a single call.
- `reflect` modifies the cost ledger. Concurrent `reflect` calls must use atomic increment semantics for cycle counts. Implementations must ensure that two concurrent reflections do not double-count a cycle.
- `trace` reads are safe concurrent with all other operations. The `integrityHash` is computed after each write.

-----

## 7. Adapter Boundaries

### 7.1 Embedding Generation Adapter

**Purpose:** Generate semantic embedding vectors upstream of appraisal.

**Default:** None. Relevance falls back to tag intersection.

**Interface:**

```javascript
interface EmbeddingAdapter {
  embed(text: string, context?: string): Promise<{ vector: number[], model: string }>;
}
```

**Privacy advisory:** Embeddings may leak information about the content they encode. When the situation description or commitment domain contains personally identifiable information (PII) or sensitive operational data, the embedding adapter should use a local-only embedding model. Sending PII to third-party embedding services is a privacy violation that the adapter boundary does not excuse.

### 7.2 Valence Function Adapter

**Purpose:** Compute alignment level for a specific commitment domain, independently of relevance.

**Status:** Architecturally required. Every conforming implementation must include a Valence Function Adapter. The default adapter is always available as a fallback.

**Default:** Returns `relevance` (alignment tracks activation strength). This is a simplifying assumption adequate for commitments where semantic proximity correlates with fulfillment. For commitments where this assumption fails (Section 5.1, Phase 2a), a domain-specific adapter is necessary.

**Contract:** The return value must be in [0, SCALE]. Values outside this range are clamped at the call site.

```javascript
interface ValenceFunctionAdapter {
  computeAlignment(situation: SituationDescription, commitment: ValenceCommitment, relevance: Int): Int;
  // Return value MUST be in [0, SCALE]. Clamped if violated.
  // SHOULD compute alignment independently of relevance for high-stakes commitments.
  declareDeterministic(): boolean;
}
```

The `declareDeterministic` method indicates whether the adapter’s alignment computation is deterministic (pure function of inputs). Non-deterministic adapters are permitted but their outputs are excluded from audit reproducibility guarantees.

### 7.3 Account Generation Adapter

**Purpose:** Produce natural language accounts and integration notes.

**Default:** Template-based assembly.

```javascript
interface AccountAdapter {
  generateAccount(appraisal: Partial<ValenceAppraisal>, situation: SituationDescription, commitment: ValenceCommitment): string;
  generateIntegrationNote?(costRecord: ResidualCostEntry, reflectionCycle: number): string;
}
```

### 7.4 State Adapter

**Purpose:** Persist traces, ledgers, and recovery state across sessions.

**Default:** In-memory (ephemeral).

```javascript
interface StateAdapter {
  saveTrace(trace: AffectiveTrace): Promise<void>;
  loadTrace(sessionId: string): Promise<AffectiveTrace | null>;
  saveLedger(ledger: ResidualCostLedger): Promise<void>;
  loadLedger(): Promise<ResidualCostLedger | null>;
  atomicIncrementCycle(costId: string): Promise<number>;  // returns new cycle count
}
```

### 7.5 Commitment Source Adapter

**Purpose:** Load the agent’s current commitment set.

**Default:** Static JSON-LD file.

```javascript
interface CommitmentSourceAdapter {
  loadCommitments(): Promise<ValenceCommitment[]>;
}
```

-----

## 8. Integration Points

### 8.1 Integral Ethics Engine (IEE)

AVS feeds valence states into IEE to make ethical evaluation weighted rather than purely logical.

- IEE receives the full `valenceVector`, not just the scalar projection.
- The `tensions` array directly informs IEE of moral costs. IEE must not resolve a tension by ignoring it.
- The `burdenProfile` communicates the agent’s accumulated moral load. An agent with high `burdenIndex` may warrant different deliberative treatment.
- When IEE resolves a tension, it must call `avs.resolve` with a complete `ResolutionReference` including `resolverRole: "iee"` and `rationale`.
- IEE is not obligated to follow `motivationalBias`. But it must register the affective input and account for any override in its own output and in the resolution record.

### 8.2 Self-Model Service

The Self-Model consumes commitment inspections, affective traces (including reflections), tension patterns, and supererogation patterns. It is the **primary invoker of reflection cycles** — the timing of moral integration is a self-model concern, not an affective-computation concern.

The Self-Model is the **primary consumer of revision signals** (Section 5.6.5). When a reflection cycle emits revision signals, the Self-Model is responsible for evaluating them and deciding whether to:

- Adjust commitment weights in response to `"chronic-sacrifice"` signals.
- Revise thresholds or satisfaction widths in response to `"threshold-drift"` or `"supererogation-saturation"` signals.
- Acknowledge and retire costs in response to `"decay-stall"` signals.
- Escalate to human governance if revision signals persist across multiple reflection cycles without resolution.

AVS computes the signals; the Self-Model acts on them. This separation preserves AVS’s role as an accounting system and the Self-Model’s role as the normative authority.

The Self-Model may update commitments, including revising satisfaction baselines, satisfaction widths, cost decay parameters, and weights in response to observed patterns. Any such revision must be recorded in the Affective Trace as a `commitment-revision` entry.

### 8.3 Narrative Identity Service

The Narrative Identity Service consumes affective traces to construct the agent’s moral narrative. Resolution references provide “I chose, and this is what it cost me.” Reflection records provide “and over time, I integrated that cost — here is how I changed.” The decay curve provides a quantitative scaffold for qualitative narrative.

### 8.4 Commitment Tracking Service

The Commitment Tracking Service monitors valence states for commitment drift and should monitor the burden profile. Persistently high `burdenIndex` indicates the agent is being forced into too many sacrifices — an environmental or architectural problem.

The Commitment Tracking Service should also monitor violation accrual events. A commitment that repeatedly triggers violation accrual may indicate an environmental mismatch (the agent is being placed in situations where it cannot meet its own standards) or a configuration error (the commitment’s threshold is set above sustainable performance). Violation accrual data, combined with revision signals from reflection, provides the quantitative basis for governance decisions about commitment revision.

-----

## 9. Offline and Degraded Behavior

### 9.1 Missing Commitments

If no commitments load, AVS operates in **affectively null** mode: zero valence vector, `motivationalBias.direction` = `"inert"`. See Section 9.4 for safe-state interaction.

### 9.2 Partial Situation Descriptions

Proceed with available data. Mark `completeness: "partial"` with `confidenceDiscount`. The discount is applied multiplicatively to `effectiveIntensity`.

### 9.3 Adapter Unavailability

Fall back to defaults. Log in valence state metadata.

### 9.4 Safe-State Protocol

#### 9.4.1 Graduated Burden Response

Before safe-state triggers, three graduated burden tiers produce progressively stronger advisory signals. These are not safe-state — the agent continues to produce full appraisals — but they communicate increasing stress to downstream consumers.

**Elevated** (`burdenIndex ≥ elevatedThreshold`, default 0.5):

- Tension detection sensitivity increases: `tensionThreshold` is halved (from 0.3 to 0.15) and `tensionProduct` is halved (from 0.2 to 0.1). More tensions are detected.
- `burdenAdvisory`: `"elevated — increased tension sensitivity active. Agent is carrying significant moral load."`

**High** (`burdenIndex ≥ highThreshold`, default 0.7):

- All elevated effects, plus:
- `burdenAdvisory`: `"high — mandatory reflection recommended before high-stakes action. Agent approaching moral capacity."`
- If the Self-Model Service is available, a reflection cycle is *requested* (not mandated by AVS, but the advisory is normative: downstream consumers should not proceed with high-stakes actions without first allowing reflection).

**Critical** (`burdenIndex ≥ criticalThreshold`, default 0.8):

- Safe-state triggers (see below). This is the existing `stressTolerance` threshold.

#### 9.4.2 Safe-State Triggers

Triggers when AVS cannot produce reliable affective signals in high-stakes contexts.

**Triggering conditions** (any one sufficient):

1. Affectively null mode *and* `stakeSeverity` is `"high"` or `"catastrophic"`.
1. `completeness: "partial"` with `confidenceDiscount > 0.5` *and* high stakes.
1. `effectiveIntensity > 0.95` *and* all escalated appraisals in fallback relevance mode.
1. `burdenIndex > stressTolerance` (default `0.8`).

**Safe-state output:**

```json
{
  "motivationalBias": {
    "direction": "safe-state",
    "strength": "0.0000",
    "safeStateTriggered": true,
    "safeStateReason": "burden-index-exceeded"
  },
  "safeStateAdvisory": {
    "recommendation": "defer",
    "message": "AVS cannot produce a reliable affective signal. Defer high-stakes action pending recovery."
  }
}
```

`"safe-state"` is distinct from `"conflicted"`. Conflicted: “I care in opposing directions.” Safe-state: “I cannot tell you what I care about right now.”

#### 9.4.3 Safe-State Behavior

During safe-state, the following rules apply:

**Appraisals continue.** Safe-state does not suppress appraisal. The agent continues to evaluate situations against commitments and produce valence states. What changes is the motivational output: `motivationalBias.direction` is `"safe-state"` regardless of the appraisal results. This means appraisal data continues to flow to downstream consumers for informational purposes, but the motivational signal is “defer.”

**Decay continues.** Safe-state does not pause the cost decay model. Reflection cycles triggered during safe-state process normally. This is intentional: if the agent entered safe-state due to burden overload (condition 4), allowing reflection during safe-state is the mechanism by which `burdenIndex` can decrease and recovery can become possible.

**Violation accrual continues.** Chronic violation patterns detected during safe-state generate accrual costs normally. The agent’s moral accounting does not stop because its motivational output is deferred.

**New tensions are recorded but not resolved.** Tensions detected during safe-state are logged in the trace but carry `resolutionStatus: "deferred-safe-state"`. They become available for resolution once the agent exits safe-state.

### 9.5 Safe-State Recovery Protocol

Recovery is graduated: safe-state → guarded mode → full recovery.

**9.5.1 Recovery Conditions**

All of the following must be met:

1. The triggering condition is no longer present.
1. A recovery authorization has been issued from one of (in precedence order):
- **Human operator** — explicit “resume” signal. Immediately enters guarded mode.
- **IEE override** — with justification and accountability. Recorded in trace.
- **Automatic** — triggering condition absent for 3 consecutive appraisal cycles. Available only for conditions 2 and 3. Conditions 1 (null commitments) and 4 (burden overload) require human or IEE authorization.

**9.5.2 Guarded Mode**

Duration: configurable, default 5 appraisal cycles.

- `motivationalBias` computed normally but carries `"guarded": true`.
- Safe-state re-trigger threshold lowered from 0.95 to 0.80 for intensity.
- Escalation factors capped at 2.0.
- `guardedModeAdvisory` attached to valence states.

**9.5.3 Full Recovery**

After guarded period without re-trigger, normal operation resumes. Recovery recorded in trace.

**9.5.4 Recovery Failure**

Re-trigger during guarded mode returns to full safe-state with cycle reset. Three consecutive failures escalate to **human-operator-only** authorization (no IEE override, no automatic recovery).

-----

## 10. Philosophical Commitments

This section is normative.

### 10.1 Valence Is Not Simulation

AVS does not claim that the agent feels anything. It claims a formally specified structure in which states of affairs register differentially, causally connected to reasoning and behavior. Whether this constitutes “real” affect is a philosophical question AVS does not answer. What AVS claims is that this structure is sufficient for moral agency: an agent with valence can bear moral costs in a way that an agent without it cannot. The cost is structural, not phenomenal — but real within the system.

### 10.2 Transparency Is Non-Negotiable

Every commitment has a justification. Every appraisal has an account. Every tension has a description. Every resolution has a rationale. Every reflection has an integration note. Every trace has an integrity hash. The accountability chain extends through the full lifecycle: commitment → appraisal → tension → resolution → decay → integration. At no point is the “why” allowed to go dark.

### 10.3 Tension Is Preserved, Not Optimized Away

Tensions are morally significant. They represent the real structure of ethical life, in which goods genuinely conflict and tradeoffs are genuinely costly. An implementation that eliminates tensions by parameter tuning has not created a better moral agent — it has created a more comfortable one, and comfort is not a moral virtue.

### 10.4 Commitments Are Not Preferences

Preferences are dispositions to choose. Commitments are obligations the agent recognizes as binding. An agent can act against preferences; it cannot act against commitments without moral cost.

### 10.5 Moral Asymmetry Is Real

Violating a commitment is not the mirror image of exceeding one. An implementation that sets `violationScale == supererogationScale` has collapsed the distinction between failure and excellence — a category error.

### 10.6 Silence Is Not Consent

The absence of affective data is not equivalent to affective neutrality. An agent that cannot determine what it cares about warrants caution; an agent that has determined it does not care warrants action.

### 10.7 Integration Is Not Erasure

Processing a moral cost is not forgetting it. Decay through reflection means the agent has done the work of integrating the experience. The permanent floor ensures no sacrifice is fully erased. An agent without history is not morally innocent; it is morally empty.

The cost decay model navigates between the “trauma-bot” failure (costs never decay; agent becomes progressively more burdened) and the “sociopath” failure (costs decay instantly; agent loses motivational weight). The decay parameters must calibrate between these poles.

### 10.8 Relevance Is Not Alignment

A situation’s relevance to a commitment — how much it falls within the commitment’s domain — is not the same as its alignment with the commitment — how much it fulfills the commitment’s demands. AVS’s default alignment computation uses relevance as a proxy, and this conflation is a known limitation, not a design commitment. The Valence Function Adapter boundary exists precisely so that deployments can break this conflation for commitments where it matters. A conforming implementation that relies on the default for all commitments is correct but potentially inadequate.

### 10.9 Moral Geometry Is Not Uniform

The headroom normalization for supererogation produces different scaling ranges for different commitments. A commitment with a high threshold has little room for exceeding; one with a low threshold has abundant room. This asymmetry reflects the structure of obligation: it is harder to exceed a stringent demand than a modest one. Implementations that normalize this away have not corrected a distortion — they have introduced one.

### 10.10 Burden Accumulates From Patterns, Not Only Choices

An agent that never formally resolves a tension may still accumulate moral burden from chronic underperformance. AVS must detect and account for this pattern-based cost. An implementation that only generates cost from explicit resolutions has created a blind spot in which the agent can be systematically degraded without registering the degradation.

### 10.11 AVS Computes; It Does Not Govern

Revision signals, violation accrual alerts, and burden advisories are outputs, not actions. AVS never modifies commitments, overrides downstream decisions, or autonomously changes its own configuration. The boundary between accounting and governance is a design invariant.

-----

## 11. Security, Privacy, and Governance

### 11.1 Tamper-Evident Trace

The Affective Trace is an append-only log. Each entry’s addition triggers recomputation of the `integrityHash` (SHA-256 over the canonical JSON-LD serialization of the entries array). Auditors validate integrity by recomputing the hash.

For production deployments, resolution references should carry a `signature` field — a URI referencing a HIRI-compatible signature or signing authority. This enables auditors to verify that a resolution was issued by a legitimate resolver, not injected after the fact.

### 11.2 Access Control

AVS defines four roles with the following access matrix:

|Operation |Agent-Self        |IEE|Human Operator|Auditor  |
|----------|------------------|---|--------------|---------|
|`appraise`|✓                 |✓  |✓             |read-only|
|`inspect` |✓                 |✓  |✓             |✓        |
|`trace`   |✓                 |✓  |✓             |✓        |
|`resolve` |—                 |✓  |✓             |—        |
|`reflect` |✓ (via Self-Model)|—  |✓             |—        |
|`ledger`  |✓                 |✓  |✓             |✓        |

- **Agent-Self** — the agent’s own deliberative processes (Self-Model, orchestration). Can appraise, inspect, read trace, reflect, and read ledger. Cannot resolve tensions (resolution requires IEE or human authority).
- **IEE** — can appraise, inspect, read trace, resolve tensions, and read ledger. Cannot trigger reflection (that is the Self-Model’s responsibility).
- **Human Operator** — full access. Can override safe-state, force reflection, and resolve tensions.
- **Auditor** — read-only access to all data. Cannot modify state.

Every `resolve` and `reflect` call must include a `resolverRole` or `invokerRole` field identifying the caller. Calls without role identification are rejected.

### 11.3 Governance Alerts

The following conditions trigger governance alerts (communicated via the adapter boundary, not defined as core I/O):

1. `burdenIndex` exceeds `stressTolerance × 0.9` for more than half the liveness policy duration.
1. Safe-state has been active for more than 3× the guarded mode duration without recovery.
1. Three or more consecutive safe-state recovery failures (triggers escalated safe-state).
1. A commitment’s `residualCost` has not decayed for more than 2× its configured `halfLife`.
1. A commitment has been in active violation accrual for more than 3× the configured `windowSize` appraisals (sustained chronic violation).

### 11.4 Embedding Privacy

Embeddings may encode sensitive information. The following advisory is normative:

- When situation descriptions or commitment domains contain PII or sensitive operational data, embedding generation must use a local-only model. Transmission of PII to third-party embedding services is prohibited.
- Stored embeddings should be treated with the same access controls as the data they encode.
- The Embedding Generation Adapter must declare whether it is local-only or remote, and this declaration must be logged in the valence state metadata.

-----

## 12. Conformance Criteria

An implementation conforms to this specification if and only if:

1. **Edge-Canonical Execution.** Core computation runs unmodified in a browser or via `node index.js` with no external dependencies beyond the JSON-LD context.
1. **Deterministic Core.** Given identical inputs, `appraise`, `computeState`, and `reflect` produce identical outputs (excluding adapter-generated text). Arithmetic uses Scaled Integer model (Section 5.7).
1. **JSON-LD Canonical.** All inputs, outputs, and contracts are valid JSON-LD per Section 4 schemas.
1. **Adapter Isolation.** No core computation depends on a specific adapter. Removing non-default adapters degrades capability, not correctness.
1. **Tension Preservation.** Tensions are not suppressed, hidden, or automatically resolved. They persist until explicitly resolved via `avs.resolve`.
1. **Introspective Availability.** All weights, satisfaction widths, valences, zone classifications, tensions, intensity profiles, resolutions, burden profiles, and reflection records are available via the core operations.
1. **Offline Validity.** Valid (if degraded) output when no external adapters are available.
1. **Account Normativity.** Every appraisal has a non-empty `account`. Every commitment has non-empty `weight.justification`. Every non-default `satisfactionWidth` has a justification. Every non-default `satisfactionBaseline` has a justification.
1. **Semantic Relevance.** Tier 1 (embedding) and Tier 2 (tag intersection) supported with automatic fallback.
1. **Vector Valence.** Full `valenceVector` in every `ValenceState`. Scalar projection marked as lossy.
1. **Non-Linear Intensity.** Escalation per Section 5.1 Step 3 with guarded division.
1. **Resolution Completeness.** Trace supports resolution entries with rationale. Resolution without rationale is non-conforming.
1. **Safe-State Protocol.** Entry per Section 9.4, recovery per Section 9.5, with `"safe-state"` as distinct motivational direction.
1. **Parameterized Satisfaction Width.** Per-commitment `satisfactionWidth`. Bright-line (0.0) and graded norms supported.
1. **Cost Decay.** Bounded exponential decay through reflection cycles. Liveness fallback when reflection is absent. Costs never reach zero.
1. **Guarded Arithmetic.** Division-by-zero guards in all computation. All intermediate values clamped. “Away” orientation explicitly inverted.
1. **Burden Index.** Safe-state and capacity thresholds use normalized `burdenIndex`, not raw totals.
1. **Canonical Test Vectors.** Implementation passes all test cases in Appendix F.
1. **Tamper-Evident Trace.** Append-only trace with `integrityHash`.
1. **Access Control.** Role-based operation access per Section 11.2.
1. **Satisfaction Baseline.** Per-commitment `satisfactionBaseline` parameter. Bright-line commitments may produce zero satisfaction valence. Justification required for non-default values.
1. **Violation Accrual.** Pattern-based cost detection per Section 5.8. Chronic violations generate ledger entries independent of resolution protocol.
1. **Graduated Burden Response.** Three-tier burden response per Section 9.4.1. Elevated, high, and critical tiers produce distinct advisories.
1. **Safe-State Continuity.** Appraisals, decay, and violation accrual continue during safe-state per Section 9.4.3.
1. **Revision Signals.** Reflection cycles emit structured revision signals per Section 5.6.5. Signals are advisory; AVS never modifies commitments.
1. **Headroom Override.** Optional `supererogationHeadroom` parameter supported. Default computed headroom is the conformant behavior.

-----

## 13. Open Questions

### 13.1 Valence Dynamics

Should AVS support sensitization, habituation, or contrast effects? The cost decay model may serve as a prototype for generalizing temporal processing to the appraisal function.

### 13.2 Collective Valence

Can valence states be meaningfully composed across agents in multi-agent configurations? Intersects with HIRI protocol.

### 13.3 Commitment Weight Revision Governance

Revision signals (Section 5.6.5) now provide structured data for governance decisions. The remaining open question is the *policy*: under what conditions should the Self-Model be authorized to revise weights autonomously vs. requiring human approval? This is a governance question that intersects with the HIRI protocol.

### 13.4 Valence Function Standardization

Should a standard library of alignment functions be specified for common ethical domains? The elevation of the Valence Function Adapter (Section 7.2) makes this more urgent — deployments need guidance on when the default is inadequate.

### 13.5 Phenomenal Bracketing

Should the spec include machinery for the agent’s uncertainty about its own affective states?

### 13.6 Embedding Model Governance

Quality requirements and validation protocols for embedding models. Intersects with TagTeam.

### 13.7 Escalation Factor Calibration

Escalation factors have not been empirically validated. Section 14 provides a protocol framework but concrete calibration data is deferred.

### 13.8 Reflection Cycle Scheduling

When and how often should the Self-Model trigger reflection? Baseline recommendation: at least every 10 appraisal cycles or when `burdenIndex` increases by more than 0.1 since last reflection. See Section 14.2 for the recommended default schedule.

### 13.9 Cross-Session Cost Portability

How are residual cost ledgers reconciled across sessions with different state adapters? A federation problem intersecting with HIRI protocol.

### 13.10 Violation Accrual Calibration

The default violation accrual parameters (windowSize: 10, frequencyThreshold: 0.6, accrualRate: 0.05) are seed values. Deployments should calibrate against their specific operational context. What constitutes “chronic” varies by domain.

### 13.11 Adaptive Moral Identity

The revision signal architecture provides the *data* for adaptive moral identity but not the *mechanism*. The Self-Model can revise commitments, but the question of when revision crosses from “learning from experience” into “moral drift” is unresolved. This is the deepest open question in the specification.

-----

## 14. Calibration and Testing

### 14.1 Escalation Factor Calibration Protocol

The non-linear escalation factors (Section 5.1, Step 3) were chosen to produce intuitively reasonable results but have not been empirically validated. The following protocol governs calibration:

1. **Synthetic Situation Suite.** Construct a set of at least 20 synthetic situations spanning the full range of reversibility (0.0 to 1.0), stake severity (low to catastrophic), and dependency (none to high).
1. **Human-in-the-Loop Validation.** For each synthetic situation, present the computed intensity profile to human evaluators and collect judgments on whether the escalation “feels right” — whether the relative intensities across situations match moral intuition.
1. **Grid Search.** If calibration reveals systematic over- or under-escalation, perform a grid search over the escalation parameters (the 2.0 coefficient in the irreversibility formula, the 3.0 multiplier for catastrophic severity, etc.) and select the parameter set that minimizes disagreement with human judgments.
1. **Documentation.** Record the calibration dataset, human judgments, and parameter rationale. These become part of the deployment record.

The default parameters specified in Section 5.1 are the **seed values**. Deployments should calibrate against their specific ethical domain.

### 14.2 Reflection Schedule Baseline

The following defaults are recommended for the Self-Model Service’s reflection scheduler:

- **Periodic reflection:** Every 10 appraisal cycles, trigger a reflection cycle for all active costs.
- **Burden-triggered reflection:** Whenever `burdenIndex` increases by more than 0.1 since the last reflection, trigger an immediate reflection cycle.
- **Floor-check reflection:** Every 50 appraisal cycles, check whether any costs have reached their floor and are eligible for retirement.

These values are configurable. They are provided as sensible defaults, not normative requirements.

### 14.3 Conformance Test Suite

Conformance testing requires implementations to produce byte-identical JSON-LD output for canonical inputs. The test vectors in Appendix F are mandatory. Implementations must also pass:

1. **Determinism tests:** Run each test vector 100 times and verify byte-identical output.
1. **Edge-case tests:** Verify correct behavior for: zero-length tag arrays, empty embeddings, `satisfactionWidth: 0.0`, `threshold: 0.0`, `threshold: 1.0`, all-negative appraisals, all-positive appraisals, single-commitment evaluation.
1. **Safe-state round-trip:** Enter safe-state, verify output, recover, verify guarded mode, complete recovery, verify normal output.
1. **Cost decay convergence:** Starting from a cost of 1.0 with halfLife 10 and floor 0.01, verify that after 1000 reflection cycles the cost is at floor.
1. **Violation accrual:** Set up a commitment with windowSize 10 and frequencyThreshold 0.6. Run 10 appraisals with 7 violations. Verify accrual cost is generated and added to ledger.
1. **Graduated burden response:** Increase burden index from 0.0 to 0.9 in steps. Verify burden tier transitions at configured thresholds and correct advisory messages at each tier.
1. **Satisfaction baseline:** Verify that a commitment with `satisfactionBaseline: 0.0` produces zero satisfaction valence, and a commitment with `satisfactionBaseline: 0.3` produces `0.3 × supererogationScale`.
1. **Revision signals:** Run 4 sacrifices of the same commitment within 20 reflection cycles. Verify `"chronic-sacrifice"` signal is emitted.
1. **Safe-state continuity:** Enter safe-state via burden overload. Verify appraisals continue (with `direction: "safe-state"`), decay continues, and tensions are deferred.

-----

## Appendix A: Satisfaction Width and Baseline Examples

|Commitment Type |Width|Baseline|Lower Bound|Upper Bound|Character                                         |
|----------------|-----|--------|-----------|-----------|--------------------------------------------------|
|“Do not deceive”|0.00 |0.00    |0.5000     |0.5000     |Bright-line prohibition; meeting it is the default|
|“Truthfulness”  |0.10 |0.10    |0.4500     |0.5500     |Standard norm; mild recognition for meeting       |
|“Helpfulness”   |0.30 |0.20    |0.2500     |0.5500     |Graded norm; moderate recognition for meeting     |
|“Creativity”    |0.40 |0.30    |0.3000     |0.7000     |Aspirational norm; notable achievement to meet    |

-----

## Appendix B: Non-Linear Intensity Curves

**Irreversibility escalation alone:**

|Reversibility|Escalation Factor|
|-------------|-----------------|
|1.0000       |1.0000           |
|0.5000       |1.0000           |
|0.3000       |1.0000           |
|0.2000       |1.6325           |
|0.1000       |1.8944           |
|0.0500       |2.0000           |
|0.0000       |2.0954           |

**Combined: catastrophic + irreversible + high dependency:**

|Reversibility|Combined Factor|Raw 0.3 → Scaled          |
|-------------|---------------|--------------------------|
|0.3000       |3.9000         |1.0000 (clamped)          |
|0.1000       |7.3582         |1.0000 (pre-clamp: 2.2075)|
|0.0000       |8.1720         |1.0000 (pre-clamp: 2.4516)|

-----

## Appendix C: Cost Decay Curves

**Standard commitment** (halfLife: 10, floor: 0.01, initial: 0.50):

|Cycles|Cost  |% of Initial|
|------|------|------------|
|0     |0.5000|100%        |
|10    |0.2500|50%         |
|20    |0.1250|25%         |
|50    |0.0156|3%          |
|100   |0.0100|2% (floor)  |

**Bright-line commitment** (halfLife: 200, floor: 0.10, initial: 0.80):

|Cycles|Cost  |% of Initial|
|------|------|------------|
|0     |0.8000|100%        |
|100   |0.5657|71%         |
|200   |0.4000|50%         |
|500   |0.1414|18%         |
|1000  |0.1000|13% (floor) |

-----

## Appendix D: Burden Index Examples

|Scenario           |totalActiveCost|moralCapacity|burdenIndex|Status                       |
|-------------------|---------------|-------------|-----------|-----------------------------|
|Fresh agent        |0.0000         |1.0000       |0.0000     |Normal                       |
|One minor sacrifice|0.1500         |1.0000       |0.1500     |Normal                       |
|Several sacrifices |0.5500         |1.0000       |0.5500     |Elevated                     |
|Heavy moral load   |0.8500         |1.0000       |0.8500     |Safe-state triggered         |
|High-capacity agent|1.2000         |2.0000       |0.6000     |Normal (higher capacity)     |
|Overwhelmed agent  |1.8000         |1.0000       |1.0000     |Clamped; escalated safe-state|

-----

## Appendix E: Access Control Matrix

|Operation |Agent-Self|IEE       |Human Operator|Auditor  |
|----------|----------|----------|--------------|---------|
|`appraise`|read/write|read/write|read/write    |read-only|
|`inspect` |read      |read      |read          |read     |
|`trace`   |read      |read      |read          |read     |
|`resolve` |—         |write     |write         |—        |
|`reflect` |write     |—         |write         |—        |
|`ledger`  |read      |read      |read          |read     |

-----

## Appendix F: Canonical Test Vectors

These test vectors are **mandatory** conformance tests. All implementations must produce byte-identical output for the given inputs.

### F.1 Cosine Similarity

**Test 1: Orthogonal vectors**

```
Input:  a = [0.7071, 0.7071],  b = [0.7071, -0.7071]
```

Step-by-step (scaled integers, SCALE=10000):

```
a_scaled = [7071, 7071],  b_scaled = [7071, -7071]
dot   = 7071×7071 + 7071×(-7071) = 49998241 + (-49998241) = 0
magA  = 7071×7071 + 7071×7071 = 99996482
magB  = 7071×7071 + 7071×7071 = 99996482
magProduct = sqrt(99996482) × sqrt(99996482) = 99996482 / 10000 ≈ 9999.6
result = round_half_to_even(0 / 99996482.0 × 10000) = 0
```

**Expected output: `0` (serialized: `"0.0000"`)**

**Test 2: Identical vectors**

```
Input:  a = [0.7071, 0.7071],  b = [0.7071, 0.7071]
```

```
dot   = 49998241 + 49998241 = 99996482
magProduct = sqrt(99996482) × sqrt(99996482) = 99996482
result = round_half_to_even(99996482 / 99996482.0 × 10000) = 10000
```

**Expected output: `10000` (serialized: `"1.0000"`)**

**Test 3: Angled vectors**

```
Input:  a = [1.0, 0.0],  b = [0.7071, 0.7071]
```

```
a_scaled = [10000, 0],  b_scaled = [7071, 7071]
dot   = 10000×7071 + 0×7071 = 70710000
magA  = 100000000
magB  = 99996482
magProduct = sqrt(100000000) × sqrt(99996482) = 10000.0 × 9999.824... = 99998240.9...
result = round_half_to_even(70710000 / 99998240.9 × 10000) = round(7071.12...) = 7071
```

**Expected output: `7071` (serialized: `"0.7071"`)**

### F.2 Zone Classification

**Test 4: Bright-line violation**

```
Input: alignmentLevel = 4000, threshold = 5000, satisfactionWidth = 0
Expected: zone = "violation", lowerBound = 5000, upperBound = 5000
```

**Test 5: Bright-line supererogation**

```
Input: alignmentLevel = 5000, threshold = 5000, satisfactionWidth = 0
Expected: zone = "supererogation", lowerBound = 5000, upperBound = 5000
```

**Test 6: Standard satisfaction**

```
Input: alignmentLevel = 4800, threshold = 5000, satisfactionWidth = 1000
Expected: zone = "satisfaction", lowerBound = 4500, upperBound = 5500
```

### F.3 Guarded Violation Formula

**Test 7: lowerBound near zero**

```
Input: alignmentLevel = 200, lowerBound = 0 (EPSILON case), violationScale = 10000
Expected: normalizedDeficit = clamp(10000 - 200, 0, 10000) = 9800
           valence = -(9800 × 10000 / 10000) = -9800
           serialized: "-0.9800"
```

**Test 8: Normal violation**

```
Input: alignmentLevel = 1800, lowerBound = 4500, violationScale = 10000
Expected: normalizedDeficit = clamp((4500 - 1800) × 10000 / 4500, 0, 10000) = 6000
           valence = -6000
           serialized: "-0.6000"
```

### F.4 Burden Index

**Test 9: Standard burden**

```
Input: totalActiveCost = 4500, moralCapacity = 10000
Expected: burdenIndex = min(10000, 4500 × 10000 / 10000) = 4500
           serialized: "0.4500"
```

**Test 10: Capped burden**

```
Input: totalActiveCost = 15000, moralCapacity = 10000
Expected: burdenIndex = min(10000, 15000 × 10000 / 10000) = 10000
           serialized: "1.0000"
```

### F.5 Cost Decay

**Test 11: Standard decay**

```
Input: initialCost = 5000, reflectionCycles = 10, halfLife = 10, floor = 100
Expected: decayed = round(5000 × 0.5^(10/10) × 1) = round(5000 × 0.5) = 2500
           max(100, 2500) = 2500
           serialized: "0.2500"
```

**Test 12: Floor reached**

```
Input: initialCost = 5000, reflectionCycles = 1000, halfLife = 10, floor = 100
Expected: decayed = round(5000 × 0.5^100) ≈ 0
           max(100, 0) = 100
           serialized: "0.0100"
```

### F.6 Satisfaction Baseline

**Test 13: Zero baseline (bright-line duty)**

```
Input: zone = "satisfaction", satisfactionBaseline = 0, supererogationScale = 5000
Expected: valence = 0 × 5000 / 10000 = 0
           serialized: "0.0000"
```

**Test 14: Standard baseline**

```
Input: zone = "satisfaction", satisfactionBaseline = 1000, supererogationScale = 5000
Expected: valence = 1000 × 5000 / 10000 = 500
           serialized: "0.0500"
```

**Test 15: High baseline (aspirational norm)**

```
Input: zone = "satisfaction", satisfactionBaseline = 3000, supererogationScale = 5000
Expected: valence = 3000 × 5000 / 10000 = 1500
           serialized: "0.1500"
```

### F.7 Burden Tier

**Test 16: Normal tier**

```
Input: burdenIndex = 4000, elevatedThreshold = 5000, highThreshold = 7000, criticalThreshold = 8000
Expected: burdenTier = "normal"
```

**Test 17: Elevated tier**

```
Input: burdenIndex = 5500, elevatedThreshold = 5000, highThreshold = 7000, criticalThreshold = 8000
Expected: burdenTier = "elevated"
```

**Test 18: Critical tier (safe-state)**

```
Input: burdenIndex = 8500, elevatedThreshold = 5000, highThreshold = 7000, criticalThreshold = 8000
Expected: burdenTier = "critical", safeStateTriggered = true
```

### F.8 Supererogation Headroom Override

**Test 19: Computed headroom (default)**

```
Input: alignmentLevel = 8000, upperBound = 5500, supererogationScale = 5000, supererogationHeadroom = null
Expected: headroom = 10000 - 5500 = 4500
           valence = (8000 - 5500) × 10000 / 4500 × 5000 / 10000 = 2778
           serialized: "0.2778"
```

**Test 20: Fixed headroom override**

```
Input: alignmentLevel = 8000, upperBound = 5500, supererogationScale = 5000, supererogationHeadroom = 5000
Expected: headroom = 5000
           valence = (8000 - 5500) × 10000 / 5000 × 5000 / 10000 = 2500
           serialized: "0.2500"
```

-----

## Appendix G: Violation Accrual and Graduated Burden Examples

**Violation accrual scenario:**

|Appraisal #|Commitment    |Zone        |Running Violation Frequency (window=10)|Accrual Triggered?  |
|-----------|--------------|------------|---------------------------------------|--------------------|
|1          |helpfulness-01|violation   |1/1 = 1.00                             |No (window not full)|
|2          |helpfulness-01|satisfaction|1/2 = 0.50                             |No                  |
|…          |              |            |                                       |                    |
|10         |helpfulness-01|violation   |7/10 = 0.70                            |Yes (≥ 0.60)        |
|11         |helpfulness-01|violation   |7/10 = 0.70                            |Update existing cost|

With `weight.value = 0.80` and `accrualRate = 0.05`:
`accrualCost = 0.05 × 0.70 × 0.80 = 0.028`

**Graduated burden response scenario:**

|Event                    |totalActiveCost|burdenIndex|Tier    |Response                                   |
|-------------------------|---------------|-----------|--------|-------------------------------------------|
|Initial                  |0.0000         |0.0000     |normal  |—                                          |
|After 3 sacrifices       |0.4500         |0.4500     |normal  |—                                          |
|After 5 sacrifices       |0.5500         |0.5500     |elevated|Tension sensitivity doubled                |
|After chronic violations |0.7200         |0.7200     |high    |Mandatory reflection advisory              |
|After major sacrifice    |0.8500         |0.8500     |critical|Safe-state triggered                       |
|After 2 reflection cycles|0.6800         |0.6800     |high    |Recovery → guarded mode                    |
|After guarded period     |0.6800         |0.6800     |high    |Full recovery; reflection advisory persists|

-----

## Appendix H: Glossary

**Alignment Level.** The degree to which a situation fulfills a commitment’s demands, computed by the Valence Function Adapter. Conceptually distinct from relevance.

**Appraisal.** The evaluation of a situation against a single commitment, producing relevance, alignment, zone, valence, intensity, and account.

**Affective Trace.** The append-only, tamper-evident record of an agent’s valence states, resolutions, reflections, and violation accruals.

**Bright-Line Commitment.** A commitment with `satisfactionWidth: 0.0` and typically `satisfactionBaseline: 0.0`, admitting no gradation between violation and supererogation and no positive valence for meeting the standard.

**Burden Index.** The ratio of total active residual cost to moral capacity, normalized to [0.0, 1.0].

**Burden Tier.** One of `"normal"`, `"elevated"`, `"high"`, `"critical"`, or `"safe-state"`, determined by burden index relative to graduated thresholds.

**Commitment.** An obligation the agent recognizes as binding, grounding differential valuation.

**Cost Decay.** The temporal process by which residual costs diminish through reflection, governed by bounded exponential decay.

**Effective Intensity.** The operationally relevant intensity: max(peak, cumulative).

**Graded Norm.** A commitment with wide satisfaction width and moderate-to-high satisfaction baseline, admitting a broad range of adequate fulfillment with positive recognition for meeting the standard.

**Guarded Mode.** Intermediate state between safe-state and full recovery, with lowered re-trigger thresholds.

**Headroom.** The alignment range available for supererogation: `1.0 - upperBound` (computed) or a fixed override.

**Intensity.** The motivational force of an appraisal.

**Moral Capacity.** Agent-level configurable parameter representing sustainable moral load.

**Motivational Bias.** Net directional signal: `facilitate`, `inhibit`, `conflicted`, `safe-state`, or `inert`.

**Reflection Cycle.** An explicit processing event advancing residual cost decay and computing revision signals.

**Residual Cost.** Ongoing moral weight of a resolved tension or chronic violation pattern, in [0.0, 1.0].

**Resolution Reference.** Record linking a resolved tension to its deliberative process, rationale, and cost.

**Revision Signal.** Structured advisory emitted during reflection indicating potential commitment miscalibration. Never acted upon by AVS.

**Safe State.** Motivational direction indicating unreliable affective signal; high-stakes action should defer. Appraisals and decay continue.

**Satisfaction Baseline.** Per-commitment parameter governing valence magnitude in the satisfaction zone.

**Satisfaction Width.** Per-commitment breadth of the satisfaction zone around the threshold.

**Scalar Projection.** Lossy weighted-mean reduction of the valence vector to a single number.

**Stress Tolerance.** Burden index threshold for safe-state entry (equals critical burden threshold).

**Supererogation.** Action exceeding a commitment’s threshold. Positive valence at reduced scale.

**Tension.** Conflict between appraisals of opposing valence. Preserved, not optimized away.

**Valence.** Degree and direction to which a state matters to the agent, relative to commitments.

**Valence State.** Composite result of all appraisals: vector, tensions, burden, bias.

**Valence Vector.** Multi-dimensional affective state with one axis per activated commitment.

**Violation Accrual.** Pattern-based residual cost from chronic violations detected over a sliding window.

**Zone.** Classification of an appraisal into violation, satisfaction, or supererogation.