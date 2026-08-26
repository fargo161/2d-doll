# First Canonical Poser Architecture Slice

## 1. Pass

- **Task:** First major architectural overhaul pass
- **Objective:** Establish a new functional canonical runtime outside the immutable inherited baseline with explicit state boundaries, complete-body navigation, independent character/camera movement, direct manipulation, one semantic elbow pose across Front/3/4/Back, and repository-native tests.
- **Branch:** `main`
- **Starting SHA:** `ab472cd4d7e7886cfa70aa9cc7ffdd7695568e36`
- **Resulting SHA:** This report is contained in the resulting implementation commit. Resolve that immutable identifier with `git rev-parse HEAD`; embedding a commit's own SHA in tracked content would change the SHA.
- **Suggested/final commit subject:** `feat: establish canonical poser rig architecture`

## 2. Current Reality Before Pass

- The worktree was clean on `main`; local `HEAD` and `origin/main` both resolved to the repository-native verification SHA.
- All 212 inherited baseline files had no diff from that SHA.
- **IMPLEMENTED:** The inherited v0.1 viewer contained useful 15-part hierarchy, 17-pivot semantics, aligned assets, and recursive transforms.
- **TESTED:** The inherited verifier and structural validator passed inside their declared evidence boundaries.
- **BROKEN/MISSING:** Clean startup, full-body reachability, root X/Y movement, camera navigation, usable handles/direct manipulation, view-aware semantic pose mapping, scoped resets, and runtime tests.
- **DESIGNED:** Five state responsibilities and one semantic pose mapped across views.
- **VALIDATED:** Nothing in the intended creative workflow.

## 3. Scope

### In Scope

- New plain-browser canonical runtime outside `baselines/`.
- Explicit rig, pose, character/world, camera, and editor boundaries.
- Complete-body Fit Body, 100%, Reset View, pan, and pointer-centered wheel zoom.
- Independent character X/Y movement plus scale, rotation, and flip.
- Visible root, all 15 articulated joint handles, and neck attachment marker.
- Pointer-driven representative shoulder/elbow/wrist/hip/knee/ankle rotation.
- Slider/numeric/direct-manipulation synchronization.
- Semantic elbow flexion mapped across Front, 3/4, and Back.
- Exact reset scopes, minimal pose serialization, extensible depth boundary, tests, and source-aligned documentation.

### Out of Scope

- Changes to inherited baseline files or body artwork.
- Full semantic mapping for non-elbow joints.
- Region mixing, depth editor UI, pose load, PNG export, touch/mobile validation, undo/redo, presets, IK, animation, multiple characters, final artwork, heads, expressions, hair, clothing, footwear, accessories, interaction authoring, Character Creator, or Placer.

## 4. Architecture Before

The inherited runtime combined view, raw joint angles, doll scale/rotation/flip, display toggles, and transient editor behavior in one closure state. It directly mapped rig coordinates through one hard-coded stage matrix to the canvas. Character X/Y and camera state did not exist. Raw view-space angle signs were canonical pose truth.

The inherited source remains unchanged as provenance and failure-baseline evidence.

## 5. Architecture After

The canonical source under `app/` implements five explicit responsibilities:

### Rig Definition — IMPLEMENTED / TESTED

- Stable hierarchy, parts, pivots, attachments, crop bounds, asset references, default per-view depth, view compatibility, semantic joint definitions, and view mappings.
- Reads inherited manifest/artwork as immutable provisional engineering input.
- Declares `pose.depthOverrides` as the extensible override boundary; editor UI remains **DESIGNED_NOT_IMPLEMENTED**.

### Pose State — IMPLEMENTED / TESTED

- Versioned semantic joints, anchor view, and depth overrides.
- Elbows use normalized flexion; other joints retain explicitly transitional semantic-degree values.
- Contains no camera data.

### Character / World State — IMPLEMENTED / TESTED

- Independent X, Y, rotation, scale, and flip.

### Camera State — IMPLEMENTED / TESTED

- Independent pan X/Y and zoom.
- Fit derives framing from the current transformed character bounds.

### Editor State — IMPLEMENTED / TESTED

- Tool, selection, hover, handle visibility, and transient drag state.
- Editor diagnostics are rendered after artwork and excluded from pose serialization.

## 6. Source / File Changes

