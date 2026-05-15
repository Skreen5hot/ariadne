# Fandaws Type Agent
## Functional Specification — Version 2.3

| Field | Value |
|---|---|
| Date | March 2026 |
| Status | HARDENED DRAFT (Pre-Final) |
| Supersedes | v2.2 (March 2026) |
| Component Role | Tier 1 Upstream Data Provider — Dual-Mode Intelligence |
| Target System | Fandaws v3.4+ |
| Edge-Canonical | SGW Module: Full. SER Module: Partial (see §2.3) |

---

## Version History

| Version | Date | Change Type | Summary |
|---|---|---|---|
| 2.3 | March 2026 | Portfolio Coherence Review — Six Resolutions | KL-007 quantified with correction loss model (§20). FTA-CAP-009 bootstrap acceptance criteria added (§15.4). Column key format unified to structured double-colon convention throughout (§4.1, §5.4, §7.2, §21.1). FNSR taint propagation added to all outputs (§6.1, §17.1, §17.4). Pattern registry weight floor with zero-weight pruning (§21.4). `pendingCrossCheck` flag on bulk-trust assertions (§17.1, §17.4). FTA-CAP-013 added. KL-008 added. |
| 2.2 | March 2026 | KL-005 Resolution — Mapping Correction Protocol | OPA cross-check algorithm specified (§21). MappingCorrection output schema defined (§21.3). TypeAgentStateAdapter extended with mapping audit methods (§7.1). Feedback loop §18 updated to include correction pathway. KL-005 resolved. KL-007 added (session eviction edge case). FTA-CAP-011 and FTA-CAP-012 added. |
| 2.1 | March 2026 | SME Review — Publication Hardening | Semantic Proximity tiebreaker. Entropy unit guard. Bulk Trust Policy. FTA-CAP-009 elevated to P0. Ambiguity threshold configurable. Reading guide. |
| 2.0 | March 2026 | Major Version — SER Module Added | Schema Ensemble Recognition (SER) capability module. ObservedTable schema. Fingerprinting. Entity Pattern Registry. Ensemble Matching. EntityTypeAssertion output. Feedback loop. FTA-CAP-007–010. |
| 1.2 | March 2026 | SME Review — Approved | Zero-entropy guard. Categorical scope. O(N²) sampling. Token sourcing. @context note. |
| 1.1 | March 2026 | Hardened Draft | D1–D3 resolved. G1–G6 closed. FTA-CAP catalogue established. |
| 1.0 | March 2026 | Initial Draft | SGW concept. PS formula. Fandaws integration pattern. |

---

## SME Review — v2.1 Advisories Addressed

| ID | Advisory | Resolved In | Resolution |
|---|---|---|---|
| B1 | Column Mapping Confidence (KL-005): structural match is not semantic match; two "Status" columns may map to wrong concepts | §16.1 | Semantic Proximity tiebreaker added. When column names are present and not opaque, the mapping algorithm applies a name-similarity bonus as a secondary scoring signal to disambiguate structurally identical columns. |
| B2 | Entropy unit misalignment between SAS and Type Agent policy silently corrupts all NMI-hat scores | §4.1, §4.2, §13 | Normative entropy unit validation guard added at ObservedAttribute ingestion boundary and ObservedTable boundary. Mismatch between declared `entropyUnit` in policy and observed entropy magnitude triggers a hard rejection with diagnostic output. |
| B3 | Human-in-the-Loop fatigue during large migrations — agent flooded with ConversationPrompts for routine recognitions | §4.2, §17.2 | `bulkTrustPolicy` field added to TypeAgentPolicy. Enables dataset-scoped automatic approval for SER recognitions above a configurable score threshold, eliminating prompt flooding during planned migrations. |
| B4 | FTA-CAP-009 (Bootstrap) is the critical path item blocking day-one SER operation; not sufficiently elevated | §9 | FTA-CAP-009 elevated to **P0 Critical Path** in the capabilities table. All other SER capabilities (FTA-CAP-007, 008, 010) marked as blocked until bootstrap is operational. Implementation ordering guidance added. |
| B5 | Ambiguity threshold (15%) may be too coarse for mixed-entity tables in large migrations | §16.2 | Disambiguation signal set documented more precisely. `ambiguityThreshold` made a configurable OPAPolicy parameter (default: 0.15) rather than a hard-coded constant. |

---

## SME Review — v2.2 Advisory Addressed

| ID | Advisory | Resolved In | Resolution |
|---|---|---|---|
| C1 | KL-005 (Mapping vs. Verification) — structural column mapping is not semantic verification; the OPA's placement results should cross-check and correct SER mappings post-placement | §21, §7.1, §18.4 | Full Mapping Correction Protocol specified as §21. After every OPA concept placement, Step 7 of the OPA pipeline performs a lookup against stored SER recognition column mappings. When a nominating column key matches a stored mapping entry, the OPA compares its placed Universal IRI against the mapping's `mapsTo` IRI. Agreement emits a `MappingConfirmation`. Disagreement emits a `MappingCorrection` that updates the TypeAgentStateAdapter and triggers a `fandaws:GraphMutation` flagging the original EntityTypeAssertion for re-evaluation. KL-005 resolved; KL-007 added for the session-eviction residual case. Two new FTA-CAP items added (OPA-011: MappingCorrection schema, OPA-012: cross-check interface). |

---

## Portfolio Coherence Review — v2.3 Advisories Addressed

| ID | Advisory | Resolved In | Resolution |
|---|---|---|---|
| D1 | KL-007 (Session Eviction) unquantified — the spec acknowledges correction loss from session-scoped adapters but provides no estimate of magnitude, making it impossible to assess deployment risk | §20 (KL-007) | Correction loss model added with three deployment scenarios (4-hour session / 24-hour / persistent). Estimated 85–95% correction loss in short-session deployments during early operation. Persistent adapter elevated from future enhancement to production deployment requirement. |
| D2 | FTA-CAP-009 (Bootstrap) underspecified — "request TagTeam parse" hand-waves over the fact that CCO definitions are semi-formal and may not produce usable TagTeam output | §15.4 | Bootstrap acceptance criteria added. Minimum viable pattern requires ≥1 required signal and ≥2 column patterns. TagTeam parse fallback specified for definitions that fail NL parsing: structured extraction from OWL axioms via BFO branch mapping. |
| D3 | Column key format inconsistency — SGW uses single-colon `datasetId:columnName`, SER uses double-colon `datasetId::tableId::columnName`. Single-colon format is ambiguous when column names contain colons | §4.1, §5.4, §7.2, §21.1 | Unified on structured double-colon convention `datasetId::tableId::columnName` throughout. SGW member keys updated from `datasetId:columnName` to `datasetId::tableId::columnName`. Legacy single-colon format deprecated with migration note. |
| D4 | No FNSR taint propagation — Type Agent outputs carry no `fnsr:taintLevel`, violating the ecosystem-wide taint contract established in the TagTeam-Fandaws Integration Guidance | §6.1, §17.1, §17.4 | `fnsr:taintLevel` added to all Type Agent outputs. SGW GraphMutations carry `L3` (speculative/inferred). SER EntityTypeAssertions carry `L3` by default, promotable to `L2` upon OPA cross-check confirmation. Bulk-trust assertions carry `L3` with `pendingCrossCheck` flag. |
| D5 | Pattern registry weight floor behavior unspecified — §21.4 decrements weights but doesn't clamp to 0.0 or define what happens at zero weight | §21.4 | Explicit `max(0.0, weight - decrement)` clamp added to algorithm. Zero-weight column pattern entries are flagged `prunable: true` and excluded from match scoring. Pruning runs at pattern registry compaction time (configurable, default: daily). |
| D6 | Bulk trust + correction timing window — bulk-trust commits are consumed by downstream services before the OPA cross-check can verify them, with no mechanism for consumers to distinguish verified from unverified assertions | §17.1, §17.4, §19 | `fandaws-ta:pendingCrossCheck: true` flag added to all bulk-trust-approved EntityTypeAssertions. Flag is cleared to `false` when the OPA cross-check confirms or corrects all column mappings. Downstream consumers can filter on this flag. FTA-CAP-013 added for the flag schema. |

---

## 0. Reading Guide

This specification is organized for multiple audiences. Read the sections most relevant to your role.

| Role | Recommended Sections |
|---|---|
| **Solution Architect** | §1, §2, §3, §9, §18, §21.4 (correction cascade) |
| **Backend Developer — SGW** | §4, §5, §6, §7, §10 |
| **Backend Developer — SER** | §12, §13, §14, §15, §16, §17, §19 |
| **Backend Developer — Mapping Correction** | §21 (complete), §7.1 (adapter methods), §18.4 (feedback loop update) |
| **Fandaws Platform Engineer** | §9 (FTA-CAP-007–012), §15.3, §17.1, §21.3 (MappingCorrection schema) |
| **OPA Specification Author** | §3.3, §15.3, §18.2, §21 (complete) |
| **QA / Test Engineer** | §10, §19, §21.5, §11, §20 |

> **Implementation Ordering (v2.x capabilities):** (1) FTA-CAP-009 Bootstrap [P0 — blocks all SER], (2) FTA-CAP-007 Pattern Registry service, (3) FTA-CAP-008 EntityTypeAssertion schema, (4) FTA-CAP-010 OPA PatternContribution, (5) FTA-CAP-011 MappingCorrection schema, (6) FTA-CAP-012 OPA cross-check interface, (7) FTA-CAP-013 `pendingCrossCheck` flag schema. The SGW pipeline (Part A) is fully operational independent of all of these.

---

## 1. Executive Summary

The Fandaws Type Agent v2.0 is a dual-mode semantic intelligence service. It operates two distinct but complementary pipelines — the Semantic Gravity Well (SGW) pipeline carried forward from v1.2, and the new Schema Ensemble Recognition (SER) pipeline introduced in this version.

**The SGW pipeline** (Part A, §§3–11) is a bottom-up, patient accumulation engine. It watches individual column attributes arrive from multiple independent datasets over time and asks: *has this attribute shape converged across enough independent sources to nominate a concept?* It builds knowledge from repeated observation. It requires no prior knowledge in Fandaws to function. It produces concept nominations for the OPA to process.

**The SER pipeline** (Part B, §§12–19) is a top-down, immediate recognition engine. When a new table arrives, it bundles all column profiles together into a structural ensemble, matches that ensemble against entity patterns already known to Fandaws, and asks: *given everything Fandaws already knows, what kind of thing does this table contain rows of?* It applies existing knowledge to new observations. It fires on the first ingestion of a new table without waiting for cross-dataset convergence. It produces entity type assertions — not concept nominations — mapping the unknown table directly to known Fandaws Universals.

The two pipelines are complementary by design. The SGW pipeline grows Fandaws' knowledge from the ground up. The SER pipeline applies that knowledge the moment it is ready. As the OPA places concepts and the SER pattern registry grows, every subsequent table ingestion benefits from all prior placements. The system becomes more capable with each dataset processed.

### 1.1 The Motivating Problem

A database table named `foobar` arrives. It has six columns: something holding values like `engineer`, `manager`, `contractor`; a date field; another date field; something holding values like `engineering`, `finance`, `hr`; an identifier column; and a sparse numeric reference column.

The table name tells us nothing. The column names are opaque. But the structural gestalt is unambiguous to anyone who has seen an HR system: this is an employee table. It has job titles, an employment period, a department, an employee identifier, and manager references.

The SGW pipeline cannot recognize this on first encounter — it has no prior convergence evidence. A human steward could recognize it immediately. The SER pipeline can recognize it on day one, provided Fandaws already has the Employee entity type and its associated column patterns. The question is not whether this recognition is possible — it obviously is — but how to make it deterministic, auditable, and automatic.

### 1.2 Architectural Division of Labor

| Dimension | SGW Pipeline (Part A) | SER Pipeline (Part B) |
|---|---|---|
| Direction | Bottom-up | Top-down |
| Input granularity | Single column (ObservedAttribute) | Entire table (ObservedTable) |
| Fandaws dependency | None — builds knowledge | Required — applies knowledge |
| Fires when | After N datasets confirm convergence | On first table ingestion |
| Output | Concept nomination → OPA | EntityTypeAssertion + column mapping |
| What it proves | This column type recurs reliably across the knowledge landscape | This table contains rows of this known entity type |
| Temporal model | Patient — accumulates evidence over time | Immediate — matches on arrival |

### 1.3 What the Type Agent Does Not Do

Neither pipeline invents ontology classes. Neither pipeline writes to the Fandaws graph directly. The SGW pipeline nominates concepts for the OPA to evaluate and place. The SER pipeline asserts entity types for Fandaws to record. All ontological commitment remains the exclusive domain of the Fandaws Knowledge Engine and OPA.

---

## 2. Architectural Adherence

### 2.1 Edge-Canonical

**SGW Module:** Fully edge-canonical. No databases or external registries. Runs purely in-memory in a browser or Node.js environment.

**SER Module:** Partially edge-canonical. The Fingerprinting algorithm and Ensemble Matching algorithm are pure in-memory computation. The Entity Pattern Registry requires read access to the Fandaws graph snapshot at recognition time. In the reference in-memory implementation, the pattern registry is loaded as a static JSON-LD snapshot at initialization. In production deployments, it is a live query against the Fandaws Knowledge Engine. The SER module **cannot** operate without a pattern registry snapshot, even a minimal bootstrap one.

### 2.2 Determinism

**SGW Module:** Fully deterministic. Given the same ordered sequence of ObservedAttribute inputs and the same TypeAgentPolicy, the SGW pipeline always produces the same SGW topology, Promotion Scores, and output contracts.

**SER Module:** Fully deterministic given the same ObservedTable input and the same pattern registry snapshot. Recognition results are a pure function of the input and the registry state at evaluation time. Results may differ across ingestion sessions if the pattern registry has been updated between sessions — this is correct behavior, not non-determinism.

### 2.3 Separation of Concerns

Both modules share the separation-of-concerns model from v1.x:

- *Computation (Core):* All algorithms — SGW and SER — are pure computation functions.
- *State (Pluggable):* The TypeAgentStateAdapter (§7) stores SGW clusters for Part A and the SER recognition history for Part B.
- *Orchestration (Pluggable):* External adapters trigger both pipelines with their respective input types.
- *Integration (Pluggable):* Both pipelines emit standard Fandaws contracts via the OrchestrationAdapter.

