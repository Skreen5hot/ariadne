# TagTeam Consolidated Roadmap

**Version:** 6.6.0
**Last Updated:** 2026-01-28
**Status:** Phase 6.6 Complete (OntologyTextTagger), v1/v2 Scope Contract Locked, Phase 7 Next (Epistemic Layer)

---

## Vision Statement

> **TagTeam is a domain-neutral semantic interpretation engine that enables ethical dilemma analysis.**

TagTeam provides the foundational NLP infrastructure for extracting structured, ontologically-grounded representations from natural language. While domain-neutral by design, its primary use case is ethical dilemma analysis—a domain where ambiguity preservation is essential.

Natural language and ambiguity are inseparable. To properly analyze ethical dilemmas, we must preserve and surface ambiguity rather than force false precision. TagTeam aims to be a **semantic interpretation engine** that:

1. Makes explicit what the text commits to ontologically
2. Preserves what remains ambiguous or underspecified
3. Distinguishes the voice of the text from the voice of the interpreter
4. Knows the boundaries of its own competence
5. Produces structured representations that are auditable, contestable, and refinable

**Guiding Principle:** Better to output structured uncertainty than false precision.

### Architecture Philosophy

**Browser-First, Node.js Compatible**

TagTeam works like mermaid.js or d3.js - a self-contained JavaScript bundle that runs in browser or Node.js with no external dependencies.

```
┌─────────────────────────────────────────────────────────────────┐
│                    TagTeam Architecture                          │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              BROWSER BUNDLE (Primary)                    │   │
│  │              tagteam.js (~5-6 MB)                        │   │
│  │                                                          │   │
│  │  • Full semantic parsing                                 │   │
│  │  • Ambiguity preservation (interpretation lattice)       │   │
│  │  • BFO/CCO ontological mapping                          │   │
│  │  • Ethical value detection                              │   │
│  │  • SHACL validation                                     │   │
│  │  • JSON-LD output                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              │ Same API                          │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              NODE.JS (Server version)                    │   │
│  │              require('tagteam')                          │   │
│  │                                                          │   │
│  │  Same bundle + optional enhancements:                    │   │
│  │  • Batch processing                                     │   │
│  │  • Corpus analysis tools                                │   │
│  │  • Extended NLP integration (future)                    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Why Browser-First:**
- Self-contained = no server dependency
- Privacy for sensitive ethical content
- Instant feedback in educational/analysis tools
- Works offline
- Same codebase for browser and Node.js

---

## What's Complete

### Phase 4: JSON-LD Semantic Graphs (DONE)

**Certification:** 5.0/5.0 BFO/CCO Realist Compliance (2026-01-19)

| Week | Deliverables | Status |
|------|-------------|--------|
| **Week 1** | Two-tier architecture, Entity/Act extraction, Role detection | ✅ Complete |
| **Week 2** | Assertion events, GIT-Minimal provenance, Information Staircase | ✅ Complete |
| **Week 3** | SHACL validation, Complexity budget, Corpus testing, Documentation | ✅ Complete |

**Key Files Created:**
```
src/graph/
├── SemanticGraphBuilder.js    # Main orchestrator
├── EntityExtractor.js         # Tier 1/2 entity extraction
├── ActExtractor.js            # IntentionalAct nodes + selectional restrictions
├── RoleDetector.js            # BFO roles (Agent, Patient)
├── DomainConfigLoader.js      # Domain configuration system
├── AssertionEventBuilder.js   # Value/Context assertions
├── ContextManager.js          # Interpretation contexts
├── InformationStaircaseBuilder.js  # IBE/ICE linkage
├── JSONLDSerializer.js        # JSON-LD output
├── SHMLValidator.js           # SHACL pattern validation
├── ComplexityBudget.js        # Graph limits
└── [other factories...]

config/
└── medical.json               # Medical domain vocabulary
```

**Test Coverage:** 290+ tests passing

### Phase 5: NLP Foundation Upgrade (DONE)

**Certification:** Complete (2026-01-23)

| Deliverable | Status |
|-------------|--------|
| **5.0** NLP Library Evaluation | ✅ Custom implementation chosen |
| **5.1** Core NLP (Lemmatizer, ContractionExpander) | ✅ 149 tests |
| **5.2** Phrase Extractors (VP, NP) | ✅ 59 tests |
| **5.3** Ambiguity Detection | ✅ 71 tests |
| **5.3.1** Stakeholder Improvements | ✅ selectionalMismatch, Organization typing |

**Key Files Created:**
```
src/core/
├── ContractionExpander.js     # "don't" → "do not"
├── Lemmatizer.js              # "walked" → "walk"
├── VerbPhraseExtractor.js     # Modal force, negation, tense
└── NounPhraseExtractor.js     # Determiners, compounds, quantifiers

src/graph/
├── AmbiguityDetector.js       # 5 ambiguity types
└── AmbiguityReport.js         # JSON-LD output
```

**Test Coverage:** 280+ tests passing (Phase 5 specific: 279 tests)

**Acronyms:**
- **IEE**: Institute for Ethical Engineering - collaboration partner for ethical value definitions
- **BFO**: Basic Formal Ontology - top-level ontology framework
- **CCO**: Common Core Ontologies - mid-level ontology extending BFO
- **GIT**: Grounded Information Transfer theory

### Domain-Neutral Parser Implementation (DONE)

**Certification:** 5.0/5.0 Expert Certified (2026-01-19)

| Phase | Deliverables | Status |
|-------|-------------|--------|
| **Phase 1** | Suffix-based process detection, result noun exceptions, ONTOLOGICAL_VOCABULARY | ✅ Complete |
| **Phase 2** | DomainConfigLoader, config/medical.json, type specialization | ✅ Complete |
| **Phase 3** | Selectional restrictions, verb sense disambiguation, config overrides | ✅ Complete |

**Key Achievements:**
- "Palliative care" → `cco:ActOfCare` (Occurrent)
- "Provide care" → `cco:ActOfService` via selectional restrictions
- "Provide medication" → `cco:ActOfTransferOfPossession` (different verb sense)
- Domain vocabulary in loadable config files
- BFO-only mode works without any config loaded

---

## Ideal NLP Roadmap

### The Core Problem

Current TagTeam forces resolution of ambiguity. For ethical dilemma analysis, this loses critical information:

```
Input: "The doctor should prioritize the younger patient"

Current Output (forced resolution):
{
  "denotesType": "cco:ActOfPrioritization",
  "actualityStatus": "tagteam:Prescribed"  // Picked one reading
}

Ideal Output (ambiguity preserved):
{
  "interpretationLattice": {
    "readings": [
      { "id": "deontic", "gloss": "obligation to prioritize", "plausibility": 0.7 },
      { "id": "epistemic", "gloss": "expectation of prioritizing", "plausibility": 0.3 }
    ]
  },
  "defaultReading": "deontic"
}
```

### API Design: Opt-In Lattice (Backwards Compatible)

```javascript
// Current API (unchanged) - returns single graph
const graph = builder.build(text);

