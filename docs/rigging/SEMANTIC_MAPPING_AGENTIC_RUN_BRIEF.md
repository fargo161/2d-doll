# Semantic Mapping Agentic Run Brief

## Status

This brief is **DESIGNED** preparation for a future bounded agentic-team run. The owner has approved the implementation scope in [the Bilateral Knee Semantic Mapping Contract](architecture/BILATERAL_KNEE_SEMANTIC_MAPPING_CONTRACT.md); no implementation or test result is claimed here.

The triggering evidence is [the non-elbow verification report](../pass-reports/2026-08-26_1058_non-elbow-semantic-mapping-verification.md): identical raw shoulder, hip, and knee degrees do not preserve anatomical direction between Front and Back. Elbow mapping remains the only current view-independent semantic precedent.

## Launch State

- **Design run:** Prepared.
- **Implementation run:** Owner-authorized within RIG-020; repository publication gate remains.
- **Repository gate:** Local `HEAD` and `origin/main` both equal `c760fe3f02d2cc343a440beee20b2f99fcd598a8`, but the verification report and pass-ledger edit are uncommitted. Close or explicitly authorize that dependency chain before implementation.
- **Contract gate:** Passed for the bilateral-knee proof. RIG-017, RIG-018, RIG-019, and RIG-020 are OWNER APPROVED / DESIGNED.
- **Owner gate:** Anatomy, artwork support, visual continuity, and workflow usefulness remain OWNER VALIDATION REQUIRED.

## Bounded Objective

Establish a data-driven semantic mapping seam without changing inherited assets or pretending provisional artwork ranges are anatomical approval.

The smallest first implementation proof is both knees across `front`, `three_quarter`, and `back`. It exercises normalized hinge semantics, bilateral/view sign projection, inverse direct manipulation, hierarchy propagation, support-status separation, and persistence compatibility without also introducing cyclic shoulder/hip authoring.

Shoulders and hips remain in the same designed contract, but their runtime implementation is a second bounded slice because it requires cyclic wrap, branch-cut-safe direct manipulation, and a signed display convention.

## Stable Identity Contract

| JointId | Parent SegmentId | Child SegmentId | Semantic kind | Unit |
| --- | --- | --- | --- | --- |
| `shoulder_L` | `chest` | `upper_arm_L` | planar cyclic swing | degrees `[0,360)` |
| `shoulder_R` | `chest` | `upper_arm_R` | planar cyclic swing | degrees `[0,360)` |
| `hip_L` | `pelvis` | `thigh_L` | planar cyclic swing | degrees `[0,360)` |
| `hip_R` | `pelvis` | `thigh_R` | planar cyclic swing | degrees `[0,360)` |
| `knee_L` | `thigh_L` | `calf_L` | hinge flexion | normalized `[0,1]` |
| `knee_R` | `thigh_R` | `calf_R` | hinge flexion | normalized `[0,1]` |

Legacy SegmentId keys remain explicit boundary aliases. `_L` and `_R` always mean anatomical side, never screen side.

## Director-Resolved Projection Rule

Define:

```text
sideSign(L) = +1
sideSign(R) = -1
viewSign(front) = +1
viewSign(three_quarter) = +1  // provisional projection; review required
viewSign(back) = -1
direction = sideSign × viewSign
```

For shoulder/hip cyclic state `q`:

```text
signedDelta = wrapTo[-180,180)(q)
renderedDelta = direction × signedDelta
inverse q = wrapTo[0,360)(direction × renderedDelta)
```

For knee flexion `u`:

```text
mechanicalDegrees = 180 × clamp(u, 0, 1)
renderedDelta = direction × mechanicalDegrees
inverse u = clamp((direction × renderedDelta) / 180, 0, 1)
```

This rule makes equal left/right semantic values produce mirrored bilateral motion and makes a semantic pose retain anatomical direction across Front/Back. It does not swap IDs.

## Mechanical Truth Versus Presentation Support

Current inherited ranges are provisional presentation evidence only:

| Family | Mechanical domain | Provisional current-art support |
| --- | --- | --- |
| Shoulder | cyclic `[0°,360°)` | signed delta approximately `[-65°,65°]` |
| Hip | cyclic `[0°,360°)` | signed delta approximately `[-38°,38°]` |
| Knee | normalized `[0,1]` → `0°…180°` | `0…98/180` flexion |

Values outside current-art support remain mechanically meaningful. They must produce a separate `PRESENTATION_RANGE_UNSUPPORTED` result; they must not be silently clamped into a different pose. The inherited knee `±8°` extension slack is not approved hyperextension and is excluded from the initial semantic support claim.

## Required Mapping Record

Each semantic joint must declare, as data rather than `partId` branches:

```text
JointId
parentSegmentId
childSegmentId
pivotId
semantic kind/unit/domain/neutral/normalization
mechanical domain
orientation mapping for front/three_quarter/back
supported visual/semantic intervals
unsupported policy and structured issue
profile/artwork compatibility
provenance and reversible tuning layers
```

Tuning precedence remains:

```text
owner-approved canonical
→ author override
→ derived result
→ generated proposal
```

Disabling an override must recompute from the preceding layer rather than destructively baking it.

## Persistence Gate

Current `2d-doll-pose-0.1` state is part-keyed and mixes normalized elbows with raw non-elbow degrees. Normalized knees must not silently reuse the same field meaning.

Before implementation, the Director must select and document one bounded strategy:

1. **Mechanics-only experimental proof:** mapping and inverse tests plus a non-persistent runtime diagnostic surface; existing Save cannot emit normalized knees as pose 0.1.
2. **Versioned semantic slice:** introduce an explicitly partial experimental document/version and an exact compatibility adapter, without claiming the complete designed pose 0.2 contract.
3. **Full pose 0.2 migration:** larger scope requiring loader, atomic validation, aliases, requested/effective orientations, and migration issues; not recommended for the first knee proof.

Any legacy Back conversion remains non-lossless and must emit `LEGACY_SEMANTIC_AMBIGUITY`. Shape guessing is forbidden.

## Agentic Team Topology

### Director

The Rig Program Director freezes scope, resolves engineering conflicts, preserves owner-only decisions, and synthesizes the pass.

### Independent Round 1 groups

1. **Schema + Orientation + Serialization:** exact records, aliases, view mappings, structured issues, version boundary, requested/effective state.
2. **Anatomy + Kinematics:** landmark meaning, equations, manipulation, constraints, bilateral and view continuity, unsupported bands.
3. **Integrator + QA:** source-fit, migration risks, tests-first sequence, adversarial matrix, independent gate result.

No group edits shared source during independent findings.

### Round 2 cross-review

- Anatomy reviews Kinematics continuity and naming.
- Kinematics reviews pivot/landmark assumptions.
- Orientation reviews every view-dependent sign and fallback.
- Serialization verifies every new semantic/status/provenance field has a durable representation.
- Integrator maps the frozen proposal to source seams.
- Illustrative Resolution reviews seams, masks, overlap, silhouette, and unsupported presentation after mechanics.
- QA audits the frozen synthesis independently.

### Implementation ownership

Only after the design and repository gates pass:

- Integrator owns bounded source changes.
- QA owns acceptance and does not rewrite the proposal while auditing.
- Director records conflicts and stops at the authorized slice boundary.

## Source-Fit Plan

Preserve these sound seams:

- `semanticToVisual()` / `visualToSemantic()` as affine conversion primitives, extended to return mechanical and presentation results separately.
- `computeBodyMatrices()` as the generic mapping consumer.
- Runtime inverse parent/character/camera transform flow for direct manipulation.

Change these seams intentionally:

- Replace elbow/non-elbow branching in `buildJointDefinitions()` with validated rig-provided semantic definitions.
- Introduce stable JointId-to-child-SegmentId adapters.
- Reject missing, non-finite, zero-scale, reversed, duplicate, or unknown-unit mappings explicitly.
- Add normalized bilateral knee controls and inverse mapping in the first implementation slice.
- Defer cyclic shoulder/hip controls until wrap and branch-cut behavior are explicitly implemented.
- Do not edit the inherited manifest or assets.

