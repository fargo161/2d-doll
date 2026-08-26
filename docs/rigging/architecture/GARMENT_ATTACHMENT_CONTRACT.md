# Garment Attachment Contract

## Status and principles

This contract and all examples are **DESIGNED, non-production architecture illustrations**. No garment assets or runtime garment behavior exist in the repository.

A garment is a reusable definition containing semantic pieces. Each piece has one primary mechanical owner, optional secondary alignment, and one or more render nodes. Secondary alignment never creates dual parentage. Attachments use segment-local anchors rather than screen/canvas coordinates.

## Garment definition

| Field | Requirement |
| --- | --- |
| schemaVersion | Garment contract version |
| garmentId, garmentVersion | Stable identity/version |
| semanticSlots | Slots occupied, such as upper_body, lower_body, outerwear |
| compatibleRigSchemas | Explicit version ranges |
| supportedBodyProfiles | Profile IDs/ranges or declared generic fit |
| supportedOrientationTuples | Region-orientation combinations actually authored |
| stateVocabulary | Open/closed, rolled, raised, lowered, tucked, damaged, removed, etc. |
| pieces | Semantic GarmentPiece records |
| fallbackPolicy | Ordered whole-garment behavior |

## GarmentPiece

Every piece declares:

- garmentPieceId and semanticSlot.
- owningBodyRegion and primaryParentSegmentId.
- primaryAttachmentAnchorId and one segment-local localAttachmentTransform.
- optional secondaryAnchor with mode, tolerance, and correction policy.
- anatomical side: L, R, center, or bilateral.
- supportedOrientations and supportedBodyProfiles.
- pivotBehavior: inherit, independent, locked, or corrective.
- followMode: rigid, secondary_align, joint_cover, or future_deform.
- renderNodes, each with renderNodeId, asset reference/version, group, relations, bounds, and variant selectors.
- occlusionBehavior and MaskRule references.
- bodyCoverage semantic targets.
- neighboringPieces and CrossJointRelationship.
- correctiveArtRefs selected by semantic joint/profile/orientation/state.
- garmentStateTags.
- fallbackPolicy and rig/garment/profile compatibility ranges.

CrossJointRelationship identifies jointId, adjacentPieceId, seam mode, overlap, secondary alignment, mask/coverage, and corrective selector. Primary ownership, secondary alignment, masking, seam overlap, corrective art, and future deformation remain distinct.

## AttachmentAnchor contract and vocabulary

AttachmentAnchor is a typed module-binding point, distinct from MechanicalPivot, FitLandmark, and InteractionAnchor. Each record declares stable attachmentAnchorId; ownerSegmentId; owner-local position, rotation, and axes; anatomical side; semanticPurpose; compatible semanticSlots/piece roles; supported body profiles/orientations; version and rig compatibility; constraints; and explicit fallback anchor/policy.

Required initial garment-binding IDs are attach.chest_garment, attach.waist_garment, attach.pelvis_garment, and paired attach.shoulder_L/R, attach.upper_arm_L/R, attach.elbow_L/R, attach.forearm_L/R, attach.wrist_L/R, attach.hip_L/R, attach.thigh_L/R, attach.knee_L/R, attach.lower_leg_L/R, attach.ankle_L/R, and attach.foot_L/R. Profile definitions supply their local transforms. Optional garment-specific anchors use namespaced extensions and cannot replace required IDs.

Coincident pivots or FitLandmarks may seed an anchor only through an explicit mapping. A secondary AttachmentAnchor measures/alters alignment or selects correctives; it never becomes a second mechanical parent.

## Variant and fallback

An asset variant selects by piece, body profile, owning-region orientation, side, garment state, and semantic joint band. A cross-region piece declares the complete orientation tuple it supports.

Fallback order:

1. Exact variant.
2. Explicit compatible variant with the same semantic orientation.
3. Explicit garment-state fallback.
4. Omit the unavailable visual non-destructively, preserve equipped/state data, reveal underlying body, and warn.
5. Apply an explicitly declared whole-garment fallback if dependent pieces cannot remain coherent.

Authoring may show a diagnostic ghost; export omits diagnostics and is blocked if a required visual remains unresolved. Never infer Front/Back, stretch an unsupported profile silently, or bind to nearest coordinates.

## Worked example 1 — fitted shirt

Shared illustration values: garmentId shirt.fitted.example; slots upper_body; profiles base_male_v0_1 and base_female_v0_1; states closed, open_collar, sleeves_rolled, removed; orientations exact Front/3/4/Back variants; fallback preserves garment state and omits unresolved optional nodes.

