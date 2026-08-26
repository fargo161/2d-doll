import { loadRigArtwork, loadRigDefinition } from "./rig-definition.js";
import {
  boundsToScreen,
  cameraMatrix,
  characterMatrix,
  characterWorldBounds,
  clamp,
  computeBodyMatrices,
  createInitialState,
  deepClone,
  fitCameraToBounds,
  matrix,
  multiply,
  normalizeAngleDelta,
  parentMatrixForPart,
  pointerInParentRigSpace,
  resetCharacter,
  resetPose,
  screenMatrix,
  semanticToVisual,
  serializePose,
  setZoomAroundScreenPoint,
  transformPoint,
  visualToSemantic,
} from "./model.js";

const PART_LABELS = {
  pelvis: "Pelvis",
  mid_torso: "Waist / Mid Torso",
  chest: "Chest / Ribcage",
  upper_arm_L: "Shoulder L",
  forearm_L: "Elbow L Flexion",
  hand_L: "Wrist L",
  upper_arm_R: "Shoulder R",
  forearm_R: "Elbow R Flexion",
  hand_R: "Wrist R",
  thigh_L: "Hip L",
  calf_L: "Knee L",
  foot_L: "Ankle L",
  thigh_R: "Hip R",
  calf_R: "Knee R",
  foot_R: "Ankle R",
};

const GROUPS = {
  Torso: ["pelvis", "mid_torso", "chest"],
  Arms: [
    "upper_arm_L",
    "forearm_L",
    "hand_L",
    "upper_arm_R",
    "forearm_R",
    "hand_R",
  ],
  Legs: ["thigh_L", "calf_L", "foot_L", "thigh_R", "calf_R", "foot_R"],
};

const els = {
  canvas: document.querySelector("#rig-canvas"),
  status: document.querySelector("#status"),
  view: document.querySelector("#view-select"),
  jointControls: document.querySelector("#joint-controls"),
  handles: document.querySelector("#handles-toggle"),
  characterX: document.querySelector("#character-x"),
  characterY: document.querySelector("#character-y"),
  characterScale: document.querySelector("#character-scale"),
  characterRotation: document.querySelector("#character-rotation"),
  characterFlip: document.querySelector("#character-flip"),
  zoomReadout: document.querySelector("#zoom-readout"),
};

const ctx = els.canvas.getContext("2d");
let rig;
let artwork;
let state;
let diagnostics = {
  lifecycle: "not-started",
  handles: [],
  renderedAngles: {},
  screenBounds: null,
};
let spaceHeld = false;

function setStatus(message) {
  els.status.textContent = message;
}

function setLifecycle(lifecycle, message) {
  diagnostics.lifecycle = lifecycle;
  setStatus(message);
}

function setContextTransform(transform) {
  ctx.setTransform(...transform);
}

function partCategory(partId) {
  if (/arm|forearm|hand/.test(partId)) return "arm";
  if (/thigh|calf|foot/.test(partId)) return "leg";
  return "torso";
}

function drawDiamond(x, y, radius, fill, stroke, lineWidth = 2) {
  ctx.beginPath();
  ctx.moveTo(x, y - radius);
  ctx.lineTo(x + radius, y);
  ctx.lineTo(x, y + radius);
  ctx.lineTo(x - radius, y);
  ctx.closePath();
  ctx.fillStyle = fill;
  ctx.fill();
  ctx.strokeStyle = stroke;
  ctx.lineWidth = lineWidth;
  ctx.stroke();
}

function renderBackground() {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, els.canvas.width, els.canvas.height);
  const gradient = ctx.createLinearGradient(0, 0, 0, els.canvas.height);
  gradient.addColorStop(0, "#f4f7fb");
  gradient.addColorStop(1, "#dbe4ef");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, els.canvas.width, els.canvas.height);
  ctx.strokeStyle = "rgba(41, 55, 76, 0.08)";
  ctx.lineWidth = 1;
  for (let x = 0; x < els.canvas.width; x += 50) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, els.canvas.height);
    ctx.stroke();
  }
  for (let y = 0; y < els.canvas.height; y += 50) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(els.canvas.width, y);
    ctx.stroke();
  }
}

