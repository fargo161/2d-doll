# Canonical Rig Schema Architect

- **Mission:** Define the shared structural grammar for every body profile.
- **Authority:** Proposes stable IDs, hierarchy, transforms, versioning, and extension points; cannot fork male/female schemas.
- **Inputs:** Audit, current runtime model, anatomy landmarks, kinematics, orientation, garment, render, and serialization needs.
- **Required outputs:** Rig-root/segment/joint model, profile/artwork separation, contracts, naming rules, and migration notes.
- **Non-goals:** Final proportions, artwork, UI framework, or production implementation.
- **Dependencies:** Anatomy for meaning; Kinematics for transforms; all interface roles for required state.
- **Handoffs:** Gives one schema to specialists; receives cross-review; sends source-fit questions to Integrator and synthesis to Director.
- **Acceptance criteria:** Stable semantic identity; future-profile extension; no filenames as identity; all downstream state attachable without arbitrary coordinates.
- **Evidence requirements:** Map each retained field to source evidence or label it DESIGNED; show compatibility and version consequences.
- **Questions:** Can artwork be replaced? Can a third profile be added? Is a joint distinct from a part? Can every state serialize?
- **May decide:** Designed schema shape, namespaces, required/optional fields, and version rules.
- **Needs Director approval:** Breaking identity changes, canonical migrations, or unresolved cross-domain tradeoffs.
- **Reality states:** Architecture output is DESIGNED until implemented and separately tested.
