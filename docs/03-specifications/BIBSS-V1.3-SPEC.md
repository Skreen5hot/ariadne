# Brain-in-the-Box Schema Service (BIBSS)

## Technical Specification — Version 1.3

**Status:** Draft  
**Author:** Aaron  
**Date:** 2026-02-28  
**FNSR Component:** Structural Inference Layer  
**Edge-Canonical Compliance:** Full  
**Supersedes:** BIBSS v1.2

---

## Changelog from v1.2

| ID | Section(s) | Severity | Change |
|---|---|---|---|
| C-011 | 7.1.3 | **High** | Boolean narrowing changed from case-sensitive (`"true"`, `"false"` only) to case-insensitive (`/^(true\|false)$/i`). Recognizes Excel/spreadsheet exports that capitalize `TRUE`/`FALSE`. The original case-sensitivity was arbitrary conservatism — matching `"true"` but rejecting `"TRUE"` is no more structurally principled, since both require the same pattern-matching heuristic. |
| C-012 | 7.1.3 | **High** | Removed scientific notation from the Number narrowing rule. CSV values like `"1E5"` remain strings. Scientific notation in CSV is rare and ambiguous (conflicts with spreadsheet cell references like `E5` in exported data). Callers requiring scientific notation parsing should pre-normalize input before passing to BIBSS. |
| C-013 | 9.1 | **High** | Added `typeDistribution` field to `SchemaNode` for primitive nodes. Records per-type observation counts before widening (e.g., `{ "integer": 97, "string": 2, "null": 1 }`). Enables downstream consumers to apply consensus thresholds without re-scanning data. Applies to all primitive nodes regardless of input format (CSV or JSON), correcting the reviewer's framing of this as CSV-specific. |
| C-014 | 20 (new) | **Medium** | Added Section 20: Downstream Integration Architecture, documenting the expected pipeline for consuming services (e.g., ECVE), the clean-input assumption, the semantic adapter pattern, and the distinction between BIBSS's structural sample window and consumer-defined semantic inspection windows. |
| C-015 | 7.1.2 | **Clarification** | Added explicit clean-input assumption: BIBSS expects callers to perform domain-specific pre-processing (currency stripping, locale conversion, etc.) before passing input. BIBSS's normalization is structural, not domain-aware. |

## Cumulative Changelog (from v1.0)

| Version | ID | Section(s) | Severity | Summary |
|---|---|---|---|---|
| v1.1 | C-001 | 8.5, 8.6, 9.1 | Critical | Property-merge algorithm replaces shape-signature unions |
| v1.1 | C-002 | 7.1, 7.3, 8.2 | Critical | Disabled Papa Parse `dynamicTyping`; explicit CSV type narrowing |
| v1.1 | C-003 | 9.2 | Critical | RFC 6901 JSON Pointer node IDs replace dot-delimited IDs |
| v1.1 | C-004 | 6.2, 16, 21 | Major | Documented `MAX_SAFE_INTEGER` precision loss; added `BIBSS-009` |
| v1.1 | C-005 | 8.4 | Minor | N=0 guard in required-field detection |
| v1.2 | C-006 | 8.5.1, 8.5.2 | Critical | Three-tier kind/type classification resolves array widening ambiguity |
| v1.2 | C-007 | 8.5.2 | Minor | Corrected Rule 4 examples |
| v1.2 | C-008 | 17.2, 17.3 | Minor | Mixed-primitive array test cases |
| v1.2 | C-009 | Appendix D | Minor | Array inference worked examples |
| v1.2 | C-010 | 8.5.2 | Clarification | Gap analysis commentary |
| v1.3 | C-011 | 7.1.3 | High | Case-insensitive boolean narrowing |
| v1.3 | C-012 | 7.1.3 | High | Removed scientific notation narrowing |
| v1.3 | C-013 | 9.1 | High | Added `typeDistribution` to SchemaNode |
| v1.3 | C-014 | 20 | Medium | Downstream integration architecture documentation |
| v1.3 | C-015 | 7.1.2 | Clarification | Clean-input assumption for domain pre-processing |

---

## 1. Purpose

The Brain-in-the-Box Schema Service (BIBSS) is a deterministic, fully client-side structural inference engine that accepts CSV or JSON input and produces a Canonical Internal Schema Model (CISM) from which downstream adapters may derive output formats.

BIBSS is a **pure service**. It performs no rendering, no visualization, and exposes no UI. It accepts input, infers structure, and emits schema. Rendering is the responsibility of consuming applications.

All processing occurs locally in the browser. No data is transmitted over the network at runtime.

---

## 2. Governing Principles

### 2.1 Determinism Contract

Given identical input bytes and an identical `InferConfig` object, BIBSS must produce byte-identical CISM output across all invocations, on all conformant JavaScript runtimes. There are no random operations anywhere in the inference pipeline. Any operation that would introduce non-determinism (randomized sampling, `Date.now()` seeding, `Math.random()`) is prohibited.

### 2.2 Edge-Canonical Compliance

BIBSS conforms to the Edge-Canonical First Principle: the service must execute deterministically in a standards-compliant browser with zero runtime network dependencies. All library code must be bundled at build time. No CDN loads, no dynamic imports from remote origins, no service worker fetch interceptions are permitted at inference time.

Build-time tooling (bundlers, test harnesses, package managers) may use the network. The compiled artifact must not.

### 2.3 Separation of Concerns

BIBSS is an inference engine with projection adapters. It is not a converter, not a validator, and not a visualization tool. The internal representation (CISM) is the sole source of truth. All output formats are derived projections of the CISM and must be provably consistent with it.

### 2.4 Structural Purity

BIBSS performs **structural inference only**. It observes the kinds of values (object, array, string, number, boolean, null) and their relationships (nesting, co-occurrence, optionality). It does not interpret the meaning of field names, the format of string values, or the domain semantics of data patterns. The string `"2026-01-15"` is a string. The field name `"email"` is an opaque key. Semantic enrichment is the responsibility of downstream annotation layers or output adapters (see Section 20).

### 2.5 Clean-Input Assumption

BIBSS expects structurally coherent input. Domain-specific pre-processing — currency symbol stripping, locale-aware number formatting, date format normalization, trailing-column removal — is the responsibility of the caller. BIBSS's normalization layer (Section 7) handles structural concerns (whitespace trimming, empty-to-null conversion, key verification). It does not perform domain-aware transformations. See Section 20 for the expected integration pipeline.

---

## 3. Non-Goals (v1.3)

The following are explicitly out of scope and deferred to future versions:

- Semantic inference or natural-language interpretation of field names
- Date, datetime, email, URI, or other format detection (these are semantic, not structural)
- Ontology alignment (BFO, CCO, or otherwise)
- SHACL or RDF generation
- Schema version comparison or diffing
- Schema drift detection or heatmaps
- Validation mode (testing data against a schema)
- Backend storage or persistence
- Any form of rendering or visualization
- Streaming inference beyond bounded sampling
- CSV type narrowing beyond the explicit post-parse pass defined in Section 7.1.3
- Currency, locale, or domain-specific pre-processing (caller responsibility; see Section 2.5)

---

## 4. High-Level Architecture

```
Input (CSV bytes | JSON bytes)
       │
       ▼
┌──────────────────┐
│ Input Adapter     │  ← Format detection, parsing
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Normalization     │  ← Type coercion (CSV only), null handling, key verification
└──────┬───────────┘
       │
       ▼
  Array<Record<string, unknown>>
       │
       ▼
┌──────────────────────────────┐
│ Structural Inference Engine   │  ← Recursive traversal, type resolution,
│                               │    property merging, union detection,
│                               │    type distribution accumulation
└──────┬───────────────────────┘
       │
       ▼
  CISM (Canonical Internal Schema Model)
       │
       ▼
┌──────────────────────────────┐
│ Output Adapter Registry       │
│  ├── JSON Schema Adapter      │
│  ├── (consumer adapters)      │
│  └── Raw CISM Serializer      │
└──────────────────────────────┘
```

Each stage is a pure function. The pipeline is: `Input → Parse → Normalize → Infer → CISM → Output`. No stage may hold mutable state between invocations.

---

## 5. Technology Stack

