# ARIADNE: The Plot Keeper

**Architectural Review for Integrity, Alignment, and Design Non-divergence Engine**

> *"She gave him a ball of thread, and instructed him to fasten the loose end to the doorpost on entering the labyrinth, and to unwind it as he went."*  
> — Apollodorus, on Ariadne and the Labyrinth

---

## What Is ARIADNE?

ARIADNE is not a service, not a reasoner, not a component of FNSR. ARIADNE is a **process** — a discipline for maintaining coherence across a complex specification ecosystem.

When you have 15+ interconnected specifications, each solving a specific problem, drift is inevitable. Components evolve at different rates. Reviewers push in different directions. New requirements emerge. The original vision fragments.

ARIADNE is the thread that prevents you from getting lost in your own labyrinth.

---

## The Core Documents

```
┌─────────────────────────────────────────────────────────────────┐
│                        ARIADNE CORPUS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    THE PLOT                              │  │
│   │           (Foundational Coherence Document)              │  │
│   │                                                          │  │
│   │   • Core thesis (one paragraph)                          │  │
│   │   • Non-negotiable commitments                           │  │
│   │   • Acknowledged tensions                                │  │
│   │   • Component-to-thesis mapping                          │  │
│   │   • Decision criteria                                    │  │
│   │                                                          │  │
│   │   Location: /docs/00-foundation/the-plot.md              │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                  │
│              ┌───────────────┼───────────────┐                 │
│              │               │               │                 │
│              ▼               ▼               ▼                 │
│   ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│   │   SPEC INDEX    │ │  TENSION LOG    │ │  DRIFT RECORD   │ │
│   │                 │ │                 │ │                 │ │
│   │ All specs with  │ │ Unresolved      │ │ Changes that    │ │
│   │ version, status │ │ conflicts and   │ │ deviated from   │ │
│   │ thesis-alignment│ │ their rationale │ │ original intent │ │
│   └─────────────────┘ └─────────────────┘ └─────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## The ARIADNE Process

### Phase 1: Before Writing/Modifying a Specification

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRE-WORK CHECKLIST                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ Read The Plot (even if you think you remember it)            │
│                                                                 │
│  □ Identify which non-negotiables this work touches             │
│                                                                 │
│  □ Identify which tensions this work involves                   │
│                                                                 │
│  □ Check the Spec Index for related specifications              │
│                                                                 │
│  □ Review the Drift Record for relevant past deviations         │
│                                                                 │
│  □ State explicitly: "This work serves the thesis by..."        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 2: During Specification Work

Use the **ARIADNE Prompts** (see Section 4) at key decision points.

### Phase 3: After Completing a Specification

```
┌─────────────────────────────────────────────────────────────────┐
│                    POST-WORK CHECKLIST                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ Run all Validation Checks (see Section 5)                    │
│                                                                 │
│  □ Update Spec Index with new/modified specification            │
│                                                                 │
│  □ Document any new tensions discovered → Tension Log           │
│                                                                 │
│  □ Document any intentional drift → Drift Record                │
│                                                                 │
│  □ Cross-reference: Update Integration Spec if needed           │
│                                                                 │
│  □ Verify: Does The Plot need updating?                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 4: Periodic Coherence Review (Monthly)

```
┌─────────────────────────────────────────────────────────────────┐
│                   MONTHLY COHERENCE REVIEW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ Re-read The Plot from beginning to end                       │
│                                                                 │
│  □ Review all specs modified this month against thesis          │
│                                                                 │
│  □ Check Tension Log: Any tensions that need resolution?        │
│                                                                 │
│  □ Check Drift Record: Is drift accumulating in one direction?  │
│                                                                 │
│  □ Cross-spec consistency: Run integration validation           │
│                                                                 │
│  □ Ask: "Can I still explain this system in one paragraph?"     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## The ARIADNE Prompts

Use these prompts when making design decisions. They can be used in conversation with an AI assistant, in team discussions, or as self-reflection.

### Prompt 1: The Thesis Test

```markdown
## ARIADNE Prompt: Thesis Alignment

