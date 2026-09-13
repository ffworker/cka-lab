from __future__ import annotations

import json
import re
from datetime import datetime, timedelta
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
    "successCriteria": list,
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
    if isinstance(identifier, str) and identifier != directory.name:
        errors.append("id must match scenario directory name")
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
    criteria = scenario.get("successCriteria")
    if isinstance(criteria, list) and (
        not criteria or any(not isinstance(item, str) or not item for item in criteria)
    ):
        errors.append("successCriteria must contain non-empty strings")
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


def rank_progress(
    xp: int, ranks: list[dict[str, Any]], *, width: int = 20
) -> dict[str, Any]:
    ordered = sorted(ranks, key=lambda rank: rank["minimumXp"])
    current_index = max(
        index for index, rank in enumerate(ordered) if xp >= rank["minimumXp"]
    )
    if current_index == len(ordered) - 1:
        return {"bar": "█" * width, "nextRank": None, "nextMinimumXp": None}
    current = ordered[current_index]
    following = ordered[current_index + 1]
    span = following["minimumXp"] - current["minimumXp"]
    gained = xp - current["minimumXp"]
    filled = min(width, gained * width // span)
    return {
        "bar": "█" * filled + "░" * (width - filled),
        "nextRank": following["name"],
        "nextMinimumXp": following["minimumXp"],
    }


def select_scenario(
    scenarios: list[dict[str, Any]],
    study: dict[str, Any],
    profile: dict[str, Any],
    mode: str,
) -> dict[str, Any]:
    if not scenarios:
        raise ValueError("no scenarios available")
    not_introduced = set(study.get("notYetIntroduced", []))
    eligible = [
        item for item in scenarios
        if item.get("topic") not in not_introduced
        and not not_introduced.intersection(item.get("prerequisites", []))
    ]
    if not eligible:
        raise ValueError("no scenarios are eligible for the current learning state")
    last_id = None
    if profile.get("missionHistory"):
        last_id = profile["missionHistory"][-1].get("scenarioId")
    candidates = [item for item in eligible if item["id"] != last_id] or eligible

    weak = set(study.get("weakTopics", []))
    improving = set(study.get("improvingTopics", []))
    stable = set(study.get("stableTopics", []))

    def score(item: dict[str, Any]) -> tuple[int, str]:
        tags = set(item.get("learningStateTags", []))
        topic = item.get("topic")
        value = 0
        if mode in {"weak", "mixed", "timed", "mock-exam"}:
            value += 100 if topic in weak or "weak" in tags else 0
        if mode in {"improving", "mixed", "timed", "mock-exam"}:
            value += 50 if topic in improving or "improving" in tags else 0
        if mode in {"troubleshooting", "mixed", "mock-exam"}:
            value += 70 if "unstable" in tags else 0
            value += 30 if item.get("category") == "troubleshooting" else 0
        if mode in {"stable", "mixed", "random"}:
            value += 20 if topic in stable and item.get("revisionEligible") else 0
        return (-value, item["id"])

    return sorted(candidates, key=score)[0]


def next_hint(active: dict[str, Any], scenario: dict[str, Any]) -> str | None:
    index = active.get("hintCount", 0)
    hints = scenario["hints"]
    if index >= len(hints):
        return None
    active["hintCount"] = index + 1
    return hints[index]


def complete_mission(
    active: dict[str, Any],
    scenario: dict[str, Any],
    profile: dict[str, Any],
    ranks: list[dict[str, Any]],
    achievements: list[dict[str, Any]],
    *,
    completed_at: str,
) -> dict[str, Any]:
    finished = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
    started = datetime.fromisoformat(active["startedAt"].replace("Z", "+00:00"))
    completion_seconds = max(0, int((finished - started).total_seconds()))
    attempts = active["attempts"]
    hints = active.get("hintCount", 0)
    old_rank = rank_for_xp(profile["xp"], ranks)

    profile["xp"] += scenario["xp"]
    profile["attempts"] += attempts
    profile["hintCount"] += hints
    profile["totalCompletionSeconds"] += completion_seconds
    first_attempt = attempts == 1
    if first_attempt:
        profile["firstAttemptWins"] += 1

    previous_day = None
    if profile["missionHistory"]:
        previous = datetime.fromisoformat(
            profile["missionHistory"][-1]["completedAt"].replace("Z", "+00:00")
        )
        previous_day = previous.date()
    finished_day = finished.date()
    if previous_day == finished_day:
        profile["currentStreak"] = max(1, profile["currentStreak"])
    elif previous_day == finished_day - timedelta(days=1):
        profile["currentStreak"] += 1
    else:
        profile["currentStreak"] = 1
    profile["bestStreak"] = max(profile["bestStreak"], profile["currentStreak"])

    profile["missionHistory"].append({
        "scenarioId": scenario["id"],
        "completedAt": completed_at,
        "completionSeconds": completion_seconds,
        "attempts": attempts,
        "hintCount": hints,
        "firstAttemptWin": first_attempt,
        "xpAwarded": scenario["xp"],
    })
    unlocked_rules = {
        "no-hint-hero": hints == 0,
        "phoenix-protocol": active.get("resetCount", 0) > 0,
        "first-attempt": first_attempt,
        "streak-three": profile["currentStreak"] >= 3,
        "under-clock": completion_seconds <= scenario.get("targetTimeMinutes", 0) * 60,
        "ten-missions": len(profile["missionHistory"]) >= 10,
    }
    names = {item["id"]: item["name"] for item in achievements}
    newly_unlocked = []
    for identifier, earned in unlocked_rules.items():
        if earned and identifier in names and identifier not in profile["achievements"]:
            profile["achievements"].append(identifier)
            newly_unlocked.append(names[identifier])
    profile["rank"] = rank_for_xp(profile["xp"], ranks)
    return {
        "completionSeconds": completion_seconds,
        "xpAwarded": scenario["xp"],
        "oldRank": old_rank,
        "newRank": profile["rank"],
        "achievements": newly_unlocked,
    }


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