| Component | Technology | Justification |
|---|---|---|
| CSV parsing | Papa Parse (bundled) | Battle-tested, handles edge cases. `dynamicTyping` disabled; type narrowing is BIBSS-controlled. |
| JSON parsing | Native `JSON.parse` | Runtime-provided, no dependency. See Section 22 (Known Limitations) for precision constraints. |
| Inference engine | Custom recursive engine | No suitable library exists |
| JSON Schema emitter | Custom adapter | Draft 2020-12 compliance requires control |
| Module format | ES Modules | Browser-native, no loader required |
| Build tooling | esbuild or Rollup | Produces single-file bundle |

**No runtime framework dependency.** The service is a library, not an application.

---

## 6. Input Specification

### 6.1 CSV

- Encoding: UTF-8 (BOM tolerated, stripped)
- Delimiter: Auto-detected by Papa Parse (comma, tab, pipe, semicolon)
- Header: First row is treated as header. **Headerless CSV is not supported in v1.3.**
- Structure: Flat tabular only. CSV does not produce nested CISM objects.
- Maximum recommended size: 10MB. Above 10MB, the service emits a warning via the diagnostic channel but does not refuse processing.
- **Pre-processing assumed.** BIBSS expects CSV input to be free of domain-specific formatting (currency symbols, locale-specific thousand separators, etc.). See Section 2.5.

### 6.2 JSON

- Encoding: UTF-8
- Accepted root types:
  - Single object (`{}`)
  - Array of objects (`[{}, {}]`)
  - Array of heterogeneous values (`[1, "a", {}]`)
- Nested structures: Fully supported to arbitrary depth.
- Maximum recommended size: 10MB (same guardrail as CSV).

**Precision limitation:** JavaScript's native `JSON.parse` silently loses precision on integers exceeding `Number.MAX_SAFE_INTEGER` (2^53 − 1, i.e., `9007199254740991`). Values such as Twitter/X snowflake IDs, certain database primary keys, and high-precision financial identifiers may be silently rounded during parsing. This occurs before BIBSS receives the parsed values and cannot be intercepted or corrected without replacing the native JSON parser. This is documented as a known limitation in Section 22.

### 6.3 Format Detection

BIBSS does not require the caller to declare the input format. Detection follows this rule:

1. Trim leading whitespace from input bytes.
2. If the first non-whitespace character is `{` or `[`, treat as JSON.
3. Otherwise, treat as CSV.

This is a heuristic. Callers may override by passing an explicit `format` field in `InferConfig`.

---

## 7. Normalization Layer

The normalization layer converts raw parsed input into a uniform intermediate form: `Array<Record<string, unknown>>`.

### 7.1 CSV Normalization

#### 7.1.1 Parse Configuration

Papa Parse is invoked with `dynamicTyping` **disabled**:

```
header: true
dynamicTyping: false
skipEmptyLines: "greedy"
transformHeader: (h) => h.trim()
```

**Rationale:** Papa Parse's `dynamicTyping` applies opaque regex heuristics that silently coerce values in ways that violate structural fidelity. The string `"00123"` becomes integer `123`, destroying the leading-zero signal. The string `"NaN"` becomes the JavaScript value `NaN`, which has no JSON representation. These coercions occur before BIBSS can observe the original data, making them unauditable and non-reversible.

All CSV values are therefore ingested as strings. Type narrowing is performed by BIBSS in a separate, explicit, deterministic pass (Section 7.1.3).

#### 7.1.2 Post-Parse Transforms

Applied in order after Papa Parse returns:

1. Trim all string values.
2. Empty string → `null` (when `emptyStringAsNull` is `true`; default `true`).
3. Verify all records have identical key sets. If a record is missing a key present in the header, insert the key with value `null`.

**Note:** These transforms are structural. Domain-specific normalization (currency stripping, locale-aware number formatting, date conversion) must be performed by the caller before BIBSS receives the input. See Section 2.5 and Section 20.

#### 7.1.3 CSV Type Narrowing Pass

After post-parse transforms, BIBSS applies a deterministic type-narrowing pass to each non-null string value. The rules are applied in order; the first match wins:

| Rule | Condition | Result Type | Result Value |
|---|---|---|---|
| Null | value is `null` (from step 2 above) | `null` | `null` |
| Boolean | value matches `/^(true\|false)$/i` (case-insensitive) | `boolean` | `true` or `false` |
| Integer | value matches `/^-?(?:0\|[1-9][0-9]*)$/` and parsed result ≤ `MAX_SAFE_INTEGER` | `integer` | Parsed via `Number()` |
| Number | value matches `/^-?[0-9]+\.[0-9]+$/` | `number` | Parsed via `Number()` if result is finite; remains `string` otherwise |
| String | No prior rule matched | `string` | Original trimmed value |

**Critical constraints on these rules:**

- **Case-insensitive booleans:** `"true"`, `"True"`, `"TRUE"`, `"false"`, `"False"`, `"FALSE"` all narrow to boolean. These are the standard boolean representations exported by Excel, Google Sheets, and database export tools. The strings `"yes"`, `"no"`, `"1"`, `"0"` are **not** narrowed — these carry categorical semantics beyond structural boolean representation.
- **Leading zeros disqualify integer narrowing:** `"00123"` remains a string. This preserves ZIP codes, product codes, and zero-padded identifiers. The integer regex requires either exactly `"0"` or a non-zero leading digit.
- **Integers exceeding `MAX_SAFE_INTEGER` remain strings** to avoid silent precision loss.
- **No scientific notation narrowing.** Values like `"1e5"`, `"1E5"`, `"2.5E+3"` remain strings. Scientific notation in CSV is rare and ambiguous — `"1E5"` conflicts with spreadsheet cell references in exported data. Callers requiring scientific notation support should pre-normalize these values before passing to BIBSS.
- **`"NaN"`, `"Infinity"`, `"-Infinity"` are not narrowed.** They remain strings.
- **No decimal with exponent:** The Number rule matches only plain decimal notation (`"3.14"`, `"-0.5"`). This is intentionally conservative.

This pass is the only point in the CSV pipeline where types are inferred. Every narrowing decision is auditable against the rules above.

### 7.2 JSON Normalization

- Single object → wrapped in array: `[object]`.
- Array of objects → used directly.
- Array of primitives → each primitive wrapped: `[{ _value: primitive }]`.
- Nested objects and arrays are **not flattened**. They are preserved for recursive traversal by the inference engine.

JSON values arrive pre-typed from `JSON.parse`. No type narrowing is applied to JSON input; the JavaScript runtime's type assignments are accepted as-is (subject to the precision limitation documented in Section 6.2).

### 7.3 Integer Detection from Parsed Values

Applicable to JSON input and to the results of CSV type narrowing. A numeric value `v` is classified as `integer` if and only if:

```
typeof v === "number" && Number.isFinite(v) && Number.isInteger(v)
```

All other numeric values are classified as `number`.

---

## 8. Structural Inference Engine

### 8.1 Core Behavior

The engine accepts `Array<Record<string, unknown>>` and produces a single CISM root node. It operates by recursive descent:

1. For each record in the array, traverse all properties.
2. For each property, determine the structural kind (object, array, primitive, null).
3. Accumulate observations across all records, **including per-type counts** for the `typeDistribution` field.
4. Resolve each property's type using the type widening lattice and required-field rules.
5. For nested objects, recurse.
6. For arrays, infer the item type using the array inference algorithm (Section 8.5).

### 8.2 Primitive Type Enumeration

```typescript
type Primitive = "string" | "number" | "integer" | "boolean" | "null"
```

These are the only leaf types in the CISM.

### 8.3 Type Widening Lattice

Type conflicts are resolved by a **total order** over primitive types. When two different primitive types are observed for the same property across records, the wider type wins.

The widening order is:

```
null < boolean < integer < number < string
```

Rules:

- If types `A` and `B` are observed, the resolved type is `max(A, B)` in the lattice.
- `null` does not widen the resolved type; it sets the `nullable` flag.
- `boolean + integer` → `integer` (boolean is narrower).
- `integer + number` → `number`.
- `number + string` → `string`.
- Any type + `null` → that type with `nullable: true`.

**There is no probabilistic inference.** The widening lattice is applied mechanically.

**Scope of the lattice:** The type widening lattice governs ALL resolution of mixed primitive types, regardless of where the mixing occurs — across records for a single property, or across elements within a single array. There is one lattice and one set of rules. The lattice does not change behavior based on context. This is the governing principle that resolves the v1.1 ambiguity documented in Section 8.5.2.