---

## 3. Architectural Position

### 3.1 Both Pipelines in Context

```
PART A — SGW Pipeline (bottom-up concept discovery):

Dataset A → SNP → BIBSS → SAS → upstream adapter → ObservedAttribute(A)  ─┐
Dataset B → SNP → BIBSS → SAS → upstream adapter → ObservedAttribute(B)  ──┼→ SGW Engine → concept nomination → OPA
Dataset C → SNP → BIBSS → SAS → upstream adapter → ObservedAttribute(C)  ─┘


PART B — SER Pipeline (top-down entity recognition):

New Table → SNP → BIBSS → SAS → upstream adapter → ObservedTable ──→ SER Engine ──→ EntityTypeAssertion
                                                                           ↑
                                                              Entity Pattern Registry
                                                              (populated by OPA placements)
```

### 3.2 The Feedback Loop

The two pipelines are connected through the Entity Pattern Registry:

```
OPA places a new concept (e.g., JobTitle) under CCO:DesignativeInformationContentEntity
  │
  └─→ OPA writes a PatternContribution to the Entity Pattern Registry:
      "NominalType columns with role-like tokens in hr-domain tables
       are evidence for the Employee entity pattern"
  │
  └─→ SER Engine consults the registry on the next table ingestion
      and recognizes tables containing this column pattern as Employee tables
  │
  └─→ SGW Engine receives ObservedAttributes from recognized Employee tables
      with sourceEntityType context, improving cluster confidence
```

The system is self-improving: every OPA placement makes subsequent SER recognitions more accurate; every SER recognition provides richer context to the SGW pipeline.

### 3.3 Relationship to Other FNSR Services

| Service | SGW Relationship | SER Relationship |
|---|---|---|
| SNP / BIBSS / SAS | Upstream — produces ObservedAttribute inputs | Upstream — produces ObservedAttribute inputs bundled into ObservedTable |
| OPA | Output consumer — receives concept nominations | Pattern registry contributor — writes PatternContributions on each placement |
| Fandaws Knowledge Engine | Output consumer via OrchestrationAdapter | Pattern registry source AND output consumer for EntityTypeAssertions |
| Termidium | Post-commit deduplication of nominated concepts | Post-commit deduplication of asserted entity types |
| IEE | Receives normative flag notifications via OPA | Receives normative flag notifications for entity types with normative significance |

---

# PART A — SGW Pipeline
## Semantic Gravity Well Module (Carried Forward from v1.2)

*Sections 4–11 constitute the complete SGW pipeline specification. The algorithms, schemas, and contracts in these sections are unchanged from v1.2 except where explicitly marked. All FTA-CAP items from v1.2 remain open.*

---

## 4. SGW Input Schemas

### 4.1 Input: ObservedAttribute

> **@context Resolution:** All `fandaws-ta:` prefixed terms require a JSON-LD `@context` declaration resolving the prefix. Without it, the Fandaws Validator will reject these nodes. See §9, **FTA-CAP-005**.

```json
{
  "@type": "fandaws-ta:ObservedAttribute",
  "fandaws-ta:datasetId":    "hr_database_v1",
  "fandaws-ta:tableId":     "foobar",
  "fandaws-ta:columnName":   "emp_role",
  "fandaws-ta:ingestTime":   "2026-03-01T14:00:00Z",
  "fandaws-ta:metrics": {
    "distinctCount":    14,
    "rowCount":         2500,
    "cardinalityRatio": 0.0056,
    "entropy":          2.14
  },
  "fandaws-ta:frequentTokens":  ["engineer", "manager", "contractor"],
  "fandaws-ta:assignedSasType": "viz:NominalType",
  "fandaws-ta:sourceSystemDomain": "hr",
  "fandaws-ta:sourceEntityType":   "fandaws:universal/Employee"
}
```

> **v2.0 Addition:** `fandaws-ta:sourceEntityType` is a new optional field populated by the SER pipeline when it has already recognized the table containing this column as an instance of a known entity type. When present, the SGW pipeline uses it as an additional clustering signal — columns from the same recognized entity type receive a bonus to their NMI-hat score (see §5.1.2). This is the primary feedback mechanism from SER to SGW.

> **v2.3 Addition:** `fandaws-ta:tableId` is a new required field identifying the table that contains this column. Upstream adapters must populate this from the source table metadata. This field enables the unified column key format (see below) and eliminates the key expansion step previously required by the Mapping Correction Protocol (§21).

> **Column Key Format (v2.3 — normative):** The canonical column key format throughout the Type Agent is `"datasetId::tableId::columnName"` using double-colon (`::`) as the delimiter. This format is used in SGW member keys, SER column mapping entries, and the Mapping Correction Protocol. The double-colon delimiter is chosen because single colons appear in dataset identifiers (e.g., `urn:dataset:hr_v1`) and column names (e.g., `ns:attribute`). Implementations must use the double-colon convention for all new column keys. The v2.2 single-colon format (`"datasetId:columnName"`) is **deprecated** and must not be used in new implementations. Adapters that consume legacy single-colon keys must expand them to the full triple format using `tableId = "_unknown"` as a sentinel value.

> **Entropy Unit Validation Guard (v2.1 — normative):** The ingestion boundary must validate that every incoming ObservedAttribute's `entropy` value is plausible given the `entropyUnit` declared in the active TypeAgentPolicy. For `entropyUnit = "bits"` (log₂), valid entropy range is `[0, log₂(distinctCount)]`. For `entropyUnit = "nats"` (ln), valid range is `[0, ln(distinctCount)]`. If the observed `entropy` exceeds `log₂(rowCount) × 1.05` under the `bits` policy, the ingestion boundary must **reject** the input with error code `ENTROPY_UNIT_MISMATCH` and a diagnostic message identifying the column, its observed entropy, and the expected maximum. Silent misalignment propagates through every NMI-hat calculation in the session and corrupts the entire SGW topology. This guard is non-negotiable.

### 4.2 Configuration: TypeAgentPolicy

```json
{
  "@type": "fandaws-ta:TypeAgentPolicy",
  "@id":   "fandaws-ta:policy/production-v1",

  "fandaws-ta:weights": {
    "wT": 0.35, "wM": 0.25, "wD": 0.15,
    "wS": 0.10, "wB": 0.10, "wY": 0.05
  },

  "fandaws-ta:thresholds": {
    "autoPromote": 0.80,
    "humanHold":   0.70
  },

  "fandaws-ta:minDatasetCount":                3,
  "fandaws-ta:sgwJoinThreshold":               0.25,
  "fandaws-ta:entropyUnit":                    "bits",
  "fandaws-ta:maxSgwClusters":                 512,
  "fandaws-ta:evictionPolicy":                 "lru",
  "fandaws-ta:targetDatasetCount":             10,
  "fandaws-ta:maxMembersForFullCalculation":   100,
  "fandaws-ta:sourceEntityTypeBonusMultiplier": 1.2,
  "fandaws-ta:serAmbiguityThreshold":           0.15,

  "fandaws-ta:bulkTrustPolicy": {
    "fandaws-ta:enabled":          false,
    "fandaws-ta:trustThreshold":   0.90,
    "fandaws-ta:trustedDatasetIds": [],
    "fandaws-ta:expiresAt":        null
  }
}
```

> **v2.0 Addition:** `sourceEntityTypeBonusMultiplier` (default: 1.2) is applied to NMI-hat when two ObservedAttributes carry the same `sourceEntityType`. This rewards clustering within a recognized entity context. Set to 1.0 to disable the bonus.

> **Weight Constraint:** `wT + wM + wD + wS + wB + wY` must sum to `1.0 ± 1e-9`.

> **Bulk Trust Policy (v2.1):** `bulkTrustPolicy` enables dataset-scoped automatic approval for SER recognitions during planned migrations. When `enabled: true` and a recognition's `matchScore >= trustThreshold` and the table's `datasetId` is in `trustedDatasetIds`, the SER pipeline skips the ConversationPrompt and auto-commits the EntityTypeAssertion regardless of whether `matchScore` falls in the normal agent-review band (§17.2). This prevents prompt flooding during large ingestion events while preserving the normal review pathway for unrecognized or untrusted datasets. `expiresAt` is an ISO-8601 datetime after which the bulk trust policy is automatically disabled — callers must set this to prevent permanent trust escalation. Setting `enabled: true` with a null `expiresAt` is a policy misconfiguration; the validator must emit a warning.

> **`serAmbiguityThreshold`:** The fraction within which two candidate patterns are considered tied and ambiguity is declared (default: 0.15). Decrease for tighter disambiguation (more prompts); increase for looser (fewer prompts, higher ambiguity acceptance). Configurable per deployment to match operational tolerance.

---

## 5. SGW Core Computation

### 5.1 MI Approximation from Summary Statistics

#### 5.1.1 Token Overlap Score

```
overlap(X, Y)  =  |T_X ∩ T_Y|  /  |T_X ∪ T_Y|
```

If either `frequentTokens` is empty, `overlap = 0.0` and `MI-hat = 0.0`.

> **Categorical Scope Boundary:** The Type Agent cannot cluster continuous numeric fields via this metric. See §11, **KL-001** and **FTA-CAP-006**.

Type-concordance multiplier when `assignedSasType` is present and matching:
```
typeConcordance(X, Y)  =  1.3  if sasType(X) = sasType(Y),  else  1.0
```

Source entity type bonus when `sourceEntityType` is present and matching:
```
entityBonus(X, Y)  =  policy.sourceEntityTypeBonusMultiplier
                       if sourceEntityType(X) = sourceEntityType(Y)
                       AND sourceEntityType ≠ null
                       else  1.0
```

#### 5.1.2 MI Approximation Formula

```
MI-hat(X, Y)  =  overlap(X, Y)  ×  typeConcordance(X, Y)  ×  entityBonus(X, Y)
                  ×  min(H(X), H(Y))

NMI-hat(X, Y)  =  MI-hat(X, Y)  /  sqrt( H(X) × H(Y) )
```

**Zero-Entropy Guard (normative):**
```
IF H(X) = 0 OR H(Y) = 0:
  IF T_X = T_Y:  NMI-hat = 1.0
  ELSE:          NMI-hat = 0.0
```

#### 5.1.3 Error Bounds

- NMI-hat is a lower bound on true NMI when token sets are representative.
- Error bounded by `(1 - f) × min(H(X), H(Y))` where `f` is token frequency coverage.
- All provenance records must use `"MI-Approximation"` not `"Mutual Information"`.

#### 5.1.4 Scope: Categorical Fields Only

Valid only for attributes with non-empty `frequentTokens`. Upstream adapters should suppress ObservedAttribute emissions for `viz:QuantitativeType` fields with `distinctCount > 100`. See §11, **KL-001**.

---

### 5.2 SGW Clustering Algorithm

#### 5.2.1 Centroid Definition

Each SGW maintains a synthetic centroid recalculated from scratch after every member assignment:

- `centroid.entropy` = arithmetic mean of member entropies
- `centroid.cardinalityRatio` = arithmetic mean of member cardinalityRatios
- `centroid.frequentTokens` = union of all member tokens, sorted descending by frequency, truncated to 50
- `centroid.assignedSasType` = modal SAS type across members; `null` if no majority
- `centroid.modalSourceEntityType` = modal `sourceEntityType` across members; `null` if no majority or none present

#### 5.2.2 Assignment Algorithm

```
FUNCTION assignObservedAttribute(A, clusters, policy):

  1. REJECT if A is missing any required field.

  2. COMPUTE NMI-hat(A, centroid(C)) for each existing cluster C.

  3. LET best = argmax_C [ NMI-hat(A, centroid(C)) ]

  4. IF NMI-hat(A, centroid(best)) >= policy.sgwJoinThreshold:
       IF tie: ASSIGN to cluster with highest current PS
       ELSE:   ASSIGN A to best
       RECOMPUTE centroid(best) and PS(best)

  5. ELSE: SEED new cluster with A as sole member, PS = 0.0

  6. APPLY retention policy [§7.3]
```

---

### 5.3 The Promotion Score (PS)

```
PS = (wT × T) + (wM × M) + (wD × D) + (wS × S) + (wB × B) + (wY × Y) − P

     with PS clamped to [0.0, 1.0]
```

#### 5.3.1 Score Components

| Sym | Name | Range | Definition |
|---|---|---|---|
| T | Token Signature | [0, 1] | Mean pairwise Jaccard. `T = (2/N(N-1)) × Σ overlap(Xᵢ,Xⱼ)`. **O(N²)** — see §5.3.2. |
| M | MI Cluster Score | [0, 1] | Mean pairwise NMI-hat. `M = (2/N(N-1)) × Σ NMI-hat(Xᵢ,Xⱼ)`. **O(N²)** — see §5.3.2. |
| D | Dependency Score | [0, 1] | `D = 1 − (std(cardinalityRatios) / mean(cardinalityRatios))`, clamped. |
| S | Structural Score | [0, 1] | `S = 1 − (max(H) − min(H)) / max(H)`, clamped. |
| B | Dataset Breadth | [0, 1] | `B = min(1.0, distinctDatasetCount / targetDatasetCount)`. Gate: minDatasetCount. |
| Y | Stability Score | [0, 1] | `Y = 1 − (variance of ingestTime epochs / max epoch range)`, normalized. |
| P | Override Penalty | {0,1} | `P = 1.0` after rejection; cleared after 3 new member assignments. |

#### 5.3.2 Pairwise Sampling for Large Clusters

When `N > policy.maxMembersForFullCalculation`, T and M use a deterministic sample:

```
FUNCTION selectSampleMembers(members, maxCount, sgwId):
  IF members.length <= maxCount: RETURN members
  seed = parseInt(sgwId.substring(0, 8), 16)
  // Fisher-Yates with LCG (a=1664525, c=1013904223, m=2^32) — NORMATIVE
  shuffled = deterministicShuffle(members, seed)
  RETURN shuffled.slice(0, maxCount)
```

LCG parameters are normative. All implementations must use these exact values.

#### 5.3.3 Dataset Breadth: Gate and Score Interaction

- `minDatasetCount`: hard gate — no output below this threshold
- `wB`: continuous scorer above the gate — must be `> 0.0` when `minDatasetCount > 1`

---

### 5.4 Deterministic Hash Function

