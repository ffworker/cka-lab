from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

SELECTION_MODES = {
    "weak",
    "improving",
    "stable",
    "mixed",
    "troubleshooting",
    "timed",
    "random",
    "mock-exam",
}

REQUIRED_SCENARIO_FIELDS = {
    "id": str,
    "title": str,
    "codename": str,
    "category": str,
    "topic": str,
    "difficulty": str,
    "prerequisites": list,
    "learningStateTags": list,
    "revisionEligible": bool,
    "missionBriefing": str,
    "injector": str,
    "validator": str,
    "reset": str,
    "hints": list,
    "solution": str,
    "xp": int,
}
OPTIONAL_SCENARIO_FIELDS = {"targetTimeMinutes"}


def _read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_study_state(path: Path) -> dict[str, Any]:
    payload = _read_json(path)
    theory = payload["theoryStatus"]
    focus = payload["practicalFocus"]
    return {
        "weakTopics": theory["weakTopics"],
        "improvingTopics": theory["improvingTopics"],
        "stableTopics": theory["stableTopics"],
        "unstableConcepts": theory["unstableConcepts"],
        "recommendedDrills": focus["recommendedDrills"],
        "readyForPractice": focus["readyForPractice"],
        "notYetIntroduced": focus["notYetIntroduced"],
        "practicalFeedback": payload["practicalFeedback"],
    }


def validate_scenario(scenario: Any, directory: Path) -> list[str]:
    if not isinstance(scenario, dict):
        return ["scenario must be a JSON object"]
    errors: list[str] = []
    if directory.is_symlink():
        errors.append("symlinked scenario directory is not allowed")
    allowed_fields = set(REQUIRED_SCENARIO_FIELDS) | OPTIONAL_SCENARIO_FIELDS
    for field in sorted(set(scenario) - allowed_fields):
        errors.append(f"unexpected field: {field}")
    for field, expected in REQUIRED_SCENARIO_FIELDS.items():
        if field not in scenario:
            errors.append(f"missing field: {field}")
        elif type(scenario[field]) is not expected:
            errors.append(f"{field} must be {expected.__name__}")
    identifier = scenario.get("id")
    if isinstance(identifier, str) and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", identifier):
        errors.append("id must use lowercase letters, numbers, and hyphens")
    string_fields = (
        "title", "codename", "category", "topic", "missionBriefing",
        "injector", "validator", "reset", "solution",
    )
    for field in string_fields:
        value = scenario.get(field)
        if isinstance(value, str) and not value:
            errors.append(f"{field} must not be empty")
    for field in ("prerequisites", "learningStateTags"):
        values = scenario.get(field)
        if isinstance(values, list) and any(not isinstance(value, str) for value in values):
            errors.append(f"{field} entries must be strings")
    hints = scenario.get("hints")
    if isinstance(hints, list) and len(hints) != 2:
        errors.append("hints must contain exactly two entries")
    if isinstance(hints, list) and any(not isinstance(hint, str) for hint in hints):
        errors.append("hints entries must be strings")
    difficulty = scenario.get("difficulty")
    if isinstance(difficulty, str) and difficulty not in {"easy", "medium", "hard", "exam"}:
        errors.append("difficulty must be easy, medium, hard, or exam")
    if type(scenario.get("xp")) is int and scenario["xp"] <= 0:
        errors.append("xp must be positive")
    target = scenario.get("targetTimeMinutes")
    if target is not None and (type(target) is not int or target <= 0):
        errors.append("targetTimeMinutes must be a positive integer")
    scenario_root = directory.resolve()
    for field in ("injector", "validator", "reset", "solution"):
        relative = scenario.get(field)
        if isinstance(relative, str) and relative:
            resolved = (directory / relative).resolve()
            if not resolved.is_relative_to(scenario_root):
                errors.append(f"{field} must stay inside the scenario directory")
            elif not resolved.is_file():
                errors.append(f"missing file for {field}: {relative}")
    return errors


