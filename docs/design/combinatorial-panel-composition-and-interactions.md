# Combinatorial Panel Composition, Interactive Elements, and Effects Philosophy

## Purpose and Authority

This document is the canonical **DESIGNED** philosophy for modular panel composition, interactive scene elements, semantic object capabilities, relationship-based constraints, event-driven effects, and the boundary between Poser performance state and Placer presentation.

It extends the durable project purpose in [Project Context](../PROJECT_CONTEXT.md), the source-aligned Poser boundary in [Canonical Poser Rig Architecture](../RIG_ARCHITECTURE.md), and the narrower **DESIGNED** contracts for [interaction anchors](../rigging/architecture/INTERACTION_ANCHOR_MODEL.md) and [Poser-to-Placer transfer](../rigging/architecture/POSE_SERIALIZATION_CONTRACT.md). Those narrower documents remain authoritative within their scopes. This document does not establish a production schema or claim that Placer, general interaction authoring, scene graphs, environment kits, relationship objects, or event-driven effects exist in source.

The objective is combinatorial expressive power:

> A limited vocabulary of compatible characters, poses, objects, environments, effects, interactions, and presentation controls should produce a very large possibility space.

2D Doll is not intended to become a library of finished pictures, a background-image editor, a catalog of one-off two-character poses or special-scene assets, a flat stack of character cutouts, or a collection of effects permanently painted into characters and scenery. It is intended to become a modular **2D illustrated performance and panel-construction system**.

## Reality Status

Three kinds of truth must remain separate:

- **Design truth** states the intended responsibilities, behaviors, and constraints defined here.
- **Repository truth** states what current source and canonical evidence actually implement.
- **Validation truth** states what creators have demonstrated useful in the intended panel-making workflow.

At the time this document is introduced:

- **SPECULATIVE:** Concrete scene-graph representation, connector deformation and occlusion algorithms, constraint solvers, effect-selection rules, crowd representation, material systems, user interfaces, and production serialization details remain open.
- **DESIGNED:** The responsibility boundaries, semantic models, capability families, relationship principles, effect taxonomy, non-destructive requirements, fallbacks, and evaluation criteria in this document.
- **IMPLEMENTED:** This design artifact and the separately documented bounded Poser/body-rig source. Documentation is not product behavior.
- **TESTED:** Only checks explicitly recorded by pass reports. No panel-composition, general-interaction, environment, connector, or event-effect workflow is promoted to TESTED by this document.
- **VALIDATED:** Nothing described here has yet been demonstrated useful in the intended end-to-end creative workflow.

Throughout this document, “should,” “eventually,” and conceptual examples describe **DESIGNED** direction unless a linked source-aligned document explicitly establishes a stronger state.

## Core Principle: State to Presentation

The governing transformation is:

> **STATE → CONSTRAINTS → POSSIBILITIES → PRESENTATION**

This is a design lens, not a mandated processing pipeline or technology choice.

### State

State records what exists and its current condition:

- character identities, orientation, articulation, expressions, and clothing state;
- object and environmental state;
- active relationships, constraints, and events;
- camera, panel, depth, and presentation state.

State must preserve requested meaning separately from any visual fallback or derived presentation. An editable scene should retain its structured facts even when a final export is flattened.

### Constraints

Constraints describe the relationships and limits that give state meaning:

- joint ranges and parent-child transforms;
- semantic source and target anchors;
- attachment points and object capabilities;
- contact, distance, restraint-length, angle, and orientation requirements;
- surface support, collision or overlap guidance, and scene-depth rules;
- character-, profile-, artwork-, or environment-specific restrictions.

Constraints should explain incompatibility, permit deliberate overrides where safe, and preserve unresolved intent rather than silently replacing or deleting it.

### Possibilities

Compatible state and constraints make many outcomes possible, including holding, sitting, leaning, carrying, restraining, embracing, fighting, handing off, operating, riding, standing on, looking toward, reacting to impact, connecting two points, and staging multiple figures in one environment.

The value of a primitive is not the number of named features it creates. Its value is the number and quality of coherent combinations it unlocks with other primitives.

### Presentation

