from __future__ import annotations

import argparse
import json
import re
import unittest
from pathlib import Path

from PIL import Image, ImageChops


REPOSITORY = Path(__file__).resolve().parents[1]
BASELINE = REPOSITORY / "baselines" / "canonical_base_body_rig_v0_1"
MANIFEST_PATH = BASELINE / "manifest.json"
MANIFEST_DATA_PATH = BASELINE / "manifest-data.js"
APP_PATH = BASELINE / "app.js"
INDEX_PATH = BASELINE / "index.html"
VALIDATOR_PATH = BASELINE / "docs" / "validate_rig.py"

EXPECTED_VIEWS = ("front", "three_quarter", "back")
EXPECTED_PARTS = {
    "pelvis",
    "mid_torso",
    "chest",
    "upper_arm_L",
    "forearm_L",
    "hand_L",
    "upper_arm_R",
    "forearm_R",
    "hand_R",
    "thigh_L",
    "calf_L",
    "foot_L",
    "thigh_R",
    "calf_R",
    "foot_R",
}


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_embedded_manifest() -> dict:
    source = MANIFEST_DATA_PATH.read_text(encoding="utf-8").strip()
    match = re.fullmatch(r"window\.RIG_MANIFEST\s*=\s*(.*);", source, re.DOTALL)
    if not match:
        raise AssertionError("manifest-data.js wrapper is not recognized")
    return json.loads(match.group(1))


def runtime_canvas(index_source: str) -> tuple[int, int]:
    match = re.search(
        r'<canvas\s+id="rigCanvas"\s+width="(\d+)"\s+height="(\d+)"',
        index_source,
    )
    if not match:
        raise AssertionError("runtime canvas dimensions were not found")
    return int(match.group(1)), int(match.group(2))


def runtime_scales(index_source: str, app_source: str) -> tuple[float, float, float]:
    slider_tag = re.search(r'<input\b[^>]*\bid="scaleSlider"[^>]*>', index_source)
    state = re.search(r"\bscale:([\d.]+)", app_source)
    if not slider_tag or not state:
        raise AssertionError("runtime scale contract was not found")

    def attribute(name: str) -> float:
        match = re.search(rf'\b{name}="([\d.]+)"', slider_tag.group(0))
        if not match:
            raise AssertionError(f"scale slider {name} attribute was not found")
        return float(match.group(1))

    minimum = attribute("min")
    maximum = attribute("max")
    html_default = attribute("value")
    state_default = float(state.group(1))
    if html_default != state_default:
        raise AssertionError("HTML and application scale defaults differ")
    return minimum, state_default, maximum


def view_alpha_bounds(manifest: dict, view_id: str) -> tuple[int, int, int, int]:
    union = Image.new("L", (manifest["canvas"]["width"], manifest["canvas"]["height"]))
    for part in manifest["views"][view_id]["parts"].values():
        with Image.open(BASELINE / part["assetAligned"]) as image:
            union = ImageChops.lighter(union, image.getchannel("A"))
    bounds = union.getbbox()
    if bounds is None:
        raise AssertionError(f"{view_id} has no visible pixels")
    return bounds


def calculate_screen_bounds(
    bounds: tuple[int, int, int, int],
    root: tuple[float, float],
    scale: float,
    canvas: tuple[int, int],
) -> tuple[float, float, float, float]:
    x0, y0, x1, y1 = bounds
    root_x, root_y = root
    canvas_w, canvas_h = canvas
    origin_x = canvas_w * 0.5
    origin_y = canvas_h * 0.94
    return (
        origin_x + scale * (x0 - root_x),
        origin_y + scale * (y0 - root_y),
        origin_x + scale * (x1 - root_x),
        origin_y + scale * (y1 - root_y),
    )


