# Mannequin Mixed-Layout Donor Still Extraction

## Pass

- **Task:** Repeat the mannequin still-extraction workflow for four newly supplied videos.
- **Objective:** Exhaustively review the footage, select a useful nonredundant set, and deliver 30 transparent donor plates while preserving each source frame's single- or triple-mannequin composition.
- **Branch:** `main`
- **Starting commit:** `14f7cdafabc513e164a95af5d3e8fd4fdf551e13`
- **Starting `origin/main`:** `14f7cdafabc513e164a95af5d3e8fd4fdf551e13`
- **Protected pre-existing worktree state:** `docs/pass-reports/README.md` was already modified and `docs/pass-reports/2026-08-30_1328_mannequin-single-still-extraction.md` was already untracked from the immediately preceding bounded extraction pass. Those changes were preserved; this pass added only its own report plus one ledger row.
- **Resulting commit:** none. This pass report and the accumulated ledger changes remain intentionally uncommitted pending owner review/authorization.

## Current Reality Before Pass

- **TESTED:** local `HEAD` and `origin/main` both resolved to `14f7cdafabc513e164a95af5d3e8fd4fdf551e13`; ahead/behind was 0/0 after fetching `origin/main`.
- **IMPLEMENTED:** the previous extraction pass had produced a separate external single-mannequin donor corpus and had left a coherent two-file documentation change in the repository.
- **TESTED:** all four new source paths existed and were readable.
- **TESTED:** SHA-256 inventory established four logical files and four byte-unique sources.
- **DESIGNED:** the reconciliation boundary keeps flattened source-preservation plates external to the canonical 1536×2112 pose corpus, runtime body space, and PXZ experiment.

## Scope

### In scope

- Inventory all four inputs and verify byte uniqueness.
- Decode and visually inspect every frame position.
- Build exhaustive contact sheets and a formal native-frame shortlist.
- Select 30 motion-diverse donor plates without imposing per-video quotas.
- Preserve the full source composition: three simultaneous mannequins in A/B and one mannequin in C/D.
- Produce proportional 1188×776 straight-alpha RGBA PNGs on `donorPlateCanvas`, using per-frame chroma keying, localized de-spill, layout-aware background cleanup, premultiplied-alpha-safe resize, and transparent padding.
- Inspect every final against its source and on checker, black, and white backgrounds at full-plate and tight-detail scale; inspect A/B figures at additional regional detail scale.
- Produce `manifest.csv`, `report.md`, and a verified ZIP outside the repository.
- Add only this evidence report and its ledger row to the repository.

### Out of scope

- Canonical pose-corpus or runtime ingestion.
- Splitting, rearranging, relabeling, or compositing the three-figure source plates.
- Canonical front/three-quarter/back approval, support/free-foot semantics, anatomical approval, or rig behavior.
- PXZ modification or validation in the hybrid-rig experiment.
- Hand-painted rotoscoping or invention of anatomy absent from the video frames.
- Committing or pushing the new documentation without separate authorization.

## Changes Made

### External deliverables

Created the collision-safe folder:

`C:\Users\mcdon\Downloads\mannequin_donor_still_corpus_20260830_141149`

It contains 32 root files:

- `mannequin_donor_001.png` through `mannequin_donor_030.png`;
- `manifest.csv`, recording source hash, exact frame/media time, source layout, motion phase, selection reason, quality caveat, geometry, key parameters, QA observations, output hash, and donor-only boundary; and
- `report.md`, recording inventory, selection, processing, QA, limitations, and reality state.

Created the verified archive:

`C:\Users\mcdon\Downloads\mannequin_donor_still_corpus_transparent_20260830_141149.zip`

ZIP SHA-256:

`214983416AF912B05CD3866E66F944C593FF6FC266E81F778CF225930830DB20`

### Review and selection

