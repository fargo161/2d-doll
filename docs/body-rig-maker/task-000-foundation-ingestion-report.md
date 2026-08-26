# Task 000 — Foundation Ingestion and Body-Rig Architecture Report

## 1. Task identification

- **Task:** Task 000 — Body Rig Maker reconciliation and foundation architecture analysis
- **Repository:** `fargo161/2d-doll`, local checkout
- **Branch:** `main`
- **Starting SHA:** `67c41a501e1f49066a13f70d0ad24f3d34cec33b`
- **Worktree at start:** `main` ahead of `origin/main` by three commits; pre-existing uncommitted pass-report ledger changes and three untracked pass reports were preserved
- **Report author:** Codex, preserving the repository's role-separated Body Rig Maker review model
- **Date:** 2026-08-26
- **Result:** **PASS WITH OPEN DECISIONS**

This was a documentation, architecture, and evidence-reconciliation pass. No body-rig feature was implemented.

## 2. Executive finding

The current `2d-doll-rig-0.2` architecture survives **partially**. Its strongest ideas remain the correct foundation: stable semantic identity, separation of rig/profile/art/pose/render/interaction/panel state, joint-family semantics, Front ↔ 3/4 ↔ Back compatibility, replaceable artwork, typed anchors, semantic render relationships, atomic validation, and versioned transfer. Those ideas should be retained.

It does not survive unchanged because it defines mechanics and downstream contracts more completely than it defines the bridge from a mechanically valid pose to a convincing illustration. The new PXZ evidence makes that missing boundary consequential. A rigid hierarchy plus region switching and numeric depth cannot by itself supply ribcage/pelvis opposition, shoulder and hip continuity, compression/stretch, foreshortening, endpoint readability, or controlled silhouette repair.

The recommended direction is:

> **DESIGNED RECOMMENDATION:** Preserve semantic mechanical pose as canonical truth, add a small semantic body-mass vocabulary and typed connection zones, and resolve difficult poses through optional view-aware corrective art, masks, semantic depth relations, endpoint variants, and only bounded deformation where an experiment proves it earns its complexity. Keep every automatic result inspectable and non-destructively overrideable by the owner.

This is Candidate B, the hybrid semantic mechanical rig plus illustrative-resolution layer. It offers more expressive combinations than rigid sprites, avoids the asset explosion of complete pose variants, and does not prematurely commit the project to a general mesh engine.

The largest uncertainty is not whether semantic joints or regional compatibility are useful. It is whether a **small, reusable** torso/pelvis and major-socket vocabulary can resolve expressive body-mass relationships without growing into one-off pose art. The recommended Task 001 is therefore a bounded **Torso–Pelvis Illustrative-Resolution Spike**, not the previously selected Orientation Compatibility Prototype.

## 3. Evidence reviewed

### Package evidence

The Task 000 package was reviewed as inert evidence. Packaged executable/script content was not run.

- `README.md`
- `TASK_000_EXECUTION_PROMPT.md`
- `SOURCE_AUTHORITY_AND_REALITY_LABELS.md`
- `REPORT_TEMPLATE.md`
- `context/PROJECT_BIBLE.md`
- `context/OWNER_BODY_RIG_DECISIONS.md`
- `context/FIRST_CANONICAL_POSER_ARCHITECTURE_SLICE.md`
- `context/FOUNDATION_SYNTHESIS.md`
- `context/RELEVANT_CHAT_TRANSCRIPT.md`
- `evidence/bodyref.pxz`, through its complete supplied extract and manifest
- `evidence/PXZ_INSPECTION_REPORT.md`
- `evidence/bodyref_pxz_extract/manifest.json`
- `evidence/derived/PXZ_LAYER_INVENTORY.csv` and JSON summary
- reconstructed render, silhouette, contact-sheet, mask, and visible-bounds diagnostics
- `evidence/derived/render_validation.json`
- package manifest and checksum listing

The derived visual evidence was inspected directly. The packaged Python utility was not executed and its reconstruction metrics were not regenerated.

### Repository evidence

- Root and rigging-scoped `AGENTS.md`
- `README.md`, `docs/PROJECT_CONTEXT.md`, `docs/RIG_REQUIREMENTS.md`, and `docs/RIG_ARCHITECTURE.md`
- `app/rig-definition.js`, `app/model.js`, `app/runtime.js`, and `app/index.html`
- `tests/model.test.mjs`, `tests/verify_inherited_rig.py`, `tests/verify_canonical_runtime.py`, and `tests/runtime-browser-tests.js`
- the immutable inherited baseline manifest, structural records, and recorded verification boundary
- all files under `docs/rigging/`, including the 11 role charters, orchestration protocol, decision log, architecture contracts, QA matrix, repository/reference audit, and previous next-pass recommendation
- prior pass reports for the canonical Poser slice and body-rig architecture

### Commands and runtime checks

