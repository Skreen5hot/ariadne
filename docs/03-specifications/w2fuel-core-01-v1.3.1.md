# W2Fuel Ontological Schema Service (OSS) Specification

**Document ID:** `w2fuel-core-01`  
**Version:** 1.3.1  
**Status:** DRAFT — Pending Rust Spike Validation  
**Classification:** FNSR Core Memory/Identity Layer Component  
**Stack:** Rust (Oxigraph/Nemo) — High-Performance Implementation

---

## Version 1.3.0 Summary: Rust Stack Adoption

> **MAJOR CHANGE:** This version adopts a high-performance Rust-based implementation stack (Oxigraph for storage, Nemo for reasoning) replacing the legacy Java stack (Jena/HermiT). This change **eliminates significant defensive complexity** from v1.2.x while preserving all logical architecture, event contracts, and consumer semantics.

### What Changed from v1.2.3

| Area | v1.2.3 (Java Stack) | v1.3.0 (Rust Stack) | Impact |
|------|---------------------|---------------------|--------|
| **Storage** | Apache Jena Fuseki | Oxigraph (RocksDB) | Persistent, crash-safe, no rebuild |
| **Reasoning** | HermiT (Tableau) | Nemo (Datalog) | Sub-second classification |
| **OWL Profile** | OWL 2 DL | OWL 2 RL (with DL authoring) | Simplified, aligned with SHACL |
| **CI Model** | 3-tier (Fast/Heavy/Deferred) | Single-tier (all commits) | No L0-PENDING state |
| **Rebuild Strategy** | Ephemeral Blue/Green | Persistent with transactions | ~570 lines of spec removed |

### What Did NOT Change

- T-Box / A-Box architecture
- Event contracts (`fnsr.schema.updated`, `sequence_id`)
- Consumer semantics (TagTeam, MDRE, Fandaws behavior)
- SHACL generation and distribution
- Namespace disambiguation
- Governance and approval workflows
- RBAC and security model
- Manual SHACL cookbook

---

## 1. Executive Summary

W2Fuel is the **Terminological Box (T-Box)** service for the FNSR architecture. It manages the class definitions, property schemas, and ontological structure that give meaning to all instance data stored in Fandaws (A-Box). W2Fuel defines *what kinds of things exist*; Fandaws stores *which things exist*. MDRE joins both when reasoning.

**Core Responsibilities:**
- Store and serve BFO/CCO class hierarchies
- Manage schema evolution and versioning
- Handle namespace federation across domains
- **Generate SHACL constraints for edge validation**
- Provide schema metadata for downstream validation
- Enforce governance controls on schema modifications

**Architectural Position:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         T-BOX / A-BOX ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                     W2Fuel (This Specification)                     │   │
│   │                         Terminological Box                          │   │
│   │                      "Laws of Physics for Data"                     │   │
│   │                                                                     │   │
│   │  "What kinds of things CAN exist in this domain?"                   │   │
│   │                                                                     │   │
│   │  • Class definitions (Person, Document, Obligation, ...)            │   │
│   │  • Property schemas (has_part, participates_in, ...)                │   │
│   │  • OWL 2 RL for Rule-based reasoning (tractable)                    │   │
│   │  • SHACL for Closed World validation (what MUST be present)         │   │
│   │  • Namespace bindings (RealEstate:Lease ≠ Auto:Lease)               │   │
│   │  • BFO/CCO alignment metadata                                       │   │
│   │                                                                     │   │
│   └───────────────────────────────────────────────────────────────────┬─┘   │
│                                                                       │     │
│                                instantiates + validates               │     │
│                                                                       ▼     │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                           Fandaws                                   │   │
│   │                         Assertion Box                               │   │
│   │                                                                     │   │
│   │  "Which specific things DO exist?"                                  │   │
│   │                                                                     │   │
│   │  • Instance data (inst:Person_42, inst:Contract_789, ...)           │   │
│   │  • Asserted facts (Person_42 has_name "Alice Smith")                │   │
│   │  • Provenance chains (who asserted what, when, with what evidence)  │   │
│   │  • Taint levels (L0-L5 per fact)                                    │   │
│   │  • LOCAL SHACL validation (downloaded from W2Fuel)                  │   │
│   │                                                                     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   MDRE queries both via unified interface; joins happen at MDRE level       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Critical Design Principle:** Schema content achieves **L0 (Verified)** status after passing automated Nemo classification in CI/CD. With sub-second classification times, **every commit is fully verified** — no tiered verification, no pending states.

---

## 2. Service Identity

| Attribute | Value |
|-----------|-------|
| **Service Name** | W2Fuel Ontological Schema Service |
| **Aliases** | OSS, Ontological Schema Service, W2Fuel |
| **Layer** | Memory & Identity (FNSR §2.2) |
| **Metaphor** | Laws of Physics for Data |
| **Upstream** | Schema authors, Governance bodies |
| **Downstream** | Fandaws, MDRE, TagTeam, OERS, all reasoning services |
| **Taint Level** | L0 (Verified) — after CI/CD Nemo validation |
| **Query Paths** | Fast (cached), Standard |
| **Implementation Stack** | Rust (Oxigraph + Nemo) |

---

## 3. Ontological Foundations

### 3.1 BFO Alignment

W2Fuel maintains the **Basic Formal Ontology (BFO)** as its upper-level framework. All domain classes must align with BFO categories:

```
BFO Upper Level (maintained by W2Fuel)
══════════════════════════════════════

                           entity
                              │
              ┌───────────────┴───────────────┐
              │                               │
          continuant                      occurrent
       (exists in full                  (unfolds in
        at any moment)                     time)
              │                               │
    ┌─────────┼─────────┐           ┌────────┼────────┐
    │         │         │           │        │        │
independent dependent  spatial   process  temporal  spatiotemporal
continuant  continuant region             region      region
    │         │
  ┌─┴─┐     ┌─┴─┐
  │   │     │   │
material    quality  role  function  disposition
entity
```

### 3.2 CCO Integration

The **Common Core Ontologies (CCO)** provide intermediate abstractions between BFO and domain-specific classes:

| CCO Module | Typical Content | Example Domain Use |
|------------|-----------------|-------------------|
| Agent Ontology | Person, Organization, Role | Identity resolution |
| Artifact Ontology | Document, Instrument | Contract processing |
| Event Ontology | Act, Process, State | Workflow tracking |
| Information Entity | Information Content Entity | Knowledge graphs |
| Geospatial Ontology | Site, Region, Location | Property management |

### 3.3 Domain Ontologies

Domain-specific ontologies extend CCO for particular use cases:

```
Domain Ontology Structure
═════════════════════════

BFO (Upper)
    │
    └── CCO (Mid-level)
            │
            ├── RealEstate Ontology
            │     ├── Lease (extends cco:Agreement)
            │     ├── Property (extends cco:Facility)
            │     └── Tenant (extends cco:AgentRole)
            │
            ├── Automotive Ontology
            │     ├── Vehicle (extends cco:Artifact)
            │     ├── Financing (extends cco:Agreement)
            │     └── Dealership (extends cco:Organization)
            │
            └── Network Ontology
                  ├── NetworkDevice (extends cco:Artifact)
                  ├── IPAllocation (extends cco:InformationContentEntity)
                  └── DHCPLease (extends cco:Agreement)
```

---

## 4. Namespace Federation

### 4.1 The Disambiguation Problem

Different domains may use the same term for different concepts. W2Fuel provides **context-aware disambiguation**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      THE POLYSEMY PROBLEM: "Lease"                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   "Lease" can mean:                                                         │
│                                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                    │
│   │ RealEstate  │    │ Automotive  │    │  Network    │                    │
│   │   :Lease    │    │   :Lease    │    │   :Lease    │                    │
│   ├─────────────┤    ├─────────────┤    ├─────────────┤                    │
│   │ Rental      │    │ Financing   │    │ DHCP        │                    │
│   │ agreement   │    │ arrangement │    │ allocation  │                    │
│   └─────────────┘    └─────────────┘    └─────────────┘                    │
│         │                  │                  │                             │
│         └──────────────────┼──────────────────┘                             │
│                            │                                                │
│                            ▼                                                │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    W2Fuel Namespace Registry                        │  │
│   │                                                                     │  │
│   │  Query: resolve("Lease", context="property rental discussion")      │  │
│   │  Result: realestate:Lease (confidence: 0.94)                        │  │
│   │                                                                     │  │
│   │  Query: resolve("Lease", context="car dealership financing")        │  │
│   │  Result: auto:Lease (confidence: 0.91)                              │  │
│   │                                                                     │  │
│   │  Query: resolve("Lease", context="router configuration")            │  │
│   │  Result: network:Lease (confidence: 0.97)                           │  │
│   │                                                                     │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Namespace Registry Schema

