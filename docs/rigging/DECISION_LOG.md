# Rig Program Decision and Conflict Log

Decisions below are **DESIGNED** unless source evidence says otherwise. Specialist findings remain preserved in the pass report; this log records Director synthesis rather than erasing alternatives.

## Resolved conflicts

| ID / question | Roles and evidence | Options and implications | Director decision / cost / status |
| --- | --- | --- | --- |
| RIG-001 — Rename current segments? | Schema/Anatomy noted clearer torso_lower/lower_leg names; current app/tests use mid_torso, chest, calf_L/R. | A rename improves vocabulary but breaks/migrates tested IDs; retention avoids churn but needs semantic roles. | Retain current v0.1 segment IDs; add roles torso_lower/lower_leg; separate JointIds through explicit mapping. Future rename requires major migration. Low short cost, some terminology debt. DECIDED. |
| RIG-002 — Rig coordinate convention? | Kinematics proposed Cartesian Y-up/CCW; current assets/runtime are X-right/Y-down/clockwise. | Y-up is math-familiar but needs pervasive adapters; current convention preserves source with no loss if explicit. | Use X-right, Y-down, positive clockwise in canonical rig space; external engines adapt at boundary. Low migration cost. DECIDED. |
| RIG-003 — Hinge storage? | Current elbows use normalized 0…1; other controls use transitional degrees. Cross-review favors profile-independent normalization. | Degrees are readable but can entangle visual ranges; normalized flexion preserves current elbows and common pose semantics. | Elbows/knees store normalized flexion 0…1 mapping to mechanical 0°…180°; other signed/cyclic joints store degrees. Legacy Back values may be ambiguous. DECIDED. |
| RIG-004 — Root transform ownership? | Task requires root preservation; current reusable pose excludes character state. | Put root in pose and reduce reuse, or omit it and lose interactions. | ReusablePose excludes root; TransferEnvelope CharacterSnapshot includes characterRootTransform; PlacerPanel adds panel placement. DECIDED. |
| RIG-005 — 360° shoulders/hips versus narrow artwork? | Mechanical intent is cyclic; current visual evidence is roughly shoulders ±65°, hips ±38°. | Silent clamp falsely removes mechanics; full display without warnings produces broken art. | Schema exposes cyclic mechanics. Authoring defaults to supported bands and requires explicit opt-in/warnings or ghosts outside them until orientation/corrective art exists. DECIDED. |
| RIG-006 — Regional granularity? | Orientation, Garment, and Integrator found no sub-limb seam evidence. | Per-segment orientations maximize theoretical mixing but create unsupported seams; branch atomicity constrains v0.1 safely. | torso, pelvis, arm_L/R, leg_L/R, head; arms/legs atomic in v0.1. Conditional bridges require authored contracts. DECIDED. |
| RIG-007 — Neck/head hierarchy? | Existing neck_socket only; task requires initial head interface without full head system. | Require neck/head artwork now, or defer all head semantics. | neck_socket required junction; neck optional mechanical helper; head required semantic module slot with regular/back presentations; artwork deferred. DECIDED. |
| RIG-008 — Numeric depth or semantic graph? | Current numeric defaults/overrides exist; Layering found they cannot preserve garment/prop relations. | Promote numbers and retain hidden ordering assumptions, or migrate to semantic partial order. | Semantic RenderRelations are canonical; numeric values become defaults/tie/migration metadata only. Cycles preserve last valid plan and block export/transfer. DECIDED. |
| RIG-009 — Reuse baseline masks as runtime coverage? | Baseline has 45 alpha masks; current adapter drops them; audit says construction/reference, not garment semantics. | Automatic reuse is quick but conflates coordinate/operation intent; explicit import is safer. | No automatic promotion. Every runtime MaskRule declares owner space, operation, target, variant, and fallback. DECIDED. |
| RIG-010 — Garment state ownership? | Requirements mention future clothing in pose; Garment/Serialization distinguish equipment and pose overlays. | Put all state in pose and couple identity, or omit pose-dependent states. | GarmentState owns equipped instances/state; reusable pose may carry optional overlay; RenderState owns manual semantic overrides. DECIDED. |
| RIG-011 — Fallback replay? | Serialization cross-review identified frozen versus reevaluate tension. | Always reevaluate may change published output; always freeze blocks recovered assets in drafts. | Editable drafts default reevaluate; explicit transfer/publish defaults frozen. Requested semantics always persist. DECIDED. |
| RIG-012 — Invalid render/orientation behavior? | Orientation requires atomic rejection; render graph may cycle after manual edges. | Arbitrary repair risks corruption. | Invalid orientation never commits. Render cycle retains last valid plan, diagnoses cycle, and blocks clean export/transfer. Authoring ghost is never exported. DECIDED. |

