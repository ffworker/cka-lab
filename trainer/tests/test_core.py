import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from trainer.core import (
    SELECTION_MODES,
    default_profile,
    discover_scenarios,
    load_catalogue,
    load_or_create_profile,
    load_study_state,
    rank_for_xp,
    validate_scenario,
)

REPO = Path(__file__).resolve().parents[2]


def test_study_state_reader_preserves_training_inputs():
    state = load_study_state(REPO / "docs/cka-shared/handoff.json")
    assert state["weakTopics"]
    assert state["improvingTopics"]
    assert state["stableTopics"]
    assert "practicalFeedback" in state
    assert SELECTION_MODES == {
        "weak", "improving", "stable", "mixed", "troubleshooting",
        "timed", "random", "mock-exam",
    }


def test_scenario_contract_discovery(tmp_path):
    scenario = {
        "id": "contract-check",
        "title": "The Silent Control Room",
        "codename": "silent-control-room",
        "category": "placeholder",
        "topic": "placeholder",
        "difficulty": "easy",
        "prerequisites": [],
        "learningStateTags": ["weak"],
        "revisionEligible": True,
        "missionBriefing": "A symptom appears. Find the cause without assumptions.",
        "injector": "inject.sh",
        "validator": "validate.sh",
        "reset": "reset.sh",
        "hints": ["Inspect the evidence.", "Compare desired and observed state."],
        "solution": "solution.md",
        "xp": 100,
        "targetTimeMinutes": 15,
    }
    mission = tmp_path / "contract-check"
    mission.mkdir()
    (mission / "scenario.json").write_text(json.dumps(scenario))
    (mission / "inject.sh").write_text("#!/bin/sh\n")
    (mission / "validate.sh").write_text("#!/bin/sh\n")
    (mission / "reset.sh").write_text("#!/bin/sh\n")
    (mission / "solution.md").write_text("placeholder\n")

    found = discover_scenarios(tmp_path)
    assert [item["id"] for item in found] == ["contract-check"]
    assert validate_scenario(found[0], mission) == []


def test_scenario_runtime_validation_matches_contract(tmp_path):
    scenario = {
        "id": "bad id",
        "title": "",
        "codename": "bad",
        "category": "placeholder",
        "topic": "placeholder",
        "difficulty": "easy",
        "prerequisites": [1],
        "learningStateTags": ["weak"],
        "revisionEligible": True,
        "missionBriefing": "briefing",
        "injector": "../outside.sh",
        "validator": "validate.sh",
        "reset": "reset.sh",
        "hints": ["one", "two"],
        "solution": "solution.md",
        "xp": True,
        "targetTimeMinutes": False,
        "unexpected": "field",
    }
    for name in ("validate.sh", "reset.sh", "solution.md"):
        (tmp_path / name).write_text("placeholder\n")
    (tmp_path.parent / "outside.sh").write_text("#!/bin/sh\n")

    errors = validate_scenario(scenario, tmp_path)
    assert "id must use lowercase letters, numbers, and hyphens" in errors
    assert "title must not be empty" in errors
    assert "prerequisites entries must be strings" in errors
    assert "xp must be int" in errors
    assert "targetTimeMinutes must be a positive integer" in errors
    assert "unexpected field: unexpected" in errors
    assert "injector must stay inside the scenario directory" in errors


def test_malformed_scenario_returns_errors_instead_of_crashing(tmp_path):
    assert validate_scenario([], tmp_path) == ["scenario must be a JSON object"]
    errors = validate_scenario({"difficulty": []}, tmp_path)
    assert "difficulty must be str" in errors


def test_scenario_discovery_rejects_symlinked_directory(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "scenario.json").write_text("{}")
    catalog = tmp_path / "catalog"
    catalog.mkdir()
    (catalog / "linked").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="symlinked scenario directory"):
        discover_scenarios(catalog)


def test_catalogues_and_profile_are_local_json():
    ranks = load_catalogue(REPO / "trainer/config/ranks.json", "ranks")
    achievements = load_catalogue(
        REPO / "trainer/config/achievements.json", "achievements"
    )
    assert rank_for_xp(0, ranks) == "YAML Goblin"
    assert rank_for_xp(5000, ranks) == "Control Plane Commander"
    assert len(achievements) >= 5
    profile = default_profile()
    assert profile["xp"] == 0
    assert profile["attempts"] == 0
    assert profile["hintCount"] == 0
    assert profile["totalCompletionSeconds"] == 0
    assert profile["missionHistory"] == []


def test_existing_profile_is_validated(tmp_path):
    (tmp_path / "profile.json").write_text('{"xp": "many"}')
    with pytest.raises(ValueError, match="invalid profile"):
        load_or_create_profile(tmp_path)


def test_make_mode_cannot_inject_shell_commands(tmp_path):
    for index, payload in enumerate(("mixed;touch", "mixed\ntouch")):
        marker = tmp_path / f"injected-{index}"
        result = subprocess.run(
            ["make", "mission", f"MODE={payload} {marker}"],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert not marker.exists()


@pytest.mark.parametrize(
    "command",
    ["status", "mission", "validate", "hint", "solution", "reset", "profile", "lab-up", "lab-down"],
)
def test_trainer_commands_respond_without_live_changes(command, tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "trainer", "--runtime-dir", str(tmp_path), command],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "CKA_FACTORY_DRY_RUN": "1"},
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip()
