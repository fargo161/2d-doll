import { buildJointDefinitions, VIEW_COMPATIBILITY } from "./model.js";

const BASELINE_ROOT = new URL(
  "../baselines/canonical_base_body_rig_v0_1/",
  import.meta.url,
);
const MANIFEST_URL = new URL("manifest.json", BASELINE_ROOT);

function copyPart(part) {
  return {
    parent: part.parent,
    pivotId: part.pivotId,
    pivot: [...part.pivot],
    crop: [...part.crop],
    zIndex: part.zIndex,
    rotationLimitsDeg: [...part.rotationLimitsDeg],
    assetUrl: new URL(part.assetAligned, BASELINE_ROOT).href,
  };
}

export async function loadRigDefinition() {
  const response = await fetch(MANIFEST_URL);
  if (!response.ok) {
    throw new Error(`Rig manifest failed to load (${response.status}).`);
  }
  const source = await response.json();
  const views = {};
  for (const [viewId, view] of Object.entries(source.views)) {
    const parts = {};
    for (const [partId, part] of Object.entries(view.parts)) {
      parts[partId] = copyPart(part);
    }
    views[viewId] = {
      id: viewId,
      label: view.label,
      facing: view.facing,
      nearSide: view.nearSide,
      pivots: structuredClone(view.pivots),
      parts,
      defaultDepth: Object.fromEntries(
        Object.entries(parts).map(([partId, part]) => [partId, part.zIndex]),
      ),
    };
  }
  const rig = {
    schemaVersion: "2d-doll-rig-0.1",
    sourceSchemaVersion: source.schemaVersion,
    sourceArtwork: "inherited-canonical-base-body-rig-v0.1",
    canvas: structuredClone(source.canvas),
    stablePivotIds: [...source.stablePivotIds],
    views,
    viewCompatibility: VIEW_COMPATIBILITY,
    anchors: {
      neck: { id: "neck_socket", kind: "attachment", rotatesPart: false },
    },
    depth: {
      defaultByView: Object.fromEntries(
        Object.entries(views).map(([viewId, view]) => [viewId, view.defaultDepth]),
      ),
      overrideState: "pose.depthOverrides",
      overrideUiStatus: "DESIGNED_NOT_IMPLEMENTED",
    },
  };
  rig.joints = buildJointDefinitions(rig);
  return rig;
}

export async function loadRigArtwork(rig) {
  const artwork = {};
  const loads = [];
  for (const [viewId, view] of Object.entries(rig.views)) {
    artwork[viewId] = {};
    for (const [partId, part] of Object.entries(view.parts)) {
      loads.push(
        new Promise((resolve, reject) => {
          const image = new Image();
          image.onload = () => {
            artwork[viewId][partId] = image;
            resolve();
          };
          image.onerror = () => reject(new Error(`Artwork failed to load: ${part.assetUrl}`));
          image.src = part.assetUrl;
        }),
      );
    }
  }
  await Promise.all(loads);
  return artwork;
}
