# Canonical Rig Requirements

This document records current product-level rig requirements for 2D Doll. It is authoritative design context for rig architecture, but it is not evidence that the behavior is implemented.

## Status

The requirements below are **DESIGNED** unless a later pass report records implementation, testing, or validation.

The inherited Canonical Base Body Rig v0.1 predates the official repository and does not satisfy all of these requirements. Its known behavior is documented in `docs/audits/canonical-base-body-rig-v0.1-functional-audit.md`.

## Anchor body views

The canonical body system uses three authored anchor view families:

- **Front**
- **3/4**
- **Back**

The 3/4 view is the bridge orientation.

Compatible region mixing:
- Front ↔ 3/4
- 3/4 ↔ Back

Direct Front ↔ Back mixing is not allowed.

Represent this through reusable compatibility data or constraints rather than one-off scene logic.

## Head views

For the current scope, the head system needs only two orientation families:

- **Regular**
- **Back**

Do not require a third independent 3/4 head family merely because the body has three anchor view families.

## Semantic pose across views

A pose should describe semantic joint state rather than only raw image rotation. The same pose should map across compatible Front, 3/4, and Back visual representations.

Preferred conceptual pipeline:

```text
semantic joint state
→ view-specific mapping
→ visual rotation / view / depth representation
→ rendered part
```

Do not solve cross-view behavior by storing three unrelated copies of a pose without evidence that this is necessary.

## Articulation intent

- Shoulders: **360° conceptual motion**
- Thighs/hips: **360° conceptual motion**
- Arm segments: approximately **180° meaningful anatomical motion**
- Leg segments: approximately **180° meaningful anatomical motion**
- Torso/pelvis: deliberately the most restrictive major controls

“360° conceptual motion” does not require one PNG to rotate cleanly through 360°. View-aware artwork, depth changes, overlap handling, or view mappings may be required.

Exact numeric limits should be chosen only after the complete body is inspectable in all relevant views.

## Mechanical rig truth vs artwork

The mechanical rig is authoritative; artwork is replaceable.

Preserve where practical:

- stable part identities
- stable hierarchy
- semantic joints and pivots
- attachment points
- interaction anchors
- constraints and compatibility rules
- view mappings
- pose state

Later replacement of limbs, proportions, masks, faces, clothing, hair, or accessories should not require rebuilding sound mechanical architecture unless evidence shows the architecture itself is wrong.

## State boundaries

Keep these conceptual responsibilities separate:

### Rig definition
- hierarchy
- joints/pivots
- attachment points
- constraints
- view-specific visual mappings
- artwork references

### Pose state
- semantic joint values
- compatible region orientation/view
- pose-dependent limb depth
- future expression/clothing state
- future interaction relationships

### Character/world state
- X/Y position
- whole-character rotation
- scale
- flip/orientation

### Camera state
- pan
- zoom
- viewport

### Editor state
- selection
- hover
- handles
- guides
- active editing mode/tool
- diagnostics

These are architectural responsibilities, not a mandated class/file layout.

## Reset and export semantics

Distinguish:

- **Reset Pose** — articulation only
- **Reset Character** — character/world transform
- **Reset View** — camera
- **Reset All** — explicit combined reset

Canonical reusable pose data should not depend on editor camera state.

Character PNG export should represent the posed character independently of editor framing, with predictable bounds/resolution and without editor diagnostics.

## Limb depth

Do not permanently assume a limb is always in front of or behind the torso. Leave room for simple semantic depth choices or constrained depth rules without prematurely building a full layer editor.

## UI is not model truth

Move/Pose/Pan may be useful editing modes, but the data model must not depend on those specific UI conventions.

Underlying actions should remain separable:

- translate character
- rotate/select joint
- pan camera
- zoom camera
- change view mapping
- change depth state

## Near-term non-goals

The first mechanical overhaul should not expand into:

- final body-art redesign/proportion approval
- IK
- animation/timeline
- multi-character runtime
- clothing deformation
- full Character Creator UI
- interaction-point authoring UI
- Placer implementation
- dialogue/background/panel composition

Architecture should avoid blocking those systems without implementing them early.

## Design test

For any major rig primitive, ask:

> What new combinations become possible because this exists?

A repair that makes one current pose work while making later characters, view combinations, interactions, clothing, or Poser-to-Placer transfer harder is not an acceptable foundational solution.
