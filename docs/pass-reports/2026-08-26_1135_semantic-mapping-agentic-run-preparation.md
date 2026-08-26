# Semantic Mapping Agentic Run Preparation

## 1. Pass

- **Task:** Ingest the non-elbow verification and prepare an agentic-team run.
- **Objective:** Confirm the supplied report, collect independent specialist handoffs, resolve engineering conflicts, and publish a bounded launch brief without implementing semantic mappings.
- **Branch:** `main`
- **Starting commit:** `c760fe3f02d2cc343a440beee20b2f99fcd598a8`
- **Starting state:** `HEAD == origin/main`; the related 10:58 verification report and ledger edit were uncommitted and explicitly protected as the same dependency chain.
- **Resulting commit:** No commit was created. Documentation changes remain in the working tree.

## 2. Current Reality Before Pass

- **IMPLEMENTED / TESTED:** Generic affine mapping/inversion, recursive transforms, elbow-only semantic flexion, part-keyed pose 0.1, and the current repository suites.
- **TESTED:** The prior verification established opposite Front/Back anatomical direction for representative left shoulder, hip, and knee raw degrees.
- **DESIGNED:** Canonical cyclic shoulders/hips, normalized knees, stable JointIds, orientation mappings, requested/effective state, provenance, and separated mechanical/presentation results.
- **UNRESOLVED:** Exact launch slice, bilateral sign convention conflict, persistence boundary, unsupported-presentation behavior, 3/4 continuity, and artistic approval.
- **VALIDATED:** Nothing for this semantic slice.

## 3. Scope

### In Scope

- Normalize and compare the supplied attachment with the repository report.
- Protect the existing dirty dependency chain.
- Run independent Schema/Orientation, Anatomy/Kinematics, and Integrator/QA preparatory reviews.
- Perform Director synthesis and record a material sign-convention decision.
- Define team topology, gates, source-fit, tests, risks, and the smallest recommended implementation proof.

### Out of Scope

- Application, test, manifest, or artwork changes.
- Starting the implementation pass.
- Resolving final anatomy, artwork, silhouette, or workflow validation.
- Pose loading, undo, touch, runtime extraction, or asset-boundary work.

## 4. Changes Made

- Added `docs/rigging/SEMANTIC_MAPPING_AGENTIC_RUN_BRIEF.md`.
- Added RIG-017 to `docs/rigging/DECISION_LOG.md`.
- Added this report and its ledger entry.
- The supplied attachment was not copied because its content exactly matched the existing report after line-ending normalization.

## 5. Agentic Team Evidence

Three independent read-only groups inspected the current source, tests, designed contracts, inherited manifest/art evidence, verification report, and team protocols:

1. **Schema + Orientation:** Proposed stable JointId/SegmentId separation, explicit mapping records, requested/effective state, structured issues, and migration consequences.
2. **Anatomy + Kinematics:** Defined provisional landmark meanings, bilateral/view equations, normalized knee mechanics, cyclic shoulder/hip mechanics, and the separation between planar rig semantics and anatomical approval.
3. **Integrator + QA:** Confirmed the existing conversion, transform, and manipulation seams are reusable; identified persistence/versioning as critical; supplied automated/browser matrices and adversarial gates.

All groups preserved the existing dirty files and made no edits. Their source-fit result was feasible with material preconditions.

## 6. Director Synthesis and Conflict Resolution

The reviews agreed on data-driven mappings, stable anatomical sides, normalized knees, cyclic shoulders/hips, explicit unsupported presentation, immutable inherited assets, and no silent pose 0.1 reinterpretation.

One material conflict existed: a proposed side-independent shoulder/hip table versus the Anatomy/Kinematics bilateral rule. RIG-017 selects `direction = sideSign × viewSign`. This lets equal left/right semantic values create mirrored motion and preserves anatomical direction across views. Three-quarter remains provisional.

The prior report recommended implementing all six joints together. Team source-fit review found a smaller uncertainty-reducing sequence:

1. bilateral knees across all three views;
2. only after that passes, cyclic shoulders and hips.

This sequencing preserves the six-joint designed contract while isolating normalized hinge/persistence risk from cyclic UI and branch-cut risk.

## 7. Combinatorial Impact

The prepared contract allows one semantic knee pose to combine with anatomical side, three whole-body views, direct or numeric manipulation, hierarchy propagation, independent character/camera state, replacement presentation data, and explicit missing/unsupported states.

Separating mechanics from current-art support avoids restricting future profiles and artwork to inherited ranges. Stable JointId aliases allow source migration without silently renaming segments. The main restriction is intentional: the first proof does not make shoulders/hips semantic and does not authorize regional view mixing.

## 8. Testing / Evidence

### Repository gate

```text
branch: main
HEAD: c760fe3f02d2cc343a440beee20b2f99fcd598a8
origin/main: c760fe3f02d2cc343a440beee20b2f99fcd598a8
```

The worktree was dirty only with the related verification report and ledger entry at pass start.

### Attachment ingestion

```text
normalized attachment length: 7931
normalized repository report length: 7931
normalized content equal: True
```

### Existing executed test evidence

The parent verification pass executed:

```text
npm test
6/6 Node model tests passed
7/7 inherited verification tests passed
4/4 canonical runtime/provenance tests passed

real-browser harness
11/11 passed; 0 failed
```

Two independent groups reran `npm test` during preparation with the same passing result. The parent did not rerun the browser harness in this preparation pass. All future acceptance cases in the run brief remain **DESIGNED**, not TESTED.

## 9. Reality State After Pass

- **SPECULATIVE:** Artist-approved offsets/ranges, 3/4 anatomical continuity, final silhouettes, corrective needs, and profile-specific support.
- **DESIGNED:** RIG-017 projection rule, the agentic topology, knee-first sequencing, mapping/issue/provenance shape, persistence choices, and acceptance matrices.
- **IMPLEMENTED:** Existing elbow-only mappings and transitional raw-degree behavior; no new runtime behavior.
- **TESTED:** Existing automated/browser boundaries and prior isolated mismatch evidence only.
- **VALIDATED:** Nothing for the proposed semantic mapping workflow.

## 10. Known Limitations / Open Gates

- Verification report and this preparation chain are uncommitted; implementation may not begin as an unrelated clean pass.
- Persistence strategy is not yet selected. Normalized knees cannot silently serialize under pose 0.1 raw-degree meaning.
- Right-side and 3/4 visual behavior still need direct evidence.
- Unsupported-state rendering must be selected: ghost/warning versus an explicit provisional authoring display.
- No approved male/female profiles or final artwork exist.
- Anatomy, Illustrative, QA, and Owner Validation gates remain open.

## 11. Recommended Next Step

Close the documentation dependency chain, then authorize a design-contract freeze for the bilateral knee proof. That freeze must select the persistence strategy and unsupported-presentation behavior. Only then start a separate bounded implementation pass with tests first, followed by runtime wiring, visual continuity review, independent QA, and owner validation kept separate.
