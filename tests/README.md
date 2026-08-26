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
