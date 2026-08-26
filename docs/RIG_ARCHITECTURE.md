# Canonical Poser Rig Architecture

## Status and Boundary

This document describes the first canonical runtime slice under [`app/`](../app/). It tracks source reality rather than the full desired Poser.

- **IMPLEMENTED:** Five explicit state responsibilities, complete-body camera fitting, independent character/camera transforms, editor handles, pointer-driven joint manipulation, semantic elbow mapping, reset separation, and semantic-pose serialization.
- **TESTED:** The behaviors listed in the corresponding pass report and self-running browser matrix.
- **DESIGNED:** Extending the semantic mapping mechanism to every joint and applying pose-dependent depth overrides through editor controls.
- **NOT IMPLEMENTED:** Pose load, PNG export, depth UI, touch/mobile validation, undo, final artwork, heads, expressions, clothing, interactions, IK, animation, multiple characters, and Placer features.
- **VALIDATED:** Nothing in the intended creative workflow.

The inherited runtime under `baselines/canonical_base_body_rig_v0_1/` remains byte-preserved. The canonical loader reads its manifest and aligned PNGs as provisional engineering artwork without mutating inherited files.

## State Responsibilities

### Rig Definition

`app/rig-definition.js` normalizes stable mechanical data:

- 15-part parent hierarchy;
- 17 stable pivot IDs;
- attachment metadata, including non-articulating `neck_socket`;
- per-view artwork, pivot, crop, and default depth data;
- Front ↔ 3/4 and 3/4 ↔ Back compatibility;
- semantic joint definitions and per-view visual mappings;
- the future `pose.depthOverrides` extension point.

Rig definition is stable input, not editable pose or workspace state.

### Pose State

`state.pose` contains:

- current anchor `viewId`;
- semantic joint values;
- future-compatible depth overrides;
- a versioned pose schema.

Elbows are stored as normalized `0…1` flexion. They are not stored as three view-specific rendered angles. Other joints currently store transitional semantic-degree values and use identity view mappings.

### Character / World State

`state.character` owns whole-character `x`, `y`, `rotation`, `scale`, and `flip`. Character movement never writes camera or pose state.

### Camera State

`state.camera` owns `panX`, `panY`, and `zoom`. Fit Body derives camera framing from the transformed character bounds. Reset View refits the current posed and transformed character while preserving pose and character state.

### Editor State

`state.editor` owns tool mode, selected/hovered joint, handle visibility, and transient drag state. Handles are rendered after artwork and are excluded from canonical pose serialization.

## Transform Pipeline

Rendering uses one forward pipeline:

```text
rig coordinates
→ recursive part/local articulation
→ character/world transform
→ camera transform
→ screen coordinates
```

Pointer-driven rotation uses the inverse of the exact parent-to-screen transform:

```text
screen pointer
→ inverse camera
→ inverse character/world
→ inverse parent transform
→ local visual angle
→ inverse view mapping
→ clamped semantic joint value
```

Because each part matrix composes with its parent, parent movement carries descendants. Manipulating a child does not mutate ancestor or unrelated-branch state.

## Semantic Elbow Proof Case

Each elbow has one normalized semantic flexion value and a mapping record per anchor view:

```text
semantic flexion
→ mapping offset + mapping scale × flexion
→ clamped rendered local angle
```

Front and 3/4 use their appropriate left/right signs. Back reverses those mapping scales because anatomical left/right occupy the opposite screen sides. This is data-driven through the same mapping model used by all joints, not an event-handler special case.

## Navigation and Resets

- **Fit Body:** changes camera only and contains the current transformed body within padded viewport bounds.
- **100%:** changes camera zoom around the viewport center.
- **Reset View:** refits camera only.
- **Reset Pose:** neutralizes articulation/depth overrides only.
- **Reset Character:** restores whole-character transform only.
- **Reset All:** explicitly invokes the three state resets; the current anchor view remains selected.

Wheel zoom operates around the pointer. Pan uses the Pan tool, middle-button drag, or Space+drag. Move Doll changes character X/Y; the root diamond offers the same action from any tool.

## Persistence and Presentation Boundaries

The implemented `2d-doll-pose-0.1` serialization contains view, semantic joints, and depth overrides. It excludes character/world placement, camera, and editor state. Those belong to future workspace and panel/Placer data contracts.

Artwork and editor diagnostics already use separate render phases. PNG export is deliberately deferred; no export behavior is claimed.

## Combinatorial Impact and Restrictions

The separation makes these combinations possible without duplicating pose data:

- one elbow pose across three anchor views;
- any character placement with any camera framing;
- posing while preserving placement/navigation;
- independent reset and persistence scopes;
- replacement artwork under the same mechanical contract;
- future per-view or pose-specific depth behavior without replacing the hierarchy.

Current restrictions are explicit: non-elbow mappings remain transitional, region mixing is not implemented, direct Front ↔ Back region compatibility remains disallowed, and no depth override UI exists.
