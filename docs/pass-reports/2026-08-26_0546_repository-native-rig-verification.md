# Repository-Native Canonical Body Rig v0.1 Verification

## 1. Pass

- **Pass/task name:** Repository-native inherited Canonical Base Body Rig v0.1 verification
- **Objective:** Convert the most important inherited audit claims into reproducible evidence generated from the official repository, without repairing or redesigning the preserved rig.
- **Branch:** `main`
- **Starting commit/SHA:** `b599459c43b47acfb19e640a132b4d92a91d6ac9`
- **Resulting commit/SHA:** This report is contained in the resulting verification commit. Resolve its immutable identifier with `git rev-parse HEAD`; embedding a commit's own SHA in its tracked content would change that SHA.

## 2. Current Reality Before Pass

- The worktree was clean on `main`; local `HEAD` and `origin/main` both resolved to `b599459c43b47acfb19e640a132b4d92a91d6ac9`.
- All 212 files under `baselines/canonical_base_body_rig_v0_1/` had raw worktree bytes matching their committed Git blobs. The imported provenance state was intact.
- **IMPLEMENTED:** The inherited viewer, three manifests/views, 45 segmented body-part instances, 17 stable semantic pivots, controls, pose persistence code, PNG export code, and the structural validator existed in source.
- **TESTED:** Import integrity, archive equivalence, the structural validator, and a startup smoke check had previously been tested. The smoke check had reproduced the initial `handleCache` exception.
- The remaining inherited audit findings were hypotheses/evidence from before the official repository, not repository-native TESTED claims.
- **VALIDATED:** No intended 2D Doll creative workflow.

## 3. Scope

### In Scope

- Startup and console behavior; clipping at minimum/default/maximum runtime scale; root movement and camera availability; pivots and direct manipulation; all 135 joint/view/limit states; representative hierarchy propagation; view switching and pose preservation; Back elbow direction; presets and Neutral; JSON save/load; PNG export; static depth; the semantic pivot contract; validator coverage; and bounded desktop/touch uncertainty.
- A small external gray-box harness under `tests/`, bounded pose fixtures, repository-native screenshots, this report, the report ledger, and concise README current-reality reconciliation.
- A DESIGNED acceptance boundary for the later major overhaul.

### Out of Scope

- Any change inside `baselines/canonical_base_body_rig_v0_1/`.
- Runtime repairs, architecture implementation, artwork changes, manifest changes, new joint limits, camera/root movement, depth controls, touch repairs, or overhaul work.
- Character Creator, Expression Maker, Placer, interaction points, clothing, heads, IK, animation, multiple characters, or semantic-pose implementation.

## 4. Verification Environment

| Item | Evidence |
| --- | --- |
| Operating environment | Windows, PowerShell, repository path `C:\Users\mcdon\Documents\ChatGPT\2d doll` |
| Browser | Codex in-app Chromium browser, actual desktop page interaction |
| Browser viewport | `1280 × 720` CSS pixels, device pixel ratio `1.25`; pointer reported non-coarse |
| Local server | `python -m http.server 8000 --bind 127.0.0.1`, run from the immutable baseline root |
| URL | `http://127.0.0.1:8000/` |
| JavaScript tooling | Node.js `v24.18.0`, npm `11.16.0` |
| Python tooling | Python `3.12.0`, Pillow `12.3.0`, standard-library `unittest` |
| Structural command | `python docs\validate_rig.py`, run from the baseline root |
| External harness | `python tests\verify_inherited_rig.py` and `python tests\verify_inherited_rig.py --json` |

The browser runtime did not expose mobile viewport or touch emulation. A second tab requested as `390 × 844` still reported `1280 × 720` and a non-coarse pointer. Mobile-width and actual touch behavior therefore remain **UNCERTAIN**, not passed by CSS inspection.

## 5. Repository-Native Functional Matrix

