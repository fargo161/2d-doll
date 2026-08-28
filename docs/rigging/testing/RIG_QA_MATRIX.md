# Canonical Rig QA Matrix

## Gate status

These are **DESIGNED future tests** unless the evidence column names a current executed boundary. Current tests do not establish the complete contract or workflow validation. Each implementation pass must record the exact cases it actually ran.

## Permanent gate vocabulary

| Gate | Question | Evidence boundary |
| --- | --- | --- |
| Mechanical | Are hierarchy, transforms, semantic joints, connectivity, constraints, reset, and serialization correct? | Primarily automated model/runtime evidence |
| Combinatorial | Are legal region/profile/art combinations accepted, illegal combinations rejected, and requested semantics preserved? | Generated matrices, replacement/missing-data fixtures, atomic validation |
| Expressive | Can the body achieve useful lean, reach, crouch, arch, crunch, twist, weight shift, asymmetry, compression, and self-overlap without structural failure? | Pose sweeps plus anatomy/continuity review |
| Illustrative | Do seams, silhouette, body masses, overlap, depth, masks, correctives, foreshortening, and endpoints resolve convincingly? | Visual diagnostics and explicit unresolved-state checks |
| Owner Validation | Is the rig useful, understandable, tuneable, and visually acceptable in the intended creative workflow? | Owner exercise and approval only |

Automated checks may support the first four gates but can never create Owner Validation. `MECHANICALLY VALID`, `PRESENTATION RESOLVED`, and `OWNER VALIDATION REQUIRED` remain separate verdicts.

