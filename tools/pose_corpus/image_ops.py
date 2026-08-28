from __future__ import annotations

import hashlib
import math
from collections import deque
from io import BytesIO
from typing import Any

import numpy as np
from PIL import Image


def decode_image(data: bytes) -> Image.Image:
    with Image.open(BytesIO(data)) as probe:
        probe.verify()
    with Image.open(BytesIO(data)) as image:
        image.load()
        return image.copy()


def rgba_array(data: bytes) -> np.ndarray:
    return np.asarray(decode_image(data).convert("RGBA"), dtype=np.uint8)


def alpha_bbox(alpha: np.ndarray, threshold: int = 1) -> tuple[int, int, int, int] | None:
    ys, xs = np.nonzero(alpha >= threshold)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def _max_run_width(row: np.ndarray) -> int:
    padded = np.pad(row.astype(np.int8), (1, 1))
    changes = np.diff(padded)
    starts = np.flatnonzero(changes == 1)
    ends = np.flatnonzero(changes == -1)
    if len(starts) == 0:
        return 0
    return int(np.max(ends - starts))


def estimate_head_top(alpha: np.ndarray) -> dict[str, Any]:
    bbox = alpha_bbox(alpha, 8)
    if bbox is None:
        return {"status": "unavailable", "reason": "empty_alpha"}
    x0, y0, x1, y1 = bbox
    mask = alpha[y0:y1, x0:x1] >= 8
    runs = np.array([_max_run_width(row) for row in mask], dtype=np.float32)
    positive = runs[runs > 0]
    if positive.size == 0:
        return {"status": "unavailable", "reason": "empty_run_profile"}
    reference_width = float(np.percentile(positive, 88))
    threshold = max(3.0, reference_width * 0.30)
    consecutive = max(2, int(round(mask.shape[0] * 0.006)))
    candidate = None
    for offset in range(0, max(1, len(runs) - consecutive + 1)):
        window = runs[offset : offset + consecutive]
        if np.count_nonzero(window >= threshold) >= max(1, consecutive - 1):
            candidate = y0 + offset
            break
    if candidate is None:
        candidate = y0
    confidence = 0.58
    if candidate - y0 <= max(3, int(0.03 * (y1 - y0))):
        confidence = 0.62
    return {
        "status": "generated_proposal",
        "yPx": float(candidate) + 0.5,
        "confidence": round(confidence, 3),
        "basis": ["silhouette_contiguous_width_profile"],
        "thresholdPx": round(threshold, 3),
    }


def estimate_root_and_ground(alpha: np.ndarray, neutral_stature_px: float) -> dict[str, Any]:
    bbox = alpha_bbox(alpha, 8)
    if bbox is None:
        return {"status": "unavailable", "reason": "empty_alpha"}
    x0, y0, x1, y1 = bbox
    head = estimate_head_top(alpha)
    head_y = float(head.get("yPx", y0 + 0.5))
    ground_y = float(y1 - 1) + 0.5
    apparent_height = max(1.0, ground_y - head_y)
    root_y_prior = head_y + 0.55 * apparent_height
    band_half = max(2, int(round(0.035 * neutral_stature_px)))
    y_start = max(y0, int(math.floor(root_y_prior)) - band_half)
    y_end = min(y1, int(math.ceil(root_y_prior)) + band_half + 1)
    band = alpha[y_start:y_end] >= 8
    ys, xs = np.nonzero(band)
    if len(xs):
        weights = alpha[y_start:y_end][ys, xs].astype(np.float64)
        root_x = float(np.average(xs + 0.5, weights=weights))
        root_y = float(np.average(ys + y_start + 0.5, weights=weights))
    else:
        root_x = (x0 + x1) * 0.5
        root_y = root_y_prior
    return {
        "status": "generated_proposal",
        "pelvisCenterPx": {"x": round(root_x, 4), "y": round(root_y, 4)},
        "groundYPx": round(ground_y, 4),
        "apparentHeadToGroundPx": round(apparent_height, 4),
        "confidence": 0.56,
        "basis": [
            "silhouette_head_candidate",
            "pelvis_height_prior",
            "alpha_weighted_medial_band",
            "lowest_alpha_envelope",
        ],
    }


