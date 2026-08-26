# Expression Maker and Face Intake: Combinatorial Facial System

## Status and Authority

This document is the authoritative **DESIGNED** context for Expression Maker and its upstream Face Intake / Expression Normalization workflow. It defines responsibilities, state boundaries, constraints, workflows, and validation targets. It does not establish that any facial authoring, extraction, runtime, schema, asset, or user-interface behavior is implemented.

The facial system extends the project context in [Project Context](../PROJECT_CONTEXT.md), consumes the current regular/back head-presentation contract in [Rig Requirements](../RIG_REQUIREMENTS.md), and must preserve expression references through the [Pose Serialization and Poser-to-Placer Transfer](../rigging/architecture/POSE_SERIALIZATION_CONTRACT.md) boundary. Where a body has Front, 3/4, and Back orientation families, `regular` remains the one semantic facial head presentation used with compatible Front and 3/4 torsos; it is not a third body orientation or an implicit fallback.

## Purpose

The system must preserve this transformation:

> **Expression source sets → normalized character face rig → reusable facial primitives → semantic expression recipes → Poser state → Placer presentation**

The objective is combinatorial expressive power: a small, compatible library of character-specific facial primitives should reproduce known expressions and create convincing expressions that were never present in the sources. A flattened face image may be a preview, fallback, or final export result. It is not the underlying authoring model.

## Architectural Placement

### Character Creator and Expression Maker

Expression Maker is a Character Creator sub-mode, not a peer to Poser or Placer. Character Creator owns reusable identity and construction:

- character-specific head proportions and neutral/base facial artwork;
- facial anchors, masks, compatible regions, and local geometry limits;
- eye complexes, eyelids, gaze behavior, eyebrows, mouth complexes, and expression-detail patches;
- bounded deformation channels;
- hair, headwear, and accessory relationships;
- compatibility rules and full-expression fallbacks;
- character-specific expression presets and semantic recipe mappings.

Expression Maker operates on that authored material. It previews compatible combinations, links or separates paired controls, permits bounded adjustment, records structured presets, explains constraints, and restores the neutral face. It must not silently alter permanent character identity.

### Face Intake / Expression Normalization

Face Intake is a guided upstream authoring or import utility. It converts messy expression source sets into standardized, editable, character-specific facial assets for Expression Maker. It may be a utility, workflow, or sub-mode rather than a permanent top-level product responsibility.

Face Intake assists with neutral selection, landmarks, alignment, face-plate definition, hair/background exclusion, region suggestions, mask correction, local color normalization, bounded deformation definition, semantic labeling, compatibility review, cross-combination testing, provenance, and export into a character face rig. It is not a guaranteed one-click converter, and it must expose uncertain or rejected results for human review.

### Poser

Poser consumes expressions already authored for a character. It selects saved presets, preserves complete facial state with whole-body pose and interaction state, and may expose a deliberately limited subset of safe controls. Poser does not reconstruct source images or re-author the face.

### Placer

Placer receives the posed character with expression relationships intact. Panel position, scale, depth, framing, tint, lighting, effects, dialogue, and export may change presentation without destroying the expression recipe or its resolved character-specific state.

## Combinatorial Model

The facial subsystem applies the project lens:

> **STATE → CONSTRAINTS → POSSIBILITIES → PRESENTATION**

### State

Facial state describes:

- head presentation and neutral face identity;
- left and right eye, eyelid, gaze, and eyebrow state;
- mouth state and local component transforms;
- jaw and lower-face deformation;
- optional expression-detail overlays;
- selected preset and any safe overrides;
- hair/headwear occlusion relationships;
- requested, effective, fallback, compatibility, and quality state.

### Constraints

Constraints prevent arbitrary combinations from becoming broken collages. They include character geometry, head presentation, anchor and mask compatibility, overlap boundaries, hair/headwear occlusion, rendering style, lighting, skin tone, makeup continuity, transform limits, deformation dependencies, left/right anatomical relationships, component compatibility groups, source quality/confidence, seam risks, and explicit fallback requirements.

### Possibilities

