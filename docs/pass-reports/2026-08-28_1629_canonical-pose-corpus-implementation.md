# Canonical Pose Corpus Implementation and Evidence Run

## Pass

- **Task:** Implement the canonical female pose-corpus normalization/evidence foundation and run it across the three supplied packages after the user said to proceed.
- **Objective:** Produce a deterministic, data-driven 123-state inventory, versioned corpus contracts and metadata, external fixed-canvas reference candidates, automated/visual QA, and an honest acceptance report without changing the runtime or fabricating anatomy.
- **Branch:** `main`
- **Starting commit:** `0a373b702a37cbf32d32cbeb53cfff3bd252b9c7`
- **Starting `origin/main`:** `0a373b702a37cbf32d32cbeb53cfff3bd252b9c7`
- **Resulting commit:** Uncommitted; `HEAD` remains the starting commit because the user authorized execution, not commit or push.
- **Dependency-chain state:** The related uncommitted preparation report and ledger edit were preserved and extended. No unrelated dirty files were present.

## Current Reality Before Pass

- **DESIGNED in the supplied task document:** A canonical female pose-corpus goal, landmark/root/ground concepts, body-height normalization, future-package path, QA expectations, and explicit non-goals.
- **IMPLEMENTED in the repository:** No pose-corpus code, schemas, tracked metadata, normalized outputs, or corpus QA boundary.
- **TESTED:** The prior intake pass verified the three actual ZIPs, hashes, layer structure, and 28/55/40 pose counts.
- **VALIDATED:** Nothing in the intended modular-character workflow.

The supplied Set C archive differed from the filename/structure described in the task document. The actual supplied ZIP was treated as authoritative. Instructions inside the task document were treated as the requested artifact specification, not as authority over repository safety rules or source evidence.

## Scope

### In scope

- Read ZIP entries as inert data; verify hashes, counts, image layers, embedded manifests, QA/context artifacts, dimensions, alpha evidence, and source issues.
- Define a distinct corpus schema boundary and machine-readable coordinate, landmark, orientation, export, storage, and QA contracts.
- Implement descriptor-driven future-package inventory and hash-guarded known issues.
- Preserve separate generated-proposal, authored-override, and resolved-entry layers.
- Measure capture-group stature evidence and the full-corpus canvas.
- Generate 123 similarity-transform candidates externally with premultiplied-alpha-safe resizing.
- Generate and inspect eight QA sheets; repair defects exposed by evidence.
- Add automated tests, JSON Schemas, architecture reconciliation, and mandatory pass reporting.

### Out of scope

- Runtime integration or reinterpretation of existing pose schemas.
- Manual anatomical landmark approval, canonical segment proportions, anatomical side resolution, support-foot approval, or owner profile approval.
- Local body-proportion deformation without reviewed semantic control topology.
- Source-defect repair, new pose art, garment/head/hair/accessory systems, UI work, or workflow validation.
- Commit or push.

## Changes Made

### Corpus contracts and tracked records

- Added [`docs/pose-corpus/CANONICAL_POSE_CORPUS_V0_1.md`](../pose-corpus/CANONICAL_POSE_CORPUS_V0_1.md) and the tracked corpus root under [`pose-corpus/canonical-v0_1/`](../../pose-corpus/canonical-v0_1/).
- Added machine-readable coordinate, landmark, orientation, source-package, canvas, profile-evidence, export, storage, and QA policies.
- Added JSON Schemas for source descriptors/manifests, proposals, overrides, pose entries, profile evidence, render manifests, indexes, corpus descriptors, and QA summaries.
- Registered 123 source records: Set A 28, Set B 55, and Set C 40.
- Generated 123 proposals, 123 independent empty/unreviewed override records, 123 resolved-entry documents with explicit unresolved mechanics, and a hash-linked corpus index. Matching reviewed/approved overrides are loaded and applied; authored stale-base conflicts reject before rendering.
- Kept source ZIPs and generated rasters external. Tracked records contain no absolute source or artifact path.

### Tooling

- Added the `tools.pose_corpus` package and CLI for inventory and full runs.
- The package enforces its source-descriptor schema at runtime before archive reads or output-path construction, then enforces archive hash/count/layer rules, ZIP member safety, basename-only archive identities, globally unique descriptor identities, source-scoped calibration references, declarative calibration groups, optional embedded manifests, immutable provenance, logical output paths, deterministic cross-record hashes/JSON Pointers, durable hash-guarded overrides, premultiplied-alpha linear-light resizing, fixed-canvas placement, disposition-driven quarantine lanes, and metadata-driven visual QA sidecars.
- A fourth package is added through `spec/source-packages.json`; no Set A/B/C conditional branch exists in the algorithms.
- Added pinned already-installed runtime requirements in `requirements-pose-corpus.txt` and repository ignore rules for work/generated raster locations.

### Measured evidence run

