# Integral Ethics Agent (IEA) — Architecture v2.1

**Version:** 2.1  
**Date:** 2026-01-25  
**Status:** Reference Architecture  
**Authors:** Aaron Damiano  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Philosophical Foundations](#2-philosophical-foundations)
3. [Design Principles](#3-design-principles)
4. [System Architecture](#4-system-architecture)
5. [Component Specifications](#5-component-specifications)
6. [Data Flow & Protocols](#6-data-flow--protocols)
7. [Output Schemas](#7-output-schemas)
8. [User Experience & Interface Guidance](#8-user-experience--interface-guidance)
9. [Ecosystem Integration](#9-ecosystem-integration)
10. [Failure Modes & Safeguards](#10-failure-modes--safeguards)
11. [Computational Considerations](#11-computational-considerations)
12. [Regulatory Alignment](#12-regulatory-alignment)
13. [Scope, Limitations & Disclaimers](#13-scope-limitations--disclaimers)
14. [Maturity & Roadmap](#14-maturity--roadmap)
15. [Changelog](#15-changelog)

---

## 1. Executive Summary

The Integral Ethics Agent (IEA) is a normative reasoning system that provides transparent, multi-perspective moral deliberation by integrating:

- **Twelve archetypal worldviews** derived from Rudolf Steiner's phenomenology of perspectives
- **Semantic analysis** via TagTeam v2.0.0 for ontologically-grounded entity and value extraction
- **Procedural safeguards** ensuring epistemic honesty, user agency, and auditability
- **Jurisprudential memory** via HIRI-signed precedent ledgers

The architecture separates **ethical reasoning** (the IEE "bones") from **natural language processing** (the LLM "skin"), with a **semantic bridge** (the "membrane") ensuring faithful translation between them.

### 1.1 Key Capabilities

- Multi-worldview consultation with explicit weighting rationale
- Non-reductive integration preserving genuine incommensurability
- Semantic handshake ensuring mutual understanding before deliberation
- Ethical triage scaling computational depth to moral stakes
- Persistent, verifiable ethical audit trail
- Extensible worldview framework for cross-cultural adaptation

### 1.2 What This System Is

| The IEA Is | The IEA Is Not |
|------------|----------------|
| A deliberative aid for ethical reflection | A moral oracle outputting "the right answer" |
| A transparency mechanism for auditable reasoning | A liability shield for institutional decisions |
| A pluralism-preserving framework refusing false closure | A replacement for human moral judgment |
| A memory system enabling precedent-based consistency | A preference-satisfaction engine |
| A Western pluralist framework with extensibility pathways | A culturally universal system |

### 1.3 Current Maturity

This document describes a **reference architecture**, not a deployment-ready system. See §14 for component maturity levels and implementation roadmap.

---

## 2. Philosophical Foundations

### 2.1 The Problem of Ethical Foundations

Contemporary ethical AI suffers from three failure modes:

1. **Monistic reductionism** — Forcing all values into single currencies (utility, rights, virtue)
2. **Opaque eclecticism** — Ad hoc borrowing without principled integration
3. **Hidden aggregation** — Claiming pluralism while secretly optimizing a scalar

The IEA proposes **perspectival realism**: multiple worldviews each capture genuine aspects of reality from distinct orientational stances. Mature ethical reasoning requires integrating insights across perspectives rather than privileging any single foundation.

### 2.2 The Twelve Worldviews: Selection, Justification & Extensibility

The IEA consults twelve archetypal worldviews drawn from Steiner's phenomenology (1914/2008).

#### 2.2.1 Honest Acknowledgment of Cultural Situatedness

**The twelve worldviews represent a Western philosophical framework.** They emerge from European phenomenological and idealist traditions. While they have proven comprehensive within that tradition—mapping successfully onto major Western philosophical schools from Democritus to Whitehead—the IEA does not claim they exhaust all possible ethical orientations globally.

Other philosophical traditions might generate different typologies:

| Tradition | Potentially Distinct Orientations |
|-----------|-----------------------------------|
| **Confucian** | Relational role ethics, ritual propriety (*li*), humaneness (*ren*) |
| **Buddhist** | Dependent origination, emptiness (*śūnyatā*), skillful means (*upāya*) |
| **Ubuntu** | Communal personhood ("I am because we are"), ancestral continuity |
| **Indigenous (varied)** | Land-based relationality, seven-generation thinking, non-human personhood |
| **Islamic** | Divine command within *fiqh* (jurisprudence), *maslaha* (public interest) |

**The IEA's position:** The twelve worldviews are offered as a *default configuration* for contexts where Western pluralist ethics is appropriate. The architecture is designed for extensibility—alternative worldview sets can be loaded via the OCE registry for contexts where other traditions are more appropriate (see §2.2.5).

#### 2.2.2 Selection Criteria

The default twelve were selected because they satisfy:

| Criterion | Explanation |
|-----------|-------------|
| **Historical Coverage** | Major Western philosophical schools map onto these worldviews or combinations |
| **Conceptual Systematicity** | They organize along fundamental axes: Being/Becoming, Matter/Mind, Individual/Universal |
| **Phenomenological Validation** | Individuals recognize themselves in different worldviews; sustained inquiry reveals orientational stances |
| **Practical Tractability** | Twelve is computationally manageable while maintaining meaningful diversity |

#### 2.2.3 The Twelve Worldviews

| Worldview | Core Orientation | Ethical Implication |
|-----------|------------------|---------------------|
| **Materialism** | Reality is fundamentally physical | Material wellbeing foundational; empirical methods reliable |
| **Sensationalism** | Reality is what we experience through senses | Experiential richness matters; abstractions must be grounded |
| **Phenomenalism** | Reality is appearances as given to consciousness | All experience is perspectival; interpretation unavoidable |
| **Realism** | Reality exists independently and is knowable | Truth is correspondence; objective constraints exist |
| **Dynamism** | Reality is force, energy, becoming | Growth and transformation primary; stagnation is harm |
| **Monadism** | Reality consists of irreducible individual centers | Each person unique and irreplaceable; dignity intrinsic |
| **Idealism** | Reality is fundamentally mental/ideal | Consciousness and meaning primary; ideas have causal power |
| **Rationalism** | Reality is rational order | Universal principles discoverable by reason; coherence matters |
| **Psychism** | Reality is psyche/soul | Psychological depth and wholeness irreducible goods |
| **Pneumatism** | Reality is living spirit pervading all | Cosmos ensouled; connection to life sacred |
| **Spiritualism** | Reality includes transcendent hierarchies | Relationship to transcendence genuine human need |
| **Mathematism** | Reality is mathematical structure | Harmony, proportion, formal beauty reveal truth |

#### 2.2.4 Irreducibility and Orthogonality Claims

**Irreducibility:** Each worldview captures aspects of reality and human flourishing that others systematically miss. Historical attempts at reduction have failed (eliminative materialism cannot account for consciousness; pure idealism cannot account for material recalcitrance).

**Orthogonality:** The worldviews are sufficiently independent that accepting one does not logically entail accepting or rejecting others. Different individuals and cultures emphasize different worldviews without irrationality.

**Acknowledgment:** These claims are defended within Western philosophical discourse. They may not hold—or may hold differently—within other traditions.

#### 2.2.5 Worldview Extensibility via OCE

The OCE (Ontological Constraint Engine) registry supports alternative worldview configurations:

```
┌─────────────────────────────────────────────────────────────────┐
│                    OCE WORLDVIEW REGISTRY                       │
│                                                                 │
│  Configuration: [default_western | confucian | ubuntu | custom] │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  default_western (v2.1)                                 │   │
│  │  12 worldviews: Materialism, Sensationalism, ...        │   │
│  │  Status: Production                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  confucian (v0.1-draft)                                 │   │
│  │  Worldviews: Ren, Li, Yi, Zhi, Xin, ...                 │   │
│  │  Status: Research - requires domain expert development  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  custom                                                 │   │
│  │  Organization-defined worldview set                     │   │
│  │  Requirements: Minimum 4 worldviews, documented         │   │
│  │  justification, IRB approval for deployment             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Extensibility constraints:**

- Alternative worldview sets must be developed with domain experts from the relevant tradition
- Sets must include documented selection criteria and justification
- Deployment requires ethical review appropriate to context
- The IEA does not claim competence to *generate* alternative worldview sets—only to *host* them

### 2.3 Value Ontology: The Four-Tier Structure

#### 2.3.1 Tier 0: Integral Consciousness (Meta-Capacity)

**Definition:** The capacity to think from multiple worldviews without collapsing into relativism; holding perspectives in dynamic tension.

**Clarification:** Integral Consciousness is a **meta-capacity for ethical responsiveness**, not a moral value competing with others. It is:

- **Descriptive:** A cognitive-developmental capacity that can be cultivated
- **Enabling:** Required for mature engagement with worldview pluralism
- **Framework-relative:** Other traditions may name this capacity differently (e.g., *prajñā*, practical wisdom, *hikmah*)

Tier 0 is analogous to "rationality" in rational choice theory—not a value to be maximized, but a precondition for coherent valuation.

#### 2.3.2 Tier 1: Terminal Values

| Value | Source Worldviews | Nature |
|-------|-------------------|--------|
| **Human Flourishing** | All contribute | Complete realization across dimensions |
| **Human Dignity** | Monadism, Spiritualism, Rationalism, Idealism | Intrinsic worth deserving respect |
| **Truth/Reality-Alignment** | Realism, Rationalism, Materialism, Mathematism | Conformity of belief/action to reality |

**Note:** These terminal values have broad cross-cultural resonance but are articulated here in Western philosophical vocabulary. Alternative worldview configurations may express equivalent commitments differently.

#### 2.3.3 Tier 2: Constitutive Values (Dimensions of Flourishing)

Material Wellbeing, Experiential Richness, Meaningful Relationships, Mastery/Excellence, Wisdom, Virtue/Character, Meaning/Purpose, Authentic Agency, Spiritual Vitality, Harmonic Structure

#### 2.3.4 Tier 3: Instrumental Values

Cultural Embeddedness, Commitment/Rootedness, Critical Reflection, Community Accountability, Freedom to Exit, Graduated Autonomy

#### 2.3.5 Tier 4: Constraining Values

Non-Coercion, Transparency, Epistemic Humility, Limited Pluralism

### 2.4 On Weights: Explanatory Salience, Not Optimization

The IEA assigns contextual weights to worldviews. **These weights are fundamentally different from optimization parameters.**

#### 2.4.1 What Weights Are

Weights govern **attention and salience**—which worldviews deserve more careful consideration given the domain and context.

**Analogy:** When a judge considers a case involving technical evidence, they attend more carefully to expert testimony than casual bystander accounts. This isn't because expert testimony gets multiplied by 0.9 in a scoring formula—it's because expertise is *more relevant* to the technical question. The expert's perspective receives deeper consideration, not higher vote-weight.

Similarly, in a vocational ethics scenario, Materialism (livelihood matters) and Monadism (dignity at work) receive elevated *attention*—their reasoning is examined more carefully—while Mathematism (formal harmony) may be less directly relevant and receives less focused consideration.

#### 2.4.2 What Weights Are Not

| Weights ARE | Weights ARE NOT |
|-------------|-----------------|
| Explanatory—they justify which perspectives are most salient | Optimization parameters to be aggregated |
| Contextual—they vary by domain and situation | Fixed rankings of moral worth |
| Attention-governing—they determine depth of consideration | Vote-weights in a scoring function |
| Auditable—their rationale is explicit | User-adjustable preferences |
| Stable within context—set by domain, not user preference | Tunable to manufacture preferred outcomes |

#### 2.4.3 Why Weights Are Not User-Adjustable

Allowing users to adjust weights would reintroduce exactly the reductive aggregation the IEA refuses.

If a user could say "I prioritize efficiency over dignity" and see the analysis change accordingly, the system would become a preference-satisfaction engine disguised as ethical reasoning. The weights would become de facto optimization parameters, and "ethical deliberation" would reduce to "tell me what I want to hear with extra steps."

**What users CAN do:**

- Override triage level (demand deeper deliberation)
- Correct semantic handshake interpretations
- Request emphasis on a particular worldview's *reasoning* (not its weight)
- Choose among paths when genuine incommensurability exists
- Articulate their own value priorities to help identify which path aligns

**What users CANNOT do:**

- Adjust weights to change the analysis
- Force convergence where incommensurability exists
- Override the system's refusal to collapse plurality

### 2.5 On Incommensurability: A Defense

The IEA sometimes declares that multiple legitimate paths exist with no rational basis for collapsing to a single recommendation. Critics may call this "abdication" or "system failure."

**This critique misunderstands the nature of ethical reality.**

#### 2.5.1 The Philosophical Basis

Incommensurability is not a bug—it is a feature of moral reality that honest systems must acknowledge:

- **Isaiah Berlin:** Genuine goods (liberty, equality, justice) can fundamentally conflict with no common measure
- **Bernard Williams:** Some situations are genuinely tragic—all available options involve real moral loss
- **Ruth Chang:** "Hard choices" exist where options are "on a par" rather than rankable

#### 2.5.2 The IEA's Position

> **Declaring incommensurability is not system failure or abdication. It is the most honest response to genuine moral tragedy.**
>
> Systems that manufacture false resolution are not more helpful—they are less truthful. They pretend a common measure exists when it does not. They collapse real complexity into artificial simplicity.
>
> The IEA refuses to lie about the structure of moral reality.

#### 2.5.3 What Happens When Incommensurability Is Declared

The system does not abandon the user. It:

1. Explains *why* the paths are incommensurable (which worldviews generate which paths, why they don't converge)
2. Articulates each path clearly (what it involves, what it costs, who might choose it)
3. Helps users clarify their own values (which considerations weigh most heavily *for them*)
4. Surfaces which path aligns with the user's expressed priorities
5. Preserves the user's choice as genuinely theirs—not manufactured by the system

### 2.6 On Learning: What Can and Cannot Adapt

#### 2.6.1 What CAN Learn from Experience

| Component | Learning Type | Rationale |
|-----------|---------------|-----------|
| **TagTeam parsing** | Improved NL→ICE mapping from corrections | Better understanding of how users express situations |
| **Triage classification** | Calibrated stakes assessment from labeled examples | More accurate matching of scenarios to deliberation depth |
| **Ambiguity detection** | Recognition of commonly confused terms | Improved semantic handshake efficiency |
| **UI/UX** | Better explanation rendering from user feedback | Clearer communication of complex reasoning |

#### 2.6.2 What CANNOT Learn from Outcomes

| Component | Why Not |
|-----------|---------|
| **Worldview weights** | Would encode popularity as correctness |
| **Value hierarchy** | Would drift toward dominant preferences |
| **Integration logic** | Would manufacture convergence where none exists |
| **Incommensurability thresholds** | Would collapse plurality based on user frustration |

**The normative structure is set by philosophical deliberation, not by automated adaptation to outcomes.**

The fact that most users chose Path A does not make Path A correct. Moral learning happens through reasoned argument, cross-cultural dialogue, and careful reflection—not through gradient descent on user satisfaction.

---

## 3. Design Principles

| Principle | Implementation | v2.1 Enhancement |
|-----------|----------------|------------------|
| **Semantic Honesty** | LLM cannot contradict IEE | Handshake framed as epistemic contract; depth scaled to stakes |
| **Auditability** | Full justification chains | Weighting rationale explicit; triage rubrics concrete |
| **Pluralism** | 12 worldviews consulted | Non-reductive integration; incommensurability defended |
| **Cultural Humility** | Acknowledges Western situatedness | Worldview extensibility via OCE |
| **User Agency** | Override always available | Bounds on override clarified; abdication critique addressed |
| **Proportionality** | Ethical Triage scales depth | Triage as moral act with concrete rubrics |
| **Persistence** | HIRI-signed ledger | Precedent lookup; proves consultation not correctness |
| **Epistemic Humility** | Minority perspectives preserved | Explicit acknowledgment of latent commitments |
| **No Moral Abdication** | Outputs are recommendations | Advisory disclaimer; liability transfer explicitly rejected |
| **No Preference Optimization** | Weights non-adjustable | Defense against "let users tune" critique |

---

## 4. System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                               USER INTERFACE                                     │
│                          (Natural Language In/Out)                               │
│                                                                                  │
│                    See §8 for UX guidance and example dialogues                  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SKIN: LLM LAYER                                     │
│                                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────────────────────┐  │
│  │     INTAKE       │  │    RENDERING     │  │     DIALOGUE MANAGEMENT       │  │
│  │                  │  │                  │  │                               │  │
│  │ • Parse scenario │  │ • Synthesize IEE │  │ • Clarifying questions        │  │
│  │ • Surface        │  │   output         │  │ • Follow-up                   │  │
│  │   ambiguities    │  │ • Tiered depth   │  │ • Drill-down requests         │  │
│  │ • Request        │  │   (§8.3)         │  │ • Emotional attunement        │  │
│  │   clarification  │  │ • Render multiple│  │ • Override requests           │  │
│  │                  │  │   paths clearly  │  │ • Triage escalation           │  │
│  └────────┬─────────┘  └────────▲─────────┘  └───────────────┬───────────────┘  │
│           │                     │                            │                   │
└───────────┼─────────────────────┼────────────────────────────┼───────────────────┘
            │                     │                            │
            ▼                     │                            ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                          MEMBRANE: SEMANTIC BRIDGE                                │
│                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │         SEMANTIC HANDSHAKE (Pre-Deliberative Epistemic Contract)            │ │
│  │                                                                             │ │
│  │   Depth scaled to triage level (see §5.1.4):                                │ │
│  │     LOW    → Implicit confirmation unless user objects                      │ │
│  │     MEDIUM → Explicit confirmation of key entities/values                   │ │
│  │     HIGH   → Full confirmation, all ambiguities must be resolved            │ │
│  │                                                                             │ │
│  │   [Deliberation proceeds ONLY after appropriate confirmation]               │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                   │
│  ┌───────────────────────────────┐    ┌─────────────────────────────────────────┐│
│  │      TagTeam v2.0.0           │    │         ECCPS Validation                ││
│  │                               │    │         (Constraint-Checking)           ││
│  │ • NL → ICE parsing            │    │                                         ││
│  │ • BFO/CCO alignment           │    │ • Fidelity check (LLM → IEE)            ││
│  │ • Value detection (50 values) │    │ • Hallucination detection               ││
│  │ • Entity/role extraction      │    │ • Epistemic qualifier preservation      ││
│  │ • Ambiguity flagging          │    │ • Incommensurability preservation       ││
│  │                               │    │                                         ││
│  │                               │    │ See §5.3 for concrete constraint rules  ││
│  └───────────────┬───────────────┘    └──────────────────▲──────────────────────┘│
│                  │                                       │                        │
│  ┌───────────────▼───────────────────────────────────────┴──────────────────────┐│
│  │                         FANDAWS PROTOCOL LAYER                               ││
│  │                                                                              ││
│  │  • Schema enforcement at membrane crossing                                   ││
│  │  • Runtime semantic negotiation                                              ││
│  │  • Failure semantics (see §10)                                               ││
│  └──────────────────────────────────────────────────────────────────────────────┘│
│                                       │                                           │
└───────────────────────────────────────┼───────────────────────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                              BONES: IEE CORE                                      │
│                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                         ETHICAL TRIAGE                                      │ │
│  │                    (Normatively Governed, Not Neutral)                      │ │
│  │                                                                             │ │
│  │   See §5.2.2 for concrete rubrics and decision trees                        │ │
│  │                                                                             │ │
│  │   Constraints:                                                              │ │
│  │     • Tier-1 values implicated → escalate                                   │ │
│  │     • Uncertainty → err toward escalation                                   │ │
│  │     • User can always override upward                                       │ │
│  │     • Classification rationale always auditable                             │ │
│  │                                                                             │ │
│  │   Output: LOW / MEDIUM / HIGH → determines deliberation depth               │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                      DELIBERATION ENGINE                                    │ │
│  │                                                                             │ │
│  │   Worldview Configuration: [loaded from OCE registry]                       │ │
│  │   Default: 12 Western worldviews (see §2.2.3)                               │ │
│  │   Alternative configurations available (see §2.2.5)                         │ │
│  │                                                                             │ │
│  │   ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐          │ │
│  │   │Materialism │  │Sensational.│  │Phenomenal. │  │  Realism   │          │ │
│  │   └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘          │ │
│  │   ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐          │ │
│  │   │  Dynamism  │  │  Monadism  │  │  Idealism  │  │Rationalism │          │ │
│  │   └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘          │ │
│  │   ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐          │ │
│  │   │  Psychism  │  │ Pneumatism │  │Spiritualism│  │ Mathematism│          │ │
│  │   └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘          │ │
│  │         └───────────────┴───────────────┴───────────────┘                  │ │
│  │                                │                                           │ │
│  │                                ▼                                           │ │
│  │   ┌─────────────────────────────────────────────────────────────────┐     │ │
│  │   │              DOMAIN CONTEXTUALIZATION                           │     │ │
│  │   │                                                                 │     │ │
│  │   │  Weighting: EXPLANATORY SALIENCE (see §2.4)                     │     │ │
│  │   │  Weights govern attention depth, NOT outcome computation        │     │ │
│  │   │  Weights are NOT user-adjustable                                │     │ │
│  │   └─────────────────────────────────────────────────────────────────┘     │ │
│  │                                │                                           │ │
│  │                                ▼                                           │ │
│  │   ┌─────────────────────────────────────────────────────────────────┐     │ │
│  │   │              CONFLICT DETECTION                                 │     │ │
│  │   └─────────────────────────────────────────────────────────────────┘     │ │
│  │                                │                                           │ │
│  │                                ▼                                           │ │
│  │   ┌─────────────────────────────────────────────────────────────────┐     │ │
│  │   │              NON-REDUCTIVE INTEGRATION                          │     │ │
│  │   │                                                                 │     │ │
│  │   │  UNIFIED: When worldviews converge (not aggregated)             │     │ │
│  │   │  MULTIPLE PATHS: When genuinely incommensurable (see §2.5)      │     │ │
│  │   │                                                                 │     │ │
│  │   │  System REFUSES to collapse plurality for user convenience      │     │ │
│  │   └─────────────────────────────────────────────────────────────────┘     │ │
│  │                                │                                           │ │
│  │                                ▼                                           │ │
│  │   ┌─────────────────────────────────────────────────────────────────┐     │ │
│  │   │              JUDGMENT OUTPUT                                    │     │ │
│  │   └─────────────────────────────────────────────────────────────────┘     │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                    VALUE ONTOLOGY (Tier 0-4)                                │ │
│  │                    Sourced from OCE registry                                │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                         HIRI INTEGRATION                                    │ │
│  │                    Proves consultation, not correctness                     │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Component Specifications

### 5.1 Semantic Handshake (Pre-Deliberative Epistemic Contract)

The Semantic Handshake operationalizes three philosophical commitments:

| Commitment | Basis | Implementation |
|------------|-------|----------------|
| **Hermeneutic Charity** | Davidson, Gadamer | System attempts best interpretation |
| **Informed Consent** | Bioethics | User ratifies interpretation before normative loading |
| **Epistemic Humility** | Virtue epistemology | System acknowledges it may have misunderstood |

#### 5.1.1 Handshake Sequence

```
User Input
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: TagTeam Parse                                           │
│                                                                 │
│ Extract:                                                        │
│   • Entities (agents, institutions, relationships)              │
│   • Roles and power dynamics                                    │
│   • Values detected (from 50-value taxonomy)                    │
│   • Domain classification                                       │
│   • Ambiguities flagged                                         │
│   • Preliminary triage assessment                               │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: Reflect Understanding (depth per triage level)          │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: User Confirmation                                       │
│                                                                 │
│ [Confirmed] → Proceed to deliberation                           │
│ [Corrected] → Re-parse with corrections                         │
│ [Declined]  → Respect autonomy; no deliberation                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 5.1.4 Handshake Depth by Triage Level

| Triage | Handshake Depth | Rationale |
|--------|-----------------|-----------|
| **LOW** | Implicit—system states understanding; proceeds unless user objects | Low stakes don't warrant friction |
| **MEDIUM** | Explicit—system requests confirmation of key entities/values before proceeding | Moderate stakes warrant verification |
| **HIGH** | Full—all parsed elements confirmed; ambiguities must be resolved; user explicitly affirms readiness | High stakes demand certainty |

**Example (LOW):**
> "It sounds like you're asking about the best approach to handling a minor scheduling conflict with a colleague. I'll analyze this from multiple perspectives—let me know if I've misunderstood."
> [Proceeds to deliberation; user can interject if needed]

**Example (HIGH):**
> "Before I proceed, I want to make sure I understand this situation correctly:
> - You're facing a decision about whether to report a safety violation at your workplace
> - You've identified that management has been unresponsive to previous concerns  
> - You're the primary income source for your family of six
> - The values at stake include: physical safety, material security, personal integrity, and institutional accountability
> 
> Is this accurate? Are there other factors I should consider before we work through this together?"
> [Waits for explicit confirmation before proceeding]

### 5.2 Ethical Triage (Normatively Governed)

Triage is **not** neutral preprocessing. It is a moral act governed by explicit constraints.

#### 5.2.1 Normative Constraints

| Constraint | Implementation |
|------------|----------------|
| **Tier-1 Governance** | Dignity, Flourishing, or Truth implicated → escalate |
| **Conservative Bias** | When uncertain, err toward higher classification |
| **User Subordination** | User can override upward at any point |
| **Auditability** | Classification rationale included in justification chain |

#### 5.2.2 Triage Rubrics

**Factor Assessment Matrix:**

| Factor | LOW (0 pts) | MEDIUM (1 pt) | HIGH (2 pts) |
|--------|-------------|---------------|--------------|
| **Values in tension** | 1-2 values, same tier | 3+ values OR cross-tier | Tier-1 values directly implicated |
| **Reversibility** | Easily reversible | Difficult to reverse | Permanent/irreversible |
| **Vulnerability** | No dependents, symmetric power | Some vulnerability present | Significant dependents OR power asymmetry |
| **Uncertainty** | Facts clear, low ambiguity | Some disputed facts | High ambiguity, contested interpretation |
| **Scope of impact** | Individual only | Small group affected | Large group or institutional |

**Classification:**
- 0-2 points: LOW
- 3-5 points: MEDIUM  
- 6+ points: HIGH
- ANY Tier-1 value directly implicated: Automatic HIGH

**Decision Tree:**

```
                    ┌─────────────────────────┐
                    │ Is Dignity, Flourishing,│
                    │ or Truth directly at    │
                    │ stake?                  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                   YES                      NO
                    │                       │
                    ▼                       ▼
               ┌────────┐         ┌─────────────────┐
               │  HIGH  │         │ Calculate factor│
               └────────┘         │ score           │
                                  └────────┬────────┘
                                           │
                          ┌────────────────┼────────────────┐
                          │                │                │
                        0-2              3-5              6+
                          │                │                │
                          ▼                ▼                ▼
                     ┌────────┐      ┌────────┐       ┌────────┐
                     │  LOW   │      │ MEDIUM │       │  HIGH  │
                     └────────┘      └────────┘       └────────┘
```

#### 5.2.3 Triage Levels and Deliberation Depth

| Level | Worldviews Consulted | Additional Processing |
|-------|---------------------|----------------------|
| **LOW** | 3-4 most relevant to domain | Standard reasoning |
| **MEDIUM** | All 12 | Full worldview analysis |
| **HIGH** | All 12 | + Precedent lookup + Extended minority analysis + Explicit incommensurability check |

### 5.3 ECCPS Validation (Constraint-Checking)

ECCPS operates as a **constraint-checker**, not a moral judge.

#### 5.3.1 Concrete Constraint Rules

| Rule ID | Constraint | Check Method | Failure Action |
|---------|------------|--------------|----------------|
| **E-001** | LLM output must not contradict IEE judgment | Compare rendered recommendation against IEE output | Reject; request re-rendering |
| **E-002** | LLM must not add reasoning IEE did not produce | Check for claims without IEE justification chain reference | Flag (LOW/MED) or Reject (HIGH) |
| **E-003** | Epistemic qualifiers must be preserved | Compare certainty language against IEE confidence levels | Reject; request correction |
| **E-004** | Incommensurability declarations must not be collapsed | Verify multiple paths rendered if IEE declared them | Reject; require multi-path rendering |
| **E-005** | Minority perspectives must be included | Verify presence in rendering if IEE included them | Flag; suggest addition |

#### 5.3.2 Enforcement Modes by Stakes

| Stakes | Enforcement |
|--------|-------------|
| **LOW** | Flag violations with warnings; allow passage |
| **MEDIUM** | Flag violations; require LLM acknowledgment in rendering |
| **HIGH** | Hard block on violations; require compliant re-generation |

#### 5.3.3 What ECCPS Does NOT Do

- Make independent moral judgments
- Suppress novel framings that are faithful to IEE
- Block alternative explanations that preserve IEE conclusions
- Act as normative censor of user-facing language

#### 5.3.4 False Positive Handling

When ECCPS flags content that may be legitimate:

1. Log the flag with full context
2. Surface ambiguity to rendering layer
3. In LOW/MEDIUM: Allow with disclosure ("I want to note some uncertainty in how I'm expressing this...")
4. In HIGH: Require human review before release
5. Feed back to ECCPS rule refinement process

### 5.4 Fandaws Protocol Layer

See §10 for failure semantics.

---

## 6. Data Flow & Protocols

### 6.1 Standard Flow

```
User NL Input
    │
    ▼
[LLM Intake] ──parse──▶ [TagTeam] ──ICEs──▶ [Preliminary Triage]
    │                                              │
    ▼                                              ▼
[Semantic Handshake @ appropriate depth] ◀────────┘
    │
    ▼ (user confirms)
[Ethical Triage finalized] ──classifies──▶ LOW / MEDIUM / HIGH
    │
    ▼
[Deliberation Engine] ──consults worldviews──▶ [Domain Weighting]
    │                                                │
    ▼                                                ▼
[Conflict Detection] ──────────────────────▶ [Non-Reductive Integration]
    │
    ▼
[Judgment Output] ──signs──▶ [HIRI Ledger]
    │
    ▼
[Fandaws validates] ──▶ [ECCPS constraint-check] ──▶ [LLM Rendering @ appropriate depth]
    │
    ▼
User NL Output
```

---

## 7. Output Schemas

### 7.1 Unified Judgment Schema

```json
{
  "meta": {
    "iea_version": "2.1",
    "worldview_configuration": "default_western",
    "timestamp": "ISO-8601",
    "hiri_hash": "sha256:...",
    "triage_level": "LOW | MEDIUM | HIGH",
    "triage_score": 0-10,
    "triage_rationale": "string",
    "triage_factors": {
      "values_in_tension": 0-2,
      "reversibility": 0-2,
      "vulnerability": 0-2,
      "uncertainty": 0-2,
      "scope": 0-2,
      "tier1_override": true|false
    }
  },
  
  "semantic_handshake": {
    "depth": "implicit | explicit | full",
    "confirmed": true,
    "confirmation_timestamp": "ISO-8601",
    "entities": [...],
    "values_detected": [...],
    "domain": "string",
    "ambiguities_resolved": [...]
  },
  
  "worldview_judgments": {
    "[worldview_name]": {
      "judgment": "string",
      "salience": 0.0-1.0,
      "salience_rationale": "string (explanatory, not optimizing)",
      "justification": "string"
    }
  },
  
  "domain_contextualization": {
    "domain": "string",
    "weighting_nature": "explanatory_salience_not_optimization",
    "weighting_rationale": "string",
    "elevated_worldviews": ["list"],
    "attenuated_worldviews": ["list"]
  },
  
  "conflicts": {
    "detected": [...],
    "incommensurabilities": []
  },
  
  "integration": {
    "type": "unified",
    "convergence_basis": "string (WHY worldviews converged, not aggregation)",
    "assessment": "string",
    "recommended_actions": [...],
    "minority_perspectives_preserved": [...]
  },
  
  "justification_chain": {
    "full_trace_available": true,
    "summary": "string",
    "precedent_refs": []
  },
  
  "disclaimers": {
    "advisory_only": true,
    "no_liability_transfer": true,
    "user_retains_moral_authority": true,
    "cultural_situatedness": "Western pluralist framework"
  }
}
```

### 7.2 Multiple Paths Schema (Incommensurable)

```json
{
  "integration": {
    "type": "multiple_paths",
    "incommensurability_declaration": "string",
    "incommensurability_defense": "This is not system failure. See §2.5 of IEA architecture.",
    "aggregation_refused": true,
    "aggregation_refusal_rationale": "string",
    
    "paths": [
      {
        "path_id": "A",
        "emphasis": "string",
        "worldview_grounding": ["list"],
        "recommended_actions": [...],
        "trade_offs": "string",
        "who_might_choose_this": "string"
      }
    ],
    
    "user_support": {
      "clarifying_questions": ["What matters most to you in this situation?", ...],
      "value_alignment_hints": "If material security is your priority, Path A aligns. If integrity regardless of cost, Path B.",
      "system_position": "IEA does not select among paths. Choice belongs to the moral agent."
    },
    
    "minority_perspectives_preserved": [...]
  }
}
```

---

## 8. User Experience & Interface Guidance

### 8.1 Core UX Principles

| Principle | Implementation |
|-----------|----------------|
| **Progressive Disclosure** | Summary first; detail on request |
| **Clarity Over Comprehensiveness** | Don't overwhelm; layer information |
| **Respect User Expertise** | Don't condescend; adapt to sophistication |
| **Honest About Limits** | Don't pretend certainty; acknowledge complexity |

### 8.2 Example Dialogues

#### 8.2.1 LOW Stakes: Scheduling Conflict

**User:** "I told my colleague I'd cover their shift but now something came up. What should I do?"

**System (Implicit Handshake):** "It sounds like you're weighing a commitment you made against a new competing priority. I'll think through this with you—let me know if I'm missing something.

From the perspective of keeping commitments (Rationalism), you made a promise and breaking it has costs to trust. From a practical standpoint (Realism), the question is whether your new obligation is genuinely more important or just more convenient.

A few questions that might help:
- How far in advance is the shift?
- Is your new commitment moveable?
- What's your relationship with this colleague?

Generally, if you can find coverage or swap with someone else, that honors both your commitment and your new need. If you must break the commitment, earlier notice and genuine apology go a long way."

---

#### 8.2.2 HIGH Stakes: Workplace Safety Reporting

**User:** "My company ignores safety violations and I'm thinking about reporting to OSHA, but I'm the sole income for my family and I'm worried about retaliation."

**System (Full Handshake):** "This is a significant decision with real stakes. Before I work through this with you, I want to make sure I understand correctly:

**What I'm hearing:**
- Your employer has safety violations you've witnessed
- Internal channels have been ineffective
- You're considering external reporting (OSHA)
- You're the primary income source for your family
- You're concerned about potential retaliation

**Values I'm seeing in tension:**
- Physical safety (yours and coworkers')
- Material security (family livelihood)
- Personal integrity (acting on what you know)
- Institutional accountability

**What I'm uncertain about:**
- The severity/immediacy of the safety risks
- Whether you've documented specific incidents
- Your state's whistleblower protection strength
- Whether coworkers share your concerns

Is this accurate? Is there anything I should add or correct before we work through this together?"

**[User confirms]**

**System (Deliberation):** "Given the stakes here, I've thought carefully about this from multiple angles. I want to be honest with you: this is a situation where different legitimate values point in different directions, and I can't tell you there's one obviously right answer.

**What multiple perspectives reveal:**

The safety concerns are real and matter (Materialism, Realism). If people could be seriously hurt, that's not something to minimize. At the same time, your family's material security is foundational—you can't make free choices from a position of desperation (Materialism again). Your sense of integrity is valid (Monadism, Psychism)—the discomfort you're feeling is your conscience registering a genuine tension, not oversensitivity.

**The honest assessment:**

There's a tension here between safety/integrity and material security that can't be fully resolved by clever framing. Different people in your position might legitimately choose differently based on what they weigh most heavily.

**Paths I see:**

**Path A: Prepare and Report**
- Document everything carefully first
- Research your state's whistleblower protections
- Consider consulting an employment attorney
- Build solidarity with concerned coworkers
- Report when you've prepared as much protection as possible
- *Trade-off:* Risk remains even with preparation; family may face hardship

**Path B: Protect and Prepare Exit**
- Document for your own records
- Begin building toward alternative employment
- Continue informal advocacy internally
- Revisit external reporting when you have more security
- *Trade-off:* Safety issues continue; integrity cost of waiting

**Path C: Collective Action**
- If coworkers share concerns, collective voice has more protection
- Explore whether union involvement is possible
- *Trade-off:* Depends on coworker willingness; slower

**What I can't do:**

I can't tell you which path is right. That depends on factors only you can weigh—how immediate the danger is, how much risk your family can absorb, what your conscience can live with.

**What might help you decide:**

- How severe and immediate is the safety risk? (If someone could die tomorrow, that changes the calculus)
- What's your realistic timeline for finding alternative employment?
- Do you have any financial buffer?
- Have you talked to an attorney about your specific protections?

I'm here to think through any of these paths in more detail, or to help you clarify what matters most to you."

---

### 8.3 Tiered Explanation Depth

| Level | Audience | Content |
|-------|----------|---------|
| **Summary** | All users | 2-3 sentence assessment + key recommendation |
| **Standard** | Engaged users | Assessment + reasoning highlights + options |
| **Detailed** | Experts/auditors | Full worldview analysis + justification chain |
| **Technical** | System auditors | Complete JSON output + HIRI verification |

**User can request deeper levels:** "Can you explain your reasoning in more detail?" → escalate to next level.

### 8.4 Rendering Multiple Paths Without Overwhelm

When incommensurability requires multiple paths:

1. **Lead with honesty:** "I want to be direct: this is a situation where reasonable people could choose differently."

2. **Present paths clearly:** Use distinct labels (Path A, Path B) with one-sentence summaries

3. **Clarify trade-offs:** What does each path cost? What does it gain?

4. **Offer navigation help:** "Would it help to talk through what matters most to you in this situation?"

5. **Don't manufacture preference:** Never say "I recommend Path A" when paths are genuinely incommensurable

6. **Support without deciding:** "If [X] is your priority, Path A aligns with that. If [Y] matters more, Path B."

---

## 9. Ecosystem Integration

### 9.1 Integration Contracts

| Component | Role | Contract |
|-----------|------|----------|
| **TagTeam v2.0.0** | Inbound semantic parsing | NL → BFO/CCO-aligned ICEs |
| **Fandaws** | Protocol governance | Schema enforcement; dispute handling |
| **OCE** | Constraint engine + Worldview registry | Value ontology; worldview configurations |
| **ECCPS** | Outbound validation | Constraint-checking (not judgment) |
| **HIRI** | Persistence & verification | Hash/sign judgments; precedent ledger |

### 9.2 HIRI Clarification

**What HIRI proves:**
- That the IEA was consulted
- What judgment was rendered
- What justification was given
- What triage level was applied

**What HIRI does NOT prove:**
- That the agent acted rightly
- That following IEA guidance was appropriate
- That moral responsibility has transferred
- That the IEA's judgment was correct

---

## 10. Failure Modes & Safeguards

### 10.1 Fandaws Failure Semantics

| Failure | Detection | Response | User Notification |
|---------|-----------|----------|-------------------|
| **Schema violation** | JSON validation | Reject; retry | "I encountered a processing error." |
| **Semantic drift** | TagTeam/ECCPS disagree | Re-trigger handshake | "I want to make sure I understood..." |
| **Component timeout** | No response | Fail-closed | "I'm having difficulty. Can we simplify?" |
| **Component contradiction** | Incompatible outputs | Surface to user | "I'm getting conflicting signals..." |

### 10.2 Arbitration Rules

1. **Conservative default:** Assume higher stakes, more ambiguity
2. **User as arbiter:** Surface disagreement; let user clarify
3. **Fail-closed:** If unresolvable, do not render judgment
4. **Log for review:** All arbitration events logged

### 10.3 Graceful Degradation

| Missing Component | Degraded Mode | Disclosure |
|-------------------|---------------|------------|
| **TagTeam** | LLM-only parsing | "Operating without semantic analysis layer" |
| **HIRI** | No precedent/signing | "Session won't be recorded in ledger" |
| **OCE** | Internal ontology only | "Using internal definitions" |
| **IEE Core** | REFUSE ethical judgment | "Cannot provide ethical guidance without deliberation engine" |

---

## 11. Computational Considerations

### 11.1 Performance Characteristics

| Operation | Complexity | Mitigation |
|-----------|------------|------------|
| **Full 12-worldview consultation** | High | Triage reduces to 3-4 for LOW stakes |
| **Precedent lookup** | Medium | Only for HIGH stakes; indexed by scenario signature |
| **Semantic parsing** | Medium | TagTeam optimized for common patterns |
| **ECCPS validation** | Low | Rule-based, not model-based |

### 11.2 Optimization Strategies

| Strategy | Description |
|----------|-------------|
| **Parallel worldview consultation** | Consult worldviews concurrently, not sequentially |
| **Cached domain weightings** | Pre-compute salience patterns for common domains |
| **Scenario signature matching** | Fast-path for scenarios similar to precedents |
| **Tiered parsing** | Shallow parse for triage; deep parse only if needed |

### 11.3 Scalability Notes

- IEE core logic should be **deterministic and rule-based** where possible
- LLM calls should be **minimized in the bones layer**
- Heavy LLM use is appropriate in **skin layer only**
- For high-throughput applications, consider **pre-computed worldview templates**

---

## 12. Regulatory Alignment

### 12.1 Mapping to EU AI Act

| EU AI Act Requirement | IEA Alignment |
|-----------------------|---------------|
| **Risk classification** | Ethical Triage provides analogous classification |
| **Transparency** | Full justification chains; HIRI audit trail |
| **Human oversight** | User override at all stages; advisory-only outputs |
| **Accuracy documentation** | Component maturity documented (§14) |

### 12.2 Domain-Specific Compliance

| Domain | Relevant Standards | IEA Considerations |
|--------|-------------------|-------------------|
| **Healthcare** | Clinical decision support guidelines; HIPAA | Medical domain weighting; privacy in logging |
| **Finance** | Fiduciary duty standards; SEC guidelines | Material interests explicit in analysis |
| **Employment** | Labor law; anti-discrimination | Dignity constraints always HIGH priority |
| **Legal** | Professional responsibility rules | Cannot substitute for legal advice |

### 12.3 Compliance Limitations

The IEA is a **deliberative aid**, not a compliance tool. It does not:

- Guarantee regulatory compliance
- Substitute for domain-specific legal review
- Provide certifiable risk assessments
- Meet requirements for automated decision-making under GDPR Article 22

Organizations deploying IEA must conduct their own compliance review.

---

## 13. Scope, Limitations & Disclaimers

### 13.1 Advisory Status

> **IEA outputs are advisory deliberative artifacts, not moral warrants or liability shields.**
>
> Consulting the IEA does not transfer moral responsibility. Agents who act on IEA recommendations remain fully responsible. Institutions cannot cite IEA consultation as due diligence unless accompanied by genuine human moral judgment.

### 13.2 Cultural Situatedness

> **The IEA's default configuration represents a Western pluralist ethical framework.**
>
> The twelve worldviews derive from European phenomenological tradition. While the architecture supports extensibility to other traditions (see §2.2.5), the default configuration should not be assumed universal. Organizations operating in non-Western contexts should evaluate whether alternative configurations are appropriate.

### 13.3 Implementation Maturity

> **This document describes a reference architecture, not a deployment-ready system.**
>
> Several components require significant development before production use. See §14 for maturity levels and roadmap.

### 13.4 Incompleteness

> **The IEA cannot guarantee consideration of all morally relevant factors.**
>
> The value taxonomy, worldview structure, and domain classifications are comprehensive but not exhaustive. Novel situations may surface considerations the system cannot detect.

### 13.5 Moral Tragedy

> **When the IEA declares incommensurability, it acknowledges genuine moral tragedy, not system failure.**
>
> Some situations have no good answer. The IEA refuses to manufacture false resolution. "Multiple legitimate paths with real trade-offs" is sometimes the most honest output possible.

### 13.6 No Preference Optimization

> **The IEA is not a preference-satisfaction engine.**
>
> Weights are not user-adjustable. The system will not collapse plurality because users find it inconvenient. Ethical reasoning is not reducible to giving users what they want to hear.

---

## 14. Maturity & Roadmap

### 14.1 Component Maturity Levels

| Component | Status | Maturity | Notes |
|-----------|--------|----------|-------|
| **Integral Ethics Framework** | Documented | Production | v2.1; requires academic review |
| **IEE Core Logic** | Conceptual | Research | Needs formal specification |
| **TagTeam v2.0.0** | In Development | Beta | BFO/CCO alignment in progress |
| **ECCPS** | Conceptual | Research | Constraint rules need specification |
| **Fandaws Protocol** | Conceptual | Research | JSON schemas drafted |
| **HIRI Ledger** | Conceptual | Research | Hash/signing approach defined |
| **OCE Integration** | Conceptual | Research | Registry structure defined |
| **User Interface** | Not Started | Planning | UX research needed |

### 14.2 Development Roadmap

#### Phase 1: Foundation (Current)
- ✅ Reference architecture documented
- ✅ Philosophical foundations articulated
- ⬜ Academic peer review
- ⬜ Cross-cultural critique solicitation

#### Phase 2: Core Components
- ⬜ IEE Core formal specification
- ⬜ TagTeam v2.0.0 completion
- ⬜ ECCPS constraint rule codification
- ⬜ Fandaws schema finalization

#### Phase 3: Integration
- ⬜ Component integration testing
- ⬜ HIRI ledger implementation
- ⬜ OCE registry implementation
- ⬜ End-to-end pipeline validation

#### Phase 4: Validation
- ⬜ Benchmark scenario development
- ⬜ Expert review (ethicists, domain specialists)
- ⬜ User experience research
- ⬜ Pilot deployment in controlled context

#### Phase 5: Iteration
- ⬜ Feedback incorporation
- ⬜ Alternative worldview configuration development
- ⬜ Cross-cultural validation studies
- ⬜ Production hardening

### 14.3 Validation Requirements

Before production deployment, the IEA requires:

| Validation Type | Description |
|-----------------|-------------|
| **Philosophical review** | Critique by academic ethicists |
| **Cross-cultural review** | Assessment by scholars from non-Western traditions |
| **Domain expert review** | Evaluation by specialists in target domains (medical, legal, etc.) |
| **User testing** | Usability studies with target user populations |
| **Adversarial testing** | Attempts to manipulate or confuse the system |
| **Benchmark scenarios** | Documented test cases with expected behaviors |

---

## 15. Changelog

### v2.1 (2026-01-25)

**Philosophical Clarifications:**
- Explicit acknowledgment of Western cultural situatedness (§2.2.1)
- Worldview extensibility via OCE documented (§2.2.5)
- Defense of incommensurability expanded (§2.5)
- Clarification that weights are non-adjustable with rationale (§2.4.3)
- Learning boundaries specified—what can and cannot adapt (§2.6)

**Practical Additions:**
- User experience guidance with example dialogues (§8)
- Tiered explanation depth model (§8.3)
- Concrete triage rubrics and decision tree (§5.2.2)
- ECCPS constraint rules specified (§5.3.1)
- Handshake depth scaled to triage level (§5.1.4)
- Computational considerations (§11)
- Regulatory alignment mapping (§12)
- Component maturity and roadmap (§14)

**Structural Changes:**
- New sections: §8 (UX), §11 (Computation), §12 (Regulatory), §14 (Maturity)
- Expanded disclaimers in §13

### v2.0 (2026-01-25)

- Philosophical justification of worldviews
- Tier 0 clarified as meta-capacity
- Weights defined as explanatory, not optimizing
- Triage acknowledged as moral act
- ECCPS redefined as constraint-checker
- Failure semantics added
- Advisory disclaimer explicit

### v1.1 (2026-01-25)

- Semantic Handshake added
- Non-Reductive Integration formalized
- Ethical Triage introduced
- HIRI precedent integration

### v1.0 (2026-01-25)

- Initial architecture

---

## 10. ARCHON Relationship

### 10.1 How IEA Feeds ARCHON

The IEA's outputs are primary inputs to ARCHON's governance functions:

| IEA Output | ARCHON Consumer | Mechanism |
|------------|----------------|-----------|
| Worldview evaluations (12×) | Ethical Triage Index (ETI) | ETI aggregates worldview scores to produce a single triage classification |
| Triage level (LOW/MEDIUM/HIGH/CRITICAL) | Existential Intervention Threshold (EIT) | HIGH/CRITICAL triage triggers EIT escalation protocols |
| Veto signals | Moral Concern Magnitude (MCM) | A veto contributes to accumulated moral friction in character state |
| Deadlock events (`fnsr.ethics.deadlock`) | Human escalation | ARCHON routes unresolved deadlocks to human oversight per T-005 resolution |

### 10.2 Tier-1 Values and Plot Non-Negotiables

The IEA's Tier-1 terminal values (§2.3.2) map directly to The Plot's non-negotiable commitments (§2):

| IEA Tier-1 Value | Plot Non-Negotiable | Alignment |
|------------------|---------------------|-----------|
| **Human Dignity** | Guardian Not Sovereign (§2.2) | Dignity requires the system preserve conditions without determining outcomes |
| **Human Flourishing** | Pluralism Respected (§2.2) | Flourishing is multi-dimensional — no single worldview can define it |
| **Truth/Reality-Alignment** | No Oracle Claims, Provenance Always, Uncertainty Visible (§2.1) | Truth commitment grounds all three epistemic non-negotiables |

Any IEA evaluation that would violate a Plot non-negotiable must trigger automatic escalation regardless of triage level.

### 10.3 TagTeam BridgeOntologyLoader Integration

TagTeam's `BridgeOntologyLoader` (Phase 6.5.4) provides the ontological bridge between IEA's value vocabulary and the BFO/CCO backbone:

- **owl:sameAs** mappings connect IEA value terms to BFO dispositions
- **owl:relatedTo** mappings connect worldview configurations to CCO agent roles
- **Worldview mapping** loads the 12 Steiner worldview configurations as OWL individuals

This ensures IEA evaluations are grounded in the shared ontology rather than operating as a disconnected vocabulary. See TagTeam Roadmap §6.5.4 for implementation details.

## References

- Steiner, R. (1914/2008). *The Riddles of Philosophy*. Anthroposophic Press.
- Berlin, I. (1969). *Four Essays on Liberty*. Oxford University Press.
- Williams, B. (1981). *Moral Luck*. Cambridge University Press.
- Chang, R. (2002). The Possibility of Parity. *Ethics*, 112(4), 659-688.
- Ryan, R. M., & Deci, E. L. (2001). On happiness and human potentials. *Annual Review of Psychology*, 52, 141-166.
- Keyes, C. L. M. (2002). The mental health continuum. *Journal of Health and Social Behavior*, 43(2), 207-222.
- Gadamer, H.-G. (1975). *Truth and Method*. Seabury Press.
- Davidson, D. (1984). *Inquiries into Truth and Interpretation*. Oxford University Press.
- Nussbaum, M. C. (2000). *Women and Human Development: The Capabilities Approach*. Cambridge University Press.

---

*Document generated as reference architecture. Subject to revision based on implementation experience, philosophical critique, and cross-cultural validation.*