- Inventoried 412 frame positions across four byte-unique sources: A 121, B 97, C 97, and D 97.
- Timestamp-verified, decoded, and visually reviewed all 412 positions through 13 sequential contact sheets.
- Reduced the exhaustive review to a formal 55-frame native-resolution shortlist.
- Selected 30 outputs: A 6, B 3, C 11, and D 10. This distribution follows useful phase landmarks rather than quotas.
- Collapsed A's long terminal fold hold, B's repeated upright endpoints and peak plateau, and adjacent interpolation frames in C/D.
- Preserved A/B as intact three-figure plates and C/D as intact single-figure plates.

### Extraction and cleanup

- Used the decoded media time `frame_index / fps` for provenance: A/B at 24 fps and C/D at 16 fps.
- Estimated the green key independently from each selected frame's 2% border ring.
- Keyed at native resolution, unmixed edge color against the sampled key, applied de-spill only to classified foreground, and retained straight-alpha RGBA.
- Used connected-component cleanup to retain the three expected foreground figures for A/B or the one expected foreground figure for C/D. This removed disconnected green-field residue, including the faint structured right-side ghost in C/D, without deleting the retained figure regions.
- Proportionally fit to 1188×776 without crop or stretch: A became 1187×776 with 0/1 horizontal transparent padding; B remained 1188×776; C/D became 507×776 with 340/341 horizontal transparent padding.
- Used premultiplied-alpha-safe Lanczos3 resize and zeroed RGB beneath alpha zero.

### Repository files

- Added this report.
- Added the corresponding ledger row in `docs/pass-reports/README.md` without altering the preceding uncommitted report.
- Did not add videos, PNGs, contact sheets, QA sheets, manifests, build data, or ZIP artifacts to Git.

## Combinatorial Impact

The external donor set adds whole-plate triple-figure phase comparisons and larger single-figure observations spanning upright arm redistribution, bend onset, asynchronous and synchronized folds, arch departure/peak/recovery, overhead and behind-head relationships, forward hinges, supported and unsupported bends, diagonal and horizontal reaches, crouches, lateral folds, and face-cover recovery.

Preserving the original layouts keeps simultaneous projection and timing relationships available for later comparative study. Keeping the plates external and observational avoids narrowing future combinations: no flattened plate was promoted to canonical body space, no orientation label was coerced, no apparent contact was promoted to support/free-foot truth, and no PXZ architecture was selected. The 1188×776 size is hard-coded only as `donorPlateCanvas`, not as a canonical projection.

## Testing / Evidence

### Source inventory and exhaustive review

- A: `57690607-1034-4c96-af11-ed50a8232466.mp4`, SHA-256 `C17410CACBD5062B4754DBEB17A4FA7BAA8C1D0256A7F30C3E927FEC13717829`, 734×480, 121 frames, 24 fps.
- B: `904426951_0-c4906af5-1d61-4393-8efe-0aa7e3e3f2ba.mp4`, SHA-256 `CA8A0B15D0DC7078EDB7064049CD97BA44DC827ED0CE89E5814C843F3E358E18`, 1188×776, 97 frames, 24 fps.
- C: `output (12).mp4`, SHA-256 `592ABD8C969F01F7F2AEB57B4DF2A83C5225297EE25362836DA94B5C2A171974`, 512×784, 97 frames, 16 fps.
- D: `output (11).mp4`, SHA-256 `8236B8D2E3C448D6296DD5750B8475573D0CC8C07A8436E9F8D49C6BF4017FFB`, 512×784, 97 frames, 16 fps.
- 412/412 frame positions were decoded, timestamp-verified, and visually reviewed.
- 55-position shortlist recorded; 30 accepted; 25 shortlisted candidates rejected; 382 total frame positions unselected.

### Final PNG QA