- `app/index.html` — canonical editor surface and startup error recording.
- `app/styles.css` — functional desktop/responsive layout and handle/tool clarity.
- `app/model.js` — matrices, mappings, state creation, transforms, bounds, fitting, resets, and persistence boundary.
- `app/rig-definition.js` — immutable inherited-data adapter, view compatibility, attachment/depth contract, and artwork loading.
- `app/runtime.js` — lifecycle, rendering, controls, pointer interaction, navigation, diagnostics, and test API.
- `package.json` — dependency-free test entry point.
- `tests/model.test.mjs` — pure model/state/transform checks.
- `tests/verify_canonical_runtime.py` — new-runtime structure and baseline-diff checks.
- `tests/runtime.html` / `tests/runtime-browser-tests.js` — self-running real-browser runtime matrix.
- `README.md`, `docs/RIG_ARCHITECTURE.md`, `tests/README.md`, and pass ledger — current-reality documentation.

No file under `baselines/canonical_base_body_rig_v0_1/` changed.

## 7. Initialization Model

The runtime uses one awaited lifecycle:

```text
load rig definition
→ load artwork
→ create separated state
→ build/bind editor
→ fit camera
→ render
→ publish ready event/API
```

A fresh direct browser tab reached `ready` with no uncaught exception, no recorded unhandled rejection, and zero error-level console entries.

## 8. Coordinate / Transform Pipeline

Forward rendering:

```text
rig coordinates
→ recursive local part matrices
→ character/world matrix
→ camera matrix
→ screen
```

Inverse direct manipulation:

```text
screen pointer
→ inverse camera
→ inverse character/world
→ inverse parent matrix
→ local visual angle delta
→ inverse view mapping
→ clamped semantic joint value
→ render
```

Fit Body transforms every part crop corner through its body and character matrices, unions the world bounds, and derives padded camera pan/zoom. It therefore continues to work after view, pose, character movement, character scale, character rotation, and camera changes.

## 9. Semantic Pose Mapping

Both elbows store normalized `0…1` flexion. Each view mapping has reusable `offset`, `scale`, `visualMin`, and `visualMax` data.

- Left elbow at `0.75`: Front `84°`, 3/4 `84°`, Back `-84°`.
- Right elbow at `0.75`: Front `-84°`, Back `84°`.
- Mapping inversion returns the same semantic value during direct manipulation.

The Back result uses the same mapping engine, not a Back-specific event-handler branch. Browser evidence visually showed Back anatomical-left 75% flexion bending inward.

## 10. Functional Test Matrix

| Behavior | Evidence | Result |
| --- | --- | --- |
| Clean startup | Fresh direct app tab; runtime error array and browser error log | PASS |
| Front/3/4/Back Fit Body | Browser bounds assertions with 54 px target padding | PASS |
| Character drag | Synthetic pointer path through real canvas listeners | PASS |
| Camera pan | Pan tool path; character unchanged | PASS |
| Pointer-centered wheel zoom | Wheel path; pose unchanged | PASS |
| Fit Body / 100% / Reset View | Runtime/browser tests and visual inspection | PASS |
| Root/joint/attachment handles | 1 root + 15 joint + 1 attachment classification | PASS |
| Joint selection | Direct drag updates selected joint/control row | PASS |
| Representative direct manipulation | Shoulder, both elbows, wrist, hip, knee, ankle | PASS |
| Control synchronization | Elbow slider and numeric input match pointer result | PASS |
| Arm/leg hierarchy | Parent propagation, child ancestor stability, branch isolation | PASS |
| Cross-view elbow semantics | Front→3/4→Back→Front, same semantic value | PASS |
| Reset scopes | Pose, Character, View, and All exact-scope assertions | PASS |
| Pose persistence boundary | Versioned semantic data; no camera/character/editor | PASS |
| View compatibility/depth boundary | 3/4 bridge and override contract assertions | PASS |

## 11. Direct Manipulation Results

Pointer rotation passed through actual canvas event listeners for:

- left shoulder;
- left and right elbow;
- left wrist;
- left hip;
- left knee;
- left ankle.

Every case changed the intended semantic value, selected the matching joint, clamped through joint definition data, and produced no app error. The elbow case also synchronized its slider and numeric input.

Other same-model joints are **IMPLEMENTED** but were not all individually pointer-dragged; the representative acceptance boundary was used.

## 12. Hierarchy Results

- Rotating `upper_arm_L` moved elbow/wrist descendants while the shoulder pivot and right arm remained stable.
- Rotating `forearm_L` moved the wrist while shoulder/elbow pivots, ancestors, and the right arm remained stable.
- Rotating `thigh_L` moved knee/ankle descendants while the hip pivot and right leg remained stable.
- Pure model tests also confirmed recursive composition without mutation of child canonical pose values.

