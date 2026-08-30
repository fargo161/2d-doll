# Mannequin Video Still Corpus Run Preparation

> **Reconciled 2026-08-30:** This still-uncommitted preparation brief was corrected by [the mannequin still-corpus reconciliation pass](2026-08-30_1112_mannequin-still-corpus-reconciliation.md). The original extraction-prompt copy remains truncated evidence; the complete reconciliation prompt supplies the explicit owner constraints used to make this run brief self-contained. No frame extraction or asset production occurred during reconciliation.

## 1. Pass

- **Task:** Ingest the supplied mannequin-still prompt and four MP4 files as reference evidence, report their actual contents, and prepare a bounded transparent-still asset pass for later explicit authorization.
- **Objective:** Establish source integrity, video structure, observed pose vocabulary, prompt/source discrepancies, alpha-extraction feasibility, execution boundaries, and a launch sequence without producing the requested 30–40-image corpus.
- **Branch:** `main`
- **Starting commit:** `b153ed81878578f1fc5602ecb0e4941b1ee7cb57`
- **Starting repository state:** Clean and synchronized; `HEAD == origin/main`; only the main worktree was registered; no listener was found on the repository's common development ports 8000, 4173, 5173, or 3000.
- **Resulting commit:** No commit was created. `HEAD` remains `b153ed81878578f1fc5602ecb0e4941b1ee7cb57`.
- **Resulting worktree change:** This pass report and its ledger entry only.

## 2. Current Reality Before Pass

- **IMPLEMENTED / previously TESTED:** The repository has a canonical Poser runtime slice and a separate `pose-corpus/canonical-v0_1/` contract for externally generated candidate rasters. Those status claims come from repository evidence; product tests were not rerun in this preparation pass.
- **IMPLEMENTED / previously TESTED:** Generated pose-corpus rasters already follow an external-artifact boundary rather than being treated as accepted rig mechanics merely because a PNG exists.
- **NOT IMPLEMENTED:** No mannequin-video still corpus, video-frame selection manifest, chroma-key extraction tool, or packaged triple-mannequin transparent asset set exists in the repository.
- **DESIGNED:** The available extraction and reconciliation prompt authority defines a desired 30–40-still extraction, curation, cleanup, manifest, and ZIP workflow. Its text is a design target, not proof that any output has been generated or quality-checked.
- **VALIDATED:** None of the supplied mannequin frames has been demonstrated useful in the intended modular rigging workflow.

## 3. Authority Boundary and Scope

The originally supplied Markdown was a truncated asset-preparation assignment. It was treated as partial reference evidence, not as a replacement for the user's controlling request. A later complete reconciliation prompt supplied explicit QA, reality-state, architectural-boundary, and closure requirements and authorized documentation-only reconciliation. The controlling request remains to prepare the run and perform no extraction until the user says `proceed`.

### In Scope

- Read the supplied truncated extraction Markdown and the later complete reconciliation Markdown as reference material.
- Verify the presence, size, and SHA-256 hash of the Markdown and all four videos.
- Inspect MP4 track structure, codec, dimensions, frame rate, duration, and frame counts without modifying the sources.
- Decode and visually inspect 12 evenly spaced frames from each video, for 48 sampled frames total.
- Measure bounded chroma-background statistics from those 48 frames.
- Identify unique and redundant pose phases, execution risks, output conventions, and launch gates.
- Add the repository-mandated preparation report and ledger entry.

### Out of Scope

- Producing the broad candidate pool or the final 30–40 transparent PNGs.
- Selecting final timestamps, removing backgrounds, refining alpha edges, upscaling, trimming, or changing source pixels.
- Creating the delivery manifest, delivery report, output folder, or ZIP archive.
- Installing FFmpeg, OpenCV, a model, or any other dependency.
- Modifying `app/**`, canonical pose-corpus records, runtime behavior, tests, or existing source documentation outside this evidence ledger.
- Running product tests, launching a development server, committing, or pushing.

## 4. Changes Made

- Added this preparation report.
- Added its chronological ledger entry.
- Created one temporary decode-feasibility frame, 48 temporary review frames, and four temporary contact sheets under the system temporary directory for bounded visual inspection. The exact temporary paths were verified to be inside the system temporary directory and were removed after review.
- Opened and closed a temporary in-app browser tab. Local-file navigation was rejected by browser security policy, so no browser workaround was attempted; inspection continued through the pre-existing local Windows media decoder.
- Made no product, runtime, test, source-video, or production-asset changes.