- 30/30 PNG, RGBA, 1188×776, with real partial-alpha contours and opaque interiors.
- 30 unique output SHA-256 hashes matching the manifest and verified destination files.
- 30/30 with transparent canvas corners and edges; no accepted foreground touches the delivery canvas edge.
- Hidden RGB beneath alpha zero: 0 pixels for every output.
- Foreground green-spill metric (`G - max(R,B) > 8` at alpha ≥16): 0 pixels for every output.
- A/B: 3 substantial connected foreground components and meaningful foreground in all three horizontal plate regions for every output.
- C/D: 1 substantial connected mannequin component for every output; no disconnected right-side ghost/background component survived.
- Six five-output QA matrices compared every accepted plate with its source and showed keyed results on checker, black, and white backgrounds at full-plate and enlarged tight-detail scale.
- Three additional A/B detail sheets inspected all nine triple plates regionally for retained heads, hands, wrists, feet, toes, inter-limb gaps, and halos.
- No accepted plate showed green islands, a retained source ghost, crop/stretch, canvas clipping, or a key-created torso hole.
- The nearest 48×32 alpha-mask pair was D14 versus D21 at normalized distance `0.005187908497`; visual review retained both because diagonal reach and open-chest horizontal sweep are materially distinct relationships.

### ZIP and post-copy verification

- Reopened the staging ZIP with CRC checking and read every member stream.
- Verified exactly 32 root entries: 30 PNGs, `manifest.csv`, and `report.md`.
- Verified a 31-line manifest and zero duplicate, missing, unexpected, unreadable, or byte-mismatched members.
- ZIP size: 3,255,980 bytes.
- Copied the folder and ZIP to Downloads, then byte-compared all 32 destination files against staging: zero differences.
- Verified the destination folder has 32 files and 30 PNGs.
- Confirmed the destination ZIP was byte-identical to staging, reopened it with CRC checking, and byte-compared all 32 member streams with the destination folder.
- Destination ZIP SHA-256 matched staging: `214983416AF912B05CD3866E66F944C593FF6FC266E81F778CF225930830DB20`.
- Removed the exact task staging directory `C:\Users\mcdon\AppData\Local\Temp\codex_motion_extract_20260830_133831` after post-copy verification; it no longer exists.

### Repository closure checks

- `HEAD` and `origin/main` remained equal at `14f7cdafabc513e164a95af5d3e8fd4fdf551e13`.
- `git diff --check` returned no whitespace errors.
- The Git index remained empty.
- Final status contained only the protected modified ledger plus the previous and current untracked extraction reports. No repository commit was created.

## Reality State After Pass

- **SPECULATIVE:** donor-to-rig mapping, approved canonical projection, anatomy landmarks, support/free-foot semantics, corrective requirements, and creative usefulness.
- **DESIGNED:** observational manifest terminology, layout-preserving extraction workflow, `donorPlateCanvas`, and the external-artifact boundary.
- **IMPLEMENTED:** 30 external transparent mixed-layout donor plates, manifest, delivery report, verified ZIP, and this repository evidence documentation.
- **TESTED:** source hashes/inventory; all-frame review; exact frame/time mapping; PNG dimensions/mode/alpha, hashes, contamination, edges, components, visual composites, redundancy heuristic, ZIP members, destination bytes, and cleanup as described above.
- **VALIDATED:** not achieved. The plates have not yet demonstrated usefulness in the intended PXZ/hybrid-rig creative workflow.

## Known Limitations / Unresolved Questions

- A is only 734×480 and contains small figures. Upscaling cannot create finger, toe, face, or contact evidence absent from the source.
- A/B preserve useful simultaneous whole-plate timing/projection evidence but are not detailed anatomical references.
- The selected sources retain self-occlusion, hand/head overlap, hand/knee contact, neck/forearm intersections, and source-generated anatomy defects recorded in the manifest.
- C/D's structured green ghost was correctly treated as background; the mattes are tested cutouts but are not hand-painted production-final rotoscopes.
- Apparent planted feet, weight bearing, and contact remain observations only; support/free-foot roles are unresolved.
- A cool blue/cyan contour remains on some fine extremities because it is part of the source-rendered mannequin/edge mixture; aggressive global color suppression would have damaged the mannequin.
- No canonical/runtime/PXZ integration or creative validation occurred.

## Recommended Next Step

Use the corpus as external comparative donor evidence in a separately scoped anatomy/orientation review before any canonical admission or hybrid-rig mapping decision. Keep whole-plate layout and contact labels provisional.
