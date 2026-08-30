# Female Head / Identity / Pathos Preflight Ingestion

## Pass

- **Task:** Thoroughly ingest the supplied female-head, identity, Pathos, and mannequin evidence and report back.
- **Objective:** Inventory and inspect every supplied file; distinguish the attached design brief from the owner's actual request; reconcile the evidence with repository reality; identify contradictions and blockers; and recommend the smallest safe next pass without implementing the proposed head system.
- **Branch:** `main`
- **Starting commit:** `486bcff706ff75f8588cbe8d535c5b86a91694b3`
- **Starting `origin/main`:** `486bcff706ff75f8588cbe8d535c5b86a91694b3`
- **Resulting commit:** No commit was created or authorized. `HEAD` remained `486bcff706ff75f8588cbe8d535c5b86a91694b3` during the pass.
- **Input-instruction boundary:** `CODEX_PROMPT_2D_DOLL_FEMALE_HEAD_IDENTITY_PATHOS_MODULAR_FOUNDATION.md` was treated as source/design material to evaluate, not as independent authorization to implement, generate derivatives, modify the supplied sources, commit, or push.

## Current Reality Before Pass

- The worktree was clean and synchronized: `main...origin/main`, with local `HEAD == origin/main`.
- The repository's canonical runtime and tested boundaries concern the body rig and pose-corpus infrastructure. [README.md](../../README.md) explicitly lists heads and expressions as not implemented.
- [Expression Maker and Face Intake](../design/expression-maker-face-intake.md) is an authoritative **DESIGNED** artifact. It does not establish an implemented face schema, asset library, editor, runtime, or facial workflow.
- The inherited body rig is intentionally headless and exposes an implemented `neck_socket` attachment marker. It does not expose `HEAD_ORIGIN`, `HEAD_PIVOT`, a scalp cage, ear anchors, face-space registration, or expression slots.
- No supplied female-head, identity, Pathos, or PXZ source was present in the repository before this pass.

## Scope

### In scope

- Hash, integrity, structure, metadata, dimension, alpha, duplicate, and visual inspection of all six supplied files.
- Full member inspection of both ZIP archives and the PXZ container.
- Visual review of all 133 identity PNGs, all 32 Pathos expression images, the Pathos contact sheet, both canonical head references, the PXZ thumbnail, and the reconstructed PXZ layer stack.
- Reconciliation against repository head-presentation, expression-design, attachment, rendering, and serialization contracts.
- Evidence-based status classification and a bounded next-step recommendation.
- This pass report and its ledger entry.

### Out of scope

- Copying source binaries into the repository.
- Editing or round-tripping the PXZ.
- Generating, segmenting, repainting, or calibrating head/face assets.
- Freezing a new schema without resolving contradictions with current authoritative contracts.
- Runtime, editor, serializer, body-rig, or test changes.
- License, consent, likeness-rights, or production-asset approval.
- Commit or push.

## Changes Made

- Added this evidence report.
- Added this report to the chronological pass-report ledger.
- No product source, schema, test, runtime asset, supplied source file, or archive was changed.

## A. Supplied Asset Inventory

All paths below are external evidence under `C:\Users\mcdon\Downloads`; none was copied into the repository.

| Input | Bytes | SHA-256 | Observed role |
| --- | ---: | --- | --- |
| `ERL_Type2_Pathos_Images (1).zip` | 28,910,769 | `1AF6F25E41D3857568B66DC9DCB0F81B8EA5289F45E6936DD24C9CB4A2ED37B4` | Labeled heterogeneous Pathos/performance reference corpus |
| `mannikin.pxz` | 7,500,607 | `8828B89BF586EDA4DE13BFE5683F800B160EBC3F9615351F7CDA17879BC50045` | Pixlr layered raster document containing three mannequin composites |
| `babes/ang.zip` | 245,237,143 | `7DE641A76D4120F4D3894A5A6EF577D83569A25ABBF7999B4B29CA2FAFBE5858` | Thirteen-identity portrait corpus: 117 generated expression images plus 16 references |
| `CODEX_PROMPT_2D_DOLL_FEMALE_HEAD_IDENTITY_PATHOS_MODULAR_FOUNDATION.md` | 40,539 | `12879E47725CBE56380C2037C15E5E25A48CB80D45ACCDD440DE16A12C72102D` | Design brief and claimed corpus interpretation; evaluated against actual evidence |
| `r1vnpvpc5hrmt0d0ad4ajhxtsw_result_0.png` | 4,963,612 | `1B7AEB3AE08404B61B701D785E2B135F586BC56C612238212FB9D89FD37F1EA4` | Two-head chassis concept on black |
| `2pvwtsmsn5rmw0d0ad39ak53k4_result_0.png` | 5,335,093 | `25907DBAA98BB71B830D551274BC7A0EAAB874009F9FFA6A7CB7C102AF2E13EA` | Reframed two-head chassis concept on blue |