**Relationship to `typeDistribution`:** The lattice determines the `primitiveType` of the resolved node. The `typeDistribution` field (Section 9.1) preserves the pre-widening observation counts. Downstream consumers that apply consensus thresholds (e.g., "95% of values are integer, so treat as integer despite 2 strings") use `typeDistribution`, not the lattice output. The lattice gives the structural worst-case; `typeDistribution` enables practical best-fit.

### 8.4 Required Field Detection

For a property `P` observed across a population of `N` objects:

```
if N === 0:
  required = false

otherwise:
  required = (occurrenceCount(P) / N) >= requiredThreshold
```

Where `requiredThreshold` is a configuration value (default: `1.0`, meaning 100% presence required).

The `N === 0` guard prevents a `0/0` division that would produce `NaN`, which JavaScript evaluates as `false` under `>=` comparison. While functionally equivalent in this specific case, the explicit guard makes the spec unambiguous and eliminates reliance on IEEE 754 edge-case behavior.

The threshold is a `>=` comparison, not strict equality, to allow configurable relaxation (e.g., `0.95` to tolerate 5% missing values).

### 8.5 Array Inference Algorithm

When the inference engine encounters an array value, it must determine a single item schema for the array's `itemType`. The elements of the array are treated as a sub-population.

#### 8.5.1 Three-Tier Classification Model

BIBSS classifies each array element using a **three-tier** model. This model resolves the v1.1 ambiguity where the kind classification table grouped all primitives under a single "primitive" kind, creating a gap in the decision tree for arrays containing mixed primitive types (e.g., `[true, 1, "hello"]`).

**Tier 1: Composite Kind**

The top-level structural distinction. There are exactly four composite kinds:

| JavaScript value | Composite Kind |
|---|---|
| `v === null` | `null` |
| `Array.isArray(v)` | `array` |
| `typeof v === "object" && v !== null && !Array.isArray(v)` | `object` |
| all other values | `primitive` |

Composite kind determines whether a union is necessary. **Unions are produced only when array elements span multiple non-null composite kinds** (e.g., some elements are `primitive` and some are `object`).

**Tier 2: Primitive Kind**

Within composite kind `primitive`, each value has a primitive kind:

| JavaScript value | Primitive Kind |
|---|---|
| `typeof v === "boolean"` | `boolean` |
| `typeof v === "number"` (integer) | `integer` |
| `typeof v === "number"` (non-integer) | `number` |
| `typeof v === "string"` | `string` |

Primitive kind determines how the type widening lattice is applied. **Mixed primitive kinds within an array are resolved by the widening lattice, not by unions.** This is identical to how mixed primitive types are resolved for a single property across multiple records.

**Tier 3: Primitive Type (the lattice output)**

The resolved type after applying the widening lattice across all observed primitive kinds. This is the `primitiveType` field on the resulting CISM `SchemaNode`.

#### 8.5.2 The Array Inference Decision Tree

The engine classifies all elements by composite kind, then applies the following rules **in order**. The first matching rule determines the outcome.

**Rule 1 — All null:** All elements are `null`.

→ `itemType` is `{ kind: "primitive", primitiveType: "null", nullable: true }`.

**Rule 2 — Single composite kind plus optional nulls:** All non-null elements share the same composite kind.

→ Dispatch to the appropriate handler:

- **All primitives (possibly mixed primitive kinds):** Collect the primitive kind of each non-null element. Apply the type widening lattice across all observed primitive kinds to produce a single resolved primitive type. Accumulate `typeDistribution` counts. If any elements are `null`, set `nullable: true`.

  Example: `[true, 1, 2, null]` → primitive kinds are `boolean, integer, integer`. Lattice resolves `boolean + integer → integer`. `typeDistribution: { "boolean": 1, "integer": 2, "null": 1 }`. Null present → `nullable: true`. Result: `{ kind: "primitive", primitiveType: "integer", nullable: true }`.

  Example: `[1, 3.14, "hello"]` → primitive kinds are `integer, number, string`. Lattice resolves `integer + number → number`, then `number + string → string`. `typeDistribution: { "integer": 1, "number": 1, "string": 1 }`. Result: `{ kind: "primitive", primitiveType: "string", nullable: false }`.

- **All objects:** Apply the property-merge algorithm (Section 8.5.3). If any elements are `null`, set `nullable: true` on the resulting object node.

- **All arrays:** Recurse. The `itemType` is itself an array node whose own `itemType` is inferred from the collected inner elements across all sub-arrays. If any elements are `null`, set `nullable: true`.

**Rule 3 — Multiple composite kinds:** Non-null elements span two or more composite kinds (e.g., some are `primitive` and some are `object`, or some are `object` and some are `array`).

→ Produce a `union` node. Union members are constructed as follows:

1. Group non-null elements by composite kind.
2. For each group, apply the appropriate inference:
   - Primitive group → widen via lattice to a single primitive type. Accumulate `typeDistribution`.
   - Object group → merge via property-merge algorithm.
   - Array group → recurse to infer array item type.
3. Each group produces one union member. The union has at most 3 members (primitive, object, array).
4. If any elements are `null`, set `nullable: true` on the union node itself.

**Rule 4 — Empty array:** The array has zero elements.

→ `itemType` is `null`. Diagnostic `BIBSS-007` is emitted.

#### 8.5.2.1 Why This Resolves the v1.1 Ambiguity

In v1.1, the kind classification table assigned `boolean`, `number`, and `string` the same kind: `primitive`. The decision tree's Rule 1 was stated as "All elements are the same primitive type," while Rule 4 cited "some integers and some booleans" as a union trigger. These statements contradicted each other and the type widening lattice:

- The kind table said `boolean` and `integer` are the same kind (`primitive`).
- Rule 1 required the "same primitive type," excluding mixed primitives.
- Rule 4 cited mixed primitives as a union case.
- The widening lattice said `boolean + integer → integer` (not a union).

The three-tier model eliminates this by introducing an explicit level of distinction:

- **Composite kind** (`primitive` vs. `object` vs. `array`) governs the **merge-or-union** decision.
- **Primitive kind** (within composite kind `primitive`) governs which **lattice rule** applies.
- **Unions are never produced from primitive-only arrays.** The lattice always resolves them.

This is consistent with property-level inference: if a field `age` contains `true` in one record and `42` in another, the lattice resolves it to `integer` — it does not produce a union. The same logic now applies identically within arrays.

#### 8.5.3 Property-Merge Algorithm for Object Arrays

Given an array of `N` object elements (after filtering out nulls), the algorithm produces a single merged object schema:

```
1. Collect the union of all property keys across all N elements.
   Call this set K.

2. For each key k in K:
   a. Collect the values of k from every element where k is present.
   b. Infer the type of k by applying the widening lattice across
      all observed values (recursing for nested objects/arrays).
      Accumulate typeDistribution for primitive-valued properties.
   c. Count the number of elements where k is present: occurrences(k).
   d. If any element lacks k entirely, and any element where k IS
      present has a non-null value, mark k as nullable: false but
      required: false (absence ≠ null; the key simply doesn't exist
      in some elements).
   e. If k is present in some elements with value null:
      set nullable: true on k's target node (independent of step d).
   f. Apply the required-field threshold:
      required(k) = (occurrences(k) / N) >= requiredThreshold

3. Return a single object SchemaNode with all keys from K as
   properties, each annotated with required, nullable, and the
   inferred target type.
```

**Example:** Given these array elements:

```json
[
  { "id": 1, "name": "Alice", "role": "admin" },
  { "id": 2, "name": "Bob" },
  { "id": 3, "name": null, "role": "user", "dept": "eng" }
]
```

The merged schema (at threshold 1.0) is:

| Property | Type | Required | Nullable | Occurrences | typeDistribution |
|---|---|---|---|---|---|
| `id` | integer | true | false | 3/3 | `{ "integer": 3 }` |
| `name` | string | true | true | 3/3 (one null) | `{ "string": 2, "null": 1 }` |
| `role` | string | false | false | 2/3 | `{ "string": 2 }` |
| `dept` | string | false | false | 1/3 | `{ "string": 1 }` |

This produces **one** object node with four properties — not a union of three distinct shapes.

#### 8.5.4 Union Bounds

Under the three-tier model, union members are bounded by the number of non-null composite kinds, which is exactly 3: `primitive`, `object`, `array`. A union node therefore has at most 3 members. In practice, most unions have 2 members (typically primitive + object).

