# Combinatorial Panel Composition and Interaction Design Philosophy

## 1. Pass

- **Task:** Establish the canonical combinatorial panel-composition, interactive-element, and effects philosophy.
- **Objective:** Create one implementation-neutral design document that expands the project's combinatorial principles into semantic scene composition, object capabilities, relationship constraints, modular environments, and event-driven presentation without implementing product behavior.
- **Branch:** `main`.
- **Starting commit:** `67c41a501e1f49066a13f70d0ad24f3d34cec33b`.
- **Starting repository state:** The working tree already contained concurrent rigging-documentation modifications, an already-modified pass ledger, the untracked `docs/body-rig-maker/` tree, and four untracked pass reports. These changes were preserved and excluded from this pass except that this pass appended its own row to the existing ledger.
- **Resulting commit:** No commit was authorized or created; `HEAD` remains the starting commit.
- **Push:** Not authorized and not performed.

## 2. Current Reality Before Pass

- **SPECULATIVE:** General panel scene graphs, Placer implementation, environment kits, relationship-object deformation, connector occlusion, event models, effect selection, crowd representations, and their user interfaces and concrete schemas.
- **DESIGNED:** The project-level `STATE → CONSTRAINTS → POSSIBILITIES → PRESENTATION` lens; Character Creator, Poser, and Placer responsibilities; semantic anchors and relationships; structured Poser-to-Placer transfer; and non-destructive, graceful-fallback principles. The newer rigging canon had already defined a narrower typed anchor model and transfer boundary.
- **IMPLEMENTED:** Repository documentation and the separately documented bounded Poser/body-rig runtime. No equivalent canonical panel-composition philosophy document existed.
- **TESTED:** Only the bounded runtime and repository properties recorded by earlier evidence. No general panel, environment, connector, event-effect, or Placer workflow was tested.
- **VALIDATED:** Nothing in the intended end-to-end 2D Doll creative workflow.

Existing material in `README.md` and `docs/PROJECT_CONTEXT.md` established the durable thesis but only summarized the requested domain. `docs/rigging/architecture/INTERACTION_ANCHOR_MODEL.md` and `POSE_SERIALIZATION_CONTRACT.md` supplied narrower body-rig and transfer contracts. Creating a dedicated document under `docs/design/` was preferable to overloading or competing with those sources.

## 3. Scope

### In scope

- Inspect repository instructions, documentation conventions, current canonical design, current source claims, the interaction-anchor contract, and Poser-to-Placer transfer boundaries.
- Create one authoritative, implementation-neutral design philosophy for semantic panel composition, interactive objects, relationships, modular environments, camera state, crowds, and visual effects.
- Add one root documentation-map link and the mandatory pass-report ledger entry.
- Verify link resolution, changed-file scope, documentation hygiene, and reality-state claims.

### Out of scope

- Application, UI, schema, renderer, constraint solver, connector, environment, effect, or Placer implementation.
- Source code, tests, dependencies, runtime behavior, rig mechanics, assets, images, masks, extraction, or generation.
- Modification of existing rigging contracts, historical reports, or unrelated concurrent work.
- Commit or push.

## 4. Changes Made

- `docs/design/combinatorial-panel-composition-and-interactions.md` — created the canonical design philosophy.
- `README.md` — added one documentation-map link to the new canon.
- `docs/pass-reports/2026-08-26_0927_combinatorial-panel-composition-design.md` — created this evidence report.
- `docs/pass-reports/README.md` — appended this pass to the chronological ledger without removing or rewriting concurrent entries.

The design establishes:

- `STATE → CONSTRAINTS → POSSIBILITIES → PRESENTATION` as the governing panel-composition lens;
- Poser ownership of internal performance and relationships, and Placer ownership of reader-facing staging and export;
- an ordered semantic scene model separating role, depth, interaction ownership, render order, and editing ownership;
- interaction-first object classification with multiple reusable capabilities per object;
- semantic character, object, environment, restraint, and effect anchors;
- entity/relationship graphs, reusable interaction recipes, and reusable connector objects;
- independent action, contact, reaction, and presentation state;
- event-derived whip, sword, punch, and magical presentation families;
- persistent, momentary, attached, relationship, environmental, lighting, and comic effects;
- modular environment kits and semantic environment interaction points;
- structured, reversible camera and panel state;
- separate primary-character and crowd-element cost models;
- non-destructive editing, compatibility feedback, fallbacks, and artwork-replacement resilience;
- generic scene decompositions, anti-patterns, evaluation questions, and unresolved design questions.

## 5. Combinatorial Impact

The canon defines a possibility space in which one chair, grip, chain, effect component, environment module, or interaction recipe can participate in many scenes instead of being duplicated for each finished outcome. It allows behavior to combine with multiple visual variants, relationships to survive camera and artwork changes, and event meaning to combine with replaceable presentation styles.