### Resolved conflict impact and cost register

| ID | Affected systems | Short-term cost | Long-term cost / benefit |
| --- | --- | --- | --- |
| RIG-001 | Schema, source adapter, pose migration, garments | Maintain aliases and role mapping | Some terminology debt; avoids breaking tested identities |
| RIG-002 | Transforms, assets, engines, direct manipulation | Document engine adapters | Preserves current assets/runtime without limiting semantics |
| RIG-003 | Pose, kinematics, migration, UI | Map normalized hinges to degrees | Profile-independent reusable hinge poses |
| RIG-004 | Pose, interactions, transfer, Placer | Maintain three document layers | Prevents placement/presentation coupling |
| RIG-005 | Kinematics, artwork, orientation, authoring | Warnings/ghosts and supported-band UI | Preserves full mechanics without false visual claims |
| RIG-006 | Orientation, artwork seams, garments | Fewer v0.1 mixing combinations | Safe extension point for future explicit sub-limb bridges |
| RIG-007 | Hierarchy, head modules, anchors | Support a slot without current artwork | Heads can arrive without body-schema replacement |
| RIG-008 | Rendering, migration, serialization | Build relation compiler and migration | Deterministic garments/props/contextual ordering |
| RIG-009 | Artwork, garments, masks, rendering | Author/import typed mask rules | Avoids destructive or coordinate-ambiguous coverage |
| RIG-010 | Appearance, pose presets, serialization | Maintain separate GarmentState/overlays | Equipment can combine with multiple poses |
| RIG-011 | Assets, drafts, published transfer | Track requested/effective variants and mode | Reproducible publish plus recoverable editable drafts |
| RIG-012 | Orientation, render graph, authoring, export | Last-valid plan and diagnostics | Invalid state cannot silently corrupt output |

## Unresolved decisions

### RIG-U01 — Approved male/female anatomy and profile values

- **Affected systems:** Profiles, artwork, garment fit, pivots, visual limits.
- **Roles/evidence:** Anatomy and Repository roles found no male body, head scale, anthropometric/stylization target, straight-back source, or owner approval.
- **Option A:** Derive values from provisional female art and invent male deltas. Fast, but hard-codes unsupported anatomy.
- **Option B:** Keep the grammar and require annotated turnarounds/profile evidence. Slower, preserves replaceability.
- **Combinatorial/technical cost:** A narrows future body diversity and garment reuse; B delays production art but not mechanical design.
- **Decision/status:** UNRESOLVED; Option B is the required safe posture. Does not block the next orientation prototype; blocks profile/art approval.

### RIG-U02 — Visual quality of regional bridge seams

- **Affected systems:** Orientation, local transforms, masks, correctives, garments, 360 presentation.
- **Roles/evidence:** Integrator found matching pivots but no mixed-region transition assets/tests.
- **Option A:** Assume pivot compatibility proves visual seams. Low short cost, high failure risk.
- **Option B:** Prototype waist plus one shoulder/hip transition with diagnostics and unchanged art.
- **Combinatorial/technical cost:** B adds a bounded proof but removes the largest integration uncertainty.
- **Decision/status:** UNRESOLVED evidence question; choose Option B as the next pass. Blocks production regional mixing.

### RIG-U03 — Immutable definition reference policy

- **Affected systems:** Transfer reproducibility and asset upgrades.
- **Roles/evidence:** Serialization recommends ID/version and optionally content hash; repository has no package registry contract.
- **Option A:** ID/version only. Simpler, weaker reproducibility.
- **Option B:** ID/version plus immutable hash. Stronger, needs asset/package policy.
- **Combinatorial/technical cost:** A is easy but can make the same transfer resolve differently; B improves reproducibility but requires content-addressed asset policy.
- **Decision/status:** UNRESOLVED; preserve extension field and decide before production transfer. Does not block next prototype.

### RIG-U04 — Legacy non-elbow Back-pose migration