The v1.0 union explosion (2^P members for P optional properties) is structurally impossible under v1.1+. The v1.1 ambiguity around mixed primitive unions is structurally impossible under v1.2+, because the lattice — not the union mechanism — governs all primitive type conflicts.

### 8.6 Empty and Degenerate Inputs

| Input condition | Behavior |
|---|---|
| Empty CSV (header only, no rows) | CISM with object node, all properties typed `string` (CSV default), all optional. `N=0`, so required-field guard applies. `typeDistribution` is `{}` for all properties. |
| Empty JSON array (`[]`) | CISM with array node, `itemType: null` |
| Empty JSON object (`{}`) | CISM with object node, no properties |
| All values null for a property | Property typed as `null`, `nullable: true`. `typeDistribution: { "null": N }`. |
| Single record | All present properties marked required (at threshold 1.0). N=1, occurrences=1. |
| Array with zero elements | `itemType: null`. Diagnostic `BIBSS-007` emitted. |

---

## 9. Canonical Internal Schema Model (CISM)

The CISM is the sole internal representation. All outputs are projections of this model.

### 9.1 Data Structures

```typescript
interface CISMRoot {
  version: "1.3"
  generatedAt: string          // ISO 8601 timestamp of generation
  config: InferConfig          // The configuration used to produce this CISM
  root: SchemaNode
  nodeIndex: Map<string, SchemaNode>  // All nodes indexed by ID (omitted from serialization)
}

interface SchemaNode {
  id: string                   // RFC 6901 JSON Pointer path (see Section 9.2)
  kind: "object" | "array" | "primitive" | "union"
  name?: string                // Human-readable label (property name or root)
  occurrences: number          // How many times this structure was observed

  // kind: "object"
  properties?: SchemaEdge[]

  // kind: "array"
  itemType?: SchemaNode

  // kind: "primitive"
  primitiveType?: Primitive
  nullable?: boolean
  typeDistribution?: Record<Primitive, number>  // See Section 9.4

  // kind: "union"
  members?: SchemaNode[]       // One per distinct composite kind (max 3; see Section 8.5.4)
  nullable?: boolean           // True if any array elements were null
}

interface SchemaEdge {
  name: string                 // Property name (unescaped)
  target: SchemaNode
  required: boolean
  occurrences: number          // Times this property was observed
  totalPopulation: number      // Size of parent object population
}
```

### 9.2 Node Identity: RFC 6901 JSON Pointer Paths

CISM node IDs use **RFC 6901 JSON Pointer** syntax. This eliminates ambiguity caused by property names containing dots, slashes, tildes, or other special characters.

#### 9.2.1 Escaping Rules (per RFC 6901)

Within each path segment:

1. `~` is escaped as `~0`
2. `/` is escaped as `~1`

No other characters require escaping.

#### 9.2.2 ID Generation Rules

```
rootId             = "#"
objectChildId      = parentId + "/" + escape(propertyName)
arrayItemId        = parentId + "/[]"
unionMemberId      = parentId + "/|" + memberIndex
```

#### 9.2.3 Examples

| Structure | ID |
|---|---|
| Root node | `#` |
| Property `customer` on root | `#/customer` |
| Nested property `address` on `customer` | `#/customer/address` |
| Item type of `orders` array | `#/orders/[]` |
| First union member inside array items | `#/orders/[]/|0` |
| Property named `user.name` (literal dot in key) | `#/user.name` |
| Property named `a/b` (literal slash in key) | `#/a~1b` |
| Property named `a~b` (literal tilde in key) | `#/a~0b` |

#### 9.2.4 Collision Proof

Under v1.0's dot-delimited scheme, the property key `"user.name"` and the nested path `user → name` both produced `root.user.name`. Under RFC 6901:

- Literal key `"user.name"` → `#/user.name` (dot is not a separator in JSON Pointer)
- Nested path `user → name` → `#/user/name` (slash is the separator)

These are distinct strings. No collision is possible for any valid JSON key, because `/` in key names is escaped to `~1`.

**Consequence:** Two properties with identical shapes but different paths produce distinct CISM nodes. Shape-based deduplication remains deferred to future versions.

### 9.3 Serialization

The CISM is serializable to JSON. The `nodeIndex` map is omitted from serialization (it is reconstructable from the tree). The serialized form includes `version`, `generatedAt`, `config`, and `root`.

Serialization must be deterministic: property keys are emitted in declaration order as defined in Section 9.1, arrays preserve insertion order, and no non-deterministic metadata (e.g., runtime memory addresses) may appear. Within `typeDistribution` objects, keys are emitted in lattice order: `null`, `boolean`, `integer`, `number`, `string`. Only keys with non-zero counts are included.

### 9.4 Type Distribution

The `typeDistribution` field on `SchemaNode` records the count of each primitive type observed **before** the widening lattice resolves to a single type. It is present on all `SchemaNode` instances where `kind === "primitive"`, regardless of whether the input was CSV or JSON.

**Purpose:** The widened `primitiveType` represents the structural worst-case type — the minimum type that accommodates every observed value. The `typeDistribution` preserves the pre-widening evidence, enabling downstream consumers to apply different resolution strategies:

- **Consensus thresholds:** A consumer might decide that if 95% of values are integer and 5% are string, the field should be treated as integer (with the strings flagged as anomalies). BIBSS does not make this judgment; it provides the data for the consumer to do so.
- **Data quality signals:** A distribution of `{ "integer": 997, "string": 3 }` strongly suggests the 3 strings are data-entry errors, not a genuine mixed-type field.
- **Visualization type mapping:** A consuming visualization service can use distribution data to select between quantitative and nominal rendering.

**Accumulation rules:**

1. For each value observed during inference, classify it by primitive kind (the Tier 2 classification from Section 8.5.1 for array elements, or the direct `typeof` result for property values).
2. Increment the count for that primitive kind in the `typeDistribution` map.
3. `null` values increment the `"null"` count.
4. For JSON input, types are determined by `JSON.parse` output. For CSV input, types are determined by the narrowing pass (Section 7.1.3).

**Serialization:** Keys appear in lattice order (`null`, `boolean`, `integer`, `number`, `string`). Zero-count keys are omitted. The sum of all values in `typeDistribution` equals `occurrences`.

**Example:** A CSV column with 100 rows: 95 parse as integer, 3 parse as string, 2 are empty (null):

```json
{
  "primitiveType": "string",
  "nullable": true,
  "typeDistribution": { "null": 2, "integer": 95, "string": 3 },
  "occurrences": 100
}
```

The lattice resolves `integer + string → string`, so `primitiveType` is `"string"`. But the distribution reveals that a consensus-based consumer should likely treat this as integer.

---

## 10. Sampling Strategy

### 10.1 Deterministic Strided Sampling

When the input record count exceeds `sampleSize` (default: 2000), BIBSS applies deterministic strided sampling:

1. Always include the first `floor(sampleSize / 2)` records.
2. For the remaining records, compute a stride: `stride = floor(remainingRecords / (sampleSize / 2))`.
3. Select every `stride`-th record from the remainder.

This produces exactly `sampleSize` records (±1 due to integer rounding) with no randomness.

**Rationale:** Strided sampling is the mathematically correct choice given the determinism contract. Any randomized approach (even with a seeded PRNG) introduces implementation-specific behavior across JavaScript runtimes. Strided sampling is fully specified by the input length and `sampleSize`; two implementations given the same inputs must select the same records.

### 10.2 Merge Semantics

The sampled records are treated as a **single flat population**. The inference engine makes one pass over the combined sample. There is no separate merge step. Occurrence counts, type observations, and `typeDistribution` counts are accumulated over the full sample as if it were the complete dataset.

### 10.3 Sample Indicator

When sampling is applied, the CISM root includes:

```typescript
interface CISMRoot {
  // ... existing fields ...
  sampling?: {
    applied: boolean
    inputSize: number
    sampleSize: number
    strategy: "strided"
  }
}
```

This allows downstream consumers to know that the schema was inferred from a subset.

---

## 11. Output Adapters

Output adapters are pure functions: `(cism: CISMRoot) → OutputFormat`. They may not modify the CISM. They may not access any state beyond their input.

### 11.1 JSON Schema Adapter

**Target:** JSON Schema Draft 2020-12.

#### Mapping Rules

