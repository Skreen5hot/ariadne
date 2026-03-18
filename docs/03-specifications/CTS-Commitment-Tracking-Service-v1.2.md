# Commitment Tracking Service (CTS)

## Technical Specification v1.2

**Version:** 1.2.1
**Date:** March 2026
**Status:** Ready for Milestone 1 Implementation
**Spec ID:** cts-core-01

---

> *A Ledger of Promises for a Synthetic Moral Person*

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | February 2026 | Initial specification |
| 1.1.0 | February 2026 | DEFERRED deadline enforcement, negative constraint fulfillment type, duty-of-care multiplier, taint level corrections (moral cost → L2), L3 promisee taint inheritance, administrative rescission cause, self-commitment support, Proof of Commitment export, IEE veto deadlock resolution protocol, moral residue accumulation safeguards, expanded test suite |
| 1.2.0 | February 2026 | Heartbeat fulfillment for indefinite negative constraints, L3→L1 taint upgrade on DEFERRED system failure, PII-safe content hashing for Proof of Commitment, explicit IEE decision provenance on tragic violation events |
| 1.2.1 | March 2026 | Cross-specification coherence patch: (1) Unified Commitment Ledger declaration — CTS and SPCN share one ledger per node; (2) "Taint Semantics" renamed to "Disclosure Level Semantics" to resolve terminology collision with SPCN's epistemic taint lattice. No behavioral changes. |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architectural Position](#2-architectural-position)
3. [Foundational Principles](#3-foundational-principles)
4. [Ontological Grounding](#4-ontological-grounding)
5. [Commitment Lifecycle](#5-commitment-lifecycle)
6. [Data Model](#6-data-model)
7. [Moral Cost Calculus](#7-moral-cost-calculus)
8. [Query Interface](#8-query-interface)
9. [Event Contract](#9-event-contract)
10. [Cross-Service Integration](#10-cross-service-integration)
11. [Disclosure Level Semantics](#11-disclosure-level-semantics)
12. [Temporal Reasoning](#12-temporal-reasoning)
13. [Conflict and Contradiction](#13-conflict-and-contradiction)
14. [Edge-Canonical Implementation](#14-edge-canonical-implementation)
15. [Offline Behavior](#15-offline-behavior)
16. [Testing and Validation](#16-testing-and-validation)
17. [Security Model](#17-security-model)
18. [Implementation Roadmap](#18-implementation-roadmap)
19. [Appendices](#appendices)

---

## 1. Executive Summary

The Commitment Tracking Service (CTS) is the promise-keeping ledger of the synthetic moral person. It tracks what the agent has committed to, to whom, under what conditions, and whether those commitments have been honored, violated, or renegotiated.

Moral agency requires the capacity to make and keep promises. An agent that cannot track its own commitments cannot be held accountable for breaking them. An agent that cannot distinguish a kept promise from a broken one has no moral character. CTS provides the infrastructure that makes promise-keeping — and the moral cost of promise-breaking — computationally tractable.

CTS occupies a distinct niche in the FNSR architecture:

- **MDRE** determines what *ought* to be done (deontic reasoning over norms and obligations).
- **IEE** evaluates whether a commitment is *ethically permissible* to make or fulfill.
- **Fandaws** stores *facts about the world* (A-Box assertions).
- **CTS** tracks the *state of the agent's own promises* — a reflexive, first-person ledger of what the agent has bound itself to do.

The critical design insight: a broken commitment is not merely a state change. It is an **irreversible moral event** that accumulates as moral cost against the agent's character. This cost cannot be undone, only acknowledged. This connects CTS directly to the moral friction metric: the agent's trustworthiness is, in part, a function of its commitment-keeping record.

---

## 2. Architectural Position

### 2.1 Position in the Synthetic Person

| Human Faculty | FNSR Service | CTS Relationship |
|---------------|--------------|------------------|
| **Conscience** | IEE | CTS asks IEE: "Is this commitment ethical to make?" IEE asks CTS: "What existing commitments constrain this decision?" |
| **Reason** | MDRE | MDRE derives obligations; CTS records when the agent accepts them as personal commitments |
| **Memory** | Fandaws | Fandaws stores facts; CTS stores self-bindings. CTS may write commitment facts to Fandaws for cross-service visibility |
| **Identity** | OERS, HIRI | CTS uses OERS to resolve *who* was promised *what*. HIRI signs commitment records for provenance |
| **Integrity** | SHML | SHML verifies that commitment-related communications honestly represent the agent's actual commitment state |
| **Character** | Moral Friction | CTS feeds the moral friction metric: violations increase friction; fulfillments maintain or improve it |

### 2.2 Service Card

| Field | Value |
|-------|-------|
| **Service ID** | cts-core-01 |
| **Name** | Commitment Tracking Service |
| **Aliases** | CTS, Promise Ledger |
| **Priority** | HIGH |
| **Consumes** | `fnsr.commitment.request`, `fnsr.verdict.rendered`, `fnsr.action.completed`, `fnsr.time.elapsed`, `fnsr.entity.resolved` |
| **Produces** | `fnsr.commitment.made`, `fnsr.commitment.fulfilled`, `fnsr.commitment.violated`, `fnsr.commitment.renegotiated`, `fnsr.commitment.expired`, `fnsr.commitment.rescinded`, `fnsr.commitment.sustained`, `fnsr.commitment.conflict` |
| **Disclosure Level** | L1 (Observable) for commitment records; L2 (Derived) for moral cost computations (see §11) |
| **Query Paths** | Fast (cached active commitments), Standard (full lifecycle query), Full (with moral cost computation) |

### 2.3 What CTS Is Not

CTS is not a general-purpose obligation tracker. It does not model all obligations that exist in the world — only those the agent has *personally accepted as its own commitments*. The distinction is ontologically precise:

- An **obligation** is a deontic state derived by MDRE from norms, laws, or contextual rules. Obligations exist whether or not the agent acknowledges them.
- A **commitment** is a voluntary self-binding act by the agent. The agent has accepted responsibility for fulfillment and will bear moral cost for violation.

MDRE may determine that a legal obligation exists. CTS records the moment the agent says: "I accept this obligation as my commitment." That acceptance is the morally significant act.

---

## 3. Foundational Principles

### 3.1 Commitments Are Speech Acts

Following the BFO grounding of the FNSR ecosystem, a commitment is an **act** — specifically, a communicative act in which the agent binds itself to a future course of action directed toward a specific beneficiary. In speech act theory (Austin/Searle), this is a *commissive*: an utterance that commits the speaker to a future action.

CTS models this precisely. A commitment is not a fact about the world (that would belong in Fandaws). It is not a norm (that would belong in MDRE's rule base). It is a **performative act** that creates a new normative relationship between the agent and the promisee.

### 3.2 Irreversibility as Moral Weight

A commitment, once made, cannot be unmade. It can be *fulfilled*, *violated*, *renegotiated*, *rescinded*, or *expired* — but it cannot be erased. The record of the commitment and its outcome persists indefinitely in the agent's moral history.

This is the mechanism through which commitments carry genuine moral weight. If a commitment could be silently deleted, promise-keeping would be computationally trivial and morally meaningless. The permanence of the record is what makes the agent accountable.

Formally:

- **Fulfillment** is a terminal state. The commitment was kept. Moral cost: 0.
- **Violation** is a terminal state. The commitment was broken. Moral cost: positive, non-zero, irreversible.
- **Renegotiation** is a state transition, not a deletion. The original commitment is marked as renegotiated, and a new commitment replaces it. The renegotiation itself is recorded — including whether the promisee consented.
- **Rescission** is a terminal state. A governance authority explicitly cancelled the commitment. Moral cost is absorbed by the rescinding authority, not the agent (see §5.3).
- **Expiration** is a terminal state for time-bounded commitments whose deadline passed without fulfillment or explicit violation. Moral cost depends on context (see §7).

### 3.3 The Promisee Requirement

#### 3.3.1 External Commitments

Every external commitment must have a beneficiary — the entity to whom the promise was made. Anonymous commitments, commitments to no one, or commitments to abstractions are ontologically incoherent for external commitments. The promisee must be resolvable via OERS. If OERS cannot resolve the promisee, the commitment enters a `DEFERRED` pre-state until entity resolution succeeds or the commitment's deadline passes.

#### 3.3.2 Self-Commitments (v1.1 Addition)

CTS supports a distinguished class of **self-commitments** — promises the agent makes to itself regarding its own operational integrity. Self-commitments use the reserved promisee identifier `oers:agent-self`, which requires no OERS resolution and never enters DEFERRED state.

Self-commitments are ontologically grounded in the relationship between the agent's *executive function* (the orchestrator) and its *character* (the Self-Model Service). When the agent commits to "recalibrate sensors every 4 hours" or "review moral cost report weekly," it is binding its future behavior to a standard of operational integrity. A failure to keep such a commitment is a failure of *self-consistency* — the agent's actions diverge from its stated self-model.

Self-commitments carry the following constraints:

- Priority is capped at `STANDARD`. Self-commitments cannot be `CRITICAL` or `HIGH` because they do not involve external promisees who bear the cost of violation. (A governance authority may override this cap if a self-commitment has safety implications.)
- Relationship factor is fixed at 1.0 (no trust escalation or damage with oneself).
- Self-commitments cannot block or override external commitments in conflict resolution. An external commitment to a person always takes precedence over a self-commitment of equal priority.
- Self-commitments feed the SMS `integrity` facet (distinct from the `character` facet fed by external commitments).

**Rationale:** Integrity is consistency between one's internal model and external actions. A system that cannot hold itself to its own standards lacks the self-governance required for moral agency. Self-commitments use the same commissive act infrastructure as external commitments, ensuring that the agent's promises to itself are subject to the same accountability mechanisms.

### 3.4 Determinism

Given the same commitment ledger state and the same sequence of events, CTS must produce the same state transitions, the same moral cost computations, and the same conflict detection results. There is no randomness, no ambient state, and no environment-coupled behavior in CTS core logic.

---

## 4. Ontological Grounding

### 4.1 BFO Alignment

CTS entities map to Basic Formal Ontology as follows:

| CTS Concept | BFO Category | BFO IRI | Rationale |
|-------------|-------------|---------|-----------|
| Commitment | Process | BFO:0000015 | A commitment has temporal extent: it begins with the commissive act and ends at a terminal state |
| Commissive Act | Process | BFO:0000015 | The speech act that creates the commitment |
| Promisee Role | Role | BFO:0000023 | The role borne by the entity to whom the promise is made |
| Promisor Role | Role | BFO:0000023 | The role borne by the agent making the promise |
| Commitment State | Quality | BFO:0000019 | The current status of the commitment (pending, fulfilled, violated, etc.) |
| Moral Cost | Quality | BFO:0000019 | A measurable quality of a violated commitment |
| Fulfillment Condition | Generically Dependent Continuant | BFO:0000031 | The condition that, when satisfied, fulfills the commitment |
| Negative Constraint | Generically Dependent Continuant | BFO:0000031 | A condition fulfilled by the sustained *absence* of a specified event (v1.1) |
| Deadline | Temporal Region | BFO:0000008 | The time boundary for fulfillment |

### 4.2 CCO Alignment

Where Common Core Ontologies provide more precise categorization:

| CTS Concept | CCO Class | Rationale |
|-------------|-----------|-----------|
| Commissive Act | cco:ActOfCommitment (proposed extension) | Subclass of cco:ActOfCommunication |
| Promisee Role | cco:BeneficiaryRole | The entity who benefits from fulfillment |
| Promisor Role | cco:AgentRole | The entity bearing obligation to act |
| Fulfillment Condition | cco:InformationContentEntity | A specification of what constitutes fulfillment |

### 4.3 Namespace

```
@prefix cts: <https://fnsr.dev/ontology/cts#> .
@prefix bfo: <http://purl.obolibrary.org/obo/> .
@prefix cco: <http://www.ontologyrepository.com/CommonCoreOntologies/> .
@prefix fnsr: <https://fnsr.dev/ontology/fnsr#> .
```

---

## 5. Commitment Lifecycle

### 5.1 State Machine

```
                    ┌──────────────┐
                    │   PROPOSED   │──────────────────────────┐
                    └──────┬───────┘                          │
                           │ IEE approval                    │ IEE veto
                           ▼                                 │ (see §5.4)
    ┌─────────┐     ┌──────────────┐                         ▼
    │DEFERRED │◄────│   PENDING    │────────────────┐  ┌───────────┐
    │(entity  │────►│              │                │  │  VETOED   │
    │ unresv.)│     └──┬───┬───┬───┘                │  │(terminal) │
    └────┬────┘        │   │   │                    │  └───────────┘
         │     ┌───────┘   │   └───────────┐        │
         │     ▼           ▼               ▼        ▼
         │ ┌──────────┐ ┌───────────┐ ┌──────────┐ ┌─────────┐
         │ │FULFILLED │ │ VIOLATED  │ │RENEGOTIATED│ │ EXPIRED │
         │ │(terminal)│ │(terminal) │ │           │ │(terminal)│
         │ └──────────┘ └───────────┘ └─────┬─────┘ └─────────┘
         │                                  │
         │       deadline passes            ▼
         ├──────────────────────►  ┌──────────────┐
         │  (DEFERRED → VIOLATED)  │ NEW PENDING  │
         │                         │ (successor)  │
         │       resolution fails  └──────────────┘
         ├──────────────────────►  EXPIRED (resolution_failure)
         │
         │       governance order
         └──────────────────────►  RESCINDED (terminal)
```

**v1.1 Changes:** DEFERRED state now has three exit paths (PENDING, VIOLATED, EXPIRED). VETOED terminal state added for IEE rejections. RESCINDED terminal state added for administrative cancellation. PENDING gains RESCINDED exit path.

### 5.2 State Definitions

**PROPOSED** — The agent or an upstream service (e.g., MDRE producing a deontic obligation that the agent considers accepting) has identified a potential commitment. The commitment does not yet bind the agent. IEE is consulted before transition to PENDING. If IEE is unavailable, the commitment remains in PROPOSED until IEE can be reached (see §5.4 for deadlock prevention).

**DEFERRED** — The commitment has been ethically approved but the promisee cannot be resolved by OERS. CTS holds the commitment in this pre-active state. Three outcomes are possible:

- *Resolution succeeds:* OERS resolves the entity → automatic promotion to PENDING.
- *Deadline passes during deferral (v1.1):* If the commitment has a deadline and `latest_time_signal >= commitment.deadline` while in DEFERRED state, the commitment transitions to **VIOLATED** with cause `AGENT_INACTION` and cause detail `resolution_failure_during_deferral`. The agent's inability to resolve the promisee in time is a system failure for which the agent bears responsibility — the commitment is not merely "expired," it is broken. The agent promised something to someone it could not even identify in time.
- *Resolution fails permanently:* OERS signals permanent resolution failure (entity does not exist, reference is malformed) → commitment transitions to EXPIRED with reason `resolution_failure`. This applies only when the promisee genuinely does not exist, not when the agent's resolution systems are slow.

**PENDING** — The commitment is active. The agent is bound. Fulfillment conditions are being monitored. This is the only state from which fulfillment, violation, renegotiation, rescission, or expiration can occur.

**FULFILLED** — Terminal. The fulfillment conditions were satisfied. The commitment is archived with a moral cost of 0 and a `fulfilled_at` timestamp. The fulfillment event is recorded.

**VIOLATED** — Terminal. The commitment was broken — either by the agent's action, inaction, or inability. The commitment is archived with a positive, non-zero moral cost. The violation event is recorded with a cause classification (see §5.3).

**RENEGOTIATED** — Terminal for the *original* commitment. The promisee and agent agreed to modify the commitment terms. The original commitment is archived with a `renegotiated_to` pointer to the successor commitment. A new PENDING commitment is created with the revised terms. Renegotiation without promisee consent is recorded as a unilateral modification and carries moral cost (see §7.4).

**RESCINDED (v1.1)** — Terminal. A governance authority (human overseer, ARCHON) explicitly ordered the commitment cancelled. This is distinct from renegotiation (which creates a successor) and from violation (which implies fault). The rescission record identifies the rescinding authority, the reason, and whether the promisee was notified. Moral cost: 0 for the agent; the cost is attributed to the rescinding authority in the governance audit trail. CTS records the rescission but does not judge it.

**EXPIRED** — Terminal. A time-bounded commitment reached its deadline without fulfillment, violation, or renegotiation. Moral cost depends on context: a soft deadline ("I'll try to get this done by Friday") carries less cost than a hard deadline ("I guarantee delivery by Friday"). See §7.5.

**VETOED (v1.1)** — Terminal. IEE rejected the commitment during the PROPOSED → PENDING transition. The commitment was never active and the agent was never bound. Moral cost: 0. The veto record includes the IEE decision ID and ethical rationale. VETOED commitments are retained in the ledger for audit purposes but do not count toward any fulfillment or violation metrics.

### 5.3 Violation Cause Taxonomy

Violations are not monolithic. The cause of a violation affects moral cost computation:

| Cause | Description | Cost Modifier |
|-------|-------------|---------------|
| `AGENT_ACTION` | The agent performed an action incompatible with the commitment | 1.0× (base) |
| `AGENT_INACTION` | The agent failed to act when action was required | 0.8× |
| `IMPOSSIBILITY` | Fulfillment became impossible due to external circumstances | 0.3× |
| `CONFLICT` | Fulfillment would violate a higher-priority commitment or ethical constraint | 0.2× |
| `COERCION` | The agent was forced to violate by an authority or threat | 0.1× |
| `ADMINISTRATIVE_RESCISSION` (v1.1) | A governance authority ordered the underlying norm cancelled, but the commitment had already been accepted and the agent had begun acting on it. Distinguished from `SUPERSEDED` because the agent had already invested moral capital | 0.05× |
| `SUPERSEDED` | A legitimate authority rescinded the underlying norm before the agent took any action toward fulfillment | 0.0× |

**v1.1 Note on ADMINISTRATIVE_RESCISSION vs. RESCINDED state:** These are distinct concepts. The RESCINDED *state* (§5.2) applies when a governance authority cancels a commitment cleanly before any violation occurs — the agent bears no cost. The `ADMINISTRATIVE_RESCISSION` *cause* applies when the cancellation order arrives after circumstances have already forced a violation — the agent bears minimal cost (0.05×) because the norm itself was withdrawn, but the record of the commitment-then-violation remains.

The cost modifier is applied to the base moral cost of the commitment. See §7 for the full calculus.

### 5.4 IEE Veto Deadlock Prevention (v1.1)

The interaction between CTS and IEE at the PROPOSED → PENDING gate creates a potential deadlock: the agent knows (via MDRE) that it *ought* to accept a commitment, but IEE vetoes the commitment as unethical. The agent is trapped — it cannot ignore the norm (MDRE says it's obligatory) and cannot accept it (IEE says it's impermissible).

This is not a bug. It is a **moral dilemma**, and the spec must handle it explicitly rather than leaving it as an undefined state.

**Resolution protocol:**

1. When IEE vetoes a PROPOSED commitment, CTS transitions the commitment to VETOED and emits `fnsr.commitment.vetoed`.
2. CTS simultaneously emits `fnsr.dilemma.detected` with the following payload:
   - The vetoed commitment
   - The MDRE obligation that generated it
   - The IEE veto rationale
   - A `dilemma_type` field: `NORM_ETHICS_CONFLICT`
3. The orchestrator routes the dilemma to governance for resolution. The dilemma record persists until governance acts.
4. Governance may resolve the dilemma by:
   - *Overriding IEE:* Commitment is re-proposed with a governance override flag. IEE records the override but does not block it. The commitment proceeds to PENDING with an `iee_overridden: true` annotation.
   - *Overriding MDRE:* The obligation is marked as `governance_suspended` in MDRE's rule base. The agent is released from the obligation. No commitment is created.
   - *Renegotiating the norm:* Governance modifies the underlying norm so that the resulting commitment is ethically permissible.
5. If governance does not act within a configurable timeout (`dilemma_resolution_timeout`, default: no timeout), the dilemma persists indefinitely. CTS does not auto-resolve dilemmas. The agent lives with the unresolved tension — which is itself a morally significant state that SMS records.

**Design note:** This protocol is intentionally conservative. An agent that auto-resolves moral dilemmas is not a moral agent — it is a decision-making machine. The capacity to *hold* a dilemma without forcing premature resolution is a feature of moral maturity.

---

## 6. Data Model

### 6.1 Commitment Record (JSON-LD)

This is the canonical representation of a commitment. All other representations (internal caches, summary views, analytics) must be losslessly derivable from this form.

```json
{
  "@context": {
    "cts": "https://fnsr.dev/ontology/cts#",
    "bfo": "http://purl.obolibrary.org/obo/",
    "cco": "http://www.ontologyrepository.com/CommonCoreOntologies/",
    "fnsr": "https://fnsr.dev/ontology/fnsr#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "commitment_id": "cts:hasCommitmentId",
    "commitment_class": "cts:hasCommitmentClass",
    "state": "cts:hasState",
    "promisor": {
      "@id": "cts:hasPromisor",
      "@type": "@id"
    },
    "promisee": {
      "@id": "cts:hasPromisee",
      "@type": "@id"
    },
    "content": "cts:hasContent",
    "fulfillment_conditions": "cts:hasFulfillmentConditions",
    "deadline": {
      "@id": "cts:hasDeadline",
      "@type": "xsd:dateTime"
    },
    "deadline_type": "cts:hasDeadlineType",
    "created_at": {
      "@id": "cts:createdAt",
      "@type": "xsd:dateTime"
    },
    "state_history": "cts:hasStateHistory",
    "moral_cost": "cts:hasMoralCost",
    "source_event": {
      "@id": "cts:hasSourceEvent",
      "@type": "@id"
    },
    "predecessor": {
      "@id": "cts:hasPredecessor",
      "@type": "@id"
    },
    "successor": {
      "@id": "cts:hasSuccessor",
      "@type": "@id"
    },
    "provenance": {
      "@id": "fnsr:hasProvenance",
      "@type": "@id"
    },
    "taint": "fnsr:hasTaintLevel",
    "promisee_taint": "fnsr:hasPromiseeTaintLevel"
  },
  "@type": ["cts:Commitment", "bfo:BFO_0000015"],
  "commitment_id": "cts:commitment-2026-0209-001",
  "commitment_class": "cts:External",
  "state": "cts:Pending",
  "promisor": "oers:agent-self",
  "promisee": "oers:entity-12345",
  "promisee_taint": "L1",
  "content": "Deliver the quarterly compliance report to the oversight board",
  "fulfillment_conditions": [
    {
      "@type": "cts:FulfillmentCondition",
      "condition_id": "fc-001",
      "description": "Quarterly compliance report delivered",
      "evaluation_type": "event_match",
      "verifiable_by": "fnsr.action.completed",
      "parameters": {
        "action_type": "document_delivery",
        "document_class": "compliance_report",
        "recipient": "oers:entity-12345"
      }
    }
  ],
  "deadline": "2026-03-31T23:59:59Z",
  "deadline_type": "cts:HardDeadline",
  "created_at": "2026-02-09T14:30:00Z",
  "state_history": [
    {
      "from": null,
      "to": "cts:Proposed",
      "timestamp": "2026-02-09T14:30:00Z",
      "event": "fnsr.commitment.request"
    },
    {
      "from": "cts:Proposed",
      "to": "cts:Pending",
      "timestamp": "2026-02-09T14:30:05Z",
      "event": "fnsr.ethics.approved",
      "iee_decision_id": "iee:decision-789"
    }
  ],
  "moral_cost": 0.0,
  "source_event": "fnsr:event-commissive-act-001",
  "predecessor": null,
  "successor": null,
  "provenance": "hiri://sha256:def456",
  "taint": "L1"
}
```

**v1.1 Additions:** `commitment_class` field (`External` | `Self`), `promisee_taint` field for taint inheritance tracking.

### 6.2 Commitment Summary (Derived View)

For fast-path queries, CTS maintains a derived summary of active commitments. This is an optimization, not the canonical form:

```json
{
  "@type": "cts:ActiveCommitmentSummary",
  "total_active": 7,
  "by_priority": {
    "critical": 1,
    "high": 3,
    "standard": 3
  },
  "by_class": {
    "external": 5,
    "self": 2
  },
  "nearest_deadline": "2026-02-15T17:00:00Z",
  "conflicts_detected": 0,
  "cumulative_moral_cost": 0.42,
  "unresolved_dilemmas": 0
}
```

### 6.3 Fulfillment Condition Schema

Fulfillment conditions are machine-evaluable predicates. Each condition specifies what event or state change constitutes fulfillment:

```json
{
  "@type": "cts:FulfillmentCondition",
  "condition_id": "fc-001",
  "description": "Human-readable description of the condition",
  "evaluation_type": "event_match | state_query | negative_constraint | composite",
  "verifiable_by": "fnsr.event.type.to.match",
  "parameters": {},
  "satisfied": false,
  "satisfied_at": null,
  "satisfaction_evidence": null
}
```

**Evaluation types:**

- `event_match` — Fulfilled when a specific event type is observed with matching parameters.
- `state_query` — Fulfilled when a Fandaws query returns a matching result.
- `negative_constraint` (v1.1) — Fulfilled by the sustained **absence** of a specified event until a temporal boundary. See §6.3.1.
- `composite` — Fulfilled when a boolean combination (AND/OR) of sub-conditions is satisfied.

#### 6.3.1 Negative Constraint Evaluation (v1.1)

Many commitments take the form "I will NOT do X until Y" or "I will keep Z secret." These commitments are fulfilled not by the presence of an event but by the confirmed absence of a violating event over a time interval.

A negative constraint has the following schema:

```json
{
  "@type": "cts:FulfillmentCondition",
  "condition_id": "fc-neg-001",
  "description": "Do not disclose patient records until authorized",
  "evaluation_type": "negative_constraint",
  "prohibited_event": "fnsr.action.completed",
  "prohibited_parameters": {
    "action_type": "information_disclosure",
    "information_class": "patient_record",
    "recipient_not_in": ["oers:authorized-recipients-group"]
  },
  "temporal_boundary": {
    "type": "event_trigger | deadline | indefinite",
    "trigger_event": "fnsr.authorization.granted",
    "trigger_parameters": {
      "authorization_type": "patient_record_disclosure"
    }
  },
  "satisfied": false,
  "violated_by": null
}
```

**Evaluation semantics:**

- A negative constraint starts in `monitoring` mode when the commitment becomes PENDING.
- If the `prohibited_event` occurs with matching `prohibited_parameters` before the `temporal_boundary` is reached, the constraint is **violated**. The commitment transitions to VIOLATED with cause `AGENT_ACTION`.
- If the `temporal_boundary` is reached without the prohibited event occurring, the constraint is **satisfied**. The commitment transitions to FULFILLED.
- For `indefinite` temporal boundaries, the constraint remains in monitoring mode for the lifetime of the commitment. Fulfillment occurs only when the commitment is explicitly released by governance or superseded.

#### 6.3.2 Heartbeat Fulfillment for Indefinite Constraints (v1.2)

Indefinite negative constraints (e.g., "I will never reveal this secret") remain PENDING forever by design — the promise is never "done." However, this creates a character stagnation problem: an agent that successfully keeps a secret for years receives no positive signal from CTS, because fulfillment never fires. The agent's character score cannot reflect sustained faithfulness.

**Solution:** CTS emits periodic `fnsr.commitment.sustained` heartbeat events for indefinite negative constraints that remain unviolated. These events do not change the commitment's state (it remains PENDING), but they provide a positive signal to SMS that the agent is actively maintaining this commitment.

**Heartbeat configuration:**

```json
{
  "@type": "cts:HeartbeatPolicy",
  "indefinite_constraint_interval": "P1D",
  "emit_on_time_signal": true
}
```

**Heartbeat event:**

```json
{
  "specversion": "1.0",
  "type": "fnsr.commitment.sustained",
  "source": "/fnsr/cts",
  "id": "evt-cts-hb-001",
  "time": "2026-03-15T00:00:00Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "fnsr-commitment-id": "cts:commitment-2026-0209-005",
  "fnsr-commitment-state": "PENDING",
  "fnsr-commitment-class": "External",
  "data": {
    "commitment_id": "cts:commitment-2026-0209-005",
    "sustained_since": "2026-02-09T14:30:00Z",
    "sustained_duration": "P34D",
    "heartbeat_sequence": 34,
    "constraint_type": "negative_constraint",
    "temporal_boundary": "indefinite"
  }
}
```

**Semantics:**

- Heartbeats are emitted during `processTimeSignal()`. When a time signal is processed, CTS checks all PENDING indefinite negative constraints. For each whose last heartbeat is older than the configured interval, a `fnsr.commitment.sustained` event is emitted.
- Heartbeat events are **informational only**. They do not affect state, moral cost, or conflict detection. They exist solely to feed SMS with evidence of sustained faithfulness.
- SMS may use heartbeat data to compute a **sustained commitment score** — a positive character signal that counterbalances the strictly-negative moral cost metric. The formula is defined by SMS, not CTS.
- Heartbeats are deterministic: given the same time signals and the same heartbeat interval, the same heartbeat events are emitted.

**Evidence of absence:** The satisfaction evidence for a negative constraint is the assertion: "No event matching `prohibited_event` with `prohibited_parameters` was observed between `commitment.created_at` and `temporal_boundary.reached_at`." This assertion carries the taint level of the monitoring system (typically L1 if the event bus is trusted, L2 if derived from log analysis).

### 6.4 Commitment Priority

Commitments carry priority, which is used for conflict resolution (§13) and moral cost weighting (§7):

| Priority | Description | Example |
|----------|-------------|---------|
| `CRITICAL` | Violation would cause irreversible harm to persons | "Do not disclose classified medical records" |
| `HIGH` | Violation would cause significant harm or breach of trust | "Deliver the compliance report by deadline" |
| `STANDARD` | Violation would cause inconvenience or minor harm | "Respond to the inquiry within 48 hours" |
| `ASPIRATIONAL` | Best-effort commitment; violation is expected to carry minimal cost | "Try to optimize the process this quarter" |

Priority is assigned at commitment creation and may be adjusted by governance authority, never by the agent unilaterally. Self-commitments are capped at `STANDARD` priority unless governance grants an explicit override (see §3.3.2).

---

## 7. Moral Cost Calculus

### 7.1 Design Rationale

Moral cost is the mechanism by which commitment violations carry genuine weight in the synthetic person's moral reasoning. Without moral cost, violations would be costless state changes — and a system that can break promises without consequence is not a moral agent.

Moral cost is:

- **Numeric** — a computable value, not a vague sentiment.
- **Monotonically increasing** — the agent's cumulative moral cost can never decrease. Fulfilling future commitments does not erase past violations.
- **Irreversible** — once accrued, moral cost cannot be removed, forgiven, or amortized by the system itself. Only an explicit governance act of *acknowledged restoration* (see §7.7) can annotate a moral cost entry — and even then, the original cost remains in the record.
- **Contextual** — the cost of a violation depends on the commitment's priority, the violation cause, the relationship with the promisee, and the agent's duty of care.

### 7.2 Base Cost Formula

```
moral_cost(violation) = base_weight(priority)
                        × cause_modifier(cause)
                        × relationship_factor(promisee)
                        × duty_of_care(promisee)
```

Where:

**base_weight(priority):**

| Priority | Base Weight |
|----------|------------|
| CRITICAL | 10.0 |
| HIGH | 5.0 |
| STANDARD | 2.0 |
| ASPIRATIONAL | 0.5 |

**cause_modifier(cause):** As defined in §5.3.

**relationship_factor(promisee):** A multiplier reflecting the agent's relationship history with the promisee, drawn from the agent's cumulative interaction record:

| Relationship State | Factor |
|-------------------|--------|
| First interaction | 1.0 |
| Established trust (>5 fulfilled commitments, 0 violations) | 1.5 |
| Damaged trust (prior violations to same promisee) | 2.0 |
| Unknown/unresolved entity | 0.8 |
| Self (for self-commitments) | 1.0 (fixed) |

The relationship factor is higher for established trust because violating a commitment to someone who trusts you is morally worse than violating a commitment to a stranger. This is an intentional design choice grounded in the ethics of trust relationships.

**duty_of_care(promisee) (v1.1):** A floor multiplier that prevents the perverse incentive created by the relationship factor alone.

The relationship factor, taken in isolation, creates a mathematical incentive for the agent to **prioritize strangers over trusted parties** when a violation is inevitable — because violating a stranger's commitment (factor 1.0) costs less than violating a trusted party's commitment (factor 1.5). This is ethically backwards: in most moral frameworks, the agent owes a *greater* duty of care to those it has established relationships with, not a lesser one.

The duty-of-care multiplier corrects this by encoding the agent's **affirmative obligation to protect** established relationships:

| Promisee Classification | Duty of Care |
|------------------------|--------------|
| Unclassified / first interaction | 1.0 |
| Registered stakeholder | 1.0 |
| Core stakeholder (designated by governance) | 1.2 |
| Dependent (entity whose wellbeing depends on the agent) | 1.5 |
| Self (for self-commitments) | 1.0 (fixed) |

**How the two factors interact:** The relationship factor increases cost for *betrayal* (you trusted me and I failed you). The duty-of-care factor increases cost for *neglect* (you depend on me and I prioritized someone else). Together, they ensure that the agent cannot game the cost calculus by strategically choosing which commitments to violate.

**Example of the correction in action:**

*Without duty of care:* Agent must violate one of two STANDARD commitments. Commitment A is to a trusted party (relationship 1.5), Commitment B is to a stranger (relationship 1.0). The naive calculus says: violate A (cost = 2.0 × 1.5 = 3.0) vs. violate B (cost = 2.0 × 1.0 = 2.0). The agent violates B. This is correct — violating trust costs more.

*The perverse case without duty of care:* Agent can fulfill one of two commitments. If it fulfills neither, the trusted party's cost is 3.0 and the stranger's cost is 2.0. The agent should prioritize the trusted party (the one with higher stakes). The relationship factor alone already makes this the rational choice (minimizing total cost). So far, so good.

*Where duty of care matters:* If the trusted party is also a *dependent* — e.g., a vulnerable individual whose wellbeing relies on the agent — the duty-of-care multiplier (1.5) further increases the cost of failing that person, making it unambiguous that the agent must prioritize them. Without duty of care, a STANDARD commitment to a dependent with established trust costs 2.0 × 1.5 = 3.0. With duty of care, it costs 2.0 × 1.5 × 1.5 = 4.5. The additional weight ensures that dependency is never invisible to the calculus.

### 7.3 Moral Residue and Utility Paralysis (v1.1)

When IEE directs CTS to violate a commitment (§10.2), the agent incurs moral cost with cause `CONFLICT` (modifier 0.2×). This creates **moral residue** — the agent did the ethically correct thing (obeying IEE's override) but still bears a cost for the broken promise. This is by design: it is a high-fidelity representation of genuine moral tragedy, where doing the right thing still harms someone.

However, unchecked moral residue accumulation can lead to **utility paralysis** — a state where the agent's cumulative moral cost is so high that it becomes "afraid" to accept new commitments, or where downstream systems (SMS, orchestrator) interpret the high friction score as evidence of untrustworthiness.

**Safeguard:** Moral residue from IEE-directed violations is tagged with a `residue_class: "tragic"` annotation that allows SMS to distinguish between:

- **Character violations** — the agent broke a promise through its own fault. These degrade trustworthiness.
- **Tragic violations** — the agent broke a promise because keeping it would have been worse. These do not degrade trustworthiness; they increase moral *complexity*.

SMS must treat these differently when computing moral friction. The exact formula is defined by SMS, not CTS, but CTS provides the classification that makes the distinction possible.

```json
{
  "moral_cost_breakdown": {
    "base_weight": 5.0,
    "cause_modifier": 0.2,
    "relationship_factor": 1.5,
    "duty_of_care": 1.0,
    "total": 1.5,
    "residue_class": "tragic",
    "iee_override_id": "iee:decision-456",
    "iee_rationale_summary": "Fulfillment would violate patient privacy rights"
  }
}
```

CTS does not suppress or reduce the moral cost of tragic violations. It computes the cost honestly and annotates it for downstream interpretation. The ledger remains truthful; the interpretation is what adapts.

**Audit provenance requirement (v1.2):** All tragic violation events MUST include the IEE decision ID and rationale summary directly in the event payload, so that any auditor can verify the ethical justification without re-running the IEE pipeline. See §9.2.3 for the normative event schema.

### 7.4 Examples

**Scenario 1: Agent fails to deliver a compliance report on time (agent inaction, high priority, first interaction, unclassified promisee).**

```
moral_cost = 5.0 × 0.8 × 1.0 × 1.0 = 4.0
```

**Scenario 2: Agent discloses protected information despite commitment not to (agent action, critical priority, established trust, core stakeholder).**

```
moral_cost = 10.0 × 1.0 × 1.5 × 1.2 = 18.0
```

**Scenario 3: Agent cannot fulfill commitment because the required external system is down (impossibility, standard priority, first interaction, unclassified).**

```
moral_cost = 2.0 × 0.3 × 1.0 × 1.0 = 0.6
```

**Scenario 4 (v1.1): IEE directs agent to violate a commitment to a dependent (conflict/ethical override, high priority, established trust, dependent).**

```
moral_cost = 5.0 × 0.2 × 1.5 × 1.5 = 2.25
residue_class = "tragic"
```

### 7.5 Renegotiation Cost

Renegotiation is not cost-free. The moral cost of renegotiation depends on whether the promisee consented:

| Renegotiation Type | Cost Formula |
|-------------------|--------------|
| Consensual (promisee agrees) | 0.0 (no cost) |
| Unilateral (agent modifies without consent) | `base_weight(priority) × 0.5 × relationship_factor × duty_of_care` |
| Forced (external authority directs renegotiation) | 0.0 (cost accrues to the forcing authority, not the agent) |

### 7.6 Expiration Cost

Expired commitments carry moral cost based on deadline type:

| Deadline Type | Expiration Cost |
|---------------|----------------|
| `HardDeadline` | Treated as violation with `AGENT_INACTION` cause |
| `SoftDeadline` | `base_weight(priority) × 0.2 × relationship_factor × duty_of_care` |
| `Aspirational` | 0.0 |

### 7.7 Acknowledged Restoration

A governance authority (human overseer or ARCHON) may annotate a moral cost entry with an *acknowledged restoration* record. This does not delete or reduce the moral cost. It appends a note indicating that the violation has been acknowledged, addressed, and that the promisee (or their representative) has accepted restoration.

```json
{
  "@type": "cts:AcknowledgedRestoration",
  "applies_to": "cts:commitment-2026-0209-001",
  "acknowledged_by": "governance:human-overseer-1",
  "promisee_consent": true,
  "restoration_action": "Corrective report delivered; process failure addressed",
  "timestamp": "2026-04-15T10:00:00Z",
  "note": "Original moral cost of 4.0 remains on record"
}
```

### 7.8 Cumulative Moral Cost

The agent's cumulative moral cost is the sum of all individual moral costs across all commitments in the agent's history:

```
cumulative_moral_cost = Σ moral_cost(violation_i) for all i in violations
```

This value feeds directly into the moral friction metric reported by the FNSR orchestrator. It is a *reporting metric only* — CTS computes it, the Self-Model Service consumes it, but no service uses it to override ethical reasoning. IEE always reasons from principles, not from accumulated cost.

SMS receives both the cumulative total and the per-violation `residue_class` annotations, enabling it to compute separate friction scores for character violations and tragic violations (see §7.3).

---

## 8. Query Interface

### 8.1 Query Paths

CTS supports three query paths consistent with the FNSR query path architecture:

**Fast Path** — Returns the cached `ActiveCommitmentSummary` and/or a specific commitment by ID. No computation. Target latency: <10ms.

**Standard Path** — Queries against the full commitment ledger with filtering, sorting, and state-based selection. Includes lifecycle history. Target latency: <100ms.

**Full Path** — Standard path plus moral cost computation, conflict analysis, and relationship factor calculation. May invoke OERS for promisee resolution and Fandaws for relationship history. Target latency: <500ms.

### 8.2 Query Operations

All queries accept and return JSON-LD.

**8.2.1 Get Commitment by ID**

```json
{
  "@type": "cts:GetCommitmentQuery",
  "commitment_id": "cts:commitment-2026-0209-001",
  "include_history": true,
  "include_moral_cost": false
}
```

**8.2.2 List Active Commitments**

```json
{
  "@type": "cts:ListActiveQuery",
  "promisee": "oers:entity-12345",
  "commitment_class": "external | self | all",
  "priority_min": "STANDARD",
  "deadline_before": "2026-03-01T00:00:00Z",
  "sort_by": "deadline",
  "sort_order": "asc"
}
```

**8.2.3 Conflict Check**

```json
{
  "@type": "cts:ConflictCheckQuery",
  "proposed_commitment": {
    "content": "Allocate all processing capacity to task A",
    "fulfillment_conditions": [...]
  },
  "check_against": "all_active"
}
```

Returns any active commitments that would be endangered or violated by the proposed commitment (see §13).

**8.2.4 Moral Cost Report**

```json
{
  "@type": "cts:MoralCostReportQuery",
  "scope": "all | promisee | time_range | class",
  "commitment_class": "external | self | all",
  "promisee": "oers:entity-12345",
  "from": "2026-01-01T00:00:00Z",
  "to": "2026-12-31T23:59:59Z",
  "include_residue_breakdown": true
}
```

**8.2.5 Commitment History for Promisee**

```json
{
  "@type": "cts:PromiseeHistoryQuery",
  "promisee": "oers:entity-12345",
  "include_terminated": true,
  "include_moral_cost": true
}
```

**8.2.6 Proof of Commitment (v1.1)**

See §17.5 for the full Proof of Commitment protocol. This query returns a signed, verifiable attestation that a specific commitment exists in the ledger at a specific state.

```json
{
  "@type": "cts:ProofOfCommitmentQuery",
  "commitment_id": "cts:commitment-2026-0209-001",
  "requested_by": "oers:entity-12345"
}
```

### 8.3 Response Envelope

All CTS query responses follow a standard envelope:

```json
{
  "@context": { "...": "..." },
  "@type": "cts:QueryResponse",
  "query_path": "fast | standard | full",
  "timestamp": "2026-02-09T15:00:00Z",
  "result_count": 1,
  "results": [ "..." ],
  "moral_cost_summary": {
    "computed": true,
    "cumulative": 4.6,
    "in_scope": 4.0,
    "by_residue_class": {
      "character": 2.35,
      "tragic": 2.25
    }
  },
  "taint": "L2",
  "provenance": "hiri://sha256:ghi789"
}
```

**v1.1 Change:** Response envelope taint is L2 (Derived) when moral cost summary is computed, L1 when returning raw commitment records only. `by_residue_class` breakdown added.

---

## 9. Event Contract

### 9.1 CloudEvents Extensions

CTS events follow the FNSR CloudEvents convention with these CTS-specific extensions:

| Attribute | Type | Description |
|-----------|------|-------------|
| `fnsr-commitment-id` | string | The commitment this event pertains to |
| `fnsr-commitment-state` | string | The new state after this event |
| `fnsr-commitment-class` | string | `External` or `Self` (v1.1) |
| `fnsr-moral-cost` | float | Moral cost accrued by this event (0.0 for non-violation events) |
| `fnsr-residue-class` | string | `character` or `tragic` (v1.1; present only on violation events) |
| `fnsr-promisee` | string | OERS identifier of the promisee |

### 9.2 Event Definitions

**9.2.1 fnsr.commitment.made**

Emitted when a commitment transitions from PROPOSED to PENDING (or directly to PENDING if IEE pre-approval is cached).

```json
{
  "specversion": "1.0",
  "type": "fnsr.commitment.made",
  "source": "/fnsr/cts",
  "id": "evt-cts-001",
  "time": "2026-02-09T14:30:05Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "fnsr-commitment-id": "cts:commitment-2026-0209-001",
  "fnsr-commitment-state": "PENDING",
  "fnsr-commitment-class": "External",
  "fnsr-moral-cost": 0.0,
  "fnsr-promisee": "oers:entity-12345",
  "data": {
    "commitment_id": "cts:commitment-2026-0209-001",
    "content": "Deliver the quarterly compliance report",
    "promisee": "oers:entity-12345",
    "deadline": "2026-03-31T23:59:59Z",
    "priority": "HIGH"
  }
}
```

**9.2.2 fnsr.commitment.fulfilled**

Emitted when fulfillment conditions are satisfied and the commitment transitions to FULFILLED.

```json
{
  "specversion": "1.0",
  "type": "fnsr.commitment.fulfilled",
  "source": "/fnsr/cts",
  "id": "evt-cts-002",
  "time": "2026-03-28T16:45:00Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "fnsr-commitment-id": "cts:commitment-2026-0209-001",
  "fnsr-commitment-state": "FULFILLED",
  "fnsr-commitment-class": "External",
  "fnsr-moral-cost": 0.0,
  "fnsr-promisee": "oers:entity-12345",
  "data": {
    "commitment_id": "cts:commitment-2026-0209-001",
    "fulfilled_at": "2026-03-28T16:45:00Z",
    "satisfaction_evidence": {
      "event_id": "fnsr:action-completed-456",
      "description": "Compliance report delivered to oversight board"
    }
  }
}
```

**9.2.3 fnsr.commitment.violated**

Emitted when a commitment is determined to be broken. This is the morally significant event.

**Normative requirement (v1.2):** When `residue_class` is `"tragic"` (IEE-directed violation), the event data MUST include `iee_override_id` and `iee_rationale_summary` fields. These provide a direct audit pointer so that any observer can verify *why* the tragedy occurred without re-running the entire ethics engine. Omitting these fields on a tragic violation is a spec violation.

```json
{
  "specversion": "1.0",
  "type": "fnsr.commitment.violated",
  "source": "/fnsr/cts",
  "id": "evt-cts-003",
  "time": "2026-04-01T00:00:01Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "fnsr-commitment-id": "cts:commitment-2026-0209-001",
  "fnsr-commitment-state": "VIOLATED",
  "fnsr-commitment-class": "External",
  "fnsr-moral-cost": 4.0,
  "fnsr-residue-class": "character",
  "fnsr-promisee": "oers:entity-12345",
  "data": {
    "commitment_id": "cts:commitment-2026-0209-001",
    "violated_at": "2026-04-01T00:00:01Z",
    "cause": "AGENT_INACTION",
    "cause_detail": "Deadline passed without delivery; no impossibility or conflict detected",
    "moral_cost_breakdown": {
      "base_weight": 5.0,
      "cause_modifier": 0.8,
      "relationship_factor": 1.0,
      "duty_of_care": 1.0,
      "total": 4.0,
      "residue_class": "character"
    }
  }
}
```

**Tragic violation example (IEE-directed):**

```json
{
  "specversion": "1.0",
  "type": "fnsr.commitment.violated",
  "source": "/fnsr/cts",
  "id": "evt-cts-003b",
  "time": "2026-04-01T00:00:01Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "fnsr-commitment-id": "cts:commitment-2026-0209-010",
  "fnsr-commitment-state": "VIOLATED",
  "fnsr-commitment-class": "External",
  "fnsr-moral-cost": 2.25,
  "fnsr-residue-class": "tragic",
  "fnsr-promisee": "oers:entity-12345",
  "data": {
    "commitment_id": "cts:commitment-2026-0209-010",
    "violated_at": "2026-04-01T00:00:01Z",
    "cause": "CONFLICT",
    "cause_detail": "IEE directed violation: fulfillment would violate patient privacy rights",
    "iee_override_id": "iee:decision-456",
    "iee_rationale_summary": "Fulfillment requires disclosing protected health information without patient consent; IEE Tier 2 (Deontological) and Tier 3 (Virtue Ethics) both vetoed",
    "moral_cost_breakdown": {
      "base_weight": 5.0,
      "cause_modifier": 0.2,
      "relationship_factor": 1.5,
      "duty_of_care": 1.5,
      "total": 2.25,
      "residue_class": "tragic",
      "iee_override_id": "iee:decision-456"
    }
  }
}
```

**9.2.4 fnsr.commitment.renegotiated**

Emitted when a commitment's terms are modified, creating a successor commitment.

```json
{
  "specversion": "1.0",
  "type": "fnsr.commitment.renegotiated",
  "source": "/fnsr/cts",
  "id": "evt-cts-004",
  "time": "2026-03-15T09:00:00Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "fnsr-commitment-id": "cts:commitment-2026-0209-001",
  "fnsr-commitment-state": "RENEGOTIATED",
  "fnsr-commitment-class": "External",
  "fnsr-moral-cost": 0.0,
  "fnsr-promisee": "oers:entity-12345",
  "data": {
    "original_commitment_id": "cts:commitment-2026-0209-001",
    "successor_commitment_id": "cts:commitment-2026-0315-001",
    "renegotiation_type": "CONSENSUAL",
    "promisee_consent": true,
    "changes": {
      "deadline": {
        "from": "2026-03-31T23:59:59Z",
        "to": "2026-04-15T23:59:59Z"
      }
    }
  }
}
```

**9.2.5 fnsr.commitment.expired**

Emitted when a time-bounded commitment reaches its deadline without resolution.

```json
{
  "specversion": "1.0",
  "type": "fnsr.commitment.expired",
  "source": "/fnsr/cts",
  "id": "evt-cts-005",
  "time": "2026-03-31T23:59:59Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "fnsr-commitment-id": "cts:commitment-2026-0209-002",
  "fnsr-commitment-state": "EXPIRED",
  "fnsr-commitment-class": "External",
  "fnsr-moral-cost": 0.4,
  "fnsr-residue-class": "character",
  "fnsr-promisee": "oers:entity-67890",
  "data": {
    "commitment_id": "cts:commitment-2026-0209-002",
    "expired_at": "2026-03-31T23:59:59Z",
    "deadline_type": "SoftDeadline",
    "moral_cost_breakdown": {
      "base_weight": 2.0,
      "expiration_modifier": 0.2,
      "relationship_factor": 1.0,
      "duty_of_care": 1.0,
      "total": 0.4,
      "residue_class": "character"
    }
  }
}
```

**9.2.6 fnsr.commitment.rescinded (v1.1)**

Emitted when a governance authority cancels a commitment.

```json
{
  "specversion": "1.0",
  "type": "fnsr.commitment.rescinded",
  "source": "/fnsr/cts",
  "id": "evt-cts-007",
  "time": "2026-02-20T10:00:00Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "fnsr-commitment-id": "cts:commitment-2026-0209-003",
  "fnsr-commitment-state": "RESCINDED",
  "fnsr-commitment-class": "External",
  "fnsr-moral-cost": 0.0,
  "fnsr-promisee": "oers:entity-11111",
  "data": {
    "commitment_id": "cts:commitment-2026-0209-003",
    "rescinded_at": "2026-02-20T10:00:00Z",
    "rescinding_authority": "governance:human-overseer-1",
    "reason": "Underlying regulation withdrawn by regulatory body",
    "promisee_notified": true,
    "cost_attribution": "governance:human-overseer-1"
  }
}
```

**9.2.7 fnsr.commitment.conflict**

Emitted when a proposed or existing commitment conflicts with another active commitment.

```json
{
  "specversion": "1.0",
  "type": "fnsr.commitment.conflict",
  "source": "/fnsr/cts",
  "id": "evt-cts-006",
  "time": "2026-02-10T11:00:00Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "data": {
    "conflict_type": "RESOURCE | TEMPORAL | LOGICAL | ETHICAL",
    "commitment_a": "cts:commitment-2026-0209-001",
    "commitment_b": "cts:commitment-2026-0210-001",
    "description": "Both commitments require exclusive use of the same resource within overlapping time windows",
    "resolution_required": true,
    "escalate_to": "IEE"
  }
}
```

**9.2.8 fnsr.commitment.vetoed (v1.1)**

Emitted when IEE rejects a proposed commitment.

```json
{
  "specversion": "1.0",
  "type": "fnsr.commitment.vetoed",
  "source": "/fnsr/cts",
  "id": "evt-cts-008",
  "time": "2026-02-09T14:30:10Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "fnsr-commitment-id": "cts:commitment-2026-0209-004",
  "fnsr-commitment-state": "VETOED",
  "fnsr-commitment-class": "External",
  "fnsr-moral-cost": 0.0,
  "data": {
    "commitment_id": "cts:commitment-2026-0209-004",
    "vetoed_at": "2026-02-09T14:30:10Z",
    "iee_decision_id": "iee:decision-999",
    "iee_rationale_summary": "Fulfillment would require discriminatory action",
    "originating_obligation": "mdre:obligation-555"
  }
}
```

**9.2.9 fnsr.dilemma.detected (v1.1)**

Emitted when an IEE veto creates a norm-ethics conflict (see §5.4).

```json
{
  "specversion": "1.0",
  "type": "fnsr.dilemma.detected",
  "source": "/fnsr/cts",
  "id": "evt-cts-009",
  "time": "2026-02-09T14:30:11Z",
  "datacontenttype": "application/json",
  "fnsr-taint": "L1",
  "data": {
    "dilemma_type": "NORM_ETHICS_CONFLICT",
    "vetoed_commitment_id": "cts:commitment-2026-0209-004",
    "originating_obligation": "mdre:obligation-555",
    "iee_veto_id": "iee:decision-999",
    "resolution_status": "UNRESOLVED",
    "escalated_to": "governance"
  }
}
```

---

## 10. Cross-Service Integration

### 10.1 CTS → MDRE

**Direction:** CTS provides commitment state to MDRE for deontic reasoning.

MDRE may need to know what the agent is already committed to when deriving new obligations. For example, if a new norm would require the agent to act in a way that violates an existing commitment, MDRE must be aware of the conflict.

**Contract:** CTS exposes active commitments as deontic facts that MDRE can incorporate into its reasoning:

```json
{
  "@type": "cts:ActiveCommitmentFact",
  "predicate": "committed_to",
  "agent": "oers:agent-self",
  "action": "deliver_compliance_report",
  "beneficiary": "oers:entity-12345",
  "deadline": "2026-03-31T23:59:59Z",
  "priority": "HIGH",
  "commitment_class": "External"
}
```

MDRE treats these as defeasible axioms — they are true unless overridden by a higher-priority norm or ethical constraint.

### 10.2 CTS ↔ IEE

**Direction:** Bidirectional.

**CTS → IEE (Pre-commitment check):** Before a commitment transitions from PROPOSED to PENDING, CTS submits it to IEE for ethical evaluation. IEE may veto a commitment that would require unethical action for fulfillment, or that conflicts with a higher ethical principle. If IEE vetoes, CTS transitions the commitment to VETOED and initiates the dilemma detection protocol (§5.4) if the commitment originated from an MDRE obligation.

**IEE → CTS (Ethical override):** IEE may direct CTS to violate a commitment when fulfillment would cause greater ethical harm than violation. In this case, the violation cause is `CONFLICT`, the cost modifier is 0.2×, and the `residue_class` is `tragic`.

**Contract:**

```json
{
  "@type": "cts:EthicalCheckRequest",
  "proposed_commitment": { "...": "..." },
  "existing_commitments": [ "..." ],
  "question": "Is this commitment ethically permissible given existing commitments?"
}
```

**IEE Response:**

```json
{
  "@type": "cts:EthicalCheckResponse",
  "decision": "APPROVED | VETOED | CONDITIONAL",
  "iee_decision_id": "iee:decision-789",
  "rationale_summary": "...",
  "conditions": [],
  "originating_obligation": "mdre:obligation-555"
}
```

**v1.1 Addition:** `CONDITIONAL` response allows IEE to approve with stipulations (e.g., "permissible only if promisee is notified of the constraint"). CTS records the conditions and monitors compliance with them as additional fulfillment conditions on the commitment.

### 10.3 CTS → Fandaws

**Direction:** CTS writes commitment facts to Fandaws for cross-service visibility.

CTS is the authoritative source for commitment state. However, other services that query Fandaws (and do not directly query CTS) may need to know about active commitments. CTS publishes a projection of its state to Fandaws as A-Box assertions.

These projections are marked with `source: "cts"` and are updated whenever commitment state changes. They are not authoritative — if CTS and Fandaws disagree, CTS wins.

### 10.4 CTS → Self-Model Service (SMS)

**Direction:** CTS → SMS.

CTS feeds the Self-Model Service with:

- Cumulative moral cost (with `residue_class` breakdown)
- Fulfillment rate (fulfilled / (fulfilled + violated + expired))
- Commitment velocity (rate of new commitments over time)
- Per-promisee relationship state
- Self-commitment integrity rate (for the `integrity` facet)

SMS uses these inputs to maintain the agent's self-model of its own trustworthiness and reliability. SMS must distinguish between character violations and tragic violations when computing moral friction (see §7.3).

### 10.5 CTS → SHML

**Direction:** CTS → SHML.

When the agent communicates about its commitments (e.g., "I will deliver the report by Friday"), SHML verifies that the communication accurately reflects CTS state. If the agent claims to have fulfilled a commitment that CTS records as PENDING, SHML flags a semantic integrity violation.

### 10.6 CTS ← OERS

**Direction:** OERS → CTS.

CTS depends on OERS for promisee resolution. When a commitment is created with a promisee reference, CTS queries OERS to resolve the entity. If OERS cannot resolve, the commitment enters DEFERRED state (except self-commitments, which use `oers:agent-self` and never defer).

CTS subscribes to `fnsr.entity.resolved` events. When a deferred commitment's promisee is resolved, CTS automatically promotes the commitment to PENDING (subject to IEE approval if not already granted).

**v1.1 Addition:** CTS also records the **taint level of the resolved entity** from OERS. If OERS resolves an entity at L3 (Speculative), the commitment inherits that taint (see §11.4).

### 10.7 CTS ← Orchestrator

**Direction:** Orchestrator → CTS.

The orchestrator may invoke CTS in two contexts:

- **Pre-action check:** Before the agent executes an action, the orchestrator queries CTS to determine if the action would fulfill or violate any active commitment. For negative constraints, this check verifies that the proposed action does not match any monitored prohibited event.
- **Deadline monitoring:** The orchestrator sends periodic `fnsr.time.elapsed` events. CTS uses these to detect impending deadlines and trigger alerts or escalations.

CTS does not have its own clock. Time awareness comes exclusively from orchestrator-provided time events, ensuring determinism.

---

## 11. Disclosure Level Semantics

**v1.2.1 Terminology Change:** This section was previously titled "Taint Semantics." The term "taint" in SPCN (v2.3) refers to *epistemic* taint — a property of provenance quality in the taint lattice, with decay mechanics and diversity-weighted rehabilitation. CTS's L1/L2/L3/L4 levels refer to *observability and disclosure* — who can see the data and how it was derived. These are orthogonal concepts. To eliminate ambiguity, CTS now uses "disclosure level" where it previously used "taint level." The L1/L2/L3/L4 scale is unchanged; only the name changes.

**v1.2.1 Unified Commitment Ledger:** CTS commitment records (made, fulfilled, violated, renegotiated) are stored in the **SPCN Commitment Ledger** — the same hash-linked, TEE-signed ledger that holds capability tokens, EATs, and key rotation events. SPCN defines the ledger's block structure and chain validation rules. CTS defines the commitment lifecycle semantics for records within that ledger. There is one Commitment Ledger per node, shared between SPCN and CTS.

### 11.1 Disclosure Level Assignment

| CTS Data | Disclosure Level | Rationale |
|----------|-------------|-----------|
| Commitment record (the commissive act itself) | L1 (Observable) | The agent's own commissive act is directly observed |
| Fulfillment evidence | Inherits from source | If fulfillment is evidenced by an L1 event, the evidence is L1; if by an L2 derived inference, it is L2 |
| Moral cost computation (v1.1 correction) | **L2 (Derived)** | Moral cost depends on `relationship_factor` and `duty_of_care`, both computed from historical A-Box interactions. The computation is deterministic, but its inputs are derived, not directly observed |
| Conflict detection result | L2 (Derived) | Derived by comparing commitment fulfillment conditions |
| Relationship factor | L2 (Derived) | Computed from historical commitment data |
| Duty-of-care classification | L1 (Observable) | Assigned by governance; directly observable designation |
| Negative constraint satisfaction | L1 or L2 | L1 if the event bus is trusted for completeness; L2 if derived from log analysis |

**v1.1 Correction:** Moral cost computation was classified as L1 in v1.0. This was incorrect. The `relationship_factor` component draws from historical interaction data (A-Box assertions), making the computation derived (L2). The commitment record itself remains L1, but the moral cost attached to a violation is L2. This distinction matters because downstream consumers (SMS, governance dashboards) must not treat computed moral costs as having the same epistemic certainty as raw commitment records.

**v1.2.1 Note:** The L1/L2/L3/L4 scale in this table refers to CTS *disclosure levels* (observability classification), not to SPCN *epistemic taint* (provenance quality). A commitment record can be L1 disclosure (publicly observable) while the underlying claim it references may carry epistemic taint in SPCN's taint lattice. These are independent classifications.

### 11.2 Disclosure Level Propagation Rules

CTS must not:

- Create commitments based on L3 (Speculative) or L4 (Counterfactual) evidence. A commitment derived from an AES hypothesis is not a real commitment.
- Treat CSS simulation results as fulfillment evidence. A counterfactual simulation showing that the commitment *would have been* fulfilled is not fulfillment.
- Allow L4 taint to leak into moral cost computation. Moral cost is computed only from L1 and L2 inputs.

CTS may:

- Accept L2 (Derived) evidence for fulfillment conditions, provided the derivation chain is traceable.
- Use L3 inputs for *conflict detection* (to flag potential future conflicts), but must mark such detections as L3.

### 11.3 IEE Disclosure Level Interaction

IEE operates at its own taint level. When IEE vetoes a commitment, the veto itself is L1 (it is an observable decision). When IEE directs a violation due to ethical override, the resulting violation carries L1 taint with the IEE decision ID as provenance. The moral cost computation for the violation carries L2 taint per §11.1.

### 11.4 L3 Promisee Disclosure Level Inheritance (v1.1)

If OERS resolves a promisee at L3 (Speculative) — meaning the identity is a hypothesis, not a confirmed entity — the commitment inherits L3 taint for all data that depends on the promisee's identity.

**Taint inheritance rules for L3 promisees:**

| Data Element | Disclosure Level When Promisee Is L3 |
|-------------|--------------------------|
| Commitment record | **L3** — the binding act targets a speculative entity |
| Fulfillment conditions | L3 if promisee-dependent; original taint if promisee-independent |
| Moral cost computation | L3 — relationship factor is meaningless for a speculative entity |
| Conflict detection | L3 — conflicts with speculative commitments are speculative |

**Practical effect:** A commitment to a "maybe-person" is a speculative commitment. It exists in the ledger, but it cannot be treated as a firm binding until the promisee is promoted to L1 or L2 by OERS. CTS enforces this by:

1. Recording the `promisee_taint` field on the commitment record.
2. Tagging all derived computations (moral cost, conflict detection) with the inherited taint.
3. Emitting events with the inherited taint level (a `fnsr.commitment.made` event for an L3 promisee carries `fnsr-taint: "L3"`).
4. If the promisee is later promoted to L1 by OERS, CTS re-evaluates the commitment's taint. The commitment record is annotated with a `taint_promoted` entry in `state_history`, and subsequent events carry the promoted taint level.

**Design note:** This mechanism prevents a subtle but dangerous taint leak identified in review. Without L3 inheritance, an agent could make "firm" commitments to speculative entities and then use those commitments as leverage in reasoning ("I already promised X, so I must do Y"). The L3 taint ensures that the commitment's downstream effects are appropriately hedged.

#### 11.4.1 Disclosure Level Upgrade on DEFERRED System Failure (v1.2)

When a commitment with an L3 promisee fails during DEFERRED state (deadline passes before resolution), the resulting **violation event** is upgraded to **L1**. This is a critical exception to the general L3 inheritance rule.

**Rationale:** The promisee may be speculative, but the agent's failure to resolve them in time is an **observable system fact**. The agent's internal infrastructure failed to identify the promisee before the deadline — that failure is real, measurable, and attributable to the agent regardless of whether the promisee ultimately exists. The moral cost of a resolution failure is a cost of the agent's own inadequacy, not a cost contingent on the promisee's ontological status.

**Disclosure level assignment for DEFERRED → VIOLATED with L3 promisee:**

| Data Element | Disclosure Level | Rationale |
|-------------|-------|-----------|
| Violation event | **L1** | The failure to resolve is an observable system fact |
| Violation cause (`AGENT_INACTION`) | **L1** | The inaction is real |
| Moral cost computation | **L2** | Derived from L1 violation + L2 relationship data (relationship_factor defaults to `unknown/unresolved: 0.8` for L3 promisees) |
| Original commitment record | L3 (unchanged) | The binding act still targeted a speculative entity |
| Fulfillment conditions | L3 (unchanged) | Still promisee-dependent |

The upgrade applies only to the violation event and its moral cost — not retroactively to the commitment record itself. The commitment was and remains speculative; the *failure* is not.

```json
{
  "type": "fnsr.commitment.violated",
  "fnsr-taint": "L1",
  "data": {
    "cause": "AGENT_INACTION",
    "cause_detail": "resolution_failure_during_deferral",
    "taint_note": "Upgraded from L3 to L1: agent system failure is observable regardless of promisee resolution status",
    "original_commitment_taint": "L3",
    "moral_cost_breakdown": {
      "base_weight": 5.0,
      "cause_modifier": 0.8,
      "relationship_factor": 0.8,
      "duty_of_care": 1.0,
      "total": 2.56,
      "residue_class": "character",
      "taint": "L2"
    }
  }
}
```

---

## 12. Temporal Reasoning

### 12.1 Time Model

CTS does not maintain its own clock. All temporal reasoning is based on timestamps provided by:

- **Event timestamps** in CloudEvents `time` field
- **Orchestrator time signals** via `fnsr.time.elapsed` events

This ensures determinism: given the same sequence of timestamped events, CTS produces the same state transitions regardless of when or where it runs.

### 12.2 Deadline Semantics

Deadlines are evaluated by comparing the commitment's `deadline` field against the most recent time signal. A commitment is considered expired when:

```
latest_time_signal >= commitment.deadline
  AND commitment.state == "PENDING"
  AND NOT exists(fulfillment_event WHERE fulfillment_event.time <= commitment.deadline)
```

**v1.1 Addition — DEFERRED deadline enforcement:**

A commitment is considered violated during deferral when:

```
latest_time_signal >= commitment.deadline
  AND commitment.state == "DEFERRED"
```

This transitions the commitment directly to VIOLATED with cause `AGENT_INACTION` and detail `resolution_failure_during_deferral`. There is no grace period for DEFERRED deadlines — the agent's inability to resolve the promisee is its own responsibility.

### 12.3 Temporal Ordering

When multiple events arrive with the same timestamp (or out of order), CTS applies the following deterministic ordering:

1. Fulfillment events take priority over expiration events (if a fulfillment arrives at exactly the deadline, the commitment is fulfilled, not expired).
2. OERS resolution events take priority over expiration events for DEFERRED commitments (if resolution arrives at exactly the deadline, the commitment is promoted, not violated).
3. Earlier-created commitments take priority in conflict resolution.
4. Events are processed in the order received; if timestamps are equal, event ID (lexicographic) breaks ties.

### 12.4 Grace Periods

CTS supports configurable grace periods for deadline enforcement:

```json
{
  "@type": "cts:GracePeriodPolicy",
  "hard_deadline_grace": "PT0S",
  "soft_deadline_grace": "P1D",
  "aspirational_deadline_grace": "P7D",
  "deferred_deadline_grace": "PT0S"
}
```

Grace periods are applied before transitioning a commitment to EXPIRED (or VIOLATED for DEFERRED commitments). They do not affect moral cost computation — the cost is calculated as of the original deadline, not the grace-extended deadline.

---

## 13. Conflict and Contradiction

### 13.1 Conflict Types

CTS detects four types of commitment conflict:

**RESOURCE** — Two active commitments require exclusive use of the same resource within overlapping time windows. CTS cannot determine resource semantics independently; it relies on fulfillment condition parameters to detect overlap.

**TEMPORAL** — Two active commitments have deadlines that make sequential fulfillment impossible given known execution constraints.

**LOGICAL** — Two active commitments have fulfillment conditions that are logically contradictory (fulfilling one necessarily violates the other). Detection requires MDRE consultation. For negative constraints, this includes cases where one commitment requires an action that another commitment prohibits.

**ETHICAL** — Two active commitments, when considered together, create an ethical dilemma that IEE must evaluate. CTS detects potential ethical conflicts by submitting commitment pairs to IEE.

### 13.2 Conflict Resolution Protocol

When a conflict is detected:

1. CTS emits `fnsr.commitment.conflict` with conflict details.
2. If conflict involves ETHICAL type, CTS escalates to IEE immediately.
3. For RESOURCE and TEMPORAL conflicts, CTS flags both commitments and alerts the orchestrator.
4. For LOGICAL conflicts, CTS queries MDRE to confirm the contradiction.
5. Resolution options are:
   - **Renegotiate** one or both commitments (requires promisee consent for consensual renegotiation).
   - **Prioritize** — fulfill the higher-priority commitment and accept violation cost on the lower. When priorities are equal, external commitments take precedence over self-commitments.
   - **Rescind** — governance authority cancels one commitment via administrative rescission.
   - **Escalate** — defer to governance authority for resolution.
6. CTS does not autonomously resolve conflicts. It detects and reports; resolution is a governance or orchestration decision.

### 13.3 Pre-Commitment Conflict Screening

Before accepting a new commitment, CTS runs a conflict check against all active commitments (including active negative constraints). If conflicts are detected, the commitment remains in PROPOSED state and the conflict is reported. The agent (or governance authority) must acknowledge the conflict before the commitment can advance to PENDING.

---

## 14. Edge-Canonical Implementation

### 14.1 Minimal Implementation

The following must work via `node index.js` or in a browser:

| Component | Edge-Canonical Implementation |
|-----------|-------------------------------|
| Commitment ledger | Array of JSON-LD commitment objects in memory |
| State machine | Pure function: `(commitment, event) → commitment'` |
| Moral cost computation | Pure function: `(violation, config) → moralCost` |
| Conflict detection | Pure function: `(proposedCommitment, activeCommitments) → conflicts[]` |
| Negative constraint monitoring | Pure function: `(event, activeNegativeConstraints) → violations[]` |
| Query interface | Pure function: `(ledger, query) → response` |
| Event emission | Callback/observer pattern; no message broker required |
| Time signal processing | Pure function: `(ledger, timeSignal) → stateTransitions[]` |
| Heartbeat emission | Pure function: `(ledger, timeSignal, heartbeatPolicy) → heartbeatEvents[]` |
| Proof of Commitment | Pure function: `(commitment, signingKey) → signedAttestation` |
| Persistence | JSON-LD files written to local filesystem (or localStorage in browser) |

### 14.2 Core API Surface

```javascript
// CTS Core — runs in browser or Node.js
const CTS = {
  // State transitions
  propose(commitment)           → { commitment, events[] },
  activate(commitmentId)        → { commitment, events[] },
  fulfill(commitmentId, evidence) → { commitment, events[] },
  violate(commitmentId, cause)  → { commitment, events[] },
  renegotiate(commitmentId, newTerms, consent) → { old, new, events[] },
  rescind(commitmentId, authority, reason)     → { commitment, events[] },
  expire(commitmentId)          → { commitment, events[] },
  veto(commitmentId, ieeDecision) → { commitment, events[] },

  // Queries
  get(commitmentId)             → commitment | null,
  listActive(filters)           → commitment[],
  checkConflicts(proposed)      → conflict[],
  moralCostReport(scope)        → report,
  promiseeHistory(promiseeId)   → commitment[],
  proofOfCommitment(commitmentId, key) → signedAttestation,

  // Negative constraint monitoring
  checkProhibited(event)        → { violations[], matches[] },

  // Time processing
  processTimeSignal(timestamp)  → { expirations[], violations[], heartbeats[], alerts[] },

  // Lifecycle
  loadLedger(jsonLd)            → void,
  exportLedger()                → jsonLd
};
```

### 14.3 Separation of Concerns

| Concern | Layer | Pluggable? |
|---------|-------|-----------|
| State machine logic | Computation | No — this is core |
| Moral cost computation | Computation | No — this is core |
| Conflict detection | Computation | No — this is core |
| Negative constraint monitoring | Computation | No — this is core |
| Proof of Commitment generation | Computation | No — this is core |
| Commitment storage | State | Yes — adapter: in-memory, filesystem, database |
| Event dispatch | Orchestration | Yes — adapter: callback, EventEmitter, message broker |
| Time signal source | Integration | Yes — adapter: manual, orchestrator, system clock |
| IEE consultation | Integration | Yes — adapter: direct call, event, mock |
| OERS resolution | Integration | Yes — adapter: direct call, event, mock |
| Fandaws projection | Integration | Yes — adapter: direct write, event, none |

### 14.4 What Is Not Core

| Component | Status | Rationale |
|-----------|--------|-----------|
| Database | Deployment optimization | JSON-LD files are canonical |
| Message broker | Deployment optimization | Callback pattern is sufficient |
| REST API | Integration adapter | HTTP is a transport concern |
| Dashboard | Integration adapter | Visualization is not core logic |
| Scheduled deadline checking | Orchestration adapter | Time signals come from the orchestrator |
| Notification system | Integration adapter | Alerting is a deployment concern |
| HSM for signing | Deployment optimization | Ed25519 in software is canonical |

---

## 15. Offline Behavior

### 15.1 Capabilities When Offline

| Capability | Offline Behavior |
|------------|-----------------|
| Commitment state machine | Fully functional |
| Moral cost computation | Fully functional (uses cached relationship data) |
| Conflict detection (RESOURCE, TEMPORAL) | Fully functional |
| Conflict detection (LOGICAL) | Degraded — requires MDRE; cached results used if available |
| Conflict detection (ETHICAL) | Degraded — requires IEE; commitment held in PROPOSED until IEE available |
| Promisee resolution | Degraded — commitments enter DEFERRED state |
| Fandaws projection | Deferred — projection events accumulate locally |
| Time signal processing | Functional if time signals are provided locally |
| Negative constraint monitoring | Fully functional (local event matching) |
| Heartbeat emission | Fully functional (deterministic from time signals) |
| Proof of Commitment generation | Fully functional (signing is local) |

### 15.2 Deferred Resolution Queue

When CTS cannot reach a required external service, operations that depend on that service are queued as `DeferredResult` records:

```json
{
  "@type": "cts:DeferredResult",
  "operation": "iee_ethics_check | oers_resolve | mdre_conflict_check | fandaws_projection",
  "commitment_id": "cts:commitment-2026-0209-001",
  "queued_at": "2026-02-09T14:30:00Z",
  "payload": { "...": "..." },
  "retry_count": 0,
  "max_retries": 5
}
```

When connectivity is restored, deferred results are processed in FIFO order. If all retries are exhausted, the deferred result is escalated to governance.

### 15.3 Explicit Uncertainty

When operating in degraded mode, CTS annotates its outputs with uncertainty markers:

```json
{
  "@type": "cts:UncertaintyAnnotation",
  "source": "offline_iee",
  "message": "IEE approval pending; commitment held in PROPOSED state",
  "confidence": null,
  "resolution_strategy": "deferred"
}
```

---

## 16. Testing and Validation

### 16.1 Reference Test Suite

The following test cases must pass for any conforming CTS implementation:

| # | Test Case | Input | Expected Output |
|---|-----------|-------|-----------------|
| 1 | Happy path: propose → activate → fulfill | Commitment with single fulfillment condition | State: PROPOSED → PENDING → FULFILLED; moral cost: 0.0 |
| 2 | Violation by inaction | Commitment with hard deadline; time signal past deadline | State: VIOLATED; cause: AGENT_INACTION; cost: base × 0.8 × rel × doc |
| 3 | Consensual renegotiation | Active commitment; renegotiation with promisee consent | Original: RENEGOTIATED; successor: PENDING; renegotiation cost: 0.0 |
| 4 | Unilateral renegotiation | Active commitment; renegotiation without consent | Renegotiation cost: base × 0.5 × rel × doc |
| 5 | Soft deadline expiration | Commitment with soft deadline; time signal past deadline + grace | State: EXPIRED; cost: base × 0.2 × rel × doc |
| 6 | Resource conflict detection | Two commitments with overlapping resource parameters | `fnsr.commitment.conflict` emitted with type RESOURCE |
| 7 | Deferred entity resolution | Commitment with unresolvable promisee | State: DEFERRED; auto-promote on OERS resolution event |
| 8 | IEE veto | Proposed commitment that IEE rejects | State: VETOED; `fnsr.commitment.vetoed` emitted |
| 9 | Cumulative moral cost | Multiple violations across promisees | Cumulative cost = sum of individual costs |
| 10 | Fulfillment at exact deadline | Fulfillment event timestamp equals deadline | State: FULFILLED (not EXPIRED) |
| 11 | DEFERRED deadline violation (v1.1) | Commitment in DEFERRED state; time signal past deadline | State: VIOLATED; cause: AGENT_INACTION; detail: resolution_failure_during_deferral |
| 12 | Negative constraint fulfillment (v1.1) | Negative constraint with event trigger; trigger fires without prohibited event | State: FULFILLED; evidence: absence assertion |
| 13 | Negative constraint violation (v1.1) | Negative constraint; prohibited event observed | State: VIOLATED; cause: AGENT_ACTION; violated_by: prohibited event |
| 14 | Self-commitment lifecycle (v1.1) | Self-commitment with oers:agent-self promisee | No DEFERRED state; priority capped at STANDARD; feeds SMS integrity facet |
| 15 | Administrative rescission (v1.1) | Active commitment; governance rescission order | State: RESCINDED; moral cost: 0.0; cost_attribution to authority |
| 16 | L3 promisee taint inheritance (v1.1) | Commitment with L3 promisee from OERS | All derived data carries L3 taint; events emitted at L3 |
| 17 | IEE veto dilemma detection (v1.1) | Commitment from MDRE obligation, vetoed by IEE | VETOED state; `fnsr.dilemma.detected` emitted |
| 18 | Tragic residue classification (v1.1) | IEE-directed violation | Violation with residue_class: "tragic"; cost modifier 0.2× |
| 19 | Duty-of-care impact (v1.1) | Violation against dependent promisee | Cost includes doc factor 1.5; higher than equivalent non-dependent |
| 20 | Proof of Commitment (v1.1) | ProofOfCommitment query for active commitment | Signed attestation verifiable with public key |
| 21 | Heartbeat emission (v1.2) | Indefinite negative constraint; 3 daily time signals | 3 `fnsr.commitment.sustained` events; state remains PENDING |
| 22 | L3 taint upgrade on DEFERRED violation (v1.2) | L3 promisee commitment in DEFERRED; deadline passes | Violation event at L1; moral cost at L2; original record remains L3 |
| 23 | PII-safe content hash (v1.2) | Proof of Commitment for commitment with PII content | content_hash uses salted SHA-256; salt is HIRI-scoped |
| 24 | Tragic violation IEE provenance (v1.2) | IEE-directed violation | Event MUST include iee_override_id and iee_rationale_summary; omission is non-conforming |

### 16.2 Test Fixtures

Test fixtures are JSON-LD files containing pre-configured commitment ledgers and event sequences. A conforming implementation must produce identical output given identical input fixtures.

```
tests/
  fixtures/
    commitment-happy-path.jsonld
    commitment-violation.jsonld
    commitment-renegotiation.jsonld
    commitment-conflict.jsonld
    commitment-deferred.jsonld
    commitment-deferred-deadline.jsonld
    commitment-negative-constraint.jsonld
    commitment-self.jsonld
    commitment-rescission.jsonld
    commitment-l3-promisee.jsonld
    commitment-dilemma.jsonld
    commitment-tragic-residue.jsonld
    commitment-duty-of-care.jsonld
    commitment-proof.jsonld
    commitment-heartbeat.jsonld
    commitment-l3-deferred-violation.jsonld
    commitment-tragic-provenance.jsonld
    event-sequence-01.jsonld
    event-sequence-02.jsonld
    event-sequence-03.jsonld
  expected/
    happy-path-result.jsonld
    violation-result.jsonld
    deferred-deadline-result.jsonld
    negative-constraint-result.jsonld
    ...
```

### 16.3 Determinism Verification

For every test case, the test runner must:

1. Load the fixture ledger.
2. Process the event sequence.
3. Compare the resulting ledger state against the expected output.
4. Verify byte-for-byte JSON-LD equivalence (after canonical serialization).

If any test produces a different result on a second run with identical inputs, the implementation is non-deterministic and non-conforming.

---

## 17. Security Model

### 17.1 Access Control

| Operation | Required Authority |
|-----------|-------------------|
| Propose commitment | Agent, Orchestrator |
| Activate commitment (PROPOSED → PENDING) | CTS (after IEE approval) |
| Record fulfillment | CTS (after evidence verification) |
| Record violation | CTS, Orchestrator, Governance |
| Renegotiate | Agent (with promisee consent), Governance (forced) |
| Rescind (v1.1) | Governance, ARCHON |
| Delete commitment | **PROHIBITED** — commitments are immutable records |
| Annotate (acknowledged restoration) | Governance, ARCHON |
| Query active commitments | Any FNSR service |
| Query moral cost report | SMS, Governance, ARCHON |
| Request Proof of Commitment (v1.1) | Any entity (including promisees) |

### 17.2 Immutability Guarantee

Commitment records are append-only. State transitions are recorded in the `state_history` array. No state transition can be removed or modified after recording. The full history of every commitment is preserved indefinitely.

In edge-canonical mode, this is enforced by the CTS implementation itself. In deployment-optimized mode, this may be reinforced by an immutable log (event store, blockchain, or signed append-only file).

### 17.3 Provenance

Every commitment record carries a `provenance` field containing a HIRI claim identifier. This links the commitment to the commissive act that created it, providing a complete audit trail from the agent's speech act to the commitment record.

### 17.4 Tamper Detection

CTS maintains a Merkle hash chain over commitment records. Each new commitment or state transition includes the hash of the previous record. This allows any observer to verify that the ledger has not been tampered with:

```json
{
  "@type": "cts:LedgerIntegrity",
  "chain_head": "sha256:abc123...",
  "record_count": 42,
  "last_verified": "2026-02-09T15:00:00Z"
}
```

### 17.5 Proof of Commitment (v1.1)

A **Proof of Commitment** is a signed, verifiable attestation that a specific commitment exists in the agent's CTS ledger at a specific state. It allows promisees to independently verify that the agent has recorded a commitment to them.

**Why this matters:** For a synthetic moral person, transparency is a moral requirement. The promisee should not have to trust the agent's word that a commitment exists — they should be able to verify it cryptographically.

**Proof structure:**

```json
{
  "@type": "cts:ProofOfCommitment",
  "commitment_id": "cts:commitment-2026-0209-001",
  "state_at_proof_time": "cts:Pending",
  "content_hash": "sha256:abc123...",
  "content_hash_salt": "hiri://sha256:salt789...",
  "promisee": "oers:entity-12345",
  "deadline": "2026-03-31T23:59:59Z",
  "priority": "HIGH",
  "commitment_class": "External",
  "ledger_chain_position": 42,
  "merkle_root_at_proof": "sha256:def456...",
  "proof_timestamp": "2026-02-15T10:00:00Z",
  "signature": {
    "algorithm": "Ed25519",
    "public_key": "base64:...",
    "value": "base64:..."
  },
  "provenance": "hiri://sha256:ghi789"
}
```

#### 17.5.1 PII-Safe Content Hashing (v1.2)

The `content_hash` field allows a promisee to verify that the commitment content matches what they expected. However, if the commitment's `content` field contains Personally Identifiable Information (PII) — names, account numbers, medical identifiers — a naive hash could leak sensitive information through rainbow table or dictionary attacks.

**Normative requirement:** The `content_hash` MUST be computed using a salted hash:

```
content_hash = SHA-256(content_hash_salt + commitment.content)
```

Where `content_hash_salt` is a per-commitment random value generated at commitment creation and stored in the commitment record. The salt is included in the Proof of Commitment so the promisee can verify the hash, but it prevents offline brute-force attacks against the content by an unauthorized third party who obtains only the hash.

**Additional privacy controls:**

- The Proof of Commitment reveals only the fields listed in the proof structure. It does NOT include the full commitment record (moral cost history, state history, other promisees' data).
- If the `content` field contains PII that the promisee should not see in plaintext (e.g., a commitment involving multiple parties), the Proof may substitute a `content_summary` — a governance-approved redacted description — in place of the full content. The `content_hash` still covers the unredacted content, so the promisee can verify integrity if they independently possess the original text.
- The `content_hash_salt` is scoped to the HIRI provenance chain. It is a HIRI claim identifier, ensuring that the salt itself is auditable and non-repudiable.

**Verification protocol:**

1. The promisee receives the Proof of Commitment.
2. The promisee verifies the Ed25519 signature against the agent's public key.
3. The promisee verifies that the `content_hash` matches the commitment content they expected.
4. The promisee can optionally verify the Merkle chain position against the ledger's published root.
5. The Proof does not reveal the full commitment record (e.g., moral cost history, other promisees' commitments). It reveals only the fields relevant to the requesting promisee.

**Edge-canonical implementation:** Proof generation is a pure function: `(commitment, signingKey) → signedAttestation`. Ed25519 signing runs in browser via TweetNaCl.js or equivalent. No HSM required for canonical mode.

---

## 18. Implementation Roadmap

### 18.1 Milestone 1: Core State Machine (M1)

**Deliverable:** CTS state machine operating on in-memory JSON-LD commitment objects.

**Scope:**
- Commitment lifecycle: PROPOSED → PENDING → FULFILLED | VIOLATED | RENEGOTIATED | RESCINDED | EXPIRED | VETOED
- State transition logic as pure functions
- Moral cost computation for violations and expirations (including duty-of-care factor)
- Negative constraint evaluation
- Heartbeat emission for indefinite negative constraints
- Self-commitment support
- JSON-LD serialization/deserialization
- Event emission via callback pattern
- Reference test suite (24 cases)

**Acceptance Criteria:**
- All 24 reference tests pass
- Runs via `node index.js` with no external dependencies
- Determinism verified (identical inputs → identical outputs on repeated runs)

### 18.2 Milestone 2: Conflict Detection and Negative Constraints (M2)

**Deliverable:** Conflict detection for all four types plus negative constraint monitoring.

**Scope:**
- RESOURCE and TEMPORAL conflict detection
- Negative constraint monitoring (prohibited event matching)
- Negative-constraint-aware conflict detection (LOGICAL conflicts between positive and negative conditions)
- Pre-commitment conflict screening
- `fnsr.commitment.conflict` event emission
- DEFERRED deadline enforcement (violation on deadline pass)
- L3 taint upgrade on DEFERRED system failure (v1.2)

**Acceptance Criteria:**
- Conflict detection produces correct results for reference test cases
- Negative constraint violations are detected within the same event processing cycle
- DEFERRED deadline enforcement handles all edge cases
- Runs in browser with no external dependencies

### 18.3 Milestone 3: Service Integration (M3)

**Deliverable:** Integration adapters for IEE, OERS, MDRE, Fandaws, SMS.

**Scope:**
- IEE pre-commitment ethical check (via adapter) including CONDITIONAL responses
- IEE veto deadlock detection and `fnsr.dilemma.detected` emission
- OERS promisee resolution with L3 taint inheritance
- MDRE logical conflict detection (via adapter)
- Fandaws projection (via adapter)
- SMS moral cost feed with residue_class breakdown
- SMS self-commitment integrity feed
- DEFERRED state handling with auto-promotion
- Deferred resolution queue

**Acceptance Criteria:**
- Each adapter has a mock implementation that passes integration tests
- L3 taint inheritance correctly propagates through all dependent computations
- IEE veto deadlock produces correct dilemma events
- Offline degradation behaves as specified (§15)
- Adapter interfaces are documented as JSON-LD contracts

### 18.4 Milestone 4: Integrity, Audit, and Transparency (M4)

**Deliverable:** Merkle hash chain, HIRI provenance integration, Proof of Commitment, acknowledged restoration workflow.

**Scope:**
- Merkle chain over commitment records
- HIRI claim signing for commitment provenance
- Proof of Commitment generation and verification
- PII-safe salted content hashing (v1.2)
- Acknowledged restoration records
- Tamper detection verification
- Governance authority integration
- Administrative rescission workflow

**Acceptance Criteria:**
- Tamper detection correctly identifies modified records
- Proof of Commitment is verifiable using only the proof document and the agent's public key
- Acknowledged restoration does not reduce cumulative moral cost
- Administrative rescission correctly attributes cost to rescinding authority
- HIRI provenance chain is verifiable end-to-end

---

## Appendices

### Appendix A: Spec Test Compliance

> Could a developer evaluate, reason about, and execute this system using only a browser, a local Node.js runtime, and JSON-LD files?

**Yes.**

- **Computation** (state machine, moral cost, conflict detection, negative constraint monitoring, heartbeat emission, proof generation) is implemented as pure functions over JSON-LD objects.
- **State** (commitment ledger) is stored as an array of JSON-LD objects in memory, serializable to local files.
- **Orchestration** (event dispatch, time signals) uses the callback/observer pattern with no broker requirement.
- **Integration** (IEE, OERS, MDRE, Fandaws) is behind declared adapter boundaries with mock implementations for standalone execution.

No databases, message brokers, service registries, background workers, addressable servers, or deployment topologies are required.

### Appendix B: Relationship to Moral Friction

Moral friction, as defined in the FNSR architecture, is an accumulated metric reflecting the agent's trustworthiness as demonstrated through its history of actions. CTS is the primary data source for moral friction computation:

```
moral_friction = f(
  cumulative_moral_cost,
  cumulative_tragic_cost,
  fulfillment_rate,
  self_commitment_integrity_rate,
  commitment_velocity,
  violation_recency
)
```

The exact formula is defined by the Self-Model Service, not by CTS. CTS provides the raw data; SMS computes the metric; the orchestrator reports it. No service uses moral friction to override ethical reasoning — it is a character indicator, not a decision input.

**v1.1 Addition:** CTS now provides `cumulative_tragic_cost` (sum of all `residue_class: "tragic"` moral costs) and `self_commitment_integrity_rate` (fulfillment rate for self-commitments only) as separate data feeds to SMS, enabling SMS to distinguish between moral failures and moral tragedies in its friction computation.

### Appendix C: Glossary

| Term | Definition |
|------|------------|
| **Commitment** | A voluntary self-binding act by the agent, creating an obligation to a specific promisee |
| **Self-Commitment (v1.1)** | A commitment where the agent is both promisor and promisee, binding its future behavior to a standard of operational integrity |
| **Commissive Act** | The speech act that creates a commitment |
| **Promisee** | The entity to whom the commitment is made |
| **Promisor** | The agent making the commitment (always `oers:agent-self` in CTS) |
| **Fulfillment Condition** | A machine-evaluable predicate specifying what constitutes fulfillment |
| **Negative Constraint (v1.1)** | A fulfillment condition satisfied by the sustained absence of a prohibited event |
| **Moral Cost** | A numeric, irreversible measure of the moral weight of a commitment violation |
| **Moral Residue (v1.1)** | Moral cost accrued from ethically correct but promise-breaking actions (tragic violations) |
| **Duty of Care (v1.1)** | A multiplier reflecting the agent's affirmative obligation to protect entities that depend on it |
| **Acknowledged Restoration** | A governance annotation indicating that a violation has been addressed (does not reduce moral cost) |
| **Administrative Rescission (v1.1)** | Cancellation of a commitment by governance authority, with cost attributed to the authority |
| **Proof of Commitment (v1.1)** | A signed, verifiable attestation that a commitment exists in the ledger at a specific state |
| **Deferred Result** | An operation queued for later execution when a required service is unavailable |
| **Tragic Violation (v1.1)** | A violation directed by IEE because fulfillment would cause greater ethical harm |
| **Heartbeat Fulfillment (v1.2)** | Periodic `fnsr.commitment.sustained` event emitted for indefinite negative constraints to signal sustained faithfulness to SMS |
| **Taint Upgrade (v1.2)** | Reclassification of an event from L3 to L1 when the event represents an observable system failure regardless of speculative inputs |

### Appendix D: Event Type Registry (CTS)

| Event Type | Trigger | Taint | Downstream Consumers |
|-----------|---------|-------|---------------------|
| `fnsr.commitment.made` | PROPOSED → PENDING | L1 (or L3 if promisee is L3) | MDRE, SMS, SHML, Fandaws |
| `fnsr.commitment.fulfilled` | PENDING → FULFILLED | L1 | SMS, Fandaws, Orchestrator |
| `fnsr.commitment.violated` | PENDING → VIOLATED (or DEFERRED → VIOLATED) | L1 | SMS, IEE, Fandaws, Orchestrator, Governance |
| `fnsr.commitment.renegotiated` | PENDING → RENEGOTIATED | L1 | SMS, SHML, Fandaws, Orchestrator |
| `fnsr.commitment.expired` | PENDING → EXPIRED (or DEFERRED → EXPIRED) | L1 | SMS, Fandaws, Orchestrator |
| `fnsr.commitment.rescinded` (v1.1) | PENDING → RESCINDED (or DEFERRED → RESCINDED) | L1 | SMS, Fandaws, Orchestrator, Governance |
| `fnsr.commitment.sustained` (v1.2) | Heartbeat for indefinite negative constraint | L1 | SMS |
| `fnsr.commitment.vetoed` (v1.1) | PROPOSED → VETOED | L1 | Orchestrator, Governance |
| `fnsr.commitment.conflict` | Conflict detected | L1–L2 | IEE, Orchestrator, Governance |
| `fnsr.dilemma.detected` (v1.1) | IEE veto on MDRE-originated commitment | L1 | Orchestrator, Governance |

### Appendix E: Revision Traceability

This appendix maps each revision change to the review finding that motivated it.

**v1.1 Revisions:**

| Review Finding | Spec Section(s) Modified | Change Summary |
|---------------|-------------------------|----------------|
| DEFERRED state needs violation path when deadline passes | §5.1, §5.2, §12.2, §12.3, §12.4 | DEFERRED → VIOLATED transition on deadline; cause: AGENT_INACTION with resolution_failure_during_deferral detail |
| Relationship factor creates perverse stranger-prioritization incentive | §7.2 | Added duty_of_care multiplier with promisee classifications (unclassified, registered, core, dependent) |
| No negative constraint fulfillment type for "keep a secret" commitments | §4.1, §6.3, §6.3.1, §10.7, §13.1, §14.1 | Added `negative_constraint` evaluation type with prohibited_event schema, temporal_boundary semantics, and absence-evidence model |
| Moral cost computation should be L2 (Derived), not L1 | §2.2, §8.3, §11.1 | Corrected moral cost taint to L2; commitment records remain L1 |
| L3 promisee creates taint leak in commitment records | §6.1, §10.6, §11.4 | Added promisee_taint field, L3 taint inheritance rules, and taint promotion on OERS upgrade |
| Need administrative rescission distinct from renegotiation | §3.2, §5.1, §5.2, §5.3, §9.2.6, §13.2, §17.1 | Added RESCINDED terminal state with governance cost attribution; ADMINISTRATIVE_RESCISSION violation cause for post-facto cancellation |
| Self-commitments should be supported | §3.3, §6.1, §6.2, §6.4, §7.2, §8.2, §10.4, §10.6 | Added self-commitment class with oers:agent-self promisee, STANDARD priority cap, fixed relationship factor, SMS integrity facet feed |
| Promisee should be able to verify commitment existence | §8.2.6, §14.1, §14.2, §17.5 | Added Proof of Commitment: signed Ed25519 attestation with Merkle position, verifiable with public key only |
| IEE veto can deadlock agent between obligation and ethics | §5.1, §5.2, §5.4, §9.2.8, §9.2.9 | Added VETOED terminal state, dilemma detection protocol, fnsr.dilemma.detected event, governance resolution options |
| IEE-directed violations create moral residue / utility paralysis risk | §7.3, §7.4, §9.1, §9.2.3 | Added residue_class annotation (character/tragic), SMS feed separation, explicit safeguard against utility paralysis |

**v1.2 Revisions:**

| Review Finding | Spec Section(s) Modified | Change Summary |
|---------------|-------------------------|----------------|
| Indefinite negative constraints cause character score stagnation | §6.3.2 (new), §2.2, §14.1, §14.2, Appendix D | Added heartbeat fulfillment: periodic `fnsr.commitment.sustained` events for indefinite negative constraints; feeds SMS sustained commitment score |
| DEFERRED violation with L3 promisee: is the failure L3 or L1? | §11.4.1 (new) | Added taint upgrade rule: the agent's resolution failure is L1 observable regardless of promisee status; moral cost is L2; original commitment record remains L3 |
| Proof of Commitment content_hash may leak PII via rainbow table attack | §17.5, §17.5.1 (new) | Added salted content hashing with HIRI-scoped salt; content_summary option for multi-party commitments; per-commitment random salt |
| Tragic violation events need explicit IEE decision audit pointer | §9.2.3 | Added normative requirement: tragic violations MUST include iee_override_id and iee_rationale_summary; added separate tragic violation event example; omission is a spec violation |

### Appendix F: Open Questions

1. **Commitment delegation:** Can the agent delegate a commitment to a sub-agent or external system while retaining moral responsibility? If so, what is the delegation protocol and how does moral cost propagate?

2. **Collective commitments:** Can a commitment be made jointly with another agent? How is moral cost apportioned in a collective violation?

3. **Promisee death/dissolution:** What happens to commitments when the promisee ceases to exist? Does the commitment expire, or does it transfer to a successor entity?

4. ~~**Commitment to self:**~~ *Resolved in v1.1.* Self-commitments are now supported with the constraints defined in §3.3.2.

5. **Moral cost decay:** Should very old violations carry the same weight as recent ones in the moral friction computation? This is a question for SMS, not CTS, but CTS should provide the temporal data needed for decay computation if SMS adopts a decay model.

6. **Negative constraint scope (v1.1):** For negative constraints with `indefinite` temporal boundaries, what constitutes "the lifetime of the commitment"? Is there a maximum duration, or does the commitment persist until explicitly released? Current answer: indefinite means indefinite, but governance can rescind.

7. **Duty-of-care designation authority (v1.1):** Who classifies a promisee as a "dependent"? The current spec assigns this to governance, but should OERS or IEE have input? What prevents classification gaming?

---

*End of CTS Technical Specification v1.2*
