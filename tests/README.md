# Inherited Rig Verification

These tests treat `baselines/canonical_base_body_rig_v0_1/` as an immutable external system. They do not import, regenerate, or modify baseline source or assets.

Run the reproducible static/structural checks from the repository root:

```text
python tests/verify_inherited_rig.py
```

Print the calculated repository-native evidence as JSON:

```text
python tests/verify_inherited_rig.py --json
```

The browser interaction matrix is recorded in the corresponding chronological pass report. `fixtures/valid-pose.json` and `fixtures/invalid-pose.json` exist only for bounded load-path verification.

## Canonical Runtime Tests

Run the dependency-free model, baseline, and canonical-structure checks from the repository root:

```text
npm test
```

Serve the repository and open the self-running browser harness:

```text
python -m http.server 8000 --bind 127.0.0.1
http://127.0.0.1:8000/tests/runtime.html
```

The harness loads the real [`app/`](../app/) runtime in a same-origin frame and exercises startup, all-view fitting, state separation, semantic view mapping, synthetic pointer manipulation, hierarchy propagation, resets, persistence boundaries, and compatibility/depth contracts. A green result proves the tested mechanical behaviors; it does not establish touch/mobile usability or creative-workflow validation.

## Canonical Pose Corpus Tests

Run tracked contract, schema, inventory, metadata, and deterministic image-operation checks with:

```text
python tests/verify_pose_corpus.py
```

That command intentionally skips checks requiring external user-supplied archives or generated rasters. Run the complete suite with:

```text
python tests/verify_pose_corpus.py --source-directory <directory-containing-zips> --artifact-root <generated-artifact-root>
```

The full suite verifies 123 archive mappings and hashes, 123 candidate files and hashes, fixed RGBA canvas, alpha borders, cleared transparent RGB, independently recomputed decoded-pixel hashes and safety margins, root/ground round trips, cross-record hashes and JSON Pointers, eight QA artifacts and sidecars, the Set C replacement-scale regression, proposal/override/entry schemas, and two concurrent synthetic future packages through the full pipeline. The synthetic run covers colliding basenames, a successful no-manifest package, a generic entry prefix, runtime descriptor-schema enforcement, unsafe path and ordinal-bound rejection, global calibration-ID rejection, reviewed override preservation/application, and stale-base rejection. Passing these checks does not resolve the real corpus's anatomical landmarks, approve the body profile, accept renders, or establish modular-character workflow validation.
