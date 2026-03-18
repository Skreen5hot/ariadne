# Semantic Normalization Proxy (SNP)

## Technical Specification — Version 1.3

|Field                        |Value                     |
|-----------------------------|--------------------------|
|**Status**                   |Final                     |
|**Author**                   |Aaron Damiano                    |
|**Date**                     |2026-02-28                |
|**FNSR Component**           |Format Cleaning Layer     |
|**Edge-Canonical Compliance**|Full                      |
|**Supersedes**               |SNP v1.2                  |

-----

## Changelog from v1.2

|ID   |Section(s)      |Severity    |Change                                                                                                                                                                           |
|-----|----------------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|C-016|All             |**Critical**|Complete architectural revision. SNP now outputs `{ cleaned: string, manifest: Manifest, format: "csv" \| "json" }` instead of JSON-LD `@graph`. Output plugs directly into BIBSS `infer()` without deserialization.|
|C-017|§5              |**Critical**|Removed all threshold-gated semantic coercion rules: Boolean Coercion (§5.4), Numeric Sanitization (§5.5), Temporal Normalization (§5.6), Delimited Array Expansion (§5.7), Categorical Folding (§5.8). SNP now performs format cleaning only. Semantic coercion is the responsibility of downstream consumers (ECVE adapter).|
|C-018|§5              |**Critical**|Removed `confidenceThreshold` and all column-level frequency analysis. All cleaning rules are unconditional — they fire on every matching value. There are no column-level decisions, no profiling phase, and no sampling.|
|C-019|§5.3            |**High**    |Currency/formatting stripping now implements ECVE v4.0 Appendix A.6 normative patterns. Patterns are defined in ECVE; execution delegated to SNP.|
|C-020|§5.4            |**High**    |Locale-aware date normalization now implements ECVE v4.0 Appendix A.7 normative patterns. Requires explicit locale hint in configuration. No locale = no date conversion.|
|C-021|§5.5            |**High**    |Null coalescence reduced to empty-string-to-null only, matching BIBSS v1.3 §7.1.2. Semantic null vocabulary (`"N/A"`, `"none"`, `"-"`) removed — these are domain-specific and belong in the ECVE semantic adapter.|
|C-022|§6              |**High**    |Configuration changed from JSON-LD document to plain TypeScript interface, consistent with BIBSS `InferConfig` pattern.|
|C-023|§10 (removed)   |**High**    |Removed BIBSS Interface Contract section. SNP documents what it produces. Consumers decide what to do with it.|
|C-024|Appendix B (rem)|**Medium**  |Removed ontological alignment appendix. BFO/CCO grounding deferred until FNSR-wide ontology integration pattern is established.|
|C-025|§3              |**Medium**  |Fixed "mutates data arrays" → "produces transformed data arrays." Contract is pure function.|
|C-026|§8              |**Medium**  |Added structured diagnostic codes `SNP-001` through `SNP-008`, consistent with BIBSS diagnostic pattern.|
|C-027|§9              |**Medium**  |Added performance targets benchmarked against BIBSS §15.3.|
|C-028|§2.5            |**Medium**  |Added hash timing documentation. Caller computes raw input hash before invoking SNP.|
|C-029|§6.4            |**Medium**  |Clarified JSON format preservation: structural equivalence guaranteed, byte-level formatting (indentation, whitespace between keys) not preserved due to AST re-serialization.|
|C-030|All             |**Medium**  |Corrected all ECVE version references from v4.1 to v4.0. The normative patterns (Appendix A.6/A.7, Step 0) already exist in ECVE v4.0. No pattern content changed — version attribution only. Resolves F-NEW-5.|
|C-030|§6.2, §4.4, §4.5|**Medium**  |Manifest `path` field specified as column header (CSV) or RFC 6901 JSON Pointer (JSON). Rule descriptions updated to use "column (CSV) or property path (JSON)" consistently.|
|C-031|§4.6            |**Low**     |BigInt protection regex updated from `/^\d{16,}$/` to `/^-?\d{16,}$/` to cover negative large integers.|
|C-032|§14.5           |**Low**     |Added known limitation: datetime strings (date + time) are not converted by §4.7. Only date-only patterns from ECVE A.7 are supported.|
|C-033|§14.6           |**Low**     |Added known limitation: thousands-separator regex may strip commas in mixed alphanumeric strings. Documents ECVE A.6 edge case.|

-----

## 1. Purpose

The Semantic Normalization Proxy (SNP) is a deterministic, fully client-side format cleaning engine. It ingests raw, human-authored data formats (CSV, JSON) and strips formatting artifacts — currency symbols, thousands separators, percentage signs, BOM characters, trailing empty columns, and locale-specific date notation — producing a cleaned string in the same format as the input.

SNP operates strictly upstream of the Brain-in-the-Box Schema Service (BIBSS). It satisfies the clean-input assumption documented in BIBSS v1.3 §2.5. SNP does not perform type inference, semantic coercion, or structural analysis. It transforms formatting noise into clean strings that BIBSS can classify.