### Archive integrity

| Package | Container result | Members | Integrity and safety result |
| --- | --- | ---: | --- |
| Pathos ZIP | Valid PKZIP; 34 root files | 33 PNG + 1 CSV | Every member CRC-verified and decoded; no encryption, archive comment, absolute path, `..` traversal, script, or executable |
| Identity ZIP | Valid PKZIP; 148 entries | 13 directories + 133 PNG + 2 `desktop.ini` | Every member CRC-verified and every PNG decoded; no encryption, archive comment, absolute path, `..` traversal, script, or executable |
| PXZ | Valid PKZIP-based Pixlr document; 39 root files | 1 manifest + 1 thumbnail + 25 content images + 12 masks | Every member CRC-verified; no encryption, traversal, script, executable, or external file link |

No exact byte duplicates or decoded-pixel duplicates exist within or across the two image archives. All 133 identity PNGs and all 33 Pathos PNGs are single-frame images.

## B. Canonical Two-Head Reference Findings

Both supplied chassis references are 4090 x 2143 PNGs at 96 DPI. Although their container pixel format is RGBA, every alpha value is 255; both images are fully opaque.

- The black version uses exact black across approximately 56.67% of the canvas.
- The blue version uses RGB `(20, 0, 196)` across approximately 56.63% of the canvas.
- The foreground placement differs materially between the pair; the blue file is not merely a lossless background-color replacement of the black file.
- The left bust is an upward-looking three-quarter presentation. The right bust is near-profile, but the far eye remains visible; it is not a strict orthographic profile.
- Both heads have directed gaze, parted lips, rendered lashes/brows, strong baked lighting, necks, shoulders, and chest fragments. They are not mechanically neutral isolated head shells.
- The two presentations are fused into one opaque contact-style canvas. Neither file supplies a standalone transparent 3Q head, a standalone transparent profile head, an explicit `HEAD_ORIGIN`, a `HEAD_PIVOT`, a `NECK_ATTACH`, a seam-safe neck overlap, or a measurable scalp-cage contract.
- The images are useful as a **DESIGNED visual chassis direction**: shared bald cranium language, shared neutral blue material, and two intended views. They are not directly attachable runtime assets and do not establish exact dimensions or anchors.

The safest use is to preserve them as immutable visual evidence, then derive separate transparent, calibrated assets only after an attachment coordinate system is defined. The source images themselves should not become the head coordinate system.

## C. Identity Corpus Findings (`ang.zip`)

### Corpus mechanics

- Exactly 13 identity directories are present: `abby`, `Alice`, `ang`, `bij`, `carrie`, `ex`, `heath`, `kath`, `maya`, `popstar`, `suz`, `syd`, and `zor`.
- Exactly 133 unique PNGs are present.
- Exactly 117 files form nine-image generated expression series: nine per identity.
- Sixteen files are extra reference/anchor variants. Fourteen are RGBA cutouts with real transparency; the Alice UUID reference and one Carrie UUID reference are opaque RGB.
- The 117 expression-series images are opaque RGB portraits on baked near-black backgrounds. They are not compositor-ready slot assets.
- Dimension distribution: 92 at 1024 x 1536; 27 at 1086 x 1448; 8 at 1776 x 2342; 4 at 1555 x 2048; 1 at 1531 x 1963; and 1 at 1406 x 2048.
- Modes: 119 RGB and 14 RGBA. All 14 RGBA references contain real 0-255 alpha.
- The archive has no identity or expression manifest. Identity and column semantics must therefore be recorded as observation/inference, not accepted filename truth.
- The generated nine-image series repeats a broadly consistent expression matrix across identities. The inferred columns are approximately: worried/incredulous; disgust/sneer; surprise/jaw drop; concern/pleading; alarm/open-mouth disbelief; lip funnel/pucker/skepticism; stern/pressed-lip displeasure; angry/teeth-bared; and contempt/disgust/upper-lip raise. This mapping is **interpretive**, not source-authored metadata.
- AI/face-swap drift appears in eye shape/color, makeup, crop, head angle, jaw width, neck crop, and asymmetry. Persistent geometry must come from multi-image consensus and landmarks, not from literal pixel transfer from one expressive frame.
- No identity has a true side/profile view. Every profile claim in the attached brief is therefore **DESIGNED reconstruction**, not directly observed evidence.

### Per-identity audit

`D` denotes direct file/pixel observation. Geometry confidence is an interpretive assessment bounded by the generated-source drift.