Within those constraints, the system should enable symmetric or asymmetric expressions, linked or independent eyes and brows, gaze changes, mouth variants, bounded intensity, optional detail activation, saved presets, character-specific realizations of shared semantic recipes, and novel combinations absent from the source set.

### Presentation

Resolved state may be previewed in Expression Maker, selected or safely adjusted in Poser, preserved during whole-body posing and interactions, transferred intact to Placer, rendered below separate hair/headwear layers, serialized with the character, and flattened only when a final image or deliberate fallback requires it.

The target is a constrained possibility space, not an unconstrained collage and not a fixed catalog of complete expressions.

## Shared Schema and Character-Specific Identity

The system uses:

> **A shared semantic schema with character-specific geometry and artwork**

Shared anchors may include `head_origin`, `face_plate_bounds`, `left_eye`, `right_eye`, `left_brow`, `right_brow`, `nose_bridge`, `nose_base`, `mouth_center`, `left_mouth_corner`, `right_mouth_corner`, `chin`, `left_jaw`, `right_jaw`, optional gaze targets, and optional deformation regions.

Each character retains its own head width and height, face angle, eye spacing and size, eyebrow placement, nose and mouth positions, jaw width, chin length, proportions, masks, transform limits, hair occlusion, neutral texture, makeup, and component artwork. Standardization creates interoperability; it must not force one photographic head shape or homogenize identity.

Expression processing must lock stable identity features explicitly. It must not silently rewrite the neutral facial surface, head proportions, jaw, chin, nose identity, ears, skin texture, permanent marks, permanent makeup, neutral lighting assumptions, or regular-head orientation.

## Head Presentations

The current head contract has exactly two semantic presentations:

- `regular`
- `back`

Expression controls apply to `regular`. The `back` presentation normally exposes no visible face controls and remains separate visual head artwork. The regular artwork may look slightly three-quarter for a particular character, but it remains the one semantic regular presentation. The body rig's Front/3/4/Back orientation families do not create a required third facial head family.

The torso/head compatibility contract remains authoritative: regular may pair with compatible Front or 3/4 torsos; back pairs with Back. A presentation mismatch must be rejected or resolved through an explicitly declared compatible fallback, never by silently substituting regular for back. Future head presentations must be additive, versioned, and backed by evidence.

## Mechanical Face-Rig Truth and Final Artwork

Mechanical facial-rig truth includes anchors, component ownership, hierarchy, masks, bounds, transform ranges, compatibility constraints, deformation channels, serialization, preset references, requested/effective fallback state, and provenance.

Final artwork includes skin rendering, eyelashes, makeup, eyebrow texture, lips, teeth, tongue, wrinkles, shadows, highlights, and character style. Artwork refinement or replacement should not require redesigning sound state and compatibility contracts. Conversely, plausible artwork does not prove that the mechanical face rig is correct.

## Face-Rig Ontology

### Identity Base

The identity base is the stable character-specific face: neutral surface, proportions, jaw, chin, nose, ears where relevant, skin texture, permanent makeup or marks, neutral lighting assumptions, regular-head orientation, and hair/headwear exclusion boundaries. Neutral restoration must return to this authored identity without residue from a prior expression.

### Facial Component Libraries

#### Eye Complexes

The first practical primitive may treat each eye as a bounded complex containing sclera, iris/pupil, eyelids, eyelashes, immediate surrounding skin, and eye makeup. Left and right remain independently addressable. A later version may separate pupils or procedural eyelids, but the initial contract does not require those unvalidated complications.

Eye semantics may include neutral, half-lidded, wide, narrowed, closed, or other authored states. Eyelid openness and gaze are distinct semantic controls even when a particular artwork asset resolves them together. Independent left/right gaze is allowed only where character assets and anatomical constraints make it safe.

#### Eyebrows

Left and right eyebrow hair shapes remain independently addressable. Possible bounded controls include variant, height, rotation, limited offset, and linked/unlinked editing.

#### Mouth Complexes

The first reliable mouth primitive may combine upper and lower lips, teeth, tongue, mouth interior, and immediate surrounding skin. Later evidence may justify splitting those elements. The architecture does not require that split before the combined mouth system works.

#### Expression-Detail Regions

