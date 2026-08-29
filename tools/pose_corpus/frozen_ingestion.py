from __future__ import annotations

import copy
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from .contracts import (
    CANONICAL_V0_1_CANVAS_SHA256,
    CANONICAL_V0_1_FROZEN_CANVAS,
    CORPUS_ID,
    CORPUS_ROOT_RELATIVE,
    TOOL_VERSION,
)
from .inventory import (
    CorpusInputError,
    canonical_json_sha256,
    collect_inventory,
    sha256_bytes,
)
from .normalize import render_corpus
from .pipeline import _corpus_descriptor
from .qa import generate_qa_artifacts
from .resolve import build_entries_and_overrides, build_proposals, measure_calibration


class FrozenIngestionError(RuntimeError):
    """Raised when a frozen-ingestion invariant would be violated."""


class CanonicalCanvasOverflowError(FrozenIngestionError):
    def __init__(self, report: dict[str, Any]):
        super().__init__("canonical canvas overflow requires review")
        self.report = report


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
        + b"\n"
    )


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_json_bytes(value))


def load_frozen_canvas(
    repository_root: Path,
) -> tuple[dict[str, Any], str, bytes]:
    corpus_root = repository_root / CORPUS_ROOT_RELATIVE
    canvas_path = corpus_root / "spec/canvas.json"
    export_path = corpus_root / "spec/export-contract.json"
    canvas_bytes = canvas_path.read_bytes()
    canvas = json.loads(canvas_bytes)
    export = _read_json(export_path)["canvas"]
    canvas_sha256 = sha256_bytes(canvas_bytes)
    pinned_mismatches = {
        field: {"actual": canvas.get(field), "required": required}
        for field, required in CANONICAL_V0_1_FROZEN_CANVAS.items()
        if canvas.get(field) != required
    }
    if pinned_mismatches or canvas_sha256 != CANONICAL_V0_1_CANVAS_SHA256:
        raise FrozenIngestionError(
            "canonical-v0.1 frozen canvas does not match its pinned contract: "
            f"fields={pinned_mismatches}, sha256={canvas_sha256}, "
            f"requiredSha256={CANONICAL_V0_1_CANVAS_SHA256}"
        )
    field_pairs = {
        "widthPx": "widthPx",
        "heightPx": "heightPx",
        "bodyPixels": "bodyPixels",
        "originXPx": "horizontalOriginPx",
        "groundYPx": "groundYPx",
        "safeMarginPx": "safeMarginPx",
        "resampleSupportPx": "resampleSupportPx",
        "roundingMultiplePx": "roundingMultiplePx",
    }
    mismatches = {
        canvas_field: {
            "canvas": canvas.get(canvas_field),
            "exportContract": export.get(export_field),
        }
        for canvas_field, export_field in field_pairs.items()
        if canvas.get(canvas_field) != export.get(export_field)
    }
    if mismatches:
        raise FrozenIngestionError(
            f"frozen canvas and export contract disagree: {mismatches}"
        )
    return canvas, canvas_sha256, canvas_bytes


def _existing_record_paths(
    corpus_root: Path, source_manifest: dict[str, Any]
) -> list[Path]:
    paths: list[Path] = []
    for source in source_manifest["entries"]:
        entry_id = source["entryId"]
        path_key = source["pathKey"]
        paths.extend(
            (
                corpus_root / f"metadata/proposals/{path_key}/{entry_id}.json",
                corpus_root / f"overrides/{path_key}/{entry_id}.json",
                corpus_root / f"metadata/poses/{path_key}/{entry_id}.json",
            )
        )
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FrozenIngestionError(f"existing corpus records are missing: {missing}")
    return sorted(paths)


def _snapshot_bytes(paths: list[Path]) -> dict[Path, bytes]:
    return {path: path.read_bytes() for path in paths}


def _assert_bytes_unchanged(snapshot: dict[Path, bytes], label: str) -> None:
    changed = [
        str(path)
        for path, original in snapshot.items()
        if not path.is_file() or path.read_bytes() != original
    ]
    if changed:
        raise FrozenIngestionError(f"{label} changed during frozen ingestion: {changed}")


