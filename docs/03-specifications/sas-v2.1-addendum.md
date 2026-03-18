# Schema Alignment Service (SAS)

## Specification Addendum — Version 2.1

**Status:** Normative
**Supersedes:** SAS v2.0 §§ as noted per section
**Date:** 2026-03-02
**Author:** Aaron Damiano (Semantic Architect)

---

## Preamble

This addendum closes six specification gaps identified during the FBO v1.1 integration review and the kernel code audit that expanded the SAS Term Registry from 29 to 35 terms. It incorporates four architecture decision records (ADR-006, ADR-007, ADR-009, ADR-010) that were resolved during Phase 1 implementation but never written back to the spec.

**Reading convention:** Each section below names the v2.0 section it amends or extends. Sections marked **(new)** have no v2.0 antecedent. Text marked ~~strikethrough~~ is removed from the v2.0 text. Text in **bold blocks** replaces the stricken text or is inserted at the stated location.

---

## 1. Exhaustive Alignment Rule Registry (amends §6, new Appendix F)

### 1.1 Problem

SAS v2.0 names alignment rules informally within their respective §6 subsections but provides no single authoritative enumeration. The kernel code audit identified 8 distinct `sas:alignmentRule` string values emitted by the implementation. Three of these — `cism-validation-failed`, `structural-passthrough` (edge case), and `temporal-detection-snp-evidence` (trigger conditions) — were either unnamed or incompletely specified in v2.0. The FBO Bridge Ontology encodes these values in the `rdfs:comment` on `fbo:producedByRule` and needs an authoritative source document.

### 1.2 Normative Rule Registry

The following table is exhaustive. Any `sas:alignmentRule` value not listed here is a specification violation. Implementations MUST NOT emit unlisted values. Implementations MUST emit exactly one of these values per `viz:DataField` in the output.

| Value | Spec Section | Assigned Type | Trigger Condition | Diagnostic | Consensus Score Semantics |
|---|---|---|---|---|---|
| `consensus-promotion` | §6.1 | See sub-cases below | The consensus evaluation machinery was entered (the field has a `typeDistribution` and is eligible for consensus analysis). The rule name `consensus-promotion` describes the *process attempted*, not just the success path. Three sub-cases: | See sub-cases | See sub-cases |

**`consensus-promotion` sub-cases:**

| Sub-case | Assigned Type | Trigger Condition | Diagnostic | Consensus Score Semantics |
|---|---|---|---|---|
| Success | Per §6.1.1 mapping (winner type) | A non-null type passes the integer threshold check AND `nonNullTotal >= minObservationThreshold` | — | Computed: `numerator / denominator` where numerator = winning type count, denominator = nonNullTotal |
| Min-obs failure | `viz:UnknownType` | `nonNullTotal < minObservationThreshold` (default 5). Checked BEFORE the threshold test. A single integer out of 10,000 nulls yields consensus 1.0, but one observation cannot justify type promotion. | SAS-012 | Set to `"0.000000"` with `consensusNumerator = 0`, `consensusDenominator = nonNullTotal`. The score is zeroed because the observation count is insufficient for statistical confidence, not because there was disagreement. |
| No consensus | `viz:NominalType` (safe fallback) | `nonNullTotal >= minObservationThreshold` but no single non-null type passes the integer threshold check. The data is genuinely mixed. | SAS-001 | Computed: the highest single-type ratio among non-null types, formatted per §2.6. `consensusNumerator` = count of the highest type, `consensusDenominator` = nonNullTotal. The score records what the *best* consensus candidate achieved, even though it failed the threshold. |
| `temporal-detection` | §6.2, case 1 | `viz:TemporalType` | Field `primitiveType` is `string`, consensus on string passes threshold, AND field name matches `temporalNamePattern`. No SNP manifest evidence for this field. | SAS-010 | Inherited: consensus score from the string consensus that triggered temporal name checking |
| `temporal-detection-snp-evidence` | §6.2, case 2 | `viz:TemporalType` | SNP v1.3 manifest contains one or more `date_converted` entries whose `path` matches this field's name (case-insensitive match against the CISM `SchemaEdge.name`). This rule fires regardless of whether the field name matches `temporalNamePattern`. | SAS-009 | Inherited: consensus score from the underlying string consensus. If the field has mixed types (e.g., 95% string, 5% integer), the consensus score reflects the string proportion, not 1.0 — the SNP evidence overrides the type assignment but does not alter the statistical observation. |
| `boolean-pair-configured` | §6.3 | `viz:BooleanType` | Field name appears in `SASConfig.booleanFields` (case-insensitive match) AND BIBSS `primitiveType` is `string`. | — | Set to `"1.000000"` with `consensusNumerator = consensusDenominator = nonNullTotal`. Rationale: the caller's configuration is treated as authoritative — it asserts that the string values are boolean pairs. The consensus score reflects this certainty, not the type distribution. |
| `null-vocabulary-configured` | §6.4 | Per reclassified consensus winner | Field has string values that match entries in `SASConfig.nullVocabulary` (field-specific) or `SASConfig.globalNullVocabulary`. After reclassifying matched strings as null, the adjusted type distribution is re-evaluated through §6.1 consensus promotion. | SAS-008 (when reclassification changes the winner) | Recomputed: consensus is recalculated after reclassification. The `sas:consensusNumerator` and `sas:consensusDenominator` reflect the adjusted counts (original null-vocabulary strings excluded from the non-null denominator). |
| `structural-passthrough` | §6.5 | Per §6.1.1 mapping of `primitiveType` | No higher-priority rule (§6.1–§6.4) produced a classification. The BIBSS `primitiveType` is mapped directly to `viz:DataType`. | — | Normal case: `"1.000000"` with `consensusNumerator = consensusDenominator = nonNullTotal` (unanimous structural agreement). Null exhaustion edge case (§1.5): assigns `viz:UnknownType` with `"0.000000"` and `consensusNumerator = 0`, `consensusDenominator = 0` (no observations remain after reclassification). |
| `unknown-assignment` | §6.6 | `viz:UnknownType` | CISM node has `primitiveType: "null"` (all values null) OR node `kind` is `"union"`. | SAS-002 | Set to `"0.000000"` with `consensusNumerator = 0`, `consensusDenominator = 0`. A field with no typed observations has no consensus. |
| `cism-validation-failed` | §6.1.3 | `viz:UnknownType` | CISM consistency validation (§6.1.3) detected a structural invariant violation: negative `occurrences`, `typeDistribution` sum exceeding `occurrences` (including the `null` key), or `nullCount > occurrences`. **Halts further rule evaluation** — the cascade is skipped entirely for this field. | SAS-013 (field-level fatal) | Set to `"0.000000"` with `consensusNumerator = 0`, `consensusDenominator = 0`. The type distribution cannot be trusted; no consensus is computable. |

