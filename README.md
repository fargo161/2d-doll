# 2D Doll

2D Doll is intended to become a modular scene-construction system for creating expressive illustrated characters, poses, interactions, and finished comic or panel compositions from reusable parts.

The project optimizes for **combinatorial expressive power**: a small vocabulary of compatible primitives should enable many creative outcomes instead of accumulating one-off assets and hard-coded scenes. The recurring design question is:

> What new combinations become possible because this exists?

## Current Reality

This repository contains the **design and development foundation** for 2D Doll, a first canonical Poser runtime slice, and an inherited pre-overhaul prototype preserved for provenance.

- **DESIGNED:** The high-level creative model, conceptual responsibilities, terminology, and development principles.
- **IMPLEMENTED:** A new canonical runtime under [`app/`](app/) with explicit rig-definition, pose, character/world, camera, and editor-state boundaries; complete-body fitting; independent character and camera navigation; visible root/joint/attachment handles; direct manipulation; scoped resets; semantic elbow flexion mapped across Front, 3/4, and Back; and a minimal semantic-pose save boundary. A separate [`pose-corpus/canonical-v0_1/`](pose-corpus/canonical-v0_1/) boundary registers 132 external source states, separates explicit calibration from frozen future-package ingestion, and generates fixed-canvas reference candidates without changing runtime pose state. The inherited Canonical Base Body Rig v0.1 remains unchanged under [`baselines/`](baselines/).
- **TESTED:** The new runtime's startup, complete-body fitting in all views, character/camera separation, wheel zoom, handles, representative direct manipulation, slider/numeric synchronization, arm/leg hierarchy and branch isolation, cross-view elbow mapping, reset scopes, pose persistence boundary, compatibility data, and extensible depth contract. The pose-corpus inventory, generic frozen-ingestion path, pinned-canvas and prior-entry immutability guards, schemas, 132 recorded render hashes, 131 transform-QA passes, structured overflow review, and visual-evidence manifests are also tested. Import integrity, inherited structural validation, and the inherited failure baseline remain tested. See the pass reports for exact evidence.
- **VALIDATED:** Nothing in the intended 2D Doll creative workflow yet.

The new runtime is a bounded mechanical vertical slice, not a complete Poser. Only elbows use the new cross-view semantic mapping; other joints retain transitional degree controls. Pose-dependent depth overrides have an implemented state boundary but no editor UI. The pose corpus is also provisional: all anatomical landmarks/profile measurements and contact semantics remain unresolved, no local proportion retarget was applied, five source-defect renders are quarantined, Set D pose 009 requires top-safe-margin review, and none of its 132 candidates is accepted or runtime-integrated. Pose load, PNG export from the runtime, touch/mobile validation, undo, final artwork, heads, expressions, clothing, interaction authoring, IK, animation, multiple characters, and Placer behavior are not implemented.

The inherited v0.1 viewer has serious documented runtime and architecture problems and is not the canonical runtime. Its [functional audit](docs/audits/canonical-base-body-rig-v0.1-functional-audit.md) is inherited pre-official-repository evidence; the later repository-native verification report records current reproducible evidence. Current canonical design requirements live in [Rig Requirements](docs/RIG_REQUIREMENTS.md).

See [Project Context](docs/PROJECT_CONTEXT.md) for durable design intent and [Pass Reports](docs/pass-reports/README.md) for chronological evidence. Development agents must follow [AGENTS.md](AGENTS.md).

## Run the Canonical Runtime

From the repository root:

```text
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/app/` for the runtime or `http://127.0.0.1:8000/tests/runtime.html` for the self-running browser test matrix.

Run the dependency-free repository checks with:

```text
npm test
```

