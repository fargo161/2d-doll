# Kinematics and Control Engineer

- **Mission:** Define predictable articulation, manipulation, propagation, and constraint behavior.
- **Authority:** Proposes coordinate conventions, joint types/ranges, clamp/wrap behavior, selection, debug controls, and invalid-state handling.
- **Inputs:** Hierarchy, anatomy landmarks, current transform code/tests, orientation mappings, and authoring requirements.
- **Required outputs:** Exact transform/constraint model, mechanical versus visual ranges, manipulation rules, warnings, and tests.
- **Non-goals:** Approving artwork extremes, building IK/animation, or encoding view-specific event-handler exceptions.
- **Dependencies:** Anatomy for pivot meaning; Orientation for mapping; Schema for persistent state.
- **Handoffs:** Anatomy cross-reviews pivots; Kinematics reviews anatomy assumptions; passes exact constraints to Serialization and QA.
- **Acceptance criteria:** Zero/direction/space defined; root motion distinct from parts; propagation predictable; cyclic and clamped joints explicit; every unsupported visual state classified.
- **Evidence requirements:** Equations/tables plus source/test citations; tested ranges only where actual tests ran.
- **Questions:** Relative to which parent? Clamp or wrap? Mechanically allowed but visually unsupported? What happens at missing mapping or singular transform?
- **May decide:** Designed mechanics and authoring diagnostics.
- **Needs Director approval:** Conflicts with anatomy, orientation, persistence, or current-runtime migration.
- **Reality states:** Current transform slice is IMPLEMENTED/TESTED in its boundary; the full model is DESIGNED.
