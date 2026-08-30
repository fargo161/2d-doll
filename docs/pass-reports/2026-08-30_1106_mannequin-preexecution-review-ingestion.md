# Mannequin Pre-execution Review Ingestion

## 1. Pass

- **Task:** Ingest the supplied screenshot as review evidence, verify its six corrections against repository source and the mannequin preparation record, and report the resulting execution gates without applying the proposed corrections or starting extraction.
- **Objective:** Separate verified repository truth from screenshot-authored recommendations, identify which earlier preparation claims are superseded, and establish whether the mannequin still pass remains ready to run.
- **Branch:** `main`
- **Starting commit:** `b153ed81878578f1fc5602ecb0e4941b1ee7cb57`
- **Starting repository state:** `HEAD == origin/main`; only the main worktree was registered. The worktree already contained the related uncommitted mannequin preparation report and its ledger row. This review is a continuation of that dependency chain, not an unrelated pass.
- **Resulting commit:** No commit was created. `HEAD` remains `b153ed81878578f1fc5602ecb0e4941b1ee7cb57`.
- **Resulting worktree change:** This correction report and its ledger entry, in addition to the prior related preparation report/ledger change.

## 2. Current Reality Before Pass

- **IMPLEMENTED / TESTED:** The canonical pose-corpus boundary registers 132 source states and has a frozen 1,536 × 2,112 raster projection contract with a 1,728-pixel body-height scale.
- **IMPLEMENTED but stale documentation exists:** The main README and canonical pose-corpus documentation report 132 states, while `docs/rigging/README.md` still reports 123.
- **DESIGNED:** The earlier mannequin preparation report proposed a 30–40-output extraction workflow, a 36-image target with exact per-video allocations, a 1,188 × 776 output plate, and pose-language shorthand.
- **NOT IMPLEMENTED:** No final mannequin candidate pool, transparent still corpus, manifest, delivery report, or ZIP exists.
- **VALIDATED:** No supplied mannequin state or proposed semantic label has been accepted in the intended rigging workflow.

## 3. Authority Boundary and Scope

The screenshot is user-supplied review material. Its prose was treated as evidence and recommendations to verify, not as authorization to edit the named documents, rewrite the prior report, or begin the extraction workflow. The controlling user request was only to **ingest and report**.

### In Scope

- Inspect and hash the screenshot.
- Verify each of its six claims against current repository text, machine-readable corpus contracts, the previously supplied prompt file, and the uncommitted mannequin preparation report.
- Record corrections and revised readiness in a new chronological report rather than silently rewriting earlier evidence.
- Add the repository-mandated ledger entry.

### Out of Scope

- Editing `docs/rigging/README.md` from 123 to 132.
- Rewriting the earlier preparation report.
- Inventing the missing tail of the prompt from the screenshot's summary.
- Selecting frames, extracting PNGs, removing backgrounds, building manifests, or creating the ZIP.
- Running product tests, committing, or pushing.

## 4. Review Attachment and Prompt Evidence

### Screenshot

- **File:** `codex-clipboard-8f5c6359-75e7-41c3-97f7-f115ca86fe2a.png`
- **Size:** 149,505 bytes
- **Dimensions / mode:** 840 × 895, RGBA PNG
- **SHA-256:** `507245ED9A7A86D5A09AD0AB1E9375545D137024339111CD0D505A34FD915A7D`
- **Role:** Review evidence containing six proposed pre-execution corrections.

### Previously supplied prompt copy

The local Markdown file still ends immediately after `report.md` inside an unclosed fenced layout example. It contains no QA, reality-discipline, or final-response sections after that point. The screenshot states that a complete authored version contains additional material, but it does not supply that material. Missing instructions cannot be reconstructed or treated as authorized merely from their description.

## 5. Verified Findings

### 1. Stale 123-state claim — CONFIRMED, independent defect

