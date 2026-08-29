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
python tests/verify_frozen_ingestion.py
```

That command intentionally skips checks requiring external user-supplied archives or generated rasters. Run the complete suite with:

```text
python tests/verify_pose_corpus.py --source-directory <directory-containing-zips> --artifact-root <baseline-generated-artifact-root> --artifact-set-root <artifact-set-id>=<frozen-ingestion-artifact-root>
```

The tracked suite verifies 132 registered records, fixed RGBA canvas, cross-record hashes and JSON Pointers, proposal/override/entry schemas, 131 transform-QA passes, and Set D pose 009's structured safe-margin review. Repeat `--artifact-set-root ID=PATH` for each external frozen-ingestion artifact set; records and QA artifacts are resolved through their `artifactSetId`, while `--artifact-root` addresses the original A–C calibration artifact root.

The architecture suite proves selected-package ingestion cannot derive or drift the pinned v0.1 canvas, preserves historical per-entry bytes and aggregate prefixes, renders only new entries, handles physical and safe-margin overflow explicitly, resolves package-local references, rolls back coordinated repository/artifact failure, rejects duplicates, and produces deterministic metadata from equivalent baselines. The calibration tests still cover colliding basenames, a successful no-manifest package, generic entry prefixes, runtime descriptor-schema enforcement, unsafe path and ordinal-bound rejection, global calibration-ID rejection, reviewed override preservation/application, and stale-base rejection. Passing these checks does not resolve anatomical landmarks, approve the body profile, accept renders, or establish modular-character workflow validation.
