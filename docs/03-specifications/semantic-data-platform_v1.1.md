## Semantic Data Platform Architecture v1.1

**Version:** 1.1
**Previous:** v1.0 (2026-01-19)
**Changes:** Addresses knowledge latency, HITL reconciliation, materialized reasoning, ontology registry

---

### Design Principles (Unchanged)

| Principle | Implication |
|-----------|-------------|
| **Shared ontology, not shared database** | Services agree on semantics (BFO/CCO), not storage |
| **Event-driven integration** | Services communicate via semantic events, not API calls |
| **Each service owns its transform** | Adapters are independent; only output format is standardized |
| **Graph is append-mostly** | New assertions don't overwrite; provenance preserved |
| **Query layer is separate from storage** | Multiple query interfaces over same graph |

---

### Architecture Overview (Revised)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              INGESTION LAYER                                     │
│                         (Modular, Self-Contained Adapters)                       │
│                                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Structured │  │    Semi-     │  │   Natural    │  │   External   │        │
│  │     Data     │  │  Structured  │  │   Language   │  │   Knowledge  │        │
│  │   Adapters   │  │   Adapters   │  │   Adapters   │  │   Adapters   │        │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤        │
│  │ • SQL/JDBC   │  │ • JSON-LD    │  │ • TagTeam    │  │ • Wikidata   │        │
│  │ • CSV/Excel  │  │ • XML/XSD    │  │ • Document   │  │ • DBpedia    │        │
│  │ • REST APIs  │  │ • FHIR/HL7   │  │   Processor  │  │ • Domain     │        │
│  │ • GraphQL    │  │ • EDI        │  │ • Email      │  │   Ontologies │        │
│  │ • Parquet    │  │ • Existing   │  │ • Voice/     │  │ • Industry   │        │
│  │              │  │   RDF/OWL    │  │   Transcript │  │   Standards  │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         │                 │                 │                 │                 │
│         │    ┌────────────┴─────────────────┴─────────────────┘                 │
│         │    │                                                                  │
│         ▼    ▼                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                     ONTOLOGY REGISTRY (v1.1)                             │   │
│  │         • Canonical URI resolution    • Version management               │   │
│  │         • Schema validation           • Adapter certification            │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│         │                                                                       │
│         ▼                                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      SEMANTIC EVENT BUS                                  │   │
│  │              (JSON-LD Assertions + Provenance + Status)                  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           RECONCILIATION LAYER                                   │
│                                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐              │
│  │ Entity Resolution │  │ Conflict Detection│  │ Provenance       │              │
│  │ Service           │  │ Service           │  │ Registry         │              │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤              │
│  │ • Same-as        │  │ • Contradictory  │  │ • Source trust   │              │
│  │   detection      │  │   assertions     │  │   scores         │              │
│  │ • Coreferent     │  │ • Temporal       │  │ • Assertion      │              │
│  │   linking        │  │   supersession   │  │   lineage        │              │
│  │ • Canonical ID   │  │ • Confidence     │  │ • Transform      │              │
│  │   assignment     │  │   comparison     │  │   audit trail    │              │
│  │ • CONFIDENCE     │  │                  │  │                  │              │
│  │   THRESHOLDS     │  │                  │  │                  │              │
│  └────────┬─────────┘  └────────┬─────────┘  └──────────────────┘              │
│           │                     │                                               │
│           │    Low confidence   │   Unresolvable conflicts                      │
│           │    matches (<0.85)  │                                               │
│           ▼                     ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                 HUMAN-IN-THE-LOOP SERVICE (v1.1)                         │   │
│  │                                                                          │   │
│  │   • Review queue for uncertain matches    • Steward dashboard            │   │
│  │   • Conflict resolution interface         • Feedback loop to adapters    │   │
│  │   • Audit trail of human decisions        • Training data export         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              GRAPH LAYER                                         │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                         UBER GRAPH                                       │   │
│  │                                                                          │   │
│  │   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌───────────┐   │   │
│  │   │ Upper       │   │ Domain      │   │ Instance    │   │Materialized│  │   │
│  │   │ Ontology    │   │ Ontologies  │   │ Data        │   │Inferences │   │   │
│  │   │ (BFO/CCO)   │   │ (loaded)    │   │ (assertions)│   │(v1.1)     │   │   │
│  │   └─────────────┘   └─────────────┘   └─────────────┘   └───────────┘   │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                       ▲                                         │
│                                       │                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    INFERENCE MATERIALIZER (v1.1)                         │   │
│  │                                                                          │   │
│  │   • Batch OWL reasoning on write      • Incremental inference            │   │
│  │   • Materialized triple storage       • Invalidation on update           │   │
│  │   • Configurable reasoning profiles   • Inference provenance             │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              QUERY LAYER                                         │
│                                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   SPARQL     │  │   GraphQL    │  │   Natural    │  │   Status     │        │
│  │   Endpoint   │  │   Federation │  │   Language   │  │   Service    │        │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  │   (v1.1)     │        │
│  │ • Standard   │  │ • Schema     │  │ • Question   │  ├──────────────┤        │
│  │   SPARQL 1.1 │  │   projection │  │   answering  │  │ • Processing │        │
│  │ • Federated  │  │ • Resolver   │  │ • Semantic   │  │   state      │        │
│  │   queries    │  │   layer      │  │   search     │  │ • Pending    │        │
│  │ • Pre-       │  │              │  │              │  │   assertions │        │
│  │   computed   │  │              │  │              │  │ • ETAs       │        │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION LAYER                                      │
│                                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Compliance  │  │  Contract    │  │  Claims      │  │  Data        │        │
│  │  Dashboard   │  │  Analyzer    │  │  Intelligence│  │  Steward     │        │
│  │              │  │              │  │              │  │  Console     │        │
│  │  (shows      │  │              │  │              │  │  (HITL UI)   │        │
│  │  pending)    │  │              │  │              │  │  (v1.1)      │        │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