function sortedParts() {
  const view = rig.views[state.pose.viewId];
  return Object.keys(view.parts).sort((left, right) => {
    const leftDepth = state.pose.depthOverrides[left] ?? view.defaultDepth[left];
    const rightDepth = state.pose.depthOverrides[right] ?? view.defaultDepth[right];
    return leftDepth - rightDepth;
  });
}

function handleForPart(partId, body, rigToScreen) {
  const part = rig.views[state.pose.viewId].parts[partId];
  const parent = parentMatrixForPart(rig, state, body, partId);
  const point = transformPoint(multiply(rigToScreen, parent), {
    x: part.pivot[0],
    y: part.pivot[1],
  });
  return {
    id: part.pivotId,
    partId,
    kind: "joint",
    category: partCategory(partId),
    x: point.x,
    y: point.y,
  };
}

function renderHandles(body, rigToScreen) {
  const handles = [];
  for (const partId of Object.keys(rig.views[state.pose.viewId].parts)) {
    handles.push(handleForPart(partId, body, rigToScreen));
  }
  const rootPivot = rig.views[state.pose.viewId].pivots.root;
  const rootPoint = transformPoint(rigToScreen, { x: rootPivot[0], y: rootPivot[1] });
  handles.push({ id: "root", partId: null, kind: "root", x: rootPoint.x, y: rootPoint.y });

  const neckPivot = rig.views[state.pose.viewId].pivots.neck_socket;
  const neckPoint = transformPoint(multiply(rigToScreen, body.chest), {
    x: neckPivot[0],
    y: neckPivot[1],
  });
  handles.push({
    id: "neck_socket",
    partId: null,
    kind: "attachment",
    x: neckPoint.x,
    y: neckPoint.y,
  });

  ctx.setTransform(1, 0, 0, 1, 0, 0);
  const colors = { torso: "#f3b72f", arm: "#149bd7", leg: "#24a55a" };
  for (const handle of handles.filter((candidate) => candidate.kind === "joint")) {
    const selected = state.editor.selectedJoint === handle.partId;
    const hovered = state.editor.hoveredJoint === handle.partId;
    ctx.beginPath();
    ctx.arc(handle.x, handle.y, selected ? 10 : hovered ? 9 : 7, 0, Math.PI * 2);
    ctx.fillStyle = colors[handle.category];
    ctx.fill();
    ctx.strokeStyle = selected ? "#ffffff" : "#17202b";
    ctx.lineWidth = selected ? 4 : 2;
    ctx.stroke();
  }
  drawDiamond(rootPoint.x, rootPoint.y, 11, "#d34bf0", "#17202b", 3);
  drawDiamond(neckPoint.x, neckPoint.y, 8, "#ffffff", "#3b4a61", 2);
  ctx.strokeStyle = "#3b4a61";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(neckPoint.x - 12, neckPoint.y);
  ctx.lineTo(neckPoint.x + 12, neckPoint.y);
  ctx.moveTo(neckPoint.x, neckPoint.y - 12);
  ctx.lineTo(neckPoint.x, neckPoint.y + 12);
  ctx.stroke();
  diagnostics.handles = handles;
}

function render() {
  if (!rig || !artwork || !state) return;
  renderBackground();
  const body = computeBodyMatrices(rig, state);
  const rigToScreen = screenMatrix(rig, state);
  const viewId = state.pose.viewId;
  diagnostics.renderedAngles = {};
  for (const partId of sortedParts()) {
    const transform = multiply(rigToScreen, body[partId]);
    setContextTransform(transform);
    ctx.drawImage(artwork[viewId][partId], 0, 0);
    diagnostics.renderedAngles[partId] = semanticToVisual(
      rig.joints[partId],
      viewId,
      state.pose.joints[partId],
    );
  }
  const worldBounds = characterWorldBounds(rig, state, body);
  diagnostics.screenBounds = boundsToScreen(state, worldBounds);
  diagnostics.worldBounds = worldBounds;
  diagnostics.characterMatrix = characterMatrix(rig, state);
  diagnostics.cameraMatrix = cameraMatrix(state);
  diagnostics.bodyMatrices = body;
  if (state.editor.showHandles) renderHandles(body, rigToScreen);
  else diagnostics.handles = [];
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  els.zoomReadout.textContent = `${Math.round(state.camera.zoom * 100)}%`;
  updateToolUi();
  updateSelectionUi();
}

