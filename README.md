# 2D Doll

2D Doll is intended to become a modular scene-construction system for creating expressive illustrated characters, poses, interactions, and finished comic or panel compositions from reusable parts.

The project optimizes for **combinatorial expressive power**: a small vocabulary of compatible primitives should enable many creative outcomes instead of accumulating one-off assets and hard-coded scenes. The recurring design question is:

> What new combinations become possible because this exists?

## Current Reality

This repository contains the **design and development foundation** for 2D Doll and an inherited pre-overhaul prototype: [Canonical Base Body Rig v0.1](baselines/canonical_base_body_rig_v0_1/README.md). The inherited viewer is preserved for provenance and comparison; it is not the canonical finished architecture or a completed 2D Doll application.

- **DESIGNED:** The high-level creative model, conceptual responsibilities, terminology, and development principles.
- **IMPLEMENTED:** Repository documentation, the permanent pass-reporting protocol, and the inherited Canonical Base Body Rig v0.1 prototype.
- **TESTED:** Import integrity, archive equivalence, the inherited structural validator, and a basic repository-native browser smoke check. The smoke check reproduced the inherited startup exception; see the pass reports for exact evidence.
- **VALIDATED:** Nothing in the intended 2D Doll creative workflow yet.

The inherited v0.1 build has serious documented runtime and architecture problems. Its [functional audit](docs/audits/canonical-base-body-rig-v0.1-functional-audit.md) is inherited pre-official-repository evidence, not a test performed by this repository's import pass. Current canonical design requirements live in [Rig Requirements](docs/RIG_REQUIREMENTS.md) and remain primarily **DESIGNED**.

See [Project Context](docs/PROJECT_CONTEXT.md) for durable design intent and [Pass Reports](docs/pass-reports/README.md) for chronological evidence. Development agents must follow [AGENTS.md](AGENTS.md).

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
- [Inherited functional audit](docs/audits/canonical-base-body-rig-v0.1-functional-audit.md): pre-official-repository evidence and known failures.
- [Canonical Base Body Rig v0.1](baselines/canonical_base_body_rig_v0_1/README.md): untouched inherited pre-overhaul runtime and assets.
- [docs/pass-reports/](docs/pass-reports/README.md): permanent chronological evidence, one report per pass.
