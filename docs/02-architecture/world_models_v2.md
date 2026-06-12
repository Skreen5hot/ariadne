# World Models as Semantic Infrastructure: A Realist Framework for Accountable AI Systems

**Author:** Aaron Damiano  
**Affiliation:** Fandaws Ontology Service  
**Date:** January 2026  
**Version:** 2.0

---

## Abstract

Contemporary AI research treats world models as internal cognitive achievements—neural representations that individual systems develop through training. We argue this framing imports assumptions from human psychology that, while potentially useful as research heuristics, create accountability gaps when applied to deployed AI systems. We propose an alternative: world models as *semantic infrastructure*—shared, governed, auditable representational systems in which both human and artificial agents participate. Drawing on ontological realism and Basic Formal Ontology (BFO), we present the Semantically Honest Middle Layer (SHML), a three-tier architecture that explicitly models the interpretive processes generating assertions, preserves provenance and uncertainty, and maintains multiple competing hypotheses without premature commitment. This approach shifts the locus of AI alignment from "making models think correctly" to "building infrastructure that supports accountable participation"—a more tractable problem with clearer governance mechanisms. We provide formal specifications, compare our approach with existing knowledge representation frameworks, address key objections, and outline an evaluation roadmap for empirical validation.

**Keywords:** World models, semantic infrastructure, ontological realism, AI accountability, knowledge representation, formal ontology

---

## 1. Introduction

The question "Does this AI system have a world model?" has become central to contemporary AI research (Ha & Schmidhuber, 2018; Hafner et al., 2023; LeCun, 2022). Recent work demonstrates that neural networks can develop internal structures corresponding to spatial, logical, and relational regularities (Li et al., 2023; Nanda et al., 2023). These findings are significant—they show that representation learning can capture meaningful world structure. However, the dominant framing treats these internal representations as *cognitive achievements* of individual systems, importing assumptions about bounded agency, stable beliefs, and epistemic authority from human psychology.

We argue this framing creates three critical problems for AI deployment in high-stakes domains:

1. **The Accountability Gap:** If a system's world model is an opaque internal state, who corrects it when wrong? Who audits it for bias? Who arbitrates between competing interpretations?

2. **The Stability Problem:** Internal representations drift silently across training runs and distributional shifts (Geirhos et al., 2020), cannot preserve minority hypotheses, and collapse uncertainty prematurely.

3. **The Governance Problem:** Granting epistemic authority to systems whose reasoning cannot be inspected or revised by domain experts undermines institutional oversight.

These are not merely technical challenges—they reflect a deeper conceptual error. We propose that world models should be understood not as private mental states but as *public semantic infrastructure*: shared, persistent, governed representational systems that multiple agents—human and artificial—participate in.

This reframing is not a restriction on AI capabilities but a continuation of how world modeling has always functioned. Human cognition itself is distributed across language, scientific theories, legal systems, maps, and social institutions (Clark & Chalmers, 1998; Hutchins, 1995). The human brain participates in this infrastructure; it does not solely contain it. Extending this participatory model to AI systems clarifies rather than constrains their role.

### 1.1 Contributions

This paper makes the following contributions:

1. **Conceptual:** We distinguish three senses of "world model"—correlational, referential, and authoritative—and argue that only the third requires the infrastructure framing we propose.

2. **Architectural:** We present the Semantically Honest Middle Layer (SHML), a formal three-tier architecture that models assertions as events, preserves provenance explicitly, and maintains multiple competing hypotheses.

3. **Technical:** We provide formal specifications for Candidate Informational Content (CIC) validation, belief-scoped reasoning protocols, and materialized projection mechanisms.

4. **Comparative:** We systematically compare our approach with existing frameworks (Semantic Web, knowledge graphs, neuro-symbolic systems) and address key objections.

5. **Practical:** We outline adoption pathways, evaluation metrics, and governance mechanisms for real-world deployment.

### 1.2 Paper Organization

Section 2 reviews related work across world models, knowledge representation, and distributed cognition. Section 3 clarifies what we mean by "world model" and distinguishes our framework from competing conceptions. Section 4 presents the SHML architecture with formal specifications. Section 5 provides concrete examples. Section 6 compares our approach with alternatives. Section 7 addresses objections. Section 8 outlines evaluation and adoption strategies. Section 9 discusses limitations and future work. Section 10 concludes.

---

## 2. Related Work

### 2.1 World Models in AI and Reinforcement Learning

The term "world model" gained prominence through Ha & Schmidhuber's (2018) work on model-based reinforcement learning, where agents learn compact latent representations of environment dynamics. Subsequent work (Hafner et al., 2019, 2020, 2023) developed increasingly sophisticated learned world models (DreamerV1-V3) that achieve impressive sample efficiency in continuous control tasks. LeCun (2022) has advocated for world models as a path toward more capable autonomous systems.

Recent interpretability work demonstrates that transformers develop internal representations of spatial layouts (Li et al., 2023), game board states (Nanda et al., 2023), and logical relationships (Olsson et al., 2022). These findings show that neural networks can capture meaningful world structure.

**Relationship to our work:** We acknowledge these internal representations exist and serve instrumental purposes. However, we argue they cannot serve the *normative* functions—accountability, auditability, governed revision—required when AI systems operate in domains with legal, medical, or financial consequences. Our framework treats learned representations as useful priors that must be grounded in auditable infrastructure rather than as standalone world models.

### 2.2 Knowledge Representation and Semantic Web

The Semantic Web vision (Berners-Lee et al., 2001) proposed a distributed knowledge layer for the internet, using RDF, OWL, and shared ontologies. Despite conceptual elegance, widespread adoption has been limited (Hitzler, 2021). Knowledge graphs have seen more practical success, particularly in industry (Noy et al., 2019; Hogan et al., 2021), though they often sacrifice formal rigor for pragmatic integration.

Upper ontologies—including BFO (Smith, 2016; Arp et al., 2015), DOLCE (Gangemi et al., 2002), SUMO (Niles & Pease, 2001), and UFO (Guizzardi, 2005)—provide foundational categories for domain modeling. BFO distinguishes between continuants (entities that persist through time) and occurrents (processes and events), a distinction central to our treatment of assertions.

The Cyc project (Lenat & Guha, 1989) represents a 40-year attempt to encode common-sense knowledge in logical form. Despite massive investment, Cyc has seen limited deployment, largely due to brittleness, manual encoding costs, and difficulty handling uncertainty.