## 5. Attachment Inventory and Integrity

### Reference prompt

- **File:** `# CODEX PROMPT — MANNEQUIN VIDEO ST.md`
- **Size:** 9,402 bytes
- **SHA-256:** `13D25305A103C7BB3D652722942EF243CB2971B798CA602AF080E50FBD9819A9`
- **Role:** Partial DESIGNED target behavior; the local copy terminates inside its archive-layout fence.

### Reconciliation prompt

- **File:** `CODEX_PROMPT_MANNEQUIN_STILL_CORPUS_RECONCILIATION_PASS.md`
- **Size:** 17,414 bytes
- **SHA-256:** `7C4D517CCEDAD3717B3A9FEC0F339988DAB85AD69ED8E304CF2FD74EE4A52F42`
- **Role:** Complete owner-supplied authority for the documentation-only reconciliation and the missing execution-boundary, QA, reality-state, ZIP-verification, and final-report requirements incorporated below.

### Source videos

All four sources decoded successfully. The video tracks are H.264/AVC (`avc1`) at 24 fps. Container duration is slightly longer than video-track duration because each file also contains an AAC audio track; frame selection should use the video timeline and frame index.

| ID | Supplied file | Bytes | Video geometry | Approx. video bitrate | Video frames / duration | Container duration | SHA-256 |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| A | `904436811_0-1f6139a9-fd84-4635-a520-6bc9d45530ff.mp4` | 1,929,969 | 1188 × 776, 24 fps | 2.950 Mb/s | 121 / 5.042 s | 5.163 s | `8C5D4727A786316BC6D6B81B7FB315D99D510C6C5976AE9E77570C688E7A55CC` |
| B | `2fe9aba5-2da1-402c-8cc1-de424780c2ae.mp4` | 204,337 | 734 × 480, 24 fps | 0.273 Mb/s | 97 / 4.042 s | 4.139 s | `6319A2069D6F861CA899B2F250CD28EB33A0D3470C7311CA902F6DD5FF0AE4AF` |
| C | `904428843_0-95d89964-04a4-4808-bf6e-ae7a7b68601d.mp4` | 1,504,861 | 1188 × 776, 24 fps | 2.267 Mb/s | 121 / 5.042 s | 5.163 s | `FF898C1D71EA3BDBA0A95653F6DBDF98219CEA4052067D694C47E73C71D282A4` |
| D | `video (2).mp4` | 251,991 | 1102 × 720, 24 fps | 0.366 Mb/s | 97 / 4.042 s | 4.139 s | `4B65FA1ACD6C8F0B2229D10BD5FF28470A4B63E9510534929B7DC9BACC168A3A` |

The four video tracks contain 436 frames in total. Source files were read in place and were not copied or modified.

## 6. Prompt-to-Source Reconciliation

The available prompt authority aligns with the repository north star: maximize reusable donor evidence and transition information rather than accumulating attractive but redundant screenshots. The future pass uses these explicit adaptations:

1. **Path mapping:** The prompt names Linux `/mnt/data/...` paths, but the user supplied Windows files under `C:\Users\mcdon\Downloads`. The user-supplied paths are authoritative.
2. **Fourth filename:** The prompt names `video (2)(1).mp4`; the actual supplied file is `video (2).mp4`. The supplied attachment is authoritative and decoded successfully, so this is a reference-text mismatch rather than a missing-input failure.
3. **Prompt authority:** The original extraction copy ends immediately after `report.md` inside an unclosed fenced layout example. The missing original tail remains unavailable and is not reconstructed. The complete reconciliation prompt explicitly supplies the required QA, reality-state, ZIP-verification, and final-report boundaries captured in this revised self-contained brief.
4. **Total count:** Select 30–40 total plates after reviewing all 436 frame positions. **36** is a working target only; there are no per-video quotas, and 30 strong nonredundant plates are preferable to padding the set.
5. **Three-figure invariant:** Every final PNG must retain the complete left, center, and right mannequin arrangement from one real source frame. Single-figure crops and multi-timestamp composites remain prohibited.
6. **Donor-evidence boundary:** Final rasters and the ZIP remain external donor/reference artifacts. They do not become runtime poses, canonical pose-corpus entries, approved body-profile evidence, accepted landmarks/joint limits, runtime artwork, garment/head variants, or validated motion primitives.
7. **Delivery location:** With no location specified in the partial extraction prompt, the prepared default is a collision-safe `mannequin_still_corpus` folder and ZIP beside the supplied files in `C:\Users\mcdon\Downloads`. Writing there will require the normal filesystem approval at execution time.
8. **Commit authority:** Saying `proceed` will authorize the prepared asset pass and its mandatory evidence documentation; it will not by itself authorize a commit or push.

