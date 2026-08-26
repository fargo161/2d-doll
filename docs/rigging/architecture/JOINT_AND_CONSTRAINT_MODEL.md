# Joint and Constraint Model

## Status and conventions

The complete model is **DESIGNED**. Current recursive/inverse transforms, propagation, root movement, clamping, and semantic elbows are **IMPLEMENTED / TESTED**.

- Rig coordinates: X right, Y down; positive rotation clockwise.
- Zero: authored neutral direction in parent-local profile bind pose.
- Elbow/knee hinge state is normalized 0…1: zero extended, one equals the 180° mechanical maximum. Profile/orientation mappings convert it to rendered degrees.
- Local = profileBind × poseDelta; world = parentWorld × local.
- No non-root translation in v0.1. Character scale is uniform/positive.
- Presentation reflection preserves IDs; semantic mirroring is separate.

Every joint declares ID, parent/child segments, pivot landmark, semantic type/unit/zero, mechanical and nominal ranges, clamp/wrap, translation policy, profile overrides, orientation maps, visual ranges, and remedy.

Precedence is explicit: the rig declares canonical mechanics; an evidence-backed body profile may narrow but never widen or redefine the semantic domain; orientation mappings convert the resulting semantic value into presentation and declare visual support but never alter mechanical truth; artwork correctives/fallbacks resolve last.

## Designed ranges

These exact defaults are mechanical design, not final anatomy or current artwork approval.

| Joint | Mechanical domain | Nominal | Behavior | Current visual evidence |
| --- | --- | --- | --- | --- |
| pelvis | -18°…+18° | same | clamp | baseline ±18° |
| waist | -14°…+14° | same | clamp | baseline ±14° |
| chest | -12°…+12° | same | clamp | baseline ±12° |
| optional neck/head | -30°…+30° | ±25° | clamp | none |
| shoulder_L/R | cyclic [0°,360°), zero arm-down | full | wrap | about ±65° |
| elbow_L/R | normalized 0…1 → flexion 0°…180° | 0…0.8333 → 0°…150° | clamp | about 0…0.6222 → 112° |
| wrist_L/R | -90°…+90° | ±60° | clamp | ±35° |
| hip_L/R | cyclic [0°,360°), zero leg-down | full | wrap | about ±38° |
| knee_L/R | normalized 0…1 → flexion 0°…180° | 0…0.8333 → 0°…150° | clamp | about 0…0.5444 → 98°; Back unapproved |
| ankle_L/R | -60°…+60° | ±45° | clamp | ±28° |

Profile overrides may narrow mechanics with evidence but cannot change units/meaning. Artwork/orientation data independently defines visual support.

## Constraint result and update

Each result has three axes:

~~~text
mechanical: allowed | wrapped | clamped | forbidden
presentation: supported | questionable | unsupported
remedy: none | orientation_swap | corrective_art | explicit_warning
~~~

A shoulder at 210° can be mechanically allowed but visually unsupported. An elbow beyond 180° is mechanically invalid. A Front/Back edge is an orientation error, not a joint-range error.

Interactive normalization displays the result. Strict imports reject invalid values; explicit repair records original/normalized values, joint, profile/orientation, and policy.

Update order is schema/orientation validation → profile bind → normalization → mapping/support → hierarchy → anchors/garment alignment → render graph/masks/correctives → root → camera/panel. Missing visuals leave a selectable mechanical ghost.

## Selection and debug

Targets are typed root, segment, joint, or anchor. Required overlays: selected identity, pivot, zero ray, mechanical arc, supported-visual arc, parent/descendants, profile/orientation, semantic/rendered value, warning/fallback, and missing-art ghost. Selection and diagnostics remain editor-only.

The [Orientation Matrix](ORIENTATION_COMPATIBILITY_MATRIX.md) supplies mappings; [Pose Serialization](POSE_SERIALIZATION_CONTRACT.md) preserves semantic values and constraint state. QA tests mechanical and presentation axes separately.
