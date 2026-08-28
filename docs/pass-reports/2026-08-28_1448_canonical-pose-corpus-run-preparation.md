# Canonical Pose Corpus Normalization Run Preparation

## 1. Pass

- **Task:** Ingest the three supplied pose archives and the supplied normalization prompt as inert evidence, reconcile them with current repository reality, and prepare a bounded run for later explicit authorization.
- **Objective:** Establish source integrity, observed corpus structure, prompt/repository conflicts, execution gates, and an evidence-backed launch sequence without implementing normalization.
- **Branch:** `main`
- **Starting commit:** `0a373b702a37cbf32d32cbeb53cfff3bd252b9c7`
- **Starting repository state:** Clean and synchronized; `HEAD == origin/main`; only the main worktree was registered.
- **Resulting commit:** No commit was created. `HEAD` remains `0a373b702a37cbf32d32cbeb53cfff3bd252b9c7`.
- **Resulting worktree change:** This pass report and its ledger entry only.

## 2. Current Reality Before Pass

- **IMPLEMENTED / previously TESTED:** The repository has a 15-part canonical runtime, three whole-body anchor views, semantic elbows, and save-only `2d-doll-pose-0.1` behavior. Those prior test claims were read from repository evidence; application tests were not rerun in this pass.
- **IMPLEMENTED / previously TESTED:** The inherited canonical base-body manifest and assets exist under `baselines/canonical_base_body_rig_v0_1/` as immutable provenance.
- **DESIGNED:** `2d-doll-pose-0.2`, a body-profile abstraction, and broader landmark/profile/orientation contracts are documented but not implemented.
- **NOT IMPLEMENTED:** No pose-corpus directory, corpus-entry schema, landmark annotation system, normalization toolchain, approved female body profile, pose loading/migration, or corpus/runtime integration exists.
- **VALIDATED:** No canonical female pose corpus or corpus-derived female body identity has been validated in the intended creative workflow.

## 3. Authority Boundary and Scope

The Markdown attachment contains a full normalization assignment. Its contents were treated as reference instructions and design evidence, not as a replacement for the user's controlling request. The controlling request for this pass was to ingest, report, and prepare to run only after the user says to proceed.

### In Scope

- Read the supplied Markdown completely as inert reference material.
- Inspect all three ZIPs without executing archive payloads.
- Verify archive integrity, structure, counts, hashes, image properties, manifests, cross-archive relationships, and selected visual QA.
- Reconcile the requested future deliverables with current repository contracts and tooling.
- Record readiness, blockers, risks, execution phases, and acceptance boundaries.
- Add the repository-mandated pass report and ledger entry.

### Out of Scope

- Creating a canonical profile, landmark metadata, corpus schemas, normalized renders, QA tooling, or runtime integration.
- Copying source archives or production assets into the repository.
- Freezing body measurements, canvas dimensions, raster scale, or artistic tolerances.
- Installing dependencies, using a remote model/API, running product tests/builds, or launching a server/browser harness.
- Modifying `app/**`, inherited baseline files, existing pose fixtures, or current runtime behavior.
- Committing or pushing changes.

## 4. Changes Made

- Added this preparation report.
- Added its chronological ledger entry.
- Extracted five supplied QA images and two Set B production samples into the session visualization directory outside the repository for inert visual inspection. No archive code was executed, and no source archive was modified.
- Removed a temporary Set B review directory created during the audit after verifying the exact resolved target was inside the system temporary directory.
- Made no product, runtime, schema, test, or source-asset changes.

## 5. Attachment Inventory and Integrity

### Prompt

- **File:** `2d_doll_canonical_pose_corpus_normalization_codex_prompt.md`
- **Size:** 42,191 bytes
- **SHA-256:** `416999A7AD82E3A25E09E2DE30CEC6CD5B218345BD9F0876DF73F75FEA49DE09`
- **Role:** DESIGNED target behavior and run requirements; not proof that package-specific claims match the supplied archives.

### Source archives

