# Rigging Documentation Instructions

These instructions apply under `docs/rigging/` and supplement the repository root `AGENTS.md`.

- Treat [architecture/CANONICAL_BODY_RIG_V0_1.md](architecture/CANONICAL_BODY_RIG_V0_1.md) as the canonical **DESIGNED** contract. Current runtime truth remains in source and source-aligned pass reports.
- Use the roles and handoffs in [agent-team/](agent-team/) for rigging passes. If subagents are unavailable, preserve role-separated findings before Director synthesis.
- Keep `front`, `three_quarter`, and `back` as canonical body-orientation IDs. Never introduce a direct `front`/`back` region transition without a later approved bridge design.
- Keep anatomical side suffixes `_L` and `_R`; they never mean screen side.
- Preserve stable segment, joint, anchor, garment-slot, render-group, and schema identities. Record migrations rather than silently renaming them.
- Keep mechanical skeleton truth, body-profile data, artwork, garments, pose state, interaction state, render state, and panel placement separate.
- Record material conflicts in [DECISION_LOG.md](DECISION_LOG.md). Unresolved decisions must remain visible.
- The inherited baseline and its artwork are structural/provisional evidence, not production approval. Trapstar material, if introduced later, is non-production reference only.
- Do not claim a designed contract is implemented, tested, or validated without source and recorded evidence.
- Every rigging pass still requires a new repository pass report and ledger entry under `docs/pass-reports/`.