The separation of concerns is:

- **SNP** cleans formatting (this specification).
- **BIBSS** infers structure (BIBSS v1.3).
- **Consumer semantic adapters** interpret meaning (consumer-owned, e.g., ECVE adapter).

-----

## 2. Governing Principles

### 2.1 Edge-Canonical Execution

SNP is a pure function. It executes entirely within a standards-compliant browser or a local Node.js environment (`node index.js`). It requires zero background workers, databases, or service registries.

### 2.2 Determinism Contract

SNP contains no probabilistic or randomized execution logic. Given identical input bytes and an identical configuration, it **must** produce byte-identical output across all runtimes. There are no column-level heuristics, no frequency analysis, and no threshold-gated decisions. Every cleaning rule fires unconditionally on every matching value.

### 2.3 Format Preservation

SNP outputs the same format it receives. CSV in, cleaned CSV out. JSON in, cleaned JSON out. The output is a string that BIBSS can consume directly via `infer(input: string)`. SNP does not restructure data, mint IRIs, create graph nodes, or wrap output in JSON-LD framing.

The manifest (mutation log) is a separate sidecar document. It records what SNP changed and why. It does not wrap or contain the cleaned data.

### 2.4 Offline-First and Degraded Execution

SNP operates with zero network dependencies. It cannot query external APIs for currency localization, schema resolution, or entity reconciliation. If a value cannot be deterministically cleaned using local logic (e.g., an ambiguous date with no locale hint), SNP leaves the value unchanged and records a diagnostic.

### 2.5 Hash Timing

SNP does not compute content hashes. Hash computation is a provenance concern owned by the caller. The caller (typically ECVE) **must** compute `viz:rawInputHash` on the exact raw bytes **before** invoking SNP. SNP receives a working copy, not the raw buffer. This aligns with ECVE v4.0 Step 0: "the raw byte buffer's SHA-256 hash is computed on the exact bytes received — before BOM stripping, before currency normalization, before any transformation."

-----

## 3. Architecture

SNP is a single function with no internal state.

```
normalize(input, config?) → { cleaned, manifest, format, diagnostics }
```

There are no layers, no pluggable components, no adapter registries. The function accepts input, applies cleaning rules in order, and returns output. Internal implementation may organize code into modules, but the architectural contract is one function call.

**Separation from prior versions:** SNP v1.0–v1.2 attempted to be a Computation/State/Orchestration/Integration architecture with pluggable parsers, column profiling, threshold evaluation, and mutation phases. This was overengineered for a formatting pass. v1.3 is a function.

-----

## 4. Cleaning Rules

SNP applies the following rules in order. All rules are **unconditional** — they fire on every value that matches, with no column-level analysis, no frequency thresholds, and no profiling phase. The engine makes a single linear pass through the data.

### 4.0 Rule Summary

|§  |Rule                           |Scope         |Input → Output       |Destructive|
|---|-------------------------------|--------------|----------------------|-----------|
|4.1|BOM Stripping                  |Document-level|bytes → bytes         |Yes        |
|4.2|Trailing Column Removal        |Document-level|columns → columns     |Yes        |
|4.3|Whitespace Hygiene             |Per-value     |string → string       |Yes        |
|4.4|Empty-to-Null Coalescence      |Per-value     |string → null literal |Yes        |
|4.5|Currency/Formatting Stripping  |Per-value     |string → string       |Yes        |
|4.6|BigInt String Protection       |Per-value     |string → string (flag)|No         |
|4.7|Locale-Aware Date Normalization|Per-value     |string → string       |Conditional|

**Rule ordering rationale:** Document-level rules (4.1, 4.2) run first because they affect the parse boundary. Whitespace hygiene (4.3) runs before all value-level rules because downstream rules operate on trimmed values. Empty-to-null (4.4) runs after trimming so that whitespace-only values become null. Currency stripping (4.5) runs before BigInt protection (4.6) so that `"$123456789012345678"` has its `$` stripped before the digit-length check. Date normalization (4.7) runs last because it is optional and conditional on locale configuration.

### 4.1 BOM Stripping

- **Scope:** Document-level, runs once on raw input.
- **Rule:** If the input string begins with UTF-8 Byte Order Mark (`\uFEFF` / `\xEF\xBB\xBF`), remove it.
- **Diagnostic:** `SNP-001` (info) when BOM is detected and stripped.
- **Implements:** ECVE v4.0 Step 0.1.

### 4.2 Trailing Column Removal (CSV Only)

- **Scope:** Document-level, CSV input only. Skipped for JSON.
- **Rule:** After parsing CSV to rows, identify any column where 100% of data cells (excluding the header) are empty strings or whitespace-only. Remove those columns entirely — both the header entry and the corresponding cell in every data row.
- **Diagnostic:** `SNP-002` (info) per column removed, including the original column header name and position.
- **Implements:** ECVE v4.0 Step 0.2.

**Constraint:** "100% empty" means every data row. A single non-empty value in any row preserves the column. This check scans all rows, not a sample.