| Supplied archive | SHA-256 | Verified production structure |
| --- | --- | --- |
| `pose_19_walk_05_front_threequarter_extension_EDGE_EXTREMITY_REFINED.zip` | `98ACED237CA341323F8951E47C29481EB9D4F2477D835A10BF0B3D5EE12E230C` | 28 RGBA poses, all 1380 × 1920; 14 dance and 14 walk states; 4 QA JPGs plus README and JSON manifest |
| `comic_pose_assets_40_edge_refined_green_cleaned.zip` | `D0BA6843D38311002E18FEA6D72455722D331FD6960C92B857D0179B6C1A8397` | 40 unique poses as 40 native RGBA, 40 upscaled RGBA, and 40 native-size grayscale masks; 3 QA JPGs and 4 metadata files |
| `comic_pose_assets_55_full_isolation.zip` | `6537C8B8CDE03057F49E35958CDC85B8FB4A266FE258733972B55A618E6686B0` | 55 unique poses as 55 RGBA images and 55 matching grayscale masks; 2 QA JPGs and 4 metadata files |

The three archives contain 123 nominal production pose states: 28 + 40 + 55.

Full ZIP CRC testing passed for all three archives. All 277 file members were readable and individually hashed. No encrypted members, symlinks, absolute or traversal paths, backslash-path variants, duplicate archive paths, case collisions, hidden metadata trees, suspicious compression ratios, or exact content duplicates were found. JSON manifests parsed. Manifest record counts and dimensions matched archive contents; Set A's per-image manifest SHA-256 values also matched. Set B and Set C JSON/CSV filename order matched.

All production RGBA images have transparent outer borders, both transparent and fully opaque pixels, and cleared RGB where alpha is zero. The 40- and 55-pose masks exactly match their paired native-image alpha channels. These are structural alpha results, not proof of correct silhouette isolation.

### Set-specific observations

**Set A — 28 poses**

- The single-pose-looking archive name is misleading: this is a complete 28-pose refined replacement package, not a one-pose extension.
- Its manifest records targeted same-package hand or shoe reconstruction for poses 03, 08, 10, 13, 19, 22, and 25.
- The checkerboard sheet and targeted before/after sheet were visually inspected. They support the package's claimed pose count and reveal useful overhead, balance, hand, gait, profile, and rear-three-quarter states. The creative quality of the repairs was observed, not VALIDATED.

**Set B — 55 poses**

- Production dimensions range from 208–451 × 711–946.
- Most assets have 14 transparent padding pixels. `45_videoB_f127_profile_walk_2.png` has only four bottom padding pixels.
- Basic alpha checks pass, but visual isolation does not pass corpus-wide:
  - **Definite retained backdrop:** `poses_transparent/45_videoB_f127_profile_walk_2.png` contains a large opaque pale-gray polygon behind the figure and held object; the paired mask contains the same erroneous region.
  - **Secondary backdrop-remnant candidate:** `poses_transparent/46_videoB_f136_profile_walk_3.png` retains a smaller pale-gray region and gray contamination.
  - **Definite isolation/masking failures:** poses 51–54 contain severe jagged black/white opaque contamination and lower-leg silhouette damage.
- At contact-sheet scale, poses 01–44 and 47–50 did not show similarly large remnants; pose 55 appeared clean. That is bounded visual review, not pixel-level certification of every silhouette.
- The top-level `contact_sheet_checkerboard.jpg` is stale/conflicting: it predates later production PNG timestamps and depicts the defect under pose 55. The newer `qa/contact_sheet_checkerboard.jpg` agrees with fresh renders of the current production assets: pose 45 has the gray polygon, poses 51–54 show lower-leg corruption, and pose 55 is clean. Production PNGs, not either supplied contact sheet, must be authoritative.

**Set C — supplied 40-pose archive**

- Native dimensions are 415–994 × 1276–2589.
- Upscaled dimensions are 752–1435 × 3038–3046. The package describes a 3000-pixel minimum longest side plus transparent padding; it is not an exact 3000-pixel canonical body height or canvas.
- Native images have 12-pixel transparent padding and upscaled images have 20-pixel padding.
- The package manifest reports a 95.36% reduction in its edge-green metric and zero package-reported QA issues. Structural values were verified; the metric was not independently regenerated.
- The supplied manifest does not encode the prompt's asserted pose-39/pose-40 source-replacement provenance. That history must remain an unresolved prompt-authored claim unless a supporting source manifest is provided.

### Cross-archive relationship

