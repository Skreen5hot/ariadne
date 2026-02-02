# Sanitization & Ingestion Service (SIS) Specification

**Document ID:** `sis-core-01`
**Version:** 2.0.0
**Status:** APPROVED
**Classification:** FNSR Core Security Component

---

## Document Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0-draft | 2025-02-01 | Initial specification |
| 1.1.0 | 2025-02-01 | Corrected latency targets μs→ms. Added JSON envelope validation. Mandated DFA regex. Added tiered processing. |
| 1.1.1 | 2025-02-01 | Fixed async ML race condition with hold-pending-analysis model. |
| 2.0.0 | 2025-02-01 | **Major revision:** Added formal position mapping API (§3.4). Expanded charset/encoding handling (§3.5). Added pattern DB governance workflow (§5). Added pending queue persistence semantics (§8.5). Added cryptographic key management (§10.3). Added benchmark environment requirements (§7.6). Added ML governance (§9.3). Formalized fail-open/fail-closed policy (§11). Added testing requirements (§12). Fixed schema notations. Unified terminology. |

---

## 1. Executive Summary

The Sanitization & Ingestion Service (SIS) is the first line of defense in FNSR's defense-in-depth security architecture. Operating at the syntactic layer with **millisecond** latency requirements, SIS performs pattern-based filtering to detect and neutralize character-level and encoding-level attacks before any semantic processing occurs.

### 1.1 Design Principles

1. **Syntactic-only processing:** SIS does not interpret meaning—that's ECCPS's job
2. **Single source of truth:** SIS-normalized content is authoritative for all downstream
3. **Deterministic mapping:** Position transformations are fully reconstructible
4. **Fail-secure by default:** Ambiguous cases quarantine rather than release
5. **Defense in depth:** Multiple detection layers with graceful degradation

### 1.2 Performance Reality

| Operation | Physical Minimum | Notes |
|-----------|------------------|-------|
| Read 1MiB from RAM | ~20μs | Memory bandwidth ~50GB/s |
| Parse 1MiB JSON | 2-15ms | Even with SIMD parsers |
| Network round-trip (loopback) | 30-100μs | gRPC/HTTP overhead |
| Unicode normalization (1MiB) | 1-5ms | NFC transformation |
| Regex scan (1MiB, DFA) | 0.5-2ms | Linear time, no backtracking |

**Unit Convention:** This specification uses **MiB (mebibytes, 2²⁰ = 1,048,576 bytes)** for all size references unless explicitly stated as MB (10⁶ bytes).

---

## 2. Architectural Position

### 2.1 System Context

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FNSR Security Architecture                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   External Input ──▶ [API Gateway] ──▶ fnsr.document.submitted              │
│                                              │                              │
│                                              ▼                              │
│                      ┌──────────────────────────────────────┐               │
│                      │    SANITIZATION & INGESTION SERVICE   │              │
│                      │            (SIS-CORE-01 v2.0)         │              │
│                      │                                       │              │
│                      │  • Charset detection & transcoding    │              │
│                      │  • JSON envelope validation           │              │
│                      │  • Pattern-based syntactic filtering  │              │
│                      │  • Encoding normalization (NFC)       │              │
│                      │  • Position mapping preservation      │              │
│                      │  • <5ms P99 latency (small tier)      │              │
│                      └───────────────┬──────────────────────┘               │
│                                      │                                      │
│                     ┌────────────────┴────────────────┐                     │
│                     │                                 │                     │
│                     ▼                                 ▼                     │
│      fnsr.document.sanitized              fnsr.input.quarantined            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Normalization Contract

**CRITICAL:** All downstream services MUST use SIS-normalized content exclusively.

```yaml
normalization_contract:
  
  # SIS is the SOLE normalizer
  authority: SIS
  
  # Normalization form choice and rationale
  normalization_form: NFC
  rationale: >
    NFC (Canonical Composition) chosen over NFKC because:
    1. NFC preserves semantic distinctions (e.g., ﬁ ligature vs "fi")
    2. NFC is reversible for display purposes
    3. NFKC collapses characters that may have distinct meaning
    4. Most text processing libraries default to NFC
    
  nfkc_consideration: >
    NFKC may be desirable for security-critical comparisons (collapses
    more attack variants). Available as opt-in per-tenant policy.
    When NFKC is used, original NFC form is preserved in metadata.
    
  # What downstream must do
  downstream_requirements:
    - Use ONLY sanitized_payload.normalized_content
    - NEVER re-normalize (will break position mapping)
    - Use position_map API for original↔normalized offset translation
    - Request original content from Quarantine Store ONLY with justification
    
  # What SIS guarantees
  sis_guarantees:
    - Deterministic: same input always produces same output
    - Reversible mapping: positions can be translated both directions
    - Original preserved: encrypted in quarantine for forensics
    - Transforms logged: all normalizations recorded with positions
```

### 2.3 Query Path Integration

| Query Path | SIS Processing | Rationale |
|------------|----------------|-----------|
| **Fast** | BYPASSED | Cached queries already validated |
| **Standard** | ACTIVE | All new input must pass validation |
| **Full** | ACTIVE | Comprehensive processing |

---

## 3. Event Contract

### 3.1 Consumed Events

#### `fnsr.document.submitted`

```yaml
event_type: fnsr.document.submitted
version: "2.0"
schema:
  $schema: "https://json-schema.org/draft/2020-12/schema"
  type: object
  required:
    - event_id
    - trace_id
    - timestamp
    - source
    - payload
  properties:
  
    event_id:
      type: string
      format: uuid
      description: Unique identifier for this submission event
      
    trace_id:
      type: string
      format: uuid
      description: Distributed trace ID for correlation across services
      
    request_id:
      type: string
      description: Optional client-provided request identifier
      
    timestamp:
      type: string
      format: date-time
      description: ISO 8601 timestamp of submission
      
    source:
      type: object
      required:
        - origin_type
        - origin_id
      properties:
        origin_type:
          type: string
          enum: [user_interface, api_client, federated_node, internal_service]
        origin_id:
          type: string
          description: Authenticated identifier of the source
        session_id:
          type: string
          format: uuid
        ip_address:
          oneOf:
            - type: string
              format: ipv4
            - type: string
              format: ipv6
        user_agent:
          type: string
          maxLength: 1024
          
    payload:
      type: object
      required:
        - content_type
        - content
      properties:
        content_type:
          type: string
          enum: [text/plain, text/markdown, application/json, multipart/mixed]
          
        content:
          type: string
          description: >
            Content with encoding specified by content_transfer_encoding.
            For base64: standard Base64 (RFC 4648) with optional MIME line breaks.
          maxLength: 1572864  # 1.5 MiB to accommodate Base64 + MIME overhead
          
        content_transfer_encoding:
          type: string
          enum: [utf-8, base64, quoted-printable, binary]
          default: utf-8
          description: How content field is encoded in the JSON payload
          
        charset:
          type: string
          description: >
            Source character set for text content. SIS will transcode to UTF-8.
            Required for non-UTF-8 text.
          enum: [utf-8, iso-8859-1, windows-1252, us-ascii]
          default: utf-8
          
        charset_declared_by:
          type: string
          enum: [client_header, content_type_param, bom, sniffed, assumed]
          description: How charset was determined (for audit)
```

