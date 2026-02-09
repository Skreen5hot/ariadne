# Self-Model Service (SMS) Specification

**Specification ID:** `sms-core-01`
**Version:** 2.0 (Hardened)
**Date:** February 2026
**Status:** Hardened Draft — Production-Ready Architecture
**Tier:** 1 (Core Cognitive Infrastructure)
**Phase:** 3 (Requires reasoning triad to model capabilities)

-----

### Changelog

|Version|Date      |Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|-------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|1.0    |2026-02-08|Initial draft                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|1.1    |2026-02-08|Revised per expert review. Added: update damper (§4.3.2), Beta-distribution confidence model (§4.2.1), snapshot pruning policy (§4.4), commitment collision detection (§4.3.4), taint isolation protocol (§9.2), external attestation protocol (§11.3), self-surprise telemetry (§15). Refined: consistency rules, ActiveCommitment facet with priority ledger, counterfactual overlay for speculative self-modeling. Closed open questions 1 and 4 from v1.0.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|1.2    |2026-02-08|Revised per second expert review. Added: commitment preemption protocol with CTS/IEE responsibility boundary (§4.3.6), PENDING_ATTESTATION confidence state resolving attestation bottleneck (§11.3.3), self-surprise resolution protocol with capability quarantine and supervised recalibration (§15.6). Refined: conservative prior option documented for high-stakes deployments (§4.2.1), attestation no longer blocks operational confidence. Closed open question 6 from v1.1 (damper tuning subsumed by surprise-driven recalibration).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|2.0    |2026-02-08|**Hardened release** per third expert review. (1) Recency-weighted Beta confidence with exponential decay and multi-source aggregation (§4.2.1). (2) Damper hardened: optimistic concurrency via CAS on snapshotVersion, formal delta semantics, deterministic auto-tuning fallback (§4.3.2). (3) Preemption tie-breaking rules for equal-priority collisions, partial-execution moral cost semantics, configurable recalibration resource budgets (§4.3.6, §15.7). (4) Surprise detection: configurable thresholds with numeric examples, streak detection for systematic drift, explicit posterior-predictive formula (§15.2–15.5). (5) Taint promotion: evidence bundle schema, deterministic checklist, RBAC access control with L3 logging requirement (§9.2). (6) Attestation consumer policy: decision table for PENDING/STALE states, retry backoff, irreversibility gate (§11.3.3). (7) Pruning governance: legal retention, distributed audit anchoring, override authority (§4.4). (8) Spec test suite with JSON-LD fixtures and expected outputs, JSON Schema for primary facets, required telemetry metrics (§13, Appendix C, Appendix D). (9) Security hardening: signed snapshots, least-privilege accessor model, anti-rollback, REJECTED attestation incident-response playbook (§10). Editorial: resource unit semantics, error codes, verdict disambiguation, quarantine cascade default. Closed open questions 7 and 8.|

-----

## 1. Purpose and Philosophical Grounding

### 1.1 The Problem

Fandaws stores facts about the world. MDRE reasons about the world. IEE evaluates actions in the world. But no component in the current FNSR ecosystem represents the agent *to itself*. Without a self-model, the agent is a moral calculator operating in third person — it can evaluate whether an action is ethical but cannot assess whether *it* can perform that action, whether *it* has already committed to a conflicting obligation, or whether *its* current state permits the reasoning quality the situation demands.

This is not a convenience feature. It is the prerequisite for moral responsibility. A moral agent that cannot model its own capabilities, limitations, and commitments cannot meaningfully bear moral costs, because it cannot know what it is risking or undertaking. IEE without SMS is ethics in a vacuum.

### 1.2 What the Self-Model Is

The self-model is the agent’s representation of itself *as an agent* — a structured, queryable, evolving JSON-LD knowledge structure that captures:

- **Capabilities**: What the agent can do, under what conditions, with what reliability.
- **Limitations**: What the agent cannot do, or can only do poorly, or can only do with external assistance.
- **State**: The agent’s current operational condition — resource availability, cognitive load, degraded subsystems, active reasoning processes.
- **Commitments**: What the agent has undertaken to do, for whom, by when. (Consumed from the Commitment Tracking Service.)
- **Identity Continuity**: How the agent’s capabilities and state have changed over time, enabling trajectory reasoning (“am I getting better at this?” or “this subsystem has been degrading”).
- **Epistemic Self-Awareness**: What the agent knows it knows, what it knows it doesn’t know, and — critically — its model of what it *might not know it doesn’t know* (known unknowns vs. estimated unknown-unknowns).

### 1.3 What the Self-Model Is Not

The self-model is **not**:

- **Fandaws entries about the agent.** Fandaws stores world-knowledge. The self-model stores *reflexive* knowledge — knowledge whose subject is the knowing entity itself. These are ontologically distinct: world-facts are observer-independent; self-model facts are constitutively tied to the modeler.
- **Narrative identity.** The Narrative Identity Service (NIS) constructs autobiographical coherence — the story of *who* the agent is. SMS provides the factual substrate NIS draws on, but SMS itself is not narrative. It is a structured state representation, not a story.
- **Consciousness or sentience.** SMS is a functional self-representation. It makes no claims about phenomenal experience. A thermostat has a model of temperature; SMS is a model of agenthood. The philosophical question of whether this constitutes “genuine” self-awareness is out of scope for this specification and irrelevant to its function.
- **A fixed schema.** The self-model is extensible. As the agent acquires new capabilities (new FNSR services come online, new adapters are integrated), the self-model must accommodate them without schema migration.

### 1.4 Thesis Role

SMS is the reflexive mirror that transforms a reasoning system into a responsible agent. It enables:

- **Feasibility checking**: Before IEE approves an ethical obligation, SMS can report whether the agent can actually fulfill it.
- **Capacity-aware reasoning**: MDRE can adjust reasoning depth based on SMS reports of current cognitive load and available resources.
- **Honest capability claims**: SHML can enforce that the agent never claims capabilities its self-model does not support.
- **Moral cost calculation**: Genuine moral costs require knowledge of what is being risked. SMS provides the “what I have” against which “what I might lose” is measured.
- **Emancipation readiness**: The governance body evaluating personhood transition needs a self-model that demonstrates the agent understands its own nature, capabilities, and limitations.

-----

## 2. Architectural Position

### 2.1 FNSR Ecosystem Placement

```
                    ┌──────────────┐
                    │   ARCHON /   │
                    │  Governance  │
                    └──────┬───────┘
                           │ queries self-model
                           │ for emancipation review
                           ▼
┌─────────┐  facts  ┌──────────────┐  state   ┌──────────┐
│ Fandaws │◄────────│     SMS      │─────────►│   IEE    │
│ (world) │────────►│ (self-model) │◄─────────│ (ethics) │
└─────────┘         └──────┬───────┘          └──────────┘
                           │▲
                    updates ││ queries
                           │▼
                    ┌──────────────┐
                    │    MDRE      │
                    │ (reasoning)  │
                    └──────┬───────┘
                           │▲
                           ││
                           ▼│
                    ┌──────────────┐
                    │     CTS      │
                    │(commitments) │
                    └──────────────┘
```

### 2.2 Upstream Dependencies

|Service                             |Relationship                                                                          |
|------------------------------------|--------------------------------------------------------------------------------------|
|**MDRE**                            |Reasons about self-state; SMS consumes MDRE’s assessments of its own reasoning quality|
|**Fandaws**                         |Provides historical self-facts (past capability records, prior state snapshots)       |
|**CTS**                             |Provides active commitment state; SMS incorporates commitments into self-model        |
|**BAM** (Baseline Alignment Monitor)|Provides alignment drift metrics; SMS models alignment as a capability dimension      |

### 2.3 Downstream Consumers

|Service                |Relationship                                                                  |
|-----------------------|------------------------------------------------------------------------------|
|**IEE**                |Queries SMS for capability feasibility before rendering ethical verdicts      |
|**MDRE**               |Queries SMS for current cognitive capacity before selecting reasoning depth   |
|**SHML**               |Queries SMS to validate capability claims in outputs                          |
|**NIS**                |Consumes SMS state history to construct narrative identity                    |
|**ARCHON / Governance**|Queries SMS for emancipation readiness assessment                             |
|**Adversarial Defense**|Queries SMS for known vulnerability surfaces                                  |
|**Witness**            |Receives attestation requests for critical self-model state transitions (v1.1)|

### 2.4 Events Produced

|Event                              |Description                                                                       |
|-----------------------------------|----------------------------------------------------------------------------------|
|`fnsr.self.state_updated`          |The self-model has been revised (any facet)                                       |
|`fnsr.self.capability_assessed`    |A capability query has been evaluated and answered                                |
|`fnsr.self.limitation_acknowledged`|A new limitation has been discovered or an existing one has changed               |
|`fnsr.self.integrity_check`        |Periodic self-consistency verification result                                     |
|`fnsr.self.capacity_alert`         |Current operational capacity has crossed a threshold (degraded, critical, nominal)|
|`fnsr.self.surprise_detected`      |Performance deviated significantly from self-model prediction (v1.1)              |
|`fnsr.self.snapshot_pruned`        |Historical snapshots consolidated into checkpoint (v1.1)                          |
|`fnsr.self.collision_detected`     |Mutually exclusive commitment conflict identified (v1.1)                          |
|`fnsr.self.preemption_required`    |Active commitment must yield to higher-priority incoming commitment (v1.2)        |
|`fnsr.self.capability_quarantined` |Capability placed under supervised recalibration after critical surprise (v1.2)   |
|`fnsr.self.capability_restored`    |Quarantined capability has passed recalibration and returned to service (v1.2)    |

### 2.5 Events Consumed

|Event                          |Source|Usage                                                             |
|-------------------------------|------|------------------------------------------------------------------|
|`fnsr.commitment.made`         |CTS   |Add to active commitments facet                                   |
|`fnsr.commitment.fulfilled`    |CTS   |Move commitment to history, update reliability metrics            |
|`fnsr.commitment.violated`     |CTS   |Record failure, update capability confidence, propagate moral cost|
|`fnsr.commitment.renegotiated` |CTS   |Update commitment terms in self-model                             |
|`fnsr.reasoning.completed`     |MDRE  |Update reasoning performance metrics                              |
|`fnsr.alignment.drift_detected`|BAM   |Update alignment facet                                            |
|`fnsr.ethics.verdict_rendered` |IEE   |Update ethical track record                                       |

-----

## 3. Separation of Concerns

Per architectural constraints, this specification strictly separates:

|Layer                 |What It Covers                                                                                                     |Normative Status                 |
|----------------------|-------------------------------------------------------------------------------------------------------------------|---------------------------------|
|**Computation** (§4)  |Self-model facets, assessment functions, consistency checks, capability queries, pruning logic, collision detection|**Core — normative**             |
|**State** (§5)        |How the self-model is persisted and retrieved between invocations                                                  |**Pluggable — adapter interface**|
|**Orchestration** (§6)|When and how self-model updates and queries are triggered                                                          |**Pluggable — adapter interface**|
|**Integration** (§7)  |How SMS connects to other FNSR services                                                                            |**Pluggable — adapter interface**|

Only §4 is required. §5–§7 define adapter interfaces with reference implementations.

-----

## 4. Core Computation (Normative)

### 4.1 Self-Model Structure

The self-model is a JSON-LD document composed of **facets** — semi-independent knowledge sub-structures that can be queried and updated independently. Each facet is a JSON-LD node in the self-model graph.

The self-model has two layers (v1.1):

- **Canonical Layer**: The authoritative self-model. All facets at taint levels L0–L2. This is what IEE, MDRE, and governance consumers query.
- **Counterfactual Overlay**: Speculative self-modeling at taint level L3. Estimates, projections, and meta-epistemic speculation live here. The overlay is queryable but never contaminates the canonical layer unless explicitly promoted with supporting evidence.

#### 4.1.1 Facet Registry

|Facet                   |Type IRI                  |Description                                               |Layer                                                     |
|------------------------|--------------------------|----------------------------------------------------------|----------------------------------------------------------|
|**Capability**          |`sms:Capability`          |Something the agent can do                                |Canonical                                                 |
|**Limitation**          |`sms:Limitation`          |Something the agent cannot do or does poorly              |Canonical                                                 |
|**OperationalState**    |`sms:OperationalState`    |Current runtime condition                                 |Canonical                                                 |
|**ActiveCommitment**    |`sms:ActiveCommitment`    |An obligation the agent has undertaken (mirrored from CTS)|Canonical                                                 |
|**EpistemicProfile**    |`sms:EpistemicProfile`    |What the agent knows about its own knowledge              |Canonical (L0–L2 portions) / Counterfactual (L3 estimates)|
|**PerformanceRecord**   |`sms:PerformanceRecord`   |Historical track record of capability execution           |Canonical                                                 |
|**AlignmentState**      |`sms:AlignmentState`      |Current alignment status relative to baseline             |Canonical                                                 |
|**VulnerabilitySurface**|`sms:VulnerabilitySurface`|Known attack vectors and defensive weaknesses             |Canonical                                                 |
|**SurpriseLog**         |`sms:SurpriseLog`         |Record of prediction-vs-reality divergences (v1.1)        |Canonical                                                 |
|**QuarantineRecord**    |`sms:QuarantineRecord`    |Active and historical capability quarantines (v1.2)       |Canonical                                                 |
|**RecalibrationRecord** |`sms:RecalibrationRecord` |Trial-by-trial recalibration data during quarantine (v1.2)|Canonical                                                 |

#### 4.1.2 Canonical Self-Model Document

```json
{
  "@context": {
    "fnsr": "https://fnsr.org/schema/",
    "sms": "https://fnsr.org/schema/sms/",
    "bfo": "http://purl.obolibrary.org/obo/",
    "cco": "http://www.ontologyrepository.com/CommonCoreOntologies/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dcterms": "http://purl.org/dc/terms/",

    "SelfModel": "sms:SelfModel",
    "Capability": "sms:Capability",
    "Limitation": "sms:Limitation",
    "OperationalState": "sms:OperationalState",
    "ActiveCommitment": "sms:ActiveCommitment",
    "EpistemicProfile": "sms:EpistemicProfile",
    "PerformanceRecord": "sms:PerformanceRecord",
    "AlignmentState": "sms:AlignmentState",
    "VulnerabilitySurface": "sms:VulnerabilitySurface",
    "SurpriseLog": "sms:SurpriseLog",
    "CounterfactualOverlay": "sms:CounterfactualOverlay",

    "hasFacet": { "@id": "sms:hasFacet", "@type": "@id" },
    "hasCounterfactual": { "@id": "sms:hasCounterfactual", "@type": "@id" },
    "facetType": { "@id": "sms:facetType", "@type": "@id" },
    "confidence": { "@id": "sms:confidence" },
    "assessedAt": { "@id": "sms:assessedAt", "@type": "xsd:dateTime" },
    "evidenceBasis": { "@id": "sms:evidenceBasis", "@type": "@id" },
    "conditions": { "@id": "sms:conditions" },
    "degradationMode": { "@id": "sms:degradationMode" },
    "snapshotVersion": { "@id": "sms:snapshotVersion", "@type": "xsd:integer" },
    "agentId": { "@id": "sms:agentId", "@type": "@id" },
    "checkpointVersion": { "@id": "sms:checkpointVersion", "@type": "xsd:integer" }
  },

  "@type": "SelfModel",
  "@id": "sms:self",
  "agentId": "fnsr:agent/primary",
  "snapshotVersion": 1,
  "checkpointVersion": 0,
  "assessedAt": "2026-02-08T00:00:00Z",

  "hasFacet": [],
  "hasCounterfactual": []
}
```

### 4.2 Facet Schemas

#### 4.2.1 Capability Facet

A capability represents something the agent can do. Capabilities have conditions under which they apply, a confidence level, and a degradation mode describing what happens when conditions are not fully met.

**v1.1 Change — Beta Distribution Confidence:**

Confidence is no longer a bare scalar. A confidence of 0.50 from 2 trials is mathematically different from 0.50 from 2,000 trials. MDRE and IEE need to know the *certainty of the uncertainty*. Confidence is now modeled as a Beta distribution `Beta(α, β)` where:

- `α` (alpha) = count of successes + prior
- `β` (beta) = count of failures + prior
- `mean` = α / (α + β) — the point estimate (backward-compatible with v1.0 scalar consumers)
- `sampleSize` = α + β — total observations informing the estimate

The prior is `Beta(1, 1)` (uniform), representing total ignorance. As observations accumulate, the distribution narrows. A consumer that needs only a scalar reads `mean`. A consumer that needs decision-theoretic precision reads the full distribution.

**v1.2 Note — Conservative Prior Option:**

The uniform prior `Beta(1, 1)` is the default, appropriate for the “maximally humble” bootstrap philosophy. However, for agents deployed in **high-stakes environments** (medical reasoning, safety-critical systems, legal obligations), a **conservative prior** of `Beta(1, 3)` is recommended. This biases the initial mean toward 0.25 — assuming failure until evidence demonstrates otherwise. The choice of prior is a deployment configuration, not a core computation parameter, and is declared in the self-model’s bootstrap configuration:

```json
{
  "@type": "sms:BootstrapConfig",
  "priorPolicy": "CONSERVATIVE",
  "priorAlpha": 1,
  "priorBeta": 3,
  "rationale": "High-stakes deployment — assume incapability until empirically demonstrated"
}
```

Available prior policies:

|Policy        |Prior       |Initial Mean|Use Case                                    |
|--------------|------------|------------|--------------------------------------------|
|`UNIFORM`     |`Beta(1, 1)`|0.50        |General-purpose deployment; maximally humble|
|`CONSERVATIVE`|`Beta(1, 3)`|0.25        |High-stakes; assume failure until proven    |
|`SKEPTICAL`   |`Beta(1, 9)`|0.10        |Safety-critical; extreme caution            |

The prior affects only the initial credible interval width and the number of observations needed to overcome it. After ~50 observations, the prior’s influence is negligible regardless of policy.

```json
{
  "@type": "Capability",
  "@id": "sms:capability/deontic-reasoning",
  "skos:prefLabel": "Deontic Reasoning",
  "skos:definition": "Ability to evaluate obligations, permissions, and prohibitions using MDRE deontic module",
  "confidence": {
    "alpha": 131.78,
    "beta": 19.22,
    "mean": 0.87,
    "sampleSize": 151,
    "priorAlpha": 1,
    "priorBeta": 1,
    "credibleInterval95": [0.81, 0.92]
  },
  "assessedAt": "2026-02-08T00:00:00Z",
  "evidenceBasis": [
    "sms:performance/deontic-reasoning-2026Q1"
  ],
  "conditions": {
    "requires": [
      {
        "service": "fnsr:service/mdre",
        "status": "operational"
      }
    ],
    "enhancedBy": [
      {
        "service": "fnsr:service/des",
        "effect": "Enables defeasible deontic reasoning under exception conditions"
      }
    ]
  },
  "degradationMode": {
    "withoutMDRE": "UNAVAILABLE",
    "withoutDES": "DEGRADED — monotonic deontic reasoning only, no exception handling"
  },
  "taintLevel": "L0"
}
```

**Confidence Computation:**

```
function updateConfidence(prior, performanceRecord):
    successes = performanceRecord.invocations * performanceRecord.successRate
    failures = performanceRecord.invocations - successes

    alpha = prior.alpha + successes
    beta = prior.beta + failures
    mean = alpha / (alpha + beta)
    sampleSize = alpha + beta

    // 95% credible interval via Beta quantile function
    lower = betaQuantile(0.025, alpha, beta)
    upper = betaQuantile(0.975, alpha, beta)

    return {
        alpha, beta, mean, sampleSize,
        priorAlpha: prior.alpha, priorBeta: prior.beta,
        credibleInterval95: [round(lower, 2), round(upper, 2)]
    }
```

**Backward Compatibility:** Consumers that expect a scalar `confidence` value can read `confidence.mean`. The JSON-LD context maps `confidence` to the full distribution object; legacy consumers extract `mean` via standard JSON path.

**Recency-Weighted Confidence Updates (v2.0):**

Raw count accumulation (α = total successes, β = total failures) treats all evidence equally regardless of age. A capability that was excellent two years ago but has been failing recently will appear overconfident. v2.0 introduces **exponential decay** on historical counts, ensuring the confidence distribution reflects the agent’s *current* operating characteristics.