- **Affected systems:** Pose 0.1 migration and semantic correctness.
- **Roles/evidence:** Current non-elbows store raw visual degrees; Back semantics are unapproved.
- **Option A:** Preserve appearance and label ambiguity. Option B: reject those values and neutralize only through explicit user repair.
- **Combinatorial/technical cost:** A preserves more visible poses with uncertain semantics; B is safer but loses unattended migration coverage.
- **Decision/status:** UNRESOLVED; migrator must emit LEGACY_SEMANTIC_AMBIGUITY and never claim lossless semantics. Blocks automated migration claim, not the next prototype.

## Authoritative complete conflict records

The earlier tables are a readable index. The records below are authoritative and contain every mandatory field.

### RIG-001 — Segment naming
- **Question:** Rename existing mid_torso/chest/calf segment IDs?
- **Agents:** Schema Architect, Anatomy Specialist, Integrator, Director.
- **Affected systems:** Rig schema, source adapter, pose migration, garments.
- **Evidence:** Current app/tests use those IDs; specialists proposed clearer torso/lower-leg terms.
- **Option A:** Rename now to torso_lower/torso_upper/lower_leg.
- **Option B:** Preserve IDs and add semantic region roles/legacy aliases.
- **Combinatorial implications:** A clarifies future profiles but breaks current combinations; B keeps all current poses/art usable.
- **Technical implications:** A requires immediate migration; B requires role mapping.
- **Short-term cost:** A high; B low.
- **Long-term cost:** A low vocabulary debt; B modest alias debt.
- **Director decision:** Option B for v0.1; a rename requires a later major version.
- **Status:** DECIDED.

### RIG-002 — Coordinate convention
- **Question:** Use Cartesian Y-up/CCW or current canvas Y-down/clockwise rig space?
- **Agents:** Kinematics Engineer, Schema Architect, Integrator, Director.
- **Affected systems:** Transforms, assets, engines, manipulation.
- **Evidence:** All current pivots/art/code use X-right/Y-down and positive clockwise rendering.
- **Option A:** Canonical Y-up/CCW with adapters around current source.
- **Option B:** Canonical X-right/Y-down/clockwise with adapters for external engines.
- **Combinatorial implications:** Both support the same poses if explicit.
- **Technical implications:** A migrates every current coordinate; B preserves current data.
- **Short-term cost:** A high; B low.
- **Long-term cost:** A math familiarity; B requires documented engine adapters.
- **Director decision:** Option B.
- **Status:** DECIDED.

### RIG-003 — Hinge representation
- **Question:** Store elbow/knee flexion in degrees or normalized semantic values?
- **Agents:** Kinematics Engineer, Schema Architect, Serialization Engineer, Director.
- **Affected systems:** Pose, mappings, profiles, migration, UI.
- **Evidence:** Current elbows already use normalized 0…1; other controls are transitional degrees.
- **Option A:** Store all hinges as degrees.
- **Option B:** Store elbow/knee 0…1 mapped to 0°…180° mechanics.
- **Combinatorial implications:** B lets profiles/art share poses despite different visual envelopes.
- **Technical implications:** A migrates elbows; B adds mapping for knees/UI display.
- **Short-term cost:** A medium; B low/medium.
- **Long-term cost:** A profile coupling risk; B stable semantic reuse.
- **Director decision:** Option B; signed/cyclic non-hinges remain degrees.
- **Status:** DECIDED.

### RIG-004 — Root transform ownership
- **Question:** Where is character root placement preserved?
- **Agents:** Serialization Engineer, Schema Architect, Integrator, Director.
- **Affected systems:** Reusable poses, interactions, transfer, Placer.
- **Evidence:** Current pose excludes character state; task requires transfer to preserve root.
- **Option A:** Put root in every reusable pose.
- **Option B:** Keep pose articulation-only; place root in CharacterSnapshot; add Placer panel transform separately.
- **Combinatorial implications:** B lets one pose combine with many world/panel placements while preserving interactions.
- **Technical implications:** B requires three document layers.
- **Short-term cost:** A low but couples state; B medium.
- **Long-term cost:** A reuse loss; B durable responsibility separation.
- **Director decision:** Option B.
- **Status:** DECIDED.

