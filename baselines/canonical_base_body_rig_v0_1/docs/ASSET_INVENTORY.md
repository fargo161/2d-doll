# Asset Inventory

For each of the three views, the package includes:

- `aligned/` — each part on the common 1000 × 1700 canvas
- `cropped/` — tightly cropped individual parts
- `masks/` — alpha masks used to construct and revise parts
- `outlines/` — color-coded diagnostic boundaries

There are 15 body components per view and 45 components total.

The aligned files are easiest for immediate canvas compositing. The cropped files are better for other engines; use `pivotInCrop` from `manifest.json` when importing them.

See `PART_INVENTORY.csv` for parent, pivot, z-order, limits, and asset paths. See `PIVOT_TABLE.csv` for cross-view coordinates.
