# Bilateral Knee Semantic Mapping Contract

## Status and Authority

This document is an **OWNER-APPROVED / DESIGNED** contract for the bounded bilateral-knee implementation proof. Owner approval authorizes that implementation scope; it does not establish workflow VALIDATION, approve anatomy/artwork, or claim executed tests.

It is subordinate to the repository protocol, the canonical rig contracts, and owner approval. Current source reality remains elbow-only semantic mapping plus transitional raw-degree knees.

## Objective

Prove one reusable bilateral hinge semantic across `front`, `three_quarter`, and `back` while preserving:

- stable JointId versus SegmentId identity;
- one requested semantic value per knee;
- explicit per-view projection;
- bilateral handedness;
- inverse direct manipulation;
- mechanical truth distinct from presentation support;
- a truthful experimental persistence boundary;
- explicit provenance and unresolved status.

## Scope

### In Scope for the Following Implementation Pass

- `knee_L` and `knee_R` only.
- Whole-body `front`, `three_quarter`, and `back` anchor views.
- Data-driven definitions, forward/inverse mapping, controls, direct manipulation, diagnostics, experimental pose export, tests, and evidence.
- Compatibility aliases from current child SegmentIds.

### Out of Scope

- Shoulder/hip cyclic implementation.
- Wrists, ankles, torso, IK, animation, touch, undo, pose loading, regional orientation mixing, runtime extraction, or asset-boundary changes.
- Production artwork, masks, correctives, deformation, or approved presentation limits.
- Full `2d-doll-pose-0.2` or transfer implementation.
- Automated migration or lossless interpretation of legacy Back raw degrees.

## Stable Identities

| JointId | Parent SegmentId | Child SegmentId | PivotId | Legacy pose key |
| --- | --- | --- | --- | --- |
| `knee_L` | `thigh_L` | `calf_L` | `knee_L` | `calf_L` |
| `knee_R` | `thigh_R` | `calf_R` | `knee_R` | `calf_R` |

`_L` and `_R` are anatomical sides in every view. A view change never swaps identities. The runtime may accept the legacy child SegmentId at a compatibility boundary, but new semantic state and experimental export use JointId.

## Semantic and Mechanical Definition

```text
semantic kind: hinge_flexion
unit: normalized
domain: [0,1]
neutral: 0
normalization: clamp
mechanical degrees: 180 × semantic value
nominal maximum: 150° (DESIGNED, not artwork-approved)
```

The control is a planar projected hinge. `0` means authored neutral/extended; `1` means the designed 180° mechanical maximum. It must not be described as artist-approved sagittal knee flexion in Front/Back artwork.

## Projection Rule

Per RIG-017:

```text
sideSign(L) = +1
sideSign(R) = -1
viewSign(front) = +1
viewSign(three_quarter) = +1
viewSign(back) = -1
direction = sideSign × viewSign

mechanicalDegrees = 180 × clamp(u, 0, 1)
renderedDegrees = direction × mechanicalDegrees
inverse u = clamp((direction × renderedDegrees) / 180, 0, 1)
```

Exact table:

| JointId | Front | Three-quarter | Back |
| --- | ---: | ---: | ---: |
| `knee_L` | `+180u` | `+180u` | `-180u` |
| `knee_R` | `-180u` | `-180u` | `+180u` |

The Front/Back handedness is a **DESIGNED** consequence of verified directionality and bilateral symmetry. The 3/4 mapping is explicitly `provisional_projection`, not “3/4 guessed” and not anatomy-approved. It must carry `PRESENTATION_MAPPING_UNVERIFIED` until direct continuity review supplies stronger evidence.

## Definition and Provenance Shape

The implementation data must express the equivalent of:

```js
{
  id: "knee_L",
  parentSegmentId: "thigh_L",
  childSegmentId: "calf_L",
  pivotId: "knee_L",
  semantic: {
    kind: "hinge_flexion",
    unit: "normalized",
    minimum: 0,
    maximum: 1,
    neutral: 0,
    normalization: "clamp",
  },
  mechanics: {
    minimumDeg: 0,
    maximumDeg: 180,
    nominalMaximumDeg: 150,
  },
  presentationMappings: {
    front: {
      mappingKind: "affine_v1",
      offsetDeg: 0,
      scaleDegPerUnit: 180,
      projectionStatus: "derived_direction",
    },
    three_quarter: {
      mappingKind: "affine_v1",
      offsetDeg: 0,
      scaleDegPerUnit: 180,
      projectionStatus: "provisional_projection",
    },
    back: {
      mappingKind: "affine_v1",
      offsetDeg: 0,
      scaleDegPerUnit: -180,
      projectionStatus: "derived_direction",
    },
  },
  presentationSupport: {
    inheritedProvisionalMaximum: 98 / 180,
    unsupportedPolicy: "render_provisional_with_warning",
    ownerApproved: false,
  },
  provenance: {
    stage: "derived_result",
    evidenceRef: "2026-08-26_1058_non-elbow-semantic-mapping-verification",
    ownerApproved: false,
  },
}
```

