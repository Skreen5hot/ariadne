# Drift Report

**Generated:** 2026-01-31
**Method:** Spec-Driven Discovery v1.1 §7
**Epistemic Classification:** L1-INTERNAL (model-mediated analysis)

---

## Summary

| Metric | Value |
|--------|-------|
| Services audited | 22 |
| Fully compliant (drift_score = 100) | 11 |
| Minor drift (drift_score 85–99) | 8 |
| Moderate drift (drift_score < 85) | 0 |
| Critical drift | 0 |
| Integration gaps (spec exists, not in event registry) | 4 |

**Overall assessment:** The ecosystem is well-aligned. No critical drift detected. Primary gaps are missing spec documents for services that already have event contracts, and services with specs that lack event registry entries.

---

## Category 1: Services With Event Contracts But No Spec Document

These services are defined in the Integration Spec §4.2 and The Plot §4 but have no dedicated specification document in `docs/03-specifications/`.

| Service | drift_score | Gap Type |
|---------|-------------|----------|
| SIS | 85 | MISSING_SPEC |
| OERS | 85 | MISSING_SPEC |
| W2Fuel | 85 | MISSING_SPEC |
| AES | 85 | MISSING_SPEC |
| DES | 85 | MISSING_SPEC |
| CSS | 85 | MISSING_SPEC |
| APS | 85 | MISSING_SPEC |

**Impact:** These services have well-defined event interfaces and thesis justifications, but their internal behavior, constraints, and implementation requirements are not formally documented. This creates risk of implementation divergence.

**Recommendation:** Prioritize SIS, OERS, and W2Fuel (Tier 1, pipeline-critical). AES, DES, CSS, APS are Tier 2 (reasoning extensions) and can follow.

---

## Category 2: Services With Spec Documents But No Event Registry Entry

These services have dedicated specifications but are not registered in the Integration Spec §4.2 event registry.

| Service | drift_score | Gap Type |
|---------|-------------|----------|
| OCE | 90 | MISSING_EVENT_CONTRACT |
| SFS | 90 | NOT_APPLICABLE (normative framework) |
| DSFC | 90 | NOT_APPLICABLE (normative framework) |
| SDP | 90 | INFRASTRUCTURE (may not need events) |

**Impact:** OCE is the most significant gap — it performs constraint checking on claims and should have a defined event contract (consumes extracted claims, produces constraint violations). SFS, DSFC, and PFCF are classification/normative frameworks that may not require event-driven integration.

**Recommendation:** Add OCE to Integration Spec §4.2. Evaluate whether SFS/DSFC/SDP need event contracts or are correctly classified as normative/infrastructure.

---

## Category 3: Governance Specification Gaps

The FNSR Integration Spec §3 explicitly identifies these as HIGH/MEDIUM priority gaps:

| Spec | Priority | Status |
|------|----------|--------|
| FNSR Governance Specification | HIGH | Not started |
| FNSR Performance Specification | HIGH | Not started |
| FNSR Adversarial Defense Specification | HIGH | Not started |
| IEE 12 Worldview Catalog | MEDIUM | Not started |

These are not service drift per se, but represent architectural gaps that affect system-wide governance, performance guarantees, and security posture.

---

## Category 4: Alias/Naming Observations

| Alias Pair | Resolution | Confidence |
|------------|-----------|------------|
| MDRE / DRS | Same service | 1.0 |
| W2Fuel / OSS | Same service | 1.0 |
| IEE / IEA | Same service | 1.0 |
| SOCIUS / IRIS | SOCIUS deprecated, replaced by IRIS | 1.0 |

No ambiguous alias mappings detected. All service identities resolve cleanly.

---

## Category 5: Philosophical Frameworks (Non-Service)

The following are referenced in The Plot §4 as components but are philosophical frameworks, not operational services:

| Framework | Thesis Role | Has Spec |
|-----------|-------------|----------|
| ARCHON | Personhood-as-constraint | archon-functional-requirements.md |
| Line in the Sand | Non-commodifiable moral costs | 01-philosophy/ |
| Integral Ethics | Value pluralism | 01-philosophy/ |
| BFO/CCO | Ontological backbone | External standard |

These correctly have no event contracts and are not service drift.

---

## Previously Resolved Drift

| Drift Item | Resolution | Round |
|-----------|-----------|-------|
| D-001: Character feedback inconsistency | FNSR §10, Integration Spec §2.1 updated | Round 1 |
| D-002: Resource-cost model | SMA §0.5 resource governance documented | Round 2 |
| T-009: Character Feedback Spec Drift | All documents now consistent | Round 1 |

---

## Open Tensions Affecting Drift

| Tension | Impact on Drift |
|---------|----------------|
| T-007: Tool-to-Person Threshold | No operational mechanism — may require new spec |
| T-008: Worldview Fixity vs. Evolution | Affects IEE Worldview Catalog design |
| T-011: Privacy Budget Authority | Affects HIRI/ARCHON governance boundary |

---

## Action Items (Prioritized)

1. **HIGH:** Write specs for SIS, OERS, W2Fuel (pipeline-critical, no spec)
2. **HIGH:** Add OCE to Integration Spec §4.2 event registry
3. **HIGH:** Begin FNSR Governance Specification
4. **MEDIUM:** Write specs for AES, DES, CSS, APS (reasoning extensions)
5. **MEDIUM:** Begin FNSR Performance Specification
6. **MEDIUM:** Begin IEE 12 Worldview Catalog
7. **LOW:** Evaluate SFS/DSFC/SDP event integration need
8. **LOW:** Begin FNSR Adversarial Defense Specification