### 3.2 Produced Events

#### `fnsr.document.sanitized`

```yaml
event_type: fnsr.document.sanitized
version: "2.0"
schema:
  $schema: "https://json-schema.org/draft/2020-12/schema"
  type: object
  required:
    - event_id
    - trace_id
    - timestamp
    - source_event_id
    - processing_metadata
    - sanitized_payload
  properties:
  
    event_id:
      type: string
      format: uuid
      
    trace_id:
      type: string
      format: uuid
      description: Preserved from input for distributed tracing
      
    timestamp:
      type: string
      format: date-time
      
    source_event_id:
      type: string
      format: uuid
      
    analysis_status:
      type: string
      enum: [complete, pending_ml]
      description: >
        'complete': all analysis done, safe to deliver.
        'pending_ml': ECCPS must HOLD until ML callback (see §8.4)
      
    processing_metadata:
      type: object
      required:
        - processing_time_ms
        - processing_tier
        - sis_version
        - pattern_db_version
        - regex_engine
      properties:
      
        processing_time_ms:
          type: number
          description: Total processing time in milliseconds
          
        payload_size_bytes:
          type: integer
          description: Original payload size
          
        processing_tier:
          type: string
          enum: [small, medium, large]
          
        stages_executed:
          type: array
          items:
            type: object
            properties:
              stage: { type: string }
              duration_ms: { type: number }
              result: { type: string, enum: [pass, flag, skip] }
              
        patterns_checked:
          type: integer
          
        detections:
          type: array
          items:
            $ref: '#/$defs/Detection'
          description: Syntactic flags for ECCPS consideration (not quarantine-worthy alone)
          
        normalizations_applied:
          type: array
          items:
            $ref: '#/$defs/NormalizationRecord'
            
        charset_transcoding:
          type: object
          properties:
            source_charset: { type: string }
            target_charset: { type: string, const: "utf-8" }
            bytes_transcoded: { type: integer }
            transcoding_errors: { type: integer }
            
        position_map_id:
          type: string
          format: uuid
          description: >
            ID to retrieve full position mapping via API.
            Present only if original_length != normalized_length.
            
        sis_version:
          type: string
          
        pattern_db_version:
          type: string
          
        regex_engine:
          type: string
          enum: [rust_regex, re2, hyperscan]
          
    sanitized_payload:
      type: object
      required:
        - content_type
        - normalized_content
        - content_hash
        - original_length
        - normalized_length
      properties:
        content_type:
          type: string
        normalized_content:
          type: string
          description: UTF-8 NFC normalized content
        content_hash:
          type: string
          pattern: "^[a-f0-9]{64}$"
          description: SHA-256 of normalized content
        original_length:
          type: integer
          description: Byte length before normalization
        normalized_length:
          type: integer
          description: Byte length after normalization
        grapheme_count:
          type: integer
          description: Number of extended grapheme clusters (user-perceived characters)

  $defs:
    Detection:
      type: object
      required: [detection_id, pattern_id, category, confidence, severity]
      properties:
        detection_id:
          type: string
          format: uuid
        pattern_id:
          type: string
        category:
          type: string
          enum: [JSON, HGL, INV, ENC, INJ, CTL, UNI, SEQ, MLX, CHARSET]
        confidence:
          type: number
          minimum: 0
          maximum: 1
        severity:
          type: string
          enum: [LOW, MEDIUM, HIGH, CRITICAL]
        evidence:
          type: object
          properties:
            normalized_byte_start: { type: integer }
            normalized_byte_end: { type: integer }
            matched_content_hash:
              type: string
              description: SHA-256 of matched segment (not raw content, for size control)
            context_summary:
              type: string
              maxLength: 256
              description: Redacted/truncated context for debugging
              
    NormalizationRecord:
      type: object
      required: [normalization_type, count]
      properties:
        normalization_type:
          type: string
          enum: 
            - unicode_nfc
            - unicode_nfkc
            - charset_transcode
            - encoding_repair
            - whitespace_normalize
            - control_char_strip
            - bom_removal
            - json_structure_validated
        count:
          type: integer
          description: Number of positions affected
        sample_positions:
          type: array
          maxItems: 10
          items:
            type: object
            properties:
              original_byte_offset: { type: integer }
              normalized_byte_offset: { type: integer }
              original_bytes_hash: { type: string }
              normalized_to_hash: { type: string }
          description: >
            Sample of affected positions (max 10). Full mapping via position_map API.
```

### 3.3 Quarantine Event

```yaml
event_type: fnsr.input.quarantined
version: "2.0"
schema:
  type: object
  required:
    - event_id
    - trace_id
    - timestamp
    - source_event_id
    - quarantine_record
  properties:
    event_id:
      type: string
      format: uuid
    trace_id:
      type: string
      format: uuid
    timestamp:
      type: string
      format: date-time
    source_event_id:
      type: string
      format: uuid
    quarantine_record:
      type: object
      required:
        - quarantine_id
        - severity
        - detection_summary
        - detections
        - disposition
        - forensic_reference
      properties:
        quarantine_id:
          type: string
          format: uuid
        severity:
          type: string
          enum: [LOW, MEDIUM, HIGH, CRITICAL]
        detection_summary:
          type: object
          properties:
            total_detections: { type: integer }
            categories: { type: array, items: { type: string } }
            confidence_weighted_score: { type: number, minimum: 0, maximum: 1 }
        detections:
          type: array
          items:
            $ref: '#/$defs/Detection'
        disposition:
          type: object
          required: [action, reason_code]
          properties:
            action:
              type: string
              enum: [quarantine_full, quarantine_partial, flag_for_review]
            reason_code:
              type: string
            reason_text:
              type: string
            escalation_required:
              type: boolean
            human_review_deadline_hours:
              type: integer
        forensic_reference:
          type: object
          required: [content_ref_id, content_hash, encryption_key_id]
          properties:
            content_ref_id:
              type: string
              format: uuid
              description: Reference to encrypted content in Quarantine Store
            content_hash:
              type: string
              pattern: "^[a-f0-9]{64}$"
              description: SHA-256 of original content for integrity
            encryption_key_id:
              type: string
              description: KMS key ID used for encryption (NOT the key itself)
            retention_until:
              type: string
              format: date-time
              description: When content will be purged (per retention policy)
```

### 3.4 Position Mapping API (NEW - CRITICAL)

Position mapping enables downstream services to translate between original and normalized byte/grapheme offsets.

