# The Witness Architecture

**AI as Accountability Infrastructure, Not Decision Replacement**

| Field | Value |
|-------|-------|
| Version | 1.1 |
| Status | Foundational Specification |
| Author | Aaron Erickson |
| Date | 2026-01-31 |
| Supersedes | v1.0 |

---

## Preamble

This document defines a philosophical and architectural framework for artificial intelligence systems that serve human institutions without replacing human judgment.

The core premise is simple: **AI should be a witness to human decisions, not a substitute for them.**

This is not a limitation born of technical inadequacy. It is a design principle born of institutional reality: when decisions disappear into organizational fog, accountability disappears with them. AI systems that "make decisions" allow humans to evade responsibility. AI systems that *witness* decisions make responsibility permanent.

The Witness Architecture does not prevent humans from making bad decisions. It prevents humans from pretending they didn't make them.

---

## Document Scope

This specification addresses the practical implementation of witnessed accountability in enterprise AI systems. It is intended for technical architects, governance officers, legal counsel, and operational leadership.

A companion document, *"Toward Synthetic Moral Agency: The Witness as Precursor,"* addresses the longer-term philosophical trajectory of this work. That document is appropriate for strategic planning and research contexts but is not required for implementation of the Witness Architecture itself.

---

## Part I: The Problem

### 1.1 The Accountability Gap

Modern institutions suffer from a fundamental accountability gap: decisions are made, but no one is responsible for them.

This gap emerges from institutional structures designed to diffuse responsibility:

- "The committee approved it"
- "It went through the normal process"
- "Leadership signed off"
- "The system recommended it"

Each of these phrases represents a decision that was made by humans but attributed to abstractions. The committee is not a person. The process is not a person. Leadership is not a person. The system is not a person.

When things go wrong, these abstractions absorb blame that should attach to individuals. The humans who actually decided are protected by institutional fog.

### 1.2 How AI Makes It Worse

The current trajectory of AI deployment deepens this accountability gap.

When organizations say they want AI to "make decisions," they are often saying they want decisions to happen without any human being accountable for them. The AI becomes the ultimate abstraction—a non-person that can be blamed for anything.

Consider the language:

- "The AI approved the loan"
- "The algorithm flagged the transaction"
- "The model recommended termination"

In each case, a consequential decision affecting human lives is attributed to a system that cannot be held responsible. The humans who built, deployed, configured, and relied upon that system recede into the background.

This is not a bug. For many institutional actors, it is the primary feature. AI offers the promise of decisions without deciders, actions without actors, consequences without accountability.

### 1.3 The Director's Question

When institutional leaders ask "What's the point of AI if humans are still the bottleneck?", they are revealing the true demand signal: they want to remove humans from the decision path so that decisions can happen faster and no human bears responsibility for them.

This demand is understandable from an institutional perspective. Human judgment is slow, expensive, and inconsistent. Humans who make decisions can be blamed, sued, fired, and imprisoned. Removing humans from decisions removes all of these problems.

But it creates a larger problem: decisions are being made that affect human lives, and no one is accountable for them. The institution becomes a machine for producing consequences without responsibility.

### 1.4 The Alternative

The Witness Architecture proposes a different role for AI: not as a decision-maker that replaces human judgment, but as a witness that makes human judgment undeniable.

A witness does not decide. A witness observes, records, and attests. A witness ensures that what happened cannot later be denied or obscured.

In the Witness Architecture:

- Humans make decisions
- AI witnesses those decisions
- The witness record is permanent, attributed, and tamper-evident
- No human can later claim "I didn't decide" or "I didn't understand"

This does not slow down good-faith decision-making. It slows down bad-faith evasion of responsibility. That is the point.

---

## Part II: The Architecture

### 2.1 Core Principles

The Witness Architecture rests on five principles:

**Principle 1: Decisions Require Deciders**

Every action that affects the world must trace to a natural person who authorized it. "The organization decided" is not valid. "The system decided" is not valid. Only "Jane Smith decided, at this time, with this understanding" is valid.

**Principle 2: Understanding Must Be Attested**

Authorization without understanding is not authorization—it is rubber-stamping. The witness records not only that a human authorized an action, but what they attested to understanding when they authorized it.

**Principle 3: The Record Is Permanent**

Witness records cannot be deleted, modified, or anonymized. The human who decided is permanently associated with the decision. This is not punitive; it is structural. Accountability requires memory.

**Principle 4: Evasion Is Visible**

When humans attempt to evade the witness—by rushing approvals, by rubber-stamping, by claiming authority they don't have—the witness records the evasion. The system does not prevent evasion; it makes evasion undeniable.

**Principle 5: The Witness Has Standing**

The witness is not merely a logging system. It is an entity with standing to attest. Its records are designed to be admissible, auditable, and legally significant. The witness can be called upon to testify to what it observed.

### 2.2 Architectural Components

The Witness Architecture comprises four components:

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE WITNESS ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   CAPABLE    │    │   WITNESS    │    │  ATTESTED    │       │
│  │   SYSTEMS    │───▶│    LAYER     │───▶│   RECORD     │       │
│  │              │    │              │    │              │       │
│  │ (SFS, APIs,  │    │ (Observes,   │    │ (Permanent,  │       │
│  │  Tools)      │    │  Records,    │    │  Attributed, │       │
│  │              │    │  Attests)    │    │  Immutable)  │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         ▲                   ▲                                    │
│         │                   │                                    │
│         │            ┌──────────────┐                           │
│         │            │    HUMAN     │                           │
│         └────────────│   DECIDER    │                           │
│                      │              │                           │
│                      │ (Authorizes, │                           │
│                      │  Attests,    │                           │
│                      │  Bears       │                           │
│                      │  Responsibility)                         │
│                      └──────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Capable Systems:** The tools, functions, and services that can affect the world. These systems are capable but not authorized. They can do things, but they cannot decide to do things.

**Human Decider:** The natural person who authorizes actions. The decider bears responsibility for what they authorize. They cannot delegate this responsibility to a system, a role, or an abstraction.

**Witness Layer:** The AI component that observes human authorization, records what was understood and decided, and attests to the record. The witness does not approve or reject—it observes and records.