The right-knee mapping uses the exact sign table above. Implementations may generate the sign from typed side/view data, but the resolved records must remain inspectable and testable.

Tuning precedence remains:

```text
owner-approved canonical
→ author override
→ derived result
→ generated proposal
```

No author or owner layer exists in this first proof. The derived values must not be mislabeled as approved.

## Requested Versus Effective Result

Canonical experimental state stores requested semantics only:

```js
semanticJoints: {
  knee_L: 0.5,
  knee_R: 0.25,
}
```

Rendering derives a non-persistent resolution record:

```js
{
  jointId: "knee_L",
  requestedSemantic: 0.5,
  normalizedSemantic: 0.5,
  requestedViewId: "three_quarter",
  effectiveViewId: "three_quarter",
  mechanicalDegrees: 90,
  renderedDegrees: 90,
  mechanicalStatus: "allowed",
  presentationRangeStatus: "supported_by_inherited_provisional_range",
  projectionStatus: "provisional_projection",
  issues: ["PRESENTATION_MAPPING_UNVERIFIED"],
}
```

There is no orientation fallback in this proof. `effectiveViewId` equals the requested whole-body view or rig initialization fails. Derived angles, support status, and issues never overwrite requested semantic state.

## Presentation Support and Failure Behavior

The inherited `98°` bend is a provisional evidence boundary, not the semantic scale. Thus:

```text
provisional supported semantic interval = [0, 98/180]
mechanically legal interval = [0,1]
```

For values above `98/180`:

- preserve the requested semantic value;
- compute and render the full mechanically mapped angle;
- set `presentationRangeStatus = unsupported`;
- emit `PRESENTATION_RANGE_UNSUPPORTED`;
- show a persistent authoring warning;
- label the rendering provisional;
- never clamp to `98°`, substitute another view, or claim presentation resolution.

This `render_provisional_with_warning` behavior is chosen specifically to expose seam, overlap, silhouette, and endpoint failures during the proof. It is authoring behavior, not export approval.

The inherited `-8°/+8°` extension slack is excluded. Hyperextension remains unsupported and unapproved.

Required structured issues:

| Code | Trigger | Required effect |
| --- | --- | --- |
| `JOINT_MAPPING_MISSING` | Missing requested knee/view mapping | Block rig readiness atomically; no identity fallback |
| `JOINT_MAPPING_INVALID` | Non-finite value, zero scale, reversed/invalid domain, duplicate JointId, or unknown unit | Block rig readiness with exact path |
| `PRESENTATION_MAPPING_UNVERIFIED` | Any 3/4 knee projection in this proof | Preserve/render state with explicit warning |
| `PRESENTATION_RANGE_UNSUPPORTED` | `u > 98/180` with inherited artwork | Preserve/render full mechanics with explicit warning |
| `LEGACY_SEMANTIC_AMBIGUITY` | Future attempt to interpret ambiguous legacy Back raw degrees | Preserve ambiguity; never claim lossless migration |

## Frozen Persistence Strategy

The knee proof must not write normalized knees under `2d-doll-pose-0.1`, and it must not claim the complete designed `2d-doll-pose-0.2` contract.

The selected strategy is a separate experimental export document:

```js
{
  schemaVersion: "2d-doll-semantic-knee-proof-0.1",
  status: "experimental",
  rigSchemaVersion: "2d-doll-rig-0.1",
  mappingContract: "bilateral-knee-semantic-0.1",
  presentationProvenance: {
    authoritative: false,
    mappingContract: "bilateral-knee-semantic-0.1",
    artworkSet: "inherited-canonical-base-body-rig-v0.1",
    supportContract: "inherited-knee-support-provisional-0.1",
    requestedViewId: "front",
    projectionStatusAtSave: "derived_direction",
    issueCodesAtSave: [],
  },
  requestedViewId: "front",
  semanticJoints: {
    elbow_L: 0,
    elbow_R: 0,
    knee_L: 0,
    knee_R: 0,
  },
  transitionalPartDegrees: {
    pelvis: 0,
    mid_torso: 0,
    chest: 0,
    upper_arm_L: 0,
    hand_L: 0,
    upper_arm_R: 0,
    hand_R: 0,
    thigh_L: 0,
    foot_L: 0,
    thigh_R: 0,
    foot_R: 0,
  },
  depthOverrides: {},
}
```

Exact semantic aliases for current elbows are `forearm_L → elbow_L` and `forearm_R → elbow_R`. Transitional fields are explicitly named and remain raw degrees. The experimental document contains no camera, character, or editor state.

Rules:

- New Save Pose output uses this experimental type once knee semantics are implemented.
- Existing pose 0.1 files are neither loaded nor migrated in this pass; pose load remains out of scope.
- No field is inferred by shape.
- A later complete pose 0.2 migrator must recognize this document by exact type/version and map its stable semantic JointIds deliberately.
- `semanticJoints` is the only authoritative articulation truth in the experimental document.
- `presentationProvenance` preserves enough non-authoritative context to explain what mapping, provisional artwork/support contract, view, projection status, and warnings were active when saved.
- Transient `renderedDegrees`, clamped/effective pose copies, matrices, and derived screen state must not be serialized. They are recomputed from requested semantics plus the referenced mapping/support context.
- Presentation provenance must never override or compete with requested semantic state during future migration or replay.