```yaml
position_mapping:

  # ═══════════════════════════════════════════════════════════════════════════
  # PROBLEM STATEMENT
  # ═══════════════════════════════════════════════════════════════════════════
  
  problem: >
    Unicode normalization (NFC) can change string length. Combining marks may
    merge, ligatures may expand, and charset transcoding may alter byte counts.
    Downstream services (ECCPS, UI) need to map positions between original and
    normalized content for accurate highlighting and attribution.
    
  complexity_factors:
    - NFC combining mark composition: 2+ codepoints → 1 codepoint
    - Charset transcoding: 1 byte (ISO-8859-1) → 1-3 bytes (UTF-8)
    - Grapheme clusters: 1 user-visible character may be multiple codepoints
    - Many-to-many mappings in edge cases
    
  # ═══════════════════════════════════════════════════════════════════════════
  # REPRESENTATION
  # ═══════════════════════════════════════════════════════════════════════════
  
  representation: sparse_anchor_map
  
  anchor_definition:
    type: object
    properties:
      original_byte_offset:
        type: integer
        description: Byte offset in original content
      normalized_byte_offset:
        type: integer
        description: Corresponding byte offset in normalized content
      original_grapheme_index:
        type: integer
        description: Grapheme cluster index in original
      normalized_grapheme_index:
        type: integer
        description: Grapheme cluster index in normalized
      span_bytes:
        type: integer
        description: Number of bytes this anchor covers (for delta encoding)
      chunk_hash:
        type: string
        description: SHA-256 of the span for verification
        
  # Anchors placed at:
  anchor_placement:
    - Every normalization transformation point
    - Every 4KB boundary (for random access)
    - Start and end of content
    
  # ═══════════════════════════════════════════════════════════════════════════
  # RETRIEVAL API
  # ═══════════════════════════════════════════════════════════════════════════
  
  api:
    endpoint: GET /sis/v1/position-map/{event_id}
    
    parameters:
      event_id:
        type: string
        format: uuid
        required: true
        
      range:
        type: string
        pattern: "^\\d+:\\d+$"
        description: "Byte range to retrieve (e.g., '0:4096'). Omit for full map."
        
      direction:
        type: string
        enum: [original_to_normalized, normalized_to_original]
        default: original_to_normalized
        
      format:
        type: string
        enum: [json, delta_encoded]
        default: json
        description: delta_encoded is more compact for large maps
        
    response:
      type: object
      properties:
        event_id: { type: string, format: uuid }
        total_anchors: { type: integer }
        returned_anchors: { type: integer }
        anchors:
          type: array
          items:
            $ref: '#/anchor_definition'
        next_cursor:
          type: string
          description: For pagination of large maps
          
    # Streaming for maps > 1 MiB
    streaming:
      threshold_bytes: 1048576
      method: chunked_transfer_encoding
      chunk_size: 65536
      
  # ═══════════════════════════════════════════════════════════════════════════
  # MAPPING ALGORITHM
  # ═══════════════════════════════════════════════════════════════════════════
  
  mapping_algorithm:
    name: anchor_interpolation
    
    steps:
      - Find anchors bracketing the target offset
      - If exact anchor exists, return directly
      - Otherwise, linear interpolate between anchors
      - Verify with chunk_hash if precision required
      
    guarantees:
      - Deterministic: same inputs always produce same mapping
      - Reversible: can map both directions
      - Verifiable: chunk hashes enable integrity checking
      
    code_example: |
      def map_offset(target_offset: int, anchors: List[Anchor], direction: str) -> int:
          """Map offset between original and normalized content."""
          
          if direction == "original_to_normalized":
              src_field, dst_field = "original_byte_offset", "normalized_byte_offset"
          else:
              src_field, dst_field = "normalized_byte_offset", "original_byte_offset"
          
          # Binary search for bracketing anchors
          left = find_anchor_before(anchors, target_offset, src_field)
          right = find_anchor_after(anchors, target_offset, src_field)
          
          if left[src_field] == target_offset:
              return left[dst_field]
          
          # Linear interpolation
          src_delta = target_offset - left[src_field]
          src_span = right[src_field] - left[src_field]
          dst_span = right[dst_field] - left[dst_field]
          
          return left[dst_field] + int(src_delta * dst_span / src_span)
          
  # ═══════════════════════════════════════════════════════════════════════════
  # STORAGE & LIMITS
  # ═══════════════════════════════════════════════════════════════════════════
  
  storage:
    max_map_size_bytes: 10485760  # 10 MiB
    compression: zstd
    retention: same_as_audit_logs  # 90 days
    
  limits:
    max_anchors_per_document: 100000
    on_limit_exceeded:
      action: store_manifest_with_streaming_api
      manifest_contains: [total_anchors, anchor_positions, chunk_hashes]
```

### 3.5 Charset & Encoding Handling (NEW - CRITICAL)

```yaml
charset_encoding_handling:

  # ═══════════════════════════════════════════════════════════════════════════
  # SUPPORTED ENCODINGS
  # ═══════════════════════════════════════════════════════════════════════════
  
  content_transfer_encodings:
    utf-8:
      description: Raw UTF-8 text
      validation: Check for valid UTF-8 sequences
      
    base64:
      description: Standard Base64 (RFC 4648)
      variants_accepted:
        - Standard (A-Za-z0-9+/)
        - URL-safe (A-Za-z0-9-_)
        - With or without padding (=)
        - With MIME line breaks (CRLF every 76 chars)
      max_decoded_size: 1048576  # 1 MiB
      
    quoted-printable:
      description: RFC 2045 quoted-printable
      validation: Decode and validate resulting charset
      
    binary:
      description: Raw bytes, must be Base64 encoded in JSON
      handling: Treat as base64 with binary flag
      
  # ═══════════════════════════════════════════════════════════════════════════
  # CHARSET DETECTION & TRANSCODING
  # ═══════════════════════════════════════════════════════════════════════════
  
  charset_handling:
    target_charset: utf-8
    
    supported_source_charsets:
      utf-8:
        bom: "EF BB BF"
        action: validate_and_strip_bom
        
      utf-16le:
        bom: "FF FE"
        action: transcode_to_utf8
        
      utf-16be:
        bom: "FE FF"
        action: transcode_to_utf8
        
      iso-8859-1:
        detection: statistical_byte_profile
        action: transcode_to_utf8
        notes: "Latin-1, 1 byte = 1 char"
        
      windows-1252:
        detection: presence_of_0x80-0x9F_printable_chars
        action: transcode_to_utf8
        notes: "Windows Western European"
        
      us-ascii:
        detection: all_bytes_below_0x80
        action: pass_through  # ASCII is valid UTF-8
        
    unsupported_charsets:
      action: quarantine
      reason_code: UNSUPPORTED_CHARSET
      
  # ═══════════════════════════════════════════════════════════════════════════
  # CHARSET SNIFFING
  # ═══════════════════════════════════════════════════════════════════════════
  
  charset_sniffing:
    priority_order:
      1: bom_detection
      2: client_declared_charset
      3: content_type_charset_param
      4: statistical_analysis
      5: assume_utf8
      
    statistical_analysis:
      method: byte_frequency_profile
      confidence_threshold: 0.8
      
    declared_vs_actual_mismatch:
      action: >
        If sniffed charset differs from declared with confidence >= 0.8:
        - Flag with CHARSET_MISMATCH detection
        - If confidence >= 0.95: quarantine (likely attack)
        - If confidence 0.8-0.95: continue with sniffed charset + flag
        
  # ═══════════════════════════════════════════════════════════════════════════
  # TRANSCODING ERRORS
  # ═══════════════════════════════════════════════════════════════════════════
  
  transcoding_errors:
    invalid_sequences:
      action: replace_with_replacement_character  # U+FFFD
      log: true
      threshold_for_quarantine: 0.05  # >5% invalid = quarantine
      
    unmappable_characters:
      action: replace_with_replacement_character
      log: true
```