Intentional restrictions protect that range: appearance does not own behavior; participants are not fused into recipes; Poser relationships are not flattened during transfer; effects do not dictate reactions; connector configurations do not become unrelated assets; and unresolved compatibility is preserved and explained rather than silently discarded.

No creative capability was implemented by this pass. The expanded possibility space remains **DESIGNED**.

## 6. Testing / Evidence

### Executed checks

- Inspected root `AGENTS.md`, the nested `docs/rigging/AGENTS.md`, repository status, branch, actual starting `HEAD`, documentation layout, project context, rig requirements, source-aligned Poser architecture, Expression Maker design, interaction-anchor contract, Poser-to-Placer transfer contract, pass-report protocol, and concurrent rigging documentation.
- Searched current documentation for Character Creator, Expression Maker, Poser, Placer, articulation, interaction points, semantic anchors, props, effects, scene composition, panel export, relationships, and connectors. No equivalent canonical panel-composition document existed.
- `npm test` passed: 6/6 Node model tests, 7/7 inherited-rig verification tests, and 4/4 canonical-runtime verification tests.
- Checked 45 relative Markdown links across the new document and modified navigation/evidence files; every target resolved.
- The initial ad hoc link check mishandled root-level files because PowerShell returned an empty parent for `README.md`. The command was corrected to resolve an empty parent as the repository root and rerun successfully. The initial verifier failure was not a documentation failure.
- Confirmed every required philosophy topic through a heading/key-concept audit, including the two governing transformations, Poser/Placer boundary, five scene-order dimensions, capability families, relationship objects, four event stages, effect categories, modular environments, camera/panel state, crowd distinction, anti-patterns, evaluation questions, open questions, and all five reality-state labels.
- Reviewed unsupported-claim search results; no language claiming that the designed panel systems are currently implemented, tested, or validated was found.
- `git diff --check -- README.md docs/pass-reports/README.md` passed with line-ending advisories only. A direct trailing-whitespace check passed for all four pass files, including the two untracked new documents.
- Reviewed the path-scoped diff and status. This pass added or modified only the four Markdown files listed in Changes Made. Pre-existing concurrent rigging and body-rig-maker changes remained present and were not rewritten by this pass.

### Scope evidence

No application source, tests, dependencies, runtime files, visual assets, generated images, masks, rig behavior, or historical pass reports were added or changed by this pass. The regression suite was executed without modifying its tests.

### Skipped checks

- No repository-native Markdown linter or documentation build is configured, so none was run.
- No browser, image, asset, connector-rendering, scene-composition, or creative-workflow test was run because this pass implemented none of those systems.

## 7. Reality State After Pass

- **SPECULATIVE:** Concrete schemas, engines, solvers, render algorithms, connector deformation and occlusion, effect-selection logic, crowd representation, material processing, user interfaces, and production file formats.
- **DESIGNED:** The panel, interaction, capability, anchor, relationship, environment, event/effect, camera, crowd, fallback, and evaluation philosophy established by the new document.
- **IMPLEMENTED:** The documentation artifact, README navigation, and evidence record exist. Separately documented bounded Poser/body-rig behavior remains implemented within its existing scope. No described Placer or general-interaction behavior is implemented.
- **TESTED:** Documentation and unchanged regression checks only where recorded below after execution. No product behavior described by this philosophy is tested.
- **VALIDATED:** Nothing in the intended panel-making workflow.

## 8. Known Limitations / Unresolved Questions

- The minimum universal anchor and object-capability vocabularies require evidence.
- The distinction and mapping among semantic depth, render order, masks, and connector crossings remain open.
- The exact Poser/Placer boundary for contextual pose edits needs an owner decision and workflow evidence.
- Compatibility authoring, validation, user feedback, and manual override behavior need a bounded prototype.
- The minimum event model and degree of automatic pose/effect assistance remain undecided.
- Crowd representation and promotion to primary-character state remain open.
- No real scene has yet demonstrated that these primitives are sufficient or usable.

## 9. Recommended Next Step

Run a separately authorized, documentation-first minimum-scene architecture pass that selects one small generic composition with two characters, one support surface, one held prop, one connector, and one attached or contact effect. Define only enough state ownership and acceptance behavior to test preservation from Poser into Placer, including missing-anchor fallback and one front/behind connector crossing. Do not broaden it into production implementation until the owner approves the resulting boundary.

## 10. Final Git State

- **HEAD:** `67c41a501e1f49066a13f70d0ad24f3d34cec33b`, unchanged from the actual pass start.
- **Working tree:** Dirty. It contains the four intended documentation paths from this pass plus unrelated concurrent rigging/body-rig-maker changes that were already present at pass start.
- **Commit status:** Uncommitted; commit and push were not authorized.
