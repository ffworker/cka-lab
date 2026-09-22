import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from trainer.core import (
    SELECTION_MODES,
    complete_mission,
    default_profile,
    discover_scenarios,
    load_catalogue,
    load_or_create_profile,
    load_study_state,
    next_hint,
    rank_for_xp,
    rank_progress,
    select_scenario,
    validate_scenario,
)

REPO = Path(__file__).resolve().parents[2]


def test_study_state_reader_preserves_training_inputs():
    path = REPO / "trainer/config/learner-state.default.json"
    payload = json.loads(path.read_text())
    state = load_study_state(path)
    assert state["readyForPractice"]
    assert state["recommendedDrills"]
    assert "practicalFeedback" in state
    assert payload["lastUpdated"] is None
    assert payload["theoryStatus"]["weakTopics"] == []
    assert payload["theoryStatus"]["improvingTopics"] == []
    assert payload["theoryStatus"]["stableTopics"] == []
    assert payload["theoryStatus"]["unstableConcepts"] == []
    assert payload["theoryStatus"]["recentQuizFindings"] == []
    assert payload["practicalFeedback"] == {
        "recentPracticeFindings": [],
        "successfulTasks": [],
        "theoryFollowupNeeded": [],
    }
    forbidden_personal_keys = {
        "xp",
        "attempts",
        "hints",
        "hintCount",
        "streak",
        "achievements",
        "missionHistory",
        "completedMissions",
    }

    def nested_keys(value):
        if isinstance(value, dict):
            for key, child in value.items():
                yield key
                yield from nested_keys(child)
        elif isinstance(value, list):
            for child in value:
                yield from nested_keys(child)

    assert forbidden_personal_keys.isdisjoint(nested_keys(payload))
    scenarios = discover_scenarios(REPO / "scenarios")
    curriculum = set(payload["practicalFocus"]["readyForPractice"])
    required = {
        item
        for scenario in scenarios
        for item in [scenario["topic"], *scenario["prerequisites"]]
    }
    assert required <= curriculum
    assert SELECTION_MODES == {
        "weak", "improving", "stable", "mixed", "troubleshooting",
        "timed", "random", "mock-exam",
    }


def test_cli_prefers_ignored_local_learner_state(tmp_path):
    default_path = REPO / "trainer/config/learner-state.default.json"
    payload = json.loads(default_path.read_text())
    payload["theoryStatus"]["weakTopics"] = ["Deployments"]
    (tmp_path / "learner-state.json").write_text(json.dumps(payload) + "\n")

    result = subprocess.run(
        [sys.executable, "-m", "trainer", "--runtime-dir", str(tmp_path), "status"],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "CKA_FACTORY_DRY_RUN": "1"},
    )

    assert result.returncode == 0, result.stderr
    assert "weak: 1" in result.stdout


def test_cli_uses_neutral_default_without_creating_local_state(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "trainer", "--runtime-dir", str(tmp_path), "status"],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "CKA_FACTORY_DRY_RUN": "1"},
    )

    assert result.returncode == 0, result.stderr
    assert "weak: 0" in result.stdout
    assert not (tmp_path / "learner-state.json").exists()


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
        "successCriteria": ["The workload is healthy."],
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
        "successCriteria": ["The workload is healthy."],
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


def _scenario(identifier, topic, tags, *, xp=140, target=10):
    return {
        "id": identifier,
        "title": identifier,
        "topic": topic,
        "learningStateTags": tags,
        "xp": xp,
        "targetTimeMinutes": target,
        "hints": ["first", "second"],
    }


def test_scenario_selection_prioritizes_weak_state_and_avoids_last_mission():
    scenarios = [
        _scenario("deployment-trace", "Deployments", ["weak", "unstable"]),
        _scenario("service-repair", "Services", ["improving", "unstable"]),
        _scenario("taint-revision", "Taints and Tolerations", ["stable"]),
    ]
    state = {
        "weakTopics": ["Deployments"],
        "improvingTopics": ["Services"],
        "stableTopics": ["Taints and Tolerations"],
        "unstableConcepts": ["Deployment -> ReplicaSet -> Pods"],
    }
    profile = default_profile()
    assert select_scenario(scenarios, state, profile, "mixed")["id"] == "deployment-trace"
    profile["missionHistory"].append({"scenarioId": "deployment-trace"})
    assert select_scenario(scenarios, state, profile, "mixed")["id"] == "service-repair"


def test_selection_excludes_topics_not_yet_introduced():
    future = _scenario("future-job", "Jobs", ["weak"])
    ready = _scenario("pod-repair", "Pods", ["improving"])
    state = {
        "weakTopics": ["Jobs"],
        "improvingTopics": ["Pods"],
        "stableTopics": [],
        "notYetIntroduced": ["Jobs"],
    }

    assert select_scenario([future, ready], state, default_profile(), "mixed")["id"] == "pod-repair"


def test_progressive_hints_stop_after_two():
    active = {"hintCount": 0}
    scenario = _scenario("service-repair", "Services", ["improving"])
    assert next_hint(active, scenario) == "first"
    assert active["hintCount"] == 1
    assert next_hint(active, scenario) == "second"
    assert next_hint(active, scenario) is None