| Piece | Owner / primary binding | Secondary / follow | Render, coverage, seam |
| --- | --- | --- | --- |
| bodice | torso / chest / attach.chest_garment | attach.waist_garment; secondary_align | wearable_core; covers chest and mid_torso; shirt-body masks; neighbors upper sleeves |
| upper_sleeve_L/R | arm_L/R / upper_arm_L/R / attach.upper_arm_L/R | attach.shoulder_L/R; rigid | wearable far/near resolved by orientation; covers upper arm; elbow seam to lower sleeve |
| lower_sleeve_L/R | arm_L/R / forearm_L/R / attach.forearm_L/R | attach.elbow_L/R; rigid | covers forearm; semantic elbow-band correctives; neighbor cuff |
| cuff_L/R | arm_L/R / hand_L/R / attach.wrist_L/R | lower-sleeve seam; joint_cover | near wearable; covers wrist seam without owning hand |

All pieces declare side, local transform, profile/orientation variants, pivot behavior inherit, asset versions, compatible rig range, and missing-variant policy. Rolled sleeves hide lower-sleeve/cuff render nodes through state, not deletion; the arm remains intact.

## Worked example 2 — segmented trousers

Shared values: garmentId trousers.segmented.example; slot lower_body; states closed, cuffed, damaged, removed; profiles both designed bases; per-region orientation tuple covers pelvis and both atomic leg branches.

| Piece | Owner / primary binding | Secondary / follow | Render, coverage, seam |
| --- | --- | --- | --- |
| pelvis_yoke | pelvis / pelvis / attach.pelvis_garment | waist fit landmark; secondary_align | wearable_core; covers pelvis; neighbors both thigh pieces |
| thigh_L/R | leg_L/R / thigh_L/R / attach.thigh_L/R | attach.hip_L/R; rigid | wearable far/near; covers thigh; knee seam relationship |
| lower_leg_L/R | leg_L/R / calf_L/R / attach.lower_leg_L/R | attach.knee_L/R; rigid | covers calf; correctives by normalized knee flexion |
| knee_cover_L/R optional | leg_L/R / calf_L/R / attach.knee_L/R | thigh piece; joint_cover | seam overlay/mask; does not replace thigh or calf piece |

Each piece carries local transform, side, variants, masks, coverage, neighbors, correctives, state tags, and version compatibility. Cuffed state changes lower-leg visual selection. Removing trousers restores unchanged body state.

## Worked example 3 — cross-region coat

Shared values: garmentId coat.long.example; slots outerwear and upper_body; states open, closed, raised, damaged, removed; supported tuples must be declared for torso/pelvis/arms.

| Piece | Owner / primary binding | Secondary / follow | Render, coverage, seam |
| --- | --- | --- | --- |
| torso_back_panel | torso / chest / attach.chest_garment | waist anchor; secondary_align | wearable_far; orientation-specific back panel and masks |
| torso_front_L/R | torso / chest / attach.chest_garment | waist/pelvis alignment; secondary_align | wearable_core/near; covers torso; open/closed relations |
| lower_panel_L/R | pelvis / pelvis / attach.pelvis_garment | torso seam anchor; secondary_align | covers leg pixels non-destructively; may have far/near render nodes |
| upper/lower_sleeve_L/R | arm branches / exact upper_arm_L/R or forearm_L/R segment | shoulder/elbow attachment | rigid pieces plus joint correctives; arm-owned despite coat connection |
| collar/cuff correctives | torso or arm primary owner | adjacent piece alignment; joint_cover | separate render nodes, masks, and conditional artwork |

A coat piece may instantiate front/back render fragments but retains one primary owner. A tuple containing direct Front torso/Back pelvis is rejected before render planning; layering cannot repair invalid orientation.

## State ownership

GarmentDefinition owns topology/defaults. GarmentState owns equipped instances, tags, manual fit offsets, requested variants, and manual corrective choices. RenderState stores only semantic manual order/coverage overrides. A reusable pose may carry an optional garment-state overlay, but garment identity is not a joint value.

The [Layer Model](LAYER_MASKING_OCCLUSION_MODEL.md) owns common render types, the [Orientation Matrix](ORIENTATION_COMPATIBILITY_MATRIX.md) owns view legality, and [Pose Serialization](POSE_SERIALIZATION_CONTRACT.md) preserves instances and state.