### 4.3 Whitespace Hygiene

- **Scope:** Per-value, all string values.
- **Rule:** Applied to every string value after CSV parsing or JSON traversal:
  1. Strip leading and trailing whitespace (equivalent to `String.prototype.trim()`).
  2. Collapse runs of two or more internal whitespace characters (spaces, tabs) to a single space.
  3. Remove non-printable Unicode control characters: zero-width spaces (`\u200B`), zero-width non-joiners (`\u200C`), zero-width joiners (`\u200D`), byte order marks embedded mid-string (`\uFEFF`), and ASCII control characters `\x00`–`\x1F` (except `\x09` tab and `\x0A` newline, which are collapsed in step 2 for mid-string occurrences and stripped in step 1 for leading/trailing).

**No manifest entry** is emitted for whitespace hygiene. It is applied universally and recording it per-value would produce noise without diagnostic value.

### 4.4 Empty-to-Null Coalescence

- **Scope:** Per-value, all string values.
- **Rule:** After whitespace hygiene, any value that is the empty string `""` is replaced with the JSON literal `null`.
- **Alignment:** Matches BIBSS v1.3 §7.1.2 post-parse transform (empty string → null when `emptyStringAsNull: true`). Performing this in SNP means BIBSS receives pre-coalesced values, which is harmless — BIBSS's empty-to-null pass is idempotent over already-null values.

**What this rule does NOT do:** It does not coalesce `"N/A"`, `"n/a"`, `"NA"`, `"-"`, `"none"`, `"null"`, or any other string to null. These are semantic interpretations. Whether `"-"` means null, zero, or "not applicable" depends on the domain. Domain-specific null vocabularies belong in the consuming application's semantic adapter, not in a general-purpose format cleaner.

**Manifest entry:** One entry per column (CSV) or property path (JSON) recording the count of values coalesced to null. No per-value entries.

### 4.5 Currency/Formatting Stripping

- **Scope:** Per-value, all string values (after whitespace hygiene and null coalescence).
- **Rule:** Applied in order to each non-null string value:

**Step 1 — Leading currency symbols.** Strip leading currency symbols and optional trailing whitespace:

```
/^[$€£¥₹₩₽₺₱฿]\s*/
```

**Step 2 — Thousands separators.** Strip commas that function as thousands separators:

```
/,(?=\d{3}(?:[,.]|\b))/g
```

This matches commas followed by exactly three digits and then another comma, a period, or a word boundary. It correctly handles `"1,234,567.89"` → `"1234567.89"` and does not match commas in non-numeric contexts.

**Step 3 — Trailing percentage sign.** Strip a trailing `%`:

```
/%$/
```

- **Implements:** ECVE v4.0 Appendix A.6, verbatim. The patterns are defined normatively in ECVE; SNP executes them. When ECVE updates Appendix A.6, SNP adopts the new patterns.
- **Manifest entry:** One entry per value modified, recording the original value, the stripped artifacts (currency symbol, separator count, percentage), and the cleaned value.
- **Diagnostic:** `SNP-003` (info) per column (CSV) or property path (JSON) where at least one value was modified, including the count of affected values.

**Idempotency:** All three steps are idempotent. Running them on already-cleaned values produces no change.

**What this rule does NOT do:** It does not resolve radix ambiguity (is `","` a decimal separator or a thousands separator in European formatting?). It does not convert the cleaned string to a number. The value `"$1,234.56"` becomes the string `"1234.56"`, not the number `1234.56`. BIBSS's Number narrowing rule (§7.1.3) handles the string-to-number conversion.

### 4.6 BigInt String Protection

- **Scope:** Per-value, all string values (after currency stripping).
- **Rule:** Any value consisting entirely of an optional leading minus sign followed by digits, matching the pattern `/^-?\d{16,}$/` (16 or more consecutive digits, optionally negative), is flagged as BigInt-protected. The value is **not modified** — it remains a string. The flag is recorded in the manifest so downstream consumers know this value was intentionally not converted to a number.
- **Rationale:** JavaScript's `Number.MAX_SAFE_INTEGER` is `2^53 - 1` (9,007,199,254,740,991), which is 16 digits. Any integer of 16+ digits — positive or negative — risks precision loss if parsed via `Number()`. Twitter/X snowflake IDs, Discord IDs, and some database primary keys fall in this range. BIBSS v1.3 §7.1.3 Integer rule already requires values to be ≤ `MAX_SAFE_INTEGER`, so flagging here is defensive documentation, not a behavioral change.
- **Manifest entry:** One entry per flagged value, recording the property path and value length.
- **Diagnostic:** `SNP-004` (info) per column (CSV) or property path (JSON) containing at least one BigInt-protected value.

**What this rule does NOT do:** It does not flag values with non-digit characters (other than a leading minus). The string `"12345678901234567890.5"` is not flagged (it contains a period). The string `"+1234567890123456"` is not flagged (it contains a plus sign — only minus is recognized). Only pure digit sequences (optionally negative) of 16+ characters are flagged.