### RIG-005 — Full-cycle mechanics versus limited art
- **Question:** Clamp shoulders/hips to current art or preserve 360° mechanics?
- **Agents:** Kinematics, Orientation, Anatomy, QA, Director.
- **Affected systems:** Mechanics, authoring, artwork, orientation, correctives.
- **Evidence:** Intent is cyclic; current visual support is about shoulder ±65° and hip ±38°.
- **Option A:** Clamp mechanics to current images.
- **Option B:** Preserve cyclic semantics; default UI to supported bands and require warnings/ghosts outside.
- **Combinatorial implications:** A permanently removes poses; B preserves future orientation/corrective combinations.
- **Technical implications:** B needs separate mechanical/presentation statuses.
- **Short-term cost:** A low; B medium.
- **Long-term cost:** A high architecture restriction; B enables artwork growth.
- **Director decision:** Option B.
- **Status:** DECIDED.

### RIG-006 — Regional granularity
- **Question:** Can each limb segment orient independently in v0.1?
- **Agents:** Orientation, Garment, Layering, Integrator, Director.
- **Affected systems:** Regional pose, seams, garments, masks, serialization.
- **Evidence:** No sub-limb bridge artwork or seam evidence exists.
- **Option A:** Per-segment orientations immediately.
- **Option B:** Atomic arm/leg branches with torso/pelvis/head regions.
- **Combinatorial implications:** A offers more theoretical mixes but many invalid seams; B provides safe declared combinations.
- **Technical implications:** A multiplies transition contracts; B keeps a clear extension point.
- **Short-term cost:** A high; B low.
- **Long-term cost:** A fragile; B needs a later explicit sub-limb bridge version.
- **Director decision:** Option B.
- **Status:** DECIDED.

### RIG-007 — Neck and head status
- **Question:** Require neck/head artwork, or defer all head structure?
- **Agents:** Schema, Anatomy, Orientation, Director.
- **Affected systems:** Hierarchy, head modules, anchors, orientation.
- **Evidence:** Only neck_socket exists; task requires regular/back head presentations.
- **Option A:** Require implemented neck/head body parts now.
- **Option B:** Require neck_socket and semantic head slot; make neck helper optional and art deferred.
- **Combinatorial implications:** B lets future heads combine without rebuilding bodies.
- **Technical implications:** B supports an empty required module interface.
- **Short-term cost:** A blocks architecture; B low.
- **Long-term cost:** A art coupling; B stable extension.
- **Director decision:** Option B.
- **Status:** DECIDED.

### RIG-008 — Render ordering model
- **Question:** Promote numeric depth or use semantic partial-order relations?
- **Agents:** Layering, Garment, Serialization, Integrator, Director.
- **Affected systems:** Rendering, garments, props, migration, serialization.
- **Evidence:** Current numeric depth exists but cannot express contextual relationships.
- **Option A:** Canonical numeric global sort.
- **Option B:** Canonical semantic relation graph; retain numbers as defaults/migration metadata.
- **Combinatorial implications:** B supports limbs, garments, props, and correctives in changing contexts.
- **Technical implications:** B needs deterministic topological sort/cycle handling.
- **Short-term cost:** A low; B medium/high.
- **Long-term cost:** A severe layering ceiling; B extensible.
- **Director decision:** Option B.
- **Status:** DECIDED.

### RIG-009 — Baseline mask promotion
- **Question:** Treat inherited alpha masks as runtime garment/coverage masks?
- **Agents:** Repository Analyst, Layering Engineer, Garment Architect, Director.
- **Affected systems:** Artwork, masks, coverage, garments.
- **Evidence:** Baseline masks are construction artifacts and current adapter drops them.
- **Option A:** Reuse automatically.
- **Option B:** Require explicit MaskRule import with owner space/operation/target.
- **Combinatorial implications:** B allows correct reuse across art/profile changes.
- **Technical implications:** A is coordinate-ambiguous; B adds typed metadata.
- **Short-term cost:** A low; B medium.
- **Long-term cost:** A hidden failures; B non-destructive predictable coverage.
- **Director decision:** Option B.
- **Status:** DECIDED.

### RIG-010 — Garment state ownership
- **Question:** Is garment identity/state part of joint pose?
- **Agents:** Garment, Serialization, Schema, Director.
- **Affected systems:** Appearance, pose presets, render state, transfer.
- **Evidence:** Requirements mention future clothing pose state; cross-review separates equipment identity from optional pose overlays.
- **Option A:** Put all garment truth inside pose joints/document.
- **Option B:** GarmentState owns equipment/state; pose may carry optional overlay; RenderState owns semantic overrides.
- **Combinatorial implications:** B lets garments combine with many poses and poses apply without forcing equipment.
- **Technical implications:** B requires reference/overlay validation.
- **Short-term cost:** A low; B medium.
- **Long-term cost:** A tight coupling; B modular reuse.
- **Director decision:** Option B.
- **Status:** DECIDED.