### Reconciled self-contained execution contract

The future asset pass must:

- select 30–40 evidence-driven, nonredundant stills across all videos with no source quota;
- preserve all three source mannequins and every useful extremity in each plate;
- produce true RGBA alpha, not a green/white/black replacement fill;
- preserve one real source frame per output without pose invention, anatomy replacement, generative redraw, secret frame substitution, or multi-timestamp compositing;
- limit cleanup to source-preserving matte, fringe, halo, speck, denoise, mild-sharpening, and compression-artifact work, rejecting an unsalvageable frame instead of repairing anatomy;
- record observed projection with `front_like`, `three_quarter_like`, `rear_like`, `rear_three_quarter_like`, or equivalent provisional language and leave canonical orientation unresolved;
- record only observation-level weight/contact terms such as `apparent_weight_shift_left`, `apparent_weight_shift_right`, `planted_foot_candidate`, `raised_leg`, `crossed_stance`, `high_knee`, `leg_extension`, and `landing_or_recovery_candidate`;
- treat limb/torso/preset labels only as donor or presentation candidates, never as a frozen runtime vocabulary;
- keep mechanics, garments, heads, hair, expressions, orientation mappings, contact mechanics, canonical corpus data, and runtime integration out of scope;
- verify every PNG, manifest row, report claim, and ZIP member before delivery; and
- report candidate/final counts, source provenance, rejects, residual limitations, reality state, output/ZIP integrity, staging/commit/push status, and local-slot release.

## 7. Observed Motion Vocabulary and Selection Implications

Across all four clips, the same three upper-body configurations recur: the left figure has both arms raised/behind the head, the center figure combines one overhead arm with a bent arm near the head, and the rear-like right figure combines a bent arm across/near the head with an outward arm. These figures provide front-like, three-quarter-like, and rear/rear-three-quarter-like observed donor projections; extraction does not resolve canonical Front / 3/4 / Back mapping. The recurring upper-body configurations do **not** create 436 distinct arm states. Most temporal variation comes from the pelvis and legs.

### Video A — subtle weight shift / cross-step vocabulary

- Approximately one gentle standing-motion cycle.
- Adds narrow stance, apparent weight transfer, crossed feet, lifted-heel/raised-foot candidates, mild knee flexion, hip shift, and recovery states.
- Useful for low-amplitude apparent-weight-bearing and planted/raised-foot relationships, but highly redundant at adjacent frames.

### Video B — high side-kick vocabulary

- Approximately one neutral-to-kick-to-neutral cycle.
- Adds initiation, lateral lift, bent-knee transition, high extension, near-vertical extreme, descent, and recovery.
- Contributes the most extreme articulation but is the lowest-resolution and most compressed source, so fingers, toes, and fast limb edges need careful rejection and matte QA.

### Video C — chamber-to-extension vocabulary

- Approximately one neutral-to-chamber-to-extension-to-recovery cycle.
- Adds planted-foot-candidate/high-knee contrast, prolonged chamber states, increasing extension, a readable horizontal kick, crossed recovery, and return to neutral.
- Provides a clear phase progression and may contribute heavily if dense review confirms distinct states.

### Video D — repeated high-knee / bounce vocabulary

- Approximately two high-knee/bounce cycles separated by a near-neutral settle.
- Adds lift, airborne/bent-knee, high chamber, landing, narrow recovery, and repeated-cycle comparison.
- The two cycles are similar; both should contribute only where pelvis, visible-floor-contact candidates, knee height, or recovery relationships differ meaningfully.

### Evidence-driven count rule

The actual run must review all 436 frame positions at contact-sheet scale, build a broader observational shortlist, then compare adjacent candidates before fixing the final count. Select from any video in whatever distribution maximizes distinct articulation evidence. Do not pad a weaker source for balance or omit strong states from a richer source. `36` remains a convenient working target inside the required 30–40 range, not an allocation or success condition. Timestamps alone are insufficient because the two short clips are fragmented MP4s; the manifest should record both zero-based video frame index and seconds.

## 8. Background and Cleanup Feasibility