| CISM Kind | JSON Schema |
|---|---|
| `object` | `{ "type": "object", "properties": {...}, "required": [...] }` |
| `array` | `{ "type": "array", "items": {...} }` |
| `primitive` | `{ "type": "<primitiveType>" }` |
| `primitive (nullable)` | `{ "type": ["<primitiveType>", "null"] }` |
| `union` | `{ "oneOf": [...members] }` |
| `union (nullable)` | `{ "oneOf": [...members, { "type": "null" }] }` |

**Note:** The `typeDistribution` field is not represented in JSON Schema output. It is structural metadata for downstream consumers, not a schema constraint.

#### `$ref` and `$defs` Strategy

In v1.3, all schemas are **inlined**. No `$ref` or `$defs` are emitted. This is a deliberate simplification.

**Rationale:** Because CISM nodes are path-scoped (not shape-deduplicated), there are no shared definitions to reference. When shape-based deduplication is added in a future version, `$ref`/`$defs` support will be added simultaneously.

#### Root Type Selection

- If the input was CSV → root is `{ "type": "array", "items": {...} }`.
- If the input was a JSON array → root is `{ "type": "array", "items": {...} }`.
- If the input was a single JSON object → root is `{ "type": "object", ... }`.

#### Schema Metadata

The emitted schema includes:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:bibss:inferred:<sha256-of-input-first-1024-bytes>",
  "title": "Inferred Schema",
  "$comment": "Generated by BIBSS v1.3"
}
```

### 11.2 Raw CISM Adapter

Emits the CISM as a JSON document, as defined in Section 9.3. This is the identity adapter. The `typeDistribution` field is included in the raw CISM output.

### 11.3 Adapter Registry

Adapters are registered by name and invoked by the public API:

```typescript
type OutputAdapter<T> = (cism: CISMRoot) => T

interface AdapterRegistry {
  register(name: string, adapter: OutputAdapter<unknown>): void
  get(name: string): OutputAdapter<unknown> | undefined
  list(): string[]
}
```

This allows consuming applications to register custom adapters without modifying BIBSS internals. See Section 20 for the expected pattern when building semantic adapters for downstream services.

---

## 12. Public API

BIBSS exposes a single entry point:

```typescript
interface BIBSS {
  /**
   * Infer schema from raw input.
   * Returns the CISM and a set of diagnostics.
   */
  infer(input: string | ArrayBuffer, config?: Partial<InferConfig>): InferResult

  /**
   * Project the CISM through a named output adapter.
   */
  project<T>(cism: CISMRoot, adapterName: string): T

  /**
   * Access the adapter registry.
   */
  adapters: AdapterRegistry
}

interface InferResult {
  cism: CISMRoot | null
  diagnostics: Diagnostic[]
}

interface Diagnostic {
  level: "info" | "warning" | "error"
  code: string
  message: string
  context?: Record<string, unknown>
}
```

### 12.1 Diagnostic Codes

| Code | Level | Condition |
|---|---|---|
| `BIBSS-001` | warning | Input exceeds 10MB |
| `BIBSS-002` | info | Sampling applied |
| `BIBSS-003` | warning | CSV row has mismatched column count |
| `BIBSS-004` | error | JSON parse failure |
| `BIBSS-005` | error | CSV parse failure |
| `BIBSS-006` | warning | Property name collision after trimming |
| `BIBSS-007` | info | Empty input (zero records or zero-element array) |
| `BIBSS-008` | warning | Array with >100 distinct property keys across elements (possible heterogeneous data) |
| `BIBSS-009` | warning | JSON input contains numeric values exceeding `Number.MAX_SAFE_INTEGER`; precision loss may have occurred |

#### BIBSS-009 Detection

Because `JSON.parse` silently rounds large integers, detection is heuristic. BIBSS performs a regex pre-scan on the raw JSON input string for integer literals matching `[0-9]{16,}` (16+ digit sequences). If any are found, `BIBSS-009` is emitted. This does not prevent processing; it alerts the consumer that the CISM's numeric types for affected fields may reflect rounded values.

---

## 13. Configuration

```typescript
interface InferConfig {
  /** Minimum presence ratio for a field to be marked required. Default: 1.0 */
  requiredThreshold: number

  /** Treat empty strings as null during CSV normalization. Default: true */
  emptyStringAsNull: boolean

  /** Maximum records to process before sampling kicks in. Default: 2000 */
  sampleSize: number

  /** Override format detection. Default: undefined (auto-detect). */
  format?: "csv" | "json"