---

## 4. Detection Architecture

### 4.1 Detection Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SIS DETECTION PIPELINE (v2.0)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Input ──▶ [Stage 0: Envelope] ──▶ [Stage 1: Charset] ──▶ [Stage 2: Fast]  │
│                  │                       │                     │            │
│                  │ (JSON attack)         │ (bad charset)       │ (known bad)│
│                  ▼                       ▼                     ▼            │
│            QUARANTINE              QUARANTINE             QUARANTINE        │
│                                                                │            │
│                                                                ▼            │
│                                                    [Stage 3: Normalize]     │
│                                                          │                  │
│                                                          ▼                  │
│                                                    [Stage 4: Pattern]       │
│                                                          │                  │
│                    ┌─────────────────────────────────────┼─────────────┐    │
│                    │                 │                   │             │    │
│                    ▼                 ▼                   ▼             ▼    │
│              [Homoglyph]      [Invisible]         [Encoding]     [Inject]   │
│                    │                 │                   │             │    │
│                    └─────────────────────────────────────┼─────────────┘    │
│                                                          │                  │
│                                                          ▼                  │
│                                                    [Stage 5: Statistical]   │
│                                                          │                  │
│                                                          ▼                  │
│                                                    [Stage 6: ML]            │
│                                                    (async if large)         │
│                                                          │                  │
│                                                          ▼                  │
│                                                    [Stage 7: Aggregate]     │
│                                                          │                  │
│                         ┌────────────────────────────────┴──────────────┐   │
│                         │                                               │   │
│                         ▼                                               ▼   │
│              fnsr.document.sanitized                    fnsr.input.quarantined
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Stage 0: JSON Envelope Validation

```yaml
json_envelope_validation:
  
  structural_limits:
    max_depth: 10
    max_key_length: 256
    max_string_length: 1572864
    max_array_length: 1000
    max_object_keys: 100
    
  parser_configuration:
    primary: simd-json
    fallback: serde_json
    
    simd_json_config:
      max_depth: 10
      # simd-json doesn't support max_keys natively; enforce post-parse
      
    serde_json_config:
      deserializer: from_slice
      recursion_limit: 10
      
  hash_collision_protection:
    hasher: siphash-2-4
    rationale: "Resistant to hash-flooding attacks on object keys"
    
  attacks_mitigated:
    - json_bomb (max_depth)
    - key_flooding (max_object_keys + SipHash)
    - string_bomb (max_string_length)
    - array_bomb (max_array_length)
```

### 4.3 Stage 1: Charset Detection & Transcoding (NEW)

```yaml
charset_stage:
  
  order_of_operations:
    1: Detect BOM and strip if present
    2: Validate declared charset against content
    3: Sniff charset if not declared or mismatch
    4: Transcode to UTF-8 if needed
    5: Validate resulting UTF-8
    
  timing_budget:
    small: 0.2ms
    medium: 0.5ms
    large: 2ms
    
  failure_modes:
    invalid_utf8_after_transcode:
      action: quarantine
      reason: CHARSET_TRANSCODING_FAILED
      
    high_replacement_char_ratio:
      threshold: 0.05
      action: quarantine
      reason: CHARSET_CORRUPTION
```

### 4.4 Regex Engine Requirements

```yaml
regex_requirements:
  
  engine_type: DFA
  rationale: >
    DFA (Deterministic Finite Automaton) engines guarantee O(n) time
    complexity, structurally preventing ReDoS attacks. No timeouts
    needed when time is bounded by input size.
    
  allowed_engines:
    rust_regex:
      crate: "regex >= 1.10"
      unicode_support: full
      notes: "Default choice. Unicode-aware, DFA-based."
      
    re2:
      library: "google/re2"
      unicode_support: full
      notes: "Battle-tested C++ engine."
      
    hyperscan:
      library: "intel/hyperscan"
      unicode_support: limited
      cpu_requirements: [SSE4.2, AVX2]
      notes: >
        SIMD-accelerated, excellent for multiple patterns.
        Requires specific CPU features.
      fallback: rust_regex
      
  prohibited_engines:
    - pcre (backtracking)
    - pcre2 (backtracking by default)
    - python re (backtracking)
    - javascript RegExp (backtracking)
    
  features_not_available:
    - backreferences
    - lookahead/lookbehind
    - atomic groups
    alternative: >
      Patterns requiring these features must use custom deterministic
      code with strict resource limits and sandboxing.
      
  defense_in_depth_timeout:
    enabled: true
    value_ms: 100
    rationale: >
      While DFA is O(n), we keep a timeout as defense against:
      - Bugs in regex engine
      - Miscompiled patterns
      - Extreme system load
      This should never trigger under normal operation.
```

---

## 5. Pattern Database Governance (NEW - HIGH)

```yaml
pattern_db_governance:

  # ═══════════════════════════════════════════════════════════════════════════
  # PATTERN LIFECYCLE
  # ═══════════════════════════════════════════════════════════════════════════
  
  lifecycle_stages:
    
    1_development:
      environment: dev
      requirements:
        - Pattern author identified
        - Test cases (benign + adversarial) provided
        - Complexity score computed
        - Estimated execution time measured
        
    2_review:
      requirements:
        - Security team review (2 approvers)
        - False positive rate measured on benign corpus (>100K samples)
        - Detection rate measured on adversarial corpus
        - No regression on existing detection benchmarks
        
    3_staging:
      environment: staging
      traffic: shadow_mode (analyze but don't act)
      duration: 24_hours_minimum
      metrics_collected:
        - false_positive_rate
        - detection_rate
        - execution_time_percentiles
        
    4_canary:
      environment: production
      traffic_percentage: 5%
      duration: 4_hours_minimum
      rollback_triggers:
        - false_positive_rate > baseline + 0.1%
        - p99_latency > baseline + 2ms
        - error_rate > 0.01%
        
    5_production:
      traffic_percentage: 100%
      monitoring: continuous
      
  # ═══════════════════════════════════════════════════════════════════════════
  # PATTERN VALIDATION
  # ═══════════════════════════════════════════════════════════════════════════
  
  validation_requirements:
    
    complexity_scoring:
      metrics:
        - nfa_state_count
        - estimated_memory_bytes
        - benchmark_execution_ms_per_kb
      rejection_threshold:
        max_states: 10000
        max_memory_mb: 10
        max_ms_per_kb: 0.1
        
    corpus_testing:
      benign_corpus:
        minimum_size: 100000
        sources: [wikipedia, news, code_samples, chat_logs]
        max_false_positive_rate: 0.001  # 0.1%
        
      adversarial_corpus:
        minimum_size: 10000
        sources: [known_attacks, fuzzer_output, research_samples]
        min_detection_rate: 0.95  # 95%
        
    regression_testing:
      requirement: >
        Every pattern update must pass full regression suite.
        No existing detection may regress without explicit approval.
        
  # ═══════════════════════════════════════════════════════════════════════════
  # CRYPTOGRAPHIC INTEGRITY
  # ═══════════════════════════════════════════════════════════════════════════
  
  integrity:
    
    signing:
      algorithm: Ed25519
      key_management: HSM-backed signing keys
      signature_coverage:
        - pattern_content
        - pattern_metadata
        - version
        - timestamp
        
    manifest:
      format: signed_json
      contents:
        - version
        - pattern_count
        - pattern_hashes (SHA-256)
        - aggregate_hash
        - signatures
        
    verification:
      on_load: mandatory
      on_update: mandatory
      failure_action: reject_and_alert
      
  # ═══════════════════════════════════════════════════════════════════════════
  # ROLLBACK
  # ═══════════════════════════════════════════════════════════════════════════
  
  rollback:
    
    automatic_triggers:
      - false_positive_spike (>2x baseline for 5 minutes)
      - latency_spike (p99 > 2x baseline for 5 minutes)
      - error_rate (>1% for 1 minute)
      
    rollback_procedure:
      1: Halt canary progression
      2: Revert to previous signed manifest
      3: Alert on-call security engineer
      4: Preserve metrics for post-mortem
      
    version_retention:
      count: 10  # Keep last 10 versions for rollback
```

