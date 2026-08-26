import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import {
  boundsToScreen,
  buildJointDefinitions,
  characterWorldBounds,
  computeBodyMatrices,
  createInitialState,
  fitCameraToBounds,
  invert,
  multiply,
  resetCamera,
  resetCharacter,
  resetPose,
  semanticToVisual,
  serializePose,
  transformPoint,
  translate,
  visualToSemantic,
  VIEW_COMPATIBILITY,
} from "../app/model.js";

const manifest = JSON.parse(
  await readFile(
    new URL("../baselines/canonical_base_body_rig_v0_1/manifest.json", import.meta.url),
    "utf8",
  ),
);

const rig = {
  canvas: manifest.canvas,
  views: Object.fromEntries(
    Object.entries(manifest.views).map(([viewId, view]) => [
      viewId,
      {
        ...view,
        parts: Object.fromEntries(
          Object.entries(view.parts).map(([partId, part]) => [
            partId,
            {
              ...part,
              pivot: [...part.pivot],
              crop: [...part.crop],
              rotationLimitsDeg: [...part.rotationLimitsDeg],
            },
          ]),
        ),
      },
    ]),
  ),
};
rig.joints = buildJointDefinitions(rig);

test("matrix inversion round-trips a point", () => {
  const transform = multiply(translate(80, -25), [1.5, 0.2, -0.1, 0.8, 0, 0]);
  const source = { x: 37, y: -9 };
  const roundTrip = transformPoint(invert(transform), transformPoint(transform, source));
  assert.ok(Math.abs(roundTrip.x - source.x) < 1e-9);
  assert.ok(Math.abs(roundTrip.y - source.y) < 1e-9);
});

test("semantic elbow flexion maps across views through reusable mappings", () => {
  const left = rig.joints.forearm_L;
  const right = rig.joints.forearm_R;
  assert.equal(semanticToVisual(left, "front", 0.75), 84);
  assert.equal(semanticToVisual(left, "three_quarter", 0.75), 84);
  assert.equal(semanticToVisual(left, "back", 0.75), -84);
  assert.equal(semanticToVisual(right, "front", 0.75), -84);
  assert.equal(semanticToVisual(right, "back", 0.75), 84);
  assert.equal(visualToSemantic(left, "back", -84), 0.75);
});

test("view compatibility keeps three-quarter as the bridge", () => {
  assert.deepEqual(VIEW_COMPATIBILITY.front, ["front", "three_quarter"]);
  assert.deepEqual(VIEW_COMPATIBILITY.back, ["three_quarter", "back"]);
  assert.equal(VIEW_COMPATIBILITY.front.includes("back"), false);
});

test("hierarchy propagates parent motion without mutating canonical pose", () => {
  const state = createInitialState(rig);
  const neutral = computeBodyMatrices(rig, state);
  state.pose.joints.upper_arm_L = 45;
  const posed = computeBodyMatrices(rig, state);
  assert.notDeepEqual(posed.forearm_L, neutral.forearm_L);
  assert.notDeepEqual(posed.hand_L, neutral.hand_L);
  assert.deepEqual(posed.upper_arm_R, neutral.upper_arm_R);
  assert.equal(state.pose.joints.forearm_L, 0);
});

test("fit body yields visible bounds in every anchor view", () => {
  const state = createInitialState(rig);
  for (const viewId of ["front", "three_quarter", "back"]) {
    state.pose.viewId = viewId;
    const bounds = characterWorldBounds(rig, state);
    fitCameraToBounds(state, bounds, 48);
    const screen = boundsToScreen(state, bounds);
    assert.ok(screen.minX >= 47.9, `${viewId} left bound`);
    assert.ok(screen.minY >= 47.9, `${viewId} top bound`);
    assert.ok(screen.maxX <= state.viewport.width - 47.9, `${viewId} right bound`);
    assert.ok(screen.maxY <= state.viewport.height - 47.9, `${viewId} bottom bound`);
  }
});

test("reset scopes and pose persistence remain independent", () => {
  const state = createInitialState(rig);
  state.pose.joints.forearm_L = 0.8;
  state.character.x = 90;
  state.character.scale = 1.4;
  state.camera.panX = 55;
  state.camera.zoom = 0.7;
  resetPose(state, rig);
  assert.equal(state.pose.joints.forearm_L, 0);
  assert.equal(state.character.x, 90);
  assert.equal(state.camera.panX, 55);
  state.pose.joints.forearm_L = 0.5;
  resetCharacter(state);
  assert.equal(state.character.x, 0);
  assert.equal(state.character.scale, 1);
  assert.equal(state.pose.joints.forearm_L, 0.5);
  assert.equal(state.camera.panX, 55);
  resetCamera(state);
  assert.deepEqual(state.camera, { panX: 0, panY: 0, zoom: 1 });
  assert.equal(state.pose.joints.forearm_L, 0.5);
  const saved = serializePose(state);
  assert.equal("camera" in saved, false);
  assert.equal("character" in saved, false);
  assert.equal("editor" in saved, false);
  assert.equal(saved.joints.forearm_L, 0.5);
});