def test_completion_awards_xp_history_achievements_and_rank():
    profile = default_profile()
    profile["xp"] = 200
    active = {
        "scenarioId": "deployment-trace",
        "startedAt": "2026-09-13T14:00:00+00:00",
        "attempts": 1,
        "hintCount": 0,
        "resetCount": 1,
    }
    scenario = _scenario("deployment-trace", "Deployments", ["weak"], xp=140, target=10)
    ranks = [
        {"name": "YAML Goblin", "minimumXp": 0},
        {"name": "Pod Whisperer", "minimumXp": 250},
    ]
    achievements = [
        {"id": "no-hint-hero", "name": "No Hint Hero"},
        {"id": "phoenix-protocol", "name": "Phoenix Protocol"},
        {"id": "first-attempt", "name": "One Shot, One Pod"},
        {"id": "under-clock", "name": "Against the Clock"},
    ]
    result = complete_mission(
        active,
        scenario,
        profile,
        ranks,
        achievements,
        completed_at="2026-09-13T14:08:42+00:00",
    )
    assert profile["xp"] == 340
    assert profile["rank"] == "Pod Whisperer"
    assert profile["firstAttemptWins"] == 1
    assert profile["missionHistory"][0]["completionSeconds"] == 522
    assert profile["missionHistory"][0]["xpAwarded"] == 140
    assert set(profile["achievements"]) == {
        "no-hint-hero", "phoenix-protocol", "first-attempt", "under-clock"
    }
    assert result["oldRank"] == "YAML Goblin"
    assert result["newRank"] == "Pod Whisperer"


def test_scenario_discovery_rejects_symlinked_directory(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "scenario.json").write_text("{}")
    catalog = tmp_path / "catalog"
    catalog.mkdir()
    (catalog / "linked").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="symlinked scenario directory"):
        discover_scenarios(catalog)


def test_scenario_id_must_match_its_directory_name(tmp_path):
    scenario = _scenario("different-id", "Pods", ["improving"])
    scenario.update({
        "injector": "inject.sh",
        "validator": "validate.sh",
        "reset": "reset.sh",
        "solution": "solution.md",
    })
    directory = tmp_path / "directory-name"
    directory.mkdir()
    for field in ("injector", "validator", "reset", "solution"):
        (directory / scenario[field]).write_text("placeholder\n")

    assert "id must match scenario directory name" in validate_scenario(
        scenario, directory
    )


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


def test_rank_progress_reports_next_threshold_and_bar():
    ranks = load_catalogue(REPO / "trainer/config/ranks.json", "ranks")

    progress = rank_progress(140, ranks, width=20)

    assert progress == {
        "bar": "███████████░░░░░░░░░",
        "nextRank": "Pod Whisperer",
        "nextMinimumXp": 250,
    }


def test_endpoint_scenario_validators_query_actual_endpoint_slices():
    scenarios = discover_scenarios(REPO / "scenarios")
    endpoint_scenarios = [
        item for item in scenarios
        if any("EndpointSlice" in criterion for criterion in item["successCriteria"])
    ]

    assert endpoint_scenarios
    for scenario in endpoint_scenarios:
        validator = REPO / "scenarios" / scenario["id"] / scenario["validator"]
        assert "endpointslice" in validator.read_text(encoding="utf-8").lower()


def test_validators_check_the_full_declared_cluster_contract():
    validators = {
        scenario_id: (REPO / "scenarios" / scenario_id / "validate.sh").read_text()
        for scenario_id in (
            "deployment-replica-trail",
            "service-endpoints",
            "config-secret-env",
            "rolling-rollback",
        )
    }

    deployment = validators["deployment-replica-trail"]
    for field in ("updatedReplicas", "readyReplicas", "availableReplicas"):
        assert field in deployment
    assert "condition=Ready" in deployment

    service = validators["service-endpoints"]
    assert "conditions.ready==true" in service
    assert ".spec.type}:{.spec.ports[0].port" in service

    configuration = validators["config-secret-env"]
    assert "configMapKeyRef.name" in configuration
    assert "configMapKeyRef.key" in configuration

    rollback = validators["rolling-rollback"]
    assert ".metadata.uid" in rollback
    assert "ownerReferences" in rollback


def test_taint_mission_only_removes_its_exact_owned_taint():
    directory = REPO / "scenarios/taint-toleration"
    injector = (directory / "inject.sh").read_text()
    reset = (directory / "reset.sh").read_text()
    validator = (directory / "validate.sh").read_text()

    assert "training-" not in injector
    assert "training-" not in reset
    assert "training:NoSchedule-" in reset
    assert "refusing to overwrite non-factory training taint" in injector
    assert 'eq .value "dedicated"' in validator