```yaml
namespace_registry:
  - prefix: "realestate"
    iri: "https://ontology.example.org/realestate#"
    domain_keywords: ["property", "rental", "tenant", "landlord", "apartment", "housing"]
    disambiguation_hints:
      - pattern: "rent|tenant|landlord|property management"
        weight: 0.9
      - pattern: "real estate|housing|apartment"
        weight: 0.8
    
  - prefix: "auto"
    iri: "https://ontology.example.org/automotive#"
    domain_keywords: ["vehicle", "car", "financing", "dealership", "monthly payment"]
    disambiguation_hints:
      - pattern: "vehicle|car|automobile|dealership"
        weight: 0.9
      - pattern: "financing|monthly payment|trade-in"
        weight: 0.7
    
  - prefix: "network"
    iri: "https://ontology.example.org/networking#"
    domain_keywords: ["DHCP", "IP address", "router", "configuration", "network"]
    disambiguation_hints:
      - pattern: "DHCP|IP|router|network configuration"
        weight: 0.95
```

### 4.3 Disambiguation API

**Request:**
```json
{
  "@type": "w2fuel:DisambiguationRequest",
  "w2fuel:term": "Lease",
  "w2fuel:context_text": "The property management company said my lease expires next month",
  "w2fuel:context_entities": [
    {"entity": "property management company", "resolved_type": "realestate:PropertyManager"},
    {"entity": "month", "resolved_type": "bfo:BFO_0000038"}
  ]
}
```

**Response:**
```json
{
  "@type": "w2fuel:DisambiguationResponse",
  "w2fuel:term": "Lease",
  "w2fuel:resolved_class": "realestate:Lease",
  "w2fuel:confidence": 0.94,
  "w2fuel:confidence_tier": "high",
  "w2fuel:reasoning": {
    "keyword_match": 0.8,
    "entity_context": 0.95,
    "combined": 0.94
  },
  "w2fuel:matched_hints": [
    {
      "pattern": "property management",
      "namespace": "realestate",
      "weight": 0.9,
      "matched_text": "property management company"
    }
  ],
  "w2fuel:alternatives": [
    {"class": "auto:Lease", "confidence": 0.12},
    {"class": "network:Lease", "confidence": 0.02}
  ],
  "w2fuel:disambiguation_metadata": {
    "processing_time_ms": 12,
    "model_version": "disambig-v3.0",
    "resolution_path": "quick_pattern_match",
    "requires_human_review": false
  }
}
```

### 4.4 Human-in-the-Loop Disambiguation

When automated confidence is low (< 0.60), disambiguation tickets are created for human review:

```yaml
disambiguation_review:
  trigger_conditions:
    - confidence < 0.60
    - timeout > 200ms
    - multiple namespaces within 0.1 confidence
    
  ticket_creation:
    template:
      ticket_id: "DISAMB-{year}-{sequence}"
      expires_at: "{creation + 7 days}"
      status: "pending"
      
  escalation_policy:
    level_1:
      assignee: "domain-steward-pool"
      sla: "7 days"
    level_2:
      trigger: "queue_depth > 100"
      assignee: "ontology-steward"
      sla: "3 days"
    level_3:
      trigger: "queue_depth > 200"
      assignee: "governance-body"
      sla: "1 day"
```

---

## 5. Schema Storage Model

### 5.1 Persistent Storage Architecture (V1.3 — Oxigraph)

> **V1.3 CHANGE:** Replaces ephemeral Jena Fuseki with persistent Oxigraph. No rebuild cycles, no Blue/Green switching.

W2Fuel uses **Oxigraph** as its persistent triple store:

| Storage Layer | Technology | Purpose |
|---------------|------------|---------|
| **Primary T-Box** | OWL 2 RL files in Git | Authoritative ontology definitions (L0 source) |
| **Query Cache** | Redis | Fast schema lookups for cached queries |
| **Triple Store** | Oxigraph (RocksDB) | SPARQL queries, persistent and crash-safe |
| **Version Control** | Git | Schema versioning and audit trail |
| **SHACL Store** | Generated artifacts | Validation shapes for edge distribution |

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    W2Fuel STORAGE ARCHITECTURE (V1.3)                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                        Git Repository                                │  │
│   │              (Authoritative Source — L0 Source of Truth)             │  │
│   │                                                                     │  │
│   │  ontologies/                                                        │  │
│   │  ├── bfo/                                                           │  │
│   │  │   └── bfo-2020.owl          # BFO upper ontology                 │  │
│   │  ├── cco/                                                           │  │
│   │  │   ├── AgentOntology.owl     # CCO Agent module                   │  │
│   │  │   └── ...                                                        │  │
│   │  ├── domains/                                                       │  │
│   │  │   ├── realestate-v1.0.owl   # Domain ontology                    │  │
│   │  │   └── ...                                                        │  │
│   │  ├── shacl/                    # Generated SHACL shapes             │  │
│   │  └── datalog/                  # Generated Datalog rules (V1.3)     │  │
│   │                                                                     │  │
│   └───────────────────────────────┬─────────────────────────────────────┘  │
│                                   │                                        │
│                                   │ CI/CD loads on commit                  │
│                                   ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    Oxigraph (Persistent Store)                      │  │
│   │                                                                     │  │
│   │  • RocksDB backend (LSM-tree, crash-safe)                           │  │
│   │  • Atomic transactions (no global write locks)                      │  │
│   │  • Concurrent read/write without degradation                        │  │
│   │  • SPARQL 1.1 Query + Update support                                │  │
│   │  • Native Rust performance                                          │  │
│   │                                                                     │  │
│   │  Configuration:                                                     │  │
│   │  ├── data_dir: /var/lib/oxigraph/w2fuel                             │  │
│   │  ├── wal_enabled: true                                              │  │
│   │  ├── compression: lz4                                               │  │
│   │  └── max_concurrent_readers: 128                                    │  │
│   │                                                                     │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   NO EPHEMERAL REBUILDS — Oxigraph persists across restarts                 │
│   NO BLUE/GREEN — Single instance with transactional updates                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Oxigraph Configuration

```yaml
oxigraph:
  storage:
    path: "/var/lib/oxigraph/w2fuel"
    wal_enabled: true
    compression: "lz4"
    block_cache_size_mb: 512
    
  performance:
    max_concurrent_readers: 128
    write_buffer_size_mb: 64
    max_write_buffer_number: 3
    
  transactions:
    max_transaction_size_triples: 100000  # Chunk larger loads
    max_transaction_duration_seconds: 300
    backpressure_threshold_triples: 50000
    
  backup:
    strategy: "continuous"
    wal_archival: true
    snapshot_interval: "hourly"
    retention_days: 30
    
  monitoring:
    metrics_endpoint: "/metrics"
    health_endpoint: "/health"
```

### 5.3 High Availability & Disaster Recovery (V1.3.1)

> **V1.3.1 Addition:** Oxigraph is a single-process store. This section defines HA/DR strategy to maintain production availability.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OXIGRAPH HA/DR ARCHITECTURE (V1.3.1)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   PRIMARY INSTANCE (Active)                                                 │
│   ─────────────────────────                                                 │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  Oxigraph Primary                                                   │  │
│   │  • Handles all reads and writes                                     │  │
│   │  • WAL enabled, continuous archival                                 │  │
│   │  • Hourly snapshots to object storage                               │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                          │                                                  │
│                          │ WAL streaming (async)                            │
│                          ▼                                                  │
│   STANDBY INSTANCE (Warm)                                                   │
│   ────────────────────────                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  Oxigraph Standby                                                   │  │
│   │  • Receives WAL updates continuously                                │  │
│   │  • Read-only queries (optional, for load distribution)              │  │
│   │  • Promoted to primary on failover                                  │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   OBJECT STORAGE (S3/GCS)                                                   │
│   ────────────────────────                                                  │
│   • Hourly snapshots (full RocksDB backup)                                  │
│   • WAL archives (continuous)                                               │
│   • 30-day retention                                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### HA Configuration