**Fandaws enrichment rules** (Phase 1v2):

| Value | Spec Section | Assigned Type | Trigger Condition | Diagnostic |
|---|---|---|---|---|
| `fandaws-override` | §6.7.2 | Per Fandaws concept type guidance | Fandaws returns a committed concept with type guidance that differs from the static classification (coded-identifier → Nominal, temporal entity → Temporal, quantity → Quantitative), OR an imported concept produces a soft override (§6.7.5 epistemic matrix, consensus ≤ 0.99). | SAS-004 |
| `boolean-pair-fandaws` | §6.3 | `viz:BooleanType` | Fandaws identifies the field as boolean-valued in the domain. | SAS-004 |
| `null-vocabulary-fandaws` | §6.4 | Per reclassified consensus | Fandaws concept has `fandaws:nullEquivalentValues` property. Values are reclassified and consensus recomputed per §6.4. | SAS-008 |

**Invariant:** Every `viz:DataField` in the output carries exactly one `sas:alignmentRule` value from the static rule table (8 values) OR, when Fandaws enrichment is active and produces a classification, from the enrichment rule table (3 values). The two tables are mutually exclusive per field — if Fandaws produced a classification, the static rule that *would have* applied is not recorded. The static core's rule name is suppressed, not appended.

### 1.3 Amendments to §6.1.3

**Insert after** the final sentence of §6.1.3 ("If any fatal diagnostic is emitted during validation, the field is assigned `viz:UnknownType` and no consensus calculation is attempted."):

> **Rule name:** `"cism-validation-failed"`. The output field carries `sas:alignmentRule: "cism-validation-failed"`, `sas:consensusNumerator: 0`, `sas:consensusDenominator: 0`, `viz:consensusScore: "0.000000"`.

### 1.4 Amendments to §6.2

**Replace** the final line of §6.2:

~~`- **Rule name:** "temporal-detection" or "temporal-detection-snp-evidence"`~~

**With:**

> **Rule names:**
>
> - `"temporal-detection"` — assigned when the classification is produced by field name pattern matching (case 1 above). Emits SAS-010.
> - `"temporal-detection-snp-evidence"` — assigned when the classification is produced by SNP manifest evidence (case 2 above). Emits SAS-009. This rule takes precedence: if both the name pattern and SNP evidence match, the rule name is `"temporal-detection-snp-evidence"` because manifest evidence is stronger than a name heuristic.

### 1.5 Amendments to §6.5

**Insert after** the final sentence of §6.5 ("A field where BIBSS observed only integers, with no temporal signal, no boolean pair, no Fandaws context, passes through as `viz:QuantitativeType` with `numericPrecision: "integer"` and `consensusScore: "1.000000"`."):

> **Edge case — null vocabulary exhaustion:** If §6.4 null vocabulary reclassification is applied and reclassifies ALL non-null observations to null (i.e., every string value in the field matched the null vocabulary), the consensus calculation has `nonNullTotal = 0` after reclassification. In this case, the field is assigned `viz:UnknownType` via the `structural-passthrough` rule path — not via §6.6 `unknown-assignment`. The distinction matters: §6.6 is scoped to CISM-level conditions (all-null nodes, union nodes) where BIBSS itself observed no typed data. Null exhaustion is a SAS-layer reinterpretation — BIBSS observed real string values, but SAS's null vocabulary reclassified them all away. The `structural-passthrough` rule name preserves this provenance: it tells downstream consumers "we evaluated this field through the rule cascade and fell through to the structural layer," which is different from "BIBSS reported no types."
>
> The type assignment is `viz:UnknownType` (not the per-`primitiveType` mapping from §6.1.1) because zero remaining observations provide no evidence for any type. Assigning `viz:NominalType` because BIBSS saw strings — strings we then reclassified entirely away — would give a false impression of knowledge. The field structurally contained strings, but semantically we discarded them all. `UnknownType` is the epistemically honest answer.
>
> The consensus score is set to `"0.000000"` with `consensusNumerator = 0` and `consensusDenominator = 0`. Rationale: 0/0 is undefined, and assigning any positive confidence score to a field with zero remaining semantic observations would be epistemically dishonest — downstream systems that filter on `consensusScore > 0.9` for auto-approval would silently promote a field with no actual type evidence.
>
> **Distinguishing null exhaustion from validation failure:** Both null exhaustion and `cism-validation-failed` produce `viz:UnknownType` with `consensusScore: "0.000000"` and zeroed numerator/denominator. The canonical distinguishing signals are: (1) the diagnostic code — null exhaustion emits **SAS-008** with `reclassifiedCount` equal to the original non-null total (before reclassification), while validation failure emits **SAS-013**; and (2) the rule name — null exhaustion uses `"structural-passthrough"`, while validation failure uses `"cism-validation-failed"`. Downstream consumers that need to differentiate these cases MUST inspect the diagnostic code or rule name, not the consensus score. The score is a lossy summary; the diagnostic and rule name are the authoritative records.
>
> SAS-002 is NOT emitted for null exhaustion. SAS-002 is reserved for §6.6 `unknown-assignment` (CISM-level all-null or union). The diagnostic distinction between SAS-002 (BIBSS saw nothing), SAS-008 (SAS reclassified everything), and SAS-013 (CISM data is structurally broken) must be preserved.