No exact file duplicates exist within or across the three archives. Sets B and C reuse generic video/frame naming and share seven `(video, frame)` keys: video A frames 001, 205, and 217; video B frames 001, 046, 091, and 217. Their labels, dimensions, hashes, and silhouettes differ, so they are separate provenance records rather than deduplication candidates.

## 6. Prompt-to-Repository Reconciliation

The supplied prompt's central principle fits the repository north star: preserve pose mechanics and uncertainty while standardizing a reusable semantic coordinate/provenance contract. Several details require explicit adaptation before implementation:

1. **Set C identity:** The prompt names `comic_pose_assets_40_cleanup_polish_upscale(1).zip`; the supplied archive is `comic_pose_assets_40_edge_refined_green_cleaned.zip`. The supplied file is authoritative. Its observed contents replace the prompt's package-specific assumptions.
2. **Female profile status:** `base_female_v0_1` is a reserved but explicitly unapproved profile ID. Corpus-derived measurements must remain provisional and cannot be called VALIDATED.
3. **Stable IDs:** Repository anatomy uses IDs such as `shoulder_L` and `elbow_R`; prompt names such as `left_shoulder` need schema aliases or mapping, not a competing stable-ID system.
4. **Root semantics:** Repository `rig_root`, character root, pelvis segment, and pelvic landmark are distinct. A prompt-level `pelvis_root` must be mapped explicitly rather than silently treated as a synonym.
5. **Orientation semantics:** Current canonical whole-body IDs are `front`, `three_quarter`, and `back`. Profile and rear-three-quarter evidence should use a separate descriptive facing/projection field unless a later architecture decision versions the canonical orientation contract.
6. **Mechanical versus visual truth:** Whole-pose PNGs may be derived reference renders, but cannot become primary canonical mechanics. Landmark/contact/pose metadata must remain separable and authoritative.
7. **Schema boundary:** Corpus records need a distinct versioned contract, such as `2d-doll-pose-corpus-entry-0.1`; they must not masquerade as implemented `2d-doll-pose-0.1` or designed `2d-doll-pose-0.2` runtime payloads.
8. **Tooling reality:** Python 3.12, Pillow 12.3, and NumPy 2.5 are available. OpenCV and SciPy are absent, and no landmark estimator exists. Any required download, remote model, or new network dependency triggers a stop-and-document gate.
9. **Binary storage:** No Git LFS or large-asset policy exists. Set C's source ZIP alone is 128,106,776 bytes, so source archives should remain external and be represented by filename, archive hash, internal path, and per-file provenance. The derived-output storage policy must be frozen before generating the full corpus.
10. **Truth limit:** Flattened, clothed source figures can support provisional anchors, scale, projection, and derived reference warps. They cannot by themselves prove a single approved final body identity.

## 7. Prepared Execution Sequence

Status: **Ready to begin Phase 0/1 when the user says `proceed`; not ready to claim or generate a canonical corpus before the recorded design and QA gates are satisfied.**

1. Re-run Git synchronization, dirty-worktree, worktree, and local-execution-slot checks. Protect this report/ledger pair as the same authorized dependency chain.
2. Materialize a repository-native inventory from the verified archives and publish the inventory checkpoint before normalization.
3. Freeze corpus-entry IDs, root mapping, descriptive facing/orientation mapping, provisional profile status, immutable-source policy, and derived-binary storage policy.
4. Select high-confidence neutral and stress references; record measurement confidence, occlusion, auto/override/resolved data, and unresolved anatomy.
5. Measure the full corpus and only then freeze `BODY_HEIGHT`, body profile v0.1, fixed canvas, raster scale, margins, alpha rules, and QA tolerances.
6. Implement deterministic local tooling with editable per-pose overrides; stop and report if a network/model dependency becomes necessary.
7. Calibrate on the actual supplied Set C, then stress-test Set A, then process Set B. Set B poses 45, 46, and 51–54 enter explicit cleanup/review failure paths rather than being forced green.
8. Run completeness, image, geometry, motion-preservation, provenance, and reproducibility checks; generate checkerboard, black/light background, landmark, before/after, cross-set scale, and stress-pose evidence.
9. Update current-reality documentation and create a separate implementation pass report. Runtime integration remains a later bounded pass.