```
FUNCTION computeSgwHash(sgwCluster):
  1. memberKey(M) = M.datasetId + "::" + M.tableId + "::" + M.columnName
  2. Sort memberKeys lexicographically (Unicode code point, ascending)
  3. canonical = memberKeys.join("|")
  4. hash = SHA-256(UTF-8 bytes of canonical)
  5. sgwId = first 16 hex chars of hash (lowercase)
```

> **v2.3 Breaking Change:** Member key format changed from `"datasetId:columnName"` (v2.2) to `"datasetId::tableId::columnName"` (v2.3). This changes the hash output for all existing SGW clusters. Termidium reconciliation handles the resulting IRI changes. Implementations upgrading from v2.2 must re-hash all clusters on first initialization.

IRI pattern: `fandaws:concept/sgw-{sgwId}`

Hash changes on every membership change. Termidium handles post-change reconciliation.

---

## 6. SGW Fandaws Integration

### 6.1 Auto-Promotion (PS ≥ 0.80)

```json
{
  "@type": "fandaws:GraphMutation",
  "fandaws:additions": [{
    "@id":   "fandaws:concept/sgw-{sgwId}",
    "@type": "fandaws:Concept",
    "fandaws:displayLabel":   "Auto-Generated Concept (SGW: {sgwId})",
    "fandaws:canonicalLabel": "auto_sgw_{sgwId}",
    "fandaws:allowRoot":      false,
    "shml:epistemicStatus":   "auto-promoted"
  }],

  "fnsr:taintLevel": "L3",

  "fandaws:reason": "SGW Convergence. PS: {ps}. Datasets: {n}. Members: {m}.",
  "fandaws:validatedBy": {
    "@type":                     "fandaws-ta:TypeAgentProvenance",
    "fandaws-ta:agentId":        "fandaws-ta:TypeAgent",
    "fandaws-ta:policyId":       "{policy[@id]}",
    "fandaws-ta:promotionScore": "{ps}",
    "fandaws-ta:memberKeys":     ["..."],
    "fandaws-ta:emittedAt":      "{ISO-8601}"
  }
}
```

> **FTA-CAP-001 dependency:** `shml:epistemicStatus: "auto-promoted"` requires Fandaws SHML vocabulary extension.

> **FNSR Taint (v2.3 — normative):** All SGW GraphMutations carry `fnsr:taintLevel: "L3"` (speculative/inferred). SGW concept nominations are derived from statistical convergence across summary statistics — they are not human-attested (L1) or externally verified (L2). The L3 taint level propagates to all downstream consumers. Taint may be promoted to L2 upon OPA placement with external vocabulary alignment, or to L1 upon human confirmation via ConversationPrompt. Taint levels follow the FNSR ecosystem taint contract (see TagTeam-Fandaws Integration Guidance, ACTION 1).

### 6.2 Human/Agent-in-the-Loop (0.70 ≤ PS < 0.80)

Token sourcing: `{token1}` = `centroid.frequentTokens[0]`, `{token2}` = `centroid.frequentTokens[1]`. If only one token: use it for both. If zero tokens: replace phrase with `"based on structural metrics (entropy and cardinality)"`.

```json
{
  "@type": "fandaws:ConversationPrompt",
  "fandaws:promptType": "confirmation",
  "fandaws:text": "Semantic convergence detected across {n} datasets for concept tokens like '{token1}' and '{token2}'. PS: {ps}. Classify as a new Concept?",
  "fandaws:context": {
    "fandaws-ta:sgwId":        "{sgwId}",
    "fandaws-ta:policyId":     "{policy[@id]}",
    "fandaws-ta:resumeAction": "fandaws-ta:action/evalSgwResponse",
    "fandaws-ta:pendingSince": "{ISO-8601}"
  },
  "fandaws:machineSignal": {
    "fandaws:expectedSchema": {
      "type": "object",
      "properties": { "approve": { "type": "boolean" } },
      "required": ["approve"]
    },
    "fandaws:constraintType": "confirmation"
  }
}
```

**Response routing:**
- `approve: true` → PS forced to 1.0, emit GraphMutation
- `approve: false` → P = 1.0 penalty; cluster persists but blocked until 3 new members

### 6.3 Insufficient Evidence (PS < 0.70 or gate not met)

SGW held in TypeAgentStateAdapter. No output. Re-evaluated on each new member assignment.

---

## 7. TypeAgentStateAdapter Interface

### 7.1 Interface Contract

| Method | Returns | Description |
|---|---|---|
| `upsertSGW(cluster: SGWCluster)` | `void` | Insert or replace by `sgwId`. Atomic. |
| `getSGW(sgwId: string)` | `SGWCluster \| null` | Retrieve by ID. |
| `listSGWs()` | `SGWCluster[]` | All clusters, PS descending. |
| `deleteSGW(sgwId: string)` | `boolean` | Delete cluster. |
| `getStats()` | `AdapterStats` | `{ clusterCount, totalMemberCount, memoryEstimateBytes }` |
| `upsertRecognition(rec: TableRecognition)` | `void` | **v2.0** Store SER recognition result by `tableId`. Atomic. |
| `getRecognition(tableId: string)` | `TableRecognition \| null` | **v2.0** Retrieve SER result for a table. |
| `listRecognitions()` | `TableRecognition[]` | **v2.0** All recognition results, score descending. |
| `getColumnMappingEntry(columnKey: string)` | `ColumnMappingLookup \| null` | **v2.2** Retrieve the stored SER column mapping entry for a specific column key of the form `"{datasetId}::{tableId}::{columnName}"`. Returns the matching `columnMapping` entry from the stored `TableRecognition`, or `null` if no recognition exists for the containing table. Used by the OPA Mapping Correction cross-check (§21). |
| `applyMappingCorrection(correction: MappingCorrection)` | `boolean` | **v2.2** Update a stored `TableRecognition`'s `columnMapping` entry in response to an OPA correction. Returns `true` if the correction was applied; `false` if the original recognition was not found (evicted). Atomic. |
| `applyMappingConfirmation(confirmation: MappingConfirmation)` | `void` | **v2.2** Increment the `confirmationCount` on a stored column mapping entry, reinforcing the original SER mapping as semantically correct. |

### 7.2 SGW Cluster Schema

```json
{
  "@type":               "fandaws-ta:SGWCluster",
  "fandaws-ta:sgwId":    "{16-char hex}",
  "fandaws-ta:ps":        0.0,
  "fandaws-ta:policyId": "{policy[@id]}",
  "fandaws-ta:members":  [{ "...": "ObservedAttribute fields" }],
  "fandaws-ta:centroid": {
    "fandaws-ta:entropy":              2.14,
    "fandaws-ta:cardinalityRatio":     0.0056,
    "fandaws-ta:frequentTokens":       ["engineer","manager","contractor"],
    "fandaws-ta:modalSasType":         "viz:NominalType",
    "fandaws-ta:modalSourceEntityType": "fandaws:universal/Employee"
  },
  "fandaws-ta:overridePenalty": false,
  "fandaws-ta:rejectionCount":  0,
  "fandaws-ta:lastUpdated":     "2026-03-01T14:00:00Z"
}
```

### 7.3 Retention Policy

Bounded by `policy.maxSgwClusters`. When cap reached:
- **`lru`** (default): evict oldest `lastUpdated`
- **`evidence-floor`**: evict lowest PS; singletons with no new members this session first

Clusters with pending ConversationPrompt are **never evicted**.

> The reference in-memory adapter is session-scoped. Cross-session persistence requires a HIRI-backed adapter (out of scope for v2.0).

---

## 8. Excised Scope (Both Modules)

- **Canary Classes:** Not used. An ontology node is either logically committed or it is not.
- **Custom Split/Merge Logic:** Handled exclusively by Fandaws Termidium.
- **Rollback State Machines:** Manual Override Penalty handles intra-session suppression. Graph mutation rollback is a Fandaws responsibility (FTA-CAP-002).
- **Supervised Training / ML Models:** Neither module uses trained models, neural networks, or probabilistic priors. All computation is deterministic from summary statistics and graph lookups.

---

## 9. Future Fandaws Capabilities Required

| Cap ID | Capability | Required For | Degradation Without It |
|---|---|---|---|
| FTA-CAP-001 | `shml:epistemicStatus: "auto-promoted"` in Fandaws SHML vocabulary | SGW §6.1 | Auto-promoted concepts use `"imported"` status — conflates statistical convergence with OWL import. |
| FTA-CAP-002 | Deterministic mutation reversal on the Fandaws graph | SGW rollback | OrchestrationAdapter must issue compensating GraphMutation instead. Additional state burden. |
| FTA-CAP-003 | Termidium §6.2 split/merge governance for overlapping structural evidence | Post-promotion concept resolution | Cross-SGW semantic overlap not detected. Duplicate concepts coexist until human merges. |
| FTA-CAP-004 | ConversationPrompt response correlation via `fandaws:context` in OrchestrationAdapter session model | SGW §6.2 | Adapter must implement own prompt-to-SGW mapping table. |
| FTA-CAP-005 | `fandaws-ta:` namespace registration in Fandaws namespace registry | Namespace hygiene | Unregistered prefix. System works but violates governance. |
| FTA-CAP-006 | Structural similarity metric for continuous numeric fields (min/max/mean/stddev) | SGW continuous field clustering | Continuous fields permanently excluded from SGW. See §11, KL-001. |
| FTA-CAP-007 | **Entity Pattern Registry** — A Fandaws service storing entity patterns as expected column-type ensembles associated with Fandaws Universals. The OPA writes to this registry as a side effect of concept placement. The SER engine reads from it. Schema defined in §15. | SER §15–16 | SER cannot operate without a pattern registry. Must fall back to bootstrap-only patterns. The whole feedback loop from OPA placement to SER recognition is broken without this. |
| FTA-CAP-008 | **EntityTypeAssertion** schema in Fandaws GraphMutation contract — a mutation type asserting "this table contains instances of this entity type" with a column mapping array. Currently GraphMutation handles concept-level assertions only. | SER §17 | SER output cannot be recorded in the Fandaws graph. Recognitions exist only in the TypeAgentStateAdapter and are lost on session end. |
| FTA-CAP-009 | **[P0 CRITICAL PATH]** **Pattern Registry Bootstrap process** — pre-populates the Entity Pattern Registry from CCO/BFO entity definitions processed through TagTeam before any data has been ingested. Without bootstrap, the SER engine has no patterns to match on day one and produces `recognition-pending` for every table. Bootstrap process parses definitions of CCO entity types (Person, Organization, Process, InformationContentEntity, Document) via TagTeam and generates initial `EntityPattern` entries with `patternWeight = 0.5`. | SER §15.4 — **blocks all SER capability** | Without bootstrap, SER is completely non-functional on day one. The feedback loop from OPA placements will eventually populate the registry (weeks to months depending on ingestion volume), but this is unacceptable for initial deployment. **FTA-CAP-009 must be completed before FTA-CAP-007, FTA-CAP-008, or FTA-CAP-010 are useful.** |
| FTA-CAP-010 | **OPA PatternContribution side-effect** — when the OPA commits a concept placement, it writes a `PatternContribution` to the Entity Pattern Registry recording the column-type context in which the concept was found. Schema defined in §15.3. | SER §18 (feedback loop) | The feedback loop from OPA placement to improved SER recognition is broken. Pattern registry must be populated manually or through the bootstrap process only. |
| FTA-CAP-011 | **MappingCorrection and MappingConfirmation schemas** in Fandaws GraphMutation contract. `MappingCorrection` is a mutation that updates an existing EntityTypeAssertion's column mapping entry when the OPA's semantic placement disagrees with the SER's structural prediction. `MappingConfirmation` records that the OPA's placement corroborates the SER mapping. Both reference the original EntityTypeAssertion IRI. Schema defined in §21.3. | §21 Mapping Correction Protocol | Without this, the OPA cross-check produces corrections that exist only in the TypeAgentStateAdapter and are lost on session end. The Fandaws graph retains the original (potentially incorrect) mapping permanently. |
| FTA-CAP-012 | **OPA cross-check interface** — a bidirectional query contract between the OPA pipeline and the Type Agent's TypeAgentStateAdapter. The OPA must be able to call `getColumnMappingEntry(columnKey)` and `applyMappingCorrection(correction)` on the adapter at post-commit time. This requires the OPA and Type Agent to share adapter access within the same FNSR service boundary, or for the adapter to expose these methods over the OrchestrationAdapter. | §21 Mapping Correction Protocol | Without this interface, the cross-check algorithm in §21 cannot execute. The OPA has no way to look up stored SER mappings or write corrections back to them. |
| FTA-CAP-013 | **`pendingCrossCheck` flag schema** — `fandaws-ta:pendingCrossCheck` boolean field on `EntityTypeAssertion` nodes. Set to `true` on all bulk-trust-approved assertions at commit time. Cleared to `false` by the OPA cross-check when all column mappings have been confirmed or corrected. Requires a `fandaws:updates` mutation to clear the flag post-commit. | §17.4 Bulk Trust + §21 Cross-Check | Without this flag, downstream consumers cannot distinguish semantically verified from unverified bulk-trust assertions. All bulk-trust assertions are treated as fully trusted regardless of cross-check status, which undermines the correction protocol's value for bulk ingestion scenarios. |

---

## 10. SGW Conformance Checklist

### 10.1 Computation

- Implements the MI approximation formula in §5.1.2 with `entityBonus` multiplier.
- Applies zero-entropy guard: no division attempted when `H = 0`.
- Applies `typeConcordance` multiplier (1.3) on matching `assignedSasType`.
- Applies `entityBonus` multiplier on matching `sourceEntityType`.
- **v2.1:** Applies entropy unit validation guard at ObservedAttribute ingestion boundary. Rejects input with error code `ENTROPY_UNIT_MISMATCH` when observed entropy exceeds `log₂(rowCount) × 1.05` under `bits` policy or `ln(rowCount) × 1.05` under `nats` policy.
- Centroid recalculated from scratch on every assignment; includes `modalSourceEntityType`.
- SGW assignment algorithm with tie-breaking by highest PS.
- Pairwise sampling via normative LCG when `N > maxMembersForFullCalculation`.
- All six PS components (T, M, D, S, B, Y) and penalty P implemented.
- Policy weights validated to sum `1.0 ± 1e-9`.
- Warning emitted when `wB = 0.0` and `minDatasetCount > 1`.
- **v2.1:** Warning emitted when `bulkTrustPolicy.enabled = true` and `expiresAt` is null.
- SGW hash via SHA-256, sorted member keys, 16 lowercase hex characters.
- **v2.3:** Member keys use unified format `"datasetId::tableId::columnName"`. `fandaws-ta:tableId` is required on all ObservedAttribute inputs.

