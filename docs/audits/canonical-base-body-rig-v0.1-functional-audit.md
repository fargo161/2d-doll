# Canonical Base Body Rig v0.1 — Functional Audit

**Audit date:** 2026-08-26  
**Scope:** Investigation, testing, and reporting only  
**Overall result:** **FAIL — FUNCTIONAL REPAIR REQUIRED**

## 1. Audit Result

The package contains a coherent three-view asset contract and a plausible recursive part hierarchy, but the browser viewer does not currently function as a useful interactive action doll.

The most important result is a startup-order defect in `app.js`. The program calls `render()` at line 31 before `handleCache`, `presets`, and `drag` are initialized later in the file. The first render draws the body and then throws at line 106. Because event binding happened immediately before that failed render, the interface remains visible and some controls partly update, creating the misleading impression that the viewer is healthy.

This defect directly breaks pivot rendering, pivot dragging, presets, Neutral/reset, PNG export, and clean pose loading. It does not explain everything. Independent architectural gaps also exist:

- no user-controlled body-root X/Y position;
- no camera abstraction, pan, zoom, fit-to-body, 100%, or reset-view control;
- the body is clipped at every permitted scale because its root is hard-coded at 94% of the 820 px viewer-canvas height;
- one global set of angle limits/signs is reused in Front, 3/4, and Back;
- Back-view elbow flexion therefore bends outward at the current maximums while Front bends inward;
- fixed z-order cannot express limbs moving alternately in front of and behind the torso;
- the structural validator cannot detect any of these runtime failures.

The architecture is **salvageable**. The 15-part hierarchy, asset metadata, semantic IDs, recursive matrix composition, and aligned/cropped asset sets are useful foundations. Body-art refinement should wait until a bounded functional repair pass is complete.

## 2. Current Reality

### IMPLEMENTED

- Three authored anchor views: Front, 3/4 Side, and Back.
- Fifteen articulated parts per view.
- Seventeen semantic pivot IDs shared across views.
- Recursive parent-child matrix composition.
- Per-view pivot coordinates and z-index values.
- Per-part sliders, view selection, scale, whole-body rotation, flip, boundary display, transparent background, pose presets, pose JSON save/load, and PNG export code.
- Pointer-event code for direct joint rotation.
- Aligned, cropped, mask, and outline assets.

### TESTED

- The bundled structural validator.
- All 15 joint sliders at minimum, maximum, and zero in all three views: 45 joint/view rows and 135 slider changes.
- Front → 3/4 → Back → Front view cycling with nonzero pose/stage values.
- Pivot visibility toggle and direct canvas pointer input.
- Stage scale, root rotation, flip, boundary, and transparent-background controls.
- Neutral/reset and all preset code paths.
- Pose JSON save and load.
- PNG export.
- Desktop layout in the Codex in-app browser at a captured 1264 × 880 viewport.

### VALIDATED

- The structural validator passes: three views, 45 parts, stable pivot sets, referenced assets present.
- All views contain the same 15 part IDs and the same 17 pivot IDs.
- All part pivots match their declared semantic pivot coordinates.
- Asset metadata checks found zero errors across 45 aligned RGBA layers, 45 cropped RGBA layers, 45 masks, and 45 outline layers.
- Slider DOM values and displayed degree outputs matched every configured min/max/zero value.
- Visible upper-body slider articulation works; recursive arm chains follow their parents.
- View switching preserves joint values, scale, and whole-body rotation when reset/preset is not invoked.
- Boundary outlines and transparent-background rendering work.
- Save JSON produces a valid file containing view, 15 angles, scale, whole-body rotation, and flip.

### PARTIAL

- The body image is drawn, but startup always logs an exception and pivots are omitted.
- View switching changes artwork and preserves state, but every switch logs the same render exception.
- Sliders change state, outputs, and visible upper-body geometry, but every slider event logs an exception after body drawing.
- The hierarchy is correct in source and visibly correct for upper-body examples; leg/foot behavior cannot be visually validated in the viewer because those areas are outside the canvas.
- Load JSON applies data, rebuilds controls, and redraws the body, then falsely displays “Could not load pose JSON” because the redraw exception is caught as if parsing failed.
- Scale, whole-body rotation, and flip change stage state, but they do not solve inspection or navigation.
- Fixed per-view z-order works for neutral composition but is insufficient for general crossed-limb poses.

