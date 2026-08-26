# Canonical Body Rig v0.1

This is the entry point for the repository-native body-rig program. It establishes a specialist team and one shared **DESIGNED** grammar for the initial male and female body profiles. It does not claim that those two profiles, garments, heads, interaction relationships, or the complete contract are implemented.

## Current reality

- **IMPLEMENTED / TESTED:** The canonical Poser slice in [`app/`](../../app/) implements a 15-part articulated engineering rig, three whole-body anchor views, separated pose/character/camera/editor state, visible controls, cross-view semantic elbow mapping, and a minimal pose-save boundary. See [`docs/RIG_ARCHITECTURE.md`](../RIG_ARCHITECTURE.md).
- **IMPLEMENTED / TESTED as inherited evidence:** The byte-preserved baseline contains 45 aligned parts, 45 cropped parts, 45 masks, diagnostic outlines, 17 pivots, and three views. Its viewer has documented failures and is not canonical runtime architecture.
- **DESIGNED:** The shared multi-profile hierarchy, regional orientation rules, garment contract, dynamic render relationships, semantic anchors, full transfer contract, and QA matrix in this directory.
- **NOT IMPLEMENTED:** Initial male profile, approved female profile, heads, garments, regional orientation mixing, the full constraint model, interaction authoring, complete pose loading/migration, and Placer transfer.
- **VALIDATED:** Nothing in the intended creative workflow.

The inherited artwork is provisional engineering material. The baseline manifest calls it a female base, but neither it nor any male artwork is approved as a canonical production profile.

## Navigation

- [Repository and Reference Audit](REPOSITORY_AND_REFERENCE_AUDIT.md)
- [Team Charter](agent-team/TEAM_CHARTER.md), [Roster](agent-team/AGENT_ROSTER.md), and [Orchestration Protocol](agent-team/ORCHESTRATION_PROTOCOL.md)
- [Canonical Body Rig v0.1](architecture/CANONICAL_BODY_RIG_V0_1.md)
- [Male/Female Profile Matrix](architecture/MALE_FEMALE_PROFILE_MATRIX.md)
- [Orientation Compatibility Matrix](architecture/ORIENTATION_COMPATIBILITY_MATRIX.md)
- [Joint and Constraint Model](architecture/JOINT_AND_CONSTRAINT_MODEL.md)
- [Garment Attachment Contract](architecture/GARMENT_ATTACHMENT_CONTRACT.md)
- [Layering, Masking, and Occlusion Model](architecture/LAYER_MASKING_OCCLUSION_MODEL.md)
- [Interaction Anchor Model](architecture/INTERACTION_ANCHOR_MODEL.md)
- [Pose Serialization Contract](architecture/POSE_SERIALIZATION_CONTRACT.md)
- [Rig QA Matrix](testing/RIG_QA_MATRIX.md)
- [Decision Log](DECISION_LOG.md)
- [Next Implementation Pass](NEXT_IMPLEMENTATION_PASS.md)

## Program boundary

These documents define contracts and acceptance behavior. They do not finalize artwork, anatomy, proportions, garments, cloth physics, face systems, Placer, or a production rig. Worked data examples are non-production architecture illustrations.