| ID | Category and setup | Action | Required oracle | Evidence needed |
| --- | --- | --- | --- | --- |
| SEL-01 | Every required segment in each profile/orientation | Select artwork and segment control | Correct typed SegmentId; no joint/anchor ambiguity | Automated enumeration plus UI observation |
| SEL-02 | Every required joint/pivot | Select visible pivot/control | Correct JointId, parent, zero, arcs, warning state | Enumeration and direct interaction |
| SEL-03 | Every required anchor | Select anchor tool/marker | Correct anchor type/owner/relationships; editor-only | UI and serialization exclusion |
| ROOT-01 | Neutral and posed character | Move whole character | Root changes; joints, camera, relationships unchanged | Model/UI regression; current narrow behavior TESTED |
| JNT-01 | Every joint, both profiles, all supported orientations | Traverse declared min/max and over-range | Clamp/wrap exact; semantic and presentation statuses correct | Parameterized model plus visual checks |
| HIE-01 | Each hierarchy branch | Move parent then child | Descendants follow; ancestors/unrelated branches stable | Matrix assertions; current representative branches TESTED |
| EDT-01 | Repeated edits and reset | Alternate direct/numeric changes 100 times | No drift; one semantic truth; reset exact | Stress/property test |
| TUN-01 | Generated/derived value plus author override | Override pivot/offset/range/mask/depth/corrective value, save/reload, disable override | Requested/generated/authored/approved values remain distinguishable; disable recomputes; no destructive bake | Model round trip plus authoring observation |
| ORI-01 | Same semantic pose in each whole-body view | Switch Front/3/4/Back repeatedly | Pose/profile/root/garments/relationships preserved | Model/render round trip; current elbows TESTED |
| ORI-02 | Every LEGAL region edge | Apply region tuple | Commits atomically with matching mappings/art | Exhaustive matrix enumeration |
| ORI-03 | Every CONDITIONAL region edge with/without contract | Apply tuple | Contracted case commits; missing contract rejects/warns | Exhaustive matrix plus issue assertion |
| ORI-04 | Every direct Front/Back edge | Attempt edit/import | Rejected atomically with ORIENTATION_EDGE_FORBIDDEN | Model/import assertions |
| ORI-05 | Generated Cartesian product of torso, pelvis, arm_L/R, leg_L/R in three body orientations plus both head states (1,458 tuples), with conditional transition contracts present and absent | Validate every tuple; repeat with simultaneous bridge edges and one deliberately invalid edge | Expected validity equals the formal tree-edge/head matrices for every tuple; all-valid graph commits; any one forbidden/unsupported edge rejects the entire edit atomically and identifies that edge; no combination is skipped | Generated exhaustive model test with tuple count, validity-class counts, issue codes, and conditional-asset fixtures |
| HEAD-01 | Front/3/4/Back × regular/back | Apply head presentation | Only matrix-legal pairs commit; no third family | Exhaustive head matrix |
| MIR-01 | Asymmetric pose/garment/anchors | Presentation reflect, then semantic mirror | Reflect preserves IDs; mirror swaps declared L/R semantics | State and visual assertions |
| SCL-01 | Min/nominal/max positive scale | Scale character | Uniform, relationships preserved, no profile mutation | Bounds and state checks |
| PROF-01 | Same pose on male/female and third synthetic profile | Switch profile | IDs/pose preserved; binds/art/fits resolve; warnings explicit | Parameterized profile test |
| ART-01 | Replacement artwork with same contract | Swap artwork set | Mechanics, pose, anchors, garments remain stable | Golden pivots/bounds and interaction |
| EXP-01 | Bounded lean/reach/crouch/arch/crunch/twist/weight-shift/asymmetry sweep | Traverse semantic body-mass and limb states | No hierarchy failure; connection-zone escapes and unsupported presentation are diagnosed; anatomy review recorded | Parameterized sweep plus continuity review |
| ILL-01 | Same semantic sweep under rigid, corrective/mask, and optional bounded-deformation presentation | Compare seams, silhouette, overlap, body-mass relation, and corrective continuity | Requested pose identical; presentation mode explicit; improvement/failure localized; no complete-pose substitution | Visual sheet, state comparison, owner review |
| ILL-02 | Shoulder, hip, elbow, knee, waist connection zones at neutral and extremes | Sweep through supported and unsupported bands | Safe overlap/masks/correctives preserve continuity or emit explicit unresolved state | Bounds/mask diagnostics plus visual review |
| FSH-01 | One limb aimed side/near/far with endpoint variants | Apply bounded projection states | Length/width compensation and endpoint direction remain coherent; unsupported states warn | State tests plus visual/owner review |
| GAR-01 | Shirt/trousers/coat examples on both profiles | Equip, pose, change orientation/state | Semantic pieces follow; no fixed-canvas drift | Model and render cases |
| GAR-02 | Cross-joint sleeves/trousers/coat | Flex joint across bands | One primary owner; secondary seam/mask/corrective resolves | Transform/render assertions |
| MSK-01 | Skirt/coat coverage | Hide/reveal legs and remove garment | Body state unchanged and restored; masks in correct space | Pixel/render plus state comparison |
| LAY-01 | Arm/sleeve/torso, hand/prop, coat panels | Change semantic over/under relation | Deterministic topological order and correct coverage | Graph and render assertions |
| LAY-02 | Deliberate render cycle | Commit edit and export | Last valid plan preserved; cycle diagnosed; export blocked | Graph/UI/export tests |
| FALL-01 | Missing garment/body variant or mask | Load/edit supported semantic state | Declared fallback only; state preserved; no Front/Back inference | Issue and resolved/requested state assertions |
| PROP-01 | Prop attached to grip/palm fallback | Pose and transfer | Prop relation stays local and semantic | Round trip and render |
| INT-01 | Two characters with hand/contact/look-at relation | Pose both, move roots, transfer | Instance/anchor relation and constraints preserved | Multi-instance round trip |
| SAVE-01 | Complete character snapshot | Save, load into clean state, save again | Canonical semantic equivalence; no editor/camera leak | Deep semantic comparison |
| XFER-01 | Two-character snapshot with garments/prop | Transfer to Placer and change panel state | Internal snapshot byte/semantic stable; panel data additive | Integration test |
| VER-01 | Compatible minor, unknown optional, unknown required major | Load | Migrate/preserve optional; required major atomic reject/read-only | Version matrix |
| BAD-01 | Missing field, unknown ID, invalid number, partial JSON | Load | No partial mutation; path/code/severity/repair issue | Fuzz/fixture suite |
| FALL-02 | Draft reevaluate and published frozen fallback | Asset availability changes across load | Mode-specific deterministic behavior; requested state retained | Versioned asset fixture |
| OUT-01 | Valid and unresolved character | Export | No diagnostics; valid export correct; required unresolved blocks | Pixel/output inspection |
| CORP-01 | Declarative source package with pose, optional mask, embedded metadata, and QA files | Inventory without package-specific code | Poses registered once; QA excluded; optional fields preserved; count/hash mismatch rejects atomically | Synthetic fourth-package automated test; current descriptor boundary TESTED |
| CORP-02 | All registered pose-corpus entries | Generate fixed-canvas candidates | RGBA/canvas/hash deterministic; alpha border zero; transparent RGB cleared; threshold-1 foreground remains inside safety margin | 123-file automated verification; current candidate transform TESTED |
| CORP-03 | Proposal, override, and resolved-entry layers | Inspect or author correction | Generated evidence remains inspectable; override is data; unresolved cannot masquerade as resolved | JSON Schema plus record enumeration; empty override boundary TESTED, author workflow not validated |
| CORP-04 | Front, 3/4, profile, rear-three-quarter, and rear observations | Map observed projection | Profile/rear-three-quarter remain reference-only; canonical orientation and anatomical L/R are not guessed | Metadata enumeration TESTED; human orientation correctness not validated |
| CORP-05 | Cross-set neutral and stress references | Review scale, ground, root and source defects | Capture-scale discontinuities and defects are visible; no raster candidate is promoted by visual similarity alone | Eight generated QA sheets; visual inspection performed, owner validation open |

## Combinatorial gate questions

For every primitive: what combinations become possible; does it work for both initial and a third profile; can art change independently; can garments attach without body hacks; do orientation and reload preserve it; can props/characters relate; what happens missing assets; and is invalid state prevented, warned, or corrupted?

## Designed acceptance

The architecture passes at designed level only if every row has a defined state location, validation/fallback behavior, and future oracle. Runtime implementation later must not mark the whole matrix TESTED after executing only representative cases.
