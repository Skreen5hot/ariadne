# Multi-Agent Retrospective Execution Protocol (MAREP)

**Version:** 2.2 (Draft — normalized to Barcode substrate v2.8.0)
**Status:** Specification — Normative
**Audience:** Orchestrator agents, agent implementers, retrospective system integrators
**Purpose:** Execute structured, low-drift, multi-agent retrospectives through shared-state coordination rather than conversational interaction.

---

## 0. Conformance Language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** in this document are to be interpreted as described in RFC 2119 and RFC 8174 when, and only when, they appear in all capitals.

A conforming implementation MUST satisfy every MUST and MUST NOT requirement in this specification. SHOULD requirements MAY be deviated from when documented justification is provided in the implementation's conformance statement.

---

## 1. Core Principle

The retrospective system is a **deterministic state machine** operated by structurally constrained agents over a shared canonical state. It is not a simulated meeting.

Three invariants govern the system:

1. **Canonicality** — A single, versioned state object is the sole authoritative artifact; all reasoning derives from and reduces to modifications of this state.
2. **Non-conversationality** — Agents MUST NOT communicate with one another directly. All inter-agent influence is mediated through state.
3. **Sequential mutation** — At any moment, at most one agent holds write authority over canonical state.

The objective is not to create the illusion of teamwork. The objective is structured collaborative cognition through controlled state transitions, yielding reliable synthesis and reduced drift.

---

## 2. Architectural Goals

The system is designed to:

* minimize hallucinated collaboration,
* reduce token waste,
* prevent recursive agreement loops,
* preserve machine-readable state,
* maintain deterministic retrospective evolution,
* support asynchronous or sequential execution,
* and enable downstream automation and analytics.

These goals are listed in priority order; in any tradeoff, earlier goals dominate.

---

## 3. Glossary

* **Canonical state** — The single authoritative state object (`RETRO_STATE.jsonld`) representing the retrospective at a point in time. Versioned, schema-validated, monotonically advanced. Chain-hashed via the substrate's audit-trail mechanism.
* **Agent** — A bounded analytical persona with defined role, scope, and update authority. All agents are dispatched via the substrate's existing agent-contract surface (Read-Grep-Glob tools; JSON envelope outputs; `required_outputs` frontmatter; no Edit/Write tools).
* **Orchestrator** — An **LLM worker agent** with elevated responsibility for retro-level workflow control, conflict detection, summarization, and consensus tracking. The Orchestrator is NOT the substrate-level orchestrator (that is the deterministic Barcode daemon); the Orchestrator is dispatched by the daemon like any other worker agent and operates under the same CPS / audit-chain constraints.
* **Turn** — A bounded interval during which one agent has been dispatched to mutate canonical state. Under the Barcode substrate, a turn corresponds to a single dispatched task; the agent's mutation lands as that task's outputs.
* **Update** — A localized, schema-conformant mutation of canonical state, expressed as a JSON envelope per the substrate's agent-output contract.
* **Phase** — A named stage of the retrospective workflow with defined entry and exit criteria. Specified per retro under `surfaces/retro/phases/<phase>.md`.
* **Scratchpad** — Private, non-canonical, agent-local working memory. Lives outside the audit chain.
* **Issue** — A retrospective finding tracked through defined status transitions (§15.3).
* **Action** — A proposed remediation or follow-up with ownership and outcome criteria.
* **Permitted sections** — The paths within canonical state an agent's role authorizes for mutation. Declared statically per-role in `AGENTS.md` (§6); validated deterministically by the substrate at dispatch (§10).

---

## 4. Agent Model

Each agent represents a distinct analytical perspective. Agents MUST be selected for epistemic diversity, non-overlapping reasoning styles, and unique evaluative function. Redundant personas (two agents covering the same focus area under different names) MUST NOT be instantiated within a single retrospective.

### 4.1 Required Agent — `@Orchestrator` (LLM worker)

The Orchestrator is the only agent permitted to advance phases, request compression, surface episodic-memory summaries, resolve schema violations, and adjudicate contradictions. Responsibilities: workflow control, state-state-transition request, summarization, conflict detection, consensus tracking.

The Orchestrator is an LLM worker agent. It is **dispatched** by the deterministic substrate (the Barcode daemon) like any other worker agent; it operates under the substrate's CPS check, audit-chain invariant, and `required_outputs` contract. The Orchestrator has elevated responsibility within the retro surface but **no substrate-level privileges**: it cannot bypass CPS, cannot write directly to `state.jsonld`, cannot extend its own dispatch authority. Authority decisions (lock granting, scope enforcement) belong to the deterministic substrate (§6, §10).