Presentation communicates the selected state and relationships in a finished panel through:

- camera framing, crop, aspect ratio, and focal emphasis;
- environment, semantic depth, layering, and overlap;
- foreground framing, lighting, tint, and atmosphere;
- impact, motion, contact, and other visual effects;
- dialogue, thought bubbles, captions, and sound-effect lettering;
- final resolution and export.

Presentation may derive suggestions from semantic state, but it must not redefine or destroy that state.

## Poser and Placer Responsibilities

These are conceptual responsibilities, not a requirement for rigidly isolated applications.

### Poser: Internal Performance State

Poser defines and preserves the performance itself:

- character articulation, whole-body position, facing, and orientation;
- expression and clothing state;
- held or attached props;
- one- or two-character posing;
- semantic interaction points;
- character-to-character and character-to-object relationships;
- reusable poses and reusable interactions.

A pose transferred from Poser should retain its internal relationships. Examples include a hand holding another character's wrist, two characters holding hands, one character carrying another, a hand gripping a sword, a character tethered to a chain, a figure leaning against a railing, or a figure kneeling in relation to another.

### Placer: Presentation for the Reader

Placer stages the performance within a panel:

- base environment, structural pieces, dressing, and foreground framing;
- scene-object placement, scale, semantic depth, layering, and overlap;
- panel aspect ratio, camera framing, focal point, and crop;
- lighting, tint, atmosphere, and visual effects;
- dialogue, thought bubbles, captions, and sound effects;
- final panel export.

Placer must not flatten, reconstruct, or discard the internal pose and relationship state imported from Poser merely to stage it. Placer may expose contextual pose or relationship adjustments where evidence supports them, but such edits must remain meaningful, reversible, and attributable.

The current transfer boundary is defined more narrowly in [Pose Serialization and Poser-to-Placer Transfer](../rigging/architecture/POSE_SERIALIZATION_CONTRACT.md). This document expands the design philosophy around that boundary without replacing its state-ownership decisions.

## Panel as an Ordered Semantic Scene

A panel is not adequately modeled as only background, characters, and foreground. It should be understood as an ordered semantic scene stack or scene graph whose members can occupy adjustable depth positions without permanent merging.

Possible members include:

1. base environment;
2. distant scenery;
3. structural architecture;
4. background crowd groups;
5. environmental dressing;
6. rear atmospheric effects;
7. primary and secondary characters;
8. interactive props and relationship objects;
9. contact effects;
10. foreground characters, architecture, and clutter;
11. lighting overlays;
12. comic presentation elements.

This order is illustrative rather than a fixed universal z-list. A useful scene model must distinguish:

- **semantic role:** what an element means or does;
- **visual depth:** where it appears in the depicted space;
- **interaction ownership:** which entity, event, or relationship it follows;
- **render order:** when or how its pieces are drawn;
- **editing ownership:** which responsibility or mode authors it.

These values are related but not identical. Smoke may belong to a torch while rendering in front of a character. A chain may connect a wrist to a wall while crossing several depth layers. A foreground pillar may cover a character without interacting with that character. A magical beam may connect two characters while rendering partly behind one and partly in front of another.

Semantic depth should therefore not be confused with a single permanent numeric draw order. Exact graph, masking, splitting, or compositing mechanisms remain **SPECULATIVE**.

## Interaction-First Element Model

The primary organizing question for an interactive element is:

> What can a character do with this element?

Appearance, genre, historical period, material, and asset family remain valuable secondary metadata and search filters. They must not be the sole source of behavior.

A chair, throne, bench, crate, bed edge, rock, and vehicle seat may share `sit-on`, `stand-on`, `lean-on`, or `brace-against` capabilities. A sword, torch, microphone, bottle, staff, lantern, handbag, or tool may share `hold`, `carry`, `present`, `point`, `pass-to`, or `attach-to-hand` capabilities.

One object may expose several capabilities. It should not be duplicated merely because it participates in several interactions. Behavior, geometry or artwork, visual style, material, color treatment, and scene lighting should remain separable where practical.