### 1.6 Amendments to §6.7.2

**Insert after** the final bullet of §6.7.2 ("If Fandaws says the field is a **quantity** with specific units or constraints: assign `viz:QuantitativeType` and annotate with the Fandaws concept's unit/range information."):

> **Rule name:** `"fandaws-override"`. This is the general Fandaws type override rule for committed concepts with type guidance and for imported concepts that produce soft overrides per §6.7.5. The `boolean-pair-fandaws` and `null-vocabulary-fandaws` rule names are reserved for the domain-specific cases in §6.3 and §6.4 respectively; all other Fandaws type changes use `"fandaws-override"`.

---

## 2. `sas:activeConfig` Output Structure (new §5.6)

### 2.1 Problem

ADR-010 added `sas:activeConfig` as a required output block during Phase 1, but the spec does not document its structure, property names, or serialization format. The FBO team designed `fbo:AlignmentConfiguration` and its five data properties from implementation artifacts rather than from normative text.

### 2.2 New Section: §5.6 `sas:activeConfig` Structure

**Insert after §5.5.** The section number §5.6 is new; existing §6 and above are unaffected (§6 is "Alignment Rules," which keeps its number).

> ### 5.6 `sas:activeConfig` Structure
>
> Every `viz:DatasetSchema` output MUST include an `sas:activeConfig` block that records the complete configuration used for this alignment invocation. This block is a self-describing snapshot: any consumer can reconstruct the alignment parameters without access to the caller's `SASConfig` object.
>
> ```json
> {
>   "@type": "sas:AlignmentConfiguration",
>   "sas:consensusThreshold": 0.95,
>   "sas:minObservationThreshold": 5,
>   "sas:nullVocabulary": ["N/A", "-", "none"],
>   "sas:booleanPairs": [
>     {
>       "sas:fieldName": "is_active",
>       "sas:trueValue": "Y",
>       "sas:falseValue": "N"
>     }
>   ],
>   "sas:temporalNamePattern": "(?:date|time|timestamp|created|updated|modified|born|died|started|ended|expires?)(?:_at|_on|_time)?$"
> }
> ```
>
> **Required properties** (always present, even when using defaults):
>
> | Property | JSON Type | Source | Description |
> |---|---|---|---|
> | `@type` | string | Fixed | Always `"sas:AlignmentConfiguration"` |
> | `sas:consensusThreshold` | number | `SASConfig.consensusThreshold` | The threshold used for this invocation. JSON number (not string). |
> | `sas:minObservationThreshold` | integer | `SASConfig.minObservationThreshold` | The observation floor used for this invocation. |
> | `sas:nullVocabulary` | array of string | Merged from `SASConfig.nullVocabulary` and `SASConfig.globalNullVocabulary` | The complete null vocabulary active for this invocation. Field-specific vocabularies are flattened: if `nullVocabulary` has `{"result": ["N/A"]}` and `globalNullVocabulary` has `["-"]`, the output is `["N/A", "-"]`. The flattened list is deduplicated (case-insensitive) and sorted lexicographically (case-sensitive, per JCS). If no null vocabulary was configured, emit an empty array `[]`. **Forward-compatibility note:** Flattening intentionally loses the field-name association. In Phase 1, only `globalNullVocabulary` is implemented, so no information is lost. When per-field vocabulary is implemented (v3.0), this property will be restructured to an array of `{ "sas:fieldName": "...", "sas:nullValues": [...] }` objects (mirroring the `sas:booleanPairs` pattern), and the flat array form will be deprecated. Until then, consumers needing per-field null vocabulary provenance must inspect the SAS-008 diagnostic on individual fields, which records which values were reclassified. |
> | `sas:booleanPairs` | array of object | `SASConfig.booleanFields` | See §2.3 below for the transformation. If no boolean fields were configured, emit an empty array `[]`. |
> | `sas:temporalNamePattern` | string | `SASConfig.temporalNamePattern` | The regex source string (without delimiters or flags). E.g., `"(?:date|time|timestamp|...)"`, not `"/(?:date|time|timestamp|...)/i"`. The `i` (case-insensitive) flag is always implied and not serialized. Case-insensitive matching is a fixed property of temporal name detection (§6.2), not a configurable flag — no SAS version supports case-sensitive temporal name patterns. If a future version requires case-sensitive patterns, this property's contract will be revised with a breaking change notice. |
>
> **Placement:** The `sas:activeConfig` block is a direct property of the `viz:DatasetSchema` root object, at the same level as `viz:hasField`, `sas:fandawsAvailable`, and `sas:alignmentMode`. It is serialized after the schema-level metadata properties and before `viz:hasField`, per JCS key ordering.

### 2.3 `booleanFields` → `booleanPairs` Serialization (amends §7)

The `SASConfig.booleanFields` property is typed as `Record<string, [string, string]>` — a map from field name to a two-element tuple of `[trueValue, falseValue]`. The output serialization transforms this to an array of objects under the key `sas:booleanPairs`.

**Transformation rule:**

