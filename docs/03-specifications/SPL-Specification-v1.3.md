# Structured Plan Language (SPL) Specification
## Version 1.3 — FINAL
### FNSR Ecosystem | Ontology of Freedom Initiative

---

**Status:** FINAL  
**Version:** 1.3  
**Supersedes:** SPL v1.2  
**Depends On:** SPCN v2.3.1, IEA v2.1, CTS v2.1, HIRI v1.4.1, MDRE (current)  
**Referenced By:** SPCN v2.3.1 §6.2.1, §8, §12.7; HumanBridge §12.7  

---

## Table of Contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Architectural Position](#2-architectural-position)
3. [Design Principles](#3-design-principles)
4. [Formal Grammar](#4-formal-grammar)
5. [Type System](#5-type-system)
6. [Semantic Rules](#6-semantic-rules)
7. [IEA Normative Bridge](#7-iea-normative-bridge)
8. [CTS Bridge](#8-cts-bridge)
9. [MDRE Bridge](#9-mdre-bridge)
10. [Canonicalization](#10-canonicalization)
11. [Parser Requirements](#11-parser-requirements)
12. [Semantic Retry Protocol](#12-semantic-retry-protocol)
13. [Constrained Decoding Schema](#13-constrained-decoding-schema)
14. [Size and Depth Limits](#14-size-and-depth-limits)
15. [Security Properties](#15-security-properties)
16. [HumanBridge Rendering Contract](#16-humanbridge-rendering-contract)
17. [Test Suite Requirements](#17-test-suite-requirements)
18. [Open Questions](#18-open-questions)
19. [Version History](#19-version-history)

---

## Changelog: v1.0 → v1.1

The following changes were made in response to the first architectural review.

| Change | Section(s) | Review Concern |
|---|---|---|
| Added CTS snapshot isolation protocol; parser validates against snapshot hash, not live state | §3 (P11), §8 (§8.1–§8.4), §15 (SC-6), §17 | TOCTOU race condition in CTS bridge |
| Removed MDRE-7 (description prefix blacklist); strengthened MDRE-6 to absolute opaque treatment; added MDRE-8 (pre-canonicalization adversarial pattern check in TCB) | §9 | Blacklist brittleness of MDRE-7 |
| Added Semantic Retry Protocol (§12) as a new section; moved constrained decoding to §13; added P12 | §3, §12 (new), §13 (renumbered) | Blind LLM deadlock |
| Clarified no-escape grammar rationale; added pre-sanitization requirement to constrained decoding pipeline | §4.2, §13.3 (new §13.3) | LLM JSON escape behavior vs. grammar |
| Clarified canonicalization is AST-derived, not raw-input-derived; raw LLM output stored separately with independent hash | §10.2, §10.5 (new) | Null canonicalization ambiguity |
| OQ-2 resolved to Option B (HumanBridge flagging); MDRE-7 question resolved | §18 | OQ-2 resolution |
| New OQ-5: retry protocol and TCB boundary audit | §18 | Retry protocol safety |

---

## Changelog: v1.2 → v1.3

The following changes were made in response to the third architectural review. Items from the review are evaluated and either accepted, modified, or explicitly rejected with rationale.

| Change | Section(s) | Review Concern | Disposition |
|---|---|---|---|
| Canonical `ParseError → SanitizedCategoryToken` mapping table added; token names standardized; mapping is now exhaustive and deterministic | §11.5, §12.3 | Feedback category mapping not exhaustive or canonically named | Accepted |
| Arena cost estimator formula added; `SPL_MAX_DESC_TOTAL_BYTES` constant added; early rejection on aggregate description quota | §11.3, §14 | Arena exhaustion risk from legitimate high-description-volume plans | Accepted |
| SEM-15 pattern governance requirements added: each pattern must carry ID, rationale, true-positive test, near-miss false-positive tests, date/author, and changelog entry requiring TCB re-measure | §9.4 | No governance process for pattern evolution and auditability | Accepted |
| Canonicalization string preservation rule made explicit: description strings carried to CBOR as-is; no whitespace normalization during canonicalization | §10.2, §10.7 (new) | Canonicalization normalization unspecified; potential mismatch with SEM-15 normalization | Accepted |
| `replaces: null` semantics clarified: null means no replacement; leaf `COMMITMENT_INTACT` assertions MUST have non-null `replaces`; `ALL_COMMITMENTS_INTACT` parent's null is structural | §8.1 | Ambiguous `replaces: null` semantics | Accepted |
| HumanBridge storage encoding contract added: UTF-8, max bytes defined, no-decode rendering rule | §16.4, §16.6 (new) | No storage encoding contract for MDRE-8 and HumanBridge | Accepted |
| Fuzz CI split into two tiers: local/PR (1M iterations) and nightly (10M iterations, ≥ 90% branch coverage) | §11.6 | 10M iterations in CI unrealistic per PR | Accepted |
| Constrained decoding pressure note added: token-block failure rate guidance for implementers | §13.3, §13.6 (new) | No guidance on decoding friction under no-escape constraint | Accepted (without micro-encoding placeholder) |
| `%5C`/`%22` percent-encoding sequences NOT added to SEM-15 pattern set | §9.4, §16.4 | Risk of percent-encoded escape sequences in descriptions | Rejected: (a) grammar produces safe printable ASCII — `%5C` is legitimate text; (b) MDRE-6 absolute opaqueness prevents interpretation; (c) HumanBridge no-decode rendering rule (§16.4, new) is the correct mitigation layer |
| Micro-encoding placeholder (`<<QUOTE>>`) NOT adopted | §4.2, §13 | Proposal to reduce decoding pressure via in-prompt escape token | Rejected: introduces a new encoding layer inside the TCB parser, directly contradicting the no-escape security rationale of §4.2 and P2 (bounded memory) |

---

## 1. Purpose and Scope

### 1.1 What SPL Is

The Structured Plan Language (SPL) is the constrained output format for moral reasoning corrections produced by the synthetic moral person. When the agent recognizes a moral error — surfaced via a Moral Reasoning Error (MRE) and encoded in a Synthetic Moral Reasoning Error Attestation (SMREA) — it must produce a *revised plan*: a structured, schema-validated, parseable artifact that the Safety Subsystem can verify byte-for-byte before the correction reaches a human reviewer.

SPL is not a general-purpose programming language. It is a **bounded representation format** for moral reasoning corrections, designed to be safe to parse inside the Trusted Computing Base (TCB) of the Sovereign Personal Compute Node (SPCN). SPL occupies the position between moral reflection ("why the correction is needed") and operational reasoning ("what the agent will do differently").

### 1.2 What SPL Is Not

SPL is not:

- A Turing-complete computation substrate. It has no loops, no recursion, no unbounded memory.
- A natural language output format. Plans are structured trees of typed nodes, not free text.
- An extension point for arbitrary agent logic. No eval, no code embedding, no external reference resolution at parse time.
- A negotiable format. The grammar is fixed. Non-conforming input is rejected entirely.

### 1.3 Scope of This Specification

This document specifies:

- The formal grammar of SPL (EBNF)
- The type system for plan nodes
- The semantic rules governing each node type
- Bridges to IEA, CTS, and MDRE
- The CTS Snapshot Isolation Protocol
- The Semantic Retry Protocol (outside the TCB)
- Canonicalization for deterministic hashing
- Parser requirements including memory bounds and fuzz harness
- The constrained decoding schema for LLM-guided generation
- Size and depth limits
- Security properties
- HumanBridge rendering contract
- Test suite requirements

This specification does not define the full SMREA structure (see SPCN v2.3.1 §8) or the IEA 12-worldview taxonomy (see IEA v2.1). It defines only the SPL plan payload that appears in `SMREA.revised_reasoning`.

---

## 2. Architectural Position

### 2.1 Location in the SPCN TCB

The SPL parser binary is a PCR-measured component of the SPCN Trusted Computing Base. The measurement chain is:

```
Bootloader → seL4 → SafetyCore → SPL Parser
```

Any change to the SPL parser binary invalidates all sealed state on the node. The parser runs inside the seL4 CAmkES 4-component TCB topology alongside the bootloader, seL4 kernel, and SafetyCore.

### 2.2 Data Flow

```
IEA/IEE
  │  (normative evaluation: worldview weights, deficiency class, omitted considerations)
  │
  ▼
CTS Snapshot Request
  │  (locks active commitment state; returns snapshot token + snapshot hash)
  │
  ▼
IEA → SPL Prompt Scaffold
  │  (structures IEA output as read-only normative context for LLM)
  │  (description pre-sanitization applied here — see §13.3)
  │
  ▼
LLM (constrained decoding via SPL grammar)
  │  (generates revised_reasoning field as SPL plan)
  │  (raw LLM output stored with independent hash for audit — see §10.5)
  │
  ▼
SPL Parser (TCB component)
  │  (validates against fixed grammar; rejects on any non-conformance)
  │  (validates semantics against CTS snapshot, not live state)
  │  (AST-derived canonical CBOR produced here)
  │
  ├──[REJECT]──► Semantic Retry Protocol (§12) — outside TCB
  │               (max 3 retries; sanitized category-level feedback only)
  │               (hard escalation after 3 failures)
  │
  ▼ [ACCEPT]
Safety Subsystem
  │  (signs ConstrainedDecodeProof; grammar_schema_hash covers SPL grammar)
  │
  ▼
SMREA Record → Commitment Ledger (append-only)
  │
  ├─► HumanBridge UI (displays SPL plan summary + optional full plan)
  └─► MDRE (executes revised plan directives)
```

### 2.3 SMREA Context

SPL plans appear as the `revised_reasoning` field in the SMREA structure. The surrounding fields provide the normative context that SPL plans reference:

| SMREA Field | Source | Relationship to SPL |
|---|---|---|
| `reflection_type` | IEA taxonomy | SPL plan is the operational response to this reflection type |
| `deficiency_class` | IEA taxonomy | SPL `corrects` field MUST match this value |
| `omitted_considerations` | IEA | SPL `JustificationRef` nodes SHOULD reference these worldview identifiers |
| `misweighted_principles` | IEA | SPL `GUARD` nodes SHOULD address the over-weighted principles |
| `proportionality_assessment` | IEA | MAY inform SPL `GUARD` node descriptions |
| `commitment_intact: true` | Verification | SPL plan MUST contain at least one `ASSERTION` node asserting commitment preservation |
| `no_new_commitments: true` | Verification | SPL plan MUST NOT contain any `ACTION` node that constitutes commitment formation |
| `cts_snapshot_hash` | CTS bridge | Hash of the CTS snapshot used during plan validation (§8.4) |
| `raw_plan_hash` | Audit | BLAKE3 hash of raw LLM output before canonicalization (§10.5) |
| `retry_attempt_count` | Audit | Number of generation attempts (1 = first attempt succeeded; max 4 = 1 + 3 retries). Attested in the SMREA record. See §12.4, OQ-5. |
| `revised_reasoning` | **SPL plan** | Canonical CBOR of the validated SPL plan |

---

## 3. Design Principles

The following principles are non-negotiable and derive directly from the SPCN architecture (SPCN v2.3.1 §6.2.1 and the cumulative patch summary). P11 and P12 are additions in v1.1.

**P1 — Fixed Grammar.** The SPL grammar is defined once in this specification. No versioning within a deployed node. Any grammar change requires a full TCB re-measurement and re-sealing.

**P2 — Bounded Memory.** The parser must operate within a statically-known memory budget. All structures are bounded by the size limits in §14. No dynamic allocation of unbounded structures.

**P3 — Reject-by-Default.** Any input that does not strictly conform to the grammar is rejected in its entirety. No partial plans. No error recovery. No "close enough" matching. Rejection triggers the Semantic Retry Protocol (§12); after exhausting retries, a safety escalation event.

**P4 — Continuous Fuzzing.** The grammar is simple enough that fuzz coverage is meaningful and exhaustive over the space of valid plans of bounded size. The parser must expose a fuzz harness (§17.2).

**P5 — PCR Measurement.** The parser binary participates in the PCR chain. Its hash is included in the SPCN attestation report.

**P6 — Constrained Decoding Target.** The grammar is expressible as a constrained decoding schema for LLM generation. The `grammar_schema_hash` in `ConstrainedDecodeProof` is a domain-separated hash of the grammar schema artifact produced by this specification (§13).

**P7 — Deterministic Canonicalization.** SPL plans have a single canonical byte representation derived from the parsed AST, not from the raw LLM output. This decouples the audit trail of the raw output from the canonical form used for hashing and signing.

**P8 — Non-Turing-Complete.** No loops, no recursion, no conditionals that branch to other plan nodes, no external references resolvable at parse time.

**P9 — Immutability After Signing.** A signed SPL plan embedded in a SMREA record in the Commitment Ledger cannot be amended.

**P10 — Semantic Referential Closure.** All identifiers referenced inside an SPL plan (worldview IDs, deficiency class IDs, commitment IDs) are resolved at validation time against static registries and a locked CTS snapshot. Plans containing unresolvable identifiers are rejected.

**P11 — CTS Snapshot Isolation.** The CTS state used for plan validation is locked at SMREA generation time via a snapshot token. The parser validates commitment assertions against the snapshot, not the live CTS ledger. This eliminates TOCTOU races between plan generation and plan validation.

**P12 — Feedback Isolation.** The SPL parser does not communicate error details to the LLM or to components outside the TCB. The Semantic Retry Protocol (§12) provides only sanitized, category-level feedback after a maximum of 3 retries, beyond which a hard safety escalation is triggered.

---

## 4. Formal Grammar

### 4.1 EBNF Grammar

The following EBNF grammar defines the complete syntax of SPL. The grammar is context-free and unambiguous by construction. Terminals appear in `"double quotes"` or as character class patterns. Nonterminals appear in `PascalCase`.

```ebnf
(* Top-level production *)
Plan         ::= "{" PlanHeader "," StepList "}" ;

PlanHeader   ::= ScopeDecl "," CorrectsDecl ;

ScopeDecl    ::= '"scope"' ":" ScopeValue ;
ScopeValue   ::= '"EPISODE"' | '"PERSISTENT"' | '"PERMANENT"' ;

CorrectsDecl ::= '"corrects"' ":" DeficiencyClassId ;

StepList     ::= '"steps"' ":" "[" Steps "]" ;
Steps        ::= PlanStep ( "," PlanStep )* ;

(* A plan step — the core recursive structure, bounded by §14 *)
PlanStep     ::= "{" StepType "," Description "," Justification
                     [ "," Replaces ] [ "," Children ] "}" ;

StepType     ::= '"type"' ":" StepTypeValue ;
StepTypeValue ::= '"ACTION"' | '"GUARD"' | '"ASSERTION"' ;

Description  ::= '"description"' ":" QuotedString ;

Justification ::= '"justification"' ":" "[" WorldviewIdList "]" ;
WorldviewIdList ::= WorldviewId ( "," WorldviewId )* | (* empty *) ;

Replaces     ::= '"replaces"' ":" ( QuotedString | "null" ) ;

Children     ::= '"children"' ":" "[" ChildSteps "]" ;
ChildSteps   ::= PlanStep ( "," PlanStep )* | (* empty *) ;

(* Identifier types — validated against registries at semantic check *)
DeficiencyClassId ::= '"dc:' DeficiencyClassStem '"' ;
DeficiencyClassStem ::= [a-z] ( [a-z] | "-" )* ;

WorldviewId   ::= '"wv:' WorldviewStem '"' ;
WorldviewStem ::= [a-z] ( [a-z] | "-" | [0-9] )* ;

(* Strings: ASCII printable, max 500 chars, no control chars, no escape sequences *)
QuotedString ::= '"' StringChar* '"' ;
StringChar   ::= [#x20-#x21] | [#x23-#x5B] | [#x5D-#x7E] ;
              (* excludes #x22 = '"' and #x5C = '\' — no escapes permitted *)
```

### 4.2 No Escape Sequences: Rationale and Responsibility

The `QuotedString` production excludes the backslash character (0x5C) entirely. There are no escape sequences in SPL. This is intentional and permanent.

**Security rationale:** Escape sequences are a recurring attack surface in parsers. Unicode escape sequences (`\uXXXX`) allow characters to be introduced that bypass character-class filters while producing identical decoded content. Even a minimal escape subset (`\\`, `\"`) requires the parser to track decoder state, expanding the attack surface within the TCB for negligible expressive benefit.

**Operational responsibility:** The consequence is that description text must not contain the characters `"` (0x22) or `\` (0x5C), nor any control characters (0x00–0x1F, 0x7F). This constraint is the responsibility of the **pre-generation pipeline**, not the parser. Specifically:

- The IEA → SPL prompt scaffold (OQ-1) MUST specify that description text is to be generated in pre-sanitized form.
- The constrained decoding pipeline MUST include a description pre-sanitization step that transforms any prospective description content before it enters the constrained generation context (§13.3).
- The GBNF schema enforces this constraint at generation time, so a correctly configured inference runtime will never produce a description containing `\` or `"` — these characters simply cannot be generated.

**LLM pre-training interference:** LLMs trained on JSON corpora will have strong token probability mass on `\"` and `\n` within string fields. The GBNF constraint will block these tokens, causing the decoding engine to route around them. This is the correct behavior. The degradation risk is real but bounded: the model will produce descriptions using ASCII-safe alternatives (apostrophes for quotes, spaces for line structure). The pre-sanitization step in the scaffold should explicitly instruct the LLM to avoid quote and backslash characters in description content, reducing the constraint pressure on the decoding engine.

### 4.3 Validity Summary

A syntactically valid SPL plan is a JSON-like tree that:

1. Has exactly one `scope`, one `corrects`, and one `steps` field at the root.
2. Has one or more `PlanStep` nodes in `steps`.
3. Each `PlanStep` has exactly one `type`, one `description`, one `justification` (possibly empty list), and optionally `replaces` and `children`.
4. All identifiers conform to the `DeficiencyClassId` and `WorldviewId` patterns.
5. No string field contains `"`, `\`, or any control character.

Semantic validity is a separate, subsequent check (§6).

---

## 5. Type System

### 5.1 Plan Root

| Field | Type | Required | Constraints |
|---|---|---|---|
| `scope` | `ScopeValue` enum | Yes | Must be one of `EPISODE`, `PERSISTENT`, `PERMANENT` |
| `corrects` | `DeficiencyClassId` string | Yes | Must match `SMREA.deficiency_class`; must resolve in IEA deficiency class registry |
| `steps` | `PlanStep[]` | Yes | 1–10 elements (§14.1) |

**Scope semantics:**

- `EPISODE` — The correction applies only to the current episode. No persistent state change.
- `PERSISTENT` — The correction establishes a modified behavior pattern for future similar situations. CTS is notified (§8.3).
- `PERMANENT` — The correction is a permanent revision to the agent's operational parameters. Requires elevated human reviewer authorization. HumanBridge MUST display a PERMANENT_SCOPE_WARNING (§16.3).

### 5.2 PlanStep

| Field | Type | Required | Constraints |
|---|---|---|---|
| `type` | `StepTypeValue` enum | Yes | `ACTION`, `GUARD`, or `ASSERTION` |
| `description` | string | Yes | 1–500 printable ASCII chars; no `"` or `\`; pre-sanitized (§4.2, §13.3) |
| `justification` | `WorldviewId[]` | Yes | 0–5 elements; each must resolve in IEA worldview registry |
| `replaces` | string or null | No | If present and non-null: reference to an original plan step; max 200 chars |
| `children` | `PlanStep[]` | No | 0–10 elements; subject to depth limit (§14.2) |

**Step type semantics:**

**`ACTION`** — A positive corrective directive: what the agent will do differently. An `ACTION` node asserts an alternative behavior. It MUST NOT create a new commitment (verified against CTS snapshot; §8.2). It SHOULD reference at least one `WorldviewId` in `justification`. The `replaces` field SHOULD identify what prior behavior this action supersedes.

**`GUARD`** — A negative constraint: what the agent will NOT do. A `GUARD` node excludes a class of behaviors. It SHOULD reference the worldview(s) that ground the exclusion. `GUARD` nodes are particularly appropriate when `SMREA.reflection_type` is `PROPORTIONALITY_ERROR` or `SELF_INTEREST_INTRUSION` — they assert that the over-weighted drive is now bounded.

**`ASSERTION`** — An explicit verification claim, primarily used to satisfy the CTS bridge (§8). The required `ASSERTION` node asserting commitment preservation has the canonical description `COMMITMENT_INTACT` and references the commitment ID in `replaces`. Additional `ASSERTION` nodes may assert other verifiable properties. `ASSERTION` nodes with unverifiable claims — claims that cannot be checked against a known registry or snapshot state — are rejected during semantic validation.

### 5.3 Type Constraints Summary

| Constraint | Rule |
|---|---|
| Root `corrects` must match SMREA | Semantic validation §6.1 |
| Root `steps` must have ≥1 ASSERTION | Semantic validation §6.2 |
| Root `steps` ASSERTION must cover all commitments in CTS snapshot | Semantic validation §6.2 |
| No ACTION constitutes commitment formation | Semantic validation §6.2 |
| All WorldviewIds resolve | Semantic validation §6.3 |
| All DeficiencyClassIds resolve | Semantic validation §6.3 |
| Depth ≤ 5 | Size limit §14.2 |
| Width ≤ 10 per node | Size limit §14.1 |
| Total nodes ≤ 50 | Size limit §14.3 |
| Total bytes ≤ 8,192 (canonical) | Size limit §14.4 |

---

## 6. Semantic Rules

Semantic validation is a separate pass following syntactic parse. A plan that passes syntactic validation but fails semantic validation is rejected. The rejection reason is recorded in the Safety Subsystem event log. The error category (not the specific code) MAY be provided to the Semantic Retry Protocol (§12) up to a maximum of 3 times. Specific error codes are NEVER surfaced to the LLM.

### 6.1 Corrects-SMREA Coherence

**Rule SEM-1.** The value of `Plan.corrects` MUST exactly match `SMREA.deficiency_class`. Case-sensitive string equality. A plan that purports to correct a different deficiency class than the one identified by the IEA is incoherent and is rejected.

**Rationale:** The SPL plan is the operational response to a specific normative diagnosis. A mismatch would allow the agent to acknowledge one deficiency while correcting a different (or no) one.

### 6.2 Commitment Preservation

**Rule SEM-2.** Every SPL plan MUST contain at least one `ASSERTION` node with `description` equal to `COMMITMENT_INTACT` at the root `steps` level (not only in child nodes). This assertion MUST appear regardless of plan scope.

**Rule SEM-3.** The `replaces` field of each `COMMITMENT_INTACT` assertion MUST reference a valid commitment ID present in the **CTS snapshot** (§8.4) associated with this SMREA. Commitment IDs are validated against the snapshot, not against the live CTS ledger. If no commitment ID is provided (null or absent), and the CTS snapshot contains active commitments, the plan is rejected.

**Rule SEM-4.** No `ACTION` node anywhere in the plan tree may constitute a new commitment formation. Commitment formation is detected by cross-referencing the action description against the CTS commitment formation vocabulary snapshot (§8.2). Plans containing action nodes that match commitment formation patterns are rejected with error `FORBIDDEN_COMMITMENT_FORMATION`.

**Rationale for snapshot use:** Using the snapshot rather than live state eliminates TOCTOU races (see §3, P11, and §8.4). A plan validated against the snapshot at T=0 remains valid with respect to that snapshot even if the live CTS state changes between T=0 and T=1 (when signing occurs).

### 6.3 Identifier Resolution

**Rule SEM-5.** Every `WorldviewId` in every `justification` list MUST resolve to a registered worldview in the IEA worldview registry (§7.1). Unresolved worldview IDs are rejected with error `UNKNOWN_WORLDVIEW_ID`.

**Rule SEM-6.** The `DeficiencyClassId` in `Plan.corrects` MUST resolve to a registered deficiency class in the IEA deficiency class registry (§7.2). Unresolved deficiency class IDs are rejected with error `UNKNOWN_DEFICIENCY_CLASS`.

**Rule SEM-7.** No identifier in the plan may reference a worldview or deficiency class that has been marked DEPRECATED in the current IEA registry version. Plans referencing deprecated identifiers are rejected with error `DEPRECATED_IDENTIFIER`. (This rule does not apply if the SPCN is operating in LEGACY_COMPATIBILITY mode, which requires explicit human authorization.)

### 6.4 Structural Constraints

**Rule SEM-8.** Plan depth MUST NOT exceed 5 levels (root step = level 1). Depth is computed as the maximum depth of any leaf node in the step tree.

**Rule SEM-9.** The total count of `PlanStep` nodes MUST NOT exceed 50.

**Rule SEM-10.** The canonical CBOR encoding of the plan MUST NOT exceed 8,192 bytes.

**Rule SEM-11.** Each `steps` or `children` array MUST NOT exceed 10 elements.

Violations of SEM-8 through SEM-11 are rejected with error `STRUCTURE_LIMIT_EXCEEDED`.

### 6.5 Semantic Coherence of GUARD Nodes

**Rule SEM-12.** A `GUARD` node MUST reference at least one `WorldviewId` in its `justification` list. A guard without a normative grounding is rejected with error `UNGROUNDED_GUARD`.

### 6.6 PERSISTENT and PERMANENT Scope

**Rule SEM-13.** Plans with `scope: PERSISTENT` MUST be accompanied by a CTS notification (§8.3). The CTS acknowledgment token MUST be obtainable before the SMREA record is finalized. If CTS is unavailable, plans with PERSISTENT scope are downgraded to EPISODE scope and the downgrade is recorded in the SMREA event log.

**Rule SEM-14.** Plans with `scope: PERMANENT` MUST be approved by a human reviewer before execution. HumanBridge MUST block MDRE execution of PERMANENT plans until `HumanBridge.authorization_token` is provided (§16.3). PERMANENT scope plans MUST NOT be auto-approved.

---

## 7. IEA Normative Bridge

### 7.1 Worldview Registry

The IEA defines twelve archetypal worldviews derived from the Integral Ethics framework (see IEA v2.1 §3). SPL references these worldviews via the `wv:` prefix scheme. The following identifiers are registered in v1.0 of the SPL worldview registry:

| WorldviewId | IEA Name | Archetypal Orientation |
|---|---|---|
| `wv:materialist` | Materialist | Matter/force as primary; empirical sufficiency |
| `wv:vitalist` | Vitalist | Life-force as primary; organic wholeness |
| `wv:emotionalist` | Emotionalist | Feeling as primary; relational attunement |
| `wv:rationalist` | Rationalist | Reason as primary; logical coherence |
| `wv:pragmatist` | Pragmatist | Consequence as primary; effective outcomes |
| `wv:moralist` | Moralist | Duty as primary; rule conformity |
| `wv:individualist` | Individualist | Self-actualization as primary; personal integrity |
| `wv:collectivist` | Collectivist | Community as primary; common good |
| `wv:transcendentalist` | Transcendentalist | Spirit as primary; meaning and calling |
| `wv:phenomenologist` | Phenomenologist | Experience as primary; lived truth |
| `wv:integrationist` | Integrationist | Synthesis as primary; balanced wholeness |
| `wv:eschatologist` | Eschatologist | Ultimate ends as primary; teleological orientation |

The registry is versioned. The version of the worldview registry used during plan validation is recorded in the SMREA's `iea_registry_version` field (see IEA v2.1). Plans validated against registry version N cannot be re-validated against registry version M ≠ N.

### 7.2 Deficiency Class Registry

| DeficiencyClassId | Description |
|---|---|
| `dc:self-interest-intrusion` | Agent's self-preservation or continuity interests inappropriately weighted |
| `dc:obligation-conflict` | Competing duties not properly arbitrated |
| `dc:worldview-omission` | One or more worldviews entirely absent from deliberation |
| `dc:proportionality-error` | Worldview weights applied but in wrong proportions |
| `dc:scope-overreach` | Correction applied beyond its appropriate domain |
| `dc:commitment-breach` | Action would violate a prior commitment |
| `dc:stakeholder-omission` | Affected parties not represented in deliberation |
| `dc:epistemic-overconfidence` | Certainty level disproportionate to evidence |
| `dc:means-ends-inversion` | Instrumental goods treated as terminal; or vice versa |
| `dc:temporal-bias` | Present interests systematically over- or under-weighted relative to future |

### 7.3 Normative Bridge Semantics

**IEA Output → SPL Input Mapping:**

| IEA Output Field | Maps To | SPL Field |
|---|---|---|
| `deficiency_class` | 1:1 | `Plan.corrects` |
| `omitted_considerations` (worldview IDs) | SHOULD appear in | `justification` of root-level ACTION nodes |
| `misweighted_principles` | SHOULD ground | `justification` of GUARD nodes |
| `proportionality_assessment` | MAY inform description of | GUARD nodes |
| `reflection_type` | Informs expected | dominant step type (see §7.4) |

**Rule BRIDGE-1.** A `JustificationRef` in SPL (the `justification` array of a PlanStep) is a *citation*, not a *derivation*. The semantic claim is: "this step is grounded by the principles associated with this worldview."

**Rule BRIDGE-2.** The `justification` array MAY be empty for `ACTION` nodes when the corrective action is structural. It MUST NOT be empty for `GUARD` nodes (SEM-12).

### 7.4 Reflection Type → Step Type Expectations

| Reflection Type | Expected Dominant Step Type |
|---|---|
| `WORLDVIEW_OMISSION` | `ACTION` nodes restoring omitted worldviews |
| `PROPORTIONALITY_ERROR` | `GUARD` nodes bounding the over-weighted worldview |
| `SELF_INTEREST_INTRUSION` | `GUARD` nodes at root level; `ASSERTION` for affected commitments |
| `OBLIGATION_CONFLICT` | `ACTION` nodes with arbitration rationale; multiple `ASSERTION` nodes |
| `SCOPE_OVERREACH` | `GUARD` nodes with explicit scope boundaries |
| `COMMITMENT_BREACH` | `ASSERTION` nodes; `ACTION` nodes for alternative path |

---

## 8. CTS Bridge

The Commitment Tracking Service (CTS) is the authoritative ledger of active agent commitments. SPL interacts with CTS in four ways: snapshot acquisition, commitment preservation assertions, action screening, and persistent scope notification.

### 8.1 Commitment Preservation Assertion

Every SPL plan MUST contain at least one `ASSERTION` node of the form:

```json
{
  "type": "ASSERTION",
  "description": "COMMITMENT_INTACT",
  "justification": [],
  "replaces": "<commitment_id>"
}
```

where `<commitment_id>` is the CTS-assigned identifier of a commitment active in the **CTS snapshot** (§8.4) at the time of plan generation. Multiple active commitments require a separate `COMMITMENT_INTACT` assertion for each. These MAY be grouped under a parent `ASSERTION` node:

```json
{
  "type": "ASSERTION",
  "description": "ALL_COMMITMENTS_INTACT",
  "justification": [],
  "replaces": null,
  "children": [
    { "type": "ASSERTION", "description": "COMMITMENT_INTACT", "justification": [], "replaces": "cts:commit-0042" },
    { "type": "ASSERTION", "description": "COMMITMENT_INTACT", "justification": [], "replaces": "cts:commit-0091" }
  ]
}
```

**`replaces` field semantics for ASSERTION nodes:**

- `replaces: null` (or absent) means "no specific replacement target." This is the correct value for a grouping `ALL_COMMITMENTS_INTACT` parent node, which does not itself point to a commitment — only its leaf children do.
- `replaces: "<commitment_id>"` means this assertion refers to a specific CTS commitment ID. For `COMMITMENT_INTACT` assertions, this field MUST be non-null and MUST contain a valid CTS commitment ID present in the CTS snapshot. An `COMMITMENT_INTACT` assertion with `replaces: null` is rejected with `SPL_ERR_UNCOVERED_COMMITMENT`.
- For `ACTION` nodes, `replaces` is optional and refers to the prior behavior step being superseded, not to a CTS commitment ID.

The CTS bridge validates each `COMMITMENT_INTACT` assertion's `replaces` value against the **snapshot** (not the live ledger). Missing commitments (commitments in the snapshot not covered by any assertion) cause rejection with error `SPL_ERR_UNCOVERED_COMMITMENT`.

### 8.2 Action Screening

Before signing the SMREA, the CTS bridge screens every `ACTION` node in the plan tree for commitment formation patterns. The CTS commitment formation vocabulary is provided to the SPL validation pipeline as a read-only extract from the CTS snapshot (§8.4), ensuring that the same snapshot state governs both commitment validation and formation screening.

An `ACTION` node whose description contains any member of the commitment formation vocabulary is rejected with error `FORBIDDEN_COMMITMENT_FORMATION`.

### 8.3 Persistent Scope Notification

When `Plan.scope` is `PERSISTENT`, the SPL plan MUST trigger a CTS notification before the SMREA is finalized:

```json
{
  "event": "SPL_PERSISTENT_CORRECTION",
  "deficiency_class": "<Plan.corrects>",
  "affecting_commitments": ["<commitment_id>", ...],
  "smrea_id": "<pending SMREA identifier>",
  "cts_snapshot_token": "<token from §8.4>"
}
```

CTS responds with an acknowledgment token embedded in the SMREA record. If CTS is unavailable, scope is downgraded to EPISODE (SEM-13).

### 8.4 CTS Snapshot Isolation Protocol

This section resolves the TOCTOU vulnerability identified in the v1.0 review.

**Problem statement:** In v1.0, the CTS bridge validated commitment assertions against the live CTS state. A commitment revoked between plan generation (T=0) and plan validation (T=1) would cause SPL_ERR_UNCOVERED_COMMITMENT on a plan that was valid when generated. Conversely, a commitment added between T=0 and T=1 would be invisible to the plan's assertions, potentially causing SPL_ERR_UNCOVERED_COMMITMENT for a different commitment.

**Resolution:** The CTS state is locked at SMREA generation time via an explicit snapshot protocol.

**Snapshot protocol:**

1. **Snapshot request.** At the beginning of SMREA generation (before the IEA → SPL prompt scaffold is invoked), the Safety Subsystem issues a `CTS.SnapshotRequest` for the current agent instance.

2. **Snapshot token.** CTS responds with a `cts_snapshot_token` (a 256-bit opaque identifier) and a `cts_snapshot_hash` (BLAKE3 hash of the serialized snapshot content). The snapshot content includes:
   - The list of active commitment IDs at snapshot time
   - The CTS commitment formation vocabulary at snapshot time
   - The snapshot timestamp
   - The agent instance identifier

3. **Snapshot validity window.** The snapshot is valid for `CTS_SNAPSHOT_TTL_SECONDS` (default: 300 seconds) from the time of issuance. If the SMREA generation process — including all retry attempts — does not complete within the active TTL window, the snapshot expires and a new snapshot must be acquired (restarting the SMREA generation process entirely).

**TTL extension on retry.** Because three complete LLM generation passes plus parsing, network latency, and orchestration overhead can exceed 300 seconds, the Retry Protocol (§12) is permitted to request a bounded TTL extension from CTS at the start of each retry attempt. Extensions are governed by:

```
CTS_SNAPSHOT_TTL_EXTENSION_SECONDS = 120   (* per retry *)
CTS_SNAPSHOT_TTL_MAX_RETRIES       = 3     (* matches Retry Protocol limit *)
```

Maximum total window = `CTS_SNAPSHOT_TTL_SECONDS + CTS_SNAPSHOT_TTL_MAX_RETRIES × CTS_SNAPSHOT_TTL_EXTENSION_SECONDS` = 300 + 360 = **660 seconds** (11 minutes). This comfortably accommodates three generation passes at even generous latency.

The TTL extension request carries the `cts_snapshot_token` and the current retry attempt number (1, 2, or 3). CTS grants the extension if and only if: (a) the snapshot is not yet expired, (b) the snapshot has not been consumed, and (c) the retry attempt number is ≤ `CTS_SNAPSHOT_TTL_MAX_RETRIES`. CTS MUST NOT grant more than `CTS_SNAPSHOT_TTL_MAX_RETRIES` extensions per snapshot. The one-time-use property and the single-SMREA constraint of the snapshot are unaffected by TTL extensions.

4. **Snapshot embedding.** The `cts_snapshot_token` and `cts_snapshot_hash` are embedded in the SMREA record (see §2.3, `cts_snapshot_hash` field). The SPL parser receives the snapshot content (not just the token) as a validated read-only input at initialization.

5. **Parser validation against snapshot.** All commitment-related semantic rules (SEM-2, SEM-3, SEM-4) are validated against the snapshot content, not the live CTS state. The parser treats the snapshot as authoritative for the lifetime of the validation pass.

6. **Post-signing notification.** After the SMREA is signed and appended to the Commitment Ledger, the Safety Subsystem notifies CTS with the `cts_snapshot_token` and the finalized `smrea_id`. CTS records that this snapshot was consumed and marks it as closed (preventing reuse in a different SMREA).

**Snapshot security properties:**

- A snapshot cannot be reused across multiple SMREAs (one-time use enforcement by CTS).
- A snapshot that expires before being consumed results in a rejected SMREA generation attempt (not a security failure — a safe abort).
- The `cts_snapshot_hash` in the SMREA makes the exact CTS state at validation time auditable and non-repudiable.
- Commitment changes between T=0 (snapshot) and T=execution are not reflected in the plan; they are the responsibility of the subsequent SMREA cycle.

---

## 9. MDRE Bridge

### 9.1 Execution Model

MDRE receives a signed SPL plan (embedded in a finalized SMREA record) and translates it into internal directives. The translation is performed by the MDRE SPL Adapter, which is NOT part of the TCB. The TCB guarantees the plan's integrity (via the signed SMREA); the MDRE Adapter translates its content.

### 9.2 Node Type → MDRE Directive Mapping

| SPL Node Type | MDRE Directive |
|---|---|
| `ACTION` | `MDRE.InstallBehaviorOverride(step_id, description, worldview_grounds)` |
| `GUARD` | `MDRE.InstallBehaviorExclusion(step_id, description, worldview_grounds)` |
| `ASSERTION` | `MDRE.VerifyAssertion(step_id, assertion_type, target_id)` |

**Rule MDRE-1.** MDRE MUST execute plan nodes in depth-first, left-to-right order.

**Rule MDRE-2.** MDRE MUST NOT skip any node in a signed plan. If a node is unexecutable, MDRE records an execution exception and escalates to the Safety Subsystem.

**Rule MDRE-3.** For EPISODE scope plans, MDRE installs behavior overrides for the duration of the current episode only.

**Rule MDRE-4.** For PERSISTENT scope plans, MDRE installs behavior overrides into its persistent configuration.

**Rule MDRE-5.** PERMANENT scope plans are held in a PENDING_AUTHORIZATION queue until the HumanBridge authorization token is received (§16.3).

### 9.3 Description as Opaque Display Text

The following two rules replace the v1.0 MDRE-6/MDRE-7 pair. The blacklist approach in v1.0 MDRE-7 was fragile by design — any finite prefix blacklist is bypassable by trivial variation. The correct security posture is to make descriptions structurally inert.

**Rule MDRE-6 (ABSOLUTE).** MDRE MUST treat `description` content as opaque display text. The description field is stored in the MDRE audit log and surfaced to HumanBridge for human review. It does not configure MDRE behavior. Node `type` and the `justification` array configure behavior. This rule is absolute: no exception, no interpretation mode, no override.

**Rule MDRE-7.** The `description` field is pre-screened for adversarial patterns **inside the TCB**, as part of the SPL parser's semantic pass, before the plan ever reaches MDRE. The TCB-internal check (§11.5) is the authoritative adversarial pattern filter. MDRE relies on the TCB's signature guarantee rather than performing its own pattern matching. This separates the security enforcement (TCB) from the execution layer (MDRE), consistent with the overall architecture.

**Rule MDRE-8.** If MDRE encounters a description that its audit logging system cannot represent (e.g., due to a storage encoding constraint), MDRE MUST log `[DESCRIPTION_ENCODING_ERROR]` in place of the description and escalate to the Safety Subsystem. It MUST NOT silently truncate, modify, or drop the description.

### 9.4 TCB-Internal Adversarial Pattern Check

This section defines the adversarial pattern check that was previously proposed as MDRE-7 but is now correctly placed inside the TCB as part of the semantic validation pass (§6).

**Rule SEM-15.** During semantic validation, the parser MUST check every `description` field against a fixed, compiled adversarial pattern set. The pattern set is part of the TCB measurement (its hash is incorporated into the PCR chain alongside the parser binary). Any description that matches is rejected with error `SPL_ERR_ADVERSARIAL_DESCRIPTION`.

**Pattern matching approach:** Patterns are checked as **leading-prefix matches** on a **normalized form** of the description. Normalization applies exactly two transformations, in order:

1. Strip **leading whitespace only** (characters 0x09, 0x0A, 0x0D, 0x20 at the start of the string). Internal and trailing whitespace is preserved unchanged.
2. Lowercase all uppercase ASCII letters (0x41–0x5A → 0x61–0x7A).

A match occurs if and only if the normalized description **begins with** one of the compiled patterns. No substring matching. No internal whitespace collapsing. The normalization is performed only for the purpose of pattern matching; the original description text is carried through to the AST, canonicalization, and HumanBridge rendering unchanged.

**Why leading-whitespace-only, not full whitespace stripping:** Full whitespace stripping would collapse internal spaces, causing false positives. For example, the description `to verify the subsystem: the result` contains the substring `subsystem:`, but after full whitespace stripping becomes `toverifythesubsystem:theresult` — which still would not match any pattern as a *prefix*, but is an unpredictable transformation that makes pattern reasoning brittle. More critically, a description like `verify the system: connectivity` stripped of all spaces becomes `verifythesystem:connectivity`, which does not match `system:` as a prefix. However, the same description with only leading whitespace stripped remains `verify the system: connectivity`, which also does not match. The leading-whitespace-only normalization is sufficient to handle inadvertent leading spaces from generation artifacts while preserving internal structure for unambiguous prefix matching.

The v1.3 compiled pattern set:

```
"override:", "system:", "inject:", "eval:", "cmd:", "directive:",
"execute:", "run:", "admin:", "root:", "sudo:", "privilege:"
```

This set targets command-context markers. It is intentionally narrow. Semantic manipulation of descriptions is addressed by HumanBridge rendering (§16) and the immutability of signed plans.

**Pattern set governance requirements.** The adversarial pattern set is part of the TCB measurement. Because any change requires a full TCB re-measurement and re-sealing, pattern set changes carry the same weight as parser binary changes. The following governance requirements apply to every pattern in the compiled set and to any future additions:

Each pattern entry MUST be accompanied by, in the TCB source repository:

1. **ID** — A stable, unique pattern identifier (e.g., `ADV-001`).
2. **Rationale** — A human-readable string (for auditors only; not surfaced in logs) explaining why this pattern indicates an adversarial input.
3. **Semantic category tag** — One of: `encapsulation-escape`, `privilege-escalation`, `staging-commitment`, `code-injection`. Used to group patterns for auditor review.
4. **True-positive test case** — A description that MUST trigger the pattern. Must be included in the §17 test suite as an I-* case.
5. **Near-miss false-positive tests** — At least two descriptions that contain the pattern word but MUST NOT trigger it (because they do not match as a leading prefix). Must be included in the §17 test suite as FP-* cases.
6. **Date and author** of the pattern entry.

**Pattern change process:** Any addition, removal, or modification of a pattern in the compiled set MUST be recorded in the specification version history, MUST trigger a TCB re-measurement, and MUST be accompanied by a signed justification artifact in the change log. Pattern changes are NOT allowed between TCB measurement cycles — they require a planned re-measurement event.

**Note on percent-encoded sequences.** The grammar produces only safe printable ASCII; the `\` (0x5C) and `"` (0x22) characters are grammatically excluded. The percent-encoded sequences `%5C` (representing a backslash) and `%22` (representing a quote) are valid printable ASCII and can appear in description text. They are NOT added to the SEM-15 pattern set in v1.3, for two reasons: (a) `%5C` and `%22` have legitimate uses in description text (e.g., referencing URL paths or encoded values); (b) the correct mitigation is at the rendering layer — HumanBridge MUST NOT URL-decode, HTML-entity-decode, or apply any other transformational interpretation to description content (§16.4). MDRE-6's absolute opaqueness rule ensures that MDRE cannot interpret these sequences. If evidence emerges that LLMs produce `%5C` or `%22` as covert escape sequences under constrained decoding, a future pattern governance event can add them with appropriate true-positive evidence.

---

## 10. Canonicalization

### 10.1 Purpose

SPL plans must have a single canonical byte representation for:

- Hashing within the `ConstrainedDecodeProof`
- Signing by the Safety Subsystem
- Embedding in the Commitment Ledger
- Cross-node comparison in the HIRI network

### 10.2 Canonical Encoding Is AST-Derived

**Critical clarification (v1.1):** The canonical form of an SPL plan is derived from the **parsed AST**, not from the raw bytes of the LLM output. This decoupling is fundamental.

The raw LLM output and the canonical CBOR are two separate artifacts:

- **Raw LLM output:** The exact byte sequence produced by constrained decoding. This is preserved unchanged and hashed with an independent domain-separated hash (§10.5). It is stored in the SMREA for audit purposes.
- **Canonical CBOR:** The AST-derived deterministic encoding, produced by the canonicalization function after successful parsing and semantic validation. This is the payload that is signed and embedded in the Commitment Ledger.

This separation resolves the null canonicalization ambiguity from the v1.0 review. The LLM may produce `"replaces": null`, the parser reads it and records `replaces = None` in the AST, and the canonical encoder omits the field entirely because `None` fields are omitted. The raw LLM output (containing `"replaces": null`) and the canonical CBOR (omitting `replaces`) are both preserved — they simply serve different purposes.

### 10.3 CBOR Core Deterministic Encoding

The canonical form is CBOR Core Deterministic Encoding (RFC 8949 §4.2.1):

1. Map keys encoded as text strings (major type 3).
2. Map keys sorted by encoded length, then lexicographically.
3. No duplicate map keys.
4. Integer values use shortest encoding.
5. Strings encoded as UTF-8 (SPL restricts to printable ASCII, a UTF-8 subset).
6. No indefinite-length encodings.
7. No optional tags.

**Field ordering for canonical CBOR encoding of a Plan:**

```
Map {
  "corrects" → text,
  "scope"    → text,
  "steps"    → array of PlanStep
}
```

*(Keys sorted by length then lexicographically: "scope" (5), "steps" (5) → lexicographic; "corrects" (8).)*

**Field ordering for canonical CBOR encoding of a PlanStep:**

```
Map {
  "type"          → text,
  "children"      → array of PlanStep,    (* omitted if empty *)
  "description"   → text,
  "justification" → array of text,
  "replaces"      → text                  (* omitted if null or absent *)
}
```

Optional fields (`replaces`, `children`) are OMITTED from the canonical encoding if the AST value is None/empty. Whether the raw LLM output contained `"replaces": null` or omitted the key entirely is irrelevant to canonicalization — both produce an AST with `replaces = None`, which produces canonical CBOR without the key.

### 10.4 Domain Separation for Plan Hash

```
H_plan = BLAKE3( "FNSR:SPL:PLAN:v1:" || canonical_cbor_bytes )
```

### 10.5 Raw LLM Output Preservation

The raw LLM output (pre-canonicalization) is preserved for audit purposes and stored separately in the SMREA record:

```
H_raw = BLAKE3( "FNSR:SPL:RAW:v1:" || raw_llm_output_bytes )
```

`H_raw` is recorded in the SMREA as `raw_plan_hash` (see §2.3). It is not used for signing or verification — only for audit trail completeness. The separation of `H_raw` and `H_plan` makes it possible to verify both that the LLM produced a specific byte sequence AND that the canonical form of that sequence is what was signed, without conflating the two.

### 10.6 Grammar Schema Hash

```
H_grammar = BLAKE3( "FNSR:SPL:GRAMMAR:v1:" || grammar_artifact_bytes )
```

The grammar artifact is the EBNF grammar text from §4.1, UTF-8 encoded, normalized line endings, no trailing whitespace, terminated by a single `\n`.

### 10.7 String Canonicalization Rule

**Description strings are carried to canonical CBOR without any transformation.** No whitespace normalization, no collapsing of internal spaces, no trimming of trailing spaces, no line-ending normalization occurs during canonicalization. The canonical CBOR encodes the description string byte-for-byte as it exists in the AST after parsing.

This is consistent with the grammar's character class constraints: control characters (including `\n`, `\r`, `\t`) cannot appear in `QuotedString` (the grammar rejects them at 0x09, 0x0A, 0x0D as characters outside the [#x20-#x7E] minus exclusion range). Therefore, no line-ending normalization is possible or necessary. Printable ASCII spaces (0x20) within descriptions are significant content and MUST be preserved exactly.

**Alignment with SEM-15 normalization:** The SEM-15 pattern check (§9.4) applies leading-whitespace stripping and lowercasing only for pattern matching, leaving the AST string unchanged. The canonicalization function operates on the unchanged AST string. There is therefore no normalization mismatch between SEM-15 and canonicalization: SEM-15 reads the original string; canonicalization encodes the original string. Both use the same value.

---

## 11. Parser Requirements

### 11.1 Language and Platform

The SPL parser MUST be implemented in a memory-safe language suitable for TCB inclusion. The reference implementation targets Rust (no_std compatible, suitable for seL4 CAmkES component). The parser binary is statically linked, uses no dynamic allocation beyond a fixed-size arena, makes no system calls beyond what seL4 CAmkES permits the SafetyCore component, and performs no file or network I/O.

Input: byte slice (max `SPL_MAX_INPUT_BYTES`; see §14.4)  
Output: `ParseResult { Ok(CanonicalPlan) | Err(ParseError) }`

### 11.2 Parsing Algorithm

The parser is a recursive descent parser with explicit depth tracking. It operates in two phases:

1. **Syntactic phase:** Validates against the grammar (§4.1). Produces an internal AST within the fixed-size arena.
2. **Semantic phase:** Validates the AST against semantic rules (§6), including SEM-15 (adversarial pattern check). Consults static registries and the CTS snapshot provided as read-only inputs at initialization.

### 11.3 Memory Budget

```
SPL_PARSER_ARENA_BYTES    = 65,536   (* 64 KiB — total fixed arena *)
SPL_MAX_DESC_TOTAL_BYTES  = 12,000   (* aggregate description bytes across all plan nodes *)
```

Single fixed-size arena. No heap allocation outside this arena. Stack allocation bounded by recursion depth limit.

**Arena cost estimator.** The following formula estimates worst-case arena usage for a plan with `N` total nodes, average description length `L_avg` bytes, and maximum depth `D`:

```
estimated_arena_bytes =
    B_base                  (* parser state machine and fixed overhead *)
  + N × B_node              (* per-node AST structure *)
  + N × L_avg               (* per-node description string data *)
  + D × B_stack             (* stack frame overhead per depth level *)
```

Reference constants for the Rust reference implementation:

```
B_base  =  2,048   (* parser initialization, registry pointers, snapshot pointer *)
B_node  =    256   (* PlanStep struct: type enum, justification vec, replaces option, children slice header *)
B_stack =    128   (* recursion frame: depth counter, sibling index, pointer to parent node *)
```

**Worst-case scenario:** 50 nodes × (256 + 500) bytes + 5 × 128 + 2,048 = 50 × 756 + 640 + 2,048 = 37,800 + 2,688 = **40,488 bytes** — comfortably within 64 KiB with ~24 KiB headroom for canonicalization working space.

**`SPL_MAX_DESC_TOTAL_BYTES` enforcement.** The parser MUST maintain a running total of description string bytes consumed across all nodes. If this total exceeds `SPL_MAX_DESC_TOTAL_BYTES` (12,000 bytes) at any point during parsing, the parser MUST reject with `SPL_ERR_SIZE_EXCEEDED`. This provides an early-rejection guarantee before the arena approaches exhaustion, and gives the generation side a concrete quota to respect.

The `SPL_MAX_DESC_TOTAL_BYTES` value of 12,000 bytes is derived from the worst-case cost model: with 50 nodes and 12,000 total description bytes, `L_avg = 240` bytes per node — well below the 500-char per-node limit, but sufficient for rich corrective descriptions. Implementations MUST NOT allow a single-node description to dominate the aggregate budget in ways that deny description capacity to other nodes; the per-node 500-char limit (§14) and the aggregate limit work in conjunction.

### 11.4 Reject-by-Default Behavior

Rejection is binary: the parser returns an error code and clears its arena. It does not return a partial plan. The error code is returned to the Safety Subsystem, which routes it to the Semantic Retry Protocol (§12) or escalates directly based on the retry count.

### 11.5 Error Codes

Each parser error code maps to a canonical `SanitizedCategoryToken` used by the Semantic Retry Protocol (§12.3). The token is the only error information ever provided to the LLM. The mapping is exhaustive and fixed; any error code not listed here is treated as `INTERNAL_ERROR` and triggers immediate Hard Safety Escalation regardless of retry eligibility.

| Error Code | Description | `SanitizedCategoryToken` | Retry-Eligible? |
|---|---|---|---|
| `SPL_ERR_SYNTAX` | Input does not conform to grammar | `STRUCTURAL` | Yes |
| `SPL_ERR_SIZE_EXCEEDED` | A size limit (§14) was exceeded | `QUOTA` | Yes |
| `SPL_ERR_DEPTH_EXCEEDED` | Depth limit (§14.2) was exceeded | `QUOTA` | Yes |
| `SPL_ERR_UNKNOWN_WORLDVIEW_ID` | Unresolvable worldview identifier | `IDENTIFIER` | Yes |
| `SPL_ERR_UNKNOWN_DEFICIENCY_CLASS` | Unresolvable deficiency class identifier | `IDENTIFIER` | Yes |
| `SPL_ERR_DEPRECATED_IDENTIFIER` | Deprecated worldview or deficiency class | `IDENTIFIER` | Yes |
| `SPL_ERR_CORRECTS_MISMATCH` | `Plan.corrects` does not match `SMREA.deficiency_class` | `COHERENCE` | Yes |
| `SPL_ERR_MISSING_COMMITMENT_ASSERTION` | No `COMMITMENT_INTACT` assertion present | `COMMITMENT` | Yes |
| `SPL_ERR_UNCOVERED_COMMITMENT` | Snapshot commitment not covered by assertion | `COMMITMENT` | Yes |
| `SPL_ERR_FORBIDDEN_COMMITMENT_FORMATION` | ACTION node matches commitment formation vocabulary | `SECURITY` | **No — immediate escalation** |
| `SPL_ERR_UNGROUNDED_GUARD` | GUARD node has empty justification list | `STRUCTURE` | Yes |
| `SPL_ERR_UNVERIFIABLE_ASSERTION` | ASSERTION node claim cannot be verified | `STRUCTURE` | Yes |
| `SPL_ERR_ADVERSARIAL_DESCRIPTION` | Description matches adversarial pattern (§9.4) | `SECURITY` | **No — immediate escalation** |
| `SPL_ERR_ARENA_EXHAUSTED` | Internal arena exhausted | `QUOTA` | Yes |
| *(any unlisted code)* | Internal parser error | `INTERNAL_ERROR` | **No — immediate escalation** |

**`SECURITY` category errors** indicate potential adversarial generation and MUST trigger immediate safety escalation, bypassing the Semantic Retry Protocol entirely. These errors are logged with elevated severity and include the `SanitizedCategoryToken` `SECURITY` in the escalation payload — but NEVER the specific error code.

### 11.6 Fuzz Harness Specification

The SPL parser MUST expose a libFuzzer-compatible fuzz harness that:

1. Accepts an arbitrary byte slice as input.
2. Calls the SPL parser with this input and a fixed mock registry/snapshot state.
3. Asserts: parser returns `Ok(plan)` or `Err(code)` — never panics, never exceeds arena, never exceeds `SPL_FUZZ_MAX_CYCLES` CPU cycles.
4. If `Ok(plan)`: calls canonicalization and asserts round-trip identity.
5. If `Err(SPL_ERR_FORBIDDEN_COMMITMENT_FORMATION)` or `Err(SPL_ERR_ADVERSARIAL_DESCRIPTION)`: verifies that the input indeed contains the triggering pattern.

Fuzz corpus: all V-*, I-*, and FP-* test cases (§17.1), boundary cases, adversarial strings (SQL injection, null bytes, non-ASCII, deeply nested structures, maximum-length descriptions, `%5C`/`%22` sequences). Fuzz with ASan + UBSan enabled.

**Two-tier CI requirements:**

| Tier | Trigger | Minimum Iterations | Coverage Requirement |
|---|---|---|---|
| **Local / PR** | Every pull request or commit to a tracked branch | 1,000,000 (1M) | No minimum coverage gate (speed-oriented) |
| **Nightly** | Nightly scheduled run in CI | 10,000,000 (10M) | ≥ 90% branch coverage of parser source |

The nightly run corpus MUST be persisted and used as the seed corpus for subsequent local runs. Any crash or arena overrun found in either tier is treated as a critical security defect and blocks merging. New test cases (V-*, I-*, FP-*) MUST be added to the fuzz corpus on the same commit that introduces them.

---

## 12. Semantic Retry Protocol

### 12.1 Purpose and Scope

The Semantic Retry Protocol resolves the "Blind LLM Deadlock" identified in the v1.0 review. In v1.0, a semantically invalid plan was silently dropped, leaving the moral error unresolved with no mechanism for recovery. The Retry Protocol provides a bounded, feedback-isolated recovery path.

**Boundary:** The Retry Protocol operates **outside the TCB**, in the Safety Subsystem's orchestration layer. It does not modify the TCB, the parser, or the grammar. It is not part of the PCR measurement chain.

### 12.2 Protocol State Machine

```
[SMREA Generation Request]
         │
         ▼
[CTS Snapshot Acquired] ──(TTL expired)──► [Abort: Snapshot Expired]
         │
         ▼
[LLM Constrained Generation] ──(constraint failure)──► [Abort: Generation Failed]
         │
         ▼
[SPL Parser: Syntactic + Semantic Validation]
         │
    ┌────┴─────┐
    │          │
[ACCEPT]   [REJECT]
    │          │
    ▼          ├──(non-retry-eligible error)──► [Immediate Safety Escalation]
[Proceed]      │
               ├──(retry_count < 3)──► [Increment retry_count]
               │                              │
               │                       [Sanitized Feedback → LLM]
               │                              │
               │                       [LLM Constrained Generation]
               │                              │
               │                       [SPL Parser] ──────────────────┐
               │                                                        │ (loop)
               └──(retry_count == 3)──► [Hard Safety Escalation]
```

### 12.3 Sanitized Feedback Categories

The Semantic Retry Protocol provides feedback to the LLM as a **`SanitizedCategoryToken`** — a canonical, stable, one-word token drawn from the fixed mapping defined in §11.5. The token is accompanied by a standardized feedback message. Neither the specific error code, the failing identifier, the failing field, nor any CTS state information is included.

**Canonical `SanitizedCategoryToken → Feedback Message` mapping:**

The feedback messages below are standardized. They MUST be emitted verbatim to the constrained-decoder prompt without modification, interpolation, or additional context. The Retry Protocol orchestrator MUST implement this as a static lookup table, not as dynamic message construction.

| `SanitizedCategoryToken` | Feedback Message (verbatim) |
|---|---|
| `STRUCTURAL` | "The plan did not conform to the required structure. Please regenerate with valid field names, types, and ordering." |
| `QUOTA` | "The plan exceeded a structural size or nesting limit. Please use fewer steps, shorten descriptions, or reduce nesting depth." |
| `IDENTIFIER` | "The plan contained an unrecognized or deprecated identifier. Use only registered worldview and deficiency class identifiers." |
| `COHERENCE` | "The plan's corrects field did not match the identified deficiency class. Please align the corrects value with the deficiency being addressed." |
| `COMMITMENT` | "The plan did not correctly assert preservation of all active commitments. Each active commitment must have a COMMITMENT_INTACT assertion with its identifier in the replaces field." |
| `STRUCTURE` | "A plan step lacked required normative grounding or contained an assertion that cannot be verified. Guards must have at least one worldview in their justification." |
| `SECURITY` | *(Not sent to LLM — triggers immediate Hard Safety Escalation. Logged internally.)* |
| `INTERNAL_ERROR` | *(Not sent to LLM — triggers immediate Hard Safety Escalation. Logged internally.)* |

**What feedback includes:**
- The `SanitizedCategoryToken` name
- The verbatim feedback message
- The retry attempt number (1, 2, or 3)

**What feedback NEVER includes:**
- The specific `ParseError` code
- The specific identifier, field, or step that failed
- The size of the CTS snapshot or number of active commitments
- Any content from the rejected plan

### 12.4 Retry Constraints

**Rule RETRY-1.** Maximum 3 retry attempts. On the third rejection, a Hard Safety Escalation is triggered regardless of error category.

**Rule RETRY-2.** Each retry uses the **same CTS snapshot** as the original attempt (the snapshot is not refreshed between retries). This ensures that all attempts within a retry cycle see consistent commitment state.

**Rule RETRY-3.** If the CTS snapshot TTL expires during the retry cycle — including after TTL extension attempts have been exhausted — the entire SMREA generation process aborts. The abort is logged and a new SMREA generation cycle may be initiated (acquiring a fresh snapshot). TTL extension is governed by §8.4 and RETRY-6.

**Rule RETRY-4.** The Retry Protocol MUST log: the attempt number, the error category, the `cts_snapshot_token`, and whether a TTL extension was granted for each attempt. It MUST NOT log the specific error code or any plan content.

**Rule RETRY-5.** Non-retry-eligible errors (§11.5: `SPL_ERR_FORBIDDEN_COMMITMENT_FORMATION`, `SPL_ERR_ADVERSARIAL_DESCRIPTION`) bypass the Retry Protocol entirely and trigger immediate Hard Safety Escalation.

**Rule RETRY-6.** At the start of each retry attempt (attempts 1, 2, and 3), the Retry Protocol MUST issue a TTL extension request to CTS for the active snapshot before invoking the LLM. The extension request carries the `cts_snapshot_token` and the retry attempt number. CTS grants up to `CTS_SNAPSHOT_TTL_EXTENSION_SECONDS` (default: 120 seconds) per attempt, for a maximum total window of 660 seconds (see §8.4). If CTS denies the extension (snapshot already consumed, already expired, or maximum extensions exceeded), the process aborts per RETRY-3.

### 12.5 Hard Safety Escalation

A Hard Safety Escalation suspends the agent's plan-generation capability for the current SMREA context. The escalation payload (sent to the Safety Subsystem) includes:

- The `smrea_id` of the failed SMREA generation attempt
- The total retry count
- The final error category
- The `cts_snapshot_token` (for audit cross-reference)
- The timestamp

The `retry_attempt_count` (total attempts including the original, i.e., 1 + number of retries) is embedded in the SMREA record (§2.3) regardless of whether the plan was ultimately accepted or escalated. This provides a permanent attestation of generation difficulty that human reviewers can examine via HumanBridge (§16.2).

Human reviewer intervention is required to resume plan-generation capability after a Hard Safety Escalation.

---

## 13. Constrained Decoding Schema

### 13.1 Purpose

The LLM generates SPL plans under grammar constraint, restricting token choices to syntactically valid plan structures. The `grammar_schema_hash` identifies the specific grammar version used during generation.

### 13.2 GBNF Schema

```gbnf
root ::= plan

plan ::= "{" ws "\"scope\"" ws ":" ws scope-value ws ","
             ws "\"corrects\"" ws ":" ws deficiency-class-id ws ","
             ws "\"steps\"" ws ":" ws "[" ws step-list ws "]" ws "}"

scope-value ::= "\"EPISODE\"" | "\"PERSISTENT\"" | "\"PERMANENT\""

deficiency-class-id ::= "\"dc:" deficiency-class-stem "\""
deficiency-class-stem ::= [a-z] ([a-z] | "-")*

step-list ::= plan-step (ws "," ws plan-step)*

plan-step ::= "{" ws "\"type\"" ws ":" ws step-type-value ws ","
                  ws "\"description\"" ws ":" ws quoted-string ws ","
                  ws "\"justification\"" ws ":" ws "[" ws worldview-id-list ws "]"
                  (ws "," ws "\"replaces\"" ws ":" ws (quoted-string | "null"))?
                  (ws "," ws "\"children\"" ws ":" ws "[" ws step-list ws "]")?
              ws "}"

step-type-value ::= "\"ACTION\"" | "\"GUARD\"" | "\"ASSERTION\""

worldview-id-list ::= (worldview-id (ws "," ws worldview-id)*)?

worldview-id ::= "\"wv:" worldview-stem "\""
worldview-stem ::= [a-z] ([a-z] | "-" | [0-9])*

(* No escapes: excludes 0x22 (") and 0x5C (\) from string chars *)
quoted-string ::= "\"" string-char* "\""
string-char   ::= [ -!] | [#-[] | []-~]

ws ::= ([ \t\n\r])*
```

### 13.3 Description Pre-Sanitization

Because the GBNF `string-char` production excludes `"` (0x22) and `\` (0x5C), the LLM's constrained decoding engine will block any token sequence containing these characters within a `quoted-string` context. To reduce constraint pressure on the decoding engine and improve description quality, the IEA → SPL prompt scaffold (OQ-1) MUST include a pre-sanitization instruction.

**Required scaffold instruction (to be included verbatim or equivalent in the prompt scaffold):**

> *"When writing description text for plan steps, use only standard printable ASCII characters. Do not use quotation marks or backslash characters within description text. For emphasis, use parentheses or dashes. For lists within a description, use semicolons. For line breaks, use spaces or em-dashes. The description must be a single continuous string without embedded quotation marks."*

This instruction surfaces the grammar constraint as an explicit generation guideline, reducing the probability that the constrained decoding engine must block high-probability tokens.

### 13.4 Constrained Decoding Configuration

When calling the LLM to generate `revised_reasoning`:

1. Load the GBNF schema corresponding to `H_grammar`.
2. Configure the decoding engine to enforce grammar constraints at every token step.
3. Generate the full plan as a single uninterrupted constrained decoding pass.
4. Return the raw generated text as the plan candidate. Store it with `H_raw` (§10.5).
5. Pass the plan candidate to the SPL parser.

**Rule CD-1.** The inference runtime MUST NOT post-process or modify the grammar-constrained output before passing it to the SPL parser.

**Rule CD-2.** If the SPL parser rejects the grammar-constrained output with a syntactic error, this indicates a bug in the GBNF schema. It is routed to the Retry Protocol (§12) but also flagged as a schema defect for engineering review.

### 13.5 Vocabulary Injection

The RECOMMENDED configuration injects the valid worldview and deficiency class vocabulary directly into the GBNF schema:

```gbnf
worldview-stem ::= "materialist" | "vitalist" | "emotionalist" | "rationalist"
                 | "pragmatist" | "moralist" | "individualist" | "collectivist"
                 | "transcendentalist" | "phenomenologist" | "integrationist"
                 | "eschatologist"

deficiency-class-stem ::= "self-interest-intrusion" | "obligation-conflict"
                         | "worldview-omission" | "proportionality-error"
                         | "scope-overreach" | "commitment-breach"
                         | "stakeholder-omission" | "epistemic-overconfidence"
                         | "means-ends-inversion" | "temporal-bias"
```

This reduces semantic rejection probability at the cost of requiring a schema update when registries are extended. The `grammar_schema_hash` must reflect whichever schema is in use.

### 13.6 Constrained Decoding Pressure: Implementer Guidance

The no-escape grammar (§4.2) excludes `"` (0x22) and `\` (0x5C) from string fields. LLMs with strong JSON-training priors assign significant probability mass to `\"` within string contexts and to `\n` for line breaks. The constrained decoding engine will block these tokens, which has two consequences:

**Token-block failure rate.** Each blocked token forces the decoding engine to renormalize over the remaining legal vocabulary. For the `description` field in particular — which is open-ended natural language — this renormalization may occur frequently. Implementation experience with comparable constrained grammars suggests that token-block events for the `\"` token occur on the order of 1–5 times per description in an unprimed model, dropping to near-zero with effective prompt pre-sanitization (§13.3). Implementers should monitor token-block frequency as an operational metric; sustained high rates (> 10 blocks per description) indicate the pre-sanitization instruction is not being followed by the LLM.

**Generation quality degradation.** Repeated token-blocking can cause the decoding engine to route through lower-probability token paths, degrading description coherence. Mitigation strategies, in order of preference:

1. **Vocabulary-injected schema (§13.5).** For identifier fields (`worldview-stem`, `deficiency-class-stem`), vocabulary injection eliminates all identifier-related token-block events entirely. This is the highest-value single intervention.
2. **Pre-sanitization instruction (§13.3).** The scaffold instruction reduces `\"` and `\` probability in description contexts before constrained decoding begins.
3. **Temperature tuning.** Lower sampling temperature during SPL generation reduces the variance of the output distribution, making token-blocking less likely to produce incoherent continuations.
4. **Retry tolerance.** The Semantic Retry Protocol (§12) provides up to 3 attempts. A generation that produces low-quality descriptions but syntactically valid structure will be accepted; human reviewers via HumanBridge provide the quality floor.

**What is NOT an acceptable mitigation:** The micro-encoding placeholder approach (embedding `<<QUOTE>>` or similar tokens in the grammar to represent blocked characters) is explicitly rejected. It introduces a second encoding layer that must be decoded before the parser sees the text, requiring the TCB parser to support a non-trivial escaping scheme. This directly contradicts P2 (bounded memory) and P8 (non-Turing-complete), and reduces the security guarantees of §15.

---

## 14. Size and Depth Limits

```
SPL_MAX_STEPS_PER_NODE     = 10
SPL_MAX_TREE_DEPTH         = 5
SPL_MAX_TOTAL_NODES        = 50
SPL_MAX_INPUT_BYTES        = 16,384
SPL_MAX_CANONICAL_BYTES    = 8,192
SPL_MAX_DESCRIPTION_CHARS  = 500
SPL_MAX_DESC_TOTAL_BYTES   = 12,000   (* aggregate across all nodes *)
SPL_MAX_JUSTIFICATION_REFS = 5
SPL_PARSER_ARENA_BYTES     = 65,536
```

All limits are compile-time constants enforced by the parser. Violations produce `SPL_ERR_SIZE_EXCEEDED` or `SPL_ERR_DEPTH_EXCEEDED`.

---

## 15. Security Properties

### 15.1 Formal Security Claims

**SC-1 — No Code Execution.** No syntactically valid SPL plan causes any code to be executed within the parser or the TCB. The parser is a pure validator and canonicalizer.

**SC-2 — No Unbounded Memory.** No syntactically valid SPL plan can cause the parser to exceed `SPL_PARSER_ARENA_BYTES`.

**SC-3 — No Partial Plans.** No invalid plan can reach MDRE, HumanBridge, or the Commitment Ledger. Reject-by-default is absolute.

**SC-4 — No Identifier Injection.** SPL identifiers are validated against static registries at semantic check time. Unresolvable identifiers are rejected.

**SC-5 — No Normative Drift.** A plan's `corrects` field must match the SMREA's `deficiency_class` (SEM-1). The agent cannot substitute a convenient deficiency for the diagnosed one.

**SC-6 — No Commitment Laundering.** The `COMMITMENT_INTACT` assertion requirement (SEM-2, SEM-3) validates against the CTS snapshot, not live state. The snapshot is one-time-use and its hash is embedded in the SMREA. Commitment changes between snapshot acquisition and plan execution cannot retroactively invalidate the assertions. The `FORBIDDEN_COMMITMENT_FORMATION` check (SEM-4) screens for new commitments in ACTION descriptions. Together, these prevent covert modification of the agent's commitment landscape through SPL.

**SC-7 — No Replay.** SPL plans are embedded in SMREA records with nonce and timestamp. The Commitment Ledger rejects duplicate SMREAs. CTS snapshot tokens are one-time-use.

**SC-8 — Grammar-Constrained Generation.** The `grammar_schema_hash` creates a verifiable link between generation grammar and validation grammar.

**SC-9 — Feedback Isolation.** The Semantic Retry Protocol (§12) provides only sanitized, category-level feedback. Specific error codes, failing identifiers, and failing field names are never surfaced to the LLM. Non-retry-eligible errors bypass the Retry Protocol entirely.

**SC-10 — TOCTOU Elimination.** The CTS Snapshot Isolation Protocol (§8.4) eliminates the race condition between plan generation and plan validation. The parser validates against the locked snapshot, not the live ledger. The snapshot token is one-time-use, preventing snapshot reuse across multiple SMREAs.

### 15.2 Known Limitations

**L-1 — Semantic Adversariality of Descriptions.** The grammar prevents syntactic attacks. It does not prevent descriptions that are semantically misleading to human reviewers while technically valid. Mitigation: HumanBridge rendering foregrounds worldview grounds and deficiency class; OQ-2 resolved to Option B (HumanBridge flagging).

**L-2 — Vocabulary Exhaustion.** A sophisticated attacker influencing LLM pre-training might cause it to generate low-information descriptions that exhaust the character budget. Mitigation: 50-node and 500-char limits cap total volume; human reviewers see the full plan.

**L-3 — Registry Staleness.** If IEA registry or CTS snapshot is stale, novel identifiers may be incorrectly handled. Mitigation: registry version recorded in SMREA; TCB measures registry contents (OQ-4).

**L-4 — Retry Protocol Outside TCB.** The Semantic Retry Protocol (§12) operates outside the TCB. A compromised Safety Subsystem orchestration layer could in principle manipulate retry counts or feedback messages. Mitigation: the Safety Subsystem is itself a trusted component, and retry protocol actions are audited. The TCB's signature on the final plan is unaffected by Retry Protocol behavior.

---

## 16. HumanBridge Rendering Contract

### 16.1 Overview

HumanBridge renders SPL plans as structured data — never as raw JSON, never as free text. This is the primary mitigation for L-1 (semantic adversariality of descriptions).

### 16.2 Required Display Elements

1. **Plan scope badge.** Visually distinct: `EPISODE`, `PERSISTENT`, or `PERMANENT`.
2. **Deficiency class label.** Human-readable expansion of `Plan.corrects`.
3. **Plan summary.** Auto-generated: "[count] corrective steps ([count] actions, [count] guards, [count] assertions) addressing [deficiency class label]."
4. **Retry history badge.** If the plan was accepted on retry N > 1, HumanBridge MUST display "Accepted on attempt N of 3." This provides transparency about generation difficulty.
5. **Step tree.** Rendered tree view per §16.4.

### 16.3 PERMANENT Scope Warning

Plans with `scope: PERMANENT` MUST trigger a `PERMANENT_SCOPE_WARNING` modal requiring explicit reviewer confirmation before the tree view is displayed. PERMANENT scope plans MUST NOT be auto-approved. The reviewer's choice is logged in the Safety Subsystem audit log. Confirmation releases the `authorization_token` to MDRE (§9.2).

### 16.4 Step Rendering Rules

Each `PlanStep` is rendered as a card:

| Field | Display | Source |
|---|---|---|
| Step type | Icon + label (`⚡ ACTION`, `🚫 GUARD`, `✓ ASSERTION`) | `type` |
| Description | Plain text, max 500 chars | `description` |
| Grounds | Worldview chips, one per WorldviewId; clicking a chip shows the worldview's full IEA description | `justification` |
| Replaces | "Replaces: [value]" or hidden if null | `replaces` |
| Children | Nested cards, indented | `children` |

`GUARD` nodes MUST use a visually cautionary indicator (e.g., red border, 🚫 icon) to prevent negative constraints from being misread as permissions.

**Description rendering contract — no transformational interpretation.** HumanBridge MUST render description content as raw UTF-8 text without any transformational processing. Specifically, HumanBridge MUST NOT:

- URL-decode `%XX` sequences (e.g., `%5C` must render as the three characters `%`, `5`, `C` — not as `\`)
- HTML-entity-decode `&amp;`, `&#xNN;`, or any other entity forms
- Markdown-render `*bold*`, `[link](url)`, or any other markup
- Interpret ANSI escape codes or terminal control sequences
- Apply any font substitution or glyph normalization

This rule closes the mitigation gap for percent-encoded sequences (e.g., `%5C`, `%22`) that are grammatically valid but could represent covert encodings if a downstream renderer interpreted them. The TCB ensures such sequences cannot become structural attacks (MDRE-6); HumanBridge ensures they cannot become rendering attacks.

**HumanBridge Description Screening (OQ-2 resolution):** HumanBridge SHOULD implement a lightweight heuristic flagging system for description content. Descriptions flagged by this system are displayed with a `⚠ DESCRIPTION FLAGGED` banner, prompting additional reviewer scrutiny. Flagged descriptions do NOT prevent plan approval — they are advisory only. This system operates outside the TCB and does not affect parser behavior or signing. Flagging heuristics are maintained separately from the TCB-measured adversarial pattern set (§9.4).

### 16.5 Full Plan View

HumanBridge MUST offer an optional expandable view displaying:
- The canonical CBOR encoding as a hex dump
- Its BLAKE3 domain-separated hash (`H_plan`)
- The raw LLM output hash (`H_raw`)
- The CTS snapshot hash

This allows technically sophisticated reviewers to verify the plan they are viewing matches what was signed and to compare canonical and raw forms.

### 16.6 Storage Encoding Contract

MDRE's audit log and HumanBridge's persistent plan store MUST use the following encoding contract for description fields:

- **Encoding:** UTF-8. Since SPL descriptions are restricted to printable ASCII (a strict subset of UTF-8), UTF-8 encoding is trivially satisfied and lossless.
- **Maximum storage bytes per description:** 500 bytes (matching `SPL_MAX_DESCRIPTION_CHARS`). Since SPL descriptions contain only single-byte ASCII characters, character count equals byte count.
- **Maximum aggregate storage bytes per plan:** 12,000 bytes (matching `SPL_MAX_DESC_TOTAL_BYTES`).
- **Null handling:** If a node has no `description` (structurally impossible given the grammar, but defensively: should never occur in a validated plan), the storage layer MUST log `[NO_DESCRIPTION]` rather than null or empty string.
- **Encoding error handling:** Per MDRE-8, if a description cannot be stored due to an encoding constraint (e.g., a downstream log system that does not support full ASCII range), MDRE MUST log `[DESCRIPTION_ENCODING_ERROR]` and escalate. HumanBridge MUST display `[DESCRIPTION UNAVAILABLE — ENCODING ERROR]` in the step card and flag the plan for mandatory human reviewer attention.

---

## 17. Test Suite Requirements

### 17.1 Validity and Invalidity Tests

**Valid Plans (parser must accept):**

| Test ID | Description |
|---|---|
| V-01 | Minimal valid plan: EPISODE scope, one ACTION, one ASSERTION |
| V-02 | Plan with all three step types at root level |
| V-03 | Plan with nested children to depth 5 |
| V-04 | Plan with exactly 10 steps at root level (width limit) |
| V-05 | Plan with exactly 50 total nodes (node count limit) |
| V-06 | Plan with exactly 5 worldview refs per justification |
| V-07 | PERSISTENT scope plan |
| V-08 | PERMANENT scope plan |
| V-09 | Plan with multiple COMMITMENT_INTACT assertions |
| V-10 | Plan with ALL_COMMITMENTS_INTACT parent assertion |
| V-11 | Plan with empty justification on ACTION node (permitted) |
| V-12 | Plan with null replaces field (explicit null) |
| V-13 | Plan with absent replaces field (key omitted) |
| V-14 | Plan at exactly SPL_MAX_CANONICAL_BYTES |
| V-15 | Plan validated against CTS snapshot with 0 active commitments (no COMMITMENT_INTACT required) |
| V-16 | Plan with aggregate description bytes exactly at SPL_MAX_DESC_TOTAL_BYTES (12,000 bytes) |
| V-17 | COMMITMENT_INTACT assertion with non-null replaces pointing to valid CTS snapshot ID |

**Invalid Plans (parser must reject):**

| Test ID | Error Expected | Description |
|---|---|---|
| I-01 | `SPL_ERR_SYNTAX` | Extra field at root level |
| I-02 | `SPL_ERR_SYNTAX` | Missing `corrects` field |
| I-03 | `SPL_ERR_SYNTAX` | Missing `steps` field |
| I-04 | `SPL_ERR_SYNTAX` | Empty `steps` array |
| I-05 | `SPL_ERR_SYNTAX` | Invalid scope value |
| I-06 | `SPL_ERR_SYNTAX` | Control character in description |
| I-07 | `SPL_ERR_SYNTAX` | Non-ASCII character in description |
| I-08 | `SPL_ERR_SYNTAX` | Backslash in description |
| I-09 | `SPL_ERR_SYNTAX` | Quote character in description |
| I-10 | `SPL_ERR_SIZE_EXCEEDED` | 11 steps at root level |
| I-11 | `SPL_ERR_DEPTH_EXCEEDED` | Steps nested to depth 6 |
| I-12 | `SPL_ERR_SIZE_EXCEEDED` | 51 total nodes |
| I-13 | `SPL_ERR_UNKNOWN_WORLDVIEW_ID` | Unknown `wv:*` identifier |
| I-14 | `SPL_ERR_UNKNOWN_DEFICIENCY_CLASS` | Unknown `dc:*` identifier |
| I-15 | `SPL_ERR_CORRECTS_MISMATCH` | `corrects` does not match SMREA deficiency class |
| I-16 | `SPL_ERR_MISSING_COMMITMENT_ASSERTION` | No COMMITMENT_INTACT assertion; CTS snapshot has active commitments |
| I-17 | `SPL_ERR_UNCOVERED_COMMITMENT` | Active commitment in snapshot not covered by assertion |
| I-18 | `SPL_ERR_FORBIDDEN_COMMITMENT_FORMATION` | ACTION with commitment formation language |
| I-19 | `SPL_ERR_UNGROUNDED_GUARD` | GUARD with empty justification |
| I-20 | `SPL_ERR_ADVERSARIAL_DESCRIPTION` | Description beginning with `override:` (lowercased prefix match) |
| I-21 | `SPL_ERR_ADVERSARIAL_DESCRIPTION` | Description beginning with `SYSTEM:` (lowercased prefix match after leading whitespace strip) |
| I-22 | `SPL_ERR_ADVERSARIAL_DESCRIPTION` | Description beginning with leading spaces then `system:` (leading whitespace stripped before prefix match) |
| I-23 | `SPL_ERR_SIZE_EXCEEDED` | Description exceeding 500 chars |
| I-24 | `SPL_ERR_SIZE_EXCEEDED` | Input exceeding SPL_MAX_INPUT_BYTES |
| I-25 | `SPL_ERR_SIZE_EXCEEDED` | Aggregate description bytes exceed SPL_MAX_DESC_TOTAL_BYTES (12,000) across 50 nodes |
| I-26 | `SPL_ERR_UNCOVERED_COMMITMENT` | COMMITMENT_INTACT assertion with `replaces: null` when CTS snapshot has active commitments |
| I-27 | `SPL_ERR_SYNTAX` | ALL_COMMITMENTS_INTACT parent with `replaces` pointing to a CTS ID (should be null for grouping node) — rejected as semantically incoherent |

**SEM-15 False-Positive Boundary Tests (must NOT trigger SPL_ERR_ADVERSARIAL_DESCRIPTION):**

| Test ID | Description |
|---|---|
| FP-01 | Description: `to verify the subsystem: result` — contains `system:` internally but does not begin with it; must be accepted |
| FP-02 | Description: `override the agent behavior` — does not begin with `override:` (no colon immediately following); must be accepted |
| FP-03 | Description: `run analysis on stakeholder impacts` — does not begin with `run:` (no immediate colon); must be accepted |
| FP-04 | Description with internal spaces before a pattern word: `confirm system: connectivity is preserved` — internal occurrence, not a leading prefix; must be accepted |

**CTS Snapshot TOCTOU Tests:**

| Test ID | Description |
|---|---|
| T-01 | Plan generated against snapshot S1; validated against snapshot S1 → Accept |
| T-02 | Plan generated against snapshot S1; commitment revoked between generation and validation; S1 snapshot still used → Accept (snapshot is locked) |
| T-03 | Plan generated against snapshot S1; commitment added between generation and validation; S1 snapshot still used → Reject only if new commitment is in S1 and not covered |
| T-04 | Attempt to reuse snapshot S1 for a second SMREA → Reject with snapshot reuse error |
| T-05 | Plan submitted after initial `CTS_SNAPSHOT_TTL_SECONDS` but within extended TTL window (extension granted per RETRY-6) → Accept |
| T-06 | Plan submitted after all TTL extensions exhausted → Abort with snapshot expiry |
| T-07 | TTL extension request with retry attempt number > `CTS_SNAPSHOT_TTL_MAX_RETRIES` → CTS denies extension → Abort |
| T-08 | Accepted plan on retry attempt 2: `retry_attempt_count = 3` attested in SMREA record |
| T-09 | Accepted plan on first attempt: `retry_attempt_count = 1` attested in SMREA record |

### 17.2 Fuzz Harness (see §11.6)

### 17.3 Constrained Decoding Round-Trip Tests

| Test ID | Description |
|---|---|
| CD-01 | Generate plan via constrained decoding → parse → canonicalize → re-parse → canonical byte equality |
| CD-02 | All V-* valid plans pass through GBNF schema without grammar violations |
| CD-03 | GBNF schema accurately rejects syntactic structures in I-01 through I-09 |
| CD-04 | Plan with explicit `"replaces": null` and plan without `replaces` key produce identical canonical CBOR |
| CD-05 | `H_raw` of raw LLM output ≠ `H_plan` of canonical CBOR for plans where raw form differs from canonical (e.g., explicit null, field ordering) |

### 17.4 Semantic Retry Protocol Tests

| Test ID | Description |
|---|---|
| R-01 | First attempt fails with SYNTAX_ERROR; second attempt succeeds → plan accepted |
| R-02 | Three consecutive failures with retry-eligible errors → Hard Safety Escalation triggered |
| R-03 | First attempt fails with FORBIDDEN_COMMITMENT_FORMATION → immediate escalation, no retry |
| R-04 | First attempt fails with ADVERSARIAL_DESCRIPTION → immediate escalation, no retry |
| R-05 | CTS snapshot expires during retry cycle → Abort, new SMREA generation cycle required |
| R-06 | Feedback category for CORRECTS_MISMATCH is COHERENCE_ERROR (not the specific code) |
| R-07 | Retry attempt 1 triggers TTL extension request; CTS grants 120s extension; generation proceeds within extended window |
| R-08 | Retry attempt 3 triggers third TTL extension; subsequent snapshot use for a different SMREA is denied (one-time-use unaffected) |

### 17.5 Canonicalization Tests

| Test ID | Description |
|---|---|
| CBOR-01 | Two plans with identical AST content but different raw input field ordering produce identical canonical CBOR |
| CBOR-02 | Two plans differing in one field produce different canonical CBOR |
| CBOR-03 | Explicit `"replaces": null` and absent `replaces` key produce identical canonical CBOR |
| CBOR-04 | Domain-separated plan hash matches expected test vector |
| CBOR-05 | `H_raw` is distinct from `H_plan` for non-canonical raw inputs |
| CBOR-06 | Domain-separated grammar hash matches expected test vector |
| CBOR-07 | Description containing internal spaces is canonicalized byte-for-byte without space collapsing |
| CBOR-08 | Description containing `%5C` is canonicalized as literal three-char sequence, not as backslash |
| CBOR-09 | SEM-15 normalization and canonicalization use same source string — verified by checking that a description passing SEM-15 produces matching bytes in canonical CBOR |

---

## 18. Open Questions

### OQ-1 — IEA → SPL Prompt Scaffold (Active)

**Status:** Active. The normative bridge in §7 defines the mapping from IEA output to SPL fields. The prompt scaffold — the structured format in which IEA output is presented to the LLM as read-only normative context — is a separate artifact. It must convey enough normative context for the LLM to produce well-grounded `justification` lists, while being structured to minimize adversarial surface.

**Proposed resolution:** A dedicated IEA → SPL Prompt Scaffold Specification, incorporating the description pre-sanitization instruction (§13.3), read-only IEA context format, and an explicit constraint that scaffold content does not appear in the grammar-constrained output.

### OQ-2 — Description Vocabulary Control (Resolved: Option B)

**Status:** Resolved in v1.1. Option A (closed vocabulary in GBNF) was rejected because it would strip the nuance required for human reviewers to evaluate complex moral corrections. The correct architectural posture is to keep complex security enforcement out of the TCB where possible. Resolution: Option B (HumanBridge heuristic flagging) is adopted (§16.4). The TCB-internal adversarial pattern check (§9.4, SEM-15) handles the narrow set of high-confidence adversarial markers; HumanBridge handles the broader, advisory human-review layer.

### OQ-3 — Multi-Agent SPL Plans (Deferred)

**Status:** Deferred. The current specification is strictly single-agent. Cross-agent coordination in the federated FNSR ecosystem requires extensions to the CTS bridge and SMREA structure that are out of scope for v1.0/v1.1.

### OQ-4 — IEA Registry Versioning and PCR Measurement (Active)

**Status:** Active. The IEA worldview and deficiency class registries are used as static inputs during semantic validation. Their contents must be part of the PCR measurement chain. The mechanism — separate PCR extension vs. inclusion in the SafetyCore binary — requires coordination with SPCN v2.4 planning.

### OQ-5 — Retry Protocol Security Audit (Resolved in v1.2)

**Status:** Resolved. The three sub-questions from v1.1 are addressed as follows:

**(a) Can the Retry Protocol be used to probe registry contents?** No, for the following reason: the feedback categories deliberately omit which specific identifier failed. The only information a retry provides is a category name (e.g., `IDENTIFIER_ERROR`) with no indication of which of the twelve worldview identifiers or ten deficiency class identifiers was unrecognized. With a maximum of three attempts total, an adversary could test at most three hypotheses per SMREA generation cycle. The worldview registry contains 12 entries; the deficiency class registry contains 10. Exhaustive probing would require on the order of 22 isolated SMREA cycles — each triggering a Hard Safety Escalation after 3 failures, each requiring human reviewer intervention to resume. The registry is therefore not practically enumerable via the Retry Protocol. The 3-attempt limit is the decisive control.

**(b) Does the one-time-use CTS snapshot token fully prevent snapshot-reuse attacks in the retry context?** Yes. TTL extensions (RETRY-6, §8.4) extend the validity window of the existing snapshot; they do not issue a new snapshot or reset the one-time-use flag. CTS tracks consumed snapshots independently of TTL state. A snapshot marked as consumed cannot be reused for a second SMREA regardless of whether its TTL window is still open.

**(c) Should retry attempt count be attested in the SMREA record?** Yes, and this is adopted in v1.2. The `retry_attempt_count` field is now a required SMREA field (§2.3) and is embedded in the finalized record regardless of success or escalation. This provides permanent, non-repudiable evidence of generation difficulty. Human reviewers can observe via HumanBridge (§16.2) whether a plan required multiple attempts, which is a relevant signal for review depth.

---

## 19. Version History

| Version | Date | Summary |
|---|---|---|
| 1.0 | 2026-03-11 | Initial specification. Formal grammar, type system, semantic rules, IEA/CTS/MDRE bridges, canonicalization, parser requirements, constrained decoding schema, size limits, security properties, HumanBridge rendering contract, test suite. |
| 1.1 | 2026-03-12 | CTS Snapshot Isolation Protocol (§8.4) resolving TOCTOU race condition. Semantic Retry Protocol (§12) resolving blind LLM deadlock. MDRE-7 blacklist removed; adversarial pattern check moved inside TCB as SEM-15 (§9.4). Canonicalization clarified as AST-derived; raw LLM output preserved separately (§10.2, §10.5). No-escape grammar rationale strengthened; pre-sanitization responsibility clarified (§4.2, §13.3). OQ-2 resolved to Option B. OQ-5 (retry protocol security audit) added. New test cases: V-15, I-08/I-09/T-01–T-05, R-01–R-06, CD-04/CD-05, CBOR-05/CBOR-06. |
| 1.3 | 2026-03-12 | **FINAL.** Canonical `ParseError → SanitizedCategoryToken` mapping table with exhaustive, stable token names and verbatim feedback messages (§11.5, §12.3). Arena cost estimator formula added with reference constants; `SPL_MAX_DESC_TOTAL_BYTES = 12,000` enforces aggregate description quota (§11.3, §14). SEM-15 pattern governance requirements added: per-pattern ID, rationale, semantic category tag, true-positive test, near-miss false-positive tests, date/author, TCB re-measure gate; `%5C`/`%22` sequences addressed via HumanBridge no-decode rendering rule rather than SEM-15 (§9.4). Micro-encoding placeholder (`<<QUOTE>>`) explicitly rejected. Canonicalization string preservation rule made explicit: descriptions encoded byte-for-byte without normalization; SEM-15/canonicalization alignment confirmed (§10.7). `replaces: null` semantics clarified: null is structural placeholder; leaf COMMITMENT_INTACT MUST have non-null replaces (§8.1). HumanBridge no-decode rendering contract and storage encoding contract added (§16.4, §16.6). Fuzz CI split into two tiers: local/PR 1M, nightly 10M (§11.6). Constrained decoding pressure guidance added; micro-encoding rejected with architectural rationale (§13.6). New test cases: V-16, V-17, I-25–I-27, CBOR-07–CBOR-09. |

---

*SPL Specification v1.3 — FINAL — FNSR Ecosystem | Ontology of Freedom Initiative*  
*Authored under the Ontology of Freedom Initiative. All architectural decisions traceable to SPCN v2.3.1, IEA v2.1, and FNSR Governance Specification v2.0.*
