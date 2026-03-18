# Schema Alignment Service (SAS)

## Technical Specification — Version 2.0

|Field                        |Value                          |
|-----------------------------|-------------------------------|
|**Status**                   |Final Review Draft             |
|**Author**                   |Aaron                          |
|**Date**                     |2026-03-01                     |
|**Supersedes**               |SAS v1.2 (2026-03-01)         |
|**FNSR Component**           |Semantic Interpretation Layer  |
|**Edge-Canonical Compliance**|Full                           |
|**Canonical Representation** |JSON-LD (output only)          |

-----

## 1. Purpose

The Schema Alignment Service (SAS) is a deterministic, fully client-side semantic interpretation engine. It accepts a Canonical Internal Schema Model (CISM) from BIBSS v1.3 and produces a `viz:DatasetSchema` JSON-LD graph for consumption by the ECVE pipeline.

SAS is the **judgment layer** — the single point in the pipeline where structural evidence meets semantic interpretation. BIBSS observes that a column contains strings. SAS decides whether those strings are dates, categories, coded identifiers, or boolean encodings. BIBSS accumulates `typeDistribution` counts. SAS applies consensus thresholds to override the lattice's worst-case type. BIBSS is mechanical. SAS is interpretive.

**Architectural position:**

```
SNP (format cleaning) → BIBSS (structural inference) → SAS (semantic interpretation) → ECVE (visualization)
```

SAS is the only service that spans the structural-to-semantic boundary. Everything upstream (SNP, BIBSS) is deterministic and domain-agnostic. Everything downstream (ECVE metric evaluation, reasoning, rendering) consumes semantic types. SAS translates between these worlds.

**The Fandaws principle:** SAS operates in two modes — **standalone** (static rules only) and **enriched** (static rules plus Fandaws domain intelligence). Standalone mode must produce correct, complete output for any input. Enriched mode produces *better* output — more accurate type promotions, domain-aware coercion decisions, ontologically grounded field-to-concept alignments — but is never required. SAS works without Fandaws. SAS works better with Fandaws.

-----

## 2. Governing Principles

### 2.1 Edge-Canonical Execution

SAS is a pure function. It executes entirely within a standards-compliant browser or local Node.js environment. It requires zero background workers, databases, or service registries. The Fandaws enrichment layer queries in-memory knowledge graphs loaded by the caller — it does not make network requests.

### 2.2 Determinism Contract

Given identical CISM input, identical configuration, and identical Fandaws scope content (or absence thereof), SAS **must** produce byte-identical `viz:DatasetSchema` output across all runtimes (Node.js versions, browser engines). All regex patterns are statically defined. The consensus threshold is evaluated using integer arithmetic (§6.1). Fandaws queries are deterministic graph traversals over immutable scope data. Output serialization follows the canonical rules in §2.6.

This contract requires three things to hold simultaneously: (a) the processing algorithm is deterministic, (b) numeric comparisons avoid floating-point ambiguity, and (c) the output serializer produces identical bytes. Each is addressed in its own section.

### 2.3 Structural Purity of Input

SAS trusts the CISM unconditionally. It does not re-parse the raw data, re-infer types, or second-guess BIBSS's structural observations. The `typeDistribution` field on CISM nodes is the evidentiary basis for SAS's decisions. If BIBSS says 95 values were integer and 3 were string, SAS uses those numbers — it does not re-scan the CSV to verify.

### 2.4 Semantic Honesty

SAS documents every judgment it makes. Each `viz:DataField` in the output carries metadata recording which rule or Fandaws query produced its type assignment, the confidence of that assignment, and whether Fandaws was consulted. Downstream consumers can distinguish "SAS classified this as Temporal because it matched a regex" from "SAS classified this as Nominal because Fandaws identified it as a coded identifier."

### 2.5 Graceful Degradation

If Fandaws is unavailable (not configured, scope not loaded, or query returns no match), SAS falls back to static rules without error. The output is valid and complete. The only difference is the absence of enrichment annotations. SAS never fails because Fandaws is absent.

### 2.6 Serialization & Canonicalization

SAS guarantees byte-identical output by producing a canonical in-memory JSON object with deterministic ordering and numeric formatting, then serializing to bytes using the JSON Canonicalization Scheme (JCS, RFC 8785). The following conventions are normative:

**Key ordering:** All JSON objects in the output have keys sorted lexicographically (Unicode code point order, per JCS). This includes the top-level `@context` object, each `viz:DataField` object, and all nested objects. Implementations must not rely on insertion-order preservation.

**Array ordering:** The `viz:hasField` array preserves CISM `SchemaEdge` order — that is, fields appear in the same order as the properties on the CISM root object node. This is the source-of-truth ordering. If the CISM does not guarantee property order (unlikely for well-formed BIBSS output), the fallback is lexicographic sort by `@id`.