Likely new implementation areas include `docs/pose-corpus/`, `pose-corpus/canonical-v0_1/`, `tools/pose_corpus/`, and `tests/verify_pose_corpus.py`, plus bounded current-reality documentation changes. `app/**`, inherited baseline files, and existing runtime pose fixtures should remain untouched during the corpus-foundation pass.

`proceed` will authorize starting the prepared run. It will not by itself authorize a push; a commit should be created only with explicit authorization consistent with repository policy.

## 8. Combinatorial Impact

This investigation adds no new product combinations. The prepared boundary preserves future combinatorial power by making a fourth or fiftieth package target one versioned body-space, landmark, root, ground, orientation, provenance, and override language without hard-coded package branches.

Separating corpus mechanics, derived reference renders, and runtime pose payloads prevents current whole-pose artwork from restricting future faces, hair, garments, footwear, accessories, or presentation systems. Explicit projection and uncertainty fields prevent profile evidence and occluded anatomy from being flattened into misleading canonical truth.

The main accidental restrictions to avoid are approving one source performer as the canonical body by default, collapsing descriptive profile/rear views into the existing three anchor IDs, or committing large immutable archives into Git without a storage policy.

## 9. Testing / Evidence

### Repository gate

```text
branch: main
HEAD: 0a373b702a37cbf32d32cbeb53cfff3bd252b9c7
origin/main: 0a373b702a37cbf32d32cbeb53cfff3bd252b9c7
worktrees: main only
starting worktree: clean
```

Executed read-only repository checks included `git status --short --branch`, `git rev-parse HEAD`, `git rev-parse origin/main`, and `git worktree list --porcelain`. A detailed Windows process-command-line query failed with access denied; a narrower process-name query was used, and this pass started no server, watcher, build, test, or browser automation.

### Attachment evidence

- Read the Markdown prompt completely and calculated its SHA-256.
- Calculated all three archive SHA-256 values.
- Ran full ZIP CRC/member safety inspection and manifest reconciliation.
- Inspected all production image headers/alpha properties and exact mask pairing.
- Visually inspected selected supplied contact sheets and before/after sheets.
- Freshly composited the current Set B production assets for bounded isolation review and compared both packaged contact sheets against current production.
- Did not execute any archive payload or packaged script.
- Did not independently regenerate Set A repair operations or Set C's green-reduction metric.
- Did not run application tests or builds because no application behavior changed.

## 10. Reality State After Pass

- **SPECULATIVE:** Exact approved female proportions, automated landmark quality, local-retarget method, final canvas/raster scale, final tolerances, and creative usefulness.
- **DESIGNED:** The prompt's semantic normalization target, the reconciled schema boundaries, the prepared execution sequence, and the planned review/failure paths.
- **IMPLEMENTED:** Only this pass report and ledger entry. Existing repository behavior is unchanged.
- **TESTED:** Archive presence, hashes, CRC integrity, member safety, manifests, counts, image modes/dimensions, alpha/mask properties, and bounded visual isolation evidence.
- **VALIDATED:** Nothing about a normalized corpus, final character identity, artistic retarget quality, or modular-character workflow.

## 11. Known Limitations / Unresolved Questions

- Set B needs explicit cleanup/review handling for poses 45, 46, and 51–54 before their normalized reference renders can satisfy the export contract.
- Set C's prompt-asserted pose-39/pose-40 replacement provenance is absent from the supplied manifest.
- No approved female body profile or human-accepted landmark set exists.
- Landmark inference and perspective-aware local retargeting are not turnkey capabilities in the current repository.
- Derived binary storage is unresolved; generating all high-resolution outputs before freezing it risks an unsuitable Git footprint.
- The prompt asks for 123 normalized renders while also requiring graceful failure. The safe contract is 123 registered records, with failed or uncertain renders explicitly flagged rather than fabricated to reach a green counter.
- Automated checks can establish TESTED status only. Intended creative-workflow usefulness still requires owner validation.
- This report and ledger entry are intentionally uncommitted. They form the related dependency chain for the later authorized run and must be reconciled before an unrelated independent pass.

## 12. Recommended Next Step

When ready, say `proceed`. Re-run the repository/local-slot gate, then begin with the verified repository-native inventory checkpoint and the schema/storage contract freeze before producing normalized outputs.

No task-specific process remains running. The local execution slot is released.