`PASS` means the bounded property was observed working. `PARTIAL` means state/code or partial drawing worked but the end-to-end behavior did not. `BROKEN` means the user path was exercised and failed. `MISSING` means no implementation exists. `UNCERTAIN` means this pass could not establish functional truth.

| Area | Front | 3/4 | Back | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| Startup | Partial frame, exception | Same after switch | Same after switch | BROKEN | First error: `ReferenceError: Cannot access 'handleCache' before initialization` at `render` (`app.js:106`) |
| Complete body at min/default/max scale | Clipped at all 3 | Clipped at all 3 | Clipped at all 3 | BROKEN | Calculated bottom bounds: Front/Back `1036.6/1160.64/1320.12`; 3/4 `1036.0/1159.76/1318.88`, canvas bottom `820` |
| Character/root X/Y movement | None | None | None | MISSING | No UI control, state field, keyboard binding, pointer path, or root-translation control |
| Camera pan/zoom/Fit/100%/Reset View | None | None | None | MISSING | Doll scale is a world transform, not camera zoom; no viewport/world separation |
| Pivot visibility | Default toggle on; handles absent | Same | Same | BROKEN | Drawing parts completes, then `handleCache=[]` throws before handle/neck-marker drawing |
| Direct pointer manipulation | Throws | Throws | Throws | BROKEN | Seven representative canvas probes produced `handleCache` and `drag` TDZ errors; no angle changed |
| Slider controls | 45/45 states accepted | 45/45 | 45/45 | PARTIAL | All 135 DOM values and degree outputs matched; every redraw emitted the `handleCache` exception |
| Upper-body hierarchy | Representative arm propagation visible | Representative arm propagation visible | Elbow extremes visible | PARTIAL | Recursive transform code plus repository screenshots; clean completion and direct manipulation absent |
| Lower-body hierarchy | Geometry clipped | Geometry clipped | Geometry clipped | UNCERTAIN | Recursive transform code exists, but hip/knee/ankle/foot visual behavior cannot be observed in the canvas |
| View switching | Front→3/4 | 3/4→Back | Back→Front | PARTIAL | Joint/stage state preserved; every switch redrew then threw |
| Back elbow semantics | Inward maximum flexion | Different projection | Outward/inconsistent maximum | BROKEN | Same raw `L=112`, `R=-112` produced inconsistent Front versus Back visual flexion |
| Presets | All fail | Same shared path | Same shared path | BROKEN | Neutral/walk/reach/crouch/twist each threw `Cannot access 'presets' before initialization` |
| Header Neutral/reset | UI/state diverge | Same | Same | BROKEN | Internal angles zero before throw; controls stay stale until a view rebuild; stage/view values are intentionally not reset by source |
| JSON save | Click produced no console error | Shared path | Shared path | UNCERTAIN | Static fields verified; no browser download event/file was observable, so payload contents were not claimed as runtime evidence |
| Valid JSON load | State applies, then false failure | Same | Same | PARTIAL | Fixture applied view, 15 angles, scale, root rotation, and flip; render error entered broad catch and reported load failure |
| Invalid JSON load | Rejected | Same | Same | PASS | Malformed fixture produced `SyntaxError`; prior state remained unchanged |
| PNG export | No file | No file | No file | BROKEN | Pre-capture `render()` throws before `toDataURL` or anchor download |
| Depth | Fixed | Fixed view-specific order | Fixed | PARTIAL | Static `zIndex` sort works; no pose-dependent or user-controlled depth |
| Pivot semantic contract | 17 IDs | Same 17 IDs | Same 17 IDs | PASS | Manifest/embedded-manifest parity and stable pivot IDs verified |
| Structural validator | Structural PASS | Structural PASS | Structural PASS | PARTIAL | It verifies structure/assets, not runtime behavior |
| Desktop/touch | Desktop tested | Desktop tested | Desktop tested | UNCERTAIN | Desktop pointer failure reproduced; mobile viewport and actual touch input unavailable |