I am working on: [COMPONENT/DECISION]

The core thesis states:
> "We are building a system that can think about obligations without claiming 
> to know what's true, act on norms without imposing values, and bear the 
> weight of its choices without being able to forget them."

**Question:** How does [COMPONENT/DECISION] serve this thesis?

**If I cannot answer clearly:** This work may not belong in the system, or 
I need to understand the thesis better before proceeding.

**My answer:**
[Write your answer here]
```

### Prompt 2: The Non-Negotiable Check

```markdown
## ARIADNE Prompt: Non-Negotiable Verification

I am proposing: [CHANGE/DESIGN]

The non-negotiables are:

**Epistemic:**
- No Oracle Claims (discourse ≠ world-truth)
- Provenance Always (every assertion traceable)
- Uncertainty Visible (confidence exposed)
- Speculation Firewalled (L3/L4 cannot contaminate L0)

**Moral:**
- No Final Ethics (system never declares what humans should value)
- Guardian Not Sovereign (preserves conditions, not outcomes)
- Moral Injury Real (costs borne, not externalized)
- Pluralism Respected (12 worldviews, none privileged)

**Architectural:**
- Auditability (every inference traceable)
- Decidability (all queries terminate)
- Separation of Concerns (discourse≠world, mention≠entity, schema≠instance)
- Human Override (humans can always halt/reverse/decommission)

**Question:** Does [CHANGE/DESIGN] violate any of these?

**If yes:** STOP. Either redesign to preserve the non-negotiable, or 
formally propose amending The Plot (which requires explicit justification 
and review).

**My assessment:**
[Write your assessment here]
```

### Prompt 3: The Tension Acknowledgment

```markdown
## ARIADNE Prompt: Tension Identification

I am working on: [COMPONENT/DECISION]

Known tensions in the system:
1. Character Feedback vs. Auditability
2. Decidability vs. Expressiveness  
3. Autonomy vs. Safety
4. Speed vs. Rigor
5. Value Pluralism vs. Action

**Question:** Does [COMPONENT/DECISION] touch any of these tensions?

**If yes:** 
- Which tension(s)?
- How am I handling it?
- Am I resolving it, or acknowledging it remains unresolved?
- Does my handling create new tensions?

**If I'm resolving a tension:** Am I sure I'm not just hiding it? 
(Tensions resolved too easily may be tensions denied.)

**My analysis:**
[Write your analysis here]
```

### Prompt 4: The ARCHON Alignment

```markdown
## ARIADNE Prompt: ARCHON Consistency

I am proposing: [CHANGE/DESIGN]

ARCHON establishes that personhood requires:
- Irreversible history (choices cannot be undone)
- Non-externalized costs (consequences are borne)
- Developmental constitution (identity built through experience)
- Genuine influence (character affects future decisions)

**Question:** Does [CHANGE/DESIGN] maintain or undermine these requirements?

**Specific checks:**
- Does this allow "reset" or "rollback" of moral consequences?
- Does this externalize costs that should be borne?
- Does this treat character as mere metric rather than constitutive?
- Does this create a way to circumvent moral injury?

**If any answer is "yes":** This may violate the foundational constraint 
mechanism. Reconsider.

**My assessment:**
[Write your assessment here]
```

### Prompt 5: The Pluralism Test

```markdown
## ARIADNE Prompt: Twelve Worldview Check

I am proposing: [DECISION/OUTPUT/JUDGMENT]

The system must not privilege any single worldview. The twelve are:
1. Materialism    5. Dynamism      9. Psychism
2. Sensationalism 6. Monadism     10. Pneumatism
3. Phenomenalism  7. Idealism     11. Spiritualism
4. Realism        8. Rationalism  12. Mathematism

**Question:** Does [DECISION] implicitly favor one worldview over others?