**Attested Record:** The permanent, immutable record of decisions. Each record includes who decided, what they authorized, what they attested to understanding, and when the decision was made.

### 2.3 The Witness Record Schema

Every witnessed decision produces an Attested Record:

```yaml
AttestedRecord:
  # Unique, permanent identifier
  record_id: "WR-2026-0131-00421"
  
  # What was witnessed
  witnessed_event:
    type: "authorization"
    action_authorized: "Execute function EvaluatePerformance"
    scope: 
      parameters:
        evaluation_period: "Q4-2025"
      # PII references use pseudonymous identifiers (see Section 2.5)
      subject_reference: "PNYM-EMP-a8f2c9b1"
    capable_system: "APQC-SFS-Executor v2.0"
    risk_tier: "standard"  # See Section 2.6 for tiering
  
  # Who decided (pseudonymized for storage, resolvable for audit)
  decider:
    # Pseudonymous identifier, resolvable through Identity Resolution Service
    pseudonym: "PNYM-DCR-7e3d1a4f"
    
    # Identity verification method (not the identity itself)
    verification_method: "SSO authentication + MFA"
    verification_timestamp: "2026-01-31T14:30:00Z"
    
    # The authority they claimed (role, not person)
    claimed_authority: "Authorized to initiate performance evaluations for direct reports"
  
  # What they attested to understanding
  attestations:
    - attestation_id: "ATT-001"
      statement: "I understand this action will create a permanent performance record for the identified employee"
      attested_at: "2026-01-31T14:30:15Z"
      
    - attestation_id: "ATT-002"
      statement: "I understand I am personally responsible for the accuracy of inputs I have provided"
      attested_at: "2026-01-31T14:30:18Z"
      
    - attestation_id: "ATT-003"
      statement: "I have reviewed the employee's metrics and believe this evaluation is warranted"
      attested_at: "2026-01-31T14:30:22Z"
  
  # Evidence of genuine engagement (see Section 2.7 for methodology)
  engagement_evidence:
    engagement_score: 0.82  # Composite score, see Section 2.7
    tier_required_score: 0.70  # Based on risk tier
    evidence_components:
      - type: "time_on_screen"
        value_seconds: 147
        weight: 0.3
      - type: "scroll_depth"
        value_percentage: 94
        weight: 0.2
      - type: "material_access"
        materials_accessed: 2
        materials_available: 3
        weight: 0.3
      - type: "attestation_pacing"
        mean_interval_seconds: 4.2
        variance: 1.8
        weight: 0.2
    flags:
      - none  # Would include "rapid_attestation", "no_material_access", etc.
  
  # The witness attestation
  witness_attestation:
    witness_system: "Witness Layer v1.1"
    witness_statement: |
      I, the Witness system, attest that on 2026-01-31 at 14:30:22 UTC,
      a verified human decider (pseudonym PNYM-DCR-7e3d1a4f) authorized 
      the action described above.
      The decider made the attestations listed above.
      Engagement evidence yielded a score of 0.82 (threshold: 0.70).
      This record is permanent and will not be modified.
      The decider's identity is resolvable through the Identity Resolution 
      Service for authorized audit purposes.
    attestation_timestamp: "2026-01-31T14:30:23Z"
    cryptographic_seal: "sha256:a3f2b8c9..."
  
  # Immutability and compliance metadata
  record_metadata:
    storage_classification: "accountability_record"
    retention_policy: "permanent_pseudonymized"
    gdpr_status: "compliant_via_pseudonymization"
    resolution_authority: "Identity Resolution Service"
```

### 2.4 What the Witness Does Not Do

The Witness Architecture is defined as much by what it refuses to do as by what it does:

**The witness does not decide.**

The witness observes human decisions. It does not make decisions itself, recommend decisions, or evaluate whether decisions are good or bad. The quality of the decision is the human's responsibility.

**The witness does not prevent.**

The witness does not stop humans from making bad decisions, unethical decisions, or illegal decisions. It records that they made them. Prevention is a different architectural concern; the witness is concerned with accountability, not control.

**The witness does not advise.**

The witness does not tell humans what they should decide. Advisory systems are valuable, but they are separate from the witness function. Combining advice and witness creates conflicts of interest—the system that advised a decision should not also be the system that records whether the human understood it.

**The witness does not forgive.**

The witness record is permanent. There is no process for removing an attested decision from the record. Humans who make decisions must live with the permanent record of having made them. This is the cost of authority.

**The witness does not judge.**

The witness records what happened. It does not determine liability, assign blame, or adjudicate disputes. Those functions belong to humans and human institutions. The witness provides the evidentiary foundation for judgment; it does not judge.

### 2.5 Privacy-Preserving Accountability (GDPR Compliance)

The Witness Architecture must reconcile two requirements that appear to conflict:

- **Accountability permanence:** Decisions must be permanently attributed to deciders
- **Privacy rights:** Individuals have rights to erasure under GDPR and similar regulations

The resolution is **pseudonymization with controlled resolution**:

```yaml
IdentityResolutionService:
  purpose: |
    Maintains the mapping between pseudonymous identifiers in Witness Records
    and actual identities. Enables accountability while preserving privacy.
    
  architecture:
    witness_records:
      contain: "pseudonymous identifiers only"
      contain_not: "names, emails, or direct identifiers"
      
    resolution_service:
      maintains: "pseudonym-to-identity mappings"
      access_control: "authorized auditors only"
      jurisdiction_aware: true
      
  gdpr_compliance:
    right_to_erasure:
      applies_to: "identity resolution mappings"
      applies_not_to: "witness records themselves"
      effect: |
        When a subject exercises right to erasure, their identity mapping
        is removed from the Resolution Service. The Witness Record remains
        (preserving the fact that A DECISION WAS MADE) but the pseudonym
        becomes unresolvable (protecting WHO MADE IT from casual access).
        
    lawful_basis_for_retention:
      witness_records: "legitimate interest in accountability"
      identity_mappings: "consent or contractual necessity"
      
    resolution_after_erasure:
      standard_audit: "pseudonym unresolvable, decision record intact"
      legal_compulsion: |
        Court order can compel identity reconstruction through
        alternative means (system logs, authentication records).
        The Witness Record provides the decision evidence;
        identity reconstruction is a separate legal process.
        
  data_subject_rights:
    access: "Subject can see their own pseudonymized records"
    portability: "Subject can export their decision history"
    erasure: "Subject can request mapping deletion (not record deletion)"
    objection: "Subject cannot object to witnessing of their authorized decisions"
```

