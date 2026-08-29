from __future__ import annotations

import copy
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Any

import numpy as np

from .contracts import (
    COORDINATE_SPACE_ID,
    CORPUS_ID,
    CORPUS_ROOT_RELATIVE,
    ENTRY_SCHEMA_VERSION,
    LANDMARK_IDS,
    OVERRIDE_SCHEMA_VERSION,
    PROFILE_EVIDENCE_ID,
    PROFILE_EVIDENCE_SCHEMA_VERSION,
    PROPOSAL_SCHEMA_VERSION,
    TARGET_PROFILE_ID,
)
from .image_ops import (
    alpha_bbox,
    contact_clusters,
    estimate_head_top,
    estimate_root_and_ground,
    rgba_array,
)
from .inventory import (
    canonical_json_sha256,
    load_source_config,
    read_runtime_artifact,
)


def _round_up(value: float, multiple: int) -> int:
    return int(math.ceil(value / multiple) * multiple)


def _artifact(entry: dict[str, Any], artifact_id: str) -> dict[str, Any]:
    return next(item for item in entry["artifacts"] if item["artifactId"] == artifact_id)


def _weighted_median(values: list[tuple[float, float]]) -> float:
    ordered = sorted(values)
    total = sum(weight for _, weight in ordered)
    cursor = 0.0
    for value, weight in ordered:
        cursor += weight
        if cursor >= total * 0.5:
            return value
    return ordered[-1][0]


def _reference_measurement(
    entry: dict[str, Any], runtime_record: dict[str, Any]
) -> dict[str, Any]:
    rgba = rgba_array(read_runtime_artifact(runtime_record, "mechanics"))
    alpha = rgba[:, :, 3]
    head = estimate_head_top(alpha)
    bbox = alpha_bbox(alpha, 8)
    if bbox is None or "yPx" not in head:
        raise RuntimeError(f"calibration reference is not measurable: {entry['entryId']}")
    ground_y = float(bbox[3] - 1) + 0.5
    stature = ground_y - float(head["yPx"])
    return {
        "entryId": entry["entryId"],
        "basename": _artifact(entry, entry["mechanicsArtifactId"])["basename"],
        "headTopYPx": round(float(head["yPx"]), 4),
        "groundYPx": round(ground_y, 4),
        "neutralStaturePx": round(stature, 4),
        "method": "silhouette_contiguous_width_profile_plus_lowest_alpha_envelope",
        "resolutionStage": "generated_proposal",
        "reviewStatus": "review_required",
        "confidence": head["confidence"],
    }


def measure_calibration(
    repository_root: Path,
    source_manifest: dict[str, Any],
    runtime_index: dict[str, Any],
    *,
    frozen_body_pixels: int | None = None,
) -> dict[str, Any]:
    config = load_source_config(repository_root)
    selected_source_set_ids = {
        source_set["sourceSetId"] for source_set in source_manifest["sourceSets"]
    }
    entries_by_source_and_basename = {
        (
            entry["sourceSetId"],
            _artifact(entry, entry["mechanicsArtifactId"])["basename"],
        ): entry
        for entry in source_manifest["entries"]
    }
    groups: dict[str, Any] = {}
    raster_candidates: list[tuple[float, float]] = []
    for source_set in config["sourceSets"]:
        if source_set["sourceSetId"] not in selected_source_set_ids:
            continue
        for group in source_set["calibrationGroups"]:
            observations = []
            for basename in group["referenceBasenames"]:
                entry = entries_by_source_and_basename.get(
                    (source_set["sourceSetId"], basename)
                )
                if entry is None:
                    raise RuntimeError(
                        "missing calibration reference "
                        f"{source_set['sourceSetId']}:{basename}"
                    )
                observation = _reference_measurement(
                    entry, runtime_index["entries"][entry["entryId"]]
                )
                observations.append(observation)
            confidence_weight = 1.0 if group["confidence"] == "high" else 0.65
            stature = _weighted_median(
                [
                    (observation["neutralStaturePx"], confidence_weight)
                    for observation in observations
                ]
            )
            groups[group["groupId"]] = {
                "groupId": group["groupId"],
                "sourceSetId": source_set["sourceSetId"],
                "neutralStaturePx": round(stature, 4),
                "observations": observations,
                "confidence": group["confidence"],
                "status": "provisional_unreviewed",
            }
            if group["rasterSelectionEvidence"]:
                raster_candidates.append((stature, confidence_weight))
    if frozen_body_pixels is None:
        if not raster_candidates:
            raise RuntimeError(
                "calibration mode requires at least one rasterSelectionEvidence group"
            )
        proposed_body_pixels = _round_up(_weighted_median(raster_candidates), 64)
        raster_status = "provisional_freeze_for_v0_1_evidence_run"
        raster_reason = (
            "Confidence-weighted median of declared calibration groups with "
            "rasterSelectionEvidence=true; other groups do not influence the "
            "canonical raster-quality scale."
        )
        canvas_policy = "calibration"
    else:
        if frozen_body_pixels <= 0:
            raise RuntimeError("frozen bodyPixels must be positive")
        proposed_body_pixels = int(frozen_body_pixels)
        raster_status = "loaded_from_frozen_canvas_contract"
        raster_reason = (
            "Package calibration is measured for placement only. bodyPixels is "
            "loaded unchanged from the frozen canonical canvas contract."
        )
        canvas_policy = "frozen_ingestion"
    return {
        "method": "confidence_weighted_median_of_declared_neutral_reference_proposals",
        "canvasPolicy": canvas_policy,
        "groups": groups,
        "rasterSelection": {
            "candidateNeutralStaturesPx": [
                round(value, 4) for value, _ in raster_candidates
            ],
            "bodyPixels": proposed_body_pixels,
            "roundingMultiplePx": 64,
            "status": raster_status,
            "reason": raster_reason,
        },
    }


