from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
VERIFICATION_SHA = "ab472cd4d7e7886cfa70aa9cc7ffdd7695568e36"
BASELINE = "baselines/canonical_base_body_rig_v0_1"


class CanonicalRuntimeStructure(unittest.TestCase):
    def test_runtime_exists_outside_preserved_baseline(self) -> None:
        expected = {
            "app/index.html",
            "app/styles.css",
            "app/model.js",
            "app/rig-definition.js",
            "app/runtime.js",
            "tests/runtime.html",
            "tests/runtime-browser-tests.js",
        }
        missing = [path for path in expected if not (REPOSITORY / path).is_file()]
        self.assertEqual(missing, [])

    def test_inherited_baseline_has_no_diff_from_verification_commit(self) -> None:
        result = subprocess.run(
            ["git", "diff", "--exit-code", VERIFICATION_SHA, "--", BASELINE],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_runtime_declares_required_state_and_controls(self) -> None:
        model = (REPOSITORY / "app/model.js").read_text(encoding="utf-8")
        runtime = (REPOSITORY / "app/runtime.js").read_text(encoding="utf-8")
        index = (REPOSITORY / "app/index.html").read_text(encoding="utf-8")
        for boundary in ("pose", "character", "camera", "editor"):
            self.assertIn(f"{boundary}:", model)
        for control_id in (
            "fit-body",
            "zoom-100",
            "reset-view",
            "reset-pose",
            "reset-character",
            "reset-all",
        ):
            self.assertIn(f'id="{control_id}"', index)
        self.assertIn("pointerInParentRigSpace", runtime)
        self.assertIn("visualToSemantic", runtime)

    def test_pose_serialization_excludes_workspace_state(self) -> None:
        model = (REPOSITORY / "app/model.js").read_text(encoding="utf-8")
        serialization = model.split("export function serializePose", 1)[1].split(
            "export function deepClone", 1
        )[0]
        self.assertNotIn("camera:", serialization)
        self.assertNotIn("character:", serialization)
        self.assertNotIn("editor:", serialization)


if __name__ == "__main__":
    unittest.main()