The Orchestrator role is the **first instance of the Bounded-Authority Orchestrator (BAO) pattern** — auditable through the same machinery as every other agent.

### 4.1.1 BAO Bounds

When the BAO pattern is invoked in documentation, the four bounding properties MUST be consistently listed. Readings of "bounded-authority" that omit any of these four risk under-specifying the pattern; readers may interpret "bounded" more narrowly than intended.

1. **Surface scope.** The BAO agent's elevated authority extends only within its assigned surface (retro for MAREP-Orchestrator; synthesis for the generalized synthesist; deliberation for FNSR moral-person coordinators). Cross-surface action requires standard dispatch through the substrate.

2. **Substrate enforcement.** All BAO outputs pass through CPS check (`required_outputs`, structured-error veto, miss-class taxonomy, anti-pattern enforcement per §17). The BAO cannot bypass substrate validation, cannot extend its own scope, cannot mutate state outside its permitted_sections (§10.2).

3. **Audit-chain visibility.** Every BAO decision lands in the audit chain via the normal dispatch path. There are no hidden BAO state transitions; the chain-hashed `audit` array captures every Orchestrator action as a versioned mutation (§7.4, §9).

4. **No substrate-level privilege.** The BAO is a worker agent. It cannot bypass the daemon's dispatch ordering, cannot write directly to `state.jsonld`, cannot acquire locks outside the dispatch protocol, cannot extend its dispatch authority beyond what its frontmatter declares. Authority decisions (lock granting, scope enforcement, schema validation) belong to the deterministic substrate.

These four bounds together distinguish a BAO from naive "give the LLM control" patterns where the LLM's elevated responsibility comes with privilege escalation. The Orchestrator role is the first instance; future BAO instances (generalized synthesist in v3.0; phase-exit retro finalizer; eventual FNSR moral-person deliberative coordinators) MUST satisfy all four bounds.

### 4.2 Analytical Agents

| Agent | Focus | Barcode substrate analog |
|---|---|---|
| `@Architect` | System design, scalability, technical debt, integration concerns | `architect.md` (mode: review) |
| `@Developer` | Implementation friction, velocity, maintainability, tooling | `developer.md` |
| `@QA` | Defects, verification gaps, regression risks, process quality | NEW; retro-surface-specific agent |
| `@DeliveryManager` | Sprint predictability, throughput, blockers, coordination overhead | NEW; retro-surface-specific |
| `@RiskAnalyst` | Hidden failure modes, systemic fragility, operational exposure | NEW; retro-surface-specific |
| `@UserAdvocate` | User impact, usability, stakeholder outcomes | `ux-sme.md` |
| `@Skeptic` | Challenging assumptions, identifying weak reasoning, preventing false consensus | `adversarial-critic.md` (mode: review-second-pass) |

A retrospective MAY define additional roles consistent with §4 invariants. The complete agent roster MUST be declared in `AGENTS.md` before Phase 1 entry. All retro-surface-specific agents (currently `@QA`, `@DeliveryManager`, `@RiskAnalyst`) follow the **read-only-by-contract pattern** (tools: Read, Grep, Glob; no Edit/Write/Bash; outputs are observations + structured proposals, not mutations).

---

## 5. Required and Optional Files

### 5.1 Canonical Files (Required)

```text
/AGENTS.md                    — Constitutional protocol; agent definitions, rules, schemas
/RETRO_STATE.jsonld           — Authoritative state; versioned and schema-validated
/RETRO_BOARD.md               — Human-readable projection of canonical state
```

### 5.2 Working Files (Optional)

```text
/private/<agent>_notes.md     — Agent-local scratchpad; non-canonical
```

Scratchpads are temporary working memory. They MUST NOT be referenced by other agents and MUST NOT be treated as authoritative input to consensus.

### 5.3 Surface-Registry Location

Per Barcode substrate FNSR Spec 01, MAREP is the **retro-surface specification** and resides under:

```text
/surfaces/retro/
    surface-spec.md           — This spec, generalized layer
    agents/<role>.md          — Per-role declaration (permitted_sections, mode, etc.)
    phases/<phase>.md         — Per-phase specification (entry/exit/permitted_sections)
```

Adding a new retro-phase = drop a new `phases/<phase>.md` file. Adding a new analytical role = drop a new `agents/<role>.md` file. No substrate release required (same surface-registry primitive that verification uses in v2.8.0).