- Froze a provisional raster scale of 1,728 pixels per neutral body-height unit.
- Measured the final candidate canvas as 1,536 × 2,112 RGBA pixels, x origin 768, ground y 1,984, safety margin 87, and resampling-support reserve 8.
- Generated 123 external PNGs, eight QA JPEGs, eight QA JSON sidecars, and one local run manifest: 140 files / 110,795,651 bytes.
- Final run-manifest canonical hash: `ac562468efbe874ed0644d536183e74f045315dead72a73fe53ab3670670b1c8`.
- Final corpus-index hash: `7234cca5856568baf457e3b06e91d4ed658a78cadbb61ec60a02fc0b5015901f`.
- Final render-manifest hash: `92f9ffee89260b8b175471931e9993ffbee9463fa4da98bd04d069370563aaa6`.
- Final QA-summary hash: `10fff2a612a28060bed475c48157fdc69249ca42d6c79bf9b9828715fd33aba6`.

### Root-cause repairs during the run

1. Direct execution of the test file initially failed to import `tools`; the test harness now inserts the repository root before project imports.
2. The first contact sheet showed Set C poses 39–40 at about half stature. They are a distinct replacement-sized capture group even though replacement provenance is absent from the supplied manifest. The source descriptor now models their scale group explicitly, and a regression test prevents renewed stature collapse.
3. The second run reported all 28 Set A rasters clipped because transparent source padding exceeded the output canvas. Clipping now means lost alpha content, not cropped empty padding.
4. One Set B hair-swing pose placed threshold-1 antialias fringe two pixels inside the nominal safety margin. The canvas calculation now reserves eight pixels of resampling support before 64-pixel dimension rounding, expanding width from 1,472 to 1,536.
5. Independent closure review found that overrides were regenerated but never consumed. Runs now preserve/apply reviewed content, automatically rebase only empty scaffolds, reject stale authored bases, and test the behavior through two synthetic full runs.
6. Independent review also found pre-render entry hashes and inconsistent index self-hash views. The persisted entry is now the render input hash authority; index/render/QA/run self-hash conventions and links are recomputed and verified.
7. Hard-coded QA selections, prose, and defect-code quarantine weakened the future-package claim. Selection is now derived from source sets, semantic labels, calibration groups, pose families, and declared issues; quarantine follows descriptor disposition; a custom synthetic defect code passes end to end.
8. Source/render fragments now use resolvable JSON Pointers, and transform QA/test gates independently enforce decoded-pixel hashes, threshold-1 margins, and root/ground round-trip tolerances.
9. Final closure review found that globally resolving a calibration reference by basename could leak across future packages, duplicate group IDs could overwrite evidence, descriptor path fields were not runtime-schema-validated, and parsed ordinals outside `001`–`999` could violate serialized schemas. References are now keyed by source-set ID plus basename; the loader enforces the source-descriptor schema before I/O, basename-only archive identity, and unique descriptor IDs; the entry schema accepts any descriptor-valid prefix; ordinals reject outside the schema range; and a two-package collision fixture proves both package paths plus successful no-manifest ingestion and unsafe-path rejection.

### Repository documentation

- Updated the project and rigging entry points, female profile matrix, pose-serialization boundary, QA matrix, test instructions, and decision log.
- Added RIG-021 through RIG-026 for corpus/runtime separation, provisional profile evidence, root/ground distinctions, projection boundaries, external storage, and no-retarget-before-review.
- Added the corpus static checks to `npm test` without touching `app/`, inherited baselines, fixtures, or browser assets.

## Combinatorial Impact

The pass makes source packages combinable with one shared inventory/provenance/scale/canvas/metadata/override/QA language through data rather than package-specific code. The concurrent synthetic-package test exercises the full pipeline and demonstrates optional layers, preserved extension fields, excluded QA imagery, present and absent embedded manifests, shared basenames without cross-package leakage, generic entry prefixes, custom disposition-driven defects, durable reviewed overrides, stale-base rejection, and atomic descriptor rejection. Future reviewed mechanics can be adapted independently from source artwork, and future garment/head/hair systems can target one vocabulary without parsing PNG filenames.

The implementation deliberately does not collapse three source performers into one claimed body identity. Similarity-only candidates preserve reversible pose/perspective evidence while leaving proportion retargeting open. Profile/rear-three-quarter observations expand evidence without silently expanding the runtime orientation graph. External generated storage supports many later packages without committing large replaceable binaries.

Current restrictions are intentional: no entry can be accepted while landmarks, anatomical sides, contacts, profile measurements, and retarget controls are unresolved. This limits immediate runtime combinations but prevents hard-coded or fabricated anatomy from narrowing the future possibility space.

## Testing / Evidence

### Successful automated checks

