# Canonical Pose Corpus v0.1

This directory contains the tracked contract, provenance, metadata, manifests, and QA summary for `canonical_female_pose_corpus_v0_1`.

Current reality:

- **IMPLEMENTED / TESTED:** 132 registered source states, an explicit calibration/frozen-ingestion boundary, 132 external fixed-canvas candidates across artifact sets, 131 transform-QA passes, one structured safe-margin review condition, and 16 external QA artifacts.
- **DESIGNED:** Versioned coordinate, orientation, landmark, export, storage, QA, and proposal/override contracts.
- **UNRESOLVED:** All anatomical landmarks, canonical body-proportion measurements, anatomical contacts, reviewed local retargeting, and runtime conversion.
- **ACCEPTED / VALIDATED:** No entries or renders.

Key files:

- `corpus.json` — top-level corpus boundary and reality state.
- `spec/` — source descriptors and canonical machine-readable contracts.
- `schemas/` — JSON Schemas for descriptors and generated records.
- `sources/source-manifest.json` — immutable source provenance and hashes.
- `metadata/proposals/` — generated, review-required observations.
- `overrides/` — independent human-editable override layer, currently empty/unreviewed.
- `metadata/poses/` — corpus entries with explicit unresolved mechanics.
- `metadata/corpus-index.json` — hash-linked registration index.
- `normalized/render-manifest.json` — external candidate paths, operations, hashes, and raster QA.
- `qa/reports/run-summary.json` — counts, issues, evidence hashes, and verdict.

Full-corpus calibration and future-package ingestion are different operations. Calibration may derive a contract only when explicitly requested; frozen ingestion loads and verifies the pinned v0.1 canvas, renders only selected new source sets, appends aggregate records, and guards all prior per-entry bytes:

```text
python -m tools.pose_corpus calibrate --source-directory <all-source-zips> --artifact-root <new-artifact-root>
python -m tools.pose_corpus ingest --source-directory <new-package-directory> --artifact-root <new-artifact-root> --source-set-id <source-set-id>
```

The legacy full-corpus `run` command now requires `--canvas-policy calibrate`. A frozen-ingestion artifact root must not already exist. Physical overflow stops before mutation; safe-margin overflow remains a structured `CANONICAL_CANVAS_OVERFLOW_REVIEW_REQUIRED` candidate condition.

See [the full contract](../../docs/pose-corpus/CANONICAL_POSE_CORPUS_V0_1.md). Generated rasters are intentionally external; see [normalized/README.md](normalized/README.md).
