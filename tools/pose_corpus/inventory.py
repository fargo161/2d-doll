from __future__ import annotations

import hashlib
import json
import re
import stat
import zipfile
from io import BytesIO
from pathlib import Path, PurePosixPath
from typing import Any

import numpy as np
from jsonschema import Draft202012Validator
from PIL import Image

from .contracts import (
    CORPUS_ID,
    SOURCE_CONFIG_RELATIVE,
    SOURCE_CONFIG_SCHEMA_RELATIVE,
    SOURCE_MANIFEST_SCHEMA_VERSION,
)
from .image_ops import decode_image, foreground_evidence, rgba_array


class CorpusInputError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def canonical_json_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def _require_unique_config_values(
    values: list[str], label: str
) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        raise CorpusInputError(
            f"duplicate {label} values are not allowed: {duplicates}"
        )


def load_source_config(repository_root: Path) -> dict[str, Any]:
    path = repository_root / SOURCE_CONFIG_RELATIVE
    config = json.loads(path.read_text(encoding="utf-8"))
    schema_path = repository_root / SOURCE_CONFIG_SCHEMA_RELATIVE
    if not schema_path.is_file():
        raise CorpusInputError(f"source config schema is missing: {schema_path}")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(config),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        raise CorpusInputError(
            f"source config schema violation at {location}: {error.message}"
        )
    source_sets = config["sourceSets"]
    for field in ("sourceSetId", "pathKey", "entryPrefix"):
        _require_unique_config_values(
            [source_set[field] for source_set in source_sets], field
        )
    _require_unique_config_values(
        [
            group["groupId"]
            for source_set in source_sets
            for group in source_set["calibrationGroups"]
        ],
        "calibration groupId",
    )
    return config


def _validate_member(info: zipfile.ZipInfo) -> None:
    name = info.filename
    if "\\" in name:
        raise CorpusInputError(f"unsafe backslash ZIP member path: {name}")
    pure = PurePosixPath(name)
    if pure.is_absolute() or ".." in pure.parts:
        raise CorpusInputError(f"unsafe ZIP member path: {name}")
    if info.flag_bits & 0x1:
        raise CorpusInputError(f"encrypted ZIP member is not allowed: {name}")
    unix_mode = (info.external_attr >> 16) & 0xFFFF
    if stat.S_ISLNK(unix_mode):
        raise CorpusInputError(f"symlink ZIP member is not allowed: {name}")
    if info.file_size > 1024 * 1024 and info.compress_size:
        ratio = info.file_size / info.compress_size
        if ratio > 1000:
            raise CorpusInputError(f"suspicious compression ratio for {name}: {ratio:.1f}")


def _members_for_layer(
    names: list[str], layer: dict[str, Any]
) -> dict[str, str]:
    prefix = layer["prefix"]
    suffix = layer["suffix"].lower()
    depth = int(layer["depth"])
    result: dict[str, str] = {}
    for name in names:
        if not name.startswith(prefix) or not name.lower().endswith(suffix):
            continue
        if len(PurePosixPath(name).parts) != depth:
            continue
        basename = PurePosixPath(name).name
        if basename in result:
            raise CorpusInputError(
                f"duplicate basename {basename} in layer {layer['layerId']}"
            )
        result[basename] = name
    return result


def _manifest_record(source_manifest: dict[str, Any], basename: str) -> Any:
    records = source_manifest.get("records", source_manifest.get("files", []))
    for record in records:
        if not isinstance(record, dict):
            continue
        for key in ("file", "filename", "name", "path"):
            value = record.get(key)
            if value and PurePosixPath(str(value)).name == basename:
                return record
    return None


def _image_artifact(
    archive: zipfile.ZipFile,
    source_set_id: str,
    entry_id: str,
    basename: str,
    member_path: str,
    layer: dict[str, Any],
) -> tuple[dict[str, Any], bytes]:
    data = archive.read(member_path)
    image = decode_image(data)
    artifact: dict[str, Any] = {
        "artifactId": f"{entry_id}.{layer['layerId']}",
        "sourceSetId": source_set_id,
        "role": layer["role"],
        "archiveMemberPath": member_path,
        "basename": basename,
        "sha256": sha256_bytes(data),
        "image": {
            "widthPx": image.width,
            "heightPx": image.height,
            "mode": image.mode,
        },
    }
    if image.mode == "RGBA":
        artifact["foregroundEvidence"] = foreground_evidence(
            np.asarray(image, dtype=np.uint8)
        )
    elif image.mode == "L":
        mask = np.asarray(image, dtype=np.uint8)
        artifact["maskEvidence"] = {
            "zero": int(np.count_nonzero(mask == 0)),
            "partial": int(np.count_nonzero((mask > 0) & (mask < 255))),
            "opaque": int(np.count_nonzero(mask == 255)),
        }
    return artifact, data