### 4.7 Locale-Aware Date Normalization (Optional)

- **Scope:** Per-value, string values only. **Conditional** — runs only when `locale` is set in configuration.
- **Rule:** If a locale hint is provided in the configuration, SNP applies the corresponding date conversion pattern from ECVE v4.0 Appendix A.7:

|Locale  |Pattern   |Regex                                  |Conversion               |
|--------|----------|---------------------------------------|-------------------------|
|`en-US` |MM/DD/YYYY|`/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/`   |`$3-$1-$2` (zero-padded) |
|`en-GB` |DD/MM/YYYY|`/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/`   |`$3-$2-$1` (zero-padded) |
|`de-DE` |DD.MM.YYYY|`/^(\d{1,2})\.(\d{1,2})\.(\d{4})$/`   |`$3-$2-$1` (zero-padded) |
|`ja-JP` |YYYY/MM/DD|`/^(\d{4})\/(\d{1,2})\/(\d{1,2})$/`   |`$1-$2-$3` (zero-padded) |

The output format is always ISO 8601: `YYYY-MM-DD`. Months and days are zero-padded to two digits.

- **Implements:** ECVE v4.0 Appendix A.7, verbatim. The patterns are defined normatively in ECVE; SNP executes them. ECVE v4.0 Step 0.4 becomes "delegate to SNP" rather than implementing internally.
- **Ambiguity rule:** If no locale is configured, this rule is skipped entirely. Two-digit years are rejected (no conversion). If the `en-US` and `en-GB` patterns produce the same regex match (they do — both are `\d{1,2}/\d{1,2}/\d{4}`), the locale determines interpretation. Without a locale, the value is left as-is.
- **Validation:** After conversion, the resulting date is validated: month must be 1–12, day must be 1–31 (with month-appropriate bounds and leap year handling for February). Invalid dates (e.g., `13/45/2026` matching the regex but producing month=13) are left unconverted, and diagnostic `SNP-005` is emitted.
- **Manifest entry:** One entry per converted value, recording the original string, the locale used, and the ISO 8601 result.
- **Diagnostic:** `SNP-005` (warning) per value that matched the date regex but failed validation.
- **Diagnostic:** `SNP-006` (info) per column (CSV) or property path (JSON) where at least one date was successfully converted.

**What this rule does NOT do:** It does not detect date formats. It does not guess locales. It does not parse natural language dates ("yesterday", "last Tuesday"). It does not handle time components. It applies a known pattern for a known locale, or it does nothing.

-----

## 5. Configuration

Configuration is passed to the `normalize()` function as a plain TypeScript object. If omitted, defaults are applied.

```typescript
interface SnpConfig {
  /**
   * Locale hint for date normalization (§4.7).
   * If null, date normalization is skipped entirely.
   * Supported values: "en-US", "en-GB", "de-DE", "ja-JP".
   * Default: null.
   */
  locale: string | null

  /**
   * Override format detection.
   * If null, SNP auto-detects: first non-whitespace char is { or [ → JSON, else CSV.
   * Default: null (auto-detect).
   */
  format: "csv" | "json" | null
}
```

**Default configuration:**

```typescript
const DEFAULT_CONFIG: SnpConfig = {
  locale: null,
  format: null
}
```

**Design note:** Previous SNP versions included `confidenceThreshold`, `nullSet`, `booleanPairs`, `radixConvention`, `delimiterPrecedence`, `temporal.assumeFormat`, and `temporal.referenceDate`. All of these controlled semantic coercion logic that has been removed from SNP. The configuration surface is intentionally minimal because SNP's cleaning rules are unconditional — they don't need tuning parameters.

-----

## 6. Output Contract

### 6.1 Return Type

```typescript
interface SnpResult {
  /** Cleaned data in the same format as input. Plugs directly into BIBSS.infer(). */
  cleaned: string

  /** Mutation log documenting every transformation applied. */
  manifest: ManifestEntry[]

  /** Detected or configured input format. */
  format: "csv" | "json"

  /** Structured diagnostic messages. */
  diagnostics: Diagnostic[]
}
```

### 6.2 Manifest Entries

```typescript
interface ManifestEntry {
  /** Cleaning rule that produced this entry. */
  rule: string

  /**
   * Location affected.
   * - For CSV input: column header name (e.g., "Price (USD)").
   * - For JSON input: RFC 6901 JSON Pointer path (e.g., "/users/0/price"),
   *   consistent with BIBSS v1.3 §9.2 node identity.
   * - For document-level rules: "*".
   */
  path: string

  /** What changed. Structure depends on the rule. */
  detail: ManifestDetail
}

type ManifestDetail =
  | { type: "bom_stripped" }
  | { type: "column_removed"; header: string; position: number }
  | { type: "null_coalescence"; count: number }
  | { type: "currency_stripped"; originalValue: string; cleanedValue: string; artifacts: string[] }
  | { type: "bigint_flagged"; valueLength: number }
  | { type: "date_converted"; originalValue: string; locale: string; isoValue: string }
```