### BROKEN

- Startup is not exception-free.
- Pivot handles never render despite the checked Pivots option.
- Direct pivot manipulation cannot begin.
- Any canvas pointer-down throws on uninitialized `handleCache`; pointer-up throws on uninitialized `drag`.
- All pose presets fail on uninitialized `presets`.
- Neutral/reset leaves stale controls and does not reset stage state.
- PNG export fails before `canvas.toDataURL()` and creates no PNG.
- Back-view elbow flexion uses the Front/3/4 signs and bends outward at the configured extremes.

### MISSING

- Body-root X/Y translation and whole-body dragging.
- Independent camera position and zoom.
- Pan, fit body, 100%, and reset view.
- A visible/draggable root handle.
- Selected-joint reset.
- Explicit Move/Pose/Pan interaction modes or another unambiguous equivalent.
- Joint selection feedback and allowed-angle arcs.
- View-aware semantic-to-visual angle mapping.
- Runtime smoke or interaction tests.

### UNCERTAIN

- Usable knee and ankle directions, overlap, detachment, and extreme-pose quality in the live viewer; the lower body cannot be seen.
- Touch behavior after the startup defect is fixed. Pointer events are used, but no successful touch manipulation was possible and the canvas has no explicit `touch-action` policy.
- Responsive/mobile layout. The desktop breakpoint source exists, but the browser’s temporary viewport override did not take effect, so a mobile result is not claimed.
- Whether exported diagnostic controls would be omitted in practice. The code intends to suppress them, but export never reaches capture.

## 3. Build / Environment

| Item | Recorded value |
| --- | --- |
| Build | Canonical Base Body Rig v0.1 |
| Schema | `canonical-body-rig-0.1` |
| Git | Not a Git repository; no branch, HEAD, or working-tree status exists |
| Standalone archive | `canonical_base_body_rig_v0_1.zip`, 6,814,607 bytes |
| Standalone SHA-256 | `1E0356AA3A1DC4A4C2555201496709E61DF13486EC79A2A271769D32720E92E7` |
| Reference archive | `codex_body_rig_reference_bundle.zip`, 119,255,140 bytes |
| Reference SHA-256 | `6D729C114947F0FC5A84AEC1AE483303C5BE5BACF6CF78B95B3A83943B97940E` |
| Current-build duplication | Core files in the standalone ZIP match `01_CURRENT_BUILD` in the reference bundle by SHA-256 |
| Run command | `python -m http.server 8000` from the project root, then `http://127.0.0.1:8000/` |
| Python | 3.12.0; the validator was also run using Python 3.12.15 by absolute path |
| Browser | Codex in-app browser |
| Captured desktop viewport | 1264 × 880 |

The supplied `RUN_BODY_RIG.bat` checks for `py` and otherwise invokes `python`; `python` is available in this environment. The audit used a local server without changing the build.

Relevant files:

- `index.html` — viewer controls and 1100 × 820 runtime canvas.
- `styles.css` — desktop two-column layout, scrolling control panel, and one-column breakpoint.
- `app.js` — state, rendering, transforms, input, save/load, and export.
- `manifest.json` / `manifest-data.js` — repeated per-view rig data.
- `docs/build_rig.py` — source generator with global `LIMITS` and hard-coded build output path.
- `docs/validate_rig.py` — structural asset validation only.
- `docs/RIG_SPEC.md` — intended rig contract.

No supplied build file was edited. Extraction and test inputs were confined to the audit work area; the outputs are this report and its evidence screenshots.

## 4. Architecture Summary

### Canvas and stage

The source assets use a 1000 × 1700 coordinate system. The browser viewer instead renders into a fixed 1100 × 820 canvas (`index.html:33`). There is no world/camera/viewport separation.

The stage transform in `app.js:88` is:

```text
translate(canvas width × 0.5, canvas height × 0.94)
→ root rotation
→ scale / horizontal flip
→ translate(-manifest root)
```

The only adjustable stage fields are `scale`, `rootRotation`, and `flip`. Root X/Y and camera state do not exist.

Measured neutral alpha bounds and resulting screen bounds prove permanent clipping:

| View | Asset alpha bounds | Screen bounds at scale 0.30 | At 0.44 | At 0.62 |
| --- | --- | --- | --- | --- |
| Front | `(240,139)–(760,1576)` | bottom `1036.6` | bottom `1160.6` | bottom `1320.1` |
| 3/4 | `(280,139)–(707,1579)` | bottom `1036.0` | bottom `1159.8` | bottom `1318.9` |
| Back | `(240,139)–(760,1576)` | bottom `1036.6` | bottom `1160.6` | bottom `1320.1` |

The runtime canvas ends at y = 820. Therefore the full body is clipped even at the minimum allowed scale.

![Initial Front view: Pivots is checked, no handles are visible, and the lower body is clipped](body-rig-front-initial.png)

### Real rig hierarchy

```text
root
└── pelvis
    ├── thigh_L
    │   └── calf_L
    │       └── foot_L
    ├── thigh_R
    │   └── calf_R
    │       └── foot_R
    └── mid_torso
        └── chest
            ├── upper_arm_L
            │   └── forearm_L
            │       └── hand_L
            └── upper_arm_R
                └── forearm_R
                    └── hand_R
```

This matches the intended conceptual structure. `app.js:90` recursively composes a child’s parent matrix with rotation around the child part’s declared pivot. Visible arm tests confirm parent movement propagates to children.

### Pivot contract

There are **17**, not 18, stable pivot IDs. `PASS_REPORT.md` incorrectly claims 18.

| Pivot ID | Front | 3/4 | Back | Parent transform / controlled part |
| --- | --- | --- | --- | --- |
| `root` | 500,690 | 515,695 | 500,690 | Stage anchor only; no part or visible handle |
| `pelvis` | 500,690 | 515,695 | 500,690 | `root` → `pelvis` |
| `waist` | 500,575 | 510,575 | 500,575 | `pelvis` → `mid_torso` |
| `chest` | 500,450 | 510,450 | 500,450 | `mid_torso` → `chest` |
| `neck_socket` | 500,150 | 510,150 | 500,150 | Attachment marker following `chest`; no rotating part |
| `shoulder_L` | 655,280 | 600,292 | 345,280 | `chest` → `upper_arm_L` |
| `elbow_L` | 702,565 | 650,562 | 298,565 | `upper_arm_L` → `forearm_L` |
| `wrist_L` | 718,810 | 666,805 | 282,810 | `forearm_L` → `hand_L` |
| `shoulder_R` | 345,280 | 405,282 | 655,280 | `chest` → `upper_arm_R` |
| `elbow_R` | 298,565 | 345,565 | 702,565 | `upper_arm_R` → `forearm_R` |
| `wrist_R` | 282,810 | 325,810 | 718,810 | `forearm_R` → `hand_R` |
| `hip_L` | 570,705 | 570,710 | 430,705 | `pelvis` → `thigh_L` |
| `knee_L` | 592,1115 | 606,1110 | 408,1115 | `thigh_L` → `calf_L` |
| `ankle_L` | 605,1480 | 620,1475 | 395,1480 | `calf_L` → `foot_L` |
| `hip_R` | 430,705 | 445,705 | 570,705 | `pelvis` → `thigh_R` |
| `knee_R` | 408,1115 | 420,1118 | 592,1115 | `thigh_R` → `calf_R` |
| `ankle_R` | 395,1480 | 410,1484 | 605,1480 | `calf_R` → `foot_R` |

`L` and `R` are consistently anatomical in the manifest: their screen positions reverse in Back. The semantic IDs do not drift between views.

### Asset representation

- The viewer uses aligned 1000 × 1700 RGBA PNGs drawn at `(0,0)` under global-coordinate transforms.
- Cropped PNGs are not used by the viewer; they are supplied for other engines with `pivotInCrop`.
- Masks are build/source artifacts and are not used for runtime clipping or hit testing.
- Outline PNGs are drawn over their matching part when Part boundaries is enabled.
- Per-view z-order is a static integer sort.
- Hidden overlap is baked into the part geometry and therefore participates in runtime transformations.

The metadata audit found no size, mode, crop, or `pivotInCrop` mismatch. The Front boundary screenshot confirms that outline layers render, while the checked pivot option still produces no handles:

![Part boundaries render, but pivots remain absent](body-rig-front-boundaries-pivots-checked.png)