```yaml
ha_config:
  mode: "active-standby"
  
  primary:
    instance_id: "oxigraph-primary"
    health_check_interval_seconds: 5
    failover_threshold_missed_checks: 3
    
  standby:
    instance_id: "oxigraph-standby"
    wal_replay_mode: "continuous"
    read_queries_enabled: true  # Optional load distribution
    promotion_timeout_seconds: 30
    
  failover:
    automatic: true
    trigger: "3 consecutive health check failures"
    dns_update_ttl_seconds: 30
    notification: "Slack #w2fuel-oncall + PagerDuty"
```

#### RTO/RPO Targets

| Metric | Target | Notes |
|--------|--------|-------|
| **RPO** (Recovery Point Objective) | < 1 minute | WAL streaming lag |
| **RTO** (Recovery Time Objective) | < 5 minutes | Failover + DNS propagation |
| **Snapshot RPO** | < 1 hour | For cold restore |
| **Cold Restore RTO** | < 30 minutes | From snapshot + WAL replay |

#### Backup & Restore Validation (REQUIRED)

```yaml
backup_validation:
  schedule: "weekly"
  
  drill_steps:
    1_snapshot_creation:
      action: "Create consistent snapshot of primary"
      command: "oxigraph_server backup --output s3://w2fuel-backups/$(date +%Y%m%d)"
      validation: "Snapshot size > 0, checksum recorded"
      
    2_restore_to_clean_node:
      action: "Restore snapshot to isolated test instance"
      command: "oxigraph_server restore --input s3://w2fuel-backups/{snapshot} --location /tmp/restore-test"
      validation: "Restore completes without error"
      
    3_consistency_check:
      action: "Run consistency queries"
      queries:
        - "SELECT (COUNT(*) AS ?count) WHERE { ?s ?p ?o }"
        - "SELECT (COUNT(DISTINCT ?g) AS ?graphs) WHERE { GRAPH ?g { ?s ?p ?o } }"
      validation: "Counts match primary within 0.1%"
      
    4_inference_check:
      action: "Run Nemo classification on restored data"
      validation: "No new unsatisfiable classes"
      
    5_hash_comparison:
      action: "Compare content hashes"
      command: "oxigraph_server dump | sha256sum"
      validation: "Hash matches expected (allowing for WAL lag)"
  
  reporting:
    output: "dr-drills/restore-validation-{date}.md"
    notify_on_failure: "governance-body"
```

#### Operational Runbook: Restore from Snapshot

```bash
# RUNBOOK: RB-RESTORE — Restore Oxigraph from Snapshot

# 1. Stop traffic to failed primary
kubectl scale deployment w2fuel-gateway --replicas=0

# 2. Identify latest valid snapshot
aws s3 ls s3://w2fuel-backups/ --recursive | tail -5

# 3. Restore to standby (or new instance)
oxigraph_server restore \
  --input s3://w2fuel-backups/20260202-hourly \
  --location /var/lib/oxigraph/w2fuel

# 4. Replay WAL to minimize data loss
oxigraph_server wal-replay \
  --wal-dir s3://w2fuel-wal/ \
  --location /var/lib/oxigraph/w2fuel

# 5. Verify consistency
curl http://localhost:7878/health
oxigraph_server query --query "SELECT (COUNT(*) AS ?c) WHERE { ?s ?p ?o }"

# 6. Update DNS / restore traffic
kubectl scale deployment w2fuel-gateway --replicas=3

# 7. Emit recovery event
curl -X POST http://w2fuel/admin/emit-recovery-event
```

### 5.4 Update Flow (Simplified)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SCHEMA UPDATE FLOW (V1.3.1 — With Checkpoints)           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. PR merged to main (Git authoritative)                                  │
│                                                                             │
│   2. CI/CD runs:                                                            │
│      • OWL 2 RL syntax validation                                           │
│      • Nemo classification (< 1 second)                                     │
│      • Inference parity check (V1.3.1)                                      │
│      • BFO/CCO compliance check                                             │
│      • SHACL generation                                                     │
│      • Datalog rule generation                                              │
│                                                                             │
│   3. On CI pass — Oxigraph transaction:                                     │
│      • Begin transaction                                                    │
│      • Clear affected graphs                                                │
│      • Load new ontology data (chunked if > 50k triples)                    │
│      • COMMIT TRANSACTION ─────────────────────────────┐                    │
│                                                        │                    │
│   4. Post-commit (only after successful commit):       │                    │
│      • Redis cache invalidation                        │ CHECKPOINT         │
│      • Verify cache cleared                            │                    │
│                                                        │                    │
│   5. Event emission (only after cache invalidation):   │                    │
│      • fnsr.schema.updated with sequence_id ───────────┘                    │
│      • Broker ack received                                                  │
│                                                                             │
│   CRITICAL: Event is emitted ONLY after commit + cache invalidation         │
│                                                                             │
│   Total time: < 30 seconds (vs. 5+ minutes with Jena Blue/Green)            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Transaction Size Limits

```yaml
transaction_limits:
  max_triples_per_transaction: 100000
  
  chunking_strategy:
    threshold: 50000  # Chunk if load exceeds this
    chunk_size: 25000
    inter_chunk_delay_ms: 100
    
  backpressure:
    queue_depth_warning: 10
    queue_depth_critical: 50
    action_on_critical: "Defer non-critical updates"
```

---

## 6. OWL Profile: OWL 2 RL

### 6.1 Profile Selection Rationale

> **V1.3 CHANGE:** W2Fuel adopts **OWL 2 RL** as the primary profile, replacing OWL 2 DL.

| Profile | Complexity | Reasoning | W2Fuel Use |
|---------|------------|-----------|------------|
| OWL 2 Full | Undecidable | No | ❌ |
| OWL 2 DL | NExpTime | Tableau (HermiT) | ❌ Removed |
| **OWL 2 RL** | **Polynomial** | **Datalog (Nemo)** | **✅ Adopted** |
| OWL 2 EL | Polynomial | Completion | ❌ Too limited |
| OWL 2 QL | Polynomial | Query rewriting | ❌ Wrong focus |

**Why OWL 2 RL:**
- Polynomial-time reasoning (tractable at scale)
- Aligns with SHACL's Closed World semantics
- Supports rule-based inference (Datalog materialization)
- Covers 95%+ of real-world ontology patterns

### 6.2 OWL 2 RL Supported Constructs

| Construct | OWL 2 RL Support | Notes |
|-----------|------------------|-------|
| `rdfs:subClassOf` | ✅ Full | Core hierarchy |
| `rdfs:subPropertyOf` | ✅ Full | Property hierarchy |
| `owl:equivalentClass` | ✅ Full | Class equivalence |
| `owl:disjointWith` | ✅ Full | Disjointness |
| `owl:allValuesFrom` | ✅ Full | Universal restrictions |
| `owl:hasValue` | ✅ Full | Value restrictions |
| `owl:maxCardinality 0/1` | ✅ Full | Limited cardinality |
| `owl:someValuesFrom` | ⚠️ Superclass only | RL restriction |
| `owl:unionOf` | ⚠️ Superclass only | RL restriction |
| `owl:cardinality > 1` | ❌ Not supported | Use SHACL instead |
| `owl:complementOf` | ❌ Not supported | Use SHACL instead |

### 6.3 Authoring in OWL 2 DL, Deploying as OWL 2 RL

For ontology authors who need full expressivity during development:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OWL 2 DL → OWL 2 RL TRANSPILATION                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   AUTHORING (local development):                                            │
│   ─────────────────────────────────                                         │
│   • Write ontology in OWL 2 DL                                              │
│   • Use Protégé with HermiT for design-time reasoning                       │
│   • Full expressivity available                                             │
│                                                                             │
│   CI/CD (transpilation):                                                    │
│   ────────────────────────                                                  │
│   • Validate OWL 2 RL compatibility                                         │
│   • Flag non-RL constructs                                                  │
│   • Generate SHACL for constructs that need CWA validation                  │
│   • Generate Datalog rules for Nemo                                         │
│                                                                             │
│   DEPLOYMENT (production):                                                  │
│   ─────────────────────────                                                 │
│   • OWL 2 RL in Oxigraph (for queries)                                      │
│   • Datalog rules in Nemo (for inference)                                   │
│   • SHACL shapes at edge (for validation)                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.4 Non-RL Construct Handling