- `git status --short --branch`, `git log`, and `git rev-parse HEAD`
- targeted `rg` source/document searches and file inventory
- `npm test`: 6/6 model tests, 7/7 inherited verification tests, and 4/4 canonical runtime structure/provenance checks passed
- real-browser runtime matrix: 11/11 scenarios passed, 0 failed

### Evidence limitations

- The PXZ's supplied reconstruction was visually inspected but not regenerated in this pass.
- The PXZ has no bones, joints, semantic region names, pose controls, or clean neutral-to-posed correspondence.
- Current artwork is provisional engineering material and cannot establish production anatomy or visual style.
- No approved male profile, approved female profile, head system, garments, regional transition art, foreshortening set, or owner workflow validation exists.
- Automated tests establish bounded mechanical behavior, not illustrative quality.

## 4. Current repository reality

### SPECULATIVE

- Final profile anatomy, proportions, silhouettes, and production artwork.
- The exact form and asset count of corrective presentation.
- Whether limited mesh/lattice deformation is worth its complexity.
- Foreshortening representation and endpoint art families.
- Final torso/pelvis UI and control vocabulary.

### DESIGNED

- The broader `2d-doll-rig-0.2` schema and multi-profile/body-art separation.
- Regional Front/3/4/Back compatibility, typed garments, semantic render relations, interaction anchors, full transfer, and exhaustive QA.
- After this pass: the hybrid mechanical-plus-illustrative-resolution direction, typed connection zones, semantic body-mass controls, non-destructive author overrides, and provenance boundary.

### IMPLEMENTED

- `app/` adapts the immutable inherited manifest into a `2d-doll-rig-0.1` runtime definition.
- The runtime has 15 articulated part records and 17 stable pivot/attachment IDs across three whole-body anchor views.
- `state.pose`, `state.character`, `state.camera`, and `state.editor` are separate. Rig definition is separate loaded input.
- Recursive parent-local transforms, character/world transform, camera transform, inverse direct manipulation, selection handles, complete-body fitting, scoped resets, whole-body view switching, and save-only `2d-doll-pose-0.1` serialization exist.
- Elbows use normalized semantic flexion with view-specific mappings. Other joints remain transitional degree values with identity mappings.
- `pose.depthOverrides` exists, is serialized/reset, and is consumed by current numeric part ordering; no authoring UI exposes it.

### TESTED

Within the exact rerun boundaries:

- affine inversion and representative hierarchy behavior;
- semantic elbow mapping and 3/4 bridge data;
- full-body fitting in three views;
- separated character/camera/pose mutations;
- root, joint, and neck-attachment handles;
- representative direct manipulation and UI synchronization;
- branch propagation/isolation;
- scoped resets;
- save-only pose boundary;
- inherited baseline integrity and structural checks;
- canonical runtime source/provenance structure.

### VALIDATED

Nothing in the intended creative workflow. The owner has not yet used and approved the system as an effective body-rig authoring workflow.

### Broken, missing, or provisional

- Region-level orientation state and transition validation are absent.
- Only elbows have non-transitional cross-view semantics.
- Pose loading/migration, author overrides, provenance, corrective presentation, deformation, pose-responsive masks, semantic depth graph, foreshortening, endpoints, garments, interactions, and production export are absent.
- Current rigid engineering art visibly limits supported ranges and is not approved production art.

### Reconciliation of the prior Poser report

**OBSERVED:** `context/FIRST_CANONICAL_POSER_ARCHITECTURE_SLICE.md` still matches current local source and rerun tests in its declared boundary. No newer runtime implementation changes its central claims. The report correctly distinguishes semantic elbows from transitional joints, whole-body view switching from regional mixing, numeric depth state from a depth UI, and automated tests from owner validation.

One clarification is important: `pose.depthOverrides` is more than a placeholder field—it is currently read by the numeric ordering logic when populated—but it has no editor control, semantic relationship model, or user-tested workflow. It remains a narrow implemented state/render hook, not the designed pose-responsive depth system.

## 5. Owner requirements ledger