def _layer_mapping(
    mechanics_rgba: np.ndarray, normalization_rgba: np.ndarray
) -> dict[str, Any]:
    mechanics_bbox = alpha_bbox(mechanics_rgba[:, :, 3], 8)
    normalization_bbox = alpha_bbox(normalization_rgba[:, :, 3], 8)
    if mechanics_bbox is None or normalization_bbox is None:
        raise RuntimeError("cannot map empty source layers")
    mx0, my0, mx1, my1 = mechanics_bbox
    nx0, ny0, nx1, ny1 = normalization_bbox
    scale_x = (nx1 - nx0) / (mx1 - mx0)
    scale_y = (ny1 - ny0) / (my1 - my0)
    offset_x = nx0 - mx0 * scale_x
    offset_y = ny0 - my0 * scale_y
    return {
        "scaleX": round(scale_x, 10),
        "scaleY": round(scale_y, 10),
        "offsetX": round(offset_x, 10),
        "offsetY": round(offset_y, 10),
        "anisotropy": round(abs(scale_x / scale_y - 1.0), 10),
        "mechanicsAlphaBbox": list(mechanics_bbox),
        "normalizationAlphaBbox": list(normalization_bbox),
    }


def _map_point(point: dict[str, float], mapping: dict[str, Any]) -> dict[str, float]:
    return {
        "x": point["x"] * mapping["scaleX"] + mapping["offsetX"],
        "y": point["y"] * mapping["scaleY"] + mapping["offsetY"],
    }


def _projection(label: str, sequence: str | None, manual_direction: str) -> dict[str, Any]:
    normalized = label.lower()
    if "rear_threequarter" in normalized or "rear_profile" in normalized:
        projection_class = "rear_three_quarter"
    elif "front_threequarter" in normalized or "quarter_turn" in normalized:
        projection_class = "front_three_quarter"
    elif "profile" in normalized or normalized in {"side_turn", "side_glance"}:
        projection_class = "profile"
    elif normalized.startswith("rear"):
        projection_class = "rear"
    elif any(token in normalized for token in ("angled_pose", "torso_turn", "glance_pose")):
        projection_class = "front_three_quarter"
    else:
        projection_class = "front"
    if projection_class == "front":
        canonical = "front"
        mapping_status = "direct_reference"
    elif projection_class == "front_three_quarter":
        canonical = "three_quarter"
        mapping_status = "provisional_reference"
    elif projection_class == "rear":
        canonical = "back"
        mapping_status = "provisional_reference"
    else:
        canonical = None
        mapping_status = "reference_only"
    return {
        "canonicalBodyOrientationId": canonical,
        "canonicalMappingStatus": mapping_status,
        "observedProjection": {
            "projectionClass": projection_class,
            "screenDirection": (
                manual_direction
                if projection_class
                in {"profile", "front_three_quarter", "rear_three_quarter"}
                else "unspecified"
            ),
            "estimatedYawDeg": None,
            "resolutionStage": "generated_proposal",
            "confidence": {
                "level": "medium" if projection_class != "front" else "low",
                "score": 0.68 if projection_class != "front" else 0.58,
                "basis": ["source_filename_label", "bounded_contact_sheet_observation"],
            },
        },
        "headObservation": {
            "projectionClass": "unknown",
            "rollDeg": None,
            "pitchClass": "unknown",
            "resolutionStage": "unresolved",
            "confidence": {"level": "unresolved", "score": 0.0, "basis": []},
        },
    }