**Key Insight:** The Witness Record answers "what decision was made, when, and with what understanding." The Identity Resolution Service answers "who made it." By separating these, we can preserve accountability (the decision happened) while respecting privacy (who made it is access-controlled and erasable).

**For Corporate Deciders:** Employees making decisions in their corporate capacity typically cannot exercise personal erasure rights over business decisions. The employment contract establishes the lawful basis for retaining accountability records. Erasure rights apply primarily to personal data incidentally captured, not to the accountability record itself.

### 2.6 Risk-Tiered Witnessing

Not every decision requires the same level of witnessing. The Witness Architecture implements risk-tiered witnessing to balance accountability with operational efficiency.

```yaml
WitnessingTiers:
  # Tier 0: Observational Only
  tier_0_observational:
    name: "Observational"
    description: "Low-risk, high-volume, easily reversible actions"
    examples:
      - "View a record"
      - "Generate a report"
      - "Query system status"
    witnessing_mode: "batch"
    engagement_required: false
    attestation_required: false
    record_granularity: "session_summary"
    typical_volume: "unlimited"
    
  # Tier 1: Lightweight Witnessing
  tier_1_lightweight:
    name: "Lightweight"
    description: "Routine actions with limited consequence"
    examples:
      - "Update non-critical metadata"
      - "Approve routine expense under threshold"
      - "Schedule standard meeting"
    witnessing_mode: "batch_with_attestation"
    engagement_required: false
    attestation_required: true
    attestation_type: "batch_acknowledgment"
    record_granularity: "action_group"
    batch_limit: 20
    typical_volume: "50-100 per hour"
    
  # Tier 2: Standard Witnessing
  tier_2_standard:
    name: "Standard"
    description: "Consequential but routine decisions"
    examples:
      - "Approve expense over threshold"
      - "Initiate performance review"
      - "Authorize data access"
    witnessing_mode: "individual"
    engagement_required: true
    engagement_threshold: 0.70
    attestation_required: true
    attestation_type: "specific_statements"
    record_granularity: "individual_action"
    typical_volume: "10-20 per hour"
    
  # Tier 3: Enhanced Witnessing
  tier_3_enhanced:
    name: "Enhanced"
    description: "High-stakes decisions with significant impact"
    examples:
      - "Terminate employment"
      - "Approve large contract"
      - "Override compliance control"
    witnessing_mode: "individual_enhanced"
    engagement_required: true
    engagement_threshold: 0.85
    attestation_required: true
    attestation_type: "specific_statements_with_rationale"
    additional_requirements:
      - "must_document_rationale"
      - "must_acknowledge_alternatives_considered"
    record_granularity: "individual_action_with_context"
    cooling_period_minutes: 5  # Forced delay before execution
    typical_volume: "5-10 per hour maximum"
    
  # Tier 4: Critical Witnessing  
  tier_4_critical:
    name: "Critical"
    description: "Irreversible or organization-defining decisions"
    examples:
      - "Authorize mass layoff"
      - "Approve merger transaction"
      - "Override safety system"
    witnessing_mode: "individual_critical"
    engagement_required: true
    engagement_threshold: 0.95
    attestation_required: true
    attestation_type: "comprehensive_with_legal_acknowledgment"
    additional_requirements:
      - "must_document_rationale"
      - "must_acknowledge_alternatives_considered"
      - "must_confirm_legal_review"
      - "requires_co-authorization"  # Second authorized human
    record_granularity: "individual_action_with_full_context"
    cooling_period_minutes: 60  # One hour delay minimum
    typical_volume: "limited by organizational capacity"

TierAssignment:
  method: "policy_driven_with_override"
  
  default_assignment:
    source: "action_risk_classification_policy"
    maintained_by: "governance_committee"
    review_frequency: "quarterly"
    
  dynamic_adjustment:
    # System can elevate tier based on context
    elevation_triggers:
      - condition: "action_affects_more_than_100_subjects"
        elevation: "+1 tier"
      - condition: "action_is_first_of_type_for_decider"
        elevation: "+1 tier"  
      - condition: "action_occurs_outside_business_hours"
        elevation: "+1 tier"
      - condition: "decider_has_recent_elevated_error_rate"
        elevation: "+1 tier"
        
    # System cannot lower tier, only elevate
    lowering_permitted: false
```

**Key Insight:** Tiered witnessing acknowledges that not every action needs a 30-second engagement check. Routine actions can be batch-witnessed. Critical actions require enhanced scrutiny. The tier is assigned by policy, not by the decider—deciders cannot choose lighter witnessing for their own actions.

### 2.7 Engagement Verification (Beyond Time-on-Screen)

The critique correctly identified that time-on-screen is gameable. Version 1.1 implements a composite engagement score using multiple signals:

```yaml
EngagementVerification:
  purpose: |
    Detect genuine human engagement versus mechanical compliance.
    No single metric is sufficient; composite scoring resists gaming.
    
  scoring_methodology:
    composite_score:
      range: 0.0 to 1.0
      threshold_by_tier:
        tier_1: 0.50
        tier_2: 0.70
        tier_3: 0.85
        tier_4: 0.95
        
    components:
      - name: "temporal_engagement"
        weight: 0.25
        signals:
          - metric: "time_on_authorization_screen"
            interpretation: "Minimum time indicates reading"
            gaming_resistance: "low"  # Can wait passively
          - metric: "time_distribution_across_sections"
            interpretation: "Even distribution suggests systematic review"
            gaming_resistance: "medium"
          - metric: "return_visits_to_sections"
            interpretation: "Re-reading suggests genuine consideration"
            gaming_resistance: "high"
            
      - name: "content_interaction"
        weight: 0.30
        signals:
          - metric: "scroll_depth_percentage"
            interpretation: "Scrolled through full content"
            gaming_resistance: "medium"
          - metric: "scroll_velocity_variance"
            interpretation: "Variable speed suggests reading vs. rapid scroll"
            gaming_resistance: "high"
          - metric: "text_selection_events"
            interpretation: "Selecting text suggests close reading"
            gaming_resistance: "high"
          - metric: "zoom_or_expand_events"
            interpretation: "Enlarging content suggests engagement"
            gaming_resistance: "high"
            
      - name: "material_access"
        weight: 0.25
        signals:
          - metric: "supporting_documents_opened"
            interpretation: "Accessed available evidence"
            gaming_resistance: "medium"
          - metric: "time_in_supporting_documents"
            interpretation: "Actually reviewed evidence"
            gaming_resistance: "medium"
          - metric: "cross_reference_pattern"
            interpretation: "Moved between decision screen and evidence"
            gaming_resistance: "high"
            
      - name: "attestation_behavior"
        weight: 0.20
        signals:
          - metric: "attestation_pacing"
            interpretation: "Time between attestations suggests reading each"
            gaming_resistance: "medium"
          - metric: "attestation_order"
            interpretation: "Non-linear order suggests genuine consideration"
            gaming_resistance: "high"
          - metric: "attestation_reconsideration"
            interpretation: "Unchecking and re-checking suggests thought"
            gaming_resistance: "high"

  gaming_resistance_analysis:
    threat_model: |
      A determined human can game any individual metric. The defense is:
      1. Composite scoring (must game multiple signals simultaneously)
      2. Pattern detection (consistent minimal engagement is flagged)
      3. Behavioral baseline (deviation from personal baseline is flagged)
      4. Random deep verification (occasional enhanced checks)
      
    pattern_detection:
      - pattern: "consistent_minimum_engagement"
        description: "Always scores just above threshold"
        response: "flag_for_supervisory_review"
        
      - pattern: "engagement_score_decline"
        description: "Scores declining over time (fatigue)"
        response: "mandatory_break_suggestion"
        
      - pattern: "time_of_day_variance"
        description: "Lower engagement at certain hours"
        response: "volume_throttling_during_low_engagement_periods"
        
    enhanced_verification:
      trigger: "random_sample_5_percent"
      method: "comprehension_question"
      example: |
        Before authorizing, please answer:
        "What is the evaluation period for this review?"
        [Free text response, validated against action parameters]
        
  future_capabilities:
    # These are noted for roadmap, not current implementation
    eye_tracking:
      status: "roadmap"
      applicability: "VR/AR interfaces, dedicated workstations"
      privacy_considerations: "requires explicit consent"
      
    biometric_attention:
      status: "research"
      applicability: "high-security environments"
      privacy_considerations: "significant, requires careful governance"
```

**Key Insight:** The goal is not to make gaming impossible—a sufficiently determined human can always game a system. The goal is to make genuine engagement *easier* than gaming. If it takes more effort to fake engagement than to actually engage, most humans will actually engage.

---

## Part III: Integration with APQC → SFS

### 3.1 Overview

The APQC → SFS Execution Specification defines a system for compiling enterprise process models into executable capabilities. It is a Capable System in the Witness Architecture: it can do things, but it cannot decide to do things.

This section illustrates how the Witness Architecture integrates with APQC → SFS to create an accountable automation system.

### 3.2 The Problem the Integration Solves

Without the Witness Architecture, APQC → SFS can be misused in predictable ways:

**Misuse Pattern 1: Rubber-Stamp Authorization**

A human is presented with hundreds of actions requiring authorization. They approve all of them in minutes, without genuine review. The audit log shows "human approved," but no human actually decided anything.

*Witness Architecture Response:* Tiered witnessing (Section 2.6) assigns appropriate scrutiny levels. High-volume routine actions get Tier 1 (batch with acknowledgment). Consequential actions get Tier 2+ (individual with engagement verification). Rubber-stamping Tier 2+ actions produces low engagement scores, which are recorded and flagged.

**Misuse Pattern 2: Authority Laundering**

A director authorizes "the system" to make decisions within certain parameters. Individual decisions are then attributed to "the system operating within authorized parameters." No human is accountable for any specific decision.

*Witness Architecture Response:* The witness layer does not recognize "system authorization." Every action requires a human decider for that specific action. Standing authorizations can establish *eligibility* to decide but cannot *constitute* decisions themselves.

**Misuse Pattern 3: Understanding Theater**

Humans click through attestation screens without reading them. The record shows they "attested to understanding," but they understood nothing. The attestation is meaningless.

*Witness Architecture Response:* Engagement verification (Section 2.7) uses composite scoring to detect mechanical compliance. Random comprehension checks verify actual understanding. Pattern detection flags consistent minimal engagement for supervisory review.

**Misuse Pattern 4: Accountability Diffusion**

Multiple humans are involved in a decision chain. When things go wrong, each points to the others. "I just approved what the previous reviewer approved." No individual is accountable.

*Witness Architecture Response:* Each human in a decision chain has their own witness record. The chain is visible. "I just approved what the previous reviewer approved" is documented—the witness records that the human attested to that, making their abdication of independent judgment explicit and permanent.

### 3.3 Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    APQC → SFS WITH WITNESS ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      APQC → SFS EXECUTOR                         │    │
│  │                      (Capable System)                            │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │    │
│  │  │   Process   │  │     SFS     │  │   Context   │              │    │
│  │  │   Intent    │─▶│  Functions  │─▶│  Bindings   │──────────┐   │    │
│  │  │   (APQC)    │  │             │  │             │          │   │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘          │   │    │
│  │                                                              │   │    │
│  │  ════════════════════════════════════════════════════════   │   │    │
│  │                    WITNESS BOUNDARY                          │   │    │
│  │  ════════════════════════════════════════════════════════   │   │    │
│  │                                                              ▼   │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐│   │
│  │  │    Tier     │  │ Engagement  │  │ Attestation │  │ Execution ││   │
│  │  │ Assignment  │─▶│ Verification│─▶│   Capture   │─▶│   Gate    ││   │
│  │  │             │  │             │  │             │  │           ││   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘│   │
│  │         │                │                │               │      │    │
│  └─────────┼────────────────┼────────────────┼───────────────┼──────┘    │
│            │                │                │               │           │
│            ▼                ▼                ▼               ▼           │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      ATTESTED RECORD STORE                       │    │
│  │                (Pseudonymized, Immutable Ledger)                 │    │
│  │                                                                  │    │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │   │ WR-0001  │  │ WR-0002  │  │ WR-0003  │  │ WR-0004  │  ...   │    │
│  │   │ Tier 2   │  │ Tier 2   │  │ Tier 1   │  │ Tier 3   │        │    │
│  │   │ Eng: 0.82│  │ Eng: 0.91│  │ Batch    │  │ Eng: 0.88│        │    │
│  │   └──────────┘  └──────────┘  └──────────┘  └──────────┘        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                   IDENTITY RESOLUTION SERVICE                    │    │
│  │              (Pseudonym ↔ Identity, Access Controlled)           │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.4 Illustrative Scenario: Quarterly Performance Evaluation Cycle