def _merge_source_manifest(
    existing: dict[str, Any], package: dict[str, Any]
) -> dict[str, Any]:
    existing_set_ids = {item["sourceSetId"] for item in existing["sourceSets"]}
    package_set_ids = {item["sourceSetId"] for item in package["sourceSets"]}
    repeated_sets = sorted(existing_set_ids & package_set_ids)
    if repeated_sets:
        raise FrozenIngestionError(
            f"source sets are already registered: {repeated_sets}"
        )
    existing_entry_ids = {item["entryId"] for item in existing["entries"]}
    package_entry_ids = {item["entryId"] for item in package["entries"]}
    repeated_entries = sorted(existing_entry_ids & package_entry_ids)
    if repeated_entries:
        raise FrozenIngestionError(
            f"entry IDs are already registered: {repeated_entries}"
        )
    merged = copy.deepcopy(existing)
    merged["sourceConfigSha256"] = package["sourceConfigSha256"]
    merged["sourceSets"] = [
        *copy.deepcopy(existing["sourceSets"]),
        *copy.deepcopy(package["sourceSets"]),
    ]
    merged["entries"] = [
        *copy.deepcopy(existing["entries"]),
        *copy.deepcopy(package["entries"]),
    ]
    merged["counts"] = {
        "registered": len(merged["entries"]),
        "bySourceSet": {
            item["sourceSetId"]: item["registeredCount"]
            for item in merged["sourceSets"]
        },
    }
    return merged


def _render_counts(renders: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "producedCandidates": len(renders),
        "accepted": sum(item["renderStatus"] == "accepted" for item in renders),
        "reviewRequired": sum(
            item["renderStatus"] == "review_required" for item in renders
        ),
        "blockedSourceDefect": sum(
            item["renderStatus"] == "blocked_source_defect" for item in renders
        ),
        "transformQaPassed": sum(
            item["qaStatus"] == "passed_transform_checks" for item in renders
        ),
    }


def _merge_render_manifest(
    existing: dict[str, Any],
    package: dict[str, Any],
    artifact_set_id: str,
    source_set_ids: list[str],
) -> dict[str, Any]:
    if existing["canvas"] != package["canvas"]:
        raise FrozenIngestionError("package render manifest changed the frozen canvas")
    existing_ids = {item["entryId"] for item in existing["renders"]}
    package_ids = {item["entryId"] for item in package["renders"]}
    repeated = sorted(existing_ids & package_ids)
    if repeated:
        raise FrozenIngestionError(f"render records are already registered: {repeated}")
    merged = copy.deepcopy(existing)
    merged["renders"] = [
        *copy.deepcopy(existing["renders"]),
        *copy.deepcopy(package["renders"]),
    ]
    merged["counts"] = _render_counts(merged["renders"])
    extensions = copy.deepcopy(existing.get("extensions", {}))
    artifact_sets = list(extensions.get("frozenIngestionArtifactSets", []))
    artifact_sets.append(
        {
            "artifactSetId": artifact_set_id,
            "sourceSetIds": source_set_ids,
            "entryIds": sorted(package_ids),
            "logicalPathsRelativeToOwnArtifactRoot": True,
        }
    )
    extensions["frozenIngestionArtifactSets"] = artifact_sets
    merged["extensions"] = extensions
    merged["renderManifestSha256"] = None
    merged["renderManifestSha256"] = canonical_json_sha256(merged)
    return merged


def _new_index_record(
    source: dict[str, Any], entry: dict[str, Any], render: dict[str, Any]
) -> dict[str, Any]:
    return {
        "entryId": entry["entryId"],
        "sourceSetId": source["sourceSetId"],
        "pathKey": source["pathKey"],
        "ordinal": source["ordinal"],
        "originalLabel": source["originalLabel"],
        "sourceEntrySha256": canonical_json_sha256(source),
        "entrySha256": canonical_json_sha256(entry),
        "proposalSha256": entry["annotationLayers"]["proposalSha256"],
        "overrideSha256": entry["annotationLayers"]["overrideSha256"],
        "renderRecordSha256": render["renderRecordSha256"],
        "renderOutput": render["output"],
        "acceptance": entry["acceptance"],
    }