## 5. Functional Test Matrix

| Area | Front | 3/4 | Back | Result | Evidence / Notes |
| --- | --- | --- | --- | --- | --- |
| Initial load | Body partly draws | Body partly draws | Body partly draws | **PARTIAL** | Startup exception at `app.js:106`; lower body clipped |
| View switching | Tested | Tested | Tested | **PARTIAL** | View, angle, scale, and root rotation persist; each switch logs an exception |
| Whole-body X/Y movement | Missing | Missing | Missing | **MISSING** | No state, UI, or pointer branch for root translation |
| Pan / camera zoom | Missing | Missing | Missing | **MISSING** | Scale changes doll, not camera; no camera model |
| Fit / 100% / reset view | Missing | Missing | Missing | **MISSING** | No controls or implementation |
| Full-body inspection | Impossible | Impossible | Impossible | **BROKEN** | Calculated bottom is 1036–1320 for an 820 px canvas at all permitted scales |
| Pivot visibility | None | None | None | **BROKEN** | Pivots checked; `handleCache=[]` throws before guide drawing |
| Direct manipulation | Fails | Fails | Fails | **BROKEN** | Pointer-down throws on `handleCache`; pointer-up throws on `drag` |
| Joint sliders | All min/0/max tested | All min/0/max tested | All min/0/max tested | **PARTIAL** | Values and outputs match; body draws before exception; lower limbs not visible |
| Shoulder hierarchy | Visible chain follows | Visible chain follows | Visible chain follows | **VALIDATED for visible arms** | Upper arm rotation carries forearm and hand |
| Elbow hierarchy | Visible chain follows | Visible chain follows | Visible chain follows | **PARTIAL** | Chain correct; Back flexion direction is wrong |
| Wrist hierarchy | Visible hand response | Visible hand response | Visible hand response | **PARTIAL** | Slider path works; direct control broken |
| Hip/knee/ankle hierarchy | Slider values tested | Slider values tested | Slider values tested | **UNCERTAIN visually** | Runtime clips the tested geometry below the canvas |
| Presets | Fail | Fail | Fail | **BROKEN** | `presets` remains uninitialized after startup abort |
| Neutral/reset | Stale UI | Stale UI | Stale UI | **BROKEN** | Angles are zeroed internally, then exception occurs before controls rebuild; stage fields are not reset |
| Save JSON | Tested | Tested | Tested | **VALIDATED** | Valid 415–416 byte JSON files observed and inspected |
| Load JSON | Data applies | Data applies | Data applies | **PARTIAL** | Loaded values appear, then a false failure alert is shown |
| PNG export | No file | No file | No file | **BROKEN** | Fails in pre-export render at `app.js:121` |
| Part boundaries | Works | Works | Works | **VALIDATED** | Outline images visibly draw before the exception |
| Transparent background | Works | Works | Works | **VALIDATED** | Viewer background is removed |
| Scale / root rotation / flip | Inputs work | Inputs work | Inputs work | **PARTIAL** | Useful transforms, but not navigation and do not prevent clipping |
| Touch/mobile | Not validated | Not validated | Not validated | **UNCERTAIN** | Direct pointer path is already broken; responsive override did not apply |

## 6. Joint-by-Joint Audit

All listed ranges are identical in Front, 3/4, and Back. Positive canvas rotation is visually clockwise; negative is counterclockwise. That raw visual sign is not mapped from a view-independent anatomical/semantic angle.

