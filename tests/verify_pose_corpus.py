from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
import zipfile
from io import BytesIO
from pathlib import Path

import numpy as np
from jsonschema import Draft202012Validator
from PIL import Image, ImageDraw

REPOSITORY = Path(__file__).resolve().parents[1]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from tools.pose_corpus.contracts import (
    CORPUS_ID,
    ENTRY_SCHEMA_VERSION,
    LANDMARK_IDS,
)
from tools.pose_corpus.image_ops import (
    alpha_bbox,
    decoded_pixel_sha256,
    place_on_canvas,
    resize_premultiplied_linear,
)
from tools.pose_corpus.inventory import (
    CorpusInputError,
    _parse_identity,
    canonical_json_sha256,
    collect_inventory,
    sha256_file,
)
from tools.pose_corpus.pipeline import run_full


CORPUS_ROOT = REPOSITORY / "pose-corpus" / "canonical-v0_1"
ARTIFACT_ROOT: Path | None = None
ARTIFACT_SET_ROOTS: dict[str, Path] = {}
SOURCE_DIRECTORY: Path | None = None
EXPECTED_REGISTERED = 132
EXPECTED_TRANSFORM_QA_PASSED = 131


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def install_source_config_schema(repository: Path) -> None:
    source = CORPUS_ROOT / "schemas/source-package-config.schema.json"
    destination = (
        repository
        / "pose-corpus/canonical-v0_1/schemas/source-package-config.schema.json"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())