## Implementation Boundary

The next pass should:

1. Add the frozen definition data and validation.
2. Add tests before behavior changes.
3. Make joint construction consume data without `partId` behavior branches.
4. Preserve generic hierarchy and pointer-space transform flows.
5. Store the two knees internally by stable JointId, with explicit compatibility aliases at current runtime/UI boundaries.
6. Add normalized controls and direct manipulation inversion.
7. Return separate mechanical and presentation resolution data.
8. Change Save Pose to the exact experimental document.
9. Run browser evidence and independent QA.

It must not begin shoulders/hips, load/migration, full regional orientation state, or runtime module extraction.

## Frozen Acceptance Matrix

All cases are **DESIGNED future tests** until executed.

### Model and Definition

| ID | Case | Required oracle |
| --- | --- | --- |
| KNEE-M01 | Enumerate both stable knees and aliases | Exact JointId/parent/child/pivot/legacy-key table; no duplicates |
| KNEE-M02 | Enumerate 2 knees × 3 views | Exact finite sign/mapping table; no missing view |
| KNEE-M03 | Delete each mapping in fixture variants | Atomic `JOINT_MAPPING_MISSING`; never identity fallback |
| KNEE-M04 | Inject non-finite/zero-scale/bad-domain/unknown-unit/duplicate-ID records | Atomic path-specific `JOINT_MAPPING_INVALID` |
| KNEE-M05 | Forward map `u = 0,.25,98/180,.75,1` for all six mappings | Exact rendered degrees from the frozen table |
| KNEE-M06 | Forward then inverse the same samples | Semantic error ≤ `1e-9` |
| KNEE-M07 | Input `-0.01`, `1.01`, `NaN`, infinity, numeric strings | Exact clamp/reject policy; no NaN propagation or coercion ambiguity |
| KNEE-M08 | Cycle Front→3/4→Back→Front 100 times with asymmetric knees | Requested semantic state deep-equal after every switch |
| KNEE-M09 | Test `98/180`, just above it, `.75`, and `1` | Semantic value preserved; support status/warnings exact; full angle not clamped |
| KNEE-M10 | Parent/descendant/opposite-branch matrices in all views | Knee pivot fixed; foot follows; thigh/opposite leg stable |
| KNEE-M11 | Reset knees from non-neutral | Both knees exact zero; character/camera/view/depth scopes unchanged |
| KNEE-M12 | Serialize asymmetric elbows/knees plus transitional values | Exact experimental document; no pose 0.1 reinterpretation; no camera/character/editor |
| KNEE-M13 | Existing elbow and repository suites | No regression |

### Browser and Visual Evidence

| ID | Case | Required oracle |
| --- | --- | --- |
| KNEE-B01 | Set asymmetric knees; Front→3/4→Back→Front | Same semantics, exact rendered signs, no runtime error |
| KNEE-B02 | Drag both knee handles in all three views | Correct JointId selected; expected inverse value; unrelated state unchanged |
| KNEE-B03 | Slider/numeric edits for both knees | Controls, canvas, and semantics synchronize |
| KNEE-B04 | Values at/above provisional support | Persistent explicit warning; full provisional rotation; no semantic or visual clamp |
| KNEE-B05 | Combine both knees with both elbows | All four hinge semantics remain independent across views |
| KNEE-B06 | Alternate direct/numeric edits and views 100 times | No drift; exact reset |
| KNEE-B07 | Pose plus character move, camera pan/zoom, and Fit Body | State scopes remain independent |
| KNEE-B08 | Save Pose | Download exactly matches KNEE-M12 |
| KNEE-B09 | Hide handles; capture neutral, support edge, just outside, and maximum for both sides/views | Anatomy and Illustrative reviewers record continuity/presentation status |
| KNEE-B10 | Direct right-side inspection | Bilateral sign is observed, not inferred only from source |
| KNEE-B11 | Lifecycle/console audit | Ready with zero error-level entries; invalid mapping blocks readiness explicitly |

## Review and Gate Sequence

```text
tests-first mechanics
→ runtime wiring
→ Front/3/4/Back evidence
→ Anatomy continuity review
→ Illustrative Resolution review
→ independent QA
→ Owner Validation later
```

- Mechanical may pass only from executed mapping, inverse, hierarchy, state, and persistence evidence.
- Combinatorial can be at most PASS WITH DOCUMENTED LIMITATIONS in this slice.
- Expressive remains unresolved until continuity sweeps are reviewed.
- Illustrative remains unresolved until seams, silhouette, overlap, depth, and endpoints are reviewed.
- Owner Validation cannot be supplied by the team.

## Contract-Freeze Verdict

**OWNER APPROVED FOR THE BOUNDED IMPLEMENTATION PROOF. NOT IMPLEMENTED.**

The next implementation pass is sufficiently bounded once the documentation closure commit is published or its unpublished dependency chain is explicitly authorized.