| Requirement | Source | Architecture consequence | Current status |
| --- | --- | --- | --- |
| Reusable mechanically coherent body, not a flat picture | `OWNER_BODY_RIG_DECISIONS.md` §1 | Semantic structure remains canonical | Mechanical slice IMPLEMENTED/TESTED; full body rig missing |
| Manual fine-tuning | same | Author overrides and provenance are required, not optional polish | DESIGNED in this pass |
| Mechanical truth separable from final art | same; repository rules | Profiles/artwork/correctives cannot redefine identity | Narrow separation IMPLEMENTED; broader contract DESIGNED |
| Front, 3/4, Back anchors | same §2 | Stable orientation IDs | Whole-body IMPLEMENTED/TESTED |
| 3/4 bridge; no direct Front/Back regional mix | same | Compatibility graph and atomic validation | Data boundary IMPLEMENTED; regional system DESIGNED |
| Regular/back head families only | same §3 | Head interface remains bounded | DESIGNED; no head runtime |
| Broad shoulders/hips, approximately 180° limb hinges | same §4 | Joint-family semantics and separate visual support | DESIGNED; elbows provide narrow precedent |
| Torso/pelvis most restricted but expressively rich | same | Use semantic body-mass controls, not arbitrary free rotation | DESIGNED in this pass |
| Dynamic illustrative nuance comparable to PXZ | same §5 | Add anatomical continuity and illustrative resolution | Requirement; not implemented/validated |
| Character Creator/Poser/Placer interoperability | same §6 | Keep construction, pose, and panel state separate | Narrow state boundary IMPLEMENTED; transfer DESIGNED |
| Garment readiness | same §7 | Stable bindings and deformation signals without garment ownership | DESIGNED |
| Interaction readiness | same §8 | Stable semantic anchors independent of panel coordinates | DESIGNED |
| Trapstar is non-canonical | same §9 | Cannot be recommended as production body art | REJECTED / NON-CANONICAL |

## 6. Mechanical, expressive, and illustrative capability gap

| Level | Current reality | Smallest missing capabilities |
| --- | --- | --- |
| Level 1 — Mechanical | A real bounded slice exists and is tested for representative operations | Full semantic joint families; typed JointIds rather than part-keyed transitional state; region state; load/migration; authorable constraint diagnostics |
| Level 2 — Expressive | Not established | Semantic ribcage/pelvis controls; shoulder/hip response; connection zones; pose sweeps; region bridge contracts; pose-responsive overlap/depth; endpoint direction |
| Level 3 — Illustrative | Not established | View-aware corrective/mask/overlap behavior; bounded deformation evidence; foreshortening; silhouette diagnostics; owner tuning; owner validation |

The smallest transition is not “add more joint rotation.” Level 1 → 2 requires body-mass and connection semantics. Level 2 → 3 requires presentation resolution that consumes those semantics while remaining replaceable and overrideable.

## 7. Reconciliation of the existing Body Rig Maker team

**DESIGNED DECISION:** Keep all 11 roles. No twelfth role is justified.

The existing role boundaries are structurally sound. Task 000 changes their emphasis:

- Layering, Masking, and Occlusion explicitly owns **Illustrative Resolution** evaluation: corrective art, seams, silhouette, bounded deformation, foreshortening, pose-responsive masks/depth, and mechanical-to-illustrative handoff.
- Anatomy and Proportion explicitly owns **Anatomy Under Pose**: line of action, weight-bearing asymmetry, shoulder/hip response, ribcage/pelvis opposition, compression/stretch, and extreme-pose continuity.
- Kinematics must hand mechanically valid output to Anatomy, then Illustrative Resolution, before QA.
- QA permanently separates Mechanical, Combinatorial, Expressive, Illustrative, and Owner Validation gates.
- All relevant roles must specify owner-adjustable values, reversibility, and provenance.
- The Director may decide engineering contracts but cannot convert artistic uncertainty into approval by consensus.

The team's earlier `2d-doll-rig-0.2` result becomes **Candidate A — retained foundation with Task 000 amendments**, not dogma.

## 8. PXZ evidence analysis

### Direct observations

- **OBSERVED:** The document is 1799 × 2448 pixels with 17 image layers, 9 visible flags, 8 visible intersecting layers, 8 hidden layers, 7 mask references, 1 locked layer, full opacity, and zero nonzero rotations.
- **OBSERVED:** The visible result uses large pre-posed source fragments, localized torso/hip fragments, legs/footwear, cropping, alpha, masks, and stack order.
- **OBSERVED:** Five masked visible layers contribute inside the canvas.
- **OBSERVED:** The result has a strong curved line of action, ribcage/pelvis opposition, pelvis shift, elevated/compressed shoulders, asymmetry, crossing masses, and directionally legible endpoints.
- **OBSERVED:** The manifest contains no bones, pivots, vectors, groups, semantic body-region names, constraints, or pose parameters.
- **OBSERVED:** One visible masked layer lies completely off-canvas, and hidden/duplicate source fragments remain. This is a working composite, not a normalized asset package.

### Interpretation boundary

- **SUPPORTED IMPLICATION:** Rigid sprite rotation alone is unlikely to resolve the target's waist curve, ribcage/pelvis mass opposition, shoulder/underarm compression, hip/thigh continuity, depth crossings, projected limb length/width, and endpoint orientation.
- **NOT PROVEN:** Which deformation technology is required; which body segmentation is canonical; whether a small corrective vocabulary is sufficient; how the target maps across Front/3/4/Back; or whether the current art can reach the target.

### Qualities likely addressable by reusable primitives

