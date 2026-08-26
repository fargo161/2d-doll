const frame = document.querySelector("#runtime");
const results = document.querySelector("#results");
const summary = document.querySelector("#summary");
const completed = [];

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function same(actual, expected, message) {
  const left = JSON.stringify(actual);
  const right = JSON.stringify(expected);
  assert(left === right, `${message}\nactual: ${left}\nexpected: ${right}`);
}

function distance(left, right) {
  return Math.hypot(left.x - right.x, left.y - right.y);
}

function handle(diagnostics, partId) {
  const found = diagnostics.handles.find((candidate) => candidate.partId === partId);
  if (!found) throw new Error(`Handle not found for ${partId}`);
  return found;
}

async function waitForRuntime() {
  frame.src = "../app/index.html?runtime-test=1";
  const started = performance.now();
  while (performance.now() - started < 30000) {
    if (frame.contentWindow?.dollApp?.ready) return frame.contentWindow.dollApp;
    await new Promise((resolve) => setTimeout(resolve, 50));
  }
  throw new Error("Runtime did not become ready within 30 seconds.");
}

async function run(name, callback) {
  const item = document.createElement("li");
  const label = document.createElement("strong");
  label.textContent = name;
  item.append(label);
  results.append(item);
  try {
    await callback();
    item.className = "pass";
    item.append("PASS");
    completed.push({ name, passed: true });
  } catch (error) {
    item.className = "fail";
    item.append("FAIL");
    const details = document.createElement("pre");
    details.textContent = String(error?.stack || error);
    item.append(details);
    completed.push({ name, passed: false, error: String(error?.stack || error) });
  }
}

function clientPoint(canvas, internalPoint) {
  const rect = canvas.getBoundingClientRect();
  return {
    x: rect.left + (internalPoint.x * rect.width) / canvas.width,
    y: rect.top + (internalPoint.y * rect.height) / canvas.height,
  };
}

function pointer(canvas, type, internalPoint, options = {}) {
  const point = clientPoint(canvas, internalPoint);
  canvas.dispatchEvent(
    new PointerEvent(type, {
      bubbles: true,
      cancelable: true,
      pointerId: options.pointerId ?? 41,
      pointerType: "mouse",
      button: options.button ?? 0,
      buttons: type === "pointerup" ? 0 : 1,
      clientX: point.x,
      clientY: point.y,
    }),
  );
}

function pointerDrag(canvas, start, end, options = {}) {
  pointer(canvas, "pointerdown", start, options);
  pointer(canvas, "pointermove", end, options);
  pointer(canvas, "pointerup", end, options);
}

function wheel(canvas, internalPoint, deltaY) {
  const point = clientPoint(canvas, internalPoint);
  canvas.dispatchEvent(
    new WheelEvent("wheel", {
      bubbles: true,
      cancelable: true,
      clientX: point.x,
      clientY: point.y,
      deltaY,
    }),
  );
}

function dragJoint(app, partId, deltaDegrees) {
  app.resetPose();
  app.setView("front");
  app.fitBody();
  app.setTool("pose");
  const joint = handle(app.getDiagnostics(), partId);
  const radius = 72;
  const radians = (deltaDegrees * Math.PI) / 180;
  const start = { x: joint.x + 8, y: joint.y };
  const end = {
    x: joint.x + Math.cos(radians) * radius,
    y: joint.y + Math.sin(radians) * radius,
  };
  pointerDrag(app.elements.canvas, start, end);
  return app.getState();
}

const app = await waitForRuntime();

await run("Startup is clean and lifecycle reaches ready", () => {
  same(frame.contentWindow.__DOLL_RUNTIME_ERRORS__, [], "runtime error list must be empty");
  assert(app.getDiagnostics().lifecycle === "ready", "lifecycle did not reach ready");
  const summary = app.getRigSummary();
  assert(summary.partCount === 15, "expected 15 articulated parts");
  assert(summary.pivotCount === 17, "expected 17 semantic pivots");
});

await run("Fit Body contains the complete body in Front, 3/4, and Back", () => {
  app.resetAll();
  app.setCharacter({ x: 145, y: -82, scale: 1.35, rotation: 9 });
  app.setCamera({ panX: 260, panY: -190, zoom: 2.1 });
  for (const viewId of ["front", "three_quarter", "back"]) {
    app.setView(viewId);
    app.fitBody();
    const bounds = app.getDiagnostics().screenBounds;
    assert(bounds.minX >= 53, `${viewId}: left bound ${bounds.minX}`);
    assert(bounds.minY >= 53, `${viewId}: top bound ${bounds.minY}`);
    assert(bounds.maxX <= 1047, `${viewId}: right bound ${bounds.maxX}`);
    assert(bounds.maxY <= 707, `${viewId}: bottom bound ${bounds.maxY}`);
  }
  app.resetAll();
});