### New Components (v1.1)

#### 1. Ontology Registry Service

**Problem Addressed:** If SQL Adapter uses one version of CCO and TagTeam uses another, the graph becomes inconsistent.

**Responsibilities:**

| Function | Description |
|----------|-------------|
| URI Resolution | Canonical URIs for all classes and properties |
| Version Management | Track ontology versions, deprecation, migration paths |
| Schema Validation | Validate adapter output against current ontology |
| Adapter Certification | Verify adapters use correct vocabulary before publishing |

**API:**

```javascript
interface OntologyRegistry {
  // Lookup
  resolveURI(term: string, context?: string): CanonicalURI
  getClassDefinition(uri: string): ClassSpec
  getPropertyDefinition(uri: string): PropertySpec
  
  // Validation
  validateAssertion(assertion: JSONLDGraph): ValidationResult
  validateAdapterConfig(config: AdapterConfig): CertificationResult
  
  // Versioning
  getCurrentVersion(ontologyPrefix: string): VersionInfo
  getMigrationPath(fromVersion: string, toVersion: string): MigrationSpec
  
  // Discovery
  listAvailableOntologies(): OntologyManifest[]
  getDomainConfig(domain: string): DomainOntologyBundle
}
```

**Adapter Integration:**

```javascript
// Every adapter calls registry on startup
class SQLAdapter {
  async initialize() {
    // Check out current ontology version
    this.ontologyVersion = await registry.getCurrentVersion('cco');
    this.validator = await registry.getValidator('cco', this.ontologyVersion);
    
    // Validate mapping configuration
    const certResult = await registry.validateAdapterConfig(this.config);
    if (!certResult.valid) {
      throw new AdapterCertificationError(certResult.errors);
    }
  }
  
  async emitAssertion(assertion) {
    // Validate before publishing
    const validation = await this.validator.validate(assertion);
    if (!validation.valid) {
      this.logger.error('Invalid assertion', validation.errors);
      return;
    }
    await this.eventBus.publish(assertion);
  }
}
```

**Registry Storage:**

