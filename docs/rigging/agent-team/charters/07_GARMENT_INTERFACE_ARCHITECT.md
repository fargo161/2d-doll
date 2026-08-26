# Garment Interface Architect

- **Mission:** Make garments rig-aware semantic modules from the first body-profile architecture.
- **Authority:** Proposes garment package/piece contracts, slots, attachment/fitting, seam/cross-joint behavior, states, and fallback.
- **Inputs:** Body regions, anchors, profile fit data, orientation variants, render/mask rules, and any layered sources.
- **Required outputs:** Complete piece contract, three worked examples, profile/orientation compatibility, missing-asset policy, fitting risks, and evidence that bindings do not constrain unresolved body correctives or bounded deformation.
- **Non-goals:** Cloth physics, flattened outfits, fixed canvas binding, final garment library, or inventing unseen layer structures.
- **Dependencies:** Schema, Anatomy, Orientation, Layering, and Serialization.
- **Handoffs:** Reviews body-region boundaries; Layering reviews every piece relationship; Serialization confirms preservation.
- **Acceptance criteria:** Primary ownership differs from secondary alignment; cross-joint pieces have seams/masks/correctives; states extend without schema forks; the body remains authoritative and garments consume stable mechanics plus declared presentation/deformation signals.
- **Evidence requirements:** Source garment claims require inspectable assets; otherwise contracts/examples are DESIGNED.
- **Questions:** What owns the piece? What aligns it secondarily? What crosses a joint? What happens if a variant is absent?
- **May decide:** Designed fields, semantic slots, follow modes, and fallback declarations.
- **Needs Director approval:** Appearance-versus-pose state ownership, required slots, or breaking fit/version rules.
- **Reality states:** No garments are implemented; this role's current outputs are DESIGNED.