### 6.3 Diagnostics

```typescript
interface Diagnostic {
  level: "info" | "warning" | "error"
  code: string
  message: string
  context?: Record<string, unknown>
}
```

### 6.4 Format Preservation Guarantee

The `cleaned` string is:

- **For CSV input:** A valid CSV string with the same delimiter and quoting conventions as the input, minus trailing columns (§4.2) and with cell values cleaned per §4.3–§4.7. The header row is preserved. Row count is preserved. Column order is preserved (minus removed trailing columns).
- **For JSON input:** A valid JSON string with values cleaned per §4.3–§4.7. **Structural equivalence** is guaranteed — no keys are added, removed, or reordered. Array lengths are preserved. Nesting depth is preserved. However, **byte-level formatting is not preserved**: because SNP must parse the JSON (via `JSON.parse()`), traverse the AST to apply per-value cleaning, and re-serialize (via `JSON.stringify()`), original indentation, line breaks, and whitespace between keys are replaced by the serializer's default compact output. The data structure is identical; the cosmetic formatting of the JSON container is not.

BIBSS receives `cleaned` as a `string` argument to `infer()`. No intermediate deserialization, no format conversion, no adapter step.

-----

## 7. Public API

```typescript
interface SNP {
  /**
   * Clean formatting artifacts from raw data.
   *
   * Input: Raw CSV or JSON string.
   * Output: Cleaned string in the same format, plus manifest and diagnostics.
   *
   * Binary-to-string decoding (e.g., FileReader, fs.readFileSync) is the
   * caller's responsibility. SNP processes strings, not bytes.
   */
  normalize(input: string, config?: Partial<SnpConfig>): SnpResult
}
```

**Input type:** `string` only. Previous versions accepted `ArrayBuffer` and `object[]`. Both are removed:

- `ArrayBuffer`: No cleaning rule addresses binary data. The caller decodes to string via `TextDecoder` before invoking SNP.
- `object[]`: SNP operates on serialized data (CSV/JSON strings), not pre-parsed objects. Accepting pre-parsed objects would bypass document-level rules (BOM stripping, trailing column removal) and require SNP to re-serialize output — defeating the format preservation guarantee.

-----

## 8. Diagnostic Codes

|Code     |Level  |Condition                                                     |Context Fields                       |
|---------|-------|--------------------------------------------------------------|-------------------------------------|
|`SNP-001`|info   |BOM detected and stripped                                     |—                                    |
|`SNP-002`|info   |Trailing column removed                                       |`header`, `position`                 |
|`SNP-003`|info   |Currency/formatting stripping applied to column (CSV) or property path (JSON)|`path`, `affectedCount`            |
|`SNP-004`|info   |BigInt-protected values detected in column (CSV) or property path (JSON)     |`path`, `flaggedCount`             |
|`SNP-005`|warning|Date regex matched but validation failed (invalid date)       |`path`, `value`, `locale`          |
|`SNP-006`|info   |Date normalization applied to column (CSV) or property path (JSON)|`path`, `convertedCount`, `locale` |
|`SNP-007`|error  |CSV parse failure (malformed quoting, encoding error)         |`row`, `message`                     |
|`SNP-008`|error  |JSON parse failure (syntax error)                             |`position`, `message`                |

**Error handling philosophy:** SNP does not throw exceptions. Parse failures produce diagnostics with `level: "error"` and a `cleaned` value of `""` (empty string). All other diagnostics are informational — cleaning proceeds regardless.

-----

## 9. Performance

### 9.1 Complexity

```
O(R × C)
```

Where `R` is the number of rows and `C` is the number of columns (CSV) or the total number of leaf values (JSON). SNP makes one linear pass through the data. There is no column profiling, no frequency accumulation, no multi-pass analysis.

### 9.2 No Sampling

SNP does not sample. Every row is cleaned. This is a deliberate difference from BIBSS (which samples 2,000 rows for inference). Cleaning is per-value and unconditional — there is no statistical decision that benefits from sampling. Skipping rows would produce inconsistent output where some values are cleaned and others are not.

### 9.3 Benchmark Targets

|Input                   |Rows   |Columns|Target Time|Notes                                     |
|------------------------|-------|-------|-----------|------------------------------------------|
|Flat CSV, minimal cleaning|2,000|20     |< 10ms     |Whitespace + null coalescence only        |
|Flat CSV, currency columns|2,000|20     |< 20ms     |Currency stripping on ~5 columns          |
|Flat CSV, date columns  |2,000  |20     |< 25ms     |Date normalization on ~3 columns          |
|Flat CSV, full cleaning |2,000  |20     |< 30ms     |All rules active                          |
|Wide CSV                |2,000  |500    |< 200ms    |All rules, many columns                   |
|Large CSV               |100,000|20     |< 500ms    |Full dataset, no sampling                 |
|JSON, nested            |2,000  |50 leaf values|< 30ms|All rules on leaf string values       |