Optional overlays may represent forehead creases, glabella compression, upper-nose wrinkles, under-eye tension, cheek raise, nasolabial compression, or localized deformation shadows/highlights. These are first-class because intense expressions may fail when only eyes, eyebrows, and mouth change.

### Eyebrow Hair and Brow Region

`eyebrow` means the hair shape: arch, angle, height, compression, asymmetry, and rotation. `brow region` means surrounding skin and tissue: forehead movement, the vertical crease between brows, raised or compressed inner brow, horizontal forehead lines, and upper-nose tension.

The two must not be collapsed. Angry eyebrow artwork over neutral brow-region skin may be unconvincing; worried inner-brow movement without corresponding forehead/tissue change may also fail.

### Deformation Channels

Some expressions require geometry beyond a replaceable patch. Character-specific bounded channels may include jaw drop, lower-face elongation, cheek compression, brow-region compression, mild mouth-width change, chin displacement, and limited local warp.

Channels must be narrow, explicit, reversible, and dependency-aware. The design does not promise unrestricted mesh deformation or continuous morphing among arbitrary source images. A value outside an authored safe range must clamp, warn, fall back, or remain unsupported according to explicit policy.

### Expression Presets

An expression preset is a structured recipe referencing component selections and transforms, linked/unlinked state, gaze, deformation values, detail overlays, supported intensity, compatibility requirements, fallback resolution, quality status, and source provenance. It is not ordinarily just a flattened replacement head.

### Full-Expression Fallbacks

Some expressions change too much of the face to decompose reliably. The same preset interface may resolve to:

- fully modular;
- partially modular;
- full normalized face-plate fallback;
- unsupported;
- provisional pending review.

A full-face fallback is deliberate graceful degradation. Its identity, source, occlusion behavior, compatibility limits, and requested/effective resolution remain explicit.

## Conceptual Data Model

The model below is implementation-neutral and does not select a language or serialization format:

```text
CharacterFaceRig
  schemaVersion
  characterId
  supportedHeadPresentations
  geometryProfile
  anchors
  neutralBase
  identityLayers
  occlusionMasks
  componentLibraries
  deformationChannels
  expressionPresets
  semanticRecipeMappings
  fullExpressionFallbacks
  compatibilityRules
  sourceProvenance
```

```text
ExpressionPreset
  id
  label
  headPresentation
  components
    leftEye
    rightEye
    leftBrow
    rightBrow
    mouth
  parameters
    leftEyeTransform
    rightEyeTransform
    leftEyelidState
    rightEyelidState
    gaze
    leftBrowTransform
    rightBrowTransform
    jawDrop
    lowerFaceDeformation
    intensity
  detailOverlays
  compatibilityRequirements
  requestedResolution
  effectiveResolution
  fallbackReference
  qualityStatus
  sourceReferences
```

Whatever implementation follows must preserve the separation among identity, components, parameters, presets, compatibility, fallbacks, and provenance. It must also distinguish requested semantic state from an effective fallback so newly available compatible artwork can be reevaluated without losing intent.

## Face Intake Workflow

Face Intake is non-destructive. Every accepted or rejected result remains traceable to preserved inputs and author decisions.

### 1. Source Registration

Import expression images without overwriting originals. Preserve filenames, source files, dimensions, orientation, provenance, and quality notes. Identify candidate neutral images, select one authoritative neutral reference, and retain alternates without silently mixing identity information among them.

### 2. Identity Fitting

Performed once per character: establish the regular-head coordinate system; place facial landmarks; define head, face, eye, brow, nose, mouth, jaw, and chin bounds/anchors; record character proportions; define safe and excluded regions; define canonical hair/headwear occlusion; and lock identity features.

### 3. Expression Alignment

Performed per source: align translation, scale, and limited rotation to the authoritative head; account for mild perspective or yaw differences; measure drift; and flag excessive angle or identity changes. Automatic warping must not conceal severe misalignment.

### 4. Region Suggestion

Suggest left eye, right eye, left eyebrow, right eyebrow, mouth, brow-region skin, nose wrinkle, cheek deformation, and jaw/lower-face regions. Suggestions are editable starting points, not accepted production masks.

### 5. Manual Correction