For example, a wall can remain leanable, attachable, obstructing, and capable of foreground or background placement while its appearance varies among stone, brick, wood, metal, painted plaster, or futuristic paneling. This separation is a design direction, not a promise of a procedural material system.

## Semantic Anchors

Semantic anchors are a foundational combinatorial primitive. An anchor expresses meaningful intent, not merely an arbitrary point on a canvas.

### Character Anchors

Possible character anchors include hand, palm, grip, wrist, elbow, shoulder, head, face, eye line, chest, waist, hip, back, knee, ankle, foot, carry support, embrace point, contact target, and look-at origin.

### Object and Environment Anchors

Possible object or environment anchors include prop grip, secondary grip, seat, backrest, hand rest, foot support, stand-on, lean-on, wall attachment, restraint attachment, door handle, ladder rung, steering grip, platform edge, contact target, effect origin, and effect destination.

An interaction relationship should be able to describe:

- source entity and source anchor;
- target entity and target anchor;
- relative orientation and offset;
- permitted movement and alignment behavior;
- distance and optional angle constraints;
- optional pose assistance;
- strength or rigidity;
- persistence, break, or release state;
- fallback behavior when an anchor is unavailable.

Relationships and relative transforms are preferred over absolute canvas coordinates. Stable local anchor identity allows artwork, camera, panel crop, and participant position to change without erasing the intended connection.

The body-rig-specific anchor distinctions and current implementation boundary are governed by the [Interaction Anchor Model](../rigging/architecture/INTERACTION_ANCHOR_MODEL.md). This broader philosophy adds object, environment, restraint, and effect use cases without declaring final anchor IDs or fields.

## Relationship Graph

A scene should be understood as entities connected by semantic relationships, not only as a hierarchy of pictures. Conceptually supported relationship domains include:

- Character ↔ Character;
- Character ↔ Prop, Furniture, Environment, Constraint, or Hazard;
- Prop ↔ Prop and Object ↔ Environment;
- Effect ↔ Character, Prop, Environment, or Event;
- Anchor ↔ Anchor.

Example relationships include hand to wrist, hand to waist, hand to shoulder, grip to sword handle, wrist to shackle, shackle to chain, chain to wall anchor, foot to platform, hip to seat, back to backrest, hand to railing, face look-at to face target, beam origin to target chest, torch flame to torch head, smoke to flame, and impact burst to contact point.

Complex scenes should emerge from several simple compatible relationships. The whole outcome should not be hard-coded when it can be assembled from reusable entities, anchors, capabilities, and constraints.

## Object Capability Families

These are conceptual capability families, not required class names or proof of implementation.

### Holdable

- one-hand and two-hand grip;
- alternate grip locations and orientations;
- dominant-hand or off-hand use;
- point, raise, lower, carry, present, and pass to another character.

### Wearable or Body-Attached

- head, neck, shoulder, waist, wrist, ankle, and back attachment;
- explicit ownership by a clothing, accessory, body, or interaction layer.

### Support Surface

- sit-on, stand-on, kneel-on, lie-on, brace-against, lean-on, and step-on.

### Operable

- open, close, pull, push, turn, press, steer, climb, enter, and exit.

### Rideable or Carrying Structure

- seated, standing, mounting, support-grip, passenger, driver, and carried-object anchors.

### Restraining or Binding

- wrist, ankle, collar, waist, and multi-point restraint;
- character-to-character and character-to-environment restraint;
- release, unlock, broken, slack, and tension state.

### Connective

- rope, chain, cable, leash, beam, magical tether, energy stream, hose, wire, and flexible weapon during contact.

### Hazard or Contact Source

- strike, cut, pierce, burn, shock, crush, trip, entangle, push, and pull.

### Environment Interaction

- doorway, ledge, ladder, railing, wall, window, platform, throne, table, stair, and control surface.

Capabilities may be combined. A torch may be holdable, attachable to a wall, operable as a light source, and the owner of attached flame and smoke effects. A vehicle may be rideable, operable, supportive, and capable of carrying props or passengers.

## Relationship Objects and Constraints

Some elements exist primarily to connect two or more anchors. Examples include rope, chain, cable, leash, handcuffs, tether, flexible hose, beam, magical stream, lightning arc, a whip during contact, and linked restraints.

