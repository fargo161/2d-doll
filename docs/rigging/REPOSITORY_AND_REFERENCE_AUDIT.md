# Repository and Reference Audit

## Scope and method

This **TESTED as an inventory observation** audit inspected the active `fargo161/2d-doll` checkout at the pass starting SHA recorded in the associated pass report. Files were inspected read-only before architecture authoring. Existence is not approval.

## Artifact classification

| Artifact | Classification | Evidence and limitation |
| --- | --- | --- |
| `app/` canonical Poser slice | Production candidate for mechanical runtime foundations | Explicit state boundaries, recursive transforms, controls, and tests exist. Only elbows have non-transitional semantic cross-view mappings; regional mixing and full contracts do not exist. |
| `docs/RIG_ARCHITECTURE.md` | Current source-aligned architecture | Describes the implemented bounded slice, not the full body-rig program. |
| `docs/RIG_REQUIREMENTS.md` | Designed product requirements | Establishes three views, 3/4 bridge, two head families, state boundaries, and articulation intent. |
| `baselines/canonical_base_body_rig_v0_1/manifest.json` | Structural reference; provisional female-labeled engineering data | Supplies 15 part IDs, 17 pivot IDs, three views, artwork paths, pivots, masks, bounds, and fixed depth. It is not an approved profile or canonical schema. |
| Baseline aligned/cropped PNGs and masks | Placeholder / structural and visual reference | Useful for segmentation, overlap, pivot, mask, and view evidence. They are explicitly non-final and have documented clipping/articulation limits. |
| Baseline outlines and previews | Diagnostic/historical evidence | Useful for inspecting part boundaries and prior articulation. Screenshots are not workflow validation. |
| Baseline browser viewer | Historical, deprecated as canonical runtime | Preserved for provenance; repository-native verification records startup, clipping, mapping, and depth failures. |
| `docs/audits/canonical-base-body-rig-v0.1-functional-audit.md` | Historical evidence | Pre-official-repository audit corroborated later by repository-native tests. |
| Male body assets | Unknown / absent | No male body-profile artwork or parameter set was found. |
| Garment assets/contracts | Unknown / absent | No garment pieces or layered garment sources were found. Baseline documentation only reserves future attachment areas. |
| Pixlr/PXZ/PSD/Krita/ORA files | Unknown / absent | No layered authoring files were present; layer contents cannot be inferred. |
| Archives/reference bundles | Unknown / absent | No ZIP/7z/RAR or equivalent bundle was present. Baseline references README says original videos remain external. |
| Trapstar material | Excluded / absent | No matching file or text was found. If added later it remains non-production structural reference only. |

## Current source facts

- `app/rig-definition.js` adapts the inherited manifest into `2d-doll-rig-0.1`, adds whole-view compatibility, a neck attachment marker, and a depth-override extension boundary.
- `app/model.js` implements affine transforms, a root/part hierarchy, whole-character and camera transforms, bridge view data, semantic elbow flexion, transitional degree values for other joints, resets, and `2d-doll-pose-0.1` serialization.
- The implemented hierarchy has `root → pelvis`, torso and paired arm/leg branches. `neck_socket` exists but head/neck parts do not.
- Implemented view selection is whole-body. It does not implement independent torso, pelvis, limb-region, or head orientation state.
- Implemented depth uses per-view defaults plus stored overrides, but no UI or relationship resolver applies authored override behavior.
- Implemented pose saving excludes character placement, camera, and editor state and has no load/migration path.

## Segmentation lessons

The baseline separates pelvis, mid-torso, chest, upper arms, forearms, hands, thighs, calves, and feet. Each part provides common-canvas and cropped images plus pivot-in-crop data. Masks and hidden overlaps demonstrate that mechanical pivots, visible artwork boundaries, and mask boundaries are related but distinct. The package contains no garment seams, clothing splits, or cross-joint garment evidence.

## Anatomy evidence boundary

Pivot coordinates and proportions are usable as engineering measurements only. The Back view was constructed from rear-three-quarter video references, and the current art was not approved through an anatomy or creative-workflow review. Consequently:

- mechanical joint location is **IMPLEMENTED** in provisional data;
- anatomical landmark interpretation is **DESIGNED** in this program;
- visible artwork, garment seam, and mask boundary remain separate contracts;
- male parameters and approved male/female differences remain **SPECULATIVE** pending source evidence and review.

## Important gaps

No repository evidence establishes approved male anatomy, approved female anatomy, layered garment segmentation, head artwork, profile fitting data, cross-joint garment corrections, interaction relationships, regional orientation artwork, or end-to-end Poser-to-Placer transfer. These gaps constrain the next implementation pass but do not prevent a shared designed grammar.

## Later evidence — Task 000 external package

This section is a chronological addition. It does not rewrite the earlier repository-only observation that no PXZ/Pixlr source was then available locally.

The later owner-supplied `body_rig_maker_task_000_foundation_ingestion_package.zip` contains `bodyref.pxz`, its complete extracted contents, and derived diagnostics.

- **OBSERVED:** The PXZ is a 1799 × 2448 layered dynamic-pose/artistic-nuance reference with 17 image layers, 7 mask references, and zero recorded layer rotations.
- **OBSERVED:** Its visible result is assembled from pre-posed fragments through placement, crop, alpha, masks, overlap, and stack order.
- **OBSERVED:** It demonstrates strong silhouette, body-mass opposition, asymmetry, localized masking, overlap, endpoint direction, and the quality gap between articulation and illustration.
- **NOT CANONICAL:** It is not approved body artwork, clean body segmentation, pivot/range evidence, a working rig, or proof of any future deformation method.
- **ARCHITECTURAL IMPLICATION:** The team must evaluate reusable waist/socket connection zones, correctives, masks, semantic depth, foreshortening, and optional bounded deformation while preserving semantic mechanics and manual tuning.

Trapstar body art remains **REJECTED / NON-CANONICAL** as a production visual base.