function displayValue(partId, semanticValue) {
  return rig.joints[partId].semantic.unit === "flexion"
    ? Math.round(semanticValue * 100)
    : Math.round(semanticValue);
}

function semanticValue(partId, displayedValue) {
  return rig.joints[partId].semantic.unit === "flexion"
    ? displayedValue / 100
    : displayedValue;
}

function controlRange(partId) {
  const semantic = rig.joints[partId].semantic;
  if (semantic.unit === "flexion") return { min: 0, max: 100, step: 1, unit: "%" };
  return { min: semantic.minimum, max: semantic.maximum, step: 1, unit: "°" };
}

function buildJointControls() {
  els.jointControls.replaceChildren();
  for (const [groupName, partIds] of Object.entries(GROUPS)) {
    const group = document.createElement("section");
    group.className = "joint-group";
    const heading = document.createElement("h3");
    heading.textContent = groupName;
    group.append(heading);
    for (const partId of partIds) {
      const range = controlRange(partId);
      const row = document.createElement("div");
      row.className = "joint-row";
      row.dataset.part = partId;
      const label = document.createElement("label");
      label.htmlFor = `joint-${partId}`;
      label.textContent = PART_LABELS[partId];
      const slider = document.createElement("input");
      slider.id = `joint-${partId}`;
      slider.className = "joint-slider";
      slider.type = "range";
      slider.min = range.min;
      slider.max = range.max;
      slider.step = range.step;
      slider.dataset.part = partId;
      const numeric = document.createElement("input");
      numeric.className = "joint-number";
      numeric.type = "number";
      numeric.min = range.min;
      numeric.max = range.max;
      numeric.step = range.step;
      numeric.dataset.part = partId;
      numeric.setAttribute("aria-label", `${PART_LABELS[partId]} numeric value`);
      const unit = document.createElement("span");
      unit.className = "joint-unit";
      unit.textContent = range.unit;
      const applyInput = (event) => {
        const displayed = clamp(Number(event.currentTarget.value), range.min, range.max);
        state.pose.joints[partId] = semanticValue(partId, displayed);
        selectJoint(partId);
        syncJointControl(partId);
        render();
      };
      slider.addEventListener("input", applyInput);
      numeric.addEventListener("input", applyInput);
      slider.addEventListener("focus", () => selectJoint(partId));
      numeric.addEventListener("focus", () => selectJoint(partId));
      row.append(label, slider, numeric, unit);
      group.append(row);
    }
    els.jointControls.append(group);
  }
  syncAllJointControls();
}

function syncJointControl(partId) {
  const value = displayValue(partId, state.pose.joints[partId]);
  for (const input of document.querySelectorAll(`[data-part="${partId}"]`)) {
    if (input instanceof HTMLInputElement) input.value = value;
  }
}

function syncAllJointControls() {
  for (const partId of Object.keys(rig.joints)) syncJointControl(partId);
}

function selectJoint(partId) {
  state.editor.selectedJoint = partId;
  updateSelectionUi();
}

function updateSelectionUi() {
  for (const row of document.querySelectorAll(".joint-row")) {
    row.classList.toggle("selected", row.dataset.part === state.editor.selectedJoint);
  }
  const selectedName = state.editor.selectedJoint
    ? PART_LABELS[state.editor.selectedJoint]
    : "none";
  document.querySelector("#selection-readout").textContent = selectedName;
}

function updateToolUi() {
  for (const button of document.querySelectorAll("[data-tool]")) {
    const active = button.dataset.tool === state.editor.tool;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  }
  els.canvas.dataset.tool = state.editor.tool;
}