A relationship object should conceptually preserve:

- source, target, and optional intermediate anchors;
- minimum and maximum length;
- slack, tension, curve, thickness, and orientation;
- attachment style and rigidity;
- depth and occlusion behavior;
- break, release, lock, or continuity state.

When either endpoint moves, the relationship object should remain logically connected. A chain must not require unrelated `wrist chain`, `ankle chain`, `wall chain`, `prisoner chain`, and `throne chain` assets. Prefer a reusable chain behavior combined with endpoints, attachment rules, length, slack, orientation, state, and a visual variant.

Convincing presentation may require several pieces of artwork, masks, or split render segments. That does not justify fragmenting the behavior model into one-off scene assets.

## Reusable Interaction Recipes

Reusable interactions are parameterized relationship recipes, not screenshots or flattened poses. Examples include holding hands, wrist grab, arm hold, embrace, carry, supporting an injured character, sitting together, kneeling before, standing behind, restraining to a wall or platform, exchanging an object, pulling another character, leaning against furniture, riding together, attacking and blocking, and pointing a prop toward a target.

A recipe may describe:

- required semantic anchors and compatible capabilities;
- preferred orientation, facing, and look-at relationships;
- relative placement and allowed offsets;
- optional pose assistance;
- fallbacks and validation warnings.

The recipe must not permanently fuse participants. The user should retain control of character identity, scale, orientation, articulation, expression, clothing, props, offsets, camera, and effect style.

## Action, Contact, Reaction, and Presentation

Event meaning and visual treatment must remain separable:

> **ACTION → CONTACT → REACTION → PRESENTATION**

### Action

What an actor attempts: strike, push, pull, throw, grab, restrain, release, carry, block, cast, fire, whip, cut, or punch.

### Contact

Where and how the action meets a target: source, source tool, target, target anchor or region, direction, angle, force or intensity, contact type and duration, glancing or direct contact, and blocked, missed, or successful state.

### Reaction

How the target responds: recoil, stumble, bend, turn, fall, brace, block, flinch, expression change, clothing or hair movement, secondary-object movement, no reaction, or a manually posed reaction.

### Presentation

How the event is communicated: motion arc, speed line, impact burst, flash, spark, slash trail, smoke, dust, debris, glow, sound-effect lettering, camera emphasis, temporary lighting, or panel treatment.

These stages must be independently editable. A creator should eventually be able to use an action without automatic effects, use a contact effect without automatic reaction posing, pose a reaction manually, replace one presentation style with another, suppress unwanted assistance, and preserve the event relationship while changing its treatment.

## Event-Driven Effect Selection

The system should not require a single baked asset such as `character_hit_by_whip`. It should conceptually describe an event through action type, source entity and object, source anchor, target entity and region, direction, intensity, contact result, reaction state, and presentation profile. Compatible presentation components can then be suggested or selected without becoming mandatory outcomes.

### Whip Impact Family

Compatible vocabulary may include a long curved path, flexible trailing line, narrow contact point, snap effect, directional recoil, a secondary curve following the weapon, and snap-appropriate lettering.

### Sword Impact Family

Compatible vocabulary may include a straighter blade arc, edge trail, directional slash line, sparks for metal contact, larger directional emphasis, and block or deflection treatment.

### Punch Impact Family

Compatible vocabulary may include a short path, compact burst, localized compression, body recoil, dust or sweat accents, and blunt-impact lettering.

### Magical Impact Family

Compatible vocabulary may include glow, particles, beams, tendrils, aura, temporary scene lighting, target illumination, and environmental response.

These are compatible presentation families derived from event meaning, not required visual outcomes. A spark, motion line, glow, or lettering component should remain reusable across many event profiles when its semantics and style are compatible.

The following non-binding example illustrates event meaning without establishing a repository schema:

```yaml
event:
  action: strike
  source_entity: character_a
  source_object: sword_01
  target_entity: character_b
  target_region: upper_torso
  direction: left_to_right
  intensity: medium
  result: contact
  reaction: manually_adjustable
  presentation_profile: sword_impact
```

