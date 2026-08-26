# Canonical Body Rig v0.1

## Status and boundary

This is the retained canonical **DESIGNED candidate foundation** for the initial male and female body profiles. Task 000 found that its identity, state, compatibility, render, anchor, and transfer boundaries remain sound, but the architecture is incomplete without explicit anatomy-under-pose, connection-zone, illustrative-resolution, author-override, and provenance contracts. It does not claim that the complete schema, either approved profile, regional orientation, illustrative-resolution mechanisms, garments, heads, interactions, or transfer behavior exists in source.

The current app runtime remains **IMPLEMENTED / TESTED** within its narrower source-aligned boundary. The inherited baseline is immutable structural/provisional input, not approved production artwork.

The designed RigDefinition version is 2d-doll-rig-0.2. Its required top-level fields remain schemaVersion, rigId, segments, joints, hierarchy, bodyRegions, orientationContractRef, anchorDefinitions, profileCompatibility, artworkCompatibility, extensionDeclarations, and legacyAliases. Task 000 additions remain logical contracts/extensions until a bounded prototype earns exact schema fields; do not silently expand the required schema from documentation alone. The current implemented 2d-doll-rig-0.1 remains a narrower source contract and requires migration rather than silent reinterpretation.

## Canonical separations

| Contract | Owns | Must not own |
| --- | --- | --- |
| Rig definition | Stable segment/joint IDs, hierarchy, limits, regions, anchors, extensions | Profile proportions, artwork files, pose values |
| Body profile | Bind transforms, proportions, landmarks, fit measurements, overrides | New hierarchy or renamed joints |
| Artwork set | Replaceable visuals, bounds, pivot maps, masks, correctives, presentations | Mechanical identity or canonical pose |
| Pose state | Semantic joints, regional orientation, pose-dependent garment/constraint state | Camera/editor state or panel framing |
| Appearance state | Body profile, artwork set, garment instances, expressions | Panel placement |
| Render state | Semantic order, coverage, active correctives | Destructive body deletion |
| Interaction state | Anchor relationships among character/prop instances | Baked screen coordinates |
| Character root | Poser/world transform for a character or interaction group | Camera and panel framing |
| Placer panel state | Panel transform/depth, framing, environment, effects, dialogue | Reconstructed internal rig |
| Author override set | Typed reversible corrections, approval state, compatibility, provenance | Destructive artwork baking or hidden semantic-pose mutation |

## Stable identity and hierarchy

IDs are semantic data, never inferred from filenames. Anatomical side suffixes _L and _R never change with view.

~~~text
rig_root (mechanical only)
└── pelvis
    ├── thigh_L → calf_L → foot_L
    ├── thigh_R → calf_R → foot_R
    └── mid_torso
        └── chest
            ├── upper_arm_L → forearm_L → hand_L
            ├── upper_arm_R → forearm_R → hand_R
            └── neck_socket → [neck helper] → head module
~~~

The existing v0.1 segment IDs are retained to avoid a silent breaking rename. calf_L/R carry semantic role lower_leg; mid_torso carries torso_lower. A future major version may rename them only through an explicit migration.

| Node | v0.1 status | Notes |
| --- | --- | --- |
| rig_root | Required, mechanical-only | Parent of pelvis; character root is instance state. |
| pelvis, mid_torso, chest | Required segments | Artwork splits are not anatomy or garment seams. |
| Paired arm and leg segments | Required | Anatomical sides are invariant. |
| neck_socket | Required attachment/junction | Existing stable pivot; does not rotate artwork. |
| neck | Optional mechanical helper | Absence cannot remove the head-module interface. |
| head | Required semantic module slot; artwork deferred | Presentations are regular and back. |
| Wrist and ankle | Required joints | Not independent required body segments. |
| Extra twist/corrective nodes | Optional extension | Must preserve required parent semantics. |
| Masks, seams, joint covers, correctives | Render/artwork nodes | Never skeleton parents merely because they cross a joint. |

## Joint identities

| Segment | Controlling joint |
| --- | --- |
| pelvis / mid_torso / chest | pelvis / waist / chest |
| upper_arm_L/R / forearm_L/R / hand_L/R | shoulder_L/R / elbow_L/R / wrist_L/R |
| thigh_L/R / calf_L/R / foot_L/R | hip_L/R / knee_L/R / ankle_L/R |

This resolves the current transitional implementation where pose values are keyed by rotating part IDs. A future adapter must map old part-keyed pose data explicitly.

## Regions, profiles, and transforms

Orientation-owning regions are torso, pelvis, arm_L, arm_R, leg_L, leg_R, and head. Arm and leg branches are atomic in v0.1. The 3/4 state is the bridge; direct Front/Back region edges are forbidden. See [Orientation Compatibility](ORIENTATION_COMPATIBILITY_MATRIX.md).

Profiles supply bind transforms, landmarks, silhouette/fitting parameters, artwork references, and explicit presentation-limit overrides while sharing IDs and schemas. base_male_v0_1 and base_female_v0_1 are reserved designed IDs; neither is an approved implemented profile.