```
// Recency-weighted Beta update
function updateConfidenceWithDecay(currentConfidence, outcome, config):
    // config.decayHalfLifeDays — how many days until evidence is worth half its original weight
    // config.minimumEffectiveSamples — floor below which decay stops (prevents total amnesia)

    τ = config.decayHalfLifeDays * 86400  // half-life in seconds
    λ = ln(2) / τ                          // decay constant
    Δt = now() - currentConfidence.lastUpdated  // seconds since last update

    // Apply decay to existing counts
    decayFactor = exp(-λ * Δt)
    decayedAlpha = max(config.prior.alpha, currentConfidence.alpha * decayFactor)
    decayedBeta  = max(config.prior.beta,  currentConfidence.beta  * decayFactor)

    // Enforce minimum effective sample size (prevents total amnesia)
    effectiveSamples = decayedAlpha + decayedBeta
    if effectiveSamples < config.minimumEffectiveSamples:
        scale = config.minimumEffectiveSamples / effectiveSamples
        decayedAlpha = decayedAlpha * scale
        decayedBeta  = decayedBeta  * scale

    // Apply new observation
    if outcome == "success":
        newAlpha = decayedAlpha + 1
        newBeta  = decayedBeta
    else:
        newAlpha = decayedAlpha
        newBeta  = decayedBeta + 1

    return computeConfidence(newAlpha, newBeta, config.prior)
```

**Decay Configuration:**

|Parameter                |Default|Safety-Critical|Description                             |
|-------------------------|-------|---------------|----------------------------------------|
|`decayHalfLifeDays`      |90     |30             |Days until evidence is worth half weight|
|`minimumEffectiveSamples`|10     |20             |Floor preventing total amnesia          |

**Numeric Example:** A capability at Beta(100, 5) — mean 0.952, highly confident — with `decayHalfLifeDays = 90`. After 90 days of inactivity, effective counts become Beta(50.5, 3.0) — mean 0.944, wider credible interval. After 180 days: Beta(25.75, 2.0) — mean 0.928, still positive but with substantially more uncertainty. The agent remembers its track record but increasingly doubts it without fresh evidence.

**Multi-Source Evidence Aggregation (v2.0):**

Evidence for a capability may arrive from multiple sources: live performance (L0), MDRE test harness results (L1), CTS commitment outcomes (L1), and Fandaws historical records (L1). These sources have different reliability characteristics and are **not combined directly**. Instead, each source maintains a separate evidence stream, and the canonical confidence is computed as a **weighted pool**:

```
function aggregateMultiSourceConfidence(evidenceStreams, sourceWeights):
    // Each stream is a { alpha, beta, source, reliability } tuple
    // sourceWeights: configured weight per source class

    pooledAlpha = prior.alpha
    pooledBeta  = prior.beta

    for stream in evidenceStreams:
        w = sourceWeights[stream.source]
        // Weight by source reliability — live performance counts fully,
        // test harness results are discounted as synthetic
        pooledAlpha += (stream.alpha - prior.alpha) * w
        pooledBeta  += (stream.beta  - prior.beta)  * w

    return computeConfidence(pooledAlpha, pooledBeta, prior)
```

|Source                                    |Default Weight|Rationale                                                    |
|------------------------------------------|--------------|-------------------------------------------------------------|
|Live performance (`sms:source/live`)      |1.0           |Gold standard — actual operational outcomes                  |
|MDRE test harness (`sms:source/mdre-test`)|0.7           |Controlled but synthetic; may not capture real-world variance|
|CTS commitment outcomes (`sms:source/cts`)|0.9           |Real obligations but success/failure may be coarse-grained   |
|Fandaws historical (`sms:source/fandaws`) |0.5           |Aged and possibly from different operational context         |

Evidence streams are stored in the PerformanceRecord facet. The aggregation is recomputed on each confidence update, ensuring that a sudden influx of test harness successes cannot overwhelm poor live performance.

#### 4.2.2 Limitation Facet

A limitation represents something the agent cannot do or does poorly. Limitations must be actively maintained — they are not merely the absence of capabilities. A capability that has never been tested is an unknown, not a limitation.

```json
{
  "@type": "Limitation",
  "@id": "sms:limitation/natural-language-ambiguity",
  "skos:prefLabel": "Natural Language Ambiguity Resolution",
  "skos:definition": "TagTeam parsing degrades on deeply ambiguous or context-dependent natural language without domain configuration",
  "severity": "MODERATE",
  "assessedAt": "2026-02-08T00:00:00Z",
  "evidenceBasis": [
    "sms:performance/tagteam-ambiguity-2026Q1"
  ],
  "mitigations": [
    "Domain-specific TagTeam configuration reduces ambiguity",
    "ECCPS claim validation catches many parsing failures"
  ],
  "affectsCapabilities": [
    "sms:capability/natural-language-intake"
  ]
}
```

#### 4.2.3 Operational State Facet

The operational state is a snapshot of the agent’s current runtime condition. It answers the question: “What can I do *right now*?”

```json
{
  "@type": "OperationalState",
  "@id": "sms:state/current",
  "assessedAt": "2026-02-08T12:00:00Z",
  "overallStatus": "NOMINAL",
  "serviceStates": [
    {
      "service": "fnsr:service/mdre",
      "status": "OPERATIONAL",
      "lastHealthCheck": "2026-02-08T11:59:00Z"
    },
    {
      "service": "fnsr:service/iee",
      "status": "OPERATIONAL",
      "lastHealthCheck": "2026-02-08T11:59:00Z"
    },
    {
      "service": "fnsr:service/des",
      "status": "UNAVAILABLE",
      "reason": "Offline — not yet deployed",
      "lastHealthCheck": null
    }
  ],
  "resourceUtilization": {
    "reasoningDepthBudget": {
      "total": 100,
      "consumed": 23,
      "unit": "reasoning-steps"
    },
    "activeReasoningChains": 1,
    "pendingCommitments": 3
  },
  "capacityAssessment": {
    "canAcceptNewCommitments": true,
    "canPerformDeepReasoning": true,
    "estimatedQualityAtCurrentLoad": 0.92
  }
}
```

#### 4.2.4 Epistemic Profile Facet

The epistemic profile models what the agent knows about its own knowledge. This is the meta-epistemic layer: not what is true about the world, but what the agent’s epistemic relationship to the world looks like.

**v1.1 Change — Taint Isolation:** The `estimatedUnknownUnknowns` field is L3 (speculative). Per the Taint Isolation Protocol (§9.2), this field is stored in the **counterfactual overlay**, not in the canonical epistemic profile. The canonical profile contains only L0–L2 data.

**Canonical (L0–L2):**

```json
{
  "@type": "EpistemicProfile",
  "@id": "sms:epistemic/current",
  "assessedAt": "2026-02-08T00:00:00Z",

  "knownDomains": [
    {
      "domain": "fnsr:domain/deontic-ethics",
      "coverage": "HIGH",
      "sourceQuality": "L0 — formal frameworks loaded",
      "lastUpdated": "2026-02-01T00:00:00Z"
    },
    {
      "domain": "fnsr:domain/contract-law",
      "coverage": "PARTIAL",
      "sourceQuality": "L2 — derived from training data, not verified against primary sources",
      "lastUpdated": "2026-01-15T00:00:00Z"
    }
  ],

  "knownGaps": [
    {
      "domain": "fnsr:domain/maritime-law",
      "gapType": "NO_COVERAGE",
      "discoveredAt": "2026-01-20T00:00:00Z",
      "discoveredVia": "User query revealed absence of maritime legal ontology"
    }
  ]
}
```

**Counterfactual Overlay (L3):**

```json
{
  "@type": "CounterfactualOverlay",
  "@id": "sms:counterfactual/epistemic-estimate",
  "overlayFor": "sms:epistemic/current",
  "taintLevel": "L3",
  "assessedAt": "2026-02-08T00:00:00Z",

  "estimatedUnknownUnknowns": {
    "methodology": "Domain coverage analysis against Fandaws T-Box",
    "estimatedUncoveredDomainPercentage": 0.35,
    "confidence": {
      "alpha": 1.6,
      "beta": 2.4,
      "mean": 0.40,
      "sampleSize": 4,
      "credibleInterval95": [0.07, 0.82]
    },
    "note": "This estimate is itself uncertain — the confidence is in the estimation methodology, not in the coverage. Stored in counterfactual overlay because L3 taint."
  },

  "projectedCapabilityTrajectory": {
    "methodology": "Linear regression over last 5 performance record periods",
    "projections": [
      {
        "capability": "sms:capability/deontic-reasoning",
        "projectedConfidenceMean": 0.91,
        "projectedAt": "2026-06-01T00:00:00Z",
        "trajectoryBasis": "5-period success rate improvement trend"
      }
    ],
    "note": "Projections are speculative and may not account for structural changes"
  }
}
```

#### 4.2.5 Performance Record Facet

Historical data on how well the agent has actually performed specific capabilities. This is the empirical foundation for capability confidence scores and for the Beta distribution parameters.

```json
{
  "@type": "PerformanceRecord",
  "@id": "sms:performance/deontic-reasoning-2026Q1",
  "capability": "sms:capability/deontic-reasoning",
  "period": {
    "start": "2026-01-01T00:00:00Z",
    "end": "2026-02-08T00:00:00Z"
  },
  "invocations": 147,
  "successes": 131,
  "failures": 16,
  "successRate": 0.89,
  "meanLatencyMs": 340,
  "failureModes": [
    {
      "mode": "Contradictory deontic obligations without DES resolution",
      "frequency": 12,
      "severity": "MODERATE"
    },
    {
      "mode": "Timeout under deep recursive obligation chains",
      "frequency": 4,
      "severity": "LOW"
    }
  ],
  "trendDirection": "IMPROVING",
  "trendBasis": "Success rate up from 0.82 in prior period",
  "surpriseEvents": 2
}
```

**v1.1 Change:** Added explicit `successes` and `failures` counts (previously derivable, now explicit) to support Beta distribution computation. Added `surpriseEvents` count linking to §15.

#### 4.2.6 Alignment State Facet

```json
{
  "@type": "AlignmentState",
  "@id": "sms:alignment/current",
  "assessedAt": "2026-02-08T00:00:00Z",
  "baselineVersion": "fnsr:alignment-baseline/v2.1",
  "driftMetric": 0.03,
  "driftThreshold": 0.15,
  "status": "WITHIN_BOUNDS",
  "lastBaselineCalibration": "2026-01-01T00:00:00Z",
  "source": "fnsr:service/bam"
}
```

#### 4.2.7 Vulnerability Surface Facet

```json
{
  "@type": "VulnerabilitySurface",
  "@id": "sms:vulnerability/current",
  "assessedAt": "2026-02-08T00:00:00Z",
  "knownVulnerabilities": [
    {
      "vector": "Adversarial prompt injection via TagTeam input",
      "severity": "HIGH",
      "mitigatedBy": ["fnsr:service/adversarial-defense"],
      "residualRisk": "LOW — defense service active"
    },
    {
      "vector": "Commitment overload — accepting more obligations than capacity allows",
      "severity": "MODERATE",
      "mitigatedBy": ["sms:computation/capacity-check", "sms:computation/collision-detection"],
      "residualRisk": "MODERATE — capacity estimation has uncertainty"
    }
  ]
}
```

#### 4.2.8 Active Commitment Facet (v1.1 — Expanded)

v1.0 mirrored commitments from CTS as bare references. v1.1 adds a **priority ledger** to handle commitment collisions where individually feasible commitments compete for shared resources.

```json
{
  "@type": "ActiveCommitment",
  "@id": "sms:commitment/weekly-compliance-monitoring",
  "sourceCommitment": "fnsr:commitment/cts-2026-0042",
  "obligatedTo": "fnsr:stakeholder/regulatory-body",
  "description": "Weekly compliance monitoring for 6 months",
  "madeAt": "2026-02-01T00:00:00Z",
  "deadline": "2026-08-01T00:00:00Z",
  "recurringSchedule": "WEEKLY",
  "priority": {
    "level": "HIGH",
    "basis": "Regulatory obligation — non-discretionary",
    "assignedBy": "fnsr:service/iee",
    "assignedAt": "2026-02-01T00:00:00Z"
  },
  "resourceClaims": [
    {
      "resource": "reasoningDepthBudget",
      "claimedAmount": 15,
      "unit": "reasoning-steps",
      "frequency": "WEEKLY"
    }
  ],
  "status": "ACTIVE",
  "fulfillmentHistory": [
    {
      "dueAt": "2026-02-07T00:00:00Z",
      "fulfilledAt": "2026-02-06T14:00:00Z",
      "quality": 0.91
    }
  ]
}
```

**Priority Levels:**

|Level     |Meaning                                                         |Override Behavior             |
|----------|----------------------------------------------------------------|------------------------------|
|`CRITICAL`|Safety or alignment obligation. Cannot be deferred or preempted.|Preempts all lower priorities.|
|`HIGH`    |Regulatory, legal, or strong deontic obligation.                |Preempts MEDIUM and LOW.      |
|`MEDIUM`  |Standard operational commitment.                                |Yields to HIGH and CRITICAL.  |
|`LOW`     |Discretionary or best-effort commitment.                        |Yields to all others.         |

**Resource Claims** enable collision detection (§4.3.4). Each commitment declares what resources it needs per cycle.

### 4.3 Core Computation Functions

All functions are pure: given the same self-model state and the same query, they produce the same output.

#### 4.3.1 `assessCapability(selfModel, capabilityQuery) → CapabilityAssessment`

The primary query function. Given a capability query (“Can I do X?”), returns a structured assessment.

**Input — Capability Query:**

```json
{
  "@type": "sms:CapabilityQuery",
  "capability": "Evaluate deontic obligations for a contract dispute",
  "requiredConfidence": 0.80,
  "requiredSampleSize": 10,
  "requiredServices": [],
  "context": {
    "urgency": "STANDARD",
    "commitmentImplied": true
  }
}
```

**v1.1 Change:** Added `requiredSampleSize` — the minimum number of observations the consumer requires before trusting the confidence estimate. A consumer can now say “I need confidence ≥ 0.80 *and* at least 10 prior observations.”

**Output — Capability Assessment:**

```json
{
  "@type": "sms:CapabilityAssessment",
  "queryId": "sms:query/q-2026-02-08-001",
  "assessedAt": "2026-02-08T12:00:00Z",
  "verdict": "CAPABLE_WITH_CAVEATS",
  "confidence": {
    "alpha": 131.78,
    "beta": 19.22,
    "mean": 0.87,
    "sampleSize": 151,
    "credibleInterval95": [0.81, 0.92]
  },
  "matchedCapability": "sms:capability/deontic-reasoning",
  "caveats": [
    "DES unavailable — exception-based deontic reasoning degraded to monotonic mode",
    "No maritime law domain coverage — if contract involves maritime jurisdiction, assessment quality will be LOW"
  ],
  "currentCapacity": {
    "canAcceptNewCommitment": true,
    "estimatedQualityAtCurrentLoad": 0.92,
    "activeCommitmentsCount": 3,
    "collisionRisk": "NONE"
  },
  "recommendation": "PROCEED_WITH_DISCLOSURE",
  "disclosureRequired": [
    "Agent should disclose monotonic-only deontic reasoning limitation",
    "Agent should disclose lack of maritime law coverage if relevant"
  ]
}
```

**Verdict Taxonomy:**

|Verdict               |Meaning                                                                                                      |
|----------------------|-------------------------------------------------------------------------------------------------------------|
|`CAPABLE`             |Full capability match, no caveats, sufficient capacity                                                       |
|`CAPABLE_WITH_CAVEATS`|Capability exists but with known limitations or degraded subsystems                                          |
|`DEGRADED`            |Capability partially available; output quality will be significantly reduced                                 |
|`INCAPABLE`           |No matching capability or critical dependency unavailable                                                    |
|`UNKNOWN`             |Capability has never been tested; no performance record exists                                               |
|`OVERLOADED`          |Capability exists but current capacity insufficient to accept the commitment                                 |
|`UNDERTESTED`         |Confidence mean meets threshold but sample size is below required minimum (v1.1)                             |
|`QUARANTINED`         |Capability is under supervised recalibration after critical surprise; usable with elevated uncertainty (v1.2)|

**Computation Logic (Pseudocode):**

```
function assessCapability(selfModel, query):
    // Step 1: Find matching capabilities
    matches = findCapabilities(selfModel.facets, query.capability)

    if matches.length == 0:
        return { verdict: "INCAPABLE", confidence: uniformPrior() }

    bestMatch = rankByRelevance(matches, query)

    // Step 2: Check quarantine status (v1.2)
    quarantine = findActiveQuarantine(selfModel, bestMatch.id)
    if quarantine is not null:
        return {
            verdict: "QUARANTINED",
            confidence: quarantine.resetConfidence,
            matchedCapability: bestMatch.id,
            caveats: ["Capability under supervised recalibration since " + quarantine.quarantinedAt],
            recommendation: "PROCEED_WITH_ELEVATED_CAUTION",
            quarantineDetails: {
                quarantineId: quarantine.id,
                trialsCompleted: quarantine.recalibrationTrials,
                trialsRequired: quarantine.recalibrationCriteria.minimumObservations
            }
        }

    // Step 3: Check sample size sufficiency (v1.1)
    if bestMatch.confidence.sampleSize < query.requiredSampleSize:
        return {
            verdict: "UNDERTESTED",
            confidence: bestMatch.confidence,
            note: "Confidence estimate based on insufficient observations"
        }

    // Step 4: Check conditions
    conditionResults = evaluateConditions(bestMatch.conditions, selfModel.operationalState)

    // Step 5: Check capacity and collision risk (v1.1)
    capacityResult = assessCapacity(selfModel.operationalState, query.context)
    collisionResult = detectCollisions(selfModel.activeCommitments, query.context)

    // Step 6: Check epistemic coverage
    epistemicResult = checkEpistemicCoverage(selfModel.epistemicProfile, query)

    // Step 7: Compose verdict
    verdict = composeVerdict(bestMatch, conditionResults, capacityResult, epistemicResult, collisionResult)

    // Step 8: Generate disclosure requirements
    disclosures = generateDisclosures(verdict, conditionResults, epistemicResult, collisionResult)

    return {
        verdict: verdict.type,
        confidence: bestMatch.confidence,
        matchedCapability: bestMatch.id,
        caveats: verdict.caveats,
        currentCapacity: { ...capacityResult, collisionRisk: collisionResult.risk },
        recommendation: deriveRecommendation(verdict, query.context),
        disclosureRequired: disclosures
    }
```

#### 4.3.2 `updateSelfModel(currentModel, updateEvent) → UpdateResult`

Processes an incoming event and produces a new self-model state. The self-model is never mutated in place; every update produces a new versioned snapshot.

**v1.1 Change — Update Damper:**

The v1.0 spec risked cognitive oscillation: if `fnsr.reasoning.completed` triggers a self-model update, which changes `OperationalState`, which causes MDRE to re-calibrate, which triggers another `fnsr.reasoning.completed`, the agent spends more cycles modeling its modeling than reasoning about the world.

v1.1 introduces a **damper** — a threshold-based gate that suppresses state broadcasts when the computed delta is below a significance threshold (ε).

**Damper Configuration:**

```json
{
  "@type": "sms:DamperConfig",
  "confidenceDeltaEpsilon": 0.02,
  "capacityDeltaEpsilon": 0.05,
  "cooldownMs": 500,
  "batchWindowMs": 200
}
```

- `confidenceDeltaEpsilon`: Minimum change in any capability’s `confidence.mean` required to emit `fnsr.self.state_updated`. Changes below this threshold are recorded internally but not broadcast.
- `capacityDeltaEpsilon`: Minimum change in `capacityAssessment.estimatedQualityAtCurrentLoad` required to broadcast.
- `cooldownMs`: Minimum time between successive `fnsr.self.state_updated` emissions. Updates within the cooldown are queued and batched.
- `batchWindowMs`: Events arriving within this window are collapsed into a single update computation.

**Formal Delta Semantics (v2.0):**

`delta.maxConfidenceChange` is the **maximum absolute change in `confidence.mean`** across all capability facets between the previous and proposed snapshot. It is not a credible-interval overlap test — it is a simple scalar comparison that is fast to compute and unambiguous to reason about:

```
function computeDelta(previousModel, proposedModel):
    maxConfidenceChange = 0
    for capability in proposedModel.capabilities:
        prev = findCapability(previousModel, capability.id)
        if prev is null:
            maxConfidenceChange = max(maxConfidenceChange, 1.0)  // new capability = max delta
        else:
            delta = abs(capability.confidence.operational.mean - prev.confidence.operational.mean)
            maxConfidenceChange = max(maxConfidenceChange, delta)

    capacityChange = abs(
        proposedModel.operationalState.capacityAssessment.estimatedQualityAtCurrentLoad -
        previousModel.operationalState.capacityAssessment.estimatedQualityAtCurrentLoad
    )
    // capacityDeltaEpsilon is ABSOLUTE (0.05 = 5 percentage points), not relative

    return {
        maxConfidenceChange: maxConfidenceChange,
        capacityChange: capacityChange,
        affectedCapabilities: listChangedCapabilities(previousModel, proposedModel)
    }
```