await run("Root, 15 joints, and neck attachment have distinct handles", () => {
  app.setView("front");
  app.fitBody();
  const handles = app.getDiagnostics().handles;
  assert(handles.filter((candidate) => candidate.kind === "joint").length === 15, "joint handle count");
  assert(handles.filter((candidate) => candidate.kind === "root").length === 1, "root handle count");
  assert(handles.filter((candidate) => candidate.kind === "attachment").length === 1, "attachment handle count");
});

await run("Character drag, camera pan, and wheel zoom mutate separate state", () => {
  app.resetAll();
  const canvas = app.elements.canvas;
  const initial = app.getState();
  app.setTool("move");
  pointerDrag(canvas, { x: 520, y: 380 }, { x: 610, y: 430 });
  const moved = app.getState();
  assert(Math.abs(moved.character.x - initial.character.x) > 10, "character X did not move");
  assert(Math.abs(moved.character.y - initial.character.y) > 10, "character Y did not move");
  same(moved.camera, initial.camera, "character drag must not mutate camera");
  same(moved.pose, initial.pose, "character drag must not mutate pose");

  app.setTool("pan");
  pointerDrag(canvas, { x: 500, y: 360 }, { x: 555, y: 320 });
  const panned = app.getState();
  same(panned.character, moved.character, "camera pan must not mutate character");
  assert(panned.camera.panX !== moved.camera.panX, "camera pan X did not change");
  assert(panned.camera.panY !== moved.camera.panY, "camera pan Y did not change");

  const poseBeforeZoom = panned.pose;
  wheel(canvas, { x: 620, y: 330 }, -160);
  const zoomed = app.getState();
  assert(zoomed.camera.zoom > panned.camera.zoom, "wheel did not zoom in");
  same(zoomed.pose, poseBeforeZoom, "zoom must not mutate pose");
});

await run("One semantic elbow pose maps Front → 3/4 → Back → Front", () => {
  app.resetAll();
  app.setJoint("forearm_L", 0.65);
  app.setCharacter({ x: 38, y: -24, scale: 1.15, rotation: 8 });
  app.setCamera({ panX: 33, panY: -17, zoom: 0.72 });
  const initial = app.getState();
  const expectedAngles = {
    front: 72.8,
    three_quarter: 72.8,
    back: -72.8,
  };
  for (const viewId of ["front", "three_quarter", "back", "front"]) {
    app.setView(viewId);
    const state = app.getState();
    const rendered = app.getDiagnostics().renderedAngles.forearm_L;
    assert(Math.abs(state.pose.joints.forearm_L - 0.65) < 1e-9, `${viewId}: semantic flexion drifted`);
    assert(Math.abs(rendered - expectedAngles[viewId]) < 1e-9, `${viewId}: rendered mapping ${rendered}`);
    same(state.character, initial.character, `${viewId}: character state changed`);
    same(state.camera, initial.camera, `${viewId}: camera state changed`);
  }
});

await run("Direct manipulation works for representative arm and leg joints", () => {
  const cases = [
    ["upper_arm_L", 42],
    ["forearm_L", 72],
    ["forearm_R", -72],
    ["hand_L", 24],
    ["thigh_L", 26],
    ["calf_L", 52],
    ["foot_L", 20],
  ];
  for (const [partId, delta] of cases) {
    const state = dragJoint(app, partId, delta);
    assert(Math.abs(state.pose.joints[partId]) > 0.05, `${partId}: semantic value did not change`);
    assert(state.editor.selectedJoint === partId, `${partId}: selection did not synchronize`);
    same(frame.contentWindow.__DOLL_RUNTIME_ERRORS__, [], `${partId}: runtime error occurred`);
  }
});

await run("Elbow direct manipulation synchronizes slider and numeric control", () => {
  const state = dragJoint(app, "forearm_L", 68);
  const expected = String(Math.round(state.pose.joints.forearm_L * 100));
  assert(app.elements.jointSlider("forearm_L").value === expected, "elbow slider is stale");
  assert(app.elements.jointNumber("forearm_L").value === expected, "elbow numeric input is stale");
});

