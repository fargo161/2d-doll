# Male/Female Shared Profile Matrix

## Status

This matrix is **DESIGNED**. The repository contains one provisional female-labeled engineering baseline and no male profile. It approves neither initial profile's anatomy, silhouette, proportions, nor artwork.

| Concern | Shared canonical grammar | Profile-variable data |
| --- | --- | --- |
| Schema | Contract shapes, compatibility/version rules | Profile ID/version and compatible rig range |
| Skeleton | Required IDs, hierarchy, sides, semantic units | Bind offsets, pivots, limited optional helpers |
| Transforms | Coordinates, propagation, clamp/wrap | Neutral binds and scale reference |
| Orientations | Region vocabulary, matrix, head rules | Supported variants, transitions, visual ranges |
| Proportions | Parameter names and landmark meanings | Lengths, spans, offsets, widths, depths, taper |
| Silhouette | Replaceable artwork/bounds contract | Shoulder, torso, hip, limb, hand, foot contours |
| Limits | Mechanical domains/status categories | Evidence-backed narrower profile/presentation overrides |
| Garments | Slots, attachment, states, seam contracts | Fit landmarks, ease/offsets, correctives |
| Anchors | Semantic IDs, relations, local-space rules | Local transforms and assistance metadata |
| Render/masks | Groups, relations, coverage semantics | Profile/orientation masks, depth defaults, correctives |
| Serialization | Canonical fields and validation | Profile reference/version |

Profiles cannot rename/remove required nodes, change anatomical side meaning, fork pose formats, or require garment code branches.

## Parameter categories

- Stature/scale reference and neutral root.
- Pelvis-to-waist, waist-to-chest, and chest-to-neck lengths.
- Shoulder/hip joint-center spans and offsets.
- Upper arm, forearm, hand, thigh, lower-leg, and foot lengths.
- Silhouette widths/depths independent of joints: shoulder, ribcage, waist, high/full hip, pelvis, limb tapers, palm, and foot.
- Controlled symmetry with optional explicit asymmetry.
- Per-orientation near/far projection, landmark reprojection, transition maps, depth defaults, and correctives.
- Garment fit landmarks: neck, chest, waist, hips, crotch, shoulder/axilla, arm/leg circumferences, inseam, and torso length.
- Profile-specific visually supported ranges and corrective selectors.

No inherited numeric value becomes a default merely because it exists.

## Boundary distinctions

| Layer | Example | Authority |
| --- | --- | --- |
| Mechanical joint | shoulder_L transform origin | Rig/profile mechanics |
| Anatomical landmark | joint center or acromion | Profile anatomy evidence |
| Artwork boundary | upper-arm sprite overlap | Artwork set |
| Garment seam | armhole/sleeve seam | Garment module |
| Mask boundary | bodice coverage of chest pixels | Render/garment mask |

Root/pelvis, anatomical pelvic center, center of mass, waistband, sitting contact, and mask edge are separate concepts.

| Profile | Evidence | Reality |
| --- | --- | --- |
| base_female_v0_1 | Provisional segmented mannequin plus `base_female_v0_1.corpus_v0_1` evidence from 123 flattened source states; all requested corpus measurements remain null/unresolved and no owner/anatomy approval exists | DESIGNED ID; structural and corpus-scale reference only |
| base_male_v0_1 | No repository asset or parameter data | DESIGNED ID; content SPECULATIVE |

Production-candidate acceptance needs annotated neutral views separating pivots, landmarks, overlaps, seams, and masks; a stated stylization target; projection maps; visual-range evaluation; artwork replacement and garment fit proofs; and owner workflow review.

The pose-corpus evidence object's `BODY_HEIGHT = 1.0` and 1,728-pixel raster scale standardize candidate stature and output resolution only. They do not supply canonical segment proportions, bind offsets, or profile anatomy. Those measurements cannot become defaults until reviewed landmark evidence is resolved and approved.
