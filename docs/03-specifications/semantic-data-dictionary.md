# **Formalizing Semantic Data Dictionaries for Realist Star Schemas: Version 2.0**

**Aaron Damiano**
*Fandaws Ontology Service*
*January 2026*

---

## **Abstract**

Conventional star and snowflake schemas in data warehousing efficiently support analytics but collapse rich semantic distinctions into relational joins. This often obscures the difference between **reality**, **information artifacts**, and **assertion events**, limiting explainability, auditability, and semantic precision.

We present **Semantic Data Dictionary Version 2.0 (SDD v2.0)**, a machine-readable artifact that explicitly maps relational tables and columns to a **realism-based ontological model** (BFO/CCO/IAO). SDD v2.0 introduces **temporal precision**, **null semantics**, and **invertible relations**, enabling conventional data warehouses to reconstruct a **realist middle layer** without restructuring the database.

Using a **Person–House–Residency** example, we demonstrate how the SDD preserves ontological rigor while remaining operationally viable and explainable.

---

## **1. Introduction**

Data warehouses are designed for **efficiency**, not ontological fidelity. Standard patterns treat fact tables as atomic truths and foreign keys as relationships, resulting in semantic shortcuts like:

```
Person -> livesAt -> House
```

These shortcuts:

1. Collapse the distinction between **real entities**, **information about entities**, and **assertions about entities**.
2. Fail to capture provenance, temporal boundaries, or epistemic status.
3. Obscure the difference between **unknown** and **nonexistent** values.

**Semantic Data Dictionaries (SDDs)** address this gap by defining a **formal, machine-readable contract** between relational data and an ontologically sound model.

---

## **2. Ontological Foundation**

### 2.1 Realism Principles

The SDD aligns with **Basic Formal Ontology (BFO)** and **Common Core Ontologies (CCO)**:

* **Independent Continuants (ICs)**: Entities persisting through time (e.g., `Person`, `House`)
* **Realizable Dependent Continuants (RDCs)**: Roles, dispositions, or qualities that depend on ICs (e.g., `ResidentRole`)
* **Processes (Occurrents)**: Temporal events or activities (e.g., `ActOfOccupancy`)
* **Information Content Entities (ICE)**: Conceptual artifacts conveying information (e.g., `PersonName`)
* **Information Bearing Entities (IBE)**: Records or documents concretizing ICEs (e.g., `PersonNameRecord`)

### 2.2 Assertion Events

Fact tables are **not direct statements of truth**; they are **assertion events**, representing **someone asserting a claim**. This ensures that:

* Unknown data does not imply negative existence.
* Temporal and provenance metadata are preserved.
* Downstream projections (RDF, APIs) remain semantically honest.

---

## **3. Semantic Data Dictionary Version 2.0**

### 3.1 Structure

SDD v2.0 is a JSON artifact defining:

1. **Tables → Ontological Classes**
2. **Columns → ICE, IBE, or attributes**
3. **Foreign keys → Semantic relations**
4. **Null semantics → Absence of assertion**
5. **Inverse relations → Facilitates query from multiple perspectives**
6. **Temporal precision → Start/end instants vs. intervals**

---

### 3.2 Global Assumptions

```json
{
  "rows_are_facts": false,
  "rows_are_assertions": true,
  "foreign_keys_are_semantically_typed": true,
  "literals_do_not_inhere_in_entities": true
}
```

#### **Null Semantics**

```json
"null_semantics": {
  "on_missing_fk": "iao:information_gap",
  "interpretation": "absence_of_assertion",
  "is_disjoint_with_nonexistence": true
}
```

**Interpretation:** Missing foreign keys signal **unknown information**, not **nonexistence**, preventing accidental negative assertions.

---

### 3.3 Person Dimension

```json
"person_dim": {
  "maps_to_class": "cco:Person",
  "ontological_type": "bfo:IndependentContinuant",
  "columns": {
    "person_id": { "role": "identifier" },
    "name_text": {
      "semantic_pattern": "Designation",
      "ice_class": "cco:PersonName",
      "ibe_class": "cco:PersonNameRecord",
      "about": "cco:Person",
      "literal_property": "has_text_value",
      "datatype": "xsd:string"
    }
  }
}
```

**Explanation:**

* `name_text` is **not a property of the person**, but a concretization of an ICE (PersonName) borne by an IBE (PersonNameRecord).
* Preserves ontological separation between **real entity** and **information artifact**.

---

### 3.4 Time Dimension