These are targets, not guarantees. Actual performance depends on the runtime. SNP's targets are deliberately faster than BIBSS's (§15.3) because SNP does simpler work — string replacement versus recursive structural inference.

-----

## 10. Integration Pipeline

This section documents how SNP fits into the ECVE/BIBSS pipeline. It does not prescribe BIBSS or ECVE behavior — their specifications are authoritative for their own contracts.

### 10.1 Expected Pipeline Position

```
Raw input bytes
       │
       ▼
┌──────────────────────────────┐
│ Caller computes              │  ← viz:rawInputHash (SHA-256 of raw bytes)
│ raw input hash               │    Before ANY transformation.
│ (ECVE v4.0 Step 0)          │
└──────┬───────────────────────┘
       │
       ▼
  input string (decoded from bytes by caller)
       │
       ▼
┌──────────────────────────────┐
│ SNP.normalize()              │  ← Format cleaning (this specification)
│                              │    BOM, trailing columns, whitespace,
│                              │    empty→null, currency, BigInt, dates
└──────┬───────────────────────┘
       │
       ▼
  SnpResult.cleaned (string, same format as input)
       │
       ▼
┌──────────────────────────────┐
│ BIBSS.infer()                │  ← Structural inference (BIBSS v1.3)
│                              │    Type narrowing, widening lattice,
│                              │    typeDistribution accumulation
└──────┬───────────────────────┘
       │
       ▼
  CISM (with typeDistribution)
       │
       ▼
┌──────────────────────────────┐
│ Consumer Semantic Adapter    │  ← Semantic interpretation (consumer-owned)
│ (e.g., ECVE adapter)        │    Type promotion, consensus thresholds,
│                              │    "Y/N" → boolean, "N/A" → null,
│                              │    date classification, metric matching
└──────────────────────────────┘
       │
       ▼
  Consumer Schema (e.g., viz:DatasetSchema)
```

### 10.2 What SNP Provides to Each Consumer

**To BIBSS:** A cleaned string in CSV or JSON format. BIBSS receives this as the `input` argument to `infer()`. BIBSS does not need to know that SNP ran — the cleaned string is valid CSV/JSON that BIBSS can parse normally. Currency symbols are gone, so BIBSS's Number rule matches `"1234.56"` instead of failing on `"$1,234.56"`. Dates are in ISO 8601 (if locale was configured), so BIBSS sees `"2026-03-04"` as a string that downstream consumers can classify as Temporal.

**To ECVE (via manifest):** The manifest documents every transformation SNP applied. ECVE can fold manifest entries into its provenance chain (`viz:wasNormalized: true` metadata on affected `viz:DataField` entities). The manifest is structured data (TypeScript objects), not JSON-LD. ECVE's adapter serializes it into the provenance graph format if needed. **Provenance hash note:** The hash of `SnpResult.cleaned` will not match `viz:rawInputHash` — by design, SNP modifies the bytes. Downstream systems must use the caller's pre-SNP raw hash for provenance, never hash the cleaned output as a substitute.

### 10.3 What SNP Does NOT Provide

- **Type assertions.** SNP does not tell BIBSS what type a column is. BIBSS infers types from the cleaned values using its own rules.
- **Confidence scores.** SNP has no column-level statistics. Every transformation is unconditional.
- **Schema hints.** Previous versions emitted `snp:inferredType` annotations. These are removed. BIBSS does its own inference; it does not need hints from the formatting pass.
- **Provenance graph.** The manifest is structured data, not a JSON-LD graph. Graph serialization is the consumer's responsibility.

-----

## 11. Deliverable Definition

SNP v1.3 is considered complete when:

1. The `normalize()` function executes entirely within a browser or `node index.js` with zero network dependencies.
2. The output `cleaned` string is valid CSV (for CSV input) or valid JSON (for JSON input) that BIBSS `infer()` accepts without error.
3. All 7 cleaning rules (§4.1 through §4.7) pass deterministic test suites.
4. Format preservation: `normalize()` on already-clean input returns the input unchanged (idempotency).
5. BOM stripping handles UTF-8 BOM correctly and emits `SNP-001`.
6. Trailing column removal identifies and removes 100%-empty columns and emits `SNP-002` per column.
7. Whitespace hygiene handles leading/trailing whitespace, internal runs, and non-printable Unicode.
8. Empty-to-null coalescence converts `""` to `null` after trimming.
9. Currency stripping implements ECVE v4.0 Appendix A.6 exactly: leading currency symbols, thousands separators, trailing percent.
10. BigInt protection flags digit sequences of 16+ characters and emits `SNP-004`.
11. Date normalization implements ECVE v4.0 Appendix A.7 for all four locale patterns, with zero-padding and date validation.
12. Date normalization is skipped entirely when no locale is configured.
13. Parse errors (CSV or JSON) produce `SNP-007`/`SNP-008` diagnostics with `level: "error"` and `cleaned: ""`.
14. All diagnostic codes in §8 are implemented with correct levels and context fields.
15. A developer can clone the repository, run the test suite offline, and inspect outputs without relying on any external infrastructure.
16. Performance targets in §9.3 are met on a modern browser (Chrome/Firefox/Safari current release).