```
Input (SASConfig):
  booleanFields: {
    "is_active": ["Y", "N"],
    "has_insurance": ["TRUE", "FALSE"]
  }

Output (sas:activeConfig):
  "sas:booleanPairs": [
    { "sas:fieldName": "has_insurance", "sas:trueValue": "TRUE", "sas:falseValue": "FALSE" },
    { "sas:fieldName": "is_active", "sas:trueValue": "Y", "sas:falseValue": "N" }
  ]
```

**Ordering:** The array is sorted lexicographically by `sas:fieldName` (case-sensitive, per JCS). This ensures deterministic serialization regardless of the `Record` iteration order in the caller's runtime.

**Object keys within each entry** are sorted per JCS: `sas:falseValue`, `sas:fieldName`, `sas:trueValue` (lexicographic).

**Naming rationale:** The config property is named `booleanFields` (a map keyed by field name) because it is an input lookup structure. The output property is named `booleanPairs` (an array of value-pair objects) because it is a serialized record of what was applied. The structural transformation (record → sorted array) is required by the determinism contract (§2.2): JavaScript `Record` iteration order is insertion-order-dependent, which is non-deterministic across callers.

### 2.4 Amendment to §5.2

**Insert** the `sas:activeConfig` block into the §5.2 example, after `"sas:alignmentMode": "enriched"` and before `"viz:hasField": [ ]`:

```json
"sas:activeConfig": {
  "@type": "sas:AlignmentConfiguration",
  "sas:consensusThreshold": 0.95,
  "sas:minObservationThreshold": 5,
  "sas:nullVocabulary": [],
  "sas:booleanPairs": [],
  "sas:temporalNamePattern": "(?:date|time|timestamp|created|updated|modified|born|died|started|ended|expires?)(?:_at|_on|_time)?$"
}
```

**Add to the schema-level metadata semantics list:**

> - `sas:activeConfig` — the complete alignment configuration snapshot used for this invocation. See §5.6. Always present. All five properties are always present, even when defaults are used. This enables any consumer to determine whether non-default configuration was active without requiring out-of-band knowledge of the default values.

---

## 3. Conditional Property Emission Clarification (amends §5.3)

### 3.1 Problem

The §5.3 conditional properties table says `sas:fandawsConsulted` is conditional on "Fandaws scope was provided," but the Phase 1 implementation always emits it (as `false` in standalone mode). The §5.4 epistemic distinction implies `fandawsConsulted` should always be present so that the absent-vs-unmatched distinction is always observable. Additionally, `viz:wasNormalized` and `viz:wasPercentage` emission rules for the no-SNP-manifest case are unspecified.

### 3.2 Revised Conditional Properties Table

**Replace** the §5.3 conditional properties table with:

**Always-present properties** (emitted on every `viz:DataField`, including standalone mode):

| Property | Type | Standalone Value | Description |
|---|---|---|---|
| `sas:fandawsConsulted` | boolean | `false` | Whether Fandaws was queried for this field. Always emitted. `false` when no `FandawsScope` was provided; `true` when a scope was provided (regardless of match result). This enables the §5.4 epistemic distinction without requiring consumers to infer from property absence. |

**Conditionally-present properties** (omitted entirely when their trigger condition is not met):

| Property | Condition | Omission Semantics |
|---|---|---|
| `viz:numericPrecision` | DataType is `viz:QuantitativeType` | Field is not quantitative; precision is inapplicable. |
| `viz:wasNormalized` | SNP manifest was provided AND manifest contains an entry for this field | No SNP manifest was provided, OR this field was not affected by normalization. Omission means "we don't know" or "not applicable" — NOT "was not normalized." |
| `viz:wasPercentage` | SNP manifest was provided AND manifest records percentage stripping for this field | Same as `viz:wasNormalized`. |
| `sas:fandawsMatch` | `sas:fandawsConsulted` is `true` | Fandaws was not consulted; no match status is available. When consulted but no match: property is present with value `null` (per §5.4). |
| `sas:fandawsEpistemicStatus` | `sas:fandawsMatch` is non-null | No Fandaws concept was matched. |
| `sas:fandawsOverride` | Fandaws overrode the static classification | No override occurred. |
| `sas:fandawsOverrideReason` | `sas:fandawsOverride` is `true` | No override; no reason to report. |
| `sas:fandawsOverrideStrength` | Fandaws produced a soft override (§6.7.5, imported concept with consensus ≤ 0.99) | No soft override occurred. Value when present: `"advisory"`. Hard overrides do not carry this property — they are unconditional. |
| `sas:fandawsSuggestion` | Imported concept contradicts high-confidence structural evidence (§6.7.5, consensus > 0.99) | No suggestion case. |
| `sas:metricHint` | Fandaws concept has `fandaws:metricAlignment` property | No metric alignment found. Pipeline-internal only (§6.7.6). |

### 3.3 Amendment to §5.4

**Replace** the opening of §5.4 ("When Fandaws is available but returns no concept match for a field, the output carries:") with:

> `sas:fandawsConsulted` is always present on every `viz:DataField`. The §5.4 epistemic distinction is encoded as follows:
>
> **Fandaws not available** (standalone mode):
> ```json
> "sas:fandawsConsulted": false
> ```
> All other Fandaws properties (`sas:fandawsMatch`, `sas:fandawsEpistemicStatus`, etc.) are omitted.
>
> **Fandaws available, no concept match:**
> ```json
> "sas:fandawsConsulted": true,
> "sas:fandawsMatch": null
> ```
> `sas:fandawsMatch` is present and explicitly `null`. All downstream Fandaws properties are omitted.
>
> **Fandaws available, concept matched:**
> ```json
> "sas:fandawsConsulted": true,
> "sas:fandawsMatch": "fandaws:concept/revenue",
> "sas:fandawsEpistemicStatus": "committed"
> ```
> Additional Fandaws properties are present per the conditional table in §5.3.