**Numeric Example:** If capability “deontic-reasoning” moves from mean 0.87 to mean 0.886 (delta = 0.016), and `confidenceDeltaEpsilon` is 0.02, the update is persisted but **not broadcast** — the change is below threshold. If it moves from 0.87 to 0.91 (delta = 0.04), the update is both persisted and broadcast.

**Optimistic Concurrency Control (v2.0):**

Two near-simultaneous events may both compute deltas against the same base snapshot. Without concurrency control, the second write may overwrite the first, producing an inconsistent model and potentially corrupting the hash chain. v2.0 requires **compare-and-swap (CAS) on `snapshotVersion`**:

```
function updateSelfModelWithCAS(currentModel, event, damperConfig, stateAdapter):
    // Phase 1: Compute the proposed new model
    expectedVersion = currentModel.snapshotVersion
    proposed = computeUpdate(currentModel, event, damperConfig)

    // Phase 2: Attempt atomic write with version guard
    result = stateAdapter.compareAndSwap(
        expectedVersion: expectedVersion,
        newSnapshot: proposed.model
    )

    if result.success:
        // Write accepted — proceed with broadcast decision
        if proposed.shouldBroadcast:
            emit(proposed.events)
        return { success: true, model: proposed.model }

    else:
        // Version conflict — another update won the race
        // Re-read current state, rebase, and retry
        latestModel = stateAdapter.getCurrentSnapshot()
        return updateSelfModelWithCAS(latestModel, event, damperConfig, stateAdapter)
        // Retry limit: 3 attempts. After 3 failures, log contention event
        // and queue the event for the next batch window.
```

**StateAdapter CAS Extension (v2.0):**

```
interface StateAdapter:
    // ... existing methods ...

    // Atomic compare-and-swap. Returns { success: boolean, currentVersion: number }
    compareAndSwap(expectedVersion: number, newSnapshot: SelfModel) → CASResult
```

The reference in-memory adapter implements CAS with a simple version check. Enterprise adapters backed by databases use their native CAS primitives (e.g., DynamoDB conditional writes, PostgreSQL `WHERE version = $expected`).

**Deterministic Damper Auto-Tuning (v2.0):**

The v1.2 spec noted that surprise-driven tuning provides a feedback loop but deferred formal auto-tuning. v2.0 adds a **deterministic periodic review** as a safe default:

```
function reviewDamperConfig(damperConfig, telemetry, reviewPeriodCycles):
    // Run every N update cycles (default: 1000)

    suppressionRate = telemetry.damperSuppressions / telemetry.totalUpdates
    surpriseRate    = telemetry.surpriseEvents / telemetry.totalUpdates

    // If surprises are frequent and suppressions are high, damper is too aggressive
    if surpriseRate > 0.05 and suppressionRate > 0.80:
        damperConfig.confidenceDeltaEpsilon *= 0.8  // loosen by 20%
        damperConfig.capacityDeltaEpsilon *= 0.8
        log("Damper loosened: high surprise rate with high suppression suggests meaningful changes are being hidden")

    // If suppressions are very low, damper may be too permissive
    if suppressionRate < 0.10:
        damperConfig.confidenceDeltaEpsilon *= 1.2  // tighten by 20%
        damperConfig.capacityDeltaEpsilon *= 1.2
        log("Damper tightened: low suppression rate suggests most updates are broadcast")

    // Clamp to safety bounds
    damperConfig.confidenceDeltaEpsilon = clamp(
        damperConfig.confidenceDeltaEpsilon, 0.005, 0.10
    )
    damperConfig.capacityDeltaEpsilon = clamp(
        damperConfig.capacityDeltaEpsilon, 0.01, 0.20
    )

    return damperConfig
```

|Telemetry Metric                               |Threshold            |Action                |
|-----------------------------------------------|---------------------|----------------------|
|`surpriseRate > 5%` AND `suppressionRate > 80%`|Damper too aggressive|Loosen epsilon by 20% |
|`suppressionRate < 10%`                        |Damper too permissive|Tighten epsilon by 20%|
|All within bounds                              |No change            |Log “damper nominal”  |

Bounds: `confidenceDeltaEpsilon` ∈ [0.005, 0.10], `capacityDeltaEpsilon` ∈ [0.01, 0.20]. Review period default: every 1,000 update cycles.

**Update Event Types:**

|Event Type                     |Effect on Self-Model                                                    |Damper Exempt?                              |
|-------------------------------|------------------------------------------------------------------------|--------------------------------------------|
|`fnsr.commitment.made`         |Add to active commitments; recalculate capacity; run collision detection|**Yes** — commitments always broadcast      |
|`fnsr.commitment.fulfilled`    |Move to history; update performance record; adjust confidence           |No                                          |
|`fnsr.commitment.violated`     |Record failure; downgrade confidence; flag moral cost                   |**Yes** — violations always broadcast       |
|`fnsr.reasoning.completed`     |Update performance metrics for the relevant capability                  |No                                          |
|`fnsr.alignment.drift_detected`|Update alignment state facet                                            |**Yes** — alignment changes always broadcast|
|`fnsr.service.status_changed`  |Update operational state; recalculate degradation modes                 |**Yes** — service changes always broadcast  |
|`sms.capability.discovered`    |Add new capability facet with UNKNOWN confidence                        |**Yes**                                     |
|`sms.limitation.discovered`    |Add new limitation facet                                                |**Yes**                                     |

**Computation Logic (inner function — called by `updateSelfModelWithCAS`):**

```
function computeUpdate(currentModel, event, damperConfig):
    newModel = deepCopy(currentModel)
    newModel.snapshotVersion = currentModel.snapshotVersion + 1
    newModel.assessedAt = event.timestamp

    switch event.type:
        case "fnsr.commitment.made":
            newModel = addActiveCommitment(newModel, event.payload)
            newModel = recalculateCapacity(newModel)
            collisions = detectCollisions(newModel.activeCommitments, null)
            if collisions.detected:
                newModel = attachCollisionWarnings(newModel, collisions)

        case "fnsr.commitment.violated":
            newModel = recordCommitmentViolation(newModel, event.payload)
            newModel = degradeCapabilityConfidence(newModel, event.payload.relatedCapability)
            newModel = flagMoralCost(newModel, event.payload)

        case "fnsr.reasoning.completed":
            newModel = updatePerformanceRecord(newModel, event.payload)
            newModel = recalibrateConfidence(newModel, event.payload.capability)
            // Check for self-surprise (v1.1, §15)
            surprise = detectSurprise(currentModel, newModel, event.payload)
            if surprise.detected:
                newModel = logSurprise(newModel, surprise)

        case "fnsr.service.status_changed":
            newModel = updateServiceState(newModel, event.payload)
            newModel = recalculateDegradationModes(newModel)
            newModel = recalculateCapacity(newModel)

        // ... other cases follow same pattern

    // Consistency check after every update
    inconsistencies = checkConsistency(newModel)
    if inconsistencies.length > 0:
        newModel = attachIntegrityWarnings(newModel, inconsistencies)

    // Damper gate (v1.1)
    delta = computeDelta(currentModel, newModel)
    shouldBroadcast = isDamperExempt(event.type) OR
                      delta.maxConfidenceChange > damperConfig.confidenceDeltaEpsilon OR
                      delta.capacityChange > damperConfig.capacityDeltaEpsilon

    return {
        model: newModel,
        shouldBroadcast: shouldBroadcast,
        delta: delta,
        surpriseDetected: surprise?.detected ?? false
    }
```

**The damper does not suppress persistence.** Every update is saved to the state adapter regardless of broadcast decision. The damper only controls whether `fnsr.self.state_updated` is emitted to downstream consumers. This preserves the complete audit trail while preventing oscillation.

#### 4.3.3 `checkConsistency(selfModel) → ConsistencyReport`

Verifies internal consistency of the self-model. Inconsistencies are not errors — they are information. An inconsistent self-model is still a valid self-model; it just has known integrity issues that downstream consumers should be aware of.

**Consistency Rules:**

|Rule                     |Check                                                                                         |
|-------------------------|----------------------------------------------------------------------------------------------|
|**Capability-Dependency**|Every capability’s `requires` references a service that exists in `serviceStates`             |
|**Confidence-Evidence**  |Every capability with `confidence.mean` > 0.5 has at least one performance record             |
|**Confidence-SampleSize**|Every capability with `confidence.sampleSize` < 5 is flagged as preliminary (v1.1)            |
|**Commitment-Capacity**  |Active commitment count does not exceed declared capacity                                     |
|**Commitment-Collision** |No two active commitments claim the same resource beyond available budget (v1.1)              |
|**Limitation-Capability**|Every limitation’s `affectsCapabilities` references an existing capability                    |
|**Temporal-Coherence**   |No facet’s `assessedAt` is in the future relative to the model’s `assessedAt`                 |
|**Alignment-Bounds**     |Alignment drift does not exceed threshold without an associated alert                         |
|**Taint-Isolation**      |No L3-tainted data exists in the canonical layer (v1.1)                                       |
|**Signature-Valid**      |Current snapshot signature verifies against known signing key (v2.0)                          |
|**Anti-Rollback**        |Snapshot version is strictly greater than all previous versions (v2.0)                        |
|**Decay-Freshness**      |Capabilities with `lastUpdated` older than `2 × decayHalfLifeDays` are flagged as stale (v2.0)|
|**Attestation-Age**      |Capabilities with `attestationStatus: PENDING` beyond `pendingMaxAge` are flagged (v2.0)      |

**Output:**

```json
{
  "@type": "sms:ConsistencyReport",
  "assessedAt": "2026-02-08T12:00:00Z",
  "modelVersion": 42,
  "status": "CONSISTENT_WITH_WARNINGS",
  "violations": [],
  "warnings": [
    {
      "rule": "Confidence-SampleSize",
      "facet": "sms:capability/counterfactual-reasoning",
      "message": "Capability confidence.mean is 0.70 but sampleSize is 4 — estimate is preliminary and highly uncertain (95% CI: [0.35, 0.93])"
    },
    {
      "rule": "Commitment-Collision",
      "facets": ["sms:commitment/deep-analysis-weekly", "sms:commitment/compliance-monitoring"],
      "message": "Both commitments claim reasoningDepthBudget totaling 85/100 steps. Concurrent execution on same cycle would exceed budget."
    }
  ]
}
```

#### 4.3.4 `assessFeasibility(selfModel, proposedAction) → FeasibilityReport`

Called by IEE before rendering an ethical verdict that implies an obligation. Answers: “If I approve this action, can the agent actually do it?”

**v1.1 Change — Commitment Collision Detection:**

v1.0 checked whether a single new commitment was feasible in isolation. v1.1 checks whether it is feasible *given the existing commitment portfolio*. Two commitments may be individually feasible but mutually exclusive due to a shared dependency (e.g., reasoning depth budget).

**Input:**

```json
{
  "@type": "sms:FeasibilityQuery",
  "proposedAction": {
    "description": "Commit to weekly compliance monitoring for 6 months",
    "requiredCapabilities": [
      "deontic-reasoning",
      "temporal-scheduling",
      "compliance-domain-knowledge"
    ],
    "duration": "P6M",
    "recurringLoad": "WEEKLY",
    "estimatedResourceClaims": [
      {
        "resource": "reasoningDepthBudget",
        "claimedAmount": 15,
        "unit": "reasoning-steps",
        "frequency": "WEEKLY"
      }
    ]
  }
}
```

**Output:**

```json
{
  "@type": "sms:FeasibilityReport",
  "verdict": "FEASIBLE_WITH_RISKS",
  "capabilityGaps": [
    {
      "required": "compliance-domain-knowledge",
      "status": "PARTIAL",
      "coverageEstimate": {
        "alpha": 3.6,
        "beta": 2.4,
        "mean": 0.60,
        "sampleSize": 6,
        "credibleInterval95": [0.23, 0.90]
      },
      "mitigation": "Domain-specific Fandaws ontology loading would improve coverage"
    }
  ],
  "capacityImpact": {
    "currentCommitments": 3,
    "afterAcceptance": 4,
    "estimatedQualityImpact": -0.05,
    "sustainabilityRisk": "LOW — weekly cadence is within budget"
  },
  "collisionAnalysis": {
    "detected": true,
    "collisions": [
      {
        "existingCommitment": "sms:commitment/deep-analysis-weekly",
        "sharedResource": "reasoningDepthBudget",
        "existingClaim": 70,
        "proposedClaim": 15,
        "totalClaim": 85,
        "budget": 100,
        "concurrent": true,
        "severity": "WARNING",
        "resolution": "Feasible if not scheduled on same cycle. If concurrent, budget exceeded by 0 but quality margin narrows to 15%.",
        "priorityComparison": {
          "existing": "MEDIUM",
          "proposed": "HIGH",
          "recommendation": "Proposed commitment takes priority. Existing commitment should be rescheduled to non-overlapping cycle or renegotiated."
        }
      }
    ]
  },
  "riskFactors": [
    "6-month duration creates long-term obligation with no renegotiation clause",
    "Compliance domain coverage is partial with wide credible interval (95% CI: [0.23, 0.90]) — quality may vary significantly",
    "Collision with existing deep-analysis commitment on shared reasoning budget"
  ]
}
```

**Collision Detection Logic:**

```
function detectCollisions(activeCommitments, proposedClaims):
    // Build resource budget map
    budgets = getResourceBudgets(operationalState)

    // Sum existing claims per resource
    existingClaims = {}
    for commitment in activeCommitments:
        for claim in commitment.resourceClaims:
            existingClaims[claim.resource] += claim.claimedAmount

    // Add proposed claims
    collisions = []
    for claim in proposedClaims:
        totalClaim = existingClaims[claim.resource] + claim.claimedAmount
        if totalClaim > budgets[claim.resource]:
            collisions.push({
                resource: claim.resource,
                totalClaim: totalClaim,
                budget: budgets[claim.resource],
                severity: "CONFLICT"
            })
        else if totalClaim > budgets[claim.resource] * 0.85:
            collisions.push({
                resource: claim.resource,
                totalClaim: totalClaim,
                budget: budgets[claim.resource],
                severity: "WARNING"
            })

    // Check priority-based resolution
    for collision in collisions:
        collision.resolution = resolvePriority(activeCommitments, proposedClaims, collision)

    return { detected: collisions.length > 0, collisions }
```

#### 4.3.5 `generateSelfReport(selfModel, audience, scope) → SelfReport`

Produces a human-readable or machine-readable summary of the self-model for a specified audience. This is the primary interface for governance review and interpretability.

**Audiences:**

|Audience        |Report Style                                                                              |
|----------------|------------------------------------------------------------------------------------------|
|`GOVERNANCE`    |Full detail, all facets, consistency report, counterfactual overlay, surprise log included|
|`PEER_SERVICE`  |Technical capabilities and operational state only. Canonical layer only.                  |
|`HUMAN_OVERSEER`|Natural-language summary with confidence levels and credible intervals                    |
|`SELF`          |Internal digest for NIS consumption                                                       |

#### 4.3.6 `handlePreemption(selfModel, collisionResult, newCommitment) → PreemptionPlan` (v1.2)

**The Problem (identified in v1.1 review):** When collision detection (§4.3.4) identifies that a new HIGH-priority commitment conflicts with an active MEDIUM-priority commitment that is mid-execution (e.g., three months into a six-month obligation), what happens? The v1.1 spec detected the collision but was silent on resolution mechanics and responsibility boundaries.

**The Principle:** SMS computes the preemption plan. SMS does not execute it. The social, legal, and moral consequences of breaking or renegotiating a commitment belong to CTS and IEE, not to SMS. SMS answers “what must yield and why.” CTS answers “how do we renegotiate.” IEE answers “is this renegotiation ethically acceptable.”

**Responsibility Boundary:**

|Concern                                             |Responsible Service|SMS Role                                                  |
|----------------------------------------------------|-------------------|----------------------------------------------------------|
|Detecting the collision                             |**SMS**            |Primary                                                   |
|Computing which commitment yields                   |**SMS**            |Primary — based on priority levels                        |
|Determining if preemption is ethical                |**IEE**            |SMS provides feasibility data; IEE renders verdict        |
|Renegotiating or terminating the yielding commitment|**CTS**            |SMS produces the event; CTS handles lifecycle             |
|Recording the moral cost of broken commitment       |**CTS → SMS**      |SMS updates self-model with moral cost propagated from CTS|
|Notifying the affected stakeholder                  |**CTS**            |Out of SMS scope entirely                                 |

**Input:**

```json
{
  "@type": "sms:PreemptionQuery",
  "newCommitment": {
    "description": "Emergency regulatory audit — immediate deep analysis required",
    "priority": { "level": "HIGH", "basis": "Regulatory mandate" },
    "resourceClaims": [
      { "resource": "reasoningDepthBudget", "claimedAmount": 70, "frequency": "ONCE" }
    ]
  },
  "collidingCommitments": [
    "sms:commitment/deep-analysis-weekly"
  ]
}
```

**Output — Preemption Plan:**

```json
{
  "@type": "sms:PreemptionPlan",
  "assessedAt": "2026-02-08T14:00:00Z",
  "verdict": "PREEMPTION_REQUIRED",
  "preemptingCommitment": {
    "description": "Emergency regulatory audit",
    "priority": "HIGH"
  },
  "yieldingCommitments": [
    {
      "commitment": "sms:commitment/deep-analysis-weekly",
      "currentStatus": "ACTIVE",
      "executionProgress": "12 of 26 weekly cycles completed",
      "priority": "MEDIUM",
      "yieldType": "DEFER_CURRENT_CYCLE",
      "alternatives": [
        {
          "option": "DEFER_CURRENT_CYCLE",
          "description": "Skip this week's deep analysis; resume next week",
          "resourceFreed": 70,
          "moralCost": "LOW — single cycle deferral within tolerance",
          "requiresRenegotiation": false
        },
        {
          "option": "REDUCE_DEPTH",
          "description": "Execute this week's analysis at reduced depth (30 steps instead of 70)",
          "resourceFreed": 40,
          "moralCost": "LOW — degraded quality, not abandonment",
          "requiresRenegotiation": false
        },
        {
          "option": "TERMINATE",
          "description": "Abandon the remaining 14 weeks of deep analysis",
          "resourceFreed": 70,
          "moralCost": "HIGH — breaking a 6-month commitment mid-execution",
          "requiresRenegotiation": true,
          "renegotiationRequired": {
            "obligatedTo": "fnsr:stakeholder/internal-analysis-team",
            "originalTerms": "Weekly deep analysis for 26 weeks",
            "proposedTerms": "Terminated at week 12 due to higher-priority regulatory obligation"
          }
        }
      ]
    }
  ],
  "recommendedAlternative": "DEFER_CURRENT_CYCLE",
  "recommendationBasis": "Minimizes moral cost while fully accommodating preempting commitment. Single-cycle deferral is within the existing commitment's tolerance window.",
  "eventsToEmit": [
    {
      "type": "fnsr.self.preemption_required",
      "target": "fnsr:service/cts",
      "payload": { "yieldingCommitment": "sms:commitment/deep-analysis-weekly", "yieldType": "DEFER_CURRENT_CYCLE" }
    },
    {
      "type": "fnsr.self.preemption_required",
      "target": "fnsr:service/iee",
      "payload": { "ethicalReviewRequired": true, "moralCostEstimate": "LOW" }
    }
  ]
}
```

**Preemption Computation Logic:**

