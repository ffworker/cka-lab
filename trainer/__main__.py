from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .core import (
    SELECTION_MODES,
    complete_mission,
    discover_scenarios,
    load_catalogue,
    load_or_create_profile,
    load_study_state,
    next_hint,
    rank_for_xp,
    rank_progress,
    select_scenario,
)

REPO = Path(__file__).resolve().parents[1]


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _run_scenario_script(
    scenario: dict, scenario_root: Path, field: str, runtime_dir: Path
) -> subprocess.CompletedProcess[str]:
    script = (scenario_root / scenario["id"] / scenario[field]).resolve()
    scenario_dir = (scenario_root / scenario["id"]).resolve()
    if not script.is_relative_to(scenario_dir) or not script.is_file():
        raise ValueError(f"unsafe or missing scenario {field}: {script}")
    env = {
        **os.environ,
        "CKA_RUNTIME_DIR": str(runtime_dir.resolve()),
        "KUBECONFIG": str((runtime_dir / "kubeconfig").resolve()),
    }
    return subprocess.run(
        [script], cwd=scenario_dir, env=env, text=True, capture_output=True, check=False
    )


def _scenario_by_id(scenarios: list[dict], identifier: str) -> dict:
    try:
        return next(item for item in scenarios if item["id"] == identifier)
    except StopIteration as error:
        raise ValueError(f"active scenario no longer exists: {identifier}") from error


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _duration(seconds: int) -> str:
    minutes, remainder = divmod(seconds, 60)
    return f"{minutes:02d}:{remainder:02d}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cka-trainer")
    parser.add_argument("--runtime-dir", type=Path, default=REPO / ".cka-factory")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("status", "validate", "hint", "solution", "reset", "profile", "lab-up", "lab-down"):
        subparsers.add_parser(command)
    mission = subparsers.add_parser("mission")
    mission.add_argument("--mode", choices=sorted(SELECTION_MODES), default="mixed")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    profile = load_or_create_profile(args.runtime_dir)
    scenario_root = Path(os.environ.get("CKA_TRAINER_SCENARIO_ROOT", REPO / "scenarios"))
    scenarios = discover_scenarios(scenario_root)
    ranks = load_catalogue(REPO / "trainer/config/ranks.json", "ranks")
    load_catalogue(REPO / "trainer/config/achievements.json", "achievements")
    profile["rank"] = rank_for_xp(profile["xp"], ranks)

    if args.command == "status":
        study = load_study_state(REPO / "trainer/config/learner-state.default.json")
        kubeconfig = args.runtime_dir / "kubeconfig"
        cluster_status = "not provisioned"
        if kubeconfig.is_file():
            env = {**os.environ, "KUBECONFIG": str(kubeconfig)}
            try:
                nodes = subprocess.run(
                    ["kubectl", "get", "nodes", "--no-headers"],
                    env=env,
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=10,
                )
                lines = nodes.stdout.splitlines()
                if nodes.returncode == 0 and len(lines) == 2 and all(" Ready " in f" {line} " for line in lines):
                    cluster_status = "ready (2 nodes)"
                else:
                    cluster_status = "unreachable or not ready"
            except (FileNotFoundError, subprocess.TimeoutExpired):
                cluster_status = "unreachable or not ready"
        print(f"factory: active | cluster: {cluster_status} | scenarios: {len(scenarios)}")
        print(f"study-state: loaded | weak: {len(study['weakTopics'])} | ready: {len(study['readyForPractice'])}")
    elif args.command == "profile":
        print(json.dumps(profile, indent=2))
    elif args.command == "mission":
        study = load_study_state(REPO / "trainer/config/learner-state.default.json")
        active_path = args.runtime_dir / "active-mission.json"
        if active_path.is_file():
            active = json.loads(active_path.read_text(encoding="utf-8"))
            active_scenario = _scenario_by_id(scenarios, active["scenarioId"])
            if active.get("completed"):
                cleaned = _run_scenario_script(
                    active_scenario, scenario_root, "reset", args.runtime_dir
                )
                if cleaned.returncode != 0:
                    print(cleaned.stderr or cleaned.stdout, end="")
                    return cleaned.returncode
                active_path.unlink()
            else:
                print(f"MISSION ACTIVE: {active_scenario['title']}")
                print(active_scenario["missionBriefing"])
                print("\nSuccess criteria:")
                for criterion in active_scenario["successCriteria"]:
                    print(f"- {criterion}")
                return 0
        if not scenarios:
            print(f"mission mode {args.mode}: no scenarios available; awaiting curriculum")
            return 0
        scenario = select_scenario(scenarios, study, profile, args.mode)
        if os.environ.get("CKA_FACTORY_DRY_RUN") == "1":
            print(f"mission dry-run: {scenario['id']}")
            return 0
        injected = _run_scenario_script(scenario, scenario_root, "injector", args.runtime_dir)
        if injected.returncode != 0:
            print(injected.stderr or injected.stdout, end="")
            return injected.returncode
        active = {
            "scenarioId": scenario["id"],
            "startedAt": _now(),
            "attempts": 0,
            "hintCount": 0,
            "resetCount": 0,
            "completed": False,
        }
        _write_json(active_path, active)
        print("═" * 46)
        print(f"MISSION: {scenario['title']}")
        print("═" * 46)
        print(scenario["missionBriefing"])
        print("\nSuccess criteria:")
        for criterion in scenario["successCriteria"]:
            print(f"- {criterion}")
        print(f"\nTarget: {scenario.get('targetTimeMinutes', '—')} minutes | XP: {scenario['xp']}")
    elif args.command in {"lab-up", "lab-down"}:
        if os.environ.get("CKA_FACTORY_DRY_RUN") == "1":
            print(f"{args.command}: factory command available (dry run)")
        else:
            subprocess.run(
                [REPO / "scripts/lab-factory.sh", args.command, args.runtime_dir],
                cwd=REPO,
                check=True,
            )
    else:
        active_path = args.runtime_dir / "active-mission.json"
        if not active_path.is_file():
            print(f"{args.command}: no active mission")
            return 0
        active = json.loads(active_path.read_text(encoding="utf-8"))
        scenario = _scenario_by_id(scenarios, active["scenarioId"])
        if args.command == "validate":
            if active.get("completed"):
                print("validate: mission already completed; run make reset")
                return 0
            active["attempts"] += 1
            checked = _run_scenario_script(scenario, scenario_root, "validator", args.runtime_dir)
            if checked.returncode != 0:
                _write_json(active_path, active)
                print("MISSION FAILED")
                if checked.stdout:
                    print(checked.stdout.strip())
                return 1
            result = complete_mission(
                active,
                scenario,
                profile,
                ranks,
                load_catalogue(REPO / "trainer/config/achievements.json", "achievements"),
                completed_at=_now(),
            )
            active["completed"] = True
            _write_json(active_path, active)
            _write_json(args.runtime_dir / "profile.json", profile)
            print("═" * 46)
            print("              MISSION COMPLETE")
            print("═" * 46)
            print(f'"{scenario["title"]}"\n')
            print(f"Time:         {_duration(result['completionSeconds'])}")
            print(f"Hints:        {active['hintCount']}")
            print(f"Attempts:     {active['attempts']}")
            print(f"XP:           +{result['xpAwarded']}")
            for achievement in result["achievements"]:
                print(f"\n🏆 ACHIEVEMENT UNLOCKED\n   {achievement.upper()}")
            print(f"\nRank: {result['oldRank']} → {result['newRank']}")
            progress = rank_progress(profile["xp"], ranks)
            print(progress["bar"])
            if progress["nextRank"]:
                print(
                    f"{progress['nextMinimumXp'] - profile['xp']} XP to "
                    f"{progress['nextRank']}"
                )
            remaining = [item for item in scenarios if item["id"] != scenario["id"]]
            if remaining:
                recommendation = select_scenario(
                    remaining,
                    load_study_state(REPO / "trainer/config/learner-state.default.json"),
                    profile,
                    "mixed",
                )
                print(f"\nNext recommendation: {recommendation['title']}")
            print("═" * 46)
        elif args.command == "hint":
            if active.get("completed"):
                print("hint: mission already completed")
                return 0
            hint = next_hint(active, scenario)
            if hint is None:
                print("No more hints. Request the solution explicitly if needed.")
            else:
                _write_json(active_path, active)
                print(f"HINT {active['hintCount']}: {hint}")
        elif args.command == "solution":
            solution = scenario_root / scenario["id"] / scenario["solution"]
            print(solution.read_text(encoding="utf-8").strip())
        elif args.command == "reset":
            reset = _run_scenario_script(scenario, scenario_root, "reset", args.runtime_dir)
            if reset.returncode != 0:
                print(reset.stderr or reset.stdout, end="")
                return reset.returncode
            if active.get("completed"):
                active_path.unlink()
                print(f"reset: cleaned completed mission {scenario['title']}")
            else:
                reinjected = _run_scenario_script(scenario, scenario_root, "injector", args.runtime_dir)
                if reinjected.returncode != 0:
                    print(reinjected.stderr or reinjected.stdout, end="")
                    return reinjected.returncode
                active.update({
                    "startedAt": _now(),
                    "resetCount": active.get("resetCount", 0) + 1,
                })
                _write_json(active_path, active)
                print(f"reset: {scenario['title']} restored and timer restarted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