## 6. Joint-by-Joint / View-by-View Results

Every row below was exercised at minimum, neutral (`0`), and maximum. `DOM/output PASS` means the requested in-range DOM value and displayed degree output matched for all three states. `Render PARTIAL` means the canvas draw ran far enough to update geometry before throwing on `handleCache`; it does not mean a clean render completed. Lower-body visual results remain unverified because authored/stage bounds put them below the runtime canvas.

| View | Part | Min / 0 / Max | DOM/output | Render | Visual access |
| --- | --- | ---: | --- | --- | --- |
| Front | pelvis | -18 / 0 / 18 | PASS | PARTIAL | Torso visible |
| Front | mid_torso | -14 / 0 / 14 | PASS | PARTIAL | Torso visible |
| Front | chest | -12 / 0 / 12 | PASS | PARTIAL | Torso visible |
| Front | upper_arm_L | -65 / 0 / 65 | PASS | PARTIAL | Arm visible |
| Front | forearm_L | -12 / 0 / 112 | PASS | PARTIAL | Arm visible |
| Front | hand_L | -35 / 0 / 35 | PASS | PARTIAL | Arm visible |
| Front | upper_arm_R | -65 / 0 / 65 | PASS | PARTIAL | Arm visible |
| Front | forearm_R | -112 / 0 / 12 | PASS | PARTIAL | Arm visible |
| Front | hand_R | -35 / 0 / 35 | PASS | PARTIAL | Arm visible |
| Front | thigh_L | -38 / 0 / 38 | PASS | PARTIAL | Clipped |
| Front | calf_L | -8 / 0 / 98 | PASS | PARTIAL | Clipped |
| Front | foot_L | -28 / 0 / 28 | PASS | PARTIAL | Clipped |
| Front | thigh_R | -38 / 0 / 38 | PASS | PARTIAL | Clipped |
| Front | calf_R | -98 / 0 / 8 | PASS | PARTIAL | Clipped |
| Front | foot_R | -28 / 0 / 28 | PASS | PARTIAL | Clipped |
| 3/4 | pelvis | -18 / 0 / 18 | PASS | PARTIAL | Torso visible |
| 3/4 | mid_torso | -14 / 0 / 14 | PASS | PARTIAL | Torso visible |
| 3/4 | chest | -12 / 0 / 12 | PASS | PARTIAL | Torso visible |
| 3/4 | upper_arm_L | -65 / 0 / 65 | PASS | PARTIAL | Arm visible |
| 3/4 | forearm_L | -12 / 0 / 112 | PASS | PARTIAL | Arm visible |
| 3/4 | hand_L | -35 / 0 / 35 | PASS | PARTIAL | Arm visible |
| 3/4 | upper_arm_R | -65 / 0 / 65 | PASS | PARTIAL | Arm visible |
| 3/4 | forearm_R | -112 / 0 / 12 | PASS | PARTIAL | Arm visible |
| 3/4 | hand_R | -35 / 0 / 35 | PASS | PARTIAL | Arm visible |
| 3/4 | thigh_L | -38 / 0 / 38 | PASS | PARTIAL | Clipped |
| 3/4 | calf_L | -8 / 0 / 98 | PASS | PARTIAL | Clipped |
| 3/4 | foot_L | -28 / 0 / 28 | PASS | PARTIAL | Clipped |
| 3/4 | thigh_R | -38 / 0 / 38 | PASS | PARTIAL | Clipped |
| 3/4 | calf_R | -98 / 0 / 8 | PASS | PARTIAL | Clipped |
| 3/4 | foot_R | -28 / 0 / 28 | PASS | PARTIAL | Clipped |
| Back | pelvis | -18 / 0 / 18 | PASS | PARTIAL | Torso visible |
| Back | mid_torso | -14 / 0 / 14 | PASS | PARTIAL | Torso visible |
| Back | chest | -12 / 0 / 12 | PASS | PARTIAL | Torso visible |
| Back | upper_arm_L | -65 / 0 / 65 | PASS | PARTIAL | Arm visible |
| Back | forearm_L | -12 / 0 / 112 | PASS | PARTIAL | Arm visible; semantic sign wrong |
| Back | hand_L | -35 / 0 / 35 | PASS | PARTIAL | Arm visible |
| Back | upper_arm_R | -65 / 0 / 65 | PASS | PARTIAL | Arm visible |
| Back | forearm_R | -112 / 0 / 12 | PASS | PARTIAL | Arm visible; semantic sign wrong |
| Back | hand_R | -35 / 0 / 35 | PASS | PARTIAL | Arm visible |
| Back | thigh_L | -38 / 0 / 38 | PASS | PARTIAL | Clipped |
| Back | calf_L | -8 / 0 / 98 | PASS | PARTIAL | Clipped; direction uncertain |
| Back | foot_L | -28 / 0 / 28 | PASS | PARTIAL | Clipped |
| Back | thigh_R | -38 / 0 / 38 | PASS | PARTIAL | Clipped |
| Back | calf_R | -98 / 0 / 8 | PASS | PARTIAL | Clipped; direction uncertain |
| Back | foot_R | -28 / 0 / 28 | PASS | PARTIAL | Clipped |

