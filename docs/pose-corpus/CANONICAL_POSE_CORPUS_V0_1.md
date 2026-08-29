# Canonical Female Pose Corpus v0.1

## Status

This document defines the first repository-native pose-corpus boundary for 2D Doll.

- **DESIGNED:** Corpus/source/profile/coordinate/orientation/landmark/export/storage/QA contracts; proposal → override → resolved-entry layering; future-package descriptor shape; and the separation between corpus observations and runtime poses.
- **IMPLEMENTED:** Deterministic ZIP inventory, hash/provenance capture, explicit calibration versus frozen-ingestion operations, calibration-group scale proposals, fixed-canvas similarity rendering, premultiplied-alpha-safe resizing, transactional external artifact storage, per-entry metadata, QA sheets, and corpus registration for 132 source states.
- **TESTED:** Source counts and hashes; synthetic full-corpus calibration; generic selected-package frozen ingestion; pinned-canvas, historical-byte, append-order, render-scope, overflow, transaction-rollback, reference-resolution, and deterministic-repeat guards; authored-override preservation/application/stale-base rejection; schema and cross-record hash/JSON-Pointer validation; deterministic image operations; 132 recorded output hashes with 131 transform-QA passes; Set C replacement-scale regression; and Set D focused external-artifact QA.
- **NOT RESOLVED / NOT ACCEPTED:** Anatomical landmarks and sides, support/free foot, canonical body proportions, reviewed local retarget controls, profile/rear-three-quarter runtime mapping, source-defect repair, runtime adapters, and intended creative-workflow usefulness.
- **VALIDATED:** Nothing in the intended modular-character workflow.

The word `canonical` names the versioned corpus contract and target coordinate language. It does not mean that these source figures have already become one approved character body.

## Boundary from runtime pose state

`2d-doll-pose-corpus-entry-0.1` is an evidence/normalization record. It is not `2d-doll-pose-0.1`, the designed `2d-doll-pose-0.2`, or the experimental semantic-knee proof. Corpus records may preserve observed projections, uncertain pixels, source-art defects, and unresolved landmarks that are not valid reusable runtime articulation.

The corpus descriptor therefore declares:

- `isReusablePose: false`;
- no compatible runtime pose schema versions;
- no runtime integration;
- an adapter is required.

No application code under `app/` was changed by this pass.

## Source sets and immutable provenance

The four source-package ZIP archives remain external and immutable. The tracked source manifest records their filenames, archive-member paths, original dimensions, SHA-256 hashes, source labels/sequences, embedded-manifest records, cleanup history where present, and identified defects. It does not record a local Downloads path.

| Set | Actual supplied archive | SHA-256 | Registered states | Role |
| --- | --- | --- | ---: | --- |
| A | `pose_19_walk_05_front_threequarter_extension_EDGE_EXTREMITY_REFINED.zip` | `98aced237ca341323f8951e47c29481eb9d4f2477d835a10bf0b3d5ee12e230c` | 28 | articulation, gait, extremity and rear-three-quarter evidence |
| B | `comic_pose_assets_55_full_isolation.zip` | `6537c8b8cde03057f49e35958cdc85b8fb4a266fe258733972b55a618e6686b0` | 55 | stance, deep-knee, profile, hair-motion and prop evidence |
| C | `comic_pose_assets_40_edge_refined_green_cleaned.zip` | `d0ba6843d38311002e18fea6d72455722d331fd6960c92b857d0179b6c1a8397` | 40 | higher-resolution frontal/three-quarter scale and silhouette evidence |
| D | `pose_bg_removed_clean_corpus_source_v1.zip` | `718e12022db64f97be4ec52aebc0db7dd6348c81632da8b2d34e79da158e286e` | 9 | front/profile/rear raised-arm, neutral, weight-shift, and wide-stance evidence |

The supplied Set C archive name and structure differ from the archive described in the accompanying task document. The actual archive is authoritative. That document also asserts replacement provenance for Set C poses 39–40, but the supplied archive manifest does not encode supporting provenance; the corpus retains this as an unverified claim. Visual QA did prove that those two rasters form a distinct capture-scale group, which is represented as data rather than a code branch.

Set B pose 45 and poses 51–54 are quarantined as source defects. Pose 46 remains a separate review case. The hash guards in `source-packages.json` prevent those findings from silently attaching to changed source bytes.

Set D uses a preserved, deterministic prepared-RGBA layer derived from the supplied background-removed package. Its package manifest records the untouched source-native members, original archive SHA-256 `10bdad3f4e7260321ea55408145525a41e65dc543024910801b7bc431890af98`, removed floor/contact-matte pixels, subthreshold-alpha cleanup, and partial-alpha RGB decontamination. No generative processing or geometry change was applied.