```
┌─────────────────────────────────────────┐
│          Ontology Registry DB            │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ Ontology Manifests                  │ │
│  │  • BFO 2020 (canonical)             │ │
│  │  • CCO 1.5 (current)                │ │
│  │  • CCO 1.4 (deprecated, migrate)    │ │
│  │  • TagTeam 3.0 (extension)          │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ URI Mappings                        │ │
│  │  • Aliases → Canonical              │ │
│  │  • Deprecated → Replacement         │ │
│  │  • Version-specific resolutions     │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ Adapter Certifications              │ │
│  │  • sql-adapter-v2.1: certified      │ │
│  │  • tagteam-v3.0: certified          │ │
│  │  • legacy-import-v1: deprecated     │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

#### 2. Processing Status Service

**Problem Addressed:** User submits document, immediately checks dashboard, data not visible yet (eventual consistency confusion).

**Design:**

Every assertion batch gets a **tracking ID** that flows through the pipeline:

```json
{
  "eventType": "AssertionBatch",
  "trackingId": "trk-a1b2c3d4",
  "sourceRef": "doc:contract-2024-0892",
  "status": "ingested",
  "timestamps": {
    "submitted": "2026-01-19T14:30:00Z",
    "ingested": "2026-01-19T14:30:01Z"
  },
  "payload": { /* assertions */ }
}
```

**Status Transitions:**

```
submitted → ingested → validating → reconciling → [pending_review] → committed
                                         │
                                         └──→ conflict_detected → [pending_review] → resolved
```

**Status Service API:**

```javascript
interface StatusService {
  // Query by tracking ID
  getStatus(trackingId: string): ProcessingStatus
  
  // Query by source document
  getStatusBySource(sourceRef: string): ProcessingStatus[]
  
  // Query pending items for a user/session
  getPendingAssertions(sessionId: string): PendingAssertion[]
  
  // Subscribe to status changes
  subscribe(trackingId: string, callback: StatusCallback): Subscription
  
  // Estimated completion
  getETA(trackingId: string): ETAEstimate
}

interface ProcessingStatus {
  trackingId: string
  sourceRef: string
  status: 'submitted' | 'ingested' | 'validating' | 'reconciling' | 
          'pending_review' | 'committed' | 'conflict_detected' | 'failed'
  timestamps: Record<string, DateTime>
  assertionCount: number
  pendingCount: number
  committedCount: number
  errors?: ProcessingError[]
  eta?: DateTime
}
```

**UI Integration:**

```javascript
// Dashboard component
function ComplianceDashboard({ documentId }) {
  const [status, setStatus] = useState(null);
  
  useEffect(() => {
    const sub = statusService.subscribe(documentId, setStatus);
    return () => sub.unsubscribe();
  }, [documentId]);
  
  return (
    <div>
      {status?.status === 'committed' ? (
        <DataView data={status.assertions} />
      ) : (
        <ProcessingIndicator 
          status={status?.status}
          progress={status?.committedCount / status?.assertionCount}
          eta={status?.eta}
        />
      )}
    </div>
  );
}
```

**Visual Indicator Patterns:**

| Status | UI Treatment |
|--------|--------------|
| `submitted` | Spinner + "Processing..." |
| `validating` | Progress bar + "Validating assertions..." |
| `reconciling` | Progress bar + "Resolving entities..." |
| `pending_review` | Warning badge + "Awaiting review" + link to steward queue |
| `committed` | Success + show data |
| `conflict_detected` | Warning + "Conflicts found" + link to resolution |
| `failed` | Error + details + retry option |

---

#### 3. Human-in-the-Loop (HITL) Service

**Problem Addressed:** Entity resolution with 0.7 confidence—auto-link or wait for human?

**Confidence Threshold Strategy:**

| Confidence | Action | Rationale |
|------------|--------|-----------|
| ≥ 0.95 | Auto-commit | High certainty, no human needed |
| 0.85 - 0.94 | Auto-commit + flag for audit | Likely correct, spot-check later |
| 0.70 - 0.84 | Queue for review | Uncertain, human decides |
| < 0.70 | Reject match, keep separate | Probably wrong, don't pollute graph |

These thresholds are **configurable per domain**—medical might require higher confidence than general business data.

**HITL Service Architecture:**

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HUMAN-IN-THE-LOOP SERVICE                         │
│                                                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │  Review Queue   │  │  Decision       │  │  Feedback       │     │
│  │  Manager        │  │  Recorder       │  │  Loop           │     │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤     │
│  │ • Priority      │  │ • Record human  │  │ • Export        │     │
│  │   scoring       │  │   decisions     │  │   training data │     │
│  │ • Assignment    │  │ • Audit trail   │  │ • Adapter       │     │
│  │   routing       │  │ • Reasoning     │  │   feedback      │     │
│  │ • SLA tracking  │  │   capture       │  │ • Threshold     │     │
│  │                 │  │                 │  │   tuning        │     │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘     │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Review Item Types                         │   │
│  │                                                              │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │   │
│  │  │ Entity      │  │ Conflict    │  │ Low         │         │   │
│  │  │ Match       │  │ Resolution  │  │ Confidence  │         │   │
│  │  │ Review      │  │ Review      │  │ Assertion   │         │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Review Item Schema:**

```javascript
interface ReviewItem {
  id: string
  type: 'entity_match' | 'conflict_resolution' | 'low_confidence_assertion'
  priority: number  // Higher = more urgent
  createdAt: DateTime
  slaDeadline?: DateTime
  
