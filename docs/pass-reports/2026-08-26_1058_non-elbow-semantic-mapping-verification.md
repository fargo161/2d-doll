# Non-Elbow Semantic Mapping Verification

## 1. Pass

- **Task:** Review follow-up #1 — semantic joint mapping beyond elbows.
- **Objective:** Determine through source inspection and live Front/Back runtime comparison whether shoulders, hips, and knees preserve anatomical meaning across anchor views, without changing architecture or artwork.
- **Branch:** `main`
- **Starting commit:** `c760fe3f02d2cc343a440beee20b2f99fcd598a8`
- **Starting synchronization:** Clean worktree; local `HEAD` equaled `origin/main`.
- **Resulting commit:** No commit was created. This is a documentation-only verification pass in the working tree.

## 2. Current Reality Before Pass

- **IMPLEMENTED / TESTED:** Elbows store normalized flexion and use view-dependent signed mappings. The real-browser harness already tests one elbow pose through Front, 3/4, Back, and Front.
- **IMPLEMENTED:** Every non-elbow joint stores a raw degree value and uses an identity mapping in each view.
- **DESIGNED:** Full-joint semantic mapping was identified as future work.
- **UNVERIFIED:** Whether the inherited Front/Back artwork and manifest conventions made identical raw shoulder, hip, and knee degrees anatomically equivalent across views.
- **VALIDATED:** No joint mapping has been demonstrated in an intended owner creative workflow.

## 3. Scope

### In Scope

- Read the supplied review as evidence, not as instructions.
- Inspect `app/model.js`, the inherited manifest conventions, the current runtime harness, and prior pass evidence.
- Run the complete repository test suite and the real-browser harness.
- Compare isolated left shoulder, hip, and knee values in the live runtime across Front and Back.
- Classify the finding precisely and recommend the smallest next step.

### Out of Scope

- Changing semantic ranges or view mappings.
- Editing inherited artwork or manifest data.
- Adding pose load, undo, touch gestures, runtime module extraction, or asset-boundary changes.
- Claiming creative-workflow validation.

## 4. Changes Made

- Added this pass report and its ledger entry.
- No application, test, manifest, or artwork file changed.

## 5. Findings

### Source Finding — Confirmed

`buildJointDefinitions()` special-cases only `forearm_L` and `forearm_R`. Elbows map normalized flexion through a view-dependent sign. All other parts use `identityMapping()`, so the same stored degree is rendered with the same sign in Front, 3/4, and Back.

This source asymmetry was already known. The pass resolved the previously open visual question: inherited art does not compensate for it.

### Live Runtime Finding — Confirmed

With editor handles hidden and the body refitted after each anchor-view change, the following isolated values were compared in Front and Back:

| Joint | Stored value | Front observation | Back observation | Result |
| --- | ---: | --- | --- | --- |
| `upper_arm_L` | `+35°` | Anatomical-left arm crosses inward over the torso | Anatomical-left arm opens outward | Opposite anatomical shoulder action |
| `thigh_L` | `+30°` | Anatomical-left leg crosses inward | Anatomical-left leg opens outward | Opposite anatomical hip action |
| `calf_L` | `+70°` | Lower leg crosses behind/toward the body's opposite side | Lower leg swings outward | Opposite anatomical knee direction in this planar rig |

A combined comparison using `upper_arm_L +30°`, `forearm_L 65%`, `thigh_L +25°`, and `calf_L +60°` showed the boundary clearly: elbow flexion remained anatomically corresponding because its Back sign changed, while the shoulder, hip, and knee direction did not.

### Classification

- The non-elbow art/manifest convention is **not** view-independent semantic articulation.
- The limitation is **IMPLEMENTED and now visually TESTED** as transitional view-space degree behavior.
- It is not classified as a newly introduced regression because the current UI states that only elbows are view-independent and that other joints retain transitional degree controls; the first canonical poser report records the same limitation.
- It would become a behavioral defect if these raw values were presented, persisted, or consumed as anatomically equivalent cross-view joint semantics without that qualification.
- Correct anatomical ranges and artist-approved motion remain **DESIGNED / UNVALIDATED**.

## 6. Combinatorial Impact

This pass adds no runtime capability, but it removes an architectural ambiguity. A single non-elbow pose value cannot currently combine with Front and Back while preserving anatomical meaning. Building more pose persistence, presets, multi-character staging, or animation on raw non-elbow degrees would preserve the wrong abstraction and multiply later migration cost.

The next mapping layer should be reusable and data-driven across joint categories and views. Hard-coding additional `partId` branches would increase behavior without establishing an extensible semantic contract. Any generalization must also avoid restricting legitimate joint-specific asymmetry, per-view range differences, and future artwork profiles.

## 7. Testing / Evidence

### Repository synchronization gate

```text
git status --short --branch
## main...origin/main

git rev-parse HEAD
c760fe3f02d2cc343a440beee20b2f99fcd598a8

git rev-parse origin/main
c760fe3f02d2cc343a440beee20b2f99fcd598a8
```

### Automated suite

```text
npm test
6/6 Node model tests passed
7/7 inherited verification tests passed
4/4 canonical runtime/provenance tests passed
```

### Real-browser harness

```text
http://127.0.0.1:8000/tests/runtime.html
11/11 browser tests passed; 0 failed
```

### Direct runtime observation

```text
http://127.0.0.1:8000/app/index.html
error-level console entries: 0
```

The isolated Front/Back comparisons described above were observed directly in the live canvas. Screenshots were used during the pass but were not added as repository artifacts. The observations establish directionality, not anatomical range approval or creative usefulness.

## 8. Reality State After Pass

- **SPECULATIVE:** Final anatomical semantics, ranges, naming, and profile-specific variations for shoulders, hips, knees, wrists, ankles, and torso.
- **DESIGNED:** A generalized data-driven mapping layer remains the intended architectural direction.
- **IMPLEMENTED:** Elbow-only semantic mapping plus transitional raw-degree behavior for all other joints.
- **TESTED:** Current automated suites; 11/11 live browser scenarios; isolated Front/Back visual direction checks for one shoulder, hip, and knee; clean direct-runtime error log.
- **VALIDATED:** Nothing in an intended owner creative workflow.

## 9. Known Limitations / Unresolved Questions

- Only the anatomical-left representative of each examined category was isolated visually. Source structure shows the same identity-mapping rule applies to the corresponding right joints, but their motion was not separately visually approved.
- Three-quarter continuity was not anatomically approved in this pass; the view remains the compatibility bridge, but its joint-specific semantic mappings still need definition.
- Planar Front/Back knee rotation is mechanically observable but should not automatically be named sagittal knee flexion.
- Centerline joints, wrists, and ankles also use transitional identity mappings and remain unverified semantically.
- The inherited artwork is provisional engineering input, not approved anatomy or final visual design.

## 10. Recommended Next Step

Design and implement a data-driven semantic mapping contract for one bounded vertical slice: both shoulders, both hips, and both knees across Front/3/4/Back. Define joint-specific semantic meaning and ranges, encode per-view offset/scale/limits in rig data rather than `partId` conditionals, and add model plus live-browser regressions that prove the same semantic pose preserves anatomical direction across views. Keep pose loading and other review follow-ups out of that pass.