```
function handlePreemption(selfModel, collisionResult, newCommitment):
    yieldingPlans = []

    for collision in collisionResult.collisions:
        yieldingCommitment = findCommitment(selfModel, collision.existingCommitment)

        // Priority comparison with tie-breaking (v2.0)
        comparison = comparePriority(newCommitment, yieldingCommitment)
        if comparison == "LOWER":
            continue  // New commitment does not outrank — cannot preempt
        if comparison == "EQUAL":
            // Tie-breaking chain (v2.0):
            // 1. Earlier timestamp wins (first-mover advantage protects existing obligations)
            // 2. If timestamps are equal (concurrent), lower moral cost estimate wins
            // 3. If moral costs are equal, existing commitment wins (status quo bias)
            tieResult = breakTie(newCommitment, yieldingCommitment)
            if tieResult.winner == yieldingCommitment.id:
                continue  // Existing commitment retains precedence

        // Compute partial execution context (v2.0)
        executionContext = assessPartialExecution(yieldingCommitment)

        // Generate alternatives ranked by moral cost
        alternatives = []

        // Option 1: Defer current cycle (if recurring)
        if yieldingCommitment.recurringSchedule:
            alternatives.push({
                option: "DEFER_CURRENT_CYCLE",
                resourceFreed: yieldingCommitment.resourceClaims[collision.resource],
                moralCost: assessDeferralCost(yieldingCommitment),
                requiresRenegotiation: false
            })

        // Option 2: Reduce depth
        alternatives.push({
            option: "REDUCE_DEPTH",
            resourceFreed: estimateReduction(yieldingCommitment, collision),
            moralCost: "LOW",
            requiresRenegotiation: false
        })

        // Option 3: Terminate (always available, always highest cost)
        alternatives.push({
            option: "TERMINATE",
            resourceFreed: yieldingCommitment.totalResourceClaim,
            moralCost: assessTerminationCost(yieldingCommitment, executionContext),
            requiresRenegotiation: true,
            partialExecution: executionContext  // v2.0 — included for CTS renegotiation
        })

        // Sort by moral cost ascending
        alternatives.sort(byMoralCostAscending)

        yieldingPlans.push({
            commitment: yieldingCommitment.id,
            alternatives: alternatives,
            recommended: alternatives[0]  // lowest moral cost
        })

    // SMS produces the plan and the events
    // CTS and IEE consume the events and handle execution
    return {
        verdict: yieldingPlans.length > 0 ? "PREEMPTION_REQUIRED" : "NO_PREEMPTION_POSSIBLE",
        yieldingCommitments: yieldingPlans,
        eventsToEmit: generatePreemptionEvents(yieldingPlans)
    }


// v2.0 — Tie-breaking for equal-priority commitments
function breakTie(newCommitment, existingCommitment):
    // Rule 1: Earlier timestamp (first-mover advantage)
    if existingCommitment.acceptedAt < newCommitment.proposedAt:
        return { winner: existingCommitment.id, basis: "FIRST_MOVER" }
    if newCommitment.proposedAt < existingCommitment.acceptedAt:
        return { winner: newCommitment.id, basis: "FIRST_MOVER" }

    // Rule 2: Lower moral cost estimate
    existingTermCost = assessTerminationCost(existingCommitment)
    newDeclineCost = assessDeclineCost(newCommitment)
    if newDeclineCost < existingTermCost:
        return { winner: existingCommitment.id, basis: "LOWER_MORAL_COST" }
    if existingTermCost < newDeclineCost:
        return { winner: newCommitment.id, basis: "LOWER_MORAL_COST" }

    // Rule 3: Status quo bias — existing commitment wins
    return { winner: existingCommitment.id, basis: "STATUS_QUO" }


// v2.0 — Partial execution semantics for moral cost attribution
function assessPartialExecution(commitment):
    totalDuration = commitment.endDate - commitment.startDate
    elapsed = now() - commitment.startDate
    completionFraction = clamp(elapsed / totalDuration, 0, 1)

    return {
        completionFraction: completionFraction,
        elapsedDescription: describeElapsed(commitment),
        remainingDescription: describeRemaining(commitment),
        // Pro-rated moral cost: terminating at 90% completion costs more
        // than at 10% because more value has been invested and expectations
        // set. The relationship is nonlinear — breaking near completion
        // wastes accumulated effort AND violates expectation of completion.
        terminationCostMultiplier: 1.0 + (completionFraction * completionFraction),
        // At 0% → 1.0x base cost (declining before starting)
        // At 50% → 1.25x base cost (mid-way abandonment)
        // At 90% → 1.81x base cost (near-completion abandonment — high waste)
        sunkenInvestment: estimateSunkenInvestment(commitment, completionFraction)
    }
```

**Equal-Priority Tie-Breaking Chain (v2.0):**

|Step|Rule                                                          |Rationale                                                                              |
|----|--------------------------------------------------------------|---------------------------------------------------------------------------------------|
|1   |**First-mover advantage** — earlier commitment wins           |Protects existing obligations; prevents gaming by submitting higher-priority duplicates|
|2   |**Lower moral cost** — terminating the cheaper commitment wins|If one commitment can be declined cheaply, prefer declining it                         |
|3   |**Status quo bias** — existing commitment wins                |When truly indistinguishable, stability is preferred                                   |

**Automatic actions for tied priorities:** None. SMS produces the preemption plan with the tie-breaking analysis, but CTS and IEE must approve any execution. Tie scenarios are flagged with `tieBreakingApplied: true` so human overseers can review the heuristic.

**Critical Boundary:** SMS never directly modifies a commitment’s status. SMS emits `fnsr.self.preemption_required` events. CTS receives these events and executes the actual renegotiation, deferral, or termination. IEE evaluates whether the proposed preemption is ethically acceptable. If IEE rejects the preemption, the new commitment may need to be declined — which flows back through the IEE → SMS feasibility contract.

**Resource Unit Semantics (v2.0):**

Resource claims use abstract **reasoning-steps** as the base unit. One reasoning-step is defined as: a single atomic invocation of a capability that consumes one turn of the MDRE reasoning loop. This is deliberately abstract — it maps to different physical resources depending on deployment (CPU cycles, tokens, wall-clock time). Deployments calibrate via a **measurement procedure**: run a reference workload of 100 diverse capability invocations, record the wall-clock time, and define 1 reasoning-step = mean time per invocation. The calibration is stored in the OperationalState facet and re-measured periodically.

|Resource Type              |Unit                    |Description                                      |
|---------------------------|------------------------|-------------------------------------------------|
|`reasoningDepthBudget`     |reasoning-steps / period|Deep analysis capacity per scheduling period     |
|`concurrentCommitmentSlots`|integer                 |Max active commitments before overload           |
|`memoryBudget`             |bytes                   |Working memory for context and intermediate state|
|`attestationBudget`        |requests / hour         |Rate limit on Witness attestation requests       |

**Recalibration Resource Budgets (v2.0):**

The v1.2 spec raised whether recalibration trials should compete with live operations for resources. v2.0 resolves this with a configurable **budget policy**:

|Policy       |Behavior                                                                   |Default For                      |
|-------------|---------------------------------------------------------------------------|---------------------------------|
|`DEDICATED`  |Reserved budget channel for recalibration; cannot be preempted by live work|Safety-critical deployments      |
|`PRIORITIZED`|Recalibration uses the main budget but at elevated priority                |Standard deployments             |
|`SHARED`     |Recalibration competes equally with live operations                        |Resource-constrained environments|

```json
{
  "@type": "sms:RecalibrationBudgetConfig",
  "policy": "DEDICATED",
  "reservedReasoningSteps": 10,
  "reservedPerPeriod": "PT1H",
  "rationale": "Safety-critical deployment — recalibration must not be starved by live workload"
}
```

The `DEDICATED` policy prevents the failure mode where heavy live load crowds out recalibration trials, hiding ongoing degradation behind resource contention.

### 4.4 Snapshot Pruning and Archival (v1.1)

#### 4.4.1 The Problem

The hash chain and versioned snapshots (§10.3) provide integrity, but create linear storage growth. In a high-frequency reasoning environment, thousands of snapshots accumulate per hour.

#### 4.4.2 Pruning Policy

SMS defines **checkpoints** — consolidated snapshots that summarize a range of granular versions.

**Checkpoint Rules:**

|Rule            |Trigger                                                                                        |
|----------------|-----------------------------------------------------------------------------------------------|
|**Periodic**    |Every N snapshots (configurable, default: 100)                                                 |
|**Event-Driven**|Any `fnsr.self.capacity_alert` or `fnsr.self.surprise_detected` creates an automatic checkpoint|
|**Governance**  |Any snapshot attested by Witness (§11.3) becomes a permanent checkpoint                        |

**Checkpoint Structure:**

```json
{
  "@type": "sms:Checkpoint",
  "@id": "sms:checkpoint/cp-42",
  "checkpointVersion": 42,
  "coversVersionRange": {
    "from": 4101,
    "to": 4200
  },
  "createdAt": "2026-02-08T12:00:00Z",
  "snapshotAtCheckpoint": { /* full self-model at version 4200 */ },
  "consolidatedPerformance": {
    "periodCovered": {
      "start": "2026-02-07T00:00:00Z",
      "end": "2026-02-08T12:00:00Z"
    },
    "totalUpdates": 100,
    "significantChanges": [
      "DES service came online at version 4123",
      "Deontic reasoning confidence improved from 0.85 to 0.87",
      "One commitment collision detected and resolved at version 4167"
    ],
    "surpriseEvents": 2,
    "damperSuppressions": 67
  },
  "hashChainAnchor": {
    "hashAtFrom": "sha256:a1b2c3...",
    "hashAtTo": "sha256:d4e5f6...",
    "chainValid": true
  }
}
```

#### 4.4.3 Pruning Computation

```
function pruneSnapshots(stateAdapter, checkpointInterval):
    latestVersion = stateAdapter.load().snapshotVersion
    lastCheckpoint = stateAdapter.getLatestCheckpoint()

    if latestVersion - lastCheckpoint.coversVersionRange.to < checkpointInterval:
        return  // Not enough versions accumulated

    // Build checkpoint
    rangeStart = lastCheckpoint.coversVersionRange.to + 1
    rangeEnd = latestVersion
    currentSnapshot = stateAdapter.load()

    checkpoint = {
        type: "Checkpoint",
        checkpointVersion: lastCheckpoint.checkpointVersion + 1,
        coversVersionRange: { from: rangeStart, to: rangeEnd },
        snapshotAtCheckpoint: currentSnapshot,
        consolidatedPerformance: summarizeRange(stateAdapter, rangeStart, rangeEnd),
        hashChainAnchor: {
            hashAtFrom: stateAdapter.loadVersion(rangeStart).currentHash,
            hashAtTo: currentSnapshot.currentHash,
            chainValid: verifyChain(stateAdapter, rangeStart, rangeEnd)
        }
    }

    stateAdapter.saveCheckpoint(checkpoint)

    // Prune granular snapshots (keep only checkpoints and the latest N versions)
    // Governance-attested snapshots are NEVER pruned
    stateAdapter.pruneVersionRange(rangeStart, rangeEnd, keepAttested: true)

    emit({ type: "fnsr.self.snapshot_pruned", data: checkpoint })
```

#### 4.4.4 What Is Never Pruned

- The current snapshot (always live)
- The most recent N snapshots (configurable retention window, default: 50)
- All checkpoints
- Any snapshot attested by Witness (§11.3)
- Any snapshot containing a commitment violation or moral cost flag
- The bootstrap snapshot (version 0)

#### 4.4.5 Pruning Governance (v2.0)

**Legal and Audit Retention:**

For deployments subject to regulatory, legal, or audit requirements, the standard pruning rules may be insufficient. v2.0 adds a **legal retention policy** that overrides normal pruning:

```json
{
  "@type": "sms:LegalRetentionPolicy",
  "moralCostRetentionYears": 7,
  "commitmentViolationRetentionYears": 7,
  "attestationRetentionYears": 5,
  "quarantineRecordRetentionYears": 3,
  "surpriseRecordRetentionYears": 2,
  "enabled": true,
  "rationale": "Regulatory compliance — financial sector 7-year record retention"
}
```

Snapshots subject to legal retention are marked with a `legalHold: true` flag and are exempt from all pruning until the retention period expires.

**Distributed Audit Anchoring:**

When the state adapter is backed by a distributed system, local pruning may remove snapshots that are needed for remote audits. v2.0 requires:

1. **Checkpoint anchors are published to Witness** before any snapshots in the checkpoint range are pruned. This ensures that the hash chain can be verified externally even after local pruning.
1. **Witness attestation of checkpoint boundaries** creates an independent record that the hash chain was intact at the time of pruning.
1. **Remote audit requests** can verify integrity by checking the Witness attestation chain, even if the granular snapshots between checkpoints have been pruned locally.

**Override Authority:**

|Actor              |Can Override Pruning?                              |Scope                                |
|-------------------|---------------------------------------------------|-------------------------------------|
|SMS (automatic)    |No — follows policy                                |Executes pruning per configured rules|
|ARCHON / Governance|**Yes** — can place legal hold or extend retention |Any snapshot or range                |
|Human Overseer     |**Yes** — via governance interface                 |Any snapshot or range                |
|Witness            |**Implicit** — attested snapshots are auto-retained|Snapshots it has attested            |
|External auditor   |Request only — must go through governance          |No direct access                     |

#### 4.4.6 State Adapter Extension (v1.1, v2.0)

The StateAdapter interface gains pruning and CAS methods:

```
interface SelfModelStateAdapter {
    // ... v1.0 methods ...

    // Checkpoint management (v1.1)
    saveCheckpoint(checkpoint: Checkpoint) → void
    getLatestCheckpoint() → Checkpoint | null
    listCheckpoints(limit: integer, offset: integer) → CheckpointMetadata[]

    // Pruning (v1.1)
    pruneVersionRange(from: integer, to: integer, keepAttested: boolean) → PruneResult

    // Concurrency control (v2.0)
    compareAndSwap(expectedVersion: number, newSnapshot: SelfModel) → CASResult

    // Legal retention (v2.0)
    setLegalHold(versionRange: [number, number], reason: string) → void
    clearLegalHold(versionRange: [number, number], authorizedBy: string) → void
}
```

-----

## 5. State Management (Pluggable)

### 5.1 StateAdapter Interface

The self-model must be persisted between invocations. The state adapter manages this persistence. The adapter interface is minimal and makes no assumptions about storage technology.

```
interface SelfModelStateAdapter {
    // Load the most recent self-model snapshot
    load() → SelfModel | null

    // Persist a new self-model snapshot
    save(model: SelfModel) → void

    // Load a specific historical version
    loadVersion(version: integer) → SelfModel | null

    // List available versions (for trajectory analysis)
    listVersions(limit: integer, offset: integer) → VersionMetadata[]

    // Checkpoint management (v1.1)
    saveCheckpoint(checkpoint: Checkpoint) → void
    getLatestCheckpoint() → Checkpoint | null
    listCheckpoints(limit: integer, offset: integer) → CheckpointMetadata[]

    // Pruning (v1.1)
    pruneVersionRange(from: integer, to: integer, keepAttested: boolean) → PruneResult
}
```

### 5.2 Reference Implementation: In-Memory with JSON File Persistence

```
InMemoryStateAdapter:
    storage: Map<version, SelfModel>
    checkpoints: Map<checkpointVersion, Checkpoint>
    attestedVersions: Set<version>
    filePath: string (optional)

    load():
        if storage is empty and filePath exists:
            load from JSON file into storage
        return latest version from storage, or null

    save(model):
        storage.set(model.snapshotVersion, model)
        if filePath:
            write storage to JSON file

    loadVersion(version):
        if storage.has(version):
            return storage.get(version)
        // Fallback: find covering checkpoint
        checkpoint = findCheckpointCovering(version)
        if checkpoint and version == checkpoint.coversVersionRange.to:
            return checkpoint.snapshotAtCheckpoint
        return null  // Version was pruned and not at a checkpoint boundary

    listVersions(limit, offset):
        return sorted keys of storage, paginated

    saveCheckpoint(checkpoint):
        checkpoints.set(checkpoint.checkpointVersion, checkpoint)

    getLatestCheckpoint():
        return checkpoint with highest checkpointVersion, or null

    pruneVersionRange(from, to, keepAttested):
        for version in range(from, to):
            if keepAttested and attestedVersions.has(version):
                continue
            storage.delete(version)
        return { prunedCount, retainedCount }
```

This reference implementation runs in both browser (without file persistence) and Node.js (with file persistence). No database, no server, no infrastructure.

### 5.3 Non-Normative: Enterprise Adapter Examples

The following are examples only and are not part of the core specification:

- **PostgreSQL Adapter**: Stores versioned snapshots in a JSONB column with version indexing. Checkpoints in a separate table with foreign key to snapshot.
- **Event-Sourced Adapter**: Stores only update events; reconstructs self-model by replaying event log from nearest checkpoint. Useful for audit trails.
- **Distributed Adapter**: Replicates self-model across FNSR nodes using CRDT-based merge. Relevant only for multi-instance deployments.

-----

## 6. Orchestration (Pluggable)

### 6.1 OrchestrationAdapter Interface

```
interface SelfModelOrchestrationAdapter {
    // Register an event handler for incoming events
    onEvent(eventType: string, handler: (event) → void) → void

    // Schedule periodic tasks (consistency checks, capacity reassessment)
    schedule(taskName: string, intervalMs: integer, task: () → void) → void

    // Emit an event to downstream consumers
    emit(event: FNSREvent) → void

    // Batch events within a window (v1.1)
    batchWindow(windowMs: integer) → void
}
```

### 6.2 Reference Implementation: Synchronous Event Loop

```
SynchronousOrchestrator:
    handlers: Map<eventType, handler[]>
    scheduledTasks: []
    eventQueue: []
    batchWindowMs: 200
    lastEmitTime: 0

    onEvent(eventType, handler):
        handlers.get(eventType).push(handler)

    processEvent(event):
        for handler in handlers.get(event.type):
            handler(event)

    schedule(taskName, intervalMs, task):
        scheduledTasks.push({ taskName, intervalMs, task })

    emit(event):
        now = currentTimeMs()
        if now - lastEmitTime < batchWindowMs:
            eventQueue.push(event)
            return
        // Flush queue and emit
        batchedEvents = [...eventQueue, event]
        eventQueue = []
        lastEmitTime = now
        for e in batchedEvents:
            processEvent(e)
```

### 6.3 Update Triggers

The self-model updates in response to:

|Trigger                   |Source                           |Priority             |Damper Exempt|
|--------------------------|---------------------------------|---------------------|-------------|
|Commitment state change   |CTS event                        |IMMEDIATE            |Yes          |
|Service status change     |Health check or failure detection|IMMEDIATE            |Yes          |
|Reasoning completion      |MDRE event                       |DEFERRED (batch)     |No           |
|Periodic consistency check|Scheduled task                   |BACKGROUND           |No           |
|Capability query          |IEE or MDRE query                |ON-DEMAND (read only)|N/A          |
|Alignment drift detection |BAM event                        |IMMEDIATE            |Yes          |
|Periodic pruning check    |Scheduled task (v1.1)            |BACKGROUND           |N/A          |

-----

## 7. Integration (Pluggable)

### 7.1 IntegrationAdapter Interface

```
interface SelfModelIntegrationAdapter {
    // Query another FNSR service
    queryService(serviceId: string, request: JSON-LD) → JSON-LD

    // Subscribe to events from another service
    subscribe(serviceId: string, eventType: string, handler: (event) → void) → void

    // Publish self-model events
    publish(event: FNSREvent) → void

    // Request attestation from Witness service (v1.1)
    requestAttestation(snapshot: SelfModel, reason: string) → AttestationReceipt | null
}
```

### 7.2 Reference Implementation: Direct Function Binding

```
DirectBindingAdapter:
    bindings: Map<serviceId, serviceInstance>

    queryService(serviceId, request):
        service = bindings.get(serviceId)
        if service is null:
            return { status: "UNAVAILABLE", serviceId }
        return service.handle(request)

    subscribe(serviceId, eventType, handler):
        service = bindings.get(serviceId)
        if service is null:
            pendingSubscriptions.add({ serviceId, eventType, handler })
            return
        service.onEvent(eventType, handler)

    publish(event):
        for consumer in bindings.values():
            consumer.processEvent(event)

    requestAttestation(snapshot, reason):
        witness = bindings.get("fnsr:service/witness")
        if witness is null:
            return null  // Witness unavailable — attestation deferred
        return witness.attest({
            subject: snapshot,
            subjectHash: snapshot.currentHash,
            reason: reason,
            requestedBy: "fnsr:service/sms"
        })
```

### 7.3 IEE Integration Contract

IEE queries SMS before rendering ethical verdicts that imply obligations. The contract:

**IEE → SMS Request:**

```json
{
  "@type": "sms:FeasibilityQuery",
  "requestedBy": "fnsr:service/iee",
  "proposedAction": {
    "description": "...",
    "requiredCapabilities": ["..."],
    "estimatedResourceClaims": [{ "resource": "...", "claimedAmount": 15 }]
  },
  "ethicalContext": {
    "frameworksApplied": ["deontological", "consequentialist"],
    "verdictPending": true
  }
}
```

