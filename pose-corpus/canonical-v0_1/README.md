# Canonical Pose Corpus v0.1

This directory contains the tracked contract, provenance, metadata, manifests, and QA summary for `canonical_female_pose_corpus_v0_1`.

Current reality:

- **IMPLEMENTED / TESTED:** 123 registered source states, deterministic data-driven ingestion, 123 external fixed-canvas candidates, 123 transform-QA passes, and eight external QA sheets.
- **DESIGNED:** Versioned coordinate, orientation, landmark, export, storage, QA, proposal/override, and future-package contracts.
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

See [the full contract](../../docs/pose-corpus/CANONICAL_POSE_CORPUS_V0_1.md). Generated rasters are intentionally external; see [normalized/README.md](normalized/README.md).