- ribcage bend/twist relative to pelvis;
- pelvis tilt/shift/tuck;
- connection zones and safe overlap envelopes;
- shoulder raised/compressed response bands;
- hip flexed/extended/cross-body response bands;
- waist stretched/neutral/compressed correctives;
- semantic before/after/coverage relationships;
- a small family of endpoint direction variants;
- bounded projected-length/width compensation;
- author overrides for offsets, masks, order, and corrective strength.

These primitives can combine across many poses. Complete target-pose fragments cannot.

## 9. Architecture Candidate A — current `2d-doll-rig-0.2`

### Strengths

- Strong identity, hierarchy, profile, artwork, state, versioning, validation, and migration separations.
- Joint families already distinguish cyclic shoulders/hips, normalized hinges, limited wrists/ankles, and restricted torso relations.
- Region compatibility encodes 3/4 as a bridge without enumerating whole-body combinations.
- Typed anchors, semantic render relations, garment pieces, and transfer boundaries are combinatorially powerful.
- Fits the current source seams incrementally.

### Weaknesses after new evidence

- Treats `mid_torso`/`chest` as mechanical segments but does not define a clear semantic ribcage/pelvis/body-mass control model.
- Connection contracts focus on pivots/anchors more than socket, insertion, overlap, compression, and silhouette behavior.
- Correctives are mentioned but not governed by a minimal activation/override/provenance contract.
- Limb atomicity and torso/pelvis region boundaries were selected before the PXZ stress case; they remain reasonable first constraints but require experimental confirmation.
- Garment and transfer contracts are more mature than the unresolved illustrative-resolution core.

### Verdict

**PARTIALLY SURVIVES.** Retain its foundations. Amend it with semantic body-mass state, typed connection zones, illustrative-resolution metadata, manual override/provenance, and quality gates. Do not implement the entire current schema before the highest-risk visual primitives are tested.

## 10. Architecture Candidate B — hybrid semantic rig plus illustrative resolution

### Shape

- Canonical pose remains semantic mechanical truth.
- Primary articulated segments remain a small stable hierarchy.
- Ribcage/pelvis semantics coordinate constrained mechanics rather than exposing arbitrary free transforms.
- Connection zones describe socket/contact, child insertion, safe overlap, mask owner, default depth relationship, and corrective hooks.
- Presentation consumes pose/profile/orientation and selects rigid art, localized correctives, masks, semantic depth relations, endpoint variants, and optional bounded deformation.
- Automatic suggestions remain derived; author overrides remain explicit, reversible, and provenance-bearing.

### Evaluation

| Criterion | Assessment |
| --- | --- |
| Combinatorial range | High: small semantic and corrective vocabularies can recombine |
| Asset burden | Medium and controllable if correctives stay localized/semantic |
| One-off explosion risk | Medium; governed by refusing complete-pose assets as canonical mechanics |
| Manual editability | High with typed overrides and diagnostics |
| Three-view compatibility | Strong; presentation is explicitly view-aware |
| Torso/pelvis opposition | Strong candidate; canonical semantic state plus localized resolution |
| Extreme articulation | Better than rigid segments; exact envelope unproven |
| Silhouette/foreshortening | Supports bounded mechanisms without requiring general 3D |
| Garments/interactions | Stable mechanics/anchors remain authoritative; presentation signals are consumable |
| Serialization/testing | Explicit semantic state and override records are testable |
| Replacement-art resilience | High if artwork declares supported ranges and corrective contracts |
| Incremental source fit | High; can extend current model in bounded vertical slices |

### Verdict

**RECOMMENDED, DESIGNED, NOT IMPLEMENTED.** It best balances expressive growth, author control, testability, and asset cost.

## 11. Architecture Candidate C — asset-heavy regional/pose resolution

### Shape

Use many discrete regional orientation and pose-specific art variants, selected from semantic pose bands. Deformation remains minimal; quality comes from authored sprites.

### Evaluation

- Predictable visual quality for covered states and straightforward owner art control.
- High asset and authoring burden across profiles, views, sides, garments, and pose bands.
- Strong risk of combinatorial multiplication and missing-state cliffs.
- Good fallback for signature extremes or endpoints, poor as the whole architecture.
- Testing selection is easier than testing deformation, but coverage completeness becomes enormous.

### Verdict

**DEFER AS A SUPPORTING MECHANISM.** Discrete correctives and endpoint variants belong inside Candidate B. A primarily asset-heavy system should not become canonical unless the hybrid spike fails and evidence shows authored states are the only reliable route.

## 12. Additional Candidate D — deformation-heavy rig

### Shape

Use meshes/lattices or richer continuous warps for torso, sockets, limbs, and foreshortening, with fewer discrete correctives.

### Evaluation

- Potentially high continuous range and reduced variant counts.
- High implementation, authoring, validation, migration, and style-preservation risk.
- Harder to make predictable across replacement artwork and crisp illustrated contours.
- May help localized waist/underarm/foreshortening problems, but the PXZ does not prove it is necessary.