-----

## 12. Testing Contract

### 12.1 Determinism Tests

For every test case, the following must hold:

```
normalize(input, config).cleaned === normalize(input, config).cleaned
```

Output must be byte-identical across invocations on the same runtime and across conformant runtimes.

### 12.2 Required Test Cases

|Category                      |Cases                                                                                                                       |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------|
|BOM stripping                 |Input with BOM → BOM removed, `SNP-001` emitted. Input without BOM → no change, no diagnostic.                             |
|Trailing columns              |CSV with 2 trailing empty columns → columns removed, 2× `SNP-002`. CSV with no trailing empties → no change. One non-empty value preserves column.|
|Whitespace hygiene            |Leading/trailing spaces, tabs, internal double-spaces, zero-width spaces (`\u200B`), mixed control characters.              |
|Empty-to-null                 |`""` → `null`. `" "` → `null` (trimmed then empty). `"N/A"` → `"N/A"` (NOT coalesced). `"-"` → `"-"` (NOT coalesced).     |
|Currency stripping            |`"$1,234.56"` → `"1234.56"`. `"€1.234,56"` → `"€1234,56"` (only thousands-separator commas stripped, not EU decimals — see note). `"45%"` → `"45"`. `"£ 100"` → `"100"`. Already-clean `"1234.56"` → `"1234.56"` (idempotent).|
|BigInt protection             |`"1234567890123456"` (16 digits) → flagged. `"-1234567890123456"` (negative, 16 digits) → flagged. `"123456789012345"` (15 digits) → not flagged. `"12345678901234AB"` → not flagged (non-digit). `"+1234567890123456"` → not flagged (plus sign). `"$1234567890123456"` → currency stripped first, then flagged.|
|Date normalization (en-US)    |`"03/04/2026"` → `"2026-03-04"`. `"3/4/2026"` → `"2026-03-04"` (zero-padded). `"13/04/2026"` → left unchanged (month 13 invalid), `SNP-005`.|
|Date normalization (en-GB)    |`"04/03/2026"` → `"2026-03-04"`. `"4/3/2026"` → `"2026-03-04"`.                                                            |
|Date normalization (de-DE)    |`"04.03.2026"` → `"2026-03-04"`.                                                                                           |
|Date normalization (ja-JP)    |`"2026/03/04"` → `"2026-03-04"`.                                                                                           |
|Date normalization (no locale)|All date-like values left unchanged. No `SNP-005` or `SNP-006` emitted.                                                    |
|Date normalization (2-digit year)|`"03/04/26"` → left unchanged (two-digit years rejected).                                                               |
|Date normalization (datetime)   |`"03/04/2026 14:30:00"` → left unchanged (date-only patterns do not match datetime strings). No diagnostic emitted.       |
|CSV parse error               |Malformed CSV → `cleaned: ""`, `SNP-007` with error level.                                                                  |
|JSON parse error              |Malformed JSON → `cleaned: ""`, `SNP-008` with error level.                                                                 |
|Idempotency                   |`normalize(normalize(input).cleaned)` produces identical `cleaned` to single pass.                                          |
|Format detection              |JSON beginning with `{` or `[` detected as JSON. Everything else as CSV. Override via `config.format`.                      |
|JSON nested values            |Cleaning rules apply to all leaf string values in nested JSON, including arrays of strings and deeply nested objects.        |
|JSON non-string values        |Existing `null`, `true`, `false`, and numeric values in JSON are passed through unchanged.                                  |
|JSON manifest paths           |Manifest entries for JSON input use RFC 6901 JSON Pointer paths (e.g., `"/users/0/price"` not `"price"`).                   |
|Combined rules                |CSV cell `" $1,234.56 "` → trimmed → currency stripped → `"1234.56"`. Manifest records both transformations.                |

### 12.3 Property-Based Invariants

For any valid input `I` and config `C`:

1. `normalize(I, C)` terminates.
2. If `I` is valid CSV, `normalize(I, C).cleaned` is valid CSV with the same number of data rows.
3. If `I` is valid JSON, `normalize(I, C).cleaned` is valid JSON.
4. `normalize(I, C).format` is `"csv"` or `"json"`.
5. `normalize(normalize(I, C).cleaned, C).cleaned === normalize(I, C).cleaned` (idempotency).
6. The manifest contains no entries for values that were not modified.
7. All diagnostics have a `code` matching a defined `SNP-0XX` code.

-----

## 13. Security Considerations