## Visual Effects Taxonomy

Effects should be organized by behavior and relationship as well as appearance.

### Persistent Effects

Rain, fog, smoke, fire, aura, environmental glow, underwater bubbles, dust-filled atmosphere, continuing magical fields, or eye glow that remains active through part or all of a panel.

### Momentary Effects

Impact, slash, muzzle flash, whip snap, explosion, spark, shock wave, burst, falling debris, and contact flash.

### Attached Effects

Flame attached to a torch, smoke attached to a barrel, glow attached to eyes, magic attached to a hand, dust attached to feet, splash attached to a contact point, aura attached to a body, or light attached to a lantern.

### Relationship Effects

Beam, lightning arc, magical tether, energy transfer, whip path, connected smoke stream, targeting line, and force-field boundary.

### Environmental Effects

Rain field, fog layer, drifting smoke, firelight, snow, sand, water disturbance, atmospheric particles, and room-wide magical corruption.

### Lighting Effects

Local light, warm or cool tint, rim light, silhouette, eye-glow spill, firelight state, magical illumination, darkness mask, and focus spotlight.

### Comic Presentation Effects

Speed lines, impact bursts, action lines, sound-effect text, caption boxes, emphasis frames, panel overlays, and focus vignette.

Depending on type, an effect may expose position, scale, rotation, opacity, intensity, depth, blend behavior, mask, attachment target, source and target anchors, direction, persistence, and visual variant. This list defines design dimensions; it does not require every parameter in a first implementation.

## Modular Environment Construction

A location should not normally be reduced to one permanently flattened image. An environment can be decomposed into reusable layers and pieces.

### Base Environment

The broad location identity, such as dungeon, street, market, ship, temple, jungle, throne room, library, bedroom, rooftop, or alley.

### Structural Pieces

Walls, floors, arches, doorways, windows, pillars, stairs, platforms, railings, masts, beams, and throne structures establish space.

### Environmental Dressing

Furniture, stalls, signs, crates, shelves, fabrics, vegetation, barrels, tools, lamps, debris, and other smaller pieces specify use, period, culture, and story.

### Atmosphere and Lighting

Fog, rain, dust, smoke, firelight, window light, environmental tint, and other area effects establish condition and mood without being permanently painted into every structure.

The same dungeon kit can support confrontation, escape, imprisonment, ritual, conversation, or exploration by recombining structure, dressing, characters, relationships, camera, and effects. It should not require a separate flattened dungeon image for every event.

## Environment Interaction Points

Environmental elements should eventually expose semantic anchors just as characters do:

- a chair or throne may expose seat, back support, hand rests, foot placement, lean-back, and stand-near;
- a platform may expose stand-on, kneel-on, sit-on, edge, and restraint anchors;
- a railing may expose hand grip, lean-on, stand-near, look-over, and brace-against;
- a door may expose handle, push side, pull side, threshold, stand-in-doorway, and lean-in-doorway;
- a bed may expose sit-edge, lie-center, head and foot positions, lean, and kneel-beside;
- a ladder may expose hand and foot rungs, climb path, and top and bottom transitions.

The interaction describes a relationship between character and environment. It must not permanently bake one completed pose into the environmental asset.

## Camera, Panel, and Composition State

The panel is structured state, not merely a fixed canvas. Conceptual panel state may include:

- aspect ratio, width, height, and export resolution;
- camera position, scale or zoom, crop, focal point, and horizon or eye level;
- composition guides, safe area, and dialogue-safe negative space;
- semantic depth, foreground framing, atmosphere, and lighting treatment.

Camera and framing should be first-class and reversible. Different aspect ratios create genuinely different compositions: a vertical pulp tableau is not simply a landscape scene cropped vertically. A wide confrontation, tight portrait, throne composition, crowded market, and multi-character action panel each require different staging logic.

Panel presentation may reorganize visual emphasis while preserving the imported performance and relationship state.

## Primary Characters and Crowd Elements

Fully articulated primary characters and lower-cost crowd elements serve different purposes.

### Primary Characters