| Controlled part / semantic joint | Current range | Parent-child result | Direct manipulation | Slider status | View-specific issue |
| --- | ---: | --- | --- | --- | --- |
| `pelvis` / pelvis | -18°…18° | Carries torso, both arms, and both legs | Broken | Min/0/max values tested | Duplicates whole-body rotation concept at same root point |
| `mid_torso` / waist | -14°…14° | Carries chest and both arm chains | Broken | Min/0/max tested; visible | Same raw signs/range in all views |
| `chest` / chest | -12°…12° | Carries both arm chains | Broken | Min/0/max tested; visible | Same raw signs/range in all views |
| `upper_arm_L` / shoulder_L | -65°…65° | Forearm and hand follow | Broken | Min/0/max tested; visible | Symmetric envelope; no view-aware semantic mapping |
| `forearm_L` / elbow_L | -12°…112° | Hand follows; upper arm stays | Broken | Min/0/max tested; visible | Front/3/4 flex inward; Back +112° bends outward |
| `hand_L` / wrist_L | -35°…35° | Only hand rotates | Broken | Min/0/max tested; visible | Same raw signs/range in all views |
| `upper_arm_R` / shoulder_R | -65°…65° | Forearm and hand follow | Broken | Min/0/max tested; visible | Symmetric envelope; no view-aware semantic mapping |
| `forearm_R` / elbow_R | -112°…12° | Hand follows; upper arm stays | Broken | Min/0/max tested; visible | Front/3/4 flex inward; Back -112° bends outward |
| `hand_R` / wrist_R | -35°…35° | Only hand rotates | Broken | Min/0/max tested; visible | Same raw signs/range in all views |
| `thigh_L` / hip_L | -38°…38° | Calf and foot follow by code | Broken | Min/0/max values tested | Rendered result not fully visible |
| `calf_L` / knee_L | -8°…98° | Foot follows by code | Broken | Min/0/max values tested | Back sign is reused; visible result inaccessible |
| `foot_L` / ankle_L | -28°…28° | Only foot rotates by code | Broken | Min/0/max values tested | Entire foot inaccessible in viewer |
| `thigh_R` / hip_R | -38°…38° | Calf and foot follow by code | Broken | Min/0/max values tested | Rendered result not fully visible |
| `calf_R` / knee_R | -98°…8° | Foot follows by code | Broken | Min/0/max values tested | Back sign is reused; visible result inaccessible |
| `foot_R` / ankle_R | -28°…28° | Only foot rotates by code | Broken | Min/0/max values tested | Entire foot inaccessible in viewer |

The 3/4 articulated screenshot demonstrates that slider-driven recursive transforms work for the visible upper chains, but also shows why lower-chain validation cannot be completed:

![3/4 articulated state created through sliders; upper chains follow, lower body remains clipped](body-rig-three-quarter-articulated.png)

Front and Back use the same elbow signs even though the anatomical screen sides reverse:

![Front elbows at their configured flexion extremes](body-rig-front-elbows-current-limits.png)

![Back elbows at the same semantic limits, now bending outward](body-rig-back-elbows-current-limits.png)

## 7. Known Owner Issues

### 1. Cannot move or view the body fully — **CONFIRMED**

The body cannot be translated. The apparent root is hard-coded to `(canvas.width × 0.5, canvas.height × 0.94)`. There is no camera, pan, zoom, fit, or view reset. Scale is limited to 0.30–0.62 and the measured body bounds exceed the 820 px canvas at every value. Browser scrolling cannot reveal pixels that were never rendered into the canvas.

### 2. Articulation is too limited or directionally wrong — **CONFIRMED**

The sliders are mechanically connected to recursive transforms, but the program applies the same raw ranges/signs in every view. Front/3/4 elbow limits bend inward; Back uses the same signs after anatomical screen positions reverse, producing outward bends. The same architectural risk applies to knees. Usability is further limited because lower-joint results cannot be seen and direct manipulation is broken.

The correct architecture should separate a semantic pose angle from a per-view visual mapping:

```text
semantic joint value
→ per-view neutral offset
→ per-view direction/sign
→ per-view safe visual limits
→ rendered part rotation
```

Exact new angle numbers should be chosen only after the full body can be inspected and each view can be exercised.

### 3. Pivots are invisible or nonfunctional — **CONFIRMED**

The Pivots checkbox defaults to checked. Guide code is intended to draw after all body parts, so z-order intent is correct. Runtime never reaches that guide block: `handleCache=[]` at `app.js:106` throws. No handle cache exists for hit testing, canvas pointer-down fails, and pointer-up independently fails because `drag` is also uninitialized.

Even after the startup fix, the root pivot is not included in the part-handle loop. A distinct root/move control still needs design and implementation.

## 8. Additional Problems Found