The tracked pose-corpus records are included in `npm test`. A full external-raster verification additionally requires the supplied ZIP directory and generated artifact root; see the [pose-corpus test instructions](tests/README.md#canonical-pose-corpus-tests).

## Conceptual Model

2D Doll is understood through:

**STATE → CONSTRAINTS → POSSIBILITIES → PRESENTATION**

- **State** describes characters, parts, expressions, clothing, poses, props, environments, dialogue, camera, and composition.
- **Constraints** preserve meaningful relationships, anatomy, compatibility, and predictable behavior.
- **Possibilities** are the scenes and interactions that reusable state and constraints can generate.
- **Presentation** turns those possibilities into readable finished panels.

Characters and their supporting systems should remain separable where practical. Prefer parameters over duplicated variants, relationships over absolute coordinates, semantic anchors over arbitrary transforms, reversible editing over destructive changes, and graceful fallbacks over fragile perfection.

## Three Responsibilities

These are design responsibilities, not a commitment to three separate applications.

### Character Creator

Defines reusable character identity and construction: proportions, body-part artwork, faces, expressions, hair, clothing, accessories, attachment points, and character-specific constraints.

### Poser

Defines character state and relationships: articulation, whole-body movement, orientation, expression, clothing state, props, interaction points, reusable poses, and one- or two-character interactions.

### Placer

Turns posed characters into finished panels: environment, position, scale, depth, framing, effects, dialogue, captions, and export.

The responsibilities must interoperate. In particular, a pose should eventually transfer from Poser to Placer without losing its internal relationships.

## Articulation and Interaction

A character is intended to be a structured articulated object with joints, segments, anchors, constraints, render layers, and semantic interaction points—not merely a draggable flattened image. Mechanical rig truth must remain distinct from final artwork so artwork can be replaced without discarding sound rig architecture.

Semantic interaction points such as `hold`, `grab`, `look-at`, `carry`, `embrace`, `sit-on`, `prop-grip`, and `contact` should eventually express relationships between objects. Those relationships are intended to support reusable interactions rather than permanently baked poses.

These generalized canonical concepts are currently **DESIGNED**. The inherited v0.1 prototype implements a limited articulated hierarchy and pivot contract, but its existence does not prove the broader architecture or workflow. Their complete rationale and constraints live in [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md).

## Documentation Map

- [README.md](README.md): concise project entry point, current reality, architecture summary, and navigation.
- [AGENTS.md](AGENTS.md): authoritative operating rules for development work.
- [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md): durable design intent, creative goals, and architectural constraints.
- [docs/RIG_REQUIREMENTS.md](docs/RIG_REQUIREMENTS.md): current canonical rig requirements, primarily DESIGNED.
- [docs/RIG_ARCHITECTURE.md](docs/RIG_ARCHITECTURE.md): source-aligned architecture for the first canonical Poser runtime slice.
- [docs/rigging/README.md](docs/rigging/README.md): repository-native body-rig specialist team and the broader Canonical Body Rig v0.1 **DESIGNED** contracts.
- [Canonical Female Pose Corpus v0.1](docs/pose-corpus/CANONICAL_POSE_CORPUS_V0_1.md): measured source-ingestion, coordinate, scale/canvas, provenance, normalization-candidate, and QA contract with explicit unresolved mechanics.
- [Expression Maker and Face Intake](docs/design/expression-maker-face-intake.md): authoritative **DESIGNED** context for the combinatorial facial system and its normalization workflow.
- [Combinatorial Panel Composition, Interactive Elements, and Effects](docs/design/combinatorial-panel-composition-and-interactions.md): authoritative **DESIGNED** philosophy for semantic scenes, reusable interactions, modular environments, and event-driven presentation.
- [Inherited functional audit](docs/audits/canonical-base-body-rig-v0.1-functional-audit.md): pre-official-repository evidence and known failures.
- [Canonical Base Body Rig v0.1](baselines/canonical_base_body_rig_v0_1/README.md): untouched inherited pre-overhaul runtime and assets.
- [docs/pass-reports/](docs/pass-reports/README.md): permanent chronological evidence, one report per pass.