These behaviors are **TESTED**, not creatively **VALIDATED**.

## 13. View / Camera / Character State Results

With non-neutral elbow flexion plus non-default character and camera state, Front→3/4→Back→Front preserved:

- semantic elbow value;
- all character/world fields;
- all camera fields.

Only the derived local rendered elbow angle changed by view mapping. Character drag left camera and pose unchanged. Camera pan left character unchanged. Zoom left pose unchanged.

## 14. Reset Semantics

- **Reset Pose:** articulation and depth overrides only.
- **Reset Character:** X/Y, whole-character rotation, scale, and flip only.
- **Reset View:** camera refit only, using the current posed/transformed character.
- **Reset All:** explicit pose + character + camera reset; current anchor view remains selected.

All scopes passed browser assertions with UI synchronization.

## 15. Automated Test Results

### Dependency-Free Repository Suite

```text
npm test

6/6 Node model tests passed
7/7 inherited verification tests passed
4/4 canonical structure/provenance tests passed
```

### Real-Browser Harness

```text
http://127.0.0.1:8765/tests/runtime.html
11/11 browser scenarios passed; 0 failed
```

### Direct App Console Check

```text
http://127.0.0.1:8765/app/index.html
lifecycle: ready
error-level console entries: 0
recorded runtime errors: 0
```

The browser harness uses the real runtime and artwork in a same-origin frame. One browser-automation instrumentation error occurred on the outer harness page while attaching observation; the direct application tab and its own runtime error recorder remained clean. The clean-start claim is therefore based on the direct app tab, not that unrelated outer-page instrumentation message.

## 16. Baseline Provenance Check

- Starting repository SHA: exact verification commit.
- Baseline file count: 212 tracked files.
- `git diff ab472cd... -- baselines/canonical_base_body_rig_v0_1`: empty before and after implementation.
- Inherited external verifier: 7/7 passed.
- Inherited structural validator: PASS for 3 views, 45 body parts, stable pivot contract, and referenced assets.

Baseline preservation is **TESTED**.

## 17. Reality State After Pass

- **SPECULATIVE:** Final artwork, full downstream product workflows, and framework choices beyond this plain-browser slice.
- **DESIGNED:** Full-joint semantic mapping, depth override UI, persistence load/workspace/panel schemas, export, and touch/mobile validation plans.
- **IMPLEMENTED:** The new canonical runtime and state/transform architecture described above.
- **TESTED:** The exact automated and browser behaviors in this report.
- **VALIDATED:** Nothing in an intended owner creative workflow. Owner testing is still required before that claim.

The canonical runtime is a functional mechanical slice, not a complete Poser.

## 18. Combinatorial Impact

> What new combinations become possible because this architecture exists?

- One semantic elbow pose can combine with any of three anchor views.
- Any pose can combine with independent character placement and camera framing.
- Navigation, posing, and placement can be reset or persisted without corrupting one another.
- Stable rig mechanics can combine with replacement artwork without rewriting editor logic.
- Editor selection/diagnostics can combine with rendering without becoming pose/export truth.
- Per-view default depth can later combine with pose-specific overrides without replacing the hierarchy.
- The mapping mechanism can extend to knees, shoulders, wrists, hips, ankles, and torso without multiplying view-specific pose copies.

Current restrictions are intentional: region mixing is absent, Front↔Back direct region compatibility remains disallowed, non-elbow semantics remain transitional, and depth overrides lack an editor surface.

## 19. Known Limitations

- Only elbows have normalized, cross-view semantic mappings.
- Other joints expose transitional degree values; Back knee/ankle semantics are not approved.
- Direct pointer tests cover representative joints rather than every one of 15 handles in every view.
- Actual touch/coarse-pointer and mobile-width behavior remain untested.
- Depth defaults and override state exist, but pose-dependent/user depth controls do not.
- Pose save exists; pose load and atomic schema validation do not.
- PNG export is deferred; diagnostic exclusion is architectural, not export-tested.
- No presets, undo/redo, keyboard nudge, numeric X/Y drag constraints, or selected-joint arc.
- Provisional inherited engineering artwork remains unapproved.
- No intended owner workflow has been creatively validated.

## 20. Recommended Next Pass

Extend semantic mapping through the full joint set, beginning with knees and shoulders while the full body is now observable. Define anatomical semantic ranges and per-view mapping data, add all-view direct-manipulation regressions for both sides, and keep artwork unchanged. Do not combine that work with persistence/export or depth UI unless evidence shows a required dependency.