When an ontology contains constructs outside OWL 2 RL:

| Construct | CI Behavior | Alternative |
|-----------|-------------|-------------|
| `owl:someValuesFrom` in subclass | **WARN** | Move to SHACL `sh:qualifiedMinCount` |
| `owl:cardinality > 1` | **WARN** | Use SHACL `sh:minCount`/`sh:maxCount` |
| `owl:complementOf` | **FAIL** unless manual SHACL | Manual `sh:not` in shacl-manual/ |
| `owl:unionOf` in subclass | **WARN** | Move to SHACL `sh:or` |

---

## 7. Reasoning Engine: Nemo

### 7.1 Nemo Overview

> **V1.3 CHANGE:** Replaces HermiT with Nemo for all classification tasks.

**Nemo** is a high-performance Datalog engine written in Rust:

| Feature | HermiT (v1.2.x) | Nemo (v1.3) |
|---------|-----------------|-------------|
| Algorithm | Hypertableau | Datalog materialization |
| Complexity | NExpTime | Polynomial |
| Performance | Minutes for large ontologies | Sub-second |
| Memory | High (tableau caching) | Low (streaming) |
| Parallelism | Single-threaded | SIMD-optimized |
| Language | Java | Rust |

### 7.2 Datalog Rule Generation

W2Fuel generates Datalog rules from OWL 2 RL axioms:

**OWL Input:**
```turtle
ex:Employee rdfs:subClassOf ex:Person .
ex:Manager rdfs:subClassOf ex:Employee .
ex:worksFor rdfs:domain ex:Employee .
ex:worksFor rdfs:range ex:Organization .
```

**Generated Datalog:**
```datalog
% Subclass inference
Person(?x) :- Employee(?x) .
Employee(?x) :- Manager(?x) .

% Domain inference
Employee(?x) :- worksFor(?x, ?y) .

% Range inference
Organization(?y) :- worksFor(?x, ?y) .
```

### 7.3 Golden-Rule Translation Tests (V1.3.1)

> **V1.3.1 Addition:** Unit tests validating OWL→Datalog translation correctness.

```yaml
golden_rule_tests:
  description: "Canonical OWL axioms → expected Datalog rules"
  
  test_cases:
    - name: "subclass_simple"
      owl: "ex:Dog rdfs:subClassOf ex:Animal ."
      expected_datalog: "Animal(?x) :- Dog(?x) ."
      
    - name: "subclass_chain"
      owl: |
        ex:Poodle rdfs:subClassOf ex:Dog .
        ex:Dog rdfs:subClassOf ex:Animal .
      expected_datalog: |
        Dog(?x) :- Poodle(?x) .
        Animal(?x) :- Dog(?x) .
      expected_inference: "Poodle(?x) → Animal(?x) via transitivity"
      
    - name: "domain_inference"
      owl: "ex:owns rdfs:domain ex:Person ."
      expected_datalog: "Person(?x) :- owns(?x, ?y) ."
      
    - name: "range_inference"
      owl: "ex:owns rdfs:range ex:Asset ."
      expected_datalog: "Asset(?y) :- owns(?x, ?y) ."
      
    - name: "equivalent_class"
      owl: "ex:Human owl:equivalentClass ex:Person ."
      expected_datalog: |
        Person(?x) :- Human(?x) .
        Human(?x) :- Person(?x) .
      
    - name: "all_values_from"
      owl: |
        ex:VeganRestaurant rdfs:subClassOf [
          a owl:Restriction ;
          owl:onProperty ex:servesFood ;
          owl:allValuesFrom ex:VeganFood
        ] .
      expected_datalog: "VeganFood(?y) :- VeganRestaurant(?x), servesFood(?x, ?y) ."
      
    - name: "has_value"
      owl: |
        ex:USCitizen rdfs:subClassOf [
          a owl:Restriction ;
          owl:onProperty ex:nationality ;
          owl:hasValue ex:USA
        ] .
      expected_datalog: "nationality(?x, ex:USA) :- USCitizen(?x) ."
      
    - name: "functional_property"
      owl: "ex:hasMother a owl:FunctionalProperty ."
      expected_datalog: "sameAs(?y1, ?y2) :- hasMother(?x, ?y1), hasMother(?x, ?y2) ."
      
    - name: "inverse_property"
      owl: "ex:hasChild owl:inverseOf ex:hasParent ."
      expected_datalog: |
        hasParent(?y, ?x) :- hasChild(?x, ?y) .
        hasChild(?x, ?y) :- hasParent(?y, ?x) .
      
    - name: "transitive_property"
      owl: "ex:ancestorOf a owl:TransitiveProperty ."
      expected_datalog: "ancestorOf(?x, ?z) :- ancestorOf(?x, ?y), ancestorOf(?y, ?z) ."
      
  round_trip_tests:
    description: "Apply generated Datalog to sample data, verify inferred triples"
    
    - name: "subclass_materialization"
      input_data: "ex:fido a ex:Dog ."
      rules: "Animal(?x) :- Dog(?x) ."
      expected_inferred: "ex:fido a ex:Animal ."
      
    - name: "domain_materialization"
      input_data: "ex:john ex:owns ex:car123 ."
      rules: "Person(?x) :- owns(?x, ?y) ."
      expected_inferred: "ex:john a ex:Person ."
      
    - name: "transitive_materialization"
      input_data: |
        ex:alice ex:ancestorOf ex:bob .
        ex:bob ex:ancestorOf ex:charlie .
      rules: "ancestorOf(?x, ?z) :- ancestorOf(?x, ?y), ancestorOf(?y, ?z) ."
      expected_inferred: "ex:alice ex:ancestorOf ex:charlie ."
```

### 7.4 Inference Parity Testing (V1.3.1)

> **V1.3.1 REQUIRED:** Validate that critical inferences are preserved when moving from HermiT to Nemo.

```yaml
inference_parity_testing:
  purpose: "Ensure Nemo+SHACL produces equivalent results to HermiT for consumer-visible inferences"
  
  test_corpus:
    - ontology: "bfo-2020.owl"
      critical_inferences:
        - "Every Continuant is an Entity"
        - "Every Occurrent is an Entity"
        - "Continuant and Occurrent are disjoint"
        
    - ontology: "cco-agent.owl"
      critical_inferences:
        - "Person subClassOf Agent"
        - "Organization subClassOf Agent"
        
    - ontology: "realestate-v1.0.owl"
      critical_inferences:
        - "Lease subClassOf Agreement"
        - "Tenant subClassOf AgentRole"
        - "Property has exactly one address"
        
  test_procedure:
    1_run_hermit:
      action: "Classify ontology with HermiT (one-time, cached)"
      output: "hermit-inferences/{ontology}.nt"
      
    2_run_nemo:
      action: "Classify ontology with Nemo"
      output: "nemo-inferences/{ontology}.nt"
      
    3_compare_class_hierarchy:
      action: "Compare rdfs:subClassOf closures"
      query: |
        SELECT ?sub ?super WHERE {
          ?sub rdfs:subClassOf+ ?super .
          FILTER(?sub != ?super)
        }
      validation: "Nemo hierarchy ⊇ HermiT hierarchy for RL-expressible axioms"
      
    4_compare_property_hierarchy:
      action: "Compare rdfs:subPropertyOf closures"
      validation: "Nemo hierarchy = HermiT hierarchy"
      
    5_check_critical_inferences:
      action: "Verify each critical inference is present in Nemo output"
      on_missing:
        - "If expressible in RL: BUG — fix Datalog generator"
        - "If not expressible in RL: Document as 'moved to SHACL'"
        
    6_shacl_coverage:
      action: "For inferences moved to SHACL, verify SHACL shape exists"
      validation: "Every non-RL inference has corresponding SHACL constraint"
  
  ci_integration:
    trigger: "Every PR modifying ontologies/"
    timeout: "120s"  # HermiT comparison is slower but only runs on changes
    failure_action: "Block merge"
    
  reporting:
    output: "inference-parity-report.md"
    sections:
      - "Hierarchy comparison"
      - "Critical inference status"
      - "Non-RL constructs moved to SHACL"
      - "Discrepancies requiring review"
```

### 7.5 Classification Performance