HR initiates the quarterly performance evaluation cycle. The APQC → SFS system is configured to execute performance evaluations for 500 employees.

**Tier Assignment:**

The governance policy classifies "initiate performance evaluation" as Tier 2 (Standard Witnessing). However, dynamic adjustment elevates certain evaluations:

- First-time evaluators: elevated to Tier 3
- Evaluations with "needs improvement" ratings: elevated to Tier 3
- Evaluations affecting employees in protected classes: elevated to Tier 3

Result: 350 evaluations at Tier 2, 150 evaluations at Tier 3.

**Tier 2 Processing (350 evaluations):**

1. HR Manager receives authorization requests grouped by team
2. For each evaluation:
   - Manager reviews employee metrics (material access tracked)
   - Manager spends time on authorization screen (temporal engagement tracked)
   - Manager confirms specific attestations
   - Engagement score computed (threshold: 0.70)
3. Manager can process approximately 15-20 evaluations per hour with genuine engagement
4. Full batch requires 18-24 hours of engaged work, spread across multiple days

**Tier 3 Processing (150 evaluations):**

1. HR Manager receives individual authorization requests
2. For each evaluation:
   - Manager must document rationale (free text)
   - Manager must acknowledge alternatives considered
   - 5-minute cooling period before execution
   - Engagement threshold: 0.85
3. Manager can process approximately 8-10 evaluations per hour
4. Full batch requires 15-20 hours of engaged work

**Total Cycle Time:**

With genuine engagement, the 500-evaluation cycle requires approximately 35-45 hours of HR Manager attention, spread across 5-7 business days.

**The HR Manager's Complaint:**

"This used to take me an afternoon! Now it takes a week!"

**The Response:**

"The previous process took an afternoon because you weren't actually reviewing 500 evaluations—you were clicking 'approve' 500 times. If your signature means 'I reviewed this and believe it's warranted,' then your signature should require actual review.

You have options:
1. **Extend the cycle:** Give yourself more time for genuine review
2. **Delegate authority:** Train and authorize additional reviewers to share the load
3. **Reduce volume:** Evaluate less frequently or in smaller batches
4. **Improve efficiency:** Invest in better tooling for the review process itself

What you cannot do is claim to have reviewed 500 evaluations in an afternoon. The witness knows that's not possible."

### 3.5 Dysfunction Metrics

The Witness Architecture generates metrics that surface institutional dysfunction:

```yaml
DysfunctionDashboard:
  audience: "Board Audit Committee, External Auditors, Governance Officers"
  refresh: "real-time, with weekly digest"
  suppression: "not_permitted"
  
  # Engagement Quality Metrics
  engagement_metrics:
    - name: "Mean Engagement Score by Tier"
      visualization: "line_chart_over_time"
      alert_condition: "declining_trend"
      interpretation: |
        Declining engagement scores suggest increasing rubber-stamping
        or decision fatigue. Investigate workload and staffing.
        
    - name: "Minimum-Threshold Rate"
      formula: "authorizations_at_threshold / total_authorizations"
      alert_threshold: 0.30
      interpretation: |
        High minimum-threshold rate indicates humans doing exactly
        enough to pass, not genuinely engaging. Consider whether
        volume exceeds human capacity.
        
    - name: "Engagement Score Distribution"
      visualization: "histogram_by_tier"
      healthy_pattern: "normal_distribution_above_threshold"
      unhealthy_pattern: "bimodal_with_peak_at_threshold"
      interpretation: |
        Bimodal distribution (some genuine, many at minimum) suggests
        structural pressure to rubber-stamp.
        
  # Volume and Capacity Metrics
  capacity_metrics:
    - name: "Authorization Velocity by Individual"
      formula: "authorizations_per_hour_per_person"
      tier_2_alert: 25  # Humans cannot genuinely review faster
      tier_3_alert: 15
      interpretation: |
        Velocity exceeding human cognitive limits indicates
        rubber-stamping regardless of engagement scores.
        
    - name: "Capacity Utilization"
      formula: "actual_authorization_hours / available_authorization_hours"
      alert_threshold: 0.90
      interpretation: |
        Sustained high utilization leads to fatigue and
        declining engagement quality. Staff accordingly.
        
    - name: "Queue Depth Trend"
      visualization: "queue_size_over_time"
      alert_condition: "growing_backlog"
      interpretation: |
        Growing backlog creates pressure to rubber-stamp.
        Address root cause (volume or capacity).
        
  # Pattern Detection Metrics
  pattern_metrics:
    - name: "Consistent Minimum Engagers"
      definition: "individuals with >50% authorizations at minimum threshold"
      response: "supervisory_review_required"
      
    - name: "Time-of-Day Engagement Variance"
      visualization: "engagement_by_hour_heatmap"
      interpretation: |
        Low engagement during certain hours suggests fatigue
        or distraction. Consider workflow adjustments.
        
    - name: "Material Access Rate"
      formula: "authorizations_with_material_access / total_authorizations"
      tier_2_alert: 0.70
      tier_3_alert: 0.90
      interpretation: |
        Authorizations without material access suggest
        decisions made without reviewing evidence.
        
  # Escalation Health Metrics
  escalation_metrics:
    - name: "Escalation Resolution Time (p50, p90)"
      alert_p50: "4 hours"
      alert_p90: "24 hours"
      
    - name: "Escalation Timeout Rate"
      alert_threshold: 0.10
      consequence: "capability_degradation"
      
    - name: "Escalation Concentration"
      definition: "percentage of escalations going to single individual"
      alert_threshold: 0.40
      interpretation: |
        High concentration creates bottleneck and
        single point of failure.
```