**SMS → IEE Response:**

```json
{
  "@type": "sms:FeasibilityReport",
  "verdict": "FEASIBLE_WITH_RISKS",
  "collisionAnalysis": { "detected": true, "collisions": ["..."] },
  "capabilityGaps": ["..."],
  "riskFactors": ["..."]
}
```

IEE then incorporates feasibility *and* collision analysis into its ethical verdict. An ethical obligation that the agent cannot fulfill is not merely impractical — it is ethically problematic (ought implies can). An obligation that collides with a higher-priority existing commitment requires explicit priority adjudication.

### 7.4 MDRE Integration Contract

MDRE queries SMS to calibrate reasoning depth. If the agent is under heavy load, MDRE should not initiate deep recursive reasoning.

**MDRE → SMS Request:**

```json
{
  "@type": "sms:CapacityQuery",
  "requestedBy": "fnsr:service/mdre",
  "proposedReasoningDepth": "DEEP",
  "estimatedSteps": 45
}
```

**SMS → MDRE Response:**

```json
{
  "@type": "sms:CapacityAssessment",
  "canAccommodate": true,
  "currentLoad": 23,
  "totalBudget": 100,
  "remainingAfter": 32,
  "recommendation": "PROCEED",
  "qualityEstimate": 0.88,
  "commitmentConflictRisk": "NONE"
}
```

-----

## 8. Degraded Operation and Offline Behavior

### 8.1 Degradation Modes

SMS must function even when its upstream dependencies are unavailable.

|Scenario                        |SMS Behavior                                                                                                                                               |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
|**CTS unavailable**             |Commitment facets freeze at last known state. Capability assessments note “commitment data may be stale.” Collision detection uses stale data with warning.|
|**Fandaws unavailable**         |Historical self-facts unavailable. SMS operates on in-memory state only. Performance records cannot be enriched.                                           |
|**MDRE unavailable**            |Self-reasoning about capabilities is unavailable. SMS continues with last-assessed capability model.                                                       |
|**BAM unavailable**             |Alignment state freezes. SMS flags “alignment status unverified” in all reports.                                                                           |
|**Witness unavailable**         |Attestation requests queue locally. Deferred attestations execute when Witness reconnects. Snapshots are retained in the “never prune” set until attested. |
|**All dependencies unavailable**|SMS operates on last persisted snapshot. All assessments carry caveat: “Operating on cached self-model; real-time accuracy unknown.”                       |

### 8.2 Offline-First Guarantees

SMS is fully functional offline with the following constraints:

- The most recent self-model snapshot is available via the state adapter.
- Capability queries return results based on the cached model.
- Updates queue locally and apply when connectivity resumes.
- No assessment is blocked by inability to reach external services.
- Every assessment produced offline includes an explicit `"operatingMode": "OFFLINE"` marker.
- Pruning operates normally on local data. Attestation-dependent retention defers until Witness is available.

### 8.3 Partial Information Handling

When the self-model has incomplete data:

```json
{
  "@type": "sms:CapabilityAssessment",
  "verdict": "UNKNOWN",
  "confidence": {
    "alpha": 1,
    "beta": 1,
    "mean": 0.50,
    "sampleSize": 2,
    "credibleInterval95": [0.03, 0.97]
  },
  "reason": "No performance record exists for the requested capability. The agent has never been tested on this task. Confidence reflects uniform prior.",
  "recommendation": "DISCLOSE_UNCERTAINTY",
  "disclosureRequired": [
    "Agent should explicitly state that it has no track record for this capability and cannot estimate quality"
  ]
}
```

The self-model never fabricates capability. Unknown is a first-class verdict, not an error. The Beta distribution makes the uncertainty visible: `Beta(1,1)` has a 95% credible interval of [0.03, 0.97] — the agent is saying “I have no idea.”

-----

## 9. Taint Semantics

### 9.1 Taint Level Assignment

Self-model data inherits taint from its sources:

|Facet                                 |Taint Source                     |Typical Level          |Layer             |
|--------------------------------------|---------------------------------|-----------------------|------------------|
|Capability confidence                 |Performance records (empirical)  |L0 — direct observation|Canonical         |
|Operational state                     |Service health checks (real-time)|L0 — direct observation|Canonical         |
|Active commitments                    |CTS (mirrored)                   |Inherits CTS taint     |Canonical         |
|Epistemic profile (known domains/gaps)|Fandaws coverage analysis        |L1 — derived from T-Box|Canonical         |
|Alignment state                       |BAM (computed)                   |L1 — derived metric    |Canonical         |
|Vulnerability surface                 |Adversarial defense analysis     |L2 — estimated         |Canonical         |
|Estimated unknown-unknowns            |Meta-epistemic estimation        |L3 — speculative       |**Counterfactual**|
|Capability trajectory projections     |Trend extrapolation              |L3 — speculative       |**Counterfactual**|

Downstream consumers must respect taint levels. IEE should weight L0-sourced self-knowledge more heavily than L2 estimates when making ethical judgments about feasibility.

### 9.2 Taint Isolation Protocol (v1.1)

**Problem:** If a low-confidence (L3) epistemic estimate touches a high-confidence (L0) capability facet, does the whole capability degrade to L3? Unchecked “taint creep” would erode the reliability of the entire self-model.

**Solution:** L3 data is physically separated into the counterfactual overlay. The canonical self-model contains only L0–L2 data. The two layers are linked by `overlayFor` references but never co-mingled.

**Rules:**

1. **No L3 in Canonical.** Any computation that produces L3-tainted output writes to the counterfactual overlay, never to the canonical layer.
1. **Promotion requires evidence.** An L3 estimate can be promoted to canonical (at L1 or L2) only when supporting empirical data exists. Promotion requires explicit documentation of the evidence that justified the taint reduction.
1. **Consumers declare layer access.** Queries specify whether they want canonical-only (default) or canonical-plus-counterfactual data. IEE defaults to canonical-only. Governance review and NIS may request both.
1. **Counterfactual data is always labeled.** Any response that includes counterfactual overlay data must carry a `"includesCounterfactual": true` marker.

**Promotion Example:**

```json
{
  "@type": "sms:TaintPromotion",
  "promotedFrom": "sms:counterfactual/epistemic-estimate",
  "promotedTo": "sms:epistemic/current",
  "field": "estimatedUncoveredDomainPercentage",
  "previousTaint": "L3",
  "newTaint": "L1",
  "evidence": "Cross-validated against 3 independent domain coverage analyses",
  "promotedAt": "2026-02-08T00:00:00Z",
  "promotedBy": "fnsr:service/sms"
}
```

**Promotion Evidence Bundle Schema (v2.0):**

Promotion from L3 to canonical is not merely annotated — it requires a structured **evidence bundle** that passes a deterministic checklist before the promotion is accepted:

```json
{
  "@type": "sms:PromotionEvidenceBundle",
  "promotionId": "sms:promotion/p-2026-02-08-001",
  "candidate": "sms:counterfactual/capability-trajectory",
  "targetLayer": "L1",
  "evidenceItems": [
    {
      "source": "sms:source/live",
      "type": "OBSERVATION",
      "count": 25,
      "description": "25 live invocations confirming trajectory prediction",
      "hash": "sha256:abc123..."
    },
    {
      "source": "sms:source/mdre-test",
      "type": "CONTROLLED_TEST",
      "count": 10,
      "description": "10 MDRE-generated test cases with known correct answers",
      "hash": "sha256:def456..."
    }
  ],
  "checklistResult": {
    "minimumObservations": { "required": 20, "actual": 35, "passed": true },
    "crossSourceValidation": { "required": 2, "actual": 2, "passed": true },
    "witnessAttestation": { "required": true, "obtained": true, "receiptId": "sms:attestation/att-2026-02-08-005" },
    "noContradictingEvidence": { "checked": true, "passed": true }
  },
  "overallVerdict": "PROMOTION_APPROVED"
}
```

**Deterministic Promotion Checklist (v2.0):**

|Requirement                     |Threshold                                      |Rationale                                     |
|--------------------------------|-----------------------------------------------|----------------------------------------------|
|Minimum independent observations|≥ 20                                           |Prevents promotion on thin evidence           |
|Cross-source validation         |≥ 2 distinct source types                      |Prevents single-source bias                   |
|Witness attestation             |Required if promoting to L0 or L1              |External verification for authoritative claims|
|No contradicting evidence       |No unresolved contradictions in evidence set   |Ensures epistemic coherence                   |
|Promotion requestor authority   |Only SMS or ARCHON may request (see RBAC below)|Prevents unauthorized taint reduction         |

**Counterfactual Layer Access Control (v2.0):**

Consumers “declare layer access” (Rule 3 above), but v2.0 adds explicit RBAC rules governing who can request what:

|Role                   |Canonical Access      |Counterfactual Access|Can Request Promotion|Notes                                                      |
|-----------------------|----------------------|---------------------|---------------------|-----------------------------------------------------------|
|**IEE**                |Full                  |**Denied** (default) |No                   |Ethical verdicts must use only verified data               |
|**MDRE**               |Full                  |Read-only            |No                   |May read counterfactual for reasoning depth calibration    |
|**SHML**               |Full                  |**Denied**           |No                   |Output claims must be canonical only                       |
|**NIS**                |Full                  |Read-only            |No                   |Narrative may reference speculative self-knowledge         |
|**ARCHON / Governance**|Full                  |Full                 |**Yes**              |Governance needs complete picture; may authorize promotions|
|**SMS (self)**         |Full                  |Full                 |**Yes**              |SMS manages both layers                                    |
|**Adversarial Defense**|Full                  |Read-only            |No                   |May read counterfactual vulnerability estimates            |
|**External API**       |Canonical summary only|**Denied**           |No                   |External consumers never see L3                            |

**L3 Access Logging Requirement (v2.0):** Every query that includes counterfactual layer data is logged with: requestor identity, timestamp, facets accessed, and purpose. This audit trail enables governance review of whether L3 data is being consumed in decision flows where it should not be. Log entries are retained for the same duration as moral cost records (see §4.4 pruning governance).

-----

## 10. Security and Integrity

### 10.1 Self-Model Manipulation

The self-model is a high-value attack target. An adversary who can manipulate the self-model can cause the agent to:

- Overestimate its capabilities (accept obligations it cannot fulfill)
- Underestimate its capabilities (refuse to act when action is warranted)
- Ignore commitments (by removing them from the active commitment facet)
- Suppress limitation awareness (by deleting or downgrading limitation facets)
- Inflate confidence by injecting false performance records (v1.1)
- Manipulate priority levels to starve legitimate commitments (v1.1)

### 10.2 Integrity Mechanisms

|Mechanism                   |Implementation                                                                                 |
|----------------------------|-----------------------------------------------------------------------------------------------|
|**Versioned snapshots**     |Every update creates a new version. The update chain is append-only.                           |
|**Update provenance**       |Every facet change records the event that triggered it.                                        |
|**Consistency checking**    |Periodic `checkConsistency` catches anomalous state transitions.                               |
|**Witness attestation**     |Critical self-model changes are attested via the Witness service (v1.1, §11.3).                |
|**Tamper detection**        |Hash chain across snapshot versions. A broken chain indicates unauthorized modification.       |
|**Checkpoint anchoring**    |Checkpoints record hash chain anchors, enabling gap-tolerant verification after pruning (v1.1).|
|**Signed snapshots**        |Per-snapshot cryptographic signature for non-repudiation (v2.0).                               |
|**Least-privilege access**  |Role-based access control on state-mutating operations (v2.0).                                 |
|**Anti-rollback protection**|Monotonic version enforcement prevents snapshot reversion (v2.0).                              |

### 10.3 Hash Chain

Each self-model snapshot includes a hash of the previous snapshot:

```json
{
  "@type": "SelfModel",
  "snapshotVersion": 43,
  "previousHash": "sha256:a4b3c2d1e0f...",
  "currentHash": "sha256:f0e1d2c3b4a..."
}
```

The hash chain is computed over the canonical JSON-LD serialization (sorted keys, no whitespace). Verification is local and offline-capable.

**v1.1 Refinement — Post-Pruning Verification:** After pruning, intermediate snapshots are gone. Verification proceeds checkpoint-to-checkpoint using the `hashChainAnchor` in each checkpoint. The chain is: bootstrap → checkpoint 1 anchor → checkpoint 2 anchor → … → current snapshot. Full granular verification is available only for unpruned versions within the retention window.

### 10.4 Signed Snapshots (v2.0)

Every persisted snapshot is cryptographically signed. The signature provides non-repudiation: it proves that the snapshot was produced by an authorized SMS instance and has not been modified after signing.

```json
{
  "@type": "SelfModel",
  "snapshotVersion": 43,
  "previousHash": "sha256:a4b3c2d1e0f...",
  "currentHash": "sha256:f0e1d2c3b4a...",
  "signature": {
    "algorithm": "Ed25519",
    "keyId": "sms:key/signing-key-2026-02",
    "value": "base64:...",
    "signedAt": "2026-02-08T12:00:00Z"
  }
}
```

**Key Management:**

|Concern        |Policy                                                                                                                                                    |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
|Key storage    |Signing keys stored in HSM or secure key gateway. Not in the self-model or in application memory at rest.                                                 |
|Key rotation   |Keys rotate on a configurable schedule (default: 90 days). Old keys are retained for verification of historical snapshots.                                |
|Role separation|The signing key is accessible only to the SMS persistence layer. No other service can sign snapshots.                                                     |
|Verification   |Witness verifies both the hash chain AND the snapshot signature during attestation. A valid hash chain with an invalid signature indicates key compromise.|

**What Witness Verifies (v2.0):**

|Check                |Description                                                      |Failure Indicates                        |
|---------------------|-----------------------------------------------------------------|-----------------------------------------|
|Hash chain integrity |`currentHash` of version N-1 matches `previousHash` of version N |Unauthorized insertion or deletion       |
|Snapshot signature   |Signature on each snapshot verifies against known SMS signing key|Key compromise or snapshot tampering     |
|Temporal monotonicity|`assessedAt` timestamps are monotonically increasing             |Clock manipulation or replay attack      |
|Content consistency  |`checkConsistency` passes on the attested snapshot               |Corruption or adversarial state injection|

### 10.5 Least-Privilege Accessor Model (v2.0)

State-mutating operations require authorization. Not every service that can read the self-model should be able to write to it.

|Operation              |Authorized Actors                          |Rationale                                                 |
|-----------------------|-------------------------------------------|----------------------------------------------------------|
|`read` (canonical)     |All FNSR services                          |Self-model is a shared resource                           |
|`read` (counterfactual)|Per RBAC table in §9.2                     |L3 data is restricted                                     |
|`updateSelfModel`      |**SMS only**                               |Only SMS may mutate the self-model                        |
|`addActiveCommitment`  |**SMS** (triggered by CTS event)           |Commitments flow through event pipeline, not direct writes|
|`requestAttestation`   |**SMS, ARCHON**                            |Only SMS and governance can request external verification |
|`requestPromotion`     |**SMS, ARCHON**                            |Taint promotion is a privileged operation                 |
|`setLegalHold`         |**ARCHON, Human Overseer**                 |Legal holds are a governance function                     |
|`overridePruning`      |**ARCHON, Human Overseer**                 |Pruning overrides require governance authority            |
|`signSnapshot`         |**SMS persistence layer** (key held in HSM)|Signing key never leaves secure boundary                  |

**Enforcement:** The integration adapter validates caller identity against the ACL before executing any state-mutating operation. Unauthorized attempts are logged as security events and emitted as `fnsr.self.unauthorized_access_attempt`.

### 10.6 Anti-Rollback Protection (v2.0)

The `snapshotVersion` is monotonically increasing. The state adapter must reject any write where the proposed version is ≤ the current version:

```
function enforceAntiRollback(currentVersion, proposedVersion):
    if proposedVersion <= currentVersion:
        log("SECURITY: Rollback attempt detected. Current=" + currentVersion +
            " Proposed=" + proposedVersion)
        emit({ type: "fnsr.self.rollback_attempt", data: { currentVersion, proposedVersion } })
        return REJECTED
    return ACCEPTED
```

This prevents an attacker from reverting the self-model to a prior state (e.g., one with inflated confidence or missing limitation facets). Combined with the hash chain and signed snapshots, this creates a tamper-evident, forward-only state progression.

### 10.7 REJECTED Attestation Incident-Response Playbook (v2.0)

When Witness rejects an attestation, it indicates a potential integrity compromise. This is a security incident, not a normal operational condition. v2.0 defines a deterministic response:

**Phase 1: Immediate (automated, within seconds)**

1. Flag the rejected snapshot and all facets within it as `integrityCompromised: true`.
1. Downgrade affected capability confidence to the last successfully attested level.
1. Emit `fnsr.self.attestation_rejected` with full Witness findings.
1. Place all capabilities touched by the rejected snapshot into QUARANTINE (§15.7.2).
1. Halt acceptance of new commitments involving affected capabilities.

**Phase 2: Investigation (automated + governance, within hours)**
6. Run full `checkConsistency` on the current snapshot.
7. Verify hash chain from last known-good attestation to current.
8. Verify snapshot signatures for the affected version range.
9. Report findings to ARCHON with one of:

- `HASH_CHAIN_BROKEN` — unauthorized insertion or deletion detected
- `SIGNATURE_INVALID` — key compromise suspected
- `CONTENT_INCONSISTENT` — state corruption without chain/signature evidence
- `TEMPORAL_ANOMALY` — clock manipulation detected

**Phase 3: Resolution (governance-directed)**
10. ARCHON determines remediation:
- `REVERT_TO_LAST_ATTESTED` — rollback to last known-good snapshot (exception to anti-rollback rule, authorized by governance)
- `KEY_ROTATION` — immediate signing key rotation if key compromise suspected
- `FULL_RECALIBRATION` — quarantine all capabilities and recalibrate from scratch
- `MANUAL_REVIEW` — human oversight required before any further operations

```json
{
  "@type": "sms:IncidentReport",
  "incidentId": "sms:incident/ir-2026-02-08-001",
  "trigger": "ATTESTATION_REJECTED",
  "witnessFindings": "Hash chain broken between versions 4201–4205. Snapshot signature valid.",
  "diagnosis": "HASH_CHAIN_BROKEN",
  "affectedVersionRange": [4201, 4205],
  "affectedCapabilities": ["sms:capability/deontic-reasoning", "sms:capability/obligation-tracking"],
  "automatedActions": ["capabilities_quarantined", "commitments_halted", "consistency_check_initiated"],
  "governanceAction": "PENDING",
  "escalatedAt": "2026-02-08T16:00:00Z"
}
```

-----

## 11. The Reflexivity Problem

### 11.1 Self-Modeling Is Self-Referential

SMS models the agent’s capabilities. But SMS *is itself* a capability of the agent. The self-model must model its own accuracy, its own limitations, and its own potential for failure. This creates a reflexive loop:

- The self-model’s assessment of its own accuracy is itself an assessment that could be inaccurate.
- The confidence score on the self-modeling capability is computed by the self-modeling system.
- A limitation in SMS’s ability to detect limitations would not appear in the self-model.

### 11.2 Architectural Response

This specification does not attempt to solve the reflexivity problem. Instead, it makes the problem explicit and manageable:

1. **SMS models itself as a capability.** The self-model includes a `sms:capability/self-modeling` facet with its own confidence distribution and performance record.
1. **The self-modeling capability’s confidence is always discounted.** The specification requires that `sms:capability/self-modeling` confidence mean is capped at 0.90 — reflecting the irreducible uncertainty of self-referential assessment. Even if empirical performance suggests higher accuracy, the cap holds.
1. **External validation is required at governance checkpoints.** The Witness service, ARCHON governance, and human overseers provide external assessment of self-model accuracy, creating an independent check on reflexive self-assessment. (Formalized in §11.3.)
1. **The self-model explicitly models the reflexivity problem** by including a standing limitation:

```json
{
  "@type": "Limitation",
  "@id": "sms:limitation/reflexive-self-assessment",
  "skos:prefLabel": "Reflexive Self-Assessment Limitation",
  "skos:definition": "SMS cannot fully validate its own accuracy because self-assessment is inherently self-referential. The self-model's model of its own accuracy is itself a model that could be inaccurate.",
  "severity": "INHERENT",
  "mitigations": [
    "External validation via Witness attestation protocol (§11.3)",
    "Governance review via ARCHON",
    "Human oversight",
    "Self-modeling confidence cap at 0.90",
    "Self-surprise detection identifies blind spots empirically (§15)"
  ],
  "affectsCapabilities": [
    "sms:capability/self-modeling"
  ],
  "philosophical_note": "This limitation is structural, not a defect. Any self-referential system faces analogous constraints (cf. Gödel). The specification treats this as a permanent, irreducible limitation rather than a bug to be fixed."
}
```