### 10.2 State

- TypeAgentStateAdapter exposes all eleven methods (five original + three v2.0 + three v2.2).
- `upsertSGW` and `upsertRecognition` are atomic.
- Retention policy never evicts clusters with pending ConversationPrompt.

### 10.3 Integration

- Auto-promote GraphMutation includes non-null TypeAgentProvenance.
- **v2.3:** Auto-promote GraphMutation includes `fnsr:taintLevel: "L3"`.
- ConversationPrompt includes `fandaws:context` with all four required fields.
- ConversationPrompt uses `constraintType: "confirmation"`.
- No SGW below `minDatasetCount` emits any output.

### 10.4 Edge-Canonical

- Runs unmodified in browser (ES2020) and Node.js v18+ with no npm dependencies.
- No file system, database, or network calls in computation core or reference adapter.
- All computation synchronous and deterministic.

---

## 11. SGW Known Limitations

### KL-001: Continuous Numeric Fields Are Not Clustered

**Description:** The SGW pipeline cannot cluster continuous numeric fields. Empty `frequentTokens` → `MI-hat = 0.0` → never joins a cluster.

**Mitigation:** Suppress ObservedAttribute emissions for `viz:QuantitativeType` with `distinctCount > 100`. Use `evictionPolicy: "evidence-floor"` to evict singletons.

**Resolution Path:** FTA-CAP-006.

### KL-002: Pairwise Score Approximation at Large Cluster Sizes

**Description:** T and M scores use a deterministic sample when N > `maxMembersForFullCalculation`. Bounded approximation in PS for large clusters.

**Mitigation:** Increase `maxMembersForFullCalculation` in Node.js server deployments.

**Resolution Path:** Future incremental centroid algorithm maintaining determinism.

---

# PART B — SER Pipeline
## Schema Ensemble Recognition Module

---

## 12. SER Executive Summary

The Schema Ensemble Recognition pipeline recognizes the entity type of an unknown database table by matching its complete column-type ensemble against known entity patterns in the Fandaws knowledge graph. It does not wait for cross-dataset convergence. It fires on the first ingestion of a new table.

The intuition: a table is not just a collection of independent columns. It is a structured record of instances of some entity in the world. The columns are the properties of that entity. The structure of those properties — their types, cardinalities, token vocabularies, and relational signatures — forms a recognizable fingerprint that uniquely identifies the entity type, even when the table and column names are opaque.

This fingerprint matching is what a skilled database analyst does immediately when they open an unfamiliar schema. The SER pipeline automates that intuition deterministically.

### 12.1 Day-One vs. Day-N Operation

The SER pipeline operates differently depending on the state of the Entity Pattern Registry:

| Registry State | SER Behavior |
|---|---|
| Bootstrap only (no OPA placements yet) | Recognizes entity types covered by CCO/BFO bootstrap patterns — Person, Organization, Process, Document subtypes. Limited but useful from day one. |
| Growing (early OPA placements) | Adds domain-specific entity types as the OPA places concepts. HR entities appear first if HR data is ingested early. |
| Mature (many OPA placements) | Recognizes a broad vocabulary of domain-specific entity types with high confidence. Unknown tables become rare. |

The bootstrap process (FTA-CAP-009) is what makes day-one operation possible. Without it, the SER engine has no patterns and produces no recognitions on first deployment.

---

## 13. SER Input Schema: ObservedTable

The ObservedTable is the SER pipeline's primary input. It bundles all column profiles from a single table ingestion event into a single container, adding table-level metadata that no individual ObservedAttribute carries.

The upstream adapter that generates ObservedTable nodes is responsible for assembling them from the SAS pipeline's per-column outputs. One ObservedTable is generated per table per ingestion event.

```json
{
  "@type": "fandaws-ta:ObservedTable",
  "fandaws-ta:tableId":            "foobar",
  "fandaws-ta:datasetId":          "hr_database_v1",
  "fandaws-ta:ingestTime":         "2026-03-14T11:00:00Z",
  "fandaws-ta:rowCount":           50000,
  "fandaws-ta:sourceSystemDomain": "hr",

  "fandaws-ta:columns": [
    {
      "fandaws-ta:columnName":      "title",
      "fandaws-ta:sasType":         "viz:NominalType",
      "fandaws-ta:cardinalityRatio": 0.0056,
      "fandaws-ta:entropy":          2.14,
      "fandaws-ta:frequentTokens":  ["engineer", "manager", "contractor"],
      "fandaws-ta:nullRatio":        0.02
    },
    {
      "fandaws-ta:columnName":      "start_dt",
      "fandaws-ta:sasType":         "viz:TemporalType",
      "fandaws-ta:cardinalityRatio": 0.85,
      "fandaws-ta:entropy":          12.3,
      "fandaws-ta:frequentTokens":  [],
      "fandaws-ta:nullRatio":        0.0
    },
    {
      "fandaws-ta:columnName":      "end_dt",
      "fandaws-ta:sasType":         "viz:TemporalType",
      "fandaws-ta:cardinalityRatio": 0.72,
      "fandaws-ta:entropy":          11.9,
      "fandaws-ta:frequentTokens":  [],
      "fandaws-ta:nullRatio":        0.38
    },
    {
      "fandaws-ta:columnName":      "dept_code",
      "fandaws-ta:sasType":         "viz:NominalType",
      "fandaws-ta:cardinalityRatio": 0.002,
      "fandaws-ta:entropy":          3.2,
      "fandaws-ta:frequentTokens":  ["engineering", "finance", "hr", "operations"],
      "fandaws-ta:nullRatio":        0.05
    },
    {
      "fandaws-ta:columnName":      "manager_id",
      "fandaws-ta:sasType":         "viz:NominalType",
      "fandaws-ta:cardinalityRatio": 0.04,
      "fandaws-ta:entropy":          8.1,
      "fandaws-ta:frequentTokens":  [],
      "fandaws-ta:nullRatio":        0.12
    },
    {
      "fandaws-ta:columnName":      "emp_id",
      "fandaws-ta:sasType":         "viz:NominalType",
      "fandaws-ta:cardinalityRatio": 1.0,
      "fandaws-ta:entropy":          15.6,
      "fandaws-ta:frequentTokens":  [],
      "fandaws-ta:nullRatio":        0.0
    }
  ]
}
```

**Required fields:** `tableId`, `datasetId`, `ingestTime`, `rowCount`, `columns` (minimum 1 column).

**Optional fields:** `sourceSystemDomain` (controlled vocabulary: `hr`, `finance`, `clinical`, `legal`, `operations`, `general`).

Each column entry requires: `columnName`, `sasType`, `cardinalityRatio`, `entropy`. Optional per-column: `frequentTokens`, `nullRatio`.

> **Entropy Unit Validation Guard (v2.1 — normative):** The same guard applied to ObservedAttribute at the SGW ingestion boundary (§4.1) applies here to every column in the ObservedTable. The SER ingestion boundary must validate all column `entropy` values against the active policy's `entropyUnit` before fingerprinting begins. If any column fails the guard, the entire ObservedTable is rejected with error code `ENTROPY_UNIT_MISMATCH` and a diagnostic identifying the offending column. Partial fingerprinting of a table with mixed entropy units produces meaningless ColumnRole classifications and must not proceed.

> **Column Name Preservation:** Although `columnName` values are stripped during fingerprint construction (§14.3), they must be preserved in the ObservedTable for use by the Semantic Proximity tiebreaker in column mapping (§16.1). Upstream adapters must not normalize or hash column names before emitting the ObservedTable.

---

## 14. Schema Fingerprinting

The Schema Fingerprint is a normalized, column-name-agnostic representation of a table's structural signature. It abstracts away all identifying information about the specific table so that `foobar.title` and `employees.job_classification` produce the same fingerprint component, provided they have the same structural profile.

Fingerprinting is a pure function. Given the same ObservedTable, it always produces the same fingerprint.

### 14.1 Column Classification

Before fingerprinting, each column is classified into a `ColumnRole` based on its SAS type and cardinality profile:

```
FUNCTION classifyColumnRole(column):

  IF column.sasType = "viz:TemporalType":
    RETURN ColumnRole.TEMPORAL

  IF column.sasType = "viz:BooleanType":
    RETURN ColumnRole.BOOLEAN

  IF column.sasType = "viz:NominalType":
    IF column.cardinalityRatio >= 0.95:
      RETURN ColumnRole.IDENTIFIER          // nearly unique — likely a PK or natural key

    IF column.cardinalityRatio >= 0.01 AND column.cardinalityRatio < 0.10:
      IF column.frequentTokens.length > 0:
        RETURN ColumnRole.CATEGORICAL_CODED  // low-card nominal with vocabulary
      ELSE:
        RETURN ColumnRole.FOREIGN_KEY        // low-card nominal without vocabulary (likely FK)

    IF column.cardinalityRatio < 0.01:
      RETURN ColumnRole.CATEGORICAL_DOMAIN   // very low cardinality — domain/enum column

    RETURN ColumnRole.NOMINAL_UNCLASSIFIED

  IF column.sasType = "viz:QuantitativeType":
    IF column.cardinalityRatio < 0.10:
      RETURN ColumnRole.QUANTITATIVE_CODED   // coded numeric (e.g., status codes as integers)
    RETURN ColumnRole.QUANTITATIVE_CONTINUOUS

  RETURN ColumnRole.UNKNOWN
```

### 14.2 Token Domain Classification

For columns with `frequentTokens`, classify the vocabulary domain:

```
FUNCTION classifyTokenDomain(frequentTokens, sourceSystemDomain):

  Check token set against pre-loaded domain vocabulary signatures:
    "engineer", "manager", "contractor", "director", "analyst"
      → TokenDomain.ORGANIZATIONAL_ROLE

    "engineering", "finance", "hr", "operations", "marketing", "legal"
      → TokenDomain.ORGANIZATIONAL_UNIT

    "active", "inactive", "terminated", "pending", "approved"
      → TokenDomain.STATUS_LIFECYCLE

    "male", "female", "nonbinary", "m", "f"
      → TokenDomain.DEMOGRAPHIC_GENDER

    "full-time", "part-time", "contract", "temporary"
      → TokenDomain.EMPLOYMENT_CLASS

    "usd", "eur", "gbp", "jpy"
      → TokenDomain.CURRENCY_CODE

    [domain vocabulary signatures are loaded from the Entity Pattern Registry
     and grow as the OPA places concepts]

  IF no match: RETURN TokenDomain.UNCLASSIFIED
```

### 14.3 Fingerprint Construction

The fingerprint is a JSON-LD object representing the table's structural signature. It is constructed from the column classifications and does not contain any column names, table names, or dataset identifiers.

```
FUNCTION computeFingerprint(observedTable):

  columns = observedTable.columns.map(col => ({
    role:        classifyColumnRole(col),
    tokenDomain: classifyTokenDomain(col.frequentTokens, observedTable.sourceSystemDomain),
    sasType:     col.sasType,
    nullRatio:   col.nullRatio >= 0.30 ? "sparse" : "dense",
    cardinality: col.cardinalityRatio >= 0.95 ? "unique"
                 : col.cardinalityRatio >= 0.10 ? "high"
                 : col.cardinalityRatio >= 0.01 ? "low"
                 : "enum"
  }))

  // Sort columns by role then tokenDomain for canonical ordering
  // (column order in the source table is not semantically significant)
  canonicalColumns = sortBy(columns,
    c => c.role + "|" + c.tokenDomain + "|" + c.sasType
  )

  return {
    "@type":               "fandaws-ta:SchemaFingerprint",
    "fandaws-ta:tableId":  observedTable.tableId,
    "fandaws-ta:domain":   observedTable.sourceSystemDomain || "general",
    "fandaws-ta:rowCount": classifyTableSize(observedTable.rowCount),
    "fandaws-ta:columnCount": observedTable.columns.length,
    "fandaws-ta:columns":  canonicalColumns,
    "fandaws-ta:structuralSignals": computeStructuralSignals(columns)
  }
```

### 14.4 Structural Signals

Structural signals are higher-order features computed from the column set as a whole. They capture patterns that no individual column can express:

```
FUNCTION computeStructuralSignals(classifiedColumns):

  signals = []

  // Temporal pair: start + end date columns together = employment period or event window
  temporalCount = classifiedColumns.filter(c => c.role = TEMPORAL).length
  IF temporalCount >= 2:
    signals.push("temporal-pair")

  // Identifier + foreign key: PK + reference = entity with relationships
  hasIdentifier = classifiedColumns.any(c => c.role = IDENTIFIER)
  hasForeignKey  = classifiedColumns.any(c => c.role = FOREIGN_KEY)
  IF hasIdentifier AND hasForeignKey:
    signals.push("entity-with-relationships")

  // Role vocabulary: organizational role tokens = person-like entity
  hasRoleVocab = classifiedColumns.any(c => c.tokenDomain = ORGANIZATIONAL_ROLE)
  IF hasRoleVocab:
    signals.push("organizational-role-vocabulary")

  // Lifecycle status: status/state column = managed entity
  hasLifecycle = classifiedColumns.any(c => c.tokenDomain = STATUS_LIFECYCLE)
  IF hasLifecycle:
    signals.push("lifecycle-managed")

  // Dense identifier + temporal pair + role vocab = strong employee signal
  IF hasIdentifier AND temporalCount >= 2 AND hasRoleVocab:
    signals.push("employment-record-signature")

  RETURN signals
```

The `employment-record-signature` signal, for instance, is the fingerprint of the `foobar` table — and the SER algorithm recognizes it as the hallmark of an HR employee-type entity before even consulting the pattern library.

---

## 15. Entity Pattern Registry

The Entity Pattern Registry is a Fandaws-backed library of entity patterns. Each entry describes the column-type ensemble expected in a table containing rows of a given Fandaws Universal. The SER algorithm matches incoming fingerprints against this registry.

The registry is **not** hand-authored. It is generated automatically from two sources:
- OPA PatternContributions (§15.3) — written as a side effect of each concept placement
- Bootstrap patterns (§15.4) — generated from CCO entity definitions at system initialization

### 15.1 EntityPattern Schema