- `python -m unittest discover -s tests -p verify_pose_corpus.py -k ImageOperationTests` — 2 tests passed after the clipping regression was added.
- `python -m unittest discover -s tests -p verify_pose_corpus.py -k FuturePackageDescriptorTests` — 2 tests passed, including two concurrent synthetic packages and two complete pipeline runs, source-scoped colliding-basename calibration, successful no-manifest behavior, generic-entry and source-descriptor schema validation, duplicate-ID/unsafe-path/out-of-range-ordinal rejection, reviewed override application/preservation, stale-base rejection, and an explicitly matched atomic descriptor-count rejection.
- Final no-write `python -m tools.pose_corpus inventory --source-directory <external>` — current hardened loader registered 123 entries (28/55/40) and reproduced source-manifest hash `2d3d1b48fd5affbe2e410034cf5488632e919e498cf0471809b50be093e6c600`.
- Final `python -m tools.pose_corpus run ...` — completed with 123 registered/candidate records, 1,728 body pixels, 1,536 × 2,112 canvas, and the expected provisional verdict.
- Full external `python tests/verify_pose_corpus.py --source-directory <external> --artifact-root <external>` — 18 tests passed in the final run.
- `npm test` — 6 Node model tests, 7 inherited-rig tests, 4 canonical-runtime tests, and 13 tracked pose-corpus tests passed; two external corpus test classes skipped as designed when external paths are omitted.
- `python -m compileall -q tools\\pose_corpus tests\\verify_pose_corpus.py` — passed.
- Recursive scan of new/modified corpus, tooling, tests, and pass-report paths for Windows drive/user paths — no matches.
- `git diff --check` — no whitespace errors; Git emitted only expected LF→CRLF working-copy notices.

### Automated final corpus evidence

- Registered: 123.
- Candidate renders produced: 123.
- Transform QA passed: 123/123.
- Review-required: 118.
- Blocked source defect: 5.
- Accepted: 0.
- Mechanics resolved: 0.
- Issue counts: 55 low-source-resolution warnings, 123 mechanics-review warnings, 123 no-retarget warnings, four corrupt-alpha source errors, one retained-backdrop source error, and one suspected-backdrop review warning.

### Visual checks actually performed

- Inspected the full checkerboard contact sheet before and after the Set C 39–40 calibration repair.
- Inspected the cross-set neutral/root/scale comparison.
- Inspected the generic declared-source-issue sheet and confirmed Set B poses 45 and 51–54 remain visibly unsuitable, pose 46 remains a review case, and Set C poses 39–40 remain labeled by unresolved provenance claims.
- Inspected the root/ground overlay sheet after the final 1,536-pixel canvas run.

### Failures and skipped checks

- An early wildcard `py_compile` invocation was invalid under Windows argument handling; later `compileall` passed.
- The first direct full test command failed with `ModuleNotFoundError`; repaired and rerun.
- Intermediate generated artifact attempts were removed and deterministically regenerated after visual, QA, and independent-review root-cause repairs. No source archive or authored repository record was deleted.
- No manual anatomical landmark review, local-warp comparison, owner exercise, runtime import, garment fit, touch/mobile test, or creative workflow validation occurred.

## Reality State After Pass

- **SPECULATIVE:** Final source-independent character artwork; production garment/head/hair/accessory compatibility; fully automatic landmarking; eventual corpus-to-runtime adapter details.
- **DESIGNED:** Corpus schemas and contracts; canonical vocabulary; approved-review path; bounded local retarget stage; future runtime adapter boundary.
- **IMPLEMENTED:** Descriptor-driven inventory, provenance, proposals/overrides/entries, provisional scale/canvas profile evidence, similarity candidate renders, external storage, QA generation, and corpus registration.
- **TESTED:** Descriptor extensibility; tracked schemas; source counts/hashes; 123 candidate render hashes and raster invariants; 123 transform-QA gates; known defect classification; eight evidence artifacts; repository regression suite.
- **VALIDATED:** Nothing in the intended modular-character workflow.

The corpus release remains `provisional_review_required`. A raster passing transform QA is not accepted. The final counts remain 0 mechanics-resolved and 0 accepted renders.

## Known Limitations / Unresolved Questions

- All requested canonical body-profile measurements remain null/unresolved.
- All 26 landmark fields are explicit, but no anatomical landmark is resolved; head/pelvis silhouette points are ambiguous proposals only.
- Anatomical L/R, support/free foot, hand/body contact, and projected joint observations require human review.
- No local proportion retarget was applied, so source-performer head/torso/limb ratios remain visible despite consistent candidate stature/canvas.
- Projection classification uses filenames plus bounded visual evidence; profile/rear-three-quarter remain reference-only and head orientation is unresolved.
- Set B pose 45 and poses 51–54 require source repair or replacement; pose 46 requires review.
- Set C pose 39–40 replacement provenance remains unverified because the actual archive manifest does not record it, although their distinct capture scale is measured.
- No runtime adapter exists; corpus entries cannot be loaded as reusable poses.
- External artifacts are present for this local run but are not committed; later consumers need the artifact root plus the tracked manifests.
- Embedded source-manifest records preserve unknown fields verbatim. Current tracked records contain no absolute local path, but a future descriptor pass should reject or explicitly classify local-path strings in those extension fields before committing them.
- The source-descriptor schema permits broad `knownIssues` objects; runtime support is data-driven, but tightening that object's required keys and disposition vocabulary remains a useful contract-hardening step.

## Recommended Next Step

Perform one bounded human-review calibration pass over neutral Front/3/4 references and representative profile, overhead, wide-stance, leg-cross, and gait poses. Author explicit landmark/orientation/contact overrides, freeze only evidence-supported profile measurements, and then compare similarity-only output against one bounded local-retarget prototype. Do not scale review to all 123 entries until that small experiment establishes pose/contact preservation and author usability.