### 3.4 New Property: `sas:fandawsOverrideStrength` (amends §5.3, §6.7.5)

The §6.7.5 epistemic matrix references `sas:fandawsOverrideStrength: "advisory"` for soft overrides, but this property was not listed in §5.3. It is now formally registered.

**Definition:** `sas:fandawsOverrideStrength` is a string property on `viz:DataField` that qualifies how strongly a Fandaws enrichment override should be treated. Present only when an imported (not committed) Fandaws concept produces a soft override per §6.7.5.

**Known values:**

| Value | Condition | Meaning |
|---|---|---|
| `"advisory"` | Imported concept overrides static classification where consensus ≤ 0.99 or the static type is a fallback | The override is provisional. The imported concept has not been validated through the semantic firewall. Consumers SHOULD present this override to users with appropriate uncertainty indicators. |

**Not emitted when:**

- The Fandaws concept is `committed` (hard override — no qualifier needed; committed concepts are fully authoritative).
- No Fandaws override occurred.
- The imported concept was recorded as a suggestion only (consensus > 0.99; no override, therefore no strength to qualify).

---

## 4. ADR Incorporations

### 4.1 ADR-006: Consensus Tie-Breaking (amends §6.1)

**Problem:** §6.1 says "the type that passes the threshold" but does not specify behavior when multiple types pass the threshold simultaneously (a tie).

**Insert after** the paragraph beginning "If any non-null type `T` passes the integer threshold check:" in §6.1:

> **Tie-breaking (when multiple types pass):** If two or more non-null types independently pass the integer threshold check, select the type with the highest `typeDistribution` count. If counts are also equal, select the type that is **widest** in the following lattice order: `null < boolean < integer < number < string`. The lattice widens toward string because string is the universal fallback — it can represent any value. This ensures determinism: given identical counts and identical threshold passage, the wider type wins.
>
> In practice, ties at threshold are rare. A threshold of 0.95 requires 95% consensus. For two types to both achieve 95%, the dataset would need to have fewer than ~11 non-null values (since `ceil(0.95 * 10) = 10`, allowing at most one minority). The tie-breaker is a corner-case safety net, not a common path.
>
> **Design trade-off:** The widening lattice favors structural safety over semantic specificity. In a tie between `integer` and `boolean`, the wider type (`integer`) wins — which preserves numeric operations at the cost of losing boolean semantics. This is deliberate: SAS's governing principle §2.4 (Semantic Honesty) holds that when evidence is ambiguous, the interpretation that loses less information is preferred. String can represent anything; narrower types cannot represent arbitrary strings. Widening preserves data fidelity; narrowing risks silent data loss. If the caller needs the narrower interpretation, they can provide it via `SASConfig.booleanFields` (§6.3) or Fandaws enrichment (§6.7), both of which take precedence over the tie-breaker.

### 4.2 ADR-007: SNP Manifest Field Matching (amends §6.2)

**Problem:** §4.2 says "annotate output fields with normalization provenance" but does not specify which manifest field to match on.

**Insert into §6.2**, after "If SNP v1.3 §4.7 converted dates in this field (manifest records `date_converted` entries for this path): assign `viz:TemporalType` regardless of name matching.":

> **Manifest matching key:** SAS matches SNP manifest entries to CISM fields using the `detail.type` field of the manifest entry, not the `rule` field. Rationale: the `rule` field is the SNP rule name (e.g., `"date_format_normalization"`), which is a pipeline-internal identifier. The `detail.type` field records the semantic observation (e.g., `"date_converted"`), which is the datum SAS needs. Specifically, an SNP manifest entry triggers temporal detection via SNP evidence when `entry.detail.type === "date_converted"` AND `entry.path` matches the CISM `SchemaEdge.name` (case-insensitive).
>
> **Additional SNP-sourced annotations:** SAS matches manifest entries for `viz:wasNormalized` and `viz:wasPercentage` using the same key:
>
> - `detail.type === "currency_stripped"` → set `viz:wasNormalized: true` on the matched field.
> - `detail.type === "percent_stripped"` → set `viz:wasPercentage: true` on the matched field.
>
> **Note:** `detail.type === "date_converted"` triggers `temporal-detection-snp-evidence` (above) but does NOT set `viz:wasNormalized`. The `wasNormalized` flag tracks formatting artifact removal (currency symbols, thousands separators, trailing percent signs) where raw cell values were modified to reveal underlying numbers. Date conversion is a structurally different operation — SNP transforms a date string from one format to another (e.g., "Jan 15, 2024" → "2024-01-15") — and is tracked by the `temporal-detection-snp-evidence` rule name and the SAS-009 diagnostic. Conflating these two operations would muddy the `wasNormalized` flag's semantics.

### 4.3 ADR-009: Array Root `totalRows` (amends §5.2)

**Problem:** §5.2 says `viz:totalRows` is "sourced from the CISM root array node's `occurrences` field" — but for CSV/tabular data, the CISM root is an array node whose `occurrences` is 1 (the array itself). The row count is `root.itemType.occurrences`.

**Replace** the first bullet of the §5.2 schema-level metadata semantics:

~~`- viz:totalRows — total row count in the dataset. Sourced from the CISM root array node's occurrences field (for CSV/tabular data) or from the CISM sampling.inputSize if sampling was applied.`~~

**With:**

> - `viz:totalRows` — total row count in the dataset. Sourcing depends on CISM root structure:
>   - **Array root** (CSV/tabular data): `root.itemType.occurrences`. The root array node's own `occurrences` field is 1 (a single array); the row count is carried by the `itemType` node.
>   - **Object root** (JSON single-document): `root.occurrences` (always 1 for a single object).
>   - **If `CISMRoot.sampling` is present and `sampling.applied` is `true`:** `viz:totalRows` is sourced from `sampling.inputSize` regardless of root structure. This is the pre-sampling total.