---

## 6. SIS/ECCPS Boundary

### 6.1 Responsibility Matrix

| Concern | SIS | ECCPS |
|---------|-----|-------|
| JSON structure validation | ✓ | — |
| Charset detection/transcoding | ✓ | — |
| Unicode normalization | ✓ | — |
| Position mapping | ✓ | Consumer |
| Homoglyph detection | ✓ Syntactic | Semantic intent |
| Invisible character detection | ✓ Syntactic | Semantic intent |
| Prompt injection patterns | ✓ Flag syntactic | Determine actual injection |
| Taint level assignment | — | ✓ |
| Semantic deception | — | ✓ |

### 6.2 No Semantic Judgments Principle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│   SIS MUST NEVER:                                                           │
│   ✗ Interpret meaning    ✗ Assess harm    ✗ Determine intent                │
│   ✗ Make value judgments ✗ Block by topic ✗ Assign taint levels             │
│                                                                             │
│   SIS MAY ONLY:                                                             │
│   ✓ Validate structure   ✓ Detect patterns  ✓ Normalize encodings           │
│   ✓ Flag anomalies       ✓ Measure statistics ✓ Quarantine known-bad        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Performance Requirements

### 7.1 Latency Specifications

```yaml
latency_requirements:
  
  targets_by_tier:
    small:  # <10 KiB
      p50: 1ms
      p95: 2ms
      p99: 3ms
      p999: 10ms
      
    medium:  # 10-100 KiB
      p50: 3ms
      p95: 7ms
      p99: 10ms
      p999: 25ms
      
    large:  # 100 KiB - 1 MiB
      p50: 10ms
      p95: 18ms
      p99: 25ms
      p999: 50ms
      
  hard_limits:
    absolute_max: 100ms
    action_on_exceed: circuit_break_and_release_with_flag
```

### 7.2 Stage Latency Budgets

| Stage | Small | Medium | Large |
|-------|-------|--------|-------|
| 0: JSON Validate | 0.1ms | 0.3ms | 1ms |
| 1: Charset | 0.1ms | 0.3ms | 1ms |
| 2: Fast Reject | 0.05ms | 0.1ms | 0.2ms |
| 3: Normalize | 0.2ms | 1ms | 4ms |
| 4: Pattern Scan | 0.3ms | 2ms | 8ms |
| 5: Statistical | 0.1ms | 0.3ms | 1ms |
| 6: ML | 0.5ms | 2ms | **ASYNC** |
| 7: Aggregate | 0.05ms | 0.1ms | 0.2ms |
| **Total** | ~1.4ms | ~6ms | ~15ms + async |

### 7.3 Tiered Processing Model

```yaml
tiered_processing:
  
  small_tier:
    size_range: "0 - 10 KiB"
    ml_mode: synchronous
    delivery: immediate_on_completion
    
  medium_tier:
    size_range: "10 KiB - 100 KiB"
    ml_mode: synchronous_with_timeout
    ml_timeout_ms: 5
    delivery: immediate_on_completion
    
  large_tier:
    size_range: "100 KiB - 1 MiB"
    ml_mode: async_with_hold
    delivery: eccps_holds_until_ml_callback_or_timeout
    ml_timeout_ms: 500
    
  oversized:
    size_range: "> 1 MiB"
    action: reject_at_gateway
```

### 7.4 Throughput Specifications

```yaml
throughput:
  sustained_rps: 10000
  burst_rps: 50000
  burst_duration_seconds: 30
  sustained_bandwidth: 1 GiB/s
```

### 7.5 Scaling Configuration

```yaml
scaling:
  min_replicas: 3
  max_replicas: 100
  scale_up_threshold: 0.7  # CPU utilization
  scale_down_threshold: 0.3
  scale_up_cooldown_seconds: 30
  scale_down_cooldown_seconds: 300
```

### 7.6 Benchmark Environment Requirements (NEW - HIGH)

```yaml
benchmark_requirements:

  # SLOs are ONLY valid when measured in specified environment
  
  reference_environment:
    cpu: "AMD EPYC 7R13 or Intel Xeon Platinum 8375C"
    cores_per_instance: 4
    memory_per_instance: 8 GiB
    network: "10 Gbps minimum"
    storage: "NVMe SSD, >50K IOPS"
    containerization: "Kubernetes with dedicated node pools"
    kernel: "Linux 5.15+ with performance governor"
    
  measurement_requirements:
    warm_start:
      warmup_requests: 10000
      measurement_requests: 100000
      
    cold_start:
      measurement_after_restart: true
      acceptable_degradation: "2x warm latency for first 100 requests"
      
    tail_latency:
      measure_p9999: true
      acceptable_p9999: "3x p99"
      
  verification_artifacts:
    required:
      - benchmark_report.json (machine-readable results)
      - environment_spec.yaml (exact environment used)
      - corpus_manifest.json (test data used)
      - flamegraph.svg (CPU profile)
      
  platform_notes:
    rust:
      expected_performance: baseline
      build_flags: "--release with LTO"
      
    go:
      expected_degradation: "1.5-2x Rust baseline"
      gc_tuning: "GOGC=100, GOMEMLIMIT set"
      
    java:
      expected_degradation: "2-3x Rust baseline"
      jvm_flags: "-XX:+UseZGC -Xmx4g"
      warmup_required: "Extended (50K requests)"
```

---

## 8. Async ML Protocol

### 8.1 Protocol Overview

```yaml
async_ml_protocol:

  trigger: "payload_size > 100 KiB"
  
  sequence:
    1: SIS completes stages 0-5, 7 synchronously
    2: SIS spawns async ML task
    3: SIS emits fnsr.document.sanitized with analysis_status: pending_ml
    4: ECCPS receives, processes semantic analysis, HOLDS delivery
    5: User sees "Processing..." (NOT content)
    6: ML completes, emits fnsr.ml.analysis_complete
    7: ECCPS receives callback, makes final decision
    8: Content delivered or blocked
    
  timeout:
    value_ms: 500
    action: release_with_elevated_flag
    flag: ml_analysis_incomplete
```