1. **False-positive pass report.** `PASS_REPORT.md` declares “PASS WITH DECLARED ART-DIRECTION LIMITS,” but its evidence is structural validation only. It does not launch the application or check the console.
2. **Incorrect pivot count.** The pass report says 18 stable pivots; the manifest has 17.
3. **Presets are all broken.** Clicking any preset zeroes internal angles, then throws before the preset is read, controls are rebuilt, or a clean render occurs.
4. **Neutral/reset is misleading.** It zeros internal joint state but leaves displayed controls stale until a later view rebuild. It never resets scale, whole-body rotation, flip, or any future root/camera state.
5. **Pose load falsely reports failure.** A test file successfully set 3/4 view, scale 0.30, root rotation 15°, flip, and forearm_L 75°, then the render exception triggered an alert saying the JSON could not be loaded.
6. **PNG export is completely blocked.** No PNG was created; the failure occurs before capture.
7. **Fixed front/back depth.** In Front and Back, both arms are behind the torso by static z-index. General action-doll poses need at least per-view/per-limb depth choices or carefully designed pose-depth rules.
8. **Duplicate global rotation concepts.** Stage `rootRotation` and rotating the root-child `pelvis` both rotate the complete chain around nearly the same point, but have separate ranges and unclear meanings.
9. **Runtime and source canvas mismatch.** Art is authored for 1000 × 1700 while the viewer canvas is 1100 × 820 with no fit calculation.
10. **Build script portability.** `docs/build_rig.py` hard-codes `/mnt/data/canonical_base_body_rig_v0_1`; it is not directly reproducible from the supplied Windows package without changing that path.
11. **Test gap.** `validate_rig.py` checks files, view/part sets, image dimensions/mode, and nonempty alpha, but not startup, console errors, bounds, controls, transforms, save/load, or export.
12. **Control-panel scrolling.** At desktop width, the right panel has its own scrollbar while the stage remains fixed. This is usable for controls but compounds the feeling that navigation and body inspection are separate, unexplained scroll contexts.

No performance failure was observed during the local run. Touch and true mobile behavior remain uncertain rather than failed.

## 9. Root Causes

### Root cause A — startup temporal-dead-zone failure

```text
SYMPTOMS:
No pivots, broken direct manipulation, broken presets/reset/export,
false pose-load failure, repeated console errors.

CAUSE:
app.js calls render() at line 31 before const presets (line 67),
let handleCache (line 85), and let drag (line 114) initialize.
The initial render throws at handleCache=[] on line 106 and aborts
the remainder of top-level initialization.
```

During the slider matrix, 142 console errors were captured in one tab: one initial render error, three view-switch errors, three preset/reset errors, and 135 slider-render errors.

### Root cause B — no world/camera separation

```text
SYMPTOMS:
Body cannot move; feet are inaccessible; scale does not solve inspection;
camera and character movement cannot be distinguished.

CAUSE:
One hard-coded stage matrix directly maps rig coordinates to canvas coordinates.
No bodyRoot position or camera transform exists.
```

### Root cause C — view-independent raw angle configuration

```text
SYMPTOM:
Back elbows bend outward using the same limits that bend Front elbows inward.

CAUSE:
docs/build_rig.py defines one global LIMITS dictionary.
The manifest repeats those same limits for all views, and app.js applies the
stored angle directly with no view-specific offset or sign mapping.
```

### Root cause D — structural validation mistaken for functional validation

```text
SYMPTOM:
The package reports PASS although the primary interaction paths fail at startup.

CAUSE:
The validator never launches the viewer or checks console/runtime behavior.
```

### Root cause E — fixed rendering depth

```text
SYMPTOM:
Cross-body poses cannot reliably place a limb in front of or behind the torso.

CAUSE:
Parts are sorted once by static per-view zIndex; pose-dependent depth is absent.
```

## 10. Useful Improvements

### Tier A — Required for a functional action doll

| Improvement | Problem solved / user benefit | Complexity | Architectural risk |
| --- | --- | ---: | ---: |
| Correct startup ordering and add a runtime smoke test | Restores all later variables and prevents another false pass | Low | Low |
| Add `bodyRoot.x/y` and Move Doll interaction | Lets the user position the character independently | Medium | Medium; must separate from camera |
| Add camera pan/zoom plus Fit Body, 100%, Reset View | Makes the complete body inspectable | Medium | Medium; coordinate conversion must be centralized |
| Render full body by default | Makes every joint testable immediately | Low–Medium | Low once camera exists |
| Restore visible handles and pointer dragging | Delivers the advertised direct manipulation | Medium | Medium; mouse/touch hit testing and selection sync |
| Add semantic angle + per-view visual mapping | Corrects Back signs and permits evidence-based per-view ranges | Medium | Medium; pose JSON migration required |
| Make reset semantics explicit and reliable | Prevents stale controls and hidden state | Low–Medium | Low |
| Repair load/export error isolation | Makes successful load truthful and export usable | Low | Low |
| Add runtime tests for load, bounds, handles, sliders, hierarchy, save/load, export | Prevents structural validation from masking broken UX | Medium | Low |

