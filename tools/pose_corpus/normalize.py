from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

from .contracts import (
    CORPUS_ID,
    RENDER_MANIFEST_SCHEMA_VERSION,
    TOOL_VERSION,
)
from .image_ops import (
    output_image_evidence,
    place_on_canvas,
    resize_premultiplied_linear,
    rgba_array,
)
from .inventory import canonical_json_sha256, read_runtime_artifact, sha256_file


def _write_png(path: Path, rgba: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, mode="RGBA").save(
        path,
        format="PNG",
        optimize=False,
        compress_level=9,
    )


def render_corpus(
    source_manifest: dict[str, Any],
    runtime_index: dict[str, Any],
    proposals: list[dict[str, Any]],
    entries: list[dict[str, Any]],
    artifact_root: Path,
    canvas: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if artifact_root.exists() and any(artifact_root.iterdir()):
        raise RuntimeError(f"artifact root must be empty: {artifact_root}")
    artifact_root.mkdir(parents=True, exist_ok=True)
    source_by_id = {item["entryId"]: item for item in source_manifest["entries"]}
    proposal_by_id = {item["entryId"]: item for item in proposals}
    entry_by_id = {item["entryId"]: item for item in entries}
    renders: list[dict[str, Any]] = []
    updated_entries: list[dict[str, Any]] = []
    canvas_size = (canvas["widthPx"], canvas["heightPx"])

    for entry_id in sorted(entry_by_id):
        source = source_by_id[entry_id]
        proposal = proposal_by_id[entry_id]
        entry = entry_by_id[entry_id]
        runtime_record = runtime_index["entries"][entry_id]
        normalization_rgba = rgba_array(
            read_runtime_artifact(runtime_record, "normalization")
        )
        transform = proposal["placement"]["canvasTransform"]
        scale = float(transform["isotropicScale"])
        target_size = (
            max(1, int(round(normalization_rgba.shape[1] * scale))),
            max(1, int(round(normalization_rgba.shape[0] * scale))),
        )
        resized = resize_premultiplied_linear(normalization_rgba, target_size)
        canvas_rgba, clipped = place_on_canvas(
            resized,
            canvas_size,
            (int(transform["translateXPx"]), int(transform["translateYPx"])),
        )
        current_status = entry["acceptance"]["renderStatus"]
        lane = "qa/quarantine" if current_status == "blocked_source_defect" else "review/previews"
        logical_path = f"{lane}/{source['pathKey']}/{entry_id}.png"
        output_path = artifact_root / Path(logical_path)
        _write_png(output_path, canvas_rgba)
        evidence = output_image_evidence(canvas_rgba, canvas["safeMarginPx"])
        issues = list(entry["issues"])
        if clipped:
            issues.append(
                {
                    "code": "RENDER_CLIPPED",
                    "severity": "error",
                    "detail": "Similarity-transformed raster exceeded the frozen canvas.",
                    "disposition": "blocked_render",
                }
            )
        if not evidence["foregroundInsideSafeRectangle"]:
            issues.append(
                {
                    "code": "SAFE_MARGIN_VIOLATION",
                    "severity": "error",
                    "detail": "Foreground entered the frozen canvas safety margin.",
                    "measured": evidence["alphaBboxByThreshold"]["1"],
                    "threshold": canvas["safeMarginPx"],
                    "disposition": "blocked_render",
                }
            )
        if evidence["transparentRgbNonzeroChannelCount"]:
            issues.append(
                {
                    "code": "TRANSPARENT_RGB_NOT_CLEARED",
                    "severity": "error",
                    "detail": "Output contains nonzero RGB under zero alpha.",
                    "measured": evidence["transparentRgbNonzeroChannelCount"],
                    "threshold": 0,
                    "disposition": "blocked_render",
                }
            )
        if transform["rootRoundTripErrorPx"] > 0.5:
            issues.append(
                {
                    "code": "ROOT_ROUND_TRIP_ERROR",
                    "severity": "error",
                    "detail": "Rounded candidate transform exceeds the root round-trip tolerance.",
                    "measured": transform["rootRoundTripErrorPx"],
                    "threshold": 0.5,
                    "disposition": "blocked_render",
                }
            )
        if transform["groundRoundTripErrorPx"] > 0.5:
            issues.append(
                {
                    "code": "GROUND_ROUND_TRIP_ERROR",
                    "severity": "error",
                    "detail": "Rounded candidate transform exceeds the ground round-trip tolerance.",
                    "measured": transform["groundRoundTripErrorPx"],
                    "threshold": 0.5,
                    "disposition": "blocked_render",
                }
            )
        mechanics_artifact = next(
            item
            for item in source["artifacts"]
            if item["artifactId"] == source["mechanicsArtifactId"]
        )
        if mechanics_artifact["image"]["heightPx"] < 1000:
            issues.append(
                {
                    "code": "LOW_SOURCE_RESOLUTION",
                    "severity": "warning",
                    "detail": "Upscaling does not create new anatomical or edge detail.",
                    "measured": mechanics_artifact["image"]["heightPx"],
                    "disposition": "review_required",
                }
            )
        transform_pass = not any(
            issue["code"]
            in {
                "RENDER_CLIPPED",
                "SAFE_MARGIN_VIOLATION",
                "TRANSPARENT_RGB_NOT_CLEARED",
                "ROOT_ROUND_TRIP_ERROR",
                "GROUND_ROUND_TRIP_ERROR",
            }
            for issue in issues
        )
        output_sha = sha256_file(output_path)
        render_index = len(renders)
        render_id = f"{entry_id}.normalized_candidate_v1"
        qa_status = "passed_transform_checks" if transform_pass else "failed"
        updated = {**entry}
        updated["acceptance"] = {**entry["acceptance"]}
        updated["acceptance"]["qaStatus"] = qa_status
        updated["acceptance"]["renderStatus"] = current_status
        updated["renderRef"] = (
            f"normalized/render-manifest.json#/renders/{render_index}"
        )
        updated["issues"] = issues
        resolved_metadata_sha = canonical_json_sha256(updated)
        render = {
            "renderId": render_id,
            "entryId": entry_id,
            "mechanicsRef": f"metadata/poses/{source['pathKey']}/{entry_id}.json",
            "inputHashes": {
                "sourceArtifactSha256": next(
                    artifact["sha256"]
                    for artifact in source["artifacts"]
                    if artifact["artifactId"] == source["normalizationArtifactId"]
                ),
                "resolvedMetadataSha256": resolved_metadata_sha,
                "overrideSha256": entry["annotationLayers"]["overrideSha256"],
            },
            "toolVersion": TOOL_VERSION,
            "operations": [
                {
                    "type": "premultiplied_linear_rgba_resize",
                    "isotropicScale": scale,
                    "targetSizePx": list(target_size),
                },
                {
                    "type": "translate_pelvis_x_and_ground_y_to_frozen_canvas",
                    "translateXPx": transform["translateXPx"],
                    "translateYPx": transform["translateYPx"],
                },
                {
                    "type": "local_proportion_retarget",
                    "applied": False,
                    "reason": "reviewed semantic control topology unavailable",
                },
            ],
            "output": {
                "storageClass": "external_generated",
                "logicalPath": logical_path,
                "sha256": output_sha,
                "decodedPixelSha256": evidence["decodedPixelSha256"],
                "widthPx": canvas["widthPx"],
                "heightPx": canvas["heightPx"],
                "mode": "RGBA",
            },
            "renderStatus": current_status,
            "qaStatus": qa_status,
            "qaEvidence": evidence,
            "issues": issues,
            "renderRecordSha256": None,
        }
        render["renderRecordSha256"] = canonical_json_sha256(render)
        renders.append(render)
        updated_entries.append(updated)

    manifest = {
        "schemaVersion": RENDER_MANIFEST_SCHEMA_VERSION,
        "corpusId": CORPUS_ID,
        "exportContractRef": "../spec/export-contract.json",
        "artifactStorage": {
            "class": "external_generated",
            "absolutePathCommitted": False,
            "logicalPathsRelativeToArtifactRoot": True,
        },
        "canvas": canvas,
        "renders": renders,
        "counts": {
            "producedCandidates": len(renders),
            "accepted": sum(
                item["renderStatus"] == "accepted" for item in renders
            ),
            "reviewRequired": sum(
                item["renderStatus"] == "review_required" for item in renders
            ),
            "blockedSourceDefect": sum(
                item["renderStatus"] == "blocked_source_defect" for item in renders
            ),
            "transformQaPassed": sum(
                item["qaStatus"] == "passed_transform_checks" for item in renders
            ),
        },
        "renderManifestSha256": None,
        "extensions": {},
    }
    manifest["renderManifestSha256"] = canonical_json_sha256(
        {**manifest, "renderManifestSha256": None}
    )
    return manifest, updated_entries