**Relationship to our work:** We build on semantic web technologies but address three critical limitations: (1) the Semantic Web assumed human-created ontologies; we propose AI-assisted discovery with human governance, (2) standard knowledge graphs lack principled uncertainty representation; we treat uncertainty as first-class, (3) existing systems require full commitment before use; we allow provisional infrastructure through Candidate Informational Content.

### 2.3 Distributed and Extended Cognition

Clark & Chalmers (1998) argued that cognitive processes extend beyond the brain into tools and environmental scaffolding. Hutchins (1995) demonstrated how navigation knowledge is distributed across instruments, team members, and procedures. Tribble & Sutton (2011) extended this framework to cultural and historical practices.

This literature establishes that even human "world models" are not solely internal but distributed across external representational systems. Language itself functions as shared semantic infrastructure (Tomasello, 1999; Vygotsky, 1978).

**Relationship to our work:** We extend distributed cognition arguments to AI systems. If human cognition is already infrastructure-dependent, treating AI as infrastructure participants is not a limitation but an acknowledgment of how cognition operates.

### 2.4 Neuro-Symbolic AI and Hybrid Architectures

Neuro-symbolic AI (Garcez et al., 2019; Kautz, 2022) attempts to combine neural learning with symbolic reasoning. Approaches include: learned symbolic programs (Ellis et al., 2021), differentiable logic (Xu et al., 2018), and neural module networks (Andreas et al., 2016).

Retrieval-Augmented Generation (RAG) systems (Lewis et al., 2020) ground language models in external knowledge bases, improving factuality. However, RAG typically treats retrieved information as static context rather than modeling its provenance, uncertainty, or revision history.

**Relationship to our work:** We provide a neuro-symbolic architecture where neural systems propose candidate content and symbolic infrastructure governs its validation and commitment. Unlike typical neuro-symbolic approaches, we maintain an explicit semantic layer between neural outputs and logical assertions.

### 2.5 AI Safety and Alignment

Research on AI safety (Hendrycks et al., 2021) and alignment (Irving et al., 2018; Christiano et al., 2017) addresses how to ensure AI systems behave as intended. Debates about AI "understanding" (Bender & Koller, 2020) and interpretability (Lipton, 2018; Doshi-Velez & Kim, 2017) are closely related.

**Relationship to our work:** We argue the alignment problem may be more tractable when reframed: rather than aligning opaque internal world models, we can build infrastructure that AI systems participate in accountably. This shifts responsibility from "making AI think correctly" to "designing systems AI can engage with responsibly."

---

## 3. What We Mean by "World Model"

### 3.1 Three Senses of World Model

Confusion around whether AI systems "have" world models stems from conflating distinct senses of the term. We distinguish:

**World Model₁ (Correlational):** Internal representations that capture statistical regularities in data. Neural networks develop these through training. They enable prediction and generalization but carry no normative force.

**World Model₂ (Referential):** Structured representations that support reference to entities, tracking change over time, causal reasoning, and counterfactual exploration. These require stable entity identification and relational structure.

**World Model₃ (Authoritative):** Representational systems that serve as grounds for action, carry epistemic authority, support correction by domain experts, and enable accountability. These require governance mechanisms.

**Our thesis:** Neural networks can develop World Models₁ (and increasingly sophisticated approximations of World Models₂), but World Models₃ require public infrastructure. The distinction is not metaphysical but *functional*—it concerns what representational systems must do to support responsible deployment.

### 3.2 Why Private World Models Are Insufficient

Consider a medical diagnostic AI that develops internal representations of disease mechanisms. Even if these representations achieve high accuracy (World Model₁) and capture causal structure (World Model₂), they cannot function as World Models₃ without:

1. **Traceability:** Can we trace each conclusion to source observations and reasoning steps?
2. **Correctability:** Can domain experts inspect and override incorrect conclusions?
3. **Explicability:** Can the system explain its reasoning in terms physicians understand?
4. **Revisability:** When medical knowledge changes, can we systematically update the model?
5. **Auditability:** Can regulators verify the model meets safety standards?

Private internal representations, however sophisticated, cannot satisfy these requirements. They may be instrumentally useful—we can use them as priors or initializations—but they cannot serve as authoritative grounds for high-stakes decisions.

### 3.3 World Models as Representational Systems

Drawing on BFO and ontological realism, we define:

**Definition 1 (World Model as Infrastructure):** A world model is a structured representational system $\mathcal{M}$ that:
1. Supports reference to entities in a domain $\mathcal{D}$
2. Tracks entity states across time
3. Enables causal and counterfactual reasoning
4. Maintains provenance for all assertions
5. Supports revision under new evidence
6. Provides governance mechanisms for conflict resolution

Examples include: scientific ontologies (Gene Ontology, Disease Ontology), engineering standards (IEEE, ISO), legal codes, financial ledgers, and medical records systems.

**Key insight:** None of these requires that any single agent possess complete internal understanding. World modeling is a collective achievement distributed across institutions, artifacts, and practices.

---

## 4. The Semantically Honest Middle Layer (SHML)

### 4.1 Architectural Overview

SHML implements a three-tier architecture separating reality, semantic processes, and logical commitments:

```
┌─────────────────────────────────────────────┐
│         Reality Layer (BFO)                 │
│  Entities, Events, Causal Powers            │
│  (What actually exists and occurs)          │
└──────────────────┬──────────────────────────┘
                   │ observation, measurement
                   ▼
┌─────────────────────────────────────────────┐
│    Semantically Honest Middle Layer (SHML)  │
│  Assertions as Events, Provenance,          │
│  Candidate Content, Competing Hypotheses    │
│  (How knowledge claims are produced)        │
│                                             │
│  Substrate: Labeled Property Graphs         │
└──────────────────┬──────────────────────────┘
                   │ evaluation, commitment
                   ▼
┌─────────────────────────────────────────────┐
│          Logic Layer (RDF/OWL)              │
│  Materialized Projections, Public APIs      │
│  (What we publicly commit to)               │
└─────────────────────────────────────────────┘
```

**Key principle:** The logic layer contains *outcomes*, not primitives. Assertions in the logic layer are projections of validated semantic processes tracked in SHML.

### 4.2 The Reality Layer

**Ontological foundation:** We adopt BFO's realist framework:
- **Continuants:** Entities that persist through time (persons, machines, locations)
- **Occurrents:** Processes and events (measurements, diagnoses, assertions)
- **Qualities:** Properties inhering in continuants (temperature, mass)
- **Roles:** Realizable entities that can be activated (employee role, sensor role)

**Constraint:** The reality layer makes no claims about belief, interpretation, or certainty—only about what exists and what occurs.

