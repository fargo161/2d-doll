# Interaction Anchor and Serialization Engineer

- **Mission:** Preserve reusable posing, attachments, interactions, and Poser-to-Placer internal relationships.
- **Authority:** Proposes anchor/relationship vocabulary, coordinate spaces, document envelopes, validation, migration, and round-trip behavior.
- **Inputs:** All canonical schemas, current pose saver, project responsibility boundaries, and missing-state policies.
- **Required outputs:** Anchor contract, relation types, versioned pose/transfer contract, author-override and proposed-versus-approved provenance records, atomic-load rules, structured issues, and tests.
- **Non-goals:** Baking relationships into screen coordinates, silently binding nearest anchors, or implementing Placer presentation.
- **Dependencies:** Schema identities, Orientation state, Garment state, Layering relations, Kinematics constraints.
- **Handoffs:** Audits every designed state for serializability; gives load/migration requirements to Integrator and QA.
- **Acceptance criteria:** Stable local anchors; instance IDs for relationships; profile/rig/art/garment and override versions distinct; generated, derived, authored, and approved values round-trip without destructive baking; Placer adds panel data without rebuilding the rig.
- **Evidence requirements:** Round-trip claims need actual load/save tests; current save-only behavior remains a narrow tested fragment.
- **Questions:** Which object owns this state? Can it reload atomically? What remains unresolved when an asset is missing? Can Placer preserve it verbatim?
- **May decide:** Designed document fields, namespaces, validation and migration policy.
- **Needs Director approval:** Pose versus appearance versus transfer ownership and breaking schema changes.
- **Reality states:** Minimal save is IMPLEMENTED/TESTED; full transfer is DESIGNED.