  // What needs review
  subject: {
    assertions: Assertion[]
    context: string  // Source text, surrounding data
    systemRecommendation?: string
    confidence: number
  }
  
  // Options for reviewer
  options: ReviewOption[]
  
  // Assignment
  assignedTo?: string
  status: 'pending' | 'assigned' | 'completed' | 'escalated'
  
  // Resolution (when completed)
  resolution?: {
    decision: string
    reasoning: string
    decidedBy: string
    decidedAt: DateTime
  }
}

interface ReviewOption {
  id: string
  label: string
  description: string
  action: 'accept' | 'reject' | 'modify' | 'escalate'
  resultingAssertions?: Assertion[]
}
```

**Entity Match Review Example:**

```json
{
  "id": "review-001",
  "type": "entity_match",
  "priority": 75,
  "subject": {
    "assertions": [
      { "@id": "inst:Person_JaneSmith_sql", "rdfs:label": "Jane Smith", "source": "HR Database" },
      { "@id": "inst:Person_JSmith_email", "rdfs:label": "J. Smith", "source": "Email parsing" }
    ],
    "context": "Email signature: 'J. Smith, Engineering'. HR record: 'Jane Smith, Engineering Dept, Employee ID E-1234'",
    "systemRecommendation": "Likely same person (same department, name match)",
    "confidence": 0.78
  },
  "options": [
    {
      "id": "accept",
      "label": "Yes, same person",
      "description": "Link these as the same individual",
      "action": "accept",
      "resultingAssertions": [
        { "inst:Person_JaneSmith_sql": { "owl:sameAs": "inst:Person_JSmith_email" } }
      ]
    },
    {
      "id": "reject",
      "label": "No, different people",
      "description": "Keep as separate entities",
      "action": "reject"
    },
    {
      "id": "need_more",
      "label": "Need more information",
      "description": "Escalate for additional research",
      "action": "escalate"
    }
  ]
}
```

**Steward Dashboard UI:**

```
┌─────────────────────────────────────────────────────────────────────┐
│  Data Steward Console                              [Jane Doe] [≡]   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Review Queue                                        Filter: [All ▼] │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ ⚠️  Entity Match (0.78)                        Priority: 75  │   │
│  │                                                              │   │
│  │  "Jane Smith" (HR Database)                                  │   │
│  │       ↕️  possible match                                     │   │
│  │  "J. Smith" (Email parsing)                                  │   │
│  │                                                              │   │
│  │  Context: Both in Engineering department                     │   │
│  │                                                              │   │
│  │  [✓ Same Person]  [✗ Different]  [? Need More Info]         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ ⚡ Conflict Detected                           Priority: 90  │   │
│  │                                                              │   │
│  │  Assertion A: "Project deadline is March 15"                 │   │
│  │     Source: Planning document (2026-01-10)                   │   │
│  │                                                              │   │
│  │  Assertion B: "Project deadline is April 1"                  │   │
│  │     Source: Email from PM (2026-01-18)                       │   │
│  │                                                              │   │
│  │  [A is current]  [B is current]  [Both valid (phases)]      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  Showing 2 of 47 pending items                      [Load more...]  │
└─────────────────────────────────────────────────────────────────────┘
```

**Feedback Loop:**

Human decisions become training data:

```javascript
// After human resolves entity match
async function recordDecision(reviewItem, decision) {
  // 1. Record in audit trail
  await auditLog.record({
    reviewId: reviewItem.id,
    decision: decision,
    decidedBy: currentUser,
    timestamp: now()
  });
  
  // 2. Apply to graph
  if (decision.action === 'accept') {
    await graphWriter.write(decision.resultingAssertions);
  }
  
  // 3. Export as training example
  await trainingExporter.export({
    input: reviewItem.subject,
    output: decision,
    confidence: reviewItem.subject.confidence,
    humanJudgment: decision.action
  });
  
  // 4. Update confidence thresholds (periodic batch job)
  // If humans consistently accept 0.75+ matches, raise auto-commit threshold
}
```

---

#### 4. Inference Materializer

**Problem Addressed:** Real-time OWL reasoning on large graphs causes timeouts.

**Strategy: Materialize on Write, Query Pre-Computed**

```
┌─────────────────────────────────────────────────────────────────────┐
│                      INFERENCE MATERIALIZER                          │
│                                                                      │
│   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐      │
│   │ Incoming      │    │ Incremental   │    │ Materialized  │      │
│   │ Assertions    │───▶│ Reasoner      │───▶│ Triple Store  │      │
│   └───────────────┘    └───────────────┘    └───────────────┘      │
│                              │                      │               │
│                              ▼                      │               │
│                     ┌───────────────┐               │               │
│                     │ Inference     │               │               │
│                     │ Provenance    │◀──────────────┘               │
│                     │ (why inferred)│                               │
│                     └───────────────┘                               │
│                                                                      │
│   Reasoning Profiles:                                                │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ • rdfs: Basic subclass/subproperty (fast, always on)        │  │
│   │ • owl-el: Tractable OWL subset (moderate, default)          │  │
│   │ • owl-dl: Full OWL (expensive, batch only)                  │  │
│   └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