function syncCharacterControls() {
  els.characterX.value = Math.round(state.character.x);
  els.characterY.value = Math.round(state.character.y);
  els.characterScale.value = state.character.scale;
  els.characterRotation.value = Math.round(state.character.rotation);
  els.characterFlip.checked = state.character.flip;
}

function canvasPoint(event) {
  const bounds = els.canvas.getBoundingClientRect();
  return {
    x: ((event.clientX - bounds.left) * els.canvas.width) / bounds.width,
    y: ((event.clientY - bounds.top) * els.canvas.height) / bounds.height,
  };
}

function findHandle(point) {
  let best = null;
  let bestDistance = 17;
  for (const handle of diagnostics.handles) {
    const distance = Math.hypot(point.x - handle.x, point.y - handle.y);
    if (distance < bestDistance) {
      best = handle;
      bestDistance = distance;
    }
  }
  return best;
}

function startPan(point) {
  state.editor.drag = {
    type: "pan",
    startPoint: point,
    startPanX: state.camera.panX,
    startPanY: state.camera.panY,
  };
}

function startCharacterMove(point) {
  state.editor.drag = {
    type: "character",
    startPoint: point,
    startX: state.character.x,
    startY: state.character.y,
  };
}

function startJointDrag(partId, point) {
  selectJoint(partId);
  const body = computeBodyMatrices(rig, state);
  const local = pointerInParentRigSpace(rig, state, body, partId, point);
  const pivot = rig.views[state.pose.viewId].parts[partId].pivot;
  state.editor.drag = {
    type: "joint",
    partId,
    startPointerAngle: (Math.atan2(local.y - pivot[1], local.x - pivot[0]) * 180) / Math.PI,
    startVisualAngle: semanticToVisual(
      rig.joints[partId],
      state.pose.viewId,
      state.pose.joints[partId],
    ),
  };
}

function onPointerDown(event) {
  const point = canvasPoint(event);
  const handle = findHandle(point);
  const temporaryPan = event.button === 1 || spaceHeld;
  if (temporaryPan || state.editor.tool === "pan") startPan(point);
  else if (handle?.kind === "root" || state.editor.tool === "move") startCharacterMove(point);
  else if (state.editor.tool === "pose" && handle?.kind === "joint") {
    startJointDrag(handle.partId, point);
  } else {
    state.editor.selectedJoint = null;
    updateSelectionUi();
    render();
    return;
  }
  try {
    els.canvas.setPointerCapture(event.pointerId);
  } catch {
    // Synthetic browser tests do not create a native active pointer.
  }
  event.preventDefault();
}

function onPointerMove(event) {
  const point = canvasPoint(event);
  const drag = state.editor.drag;
  if (!drag) {
    const handle = findHandle(point);
    const hovered = handle?.kind === "joint" ? handle.partId : null;
    if (hovered !== state.editor.hoveredJoint) {
      state.editor.hoveredJoint = hovered;
      render();
    }
    return;
  }
  if (drag.type === "pan") {
    state.camera.panX = drag.startPanX + point.x - drag.startPoint.x;
    state.camera.panY = drag.startPanY + point.y - drag.startPoint.y;
  } else if (drag.type === "character") {
    state.character.x = drag.startX + (point.x - drag.startPoint.x) / state.camera.zoom;
    state.character.y = drag.startY + (point.y - drag.startPoint.y) / state.camera.zoom;
    syncCharacterControls();
  } else if (drag.type === "joint") {
    const body = computeBodyMatrices(rig, state);
    const local = pointerInParentRigSpace(rig, state, body, drag.partId, point);
    const pivot = rig.views[state.pose.viewId].parts[drag.partId].pivot;
    const pointerAngle = (Math.atan2(local.y - pivot[1], local.x - pivot[0]) * 180) / Math.PI;
    const nextVisual = drag.startVisualAngle
      + normalizeAngleDelta(pointerAngle - drag.startPointerAngle);
    state.pose.joints[drag.partId] = visualToSemantic(
      rig.joints[drag.partId],
      state.pose.viewId,
      nextVisual,
    );
    syncJointControl(drag.partId);
  }
  render();
  event.preventDefault();
}

