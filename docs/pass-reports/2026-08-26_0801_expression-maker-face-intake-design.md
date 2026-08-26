# Expression Maker and Face Intake Design Context

## 1. Pass

- **Task:** Create the Combinatorial Expression Maker and Face Intake Design Context.
- **Objective:** Establish one durable, authoritative facial-system design document without implementing product behavior.
- **Branch:** `main`.
- **Starting commit:** `cb55091b2dda1dc55195b234f37fee44efad81cb`.
- **Starting repository state:** `main` was two commits ahead of `origin/main`. The working tree already contained an unrelated modified pass ledger plus untracked reports `2026-08-26_0733_task-000-zip-ingestion.md` and `2026-08-26_0750_body-rig-architecture-commit-closure.md`; they were preserved and excluded from this pass.
- **Resulting commit:** Recorded by Git history and the final task response if a clean path-scoped commit is created. A commit cannot contain its own final SHA.
- **Push:** Not authorized and not performed.

## 2. Current Reality Before Pass

- **SPECULATIVE:** Facial extraction technology, production face schemas, asset formats, automatic segmentation, and final authoring/runtime interfaces.
- **DESIGNED:** Project-level Character Creator, Poser, and Placer responsibilities; regular/back head presentations; structured state and transfer principles; expressions as future appearance/pose state.
- **IMPLEMENTED:** A bounded canonical body-rig/Poser runtime and repository documentation. No Expression Maker, Face Intake, facial component library, character face-rig package, or expression runtime existed.
- **TESTED:** The bounded body-rig/Poser runtime and inherited-baseline checks described by prior reports. No facial authoring workflow was tested.
- **VALIDATED:** Nothing in the intended 2D Doll creative workflow.

Repository search found no existing authoritative face/expression design document and no Batch 1 face assets. Existing references were brief scope statements or transfer placeholders, so extending them would have mixed body-rig and facial-authoring responsibilities.

## 3. Scope

### In scope

- Inspect applicable instructions, documentation conventions, current source reality, head-presentation contracts, and Poser-to-Placer state boundaries.
- Create one implementation-neutral design context for Expression Maker and guided Face Intake.
- Record shared semantics versus character identity, component ontology, compatibility, provenance, fallbacks, asymmetry, hair occlusion, prior Batch 1 review context, and validation experiments.
- Update repository navigation and the mandatory pass ledger.
- Run documentation hygiene and unchanged regression checks.

### Out of scope

- Runtime, user-interface, schema, importer, detector, segmenter, renderer, or serialization implementation.
- Production face assets, masks, landmarks, component extraction, binary archives, or asset copying.
- Selection of a programming language, framework, computer-vision model, or storage format.
- Modification of existing body-rig contracts, application code, tests, baselines, historical reports, or unrelated concurrent work.
- Push to a remote.

## 4. Repository Inspection and Document Placement

Applicable instructions came from root `AGENTS.md`, including precise reality-state vocabulary, functional-truth priority, combinatorial-impact review, non-destructive state, documentation roles, and mandatory pass reporting.

Reviewed documentation included `README.md`, `docs/PROJECT_CONTEXT.md`, `docs/RIG_REQUIREMENTS.md`, `docs/RIG_ARCHITECTURE.md`, the rigging entry point and canonical body/head/orientation contracts, the Poser-to-Placer serialization contract, the pass ledger, and recent report conventions.

The authoritative document was placed at `docs/design/expression-maker-face-intake.md`. A dedicated design path avoids overloading the durable general project context or the body-rig specialist program. It also makes the boundary explicit: facial design consumes the existing regular/back head and transfer contracts but does not redefine body orientation or claim body-rig implementation.

## 5. Changes Made

- `docs/design/expression-maker-face-intake.md` — created the authoritative combinatorial facial-system design context.
- `README.md` — added the design document to the existing Documentation Map.
- `docs/pass-reports/2026-08-26_0801_expression-maker-face-intake-design.md` — created this evidence report.
- `docs/pass-reports/README.md` — added this pass to the chronological ledger while preserving pre-existing concurrent entries.

The design defines:

- Expression Maker as a Character Creator sub-mode and Face Intake as guided, non-destructive upstream normalization;
- `STATE → CONSTRAINTS → POSSIBILITIES → PRESENTATION` for facial state;
- a shared semantic schema resolved through character-specific geometry, artwork, identity, limits, and fallbacks;
- exactly regular/back head presentations, distinct from the body's Front/3/4/Back orientation families;
- identity base, eye/mouth complexes, independent eyebrows, brow-region detail, bounded deformation, structured presets, and full-face fallback;
- left/right independence with optional linking, explicit compatibility and warnings, and hair/headwear/accessory separation;
- character-specific presets versus cross-character semantic recipes;
- a nine-stage Face Intake workflow, conceptual implementation-neutral data model, and non-destructive provenance lifecycle;
- Poser/Placer transfer and final-flattening boundaries;
- bounded prior Batch 1 observations without claiming repository ownership or direct verification;
- the decisive novel-recombination experiment and open questions for evidence-driven prototypes.

