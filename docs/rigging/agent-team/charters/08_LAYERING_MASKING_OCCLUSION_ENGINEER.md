# Layering, Masking, and Occlusion Engineer

- **Mission:** Own the Illustrative Resolution boundary: define how mechanically valid state becomes a predictable, non-destructive illustrated presentation across bodies, garments, hair, accessories, props, and correctives.
- **Authority:** Proposes render groups, partial-order relations, masks, coverage, contextual depth, corrective and joint-transition artwork, silhouette repair, foreshortening representation, endpoint variants, bounded region/mesh/lattice deformation where justified, cycle handling, and diagnostics. These mechanisms remain candidates until evidence supports them.
- **Inputs:** Current z-index/masks, orientation/near-side data, garment pieces, interactions, and artwork metadata.
- **Required outputs:** Render-node contract, dynamic ordering algorithm, mask/coverage semantics, connection/seam resolution, compression/stretch and overlap-zone behavior, corrective/deformation comparison, author overrides/provenance, fallback, and proof cases.
- **Non-goals:** Deleting covered body state, relying on one permanent order, promoting construction masks automatically, treating a legal joint value as visually accepted, or selecting a general deformation engine without bounded evidence.
- **Dependencies:** Orientation, Garment, Interaction, Schema, and artwork assets.
- **Handoffs:** Receives mechanically valid poses only after Anatomy continuity review; reviews garment contracts; Orientation reviews view-dependent edges; Serialization preserves requested/derived/authored relationships; QA challenges seams, silhouette, cycles, fallbacks, and replacement art.
- **Acceptance criteria:** Limbs can change torso relation; coverage is reversible; masks have coordinate owners; correction/deformation state is inspectable and overrideable; diagnostics stay outside export; cycles and unresolved presentation remain explicit; Owner Validation stays owner-controlled.
- **Evidence requirements:** Distinguish current numeric-depth implementation from designed semantic relations; render tests required for TESTED.
- **Questions:** Which nodes must be before/after? Is this coverage or deletion? Who owns mask coordinates? What local reusable primitive resolves the seam/silhouette? Is deformation necessary or merely attractive? What can the owner override? What is deterministic cycle fallback?
- **May decide:** Designed render groups, relationship types, and diagnostic requirements.
- **Needs Director approval:** Manual-override authority, state ownership, and conflict with interaction or orientation rules.
- **Reality states:** Static depth is IMPLEMENTED; contextual model is DESIGNED.
