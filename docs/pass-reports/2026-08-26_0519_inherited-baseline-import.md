# Inherited Canonical Base Body Rig v0.1 Import

## 1. Pass

- **Pass/task name:** Inherited Canonical Base Body Rig v0.1 import and documentation reconciliation
- **Objective:** Preserve the inherited rig as a historically identifiable, byte-faithful pre-overhaul baseline; import its audit and current rig requirements; reconcile repository current reality; and perform bounded import/integrity verification without repairs.
- **Branch:** `main`
- **Starting commit/SHA:** `9b385d56d253dbb69b7eb13db85895e589254994`
- **Resulting commit/SHA:** This report is contained in the resulting baseline-import commit. Resolve its immutable identifier with `git rev-parse HEAD`; embedding a commit's own final SHA in its tracked content would change that SHA.

## 2. Current Reality Before Pass

- The official repository was clean on `main`, synchronized with `origin/main`, at `9b385d56d253dbb69b7eb13db85895e589254994`.
- The repository contained its documentation and reporting foundation but no application or rig implementation.
- No target baseline, rig-requirements document, inherited audit, or `.gitignore` existed.
- **SPECULATIVE:** Detailed technical architecture and application implementation choices.
- **DESIGNED:** The high-level creative/system model and development rules.
- **IMPLEMENTED:** Repository documentation and pass-report infrastructure only.
- **TESTED:** Foundation document structure and repository state as recorded in the prior report.
- **VALIDATED:** Nothing in the intended creative workflow.

## 3. Source Archives

| Archive | Role | Files | SHA-256 |
| --- | --- | ---: | --- |
| `2d_doll_baseline_import_handoff.zip` | Inherited functional audit, current rig requirements, and import constraints | 3 | `20BEFF2D78C06E0CB533548FF08CE8E6BB1F94519DC7BBD2E8D35AC07B72B958` |
| `canonical_base_body_rig_v0_1.zip` | Primary standalone inherited v0.1 build | 212 | `1E0356AA3A1DC4A4C2555201496709E61DF13486EC79A2A271769D32720E92E7` |
| `codex_body_rig_reference_bundle.zip` | Supporting provenance and comparison source; not a production import | 418 | `6D729C114947F0FC5A84AEC1AE483303C5BE5BACF6CF78B95B3A83943B97940E` |

All three archives opened successfully, contained no duplicate paths, and contained no absolute or parent-traversal paths.

The standalone build and `codex_body_rig_reference_bundle/01_CURRENT_BUILD/canonical_base_body_rig_v0_1/` each contained 212 files. After normalizing their different archive prefixes, relative-path inventories and every per-file SHA-256 hash matched exactly: zero path differences and zero content differences.

The reference bundle's historical prototypes, videos, source projects, pixel-rig material, and quick previews were deliberately not imported.

## 4. Scope

### In Scope

- Import the complete untouched standalone v0.1 runtime, assets, previews, documentation, inventories, launcher, builder, and validator.
- Preserve a recognizable pre-overhaul identity under `baselines/`.
- Import the inherited functional audit and current rig requirements.
- Add minimal repository attributes and ignore rules that preserve baseline bytes and exclude only disposable local output.
- Reconcile README current reality and documentation navigation.
- Perform archive comparison, byte-integrity checks, structural validation, and a bounded browser launch smoke check.
- Create this permanent report and update the ledger.
- Create one bounded commit and push it to `origin/main` if verification and access succeed.

### Out of Scope

- Any runtime, architecture, validator, asset, proportion, anatomy, or documentation repair inside the inherited baseline.
- Fixing startup order, pivots, dragging, presets, reset, pose loading, PNG export, root movement, camera, pan, zoom, fit, articulation ranges, view mapping, depth, touch, or mobile behavior.
- Implementing heads, clothing, expressions, interaction points, Character Creator, Placer, IK, animation, or multiple characters.
- Importing unrelated material from the reference bundle.
- Conducting a new full functional audit or beginning the major overhaul.