def contact_clusters(alpha: np.ndarray, root_x: float) -> list[dict[str, Any]]:
    bbox = alpha_bbox(alpha, 8)
    if bbox is None:
        return []
    x0, y0, x1, y1 = bbox
    band_height = max(2, int(math.ceil(0.005 * (y1 - y0))))
    band = np.any(alpha[max(y0, y1 - band_height) : y1, x0:x1] >= 8, axis=0)
    padded = np.pad(band.astype(np.int8), (1, 1))
    changes = np.diff(padded)
    starts = np.flatnonzero(changes == 1)
    ends = np.flatnonzero(changes == -1)
    clusters: list[dict[str, Any]] = []
    merge_gap = max(2, int(0.01 * (y1 - y0)))
    for start, end in zip(starts, ends):
        sx0, sx1 = int(start + x0), int(end + x0)
        if clusters and sx0 - clusters[-1]["xEndPx"] <= merge_gap:
            clusters[-1]["xEndPx"] = sx1
            clusters[-1]["xCenterPx"] = round(
                (clusters[-1]["xStartPx"] + sx1) * 0.5, 4
            )
            continue
        center = (sx0 + sx1) * 0.5
        clusters.append(
            {
                "xStartPx": sx0,
                "xEndPx": sx1,
                "xCenterPx": round(center, 4),
                "screenSide": "left" if center < root_x else "right",
                "state": "ground_envelope_candidate",
                "confidence": 0.62,
            }
        )
    return clusters


def _component_summary(mask: np.ndarray) -> dict[str, Any]:
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    sizes: list[int] = []
    for y in range(height):
        for x in range(width):
            if not mask[y, x] or visited[y, x]:
                continue
            queue: deque[tuple[int, int]] = deque([(y, x)])
            visited[y, x] = True
            size = 0
            while queue:
                cy, cx = queue.popleft()
                size += 1
                for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                    if (
                        0 <= ny < height
                        and 0 <= nx < width
                        and mask[ny, nx]
                        and not visited[ny, nx]
                    ):
                        visited[ny, nx] = True
                        queue.append((ny, nx))
            sizes.append(size)
    sizes.sort(reverse=True)
    total = sum(sizes)
    detached = sum(sizes[1:]) if len(sizes) > 1 else 0
    return {
        "count": len(sizes),
        "largestArea": sizes[0] if sizes else 0,
        "detachedAreaRatio": round(detached / total, 6) if total else 0.0,
    }


def foreground_evidence(rgba: np.ndarray) -> dict[str, Any]:
    alpha = rgba[:, :, 3]
    height, width = alpha.shape
    bboxes = {
        str(threshold): list(bbox) if (bbox := alpha_bbox(alpha, threshold)) else None
        for threshold in (1, 8, 128)
    }
    transparent = alpha == 0
    transparent_rgb_nonzero = int(np.count_nonzero(rgba[:, :, :3][transparent]))
    thumbnail = Image.fromarray((alpha >= 8).astype(np.uint8) * 255, mode="L")
    thumbnail.thumbnail((384, 384), Image.Resampling.NEAREST)
    components = _component_summary(np.asarray(thumbnail) > 0)
    return {
        "widthPx": width,
        "heightPx": height,
        "mode": "RGBA",
        "alphaCounts": {
            "zero": int(np.count_nonzero(alpha == 0)),
            "partial": int(np.count_nonzero((alpha > 0) & (alpha < 255))),
            "opaque": int(np.count_nonzero(alpha == 255)),
        },
        "alphaBboxByThreshold": bboxes,
        "borderAlphaMax": {
            "top": int(alpha[0, :].max()),
            "right": int(alpha[:, -1].max()),
            "bottom": int(alpha[-1, :].max()),
            "left": int(alpha[:, 0].max()),
        },
        "transparentRgbNonzeroChannelCount": transparent_rgb_nonzero,
        "foregroundCoverage": round(int(np.count_nonzero(alpha)) / (width * height), 8),
        "componentsAtAlpha8Thumbnail": components,
    }


def _srgb_to_linear(rgb: np.ndarray) -> np.ndarray:
    return np.where(
        rgb <= 0.04045,
        rgb / 12.92,
        ((rgb + 0.055) / 1.055) ** 2.4,
    )


def _linear_to_srgb(rgb: np.ndarray) -> np.ndarray:
    return np.where(
        rgb <= 0.0031308,
        rgb * 12.92,
        1.055 * np.power(np.maximum(rgb, 0.0), 1.0 / 2.4) - 0.055,
    )