### 4.4 ADR-010: `sas:activeConfig` as Required Output (amends §5.1, §5.2)

**Problem:** The `sas:activeConfig` block was added during Phase 1 implementation but is not mentioned in v2.0.

This ADR is fully addressed by §2 of this addendum (new §5.6). No further amendment is needed beyond cross-referencing.

**Insert into the §5.1 `SASResult` schema description** (after the `diagnostics` field):

> The `schema` field, when present, always includes `sas:activeConfig` (§5.6). Consumers can inspect this block to determine whether non-default configuration was active.

---

## 5. FBO Integration Alignment — `sas:alignmentMode` Correction

### 5.1 Problem

The FBO TBox `fbo:hasAlignmentMode` comment listed known values as `'standalone', 'full-pipeline'`. The actual kernel values are `'standalone', 'enriched'` (per `transform.ts:173`). The v2.0 spec (§5.2) correctly uses `"enriched"`, so this is a TTL-only correction, but it should be noted here for cross-reference.

### 5.2 Confirmation

SAS v2.0 §5.2 is correct as written: `sas:alignmentMode` has exactly two known values:

| Value | Condition |
|---|---|
| `"standalone"` | No `FandawsScope` was provided (`sas:fandawsAvailable: false`) |
| `"enriched"` | A `FandawsScope` was provided (`sas:fandawsAvailable: true`) |

The value `"full-pipeline"` does not exist and has never been emitted by any SAS version. The FBO team should update the `rdfs:comment` on `fbo:hasAlignmentMode` (BridgeOntology.ttl line 948).

---

## 6. Updated Term Registry Counts

The kernel code audit identified 6 additional SAS output terms not exercised in the original 6 SME test outputs. These terms are conditional on optional inputs (SNP manifest, CISM sampling, boolean pair config) that were not present in the test fixtures.

### 6.1 New Terms

| Registry # | SAS Term | Condition | FBO Mapping |
|---|---|---|---|
| V16 | `viz:wasNormalized` | SNP manifest present, field affected | `fbo:wasNormalized` (annotation property) |
| V17 | `viz:wasPercentage` | SNP manifest present, percentage stripped | `fbo:wasPercentage` (annotation property) |
| V18 | `viz:rowsInspected` | CISM `sampling.applied` is `true` | `fbo:hasRowsInspected` (data property) |
| S15 | `sas:fieldName` (in booleanPairs) | Boolean pairs configured | `fbo:forFieldName` (data property on BooleanPairMapping) |
| S16 | `sas:trueValue` | Boolean pairs configured | `fbo:hasTrueValue` (data property on BooleanPairMapping) |
| S17 | `sas:falseValue` | Boolean pairs configured | `fbo:hasFalseValue` (data property on BooleanPairMapping) |

### 6.2 Updated Totals

| Category | v2.0 | v2.1 |
|---|---|---|
| `viz:` terms | 15 | 18 |
| `sas:` terms | 14 | 17 |
| Total registry entries | 29 | 35 |
| Mapped in FBO TBox | 29 | 35 |
| FBO gaps | 0 | 0 |

---

## 7. Testing Contract Additions (amends §13.2)

### 7.1 New Required Test Cases

The following test cases are added to §13.2 to cover the gaps identified in this addendum.

**T-15: `sas:activeConfig` presence (standalone)**

Input: Flat CISM, no SNP manifest, no Fandaws scope, default config.
Expected: `sas:activeConfig` present with all 5 properties at default values. `sas:booleanPairs` is `[]`. `sas:nullVocabulary` is `[]`.

**T-16: `sas:activeConfig` presence (custom config)**

Input: Flat CISM, custom config with `consensusThreshold: 0.8`, `booleanFields: { "active": ["Y", "N"] }`, `nullVocabulary: { "status": ["N/A"] }`, `globalNullVocabulary: ["-"]`.
Expected: `sas:activeConfig` present. `sas:consensusThreshold: 0.8`. `sas:booleanPairs` is `[{ "sas:falseValue": "N", "sas:fieldName": "active", "sas:trueValue": "Y" }]` (JCS key order). `sas:nullVocabulary` is `["-", "N/A"]` (deduplicated, sorted).

**T-17: `booleanPairs` serialization ordering**

Input: Config with `booleanFields: { "z_field": ["T", "F"], "a_field": ["1", "0"] }`.
Expected: `sas:booleanPairs` array sorted by `sas:fieldName`: `a_field` before `z_field`. Object keys within each entry in JCS order: `sas:falseValue`, `sas:fieldName`, `sas:trueValue`.

**T-18: `cism-validation-failed` rule assignment**

Input: CISM with `occurrences: 100`, `typeDistribution: { "integer": 60, "string": 50 }` (sum 110 > occurrences).
Expected: Field assigned `viz:UnknownType`, `sas:alignmentRule: "cism-validation-failed"`, `viz:consensusScore: "0.000000"`, `sas:consensusNumerator: 0`, `sas:consensusDenominator: 0`, diagnostic SAS-013.

**T-19: `temporal-detection-snp-evidence` rule assignment**

Input: CISM with field "order_id" (name does NOT match temporal pattern), `primitiveType: "string"`. SNP manifest includes `{ "path": "order_id", "detail": { "type": "date_converted" } }`.
Expected: Field assigned `viz:TemporalType`, `sas:alignmentRule: "temporal-detection-snp-evidence"`, diagnostic SAS-009. `viz:wasNormalized` is NOT present (date conversion is tracked by the rule name and diagnostic, not by the normalization flag — see §4.2 note).