The matrix totals 45 part/view rows and 135 limit states. All 135 requested values and displayed outputs matched. The browser log retained up to 100 repeated instances of the same `handleCache` error; the cap means 100 is not asserted as the total number emitted.

### Parent/Child Propagation

- **Left and right arms — PARTIAL/TESTED:** Parent and child angles produce chained arm geometry in the canvas, and the transform recursion composes each child with its parent. Representative 3/4 and elbow-extreme screenshots show descendants moving with their chains. Direct manipulation never becomes usable, and clean rendering never completes.
- **Left and right legs — IMPLEMENTED but not visually TESTED:** The same recursive transform path covers thigh→calf→foot, but all relevant lower-body geometry is clipped. This pass therefore does not promote leg propagation or Back knee direction to TESTED visual behavior.
- **Branch isolation — code-level evidence only:** `calc(pid)` derives each part from its declared parent, which supports independent branches, but the clipped geometry prevents complete visual verification across all four chains.

### View/State Preservation

With `forearm_L=75`, `thigh_R=-25`, `scale=0.30`, `rootRotation=15`, and `flip=true`, Front→3/4→Back→Front preserved every observed value. Each switch rebuilt controls and redrew, then emitted the same `handleCache` exception.

## 7. Reproduced Inherited Findings

- Startup executes an initial render before `handleCache`, `presets`, and `drag` initialize. The first thrown exception is the inherited `handleCache` temporal-dead-zone error.
- Rendering is partial: images are drawn before the exception, while pivot handles and the neck marker are not drawn.
- The body is clipped at every allowed scale in all views. The cause is the combination of 1000×1700 authored alpha bounds, a 1100×820 runtime canvas, stage placement at `canvas.height × 0.94`, and a minimum doll scale of `0.30`.
- No root X/Y character movement exists. No camera pan/zoom, Fit Body, 100%, Reset View, or viewport/world separation exists.
- Direct manipulation is unusable. Pointer events reach handlers, but `handleCache`/`drag` remain uninitialized and state does not change.
- Slider values and view switching partially work but every render logs the startup-derived exception.
- Raw joint limits are identical across views. Front-versus-Back elbow screenshots reproduce anatomically inconsistent maximum flexion, supporting the inherited semantic sign/mapping concern.
- All five presets and header Neutral fail on the uninitialized `presets` binding.
- Valid JSON state applies but the subsequent render error enters a broad catch and is presented as a load failure. Malformed JSON is rejected without changing pose state.
- PNG export fails before capture because its first `render()` throws.
- Depth is fixed per view by static `zIndex`; it is neither pose-dependent nor user-controlled.
- The structural validator can pass while the viewer remains functionally broken.