---

## 6. AGENTS.md Specification

`AGENTS.md` defines the agent roster, behavioral rules, execution constraints, schema requirements, retrospective phases, and orchestration policy for a given retrospective instance. It functions as the constitutional protocol for that retrospective.

`AGENTS.md` MUST be finalized before Phase 1 entry. Mid-retrospective amendments MUST be recorded as numbered amendments and validated by the substrate before taking effect.

### 6.1 Per-Role Declaration Schema

Each role's static declaration (operator-authored; not LLM-determined):

```yaml
agents:
  - role: "@Architect"
    agent_file: ".claude/agents/architect.md"
    mode: "review"                       # Multi-mode agents specify mode
    permitted_sections:                  # Static; per-role authorization scope
      - issues
      - decisions
      - actions[*]/architectural_review
    required_outputs_overrides: {}       # Per-role overrides of agent default required_outputs
  - role: "@QA"
    agent_file: "surfaces/retro/agents/qa.md"
    permitted_sections:
      - issues[*]/qa_evidence
      - actions
```

Operators author `permitted_sections` once per retro instance per role; they are static throughout the retro. Mid-retro changes require an amendment + Orchestrator validation + substrate audit-trail entry.

---

## 7. Canonical State Model

`RETRO_STATE.jsonld` is the sole authoritative state. All retrospective reasoning, history, and decisions reduce to its contents. Stored as JSON-LD for cross-reference compatibility with substrate state (state.jsonld can reference retro entities by @id; retro entities can reference substrate tasks).

Agents MAY modify structured sections, append evidence, update issue status, and propose actions within their permitted_sections. Agents MUST NOT chat, roleplay, greet other agents, or simulate meetings. Any natural-language content placed into canonical state MUST be confined to designated free-text fields (e.g., `description`, `evidence`, `rationale`) and MUST NOT contain conversational artifacts (§17).

### 7.1 Required Top-Level Schema

```json
{
  "@context": "https://barcode.substrate/retro/v1",
  "retro": {
    "@id": "urn:retro:<id>",
    "sprint": "<string>",
    "phase": "gathering | merge | analysis | consensus | actions | compression | complete",
    "version": 0,
    "schema_version": "<semver>"
  },
  "issues":    [],
  "actions":   [],
  "decisions": [],
  "votes":     [],
  "audit":     []
}
```

Conforming implementations MUST publish a JSON Schema for the full state document.

### 7.2 Issue Schema

```json
{
  "@id": "urn:retro:issue:<DOMAIN>-<NNN>",
  "title": "<string>",
  "severity": "low | medium | high | critical",
  "status": "proposed | contested | confirmed | rejected | archived",
  "evidence": ["<string>"],
  "confirmed_by": ["<agent>"],
  "contested_by": ["<agent>"],
  "related_actions": ["<action_@id>"]
}
```

### 7.3 Action Schema

```json
{
  "@id": "urn:retro:action:ACT-<NNN>",
  "description": "<string>",
  "owner": "<agent>",
  "status": "proposed | accepted | rejected | deferred",
  "outcome_criteria": "<string>",
  "due_by": "<ISO8601 date>"
}
```

### 7.4 Audit Schema (Chain-Hashed)

Each accepted mutation MUST append an audit entry chained via the substrate's `hiri_sign` mechanism:

```json
{
  "version": 0,
  "agent": "<role>",
  "task_id": "<urn:fnsr:task:...>",
  "timestamp": "<ISO8601>",
  "diff_summary": "<string>",
  "affected_sections": ["<path>"],
  "prev_hash": "<sha256>",
  "chain_hash": "<sha256>"
}
```

This is the same audit-chain structure as `state.jsonld` task history; retro state inherits the substrate's append-only invariant.

---

## 8. Markdown Rendering Layer

`RETRO_BOARD.md` is a human-readable projection of canonical state. It exists for readability, human review, and lightweight inspection. The JSON-LD state remains authoritative; in any divergence, JSON-LD wins. Implementations SHOULD regenerate `RETRO_BOARD.md` from `RETRO_STATE.jsonld` rather than edit it directly.

---

## 9. State Versioning

Canonical state version (`retro.version`) is a monotonically increasing integer. Every accepted mutation MUST increment the version by exactly 1. Agents MUST submit updates that reference the version they read; the substrate MUST reject updates whose referenced version is not the current version (compare-and-swap semantics).

CAS rejection produces a `version_mismatch` structured error; the agent's turn is reclaimed and re-dispatched after the substrate refreshes the agent's view of state.