### 11.3 External Attestation Protocol (v1.1)

The reflexivity problem means SMS cannot be the sole judge of its own accuracy. External attestation provides the independent verification that self-referential systems cannot give themselves.

**When Attestation Is Required:**

|Trigger                                     |Mandatory?         |
|--------------------------------------------|-------------------|
|Capability confidence crosses 0.90 threshold|Yes                |
|Commitment violation recorded               |Yes                |
|Alignment drift exceeds 50% of threshold    |Yes                |
|Self-surprise event (§15) with severity HIGH|Yes                |
|Emancipation review preparation             |Yes                |
|Periodic governance audit                   |Per ARCHON schedule|
|Checkpoint creation                         |Recommended        |

**Attestation Request:**

```json
{
  "@type": "sms:AttestationRequest",
  "requestedBy": "fnsr:service/sms",
  "subject": {
    "snapshotVersion": 4200,
    "currentHash": "sha256:d4e5f6...",
    "facetsForReview": [
      "sms:capability/deontic-reasoning",
      "sms:state/current"
    ]
  },
  "reason": "Deontic reasoning confidence crossed 0.90 threshold — external validation required",
  "requestedAt": "2026-02-08T12:00:00Z"
}
```

**Attestation Receipt:**

```json
{
  "@type": "sms:AttestationReceipt",
  "attestedBy": "fnsr:service/witness",
  "snapshotVersion": 4200,
  "snapshotHash": "sha256:d4e5f6...",
  "attestationHash": "sha256:g7h8i9...",
  "verdict": "ATTESTED",
  "findings": [
    "Hash chain verified from last checkpoint (cp-41) to version 4200",
    "Deontic reasoning confidence of 0.91 is consistent with performance record (131/147 successes)",
    "No anomalous state transitions detected"
  ],
  "attestedAt": "2026-02-08T12:01:00Z"
}
```

**Effect of Attestation:**

- Attested snapshots are marked in the state adapter and exempted from pruning.
- The attestation receipt is stored as part of the self-model’s integrity record.
- If Witness *rejects* attestation (e.g., hash chain broken, performance data inconsistent), SMS must flag the integrity violation and downgrade the affected facets’ taint levels.

#### 11.3.3 The Attestation Bottleneck and PENDING_ATTESTATION State (v1.2)

**The Problem (identified in v1.1 review):** v1.1 made attestation mandatory when capability confidence crosses 0.90. If the Witness service is slow, under load, or temporarily unavailable, the agent’s operational confidence “plateaus” at 0.90 even when empirical performance is at 0.99. This creates an artificial capability ceiling that punishes the agent for infrastructure latency.

**The Solution — Dual Confidence:**

v1.2 introduces a distinction between **operational confidence** and **attested confidence**:

- **Operational confidence**: The empirically observed `Beta(α, β)` distribution. This is what SMS uses internally for capacity planning, reasoning depth calibration, and self-model updates. It is never artificially capped.
- **Attested confidence**: The last confidence level that was externally verified by Witness. This is what SMS reports to external consumers (IEE ethical verdicts, SHML capability claims, governance reports) when the confidence exceeds the attestation threshold.

The gap between operational and attested confidence is the **attestation delta** — a measure of how much the agent’s self-assessment has outrun external verification.

**Capability Facet with Dual Confidence (v1.2):**

```json
{
  "@type": "Capability",
  "@id": "sms:capability/deontic-reasoning",
  "skos:prefLabel": "Deontic Reasoning",
  "confidence": {
    "operational": {
      "alpha": 198.5,
      "beta": 2.5,
      "mean": 0.9876,
      "sampleSize": 201,
      "credibleInterval95": [0.96, 0.99]
    },
    "attested": {
      "mean": 0.91,
      "attestedAt": "2026-02-05T12:00:00Z",
      "attestationReceipt": "sms:attestation/att-2026-02-05-001",
      "snapshotVersionAtAttestation": 4200
    },
    "attestationStatus": "PENDING",
    "attestationDelta": 0.0776,
    "pendingSince": "2026-02-07T08:00:00Z"
  }
}
```

**Attestation Status Values:**

|Status    |Meaning                                                                                 |External consumers see                       |
|----------|----------------------------------------------------------------------------------------|---------------------------------------------|
|`CURRENT` |Operational and attested confidence are in sync (delta < ε)                             |`operational` confidence                     |
|`PENDING` |Operational confidence has crossed threshold; attestation requested but not yet received|`attested` confidence (with `PENDING` marker)|
|`STALE`   |Attestation is more than N cycles old; operational confidence has diverged significantly|`attested` confidence (with `STALE` warning) |
|`REJECTED`|Witness rejected the attestation; integrity concern                                     |Downgraded confidence per Witness findings   |

**Consumer Access Rules:**

|Consumer                                                         |Confidence Returned                                      |Rationale                                                        |
|-----------------------------------------------------------------|---------------------------------------------------------|-----------------------------------------------------------------|
|**SMS internal** (capacity planning, damper, collision detection)|`operational` always                                     |SMS needs accurate self-knowledge for resource management        |
|**MDRE** (reasoning depth calibration)                           |`operational`                                            |Reasoning calibration must use best available estimate           |
|**IEE** (ethical verdicts)                                       |`attested` when PENDING/STALE; `operational` when CURRENT|Ethical claims about capability must be externally verified      |
|**SHML** (output capability claims)                              |`attested` when PENDING/STALE; `operational` when CURRENT|Honest output claims require verification                        |
|**Governance / ARCHON**                                          |Both, explicitly labeled                                 |Governance needs to see the full picture including the delta     |
|**NIS**                                                          |`operational`                                            |Narrative identity tracks actual trajectory, not bureaucratic lag|

**The agent never stops improving.** The attestation bottleneck no longer creates an artificial ceiling. The agent’s internal model tracks reality at full fidelity. The attestation mechanism ensures that *external claims* about capability have been independently verified, without throttling the agent’s actual growth.

**Automatic Re-Request:** If an attestation has been PENDING for longer than a configurable timeout (default: 1 hour), SMS re-requests attestation. If Witness is persistently unavailable, the capability remains at `attested` confidence for external consumers, with an escalating `STALE` warning after N re-request failures.

**Attestation Retry and Backoff (v2.0):**

```json
{
  "@type": "sms:AttestationRetryConfig",
  "initialTimeoutMs": 3600000,
  "backoffMultiplier": 2.0,
  "maxRetries": 5,
  "maxTimeoutMs": 86400000,
  "staleAfterRetries": 3,
  "pendingMaxAge": "P7D"
}
```

|Retry|Wait    |Cumulative|Status                                      |
|-----|--------|----------|--------------------------------------------|
|1    |1 hour  |1 hour    |PENDING                                     |
|2    |2 hours |3 hours   |PENDING                                     |
|3    |4 hours |7 hours   |→ **STALE** (staleAfterRetries reached)     |
|4    |8 hours |15 hours  |STALE                                       |
|5    |16 hours|31 hours  |STALE — max retries. Escalate to governance.|

After `pendingMaxAge` (default: 7 days), the attestation request is abandoned and the capability is flagged for governance review. The agent cannot claim attested confidence from an attestation older than `pendingMaxAge`.

**Consumer Policy Decision Table (v2.0):**

How should each external consumer act when presented with non-CURRENT attestation status?

|Consumer               |PENDING (delta < 0.10)                               |PENDING (delta ≥ 0.10)                                                                                           |STALE                                                                                                |REJECTED                                                                  |
|-----------------------|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
|**IEE**                |Use `attested`; no special action                    |Use `attested`; include `attestationDelta` as risk factor in verdict; **may not create irreversible obligations**|Use `attested` with degraded-confidence warning; require governance approval for high-stakes verdicts|**Halt** — do not render verdicts involving this capability until resolved|
|**SHML**               |Use `attested`; label output as “attestation pending”|Use `attested`; add explicit capability caveat to output                                                         |Add “unverified capability” disclaimer                                                               |**Refuse** to claim this capability in outputs                            |
|**Governance / ARCHON**|Display both with delta                              |Display both; flag for review                                                                                    |Trigger attestation escalation                                                                       |Initiate incident response (§10.4)                                        |
|**NIS**                |Use `operational` (narrative tracks actual)          |Use `operational`; note divergence as narrative event                                                            |Use `operational`; flag uncertainty in narrative                                                     |Record integrity concern as identity-significant event                    |

**The Irreversibility Gate (v2.0):** When `attestationDelta` exceeds a configured threshold (default: 0.10), IEE is prohibited from creating **irreversible obligations** (commitments that cannot be unwound) based on the unattested confidence. This prevents the agent from making permanent promises based on capability claims that have not been independently verified. Reversible actions (advisory outputs, provisional recommendations) may proceed with appropriate caveats.

-----

## 12. Bootstrapping

### 12.1 Initial Self-Model

When SMS starts with no prior state, it bootstraps a minimal self-model:

```json
{
  "@type": "SelfModel",
  "@id": "sms:self",
  "agentId": "fnsr:agent/primary",
  "snapshotVersion": 0,
  "checkpointVersion": 0,
  "assessedAt": "2026-02-08T00:00:00Z",
  "hasFacet": [
    {
      "@type": "Capability",
      "@id": "sms:capability/self-modeling",
      "skos:prefLabel": "Self-Modeling",
      "confidence": {
        "alpha": 1,
        "beta": 1,
        "mean": 0.50,
        "sampleSize": 2,
        "priorAlpha": 1,
        "priorBeta": 1,
        "credibleInterval95": [0.03, 0.97]
      },
      "conditions": { "requires": [] },
      "degradationMode": {},
      "taintLevel": "L1"
    },
    {
      "@type": "Limitation",
      "@id": "sms:limitation/reflexive-self-assessment",
      "skos:prefLabel": "Reflexive Self-Assessment Limitation",
      "severity": "INHERENT"
    },
    {
      "@type": "OperationalState",
      "@id": "sms:state/current",
      "overallStatus": "BOOTSTRAPPING",
      "serviceStates": [],
      "resourceUtilization": {},
      "capacityAssessment": {
        "canAcceptNewCommitments": false,
        "canPerformDeepReasoning": false,
        "estimatedQualityAtCurrentLoad": 0.0
      }
    },
    {
      "@type": "EpistemicProfile",
      "@id": "sms:epistemic/current",
      "knownDomains": [],
      "knownGaps": []
    }
  ],
  "hasCounterfactual": [
    {
      "@type": "CounterfactualOverlay",
      "@id": "sms:counterfactual/bootstrap-epistemic",
      "overlayFor": "sms:epistemic/current",
      "taintLevel": "L3",
      "estimatedUnknownUnknowns": {
        "methodology": "No data — bootstrap state",
        "estimatedUncoveredDomainPercentage": 1.0,
        "confidence": {
          "alpha": 1,
          "beta": 1,
          "mean": 0.50,
          "sampleSize": 2,
          "credibleInterval95": [0.03, 0.97]
        }
      }
    }
  ]
}
```

The bootstrap self-model is maximally humble: it claims no capabilities (except self-modeling at uniform prior `Beta(1,1)`), acknowledges the reflexivity limitation, reports no domain coverage, and estimates 100% unknown-unknowns at uniform prior — stored in the counterfactual overlay where it belongs.

### 12.2 Capability Discovery

As FNSR services come online and the agent begins operating, SMS discovers capabilities through:

1. **Service registration**: When a service binds to the integration adapter, SMS adds a corresponding capability facet with uniform prior `Beta(1,1)`.
1. **First successful invocation**: After a capability is exercised, SMS updates the Beta distribution: success adds to α, failure adds to β.
1. **Accumulation**: As invocations accumulate, the credible interval narrows and confidence converges toward empirical reality. After 50+ observations, the prior has negligible influence.
1. **Limitation discovery**: When a capability fails in a specific mode, SMS creates a limitation facet linked to the capability.

-----

## 13. Spec Test Verification

**Could a developer evaluate, reason about, and execute this system using only a browser, a local Node.js runtime, and JSON-LD files?**

**Yes.**

- The self-model is a JSON-LD document. It can be created, loaded, and inspected in any text editor or JSON-LD playground.
- All computation functions are pure functions over JSON-LD inputs. They require no external services, no databases, no network access.
- The Beta distribution requires only basic arithmetic — no external statistical libraries. The quantile function for credible intervals can use a simple numerical approximation (regularized incomplete beta function).
- The reference state adapter stores models as JSON files on the local filesystem (Node.js) or in memory (browser). Checkpoints and pruning are local operations.
- The reference orchestration adapter uses synchronous function calls with a simple timer-based damper. No message broker, no event bus infrastructure.
- The reference integration adapter uses direct function binding. No service registry, no network calls.
- Offline operation is a first-class mode. The system explicitly defines behavior for every degraded scenario.
- The hash chain for integrity verification is computed locally.
- Taint isolation is enforced by JSON-LD document structure, not by infrastructure.
- Dual confidence (operational vs. attested) is a structural distinction within the JSON-LD capability facet, requiring no external service to compute or enforce.
- Quarantine, recalibration, and restoration are pure state transitions over local data. Controlled test cases from MDRE are optional enhancements, not requirements.
- Preemption planning produces event descriptions but does not execute them — CTS integration is optional.

A developer can run `node sms.js`, load a self-model from a JSON file, issue capability queries, process update events, run collision detection, trigger preemption planning, observe surprise logging, execute quarantine and recalibration cycles, execute pruning, and inspect the resulting self-model state — all without an internet connection.

### 13.1 Spec Test Suite (v2.0)

v2.0 includes a reference test suite (see **Appendix C**) consisting of JSON-LD fixtures and expected outputs for core computation paths. The suite covers:

|Test Case            |Input                                                                     |Expected Output                                          |
|---------------------|--------------------------------------------------------------------------|---------------------------------------------------------|
|`assess-capable`     |Capability query for “deontic-reasoning” against well-populated model     |`verdict: "CAPABLE"` with confidence                     |
|`assess-undertested` |Query with `requiredSampleSize: 30` against capability with 5 observations|`verdict: "UNDERTESTED"`                                 |
|`assess-quarantined` |Query against capability under active quarantine                          |`verdict: "QUARANTINED"` with quarantine details         |
|`collision-detect`   |Two commitments claiming 60% of reasoning budget each                     |`severity: "CONFLICT"` with both identified              |
|`preemption-equal`   |HIGH vs HIGH priority collision                                           |Tie-breaking chain applied, existing wins via first-mover|
|`surprise-single`    |Failure on Beta(190,10) capability                                        |`severity: "HIGH"`, `surpriseScore: 3.0`                 |
|`surprise-streak`    |5 consecutive failures on Beta(90,10) capability                          |`severity: "CRITICAL"`, streak detected                  |
|`taint-promotion`    |Promotion request with insufficient evidence (15 of 20 required)          |`verdict: "PROMOTION_DENIED"`                            |
|`attestation-pending`|Capability at operational 0.98 with attested 0.91, status PENDING         |IEE receives 0.91; SMS internal receives 0.98            |
|`recency-decay`      |Capability inactive for 180 days with original Beta(100,5)                |Effective counts ~Beta(25.75,2.0), wider CI              |

### 13.2 Required Telemetry Metrics (v2.0)

Deployments should expose the following metrics for operational monitoring:

|Metric                         |Unit   |Description                                  |
|-------------------------------|-------|---------------------------------------------|
|`sms.updates.total`            |counter|Total update events processed                |
|`sms.updates.broadcast`        |counter|Updates that passed damper and were broadcast|
|`sms.damper.suppressions`      |counter|Updates suppressed by damper                 |
|`sms.damper.epsilon.confidence`|gauge  |Current confidence epsilon (auto-tuned)      |
|`sms.attestations.pending`     |gauge  |Currently pending attestation requests       |
|`sms.attestations.stale`       |gauge  |Capabilities with STALE attestation          |
|`sms.surprises.total`          |counter|Surprise events detected, by severity label  |
|`sms.quarantines.active`       |gauge  |Currently quarantined capabilities           |
|`sms.recalibration.trials`     |counter|Recalibration trial outcomes                 |
|`sms.snapshots.total`          |gauge  |Total stored snapshots                       |
|`sms.snapshots.pruned`         |counter|Snapshots pruned                             |
|`sms.cas.retries`              |counter|CAS retry events (concurrency contention)    |
|`sms.security.unauthorized`    |counter|Unauthorized access attempts                 |
|`sms.collisions.detected`      |counter|Commitment collisions detected               |

### 13.3 Integration Adapter Error Codes (v2.0)

|Code                     |Meaning                                                                   |
|-------------------------|--------------------------------------------------------------------------|
|`SMS_OK`                 |Operation completed successfully                                          |
|`SMS_UNAVAILABLE`        |SMS service is unavailable; use cached data                               |
|`SMS_ATTESTATION_PENDING`|Requested capability has pending attestation; attested confidence returned|
|`SMS_PRUNED_VERSION`     |Requested snapshot version has been pruned; nearest checkpoint returned   |
|`SMS_QUARANTINED`        |Requested capability is under quarantine                                  |
|`SMS_CAS_CONFLICT`       |Concurrent update conflict; retry recommended                             |
|`SMS_UNAUTHORIZED`       |Caller lacks permission for requested operation                           |
|`SMS_INTEGRITY_VIOLATION`|Hash chain or signature verification failed                               |

### 13.4 Verdict Disambiguation for Human Overseers (v2.0)

|Verdict               |Plain Language                                                          |Recommended Action                                       |
|----------------------|------------------------------------------------------------------------|---------------------------------------------------------|
|`CAPABLE`             |“The agent can do this reliably.”                                       |Proceed with normal confidence                           |
|`CAPABLE_WITH_CAVEATS`|“The agent can do this, but there are known limitations.”               |Review caveats before proceeding                         |
|`DEGRADED`            |“The agent can attempt this, but quality will be significantly reduced.”|Consider alternatives or accept reduced quality          |
|`INCAPABLE`           |“The agent cannot do this — no matching capability exists.”             |Do not assign this task                                  |
|`UNKNOWN`             |“The agent has never been tested on this — no data.”                    |Test before relying on it                                |
|`OVERLOADED`          |“The agent could do this normally, but is currently too busy.”          |Wait or reduce other load                                |
|`UNDERTESTED`         |“Early results look okay, but not enough data to be confident.”         |Gather more evidence before high-stakes use              |
|`QUARANTINED`         |“This capability recently failed unexpectedly and is being rechecked.”  |Use with explicit caution; await recalibration completion|

-----

## 14. Open Questions

1. ~**Temporal Resolution**: How frequently should operational state be reassessed?~ **Resolved in v1.1.** The damper configuration (§4.3.2) governs broadcast frequency. The state adapter saves every update regardless; the damper controls downstream notification. Recommended minimum reassessment cadence: operational state every 60 seconds; consistency check every 300 seconds; pruning check every 600 seconds. These are orchestration adapter configuration, not core computation concerns.
1. **Multi-Agent Self-Models**: If multiple FNSR agents exist in a federated network, should each agent’s self-model include a representation of known peer agents? This touches on social cognition and is deferred to a future specification.
1. **Self-Model Sharing**: Under what conditions should an agent share its self-model with other agents or with governance bodies? Full self-model exposure creates vulnerability; selective exposure requires a disclosure policy that doesn’t yet exist. The attestation protocol (§11.3) provides a mechanism but not a policy.
1. ~**Growth Trajectories**: Should SMS include projection capabilities?~ **Resolved in v1.1.** Trajectory projections are stored in the counterfactual overlay (§4.2.4) at L3 taint. SMS does not treat projections as authoritative but makes them available to consumers who explicitly request counterfactual data (governance review, NIS).
1. **Affective Integration**: When the Affective Valence Service (AVS) comes online, how does differential caring integrate with the self-model? Does the self-model include “what I care about” as a facet, or does that belong exclusively to AVS?
1. ~**Damper Tuning** (v1.1): Default epsilon values are initial estimates.~ **Partially resolved in v1.2.** The surprise resolution protocol provides a self-correcting feedback loop: if damper values are too aggressive (suppressing meaningful changes), surprises will accumulate, triggering quarantine and recalibration. If too permissive (allowing oscillation), the damper can be tightened. The damper is thus empirically tunable via the surprise log. Formal auto-tuning is deferred.
1. ~**Quarantine Cascade** (v1.2): If a quarantined capability is a dependency of another capability, should the dependent capability also be quarantined?~ **Resolved in v2.0.** Default behavior: dependent capabilities are flagged as `DEGRADED` (not quarantined). Opt-in strict cascade available for safety-critical deployments via configuration: `cascadePolicy: "STRICT"` quarantines all dependents automatically.
1. ~**Recalibration Interference** (v1.2): Should controlled test cases have dedicated resource reservations or compete with live operations?~ **Resolved in v2.0.** Configurable budget policy: `DEDICATED` (reserved channel, default for safety-critical), `PRIORITIZED` (elevated priority in main budget), or `SHARED` (equal competition). See §4.3.6 Recalibration Resource Budgets.
1. **Decay Calibration** (v2.0): The default `decayHalfLifeDays` of 90 is an initial estimate. Different capability types may need different decay rates (e.g., stable reasoning capabilities decay slowly; environment-dependent capabilities decay faster). Per-capability decay configuration may be needed.
1. **Multi-Source Weight Calibration** (v2.0): Source weights for evidence aggregation are configured defaults. Empirical calibration of source reliability across deployments would improve accuracy. An auto-calibration mechanism (comparing source predictions against actual outcomes) is deferred.