## 8. Inherited Findings Not Reproduced

- Actual touch input and a true mobile-width browser viewport were not available. Desktop pointer failure was reproduced, but touch ergonomics and mobile layout remain **UNCERTAIN**.
- Back-knee semantic direction risk was not visually confirmed because the legs and feet are outside the canvas.
- Complete lower-body parent/child propagation, branch isolation, and hit testing were not visually verified for the same reason.
- The exact runtime JSON save payload was not inspected: the Save JSON click produced no console error, but the browser automation layer observed no download event or file. Source fields are known, but successful delivery remains **UNCERTAIN**.
- PNG contents, including the actual exclusion of guides/outlines, were not inspected because no PNG was produced.
- No pivot handle, root handle, or neck marker could be identified in runtime output because handle generation never begins. Their source definitions do not establish visible usability.

## 9. New Findings

- All 135 slider states update their DOM values and degree outputs, and the renderer redraws body images before throwing. The viewer is therefore more precisely classified as **PARTIAL**, not simply “nothing renders.” This partial behavior can mask the initialization failure during casual visual inspection.
- Header Neutral first zeros internal joint angles and then throws when it reads `presets`. Controls remain stale until another view rebuild: the browser showed `forearm_L=50` immediately after Neutral, then `0` after switching views. View, scale, root rotation, and flip remained unchanged. This is a concrete internal-state/UI divergence.
- The manifest contract contains exactly 17 stable pivot IDs, including `root` and `neck_socket`. The inherited historical statement of 18 pivots does not match current repository source. The inherited report remains untouched as historical evidence.
- Browser download observation is not reliable enough here to classify pose JSON save as passed or broken. This pass keeps it **UNCERTAIN** rather than inferring success from source or failure from an absent automation event.
- The first two runs of the newly added external harness failed because its scale/state regexes did not account for HTML attribute order and a nested state object. Those test-only parser bugs were corrected; the baseline was never modified, and the final seven-test suite passes.

## 10. Root-Cause Analysis

This section is verification, not a repair proposal.

1. **Initialization order:** The awaited image load resumes into `buildControls(); bind(); render();` before lexical declarations for `presets`, `handleCache`, and `drag`. `render()` draws images and then assigns `handleCache=[]`, which triggers the first temporal-dead-zone exception and aborts the async initializer permanently.
2. **Cascading interaction failures:** Event listeners were already bound, so later controls still call functions. Slider/view/display paths redraw before hitting `handleCache`; presets fail earlier on `presets`; pointer paths fail on `handleCache` and `drag`; export fails in its pre-capture render.
3. **False load failure:** `loadPose` wraps parsing, state application, control rebuilding, and rendering in one catch. A render exception after successful parsing is therefore reported as inability to load pose JSON.
4. **Clipping model:** Source images use a 1000×1700 coordinate space. Their alpha extends to approximately y=1576–1579. Runtime placement anchors the source root near 94% of an 820px-high canvas, and even the minimum scale places the visible bottom near y=1036. No camera or root translation can recover the missing region.
5. **View semantics:** One raw signed-angle table is copied across views while artwork/projection changes. The Back view therefore lacks a semantic mapping layer that can preserve “flex elbow” meaning independent of view-space sign.
6. **Depth model:** A fixed per-view `zIndex` sort has no pose state, crossing rules, or editor override. It cannot adapt to crossed-limb poses.
7. **State boundaries:** View, joint pose, doll scale, root rotation, flip, display toggles, and editor/runtime concerns share one closure state; character translation and camera state do not exist. Reset and persistence semantics are consequently incomplete and coupled.

The evidence supports a future **DESIGNED**, not implemented, separation:

```text
RIG DEFINITION
POSE STATE
CHARACTER / WORLD STATE
CAMERA STATE
EDITOR STATE
```