def png_bytes(width: int, height: int, variant: int) -> bytes:
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    if variant == 4:
        draw.rectangle((3, 3, width - 4, height - 4), fill=(128, 128, 128, 255))
    draw.ellipse(
        (width * 0.35, height * 0.08, width * 0.65, height * 0.28),
        fill=(150 + variant * 10, 80, 60, 255),
    )
    draw.rectangle(
        (width * 0.40, height * 0.24, width * 0.60, height * 0.72),
        fill=(210, 120, 100, 255),
    )
    draw.line(
        (width * 0.45, height * 0.70, width * 0.35, height * 0.94),
        fill=(210, 120, 100, 255),
        width=max(2, width // 12),
    )
    draw.line(
        (width * 0.55, height * 0.70, width * 0.65, height * 0.94),
        fill=(210, 120, 100, 255),
        width=max(2, width // 12),
    )
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


class ImageOperationTests(unittest.TestCase):
    def test_premultiplied_resize_is_deterministic_and_clears_transparent_rgb(self) -> None:
        source = np.zeros((8, 8, 4), dtype=np.uint8)
        source[:, :, :3] = (0, 255, 0)
        source[2:6, 2:6] = (255, 0, 0, 255)
        first = resize_premultiplied_linear(source, (17, 13))
        second = resize_premultiplied_linear(source, (17, 13))
        self.assertTrue(np.array_equal(first, second))
        self.assertTrue(np.all(first[first[:, :, 3] == 0, :3] == 0))
        edge = first[(first[:, :, 3] > 0) & (first[:, :, 3] < 255)]
        self.assertGreater(len(edge), 0)
        self.assertGreater(float(edge[:, 0].mean()), float(edge[:, 1].mean()))

    def test_transparent_source_padding_is_not_reported_as_content_clipping(self) -> None:
        source = np.zeros((20, 20, 4), dtype=np.uint8)
        source[6:14, 6:14] = (255, 0, 0, 255)
        canvas, clipped = place_on_canvas(source, (16, 16), (-2, -2))
        self.assertFalse(clipped)
        self.assertEqual(int(canvas[:, :, 3].sum()), 8 * 8 * 255)


class FuturePackageDescriptorTests(unittest.TestCase):
    def test_multiple_future_packages_ingest_through_data_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            source_directory = root / "sources"
            config_path = (
                repository
                / "pose-corpus"
                / "canonical-v0_1"
                / "spec"
                / "source-packages.json"
            )
            config_path.parent.mkdir(parents=True)
            install_source_config_schema(repository)
            source_directory.mkdir()
            archive_path = source_directory / "synthetic_package_d.zip"
            image_data = {
                f"{index:02d}_clip_f{index:03d}_{label}.png": png_bytes(
                    48 + index * 3, 90 + index * 5, index
                )
                for index, label in enumerate(
                    ("neutral", "wide_overhead", "profile", "opaque_failure"), 1
                )
            }
            manifest = {
                "records": [
                    {
                        "file": name,
                        "unknownOptionalField": {"preserved": True},
                    }
                    for name in image_data
                ]
            }
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
                for name, data in image_data.items():
                    archive.writestr(f"poses/{name}", data)
                profile_name = sorted(image_data)[2]
                with Image.open(BytesIO(image_data[profile_name])) as profile:
                    mask_buffer = BytesIO()
                    profile.getchannel("A").save(mask_buffer, format="PNG")
                archive.writestr(f"masks/{profile_name}", mask_buffer.getvalue())
                archive.writestr("qa/contact.png", png_bytes(64, 64, 1))
                archive.writestr("manifest.json", json.dumps(manifest))
            collision_basename = sorted(image_data)[0]
            extra_archive_path = source_directory / "synthetic_package_e.zip"
            extra_image = png_bytes(72, 144, 2)
            with zipfile.ZipFile(
                extra_archive_path, "w", zipfile.ZIP_DEFLATED
            ) as archive:
                archive.writestr(f"poses/{collision_basename}", extra_image)
            opaque_name = sorted(image_data)[3]
            opaque_hash = hashlib.sha256(image_data[opaque_name]).hexdigest()
            config = {
                "schemaVersion": "2d-doll-pose-corpus-source-config-0.1",
                "corpusId": CORPUS_ID,
                "sourceSets": [
                    {
                        "sourceSetId": "synthetic_package_d_v1",
                        "pathKey": "set_d",
                        "entryPrefix": "set_d_pose_",
                        "archiveFilename": archive_path.name,
                        "archiveSha256": sha256_file(archive_path),
                        "expectedPoseCount": 4,
                        "sourceManifestPath": "manifest.json",
                        "filenamePattern": "^(?P<ordinal>\\d{2})_clip_f(?P<frame>\\d{3})_(?P<label>.+)\\.png$",
                        "layers": [
                            {
                                "layerId": "rgba",
                                "role": "source_native_rgba",
                                "prefix": "poses/",
                                "suffix": ".png",
                                "depth": 2,
                                "mechanicsInput": True,
                                "normalizationInput": True,
                            },
                            {
                                "layerId": "optional_mask",
                                "role": "source_alpha_mask",
                                "prefix": "masks/",
                                "suffix": ".png",
                                "depth": 2,
                                "mechanicsInput": False,
                                "normalizationInput": False,
                                "optional": True,
                            },
                        ],
                        "calibrationGroups": [
                            {
                                "groupId": "synthetic_capture",
                                "matchPattern": ".*",
                                "referenceBasenames": [sorted(image_data)[0]],
                                "confidence": "high",
                                "rasterSelectionEvidence": True,
                            }
                        ],
                        "manualProjectionDirection": "right",
                        "knownIssues": [
                            {
                                "memberPath": f"poses/{opaque_name}",
                                "sourceSha256": opaque_hash,
                                "code": "SYNTHETIC_OPAQUE_FAILURE",
                                "severity": "error",
                                "disposition": "blocked_source_defect",
                                "detail": "Synthetic expected failure",
                            }
                        ],
                        "unresolvedClaims": [],
                    },
                    {
                        "sourceSetId": "synthetic_package_e_v1",
                        "pathKey": "synthetic_extra",
                        "entryPrefix": "synthetic_extra_pose_",
                        "archiveFilename": extra_archive_path.name,
                        "archiveSha256": sha256_file(extra_archive_path),
                        "expectedPoseCount": 1,
                        "sourceManifestPath": None,
                        "filenamePattern": "^(?P<ordinal>\\d{2})_clip_f(?P<frame>\\d{3})_(?P<label>.+)\\.png$",
                        "layers": [
                            {
                                "layerId": "rgba",
                                "role": "source_native_rgba",
                                "prefix": "poses/",
                                "suffix": ".png",
                                "depth": 2,
                                "mechanicsInput": True,
                                "normalizationInput": True,
                            }
                        ],
                        "calibrationGroups": [
                            {
                                "groupId": "synthetic_extra_capture",
                                "matchPattern": ".*",
                                "referenceBasenames": [collision_basename],
                                "confidence": "high",
                                "rasterSelectionEvidence": False,
                            }
                        ],
                        "manualProjectionDirection": "right",
                        "knownIssues": [],
                        "unresolvedClaims": [],
                    },
                ],
            }
            config_path.write_text(json.dumps(config), encoding="utf-8")
            first, _ = collect_inventory(repository, source_directory)
            second, _ = collect_inventory(repository, source_directory)
            self.assertEqual(first["counts"]["registered"], 5)
            self.assertEqual(canonical_json_sha256(first), canonical_json_sha256(second))
            self.assertEqual(
                [entry["entryId"] for entry in first["entries"]],
                [f"set_d_pose_{index:03d}" for index in range(1, 5)]
                + ["synthetic_extra_pose_001"],
            )
            self.assertEqual(first["entries"][3]["issues"][0]["code"], "SYNTHETIC_OPAQUE_FAILURE")
            self.assertTrue(
                first["entries"][0]["sourceManifestRecord"]["unknownOptionalField"]["preserved"]
            )
            evidence_paths = {
                item["archiveMemberPath"]
                for item in first["sourceSets"][0]["sourceEvidenceArtifacts"]
            }
            self.assertIn("qa/contact.png", evidence_paths)
            self.assertNotIn("qa/contact.png", {
                artifact["archiveMemberPath"]
                for entry in first["entries"]
                for artifact in entry["artifacts"]
            })
            extra_inventory_entry = next(
                entry
                for entry in first["entries"]
                if entry["entryId"] == "synthetic_extra_pose_001"
            )
            self.assertIsNone(extra_inventory_entry["sourceManifestRecord"])
            self.assertIsNone(first["sourceSets"][1]["sourceManifest"])
            artifact_root = root / "artifacts-first"
            with contextlib.redirect_stdout(io.StringIO()):
                result = run_full(repository, source_directory, artifact_root)
            self.assertEqual(result["counts"]["registered"], 5)
            self.assertEqual(result["counts"]["candidatesProduced"], 5)
            self.assertEqual(result["counts"]["blockedSourceDefectRenders"], 1)
            run_qa = load_json(
                repository
                / "pose-corpus/canonical-v0_1/qa/reports/run-summary.json"
            )
            self.assertEqual(run_qa["counts"]["transformQaPassed"], 5)
            self.assertEqual(run_qa["counts"]["qaArtifactCount"], 8)
            calibration = load_json(
                repository
                / "pose-corpus/canonical-v0_1/spec/calibration-evidence.json"
            )
            self.assertEqual(
                calibration["groups"]["synthetic_capture"]["observations"][0]["entryId"],
                "set_d_pose_001",
            )
            self.assertEqual(
                calibration["groups"]["synthetic_extra_capture"]["observations"][0]["entryId"],
                "synthetic_extra_pose_001",
            )
            resolved_extra = load_json(
                repository
                / "pose-corpus/canonical-v0_1/metadata/poses/synthetic_extra/synthetic_extra_pose_001.json"
            )
            entry_validator = Draft202012Validator(
                load_json(CORPUS_ROOT / "schemas/pose-entry.schema.json")
            )
            self.assertEqual([], list(entry_validator.iter_errors(resolved_extra)))

            override_path = (
                repository
                / "pose-corpus/canonical-v0_1/overrides/set_d/set_d_pose_001.json"
            )
            authored_override = load_json(override_path)
            authored_override["landmarks"] = {
                "pelvis_center": {
                    "availability": "visible",
                    "resolved": {"x": 0.0, "y": 0.0, "z": 0.0},
                    "reviewer": "synthetic_test",
                    "reason": "exercise non-destructive override precedence"
                }
            }
            authored_override["approval"] = {
                "status": "reviewed",
                "reviewer": "synthetic_test",
                "reason": "test fixture"
            }
            override_path.write_text(
                json.dumps(authored_override, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with contextlib.redirect_stdout(io.StringIO()):
                run_full(repository, source_directory, root / "artifacts-second")
            persisted_override = load_json(override_path)
            self.assertEqual(persisted_override, authored_override)
            resolved_entry = load_json(
                repository
                / "pose-corpus/canonical-v0_1/metadata/poses/set_d/set_d_pose_001.json"
            )
            self.assertEqual(
                resolved_entry["mechanics"]["landmarks"]["pelvis_center"]["resolved"],
                {"x": 0.0, "y": 0.0, "z": 0.0},
            )
            self.assertEqual(
                resolved_entry["mechanics"]["landmarks"]["pelvis_center"]["override"]["reviewer"],
                "synthetic_test",
            )

            authored_override["baseProposalSha256"] = "0" * 64
            override_path.write_text(
                json.dumps(authored_override, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "authored override is stale"):
                with contextlib.redirect_stdout(io.StringIO()):
                    run_full(repository, source_directory, root / "artifacts-stale")

            duplicate_group_config = json.loads(json.dumps(config))
            duplicate_group_config["sourceSets"][1]["calibrationGroups"][0][
                "groupId"
            ] = "synthetic_capture"
            config_path.write_text(
                json.dumps(duplicate_group_config), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                CorpusInputError, "duplicate calibration groupId"
            ):
                collect_inventory(repository, source_directory)

            for field, unsafe_value in (
                ("pathKey", "../../escape"),
                ("entryPrefix", "../escape_pose_"),
                ("archiveFilename", "../escape.zip"),
            ):
                unsafe_config = json.loads(json.dumps(config))
                unsafe_config["sourceSets"][1][field] = unsafe_value
                config_path.write_text(json.dumps(unsafe_config), encoding="utf-8")
                with self.subTest(field=field):
                    with self.assertRaisesRegex(
                        CorpusInputError, "source config schema violation"
                    ):
                        collect_inventory(repository, source_directory)

            ordinal_descriptor = {
                "entryPrefix": "future_pose_",
                "filenamePattern": "^(?P<ordinal>\\d+)_clip_f(?P<frame>\\d+)_(?P<label>.+)\\.png$",
            }
            for basename in (
                "0_clip_f0_zero.png",
                "1000_clip_f1000_overflow.png",
            ):
                with self.subTest(basename=basename):
                    with self.assertRaisesRegex(
                        CorpusInputError, "pose ordinal must be between 1 and 999"
                    ):
                        _parse_identity(ordinal_descriptor, basename)

    def test_descriptor_count_mismatch_rejects_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository = root / "repository"
            source_directory = root / "sources"
            config_path = repository / "pose-corpus/canonical-v0_1/spec/source-packages.json"
            config_path.parent.mkdir(parents=True)
            install_source_config_schema(repository)
            source_directory.mkdir()
            archive_path = source_directory / "bad.zip"
            image = png_bytes(48, 96, 1)
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("poses/01_clip_f001_neutral.png", image)
                archive.writestr("manifest.json", json.dumps({"records": []}))
            config = {
                "schemaVersion": "2d-doll-pose-corpus-source-config-0.1",
                "corpusId": CORPUS_ID,
                "sourceSets": [
                    {
                        "sourceSetId": "bad",
                        "pathKey": "bad",
                        "entryPrefix": "bad_pose_",
                        "archiveFilename": "bad.zip",
                        "archiveSha256": sha256_file(archive_path),
                        "expectedPoseCount": 2,
                        "sourceManifestPath": None,
                        "filenamePattern": "^(?P<ordinal>\\d{2})_clip_f(?P<frame>\\d{3})_(?P<label>.+)\\.png$",
                        "layers": [
                            {
                                "layerId": "rgba",
                                "role": "source_native_rgba",
                                "prefix": "poses/",
                                "suffix": ".png",
                                "depth": 2,
                                "mechanicsInput": True,
                                "normalizationInput": True,
                            }
                        ],
                        "calibrationGroups": [
                            {
                                "groupId": "bad_capture",
                                "matchPattern": ".*",
                                "referenceBasenames": [
                                    "01_clip_f001_neutral.png"
                                ],
                                "confidence": "high",
                                "rasterSelectionEvidence": True,
                            }
                        ],
                        "manualProjectionDirection": "right",
                        "knownIssues": [],
                        "unresolvedClaims": [],
                    }
                ],
            }
            config_path.write_text(json.dumps(config), encoding="utf-8")
            with self.assertRaisesRegex(
                CorpusInputError, "expected 2 poses; found 1"
            ):
                collect_inventory(repository, source_directory)


class RepositoryCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = load_json(CORPUS_ROOT / "corpus.json")
        cls.source = load_json(CORPUS_ROOT / "sources/source-manifest.json")
        cls.index = load_json(CORPUS_ROOT / "metadata/corpus-index.json")
        cls.profile = load_json(
            CORPUS_ROOT / "spec/base_female_v0_1.corpus-evidence.json"
        )
        cls.render = load_json(CORPUS_ROOT / "normalized/render-manifest.json")
        cls.qa = load_json(CORPUS_ROOT / "qa/reports/run-summary.json")

    def test_corpus_counts_and_schema_boundary(self) -> None:
        self.assertEqual(self.corpus["corpusId"], CORPUS_ID)
        self.assertFalse(self.corpus["runtimeBoundary"]["isReusablePose"])
        self.assertEqual(self.corpus["runtimeBoundary"]["compatiblePoseSchemaVersions"], [])
        self.assertEqual(self.index["counts"]["registered"], EXPECTED_REGISTERED)
        self.assertEqual(self.index["counts"]["reviewRequiredRenders"], 127)
        self.assertEqual(self.index["counts"]["blockedSourceDefectRenders"], 5)
        self.assertEqual(self.index["counts"]["acceptedRenders"], 0)

    def test_source_counts_and_known_issues(self) -> None:
        self.assertEqual(
            self.source["counts"]["bySourceSet"],
            {
                "set_a_edge_extremity_refined_v1": 28,
                "set_b_full_isolation_v1": 55,
                "set_c_edge_refined_green_cleaned_v1": 40,
                "set_d_pose_bg_removed_clean_v1": 9,
            },
        )
        issues = {
            entry["entryId"]: [issue["code"] for issue in entry["issues"]]
            for entry in self.source["entries"]
            if entry["issues"]
        }
        self.assertEqual(
            issues,
            {
                "set_b_pose_045": ["SOURCE_BACKDROP_RETAINED"],
                "set_b_pose_046": ["SOURCE_BACKDROP_SUSPECT"],
                "set_b_pose_051": ["SOURCE_ALPHA_CORRUPT"],
                "set_b_pose_052": ["SOURCE_ALPHA_CORRUPT"],
                "set_b_pose_053": ["SOURCE_ALPHA_CORRUPT"],
                "set_b_pose_054": ["SOURCE_ALPHA_CORRUPT"],
            },
        )
        self.assertNotIn("C:\\", json.dumps(self.source))

    def test_profile_is_provisional_and_measurements_are_honest(self) -> None:
        self.assertEqual(self.profile["approvalStatus"], "provisional_unapproved")
        self.assertFalse(self.profile["ownerApproved"])
        self.assertFalse(self.profile["workflowValidated"])
        self.assertFalse(
            self.profile["constraints"]["mayClaimCanonicalProportionContinuity"]
        )
        self.assertTrue(
            all(
                measurement["resolutionStage"] == "unresolved"
                for measurement in self.profile["measurements"].values()
            )
        )

    def test_all_pose_entries_have_explicit_landmark_states(self) -> None:
        pose_paths = sorted((CORPUS_ROOT / "metadata/poses").glob("*/*.json"))
        self.assertEqual(len(pose_paths), EXPECTED_REGISTERED)
        for path in pose_paths:
            entry = load_json(path)
            self.assertEqual(entry["schemaVersion"], ENTRY_SCHEMA_VERSION)
            landmarks = entry["mechanics"]["landmarks"]
            self.assertEqual(set(landmarks), set(LANDMARK_IDS))
            for value in landmarks.values():
                self.assertIn(value["availability"], {"ambiguous", "unavailable"})
                self.assertIsNone(value["resolved"])
                self.assertTrue(value["unresolvedReason"])
            self.assertNotEqual(
                entry["mechanics"]["poseOrigin"]["landmarkId"], "rig_root"
            )

    def test_profile_and_rear_threequarter_are_not_coerced(self) -> None:
        pose_paths = sorted((CORPUS_ROOT / "metadata/poses").glob("*/*.json"))
        reference_only = 0
        for path in pose_paths:
            entry = load_json(path)
            orientation = entry["mechanics"]["orientation"]
            projection = orientation["observedProjection"]["projectionClass"]
            if projection in {"profile", "rear_three_quarter"}:
                reference_only += 1
                self.assertIsNone(orientation["canonicalBodyOrientationId"])
                self.assertEqual(orientation["canonicalMappingStatus"], "reference_only")
        self.assertGreater(reference_only, 0)

    def test_render_and_qa_manifests_cover_every_entry(self) -> None:
        self.assertEqual(len(self.render["renders"]), EXPECTED_REGISTERED)
        self.assertEqual(
            self.render["counts"]["producedCandidates"], EXPECTED_REGISTERED
        )
        self.assertEqual(
            self.render["counts"]["transformQaPassed"],
            EXPECTED_TRANSFORM_QA_PASSED,
        )
        self.assertEqual(self.qa["counts"]["registered"], EXPECTED_REGISTERED)
        self.assertEqual(self.qa["verdict"]["mechanicsStatus"], "review_required")
        self.assertEqual(self.qa["verdict"]["workflowValidationStatus"], "not_validated")
        self.assertGreaterEqual(self.qa["counts"]["qaArtifactCount"], 8)
        forbidden = {"RENDER_CLIPPED", "SAFE_MARGIN_VIOLATION", "TRANSPARENT_RGB_NOT_CLEARED"}
        self.assertFalse(
            forbidden
            & {
                issue["code"]
                for render in self.render["renders"]
                for issue in render["issues"]
            }
        )
        overflow = [
            issue
            for render in self.render["renders"]
            for issue in render["issues"]
            if issue["code"] == "CANONICAL_CANVAS_OVERFLOW_REVIEW_REQUIRED"
        ]
        self.assertEqual(len(overflow), 1)
        self.assertEqual(overflow[0]["entryId"], "set_d_pose_009")
        self.assertEqual(overflow[0]["offendingBoundaries"], ["top"])
        self.assertEqual(overflow[0]["boundaryOverflowPx"]["top"], 2)

    def test_machine_readable_contracts_validate_generated_records(self) -> None:
        schema_root = CORPUS_ROOT / "schemas"
        singleton_cases = {
            "source-package-config.schema.json": CORPUS_ROOT / "spec/source-packages.json",
            "source-manifest.schema.json": CORPUS_ROOT / "sources/source-manifest.json",
            "profile-evidence.schema.json": CORPUS_ROOT / "spec/base_female_v0_1.corpus-evidence.json",
            "render-manifest.schema.json": CORPUS_ROOT / "normalized/render-manifest.json",
            "corpus-index.schema.json": CORPUS_ROOT / "metadata/corpus-index.json",
            "corpus.schema.json": CORPUS_ROOT / "corpus.json",
            "qa-summary.schema.json": CORPUS_ROOT / "qa/reports/run-summary.json",
        }
        for schema_name, instance_path in singleton_cases.items():
            schema = load_json(schema_root / schema_name)
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(load_json(instance_path))

        collection_cases = {
            "pose-entry.schema.json": CORPUS_ROOT / "metadata/poses",
            "proposal.schema.json": CORPUS_ROOT / "metadata/proposals",
            "override.schema.json": CORPUS_ROOT / "overrides",
        }
        for schema_name, record_root in collection_cases.items():
            schema = load_json(schema_root / schema_name)
            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema)
            paths = sorted(record_root.glob("*/*.json"))
            self.assertEqual(len(paths), EXPECTED_REGISTERED)
            for path in paths:
                validator.validate(load_json(path))

    def test_static_contracts_are_parseable_and_match_measured_canvas(self) -> None:
        for path in sorted((CORPUS_ROOT / "spec").glob("*.json")):
            load_json(path)
        export = load_json(CORPUS_ROOT / "spec/export-contract.json")
        coordinate = load_json(CORPUS_ROOT / "spec/coordinate-space.json")
        self.assertEqual(export["canvas"]["widthPx"], self.render["canvas"]["widthPx"])
        self.assertEqual(export["canvas"]["heightPx"], self.render["canvas"]["heightPx"])
        self.assertEqual(export["canvas"]["bodyPixels"], self.render["canvas"]["bodyPixels"])
        self.assertEqual(coordinate["mechanicalSpace"]["origin"], "pelvis_center")

    def test_hash_graph_counts_and_json_pointers_are_internally_verifiable(self) -> None:
        self.assertEqual(
            self.index["indexSha256"],
            canonical_json_sha256({**self.index, "indexSha256": None}),
        )
        self.assertEqual(
            self.render["renderManifestSha256"],
            canonical_json_sha256(
                {**self.render, "renderManifestSha256": None}
            ),
        )
        self.assertEqual(
            self.qa["qaSummarySha256"],
            canonical_json_sha256({**self.qa, "qaSummarySha256": None}),
        )
        self.assertEqual(self.qa["corpusIndexSha256"], self.index["indexSha256"])
        self.assertEqual(
            self.qa["renderManifestSha256"], self.render["renderManifestSha256"]
        )

        source_entries = self.source["entries"]
        render_records = self.render["renders"]
        index_by_id = {item["entryId"]: item for item in self.index["entries"]}
        render_by_id = {item["entryId"]: item for item in render_records}
        pose_paths = sorted((CORPUS_ROOT / "metadata/poses").glob("*/*.json"))
        for pose_path in pose_paths:
            entry = load_json(pose_path)
            entry_id = entry["entryId"]
            index_record = index_by_id[entry_id]
            render = render_by_id[entry_id]
            entry_sha = canonical_json_sha256(entry)
            self.assertEqual(index_record["entrySha256"], entry_sha)
            self.assertEqual(render["inputHashes"]["resolvedMetadataSha256"], entry_sha)

            source_index = int(entry["sourceRecordRef"].rsplit("/", 1)[1])
            self.assertEqual(source_entries[source_index]["entryId"], entry_id)
            render_index = int(entry["renderRef"].rsplit("/", 1)[1])
            self.assertEqual(render_records[render_index]["entryId"], entry_id)

            proposal = load_json(CORPUS_ROOT / entry["annotationLayers"]["proposalRef"])
            override = load_json(CORPUS_ROOT / entry["annotationLayers"]["overrideRef"])
            self.assertEqual(
                proposal["proposalSha256"],
                canonical_json_sha256({**proposal, "proposalSha256": None}),
            )
            self.assertEqual(
                entry["annotationLayers"]["overrideSha256"],
                canonical_json_sha256(override),
            )
            self.assertEqual(
                render["renderRecordSha256"],
                canonical_json_sha256({**render, "renderRecordSha256": None}),
            )

        counts = self.index["counts"]
        self.assertEqual(counts["registered"], len(self.index["entries"]))
        self.assertEqual(
            counts["reviewRequiredRenders"],
            sum(
                item["acceptance"]["renderStatus"] == "review_required"
                for item in self.index["entries"]
            ),
        )
        self.assertEqual(
            counts["blockedSourceDefectRenders"],
            sum(
                item["acceptance"]["renderStatus"] == "blocked_source_defect"
                for item in self.index["entries"]
            ),
        )


class ExternalArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if ARTIFACT_ROOT is None and not ARTIFACT_SET_ROOTS:
            raise unittest.SkipTest("external artifact roots not supplied")
        cls.artifact_root = ARTIFACT_ROOT
        cls.artifact_set_roots = ARTIFACT_SET_ROOTS
        cls.index = load_json(CORPUS_ROOT / "metadata/corpus-index.json")
        cls.render = load_json(CORPUS_ROOT / "normalized/render-manifest.json")
        cls.qa = load_json(CORPUS_ROOT / "qa/reports/run-summary.json")

    def _root_for_artifact_set(self, artifact_set_id: str | None) -> Path | None:
        if artifact_set_id is None:
            return self.artifact_root
        return self.artifact_set_roots.get(artifact_set_id)

    def test_all_candidate_renders_match_manifest(self) -> None:
        canvas = self.render["canvas"]
        checked = 0
        for render in self.render["renders"]:
            root = self._root_for_artifact_set(
                render["output"].get("artifactSetId")
            )
            if root is None:
                continue
            checked += 1
            path = root / Path(render["output"]["logicalPath"])
            self.assertTrue(path.is_file(), path)
            self.assertEqual(sha256_file(path), render["output"]["sha256"])
            with Image.open(path) as image:
                self.assertEqual(image.mode, "RGBA")
                self.assertEqual(image.size, (canvas["widthPx"], canvas["heightPx"]))
                rgba = np.asarray(image, dtype=np.uint8)
            alpha = rgba[:, :, 3]
            self.assertEqual(int(alpha[0].max()), 0)
            self.assertEqual(int(alpha[-1].max()), 0)
            self.assertEqual(int(alpha[:, 0].max()), 0)
            self.assertEqual(int(alpha[:, -1].max()), 0)
            self.assertTrue(np.all(rgba[alpha == 0, :3] == 0))
            self.assertEqual(
                decoded_pixel_sha256(rgba), render["output"]["decodedPixelSha256"]
            )
            bbox = alpha_bbox(alpha, 1)
            self.assertIsNotNone(bbox)
            assert bbox is not None
            margin = canvas["safeMarginPx"]
            if render["qaEvidence"]["foregroundInsideSafeRectangle"]:
                self.assertGreaterEqual(bbox[0], margin)
                self.assertGreaterEqual(bbox[1], margin)
                self.assertLessEqual(bbox[2], canvas["widthPx"] - margin)
                self.assertLessEqual(bbox[3], canvas["heightPx"] - margin)
            else:
                overflow = [
                    issue
                    for issue in render["issues"]
                    if issue["code"]
                    == "CANONICAL_CANVAS_OVERFLOW_REVIEW_REQUIRED"
                ]
                self.assertEqual(len(overflow), 1)
                self.assertEqual(overflow[0]["disposition"], "review_required")

            entry = load_json(CORPUS_ROOT / render["mechanicsRef"])
            transform = entry["normalizationCandidate"]["transform"]
            self.assertLessEqual(transform["rootRoundTripErrorPx"], 0.5)
            self.assertLessEqual(transform["groundRoundTripErrorPx"], 0.5)
            proposal = load_json(
                CORPUS_ROOT / entry["annotationLayers"]["proposalRef"]
            )
            root = proposal["placement"]["pelvisCenterNormalizationPx"]
            ground = proposal["placement"]["groundNormalizationYPx"]
            scale = transform["isotropicScale"]
            self.assertLessEqual(
                abs(
                    root["x"] * scale
                    + transform["translateXPx"]
                    - canvas["originXPx"]
                ),
                0.5,
            )
            self.assertLessEqual(
                abs(
                    ground * scale
                    + transform["translateYPx"]
                    - canvas["groundYPx"]
                ),
                0.5,
            )
        self.assertGreater(checked, 0)

    def test_generated_qa_artifacts_match_manifest(self) -> None:
        checked = 0
        for artifact in self.qa["qaArtifacts"]:
            root = self._root_for_artifact_set(artifact.get("artifactSetId"))
            if root is None:
                continue
            checked += 1
            path = root / Path(artifact["logicalPath"])
            sidecar = root / Path(artifact["sidecarLogicalPath"])
            self.assertEqual(sha256_file(path), artifact["sha256"])
            self.assertEqual(sha256_file(sidecar), artifact["sidecarSha256"])
        self.assertGreater(checked, 0)

    def test_external_run_manifests_describe_their_own_artifact_sets(self) -> None:
        if self.artifact_root is not None:
            run = load_json(self.artifact_root / "run-manifest.json")
            self.assertEqual(run["corpusId"], CORPUS_ID)
            self.assertNotIn(str(self.artifact_root), json.dumps(run))
        for artifact_set_id, root in self.artifact_set_roots.items():
            run = load_json(root / "run-manifest.json")
            self.assertEqual(run["corpusId"], CORPUS_ID)
            self.assertEqual(run["artifactSetId"], artifact_set_id)
            self.assertEqual(run["operation"], "frozen_ingestion")
            self.assertEqual(run["referenceScope"], "package_local")
            self.assertNotIn(str(root), json.dumps(run))
            local_render = load_json(root / "normalized/render-manifest.json")
            local_index = load_json(root / "metadata/corpus-index.json")
            local_qa = load_json(root / "qa/reports/run-summary.json")
            self.assertEqual(
                run["packageRenderManifestSha256"],
                local_render["renderManifestSha256"],
            )
            self.assertEqual(
                run["packageCorpusIndexSha256"], local_index["indexSha256"]
            )
            self.assertEqual(
                run["packageQaSummarySha256"], local_qa["qaSummarySha256"]
            )

    def test_set_c_replacement_scale_does_not_collapse(self) -> None:
        if self.artifact_root is None:
            raise unittest.SkipTest("baseline A-C artifact root not supplied")
        renders = {item["entryId"]: item for item in self.render["renders"]}
        minimum_height = round(self.render["canvas"]["bodyPixels"] * 0.75)
        for entry_id in ("set_c_pose_039", "set_c_pose_040"):
            alpha_bbox = renders[entry_id]["qaEvidence"]["alphaBboxByThreshold"]["8"]
            self.assertGreaterEqual(alpha_bbox[3] - alpha_bbox[1], minimum_height)


class ExternalSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if SOURCE_DIRECTORY is None:
            raise unittest.SkipTest("external source directory not supplied")

    def test_external_archive_hashes_match_tracked_manifest(self) -> None:
        source = load_json(CORPUS_ROOT / "sources/source-manifest.json")
        for source_set in source["sourceSets"]:
            archive = source_set["archive"]
            self.assertEqual(
                sha256_file(SOURCE_DIRECTORY / archive["filename"]), archive["sha256"]
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path)
    parser.add_argument(
        "--artifact-set-root",
        action="append",
        default=[],
        metavar="ARTIFACT_SET_ID=PATH",
    )
    parser.add_argument("--source-directory", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    ARTIFACT_ROOT = args.artifact_root.resolve() if args.artifact_root else None
    for assignment in args.artifact_set_root:
        artifact_set_id, separator, path = assignment.partition("=")
        if not separator or not artifact_set_id or not path:
            raise SystemExit(
                "--artifact-set-root requires ARTIFACT_SET_ID=PATH"
            )
        if artifact_set_id in ARTIFACT_SET_ROOTS:
            raise SystemExit(f"duplicate artifact-set ID: {artifact_set_id}")
        ARTIFACT_SET_ROOTS[artifact_set_id] = Path(path).resolve()
    SOURCE_DIRECTORY = (
        args.source_directory.resolve() if args.source_directory else None
    )
    unittest.main(argv=[__file__])