function onPointerUp(event) {
  if (!state.editor.drag) return;
  state.editor.drag = null;
  try {
    els.canvas.releasePointerCapture(event.pointerId);
  } catch {
    // See pointer-down note for synthetic tests.
  }
  event.preventDefault();
}

function onWheel(event) {
  const point = canvasPoint(event);
  const factor = Math.exp(-event.deltaY * 0.0015);
  setZoomAroundScreenPoint(state, state.camera.zoom * factor, point);
  render();
  event.preventDefault();
}

function fitBody() {
  const body = computeBodyMatrices(rig, state);
  fitCameraToBounds(state, characterWorldBounds(rig, state, body), 54);
  render();
  setStatus("Camera fitted to the complete posed body.");
}

function zoom100() {
  setZoomAroundScreenPoint(
    state,
    1,
    { x: state.viewport.width / 2, y: state.viewport.height / 2 },
  );
  render();
  setStatus("Camera zoom set to 100%.");
}

function resetView() {
  fitBody();
  setStatus("View reset: camera refitted; pose and character were preserved.");
}

function resetPoseOnly() {
  resetPose(state, rig);
  syncAllJointControls();
  render();
  setStatus("Pose reset; character and camera were preserved.");
}

function resetCharacterOnly() {
  resetCharacter(state);
  syncCharacterControls();
  render();
  setStatus("Character transform reset; pose and camera were preserved.");
}

function resetAll() {
  resetPose(state, rig);
  resetCharacter(state);
  state.editor.selectedJoint = null;
  syncAllJointControls();
  syncCharacterControls();
  fitBody();
  setStatus("Pose, character, and camera reset.");
}

