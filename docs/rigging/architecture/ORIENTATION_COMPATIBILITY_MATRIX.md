# Orientation Compatibility Matrix

## Vocabulary and reality

Body orientations are front, three_quarter, and back. Head presentations are regular and back. Regions are torso, pelvis, arm_L/R, leg_L/R, and head.

The regional system is **DESIGNED**. The current whole-body view and bridge data are **IMPLEMENTED / TESTED**; regional mixing, validation, and fallback are not.

| Parent \ child | front | three_quarter | back |
| --- | --- | --- | --- |
| front | LEGAL | CONDITIONAL BRIDGE | FORBIDDEN |
| three_quarter | CONDITIONAL BRIDGE | LEGAL | CONDITIONAL BRIDGE |
| back | FORBIDDEN | CONDITIONAL BRIDGE | LEGAL |

CONDITIONAL BRIDGE requires an allowed region edge plus explicit profile/artwork transition, joint mapping, and compatible assets.

| Edge | Rule |
| --- | --- |
| pelvis ↔ torso | Matrix at waist |
| torso ↔ arm_L/R | Matrix at shoulder; arm branch atomic |
| pelvis ↔ leg_L/R | Matrix at hip; leg branch atomic |
| torso ↔ head | Head matrix |
| within arm/leg | All segments share one v0.1 orientation |

Thus front torso with compatible 3/4 pelvis is conditional legal; 3/4 torso with compatible front or back pelvis is conditional legal; front torso with back pelvis is forbidden; front upper arm with back forearm is forbidden.

## Head matrix

| Torso orientation | regular | back |
| --- | --- | --- |
| front | LEGAL | FORBIDDEN |
| three_quarter | LEGAL | FORBIDDEN |
| back | FORBIDDEN | LEGAL |

regular intentionally serves Front and 3/4; it is not a fallback. No third head family is introduced.

## Validation, edits, and fallback

Validate schema/vocabulary → required regions → every edge → conditional transition contract → head pair → profile/artwork/joint mapping → render/garment relations.

Interactive changes are atomic: invalid edits keep the last valid state and explain the edge. An explicit cascade action may repair descendants; silent cascading is forbidden.

- strict import rejects without partial mutation.
- diagnostic import preserves requested semantics, shows ghosts/placeholders, and reports errors.
- cascade import runs only by explicit request and records each repair.

Fallback order is exact variant → declared same-semantic-orientation fallback → mechanical ghost → omit optional visual with warning. Never substitute Front for Back, regular for back, or nearest coordinates.

Issue codes: ORIENTATION_VALUE_UNKNOWN, ORIENTATION_EDGE_FORBIDDEN, TRANSITION_UNSUPPORTED, HEAD_ORIENTATION_INCOMPATIBLE, PROFILE_ORIENTATION_UNSUPPORTED, ASSET_VARIANT_MISSING, and JOINT_MAPPING_MISSING.

Each conditional edge declares orientations, transition owner, supported joint interval, seam/mask strategy, default ordering, correctives, and fallback. The [Joint Model](JOINT_AND_CONSTRAINT_MODEL.md), [Garment Contract](GARMENT_ATTACHMENT_CONTRACT.md), and [Layer Model](LAYER_MASKING_OCCLUSION_MODEL.md) consume this matrix.