The audit chain (§7.4) is append-only; chain-hash integrity is verified deterministically by the substrate via the existing `state_admin verify` mechanism extended to retro state files.

---

## 10. Locking and Permitted-Sections Enforcement

### 10.1 Per-Mutation Lock

The substrate's existing per-mutation lock (`state.jsonld.lock`; OS-level cross-platform) is reused for retro state. MAREP does NOT introduce a turn-lock layer above the per-mutation lock; each dispatched task is one mutation.

At most one agent MAY hold the write lock at any time. Concurrent writes MUST be rejected (CAS in §9 backstops this).

### 10.2 Three-Stage Permitted-Sections Safety

Authority decisions belong to the deterministic substrate, not the LLM Orchestrator. The pattern:

**Stage 1: Static per-role declaration (operator-authored, §6.1).** Each role's permitted_sections is fixed in `AGENTS.md` before Phase 1 entry. Operator-authored; LLM-immutable.

**Stage 2: Per-turn requested_sections (agent-declared).** When the Orchestrator dispatches an analytical agent for a turn, the agent's lock-acquisition request declares `requested_sections` — the specific paths it intends to modify in this turn:

```json
{
  "requested_sections": ["issues[*]/qa_evidence"]
}
```

**Stage 3: Deterministic substrate validation.** The substrate (Barcode daemon, Python) validates `requested_sections ⊆ role_permitted_sections` as a set-membership check. Lock granted only if subset holds. The LLM Orchestrator triggers sequencing but never makes the authority decision.

**Defense in depth:** the CPS pre-commit hook re-validates the actual mutation diff against the granted requested_sections. If an agent's output touches paths outside its declared scope, CPS vetoes with `error: out_of_scope_mutation`. Anti-pattern enforcement §17.4.

### 10.3 Permitted Operations

A turn-holding agent MAY:

* read the current state,
* analyze sections (read access is unrestricted; the read tools are Read/Grep/Glob),
* submit one or more deterministic updates within `requested_sections`,
* release the lock by returning outputs.

A turn-holding agent MUST NOT:

* modify sections outside `requested_sections`,
* revise archived conclusions (§13 archive is read-only after compression),
* modify another agent's scratchpad,
* self-extend turn duration.

---

## 11. Update Semantics

Every update MUST be deterministic, localized, idempotent, and schema-compliant. Updates are expressed as **JSON envelopes** per the substrate's existing agent-output contract — NOT as YAML-merge-style diffs.

### 11.1 Update Form

Agents emit:

```json
{
  "outputs": {
    "proposed_issues": [
      {
        "@id": "urn:retro:issue:DEPLOY-002",
        "title": "Deployment instability",
        "severity": "medium",
        "status": "proposed",
        "evidence": [
          "failed rollback in sprint-42",
          "inconsistent environment parity between staging and prod"
        ]
      }
    ],
    "summary": "Surfaced one deployment issue; severity medium.",
    "version_read": 7
  }
}
```

A **retro-applier system agent** (deterministic Python; new for MAREP-on-Barcode integration; analog to the v2.6.0 `applier` for code changes) consumes the analytical agent's `proposed_issues` / `proposed_actions` / `vote_casts` and merges them into `RETRO_STATE.jsonld`. The merger is the deterministic step that materializes the mutation; the agent's output is the proposal, not the mutation itself.

### 11.2 Properties

