# Pose Serialization and Poser-to-Placer Transfer

## Status and document layers

This contract is **DESIGNED**. The current save-only 2d-doll-pose-0.1 fragment is **IMPLEMENTED / TESTED** but insufficient and has no load/migration path.

Four document families remain distinct:

1. ReusablePose, version 2d-doll-pose-0.2: semantic articulation/orientation and optional overlays; no camera or panel placement.
2. CharacterSnapshot inside TransferEnvelope 2d-doll-transfer-0.1: complete internal character/interaction state plus character root transform.
3. PlacerPanel: references transferred snapshots and adds panel presentation.
4. Pose-corpus entry, version `2d-doll-pose-corpus-entry-0.1`: source evidence, unresolved observations, normalization-candidate provenance, and acceptance state; not a ReusablePose.

Corpus entries declare no compatible reusable-pose schema versions. Profile/rear-three-quarter image observations, silhouette-derived proposals, source defects, and null anatomical landmarks must pass through a future reviewed adapter rather than being inferred into runtime semantics by shape.

## ReusablePose

Stores rig schema range, optional profile selector, semantic joints keyed by JointId, regional orientations and head presentation, constraint acknowledgements, optional garment-state overlay, optional semantic render/interaction overlay, and extensions. It does not own equipped garment identity, camera/editor state, or panel placement.

Hinge flexion is normalized 0…1 in canonical pose state; joint definitions map it to the designed 0°…180° mechanical domain and artwork mappings. This preserves the current elbow precedent. Cyclic shoulder/hip values normalize to [0°,360°).

## TransferEnvelope

The versioned envelope contains:

- document/schema version, creation metadata, required extension list, and resolutionMode.
- definition references: rig ID/version, body profile ID/version, artwork-set ID/version, compatible ranges or immutable hashes.
- characters with stable instanceId.
- each CharacterSnapshot: characterRootTransform; semantic pose and regional orientations; expression references; GarmentState with equipped instances, attachment bindings, state tags, requested variants, manual fit/corrective choices; semantic RenderState; anchor definition references/overrides; constraint state.
- relationships between source and target instance/anchor IDs, offsets, constraints, assistance and active/suspended/unresolved state.
- props with stable instance/asset reference and attachment relationship.
- structured unresolved issues and preserved optional extensions.

Semantic render relations are stored; derived sort order, screen anchors, raster masks, computed near/far side, automatic corrective choice, diagnostics, selection, and transient warnings are not.

## PlacerPanel

Placer adds panel position, panel scale, panel depth, framing/camera, background, foreground, effects, dialogue, captions, and panel-specific visibility. It must preserve the CharacterSnapshot and relationships rather than reconstruct joints, garment attachments, anchors, or constraints.

## Root and state ownership

ReusablePose excludes placement. TransferEnvelope preserves characterRootTransform in Poser/world interaction space. PlacerPanel adds panel placement around the snapshot. This satisfies root preservation without confusing reusable articulation with presentation.

GarmentDefinition owns topology/defaults; GarmentState owns equipped identity and editable state. A reusable pose may carry an optional overlay but cannot duplicate authoritative equipment state. RenderState stores semantic manual overrides; InteractionState stores relationships.

## Requested versus effective fallback

State preserves requestedVariant, effectiveVariant provenance, fallbackReason, and resolutionMode:

- editable drafts default to reevaluate, allowing newly available compatible assets.
- explicit transfer/publish defaults to frozen, reproducing the resolved compatible choice.

The requested semantic state always remains. Frozen mode cannot make an invalid Front/Back substitution valid.

## Validation and loading

Validate the complete document before mutating runtime state. Required major-version mismatch, missing required segment/joint, invalid orientation graph, or corrupt required field rejects atomically or opens read-only. Unknown optional extensions are preserved for round trip.

Structured issues contain path, code, severity, original value, applied migration/fallback, affected instances/versions, and repair. Missing optional visuals/anchors preserve semantic or unresolved state. Shape guessing is forbidden.

## Migration

- Current 2d-doll-pose-0.1 whole-body view expands to the same orientation across torso, pelvis, arms, and legs.
- Current normalized elbows remain unchanged and map to 0…180° mechanics.
- Other part-keyed values map through explicit segment-to-joint aliases. Back-view raw angles carry LEGACY_SEMANTIC_AMBIGUITY where meaning cannot be proven.
- Missing profile becomes an explicit inherited provisional reference, not approved female.
- Missing root defaults to identity with migration notice.
- Legacy root stage/pivot identity maps explicitly to rig_root mechanics; legacy character fields, when present, map to CharacterSnapshot.characterRootTransform rather than a joint or PlacerPanel field.
- Legacy numeric depth becomes semantic relations only where unambiguous; otherwise it remains preserved legacy metadata with warning.
- The older canonical-body-rig-0.1 raw-angle fixture is a separate document type and never inferred by shape.

## Transfer acceptance

Round trip must preserve profile/schema versions, all region/joint state, root, expressions, garments/attachments/states, semantic render relations, anchors and overrides, two-character/prop relationships, constraints, unresolved state, and extensions. Placer edits must not alter internal values.