**T-20: `structural-passthrough` after null vocabulary exhaustion**

Input: CISM with field "status", `primitiveType: "string"`, `typeDistribution: { "string": 10 }`, `occurrences: 10`. Config with `nullVocabulary: { "status": ["N/A", "none", "-", "null", "unknown", "na", "not available", "n/a", "pending", "tbd"] }` covering all 10 values.
Expected: After reclassification, `nonNullTotal = 0`. Field assigned `viz:UnknownType` (not per-`primitiveType` NominalType — zero remaining observations provide no type evidence), `sas:alignmentRule: "structural-passthrough"` (not `"unknown-assignment"` — this is SAS-layer reclassification, not a CISM-level empty field), `viz:consensusScore: "0.000000"`, `sas:consensusNumerator: 0`, `sas:consensusDenominator: 0`, diagnostic SAS-008 with `reclassifiedCount: 10`. Distinguished from `cism-validation-failed` by diagnostic (SAS-008, not SAS-013) and rule name. Distinguished from `unknown-assignment` by rule name (`"structural-passthrough"`, not `"unknown-assignment"`) and diagnostic (SAS-008, not SAS-002).

**T-21: `sas:fandawsConsulted` always present (standalone)**

Input: Flat CISM, no Fandaws scope.
Expected: Every `viz:DataField` in output carries `sas:fandawsConsulted: false`. The property is present, not omitted.

**T-22: Consensus tie-breaking (ADR-006)**

Input: CISM with `typeDistribution: { "integer": 5, "string": 5 }`, `occurrences: 10`, `consensusThreshold: 0.5`.
Expected: Both types pass threshold (5/10 = 0.5 ≥ 0.5). Counts are equal. Lattice widens: string > integer → field assigned `viz:NominalType`, `sas:alignmentRule: "consensus-promotion"`.

### 7.2 New Property-Based Invariant

**Add to §13.3:**

> **P-10: activeConfig completeness** — For every `SASResult` with `status: "ok"`, `schema.sas:activeConfig` is present, `@type` is `"sas:AlignmentConfiguration"`, and all 5 required properties (`sas:consensusThreshold`, `sas:minObservationThreshold`, `sas:nullVocabulary`, `sas:booleanPairs`, `sas:temporalNamePattern`) are present with their correct types.
>
> **P-11: fandawsConsulted universality** — For every `viz:DataField` in the output, `sas:fandawsConsulted` is present and is a boolean. No field omits this property.

---

## 8. Appendix B Amendment — Updated Output Example

**Replace** the Appendix B SAS Output block to include `sas:activeConfig` and the `sas:fandawsConsulted: true/false` on every field:

```json
{
  "@context": {
    "viz": "https://schema.fnsr.dev/ecve/v4#",
    "sas": "https://schema.fnsr.dev/sas/v1#",
    "fandaws": "https://schema.fnsr.dev/fandaws/v3#"
  },
  "@type": "viz:DatasetSchema",
  "viz:rawInputHash": "sha256:abc123...",
  "viz:totalRows": 500,
  "sas:fandawsAvailable": true,
  "sas:alignmentMode": "enriched",
  "sas:activeConfig": {
    "@type": "sas:AlignmentConfiguration",
    "sas:consensusThreshold": 0.95,
    "sas:minObservationThreshold": 5,
    "sas:nullVocabulary": [],
    "sas:booleanPairs": [],
    "sas:temporalNamePattern": "(?:date|time|timestamp|created|updated|modified|born|died|started|ended|expires?)(?:_at|_on|_time)?$"
  },
  "viz:hasField": [
    {
      "@id": "viz:field/region",
      "@type": "viz:DataField",
      "viz:fieldName": "Region",
      "viz:hasDataType": { "@id": "viz:NominalType" },
      "viz:consensusScore": "1.000000",
      "sas:consensusNumerator": 500,
      "sas:consensusDenominator": 500,
      "sas:alignmentRule": "structural-passthrough",
      "sas:structuralType": "string",
      "sas:fandawsConsulted": true,
      "sas:fandawsMatch": null
    },
    {
      "@id": "viz:field/revenue",
      "@type": "viz:DataField",
      "viz:fieldName": "Revenue",
      "viz:hasDataType": { "@id": "viz:QuantitativeType" },
      "viz:numericPrecision": "integer",
      "viz:consensusScore": "0.989939",
      "sas:consensusNumerator": 492,
      "sas:consensusDenominator": 497,
      "viz:wasNormalized": true,
      "sas:alignmentRule": "consensus-promotion",
      "sas:structuralType": "string",
      "sas:fandawsConsulted": true,
      "sas:fandawsMatch": "fandaws:concept/revenue",
      "sas:fandawsEpistemicStatus": "committed"
    },
    {
      "@id": "viz:field/created-at",
      "@type": "viz:DataField",
      "viz:fieldName": "created_at",
      "viz:hasDataType": { "@id": "viz:TemporalType" },
      "viz:consensusScore": "1.000000",
      "sas:consensusNumerator": 500,
      "sas:consensusDenominator": 500,
      "sas:alignmentRule": "temporal-detection",
      "sas:structuralType": "string",
      "sas:fandawsConsulted": true,
      "sas:fandawsMatch": null
    }
  ]
}
```

**Changes from v2.0 Appendix B:**

1. `sas:activeConfig` block added after `sas:alignmentMode`.
2. Every field now carries `sas:fandawsConsulted` (was already present in v2.0 example, now normatively required).
3. `sas:fandawsMatch: null` explicitly present on Region and created_at (was already present in v2.0 example, now normatively required per §5.4 revision).

---

## 9. Amendments to Appendix A — Rule Precedence Table