def test_factory_delegates_to_pinned_proxmox_scenario(tmp_path):
    adapter = REPO / "scripts/lab-factory.sh"
    proxmox_root = tmp_path / "proxmox-lab"
    delegated = (
        proxmox_root
        / "scenarios/cka-kubernetes-proxmox/scripts/lab-factory.sh"
    )
    delegated.parent.mkdir(parents=True)
    delegated.write_text(
        '#!/bin/sh\nprintf "%s\\n" "$1" "$2" >"$CAPTURE"\n',
        encoding="utf-8",
    )
    delegated.chmod(0o755)
    runtime = tmp_path / "runtime"
    capture = tmp_path / "delegated-arguments"

    result = subprocess.run(
        [adapter, "lab-up", runtime],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
        env={
            **os.environ,
            "PROXMOX_LAB_ROOT": str(proxmox_root),
            "CAPTURE": str(capture),
        },
    )

    assert result.returncode == 0, result.stderr
    assert capture.read_text().splitlines() == ["lab-up", str(runtime)]
    script = adapter.read_text()
    assert "scenarios/cka-kubernetes-proxmox/scripts/lab-factory.sh" in script
    assert "infrastructure/proxmox" not in script


def test_factory_rejects_relative_proxmox_override(tmp_path):
    result = subprocess.run(
        [REPO / "scripts/lab-factory.sh", "lab-down", tmp_path / "runtime"],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PROXMOX_LAB_ROOT": "../proxmox-lab"},
    )
    assert result.returncode == 1
    assert "must be an absolute path" in result.stderr


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
            env={**os.environ, "CKA_FACTORY_DRY_RUN": "1"},
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


def test_cli_runs_a_complete_mission_loop(tmp_path):
    scenario_root = tmp_path / "scenarios"
    mission = scenario_root / "test-mission"
    mission.mkdir(parents=True)
    metadata = {
        "id": "test-mission",
        "title": "Test Mission",
        "codename": "test-mission",
        "category": "troubleshooting",
        "topic": "Deployments",
        "difficulty": "easy",
        "prerequisites": ["Pods"],
        "learningStateTags": ["weak"],
        "revisionEligible": True,
        "missionBriefing": "Repair the test workload.",
        "successCriteria": ["The marker exists."],
        "injector": "inject.sh",
        "validator": "validate.sh",
        "reset": "reset.sh",
        "hints": ["Inspect the marker.", "Create the solved marker."],
        "solution": "solution.md",
        "xp": 140,
        "targetTimeMinutes": 10,
    }
    (mission / "scenario.json").write_text(json.dumps(metadata))
    (mission / "inject.sh").write_text("#!/bin/sh\ntouch \"$CKA_RUNTIME_DIR/injected\"\n")
    (mission / "validate.sh").write_text(
        "#!/bin/sh\ntest -f \"$CKA_RUNTIME_DIR/solved\"\n"
    )
    (mission / "reset.sh").write_text(
        "#!/bin/sh\nrm -f \"$CKA_RUNTIME_DIR/injected\" \"$CKA_RUNTIME_DIR/solved\"\n"
    )
    (mission / "solution.md").write_text("Create the solved marker.\n")
    for script in mission.glob("*.sh"):
        script.chmod(0o755)
    runtime = tmp_path / "runtime"
    env = {
        **os.environ,
        "CKA_TRAINER_SCENARIO_ROOT": str(scenario_root),
        "CKA_RUNTIME_DIR": str(runtime),
    }

    def run(command):
        return subprocess.run(
            [sys.executable, "-m", "trainer", "--runtime-dir", str(runtime), command],
            cwd=REPO,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    started = run("mission")
    assert started.returncode == 0
    assert "Test Mission" in started.stdout
    assert (runtime / "active-mission.json").is_file()
    assert (runtime / "injected").is_file()
    resumed = run("mission")
    assert "Success criteria:" in resumed.stdout

    failed = run("validate")
    assert failed.returncode == 1
    assert "MISSION FAILED" in failed.stdout
    hint = run("hint")
    assert "Inspect the marker." in hint.stdout
    assert "Create the solved marker." in run("solution").stdout
    restarted = run("reset")
    assert restarted.returncode == 0
    restarted_active = json.loads((runtime / "active-mission.json").read_text())
    assert restarted_active["attempts"] == 1
    assert restarted_active["hintCount"] == 1
    assert restarted_active["resetCount"] == 1

    (runtime / "solved").touch()
    passed = run("validate")
    assert passed.returncode == 0
    assert "MISSION COMPLETE" in passed.stdout
    profile = json.loads((runtime / "profile.json").read_text())
    assert profile["xp"] == 140
    assert profile["missionHistory"][0]["scenarioId"] == "test-mission"

    (mission / "reset.sh").write_text("#!/bin/sh\nexit 1\n")
    (mission / "reset.sh").chmod(0o755)
    blocked_reset = run("reset")
    assert blocked_reset.returncode == 1
    assert (runtime / "active-mission.json").is_file()
    blocked_start = run("mission")
    assert blocked_start.returncode == 1
    assert (runtime / "active-mission.json").is_file()

    (mission / "reset.sh").write_text(
        "#!/bin/sh\nrm -f \"$CKA_RUNTIME_DIR/injected\" \"$CKA_RUNTIME_DIR/solved\"\n"
    )
    (mission / "reset.sh").chmod(0o755)
    reset = run("reset")
    assert reset.returncode == 0
    assert not (runtime / "active-mission.json").exists()
    assert not (runtime / "injected").exists()
