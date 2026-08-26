# Bilateral Knee Contract Freeze

## 1. Pass

- **Task:** Prepare the first semantic-mapping pass for review.
- **Objective:** Freeze the bilateral knee semantics, version/persistence strategy, mapping/provenance shape, unsupported-state behavior, and exact acceptance tests without runtime changes.
- **Branch:** `main`
- **Starting commit:** `c760fe3f02d2cc343a440beee20b2f99fcd598a8`
- **Starting state:** `HEAD == origin/main`; prior semantic-mapping documentation remained an explicitly protected unpublished dependency chain.
- **Resulting commit:** No commit was created. Documentation changes remain in the working tree for review.

## 2. Current Reality Before Pass

- **TESTED:** The 10:58 verification established the non-elbow Front/Back mismatch; existing suites remained green in the preparation evidence.
- **DESIGNED:** RIG-017, knee-first sequencing, data-driven mappings, normalized knees, stable JointIds, experimental persistence options, and separate support status.
- **UNRESOLVED:** One persistence choice, unsupported-state behavior, exact freeze artifact, and acceptance matrix.
- **IMPLEMENTED:** No bilateral semantic knee behavior.
- **VALIDATED:** Nothing for the proposed workflow.

## 3. Scope

### In Scope

- Treat the supplied screenshot as review evidence, not executable instruction.
- Freeze `knee_L/R` semantics and mappings across whole-body Front/3/4/Back.
- Select a non-deceptive persistence/version boundary.
- Select authoring behavior outside provisional art support.
- Define provenance, requested/effective results, issue codes, source boundary, tests, visual evidence, and gates.

### Out of Scope

- Runtime, test, manifest, or artwork changes.
- Shoulder/hip cyclic implementation.
- Pose loading/migration, full pose 0.2, regional orientations, correctives, or owner validation.

## 4. Changes Made

- Added `docs/rigging/architecture/BILATERAL_KNEE_SEMANTIC_MAPPING_CONTRACT.md`.
- Added RIG-018 and RIG-019 to the decision log.
- Linked and advanced the agentic run brief to owner-review status.
- Added this pass report and its ledger entry.

## 5. Frozen Design

- Stable joints: `knee_L` and `knee_R`; current `calf_L/R` remain child SegmentIds and explicit legacy aliases.
- Semantic value: normalized hinge flexion `[0,1]`, neutral `0`, mechanical mapping `180° × u`.
- Projection: `direction = sideSign × viewSign`; Front/3/4 view sign `+1`, Back `-1`.
- 3/4 status: `provisional_projection` with `PRESENTATION_MAPPING_UNVERIFIED`.
- Inherited art support: provisional `u ≤ 98/180`; mechanics remain legal to `1`.
- Unsupported behavior: preserve semantics and render the full provisional angle with persistent `PRESENTATION_RANGE_UNSUPPORTED`; never silently clamp.
- Persistence: exact experimental document type `2d-doll-semantic-knee-proof-0.1`; semantic elbows/knees use stable JointIds and remaining raw values live in an explicitly transitional part-degree map.
- Pose 0.1 loading/migration and full pose 0.2 remain out of scope.

## 6. Combinatorial Impact

The freeze makes one semantic knee pose combinable with anatomical side, three whole-body views, multiple manipulation paths, independent state domains, explicit unsupported presentation, and future artwork replacement without redefining mechanics.

It avoids restricting future knees to the current `98°` provisional art, avoids contaminating pose 0.1, and avoids forcing cyclic shoulder/hip mechanics into the same proof. Direct regional Front/Back mixing remains forbidden.

## 7. Testing / Evidence

### Repository gate

```text
branch: main
HEAD: c760fe3f02d2cc343a440beee20b2f99fcd598a8
origin/main: c760fe3f02d2cc343a440beee20b2f99fcd598a8
```

`git diff --check` reported no patch errors; only the repository's existing PowerShell line-ending warnings appeared.

The screenshot review was visually inspected and its recommendations were treated as evidence. No automated or browser suite was rerun because this pass changed documentation only. Every new acceptance case is recorded as **DESIGNED future testing**, not TESTED.

## 8. Reality State After Pass

- **SPECULATIVE:** Approved anatomical ranges, true 3/4 continuity, final artwork support, correctives, silhouettes, and additional profiles.
- **DESIGNED:** The complete bilateral knee freeze candidate, RIG-018, RIG-019, experimental export, issue behavior, source boundary, and acceptance matrix.
- **IMPLEMENTED:** Existing elbow-only semantic mapping and transitional raw-degree knees; no runtime change.
- **TESTED:** Prior source/runtime boundaries only; none of the new knee contract.
- **VALIDATED:** Nothing for this workflow.

## 9. Known Limitations / Open Review Questions

- Later owner review approved the experimental schema name and the change to Save Pose output within the proof; see the 11:53 owner-approval closure report.
- Later owner review approved provisional full-angle rendering with persistent structured warnings; see the 11:53 owner-approval closure report.
- Three-quarter remains explicitly unverified even though the mechanical sign is frozen provisionally.
- Right-side and all-view behavior require direct runtime evidence in the next pass.
- The documentation dependency chain remains uncommitted.

## 10. Recommended Next Step

Review and approve or amend the freeze candidate. After approval and repository-chain closure or explicit authorization, run a separate bilateral-knee implementation proof: tests first, model/runtime wiring, Front/3/4/Back evidence, Anatomy and Illustrative review, independent QA, and no shoulder/hip expansion.
