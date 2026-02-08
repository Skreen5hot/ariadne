# FANDAWS — Fact and Answer Web Service

## Edge-Canonical Functional Specification

**Version:** 3.4  
**Date:** February 2026  
**Author:** Aaron Damiano  
**Organization:** Ontology of Freedom Initiative  
**Status:** Fianl

---

# 1. Executive Summary

Fandaws (Fact and Answer Web Service) is a conversational knowledge-building platform that enables users and agents to teach a system through natural language, creating structured concept hierarchies with classifications, properties, and relationships. This specification defines Fandaws as an edge-canonical system: one that runs unmodified in a browser or via a local Node.js runtime, with no required infrastructure beyond JSON-LD files.

Fandaws operates as both a human-facing knowledge builder and a machine-to-machine (M2M) ontology protocol. In the M2M context, Fandaws acts as a Structured Thinking Processor: it forces probabilistic AI models to commit to grounded, consistent ontological structures before those structures are consumed by downstream reasoning systems. The conversational validation pipeline — scope narrowing, disambiguation, deduplication — functions as a semantic firewall that prevents unverified generalizations and hyper-specific noise from polluting the knowledge graph. This "friction" is not a usability problem; it is compute-time verification that translates probabilistic token generation into ontologically committed facts.

This document supersedes the original Fandaws functional specification. It preserves all core knowledge-building workflows, validation rules, and business logic while restructuring the architecture around six governing constraints: edge-canonical execution, no required infrastructure, deterministic computation, mandatory separation of concerns, JSON-LD as canonical representation, and offline as a first-class mode.

Fandaws occupies a unique position in the broader ecosystem of semantic reasoning and AI governance tools. As a conversational ontology builder, it provides the foundational knowledge structures that downstream systems—such as the Integral Ethics Engine, HIRI protocol, and FNSR services—depend on for grounded, structured reasoning. Every concept hierarchy, property chain, and relationship graph that Fandaws produces is a potential input to moral reasoning, counterfactual simulation, or analogical precedent matching.

# 2. Architectural Constraints

The following constraints are not implementation preferences. They define the architectural truth of the system. Every component, workflow, and data structure in this specification must satisfy all six constraints simultaneously.

## 2.1 Edge-Canonical First Principle

All components specified here must be able to run, unmodified, in a browser or via node index.js. This is the canonical execution model. Any cloud, server, or enterprise deployment is a derivative optimization, not the baseline assumption. If a component cannot function under this constraint, it is infrastructure, not core logic, and must be treated as optional, pluggable, or out-of-scope for the core specification.

## 2.2 No Required Infrastructure

Specifications must not assume the existence of databases, message brokers, service registries, background workers, addressable servers, or deployment topologies. These may appear only as non-normative examples or adapter implementations, never as architectural requirements.

## 2.3 Determinism Over Deployment

Given the same inputs, the system must produce the same outputs. Hidden state, ambient services, and environment-coupled behavior are violations of the model unless explicitly isolated behind a declared adapter boundary.

## 2.4 Separation of Concerns

Every component must clearly distinguish between four layers:

1.  Computation — what is being derived or reasoned (CORE)

2.  State — how intermediate results are stored or resumed (PLUGGABLE)

3.  Orchestration — how and when computation is invoked (PLUGGABLE)

4.  Integration — how the external world is contacted (PLUGGABLE)

Only layer (1) is core. Layers (2) through (4) must be pluggable via declared adapter interfaces.

## 2.5 JSON-LD as Canonical Representation

JSON-LD is the authoritative format for inputs, outputs, configuration, knowledge structures, and inter-component contracts. Alternative internal representations are permitted only as optimizations and must be losslessly derivable from the JSON-LD form.

## 2.6 Offline as First-Class Mode

Inability to reach external systems is not an error state. The system must define valid behavior for partial information, deferred resolution, degraded execution, and explicit uncertainty.

## 2.7 Spec Test

The definitive acceptance criterion: Could a developer evaluate, reason about, and execute this system using only a browser, a local Node.js runtime, and JSON-LD files? If the answer is no, the specification requires revision.

## 2.8 No Probabilistic Core Computation

No core computation module (Section 3.2) may use probabilistic inference, neural network weights, language model API calls, or any non-deterministic reasoning method. The NLParser uses grammar-based and regex extraction. The Classifier uses enum matching. The KnowledgeEngine uses graph traversal. The Validator uses rule evaluation. All core computation is reproducible without access to any model or inference service.

Large language models, embedding models, and other probabilistic systems are external callers that interact with Fandaws through the OrchestrationAdapter. They are never components of the pipeline. All references to "agents" and "LLMs" in the M2M Conversation Protocol (Section 5.9) refer exclusively to upstream callers, not to internal components. Fandaws disciplines probabilistic systems; it does not contain them.

IntegrationAdapter methods (dictionary lookup, BFO alignment, ontology import) may contact external services that are themselves non-deterministic, but these calls are isolated behind the adapter boundary, their results are cached deterministically, and they must return provenance metadata (Section 3.3.2) so that the source and version of every external result is auditable.

# 3. System Architecture

Fandaws is structured as a pipeline of pure computation modules connected through JSON-LD contracts. Each module accepts JSON-LD input, performs deterministic transformation, and emits JSON-LD output. State persistence, orchestration, and external integration are handled exclusively through adapter interfaces that are not part of the core specification.

## 3.1 Architectural Layers

|               |           |                                                                             |                                                     |
|---------------|-----------|-----------------------------------------------------------------------------|-----------------------------------------------------|
| **Layer**     | **Type**  | **Responsibility**                                                          | **Examples**                                        |
| Computation   | CORE      | Parsing, classification, validation, inference, description generation      | NLParser, Classifier, Validator, DescriptionEngine  |
| State         | PLUGGABLE | Persisting knowledge graphs, session state, cache entries                   | InMemoryStore, IndexedDBStore, FileSystemStore      |
| Orchestration | PLUGGABLE | Routing user input through computation pipeline, managing conversation flow | ConversationOrchestrator, BatchProcessor, CLIRunner |
| Integration   | PLUGGABLE | Dictionary lookup, BFO alignment, external ontology import                  | DictionaryAdapter, BFOAdapter, SPARQLAdapter        |

## 3.2 Core Computation Modules

Each module is a pure function or stateless class that operates exclusively on JSON-LD input and produces JSON-LD output. No module may hold mutable state between invocations. No module may perform I/O directly.

### 3.2.1 NLParser (Natural Language Parser)

**Purpose:** Parse user utterances into structured semantic frames.

**Input:** A JSON-LD UserUtterance node containing the raw text and current conversation context.

**Output:** A JSON-LD ParseResult node containing extracted subject, predicate, object, verb type (is/has/custom), and confidence scores.

**Determinism Guarantee:** Given identical utterance text and context, the parser must produce identical ParseResult output. If the parser delegates to an LLM or probabilistic model, that delegation must occur through the Integration layer, and the core parser must define fallback behavior for when the integration is unavailable.

### 3.2.2 Classifier

**Purpose:** Route parsed statements to the appropriate knowledge-building workflow.

**Input:** A ParseResult node.

**Output:** A ClassificationAction node specifying the workflow (classification, property, custom-relationship) and extracted operands.

Classification routing follows the original Fandaws logic: “X is a Y” routes to the classification workflow, “X has Y” routes to the property workflow, and any other verb form routes to the custom relationship workflow.

### 3.2.3 KnowledgeEngine

**Purpose:** Execute knowledge-building operations against a knowledge graph, producing graph mutations.

**Input:** A ClassificationAction node plus the current KnowledgeGraph (as JSON-LD).

**Output:** A GraphMutation node describing additions, modifications, and deletions to apply, plus any ConversationPrompt nodes for disambiguation.

The KnowledgeEngine contains the core business logic for all three workflows (classification, property, custom relationship) and all validation rules (deduplication, sanity check, property redundancy prevention, custom relationship validation). It does not apply mutations directly; it emits them as declarative descriptions for the State layer to execute.

### 3.2.4 Validator

**Purpose:** Enforce structural integrity constraints on proposed graph mutations before they are applied.

**Input:** A GraphMutation node plus the current KnowledgeGraph.

**Output:** A ValidationResult node (valid/invalid with specific violation descriptors).

Validation rules are specified in Section 6.

### 3.2.5 DescriptionEngine

**Purpose:** Generate natural-language definitions for concepts based on their position in the knowledge graph.

**Input:** A concept identifier plus the current KnowledgeGraph.

**Output:** A Description node containing the generated text and the template used.

Description templates follow the original Fandaws patterns. Standard concepts: “\[Term\] is a \[parent\] that has \[prop1\], \[prop2\], \[prop3\].” Process concepts: “\[Object\] \[term\] is the \[parent+ing\] of \[object\] by \[subject\].”

### 3.2.6 ExportEngine

**Purpose:** Transform the knowledge graph into external ontology formats.

**Input:** A KnowledgeGraph (JSON-LD) plus an ExportConfiguration specifying target format.

**Output:** Serialized output in the requested format (SKOS, OWL, RDF/XML, Turtle).

The ExportEngine performs read-only traversal of the knowledge graph. It makes no mutations and requires no external services. Export to each format is a deterministic mapping from the JSON-LD canonical form.

### 3.2.7 ScopeResolver

**Purpose:** Resolve terms and detect conflicts across a hierarchy of knowledge graphs (scopes). The ScopeResolver sits between the OrchestrationAdapter and the core pipeline. When a term is referenced during knowledge entry, the ScopeResolver searches the scope hierarchy before the pipeline creates a new concept, preventing redundant definitions and detecting cross-scope conflicts.

**Input:** A term (string), a ScopeConfiguration (JSON-LD) listing the scope hierarchy, and read access to each scope graph via the StateAdapter.

**Output:** A ScopeResolution (JSON-LD) containing either a resolved concept (found in a higher scope), a conflict report (incompatible definitions across scopes), or a null result (term not found in any scope, proceed with normal pipeline creation).

The ScopeResolver is a pure function. It performs read-only traversal of scope graphs. It does not mutate any graph. It does not perform I/O directly — all graph access is mediated by the StateAdapter, which may load scope graphs from local files, IndexedDB, or IPFS-cached snapshots. The ScopeResolver has no knowledge of where scope graphs are stored or how they were published.

**Scope Hierarchy Model:**

Fandaws operates on a hierarchy of knowledge graphs called scopes. Each scope is a complete Fandaws KnowledgeGraph — the same JSON-LD structure used for local knowledge. Scopes are resolved in priority order:

1. **Context scope** — A temporary, session-bound graph shared by participants in a specific conversation or decision. Created by the OrchestrationAdapter, typically for a single interaction context (e.g., a moral reasoning case, a policy evaluation). Context scopes expire.

2. **User scope** — The caller's personal knowledge graph, accumulating definitions across sessions. This is the default working graph when no context scope is active. Persisted locally or published to IPFS.

3. **Global scope** — A federation of published knowledge graphs, resolved in a configurable order. Each published graph is an IPFS-pinned Fandaws KnowledgeGraph with a known CID. The resolution order is specified in the ScopeConfiguration.

The global scope is not a single canonical graph. It is a search path over a federation of published graphs, analogous to how a Unix shell searches PATH for executables. The first match wins, subject to conflict detection.

**Resolution Algorithm:**

1. Normalize the input term via Identity Simplification (Section 6.6).
2. Search the context scope graph (if active) for a concept with a matching canonicalLabel.
3. If not found, search the user scope graph.
4. If not found, search each global scope graph in resolution order.
5. If a match is found:
   a. Copy the concept, its parent chain (up to root), its direct properties, and its direct relationships into the local working graph. Each copied node carries a fandaws:resolvedFrom annotation (Section 4.2.8) recording the source graph IRI, the source concept IRI, and the resolution timestamp.
   b. Return a ScopeResolution with status="resolved", the copied concept, and the source scope metadata.