def _parse_identity(source_set: dict[str, Any], basename: str) -> dict[str, Any]:
    match = re.fullmatch(source_set["filenamePattern"], basename)
    if not match:
        raise CorpusInputError(
            f"production filename does not match descriptor pattern: {basename}"
        )
    parsed = match.groupdict()
    ordinal = int(parsed["ordinal"])
    if not 1 <= ordinal <= 999:
        raise CorpusInputError(
            f"pose ordinal must be between 1 and 999: {basename}"
        )
    entry_id = f"{source_set['entryPrefix']}{ordinal:03d}"
    sequence = parsed.get("sequence")
    if sequence in {"A", "B"}:
        sequence = f"video{sequence}"
    return {
        "entryId": entry_id,
        "ordinal": ordinal,
        "sourceSequence": {
            "sequenceId": sequence,
            "sequenceOrdinal": (
                int(parsed["sequenceOrdinal"])
                if parsed.get("sequenceOrdinal")
                else None
            ),
            "frameNumber": int(parsed["frame"]) if parsed.get("frame") else None,
            "timeSeconds": None,
        },
        "originalLabel": parsed.get("label", "unknown"),
    }


def _known_issues(
    source_set: dict[str, Any], member_path: str, source_hash: str
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for issue in source_set.get("knownIssues", []):
        if issue["memberPath"] != member_path:
            continue
        if issue["sourceSha256"] != source_hash:
            issues.append(
                {
                    "code": "KNOWN_ISSUE_HASH_GUARD_MISMATCH",
                    "severity": "error",
                    "detail": "The configured issue disposition does not match this source content hash.",
                    "expectedSourceSha256": issue["sourceSha256"],
                    "actualSourceSha256": source_hash,
                    "disposition": "review_required",
                }
            )
            continue
        issues.append(
            {
                "code": issue["code"],
                "severity": issue["severity"],
                "detail": issue["detail"],
                "sourceSha256": source_hash,
                "disposition": issue["disposition"],
            }
        )
    return issues


def _unresolved_claims(
    source_set: dict[str, Any], ordinal: int
) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    for claim in source_set.get("unresolvedClaims", []):
        if ordinal in claim.get("ordinals", []):
            claims.append(
                {
                    "code": claim["code"],
                    "detail": claim["detail"],
                    "status": "unverified_claim",
                }
            )
    return claims


def _calibration_group(source_set: dict[str, Any], basename: str) -> str:
    matches = [
        group["groupId"]
        for group in source_set["calibrationGroups"]
        if re.fullmatch(group["matchPattern"], basename)
    ]
    if len(matches) != 1:
        raise CorpusInputError(
            f"expected one calibration group for {basename}; found {matches}"
        )
    return matches[0]


def collect_inventory(
    repository_root: Path, source_directory: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    config = load_source_config(repository_root)
    source_sets_out: list[dict[str, Any]] = []
    entries_out: list[dict[str, Any]] = []
    runtime_index: dict[str, Any] = {"archives": {}, "entries": {}}

    for source_set in config["sourceSets"]:
        archive_path = source_directory / source_set["archiveFilename"]
        if not archive_path.is_file():
            raise CorpusInputError(f"source archive is missing: {archive_path}")
        archive_hash = sha256_file(archive_path)
        if archive_hash != source_set["archiveSha256"]:
            raise CorpusInputError(
                f"archive hash mismatch for {source_set['archiveFilename']}: {archive_hash}"
            )
        with zipfile.ZipFile(archive_path) as archive:
            bad_member = archive.testzip()
            if bad_member:
                raise CorpusInputError(f"ZIP CRC failure: {bad_member}")
            infos = archive.infolist()
            for info in infos:
                _validate_member(info)
            file_infos = [info for info in infos if not info.is_dir()]
            names = sorted(info.filename for info in file_infos)
            if len(names) != len(set(names)):
                raise CorpusInputError(
                    f"duplicate member paths in {source_set['archiveFilename']}"
                )
            lowered = [name.casefold() for name in names]
            if len(lowered) != len(set(lowered)):
                raise CorpusInputError(
                    f"case-colliding member paths in {source_set['archiveFilename']}"
                )

            source_manifest_path = source_set.get("sourceManifestPath")
            if source_manifest_path is None:
                source_manifest_bytes = b""
                source_manifest: dict[str, Any] = {}
            else:
                if source_manifest_path not in names:
                    raise CorpusInputError(
                        f"source manifest is missing: {source_manifest_path}"
                    )
                source_manifest_bytes = archive.read(source_manifest_path)
                source_manifest = json.loads(source_manifest_bytes)
            layer_members = {
                layer["layerId"]: _members_for_layer(names, layer)
                for layer in source_set["layers"]
            }
            mechanics_layers = [
                layer for layer in source_set["layers"] if layer["mechanicsInput"]
            ]
            render_layers = [
                layer for layer in source_set["layers"] if layer["normalizationInput"]
            ]
            if len(mechanics_layers) != 1 or len(render_layers) != 1:
                raise CorpusInputError(
                    f"{source_set['sourceSetId']} requires exactly one mechanics and one normalization input layer"
                )
            mechanics_layer = mechanics_layers[0]
            render_layer = render_layers[0]
            mechanics_members = layer_members[mechanics_layer["layerId"]]
            if len(mechanics_members) != source_set["expectedPoseCount"]:
                raise CorpusInputError(
                    f"{source_set['sourceSetId']} expected {source_set['expectedPoseCount']} poses; "
                    f"found {len(mechanics_members)}"
                )
            if set(layer_members[render_layer["layerId"]]) != set(mechanics_members):
                raise CorpusInputError(
                    f"normalization layer does not pair exactly in {source_set['sourceSetId']}"
                )

            source_evidence: list[dict[str, Any]] = []
            production_paths = {
                path for members in layer_members.values() for path in members.values()
            }
            for member_path in names:
                if member_path in production_paths:
                    continue
                data = archive.read(member_path)
                source_evidence.append(
                    {
                        "archiveMemberPath": member_path,
                        "sha256": sha256_bytes(data),
                        "authoritative": member_path == source_manifest_path,
                        "role": (
                            "source_manifest"
                            if member_path == source_manifest_path
                            else "source_qa_or_context"
                        ),
                    }
                )

            ordered_basenames = sorted(
                mechanics_members,
                key=lambda name: _parse_identity(source_set, name)["ordinal"],
            )
            for basename in ordered_basenames:
                identity = _parse_identity(source_set, basename)
                entry_id = identity["entryId"]
                artifacts: list[dict[str, Any]] = []
                artifact_bytes: dict[str, bytes] = {}
                for layer in source_set["layers"]:
                    member_path = layer_members[layer["layerId"]].get(basename)
                    if not member_path:
                        if layer.get("optional", False):
                            continue
                        raise CorpusInputError(
                            f"missing {layer['layerId']} for {basename}"
                        )
                    artifact, data = _image_artifact(
                        archive,
                        source_set["sourceSetId"],
                        entry_id,
                        basename,
                        member_path,
                        layer,
                    )
                    artifacts.append(artifact)
                    artifact_bytes[layer["role"]] = data

                mechanics_artifact = next(
                    artifact
                    for artifact in artifacts
                    if artifact["role"] == mechanics_layer["role"]
                )
                render_artifact = next(
                    artifact
                    for artifact in artifacts
                    if artifact["role"] == render_layer["role"]
                )
                mask_artifacts = [
                    artifact
                    for artifact in artifacts
                    if artifact["role"] == "source_alpha_mask"
                ]
                mask_matches = None
                if mask_artifacts:
                    mechanics_rgba = rgba_array(
                        artifact_bytes[mechanics_layer["role"]]
                    )
                    with Image.open(BytesIO(artifact_bytes["source_alpha_mask"])) as mask_image:
                        mask = np.asarray(mask_image.convert("L"), dtype=np.uint8)
                    mask_matches = bool(
                        mask.shape == mechanics_rgba[:, :, 3].shape
                        and np.array_equal(mask, mechanics_rgba[:, :, 3])
                    )
                    if not mask_matches:
                        raise CorpusInputError(f"alpha mask mismatch for {entry_id}")

                issues = _known_issues(
                    source_set,
                    mechanics_artifact["archiveMemberPath"],
                    mechanics_artifact["sha256"],
                )
                cleanup_history: list[dict[str, Any]] = []
                corrections = source_manifest.get("targeted_corrections", {})
                if basename in corrections:
                    cleanup_history.append(
                        {
                            "kind": "same_package_targeted_reconstruction",
                            "claims": corrections[basename],
                            "source": source_manifest_path,
                            "verificationStatus": "manifest_claim_structurally_preserved",
                        }
                    )
                manifest_record = _manifest_record(source_manifest, basename)
                entry = {
                    **identity,
                    "sourceSetId": source_set["sourceSetId"],
                    "pathKey": source_set["pathKey"],
                    "archive": {
                        "filename": source_set["archiveFilename"],
                        "sha256": archive_hash,
                    },
                    "calibrationGroupId": _calibration_group(source_set, basename),
                    "artifacts": artifacts,
                    "mechanicsArtifactId": mechanics_artifact["artifactId"],
                    "normalizationArtifactId": render_artifact["artifactId"],
                    "maskMatchesMechanicsAlpha": mask_matches,
                    "sourceManifestRecord": manifest_record,
                    "cleanupHistory": cleanup_history,
                    "unresolvedClaims": _unresolved_claims(
                        source_set, identity["ordinal"]
                    ),
                    "issues": issues,
                    "extensions": {},
                }
                entries_out.append(entry)
                runtime_index["entries"][entry_id] = {
                    "archivePath": archive_path,
                    "mechanicsMemberPath": mechanics_artifact["archiveMemberPath"],
                    "normalizationMemberPath": render_artifact["archiveMemberPath"],
                    "sourceSet": source_set,
                }

            source_sets_out.append(
                {
                    "sourceSetId": source_set["sourceSetId"],
                    "pathKey": source_set["pathKey"],
                    "archive": {
                        "filename": source_set["archiveFilename"],
                        "sha256": archive_hash,
                        "sizeBytes": archive_path.stat().st_size,
                        "storageClass": "external_immutable",
                        "committed": False,
                    },
                    "sourceManifest": (
                        {
                            "archiveMemberPath": source_manifest_path,
                            "sha256": sha256_bytes(source_manifest_bytes),
                        }
                        if source_manifest_path is not None
                        else None
                    ),
                    "registeredCount": source_set["expectedPoseCount"],
                    "sourceEvidenceArtifacts": source_evidence,
                    "extensions": {},
                }
            )
            runtime_index["archives"][source_set["sourceSetId"]] = archive_path

    entries_out.sort(key=lambda entry: entry["entryId"])
    expected_total = sum(
        int(source_set["expectedPoseCount"]) for source_set in config["sourceSets"]
    )
    if (
        len(entries_out) != expected_total
        or len({entry["entryId"] for entry in entries_out}) != expected_total
    ):
        raise CorpusInputError(
            f"descriptor expects {expected_total} unique entries; found {len(entries_out)}"
        )
    manifest = {
        "schemaVersion": SOURCE_MANIFEST_SCHEMA_VERSION,
        "corpusId": CORPUS_ID,
        "sourceConfigSha256": canonical_json_sha256(config),
        "sourceSets": source_sets_out,
        "entries": entries_out,
        "counts": {
            "registered": len(entries_out),
            "bySourceSet": {
                source_set["sourceSetId"]: source_set["registeredCount"]
                for source_set in source_sets_out
            },
        },
        "extensions": {},
    }
    return manifest, runtime_index


def read_runtime_artifact(runtime_record: dict[str, Any], role: str) -> bytes:
    member_key = (
        "mechanicsMemberPath" if role == "mechanics" else "normalizationMemberPath"
    )
    with zipfile.ZipFile(runtime_record["archivePath"]) as archive:
        return archive.read(runtime_record[member_key])