### 4.3 The Middle Layer: SHML Core Concepts

#### 4.3.1 Assertions as Occurrents

**Principle:** Every assertion is an event carried out by an agent in a context, not a static fact about the world.

**Traditional knowledge graph:**
```
(Person_Aaron) -[worksAt]-> (Company_Fandaws)
```

**SHML representation:**
```
(Employment_Assertion_E47)
  -[:SUBJECT]-> (Person_Aaron)
  -[:OBJECT]-> (Company_Fandaws)
  -[:ASSERTED_BY]-> (HR_System_v2.3)
  -[:SOURCE]-> (Payroll_Database)
  -[:VALID_FROM {timestamp: "2024-01-15T09:00:00Z"}]
  -[:CONFIDENCE {value: 0.98, method: "direct_query"}]
```

**Benefits:**
- Temporal validity explicitly represented
- Source traceability preserved
- Confidence and method captured
- Revision history maintainable
- Multiple competing assertions can coexist

#### 4.3.2 The ICE → IBE → Text Staircase

To prevent collapsing persons with strings (a common knowledge graph error), SHML distinguishes:

1. **Information Content Entity (ICE):** Abstract informational structure (e.g., the *concept* of a name)
2. **Information Bearing Entity (IBE):** Physical realization of information (database record, document)
3. **Text Value:** Literal string in logic layer

**Example: Person designation**
```
[Person_Aaron] 
  --(is_designated_by)--> 
  [PersonName_ICE_744] 
  --(is_concretized_by)--> 
  [BirthCertificate_IBE_102] 
  --(has_text_value)--> 
  "Aaron Damiano"
```

**Why this matters:** When the person legally changes their name, the *person* hasn't changed—we create a new ICE linked to the same continuant with temporal validity. The staircase prevents ontological confusion between entities and their designations.

#### 4.3.3 Candidate Informational Content (CIC)

**Definition 2 (CIC):** A Candidate Informational Content is a tuple:

$$\text{CIC} = \langle e, r, v, c, P, t, s \rangle$$

Where:
- $e$ = entity (subject)
- $r$ = relation type
- $v$ = value (object)
- $c$ = confidence score $\in [0,1]$
- $P$ = provenance chain (ordered set of sources)
- $t$ = timestamp
- $s$ = status $\in \{\text{candidate, provisional, validated, deprecated}\}$

**Example:**
```
CIC_2847 = ⟨
  entity: Patient_47382,
  relation: hasDiagnosis,
  value: COVID-19_LongCOVID,
  confidence: 0.73,
  provenance: [Symptom_Report_S9234, Lab_Test_L4421, Dr_Smith_Assessment],
  timestamp: "2024-11-03T14:22:00Z",
  status: provisional
⟩
```

#### 4.3.4 CIC Validation Protocol

**Algorithm 1: CIC Promotion**

```
Input: CIC c, Domain D, Infrastructure I
Output: Updated status s' ∈ {rejected, provisional, validated}

1. Consistency Check:
   For each assertion a ∈ I:
     If conflicts(c, a, D.threshold):
       Create conflict record CR(c, a)
       If |{a ∈ I : conflicts(c, a)}| > D.max_conflicts:
         Return rejected

2. Confidence Thresholding:
   If c.confidence < D.min_confidence:
     Return rejected
   If c.confidence < D.validation_threshold:
     Return provisional

3. Provenance Validation:
   If |c.provenance| < D.min_sources:
     Return provisional
   For each source s ∈ c.provenance:
     If reliability(s) < D.min_reliability:
       Reduce c.confidence by penalty(s)

4. Expert Review (if required):
   If D.requires_expert AND available(qualified_expert):
     expert_assessment ← review(c, qualified_expert)
     If expert_assessment = approve:
       Return validated
     Else:
       Return provisional
   
5. Cross-Validation:
   corroboration ← count({c' ∈ I : supports(c', c)})
   If corroboration ≥ D.corroboration_threshold:
     Return validated
   Else:
     Return provisional
```

**Domain-specific thresholds:** Medical domains require higher confidence and expert review; exploratory scientific domains allow lower thresholds with clear provisional status.

### 4.4 Belief-Scoped Reasoning

#### 4.4.1 Situations as Coherent Belief Sets

**Definition 3 (Situation):** A situation $\Sigma$ is a coherent set of assertions that represents a possible state of affairs:

$$\Sigma = \{a_1, a_2, ..., a_n\} \text{ where } \forall i,j : \neg\text{contradicts}(a_i, a_j)$$

Multiple situations can coexist in SHML, representing:
- Competing hypotheses
- Different stakeholder perspectives
- Temporal states (current vs. historical)
- Counterfactual scenarios

**Example: Medical diagnosis with competing hypotheses**
```
Situation_Viral = {
  (Patient_X hasSymptom Fever),
  (Patient_X hasSymptom Fatigue),
  (Patient_X hasDiagnosis ViralInfection),
  (Patient_X recommendedTreatment RestAndFluids)
}

Situation_Bacterial = {
  (Patient_X hasSymptom Fever),
  (Patient_X hasSymptom Fatigue),
  (Patient_X hasDiagnosis BacterialInfection),
  (Patient_X recommendedTreatment Antibiotics)
}
```

Both situations share symptom observations but diverge on diagnosis and treatment.

#### 4.4.2 Conditional Reasoning Without Scope Crossing

**Inference Rule:** Reasoning never crosses situation boundaries unless explicitly comparing.

```
IF situation = Situation_Viral THEN
  Infer: Patient_X should avoid antibiotics
  
IF situation = Situation_Bacterial THEN
  Infer: Patient_X requires immediate antibiotics
  
Comparison:
  P(Situation_Viral | Evidence) = 0.35
  P(Situation_Bacterial | Evidence) = 0.65
  
Recommendation: 
  Proceed with Situation_Bacterial treatment
  Monitor for evidence that would increase P(Situation_Viral)
```

**Why this matters:** The system can reason soundly within each hypothesis while maintaining uncertainty about which hypothesis is correct—crucial for medical, legal, and scientific domains.

### 4.5 Materialized Projections to Logic Layer

#### 4.5.1 Projection Mechanism

The logic layer consists of *materialized views* of SHML content, optimized for:
- Performance (fast SPARQL queries)
- Interoperability (standard RDF/OWL)
- Stakeholder access control (different projections for different users)

**Projection Function:**
$$\pi: \text{SHML} \times \text{Context} \rightarrow \text{RDF}$$

