# Canonical Body Rig v0.1

This is the entry point for the repository-native body-rig program. It establishes a specialist team and one shared **DESIGNED** grammar for the initial male and female body profiles. Task 000 retained that grammar as a strong foundation but amended it with an explicit illustrative-resolution, anatomy-under-pose, author-override, and provenance boundary. It does not claim that those profiles, presentation mechanisms, garments, heads, interactions, or the complete contract are implemented.

## Current reality

- **IMPLEMENTED / TESTED:** The canonical Poser slice in [`app/`](../../app/) implements a 15-part articulated engineering rig, three whole-body anchor views, separated pose/character/camera/editor state, visible controls, cross-view semantic elbow mapping, and a minimal pose-save boundary. See [`docs/RIG_ARCHITECTURE.md`](../RIG_ARCHITECTURE.md).
- **IMPLEMENTED / TESTED as a separate corpus boundary:** [`pose-corpus/canonical-v0_1/`](../../pose-corpus/canonical-v0_1/) registers 132 source-image pose observations, produces 132 fixed-canvas external candidates, and preserves proposal/override/unresolved mechanics plus provenance. It is not reusable runtime pose state and does not approve `base_female_v0_1` proportions.
- **IMPLEMENTED / TESTED as inherited evidence:** The byte-preserved baseline contains 45 aligned parts, 45 cropped parts, 45 masks, diagnostic outlines, 17 pivots, and three views. Its viewer has documented failures and is not canonical runtime architecture.
- **DESIGNED:** The shared multi-profile hierarchy, regional orientation rules, garment contract, dynamic render relationships, semantic anchors, full transfer contract, and QA matrix in this directory.
- **DESIGNED after Task 000:** A hybrid semantic mechanical rig plus localized corrective art, masks, semantic depth, endpoint variants, and optional bounded deformation; all automatic values remain inspectable and non-destructively overrideable.
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
- [Task 000 Foundation Ingestion and Architecture Report](../body-rig-maker/task-000-foundation-ingestion-report.md)
- [Canonical Female Pose Corpus v0.1](../pose-corpus/CANONICAL_POSE_CORPUS_V0_1.md)

## Program boundary

These documents define contracts and acceptance behavior. The `2d-doll-rig-0.2` design is the retained current candidate foundation, not proof that every field or mechanism should be implemented before bounded experiments. These documents do not finalize artwork, anatomy, proportions, correctives, deformation, garments, cloth physics, face systems, Placer, or a production rig. Worked data examples are non-production architecture illustrations.