```json
{
  "@type":  "fandaws-ta:EntityPattern",
  "@id":    "fandaws-ta:pattern/Employee-v1",

  "fandaws-ta:forUniversal":     "fandaws:universal/Employee",
  "fandaws-ta:universalLabel":   "Employee",
  "fandaws-ta:domain":           "hr",
  "fandaws-ta:version":          1,
  "fandaws-ta:lastUpdated":      "2026-03-14T11:25:00Z",
  "fandaws-ta:patternWeight":    1.0,

  "fandaws-ta:requiredSignals":  ["employment-record-signature"],
  "fandaws-ta:supportingSignals": ["temporal-pair", "organizational-role-vocabulary",
                                    "entity-with-relationships", "lifecycle-managed"],

  "fandaws-ta:columnPatterns": [
    {
      "fandaws-ta:patternRole":       "identifier",
      "fandaws-ta:columnRole":        "IDENTIFIER",
      "fandaws-ta:sasType":           "viz:NominalType",
      "fandaws-ta:required":          true,
      "fandaws-ta:forConcept":        "fandaws:universal/EmployeeId",
      "fandaws-ta:matchWeight":       0.20
    },
    {
      "fandaws-ta:patternRole":       "title",
      "fandaws-ta:columnRole":        "CATEGORICAL_CODED",
      "fandaws-ta:tokenDomain":       "ORGANIZATIONAL_ROLE",
      "fandaws-ta:sasType":           "viz:NominalType",
      "fandaws-ta:required":          false,
      "fandaws-ta:forConcept":        "fandaws:universal/JobTitle",
      "fandaws-ta:matchWeight":       0.20
    },
    {
      "fandaws-ta:patternRole":       "start-date",
      "fandaws-ta:columnRole":        "TEMPORAL",
      "fandaws-ta:nullRatio":         "dense",
      "fandaws-ta:required":          false,
      "fandaws-ta:forConcept":        "fandaws:universal/EmploymentStartDate",
      "fandaws-ta:matchWeight":       0.15
    },
    {
      "fandaws-ta:patternRole":       "end-date",
      "fandaws-ta:columnRole":        "TEMPORAL",
      "fandaws-ta:nullRatio":         "sparse",
      "fandaws-ta:required":          false,
      "fandaws-ta:forConcept":        "fandaws:universal/EmploymentEndDate",
      "fandaws-ta:matchWeight":       0.15
    },
    {
      "fandaws-ta:patternRole":       "department",
      "fandaws-ta:columnRole":        "CATEGORICAL_DOMAIN",
      "fandaws-ta:tokenDomain":       "ORGANIZATIONAL_UNIT",
      "fandaws-ta:sasType":           "viz:NominalType",
      "fandaws-ta:required":          false,
      "fandaws-ta:forConcept":        "fandaws:universal/Department",
      "fandaws-ta:matchWeight":       0.15
    },
    {
      "fandaws-ta:patternRole":       "manager-reference",
      "fandaws-ta:columnRole":        "FOREIGN_KEY",
      "fandaws-ta:required":          false,
      "fandaws-ta:forConcept":        "fandaws:universal/ManagerReference",
      "fandaws-ta:matchWeight":       0.15
    }
  ],

  "fandaws-ta:minimumMatchScore":  0.60,
  "fandaws-ta:contributionCount":  4
}
```

### 15.2 Pattern Matching Score

The match score between a fingerprint and a pattern is computed as:

```
FUNCTION computeMatchScore(fingerprint, pattern):

  score = 0.0

  // Signal matching (required signals are gates)
  FOR EACH signal IN pattern.requiredSignals:
    IF signal NOT IN fingerprint.structuralSignals:
      RETURN 0.0  // required signal absent — hard fail

  signalBonus = count(fingerprint.structuralSignals ∩ pattern.supportingSignals)
                / pattern.supportingSignals.length × 0.20

  // Column pattern matching
  columnScore = 0.0
  FOR EACH columnPattern P in pattern.columnPatterns:
    bestMatch = argmax over fingerprint.columns of:
      columnSimilarity(fingerprintColumn, P)

    IF columnSimilarity(bestMatch, P) >= 0.60:
      columnScore += P.matchWeight × columnSimilarity(bestMatch, P)

    ELSE IF P.required = true:
      RETURN 0.0  // required column pattern absent — hard fail

  // Domain concordance bonus
  domainBonus = 0.10 if fingerprint.domain = pattern.domain
                0.05 if fingerprint.domain = "general"
                0.0  otherwise

  score = columnScore + signalBonus + domainBonus
  RETURN min(1.0, score)
```

**Column similarity** is computed as:

```
FUNCTION columnSimilarity(fingerprintColumn, patternColumn):

  score = 0.0

  IF fingerprintColumn.role = patternColumn.columnRole:     score += 0.50
  IF fingerprintColumn.sasType = patternColumn.sasType:     score += 0.20
  IF patternColumn.tokenDomain IS SET AND
     fingerprintColumn.tokenDomain = patternColumn.tokenDomain: score += 0.20
  IF patternColumn.nullRatio IS SET AND
     fingerprintColumn.nullRatio = patternColumn.nullRatio:  score += 0.10

  RETURN score
```

### 15.3 PatternContribution: OPA Side-Effect

When the OPA places a concept under a Fandaws Universal, it writes a PatternContribution to the Entity Pattern Registry. This is the mechanism that grows the registry organically from OPA activity.

```json
{
  "@type": "fandaws-ta:PatternContribution",
  "fandaws-ta:forUniversal":      "fandaws:universal/JobTitle",
  "fandaws-ta:placedUnder":       "cco:DesignativeInformationContentEntity",

  "fandaws-ta:observedColumnProfile": {
    "fandaws-ta:columnRole":    "CATEGORICAL_CODED",
    "fandaws-ta:tokenDomain":   "ORGANIZATIONAL_ROLE",
    "fandaws-ta:sasType":       "viz:NominalType",
    "fandaws-ta:nullRatio":     "dense"
  },

  "fandaws-ta:observedTableContext": {
    "fandaws-ta:domain":        "hr",
    "fandaws-ta:coOccurringSignals": [
      "temporal-pair",
      "employment-record-signature",
      "entity-with-relationships"
    ]
  },

  "fandaws-ta:sourceKeys":        ["hr_database_v1::foobar::title", "finance_db_v2::emp_table::employees_title"],
  "fandaws-ta:contributedAt":     "2026-03-14T11:25:00Z",
  "fandaws-ta:opaTraceId":        "fandaws-opa:trace/JobTitle-20260314"
}
```

The registry service accumulates PatternContributions and uses them to update EntityPattern entries for the parent entity type (Employee, in this case — the entity whose tables contain JobTitle columns). This update process is incremental: each new contribution adds evidence to the existing pattern, increasing its `contributionCount` and potentially adding new `columnPatterns` or strengthening existing match weights.

> **FTA-CAP-010 dependency:** This side-effect requires the OPA to have write access to the Entity Pattern Registry at placement time.

### 15.4 Bootstrap Pattern Generation *(expanded in v2.3)*

The bootstrap process generates an initial set of EntityPattern entries from CCO entity definitions before any data has been ingested. It runs once at system initialization and whenever CCO/BFO vocabularies are updated.

The bootstrap process operates as follows:

```
FOR EACH entity type E in CCO/BFO that represents a record-bearing entity:
  (Person, Organization, InformationContentEntity subtypes, Process subtypes, etc.)

  1. Retrieve E's definition from Fandaws or OWL source ontology

  2. ATTEMPT TagTeam NL parse of E's definition text
     IF TagTeam produces a valid parse (see acceptance criteria below):
       GOTO step 3a (NL path)
     ELSE:
       GOTO step 3b (OWL axiom fallback path)

  3a. NL PATH — Extract conceptual neighborhood from TagTeam output
      Map neighborhood entities to expected column patterns:
        - Person references → FOREIGN_KEY with person-referencing token domain
        - Temporal entities → TEMPORAL columns
        - Organizational entities → CATEGORICAL_DOMAIN with org token domain
        - Information entities → CATEGORICAL_CODED or IDENTIFIER
      GOTO step 4

  3b. OWL AXIOM FALLBACK PATH — Extract column patterns from OWL restrictions
      FOR EACH restriction R on E or its direct superclasses:
        IF R is someValuesFrom(P, C):
          Map C to a column pattern using BFO branch:
            C ∈ BFO:Occurrent or temporal subclass → TEMPORAL
            C ∈ BFO:IndependentContinuant (Agent/Person) → FOREIGN_KEY
            C ∈ IAO:InformationContentEntity → CATEGORICAL_CODED
            C ∈ BFO:Quality or BFO:Disposition → NOMINAL_UNCLASSIFIED
          Assign matchWeight = 0.10 (lower than NL-derived patterns)
      GOTO step 4

  4. APPLY acceptance criteria (§15.4.1) — reject if minimum viable pattern
     threshold not met

  5. Generate EntityPattern with matchWeight proportional to definition prominence
  6. Write to Entity Pattern Registry with patternWeight = 0.5
     (bootstrap patterns are lower weight than OPA-contributed patterns)
```