Rig space uses X right, Y down, and positive rotation clockwise, matching current canvas/source coordinates. Every joint value is parent-local.

~~~text
nodeLocal = profileBind × poseDelta
nodeWorld = parentWorld × nodeLocal
artworkWorld = nodeWorld × assetToNode
screen = camera × characterRoot × artworkWorld
~~~

Current common-canvas assets may use an assetToNode adapter; future assets should use node-local bounds. Character scale is positive/uniform. Presentation reflection does not swap anatomical IDs; semantic mirroring is separate.

Evaluation order: schema/version → orientation graph → profile/bind → joint clamp/wrap → view mapping → hierarchy → anchors/garment alignment → render graph/masks/correctives → character root → camera/panel.

## Task 000 body-mass and connection amendment

The required hierarchy remains small, but torso expressiveness is not reduced to unrestricted raw rotations. The retained `pelvis`, `mid_torso`, and `chest` identities may resolve a compact semantic body-mass vocabulary such as bend, twist, arch/crunch, pelvis tilt, bounded pelvis shift, and tuck. Exact fields, combinations, and limits remain **SPECULATIVE** until the Torso–Pelvis Illustrative-Resolution Spike.

Profiles/artwork may declare typed connection metadata: parent socket/contact zone, child insertion zone, safe overlap envelope, mask owner/target, default/suggested render relation, supported semantic/orientation range, and optional corrective/deformation hooks. These do not replace the mechanical pivot or become skeleton parents.

## Task 000 illustrative-resolution and tuning amendment

The canonical direction is a hybrid: semantic mechanics remain authoritative; localized corrective art, masks, semantic depth relations, endpoint variants, and evidence-justified bounded deformation resolve presentation. General deformation and complete-pose assets are not approved foundations.

Automatic presentation records requested semantics separately from derived/effective values and typed owner overrides. Generated proposal → derived result → author override → owner-approved canonical value remains reversible and version/provenance aware. The exact schema is deferred to bounded implementation evidence.

## Artwork interface

Every visual variant declares assetId/version/reference; segmentId, orientation, and side; supported profile selectors; assetSpace (node_local or legacy_common_canvas); cropBounds and pivotInCrop where applicable; assetToNode and node-local bounds; parent/child joint maps; render group/relationships; masks/coverage; corrective selectors; supported visual range; fallback policy; and compatible schema ranges. The legacy adapter derives assetToNode from crop, pivotInCrop, and named per-view pivots without changing inherited files.

Mechanical joint, anatomical landmark, artwork edge, garment seam, and mask boundary remain distinct even when coordinates overlap.

Artwork orientation fields and fallbacks consume the [Orientation Compatibility Matrix](ORIENTATION_COMPATIBILITY_MATRIX.md); filenames or available bitmaps cannot override that matrix.

## Failure behavior

- Unknown required major version: reject atomically or open read-only.
- Invalid orientation graph: preserve the last valid interactive state; strict import never partially mutates.
- Missing required artwork: preserve mechanics/state, render a diagnostic ghost, and issue a structured warning.
- Missing optional visual: use only a declared compatible fallback, otherwise omit it non-destructively and warn.
- Never infer Front/Back fallback, bind nearest coordinates, discard relationships, or delete body state.

Issues include code, severity, object/path, attempted/allowed values, versions, fallback, and explicit repair.

## Debug and authoring requirements

Authoring must expose typed root/segment/joint/anchor selection; visible pivots/anchors; identity; parent/descendant highlighting; zero rays; mechanical and visual-support arcs; region/profile display; constraint/fallback warnings; layer relationships; mask/coverage inspection; garment primary/secondary alignment; and invalid-state explanation. Diagnostics remain editor-only.

## Integration and combinatorial impact

Implementation should extend the tested transform/state seams in app/model.js and app/rig-definition.js through explicit rig/profile/artwork objects, segment-to-joint mapping, regional orientation, atomic validation, and migration from pose 0.1. The baseline remains read-only.

This grammar allows compatible profiles to share poses, garments, and anchors; artwork replacement without mechanical rewrite; declared regional bridge combinations; cross-seam garments without baked bodies; preserved interactions across panel placement; and future profiles without schema forks.

## Canonical contract map

- [Male/Female Profile Matrix](MALE_FEMALE_PROFILE_MATRIX.md)
- [Orientation Compatibility Matrix](ORIENTATION_COMPATIBILITY_MATRIX.md)
- [Joint and Constraint Model](JOINT_AND_CONSTRAINT_MODEL.md)
- [Garment Attachment Contract](GARMENT_ATTACHMENT_CONTRACT.md)
- [Layering, Masking, and Occlusion Model](LAYER_MASKING_OCCLUSION_MODEL.md)
- [Interaction Anchor Model](INTERACTION_ANCHOR_MODEL.md)
- [Pose Serialization and Transfer](POSE_SERIALIZATION_CONTRACT.md)