### RIG-011 — Fallback replay
- **Question:** Reevaluate or freeze effective visual fallbacks across load/transfer?
- **Agents:** Serialization, Garment, Layering, Director.
- **Affected systems:** Drafts, assets, published transfer, reproducibility.
- **Evidence:** Missing assets may later appear; published panels must not change unexpectedly.
- **Option A:** One global reevaluate or freeze policy.
- **Option B:** Drafts default reevaluate; explicit transfer/publish defaults frozen; requested state always retained.
- **Combinatorial implications:** B restores compatible assets in drafts while preserving published combinations.
- **Technical implications:** Track requested/effective variant, reason, and mode.
- **Short-term cost:** A low; B medium.
- **Long-term cost:** A either stale drafts or unstable publish; B predictable.
- **Director decision:** Option B.
- **Status:** DECIDED.

### RIG-012 — Invalid graph behavior
- **Question:** How do invalid orientation edits and render cycles behave?
- **Agents:** Orientation, Layering, QA, Director.
- **Affected systems:** Authoring, rendering, export, transfer.
- **Evidence:** Silent repair would corrupt state; graph cycles may arise from manual relations.
- **Option A:** Arbitrarily repair/sort.
- **Option B:** Reject orientation atomically; preserve last valid render plan on cycle; diagnose and block clean export/transfer.
- **Combinatorial implications:** B makes invalid combinations explicit without destroying the last valid composition.
- **Technical implications:** Requires transactional edits and cycle-path reporting.
- **Short-term cost:** A low; B medium.
- **Long-term cost:** A nondeterminism; B trustworthy state.
- **Director decision:** Option B; diagnostic ghosts are authoring-only.
- **Status:** DECIDED.

### RIG-U01 — Initial profile values
- **Question:** How are male/female anatomy and proportions approved?
- **Agents:** Repository Analyst, Anatomy, Garment, Director.
- **Affected systems:** Profiles, art, pivots, garment fit, visual limits.
- **Evidence:** No male body, approved female, head scale, target, or owner validation exists.
- **Option A:** Derive/invent values from provisional art.
- **Option B:** Require annotated references/turnarounds and owner review.
- **Combinatorial implications:** A narrows diversity/fit; B preserves future profiles.
- **Technical implications:** A hard-codes unsupported values; B delays content, not grammar.
- **Short-term cost:** A low; B high evidence effort.
- **Long-term cost:** A high rework; B sound reusable profiles.
- **Director decision:** No final value selected; safe posture is B.
- **Status:** UNRESOLVED; blocks production profile/art, not next prototype.

### RIG-U02 — Regional bridge seam quality
- **Question:** Can current turnaround art support mixed-region seams?
- **Agents:** Integrator, Orientation, Layering, Garment, Director.
- **Affected systems:** Local transforms, transitions, masks, correctives, garments.
- **Evidence:** Pivots match semantically; no mixed-region transition has been tested.
- **Option A:** Assume pivot alignment proves visuals.
- **Option B:** Prototype waist plus one shoulder/hip bridge and record corrective needs.
- **Combinatorial implications:** A risks false support; B proves a reusable transition boundary.
- **Technical implications:** B may reveal offset/mask/depth/corrective requirements.
- **Short-term cost:** A low; B bounded medium.
- **Long-term cost:** A high rework; B reduces largest uncertainty.
- **Director decision:** Evidence remains unresolved; next pass selects B.
- **Status:** UNRESOLVED; blocks production regional mixing.

### RIG-U03 — Immutable definition references
- **Question:** Reference definitions by ID/version only or include content hash?
- **Agents:** Serialization Engineer, Integrator, Director.
- **Affected systems:** Transfer reproducibility, asset upgrades, package policy.
- **Evidence:** No registry/content-address policy exists.
- **Option A:** ID/version only.
- **Option B:** ID/version plus immutable hash.
- **Combinatorial implications:** A eases replacement but may change resolution; B freezes exact combinations.
- **Technical implications:** B requires hashing/package rules.
- **Short-term cost:** A low; B medium.
- **Long-term cost:** A reproducibility risk; B policy/ storage complexity.
- **Director decision:** Preserve extension field; decide before production transfer.
- **Status:** UNRESOLVED; does not block orientation prototype.

