# Canonical Base Body Rig Specification v0.1

## Objective

Provide one reusable body skeleton with three authored visual orientations while keeping all runtime identifiers stable across views.

## Canvas

- Width: 1000 px
- Height: 1700 px
- Coordinate origin: upper-left
- Neutral root: pelvis center
- Assets: transparent RGBA PNG

## Stable pivot IDs

```text
root
pelvis
waist
chest
neck_socket
shoulder_L
elbow_L
wrist_L
shoulder_R
elbow_R
wrist_R
hip_L
knee_L
ankle_L
hip_R
knee_R
ankle_R
```

`L` and `R` always mean the character's anatomical left and right, not the viewer's screen side. This is why their screen positions reverse in the Back view.

## Part IDs

```text
pelvis
mid_torso
chest
upper_arm_L
forearm_L
hand_L
upper_arm_R
forearm_R
hand_R
thigh_L
calf_L
foot_L
thigh_R
calf_R
foot_R
```

## Hidden-overlap policy

Every limb asset extends beyond its visible joint boundary. Rounded internal overlap zones are included at shoulders, elbows, wrists, hips, knees, and ankles. Torso components also overlap at chest and waist transitions.

The neutral composite therefore does not depend on exact edge-to-edge alignment. Small rotations reveal valid body material rather than immediate transparency.

## View policy

### Front

Measurement authority for overall proportions. Anatomical left appears on the viewer's right.

### 3/4 Side

Faces stage-right. Character-right is treated as the near side. Near-side parts are larger and use a foreground z-order; far-side parts are narrower and pass behind the torso.

### Back

Uses the same body lengths and hierarchy, with rear-specific torso/pelvis contours. Anatomical left appears on the viewer's left.

## Rotation policy

The limits in `manifest.json` are first-pass safe envelopes, not promises that every extreme combination will remain visually perfect. Presets stay inside conservative combinations.

Future passes may add alternate limb sprites or corrective joint patches without changing the stable part or pivot IDs.

## Module attachment points reserved for later

- `neck_socket`: head packs
- chest and shoulders: hair overlap and upper garments
- torso and pelvis: clothing bridges
- wrists: hand variants and accessories
- ankles/feet: footwear packs