```json
"time_dim": {
  "maps_to_class": "bfo:TemporalInstant",
  "ontological_type": "bfo:TemporalRegion",
  "temporal_precision": {
    "is_interval": false,
    "is_instant": true,
    "boundary_of": "bfo:Occurrent"
  },
  "columns": {
    "time_id": { "role": "identifier" },
    "timestamp": { "datatype": "xsd:dateTime" }
  }
}
```

**Explanation:**

* Provides **instants** that bound a process.
* Enables derivation of **temporal intervals** without asserting completion.

---

### 3.5 Fact Table: Residency

```json
"residency_fact": {
  "maps_to_class": "cco:ActOfOccupancy",
  "ontological_type": "bfo:Process",
  "epistemic_role": "AssertionEvent",
  "columns": {
    "person_id": {
      "foreign_key_to": "person_dim.person_id",
      "relation": {
        "type": "participates_as",
        "inverse_type": "is_realized_by",
        "role_class": "cco:ResidentRole",
        "target_class": "cco:Person"
      }
    },
    "house_id": {
      "foreign_key_to": "house_dim.house_id",
      "relation": {
        "type": "has_site",
        "inverse_type": "is_site_of",
        "target_class": "cco:House"
      }
    },
    "start_date_id": {
      "foreign_key_to": "time_dim.time_id",
      "relation": {
        "type": "bfo:occupies_temporal_region",
        "boundary_type": "bfo:start_instant"
      }
    }
  }
}
```

**Notes:**

* Each row is an **assertion event** that person participates in a residency process.
* Inverse relations allow querying **House → Occupancy → Person**.
* Temporal instants define start; absence of end instant is **neutral** (open-world).

---

### 3.6 Role Definitions

```json
"cco:ResidentRole": {
  "ontological_type": "bfo:RealizableDependentContinuant",
  "inheres_in": "cco:Person",
  "realized_by": "cco:ActOfOccupancy",
  "behavior_on_null_assertion": "role_remains_latent"
}
```

**Explanation:**

* Role exists independently of assertion.
* Null facts do not erase the potential for role realization.

---

## **4. Examples**

### 4.1 Person Example

| Column    | Value           |
| --------- | --------------- |
| person_id | 1               |
| name_text | "Aaron Damiano" |

**Ontological Mapping:**

```text
Person_1 (IC)
  has ICE: PersonName
    concretized by IBE: PersonNameRecord
      has_text_value "Aaron Damiano"
```

---

### 4.2 Occupancy Example

| Column        | Value            |
| ------------- | ---------------- |
| person_id     | 1                |
| house_id      | 100              |
| start_date_id | 2026-01-01T10:09 |

**Ontological Mapping:**

```text
ActOfOccupancy_1 (Process)
  realizes ResidentRole_1
    inheres_in Person_1
  has_site House_100
  occupies_temporal_region TemporalInterval_1
    bounded_by start: 2026-01-01T10:09
```

* Inverse relations allow queries from **House → Residents**.
* Null end_date = open-world, neutral.

---

## **5. Benefits**

1. **Semantic Honesty:** Distinguishes reality, assertion, and information.
2. **Auditability:** Every fact is traceable to an assertion event.
3. **Temporal Precision:** Supports time-based reasoning without assuming complete intervals.
4. **Null Semantics:** Explicitly encodes absence of information without asserting negative facts.
5. **Invertibility:** Queries and projections can traverse forwards or backwards along semantic relations.
6. **Operational Feasibility:** Compatible with existing star/snowflake schemas; no restructuring needed.

---

## **6. Evaluation Criteria**

Reviewers should consider:

1. **Ontological Soundness** (ICs, RDCs, processes, ICE/IBE)
2. **Architectural Plausibility** (warehouse-friendly, ETL-compatible)
3. **Invertibility & Traceability** (can we reconstruct the realist model?)
4. **Null and Edge Cases** (absence vs. negative assertions)
5. **Temporal Reasoning** (instant vs. interval correctness)
6. **Projection Capability** (RDF, APIs, SHML reconstruction)

---

## **7. Conclusion**

SDD v2.0 demonstrates that **semantic rigor and operational pragmatism can coexist**.
By formalizing the **ontological meaning of tables, columns, and relations**, it allows **existing star schemas** to be interpreted in a **realist middle layer** without altering the database.

This enables:

* belief-scoped reasoning
* counterfactual projections
* audit trails and explanations
* clear separation between reality, information artifacts, and assertions

Version 2.0 is now a **review-ready artifact** that bridges **ontology theory** and **practical information engineering**.