- `README.md` reports 132 registered external source states.
- `docs/pose-corpus/CANONICAL_POSE_CORPUS_V0_1.md` reports 132 registered states and explains the Set D advance from 123 to 132.
- `pose-corpus/canonical-v0_1/README.md` reports 132 registered source states.
- `docs/rigging/README.md` line 8 still reports 123 observations and 123 candidates.

This is a real pre-existing documentation contradiction left from before Set D. It was not caused by the mannequin work and should be corrected in a separately authorized documentation repair rather than silently folded into this review-only pass.

### 2. Front / 3/4 / Back wording — CONFIRMED

The earlier preparation report describes the three mannequins as providing simultaneous front, three-quarter, and back references. That is more definite than current evidence allows.

The corpus contract explicitly separates observed projection from the runtime orientation graph:

- front may be a direct Front reference;
- front-three-quarter and rear may be provisional references for 3/4 and Back;
- profile and rear-three-quarter remain `reference_only` with null canonical orientation;
- head orientation is independently unresolved.

Future mannequin records should therefore use wording such as **front-ish, three-quarter-ish, and rear/rear-three-quarter observed projections; canonical orientation unresolved**. The triple arrangement must not settle a runtime orientation mapping.

### 3. Support/free-leg semantics — CONFIRMED

The earlier report repeatedly uses `support leg`, `free leg`, `support foot`, and `planted support` as if anatomical roles were established. The canonical corpus contract explicitly lists support/free foot as unresolved and says contact candidates are screen-space alpha-envelope observations, not resolved anatomical support.

The extraction manifest should use observation-level descriptors such as:

- `apparent_weight_bearing`;
- `planted_foot_candidate`;
- `raised_leg`;
- `crossed_stance`;
- `visible_floor_contact_candidate`.

These names are a **DESIGNED donor-manifest vocabulary**, not existing canonical pose-corpus semantics. Later anatomical review may promote or replace them.

### 4. The 1,188 × 776 plate needs a non-canonical namespace — CONFIRMED WITH NUANCE

The canonical pose-corpus export contract is already frozen for v0.1 evidence at:

- 1,536 × 2,112 RGBA pixels;
- `BODY_HEIGHT = 1.0` in body space;
- 1,728 raster pixels per body height;
- horizontal origin x = 768;
- ground line y = 1,984.

The proposed 1,188 × 776 triple-mannequin output is not mechanically incompatible because it is an external source plate, but calling it merely a standardized or canonical-looking canvas creates avoidable ambiguity. The future manifest should call it `donorPlateCanvas` (with `reviewCanvas` reserved for QA sheets) and state:

> The 1,188 × 776 triple-mannequin donor plate is a source-preservation and delivery format only. It does not target, alter, satisfy, or modify `canonical_body_space_v0_1` or the canonical pose-corpus v0.1 canvas.

The screenshot's phrase “BODY_HEIGHT 1728” is directionally correct but imprecise: `BODY_HEIGHT` is 1.0; 1,728 is the raster scale in pixels per body height.

### 5. Exact 8/10/11/7 allocation — CONFIRMED AS PREMATURE

The earlier report labels the allocation provisional and requires all 436 frames to be reviewed, but exact per-video quotas still create an unnecessary anchor after only 48 sampled frames.

The corrected boundary is:

- retain **36** only as a working target inside the requested 30–40 range;
- apply no per-video quota;
- inspect all 436 frame positions;
- let distinct observed articulation determine the final distribution;
- finish anywhere from 30 to 40 rather than preserve 36 by admitting redundant states.

### 6. Truncated prompt — CONFIRMED AND MATERIAL

The local file is objectively truncated at the unfinished archive-layout fence. The screenshot says the missing original contains additional QA, reality-discipline, and final-response instructions. The earlier preparation pass reconstructed several reasonable safeguards, but reconstruction is not a substitute for the actual user-authored text.

This changes status from **ready when told to proceed** to **not ready for extraction until the complete prompt is supplied and reconciled**. No future agent should rely solely on the earlier preparation report to infer the missing tail.

## 6. Changes Made