| Ontology Size | HermiT (v1.2.x) | Nemo (v1.3) | Speedup |
|---------------|-----------------|-------------|---------|
| Small (<500 axioms) | 5-30s | <100ms | 50-300x |
| Medium (500-5000) | 30-120s | 100-500ms | 60-240x |
| Large (5000-50000) | 2-10 min | 500ms-2s | 120-300x |
| Very Large (>50000) | 10+ min or timeout | 2-5s | 120x+ |

### 7.6 CI/CD Integration

With sub-second classification, **every commit is fully verified**:

```yaml
ci_pipeline:
  # NO TIERED VERIFICATION — single fast pipeline
  
  stages:
    - name: "syntax"
      timeout: "30s"
      checks:
        - "OWL 2 RL well-formed"
        - "Non-RL construct detection"
        
    - name: "reasoning"
      timeout: "30s"  # Was 5-30 minutes with HermiT
      checks:
        - "Nemo classification"
        - "Golden-rule translation tests (V1.3.1)"
        - "Consistency check"
        - "Unsatisfiable class detection"
        
    - name: "inference_parity"
      timeout: "120s"  # Includes HermiT comparison
      checks:
        - "Inference parity test (V1.3.1)"
        - "Critical inference verification"
        - "Non-RL → SHACL coverage check"
        
    - name: "compliance"
      timeout: "30s"
      checks:
        - "BFO anchor verification"
        - "CCO alignment"
        - "Annotation completeness"
        
    - name: "shacl"
      timeout: "30s"
      checks:
        - "SHACL generation"
        - "Manual SHACL validation"
        - "Test vector verification"
        
    - name: "datalog"
      timeout: "30s"
      checks:
        - "Datalog rule generation"
        - "Rule consistency check"
        
    - name: "deploy"
      timeout: "60s"
      checks:
        - "Oxigraph transaction load"
        - "Cache invalidation"
        - "Event emission (checkpoint)"
  
  total_pipeline_time: "< 3 minutes"  # Was potentially hours with HermiT
```

---

## 8. SHACL Constraint Generation

### 8.1 Dual Semantics (Preserved from v1.2.x)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    OWL + SHACL DUAL SEMANTICS (V1.3)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   OWL 2 RL (Open World)             SHACL (Closed World)                    │
│   ═══════════════════════           ═══════════════════════                 │
│                                                                             │
│   "What COULD be true?"             "What MUST be present?"                 │
│                                                                             │
│   • Inference rules                 • Validation rules                      │
│   • If data missing → unknown       • If data missing → violation           │
│   • Used by: MDRE, Nemo             • Used by: Fandaws, TagTeam             │
│                                                                             │
│   With OWL 2 RL, the semantics are MORE ALIGNED:                            │
│   • RL rules produce deterministic inferences                               │
│   • SHACL validates those inferences                                        │
│   • No "what could theoretically exist" uncertainty                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 OWL 2 RL → SHACL Mapping

| OWL 2 RL Construct | SHACL Output | Semantic Notes |
|--------------------|--------------|----------------|
| `rdfs:subClassOf` | `sh:targetClass` on superclass | Target inheritance |
| `rdfs:range` (class) | `sh:class` | Type constraint |
| `rdfs:range` (datatype) | `sh:datatype` | Datatype constraint |
| `owl:allValuesFrom C` | `sh:class C` on property | All values must be C |
| `owl:hasValue v` | `sh:hasValue v` | Exact value |
| `owl:maxCardinality 1` | `sh:maxCount 1` | At most one |
| `owl:FunctionalProperty` | `sh:maxCount 1` | Functional = max 1 |

### 8.3 Non-RL Constructs in SHACL

Constructs outside OWL 2 RL are handled by SHACL directly:

| Need | OWL 2 DL | OWL 2 RL | SHACL Alternative |
|------|----------|----------|-------------------|
| "At least one" | `owl:someValuesFrom` | ❌ | `sh:minCount 1` |
| "Exactly N" | `owl:cardinality N` | ❌ | `sh:minCount N` + `sh:maxCount N` |
| "Not a" | `owl:complementOf` | ❌ | `sh:not` |
| "A or B" | `owl:unionOf` | ⚠️ Limited | `sh:or` |

### 8.4 Signed SHACL Bundles

```http
GET /shacl/realestate/v1.0 HTTP/1.1

HTTP/1.1 200 OK
Content-Type: text/turtle
W2Fuel-Bundle-Signature: ed25519:abc123def456...
W2Fuel-Signed-By: key:ed25519:w2fuel-signing-key-2026
W2Fuel-Signature-Timestamp: 2026-02-01T15:30:00Z
W2Fuel-Schema-Version: realestate-v1.0.3
X-W2Fuel-Verification: verified
```

Downstream services **MUST** verify signatures before using SHACL shapes.

---

## 9. Event Contract

### 9.1 Canonical Final Checkpoint Event (V1.3.1 — NORMATIVE)

> **V1.3.1 NORMATIVE:** This is the single "all done" event. It is emitted **ONLY AFTER**:
> 1. Oxigraph transaction commits successfully
> 2. Redis cache invalidation completes
> 3. Health check confirms Oxigraph is serving new data

```json
{
  "@type": "fnsr:SchemaUpdatedEvent",
  "@context": "https://fnsr.spec/v2/events",
  
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-02-01T15:30:00Z",
  
  "sequence_id": 42,
  
  "update_type": "minor",
  "breaking": false,
  "affected_namespaces": ["realestate"],
  
  "version_info": {
    "previous_version": "1.0.0",
    "new_version": "1.1.0",
    "git_commit": "abc123def456"
  },
  
  "verification_status": "verified",
  
  "infrastructure_state": {
    "oxigraph_transaction_committed": true,
    "oxigraph_health_check_passed": true,
    "cache_invalidation_completed": true,
    "cache_invalidation_timestamp": "2026-02-01T15:29:58Z"
  },
  
  "shacl_state": {
    "shacl_bundle_hash": "sha256:a1b2c3d4e5f6789...",
    "shacl_hash_verified": true
  },
  
  "ci_verification": {
    "nemo_classification_passed": true,
    "inference_parity_passed": true,
    "golden_rule_tests_passed": true,
    "compliance_passed": true,
    "shacl_generated": true,
    "pipeline_run_id": "ci-run-12345"
  }
}
```

#### Event Emission Preconditions (NORMATIVE)

```yaml
event_emission_preconditions:
  # ALL must be true before emitting fnsr.schema.updated
  
  required_checkpoints:
    - name: "oxigraph_committed"
      description: "Oxigraph transaction committed successfully"
      verification: "Transaction returns success, no rollback"
      
    - name: "oxigraph_health"
      description: "Oxigraph health check passes"
      verification: "GET /health returns 200, query returns expected count"
      
    - name: "cache_invalidated"
      description: "Redis cache keys deleted"
      verification: "KEYS class:{namespace}:* returns empty"
      
  emission_order:
    1: "Verify all preconditions"
    2: "Construct event with all required fields"
    3: "Publish to Kafka"
    4: "Wait for broker ack (timeout: 5s)"
    5: "Log emission with sequence_id"
    
  failure_behavior:
    precondition_failed:
      action: "DO NOT emit event"
      recovery: "Rollback transaction, alert operator"
      
    kafka_publish_failed:
      action: "Retry with exponential backoff"
      max_retries: 3
      initial_delay_ms: 100
      max_delay_ms: 5000
      on_exhaustion: "Alert operator, system inconsistent"
```

#### Idempotent Event Handler (V1.3.1)

