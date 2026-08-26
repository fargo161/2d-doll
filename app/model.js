export const VIEW_IDS = ["front", "three_quarter", "back"];

export const VIEW_COMPATIBILITY = Object.freeze({
  front: Object.freeze(["front", "three_quarter"]),
  three_quarter: Object.freeze(["front", "three_quarter", "back"]),
  back: Object.freeze(["three_quarter", "back"]),
});

export function matrix(a = 1, b = 0, c = 0, d = 1, e = 0, f = 0) {
  return [a, b, c, d, e, f];
}

export function multiply(left, right) {
  return [
    left[0] * right[0] + left[2] * right[1],
    left[1] * right[0] + left[3] * right[1],
    left[0] * right[2] + left[2] * right[3],
    left[1] * right[2] + left[3] * right[3],
    left[0] * right[4] + left[2] * right[5] + left[4],
    left[1] * right[4] + left[3] * right[5] + left[5],
  ];
}

export function translate(x, y) {
  return matrix(1, 0, 0, 1, x, y);
}

export function rotate(degrees) {
  const radians = (degrees * Math.PI) / 180;
  const cosine = Math.cos(radians);
  const sine = Math.sin(radians);
  return matrix(cosine, sine, -sine, cosine, 0, 0);
}

export function scale(x, y = x) {
  return matrix(x, 0, 0, y, 0, 0);
}

export function around(pivot, degrees) {
  return multiply(
    multiply(translate(pivot[0], pivot[1]), rotate(degrees)),
    translate(-pivot[0], -pivot[1]),
  );
}

export function transformPoint(transform, point) {
  return {
    x: transform[0] * point.x + transform[2] * point.y + transform[4],
    y: transform[1] * point.x + transform[3] * point.y + transform[5],
  };
}

export function invert(transform) {
  const determinant = transform[0] * transform[3] - transform[1] * transform[2];
  if (Math.abs(determinant) < 1e-9) {
    throw new Error("Cannot invert a singular transform.");
  }
  return [
    transform[3] / determinant,
    -transform[1] / determinant,
    -transform[2] / determinant,
    transform[0] / determinant,
    (transform[2] * transform[5] - transform[3] * transform[4]) / determinant,
    (transform[1] * transform[4] - transform[0] * transform[5]) / determinant,
  ];
}

export function clamp(value, minimum, maximum) {
  return Math.max(minimum, Math.min(maximum, value));
}

export function normalizeAngleDelta(degrees) {
  let normalized = degrees;
  while (normalized > 180) normalized -= 360;
  while (normalized < -180) normalized += 360;
  return normalized;
}

function identityMapping(limits) {
  return {
    offset: 0,
    scale: 1,
    visualMin: limits[0],
    visualMax: limits[1],
  };
}

function elbowMapping(partId, viewId) {
  const back = viewId === "back";
  const anatomicalLeft = partId === "forearm_L";
  const direction = anatomicalLeft !== back ? 1 : -1;
  return {
    offset: 0,
    scale: direction * 112,
    visualMin: direction > 0 ? 0 : -112,
    visualMax: direction > 0 ? 112 : 0,
  };
}

export function buildJointDefinitions(rig) {
  const definitions = {};
  const frontParts = rig.views.front.parts;
  for (const [partId, part] of Object.entries(frontParts)) {
    const isElbow = partId === "forearm_L" || partId === "forearm_R";
    const semantic = isElbow
      ? { minimum: 0, maximum: 1, neutral: 0, unit: "flexion", transitional: false }
      : {
          minimum: part.rotationLimitsDeg[0],
          maximum: part.rotationLimitsDeg[1],
          neutral: 0,
          unit: "degrees",
          transitional: true,
        };
    const viewMappings = {};
    for (const viewId of VIEW_IDS) {
      viewMappings[viewId] = isElbow
        ? elbowMapping(partId, viewId)
        : identityMapping(rig.views[viewId].parts[partId].rotationLimitsDeg);
    }
    definitions[partId] = {
      partId,
      pivotId: part.pivotId,
      parentId: part.parent,
      semantic,
      viewMappings,
    };
  }
  return definitions;
}

export function semanticToVisual(definition, viewId, semanticValue) {
  const value = clamp(
    semanticValue,
    definition.semantic.minimum,
    definition.semantic.maximum,
  );
  const mapping = definition.viewMappings[viewId];
  return clamp(
    mapping.offset + mapping.scale * value,
    mapping.visualMin,
    mapping.visualMax,
  );
}

export function visualToSemantic(definition, viewId, visualAngle) {
  const mapping = definition.viewMappings[viewId];
  const visual = clamp(visualAngle, mapping.visualMin, mapping.visualMax);
  if (Math.abs(mapping.scale) < 1e-9) return definition.semantic.neutral;
  return clamp(
    (visual - mapping.offset) / mapping.scale,
    definition.semantic.minimum,
    definition.semantic.maximum,
  );
}

export function createInitialState(rig, viewport = { width: 1100, height: 760 }) {
  const joints = {};
  for (const [partId, definition] of Object.entries(rig.joints)) {
    joints[partId] = definition.semantic.neutral;
  }
  return {
    pose: {
      schemaVersion: "2d-doll-pose-0.1",
      viewId: "front",
      joints,
      depthOverrides: {},
    },
    character: {
      x: 0,
      y: 0,
      rotation: 0,
      scale: 1,
      flip: false,
    },
    camera: {
      panX: 0,
      panY: 0,
      zoom: 1,
    },
    editor: {
      tool: "pose",
      selectedJoint: null,
      hoveredJoint: null,
      showHandles: true,
      drag: null,
    },
    viewport: { ...viewport },
  };
}

