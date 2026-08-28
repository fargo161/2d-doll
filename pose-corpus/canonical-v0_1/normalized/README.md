# Generated render boundary

Normalized candidate PNGs are generated outside Git. This directory tracks only `render-manifest.json`.

Each manifest output path is relative to a caller-supplied artifact root:

- `review/previews/<set>/<entryId>.png` for review-required candidates;
- `qa/quarantine/<set>/<entryId>.png` for blocked source defects;
- `qa/*.jpg` and matching `qa/*.json` for visual evidence.

The local external `run-manifest.json` may record the absolute artifact root, but it is not committed. Source archives also remain external and immutable. A raster passing transform QA is still a candidate, not an accepted mechanical pose or workflow-validated asset.
