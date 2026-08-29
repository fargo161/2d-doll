from __future__ import annotations

import contextlib
import hashlib
import io
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from io import BytesIO
from pathlib import Path
from unittest import mock

from PIL import Image, ImageDraw


REPOSITORY = Path(__file__).resolve().parents[1]
if str(REPOSITORY) not in sys.path:
    sys.path.insert(0, str(REPOSITORY))

from tools.pose_corpus.frozen_ingestion import (
    CanonicalCanvasOverflowError,
    FrozenIngestionError,
    run_frozen_ingestion,
)
from tools.pose_corpus.inventory import sha256_file
from tools.pose_corpus.pipeline import parse_args


CORPUS_RELATIVE = Path("pose-corpus/canonical-v0_1")
CORPUS_ROOT = REPOSITORY / CORPUS_RELATIVE
FROZEN_FIELDS = {
    "widthPx": 1536,
    "heightPx": 2112,
    "bodyPixels": 1728,
    "originXPx": 768,
    "groundYPx": 1984,
    "safeMarginPx": 87,
    "resampleSupportPx": 8,
    "roundingMultiplePx": 64,
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def synthetic_png(
    width: int,
    height: int,
    *,
    extreme: bool = False,
    top_extension: bool = False,
) -> bytes:
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    center = width // 2
    draw.ellipse(
        (center - 14, 12, center + 14, 42), fill=(190, 110, 90, 255)
    )
    draw.rectangle(
        (center - 18, 40, center + 18, height - 55), fill=(210, 125, 105, 255)
    )
    draw.line(
        (center - 8, height - 58, center - 18, height - 12),
        fill=(210, 125, 105, 255),
        width=9,
    )
    draw.line(
        (center + 8, height - 58, center + 18, height - 12),
        fill=(210, 125, 105, 255),
        width=9,
    )
    if extreme:
        draw.line((1, 70, width - 2, 70), fill=(210, 125, 105, 255), width=11)
    if top_extension:
        draw.line((center, 0, center, 14), fill=(45, 30, 25, 255), width=3)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def record_hashes(corpus_root: Path, set_pattern: str = "set_[abc]") -> dict[str, str]:
    paths = []
    for relative in ("metadata/poses", "metadata/proposals", "overrides"):
        paths.extend(
            path
            for path in (corpus_root / relative).glob(f"{set_pattern}/*.json")
            if path.is_file()
        )
    return {
        path.relative_to(corpus_root).as_posix(): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted(paths)
    }


def resolve_json_ref(root: Path, reference: str) -> object:
    relative, separator, fragment = reference.partition("#")
    path = root / relative
    if not path.is_file():
        raise AssertionError(f"missing referenced file: {reference}")
    value: object = read_json(path)
    if not separator:
        return value
    for token in fragment.lstrip("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def tree_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def install_repository_fixture(destination: Path) -> Path:
    corpus_root = destination / CORPUS_RELATIVE
    shutil.copytree(
        CORPUS_ROOT,
        corpus_root,
        ignore=shutil.ignore_patterns(".work"),
    )
    return corpus_root


def add_synthetic_descriptor(
    corpus_root: Path,
    archive_path: Path,
    *,
    source_set_id: str,
    path_key: str,
    entry_prefix: str,
    expected_count: int,
) -> None:
    config_path = corpus_root / "spec/source-packages.json"
    config = read_json(config_path)
    config["sourceSets"].append(
        {
            "sourceSetId": source_set_id,
            "pathKey": path_key,
            "entryPrefix": entry_prefix,
            "archiveFilename": archive_path.name,
            "archiveSha256": sha256_file(archive_path),
            "expectedPoseCount": expected_count,
            "sourceManifestPath": None,
            "filenamePattern": "^(?P<ordinal>\\d{3})_(?P<label>.+)\\.png$",
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
                    "groupId": f"{path_key}_capture",
                    "matchPattern": ".*",
                    "referenceBasenames": ["001_neutral.png"],
                    "confidence": "high",
                    "rasterSelectionEvidence": False,
                }
            ],
            "manualProjectionDirection": "right",
            "knownIssues": [],
            "unresolvedClaims": [],
        }
    )
    write_json(config_path, config)