### Verdict

**DEFER GENERAL DEFORMATION.** Permit bounded deformation as an optional presentation primitive only when a focused experiment shows a rigid/corrective solution fails and the deformation remains inspectable and overrideable.

## 13. Comparative matrix

| Concern | A: current design | B: hybrid | C: asset-heavy | D: deformation-heavy |
| --- | --- | --- | --- | --- |
| Mechanical reuse | High | High | Medium | High |
| Illustrative ceiling | Medium/unclear | High candidate | High for covered states | High candidate |
| Asset growth | Medium | Medium | Very high | Low/medium |
| Engineering complexity | Medium/high | Medium/high incrementally | Medium runtime, high content | Very high |
| Manual predictability | High mechanically | High if overrides are explicit | High per asset | Medium/low without excellent tools |
| Graceful fallback | Designed | Strong layered fallback | Often abrupt missing-state gaps | Difficult distortion failures |
| Replacement art | Strong contracts | Strong with metadata | Expensive reauthoring | Rebinding/weighting burden |
| Testability | Strong structural | Strong structural + visual diagnostics | Strong selection, huge coverage | Harder numeric/visual validation |
| Current source fit | Strong | Strong incremental | Moderate | Weakest |
| Recommended role | Foundation | Canonical direction | Supporting mechanism | Optional localized mechanism |

## 14. Recommended architecture

Adopt Candidate B as an amendment to Candidate A:

```text
semantic mechanical pose
  ├─ joint-family state
  ├─ ribcage/pelvis body-mass state
  └─ regional orientation
        ↓
constraint + connection resolver
  ├─ ranges and compatibility
  ├─ socket/contact/overlap envelopes
  └─ suggested semantic depth relations
        ↓
illustrative resolution
  ├─ view artwork
  ├─ localized correctives
  ├─ masks/coverage
  ├─ endpoint variants
  └─ optional bounded deformation
        ↓
author overrides + provenance
        ↓
resolved presentation
```

Mechanical and requested semantic state remain authoritative. Effective presentation may be derived or manually overridden. Derived state never destroys requested state.

## 15. What survives from `2d-doll-rig-0.2`

- Stable segment and separate joint identity.
- One hierarchy shared across profiles.
- Rig/profile/artwork/pose/appearance/render/interaction/root/panel separations.
- X-right/Y-down/clockwise convention and parent-local transforms.
- Normalized elbow/knee flexion, cyclic shoulder/hip semantics, and mechanical versus visual-support status.
- Front/three_quarter/back IDs, 3/4 bridge rule, and no direct Front/Back regional edge.
- Atomic validation, explicit fallback, and mechanical ghosts.
- Typed attachment and interaction anchors.
- Semantic partial-order render relationships rather than canonical global z-index.
- Versioned reusable pose, transfer snapshot, and panel boundaries.
- Branch-atomic arms/legs as a conservative first implementation constraint, subject to later evidence.

## 16. What changes

- Add semantic ribcage/pelvis/body-mass responsibilities instead of treating torso expressiveness as raw rotations alone.
- Add typed connection-zone metadata beyond a pivot.
- Define Illustrative Resolution as an explicit architecture boundary and team responsibility.
- Define localized corrective activation and optional bounded deformation as presentation, not skeleton truth.
- Add requested/derived/author-approved override layers and provenance.
- Add Mechanical, Combinatorial, Expressive, Illustrative, and Owner Validation gates.
- Reopen the priority of region atomicity, garment assumptions, and Task 001 under evidence rather than history.

## 17. What is deferred

- Final numeric anatomy/proportion values and production art.
- General mesh/lattice engine.
- Dense per-segment region orientation.
- Full garment and interaction runtime.
- Full authoring UI, pose loading/transfer, export, IK, animation, multi-character runtime, head/face/hair systems, and Placer.
- Final corrective asset counts and interpolation policy.

## 18. What is rejected

- **REJECTED:** Treating the PXZ as a rig schema or clean segmentation source.
- **REJECTED:** Canonical complete-pose images as the primary body-state model.
- **REJECTED:** Equating mechanical legality with visual acceptance.
- **REJECTED:** Silent Front/Back substitution, silent nearest-anchor binding, destructive coverage, or opaque auto-correction.
- **REJECTED / NON-CANONICAL:** Trapstar body artwork as production visual base.
- **NOT SELECTED:** A general deformation engine before bounded evidence.

## 19. Body grammar

### Required shared mechanical grammar

```text
rig_root
└── pelvis mass
    ├── hip_L → thigh_L → knee_L → lower_leg_L → ankle_L → foot interface_L
    ├── hip_R → thigh_R → knee_R → lower_leg_R → ankle_R → foot interface_R
    └── waist relation
        └── ribcage/chest mass
            ├── shoulder_L → upper_arm_L → elbow_L → forearm_L → wrist_L → hand interface_L
            ├── shoulder_R → upper_arm_R → elbow_R → forearm_R → wrist_R → hand interface_R
            └── neck_socket → optional neck helper → head module
```