### 8.2 Sequence Diagram

```
  User        Gateway       SIS          ECCPS        ML Worker
    │            │           │             │              │
    │──Request──▶│           │             │              │
    │            │──Submit──▶│             │              │
    │            │           │──Stages 0-5─│              │
    │            │           │══Spawn═════════════════════▶
    │            │           │──Sanitized─▶│              │
    │            │           │  (pending)  │              │
    │◀─"Processing..."───────────────────────              │
    │  (spinner)             │             │              │
    │            │           │             │◀──Complete───│
    │            │           │             │   (clean)    │
    │◀─Content────────────────────────────────            │
    │                                                     │
```

### 8.3 ECCPS Contract

```yaml
eccps_pending_ml_contract:
  
  on_receive_pending_ml:
    - Complete ECCPS semantic analysis
    - Store in pending_delivery queue
    - DO NOT deliver to user
    - Start timeout timer (500ms)
    - Subscribe to fnsr.ml.analysis_complete
    
  on_ml_complete_clean:
    - Merge ML result with ECCPS analysis
    - Deliver to user
    
  on_ml_complete_suspicious:
    - DO NOT deliver
    - Quarantine
    - Notify security
    
  on_timeout:
    - Deliver with flag: ml_analysis_incomplete
    - Log for investigation
    - Emit metric
```

### 8.4 ML Analysis Events

```yaml
fnsr.ml.analysis_complete:
  type: object
  required: [event_id, trace_id, source_event_id, result]
  properties:
    event_id: { type: string, format: uuid }
    trace_id: { type: string, format: uuid }
    source_event_id: { type: string, format: uuid }
    result:
      type: string
      enum: [clean, suspicious, error]
    score:
      type: number
      minimum: 0
      maximum: 1
    confidence_interval:
      type: object
      properties:
        lower: { type: number }
        upper: { type: number }
    detections:
      type: array
      items:
        $ref: '#/$defs/Detection'
    model_metadata:
      type: object
      properties:
        model_version: { type: string }
        model_id: { type: string }
        features_used: { type: array, items: { type: string } }
    processing_time_ms: { type: number }
```

### 8.5 Pending Queue Persistence (NEW - HIGH)

```yaml
pending_queue:

  # ═══════════════════════════════════════════════════════════════════════════
  # STORAGE
  # ═══════════════════════════════════════════════════════════════════════════
  
  storage:
    primary: in_memory
    persistence: write_ahead_log
    
    wal_configuration:
      path: /var/lib/sis/pending_wal
      fsync: on_every_write
      max_size_mb: 1024
      rotation: on_size_or_hourly
      
  # ═══════════════════════════════════════════════════════════════════════════
  # LIMITS & BACKPRESSURE
  # ═══════════════════════════════════════════════════════════════════════════
  
  limits:
    max_pending_items: 10000
    max_memory_bytes: 1073741824  # 1 GiB
    max_item_age_ms: 60000  # 1 minute (well beyond 500ms timeout)
    
  backpressure:
    trigger_threshold: 0.8  # 80% of limits
    
    actions_when_triggered:
      - Emit metric: sis.pending_queue.backpressure
      - Alert on-call
      - For new large payloads: fall back to synchronous ML with extended timeout
      - If synchronous ML also times out: release with flag
      
    actions_when_critical:  # 95% of limits
      - Reject new large payloads with 503 Service Unavailable
      - Continue processing existing queue
      - Page on-call immediately
      
  # ═══════════════════════════════════════════════════════════════════════════
  # CRASH RECOVERY
  # ═══════════════════════════════════════════════════════════════════════════
  
  recovery:
    on_startup:
      1: Replay WAL to reconstruct pending queue
      2: For each pending item older than timeout: release with flag
      3: For each pending item within timeout: re-subscribe to ML callback
      4: Resume normal operation
      
    wal_corruption:
      action: discard_corrupted_entries
      alert: critical
      
  # ═══════════════════════════════════════════════════════════════════════════
  # PRIORITY
  # ═══════════════════════════════════════════════════════════════════════════
  
  priority:
    interactive_requests:
      priority: high
      timeout_ms: 500
      
    batch_requests:
      priority: low
      timeout_ms: 5000
      backpressure_first: true  # Shed batch load before interactive
```

---

## 9. ML Governance (NEW - MEDIUM)

```yaml
ml_governance:

  # ═══════════════════════════════════════════════════════════════════════════
  # MODEL VERSIONING
  # ═══════════════════════════════════════════════════════════════════════════
  
  versioning:
    format: "model_name-YYYYMMDD-hash"
    example: "sis_anomaly_detector-20250201-a1b2c3d4"
    
    artifacts_per_version:
      - model_weights (encrypted at rest)
      - feature_schema.json
      - training_config.yaml
      - validation_metrics.json
      - training_data_manifest.json (hashes, not data)
      
  # ═══════════════════════════════════════════════════════════════════════════
  # DEPLOYMENT
  # ═══════════════════════════════════════════════════════════════════════════
  
  deployment:
    strategy: canary
    
    stages:
      shadow:
        traffic: 0% (parallel execution, no action)
        duration: 24h
        metrics: [accuracy, latency, resource_usage]
        
      canary:
        traffic: 5%
        duration: 4h
        rollback_triggers:
          - accuracy_drop > 2%
          - false_positive_increase > 50%
          - latency_p99_increase > 20%
          
      production:
        traffic: 100%
        monitoring: continuous
        
  # ═══════════════════════════════════════════════════════════════════════════
  # MONITORING
  # ═══════════════════════════════════════════════════════════════════════════
  
  monitoring:
    
    drift_detection:
      input_distribution:
        method: population_stability_index
        threshold: 0.2
        window: 24h
        
      prediction_distribution:
        method: chi_squared_test
        threshold: 0.05
        window: 24h
        
      action_on_drift: alert_and_investigate
      
    adversarial_monitoring:
      track_near_threshold_predictions: true
      threshold_range: [0.4, 0.6]
      alert_on_spike: true
      
  # ═══════════════════════════════════════════════════════════════════════════
  # EXPLAINABILITY
  # ═══════════════════════════════════════════════════════════════════════════
  
  explainability:
    
    per_prediction:
      include_in_event:
        - top_5_contributing_features
        - feature_importance_scores
        - confidence_interval
        
    model_level:
      documentation:
        - feature_definitions
        - training_methodology
        - known_limitations
        - bias_assessment
```

---

## 10. Security Considerations

### 10.1 Self-Protection

```yaml
self_protection:
  
  regex:
    engine: DFA_only
    defense_in_depth_timeout_ms: 100
    
  resource_limits:
    max_input_size: 1048576  # 1 MiB
    max_pattern_matches: 1000
    max_normalizations: 100
    max_normalizations_exceeded_action: quarantine_with_reason
    json_max_depth: 10
    json_max_keys: 100
    
  circuit_breaker:
    error_rate_threshold: 0.5
    recovery_time_seconds: 60
```

### 10.2 Audit Requirements