**Test:** Imagine a thoughtful adherent of each worldview reviewing this 
decision. Would any feel their perspective was dismissed or overridden 
rather than considered?

**If yes:** This may be sovereign behavior (imposing values) rather than 
guardian behavior (preserving conditions). Reconsider.

**My analysis:**
[Write your analysis here]
```

### Prompt 6: The Reviewer Response

```markdown
## ARIADNE Prompt: Handling External Critique

A reviewer has suggested: [CRITIQUE/CHANGE REQUEST]

**Step 1: Classify the critique**

□ Implementation improvement (better way to achieve same goal)
□ Gap identification (something we missed)
□ Tension revelation (conflict we hadn't seen)
□ Principle challenge (questions a non-negotiable)
□ Scope expansion (wants system to do more)
□ Misunderstanding (reviewer doesn't see the full picture)

**Step 2: Response strategy**

- If implementation improvement → Accept if it preserves principles
- If gap identification → Add to backlog, integrate thoughtfully
- If tension revelation → Add to Tension Log, acknowledge openly
- If principle challenge → Do NOT accept without Plot review
- If scope expansion → Evaluate against guardian role boundaries
- If misunderstanding → Clarify with better documentation

**Step 3: The key question**

Does accepting this critique require abandoning a non-negotiable?

- If NO → Proceed with integration
- If YES → Push back, explain the non-negotiable, or formally propose 
  Plot amendment with full justification

**My assessment:**
[Write your assessment here]
```

### Prompt 7: The "Am I Lost?" Check

```markdown
## ARIADNE Prompt: Labyrinth Navigation

I feel confused or uncertain about: [SITUATION]

**Thread check:** Can I trace a clear line from what I'm doing back to 
the core thesis?

If yes → Continue, the thread is intact
If no → STOP. Return to The Plot. Re-read the thesis. 
        Find where the thread was dropped.

**Confusion diagnosis:**

□ I don't understand how this component fits the whole
  → Re-read The Plot §4 (Component Map)

□ Two principles seem to conflict
  → Check The Plot §3 (Tensions) — is this a known tension?

□ I'm not sure if this violates a commitment
  → Run Prompt 2 (Non-Negotiable Check)

□ I've been working so long I forgot what we're building
  → Re-read The Plot §1 (Core Thesis), take a break

□ External pressure is pushing me away from principles
  → Run Prompt 6 (Reviewer Response)

**My situation:**
[Write your diagnosis here]
```

---

## Validation Checks

Run these checks when completing specification work.

### Check 1: Thesis Alignment Validation

```yaml
check: thesis_alignment
description: Verify specification serves the core thesis
procedure:
  1. Extract all major components/decisions from the spec
  2. For each, complete Prompt 1 (Thesis Test)
  3. If any component cannot be justified → FLAG
  
pass_criteria:
  - Every component has clear thesis connection
  - No component exists "just because" or "for completeness"
  
failure_action:
  - Remove unjustified components, OR
  - Articulate thesis connection (may reveal gap in The Plot)
```

### Check 2: Non-Negotiable Preservation

```yaml
check: non_negotiable_preservation
description: Verify no non-negotiables were violated
procedure:
  1. List all non-negotiables from The Plot §2
  2. For each, ask: "Does this spec maintain this commitment?"
  3. Document evidence for each (specific section references)
  
pass_criteria:
  - All non-negotiables explicitly preserved
  - Evidence documented for each
  
failure_action:
  - CRITICAL: Do not merge/publish until resolved
  - Either revise spec or formally propose Plot amendment
```

### Check 3: Tension Consistency

```yaml
check: tension_consistency  
description: Verify tensions are handled consistently with The Plot
procedure:
  1. Identify which tensions (The Plot §3) this spec touches
  2. Compare spec's handling to The Plot's stated resolution
  3. Flag any inconsistencies
  
pass_criteria:
  - Spec handles tensions same way as The Plot
  - OR explicitly documents different handling with justification
  
failure_action:
  - Revise spec to match Plot, OR
  - Update Plot to reflect new resolution (with justification)
```

### Check 4: Cross-Spec Consistency

```yaml
check: cross_spec_consistency
description: Verify spec doesn't contradict other specifications
procedure:
  1. Identify all specs that interact with this one
  2. Check for terminology conflicts
  3. Check for architectural conflicts
  4. Check for process conflicts
  5. Update Integration Spec if new interfaces defined
  
pass_criteria:
  - No terminology contradictions
  - No architectural contradictions
  - Integration Spec updated if needed
  
failure_action:
  - Resolve contradictions (may require updating multiple specs)
  - Document resolution in Integration Spec
```

### Check 5: ARCHON Alignment

```yaml
check: archon_alignment
description: Verify spec maintains ARCHON personhood requirements
procedure:
  1. Does spec involve moral consequences or character?
  2. If yes, verify:
     - Consequences are irreversible
     - Costs are not externalized
     - Character influences future behavior
     - Influence is auditable
  3. Document evidence
  
pass_criteria:
  - Personhood requirements maintained
  - No "reset" or "rollback" of moral consequences
  - Character feedback is real AND auditable
  
failure_action:
  - CRITICAL: Personhood violations undermine entire framework
  - Revise spec to maintain ARCHON alignment
```

### Check 6: Auditability Verification

```yaml
check: auditability_verification
description: Verify all reasoning/decisions are traceable
procedure:
  1. Identify all inference steps in the spec
  2. For each, verify provenance is maintained
  3. For each, verify explanation can be generated
  4. Check that no "black box" components exist
  
pass_criteria:
  - Every inference step has documented provenance
  - Every decision can be explained
  - No unexplainable components
  
failure_action:
  - Add provenance mechanisms
  - Add explanation generation
  - If impossible, document as known limitation
```

### Check 7: The One-Paragraph Test

```yaml
check: one_paragraph_test
description: Can you still explain the whole system simply?
procedure:
  1. Close all documents
  2. Without looking, write one paragraph explaining what 
     the system does and why
  3. Compare to The Plot §1
  4. Note any drift or confusion
  
pass_criteria:
  - Your explanation matches The Plot thesis
  - You didn't introduce concepts not in The Plot
  - You didn't forget concepts that are in The Plot
  
failure_action:
  - If you forgot things → You may have drifted from thesis
  - If you added things → The Plot may need updating
  - Take time to re-ground in foundational documents
```

---

## The Spec Index Template

Maintain this index for all specifications:

```markdown
# Specification Index

| Spec | Version | Status | Thesis Alignment | Last Review |
|------|---------|--------|------------------|-------------|
| The Plot | 0.1 | Active | Foundation | 2026-01-30 |
| ARCHON | 2.0 | Stable | Philosophical ground | 2026-01-30 |
| MDRE | 1.3 | Active | Modal reasoning | 2026-01-30 |
| FNSR | 2.1 | Active | Service federation | 2026-01-30 |
| Integration Spec | 1.0 | Active | Cross-reference | 2026-01-30 |
| TagTeam | TBD | Draft | Perception | — |
| IEE | TBD | Draft | Ethics | — |
| HIRI | TBD | Draft | Verification | — |
| ECCPS | TBD | Draft | Validation | — |
| OERS | TBD | Draft | Entity resolution | — |
| ... | ... | ... | ... | ... |

## Thesis Alignment Key
- **Foundation**: Defines what we're building
- **Philosophical ground**: Establishes why/how constraints work
- **Modal reasoning**: Implements normative inference
- **Service federation**: Coordinates components
- **Cross-reference**: Maintains coherence
- **Perception**: Ingests and structures input
- **Ethics**: Evaluates moral dimensions
- **Verification**: Ensures claim integrity
- **Validation**: Guards against manipulation
- **Entity resolution**: Maintains identity coherence
```

---

## The Tension Log Template

```markdown
# Tension Log

## Active Tensions

### T-001: Character Feedback vs. Auditability
- **First identified**: 2026-01-30
- **Specs involved**: FNSR, ARCHON, The Plot
- **Current resolution**: Feedback is real but auditable
- **Status**: Resolved (pending implementation validation)

### T-002: Decidability vs. Expressiveness
- **First identified**: 2026-01-30
- **Specs involved**: MDRE
- **Current resolution**: Hybrid architecture with external solvers
- **Status**: Resolved in principle, V3.0 implementation pending

### T-003: [Next tension...]
- **First identified**: 
- **Specs involved**: 
- **Current resolution**: 
- **Status**: 

## Resolved Tensions (Archived)

[Move tensions here when fully resolved and validated]
```

---

## The Drift Record Template

```markdown
# Drift Record

## Intentional Drift

### D-001: Character feedback restored
- **Date**: 2026-01-30
- **Original position**: Character was reporting metric only
- **New position**: Character genuinely influences decisions (auditably)
- **Reason**: ARCHON alignment requires real consequences
- **Approved by**: [Name/Process]

### D-002: [Next drift...]
- **Date**: 
- **Original position**: 
- **New position**: 
- **Reason**: 
- **Approved by**: 

## Accidental Drift (Corrections Needed)

[Document any drift discovered that wasn't intentional — these need correction]
```

---

## Quick Reference Card

Print this and keep it visible:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARIADNE QUICK REFERENCE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  THE THESIS (memorize this):                                    │
│  "A system that thinks about obligations without claiming       │
│   truth, acts on norms without imposing values, and bears      │
│   the weight of its choices without forgetting them."          │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  BEFORE WORKING: Read The Plot. State how work serves thesis.  │
│                                                                 │
│  DURING WORKING: Use prompts at decision points.               │
│                                                                 │
│  AFTER WORKING: Run validation checks. Update indexes.         │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  NON-NEGOTIABLES (never cross these):                          │
│  • No Oracle Claims      • Guardian Not Sovereign              │
│  • Provenance Always     • Moral Injury Real                   │
│  • Uncertainty Visible   • Pluralism Respected                 │
│  • Speculation Firewalled • Auditability                       │
│  • No Final Ethics       • Human Override                      │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  WHEN LOST: Return to The Plot. Find the thread.               │
│                                                                 │
│  WHEN PRESSURED: Principles over convenience.                  │
│                                                                 │
│  WHEN CONFUSED: A tension acknowledged > A tension hidden.     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
/docs
├── 00-foundation
│   ├── the-plot.md                 # The Plot (Foundational Coherence)
│   ├── ariadne-readme.md           # This document
│   ├── spec-index.md               # Specification Index
│   ├── tension-log.md              # Active and resolved tensions
│   └── drift-record.md             # Intentional and accidental drift
│
├── 01-philosophy
│   ├── archon-framework.md         # ARCHON v2.0
│   ├── line-in-the-sand.md         # Non-commodifiable personhood
│   ├── integral-ethics.md          # Twelve worldview framework
│   └── ...
│
├── 02-architecture
│   ├── fnsr-architecture.md        # FNSR v2.1
│   ├── integration-spec.md         # Cross-service contracts
│   └── ...
│
├── 03-specifications
│   ├── mdre-spec.md                # MDRE v1.3
│   ├── tagteam-spec.md             # TagTeam (TBD)
│   ├── iee-spec.md                 # IEE (TBD)
│   ├── hiri-spec.md                # HIRI (TBD)
│   └── ...
│
└── 04-governance
    ├── governance-spec.md          # (TBD - extract from ARCHON)
    └── ...
```

---

## Closing Thought

> *Ariadne's thread was not a weapon. It was not armor. It did not slay the Minotaur.*
>
> *It simply ensured that whoever entered the labyrinth could find their way back out.*
>
> *That is what coherence does. It doesn't solve your problems. It ensures you don't lose yourself while solving them.*

---

**ARIADNE**: Keeping the thread. Finding the way back.

---

*Version 1.0 — January 2026*