Existing stable segment IDs (`pelvis`, `mid_torso`, `chest`, `calf_L/R`, and others) remain source identities. Semantic roles may describe pelvis mass, waist relation, ribcage mass, and lower leg without a silent rename.

### Required connection metadata

Each major articulated connection should be able to declare:

- mechanical pivot and anatomical landmark reference;
- parent socket/contact zone;
- child insertion zone;
- safe overlap envelope;
- supported semantic/orientation range;
- default and suggested render relationships;
- mask/coverage owner space;
- optional corrective/deformation hooks;
- author overrides and provenance.

### Profile-specific data

Profiles own bind transforms, resolved landmarks, proportions, silhouette envelopes, connection-zone geometry, fit measures, supported presentation ranges, and profile-specific corrective assets. Profiles do not rename required joints or fork pose semantics.

## 20. Joint semantics

| Family | Joints/relations | Canonical meaning | Presentation responsibility |
| --- | --- | --- | --- |
| Directional/cyclic | shoulder, hip/thigh root | Direction around socket, mechanically broad | view mapping, near/far, socket response, correctives |
| Hinge/flexion | elbow, knee | normalized extension→flexion | bend-side mapping, compression correctives, depth |
| Limited rotation | wrist, ankle | bounded local rotation | endpoint orientation/variant and footwear/hand presentation |
| Restricted body-mass relation | ribcage/waist/pelvis | bend, twist, arch/crunch, tilt/shift/tuck | coordinated transforms, compression/stretch, silhouette resolution |
| Attachment/non-articulating | neck_socket and module bindings | stable interface | module alignment and presentation selection |

Shoulders and hips must not be modeled as elbows. Torso/pelvis must not be modeled as unrestricted cyclic joints. Wrist/ankle rotation alone must not carry the entire hand/foot orientation problem.

## 21. Torso/pelvis model

### Canonical pose truth

Use a small semantic vocabulary:

- `torsoBend` — signed lateral/forward bend in a declared semantic frame;
- `torsoTwist` — constrained ribcage orientation relative to pelvis;
- `archCrunch` — signed extension/compression relationship;
- `pelvisTilt` — constrained angular relation;
- `pelvisShift` — bounded local translation relative to support/reference;
- `pelvisTuck` — bounded sagittal/postural relation.

These names are **DESIGNED concepts**, not final field names or limits. The prototype must determine which can be merged or derived. The public Poser UI may expose fewer compound controls.

### Derived mechanics

Semantic state may coordinate small rotations/translations across existing `pelvis`, `mid_torso`, and `chest` nodes. It must remain deterministic, inspectable, and serializable. It must not require the user to manipulate hidden corrective nodes directly.

### Presentation

Waist stretch/compression, ribcage side contour, pelvis/hip contour, mask boundaries, depth, and optional bounded warp are derived presentation. The owner can override them without changing the requested semantic pose.

## 22. View and region compatibility

- Keep `front`, `three_quarter`, and `back`; do not add continuous view interpolation yet.
- Keep 3/4 as the only bridge and reject direct Front/Back region edges atomically.
- Retain `torso`, `pelvis`, `arm_L/R`, `leg_L/R`, and `head` as first implementation orientation owners.
- Treat ribcage and pelvis as distinct orientation-capable body masses through the torso/pelvis edge; the waist is their transition contract, not a separate freely mixed view region in the first implementation.
- Keep limb branches orientation-atomic initially. Reopen sub-limb orientation only after endpoint/foreshortening evidence demonstrates that atomic branches are the limiting factor.
- Presentation can use localized transition assets/masks without converting those nodes into independent orientation state.

This preserves a tractable compatibility graph while enabling torso/pelvis opposition—the highest-value new combination suggested by the reference.

## 23. Illustrative-resolution boundary

### Mechanisms and roles

| Mechanism | Problem solved | Truth layer | Near-term status |
| --- | --- | --- | --- |
| Rigid transforms | Basic articulation and placement | Mechanical | Retain |
| Safe overlap/socket zones | Gaps at connections | Rig/profile/art metadata | Design now; prototype next |
| Corrective sprites | Local compression/stretch/contour | Presentation | Prototype small bands |
| Pose-responsive masks | Hide/reveal seam conflicts | Presentation | Prototype with typed owner/target |
| Semantic depth relations | Crossing limbs/masses | Render/presentation | Retain designed graph; defer full compiler |
| Endpoint variants | Hand/foot direction readability | Presentation module | Design interface; defer assets |
| Width/length compensation | Bounded foreshortening | Presentation | Open question |
| Mesh/lattice warp | Continuous localized contour | Presentation | Optional experiment only |
| Complete pose assets | Signature exception | Non-canonical fallback/content | Reject as primary architecture |