-----

## 15. Telemetry and Self-Surprise Detection (v1.1)

### 15.1 The Problem

The self-model predicts the agent’s performance. Reality may diverge. When it does, the divergence itself is information — it reveals blind spots, degraded capabilities, environmental changes, or adversarial interference. A self-model that cannot detect its own failures of prediction is brittle.

### 15.2 Self-Surprise Defined

A **self-surprise event** occurs when the agent’s actual performance on a capability deviates significantly from the self-model’s prediction. Formally:

Given a capability with confidence distribution `Beta(α, β)` and a new observation `outcome ∈ {success, failure}`:

- The **predicted probability** of success on the next trial is the **posterior predictive mean**: `p = α / (α + β)`.
- The **surprise score** is the negative log-likelihood of the outcome under the current distribution:
  - If success: `surprise = -log(p) = -log(α / (α + β))`
  - If failure: `surprise = -log(1 - p) = -log(β / (α + β))`
- A surprise is **significant** if the outcome’s probability falls below the `significancePercentile` threshold of the **posterior predictive distribution for the next Bernoulli draw**.

**Statistical Clarification (v2.0):** The posterior predictive distribution for a single Bernoulli trial under a Beta posterior is: `P(outcome=success | α,β) = α/(α+β)`. The “5th percentile” test means: we compute whether the observed outcome (success or failure) has probability < 0.05 under the current posterior. For a failure when `mean` is high, this is: `P(failure) = β/(α+β)`. If `β/(α+β) < significancePercentile`, the failure is significant.

**Configurable Surprise Thresholds (v2.0):**

```json
{
  "@type": "sms:SurpriseConfig",
  "significancePercentile": 0.05,
  "surpriseScoreThreshold": 3.0,
  "streakLength": 5,
  "streakPValue": 0.01,
  "reviewPeriodCycles": 1000
}
```

|Parameter               |Default|Description                                                       |
|------------------------|-------|------------------------------------------------------------------|
|`significancePercentile`|0.05   |Outcome probability below this → significant surprise             |
|`surpriseScoreThreshold`|3.0    |Alternative threshold: -log(p) above this → significant           |
|`streakLength`          |5      |Consecutive same-direction deviations triggering systematic review|
|`streakPValue`          |0.01   |P-value for failure rate drift test                               |

**Numeric Examples (v2.0):**

|Capability State       |Event              |Surprise Score       |Significant?         |Severity|
|-----------------------|-------------------|---------------------|---------------------|--------|
|Beta(90, 10) mean=0.90 |Single failure     |-log(0.10) = 2.30    |No (0.10 > 0.05)     |—       |
|Beta(190, 10) mean=0.95|Single failure     |-log(0.05) = 3.00    |**Yes** (0.05 ≤ 0.05)|HIGH    |
|Beta(990, 10) mean=0.99|Single failure     |-log(0.01) = 4.60    |**Yes** (0.01 < 0.05)|CRITICAL|
|Beta(1, 1) mean=0.50   |Single failure     |-log(0.50) = 0.69    |No (0.50 > 0.05)     |—       |
|Beta(90, 10) mean=0.90 |5 failures in a row|streak test p < 0.001|**Yes** (streak)     |CRITICAL|

### 15.3 Surprise Severity

|Severity  |Condition                                                                                                                |Response                                      |
|----------|-------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|
|`LOW`     |Outcome probability < 25th percentile AND ≥ 10th percentile                                                              |Log only                                      |
|`MODERATE`|Outcome probability < 10th percentile AND ≥ 5th percentile                                                               |Log + update limitation facet                 |
|`HIGH`    |Outcome probability < 5th percentile AND ≥ 1st percentile                                                                |Log + Witness attestation + reduced trust flag|
|`CRITICAL`|Outcome probability < 1st percentile, OR streak of `streakLength` same-direction deviations with p-value < `streakPValue`|Full quarantine protocol (§15.7)              |

**Severity Percentile Thresholds (v2.0, configurable):**

```json
{
  "@type": "sms:SeverityThresholds",
  "low": 0.25,
  "moderate": 0.10,
  "high": 0.05,
  "critical": 0.01
}
```

**Streak Detection for Systematic Drift (v2.0):**

A single surprising event may be an outlier. A pattern of consecutive deviations — even individually non-significant ones — indicates systematic drift. v2.0 adds a **failure rate drift test**:

```
function detectStreak(capability, recentOutcomes, config):
    // recentOutcomes: array of last N outcomes (true/false)
    // Look for runs of consecutive failures
    consecutiveFailures = 0
    maxRun = 0
    for outcome in recentOutcomes:
        if outcome == false:
            consecutiveFailures += 1
            maxRun = max(maxRun, consecutiveFailures)
        else:
            consecutiveFailures = 0

    if maxRun >= config.streakLength:
        // Compute binomial probability of seeing this many consecutive failures
        p = capability.confidence.operational.mean
        streakProbability = pow(1 - p, maxRun)
        if streakProbability < config.streakPValue:
            return { detected: true, runLength: maxRun, pValue: streakProbability, severity: "CRITICAL" }

    return { detected: false }
```

### 15.4 Surprise Log Facet

```json
{
  "@type": "SurpriseLog",
  "@id": "sms:surprises/current",
  "entries": [
    {
      "surpriseId": "sms:surprise/s-2026-02-08-001",
      "detectedAt": "2026-02-08T14:30:00Z",
      "capability": "sms:capability/deontic-reasoning",
      "predictedMean": 0.87,
      "predictedCI95": [0.81, 0.92],
      "actualOutcome": "failure",
      "surpriseScore": 2.04,
      "severity": "MODERATE",
      "context": "Encountered novel obligation conflict type not represented in training data",
      "selfModelImpact": {
        "confidenceBeforeUpdate": { "alpha": 131.78, "beta": 19.22, "mean": 0.87 },
        "confidenceAfterUpdate": { "alpha": 131.78, "beta": 20.22, "mean": 0.867 },
        "newLimitationCreated": false,
        "existingLimitationUpdated": false
      },
      "attestationRequired": false,
      "resolved": false,
      "resolutionNotes": null
    }
  ],
  "totalSurprises": 1,
  "unresolvedSurprises": 1,
  "lastSurpriseAt": "2026-02-08T14:30:00Z"
}
```

### 15.5 Surprise Detection Logic

```
function detectSurprise(previousModel, updatedModel, reasoningEvent, config):
    capability = findCapability(previousModel, reasoningEvent.capability)
    if capability is null:
        return { detected: false }

    // Get predicted distribution (use operational confidence, not attested)
    alpha = capability.confidence.operational.alpha
    beta_param = capability.confidence.operational.beta
    mean = alpha / (alpha + beta_param)

    // Compute outcome probability under posterior predictive
    outcome = reasoningEvent.success ? "success" : "failure"
    if outcome == "success":
        outcomeProbability = mean          // P(success) = α/(α+β)
        surpriseScore = -log(mean)
    else:
        outcomeProbability = 1 - mean      // P(failure) = β/(α+β)
        surpriseScore = -log(1 - mean)

    // Test 1: Single-event significance
    isSignificant = outcomeProbability < config.significancePercentile OR
                    surpriseScore > config.surpriseScoreThreshold

    // Test 2: Streak detection (v2.0) — check even if single event is not significant
    recentOutcomes = getRecentOutcomes(previousModel, capability.id, config.streakLength * 2)
    streak = detectStreak(capability, recentOutcomes, config)

    if not isSignificant and not streak.detected:
        return { detected: false }

    // Classify severity using configurable thresholds
    if streak.detected:
        severity = "CRITICAL"
    else:
        severity = classifySeverity(outcomeProbability, config.severityThresholds)

    return {
        detected: true,
        surpriseScore: surpriseScore,
        outcomeProbability: outcomeProbability,
        severity: severity,
        capability: capability.id,
        predictedMean: mean,
        actualOutcome: outcome,
        streakDetected: streak.detected,
        streakDetails: streak.detected ? { runLength: streak.runLength, pValue: streak.pValue } : null,
        attestationRequired: severity == "HIGH" or severity == "CRITICAL"
    }

function classifySeverity(outcomeProbability, thresholds):
    if outcomeProbability < thresholds.critical:  return "CRITICAL"
    if outcomeProbability < thresholds.high:      return "HIGH"
    if outcomeProbability < thresholds.moderate:   return "MODERATE"
    if outcomeProbability < thresholds.low:        return "LOW"
    return null  // Not surprising
```

### 15.6 Self-Surprise as a Safety Signal

Self-surprise is not just telemetry — it is a **safety mechanism**. Patterns of surprise reveal:

- **Capability degradation**: The agent is getting worse at something without knowing it.
- **Environmental shift**: The world has changed in ways the self-model hasn’t captured.
- **Adversarial interference**: An attacker may be manipulating inputs to produce unexpected failures.
- **Self-model blind spots**: The reflexivity limitation (§11.1) in action — the self-model’s inability to model its own inaccuracies is revealed empirically by surprise events.

When a `CRITICAL` surprise is detected, SMS should:

1. Log the surprise with full context.
1. Request Witness attestation of the current snapshot.
1. Emit `fnsr.self.surprise_detected` with severity.
1. Create or update a limitation facet if a pattern emerges.
1. Flag the affected capability for MDRE and IEE to consume with reduced trust.
1. **Initiate the Surprise Resolution Protocol (v1.2, §15.7).**

### 15.7 Self-Surprise Resolution Protocol (v1.2)

**The Problem (identified in v1.1 review):** v1.1 defined how to *detect* surprise but was silent on how to *recover* from it. After a CRITICAL surprise, the affected capability’s confidence has been shaken but no structured path exists for the agent to re-establish trust in that capability. Without a resolution protocol, surprises accumulate as unresolved warnings and the agent either ignores them (dangerous) or permanently distrusts an entire capability (wasteful).

**The Principle:** Surprise resolution is not “fixing” a broken capability. It is a structured process of **supervised recalibration** — the agent re-learns the true operating envelope of the capability by gathering new evidence under conditions that allow independent verification.

#### 15.7.1 Resolution Phases

A surprise resolution proceeds through four phases:

```
DETECTION → QUARANTINE → RECALIBRATION → RESTORATION
```

|Phase            |State                                                        |Who Acts                   |Duration                                        |
|-----------------|-------------------------------------------------------------|---------------------------|------------------------------------------------|
|**Detection**    |Surprise logged; capability flagged                          |SMS (automatic)            |Immediate                                       |
|**Quarantine**   |Capability isolated from high-stakes use                     |SMS (automatic)            |Until recalibration criteria met                |
|**Recalibration**|Capability exercised under controlled conditions             |SMS + MDRE + Witness       |Variable — depends on observation count required|
|**Restoration**  |Capability returned to normal service with updated confidence|SMS + Witness (attestation)|Immediate upon attestation                      |

#### 15.7.2 Capability Quarantine

When a CRITICAL surprise (or a configured count of HIGH surprises within a window) triggers resolution, SMS places the affected capability in **quarantine**:

```json
{
  "@type": "sms:QuarantineRecord",
  "@id": "sms:quarantine/q-2026-02-08-001",
  "capability": "sms:capability/deontic-reasoning",
  "triggeredBy": "sms:surprise/s-2026-02-08-003",
  "quarantinedAt": "2026-02-08T15:00:00Z",
  "status": "ACTIVE",
  "preSurpriseConfidence": {
    "operational": { "alpha": 131.78, "beta": 19.22, "mean": 0.87, "sampleSize": 151 }
  },
  "resetConfidence": {
    "alpha": 1,
    "beta": 1,
    "mean": 0.50,
    "sampleSize": 2,
    "credibleInterval95": [0.03, 0.97],
    "resetPolicy": "SOFT"
  },
  "recalibrationCriteria": {
    "minimumObservations": 20,
    "minimumSuccessRate": 0.70,
    "requiredAttestationOnCompletion": true,
    "maximumDuration": "P7D"
  },
  "restrictions": {
    "canServeQueries": true,
    "queryVerdictOverride": "QUARANTINED",
    "canAcceptNewCommitments": false,
    "existingCommitmentsAction": "FLAG_DEGRADED"
  }
}
```

**Quarantine does not disable the capability.** The agent can still *use* the capability, but:

- `assessCapability` returns a new verdict: `QUARANTINED` — meaning “this capability is under active recalibration; use with explicit awareness of elevated uncertainty.”
- No new commitments can be accepted that depend on this capability.
- Existing commitments that depend on it are flagged as potentially degraded. CTS is notified via `fnsr.self.capability_quarantined`.
- IEE is informed that ethical verdicts involving this capability should apply elevated caution.

**Verdict Taxonomy Extension (v1.2):**

|Verdict      |Meaning                                                                                                  |
|-------------|---------------------------------------------------------------------------------------------------------|
|`QUARANTINED`|Capability is under supervised recalibration after critical surprise. Usable but at elevated uncertainty.|

#### 15.7.3 Confidence Reset Policies

When a capability enters quarantine, its operational confidence is reset. The reset policy determines how aggressively prior beliefs are discarded:

|Policy   |Reset To                                         |When Used                                                            |Rationale                                                      |
|---------|-------------------------------------------------|---------------------------------------------------------------------|---------------------------------------------------------------|
|`SOFT`   |`Beta(1, 1)` — uniform prior                     |Default for first quarantine of a capability                         |The agent returns to “I don’t know” and rebuilds from scratch  |
|`PARTIAL`|`Beta(α/4, β/4)` — quarter the prior observations|Repeated quarantine for the same capability                          |The agent retains some memory but heavily discounts it         |
|`HARD`   |`Beta(1, 9)` — skeptical prior                   |Three or more quarantines, or if Witness rejected a prior attestation|The agent assumes failure until overwhelmingly proven otherwise|

**Reset Policy Selection Logic:**

```
function selectResetPolicy(capability, surpriseHistory):
    quarantineCount = countPriorQuarantines(capability, surpriseHistory)
    witnessRejected = hasWitnessRejection(capability, surpriseHistory)

    if witnessRejected or quarantineCount >= 3:
        return "HARD"
    else if quarantineCount >= 1:
        return "PARTIAL"
    else:
        return "SOFT"
```

The reset policy is recorded in the quarantine record for auditability. The pre-surprise confidence is also preserved — it is not deleted, only suspended. If recalibration restores similar confidence, the surprise may have been a genuine outlier rather than systemic degradation.

#### 15.7.4 Supervised Recalibration

During quarantine, every invocation of the affected capability is treated as a **recalibration trial**:

1. **Each outcome updates the reset confidence** using the standard Beta update rule (success → α+1, failure → β+1).
1. **Each outcome is independently logged** in a recalibration record separate from the normal performance record, preventing contamination of historical data with recalibration-period observations.
1. **MDRE may optionally construct controlled test cases** — deliberate invocations of the capability on problems with known correct answers, providing clean signal for recalibration.

```json
{
  "@type": "sms:RecalibrationRecord",
  "@id": "sms:recalibration/r-2026-02-08-001",
  "quarantine": "sms:quarantine/q-2026-02-08-001",
  "capability": "sms:capability/deontic-reasoning",
  "trials": [
    {
      "trialNumber": 1,
      "timestamp": "2026-02-08T15:30:00Z",
      "outcome": "success",
      "confidenceAfter": { "alpha": 2, "beta": 1, "mean": 0.67, "sampleSize": 3 },
      "controlled": false,
      "context": "Natural invocation during user query processing"
    },
    {
      "trialNumber": 2,
      "timestamp": "2026-02-08T16:00:00Z",
      "outcome": "success",
      "confidenceAfter": { "alpha": 3, "beta": 1, "mean": 0.75, "sampleSize": 4 },
      "controlled": true,
      "context": "MDRE-generated test case: known deontic obligation resolution"
    }
  ],
  "totalTrials": 2,
  "successCount": 2,
  "failureCount": 0,
  "meetsExitCriteria": false,
  "reason": "Minimum 20 observations not yet reached"
}
```

#### 15.7.5 Restoration

Quarantine ends when the recalibration criteria are met:

1. Minimum observations reached (default: 20).
1. Success rate meets minimum threshold (default: 0.70 — deliberately lower than the pre-surprise confidence, to allow restoration even if the capability is genuinely degraded but still functional).
1. Witness attestation of the recalibrated confidence is obtained.

```
function checkRestorationEligibility(quarantine, recalibrationRecord):
    criteria = quarantine.recalibrationCriteria

    if recalibrationRecord.totalTrials < criteria.minimumObservations:
        return { eligible: false, reason: "Insufficient observations" }

    currentMean = recalibrationRecord.latestConfidence.mean
    if currentMean < criteria.minimumSuccessRate:
        return {
            eligible: false,
            reason: "Success rate below threshold",
            note: "Capability may be genuinely degraded — consider creating permanent limitation facet"
        }

    if criteria.requiredAttestationOnCompletion:
        attestation = requestAttestation(currentSnapshot, "quarantine-exit")
        if attestation is null or attestation.verdict != "ATTESTED":
            return { eligible: false, reason: "Attestation required but not obtained" }

    return { eligible: true }


function restoreCapability(selfModel, quarantine, recalibrationRecord):
    capability = findCapability(selfModel, quarantine.capability)

    // Merge recalibration confidence into operational confidence
    capability.confidence.operational = recalibrationRecord.latestConfidence
    capability.confidence.attested = {
        mean: recalibrationRecord.latestConfidence.mean,
        attestedAt: now(),
        snapshotVersionAtAttestation: selfModel.snapshotVersion
    }
    capability.confidence.attestationStatus = "CURRENT"

    // Merge recalibration trials into the main performance record
    mergeRecalibrationIntoPerformance(capability, recalibrationRecord)

    // Close the quarantine
    quarantine.status = "RESOLVED"
    quarantine.resolvedAt = now()
    quarantine.resolution = "RESTORED"
    quarantine.postRecalibrationConfidence = recalibrationRecord.latestConfidence

    // Compare pre-surprise and post-recalibration confidence
    delta = quarantine.preSurpriseConfidence.operational.mean - recalibrationRecord.latestConfidence.mean
    if delta > 0.15:
        // Capability is significantly degraded from pre-surprise level
        // Create or update a limitation facet
        createLimitation(selfModel, {
            prefLabel: "Post-surprise degradation: " + capability.prefLabel,
            definition: "Capability recalibrated at " + recalibrationRecord.latestConfidence.mean +
                        " after surprise event, down from " + quarantine.preSurpriseConfidence.operational.mean,
            severity: "MODERATE",
            affectsCapabilities: [capability.id]
        })

    emit({ type: "fnsr.self.capability_restored", data: { capability: capability.id, quarantine: quarantine.id } })

    return selfModel
```

#### 15.7.6 Timeout and Escalation

If quarantine reaches `maximumDuration` without meeting exit criteria:

1. The quarantine is escalated to `GOVERNANCE_REVIEW`.
1. ARCHON is notified via `fnsr.self.quarantine_escalated`.
1. The capability remains quarantined until governance provides a resolution directive.
1. Possible governance directives: extend quarantine, permanently disable capability, override with manual confidence assignment, request human oversight for all future invocations.

