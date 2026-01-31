# Fandaws 3.0 - Functional Requirements Document
## Runtime Semantic Negotiation Service

**Version:** 3.0.0  
**Date:** December 30, 2025  
**Status:** Draft for Review  
**Author:** Aaron Damaino  
**Document Type:** Functional Requirements

---

## DOCUMENT CONTROL

### Version History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 3.0.0 | 2025-12-30 | Aaron Damaino | Initial draft for new architecture |

### Review & Approval
| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | Aaron Damaino | | |
| Technical Lead | | | |
| Integration Lead | | | |

---

## TABLE OF CONTENTS

1. [Introduction](#1-introduction)
2. [System Overview](#2-system-overview)
3. [Functional Requirements](#3-functional-requirements)
4. [Integration Requirements](#4-integration-requirements)
5. [Data Requirements](#5-data-requirements)
6. [User Interface Requirements](#6-user-interface-requirements)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [Acceptance Criteria](#8-acceptance-criteria)
9. [Appendices](#9-appendices)

---

## 1. INTRODUCTION

### 1.1 Purpose

This document specifies the functional requirements for Fandaws 3.0, a semantic negotiation service that enables AI ethics systems to dynamically ground ambiguous or unknown terms through structured dialogue with users while maintaining formal ontological consistency.

### 1.2 Scope

**In Scope:**
- Runtime term resolution via API
- Structured semantic negotiation dialogues
- User, context, and global ontology management
- Relationship consistency validation
- Integration with ARCHON, Synthetic Moral Agents, ECCPS, and HIRI
- OWL/RDF ontology export
- Conflict detection and resolution

**Out of Scope:**
- Standalone web application (except admin tools)
- Natural language processing/understanding (delegated to calling systems or optional LLM layer)
- General-purpose knowledge graph (focus is on grounding terms for ethics systems)
- Real-time collaboration UI (MVP uses async negotiation)

### 1.3 Definitions

| Term | Definition |
|------|------------|
| **Term** | A concept or entity that needs ontological grounding (e.g., "autonomy", "consciousness") |
| **Grounding** | The process of establishing formal ontological relationships for a term |
| **Negotiation** | Structured dialogue to clarify what a term IS and what it HAS |
| **Scope** | The visibility boundary of ontological definitions (global, user, context) |
| **Consistency Check** | Validation rules preventing contradictory or redundant relationships |
| **Calling System** | External system requesting term resolution (ARCHON, Synthetic Moral Agent, ECCPS) |

### 1.4 References

- Basic Formal Ontology (BFO) 2.0 Specification
- OWL 2 Web Ontology Language Document Overview
- **Semantically Honest Middle Layer (SHML)** - Architectural Basis
- **Grounded Intentionality Theory (GIT)** - Core Ontology
- **Generative Concretization v2.0** - LLM Integration Spec
- HIRI Protocol Specification
- ECCPS Architecture Document
- Synthetic Moral Agent Design Document

---

## 2. SYSTEM OVERVIEW

### 2.1 System Context

```
┌─────────────────────────────────────────────────────────────┐
│  External Systems (Calling Systems)                          │
│  ┌─────────┐  ┌──────────────┐  ┌────────┐  ┌────────┐    │
│  │ ARCHON  │  │ Syn. Moral   │  │ ECCPS  │  │  HIRI  │    │
│  │         │  │ Agents       │  │        │  │        │    │
│  └────┬────┘  └──────┬───────┘  └───┬────┘  └───┬────┘    │
└───────┼──────────────┼──────────────┼───────────┼─────────┘
        │              │              │           │
        └──────────────┼──────────────┼───────────┘
                       │              │
        ┌──────────────▼──────────────▼──────────────┐
        │     FANDAWS 3.0 API Gateway                 │
        │     - Authentication                        │
        │     - Rate Limiting                         │
        │     - Request Routing                       │
        └──────────────┬──────────────────────────────┘
                       │
        ┌──────────────▼──────────────────────────────┐
        │     CORE SERVICES                            │
        │  ┌──────────────────────────────────────┐   │
        │  │ Term Resolution Service              │   │
        │  │ - Scope hierarchy lookup             │   │
        │  │ - Cache management                   │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │ Semantic Negotiation Engine          │   │
        │  │ - Dialogue state management          │   │
        │  │ - Question generation                │   │
        │  │ - Response parsing                   │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │ Consistency Validation Engine        │   │
        │  │ - 7 relationship checks              │   │
        │  │ - Conflict detection                 │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │ Context Management Service           │   │
        │  │ - Scope resolution                   │   │
        │  │ - Ontology versioning                │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │ Export Service                       │   │
        │  │ - OWL generation                     │   │
        │  │ - JSON-LD formatting                 │   │
        │  └──────────────────────────────────────┘   │
        └──────────────┬──────────────────────────────┘
                       │
        ┌──────────────▼──────────────────────────────┐
        │     DATA LAYER                               │
        │  ┌──────────────────────────────────────┐   │
        │  │ Neo4j Graph Database                 │   │
        │  │ - Term nodes                         │   │
        │  │ - Relationship edges                 │   │
        │  │ - Scope partitioning                 │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │ PostgreSQL Relational Database       │   │
        │  │ - User accounts                      │   │
        │  │ - Negotiation sessions               │   │
        │  │ - Audit logs                         │   │
        │  └──────────────────────────────────────┘   │
        │  ┌──────────────────────────────────────┐   │
        │  │ Redis Cache                          │   │
        │  │ - Frequent term lookups              │   │
        │  │ - Session state                      │   │
        │  └──────────────────────────────────────┘   │
        └──────────────────────────────────────────────┘
```

### 2.2 User Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| **System User** | External AI systems (ARCHON, etc.) | Request term resolution, initiate negotiations, read global ontology |
| **End User** | Human interacting through calling system | Define terms in user/context scopes, resolve conflicts |
| **Administrator** | Fandaws system administrator | Manage global ontology, review conflicts, system configuration |
| **Curator** | Community ontology curator | Promote user terms to global, resolve global conflicts |

### 2.3 Key Use Cases

| UC ID | Use Case Name | Actor |
|-------|---------------|-------|
| UC-01 | Resolve Known Term | System User |
| UC-02 | Negotiate Unknown Term | System User + End User |
| UC-03 | Detect Semantic Conflict | System |
| UC-04 | Resolve Semantic Conflict | End User |
| UC-05 | Validate Relationship | System User |
| UC-06 | Export Ontology | System User |
| UC-07 | Create Context Ontology | System User |
| UC-08 | Promote Term to Global | Curator |

---

## 3. FUNCTIONAL REQUIREMENTS

### 3.1 Term Resolution Service

#### FR-TRS-001: Resolve Term in Scope Hierarchy
**Priority:** MUST HAVE  
**User Story:** As a calling system, I need to resolve a term through the scope hierarchy so I can use formally grounded concepts in reasoning.

**Description:**  
When a calling system requests term resolution, the service must search through the scope hierarchy (context → user → global) and return the first matching definition found.

**Inputs:**
- `term` (string): The term to resolve
- `user_id` (UUID): Requesting user identifier
- `context_id` (UUID, optional): Context identifier
- `usage_example` (string, optional): Example of how term is used
- `requesting_system` (string): Name of calling system

**Processing:**
1. Normalize term (lowercase, trim whitespace)
2. If `context_id` provided, search context scope
3. If not found, search user scope for `user_id`
4. If not found, search global scope
5. If found, return full definition with relationships
6. If not found, return status "unknown"

**Outputs:**
```json
{
  "status": "resolved" | "needs_clarification" | "unknown",
  "term_uuid": "uuid",
  "term": "autonomy",
  "normalized_term": "autonomy",
  "definition": "Autonomy is a capacity to self-govern that has moral significance",
  "scope": "user",
  "scope_id": "user-uuid",
  "is_a_chain": [
    {"uuid": "...", "name": "capacity"},
    {"uuid": "...", "name": "quality"},
    {"uuid": "...", "name": "entity"}
  ],
  "has_relationships": [
    {"uuid": "...", "name": "self-governance", "relationship_type": "HAS"},
    {"uuid": "...", "name": "moral significance", "relationship_type": "HAS"}
  ],
  "bfo_mapping": "BFO_0000017",
  "created_at": "2025-12-30T10:00:00Z",
  "verified": true,
  "verification_count": 5
}
```

**Acceptance Criteria:**
- ✓ Searches context scope first if context_id provided
- ✓ Falls back to user scope, then global scope
- ✓ Returns full relationship graph for resolved terms
- ✓ Response time < 200ms for cached terms
- ✓ Response time < 500ms for uncached terms
- ✓ Handles non-existent user_id gracefully (400 error)
- ✓ Handles malformed requests (400 error)

**Error Conditions:**
- Invalid user_id → 400 Bad Request
- Invalid context_id → 400 Bad Request
- System error → 500 Internal Server Error

---

#### FR-TRS-002: Handle Ambiguous Terms
**Priority:** SHOULD HAVE  
**User Story:** As a calling system, when a term has multiple meanings, I need the system to identify this so the user can clarify.

**Description:**  
If a term exists with multiple incompatible definitions across scopes or within the same scope, the system should detect this and request clarification.

**Inputs:**
- Same as FR-TRS-001

**Processing:**
1. Search for term across relevant scopes
2. If multiple definitions found with incompatible IS_A chains, flag as ambiguous
3. Return all definitions with clarification prompt

**Outputs:**
```json
{
  "status": "needs_clarification",
  "term": "autonomy",
  "message": "This term has multiple meanings. Which do you mean?",
  "options": [
    {
      "term_uuid": "uuid-1",
      "definition": "Autonomy is a political right...",
      "scope": "global",
      "usage_context": "political science"
    },
    {
      "term_uuid": "uuid-2",
      "definition": "Autonomy is a moral capacity...",
      "scope": "global",
      "usage_context": "ethics"
    }
  ]
}
```

**Acceptance Criteria:**
- ✓ Detects incompatible IS_A chains (e.g., capacity vs right)
- ✓ Returns all relevant options
- ✓ Includes usage context for each option
- ✓ Allows user to select or initiate new negotiation

---

#### FR-TRS-003: Cache Frequently Resolved Terms
**Priority:** SHOULD HAVE  
**User Story:** As the system, I need to cache frequently resolved terms so I can respond faster to term resolution requests.

**Description:**  
Terms resolved frequently (based on access patterns) should be cached in Redis with appropriate TTL.

**Processing:**
1. On term resolution, increment access counter
2. If access_count > threshold, add to cache
3. Cache key: `term:{scope}:{scope_id}:{normalized_term}`
4. TTL: 1 hour for user/context scope, 24 hours for global scope
5. Invalidate cache on term update

**Acceptance Criteria:**
- ✓ Cached terms return in < 50ms
- ✓ Cache hit rate > 80% for frequently accessed terms
- ✓ Cache invalidated on term updates
- ✓ Cache respects scope boundaries (no leakage)

---

### 3.2 Semantic Negotiation Service

#### FR-SNS-001: Initiate Negotiation Session
**Priority:** MUST HAVE  
**User Story:** As a calling system, when I encounter an unknown term, I need to start a negotiation session so the user can define it.

**Description:**  
When term resolution returns "unknown", the calling system can initiate a structured negotiation session.

**Inputs:**
- `term` (string): Term to negotiate
- `user_id` (UUID): User who will define term
- `context_id` (UUID, optional): Context for definition
- `requesting_system` (string): System requesting negotiation
- `usage_example` (string, optional): How term is being used

**Processing:**
1. Create negotiation session record
2. Set state to "negotiating"
3. Generate initial question: "What IS {term}?"
4. Store session in database and Redis
5. Return session details

**Outputs:**
```json
{
  "session_id": "uuid",
  "term": "autonomy",
  "state": "negotiating",
  "current_question": "What IS autonomy?",
  "dialogue_type": "is_a",
  "expected_response_format": "free_text",
  "examples": [
    "Autonomy is a capacity",
    "Autonomy is a right",
    "Autonomy is a quality"
  ],
  "created_at": "2025-12-30T10:00:00Z"
}
```

**Acceptance Criteria:**
- ✓ Creates unique session_id
- ✓ Stores session in PostgreSQL and Redis
- ✓ Generates contextually appropriate initial question
- ✓ Session expires after 24 hours of inactivity
- ✓ User can have max 5 concurrent sessions

---

#### FR-SNS-002: Continue Negotiation - IS_A Phase
**Priority:** MUST HAVE  
**User Story:** As an end user, I need to answer questions about what a term IS so the system can place it in the ontology.

**Description:**  
Process user responses during the IS_A phase of negotiation to establish taxonomic relationships.

**Inputs:**
- `session_id` (UUID): Active negotiation session
- `user_response` (string): User's answer to current question

**Processing:**
1. Load session from database/cache
2. Parse user response to extract parent term
   - Pattern: "{term} is a {parent_term}"
   - Pattern: "{term} is an {parent_term}"
   - Pattern: "a {parent_term}"
3. Check if parent_term exists in ontology
4. If parent exists:
   - Record IS_A relationship (pending validation)
   - Move to HAS phase
5. If parent unknown:
   - Create nested negotiation for parent term
   - Pause current session
6. Update session state
7. Generate next question

**Response (Parent Found):**
```json
{
  "session_id": "uuid",
  "state": "negotiating",
  "current_question": "What does autonomy have? (Or what are properties of autonomy?)",
  "dialogue_type": "has",
  "progress": {
    "phase": "has",
    "is_a_resolved": true,
    "parent_term": "capacity",
    "parent_uuid": "uuid"
  }
}
```

**Response (Parent Unknown):**
```json
{
  "session_id": "uuid",
  "state": "negotiating_nested",
  "current_question": "I'm not familiar with 'capacity'. What IS capacity?",
  "dialogue_type": "is_a",
  "nested_term": "capacity",
  "nested_session_id": "uuid-nested",
  "message": "We'll define 'capacity' first, then return to 'autonomy'"
}
```

**Acceptance Criteria:**
- ✓ Correctly parses IS_A responses (90%+ accuracy)
- ✓ Handles variations: "is a", "is an", implicit parent
- ✓ Detects unknown parents and initiates nested negotiation
- ✓ Maintains session stack for nested negotiations
- ✓ Prevents infinite recursion (max depth: 10)
- ✓ Updates session state correctly
- ✓ Logs all dialogue for audit

**Error Conditions:**
- Cannot parse response → Ask clarifying question
- Max nesting depth reached → Suggest using existing term
- Session expired → Return error, offer restart

---

#### FR-SNS-003: Continue Negotiation - HAS Phase
**Priority:** MUST HAVE  
**User Story:** As an end user, I need to specify what properties or parts a term has so the system captures its distinguishing features.

**Description:**  
Process user responses during the HAS phase to establish property/part relationships.

**Inputs:**
- `session_id` (UUID): Active negotiation session
- `user_response` (string): User's answer about properties

**Processing:**
1. Load session from database/cache
2. Parse user response to extract properties
   - Pattern: "{term} has {property}"
   - Pattern: "{property}"
   - Pattern: "nothing" or "none" or "skip"
3. For each extracted property:
   - Check if property exists in ontology
   - If exists, record HAS relationship (pending validation)
   - If unknown, queue for nested negotiation
4. Run consistency checks (FR-CVS-001 through FR-CVS-007)
5. If validation passes:
   - Record relationship
   - Ask if more properties exist
6. If validation fails:
   - Present conflict
   - Request resolution
7. Update session state

**Response (Properties Added):**
```json
{
  "session_id": "uuid",
  "state": "negotiating",
  "current_question": "Does autonomy have any other properties or characteristics?",
  "dialogue_type": "has",
  "progress": {
    "phase": "has",
    "is_a_resolved": true,
    "properties_added": [
      {"name": "self-governance", "uuid": "uuid"},
      {"name": "moral significance", "uuid": "uuid"}
    ]
  },
  "actions": ["add_more", "complete"]
}
```

**Response (Validation Conflict):**
```json
{
  "session_id": "uuid",
  "state": "conflict",
  "conflict_type": "inherited_redundancy",
  "message": "'Autonomy' already inherits 'self-governance' from its parent 'capacity'. Do you want to add it anyway?",
  "options": [
    {"action": "skip", "label": "Skip - it's already inherited"},
    {"action": "add_anyway", "label": "Add anyway - it's important to emphasize"},
    {"action": "reconsider", "label": "I need to reconsider the parent relationship"}
  ]
}
```

**Acceptance Criteria:**
- ✓ Correctly parses HAS responses (85%+ accuracy)
- ✓ Handles multiple properties in one response
- ✓ Detects "none"/"nothing" to skip to completion
- ✓ Runs all 7 consistency checks before recording
- ✓ Presents conflicts clearly with options
- ✓ Allows user to add more properties iteratively
- ✓ Tracks all properties discovered

---

#### FR-SNS-004: Complete Negotiation
**Priority:** MUST HAVE  
**User Story:** As an end user, when I've defined a term sufficiently, I need the system to finalize the definition and make it available for use.

**Description:**  
Finalize negotiation session, commit term to ontology, generate definition string.

**Inputs:**
- `session_id` (UUID): Active negotiation session
- `user_action` (string): "complete" or explicit completion signal

**Processing:**
1. Load complete session data
2. Validate all relationships one final time
3. Generate definition string:
   - Pattern: "{Term} is a {parent} that has {prop1}, {prop2}..."
4. Create term node in graph database
5. Create relationship edges
6. Generate term UUID
7. Mark session as complete
8. Clear from Redis cache (keep in DB for audit)
9. Return completed term details
10. Optionally notify HIRI for attestation

**Outputs:**
```json
{
  "session_id": "uuid",
  "state": "complete",
  "term_uuid": "uuid-new-term",
  "term": "autonomy",
  "definition": "Autonomy is a capacity that has self-governance, moral significance.",
  "scope": "user",
  "scope_id": "user-uuid",
  "ontology_graph": {
    "term": {"uuid": "...", "name": "autonomy"},
    "is_a": [
      {"uuid": "...", "name": "capacity"}
    ],
    "has": [
      {"uuid": "...", "name": "self-governance"},
      {"uuid": "...", "name": "moral significance"}
    ]
  },
  "created_at": "2025-12-30T10:15:00Z",
  "negotiation_duration_seconds": 180,
  "hiri_attestation_id": "uuid" // if HIRI integration enabled
}
```

**Acceptance Criteria:**
- ✓ Generates grammatically correct definition
- ✓ Creates all nodes and edges atomically (transaction)
- ✓ Assigns globally unique UUID
- ✓ Term immediately available for resolution
- ✓ Session marked complete and archived
- ✓ Audit log created
- ✓ HIRI attestation created if configured
- ✓ Calling system notified via webhook (if registered)

---

#### FR-SNS-005: Abandon/Pause Negotiation
**Priority:** SHOULD HAVE  
**User Story:** As an end user, I need to pause or abandon a negotiation if I'm unsure or need more time.

**Description:**  
Allow users to pause negotiations and resume later, or abandon entirely.

**Inputs:**
- `session_id` (UUID): Active negotiation session
- `action` (string): "pause" or "abandon"

**Processing:**
1. If "pause":
   - Update state to "paused"
   - Keep in database
   - Remove from active Redis cache
   - Set expiration: 7 days
2. If "abandon":
   - Update state to "abandoned"
   - Log reason if provided
   - Clean up partial relationships
   - Archive session

**Acceptance Criteria:**
- ✓ Paused sessions can be resumed within 7 days
- ✓ Abandoned sessions cleaned up properly
- ✓ User can list their paused sessions
- ✓ System suggests resuming paused sessions when term re-encountered

---

### 3.3 Consistency Validation Service

#### FR-CVS-001: Prevent Duplicate Relationships
**Priority:** MUST HAVE  
**User Story:** As the system, I need to prevent duplicate relationships so the ontology remains clean and unambiguous.

**Description:**  
Before creating any relationship, check if identical relationship already exists.

**Cypher Query:**
```cypher
MATCH (x {uuid: $subject_uuid})-[r:HAS]->(a {uuid: $object_uuid})
RETURN count(r) as existing
```

**Validation Logic:**
- If `existing > 0` → REJECT with reason "duplicate"

**Acceptance Criteria:**
- ✓ Detects exact duplicates (same subject, relation, object)
- ✓ Returns clear error message
- ✓ Executes in < 50ms

---

#### FR-CVS-002: Prevent Ancestor Relationships on Same Node
**Priority:** MUST HAVE  
**User Story:** As the system, I need to prevent adding relationships that are more generic than existing ones on the same node.

**Description:**  
If node X has relationship to A, and user tries to add relationship from X to B where A IS_A B, this is redundant. Reject.

**Example:**
- Existing: `(dog)-[:HAS]->(tail)`
- `(tail)-[:IS_A]->(appendage)`
- User tries: `(dog)-[:HAS]->(appendage)`
- Result: REJECT (already has more specific)

**Cypher Query:**
```cypher
MATCH (x {uuid: $subject_uuid}), (b {uuid: $object_uuid})
WITH x, b
MATCH (x)-[:HAS]->(a)-[:IS_A*]->(b)
RETURN x, a, b
```

**Validation Logic:**
- If query returns data → REJECT with reason "has_more_specific"
- Include path in error message

**Acceptance Criteria:**
- ✓ Detects ancestor relationships through IS_A chain
- ✓ Works with multi-level hierarchies (IS_A*)
- ✓ Explains which specific relationship exists
- ✓ Executes in < 100ms

---

#### FR-CVS-003: Replace Generic with Specific on Same Node
**Priority:** MUST HAVE  
**User Story:** As the system, when a user adds a more specific relationship that makes an existing generic one redundant, I need to replace the generic with the specific.

**Description:**  
Inverse of FR-CVS-002. If node X has relationship to B, and user adds relationship from X to A where A IS_A B, remove B relationship and add A.

**Example:**
- Existing: `(dog)-[:HAS]->(appendage)`
- `(tail)-[:IS_A]->(appendage)`
- User adds: `(dog)-[:HAS]->(tail)`
- Result: DELETE `(dog)-[:HAS]->(appendage)`, ADD `(dog)-[:HAS]->(tail)`

**Cypher Query:**
```cypher
MATCH (x {uuid: $subject_uuid}), (a {uuid: $object_uuid})
WITH x, a
MATCH (x)-[r:HAS]->(b)<-[:IS_A*]-(a)
DELETE r
// Then add new relationship
```

**Validation Logic:**
- If query finds generic relationship → DELETE it
- Then CREATE new specific relationship
- Log the replacement in audit log

**Acceptance Criteria:**
- ✓ Correctly identifies generic relationship
- ✓ Deletes generic atomically with adding specific
- ✓ Transaction rolls back if anything fails
- ✓ Audit log records the replacement
- ✓ Executes in < 100ms

---

#### FR-CVS-004: Prevent Inherited Redundant Relationships
**Priority:** MUST HAVE  
**User Story:** As the system, I need to prevent adding relationships to nodes that already inherit those relationships from ancestors.

**Description:**  
If node X has relationship to A, and node Y IS_A X, don't allow adding relationship from Y to A (it's inherited).

**Example:**
- Existing: `(dog)-[:HAS]->(tail)` and `(boxer)-[:IS_A]->(dog)`
- User tries: `(boxer)-[:HAS]->(tail)`
- Result: REJECT (inherited from dog)

**Cypher Query:**
```cypher
MATCH (x {uuid: $subject_uuid}), (a {uuid: $object_uuid})
WITH x, a
MATCH (x)-[:IS_A*]->(y)-[:HAS]->(a)
RETURN x, y, a
```

**Validation Logic:**
- If query returns data → REJECT with reason "inherited_from_ancestor"
- Include ancestor name in error message

**Acceptance Criteria:**
- ✓ Detects inheritance through IS_A chain
- ✓ Works with multi-level hierarchies
- ✓ Explains which ancestor has the relationship
- ✓ Executes in < 100ms

---

#### FR-CVS-005: Push Relationship to Ancestor
**Priority:** MUST HAVE  
**User Story:** As the system, when a user adds a relationship to an ancestor that makes descendant relationships redundant, I need to move the relationship up.

**Description:**  
Inverse of FR-CVS-004. If descendant has relationship and user adds same to ancestor, remove from descendant(s).

**Example:**
- Existing: `(boxer)-[:HAS]->(tail)` and `(boxer)-[:IS_A]->(dog)`
- User adds: `(dog)-[:HAS]->(tail)`
- Result: DELETE `(boxer)-[:HAS]->(tail)`, ADD `(dog)-[:HAS]->(tail)`

**Cypher Query:**
```cypher
MATCH (y {uuid: $subject_uuid}), (a {uuid: $object_uuid})
WITH y, a
MATCH (a)<-[r:HAS]-(x)-[:IS_A*]->(y)
DELETE r
// Then add new relationship to ancestor
```

**Validation Logic:**
- Find all descendants with same relationship
- DELETE all descendant relationships
- CREATE ancestor relationship
- Log all deletions in audit log

**Acceptance Criteria:**
- ✓ Finds all descendants with redundant relationship
- ✓ Deletes all in single transaction
- ✓ Transaction rolls back if anything fails
- ✓ Audit log records all deletions and reason
- ✓ Executes in < 200ms even with many descendants

---

#### FR-CVS-006: Prevent Generic Relationships on Descendants
**Priority:** MUST HAVE  
**User Story:** As the system, I need to prevent descendants from having relationships that are more generic than their ancestors have.

**Description:**  
If ancestor has specific relationship and user tries to add generic one to descendant, reject.

**Example:**
- Existing: `(dog)-[:HAS]->(tail)`, `(boxer)-[:IS_A]->(dog)`, `(tail)-[:IS_A]->(appendage)`
- User tries: `(boxer)-[:HAS]->(appendage)`
- Result: REJECT (ancestor has more specific: tail)

**Cypher Query:**
```cypher
MATCH (x {uuid: $subject_uuid}), (b {uuid: $object_uuid})
WITH x, b
MATCH (x)-[:IS_A*]->(y)-[:HAS]->(a)-[:IS_A*]->(b)
RETURN x, y, a, b
```

**Validation Logic:**
- If query returns data → REJECT with reason "ancestor_has_more_specific"
- Include ancestor name and specific relationship in error

**Acceptance Criteria:**
- ✓ Detects more specific relationships on ancestors
- ✓ Works through multiple IS_A levels
- ✓ Explains which ancestor and which specific relationship
- ✓ Executes in < 150ms

---

#### FR-CVS-007: Replace Descendant Generic with Ancestor Specific
**Priority:** MUST HAVE  
**User Story:** As the system, when a user adds a specific relationship to an ancestor that makes generic descendant relationships wrong, I need to correct this.

**Description:**  
Inverse of FR-CVS-006. If descendant has generic relationship and user adds specific to ancestor, remove generic from descendant(s).

**Example:**
- Existing: `(boxer)-[:HAS]->(appendage)`, `(boxer)-[:IS_A]->(dog)`, `(tail)-[:IS_A]->(appendage)`
- User adds: `(dog)-[:HAS]->(tail)`
- Result: DELETE `(boxer)-[:HAS]->(appendage)`, ADD `(dog)-[:HAS]->(tail)`

**Cypher Query:**
```cypher
MATCH (y {uuid: $subject_uuid}), (a {uuid: $object_uuid})
WITH y, a
MATCH (a)-[:IS_A*]->(b)<-[r:HAS]-(x)-[:IS_A*]->(y)
DELETE r
// Then add new relationship to ancestor
```

**Validation Logic:**
- Find all descendants with generic relationship
- DELETE all generic descendant relationships
- CREATE specific ancestor relationship
- Log all changes in audit log

**Acceptance Criteria:**
- ✓ Finds all descendants with more generic relationship
- ✓ Deletes all in single transaction
- ✓ Transaction rolls back if anything fails
- ✓ Audit log records all deletions and reason
- ✓ Executes in < 200ms

---

#### FR-CVS-008: Prevent Circular IS_A Relationships
**Priority:** MUST HAVE  
**User Story:** As the system, I need to prevent circular taxonomic relationships to maintain ontological integrity.

**Description:**  
Before accepting any IS_A relationship, verify it doesn't create a cycle.

**Cypher Query:**
```cypher
// Check if adding (A)-[:IS_A]->(B) would create cycle
MATCH path=(b {uuid: $object_uuid})-[:IS_A*]->(a {uuid: $subject_uuid})
RETURN path
```

**Validation Logic:**
- If query returns any path → REJECT with reason "circular_inheritance"
- Show the circular path to user

**Acceptance Criteria:**
- ✓ Detects direct cycles (A → B → A)
- ✓ Detects indirect cycles (A → B → C → A)
- ✓ Works with arbitrarily long chains
- ✓ Clear error message showing cycle
- ✓ Executes in < 100ms

---

### 3.4 Context Management Service

#### FR-CMS-001: Create Context Scope
**Priority:** MUST HAVE  
**User Story:** As a calling system, I need to create a context scope so multiple users can share ontological understanding for a specific conversation or decision.

**Description:**  
Create a new context scope with optional participants and lifetime.

**Inputs:**
```json
{
  "context_name": "Patient autonomy discussion - Case #12345",
  "created_by": "user-uuid",
  "participants": ["user-uuid-1", "user-uuid-2"],
  "requesting_system": "synthetic-moral-agent",
  "parent_context_id": "uuid", // optional, for nested contexts
  "expiration_hours": 72 // optional, default 24
}
```

**Processing:**
1. Create context record in database
2. Set expiration timestamp
3. Initialize empty ontology subgraph
4. Grant access to participants
5. Return context details

**Outputs:**
```json
{
  "context_id": "uuid",
  "context_name": "Patient autonomy discussion - Case #12345",
  "scope": "context",
  "created_by": "user-uuid",
  "participants": ["user-uuid-1", "user-uuid-2"],
  "created_at": "2025-12-30T10:00:00Z",
  "expires_at": "2025-01-02T10:00:00Z",
  "term_count": 0,
  "relationship_count": 0
}
```

**Acceptance Criteria:**
- ✓ Creates unique context_id
- ✓ Enforces participant access control
- ✓ Supports nested contexts
- ✓ Automatically expires after set time
- ✓ Sends expiration warnings to participants
- ✓ Allows extension of expiration

---

#### FR-CMS-002: Resolve Scope Hierarchy
**Priority:** MUST HAVE  
**User Story:** As the system, when resolving terms, I need to check scopes in the correct order so the most specific definition is used.

**Description:**  
Implement scope resolution logic: context → user → global.

**Processing:**
1. If `context_id` provided and valid:
   - Check if user is participant
   - Search context scope first
2. Always check user scope for `user_id`
3. Fall back to global scope
4. Return first match with scope metadata

**Acceptance Criteria:**
- ✓ Context scope takes precedence if present
- ✓ User scope overrides global
- ✓ Global is always available as fallback
- ✓ Clear indication of which scope was used
- ✓ Respects access control (users can't see others' user scope)

---

#### FR-CMS-003: List Context Terms
**Priority:** SHOULD HAVE  
**User Story:** As an end user, I want to see what terms have been defined in this context so I know what shared understanding exists.

**Description:**  
List all terms defined in a specific context scope.

**Inputs:**
- `context_id` (UUID): Context to query
- `user_id` (UUID): Requesting user (must be participant)

**Outputs:**
```json
{
  "context_id": "uuid",
  "context_name": "Patient autonomy discussion",
  "terms": [
    {
      "term_uuid": "uuid",
      "term": "autonomy",
      "definition": "...",
      "created_by": "user-uuid-1",
      "created_at": "2025-12-30T10:15:00Z",
      "usage_count": 5
    }
  ],
  "term_count": 1
}
```

**Acceptance Criteria:**
- ✓ Only shows terms in specified context
- ✓ Enforces participant access control
- ✓ Shows who created each term
- ✓ Sortable by creation date, usage count
- ✓ Paginated for large contexts

---

#### FR-CMS-004: Promote Term to Higher Scope
**Priority:** SHOULD HAVE (Phase 2)  
**User Story:** As a curator, when a context/user term proves broadly useful, I want to promote it to a higher scope.

**Description:**  
Promote a term from user → global or context → user/global.

**Inputs:**
```json
{
  "term_uuid": "uuid",
  "current_scope": "user",
  "target_scope": "global",
  "promoted_by": "curator-uuid",
  "justification": "Widely used, well-defined"
}
```

**Processing:**
1. Verify curator permissions
2. Check for conflicts in target scope
3. If conflicts, initiate resolution process
4. Copy term and relationships to target scope
5. Maintain reference to origin
6. Notify original creator

**Acceptance Criteria:**
- ✓ Only curators/admins can promote to global
- ✓ Detects and handles conflicts
- ✓ Maintains provenance trail
- ✓ Original term remains in source scope
- ✓ Audit log created

---

### 3.5 Conflict Detection & Resolution Service

#### FR-CDR-001: Detect Semantic Conflicts
**Priority:** MUST HAVE  
**User Story:** As the system, when a user uses a term inconsistently, I need to detect this and request clarification.

**Description:**  
Monitor for conflicting definitions of the same term across a user's interactions.

**Trigger Conditions:**
- User defines term X differently in two contexts
- User's definition conflicts with global definition they previously accepted
- Within a context, multiple users define same term differently

**Processing:**
1. On term creation/usage, check for existing definitions
2. Compare IS_A chains for compatibility
3. If incompatible (different ancestors that don't converge):
   - Flag as conflict
   - Pause current operation
   - Present conflict to user
4. Log conflict occurrence

**Outputs:**
```json
{
  "conflict_id": "uuid",
  "conflict_type": "incompatible_definitions",
  "term": "autonomy",
  "definitions": [
    {
      "definition_id": "uuid-1",
      "definition": "Autonomy is a capacity...",
      "scope": "user",
      "context": "conversation-xyz",
      "created_at": "2025-12-20T10:00:00Z"
    },
    {
      "definition_id": "uuid-2",
      "definition": "Autonomy is a right...",
      "scope": "context",
      "context": "conversation-abc",
      "created_at": "2025-12-30T10:00:00Z"
    }
  ],
  "message": "You've defined 'autonomy' differently in different contexts. Which definition should we use here?",
  "resolution_options": [
    {
      "action": "use_definition_1",
      "label": "Use 'capacity' definition",
      "description": "Use the definition from conversation-xyz"
    },
    {
      "action": "use_definition_2",
      "label": "Use 'right' definition",
      "description": "Use the current definition"
    },
    {
      "action": "create_distinct",
      "label": "These are different concepts",
      "description": "Create separate terms: 'moral autonomy' and 'political autonomy'"
    },
    {
      "action": "refine",
      "label": "I need to refine my understanding",
      "description": "Start a new negotiation to clarify"
    }
  ]
}
```

**Acceptance Criteria:**
- ✓ Detects incompatible IS_A chains
- ✓ Detects contradictory HAS relationships
- ✓ Presents conflicts clearly with context
- ✓ Offers reasonable resolution options
- ✓ Logs all conflicts for analysis

---

#### FR-CDR-002: Resolve Semantic Conflicts
**Priority:** MUST HAVE  
**User Story:** As an end user, when the system detects I've been inconsistent, I need to resolve this so I can continue.

**Description:**  
Process user's resolution choice and update ontology accordingly.

**Inputs:**
```json
{
  "conflict_id": "uuid",
  "resolution_action": "use_definition_1" | "use_definition_2" | "create_distinct" | "refine",
  "user_id": "uuid",
  "additional_params": {...} // for create_distinct: new term names
}
```

**Processing:**
Based on `resolution_action`:

1. **use_definition_1**: 
   - Use existing definition
   - Update current context to reference it
   - Mark conflict resolved

2. **use_definition_2**:
   - Update previous contexts to use new definition
   - Or: keep previous and use new going forward
   - Mark conflict resolved

3. **create_distinct**:
   - Create two separate terms with user-provided names
   - Update references in each context
   - Create disambiguation note
   - Mark conflict resolved

4. **refine**:
   - Start new negotiation session
   - Pause current operation
   - Allow user to create refined definition

**Acceptance Criteria:**
- ✓ All resolution options work correctly
- ✓ Updates are atomic (transaction)
- ✓ Audit log records resolution
- ✓ Calling system can resume operation
- ✓ User notified of resolution completion

---

### 3.6 Export Service

#### FR-EXP-001: Generate OWL Ontology
**Priority:** MUST HAVE  
**User Story:** As a calling system, I need to export ontologies in OWL format so they can be used in standard ontology tools.

**Description:**  
Generate valid OWL 2 ontology from Fandaws graph for a given term and its relationships.

**Inputs:**
- `term_uuid` (UUID): Root term for export
- `scope` (string): "global" | "user" | "context"
- `scope_id` (UUID): If user/context scope
- `depth` (integer): How many relationship levels to include (default: all)
- `include_bfo` (boolean): Include BFO imports (default: true)

**Processing:**
1. Build ontology graph starting from root term
2. Include:
   - Domain term (root)
   - All ancestors (IS_A chain)
   - All descendants
   - All directly related terms (HAS targets)
   - Direct properties of all included terms
3. Generate OWL XML following specification from Fandaws 2.4
4. Validate against OWL 2 schema
5. Return as XML string

**Output Format:**
```xml
<?xml version="1.0"?>
<rdf:RDF xmlns="http://fandaws.com/ontology/autonomy/uuid.owl#"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:fan="http://fandaws.com/fan/"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:bfo="http://purl.obolibrary.org/obo/bfo.owl#"
     ...>

    <owl:Ontology rdf:about="http://fandaws.com/ontology/autonomy/uuid.owl">
        <owl:imports rdf:resource="http://purl.obolibrary.org/obo/bfo.owl"/>
        <rdfs:comment>Generated by Fandaws 3.0</rdfs:comment>
        ...
    </owl:Ontology>

    <!-- Classes -->
    <owl:Class rdf:about="http://fandaws.com/fan/autonomy/uuid">
        <rdfs:label xml:lang="en">autonomy</rdfs:label>
        <fan:definition xml:lang="en">Autonomy is a capacity that has self-governance.</fan:definition>
        <fan:uuid>uuid</fan:uuid>
        <rdfs:subClassOf rdf:resource="http://fandaws.com/fan/capacity/parent-uuid"/>
        <rdfs:subClassOf>
            <owl:Restriction>
                <owl:onProperty rdf:resource="http://fandaws.com/fan/has"/>
                <owl:someValuesFrom rdf:resource="http://fandaws.com/fan/self-governance/uuid"/>
            </owl:Restriction>
        </rdfs:subClassOf>
    </owl:Class>
    ...
</rdf:RDF>
```

**Acceptance Criteria:**
- ✓ Validates at http://mowl-power.cs.man.ac.uk:8080/validator/
- ✓ Imports successfully into WebProtege
- ✓ Correctly represents multiple HAS relationships (separate Restrictions)
- ✓ URL-encodes special characters in names
- ✓ Includes all required metadata
- ✓ Generates in < 5 seconds for ontologies with 1000+ terms
- ✓ Respects scope boundaries (no leakage)

---

#### FR-EXP-002: Generate JSON-LD
**Priority:** SHOULD HAVE  
**User Story:** As a calling system, I need to export ontologies in JSON-LD so I can easily consume them in my application.

**Description:**  
Export ontology graph as JSON-LD for programmatic consumption.

**Outputs:**
```json
{
  "@context": {
    "@vocab": "http://fandaws.com/fan/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#"
  },
  "@id": "http://fandaws.com/fan/autonomy/uuid",
  "@type": "owl:Class",
  "rdfs:label": "autonomy",
  "fan:definition": "Autonomy is a capacity that has self-governance.",
  "fan:uuid": "uuid",
  "rdfs:subClassOf": {
    "@id": "http://fandaws.com/fan/capacity/parent-uuid"
  },
  "fan:has": [
    {"@id": "http://fandaws.com/fan/self-governance/uuid"}
  ]
}
```

**Acceptance Criteria:**
- ✓ Valid JSON-LD
- ✓ Includes full graph structure
- ✓ Easily parseable by JSON libraries
- ✓ Same scope restrictions as OWL export

---

#### FR-EXP-003: Export Turtle Format
**Priority:** SHOULD HAVE  
**User Story:** As a calling system, I need to export ontologies in Turtle format for compatibility with RDF tools.

**Description:**  
Export as Turtle (TTL) format per website feature description.

**Output Format:**
```turtle
@prefix fan: <http://fandaws.com/fan/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

fan:autonomy_uuid a owl:Class ;
    rdfs:label "autonomy" ;
    fan:definition "Autonomy is a capacity that has self-governance." ;
    fan:uuid "uuid" ;
    rdfs:subClassOf fan:capacity_parentuuid ;
    rdfs:subClassOf [
        a owl:Restriction ;
        owl:onProperty fan:has ;
        owl:someValuesFrom fan:self-governance_uuid
    ] .
```

**Acceptance Criteria:**
- ✓ Valid Turtle syntax
- ✓ Compatible with standard RDF parsers
- ✓ Compact and readable

---

### 3.7 Audit & Provenance Service

#### FR-APS-001: Log All Ontology Changes
**Priority:** MUST HAVE  
**User Story:** As an administrator, I need complete audit logs so I can understand how the ontology evolved.

**Description:**  
Log all create, update, delete operations on terms and relationships.

**Log Entry Format:**
```json
{
  "log_id": "uuid",
  "timestamp": "2025-12-30T10:15:00Z",
  "operation": "create_term" | "update_term" | "delete_term" | "create_relationship" | "delete_relationship",
  "user_id": "uuid",
  "requesting_system": "synthetic-moral-agent",
  "context_id": "uuid",
  "entity_type": "term" | "relationship",
  "entity_id": "uuid",
  "entity_data": {
    "term": "autonomy",
    "before": {...}, // for updates/deletes
    "after": {...}   // for creates/updates
  },
  "reason": "user_negotiation" | "conflict_resolution" | "consistency_check",
  "negotiation_session_id": "uuid", // if applicable
  "conflict_id": "uuid" // if applicable
}
```

**Acceptance Criteria:**
- ✓ Logs created synchronously with operations
- ✓ Immutable (append-only)
- ✓ Queryable by user, term, timerange
- ✓ Retained for minimum 1 year
- ✓ Separate storage from operational DB

---

#### FR-APS-002: Integrate with HIRI
**Priority:** SHOULD HAVE (Phase 2)  
**User Story:** As the system, I need to create HIRI attestations for semantic agreements so they are cryptographically verifiable.

**Description:**  
When negotiation completes, create HIRI attestation of semantic agreement.

**Integration Points:**
1. On negotiation completion → create attestation
2. On conflict resolution → create attestation
3. On term promotion → create attestation

**Attestation Format:**
```json
{
  "type": "semantic_agreement",
  "version": "1.0",
  "content": {
    "term": "autonomy",
    "term_uuid": "uuid",
    "definition": "Autonomy is a capacity...",
    "ontology_graph": {...},
    "scope": "user",
    "scope_id": "user-uuid"
  },
  "participants": [
    {"id": "user-uuid", "role": "definer"},
    {"id": "system-uuid", "role": "validator"}
  ],
  "context": {
    "negotiation_session_id": "uuid",
    "requesting_system": "synthetic-moral-agent",
    "decision_context": "uuid"
  },
  "timestamp": "2025-12-30T10:15:00Z"
}
```

**Acceptance Criteria:**
- ✓ Attestation created atomically with term
- ✓ Includes full ontology graph
- ✓ Cryptographically signed
- ✓ Retrievable via HIRI API
- ✓ Referenced in Fandaws audit log

---

## 4. INTEGRATION REQUIREMENTS

### 4.1 Integration with Synthetic Moral Agent

#### IR-SMA-001: Term Resolution During Decision Making
**Priority:** MUST HAVE  

**Description:**  
When Synthetic Moral Agent encounters unknown terms during ethical evaluation, it must seamlessly integrate Fandaws negotiation into its decision flow.

**Integration Pattern:**
```javascript
// Pseudo-code for integration
class SyntheticMoralAgent {
  async evaluateAction(action, context) {
    // Extract ethical terms from action
    let terms = this.extractEthicalTerms(action);
    
    // Ground each term
    for (let term of terms) {
      let grounding = await fandaws.resolveTerm({
        term: term,
        user_id: context.user_id,
        context_id: context.decision_id,
        requesting_system: "synthetic-moral-agent"
      });
      
      if (grounding.status === "unknown") {
        // Pause decision, initiate negotiation
        await this.pauseDecision(context.decision_id);
        let session = await fandaws.startNegotiation({
          term: term,
          user_id: context.user_id,
          context_id: context.decision_id
        });
        
        // Present negotiation to user
        await this.presentNegotiation(session);
        
        // Wait for completion (webhook or polling)
        await this.waitForNegotiation(session.session_id);
        
        // Resume decision with grounded term
        grounding = await fandaws.resolveTerm({
          term: term,
          user_id: context.user_id,
          context_id: context.decision_id
        });
      }
      
      // Use grounded term in moral reasoning
      this.groundedTerms[term] = grounding;
    }
    
    // Now evaluate with formally grounded terms
    return this.evaluateWithGroundedTerms(action, this.groundedTerms);
  }
}
```

**Acceptance Criteria:**
- ✓ Decision pauses gracefully when negotiation needed
- ✓ User experience is coherent (doesn't feel like two systems)
- ✓ Negotiation state persists across session interruptions
- ✓ Decision resumes automatically when negotiation completes
- ✓ Agent uses grounded terms correctly in reasoning

---

#### IR-SMA-002: Context Sharing for Related Decisions
**Priority:** SHOULD HAVE  

**Description:**  
When multiple moral decisions in same case/conversation, share context scope so semantic agreements persist.

**Requirements:**
- Create context scope at start of case/conversation
- All decisions in case use same context_id
- Terms negotiated once apply to all decisions
- Context expires when case closes

**Acceptance Criteria:**
- ✓ Single negotiation applies to multiple decisions
- ✓ Context lifecycle matches case lifecycle
- ✓ Users can review context terms
- ✓ Context can be extended if needed

---

### 4.2 Integration with ECCPS

#### IR-ECC-001: Ground Claims Before Validation
**Priority:** MUST HAVE  

**Description:**  
Before ECCPS validates epistemic claims, all terms must be ontologically grounded.

**Integration Pattern:**
```javascript
class ECCPS {
  async validateClaim(claim, claimant) {
    // Parse claim to extract terms
    let terms = this.parseClaimTerms(claim);
    
    // Ground each term
    let groundedTerms = {};
    for (let term of terms) {
      let grounding = await fandaws.resolveTerm({
        term: term,
        user_id: claimant.id,
        context_id: claim.context_id,
        requesting_system: "ECCPS",
        usage_example: claim.text
      });
      
      if (grounding.status === "unknown") {
        // Must ground before validating
        return {
          status: "pending_grounding",
          term_needing_grounding: term,
          negotiation_session: await fandaws.startNegotiation({...})
        };
      }
      
      groundedTerms[term] = grounding;
    }
    
    // Now validate claim against grounded ontology
    return this.validateAgainstOntology(claim, groundedTerms);
  }
  
  validateAgainstOntology(claim, groundedTerms) {
    // Check if claim is consistent with ontological structure
    // E.g., "All dogs have consciousness" requires:
    //   - dog IS_A something
    //   - consciousness IS_A something
    //   - Relationship between them is ontologically valid
  }
}
```

**Acceptance Criteria:**
- ✓ Claims cannot be validated until terms grounded
- ✓ Validation uses formal ontological relationships
- ✓ Detects claims that contradict ontology
- ✓ Explains validation failures in terms of ontology

---

#### IR-ECC-002: Detect Ontological Contradictions in Claims
**Priority:** MUST HAVE  

**Description:**  
ECCPS uses Fandaws ontology to detect when claims contain ontological contradictions.

**Example Contradictions:**
- "This dog is a cat" (violates IS_A taxonomy)
- "This autonomy lacks self-governance" (contradicts HAS relationship)
- "All X are Y" when ontology shows X NOT_IS_A Y

**Requirements:**
- ECCPS queries Fandaws for term relationships
- Compares claim structure to ontological structure
- Flags contradictions with explanation

**Acceptance Criteria:**
- ✓ Detects IS_A contradictions
- ✓ Detects HAS contradictions
- ✓ Explains why claim contradicts ontology
- ✓ Suggests corrections based on ontology

---

### 4.3 Integration with ARCHON

#### IR-ARC-001: Ground Governance Policy Terms
**Priority:** MUST HAVE  

**Description:**  
ARCHON governance policies contain critical terms that need precise grounding.

**Example Terms:**
- "safety", "autonomy", "dignity", "rights", "harm"
- "transparency", "accountability", "oversight"

**Integration Pattern:**
```javascript
class ARCHON {
  async evaluatePolicy(policy, stakeholders) {
    // Extract terms from policy
    let terms = this.extractPolicyTerms(policy);
    
    // For each stakeholder, ground terms
    let stakeholderGroundings = {};
    for (let stakeholder of stakeholders) {
      stakeholderGroundings[stakeholder.id] = {};
      for (let term of terms) {
        let grounding = await fandaws.resolveTerm({
          term: term,
          user_id: stakeholder.id,
          context_id: policy.id,
          requesting_system: "ARCHON"
        });
        stakeholderGroundings[stakeholder.id][term] = grounding;
      }
    }
    
    // Detect definitional conflicts across stakeholders
    let conflicts = await this.detectStakeholderConflicts(
      terms, 
      stakeholderGroundings
    );
    
    if (conflicts.length > 0) {
      // Facilitate negotiation for shared understanding
      return this.facilitateSemanticNegotiation(conflicts);
    }
    
    // Evaluate policy with shared grounded terms
    return this.evaluatePolicyWithGrounding(policy, stakeholderGroundings);
  }
}
```

**Acceptance Criteria:**
- ✓ Detects when stakeholders define terms differently
- ✓ Facilitates negotiation to shared understanding
- ✓ Makes definitional pluralism explicit when resolution impossible
- ✓ Policy evaluation considers semantic agreements

---

#### IR-ARC-002: Track Semantic Evolution in Governance
**Priority:** SHOULD HAVE (Phase 2)  

**Description:**  
As governance policies evolve, track how key terms are defined over time.

**Requirements:**
- Version control for policy-related terms
- Audit trail of semantic changes
- Impact analysis when definitions change
- Notification to affected systems

**Acceptance Criteria:**
- ✓ Term definitions versioned with timestamps
- ✓ Policy versions linked to term versions
- ✓ Changes trigger impact analysis
- ✓ Stakeholders notified of semantic changes

---

### 4.4 Integration with HIRI

#### IR-HIR-001: Create Attestations for Semantic Agreements
**Priority:** SHOULD HAVE (Phase 2)  

**Covered in FR-APS-002**

---

#### IR-HIR-002: Verify Semantic Agreement Provenance
**Priority:** SHOULD HAVE (Phase 2)  

**Description:**  
Allow systems to verify that a semantic agreement was properly negotiated and recorded.

**Integration Pattern:**
```javascript
// System wants to verify that a term definition is legitimate
let verification = await hiri.verifyAttestation(attestation_id);

if (verification.valid) {
  // Attestation is cryptographically valid
  // Check if it matches current Fandaws definition
  let currentDef = await fandaws.resolveTerm({
    term_uuid: verification.content.term_uuid
  });
  
  if (currentDef.definition === verification.content.definition) {
    // Definition unchanged since attestation
    return "verified_unchanged";
  } else {
    // Definition has evolved
    return "verified_but_updated";
  }
}
```

**Acceptance Criteria:**
- ✓ Attestations cryptographically verifiable
- ✓ Can detect if definition changed since attestation
- ✓ Provides full negotiation provenance
- ✓ Links to audit logs

---

## 5. DATA REQUIREMENTS

### 5.1 Neo4j Graph Schema

#### Node Types

**Term Node:**
```javascript
{
  // Core properties
  uuid: String (unique, indexed),
  name: String (indexed),
  normalized_name: String (indexed),
  definition: String,
  
  // Scope properties
  scope: String ["global", "user", "context"],
  scope_id: String (indexed), // user_id or context_id
  
  // Metadata
  created_by: String (user_id),
  created_at: Timestamp,
  updated_at: Timestamp,
  
  // Verification
  verified: Boolean,
  verification_count: Integer,
  verification_users: [String], // user_ids who verified
  
  // BFO mapping
  bfo_class: String, // e.g., "BFO_0000017" for quality
  
  // Usage tracking
  usage_count: Integer,
  last_used_at: Timestamp,
  
  // Labels
  labels: [String] // for categorization
}
```

**Indexes:**
```cypher
CREATE INDEX term_uuid FOR (t:Term) ON (t.uuid);
CREATE INDEX term_name_scope FOR (t:Term) ON (t.normalized_name, t.scope, t.scope_id);
CREATE INDEX term_scope FOR (t:Term) ON (t.scope, t.scope_id);
CREATE INDEX term_bfo FOR (t:Term) ON (t.bfo_class);
```

#### Relationship Types

**IS_A Relationship:**
```javascript
{
  uuid: String (unique),
  type: "IS_A",
  
  // Scope
  scope: String,
  scope_id: String,
  
  // Provenance
  created_by: String,
  created_at: Timestamp,
  negotiation_session_id: String,
  
  // Validation
  validated: Boolean,
  validation_checks_passed: [String]
}
```

**HAS Relationship:**
```javascript
{
  uuid: String (unique),
  type: "HAS",
  
  // Scope
  scope: String,
  scope_id: String,
  
  // Provenance
  created_by: String,
  created_at: Timestamp,
  negotiation_session_id: String,
  
  // Semantics
  relationship_subtype: String, // "has_part", "has_quality", etc.
  
  // Validation
  validated: Boolean,
  validation_checks_passed: [String]
}
```

**CONTRADICTS Relationship:**
```javascript
{
  uuid: String (unique),
  type: "CONTRADICTS",
  reason: String,
  detected_at: Timestamp,
  resolved: Boolean,
  resolution: String
}
```

#### Constraints

```cypher
// Ensure no duplicate terms in same scope
CREATE CONSTRAINT unique_term_in_scope 
FOR (t:Term) 
REQUIRE (t.normalized_name, t.scope, t.scope_id) IS NODE KEY;

// Ensure UUIDs are unique
CREATE CONSTRAINT unique_uuid 
FOR (t:Term) 
REQUIRE t.uuid IS UNIQUE;

// Prevent orphaned terms (except root "entity")
// This is enforced at application level, not database level
```

---

### 5.2 PostgreSQL Schema

#### Users Table
```sql
CREATE TABLE users (
  user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  external_id VARCHAR(255) UNIQUE NOT NULL, -- from auth system
  username VARCHAR(100),
  email VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_active_at TIMESTAMP,
  preferences JSONB, -- user preferences for negotiations
  role VARCHAR(50) DEFAULT 'user', -- 'user', 'curator', 'admin'
  
  INDEX idx_external_id (external_id),
  INDEX idx_email (email)
);
```

#### Contexts Table
```sql
CREATE TABLE contexts (
  context_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  context_name VARCHAR(255),
  created_by UUID REFERENCES users(user_id),
  requesting_system VARCHAR(100),
  parent_context_id UUID REFERENCES contexts(context_id),
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP,
  closed_at TIMESTAMP,
  
  status VARCHAR(50) DEFAULT 'active', -- 'active', 'expired', 'closed'
  
  metadata JSONB, -- flexible storage for system-specific data
  
  INDEX idx_created_by (created_by),
  INDEX idx_status (status),
  INDEX idx_expires_at (expires_at)
);
```

#### Context Participants Table
```sql
CREATE TABLE context_participants (
  context_id UUID REFERENCES contexts(context_id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(user_id),
  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  role VARCHAR(50) DEFAULT 'participant', -- 'participant', 'moderator'
  
  PRIMARY KEY (context_id, user_id),
  INDEX idx_user_contexts (user_id, context_id)
);
```

#### Negotiation Sessions Table
```sql
CREATE TABLE negotiation_sessions (
  session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  term VARCHAR(255) NOT NULL,
  normalized_term VARCHAR(255) NOT NULL,
  
  user_id UUID REFERENCES users(user_id),
  context_id UUID REFERENCES contexts(context_id),
  requesting_system VARCHAR(100),
  parent_session_id UUID REFERENCES negotiation_sessions(session_id), -- for nested
  
  state VARCHAR(50) DEFAULT 'negotiating', 
  -- 'negotiating', 'negotiating_nested', 'conflict', 'paused', 'complete', 'abandoned'
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP,
  
  discovered_term_uuid UUID, -- reference to Neo4j term
  
  current_phase VARCHAR(50), -- 'is_a', 'has', 'complete'
  current_question TEXT,
  
  metadata JSONB, -- dialogue history, discovered relationships
  
  INDEX idx_user_state (user_id, state),
  INDEX idx_term (normalized_term),
  INDEX idx_context (context_id)
);
```

#### Dialogue History Table
```sql
CREATE TABLE dialogue_history (
  dialogue_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID REFERENCES negotiation_sessions(session_id) ON DELETE CASCADE,
  
  turn_number INTEGER NOT NULL,
  speaker VARCHAR(50) NOT NULL, -- 'system', 'user'
  message TEXT NOT NULL,
  message_type VARCHAR(50), -- 'question', 'response', 'validation', 'error'
  
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  metadata JSONB, -- parsed entities, validation results, etc.
  
  INDEX idx_session (session_id, turn_number)
);
```

#### Conflicts Table
```sql
CREATE TABLE conflicts (
  conflict_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conflict_type VARCHAR(100) NOT NULL,
  
  term VARCHAR(255),
  user_id UUID REFERENCES users(user_id),
  
  definitions JSONB NOT NULL, -- array of conflicting definitions
  
  detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  resolved_at TIMESTAMP,
  
  resolution_action VARCHAR(100),
  resolution_metadata JSONB,
  
  resolved_by UUID REFERENCES users(user_id),
  
  INDEX idx_user_unresolved (user_id, resolved_at) WHERE resolved_at IS NULL,
  INDEX idx_term (term),
  INDEX idx_detected_at (detected_at)
);
```

#### Audit Log Table
```sql
CREATE TABLE audit_log (
  log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  
  operation VARCHAR(100) NOT NULL,
  entity_type VARCHAR(50) NOT NULL, -- 'term', 'relationship', 'context', etc.
  entity_id UUID, -- reference to relevant entity
  
  user_id UUID REFERENCES users(user_id),
  requesting_system VARCHAR(100),
  context_id UUID REFERENCES contexts(context_id),
  
  entity_data JSONB NOT NULL, -- before/after state
  
  reason VARCHAR(255),
  negotiation_session_id UUID REFERENCES negotiation_sessions(session_id),
  conflict_id UUID REFERENCES conflicts(conflict_id),
  
  -- Partitioned by month for performance
  INDEX idx_timestamp (timestamp),
  INDEX idx_user (user_id, timestamp),
  INDEX idx_entity (entity_type, entity_id),
  INDEX idx_operation (operation, timestamp)
) PARTITION BY RANGE (timestamp);
```

#### System Configuration Table
```sql
CREATE TABLE system_config (
  config_key VARCHAR(100) PRIMARY KEY,
  config_value JSONB NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by UUID REFERENCES users(user_id)
);

-- Example configurations
INSERT INTO system_config VALUES
  ('consistency_checks_enabled', '{"checks": ["all"]}'),
  ('negotiation_max_depth', '10'),
  ('context_default_expiration_hours', '24'),
  ('cache_ttl_seconds', '3600');
```

---

### 5.3 Redis Cache Schema

#### Cache Keys

**Term Resolution Cache:**
```
Key: "term:{scope}:{scope_id}:{normalized_term}"
Value: JSON string of resolved term
TTL: 3600 seconds (1 hour) for user/context, 86400 (24h) for global
```

**Active Session Cache:**
```
Key: "session:{session_id}"
Value: JSON string of session state
TTL: 3600 seconds (renewed on each interaction)
```

**User Rate Limit:**
```
Key: "ratelimit:user:{user_id}:{endpoint}"
Value: Request count
TTL: 60 seconds (sliding window)
```

**System Rate Limit:**
```
Key: "ratelimit:system:{system_id}:{endpoint}"
Value: Request count
TTL: 60 seconds
```

---

## 6. USER INTERFACE REQUIREMENTS

### 6.1 Negotiation UI Components

While Fandaws 3.0 is primarily an API service, it needs UI components that calling systems can embed.

#### UIR-001: Term Clarification Modal
**Priority:** MUST HAVE  

**Description:**  
Embeddable React component for conducting term negotiations.

**Props:**
```typescript
interface TermClarificationModalProps {
  session_id: string;
  onComplete: (term_uuid: string, definition: string) => void;
  onCancel: () => void;
  onPause: () => void;
  theme?: 'light' | 'dark';
  customStyles?: CSSProperties;
}
```

**Features:**
- Displays current question
- Accepts text input
- Shows progress indicator
- Handles nested negotiations
- Shows validation errors
- Presents conflicts

**Acceptance Criteria:**
- ✓ Responsive design (mobile, tablet, desktop)
- ✓ Accessible (WCAG 2.1 AA)
- ✓ Supports keyboard navigation
- ✓ Localized (en, es, fr minimum)
- ✓ Graceful error handling
- ✓ Can be styled to match host application

---

#### UIR-002: Conflict Resolution Component
**Priority:** MUST HAVE  

**Description:**  
Component for presenting and resolving semantic conflicts.

**Props:**
```typescript
interface ConflictResolutionProps {
  conflict_id: string;
  onResolve: (resolution: Resolution) => void;
  onDismiss: () => void;
}
```

**Features:**
- Shows conflicting definitions side-by-side
- Provides context for each definition
- Clear action buttons for resolution
- Visual distinction between options

**Acceptance Criteria:**
- ✓ Clearly presents both definitions
- ✓ Shows when/where each was used
- ✓ All resolution options accessible
- ✓ Confirmation before destructive actions
- ✓ Responsive and accessible

---

#### UIR-003: Context Term Viewer
**Priority:** SHOULD HAVE  

**Description:**  
Component for viewing all terms defined in a context.

**Props:**
```typescript
interface ContextTermViewerProps {
  context_id: string;
  user_id: string;
  onSelectTerm: (term_uuid: string) => void;
}
```

**Features:**
- List view of all terms
- Search/filter capability
- Sort by name, date, usage
- Shows who defined each term
- Click to see full definition

**Acceptance Criteria:**
- ✓ Loads large term lists efficiently
- ✓ Search works in real-time
- ✓ Pagination or virtual scrolling
- ✓ Responsive design

---

### 6.2 Administrative Interface

#### UIR-004: Admin Dashboard
**Priority:** SHOULD HAVE (Phase 2)  

**Description:**  
Web-based admin interface for system management.

**Features:**
- System health monitoring
- User management
- Global ontology curation
- Conflict review queue
- Audit log viewer
- Configuration management

**Acceptance Criteria:**
- ✓ Role-based access control
- ✓ Real-time metrics
- ✓ Export capabilities
- ✓ Bulk operations

---

## 7. NON-FUNCTIONAL REQUIREMENTS

### 7.1 Performance

#### NFR-PERF-001: API Response Time
- Term resolution (cached): < 50ms (p95)
- Term resolution (uncached): < 500ms (p95)
- Negotiation step: < 300ms (p95)
- Consistency validation: < 100ms per check (p95)
- OWL export (1000 terms): < 5 seconds

#### NFR-PERF-002: Throughput
- Support 1000 requests/second across all endpoints
- Support 100 concurrent negotiations
- Handle 10,000 terms per user scope
- Handle 1,000,000 terms in global scope

#### NFR-PERF-003: Database Performance
- Neo4j queries: < 100ms for simple traversals
- Neo4j queries: < 500ms for complex consistency checks
- PostgreSQL queries: < 50ms for session/user lookups
- Redis cache hit rate: > 80% for frequent terms

---

### 7.2 Scalability

#### NFR-SCAL-001: Horizontal Scaling
- API servers: stateless, can scale horizontally
- Support load balancing across multiple instances
- Session state in Redis allows any server to handle requests

#### NFR-SCAL-002: Database Scaling
- Neo4j: support sharding by scope (global, users, contexts)
- PostgreSQL: support read replicas
- Redis: support clustering

#### NFR-SCAL-003: Growth Capacity
- Support 100,000 active users
- Support 10,000 concurrent sessions
- Support 1M terms in global ontology
- Support 100M term relationships

---

### 7.3 Reliability

#### NFR-REL-001: Availability
- API availability: 99.9% uptime (excluding planned maintenance)
- Maximum planned downtime: 4 hours/month
- Graceful degradation when services unavailable

#### NFR-REL-002: Data Durability
- No data loss for committed transactions
- Daily backups of all databases
- Point-in-time recovery capability (7 days)
- Geographic redundancy for production

#### NFR-REL-003: Error Handling
- All errors logged with context
- User-friendly error messages
- Automatic retry for transient failures
- Circuit breakers for downstream services

---

### 7.4 Security

#### NFR-SEC-001: Authentication & Authorization
- OAuth 2.0 / OpenID Connect support
- JWT token-based authentication
- Role-based access control (User, Curator, Admin)
- Scope-based access control (users can't access others' private ontologies)

#### NFR-SEC-002: Data Protection
- Encryption at rest for databases
- Encryption in transit (TLS 1.3)
- PII/sensitive data encrypted
- Secure key management (HSM or cloud KMS)

#### NFR-SEC-003: API Security
- Rate limiting per user and system
- Input validation on all endpoints
- SQL/Cypher injection prevention
- XSS prevention in responses

#### NFR-SEC-004: Audit & Compliance
- Complete audit trail for all operations
- Immutable audit logs
- GDPR compliance (right to deletion, data portability)
- SOC 2 Type II ready

---

### 7.5 Maintainability

#### NFR-MAIN-001: Code Quality
- Test coverage > 80%
- Unit tests for all business logic
- Integration tests for API endpoints
- End-to-end tests for critical flows

#### NFR-MAIN-002: Documentation
- API documentation (OpenAPI/Swagger)
- Architecture documentation
- Deployment documentation
- Runbooks for common operations

#### NFR-MAIN-003: Monitoring & Observability
- Structured logging (JSON format)
- Distributed tracing (OpenTelemetry)
- Metrics (Prometheus format)
- Alerting for critical errors

#### NFR-MAIN-004: Deployment
- Infrastructure as Code (Terraform/CloudFormation)
- CI/CD pipeline (automated testing, deployment)
- Blue-green or canary deployments
- Automated rollback on failure

---

### 7.6 Usability

#### NFR-USE-001: Developer Experience
- Clear, consistent API design
- Comprehensive SDK/client libraries (JavaScript, Python)
- Interactive API documentation
- Example integrations for each calling system

#### NFR-USE-002: End User Experience
- Negotiation completes in < 3 minutes (average)
- Clear, jargon-free language in questions
- Helpful examples and guidance
- Progress indicators throughout negotiation

#### NFR-USE-003: Accessibility
- WCAG 2.1 AA compliance for all UI components
- Keyboard navigation support
- Screen reader compatibility
- Internationalization (i18n) ready

---

## 8. ACCEPTANCE CRITERIA

### 8.1 MVP Acceptance (Phase 1)

The system is ready for initial deployment when:

**Core Functionality:**
- ✓ FR-TRS-001: Term resolution works through scope hierarchy
- ✓ FR-SNS-001: Can initiate negotiation sessions
- ✓ FR-SNS-002: IS_A phase negotiation works
- ✓ FR-SNS-003: HAS phase negotiation works
- ✓ FR-SNS-004: Can complete negotiations and commit terms
- ✓ FR-CVS-001 through FR-CVS-008: All consistency checks implemented
- ✓ FR-EXP-001: Can export valid OWL ontologies

**Integration:**
- ✓ IR-SMA-001: Synthetic Moral Agent integration working
- ✓ API documented with examples
- ✓ SDK available for JavaScript

**Non-Functional:**
- ✓ NFR-PERF-001: Performance targets met
- ✓ NFR-REL-001: 99% availability in staging
- ✓ NFR-SEC-001: Authentication working
- ✓ Test coverage > 70%

**Demo Scenarios:**
- ✓ Can negotiate "autonomy" from scratch
- ✓ Can detect and prevent duplicate relationships
- ✓ Can export ontology and import into WebProtege
- ✓ Synthetic Moral Agent can use for real decision

---

### 8.2 Phase 2 Acceptance

Phase 2 is complete when:

**Additional Features:**
- ✓ FR-CDR-001: Conflict detection working
- ✓ FR-CDR-002: Conflict resolution working
- ✓ FR-CMS-003: Context term viewer available
- ✓ FR-CMS-004: Term promotion implemented
- ✓ IR-ECC-001: ECCPS integration working
- ✓ IR-ARC-001: ARCHON integration working
- ✓ IR-HIR-001: HIRI attestations created

**UI Components:**
- ✓ UIR-001: Term clarification modal polished
- ✓ UIR-002: Conflict resolution component working
- ✓ UIR-003: Context term viewer implemented

**Performance:**
- ✓ NFR-PERF-002: Throughput targets met
- ✓ Test coverage > 80%

---

## 9. APPENDICES

### Appendix A: API Quick Reference

See Section 3 for detailed requirements. Summary:

**Term Resolution:**
- `POST /api/v3/term/resolve` - Resolve term
- `GET /api/v3/term/{uuid}` - Get term details

**Negotiation:**
- `POST /api/v3/negotiate/start` - Start session
- `POST /api/v3/negotiate/continue` - Continue session
- `POST /api/v3/negotiate/complete` - Complete session
- `POST /api/v3/negotiate/pause` - Pause session
- `GET /api/v3/negotiate/{session_id}` - Get session state

**Validation:**
- `POST /api/v3/validate/relationship` - Validate relationship
- `POST /api/v3/validate/term` - Validate term

**Context Management:**
- `POST /api/v3/context/create` - Create context
- `GET /api/v3/context/{context_id}` - Get context
- `GET /api/v3/context/{context_id}/terms` - List context terms
- `DELETE /api/v3/context/{context_id}` - Close context

**Conflict Management:**
- `POST /api/v3/conflict/detect` - Detect conflicts
- `POST /api/v3/conflict/{conflict_id}/resolve` - Resolve conflict
- `GET /api/v3/conflict/user/{user_id}` - List user conflicts

**Export:**
- `GET /api/v3/export/ontology/{term_uuid}?format=owl|jsonld|turtle` - Export ontology

**Admin:**
- `GET /api/v3/admin/stats` - System statistics
- `GET /api/v3/admin/audit` - Audit logs

---

### Appendix B: Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| ERR_AUTH_001 | Invalid or expired token | 401 |
| ERR_AUTH_002 | Insufficient permissions | 403 |
| ERR_VAL_001 | Invalid request format | 400 |
| ERR_VAL_002 | Missing required parameter | 400 |
| ERR_VAL_003 | Invalid UUID format | 400 |
| ERR_TERM_001 | Term not found | 404 |
| ERR_TERM_002 | Duplicate term | 409 |
| ERR_REL_001 | Invalid relationship | 400 |
| ERR_REL_002 | Consistency check failed | 422 |
| ERR_REL_003 | Circular reference detected | 422 |
| ERR_CTX_001 | Context not found | 404 |
| ERR_CTX_002 | Not a context participant | 403 |
| ERR_CTX_003 | Context expired | 410 |
| ERR_SES_001 | Session not found | 404 |
| ERR_SES_002 | Session expired | 410 |
| ERR_SES_003 | Max nested depth reached | 422 |
| ERR_SYS_001 | Database error | 500 |
| ERR_SYS_002 | Service unavailable | 503 |

---

### Appendix C: Glossary

See Section 1.3 for core definitions. Additional terms:

| Term | Definition |
|------|------------|
| **Calling System** | External system that consumes Fandaws API (ARCHON, Synthetic Moral Agent, ECCPS) |
| **Curator** | User with permissions to manage global ontology |
| **Grounded Term** | Term with complete formal ontological definition (IS_A chain and HAS relationships) |
| **Nested Negotiation** | When defining a term requires first defining its parent or properties |
| **Scope Hierarchy** | Order of precedence: context → user → global |
| **Semantic Agreement** | Completed negotiation resulting in shared understanding of term |
| **Session** | Stateful negotiation dialogue to ground a term |
| **Validation Check** | Rule preventing ontological inconsistency |

---

### Appendix D: Future Enhancements (Post Phase 2)

**Intelligence Layer:**
- LLM-assisted term extraction from natural language
- Automatic relationship inference from usage patterns
- Suggested definitions based on corpus analysis
- Semantic similarity detection

**Collaboration Features:**
- Real-time multi-user negotiation
- Discussion threads on definitions
- Voting/consensus mechanisms
- Ontology diff/merge tools

**Advanced Reasoning:**
- Ontology-based inference
- Contradiction detection beyond direct relationships
- Support for probabilistic relationships
- Temporal ontologies (things that change over time)

**Integration Enhancements:**
- GraphQL API
- WebSocket support for real-time updates
- Batch operations API
- Import from existing ontologies (OWL, OBO, etc.)