Correctives should activate from reusable semantic conditions and allow explicit author selection/strength. No corrective node becomes a mechanical parent.

## 24. Garment readiness

The current garment contract is retained as **DESIGNED — MUST SURVIVE BODY/DEFORMATION REVIEW**.

Garments should bind primarily to stable mechanical segments/AttachmentAnchors, consume profile fit landmarks and presentation/deformation signals, and own their own seam/corrective behavior. They must not force the body to remain rigid. A body corrective may expose a signal or transformed connection zone; a shirt-specific correction remains garment state/art.

No garment runtime belongs in Task 001.

## 25. Interaction readiness

Retain stable local semantic anchors for root, chest, waist, pelvis, shoulders, elbows, wrists, hands/palms/grips, knees, ankles, feet/contacts, head/face/look targets, and sitting contact. Anchors follow mechanical/profile transforms. Presentation corrections may publish optional visual/contact offsets but must not silently replace the canonical anchor. Relationships remain between instance/anchor IDs, never panel coordinates.

No interaction runtime belongs in Task 001.

## 26. Manual tuning and author override model

Every tunable value should support this provenance ladder where applicable:

```text
generated proposal
→ derived/effective value
→ owner author override
→ owner-approved canonical value
```

The minimal record needs:

- stable target path/ID and property;
- proposed value and generator/source evidence;
- authored override value;
- effective value and resolution reason;
- author/status/timestamp or equivalent provenance;
- compatible rig/profile/artwork versions;
- ability to disable/remove the override and recompute.

Override classes include pivots, local art offsets, connection zones, supported ranges, view mappings, mask parameters, seam overlap, depth relations, corrective choice/strength, bounded deformation, foreshortening, and anchor offsets. Pose-specific overrides belong to pose/authoring state; canonical profile/art overrides belong to their definition packages. Overrides never silently bake into source artwork.

## 27. Minimal rig-package amendment

Do not require many physical JSON files; require logical versioned contracts:

### Required core

- `RigDefinition`: stable IDs, hierarchy, joint families, semantic state schema, regions, anchors, extension declarations.
- `BodyProfile`: bind transforms, landmarks, proportions, connection zones, supported mechanical/presentation ranges.
- `ArtworkSet`: assets, owner spaces, view variants, bounds, masks, overlap envelopes, correctives, endpoint variants, optional deformation descriptors.
- `CompatibilityContract`: orientation graph, transition requirements, fallbacks.
- `AuthorOverrideSet`: typed overrides and approval state.
- `Provenance`: generator/source/version and proposed-versus-approved changes.

### Optional presentation extensions

- corrective selectors;
- pose-responsive render suggestions;
- mask/coverage rules;
- bounded deformation descriptors;
- garment-consumable deformation signals;
- visual/contact anchor offsets.

Unknown optional extensions round-trip. Required major-version mismatches reject or open read-only. Migration is explicit and never shape-guessed.

## 28. QA and validation strategy

### Mechanical gate

Pure model tests cover semantic domains, clamps/wraps, transform propagation, state separation, reset, serialization, atomic invalid edits, and migration.

### Combinatorial gate

Generated tests cover region/head tuples, bridge contracts, missing assets, fallback, profile/art replacement, and preservation of requested semantic state.

### Expressive gate

Pose sweeps cover lean, reach, crouch, arch, crunch, twist, weight shift, asymmetric stance, crossed limbs, and compressed hinges. Diagnostics measure gaps, connection-zone escape, overlap inversion, discontinuous corrective selection, anchor drift, and unsupported-state frequency.

### Illustrative gate

Visual diagnostics compare silhouettes, seam continuity, body-mass relationships, masks, depth order, endpoint readability, and foreshortening across a bounded pose set. Golden images can detect change; they cannot decide artistic acceptability.

### Owner Validation

The owner must pose and tune representative characters, inspect failure explanations, correct defects non-destructively, reload the result, and approve that the workflow and output are useful. No automated score can replace this gate.

## 29. Open questions