- Added this review-ingestion report.
- Added its chronological ledger entry.
- Made no correction to `docs/rigging/README.md`.
- Preserved the earlier preparation report unchanged as historical evidence and explicitly superseded only its readiness and terminology conclusions here.
- Made no product, corpus, source-video, extraction, test, or delivery-asset changes.

## 7. Revised Execution Gates

Before mannequin extraction can begin:

1. Receive the complete, untruncated prompt file and verify its hash, end-of-file structure, and full instruction set.
2. Reconcile the complete prompt with repository reality and this correction report; do not infer unseen requirements.
3. Use observed-projection language and leave canonical orientation unresolved.
4. Use observation-level contact/weight labels; do not assign anatomical support/free roles.
5. Name the 1,188 × 776 format `donorPlateCanvas` and explicitly separate it from `canonical_body_space_v0_1` and the 1,536 × 2,112 corpus canvas.
6. Treat 36 as a working target only, with no video quotas, after review of all 436 frames.
7. Re-run repository synchronization and one-local-execution-slot checks immediately before execution.

The stale 123-state sentence is a confirmed independent documentation defect. It should receive a small separately authorized repair, but it is not a technical dependency of decoding the mannequin videos.

## 8. Combinatorial Impact

This review adds no product combinations. Its corrections protect future combinatorial freedom by keeping observed projection separate from runtime orientation, visual floor contact separate from anatomical support semantics, and donor delivery plates separate from canonical body-space records.

Removing per-video quotas lets the actual articulation vocabulary determine the corpus rather than forcing equal-looking source coverage. Requiring the complete prompt prevents a future extraction pass from unknowingly omitting QA or reality-state gates.

## 9. Testing / Evidence

- Re-ran `git status --short --branch`, `git rev-parse HEAD`, `git rev-parse origin/main`, and `git worktree list --porcelain`.
- Visually inspected the screenshot at original resolution.
- Recorded its file size, image properties, and SHA-256.
- Verified the 123/132 contradiction in the main README, rigging README, canonical pose-corpus document, and corpus README.
- Verified orientation, support/contact, body-scale, origin, ground, and fixed-canvas language in the canonical corpus document and machine-readable orientation/canvas records.
- Verified each challenged phrase and allocation in the earlier mannequin preparation report.
- Re-read the supplied prompt's final lines and confirmed the unclosed fence and missing tail.
- Did not run product tests or builds because no product behavior changed.

## 10. Reality State After Pass

- **SPECULATIVE:** The missing prompt contents, final frame distribution, final matte quality, and creative-workflow usefulness.
- **DESIGNED:** Corrected observed-projection terminology, donor contact vocabulary, `donorPlateCanvas` separation, quota-free 36-image working target, and revised execution gates.
- **IMPLEMENTED:** Only this report and ledger entry. The confirmed stale rigging-document sentence and earlier preparation text remain unchanged.
- **TESTED:** The six review claims against current repository/source evidence, including the 123/132 contradiction and physical prompt truncation.
- **VALIDATED:** Nothing about extracted still quality, anatomical roles, canonical orientation, or rigging value.

## 11. Known Limitations / Unresolved Questions

- The complete prompt has not been supplied, so its missing QA and closure instructions cannot be audited.
- The suggested observation-field names are not yet a versioned schema and must remain donor-manifest terminology.
- No formal projection classification has been performed on the three mannequin figures.
- No anatomical contact/support review has occurred.
- The 1,188 × 776 donor plate remains a proposed delivery choice until the complete prompt is reconciled.
- The stale 123-state rigging sentence remains in source because this request did not authorize applying corrections.
- All preparation/correction reports and their ledger changes remain uncommitted as one related dependency chain.

## 12. Recommended Next Step

Supply the complete original Markdown prompt before authorizing extraction. Then perform a bounded prompt-reconciliation pass using this correction report as evidence, apply any separately authorized documentation fixes, and only afterward re-evaluate readiness to process all 436 frames.

No task-specific server, watcher, browser tab, test process, or media process was started. The local execution slot remains released.
