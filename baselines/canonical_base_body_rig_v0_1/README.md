# Canonical Base Body Rig v0.1

This package is the body-only foundation for a modular 2D character system.

It contains one standardized, headless anatomical mannequin expressed in three anchor views:

- Front
- 3/4 Side
- Back

Each view uses the same semantic pivot IDs and the same 15-part hierarchy. The body is intentionally smooth and non-explicit so future head, hair, clothing, footwear, and accessory packs can attach without being baked into the anatomy.

## What is included

- 45 aligned transparent PNG layers: 15 parts × 3 views
- 45 cropped transparent PNG layers with local pivot coordinates
- 45 alpha masks
- 45 diagnostic outline layers
- one shared `manifest.json`
- interactive browser rig viewer
- neutral, diagnostic, isolated-part, and articulation-test previews
- source-frame mapping documentation
- reproducible build and validation scripts

## Body hierarchy

```text
root
└── pelvis
    ├── thigh_L → calf_L → foot_L
    ├── thigh_R → calf_R → foot_R
    └── mid_torso
        └── chest
            ├── upper_arm_L → forearm_L → hand_L
            └── upper_arm_R → forearm_R → hand_R
```

The `neck_socket` is present as a stable pivot, but no head is attached.

## Run the interactive viewer

### Windows

Double-click:

```text
RUN_BODY_RIG.bat
```

Or use PowerShell:

```powershell
cd "$HOME\Downloads\canonical_base_body_rig_v0_1"
py -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

The viewer supports:

- switching Front / 3/4 / Back while preserving joint IDs
- rotating every separated body segment
- draggable pivot controls
- pose presets
- part-boundary diagnostics
- PNG export
- pose JSON save/load

## Important scope boundary

This is an engineering and standardization pass, not the final painted character surface.

It deliberately excludes:

- heads and faces
- hair
- clothes
- shoes
- accessories

Those systems should be built as independent modules against this rig contract.