The author can edit and feather masks, adjust overlaps, reposition anchors, classify regions, reject extraction, mark a full-expression fallback, mark a source unusable, and compare every decision against the neutral face.

### 6. Normalization

Where required, color-match local skin, normalize local brightness, reduce patch seams, preserve makeup and identity continuity, and define bounded local warp or jaw behavior. Normalization must remain local and reviewable; it is not unrestricted generative repainting.

### 7. Semantic Labeling

Labels are meaningful and editable, such as `eye.neutral`, `eye.half_lidded`, `eye.wide`, `eye.narrowed`, `brow.worried_inner_up`, `brow.stern_down`, `mouth.closed_neutral`, `mouth.pursed`, `mouth.slight_open`, `mouth.wide_open`, `mouth.clenched_teeth`, `overlay.glabella_compression`, `overlay.forehead_raised`, and `overlay.nose_wrinkle`. Source image numbers must not become permanent semantics by inference.

### 8. Recombination Preview

Preview extracted components on the neutral head. Test original-expression reconstruction, novel combinations, left/right asymmetry, canonical hair/headwear overlay, neutral restoration, compatibility feedback, serialization, and reload.

### 9. Acceptance and Export

Classify each component or preset as accepted, provisional, fallback-only, incompatible with stated groups, rejected, or requiring manual refinement. Export only accepted/provisional results and their evidence into the character-specific face-rig package; do not discard rejected-source provenance.

## Expression Maker Behavior and Controls

Expression Maker must first make mechanical truth inspectable: select a component; show its semantic identity, mask, anchors, safe bounds, compatibility, source, and quality status; apply predictable bounded edits; link or unlink paired controls; preview the resolved composition; explain fallback; save a structured preset; and restore neutral state exactly.

The conceptual control surface supports independent:

- left and right eye state;
- left and right eyelid openness;
- left and right gaze where safe;
- left and right eyebrow state, height, and rotation;
- bounded per-component transforms;
- mouth state;
- jaw/lower-face deformation;
- compatible detail overlays.

Ordinary editing may link paired eyes or eyebrows. Expressive editing may unlink them. Permanent coupling is forbidden because it removes one raised eyebrow, one narrowed eye, side-eye, crooked suspicion, sarcasm, disgust, uneven fear, and skeptical annoyance from the possibility space.

Intensity may be discrete, continuous, or preset-specific; that decision remains open. Unsupported interpolation must not be invented between component assets.

## Compatibility and Constraint Data

Not every primitive must combine with every other primitive. Compatibility is first-class data rather than a visual failure discovered after export. Dimensions may include:

- character and head presentation;
- face-rig schema and asset version;
- eye-, brow-, mouth-, and face-mask family;
- lighting, skin, makeup, and rendering-style profile;
- required deformation channels or detail overlays;
- hair/headwear occlusion;
- left/right pairing and anatomical dependencies;
- supported transform and intensity range;
- source confidence and known seam risk.

Compatibility groups may declare required dependencies, exclusions, warnings, confidence, author review status, and fallback resolution. Invalid edits preserve the last valid state or remain visibly unresolved; they must not silently corrupt identity. Warnings must distinguish a supported-but-risky composition from a forbidden one.

## Hair, Headwear, and Accessory Separation

Hair remains outside facial-expression state wherever practical. Face Intake defines a safe face plate, masks away hair/background/neck as appropriate, and lets canonical hair or headwear render above it. It does not need to reconstruct a perfect bald scalp beneath every source image.

Bangs, loose strands, caps, headbands, hats, glasses, earrings, and accessory-owned piercings normally remain separate layers with explicit ownership and occlusion. Permanent marks or identity-owned piercings may belong to the base face, but the choice must be explicit. Hair is baked into a saved expression only when a declared fallback requires it.

## Character Presets and Semantic Recipes

A **character expression preset** resolves one character's artwork and geometry, such as Carrie's worried eye assets, inner-brow assets, slightly open mouth, forehead crease, and local jaw value.

A **semantic expression recipe** describes abstract intent, such as inner brows raised, outer brows slightly lowered, eyes moderately widened, mouth slightly open, and optional forehead crease. A character maps that recipe through its own anchors, proportions, assets, compatibility rules, limits, and fallbacks.

