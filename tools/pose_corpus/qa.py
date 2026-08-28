from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageFont

from .contracts import CORPUS_ID, QA_SUMMARY_SCHEMA_VERSION
from .image_ops import rgba_array
from .inventory import canonical_json_sha256, read_runtime_artifact, sha256_file


CELL_WIDTH = 320
CELL_HEIGHT = 390
THUMB_WIDTH = 280
THUMB_HEIGHT = 300
COLUMNS = 6


def _checker(size: tuple[int, int], tile: int = 16) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, "#d7d7d7")
    draw = ImageDraw.Draw(image)
    for y in range(0, height, tile):
        for x in range(0, width, tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill="#eeeeee")
    return image


def _background(kind: str, size: tuple[int, int]) -> Image.Image:
    if kind == "checkerboard":
        return _checker(size)
    if kind == "black":
        return Image.new("RGB", size, "#000000")
    if kind == "light":
        return Image.new("RGB", size, "#f2f2f2")
    raise ValueError(kind)


def _thumbnail(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as source:
        source.load()
        image = source.convert("RGBA")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    return image


def _paste_rgba(background: Image.Image, image: Image.Image, xy: tuple[int, int]) -> None:
    layer = Image.new("RGBA", background.size, (0, 0, 0, 0))
    layer.paste(image, xy, image)
    merged = Image.alpha_composite(background.convert("RGBA"), layer).convert("RGB")
    background.paste(merged)


def _save_jpeg(path: Path, image: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="JPEG", quality=92, subsampling=0, optimize=False)


def _sheet_sidecar(
    sheet_path: Path,
    kind: str,
    cells: list[dict[str, Any]],
    corpus_index_hash: str,
) -> dict[str, Any]:
    sidecar = {
        "schemaVersion": "2d-doll-pose-corpus-qa-sheet-0.1",
        "corpusId": CORPUS_ID,
        "sheetKind": kind,
        "sheetFilename": sheet_path.name,
        "corpusIndexSha256": corpus_index_hash,
        "cells": cells,
    }
    sidecar_path = sheet_path.with_suffix(".json")
    sidecar_path.write_text(
        json.dumps(sidecar, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {
        "kind": kind,
        "logicalPath": sheet_path.as_posix(),
        "sha256": sha256_file(sheet_path),
        "sidecarLogicalPath": sidecar_path.as_posix(),
        "sidecarSha256": sha256_file(sidecar_path),
        "cellCount": len(cells),
    }


def contact_sheet(
    artifact_root: Path,
    render_manifest: dict[str, Any],
    kind: str,
    corpus_index_hash: str,
) -> dict[str, Any]:
    renders = render_manifest["renders"]
    rows = (len(renders) + COLUMNS - 1) // COLUMNS
    sheet = _background(kind, (COLUMNS * CELL_WIDTH, rows * CELL_HEIGHT))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    cells: list[dict[str, Any]] = []
    for index, render in enumerate(renders):
        row, column = divmod(index, COLUMNS)
        cell_x, cell_y = column * CELL_WIDTH, row * CELL_HEIGHT
        path = artifact_root / Path(render["output"]["logicalPath"])
        thumb = _thumbnail(path, (THUMB_WIDTH, THUMB_HEIGHT))
        x = cell_x + (CELL_WIDTH - thumb.width) // 2
        y = cell_y + 8 + (THUMB_HEIGHT - thumb.height)
        _paste_rgba(sheet, thumb, (x, y))
        status = render["renderStatus"]
        status_color = {
            "accepted": "#16843d",
            "review_required": "#9a6500",
            "blocked_source_defect": "#b21f2d",
        }.get(status, "#333333")
        label_y = cell_y + 315
        draw.rectangle(
            (cell_x + 4, label_y - 3, cell_x + CELL_WIDTH - 4, label_y + 66),
            fill="#ffffff" if kind != "light" else "#e7e7e7",
        )
        draw.text((cell_x + 10, label_y), render["entryId"], fill="#111111", font=font)
        draw.text((cell_x + 10, label_y + 17), status, fill=status_color, font=font)
        draw.text(
            (cell_x + 10, label_y + 34),
            render["output"]["decodedPixelSha256"][:12],
            fill="#333333",
            font=font,
        )
        cells.append(
            {
                "cellIndex": index,
                "entryId": render["entryId"],
                "renderStatus": status,
                "outputSha256": render["output"]["sha256"],
                "decodedPixelSha256": render["output"]["decodedPixelSha256"],
            }
        )
    relative = Path("qa") / f"canonical-contact-{kind}.jpg"
    path = artifact_root / relative
    _save_jpeg(path, sheet)
    artifact = _sheet_sidecar(path, f"canonical_contact_{kind}", cells, corpus_index_hash)
    artifact["logicalPath"] = relative.as_posix()
    artifact["sidecarLogicalPath"] = relative.with_suffix(".json").as_posix()
    return artifact


def _proposal_point_to_canvas(
    point: dict[str, float], proposal: dict[str, Any]
) -> tuple[float, float]:
    mapping = proposal["calibration"]["mechanicsToNormalization"]
    transform = proposal["placement"]["canvasTransform"]
    nx = point["x"] * mapping["scaleX"] + mapping["offsetX"]
    ny = point["y"] * mapping["scaleY"] + mapping["offsetY"]
    return (
        nx * transform["isotropicScale"] + transform["translateXPx"],
        ny * transform["isotropicScale"] + transform["translateYPx"],
    )


def overlay_sheet(
    artifact_root: Path,
    render_manifest: dict[str, Any],
    proposals: list[dict[str, Any]],
    corpus_index_hash: str,
) -> dict[str, Any]:
    proposal_by_id = {item["entryId"]: item for item in proposals}
    renders = render_manifest["renders"]
    rows = (len(renders) + COLUMNS - 1) // COLUMNS
    sheet = _checker((COLUMNS * CELL_WIDTH, rows * CELL_HEIGHT))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    cells: list[dict[str, Any]] = []
    canvas = render_manifest["canvas"]
    for index, render in enumerate(renders):
        row, column = divmod(index, COLUMNS)
        cell_x, cell_y = column * CELL_WIDTH, row * CELL_HEIGHT
        path = artifact_root / Path(render["output"]["logicalPath"])
        with Image.open(path) as source:
            source.load()
            rgba = source.convert("RGBA")
        scale = min(THUMB_WIDTH / rgba.width, THUMB_HEIGHT / rgba.height)
        thumb = rgba.resize(
            (max(1, round(rgba.width * scale)), max(1, round(rgba.height * scale))),
            Image.Resampling.LANCZOS,
        )
        x = cell_x + (CELL_WIDTH - thumb.width) // 2
        y = cell_y + 8 + (THUMB_HEIGHT - thumb.height)
        _paste_rgba(sheet, thumb, (x, y))
        ground_y = y + canvas["groundYPx"] * scale
        origin_x = x + canvas["originXPx"] * scale
        draw.line((cell_x + 8, ground_y, cell_x + CELL_WIDTH - 8, ground_y), fill="#00a4ff", width=2)
        proposal = proposal_by_id[render["entryId"]]
        pelvis_point = proposal["landmarks"]["pelvis_center"]["proposal"]["sourceImagePx"]
        pelvis_canvas = _proposal_point_to_canvas(pelvis_point, proposal)
        px = x + pelvis_canvas[0] * scale
        py = y + pelvis_canvas[1] * scale
        draw.line((px - 6, py, px + 6, py), fill="#ff00a8", width=2)
        draw.line((px, py - 6, px, py + 6), fill="#ff00a8", width=2)
        head_point = proposal["landmarks"]["head_top"]["proposal"]["sourceImagePx"]
        head_canvas = _proposal_point_to_canvas(head_point, proposal)
        hx = x + head_canvas[0] * scale
        hy = y + head_canvas[1] * scale
        draw.ellipse((hx - 4, hy - 4, hx + 4, hy + 4), outline="#ff4d00", width=2)
        label_y = cell_y + 315
        draw.rectangle((cell_x + 4, label_y - 3, cell_x + CELL_WIDTH - 4, label_y + 52), fill="#ffffff")
        draw.text((cell_x + 10, label_y), render["entryId"], fill="#111111", font=font)
        draw.text((cell_x + 10, label_y + 17), "cyan ground / magenta pelvis / orange head proposal", fill="#333333", font=font)
        cells.append(
            {
                "cellIndex": index,
                "entryId": render["entryId"],
                "outputSha256": render["output"]["sha256"],
                "proposalSha256": proposal["proposalSha256"],
            }
        )
    relative = Path("qa") / "landmark-root-ground-overlay.jpg"
    path = artifact_root / relative
    _save_jpeg(path, sheet)
    artifact = _sheet_sidecar(path, "landmark_root_ground_overlay", cells, corpus_index_hash)
    artifact["logicalPath"] = relative.as_posix()
    artifact["sidecarLogicalPath"] = relative.with_suffix(".json").as_posix()
    return artifact


def selection_sheet(
    artifact_root: Path,
    render_manifest: dict[str, Any],
    entry_ids: Iterable[str],
    title: str,
    filename: str,
    corpus_index_hash: str,
) -> dict[str, Any]:
    render_by_id = {item["entryId"]: item for item in render_manifest["renders"]}
    selected = [render_by_id[entry_id] for entry_id in entry_ids]
    columns = min(4, len(selected))
    rows = (len(selected) + columns - 1) // columns
    sheet = _checker((columns * 420, rows * 460 + 42), tile=18)
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.rectangle((0, 0, sheet.width, 42), fill="#ffffff")
    draw.text((14, 14), title, fill="#111111", font=font)
    cells: list[dict[str, Any]] = []
    for index, render in enumerate(selected):
        row, column = divmod(index, columns)
        cell_x, cell_y = column * 420, 42 + row * 460
        path = artifact_root / Path(render["output"]["logicalPath"])
        thumb = _thumbnail(path, (380, 380))
        _paste_rgba(
            sheet,
            thumb,
            (cell_x + (420 - thumb.width) // 2, cell_y + 8 + (380 - thumb.height)),
        )
        draw.rectangle((cell_x + 5, cell_y + 390, cell_x + 415, cell_y + 452), fill="#ffffff")
        draw.text((cell_x + 12, cell_y + 397), render["entryId"], fill="#111111", font=font)
        draw.text((cell_x + 12, cell_y + 414), render["renderStatus"], fill="#8f1f26" if "blocked" in render["renderStatus"] else "#9a6500", font=font)
        draw.text((cell_x + 12, cell_y + 431), render["output"]["decodedPixelSha256"][:12], fill="#333333", font=font)
        cells.append(
            {
                "cellIndex": index,
                "entryId": render["entryId"],
                "renderStatus": render["renderStatus"],
                "outputSha256": render["output"]["sha256"],
            }
        )
    relative = Path("qa") / filename
    path = artifact_root / relative
    _save_jpeg(path, sheet)
    artifact = _sheet_sidecar(path, filename.removesuffix(".jpg"), cells, corpus_index_hash)
    artifact["logicalPath"] = relative.as_posix()
    artifact["sidecarLogicalPath"] = relative.with_suffix(".json").as_posix()
    return artifact


def before_after_sheet(
    artifact_root: Path,
    source_manifest: dict[str, Any],
    runtime_index: dict[str, Any],
    render_manifest: dict[str, Any],
    entry_ids: list[str],
    corpus_index_hash: str,
) -> dict[str, Any]:
    source_by_id = {item["entryId"]: item for item in source_manifest["entries"]}
    render_by_id = {item["entryId"]: item for item in render_manifest["renders"]}
    sheet = _checker((1200, len(entry_ids) * 400 + 42), tile=18)
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    draw.rectangle((0, 0, sheet.width, 42), fill="#ffffff")
    draw.text((14, 14), "Source normalization input → fixed-canvas similarity candidate", fill="#111111", font=font)
    cells: list[dict[str, Any]] = []
    for index, entry_id in enumerate(entry_ids):
        y = 42 + index * 400
        source_rgba = Image.fromarray(
            rgba_array(read_runtime_artifact(runtime_index["entries"][entry_id], "normalization")),
            mode="RGBA",
        )
        source_rgba.thumbnail((500, 340), Image.Resampling.LANCZOS)
        render = render_by_id[entry_id]
        normalized = _thumbnail(
            artifact_root / Path(render["output"]["logicalPath"]), (500, 340)
        )
        _paste_rgba(sheet, source_rgba, (50 + (500 - source_rgba.width) // 2, y + 10 + (340 - source_rgba.height)))
        _paste_rgba(sheet, normalized, (650 + (500 - normalized.width) // 2, y + 10 + (340 - normalized.height)))
        draw.rectangle((5, y + 350, 1195, y + 395), fill="#ffffff")
        draw.text((15, y + 360), f"{entry_id}  source", fill="#111111", font=font)
        draw.text((615, y + 360), f"candidate  {render['renderStatus']}", fill="#111111", font=font)
        cells.append(
            {
                "cellIndex": index,
                "entryId": entry_id,
                "sourceArtifactSha256": next(
                    artifact["sha256"]
                    for artifact in source_by_id[entry_id]["artifacts"]
                    if artifact["artifactId"]
                    == source_by_id[entry_id]["normalizationArtifactId"]
                ),
                "outputSha256": render["output"]["sha256"],
            }
        )
    relative = Path("qa") / "representative-before-after.jpg"
    path = artifact_root / relative
    _save_jpeg(path, sheet)
    artifact = _sheet_sidecar(path, "representative_before_after", cells, corpus_index_hash)
    artifact["logicalPath"] = relative.as_posix()
    artifact["sidecarLogicalPath"] = relative.with_suffix(".json").as_posix()
    return artifact


def _unique_fill(
    selected: Iterable[str], all_entry_ids: list[str], limit: int
) -> list[str]:
    result: list[str] = []
    for entry_id in [*selected, *all_entry_ids]:
        if entry_id not in result:
            result.append(entry_id)
        if len(result) == min(limit, len(all_entry_ids)):
            break
    return result


def _representative_entry_ids(
    source_manifest: dict[str, Any], limit: int = 6
) -> list[str]:
    groups: dict[str, list[str]] = {}
    for entry in source_manifest["entries"]:
        groups.setdefault(entry["sourceSetId"], []).append(entry["entryId"])
    selected = [ids[0] for ids in groups.values()]
    selected.extend(ids[-1] for ids in groups.values())
    all_ids = [entry["entryId"] for entry in source_manifest["entries"]]
    return _unique_fill(selected, all_ids, limit)


def _calibration_entry_ids(
    source_manifest: dict[str, Any], limit: int = 8
) -> list[str]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for entry in source_manifest["entries"]:
        groups.setdefault(entry["calibrationGroupId"], []).append(entry)
    preferred_tokens = (
        "neutral",
        "upright",
        "front_lock",
        "steady_hold",
        "step_initiation",
        "glance_pose",
        "torso_turn",
    )

    def rank(entry: dict[str, Any]) -> tuple[int, int]:
        label = entry["originalLabel"].lower()
        token_rank = next(
            (
                index
                for index, token in enumerate(preferred_tokens)
                if token in label
            ),
            len(preferred_tokens),
        )
        return token_rank, entry["ordinal"]

    return [
        min(entries, key=rank)["entryId"]
        for entries in list(groups.values())[:limit]
    ]


def _stress_entry_ids(
    proposals: list[dict[str, Any]], limit: int = 8
) -> list[str]:
    desired_families = (
        "overhead_arms",
        "knee_flexion",
        "stance",
        "leg_cross",
        "walk",
        "torso_turn",
        "torso_lean",
        "head_motion",
    )
    selected: list[str] = []
    for family in desired_families:
        match = next(
            (
                proposal["entryId"]
                for proposal in proposals
                if family in proposal["classification"]["poseFamilyIds"]
            ),
            None,
        )
        if match is not None:
            selected.append(match)
    all_ids = [proposal["entryId"] for proposal in proposals]
    return _unique_fill(selected, all_ids, limit)


def _source_issue_entry_ids(
    source_manifest: dict[str, Any], limit: int = 12
) -> list[str]:
    all_ids = [entry["entryId"] for entry in source_manifest["entries"]]
    selected = [
        entry["entryId"]
        for entry in source_manifest["entries"]
        if entry["issues"] or entry["unresolvedClaims"]
    ]
    if selected:
        return selected[:limit]
    return all_ids[: min(6, limit)]


def generate_qa_artifacts(
    artifact_root: Path,
    source_manifest: dict[str, Any],
    runtime_index: dict[str, Any],
    render_manifest: dict[str, Any],
    proposals: list[dict[str, Any]],
    corpus_index: dict[str, Any],
) -> dict[str, Any]:
    corpus_index_hash = corpus_index["indexSha256"]
    artifacts = [
        contact_sheet(artifact_root, render_manifest, kind, corpus_index_hash)
        for kind in ("checkerboard", "black", "light")
    ]
    artifacts.append(
        overlay_sheet(
            artifact_root, render_manifest, proposals, corpus_index_hash
        )
    )
    artifacts.append(
        before_after_sheet(
            artifact_root,
            source_manifest,
            runtime_index,
            render_manifest,
            _representative_entry_ids(source_manifest),
            corpus_index_hash,
        )
    )
    artifacts.append(
        selection_sheet(
            artifact_root,
            render_manifest,
            _calibration_entry_ids(source_manifest),
            "Cross-set neutral/root/scale calibration references",
            "cross-set-scale-comparison.jpg",
            corpus_index_hash,
        )
    )
    artifacts.append(
        selection_sheet(
            artifact_root,
            render_manifest,
            _stress_entry_ids(proposals),
            "Stress poses: overhead, knee bend, cross, stride, profile, rear, lift",
            "stress-pose-comparison.jpg",
            corpus_index_hash,
        )
    )
    artifacts.append(
        selection_sheet(
            artifact_root,
            render_manifest,
            _source_issue_entry_ids(source_manifest),
            "Declared source defects, review cases, and unresolved claims",
            "source-defect-review.jpg",
            corpus_index_hash,
        )
    )
    issue_counts = Counter(
        issue["code"]
        for render in render_manifest["renders"]
        for issue in render["issues"]
    )
    summary = {
        "schemaVersion": QA_SUMMARY_SCHEMA_VERSION,
        "corpusId": CORPUS_ID,
        "corpusIndexSha256": corpus_index_hash,
        "renderManifestSha256": render_manifest["renderManifestSha256"],
        "counts": {
            "registered": len(source_manifest["entries"]),
            **render_manifest["counts"],
            "qaArtifactCount": len(artifacts),
        },
        "verdict": {
            "inventoryStatus": "passed",
            "mechanicsStatus": "review_required",
            "renderStatus": "candidates_generated_not_accepted",
            "workflowValidationStatus": "not_validated",
        },
        "issueCounts": dict(sorted(issue_counts.items())),
        "qaArtifacts": artifacts,
        "limitations": [
            "Silhouette proposals do not resolve anatomical landmarks or left/right semantics.",
            "No local proportion retarget was applied without reviewed control topology.",
            (
                f"{render_manifest['counts']['blockedSourceDefect']} candidate(s) "
                "remain quarantined by source-declared defect dispositions."
            ),
            "Automated evidence establishes no owner or creative-workflow validation.",
        ],
        "qaSummarySha256": None,
    }
    summary["qaSummarySha256"] = canonical_json_sha256(
        {**summary, "qaSummarySha256": None}
    )
    return summary
