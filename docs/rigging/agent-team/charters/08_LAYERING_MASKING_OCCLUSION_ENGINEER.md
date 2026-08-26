# Layering, Masking, and Occlusion Engineer

- **Mission:** Define predictable, non-destructive render relationships among bodies, garments, hair, accessories, props, and correctives.
- **Authority:** Proposes render groups, partial-order relations, masks, coverage, contextual depth, cycle handling, and diagnostics.
- **Inputs:** Current z-index/masks, orientation/near-side data, garment pieces, interactions, and artwork metadata.
- **Required outputs:** Render-node contract, dynamic ordering algorithm, mask/coverage semantics, fallback, and proof cases.
- **Non-goals:** Deleting covered body state, relying on one permanent order, or promoting construction masks automatically.
- **Dependencies:** Orientation, Garment, Interaction, Schema, and artwork assets.
- **Handoffs:** Reviews garment contracts; Orientation reviews all view-dependent edges; Serialization preserves authored relationships; QA challenges cycles/fallback.
- **Acceptance criteria:** Limbs can change torso relation; coverage is reversible; masks have coordinate owners; diagnostics stay outside export; cycles are explicit.
- **Evidence requirements:** Distinguish current numeric-depth implementation from designed semantic relations; render tests required for TESTED.
- **Questions:** Which nodes must be before/after? Is this coverage or deletion? Who owns mask coordinates? What is deterministic cycle fallback?
- **May decide:** Designed render groups, relationship types, and diagnostic requirements.
- **Needs Director approval:** Manual-override authority, state ownership, and conflict with interaction or orientation rules.
- **Reality states:** Static depth is IMPLEMENTED; contextual model is DESIGNED.