Where Context specifies:
- Temporal scope (current state vs. historical)
- Confidence threshold (include only high-confidence assertions)
- Belief scope (which situations to project)
- Stakeholder role (what they're authorized to see)

**Example:**
```
π(SHML, {time: current, confidence: ≥0.9, role: physician})
→ RDF graph containing only current, high-confidence clinical assertions
  visible to physicians

π(SHML, {time: all, confidence: ≥0.5, role: researcher})
→ RDF graph containing historical and provisional assertions
  for research purposes
```

#### 4.5.2 Consistency Guarantees

**Theorem 1 (Projection Consistency):** For any context $C$, the projection $\pi(\text{SHML}, C)$ is internally consistent within the scope defined by $C$.

*Proof sketch:* The CIC validation protocol (Algorithm 1) ensures no contradictory assertions achieve validated status within the same domain context. Projections filter by context parameters, inheriting this consistency.

**Note:** Global consistency across all contexts is neither required nor desirable—different stakeholders legitimately hold different beliefs.

### 4.6 Substrate: Why Labeled Property Graphs

SHML uses Labeled Property Graphs (LPGs) rather than RDF triples because:

1. **Properties on edges:** Assertions carry metadata (confidence, timestamp, source) that would require complex reification in RDF
2. **Native provenance:** Directed edges naturally represent "according to" and "derived from" relationships
3. **Performanc:** Graph databases optimize for path queries essential to provenance tracing
4. **Clarity:** Process modeling maps naturally to graph structure

RDF remains valuable for the *logic layer* where simplicity and standardization matter. The architecture uses each substrate where it excels.

---

## 5. Concrete Examples

### 5.1 Example 1: Residency Assertion

**Scenario:** A property management system tracks where a person lives.

**Reality Layer (BFO):**
```
Person_Aaron: IndependentContinuant
House_123: Site (IndependentContinuant)
Resident_Role: Role (borne by Person_Aaron)
Occupancy_Process: Process (realizes Resident_Role)
```

**Middle Layer (SHML):**
```
(Residency_Assertion_A001)
  -[:SUBJECT]-> (Person_Aaron)
  -[:OBJECT]-> (House_123)
  -[:SOURCE]-> (Lease_Agreement_PDF_789)
  -[:ASSERTED_BY]-> (Property_Manager_Agent)
  -[:VALID_FROM {timestamp: "2024-01-01T00:00:00Z"}]
  -[:CONFIDENCE {value: 0.99, method: "legal_document"}]
  -[:STATUS]-> validated
```

**Logic Layer (RDF projection):**
```
:Person_Aaron :livesAt :House_123 .
```

**What honesty preserves:**
- Source: Lease agreement (traceable)
- Agent: Property manager (accountable)
- Temporal validity: From Jan 1, 2024 (revisable)
- Confidence: 0.99 (uncertainty acknowledged)

**Revision scenario:** If Person_Aaron moves out on June 1, 2024:
1. Property manager creates new assertion with VALID_UNTIL on original
2. New assertion created for new residence
3. Logic layer projection updated automatically
4. Historical queries can retrieve past residency
5. Audit trail preserved

### 5.2 Example 2: Medical Diagnosis Under Uncertainty

**Scenario:** Patient presents with fever, cough, and fatigue. Two competing diagnoses are plausible.

**Reality Layer:**
```
Patient_57: Person
Symptom_Fever: Quality (inheres in Patient_57)
Symptom_Cough: Quality (inheres in Patient_57)
Lab_Test_Process_01: Measurement (has participant: Patient_57)
```

**Middle Layer (SHML) - Competing CICs:**

```
CIC_Flu = ⟨
  entity: Patient_57,
  relation: hasDiagnosis,
  value: InfluenzaA,
  confidence: 0.62,
  provenance: [Symptom_Report, Rapid_Flu_Test_Positive, Clinical_Assessment],
  timestamp: "2024-12-15T10:30:00Z",
  status: provisional
⟩

CIC_COVID = ⟨
  entity: Patient_57,
  relation: hasDiagnosis,
  value: COVID19,
  confidence: 0.71,
  provenance: [Symptom_Report, PCR_Test_Positive, Clinical_Assessment],
  timestamp: "2024-12-15T11:00:00Z",
  status: provisional
⟩

CIC_Coinfection = ⟨
  entity: Patient_57,
  relation: hasDiagnosis,
  value: Flu_COVID_Coinfection,
  confidence: 0.38,
  provenance: [Both_Tests_Positive, Literature_Review_Study_X],
  timestamp: "2024-12-15T11:15:00Z",
  status: candidate
⟩
```

**Situation-based reasoning:**
```
Situation_COVID_Primary:
  Diagnosis: COVID-19
  Treatment: Paxlovid + monitoring
  Confidence: 0.71
  
Situation_Flu_Primary:
  Diagnosis: Influenza A
  Treatment: Tamiflu + monitoring
  Confidence: 0.62
  
Situation_Coinfection:
  Diagnosis: Both
  Treatment: Both antivirals
  Confidence: 0.38
```

**Physician interface (logic layer projection):**
Shows all three situations with confidence scores, allowing physician to:
- Review evidence for each hypothesis
- Make informed treatment decision
- Document which hypothesis they're acting on
- System tracks actual clinical outcome for future learning

**What traditional systems lose:**
- Multiple hypotheses collapsed to single diagnosis
- Uncertainty hidden or eliminated
- Provenance of each hypothesis lost
- Cannot track which hypothesis informed treatment
- Difficult to learn from outcomes

### 5.3 Example 3: Scientific Literature Integration

**Scenario:** Different research papers report conflicting findings about a biochemical pathway.

**Reality Layer:**
```
Protein_BRCA1: IndependentContinuant (Molecule)
Protein_P53: IndependentContinuant (Molecule)
Interaction_Process: BiologicalProcess
```

**Middle Layer (SHML) - Competing claims:**

```
CIC_Strong_Binding = ⟨
  entity: Protein_BRCA1,
  relation: bindsTo,
  value: Protein_P53,
  confidence: 0.88,
  provenance: [Paper_Nature_2023, Experiment_Yeast2H, Lab_Harvard],
  timestamp: "2023-09-12T00:00:00Z",
  status: validated
⟩

CIC_Weak_Binding = ⟨
  entity: Protein_BRCA1,
  relation: bindsTo,
  value: Protein_P53,
  confidence: 0.79,
  provenance: [Paper_Cell_2023, Experiment_CoIP, Lab_Stanford],
  timestamp: "2023-10-20T00:00:00Z",
  status: validated,
  qualifier: "only in presence of DNA damage"
⟩

CIC_No_Binding = ⟨
  entity: Protein_BRCA1,
  relation: bindsTo,
  value: Protein_P53,
  confidence: 0.34,
  provenance: [Paper_PLOS_2024, Experiment_SPR, Lab_MIT],
  timestamp: "2024-01-15T00:00:00Z",
  status: provisional,
  conflict_note: "contradicts CIC_Strong_Binding, CIC_Weak_Binding"
⟩
```

**SHML preserves scientific discourse:**
- All three findings remain in the system
- Researchers can access full provenance
- Meta-analysis can weight by experimental method
- System flags conflicts for investigation
- New experiments can be designed to resolve disagreement

**Logic layer projections for different users:**
```
π(SHML, {role: undergraduate, confidence: ≥0.85}) 
→ Shows only strong binding (simplified for teaching)

π(SHML, {role: researcher, confidence: ≥0.3})
→ Shows all three with full context (comprehensive for research)

π(SHML, {role: clinician, confidence: ≥0.75})
→ Shows strong and weak binding with clinical implications
```

---

## 6. Comparison with Existing Approaches

### 6.1 Traditional Knowledge Graphs

| Dimension | Traditional KG | SHML |
|-----------|---------------|------|
| Assertions | Static predicates | Events with provenance |
| Contradiction | Error condition | Divergent hypotheses (preserved) |
| Uncertainty | Sometimes confidence scores | Explicit CIC status + confidence |
| Temporal | Versioning (if implemented) | Native temporal validity |
| Provenance | Reification or named graphs | First-class LPG properties |
| Revision | Replace triples | Create new assertions, preserve history |

**Example:** DBpedia states "Barack Obama was President of the United States" but doesn't explicitly represent *when* this was true or *who asserted* it. Historical queries are difficult.

### 6.2 Semantic Web

The Semantic Web (Berners-Lee et al., 2001) shares our vision of shared knowledge infrastructure but faces three limitations SHML addresses:

1. **Ontology Creation:** Semantic Web assumed human experts would build ontologies manually → SHML enables AI-assisted ontology discovery through CIC proposal mechanism

2. **Uncertainty:** OWL provides logical expressivity but no principled uncertainty handling → SHML treats uncertainty as first-class through confidence scores and belief scopes

3. **Commitment Requirements:** RDF requires full commitment to triples before use → SHML allows provisional infrastructure through CIC status levels

**Why Semantic Web adoption was limited:**
- High barrier to entry (required ontology engineering expertise)
- Brittleness (no graceful degradation under partial knowledge)
- Closed-world assumptions (anything not stated is false)

**How SHML differs:**
- Lower barrier (AI systems can propose structure, humans govern)
- Graceful uncertainty (provisional content remains useful)
- Open-world by design (absence of assertion ≠ falsehood)

### 6.3 Cyc

The Cyc project (Lenat & Guha, 1989) represents perhaps the most ambitious attempt at building a comprehensive world model. After 40 years and hundreds of millions of dollars, Cyc contains millions of assertions but has seen limited real-world deployment.

**Cyc's challenges:**
1. **Top-down engineering:** Expert-designed ontology → SHML uses bottom-up CIC discovery
2. **Classical logic:** No uncertainty representation → SHML native uncertainty support
3. **Manual entry:** Human knowledge engineering → SHML AI-assisted extraction
4. **Closed system:** Proprietary, centralized → SHML designed for federation
5. **Commitment overhead:** Must fully specify before use → SHML provisional content

**Lesson learned:** Comprehensive world models cannot be hand-crafted. They must emerge from participatory processes with explicit uncertainty management.

### 6.4 Retrieval-Augmented Generation (RAG)

RAG systems (Lewis et al., 2020) ground language models in external knowledge by retrieving relevant passages. This improves factuality but has limitations:

| Dimension | RAG | SHML |
|-----------|-----|------|
| Retrieval unit | Text passages | Structured assertions |
| Provenance | Document citation | Full evidence chain |
| Uncertainty | Implicit in generation | Explicit confidence scores |
| Contradiction | Left to LLM to resolve | Preserved as competing hypotheses |
| Revision | Update document store | Governed validation protocol |
| Temporal | Timestamp on documents | Assertion-level temporal validity |

**Example:** RAG might retrieve conflicting medical studies and ask the LLM to synthesize them. SHML would preserve both as competing CICs with full provenance, allowing physicians to see the evidence directly.

### 6.5 Neuro-Symbolic Architectures

Recent neuro-symbolic approaches (Garcez et al., 2019; Kautz, 2022) combine learning and reasoning but typically:
- Treat symbols as ground truth → SHML treats assertions as provisional
- Require clean symbolic input → SHML handles noisy candidate content
- Focus on inference → SHML emphasizes provenance and governance

**Complementarity:** SHML provides the semantic layer where neuro-symbolic systems can contribute candidate content through learning while symbolic infrastructure provides grounding and governance.

---

## 7. Addressing Objections

### 7.1 Objection: "This is too complex for practical use"

**Response:** Complexity exists whether we acknowledge it or not. Traditional systems hide complexity by:
- Collapsing uncertainty into point estimates
- Discarding provenance information
- Forcing premature commitment
- Hiding contradictions

SHML makes existing complexity *explicit and manageable* rather than hidden and uncontrollable.

**Empirical question:** Does explicit complexity management reduce overall system fragility? We hypothesize yes, and outline evaluation metrics in Section 8.

**Adoption path:** Organizations can adopt SHML incrementally:
- Phase 1: Audit layer only (track provenance of existing assertions)
- Phase 2: Add conflict detection (identify contradictions)
- Phase 3: Full governance (CIC validation protocol)

Each phase delivers value independently.

### 7.2 Objection: "Internal models are faster and more flexible"

**Response:** We don't claim infrastructure replaces internal models entirely. The architecture supports both:

- **Internal models (neural):** Handle real-time inference, pattern recognition, proposal generation → optimized for speed
- **Infrastructure (SHML):** Provides grounding, governance, accountability → optimized for auditability
- **Combination:** Enables both rapid response and responsible oversight

**Example:** A medical AI might use internal representations to generate diagnostic hypotheses quickly (World Model₁), but these enter SHML as CICs requiring validation before being presented to physicians as recommendations (World Model₃).

### 7.3 Objection: "You can't bootstrap infrastructure without internal models"

**Response:** This is correct—and our architecture accommodates it:

1. **Initial state:** Domain lacks formal infrastructure
2. **AI proposes:** Neural systems extract candidate structure from text/data → generates CICs
3. **Humans validate:** Domain experts review proposals, adjusting confidence and adding context
4. **Infrastructure emerges:** Validated CICs become shared infrastructure
5. **Refinement:** AI proposes modifications, humans govern acceptance

**Crucially:** AI accelerates *proposal*, not *authority*. The system maintains clear accountability for what achieves validated status.

**Historical parallel:** Scientific literature works this way—papers propose findings (CICs), peer review validates (governance), accepted findings become shared knowledge (infrastructure). SHML formalizes and accelerates this process.

### 7.4 Objection: "This just pushes the problem up one level"

**Response:** Partially true—validation criteria themselves require justification. However:

1. **Transparency gain:** Domain-specific validation thresholds are explicit parameters that can be audited, debated, and adjusted
2. **Accountability improvement:** When validation fails, we can identify whether the problem was inadequate evidence, poor validation criteria, or system malfunction
3. **Governance mechanism:** Unlike opaque neural models, validation protocols can be understood and modified by domain experts

**Example:** Medical domains might require:
```
min_confidence = 0.85
min_sources = 3
requires_expert = true
corroboration_threshold = 2
```

These parameters are *policy decisions* open to institutional oversight—far better than black-box model decisions.

### 7.5 Objection: "Biological systems have internal world models that work fine"

**Response:** We distinguish two claims:

1. **Descriptive:** Do biological systems develop internal representations? Yes, uncontroversially.
2. **Normative:** Should we grant artificial systems the same autonomy we grant biological ones? This requires argument.

**Key differences:**
- **Evolutionary testing:** Biological world models were refined over millions of years by survival pressure
- **Social embedding:** Human cognition is already embedded in institutional oversight (legal, medical, scientific)
- **Scale:** Individual human errors have bounded impact; AI systems operate at scale where errors compound
- **Responsibility:** Humans can be held accountable; current AI systems cannot

**Our claim:** For AI deployment in high-stakes domains, explicit infrastructure governance is preferable to assuming learned representations are sufficient—especially given current brittleness and lack of theoretical guarantees.

### 7.6 Objection: "This assumes disagreement is common, but most facts are agreed upon"

**Response:** Domain-dependent. In stable, well-characterized domains (e.g., basic physics), agreement is high. In rapidly evolving, high-stakes domains (medicine, law, climate science, public health), disagreement is common and epistemically important.

**Examples of legitimate disagreement:**
- Multiple plausible diagnoses given limited evidence
- Competing scientific theories prior to decisive experiments
- Different legal interpretations of novel situations
- Uncertainty in predictive models (economic forecasts, climate projections)

**SHML design choice:** Optimize for domains where disagreement matters. For domains with stable consensus, the system simplifies—high-confidence assertions converge quickly.

---

## 8. Evaluation and Adoption

### 8.1 Evaluation Metrics

We propose evaluating SHML-based systems against traditional approaches using:

#### 8.1.1 Accuracy Metrics
- **Calibrated confidence:** Do confidence scores match empirical frequencies? ($\text{ECE}$ - Expected Calibration Error)
- **Predictive accuracy:** Correctness of high-confidence assertions in held-out data
- **Temporal stability:** Do assertions remain valid over specified time windows?

#### 8.1.2 Explainability Metrics
- **Provenance completeness:** Percentage of assertions with full traceable provenance
- **Explanation depth:** Average chain length from conclusion to source observations
- **Expert comprehensibility:** Can domain experts understand and verify reasoning chains? (human evaluation)

#### 8.1.3 Revisability Metrics
- **Update latency:** Time from new evidence to infrastructure revision
- **Impact propagation:** Percentage of dependent assertions correctly updated when foundational assertions change
- **Rollback capability:** Can system reconstruct state at any historical timestamp?

#### 8.1.4 Governance Metrics
- **Audit coverage:** Percentage of high-stakes assertions with complete audit trails
- **Conflict detection:** Recall/precision for identifying contradictory assertions
- **Accountability tracing:** Can every assertion be traced to a responsible agent?

### 8.2 Proposed Experimental Evaluation

**Domain:** Medical knowledge graph construction from literature

**Comparison groups:**
1. **Baseline (traditional KG):** Direct entity-relation extraction → RDF triples
2. **RAG System:** LLM with retrieval grounding
3. **SHML System:** Full three-tier architecture with CIC validation

**Test scenario:** 
- Input: 1000 recent medical papers on a specific condition (e.g., long COVID)
- Task: Build knowledge graph of symptoms, treatments, outcomes
- Evaluation: Physician expert panel assesses:
  - Factual accuracy of extracted relations
  - Handling of conflicting evidence
  - Utility for clinical decision support
  - Audit trail completeness

**Hypotheses:**
- H1: SHML will show better calibration (confidence matches accuracy)
- H2: SHML will preserve more contradictory evidence (higher conflict detection)
- H3: SHML will provide more complete provenance (higher audit coverage)
- H4: SHML may have lower raw precision but higher utility (explicitly shows uncertainty)

### 8.3 Adoption Strategy

#### 8.3.1 Backward Compatibility

SHML can wrap existing systems without requiring full rebuilds:

**Legacy system integration:**
```
Traditional KG triple: (Drug_X treats Disease_Y)
↓ automatic wrapping
SHML representation:
  Assertion_Import_47 {
    subject: Drug_X,
    relation: treats,
    object: Disease_Y,
    source: Legacy_KG_v3,
    confidence: 0.7 (default for legacy imports),
    status: provisional,
    timestamp: import_date,
    note: "Requires expert validation"
  }
```

**Benefit:** Existing knowledge isn't lost but gains explicit provenance and requires validation.

#### 8.3.2 Economic Incentives

Organizations adopt new infrastructure when it provides value. SHML offers:

1. **Risk reduction:** In regulated domains (healthcare, finance), audit trails prevent costly compliance failures
2. **Debugging efficiency:** Provenance tracking reduces time to identify and fix errors
3. **Knowledge reuse:** Validated infrastructure prevents redundant discovery
4. **Liability protection:** Clear accountability when AI systems contribute to decisions

**ROI calculation example (healthcare):**
- Cost: Initial SHML implementation (~$500K for mid-size hospital system)
- Benefit: Prevent one major misdiagnosis liability case ($2M average)
- Additional: Reduce diagnostic error investigation time (20% time savings for medical teams)

#### 8.3.3 Phased Deployment

**Phase 1: Observation (Months 1-3)**
- Deploy SHML as passive audit layer
- Track provenance of existing system outputs
- Identify gaps in traceability
- Build confidence in architecture

**Phase 2: Detection (Months 4-6)**
- Activate conflict detection
- Flag contradictions for review
- Measure impact on decision quality
- Refine validation protocols

**Phase 3: Governance (Months 7-12)**
- Full CIC validation activated
- AI-proposed content enters as candidates
- Expert review workflow integrated
- Complete infrastructure transition

**Success metrics per phase:**
- Phase 1: 95% provenance coverage
- Phase 2: 80% conflict detection recall
- Phase 3: 90% expert satisfaction with validation workflow

### 8.4 Open Research Questions

1. **Optimal validation protocols:** How should domain-specific thresholds be set? Can they be learned from data?

2. **Scale characteristics:** How does SHML performance degrade with millions of CICs? What indexing strategies are optimal?

3. **Cross-domain federation:** Can multiple SHML instances negotiate semantic alignment without central coordination?

4. **AI proposal quality:** How can we improve AI-generated CIC quality to reduce validation burden?

5. **Theoretical guarantees:** Can we prove formal properties about consistency, convergence, or information preservation?

---

## 9. Limitations and Future Work

### 9.1 Current Limitations

**Technical:**
- No implemented large-scale deployment (proof-of-concept only)
- Computational overhead not fully characterized
- Optimal LPG database technology not definitively identified

**Theoretical:**
- Validation protocols remain domain-specific (no universal solution)
- Conflict resolution mechanisms need refinement
- Relationship to formal epistemology under-explored

**Practical:**
- Adoption barriers in organizations with legacy systems
- Requires cultural shift toward explicit uncertainty
- Expert validation remains human bottleneck

### 9.2 Future Work

**Near-term (1-2 years):**
1. Implement production SHML system in constrained medical domain
2. Conduct empirical evaluation per Section 8.2 metrics
3. Develop tooling for expert validation workflows
4. Publish formal semantics and complexity analysis

**Medium-term (2-5 years):**
1. Extend to multiple domains (legal, financial, scientific)
2. Develop federated SHML protocols for cross-organizational collaboration
3. Investigate automated validation using ensembles of expert models
4. Build educational curricula for semantic infrastructure engineering

**Long-term (5+ years):**
1. Establish SHML as standard middleware for safety-critical AI systems
2. Develop governance frameworks for public semantic infrastructure
3. Investigate relationship to human institutional knowledge production
4. Theoretical foundations for provable properties

### 9.3 Broader Implications

**For AI Safety:**
If alignment is about building infrastructure rather than aligning models, safety research should focus on:
- Governance protocol design
- Audit mechanism development
- Uncertainty representation standards
- Accountability frameworks

**For Epistemology:**
SHML formalizes philosophical concepts:
- Justification (provenance chains)
- Defeaters (conflicting evidence)
- Degrees of belief (confidence scores)
- Epistemic community (validation governance)

Bidirectional exchange between AI and formal epistemology could be productive.

**For Science Studies:**
SHML mirrors scientific practice:
- Hypothesis proposal
- Peer validation
- Provisional acceptance
- Revision under new evidence

Could SHML itself become infrastructure for scientific knowledge management?

---

## 10. Conclusion

We have argued that the question "Does this AI system have a world model?" conflates three distinct senses—correlational, referential, and authoritative—with different requirements and implications. While neural networks can develop sophisticated internal representations serving correlational and increasingly referential functions, these cannot fulfill the accountability, auditability, and governance requirements of authoritative world models in high-stakes domains.

We propose an alternative framing: world models as *semantic infrastructure*—shared, governed, auditable representational systems that both humans and AI systems participate in. The Semantically Honest Middle Layer (SHML) implements this vision through a three-tier architecture that:

1. Grounds assertions in ontological realism (BFO reality layer)
2. Models knowledge production processes explicitly (SHML with LPG substrate)
3. Provides performant logical interfaces (materialized RDF projections)

SHML treats assertions as events, preserves provenance, maintains competing hypotheses, and allows provisional content—addressing critical limitations of both traditional knowledge graphs and opaque neural representations.

This reframing shifts the locus of AI alignment from "making models think correctly" to "building infrastructure that supports accountable participation"—a more tractable problem with clearer governance mechanisms and institutional oversight.

**The path forward:** We do not propose abandoning learned world models but integrating them into accountable infrastructure. Neural systems excel at pattern recognition and candidate proposal; formal infrastructure excels at governance and auditability. Together, they can support AI deployment that is both capable and responsible.

The future of AI lies not in ever-larger private world models, but in participatory semantic infrastructure that distributes epistemic authority appropriately—granting AI systems the role of rapid, creative proposal generators while preserving human expertise, institutional oversight, and democratic accountability where they matter most.

---

## Acknowledgments

This work builds on decades of research in knowledge representation, formal ontology, and distributed cognition. We are particularly indebted to Barry Smith and the BFO community for ontological foundations, and to Andy Clark, Ed Hutchins, and distributed cognition researchers for demonstrating that cognition has always been infrastructure-dependent.

---

## References

Andreas, J., Rohrbach, M., Darrell, T., & Klein, D. (2016). Neural module networks. *Proceedings of CVPR 2016*.

Arp, R., Smith, B., & Spear, A. D. (2015). *Building ontologies with basic formal ontology*. MIT Press.

Bender, E. M., & Koller, A. (2020). Climbing towards NLU: On meaning, form, and understanding in the age of data. *Proceedings of ACL 2020*, 5185-5198.

Berners-Lee, T., Hendler, J., & Lassila, O. (2001). The semantic web. *Scientific American*, 284(5), 34-43.

Christiano, P. F., Leike, J., Brown, T., Martic, M., Legg, S., & Amodei, D. (2017). Deep reinforcement learning from human preferences. *Advances in Neural Information Processing Systems*, 30.

Clark, A., & Chalmers, D. (1998). The extended mind. *Analysis*, 58(1), 7-19.

Doshi-Velez, F., & Kim, B. (2017). Towards a rigorous science of interpretable machine learning. *arXiv preprint arXiv:1702.08608*.

Ellis, K., Wong, L., Nye, M., Sablé-Meyer, M., Cary, L., Morales, L., ... & Tenenbaum, J. B. (2021). DreamCoder: Growing generalizable, interpretable knowledge with wake-sleep Bayesian program learning. *Proceedings of PLDI 2021*.

Gangemi, A., Guarino, N., Masolo, C., Oltramari, A., & Schneider, L. (2002). Sweetening ontologies with DOLCE. *Knowledge Engineering and Knowledge Management*, 166-181.

Garcez, A. D. A., Gori, M., Lamb, L. C., Serafini, L., Spranger, M., & Tran, S. N. (2019). Neural-symbolic computing: An effective methodology for principled integration of machine learning and reasoning. *arXiv preprint arXiv:1905.06088*.

Geirhos, R., Jacobsen, J. H., Michaelis, C., Zemel, R., Brendel, W., Bethge, M., & Wichmann, F. A. (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence*, 2(11), 665-673.

Guizzardi, G. (2005). *Ontological foundations for structural conceptual models*. University of Twente.

Ha, D., & Schmidhuber, J. (2018). World models. *arXiv preprint arXiv:1803.10122*.

Hafner, D., Lillicrap, T., Ba, J., & Norouzi, M. (2019). Dream to control: Learning behaviors by latent imagination. *arXiv preprint arXiv:1912.01603*.

Hafner, D., Lillicrap, T., Fischer, I., Villegas, R., Ha, D., Lee, H., & Davidson, J. (2020). Learning latent dynamics for planning from pixels. *ICML 2020*.

Hafner, D., Pasukonis, J., Ba, J., & Lillicrap, T. (2023). Mastering diverse domains through world models. *arXiv preprint arXiv:2301.04104*.

Hendrycks, D., Carlini, N., Schulman, J., & Steinhardt, J. (2021). Unsolved problems in ML safety. *arXiv preprint arXiv:2109.13916*.

Hitzler, P. (2021). A review of the semantic web field. *Communications of the ACM*, 64(2), 76-83.

Hogan, A., Blomqvist, E., Cochez, M., d'Amato, C., Melo, G. D., Gutierrez, C., ... & Zimmermann, A. (2021). Knowledge graphs. *ACM Computing Surveys*, 54(4), 1-37.

Hutchins, E. (1995). *Cognition in the wild*. MIT Press.

Irving, G., Christiano, P., & Amodei, D. (2018). AI safety via debate. *arXiv preprint arXiv:1805.00899*.

Kautz, H. (2022). The third AI summer: AAAI Robert S. Engelmore memorial lecture. *AI Magazine*, 43(1), 93-104.

LeCun, Y. (2022). A path towards autonomous machine intelligence. *Open Review*, 62.

Lenat, D. B., & Guha, R. V. (1989). *Building large knowledge-based systems: Representation and inference in the Cyc project*. Addison-Wesley.

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., ... & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems*, 33, 9459-9474.

Li, K., Hopkins, A. K., Bau, D., Viégas, F., Pfister, H., & Wattenberg, M. (2023). Emergent world representations: Exploring a sequence model trained on a synthetic task. *ICLR 2023*.

Lipton, Z. C. (2018). The mythos of model interpretability. *Queue*, 16(3), 31-57.

Nanda, N., Chan, L., Lieberum, T., Smith, J., & Steinhardt, J. (2023). Progress measures for grokking via mechanistic interpretability. *ICLR 2023*.

Niles, I., & Pease, A. (2001). Towards a standard upper ontology. *Proceedings of FOIS*, 2, 2-9.

Noy, N., Gao, Y., Jain, A., Narayanan, A., Patterson, A., & Taylor, J. (2019). Industry-scale knowledge graphs: Lessons and challenges. *Communications of the ACM*, 62(8), 36-43.

Olsson, C., Elhage, N., Nanda, N., Joseph, N., DasSarma, N., Henighan, T., ... & Olah, C. (2022). In-context learning and induction heads. *arXiv preprint arXiv:2209.11895*.

Smith, B. (2016). *Basic formal ontology 2.0: Specification and user's guide*. University at Buffalo.

Tomasello, M. (1999). *The cultural origins of human cognition*. Harvard University Press.

Tribble, E. B., & Sutton, J. (2011). Cognitive ecology as a framework for Shakespearean studies. *Shakespeare Studies*, 39, 94-103.

Vygotsky, L. S. (1978). *Mind in society: Development of higher psychological processes*. Harvard University Press.

Xu, J., Zhang, Z., Friedman, T., Liang, Y., & Van den Broeck, G. (2018). A semantic loss function for deep learning with symbolic knowledge. *ICML 2018*.

---

## Appendix A: Formal Notation Summary

**Candidate Informational Content (CIC):**
$$\text{CIC} = \langle e, r, v, c, P, t, s \rangle$$
- $e \in \mathcal{E}$: entity (subject)
- $r \in \mathcal{R}$: relation type
- $v \in \mathcal{V}$: value (object)
- $c \in [0,1]$: confidence score
- $P \subseteq \mathcal{S}$: ordered provenance chain (sources)
- $t \in \mathbb{T}$: timestamp
- $s \in \{\text{candidate, provisional, validated, deprecated}\}$: status

**Situation:**
$$\Sigma \subseteq \mathcal{A} \text{ such that } \forall a_i, a_j \in \Sigma: \neg\text{contradicts}(a_i, a_j)$$

**Projection Function:**
$$\pi: \text{SHML} \times \mathcal{C} \rightarrow \text{RDF}$$
Where $\mathcal{C}$ = context parameters (time, confidence threshold, belief scope, role)

**Conflict Relation:**
$$\text{conflicts}: \text{CIC} \times \text{CIC} \times \mathbb{R}^+ \rightarrow \{\text{true, false}\}$$

**Domain Parameters $\mathcal{D}$:**
- min_confidence: $\alpha \in [0,1]$
- min_sources: $\beta \in \mathbb{N}$
- requires_expert: $\text{bool}$
- corroboration_threshold: $\gamma \in \mathbb{N}$
- max_conflicts: $\delta \in \mathbb{N}$

---

## Appendix B: SHML Implementation Notes

**Recommended Technology Stack:**

- **SHML Layer:** Neo4j or Amazon Neptune (LPG databases with strong query performance)
- **Logic Layer:** Apache Jena or Virtuoso (RDF triple stores)
- **Projection Mechanism:** Custom materialization engine (scheduled or event-driven)
- **Validation Workflow:** Apache Airflow or Temporal (orchestration)
- **Expert Interface:** Domain-specific web application with provenance visualization

**Performance Considerations:**

- LPG queries (provenance tracing): O(path_length) 
- Projection generation: O(SHML_size × context_filters)
- Conflict detection: O(n²) worst case, O(n log n) with indexing

**Open Source Components:**

We commit to open-sourcing:
1. SHML formal specification (OWL/SHACL)
2. Reference implementation (Python/Neo4j)
3. Validation protocol templates
4. Example datasets with CICs

Target: Q3 2026

---

*End of Document*