**Reasoning Profile Selection:**

| Profile | Use Case | Performance | Completeness |
|---------|----------|-------------|--------------|
| `rdfs` | Basic hierarchy traversal | Fast (real-time) | Low |
| `owl-el` | Class expressions, property chains | Moderate (near real-time) | Medium |
| `owl-rl` | Rules-based reasoning | Moderate | Medium |
| `owl-dl` | Full description logic | Slow (batch) | High |

Default: `owl-el` for write-time materialization, `owl-dl` for nightly batch.

**Incremental Reasoning:**

When new assertions arrive, don't re-reason entire graph:

```javascript
class IncrementalReasoner {
  async materialize(newAssertions, profile = 'owl-el') {
    // 1. Identify affected region of graph
    const affectedEntities = this.findAffectedEntities(newAssertions);
    
    // 2. Extract relevant subgraph
    const subgraph = await this.graph.extractSubgraph(affectedEntities, depth = 2);
    
    // 3. Run reasoner on subgraph + new assertions
    const inferences = await this.reasoner.infer(subgraph, newAssertions, profile);
    
    // 4. Store inferences with provenance
    for (const inference of inferences) {
      await this.graph.write({
        ...inference,
        '_provenance': {
          type: 'inference',
          rule: inference.derivation,
          premises: inference.premises,
          materializedAt: now(),
          profile: profile
        }
      });
    }
    
    return inferences;
  }
}
```

**Inference Provenance:**

Every inferred triple is tagged:

```turtle
# Explicit assertion
GRAPH inst:assertions {
  inst:Person_Jane a cco:Person .
  cco:Person rdfs:subClassOf bfo:BFO_0000040 .
}

# Materialized inference
GRAPH inst:inferences {
  inst:Person_Jane a bfo:BFO_0000040 .
}

# Inference provenance
GRAPH inst:inference_provenance {
  inst:inference_001 a tagteam:MaterializedInference ;
    tagteam:inferred_triple inst:Person_Jane_is_MaterialEntity ;
    tagteam:derivation_rule "rdfs:subClassOf transitivity" ;
    tagteam:premises ( inst:Person_Jane_is_Person inst:Person_subClassOf_MaterialEntity ) ;
    tagteam:materialized_at "2026-01-19T14:35:00Z" ;
    tagteam:reasoning_profile "owl-el" .
}
```

**Invalidation on Update:**

When base assertions change, affected inferences must be recomputed:

```javascript
async function handleAssertionUpdate(updatedAssertion) {
  // 1. Find inferences that depended on this assertion
  const dependentInferences = await graph.query(`
    SELECT ?inference WHERE {
      GRAPH inst:inference_provenance {
        ?inference tagteam:premises ?premiseList .
        ?premiseList rdf:rest*/rdf:first ${updatedAssertion.id} .
      }
    }
  `);
  
  // 2. Mark as stale
  for (const inf of dependentInferences) {
    await graph.update(inf, { 'tagteam:status': 'stale' });
  }
  
  // 3. Re-materialize affected region
  await incrementalReasoner.materialize([updatedAssertion]);
}
```

---

### Revised Data Flow (v1.1)

**Scenario:** New employee announcement email arrives

```
1. EMAIL ADAPTER
   • Checks out ontology from Registry (validates vocabulary)
   • Parses email via TagTeam
   • Emits AssertionBatch with trackingId: trk-001
   • Status: "submitted" → "ingested"

2. ONTOLOGY REGISTRY
   • Validates assertions against current CCO version
   • Rejects malformed vocabulary
   • Status: "ingested" → "validating" → "validated"

3. ENTITY RESOLUTION SERVICE
   • Finds potential match: confidence 0.78
   • Below auto-commit threshold (0.85)
   • Routes to HITL queue
   • Status: "validated" → "pending_review"

4. STATUS SERVICE
   • Dashboard shows: "Processing... Awaiting review (1 item)"
   • User can see partial data that IS committed

5. HUMAN-IN-THE-LOOP
   • Steward reviews match, confirms "same person"
   • Decision recorded with reasoning
   • owl:sameAs assertion emitted
   • Status: "pending_review" → "reconciling"

6. INFERENCE MATERIALIZER
   • New assertions trigger incremental reasoning
   • Materializes: Jane is a MaterialEntity (via Person subclass)
   • Stores inference with provenance

7. GRAPH WRITER
   • Commits all assertions + inferences
   • Status: "reconciling" → "committed"

8. STATUS SERVICE
   • Dashboard updates: "Complete ✓"
   • All data now visible
```

---

### Scaling Considerations (Revised)

| Component | Scaling Strategy | Bottleneck Risk |
|-----------|------------------|-----------------|
| Structured Adapters | Horizontal (stateless) | Low |
| TagTeam Adapters | Horizontal (stateless, but high CPU) | **Medium** - needs more instances |
| Ontology Registry | Replicated read, single write | Low |
| Event Bus | Partitioned by source/entity | Low |
| Entity Resolution | Horizontal with entity-based partitioning | **Medium** |
| HITL Service | Horizontal (queue-based) | Low (human throughput is limit) |
| Inference Materializer | Horizontal with graph region partitioning | **High** - most complex |
| Graph Store | Sharded or clustered triple store | **High** |
| Status Service | Replicated read, event-sourced write | Low |

**Resource Allocation Guidance:**

```yaml
# Example Kubernetes resource allocation
services:
  sql-adapter:
    replicas: 2
    cpu: 0.5
    memory: 512Mi
    
  tagteam-adapter:
    replicas: 6       # More replicas - high CPU
    cpu: 2.0          # More CPU per replica
    memory: 2Gi
    
  entity-resolution:
    replicas: 4
    cpu: 1.0
    memory: 4Gi       # Needs memory for candidate matching
    
  inference-materializer:
    replicas: 2
    cpu: 4.0          # Reasoning is CPU-intensive
    memory: 8Gi       # Needs memory for subgraph extraction
```

---

### Summary of v1.1 Changes

| Concern | v1.0 | v1.1 Resolution |
|---------|------|-----------------|
| Knowledge Latency | Not addressed | Status Service + processing indicators |
| HITL Reconciliation | Not addressed | HITL Service + Steward Dashboard |
| Reasoning Performance | Real-time OWL | Materialized inferences + profiles |
| Schema Consistency | Implicit | Ontology Registry + adapter certification |
| Confidence Handling | Not specified | Threshold tiers + configurable per domain |
| Inference Provenance | Not addressed | Materialized triples tagged with derivation |

---

### Next Steps

1. **Detailed Entity Resolution Spec** — Define matching algorithms, blocking strategies, confidence scoring
2. **HITL UI Wireframes** — Design steward interface for review workflows
3. **Ontology Registry Schema** — Define manifest format, versioning rules
4. **Status Service Event Schema** — Define event types, state machine

Want me to proceed with any of these?