```yaml
audit:
  
  decision_logging:
    retention_days: 90
    immutable: true
    
    fields:
      - event_id
      - trace_id
      - timestamp
      - decision
      - patterns_matched
      - processing_time_ms
      - payload_size_bytes
      - processing_tier
      - sis_version
      - pattern_db_version
      - regex_engine
      - ml_model_version (if applicable)
      
    pii_handling:
      content: never_logged (only hashes)
      ip_address: anonymize_after_7_days
      user_id: pseudonymize
      
  access_logging:
    quarantine_access: all_access_logged
    position_map_access: all_access_logged
```

### 10.3 Cryptographic Key Management (NEW - HIGH)

```yaml
key_management:

  # ═══════════════════════════════════════════════════════════════════════════
  # QUARANTINE ENCRYPTION
  # ═══════════════════════════════════════════════════════════════════════════
  
  quarantine_encryption:
    algorithm: AES-256-GCM
    key_source: aws_kms  # or gcp_kms, azure_keyvault, hashicorp_vault
    
    key_hierarchy:
      master_key:
        location: HSM-backed KMS
        rotation: annual
        
      data_encryption_key:
        derivation: per_quarantine_record
        algorithm: HKDF-SHA256
        rotation: derived_fresh_each_time
        
  # ═══════════════════════════════════════════════════════════════════════════
  # ACCESS CONTROL
  # ═══════════════════════════════════════════════════════════════════════════
  
  access_control:
    
    roles:
      sis_service:
        permissions: [encrypt]
        cannot: [decrypt, delete]
        
      security_analyst:
        permissions: [decrypt_with_approval]
        approval_required: true
        approval_workflow: two_person_rule
        
      security_lead:
        permissions: [approve_decrypt, decrypt]
        audit: enhanced
        
      incident_responder:
        permissions: [decrypt]
        condition: active_incident_ticket
        time_limit: incident_duration
        
    separation_of_duties:
      - No single role can both encrypt and delete
      - Decryption requires justification and approval
      - All access logged immutably
      
  # ═══════════════════════════════════════════════════════════════════════════
  # KEY ROTATION
  # ═══════════════════════════════════════════════════════════════════════════
  
  rotation:
    master_key:
      frequency: annual
      procedure: kms_managed_rotation
      
    signing_keys:
      frequency: quarterly
      overlap_period: 30_days
      
  # ═══════════════════════════════════════════════════════════════════════════
  # PATTERN DB SIGNING
  # ═══════════════════════════════════════════════════════════════════════════
  
  pattern_db_signing:
    algorithm: Ed25519
    key_storage: HSM
    
    signing_authority:
      required_approvers: 2
      from_team: security_engineering
      
    verification:
      on_load: mandatory
      on_update: mandatory
      failure: reject_and_alert_critical
```

---

## 11. Failure Modes & Policies (NEW - MEDIUM)

```yaml
failure_policies:

  # ═══════════════════════════════════════════════════════════════════════════
  # GLOBAL POLICY
  # ═══════════════════════════════════════════════════════════════════════════
  
  default_stance: fail_secure
  
  rationale: >
    SIS is a security service. When in doubt, protect the user by
    quarantining rather than releasing potentially harmful content.
    Specific exceptions documented below for availability tradeoffs.
    
  # ═══════════════════════════════════════════════════════════════════════════
  # COMPONENT FAILURES
  # ═══════════════════════════════════════════════════════════════════════════
  
  component_failures:
    
    sis_service_crash:
      detection: health_check_failure
      action: fail_closed
      behavior: >
        API Gateway returns 503. No content passes.
        Kubernetes restarts pod. Recovery in <30s typical.
      user_experience: "Service temporarily unavailable"
      
    ml_worker_unavailable:
      detection: callback_timeout + health_check
      action: fail_open_with_flag
      behavior: >
        Release content with ml_analysis_incomplete flag.
        ECCPS applies elevated scrutiny.
      rationale: >
        ML is defense-in-depth, not primary. Syntactic checks
        already passed. Availability preferred over blocking.
      user_experience: normal (slightly elevated monitoring)
      
    pattern_db_unavailable:
      detection: load_failure
      action: fail_closed
      behavior: >
        Reject all input until pattern DB restored.
        Critical alert to on-call.
      rationale: >
        Without patterns, SIS cannot perform its core function.
        Security must not be bypassed.
      user_experience: "Service temporarily unavailable"
      
    quarantine_store_unavailable:
      detection: write_failure
      action: fail_closed_for_quarantine_decisions
      behavior: >
        If content would be quarantined but store unavailable:
        reject with 503, do not release.
        Clean content can still pass.
      rationale: >
        Forensic chain of custody must be maintained.
        Cannot quarantine without storing evidence.
        
    event_bus_unavailable:
      detection: publish_failure
      action: local_queue_with_retry
      behavior: >
        Queue events locally (max 10K).
        Retry with exponential backoff.
        If queue full: fail_closed.
        
    position_map_api_unavailable:
      detection: api_health_check
      action: degraded_mode
      behavior: >
        Continue processing. position_map_id still set.
        API will recover; maps persisted.
      user_experience: >
        Downstream highlighting may be temporarily unavailable.
        
  # ═══════════════════════════════════════════════════════════════════════════
  # EXPLICIT FAIL-OPEN CASES
  # ═══════════════════════════════════════════════════════════════════════════
  
  explicit_fail_open:
    
    ml_timeout:
      condition: ML analysis exceeds 500ms
      action: release_with_flag
      flag: ml_analysis_incomplete
      monitoring: elevated
      rationale: >
        Blocking user indefinitely unacceptable.
        Syntactic checks passed. Risk accepted.
        
    processing_timeout:
      condition: Total processing exceeds 100ms
      action: release_with_flag
      flag: processing_timeout
      monitoring: elevated
      rationale: >
        Extreme edge case (should never happen).
        Log for investigation. Don't block user.
```

---

## 12. Testing Requirements (NEW)

