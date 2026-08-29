from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .contracts import (
    CORPUS_ID,
    CORPUS_ROOT_RELATIVE,
    CORPUS_SCHEMA_VERSION,
    PROFILE_EVIDENCE_ID,
    TOOL_VERSION,
)
from .inventory import canonical_json_sha256, collect_inventory
from .normalize import render_corpus
from .qa import generate_qa_artifacts
from .resolve import (
    build_entries_and_overrides,
    build_profile_evidence,
    build_proposals,
    measure_calibration,
)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
        + b"\n"
    )


def _corpus_index(
    source_manifest: dict[str, Any],
    entries: list[dict[str, Any]],
    render_manifest: dict[str, Any],
) -> dict[str, Any]:
    source_by_id = {item["entryId"]: item for item in source_manifest["entries"]}
    render_by_id = {item["entryId"]: item for item in render_manifest["renders"]}
    records = []
    for entry in sorted(entries, key=lambda item: item["entryId"]):
        source = source_by_id[entry["entryId"]]
        render = render_by_id[entry["entryId"]]
        records.append(
            {
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
        )
    counts = {
        "registered": len(records),
        "mechanicsResolved": sum(
            record["acceptance"]["mechanicsStatus"] == "resolved"
            for record in records
        ),
        "candidatesProduced": len(render_manifest["renders"]),
        "acceptedRenders": sum(
            record["acceptance"]["renderStatus"] == "accepted"
            for record in records
        ),
        "reviewRequiredRenders": sum(
            record["acceptance"]["renderStatus"] == "review_required"
            for record in records
        ),
        "blockedSourceDefectRenders": sum(
            record["acceptance"]["renderStatus"] == "blocked_source_defect"
            for record in records
        ),
    }
    index = {
        "schemaVersion": "2d-doll-pose-corpus-index-0.1",
        "corpusId": CORPUS_ID,
        "counts": counts,
        "entries": records,
        "indexSha256": None,
        "extensions": {},
    }
    index["indexSha256"] = canonical_json_sha256({**index, "indexSha256": None})
    return index


def _corpus_descriptor(
    index: dict[str, Any], qa_summary: dict[str, Any]
) -> dict[str, Any]:
    return {
        "schemaVersion": CORPUS_SCHEMA_VERSION,
        "corpusId": CORPUS_ID,
        "releaseStatus": "provisional_review_required",
        "profileEvidenceRef": "spec/base_female_v0_1.corpus-evidence.json",
        "coordinateContractRef": "spec/coordinate-space.json",
        "landmarkVocabularyRef": "spec/landmark-vocabulary.json",
        "orientationVocabularyRef": "spec/orientation-vocabulary.json",
        "sourceManifestRef": "sources/source-manifest.json",
        "entryIndexRef": "metadata/corpus-index.json",
        "renderManifestRef": "normalized/render-manifest.json",
        "qaSummaryRef": "qa/reports/run-summary.json",
        "storagePolicyRef": "spec/storage-policy.json",
        "counts": index["counts"],
        "runtimeBoundary": {
            "integrationStatus": "none",
            "isReusablePose": False,
            "compatiblePoseSchemaVersions": [],
            "adapterRequired": True,
        },
        "acceptance": {
            "inventoryStatus": qa_summary["verdict"]["inventoryStatus"],
            "mechanicsStatus": qa_summary["verdict"]["mechanicsStatus"],
            "renderStatus": qa_summary["verdict"]["renderStatus"],
            "workflowValidationStatus": "not_validated",
        },
        "extensions": {},
    }


def _write_repository_records(
    repository_root: Path,
    source_manifest: dict[str, Any],
    calibration: dict[str, Any],
    canvas: dict[str, Any],
    profile: dict[str, Any],
    proposals: list[dict[str, Any]],
    overrides: list[dict[str, Any]],
    entries: list[dict[str, Any]],
    render_manifest: dict[str, Any],
    index: dict[str, Any],
    qa_summary: dict[str, Any],
) -> None:
    root = repository_root / CORPUS_ROOT_RELATIVE
    write_json(root / "sources/source-manifest.json", source_manifest)
    write_json(root / "spec/calibration-evidence.json", calibration)
    write_json(root / "spec/canvas.json", canvas)
    write_json(root / "spec/base_female_v0_1.corpus-evidence.json", profile)
    source_by_id = {item["entryId"]: item for item in source_manifest["entries"]}
    proposal_by_id = {item["entryId"]: item for item in proposals}
    override_by_id = {item["entryId"]: item for item in overrides}
    for entry in entries:
        entry_id = entry["entryId"]
        path_key = source_by_id[entry_id]["pathKey"]
        write_json(
            root / f"metadata/proposals/{path_key}/{entry_id}.json",
            proposal_by_id[entry_id],
        )
        write_json(
            root / f"overrides/{path_key}/{entry_id}.json",
            override_by_id[entry_id],
        )
        write_json(
            root / f"metadata/poses/{path_key}/{entry_id}.json",
            entry,
        )
    write_json(root / "normalized/render-manifest.json", render_manifest)
    write_json(root / "metadata/corpus-index.json", index)
    write_json(root / "qa/reports/run-summary.json", qa_summary)
    write_json(root / "corpus.json", _corpus_descriptor(index, qa_summary))


def run_inventory(
    repository_root: Path, source_directory: Path, write: bool
) -> dict[str, Any]:
    source_manifest, _ = collect_inventory(repository_root, source_directory)
    if write:
        write_json(
            repository_root / CORPUS_ROOT_RELATIVE / "sources/source-manifest.json",
            source_manifest,
        )
    result = {
        "corpusId": CORPUS_ID,
        "registered": source_manifest["counts"]["registered"],
        "sourceSets": source_manifest["counts"]["bySourceSet"],
        "sourceManifestSha256": canonical_json_sha256(source_manifest),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def run_full(
    repository_root: Path,
    source_directory: Path,
    artifact_root: Path,
) -> dict[str, Any]:
    source_manifest, runtime_index = collect_inventory(
        repository_root, source_directory
    )
    calibration = measure_calibration(
        repository_root, source_manifest, runtime_index
    )
    proposals, canvas = build_proposals(
        repository_root,
        source_manifest,
        runtime_index,
        calibration,
        canvas_policy="calibration",
    )
    profile = build_profile_evidence(calibration, canvas)
    entries, overrides = build_entries_and_overrides(
        repository_root, source_manifest, proposals, canvas
    )
    render_manifest, entries = render_corpus(
        source_manifest,
        runtime_index,
        proposals,
        entries,
        artifact_root,
        canvas,
    )
    index = _corpus_index(source_manifest, entries, render_manifest)
    qa_summary = generate_qa_artifacts(
        artifact_root,
        source_manifest,
        runtime_index,
        render_manifest,
        proposals,
        index,
    )
    _write_repository_records(
        repository_root,
        source_manifest,
        calibration,
        canvas,
        profile,
        proposals,
        overrides,
        entries,
        render_manifest,
        index,
        qa_summary,
    )
    external_run_manifest = {
        "schemaVersion": "2d-doll-pose-corpus-local-run-0.1",
        "corpusId": CORPUS_ID,
        "toolVersion": TOOL_VERSION,
        "profileEvidenceId": PROFILE_EVIDENCE_ID,
        "artifactRoot": str(artifact_root.resolve()),
        "artifactRootCommitted": False,
        "sourceManifestSha256": canonical_json_sha256(source_manifest),
        "corpusIndexSha256": index["indexSha256"],
        "renderManifestSha256": render_manifest["renderManifestSha256"],
        "qaSummarySha256": qa_summary["qaSummarySha256"],
        "counts": index["counts"],
    }
    write_json(artifact_root / "run-manifest.json", external_run_manifest)
    result = {
        "corpusId": CORPUS_ID,
        "artifactRoot": str(artifact_root.resolve()),
        "bodyPixels": canvas["bodyPixels"],
        "canvas": [canvas["widthPx"], canvas["heightPx"]],
        "counts": index["counts"],
        "qaVerdict": qa_summary["verdict"],
        "runManifestSha256": canonical_json_sha256(external_run_manifest),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deterministic canonical pose-corpus ingestion and normalization"
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    inventory = subparsers.add_parser("inventory")
    inventory.add_argument("--source-directory", type=Path, required=True)
    inventory.add_argument("--write", action="store_true")
    calibrate = subparsers.add_parser(
        "calibrate",
        help="explicitly derive a coordinate contract and rebuild the full corpus",
    )
    calibrate.add_argument("--source-directory", type=Path, required=True)
    calibrate.add_argument("--artifact-root", type=Path, required=True)
    run = subparsers.add_parser(
        "run",
        help="legacy full-corpus command; requires an explicit calibration policy",
    )
    run.add_argument("--source-directory", type=Path, required=True)
    run.add_argument("--artifact-root", type=Path, required=True)
    run.add_argument("--canvas-policy", choices=("calibrate",), required=True)
    ingest = subparsers.add_parser(
        "ingest",
        help="ingest selected packages against the existing frozen canvas",
    )
    ingest.add_argument("--source-directory", type=Path, required=True)
    ingest.add_argument("--artifact-root", type=Path, required=True)
    ingest.add_argument(
        "--source-set-id", action="append", required=True, dest="source_set_ids"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    repository_root = args.repository_root.resolve()
    if args.command == "inventory":
        run_inventory(repository_root, args.source_directory.resolve(), args.write)
    elif args.command in {"calibrate", "run"}:
        run_full(
            repository_root,
            args.source_directory.resolve(),
            args.artifact_root.resolve(),
        )
    elif args.command == "ingest":
        from .frozen_ingestion import run_frozen_ingestion

        run_frozen_ingestion(
            repository_root,
            args.source_directory.resolve(),
            args.artifact_root.resolve(),
            args.source_set_ids,
        )
    else:
        raise AssertionError(args.command)