### Tier B — Strong usability improvements

| Improvement | Benefit | Complexity | Risk |
| --- | --- | ---: | ---: |
| Selected-joint outline and angle arc | Makes active joint and legal motion obvious | Medium | Low |
| Numeric angle entry and keyboard nudging | Improves precision beyond small sliders | Low | Low |
| Undo/redo | Makes pose exploration safe | Medium | Medium; state history design |
| Per-limb front/behind depth control or constrained depth states | Enables crossed-body poses | Medium | Medium–High |
| Lock joints and isolate/hide parts | Helps diagnose hierarchy and overlap | Medium | Low |
| Pose presets after the base is stable | Offers useful starting poses and regression cases | Low | Low |
| Temporary skeleton/X-ray diagnostic mode | Makes pivots and hierarchy easier to inspect | Medium | Low |

### Tier C — Future capability

- Inverse kinematics and hand/foot targets.
- Multiple characters.
- Animation timeline, tweening, and playback.
- Clothing deformation/collision.
- Modular head, expression, hair, clothing, footwear, and accessory libraries.

Tier C should not be implemented in the next pass. The only architecture decision worth preserving now is clean separation between semantic pose state, visual view mapping, body-root/world state, and camera state.

## 11. Recommended Interaction Model

Use three visible modes, with temporary shortcuts so desktop users are not forced to click modes constantly:

### Move Doll

- Drag a visible root handle or any non-joint body region to change `bodyRoot.x/y`.
- Arrow keys nudge the doll; optional numeric X/Y fields provide precision.
- Joint handles remain visible but do not capture body-region drags unless directly targeted.

### Pose

- Hover highlights a joint; click selects it.
- Drag around the displayed pivot to rotate the correct part.
- The child chain follows recursively.
- A safe-range arc shows limits and neutral.
- Slider, numeric value, selected handle, and rendered angle stay synchronized.
- Shift provides fine adjustment.

### Pan / Zoom

- Wheel/pinch zooms around the pointer.
- Middle mouse or Space+drag temporarily pans from any mode.
- A visible Pan mode remains available for touch users.
- Fit Body, 100%, and Reset View are always accessible.

This explicit separation is preferable here because body translation, joint rotation, and camera movement all use drag gestures. Temporary Space/middle-mouse pan keeps the interaction fast without hiding the active meaning of a normal drag.

Coordinate conversion should follow one pipeline:

```text
screen pointer
→ inverse camera transform
→ world/body-root coordinates
→ inverse parent transform
→ local joint angle
```

## 12. What NOT To Do Yet

Do not spend the next pass on:

- final limb proportions;
- polished anatomy or silhouette cleanup;
- heads or expression packs;
- hair;
- clothing;
- shoes;
- accessories;
- inverse kinematics;
- animation timelines;
- multiple characters.

The current placeholder art is adequate to prove upper-body hierarchy and semantic IDs. The major barrier to leg testing is runtime clipping, not limb appearance. Artwork should only be touched if a specific overlap or pivot geometry defect remains after the full body becomes inspectable.

## 13. Recommended Next Task Pack

### Objective

Produce an exception-free, fully inspectable three-view action-doll viewer with working root movement, camera navigation, visible/direct joint controls, view-aware angle mapping, reliable reset/load/export, and automated functional checks—without changing body artwork.

### Exact files likely affected

- `app.js`
- `index.html`
- `styles.css`
- `manifest.json`
- `manifest-data.js`
- `docs/build_rig.py`
- `docs/validate_rig.py`
- new browser/runtime test file(s), for example `tests/rig-runtime.spec.js`

`manifest.json` and `manifest-data.js` should remain generated from one authoritative configuration rather than being hand-edited independently.

### Bounded implementation scope