def _classification(label: str, sequence: str | None) -> dict[str, Any]:
    normalized = label.lower()
    families: list[str] = []
    keyword_families = (
        ("walk", "walk"),
        ("stride", "walk"),
        ("step", "walk"),
        ("knee", "knee_flexion"),
        ("stance", "stance"),
        ("hip", "hip_shift"),
        ("head", "head_motion"),
        ("hand", "hand_gesture"),
        ("wrist", "hand_gesture"),
        ("overhead", "overhead_arms"),
        ("arms_high", "overhead_arms"),
        ("leg_cross", "leg_cross"),
        ("torso", "torso_turn"),
        ("lean", "torso_lean"),
        ("glance", "glance"),
    )
    for token, family in keyword_families:
        if token in normalized and family not in families:
            families.append(family)
    if sequence in {"dance", "walk"} and sequence not in families:
        families.insert(0, sequence)
    if not families:
        families = ["pose_reference"]
    gait = None
    if "walk" in families:
        gait = {
            "phase": "unresolved",
            "travelDirection": "screen_right",
            "supportFoot": "unknown",
            "strideLengthBody": None,
            "resolutionStage": "unresolved",
        }
    return {
        "primaryPoseFamilyId": families[0],
        "poseFamilyIds": families,
        "variantId": re.sub(r"[^a-z0-9]+", "_", normalized).strip("_"),
        "gait": gait,
    }


def _proposal_landmarks(
    root_ground: dict[str, Any],
    head: dict[str, Any],
    neutral_stature_px: float,
) -> dict[str, Any]:
    root = root_ground["pelvisCenterPx"]
    root_x = root["x"]
    head_y = float(head.get("yPx", root["y"] - 0.55 * neutral_stature_px))
    generated: dict[str, dict[str, Any]] = {
        "head_top": {
            "sourceImagePx": {"x": root_x, "y": head_y},
            "confidence": 0.56,
            "basis": ["silhouette_contiguous_width_profile", "body_medial_x_proxy"],
        },
        "head_center": {
            "sourceImagePx": {
                "x": root_x,
                "y": head_y + 0.065 * neutral_stature_px,
            },
            "confidence": 0.42,
            "basis": ["head_height_prior", "body_medial_x_proxy"],
        },
        "chin": {
            "sourceImagePx": {
                "x": root_x,
                "y": head_y + 0.13 * neutral_stature_px,
            },
            "confidence": 0.35,
            "basis": ["head_height_prior"],
        },
        "neck_base": {
            "sourceImagePx": {
                "x": root_x,
                "y": head_y + 0.15 * neutral_stature_px,
            },
            "confidence": 0.32,
            "basis": ["neutral_stature_prior"],
        },
        "neck_socket": {
            "sourceImagePx": {
                "x": root_x,
                "y": head_y + 0.16 * neutral_stature_px,
            },
            "confidence": 0.30,
            "basis": ["neutral_stature_prior"],
        },
        "chest_center": {
            "sourceImagePx": {
                "x": root_x,
                "y": head_y + 0.25 * neutral_stature_px,
            },
            "confidence": 0.28,
            "basis": ["neutral_stature_prior"],
        },
        "waist_center": {
            "sourceImagePx": {
                "x": root_x,
                "y": head_y + 0.42 * neutral_stature_px,
            },
            "confidence": 0.30,
            "basis": ["neutral_stature_prior"],
        },
        "pelvis_center": {
            "sourceImagePx": {"x": root["x"], "y": root["y"]},
            "confidence": root_ground["confidence"],
            "basis": root_ground["basis"],
        },
    }
    landmarks: dict[str, Any] = {}
    for landmark_id in LANDMARK_IDS:
        proposal = generated.get(landmark_id)
        if proposal:
            landmarks[landmark_id] = {
                "availability": "ambiguous",
                "proposal": {
                    **proposal,
                    "resolutionStage": "generated_proposal",
                },
                "override": None,
                "resolved": None,
                "unresolvedReason": "semantic_landmark_requires_human_review",
            }
        else:
            landmarks[landmark_id] = {
                "availability": "unavailable",
                "proposal": None,
                "override": None,
                "resolved": None,
                "unresolvedReason": "not_reliably_inferable_from_flattened_silhouette",
            }
    return landmarks