def collect_evidence() -> dict:
    manifest = load_manifest()
    embedded = load_embedded_manifest()
    app_source = APP_PATH.read_text(encoding="utf-8")
    index_source = INDEX_PATH.read_text(encoding="utf-8")
    validator_source = VALIDATOR_PATH.read_text(encoding="utf-8")
    canvas = runtime_canvas(index_source)
    scales = runtime_scales(index_source, app_source)

    view_evidence = {}
    for view_id in EXPECTED_VIEWS:
        view = manifest["views"][view_id]
        alpha_bounds = view_alpha_bounds(manifest, view_id)
        screen = {}
        for label, scale in zip(("minimum", "default", "maximum"), scales):
            bounds = calculate_screen_bounds(
                alpha_bounds,
                tuple(view["pivots"]["root"]),
                scale,
                canvas,
            )
            screen[label] = {
                "scale": scale,
                "bounds": [round(value, 2) for value in bounds],
                "fullyVisible": (
                    bounds[0] >= 0
                    and bounds[1] >= 0
                    and bounds[2] <= canvas[0]
                    and bounds[3] <= canvas[1]
                ),
            }
        view_evidence[view_id] = {
            "alphaBounds": list(alpha_bounds),
            "screen": screen,
            "partCount": len(view["parts"]),
            "pivotCount": len(view["pivots"]),
        }

    limits = {
        view_id: {
            part_id: part["rotationLimitsDeg"]
            for part_id, part in manifest["views"][view_id]["parts"].items()
        }
        for view_id in EXPECTED_VIEWS
    }
    z_indexes = {
        view_id: {
            part_id: part["zIndex"]
            for part_id, part in manifest["views"][view_id]["parts"].items()
        }
        for view_id in EXPECTED_VIEWS
    }

    startup_call = app_source.index("buildControls(); bind(); render();")
    declarations = {
        "presets": app_source.index("const presets="),
        "handleCache": app_source.index("let handleCache=[]"),
        "drag": app_source.index("let drag=null"),
    }
    control_ids = set(re.findall(r'id="([^"]+)"', index_source))
    state_match = re.search(r"const state=(\{[^\n]+\});", app_source)
    state_source = state_match.group(1) if state_match else ""

    return {
        "manifestParity": manifest == embedded,
        "schemaVersion": manifest["schemaVersion"],
        "sourceCanvas": manifest["canvas"],
        "runtimeCanvas": {"width": canvas[0], "height": canvas[1]},
        "stablePivotCount": len(manifest["stablePivotIds"]),
        "stablePivotIds": manifest["stablePivotIds"],
        "views": view_evidence,
        "rotationLimitsIdenticalAcrossViews": (
            limits["front"] == limits["three_quarter"] == limits["back"]
        ),
        "rotationLimits": limits["front"],
        "zIndexes": z_indexes,
        "startup": {
            "initialRenderBeforeDeclarations": all(
                startup_call < position for position in declarations.values()
            ),
            "initializationOrderOffsets": {
                "initialRender": startup_call,
                **declarations,
            },
        },
        "implementedStateSource": state_source,
        "wholeCharacterXYControlsPresent": any(
            name in control_ids
            for name in ("bodyX", "bodyY", "rootX", "rootY", "moveDoll")
        ),
        "cameraControlsPresent": any(
            name in control_ids
            for name in ("cameraPan", "cameraZoom", "fitBody", "zoom100", "resetView")
        ),
        "staticDepthSortPresent": "zIndex-v.parts[b].zIndex" in app_source,
        "poseDependentDepthStatePresent": "depth" in state_source.lower(),
        "savePoseFields": [
            "schemaVersion",
            "viewId",
            "angles",
            "scale",
            "rootRotation",
            "flip",
        ],
        "validator": {
            "checksImageSize": "aligned.size!=(1000,1700)" in validator_source,
            "checksImageMode": "aligned.mode!='RGBA'" in validator_source,
            "checksNonemptyAlpha": "empty alpha" in validator_source,
            "checksViewsPartsPivotsAssets": all(
                token in validator_source
                for token in (
                    "view set mismatch",
                    "part set mismatch",
                    "pivot set mismatch",
                    "missing",
                )
            ),
            "launchesBrowser": any(
                token in validator_source.lower()
                for token in ("playwright", "selenium", "browser", "http.server")
            ),
            "checksConsole": "console" in validator_source.lower(),
        },
    }


class InheritedRigVerification(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = collect_evidence()

    def test_manifest_and_contract(self) -> None:
        self.assertTrue(self.evidence["manifestParity"])
        self.assertEqual(self.evidence["schemaVersion"], "canonical-body-rig-0.1")
        self.assertEqual(self.evidence["stablePivotCount"], 17)
        for view in self.evidence["views"].values():
            self.assertEqual(view["partCount"], len(EXPECTED_PARTS))
            self.assertEqual(view["pivotCount"], 17)

    def test_full_body_is_clipped_at_every_allowed_scale(self) -> None:
        for view_id, view in self.evidence["views"].items():
            for scale_name, result in view["screen"].items():
                with self.subTest(view=view_id, scale=scale_name):
                    self.assertFalse(result["fullyVisible"])
                    self.assertGreater(result["bounds"][3], 820)

    def test_startup_order_matches_known_failure_baseline(self) -> None:
        self.assertTrue(self.evidence["startup"]["initialRenderBeforeDeclarations"])

    def test_world_and_camera_controls_are_missing(self) -> None:
        self.assertFalse(self.evidence["wholeCharacterXYControlsPresent"])
        self.assertFalse(self.evidence["cameraControlsPresent"])

    def test_view_limits_are_raw_and_identical(self) -> None:
        self.assertTrue(self.evidence["rotationLimitsIdenticalAcrossViews"])

    def test_depth_is_static(self) -> None:
        self.assertTrue(self.evidence["staticDepthSortPresent"])
        self.assertFalse(self.evidence["poseDependentDepthStatePresent"])

    def test_structural_validator_has_no_runtime_coverage(self) -> None:
        validator = self.evidence["validator"]
        self.assertTrue(validator["checksViewsPartsPivotsAssets"])
        self.assertTrue(validator["checksImageSize"])
        self.assertTrue(validator["checksImageMode"])
        self.assertTrue(validator["checksNonemptyAlpha"])
        self.assertFalse(validator["launchesBrowser"])
        self.assertFalse(validator["checksConsole"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print calculated evidence")
    args = parser.parse_args()
    if args.json:
        print(json.dumps(collect_evidence(), indent=2, sort_keys=True))
        return
    unittest.main(argv=[__file__])


if __name__ == "__main__":
    main()