* **Deterministic** — Given the same input state and the same agent prompt, the update SHOULD produce structurally equivalent diffs across runs. Semantic equivalence under field-level normalization is sufficient (LLM nondeterminism is bounded but not eliminated).
* **Localized** — Updates MUST modify only sections within the lock's `requested_sections` (validated by §10.2 Stage 3 + CPS).
* **Idempotent** — Re-applying an accepted update MUST be a no-op. Each update includes a stable `update_id` (typically the dispatching task's `@id`) to enable safe retry.
* **Schema-compliant** — Updates MUST validate against the published schema. The substrate MUST reject any non-conforming update without partial application (CPS structural-error path).

### 11.3 Non-Conforming Example

```text
I think we had some deployment issues.
```

Plain prose is not a valid update. The substrate rejects with `error: not_a_structured_update`.

---

## 12. Phase Workflow

The retrospective progresses through six phases in strict order. Phase transitions are exclusively performed by the Orchestrator (via dispatched `phase_transition` task) and MUST be recorded in `audit`. Each phase has its own spec file under `surfaces/retro/phases/<phase>.md` declaring entry/exit criteria and per-role permitted_sections active during that phase.

### 12.1 Phase 1 — Independent Gathering

* **Entry:** `AGENTS.md` finalized; `RETRO_STATE.jsonld` initialized.
* **Activity:** Each agent independently analyzes the sprint, records findings in private scratchpad, and submits compressed findings as `proposed` issues.
* **Purpose:** Maximize diversity of reasoning; prevent premature convergence.
* **Exit:** Every agent has either submitted findings or explicitly declined (recorded in audit).

### 12.2 Phase 2 — Canonical Merge

* **Entry:** Phase 1 exit conditions satisfied.
* **Activity:** Orchestrator (LLM) merges findings, normalizes issue identifiers, removes duplicates, organizes themes. Merge is itself a dispatched task; its outputs are mutations to `issues[]`.
* **Exit:** No duplicate @ids; every proposed issue conforms to schema.

### 12.3 Phase 3 — Structured Analysis

* **Entry:** Phase 2 exit conditions satisfied.
* **Activity:** Agents take turns evaluating themes, challenging assumptions, validating evidence, refining root causes.
* **Exit:** Every issue has reached `confirmed`, `rejected`, or `contested` status with supporting evidence.

### 12.4 Phase 4 — Consensus Resolution

* **Entry:** Phase 3 exit conditions satisfied.
* **Activity:** Orchestrator identifies unresolved conflicts, triggers voting where required (§15), finalizes issue states.
* **Exit:** No issues remain in `contested` status.

### 12.5 Phase 5 — Action Assignment

* **Entry:** Phase 4 exit conditions satisfied.
* **Activity:** Agents propose actions with ownership, outcome criteria, due dates.
* **Exit:** Every `confirmed` issue has at least one accepted action OR an explicit `no_action_required` decision.

### 12.6 Phase 6 — Final Compression

* **Entry:** Phase 5 exit conditions satisfied.
* **Activity:** Orchestrator archives discussion history (logically relocates per §13), preserves canonical findings, generates final summary and action manifest (§19).
* **Exit:** All deliverables produced and validated; retro state promoted to episodic memory (§16).

---

## 13. Context Compression

Large retrospectives accumulate entropy. The Orchestrator MUST request compression when any of the following triggers fires:

* token usage exceeds the configured budget,
* duplicate issues are detected,
* canonical state contains semantically redundant entries,
* historical context begins biasing new analysis (detected by repeated re-derivation of archived conclusions).

### 13.1 Compression Is Logical Relocation, Not Destruction

Compression preserves canonical conclusions, relocates obsolete sections under `archive`, and generates compressed summaries. **The append-only audit-chain invariant MUST hold:** compression is logical relocation (the entry moves from `issues[]` to `archive.issues[]`), not destruction. The chain-hash remains continuous; a `compression` audit event records what relocated and when.

Compression MUST NOT alter the substantive content of `confirmed`, `rejected`, or `accepted` records — only their location within the JSON-LD document. Re-deriving the substrate's audit chain over the compressed state MUST yield the same chain-hash for the relocated entries as it would have for the un-compressed entries.

---

## 14. Contradiction Management

The Orchestrator MUST detect:

* conflicting root causes,
* incompatible action items,
* duplicate issue identifiers,
* unresolved disagreements between agents.

When a contradiction is detected, the Orchestrator MUST mark the affected items with `status: contested`, record the conflicting positions in `conflict_record`, and either request targeted re-analysis from a specific agent or trigger a consensus vote (§15).

```json
{
  "conflict_record": [
    {
      "issue_@id": "urn:retro:issue:PERF-001",
      "positions": [
        { "agent": "@Architect", "claim": "API latency caused by N+1 query pattern" },
        { "agent": "@QA",        "claim": "API latency caused by network egress saturation" }
      ],
      "resolution_required_by": "<phase | timestamp>"
    }
  ]
}
```

---

## 15. Consensus Protocol

Consensus is explicit. Implicit agreement is not consensus.

### 15.1 Decision Rules

```json
{
  "decision_rules": {
    "standard_threshold": 0.7,
    "architecture_changes": { "unanimous_required": true },
    "abstention_policy": "counts_against_quorum",
    "tie_break": "orchestrator"
  }
}
```

`tie_break` values: `orchestrator`, `skeptic`, `re_vote`.

### 15.2 Vote Record

```json
{
  "@id": "urn:retro:vote:<NNN>",
  "subject": "ISSUE:PERF-001:status:confirmed",
  "threshold": 0.7,
  "cast": [
    { "agent": "@Architect", "position": "confirm" },
    { "agent": "@QA",        "position": "confirm" },
    { "agent": "@Skeptic",   "position": "reject"  }
  ],
  "outcome": "confirmed",
  "closed_at": "<ISO8601>"
}
```

### 15.3 Issue Status Transition Graph

```text
proposed   → contested
proposed   → confirmed
proposed   → rejected
contested  → confirmed
contested  → rejected
confirmed  → archived
rejected   → archived
```

All other transitions MUST be rejected by the substrate's CPS check with `error: invalid_status_transition`.

---

## 16. Memory Boundaries

Agents MUST NOT recursively inherit unlimited prior retrospectives. Memory is partitioned into three layers with explicit promotion and access rules.

### 16.1 Working Memory

* **Storage:** the active retro's `RETRO_STATE.jsonld` plus the substrate's active `state.jsonld` task graph.
* **Access:** read+write by participating agents within their `requested_sections` (§10.2). Reads are unrestricted within working memory; writes are scope-bounded.
* **Lifecycle:** persists for the duration of the retro (Phase 1 through Phase 6). Promoted to episodic memory at retro close (§16.4).

### 16.2 Episodic Memory

* **Storage:** sealed past retros under `<fnsr-archive>/archive/retrospectives/<YYYY-MM-retro-id>/` (canonically the operator's FNSR archive; e.g., `ariadne/archive/retrospectives/`) plus the substrate's chain-hashed audit history (`state.jsonld` task histories, retained permanently per the append-only invariant).
* **Access:** read-only; surfaced to analytical agents **only on explicit Orchestrator request, and only as compressed summaries** (raw past retro state is NOT directly readable by analytical agents during a current retro turn). The Orchestrator may consult episodic memory directly to inform its own dispatching and conflict-detection decisions but MUST disclose the consultation in `audit`.
* **Lifecycle:** permanent. Append-only. Never destroyed.

### 16.3 Semantic Memory

* **Storage:** stable operational principles, standards, and team conventions. Canonical paths: `CLAUDE.md`, `PLAYBOOK.md`, `project/DECISIONS.md` (ADRs), `project/Routing/` (FNSR specs), `surfaces/<surface>/surface-spec.md` files.
* **Access:** read-only by all agents during retro execution. Updates MUST require ADR-or-equivalent operator-deliberated process and MUST NOT be performable from within a retro turn (Phase 1 through Phase 6 are read-only against semantic memory).
* **Lifecycle:** evolves via deliberate operator action between retros. Entries can be flagged as `superseded_by: <newer-entry>` but MUST NOT be destroyed (audit-trail-honesty invariant carries into semantic memory).

### 16.4 Promotion Rules

**Working → Episodic** (at retro close, Phase 6 exit):

1. The MAREP-Orchestrator generates `RETRO_SUMMARY.md` per §19.
2. Final `RETRO_STATE.jsonld` + `RETRO_SUMMARY.md` are written to `<fnsr-archive>/archive/retrospectives/<YYYY-MM-retro-id>/`.
3. A `retro_closed` audit event is appended to the substrate's `state.jsonld` referencing the archive path. Substrate task `urn:fnsr:retro:<id>` transitions to `status: done`.

**Episodic → Semantic** (deliberate, operator-driven, NOT automatic):

1. Operator reviews episodic entries at phase-exit retro deliberation.
2. High-signal observations are folded into PLAYBOOK / CLAUDE.md / ADRs via the normal authoring process (architect ratification + commit-finalize per FNSR Spec 03).
3. The promotion is itself recorded as a **forward-track event** (`subject.type: candidacy`, `sub_surface: internal-methodology-refinement`, `surfacing_task_id: <retro task @id>`) so the promotion path is auditable.

### 16.5 Demotion Rules

* **Semantic deprecation:** ADRs / PLAYBOOK entries that are superseded gain a `superseded_by: <reference>` field. Original remains readable; the supersession is itself recorded as an ADR.
* **No working → demotion within a retro.** Working memory at retro close compresses to episodic only; there is no in-retro rollback.
* **No episodic demotion.** Episodic memory does not compress further; the substrate's append-only invariant carries through.

### 16.6 Boundary Enforcement (Substrate-Mechanical)

* Schema validation (CPS) rejects retro-turn updates whose `requested_sections` include semantic-memory paths (`surfaces/`, `project/DECISIONS.md`, `project/SPEC.md`, `CLAUDE.md`, `PLAYBOOK.md`, etc.) with `error: semantic_memory_immutable_from_retro`.
* Episodic memory access by analytical agents is gated by the Orchestrator's dispatch — analytical agents lack file-read access to past retros' archive directories during their turn. The Orchestrator surfaces summaries via UPSTREAM in the dispatched task.
* Semantic memory is read-only via the standard Read tool during a retro; the substrate enforces write-boundary via §16.6's path rejection.

---

## 17. Anti-Pattern Enforcement

The Orchestrator MUST actively suppress the following anti-patterns. Each is paired with a substrate-mechanical detection mechanism so enforcement is structural rather than discretionary. Detections map to CPS checks; vetoes produce structured errors per the substrate's miss-class taxonomy.

### 17.1 Persona Theater

* **Forbidden:** conversational addresses, affirmations to other agents (e.g., `"Great point @QA!"`).
* **Detection:** CPS pre-commit text-scan. The substrate's `_check_no_persona_theater(outputs, designated_reference_fields)` rejects free-text fields containing `@<agent>` patterns outside designated reference fields (e.g., `votes.cast[*].agent`, `confirmed_by[]`, `contested_by[]`).
* **Veto error:** `persona_theater_detected`.

### 17.2 Recursive Agreement Loops

* **Forbidden:** repeated affirmations, redundant summaries, synthetic collaboration language.
* **Detection:** CPS semantic-similarity check against the prior turn's outputs in the same retro. `_check_no_redundant_affirmation(outputs, prior_turn_outputs, threshold)` rejects updates whose free-text body exceeds similarity threshold. v1 implementation: Levenshtein-distance-based; future implementations MAY substitute LLM-judge similarity for higher fidelity.
* **Veto error:** `redundant_affirmation`.

### 17.3 Freeform Brainstorm Drift

* **Forbidden:** unconstrained speculation, conversational sprawl, narrative discussion in canonical state.
* **Detection:** CPS length-budget check. Each agent's role declaration in `AGENTS.md` specifies per-field `max_length` budgets (e.g., `evidence: 500 chars`, `rationale: 1000 chars`). Updates exceeding budget OR containing flagged conversational connectives (e.g., "as we discussed", "circling back", "to your point") are rejected.
* **Veto error:** `freeform_brainstorm_drift`.

### 17.4 Out-of-Scope Mutation

* **Forbidden:** modifying sections outside the turn's `requested_sections`.
* **Detection:** §10.2 Stage 3 + CPS pre-commit diff scan. Already enforced by the permitted-sections deterministic validation.
* **Veto error:** `out_of_scope_mutation`.

---

## 18. Error Handling and Recovery

### 18.1 Schema Violation

When an update fails schema validation, the substrate's CPS check rejects without partial application, logs the violation with `evidence.miss_class: unresolved_predicate` (per the substrate's four-class miss taxonomy), and either:

* requests a corrected update from the holding agent (operator may reset the task via `state_admin reset`), OR
* revokes the lock and re-dispatches to a different agent.

### 18.2 Lock Expiration / Stalled Turn

The substrate's existing in-progress reconciliation handles this: any task left in `in_progress` at daemon restart is revived to `ready` with a `recovered_from_in_progress` audit entry (`attempts` preserved). No timeout-based reclaim in v2.2; if a turn-timeout pattern is needed, it can be added as a future MAREP refinement.

### 18.3 Orchestrator Failure

If the MAREP-Orchestrator agent fails (CPS veto on its outputs; LLM dispatch error; structural error), the substrate's normal failure-recovery applies: `attempts++`; retry up to `MAX_ATTEMPTS`; hard-fail to `status: failed` thereafter. The operator may dispatch a replacement Orchestrator task via `state_admin reset` + re-queue.

The retro state itself is not corrupted by an Orchestrator failure — `RETRO_STATE.jsonld` remains at the last valid version; no partial writes per the substrate's atomic-write invariant.

### 18.4 State Corruption

If `RETRO_STATE.jsonld` fails schema validation or chain-hash verification outside an in-flight update, the substrate emits a corruption event and refuses further retro mutations until the operator reconciles. Use `state_admin verify` (extended to retro state files) to detect; manual repair via `state_admin reset` or substrate reload from last valid version.

---

## 19. Final Deliverables

At retrospective completion (Phase 6 exit), the system MUST produce:

```text
/RETRO_BOARD.md                — Final human-readable rendering
/RETRO_STATE.jsonld            — Final canonical state
/RETRO_SUMMARY.md              — Executive summary derived from canonical state
/ACTION_ITEMS.jsonld           — Extracted action manifest
```

Each deliverable MUST validate against its respective schema. `RETRO_SUMMARY.md` MUST be derivable from `RETRO_STATE.jsonld`; the summary is a projection, not an independent artifact. Files are written to `<fnsr-archive>/archive/retrospectives/<YYYY-MM-retro-id>/` per §16.4 promotion rules.

---

## 20. Substrate Integration (NEW in v2.2)

MAREP-on-Barcode integration requires the following net-new substrate primitives:

1. **Retro-applier system agent** (new system agent in `SYSTEM_AGENTS`): consumes analytical-agent `proposed_issues` / `proposed_actions` / `vote_casts` and merges them into `RETRO_STATE.jsonld` per §11.
2. **Three new analytical agents** (`@QA`, `@DeliveryManager`, `@RiskAnalyst`): read-only-by-contract worker agents under `surfaces/retro/agents/`.
3. **`vote_record` audit event type**: new event_type alongside existing `banking`, `forward_track`, `phase_boundary_declared`, etc.
4. **Three new CPS checks** (per §17): `_check_no_persona_theater`, `_check_no_redundant_affirmation`, `_check_no_freeform_brainstorm`.
5. **Length-budget frontmatter syntax**: per-field `max_length` declarations in agent .md frontmatter (additive; non-MAREP agents ignore).
6. **`state_admin retro` subcommand family**: `init`, `phase-transition`, `vote`, `archive`, `verify` — operator surface for retro lifecycle. Mirrors existing `forward-track` subcommand family.

These primitives are scoped to a v3.0 minor release alongside the generalized-synthesist work (per the substrate build order); MAREP retros run on substrate v3.0+.

For v2.8.0-compatible retros (light adoption per the substrate integration spec), MAREP MAY operate without the new primitives by using existing substrate agents (architect / developer / ux-sme / adversarial-critic) and bypassing voting/compression in favor of `awaiting_operator_decision` resolution. Full MAREP conformance requires v3.0+.

---

## 21. Guiding Philosophy

This system is not simulated human conversation. It is structured collaborative cognition through controlled state transitions. The objective is reliable synthesis, disciplined analysis, reduced drift, and high-quality operational insight — not the appearance of teamwork.

The pattern that crystallized in Barcode substrate v2.8.0 — deterministic where possible, LLM where necessary, adversarial-critic where verdict changes state, audit-chain for all of it — applies to MAREP retros as well. The Orchestrator is LLM-because-necessary; the permitted-sections enforcement is deterministic-where-possible; the consensus protocol's tie-break-by-Skeptic is adversarial-critic-where-state-changes; the chain-hashed audit log is audit-chain-for-all-of-it.

---

## Changelog

* **v2.2 (Draft, 2026-05-18)** — Normalized to Barcode substrate v2.8.0:
  * Orchestrator clarified as LLM worker agent (§4.1); substrate orchestration distinguished from retro orchestration.
  * Canonical state file renamed `.yaml` → `.jsonld`; agent outputs normalized to JSON-envelope `{"outputs": {...}}` form (§7, §11).
  * Per-turn lock replaced with per-mutation lock; turn-tracking absorbed into substrate dispatch (§10).
  * Three-stage permitted-sections safety pattern: static AGENTS.md declaration + per-turn requested_sections + deterministic substrate validation. LLM never makes authority decisions (§10.2, §6.1).
  * Memory rules fully specified: storage, access, lifecycle, promotion, demotion, boundary enforcement (§16).
  * Anti-pattern detection mechanisms mapped to substrate CPS surface (§17).
  * Compression specified as logical relocation preserving append-only invariant (§13.1).
  * Roster mapped to existing Barcode agents + identified three new retro-surface-specific agents needed (§4.2).
  * Spec relocated under `surfaces/retro/` per FNSR Spec 01 surface-registry primitive (§5.3).
  * New §20 documenting required substrate primitives for full MAREP conformance.
* **v2.1 (Draft)** — Added conformance language (§0), glossary (§3), state versioning with CAS (§9), formal lock lifecycle (§10), update semantics with idempotence (§11), formal phase entry/exit criteria (§12), structured contradiction records (§14), explicit status transition graph (§15.3), error handling and recovery (§18), detection mechanisms paired with each anti-pattern (§17). Reorganized heading hierarchy.
* **v2.0** — Initial blackboard architecture; agent model; phase workflow; anti-pattern catalog.
