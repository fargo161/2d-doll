# Mannequin Single-Still Extraction

## Pass

- **Task:** Repeat the mannequin still-extraction workflow for the six newly supplied videos.
- **Objective:** Exhaustively review the supplied footage, select a useful nonredundant set, and deliver 30 transparent single-mannequin donor plates with provenance, QA evidence, and a verified ZIP.
- **Branch:** `main`
- **Starting commit:** `486bcff706ff75f8588cbe8d535c5b86a91694b3`
- **Starting `origin/main`:** `486bcff706ff75f8588cbe8d535c5b86a91694b3`
- **Repository state observed during closure:** `HEAD == origin/main == 14f7cdafabc513e164a95af5d3e8fd4fdf551e13`. The repository advanced independently through a clean, synchronized documentation-only commit while media work was in progress; that change did not overlap this pass.
- **Resulting commit:** none. This pass report and ledger row are intentionally uncommitted pending owner review/authorization.

## Current Reality Before Pass

- **TESTED:** the repository began clean and synchronized at `486bcff706ff75f8588cbe8d535c5b86a91694b3`, with no local ahead/behind delta.
- **TESTED:** the six supplied paths existed and were readable.
- **TESTED:** SHA-256 inventory established six logical files but five unique byte sources: `output (10).mp4` is an exact duplicate of the longer `magichour...mp4` source.
- **IMPLEMENTED:** the prior four-video triple-mannequin corpus existed as a separate external deliverable; no corpus for the new six-file single-mannequin footage existed.
- **DESIGNED:** existing reconciliation guidance keeps flattened extraction plates external to the canonical pose corpus and runtime body space.

## Scope

### In scope

- Inventory all six logical inputs and detect byte duplicates.
- Decode and visually inspect every unique-content frame position.
- Build exhaustive contact sheets and a broad candidate shortlist.
- Select and render 30 useful single-mannequin donor plates.
- Produce proportional 1188×776 straight-alpha RGBA PNGs on `donorPlateCanvas` with adaptive chroma keying, bounded spill cleanup, and transparent padding.
- Inspect every final plate on black, white, and checkerboard backgrounds at full-plate and enlarged detail scale.
- Produce `manifest.csv`, `report.md`, and a verified ZIP outside the repository.
- Add only this evidence report and ledger row to the repository.

### Out of scope

- Canonical pose-corpus or runtime ingestion.
- Canonical front/three-quarter/back approval, support/free-foot semantics, anatomical approval, or rig behavior.
- PXZ modification or validation in the hybrid-rig experiment.
- Hand-painted rotoscoping or invention of anatomy absent from the video frames.
- Committing or pushing this new pass documentation without a separate authorization.

## Changes Made

### External deliverables

Created the collision-safe folder:

`C:\Users\mcdon\Downloads\mannequin_single_still_corpus_20260830_132745`

It contains:

- `png/` with `mannequin_single_001.png` through `mannequin_single_030.png`;
- `manifest.csv` with source hash, exact frame/timestamp, observational metadata, transformations, quality caveats, QA status, and output hash for every PNG; and
- `report.md` with the source inventory, exhaustive-review counts, selection method, QA, limitations, and reality boundary.

Created the verified archive:

`C:\Users\mcdon\Downloads\mannequin_single_still_corpus_transparent_20260830_132745.zip`

ZIP SHA-256:

`B7850116496C62E139D656E9100D64142024CCA4172A3A5C21A34370951BCB16`

### Review and selection

- Inventoried 438 logical frame positions across six files.
- Detected the 97-frame A/B byte duplicate and decoded/reviewed 341 unique-content positions rather than double-counting it as new evidence.
- Visually reviewed all 341 unique positions through 12 exhaustive contact sheets.
- Reduced a 57-frame broad shortlist to 30 outputs: A 7, B 0, C 10, D 6, E 5, and F 2.
- Compared all 435 final pairs with a 48×32 alpha-mask heuristic, then used visual/semantic judgment for the close pairs rather than treating numeric similarity as proof.
- Rejected the first 30-output render after enlarged QA found a motion trail in D48 and lower-leg alpha erosion in F12. D14 and F31 were also replaced conservatively because distal-leg evidence remained ambiguous. The accepted replacements are D16, D24, F20, and F40.

### Extraction and cleanup

- Captured exact real frames at 16 fps presentation positions and verified returned media time against `frame_index / 16`.
- Estimated the green screen separately from each frame's border distribution; no fixed PXZ or external key value was used.
- Keyed at native 560×736 resolution, applied bounded edge color unmix/de-spill, and retained straight-alpha RGBA.
- Scaled proportionally to 590×776 with Lanczos3 and added 299 transparent pixels on each horizontal side. No source-content crop, stretch, rearrangement, or figure separation occurred.
- Applied low-alpha cleanup and small disconnected-component screening while preserving the single source figure.

### Repository files

- Added this report.
- Added the corresponding ledger row in `docs/pass-reports/README.md`.
- Did not add source videos, PNGs, contact sheets, QA sheets, manifests, or ZIP artifacts to Git.

## Combinatorial Impact