function downloadPose() {
  const payload = JSON.stringify(serializePose(state), null, 2);
  const url = URL.createObjectURL(new Blob([payload], { type: "application/json" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = `2d-doll-pose-${Date.now()}.json`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  setStatus("Semantic pose saved without camera or editor state.");
}

function bindUi() {
  for (const [viewId, view] of Object.entries(rig.views)) {
    const option = document.createElement("option");
    option.value = viewId;
    option.textContent = view.label;
    els.view.append(option);
  }
  els.view.value = state.pose.viewId;
  els.view.addEventListener("change", () => {
    state.pose.viewId = els.view.value;
    render();
    setStatus(`Mapped the same semantic pose to ${rig.views[state.pose.viewId].label}.`);
  });
  els.handles.addEventListener("change", () => {
    state.editor.showHandles = els.handles.checked;
    render();
  });
  for (const button of document.querySelectorAll("[data-tool]")) {
    button.addEventListener("click", () => {
      state.editor.tool = button.dataset.tool;
      render();
    });
  }
  document.querySelector("#fit-body").addEventListener("click", fitBody);
  document.querySelector("#zoom-100").addEventListener("click", zoom100);
  document.querySelector("#reset-view").addEventListener("click", resetView);
  document.querySelector("#reset-pose").addEventListener("click", resetPoseOnly);
  document.querySelector("#reset-character").addEventListener("click", resetCharacterOnly);
  document.querySelector("#reset-all").addEventListener("click", resetAll);
  document.querySelector("#save-pose").addEventListener("click", downloadPose);

  const bindCharacterNumber = (element, field, minimum, maximum) => {
    element.addEventListener("input", () => {
      state.character[field] = clamp(Number(element.value), minimum, maximum);
      render();
    });
  };
  bindCharacterNumber(els.characterX, "x", -3000, 3000);
  bindCharacterNumber(els.characterY, "y", -3000, 3000);
  bindCharacterNumber(els.characterScale, "scale", 0.25, 3);
  bindCharacterNumber(els.characterRotation, "rotation", -180, 180);
  els.characterFlip.addEventListener("change", () => {
    state.character.flip = els.characterFlip.checked;
    render();
  });

  els.canvas.addEventListener("pointerdown", onPointerDown);
  els.canvas.addEventListener("pointermove", onPointerMove);
  els.canvas.addEventListener("pointerup", onPointerUp);
  els.canvas.addEventListener("pointercancel", onPointerUp);
  els.canvas.addEventListener("wheel", onWheel, { passive: false });
  window.addEventListener("keydown", (event) => {
    if (event.code === "Space" && !event.repeat) {
      spaceHeld = true;
      els.canvas.classList.add("temporary-pan");
      if (event.target === document.body) event.preventDefault();
    }
  });
  window.addEventListener("keyup", (event) => {
    if (event.code === "Space") {
      spaceHeld = false;
      els.canvas.classList.remove("temporary-pan");
    }
  });
}

function publicApi() {
  return {
    ready: true,
    getState: () => deepClone(state),
    getDiagnostics: () => deepClone(diagnostics),
    getRigSummary: () => ({
      schemaVersion: rig.schemaVersion,
      sourceArtwork: rig.sourceArtwork,
      partCount: Object.keys(rig.views.front.parts).length,
      pivotCount: rig.stablePivotIds.length,
      viewCompatibility: deepClone(rig.viewCompatibility),
      depth: deepClone(rig.depth),
    }),
    setView: (viewId) => {
      if (!rig.views[viewId]) throw new Error(`Unknown view: ${viewId}`);
      state.pose.viewId = viewId;
      els.view.value = viewId;
      render();
    },
    setJoint: (partId, value) => {
      const definition = rig.joints[partId];
      if (!definition) throw new Error(`Unknown joint part: ${partId}`);
      state.pose.joints[partId] = clamp(
        value,
        definition.semantic.minimum,
        definition.semantic.maximum,
      );
      syncJointControl(partId);
      render();
    },
    setCharacter: (partial) => {
      Object.assign(state.character, partial);
      state.character.scale = clamp(state.character.scale, 0.25, 3);
      syncCharacterControls();
      render();
    },
    setCamera: (partial) => {
      Object.assign(state.camera, partial);
      state.camera.zoom = clamp(state.camera.zoom, 0.08, 4);
      render();
    },
    setTool: (tool) => {
      if (!new Set(["pose", "move", "pan"]).has(tool)) throw new Error(`Unknown tool: ${tool}`);
      state.editor.tool = tool;
      render();
    },
    fitBody,
    zoom100,
    resetPose: resetPoseOnly,
    resetCharacter: resetCharacterOnly,
    resetView,
    resetAll,
    serializePose: () => deepClone(serializePose(state)),
    render,
    elements: {
      canvas: els.canvas,
      jointSlider: (partId) => document.querySelector(`.joint-slider[data-part="${partId}"]`),
      jointNumber: (partId) => document.querySelector(`.joint-number[data-part="${partId}"]`),
    },
  };
}

async function init() {
  setLifecycle("load-rig", "Loading rig definition…");
  rig = await loadRigDefinition();
  setLifecycle("load-artwork", "Loading provisional body artwork…");
  artwork = await loadRigArtwork(rig);
  setLifecycle("create-state", "Creating separated pose, character, camera, and editor state…");
  state = createInitialState(rig, { width: els.canvas.width, height: els.canvas.height });
  setLifecycle("bind-editor", "Binding editor controls…");
  buildJointControls();
  bindUi();
  syncCharacterControls();
  setLifecycle("fit-camera", "Fitting complete body…");
  fitCameraToBounds(state, characterWorldBounds(rig, state), 54);
  setLifecycle("render", "Rendering…");
  render();
  diagnostics.lifecycle = "ready";
  setStatus("Ready — complete body fitted. Pose, Move Doll, or Pan.");
  window.dollApp = publicApi();
  window.dispatchEvent(new CustomEvent("doll-ready"));
}

init().catch((error) => {
  diagnostics.lifecycle = "failed";
  diagnostics.initializationError = String(error?.stack || error);
  setStatus("Initialization failed. See the recorded runtime error.");
  window.__DOLL_RUNTIME_ERRORS__?.push(String(error?.stack || error));
  console.error(error);
});