## 5. Import Map

| Archive path | Repository path | Content handling |
| --- | --- | --- |
| `canonical_base_body_rig_v0_1/` | `baselines/canonical_base_body_rig_v0_1/` | All 212 files imported unchanged; only the containing `baselines/` path was added. |
| `docs/RIG_REQUIREMENTS.md` | `docs/RIG_REQUIREMENTS.md` | Imported byte-for-byte from the handoff. |
| `docs/audits/canonical-base-body-rig-v0.1-functional-audit.md` | `docs/audits/canonical-base-body-rig-v0.1-functional-audit.md` | Imported byte-for-byte from the handoff and retained as inherited evidence. |
| Reference bundle `01_CURRENT_BUILD/` | Not imported | Used only for inventory and hash comparison because it exactly duplicates the standalone build. |
| Other reference-bundle sections | Not imported | Preserved externally as provenance/reference material. |

The additional `baselines/` parent does not alter the build's internal relative paths. The launcher, viewer asset references, rig validator root calculation, and runtime contract remain internally coherent.

## 6. Changes Made

- Added `baselines/canonical_base_body_rig_v0_1/` containing 212 inherited files and 7,833,179 uncompressed bytes.
- Added `docs/RIG_REQUIREMENTS.md`, whose requirements remain primarily **DESIGNED**.
- Added `docs/audits/canonical-base-body-rig-v0.1-functional-audit.md` as explicitly inherited pre-official-repository evidence.
- Added a minimal root `.gitignore` for OS/editor debris, Python caches, disposable browser-test output, and temporary files. Required source assets and previews remain tracked.
- Added a narrowly scoped `.gitattributes` rule disabling text normalization only under the inherited baseline directory so committed blobs remain byte-identical to the archive.
- Updated `README.md` to distinguish the inherited implementation, newly performed checks, known-broken status, and absence of creative-workflow validation.
- Updated the pass-report ledger and added this report.
- Made no change inside the imported baseline after extraction.

## 7. Testing / Evidence

### Archive and Import Evidence Performed in This Pass

- Confirmed clean starting Git state and equality of local `HEAD` and `origin/main`.
- Recalculated and matched all three whole-archive SHA-256 values listed above.
- Confirmed all import targets were absent before extraction.
- Compared the standalone build with the reference bundle's current-build copy: 212 versus 212 files, identical normalized inventories, and zero per-file SHA-256 mismatches.
- After extraction, compared all 212 imported baseline files against their primary archive entries by SHA-256: **PASS**.
- Compared the imported audit and rig requirements against their handoff archive entries by SHA-256: **PASS**, byte-faithful.
- Confirmed expected runtime contract files were present, including `index.html`, `styles.css`, `app.js`, both manifests, the launcher, builder, validator, rig specification, and CSV inventories.
- Confirmed the imported asset contract contains 60 files for each of Front, 3/4, and Back, plus 15 previews and 8 package documentation files.
- Inspected the complete staged scope: 219 changed paths comprising 212 baseline files, three top-level files, and four `docs/` paths; no unrelated path was present.
- `git diff --cached --check` initially found one extra blank line at the end of the new `.gitignore`, which was removed. Its final remaining whitespace notices are the two intentional Markdown hard-break spaces on the inherited audit's date and scope lines; those bytes were preserved rather than silently rewriting historical evidence.
- A staged-blob provenance check detected that Git's Windows text filter would normalize CRLF bytes in the two inherited CSV inventories. A baseline-only `.gitattributes` `-text` rule was added and the baseline was restaged with `git add --renormalize`; raw worktree hashes then matched all staged Git blob IDs. Because Git's whitespace scanner otherwise treats the restored CSV carriage returns as trailing spaces, only those two immutable CSV inventories are marked `-diff`. This protects rather than changes the inherited bytes while leaving baseline source and Markdown diffable.