---

## Part IV: Addressing Institutional Resistance

### 4.1 The Liability Question

**Anticipated Objection:** "This creates a perfect audit trail for plaintiffs' lawyers. Currently, institutional fog provides legal cover. Why would we create evidence against ourselves?"

**Response:**

The objection assumes that hidden liability is preferable to visible liability. This assumption is increasingly false, for three reasons:

**1. Regulatory Environment Is Shifting**

Regulators are moving from "did you have a process?" to "did the process actually work?" The EU AI Act, proposed US algorithmic accountability legislation, and sector-specific regulations (financial services, healthcare) increasingly require demonstrable human oversight—not just claimed oversight.

Organizations without witness documentation will face the question: "How do you know humans actually reviewed these decisions?" The answer "we had an approval workflow" is becoming insufficient. The answer "we have timestamped, engagement-verified, cryptographically sealed records of every human authorization" is defensible.

**2. Plaintiff Strategy Is Evolving**

Plaintiffs' attorneys have learned to ask for algorithm audits, decision logs, and approval records. Organizations that claim "human oversight" but cannot produce evidence of genuine oversight face discovery battles that are expensive regardless of outcome.

The Witness Architecture changes the legal positioning:

- Without witness: "We claim humans approved, but we cannot prove they actually reviewed"
- With witness: "We can prove exactly what the human reviewed, attested to, and authorized"

The first position invites fishing expeditions. The second position provides a clear factual record that may be unfavorable but is at least *clear*. Clarity is often preferable to ambiguity in litigation.

**3. Insurance Markets Are Pricing AI Risk**

AI liability insurance is emerging as a market. Insurers will price based on risk controls. Organizations with demonstrable accountability controls will pay lower premiums than organizations relying on institutional fog.

The Witness Architecture is insurance documentation. It demonstrates that the organization takes accountability seriously and has controls in place. This is increasingly valuable as insurers become sophisticated about AI risk.

**The Real Question:**

The real question is not "why create evidence?" but "what evidence do you want to exist when things go wrong?"

Without the Witness Architecture: evidence will be ambiguous, incomplete, and subject to interpretation. Litigation will be expensive and outcomes uncertain.

With the Witness Architecture: evidence will be clear. If the human made a bad decision, that's documented. If the human made a reasonable decision that had bad outcomes, that's also documented. Clarity enables resolution.

### 4.2 Anticipated Objections and Responses

**Objection: "This will slow everything down."**

Response: Yes. The current speed is achieved by removing genuine human oversight. This system restores genuine oversight, which has a cost. 

However, tiered witnessing (Section 2.6) ensures the cost is proportionate. Low-risk actions remain fast. Only consequential actions require engagement. If your organization is slowed dramatically, that reveals how many consequential actions were being rubber-stamped.

**Objection: "Our competitors don't require this."**

Response: Your competitors are accumulating accountability debt. When the failures happen—and they will—your competitors will face consequences without documentation. You will have documentation showing that humans genuinely authorized every action. 

As AI regulation increases, early adopters of accountability infrastructure will have competitive advantage over organizations scrambling to retrofit controls.

**Objection: "We trust our managers to make good decisions without all this overhead."**

Response: The Witness Architecture does not question whether managers make good decisions. It ensures that whatever decisions they make are permanently attributed to them. If you trust your managers, the witness record will reflect well-considered decisions. 

If you don't want a witness record, ask why. What decisions are you expecting that you wouldn't want documented?

**Objection: "People will refuse to authorize anything."**

Response: If people refuse to authorize actions they were previously rubber-stamping, that reveals the rubber-stamping. 

If genuinely consequential decisions are now being delayed because people are reluctant to take personal responsibility, that's information. Perhaps those decisions should be delayed. Perhaps the organization needs clearer decision authority. Perhaps the risks need to be better communicated.

Authorization paralysis is a symptom. The Witness Architecture makes the symptom visible; it doesn't cause the underlying condition.

**Objection: "GDPR requires us to delete personal data."**

Response: Section 2.5 addresses this directly. The Witness Architecture uses pseudonymization to separate "what decision was made" (permanent) from "who made it" (access-controlled and erasable). 

The decision record persists because accountability requires memory. The identity mapping can be erased because privacy requires boundaries. Both requirements are satisfied.

### 4.3 Finding Allies

The Witness Architecture will be resisted by those who benefit from diffuse accountability. It will be supported by those who bear the costs of accountability failures:

**Natural Allies:**

| Stakeholder | Interest | Talking Point |
|-------------|----------|---------------|
| General Counsel | Defensible litigation position | "Clear records are better than ambiguous records in discovery" |
| Chief Risk Officer | Quantifiable risk management | "We can measure and manage what we can see" |
| External Auditors | Verifiable controls | "This gives us something to actually audit" |
| Board Audit Committee | Personal liability protection | "Documentation that oversight actually occurred" |
| Regulators | Demonstrable compliance | "Evidence that human-in-the-loop isn't theater" |
| Insurers | Pricing AI risk | "Controls we can underwrite" |
| Employees Who Refuse to Rubber-Stamp | Structural support | "I can point to the system, not just my judgment" |

**Entry Strategy:**

Begin with General Counsel and Chief Risk Officer. Frame the Witness Architecture as risk management infrastructure, not process overhead. Emphasize the liability positioning (Section 4.1).

Board Audit Committee is the escalation path. If operational leadership resists, governance leadership can mandate accountability controls as part of fiduciary duty.

External auditors and regulators are validation channels. Proactively share the approach; position the organization as a leader in AI accountability.

### 4.4 The Honest Trade-Off

The Witness Architecture offers organizations a trade-off:

| Dimension | Without Witness | With Witness |
|-----------|-----------------|--------------|
| Throughput | Bounded only by system capacity | Bounded by human attention capacity |
| Accountability | Diffuse, deniable | Specific, permanent |
| Litigation exposure | Ambiguous (expensive to resolve) | Clear (may be unfavorable but resolvable) |
| Regulatory posture | "We have a process" | "We have evidence the process works" |
| Insurance position | Unknown/unquantified risk | Documented controls |
| Failure mode | "No one is responsible" | "This person is responsible" |