```python
# Reference implementation for downstream consumers

class SchemaEventHandler:
    def __init__(self, redis_client, consistency_url):
        self.redis = redis_client
        self.consistency_url = consistency_url
        self.last_seq_key = "w2fuel:last_processed_sequence_id"
        self.processed_prefix = "w2fuel:processed_event:"
        
    def handle_event(self, event: dict) -> bool:
        """Handle fnsr.schema.updated idempotently."""
        event_id = event["event_id"]
        sequence_id = event["sequence_id"]
        
        # R1: Check duplicate by event_id (1-hour window)
        if self.redis.exists(f"{self.processed_prefix}{event_id}"):
            return False  # Duplicate
        
        # Get last processed
        last_seq = int(self.redis.get(self.last_seq_key) or 0)
        
        # R1: Old event
        if sequence_id <= last_seq:
            return False
        
        # R3: Gap detection
        gap = sequence_id - last_seq
        if gap > 1:
            self._handle_gap(gap)
        
        # R4: Store before processing
        self.redis.set(self.last_seq_key, sequence_id)
        self.redis.setex(f"{self.processed_prefix}{event_id}", 3600, "1")
        
        # Process
        self._apply_schema_update(event)
        return True
    
    def _handle_gap(self, gap: int):
        if gap <= 10:
            log.warning(f"Small event gap: {gap}")
        elif gap <= 100:
            log.error(f"Medium event gap: {gap}")
            self._request_consistency_check()
        else:
            log.critical(f"Large event gap: {gap}")
            self._alert_operator()
    
    def sync_on_startup(self):
        """R5: Sync on restart."""
        resp = requests.get(self.consistency_url)
        if resp.json()["status"] == "consistent":
            self.redis.set(self.last_seq_key, resp.json()["sequence_id"])
```

### 9.2 Simplified Verification Status (V1.3)

> **V1.3 CHANGE:** No more "pending" state — every commit is fully verified before merge.

| Status | Meaning | When |
|--------|---------|------|
| `verified` | Full Nemo classification passed | Normal operation |
| `lite` | Syntax-only (Nemo disabled for this namespace) | Exceptional cases only |
| `inconsistent` | System error | Never in normal operation |

**No `pending` status** — sub-second Nemo classification means we don't need async verification.

### 9.3 Consumer Semantics (Simplified)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 CONSUMER BEHAVIOR BY STATUS (V1.3 — Simplified)             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   STATUS: "verified" (Normal)                                               │
│   ────────────────────────────                                              │
│   Header: X-W2Fuel-Verification: verified                                   │
│                                                                             │
│   • TagTeam: Extract entities normally                                      │
│   • MDRE: Load schema, generate inferences via Nemo                         │
│   • Fandaws: Validate with SHACL, reject non-conformant                     │
│   • All: Cache normally (1 hour TTL)                                        │
│                                                                             │
│   STATUS: "lite" (Rare — Nemo disabled)                                     │
│   ─────────────────────────────────────                                     │
│   Header: X-W2Fuel-Verification: lite                                       │
│                                                                             │
│   • TagTeam: Extract normally                                               │
│   • MDRE: Load schema, NO Nemo inference (explicit axioms only)             │
│   • Fandaws: Validate with SHACL normally                                   │
│   • All: Log lite usage for audit                                           │
│                                                                             │
│   NO "pending" STATUS — all commits are fully verified before merge         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.4 Idempotent Event Handling (Preserved)

The idempotency rules from v1.2.x are **unchanged**:

```yaml
idempotency:
  mechanism: sequence_id
  
  normative_rules:
    R1: "If sequence_id <= last_processed: IGNORE (duplicate)"
    R2: "If sequence_id == last_processed + 1: PROCESS normally"
    R3: "If sequence_id > last_processed + 1: PROCESS but log gap warning"
    R4: "Store last_processed_sequence_id durably before processing"
    R5: "On restart, query /admin/consistency-check to sync"
```

---

## 10. REST API

### 10.1 Base URL

```
https://w2fuel.fnsr.org/v1
```

### 10.2 Core Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/class/{prefix}:{localname}` | Class definition |
| GET | `/property/{prefix}:{localname}` | Property definition |
| GET | `/hierarchy/{prefix}:{localname}` | Class hierarchy |
| POST | `/namespace/resolve` | Disambiguation |
| GET | `/shacl/{namespace}/{version}` | SHACL shapes |
| GET | `/datalog/{namespace}/{version}` | Datalog rules (V1.3) |
| POST | `/sparql` | SPARQL queries |
| GET | `/health` | Health check |
| GET | `/admin/consistency-check` | Consistency verification |

### 10.3 Response Headers

All responses include:

```http
X-W2Fuel-Verification: verified
X-W2Fuel-Schema-Version: realestate-v1.1.0
X-W2Fuel-Sequence-Id: 42
X-W2Fuel-Cache: HIT|MISS|BYPASS
```

### 10.4 New Endpoint: Datalog Rules (V1.3)

```http
GET /datalog/realestate/v1.0 HTTP/1.1
Accept: text/plain

HTTP/1.1 200 OK
Content-Type: text/plain
W2Fuel-Datalog-Hash: sha256:def789...

% Datalog rules for realestate v1.0
% Generated by W2Fuel CI at 2026-02-01T15:30:00Z

Property(?x) :- ResidentialProperty(?x) .
Property(?x) :- CommercialProperty(?x) .
Agreement(?x) :- Lease(?x) .
...
```

---

## 11. CI/CD Pipeline (Simplified)

### 11.1 Single-Tier Verification

> **V1.3 CHANGE:** No more tiered verification. Every commit runs full pipeline.

```yaml
ci_pipeline:
  name: "W2Fuel Schema Verification"
  trigger: "Pull Request and Push to main"
  
  total_timeout: "5 minutes"  # Was potentially hours
  
  stages:
    syntax_validation:
      timeout: "30s"
      steps:
        - "Parse OWL 2 RL syntax"
        - "Detect non-RL constructs (warn or fail)"
        - "Validate imports"
      
    nemo_classification:
      timeout: "30s"
      steps:
        - "Generate Datalog rules from OWL"
        - "Run Nemo materialization"
        - "Check for inconsistencies"
        - "Verify no unsatisfiable classes"
      resources:
        memory: "2GB"  # Was 16-32GB for HermiT
        cpu: "2 cores"
      
    compliance_check:
      timeout: "30s"
      steps:
        - "Verify BFO anchoring"
        - "Check CCO alignment"
        - "Validate annotations"
      
    shacl_generation:
      timeout: "30s"
      steps:
        - "Generate SHACL from OWL 2 RL"
        - "Merge with manual SHACL"
        - "Run test vectors"
        - "Sign bundle"
      
    deployment:
      timeout: "60s"
      steps:
        - "Begin Oxigraph transaction"
        - "Load new ontology"
        - "Commit transaction"
        - "Invalidate Redis cache"
        - "Emit fnsr.schema.updated"
```

### 11.2 No More Complexity Grading

| v1.2.x | v1.3 |
|--------|------|
| Small: 60s timeout | All: 30s timeout |
| Medium: 180s timeout | All: 30s timeout |
| Large: 600s timeout, dedicated worker | All: 30s timeout |
| Very Large: 1800s timeout, opt-in | All: 30s timeout |

### 11.3 No More L0-PENDING

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VERIFICATION STATE MACHINE (V1.3 — Simplified)           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                              ┌─────────────┐                                │
│                              │   INITIAL   │                                │
│                              │ (no schema) │                                │
│                              └──────┬──────┘                                │
│                                     │                                       │
│                                     │ PR merged + CI passes (< 5 min)       │
│                                     ▼                                       │
│                            ┌──────────────┐                                 │
│                            │  L0 VERIFIED │                                 │
│                            │              │                                 │
│                            │ Nemo passed  │                                 │
│                            │ SHACL signed │                                 │
│                            │ Event emitted│                                 │
│                            └──────────────┘                                 │
│                                                                             │
│   NO L0-PENDING — sub-second Nemo means every commit is verified inline     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 12. Governance

### 12.1 Schema Change Types (Preserved)

| Change Type | Examples | Approval | CI |
|-------------|----------|----------|-----|
| PATCH | Typo fix, comment update | Auto | Required |
| MINOR | New class, new property | Domain Steward | Required |
| MAJOR | Breaking change, removal | Governance Body | Required |

### 12.2 Bridge Ontologies (Preserved)

Version migration bridges are unchanged from v1.2.x:

```turtle
# Bridge: realestate-v1-to-v2
realestate-v1:RentalProperty owl:equivalentClass realestate-v2:ResidentialLease .
realestate-v1:monthlyRent owl:equivalentProperty realestate-v2:rentAmount .
```

### 12.3 RBAC (Preserved)

| Role | Permissions |
|------|-------------|
| anonymous | Health check only |
| authenticated_service | Read, query, SHACL download |
| schema_author | Submit PRs |
| domain_steward | Approve MINOR changes |
| ontology_steward | Cross-namespace changes |
| operator | Admin endpoints |
| governance_body | All permissions |

---

