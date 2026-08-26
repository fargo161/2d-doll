# Orchestration Protocol

## Round 1 — independent evidence

The Repository Analyst, Schema Architect, Anatomy Specialist, Kinematics Engineer, Orientation Architect, Garment Architect, Layering Engineer, and Interaction/Serialization Engineer inspect evidence without receiving a synthesized answer. Each records its own conclusions and reality states. Parallel agents are preferred but not required.

## Round 2 — cross-review

Required reviews are directional and recorded:

1. Anatomy reviews Kinematics joint locations and pose continuity; Kinematics reviews anatomical pivot and body-mass assumptions.
2. Garment reviews body-region boundaries; Layering reviews the garment-piece contract.
3. Orientation reviews every orientation-sensitive layer and artwork rule.
4. Serialization verifies that every designed pose, garment, render, anchor, and relationship state has a durable representation.
5. Integrator maps the combined proposal to current source without destructive rewriting.
6. QA tests every primitive against multiple profiles, artwork replacement, missing data, reload, and interaction combinations.

### Mandatory pose-resolution chain

A mechanically legal pose cannot proceed directly to artistic acceptance:

```text
KINEMATICS — MECHANICALLY VALID
    ↓
ANATOMICAL CONTINUITY REVIEW
    ↓
ILLUSTRATIVE RESOLUTION REVIEW — PRESENTATION RESOLVED or UNRESOLVED
    ↓
QA
    ↓
OWNER VALIDATION REQUIRED
```

Kinematics establishes legal semantic/mechanical state. Anatomy reviews body-mass relationships, joint continuity, compression/stretch, weight, and silhouette risk. Illustrative Resolution reviews seams, masks, overlap, depth, correctives, foreshortening, endpoints, and bounded deformation. QA audits evidence and state preservation. Only the owner can establish visual/workflow validation.

## Round 3 — conflict register

Every material disagreement is added to [`../DECISION_LOG.md`](../DECISION_LOG.md) with conflict ID, question, roles, evidence, options, combinatorial and technical implications, short/long-term cost, Director decision, and status. `UNRESOLVED` is an acceptable result; silent selection is not.

## Round 4 — Director synthesis

The Director produces one canonical definition of part IDs, joint IDs, orientation states, garment slots, anchors, render groups, serialization fields, author-override boundaries, and provenance. Approved contracts cross-reference one another. Proposals that cannot coexist are resolved or explicitly deferred. The Director may resolve engineering contracts but must leave artistic uncertainty as OWNER VALIDATION REQUIRED.

## Round 5 — QA gate

The Auditor evaluates the synthesized documents against [`../testing/RIG_QA_MATRIX.md`](../testing/RIG_QA_MATRIX.md). Documentation existence is insufficient. Mechanical, Combinatorial, Expressive, and Illustrative gates receive separate evidence. A designed gate result is `PASS`, `PASS WITH DOCUMENTED LIMITATIONS`, or `FAIL`; Owner Validation remains separate and cannot be manufactured by the team.

## Operating without subagents

Use separate role sections or scratch findings, freeze each role's conclusion before reading the others, then perform explicit cross-review. Do not collapse evidence gathering and Director synthesis into one untraceable opinion.

## Change control

Implementation is a later bounded pass. Contract changes require impact analysis, schema/version consequences, QA updates, a decision-log entry when material, and a new repository pass report.