def discover_scenarios(root: Path) -> list[dict[str, Any]]:
    scenarios: list[dict[str, Any]] = []
    if not root.exists():
        return scenarios
    for metadata in sorted(root.glob("*/scenario.json")):
        if metadata.parent.is_symlink():
            raise ValueError(f"{metadata.parent}: symlinked scenario directory is not allowed")
        scenario = _read_json(metadata)
        errors = validate_scenario(scenario, metadata.parent)
        if errors:
            raise ValueError(f"{metadata}: " + "; ".join(errors))
        scenarios.append(scenario)
    return scenarios


def load_catalogue(path: Path, key: str) -> list[dict[str, Any]]:
    payload = _read_json(path)
    catalogue = payload[key]
    if not isinstance(catalogue, list) or not catalogue:
        raise ValueError(f"{key} catalogue must be a non-empty list")
    return catalogue


def rank_for_xp(xp: int, ranks: list[dict[str, Any]]) -> str:
    eligible = [rank for rank in ranks if xp >= rank["minimumXp"]]
    return max(eligible, key=lambda rank: rank["minimumXp"])["name"]


def default_profile() -> dict[str, Any]:
    return {
        "xp": 0,
        "rank": "YAML Goblin",
        "currentStreak": 0,
        "bestStreak": 0,
        "attempts": 0,
        "hintCount": 0,
        "firstAttemptWins": 0,
        "totalCompletionSeconds": 0,
        "achievements": [],
        "missionHistory": [],
    }


def _validate_profile(profile: Any) -> list[str]:
    if not isinstance(profile, dict):
        return ["profile must be a JSON object"]
    expected = default_profile()
    errors: list[str] = []
    for field, default in expected.items():
        if field not in profile:
            errors.append(f"missing field: {field}")
        elif type(profile[field]) is not type(default):
            errors.append(f"{field} must be {type(default).__name__}")
    for field in sorted(set(profile) - set(expected)):
        errors.append(f"unexpected field: {field}")
    for field in (
        "xp", "currentStreak", "bestStreak", "attempts", "hintCount",
        "firstAttemptWins", "totalCompletionSeconds",
    ):
        value = profile.get(field)
        if type(value) is int and value < 0:
            errors.append(f"{field} must not be negative")
    if isinstance(profile.get("achievements"), list) and any(
        not isinstance(item, str) for item in profile["achievements"]
    ):
        errors.append("achievement entries must be strings")
    history_fields = {
        "scenarioId": str,
        "completedAt": str,
        "completionSeconds": int,
        "attempts": int,
        "hintCount": int,
        "firstAttemptWin": bool,
        "xpAwarded": int,
    }
    history = profile.get("missionHistory")
    if isinstance(history, list):
        for index, entry in enumerate(history):
            if not isinstance(entry, dict):
                errors.append(f"missionHistory[{index}] must be an object")
                continue
            for field, expected_type in history_fields.items():
                if field not in entry:
                    errors.append(f"missionHistory[{index}] missing field: {field}")
                elif type(entry[field]) is not expected_type:
                    errors.append(
                        f"missionHistory[{index}].{field} must be {expected_type.__name__}"
                    )
            for field in sorted(set(entry) - set(history_fields)):
                errors.append(f"missionHistory[{index}] unexpected field: {field}")
            for field in ("completionSeconds", "hintCount", "xpAwarded"):
                value = entry.get(field)
                if type(value) is int and value < 0:
                    errors.append(f"missionHistory[{index}].{field} must not be negative")
            attempts = entry.get("attempts")
            if type(attempts) is int and attempts < 1:
                errors.append(f"missionHistory[{index}].attempts must be positive")
            completed_at = entry.get("completedAt")
            if isinstance(completed_at, str):
                try:
                    parsed = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
                    if parsed.tzinfo is None:
                        raise ValueError
                except ValueError:
                    errors.append(f"missionHistory[{index}].completedAt must be an RFC 3339 timestamp")
    return errors


def load_or_create_profile(runtime_dir: Path) -> dict[str, Any]:
    runtime_dir.mkdir(parents=True, exist_ok=True)
    path = runtime_dir / "profile.json"
    if path.exists():
        profile = _read_json(path)
        errors = _validate_profile(profile)
        if errors:
            raise ValueError("invalid profile: " + "; ".join(errors))
        return profile
    profile = default_profile()
    path.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
    return profile