def _derive_canvas(extents: dict[str, float], body_pixels: int) -> dict[str, Any]:
    safe_margin = max(8, int(math.ceil(0.05 * body_pixels)))
    resample_support = 8
    half_width = math.ceil(
        max(abs(extents["xMin"]), abs(extents["xMax"]))
        + safe_margin
        + resample_support
    )
    canvas_width = _round_up(2 * half_width, 64)
    root_x = canvas_width // 2
    ground_y = _round_up(
        math.ceil(-extents["yMin"] + safe_margin + resample_support), 64
    )
    canvas_height = _round_up(
        ground_y
        + math.ceil(extents["yMax"] + safe_margin + resample_support),
        64,
    )
    return {
        "widthPx": canvas_width,
        "heightPx": canvas_height,
        "bodyPixels": body_pixels,
        "originXPx": root_x,
        "groundYPx": ground_y,
        "safeMarginPx": safe_margin,
        "resampleSupportPx": resample_support,
        "roundingMultiplePx": 64,
        "measuredRelativeExtentPx": {
            key: round(value, 6) for key, value in extents.items()
        },
        "status": "provisional_frozen_for_v0_1_evidence_run",
    }


def _boundary_overflow(
    extent: dict[str, float],
    *,
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
) -> dict[str, float]:
    return {
        "left": round(max(0.0, x_min - extent["xMin"]), 6),
        "top": round(max(0.0, y_min - extent["yMin"]), 6),
        "right": round(max(0.0, extent["xMax"] - x_max), 6),
        "bottom": round(max(0.0, extent["yMax"] - y_max), 6),
    }


def _canvas_fit_evidence(
    relative: dict[str, float], canvas: dict[str, Any]
) -> dict[str, Any]:
    transformed = {
        "xMin": float(canvas["originXPx"]) + relative["xMin"],
        "xMax": float(canvas["originXPx"]) + relative["xMax"],
        "yMin": float(canvas["groundYPx"]) + relative["yMin"],
        "yMax": float(canvas["groundYPx"]) + relative["yMax"],
    }
    support = float(canvas["resampleSupportPx"])
    conservative = {
        "xMin": transformed["xMin"] - support,
        "xMax": transformed["xMax"] + support,
        "yMin": transformed["yMin"] - support,
        "yMax": transformed["yMax"] + support,
    }
    physical = _boundary_overflow(
        conservative,
        x_min=0.0,
        y_min=0.0,
        x_max=float(canvas["widthPx"]),
        y_max=float(canvas["heightPx"]),
    )
    margin = float(canvas["safeMarginPx"])
    safe = _boundary_overflow(
        conservative,
        x_min=margin,
        y_min=margin,
        x_max=float(canvas["widthPx"]) - margin,
        y_max=float(canvas["heightPx"]) - margin,
    )
    physical_overflow = any(value > 0 for value in physical.values())
    safe_overflow = any(value > 0 for value in safe.values())
    return {
        "measuredTransformedExtentPx": {
            key: round(value, 6) for key, value in transformed.items()
        },
        "conservativeTransformedExtentPx": {
            key: round(value, 6) for key, value in conservative.items()
        },
        "resampleSupportPx": int(support),
        "physicalBoundaryOverflowPx": physical,
        "safeMarginBoundaryOverflowPx": safe,
        "physicalCanvasOverflow": physical_overflow,
        "safeMarginReviewRequired": safe_overflow,
        "reviewRequired": physical_overflow or safe_overflow,
    }