## 13. Security (Preserved)

### 13.1 Authentication

OAuth 2.0 + JWT (RS256), unchanged from v1.2.x.

### 13.2 SHACL Signature Verification

Ed25519 signatures, unchanged from v1.2.x. **Verification is REQUIRED.**

### 13.3 Secrets Management

HashiCorp Vault integration, unchanged from v1.2.x.

---

## 14. Monitoring

### 14.1 Key Metrics (Updated for Nemo)

| Metric | SLO | Alert |
|--------|-----|-------|
| `w2fuel_nemo_classification_seconds` | P99 < 1s | P99 > 2s |
| `w2fuel_oxigraph_query_seconds` | P99 < 100ms | P99 > 500ms |
| `w2fuel_oxigraph_transaction_seconds` | P99 < 5s | P99 > 10s |
| `w2fuel_ci_pipeline_seconds` | P99 < 180s | P99 > 300s |
| `w2fuel_shacl_download_seconds` | P99 < 50ms | P99 > 200ms |

### 14.2 Sentinel Metrics (V1.3.1 — Preserved)

> **V1.3.1 Addition:** Keep these anomaly-detection metrics even though Nemo is fast.

| Metric | Purpose | Alert |
|--------|---------|-------|
| `w2fuel_event_gap_seconds` | Detect missed events | Gap > 60s |
| `w2fuel_nemo_run_failure_count` | CI anomaly detection | > 0 in 1 hour |
| `w2fuel_schema_commit_duration_seconds` | Detect unexpected slowdowns | P99 > 30s |
| `w2fuel_oxigraph_wal_lag_seconds` | HA standby health | > 60s |
| `w2fuel_inference_parity_failures` | Semantic drift detection | > 0 |

### 14.3 Removed Metrics

The following metrics from v1.2.x are **removed** (no longer applicable):

- `w2fuel_fuseki_rebuild_duration_seconds` — No rebuilds
- `w2fuel_l0_pending_duration_hours` — No pending state
- `w2fuel_reasoner_timeout_rate` — Nemo doesn't timeout (but we keep failure count)

---

## 15. Migration Guide: v1.2.x → v1.3

### 15.1 What Consumers Must Change

**Nothing.** The API contract and event schema are unchanged. Consumers can upgrade W2Fuel without code changes.

### 15.2 What Operators Must Change

| Component | v1.2.x | v1.3 | Migration |
|-----------|--------|------|-----------|
| Triple Store | Jena Fuseki | Oxigraph | Full data migration |
| Reasoner | HermiT | Nemo | No migration (CI replacement) |
| OWL Profile | OWL 2 DL | OWL 2 RL | Ontology audit + transpilation |
| CI Pipeline | Tiered | Single | Pipeline replacement |

### 15.3 SPARQL Compatibility Testing (V1.3.1)

> **V1.3.1 Addition:** Validate SPARQL semantics are preserved during migration.

```yaml
sparql_compatibility_tests:
  purpose: "Ensure queries produce identical results in Fuseki and Oxigraph"
  
  test_categories:
    basic_queries:
      - "SELECT * WHERE { ?s ?p ?o } LIMIT 100"
      - "SELECT (COUNT(*) AS ?c) WHERE { ?s ?p ?o }"
      - "SELECT DISTINCT ?type WHERE { ?s a ?type }"
      
    named_graphs:
      - "SELECT ?g (COUNT(*) AS ?c) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g"
      - "SELECT * WHERE { GRAPH <http://example.org/realestate> { ?s ?p ?o } }"
      
    hierarchy_queries:
      - "SELECT ?sub ?super WHERE { ?sub rdfs:subClassOf+ ?super }"
      - "SELECT ?class WHERE { ?class rdfs:subClassOf bfo:BFO_0000001 }"
      
    property_queries:
      - "SELECT ?prop ?domain WHERE { ?prop rdfs:domain ?domain }"
      - "SELECT ?prop ?range WHERE { ?prop rdfs:range ?range }"
      
    blank_nodes:
      - "SELECT * WHERE { ?s ?p [ ?p2 ?o2 ] }"
      - "CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o . FILTER(isBlank(?s) || isBlank(?o)) }"
  
  validation:
    result_comparison: "Sort and compare result sets"
    count_tolerance: "0 (exact match required)"
    blank_node_handling: "Compare structure, not IDs"
    
  known_differences:
    - issue: "Default graph semantics"
      fuseki: "Union of all graphs by default"
      oxigraph: "Empty default graph"
      mitigation: "Explicitly specify GRAPH or use FROM"
      
    - issue: "Blank node serialization"
      fuseki: "_:b0, _:b1, ..."
      oxigraph: "_:riog1, _:riog2, ..."
      mitigation: "Compare by structure, not by ID"
```

### 15.4 Ontology Migration

1. **Audit**: Run `w2fuel-rl-check` on all ontologies to identify non-RL constructs
2. **Transpile**: Generate SHACL for constructs that need CWA validation
3. **Validate**: Run Nemo classification on transpiled ontologies
4. **Deploy**: Load into Oxigraph

### 15.5 Data Migration (Fuseki → Oxigraph)

```bash
# Export from Fuseki
curl "http://fuseki:3030/w2fuel/data" -H "Accept: application/n-quads" > w2fuel.nq

# Import to Oxigraph
oxigraph_server load --file w2fuel.nq --location /var/lib/oxigraph/w2fuel
```

---

## 16. Appendices

### Appendix A: Rust Stack Validation Results (V1.3.1 — REQUIRED)

> **V1.3.1 REQUIRED:** This appendix MUST be populated before governance sign-off.

```yaml
rust_spike_results:
  # STORAGE BENCHMARK
  storage_benchmark:
    test_datasets:
      - name: "bfo-2020"
        triples: "~2,000"
      - name: "cco-full"
        triples: "~15,000"
      - name: "realestate-v1.0"
        triples: "~5,000"
      - name: "combined-production"
        triples: "~50,000"
    
    jena_fuseki:
      load_time_seconds: "TBD"
      cold_query_p99_ms: "TBD"
      warm_query_p99_ms: "TBD"
      memory_usage_mb: "TBD"
      
    oxigraph:
      load_time_seconds: "TBD"
      cold_query_p99_ms: "TBD"
      warm_query_p99_ms: "TBD"
      memory_usage_mb: "TBD"
      
    comparison:
      load_speedup: "TBD"
      query_speedup: "TBD"
      memory_reduction: "TBD"
      
  # REASONING BENCHMARK
  reasoning_benchmark:
    test_ontologies:
      - name: "realestate-v1.0"
        axioms: "~1,200"
      - name: "automotive-v1.0"
        axioms: "~3,500"
      - name: "combined-domains"
        axioms: "~25,000"
    
    hermit:
      classification_time_seconds: "TBD"
      memory_peak_mb: "TBD"
      timeout_rate: "TBD"
      
    nemo:
      classification_time_seconds: "TBD"
      memory_peak_mb: "TBD"
      datalog_rules_generated: "TBD"
      
    comparison:
      speedup: "TBD"
      memory_reduction: "TBD"
      
  # EXPRESSIVITY AUDIT
  expressivity_audit:
    total_owl_files: "TBD"
    total_axioms: "TBD"
    
    rl_compliant:
      axiom_count: "TBD"
      percentage: "TBD"
      
    non_rl_constructs:
      someValuesFrom_count: "TBD"
      cardinality_gt_1_count: "TBD"
      complementOf_count: "TBD"
      unionOf_subclass_count: "TBD"
      other_count: "TBD"
      
    shacl_coverage:
      constructs_with_shacl: "TBD"
      constructs_needing_manual_shacl: "TBD"
      
  # INFERENCE PARITY
  inference_parity:
    critical_inferences_tested: "TBD"
    inferences_preserved: "TBD"
    inferences_moved_to_shacl: "TBD"
    inferences_lost: "TBD"  # Must be 0 or explicitly justified
    
  # SPARQL COMPATIBILITY
  sparql_compatibility:
    queries_tested: "TBD"
    queries_identical_results: "TBD"
    queries_with_differences: "TBD"
    differences_documented: "TBD"

# Sign-off: Spike results reviewed and approved
spike_approval:
  reviewed_by: ""
  date: ""
  signature: ""
```

### Appendix B: OWL 2 RL Compliance Checker

