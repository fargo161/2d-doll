# Interaction Anchor Model

## Status and distinction

The anchor contract is **DESIGNED**. Current root/joint handles and neck_socket are **IMPLEMENTED**, but they are not a complete interaction system.

MechanicalPivot, FitLandmark, AttachmentAnchor, and InteractionAnchor are typed concepts. They may share local transforms or an explicit mapping but are never interchangeable by coordinate coincidence.

## Stable vocabulary

Required initial IDs:

- anchor.root, anchor.head, anchor.face, anchor.look_at, anchor.chest, anchor.waist, anchor.pelvis.
- anchor.shoulder_L/R, anchor.elbow_L/R, anchor.wrist_L/R.
- anchor.hand_L/R, anchor.palm_L/R, anchor.grip_L/R.
- anchor.knee_L/R, anchor.ankle_L/R, anchor.foot_L/R.
- anchor.standing_contact_L/R and anchor.sitting_contact.

Anatomical side is invariant across orientations and reflection.

## Anchor contract

Every anchor declares anchorId, ownerSegmentId, side, semanticType, owner-local position and rotation, supported orientations/profiles, allowed relationship types, optional constraints, optional pose-assistance metadata, explicit fallbackAnchors, availability policy, and version/extensions.

Coordinates are relative to the structured owning segment, never the canvas, screen, camera, or panel. Head/face/look-at/palm/grip/contact anchors require profile/artwork evidence before production approval.

## Relationships

Initial relationship types are align, contact, grip, hold_hand, look_at, support, stand_on, sit_on, and attach_prop.

Each relationship declares relationshipId/type; source instance/anchor; target instance/anchor; local offset/orientation; constraints and tolerance; optional pose assistance; active, suspended, or unresolved resolution state; and fallback policy. Relationships may connect two characters or a character and prop.

Pose assistance may suggest or apply an explicitly accepted joint adjustment; it cannot silently rewrite canonical joints. Missing anchors try only the declared ordered semantic fallback chain. If unresolved, the relationship and authored offsets remain serialized and diagnostics explain the suspension.

## Default mappings

Some interaction anchors may be explicitly derived from mechanical pivots, such as shoulder/elbow/wrist/knee/ankle anchors. This is a declared default mapping and does not turn the pivot into an interaction endpoint. Palm, grip, standing, sitting, face, and look-at require distinct definitions.

## Authoring

Anchor overlays show ID/type, owner segment, local axes, compatible relationship types, constraints, fallback chain, and resolution state. Anchor selection is typed/editor-only. Missing-art ghosts may show anchors in authoring but never enter exported artwork.

The [Serialization Contract](POSE_SERIALIZATION_CONTRACT.md) preserves anchor references, overrides, relationships, and unresolved state. The [Garment Contract](GARMENT_ATTACHMENT_CONTRACT.md) uses AttachmentAnchors rather than interaction endpoints.
