# Mannequin Still Extraction

## Pass

- **Task:** Authorized mannequin still-extraction asset-evidence pass.
- **Objective:** Review every available frame position in the four supplied videos and deliver a curated external corpus of 30–40 transparent triple-mannequin donor plates with provenance, QA evidence, and a verified ZIP.
- **Branch:** `main`
- **Starting commit:** `1ccd9b8133ab7a016480bce50492dcc14afe8e8b`
- **Starting `origin/main`:** `1ccd9b8133ab7a016480bce50492dcc14afe8e8b`
- **Resulting commit:** none; committing and pushing were not authorized for this pass, so repository `HEAD` remains `1ccd9b8133ab7a016480bce50492dcc14afe8e8b`.

## Current Reality Before Pass

- **TESTED:** `git fetch origin main`, branch inspection, local/remote SHA comparison, ahead/behind inspection, dirty-state inspection, and registered-worktree inspection established that `main` was clean, synchronized, and `0/0` ahead/behind at the expected reconciliation commit.
- **TESTED:** no conflicting task-specific listener, development server, watcher, or second implementation worktree was found before taking the local execution slot.
- **TESTED:** all four supplied videos existed, were readable, and matched the SHA-256 values recorded by the published preparation pass.
- **DESIGNED:** the published reconciliation chain defined these outputs as external `donorPlateCanvas` reference plates rather than canonical runtime poses.
- **IMPLEMENTED:** no extracted donor PNG corpus existed before this pass.

## Scope

### In scope

- Verify the repository safety/synchronization gate and the exact four source files.
- Decode and inspect all 436 available video frame positions.
- Build complete per-video contact sheets and a broad candidate shortlist.
- Select a nonredundant 30–40-image final set based on future articulation/reference value.
- Produce true RGBA triple-mannequin PNGs on a transparent 1188 × 776 `donorPlateCanvas`.
- Apply deterministic chroma matte, de-spill, alpha-safe proportional scaling, padding, and small disconnected-component cleanup without altering pose geometry.
- Generate `manifest.csv`, `report.md`, and a verified ZIP outside the repository.
- Add only this required evidence report and its ledger entry to the repository.

### Out of scope

- Runtime or canonical pose-corpus ingestion.
- Canonical Front / 3/4 / Back mapping.
- Support/free-leg approval, anatomical landmark approval, joint limits, or rig mechanics.
- Garment, head, hair, expression, IK, timeline, or character-art implementation.
- Committing or pushing this documentation change.

## Changes Made

### External deliverables

Created the collision-safe external folder:

`C:\Users\mcdon\Downloads\mannequin_still_corpus_20260830_122053`

It contains:

- `png/` with 30 sequential files, `mannequin_triple_001.png` through `mannequin_triple_030.png`;
- `manifest.csv` with one provenance/QA row per PNG; and
- `report.md` with source inventory, candidate reduction, method, QA, limitations, and the donor-only reality boundary.

Created the verified package:

`C:\Users\mcdon\Downloads\mannequin_still_corpus_transparent_20260830_122053.zip`

ZIP SHA-256:

`07DA5C2524BDA0ACA6593C8743B55C8CF545F92653A9A15EBA2D4A48A473053A`

### Review and selection

- Decoded and reviewed 436/436 positions: A 121, B 97, C 121, and D 97.
- Verified 436 unique exact video-frame media times.
- Built four complete contact sheets.
- Recorded a 54-position broad shortlist: A 16, B 14, C 16, and D 8.
- Reduced the shortlist to 30 plates: A 9, B 8, C 10, and D 3.
- Compared all 435 final output pairs using coarse alpha silhouettes, then manually interpreted the closest pairs by motion phase.
- Replaced a near-duplicate B transition with C frame 92, adding a distinct lower descent between horizontal extension and crossed recovery.

### Extraction and cleanup

- Captured one exact real frame per plate; no timestamps or anatomy were combined.
- Estimated the green key independently from each frame's border samples.
- Generated a data-derived alpha matte, unmixed/de-spilled contaminated edge pixels, and retained straight-alpha RGBA.
- Resized after background removal with premultiplied-alpha-aware Lanczos3 interpolation.
- Preserved A and C at 1.000000×, scaled B proportionally by 1.616667× with transparent padding, and scaled D proportionally by 1.077778×.
- Removed 39 disconnected post-resize components / 1,354 pixels across the final set, using a less-than-500-pixel threshold at alpha >= 4.
- Applied the final residual green-dominance clamp to 913 edge pixels.

### Repository files

- Added this report.
- Added the corresponding ledger row in `docs/pass-reports/README.md`.
- Did not place PNGs, source videos, review sheets, or the ZIP in Git.

## Combinatorial Impact

The corpus adds reusable donor observations for neutral, initiation, apparent weight transfer, forward-foot and cross-step relationships, raised-foot transitions, recovery, high-knee lift and chamber, diagonal/steep/high extensions, horizontal extremes, descent, and crossed recovery. Future anatomy, segmentation, preset, transition, and corrective studies can compare these relationships without treating any flattened plate as a runtime pose.

