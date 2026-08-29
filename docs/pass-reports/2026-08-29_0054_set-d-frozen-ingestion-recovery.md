# Set D Recovery and Frozen-Ingestion Boundary

## Pass

- **Task:** Recover the interrupted Set D pass, separate full-corpus calibration from future-package ingestion, and ingest/QA Set D against the frozen canonical-v0.1 contract.
- **Branch:** `main`
- **Starting commit:** `66cd2938873e2b9fbc7f33635dc235628e3044a3`
- **Starting `origin/main`:** `66cd2938873e2b9fbc7f33635dc235628e3044a3` (`0` ahead / `0` behind)
- **Resulting commit:** none; local `HEAD` remains the starting commit.
- **Push:** none.

## Current Reality Before Pass

The repository was synchronized but dirty from an interrupted Set D full-corpus run: 388 tracked unstaged paths, 27 untracked Set D proposal/override/pose records, no staged paths, and no unpublished commits. Provenance review attributed all dirty paths to the interrupted run; no unrelated user change was found. The ignored work root contained 891 files totaling 1,126,963,593 bytes. No competing task-specific Python/test/dev-server workload or additional worktree was active.

The interrupted run had recalculated the canonical canvas from A–D aggregate extents and produced `1536 × 2176` with Ground Y `2048`, then regenerated A–C. That state was rejected. The authoritative A–C commit instead defined `1536 × 2112`, BODY `1728`, origin X `768`, Ground Y `1984`, safe margin `87`, resampling support `8`, and 64-pixel rounding.

The starting reality was therefore:

- **IMPLEMENTED / TESTED:** the committed 123-pose A–C corpus foundation at the frozen v0.1 canvas.
- **IMPLEMENTED but inappropriate for ordinary ingestion:** a full pipeline that coupled package addition to corpus-wide canvas derivation and regeneration.
- **NOT IMPLEMENTED:** a selected-package ingestion operation that preserved the existing canvas and historical per-entry bytes.
- **NOT VALIDATED:** Set D and the pose-corpus creative workflow.

## Scope

In scope:

- preserve ignored/interrupted Set D evidence without duplicating the entire work tree;
- restore only interrupted tracked/untracked repository changes after recovery capture;
- prove the A–C per-entry baseline matches `HEAD`;
- implement a generic calibration/frozen-ingestion boundary and focused tests;
- register, render, and QA the nine Set D poses against the frozen contract;
- preserve pose 009 and report overflow/review evidence instead of altering geometry or canvas;
- create a clean nine-pose ZIP and mandatory pass report.

Out of scope:

- application runtime, rig, baseline, or artwork changes;
- A–C remeasurement, per-pose regeneration, or rerendering;
- body-proportion retargeting, manual landmark resolution, render acceptance, or workflow validation;
- staging, committing, or pushing.

## Recovery and Failure Confirmation

Recovery evidence was secured under the ignored directory:

`pose-corpus/canonical-v0_1/.work/set_d_recovery_2026-08-28_233703/`

It contains the binary tracked patch, all 27 untracked Set D records, Git state, ignored-work inventory, attached recovery runbook, a human recovery manifest, and A–C integrity evidence. Important hashes:

- interrupted tracked patch: `08e5afb530e893f321f266fb3970414450e0aba9ac291b3a49c559dc40fdbafe`;
- ignored-work inventory: `7f0bfc7cb9b6aaf6e1849703612621d172c9f75990bb8cf0587f200dfbede5b7`;
- recovery snapshot: `ccabf0024e3db910bfc90106998c4a2e2c6be0f8f9886c0da93026e311bce345`;
- restored A–C per-entry integrity manifest: `dfe5f9bf6305b11ea98414dc9bfca008e957275c0ada8d3603bce19adc5d8a32`.

The original ignored work root remains intact at:

`pose-corpus/canonical-v0_1/.work/2026-08-28_2038_set_d_standardization/`

The selected recovery input is its deterministic floor-final prepared package:

`prepared_source_floor_final/pose_bg_removed_clean_corpus_source_v1.zip`

- SHA-256: `718e12022db64f97be4ec52aebc0db7dd6348c81632da8b2d34e79da158e286e`;
- members: 9 source-native PNGs, 9 prepared-RGBA PNGs, and one manifest;
- original supplied archive SHA-256: `10bdad3f4e7260321ea55408145525a41e65dc543024910801b7bc431890af98`.