### RIG-U04 — Legacy Back-pose migration
- **Question:** How are non-elbow Back raw degrees migrated?
- **Agents:** Kinematics, Serialization, Integrator, Director.
- **Affected systems:** Pose migration, semantic correctness, user repair.
- **Evidence:** Legacy values encode visual signs with unapproved Back semantics.
- **Option A:** Preserve visible appearance and label ambiguity.
- **Option B:** Reject/neutralize only through explicit user repair.
- **Combinatorial implications:** A retains more historical poses; B prevents uncertain semantics from propagating.
- **Technical implications:** Both require document-type checks; A needs ambiguity metadata.
- **Short-term cost:** A medium; B low implementation but user repair cost.
- **Long-term cost:** A semantic debt; B lost unattended migration coverage.
- **Director decision:** No lossless claim; always emit LEGACY_SEMANTIC_AMBIGUITY pending migration prototype.
- **Status:** UNRESOLVED; blocks automated lossless-migration claim.

## Task 000 reconciliation decisions — later evidence

These decisions were added after the external Task 000 PXZ evidence arrived. They preserve rather than rewrite the earlier conflict chronology.

### RIG-013 — Architecture family after illustrative-reference review

- **Question:** Retain the current designed architecture unchanged, shift to asset-heavy pose variants, adopt general deformation, or amend it with a hybrid illustrative-resolution layer?
- **Roles:** Director, Schema, Anatomy, Kinematics, Orientation, Layering/Illustrative Resolution, Integrator, QA.
- **Affected systems:** Rig/profile/art boundaries, torso/pelvis, sockets, masks, depth, correctives, endpoints, garments, serialization, QA.
- **Evidence:** Current source/tests establish a sound mechanical slice; the PXZ establishes a dynamic-pose quality target assembled from pre-posed fragments/masks/overlap and zero manifest rotations, not a rig.
- **Options:** A current design unchanged; B semantic mechanics plus localized correctives/masks/depth/optional bounded deformation; C primarily pre-authored regional/pose states; D general deformation-heavy system.
- **Combinatorial implications:** B preserves reusable semantic poses while allowing localized presentation combinations; C risks asset multiplication; D risks opaque complexity; A lacks an explicit anatomy-to-illustration boundary.
- **Director decision:** Choose B as the DESIGNED direction and retain A's semantic/state/versioning foundation. C remains a supporting mechanism; D remains optional and evidence-gated.
- **Status:** DECIDED / DESIGNED, not implemented or validated.

### RIG-014 — Torso/pelvis responsibility

- **Question:** Treat torso expressiveness as raw segment rotation, add many free spine controls, or use a small semantic body-mass vocabulary with derived mechanics/presentation?
- **Roles:** Anatomy, Kinematics, Schema, Illustrative Resolution, QA, Director.
- **Affected systems:** Pose semantics, existing pelvis/mid_torso/chest nodes, waist connection, orientation, correctives, garments.
- **Evidence:** The PXZ target depends strongly on ribcage/pelvis opposition, waist curve, arch/compression, and pelvis shift; exact reusable controls are unproven.
- **Options:** Raw rotations; dense free controls; compact semantic bend/twist/arch-crunch/tilt-shift-tuck candidates.
- **Combinatorial implications:** Compact semantics can drive many profiles/presentations; raw rotations underdescribe intent; dense controls increase tuning burden.
- **Director decision:** Retain existing node identities and prototype a compact semantic layer. Exact fields/limits remain experimental until Task 001 evidence.
- **Status:** DIRECTION DECIDED; exact vocabulary OPEN.

### RIG-015 — Manual tuning and provenance

- **Question:** May generated/derived rig and presentation values overwrite canonical values, or must owner corrections remain typed and reversible?
- **Roles:** Schema, Serialization, Integrator, QA, Director, owner requirement.
- **Affected systems:** Pivots, ranges, offsets, orientations, connection zones, masks, depth, correctives, deformation, anchors, versioning.
- **Evidence:** The owner explicitly requires fine-tuning; current designed contracts lack one shared proposed/derived/authored/approved boundary.
- **Options:** Destructive baking; opaque final effective value; typed override/provenance chain.
- **Combinatorial implications:** Typed overrides allow regeneration, comparison, art replacement, and profile reuse without discarding owner decisions.
- **Director decision:** Require generated proposal → derived result → author override → owner-approved canonical value, with disable/recompute and compatibility metadata.
- **Status:** DECIDED / DESIGNED.

### RIG-016 — Acceptance and artistic authority

