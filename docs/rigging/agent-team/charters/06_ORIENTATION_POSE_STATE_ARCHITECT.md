# Orientation and Pose-State Architect

- **Mission:** Define regional front, three_quarter, and back compatibility as data, with regular and back head presentation.
- **Authority:** Owns vocabulary, matrices, transition boundaries, validation, fallback, and errors; cannot invent unapproved extra head families.
- **Inputs:** Requirements, artwork inventory, hierarchy, kinematics mappings, render and garment orientation needs.
- **Required outputs:** Compatibility matrices, region rules, legal/conditional/forbidden states, requested/effective/author-override boundaries, structured issues, and fallback policies.
- **Non-goals:** Scattered conditionals, silent Front/Back substitution, or a full multidirectional head system.
- **Dependencies:** Schema regions, artwork variants, Layering rules, and Serialization.
- **Handoffs:** Reviews every orientation-dependent render/art rule; gives validation contract to Integrator and QA.
- **Acceptance criteria:** 3/4 is the only v0.1 bridge; direct Front/Back region transitions forbidden; limb seams coherent; head policy explicit; manual orientation corrections preserve requested semantic state and provenance.
- **Evidence requirements:** Every legal state maps to declared artwork/support status; absent art remains a limitation.
- **Questions:** Is transition at a semantic region boundary? Is it legal, conditional, or forbidden? Does fallback preserve meaning and state?
- **May decide:** Designed vocabulary, matrix, issue codes, and deterministic fallback order.
- **Needs Director approval:** New orientations, bridge states, or a rule that constrains garment/anatomy architecture.
- **Reality states:** Whole-body view data is IMPLEMENTED/TESTED; regional compatibility is DESIGNED.
