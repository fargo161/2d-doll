from __future__ import annotations

from pathlib import Path


TOOL_VERSION = "pose-corpus-normalizer-0.1"
CORPUS_ID = "canonical_female_pose_corpus_v0_1"
CORPUS_SCHEMA_VERSION = "2d-doll-pose-corpus-0.1"
ENTRY_SCHEMA_VERSION = "2d-doll-pose-corpus-entry-0.1"
SOURCE_MANIFEST_SCHEMA_VERSION = "2d-doll-pose-corpus-source-manifest-0.1"
PROFILE_EVIDENCE_SCHEMA_VERSION = "2d-doll-pose-corpus-profile-evidence-0.1"
RENDER_MANIFEST_SCHEMA_VERSION = "2d-doll-pose-corpus-render-manifest-0.1"
OVERRIDE_SCHEMA_VERSION = "2d-doll-pose-corpus-override-0.1"
PROPOSAL_SCHEMA_VERSION = "2d-doll-pose-corpus-proposal-0.1"
QA_SUMMARY_SCHEMA_VERSION = "2d-doll-pose-corpus-qa-summary-0.1"

TARGET_PROFILE_ID = "base_female_v0_1"
PROFILE_EVIDENCE_ID = "base_female_v0_1.corpus_v0_1"
COORDINATE_SPACE_ID = "canonical_body_space_v0_1"

SOURCE_CONFIG_RELATIVE = Path(
    "pose-corpus/canonical-v0_1/spec/source-packages.json"
)
CORPUS_ROOT_RELATIVE = Path("pose-corpus/canonical-v0_1")
SOURCE_CONFIG_SCHEMA_RELATIVE = (
    CORPUS_ROOT_RELATIVE / "schemas/source-package-config.schema.json"
)

CANONICAL_ORIENTATION_IDS = ("front", "three_quarter", "back")
PROJECTION_CLASSES = (
    "front",
    "front_three_quarter",
    "profile",
    "rear_three_quarter",
    "rear",
    "unknown",
)

LANDMARK_IDS = (
    "head_top",
    "head_center",
    "chin",
    "neck_base",
    "neck_socket",
    "shoulder_L",
    "shoulder_R",
    "chest_center",
    "waist_center",
    "pelvis_center",
    "hip_L",
    "hip_R",
    "elbow_L",
    "elbow_R",
    "wrist_L",
    "wrist_R",
    "hand_center_L",
    "hand_center_R",
    "knee_L",
    "knee_R",
    "ankle_L",
    "ankle_R",
    "heel_L",
    "heel_R",
    "toe_L",
    "toe_R",
)

PROMPT_ALIASES = {
    "pelvis_root": "pelvis_center",
    "left_shoulder": "shoulder_L",
    "right_shoulder": "shoulder_R",
    "left_hip": "hip_L",
    "right_hip": "hip_R",
    "left_elbow": "elbow_L",
    "right_elbow": "elbow_R",
    "left_wrist": "wrist_L",
    "right_wrist": "wrist_R",
    "left_hand_anchor": "hand_center_L",
    "right_hand_anchor": "hand_center_R",
    "left_knee": "knee_L",
    "right_knee": "knee_R",
    "left_ankle": "ankle_L",
    "right_ankle": "ankle_R",
    "left_heel": "heel_L",
    "right_heel": "heel_R",
    "left_toe": "toe_L",
    "right_toe": "toe_R",
}

def repository_root_from(module_path: Path) -> Path:
    return module_path.resolve().parents[2]