```bash
# Check ontology for OWL 2 RL compliance
w2fuel-rl-check ontologies/domains/realestate-v1.0.owl

# Output:
# ✓ 142 axioms checked
# ✓ 138 axioms are OWL 2 RL compliant
# ⚠ 4 axioms require SHACL alternative:
#   - Line 45: owl:someValuesFrom → use sh:minCount 1
#   - Line 78: owl:cardinality 2 → use sh:minCount 2 + sh:maxCount 2
#   - Line 112: owl:unionOf in subclass → use sh:or
#   - Line 156: owl:complementOf → use sh:not
```

### Appendix C: Manual SHACL Cookbook (Preserved)

The Manual SHACL Cookbook from v1.2.x is **unchanged** — templates for unsupported constructs remain valid.

### Appendix D: SHACL Signing & Key Rotation (V1.3.1)

```yaml
shacl_signing:
  algorithm: "Ed25519"
  
  key_management:
    storage: "HashiCorp Vault"
    path: "secret/w2fuel/signing-keys"
    
  rotation_policy:
    frequency: "annual"
    overlap_period_days: 30
    notification_days_before: 60
    
  key_lifecycle:
    active: "Current signing key"
    previous: "Still valid for verification during overlap"
    deprecated: "No longer valid for verification"
    
  rotation_procedure:
    1: "Generate new key in Vault"
    2: "Update CI to sign with new key"
    3: "Both keys valid for 30 days"
    4: "After 30 days, deprecate old key"
    5: "Notify downstream services of key change"
    
  verification_behavior:
    valid_signature: "Accept SHACL bundle"
    invalid_signature: "REJECT — do not use"
    unknown_key: "REJECT — unknown signing key"
    expired_key: "REJECT — key no longer valid"
    
  emergency_bypass:
    requires: "Governance body approval"
    audit: "Log bypass with approval reference"
    flag: "w2fuel:signatureBypass: true on validated instances"
```

### Appendix E: Operational Runbooks (V1.3.1)

#### RB-001: Rollback Bad Schema

```bash
# RUNBOOK: Rollback a bad schema deployment

# 1. Identify bad commit
BAD_COMMIT=$(git log --oneline -1)  # e.g., abc123

# 2. Revert in Git
git revert --no-commit $BAD_COMMIT
git commit -m "[ROLLBACK] Revert $BAD_COMMIT due to <reason>"
git push

# 3. CI will automatically:
#    - Run Nemo classification
#    - Load reverted ontology to Oxigraph
#    - Emit fnsr.schema.updated

# 4. Verify rollback
curl https://w2fuel.fnsr.org/admin/consistency-check

# 5. Notify downstream
# Event is emitted automatically; manual notification if urgent
```

#### RB-002: Restore from Snapshot

See §5.3 HA/DR section for full restore procedure.

#### RB-003: Re-run Nemo on Older Commit

```bash
# RUNBOOK: Re-run classification on historical commit

# 1. Checkout historical commit
git checkout <commit_hash>

# 2. Run Nemo manually
nemo --input ontologies/domains/*.owl \
     --output /tmp/nemo-output \
     --rules datalog/generated/*.dl

# 3. Compare with current
diff /tmp/nemo-output current-inferences/

# 4. Return to main
git checkout main
```

#### RB-004: Triage Event Gaps

```bash
# RUNBOOK: Triage missing events

# 1. Check current sequence_id
curl https://w2fuel.fnsr.org/admin/consistency-check | jq '.sequence_id'

# 2. Check downstream last processed
redis-cli GET w2fuel:last_processed_sequence_id

# 3. If gap exists:
#    - Check Kafka for undelivered messages
#    - Check W2Fuel logs for emission failures
#    - Downstream can call /admin/consistency-check to sync

# 4. If events are lost:
#    - Downstream should request full refresh
#    - Emit fnsr.schema.refresh_required event
```

### Appendix F: Removed Sections from v1.2.x

The following sections were **removed** as no longer applicable:

| v1.2.x Section | Reason Removed |
|----------------|----------------|
| §5.1.1 Fuseki Rebuild Hardening | Oxigraph is persistent |
| §5.1.1 Blue/Green Rehydration | No ephemeral rebuilds |
| §5.1.1 Fuseki SLO Staging Test Plan | No rebuild SLOs |
| §8.3 Tiered CI Verification | Single-tier with Nemo |
| §8.3 L0-PENDING Status | No pending state |
| §8.3 Verification Status Consumer Contract (pending) | Simplified |
| §5.1.1 Automatic Fuseki SLO Remediation | No SLO concerns |

**Lines removed from v1.2.x:** ~570 (12%)  
**Lines added in v1.3.1:** ~500 (HA/DR, inference parity, golden rules, runbooks)  
**Net reduction:** ~70 lines, but significantly simpler architecture

### Appendix G: V1.3.1 Change Summary

| Section | Change | Rationale |
|---------|--------|-----------|
| §5.3 HA/DR | NEW: Active-standby architecture, RTO/RPO, restore validation | Blocker: Oxigraph single-point-of-failure |
| §5.4 Update Flow | ENHANCED: Explicit checkpoints, transaction limits | Blocker: Event emission semantics |
| §7.3 Golden-Rule Tests | NEW: OWL→Datalog translation unit tests | Blocker: Transpilation fidelity |
| §7.4 Inference Parity | NEW: HermiT vs Nemo comparison in CI | Blocker: Semantic drift risk |
| §9.1 Checkpoint Event | ENHANCED: Normative emission preconditions, handler pseudocode | Blocker: Final checkpoint semantics |
| §14.2 Sentinel Metrics | NEW: Preserved anomaly detection metrics | Risk: Monitoring gaps |
| §15.3 SPARQL Compatibility | NEW: Query comparison test suite | Risk: Migration edge cases |
| Appendix A | ENHANCED: Required spike validation checklist | Blocker: Populate before sign-off |
| Appendix D | NEW: Key rotation policy | Risk: Security lifecycle |
| Appendix E | NEW: Operational runbooks | Risk: Recovery procedures |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0-draft | 2026-02-01 | Aaron / Claude | Initial specification |
| 1.1.0 | 2026-02-01 | Aaron / Claude | SHACL, CI/CD, bridges, disambiguation |
| 1.2.0 | 2026-02-01 | Aaron / Claude | Production hardening |
| 1.2.3 | 2026-02-02 | Aaron / Claude | Final v1.2.x (Java stack) |
| 1.3.0-draft | 2026-02-02 | Aaron / Claude | Rust stack adoption (Oxigraph/Nemo) |
| **1.3.1** | **2026-02-02** | **Aaron / Claude** | **HA/DR, inference parity, golden-rules, checkpoint semantics, runbooks** |

---

## Production Readiness Sign-off

### Acceptance Checklist (V1.3.1)

**Critical (MUST pass before production):**

- [ ] **Appendix A populated** — Rust spike results with all TBD fields filled
- [ ] **Inference parity tests pass** — HermiT vs Nemo comparison for representative ontologies
- [ ] **Golden-rule translation tests pass** — All OWL→Datalog unit tests green
- [ ] **HA/DR validated** — At least one snapshot restore drill completed in staging
- [ ] **Canonical checkpoint event reviewed** — Integration team approves event schema
- [ ] **SPARQL compatibility verified** — Migration queries produce identical results

**High (SHOULD pass before production):**

- [ ] **Sentinel metrics configured** — Event gap, Nemo failure, WAL lag monitoring
- [ ] **Key rotation tested** — SHACL signing key rotation exercised
- [ ] **Runbooks reviewed** — Operations team approves RB-001 through RB-004
- [ ] **Downstream notification** — All consumer teams informed of upgrade

### Sign-off Table

| Approval | Name | Role | Date | Signature |
|----------|------|------|------|-----------|
| Rust Spike Validation | | Engineering Lead | | |
| Inference Parity | | Ontology Steward | | |
| HA/DR Validation | | SRE Lead | | |
| Security Review | | Security Engineer | | |
| Technical Review | | Ontology Steward | | |
| Operations Review | | SRE Lead | | |
| Governance Approval | | Governance Body Chair | | |

**Review Status:** DRAFT — Pending Rust Spike Validation  
**Prerequisite:** Complete Rust Spike benchmarks and populate Appendix A  
**Effective Date:** Upon governance approval after spike validation

---

*End of Specification*