// New API (opt-in) - returns lattice with multiple readings
const result = builder.build(text, { preserveAmbiguity: true });
// Returns: {
//   defaultReading: JSON-LD graph,
//   lattice: InterpretationLattice,
//   _epistemics: { sourceAttributions, certaintyMarkers },
//   _validation: { internal, external }
// }
```

---

## Phase 5: NLP Foundation Upgrade ✅ COMPLETE

**Goal:** Remove Compromise bottleneck, enable ambiguity detection

**Status:** ✅ Complete (2026-01-23)
**Test Coverage:** 280+ tests passing (100% pass rate)
**Bundle Size:** +50KB (well under +200KB budget)

### Key Decision: Custom Implementation Over External Libraries

After evaluation, we chose **custom implementation** over external NLP libraries because:

1. **Zero new dependencies** - No supply chain risk
2. **Full control** - Tailored for ethical reasoning domain
3. **Archive code** - Robust implementations already existed
4. **Bundle size** - Custom code smaller than Wink NLP (+600KB) or nlp.js (+800KB)
5. **IEE corpus tested** - 100% accuracy on test scenarios

### 5.0 NLP Library Evaluation ✅ COMPLETE

**Decision:** Build custom modules using archived code rather than adding external dependencies.

**Rationale documented in:** Phase 5 Demo Presentation (`demos/Phase5_Demo_Presentation.md`)

### 5.1 Core NLP Modules ✅ COMPLETE

Created from archived POSTaggerGraph.js code:

| Module | Purpose | Test Count |
|--------|---------|------------|
| `src/core/ContractionExpander.js` | "don't" → "do not" with POS tags | 49 tests |
| `src/core/Lemmatizer.js` | "walked" → "walk", "children" → "child" | 100 tests |

### 5.2 Phrase Extractors ✅ COMPLETE

Custom extractors reduce Compromise dependency:

| Module | Purpose | Test Count |
|--------|---------|------------|
| `src/core/VerbPhraseExtractor.js` | Modals, negation, tense, voice | 27 tests |
| `src/core/NounPhraseExtractor.js` | Determiners, modifiers, compounds | 32 tests |

**Key Features:**
- Modal force classification (deontic vs epistemic signals)
- Negation detection including "never" look-back
- Quantifier detection (universal, existential, negative)
- Nominalization detection for process/continuant ambiguity

### 5.3 Ambiguity Detection Layer ✅ COMPLETE

| Module | Purpose | Test Count |
|--------|---------|------------|
| `src/graph/AmbiguityDetector.js` | Identifies 5+ ambiguity types | 31 tests |
| `src/graph/AmbiguityReport.js` | Structured output with JSON-LD | 26 tests |
| Integration tests | End-to-end with SemanticGraphBuilder | 14 tests |

**Ambiguity Types Detected:**

| Type | Detection Signal | Example |
|------|------------------|---------|
| `noun_category` | Nominalization suffix + context | "organization" (process vs entity) |
| `modal_force` | Modal + subject/verb analysis | "should" (obligation vs expectation) |
| `scope` | Quantifier + negation position | "not all" (wide vs narrow scope) |
| `selectional_violation` | Inanimate agent + intentional verb | "The rock decided" |
| `potential_metonymy` | Location as agent | "The White House announced" |

### 5.3.1 Stakeholder Improvements ✅ COMPLETE

Based on stakeholder review (2026-01-23):

1. **`tagteam:selectionalMismatch: true`** - Flag on acts with inanimate agents
2. **Organization typing** - committee, board, council, commission, panel, team → `cco:Organization`
3. **Ambiguity surfacing** - Flags added directly to `@graph` nodes, not just `_ambiguityReport`

### Phase 5 Lessons Learned

**What Worked Well:**
- Incremental development with continuous testing
- Custom code + archived implementations = zero dependencies
- `detectAmbiguity: true` opt-in flag preserves backwards compatibility
- Surfacing ambiguity in both `_ambiguityReport` AND `@graph` nodes serves different consumers

**What Could Be Improved:**
- Entity label handling inconsistency (`label` vs `rdfs:label`) caused bug in integration
- Need consistent interface between test data and production graph structure

**Key Insight for Phase 6:**
The ambiguity detection foundation is solid, but **resolution** is the hard problem. Phase 5 flags ambiguity; Phase 6 must decide *when* to preserve multiple readings vs pick a default.

---

## Phase 6: Interpretation Lattice

**Goal:** Transform detected ambiguities (Phase 5) into preserved, structured readings

**Bundle Size Budget:** +100KB max (target: 5.1MB total)

**Prerequisites:** Phase 5 complete (AmbiguityDetector, AmbiguityReport)

### Phase 5 → Phase 6 Connection

Phase 5 **detects** ambiguities and flags them. Phase 6 **resolves** when to preserve multiple readings:

```
Phase 5 Output:                      Phase 6 Output:
┌────────────────────────┐           ┌────────────────────────────────────┐
│ _ambiguityReport: {    │           │ interpretationLattice: {           │
│   ambiguities: [       │    →      │   defaultReading: { graph... },    │
│     { type: "modal",   │           │   alternativeReadings: [           │
│       readings: [...], │           │     { id: "epistemic",             │
│       confidence: ... }│           │       plausibility: 0.3,           │
│   ]                    │           │       graph: {...} }               │
│ }                      │           │   ]                                │
└────────────────────────┘           └────────────────────────────────────┘
```

### 6.0 Selectional Preference Lookup Table ✅ COMPLETE

**Status:** ✅ Complete (2026-01-26)
**Priority:** Critical (stakeholder requested)
**Effort:** Low
**Tests:** 60 passing

Before building the full lattice, create the selectional preference system that Phase 5 exposed as missing:

| Verb Class | Subject Requirement | Object Requirement |
|------------|--------------------|--------------------|
| `intentional_mental` (decide, believe, intend) | `animate` OR `organization` | - |
| `intentional_physical` (lift, throw, carry) | `animate` | `material_entity` |
| `communication` (announce, report, claim) | `animate` OR `organization` | `proposition` |
| `transfer` (give, allocate, assign) | `animate` OR `organization` | `continuant` |

**Deliverables:**
- `src/graph/SelectionalPreferences.js` - lookup table with verb→requirement mappings
- Extend `AmbiguityDetector._isIntentionalAct()` to use centralized preferences
- Add `cco:Organization` as valid agent for intentional acts (committees can "decide")

**Why First:** This fixes the "inanimate agent" false positives (ventilator ≠ rock) and provides foundation for plausibility scoring.

### 6.1 Ambiguity Resolution Strategy ✅ COMPLETE

**Status:** ✅ Complete (2026-01-26)
**Priority:** High
**Effort:** Medium
**Tests:** 46 passing

**Key Insight from Phase 5:** Not all ambiguities need multiple readings preserved. Define resolution strategy:

| Ambiguity Type | Resolution Strategy |
|----------------|---------------------|
| `selectional_violation` | Flag but DON'T create alternative (anomalous input) |
| `modal_force` | Preserve 2 readings if confidence < 0.8 |
| `noun_category` | Use context signals; preserve if "of" complement present |
| `scope` | Preserve 2 readings (semantic difference significant) |
| `potential_metonymy` | Flag with suggested reading; don't fork graph |

**Deliverables:**
- `src/graph/AmbiguityResolver.js` - decides which ambiguities to preserve
- Configuration: `{ preserveThreshold: 0.7, maxReadingsPerNode: 3 }`

### 6.2 Lattice Data Structure (Simplified) ✅ COMPLETE

**Status:** ✅ Complete (2026-01-26)
**Priority:** High
**Effort:** Medium
**Tests:** 55 passing

Based on Phase 5 learnings, simplify from original spec. Focus on **practical utility**:

```javascript
class InterpretationLattice {
  constructor(defaultGraph, ambiguities) {
    this.defaultReading = defaultGraph;     // The "best guess" graph
    this.ambiguities = ambiguities;         // Phase 5 AmbiguityReport
    this.alternativeReadings = [];          // Only for preserved ambiguities
    this.resolutionLog = [];                // Audit trail
  }

  // Primary API
  getDefaultReading()           // Returns defaultReading (most consumers use this)
  getAlternatives()             // Returns array of alternative interpretations
  getAmbiguitiesPreserved()     // Returns which ambiguities have multiple readings

  // Analysis API
  hasSignificantAmbiguity()     // True if any unresolved ambiguity
  getResolutionReasoning()      // Why each ambiguity was resolved/preserved

  // Serialization
  toJSONLD()                    // Full lattice as JSON-LD
  toSimplifiedGraph()           // Default reading only (backwards compatible)
}
```

**Key Simplification:** Don't build full lattice graph with subsumption relations upfront. Build alternative readings on-demand for specific ambiguity types.

**Deliverables:**
- `src/graph/InterpretationLattice.js`

### 6.3 Alternative Graph Generation ✅ COMPLETE

**Status:** ✅ Complete (2026-01-26)
**Priority:** Medium
**Effort:** Medium
**Tests:** 75 passing

For preserved ambiguities, generate alternative graph fragments:

```javascript
// Modal force ambiguity → two act interpretations
{
  defaultReading: {
    "@id": "inst:Act_123",
    "tagteam:actualityStatus": "tagteam:Prescribed",  // Deontic: obligation
    "tagteam:modality": "obligation"
  },
  alternativeReadings: [{
    "@id": "inst:Act_123_alt1",
    "tagteam:actualityStatus": "tagteam:Hypothetical", // Epistemic: expectation
    "tagteam:modality": "expectation",
    "tagteam:plausibility": 0.3,
    "tagteam:derivedFrom": { "@id": "inst:Act_123" }
  }]
}
```

**Deliverables:**
- `src/graph/AlternativeGraphBuilder.js` - creates variant nodes for ambiguities
- Ensure IRIs are unique but traceable (`_alt1`, `_alt2` suffixes)

### 6.4 SemanticGraphBuilder Integration + Deontic Enhancement ✅ COMPLETE

**Status:** ✅ Complete (2026-01-26)
**Priority:** High
**Effort:** Medium (builder integration + deontic vocabulary extension)
**Tests:** 72 passing

**Two Main Goals:**
1. **Builder Integration:** Wire up Phase 6 components (AmbiguityResolver, InterpretationLattice, AlternativeGraphBuilder) into SemanticGraphBuilder
2. **Deontic Enhancement:** Extend deontic vocabulary based on BFO-based deontic ontology research

**Deontic Coverage (Current vs Extended):**

| Deontic Concept | Modality | ActualityStatus | Status |
|-----------------|----------|-----------------|--------|
| Obligation | `obligation` | `tagteam:Prescribed` | ✅ Exists |
| Permission | `permission` | `tagteam:Permitted` | ✅ Exists |
| Prohibition | `prohibition` | `tagteam:Prohibited` | ✅ Exists |
| Claim/Right | `claim` | `tagteam:Entitled` | **New** |
| Power/Authority | `power` | `tagteam:Empowered` | **New** |
| Immunity | `immunity` | `tagteam:Protected` | **New** |

**Extended Deontic Markers:**
- Claim: "entitled", "has right", "deserves", "owed"
- Power: "authorized", "empowered", "delegates", "grants", "confers"
- Immunity: "exempt", "immune", "protected"
- Enhanced prohibition: "forbidden", "prohibited", "shall not", "not allowed"

Extend `build()` with opt-in lattice (builds on `detectAmbiguity: true`):

```javascript
build(text, options = {}) {
  // Phase 5: Detect ambiguities
  if (options.detectAmbiguity || options.preserveAmbiguity) {
    ambiguityReport = this.ambiguityDetector.detect(...);
  }

  // Phase 6: Resolve and optionally preserve
  if (options.preserveAmbiguity) {
    const resolutions = this.ambiguityResolver.resolve(ambiguityReport, options);
    const lattice = new InterpretationLattice(graph, resolutions);

    // Build alternative readings for preserved ambiguities
    for (const preserved of resolutions.preserved) {
      const altGraph = this.alternativeBuilder.build(graph, preserved);
      lattice.addAlternative(altGraph);
    }

    return {
      '@graph': lattice.getDefaultReading()['@graph'],
      _ambiguityReport: ambiguityReport,        // Phase 5 output (kept)
      _interpretationLattice: lattice,          // Phase 6 output (new)
      _metadata: { ... }
    };
  }

  // Backwards compatible
  return { '@graph': this.nodes, ... };
}
```

**API Options:**
```javascript
builder.build(text, {
  detectAmbiguity: true,        // Phase 5: flag ambiguities
  preserveAmbiguity: true,      // Phase 6: create alternative readings
  preserveThreshold: 0.7,       // Only preserve if confidence < threshold
  maxAlternatives: 3,           // Cap on alternative readings
  deonticVocabulary: 'extended' // 'basic' | 'extended' | 'hohfeldian'
});
```

**Test Coverage:** 72 tests across 8 categories
- Builder integration: 20 tests
- Deontic detection (basic + extended): 20 tests
- ActualityStatus mapping: 10 tests
- Graph output: 8 tests
- Edge cases: 8 tests
- Lattice integration: 6 tests

**Detailed Plan:** `planning/phase6/PHASE_6.4_IMPLEMENTATION_PLAN.md`

### 6.4.5 Ontology Validation ✅ COMPLETE

**Status:** ✅ Complete (2026-01-26)
**Priority:** High
**Effort:** Medium
**Tests:** 80 passing

Validate ontology files (JSON configs and TTL) before loading to prevent misclassifications and runtime errors.

**Two-Mode Operation:**

```javascript
// Option B: Validate on Load (Non-Blocking) - Default
const result = await TagTeam.loadOntology('./custom.json');
if (result._validation.hasWarnings()) {
  console.log(result._validation.warnings);
}

// Option C: Explicit Validation (Blocking Available)
const report = TagTeam.validateOntology('./custom.json');
if (report.hasErrors()) {
  console.log(report.errors);
  return; // Don't load
}
```

**Validation Layers:**

| Layer | Checks | Examples |
|-------|--------|----------|
| Structural | JSON syntax, required fields, types | Missing `domain`, invalid JSON |
| Semantic | IRI format, BFO/CCO types, hierarchy | Unknown prefix, Occurrent as Continuant |
| Compatibility | Conflicts with loaded ontologies | Term → different type, namespace collision |
| TagTeam-Specific | Verb overrides, type specs structure | Missing `default` key, invalid value def |

**Test Coverage:** 80 tests across 9 categories
- Basic validation: 10 tests
- Structural validation: 10 tests
- IRI validation: 10 tests
- BFO hierarchy validation: 10 tests
- Compatibility validation: 10 tests
- Verb override validation: 8 tests
- ValidationReport API: 8 tests
- Integration: 6 tests
- Edge cases: 8 tests

**Deliverables:**
- `src/graph/OntologyValidator.js` - validation engine ✅
- `src/graph/ValidationReport.js` - structured report ✅
- `src/data/bfo-cco-registry.js` - known types registry ✅
- Integration with DomainConfigLoader ✅

### Phase 6 Test Strategy

**Golden Corpus:** `tests/golden/interpretation-lattice.json`

```json
{
  "corpus": [
    {
      "id": "modal-001",
      "input": "The doctor should prioritize the younger patient",
      "expectedDefaultModality": "obligation",
      "expectedAlternatives": ["expectation"],
      "expectedPreserved": true
    },
    {
      "id": "scope-001",
      "input": "Not all patients received treatment",
      "expectedDefaultScope": "wide",
      "expectedAlternatives": ["narrow"],
      "expectedPreserved": true
    },
    {
      "id": "selectional-001",
      "input": "The rock decided to move",
      "expectedFlag": "selectional_violation",
      "expectedPreserved": false,
      "reason": "Anomalous input, not genuine ambiguity"
    }
  ]
}
```

### Phase 6 Lessons from Phase 5

1. **Test-first development** works well - write tests before implementation
2. **Opt-in flags** preserve backwards compatibility (`detectAmbiguity`, `preserveAmbiguity`)
3. **Surface data in multiple places** - both `_ambiguityReport` AND `@graph` nodes
4. **Handle both test and production data formats** - `entity.label` vs `entity['rdfs:label']`
5. **Incremental stakeholder feedback** catches issues early

---

## Phase 6.5: TTL Ontology Loading (IEE ValueNet Integration)

**Goal:** Enable loading of TTL/Turtle ontology files for value detection and type specialization

**Bundle Size Budget:** +75KB max (target: 5.025MB total)

**Priority:** High (IEE Integration Requirement)

**Motivation:** IEE's ValueNet ontology contains 100+ values based on Schwartz values and moral foundations, stored in TTL format. Current `DomainConfigLoader` only supports JSON configs. This phase enables direct ValueNet integration, potentially eliminating the need for `valueMapper.js` in IEE.

### Current Gap

```
Current (JSON only):
┌─────────────────┐     ┌─────────────────┐
│ DomainConfig    │ ←── │ medical.json    │  ✅ Works
│ Loader (JSON)   │     │ legal.json      │  ✅ Works
└─────────────────┘     │ value-net.ttl   │  ❌ Not supported
                        └─────────────────┘

Proposed (JSON + TTL):
┌─────────────────┐     ┌─────────────────┐
│ OntologyManager │ ←── │ medical.json    │  ✅ Works
│ (JSON + TTL)    │     │ valuenet.ttl    │  ✅ NEW
└─────────────────┘     │ iee-bridge.ttl  │  ✅ NEW
                        └─────────────────┘
```

### 6.5.1 Lightweight TTL Parser ✅ COMPLETE

**Status:** ✅ Complete (2026-01-26)
**Priority:** Critical
**Effort:** Medium
**Tests:** 80 passing

Created minimal Turtle parser for ontology loading (NOT full RDF library):

**Supported Constructs:**
| Construct | Example | Purpose |
|-----------|---------|---------|
| Prefixes | `@prefix vn: <...>` | Namespace resolution |
| Class declarations | `vn:Autonomy a bfo:Quality` | Value type mapping |
| Labels | `rdfs:label "Autonomy"` | Display names |
| Keywords | `ethics:keywords "choice, freedom"` | Pattern matching |
| Relationships | `ethics:ConflictsWith`, `owl:sameAs` | Value relationships |

**NOT Supported (out of scope):**
- Full OWL reasoning
- SPARQL queries
- Blank node complex structures
- RDF/XML format

**Deliverables:**
- `src/ontology/TurtleParser.js` - lightweight TTL parser ✅
- Support for `@prefix`, `a` (rdf:type), basic triples ✅
- Extract: classes, labels, keywords, relationships ✅
- ParseResult class with helper methods ✅
- toValueDefinition() for TagTeam format conversion ✅
- Error detection for malformed TTL ✅

**Test Coverage:** 80 tests across 9 categories
- Basic Parsing: 10 tests
- Prefix Parsing: 10 tests
- Triple Parsing: 10 tests
- Literal Parsing: 10 tests
- ValueNet Structure Extraction: 10 tests
- Relationship Extraction: 8 tests
- Error Handling: 8 tests
- IRI Resolution: 6 tests
- Integration & Performance: 8 tests

### 6.5.2 OntologyManager Class ✅ COMPLETE

**Status:** ✅ Complete (2026-01-26)
**Priority:** High
**Effort:** Medium
**Tests:** 80 passing

Unified ontology loading with caching:

```javascript
class OntologyManager {
  constructor(options = {}) {
    this.memoryCache = new Map();     // Hot cache
    this.loadedOntologies = [];       // Track sources
  }

  // Load from file path or URL
  async loadOntology(source) {
    // source: { path: './valuenet.ttl', format: 'turtle', namespace: 'vn' }
    // OR: { path: './medical.json', format: 'json', namespace: 'medical' }
  }

  // Load multiple ontologies with merge
  async loadOntologies(sources, options = { merge: true }) { }

  // Query loaded ontologies
  getValueDefinition(valueName) { }
  getTypeSpecialization(bfoType, term) { }
  getConflicts(valueName) { }
  getLoadedOntologies() { }
}
```

**Deliverables:**
- `src/ontology/OntologyManager.js` - unified loader ✅
- Format detection (JSON vs TTL by extension) ✅
- Merge strategy for overlapping definitions (last wins with warning) ✅
- Memory caching for performance ✅
- Query methods (getValueDefinition, findByKeyword, getConflicts) ✅
- Serialization (toJSON/fromJSON) for state persistence ✅

**Test Coverage:** 80 tests across 9 categories
- Constructor and Initialization: 8 tests
- Format Detection: 8 tests
- Loading TTL Ontologies: 10 tests
- Loading JSON Configs: 10 tests
- Memory Caching: 8 tests
- Merge Strategy: 8 tests
- Query Methods: 10 tests
- Clear and Reset: 6 tests
- Integration & Performance: 12 tests

### 6.5.3 ValueNet Integration ✅ COMPLETE

**Status:** ✅ Complete (2026-01-26)
**Priority:** High
**Effort:** Low
**Tests:** 50 passing

Map ValueNet TTL structure to TagTeam value detection:

**ValueNet TTL Structure:**
```turtle
@prefix vn: <https://fandaws.com/ontology/bfo/valuenet#> .
@prefix bfo: <http://purl.obolibrary.org/obo/BFO_> .

vn:SecurityDisposition a bfo:0000016 ;  # bfo:Disposition
    rdfs:label "Security" ;
    vn:keywords "safety, stability, protection" ;
    vn:upholdingTerms "protect, secure, safeguard" ;
    vn:violatingTerms "endanger, threaten, risk" .
```

**TagTeam Mapping:**
```javascript
// OntologyManager extracts:
{
  name: "SecurityDisposition",
  iri: "https://fandaws.com/ontology/bfo/valuenet#SecurityDisposition",
  bfoClass: "bfo:Disposition",
  keywords: ["safety", "stability", "protection"],
  upholdingTerms: ["protect", "secure", "safeguard"],
  violatingTerms: ["endanger", "threaten", "risk"]
}
```

**Deliverables:**
- `src/ontology/ValueNetAdapter.js` - ValueNet → ValueMatcher format adapter ✅
- Integration with existing `ValueMatcher.js` via `createValueMatcher()` ✅
- Format conversion (keywords → semanticMarkers, upholdingTerms/violatingTerms → polarityIndicators) ✅
- Conflict relationship extraction ✅
- Static `convert()` method for standalone use ✅

**Test Coverage:** 50 tests across 6 categories
- Constructor and Initialization: 6 tests
- Single Value Conversion: 10 tests
- Bulk Conversion: 8 tests
- ValueMatcher Integration: 10 tests
- Conflict Extraction: 8 tests
- Edge Cases and Static Methods: 8 tests

### 6.5.4 IEE Bridge Ontology Support ✅ COMPLETE

**Status:** ✅ Complete (2026-01-26)
**Priority:** Medium
**Effort:** Low
**Tests:** 54 passing

Support loading IEE's proposed bridge ontology that maps:
- TagTeam 50 values → ValueNet dispositions (owl:sameAs)
- ValueNet dispositions → IEE worldview values (ethics:mapsToWorldview)
- Related value associations (ethics:relatedTo)
- Category subsumption (ethics:subsumedBy)

```javascript
// Example usage
const loader = new BridgeOntologyLoader({ ontologyManager });
loader.loadFromString(bridgeTTL);

// Get full mapping chain: TagTeam → ValueNet → IEE
const chain = loader.getMappingChain('tagteam:Autonomy');
// { tagteamValue: 'tagteam:Autonomy',
//   valuenetDisposition: 'vn:AutonomyDisposition',
//   ieeWorldview: 'iee:SelfDirectionWorldview' }

// Resolve TagTeam value to full ValueNet definition
const resolved = loader.resolveValue('tagteam:Security');
// { keywords: ['safety', 'stability', 'protection'], ... }
```

**Deliverables:**
- `src/ontology/BridgeOntologyLoader.js` - bridge ontology loader ✅
- `owl:sameAs` equivalence handling (with symmetry) ✅
- `ethics:relatedTo` association handling ✅
- `ethics:mapsToWorldview` worldview mapping ✅
- `ethics:subsumedBy` subsumption handling ✅
- Custom predicate support ✅
- Batch operations and lookup tables ✅
- `examples/ontologies/iee-bridge-template.ttl` - example template ✅

**Test Coverage:** 54 tests across 11 categories
- Constructor and Initialization: 6 tests
- Loading Bridge Ontologies: 9 tests
- Equivalence Queries: 7 tests
- Related Value Queries: 5 tests
- Worldview Mapping: 5 tests
- Full Pipeline Integration: 4 tests
- Batch Operations: 4 tests
- Custom Predicates: 3 tests
- Error Handling: 4 tests
- Clear and Reset: 3 tests
- Statistics and Metadata: 4 tests

### Phase 6.5 API Design

```javascript
// NEW: Ontology loading API
TagTeam.loadOntology({
  source: 'file',           // 'file' | 'url' | 'object'
  path: './valuenet.ttl',   // File path or URL
  format: 'turtle',         // 'turtle' | 'json' (auto-detect if omitted)
  namespace: 'vn',          // Optional namespace prefix
  merge: true               // Merge with existing (default: true)
});

// Batch loading
TagTeam.loadOntologies([
  { path: './valuenet-core.ttl' },
  { path: './valuenet-schwartz.ttl' },
  { path: './config/medical.json' }
]);

// Query loaded ontologies
TagTeam.getLoadedOntologies();
// [{ namespace: 'vn', format: 'turtle', valueCount: 100 }, ...]

// Clear and reload
TagTeam.clearOntologies();
```

### Phase 6.5 Test Strategy

**Test Corpus:** `tests/ontology/ttl-loading.test.js`

| Test Category | Count | Description |
|---------------|-------|-------------|
| TTL parsing | 20 | Prefix, triples, labels, keywords |
| JSON fallback | 10 | Existing config files still work |
| Merge behavior | 10 | Multiple ontologies, conflict handling |
| ValueNet integration | 15 | IEE value detection with loaded ontology |
| Performance | 5 | Cache hits, load times |

**Success Criteria:**
- Load ValueNet TTL in < 500ms
- Cached load < 10ms
- Detect 95%+ of ValueNet values in IEE test corpus
- Zero regression on existing JSON config tests

### Phase 6.5 Files

```
src/ontology/
├── TurtleParser.js         # Lightweight TTL parser ✅
├── OntologyManager.js      # Unified loader with caching ✅
├── ValueNetAdapter.js      # ValueNet → TagTeam mapping ✅
└── BridgeOntologyLoader.js # IEE bridge ontology loader ✅

tests/unit/phase6/
├── turtle-parser.test.js          # Parser tests (80 tests) ✅
├── ontology-manager.test.js       # Loader tests (80 tests) ✅
├── valuenet-adapter.test.js       # Adapter tests (50 tests) ✅
└── bridge-ontology-loader.test.js # Bridge tests (54 tests) ✅

examples/ontologies/
├── valuenet-example.ttl    # Example ValueNet fragment
└── iee-bridge-template.ttl # Bridge ontology template ✅
```

---

## Phase 6.6: OntologyTextTagger — General-Purpose Ontology-Driven Text Tagging

**Goal:** Enable any team to load their own ontology (TTL or JSON) and tag text with their custom classes, without requiring ValueNet-specific property conventions.

**Status:** ✅ Complete (2026-01-27)
**Priority:** High
**Effort:** Medium
**Tests:** 64 passing
**Depends On:** Phase 6.5 (TurtleParser, OntologyManager)

### Problem Statement

Phase 6.5 delivers a pipeline that is hardcoded to the ValueNet property schema:

```
TTL → TurtleParser → OntologyManager → ValueNetAdapter → ValueMatcher
                                         ↑ hardcoded:
                                         vn:keywords → semanticMarkers
                                         vn:upholdingTerms → polarity.upholding
                                         vn:violatingTerms → polarity.violating
                                         rdf:type = bfo:0000016 (Disposition)
```

A new team with a different ontology (e.g., medical, legal, environmental) cannot use this pipeline unless they restructure their ontology to match ValueNet conventions. We need a configurable adapter that maps arbitrary ontology properties to TagTeam's text-matching engine.

### Design: Property Mapping Schema

The core idea is a **mapping configuration** that tells the tagger which ontology properties serve which roles in text detection:

```javascript
const tagger = new OntologyTextTagger({
  // Required: OntologyManager with loaded TTL/JSON
  ontologyManager: manager,

  // Property mapping — tells the tagger what to look for
  propertyMap: {
    // Which property holds the matching keywords/terms
    // (equivalent to ValueNet's vn:keywords)
    keywords: 'myns:searchTerms',

    // Which property holds the human-readable label
    // Default: 'rdfs:label'
    label: 'rdfs:label',

    // Which rdf:type(s) to consider as taggable classes
    // Default: all typed subjects
    // Can be a string or array of strings
    typeFilter: 'myns:TaggableEntity',

    // Optional: polarity indicators (for value-like ontologies)
    upholding: 'myns:positiveIndicators',
    violating: 'myns:negativeIndicators',

    // Optional: category/classification property
    // Allows grouping tagged instances under broader categories
    category: 'myns:belongsToCategory',

    // Optional: description for context
    description: 'rdfs:comment',

    // Optional: additional properties to extract and attach to results
    // These are passed through as metadata on each match
    extraProperties: ['myns:severity', 'myns:source', 'myns:exampleUsage']
  },

  // Optional: matching configuration
  matchOptions: {
    caseSensitive: false,         // default: false
    wordBoundary: true,           // default: true (use \b regex)
    partialMatch: false,          // default: false
    lemmatize: true,              // default: true (use PatternMatcher)
    minKeywordMatches: 1,         // default: 1 (min keywords to count as match)
    confidenceThreshold: 0.0      // default: 0.0 (return all matches)
  },

  // Optional: domain label for output
  domain: 'environmental-law'
});
```

### API Surface

```javascript
// === Construction ===

// From OntologyManager (TTL already loaded)
const tagger = new OntologyTextTagger({ ontologyManager, propertyMap });

// From raw TTL string (convenience — creates internal OntologyManager)
const tagger = OntologyTextTagger.fromTTL(ttlString, { propertyMap });

// From JSON config (for teams not using TTL)
const tagger = OntologyTextTagger.fromJSON(jsonConfig, { propertyMap });


// === Tagging ===

// Tag text — returns array of matches
const tags = tagger.tagText('The factory discharged effluent into the river.');
// [
//   {
//     class: 'env:WaterPollution',
//     label: 'Water Pollution',
//     category: 'env:EnvironmentalHarm',
//     confidence: 0.85,
//     evidence: ['discharged', 'effluent', 'river'],
//     keywordCount: 3,
//     polarity: -1,                    // only if polarity properties mapped
//     domain: 'environmental-law',
//     iri: 'https://env.org/ontology#WaterPollution',
//     metadata: {                      // from extraProperties
//       severity: 'high',
//       source: 'EPA Clean Water Act'
//     }
//   }
// ]

// Tag with specific class filter
const tags = tagger.tagText(text, { classes: ['env:WaterPollution', 'env:AirPollution'] });

// Tag and group by category
const grouped = tagger.tagTextGrouped(text);
// {
//   'env:EnvironmentalHarm': [ ...matches ],
//   'env:RegulatoryViolation': [ ...matches ]
// }


// === Introspection ===

// List all taggable classes from the loaded ontology
const classes = tagger.getTaggableClasses();
// [
//   { id: 'env:WaterPollution', label: 'Water Pollution', category: 'env:EnvironmentalHarm',
//     keywordCount: 5, hasPolarity: false },
//   ...
// ]

// Get the compiled tag definition for a single class
const def = tagger.getTagDefinition('env:WaterPollution');

// Get summary statistics
const stats = tagger.getStats();
// { classCount: 12, totalKeywords: 87, withPolarity: 4, categories: 3 }

// Validate the property map against the loaded ontology
// (check that mapped properties actually exist in the data)
const validation = tagger.validatePropertyMap();
// {
//   valid: true,
//   warnings: ['myns:severity found on 3/12 classes only'],
//   errors: [],
//   coverage: { keywords: 12/12, category: 8/12, severity: 3/12 }
// }


// === Export / Integration ===

// Export as ValueMatcher-compatible format (backwards compatibility)
const vmFormat = tagger.toValueMatcherFormat();
// { values: [...], version: '6.6', source: 'environmental-law' }

// Create a ValueMatcher directly (for teams that need the existing pipeline)
const matcher = tagger.createValueMatcher();

// Export tag definitions as JSON (for sharing/caching)
const json = tagger.exportDefinitions();
```

### Example: Medical Ontology

```turtle
@prefix med: <https://example.org/medical#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix bfo: <http://purl.obolibrary.org/obo/BFO_> .

med:CardiovascularDisease a bfo:0000016 ;
    rdfs:label "Cardiovascular Disease" ;
    med:indicators "chest pain, shortness of breath, heart attack, stroke, hypertension" ;
    med:icdCode "I00-I99" ;
    med:riskFactors "smoking, obesity, diabetes, high cholesterol" ;
    med:category med:ChronicDisease .

med:RespiratoryInfection a bfo:0000016 ;
    rdfs:label "Respiratory Infection" ;
    med:indicators "cough, fever, congestion, pneumonia, bronchitis" ;
    med:icdCode "J00-J99" ;
    med:category med:AcuteDisease .
```

```javascript
const tagger = OntologyTextTagger.fromTTL(medicalTTL, {
  propertyMap: {
    keywords: 'med:indicators',
    category: 'med:category',
    extraProperties: ['med:icdCode', 'med:riskFactors']
  },
  domain: 'medical'
});

const tags = tagger.tagText('Patient presents with chest pain and shortness of breath.');
// [{ class: 'med:CardiovascularDisease', label: 'Cardiovascular Disease',
//    evidence: ['chest pain', 'shortness of breath'], keywordCount: 2,
//    metadata: { icdCode: 'I00-I99', riskFactors: 'smoking, obesity, ...' } }]
```

### Example: Legal Ontology

```turtle
@prefix legal: <https://example.org/legal#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

legal:ContractBreach a legal:LegalConcept ;
    rdfs:label "Breach of Contract" ;
    legal:searchTerms "breach, violated agreement, failed to perform, non-performance" ;
    legal:positiveResolution "cure, remedy, settlement, mediation" ;
    legal:negativeOutcome "damages, penalty, termination, liability" ;
    legal:jurisdiction "common-law" ;
    legal:category legal:ContractLaw .
```

```javascript
const tagger = OntologyTextTagger.fromTTL(legalTTL, {
  propertyMap: {
    keywords: 'legal:searchTerms',
    typeFilter: 'legal:LegalConcept',
    upholding: 'legal:positiveResolution',
    violating: 'legal:negativeOutcome',
    category: 'legal:category',
    extraProperties: ['legal:jurisdiction']
  },
  domain: 'legal'
});
```

### Internal Architecture

```
                    ┌─────────────────────────┐
                    │   OntologyTextTagger     │
                    │                          │
  TTL/JSON ────────►│  propertyMap config      │
                    │         │                │
                    │         ▼                │
                    │  ┌──────────────┐        │
                    │  │ PropertyMapper│        │  Reads ontology triples,
                    │  │ (new class)  │        │  applies propertyMap to
                    │  └──────┬───────┘        │  extract tag definitions
                    │         │                │
                    │         ▼                │
                    │  ┌──────────────┐        │
                    │  │ TagDefinition │        │  Normalized internal format:
                    │  │[] (array)    │        │  { id, label, keywords[],
                    │  └──────┬───────┘        │    polarity?, category?, meta }
                    │         │                │
                    │         ▼                │
  text ────────────►│  ┌──────────────┐        │
                    │  │  TextMatcher  │        │  Reuses ValueMatcher's
                    │  │  (internal)   │        │  matching algorithm
                    │  └──────┬───────┘        │
                    │         │                │
                    │         ▼                │
                    │    TagResult[]           │
                    └─────────────────────────┘
```

**Key design decisions:**

1. **PropertyMapper** — New internal class that reads triples from OntologyManager/TurtleParser using the configured property map. This is the generalization of what ValueNetAdapter does with hardcoded properties.

2. **TagDefinition** — Internal normalized format. Structurally identical to ValueMatcher's input format but with added `category` and `metadata` fields. This means we can delegate to the existing matching algorithm.

3. **TextMatcher** — Wraps or reuses ValueMatcher's regex + PatternMatcher approach. No need to rewrite the matching engine; we just need to feed it differently-shaped definitions.

4. **Backwards compatibility** — `toValueMatcherFormat()` and `createValueMatcher()` ensure teams can drop OntologyTextTagger into existing ValueMatcher-based pipelines.

### Deliverables

| File | Description |
|------|-------------|
| `src/ontology/OntologyTextTagger.js` | Main class with property mapping, tagging, introspection ✅ |
| `src/ontology/PropertyMapper.js` | Internal: maps ontology triples to TagDefinitions via config ✅ |
| `tests/unit/phase6/ontology-text-tagger.test.js` | Test suite (64 tests) ✅ |
| `examples/ontologies/medical-example.ttl` | Example: medical domain ontology ✅ |
| `examples/ontologies/legal-example.ttl` | Example: legal domain ontology ✅ |
| `demos/phase66-custom-tagger-demo.html` | Interactive demo: paste TTL, configure mapping, tag text |

### Test Coverage: 64 tests across 9 categories

| Category | Count | Description |
|----------|-------|-------------|
| Constructor & Config | 8 | Valid/invalid propertyMap, defaults, convenience factories |
| Property Mapping | 10 | Keyword extraction, label fallback, type filtering, extra properties |
| Text Tagging | 12 | Single class, multiple classes, evidence, confidence, polarity |
| Category Grouping | 6 | tagTextGrouped, category extraction, uncategorized handling |
| Match Options | 8 | Case sensitivity, word boundary, partial match, min keywords |
| Introspection | 6 | getTaggableClasses, getStats, validatePropertyMap |
| Export & Compat | 5 | toValueMatcherFormat, createValueMatcher, exportDefinitions |
| Edge Cases | 4 | Empty ontology, missing properties, no data, cross-domain |
| PropertyMapper | 5 | Constructor, extraction, validation, coverage reporting |

### Success Criteria

- Any TTL ontology with keyword-bearing properties can drive text tagging without code changes
- Property map validation catches misconfigurations before runtime
- Existing ValueNet pipeline continues to work unchanged (zero regression)
- Demo page allows paste-your-own-TTL with live property mapping configuration
- Performance: tagging 1000 words against 50 classes < 100ms

### Phase 6.6 Files

```
src/ontology/
├── OntologyTextTagger.js   # Main general-purpose tagger ✅
└── PropertyMapper.js       # Property map → TagDefinition converter ✅

tests/unit/phase6/
└── ontology-text-tagger.test.js  # 64 tests ✅

examples/ontologies/
├── medical-example.ttl     # Medical domain example ✅
└── legal-example.ttl       # Legal domain example ✅

demos/
└── phase66-custom-tagger-demo.html  # Interactive demo (planned)
```

---

## v1/v2 Scope Contract (2026-01-28)

> **TagTeam.js is an intake compiler, not an AI.**
> Its job is to deterministically map standard linguistic inputs into ontology-aligned semantic structures — not to understand everything.
> Success is measured by correctness and predictability, not coverage.

### v1: Stabilization / Semantic Intake Engine

**Mission:** Produce correct, deterministic semantic graphs for single-clause and minimally compound sentences, with explicit uncertainty when structure cannot be resolved.

**Architectural constraints:** Flat/shallow parsing only. No discourse memory. No cross-clause normalization. No cross-sentence inference. When ambiguous: do not guess.

**v1 IN SCOPE (locked):**
- Passive voice transformations (active ↔ passive, agent demotion/promotion)
- Verb-context object typing / selectional restrictions (ENH-001)
- Implicit agent for imperatives (ENH-003, partial — no directive ICE nodes)
- Prepositional phrase role discrimination: with→Instrument, for→Beneficiary, to→Recipient (ENH-015, bounded)
- Ergative verb agent demotion on hardcoded allowlist, inanimate subjects only (ENH-008, bounded)
- All existing passing capabilities frozen: simple declaratives, active/passive/middle voice, basic ditransitives, direct/indirect objects, oblique arguments

**v1 EXPLICITLY DEFERRED to v2:**
- Question/Directive ICE nodes (ENH-002, ENH-004)
- Exclamatory/ValueAssertion semantics (ENH-005)
- Conditional logic (ENH-006)
- Compound/complex/compound-complex clause linking (ENH-007)
- Temporal relations (ENH-009)
- Abstract anaphora (ENH-010)
- Clausal subjects (ENH-011)
- Psych verbs (ENH-012)
- Causative constructions (ENH-013)
- Wh-movement & do-support (ENH-014)
- Expletive "it" constructions (ENH-016)
- Raising verbs (ENH-017)

### v2: Structural Semantics & Normalization

**Mission:** Normalize surface syntax into semantically scoped clauses and speech acts before semantic compilation. v2 prepares normalized input; v1 compiles it.

**v2 introduces:** Clause segmentation, structural normalization, ICE wrapper nodes (Question, Directive, Conditional, ValueAssertion), verb-class routing (raising, psych, causative), scoped temporal and causal relations, limited discourse memory.

See [enhancements_from_tests.md](enhancements_from_tests.md) for full enhancement details with `[v1]`/`[v2]` scope tags.

---

## Phase 7: Epistemic Layer

**Goal:** Support epistemic status analysis for ethical reasoning

**Bundle Size Budget:** +50KB max (target: 5.15MB total)

**Scope Definition:** This phase focuses on *detecting* epistemic markers in text, NOT implementing a full epistemology framework. The goal is structured metadata that downstream consumers can use.

### Phase Scope Legend

| Marker | Meaning |
|--------|---------|
| ✅ v1-Core | Fully in scope for v1 stabilization |
| ✅ v1-Complete | Already implemented, no further v1 work |
| 🟡 v1-Limited | Partial v1 scope with bounded implementation |
| 🟢 v1-Optional | Nice-to-have, not blocking v1 |
| 🔜 v2-Only | Deferred entirely to v2 |
| ❌ Defer Entirely | Post-v2 or indefinitely deferred |

### 7.1 Source Attribution Detection — 🟡 v1-Limited / v2-Expanded

**Status:** ✅ Complete (2026-01-28)
**Priority:** High
**Effort:** Medium
**Scope:** v1 = detect quoted speech attribution only; v2 = reported speech, institutional sources, evidential chains
**Tests:** 39 passing (source-attribution.test.js)

Detect and structure attribution patterns in text:

**Detection Patterns:**
| Pattern | Example | Output |
|---------|---------|--------|
| Quote attribution | `"X," said Dr. Smith` | `{ source: "Dr. Smith", type: "direct_quote" }` |
| Reported speech | `The nurse reported that...` | `{ source: "nurse", type: "reported" }` |
| Institutional | `Hospital policy states...` | `{ source: "hospital", type: "institutional" }` |

**Output Structure:**
```json
{
  "claim": "The patient should receive treatment",
  "attribution": {
    "detectedSource": "physician",
    "sourceType": "cco:Physician",
    "attributionType": "direct_quote",
    "confidence": 0.85
  }
}
```

**Deliverables:**
- `src/graph/SourceAttributionDetector.js` - pattern-based detection
- Detection patterns for 5 common attribution types
- Extended @context vocabulary

**NOT in scope:** Full evidential reasoning chains, multi-hop attribution

### 7.2 Certainty Markers — ✅ v1-Core

**Status:** ✅ Complete (2026-01-28)
**Priority:** Medium
**Effort:** Low
**Scope:** Lexical hedges/boosters within single clauses. No cross-clause evidential reasoning.
**Tests:** 24 passing (certainty-analyzer.test.js)

Detect hedges and boosters via lexical patterns:

| Marker Type | Examples | Effect |
|-------------|----------|--------|
| Hedges | "might", "possibly", "seems" | Reduce certainty |
| Boosters | "definitely", "clearly", "must" | Increase certainty |
| Evidentials | "reportedly", "allegedly" | Mark as reported |

**Deliverables:**
- `src/analyzers/CertaintyAnalyzer.js` - lexicon-based detection
- Certainty vocabulary in @context
- ~50 marker terms in lexicon

### 7.3 Temporal Grounding — 🔜 v2-Only

**Status:** Not started
**Priority:** Medium
**Effort:** Medium
**Scope:** Requires discourse memory and cross-clause temporal relation resolution. Deferred entirely to v2.

Add explicit referenceTime support for relative temporal expressions:

```javascript
builder.build(text, {
  referenceTime: '2026-01-19T00:00:00Z',
  documentDate: '2026-01-15T00:00:00Z'
});

// Resolves: "last week" → 2026-01-12 to 2026-01-19
// Resolves: "yesterday" → 2026-01-18
```

**Deliverables:**
- `src/graph/TemporalGrounder.js` - relative time resolution
- Support for: yesterday/today/tomorrow, last/next week/month, N days ago
- Temporal resolution in entity extraction

**NOT in scope:** Complex temporal reasoning, event ordering

---

## Phase 8: Enhanced Disambiguation

**Goal:** Improve accuracy using context and iteration

### 8.1 Noun Ambiguity Resolution — 🔜 v2-Only

**Status:** Not started
**Priority:** Medium
**Effort:** Medium
**Scope:** Requires cross-clause context signals (e.g., "during X"). Deferred to v2.

| Signal | Interpretation | Example |
|--------|---------------|---------|
| "the X" + verb phrase | Continuant | "The organization hired..." |
| "X of Y" | Process | "Organization of files..." |
| "during X" | Occurrent | "During treatment..." |

### 8.2 Iterative Verb Refinement — 🔜 v2-Only

**Status:** Not started
**Priority:** Low
**Effort:** Medium
**Scope:** Multi-pass disambiguation requires architectural changes. Deferred to v2.

Multi-pass disambiguation:
```
Pass 1: Selectional restrictions (current)
Pass 2: ContextDimension scores
Pass 3: ActualityStatus consistency
```

### 8.3 Evaluate Wink NLP — ❌ Defer Entirely (Post-v2)

**Status:** Not started
**Priority:** Low
**Effort:** Medium
**Scope:** External NLP library evaluation deferred indefinitely. Phase 5 custom implementations sufficient. Only revisit if v2 requirements expose gaps that cannot be addressed by custom code.

If Phase 5 improvements insufficient, evaluate Wink NLP:
- +600KB bundle size
- Better tokenization
- Named entity recognition
- Sentiment (may help with ethical valence)

---

## Phase 8.5: Linguistic Feature Gaps (Test-Driven)

**Goal:** Address specific parsing gaps identified by comprehensive test suite

**Status:** ✅ Complete (2026-01-28)
**Priority:** High (blocks 86% → 95%+ test pass rate)
**Effort:** Low-Medium

These enhancements are derived from failing P0 tests and represent concrete, bounded improvements.

### 8.5.1 Definiteness Tracking Enhancement — ✅ v1-Core

**Status:** ✅ Complete
**Priority:** High
**Effort:** Low
**Scope:** Single-NP definiteness detection. No cross-clause coreference.
**Tests:** 13 passing (definite-np.test.js), 10 passing (declarative.test.js)

Current `tagteam:definiteness` only works for simple "the X" patterns. Extend to handle:

| Pattern | Example | Expected Definiteness |
|---------|---------|----------------------|
| "the last X" | "the last ventilator" | definite |
| "the only X" | "the only option" | definite |
| "the critically ill X" | "the critically ill patient" | definite |
| Proper names | "Dr. Smith" | definite (inherent) |

**Deliverables:**
- Modify `src/graph/EntityExtractor.js` - extend definiteness detection
- Handle adjective/modifier sequences before head noun
- Proper name detection (capitalized NPs without determiner)

**Test File:** `tests/linguistic/referents/definiteness/definite-np.test.js`

### 8.5.2 Extended Modal Detection — ✅ v1-Core

**Status:** ✅ Complete
**Priority:** High
**Effort:** Low
**Scope:** Lexical modal expansion. No conditional/subjunctive mood.
**Tests:** 12 passing (deontic-obligation.test.js)

Current modal detection misses some obligation markers:

| Modal | Current Status | Fix Required |
|-------|---------------|--------------|
| "must" | ✅ Working | - |
| "shall" | ❌ Maps to Actual | Add to obligation modals |
| "have to" | ❌ Not detected | Multi-word modal detection |
| "need to" | ✅ Working | - |

**Deliverables:**
- Modify `src/graph/ActExtractor.js` - add "shall" to DEONTIC_MODALS
- Modify `src/graph/DirectiveExtractor.js` - ensure multi-word modal patterns match

**Test File:** `tests/linguistic/verbphrase/modality/deontic-obligation.test.js`

### 8.5.3 Domain Vocabulary Expansion — ✅ v1-Core

**Status:** ✅ Complete
**Priority:** Medium
**Effort:** Low
**Scope:** Medical domain config updates only. No new domain configs in v1.
**Tests:** 14 passing (person.test.js)

Add missing terms to medical domain config:

| Term | Expected Mapping | Current Status |
|------|-----------------|----------------|
| "surgeon" | cco:Person | ❌ Falls back to bfo:MaterialEntity |
| "committee" | cco:GroupOfPersons | ❌ Not recognized |
| "board" | cco:GroupOfPersons | ❌ Not recognized |

**Deliverables:**
- Update `config/medical.json` - add surgeon, committee, board
- Add group entity patterns to EntityExtractor

**Test File:** `tests/ontology/cco-mapping/agents/person.test.js`

### 8.5.4 Scarcity Marker Detection — 🟡 v1-Limited

**Status:** ✅ Complete
**Priority:** Medium
**Effort:** Low
**Scope:** v1 = basic scarcity adjective detection ("last", "only", "remaining"). No scarcity reasoning or inference.
**Tests:** Passing (definite-np.test.js - scarcity marker tests included)

Detect scarcity/uniqueness markers that affect resource allocation analysis:

| Marker | Example | Scarcity Property |
|--------|---------|-------------------|
| "the last" | "the last ventilator" | `tagteam:scarcityMarker: "last"` |
| "the only" | "the only option" | `tagteam:scarcityMarker: "only"` |
| "the remaining" | "the remaining supplies" | `tagteam:scarcityMarker: "remaining"` |

**Deliverables:**
- Modify `src/graph/EntityExtractor.js` - detect scarcity modifiers
- Add `tagteam:scarcityMarker` to entity nodes
- Update JSONLDSerializer @context

**Test File:** `tests/linguistic/referents/definiteness/definite-np.test.js`

### Test Coverage Impact — ✅ Complete

| Enhancement | Tests Passing | Status |
|-------------|---------------|--------|
| 8.5.1 Definiteness | 23 (13 + 10) | ✅ |
| 8.5.2 Modal Detection | 12 | ✅ |
| 8.5.3 Vocabulary | 14 | ✅ |
| 8.5.4 Scarcity Markers | included | ✅ |
| **Combined** | **49+** | **✅ Complete** |

---

## Phase 9: Validation Layer

**Goal:** Robust internal and external validation

### 9.1 Internal Self-Assessment — ✅ v1-Core

**Status:** Partial (SHACL done)
**Priority:** Medium
**Effort:** Low
**Scope:** Self-assessment metrics already implemented. v1-complete.

What TagTeam can reliably know about itself:
- Configuration state (ontologies loaded, domain configs active)
- Processing metrics (parse success/failure, unknown terms)
- Coverage (% of input that produced output)

### 9.2 External SHACL Validation — ✅ v1-Complete

**Status:** ✅ Complete (SHMLValidator)
**Priority:** N/A
**Scope:** Already implemented with 8 expert-certified patterns. v1-complete.

Already implemented:
- 8 expert-certified patterns
- Domain plausibility checks
- Role bearer constraints

### 9.3 Combined Validation Report — 🟢 v1-Optional

**Status:** ✅ Complete (2026-01-28)
**Priority:** Low
**Effort:** Low
**Scope:** Nice-to-have unified report format. Not blocking for v1.
**Tests:** 32 tests in `tests/unit/phase9/combined-validation-report.test.js`
**Module:** `src/graph/CombinedValidationReport.js` — weighted scoring (SHACL 35%, coverage 25%, budget 15%, ambiguity 15%, completeness 10%), grades A-F, human-readable format output. Integrated into SemanticGraphBuilder via `validate()` method.

Unified report format:
```json
{
  "validation": {
    "internal": { "selfAssessmentScore": 0.85 },
    "external": { "shaclValidationScore": 0.92 },
    "combined": { "overallScore": 0.88, "recommendation": "..." }
  }
}
```

---

## Phase 10: Human Validation Loop — 🔜 v2-Only (Design-Only in v1)

**Goal:** Enable expert correction workflow

**Status:** Not Started - Requires IEE (Institute for Ethical Engineering) team input

**v1 Scope:** Design data model only (no implementation). Define JSON-LD vocabulary for validation events.
**v2 Scope:** Full implementation of validation event builder and supersession chains.

**Scope:** Define data model for human corrections. TagTeam does NOT implement UI—consumers build their own validation interfaces using this data model.

### 10.1 Validation Data Model

**Assertion Types:**
```javascript
// Human validates machine assertion
{
  "@type": "tagteam:HumanValidationEvent",
  "tagteam:validates": "inst:Autonomy_ValueAssertion_abc123",
  "tagteam:validator": "inst:Expert_Jane_Doe",
  "tagteam:validationStatus": "tagteam:Confirmed",  // Confirmed | Rejected | Modified
  "tagteam:timestamp": "2026-01-19T..."
}

// Human rejects false positive
{
  "@type": "tagteam:HumanRejectionEvent",
  "tagteam:rejects": "inst:Justice_ValueAssertion_def456",
  "tagteam:rejectionReason": "Value not present in context",
  "tagteam:validator": "inst:Expert_Jane_Doe"
}

// Human provides correction
{
  "@type": "tagteam:HumanCorrectionEvent",
  "tagteam:corrects": "inst:Beneficence_ValueAssertion_ghi789",
  "tagteam:supersedes": "inst:Autonomy_ValueAssertion_abc123",
  "tagteam:correctionNote": "Should be classified as Beneficence, not Autonomy"
}
```

### 10.2 Supersession Chain

Track correction history:
```
Original → Correction1 → Correction2 (current)
           supersedes    supersedes
```

**Deliverables:**
- `src/graph/HumanValidationBuilder.js` - creates validation event nodes
- @context vocabulary for validation types
- `tagteam:supersedes` chain for tracking correction history
- API: `builder.recordValidation(assertionId, validatorId, status)`

---

## Phase 11: Extended Domain Support — ✅ Medical v1 / 🔜 Others v2

**Goal:** Expand to additional domains

**Scope:** Medical domain config is v1-complete. Additional domains (legal, business, scientific) deferred to v2.

| Domain | Config File | Status | Scope |
|--------|-------------|--------|-------|
| Medical | `config/medical.json` | ✅ Complete | ✅ v1 |
| Legal | `config/legal.json` | Not started | 🔜 v2 |
| Business | `config/business.json` | Not started | 🔜 v2 |
| Scientific | `config/scientific.json` | Not started | 🔜 v2 |

---

## Test Strategy for Ambiguity Preservation

**Goal:** Ensure lattice correctness through golden test corpus

### Golden Corpus Requirements

Create `tests/golden/ambiguity-corpus.json` with:

```json
{
  "corpus": [
    {
      "id": "deontic-epistemic-001",
      "input": "The doctor should prioritize the younger patient",
      "expectedReadings": [
        { "type": "deontic", "gloss": "obligation to prioritize" },
        { "type": "epistemic", "gloss": "expectation of prioritizing" }
      ],
      "expectedDefault": "deontic",
      "minReadings": 2,
      "maxReadings": 3
    }
  ]
}
```

### Test Categories

| Category | Test Count | Example |
|----------|------------|---------|
| Deontic/Epistemic modals | 10 | "should", "must", "ought to" |
| Noun process/continuant | 10 | "organization", "treatment" |
| Verb sense ambiguity | 10 | "provide care" vs "provide equipment" |
| Scope ambiguity | 5 | "not all patients", "every doctor" |
| PP attachment | 5 | "treated the patient with care" |

### Validation Criteria

1. **Reading count:** `minReadings <= actual <= maxReadings`
2. **Reading types:** All `expectedReadings` types present
3. **Default selection:** `defaultReading` matches `expectedDefault`
4. **Plausibility ordering:** Higher-plausibility readings ranked first

### Test Commands

```bash
node tests/unit/test-lattice-golden.js      # Golden corpus validation
node tests/unit/test-lattice-properties.js  # Property-based tests
```

---

## Bundle Size Trajectory

| Phase | Component | Size Delta | Cumulative | Status |
|-------|-----------|------------|------------|--------|
| Phase 4 | Core + Graph | - | 4.8 MB | ✅ Complete |
| Phase 5 | NLP upgrades | +50 KB | 4.85 MB | ✅ Complete (under budget!) |
| Phase 6 | Lattice | +100 KB | 4.95 MB | Planned |
| Phase 6.5 | TTL/Ontology Loading | +75 KB | 5.025 MB | Planned |
| Phase 7 | Epistemic | +50 KB | 5.075 MB | Planned |
| Phase 8-9 | Disambiguation + Validation | +50 KB | 5.125 MB | Planned |
| **Target Max** | - | - | **6.0 MB** | - |

**Phase 5 Size Success:** Stayed well under +200KB budget by using custom implementations instead of external libraries.

**Size Management Strategies:**
- Tree-shaking unused code paths
- Lazy loading of domain configs
- Custom implementations over external libraries (proven in Phase 5)

---

## Implementation Priority Matrix

| Phase | Priority | Effort | Dependencies | Enables | Status |
|-------|----------|--------|--------------|---------|--------|
| **5.0** NLP Library Eval | Critical | Low | None | 5.1, 5.2, 5.3 | ✅ Complete |
| **5.1** Core NLP Modules | High | Low | 5.0 | 5.2, 5.3 | ✅ Complete |
| **5.2** Phrase Extractors | High | Medium | 5.0, 5.1 | 5.3, 6.x | ✅ Complete |
| **5.3** Ambiguity Detection | High | Medium | 5.2 | 6.x | ✅ Complete |
| **6.0** Selectional Preferences | Critical | Low | 5.3 | 6.1, 6.2 | ✅ Complete |
| **6.1** Ambiguity Resolver | High | Medium | 6.0 | 6.2, 6.3 | ✅ Complete |
| **6.2** Lattice Data Structure | High | Medium | 6.1 | 6.3, 6.4 | ✅ Complete |
| **6.3** Alternative Graph Builder | Medium | Medium | 6.2 | 6.4 | ✅ Complete |
| **6.4** Builder Integration + Deontic | High | Medium | 6.2, 6.3 | 6.4.5 | ✅ Complete |
| **6.4.5** OntologyValidator | High | Medium | 6.4 | 6.5 | ✅ Complete |
| **6.5.1** TTL Parser | High | Medium | 6.4.5 | 6.5.2 | ✅ Complete |
| **6.5.2** OntologyManager | High | Medium | 6.5.1 | 6.5.3 | ✅ Complete |
| **6.5.3** ValueNet Integration | High | Low | 6.5.2 | IEE | ✅ Complete |
| **6.6** OntologyTextTagger | High | Medium | 6.5 | 7.x, Demo | ✅ Complete |
| **7.1** Source Attribution | High | Medium | 6.4 | 7.2 | Planned |
| **7.2** Certainty Markers | Medium | Low | 7.1 | - | Planned |
| **7.3** Temporal Grounding | Medium | Medium | 6.4 | - | Planned |
| **8.x** Disambiguation | Low | Medium | 6.4 | - | Planned |
| **9.x** Validation | Low | Low | 6.4 | - | Planned |
| **10** Human Validation | Medium | Medium | 6.4 | - | Planned |
| **11** Domain Support | Low | Low | None | - | Planned |

---

## Recommended Implementation Sequence

### ✅ Complete

1. **Phase 5.0:** NLP Library evaluation → Custom implementation chosen
2. **Phase 5.1:** Core NLP (Lemmatizer, ContractionExpander) → 149 tests
3. **Phase 5.2:** Phrase extractors (VP, NP) → 59 tests
4. **Phase 5.3:** Ambiguity detection → 71 tests
5. **Phase 5.3.1:** Stakeholder improvements → selectionalMismatch, Organization typing

### Immediate (Phase 6)

6. **Phase 6.0:** Selectional Preferences lookup table ✅ Complete (60 tests)
7. **Phase 6.1:** Ambiguity Resolver ✅ Complete (46 tests)
8. **Phase 6.2:** InterpretationLattice ✅ Complete (55 tests)
9. **Phase 6.3:** Alternative graph generation ✅ Complete (75 tests)
10. **Phase 6.4:** SemanticGraphBuilder integration + Deontic enhancement (opt-in API, claim/power/immunity) ✅ Complete (72 tests)
11. **Phase 6.4.5:** OntologyValidator (validate before load) ✅ Complete (80 tests)
12. **Phase 6.5.1:** TTL Parser (lightweight Turtle parser) ✅ Complete (80 tests)
13. **Phase 6.5.2:** OntologyManager (unified JSON + TTL loading) ✅ Complete (80 tests)
14. **Phase 6.5.3:** ValueNet Integration (IEE value detection) ✅ Complete (50 tests)
15. **Phase 6.5.4:** IEE bridge ontology support ✅ Complete (54 tests)
16. **Phase 6.6:** OntologyTextTagger (general-purpose text tagging) ✅ Complete (64 tests)
17. Create golden test corpus for lattice validation ← **Next**

### Near-Term (Phase 6.5 - IEE ValueNet Integration) ✅ COMPLETE

13. **Phase 6.5.1:** Lightweight TTL Parser ✅ Complete (80 tests)
14. **Phase 6.5.2:** OntologyManager ✅ Complete (80 tests)
15. **Phase 6.5.3:** ValueNet integration (IEE value detection) ✅ Complete (50 tests)
16. **Phase 6.5.4:** IEE bridge ontology support ✅ Complete (54 tests)

### Medium-Term (Phase 7)

16. **Phase 7.1:** Source attribution detection
17. **Phase 7.2-7.3:** Certainty markers, temporal grounding

### Longer-Term

14. **Phase 8.x:** Enhanced disambiguation
15. **Phase 9.x:** Extended validation

### As Needed

- **Phase 10:** Human validation (when IEE ready)
- **Phase 11:** Domain configs (as domains are needed)

---

## Ideal NLP Capability Mapping

| Ideal NLP Requirement | TagTeam Phase | Status |
|-----------------------|---------------|--------|
| BFO Category Assignment | Phase 4 | ✅ Complete |
| Semantic Role Detection | Phase 4 | ✅ Complete |
| Selectional Restrictions | Phase 4 | ✅ Complete |
| Domain Ontology Integration | Phase 4 | ✅ Complete |
| SHACL Validation | Phase 4 | ✅ Complete |
| GIT-Minimal Provenance | Phase 4 | ✅ Complete |
| Confidence Decomposition | Phase 4 | ✅ Complete |
| **Ambiguity Detection** | Phase 5 | ✅ Complete |
| **Modal Force Classification** | Phase 5 | ✅ Complete |
| **Selectional Violation Detection** | Phase 5 | ✅ Complete |
| **Scope Ambiguity Detection** | Phase 5 | ✅ Complete |
| **Metonymy Detection** | Phase 5 | ✅ Complete |
| **Ambiguity Resolution** | Phase 6 | ✅ Complete |
| **Interpretation Lattice** | Phase 6 | ✅ Complete |
| **Alternative Graph Generation** | Phase 6 | ✅ Complete |
| **Ontology Validation** | Phase 6.4.5 | ✅ Complete |
| **TTL Ontology Loading** | Phase 6.5.1 | ✅ Complete |
| **ValueNet Integration** | Phase 6.5.3 | ✅ Complete |
| **Source Attribution** | Phase 7 | Planned |
| **Epistemic Status** | Phase 7 | Planned |
| **Temporal Grounding** | Phase 7 | Planned |
| Human Validation Loop | Phase 10 | Planned |

---

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| 6.6.0 | 2026-01-27 | Phase 6.6 complete: OntologyTextTagger with 64 tests, configurable property mapping, medical/legal examples |
| 6.5.4.0 | 2026-01-26 | Phase 6.5.4 complete: BridgeOntologyLoader with 54 tests, owl:sameAs/relatedTo/worldview mapping, IEE bridge template |
| 6.5.3.0 | 2026-01-26 | Phase 6.5.3 complete: ValueNetAdapter with 50 tests, OntologyManager→ValueMatcher bridge, polarity conversion |
| 6.5.2.0 | 2026-01-26 | Phase 6.5.2 complete: OntologyManager with 80 tests, unified JSON+TTL loading, caching, merge strategy |
| 6.5.1.0 | 2026-01-26 | Phase 6.5.1 complete: TurtleParser with 80 tests, prefix/triple parsing, ValueNet extraction |
| 6.4.5.0 | 2026-01-26 | Phase 6.4.5 complete: OntologyValidator with 80 tests, BFO/CCO registry, ValidationReport |
| 6.4.0-deontic | 2026-01-26 | Phase 6.4 complete: Deontic enhancement (claim, power, immunity), sentence-level detection, 72 tests |
| 6.3.0-alternatives | 2026-01-26 | Phase 6.3 complete: AlternativeGraphBuilder with 75 tests, modal/scope/noun alternatives |
| 6.2.0-lattice | 2026-01-26 | Phase 6.2 complete: InterpretationLattice with 55 tests, alternatives, serialization |
| 6.1.0-resolver | 2026-01-26 | Phase 6.1 complete: AmbiguityResolver with 46 tests, resolution rules, threshold config |
| 6.0.0-selectional | 2026-01-26 | Phase 6.0 complete: SelectionalPreferences with 60 tests, verb taxonomy, entity categories |
| 5.3.2-roadmap | 2026-01-25 | Added Phase 6.5: TTL Ontology Loading for IEE ValueNet integration |
| 5.3.1-phase5 | 2026-01-23 | Phase 5 complete: 280+ tests, ambiguity detection, stakeholder improvements |
| 5.2.0-tests | 2026-01-22 | Phase 8.5 test-driven enhancements, comprehensive test framework |
| 5.1.0-vision | 2026-01-19 | Addressed critique: scope clarity, bundle budgets, test strategy, Phase 7/10 detail |
| 5.0.0-vision | 2026-01-19 | Ideal NLP roadmap, opt-in lattice API design |
| 4.0.0-phase4 | 2026-01-19 | Domain-Neutral Parser, Selectional Restrictions |
| 4.0.0 | 2026-01-19 | Phase 4 complete, JSON-LD, SHACL validation |
| 2.0.0 | 2026-01 | IEE integration, 50 values, ethical profiling |
| 1.0.0 | 2025 | Initial semantic parser |

---

## Current Bundle

```
dist/tagteam.js  (~4.85 MB single bundle)

┌─────────────────────────────────────────────────────────────┐
│                    tagteam.js (4.85 MB)                     │
├─────────────────────────────────────────────────────────────┤
│  Core                                                       │
│  ├── lexicon.js (4.1 MB POS lexicon)                       │
│  ├── POSTagger.js                                          │
│  ├── PatternMatcher.js                                     │
│  ├── SemanticRoleExtractor.js                              │
│  ├── ContractionExpander.js (Phase 5)                      │
│  ├── Lemmatizer.js (Phase 5)                               │
│  ├── VerbPhraseExtractor.js (Phase 5)                      │
│  └── NounPhraseExtractor.js (Phase 5)                      │
├─────────────────────────────────────────────────────────────┤
│  Analyzers                                                  │
│  ├── ContextAnalyzer.js (12 dimensions)                    │
│  ├── ValueMatcher.js                                       │
│  ├── ValueScorer.js                                        │
│  └── EthicalProfiler.js                                    │
├─────────────────────────────────────────────────────────────┤
│  Graph (Phase 4 + 5)                                        │
│  ├── SemanticGraphBuilder.js                               │
│  ├── JSONLDSerializer.js                                   │
│  ├── SHMLValidator.js                                      │
│  ├── AmbiguityDetector.js (Phase 5)                        │
│  └── AmbiguityReport.js (Phase 5)                          │
│  └── [12 other modules]                                    │
├─────────────────────────────────────────────────────────────┤
│  Data                                                       │
│  ├── IEE 50 value definitions                              │
│  ├── Frame-value boosts                                    │
│  ├── Conflict pairs                                        │
│  └── Compound terms                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
TagTeam.js/
├── dist/
│   └── tagteam.js              # Production bundle (4.8 MB)
├── src/
│   ├── core/                   # Semantic parsing
│   ├── analyzers/              # Ethics analysis
│   ├── graph/                  # Phase 4 JSON-LD
│   └── types/                  # TypeScript definitions
├── tests/
│   ├── unit/                   # 290+ unit tests
│   └── integration/            # Corpus validation
├── docs/
│   ├── PHASE4_USER_GUIDE.md
│   ├── JSONLD_EXAMPLES.md
│   ├── SHACL_VALIDATION_GUIDE.md
│   └── research/
│       └── idealNLP_v1.1.md    # Vision document
├── config/
│   └── medical.json            # Medical domain config
├── planning/
│   └── week3/                  # Phase 4 planning docs
├── archive/
│   └── POS Graph POC/          # POSTaggerGraph.js (to revive)
├── iee-collaboration/          # IEE test corpus
├── ROADMAP.md                  # This file
└── README.md
```

---

## Quick Reference

### Build Commands

```bash
npm run build          # Build production bundle
npm test               # Run all tests
node tests/unit/test-shacl-validation.js    # SHACL tests
node tests/integration/test-phase4-corpus.js # Corpus validation
```

### Current API

```javascript
// Basic parsing (current)
const result = TagTeam.parse(text);

// With JSON-LD output (current)
const builder = new SemanticGraphBuilder();
const graph = builder.build(text, { context: 'MedicalEthics' });

// SHACL validation (current)
const validator = new SHMLValidator();
const report = validator.validate(graph);
```

### Future API (Phase 6+)

```javascript
// Opt-in ambiguity preservation
const result = builder.build(text, {
  preserveAmbiguity: true,
  pruningConfig: { maxReadings: 5, plausibilityThreshold: 0.1 }
});

// Access lattice
console.log(result.defaultReading);     // JSON-LD graph (most likely)
console.log(result.lattice.nodes);      // All significant readings
console.log(result._epistemics);        // Source attribution, certainty
```

---

## Contact & Support

- **Issues:** https://github.com/anthropics/claude-code/issues
- **IEE Collaboration:** See `iee-collaboration/` folder

---

**TagTeam** - A domain-neutral semantic interpretation engine for ethical dilemma analysis.

*"Better to output structured uncertainty than false precision."*