Raw component asset IDs are not cross-character semantics. Shared recipe resolution is a design direction that requires evidence across multiple characters, complexions, angles, styles, and occlusion patterns before it can be promoted beyond **DESIGNED**.

## Why Pixel Subtraction Is Only an Aid

Independently rendered or generated source images may vary in head position/scale, jaw and cheek shape, eye size, iris position, skin texture, makeup, lighting, ears, neck, hair strands, silhouette, or identity proportions. Naive subtraction therefore highlights many pixels unrelated to the intended expression.

Extraction must use landmarks, semantic regions, bounded alignment, guided masks, manual review, and recombination tests. Pixel differences may suggest regions but cannot be the sole definition of a component.

## Non-Destructive Asset Lifecycle

Keep the following conceptually separate and traceable:

- original source and authoritative/alternate neutral images;
- landmark data and alignment transform;
- original suggestion mask and corrected mask;
- normalized component and preview render;
- semantic label and compatibility data;
- accepted preset and full-face fallback;
- source-quality notes, decisions, and rejection reasons.

Derived assets should be reproducible from preserved source data where practical. Editing an expression never overwrites permanent neutral identity. Versioning and provenance must make it possible to replace a mask or normalized component, reevaluate dependent presets, and retain the original requested semantics.

## Poser, Placer, and Export Interoperability

### Expression Maker to Poser

Character Creator exports a face-rig reference plus selected character preset or semantic recipe resolution. Poser preserves head presentation, component references/semantic choices, transforms, linking, gaze, deformation, overlays, compatibility/fallback state, and necessary version references with the pose. Poser may expose safe adjustments but does not own source normalization.

### Poser to Placer

The transfer envelope's CharacterSnapshot carries expression references and resolved state with character root, pose, render, constraint, and relationship state. Placer adds presentation around that snapshot. Moving, scaling, depth-sorting, framing, or tinting a character must not flatten or reconstruct its internal expression.

### Final Export

Editable project state retains structure. A final raster export may flatten the rendered face with hair, headwear, body, lighting, and panel effects. Export does not redefine the stored preset as a bitmap and must not leak editor masks, handles, bounds, warnings, or provenance diagnostics.

## Prior Batch 1 Asset-Review Context

No reviewed Batch 1 face assets are present in this repository as of this design pass. The following is bounded prior external review context, not a repository inventory and not independent verification:

- 12 character face sets: Abby, Ang, Bij, Carrie, Ex, Heath, Kath, Maya, Popstar, Suz, Syd, and Zor;
- 108 generated expression images, nine per character;
- 15 base/reference images and 123 PNG files total;
- bald/closely shaved, hair-bearing, and headwear-bearing sets;
- predominantly black backgrounds and no expression-image transparency;
- varied reference preparation quality;
- mostly similar regular-head orientations with some alignment drift.

The reviewed batch appeared strongest in concern, worry, fear, surprise, alarm, suspicion, anger, disgust, defensive reactions, pursed-mouth skepticism, and teeth-bared tension. It appeared weaker in relaxed neutral, small/full smiles, laughter, contentment, sadness without fear, crying, boredom, deadpan, sleepy/half-lidded or closed eyes, blinking, deliberate gaze, one-eyebrow skepticism, subtle smirks, conversational/phoneme mouths, and ordinary social reactions.

These are provisional asset-library coverage findings, not evidence of a software defect or a working face system. The architecture must permit missing categories to be added without redesigning the rig.

## Recommended Prototype and Validation Sequence

This sequence is **DESIGNED** guidance and has not been executed:

1. **Carrie — primary authoring case:** clean scalp, useful neutral references, strong differentiation, and comparatively stable face. Assign any piercing or identity mark explicit ownership.
2. **Zor — cross-character validation:** clean scalp, stable angle, and useful identity continuity for detecting overfitting to one complexion or lighting profile.
3. **Bij — hair-bearing validation:** strong expressions and bangs that exercise face-plate clipping and canonical hair occlusion.
4. **Heath — alignment stress test:** larger head-angle/framing variation for deciding when to reject, manually correct, or retain a full-expression fallback.