Primary performers require identity, articulation, expression, clothing state, interaction anchors, relationships, editability, and pose preservation.

### Crowd Elements

Crowds may use precomposed clusters, simplified modular figures, limited pose variants, silhouette groups, depth-specific groups, directional attention, and density controls. They often provide environmental texture, scale, social pressure, or framing rather than individually authored performance.

Not every visible background person must be a complete Doll character. A crowd element should be promotable to a primary character when narrative needs change, but that possibility does not require full articulation from the start.

## Reversibility, Compatibility, and Fallbacks

Major composition and interaction operations should be reversible and non-destructive where practical. Preserve separately:

- source assets;
- pose, interaction, object, and effect state;
- camera and panel state;
- derived presentation;
- final rendered output.

A final export may be flattened. The editable scene should retain its internal structure.

Not every character, prop, or artwork set will support every interaction perfectly. Graceful fallbacks may include using a generic grip, warning that an anchor is missing, preserving a relationship for manual alignment, disabling optional pose assistance, using a simplified straight connector, allowing an explicit override, marking partial compatibility, or retaining data the current artwork cannot display fully.

Replacing an asset must not silently destroy relationships. Mechanical rig truth and semantic relationship data should survive artwork replacement wherever practical. Requested state, effective fallback, reason, and author override should remain distinguishable.

## Conceptual Relationship Examples

The examples below are explanatory and non-binding. They are not established repository schemas.

```yaml
relationship:
  type: hold
  source:
    entity: character_a
    anchor: right_hand_grip
  target:
    entity: sword_01
    anchor: primary_grip
  orientation: aligned
  offset: adjustable
  pose_assistance: optional
```

```yaml
connector:
  type: chain
  source_anchor: character_b.left_wrist
  target_anchor: wall_anchor_02
  slack: medium
  tension: low
  depth_behavior: adjustable
  release_state: locked
```

Any future implementation may use a different representation if it preserves the behavior, ownership, interoperability, reversibility, and fallback requirements defined here.

## Example Scene Decompositions

These generic examples demonstrate decomposition, not mandatory templates or reconstruction of any specific illustration.

### Torch-Lit Dungeon Confrontation

Combine a stone chamber base, rear arch, wall columns, foreground cauldron, primary hero, kneeling secondary character, doorway antagonist, sword attached through a grip relationship, wall-attached torches, flame and smoke attached to those torches, warm local light, cool ambient darkness, an optional action or magical relationship effect, a camera crop, and dialogue-safe space.

### Market Procession

Combine a street base, façade modules, market-stall dressing, crowd clusters, an animal or cart background element, scaffold or platform, two primary walking characters, arm-hold interaction, restraint connector, atmospheric dust, foreground spectator, and wide framing.

### Ship Deck Scene

Combine ocean and sky, ship hull and deck structure, mast and rigging modules, railing anchors, three primary characters, standing and leaning relationships, held sword, rope connectors, water splash, wind-influenced hair or clothing state, and a wide panel.

### Throne-Room Restraint Scene

Combine a throne, seated character, secondary character near the throne, character-to-environment restraint, chain connector, columns, stairs, fire bowls, lighting treatment, vertical framing, caption box, and foreground floor treatment.

Each example remains editable because the scene is a composition of reusable entities, capabilities, relationships, and presentation state rather than one finished asset.

## Anti-Patterns

Avoid:

- creating a special feature for each finished illustration;
- making every chain configuration a different asset;
- painting effects permanently into characters or scenery;
- flattening pose relationships before transfer to Placer;
- classifying objects only by appearance;
- using absolute coordinates when semantic relationships are available;
- requiring full articulation for every crowd figure;
- treating foreground and background as only two fixed layers;
- coupling event meaning directly to one visual style;
- building whip, sword, punch, and magic contact as unrelated systems;
- treating a chair and throne as behaviorally unrelated only because their artwork differs;
- duplicating a prop for every supported interaction;
- exposing arbitrary transforms when a semantic control would be clearer;
- allowing visual polish to conceal broken selection, manipulation, compatibility, or state preservation;
- describing **DESIGNED** behavior as **IMPLEMENTED**.