### Structural Validator Performed in This Pass

Command, run from the imported baseline root:

```text
python docs\validate_rig.py
```

Result:

```text
PASS: 3 views, 45 body parts, stable pivot contract, all referenced assets present.
```

Python 3.12.0 and Pillow 12.3.0 were used. This is structural evidence only; the validator does not establish runtime correctness or creative usefulness.

### Browser Smoke Check Performed in This Pass

The imported build was served unchanged with:

```text
python -m http.server 8000 --bind 127.0.0.1
```

The repository-native URL `http://127.0.0.1:8000/` loaded with title `Canonical Base Body Rig v0.1`. The page exposed Front, 3/4, and Back view controls; pose and stage controls; 15 part sliders; save/load controls; and a partially rendered body.

The smoke check reproduced one inherited failure exactly:

```text
ReferenceError: Cannot access 'handleCache' before initialization
    at render (app.js:106:16)
    at app.js:31:28
```

This is newly reproduced repository-native evidence of the startup defect. No controls were exercised, no downloads were triggered, and no broader functional claims were retested. The local server and temporary browser tab were closed after observation.

### Inherited Evidence Not Reclassified as New Testing

The imported audit reports broken pivot rendering/dragging, presets, reset, PNG export, and clean pose loading; missing body-root movement and camera controls; clipping; view-independent angle problems; static depth; and other limitations. Except for the startup exception above and the structural validator result, those findings were **not** reproduced by this pass and remain inherited evidence.

The inherited audit references five screenshot filenames that are absent from all three supplied archives. The audit was preserved byte-for-byte, so those five relative image references remain unresolved. No replacement evidence was fabricated or silently substituted.

## 8. Reality State After Pass

- **SPECULATIVE:** The future technical architecture, repair design, and broad product implementation choices.
- **DESIGNED:** Current canonical rig requirements, including semantic pose mapping, state boundaries, reset/export semantics, view compatibility, and future-safe depth behavior.
- **IMPLEMENTED:** The inherited Canonical Base Body Rig v0.1 source/assets now exist in Git alongside the repository documentation and reporting infrastructure.
- **TESTED:** Archive equivalence, path safety, import byte integrity, required-file presence, the inherited structural validator, and a bounded initial browser launch. The launch reproduced the startup exception.
- **VALIDATED:** Nothing in the intended 2D Doll creative workflow.

The baseline is preserved evidence, not the canonical finished architecture. No inherited runtime functionality was repaired in this pass.

## 9. Combinatorial Impact

This pass adds no new creative capability. Its combinatorial value is evidentiary: future architecture and repair work can now compare against an immutable, provenance-checked baseline, distinguish inherited behavior from regressions, and evaluate whether proposed primitives preserve or expand the intended possibility space.

The baseline is isolated under `baselines/`, so its special cases and limitations do not silently become requirements for future architecture. No existing creative possibility was removed, and no future product framework was selected or hard-coded.

## 10. Known Limitations

- The repository-native smoke check reproduces the startup temporal-dead-zone exception in `app.js`.
- The inherited audit reports serious broken, partial, missing, and uncertain behavior; only the evidence explicitly listed above was newly tested.
- The structural validator cannot detect runtime, interaction, camera, clipping, save/load, or export failures.
- Five screenshot references in the inherited audit have no supplied image files.
- `docs/build_rig.py` in the baseline contains an inherited hard-coded build output path and was not run or changed.
- The baseline contains placeholder engineering artwork, not approved final character art.
- No creative workflow has been validated.

## 11. Recommended Next Step

Run a bounded repository-native baseline verification pass before any architectural overhaul. Convert the inherited audit's most important claims into reproducible repository evidence, define a focused runtime test boundary, and answer the owner decisions recorded in the audit and rig requirements. Do not repair the rig during that verification pass; use its evidence to scope the subsequent major overhaul.