- **No network calls.** The function makes zero HTTP requests at runtime.
- **No data persistence.** Input and output exist only in memory during execution. Nothing is written to `localStorage`, `IndexedDB`, cookies, or the filesystem.
- **No `eval` or dynamic code generation.** All regex patterns are statically defined.
- **No prototype pollution.** Object traversal uses `Object.hasOwn()` or equivalent.
- **CSV injection.** SNP does not execute formulas found in CSV cells. All values are treated as inert strings. SNP does not sanitize output against formula injection — downstream consumers that render values in spreadsheet contexts must implement their own sanitization.
- **Regex denial of service.** All regex patterns in §4 are linear-time (no nested quantifiers, no catastrophic backtracking). The currency thousands-separator regex uses a lookahead, but it matches only fixed-length sequences (`\d{3}`), bounding the lookahead to constant time.

-----

## 14. Known Limitations (v1.3)

### 14.1 European Radix Convention

The thousands-separator stripping regex (§4.5 Step 2) targets commas followed by exactly three digits. In European formatting (`"1.234,56"`), the comma is the decimal separator and the period is the thousands separator. SNP does not strip periods-as-thousands-separators because the regex cannot distinguish `"1.234"` (European thousands) from `"1.234"` (a decimal number). European radix handling is a semantic decision that requires domain context — it belongs in the consuming application, not in SNP.

### 14.2 Date Format Detection

SNP does not detect date formats. It converts dates only when a locale is explicitly configured. A column containing `"03/04/2026"` with no locale hint passes through unchanged as a string. Format detection (deciding whether a column contains dates) is a semantic inference that belongs in the ECVE semantic adapter, using BIBSS's `typeDistribution` to determine that a column's values are strings matching a date pattern.

### 14.3 No JSON Structural Modification

SNP cleans leaf values in JSON but does not modify structure. Empty objects (`{}`), empty arrays (`[]`), and null-valued keys are preserved as-is. Structural decisions (removing empty keys, flattening nested objects) are not format cleaning.

### 14.4 Character Encoding

SNP assumes UTF-8 input. Files in other encodings (UTF-16, ISO-8859-1, Shift-JIS) produce unpredictable results. The caller is responsible for ensuring UTF-8 input, consistent with BIBSS v1.3 §22.2.

### 14.5 Datetime Strings

SNP's date normalization (§4.7) handles date-only values (`"03/04/2026"` → `"2026-03-04"`). Datetime strings that include time components (`"03/04/2026 14:30:00"`) do not match the ECVE A.7 date-only regexes and pass through unchanged. This is by design: SNP implements ECVE A.7 verbatim, and ECVE A.7 defines only date-only patterns. If datetime normalization is needed, ECVE should extend Appendix A.7 with datetime patterns, and SNP will adopt them in a subsequent release.

### 14.6 Thousands-Separator Stripping in Mixed Strings

The thousands-separator regex (§4.5 Step 2, implementing ECVE v4.0 Appendix A.6 Step 2) operates on raw string values without requiring the entire value to be numeric. A mixed alphanumeric string like `"Apples,123,456"` will have its first comma stripped, producing `"Apples123,456"`. This is a consequence of the ECVE A.6 pattern, which is designed for cells that contain numeric values with formatting artifacts. In practice, mixed alphanumeric cells are unlikely to contain comma-separated digit groups that happen to match thousands-separator patterns, but the edge case exists. If this proves problematic in production, the fix belongs in ECVE A.6 (adding a lookbehind or full-value numeric guard), not in SNP — SNP implements what ECVE specifies.

-----

## Appendix A — ECVE Pattern Cross-Reference

This appendix documents the ECVE v4.0 patterns that SNP implements, for traceability.

|SNP Rule                   |ECVE Source                   |Pattern                                      |
|---------------------------|------------------------------|---------------------------------------------|
|§4.1 BOM Stripping         |ECVE v4.0 Step 0.1           |Strip `\xEF\xBB\xBF`                        |
|§4.2 Trailing Column Removal|ECVE v4.0 Step 0.2          |100% empty columns removed                  |
|§4.5 Step 1 (Currency)     |ECVE v4.0 Appendix A.6 Step 1|`/^[$€£¥₹₩₽₺₱฿]\s*/`                       |
|§4.5 Step 2 (Thousands)    |ECVE v4.0 Appendix A.6 Step 2|`/,(?=\d{3}(?:[,.]|\b))/g`                  |
|§4.5 Step 3 (Percent)      |ECVE v4.0 Appendix A.6 Step 3|`/%$/`                                       |
|§4.7 Date (en-US)          |ECVE v4.0 Appendix A.7       |`/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/` → `$3-$1-$2`|
|§4.7 Date (en-GB)          |ECVE v4.0 Appendix A.7       |`/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/` → `$3-$2-$1`|
|§4.7 Date (de-DE)          |ECVE v4.0 Appendix A.7       |`/^(\d{1,2})\.(\d{1,2})\.(\d{4})$/` → `$3-$2-$1`|
|§4.7 Date (ja-JP)          |ECVE v4.0 Appendix A.7       |`/^(\d{4})\/(\d{1,2})\/(\d{1,2})$/` → `$1-$2-$3`|

When ECVE updates these patterns in a future version, SNP adopts the updated patterns in its next release. ECVE is the normative source; SNP is the execution point.

-----

*End of specification.*