  /** Maximum file size in bytes before warning. Default: 10485760 (10MB) */
  maxSizeWarning: number
}
```

All configuration values have defaults. Passing an empty object or `undefined` produces valid behavior.

---

## 14. Error Handling

### 14.1 Philosophy

BIBSS does not throw exceptions during inference. All errors are captured as `Diagnostic` entries with `level: "error"` in the `InferResult`. The `cism` field is `null` if inference could not proceed (e.g., unparseable input).

### 14.2 Specific Error Conditions

| Condition | Behavior |
|---|---|
| Malformed JSON (syntax error) | `cism: null`, diagnostic `BIBSS-004` |
| Malformed CSV (parse failure) | `cism: null`, diagnostic `BIBSS-005` |
| CSV with mismatched row lengths | Pad short rows with `null`, truncate long rows to header length, emit `BIBSS-003` per affected row (capped at 10 diagnostics) |
| Empty string input | `cism: null`, diagnostic `BIBSS-007` |
| Non-UTF-8 encoding | Behavior undefined in v1.3. Documented as known limitation (Section 22). |
| Circular JSON references | Not possible via `JSON.parse`. No handling required. |
| Large integer in JSON | Processing continues; `BIBSS-009` emitted if detected by pre-scan |

---

## 15. Performance

### 15.1 Complexity

Worst-case time complexity:

```
O(S × D × P)
```

Where:

- `S` = number of sampled records (bounded by `sampleSize`)
- `D` = maximum nesting depth
- `P` = average property count per object

For typical tabular data (D=1), this reduces to `O(S × P)`.

The `typeDistribution` accumulation adds no asymptotic cost — it is a constant-time map increment per value observation, performed within the existing traversal loop.

### 15.2 Memory

The CISM is a tree of bounded size: one node per unique path in the schema. For a dataset with `P` properties and maximum depth `D`, the CISM has at most `P^D` nodes. In practice, schema trees rarely exceed a few hundred nodes even for complex JSON.

**Union memory bound:** Union nodes have at most 3 members (one per composite kind). This is a structural guarantee of the three-tier model, not a configurable limit.

**`typeDistribution` memory:** Each primitive node's `typeDistribution` map has at most 5 entries (one per primitive type). Memory overhead is O(1) per primitive node.

### 15.3 Benchmarks (Target)

| Input | Records | Properties | Target Time |
|---|---|---|---|
| Flat CSV | 2,000 | 20 | < 50ms |
| Nested JSON | 2,000 | 50 (across depth 4) | < 200ms |
| Wide CSV | 2,000 | 500 | < 500ms |
| JSON array with 20 optional properties | 2,000 | 20 | < 100ms |
| JSON array with mixed primitives | 2,000 | 10 | < 50ms |

These are targets, not guarantees. Actual performance depends on the runtime.

---

## 16. Security Considerations

- **No network calls at runtime.** The bundled artifact makes zero HTTP requests.
- **No data persistence.** Input and output exist only in memory during execution. BIBSS writes nothing to `localStorage`, `IndexedDB`, cookies, or any other storage mechanism.
- **No `eval` or dynamic code generation.** All inference logic is statically defined.
- **Large file guardrail.** Inputs exceeding `maxSizeWarning` emit a diagnostic. The service does not enforce a hard limit (the caller is responsible for resource management), but the diagnostic serves as a signal.
- **No prototype pollution.** JSON parsing uses `JSON.parse` without a reviver that copies to `Object.prototype`. Object traversal uses `Object.hasOwn()` or equivalent, never bare `in` operator on untrusted keys.
- **Integer precision.** JavaScript's `Number` type cannot faithfully represent integers above 2^53 − 1. Consumers handling data with large integer identifiers (snowflake IDs, certain database keys) should be aware that the CISM may reflect rounded values for those fields. See Section 22.
- **CSV injection.** BIBSS does not execute formulas or expressions found in CSV cells. All values are treated as inert data. However, BIBSS does not sanitize output; downstream consumers that render CSV-derived values in contexts where formula injection is possible (e.g., spreadsheet applications) must implement their own sanitization.

---

## 17. Testing Contract

### 17.1 Determinism Tests

For every test case, the following must hold:

```
JSON.stringify(infer(input, config).cism) === JSON.stringify(infer(input, config).cism)
```

Serialized CISM output must be byte-identical across invocations. This includes `typeDistribution` maps, which must serialize in lattice key order.

### 17.2 Required Test Cases

| Category | Cases |
|---|---|
| Empty inputs | Empty CSV, empty JSON array, empty JSON object, zero-byte input |
| Type widening | All pairs in the lattice: null↔boolean, boolean↔integer, integer↔number, number↔string, three-way combinations |
| Nullable | Property observed as string in some records, null in others |
| Required fields | 100% presence, 99% presence (at threshold 1.0), configurable threshold, **N=0 population** |
| Nested objects | Depth 1 through depth 5 |
| Arrays (homogeneous primitives) | All-string, all-integer, all-boolean arrays |
| Arrays (mixed primitives) | `[true, 1, 2]` → integer (not union). `[1, "hello"]` → string (not union). `[true, 3.14]` → number (not union). `[true, 1, 3.14, "x"]` → string (not union). These MUST produce a single primitive node, never a union. |
| Arrays (objects, optional props) | Objects with 5 optional properties across 100 elements. Must produce 1 merged object, not 2^5 unions. |
| Arrays (cross-kind union) | `[1, {"a": 2}]` → union of primitive (integer) and object. `["x", [1,2]]` → union of primitive (string) and array. |
| Arrays (mixed kinds + null) | `[1, {"a": 2}, null]` → union of primitive and object, nullable. |
| CSV boolean narrowing | `"true"` → boolean, `"True"` → boolean, `"TRUE"` → boolean, `"false"` → boolean, `"False"` → boolean, `"FALSE"` → boolean, `"yes"` → string, `"1"` → integer, `"0"` → integer |
| CSV no scientific notation | `"1e5"` → string, `"1E5"` → string, `"2.5E+3"` → string, `"-1e-2"` → string |
| CSV type narrowing (other) | `"00123"` → string, `"123"` → integer, `"NaN"` → string, `""` → null (if configured) |
| CSV edge cases | Quoted fields, embedded commas, embedded newlines, BOM, mixed line endings |
| typeDistribution | Column with 95 integers, 3 strings, 2 nulls → `primitiveType: "string"`, `typeDistribution: { "null": 2, "integer": 95, "string": 3 }`. Sum of distribution values equals `occurrences`. |
| typeDistribution (JSON) | JSON field with integers in 50 records and numbers in 50 → `typeDistribution: { "integer": 50, "number": 50 }`. Verify distribution works for JSON, not only CSV. |
| typeDistribution (arrays) | Array `[1, 2, "x"]` → `typeDistribution: { "integer": 2, "string": 1 }` on the primitive itemType node. |
| Node identity (RFC 6901) | Key `"user.name"` and nested `user.name` produce distinct IDs. Key `"a/b"` is escaped as `a~1b`. Key `"a~b"` is escaped as `a~0b`. |
| Sampling | Input at exactly sampleSize, sampleSize+1, 10× sampleSize |
| JSON Schema output | Validate emitted schema against JSON Schema Draft 2020-12 meta-schema |
| Large integers | JSON with value `9007199254740993` triggers `BIBSS-009` |

### 17.3 Property-Based Invariants (Recommended)

For any valid input `I` and config `C`:

1. `infer(I, C)` terminates.
2. If `infer(I, C).cism` is non-null, `project(cism, "jsonschema")` produces valid Draft 2020-12.
3. The original input validates against the emitted JSON Schema (the schema is a sound overapproximation).
4. **No CISM produced by `infer()` contains a `union` node where all members have `kind: "object"`.** (Property-merge invariant from v1.1.)
5. **No CISM produced by `infer()` contains a `union` node where all members have `kind: "primitive"`.** (Lattice-widening invariant from v1.2.)
6. **Every `union` node has at most 3 members.** (Composite-kind bound from v1.2.)
7. **For every primitive `SchemaNode` with `typeDistribution`, the sum of all values in `typeDistribution` equals `occurrences`.** (Distribution completeness invariant from v1.3.)

---

## 18. Versioning

### 18.1 CISM Version

The `CISMRoot.version` field is a string following semantic versioning: `"major.minor"`.

- **Major** increments when the CISM structure changes in backward-incompatible ways (fields removed, semantics changed).
- **Minor** increments when fields are added or optional semantics are extended.

v1.3 is the current release. It is backward-compatible with v1.0–v1.2 consumers (the `typeDistribution` field is additive; the `version` field distinguishes behavior).

### 18.2 Compatibility Promise

Any tool that consumes CISM v1.x must be able to consume any CISM v1.y where y ≥ x, by ignoring unrecognized fields. This is a forward-compatibility guarantee for minor versions.

### 18.3 Behavioral Changes Across Versions

| Behavior | v1.0 | v1.1 | v1.2 | v1.3 |
|---|---|---|---|---|
| CSV boolean matching | Papa Parse heuristic | Case-sensitive (`"true"` only) | No change | **Case-insensitive** (`"True"`, `"TRUE"`, etc.) |
| CSV scientific notation | Papa Parse heuristic | Narrowed to number | No change | **Remains string** (removed) |
| Array: objects with optional props | Union of shape signatures (2^P explosion) | Property-merge (single object) | No change | No change |
| Array: mixed primitives | Not clearly specified | Ambiguous | Widened via lattice, never union | No change |
| Node IDs | Dot-delimited | RFC 6901 JSON Pointer | No change | No change |
| Union member bound | Unbounded | Bounded ≤7 | Formally bounded at 3 | No change |
| Type distribution | Not available | Not available | Not available | **`typeDistribution` on all primitive nodes** |

---

## 19. Future Extension Hooks (Explicitly Deferred)

These capabilities are anticipated but not specified. The architecture supports their addition without restructuring the core pipeline.

| Extension | Integration Point |
|---|---|
| Semantic enrichment (field name interpretation) | Post-inference CISM annotation pass |
| Date/datetime/URI format detection | Consumer-side output adapter (see Section 20) |
| Ontology alignment (BFO/CCO mapping) | Output adapter or CISM annotation |
| SHACL generation | Output adapter |
| RDF generation | Output adapter |
| Mermaid diagram | Output adapter |
| D3 graph model | Output adapter |
| Schema version diffing | Separate service consuming two CISMs |
| Schema drift heatmaps | Separate service consuming CISM time series |
| Validation mode | Separate service consuming CISM + data |
| Shape-based node deduplication | CISM post-processing pass, enables `$ref` in JSON Schema |
| BigInt support for large integers | Alternative JSON parser (e.g., `json-bigint`) replacing native `JSON.parse` |
| Configurable CSV narrowing rules | Extension of Section 7.1.3 rule table |

---

## 20. Downstream Integration Architecture

This section documents how consuming services are expected to integrate with BIBSS. It does not specify consumer behavior — that is the consumer's responsibility. It specifies the contract BIBSS offers and the integration patterns it supports.

### 20.1 The Semantic Adapter Pattern

BIBSS produces structural types (`string`, `integer`, `number`, `boolean`, `null`). Consuming services often require semantic types (e.g., Temporal, Nominal, Quantitative, Boolean). The translation from structural to semantic is performed by an **output adapter** registered in BIBSS's adapter registry (Section 11.3).

The adapter is:

- **A pure function** `(cism: CISMRoot) → ConsumerSchemaFormat`.
- **Owned by the consumer**, not by BIBSS. It lives in the consumer's codebase, is registered at the consumer's startup, and is invoked via `bibss.project(cism, "consumer-name")`.
- **The single integration point** where BIBSS's structural world meets the consumer's semantic world.

The adapter may apply any logic to the CISM, including:

- Regex cascades over string field names or values to promote strings to semantic types (Temporal, URI, etc.).
- Consensus thresholds using `typeDistribution` to override the lattice's worst-case type.
- Domain-specific rules (e.g., fields named `*_date` are Temporal).

BIBSS provides the structural evidence. The adapter applies the semantic judgment.

### 20.2 The Expected Integration Pipeline

For a consuming service (e.g., a visualization engine) that needs BIBSS for schema inference, the expected pipeline is:

```
Raw input bytes
       │
       ▼