Bootstrap pattern weight is 0.5 (half of OPA-contributed patterns' default 1.0) to reflect that they are derived from definitions rather than observed data. As OPA contributions accumulate for the same entity type, the registry blends both sources with OPA contributions taking increasing weight.

#### 15.4.1 Bootstrap Acceptance Criteria *(new in v2.3)*

Not all CCO/BFO entity definitions produce usable EntityPatterns. Many definitions are semi-formal ("An agent is an independent continuant that is the bearer of a role and can be the agent of a process") and may not yield sufficient structural signal for table recognition.

A bootstrap-generated EntityPattern is accepted if and only if it meets the **minimum viable pattern** threshold:

```
FUNCTION isViableBootstrapPattern(candidatePattern):

  // Minimum structural signal requirements:
  requiredSignalCount = candidatePattern.requiredSignals.length
  columnPatternCount  = candidatePattern.columnPatterns.length

  // A viable pattern must have at least:
  // - 1 required signal (structural signature that gates recognition)
  // - 2 column patterns (enough to distinguish from noise)
  IF requiredSignalCount < 1 OR columnPatternCount < 2:
    RETURN false

  // At least one column pattern must have a non-UNKNOWN role
  classifiedCount = candidatePattern.columnPatterns
    .filter(p => p.columnRole != "NOMINAL_UNCLASSIFIED" AND p.columnRole != "UNKNOWN")
    .length
  IF classifiedCount < 1:
    RETURN false

  RETURN true
```

**TagTeam parse quality assessment:** The TagTeam parse is considered valid for bootstrap purposes if:

- `tagteam:genericityCategory` is `GEN` (the definition describes a general type, not an instance)
- `tagteam:structuralAssertions` contains at least one assertion with a recognized relation
- `tagteam:conceptualNeighborhood` contains at least two neighborhood entities

If the TagTeam parse fails any of these criteria, the bootstrap process falls back to the OWL axiom path (step 3b). Both paths converge on the same acceptance criteria in step 4.

**Expected bootstrap coverage:** Based on CCO's entity type inventory:

| Entity Type | Expected Path | Viable Pattern? |
|---|---|---|
| Person | NL path — well-defined in CCO | Yes — identifier, temporal pair, role vocabulary |
| Organization | NL path | Yes — identifier, categorical domain, entity-with-relationships |
| Document | NL path | Yes — identifier, temporal, categorical coded |
| Process | OWL axiom fallback — abstract definition | Marginal — may produce only 1 column pattern (temporal) |
| Quality | OWL axiom fallback | No — insufficient structural signal for table recognition |
| Role | OWL axiom fallback | No — roles are column-level, not table-level entities |

Entity types that fail the acceptance criteria are logged as `bootstrap-rejected` with the specific criterion that failed. They are not written to the registry. They can be manually added later if domain-specific knowledge identifies a viable pattern.

> **FTA-CAP-009 updated requirement (v2.3):** The bootstrap process must implement both the NL path and the OWL axiom fallback path. Implementations that only implement the NL path will produce fewer viable patterns for abstract entity types. The acceptance criteria in §15.4.1 are normative — patterns that fail the criteria must not be written to the registry.

---

## 16. Ensemble Matching Algorithm

The ensemble matching algorithm searches the Entity Pattern Registry for the best match to an incoming fingerprint and produces a ranked list of candidate entity types.

```
FUNCTION matchEnsemble(fingerprint, patternRegistry, policy):

  candidates = []

  FOR EACH pattern P in patternRegistry:
    score = computeMatchScore(fingerprint, P)
    IF score >= P.minimumMatchScore:
      candidates.push({
        pattern:         P,
        matchScore:      score,
        entityType:      P.forUniversal,
        entityLabel:     P.universalLabel
      })

  // Sort by score descending
  candidates = sortBy(candidates, c => -c.matchScore)

  // Produce column mapping for the best candidate
  IF candidates.length > 0:
    best = candidates[0]
    columnMapping = mapColumnsToPattern(fingerprint, best.pattern)
    RETURN MatchResult {
      recognized:       true,
      topCandidate:     best.entityType,
      topScore:         best.matchScore,
      allCandidates:    candidates,
      columnMapping:    columnMapping,
      ambiguous:        candidates.length >= 2
                        AND candidates[1].matchScore >= best.matchScore × 0.85
    }

  RETURN MatchResult { recognized: false }
```

### 16.1 Column Mapping

When the best pattern is identified, the algorithm produces a column mapping — the operational output that makes recognition actionable. In v2.1, a Semantic Proximity tiebreaker is applied when two or more source columns produce the same structural similarity score against the same pattern column.

```
FUNCTION mapColumnsToPattern(fingerprint, pattern, observedTable):

  mapping = []
  usedSourceColumns = {}

  FOR EACH columnPattern P in pattern.columnPatterns
    (ordered by matchWeight descending — highest weight patterns claim columns first):

    candidates = fingerprint.source columns NOT in usedSourceColumns

    // Primary score: structural similarity (unchanged from v2.0)
    scoredCandidates = candidates.map(col => ({
      col,
      structuralScore: columnSimilarity(col, P)
    }))

    // Semantic Proximity tiebreaker (v2.1):
    // When two candidates have structuralScore within 0.05 of each other,
    // and the pattern column has a forConcept with a known rdfs:label,
    // apply a name-similarity bonus using the original column names from
    // observedTable (which are preserved in full — not stripped during fingerprinting).
    FOR EACH candidate WHERE |candidate.structuralScore - maxStructuralScore| <= 0.05:
      conceptLabel = rdfsLabel(P.forConcept)   // e.g., "JobTitle", "Department"
      nameBonus    = normalizedNameSimilarity(
                       candidate.originalColumnName,
                       conceptLabel
                     )
      // normalizedNameSimilarity uses token overlap after splitting on
      // underscores, camelCase, and hyphens. "job_classification" against
      // "JobTitle" → tokens {"job","classification"} ∩ {"job","title"} = {"job"}
      // → similarity = 1/3 = 0.33 → bonus = 0.33 × 0.15 = 0.05

      candidate.totalScore = candidate.structuralScore + (nameBonus × 0.15)

    bestCandidate = argmax(candidate.totalScore)

    IF bestCandidate.structuralScore >= 0.60:
      mapping.push({
        "fandaws-ta:sourceColumnName": bestCandidate.originalColumnName,
        "fandaws-ta:mapsTo":           P.forConcept,
        "fandaws-ta:mapConfidence":    bestCandidate.totalScore,
        "fandaws-ta:patternRole":      P.patternRole,
        "fandaws-ta:nameProximityBonus": nameBonus × 0.15
      })
      usedSourceColumns[bestCandidate.originalColumnName] = true

  // Collect unmapped columns for EntityTypeAssertion
  unmapped = observedTable.columns
    .filter(col => col.columnName NOT in usedSourceColumns)
    .map(col => col.columnName)

  RETURN { mapping, unmapped }
```

**Semantic Proximity semantics:** The name bonus is strictly a tiebreaker. It has a maximum contribution of `0.15 × 1.0 = 0.15` to the total score. It cannot promote a structurally poor match above a structurally strong one — a candidate must achieve `structuralScore >= 0.60` to be eligible regardless of name similarity. Its purpose is to resolve the specific case where two structurally identical columns (e.g., two `STATUS_LIFECYCLE` nominal columns) must be assigned to two different pattern slots, and the column name provides evidence for which is which.

**Opaque name handling:** If `originalColumnName` is a single character, a UUID pattern, or matches a known opaque naming pattern (configurable list, default: `["col_\d+", "f\d+", "field\d+"]`), the name bonus is suppressed (`nameBonus = 0.0`). Opaque names contain no semantic signal and must not influence mapping decisions.

### 16.2 Ambiguity Handling

When two or more patterns score within `policy.serAmbiguityThreshold` (default: 0.15) of each other, the match result is flagged as `ambiguous`. Ambiguous recognitions are routed to agent review rather than auto-commit, regardless of absolute score.

> **v2.1:** The ambiguity threshold is now a configurable `OPAPolicy` parameter rather than a hard-coded constant. Deployments with a high tolerance for ambiguity (e.g., where all tables are well-understood business entities) may increase this value to reduce prompt frequency. Deployments requiring precision (e.g., regulated data environments where entity misclassification has compliance consequences) should decrease it toward 0.05.

**Ambiguity resolution signals** (applied when ambiguous = true):

```
SIGNAL 1 — Domain concordance: does one candidate's domain match the
           observed table's sourceSystemDomain? Score that candidate +0.10.

SIGNAL 2 — Row count compatibility: does one candidate's typical row count
           range match the observed table's rowCount class?

SIGNAL 3 — Required signal coverage: does one candidate have more of its
           required signals satisfied than the other?

After applying disambiguation signals, re-evaluate. If gap > 15%: resolve.
If still tied: emit ConversationPrompt asking the agent to choose.
```

---

## 17. SER Output: EntityTypeAssertion

When the SER engine produces a high-confidence, unambiguous match, it emits an EntityTypeAssertion to the Fandaws OrchestrationAdapter.

### 17.1 Auto-Recognition (matchScore ≥ 0.80, ambiguous = false)

```json
{
  "@type": "fandaws:GraphMutation",
  "fandaws:additions": [
    {
      "@id":   "fandaws-ta:recognition/{tableId}-{ingestTime-hash}",
      "@type": "fandaws-ta:EntityTypeAssertion",

      "fandaws-ta:assertedTable":      "hr_database_v1::foobar",
      "fandaws-ta:assertedEntityType": "fandaws:universal/Employee",
      "fandaws-ta:entityTypeLabel":    "Employee",
      "fandaws-ta:matchScore":         0.84,
      "fandaws-ta:ambiguous":          false,
      "shml:epistemicStatus":          "auto-recognized",

      "fandaws-ta:columnMapping": [
        {
          "fandaws-ta:sourceColumnName": "title",
          "fandaws-ta:mapsTo":           "fandaws:universal/JobTitle",
          "fandaws-ta:mapConfidence":     0.90,
          "fandaws-ta:patternRole":       "title"
        },
        {
          "fandaws-ta:sourceColumnName": "start_dt",
          "fandaws-ta:mapsTo":           "fandaws:universal/EmploymentStartDate",
          "fandaws-ta:mapConfidence":     0.85,
          "fandaws-ta:patternRole":       "start-date"
        },
        {
          "fandaws-ta:sourceColumnName": "end_dt",
          "fandaws-ta:mapsTo":           "fandaws:universal/EmploymentEndDate",
          "fandaws-ta:mapConfidence":     0.80,
          "fandaws-ta:patternRole":       "end-date"
        },
        {
          "fandaws-ta:sourceColumnName": "dept_code",
          "fandaws-ta:mapsTo":           "fandaws:universal/Department",
          "fandaws-ta:mapConfidence":     0.88,
          "fandaws-ta:patternRole":       "department"
        },
        {
          "fandaws-ta:sourceColumnName": "manager_id",
          "fandaws-ta:mapsTo":           "fandaws:universal/ManagerReference",
          "fandaws-ta:mapConfidence":     0.75,
          "fandaws-ta:patternRole":       "manager-reference"
        },
        {
          "fandaws-ta:sourceColumnName": "emp_id",
          "fandaws-ta:mapsTo":           "fandaws:universal/EmployeeId",
          "fandaws-ta:mapConfidence":     0.95,
          "fandaws-ta:patternRole":       "identifier"
        }
      ],

      "fandaws-ta:unmappedColumns": [],

      "fnsr:taintLevel": "L3",

      "fandaws-ta:recognitionProvenance": {
        "@type":                   "fandaws-ta:SERProvenance",
        "fandaws-ta:agentId":      "fandaws-ta:TypeAgent",
        "fandaws-ta:pipelineMode": "SER",
        "fandaws-ta:matchedPattern": "fandaws-ta:pattern/Employee-v1",
        "fandaws-ta:structuralSignals": [
          "employment-record-signature",
          "temporal-pair",
          "entity-with-relationships",
          "organizational-role-vocabulary"
        ],
        "fandaws-ta:recognizedAt": "2026-03-14T11:01:00Z"
      }
    }
  ],

  "fnsr:taintLevel": "L3",

  "fandaws:reason": "SER auto-recognition. Table: foobar. Entity type: Employee. Score: 0.84. Pattern: Employee-v1. Signals: employment-record-signature, temporal-pair.",

  "fandaws:validatedBy": {
    "@type":             "fandaws-ta:SERProvenance",
    "fandaws-ta:agentId": "fandaws-ta:TypeAgent"
  }
}
```

> **FTA-CAP-008 dependency:** The `fandaws-ta:EntityTypeAssertion` node type and `fandaws-ta:columnMapping` structure must be added to the Fandaws GraphMutation schema.

> **FTA-CAP-001 parallel:** `shml:epistemicStatus: "auto-recognized"` is a new value, analogous to `"auto-promoted"` for SGW. Requires the same Fandaws SHML vocabulary extension.

> **FNSR Taint (v2.3 — normative):** All SER EntityTypeAssertions carry `fnsr:taintLevel: "L3"` (speculative/inferred) by default. SER recognition is structural pattern matching without human verification — this is definitionally L3. Taint levels for EntityTypeAssertions follow this promotion path:
>
> | State | Taint Level | Trigger |
> |---|---|---|
> | Initial SER recognition | **L3** | Auto-recognition or agent-review commit |
> | OPA cross-check confirms all column mappings | **L2** | All column mappings in the assertion have received `MappingConfirmation` from the OPA |
> | Human attestation | **L1** | Agent explicitly confirms the entity type via ConversationPrompt |
>
> The `fnsr:taintLevel` field appears both on the EntityTypeAssertion node (assertion-level taint) and on the enclosing GraphMutation (envelope-level taint, per FNSR Integration Guidance ACTION 1). Both must be present and consistent.

### 17.2 Agent-Review (0.60 ≤ matchScore < 0.80 or ambiguous = true)

```json
{
  "@type": "fandaws:ConversationPrompt",
  "fandaws:promptType": "disambiguation",
  "fandaws:text": "Table '{tableId}' ({rowCount} rows) matches the {topCandidate} entity pattern with {matchScore}% confidence. {ambiguousText} Should I classify this table as containing {topCandidateLabel} records?",

  "fandaws:context": {
    "fandaws-ta:observedTableId":  "{tableId}",
    "fandaws-ta:datasetId":        "{datasetId}",
    "fandaws-ta:resumeAction":     "fandaws-ta:action/evalSerResponse",
    "fandaws-ta:topCandidate":     "{entityTypeIRI}",
    "fandaws-ta:allCandidates":    ["{ entityTypeIRI, label, score }..."],
    "fandaws-ta:pendingSince":     "{ISO-8601}"
  },

  "fandaws:machineSignal": {
    "fandaws:expectedSchema": {
      "type": "object",
      "properties": {
        "confirmedEntityType": { "type": "string" },
        "approve":             { "type": "boolean" }
      },
      "required": ["approve"]
    },
    "fandaws:constraintType": "disambiguation"
  }
}
```

**Response routing:**
- `approve: true, confirmedEntityType: IRI` → emit EntityTypeAssertion with the confirmed entity type
- `approve: true` (no confirmedEntityType) → emit EntityTypeAssertion with the top candidate
- `approve: false` → store in TypeAgentStateAdapter as `recognition-rejected`; suppress future prompts for the same table in the same session

### 17.3 No Match (matchScore < 0.60 or registry empty)

The ObservedTable is stored in the TypeAgentStateAdapter as `recognition-pending`. No output is emitted to Fandaws. The SGW pipeline processes the table's columns independently via the normal ObservedAttribute pathway. When future OPA placements add new patterns to the registry, the pending table may be re-evaluated.

```
FUNCTION handleNoMatch(observedTable):
  storeRecognition(observedTable.tableId, {
    status:        "recognition-pending",
    reason:        bestCandidate?.score < 0.60 ? "below-threshold" : "no-patterns",
    bestCandidate: bestCandidate || null,
    storedAt:      now()
  })
  // Route columns to SGW pipeline normally
  FOR EACH column IN observedTable.columns:
    emitObservedAttribute(buildObservedAttribute(column, observedTable))
```

### 17.4 Bulk Trust Policy Routing (v2.1)

When `policy.bulkTrustPolicy.enabled = true`, a dataset-scoped automatic approval pathway applies before the normal routing logic. This is designed for planned migrations where the operator has pre-approved a specific dataset for autonomous recognition above a defined score threshold.

```
FUNCTION applyBulkTrustPolicy(matchResult, observedTable, policy):

  btp = policy.bulkTrustPolicy

  IF NOT btp.enabled:
    RETURN false  // normal routing applies

  IF btp.expiresAt IS SET AND now() > btp.expiresAt:
    EMIT warning "BulkTrustPolicy expired — reverting to normal routing"
    RETURN false

  IF observedTable.datasetId NOT IN btp.trustedDatasetIds:
    RETURN false  // dataset not in scope — normal routing applies

  IF matchResult.matchScore >= btp.trustThreshold AND NOT matchResult.ambiguous:
    RETURN true   // auto-commit without ConversationPrompt

  RETURN false    // below threshold or ambiguous — normal routing applies
```

**Integration with normal routing:** The bulk trust check is applied immediately after the ensemble match result is produced and before the normal routing decision (§17.1/§17.2). If `applyBulkTrustPolicy` returns `true`, the EntityTypeAssertion is emitted with `shml:epistemicStatus: "bulk-trust-approved"` instead of `"auto-recognized"`, and the recognition provenance records the bulk trust policy ID that authorized the commit.

**Pending Cross-Check Flag (v2.3 — normative):** Every bulk-trust-approved EntityTypeAssertion is emitted with `fandaws-ta:pendingCrossCheck: true`. This flag signals to downstream consumers that the column mappings in this assertion have not yet been semantically verified by the OPA cross-check protocol (§21). Downstream consumers that require verified mappings — including reasoning services, IEE normative evaluations, and knowledge commitment pipelines — should treat `pendingCrossCheck: true` assertions as provisional and filter or defer processing accordingly.

The flag is cleared to `false` when **all** column mappings in the EntityTypeAssertion have been either confirmed or corrected by the OPA cross-check. The clearing is performed by the cross-check algorithm (§21) as an additional step after processing all member keys:

```
// v2.3: After cross-checking all keys for a given recognition,
// evaluate whether pendingCrossCheck can be cleared.
FUNCTION evaluateCrossCheckCompleteness(recognitionId, adapter):

  recognition = adapter.getRecognition(recognitionId)
  IF recognition IS NULL: RETURN  // evicted — cannot clear

  allMappingsChecked = recognition.columnMapping.every(mapping =>
    mapping.confirmationCount > 0 OR mapping.correctedMapsTo IS SET
  )

  IF allMappingsChecked:
    emitPendingCrossCheckClearedMutation(recognitionId)
    // GraphMutation: set fandaws-ta:pendingCrossCheck = false
    // Also promotes fnsr:taintLevel from L3 to L2 on the assertion
```

> **FTA-CAP-013 dependency:** The `fandaws-ta:pendingCrossCheck` boolean field must be added to the `EntityTypeAssertion` schema. Without this, downstream consumers cannot distinguish verified from unverified bulk-trust assertions.

**Audit trail:** Every bulk-trust-approved commit records `fandaws-ta:bulkTrustPolicyId`, `fandaws-ta:trustedDatasetId`, and `fandaws-ta:pendingCrossCheck: true` in the EntityTypeAssertion. This allows post-migration audits to identify which recognitions bypassed normal review and which have not yet been semantically verified. The `expiresAt` field is required; deployments that omit it receive a policy validation warning (§4.2).

---

## 18. The SER–SGW Feedback Loop

The feedback loop is the mechanism that makes the Type Agent v2.0 self-improving. It operates in both directions.

### 18.1 SER → SGW (Context Enrichment)

When the SER pipeline successfully recognizes a table as an instance of a known entity type, it populates `fandaws-ta:sourceEntityType` on every ObservedAttribute emitted from that table's columns. This field feeds back into the SGW pipeline's NMI-hat calculation via the `entityBonus` multiplier (§5.1.2), improving the clustering signal for columns from recognized entity contexts.

Effect: columns from an Employee table cluster together more strongly than columns from unrecognized tables, because the SGW pipeline knows they are all describing properties of the same entity type. Cross-dataset convergence on Employee columns is detected faster and with higher confidence.

### 18.2 OPA → SER (Pattern Accumulation)

When the OPA places a concept and records its column-type context as a PatternContribution (§15.3), the Entity Pattern Registry learns that columns of a certain structural profile, found in tables of a certain domain, are evidence for a specific entity type. This improves the SER engine's pattern matching on all subsequent table ingestions.

Effect: as more concepts are placed by the OPA, the SER engine recognizes a progressively wider variety of entity types. The system's day-N capability is substantially better than its day-one capability, and it improves without any human intervention.

### 18.3 SER → Pattern Registry (Self-Reinforcement)

When the SER engine produces a high-confidence recognition, it also writes a lightweight PatternContribution back to the Entity Pattern Registry, recording the specific column-role combination that produced the match. This reinforces the pattern with real-world evidence and adjusts column pattern match weights based on observed frequency.

This creates a complete self-reinforcing loop:

```
Data arrives → SGW detects column convergence → OPA places concepts
    ↓
OPA writes PatternContributions → Registry grows
    ↓
New table arrives → SER matches richer registry → EntityTypeAssertion emitted
    ↓
SER writes reinforcement PatternContributions → Registry grows further
    ↓
SGW receives sourceEntityType context → Clustering improves
    ↓
More concepts nominated sooner → OPA places more concepts
    ↓ (loop continues)
```

### 18.4 OPA → SER (Mapping Correction) *(new in v2.2)*

The cross-check protocol closes the final gap in the feedback loop: semantic verification of SER column mappings. When the OPA places a concept, it performs a backward lookup against stored SER recognitions to determine whether any of the concept's nominating column keys appear in an existing column mapping. If they do, it compares the semantic placement result against the structural mapping prediction.

```
OPA places JobTitle under CCO:DesignativeInformationContentEntity
    │
    └─→ Looks up column keys: ["hr_database_v1::foobar::title"]
        in TypeAgentStateAdapter.getColumnMappingEntry(...)
    │
    ├── Found: SER had mapped foobar.title → fandaws:universal/JobTitle
    │   OPA placed concept = fandaws:universal/JobTitle  ← MATCH
    │   → emit MappingConfirmation
    │   → increment confirmationCount on mapping entry
    │
    └── Found: SER had mapped foobar.title → fandaws:universal/ProjectRole
        OPA placed concept = fandaws:universal/JobTitle  ← MISMATCH
        → emit MappingCorrection
        → update stored mapping entry: mapsTo := fandaws:universal/JobTitle
        → emit GraphMutation flagging original EntityTypeAssertion for re-evaluation
```

This loop runs silently as a post-commit step in the OPA pipeline. Over time, every SER column mapping that the SGW pipeline subsequently touches is either confirmed or corrected by actual semantic placement evidence. The system converges on semantic accuracy without human review of individual column mappings.

---

## 19. SER Conformance Checklist

### 19.1 Fingerprinting

- Implements `classifyColumnRole` exactly as specified in §14.1. All seven ColumnRole values must be produced.
- Implements `classifyTokenDomain` with at minimum the six token domain patterns specified in §14.2. Additional domain patterns may be added from the Entity Pattern Registry.
- Computes `structuralSignals` from §14.4. All six signals must be detected.
- Fingerprint construction is deterministic: same ObservedTable always produces same fingerprint.
- Fingerprint does not contain column names, table names, or dataset identifiers.
- **v2.1:** Entropy unit validation guard applied to every column before fingerprinting begins. Any column failing the guard causes the entire ObservedTable to be rejected with `ENTROPY_UNIT_MISMATCH`. Partial fingerprinting must not proceed.
- **v2.1:** Original column names preserved verbatim in the ObservedTable for the Semantic Proximity tiebreaker (§16.1). The implementation must not normalize, hash, or truncate column names before passing them to `mapColumnsToPattern`.

### 19.2 Pattern Matching

- `computeMatchScore` applies required signal gates before scoring — a failed required signal immediately returns 0.0.
- `columnSimilarity` uses the four-component scoring function from §16.
- `mapColumnsToPattern` uses a one-to-one mapping with the Semantic Proximity tiebreaker (§16.1).
- The name similarity bonus has maximum contribution `0.15`; it cannot promote a structurally poor match above a structurally strong one.
- Opaque column name patterns suppress the name bonus (configurable list per §16.1).
- Ambiguity is declared when the second-ranked candidate scores within `policy.serAmbiguityThreshold` of the top candidate (default: 0.15).
- Disambiguation signals are applied before emitting a ConversationPrompt.

### 19.3 Output

- Auto-recognition emits EntityTypeAssertion with `shml:epistemicStatus: "auto-recognized"` and a complete `columnMapping` array including `fandaws-ta:nameProximityBonus` per mapped column.
- **v2.3:** All EntityTypeAssertions carry `fnsr:taintLevel: "L3"` on both the assertion node and the enclosing GraphMutation envelope.
- Bulk-trust-approved recognitions emit EntityTypeAssertion with `shml:epistemicStatus: "bulk-trust-approved"` and record `fandaws-ta:bulkTrustPolicyId` and `fandaws-ta:trustedDatasetId` in recognition provenance.
- **v2.3:** Bulk-trust-approved EntityTypeAssertions carry `fandaws-ta:pendingCrossCheck: true`.
- Agent-review emits ConversationPrompt with `fandaws:context` containing `observedTableId`, `datasetId`, `resumeAction`, `topCandidate`, `allCandidates`, and `pendingSince`.
- No-match stores recognition state and routes columns to SGW pipeline via ObservedAttribute.
- Every auto-recognition (including bulk-trust-approved) writes a reinforcement PatternContribution to the Entity Pattern Registry.
- **v2.1:** `unmappedColumns` array included in every EntityTypeAssertion, listing columns from the source table that were not matched to any pattern column. This supports downstream consumers in deciding whether unrecognized columns warrant further investigation.

### 19.4 Feedback Loop

- Every recognized ObservedTable's columns are emitted as ObservedAttributes with `sourceEntityType` populated.
- Every auto-recognition writes a reinforcement PatternContribution (§18.3).
- The TypeAgentStateAdapter stores all recognition results via `upsertRecognition`.
- Recognition-pending tables are re-evaluated when the pattern registry is updated (new patterns available).
- **v2.2:** Every stored `TableRecognition` includes a fully-qualified column key index — mapping `"datasetId::tableId::columnName"` to the corresponding `columnMapping` entry — to support O(1) lookup by the OPA cross-check.

### 19.5 Bulk Trust Policy (v2.1)

- `applyBulkTrustPolicy` is evaluated before normal routing for every SER recognition result.
- Bulk-trust-approved commits carry `shml:epistemicStatus: "bulk-trust-approved"` and record `bulkTrustPolicyId` and `trustedDatasetId` in provenance.
- Expired bulk trust policies (`now() > expiresAt`) revert to normal routing and emit a warning.
- Bulk trust is never applied to ambiguous recognitions regardless of `matchScore`.
- The policy validator emits a warning when `enabled = true` and `expiresAt` is null.
- **v2.2:** Bulk-trust-approved EntityTypeAssertions are subject to the same OPA cross-check as normally-committed assertions. No special handling required in the SER pipeline.
- **v2.3:** Bulk-trust-approved EntityTypeAssertions carry `fandaws-ta:pendingCrossCheck: true`. The flag is cleared by the OPA cross-check (§21), not by the SER pipeline. The SER pipeline's only obligation is to set the flag at commit time.
- **v2.3:** `fnsr:taintLevel` promotion from L3 → L2 occurs atomically with `pendingCrossCheck` clearing, when the OPA cross-check confirms all column mappings.

### 19.6 Mapping Correction Protocol (v2.2)

- `getColumnMappingEntry(fullyQualifiedKey)` returns the correct `columnMapping` entry or `null` within O(1) time using the column key index.
- `applyMappingCorrection(correction)` updates the stored mapping entry atomically and returns `true` if applied, `false` if recognition was evicted.
- `applyMappingConfirmation(confirmation)` increments `confirmationCount` on the mapping entry.
- `correction-missed` events are logged when `applyMappingCorrection` returns `false`. Events are retrievable via `getStats()`.
- The correction cascade (§21.4) must be applied by the OPA (not the SER module) — the SER module's only obligation is to expose the adapter interface.

---

## 20. SER Known Limitations

### KL-003: Day-One Operation Requires Bootstrap; Bootstrap Quality Limits Early Recognition

**Description:** The SER engine cannot recognize any entity type on day one without the bootstrap process (FTA-CAP-009). Bootstrap pattern quality is limited by the depth of CCO entity definitions and TagTeam's ability to parse them.

**Mitigation:** Prioritize bootstrap for entity types likely to appear in the first datasets ingested. For an HR-focused deployment, bootstrap Employee, Organization, Position, and Department before any data arrives.

**Resolution Path:** FTA-CAP-009 specifies the bootstrap process. The bootstrap quality improves automatically as OPA placements accumulate via the feedback loop.

### KL-004: SER Cannot Recognize Entity Types Not in the Pattern Registry

**Description:** The SER engine produces no recognition for a table whose entity type has no corresponding pattern. These tables produce `recognition-pending` status and fall back to SGW processing.

**Mitigation:** This is correct behavior, not a defect. The SGW pipeline will eventually nominate concepts for the OPA to place, adding patterns to the registry. The fallback to SGW is seamless.

**Resolution Path:** The feedback loop (§18) resolves this organically over time.

### KL-005: Column Mapping Confidence — ~~Deferred~~ RESOLVED in v2.2

**Resolution:** The Mapping Correction Protocol (§21) provides full post-hoc semantic verification of SER column mappings through the OPA cross-check. Every column mapping subsequently touched by the SGW pipeline and processed through the OPA will be either confirmed or corrected. The correction cascade (§21.4) propagates corrections back into the Entity Pattern Registry.

**Residual exposure (KL-007):** The cross-check can only operate on SER recognitions remaining in the TypeAgentStateAdapter at OPA placement time. See KL-007.

---

### KL-006: Bulk Trust Policy Bypasses Normal Review — Requires Operational Discipline

**Description:** When `bulkTrustPolicy.enabled = true`, recognitions above `trustThreshold` are committed without ConversationPrompt review. If the registry contains an incorrect or immature pattern, bulk trust can commit incorrect EntityTypeAssertions at scale before any agent can intervene.

**Built-in safeguards:** `expiresAt` forces time-bounding. `trustedDatasetIds` limits scope. `trustThreshold` (default: 0.90) exceeds the normal auto-commit threshold (0.80). `shml:epistemicStatus: "bulk-trust-approved"` makes bulk-approved commits distinguishable in audit queries.

**Interaction with Mapping Correction Protocol:** Bulk-trust-approved EntityTypeAssertions are subject to the same OPA cross-check as normally-committed assertions. Bulk trust errors are self-healing — they will be detected and corrected as the SGW pipeline processes the same columns. The correction may lag the initial commit by hours or days.

**Operator responsibility:** Verify the registry contains at least one OPA-contributed pattern (not only bootstrap patterns) for each entity type in the trusted dataset before activating bulk trust.

**Resolution Path:** No algorithmic resolution. Operational discipline requirement.

---

### KL-007: Mapping Corrections Unavailable After Session Eviction *(v2.2, quantified v2.3)*

**Description:** The cross-check (§21) requires the original SER recognition to be present in the TypeAgentStateAdapter at OPA placement time. If the recognition has been evicted — due to the retention cap, LRU eviction, or a session restart — the cross-check is skipped and the original EntityTypeAssertion retains its uncorrected mapping permanently.

**Root Cause:** The TypeAgentStateAdapter is session-scoped in the reference in-memory implementation. SER recognitions may be evicted before the SGW pipeline has accumulated sufficient convergence evidence to trigger an OPA placement.

#### Correction Loss Model *(new in v2.3)*

The correction opportunity window is the overlap between SER recognition retention and SGW convergence time. When the retention window is shorter than the convergence time, corrections are lost.

**Key timing parameters:**

| Parameter | Typical Value | Source |
|---|---|---|
| Median SGW convergence time (to `minDatasetCount = 3`) | 3–7 days | Depends on ingestion rate and cross-dataset overlap |
| SER recognition time (from table ingestion to stored mapping) | Seconds | Immediate on ingestion |
| OPA placement time (from SGW promotion to concept commit) | Seconds | Immediate on PS threshold |
| Gap = convergence time − recognition time | 3–7 days | The window during which the recognition must survive |

**Estimated correction loss by deployment scenario:**

| Scenario | Session Lifetime | Retention | Estimated Correction Loss | Rationale |
|---|---|---|---|---|
| **Development** (in-memory, short sessions) | ~4 hours | Session-scoped | **85–95%** | Almost no SGW cluster reaches `minDatasetCount` within a single 4-hour session. Nearly all SER recognitions evicted before any cross-check is possible. |
| **Staging** (in-memory, long-running) | ~24 hours | Session-scoped | **60–80%** | Some fast-converging clusters (high-overlap datasets ingested in batch) reach promotion within the session. Most multi-day convergences still lost. |
| **Production** (HIRI-persistent adapter) | Indefinite | Persistent | **~0%** | No eviction. All SER recognitions survive until the cross-check executes, regardless of convergence time. |

**Interpretation:** In early deployment — when patterns are immature and corrections matter most — the in-memory adapter loses the vast majority of correction opportunities. This is acceptable for development and testing where the focus is on algorithm correctness, not semantic convergence. It is **not acceptable for production deployment** where uncorrected EntityTypeAssertions propagate incorrect column mappings to downstream consumers indefinitely.

**Mitigation (in-memory adapter):** Configure `evictionPolicy: "evidence-floor"` to preferentially evict zero-PS singletons before recognized tables. This extends the effective retention window for SER recognitions but does not resolve the fundamental session-scope limitation.

**Resolution Path:** **HIRI-backed TypeAgentStateAdapter is a production deployment requirement, not a future enhancement.** The in-memory reference adapter is sufficient for development and algorithm validation. Any deployment that commits EntityTypeAssertions to the Fandaws graph and expects downstream consumers to rely on column mappings must use a persistent adapter.

---

### KL-008: Taint Promotion Requires Cross-Service Coordination *(new in v2.3)*

**Description:** The FNSR taint propagation model (§6.1, §17.1) specifies that EntityTypeAssertion taint can be promoted from L3 → L2 when the OPA cross-check confirms all column mappings, and from L3/L2 → L1 upon human attestation. However, the taint promotion from L3 → L2 requires the OPA cross-check to emit a `fandaws:updates` mutation that modifies the `fnsr:taintLevel` field on an existing EntityTypeAssertion node. This is a cross-service write: the OPA (a Fandaws-internal agent) modifies a node originally created by the Type Agent (another Fandaws-internal agent).

**Root Cause:** The FNSR taint model was designed for service-boundary events (TagTeam → HIRI → Fandaws), not for intra-Fandaws agent coordination. The Type Agent and OPA share the Fandaws graph but have no explicit protocol for taint promotion.

**Mitigation:** The `pendingCrossCheck` flag (§17.4) serves as a proxy for taint status: `pendingCrossCheck: true` implies L3; `pendingCrossCheck: false` implies the OPA has verified the assertion, supporting L2 promotion. Downstream consumers that cannot read `fnsr:taintLevel` directly can use `pendingCrossCheck` as a coarser signal.

**Resolution Path:** The OPA cross-check completeness evaluation (§17.4) already emits a GraphMutation to clear `pendingCrossCheck`. That same mutation should also update `fnsr:taintLevel` from L3 to L2 atomically. This requires FTA-CAP-013 (pendingCrossCheck schema) and FTA-CAP-011 (updates mutation support) to both be implemented.

---

## 21. Mapping Correction Protocol *(new in v2.2)*

The Mapping Correction Protocol is the final stage of the SER–OPA feedback loop. It provides semantic verification of SER column mappings by cross-checking them against OPA concept placements. When the OPA places a concept whose nominating column evidence came from a SER-recognized table, it either confirms or corrects the original structural mapping. Over time, this protocol converges the SER's structural predictions toward semantic accuracy without any human review of individual column assignments.

### 21.1 Cross-Check Algorithm (OPA Step 7)

The cross-check runs as Step 7 of the OPA pipeline, immediately after the concept placement GraphMutation has been committed to Fandaws. It is a pure lookup-and-compare operation. It does not block the OPA placement — the concept is committed regardless of whether a cross-check is possible.

```
FUNCTION performMappingCrossCheck(placedConcept, nominationRequest, adapter):

  // Build the column key set from the nomination's member keys
  // v2.3: Member keys are already in the unified format "datasetId::tableId::columnName"
  // (see §4.1 Column Key Format). No expansion step required.

  memberKeys = nominationRequest.statisticalEvidence?.memberKeys
               OR [buildColumnKey(nominationRequest.tagteamEvidence)]

  FOR EACH key IN memberKeys:

    mappingEntry = adapter.getColumnMappingEntry(key)

    IF mappingEntry IS NULL:
      // No SER recognition stored for this column — skip
      CONTINUE

    serPrediction   = mappingEntry.mapsTo        // IRI the SER mapped this column to
    opaPlacement    = placedConcept.universalIRI  // IRI the OPA just committed

    IF serPrediction = opaPlacement:
      // Agreement: the SER's structural prediction was semantically correct
      adapter.applyMappingConfirmation({
        columnKey:       fullyQualifiedKey,
        confirmedIRI:    opaPlacement,
        confirmedAt:     now(),
        opaTraceId:      placedConcept.reasoningTraceId
      })
      // No Fandaws mutation needed — original EntityTypeAssertion stands

    ELSE:
      // Disagreement: the SER predicted the wrong concept for this column
      correction = buildMappingCorrection(
        mappingEntry, serPrediction, opaPlacement, placedConcept
      )
      applied = adapter.applyMappingCorrection(correction)

      IF applied:
        emitMappingCorrectionMutation(correction)
      ELSE:
        // Recognition was evicted from adapter before correction could be applied
        // Record as a correction-missed event for audit; see KL-007
        logEvictionMiss(fullyQualifiedKey, correction)
```

#### 21.1.1 Column Key Format *(revised in v2.3)*

~~The SGW pipeline stores member keys in the format `"datasetId:columnName"`. The cross-check requires the fully-qualified form `"datasetId::tableId::columnName"` to match against SER recognition entries. The expansion queries the SGW cluster state for the `sourceEntityType` context of the relevant member.~~

**v2.3:** The unified column key format `"datasetId::tableId::columnName"` is now used throughout the Type Agent — in SGW member keys, SER column mapping entries, and the cross-check algorithm. The key expansion step from v2.2 is eliminated. Member keys already contain the `tableId` because `fandaws-ta:tableId` is a required field on `ObservedAttribute` (§4.1).

If a member key has `tableId = "_unknown"` (legacy sentinel for migrated single-colon keys), the cross-check skips that key — no SER mapping can exist for a column whose table is unknown.

---

### 21.2 MappingConfirmation Schema

```json
{
  "@type":                         "fandaws-ta:MappingConfirmation",
  "fandaws-ta:columnKey":          "hr_database_v1::foobar::title",
  "fandaws-ta:confirmedMapsTo":    "fandaws:universal/JobTitle",
  "fandaws-ta:confirmationCount":  3,
  "fandaws-ta:confirmedAt":        "2026-03-14T12:00:00Z",
  "fandaws-ta:opaTraceId":         "fandaws-opa:trace/JobTitle-20260314"
}
```

Confirmations are recorded in the TypeAgentStateAdapter only. They do not produce Fandaws GraphMutations — the original EntityTypeAssertion is already correct and requires no update. The `confirmationCount` field accumulates across multiple OPA placements that independently corroborate the same mapping entry, providing a signal of mapping reliability to downstream consumers.

---

### 21.3 MappingCorrection Schema

A MappingCorrection is emitted when the OPA's semantic placement disagrees with the SER's structural column mapping prediction. It produces both an adapter update and a Fandaws GraphMutation.

#### 21.3.1 TypeAgentStateAdapter Correction Record

```json
{
  "@type":                          "fandaws-ta:MappingCorrection",
  "fandaws-ta:columnKey":           "hr_database_v1::foobar::status",
  "fandaws-ta:originalMapsTo":      "fandaws:universal/EmploymentStatus",
  "fandaws-ta:correctedMapsTo":     "fandaws:universal/ProjectStatus",
  "fandaws-ta:originalMapConfidence": 0.72,
  "fandaws-ta:correctionBasis":     "opa-semantic-placement",
  "fandaws-ta:correctedAt":         "2026-03-14T13:00:00Z",
  "fandaws-ta:opaTraceId":          "fandaws-opa:trace/ProjectStatus-20260314",
  "fandaws-ta:originalRecognitionId": "fandaws-ta:recognition/foobar-20260314"
}
```

#### 21.3.2 Fandaws GraphMutation

```json
{
  "@type": "fandaws:GraphMutation",

  "fandaws:updates": [
    {
      "@id":   "fandaws-ta:recognition/foobar-20260314",
      "@type": "fandaws-ta:EntityTypeAssertion",

      "fandaws-ta:columnMappingCorrections": [
        {
          "fandaws-ta:columnKey":         "hr_database_v1::foobar::status",
          "fandaws-ta:originalMapsTo":    "fandaws:universal/EmploymentStatus",
          "fandaws-ta:correctedMapsTo":   "fandaws:universal/ProjectStatus",
          "fandaws-ta:correctionSource":  "opa-semantic-placement",
          "fandaws-ta:correctedAt":       "2026-03-14T13:00:00Z",
          "fandaws-ta:opaTraceId":        "fandaws-opa:trace/ProjectStatus-20260314"
        }
      ],

      "fandaws-ta:mappingCorrectionStatus": "corrected",
      "fandaws-ta:requiresReEvaluation":    true
    }
  ],

  "fandaws:reason": "OPA semantic placement disagreed with SER structural mapping for column hr_database_v1::foobar::status. Original: EmploymentStatus. Corrected: ProjectStatus.",

  "fandaws:validatedBy": {
    "@type":             "fandaws-ta:MappingCorrectionProvenance",
    "fandaws-ta:agentId": "fandaws-ta:TypeAgent",
    "fandaws-ta:opaTraceId": "fandaws-opa:trace/ProjectStatus-20260314"
  }
}
```

The `requiresReEvaluation: true` flag signals to Fandaws downstream consumers — including the IEE and any reasoning services — that the `columnMapping` in this EntityTypeAssertion has been partially superseded and they should consult the `columnMappingCorrections` array before relying on the original mapping.

> **FTA-CAP-011 dependency:** The `fandaws:updates` operation and the `fandaws-ta:columnMappingCorrections` array on `EntityTypeAssertion` require schema additions to Fandaws. Without these, corrections can only be stored in the TypeAgentStateAdapter and are not reflected in the Fandaws graph.

---

### 21.4 Correction Cascade: When a Correction Triggers Pattern Registry Updates

A MappingCorrection does not only fix a single column mapping in a single recognition. Because the Entity Pattern Registry was partially built from reinforcement PatternContributions from SER recognitions, a correction that contradicts a prior reinforcement contribution may require the registry to be updated as well.

```
FUNCTION handleCorrectionCascade(correction, patternRegistry):

  // Find any PatternContribution records that were generated from
  // the same column key with the original (now-incorrect) mapsTo IRI
  affectedContributions = patternRegistry.findContributions({
    columnKey:   correction.columnKey,
    forUniversal: correction.originalMapsTo
  })

  FOR EACH contribution IN affectedContributions:
    // Reduce the weight of the affected pattern column in the registry
    // rather than deleting it — the structural evidence was real,
    // just semantically misinterpreted
    currentWeight = patternRegistry.getColumnPatternWeight(
      contribution.patternId, contribution.patternRole
    )
    newWeight = max(0.0, currentWeight - 0.10)  // v2.3: explicit floor clamp
    patternRegistry.setColumnPatternWeight(
      patternId:       contribution.patternId,
      patternRole:     contribution.patternRole,
      weight:          newWeight
    )

    // v2.3: Zero-weight pruning — flag entries that have lost all weight
    IF newWeight = 0.0:
      patternRegistry.flagPrunable(
        patternId:   contribution.patternId,
        patternRole: contribution.patternRole
      )
      // Prunable entries are excluded from match scoring immediately.
      // Physical removal occurs at registry compaction time (see §21.4.1).

  // Add a positive contribution for the correct concept
  patternRegistry.addContribution({
    forUniversal:           correction.correctedMapsTo,
    observedColumnProfile:  lookupColumnProfile(correction.columnKey),
    correctionBasis:        "opa-cross-check"
  })
```

The correction cascade ensures that future SER recognitions do not repeat the same structural misclassification. The decremented weight on the incorrect pattern column reduces its influence on match scoring without discarding the structural evidence entirely — the column genuinely has the profile the SER detected, it was just mapped to the wrong concept.

#### 21.4.1 Zero-Weight Pruning *(new in v2.3)*

When a column pattern entry's `matchWeight` reaches 0.0 through repeated corrections, it is flagged `prunable: true`. Prunable entries have the following properties:

- **Immediately excluded from match scoring.** The `computeMatchScore` function (§15.2) skips prunable column patterns. They contribute 0.0 to `columnScore` and do not trigger the required-column-absent hard fail (even if `required: true`, since a required column pattern that has been corrected to zero weight is clearly not a reliable signal).

- **Retained in the registry for audit.** Prunable entries are not physically deleted immediately — they serve as a record of which structural signals were initially believed relevant but were semantically incorrect.

- **Physically removed at compaction time.** The registry compaction process runs periodically (configurable, default: daily) and removes all `prunable: true` entries that have been flagged for more than `pruneRetentionPeriod` (configurable, default: 7 days). This allows operators to audit recently-pruned entries before they are permanently deleted.

- **Cannot be revived by new contributions.** A prunable entry cannot be un-pruned by a new PatternContribution for the same pattern role. Instead, a new column pattern entry is created with the corrected `forConcept` IRI — the prunable entry and the new entry coexist during the retention period.

---

### 21.5 Cross-Check Conformance Requirements

A conformant implementation of the OPA Mapping Correction Protocol must:

- Execute the cross-check as Step 7, after and independent of the concept placement commit. The cross-check must not delay or block the placement.
- **v2.3:** Member keys are already in unified `"datasetId::tableId::columnName"` format. No key expansion step is required. Keys with `tableId = "_unknown"` (legacy sentinel) are silently skipped.
- Emit a `MappingConfirmation` for every match where `serPrediction = opaPlacement`. Confirmations are stored in the adapter only.
- Emit a `MappingCorrection` for every match where `serPrediction ≠ opaPlacement`. Corrections are stored in the adapter AND produce a Fandaws `GraphMutation`.
- Apply the correction cascade (§21.4) for every emitted correction. **v2.3:** Weight decrements use explicit `max(0.0, weight - decrement)` clamp. Zero-weight entries are flagged `prunable: true` and excluded from match scoring.
- Log `correction-missed` events when `applyMappingCorrection` returns false due to eviction. These events are stored in the adapter's diagnostic log, not emitted as Fandaws mutations.
- Include `fandaws-ta:requiresReEvaluation: true` on all correction mutations.
- **v2.3:** After processing all member keys for a given recognition, evaluate cross-check completeness (§17.4). If all column mappings are confirmed or corrected, emit a GraphMutation clearing `fandaws-ta:pendingCrossCheck` to `false` and promoting `fnsr:taintLevel` from L3 to L2.

> **FTA-CAP-012 dependency:** The cross-check requires the OPA to call `getColumnMappingEntry` and `applyMappingCorrection` on the Type Agent's TypeAgentStateAdapter. This shared access must be established through the OrchestrationAdapter inter-service contract. The exact mechanism is out of scope for this specification and is deferred to the FNSR Inter-Service Protocol (ISP).