## Three non-destructive truth layers

1. **Immutable source evidence** — external ZIP bytes plus tracked hashes and archive-member metadata.
2. **Mechanical evidence** — generated proposals, empty authored-override records, and resolved-entry documents with explicit unresolved states.
3. **Derived render evidence** — replaceable external PNG candidates plus tracked operation/output hashes.

The proposal, override, and resolved-entry records are separate files. A future reviewer can add a schema-valid `reviewed` or `approved` landmark/orientation/contact override without changing inference code or erasing the proposal that motivated it. Runs load and apply matching overrides; empty generated scaffolds may rebase automatically, while authored content with a stale proposal hash rejects before rendering. Reserved source-cleanup overrides reject until that operation has an implemented contract. A proposal is never promoted merely because a raster was generated.

## Canonical profile evidence

The target profile identity is `base_female_v0_1`; the corpus evidence object is `base_female_v0_1.corpus_v0_1`. It is `provisional_unapproved`, not a second competing body-profile definition.

The measured raster convention is:

- neutral anatomical stature unit: `BODY_HEIGHT = 1.0`;
- raster scale: 1,728 pixels per body height;
- selection: confidence-weighted median of declared high/medium-resolution Set A and Set C reference groups, rounded upward to 64 pixels;
- Sets B and D omitted from raster-quality selection because upscaling cannot create anatomical detail; their package calibration measures placement against the already frozen body scale.

Every requested profile measurement key exists in the machine-readable evidence object, but its value remains `null` and its stage remains `unresolved`. Flattened clothed silhouettes, perspective, footwear, hair, props, and unknown anatomical sides do not support honest segment-length or width approval. Consequently the corpus may claim tested cross-set stature calibration candidates, but it may not claim canonical head/torso/limb proportion continuity.

## Coordinates, root, and ground

The mechanical coordinate space is `canonical_body_space_v0_1`:

- origin: `pelvis_center`;
- +x: screen right;
- +y: up;
- +z: toward viewer;
- `L` and `R`: character anatomical side, never screen side.

`pelvis_center` is not `rig_root`, `character_root`, center of mass, waistband, sitting contact, or canvas origin. A per-pose ground-plane relation remains separate from the pose origin. Contact candidates are screen-space alpha-envelope observations only; they do not resolve anatomical support foot or force both feet onto the floor.

The derived raster projection uses a fixed horizontal pelvis line and a fixed ground line, while leaving pelvis height above the ground pose-dependent. A crouch therefore remains shorter, a raised foot remains raised, and an overhead or long-stride silhouette is not bounding-box normalized.

## Orientation and landmarks

Observed projection is stored independently from the runtime's canonical orientation graph. Front, front-three-quarter, and rear observations may form direct/provisional references for Front, 3/4, and Back. Profile and rear-three-quarter observations stay `reference_only` with a null canonical orientation; they are not coerced into the three-state runtime grammar.

All 26 landmark IDs are present in every entry. Silhouette-derived head/pelvis approximations are marked `ambiguous`; landmarks not reliably inferable from the flattened image are `unavailable`. Every resolved value is currently null with a reason. Head orientation is independently unresolved.

## Normalization method and measured canvas

The implemented candidate transform is deliberately bounded:

1. Select a declarative capture-scale calibration group.
2. Estimate head-top, pelvis-medial proxy, ground envelope, and source-layer mapping.
3. Apply one isotropic group scale to the normalization input.
4. Place pelvis horizontally and the estimated ground vertically on the frozen canvas.
5. Resize in premultiplied-alpha linear light and clear RGB where alpha is zero.
6. Do not apply a local body-proportion warp without reviewed semantic controls.

The full-corpus measured export contract is:

| Field | Value |
| --- | ---: |
| Canvas | 1,536 × 2,112 RGBA pixels |
| Body height | 1,728 pixels |
| Horizontal origin | x = 768 |
| Ground line | y = 1,984 |
| Minimum transparent safety margin | 87 pixels (5% body height, rounded up) |
| Resampling support reserve | 8 pixels |
| Dimension rounding | 64 pixels |

The 1,536-pixel width is evidence-derived. An earlier candidate width of 1,472 exposed a two-pixel threshold-1 alpha fringe in a Set B hair-swing pose; the root fix added explicit resampling support and remeasured the rounded canvas. Empty transparent source padding is not treated as clipped content.