export function computeBodyMatrices(rig, state) {
  const view = rig.views[state.pose.viewId];
  const body = { root: matrix() };
  const calculate = (partId) => {
    if (body[partId]) return body[partId];
    const part = view.parts[partId];
    const parent = calculate(part.parent);
    const renderedAngle = semanticToVisual(
      rig.joints[partId],
      state.pose.viewId,
      state.pose.joints[partId],
    );
    body[partId] = multiply(parent, around(part.pivot, renderedAngle));
    return body[partId];
  };
  for (const partId of Object.keys(view.parts)) calculate(partId);
  return body;
}

export function characterMatrix(rig, state) {
  const root = rig.views[state.pose.viewId].pivots.root;
  const flipScale = state.character.flip ? -state.character.scale : state.character.scale;
  return multiply(
    multiply(
      multiply(
        translate(state.character.x, state.character.y),
        rotate(state.character.rotation),
      ),
      scale(flipScale, state.character.scale),
    ),
    translate(-root[0], -root[1]),
  );
}

export function cameraMatrix(state) {
  return multiply(
    translate(
      state.viewport.width / 2 + state.camera.panX,
      state.viewport.height / 2 + state.camera.panY,
    ),
    scale(state.camera.zoom),
  );
}

export function screenMatrix(rig, state) {
  return multiply(cameraMatrix(state), characterMatrix(rig, state));
}

export function parentMatrixForPart(rig, state, bodyMatrices, partId) {
  const parentId = rig.views[state.pose.viewId].parts[partId].parent;
  return parentId === "root" ? matrix() : bodyMatrices[parentId];
}

export function pointerInParentRigSpace(rig, state, bodyMatrices, partId, screenPoint) {
  const parent = parentMatrixForPart(rig, state, bodyMatrices, partId);
  const parentToScreen = multiply(screenMatrix(rig, state), parent);
  return transformPoint(invert(parentToScreen), screenPoint);
}

function includePoint(bounds, point) {
  bounds.minX = Math.min(bounds.minX, point.x);
  bounds.minY = Math.min(bounds.minY, point.y);
  bounds.maxX = Math.max(bounds.maxX, point.x);
  bounds.maxY = Math.max(bounds.maxY, point.y);
}

export function characterWorldBounds(rig, state, bodyMatrices = computeBodyMatrices(rig, state)) {
  const view = rig.views[state.pose.viewId];
  const character = characterMatrix(rig, state);
  const bounds = {
    minX: Number.POSITIVE_INFINITY,
    minY: Number.POSITIVE_INFINITY,
    maxX: Number.NEGATIVE_INFINITY,
    maxY: Number.NEGATIVE_INFINITY,
  };
  for (const [partId, part] of Object.entries(view.parts)) {
    const [x, y, width, height] = part.crop;
    const partToWorld = multiply(character, bodyMatrices[partId]);
    for (const corner of [
      { x, y },
      { x: x + width, y },
      { x: x + width, y: y + height },
      { x, y: y + height },
    ]) {
      includePoint(bounds, transformPoint(partToWorld, corner));
    }
  }
  return bounds;
}

export function boundsToScreen(state, worldBounds) {
  const transform = cameraMatrix(state);
  const first = transformPoint(transform, { x: worldBounds.minX, y: worldBounds.minY });
  const second = transformPoint(transform, { x: worldBounds.maxX, y: worldBounds.maxY });
  return {
    minX: Math.min(first.x, second.x),
    minY: Math.min(first.y, second.y),
    maxX: Math.max(first.x, second.x),
    maxY: Math.max(first.y, second.y),
  };
}

export function fitCameraToBounds(state, worldBounds, padding = 48) {
  const width = Math.max(1, worldBounds.maxX - worldBounds.minX);
  const height = Math.max(1, worldBounds.maxY - worldBounds.minY);
  const usableWidth = Math.max(1, state.viewport.width - padding * 2);
  const usableHeight = Math.max(1, state.viewport.height - padding * 2);
  const zoom = clamp(Math.min(usableWidth / width, usableHeight / height), 0.08, 4);
  const centerX = (worldBounds.minX + worldBounds.maxX) / 2;
  const centerY = (worldBounds.minY + worldBounds.maxY) / 2;
  state.camera.zoom = zoom;
  state.camera.panX = -centerX * zoom;
  state.camera.panY = -centerY * zoom;
  return state.camera;
}

export function setZoomAroundScreenPoint(state, nextZoom, screenPoint) {
  const oldZoom = state.camera.zoom;
  const centerX = state.viewport.width / 2;
  const centerY = state.viewport.height / 2;
  const worldX = (screenPoint.x - centerX - state.camera.panX) / oldZoom;
  const worldY = (screenPoint.y - centerY - state.camera.panY) / oldZoom;
  const zoom = clamp(nextZoom, 0.08, 4);
  state.camera.zoom = zoom;
  state.camera.panX = screenPoint.x - centerX - worldX * zoom;
  state.camera.panY = screenPoint.y - centerY - worldY * zoom;
}

export function resetPose(state, rig) {
  for (const [partId, definition] of Object.entries(rig.joints)) {
    state.pose.joints[partId] = definition.semantic.neutral;
  }
  state.pose.depthOverrides = {};
}

export function resetCharacter(state) {
  Object.assign(state.character, {
    x: 0,
    y: 0,
    rotation: 0,
    scale: 1,
    flip: false,
  });
}

export function resetCamera(state) {
  Object.assign(state.camera, { panX: 0, panY: 0, zoom: 1 });
}

export function serializePose(state) {
  return {
    schemaVersion: state.pose.schemaVersion,
    viewId: state.pose.viewId,
    joints: { ...state.pose.joints },
    depthOverrides: { ...state.pose.depthOverrides },
  };
}

export function deepClone(value) {
  return JSON.parse(JSON.stringify(value));
}