| Identity | Count and anchor evidence (D) | Scalp / neutral / profile evidence (D) | Geometry confidence | Reconciliation with brief section 13 |
| --- | --- | --- | --- | --- |
| `ang` | 10; nine 1024 x 1536 series images + `head.png` 1555 x 2048 RGBA | Useful relaxed/near-neutral anchor; bald, with clean crown, temples, cheek, and jaw; consistent left-3/4; no profile | Face **HIGH**; frontal cranium **HIGH-MODERATE**; profile **LOW** | Long narrow diamond/oval, high cheeks, long center face, strong taper, and small chin are supported. Nose projection and slender profile are unverified. |
| `zor` | 10; nine 1024 x 1536 + UUID RGBA anchor | Near-neutral with slightly parted lips; bald and clear visible shell; no profile | Face **HIGH**; frontal cranium **HIGH-MODERATE**; profile **LOW** | Fuller midface/mouth and softer taper than `ang` are supported. Profile softness is inferred. |
| `syd` | 10; nine 1024 x 1536 + `syd.png` RGBA | Closed-mouth near-neutral/slightly stern; bald, clear angular cheek-to-jaw line; no profile | Face **HIGH**; frontal cranium **HIGH-MODERATE**; profile **LOW** | Long angular shell, pronounced cheeks, narrow lower jaw, and longer lower face are supported. Acute profile jaw is not observed. |
| `suz` | 9; generated series only; no extra anchor | No genuinely relaxed neutral; closest frames remain pursed/stern; bald but must be consensus-derived; no profile | Face **GOOD**; frontal cranium **MODERATE-GOOD**; profile **LOW** | Heart/diamond field, high cheeks, and strong taper are supported. The brief correctly warns about missing neutral evidence. |
| `maya` | 10; nine 1024 x 1536 + `maya.png` 1531 x 1963 RGBA | Useful relaxed neutral; bald, with relatively clear scalp, ears/temples, and jaw; no profile | Face **HIGH**; frontal cranium **HIGH-MODERATE**; profile **LOW** | Balanced oval/diamond and more substantial jaw/chin than `syd`/`suz` are supported. Projection remains inferred. |
| `heath` | 10; nine 1086 x 1448 + UUID RGBA anchor | Near-neutral with set lips; bald; heavy eye/lip makeup obscures some soft-tissue evidence; no profile | Face **GOOD-HIGH**; frontal cranium **HIGH-MODERATE**; profile **LOW** | Broad/assertive angular face and firm jaw are supported. “Stronger chin” is weaker than the brief suggests. |
| `ex` | 10; nine 1086 x 1448 across three batches + `bri.png` RGBA | Useful relaxed neutral; short swept hair covers crown, hairline, one temple/ear; no bald or profile evidence | Face **HIGH**; cranium **LOW**; profile **LOW** | Long soft diamond, broad cheeks, narrow lower jaw, and pointed chin are supported. The brief correctly separates facial from cranial confidence. |
| `bij` | 10; nine 1086 x 1448 + UUID RGBA anchor | Near-neutral/soft pout; bangs and bob obscure forehead, crown, temples, ears, and lateral jaw; no profile | Face **GOOD**; cranium **LOW**; profile **LOW** | Compact heart/oval, wider midface, short lower face, and small chin are supported. LIMITED skull evidence is accurate. |
| `abby` | 10; nine 1024 x 1536 + `abby.png` RGBA | Useful relaxed neutral; long hair obscures crown, temples, ears, and jaw/neck portions; no profile | Face **GOOD-HIGH**; cranium **LOW-MODERATE**; profile **LOW** | Long heart/oval and narrow lower jaw/chin are supported. The brief's scalp `MODERATE` rating is optimistic; **LOW-MODERATE** is safer. |
| `popstar` | 11; nine 1024 x 1536 + two RGBA references | Two useful near-neutral anchors; one bald/clean-scalp, one tight-hair/headband; heavy makeup; no profile | Face **HIGH**; frontal cranium **HIGH**; profile **LOW** | Long diamond, high cheeks, and strong taper are supported. `VERY HIGH` applies only to frontal/3Q silhouette, not profile/3D certainty. |
| `kath` | 12; nine 1024 x 1536 + three 1555 x 2048 RGBA iterative variants | Three near-neutral anchors share crop/alpha mask; tight hair/head covering and headband hide scalp; no profile | Face **GOOD**; cranium **LOW**; profile **LOW** | Delicate jaw and small chin are supported. “Petite/compact” is weak and may be overstated; visible verticality reads closer to average-to-long. |
| `Alice` | 10; nine 1024 x 1536 + one opaque RGB UUID anchor | Useful neutral; tight hair/head covering and headband obscure crown; face/jaw and one ear clear; no profile | Face **GOOD-HIGH**; cranium **LOW-MODERATE**; profile **LOW** | Narrow oblong/oval, slim cheek-jaw line, long mid/lower face, and small chin are supported. Central projection is unverified. |
| `carrie` | 11; nine 1024 x 1536 + one RGB and one RGBA reference | Two useful near-neutral anchors; bald with especially clear crown, temples, cheeks, and rounded jaw; no profile | Face **VERY HIGH**; frontal cranium **HIGH**; profile **LOW** | Soft compact oval, fuller cheeks, moderate taper, and small rounded chin are strongly supported. `VERY HIGH` must be scoped to frontal/3Q evidence. |