- **Question:** Can mechanically valid or automated visual results be accepted as artistically resolved by the team?
- **Roles:** Kinematics, Anatomy, Illustrative Resolution, QA, Director, owner.
- **Affected systems:** Orchestration, QA, reporting, prototype exit criteria.
- **Evidence:** Current automated tests establish mechanical boundaries only; repository rules reserve VALIDATED for intended workflow evidence.
- **Options:** One PASS; team consensus; separated Mechanical/Combinatorial/Expressive/Illustrative gates plus Owner Validation.
- **Combinatorial implications:** Separate gates expose where a primitive fails without falsely narrowing mechanics or hiding presentation debt.
- **Director decision:** Use separate gates and the Kinematics → Anatomy → Illustrative Resolution → QA chain. Owner Validation cannot be delegated or voted into existence.
- **Status:** DECIDED / DESIGNED.

### RIG-U05 — Minimum torso/pelvis illustrative vocabulary

- **Question:** Which body-mass semantics, connection-zone fields, and localized corrective bands are necessary and non-redundant?
- **Roles:** Anatomy, Kinematics, Illustrative Resolution, Schema, Integrator, QA, owner.
- **Affected systems:** Pose state, waist/pelvis mechanics, artwork metadata, overrides, garments.
- **Evidence:** The need is strong; the minimum vocabulary and interaction quality are unknown.
- **Smallest experiment:** Task 001 Torso–Pelvis Illustrative-Resolution Spike in one 3/4 presentation.
- **Status:** UNRESOLVED; highest-priority architecture uncertainty.

### RIG-U06 — Threshold for bounded deformation

- **Question:** When do localized correctives/masks stop being sufficient and bounded deformation earn its complexity?
- **Roles:** Illustrative Resolution, Anatomy, Integrator, QA, owner.
- **Affected systems:** Artwork authoring, renderer, replacement art, serialization, garment signals.
- **Evidence:** The PXZ proves masks/fragments matter but does not prove deformation. Current runtime has no deformation engine.
- **Smallest experiment:** Compare rigid and localized corrective/mask modes first; run one bounded deformation trial only if the same sweep exposes a specific unresolved contour problem.
- **Status:** UNRESOLVED; general deformation remains deferred.

## Semantic mapping preparation decisions

### RIG-017 — Bilateral and view projection sign convention

- **Question:** How should one semantic shoulder, hip, or knee value project across anatomical sides and whole-body views?
- **Roles:** Schema, Anatomy, Kinematics, Orientation, Serialization, Integrator, QA, Director.
- **Affected systems:** Joint definitions, direct manipulation, view switching, serialization, pose symmetry, future profiles and artwork sets.
- **Evidence:** The 2026-08-26 non-elbow verification shows identity mapping reverses anatomical direction between Front and Back. Stable `_L/_R` identifiers are anatomical, not screen-side. Mirrored bilateral motion requires opposite rendered handedness by side, while Back projection reverses Front handedness.
- **Option A:** Same rendered sign for both sides and all views.
- **Option B:** View-only sign reversal, identical across sides.
- **Option C:** `direction = sideSign × viewSign`, where L=`+1`, R=`-1`, Front/3/4=`+1`, and Back=`-1`; preserve IDs and canonical semantic values.
- **Combinatorial implications:** C lets equal bilateral semantic values form mirrored poses and lets the same pose combine with Front/3/4/Back without anatomical-side swaps. A and B make equal values asymmetric or conflate semantic and screen handedness.
- **Technical implications:** C requires data-driven per-view mappings, inverse conversion, bilateral tests, and a provisional 3/4 qualification. It does not authorize regional Front/Back transitions.
- **Short-term cost:** A low; B low; C medium.
- **Long-term cost:** A/B preserve semantic ambiguity; C creates a reusable projection rule for profiles and replacement artwork.
- **Director decision:** Option C as the **DESIGNED** mechanical projection convention. For cyclic shoulder/hip state, map the signed delta; for normalized knee flexion, map `180° × flexion`. Three-quarter sign is provisional pending anatomy/illustrative review.
- **Status:** DECIDED / DESIGNED; not implemented, tested, visually approved, or owner-validated.

### RIG-018 — Knee-proof persistence boundary