**Numeric formatting:** The `viz:consensusScore` field is emitted as a **JSON string** containing exactly 6 fractional digits, rounded using the IEEE 754 "round half to even" (banker's rounding) rule. For example, a raw ratio of `492/497` produces `"0.989939"` (not a JSON number). This design choice is deliberate: standard JSON serializers (`JSON.stringify`, `json.dumps`) cannot guarantee trailing zeros or fixed decimal places on numeric literals — `1.000000` becomes `1`, breaking byte-identity. A string representation is fully deterministic under JCS without requiring a custom emitter.

The **authoritative values** for programmatic comparison are the exact integer companion fields:

- `sas:consensusNumerator` — integer count of values matching the assigned type.
- `sas:consensusDenominator` — integer `nonNullTotal` used as the divisor.

These are JSON numbers (integers). The string `viz:consensusScore` is the display/comparison value for human consumption and UI rendering; the numerator/denominator pair is the machine-readable audit trail. Threshold comparisons within SAS itself use integer arithmetic (§6.1) and never parse `viz:consensusScore`.

**Implementation note:** To produce the string, compute `(numerator / denominator).toFixed(6)` or equivalent in the implementation language. The result is always a string of the form `"X.YYYYYY"` where `YYYYYY` is exactly 6 digits. For `denominator === 0` (all-null field), emit `"0.000000"` with `numerator: 0, denominator: 0`.

**Boolean values:** `true` and `false` are serialized as JSON literals (not strings).

**Null handling:** JSON `null` is used for explicitly-null properties (e.g., `sas:fandawsMatch: null`). Properties that are absent (not applicable) are omitted entirely, never set to `null`.

**Final serialization:** The implementation must produce output bytes equivalent to `JSON.stringify` applied to a key-sorted object tree with the consensusScore string formatting above. JCS (RFC 8785) is the normative standard. Implementations may use any method that produces JCS-equivalent bytes.

**JSON-LD vs JCS interplay:** The JCS-canonicalized bytes are the **authoritative interchange form** for determinism verification (provenance chain, hash comparison, cross-runtime tests). JSON-LD semantic operations (expand, compact, frame) may reorder keys or restructure the graph — output after such operations is **not** expected to be byte-identical to the canonical form. When consuming the schema as RDF, consumers should perform JSON-LD expansion as needed but must not expect byte equality after transformation. The `@context` key ordering (lexicographic per JCS) and the `viz:hasField` array ordering (CISM property order) are canonical only in the JCS-serialized form.

-----

## 3. Non-Goals (v2.0)

The following are explicitly out of scope:

- Natural-language interpretation of field names (beyond exact/normalized string matching)
- Machine learning or embedding-based field classification
- Data validation (testing values against a schema)
- Data transformation or coercion (SAS classifies; it does not modify values)
- Metric formula evaluation (ECVE's metric evaluator owns this)
- Ontology alignment (BFO/CCO mapping of SAS's own operations — deferred per FNSR-wide pattern)
- Schema diffing or drift detection
- Any form of rendering or visualization

-----

## 4. Input Contract

### 4.1 Primary Input: BIBSS CISM

SAS accepts a `CISMRoot` object as defined in BIBSS v1.3 §9.1. The CISM must be version 1.3 or later (the `typeDistribution` field is required).

```typescript
interface CISMRoot {
  version: string                    // "1.3" or later
  generatedAt: string                // ISO 8601
  config: InferConfig
  root: SchemaNode
  sampling?: {
    applied: boolean
    inputSize: number
    sampleSize: number
    strategy: "strided"
  }
}
```

SAS uses the following CISM fields:

- `SchemaNode.kind` — to distinguish objects, arrays, primitives, and unions.
- `SchemaNode.primitiveType` — the lattice-resolved structural type.
- `SchemaNode.typeDistribution` — pre-widening observation counts (the evidentiary basis for consensus).
- `SchemaNode.occurrences` — total observation count (denominator for consensus).
- `SchemaNode.nullable` — whether null values were observed.
- `SchemaNode.id` — RFC 6901 JSON Pointer path (used for field identity).
- `SchemaEdge.name` — property name (used for field naming and Fandaws concept matching).
- `SchemaEdge.required` — whether the field was present in all records.
- `SchemaEdge.occurrences` / `SchemaEdge.totalPopulation` — presence statistics.

### 4.2 Secondary Input: SNP Manifest (Optional)

SAS may receive the `ManifestEntry[]` from SNP v1.3 to annotate output fields with normalization provenance. If the manifest records that a field's values had currency symbols stripped, SAS sets `viz:wasNormalized: true` on the corresponding `viz:DataField`. If the manifest records percentage stripping, SAS sets `viz:wasPercentage: true`.

The manifest is optional. If absent, normalization annotations are omitted from the output.

### 4.3 Tertiary Input: Fandaws Scope (Optional)

SAS may receive a Fandaws scope providing domain knowledge for enriched alignment. The scope is accessed through a read-only query interface:

```typescript
interface FandawsScope {
  /**
   * Search for a concept by label.
   * Returns matching concepts from the scope hierarchy (context → user → global),
   * consistent with Fandaws v3.4 §3.2.7 ScopeResolver.
   * Returns empty array if no match.
   */
  resolveTerm(label: string): FandawsConcept[]

  /**
   * Check if a concept has a specific property or relationship.
   * Used for domain-aware type decisions (e.g., "is this concept a coded identifier?").
   */
  hasProperty(conceptId: string, propertyPath: string): boolean

  /**
   * Get a concept's properties.
   * Used for field-to-concept alignment annotations.
   */
  getConcept(conceptId: string): FandawsConcept | null

  /**
   * Check if a specific value has a concept mapping in the active scope.
   * Used for boolean pair veto (e.g., "does 'Y' map to a non-boolean concept?").
   */
  resolveValue(value: string): FandawsConcept | null
}

interface FandawsConcept {
  id: string                          // Fandaws IRI (e.g., "fandaws:concept/diagnostic_code")
  canonicalLabel: string              // Normalized label
  displayLabel: string                // Human-readable label
  epistemicStatus: "committed" | "imported"
  parentConcepts: string[]            // IS_A chain
  properties: Record<string, unknown> // Concept properties
  importedFrom?: string               // Original OWL IRI (for IVNE-imported concepts)
}
```

**Scope lifetime:** The `FandawsScope` is provided by the caller at invocation time. SAS holds no reference to it between invocations. SAS does not load, cache, or manage Fandaws knowledge graphs — it queries what the caller provides.

**Fandaws determinism contract:** All `FandawsScope` methods must be **synchronous**, **pure** (no side effects, no network calls, no I/O), and **stable** (identical inputs produce identical outputs across calls). SAS may call any method multiple times during a single `align` invocation and expects identical results each call. The `resolveTerm` method must return concepts in a deterministic priority order (context → user → global scope, then by concept `id` within the same scope level). SAS applies a final deterministic tie-breaker (§6.7.1) to guarantee stability even if the caller's ordering is imperfect.

**Synchronous-only contract:** SAS requires synchronous `FandawsScope` methods. The `align` function is synchronous and returns `SASResult` directly (not a `Promise`). If a caller provides a `FandawsScope` implementation whose methods return Promises or perform asynchronous operations, behavior is undefined. Callers with async data sources must resolve all data into an in-memory synchronous scope before invoking `align`.

**Fandaws property names used by SAS:** SAS inspects the following properties on `FandawsConcept.properties`. All property names are case-sensitive. All values must conform to the specified types.

|Property Name                |Expected Type         |Used In  |Description                                                                 |
|-----------------------------|----------------------|---------|----------------------------------------------------------------------------|
|`fandaws:nullEquivalentValues`|`string[]`           |§6.7.4   |Domain-specific null vocabulary. Values are compared case-insensitively.     |
|`fandaws:metricAlignment`    |`string` (IRI)        |§6.7.6   |Metric IRI for pre-matching hint. Must be a valid `viz:SemanticMetric` IRI. |
|`fandaws:dataTypeGuidance`   |`string`              |§6.7.2   |One of: `"coded-identifier"`, `"temporal"`, `"boolean-pair"`, `"quantity"`. Determines type override behavior.|
|`fandaws:unitOfMeasure`      |`string`              |§6.7.2   |Unit annotation for quantity types (e.g., `"USD"`, `"kg"`, `"percent"`).    |

If a property is absent or has an unexpected type, SAS ignores it (does not error) and proceeds as if the property were not present.

### 4.4 Metadata Input: Raw Input Hash

SAS receives the `viz:rawInputHash` (SHA-256 of the original raw bytes, computed by the caller before SNP ran) as a string parameter. This is propagated to the output `viz:DatasetSchema` for provenance chain continuity.

-----

## 5. Output Contract

### 5.1 Primary Output: `viz:DatasetSchema`

SAS produces a JSON-LD document conforming to the `viz:DatasetSchema` structure defined in ECVE v4.1 §5 and demonstrated in ECVE v4.1 Appendix C (lines 1698–1718).

```typescript
interface SASResult {
  /** Processing outcome. "ok" if no fatal diagnostics; "error" if validation failed. */
  status: "ok" | "error"

  /** The viz:DatasetSchema JSON-LD graph. Present when status is "ok". Absent when "error". */
  schema?: DatasetSchemaLD

  /** Structured diagnostic messages (always present, may be empty). */
  diagnostics: Diagnostic[]
}

interface Diagnostic {
  /** Machine-readable code (e.g., "SAS-001"). */
  code: string

  /** Severity level. "fatal" means align could not produce a schema. */
  level: "fatal" | "warning" | "info"

  /** Human-readable description of what happened. */
  message: string

  /** Suggested remediation or next step. */
  remediation: string

  /** Structured context fields specific to this diagnostic code. */
  context: Record<string, unknown>
}
```

**Error handling contract:** `align` **never throws** for expected inputs. All error conditions — including invalid CISM versions, structural inconsistencies, and malformed configuration — are reported as `Diagnostic` entries with appropriate severity.

**Schema-level vs field-level fatals:** A `fatal` diagnostic at the **schema level** (invalid CISM version, malformed root node structure) sets `status` to `"error"` and omits `schema` entirely — no fields can be processed. A `fatal` diagnostic at the **field level** (e.g., count mismatch on a single `SchemaNode`) marks that field as `viz:UnknownType` and records the diagnostic, but does **not** prevent schema emission. One bad column must not block all fields. The overall `status` remains `"ok"` unless a schema-level fatal occurred.

|Diagnostic Scope|Codes          |Effect on `status`|Effect on `schema`                         |
|----------------|---------------|------------------|-------------------------------------------|
|Schema-level    |SAS-007        |`"error"`         |Omitted entirely                           |
|Field-level     |SAS-013        |`"ok"` (unchanged)|Present; affected field is `viz:UnknownType`|

Callers must check `status` before consuming `schema`.

### 5.2 `viz:DatasetSchema` Structure

```json
{
  "@context": {
    "viz": "https://schema.fnsr.dev/ecve/v4#",
    "sas": "https://schema.fnsr.dev/sas/v1#",
    "fandaws": "https://schema.fnsr.dev/fandaws/v3#",
    "prov": "http://www.w3.org/ns/prov#"
  },
  "@type": "viz:DatasetSchema",
  "viz:rawInputHash": "sha256:...",
  "viz:rowsInspected": 100,
  "viz:totalRows": 500,
  "sas:fandawsAvailable": true,
  "sas:alignmentMode": "enriched",
  "viz:hasField": [ ]
}
```

**Schema-level metadata semantics:**

- `viz:totalRows` — total row count in the dataset. Sourced from the CISM root array node's `occurrences` field (for CSV/tabular data) or from the CISM `sampling.inputSize` if sampling was applied.
- `viz:rowsInspected` — number of rows actually observed by BIBSS. If `CISMRoot.sampling.applied` is `true`, this is `sampling.sampleSize`. If sampling was not applied (or the `sampling` field is absent), `viz:rowsInspected` equals `viz:totalRows`. If neither can be determined, `viz:rowsInspected` is omitted.
- `sas:fandawsAvailable` — `true` if a `FandawsScope` was provided to `align` (regardless of whether any field matched a concept). `false` if no scope was provided.
- `sas:alignmentMode` — `"enriched"` when `sas:fandawsAvailable` is `true`; `"standalone"` when `false`. This is a convenience alias — it carries no independent information beyond `sas:fandawsAvailable`.

### 5.3 `viz:DataField` Structure

Each field in the output carries:

```json
{
  "@id": "viz:field/revenue",
  "@type": "viz:DataField",
  "viz:fieldName": "Revenue",
  "viz:hasDataType": { "@id": "viz:QuantitativeType" },
  "viz:consensusScore": "0.989939",
  "sas:consensusNumerator": 492,
  "sas:consensusDenominator": 497,
  "viz:numericPrecision": "integer",
  "viz:wasNormalized": true,
  "viz:wasPercentage": false,
  "sas:alignmentRule": "consensus-promotion",
  "sas:structuralType": "string",
  "sas:fandawsConsulted": true,
  "sas:fandawsMatch": "fandaws:concept/revenue",
  "sas:fandawsEpistemicStatus": "committed"
}
```

**Required properties** (always present):

|Property              |Type       |Description                                                                                    |
|----------------------|-----------|-----------------------------------------------------------------------------------------------|
|`@id`                 |string     |Field IRI: `viz:field/{slug}` where `slug = normalizeFieldName(fieldName)` (see §5.5)          |
|`@type`               |string     |Always `"viz:DataField"`                                                                       |
|`viz:fieldName`       |string     |Original column/property name from the input data (unmodified)                                 |
|`viz:hasDataType`     |`@id`      |One of: `viz:QuantitativeType`, `viz:NominalType`, `viz:TemporalType`, `viz:BooleanType`, `viz:UnknownType`|
|`viz:consensusScore`  |string     |The proportion of non-null values that matched the assigned type, as a 6-decimal-place string (e.g., `"0.989939"`). See §2.6.|
|`sas:consensusNumerator`|integer  |Count of non-null values matching the assigned type (exact integer)                            |
|`sas:consensusDenominator`|integer|`nonNullTotal` used as divisor (exact integer). `viz:consensusScore = numerator / denominator` rounded to 6dp.|
|`sas:alignmentRule`   |string     |The rule that produced this assignment (see §6 rule names)                                     |
|`sas:structuralType`  |string     |The BIBSS `primitiveType` before SAS interpretation                                            |

**Conditional properties** (present when applicable):

|Property                     |Condition                    |Description                                                                |
|-----------------------------|-----------------------------|---------------------------------------------------------------------------|
|`viz:numericPrecision`       |DataType is Quantitative     |`"integer"` or `"float"` based on `typeDistribution` evidence              |
|`viz:wasNormalized`          |SNP manifest present         |`true` if SNP applied currency/formatting stripping to this field          |
|`viz:wasPercentage`          |SNP manifest present         |`true` if SNP stripped a trailing `%` from this field's values             |
|`sas:fandawsConsulted`       |Fandaws scope was provided   |`true` if Fandaws was queried for this field; `false` if scope unavailable |
|`sas:fandawsMatch`           |Fandaws returned a concept   |The Fandaws concept IRI that matched this field                            |
|`sas:fandawsEpistemicStatus` |Fandaws match exists         |`"committed"` or `"imported"` — the concept's epistemic status             |
|`sas:fandawsOverride`        |Fandaws overrode static rule |`true` when Fandaws contradicted the static classification                 |
|`sas:fandawsOverrideReason`  |Fandaws override occurred    |Human-readable explanation (e.g., `"Fandaws identifies 'Y' as chromosome Y, not boolean"`) |
|`sas:fandawsSuggestion`      |Imported concept vs. high consensus|`true` when an imported Fandaws concept contradicts high-confidence structural evidence (§6.7.5). Type assignment unchanged; concept recorded for human review.|
|`sas:metricHint`             |Fandaws metric alignment found|Pipeline-internal metric pre-fetch hint (§6.7.6). **Must not** be surfaced to users — ECVE's `viz:matchedMetric` is authoritative.|

### 5.4 Epistemic Distinction: Absent vs. Unmatched

When Fandaws is available but returns no concept match for a field, the output carries:

```json
"sas:fandawsConsulted": true,
"sas:fandawsMatch": null
```

When Fandaws is not available (no scope provided), the output carries:

```json
"sas:fandawsConsulted": false
```

(`sas:fandawsMatch` is omitted entirely — not set to null.)

This distinction is semantically significant. `fandawsConsulted: true, fandawsMatch: null` means "we asked the domain expert and they didn't recognize this field." `fandawsConsulted: false` means "we didn't ask." Downstream consumers can treat these differently — an unrecognized field in a domain-rich scope may warrant human review; an unconsulted field is simply uninformed.

### 5.5 Field IRI Normalization

Each `viz:DataField` carries an `@id` of the form `viz:field/{slug}`. The slug is derived from the original field name by the `normalizeFieldName` algorithm:

```
normalizeFieldName(name: string): string
  1. Apply Unicode NFC normalization.
  2. Convert to lowercase.
  3. Replace any character outside [a-z0-9] with a hyphen "-".
  4. Collapse consecutive hyphens to a single hyphen.
  5. Trim leading and trailing hyphens.
  6. If the result is empty, use "field".
```

**Completeness note:** After steps 2–5, the result contains only characters from `[a-z0-9\-]`. No percent-encoding step is needed — the algorithm is self-contained and produces IRI-safe slugs by construction. Unicode characters (CJK, Cyrillic, Arabic, etc.) are replaced with hyphens in step 3, which may produce empty slugs for fully non-Latin field names; step 6 handles this. Implementations should not attempt to transliterate or romanize Unicode — that would introduce locale-dependent behavior and break determinism.

**Collision resolution:** If two or more fields produce the same normalized slug, append `-1`, `-2`, etc., based on the field's position in CISM `SchemaEdge` order (0-indexed from the second collision). The first field with a given slug keeps the bare slug; the second gets `-1`, the third `-2`, and so on.

**Example:**

|Original Field Name |Slug           |`@id`                 |
|--------------------|---------------|----------------------|
|`"Revenue"`         |`revenue`      |`viz:field/revenue`   |
|`"First Name"`      |`first-name`   |`viz:field/first-name`|
|`"first_name"`      |`first-name`   |`viz:field/first-name-1` (collision)|
|`""`                |`field`        |`viz:field/field`     |
|`"日付"`            |`""` → `field` (step 6)|`viz:field/field-1` (collision with empty)|

This algorithm is deterministic: given the same CISM property order and field names, the same `@id` values are produced.

-----

## 6. Alignment Rules

SAS processes each primitive `SchemaNode` in the CISM and assigns a `viz:DataType`. Rules are organized into two layers: the **static core** (always active) and the **Fandaws enrichment layer** (active when a scope is provided). The Fandaws layer runs first — its decisions take precedence over static rules.

### 6.0 Processing Order

For each field (each `SchemaEdge` on the CISM root object node):

1. **Fandaws enrichment** (§6.7) — if a scope is available, query Fandaws for the field name. If Fandaws returns a concept with type guidance, apply it. Record the decision.
2. **Static rules** (§6.1–§6.6) — if Fandaws did not produce a classification (no scope, no match, or no type guidance on the matched concept), apply the static rule cascade.
3. **Annotation** — attach provenance metadata (`sas:alignmentRule`, Fandaws annotations) to the output `viz:DataField`.

### 6.1 Consensus Promotion

- **Applies when:** `typeDistribution` exists on the CISM node and the BIBSS lattice resolved to a wider type than the majority.
- **Rule:** Compute the consensus score for each primitive type in the distribution:

```
For each type T in typeDistribution:
  consensus(T) = typeDistribution[T] / (occurrences - nullCount)
```

Where `nullCount = typeDistribution["null"] || 0`. Null values are excluded from the denominator because they are orthogonal to type — a null value is not evidence for or against any type.

**Integer-based threshold comparison (determinism):** To avoid floating-point comparison ambiguity across runtimes, the threshold check uses integer arithmetic with a fixed scale factor. Define:

```
THRESH_SCALE = 1_000_000
scaledThreshold = Math.round(consensusThreshold * THRESH_SCALE)
```

`scaledThreshold` is computed once per `align` invocation from the configured `consensusThreshold`. For the default threshold of `0.95`, `scaledThreshold = 950000`.

A type `T` passes the threshold check if:

```
typeDistribution[T] * THRESH_SCALE >= scaledThreshold * nonNullTotal
```

**Overflow note:** For a dataset with `nonNullTotal` up to 2^32 (~4 billion rows), the right-hand side reaches `950000 * 4294967296 ≈ 4.08 × 10^15`, which exceeds the 32-bit integer range but is within the 64-bit safe integer range (`Number.MAX_SAFE_INTEGER` = 2^53 - 1 ≈ 9.0 × 10^15 in JavaScript). Implementations must use 64-bit integers or equivalent (JavaScript `Number` is safe up to 2^53; use `BigInt` for datasets exceeding ~9 trillion rows). For all practical datasets, standard 64-bit arithmetic suffices.

The `viz:consensusScore` stored in the output is a formatted string (§2.6); the **decision** to promote or not uses this integer formula exclusively.

If any non-null type `T` passes the integer threshold check:

- **First**, check the observation threshold: if `nonNullTotal < minObservationThreshold` (default 5), **abort consensus promotion**. Assign `viz:UnknownType` and emit diagnostic `SAS-012` (insufficient data for consensus). A single integer out of 10,000 nulls yields `consensus = 1.0`, but that score is statistically meaningless — one observation cannot justify type promotion.
- If `nonNullTotal >= minObservationThreshold`: assign the `viz:DataType` corresponding to `T` (see §6.1.1 mapping table).
- Set `viz:consensusScore` to `(typeDistribution[T] / nonNullTotal).toFixed(6)`.
- Set `sas:consensusNumerator` to `typeDistribution[T]` and `sas:consensusDenominator` to `nonNullTotal`.
- The minority values (those not matching `T`) are anomalies, not type evidence.

If no type passes the integer threshold check:

- Assign `viz:NominalType` (the safe fallback).
- Set `viz:consensusScore` to the highest single-type ratio, formatted per §2.6.
- Emit diagnostic `SAS-001` (inference uncertainty).

- **Rule name:** `"consensus-promotion"`

#### 6.1.1 Structural-to-Semantic Type Mapping

|BIBSS Primitive|Consensus Target|viz:DataType         |viz:numericPrecision|
|---------------|----------------|---------------------|--------------------|
|`integer`      |`integer`       |`viz:QuantitativeType`|`"integer"`         |
|`number`       |`number`        |`viz:QuantitativeType`|`"float"`           |
|`boolean`      |`boolean`       |`viz:BooleanType`    |—                   |
|`boolean-encoded-string`|`boolean-encoded-string`|`viz:BooleanType`|—              |
|`string`       |`string`        |`viz:NominalType`    |—                   |
|`null`         |—               |`viz:UnknownType`    |—                   |

When the consensus winner is `integer` but the BIBSS lattice widened to `number` (because a few float values were present), the SAS assignment is `viz:QuantitativeType` with `viz:numericPrecision: "integer"`. The minority floats are treated as anomalies.

When the consensus winner is `integer` but the BIBSS lattice widened to `string` (because a few string values were present), the SAS assignment is `viz:QuantitativeType` with `viz:numericPrecision: "integer"`. The minority strings are data-entry errors.

#### 6.1.2 Canonical `typeDistribution` Keys

SAS recognizes the following keys in the CISM `typeDistribution` object. All keys are case-sensitive, lowercase, and must match exactly.

|Key                       |BIBSS Source                                    |Notes                                    |
|--------------------------|------------------------------------------------|-----------------------------------------|
|`"integer"`               |Lattice integer type                            |Whole numbers, no leading zeros (BIBSS §20.4)|
|`"number"`                |Lattice number/float type                       |Decimal numbers                          |
|`"string"`                |Lattice string type                             |All non-numeric, non-boolean, non-null   |
|`"boolean"`               |Lattice boolean type                            |Native `true`/`false` JSON values        |
|`"boolean-encoded-string"`|BIBSS v1.4+ recognized boolean pair             |String values matching a boolean pair pattern (e.g., `"Y"/"N"`)|
|`"null"`                  |JSON `null` or absent value                     |Excluded from consensus denominator      |

Any `typeDistribution` key not in this list is treated as `"string"` for consensus purposes and emits diagnostic `SAS-014` (unrecognized type key). This forward-compatibility rule ensures SAS does not fail if BIBSS adds new primitive types — it degrades to the safe nominal fallback.

#### 6.1.3 CISM Consistency Validation

Before computing consensus, SAS validates the following invariants on each `SchemaNode`:

- `occurrences >= 0`. If negative, emit `SAS-013` (fatal).
- `sum(typeDistribution[*]) <= occurrences`. If the sum exceeds `occurrences`, emit `SAS-013` (fatal) — the counts are structurally inconsistent and cannot be trusted.
- `nullCount <= occurrences`. If violated, emit `SAS-013` (fatal).
- `nonNullTotal >= 0` (by construction from the above, but verified explicitly).

If any fatal diagnostic is emitted during validation, the field is assigned `viz:UnknownType` and no consensus calculation is attempted.

### 6.2 Temporal Detection

- **Applies when:** Consensus promotion assigned `viz:NominalType` (the field is majority string), or the field's `primitiveType` is `string` with unanimous consensus.
- **Rule:** For string-typed fields, SAS applies the ECVE v4.1 Appendix A.1 Temporal regex against the field name:

```
/^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2})?(\.\d+)?(Z|[+-]\d{2}:?\d{2})?)?$/
```

SAS does not re-scan raw data values (it has no access to them — only the CISM). Instead, it uses a **name-based heuristic** combined with **structural evidence**:

1. If the field's `primitiveType` is `string` AND `consensus("string") >= consensusThreshold`:
   - Check if the field name matches a temporal name pattern (configurable, default: `/(?:date|time|timestamp|created|updated|modified|born|died|started|ended|expires?)(?:_at|_on|_time)?$/i`).
   - If the name matches: assign `viz:TemporalType`.
   - If the name does not match: assign `viz:NominalType` (strings with no temporal signal).

2. If SNP v1.3 §4.7 converted dates in this field (manifest records `date_converted` entries for this path): assign `viz:TemporalType` regardless of name matching. The SNP manifest is direct evidence that the field contained date-formatted values.

- **Rule name:** `"temporal-detection"` or `"temporal-detection-snp-evidence"`

**Why SAS cannot re-scan values:** SAS receives the CISM, not the raw data. This is by design — the pipeline is `SNP → BIBSS → SAS`, and SAS operates on BIBSS's structural summary. If SNP converted dates to ISO 8601 before BIBSS ran, then BIBSS saw ISO 8601 strings and classified them as `string`. The `typeDistribution` says `{ "string": N }`. SAS needs the SNP manifest or the field name to infer temporality. Per the architectural boundary established in v1.1 §15.1, SAS will never accept value samples. If temporal detection is failing for non-standard date formats, the fix belongs in SNP (normalize them) or BIBSS (emit a `temporal-string` primitive type).

### 6.3 Boolean Pair Detection

- **Applies when:** The field is classified as `string` by BIBSS (not caught by consensus promotion or temporal detection).
- **Rule:** SAS checks if the field's values form a recognizable boolean pair. Because SAS does not have access to raw values, this rule operates on the CISM's `typeDistribution`:

If `typeDistribution` shows `{ "string": N }` (unanimous string), SAS cannot determine boolean-pair status from the CISM alone. Boolean pair detection therefore requires **one of**:

1. **BIBSS v1.4+ structural observation** — BIBSS identifies the field's `primitiveType` as `boolean-encoded-string` based on its own raw-data lattice analysis (e.g., observing that all string values belong to a recognized boolean pair like `"Y"/"N"`, `"true"/"false"`, `"yes"/"no"`). BIBSS passes this observation to SAS via a `typeDistribution` key of `"boolean-encoded-string"`. SAS then maps it to `viz:BooleanType` through normal consensus promotion. This is the correct architectural solution: BIBSS observes raw data, SAS interprets the observation.
2. **Fandaws enrichment** (§6.7) — Fandaws identifies the field as boolean-valued in the domain.
3. **Caller configuration** — the `SASConfig.booleanFields` list explicitly names fields that should be treated as boolean.

In v1.0–v2.0, boolean pair detection from raw values is **not performed** by SAS. The CISM does not contain string value inventories — only type counts. If BIBSS classified values as `string`, SAS cannot know whether those strings are `"Y"/"N"` without additional input. The fix belongs in BIBSS, not SAS. SAS does not touch raw data — ever.

If a field is identified as boolean (via Fandaws or configuration), SAS assigns `viz:BooleanType`.

- **Rule name:** `"boolean-pair-fandaws"` or `"boolean-pair-configured"`

**Design note:** This is a deliberate architectural boundary, not a limitation. SNP v1.2 attempted boolean pair detection via column-level frequency analysis. That was correctly removed as semantic coercion. SAS holds the line on structural purity: if boolean detection is failing without Fandaws, the fix belongs in BIBSS (emitting a `boolean-encoded-string` primitive type based on its own raw-data lattice), not in SAS. The pipeline contract is: SNP cleans → BIBSS observes → SAS judges. SAS never re-scans raw data.

### 6.4 Null Vocabulary Coercion

- **Applies when:** A field contains string values that represent null in a domain-specific convention.
- **Rule:** Like boolean pair detection, null vocabulary coercion requires domain context. The static core does not coalesce `"N/A"`, `"none"`, or `"-"` to null — SNP v1.3 §4.4 explicitly excluded these, and BIBSS classifies them as strings.

Null vocabulary coercion is available through:

1. **Fandaws enrichment** (§6.7) — Fandaws identifies specific string values as null-equivalent in the domain.
2. **Caller configuration** — `SASConfig.nullVocabulary` maps string values to null for specific fields.

When null vocabulary is applied, SAS adjusts the `typeDistribution` interpretation: values matching the null vocabulary are reclassified from `string` to `null` in the consensus calculation. This may change the consensus winner (e.g., a field with `{ "integer": 95, "string": 5 }` where all 5 strings are `"N/A"` becomes effectively `{ "integer": 95, "null": 5 }`, and consensus on integer rises from 0.95 to 1.0).

- **Rule name:** `"null-vocabulary-fandaws"` or `"null-vocabulary-configured"`

### 6.5 Direct Structural Pass-Through

- **Applies when:** No higher-priority rule has assigned a type.
- **Rule:** Map the BIBSS `primitiveType` directly to a `viz:DataType` using the §6.1.1 mapping table. Set `viz:consensusScore` to `"1.000000"` (unanimous structural agreement).
- **Rule name:** `"structural-passthrough"`

This is the fallback. A field where BIBSS observed only integers, with no temporal signal, no boolean pair, no Fandaws context, passes through as `viz:QuantitativeType` with `numericPrecision: "integer"` and `consensusScore: "1.000000"`.

### 6.6 Unknown Type Assignment

- **Applies when:** The CISM node has `primitiveType: "null"` (all values were null) or the node kind is `union` (cross-kind mixed types that cannot be mapped to a single `viz:DataType`).
- **Rule:** Assign `viz:UnknownType`. Emit diagnostic `SAS-002`.
- **Rule name:** `"unknown-assignment"`

### 6.7 Fandaws Enrichment Layer

When a `FandawsScope` is provided, SAS queries it for each field **before** applying static rules. The enrichment layer operates as follows:

#### 6.7.1 Field-to-Concept Resolution

For each field with name `N`:

1. Call `fandawsScope.resolveTerm(N)`.
2. If one or more concepts are returned:
   a. **Deterministic tie-breaker:** Sort the returned concepts lexicographically by `id`. This ensures SAS produces identical output even if the caller's `FandawsScope` implementation returns concepts in a non-deterministic order (e.g., due to hash map iteration). The sort is a safety net — a well-behaved scope already returns concepts in priority order (context → user → global), but SAS does not trust this.
   b. Select the first concept after sorting as the authoritative match.
3. Record the match on the output field: `sas:fandawsMatch`, `sas:fandawsEpistemicStatus`.

#### 6.7.2 Type Override

If the matched Fandaws concept has type guidance (a property or parent concept that indicates the expected data type), SAS uses it to override or confirm the static classification:

- If Fandaws says the field is a **coded identifier** (e.g., the concept's parent chain includes a coding system or classification scheme): assign `viz:NominalType`, even if the values are numeric. A field of ICD-10 codes (`"J06.9"`, `"M54.5"`) that BIBSS classified as `string` would be confirmed as Nominal. A field of numeric ZIP codes (`"14221"`, `"90210"`) that BIBSS classified as `string` (leading zeros preserved) would be confirmed as Nominal.

- If Fandaws says the field is a **temporal concept** (parent chain includes a temporal entity): assign `viz:TemporalType`, overriding the static temporal name-matching heuristic.

- If Fandaws says the field is a **boolean pair** in this domain: assign `viz:BooleanType`. This is how `"Y"/"N"` gets classified as boolean — Fandaws provides the domain context that the static core cannot.

- If Fandaws says the field is a **quantity** with specific units or constraints: assign `viz:QuantitativeType` and annotate with the Fandaws concept's unit/range information.

#### 6.7.3 Type Veto

Fandaws can also **prevent** a classification:

- If the static rule would classify `"Y"/"N"` as boolean (via configuration), but Fandaws identifies `"Y"` as a non-boolean concept in the domain (e.g., chromosome Y in genetics), Fandaws vetoes the boolean classification. The field remains `viz:NominalType`.

The veto is recorded: `sas:fandawsOverride: true`, `sas:fandawsOverrideReason: "Fandaws identifies 'Y' as chromosome Y, not boolean"`.

#### 6.7.4 Null Vocabulary Override

If Fandaws identifies specific string values as null-equivalent in the domain:

1. Fandaws returns a concept with a `fandaws:nullEquivalentValues` property listing the domain's null vocabulary (e.g., `["N/A", "Not Applicable", "-"]`).
2. SAS reclassifies those values in the consensus calculation (§6.4).
3. The reclassification may change the assigned `viz:DataType` if the null vocabulary removal shifts the consensus.

#### 6.7.5 Epistemic Matrix

The `epistemicStatus` of the matched Fandaws concept interacts with the **strength of the structural evidence** to determine override behavior. This prevents epistemic inversion — where unverified bulk-imported ontology data blindly overrides pristine, mathematically verified structural evidence.

**Override rules:**

- **`committed` concepts** (negotiated through the Fandaws semantic firewall, validated by a domain expert):
  - If the static `consensusScore > 0.99`: produce a **hard override** — replace the static classification unconditionally. A domain expert's committed judgment outweighs even strong structural evidence.
  - If the static `consensusScore ≤ 0.99`: produce a **hard override** — the structural evidence is not overwhelming, so the committed concept governs.

- **`imported` concepts** (bulk-loaded by IVNE, not yet validated through the semantic firewall):
  - If the static `consensusScore > 0.99`: produce a **suggestion only** — the structural evidence is overwhelming and the import is unverified. SAS records the Fandaws concept as `sas:fandawsSuggestion` but does **not** replace the static classification. Emit diagnostic `SAS-011` (imported concept contradicts high-confidence structural evidence).
  - If the static `consensusScore ≤ 0.99` or the static type is a fallback (`viz:NominalType` from string pass-through, `viz:UnknownType`): produce a **soft override** — replace the static classification with an advisory annotation: `sas:fandawsOverrideStrength: "advisory"`. The structural evidence is ambiguous enough that even an unverified import adds value.

**Epistemic Matrix summary:**

|Fandaws Status|Consensus > 0.99|Consensus ≤ 0.99 or Fallback Type|
|--------------|----------------|----------------------------------|
|`committed`   |Hard override   |Hard override                     |
|`imported`    |Suggestion only (SAS-011)|Soft override (advisory)  |

This distinction matters because an IVNE-imported concept from a medical ontology may contain structural assumptions that haven't been validated against the current domain context. If BIBSS observes 100,000 perfect integers (consensus 1.0) but a dirty Fandaws bulk-import flags the column as `NominalType`, the structural evidence must prevail. A committed concept has been explicitly reviewed and earns override authority even against strong structural evidence.

**Output annotations for suggestions:**

When an imported concept is recorded as a suggestion (not an override), the output carries:

```json
"sas:fandawsConsulted": true,
"sas:fandawsMatch": "fandaws:concept/some_imported_concept",
"sas:fandawsEpistemicStatus": "imported",
"sas:fandawsSuggestion": true,
"sas:fandawsOverride": false
```

Downstream consumers can surface these suggestions for human review without them corrupting the type assignment.

#### 6.7.6 Metric Pre-Matching (Internal Only)

If the Fandaws scope contains concepts that correspond to `viz:SemanticMetric` definitions in a loaded metric ontology, SAS can annotate fields with metric compatibility hints:

- For each field, if the matched Fandaws concept has a `fandaws:metricAlignment` property pointing to a metric IRI, SAS records `sas:metricHint` on the output field.
- **This annotation is strictly an internal optimization for the ECVE pipeline.** It enables the ECVE Metric Evaluator to pre-fetch or prioritize candidate metrics, reducing evaluation time. It is **not** a binding and **must not** be surfaced to the user until the ECVE Metric Evaluator (v4.1 §6.1 Step 3a) performs authoritative matching and confirms or rejects the hint.

**Split-brain prevention:** SAS annotates with `sas:metricHint`; ECVE evaluates with `viz:matchedMetric`. These are distinct properties. The UI layer must consume only `viz:matchedMetric` (produced by ECVE after formula evaluation) for display. If the UI surfaces `sas:metricHint` directly, users may see metric associations that ECVE later rejects due to formula constraints SAS cannot evaluate — producing broken promises and UI flicker. The `sas:metricHint` property is a pipeline-internal routing signal, not a user-facing assertion.

- **Rule name:** `"metric-hint"` (informational, does not affect type assignment)

-----

## 7. Configuration

```typescript
interface SASConfig {
  /**
   * Consensus threshold for type promotion (§6.1).
   * Default: 0.95, matching ECVE v4.1 Step 2d.
   */
  consensusThreshold: number

  /**
   * Minimum non-null observations required for consensus promotion (§6.1).
   * If (occurrences - nullCount) < this threshold, consensus promotion is
   * aborted and the field is assigned viz:UnknownType with SAS-012.
   * Prevents small-sample bias (e.g., 1 integer out of 10,000 nulls = 1.0 consensus).
   * Default: 5.
   */
  minObservationThreshold: number

  /**
   * Temporal field name pattern (§6.2).
   * Default: /(?:date|time|timestamp|created|updated|modified|born|died|
   *           started|ended|expires?)(?:_at|_on|_time)?$/i
   */
  temporalNamePattern: RegExp

  /**
   * Explicitly declared boolean fields (§6.3).
   * Maps field name to the boolean pair values.
   * Matching: field names are compared case-insensitively (both sides lowercased).
   * Boolean pair values are compared case-insensitively against raw string values.
   * This config applies only when BIBSS reports primitiveType as "string" —
   * numeric or boolean BIBSS types are not eligible for boolean pair override.
   * Default: empty (no static boolean pair detection).
   * Example: { "is_active": ["Y", "N"], "status": ["TRUE", "FALSE"] }
   */
  booleanFields: Record<string, [string, string]>

  /**
   * Domain-specific null vocabulary (§6.4).
   * Maps field name to null-equivalent string values.
   * Field name matching: case-insensitive (both sides lowercased).
   * Value matching: case-insensitive, whitespace-trimmed.
   * Default: empty (no static null vocabulary).
   * Example: { "result": ["N/A", "-", "none"] }
   */
  nullVocabulary: Record<string, string[]>

  /**
   * Global null vocabulary applied to all fields (§6.4).
   * Value matching: case-insensitive, whitespace-trimmed.
   * Default: empty. Use with caution — domain-specific is preferred.
   */
  globalNullVocabulary: string[]
}
```

**Default configuration:**

```typescript
const DEFAULT_CONFIG: SASConfig = {
  consensusThreshold: 0.95,
  minObservationThreshold: 5,
  temporalNamePattern: /(?:date|time|timestamp|created|updated|modified|born|died|started|ended|expires?)(?:_at|_on|_time)?$/i,
  booleanFields: {},
  nullVocabulary: {},
  globalNullVocabulary: []
}
```

**Design note:** The configuration surface is intentionally lean. Most intelligence comes from Fandaws, not from caller-supplied configuration. The static config exists for the standalone (no-Fandaws) path and for cases where the caller has domain knowledge that Fandaws doesn't yet contain.

-----

## 8. Public API

```typescript
interface SAS {
  /**
   * Align a BIBSS CISM to a viz:DatasetSchema.
   *
   * Synchronous. Returns SASResult directly (not a Promise).
   * Never throws — all errors reported as diagnostics in the result.
   *
   * @param cism       - BIBSS CISM (version 1.3+, with typeDistribution)
   * @param rawHash    - viz:rawInputHash (SHA-256, computed by caller before SNP)
   * @param config     - Optional configuration overrides
   * @param snpManifest - Optional SNP v1.3 manifest entries for normalization provenance
   * @param fandaws    - Optional Fandaws scope for enriched alignment (must be synchronous)
   */
  align(
    cism: CISMRoot,
    rawHash: string,
    config?: Partial<SASConfig>,
    snpManifest?: ManifestEntry[],
    fandaws?: FandawsScope
  ): SASResult
}
```

**Synchronous contract:** `align` is synchronous and returns `SASResult` directly. It does not return a `Promise`. This matches the edge-canonical execution model (§2.1) and the synchronous `FandawsScope` requirement (§4.3). All inputs must be fully resolved in memory before invocation.

**Parameter ordering rationale:** Required parameters first (`cism`, `rawHash`), then optional parameters in order of expected usage frequency. `config` is more commonly customized than `snpManifest`, which is more commonly provided than `fandaws`. The most common invocation is `sas.align(cism, rawHash)` with all defaults.

-----

## 9. Processing Algorithm

### 9.1 Overview

```
Input: CISMRoot + rawHash + config? + snpManifest? + fandawsScope?

1. Validate CISM version (must be ≥ 1.3). If invalid: emit SAS-007 (fatal), return error.
2. Validate CISM structure: root node must be object or array-of-object.
   If invalid: emit SAS-013 (fatal), return error.
3. Extract the root node's properties (SchemaEdge[])
4. For each field (SchemaEdge), in CISM property order:
   a. Resolve the target SchemaNode
   b. Validate SchemaNode consistency (§6.1.3)
   c. If validation failed: assign UnknownType, skip to step f
   d. If fandawsScope available: run Fandaws enrichment (§6.7)
   e. If Fandaws produced a classification: use it
      Else: run static rule cascade (§6.1 → §6.2 → §6.3 → §6.4 → §6.5 → §6.6)
   f. Attach SNP manifest annotations if available
   g. Build viz:DataField JSON-LD entity (with @id per §5.5 normalizeFieldName)
5. Assemble viz:DatasetSchema with all fields (ordered per §2.6)
6. Serialize using JCS canonicalization (§2.6)
7. Return SASResult with status "ok"
```

### 9.2 Field Traversal

SAS operates on the **top-level properties** of the CISM root node. For CSV input (CISM root is an array with an object itemType), these are the columns. For JSON input (CISM root is an object), these are the top-level keys.

**Nested fields:** In v2.0, SAS does not produce `viz:DataField` entities for nested JSON properties. The ECVE pipeline consumes flat tabular data. If the CISM contains nested objects or arrays, SAS processes only the top-level properties and emits diagnostic `SAS-003` for any nested structure it skips.

**Union fields:** If a top-level property has `kind: "union"`, SAS assigns `viz:UnknownType` (§6.6). Union types cannot be cleanly mapped to a single `viz:DataType`.

### 9.3 Consensus Calculation Detail

Given a `SchemaNode` with `typeDistribution`:

```
typeDistribution: { "null": 2, "integer": 95, "string": 3 }
occurrences: 100
```

1. **Validate counts** (§6.1.3): `sum(2 + 95 + 3) = 100 ≤ occurrences(100)` → valid.
2. Compute `nullCount = typeDistribution["null"] || 0` → 2
3. Compute `nonNullTotal = occurrences - nullCount` → 98
4. **Observation threshold check:** Is `nonNullTotal >= minObservationThreshold` (default 5)? 98 ≥ 5 → yes, proceed. (If no: assign `viz:UnknownType`, emit SAS-012, skip remaining steps.)
5. For each non-null type, **integer threshold check** (THRESH_SCALE = 1,000,000; scaledThreshold = 950,000 for default 0.95):
   - `"integer"`: `95 * 1_000_000 = 95_000_000 ≥ 950_000 * 98 = 93_100_000`? Yes → passes.
   - `"string"`: `3 * 1_000_000 = 3_000_000 ≥ 950_000 * 98 = 93_100_000`? No.
6. Highest-passing type: `integer`.
7. Assign `viz:QuantitativeType` with `numericPrecision: "integer"`.
8. Compute display score: `(95 / 98).toFixed(6)` → `"0.969388"`.
9. Set `viz:consensusScore: "0.969388"`, `sas:consensusNumerator: 95`, `sas:consensusDenominator: 98`.

If null vocabulary is applied (§6.4) and all 3 strings are `"N/A"`:

1. Reclassify: `{ "null": 5, "integer": 95 }` (the 3 strings become null)
2. `nonNullTotal = 100 - 5` → 95
3. Integer check: `95 * 1_000_000 = 95_000_000 ≥ 950_000 * 95 = 90_250_000` → yes.
4. Assign `viz:QuantitativeType` with `consensusScore: "1.000000"`, `sas:consensusNumerator: 95`, `sas:consensusDenominator: 95`.

-----

## 10. Diagnostic Codes

Each diagnostic emitted by SAS conforms to the `Diagnostic` interface (§5.1). The `message` and `remediation` fields are human-readable and may vary in wording across implementations; the `code` and `level` are normative.

|Code     |Level  |Condition                                                                  |Context Fields                               |Example `remediation`                        |
|---------|-------|---------------------------------------------------------------------------|---------------------------------------------|---------------------------------------------|
|`SAS-001`|warning|No type achieved consensus threshold; field assigned NominalType as fallback|`field`, `highestConsensus`, `highestType`   |"Review field data for mixed types or increase consensusThreshold."|
|`SAS-002`|info   |Field assigned UnknownType (all-null or union)                             |`field`, `reason`                            |"Field contains no typed data. Verify data source."|
|`SAS-003`|info   |Nested structure skipped (not mapped to viz:DataField in v2.0)             |`field`, `kind`                              |"Flatten nested data before pipeline ingestion."|
|`SAS-004`|info   |Fandaws override applied                                                  |`field`, `staticType`, `fandawsType`, `concept`|"Fandaws concept determined type. Review concept if unexpected."|
|`SAS-005`|info   |Fandaws veto applied (prevented static classification)                    |`field`, `vetoedType`, `reason`              |"Fandaws identified domain-specific meaning for this field's values."|
|`SAS-006`|info   |Fandaws consulted, no match found                                         |`field`                                      |"Consider adding a Fandaws concept for this field."|
|`SAS-007`|fatal  |CISM version below 1.3 (typeDistribution unavailable). **Schema-level:** blocks all processing.|`version`                                    |"Upgrade BIBSS to v1.3+ to produce typeDistribution data."|
|`SAS-008`|info   |Null vocabulary reclassification changed consensus winner                  |`field`, `beforeType`, `afterType`, `reclassifiedCount`|"Null vocabulary improved type detection."|
|`SAS-009`|info   |Temporal detection via SNP manifest evidence                               |`field`                                      |"SNP date conversion confirmed temporal type."|
|`SAS-010`|info   |Temporal detection via name pattern heuristic                              |`field`, `matchedPattern`                    |"Field name matched temporal pattern. Verify if field contains dates."|
|`SAS-011`|warning|Imported Fandaws concept contradicts high-confidence structural evidence (consensus > 0.99); recorded as suggestion only|`field`, `staticType`, `staticConsensus`, `fandawsConcept`|"Validate the imported Fandaws concept through the semantic firewall."|
|`SAS-012`|warning|Insufficient non-null observations for consensus promotion; field assigned UnknownType|`field`, `nonNullTotal`, `minObservationThreshold`|"Field is mostly null. Collect more data or lower minObservationThreshold."|
|`SAS-013`|fatal  |CISM structural inconsistency (count mismatch, negative occurrences, or invalid structure). **Field-level:** marks field as UnknownType but does not block schema emission.|`field`, `reason`, `occurrences`, `typeDistributionSum`|"BIBSS produced invalid counts for this field. Example: `{ occurrences: 100, typeDistributionSum: 105 }` — sum exceeds occurrences. Check BIBSS version and configuration."|
|`SAS-014`|warning|Unrecognized `typeDistribution` key (treated as string for consensus)      |`field`, `unknownKey`                        |"BIBSS emitted unknown type key `'custom_type'`. Treated as string. Verify BIBSS/SAS version compatibility."|

**Severity semantics:**

- `fatal` — processing cannot continue for the affected scope. **Schema-level fatal** (SAS-007): `SASResult.status` is `"error"` and no schema is produced. **Field-level fatal** (SAS-013): that field gets `viz:UnknownType` but the schema is still emitted and `status` remains `"ok"`. See §5.1 for the full distinction.
- `warning` — processing continued but the result may be suboptimal or require human review.
- `info` — informational trace. No action required.

-----

## 11. Performance

### 11.1 Complexity

```
O(F × (R + Q))
```

Where `F` is the number of top-level fields, `R` is the static rule cascade depth (constant — at most 6 rules checked), and `Q` is the Fandaws query cost per field. Without Fandaws, this reduces to `O(F)`. With Fandaws, the cost depends on the scope implementation — for in-memory graph traversal, `Q` is typically O(log N) where N is the concept count.

SAS does not scan raw data. It operates on the CISM summary, which is a small tree regardless of dataset size. A dataset with 100,000 rows and 20 columns produces a CISM with ~20 leaf nodes. SAS processes those 20 nodes, not the 100,000 rows.

### 11.2 Benchmark Targets

|Input                               |Fields|Fandaws|Target Time|
|------------------------------------|------|-------|-----------|
|Flat CISM, all numeric              |20    |No     |< 1ms      |
|Flat CISM, mixed types              |20    |No     |< 2ms      |
|Flat CISM, temporal name matching   |20    |No     |< 2ms      |
|Flat CISM, all types + config       |20    |No     |< 3ms      |
|Flat CISM, Fandaws (1K concepts)    |20    |Yes    |< 10ms     |
|Flat CISM, Fandaws (50K concepts)   |20    |Yes    |< 50ms     |
|Wide CISM                           |500   |No     |< 20ms     |
|Wide CISM, Fandaws (50K concepts)   |500   |Yes    |< 500ms    |

These are targets, not guarantees. The Fandaws query cost depends on the scope implementation. SAS's own processing is negligible — nearly all time in the enriched path is Fandaws graph traversal.

### 11.3 Fandaws Scope Performance Guidance

SAS calls `resolveTerm` once per field and may call `hasProperty` or `getConcept` for matched concepts. For large Fandaws scopes (>10K concepts), the caller should ensure the `FandawsScope` implementation maintains an internal label → concept index (hash map) so that `resolveTerm` operates in O(1) average time rather than scanning the full concept list. SAS does not impose memory limits on the scope, but callers should be aware that loading a 50K-concept scope into browser memory may consume 50–200MB depending on property density. For browser environments, consider lazy-loading or pre-filtering the scope to the active domain context.

-----

## 12. Integration Pipeline

### 12.1 Complete ECVE Data Pipeline

```
Raw input bytes
       │
       ▼ (Caller computes viz:rawInputHash — SHA-256 of raw bytes)
       │
       ▼
SNP.normalize(input, snpConfig)
       │ Output: { cleaned: string, manifest: ManifestEntry[], format, diagnostics }
       │
       ▼
BIBSS.infer(cleaned, bibssConfig)
       │ Output: { cism: CISMRoot, diagnostics }
       │
       ▼
SAS.align(cism, rawHash, sasConfig?, manifest?, fandawsScope?)
       │ Output: { schema: viz:DatasetSchema, diagnostics }
       │
       ▼
ECVE Metric Evaluator (v4.1 Phase 1, Step 3)
       │ Input: viz:DatasetSchema + Working Copy Data + Metric Ontology[]
       │ Output: Enriched viz:DatasetSchema with viz:DerivedField entities
       │
       ▼
ECVE Reasoner (v4.1 Phase 2)
       │
       ▼
ECVE Compiler + Renderer (v4.1 Phases 3–5)
```

### 12.2 Orchestration Note

The caller (typically ECVE's orchestration layer) is responsible for:

1. Computing `viz:rawInputHash` before any transformation.
2. Invoking SNP, passing the raw string.
3. Invoking BIBSS, passing SNP's `cleaned` output.
4. Loading the appropriate Fandaws scope (if available) from the active session.
5. Invoking SAS, passing the CISM, raw hash, SNP manifest, and Fandaws scope.
6. Passing the `viz:DatasetSchema` to the ECVE metric evaluator.

SAS does not orchestrate these steps. It is a pure function that accepts inputs and produces output.

### 12.3 What Changes from ECVE v4.1

ECVE v4.1 Step 2 (Type Inference Algorithm) is replaced by the SNP → BIBSS → SAS pipeline. Specifically:

- **ECVE v4.1 Step 0** (Pre-Processing Normalization) → now **SNP** (format cleaning).
- **ECVE v4.1 Step 2a–2d** (Regex cascade, numeric unification, consensus threshold) → now **BIBSS** (structural inference) + **SAS** (consensus promotion and type mapping).
- **ECVE v4.1 Step 2e** (Output: `viz:DatasetSchema`) → now **SAS output**.

The ECVE regex patterns (Appendix A.1–A.5) remain normative. SAS uses A.1 for temporal detection. BIBSS v1.3 §7.1.3 aligns with A.2 (boolean), A.3 (integer — with the leading-zero fix noted in BIBSS v1.3 §20.4), and A.4 (float). A.5 (nominal) is the default fallback.

ECVE v4.1 Steps 3–5 (Metric Evaluation, Reasoning, Rendering) are unchanged. They consume `viz:DatasetSchema` regardless of whether it was produced by the old monolithic Step 2 or the new SNP → BIBSS → SAS pipeline.

-----

## 13. Testing Contract

### 13.1 Determinism Tests

**Same-runtime idempotency:**

```
const a = canonicalize(align(cism, hash, config).schema)
const b = canonicalize(align(cism, hash, config).schema)
assert(a === b)  // byte-identical
```

**Cross-runtime determinism (CI matrix):** Run the same test fixtures in at minimum: Node.js 18, Node.js 20, and one Chromium-based browser engine. The JCS-canonicalized output bytes must be identical across all environments. This is the primary guard against floating-point formatting divergence and object key ordering differences.

**Fandaws ordering stability:** Construct a `FandawsScope` where `resolveTerm` returns multiple concepts for a single label. Verify that SAS selects the same concept regardless of the order the scope was constructed, and that the output is byte-identical.

**Fandaws nondeterministic scope robustness:** Construct a `FandawsScope` that returns concepts in shuffled order across invocations (simulating hash-map iteration). Verify SAS output is byte-identical regardless of shuffle order, because of the §6.7.1 tie-breaker sort.

**Serializer string format test:** For every `viz:DataField` in the output, assert that `viz:consensusScore` is a JSON string (not a number) matching the regex `/^\d+\.\d{6}$/`. Specifically verify that `1.0` is emitted as `"1.000000"`, not `"1"`, `"1.0"`, or bare `1`.

**Consensus precision tests:** For threshold-boundary cases, verify that the THRESH_SCALE integer arithmetic (§6.1) produces the correct promotion/rejection decision. Specifically:

- `typeDistribution: { "integer": 19, "string": 1 }`, occurrences 20, threshold 0.95 → `19 * 1_000_000 = 19_000_000 ≥ 950_000 * 20 = 19_000_000` → **passes** (exactly at threshold).
- `typeDistribution: { "integer": 189, "string": 11 }`, occurrences 200, threshold 0.95 → `189 * 1_000_000 = 189_000_000 ≥ 950_000 * 200 = 190_000_000` → **fails** (0.945, below threshold).

**JSON-LD structural validation:** Validate that produced output is valid JSON-LD by confirming all `@id`, `@type`, and property values conform to the `viz:` and `sas:` namespaces. Optionally validate against a SHACL shape for `viz:DatasetSchema` if one is maintained.

### 13.2 Required Test Cases

|Category                          |Cases                                                                                                                                                |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
|Consensus promotion (integer)     |`typeDistribution: { "integer": 95, "string": 5 }` → QuantitativeType (consensus 0.95). `{ "integer": 94, "string": 6 }` → NominalType (consensus 0.94 < 0.95), SAS-001.|
|Consensus promotion (with nulls)  |`{ "null": 10, "integer": 85, "string": 5 }`, occurrences 100 → nonNullTotal 90, consensus("integer") = 85/90 = 0.944 → NominalType (below threshold). Verify null exclusion from denominator.|
|Consensus exact threshold         |`{ "integer": 95, "string": 5 }`, occurrences 100 → consensus exactly 0.95 → QuantitativeType (threshold is ≥, not >).|
|Structural pass-through (integer) |CISM with `primitiveType: "integer"`, `typeDistribution: { "integer": 100 }` → QuantitativeType, consensusScore `"1.000000"`, numericPrecision "integer".|
|Structural pass-through (boolean) |CISM with `primitiveType: "boolean"`, `typeDistribution: { "boolean": 100 }` → BooleanType.|
|Structural pass-through (string)  |CISM with `primitiveType: "string"`, `typeDistribution: { "string": 100 }` → NominalType (no temporal name match).|
|Temporal detection (name match)   |Field named `"created_at"`, `primitiveType: "string"` → TemporalType via name pattern. `sas:alignmentRule: "temporal-detection"`.|
|Temporal detection (SNP evidence) |Field with SNP manifest `date_converted` entries → TemporalType. `sas:alignmentRule: "temporal-detection-snp-evidence"`.|
|Temporal detection (no match)     |Field named `"description"`, `primitiveType: "string"` → NominalType (name does not match temporal pattern).|
|Boolean pair (configured)         |`booleanFields: { "is_active": ["Y", "N"] }`, field `"is_active"` → BooleanType.|
|Boolean pair (not configured)     |Field `"is_active"`, no config, no Fandaws → NominalType (static core cannot detect boolean pairs from CISM alone).|
|Null vocabulary (field-specific)  |`nullVocabulary: { "result": ["N/A"] }`, field `"result"` with `{ "integer": 95, "string": 5 }` where strings are "N/A" → reclassify, consensus rises, QuantitativeType.|
|Unknown type (all null)           |`typeDistribution: { "null": 100 }` → UnknownType, SAS-002.|
|Unknown type (union)              |CISM node with `kind: "union"` → UnknownType, SAS-002.|
|Nested structure skipped          |CISM with nested object property → top-level field processed, nested skipped, SAS-003.|
|SNP normalization annotation      |SNP manifest with `currency_stripped` for field → `viz:wasNormalized: true`.|
|SNP percentage annotation         |SNP manifest with percent stripping → `viz:wasPercentage: true`.|
|Fandaws override                  |Fandaws says field is coded identifier, static would say Quantitative → NominalType, SAS-004.|
|Fandaws veto                      |Fandaws says "Y" is chromosome Y, config has boolean pair → NominalType (veto), SAS-005.|
|Fandaws no match                  |Fandaws scope provided, no concept matches field → `sas:fandawsConsulted: true, sas:fandawsMatch: null`, SAS-006.|
|Fandaws not available             |No scope provided → `sas:fandawsConsulted: false`, no Fandaws annotations.|
|Fandaws epistemic weighting       |Committed concept → hard override. Imported concept with low static consensus → soft override with `sas:fandawsOverrideStrength: "advisory"`.  |
|Fandaws epistemic matrix (imported vs high consensus)|Imported concept contradicts static classification with `consensusScore > 0.99` → suggestion only, `sas:fandawsSuggestion: true`, type unchanged, SAS-011.|
|Fandaws epistemic matrix (imported vs low consensus)|Imported concept contradicts static classification with `consensusScore ≤ 0.99` → soft override, `sas:fandawsOverrideStrength: "advisory"`.|
|Fandaws epistemic matrix (committed vs high consensus)|Committed concept contradicts static classification with `consensusScore > 0.99` → hard override, type replaced.|
|Min observation threshold (below)  |`typeDistribution: { "null": 9997, "integer": 3 }`, occurrences 10000, `minObservationThreshold: 5` → nonNullTotal = 3 < 5 → UnknownType, SAS-012.|
|Min observation threshold (at)     |`typeDistribution: { "null": 95, "integer": 5 }`, occurrences 100, `minObservationThreshold: 5` → nonNullTotal = 5 ≥ 5 → consensus proceeds normally.|
|Min observation threshold (single obs)|`typeDistribution: { "null": 9999, "integer": 1 }`, occurrences 10000 → nonNullTotal = 1 < 5 → UnknownType, SAS-012 (prevents false 1.0 consensus).|
|Metric hint not in output type     |`sas:metricHint` present on field → does not affect `viz:hasDataType`. Type determined by static/Fandaws rules only.|
|Field IRI normalization            |`"Revenue"` → `viz:field/revenue`. `"First Name"` → `viz:field/first-name`. `"日付"` → `viz:field/field`.|
|Field IRI collision                |Two fields normalizing to same slug → second gets `-1` suffix per CISM property order.|
|Consensus numerator/denominator    |Output includes `sas:consensusNumerator` and `sas:consensusDenominator` as exact integers alongside rounded `viz:consensusScore`.|
|Integer threshold boundary         |`{ "integer": 19, "string": 1 }`, threshold 0.95 → integer check `19*100 ≥ 95*20` → passes (exact boundary).|
|CISM count mismatch                |`typeDistribution` sum exceeds `occurrences` → SAS-013 (fatal for that field), UnknownType.|
|Unrecognized typeDistribution key  |CISM contains `{ "custom_type": 50 }` → treated as string, SAS-014 emitted.|
|SASResult status on fatal          |CISM version "1.0" → `SASResult.status: "error"`, `schema` absent, SAS-007 diagnostic.|
|JCS canonicalization               |Output keys are lexicographically sorted. `viz:consensusScore` is a string matching `/^\d+\.\d{6}$/`.|
|ConsensusScore string format       |`viz:consensusScore` is always a JSON string (quoted), never a bare number. `"1.000000"` not `1` or `1.0`.|
|Fandaws tie-breaker (shuffled)     |`resolveTerm` returns concepts `[{id:"z"}, {id:"a"}, {id:"m"}]` → SAS sorts by `id`, selects `{id:"a"}`. Output stable regardless of input order.|
|Schema-level fatal (SAS-007)       |CISM version "1.0" → `status: "error"`, `schema` absent, diagnostics contain SAS-007 with `level: "fatal"`.|
|Field-level fatal (SAS-013)        |One field has count mismatch → that field gets UnknownType + SAS-013, but `status: "ok"` and schema is produced with all other fields intact.|
|THRESH_SCALE overflow safety       |Dataset with `nonNullTotal = 2_000_000_000` (2B rows) → integer check uses values within 64-bit safe range. No overflow.|
|Output JSON-LD validity           |Output is valid JSON-LD. All @id, @type, and property values conform to the viz: and sas: namespaces.|
|Numeric precision (integer)       |BIBSS `primitiveType: "integer"` → `viz:numericPrecision: "integer"`.|
|Numeric precision (float)         |BIBSS `primitiveType: "number"` → `viz:numericPrecision: "float"`.|
|Numeric precision (consensus)     |BIBSS widened to `number`, but `typeDistribution` shows 98% integer → `numericPrecision: "integer"` (consensus winner determines precision).|
|Raw hash propagation              |`rawHash` parameter appears as `viz:rawInputHash` in output schema.|

### 13.3 Property-Based Invariants

For any valid CISM `C`, hash `H`, and config `K`:

1. `align(C, H, K)` terminates and never throws.
2. `align(C, H, K).status` is either `"ok"` or `"error"`.
3. If `status` is `"ok"`: `schema` is present and every `SchemaEdge` on the CISM root node produces exactly one `viz:DataField` in the output.
4. If `status` is `"error"`: `schema` is absent and at least one diagnostic has `level: "fatal"` at schema scope (SAS-007).
5. Every `viz:DataField` has exactly one `viz:hasDataType`.
6. Every `viz:DataField` has a `viz:consensusScore` string matching the pattern `/^\d+\.\d{6}$/` with value in range `["0.000000", "1.000000"]`.
7. Every `viz:DataField` has `sas:consensusNumerator` and `sas:consensusDenominator` as non-negative integers where `numerator <= denominator`.
8. Every `viz:DataField` has an `sas:alignmentRule` string.
9. If `fandaws` is provided, every field has `sas:fandawsConsulted: true`.
10. If `fandaws` is not provided, no field has `sas:fandawsMatch`.
11. The output `viz:rawInputHash` equals the input `rawHash`.
12. If a field has `nonNullTotal < minObservationThreshold`, its `viz:hasDataType` is `viz:UnknownType`.
13. If `sas:fandawsSuggestion` is `true` on a field, `sas:fandawsOverride` is `false` on that field.
14. The `viz:hasField` array preserves CISM `SchemaEdge` order.
15. All `@id` values in `viz:hasField` are unique.
16. The output, when serialized via JCS (RFC 8785), is byte-identical across runtimes for identical inputs.

-----

## 14. Security Considerations

- **No network calls.** SAS makes zero HTTP requests. Fandaws queries are in-memory graph traversals.
- **No data persistence.** SAS writes nothing to storage.
- **No `eval` or dynamic code generation.**
- **No access to raw data.** SAS operates on the CISM summary, not on the dataset itself. It cannot leak or expose individual data values.
- **Fandaws scope is read-only.** SAS queries the scope but cannot modify it.
- **Fandaws scope trust boundary.** SAS treats the `FandawsScope` as caller-provided input, not as trusted code. SAS will not execute arbitrary functions from the scope beyond the four interface methods (§4.3). However, SAS cannot prevent a malicious `FandawsScope` implementation from performing side effects (network calls, storage writes) inside its method bodies. The caller is responsible for ensuring the provided scope is a vetted, pure, in-memory implementation — not an untrusted proxy. For maximum safety in browser environments, callers should construct the scope from a plain data object (concept map) rather than wrapping an external API.

-----

## 15. Known Limitations (v2.0)

### 15.1 No Value-Level Access

SAS operates on CISM metadata (type distributions, field names), not on individual cell values. This means:

- Boolean pair detection requires Fandaws, explicit configuration, or BIBSS v1.4+ emitting `boolean-encoded-string` in its `typeDistribution`; the static core cannot detect `"Y"/"N"` patterns from type counts alone.
- Null vocabulary reclassification requires knowing which specific string values are null-equivalent; the CISM only records that `N` values were strings.
- Temporal detection for non-ISO-8601 dates relies on field name heuristics or SNP manifest evidence.

**Architectural boundary:** SAS will never accept an optional value sample or re-scan raw data. If a classification problem cannot be solved from CISM metadata alone, the fix belongs in BIBSS (which has raw-data access) or Fandaws (which has domain knowledge). The pipeline contract — SNP cleans, BIBSS observes, SAS judges — is inviolable.

### 15.2 Flat Fields Only

SAS v2.0 maps only top-level CISM properties to `viz:DataField` entities. Nested JSON structures are skipped. The ECVE pipeline operates on flat tabular data; nested-to-flat projection is a separate concern.

### 15.3 Union Types

Union-typed fields are assigned `viz:UnknownType` (§6.6). A future version may introduce an opt-in `SASConfig.unionResolutionStrategy` with policies such as: prefer the non-null branch, attempt to unify numeric subtypes into a single `QuantitativeType`, or expand to multiple `viz:hasDataType` entries with weights. For v2.0, union → Unknown is the safe default.

### 15.4 No Metric Formula Evaluation

SAS annotates fields with metric compatibility hints (via Fandaws), but it does not evaluate metric formulas or produce `viz:DerivedField` entities. That remains the ECVE Metric Evaluator's responsibility. SAS provides the schema; ECVE computes the KPIs.

### 15.5 Temporal Detection Limitations

SAS's temporal detection has three sources of evidence: (a) SNP manifest `date_converted` entries, (b) field name pattern matching, (c) Fandaws concept alignment. It does not apply the ECVE A.1 temporal regex to individual values (it has no value access). A field named `"code"` containing ISO 8601 dates will be classified as NominalType in standalone mode unless SNP converted them (producing manifest evidence) or Fandaws identifies the field as temporal.

### 15.6 Fandaws Query Interface Assumptions

SAS v2.0 assumes the `FandawsScope` interface defined in §4.3. If the Fandaws v3.4+ API evolves (e.g., adding typed query results, SPARQL-like graph patterns), SAS's interface may need updating. The interface is intentionally minimal — four methods — to reduce coupling.

-----

## Appendix A — Complete Rule Precedence

The following table shows the complete rule evaluation order for a single field. The first rule that produces a classification wins.

|Priority|Rule                            |Source      |Condition                                                    |Output DataType       |
|--------|--------------------------------|------------|-------------------------------------------------------------|----------------------|
|1       |Fandaws type override (§6.7.2)  |Enrichment  |Fandaws concept has type guidance                            |Per Fandaws concept   |
|2       |Fandaws type veto (§6.7.3)      |Enrichment  |Fandaws vetoes a static classification                       |Reverts to Nominal    |
|3       |Consensus promotion (§6.1)      |Static core |typeDistribution consensus ≥ threshold on non-string type    |Per consensus winner  |
|4       |Temporal (SNP evidence) (§6.2)  |Static core |SNP manifest has date_converted entries for this field       |TemporalType          |
|5       |Temporal (name match) (§6.2)    |Static core |Field name matches temporal pattern, type is string          |TemporalType          |
|6       |Boolean pair (configured) (§6.3)|Static core |Field in booleanFields config                                |BooleanType           |
|7       |Null vocabulary reclassify (§6.4)|Static core|Null vocab shifts consensus winner                           |Per reclassified consensus|
|8       |Structural pass-through (§6.5)  |Static core |No prior rule matched                                        |Per §6.1.1 mapping    |
|9       |Unknown assignment (§6.6)       |Static core |All-null or union node                                       |UnknownType           |

**Fandaws enrichment annotations** (field-to-concept alignment, epistemic status, metric hints) are attached regardless of which rule determined the type. A field can be classified by consensus promotion (static) and still carry a Fandaws concept alignment.

-----

## Appendix B — Output Example

**Input CISM** (simplified, 3-column CSV dataset):

```json
{
  "version": "1.3",
  "root": {
    "kind": "array",
    "itemType": {
      "kind": "object",
      "properties": [
        {
          "name": "Region",
          "target": { "kind": "primitive", "primitiveType": "string", "typeDistribution": { "string": 500 }, "occurrences": 500 }
        },
        {
          "name": "Revenue",
          "target": { "kind": "primitive", "primitiveType": "string", "typeDistribution": { "null": 3, "integer": 492, "string": 5 }, "occurrences": 500, "nullable": true }
        },
        {
          "name": "created_at",
          "target": { "kind": "primitive", "primitiveType": "string", "typeDistribution": { "string": 500 }, "occurrences": 500 }
        }
      ]
    }
  }
}
```

**SNP Manifest** (partial):

```json
[
  { "rule": "currency_stripped", "path": "Revenue", "detail": { "type": "currency_stripped", "originalValue": "$1,234.56", "cleanedValue": "1234.56", "artifacts": ["$", ","] } }
]
```

**SAS Output** (with Fandaws scope providing a concept for "Revenue"):

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

**Trace of decisions:**

- **Region:** Fandaws consulted, no match. Static cascade: `typeDistribution` is `{ "string": 500 }`, consensus on string = 1.0. String → NominalType via structural pass-through (§6.5). No temporal name match.

- **Revenue:** Fandaws consulted, matched `fandaws:concept/revenue` (committed). Fandaws concept is a quantity — confirms static classification. Static cascade: BIBSS widened to `string` (because 5 values were strings after currency stripping), but `typeDistribution` shows `{ "integer": 492, "string": 5 }`. Validate: sum(3+492+5) = 500 ≤ 500 → ok. nonNullTotal = 500 - 3 = 497. Integer threshold check (THRESH_SCALE): `492 * 1_000_000 = 492_000_000 ≥ 950_000 * 497 = 472_150_000` → passes. Consensus promotion to QuantitativeType. `consensusScore: "0.989939"` (492/497, 6dp string). SNP manifest records currency stripping → `viz:wasNormalized: true`.

- **created_at:** Fandaws consulted, no match. Static cascade: all strings, consensus 1.0. Field name `"created_at"` matches temporal pattern `/(created)(_at)$/i`. Temporal detection fires → TemporalType.

-----

## Appendix C — Changelog (v1.2 → v2.0)

|Change|Sections Affected|Description|
|------|-----------------|-----------| 
|**consensusScore as string**|§2.6, §5.3, §9.3, §13.3, Appendix B|`viz:consensusScore` is now a JSON **string** with exactly 6 decimal places (e.g., `"0.989939"`) rather than a JSON number. Eliminates the `toFixed(6)` trailing-zero problem where `JSON.stringify` drops trailing zeros from numeric literals (`1.000000` → `1`), breaking byte-identity. The `sas:consensusNumerator` / `sas:consensusDenominator` integer pair remains the authoritative machine-readable value.|
|**Schema-level vs field-level fatals**|§5.1, §10|Clarified that only **schema-level** fatal diagnostics (SAS-007) set `status: "error"` and omit the schema. **Field-level** fatals (SAS-013) mark the affected field as `viz:UnknownType` but allow schema emission to continue. One bad column does not block all fields.|
|**Synchronous-only API**|§4.3, §8|Removed the async escape hatch. `align` is explicitly synchronous (returns `SASResult`, not `Promise`). `FandawsScope` methods must be synchronous. Callers with async data sources must resolve to an in-memory scope before invocation.|
|**THRESH_SCALE integer arithmetic**|§6.1, §9.3, §13.1, Appendix B|Canonicalized the integer threshold formula: `typeDistribution[T] * THRESH_SCALE >= scaledThreshold * nonNullTotal` where `THRESH_SCALE = 1_000_000`. Eliminates implementation drift from ad-hoc scale factors. Added overflow analysis and 64-bit integer requirement.|
|**Fandaws tie-breaker**|§6.7.1, §4.3|SAS now sorts `resolveTerm` results by `id` (lexicographic) before selecting the first concept. This is a defensive tie-breaker that guarantees determinism even when the caller's scope ordering is buggy.|
|**normalizeFieldName simplified**|§5.5|Removed the vestigial percent-encoding step 7. Steps 2–5 produce only `[a-z0-9\-]` by construction; no further encoding is needed. Added note that Unicode names are replaced (not transliterated) to preserve determinism.|
|**JSON-LD vs JCS interplay**|§2.6|Documented that JCS-canonicalized bytes are the authoritative interchange form. JSON-LD expand/compact operations produce non-byte-identical representations, which is expected and acceptable.|
|**Diagnostic examples**|§10|Added concrete `context` and `remediation` examples for SAS-013 and SAS-014.|

-----

## Appendix D — Changelog (v1.1 → v1.2)

|Change|Sections Affected|Description|
|------|-----------------|-----------| 
|**Serialization & canonicalization**|New §2.6, §2.2, §13.1|Added JCS (RFC 8785) canonicalization requirement. Defined key ordering (lexicographic), array ordering (CISM property order), and numeric formatting (6dp half-even). Consensus now emits `sas:consensusNumerator` / `sas:consensusDenominator` alongside the rounded `viz:consensusScore`.|
|**Integer-based threshold comparison**|§6.1, §9.3|Consensus threshold check now uses integer arithmetic (`count * 100 >= threshold * nonNullTotal * 100`) to eliminate floating-point comparison ambiguity at threshold boundaries.|
|**Field IRI normalization**|New §5.5, §5.3|Defined `normalizeFieldName()` algorithm (NFC → lowercase → replace non-alphanum → collapse hyphens → trim) with deterministic collision resolution (append `-1`, `-2` by CISM order).|
|**Fandaws determinism contract**|§4.3|Required `FandawsScope` methods to be synchronous, pure, side-effect-free, and return results in stable priority order. Documented exact Fandaws property names and types used by SAS.|
|**Structured diagnostics**|§5.1, §10|`SASResult` now has `status: "ok" | "error"`. `Diagnostic` interface includes `message` and `remediation` fields. `align` never throws — all errors reported as diagnostics. SAS-007 promoted to `fatal`.|
|**CISM consistency validation**|New §6.1.3, §9.1, §10|Added count-mismatch validation (SAS-013 fatal) and unrecognized typeDistribution key handling (SAS-014 warning).|
|**Schema metadata semantics**|§5.2|Defined precise sourcing for `viz:totalRows` (CISM occurrences or sampling.inputSize), `viz:rowsInspected` (sampling.sampleSize), `sas:fandawsAvailable`, and `sas:alignmentMode`.|
|**Configuration matching rules**|§7|Documented case-sensitivity, whitespace-trimming, and type-eligibility rules for `booleanFields` and `nullVocabulary` config.|
|**Security: Fandaws scope trust**|§14|Added guidance on Fandaws scope injection risk. Caller responsible for ensuring scope is a pure, in-memory implementation.|
|**Union future extension**|New §15.3|Noted future `unionResolutionStrategy` config as a potential v2 addition.|
|**Performance: Fandaws cost model**|New §11.3|Added guidance for large scope implementations (label→concept index, memory considerations).|
|**Cross-runtime testing**|§13.1, §13.2, §13.3|Added cross-runtime determinism tests (Node 18/20 + Chromium), precision boundary tests, Fandaws ordering stability tests, and expanded property invariants.|

-----

## Appendix E — Changelog (v1.0 → v1.1)

|Change|Sections Affected|Description|
|------|-----------------|-----------|
|**Minimum observation threshold**|§6.1, §7, §9.3, §10|Added `minObservationThreshold` (default 5) to prevent small-sample consensus bias. If `nonNullTotal < threshold`, consensus promotion aborts → `viz:UnknownType` + SAS-012. Fixes: 1 integer out of 10,000 nulls no longer yields a 1.0 promotion.|
|**Epistemic Matrix**|§6.7.5, §5.3, §10|Replaced blanket "soft override" for `imported` concepts with an Epistemic Matrix. Imported concepts now cannot override static classifications when `consensusScore > 0.99` — they are recorded as suggestions (SAS-011) instead. Prevents epistemic inversion where unverified bulk imports override pristine structural evidence.|
|**Boolean detection boundary**|§6.3, §15.1|Retracted future value-sampling language. Boolean detection fix belongs in BIBSS (emit `boolean-encoded-string` in `typeDistribution`), not in SAS. SAS's no-value-access boundary is now declared architectural and permanent, not a temporary limitation.|
|**Metric hint restriction**|§6.7.6, §5.3|Clarified `sas:metricHint` as pipeline-internal routing signal only. Must not be surfaced to users — ECVE's `viz:matchedMetric` is authoritative. Prevents split-brain where UI shows metric associations that ECVE later rejects.|

-----

*End of specification.*
