# Layering, Masking, and Occlusion Model

## Status

This semantic model is **DESIGNED**. Current per-view numeric z-index defaults and stored depth overrides are **IMPLEMENTED / narrowly TESTED**; contextual ordering, coverage, and masks are not.

## Render nodes and groups

Artwork and garment pieces instantiate RenderNodes. One semantic piece may create multiple nodes. Coarse groups, back to front:

1. character_back — back hair, rear accessories.
2. body_far — far limbs/body extensions.
3. wearable_far — far sleeves, coat/skirt rear panels.
4. body_core — pelvis and torso core.
5. wearable_core — bodices, trousers pelvis, central garments.
6. body_near — near limbs/hands where appropriate.
7. wearable_near — near sleeves/panels/cuffs.
8. attached_front — held props and front accessories.
9. character_front — front hair, frontmost hand/finger or corrective nodes.
10. diagnostics — authoring only, never export.

Groups are defaults, not a permanent global order.

## Semantic relations

RenderRelation types are before, after, covers, clips_to, and occluded_by. CoverageRule targets SegmentId or BodyRegionId, then resolves to current artwork nodes. MaskRule declares mask ID/version, operation (clip, subtract, intersect, reveal), target, owner coordinate space, transform source, profile/orientation applicability, and fallback.

The render compiler derives edges from group defaults, region orientation/near-far metadata, semantic limb relation, garment coverage/seams, corrective activation, hand/prop interaction, garment state, and constrained manual overrides. Anatomical L/R never implies screen near/far.

## Determinism and invalid state

The compiler validates orientation before rendering, expands semantic targets, adds group and specific edges, detects cycles, and performs a topological sort. Independent nodes use the stable tie key group index → semantic node ID → instance ID. Insertion/property order is never canonical.

An orientation-invalid edit is rejected atomically. A render-cycle edit preserves the last valid render plan, emits RENDER_RELATION_CYCLE with the cycle path, and blocks export/transfer until resolved. On initial load with no valid plan, only non-conflicting nodes plus authoring diagnostics may render; no arbitrary order is serialized.

## Non-destructive coverage and masks

Covered body segments remain articulated and serialized. A skirt may subtract thigh/calf pixels while their state persists and reappears unchanged when removed. Missing masks default to preserving body art and warning unless an explicit alternate mask exists.

Baseline body masks are construction/alpha reference artifacts, not canonical garment/runtime masks. They require explicit import with coordinate ownership and semantics before runtime use.

Cross-joint correctives are independent render nodes aligned to a joint/secondary anchor and ordered relative to both neighboring pieces. They do not replace the joint or its pieces.

## Dynamic proof cases

- Arm and attached sleeve switch behind/in front of torso.
- Cuff covers sleeve/hand seam.
- Trouser pieces articulate at knee with reversible coverage.
- Skirt hides legs without deleting state.
- Coat rear/front panels retain orientation-sensitive order.
- Held prop lies below palm but above declared fingers/hand art.
- Accessory/hair insertion respects local relationships.
- Diagnostics show node IDs, generated edges, masks, coverage, fallback, and cycle path.

## Migration and serialization

Legacy numeric z-index becomes group default and deterministic tie seed only. Existing depthOverrides may migrate to constrained manual before/after relations when an unambiguous target exists; ambiguous values are preserved as legacy metadata with a warning. Canonical serialization stores semantic relations/coverage/manual overrides, never final sort order or generated mask pixels.

Render fallback follows the owning garment/artwork contract. Authoring ghosts remain editor-only; unresolved required visuals block clean export. See [Garment Contract](GARMENT_ATTACHMENT_CONTRACT.md) and [Pose Serialization](POSE_SERIALIZATION_CONTRACT.md).