- **Question:** How can normalized knee semantics be saved without silently reinterpreting part-keyed raw degrees under pose 0.1 or falsely claiming the complete pose 0.2 contract?
- **Roles:** Schema, Kinematics, Orientation, Serialization, Integrator, QA, Director.
- **Affected systems:** Runtime pose state, Save Pose, future loading/migration, fixtures, JointId aliases, semantic provenance.
- **Evidence:** Current pose 0.1 stores `calf_L/R` as transitional raw degrees; the designed pose 0.2 contract includes broader regional and migration behavior that the knee proof will not implement.
- **Option A:** Reuse pose 0.1 and reinterpret `calf_*` as normalized values.
- **Option B:** Claim pose 0.2 for the partial proof.
- **Option C:** Emit a separately typed experimental document with stable elbow/knee JointIds and an explicitly named transitional raw-degree map for remaining parts.
- **Combinatorial implications:** C lets semantic hinges combine and round-trip into a future migrator without contaminating old meaning or forcing unrelated pose-0.2 scope.
- **Technical implications:** Save output changes type; aliases are explicit; loading/migration stays out of scope; future migration must discriminate exact document types.
- **Director decision:** Option C with schema `2d-doll-semantic-knee-proof-0.1` and mapping contract `bilateral-knee-semantic-0.1`.
- **Owner decision:** Approved exactly as proposed. Do not reuse pose 0.1 or claim the complete pose 0.2 contract.
- **Status:** OWNER APPROVED / DESIGNED; not implemented, tested, or workflow-validated.

### RIG-019 — Unsupported knee-presentation behavior

- **Question:** What should the authoring runtime do when a mechanically legal knee value exceeds inherited provisional artwork support or uses the unverified 3/4 projection?
- **Roles:** Anatomy, Kinematics, Orientation, Illustrative Resolution, Serialization, Integrator, QA, Director.
- **Affected systems:** Rendering, diagnostics, controls, evidence sweeps, future correctives, owner tuning.
- **Evidence:** Knee mechanics are designed for normalized `0…1` → `0°…180°`; inherited art supplies only an unapproved bend envelope near `98°`; silent clamping would collapse distinct semantic states and hide presentation failures.
- **Option A:** Clamp rendering to inherited limits.
- **Option B:** Replace unsupported states with a ghost only.
- **Option C:** Render the full mechanically mapped provisional rotation with a persistent structured warning; preserve requested semantics and separate support/projection status.
- **Combinatorial implications:** C exposes where new artwork/correctives are needed while keeping mechanics reusable across future profiles and presentation sets.
- **Technical implications:** Mapping returns separate mechanical and presentation results; values above `98/180` emit `PRESENTATION_RANGE_UNSUPPORTED`; 3/4 emits `PRESENTATION_MAPPING_UNVERIFIED`; neither warning mutates pose truth.
- **Director decision:** Option C for the experimental authoring proof. It is not export/presentation approval.
- **Owner decision:** Approved full-angle provisional rendering with persistent structured warnings. Unsupported presentation must remain observable in diagnostics/public state and the authoring interface.
- **Status:** OWNER APPROVED / DESIGNED; Anatomy, Illustrative, QA, and workflow VALIDATION remain open.

### RIG-020 — Bilateral-knee proof authorization boundary

- **Question:** What implementation scope does owner approval authorize after the freeze?
- **Roles:** Owner, Director, Kinematics, Orientation, Serialization, Integrator, QA.
- **Affected systems:** Next-pass scope, sequencing, evidence, persistence, 3/4 status, future shoulder/hip work.
- **Evidence:** Owner review approved the frozen knee abstraction, RIG-018, and RIG-019, while explicitly preserving pose 0.1, provisional 3/4 status, and the shoulder/hip deferral.
- **Authorized:** Bilateral knees only; tests first; generic mapping/model; direct manipulation/inversion; experimental serialization; Front/3/4/Back evidence; unsupported-range evidence; independent QA.
- **Not authorized:** Shoulder/hip expansion; pose 0.1 reinterpretation; full pose 0.2; promotion of 3/4 beyond provisional without evidence; anatomy/artwork/workflow validation claims.
- **Persistence condition:** Requested semantic state is authoritative. Mapping/artwork/support/view/issue provenance may explain the saved display context, but transient rendered degrees and effective pose copies are not authoritative pose fields.
- **Repository condition:** Close and publish the documentation dependency chain, or explicitly authorize an unpublished dependency chain, before implementation.
- **Owner decision:** Approve the bilateral-knee implementation proof within this boundary.
- **Status:** OWNER APPROVED / DESIGNED IMPLEMENTATION SCOPE; implementation and all test gates remain pending.