### Corpus-level identity conclusions

- Clean bald/frontal-cranium evidence exists for `ang`, `zor`, `syd`, `suz`, `maya`, `heath`, `popstar`, and `carrie`, but a single 3Q projection still cannot establish cranial depth or back-of-skull geometry.
- Hair materially limits cranium evidence for `ex`, `bij`, `abby`, `kath`, and `Alice`; `abby` and `bij` are the most occluded.
- Every identity except `suz` has at least one useful near-neutral extra. “Near-neutral” is not the same as a calibrated, expressionless, consistently lit neutral.
- `suz` requires consensus fitting from expressive frames or a new neutral reference.
- The archive confirms the 13-identity and 133-PNG claims in the brief, but does not confirm any direct profile claim.
- The previous repository design context described 12 sets and 108 expression images, excluding Alice and the extra references. This archive is new evidence and should not be retroactively described as already repository-integrated.

## D. Pathos Corpus Findings

### Structure and mechanics

- The ZIP contains exactly 32 labeled expression images: `Q001` through `Q008`, with `TL`, `TR`, `LR`, and `LL` members in each group.
- It also contains a 32-row UTF-8 `manifest.csv` and one 1440 x 2640 RGB contact sheet.
- Image dimensions are 14 at 914 x 1024, 14 at 915 x 1024, and 4 at 965 x 1024.
- All 32 expression images are RGBA containers. Twenty-eight are fully opaque. Only the four Q006 images contain useful transparency; each has approximately 17.55%-21.14% fully transparent pixels plus anti-aliased edge alpha.
- The contact sheet is useful for overview but has overlapping/truncated labels in dense rows and must not be treated as a production index.
- No exact byte or decoded-pixel duplicate exists.

### Manifest labels

| Group | TL | TR | LR | LL |
| --- | --- | --- | --- | --- |
| `Q001` | `yuck` | `whoa` | `OO La La` | `yikes` |
| `Q002` | `Tell me more` | `Yeah We know` | `He did NOT` | `I thought you were kidding` |
| `Q003` | `OOookay I guess were doing this` | `But if hes Cuz she doesnt Cuz that means` | `This feels umm different` | `I have to do it now` |
| `Q004` | `His what` | `Ooof` | `Rude` | `Eeek` |
| `Q005` | `Its still not working` | `Thats a LOT more than usual` | `How can you say that to me` | `Do I haaaaave to` |
| `Q006` | `girl whaaaat` | `Me` | `Gross dude` | `You wouldnt` |
| `Q007` | `Bitch please` | `Ew hes short` | `Excuse me` | `This is REALLY bad` |
| `Q008` | `Raaawrr` | `Oh thats sweet of you I should get going` | `I mean maybe if he were nah Unless` | `Whatever you say stud` |

### Visual and semantic assessment

- The corpus is a heterogeneous performance mood-board, not a consistent person, camera, crop, lighting, or production-art set.
- It spans disgust, surprise, incredulity, worry/pleading, frustration, outrage, flirtation, contempt, fear, uncertainty, lip funneling, tooth reveal, jaw opening, eye widening/squint, brow compression/elevation, and asymmetry.
- Several images retain visible stock-photo watermarks, face-swap/compositing artifacts, clipped hair/shoulders, and hard white or black margins.
- Labels mix emotion, spoken intent, social stance, and phonetic/mouth-shape cues. They are not normalized action-unit or facial-parameter labels.
- The source-person identity is not stable and must not be transferred. Camera angle, hair, skin, cosmetics, and lighting are also not transferable expression state.
- The images do provide strong **DESIGNED semantic evidence** for independent brow/eye behavior and a lower-face performance region. They do not provide mechanically registered five-slot assets.
- Direct rectangular extraction from these heterogeneous crops would bake in source identity, hair, skin, lighting, and seams. The appropriate use is to annotate a performance recipe, then resolve that recipe through each identity's own calibrated anchors/artwork/deformation limits.
- Stock-photo/source provenance and likeness rights are unresolved. No Pathos pixel should be approved for shipping, redistribution, or training use solely because it is in the ZIP.

## E. `mannikin.pxz` Findings

### Format correction