After recovery capture, the exact 388 tracked snapshot paths were restored from `HEAD` and the exact 27 preserved untracked Set D paths were removed. No blanket reset or clean was used. A Git autocrlf status artifact was corrected by restoring the same explicit path list with `core.autocrlf=false`; filtered content already matched `HEAD`, and the final restored state was clean.

The exact rejected canvas expansion was confirmed in `resolve.build_proposals()`:

- A–C aggregate `yMin`: `-1873.112888`;
- A–D aggregate `yMin` after pose 009: `-1895.045328`;
- Ground Y formula: `roundUp64(ceil(-yMin + 87 + 8))`;
- A–C: `1969 → 1984`;
- A–D: `1991 → 2048`;
- lower reserve remained 99 pixels, so height rounded from `1984 + 99 → 2112` to `2048 + 99 → 2176`.

The old `run_full()` path inventoried all descriptors, remeasured all groups, derived a canvas from aggregate extents, rebuilt every proposal/override/entry, rerendered every candidate, and overwrote the entire tracked graph. The tool source was unchanged from `HEAD` before this repair; the defect was the existing operation boundary.

## Changes Made

### Generic architecture

- Added explicit `calibrate` and selected-package `ingest --source-set-id` operations. Legacy `run` requires `--canvas-policy calibrate`.
- Added descriptor-selected inventory and package-only calibration measurement.
- Added explicit `calibration` versus `frozen_ingestion` proposal canvas policy.
- Pinned canonical-v0.1 canvas values and exact canvas-file SHA-256; cross-checked `canvas.json` with `export-contract.json`.
- Added conservative physical/safe-margin fit evidence and structured `CANONICAL_CANVAS_OVERFLOW_REVIEW_REQUIRED` conditions.
- Added package-only rendering with stable aggregate index offsets and artifact-set identity.
- Added append-only aggregate source/render/index/QA merges that deep-copy existing records and preserve their order and JSON-pointer indices.
- Added pre/post byte guards for all existing proposal, override, and pose files plus canvas bytes.
- Added coordinated artifact staging and repository rollback. A failure removes the staged/finalized artifact and restores every repository target.
- Added package-local metadata, references, specs, index, render manifest, and QA report so frozen artifact sets are independently inspectable.
- Added repeatable external artifact-set root mappings to the corpus verifier.

The generic implementation contains no Set D/filename-specific rendering or placement branch. Set D-specific knowledge is confined to its data descriptor and ignored deliverable-packaging evidence.

### Set D registration and artifacts

- Added source descriptor `set_d_pose_bg_removed_clean_v1` for 9 poses using the prepared-RGBA normalization layer and source-native provenance layer.
- Added 9 proposals, 9 empty/unreviewed overrides, and 9 resolved pose records under `set_d`.
- Append-merged the source manifest, render manifest, corpus index, QA summary, and top-level corpus counts from 123 to 132 without reconstructing historical records.
- Created the ignored artifact set:

  `pose-corpus/canonical-v0_1/.work/2026-08-29_003710_set_d_frozen_ingestion/`

- Created 9 canonical transparent PNG candidates and 8 focused QA artifacts.
- Created the user deliverable:

  `deliverable/pose_corpus_set_d_canonical_v0_1.zip`

  ZIP SHA-256: `fe8ac0624c345939e1e0c23248b4066f54eec40997b0d660adabd6a38a8b288c`.

  The ZIP has 18 unique traversal-safe members: 9 pose PNGs, 3 QA contact sheets, package/source/canvas/overflow/focused-QA manifests, and checksums. Round-trip checksums and privacy scan passed; no A–C pose IDs, source archives, local absolute paths, or superseded artifacts are included.

### Documentation

Updated current pose-corpus/project/test documentation for 132 registered states, explicit calibration versus frozen ingestion, multi-artifact verification, and pose 009's review state. Historical pass reports were not rewritten.

## Combinatorial Impact

The repair makes later descriptor-defined Sets E/F/G possible without allowing new evidence to silently rewrite the v0.1 coordinate language. A package can now be inventoried, measured, placed, rendered, QA'd, and registered independently while existing packages remain authoritative input state. Artifact-set identities let independently generated raster roots coexist with one tracked aggregate registry.

Restrictions are intentional: canonical-v0.1 ingestion rejects any pinned contract drift, duplicate package ID, physical overflow, unsafe reference/path, or failed transaction. Revising the coordinate language requires the explicit calibration operation. Safe-margin entry is not hidden; it remains a candidate-level review condition. No body/profile/filename hard-coding was introduced.

## Testing / Evidence

Commands and checks actually run:

- `python tests/verify_frozen_ingestion.py`
  - initial implementation: 3/4 passed; deterministic fixture failed because ZIP member timestamps differed while PNG bytes matched;
  - timestamp-fixed fixture: 4/4 passed;
  - expanded final boundary suite: 7/7 passed in the standalone run and again through `npm test`.
- `python tests/verify_pose_corpus.py`
  - final tracked suite: 13 discovered, 11 passed, 2 expected external-input skips.
- `python tests/verify_pose_corpus.py --artifact-set-root set_d_pose_bg_removed_clean_v1.e639f4ebb52c=<Set-D-artifact-root>`
  - 17 discovered, 15 passed, 2 expected skips (A–C artifact root and external source directory not supplied).
- `npm test`
  - 6 Node model tests passed;
  - 7 inherited-rig tests passed;
  - 4 canonical-runtime tests passed;
  - 11 pose-corpus tests passed with 2 expected skips;
  - 7 frozen-ingestion tests passed.
- `git diff --check` passed at architecture gates and final closure.

Focused frozen-ingestion tests prove:

- the exact v0.1 values/hash reject coordinated canvas/export-contract drift;
- existing A–C proposal/override/pose bytes remain unchanged;
- old source/render/index aggregate prefixes and indices remain identical;
- only selected new package entries render;
- package-local references resolve;
- safe-margin review includes pose identity and boundary measurements;
- physical overflow creates structured no-mutation evidence;
- injected post-write failure rolls back repository files, new directories, and artifact output;
- duplicate ingestion rejects without mutation;
- equivalent baselines produce deterministic package metadata/hashes;
- frozen ingestion cannot call canvas derivation.

Real Set D evidence:

- 9/9 sources registered and 9/9 candidates produced at `1536 × 2112`, BODY `1728`, origin X `768`, Ground Y `1984`;
- 8/9 passed all transform checks;
- 9/9 have RGBA mode, zero border alpha, cleared transparent RGB, one connected alpha-8 thumbnail component, zero detached-area ratio, and root/ground round-trip error ≤ 0.5 px;
- pose 009 has alpha-1 bounds `[506, 85, 999, 1989]`, fits the physical canvas without clipping, and enters the top safe margin by 2 pixels; it was not cropped, rescaled, moved, or rejected from the package;
- checkerboard, black, and light nine-pose contact sheets showed no obvious pale floor/contact matte or large white/gray halo at review scale;
- hands, hair, heels/feet, ankle straps, and thin garment structures remained visible;
- source/candidate comparison plus similarity-only transforms showed no unintended pose/proportion change;
- full-resolution samples 006, 009, and 014 were inspected.

Repository immutability evidence after the real run:

- `spec/canvas.json` SHA-256 remains `fa59f6d898422b4b728b722328ec4d8f42d346ab0692d9419dce569628490c85`;
- Git reports no A–C per-entry or canvas diff;
- historical source-set, source-entry, render, corpus-index, and QA-artifact array prefixes all compared semantically identical to `HEAD`;
- counts advanced exactly `123 → 132`.

## Reality State After Pass

- **IMPLEMENTED:** explicit calibration/frozen-ingestion boundary, pinned v0.1 guard, transactional selected-package ingestion, artifact-set metadata, Set D descriptor/records/aggregates, nine candidate PNGs, focused QA evidence, and nine-pose ZIP.
- **TESTED:** architecture boundary, deterministic/rollback/overflow behavior, tracked hash/reference graph, Set D external candidates and QA manifests, A–C immutability, and ZIP structure/checksums/privacy.
- **VALIDATED:** nothing. Neither Set D nor the corpus has been demonstrated useful in the owner creative workflow.
- **ACCEPTED:** no mechanics entries or renders.

## Known Limitations / Unresolved Questions

- Set D pose 009 requires owner review for a two-pixel top safe-margin entry at alpha threshold 1. The physical canvas and alpha-8 content are not clipped.
- All landmarks, anatomical sides, support-foot semantics, and local body-proportion retargeting remain unresolved/review-required.
- Five historical Set B candidates remain source-defect quarantines.
- Visual isolation QA is evidence, not owner approval; only three final PNGs received individual full-resolution inspection in this pass, while all nine were reviewed through contact sheets and automated evidence.
- External rasters remain ignored and distributed across artifact-set roots; tracked paths are logical rather than committed binaries.

## Recommended Next Step

Have the owner review pose 009's top-edge condition and the nine-pose checker/black/light sheets, then review the bounded unstaged diff. If accepted, authorize a separate closure pass to commit and publish only the intended tracked files.