The donor-only boundary protects the possibility space: observational labels remain provisional, canonical projection and contact semantics remain unresolved, and no runtime vocabulary or schema was frozen around the source clips. The fixed 1188 × 776 size is hard-coded only as a source-preservation delivery canvas; it does not target or restrict `canonical_body_space_v0_1`.

The source videos provide little upper-body variation, so this pass does not imply broad arm-preset coverage. Its strongest new combinations are in torso/pelvis/lower-body relationships.

## Testing / Evidence

### Repository and source gate

- `git status --short --branch` reported clean synchronized `main` before media work.
- `git rev-parse HEAD` and `git rev-parse origin/main` both returned `1ccd9b8133ab7a016480bce50492dcc14afe8e8b`.
- `git fetch origin main` completed successfully.
- Source hashes matched the preparation report:
  - A: `8C5D4727A786316BC6D6B81B7FB315D99D510C6C5976AE9E77570C688E7A55CC`
  - B: `6319A2069D6F861CA899B2F250CD28EB33A0D3470C7311CA902F6DD5FF0AE4AF`
  - C: `FF898C1D71EA3BDBA0A95653F6DBDF98219CEA4057D694C47E73C71D282A4`
  - D: `4B65FA1ACD6C8F0B2229D10BD5FF28470A4B63E9510534929B7DC9BACC168A3A`

### Frame and selection evidence

- Chromium/Playwright decoded every expected frame position using the installed Chrome H.264 decoder; no dependency was installed.
- Frame capture sought `(frame_index + 0.5) / 24` and required the presented-frame callback media time to equal `frame_index / 24` within 0.00001 seconds.
- All four all-frame contact sheets were visually inspected before final selection.
- All 435 final pairings were calculated for redundancy review.

### Iterative failures and corrections

- Build 01 failed structural QA because one output retained nontransparent corner pixels; it was rejected.
- Build 02 passed initial structure checks, but visual QA exposed small detached blur specks, residual semitransparent green after resize, and overly close selections; it was rejected.
- Later candidates added post-resize connected-component cleanup, a final residual green clamp, and stronger redundancy reduction.
- Build 04 is the delivered candidate.

### Final PNG QA

- **30/30 decode:** PNG, 1188 × 776, four channels, real alpha.
- **30/30 transparency:** transparent corners/background and no large opaque green field.
- **30/30 composition:** foreground present in all three mannequin regions; all three figures preserved together.
- **30/30 provenance:** one manifest row and matching output SHA-256.
- **30 unique PNG SHA-256 hashes.**
- **0 semitransparent green-dominant pixels** under the final analyzer's contamination test.
- Visually inspected all 30 plates on black, white, and checkerboard backgrounds at full-plate and enlarged per-figure scale through 18 final QA sheets.
- No baked background, clipped useful extremity, opaque background island, invented hole, or generated anatomy was observed.

### ZIP and delivery verification

- Opened the ZIP with .NET `ZipArchive` and read every member stream.
- Verified 32 file entries: 30 PNGs, `manifest.csv`, and `report.md`.
- Verified zero duplicate names, missing members, unexpected members, or entry-hash mismatches.
- Verified the manifest has 31 nonempty lines: one header plus 30 rows.
- Copied the folder and ZIP to the collision-safe Downloads paths, then re-hashed the complete folder tree: 32/32 destination files matched the staging bytes.
- Destination ZIP SHA-256 matched staging: `07DA5C2524BDA0ACA6593C8743B55C8CF545F92653A9A15EBA2D4A48A473053A`.

## Reality State After Pass

- **SPECULATIVE:** donor-to-runtime mapping, preset vocabulary, approved projection mapping, anatomical landmarks, support/free-leg semantics, joint limits, corrective requirements, and creative usefulness.
- **DESIGNED:** the deterministic extraction workflow, observational manifest terminology, 1188 × 776 donor-only delivery format, and external-artifact boundary.
- **IMPLEMENTED:** 30 external triple-mannequin transparent donor plates, the manifest, delivery report, verified ZIP, and repository evidence documentation.
- **TESTED:** exhaustive 436-position review; exact frame-time checks; PNG structure, transparency, composition, contamination, dimension, hash, visual-composite, redundancy, ZIP-member, and post-copy integrity checks described above.
- **VALIDATED:** not achieved. The donor plates have not yet demonstrated usefulness in the intended modular illustrated rigging workflow.

## Known Limitations / Unresolved Questions

- Fast B and C kicks retain source motion blur and faint extremity trails. These were preserved as source evidence rather than repaired with invented anatomy.
- Source B is only 734 × 480 and is visibly softer after proportional upscale.
- Compression constrains finger, toe, and facial-profile detail.
- Browser duration reporting for B and D was inconsistent; exact verified frame indices/timestamps governed extraction, while the delivery inventory uses the tested MP4 track/container durations from the preparation pass.
- Coarse silhouette distance can rank semantically different phases as close; manual motion-phase review remains necessary for the nearest pairs.
- Canonical orientation, contact mechanics, and useful donor-to-rig mapping remain unresolved by design.

## Recommended Next Step

Have the owner visually review the external corpus and identify the smallest group of high-value donors for a separate anatomy/segmentation study. Do not ingest the flattened plates into the canonical pose corpus or implement rig mechanics without a separately authorized bounded pass.