def build_proposals(
    repository_root: Path,
    source_manifest: dict[str, Any],
    runtime_index: dict[str, Any],
    calibration: dict[str, Any],
    *,
    canvas_policy: str,
    frozen_canvas: dict[str, Any] | None = None,
    frozen_canvas_sha256: str | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if canvas_policy not in {"calibration", "frozen_ingestion"}:
        raise RuntimeError(f"unsupported canvas policy: {canvas_policy}")
    if canvas_policy == "frozen_ingestion" and frozen_canvas is None:
        raise RuntimeError("frozen ingestion requires an existing canvas contract")
    if canvas_policy == "calibration" and frozen_canvas is not None:
        raise RuntimeError("calibration mode cannot accept a frozen canvas")
    config = load_source_config(repository_root)
    source_sets = {item["sourceSetId"]: item for item in config["sourceSets"]}
    body_pixels = calibration["rasterSelection"]["bodyPixels"]
    proposals: list[dict[str, Any]] = []
    extents = {"xMin": 0.0, "xMax": 0.0, "yMin": 0.0, "yMax": 0.0}

    for entry in source_manifest["entries"]:
        runtime_record = runtime_index["entries"][entry["entryId"]]
        mechanics_rgba = rgba_array(read_runtime_artifact(runtime_record, "mechanics"))
        normalization_rgba = rgba_array(
            read_runtime_artifact(runtime_record, "normalization")
        )
        group = calibration["groups"][entry["calibrationGroupId"]]
        neutral_stature = group["neutralStaturePx"]
        group_scale = body_pixels / neutral_stature
        root_ground = estimate_root_and_ground(
            mechanics_rgba[:, :, 3], neutral_stature
        )
        head = estimate_head_top(mechanics_rgba[:, :, 3])
        layer_mapping = _layer_mapping(mechanics_rgba, normalization_rgba)
        mapping_scale = (layer_mapping["scaleX"] + layer_mapping["scaleY"]) * 0.5
        output_scale = group_scale / mapping_scale
        root_normalization = _map_point(
            root_ground["pelvisCenterPx"], layer_mapping
        )
        ground_normalization = (
            root_ground["groundYPx"] * layer_mapping["scaleY"]
            + layer_mapping["offsetY"]
        )
        normalization_bbox = alpha_bbox(normalization_rgba[:, :, 3], 1)
        if normalization_bbox is None:
            raise RuntimeError(f"empty normalization input: {entry['entryId']}")
        x0, y0, x1, y1 = normalization_bbox
        relative = {
            "xMin": (x0 - root_normalization["x"]) * output_scale,
            "xMax": (x1 - root_normalization["x"]) * output_scale,
            "yMin": (y0 - ground_normalization) * output_scale,
            "yMax": (y1 - ground_normalization) * output_scale,
        }
        for key in extents:
            if key.endswith("Min"):
                extents[key] = min(extents[key], relative[key])
            else:
                extents[key] = max(extents[key], relative[key])
        source_set = source_sets[entry["sourceSetId"]]
        contact = contact_clusters(
            mechanics_rgba[:, :, 3], root_ground["pelvisCenterPx"]["x"]
        )
        source_issues = list(entry["issues"])
        if layer_mapping["anisotropy"] > 0.01:
            source_issues.append(
                {
                    "code": "LAYER_MAPPING_ANISOTROPY",
                    "severity": "warning",
                    "detail": "Native-to-render source layers do not map isotropically within tolerance.",
                    "measured": layer_mapping["anisotropy"],
                    "disposition": "review_required",
                }
            )
        source_issues.extend(
            [
                {
                    "code": "MECHANICS_REVIEW_REQUIRED",
                    "severity": "warning",
                    "detail": "Silhouette proposals do not resolve anatomical landmarks, side, support foot, or hidden anatomy.",
                    "disposition": "review_required",
                },
                {
                    "code": "PROPORTION_RETARGET_NOT_APPLIED",
                    "severity": "warning",
                    "detail": "No reviewed semantic control topology exists; candidate render uses similarity transform only.",
                    "disposition": "review_required",
                },
            ]
        )
        proposal = {
            "schemaVersion": PROPOSAL_SCHEMA_VERSION,
            "entryId": entry["entryId"],
            "corpusId": CORPUS_ID,
            "sourceArtifactSha256": _artifact(
                entry, entry["mechanicsArtifactId"]
            )["sha256"],
            "calibration": {
                "groupId": entry["calibrationGroupId"],
                "groupNeutralStaturePx": neutral_stature,
                "targetBodyPixels": body_pixels,
                "mechanicsToNormalization": layer_mapping,
                "normalizationScale": round(output_scale, 12),
                "status": "provisional_unreviewed",
            },
            "placement": {
                "pelvisCenterMechanicsPx": root_ground["pelvisCenterPx"],
                "pelvisCenterNormalizationPx": {
                    key: round(value, 6) for key, value in root_normalization.items()
                },
                "groundMechanicsYPx": root_ground["groundYPx"],
                "groundNormalizationYPx": round(ground_normalization, 6),
                "relativeOutputExtentPx": {
                    key: round(value, 6) for key, value in relative.items()
                },
                "confidence": root_ground["confidence"],
                "status": "generated_proposal_review_required",
            },
            "orientation": _projection(
                entry["originalLabel"],
                entry["sourceSequence"]["sequenceId"],
                source_set["manualProjectionDirection"],
            ),
            "landmarks": _proposal_landmarks(
                root_ground, head, neutral_stature
            ),
            "contactCandidates": {
                "screenClusters": contact,
                "anatomicalSupportFoot": "unknown",
                "feet": {
                    "L": {"state": "unknown", "resolutionStage": "unresolved"},
                    "R": {"state": "unknown", "resolutionStage": "unresolved"},
                },
                "reviewStatus": "review_required",
            },
            "classification": _classification(
                entry["originalLabel"], entry["sourceSequence"]["sequenceId"]
            ),
            "retarget": {
                "method": "similarity_transform_only",
                "localWarpApplied": False,
                "reason": "reviewed semantic control topology unavailable",
                "capabilityStatus": "bounded_local_warp_designed_not_applied",
            },
            "issues": source_issues,
            "extensions": {},
        }
        proposals.append(proposal)

    if canvas_policy == "calibration":
        canvas = _derive_canvas(extents, body_pixels)
    else:
        assert frozen_canvas is not None
        canvas = copy.deepcopy(frozen_canvas)
        if canvas["bodyPixels"] != body_pixels:
            raise RuntimeError(
                "package calibration bodyPixels does not match frozen canvas: "
                f"{body_pixels} != {canvas['bodyPixels']}"
            )
    root_x = int(canvas["originXPx"])
    ground_y = int(canvas["groundYPx"])
    for proposal in proposals:
        placement = proposal["placement"]
        scale = proposal["calibration"]["normalizationScale"]
        root = placement["pelvisCenterNormalizationPx"]
        ground = placement["groundNormalizationYPx"]
        translation_x = int(round(root_x - root["x"] * scale))
        translation_y = int(round(ground_y - ground * scale))
        placement["canvasTransform"] = {
            "isotropicScale": scale,
            "translateXPx": translation_x,
            "translateYPx": translation_y,
            "rootRoundTripErrorPx": round(
                abs((root["x"] * scale + translation_x) - root_x), 6
            ),
            "groundRoundTripErrorPx": round(
                abs((ground * scale + translation_y) - ground_y), 6
            ),
        }
        if canvas_policy == "frozen_ingestion":
            fit = _canvas_fit_evidence(
                placement["relativeOutputExtentPx"], canvas
            )
            placement["canvasFit"] = fit
            proposal["extensions"] = {
                **proposal["extensions"],
                "canvasPolicy": "frozen_ingestion",
                "frozenCanvasSha256": frozen_canvas_sha256,
            }
            if fit["reviewRequired"]:
                proposal["issues"].append(
                    {
                        "code": "CANONICAL_CANVAS_OVERFLOW_REVIEW_REQUIRED",
                        "severity": (
                            "error" if fit["physicalCanvasOverflow"] else "warning"
                        ),
                        "detail": (
                            "The package pose exceeds the conservative physical canvas "
                            "envelope."
                            if fit["physicalCanvasOverflow"]
                            else "The package pose enters the frozen canvas safety margin."
                        ),
                        "disposition": (
                            "blocked_render"
                            if fit["physicalCanvasOverflow"]
                            else "review_required"
                        ),
                        "frozenCanvasSha256": frozen_canvas_sha256,
                        "frozenCanvas": {
                            key: canvas[key]
                            for key in (
                                "widthPx",
                                "heightPx",
                                "bodyPixels",
                                "originXPx",
                                "groundYPx",
                                "safeMarginPx",
                                "resampleSupportPx",
                            )
                        },
                        "fitEvidence": fit,
                    }
                )
        proposal["proposalSha256"] = None
        proposal["proposalSha256"] = canonical_json_sha256(proposal)
    return proposals, canvas


def build_profile_evidence(
    calibration: dict[str, Any], canvas: dict[str, Any]
) -> dict[str, Any]:
    unresolved_measurements = (
        "head_height",
        "head_width",
        "neck_length",
        "neck_width",
        "shoulder_width",
        "shoulder_to_pelvis_torso_length",
        "waist_position",
        "pelvis_width",
        "upper_arm_length",
        "forearm_length",
        "hand_length",
        "thigh_length",
        "lower_leg_length",
        "foot_length",
    )
    measurements = {
        name: {
            "unit": "body_height",
            "value": None,
            "valueBySide": {"L": None, "R": None}
            if name
            in {
                "upper_arm_length",
                "forearm_length",
                "hand_length",
                "thigh_length",
                "lower_leg_length",
                "foot_length",
            }
            else None,
            "resolutionStage": "unresolved",
            "confidence": {"level": "unresolved", "score": 0.0, "basis": []},
            "evidenceEntryIds": [],
            "unresolvedReason": "reviewed_non_foreshortened_landmarks_unavailable",
        }
        for name in unresolved_measurements
    }
    return {
        "schemaVersion": PROFILE_EVIDENCE_SCHEMA_VERSION,
        "profileEvidenceId": PROFILE_EVIDENCE_ID,
        "targetProfileId": TARGET_PROFILE_ID,
        "evidenceStatus": "generated_proposal",
        "approvalStatus": "provisional_unapproved",
        "ownerApproved": False,
        "workflowValidated": False,
        "corpusId": CORPUS_ID,
        "bodyHeightUnit": 1.0,
        "bodyPixels": canvas["bodyPixels"],
        "calibration": calibration,
        "measurements": measurements,
        "constraints": {
            "mayRenameRequiredNodes": False,
            "mayRedefineJointSemantics": False,
            "mayChangeOrientationGraph": False,
            "mayClaimCanonicalProportionContinuity": False,
        },
        "extensions": {},
    }


def _default_override(entry_id: str, proposal_sha256: str) -> dict[str, Any]:
    return {
        "schemaVersion": OVERRIDE_SCHEMA_VERSION,
        "entryId": entry_id,
        "baseProposalSha256": proposal_sha256,
        "landmarks": {},
        "orientation": None,
        "contacts": None,
        "sourceCleanup": [],
        "approval": {
            "status": "not_reviewed",
            "reviewer": None,
            "reason": None,
        },
        "extensions": {},
    }


def _override_has_authored_content(override: dict[str, Any]) -> bool:
    return bool(
        override.get("landmarks")
        or override.get("orientation") is not None
        or override.get("contacts") is not None
        or override.get("sourceCleanup")
    )


def _load_override(
    repository_root: Path,
    source: dict[str, Any],
    proposal: dict[str, Any],
) -> dict[str, Any]:
    entry_id = proposal["entryId"]
    default = _default_override(entry_id, proposal["proposalSha256"])
    path = (
        repository_root
        / CORPUS_ROOT_RELATIVE
        / "overrides"
        / source["pathKey"]
        / f"{entry_id}.json"
    )
    if not path.is_file():
        return default
    override = json.loads(path.read_text(encoding="utf-8"))
    if override.get("schemaVersion") != OVERRIDE_SCHEMA_VERSION:
        raise RuntimeError(f"unsupported override schema: {path}")
    if override.get("entryId") != entry_id:
        raise RuntimeError(f"override entryId mismatch: {path}")
    authored = _override_has_authored_content(override)
    status = override.get("approval", {}).get("status")
    if override.get("baseProposalSha256") != proposal["proposalSha256"]:
        if not authored and status == "not_reviewed":
            return default
        raise RuntimeError(
            f"authored override is stale for {entry_id}; rebase it onto "
            f"proposal {proposal['proposalSha256']}"
        )
    if authored and status not in {"reviewed", "approved"}:
        raise RuntimeError(
            f"authored override for {entry_id} requires reviewed or approved status"
        )
    if override.get("sourceCleanup"):
        raise RuntimeError(
            f"sourceCleanup overrides are reserved but not implemented for {entry_id}"
        )
    return override


def _apply_override(
    proposal: dict[str, Any], override: dict[str, Any]
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    landmarks = copy.deepcopy(proposal["landmarks"])
    orientation = copy.deepcopy(proposal["orientation"])
    contacts = copy.deepcopy(proposal["contactCandidates"])
    applied_fields: list[str] = []
    for landmark_id, authored in override["landmarks"].items():
        if landmark_id not in LANDMARK_IDS:
            raise RuntimeError(
                f"unknown landmark override {landmark_id} for {proposal['entryId']}"
            )
        resolved = authored.get("resolved")
        if not isinstance(resolved, dict) or not all(
            isinstance(resolved.get(axis), (int, float)) for axis in ("x", "y", "z")
        ):
            raise RuntimeError(
                f"landmark override {landmark_id} for {proposal['entryId']} "
                "requires numeric resolved x/y/z body-space coordinates"
            )
        landmarks[landmark_id] = {
            **landmarks[landmark_id],
            "availability": authored.get("availability", "visible"),
            "override": copy.deepcopy(authored),
            "resolved": {axis: float(resolved[axis]) for axis in ("x", "y", "z")},
            "unresolvedReason": None,
        }
        applied_fields.append(f"landmarks.{landmark_id}")
    if override["orientation"] is not None:
        authored_orientation = override["orientation"]
        orientation.update(
            {
                "canonicalBodyOrientationId": authored_orientation[
                    "canonicalBodyOrientationId"
                ],
                "canonicalMappingStatus": "reviewed_override",
                "override": copy.deepcopy(authored_orientation),
            }
        )
        applied_fields.append("orientation")
    if override["contacts"] is not None:
        authored_contacts = override["contacts"]
        for key in ("anatomicalSupportFoot", "feet"):
            if key in authored_contacts:
                contacts[key] = copy.deepcopy(authored_contacts[key])
        contacts["reviewStatus"] = "reviewed_override"
        contacts["override"] = copy.deepcopy(authored_contacts)
        applied_fields.append("contacts")
    issues: list[dict[str, Any]] = []
    if applied_fields:
        issues.append(
            {
                "code": "AUTHORED_OVERRIDE_APPLIED",
                "severity": "info",
                "detail": "Reviewed authored override data was applied to resolved corpus mechanics.",
                "disposition": "review_required",
                "fields": applied_fields,
            }
        )
    return {
        "landmarks": landmarks,
        "orientation": orientation,
        "contacts": contacts,
    }, issues


def build_entries_and_overrides(
    repository_root: Path,
    source_manifest: dict[str, Any],
    proposals: list[dict[str, Any]],
    canvas: dict[str, Any],
    *,
    source_indices: dict[str, int] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source_entries = {entry["entryId"]: entry for entry in source_manifest["entries"]}
    if source_indices is None:
        source_indices = {
            entry["entryId"]: index
            for index, entry in enumerate(source_manifest["entries"])
        }
    missing_indices = sorted(set(source_entries) - set(source_indices))
    if missing_indices:
        raise RuntimeError(
            f"source indices are missing package entries: {missing_indices}"
        )
    entries: list[dict[str, Any]] = []
    overrides: list[dict[str, Any]] = []
    for proposal in proposals:
        entry_id = proposal["entryId"]
        source = source_entries[entry_id]
        hard_blocked = any(
            issue.get("disposition") == "blocked_source_defect"
            for issue in proposal["issues"]
        )
        known_review = any(
            issue.get("disposition") == "review_required"
            for issue in source["issues"]
        )
        render_status = (
            "blocked_source_defect"
            if hard_blocked
            else "review_required"
            if known_review or proposal["retarget"]["localWarpApplied"] is False
            else "candidate"
        )
        override = _load_override(repository_root, source, proposal)
        resolved, override_issues = _apply_override(proposal, override)
        override_hash = canonical_json_sha256(override)
        mechanics = {
            "authority": "corpus_mechanics_reference",
            "coordinateSpaceId": COORDINATE_SPACE_ID,
            "poseOrigin": {
                "landmarkId": "pelvis_center",
                "mappingStatus": "generated_proposal_review_required",
                "notEquivalentTo": ["rig_root", "character_root"],
            },
            "orientation": resolved["orientation"],
            "landmarks": resolved["landmarks"],
            "contacts": resolved["contacts"],
            "classification": proposal["classification"],
            "projectedJointObservations": {},
        }
        entry = {
            "schemaVersion": ENTRY_SCHEMA_VERSION,
            "entryId": entry_id,
            "corpusId": CORPUS_ID,
            "sourceRecordRef": (
                "sources/source-manifest.json#/entries/"
                f"{source_indices[entry_id]}"
            ),
            "profileEvidenceRef": "spec/base_female_v0_1.corpus-evidence.json",
            "annotationLayers": {
                "proposalRef": f"metadata/proposals/{source['pathKey']}/{entry_id}.json",
                "overrideRef": f"overrides/{source['pathKey']}/{entry_id}.json",
                "proposalSha256": proposal["proposalSha256"],
                "overrideSha256": override_hash,
            },
            "mechanics": mechanics,
            "normalizationCandidate": {
                "canvas": canvas,
                "transform": proposal["placement"]["canvasTransform"],
                "retarget": proposal["retarget"],
            },
            "acceptance": {
                "registrationStatus": "registered",
                "mechanicsStatus": "review_required",
                "renderStatus": render_status,
                "qaStatus": "not_run",
                "workflowValidationStatus": "not_validated",
            },
            "issues": [*proposal["issues"], *override_issues],
            "extensions": {},
        }
        entries.append(entry)
        overrides.append(override)
    return entries, overrides