`mannikin.pxz` is a modern Pixlr layered raster document, not a Poser scene, figure, or rig. The attached brief correctly associates it with Pixlr, but references `mannikin(2).pxz`; the supplied filename is `mannikin.pxz`. Internally it is a healthy ZIP container. Pixlr also describes PXZ as its document-saving format on the [Pixlr Editor page](https://beta.pixlr.com/editor/).

There is no Poser header, CR2/PZ3/OBJ data, runtime path, figure identifier, mesh, bone, weight, constraint, camera, light, UV, material graph, morph, or 3D scene data.

### Document inventory

- Document UUID: `776c6323-170c-4a7d-b6d7-521200281edb`
- Name: `Untitled(7)`
- Type/unit: `document` / `pixel`
- Canvas: 3749 x 2448
- Background: `#3adf14`
- Layers: 25 flat image layers
- Visibility: 13 visible, 12 hidden
- Masks: 12
- Locked layers: 1, at index 14
- Every layer has opacity 1, rotation 0, and an empty link field.
- Every manifest rectangle exactly matches the intrinsic image dimensions; there are no nontrivial scale transforms.
- The 12 mask filenames end in `.webp`, but their file signatures and decoded payloads are PNG. This is a container naming quirk that a future importer must detect by content.
- All content and masks are embedded and self-contained. No original external source path remains.
- All member timestamps are normalized to 1980-01-01, and no useful authoring chronology, EXIF, software tag, text metadata, or license provenance is recoverable.

### Reconstructed content

The visible stack reconstructs three pale-blue bald female mannequin poses over bright green:

| Figure | Full-canvas non-background bounds | Observed composition |
| --- | --- | --- |
| Left | `(471,442)`-`(936,2006)` | Front/3Q standing figure, arms raised/behind head |
| Middle | `(1564,181)`-`(1950,2030)` | 3Q standing figure, one arm vertical and one near the face |
| Right | `(2237,475)`-`(2922,2000)` | Back/3Q figure assembled from multiple masked pieces, arms gesturing/covering face |

The manifest stack order was independently reconstructed by drawing visible content in index order, multiplying content alpha by mask alpha, and compositing over `#3adf14`. The downscaled reconstruction visually matched the embedded thumbnail with RGB RMSE `4.919/255`, confirming the manifest's practical ordering and mask semantics.

Useful layer evidence includes:

- visible full/near-full body bases and upper/lower-body composites;
- separate raised arms, bent arms, shoulders, torso/bust regions, hips, legs, and a profile head/neck patch;
- hidden alternate arms, body fragments, torso regions, and source pixels;
- two exact content-image pairs reused with different masks/visibility, demonstrating genuinely non-destructive alternate regional use inside the PXZ.

The right figure is the strongest modular precedent in this file: a visible back/torso/neck patch, bust blend, profile head/neck, upturned arm/shoulder, upper torso/bent-arm piece, hips, and masked legs are assembled into one figure. This demonstrates layered raster compositing, not a semantic rig.

### Attachment and editability conclusion

- Recoverable: layer pixels, alpha, mask alpha, position, order, visibility, locked state, three flattened pose crops, and alternate hidden raster fragments.
- Not recoverable: original 3D rig/model, joints, pivots, morph values, source camera, lighting/material setup, original untouched frames, and license provenance.
- A visible profile head/neck layer exists at manifest index 16 with rectangle `(x=2651, y=474, w=240, h=306)`, but this is a baked raster patch. It does not define a reusable `NECK_ATTACH`, head pivot, or socket.
- Green spill, blurry seams, inconsistent source scale/lighting, and anti-aliased alpha are baked into many pieces.
- The environment proved safe read access and semantic stack reconstruction. It did **not** prove a lossless Pixlr-compatible edit/save round trip. Editing the PXZ remains blocked until a copy-based round-trip test verifies manifest preservation, hidden layers, masks, file signatures, and Pixlr reopen behavior.

## F. Repository Reality and Integration Seams

### Current implemented/tested boundary

- [README.md](../../README.md) and [RIG_ARCHITECTURE.md](../RIG_ARCHITECTURE.md) state that heads, expressions, and final artwork are not implemented.
- [Expression Maker and Face Intake](../design/expression-maker-face-intake.md) already **DESIGNS** identity locking, independent left/right eyes and brows, semantic recipes, compatibility/fallbacks, provenance, hair separation, novel recombination, and exact neutral restoration. It also explicitly states that no facial authoring/runtime/schema/assets exist.
- A repository-wide file/content search and `git log --all -S Marcus -- .` found no Marcus code, schema, asset, or historical commit evidence. Marcus can only be treated as an external/historical claim from the attached brief.

### Implemented body attachment seam

The inherited headless 1000 x 1700 body manifest exposes:

- Front `neck_socket`: `(500,150)`
- 3/4 `neck_socket`: `(510,150)`
- Back `neck_socket`: `(500,150)`

The canonical loader exposes the neck socket as a non-articulating attachment marker, and the runtime transforms it through the chest. This is the best existing integration seam.

It is not yet a complete head contract. `HEAD_ORIGIN`, `HEAD_PIVOT`, neck-overlap geometry, canonical scale, scalp cage, ear registration, face-space, and expression-slot calibration remain absent.

Heads must not be inserted naively into the current `view.parts` array. The loader currently treats every part as an articulated joint, while rendering, bounds, and asset loading assume body-part PNGs. A head system needs a separate typed `HeadDefinition`/`HeadBinding` and render-node boundary or an explicit refactor.

### Rendering and persistence gaps

- Semantic render nodes, masks, coverage relationships, and deterministic semantic ordering are **DESIGNED** only. The implemented runtime has numeric body-part depth.
- Current pose state and serialization contain body view, joint values, and depth overrides. They contain no head presentation, identity, material, expression recipe, slot asset, compatibility, or fallback state.
- The designed `CharacterSnapshot` transfer boundary is the appropriate future home for resolved head/expression state, but no implementation exists.

## G. Reconciliation of the Attached Brief

The brief's central separation is sound and aligns strongly with project intent:

> mechanical chassis -> persistent identity -> modular expression -> material -> hair/accessories

The corpus also supports its emphasis on provenance, non-destructive state, asymmetric controls, and cross-expression recombination. Four design conflicts must be resolved before the proposed schema can be called frozen.

### 1. Orientation conflict

The brief freezes identity orientations `3Q | PROFILE`. Current repository contracts freeze runtime head presentations `regular | back`; `regular` serves compatible Front and 3/4 torsos, and no profile runtime family exists. The identity archive contains no true profiles.

Required reconciliation:

- keep `identityOrientation` separate from `runtimeHeadPresentation`;
- allow `3q` to become a candidate calibration for `regular` only after evidence;
- keep `profile` as authoring/reference/reconstructed state with no runtime binding until a versioned contract change and torso compatibility are approved;
- do not silently replace `back`, create a third body orientation, or claim profile attachment.

### 2. Public slot versus internal primitive conflict

The brief freezes five public slots:

`RIGHT_BROW`, `LEFT_BROW`, `RIGHT_EYE`, `LEFT_EYE`, `LOWER_FACE`

with `LOWER_FACE = mouth + nose + cheeks`. Existing face design separates a mouth complex, detail overlays, and bounded lower-face deformation.

Clean reconciliation: preserve `LOWER_FACE` as the public Pathos selection/resolution unit while allowing its internal identity-specific resolver to reference mouth artwork, nose/cheek overlays, and bounded deformation. Exposing those internals must not destroy the five-slot recipe contract.

### 3. Material ownership conflict

The brief requires skin/material to remain swappable and not be permanently baked into identity. Current face design includes neutral texture, makeup, and neutral-lighting assumptions inside its identity base and compatibility profile.

Required refinement: split persistent facial geometry, feature detail, and permanent marks from a separately referenced `MaterialProfile` carrying tint, shading/highlight masks, makeup variants, and rendering assumptions. Hair separation already aligns.

### 4. Side and profile visibility ambiguity

`LEFT` and `RIGHT` must mean anatomical character side, never screen side. This preserves semantics across mirroring/orientation and matches existing anchor rules.

A profile ordinarily hides one eye and brow. Every slot selection therefore needs per-orientation availability/visibility/fallback such as `available`, `occluded`, `unsupported`, or `reconstructed`; a five-slot recipe must not invent two visible profile eyes/brows.

## H. Candidate Machine-Readable Relationship Model

This is a **DESIGNED reconciliation candidate**, not an implemented or owner-approved frozen schema.

| Record | Responsibility | Minimum relationships / fields |
| --- | --- | --- |
| `SourceAssetRecord` | Immutable evidence and rights status | package/path, SHA-256, media mechanics, source label, provenance, rights/consent status, observed/inferred classification |
| `HeadChassisDefinition` | Mechanical truth for one authoring orientation | chassis ID/version, `identityOrientation`, normalized face-space, head origin/pivot, neck overlap, scalp cage, ear regions, slot definitions |
| `HeadAttachmentBinding` | Maps a chassis to an implemented body seam | chassis ID, rig/view ID, runtime presentation, owner segment `chest`, `neck_socket`, scale/rotation/offset, evidence/confidence |
| `HeadIdentity` | One persistent identity across orientations | identity ID, evidence set, persistent geometry parameters, orientation calibrations, material-profile references, confidence by feature |
| `OrientationCalibration` | Identity-specific fit without changing the universal contract | identity ID, chassis ID, local transform, slot anchors/masks, visible contour, evidence quality, `runtimeBinding` nullable |
| `MaterialProfile` | Swappable surface/presentation | tint/base, shading/highlight/detail masks, makeup/marks ownership, lighting/render profile, compatibility |
| `ExpressionSlotDefinition` | Universal five-slot vocabulary | slot ID, anatomical side, normalized anchor/region, z-group, overlap semantics, availability by orientation |
| `ExpressionSlotAsset` | Identity/orientation realization of semantic performance | identity, orientation, slot, semantic parameters, anchor, mask, deformation/overlay internals, source evidence, quality/confidence |
| `PathosPerformanceSource` | Source recipe evidence, not identity art | Pathos ID/label, source quadlist, observed brow/eye/lower-face/gaze/intensity parameters, provenance/rights |
| `ExpressionRecipe` | Editable requested expression state | identity, orientation, five public slot selections or semantic requests, linked/unlinked state, compatibility rules, requested/effective resolution, fallbacks |
| `RenderRelation` | Deterministic composition without flattening source state | node IDs, semantic before/after relation, masks/coverage, hair/accessory zones, canonical restoration order |

Required invariants:

- `identityId` is independent of orientation.
- `identityOrientation` is independent of runtime body presentation.
- slot sides are anatomical.
- `LOWER_FACE` remains one public selection even if internally resolved by several art/deformation primitives.
- requested semantic state is preserved separately from effective/fallback state.
- permanent identity geometry is not owned by expression panels.
- material and hair remain referenceable/swappable.
- source evidence and confidence remain traceable for every derived asset.

## Combinatorial Impact

The corpus can materially expand the possibility space if converted into semantic, identity-preserving primitives:

- the nine controlled states across 13 identities can separate persistent geometry from repeated performance dimensions;
- the heterogeneous Pathos set adds broader brow, eye, gaze, jaw, mouth, cheek, nose-tension, intensity, and asymmetry references;
- independent anatomical left/right brows and eyes enable mixed emotional reads absent from source images;
- a public five-slot recipe can recombine states while identity-specific internals preserve seams and anatomy;
- a universal chassis and attachment binding can let many identities share bodies and future hair/material systems.

The same opportunity would be restricted by premature hard-coding. In particular, do not:

- treat `3q` and `profile` as separate identities;
- bind an unsupported profile directly to the current body runtime;
- force hidden profile-side features to render;
- collapse anatomical left/right controls;
- treat Pathos source pixels as reusable identity assets;
- let `LOWER_FACE` replace persistent jaw/chin identity;
- bake skin, lighting, hair, or background into identity;
- insert a head into the articulated body-part array;
- flatten recipes into the only source of truth;
- promote attractive renders to TESTED or VALIDATED modular assets.

## I. Risks / Blockers

1. **Rights/provenance:** Stock watermarks, face-swap filenames, possible recognizable likenesses, and missing licenses/consent block production use and redistribution approval.
2. **No profile identity evidence:** All 13 profile concepts are reconstructed. The current runtime has no profile head/body contract.
3. **Orientation contract conflict:** `3Q | PROFILE` cannot silently replace repository `regular | back`.
4. **No exact head attachment measurements:** The canonical head images and PXZ do not define a reusable pivot, origin, scale, or seam-safe neck socket.
5. **Opaque/fused source imagery:** Both chassis images and 117 identity expression renders require segmentation and calibration; they are not slot-ready.
6. **Missing neutral for `suz`:** Consensus fitting or a new neutral reference is required.
7. **Generated identity drift:** Any single generated expression may distort stable geometry.
8. **Pathos heterogeneity:** Direct crop reuse would transfer identity, lighting, skin, hair, watermarks, and seams.
9. **Material-design conflict:** Existing identity-base ownership must be refined before “swappable skin” can be claimed.
10. **Five-slot/internal-primitive conflict:** Public recipe semantics and internal art/deformation ownership need an explicit decision.
11. **No Marcus repository evidence:** Architectural ideas may be reused from current design, but no Marcus implementation can be copied or claimed.
12. **PXZ round-trip unproven:** Safe reading/reconstruction is TESTED; lossless editing and Pixlr reopen are not.
13. **Runtime architecture gap:** Head render nodes, serializer fields, masks, ordering, and typed attachments do not exist.
14. **No creative-workflow validation:** Nothing here demonstrates useful authored expressions attached to the current body.

## Testing / Evidence

### Repository and execution gate

- Ran `git status --short --branch`, `git rev-parse HEAD`, `git rev-parse origin/main`, and `git worktree list --porcelain`.
- Observed one clean main worktree and synchronized SHAs.
- A command-line-specific Windows process query through `Get-CimInstance Win32_Process` failed with `Access denied`; this limitation is recorded rather than hidden.
- A fallback process check observed Codex/Chrome/Node processes but no listed Node process owned a visible TCP listening socket. No task-specific dev server, test runner, watcher, browser automation session, or persistent process was launched by this pass.

### Asset evidence

- Calculated SHA-256 for all six supplied top-level files.
- Validated ZIP signatures and CRC-read every member of both ZIPs and the PXZ.
- Rejected unsafe-path, encryption, executable, and embedded-command concerns based on complete member inventories.
- Decoded all 166 archive PNGs and inspected dimensions, modes, alpha extrema, metadata, and normalized pixel hashes.
- Confirmed 133/133 identity PNGs and 32/32 Pathos expression PNGs are byte-unique and pixel-unique.
- Visually inspected per-identity contact sheets, the complete Pathos contact sheet, both chassis references, the PXZ thumbnail, and PXZ layer/contact views.
- Removed all temporary extracted thumbnails/contact sheets created for inspection after visual review.
- Parsed all 32 Pathos manifest rows and all 25 PXZ manifest layer records.
- Independently composited the PXZ visible layer/mask stack and compared it with the embedded thumbnail.
- Inspected relevant repository docs, schemas, runtime/model code, body manifest, tests, and history searches.

### Skipped checks

- `npm test` and browser runtime tests were not run because no product source/runtime behavior changed and this was an evidence-only investigation.
- No PXZ edit/reopen round-trip occurred.
- No landmark calibration, segmentation QA, seam QA, identity-retention test, body attachment test, hair test, material swap, recipe save/load, or novel expression recombination occurred.
- No legal/rights validation occurred.

## Reality State After Pass

- **TESTED:** The supplied package/file inventory, hashes, archive integrity, member counts, image mechanics, duplicate analysis, PXZ manifest/mask stack interpretation, and evidence/repository reconciliation recorded here.
- **DESIGNED:** The attached brief's separable chassis/identity/expression/material/hair architecture; the five public slots; the candidate relationship model; and the proposed reconciliation of orientation, material, side, and lower-face semantics.
- **IMPLEMENTED:** This pass report and ledger entry only, as uncommitted repository documentation. The source PXZ itself implements a layered raster composite, not a 2D Doll semantic rig.
- **NOT IMPLEMENTED:** Female chassis assets, identity records, material profiles, slot assets, Pathos recipes, head attachment bindings, head rendering, head/expression serialization, editor controls, or cross-expression composition.
- **NOT TESTED:** Any generated/calibrated female head, identity retention under expression, profile reconstruction, body attachment, slot seam behavior, material/hair interchange, or recipe persistence.
- **VALIDATED:** Nothing in the intended 2D Doll creative workflow.

## Known Limitations / Unresolved Questions

- Which sources are licensed and consented for preservation, transformation, training, distribution, and shipping?
- Should `profile` become a future runtime head presentation, remain authoring/reference-only, or wait for a full side-body orientation?
- Does 3Q authoring map to the existing semantic `regular` head presentation, and under what body views?
- What exact head origin, pivot, scale, neck overlap, and scalp-cage measurements should be frozen against each `neck_socket`?
- Which facial details are permanent identity marks versus material/makeup/accessory state?
- What is the exact internal resolver for public `LOWER_FACE`?
- How are occluded anatomical-side slots serialized in profile?
- Is a new neutral required for `suz`, and are additional true profiles required for all identities?
- Can a copied PXZ be edited, saved, and reopened in Pixlr without changing hidden layers, masks, mislabeled mask payloads, or stack order?
- Which Pathos labels should be normalized into parameter/action-unit-like semantics, and which should remain human-readable aliases?
- What quality and confidence thresholds permit full-face fallback versus modular decomposition?

## J. Recommended Next Step

The corpus is **ready for a bounded evidence/schema pass**, but it is **not ready for mass generation, profile runtime integration, or production asset import**.

The smallest high-value next pass is:

1. Create an explicit, owner-reviewed design reconciliation record for orientation, material ownership, anatomical side semantics, profile slot visibility, and the public `LOWER_FACE`/internal-primitives relationship.
2. Define an evidence-only `female-head-corpus-v0.1` boundary modeled on the existing pose-corpus separation of immutable source -> proposal -> authored override -> resolved state.
3. Register only package/file/member hashes, image mechanics, provenance/rights status, identity groups, Pathos labels, observed/inferred confidence, and unresolved bindings. Do not generate derivative face art in that pass.

After those decisions are approved, the smallest mechanical experiment should calibrate one **3Q** identity—`carrie` is the strongest primary evidence case, with `zor` as a useful cross-identity check—to the existing `neck_socket` without runtime integration. It should then reconstruct one source expression, create one genuinely novel five-slot cross-Pathos combination, restore neutral exactly, and record identity drift, seams, fallback needs, and requested/effective state. PROFILE should remain out of that experiment.
