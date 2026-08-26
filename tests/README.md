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