def _index_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "registered": len(records),
        "mechanicsResolved": sum(
            item["acceptance"]["mechanicsStatus"] == "resolved" for item in records
        ),
        "candidatesProduced": len(records),
        "acceptedRenders": sum(
            item["acceptance"]["renderStatus"] == "accepted" for item in records
        ),
        "reviewRequiredRenders": sum(
            item["acceptance"]["renderStatus"] == "review_required"
            for item in records
        ),
        "blockedSourceDefectRenders": sum(
            item["acceptance"]["renderStatus"] == "blocked_source_defect"
            for item in records
        ),
    }


def _merge_index(
    existing: dict[str, Any],
    package_source_manifest: dict[str, Any],
    package_entries: list[dict[str, Any]],
    package_render_manifest: dict[str, Any],
    artifact_set_id: str,
) -> dict[str, Any]:
    existing_ids = {item["entryId"] for item in existing["entries"]}
    source_by_id = {
        item["entryId"]: item for item in package_source_manifest["entries"]
    }
    render_by_id = {
        item["entryId"]: item for item in package_render_manifest["renders"]
    }
    new_records = [
        _new_index_record(source_by_id[entry["entryId"]], entry, render_by_id[entry["entryId"]])
        for entry in sorted(package_entries, key=lambda item: item["entryId"])
    ]
    repeated = sorted(existing_ids & {item["entryId"] for item in new_records})
    if repeated:
        raise FrozenIngestionError(f"index records are already registered: {repeated}")
    merged = copy.deepcopy(existing)
    merged["entries"] = [*copy.deepcopy(existing["entries"]), *new_records]
    merged["counts"] = _index_counts(merged["entries"])
    extensions = copy.deepcopy(existing.get("extensions", {}))
    packages = list(extensions.get("frozenIngestionPackages", []))
    packages.append(
        {
            "artifactSetId": artifact_set_id,
            "entryIds": [item["entryId"] for item in new_records],
        }
    )
    extensions["frozenIngestionPackages"] = packages
    merged["extensions"] = extensions
    merged["indexSha256"] = None
    merged["indexSha256"] = canonical_json_sha256(merged)
    return merged