def create_archive(
    path: Path,
    *,
    include_extreme: bool = False,
    include_safe_margin: bool = False,
) -> None:
    def write_member(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
        info = zipfile.ZipInfo(name, date_time=(2024, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, data)

    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        write_member(archive, "poses/001_neutral.png", synthetic_png(100, 200))
        if include_extreme:
            write_member(
                archive,
                "poses/002_extreme_extension.png",
                synthetic_png(520, 200, extreme=True),
            )
        if include_safe_margin:
            write_member(
                archive,
                "poses/002_tall_hair_extension.png",
                synthetic_png(100, 206, top_extension=True),
            )


class FrozenIngestionArchitectureTests(unittest.TestCase):
    def _run_fixture(
        self,
        root: Path,
        *,
        name: str,
        include_extreme: bool = False,
        include_safe_margin: bool = False,
    ) -> tuple[Path, Path, Path, str]:
        repository = root / f"repository-{name}"
        corpus_root = install_repository_fixture(repository)
        source_directory = root / f"sources-{name}"
        archive_path = source_directory / f"{name}.zip"
        create_archive(
            archive_path,
            include_extreme=include_extreme,
            include_safe_margin=include_safe_margin,
        )
        source_set_id = f"{name}_v1"
        add_synthetic_descriptor(
            corpus_root,
            archive_path,
            source_set_id=source_set_id,
            path_key=name,
            entry_prefix=f"{name}_pose_",
            expected_count=1 + int(include_extreme) + int(include_safe_margin),
        )
        return repository, corpus_root, source_directory, source_set_id

    def test_frozen_ingestion_preserves_canvas_and_existing_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository, corpus_root, source_directory, source_set_id = self._run_fixture(
                root, name="synthetic_frozen"
            )
            canvas_path = corpus_root / "spec/canvas.json"
            canvas_before = canvas_path.read_bytes()
            abc_before = record_hashes(corpus_root)
            source_before = read_json(corpus_root / "sources/source-manifest.json")
            render_before = read_json(corpus_root / "normalized/render-manifest.json")
            index_before = read_json(corpus_root / "metadata/corpus-index.json")
            artifact_root = root / "artifacts"

            with mock.patch(
                "tools.pose_corpus.resolve._derive_canvas",
                side_effect=AssertionError("frozen ingestion reached canvas derivation"),
            ):
                with contextlib.redirect_stdout(io.StringIO()):
                    result = run_frozen_ingestion(
                        repository,
                        source_directory,
                        artifact_root,
                        [source_set_id],
                    )

            self.assertEqual(canvas_path.read_bytes(), canvas_before)
            self.assertEqual(record_hashes(corpus_root), abc_before)
            canvas = read_json(canvas_path)
            for field, expected in FROZEN_FIELDS.items():
                self.assertEqual(canvas[field], expected)
            self.assertEqual(result["canvas"], [1536, 2112])
            self.assertEqual(result["groundYPx"], 1984)
            self.assertEqual(result["bodyPixels"], 1728)

            source_after = read_json(corpus_root / "sources/source-manifest.json")
            render_after = read_json(corpus_root / "normalized/render-manifest.json")
            index_after = read_json(corpus_root / "metadata/corpus-index.json")
            self.assertEqual(
                source_after["entries"][: len(source_before["entries"])],
                source_before["entries"],
            )
            self.assertEqual(
                render_after["renders"][: len(render_before["renders"])],
                render_before["renders"],
            )
            self.assertEqual(
                index_after["entries"][: len(index_before["entries"])],
                index_before["entries"],
            )
            new_pngs = sorted(artifact_root.glob("review/previews/**/*.png"))
            self.assertEqual([path.name for path in new_pngs], ["synthetic_frozen_pose_001.png"])
            self.assertFalse(any("set_a_pose" in path.name for path in new_pngs))

            local_entries = sorted(
                artifact_root.glob("metadata/poses/**/*.json")
            )
            self.assertEqual(len(local_entries), 1)
            local_entry = read_json(local_entries[0])
            source_record = resolve_json_ref(
                artifact_root, local_entry["sourceRecordRef"]
            )
            self.assertEqual(source_record["entryId"], local_entry["entryId"])
            resolve_json_ref(artifact_root, local_entry["profileEvidenceRef"])
            resolve_json_ref(
                artifact_root,
                local_entry["annotationLayers"]["proposalRef"],
            )
            resolve_json_ref(
                artifact_root,
                local_entry["annotationLayers"]["overrideRef"],
            )
            render_record = resolve_json_ref(
                artifact_root, local_entry["renderRef"]
            )
            self.assertEqual(render_record["entryId"], local_entry["entryId"])
            resolve_json_ref(artifact_root, render_record["mechanicsRef"])
            self.assertTrue(
                (artifact_root / render_record["output"]["logicalPath"]).is_file()
            )
            local_render_manifest_path = (
                artifact_root / "normalized/render-manifest.json"
            )
            local_render_manifest = read_json(local_render_manifest_path)
            export_contract = (
                local_render_manifest_path.parent
                / local_render_manifest["exportContractRef"]
            ).resolve()
            self.assertTrue(export_contract.is_file())
            local_qa = read_json(artifact_root / "qa/reports/run-summary.json")
            for qa_artifact in local_qa["qaArtifacts"]:
                self.assertTrue(
                    (artifact_root / qa_artifact["logicalPath"]).is_file()
                )
            committed_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in artifact_root.rglob("*.json")
            )
            self.assertNotIn(str(root), committed_text)
            self.assertNotIn(str(source_directory), committed_text)

            state_after_first = {
                "canvas": canvas_path.read_bytes(),
                "abc": record_hashes(corpus_root),
                "source": (corpus_root / "sources/source-manifest.json").read_bytes(),
            }
            duplicate_artifact_root = root / "duplicate-artifacts"
            with self.assertRaisesRegex(FrozenIngestionError, "already registered"):
                with contextlib.redirect_stdout(io.StringIO()):
                    run_frozen_ingestion(
                        repository,
                        source_directory,
                        duplicate_artifact_root,
                        [source_set_id],
                    )
            self.assertFalse(duplicate_artifact_root.exists())
            self.assertEqual(canvas_path.read_bytes(), state_after_first["canvas"])
            self.assertEqual(record_hashes(corpus_root), state_after_first["abc"])
            self.assertEqual(
                (corpus_root / "sources/source-manifest.json").read_bytes(),
                state_after_first["source"],
            )

    def test_physical_overflow_produces_review_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository, corpus_root, source_directory, source_set_id = self._run_fixture(
                root, name="synthetic_overflow", include_extreme=True
            )
            canvas_path = corpus_root / "spec/canvas.json"
            canvas_before = canvas_path.read_bytes()
            abc_before = record_hashes(corpus_root)
            source_before = (corpus_root / "sources/source-manifest.json").read_bytes()
            artifact_root = root / "overflow-artifacts"

            with self.assertRaises(CanonicalCanvasOverflowError) as raised:
                with contextlib.redirect_stdout(io.StringIO()):
                    run_frozen_ingestion(
                        repository,
                        source_directory,
                        artifact_root,
                        [source_set_id],
                    )

            report = raised.exception.report
            self.assertEqual(
                report["schemaVersion"],
                "2d-doll-canonical-canvas-overflow-review-0.1",
            )
            self.assertEqual(report["repositoryMutation"], "none")
            self.assertTrue(report["conditions"])
            condition = report["conditions"][0]
            self.assertEqual(
                condition["code"], "CANONICAL_CANVAS_OVERFLOW_REVIEW_REQUIRED"
            )
            self.assertTrue(condition["offendingBoundaries"])
            self.assertFalse(artifact_root.exists())
            self.assertEqual(canvas_path.read_bytes(), canvas_before)
            self.assertEqual(record_hashes(corpus_root), abc_before)
            self.assertEqual(
                (corpus_root / "sources/source-manifest.json").read_bytes(),
                source_before,
            )

    def test_coordinated_canvas_drift_is_rejected_before_artifact_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository, corpus_root, source_directory, source_set_id = self._run_fixture(
                root, name="synthetic_drift"
            )
            canvas_path = corpus_root / "spec/canvas.json"
            export_path = corpus_root / "spec/export-contract.json"
            canvas = read_json(canvas_path)
            export_contract = read_json(export_path)
            canvas["heightPx"] = 2176
            canvas["groundYPx"] = 2048
            export_contract["canvas"]["heightPx"] = 2176
            export_contract["canvas"]["groundYPx"] = 2048
            write_json(canvas_path, canvas)
            write_json(export_path, export_contract)
            corpus_before = tree_bytes(corpus_root)
            artifact_root = root / "drift-artifacts"

            with self.assertRaisesRegex(FrozenIngestionError, "pinned contract"):
                with contextlib.redirect_stdout(io.StringIO()):
                    run_frozen_ingestion(
                        repository,
                        source_directory,
                        artifact_root,
                        [source_set_id],
                    )

            self.assertFalse(artifact_root.exists())
            self.assertEqual(tree_bytes(corpus_root), corpus_before)

    def test_safe_margin_review_identifies_the_preserved_pose(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository, _, source_directory, source_set_id = self._run_fixture(
                root,
                name="synthetic_margin",
                include_safe_margin=True,
            )
            artifact_root = root / "margin-artifacts"
            with contextlib.redirect_stdout(io.StringIO()):
                result = run_frozen_ingestion(
                    repository,
                    source_directory,
                    artifact_root,
                    [source_set_id],
                )

            conditions = result["overflowReviewConditions"]
            condition = next(
                item
                for item in conditions
                if item["entryId"] == "synthetic_margin_pose_002"
            )
            self.assertEqual(condition["sourceSetId"], source_set_id)
            self.assertEqual(condition["originalLabel"], "tall_hair_extension")
            self.assertIn("top", condition["offendingBoundaries"])
            self.assertGreater(condition["boundaryOverflowPx"]["top"], 0)
            self.assertEqual(condition["alphaThreshold"], 1)
            self.assertTrue(condition["frozenCanvasSha256"])
            overflow_report = read_json(
                artifact_root / "qa/reports/overflow-review.json"
            )
            reported = {item["entryId"] for item in overflow_report["conditions"]}
            self.assertIn("synthetic_margin_pose_002", reported)

    def test_post_write_failure_rolls_back_repository_and_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repository, corpus_root, source_directory, source_set_id = self._run_fixture(
                root, name="synthetic_transaction"
            )
            files_before = tree_bytes(corpus_root)
            directories_before = {
                path.relative_to(corpus_root).as_posix()
                for path in corpus_root.rglob("*")
                if path.is_dir()
            }
            artifact_root = root / "transaction-artifacts"
            staging_root = artifact_root.with_name(
                f".{artifact_root.name}.frozen-ingest.tmp"
            )

            with mock.patch(
                "tools.pose_corpus.frozen_ingestion._assert_bytes_unchanged",
                side_effect=[
                    None,
                    FrozenIngestionError("injected post-write failure"),
                ],
            ):
                with self.assertRaisesRegex(
                    FrozenIngestionError, "injected post-write failure"
                ):
                    with contextlib.redirect_stdout(io.StringIO()):
                        run_frozen_ingestion(
                            repository,
                            source_directory,
                            artifact_root,
                            [source_set_id],
                        )

            self.assertFalse(artifact_root.exists())
            self.assertFalse(staging_root.exists())
            self.assertEqual(tree_bytes(corpus_root), files_before)
            directories_after = {
                path.relative_to(corpus_root).as_posix()
                for path in corpus_root.rglob("*")
                if path.is_dir()
            }
            self.assertEqual(directories_after, directories_before)

    def test_equivalent_baselines_produce_deterministic_package_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            results = []
            for suffix in ("one", "two"):
                repository, _, source_directory, source_set_id = self._run_fixture(
                    root / suffix, name="synthetic_repeat"
                )
                artifact_root = root / suffix / "artifacts"
                with contextlib.redirect_stdout(io.StringIO()):
                    run_frozen_ingestion(
                        repository,
                        source_directory,
                        artifact_root,
                        [source_set_id],
                    )
                results.append(
                    {
                        path.relative_to(artifact_root).as_posix(): hashlib.sha256(
                            path.read_bytes()
                        ).hexdigest()
                        for path in sorted(artifact_root.rglob("*"))
                        if path.is_file()
                    }
                )
            differences = {
                path: (results[0].get(path), results[1].get(path))
                for path in sorted(set(results[0]) | set(results[1]))
                if results[0].get(path) != results[1].get(path)
            }
            self.assertFalse(differences, sorted(differences))

    def test_legacy_run_requires_explicit_calibration_policy(self) -> None:
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                parse_args(
                    [
                        "run",
                        "--source-directory",
                        "sources",
                        "--artifact-root",
                        "artifacts",
                    ]
                )
        parsed = parse_args(
            [
                "run",
                "--source-directory",
                "sources",
                "--artifact-root",
                "artifacts",
                "--canvas-policy",
                "calibrate",
            ]
        )
        self.assertEqual(parsed.canvas_policy, "calibrate")


if __name__ == "__main__":
    unittest.main()