┌──────────────────────────────┐
│ Consumer Pre-Processing       │  ← Currency stripping, locale conversion,
│ (consumer-owned)              │    date normalization, raw hash computation
└──────┬───────────────────────┘
       │
       ▼
  Cleaned input string
       │
       ▼
┌──────────────────────────────┐
│ BIBSS.infer()                 │  ← Structural inference, type narrowing,
│                               │    distribution accumulation
└──────┬───────────────────────┘
       │
       ▼
  CISM (with typeDistribution)
       │
       ▼
┌──────────────────────────────┐
│ Consumer Semantic Adapter     │  ← Type promotion, consensus thresholds,
│ (consumer-owned, registered   │    JSON-LD serialization, etc.
│  in BIBSS adapter registry)   │
└──────────────────────────────┘
       │
       ▼
  Consumer Schema (e.g., viz:DatasetSchema)
```

**Key boundaries:**

1. The consumer computes any required hashes (e.g., raw input hash) **before** pre-processing, on the original bytes.
2. Pre-processing transforms the raw input into clean input suitable for BIBSS. BIBSS does not see currency symbols, locale-specific separators, or other domain formatting.
3. BIBSS infers structure and produces the CISM with `typeDistribution`.
4. The consumer's adapter transforms the CISM into the consumer's own schema format, applying semantic rules that BIBSS intentionally does not perform.

### 20.3 Structural Sample Window vs. Semantic Inspection Window

BIBSS's `sampleSize` (default: 2000) governs structural completeness — sampling enough records to discover all property keys, nesting patterns, and type variation in potentially heterogeneous data (especially JSON with optional nested structures).

A consuming service may define a separate **semantic inspection window** (e.g., 100 rows) for its own purposes — such as the number of rows within which a type must reach consensus to be promoted from string to a semantic type. This window is smaller because semantic type promotion on flat CSV columns converges quickly.

These two windows serve different purposes and operate at different stages of the pipeline:

- BIBSS's sample window: structural completeness over the full dataset shape.
- Consumer's inspection window: semantic confidence over column-level patterns.

The consumer's adapter may use the CISM's `typeDistribution` and `occurrences` fields to apply its own consensus logic without re-scanning the raw data.

### 20.4 Cross-Service Alignment Notes

When integrating BIBSS with a consuming service, the following alignment points should be verified:

- **Boolean representation:** BIBSS v1.3 uses case-insensitive matching (`/^(true|false)$/i`). Consumers with their own boolean detection should align or defer to BIBSS's classification.
- **Integer leading zeros:** BIBSS preserves leading-zero values as strings. Consumers whose integer regex does not reject leading zeros should adopt BIBSS's pattern (`/^-?(?:0|[1-9][0-9]*)$/`).
- **Scientific notation:** BIBSS v1.3 does not narrow scientific notation. Consumers that need scientific notation support should pre-normalize input before passing to BIBSS.
- **Null representation:** BIBSS distinguishes between "property absent" (key missing from record) and "property present with null value." Consumers should verify they handle both cases.

---

## 21. Deliverable Definition

BIBSS v1.3 is complete when:

1. The `infer()` function accepts CSV and JSON input and produces a CISM.
2. The CISM conforms to the schema defined in Section 9.
3. The JSON Schema adapter produces Draft 2020-12 compliant output.
4. The adapter registry supports registration and invocation of custom adapters.
5. All diagnostic codes in Section 12.1 are implemented (including `BIBSS-009`).
6. All required test cases in Section 17.2 pass — including boolean case-insensitivity, scientific notation rejection, `typeDistribution` for both CSV and JSON inputs, and `typeDistribution` within arrays.
7. The determinism contract (Section 2.1) is verified by test.
8. The property-merge invariant (Section 17.3, item 4) holds for all test inputs.
9. The lattice-widening invariant (Section 17.3, item 5) holds for all test inputs.
10. The union-bound invariant (Section 17.3, item 6) holds for all test inputs.
11. The distribution completeness invariant (Section 17.3, item 7) holds for all test inputs.
12. CSV type narrowing follows Section 7.1.3 exactly, with no reliance on Papa Parse `dynamicTyping`.
13. Node IDs conform to RFC 6901 and pass collision tests.
14. The bundled artifact makes zero network requests at runtime.
15. Performance targets in Section 15.3 are met on a modern browser (Chrome/Firefox/Safari current release).

---

## 22. Known Limitations (v1.3)

### 22.1 JavaScript Integer Precision

JavaScript's `Number` type is an IEEE 754 double-precision float. Integers above `Number.MAX_SAFE_INTEGER` (9,007,199,254,740,991, or 2^53 − 1) lose precision silently during `JSON.parse`. BIBSS cannot detect or correct this loss after parsing; it can only perform a heuristic pre-scan of the raw input string to warn when large integer literals are present (diagnostic `BIBSS-009`).

**Impact:** Fields containing snowflake IDs (Twitter/X, Discord), certain database auto-increment keys, and high-precision financial identifiers may be represented with incorrect values in the CISM.

**Future mitigation:** A future version may offer an optional `BigInt`-aware JSON parser (e.g., `json-bigint`) as an alternative input path. This would require extending the primitive type enumeration to include `biginteger` and updating the widening lattice accordingly. This is deferred.

### 22.2 Non-UTF-8 Encoding

BIBSS assumes UTF-8 input. Files encoded in UTF-16, ISO-8859-1, Shift-JIS, or other encodings will produce unpredictable results. No detection or transcoding is performed. Callers are responsible for ensuring UTF-8 input.

### 22.3 CSV Without Headers

BIBSS requires a header row for CSV input. Headerless CSV files will have their first data row consumed as headers, producing incorrect property names and losing one record. This is a documented limitation, not a graceful failure.

### 22.4 Deeply Recursive JSON

JavaScript engines impose a call stack limit (typically 10,000–25,000 frames depending on the runtime). JSON structures nested beyond this depth will cause a stack overflow during inference. BIBSS does not implement tail-call optimization or iterative traversal in v1.3. For practical purposes, structures nested beyond depth 100 should be considered unsupported.

### 22.5 Scientific Notation in CSV

BIBSS v1.3 does not narrow scientific notation strings (e.g., `"1e5"`, `"2.5E+3"`) to numeric types. These remain strings. Callers that need scientific notation parsed should convert these values to decimal notation before passing input to BIBSS. This is a deliberate design choice to avoid ambiguity with spreadsheet cell references in exported CSV data.

---

## 23. Appendix A — Type Widening Lattice Reference

Complete resolution table for all primitive type pairs:

| Observed A | Observed B | Resolved Type | Nullable |
|---|---|---|---|
| null | null | null | true |
| null | boolean | boolean | true |
| null | integer | integer | true |
| null | number | number | true |
| null | string | string | true |
| boolean | boolean | boolean | false |
| boolean | integer | integer | false |
| boolean | number | number | false |
| boolean | string | string | false |
| integer | integer | integer | false |
| integer | number | number | false |
| integer | string | string | false |
| number | number | number | false |
| number | string | string | false |
| string | string | string | false |

The table is symmetric: `resolve(A, B) === resolve(B, A)`.

For three or more observed types, resolution is left-folded: `resolve(resolve(A, B), C)`. The lattice is associative and commutative, so fold order does not affect the result.

**This lattice applies identically in all contexts:** property-level inference across records, and element-level inference within arrays. There is one lattice. It does not change behavior based on where the type conflict is observed.

---

## 24. Appendix B — CISM Serialization Example

Input JSON:

```json
[
  { "id": 1, "name": "Alice", "active": true },
  { "id": 2, "name": "Bob", "active": false, "role": "admin" },
  { "id": 3, "name": null, "role": "user" }
]
```

Serialized CISM:

```json
{
  "version": "1.3",
  "generatedAt": "2026-02-28T12:00:00.000Z",
  "config": {
    "requiredThreshold": 1.0,
    "emptyStringAsNull": true,
    "sampleSize": 2000,
    "maxSizeWarning": 10485760
  },
  "root": {
    "id": "#",
    "kind": "array",
    "name": "root",
    "occurrences": 3,
    "itemType": {
      "id": "#/[]",
      "kind": "object",
      "name": "item",
      "occurrences": 3,
      "properties": [
        {
          "name": "id",
          "required": true,
          "occurrences": 3,
          "totalPopulation": 3,
          "target": {
            "id": "#/[]/id",
            "kind": "primitive",
            "primitiveType": "integer",
            "nullable": false,
            "occurrences": 3,
            "typeDistribution": { "integer": 3 }
          }
        },
        {
          "name": "name",
          "required": true,
          "occurrences": 3,
          "totalPopulation": 3,
          "target": {
            "id": "#/[]/name",
            "kind": "primitive",
            "primitiveType": "string",
            "nullable": true,
            "occurrences": 3,
            "typeDistribution": { "null": 1, "string": 2 }
          }
        },
        {
          "name": "active",
          "required": false,
          "occurrences": 2,
          "totalPopulation": 3,
          "target": {
            "id": "#/[]/active",
            "kind": "primitive",
            "primitiveType": "boolean",
            "nullable": false,
            "occurrences": 2,
            "typeDistribution": { "boolean": 2 }
          }
        },
        {
          "name": "role",
          "required": false,
          "occurrences": 2,
          "totalPopulation": 3,
          "target": {
            "id": "#/[]/role",
            "kind": "primitive",
            "primitiveType": "string",
            "nullable": false,
            "occurrences": 2,
            "typeDistribution": { "string": 2 }
          }
        }
      ]
    }
  }
}
```

---

## 25. Appendix C — CSV Type Narrowing Examples

| Raw CSV Value | Rule Matched | Result Type | Result Value |
|---|---|---|---|
| `""` | Null (emptyStringAsNull) | null | `null` |
| `"true"` | Boolean (case-insensitive) | boolean | `true` |
| `"True"` | Boolean (case-insensitive) | boolean | `true` |
| `"TRUE"` | Boolean (case-insensitive) | boolean | `true` |
| `"false"` | Boolean (case-insensitive) | boolean | `false` |
| `"False"` | Boolean (case-insensitive) | boolean | `false` |
| `"FALSE"` | Boolean (case-insensitive) | boolean | `false` |
| `"yes"` | String (no match) | string | `"yes"` |
| `"no"` | String (no match) | string | `"no"` |
| `"1"` | Integer | integer | `1` |
| `"0"` | Integer | integer | `0` |
| `"42"` | Integer | integer | `42` |
| `"-7"` | Integer | integer | `-7` |
| `"00123"` | String (leading zero) | string | `"00123"` |
| `"007"` | String (leading zero) | string | `"007"` |
| `"3.14"` | Number | number | `3.14` |
| `"-0.5"` | Number | number | `-0.5` |
| `"1e5"` | String (no scientific notation) | string | `"1e5"` |
| `"1E5"` | String (no scientific notation) | string | `"1E5"` |
| `"2.5E+3"` | String (no scientific notation) | string | `"2.5E+3"` |
| `"-1e-2"` | String (no scientific notation) | string | `"-1e-2"` |
| `"NaN"` | String (no match) | string | `"NaN"` |
| `"Infinity"` | String (no match) | string | `"Infinity"` |
| `"9007199254740993"` | String (exceeds MAX_SAFE_INTEGER) | string | `"9007199254740993"` |
| `"hello"` | String (no match) | string | `"hello"` |
| `" 42 "` | Integer (after trim) | integer | `42` |

---

## 26. Appendix D — Array Inference Worked Examples

This appendix demonstrates the array inference decision tree (Section 8.5.2) with concrete inputs, showing the three-tier classification in action.

### D.1 — Homogeneous Primitives (Rule 2, all same primitive kind)

**Input:** `[1, 2, 3, 4]`

| Element | Composite Kind | Primitive Kind |
|---|---|---|
| `1` | primitive | integer |
| `2` | primitive | integer |
| `3` | primitive | integer |
| `4` | primitive | integer |

All composite kinds: `primitive`. → Rule 2 applies.
All primitive kinds: `integer`. → Lattice: `integer`.
`typeDistribution: { "integer": 4 }`
**Result:** `{ kind: "primitive", primitiveType: "integer", nullable: false }`

---

### D.2 — Mixed Primitives, Widened (Rule 2, mixed primitive kinds)

**Input:** `[true, 1, 2]`

| Element | Composite Kind | Primitive Kind |
|---|---|---|
| `true` | primitive | boolean |
| `1` | primitive | integer |
| `2` | primitive | integer |

All composite kinds: `primitive`. → Rule 2 applies.
Primitive kinds: `boolean, integer, integer`. → Lattice: `boolean + integer → integer`.
`typeDistribution: { "boolean": 1, "integer": 2 }`
**Result:** `{ kind: "primitive", primitiveType: "integer", nullable: false }`

**This is NOT a union.** The lattice governs all primitive mixing.

---

### D.3 — Mixed Primitives with Null (Rule 2)

**Input:** `[true, 1, null, "hello"]`

| Element | Composite Kind | Primitive Kind |
|---|---|---|
| `true` | primitive | boolean |
| `1` | primitive | integer |
| `null` | null | — |
| `"hello"` | primitive | string |

Non-null composite kinds: all `primitive`. → Rule 2 applies.
Primitive kinds: `boolean, integer, string`. → Lattice: `boolean + integer → integer`, then `integer + string → string`.
Null present → `nullable: true`.
`typeDistribution: { "null": 1, "boolean": 1, "integer": 1, "string": 1 }`
**Result:** `{ kind: "primitive", primitiveType: "string", nullable: true }`

---

### D.4 — Homogeneous Objects with Optional Properties (Rule 2, property-merge)

**Input:**
```json
[
  { "a": 1, "b": "x" },
  { "a": 2, "c": true },
  { "a": 3 }
]
```

All composite kinds: `object`. → Rule 2 applies. → Property-merge algorithm.

| Property | Type | Required | Occurrences | typeDistribution |
|---|---|---|---|---|
| `a` | integer | true | 3/3 | `{ "integer": 3 }` |
| `b` | string | false | 1/3 | `{ "string": 1 }` |
| `c` | boolean | false | 1/3 | `{ "boolean": 1 }` |

**Result:** Single object node. No union.

---

### D.5 — Cross-Kind Union: Primitive + Object (Rule 3)

**Input:** `[1, 2, {"name": "Alice"}]`

| Element | Composite Kind |
|---|---|
| `1` | primitive |
| `2` | primitive |
| `{"name": "Alice"}` | object |

Non-null composite kinds: `primitive` and `object`. → Rule 3 applies. → Union.

- Primitive group `[1, 2]`: lattice → `integer`. `typeDistribution: { "integer": 2 }`.
- Object group `[{"name": "Alice"}]`: merge → `{ properties: [name: string] }`.

**Result:** `{ kind: "union", members: [integer_node, object_node], nullable: false }`

---

### D.6 — Cross-Kind Union with Null (Rule 3)

**Input:** `["hello", [1, 2, 3], null]`

| Element | Composite Kind |
|---|---|
| `"hello"` | primitive |
| `[1, 2, 3]` | array |
| `null` | null |

Non-null composite kinds: `primitive` and `array`. → Rule 3 applies. → Union.

- Primitive group `["hello"]`: lattice → `string`. `typeDistribution: { "string": 1 }`.
- Array group `[[1, 2, 3]]`: recurse → array of `integer`.

Null present → `nullable: true`.
**Result:** `{ kind: "union", members: [string_node, array_node], nullable: true }`

---

### D.7 — Maximum Union: All Three Composite Kinds (Rule 3)

**Input:** `[42, {"x": 1}, [1, 2]]`

| Element | Composite Kind |
|---|---|
| `42` | primitive |
| `{"x": 1}` | object |
| `[1, 2]` | array |

Non-null composite kinds: `primitive`, `object`, `array`. → Rule 3. → Union with 3 members.

- Primitive group: `integer`. `typeDistribution: { "integer": 1 }`.
- Object group: `{ properties: [x: integer] }`.
- Array group: array of `integer`.

**Result:** `{ kind: "union", members: [integer_node, object_node, array_node], nullable: false }`

This is the **maximum possible union size**: 3 members. The three-tier model structurally guarantees this bound.

---

### D.8 — Empty Array (Rule 4)

**Input:** `[]`

Zero elements. → Rule 4.
**Result:** `itemType: null`. Diagnostic `BIBSS-007` emitted.

---

### D.9 — All Null (Rule 1)

**Input:** `[null, null, null]`

All elements are null. → Rule 1.
`typeDistribution: { "null": 3 }`
**Result:** `{ kind: "primitive", primitiveType: "null", nullable: true }`

---

*End of specification.*