The external corpus adds reusable observations spanning neutral-like stances, squat depths, recovery, axial turn/rear-oblique evidence, arm reach, torso arch and fold arcs, stride opening, landing/rebound, toe-off, leg lift, crossed relationships, and subtle weight shifts. These relationships can be compared in later anatomy, segmentation, transition, corrective, and hybrid-rig studies without freezing any one flattened plate into the runtime pose vocabulary.

The donor-only boundary preserves future combinations: orientation and contact labels remain provisional, the source-generated anatomical defects remain visible and documented, and no canonical body-space dimension or rig ontology was changed. The hard-coded 1188×776 size applies only to the external delivery canvas.

## Testing / Evidence

### Source inventory and exhaustive review

- Six logical files / five unique SHA-256 contents.
- A and B: identical 97-frame, 560×736, 16 fps sources; B contributed no new extraction.
- C: 97 frames; D, E, and F: 49 frames each; all 560×736 at constant 16 fps.
- 341/341 unique-content frame positions decoded and visually reviewed; 438 logical positions represented when duplicate B is counted.
- 57-position shortlist recorded; 30 accepted; 311 unique-content positions not selected.

### Iterative correction

- Build 01 passed basic structural checks but failed enlarged visual acceptance for D48 and F12; D14 and F31 were borderline.
- Build 02 substituted D16, D24, F20, and F40.
- Independent visual review confirmed all four replacements resolved the earlier motion/alpha defects.

### Final PNG QA

- 30/30 PNG, RGBA, 1188×776, with real 0–255 alpha.
- 30 unique output SHA-256 hashes matching `build-data.json`, `qa-analysis.json`, and the manifest.
- 30/30 transparent corners and no foreground touching the canvas edge.
- 30/30 with one substantial connected foreground component at alpha ≥16; output 021 also contains one isolated one-pixel alpha=16 component, below the substantial-component threshold.
- Zero files flagged for opaque or semitransparent green-screen contamination by the final analyzer.
- All 435 output pairs included in heuristic redundancy review.
- All 30 accepted plates manually inspected on black, white, and checkerboard at full-plate and enlarged tight-detail scale.
- No accepted plate showed residual green islands, disconnected background debris, key-created torso holes, or canvas clipping.
- A thin cool blue/cyan contour and source motion softness remain on some fine extremities; these limitations are disclosed rather than over-erased.

### ZIP and post-copy verification

- Reopened the staging ZIP and read every member stream.
- Verified exactly 32 entries: 30 PNGs, `manifest.csv`, and `report.md`.
- Verified 30 PNG entries, a 31-line manifest, and zero duplicate, missing, unexpected, unreadable, or hash-mismatched members.
- ZIP size: 2,486,873 bytes.
- Copied the folder and ZIP to Downloads, then compared all 32 destination files with staging hashes: zero missing, unexpected, or mismatched files.
- Reopened the destination ZIP and read all 32 entries.
- Destination ZIP SHA-256 matched staging: `B7850116496C62E139D656E9100D64142024CCA4172A3A5C21A34370951BCB16`.
- Removed the exact task staging directory under the user temp root after destination verification; only the verified Downloads folder/ZIP and repository evidence files remain.

### Repository closure checks

- `git status --short --branch` was clean before this report was added.
- `HEAD` and `origin/main` both resolved to `14f7cdafabc513e164a95af5d3e8fd4fdf551e13` at closure after the independent documentation commit appeared.
- `git diff --check` returned no whitespace errors. Final status contained only the modified ledger and this new untracked report; the index was empty. No repository commit was created by this pass.

## Reality State After Pass

- **SPECULATIVE:** donor-to-rig mapping, approved canonical projection, anatomy landmarks, support/free-foot semantics, corrective requirements, and creative usefulness.
- **DESIGNED:** observational manifest terminology, native-resolution adaptive extraction workflow, 1188×776 donor-only delivery format, and external-artifact boundary.
- **IMPLEMENTED:** 30 external single-mannequin transparent donor plates, manifest, delivery report, verified ZIP, and repository evidence documentation.
- **TESTED:** source hashes/inventory; exhaustive unique-frame review; exact frame/time mapping; PNG dimensions/mode/alpha, hashes, contamination, edges, components, visual composites, redundancy heuristic, ZIP members, and post-copy integrity as described above.
- **VALIDATED:** not achieved. The plates have not yet demonstrated usefulness in the intended PXZ/hybrid-rig creative workflow.

## Known Limitations / Unresolved Questions

- Source resolution and generation constrain fingers, toes, faces, and contact detail.
- Several C frames intentionally preserve source-generated arm/head/neck fusion or extreme anatomical deformation because they add torso-arc evidence; they are not clean anatomy references.
- A86, C62, and D20 retain visible source motion softness.
- Crossed/overlapped legs do not establish true depth order or semantic ground contact.
- F20 and F40 encode subtle weight-shift differences and are close at broad silhouette scale; F40 is the stronger of the pair if a future stricter prune is desired.
- The chroma mattes are structurally and visually tested but are not hand-painted production-final cutouts.
- No canonical/runtime/PXZ integration or creative validation occurred.

## Recommended Next Step

Use the corpus as external donor/reference evidence in the separately scoped hybrid-rig experiment, with projection and contact labels kept provisional. Do not ingest these flattened plates into the canonical pose corpus without a separate anatomy/orientation review.