## 6. Combinatorial Impact

The document establishes primitives and constraints that can eventually combine eye, eyelid, gaze, eyebrow, mouth, detail, and bounded deformation state without accumulating one flattened head per expression. Left/right independence permits asymmetric performances; semantic recipes permit character-specific realizations of shared intent; explicit fallbacks allow difficult expressions without corrupting the modular contract; and structured transfer preserves facial intent through pose and panel presentation.

Intentional restrictions protect existing possibilities: components remain character-specific unless resolved semantically; regular/back remain the only required head presentations; hair is not baked into every expression; unsupported interpolation is not invented; and invalid combinations warn, remain unresolved, or use declared fallbacks rather than silently changing identity.

No creative combination was implemented by this documentation pass. These combinations remain **DESIGNED** until source and evidence support stronger claims.

## 7. Testing / Evidence

### Executed checks

- Inspected branch, starting HEAD, status, tracked documentation, current runtime claims, head-presentation matrix, transfer contract, and documentation hierarchy.
- Searched canonical documentation for existing face, expression, Character Creator, Poser, Placer, head-presentation, and normalization material; no competing authoritative facial-system document was found.
- Searched repository filenames for Batch 1 character/face-expression image assets; none were found.
- `npm test` passed: 6/6 Node model tests, 7/7 inherited-rig verification tests, and 4/4 canonical-runtime verification tests.
- `git diff --check` passed with only existing line-ending advisories for `README.md` and the pass ledger.
- Verified all new direct relative-link targets exist.
- Reviewed the design document headings and acceptance content for Expression Maker ownership, Face Intake, shared/character-specific state, regular/back presentations, facial ontology, brow distinction, asymmetry, compatibility, hair separation, presets/recipes, fallbacks, provenance, transfer, Batch 1 context, pixel-subtraction warning, decisive experiment, reality states, open questions, and non-goals.
- Inspected intended changed/untracked file extensions; all files introduced by this pass are Markdown.

### Scope evidence

No application source, tests, baseline files, or binary assets were edited or added by this pass. The unrelated reports and ledger additions present at pass start were preserved.

### Skipped checks

- No Markdown linter is configured in `package.json`, so no project Markdown-lint command was available.
- No browser, image, asset, segmentation, serialization, or creative-workflow test was run because this pass implemented none of those systems and the reviewed Batch 1 assets are absent.

## 8. Reality State After Pass

- **SPECULATIVE:** Automatic segmentation/extraction, unrestricted or continuous morphing, generated hidden-region reconstruction, procedural fine-grained face controls, universal cross-character recipe transfer, and automated compatibility scoring.
- **DESIGNED:** Expression Maker/Face Intake ownership and workflow; shared semantics with character-specific identity; face-rig ontology; compatibility; fallbacks; provenance; asymmetric controls; recipe/preset distinction; and Poser/Placer interoperability.
- **IMPLEMENTED:** The authoritative design artifact, README navigation, and evidence report exist in the repository. The pre-existing body-rig/Poser runtime remains implemented within its prior bounded scope. No facial product behavior is implemented.
- **TESTED:** Documentation link/scope/diff hygiene and the unchanged repository regression suite. No facial authoring or runtime behavior is tested.
- **VALIDATED:** Nothing in the intended Expression Maker or Face Intake creative workflow.

## 9. Known Limitations / Unresolved Questions

- Eye complexes versus independently movable pupils remains an evidence-driven implementation choice.
- Required surrounding-skin masks, feather representation, safe local warp, and makeup compatibility remain undefined.
- Intensity may be discrete, continuous, or preset-specific.
- Compatibility authoring/visualization and rejection thresholds need prototype evidence.
- Full-expression fallback selection and later reevaluation need concrete state semantics.
- Shared semantic recipe coverage across diverse characters remains unvalidated.
- Minimum useful expression coverage for real panel construction is unknown.
- Batch 1 counts and qualitative findings remain prior external review context because the files are absent.

## 10. Recommended Next Step

Authorize one bounded manual vertical-slice experiment using a well-prepared character, preferably Carrie if the referenced source set becomes available. Preserve a neutral reference and provenance; normalize only enough eye, brow, mouth, and detail primitives to reconstruct one source expression and create one novel expression; then test neutral restoration, seams, identity preservation, compatibility explanations, structured save/reload, and declared fallback. Do not broaden that prototype into automatic segmentation, a production schema, or a complete UI before its evidence is reviewed.

## 11. Final Git State

Final status, exact commit SHA if created, and the path-scope comparison are reported in the task response after post-report verification. No push is performed.