Organizations must choose. The Witness Architecture implements the right column. Organizations that want the left column should not use it—but should understand that the left column is increasingly risky as AI governance matures.

---

## Part V: Visualizing the Difference

### 5.1 Traditional AI Automation vs. Witness Architecture

**Traditional Approach: Accountability Lost**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     TRADITIONAL AI AUTOMATION                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────┐  │
│   │  Human  │────▶│ "Approve    │────▶│  Black Box  │────▶│   500   │  │
│   │         │     │    All"     │     │     AI      │     │ Actions │  │
│   └─────────┘     └─────────────┘     └─────────────┘     └─────────┘  │
│                                                                          │
│   Time: 5 minutes                                                        │
│   Evidence: "Batch approved by HR Manager"                               │
│   Accountability: Diffuse ("the system did it")                          │
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ WHEN THINGS GO WRONG:                                            │   │
│   │                                                                  │   │
│   │ Plaintiff: "Who decided to terminate my client?"                 │   │
│   │ Organization: "The system recommended it based on parameters"    │   │
│   │ Plaintiff: "Who approved those parameters?"                      │   │
│   │ Organization: "That was a committee decision"                    │   │
│   │ Plaintiff: "Who was on the committee?"                           │   │
│   │ Organization: "We'd have to check the records..."                │   │
│   │                                                                  │   │
│   │ Result: Expensive discovery, ambiguous liability                 │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Witness Architecture: Accountability Preserved**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      WITNESS ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────┐  │
│   │  Human  │────▶│ Engagement  │────▶│  Witness    │────▶│ Action  │  │
│   │         │     │ Verification│     │  Record     │     │         │  │
│   └─────────┘     └─────────────┘     └─────────────┘     └─────────┘  │
│        │                                     │                          │
│        │          ┌─────────────┐            │                          │
│        └─────────▶│ Attestation │────────────┘                          │
│                   │   Capture   │                                        │
│                   └─────────────┘                                        │
│                                                                          │
│   Time: 3-4 minutes per consequential action                            │
│   Evidence: Specific record per action with engagement score            │
│   Accountability: Individual, permanent, cryptographically sealed       │
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ WHEN THINGS GO WRONG:                                            │   │
│   │                                                                  │   │
│   │ Plaintiff: "Who decided to terminate my client?"                 │   │
│   │ Organization: "Jane Smith, on January 15 at 2:30 PM"             │   │
│   │ Plaintiff: "What did she review?"                                │   │
│   │ Organization: "Performance metrics, prior evaluations.           │   │
│   │               She accessed them for 4 minutes before deciding."  │   │
│   │ Plaintiff: "What did she attest to?"                             │   │
│   │ Organization: "Here are her three attestations, timestamped."    │   │
│   │                                                                  │   │
│   │ Result: Clear factual record, focused liability determination    │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Decision Flow Comparison

```
TRADITIONAL:                          WITNESS ARCHITECTURE:

Request ──────────────────────▶       Request ──────────────────────▶
    │                                     │
    ▼                                     ▼
┌────────────┐                       ┌────────────┐
│  Approval  │                       │    Tier    │
│   Queue    │                       │ Assignment │
└────────────┘                       └────────────┘
    │                                     │
    ▼                                     ▼
┌────────────┐                       ┌────────────────────────────────┐
│  "Approve  │                       │  Tier 1?  ──▶ Batch Witness   │
│    All"    │                       │  Tier 2?  ──▶ Individual +    │
└────────────┘                       │               Engagement      │
    │                                │  Tier 3+? ──▶ Enhanced +      │
    │                                │               Cooling Period  │
    │                                └────────────────────────────────┘
    │                                     │
    │                                     ▼
    │                                ┌────────────┐
    │                                │ Engagement │
    │                                │   Check    │
    │                                └────────────┘
    │                                     │
    │                                Pass │ Fail
    │                                  │     │
    │                                  ▼     ▼
    │                                ┌────┐ ┌────────┐
    │                                │ OK │ │ Reject │
    │                                └────┘ └────────┘
    │                                  │
    ▼                                  ▼
┌────────────┐                       ┌────────────┐
│  Execute   │                       │  Witness   │
│            │                       │  Record    │
└────────────┘                       └────────────┘
    │                                     │
    ▼                                     ▼
┌────────────┐                       ┌────────────┐
│ Audit Log: │                       │  Execute   │
│ "Approved" │                       │            │
└────────────┘                       └────────────┘
                                          │
                                          ▼
                                     ┌────────────┐
                                     │ Immutable  │
                                     │   Record   │
                                     └────────────┘
```

---

## Part VI: Implementation Guidance

### 6.1 Adoption Phases

**Phase 1: Observation Only (Months 1-3)**

Deploy the witness layer in observation mode. Record authorizations but do not enforce engagement requirements. Generate dysfunction metrics. Present findings to governance bodies.

Deliverables:
- Baseline dysfunction metrics
- Current rubber-stamping rate
- Authorization velocity by individual
- Recommendations for tier assignment

This phase surfaces the current state of accountability (or lack thereof) without disrupting operations.

**Phase 2: Tier Assignment and Soft Enforcement (Months 4-6)**

Implement tier assignment policy. Enable engagement verification with warnings. When humans rush authorizations, warn them but allow the authorization. Record the warning in the witness record.

Deliverables:
- Tier assignment policy (approved by governance)
- Engagement scoring implementation
- Warning system for low engagement
- Tracking of engagement trends

This phase acclimates humans to the engagement requirements without blocking operations.

**Phase 3: Hard Enforcement for High Tiers (Months 7-9)**

Enable full engagement requirements for Tier 3 and Tier 4 actions. Authorizations that fail engagement checks are rejected. Lower tiers remain in soft enforcement.

Deliverables:
- Tier 3/4 hard enforcement
- Escalation procedures for rejected authorizations
- Capacity planning based on actual throughput
- Process adjustments as needed

This phase implements consequential accountability while allowing volume operations to continue adapting.

**Phase 4: Full Enforcement (Months 10-12)**