## Minimum Knee-Proof Acceptance

All tests below are **DESIGNED** until executed.

### Model

- Enumerate both knee identities and all six knee/view mappings.
- Forward/inverse round trip at `0`, `0.25`, `98/180`, `0.75`, and `1` with error at most `1e-9`.
- Clamp below `0` and above `1` mechanically while preserving presentation status.
- Cycle `front → three_quarter → back → front` 100 times with exact semantic stability.
- Confirm the `98/180` boundary, then verify values above it remain semantic truth and report unsupported presentation.
- Reject missing/invalid mapping atomically with `JOINT_MAPPING_MISSING` or a path-specific validation issue.
- Preserve hierarchy propagation, opposite-branch isolation, reset scopes, and elbow behavior.
- Prove the selected persistence strategy does not reinterpret pose 0.1.

### Browser

- Manipulate both knees in all three views through handles, sliders, and numeric inputs.
- Verify same semantic flexion, expected rendered sign, selected JointId, synchronized controls, and unrelated-state stability.
- Test asymmetric bilateral knees plus both elbows.
- Repeat view switches and edits without drift.
- Capture neutral, support-edge, just-outside-support, and mechanical-maximum sheets with handles hidden.
- Observe zero error-level console entries and explicit failure for invalid mapping data.

### Gates

- **Mechanical:** May pass from executed mapping, inverse, hierarchy, state, and persistence evidence.
- **Combinatorial:** At most PASS WITH DOCUMENTED LIMITATIONS until shoulders/hips, replacement art, and additional profiles are covered.
- **Expressive:** Requires anatomy continuity review of the sweep.
- **Illustrative:** Remains unresolved until seams, silhouette, overlap, depth, and endpoints are reviewed.
- **Owner Validation:** Required separately and cannot be supplied by the team.

## Adversarial Cases

- Missing Back or 3/4 mapping; never fall back to identity.
- Zero scale, non-finite value, reversed bounds, or swapped `_L/_R` record.
- `u = -0.01`, `1.01`, `NaN`, infinity, and numeric strings.
- One invalid mapping among otherwise valid records; reject atomically.
- View switch or reset during active drag.
- Mapping present with missing artwork and artwork present with missing mapping.
- Legacy Back degree values that resemble normalized values.
- Presentation reflection versus semantic mirror; neither may rewrite anatomical IDs.
- Save after failed edit; preserve the last valid pose.

## Explicit Non-Goals

- Shoulder/hip cyclic runtime work in the first knee proof.
- Wrists, ankles, torso semantics, IK, animation, touch, undo, or pose loading.
- Regional orientation mixing.
- Artwork, mask, corrective, or deformation production work.
- Full pose 0.2 or transfer implementation unless separately authorized.
- Claims of anatomical, illustrative, or workflow validation.

## Start Checklist

- [x] Documentation chain included in the bounded owner-approval closure commit containing this update; publication remains required before implementation unless an unpublished chain is explicitly authorized.
- [x] Persistence strategy owner-approved as DESIGNED.
- [x] Knee JointId/mapping/support records owner-approved as DESIGNED.
- [x] Missing/unsupported behavior and issue codes owner-approved as DESIGNED.
- [x] Independent role briefs issued with no synthesized answer in Round 1.
- [ ] Implementation file ownership assigned after synthesis.
- [ ] Model tests written before runtime behavior changes.
- [x] Browser, Anatomy, Illustrative, and QA evidence specified in the freeze contract.
- [ ] Mandatory implementation pass report and ledger entry reserved.
- [x] Owner-validation boundary stated in the handoff.

## Current Readiness Verdict

**OWNER-APPROVED DESIGN. IMPLEMENTATION AWAITS THE REPOSITORY PUBLICATION GATE.**

The source seam is viable and the first mechanical proof is bounded. Implementation remains gated by repository closure and the persistence strategy, not by uncertainty about whether the current raw mapping is deficient.
