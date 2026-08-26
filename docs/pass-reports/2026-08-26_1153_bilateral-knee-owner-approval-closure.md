# Bilateral Knee Owner Approval and Documentation Closure

## 1. Pass

- **Task:** Record owner approval of the bilateral-knee freeze and close the documentation dependency chain.
- **Objective:** Promote the reviewed freeze from a candidate to an owner-approved DESIGNED implementation scope, incorporate the serializer provenance caveat, and create one bounded documentation commit without starting implementation.
- **Branch:** `main`
- **Starting commit:** `c760fe3f02d2cc343a440beee20b2f99fcd598a8`
- **Starting state:** `HEAD == origin/main`; five related semantic-mapping documentation files were modified/untracked as one explicitly protected dependency chain.
- **Resulting commit:** This report is contained in the resulting bounded closure commit. Resolve its immutable identifier with `git log -1 --format=%H`; embedding a commit's own SHA in tracked content would change the SHA.

## 2. Current Reality Before Pass

- **DESIGNED / READY FOR OWNER REVIEW:** Bilateral knee semantic mapping, RIG-018 experimental persistence, RIG-019 provisional full-angle warning behavior, acceptance matrix, and knee-first run brief.
- **IMPLEMENTED:** Elbow-only semantic mapping and transitional raw-degree knees.
- **TESTED:** Existing source/runtime boundaries and prior non-elbow mismatch evidence only.
- **VALIDATED:** Nothing for the knee workflow.
- **UNPUBLISHED:** The verification, team preparation, and freeze reports remained in the working tree.

## 3. Scope

### In Scope

- Record owner approval of RIG-018 and RIG-019.
- Record the exact bilateral-knee implementation authorization boundary.
- Preserve `2d-doll-semantic-knee-proof-0.1` exactly.
- Make unsupported presentation observability mandatory.
- Preserve requested semantics as the sole authoritative pose truth while serializing non-authoritative display provenance.
- Close the related documentation chain in one commit.

### Out of Scope

- Runtime, tests, manifest, or artwork changes.
- Starting the bilateral-knee implementation.
- Shoulder/hip expansion, pose 0.1 reinterpretation, full pose 0.2, or promotion of 3/4 status.
- Claims of anatomy, artwork, presentation, or workflow validation.

## 4. Changes Made

- Promoted the bilateral-knee contract to OWNER APPROVED / DESIGNED.
- Added an explicit non-authoritative `presentationProvenance` record to the experimental serializer contract.
- Prohibited serialization of transient rendered degrees, effective pose copies, matrices, or screen state.
- Updated RIG-018 and RIG-019 with owner decisions.
- Added RIG-020 to record the exact implementation authorization boundary.
- Updated the run brief readiness and checklist.
- Added this report and its ledger entry.

## 5. Owner Decisions

- Approve `2d-doll-semantic-knee-proof-0.1` exactly as the experimental persistence boundary.
- Approve full mechanically mapped provisional rendering with persistent structured warnings beyond inherited support.
- Approve the bilateral-knee contract for implementation proof.
- Do not authorize shoulder/hip expansion.
- Do not reinterpret pose 0.1.
- Keep 3/4 as `provisional_projection + PRESENTATION_MAPPING_UNVERIFIED` until evidence exists.
- Preserve requested semantic state as authoritative; serialize enough mapping/support provenance to explain display context without storing transient rendered degrees as another pose truth.

These decisions approve a DESIGNED contract and implementation scope. They do not establish intended-workflow VALIDATION.

## 6. Combinatorial Impact

The approved boundary allows semantic knee poses to outlive current artwork support because persistence owns requested mechanics and references presentation context without baking derived visual angles. Replacement artwork can expand support without rewriting saved semantics or interaction logic.

The boundary also prevents experimental knee meaning from contaminating pose 0.1 or overstating full pose 0.2 maturity. Deferring cyclic shoulders/hips keeps the first implementation proof focused on one reusable hinge architecture.

## 7. Testing / Evidence

### Repository gate before edits

```text
branch: main
HEAD: c760fe3f02d2cc343a440beee20b2f99fcd598a8
origin/main: c760fe3f02d2cc343a440beee20b2f99fcd598a8
```

`git diff --check` reported no patch errors before this pass; only existing line-ending warnings appeared.

No automated or browser tests were run because the pass changes documentation only. All bilateral-knee implementation and acceptance tests remain **DESIGNED**, not TESTED.

## 8. Reality State After Pass

- **SPECULATIVE:** Artist-approved range, final artwork support, correctives, true 3/4 continuity, and additional profiles.
- **DESIGNED / OWNER APPROVED:** Bilateral-knee mechanics, experimental persistence, presentation warnings/provenance, implementation boundary, and acceptance gates.
- **IMPLEMENTED:** Existing elbow-only semantics and transitional knees; no knee-proof source exists yet.
- **TESTED:** Prior evidence only; none of the approved knee contract.
- **VALIDATED:** Nothing for the intended creative workflow.

## 9. Known Limitations / Open Gates

- The closure commit must be published, or its unpublished dependency chain explicitly authorized, before implementation.
- Implementation file ownership, tests-first source changes, browser evidence, Anatomy, Illustrative Resolution, and independent QA remain pending.
- Three-quarter is still provisional and warning-bearing.
- Unsupported presentation is observable but not approved.

## 10. Recommended Next Step

Publish the bounded documentation closure commit. Then begin a separate bilateral-knee implementation proof only: tests first → generic mapping/model → direct manipulation/inversion → experimental serialization → Front/3/4/Back evidence → unsupported-range evidence → Anatomy/Illustrative review → independent QA.