One semantic pose mapped into compatible Front/3/4/Back views remains the most defensible direction. It preserves intent across projections and avoids multiplying view-specific pose assets or exposing raw sign conventions as user semantics.

## 11. Structural-Validator Gap

`python docs\validate_rig.py` returned:

```text
PASS: 3 views, 45 body parts, stable pivot contract, all referenced assets present.
```

It checks:

- exactly Front, 3/4, and Back view IDs;
- 15 part IDs per view and stable pivot-set parity;
- referenced aligned/outline assets;
- 1000×1700 RGBA image contract;
- non-empty alpha and structural manifest relationships.

It does not launch a browser or check:

- startup or console errors;
- canvas placement/clipping or scale reachability;
- controls, pivots, hit testing, or direct manipulation;
- runtime parent/child behavior;
- view-state preservation or semantic direction;
- root movement or camera navigation;
- presets/reset synchronization;
- JSON save/load delivery and messaging;
- PNG export or diagnostic exclusion;
- static versus pose-dependent depth;
- desktop, mobile, or touch usability.

The validator's structural PASS is truthful within its boundary and is not a functional PASS.

## 12. Reality State After Pass

- **SPECULATIVE:** Framework choice, implementation sequencing beyond the first overhaul boundary, and final artwork/workflow details.
- **DESIGNED:** The five-way state separation above, semantic cross-view pose mapping, independent world/camera transforms, reset separation, and the acceptance criteria below.
- **IMPLEMENTED:** The unchanged inherited baseline plus a small external static/structural verification harness, two load fixtures, and repository-native evidence/reporting.
- **TESTED:** Startup, static bounds, all 135 slider states, desktop view switching/state preservation, representative upper-body articulation, Front/Back elbow extremes, all presets, Neutral divergence, display/stage controls, valid and invalid JSON load paths, PNG export failure, depth source behavior, manifest parity, pivot contract, and validator limits.
- **VALIDATED:** Nothing in the intended creative workflow.

No product behavior was repaired or promoted to canonical architecture.

## 13. Combinatorial Impact

This pass adds no creative combinations. Its value is a stronger evidence boundary: later architecture can target reusable state separations and semantic operations instead of accumulating fixes for individual views, sliders, or export buttons.

The full matrix reveals where one-off repairs would restrict expressive range. For example, negating only the Back elbow angle might fix one screenshot while leaving knees, mirrored views, pose transfer, direct manipulation, and future artwork inconsistent. Separating rig definition, semantic pose, character/world, camera, and editor state makes more combinations possible: one pose across views, independent framing, reusable reset scopes, consistent persistence, and future depth policies without baking scene-specific exceptions into assets.

The preserved baseline and external harness protect provenance and future comparison. They do not hard-code a replacement framework, angle table, or art style.

## 14. Major-Overhaul Acceptance Criteria

The later major overhaul is not complete until repository-native evidence demonstrates all applicable items:

- [ ] Clean startup in a supported desktop browser with zero uncaught exceptions and zero error-level console entries.
- [ ] Complete body, including both feet, visible and reachable at supported minimum/default/maximum scales.
- [ ] Independent character/world X and Y movement, represented in explicit state and usable without changing camera framing.
- [ ] Independent camera pan and zoom with explicit Fit Body, 100%, and Reset View behavior.
- [ ] Explicit separation of rig definition, pose state, character/world state, camera state, and editor state.
- [ ] All required semantic pivots, including root and neck attachment, visibly rendered, selectable, and identifiable.
- [ ] Pointer and touch direct manipulation works for shoulder, elbow, wrist, hip, knee, and ankle without console errors.
- [ ] Slider and direct-manipulation state remain synchronized in both directions.
- [ ] Parent motion carries descendants; child motion leaves ancestors unchanged; unrelated branches remain stable for both arms and legs.
- [ ] One semantic pose remains consistent across compatible Front, 3/4, and Back projections.
- [ ] Back left/right elbow flexion is anatomically correct at neutral and limits, without a one-off unexplained sign patch.
- [ ] Front/3/4/Back knee and ankle direction is explicitly reviewed and tested.
- [ ] View switching preserves the documented pose, character/world, stage, and editor state—and only that state.
- [ ] Pose reset, character-transform reset, camera reset, and full-session reset have explicit, separate semantics and synchronized UI.
- [ ] Every shipped preset updates state and controls, renders cleanly, remains within semantic limits, and is visible in-frame.
- [ ] Pose JSON save produces a versioned, inspectable file containing the documented fields and no accidental editor/camera leakage.
- [ ] Valid JSON load applies atomically and reports success truthfully; malformed/incompatible data fails without partial mutation.
- [ ] PNG export succeeds for neutral and articulated poses at supported views/scales.
- [ ] Exported PNG excludes pivots, boundaries, selection handles, and other diagnostics while preserving requested background/transparency.
- [ ] Limb depth supports at least extensible per-view defaults plus a documented pose-dependent or user-controlled override model.
- [ ] Automated runtime tests cover startup, console cleanliness, body bounds, all joint limits, hierarchy propagation, view semantics, persistence, reset, save/load, export, and representative pointer/touch paths.
- [ ] Mobile-width layout and actual coarse-pointer/touch behavior are tested on a supported environment.
- [ ] Original asset, manifest, pivot, and import provenance remains traceable and byte-preserved where designated.
- [ ] At least one intended posing/export workflow is owner-tested before any claim advances from TESTED to VALIDATED.

## 15. Known Limitations / Uncertainties

- No mobile viewport or touch emulation was available in the browser runtime.
- Lower-body visual and interaction truth is obstructed by clipping; source recursion is not a substitute for runtime visual proof.
- The browser automation layer did not expose a pose-save download, so save delivery and payload remain uncertain despite a no-error click and clear source fields.
- PNG output contents are unavailable because export fails before capture.
- Repeated console logs are capped by the browser tool, so their exact total was not counted.
- Screenshots document representative states, not every one of the 135 matrix states.
- The inherited audit's five missing screenshots were not fabricated or replaced under inherited filenames.
- Baseline artwork remains placeholder engineering art and has not been visually approved.

## 16. Recommended Next Step

Begin a separately authorized first major architectural overhaul pass by defining and implementing the state boundary between **rig definition**, **semantic pose**, **character/world transform**, **camera**, and **editor diagnostics**, with clean initialization and a fit-capable viewport as the first vertical slice. Preserve the inherited baseline unchanged and use this pass's tests and acceptance checklist as regression evidence. Do not start artwork redesign or downstream product systems until that slice satisfies its bounded runtime criteria.

## Changes Made and Evidence Index

- Added `tests/verify_inherited_rig.py`, `tests/README.md`, and bounded valid/invalid JSON fixtures.
- Added repository-native screenshots under `docs/evidence/2026-08-26_0546_rig-verification/`:
  - `initial-front-startup-failure.png`
  - `three-quarter-articulated-clipped.png`
  - `front-elbow-extremes.png`
  - `back-elbow-extremes.png`
  - `valid-pose-import-applied-before-render-error.png`
  - `front-maximum-scale-clipping.png`
- Updated the pass ledger and README current-reality wording.
- Changed no file under `baselines/canonical_base_body_rig_v0_1/`.

## Commands and Outcomes

```text
python tests\verify_inherited_rig.py
.......
Ran 7 tests in 0.385s
OK

python docs\validate_rig.py
PASS: 3 views, 45 body parts, stable pivot contract, all referenced assets present.
```

The first two harness development runs failed before executing tests because the newly written scale/state parser did not handle the inherited markup/state syntax. The parser was corrected externally, the final suite passed, and the immutable baseline stayed unchanged.