def resize_premultiplied_linear(rgba: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    target_w, target_h = size
    source_h, source_w = rgba.shape[:2]
    if (source_w, source_h) == (target_w, target_h):
        result = rgba.copy()
        result[result[:, :, 3] == 0, :3] = 0
        return result
    alpha = rgba[:, :, 3].astype(np.float32) / 255.0
    rgb = _srgb_to_linear(rgba[:, :, :3].astype(np.float32) / 255.0)
    premultiplied = rgb * alpha[:, :, None]
    resized_channels: list[np.ndarray] = []
    for channel in range(3):
        plane = Image.fromarray(premultiplied[:, :, channel].astype(np.float32), mode="F")
        resized_channels.append(
            np.asarray(plane.resize(size, Image.Resampling.LANCZOS), dtype=np.float32)
        )
    alpha_plane = Image.fromarray(alpha.astype(np.float32), mode="F")
    resized_alpha = np.asarray(
        alpha_plane.resize(size, Image.Resampling.LANCZOS), dtype=np.float32
    )
    resized_alpha = np.clip(resized_alpha, 0.0, 1.0)
    resized_premultiplied = np.stack(resized_channels, axis=2)
    resized_premultiplied = np.clip(
        resized_premultiplied, 0.0, resized_alpha[:, :, None]
    )
    linear_rgb = np.zeros_like(resized_premultiplied)
    visible = resized_alpha > (0.5 / 255.0)
    linear_rgb[visible] = (
        resized_premultiplied[visible] / resized_alpha[visible, None]
    )
    srgb = np.clip(_linear_to_srgb(linear_rgb), 0.0, 1.0)
    result = np.empty((target_h, target_w, 4), dtype=np.uint8)
    result[:, :, :3] = np.rint(srgb * 255.0).astype(np.uint8)
    result[:, :, 3] = np.rint(resized_alpha * 255.0).astype(np.uint8)
    result[result[:, :, 3] == 0, :3] = 0
    return result


def place_on_canvas(
    rgba: np.ndarray,
    canvas_size: tuple[int, int],
    top_left: tuple[int, int],
) -> tuple[np.ndarray, bool]:
    canvas_w, canvas_h = canvas_size
    x, y = top_left
    height, width = rgba.shape[:2]
    canvas = np.zeros((canvas_h, canvas_w, 4), dtype=np.uint8)
    src_x0 = max(0, -x)
    src_y0 = max(0, -y)
    src_x1 = min(width, canvas_w - x)
    src_y1 = min(height, canvas_h - y)
    foreground_bbox = alpha_bbox(rgba[:, :, 3], 1)
    clipped = bool(
        foreground_bbox
        and (
            foreground_bbox[0] < src_x0
            or foreground_bbox[1] < src_y0
            or foreground_bbox[2] > src_x1
            or foreground_bbox[3] > src_y1
        )
    )
    if src_x1 > src_x0 and src_y1 > src_y0:
        dst_x0 = x + src_x0
        dst_y0 = y + src_y0
        canvas[dst_y0 : dst_y0 + (src_y1 - src_y0), dst_x0 : dst_x0 + (src_x1 - src_x0)] = rgba[
            src_y0:src_y1, src_x0:src_x1
        ]
    return canvas, clipped


def decoded_pixel_sha256(rgba: np.ndarray) -> str:
    header = f"RGBA:{rgba.shape[1]}x{rgba.shape[0]}:".encode("ascii")
    return hashlib.sha256(header + rgba.tobytes(order="C")).hexdigest()


def output_image_evidence(rgba: np.ndarray, safe_margin_px: int) -> dict[str, Any]:
    evidence = foreground_evidence(rgba)
    alpha = rgba[:, :, 3]
    bbox = alpha_bbox(alpha, 1)
    canvas_h, canvas_w = alpha.shape
    inside_safe = False
    if bbox:
        x0, y0, x1, y1 = bbox
        inside_safe = (
            x0 >= safe_margin_px
            and y0 >= safe_margin_px
            and x1 <= canvas_w - safe_margin_px
            and y1 <= canvas_h - safe_margin_px
        )
    evidence["safeMarginPx"] = safe_margin_px
    evidence["foregroundInsideSafeRectangle"] = inside_safe
    evidence["decodedPixelSha256"] = decoded_pixel_sha256(rgba)
    return evidence