6. If matches are found in multiple scopes with incompatible IS_A chains (the concept's parent chain diverges), return a ScopeResolution with status="conflict" and a ConflictReport listing each definition, its source scope, and resolution options.
7. If no match is found in any scope, return a ScopeResolution with status="unknown". The pipeline proceeds with normal concept creation in the local working graph.

**Conflict Detection:**

Two definitions of the same term conflict if their IS_A chains are incompatible — that is, the parent concepts diverge and do not converge to a common ancestor within the deduplication depth (Section 6.2). For example, "autonomy IS_A capacity" and "autonomy IS_A right" conflict because "capacity" and "right" are not related. "autonomy IS_A capacity" and "autonomy IS_A cognitive_capacity" do not conflict because "cognitive_capacity IS_A capacity" (one is more specific).

**Offline Behavior:**

When a global scope graph is unavailable (IPFS CID not cached locally), the ScopeResolver skips it and continues to the next graph in the resolution order. The skipped scope is recorded in the ScopeResolution as a DeferredResult. When connectivity is restored, the OrchestrationAdapter may re-run scope resolution to check for conflicts with the previously unavailable graph.

## 3.3 Adapter Interfaces

Each pluggable layer defines a TypeScript-style interface that adapters must implement. The core specification provides reference implementations for in-memory and file-system adapters. All other adapters (IndexedDB, REST API, SPARQL endpoint) are non-normative extensions.

### 3.3.1 StateAdapter Interface

The StateAdapter provides persistence operations for knowledge graphs and session state. The reference implementation stores all state as JSON-LD files in memory or on the local file system.

|                             |                             |                                                                                  |
|-----------------------------|-----------------------------|----------------------------------------------------------------------------------|
| **Method**                  | **Returns**                 | **Description**                                                                  |
| loadGraph(id)               | KnowledgeGraph \| null      | Load a knowledge graph by identifier. Returns null if not found (offline-safe).  |
| saveGraph(id, graph)        | void                        | Persist a knowledge graph. The graph must be valid JSON-LD.                      |
| applyMutation(id, mutation) | KnowledgeGraph              | Apply a GraphMutation to a stored graph and return the updated graph.            |
| loadSession(id)             | ConversationSession \| null | Load conversation session state.                                                 |
| saveSession(id, session)    | void                        | Persist conversation session state.                                              |
| listSessions(callerId, filter) | ConversationSession\[\]  | List sessions for a caller, optionally filtered by state.                        |
| queryGraph(id, query)       | QueryResult                 | Execute a graph query (pattern matching, path traversal) against a stored graph. |
| loadScopeConfig(id)         | ScopeConfiguration \| null  | Load the scope configuration for a session. Returns null for single-graph mode.  |
| saveScopeConfig(id, config) | void                        | Persist a scope configuration.                                                   |

**Scope Graph Access:** When the ScopeResolver calls loadGraph(id) for a global-scope graph, the StateAdapter is responsible for resolving the graph identifier — which may be an IPFS CID URI — to a locally accessible JSON-LD file. If the graph is not cached locally, the StateAdapter returns null (offline-safe). The StateAdapter may use IPFS gateway APIs, local pin caches, or pre-loaded files to resolve scope graphs. This resolution is an adapter concern, not a pipeline concern.

**Atomicity:** applyMutation is atomic per GraphMutation. A single GraphMutation may contain multiple additions, modifications, deletions, and merges; either all operations in the mutation succeed and the graph transitions to a new consistent state, or none do and the graph remains unchanged. If a mutation cannot be applied atomically (e.g., a merge target no longer exists because of a concurrent deletion), applyMutation must reject the entire mutation and return the unmodified graph along with a MutationRejection reason.

**Concurrency Model:** Fandaws is edge-canonical and single-writer by default. A single browser tab or Node.js process owns the authoritative copy of a knowledge graph. Multi-device synchronization is not part of the core specification — it is an infrastructure concern managed by the StateAdapter. Implementations that support multi-writer scenarios must adopt a conflict resolution strategy (e.g., causal ordering via mutation timestamps, or CRDT-based merge) and document it as part of their adapter contract. The core computation pipeline assumes it is the sole writer and does not perform optimistic concurrency checks.

When IPFS/HIRI optimistic batching (Section 10.5.3) is in use, the in-memory graph is the authoritative single-writer state. Batch commits to IPFS are append-only snapshots, not concurrent writes, so no conflict resolution is needed for the publication path.

### 3.3.2 IntegrationAdapter Interface

The IntegrationAdapter handles all external communication. When unavailable, each method must define graceful degradation behavior. No IntegrationAdapter method may invoke probabilistic inference or language model APIs (Section 2.8). These methods contact deterministic external services (dictionary endpoints, BFO SPARQL endpoints, ontology file servers).

|                        |                                    |                                                                                         |
|------------------------|------------------------------------|-----------------------------------------------------------------------------------------|
| **Method**             | **Returns**                        | **Description**                                                                         |
| lookupDictionary(term) | DictionaryResult \| DeferredResult | Look up a term in an external dictionary. Returns DeferredResult when offline.          |
| lookupBFO(concept)     | BFOMapping \| DeferredResult       | Map a concept to Basic Formal Ontology categories. Returns DeferredResult when offline. |
| importOntology(source) | KnowledgeGraph \| DeferredResult   | Import an external ontology as a partial knowledge graph.                               |

**Provenance:** Every result returned by an IntegrationAdapter method must include a provenance envelope so that the source and version of every external result is auditable and reproducible:

|                               |                  |                                                              |
|-------------------------------|------------------|--------------------------------------------------------------|
| **Field**                     | **Type**         | **Description**                                              |
| fandaws:provenance.provider   | string           | Service identifier (e.g., "wordnik-api", "obo-foundry")     |
| fandaws:provenance.version    | string \| null   | Service version or API version, if known                     |
| fandaws:provenance.inputHash  | string           | SHA-256 hash of the request payload                          |
| fandaws:provenance.outputHash | string           | SHA-256 hash of the response payload                         |
| fandaws:provenance.retrievedAt| dateTime         | When the result was retrieved                                |
| fandaws:provenance.fromCache  | boolean          | Whether this result was served from cache rather than live   |

This provenance envelope enables the Spec Test to verify that two runs against the same cached integration results produce identical graphs. It also enables HIRI (Section 10.5.3) to trace every external fact to its source.

### 3.3.3 OrchestrationAdapter Interface

The OrchestrationAdapter manages conversation flow, input/output routing, and pipeline execution sequencing. The reference implementation is a synchronous conversation loop. In M2M deployments, the OrchestrationAdapter must additionally enforce convergence constraints to prevent semantic deadlock.

|                                 |                            |                                                                                          |
|---------------------------------|----------------------------|------------------------------------------------------------------------------------------|
| **Method**                      | **Returns**                | **Description**                                                                          |
| receiveInput(input)             | void                       | Accept input (text, confirmation, selection) from a human or agent and route to the computation pipeline. |
| emitOutput(output)              | void                       | Deliver system output (prompts, confirmations, results) to the caller interface.          |
| runPipeline(utterance, context) | PipelineResult             | Execute the full computation pipeline for a single utterance.                            |
| getCallerMode()                 | enum                       | Returns "human" or "agent" to control machineSignal population on ConversationPrompts.   |
| checkDeadlock(sessionId)        | DeadlockStatus             | Evaluate whether the current session has entered a semantic deadlock (see Section 6.7).  |

**M2M Mode:** When getCallerMode() returns "agent", the OrchestrationAdapter must populate the machineSignal field on every emitted ConversationPrompt (Section 4.2.6). This enables upstream agents to respond with structured selections rather than reparsing natural language questions.

**Convergence Enforcement:** The OrchestrationAdapter must track the number of consecutive rejected mutations per concept per session. When this count exceeds the configured repetitionLimit (Section 11.1), the adapter must trigger a Semantic Deadlock event (Section 6.7) rather than allowing unbounded retry loops.

# 4. JSON-LD Data Model

All data in Fandaws is represented as JSON-LD. This section defines the canonical shapes for the core data types. The @context for Fandaws uses the namespace prefix "fandaws" and extends schema.org and SKOS vocabularies where appropriate.

## 4.1 Fandaws Context

The Fandaws JSON-LD context defines the vocabulary for all system data types. It is self-contained and does not require network access to resolve. The context file must be bundled with every Fandaws deployment.

|            |                                      |                                                              |
|------------|--------------------------------------|--------------------------------------------------------------|
| **Prefix** | **IRI**                              | **Usage**                                                    |
| fandaws    | https://fandaws.org/schema/          | Core Fandaws vocabulary (concepts, relationships, mutations) |
| skos       | http://www.w3.org/2004/02/skos/core# | Concept schemes, labels, broader/narrower                    |
| owl        | http://www.w3.org/2002/07/owl#       | OWL class and property exports                               |
| bfo        | http://purl.obolibrary.org/obo/      | Basic Formal Ontology alignment                              |
| schema     | https://schema.org/                  | General-purpose properties                                   |

## 4.2 Core Data Types

### 4.2.1 Concept

A Concept is the fundamental unit of knowledge in Fandaws. It represents a named entity in the knowledge graph with a position in a classification hierarchy, a set of properties, and relationships to other concepts.

|                         |                  |                                                             |
|-------------------------|------------------|-------------------------------------------------------------|
| **Field**               | **Type**         | **Description**                                             |
| @id                     | IRI              | Unique concept identifier (e.g., fandaws:concept/dog)       |
| @type                   | fandaws:Concept  | Type discriminator                                          |
| fandaws:label           | string           | Canonical display name (lowercase, trimmed)                 |
| fandaws:simplifiedLabel | string           | Identity-simplified form for matching                       |
| fandaws:parent          | IRI \| null      | Parent concept in classification hierarchy (null for roots) |
| fandaws:children        | IRI\[\]          | Child concepts in classification hierarchy                  |
| fandaws:properties      | Property\[\]     | Properties attached to this concept                         |
| fandaws:relationships   | Relationship\[\] | Custom relationships involving this concept                 |
| fandaws:description     | string           | Auto-generated natural-language definition                  |
| fandaws:bfoMapping      | IRI \| null      | Basic Formal Ontology category alignment                    |
| fandaws:createdAt       | dateTime         | Creation timestamp                                          |
| fandaws:depth           | integer          | Depth in classification hierarchy (root = 0)                |

### 4.2.2 Property

A Property represents a characteristic or attribute attached to a concept. Properties are inherited down the classification hierarchy unless overridden.

|                    |                  |                                               |
|--------------------|------------------|-----------------------------------------------|
| **Field**          | **Type**         | **Description**                               |
| @id                | IRI              | Unique property identifier                    |
| @type              | fandaws:Property | Type discriminator                            |
| fandaws:label      | string           | Property name                                 |
| fandaws:attachedTo | IRI              | Concept this property is directly attached to |
| fandaws:scope      | string           | Scope level (concept-specific or inherited)   |
| fandaws:value      | any \| null      | Optional property value                       |

### 4.2.3 Relationship

A Relationship represents a custom (non-is, non-has) connection between concepts, capturing arbitrary verb forms as first-class semantic structures.

|                           |                      |                                                                     |
|---------------------------|----------------------|---------------------------------------------------------------------|
| **Field**                 | **Type**             | **Description**                                                     |
| @id                       | IRI                  | Unique relationship identifier                                      |
| @type                     | fandaws:Relationship | Type discriminator                                                  |
| fandaws:verb              | string               | The verb connecting subject and object                              |
| fandaws:subject           | IRI                  | Source concept                                                      |
| fandaws:object            | IRI                  | Target concept                                                      |
| fandaws:subRelationshipOf | IRI \| null          | Parent relationship for verb hierarchies                            |
| fandaws:promoted          | boolean              | Whether this relationship has been promoted from a sub-relationship |

### 4.2.4 KnowledgeGraph

The KnowledgeGraph is the top-level container for all knowledge in a Fandaws session. It is a valid JSON-LD document that can be serialized, transmitted, and loaded as a single unit.

|                       |                        |                                                        |
|-----------------------|------------------------|--------------------------------------------------------|
| **Field**             | **Type**               | **Description**                                        |
| @context              | object                 | Fandaws JSON-LD context                                |
| @id                   | IRI                    | Graph identifier                                       |
| @type                 | fandaws:KnowledgeGraph | Type discriminator                                     |
| fandaws:concepts      | Concept\[\]            | All concepts in the graph                              |
| fandaws:relationships | Relationship\[\]       | All custom relationships                               |
| fandaws:metadata      | GraphMetadata          | Graph-level metadata (version, timestamps, statistics) |

### 4.2.5 GraphMutation

A GraphMutation is a declarative description of changes to be applied to a KnowledgeGraph. Mutations are emitted by the KnowledgeEngine and executed by the StateAdapter. This separation ensures that all graph modifications are auditable, reversible, and deterministic.

|                       |                       |                                                               |
|-----------------------|-----------------------|---------------------------------------------------------------|
| **Field**             | **Type**              | **Description**                                               |
| @type                 | fandaws:GraphMutation | Type discriminator                                            |
| fandaws:additions     | Node\[\]              | Nodes and edges to add                                        |
| fandaws:modifications | Patch\[\]             | Property-level changes to existing nodes                      |
| fandaws:deletions     | IRI\[\]               | Node identifiers to remove                                    |
| fandaws:merges        | Merge\[\]             | Node merge operations (deduplication)                         |
| fandaws:reason        | string                | Human-readable explanation of the mutation                    |
| fandaws:validatedBy   | IRI \| null           | Reference to the ValidationResult that approved this mutation |

### 4.2.6 ConversationPrompt

A ConversationPrompt represents a system-initiated question to the caller, used for disambiguation, confirmation, or scope narrowing during knowledge building. When the caller is a human, the text field provides a readable question. When the caller is an agent (M2M mode), the machineSignal field provides a structured negotiation contract so the upstream agent does not need to parse natural language back into a structured response.

|                          |                            |                                                           |
|--------------------------|----------------------------|-----------------------------------------------------------|
| **Field**                | **Type**                   | **Description**                                           |
| @type                    | fandaws:ConversationPrompt | Type discriminator                                        |
| fandaws:promptType       | enum                       | Type: confirmation, disambiguation, scopeNarrowing, yesNo |
| fandaws:text             | string                     | Display text for the prompt (human-readable)              |
| fandaws:options          | string\[\] \| null         | Available choices (null for open-ended)                   |
| fandaws:context          | object                     | State needed to resume processing after response          |
| fandaws:machineSignal    | MachineSignal \| null      | Structured negotiation contract for M2M callers (null for human callers) |

**MachineSignal Schema:**

|                          |                            |                                                           |
|--------------------------|----------------------------|-----------------------------------------------------------|
| **Field**                | **Type**                   | **Description**                                           |
| fandaws:expectedSchema   | object                     | JSON Schema defining the valid response shape             |
| fandaws:validValues      | string\[\] \| null         | Enumerated valid responses, if bounded                    |
| fandaws:constraintType   | enum                       | The ontological constraint being negotiated: subsumption, inherence, disjointness, scopeLevel |
| fandaws:candidateIRIs    | IRI\[\] \| null            | Candidate concept IRIs for disambiguation (agent can select by IRI rather than label) |
| fandaws:hierarchyContext | object \| null             | Relevant subgraph showing where the concept sits in the hierarchy, enabling the agent to make an informed selection |

When an OrchestrationAdapter operates in M2M mode, it must populate the machineSignal field on every ConversationPrompt. When operating in human mode, machineSignal may be null. The presence or absence of machineSignal does not alter the computation pipeline — it is a presentation concern managed by the OrchestrationAdapter.

### 4.2.7 DeferredResult

A DeferredResult represents an operation that could not be completed due to offline status or integration unavailability. It captures enough context to retry the operation when connectivity is restored.

|                      |                        |                                                         |
|----------------------|------------------------|---------------------------------------------------------|
| **Field**            | **Type**               | **Description**                                         |
| @type                | fandaws:DeferredResult | Type discriminator                                      |
| fandaws:operation    | string                 | The operation that was deferred                         |
| fandaws:input        | object                 | The input that triggered the operation                  |
| fandaws:reason       | string                 | Why the operation was deferred (e.g., offline, timeout) |
| fandaws:retryAfter   | dateTime \| null       | Suggested retry time, if known                          |
| fandaws:fallbackUsed | boolean                | Whether a degraded fallback was used instead            |

### 4.2.8 ScopeConfiguration

A ScopeConfiguration defines the scope hierarchy for a session. It is loaded at session initialization and determines how the ScopeResolver searches for existing definitions before creating new concepts.

|                                   |                           |                                                            |
|-----------------------------------|---------------------------|------------------------------------------------------------|
| **Field**                         | **Type**                  | **Description**                                            |
| @type                             | fandaws:ScopeConfiguration| Type discriminator                                         |
| fandaws:contextGraphId            | IRI \| null               | Active context scope graph, if any                         |
| fandaws:userGraphId               | IRI                       | The caller's personal knowledge graph                      |
| fandaws:globalFederation          | ScopeEntry\[\]            | Ordered list of global scope graphs to search              |

**ScopeEntry:**

|                                   |                           |                                                            |
|-----------------------------------|---------------------------|------------------------------------------------------------|
| **Field**                         | **Type**                  | **Description**                                            |
| fandaws:graphId                   | IRI                       | Graph identifier (may be an IPFS CID URI)                  |
| fandaws:label                     | string                    | Human-readable name (e.g., "BFO Core v1.2", "Medical Domain") |
| fandaws:ipfsCid                   | string \| null            | IPFS Content Identifier for retrieval                      |
| fandaws:priority                  | integer                   | Resolution order (lower = searched first)                  |
| fandaws:trustLevel                | enum                      | authoritative, community, experimental                     |
| fandaws:staleCopyAction           | enum \| null              | Per-scope override for the global staleCopyAction. If null, uses the global setting. |

**Scope Versioning:** Because IPFS CIDs are content-addressed and immutable, each CID in a ScopeEntry represents a specific, frozen version of a knowledge graph. "Updating" a global scope graph means publishing a new version to IPFS (producing a new CID) and updating the ScopeEntry's fandaws:ipfsCid field in the ScopeConfiguration. The previous CID remains valid and accessible — it is not overwritten. This makes the ScopeConfiguration a **versioned dependency manifest** analogous to a `package-lock.json` for knowledge: each entry pins a specific immutable snapshot. Federations that need reproducible resolution behavior should version-control their ScopeConfiguration files. Callers who need to pin a scope graph to a specific version simply retain its CID in their local ScopeConfiguration and do not update it.

### 4.2.9 ScopeResolution

The output of the ScopeResolver when resolving a term across the scope hierarchy.

|                                   |                           |                                                            |
|-----------------------------------|---------------------------|------------------------------------------------------------|
| **Field**                         | **Type**                  | **Description**                                            |
| @type                             | fandaws:ScopeResolution   | Type discriminator                                         |
| fandaws:term                      | string                    | The term that was resolved                                 |
| fandaws:status                    | enum                      | resolved, conflict, unknown                                |
| fandaws:resolvedConcept           | Concept \| null           | The copied concept, if status="resolved"                   |
| fandaws:sourceScope               | ScopeSource \| null       | Which scope provided the resolution                        |
| fandaws:conflictReport            | ConflictReport \| null    | Cross-scope conflict details, if status="conflict"         |
| fandaws:skippedScopes             | ScopeEntry\[\]            | Global scopes that were unavailable (offline)              |

**ScopeSource:**

|                                   |                           |                                                            |
|-----------------------------------|---------------------------|------------------------------------------------------------|
| **Field**                         | **Type**                  | **Description**                                            |
| fandaws:scopeType                 | enum                      | context, user, global                                      |
| fandaws:graphId                   | IRI                       | Source graph identifier                                    |
| fandaws:conceptIri                | IRI                       | Original concept IRI in the source graph                   |
| fandaws:resolvedAt                | dateTime                  | When the resolution was performed                          |

### 4.2.10 ConflictReport

Emitted when the ScopeResolver detects incompatible definitions of the same term across different scopes.

|                                   |                           |                                                            |
|-----------------------------------|---------------------------|------------------------------------------------------------|
| **Field**                         | **Type**                  | **Description**                                            |
| @type                             | fandaws:ConflictReport    | Type discriminator                                         |
| fandaws:term                      | string                    | The conflicting term                                       |
| fandaws:definitions               | ConflictingDefinition\[\] | Each definition with its scope and IS_A chain              |
| fandaws:resolutionOptions         | ResolutionOption\[\]      | Suggested resolution actions                               |

**ConflictingDefinition:**

|                                   |                           |                                                            |
|-----------------------------------|---------------------------|------------------------------------------------------------|
| **Field**                         | **Type**                  | **Description**                                            |
| fandaws:conceptIri                | IRI                       | Concept IRI in source graph                                |
| fandaws:scopeType                 | enum                      | context, user, global                                      |
| fandaws:graphId                   | IRI                       | Source graph identifier                                    |
| fandaws:parentChain               | string\[\]                | IS_A chain from concept to root (display labels)           |
| fandaws:definition                | string                    | Generated description string                               |
| fandaws:properties                | string\[\]                | Direct property display labels                             |

**ResolutionOption:**

|                                   |                           |                                                            |
|-----------------------------------|---------------------------|------------------------------------------------------------|
| **Field**                         | **Type**                  | **Description**                                            |
| fandaws:action                    | enum                      | useDefinition, createDistinct, refine                      |
| fandaws:label                     | string                    | Human-readable description of the option                   |
| fandaws:targetDefinition          | ConflictingDefinition \| null | Which definition to use (for useDefinition action)     |

### 4.2.11 ResolvedFrom Annotation

When the ScopeResolver copies a concept from a higher scope into the local working graph, the copied concept carries a fandaws:resolvedFrom annotation preserving its provenance. This enables traceability: downstream consumers can verify where a concept originated and whether the source has since changed.

|                                   |                           |                                                            |
|-----------------------------------|---------------------------|------------------------------------------------------------|
| **Field**                         | **Type**                  | **Description**                                            |
| fandaws:resolvedFrom.graphId      | IRI                       | Source graph identifier                                    |
| fandaws:resolvedFrom.conceptIri   | IRI                       | Original concept IRI in the source graph                   |
| fandaws:resolvedFrom.scopeType    | enum                      | context, user, global                                      |
| fandaws:resolvedFrom.resolvedAt   | dateTime                  | When the copy was made                                     |
| fandaws:resolvedFrom.graphVersion | string \| null            | Version hash of the source graph at resolution time        |

### 4.2.12 ConversationSession

A ConversationSession tracks the state of an ongoing negotiation dialogue. Session state is managed by the OrchestrationAdapter and persisted via the StateAdapter.

|                                   |                           |                                                            |
|-----------------------------------|---------------------------|------------------------------------------------------------|
| **Field**                         | **Type**                  | **Description**                                            |
| @type                             | fandaws:ConversationSession| Type discriminator                                        |
| fandaws:sessionId                 | IRI                       | Unique session identifier                                  |
| fandaws:callerId                  | string                    | Caller identity (Section 11.2)                             |
| fandaws:state                     | enum                      | negotiating, paused, nested, conflict, complete, abandoned, expired |
| fandaws:currentPhase              | enum                      | is_a, has, relationship, complete                          |
| fandaws:term                      | string                    | The term being negotiated                                  |
| fandaws:workingGraphId            | IRI                       | The graph being built during this session                  |
| fandaws:scopeConfig               | ScopeConfiguration        | Active scope hierarchy for this session                    |
| fandaws:parentSessionId           | IRI \| null               | Parent session if this is a nested negotiation             |
| fandaws:nestingDepth              | integer                   | Current nesting depth (0 = root session)                   |
| fandaws:dialogueHistory           | DialogueTurn\[\]          | Ordered record of all prompts and responses                |
| fandaws:createdAt                 | dateTime                  | When the session was created                               |
| fandaws:lastActiveAt              | dateTime                  | When the session last received input                       |
| fandaws:expiresAt                 | dateTime \| null          | When the session will auto-expire (null = no expiry)       |

# 5. Core Workflows

Fandaws operates through a conversational loop in which the user teaches the system by making natural-language statements. Each statement is parsed, classified, and routed to one of three knowledge-building workflows. All workflows produce GraphMutation nodes that are validated before application.

## 5.1 Conversational Knowledge Entry Pipeline

The primary interaction pattern follows this pipeline:

1.  User states a fact in natural language.

2.  NLParser extracts subject, predicate, and object from the utterance.

3.  ScopeResolver checks whether the subject and object already exist in higher-scope graphs (context → user → global). If found, the concept is copied into the local graph with a fandaws:resolvedFrom annotation. If a cross-scope conflict is detected, a ConversationPrompt is emitted for conflict resolution before proceeding. If not found, the pipeline proceeds with normal concept creation.

4.  Classifier determines the workflow based on verb type.

5.  KnowledgeEngine executes the workflow, potentially emitting ConversationPrompts for disambiguation.

6.  Validator checks the proposed GraphMutation against structural integrity rules.

7.  StateAdapter applies the validated mutation to the KnowledgeGraph.

8.  DescriptionEngine regenerates descriptions for affected concepts.

Each step in this pipeline is a pure computation that can be executed synchronously in a browser. The OrchestrationAdapter manages the sequencing and user interaction between steps. Step 3 (ScopeResolver) requires read access to scope graphs via the StateAdapter; if no ScopeConfiguration is loaded (single-graph mode), this step is a no-op and the pipeline behaves identically to v3.2.

## 5.2 Classification Workflow (“X is a Y”)

The classification workflow establishes type hierarchies between concepts. When a user states “A dog is an animal,” the system creates or locates both concepts and establishes a parent-child relationship.

### 5.2.1 Procedure

1.  Parse the statement to extract subject (X) and object (Y).

2.  Apply Identity Simplification to both terms.

3.  Search the existing graph for matching concepts (case-insensitive, trimmed).

4.  If Y exists with multiple meanings, emit a Disambiguation prompt.

5.  If X already exists, check for circular hierarchy (Sanity Check).

6.  Run Termidium deduplication within 8 hierarchy levels.

7.  Emit GraphMutation: create X if new, set X.parent = Y, update Y.children.

8.  Regenerate descriptions for X and all affected ancestors.

### 5.2.2 Ambiguity Handling

When the target parent concept Y has multiple existing meanings (homonyms), the system emits a Disambiguation ConversationPrompt listing all known meanings with their auto-generated descriptions. The user selects the intended meaning, and the workflow continues with the selected concept. If the user indicates none of the existing meanings match, a new concept node is created for Y.

## 5.3 Property Workflow (“X has Y”)

The property workflow attaches characteristics to concepts. When a user states “A dog has fur,” the system determines the appropriate hierarchy level for the property and attaches it there.

### 5.3.1 Procedure

1.  Parse the statement to extract concept (X) and property (Y).

2.  Locate concept X in the graph. If not found, prompt user to classify it first.

3.  Run Property Redundancy Prevention (four checks — see Section 6.3).

4.  Begin Scope Narrowing: starting from X, walk up the hierarchy asking “Does \[ancestor\] also have \[Y\]?”

5.  The property is attached at the highest level where the user confirms it applies.

6.  Emit GraphMutation: add Property node, attach to determined concept.

7.  Regenerate descriptions for the target concept and all descendants that inherit the property.

### 5.3.2 Scope Narrowing

Scope narrowing is the iterative process of determining the most general concept to which a property applies. The system walks from the stated concept upward through its ancestors, asking the user at each level whether the property holds. This ensures properties are attached at the correct generality level, preventing redundant property declarations at more specific levels.

## 5.4 Custom Relationship Workflow (“X \[verb\] Y”)

The custom relationship workflow handles any verb form that is not “is” or “has.” When a user states “Dogs chase cats,” the system creates a named relationship with “chase” as the verb.

### 5.4.1 Procedure

1.  Parse the statement to extract subject (X), verb, and object (Y).

2.  Locate X and Y in the graph. Create placeholder concepts if needed.

3.  Run Custom Relationship Validation (seven checks — see Section 6.4).

4.  Determine if the verb matches an existing relationship type or requires a new one.

5.  If a matching verb exists at a more general level, create as sub-relationship.

6.  Emit GraphMutation: add Relationship node with subject, verb, object, and hierarchy position.

### 5.4.2 Relationship Hierarchy

Custom relationships form their own type hierarchy, independent of the concept hierarchy. When a verb is used at multiple specificity levels (e.g., “animals eat food” and “dogs eat meat”), the more specific relationship becomes a sub-relationship of the more general one. This enables inheritance reasoning: if animals eat food, and dogs are animals, then dogs eat food—but the specific assertion that dogs eat meat provides more precise information.

## 5.5 Term Explorer

The Term Explorer provides keyword search across the knowledge graph, returning matching concepts with their auto-generated definitions. This is a read-only computation that operates entirely on the in-memory or locally stored graph.

**Input:** A search string.

**Output:** An array of matching Concept nodes with descriptions, sorted by relevance (exact match first, then partial match, then label similarity).

## 5.6 Dictionary Lookup

Dictionary lookup retrieves external definitions for terms. This is an Integration-layer operation that gracefully degrades when offline.

**Online behavior:** Query the IntegrationAdapter for dictionary definitions. Cache results as JSON-LD with a staleness timestamp.

**Offline behavior:** If a cached result exists and is less than 24 hours old, serve it. If stale or absent, return a DeferredResult with the term queued for lookup when connectivity is restored.

**Degraded behavior:** If a cached result exists but is stale (older than 24 hours), serve the stale result immediately and queue a background refresh. Clearly mark the result as potentially stale.

## 5.7 Knowledge Export

The ExportEngine transforms the canonical JSON-LD KnowledgeGraph into external ontology formats. Each export is a deterministic, read-only transformation.

|            |               |                                                                                                              |
|------------|---------------|--------------------------------------------------------------------------------------------------------------|
| **Format** | **Standard**  | **Mapping Strategy**                                                                                         |
| SKOS       | W3C SKOS Core | Concepts → skos:Concept, hierarchies → skos:broader/narrower, descriptions → skos:definition                 |
| OWL        | W3C OWL 2     | Concepts → owl:Class, properties → owl:ObjectProperty or owl:DatatypeProperty, hierarchies → rdfs:subClassOf |
| RDF/XML    | W3C RDF       | Direct serialization of the JSON-LD graph into RDF/XML syntax                                                |
| Turtle     | W3C Turtle    | Compact serialization of the JSON-LD graph into Turtle syntax                                                |

## 5.8 Graph Visualization

Fandaws provides real-time, physics-based graph visualization of the knowledge graph. In the edge-canonical model, visualization is rendered client-side using the graph data from the JSON-LD KnowledgeGraph. The visualization module reads the graph state and renders it; it does not modify the graph. Any user interactions with the visualization (e.g., clicking a node to explore it) are routed back through the OrchestrationAdapter.

## 5.9 Machine-to-Machine Conversation Protocol

When the caller is an agent rather than a human, the conversational knowledge entry pipeline (Section 5.1) operates identically at the computation layer but with two presentation-layer differences managed by the OrchestrationAdapter.

### 5.9.1 Structured Negotiation

Every ConversationPrompt emitted during M2M operation includes a populated machineSignal field (Section 4.2.6). This transforms the conversational handshake from a natural-language question-and-answer into a structured API negotiation. The upstream agent receives a JSON Schema describing the expected response shape, enumerated valid values where applicable, and candidate concept IRIs for direct selection.

Example M2M negotiation flow:

1. Agent A asserts: "The suspect was anxious."
2. NLParser extracts subject="suspect", predicate="has", object="anxious".
3. KnowledgeEngine determines "anxious" could be a Property (permanent characteristic) or a subtype of a temporal state (bfo:Occurrent).
4. OrchestrationAdapter emits ConversationPrompt with machineSignal containing: expectedSchema for a single-selection response, validValues = \["property", "temporalState"\], constraintType = "inherence", and hierarchyContext showing the relevant subgraph.
5. Agent A responds with structured selection: {"selection": "temporalState"}.
6. KnowledgeEngine creates BFO alignment to bfo:Occurrent and attaches accordingly.

The computation pipeline does not change between human and M2M modes. The difference is strictly in how ConversationPrompts are presented and how responses are received — a concern of the OrchestrationAdapter, not of core computation.

### 5.9.2 Convergence Guarantee

M2M interactions can occur at millisecond speeds, creating a risk of unbounded retry loops if an agent persistently attempts to assert facts that the Validator rejects. The OrchestrationAdapter enforces the repetitionLimit configuration parameter (Section 11.1) as a runtime constraint, not merely a test constraint. When the limit is reached, the OrchestrationAdapter triggers a Semantic Deadlock event (Section 6.7) and emits an EpistemicFailure result to the caller rather than continuing the negotiation. See Section 6.7 for the full deadlock prevention specification.

### 5.9.3 Semantic Firewall Properties

The scope narrowing, disambiguation, and validation workflows function as a semantic firewall in M2M contexts. Specifically:

- **Scope Narrowing** (Section 5.3.2) forces the calling agent to commit to a specific level of abstraction, preventing property pollution at inappropriate hierarchy levels.
- **Disambiguation** (Section 5.2.2) forces the calling agent to resolve homonyms explicitly, preventing concept drift across multiple agent interactions.
- **Termidium** (Section 6.2) prevents agents from creating redundant concept nodes that would fragment the knowledge graph over time.
- **Property Redundancy Prevention** (Section 6.3) prevents agents from attaching properties that are already inherited, maintaining clean hierarchical inheritance.

These validation steps impose a small per-assertion cost but prevent the combinatorial cost of graph corruption that would require full audit and reconstruction downstream.

## 5.10 Scope Resolution Workflow

Before the Classifier and KnowledgeEngine process a term, the ScopeResolver checks whether the term already has a definition in a higher-scope graph. This prevents redundant definitions and surfaces cross-scope conflicts early.

### 5.10.1 Procedure

1. NLParser extracts subject and object terms from the utterance.
2. For each extracted term, the ScopeResolver searches the scope hierarchy (Section 3.2.7).
3. If a term is found in a higher scope (status="resolved"):
   a. The concept, its parent chain, direct properties, and direct relationships are copied into the local working graph.
   b. Each copied node carries a fandaws:resolvedFrom annotation (Section 4.2.11).
   c. The pipeline continues with the resolved concept in place — the KnowledgeEngine uses the copied concept rather than creating a new one.
4. If a cross-scope conflict is detected (status="conflict"):
   a. The OrchestrationAdapter emits a ConversationPrompt presenting the conflicting definitions and resolution options (Section 5.11).
   b. The pipeline pauses until the caller resolves the conflict.
5. If the term is not found in any scope (status="unknown"):
   a. The pipeline proceeds with normal concept creation in the local working graph.
6. If scope graphs were unavailable during resolution, the skipped scopes are recorded. The OrchestrationAdapter may re-run scope resolution when connectivity is restored.

### 5.10.2 Scope Graph Loading

Scope graphs are loaded via the StateAdapter. The ScopeResolver calls loadGraph(graphId) for each scope in the hierarchy. The StateAdapter is responsible for knowing how to fetch each graph — from local memory, IndexedDB, the local file system, or a locally cached IPFS snapshot. The ScopeResolver does not know or care about the storage mechanism.

For global scope graphs published to IPFS, the StateAdapter resolves the IPFS CID to a local cache path. If the CID is not cached, the StateAdapter returns null and the ScopeResolver treats this as an unavailable scope (DeferredResult).

### 5.10.3 Copy-on-Resolve Semantics

When a concept is copied from a higher scope into the local graph, the copy is a full structural copy: the concept node, its parent chain up to the root, all direct properties, and all direct relationships. This ensures the local graph is self-contained for offline operation — the user can continue building knowledge that depends on the resolved concept even if the source scope becomes unavailable.

The fandaws:resolvedFrom annotation is metadata, not a live reference. The local copy does not auto-update when the source scope changes. If the source scope is updated, the ScopeResolver will detect the version mismatch on the next resolution attempt and may flag a stale copy for review.

**Stale Copy Detection:** When resolving a term that already exists in the local graph with a fandaws:resolvedFrom annotation, the ScopeResolver compares the graphVersion of the local copy's annotation to the current version of the source graph. If they differ, the source concept has changed since the local copy was made. The ScopeResolver's response is controlled by the fandaws:staleCopyAction configuration parameter:

- **prompt** (default) — Emit a ConversationPrompt asking the caller whether to update the local copy, keep the local version, or fork. In M2M mode, the machineSignal includes the old and new definitions for programmatic comparison.
- **auto-update** — Silently replace the local copy with the current upstream version. The previous local copy is preserved in a fandaws:previousVersion annotation for audit. This mode is appropriate for global scope graphs with trustLevel="authoritative" where the upstream is the source of truth.
- **ignore** — Keep the local copy unchanged. The version mismatch is logged but no action is taken. This mode is appropriate for stable, slowly evolving scope graphs.
- **fork** — Automatically detach the local copy from its upstream source. The fandaws:resolvedFrom annotation is removed and replaced with a fandaws:forkedFrom annotation recording the original source, the version at which the fork occurred, and a timestamp. The concept becomes a fully local concept with no upstream dependency. This mode is essential for M2M contexts where the "prompt" action is not viable and upstream refactoring (e.g., splitting a concept into two) would corrupt the local reasoning history. Forking preserves the integrity of all local assertions that depend on the concept as it was when originally resolved.

The staleCopyAction can be set globally or overridden per-scope in the ScopeConfiguration. For example, a federation may set staleCopyAction="auto-update" for its BFO Core graph (authoritative, rarely changes) and staleCopyAction="fork" for its experimental-tier graphs (likely to refactor).

## 5.11 Cross-Scope Conflict Resolution

When the ScopeResolver detects that the same term has incompatible definitions in different scopes, the OrchestrationAdapter presents the conflict to the caller for resolution.

### 5.11.1 Conflict Presentation

The ConversationPrompt for a cross-scope conflict includes:

- The term in question.
- Each conflicting definition with its scope type, source graph, IS_A chain, and properties.
- Resolution options (Section 4.2.10 ResolutionOption).

In M2M mode, the machineSignal on the ConversationPrompt includes the full ConflictReport with candidate IRIs for each definition, enabling the upstream agent to select a resolution programmatically.

### 5.11.2 Resolution Actions

Three resolution actions are supported:

1. **useDefinition** — Select one of the existing definitions. The selected definition's concept is copied into the local graph via copy-on-resolve. The unselected definitions are noted in the session metadata but not imported.

2. **createDistinct** — Treat the conflicting definitions as genuinely different concepts. The caller provides disambiguated names (e.g., "moral autonomy" and "political autonomy"). Both concepts are copied into the local graph with their respective scope annotations, and a fandaws:disambiguatedFrom annotation links them to the original shared term.

3. **refine** — Reject all existing definitions and start a new negotiation to define the term from scratch in the local working graph. The new definition exists only at the current scope level. Because the new local definition deliberately overrides a definition that exists in a higher scope, the locally created concept carries a **fandaws:shadows** annotation recording the scope type, graph ID, and concept IRI of each overridden definition. This annotation serves as a warning to downstream consumers (FNSR, IEE) that this concept is a local override, not a universally agreed-upon definition.

   **Mandatory Disambiguation:** To prevent silent shadowing — where a local concept with the same name as a global concept creates ambiguity for downstream consumers — the OrchestrationAdapter must prompt the caller to provide a disambiguated display label when refine is chosen (e.g., "autonomy (local)" or "moral autonomy"). The canonical label may remain the same for local matching purposes, but the display label must differ from the shadowed concept's display label. In M2M mode, the machineSignal includes the shadowed concept's display label and a constraint requiring the new label to differ.

### 5.11.3 Conflict Logging

All conflict detections and resolutions are logged as GraphMutations with mutationType="conflictResolution", preserving the full ConflictReport and the chosen resolution action. This enables downstream consumers (FNSR, IEE) to track how semantic disagreements are resolved.

## 5.12 Session Lifecycle

A ConversationSession (Section 4.2.12) tracks the state of an ongoing negotiation. The OrchestrationAdapter manages session lifecycle; the core pipeline is session-unaware.

### 5.12.1 Session States

| State       | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| negotiating | Active session, caller is answering questions                               |
| paused      | Caller explicitly paused; session persisted for later resumption            |
| nested      | Session is suspended while a nested negotiation (for a parent or property) completes |
| conflict    | Session is suspended pending cross-scope conflict resolution                |
| complete    | Negotiation finished; term committed to the knowledge graph                 |
| abandoned   | Caller explicitly abandoned; partial state archived but not committed       |
| expired     | Session exceeded its inactivity timeout without being paused or completed   |

### 5.12.2 Pause and Resume

A caller may pause a session at any point during negotiation. The OrchestrationAdapter persists the full ConversationSession (including dialogue history, current phase, and pending mutations) via the StateAdapter. Paused sessions are available for resumption until they expire.

On resume, the OrchestrationAdapter reloads the session and presents the last unanswered ConversationPrompt. The pipeline state is reconstructed from the session's dialogue history — no mutable in-memory state is assumed between pause and resume.

**Expiration:** Paused sessions expire after the configured sessionExpiryDuration (Section 11.1, default: P7D — 7 days). Expired sessions transition to the "expired" state and are archived. The OrchestrationAdapter may notify the caller when a paused session is about to expire.

### 5.12.3 Nested Negotiation

When the pipeline encounters an unknown parent or property during negotiation (e.g., "A dog is a canine" where "canine" does not exist in any scope), it must define "canine" before it can complete "dog." This creates a nested negotiation.

1. The current session transitions to state="nested" and records the pending assertion.
2. A child session is created with parentSessionId pointing to the current session and nestingDepth incremented by 1.
3. The child session runs a normal negotiation for the unknown term.
4. When the child session completes, the OrchestrationAdapter resumes the parent session with the newly defined concept available.

**Nesting Depth Limit:** The maximum nesting depth is controlled by maxNestingDepth (Section 11.1, default: 10). If a negotiation would exceed this depth, the OrchestrationAdapter emits a ConversationPrompt suggesting the caller use an existing concept instead of defining a new one. In M2M mode, this is surfaced as an EpistemicFailure with suggestedActions listing candidate existing concepts from the scope hierarchy.

### 5.12.4 Abandon

A caller may abandon a session at any point. Abandoned sessions are archived with their full dialogue history for audit purposes, but no partial mutations are committed to the knowledge graph. Any nested child sessions are also abandoned.

### 5.12.5 Concurrent Session Limits

A single caller may have at most maxConcurrentSessions (Section 11.1, default: 5) active sessions (state="negotiating" or "nested") simultaneously. Paused sessions do not count toward this limit. If the limit is exceeded, the OrchestrationAdapter rejects the new session and suggests resuming or abandoning an existing one.

## 5.13 Term Promotion

Term promotion is the process of publishing a concept from a lower scope to a higher scope, making it available to a wider audience. In the edge-canonical architecture, promotion means publishing the concept (and its dependencies) to an IPFS-addressable graph that other users can add to their global federation.

### 5.13.1 Promotion Path

Promotion follows the scope hierarchy upward:

1. **Context → User:** When a context-scope session completes, the caller may promote negotiated terms to their user-scope graph. This is a local operation — the concept and its dependencies are copied from the context graph into the user graph with fandaws:promotedFrom provenance.

2. **User → Global:** The caller publishes their user-scope graph (or a curated subset) to IPFS via the HIRI protocol (Section 10.5.3). Once published, the graph has an immutable CID that other users can add to their globalFederation search path. Publication is an adapter concern — the core pipeline only provides the export; the HIRI/IPFS adapter handles pinning and distribution.

### 5.13.2 Curator Review

For quality control, a global federation may designate curators (Section 11.2) who review proposed additions before they enter the federation's resolution order. The curation workflow is:

1. A caller publishes their graph to IPFS and submits the CID to the federation's curation channel (adapter-specific: could be a pull request, a shared document, or a dedicated review queue).
2. A curator reviews the graph for ontological quality: well-formed IS_A chains, no orphan concepts, consistent BFO alignment.
3. If approved, the curator adds the graph's ScopeEntry to the federation's canonical ScopeConfiguration with an appropriate priority and trustLevel.
4. Other users who subscribe to the federation's ScopeConfiguration will see the new graph in their global scope on their next session initialization.

Curation is not part of the core pipeline. The core specification defines the ScopeConfiguration contract; curation workflows are governance concerns managed by the community operating the federation.

### 5.13.3 Algorithmic Curation

Human curator review (Section 5.13.2) is the quality gate for the "authoritative" trust tier. However, in M2M environments, agents generate new concepts faster than humans can curate. To prevent curation from becoming a bottleneck, federations may define algorithmic promotion rules for the lower trust tiers.

**Auto-Promotion to "community" tier:** A concept published to IPFS is eligible for automatic promotion to a federation's "community" trust tier if all of the following conditions are met:

1. The concept has been resolved (copy-on-resolve) by at least autoPromotionThreshold (Section 11.1, default: 3) distinct user graphs, as verified via HIRI provenance logs.
2. The concept has no active EthicalContestationFlags from any IEE instance (no blocking, warning, or advisory flags).
3. The concept passes structural validation: well-formed IS_A chain, no orphan nodes, BFO alignment present.
4. The concept has been published for at least autoPromotionCooldown (Section 11.1, default: P7D — 7 days).

When all conditions are met, the federation's OrchestrationAdapter may automatically add the concept's source graph to the ScopeConfiguration at trustLevel="community" without curator intervention.

**Promotion from "community" to "authoritative":** Promotion to the "authoritative" tier always requires human curator review. Algorithmic promotion only applies to the "experimental" → "community" transition.

**Override:** Curators may demote or remove any auto-promoted graph at any time. Auto-promotion does not bypass the curator's authority — it reduces the curator's workload by pre-filtering concepts that have already demonstrated community adoption and ethical safety.

### 5.13.4 Verification and Endorsement

When multiple callers resolve the same concept from a global-scope graph, the resolution events serve as implicit endorsements. The OrchestrationAdapter may track a fandaws:usageCount on resolved concepts. Concepts with high usage counts across different callers gain community trust, while concepts with zero usage may be candidates for pruning from the federation.

Explicit endorsement is also supported: a caller can attach a fandaws:endorsement annotation to a resolved concept, recording their callerId, a timestamp, and an optional comment. Endorsements are metadata on the local copy; they can be aggregated across published graphs by downstream consumers.

# 6. Validation Rules

All validation rules are implemented as pure functions within the Validator module. They accept a proposed GraphMutation and the current KnowledgeGraph and return a ValidationResult. No validation rule may perform I/O or modify state.

## 6.1 Input Sanitization

All user input undergoes sanitization before entering the computation pipeline. Sanitization is deterministic and produces identical output for identical input.

- Trim leading and trailing whitespace.

- Normalize to canonical form via Identity Simplification (Section 6.6). The original input is preserved as fandaws:displayLabel; the normalized form is stored as fandaws:canonicalLabel and used for all matching and deduplication.

- Reject compound statements (multiple subjects). Response: ValidationRejection with reason="compoundStatement" and message="Input contains multiple subjects. Please state one fact at a time."

- Reject structurally ungroundable concepts. A concept assertion is ungroundable if the proposed concept satisfies none of the following: (a) it is being classified under an existing parent, (b) it already exists in the graph with at least one parent, (c) it carries the fandaws:allowRoot flag, or (d) it has at least one typed property. Ungroundable concepts are rejected with reason="structuralGroundingError" and a message indicating what structural requirement is missing (e.g., "Concept 'truth' has no parent classification. Please classify it first: 'Truth is a [category].'").

- At confirmation steps, accept only yes/no responses. All other input triggers a re-prompt.

## 6.2 Termidium (Deduplication)

Termidium is the deduplication engine that prevents redundant concept nodes in the knowledge graph. It operates on a bounded search scope and runs recursively until no further merges are found.

### 6.2.1 Algorithm

1.  Starting from the newly created or modified concept, search upward and downward within 8 hierarchy levels for concepts with matching labels.

2.  If a match is found, determine which concept is deeper in the hierarchy.

3.  Merge the shallower concept into the deeper one, transferring all properties, relationships, and child connections.

4.  Run the search again from the merge result to catch transitive duplicates.

5.  Repeat until no further matches are found.

### 6.2.2 Merge Semantics

When two matching concepts are found, the merge target (the concept that survives) is determined by the following ordered policy:

1. **Depth priority:** The deeper concept (farther from root) survives. The shallower concept is merged into it.
2. **Tie-breaking by creation time:** If both concepts are at the same depth, the concept with the earlier fandaws:createdAt timestamp survives.
3. **Tie-breaking by assertion count:** If creation times are identical (e.g., bulk import), the concept with more direct children, properties, and relationships survives.

When merging concept A (source) into concept B (target), the following rules apply:

- All children of A become children of B.
- All properties of A are added to B, subject to Property Redundancy Prevention (Section 6.3). Conflicting properties (same predicate, different value) are preserved as alternatives with the source annotated.
- All relationships referencing A are rewritten to reference B.
- Concept A's IRI is recorded on B as fandaws:mergedFrom (an array of IRIs). This preserves provenance so that external systems holding references to A's IRI can trace it to B.
- Concept A is deleted from the graph.
- Descriptions are regenerated for B and all affected nodes.

**Large Merge Threshold:** If a merge operation would affect more than the configured mergeReviewThreshold (Section 11.1, default: 10) child concepts, the merge is not applied automatically. Instead, it is emitted as a ConversationPrompt of type "mergeReview" presenting the proposed merge and requesting confirmation. In M2M mode, the machineSignal includes the full merge plan (source IRI, target IRI, affected concept count, and a list of property conflicts). This prevents automated agents from silently restructuring large portions of the graph.

## 6.3 Property Redundancy Prevention

Four checks prevent redundant property declarations:

1.  No Duplicates: The exact property must not already exist on the target concept.

2.  No Ancestor Overlap: The property must not already exist on any ancestor of the target (it would be inherited).

3.  No Descendant Overlap: If the property already exists on a descendant, attaching it at a higher level makes the descendant’s copy redundant (descendant copy is removed).

4.  No Inherited Redundancy: The property must not be logically entailed by the combination of existing properties and hierarchy position.

## 6.4 Custom Relationship Validation

Seven checks validate custom relationship operations:

1.  Verb Normalization: Standardize verb forms (lemmatization) before matching.

2.  Duplicate Check: Reject if an identical relationship (same subject, verb, object) already exists.

3.  Inverse Check: Detect and flag potential inverse relationships (e.g., “chases” vs. “is chased by”).

4.  Hierarchy Consistency: Ensure the relationship does not contradict existing hierarchy relationships.

5.  Reuse Assessment: Determine if an existing relationship type can be reused for this verb.

6.  Promotion Check: Determine if a sub-relationship should be promoted to a primary relationship.

7.  Refactoring Check: Determine if existing relationships should be refactored based on the new addition.

## 6.5 Sanity Check (Circular Hierarchy Prevention)

Before establishing any parent-child relationship, the Sanity Check verifies that no circular path would be created. Starting from the proposed parent, it walks up the hierarchy to the root. If the proposed child is encountered during this traversal, the operation is rejected. This check is O(d) where d is the depth of the hierarchy.

## 6.6 Identity Simplification

Identity Simplification reduces complex, multi-word terms to clean concept names for matching and deduplication. The simplification process is deterministic: given the same input term, it always produces the same simplified form.

**Dual-Label Model:** Every concept maintains two label fields:

- **fandaws:displayLabel** — the original input as provided by the user or agent, preserving case, diacritics, and language-specific characters. This is the human-readable form shown in descriptions, exports, and UI.

- **fandaws:canonicalLabel** — the normalized form used for all matching, deduplication, and Termidium operations. This is the output of Identity Simplification applied to displayLabel.

**Normalization Rules:** The canonicalLabel is produced by the following deterministic pipeline:

1. Trim leading and trailing whitespace.
2. Collapse internal whitespace sequences to a single space.
3. Remove leading articles in the configured locale (English default: "a", "an", "the").
4. Apply Unicode NFKC normalization to resolve compatibility equivalences (e.g., ligatures, width variants).
5. Apply locale-aware case folding (not simple ASCII lowercasing). For English, this is standard toLowerCase(). For Turkish, dotted/dotless I is handled correctly. For languages without case (CJK, Arabic, Hebrew), this step is a no-op.
6. Apply domain-specific abbreviation expansion from a configurable abbreviation table.
7. Apply language tag: canonicalLabel carries an optional BCP 47 language tag (e.g., "en", "tr", "zh") to prevent cross-language false matches.

**Matching:** Two concepts match if and only if their canonicalLabels are identical (including language tag, if present). The displayLabel is never used for matching.

**Configuration:** The locale, article list, and abbreviation table are configuration parameters (Section 11.1). The default locale is "en".

## 6.7 Semantic Deadlock Prevention

In machine-to-machine contexts, a persistent upstream agent may repeatedly attempt to assert facts that the Validator rejects, creating an unbounded validation loop. Semantic deadlock prevention is a runtime constraint that guarantees convergence.

### 6.7.1 Detection

The OrchestrationAdapter tracks, per session, a rejection counter for each (conceptId, mutationType) pair. A semantic deadlock is detected when the rejection count for any pair exceeds the configured repetitionLimit (Section 11.1, default: 5). Rephrased assertions that resolve to the same conceptId and mutationType through Identity Simplification (Section 6.6) are counted as the same pair — the agent cannot evade the limit by surface-level rephrasing.

### 6.7.2 Resolution

When a semantic deadlock is detected, the OrchestrationAdapter applies a graduated remediation sequence. Each step is attempted in priority order; the sequence advances only if the previous step fails to resolve the deadlock.

1. **Auto-Repair Suggestion:** The OrchestrationAdapter examines the aggregated rejection reasons and, where possible, generates a repair suggestion. For example, if the rejection is "concept X has no parent," the suggestion is "classify X under [nearest plausible parent from graph]." If OCE (Section 10.4.3) is available and has returned repairPaths for the violation, those paths are included in the suggestion. In M2M mode, the repair suggestion is emitted as a ConversationPrompt with machineSignal containing the suggested GraphMutation that would resolve the prerequisite.

2. **Deferred Resolution:** If the rejection is caused by missing information that no auto-repair can address (e.g., a concept that depends on an unresolved DeferredResult from an offline IntegrationAdapter), the OrchestrationAdapter emits a DeferredResult with reason="semanticDeadlock" and queues the assertion for retry after the prerequisite information is available.

3. **Human Escalation:** If the caller is an agent (M2M mode) and both auto-repair and deferral have failed, the OrchestrationAdapter may escalate to a human review queue. The escalation event includes the full rejection history, the proposed mutation, and any OCE repairPaths. This step is optional and requires an OrchestrationAdapter that supports a human-in-the-loop channel. If no human channel is available, the sequence proceeds to step 4.

4. **Epistemic Failure:** If all preceding steps have been exhausted, the OrchestrationAdapter emits an EpistemicFailure event, declaring that the assertion cannot be grounded in the current graph state.

**EpistemicFailure Schema:**

|                          |                            |                                                           |
|--------------------------|----------------------------|-----------------------------------------------------------|
| **Field**                | **Type**                   | **Description**                                           |
| @type                    | fandaws:EpistemicFailure   | Type discriminator                                        |
| fandaws:conceptId        | IRI                        | The concept the agent was attempting to modify             |
| fandaws:mutationType     | string                     | The type of mutation that was rejected                     |
| fandaws:attemptCount     | integer                    | Number of attempts before deadlock was declared            |
| fandaws:rejectionReasons | string\[\]                 | Aggregated reasons from all ValidationResults              |
| fandaws:suggestedActions | string\[\]                 | Constructive suggestions (e.g., "classify X before attaching properties to it") |
| fandaws:repairPaths      | object\[\] \| null         | OCE repair paths, if available                             |
| fandaws:escalatedToHuman | boolean                    | Whether human escalation was attempted                     |

**Rate Limiting:** In M2M mode, the OrchestrationAdapter may apply per-agent rate limiting (configurable via agentRateLimit in Section 11.1) to prevent a single agent from consuming disproportionate pipeline capacity through repeated deadlock cycles.

### 6.7.3 Logging

Every deadlock detection and resolution is logged as a GraphMutation with mutationType="deadlockResolution" to maintain full auditability. The rejection history is preserved so that downstream consumers (FNSR, IEE) can analyze patterns of failed assertions.

### 6.7.4 Scope

Semantic deadlock prevention is a runtime constraint enforced by the OrchestrationAdapter. It is not a Validator concern — the Validator remains a pure function that evaluates individual mutations. The deadlock detector operates at the session level, tracking patterns across multiple Validator invocations. This preserves the separation of concerns (Section 2.4): computation (Validator) remains stateless; orchestration (deadlock tracking) manages session-level state.

# 7. Upper Ontology Alignment

Fandaws aligns its knowledge structures with Basic Formal Ontology (BFO), providing philosophical grounding and interoperability with the broader ontology ecosystem. BFO alignment is performed through the IntegrationAdapter and gracefully degrades when offline.

## 7.1 BFO Category Mapping

Fandaws maps concepts to BFO’s top-level categories. The mapping is stored as the fandaws:bfoMapping property on each concept. When the BFO integration is unavailable, concepts are created without a mapping and flagged for deferred alignment.

|                      |                          |                             |
|----------------------|--------------------------|-----------------------------|
| **BFO Category**     | **Fandaws Concept Type** | **Example**                 |
| bfo:Entity           | Root concepts            | thing, entity               |
| bfo:Continuant       | Objects, substances      | dog, water, table           |
| bfo:Occurrent        | Processes, events        | running, photosynthesis     |
| bfo:Quality          | Properties, attributes   | color, weight, temperature  |
| bfo:Role             | Functional roles         | teacher, predator, catalyst |
| bfo:Disposition      | Tendencies, capacities   | fragility, solubility       |
| bfo:RealizableEntity | Realizable properties    | function, capability        |

## 7.2 Relationship Type Mapping

Fandaws’ three relationship types (is-a, has, custom) map to BFO’s formal relations. The is-a relationship maps to rdfs:subClassOf. The has relationship maps to BFO’s “bearer of” (for qualities) or “has part” (for structural components). Custom relationships are mapped to the most specific applicable BFO relation, or left unmapped with an explicit “unmapped” annotation.

## 7.3 Offline BFO Alignment

When the BFO integration is unavailable, Fandaws applies a local heuristic alignment based on linguistic patterns. Concepts containing process-related words (e.g., “-ing”, “-tion”) are tentatively aligned to bfo:Occurrent. Concepts with quality-related words (e.g., “-ness”, “-ity”) are tentatively aligned to bfo:Quality. All heuristic alignments are marked as provisional and queued for verification when the integration becomes available.

# 8. Caching and Offline Behavior

Fandaws treats offline operation as a first-class mode, not an error state. All external dependencies are mediated through the IntegrationAdapter, and every integration method defines explicit behavior for three connectivity states.

## 8.1 Connectivity States

|           |                                                   |                                                                                                                                              |
|-----------|---------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| **State** | **Definition**                                    | **System Behavior**                                                                                                                          |
| Online    | IntegrationAdapter methods succeed within timeout | Full functionality. Cache results for future offline use.                                                                                    |
| Degraded  | Some methods succeed, others fail or timeout      | Use cached results where available. Emit DeferredResult for unavailable operations. Continue core computation.                               |
| Offline   | No IntegrationAdapter methods succeed             | Use cached results exclusively. All integration operations return DeferredResult. Core knowledge-building workflows remain fully functional. |

## 8.2 Cache Strategy

Caching is implemented in the StateAdapter, not in core computation modules. Cache entries are JSON-LD nodes with staleness metadata.

**Fresh cache:** Entry is less than 24 hours old. Served immediately without background refresh.

**Stale cache:** Entry is more than 24 hours old. Served immediately. Background refresh queued if online.

**Missing cache:** No entry exists. If online, fetch and cache. If offline, return DeferredResult.

The 24-hour staleness threshold is a configuration parameter, not a hardcoded value. It can be adjusted per integration type (e.g., dictionary definitions may tolerate longer staleness than BFO mappings).

## 8.3 Deferred Resolution Queue

When operations are deferred due to offline status, they are recorded as DeferredResult nodes in the session state. When connectivity is restored, the OrchestrationAdapter processes the queue in order, applying results to the knowledge graph and notifying the user of any changes that affect their current work.

# 9. Testing Strategy

Because all core computation is deterministic and infrastructure-free, Fandaws is inherently testable. Every module can be tested in isolation with JSON-LD fixtures, with no mocking of external services required.

## 9.1 Unit Testing

Each core computation module (NLParser, Classifier, KnowledgeEngine, Validator, DescriptionEngine, ExportEngine) is tested by providing JSON-LD input fixtures and asserting JSON-LD output matches expected results. Tests run in Node.js or in the browser with no setup beyond loading the module and fixtures.

## 9.2 Conversation Simulation Testing

Fandaws supports automated conversation simulation for integration testing. A test script provides a sequence of user utterances and expected system responses (using pattern matching). The OrchestrationAdapter replays the sequence, and assertions verify that the knowledge graph reaches the expected state.

**Execution limit:** Each test step is limited to the configured repetitionLimit (Section 11.1, default: 5) to prevent infinite loops in disambiguation or scope-narrowing sequences. This is the same runtime constraint enforced by the Semantic Deadlock Prevention mechanism (Section 6.7) — tests validate that the deadlock breaker activates correctly.

**Determinism requirement:** Given the same sequence of utterances and responses, the final knowledge graph state must be identical across runs.

## 9.3 M2M Simulation Testing

Machine-to-machine interactions are tested by running the OrchestrationAdapter in agent mode (callerMode="agent") with a scripted agent that responds to machineSignal fields on ConversationPrompts. Tests verify that: machineSignal is populated on every prompt, structured responses are correctly routed back into the pipeline, the semantic deadlock breaker fires after repetitionLimit consecutive rejections, and EpistemicFailure events are emitted with correct metadata. M2M simulation tests also verify pipeline throughput against the performance targets in Section 10.8.4.

## 9.4 Offline Testing

Offline behavior is tested by providing a NullIntegrationAdapter that returns DeferredResult for every method call. All core workflows must complete successfully with this adapter, demonstrating that the system functions without any external dependencies. Tests verify that deferred results are correctly queued, that cached results are served when available, and that no computation module throws or fails due to integration unavailability.

## 9.5 Export Validation

Each export format is validated against its respective standard. SKOS exports are validated against the SKOS data model. OWL exports are validated for OWL 2 DL consistency. RDF/XML and Turtle exports are validated for syntactic correctness. All validation is performed locally using bundled schema files.


# 10. Ecosystem Integration

## 10.1 Purpose and Scope

Fandaws is a foundational component in a broader ecosystem of semantic reasoning, AI governance, and domain application systems. Its knowledge graphs—concept hierarchies, property inheritance chains, custom relationship structures—serve as structured inputs for downstream reasoning, ethical evaluation, and operational automation.

This section defines the integration points between Fandaws and every system in the ecosystem. Each integration is classified into one of five tiers based on the directionality and nature of data flow. For each integration, this section specifies: the JSON-LD contract shape exchanged between systems, the adapter interface (if applicable), offline degradation behavior, and a narrative describing the integration’s purpose and mechanics.

All integrations are non-normative extensions. They do not alter Fandaws’ core architecture. They are implemented as IntegrationAdapter methods or as consumers of the KnowledgeGraph JSON-LD export. Fandaws must pass the Spec Test with all integrations disabled.

## 10.2 Integration Tier Model

The ecosystem is organized into five tiers reflecting the relationship between Fandaws and each connected system:

|          |                |                                                                                                |                                                   |
|----------|----------------|------------------------------------------------------------------------------------------------|---------------------------------------------------|
| **Tier** | **Direction**  | **Relationship to Fandaws**                                                                    | **Systems**                                       |
| Tier 1   | Upstream       | Data providers: supply raw material that Fandaws consumes to build knowledge                   | BFO, External Dictionaries, Imported Ontologies   |
| Tier 2   | Bidirectional  | Peer services: exchange structured data with Fandaws in both directions                        | TagTeam.js, SHML, Ontological Constraint Engine   |
| Tier 3   | Downstream     | Consumers: ingest Fandaws knowledge graphs as structured inputs for reasoning                  | FNSR, IEE, HIRI, ARCHON, Assay                    |
| Tier 4   | Downstream     | Domain applications: use Fandaws ontologies for specific operational purposes                  | Aligned Property Commons, Code-to-CAD, Eulogy Pen |
| Tier 5   | Infrastructure | Optional infrastructure: provide distribution, storage, and verification for Fandaws artifacts | IPFS                                              |

## 10.3 Tier 1 — Upstream Data Providers

Tier 1 systems supply raw semantic material that Fandaws consumes during knowledge building. These integrations are accessed through the IntegrationAdapter and all degrade gracefully when offline.

### 10.3.1 Basic Formal Ontology (BFO)

**Purpose:** Provide upper-ontology grounding for Fandaws concepts. Every concept in the knowledge graph can be aligned to a BFO category, enabling interoperability with the broader ontology ecosystem and philosophical coherence in downstream reasoning.

**Direction:** Upstream → Fandaws. BFO supplies category definitions; Fandaws consumes them.

**JSON-LD Contract: BFOAlignmentRequest**

Sent from the KnowledgeEngine to the IntegrationAdapter when a new concept requires BFO alignment:

|                          |                             |                                                                          |
|--------------------------|-----------------------------|--------------------------------------------------------------------------|
| **Field**                | **Type**                    | **Description**                                                          |
| @type                    | fandaws:BFOAlignmentRequest | Contract type discriminator                                              |
| fandaws:conceptId        | IRI                         | The concept to align                                                     |
| fandaws:conceptLabel     | string                      | Concept display name                                                     |
| fandaws:parentBFOMapping | IRI \| null                 | Parent concept’s BFO category, if known                                  |
| fandaws:linguisticHints  | string\[\]                  | Morphological features (e.g., -ing, -ness, -tion) for heuristic fallback |

**JSON-LD Contract: BFOAlignmentResult**

Returned by the IntegrationAdapter:

|                     |                            |                                                              |
|---------------------|----------------------------|--------------------------------------------------------------|
| **Field**           | **Type**                   | **Description**                                              |
| @type               | fandaws:BFOAlignmentResult | Contract type discriminator                                  |
| fandaws:conceptId   | IRI                        | The aligned concept                                          |
| fandaws:bfoCategory | IRI                        | Selected BFO category (e.g., bfo:Continuant)                 |
| fandaws:confidence  | float \[0,1\]              | Confidence in the alignment                                  |
| fandaws:method      | enum                       | How alignment was determined: integration, heuristic, manual |
| fandaws:provisional | boolean                    | True if alignment is heuristic and needs verification        |

**Offline Degradation**

When the BFO integration is unavailable, the KnowledgeEngine applies a local heuristic alignment based on morphological patterns. Concepts with process-related suffixes (-ing, -tion, -ment) are tentatively aligned to bfo:Occurrent. Concepts with quality-related suffixes (-ness, -ity, -ful) are tentatively aligned to bfo:Quality. All heuristic alignments are marked provisional=true and queued for verification. Core knowledge building is unaffected.

### 10.3.2 External Dictionaries

**Purpose:** Provide natural-language definitions for terms during knowledge building and term exploration.

**Direction:** Upstream → Fandaws.

**JSON-LD Contract: DictionaryLookupResult**

|                     |                                |                                                                 |
|---------------------|--------------------------------|-----------------------------------------------------------------|
| **Field**           | **Type**                       | **Description**                                                 |
| @type               | fandaws:DictionaryLookupResult | Contract type discriminator                                     |
| fandaws:term        | string                         | The looked-up term                                              |
| fandaws:definitions | Definition\[\]                 | Array of definitions with part-of-speech and source attribution |
| fandaws:cachedAt    | dateTime                       | When this result was cached                                     |
| fandaws:stale       | boolean                        | True if cached result is older than staleness threshold         |

**Offline Degradation**

Cached results are served when available (fresh or stale). Missing terms return a DeferredResult and are queued for lookup. Core knowledge building proceeds without definitions; descriptions will use hierarchy-based templates until dictionary data becomes available.

### 10.3.3 Imported Ontologies

**Purpose:** Import existing ontologies (OWL, SKOS, RDF) as seed knowledge for a Fandaws knowledge graph, enabling bootstrapping from established domain models.

**Direction:** Upstream → Fandaws.

**JSON-LD Contract: OntologyImportResult**

|                          |                              |                                                            |
|--------------------------|------------------------------|------------------------------------------------------------|
| **Field**                | **Type**                     | **Description**                                            |
| @type                    | fandaws:OntologyImportResult | Contract type discriminator                                |
| fandaws:sourceIRI        | IRI                          | Origin of the imported ontology                            |
| fandaws:concepts         | Concept\[\]                  | Extracted concepts mapped to Fandaws schema                |
| fandaws:relationships    | Relationship\[\]             | Extracted relationships                                    |
| fandaws:unmappedEntities | object\[\]                   | Entities that could not be cleanly mapped to Fandaws types |
| fandaws:importMethod     | enum                         | owl, skos, rdf, turtle                                     |

**Offline Degradation**

Ontology import requires the source file to be locally available (as a JSON-LD file or cached download). If the source is a remote IRI that cannot be fetched, the operation returns DeferredResult. Previously cached ontology files can be imported offline.

## 10.4 Tier 2 — Peer Services

Tier 2 systems exchange data bidirectionally with Fandaws. They may consume Fandaws knowledge graphs and also supply structured data that Fandaws incorporates. These integrations require dedicated adapter interfaces because data flows in both directions.

### 10.4.1 TagTeam.js

**Purpose:** TagTeam.js is a discourse-model semantic parser that can serve as an alternative NLParser implementation for Fandaws. Because the NLParser interface is defined as a pure computation contract (JSON-LD in, JSON-LD out), TagTeam.js can be swapped in as the parsing layer without modifying any other component.

**Direction:** Bidirectional. TagTeam.js receives raw utterances from the OrchestrationAdapter and returns ParseResult nodes. TagTeam.js may also consume the current KnowledgeGraph as parsing context to improve disambiguation.

**Integration Architecture**

TagTeam.js integrates at the NLParser boundary. The OrchestrationAdapter checks which parser implementation is configured and delegates accordingly. The key architectural distinction: TagTeam.js is a discourse-model system, not a world-model system. It parses what the user said and how they said it, not what the world is. This makes it complementary to Fandaws’ knowledge engine, which handles world-model commitments.

**JSON-LD Contract: TagTeamParseRequest**

|                             |                             |                                                                |
|-----------------------------|-----------------------------|----------------------------------------------------------------|
| **Field**                   | **Type**                    | **Description**                                                |
| @type                       | fandaws:TagTeamParseRequest | Contract type discriminator                                    |
| fandaws:utterance           | string                      | Raw user input text                                            |
| fandaws:conversationHistory | Utterance\[\]               | Recent conversation turns for discourse context                |
| fandaws:knowledgeGraphId    | IRI \| null                 | Optional reference to current graph for disambiguation context |

**JSON-LD Contract: TagTeamParseResult**

Must conform to the same ParseResult schema as the built-in NLParser:

|                              |                     |                                                                          |
|------------------------------|---------------------|--------------------------------------------------------------------------|
| **Field**                    | **Type**            | **Description**                                                          |
| @type                        | fandaws:ParseResult | Same type as built-in parser output                                      |
| fandaws:subject              | string              | Extracted subject term                                                   |
| fandaws:predicate            | string              | Extracted predicate (is, has, or custom verb)                            |
| fandaws:object               | string              | Extracted object term                                                    |
| fandaws:verbType             | enum                | classification, property, customRelationship                             |
| fandaws:confidence           | float \[0,1\]       | Parser confidence in extraction                                          |
| fandaws:parserImplementation | string              | tagteam-js (for provenance tracking)                                     |
| fandaws:discourseAnnotations | object \| null      | TagTeam-specific discourse metadata (speech act type, hedging, modality) |

**Adapter Interface: TagTeamAdapter**

|                   |                    |                                                 |
|-------------------|--------------------|-------------------------------------------------|
| **Method**        | **Returns**        | **Description**                                 |
| parse(request)    | ParseResult        | Parse utterance and return standard ParseResult |
| isAvailable()     | boolean            | Check if TagTeam.js is loaded and operational   |
| getCapabilities() | ParserCapabilities | Report which linguistic features are supported  |

**Offline Degradation**

TagTeam.js is designed for edge-canonical execution and runs entirely in the browser or Node.js. It has no external dependencies. If TagTeam.js is not loaded (e.g., not bundled in the deployment), the OrchestrationAdapter falls back to the built-in NLParser. This fallback is transparent to the rest of the pipeline.

### 10.4.2 Semantically Honest Middle Layer (SHML)

**Purpose:** SHML ensures that knowledge claims flowing through the ecosystem are framed with epistemic honesty—separating what is asserted from what is observed, what is provisional from what is committed, and what is discourse from what is reality. Fandaws knowledge graphs represent committed ontological structure; SHML governs how those commitments are presented and attributed.

**Direction:** Bidirectional. Fandaws exports committed knowledge claims to SHML. SHML returns attribution and framing metadata that Fandaws stores as provenance on its concepts.

**Integration Architecture**

SHML operates on a three-tier architecture: Reality Layer (BFO-grounded entities), Semantically Honest Middle Layer (assertions as events with provenance), and Logic Layer (materialized projections). Fandaws contributes to the Logic Layer by exporting committed concept hierarchies. SHML wraps these exports with epistemic metadata: who asserted this, when, with what evidence, and at what confidence level.

The critical insight is that Fandaws concepts are not raw observations—they are the product of conversational knowledge building. Every concept was stated by a user, parsed by the NLParser, validated by the Validator, and committed by the StateAdapter. This provenance chain maps directly to SHML’s “assertions as occurrents” model.

**JSON-LD Contract: SHMLAssertionWrapper**

When Fandaws exports a concept or relationship to SHML, it wraps the JSON-LD node in an assertion envelope:

|                       |                                         |                                                                   |
|-----------------------|-----------------------------------------|-------------------------------------------------------------------|
| **Field**             | **Type**                                | **Description**                                                   |
| @type                 | shml:Assertion                          | SHML assertion type                                               |
| shml:content          | fandaws:Concept \| fandaws:Relationship | The Fandaws knowledge claim being asserted                        |
| shml:assertedBy       | IRI                                     | Agent who made the original statement (user identifier)           |
| shml:assertedAt       | dateTime                                | When the statement was parsed and committed                       |
| shml:epistemicStatus  | enum                                    | committed, provisional, hypothetical                              |
| shml:provenanceChain  | GraphMutation\[\]                       | Chain of mutations that led to this concept’s current state       |
| shml:validationResult | IRI                                     | Reference to the ValidationResult that approved the last mutation |

**JSON-LD Contract: SHMLFramingResult**

Returned by SHML with framing and attribution metadata:

|                               |                    |                                                                                                   |
|-------------------------------|--------------------|---------------------------------------------------------------------------------------------------|
| **Field**                     | **Type**           | **Description**                                                                                   |
| @type                         | shml:FramingResult | SHML framing type                                                                                 |
| shml:assertionId              | IRI                | The assertion being framed                                                                        |
| shml:candidateInterpretations | Interpretation\[\] | Competing interpretations if the assertion is ambiguous                                           |
| shml:conflictsWith            | IRI\[\]            | Other assertions that conflict with this one                                                      |
| shml:evidenceChain            | Evidence\[\]       | Evidence supporting or undermining the assertion                                                  |
| shml:displayFraming           | string             | How this assertion should be presented (e.g., “User stated that...” vs. “It is the case that...”) |

**Adapter Interface: SHMLAdapter**

|                                    |                                     |                                                         |
|------------------------------------|-------------------------------------|---------------------------------------------------------|
| **Method**                         | **Returns**                         | **Description**                                         |
| wrapAssertion(concept, provenance) | SHMLAssertionWrapper                | Create an SHML assertion envelope for a Fandaws concept |
| submitAssertion(wrapper)           | SHMLFramingResult \| DeferredResult | Submit assertion to SHML for framing analysis           |
| queryConflicts(conceptId)          | Conflict\[\] \| DeferredResult      | Check for conflicting assertions across the SHML layer  |

**Offline Degradation**

When SHML is unavailable, Fandaws creates assertion wrappers locally using the provenance data already captured in GraphMutation history. These local wrappers carry epistemicStatus=“committed” and are queued for SHML framing analysis when connectivity is restored. Core knowledge building is unaffected—SHML adds epistemic depth but is not required for structural operations.

### 10.4.3 Ontological Constraint Engine (OCE)

**Purpose:** The OCE validates proposed world states and state transitions against BFO-grounded ontological commitments. It answers the question: given the world as modeled, which transitions are ontologically permitted? Fandaws knowledge graphs provide the taxonomic and property structures that the OCE uses as its constraint base. The OCE, in turn, can validate proposed Fandaws mutations for ontological coherence beyond what the Validator’s structural checks cover.

**Direction:** Bidirectional. Fandaws exports knowledge graphs as constraint definitions to the OCE. The OCE returns typed violation reports and repair paths that Fandaws can use to improve mutation quality.

**Integration Architecture**

The OCE sits between a synthetic agent’s world model and its action planning layer. It performs possibility-space validation: given a set of concepts, properties, and relationships, which state transitions are ontologically coherent? Fandaws provides the ontological backbone—the concept hierarchies and property inheritance chains that define what kinds of things exist and what they can do.

The key integration point is the OCE’s constraint import interface. When the OCE loads a Fandaws knowledge graph, it extracts ontological axioms: subclass hierarchies become subsumption constraints, properties become inherence constraints, and relationships become relational constraints. The OCE then uses these constraints to validate proposed states from its upstream consumers (action planners, counterfactual simulators).

**JSON-LD Contract: OCEConstraintExport**

Fandaws exports its knowledge graph in a form the OCE can consume as constraints:

|                            |                             |                                                               |
|----------------------------|-----------------------------|---------------------------------------------------------------|
| **Field**                  | **Type**                    | **Description**                                               |
| @type                      | fandaws:OCEConstraintExport | Contract type discriminator                                   |
| fandaws:graphId            | IRI                         | Source knowledge graph identifier                             |
| fandaws:subsumptionAxioms  | Axiom\[\]                   | Concept hierarchy as subsumption constraints (X subClassOf Y) |
| fandaws:inherenceAxioms    | Axiom\[\]                   | Property attachments as inherence constraints (X bearer_of Y) |
| fandaws:relationalAxioms   | Axiom\[\]                   | Custom relationships as relational constraints                |
| fandaws:disjointnessAxioms | Axiom\[\]                   | Inferred disjointness from hierarchy structure                |
| fandaws:graphVersion       | string                      | Version hash for cache invalidation                           |

**JSON-LD Contract: OCEValidationFeedback**

The OCE can return feedback on proposed Fandaws mutations:

|                 |                        |                                                                                                        |
|-----------------|------------------------|--------------------------------------------------------------------------------------------------------|
| **Field**       | **Type**               | **Description**                                                                                        |
| @type           | oce:ValidationFeedback | OCE feedback type                                                                                      |
| oce:mutationId  | IRI                    | The GraphMutation being evaluated                                                                      |
| oce:violations  | TypedViolation\[\]     | Ontological violations with category (InherenceError, SpatialInconsistency, TemporalIncoherence, etc.) |
| oce:repairPaths | RepairPath\[\]         | Suggested corrections ranked by cost                                                                   |
| oce:coherent    | boolean                | Whether the mutation is ontologically coherent                                                         |

**Adapter Interface: OCEAdapter**

|                                     |                                         |                                                                 |
|-------------------------------------|-----------------------------------------|-----------------------------------------------------------------|
| **Method**                          | **Returns**                             | **Description**                                                 |
| exportConstraints(graphId)          | OCEConstraintExport                     | Export current graph as OCE constraint set                      |
| validateMutation(mutation, graphId) | OCEValidationFeedback \| DeferredResult | Submit a proposed mutation for ontological coherence validation |
| isAvailable()                       | boolean                                 | Check if OCE is loaded and operational                          |

**Offline Degradation**

The OCE is designed for edge-canonical execution. When bundled with Fandaws, it operates locally. When not bundled, Fandaws relies exclusively on its built-in Validator for structural checks. OCE validation adds ontological depth (catching inherence errors, spatial inconsistencies, temporal incoherence) that the Validator's simpler checks do not cover, but is not required for core operation.

**Validator / OCE Governance**

The Validator (Section 3.2.4) and the OCE check different things. The Validator enforces structural integrity (no circular hierarchies, no duplicate properties, no dangling references). The OCE enforces ontological coherence (no inherence errors, no spatial inconsistencies, no temporal contradictions). They may produce contradictory outcomes: the Validator may accept a mutation that the OCE later rejects as ontologically incoherent.

The canonical governance flow is:

1. The Validator runs first as part of the core pipeline. If the Validator rejects, the mutation is rejected. The OCE is never consulted.
2. If the Validator accepts and the OCE is available, the OrchestrationAdapter may optionally submit the mutation to the OCE via validateMutation() before committing it to the StateAdapter.
3. If the OCE returns oce:coherent = false, the OrchestrationAdapter has two options depending on configuration: (a) **strict mode** — treat the OCE rejection as authoritative and reject the mutation, emitting the OCE's repairPaths to the caller; (b) **advisory mode** — commit the mutation but annotate it with the OCE's violation report as metadata (fandaws:oceAdvisory on the GraphMutation). The default is advisory mode, preserving the principle that OCE is a non-normative extension.
4. If the OCE is unavailable, the mutation is committed with no OCE annotation. The OCE can retroactively evaluate committed mutations when it becomes available, producing advisory reports that the OrchestrationAdapter surfaces to the caller.

This flow ensures that the Validator is always authoritative for structural integrity, the OCE adds depth without blocking core operation, and the governance boundary is explicit.

## 10.5 Tier 3 — Downstream Consumers

Tier 3 systems ingest Fandaws knowledge graphs as structured inputs for reasoning, governance, and verification. Fandaws does not depend on these systems; they depend on Fandaws. The integration contract is the JSON-LD KnowledgeGraph export.

### 10.5.1 Federated Network for Structured Reasoning (FNSR)

**Purpose:** FNSR is a distributed reasoning architecture whose services consume structured knowledge for deductive, abductive, analogical, and counterfactual reasoning. Fandaws knowledge graphs provide the concept hierarchies, property chains, and relationship structures that FNSR services reason over.

**Direction:** Fandaws → FNSR. Fandaws exports knowledge graphs; FNSR services consume them.

**FNSR Sub-Service Integration Points**

|                                         |                                                                      |                                                                                                                                                                                    |
|-----------------------------------------|----------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **FNSR Service**                        | **What It Consumes from Fandaws**                                    | **How It Uses It**                                                                                                                                                                 |
| MDRE (Multi-Domain Reasoning Engine)    | Full knowledge graph: concept hierarchies, properties, relationships | Deductive reasoning over structured domain knowledge. Uses Fandaws hierarchies as the taxonomic backbone for syllogistic inference.                                                |
| APS (Analogical Precedent Service)      | Concept hierarchy structure, property patterns                       | Embeds reasoning graphs (which reference Fandaws concepts) into vector space for structural similarity matching. Uses hierarchy depth and property overlap as similarity features. |
| CSS (Counterfactual Simulation Service) | Concept properties, relationship constraints                         | Simulates alternative states by modifying Fandaws-derived facts and propagating consequences through the knowledge graph structure.                                                |
| DES (Defeasible Expectation Service)    | Property inheritance chains, default values                          | Generates defeasible expectations from Fandaws property inheritance (e.g., “birds typically fly”). Expectations are defeated by more specific information.                         |
| AES (Abductive Elicitation Service)     | Knowledge graph gaps (missing properties, unclassified concepts)     | Identifies what Fandaws knowledge is missing when MDRE’s deduction fails. Generates hypotheses about missing predicates.                                                           |

**JSON-LD Contract: FNSRKnowledgeIngestion**

The standard contract for FNSR services consuming a Fandaws knowledge graph:

|                              |                                |                                                                                      |
|------------------------------|--------------------------------|--------------------------------------------------------------------------------------|
| **Field**                    | **Type**                       | **Description**                                                                      |
| @type                        | fandaws:FNSRKnowledgeIngestion | Contract type discriminator                                                          |
| fandaws:graphId              | IRI                            | Source knowledge graph identifier                                                    |
| fandaws:graph                | KnowledgeGraph                 | The full JSON-LD knowledge graph                                                     |
| fandaws:graphVersion         | string                         | Version hash for cache invalidation                                                  |
| fandaws:exportedAt           | dateTime                       | When the graph was exported                                                          |
| fandaws:bfoAlignmentCoverage | float \[0,1\]                  | Fraction of concepts with BFO alignment (helps FNSR assess ontological completeness) |
| fandaws:scope                | enum                           | full, delta (full graph or incremental changes since last export)                    |

**Offline Degradation**

FNSR services are downstream consumers. If FNSR is unavailable, Fandaws is unaffected. If Fandaws is unavailable, FNSR services operate on their last-ingested copy of the knowledge graph. The graphVersion field enables FNSR to detect staleness.

**Streaming Subscription Model**

The FNSRKnowledgeIngestion contract supports bulk export, but M2M interactions require near-real-time knowledge propagation. When FNSR services need to react to graph changes as they occur (e.g., AES discovers a missing concept, queries Fandaws, and Fandaws structures the answer), bulk export introduces unacceptable latency.

To address this, FNSR services may subscribe to specific concept subtrees via the GraphChangeEvent mechanism (Section 10.8.1). The subscription model is defined as follows:

**JSON-LD Contract: GraphChangeSubscription**

|                           |                                  |                                                              |
|---------------------------|----------------------------------|--------------------------------------------------------------|
| **Field**                 | **Type**                         | **Description**                                              |
| @type                     | fandaws:GraphChangeSubscription  | Contract type discriminator                                  |
| fandaws:subscriberId      | IRI                              | The FNSR service subscribing                                 |
| fandaws:graphId           | IRI                              | The knowledge graph being monitored                          |
| fandaws:subtreeRoots      | IRI\[\] \| null                  | Concept IRIs defining the subtrees of interest (null = entire graph) |
| fandaws:changeTypes       | enum\[\]                         | Which change types to receive: structural, attributive, relational |
| fandaws:deliveryMode      | enum                             | push (OrchestrationAdapter emits to subscriber), poll (subscriber queries at interval) |

When a GraphMutation affects a concept within a subscribed subtree, the OrchestrationAdapter emits a targeted GraphChangeEvent to the subscriber containing only the relevant delta (scope="delta" in the FNSRKnowledgeIngestion contract). This enables the AES loop described in the critique: AES detects a gap, queries Fandaws, Fandaws structures the answer via its pipeline, and the resulting GraphMutation is streamed back to FNSR as a delta event — without requiring a full graph re-export.

Subscription management is an OrchestrationAdapter concern. The core computation pipeline is unaware of subscriptions. The push delivery mode requires an OrchestrationAdapter that supports outbound notification (e.g., WebSocket, event emitter). The poll delivery mode works with any OrchestrationAdapter, including the SynchronousOrchestrationAdapter, since the subscriber controls the polling interval.

### 10.5.2 Integral Ethics Engine (IEE)

**Purpose:** The IEE evaluates actions and decisions from the perspective of twelve archetypal worldviews, accumulating moral friction and synthesizing ethical judgments. Fandaws knowledge graphs ground the IEE’s reasoning in structured domain knowledge: concept hierarchies define what kinds of entities are involved, properties define their characteristics, and relationships define how they are connected.

**Direction:** Bidirectional. Fandaws exports knowledge contexts to the IEE. The IEE writes back ethical contestation flags to Fandaws when concept definitions produce ethically problematic outcomes.

**What the IEE Consumes**

- Concept hierarchies for ethical category analysis (e.g., distinguishing persons from objects, living from non-living)

- Property inheritance chains for value propagation reasoning (e.g., if “living things” have “intrinsic value,” then specific organisms inherit that property)

- Custom relationship structures for stakeholder and consequence mapping (e.g., “employer employs worker” establishes a relationship with ethical implications)

**JSON-LD Contract: IEEKnowledgeContext**

The IEE requests a focused knowledge context for a specific ethical evaluation:

|                              |                             |                                                              |
|------------------------------|-----------------------------|--------------------------------------------------------------|
| **Field**                    | **Type**                    | **Description**                                              |
| @type                        | fandaws:IEEKnowledgeContext | Contract type discriminator                                  |
| fandaws:focusConcepts        | IRI\[\]                     | Concepts central to the ethical question                     |
| fandaws:ancestorDepth        | integer                     | How far up the hierarchy to include (for category reasoning) |
| fandaws:descendantDepth      | integer                     | How far down to include (for consequence propagation)        |
| fandaws:includeRelationships | boolean                     | Whether to include custom relationships in the context       |
| fandaws:includeProperties    | boolean                     | Whether to include properties (for value propagation)        |

**IEE Write-Back: Ethical Contestation**

If the IEE determines that a concept definition or relationship structure leads to ethically problematic outcomes — for example, a definition of "person" that excludes a subgroup, or a property inheritance chain that propagates discriminatory classifications — it may flag the responsible concept in Fandaws as ethically contested.

**JSON-LD Contract: EthicalContestationFlag**

|                              |                                    |                                                              |
|------------------------------|------------------------------------|--------------------------------------------------------------|
| **Field**                    | **Type**                           | **Description**                                              |
| @type                        | fandaws:EthicalContestationFlag    | Contract type discriminator                                  |
| fandaws:conceptId            | IRI                                | The concept being contested                                  |
| fandaws:contestationType     | enum                               | exclusion, discrimination, harmPropagation, categoryError    |
| fandaws:worldviewSource      | string\[\]                         | Which of the twelve archetypal worldviews raised the concern |
| fandaws:frictionScore        | float \[0,1\]                      | Moral friction magnitude from the IEE evaluation             |
| fandaws:explanation          | string                             | Human-readable explanation of the ethical concern             |
| fandaws:suggestedRevision    | GraphMutation \| null              | Optional suggested mutation to resolve the contestation      |
| fandaws:severity             | enum                               | advisory, warning, blocking                                  |

When Fandaws receives an EthicalContestationFlag, it stores the flag as metadata on the contested concept — the flag annotates rather than modifies the concept's ontological content. Downstream consumers of the knowledge graph can see which concepts carry unresolved ethical contestations.

At "advisory" severity, mutations proceed normally; the flag is visible in the GraphMutation provenance chain. At "warning" severity, mutations proceed but the OrchestrationAdapter emits a notification to the caller. At "blocking" severity, the OrchestrationAdapter prevents further mutations to the contested concept until the contestation is resolved.

**Contestation Governance:** Because a "blocking" EthicalContestationFlag effectively halts knowledge building for a concept, the governance model must prevent denial-of-service (a misconfigured or adversarial IEE blocking all edits) while preserving the ethical safeguard:

- **Adjudication authority:** Only callers with the "ethicsAdmin" role (Section 11.2) may resolve blocking contestations. Resolution options are: accept (revise the concept per suggestedRevision), dismiss (remove the flag with a documented reason), or downgrade (change severity to "warning" or "advisory").
- **Automatic expiry:** Blocking flags that remain unresolved for longer than the configured contestationExpiryDuration (Section 11.1, default: PT72H) are automatically downgraded to "warning" severity to prevent indefinite concept lockout. The expiry event is logged with full provenance.
- **Appeal mechanism:** The caller whose mutation was blocked may submit a contestationAppeal containing a counter-argument and an alternative GraphMutation. The appeal is queued for ethicsAdmin review and does not bypass the block.
- **Rate limiting:** A single IEE instance may not issue more than the configured contestationRateLimit (Section 11.1, default: 10) blocking flags per graph per hour. Excess flags are automatically downgraded to "warning" severity.
- **M2M deadlock prevention:** In M2M mode, a "blocking" flag must not cause the calling agent to hang indefinitely. When a mutation is blocked by an EthicalContestationFlag and the caller is an M2M agent (identified by the OrchestrationAdapter), the OrchestrationAdapter treats the block as a Semantic Deadlock (Section 6.7) and emits an EpistemicFailure event. The EpistemicFailure includes the full EthicalContestationFlag, the blocked GraphMutation, and suggestedActions listing: (1) the IEE's suggestedRevision as an alternative mutation, (2) an appeal path, and (3) a recommendation to try a different reasoning path that avoids the contested concept. This ensures the agent's pipeline continues rather than stalling on an ethical review that requires human adjudication.

This write-back mechanism transforms the IEE integration from one-way consumption to a bidirectional feedback loop: Fandaws informs the IEE's reasoning, and the IEE informs Fandaws' knowledge quality. The governance rules ensure the feedback loop cannot become a denial-of-service vector.

**Offline Degradation**

The IEE operates on exported knowledge graphs and does not require real-time Fandaws connectivity for its evaluation work. Ethical contestation flags may be queued as DeferredResult if the IEE's write-back channel is unavailable. Stale knowledge graphs are acceptable for ethical reasoning but should be flagged so the IEE can note that its domain knowledge may not reflect the latest state.

### 10.5.3 HIRI Protocol

**Purpose:** HIRI is a local-first verifiable knowledge protocol that enables agents to make knowledge claims with cryptographic provenance. Fandaws knowledge graphs can serve as verifiable knowledge claims within HIRI’s framework. Each GraphMutation in Fandaws carries provenance metadata—who stated the fact, when, and through what workflow—making Fandaws-generated knowledge compatible with HIRI’s epistemic transparency requirements.

**Direction:** Fandaws → HIRI.

**Integration Architecture**

HIRI uses a sovereign log (Hypercore) for append-only agent records and IPFS for content-addressed public knowledge. Fandaws knowledge graphs can be published to HIRI in two ways: as complete graph snapshots (content-addressed on IPFS) referenced from an agent’s manifest, or as individual GraphMutation events appended to a sovereign log.

The critical compatibility point is provenance. HIRI requires that every knowledge claim be traceable to an assertion event performed by an identifiable agent. Fandaws’ GraphMutation model already captures this: every mutation records the user who initiated it, the timestamp, the workflow that produced it, and the validation result that approved it.

**JSON-LD Contract: HIRIManifestEntry**

A Fandaws knowledge graph published as a HIRI manifest entry:

|                    |                    |                                                          |
|--------------------|--------------------|----------------------------------------------------------|
| **Field**          | **Type**           | **Description**                                          |
| @type              | hiri:ManifestEntry | HIRI manifest type                                       |
| hiri:contentCID    | string             | IPFS Content Identifier for the published graph snapshot |
| hiri:contentType   | string             | fandaws/knowledge-graph                                  |
| hiri:assertedBy    | IRI                | Agent identifier (Fandaws user or instance)              |
| hiri:assertedAt    | dateTime           | Publication timestamp                                    |
| hiri:graphId       | IRI                | Fandaws knowledge graph identifier                       |
| hiri:graphVersion  | string             | Version hash                                             |
| hiri:mutationCount | integer            | Total mutations applied (provenance depth indicator)     |
| hiri:taintLevel    | string             | Epistemic taint level (L0–L5, per FNSR taint model)      |

**Offline Degradation**

HIRI publication is a write-only downstream operation. If HIRI is unavailable, Fandaws queues graph snapshots for later publication. If Fandaws is offline, HIRI consumers use the last published snapshot (identified by CID, which is immutable). The content-addressed nature of IPFS means that any cached copy is guaranteed to be identical to the original.

**Optimistic Batching**

In M2M contexts, agents may execute dozens of mutations per second during a knowledge-building dialogue. Writing every individual GraphMutation to HIRI/IPFS at mutation speed creates an I/O bottleneck that would throttle the pipeline.

Fandaws addresses this through optimistic batching in the StateAdapter. During an active dialogue session, mutations are applied to the in-memory knowledge graph immediately (optimistic) but are only committed to HIRI/IPFS in batches. The batch commit is triggered by one of:

1. **Session close:** When the dialogue session ends, all uncommitted mutations are flushed to HIRI as a single graph snapshot.
2. **Stabilization timeout:** If no new mutations are received for the configured commitBatchInterval (Section 11.1, default: PT5S), the current batch is committed.
3. **Batch size threshold:** If the uncommitted mutation count exceeds the configured commitBatchSize (Section 11.1, default: 50), the batch is committed immediately.
4. **Explicit flush:** The OrchestrationAdapter or an upstream agent may request an explicit commit at any time.

Between batch commits, the in-memory graph is the authoritative state. If the process crashes before a batch commit, uncommitted mutations are lost — this is an acceptable tradeoff because the last committed HIRI snapshot provides a consistent rollback point, and the dialogue can be replayed from that point. The StateAdapter must track which mutations have been committed and which are pending.

### 10.5.4 ARCHON

**Purpose:** ARCHON is a framework for superintelligent guardianship grounded in moral ontology. It operates as a guardian (not sovereign) that preserves structural conditions for human agency. Fandaws knowledge graphs provide the ontological backbone that ARCHON uses for domain-specific reasoning about what kinds of entities exist, what their properties are, and how they relate to one another.

**Direction:** Fandaws → ARCHON.

**Integration Architecture**

ARCHON’s architecture includes a world model layer (BFO-grounded state representation), an Ontological Constraint Engine (possibility validation), a normative reasoning layer (integral ethics), and an action planning layer. Fandaws feeds the world model layer by providing structured domain ontologies that define the conceptual vocabulary ARCHON reasons with.

ARCHON’s moral personhood model—where the system bears irreversible costs for its decisions—depends on coherent ontological categories. If ARCHON is to reason about whether an action destroys “human cognitive agency,” it needs a concept hierarchy that distinguishes agents from non-agents, cognitive capacities from physical ones, and temporary impairments from permanent destruction. Fandaws provides this structure.

**JSON-LD Contract**

ARCHON consumes the standard FNSRKnowledgeIngestion contract (Section 10.5.1). No ARCHON-specific contract is required because ARCHON’s world model layer accepts any BFO-aligned ontology. ARCHON-specific reasoning happens in its own normative and constraint layers, not in the knowledge ingestion interface.

**Offline Degradation**

ARCHON is a downstream consumer operating on pre-ingested ontologies. Real-time Fandaws connectivity is not required. Ontological updates are ingested through scheduled graph refreshes, not real-time streaming.

### 10.5.5 Assay

**Purpose:** Assay is a deterministic control plane for enterprise AI workflows. It separates generation from validation, automation from authority, and intelligence from responsibility. Fandaws knowledge graphs can serve as the domain knowledge layer that Assay uses to validate AI outputs against structured ontological constraints.

**Direction:** Fandaws → Assay.

**Integration Architecture**

Assay’s architecture includes input shape validation, AI generation, external validation rules, human gates, and immutable execution traces. Fandaws integrates at the validation rules layer: when an AI generates output in a domain covered by a Fandaws knowledge graph, Assay can validate that the output uses terminology consistently with the ontology, references valid concepts, and respects hierarchical relationships.

For example, in a healthcare Assay workflow, a Fandaws medical ontology could validate that an AI-generated clinical summary uses diagnosis terms that exist in the ontology and correctly classifies conditions under their parent categories.

**JSON-LD Contract: AssayValidationRuleSet**

Fandaws exports a validation rule set that Assay can apply to AI outputs:

|                          |                                |                                                           |
|--------------------------|--------------------------------|-----------------------------------------------------------|
| **Field**                | **Type**                       | **Description**                                           |
| @type                    | fandaws:AssayValidationRuleSet | Contract type discriminator                               |
| fandaws:graphId          | IRI                            | Source knowledge graph                                    |
| fandaws:terminologyRules | Rule\[\]                       | Valid terms and their canonical forms                     |
| fandaws:hierarchyRules   | Rule\[\]                       | Valid classification relationships                        |
| fandaws:propertyRules    | Rule\[\]                       | Required and forbidden property combinations              |
| fandaws:guaranteeLevel   | enum                           | full, modified, custom (maps to Assay’s guarantee system) |

**Offline Degradation**

Assay is a downstream consumer. It operates on pre-loaded validation rule sets. If Fandaws is unavailable at rule-set refresh time, Assay continues using the last loaded rules and logs the staleness.

## 10.6 Tier 4 — Domain Applications

Tier 4 systems are specific operational applications that use Fandaws ontologies for domain-specific purposes. They are leaf nodes in the ecosystem—they consume Fandaws knowledge but do not feed back into it. Integration contracts are lightweight.

### 10.6.1 Aligned Property Commons (APC)

**Purpose:** APC is a non-extractive property management model that uses automated systems for maintenance triage, tenant communication, vendor dispatch, and compliance tracking. Fandaws knowledge graphs provide the domain ontology for property management: concept hierarchies for property types, maintenance categories, and regulatory requirements; property inheritance for building specifications; and relationships for stakeholder mapping.

**Direction:** Fandaws → APC.

**Integration Points**

- Maintenance ontology: Fandaws concept hierarchy classifying maintenance requests (plumbing \> leak \> burst pipe) for automated triage scoring.

- Property taxonomy: Building types, unit configurations, amenity classifications for portfolio analysis.

- Regulatory ontology: Jurisdiction-specific compliance requirements organized by property type and location.

- Stakeholder relationships: Tenant-unit, unit-building, building-portfolio relationships for governance and reporting.

**JSON-LD Contract**

APC consumes standard KnowledgeGraph exports filtered to property-management-relevant concept subtrees. No APC-specific contract is required.

**Offline Degradation**

APC pre-loads domain ontologies at deployment. Runtime Fandaws connectivity is not required. Ontology updates are applied through scheduled refreshes.

### 10.6.2 Code-to-CAD

**Purpose:** Code-to-CAD translates programmatic descriptions into manufacturing-ready CAD models. Fandaws knowledge graphs provide the ontological layer for manufacturing object taxonomies: material hierarchies, component relationships, dimensional property inheritance, and manufacturing process classifications.

**Direction:** Fandaws → Code-to-CAD.

**Integration Points**

- Material ontology: Hierarchical classification of materials with inherited properties (density, tensile strength, thermal conductivity).

- Component taxonomy: Part types, assembly relationships, and compatibility constraints.

- Process ontology: Manufacturing processes (milling, printing, casting) with applicability constraints per material type.

**JSON-LD Contract**

Code-to-CAD consumes standard KnowledgeGraph exports filtered to manufacturing-relevant concept subtrees. The key requirement is that property inheritance is preserved in the export so that Code-to-CAD can derive material properties for specific components from their parent categories.

### 10.6.3 Eulogy Pen

**Purpose:** Eulogy Pen is an AI generative platform for commemorative writing. Fandaws knowledge graphs can provide structured narrative ontologies: person-event-relationship structures, temporal sequencing, and thematic classification that guide generative AI in producing coherent, factually grounded commemorative texts.

**Direction:** Fandaws → Eulogy Pen.

**Integration Points**

- Person ontology: Biographical concept hierarchies (roles, relationships, achievements, values).

- Event taxonomy: Life event classifications with temporal ordering constraints.

- Thematic ontology: Themes and motifs classified by tradition, tone, and audience.

**JSON-LD Contract**

Eulogy Pen consumes standard KnowledgeGraph exports focused on biographical and narrative concept subtrees. The knowledge graph provides structural scaffolding; the generative AI provides natural language realization.

## 10.7 Tier 5 — Optional Infrastructure

Tier 5 provides optional distribution, storage, and verification infrastructure for Fandaws artifacts. These systems are never required for core operation. They enhance availability, immutability, and decentralized access.

### 10.7.1 IPFS (InterPlanetary File System)

**Purpose:** IPFS provides content-addressed, decentralized storage for Fandaws knowledge graphs. Every graph snapshot is identified by its Content Identifier (CID)—a cryptographic hash of the content. This guarantees immutability (any change produces a different CID), deduplication (identical graphs share the same CID), and location independence (the graph can be fetched from any node that has it).

**Direction:** Fandaws → IPFS (publication) and IPFS → Fandaws (retrieval).

**Integration Architecture**

IPFS integration serves three purposes in the Fandaws ecosystem:

- **Immutable snapshots:** Every knowledge graph version can be published to IPFS, creating a permanent, tamper-evident record. This supports HIRI’s verifiable knowledge claims (Section 10.5.3)—the CID in a HIRI manifest entry guarantees that any consumer fetches exactly the graph the publisher intended.

- **Decentralized distribution:** Knowledge graphs published to IPFS are available from any node that has pinned them, eliminating single-point-of-failure risks. A Fandaws deployment in one location can publish a graph; a deployment in another location can consume it by CID without knowing the publisher’s address.

- **Shared T-Box:** Common ontological definitions (BFO alignments, standard vocabularies, shared concept hierarchies) can be published once to IPFS and referenced by CID from multiple Fandaws instances. This eliminates redundant storage and ensures all instances use identical definitions.

**JSON-LD Contract: IPFSPublicationResult**

|                     |                               |                                                   |
|---------------------|-------------------------------|---------------------------------------------------|
| **Field**           | **Type**                      | **Description**                                   |
| @type               | fandaws:IPFSPublicationResult | Contract type discriminator                       |
| fandaws:graphId     | IRI                           | Source knowledge graph identifier                 |
| fandaws:cid         | string                        | CIDv1 content identifier (e.g., bafybeig...)      |
| fandaws:publishedAt | dateTime                      | Publication timestamp                             |
| fandaws:sizeBytes   | integer                       | Size of the published JSON-LD document            |
| fandaws:pinned      | boolean                       | Whether the CID has been pinned for persistence   |
| fandaws:gatewayUrl  | string \| null                | HTTP gateway URL for browser-accessible retrieval |

**Adapter Interface: IPFSAdapter**

|                       |                                         |                                                                    |
|-----------------------|-----------------------------------------|--------------------------------------------------------------------|
| **Method**            | **Returns**                             | **Description**                                                    |
| publishGraph(graphId) | IPFSPublicationResult \| DeferredResult | Serialize current graph as JSON-LD and publish to IPFS             |
| fetchGraph(cid)       | KnowledgeGraph \| DeferredResult        | Retrieve a knowledge graph by CID                                  |
| pinGraph(cid)         | boolean                                 | Request persistent pinning for a CID                               |
| resolveIPNS(name)     | string \| DeferredResult                | Resolve an IPNS name to the latest CID for a mutable graph pointer |

**Offline Degradation**

IPFS is entirely optional infrastructure. When unavailable: publishing is queued as DeferredResult; retrieval falls back to locally cached copies (if the CID has been previously fetched); all core operations continue without interruption. Locally stored knowledge graphs are the canonical source; IPFS copies are distribution artifacts.

## 10.8 Cross-Cutting Concerns

### 10.8.1 Event Notification Model

When a Fandaws knowledge graph changes, downstream consumers may need to be notified. The core specification does not include an event bus or publish-subscribe system (these are infrastructure). Instead, Fandaws defines a GraphChangeEvent JSON-LD type that any OrchestrationAdapter can emit through whatever notification channel is available.

**JSON-LD Contract: GraphChangeEvent**

|                          |                          |                                                                                                      |
|--------------------------|--------------------------|------------------------------------------------------------------------------------------------------|
| **Field**                | **Type**                 | **Description**                                                                                      |
| @type                    | fandaws:GraphChangeEvent | Event type discriminator                                                                             |
| fandaws:graphId          | IRI                      | Affected knowledge graph                                                                             |
| fandaws:graphVersion     | string                   | New version hash after the change                                                                    |
| fandaws:mutationSummary  | object                   | Counts of additions, modifications, deletions, merges                                                |
| fandaws:affectedConcepts | IRI\[\]                  | Concepts that were directly modified                                                                 |
| fandaws:timestamp        | dateTime                 | When the change occurred                                                                             |
| fandaws:scope            | enum                     | structural (hierarchy changed), attributive (properties changed), relational (relationships changed) |

Non-normative notification channels include: file system watchers (for FileSystemStateAdapter), WebSocket broadcasts (for browser-based deployments), HTTP webhooks (for server deployments), and IPFS re-publication (for decentralized distribution). The choice of notification channel is an OrchestrationAdapter concern, not a core specification concern.

### 10.8.2 Versioning and Cache Invalidation

Every KnowledgeGraph maintains a version hash (a content-based hash of the graph’s JSON-LD serialization). This hash serves as the universal cache invalidation key across all tiers. When a downstream consumer holds a cached copy of a Fandaws graph, it compares its cached version hash against the current version hash. If they differ, the cache is stale and should be refreshed.

The version hash is deterministic: given identical graph content, the hash is identical regardless of when or where it was computed. This aligns with the determinism constraint (Section 2.3) and with IPFS’s content-addressing model (Section 10.7.1).

### 10.8.3 Integration Testing Strategy

Each integration tier can be tested independently:

- **Tier 1:** Test with mock IntegrationAdapter implementations that return predefined BFO alignments, dictionary results, and ontology imports.

- **Tier 2:** Test with local instances of TagTeam.js, SHML, and OCE running in the same Node.js process or browser tab.

- **Tier 3:** Test by exporting a KnowledgeGraph and verifying it conforms to the FNSRKnowledgeIngestion, IEEKnowledgeContext, and HIRIManifestEntry contracts.

- **Tier 4:** Test by exporting domain-specific subtrees and verifying they contain the expected concept hierarchies and properties.

- **Tier 5:** Test with a local IPFS node or mock IPFS gateway. Verify CID computation is deterministic.

All integration tests must pass with the NullIntegrationAdapter (offline mode), verifying that no integration is required for core operation.

### 10.8.4 M2M Performance Considerations

In machine-to-machine deployments, the bottleneck shifts from human typing speed to the GraphMutation/Validation cycle time. The following performance targets apply to the core computation pipeline when operating in M2M mode:

|                              |                    |                                                              |
|------------------------------|--------------------|--------------------------------------------------------------|
| **Operation**                | **Target Latency** | **Notes**                                                    |
| NLParser (single utterance)  | < 5ms              | Pure string parsing with regex/grammar, no I/O               |
| Classifier (verb routing)    | < 1ms              | Enum matching                                                |
| KnowledgeEngine (mutation)   | < 10ms             | Graph traversal for hierarchy, scope narrowing               |
| Validator (full check suite) | < 15ms             | Termidium (8-level search), property redundancy, sanity check |
| StateAdapter (apply mutation)| < 5ms              | In-memory graph update                                       |
| DescriptionEngine            | < 2ms              | Template application                                         |
| **Full pipeline (no prompt)**| < 40ms             | End-to-end for assertions that require no disambiguation     |
| **Full pipeline (with prompt)** | < 40ms + round-trip | Pipeline pauses at ConversationPrompt; agent response adds network or in-process latency |

These are interactive design targets under typical workloads (knowledge graphs under 10,000 concepts). Larger graphs may require indexing optimizations in the StateAdapter (e.g., concept label indexes for Termidium search, property lookup indexes for redundancy checks).

The Validator is the critical path component because it performs the most graph traversal per invocation. Implementations should consider precomputing ancestor/descendant caches that are invalidated on structural mutations, reducing Termidium's 8-level search from a recursive traversal to a cache lookup for the common case.

## 10.9 Ecosystem Map

The following table provides a complete reference of all ecosystem integrations:

|                 |          |               |                    |                                     |                                           |
|-----------------|----------|---------------|--------------------|-------------------------------------|-------------------------------------------|
| **System**      | **Tier** | **Direction** | **Adapter**        | **Contract**                        | **Offline Behavior**                      |
| BFO             | 1        | Upstream      | IntegrationAdapter | BFOAlignmentRequest/Result          | Heuristic fallback, provisional alignment |
| Dictionaries    | 1        | Upstream      | IntegrationAdapter | DictionaryLookupResult              | Cached/stale/deferred                     |
| Ontology Import | 1        | Upstream      | IntegrationAdapter | OntologyImportResult                | Local files only                          |
| TagTeam.js      | 2        | Bidirectional | TagTeamAdapter     | ParseRequest/Result                 | Fallback to built-in NLParser             |
| SHML            | 2        | Bidirectional | SHMLAdapter        | AssertionWrapper/FramingResult      | Local wrappers, deferred framing          |
| OCE             | 2        | Bidirectional | OCEAdapter         | ConstraintExport/ValidationFeedback | Built-in Validator only                   |
| FNSR            | 3        | Downstream    | —                  | FNSRKnowledgeIngestion              | Consumers use last-ingested graph         |
| IEE             | 3        | Bidirectional | —                  | IEEKnowledgeContext / EthicalContestationFlag | Export context; receive ethical flags      |
| HIRI            | 3        | Downstream    | —                  | HIRIManifestEntry                   | Publication queued                        |
| ARCHON          | 3        | Downstream    | —                  | FNSRKnowledgeIngestion              | Scheduled refresh                         |
| Assay           | 3        | Downstream    | —                  | AssayValidationRuleSet              | Last-loaded rules                         |
| APC             | 4        | Downstream    | —                  | KnowledgeGraph export               | Pre-loaded ontology                       |
| Code-to-CAD     | 4        | Downstream    | —                  | KnowledgeGraph export               | Pre-loaded ontology                       |
| Eulogy Pen      | 4        | Downstream    | —                  | KnowledgeGraph export               | Pre-loaded ontology                       |
| IPFS            | 5        | Both          | IPFSAdapter        | IPFSPublicationResult               | Publish queued, fetch from cache          |


# 11. Configuration

All configuration is expressed as JSON-LD. There are no environment variables, command-line flags, or external configuration services in the core specification. Configuration is loaded as a JSON-LD document at initialization and treated as immutable for the duration of a session.

## 11.1 Configuration Parameters

|                                      |            |                             |                                                                           |
|--------------------------------------|------------|-----------------------------|---------------------------------------------------------------------------|
| **Parameter**                        | **Type**   | **Default**                 | **Description**                                                           |
| fandaws:cacheStalenessThreshold      | duration   | PT24H                       | Duration before cached integration results are considered stale           |
| fandaws:deduplicationDepth           | integer    | 8                           | Maximum hierarchy levels to search during Termidium deduplication         |
| fandaws:repetitionLimit              | integer    | 5                           | Maximum consecutive rejected mutations per (concept, mutationType) pair before semantic deadlock is declared (Section 6.7). Applied at runtime, not only in tests. |
| fandaws:descriptionTemplate.standard | string     | \[Term\] is a \[parent\]... | Template for standard concept descriptions                                |
| fandaws:descriptionTemplate.process  | string     | \[Object\] \[term\] is...   | Template for process concept descriptions                                 |
| fandaws:bfoAlignmentMode             | enum       | auto                        | BFO alignment mode: auto (heuristic + integration), manual, disabled      |
| fandaws:offlineMode                  | enum       | adaptive                    | Offline handling: adaptive (auto-detect), forced-offline, online-required |
| fandaws:exportFormats                | string\[\] | \[skos, owl, rdf, turtle\]  | Enabled export formats                                                    |
| fandaws:callerMode                   | enum       | human                       | Caller type: human (text prompts), agent (machineSignal on ConversationPrompts). Controls M2M Conversation Protocol (Section 5.9). |
| fandaws:commitBatchInterval          | duration   | PT5S                        | Stabilization timeout for HIRI/IPFS optimistic batching (Section 10.5.3). After this duration with no new mutations, the pending batch is committed. |
| fandaws:commitBatchSize              | integer    | 50                          | Maximum uncommitted mutations before a forced batch commit to HIRI/IPFS.  |
| fandaws:mergeReviewThreshold         | integer    | 10                          | If a Termidium merge would affect more than this many child concepts, require caller confirmation before applying (Section 6.2.2). |
| fandaws:locale                       | string     | en                          | BCP 47 language tag for Identity Simplification (Section 6.6). Controls article removal, case folding, and abbreviation expansion. |
| fandaws:abbreviationTable            | object     | {}                          | Domain-specific abbreviation expansions for Identity Simplification.      |
| fandaws:agentRateLimit               | integer    | 100                         | Maximum pipeline invocations per agent per minute in M2M mode. Excess invocations are rejected with a RateLimitExceeded error. |
| fandaws:oceMode                      | enum       | advisory                    | OCE governance mode: advisory (annotate but commit), strict (OCE rejection blocks commit). See Section 10.4.3. |
| fandaws:contestationExpiryDuration   | duration   | PT72H                       | Duration before unresolved "blocking" EthicalContestationFlags are automatically downgraded to "warning" (Section 10.5.2). |
| fandaws:contestationRateLimit        | integer    | 10                          | Maximum "blocking" EthicalContestationFlags per graph per hour from a single IEE instance. |
| fandaws:sessionExpiryDuration        | duration   | P7D                         | Duration before paused sessions auto-expire (Section 5.12.2).                              |
| fandaws:maxNestingDepth              | integer    | 10                          | Maximum nested negotiation depth before the pipeline suggests using an existing concept.   |
| fandaws:maxConcurrentSessions        | integer    | 5                           | Maximum active sessions per caller (Section 5.12.5).                                       |
| fandaws:scopeResolutionEnabled       | boolean    | false                       | Whether ScopeResolver is active. When false, the pipeline operates in single-graph mode.   |
| fandaws:staleCopyAction              | enum       | prompt                      | What to do when a resolved concept's source has been updated: prompt (ask caller), auto-update, ignore, fork. See Section 5.10.3. |
| fandaws:autoPromotionThreshold       | integer    | 3                           | Minimum distinct user graphs that must resolve a concept before auto-promotion to "community" tier (Section 5.13.3). |
| fandaws:autoPromotionCooldown        | duration   | P7D                         | Minimum time a concept must be published before auto-promotion eligibility (Section 5.13.3). |

## 11.2 Authorization and Provenance

Fandaws is edge-canonical and single-user by default. A browser tab or Node.js process is operated by a single caller who has full read/write access to the knowledge graph. In this default mode, no authentication or authorization infrastructure is required, consistent with the Spec Test.

For multi-agent M2M deployments where multiple callers interact with the same Fandaws instance, the OrchestrationAdapter must implement an authorization model. The core specification defines the authorization contract; implementations are adapter-specific.

**Caller Identity:** Every input received by receiveInput() must carry a callerId (an opaque string or IRI identifying the caller). In single-user mode, this defaults to "local." In M2M mode, the OrchestrationAdapter is responsible for authenticating the callerId via whatever mechanism is appropriate for the deployment (API keys, OAuth tokens, DID-based authentication, or simple shared secrets).

**Roles:** The authorization model defines four roles:

- **writer** — May assert facts, which flow through the normal computation pipeline. This is the default role.
- **reader** — May query the graph and receive exports but may not submit mutations.
- **curator** — May review and approve term promotions to the global federation (Section 5.13.2). May also manage the ScopeConfiguration for a federation, adding or removing global scope entries and setting priority/trustLevel. Curators inherit all writer permissions.
- **ethicsAdmin** — May resolve "blocking" EthicalContestationFlags (Section 10.5.2). This role is required only when IEE write-back is enabled.

Role assignment is a configuration concern managed by the OrchestrationAdapter. The core computation pipeline is role-unaware — it processes mutations identically regardless of the caller's role. The OrchestrationAdapter enforces role checks before passing input to the pipeline.

**Provenance Signing:** For deployments that publish to HIRI (Section 10.5.3), each GraphMutation should carry a cryptographic signature from the callerId. The signature scheme (e.g., Ed25519 via DID keys, HMAC via shared secret) is specified by the HIRI adapter, not by the core specification. The fandaws:provenance envelope on IntegrationAdapter results (Section 3.3.2) and the GraphMutation's existing provenance fields (who, when, workflow) provide the unsigned provenance chain. Signing adds tamper-resistance for multi-agent environments.

**Scope:** Authorization, authentication, and signing are OrchestrationAdapter and IntegrationAdapter concerns. They do not enter the core computation pipeline. This preserves the Spec Test: a single-user browser deployment requires no authentication infrastructure.

# 12. Reference Implementations

This section defines the reference adapter implementations that ship with the core specification. These implementations satisfy the Spec Test: they enable a developer to run Fandaws with only a browser, a local Node.js runtime, and JSON-LD files.

## 12.1 InMemoryStateAdapter

The InMemoryStateAdapter stores all knowledge graphs and session state in JavaScript objects. Graphs are held as parsed JSON-LD. This adapter is suitable for browser-based usage and short-lived sessions.

**Persistence:** None. State is lost when the process ends.

**Performance:** O(1) for load/save operations. Graph queries are O(n) where n is the number of concepts.

**Indexing:** To meet the performance targets in Section 10.8.4 (full pipeline < 40ms, Termidium < 15ms), the InMemoryStateAdapter must maintain reverse-lookup indices that are updated on every applyMutation call. At minimum:

- **canonicalLabel → concept IRI:** Hash map enabling O(1) lookup by normalized name. Required by Identity Simplification (Section 6.6) and ScopeResolver term matching.
- **concept IRI → parent IRI:** Hash map enabling O(1) parent lookup. Required by Property Redundancy Prevention (Section 6.3) and Scope Narrowing (Section 5.3.2).
- **concept IRI → child IRIs:** Reverse map enabling O(1) descendant enumeration. Required by Termidium's 8-level hierarchy search (Section 6.2) and CVS-005/CVS-007 push-to-ancestor checks.
- **concept IRI → property IRIs:** Hash map enabling O(1) property enumeration. Required by Property Redundancy Prevention.

Without these indices, graph operations degrade to O(n) full scans on every assertion, which is unacceptable for graphs exceeding ~1,000 concepts. The indices are implementation details of the adapter and do not affect the JSON-LD canonical representation — they are rebuilt from the graph on load.

**Offline behavior:** Fully functional. No external dependencies.

## 12.2 FileSystemStateAdapter

The FileSystemStateAdapter stores knowledge graphs and session state as JSON-LD files on the local file system. This adapter is suitable for Node.js usage and persistent sessions.

**Persistence:** Full. Graphs survive process restarts.

**File structure:** Each graph is a single .jsonld file. Session state is a separate .jsonld file per session.

**Offline behavior:** Fully functional. No external dependencies.

## 12.3 NullIntegrationAdapter

The NullIntegrationAdapter returns DeferredResult for every integration method. It is used for offline operation and for testing.

## 12.4 SynchronousOrchestrationAdapter

The SynchronousOrchestrationAdapter implements a simple read-eval-print loop for conversational interaction. In Node.js, it reads from stdin and writes to stdout. In the browser, it can be connected to a text input and output display. All computation is synchronous and blocking.

# 13. Glossary

| Term | Definition |
| --- | --- |
| Adapter | A pluggable implementation of a State, Integration, or Orchestration interface that separates infrastructure from core computation. |
| APC | Aligned Property Commons. A non-extractive property management model that uses Fandaws ontologies for domain modeling. |
| ARCHON | A framework for superintelligent guardianship grounded in moral ontology, operating as guardian rather than sovereign. |
| Algorithmic Curation | Automatic promotion of concepts to the "community" trust tier when they meet adoption, ethical safety, and structural quality thresholds, without requiring human curator review (Section 5.13.3). |
| Assay | A deterministic control plane for enterprise AI workflows that separates generation from validation. |
| BFO | Basic Formal Ontology. An upper-level ontology providing a philosophical framework for categorizing entities. |
| Canonical Label | The normalized form of a concept name used for matching and deduplication (fandaws:canonicalLabel). Produced by Identity Simplification with locale-aware case folding, NFKC normalization, and article removal. |
| CCO | Common Core Ontologies. Mid-level ontologies extending BFO with commonly used domain-independent concepts. |
| CID | Content Identifier. A cryptographic hash used by IPFS to address content immutably. |
| Computation Module | A pure function or stateless class that performs deterministic transformation of JSON-LD input to JSON-LD output. |
| Conflict Report | A JSON-LD document emitted by the ScopeResolver when the same term has incompatible IS_A chains in different scope graphs. Contains each conflicting definition, its source scope, and resolution options. |
| Context Scope | A temporary, session-bound knowledge graph shared by participants in a specific conversation or decision. The highest-priority scope in the resolution hierarchy. |
| ConversationSession | A JSON-LD document tracking the state of an ongoing negotiation dialogue, including phase, dialogue history, nesting depth, and expiration. |
| Copy-on-Resolve | The mechanism by which the ScopeResolver copies a concept and its dependencies from a higher scope into the local working graph, with a fandaws:resolvedFrom provenance annotation. |
| Curator | A role (Section 11.2) with authority to review and approve term promotions to a global federation, managing the shared ScopeConfiguration. |
| DeferredResult | A marker indicating an operation could not complete (typically due to offline status) and has been queued for later execution. |
| Display Label | The original form of a concept name as provided by the user or agent (fandaws:displayLabel). Preserved for human-readable descriptions and exports. |
| Edge-Canonical | An architecture where the browser/local runtime is the normative execution environment, not a degraded version of a server system. |
| EpistemicFailure | An event emitted when semantic deadlock is detected -- an agent has exhausted its retry budget for a concept/mutation pair and the assertion cannot be grounded. |
| Ethical Contestation Flag | A write-back annotation from the IEE indicating that a concept definition or relationship produces ethically problematic outcomes across one or more archetypal worldviews. |
| Fandaws | Fact and Answer Web Service. The conversational knowledge-building platform specified in this document. Operates as both a human-facing knowledge builder and a machine-to-machine ontology protocol. |
| FNSR | Federated Network for Structured Reasoning. A distributed reasoning architecture whose services consume structured knowledge for deductive, abductive, analogical, and counterfactual reasoning. |
| Fork (staleCopyAction) | A stale copy resolution mode where the local copy is automatically detached from its upstream source. The fandaws:resolvedFrom annotation is replaced with fandaws:forkedFrom, preserving the local reasoning history when upstream refactoring would corrupt it. Essential for M2M contexts (Section 5.10.3). |
| Global Federation | The global scope, consisting of an ordered set of IPFS-published Fandaws knowledge graphs searched in priority order during scope resolution. Analogous to a Unix PATH. |
| Global Scope | The lowest-priority tier in the scope hierarchy. A federation of published knowledge graphs, each with an IPFS CID, searched in a configurable resolution order. |
| GraphChangeEvent | A JSON-LD notification type emitted when a KnowledgeGraph is modified, enabling downstream cache invalidation and refresh. |
| GraphChangeSubscription | A contract enabling FNSR services to subscribe to specific concept subtrees for near-real-time delta notifications rather than bulk re-ingestion. |
| GraphMutation | A declarative description of changes to be applied to a KnowledgeGraph, emitted by computation and executed by the StateAdapter. |
| HIRI | A local-first verifiable knowledge protocol enabling agents to make knowledge claims with cryptographic provenance. Uses IPFS for content-addressed storage and Hypercore for sovereign logs. |
| Identity Simplification | The process of reducing complex multi-word terms to clean concept names for matching and deduplication. Uses the dual-label model (displayLabel/canonicalLabel) with locale-aware normalization. |
| IEE | Integral Ethics Engine. Evaluates actions from twelve archetypal worldviews, accumulating moral friction and synthesizing ethical judgments. Provides bidirectional feedback to Fandaws via Ethical Contestation Flags. |
| IPFS | InterPlanetary File System. A content-addressed, decentralized storage network providing immutable data distribution and verification. |
| JSON-LD | JSON for Linking Data. A W3C standard for expressing structured data as JSON with linked data semantics. The canonical representation format for all Fandaws data. |
| KnowledgeGraph | The top-level container for all knowledge in a Fandaws session, expressed as a JSON-LD document containing concepts, relationships, and metadata. |
| MachineSignal | A structured negotiation contract attached to ConversationPrompts in M2M mode, providing JSON Schema, valid values, and candidate IRIs so upstream agents can respond without parsing natural language. |
| Nested Negotiation | When defining a term requires first defining its parent or properties, creating a child session. Limited by maxNestingDepth (default: 10). |
| OCE | Ontological Constraint Engine. Validates proposed world states and state transitions against BFO-grounded ontological commitments. Returns typed violations with repair paths. |
| Optimistic Batching | A write strategy for HIRI/IPFS integration where mutations are applied to the in-memory graph immediately but committed to persistent storage in batches, trading crash durability for throughput. |
| Provenance Envelope | Metadata attached to every IntegrationAdapter result recording the service provider, version, input/output hashes, retrieval time, and cache status. Enables auditability and reproducibility. |
| Scope Configuration | A JSON-LD document defining the scope hierarchy for a session: context graph, user graph, and the ordered global federation of published graphs. |
| Scope Narrowing | The iterative process of walking up a concept hierarchy to determine the most general level at which a property applies. Functions as a semantic firewall in M2M contexts. |
| Scope Resolution | The process by which the ScopeResolver searches context, user, and global scope graphs for an existing definition of a term before creating a new one. |
| Scope Versioning | The principle that each IPFS CID in a ScopeEntry represents an immutable snapshot. Updating a scope means publishing a new CID and updating the ScopeConfiguration, making it a versioned dependency manifest analogous to package-lock.json (Section 4.2.8). |
| ScopeResolver | A core computation module (Section 3.2.7) that resolves terms across the scope hierarchy, detecting cross-scope conflicts and performing copy-on-resolve with provenance tracking. |
| Shadows (annotation) | A fandaws:shadows annotation on a locally defined concept indicating it deliberately overrides a definition in a higher scope. Warns downstream consumers that the concept is a local override requiring a disambiguated display label (Section 5.11.2). |
| Semantic Deadlock | A state where an agent persistently attempts to assert facts that the Validator rejects, creating an unbounded validation loop. Prevented by the repetitionLimit runtime constraint. |
| Semantic Firewall | The collective effect of scope narrowing, disambiguation, deduplication, and property redundancy checks that prevent unverified generalizations and hyper-specific noise from polluting the knowledge graph. |
| SHML | Semantically Honest Middle Layer. Ensures knowledge claims are framed with epistemic honesty, separating assertions from observations and tracking provenance. |
| Spec Test | The acceptance criterion: can a developer run this system with only a browser, Node.js, and JSON-LD files? |
| Structural Grounding | The requirement that every concept in the graph must have at least one of: a parent classification, an allowRoot flag, or a typed property. Replaces the subjective "abstract philosophical concept" rejection. |
| TagTeam.js | A discourse-model semantic parser that can serve as an alternative NLParser implementation for Fandaws. Operates on what was said, not what the world is. |
| Term Promotion | The process of publishing a concept from a lower scope to a higher scope (context to user, user to global) via IPFS publication and optional curator review. |
| Termidium | The deduplication engine that merges redundant concept nodes within a bounded search scope of 8 hierarchy levels. Uses ordered tie-breaking (depth, creation time, assertion count) and preserves source IRIs via fandaws:mergedFrom. |
| User Scope | The caller's personal knowledge graph, accumulating definitions across sessions. The middle tier in the scope resolution hierarchy. |

# 14. Revision History

| Version | Date | Author | Summary |
| --- | --- | --- | --- |
| 1.0 | Original | Aaron Damiano | Initial Fandaws functional specification (server-based architecture). |
| 2.0 | Feb 2026 | Aaron Damiano | Complete rebuild for edge-canonical architecture. JSON-LD canonical representation. Separation of concerns. Offline-first. Infrastructure-free core specification. |
| 3.0 | Feb 2026 | Aaron Damiano | Expanded Section 10 (Ecosystem Integration) from 4 service descriptions to 15 across five tiers with full JSON-LD contracts, adapter interfaces, and offline degradation behavior. Added SHML, OCE, ARCHON, Assay, IPFS, Aligned Property Commons, Code-to-CAD, Eulogy Pen. Added cross-cutting concerns: event notification model, versioning/cache invalidation, integration testing strategy, and complete ecosystem map. Expanded glossary with 13 new terms. |
| 3.1 | Feb 2026 | Aaron Damiano | Addressed M2M protocol critique. Reframed Fandaws as Structured Thinking Processor with semantic firewall properties. Added Machine-to-Machine Conversation Protocol (Section 5.9) with machineSignal on ConversationPrompt and structured negotiation flow. Added Semantic Deadlock Prevention (Section 6.7) as runtime constraint with EpistemicFailure events. Added FNSR streaming subscription model (GraphChangeSubscription). Added IEE bidirectional write-back via EthicalContestationFlag. Added HIRI/IPFS Optimistic Batching. Added M2M performance targets (Section 10.8.4) and M2M Simulation Testing (Section 9.5). Expanded OrchestrationAdapter with callerMode and deadlock detection. Added 8 new glossary terms. Updated configuration with 3 new parameters (callerMode, commitBatchInterval, commitBatchSize). Renamed testRepetitionLimit to repetitionLimit as runtime constraint. |
| 3.2 | Feb 2026 | Aaron Damiano | Addressed structural critique. Added Constraint 2.8 (No Probabilistic Core Computation) explicitly excluding LLMs from pipeline. Added IntegrationAdapter provenance envelope (Section 3.3.2). Added StateAdapter atomicity and concurrency model (Section 3.3.1). Replaced subjective validation rules with deterministic structural grounding criteria (Section 6.1). Expanded Identity Simplification with dual-label model and i18n normalization pipeline (Section 6.6). Expanded Termidium merge policy with tie-breaking, IRI preservation via mergedFrom, and large-merge review threshold (Section 6.2.2). Added graduated deadlock remediation: auto-repair, deferral, human escalation, epistemic failure (Section 6.7.2). Added Validator/OCE governance flow with strict/advisory modes (Section 10.4.3). Added EthicalContestationFlag governance: adjudication roles, automatic expiry, appeal mechanism, rate limiting (Section 10.5.2). Added authorization model with caller identity, roles, and provenance signing (Section 11.2). Added 7 new configuration parameters. Added Appendix A with 8 canonical JSON-LD examples. |
| 3.3 | Feb 2026 | Aaron Damiano | Restored scope hierarchy from Fandaws 3.0 requirements document, adapted for edge-canonical/IPFS architecture. Added ScopeResolver as core computation module (Section 3.2.7) with copy-on-resolve semantics and provenance tracking. Added scope model: context scope, user scope, and global federation of IPFS-published graphs with configurable resolution order (Section 4.2.8-4.2.12). Updated pipeline (Section 5.1) to include ScopeResolver step before Classifier. Added Scope Resolution Workflow (Section 5.10) with scope graph loading, copy-on-resolve semantics, and stale copy detection. Added Cross-Scope Conflict Resolution (Section 5.11) with three resolution actions: useDefinition, createDistinct, refine. Added Session Lifecycle (Section 5.12) with pause/resume/abandon, nested negotiation with depth limits, session expiration, and concurrent session limits. Added Term Promotion (Section 5.13) with promotion path (context to user to global), curator review workflow, and verification/endorsement model. Added curator role to authorization (Section 11.2). Added StateAdapter scope methods: listSessions, loadScopeConfig, saveScopeConfig. Added 6 new configuration parameters (sessionExpiryDuration, maxNestingDepth, maxConcurrentSessions, scopeResolutionEnabled, staleCopyAction). Added 15 new glossary terms. Added Appendix examples A.9-A.11. |
| 3.4 | Feb 2026 | Aaron Damiano | Final hardening addressing federation critique. Expanded stale copy detection (Section 5.10.3) with four action modes: prompt, auto-update, ignore, fork. Added fork mode for M2M contexts where upstream refactoring would corrupt local reasoning history. Added per-scope staleCopyAction override on ScopeEntry. Added scope versioning clarification: CIDs as immutable snapshots, ScopeConfiguration as versioned dependency manifest (Section 4.2.8). Added fandaws:shadows annotation and mandatory display-label disambiguation for refine conflict resolution action (Section 5.11.2). Added InMemoryStateAdapter indexing requirements: canonicalLabel, parent, child, and property reverse-lookup maps for Termidium performance at scale (Section 12.1). Added algorithmic curation (Section 5.13.3) for automatic promotion to community tier based on adoption, ethical safety, and structural quality thresholds. Added M2M deadlock prevention for IEE blocking flags: blocking contestation triggers EpistemicFailure in M2M mode rather than hanging (Section 10.5.2). Added 2 new configuration parameters (autoPromotionThreshold, autoPromotionCooldown). Added 4 new glossary terms. Updated Appendix A.9 with per-scope staleCopyAction and versioning note. |


# Appendix A: Canonical JSON-LD Examples

This appendix provides reference JSON-LD documents for implementers. These are normative examples — conforming implementations must produce and consume documents structurally compatible with these shapes.

## A.1 Fandaws Context

```json
{
  "@context": {
    "fandaws": "https://fandaws.org/schema/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "bfo": "http://purl.obolibrary.org/obo/",
    "schema": "https://schema.org/",
    "fandaws:displayLabel": { "@type": "xsd:string" },
    "fandaws:canonicalLabel": { "@type": "xsd:string" },
    "fandaws:parent": { "@type": "@id" },
    "fandaws:children": { "@container": "@set", "@type": "@id" },
    "fandaws:properties": { "@container": "@set" },
    "fandaws:mergedFrom": { "@container": "@set", "@type": "@id" },
    "fandaws:createdAt": { "@type": "xsd:dateTime" },
    "fandaws:bfoMapping": { "@type": "@id" }
  }
}
```

## A.2 Concept

```json
{
  "@id": "fandaws:concept/dog",
  "@type": "fandaws:Concept",
  "fandaws:displayLabel": "Dog",
  "fandaws:canonicalLabel": "dog",
  "fandaws:parent": "fandaws:concept/animal",
  "fandaws:children": [],
  "fandaws:properties": ["fandaws:property/dog-has-fur"],
  "fandaws:bfoMapping": "bfo:0000040",
  "fandaws:depth": 3,
  "fandaws:createdAt": "2026-02-08T14:30:00Z",
  "fandaws:mergedFrom": []
}
```

## A.3 GraphMutation (Property Attachment)

```json
{
  "@type": "fandaws:GraphMutation",
  "fandaws:additions": [
    {
      "@id": "fandaws:property/animal-has-eyes",
      "@type": "fandaws:Property",
      "fandaws:displayLabel": "has eyes",
      "fandaws:attachedTo": "fandaws:concept/animal",
      "fandaws:scope": "inherited"
    }
  ],
  "fandaws:modifications": [],
  "fandaws:deletions": [],
  "fandaws:merges": [],
  "fandaws:reason": "Scope narrowing: property 'has eyes' promoted from 'dog' to 'animal'",
  "fandaws:validatedBy": "fandaws:validation/v-20260208-001"
}
```

## A.4 ConversationPrompt (Human Mode)

```json
{
  "@type": "fandaws:ConversationPrompt",
  "fandaws:promptType": "scopeNarrowing",
  "fandaws:text": "Does an Animal have eyes, or is this specific to Dog?",
  "fandaws:options": ["Animal (applies to all animals)", "Dog (specific to dogs)"],
  "fandaws:context": {
    "property": "has eyes",
    "originalConcept": "fandaws:concept/dog",
    "candidateAncestor": "fandaws:concept/animal"
  },
  "fandaws:machineSignal": null
}
```

## A.5 ConversationPrompt (M2M Mode with MachineSignal)

```json
{
  "@type": "fandaws:ConversationPrompt",
  "fandaws:promptType": "scopeNarrowing",
  "fandaws:text": "Does an Animal have eyes, or is this specific to Dog?",
  "fandaws:options": ["Animal (applies to all animals)", "Dog (specific to dogs)"],
  "fandaws:context": {
    "property": "has eyes",
    "originalConcept": "fandaws:concept/dog",
    "candidateAncestor": "fandaws:concept/animal"
  },
  "fandaws:machineSignal": {
    "fandaws:expectedSchema": {
      "type": "object",
      "properties": {
        "selection": { "type": "string", "enum": ["animal", "dog"] }
      },
      "required": ["selection"]
    },
    "fandaws:validValues": ["animal", "dog"],
    "fandaws:constraintType": "scopeLevel",
    "fandaws:candidateIRIs": [
      "fandaws:concept/animal",
      "fandaws:concept/dog"
    ],
    "fandaws:hierarchyContext": {
      "fandaws:concept/animal": { "depth": 2, "children": ["fandaws:concept/dog", "fandaws:concept/cat"] },
      "fandaws:concept/dog": { "depth": 3, "parent": "fandaws:concept/animal" }
    }
  }
}
```

## A.6 EpistemicFailure

```json
{
  "@type": "fandaws:EpistemicFailure",
  "fandaws:conceptId": "fandaws:concept/truth",
  "fandaws:mutationType": "classification",
  "fandaws:attemptCount": 5,
  "fandaws:rejectionReasons": [
    "structuralGroundingError: concept has no parent classification",
    "structuralGroundingError: concept has no parent classification",
    "structuralGroundingError: concept has no typed property",
    "structuralGroundingError: concept has no parent classification",
    "structuralGroundingError: concept has no parent classification"
  ],
  "fandaws:suggestedActions": [
    "Classify 'truth' under an existing concept: 'Truth is a [category].'",
    "Add a typed property: 'Truth has [characteristic].'"
  ],
  "fandaws:repairPaths": null,
  "fandaws:escalatedToHuman": false
}
```

## A.7 IntegrationAdapter Provenance Envelope

```json
{
  "@type": "fandaws:DictionaryResult",
  "fandaws:term": "dog",
  "fandaws:definitions": [
    "A domesticated carnivorous mammal (Canis familiaris)"
  ],
  "fandaws:provenance": {
    "fandaws:provenance.provider": "wordnik-api",
    "fandaws:provenance.version": "4.0",
    "fandaws:provenance.inputHash": "sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    "fandaws:provenance.outputHash": "sha256:a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a",
    "fandaws:provenance.retrievedAt": "2026-02-08T14:25:00Z",
    "fandaws:provenance.fromCache": false
  }
}
```

## A.8 EthicalContestationFlag

```json
{
  "@type": "fandaws:EthicalContestationFlag",
  "fandaws:conceptId": "fandaws:concept/person",
  "fandaws:contestationType": "exclusion",
  "fandaws:worldviewSource": ["Idealism", "Monadism"],
  "fandaws:frictionScore": 0.82,
  "fandaws:explanation": "The current definition of 'person' requires biological embodiment, which excludes synthetic agents that may possess morally relevant cognitive capacities.",
  "fandaws:suggestedRevision": {
    "@type": "fandaws:GraphMutation",
    "fandaws:modifications": [
      {
        "target": "fandaws:concept/person",
        "field": "fandaws:properties",
        "action": "add",
        "value": {
          "@type": "fandaws:Property",
          "fandaws:displayLabel": "may be biologically or synthetically embodied",
          "fandaws:attachedTo": "fandaws:concept/person"
        }
      }
    ]
  },
  "fandaws:severity": "warning"
}
```

## A.9 ScopeConfiguration

```json
{
  "@type": "fandaws:ScopeConfiguration",
  "fandaws:contextGraphId": "fandaws:graph/case-12345",
  "fandaws:userGraphId": "fandaws:graph/user-aaron",
  "fandaws:globalFederation": [
    {
      "fandaws:graphId": "fandaws:graph/bfo-core",
      "fandaws:label": "BFO Core Ontology v2.0",
      "fandaws:ipfsCid": "QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG",
      "fandaws:priority": 1,
      "fandaws:trustLevel": "authoritative",
      "fandaws:staleCopyAction": "auto-update"
    },
    {
      "fandaws:graphId": "fandaws:graph/medical-domain",
      "fandaws:label": "Medical Domain Ontology v1.2",
      "fandaws:ipfsCid": "QmT5NvUtoM5nWFfrQdVrFtvGfKFmG7AHE8P34isapyhCxX",
      "fandaws:priority": 2,
      "fandaws:trustLevel": "community",
      "fandaws:staleCopyAction": null
    },
    {
      "fandaws:graphId": "fandaws:graph/ethics-research",
      "fandaws:label": "Ethics Research Terms v0.3",
      "fandaws:ipfsCid": "QmPZ9gcCEpqKTo6aq61g2nXGUhM4iCL3ewB6LDXZCtioEB",
      "fandaws:priority": 3,
      "fandaws:trustLevel": "experimental",
      "fandaws:staleCopyAction": "fork"
    }
  ]
}
```

Note: Each `fandaws:ipfsCid` pins a specific immutable snapshot. "Medical Domain Ontology v1.2" will always resolve to exactly this CID. To update to v1.3, the curator publishes a new graph to IPFS (producing a new CID) and updates this ScopeConfiguration. The old CID remains accessible for any caller who has not updated their configuration.

## A.10 ScopeResolution (Resolved)

```json
{
  "@type": "fandaws:ScopeResolution",
  "fandaws:term": "autonomy",
  "fandaws:status": "resolved",
  "fandaws:resolvedConcept": {
    "@id": "fandaws:concept/autonomy",
    "@type": "fandaws:Concept",
    "fandaws:displayLabel": "Autonomy",
    "fandaws:canonicalLabel": "autonomy",
    "fandaws:parent": "fandaws:concept/capacity",
    "fandaws:resolvedFrom": {
      "fandaws:resolvedFrom.graphId": "fandaws:graph/ethics-research",
      "fandaws:resolvedFrom.conceptIri": "fandaws:graph/ethics-research/concept/autonomy",
      "fandaws:resolvedFrom.scopeType": "global",
      "fandaws:resolvedFrom.resolvedAt": "2026-02-08T15:00:00Z",
      "fandaws:resolvedFrom.graphVersion": "sha256:abc123"
    }
  },
  "fandaws:sourceScope": {
    "fandaws:scopeType": "global",
    "fandaws:graphId": "fandaws:graph/ethics-research",
    "fandaws:conceptIri": "fandaws:graph/ethics-research/concept/autonomy",
    "fandaws:resolvedAt": "2026-02-08T15:00:00Z"
  },
  "fandaws:conflictReport": null,
  "fandaws:skippedScopes": []
}
```

## A.11 ScopeResolution (Conflict)

```json
{
  "@type": "fandaws:ScopeResolution",
  "fandaws:term": "autonomy",
  "fandaws:status": "conflict",
  "fandaws:resolvedConcept": null,
  "fandaws:sourceScope": null,
  "fandaws:conflictReport": {
    "@type": "fandaws:ConflictReport",
    "fandaws:term": "autonomy",
    "fandaws:definitions": [
      {
        "fandaws:conceptIri": "fandaws:graph/user-aaron/concept/autonomy",
        "fandaws:scopeType": "user",
        "fandaws:graphId": "fandaws:graph/user-aaron",
        "fandaws:parentChain": ["capacity", "quality", "entity"],
        "fandaws:definition": "Autonomy is a capacity that has self-governance and moral significance.",
        "fandaws:properties": ["self-governance", "moral significance"]
      },
      {
        "fandaws:conceptIri": "fandaws:graph/ethics-research/concept/autonomy",
        "fandaws:scopeType": "global",
        "fandaws:graphId": "fandaws:graph/ethics-research",
        "fandaws:parentChain": ["right", "social construct", "entity"],
        "fandaws:definition": "Autonomy is a right that has legal recognition and political foundation.",
        "fandaws:properties": ["legal recognition", "political foundation"]
      }
    ],
    "fandaws:resolutionOptions": [
      {
        "fandaws:action": "useDefinition",
        "fandaws:label": "Use 'capacity' definition from your personal graph",
        "fandaws:targetDefinition": 0
      },
      {
        "fandaws:action": "useDefinition",
        "fandaws:label": "Use 'right' definition from Ethics Research",
        "fandaws:targetDefinition": 1
      },
      {
        "fandaws:action": "createDistinct",
        "fandaws:label": "These are different concepts (e.g., 'moral autonomy' and 'political autonomy')"
      },
      {
        "fandaws:action": "refine",
        "fandaws:label": "Define 'autonomy' fresh for this context"
      }
    ]
  },
  "fandaws:skippedScopes": []
}
```