This method produces scale/canvas/reference candidates. It does not standardize source-performer body proportions. The local-retarget capability is **DESIGNED but not applied** until reviewed landmarks and control topology exist.

## QA and acceptance

Automated evidence across the recorded calibration and frozen-ingestion artifact sets is:

- 28 + 55 + 40 + 9 = 132 registered source states;
- 132 candidate PNGs produced;
- 131/132 passed all transform checks;
- Set D pose 009 fits the physical canvas without clipping but enters the top safety margin by two alpha-threshold-1 pixels and is explicitly review-required;
- 127 review-required candidates;
- 5 source-defect quarantines;
- 0 mechanics-resolved entries;
- 0 accepted renders;
- 16 generated visual-evidence artifacts with sidecar manifests and hashes across the two artifact sets.

Visual evidence includes checkerboard, black, and light contact sheets; root/ground overlays; representative before/after examples; cross-set scale references; stress poses; and a declared-source-issue sheet containing the Set B defects/review case plus the Set C provenance claims. These sheets are inspection evidence, not creative approval.

## Calibration and frozen-ingestion contract

A later package is added by one data descriptor in `spec/source-packages.json`. The descriptor supplies archive identity/hash, pose filename grammar, layer roles, calibration groups, optional embedded manifest, known hash-guarded issues, and unresolved claims. The runtime validates the descriptor schema before reading archives or constructing output paths. Source-set IDs, path keys, entry prefixes, and calibration-group IDs are globally unique; archive identities are basenames within the supplied source directory; calibration reference basenames are resolved within their declaring source set; and pose ordinals are restricted to `001`–`999`. The generic inventory and normalization code has no Set A/B/C/D branch.

Full-corpus calibration is now an explicit operation that may derive a coordinate contract. Frozen ingestion is a separate selected-package operation: it pins both the canonical-v0.1 canvas values and canvas-file hash, measures only the selected package, places it against the existing canvas, renders only new records, and append-merges aggregate records without reconstructing historical array entries. Before and after the coordinated repository/artifact transaction it guards every prior proposal, override, and resolved-entry byte plus the canvas bytes. Duplicate packages reject deterministically. Physical overflow stops before mutation; safe-margin overflow remains a structured candidate review condition rather than enlarging, cropping, or rescaling.

The automated suite proves the calibration path with two synthetic packages loaded together and proves frozen ingestion with fitting, safe-margin, physical-overflow, coordinated-drift, deterministic-repeat, duplicate, and injected post-write-failure fixtures. Package-local metadata references are resolved in tests. The real Set D run additionally proves that a descriptor-only fourth package can advance 123 → 132 while preserving the A–C per-entry byte graph and old aggregate array prefixes.

Run from the repository root:

```text
python -m tools.pose_corpus inventory --source-directory <directory-containing-zips> --write
python -m tools.pose_corpus calibrate --source-directory <all-source-zips> --artifact-root <new-artifact-root>
python -m tools.pose_corpus ingest --source-directory <new-package-directory> --artifact-root <new-artifact-root> --source-set-id <source-set-id>
python tests/verify_frozen_ingestion.py
python tests/verify_pose_corpus.py --artifact-set-root <artifact-set-id>=<artifact-root>
```

Frozen-ingestion artifact roots must not already exist. Large PNGs and QA JPEGs remain outside Git; tracked aggregate records identify their artifact set while package-local manifests use resolvable paths relative to their own root. The external verifier accepts a baseline `--artifact-root` and repeatable `--artifact-set-root ID=PATH` mappings.

## Final acceptance question

Can a fourth transparent pose package enter this system without a new code path and receive the same inventory, hash/provenance, capture-scale, root/ground proposal, frozen canvas, alpha/export, metadata, override, QA, and registration treatment without rewriting A–C? **TESTED yes, synthetically and with the nine-pose Set D package.**

Can it presently receive reviewed anatomical landmarks, an approved canonical female proportion profile, bounded local retargeting, resolved contact semantics, and accepted future garment/head/hair sockets automatically? **No.** Those gates are explicitly unresolved. The reusable ingestion and evidence foundation exists, but the canonical character-normalization foundation is not finished or workflow-validated.

## Smallest high-value next step

Review Set D pose 009's two-pixel top safe-margin condition and author overrides for a deliberately small calibration set: neutral Front and 3/4 references from Sets A and C plus representative profile, wide-stance, overhead, and gait states. Freeze only the landmarks and profile measurements supported by that review; then implement and evaluate one bounded local-retarget prototype before scaling review to all 132 entries.