Enable full engagement requirements for all tiers. The system operates at the pace of genuine human attention.

Deliverables:
- Full enforcement across all tiers
- Dysfunction metrics integrated into governance reporting
- Capacity matched to authorization load
- Continuous improvement process established

**Phase 5: Metric-Driven Governance (Ongoing)**

Dysfunction metrics drive governance decisions. Authorization capacity is matched to authorization load. Processes that exceed human attention capacity are redesigned or descoped.

Deliverables:
- Quarterly governance review of dysfunction metrics
- Continuous process optimization
- Regulatory and audit integration
- Insurance documentation

### 6.2 Technical Requirements

**Identity Management:**
- SSO integration with MFA minimum
- Pseudonymization infrastructure
- Identity Resolution Service with access controls
- Audit logging of identity resolution requests

**Engagement Verification:**
- Client-side telemetry for engagement signals
- Server-side scoring engine
- Pattern detection for gaming resistance
- Random comprehension check infrastructure

**Immutable Storage:**
- Append-only storage (distributed ledger, write-once, or cryptographic chaining)
- Cryptographic sealing of records
- Tamper evidence and detection
- Geographic distribution for durability

**Integration:**
- API for Capable Systems to request witnessed authorization
- Webhook/event integration for authorization outcomes
- Bulk import for tier assignment policies
- Export for audit and regulatory reporting

### 6.3 Governance Requirements

**Board-Level Oversight:**
- Board Audit Committee receives dysfunction metrics quarterly
- Authority to mandate process changes based on metrics
- Annual review of tier assignment policy

**Policy Ownership:**
- Governance committee owns tier assignment policy
- Risk committee owns engagement thresholds
- Legal owns retention and privacy policies

**Audit Integration:**
- External auditors have full access to witness records
- Pseudonym resolution available under audit protocols
- Annual attestation on witness system integrity

**Regulatory Coordination:**
- Proactive engagement with relevant regulators
- Documentation of Witness Architecture for regulatory inquiries
- Participation in AI governance standards development

---

## Part VII: Conclusion

### 7.1 The Choice

Organizations deploying AI face a choice:

They can use AI to evade accountability—to make decisions faster than humans can review them, to diffuse responsibility into algorithmic fog, to create the appearance of oversight without its substance.

Or they can use AI to strengthen accountability—to ensure that every consequential decision is witnessed, every authorization is attested, every human who decides is permanently responsible for their decision.

The Witness Architecture implements the second choice.

It will be resisted by those who benefit from ambiguity. It will be welcomed by those who bear the costs of accountability failures. It will be required, eventually, by regulators and courts and insurers who understand that "the AI decided" is not a defense.

Organizations that adopt the Witness Architecture now are building the infrastructure of accountability before it becomes mandatory. They are positioning themselves for a future where AI accountability is not optional.

### 7.2 The Summary

**The Witness Architecture ensures that:**

- Every consequential action traces to a human who authorized it
- That human attested to specific understanding before authorizing
- Evidence of genuine engagement is captured and scored
- The record is permanent, tamper-evident, and auditable
- Dysfunction is visible and measurable
- Privacy is preserved through pseudonymization
- Proportionality is maintained through risk tiering

**The Witness Architecture does not:**

- Prevent bad decisions
- Replace human judgment
- Slow down low-risk operations
- Create liability that doesn't already exist
- Conflict with privacy regulations

**The Witness Architecture reframes AI from:**

"A way to remove humans from decisions"

**To:**

"A way to make human decisions undeniable"

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Attestation** | A statement that a human confirms as true and accepts responsibility for |
| **Attested Record** | The permanent, pseudonymized record of a witnessed decision |
| **Capable System** | A system that can perform actions but cannot authorize them |
| **Decider** | A natural person who authorizes actions and bears responsibility for them |
| **Dysfunction Metric** | A measurement that surfaces accountability failures |
| **Engagement Score** | Composite measure of genuine human attention during authorization |
| **Engagement Verification** | Process of assessing whether a human genuinely engaged with an authorization |
| **Identity Resolution Service** | System that maps pseudonyms to identities under controlled access |
| **Institutional Fog** | The diffusion of accountability into organizational abstractions |
| **Pseudonymization** | Replacing direct identifiers with pseudonyms that can be resolved under controls |
| **Risk Tier** | Classification of action consequence level determining witnessing requirements |
| **Rubber-Stamping** | Authorizing actions without genuine review |
| **Witness** | The system component that observes and records human decisions |
| **Witness Boundary** | The architectural layer where human decisions are witnessed |

---

## Appendix B: Reference to Related Specifications

| Specification | Relationship |
|---------------|--------------|
| APQC → SFS Execution Specification v2.0 | The Witness Architecture wraps APQC → SFS as a Capable System |
| Semantic Function Schema (SFS) v2.2 | SFS functions are the capabilities that require witnessed authorization |
| *Toward Synthetic Moral Agency* (companion) | Philosophical trajectory for witness-as-precursor-to-agent |

---

## Appendix C: GDPR Compliance Summary

| GDPR Requirement | Witness Architecture Compliance |
|------------------|--------------------------------|
| Right to Access | Subject can access their own pseudonymized witness records |
| Right to Rectification | Witness records are factual observations, not subject to rectification; identity mappings can be corrected |
| Right to Erasure | Identity mappings can be erased; witness records (pseudonymized) persist for legitimate interest |
| Right to Portability | Subject can export their decision history |
| Data Minimization | Only necessary data captured; PII pseudonymized |
| Purpose Limitation | Clear purpose: accountability for authorized actions |
| Storage Limitation | Identity mappings subject to retention policy; witness records permanent for accountability |
| Lawful Basis | Legitimate interest (accountability) for witness records; consent/contract for identity mappings |

---

## Appendix D: Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-31 | Initial specification |
| 1.1 | 2026-01-31 | Added: Risk-tiered witnessing (2.6), Enhanced engagement verification (2.7), GDPR/pseudonymization compliance (2.5), Expanded liability argument (4.1), Visual decision flow diagrams (Part V). Removed: Synthetic moral agency content (moved to companion document). Refined: Witness record schema for pseudonymization. |

---

*The Witness Architecture: Because decisions should have deciders, and deciders should have names.*