1. Move all runtime declarations before the first initialization render; add explicit `init()` error handling.
2. Split state into:

   ```text
   semanticPose
   bodyRoot
   camera
   editorDisplay
   ```

3. Add independent world/body-root and camera matrices plus centralized forward/inverse coordinate conversion.
4. Add Move Doll, Pose, and Pan modes; whole-body drag; wheel/pinch zoom; Space/middle-drag pan; Fit Body; 100%; Reset View.
5. Restore and test handles above artwork, including a distinct root/move handle and the neck attachment marker.
6. Add view-aware joint configuration with semantic neutral/range and per-view visual sign/offset.
7. Correct reset behavior and separate “Reset Pose” from “Reset View.”
8. Repair load so render failures are not reported as parse failures; validate schema/ranges safely.
9. Repair PNG export and verify guides/outlines are omitted.
10. Add automated runtime coverage for all acceptance criteria below.

### Acceptance criteria

- Viewer loads in a supported browser with zero console errors.
- Front, 3/4, and Back initially fit completely inside the viewport, including neck socket and feet.
- Doll X/Y movement is independent of camera pan/zoom.
- Fit Body works after root movement, scale changes, and view switching.
- Every one of the 15 part handles is visible, selectable, and draggable; root movement is separately controllable.
- Direct manipulation and sliders remain synchronized at min, neutral, and max.
- Shoulder/elbow/wrist and hip/knee/ankle child propagation passes in every view.
- Back elbow flexion is semantically consistent with Front/3/4; knees are reviewed with the full body visible.
- No unrelated part moves during child-joint manipulation.
- Reset Pose produces a canonical neutral pose without silently changing camera unless explicitly specified.
- Reset View restores camera only.
- Save/load round-trips view, semantic pose, body-root position, stage flip/rotation if retained, and camera state if included by product decision.
- Export creates a valid PNG and excludes handles, arcs, labels, and outlines.
- Existing asset/pivot structural validation still passes.

### Tests

- Startup smoke test and zero-console-error assertion.
- Three-view full-body bounds assertion.
- 45-row slider min/neutral/max matrix.
- Direct pointer drag for all supported joints.
- Parent-child transform assertions for both sides.
- Root-drag versus camera-pan separation.
- Per-view sign/range regression tests, especially Back elbows and knees.
- Reset Pose and Reset View tests.
- JSON round-trip and invalid-file tests.
- Neutral/articulated export tests with diagnostics enabled in the editor.
- Desktop and touch-sized responsive checks.

### Explicit non-goals

- Body-art redesign or proportion changes.
- Heads, expressions, hair, clothing, shoes, or accessories.
- IK, animation, multi-character support, or deformation meshes.
- Unrelated architecture rewrites.

## 14. Questions for the Owner

1. When switching anchor views, should one **semantic pose** map across views, or should each view retain an independent authored pose? The recommended semantic-angle architecture assumes one pose mapped visually per view.
2. Should **Reset Pose** reset only joints, or also body position, whole-body rotation, scale, and horizontal flip? The report recommends separate Reset Pose and Reset View commands.
3. Should saved pose JSON include camera state, or should camera remain editor-only? This affects schema and reproducibility.
4. Does Front/Back posing need user-controlled limb depth (arm in front/behind torso), or are fixed depth rules acceptable for the first functional pass?
5. Should PNG export capture the full world/body at source resolution regardless of camera, or exactly the current camera viewport? Full-body source-resolution export is recommended.

## 15. Bottom-Line Recommendation

The rig is not currently a functional action doll, even though it displays a body and has many visible controls. A startup coding error prevents the advertised pivot, preset, reset, load, and export experiences from completing. Separately, the viewer has no way to move the doll or navigate a camera, and its hard-coded placement guarantees that the legs and feet stay outside the canvas. Back-view elbow motion also proves that the same raw angle signs cannot simply be reused across all views.

The good news is that the core data is worth keeping. The parts, parent hierarchy, semantic IDs, asset dimensions, crop metadata, and recursive transform approach are coherent. The smallest sensible next step is the bounded functional Task Pack above: fix startup, separate pose/body/camera state, make the full body navigable, restore direct handles, introduce view-aware angle mapping, and add runtime tests.

Do that before refining anatomy. Otherwise, art decisions will be made inside a viewer that cannot show or exercise much of the body.