def _package_local_metadata(
    package_source_manifest: dict[str, Any],
    package_entries: list[dict[str, Any]],
    package_render_manifest: dict[str, Any],
    artifact_set_id: str,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    source_indices = {
        item["entryId"]: index
        for index, item in enumerate(package_source_manifest["entries"])
    }
    render_indices = {
        item["entryId"]: index
        for index, item in enumerate(package_render_manifest["renders"])
    }
    local_entries: list[dict[str, Any]] = []
    for entry in package_entries:
        entry_id = entry["entryId"]
        local = copy.deepcopy(entry)
        local["sourceRecordRef"] = (
            f"sources/source-manifest.json#/entries/{source_indices[entry_id]}"
        )
        local["renderRef"] = (
            f"normalized/render-manifest.json#/renders/{render_indices[entry_id]}"
        )
        local_entries.append(local)
    local_entry_by_id = {item["entryId"]: item for item in local_entries}

    local_render = copy.deepcopy(package_render_manifest)
    local_render["extensions"] = {
        **local_render.get("extensions", {}),
        "referenceScope": "package_local",
        "renderIndexOffset": 0,
    }
    for render in local_render["renders"]:
        entry_id = render["entryId"]
        render["inputHashes"]["resolvedMetadataSha256"] = canonical_json_sha256(
            local_entry_by_id[entry_id]
        )
        render["renderRecordSha256"] = None
        render["renderRecordSha256"] = canonical_json_sha256(render)
    local_render["renderManifestSha256"] = None
    local_render["renderManifestSha256"] = canonical_json_sha256(local_render)

    source_by_id = {
        item["entryId"]: item for item in package_source_manifest["entries"]
    }
    render_by_id = {item["entryId"]: item for item in local_render["renders"]}
    index_records = [
        _new_index_record(
            source_by_id[entry["entryId"]],
            entry,
            render_by_id[entry["entryId"]],
        )
        for entry in local_entries
    ]
    local_index = {
        "schemaVersion": "2d-doll-pose-corpus-index-0.1",
        "corpusId": CORPUS_ID,
        "counts": _index_counts(index_records),
        "entries": index_records,
        "extensions": {
            "scope": "frozen_ingestion_package",
            "artifactSetId": artifact_set_id,
        },
        "indexSha256": None,
    }
    local_index["indexSha256"] = canonical_json_sha256(local_index)
    return local_entries, local_render, local_index


def _merge_qa_summary(
    existing: dict[str, Any],
    package: dict[str, Any],
    merged_index: dict[str, Any],
    merged_render_manifest: dict[str, Any],
    artifact_set_id: str,
) -> dict[str, Any]:
    package_artifacts = []
    for artifact in package["qaArtifacts"]:
        package_artifacts.append({**copy.deepcopy(artifact), "artifactSetId": artifact_set_id})
    issue_counts = Counter(
        issue["code"]
        for render in merged_render_manifest["renders"]
        for issue in render["issues"]
    )
    limitations = list(existing["limitations"])
    if any(
        issue["code"] == "CANONICAL_CANVAS_OVERFLOW_REVIEW_REQUIRED"
        for render in merged_render_manifest["renders"]
        if render["output"].get("artifactSetId") == artifact_set_id
        for issue in render["issues"]
    ):
        limitations.append("One or more new package poses require frozen-canvas overflow review.")
    merged = copy.deepcopy(existing)
    merged["corpusIndexSha256"] = merged_index["indexSha256"]
    merged["renderManifestSha256"] = merged_render_manifest[
        "renderManifestSha256"
    ]
    merged["counts"] = {
        "registered": merged_index["counts"]["registered"],
        **merged_render_manifest["counts"],
        "qaArtifactCount": len(existing["qaArtifacts"]) + len(package_artifacts),
    }
    merged["issueCounts"] = dict(sorted(issue_counts.items()))
    merged["qaArtifacts"] = [
        *copy.deepcopy(existing["qaArtifacts"]),
        *package_artifacts,
    ]
    merged["limitations"] = limitations
    merged["qaSummarySha256"] = None
    merged["qaSummarySha256"] = canonical_json_sha256(merged)
    return merged


def _atomic_write_updates(
    updates: dict[Path, bytes],
    post_write_check: Callable[[], None],
    finalize_artifact: Callable[[], None],
    rollback_artifact: Callable[[], None],
) -> None:
    backups = {
        path: path.read_bytes() if path.is_file() else None for path in updates
    }
    applied: list[Path] = []
    temporary_paths: list[Path] = []
    created_directories: set[Path] = set()
    try:
        for path, data in updates.items():
            cursor = path.parent
            while not cursor.exists():
                created_directories.add(cursor)
                cursor = cursor.parent
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_name(f".{path.name}.frozen-ingest.tmp")
            if temporary.exists():
                raise FrozenIngestionError(
                    f"stale frozen-ingestion temporary file exists: {temporary}"
                )
            temporary.write_bytes(data)
            temporary_paths.append(temporary)
            temporary.replace(path)
            applied.append(path)
        post_write_check()
        finalize_artifact()
        post_write_check()
    except Exception:
        try:
            rollback_artifact()
        finally:
            for temporary in temporary_paths:
                if temporary.exists():
                    temporary.unlink()
            for path in reversed(applied):
                original = backups[path]
                if original is None:
                    if path.exists():
                        path.unlink()
                else:
                    rollback = path.with_name(
                        f".{path.name}.frozen-ingest-rollback.tmp"
                    )
                    rollback.write_bytes(original)
                    rollback.replace(path)
            for directory in sorted(
                created_directories,
                key=lambda item: len(item.parts),
                reverse=True,
            ):
                if directory.is_dir() and not any(directory.iterdir()):
                    directory.rmdir()
        raise


class _ArtifactTransaction:
    def __init__(self, final_root: Path):
        self.final_root = final_root
        self.staging_root = final_root.with_name(
            f".{final_root.name}.frozen-ingest.tmp"
        )
        self.finalized = False
        if self.final_root.exists():
            raise FrozenIngestionError(
                f"artifact root must not already exist: {self.final_root}"
            )
        if self.staging_root.exists():
            raise FrozenIngestionError(
                f"stale artifact staging root exists: {self.staging_root}"
            )

    def finalize(self) -> None:
        if not self.staging_root.is_dir():
            raise FrozenIngestionError(
                f"artifact staging root is missing: {self.staging_root}"
            )
        if self.final_root.exists():
            raise FrozenIngestionError(
                f"artifact root appeared during ingestion: {self.final_root}"
            )
        self.staging_root.replace(self.final_root)
        self.finalized = True

    def rollback(self) -> None:
        if self.finalized and self.final_root.exists():
            if self.staging_root.exists():
                raise FrozenIngestionError(
                    "cannot roll back artifact output because the staging root reappeared"
                )
            self.final_root.replace(self.staging_root)
            self.finalized = False
        if self.staging_root.exists():
            shutil.rmtree(self.staging_root)


def _overflow_report(
    proposals: list[dict[str, Any]],
    source_by_id: dict[str, dict[str, Any]],
    canvas: dict[str, Any],
    canvas_sha256: str,
) -> dict[str, Any] | None:
    conditions = []
    for proposal in proposals:
        fit = proposal["placement"].get("canvasFit")
        if not fit or not fit["physicalCanvasOverflow"]:
            continue
        source = source_by_id[proposal["entryId"]]
        conditions.append(
            {
                "code": "CANONICAL_CANVAS_OVERFLOW_REVIEW_REQUIRED",
                "entryId": proposal["entryId"],
                "sourceSetId": source["sourceSetId"],
                "originalLabel": source["originalLabel"],
                "offendingBoundaries": [
                    key
                    for key, value in fit["physicalBoundaryOverflowPx"].items()
                    if value > 0
                ],
                "fitEvidence": fit,
            }
        )
    if not conditions:
        return None
    return {
        "schemaVersion": "2d-doll-canonical-canvas-overflow-review-0.1",
        "corpusId": CORPUS_ID,
        "canvasPolicy": "frozen_ingestion",
        "frozenCanvasSha256": canvas_sha256,
        "frozenCanvas": canvas,
        "conditions": conditions,
        "repositoryMutation": "none",
        "artifactMutation": "none",
    }


def _artifact_metadata(
    artifact_root: Path,
    corpus_root: Path,
    package_source_manifest: dict[str, Any],
    calibration: dict[str, Any],
    proposals: list[dict[str, Any]],
    overrides: list[dict[str, Any]],
    package_local_entries: list[dict[str, Any]],
    package_local_render_manifest: dict[str, Any],
    package_local_index: dict[str, Any],
    package_qa_summary: dict[str, Any],
    run_manifest: dict[str, Any],
) -> None:
    source_by_id = {
        item["entryId"]: item for item in package_source_manifest["entries"]
    }
    _write_json(artifact_root / "sources/source-manifest.json", package_source_manifest)
    _write_json(artifact_root / "metadata/calibration.json", calibration)
    _write_json(
        artifact_root / "normalized/render-manifest.json",
        package_local_render_manifest,
    )
    _write_json(artifact_root / "metadata/corpus-index.json", package_local_index)
    _write_json(artifact_root / "qa/reports/run-summary.json", package_qa_summary)
    for proposal in proposals:
        path_key = source_by_id[proposal["entryId"]]["pathKey"]
        _write_json(
            artifact_root
            / f"metadata/proposals/{path_key}/{proposal['entryId']}.json",
            proposal,
        )
    for override in overrides:
        path_key = source_by_id[override["entryId"]]["pathKey"]
        _write_json(
            artifact_root / f"overrides/{path_key}/{override['entryId']}.json",
            override,
        )
    for entry in package_local_entries:
        path_key = source_by_id[entry["entryId"]]["pathKey"]
        _write_json(
            artifact_root / f"metadata/poses/{path_key}/{entry['entryId']}.json",
            entry,
        )
    overflow_conditions = [
        issue
        for render in package_local_render_manifest["renders"]
        for issue in render["issues"]
        if issue["code"] == "CANONICAL_CANVAS_OVERFLOW_REVIEW_REQUIRED"
    ]
    _write_json(
        artifact_root / "qa/reports/overflow-review.json",
        {
            "schemaVersion": "2d-doll-canonical-canvas-overflow-review-0.1",
            "corpusId": CORPUS_ID,
            "canvasPolicy": run_manifest["canvasPolicy"],
            "conditions": overflow_conditions,
        },
    )
    for filename in (
        "canvas.json",
        "export-contract.json",
        "base_female_v0_1.corpus-evidence.json",
    ):
        source_path = corpus_root / f"spec/{filename}"
        target_path = artifact_root / f"spec/{filename}"
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(source_path.read_bytes())
    _write_json(artifact_root / "run-manifest.json", run_manifest)


def run_frozen_ingestion(
    repository_root: Path,
    source_directory: Path,
    artifact_root: Path,
    source_set_ids: list[str],
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    source_directory = source_directory.resolve()
    artifact_root = artifact_root.resolve()
    requested_ids = list(dict.fromkeys(source_set_ids))
    if not requested_ids or len(requested_ids) != len(source_set_ids):
        raise CorpusInputError("source-set IDs must be non-empty and unique")

    artifact_transaction = _ArtifactTransaction(artifact_root)

    corpus_root = repository_root / CORPUS_ROOT_RELATIVE
    canvas, canvas_sha256, canvas_bytes = load_frozen_canvas(repository_root)
    existing_source = _read_json(corpus_root / "sources/source-manifest.json")
    existing_render = _read_json(corpus_root / "normalized/render-manifest.json")
    existing_index = _read_json(corpus_root / "metadata/corpus-index.json")
    existing_qa = _read_json(corpus_root / "qa/reports/run-summary.json")
    existing_record_snapshot = _snapshot_bytes(
        _existing_record_paths(corpus_root, existing_source)
    )

    package_source, runtime_index = collect_inventory(
        repository_root, source_directory, set(requested_ids)
    )
    merged_source = _merge_source_manifest(existing_source, package_source)
    source_indices = {
        entry["entryId"]: index
        for index, entry in enumerate(merged_source["entries"])
    }
    calibration = measure_calibration(
        repository_root,
        package_source,
        runtime_index,
        frozen_body_pixels=canvas["bodyPixels"],
    )
    proposals, proposal_canvas = build_proposals(
        repository_root,
        package_source,
        runtime_index,
        calibration,
        canvas_policy="frozen_ingestion",
        frozen_canvas=canvas,
        frozen_canvas_sha256=canvas_sha256,
    )
    if proposal_canvas != canvas:
        raise FrozenIngestionError("proposal construction changed the frozen canvas")
    source_by_id = {item["entryId"]: item for item in package_source["entries"]}
    physical_overflow = _overflow_report(
        proposals, source_by_id, canvas, canvas_sha256
    )
    if physical_overflow is not None:
        raise CanonicalCanvasOverflowError(physical_overflow)

    entries, overrides = build_entries_and_overrides(
        repository_root,
        package_source,
        proposals,
        canvas,
        source_indices=source_indices,
    )
    artifact_set_id = (
        f"{'+'.join(requested_ids)}."
        f"{canonical_json_sha256(package_source)[:12]}"
    )
    try:
        package_render, entries = render_corpus(
            package_source,
            runtime_index,
            proposals,
            entries,
            artifact_transaction.staging_root,
            canvas,
            render_index_offset=len(existing_render["renders"]),
            artifact_set_id=artifact_set_id,
            frozen_canvas_sha256=canvas_sha256,
        )
        merged_render = _merge_render_manifest(
            existing_render, package_render, artifact_set_id, requested_ids
        )
        merged_index = _merge_index(
            existing_index,
            package_source,
            entries,
            package_render,
            artifact_set_id,
        )
        local_entries, local_render, local_index = _package_local_metadata(
            package_source,
            entries,
            package_render,
            artifact_set_id,
        )
        package_qa = generate_qa_artifacts(
            artifact_transaction.staging_root,
            package_source,
            runtime_index,
            local_render,
            proposals,
            local_index,
        )
        merged_qa = _merge_qa_summary(
            existing_qa,
            package_qa,
            merged_index,
            merged_render,
            artifact_set_id,
        )
        aggregate_source_sha256 = canonical_json_sha256(merged_source)
        run_manifest = {
            "schemaVersion": "2d-doll-pose-corpus-frozen-ingestion-run-0.1",
            "corpusId": CORPUS_ID,
            "toolVersion": TOOL_VERSION,
            "operation": "frozen_ingestion",
            "sourceSetIds": requested_ids,
            "entryIds": [item["entryId"] for item in package_source["entries"]],
            "artifactSetId": artifact_set_id,
            "artifactRootCommitted": False,
            "referenceScope": "package_local",
            "canvasPolicy": {
                "mode": "frozen_ingestion",
                "frozenCanvasSha256": canvas_sha256,
                "canvas": canvas,
            },
            "packageSourceManifestSha256": canonical_json_sha256(package_source),
            "aggregateSourceManifestSha256": aggregate_source_sha256,
            "packageRenderManifestSha256": local_render[
                "renderManifestSha256"
            ],
            "aggregateScopePackageRenderManifestSha256": package_render[
                "renderManifestSha256"
            ],
            "aggregateRenderManifestSha256": merged_render[
                "renderManifestSha256"
            ],
            "packageCorpusIndexSha256": local_index["indexSha256"],
            "packageQaSummarySha256": package_qa["qaSummarySha256"],
            "aggregateQaSummarySha256": merged_qa["qaSummarySha256"],
            "aggregateCorpusIndexSha256": merged_index["indexSha256"],
            "packageCounts": local_render["counts"],
            "aggregateCounts": merged_index["counts"],
        }
        _artifact_metadata(
            artifact_transaction.staging_root,
            corpus_root,
            package_source,
            calibration,
            proposals,
            overrides,
            local_entries,
            local_render,
            local_index,
            package_qa,
            run_manifest,
        )

        proposal_by_id = {item["entryId"]: item for item in proposals}
        override_by_id = {item["entryId"]: item for item in overrides}
        updates: dict[Path, bytes] = {
            corpus_root / "sources/source-manifest.json": _json_bytes(merged_source),
            corpus_root / "normalized/render-manifest.json": _json_bytes(
                merged_render
            ),
            corpus_root / "metadata/corpus-index.json": _json_bytes(merged_index),
            corpus_root / "qa/reports/run-summary.json": _json_bytes(merged_qa),
            corpus_root / "corpus.json": _json_bytes(
                _corpus_descriptor(merged_index, merged_qa)
            ),
        }
        for entry in entries:
            entry_id = entry["entryId"]
            path_key = source_by_id[entry_id]["pathKey"]
            updates[
                corpus_root / f"metadata/proposals/{path_key}/{entry_id}.json"
            ] = _json_bytes(proposal_by_id[entry_id])
            updates[
                corpus_root / f"overrides/{path_key}/{entry_id}.json"
            ] = _json_bytes(override_by_id[entry_id])
            updates[
                corpus_root / f"metadata/poses/{path_key}/{entry_id}.json"
            ] = _json_bytes(entry)

        resolved_corpus_root = corpus_root.resolve()
        unsafe_targets = [
            str(path)
            for path in updates
            if not path.resolve().is_relative_to(resolved_corpus_root)
        ]
        if unsafe_targets:
            raise FrozenIngestionError(
                f"repository update escaped the corpus root: {unsafe_targets}"
            )

        def post_write_check() -> None:
            _assert_bytes_unchanged(
                existing_record_snapshot, "existing per-entry records"
            )
            if (corpus_root / "spec/canvas.json").read_bytes() != canvas_bytes:
                raise FrozenIngestionError(
                    "canonical canvas changed during ingestion"
                )

        _assert_bytes_unchanged(
            existing_record_snapshot, "existing per-entry records"
        )
        if (corpus_root / "spec/canvas.json").read_bytes() != canvas_bytes:
            raise FrozenIngestionError(
                "canonical canvas changed before repository update"
            )
        _atomic_write_updates(
            updates,
            post_write_check,
            artifact_transaction.finalize,
            artifact_transaction.rollback,
        )
    except Exception:
        artifact_transaction.rollback()
        raise

    result = {
        "corpusId": CORPUS_ID,
        "operation": "frozen_ingestion",
        "artifactRoot": str(artifact_root),
        "artifactSetId": artifact_set_id,
        "sourceSetIds": requested_ids,
        "entryIds": run_manifest["entryIds"],
        "canvas": [canvas["widthPx"], canvas["heightPx"]],
        "bodyPixels": canvas["bodyPixels"],
        "groundYPx": canvas["groundYPx"],
        "packageCounts": local_render["counts"],
        "aggregateCounts": merged_index["counts"],
        "overflowReviewConditions": [
            issue
            for render in local_render["renders"]
            for issue in render["issues"]
            if issue["code"] == "CANONICAL_CANVAS_OVERFLOW_REVIEW_REQUIRED"
        ],
        "runManifestSha256": canonical_json_sha256(run_manifest),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result