The sampled frames have a strongly separated green field and pale blue-gray mannequins. A bounded background measurement used `G - max(R, B) > 80` to identify obvious green-screen pixels:

| Video | Median sampled background RGB | Background share across samples | Median 10th-percentile green separation |
| --- | --- | --- | ---: |
| A | approximately `(48, 196, 13)` | 88.7%–90.1% | 147 |
| B | approximately `(58, 225, 19)` | 89.3%–90.0% | 166 |
| C | approximately `(48, 197, 13)` | 89.2%–90.0% | 147 |
| D | approximately `(47, 197, 12)` | 89.2%–90.3% | 148 |

This is favorable evidence for a deterministic local chroma-key matte; it is not a tested alpha result. The future pass must still verify anti-aliased fingers, toes, facial profiles, raised feet, motion blur, compression blocks, green spill, pinholes, and halos on black, white, and checkerboard backgrounds.

All 48 sampled frames visibly retained all three figures and their useful extremities inside the source frame, including the peak kicks. No sampled frame showed a clearly corrupted pose. Dense review may still reveal blur or deformation between the sampled timestamps.

The proposed `donorPlateCanvas` is a 1188 × 776 transparent source-preservation/delivery plate matching the largest videos. Chroma removal should occur at native resolution first; lower-resolution results should then be resized proportionally in premultiplied-alpha space and centered with at most minimal transparent padding. This enables donor-plate comparison without cropping or aspect distortion. The manifest must retain native resolution and scale-factor provenance, especially for Video B.

> The triple-mannequin `donorPlateCanvas` exists only to preserve and compare the source three-figure composition. It does not target, replace, recalibrate, satisfy, or modify `canonical_body_space_v0_1`, the frozen 1536 × 2112 canonical pose-corpus projection, its ground/origin/body-height contract, or runtime-pose interpretation. `reviewCanvas` names QA sheets only.

## 9. Prepared Execution Sequence

Status: **READY FOR MANNEQUIN STILL EXTRACTION when the user says `proceed`; no final still, alpha matte, manifest, or ZIP currently exists.**

1. Re-run Git synchronization, dirty-worktree, worktree, common-server, browser-session, and local-execution-slot checks. Stop on any independent local-pass conflict.
2. Resolve a new collision-safe external staging/output root beside the source files; never overwrite an existing corpus silently.
3. Decode and inventory all 436 video-frame positions. Generate `reviewCanvas` contact sheets and an observational shortlist larger than the final set.
4. Curate 30–40 plates by distinct observed articulation, not even time spacing or per-video quotas. Reject near-duplicates, blur, compression damage, and any frame that clips useful anatomy.
5. Extract each selected native frame deterministically and record source file, zero-based frame index, exact video timestamp, source SHA-256, observed-projection candidates, and observation-level motion/contact notes.
6. Build a soft chroma matte from the measured per-frame green field; de-spill/refine edges without redrawing or inventing anatomy. Reject and replace any unsalvageable frame.
7. Place each keyed frame on the 1188 × 776 RGBA `donorPlateCanvas` using proportional premultiplied-alpha resizing and transparent padding. Preserve all three figures and the original three-figure composition; do not map the plate into canonical body space.
8. Run structural QA: RGBA mode, real alpha, transparent borders/corners, no opaque green field, three occupied figure regions, no clipped extremities, filename continuity, and manifest/file agreement.
9. Run visual QA on checkerboard, black, and white contact sheets at both overview and edge-detail scales; record rejects and residual limitations.
10. Produce `png/mannequin_triple_001.png` through the evidence-driven final number, `manifest.csv`, `report.md`, and a ZIP containing the complete folder. Include output SHA-256 values plus source/native/`donorPlateCanvas` provenance in the manifest.
11. Reopen the ZIP and verify CRC/readability, exact member list, PNG count, RGBA/true-alpha properties, filename continuity, manifest-to-file agreement, and recorded hashes; reject delivery if any check fails.
12. Add a separate implementation/evidence pass report and ledger row. The final response must report source/candidate/final/reject counts, output and ZIP locations/hashes, QA evidence, residual limitations, reality states, staging/commit/push status, and local-slot release. Update broader current-reality documentation only if source reality actually changes.
13. Stop all task-specific processes, remove review-only temporary material after verifying exact paths, report any intentionally retained process, and release the local execution slot.

The planned delivery layout is:

```text
mannequin_still_corpus/
  png/
    mannequin_triple_001.png
    ...
  manifest.csv
  report.md
mannequin_still_corpus.zip
```

## 10. Combinatorial Impact

This preparation pass adds no new product capability. The prepared donor corpus could later expand combinatorial design by preserving apparent weight/contact relationships, chamber and extension phases, weight shifts, and the same moment through three simultaneous observed projections. Frame-level provenance would let future rigging work investigate limb or torso presentation candidates without treating a flattened triple image as canonical mechanics.

The main restrictions to avoid are inflating the corpus with duplicate arm configurations, mistaking whole-frame PNGs for modular rig parts, treating donor-plate coordinates as approved anatomy, resolving orientation/contact roles through naming, freezing example preset labels as runtime schema, or polishing away real source articulation. `36` is useful only as a working review target; the accepted range remains 30–40 distinct donor plates.

## 11. Testing / Evidence

### Repository gate

```text
branch: main
HEAD: b153ed81878578f1fc5602ecb0e4941b1ee7cb57
origin/main: b153ed81878578f1fc5602ecb0e4941b1ee7cb57
worktrees: main only
starting worktree: clean
common development listeners checked: none found
```

### Attachment and media evidence

- Read the truncated extraction Markdown and complete reconciliation Markdown through their actual ends and calculated both SHA-256 values.
- Calculated SHA-256 values for all four MP4 files.
- Parsed ordinary and fragmented MP4 track/sample structures to establish codec and exact video-frame counts.
- Queried Windows media properties for dimensions, frame rate, bitrate, and container duration.
- Successfully decoded all four files with the existing local Windows media stack; no dependency was installed.
- Extracted and visually inspected 12 evenly spaced frames per video, for 48 sampled frames total.
- Calculated bounded chroma-background statistics from those 48 samples.
- Confirmed the temporary browser tab was closed and temporary review rasters were removed.
- Did not prototype or claim alpha-edge quality.
- Did not run repository tests or builds because no product behavior changed.

## 12. Reality State After Pass

- **SPECULATIVE:** Exact final frame list/distribution/count within 30–40, matte thresholds, residual edge quality, donor-to-runtime mapping, preset vocabulary, orientation/contact semantics, and usefulness in the intended creative workflow.
- **DESIGNED:** The reconciled authority/path boundary, quota-free evidence-driven count rule, external donor-evidence boundary, `donorPlateCanvas`, observational provenance fields, QA/ZIP gates, and prepared execution sequence.
- **IMPLEMENTED:** Only this pass report and ledger entry. No mannequin corpus or extraction pipeline exists in the repository.
- **TESTED:** Attachment presence and hashes; video codec, dimensions, rate, frame counts, and durations; local decode feasibility; 48-frame bounded visual coverage; and sampled green-field separation.
- **VALIDATED:** Nothing about final asset quality, anatomical usefulness, modular state harvesting, or rig integration.

## 13. Known Limitations / Unresolved Questions

- The videos repeat the same three upper-body presets, so final diversity will be lower-body dominated.
- Video B is only 734 × 480 and carries the greatest interpolation/compression risk; Video D is also lower bitrate than Videos A and C.
- The final per-video distribution is intentionally unresolved until all 436 frames are compared; repeated high-knee phases in Video D may contribute few plates if redundant.
- Only 48 spaced frames were visually inspected in preparation; the execution pass must inspect all 436 frame positions.
- No final chroma key, de-spill, edge matte, or black/white/checkerboard validation has occurred.
- FFmpeg is not installed. The existing Windows decoder succeeded for preflight, but the execution pass must verify selected-frame indexing before batch output and stop before installing anything if a new dependency becomes necessary.
- Writing final deliverables beside the inputs is outside the repository write root and will require normal filesystem approval when execution begins.
- The complete original extraction-prompt tail remains unavailable. The complete reconciliation prompt makes this revised brief self-contained but does not prove recovery of the missing original wording.
- The external whole-frame donor plates must not be labeled accepted rig mechanics, canonical orientation/contact evidence, or a validated pose vocabulary.
- This report and ledger entry are intentionally uncommitted. They form the related dependency chain for the later authorized run and must be reconciled before unrelated work begins.

## 14. Recommended Next Step

When ready, say `proceed`. Re-run the repository/local-slot gate, then review all 436 source frame positions and build the curated transparent corpus through the recorded alpha and visual-QA gates.

No task-specific server, watcher, browser tab, test process, or media process remains running. The local execution slot is released.