```yaml
testing_requirements:

  # ═══════════════════════════════════════════════════════════════════════════
  # PERFORMANCE BENCHMARKS
  # ═══════════════════════════════════════════════════════════════════════════
  
  performance:
    
    benchmark_suite:
      corpus_sizes: [1KB, 10KB, 100KB, 500KB, 1MB]
      requests_per_size: 10000
      
      measurements:
        - p50, p95, p99, p999, p9999
        - throughput_rps
        - memory_usage
        - cpu_utilization
        
      conditions:
        warm_start: after 10K warmup requests
        cold_start: immediately after restart
        under_load: at 80% capacity
        
    acceptance_criteria:
      must_meet: "All p99 targets per tier"
      cold_start_allowance: "2x warm for first 100 requests"
      
  # ═══════════════════════════════════════════════════════════════════════════
  # FUZZ TESTING
  # ═══════════════════════════════════════════════════════════════════════════
  
  fuzz_testing:
    
    corpus:
      json_bombs:
        - deeply_nested (depth 100+)
        - wide_objects (10K+ keys)
        - huge_arrays (100K+ elements)
        - key_collision_attempts
        
      encoding_attacks:
        - overlong_utf8
        - invalid_utf8_sequences
        - mixed_encodings
        - bom_variations
        - charset_mismatch
        
      unicode_attacks:
        - combining_mark_sequences (100+ marks)
        - homoglyph_corpus (1000+ confusables)
        - invisible_char_injection
        - bidi_override_attacks
        - tag_characters
        
      regex_stress:
        - pathological_patterns (for non-DFA engines)
        - maximum_length_inputs
        - repetitive_patterns
        
    execution:
      frequency: nightly
      timeout_per_input: 10s
      crash_detection: enabled
      memory_leak_detection: enabled
      
  # ═══════════════════════════════════════════════════════════════════════════
  # PATTERN REGRESSION
  # ═══════════════════════════════════════════════════════════════════════════
  
  pattern_regression:
    
    benign_corpus:
      size: 100000+
      sources: [wikipedia, news, code, chat]
      
    adversarial_corpus:
      size: 10000+
      sources: [known_attacks, research, fuzzer]
      
    metrics:
      false_positive_rate:
        max_allowed: 0.001
        alert_threshold: 0.0005
        
      detection_rate:
        min_required: 0.95
        alert_threshold: 0.97
        
    execution:
      on_every_pattern_update: mandatory
      nightly_full_suite: mandatory
      
  # ═══════════════════════════════════════════════════════════════════════════
  # INTEGRATION TESTS
  # ═══════════════════════════════════════════════════════════════════════════
  
  integration:
    
    ml_callback_flows:
      - ml_returns_clean_before_timeout
      - ml_returns_suspicious_before_timeout
      - ml_times_out
      - ml_returns_error
      - ml_worker_crashes_mid_analysis
      
    eccps_integration:
      - position_map_retrieval
      - normalization_contract_compliance
      - trace_id_propagation
      
    end_to_end:
      - user_submits_clean_small_document
      - user_submits_clean_large_document
      - user_submits_malicious_document
      - user_submits_charset_mismatch
      
  # ═══════════════════════════════════════════════════════════════════════════
  # CHAOS TESTING
  # ═══════════════════════════════════════════════════════════════════════════
  
  chaos:
    
    scenarios:
      - kill_ml_worker_mid_analysis
      - network_partition_to_quarantine_store
      - disk_full_on_wal
      - pattern_db_corruption
      - kms_unavailable
      - event_bus_partition
      
    execution:
      frequency: weekly
      environment: staging
      
    verification:
      - service_recovers_within_slo
      - no_data_loss
      - no_security_bypass
      - alerts_fire_correctly
      
  # ═══════════════════════════════════════════════════════════════════════════
  # SECURITY TESTS
  # ═══════════════════════════════════════════════════════════════════════════
  
  security:
    
    pattern_db_integrity:
      - tampered_manifest_rejected
      - unsigned_patterns_rejected
      - rollback_attack_prevented
      
    key_management:
      - unauthorized_decrypt_blocked
      - key_rotation_works
      - audit_log_tamper_detected
      
    access_control:
      - role_separation_enforced
      - approval_workflow_required
```

---

## 13. Observability

```yaml
observability:

  # ═══════════════════════════════════════════════════════════════════════════
  # METRICS
  # ═══════════════════════════════════════════════════════════════════════════
  
  metrics:
    
    latency:
      - sis_processing_duration_ms (histogram, labels: tier, stage, result)
      - sis_stage_duration_ms (histogram, labels: stage)
      - sis_ml_callback_duration_ms (histogram)
      
    throughput:
      - sis_requests_total (counter, labels: tier, result)
      - sis_bytes_processed_total (counter, labels: tier)
      
    queue:
      - sis_pending_queue_size (gauge)
      - sis_pending_queue_age_ms (histogram)
      - sis_pending_queue_backpressure (counter)
      
    detection:
      - sis_detections_total (counter, labels: category, severity)
      - sis_quarantine_total (counter, labels: reason)
      - sis_false_positive_rate (gauge, computed)
      
    ml:
      - sis_ml_timeout_total (counter)
      - sis_ml_result_total (counter, labels: result)
      
    errors:
      - sis_errors_total (counter, labels: stage, error_type)
      
  # ═══════════════════════════════════════════════════════════════════════════
  # DISTRIBUTED TRACING
  # ═══════════════════════════════════════════════════════════════════════════
  
  tracing:
    propagation: W3C_trace_context
    sampling:
      default: 0.01  # 1%
      on_error: 1.0  # 100%
      on_slow: 1.0   # 100% if > p95
      
    spans:
      - sis.process_document (root)
      - sis.stage.json_validate
      - sis.stage.charset
      - sis.stage.normalize
      - sis.stage.pattern_scan
      - sis.stage.ml (async)
      - sis.quarantine.store
      
  # ═══════════════════════════════════════════════════════════════════════════
  # LOGGING
  # ═══════════════════════════════════════════════════════════════════════════
  
  logging:
    format: structured_json
    
    required_fields:
      - timestamp
      - level
      - trace_id
      - event_id
      - message
      
    pii_redaction:
      - content: NEVER_LOG
      - ip_address: HASH_AFTER_7_DAYS
      
  # ═══════════════════════════════════════════════════════════════════════════
  # DASHBOARDS
  # ═══════════════════════════════════════════════════════════════════════════
  
  dashboards:
    
    slo_dashboard:
      - latency_vs_target (by tier)
      - error_rate
      - availability
      
    security_dashboard:
      - quarantine_rate
      - detection_by_category
      - false_positive_trend
      - ml_timeout_rate
      
    operational_dashboard:
      - throughput
      - pending_queue_depth
      - resource_utilization
      - pattern_db_version
```

---

## 14. Document Control

| Field | Value |
|-------|-------|
| Document ID | sis-core-01 |
| Version | 2.0.0 |
| Status | APPROVED |
| Author | Aaron / Claude |
| Date | 2025-02-01 |
| Review Status | All critical/high items addressed |

### Related Documents

- `the-plot.md` §4 - SIS architectural context
- `FNSR-Integration-Specification-v1.0.md` §4.2 - Event contract
- `FNSR-Complete-Architecture-v2.1.md` - System architecture
- `eccps-core-01` (pending) - Downstream semantic processing

---

## Appendix A: Conformance Test Vectors

```yaml
# Sample test vectors for implementation validation

test_vectors:

  charset_detection:
    - input_hex: "EF BB BF 48 65 6C 6C 6F"
      expected_charset: utf-8
      expected_bom: true
      expected_output: "Hello"
      
    - input_hex: "48 E9 6C 6C 6F"  # "Héllo" in ISO-8859-1
      declared_charset: iso-8859-1
      expected_output_utf8: "Héllo"
      expected_transcoding: true
      
  normalization:
    - input: "café"  # With combining acute accent (e + ́)
      input_codepoints: [0x63, 0x61, 0x66, 0x65, 0x0301]
      expected_nfc: "café"
      expected_nfc_codepoints: [0x63, 0x61, 0x66, 0xE9]
      position_change: true
      
  homoglyph_detection:
    - input: "pаypal"  # Cyrillic 'а' (U+0430)
      expected_detection: true
      detection_category: HGL
      detection_position: 1
      
  json_bomb:
    - input: '{"a":{"a":{"a":...}}}' # depth 20
      expected_result: quarantine
      reason: JSON_MAX_DEPTH_EXCEEDED
```

---

*End of Specification*