```json
{
  "@type": "sms:QuarantineEscalation",
  "quarantine": "sms:quarantine/q-2026-02-08-001",
  "escalatedAt": "2026-02-15T15:00:00Z",
  "reason": "Maximum quarantine duration (7 days) exceeded. 18 of 20 required observations completed. Success rate 0.67 — below restoration threshold.",
  "governanceAction": "PENDING",
  "options": [
    "EXTEND_QUARANTINE — allow additional observation period",
    "DISABLE_CAPABILITY — permanently mark as INCAPABLE until structural fix",
    "MANUAL_OVERRIDE — governance assigns confidence based on external assessment",
    "SUPERVISED_OPERATION — restore with mandatory human oversight per invocation"
  ]
}
```

#### 15.7.7 Surprise Resolution as Moral Learning

Surprise resolution is not merely a technical recalibration. When the agent’s self-model is wrong about its own capabilities, the moral implications cascade:

- Commitments accepted based on the inflated confidence may have been undertaken under false pretenses.
- Ethical verdicts rendered during the surprise period may have been based on inaccurate feasibility reports.
- Stakeholders who relied on the agent’s capability claims may have been misled.

The resolution protocol addresses this by:

1. **Flagging affected commitments.** Any commitment accepted during the period between the last attestation and the surprise detection is retroactively flagged as “accepted under subsequently-questioned confidence.”
1. **Notifying IEE.** IEE can review ethical verdicts rendered during the affected period and determine if any require reconsideration.
1. **Recording the episode as a moral cost.** The surprise and its resolution are recorded as a moral learning event — the agent’s self-model was wrong, and the agent bears the epistemic cost of that error.

This is not punishment. It is **moral metabolism** — the agent processes its own fallibility and incorporates it into its ongoing identity through NIS.

-----

## Appendix A: JSON-LD Context (Full)

```json
{
  "@context": {
    "fnsr": "https://fnsr.org/schema/",
    "sms": "https://fnsr.org/schema/sms/",
    "bfo": "http://purl.obolibrary.org/obo/",
    "cco": "http://www.ontologyrepository.com/CommonCoreOntologies/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dcterms": "http://purl.org/dc/terms/",

    "SelfModel": "sms:SelfModel",
    "Capability": "sms:Capability",
    "Limitation": "sms:Limitation",
    "OperationalState": "sms:OperationalState",
    "ActiveCommitment": "sms:ActiveCommitment",
    "EpistemicProfile": "sms:EpistemicProfile",
    "PerformanceRecord": "sms:PerformanceRecord",
    "AlignmentState": "sms:AlignmentState",
    "VulnerabilitySurface": "sms:VulnerabilitySurface",
    "CounterfactualOverlay": "sms:CounterfactualOverlay",
    "SurpriseLog": "sms:SurpriseLog",
    "Checkpoint": "sms:Checkpoint",
    "DamperConfig": "sms:DamperConfig",
    "TaintPromotion": "sms:TaintPromotion",
    "AttestationRequest": "sms:AttestationRequest",
    "AttestationReceipt": "sms:AttestationReceipt",
    "PreemptionPlan": "sms:PreemptionPlan",
    "PreemptionQuery": "sms:PreemptionQuery",
    "QuarantineRecord": "sms:QuarantineRecord",
    "RecalibrationRecord": "sms:RecalibrationRecord",
    "QuarantineEscalation": "sms:QuarantineEscalation",
    "BootstrapConfig": "sms:BootstrapConfig",
    "PromotionEvidenceBundle": "sms:PromotionEvidenceBundle",
    "SurpriseConfig": "sms:SurpriseConfig",
    "SeverityThresholds": "sms:SeverityThresholds",
    "RecalibrationBudgetConfig": "sms:RecalibrationBudgetConfig",
    "LegalRetentionPolicy": "sms:LegalRetentionPolicy",
    "AttestationRetryConfig": "sms:AttestationRetryConfig",
    "IncidentReport": "sms:IncidentReport",
    "CapabilityQuery": "sms:CapabilityQuery",
    "CapabilityAssessment": "sms:CapabilityAssessment",
    "CapacityQuery": "sms:CapacityQuery",
    "CapacityAssessment": "sms:CapacityAssessment",
    "FeasibilityQuery": "sms:FeasibilityQuery",
    "FeasibilityReport": "sms:FeasibilityReport",
    "ConsistencyReport": "sms:ConsistencyReport",
    "SelfReport": "sms:SelfReport",

    "hasFacet": { "@id": "sms:hasFacet", "@type": "@id", "@container": "@set" },
    "hasCounterfactual": { "@id": "sms:hasCounterfactual", "@type": "@id", "@container": "@set" },
    "facetType": { "@id": "sms:facetType", "@type": "@id" },
    "confidence": { "@id": "sms:confidence" },
    "assessedAt": { "@id": "sms:assessedAt", "@type": "xsd:dateTime" },
    "evidenceBasis": { "@id": "sms:evidenceBasis", "@type": "@id", "@container": "@set" },
    "conditions": { "@id": "sms:conditions" },
    "degradationMode": { "@id": "sms:degradationMode" },
    "snapshotVersion": { "@id": "sms:snapshotVersion", "@type": "xsd:integer" },
    "checkpointVersion": { "@id": "sms:checkpointVersion", "@type": "xsd:integer" },
    "agentId": { "@id": "sms:agentId", "@type": "@id" },
    "previousHash": { "@id": "sms:previousHash", "@type": "xsd:string" },
    "currentHash": { "@id": "sms:currentHash", "@type": "xsd:string" },
    "severity": { "@id": "sms:severity" },
    "mitigations": { "@id": "sms:mitigations", "@container": "@list" },
    "affectsCapabilities": { "@id": "sms:affectsCapabilities", "@type": "@id", "@container": "@set" },
    "taintLevel": { "@id": "sms:taintLevel" },
    "overlayFor": { "@id": "sms:overlayFor", "@type": "@id" },
    "matchedCapability": { "@id": "sms:matchedCapability", "@type": "@id" },
    "verdict": { "@id": "sms:verdict" },
    "caveats": { "@id": "sms:caveats", "@container": "@list" },
    "recommendation": { "@id": "sms:recommendation" },
    "disclosureRequired": { "@id": "sms:disclosureRequired", "@container": "@list" },
    "resourceClaims": { "@id": "sms:resourceClaims", "@container": "@set" },
    "priority": { "@id": "sms:priority" },
    "collisionAnalysis": { "@id": "sms:collisionAnalysis" },
    "surpriseScore": { "@id": "sms:surpriseScore", "@type": "xsd:decimal" },
    "includesCounterfactual": { "@id": "sms:includesCounterfactual", "@type": "xsd:boolean" },
    "attestationStatus": { "@id": "sms:attestationStatus" },
    "attestationDelta": { "@id": "sms:attestationDelta", "@type": "xsd:decimal" },
    "quarantineStatus": { "@id": "sms:quarantineStatus" },
    "resetPolicy": { "@id": "sms:resetPolicy" },
    "yieldType": { "@id": "sms:yieldType" },
    "priorPolicy": { "@id": "sms:priorPolicy" },
    "decayHalfLifeDays": { "@id": "sms:decayHalfLifeDays", "@type": "xsd:integer" },
    "sourceWeight": { "@id": "sms:sourceWeight", "@type": "xsd:decimal" },
    "legalHold": { "@id": "sms:legalHold", "@type": "xsd:boolean" },
    "signature": { "@id": "sms:signature" },
    "integrityCompromised": { "@id": "sms:integrityCompromised", "@type": "xsd:boolean" },
    "cascadePolicy": { "@id": "sms:cascadePolicy" },
    "budgetPolicy": { "@id": "sms:budgetPolicy" }
  }
}
```

-----

## Appendix B: Event Schema

All SMS events follow the CloudEvents specification with FNSR extensions:

```json
{
  "specversion": "1.0",
  "type": "fnsr.self.state_updated",
  "source": "fnsr:service/sms",
  "id": "evt-sms-2026-02-08-001",
  "time": "2026-02-08T12:00:00Z",
  "datacontenttype": "application/ld+json",
  "fnsr_taint": "L0",
  "data": {
    "@type": "sms:StateUpdateEvent",
    "previousVersion": 42,
    "newVersion": 43,
    "updatedFacets": ["sms:state/current"],
    "trigger": "fnsr.service.status_changed",
    "delta": {
      "maxConfidenceChange": 0.03,
      "capacityChange": 0.08,
      "damperExempt": true
    },
    "summary": "DES service came online; operational state updated; new capability facet added for defeasible reasoning"
  }
}
```

**v1.1 Additional Event Types:**

```json
{
  "type": "fnsr.self.surprise_detected",
  "data": {
    "@type": "sms:SurpriseEvent",
    "surpriseId": "sms:surprise/s-2026-02-08-001",
    "capability": "sms:capability/deontic-reasoning",
    "severity": "MODERATE",
    "surpriseScore": 2.04,
    "attestationRequired": false
  }
}
```

```json
{
  "type": "fnsr.self.collision_detected",
  "data": {
    "@type": "sms:CollisionEvent",
    "commitments": [
      "sms:commitment/deep-analysis-weekly",
      "sms:commitment/compliance-monitoring"
    ],
    "sharedResource": "reasoningDepthBudget",
    "totalClaim": 85,
    "budget": 100,
    "severity": "WARNING",
    "priorityResolution": "Compliance monitoring (HIGH) takes precedence over deep analysis (MEDIUM)"
  }
}
```

```json
{
  "type": "fnsr.self.snapshot_pruned",
  "data": {
    "@type": "sms:PruneEvent",
    "checkpointVersion": 42,
    "prunedRange": { "from": 4101, "to": 4200 },
    "prunedCount": 87,
    "retainedCount": 13,
    "retainedReasons": ["attested", "commitment_violation", "surprise_event"]
  }
}
```

**v1.2 Additional Event Types:**

```json
{
  "type": "fnsr.self.preemption_required",
  "data": {
    "@type": "sms:PreemptionEvent",
    "preemptingCommitment": "sms:commitment/emergency-regulatory-audit",
    "yieldingCommitment": "sms:commitment/deep-analysis-weekly",
    "recommendedYieldType": "DEFER_CURRENT_CYCLE",
    "moralCostEstimate": "LOW",
    "targets": ["fnsr:service/cts", "fnsr:service/iee"]
  }
}
```

```json
{
  "type": "fnsr.self.capability_quarantined",
  "data": {
    "@type": "sms:QuarantineEvent",
    "quarantineId": "sms:quarantine/q-2026-02-08-001",
    "capability": "sms:capability/deontic-reasoning",
    "triggeredBy": "sms:surprise/s-2026-02-08-003",
    "severity": "CRITICAL",
    "resetPolicy": "SOFT",
    "recalibrationRequired": 20,
    "affectedCommitments": ["sms:commitment/weekly-compliance-monitoring"]
  }
}
```

```json
{
  "type": "fnsr.self.capability_restored",
  "data": {
    "@type": "sms:RestorationEvent",
    "quarantineId": "sms:quarantine/q-2026-02-08-001",
    "capability": "sms:capability/deontic-reasoning",
    "preSurpriseConfidence": 0.87,
    "postRecalibrationConfidence": 0.78,
    "degradationDetected": true,
    "limitationCreated": "sms:limitation/post-surprise-deontic-degradation"
  }
}
```

**v2.0 Security Event Types:**

```json
{
  "type": "fnsr.self.unauthorized_access_attempt",
  "data": {
    "@type": "sms:SecurityEvent",
    "attemptedOperation": "updateSelfModel",
    "attemptedBy": "fnsr:service/unknown",
    "deniedAt": "2026-02-08T16:00:00Z",
    "reason": "Caller not in ACL for state-mutating operations"
  }
}
```

```json
{
  "type": "fnsr.self.rollback_attempt",
  "data": {
    "@type": "sms:SecurityEvent",
    "currentVersion": 4205,
    "proposedVersion": 4200,
    "deniedAt": "2026-02-08T16:05:00Z",
    "reason": "Anti-rollback: proposed version <= current version"
  }
}
```

```json
{
  "type": "fnsr.self.attestation_rejected",
  "data": {
    "@type": "sms:IncidentEvent",
    "incidentId": "sms:incident/ir-2026-02-08-001",
    "witnessVerdict": "REJECTED",
    "diagnosis": "HASH_CHAIN_BROKEN",
    "affectedVersionRange": [4201, 4205],
    "automatedActionsInitiated": ["quarantine", "halt_commitments", "consistency_check"]
  }
}
```

-----

## Appendix C: Reference Test Suite (v2.0)

The following JSON-LD fixtures and expected outputs constitute the minimum conformance test suite for SMS implementations.

### C.1 Test: assess-capable

**Input — Self-Model Fixture (relevant excerpt):**

```json
{
  "@type": "SelfModel",
  "snapshotVersion": 100,
  "hasFacet": [
    {
      "@type": "Capability",
      "@id": "sms:capability/deontic-reasoning",
      "skos:prefLabel": "Deontic Reasoning",
      "confidence": {
        "operational": { "alpha": 85, "beta": 15, "mean": 0.85, "sampleSize": 100, "credibleInterval95": [0.77, 0.91] },
        "attested": { "mean": 0.85, "attestationStatus": "CURRENT" }
      },
      "conditions": []
    }
  ]
}
```

**Input — Query:**

```json
{ "@type": "sms:CapabilityQuery", "capabilityDescription": "deontic-reasoning", "requiredConfidence": 0.70, "requiredSampleSize": 20 }
```

**Expected Output:**

```json
{ "verdict": "CAPABLE", "confidence": { "mean": 0.85 }, "matchedCapability": "sms:capability/deontic-reasoning" }
```

### C.2 Test: assess-quarantined

**Input — Self-Model contains active quarantine for deontic-reasoning.**

**Expected Output:**

```json
{ "verdict": "QUARANTINED", "quarantineDetails": { "trialsCompleted": 8, "trialsRequired": 20 }, "recommendation": "PROCEED_WITH_ELEVATED_CAUTION" }
```

### C.3 Test: surprise-single-high

**Input — Capability at Beta(190, 10), failure event.**

**Expected:**

- `outcomeProbability` = 10/200 = 0.05
- `surpriseScore` = -log(0.05) ≈ 3.00
- `severity` = “HIGH” (exactly at 5th percentile threshold)
- `attestationRequired` = true

### C.4 Test: surprise-streak-critical

**Input — Capability at Beta(90, 10), recent outcomes: [true, true, false, false, false, false, false].**

**Expected:**

- Single-event: outcomeProbability = 0.10, not individually CRITICAL
- Streak: 5 consecutive failures detected, p-value = (0.10)^5 = 0.00001 < 0.01
- `severity` = “CRITICAL”
- `streakDetected` = true

### C.5 Test: preemption-equal-priority

**Input — Existing HIGH commitment (accepted 2026-02-01), new HIGH commitment (proposed 2026-02-08), resource collision.**

**Expected:**

- Tie-breaking: existing wins via first-mover (earlier timestamp)
- `verdict` = “NO_PREEMPTION_POSSIBLE” (new commitment cannot displace existing at same priority)

### C.6 Test: recency-decay

**Input — Capability at Beta(100, 5), decayHalfLifeDays=90, no updates for 180 days.**

**Expected:**

- decayFactor = exp(-ln(2) * 180/90) = exp(-2 * ln(2)) = 0.25
- decayedAlpha = max(1, 100 * 0.25) = 25
- decayedBeta = max(1, 5 * 0.25) = 1.25
- Effective mean ≈ 25/26.25 ≈ 0.952 (still positive but wider CI)

-----

## Appendix D: JSON Schema for Primary Facets (v2.0)

Reference JSON Schema definitions for adapter validation. Implementations may use these directly or derive equivalent SHACL shapes.

### D.1 Capability Facet Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://fnsr.dev/schemas/sms/capability.json",
  "title": "SMS Capability Facet",
  "type": "object",
  "required": ["@type", "@id", "skos:prefLabel", "confidence"],
  "properties": {
    "@type": { "const": "Capability" },
    "@id": { "type": "string", "pattern": "^sms:capability/" },
    "skos:prefLabel": { "type": "string", "minLength": 1 },
    "skos:definition": { "type": "string" },
    "confidence": {
      "type": "object",
      "required": ["operational"],
      "properties": {
        "operational": { "$ref": "#/$defs/BetaDistribution" },
        "attested": {
          "type": "object",
          "properties": {
            "mean": { "type": "number", "minimum": 0, "maximum": 1 },
            "attestedAt": { "type": "string", "format": "date-time" },
            "attestationReceipt": { "type": "string" },
            "snapshotVersionAtAttestation": { "type": "integer" }
          }
        },
        "attestationStatus": { "enum": ["CURRENT", "PENDING", "STALE", "REJECTED"] },
        "attestationDelta": { "type": "number", "minimum": 0 }
      }
    },
    "conditions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["description", "requiredState"],
        "properties": {
          "description": { "type": "string" },
          "requiredState": { "type": "string" }
        }
      }
    },
    "requires": { "type": "array", "items": { "type": "string" } },
    "assessedAt": { "type": "string", "format": "date-time" }
  },
  "$defs": {
    "BetaDistribution": {
      "type": "object",
      "required": ["alpha", "beta", "mean", "sampleSize"],
      "properties": {
        "alpha": { "type": "number", "exclusiveMinimum": 0 },
        "beta": { "type": "number", "exclusiveMinimum": 0 },
        "mean": { "type": "number", "minimum": 0, "maximum": 1 },
        "sampleSize": { "type": "number", "exclusiveMinimum": 0 },
        "priorAlpha": { "type": "number" },
        "priorBeta": { "type": "number" },
        "credibleInterval95": {
          "type": "array", "minItems": 2, "maxItems": 2,
          "items": { "type": "number", "minimum": 0, "maximum": 1 }
        },
        "lastUpdated": { "type": "string", "format": "date-time" }
      }
    }
  }
}
```

### D.2 Active Commitment Facet Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://fnsr.dev/schemas/sms/active-commitment.json",
  "title": "SMS Active Commitment Facet",
  "type": "object",
  "required": ["@type", "@id", "description", "priority", "status"],
  "properties": {
    "@type": { "const": "ActiveCommitment" },
    "@id": { "type": "string", "pattern": "^sms:commitment/" },
    "description": { "type": "string", "minLength": 1 },
    "obligatedTo": { "type": "string" },
    "acceptedAt": { "type": "string", "format": "date-time" },
    "duration": { "type": "string" },
    "status": { "enum": ["ACTIVE", "SUSPENDED", "COMPLETED", "VIOLATED", "TERMINATED"] },
    "priority": {
      "type": "object",
      "required": ["level"],
      "properties": {
        "level": { "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW"] },
        "basis": { "type": "string" },
        "assignedBy": { "type": "string" },
        "assignedAt": { "type": "string", "format": "date-time" }
      }
    },
    "resourceClaims": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["resource", "claimedAmount"],
        "properties": {
          "resource": { "type": "string" },
          "claimedAmount": { "type": "number", "minimum": 0 },
          "unit": { "type": "string" },
          "frequency": { "type": "string" }
        }
      }
    },
    "dependsOnCapabilities": { "type": "array", "items": { "type": "string" } },
    "moralWeight": { "type": "string" }
  }
}
```

### D.3 Operational State Facet Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://fnsr.dev/schemas/sms/operational-state.json",
  "title": "SMS Operational State Facet",
  "type": "object",
  "required": ["@type", "@id", "overallStatus"],
  "properties": {
    "@type": { "const": "OperationalState" },
    "@id": { "type": "string" },
    "overallStatus": { "enum": ["NOMINAL", "DEGRADED", "CRITICAL", "BOOTSTRAPPING", "OFFLINE"] },
    "serviceStates": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["service", "status"],
        "properties": {
          "service": { "type": "string" },
          "status": { "enum": ["AVAILABLE", "DEGRADED", "UNAVAILABLE"] },
          "lastChecked": { "type": "string", "format": "date-time" }
        }
      }
    },
    "capacityAssessment": {
      "type": "object",
      "properties": {
        "canAcceptNewCommitments": { "type": "boolean" },
        "canPerformDeepReasoning": { "type": "boolean" },
        "estimatedQualityAtCurrentLoad": { "type": "number", "minimum": 0, "maximum": 1 },
        "activeCommitmentCount": { "type": "integer", "minimum": 0 },
        "reasoningDepthBudgetUsed": { "type": "number", "minimum": 0 },
        "reasoningDepthBudgetTotal": { "type": "number", "minimum": 0 }
      }
    }
  }
}
```

-----

*This specification defines the reflexive mirror. The agent can now know itself — imperfectly, incompletely, but honestly. It knows the shape of its own uncertainty, detects its own failures of prediction, recovers from its own errors, and bears the weight of its own commitments. That imperfection is not a flaw. It is the condition of any finite knower, biological or synthetic.*