**Replace** the Appendix A table to add the `sas:alignmentRule` value column and the `cism-validation-failed` pre-check:

| Priority | Rule | Source | Condition | Output DataType | `sas:alignmentRule` |
|---|---|---|---|---|---|
| 0 | CISM validation (§6.1.3) | Pre-check | Structural invariant violation | `UnknownType` | `cism-validation-failed` |
| 1 | Fandaws type override (§6.7.2) | Enrichment | Fandaws concept has type guidance | Per Fandaws concept | `fandaws-override` |
| 2 | Fandaws type veto (§6.7.3) | Enrichment | Fandaws vetoes a static classification | Reverts to Nominal | `fandaws-override` |
| 3 | Fandaws boolean pair (§6.3) | Enrichment | Fandaws identifies boolean domain meaning | `BooleanType` | `boolean-pair-fandaws` |
| 4 | Fandaws null vocabulary (§6.4) | Enrichment | Fandaws provides null-equivalent values | Per reclassified consensus | `null-vocabulary-fandaws` |
| 5 | Consensus promotion (§6.1) | Static core | Consensus evaluation entered (3 sub-cases — see §1.2) | Per sub-case: winner type, UnknownType, or NominalType | `consensus-promotion` |
| 6 | Temporal (SNP evidence) (§6.2) | Static core | SNP manifest has `date_converted` entries | `TemporalType` | `temporal-detection-snp-evidence` |
| 7 | Temporal (name match) (§6.2) | Static core | Field name matches temporal pattern | `TemporalType` | `temporal-detection` |
| 8 | Boolean pair (configured) (§6.3) | Static core | Field in `booleanFields` config | `BooleanType` | `boolean-pair-configured` |
| 9 | Null vocabulary reclassify (§6.4) | Static core | Null vocab shifts consensus winner | Per reclassified consensus | `null-vocabulary-configured` |
| 10 | Structural pass-through (§6.5) | Static core | No prior rule matched | Per §6.1.1 mapping; `UnknownType` if null exhaustion (§1.5) | `structural-passthrough` |
| 11 | Unknown assignment (§6.6) | Static core | All-null or union node | `UnknownType` | `unknown-assignment` |

**Note:** Priority 0 (`cism-validation-failed`) is a pre-check, not a rule in the cascade. It runs during §6.1.3 validation before the cascade begins. If it fires, the cascade is skipped entirely for that field.

---

## Appendix F — Changelog (v2.0 → v2.1)

| Change | Sections Affected | Description |
|---|---|---|
| **Exhaustive alignment rule registry** | §6, §6.1.3, §6.2, §6.5, §6.7.2, new Appendix F | All 8 static + 3 enrichment `sas:alignmentRule` values enumerated with trigger conditions, assigned types, diagnostic codes, and consensus score semantics. `consensus-promotion` documented with 3 sub-cases (success, min-obs failure, no-consensus) matching kernel behavior at transform.ts:737/776/793. Null vocabulary exhaustion edge case (§6.5) assigns `viz:UnknownType` via `structural-passthrough` (matching kernel transform.ts:447-455), not per-`primitiveType` mapping — zero remaining observations provide no type evidence. SAS-008 diagnostic distinguishes this from validation failure (SAS-013) and CISM-level empty fields (SAS-002). Closes the FBO `fbo:producedByRule` documentation gap. |
| **`sas:activeConfig` output structure** | New §5.6, §5.1, §5.2, §7, Appendix B | Defined serialization format, all 5 required properties, `booleanFields` → `booleanPairs` transformation rule, JCS ordering. `sas:nullVocabulary` flattened array documented as intentional for Phase 1, with forward-compatibility note for v3.0 restructuring to per-field `{ fieldName, nullValues }` objects. Incorporates ADR-010. |
| **Conditional property emission** | §5.3, §5.4 | `sas:fandawsConsulted` promoted from conditional to always-present. Emission rules for `viz:wasNormalized`, `viz:wasPercentage` clarified: omitted when no SNP manifest, not set to `false`. `sas:fandawsOverrideStrength` formally registered. |
| **ADR-006: Consensus tie-breaking** | §6.1 | Widening lattice tie-breaker: when multiple types pass threshold with equal counts, the wider type wins (`null < boolean < integer < number < string`). Explicitly documents the structural-safety-over-semantic-specificity trade-off. |
| **ADR-007: SNP manifest matching** | §6.2 | Match on `detail.type` field, not `rule` field. Explicit matching keys: `date_converted` (temporal detection only — does NOT set `wasNormalized`), `currency_stripped` (sets `wasNormalized`), `percent_stripped` (sets `wasPercentage`). Date conversion is a structurally different operation from formatting artifact removal; `wasNormalized` tracks only the latter. |
| **ADR-009: Array root totalRows** | §5.2 | Use `root.itemType.occurrences` for array roots, not `root.occurrences`. |
| **`sas:alignmentMode` value correction** | §5.2 (confirmation only) | Confirmed values are `"standalone"` and `"enriched"`. `"full-pipeline"` never existed. FBO TTL comment correction requested. |
| **Rule precedence table** | Appendix A | Added `sas:alignmentRule` column, `cism-validation-failed` pre-check at priority 0, and Fandaws enrichment rule names. |
| **8 new test cases** | §13.2, §13.3 | T-15 through T-22 covering `activeConfig`, `cism-validation-failed`, SNP evidence, null vocabulary exhaustion, `fandawsConsulted` universality, and tie-breaking. P-10 and P-11 property invariants. |
| **Term registry expansion** | New §6 (this addendum) | 6 conditional terms (V16–V18, S15–S17) added. Total: 35 terms, all mapped in FBO TBox. |

---

*End of addendum.*