Other sets may later become regression cases. Suz remains provisional unless an authoritative neutral reference is available.

Functional validation follows project priority:

1. Select a component.
2. Manipulate it predictably.
3. Link and unlink left/right controls.
4. Combine components without corrupting identity.
5. Constrain or explain invalid combinations.
6. Save and restore the expression exactly.
7. Transfer it to Poser and preserve it in Placer.
8. Preserve structured state through serialization and final export.
9. Only then refine visual polish and automation.

## Decisive Novel-Recombination Experiment

Reconstructing a source expression is necessary but insufficient. The decisive experiment is:

> Can components from different source expressions produce a convincing expression that never existed as a source image?

Candidate combinations include surprised eyes + worried brows + flat mouth; narrowed eyes + one raised eyebrow + slight smirk; neutral eyes + angry brows + closed mouth; asymmetric eyes + pursed mouth + no wrinkle overlay; and worried brows + neutral mouth + side gaze.

Evaluate identity preservation, seam visibility, alignment, anatomical readability, compatibility behavior, hair occlusion, neutral restoration, save/load fidelity, and transfer through Poser and Placer. A convincing novel expression with preserved structured state is stronger evidence of combinatorial value than a successful reconstruction alone.

## Reality-State Classification

- **SPECULATIVE:** Fully automatic segmentation; universal one-click extraction; continuous morphing among arbitrary sources; generative reconstruction of hidden forehead regions; reliable universal cross-character recipe transfer; fully procedural independent pupils, eyelids, lips, teeth, and tongue; and automatic compatibility scoring without review.
- **DESIGNED:** Character Creator ownership; Expression Maker as a sub-mode; guided Face Intake; the shared semantic/character-specific split; components, bounded deformation, presets, compatibility, fallbacks, provenance, and Poser/Placer interoperability described here.
- **IMPLEMENTED:** This repository contains this design artifact and pre-existing body-rig/Poser source described elsewhere. It contains no Expression Maker, Face Intake, facial component library, character face-rig package, or expression runtime.
- **TESTED:** Documentation structure and repository checks may be tested by the pass that introduced this document. No facial authoring, recombination, save/load, or transfer behavior has been tested.
- **VALIDATED:** Nothing in the intended Expression Maker or Face Intake creative workflow.

Prior Batch 1 observations remain narrowly described as external asset-review context. They do not promote the designed system to IMPLEMENTED, TESTED, or VALIDATED.

## Open Design Questions

- Should the first eye implementation use bounded eye complexes or independent pupils?
- Which components require surrounding skin, and how should feathered overlap be represented?
- How much local warp is safe before identity drifts?
- Should intensity be discrete, continuous, or preset-specific?
- How do makeup variants interact with component libraries?
- Which identity details belong to the base face versus accessories?
- How are compatibility groups authored, inspected, and explained?
- When should a source be rejected rather than heavily normalized?
- How do full-expression fallbacks participate in preset selection and later reevaluation?
- Which semantic recipes merit cross-character mappings?
- How does gaze interact with eye-complex artwork?
- How should future head presentations extend the schema?
- Which facial states constitute a minimally useful real panel workflow?

These questions require evidence-driven prototype passes. This document intentionally does not settle them.

## Non-Goals

This design pass does not implement or select:

- Expression Maker, Face Intake, runtime controls, or user interfaces;
- a concrete schema, serialization syntax, programming language, framework, or storage system;
- face detection, segmentation, image generation, or a particular computer-vision model;
- production masks, landmarks, component assets, normalized faces, approved expressions, or binary archives;
- unrestricted deformation, universal cross-character component reuse, or automatic visual approval;
- additional required head presentations beyond regular/back;
- Poser reconstruction behavior, Placer rendering behavior, or final artwork policy.

The smallest high-value next step is a separately authorized manual vertical-slice experiment using one well-prepared character: preserve source/neutral data, normalize a few eye/brow/mouth/detail components, reconstruct one source expression, create one novel recombination, restore neutral, and record seams, identity drift, compatibility needs, and fallback decisions. Implementation architecture should be chosen only after that evidence exists.