await run("Hierarchy propagation and branch isolation hold for arms and legs", () => {
  app.resetAll();
  app.setView("front");
  app.fitBody();
  const armNeutral = app.getDiagnostics();
  app.setJoint("upper_arm_L", 40);
  const armParent = app.getDiagnostics();
  assert(distance(handle(armNeutral, "forearm_L"), handle(armParent, "forearm_L")) > 8, "arm child did not follow parent");
  assert(distance(handle(armNeutral, "hand_L"), handle(armParent, "hand_L")) > 8, "arm descendant did not follow parent");
  assert(distance(handle(armNeutral, "upper_arm_L"), handle(armParent, "upper_arm_L")) < 0.01, "shoulder pivot moved");
  assert(distance(handle(armNeutral, "forearm_R"), handle(armParent, "forearm_R")) < 0.01, "unrelated arm moved");

  app.resetPose();
  const childNeutral = app.getDiagnostics();
  app.setJoint("forearm_L", 0.7);
  const armChild = app.getDiagnostics();
  assert(distance(handle(childNeutral, "hand_L"), handle(armChild, "hand_L")) > 8, "wrist did not follow elbow");
  assert(distance(handle(childNeutral, "forearm_L"), handle(armChild, "forearm_L")) < 0.01, "elbow pivot moved");
  assert(distance(handle(childNeutral, "upper_arm_L"), handle(armChild, "upper_arm_L")) < 0.01, "ancestor moved");
  assert(distance(handle(childNeutral, "hand_R"), handle(armChild, "hand_R")) < 0.01, "unrelated branch moved");

  app.resetPose();
  const legNeutral = app.getDiagnostics();
  app.setJoint("thigh_L", 28);
  const legParent = app.getDiagnostics();
  assert(distance(handle(legNeutral, "calf_L"), handle(legParent, "calf_L")) > 8, "knee did not follow hip");
  assert(distance(handle(legNeutral, "foot_L"), handle(legParent, "foot_L")) > 8, "ankle did not follow hip");
  assert(distance(handle(legNeutral, "thigh_L"), handle(legParent, "thigh_L")) < 0.01, "hip pivot moved");
  assert(distance(handle(legNeutral, "foot_R"), handle(legParent, "foot_R")) < 0.01, "unrelated leg moved");
});

await run("Reset Pose, Character, View, and All have exact scopes", () => {
  app.resetAll();
  app.setJoint("forearm_L", 0.8);
  app.setCharacter({ x: 70, y: 45, scale: 1.3, rotation: 12, flip: true });
  app.setCamera({ panX: 31, panY: -28, zoom: 0.8 });
  const beforePoseReset = app.getState();
  app.resetPose();
  const poseReset = app.getState();
  assert(poseReset.pose.joints.forearm_L === 0, "Reset Pose did not neutralize articulation");
  same(poseReset.character, beforePoseReset.character, "Reset Pose changed character");
  same(poseReset.camera, beforePoseReset.camera, "Reset Pose changed camera");

  app.setJoint("forearm_L", 0.55);
  const beforeCharacterReset = app.getState();
  app.resetCharacter();
  const characterReset = app.getState();
  same(characterReset.character, { x: 0, y: 0, rotation: 0, scale: 1, flip: false }, "Reset Character result");
  same(characterReset.pose, beforeCharacterReset.pose, "Reset Character changed pose");
  same(characterReset.camera, beforeCharacterReset.camera, "Reset Character changed camera");

  app.setCharacter({ x: 44, y: 9, scale: 1.1 });
  app.setCamera({ panX: 500, panY: 350, zoom: 2 });
  const beforeViewReset = app.getState();
  app.resetView();
  const viewReset = app.getState();
  same(viewReset.pose, beforeViewReset.pose, "Reset View changed pose");
  same(viewReset.character, beforeViewReset.character, "Reset View changed character");
  assert(JSON.stringify(viewReset.camera) !== JSON.stringify(beforeViewReset.camera), "Reset View did not reset camera");

  app.resetAll();
  const allReset = app.getState();
  assert(Object.values(allReset.pose.joints).every((value) => value === 0), "Reset All left articulation");
  same(allReset.character, { x: 0, y: 0, rotation: 0, scale: 1, flip: false }, "Reset All character result");
});

await run("Pose persistence excludes camera, character, and editor state", () => {
  app.setJoint("forearm_L", 0.44);
  app.setCharacter({ x: 88, y: -40 });
  app.setCamera({ panX: 77, zoom: 0.6 });
  const saved = app.serializePose();
  assert(saved.schemaVersion === "2d-doll-pose-0.1", "pose schema version missing");
  assert(saved.joints.forearm_L === 0.44, "semantic pose value missing");
  assert(!("camera" in saved), "camera leaked into pose data");
  assert(!("character" in saved), "character leaked into pose data");
  assert(!("editor" in saved), "editor leaked into pose data");
});

await run("Three-quarter remains the compatibility bridge and depth is extensible", () => {
  const summary = app.getRigSummary();
  same(summary.viewCompatibility.front, ["front", "three_quarter"], "Front compatibility");
  same(summary.viewCompatibility.back, ["three_quarter", "back"], "Back compatibility");
  assert(summary.depth.overrideState === "pose.depthOverrides", "depth override state is missing");
  assert(summary.depth.overrideUiStatus === "DESIGNED_NOT_IMPLEMENTED", "depth limitation must remain explicit");
});

const failures = completed.filter((result) => !result.passed);
const passes = completed.length - failures.length;
document.body.dataset.status = failures.length ? "fail" : "pass";
document.body.dataset.passed = String(passes);
document.body.dataset.failed = String(failures.length);
summary.textContent = `${passes}/${completed.length} browser tests passed; ${failures.length} failed.`;
document.title = failures.length
  ? `2D Doll Runtime Tests — ${failures.length} failed`
  : `2D Doll Runtime Tests — ${passes} passed`;
window.__RUNTIME_TEST_RESULTS__ = completed;