| Priority | OPEN QUESTION | Existing evidence | Smallest resolving experiment | Owner judgment? |
| --- | --- | --- | --- | --- |
| 1 | Can a small torso/pelvis semantic + corrective vocabulary reach useful expressive continuity? | PXZ shows need; current rig lacks it | Task 001 torso/pelvis spike | Yes for visual usefulness |
| 2 | Are discrete waist/socket correctives sufficient, or is bounded deformation necessary? | Masks/fragments imply local resolution; method unproven | Compare rigid, corrective/mask, and one bounded-warp variant in Task 001 | Yes |
| 3 | What is the smallest body-mass semantic vocabulary? | Bend/twist/arch/shift concepts exist only in design | Interaction/control sweep in Task 001 | Yes for usability |
| 4 | How many shoulder/hip response bands avoid asset explosion? | Target shows compression; current art/ranges narrow | Later one-socket spike after torso result | Yes |
| 5 | How should foreshortening be represented? | Rigid 2D rotation is insufficient; no canonical assets | Later single-limb endpoint spike | Yes |
| 6 | Does branch-atomic limb orientation remain adequate? | Safe current design; no sub-limb transition evidence | Revisit after foreshortening/endpoint spike | Possibly |
| 7 | How do garments consume deformation without constraining body anatomy? | Strong designed contract, no assets/runtime | Garment contract review after body signal prototype | Yes for garment behavior |
| 8 | What immutable reference policy is required? | Existing RIG-U03 | Decide before production transfer | No/engineering policy |
| 9 | How are legacy Back non-elbow poses migrated? | Existing ambiguity | Migration fixture/prototype | No, unless visual repair |

## 30. Combinatorial impact

The recommended architecture enables combinations unavailable to the current mechanical slice:

- one semantic torso/pelvis relationship across multiple profiles and view presentations;
- many poses sharing a small neutral/stretched/compressed waist vocabulary;
- shoulders/hips combining broad mechanics with localized socket response;
- view changes preserving pose meaning while presentation assets/masks change;
- garments and interactions following stable mechanics while consuming optional presentation signals;
- automatic proposals combining with reversible owner corrections;
- replacement art retaining pose semantics and override provenance.

The primary restriction is intentional: not every mechanically imaginable state is automatically presentation-supported. Unsupported states remain visible, diagnosable, and non-destructive instead of being silently faked.

## 31. Reality state after Task 000

- **SPECULATIVE:** Exact torso fields/limits, deformation method, corrective counts, foreshortening, and final assets.
- **DESIGNED:** Candidate B hybrid direction; semantic body-mass/connection/illustrative-resolution/override/provenance boundaries; updated team and QA responsibilities.
- **IMPLEMENTED:** Only documentation from this pass plus the pre-existing bounded Poser runtime.
- **TESTED:** Current source-aligned mechanical suite and browser matrix; document integrity checks recorded in the associated pass report. The new architecture is not runtime-tested.
- **VALIDATED:** Nothing in the owner creative workflow.

## 32. Recommended bounded Task 001

### Task

**Torso–Pelvis Illustrative-Resolution Spike**

### Why this uncertainty is highest leverage

The PXZ target derives much of its expressive quality from ribcage/pelvis opposition, waist curvature, compression/stretch, and pelvis shift. These relationships affect shoulder/hip connections, region orientation, garments, depth, and the decision between correctives and deformation. Testing them first challenges the recommended hybrid architecture at its riskiest point.

### In scope

- An isolated experimental harness or explicitly experimental model path; do not replace the canonical runtime.
- One 3/4 presentation only, so view mixing does not confound the anatomy/presentation question.
- A bounded semantic state covering a small trial set of bend, arch/crunch, pelvis tilt, and pelvis shift; reduce the vocabulary if redundancy is found.
- Existing/provisional or purpose-built diagnostic torso/pelvis artwork clearly labeled non-production.
- Typed waist connection zone, safe overlap, and mask ownership.
- Compare three resolution modes over the same semantic sweep: rigid overlap only; three-band localized corrective/mask behavior (neutral, stretch, compression); and one bounded deformation trial if rigid/corrective evidence warrants it.
- Explicit author overrides for offset, mask/corrective selection or strength, and depth relation.
- A pose-sweep contact sheet plus model diagnostics for gaps, overlap, unsupported states, and override round trip.

### Out of scope

- Front/Back regional mixing, full-body orientation UI, shoulders/hips, limb semantics, foreshortening, hands/feet, garments, interactions, final art, full transfer/export, IK, animation, and production schema migration.

### Evidence supporting success

- One semantic state deterministically drives all three presentation modes.
- The corrective vocabulary improves continuity across the bounded sweep without complete-pose assets.
- Overrides remain reversible and reload without changing requested semantic pose.
- Failures are explicit and localized.
- Owner review finds at least one mode meaningfully easier to tune toward an expressive silhouette than rigid segments alone.

### Falsification/revision result

Revise Candidate B if the bounded vocabulary cannot avoid severe seams/silhouette failures without pose-specific whole-body fragments, if correction choice becomes opaque/nonlocal, or if the deformation trial is required but cannot remain stable under replacement diagnostic art. A failure is useful evidence, not permission to hide the target behind more rigid constraints.

### Files Task 001 should avoid

- Do not edit the inherited baseline.
- Do not add garment/interaction/runtime production features.
- Do not silently promote experimental schema fields into `2d-doll-rig-0.2` before results are reviewed.

The old Orientation Compatibility Prototype remains valuable, but it no longer has the highest information value. It should follow after the torso/pelvis spike establishes what a transition contract must be able to resolve.