## Combinatorial Evaluation Questions

For every proposed object, effect, interaction, or environment feature, ask:

1. What new combinations become possible because this exists?
2. Is it a reusable primitive or a finished outcome?
3. Can the behavior work with several visual variants?
4. Can several object categories share the capability?
5. Is the relationship semantic or only absolute placement?
6. Can it connect to existing anchors?
7. Can it survive artwork replacement?
8. Can it be edited non-destructively?
9. Can it participate in more than one responsibility or mode?
10. Does it preserve Poser-to-Placer transfer?
11. Does it reduce repeated manual work?
12. Is a proposed special case actually a general rule?
13. Could a smaller primitive produce the same expressive range?
14. What happens when compatibility is incomplete?
15. How are missing anchors or invalid relationships explained?
16. Does an effect describe an event or only one baked depiction?
17. Can action, contact, reaction, and presentation change independently?
18. Does the proposal improve expressive range, control, reliability, or workflow efficiency?

Also ask what existing possibilities the proposal might restrict. A primitive that works for one current asset but prevents artwork replacement, cross-character reuse, depth adjustment, or manual override is not a sound combinatorial foundation.

## Open Design Questions

- What minimum anchor vocabulary should all characters support?
- Which anchors are universal, optional, or character-specific?
- How should semantic depth differ from literal render order?
- How should a connector cross in front of and behind several entities?
- Which interactions belong in Poser, and which belong in Placer?
- When and how should Placer permit contextual pose editing?
- How should object-capability compatibility be authored and validated?
- How much automatic pose assistance is desirable?
- How should manual edits override assistance without losing requested intent?
- How should crowd elements be represented and promoted?
- How should effect profiles vary by visual style?
- What is the minimum useful event model?
- Which environmental elements need anchors in the first useful version?
- What exact state must survive Poser-to-Placer transfer?
- How should constraints behave when a character is rescaled?
- How should incompatible artwork fail gracefully?
- What is the smallest scene experiment that can test relationship-object depth and occlusion?
- Which capabilities are required before a real panel-making workflow can be considered **VALIDATED**?

These questions require evidence or explicit owner decisions. This document does not resolve them prematurely.

## Implementation Neutrality and Non-Goals

This philosophy does not require a specific rendering engine, UI framework, physics library, file format, database, serialization package, vector format, or sprite system. Conceptual examples clarify relationships but do not establish field names or production schemas.

This documentation pass does not implement application behavior, create or extract assets, modify rigs, select dependencies, alter tests, redesign the interface, or prove any described workflow. Future implementation passes must establish source truth and tests within a separately authorized scope.

## Relationship to Existing Canonical Documents

- [Project Context](../PROJECT_CONTEXT.md) defines the durable project purpose, combinatorial lens, conceptual Character Creator/Poser/Placer responsibilities, and reality-state discipline.
- [Rig Requirements](../RIG_REQUIREMENTS.md) defines current canonical body and articulation requirements.
- [Canonical Poser Rig Architecture](../RIG_ARCHITECTURE.md) records the source-aligned boundary of the first canonical Poser runtime slice.
- [Body Rig Program](../rigging/README.md) indexes broader **DESIGNED** body-rig contracts.
- [Interaction Anchor Model](../rigging/architecture/INTERACTION_ANCHOR_MODEL.md) defines typed body-rig anchor and relationship contracts within its narrower scope.
- [Pose Serialization and Poser-to-Placer Transfer](../rigging/architecture/POSE_SERIALIZATION_CONTRACT.md) defines current designed state ownership across reusable poses, transfer snapshots, and panels.
- [Expression Maker and Face Intake](expression-maker-face-intake.md) defines the combinatorial facial subsystem and its transfer requirements.
- [Pass Reports](../pass-reports/README.md) are the chronological evidence ledger and must be consulted for actual implementation and testing claims.
- [Repository Instructions](../../AGENTS.md) govern reality-state language, documentation responsibility, and pass reporting.

If a future source-aligned contract conflicts with a speculative mechanism suggested here, preserve the behavioral principle, record the decision, and update current canonical documentation without rewriting historical evidence.
