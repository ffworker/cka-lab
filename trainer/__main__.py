from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
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


def _elapsed(active: dict) -> int:
    started = datetime.fromisoformat(active["startedAt"].replace("Z", "+00:00"))
    return max(0, int((datetime.now(timezone.utc) - started).total_seconds()))


def _rule(title: str) -> None:
    print("═" * 46)
    print(title.center(46))
    print("═" * 46)


def _difficulty(value: str) -> str:
    levels = {"easy": 1, "medium": 2, "hard": 3, "exam": 5}
    filled = levels.get(value, 0)
    return "★" * filled + "☆" * (5 - filled)


def _show_mission(scenario: dict, *, resumed: bool = False) -> None:
    _rule("INCIDENT // RESUME" if resumed else "INCIDENT // ACTIVE")
    print(f"\n{scenario['title']}")
    if scenario.get("codename") and scenario["codename"] != scenario["title"]:
        print(f"Codename     {scenario['codename']}")
    print(f"Domain       {scenario['category']} / {scenario['topic']}")
    print(f"Difficulty   {_difficulty(scenario['difficulty'])}  {scenario['difficulty']}")
    print(f"Target       {scenario.get('targetTimeMinutes', '—')} min")
    print(f"Reward       {scenario['xp']} XP")
    print("\nOBJECTIVE\n")
    print(scenario["missionBriefing"])
    print("\nSUCCESS\n\nSuccess criteria:")
    for criterion in scenario["successCriteria"]:
        print(f"✓ {criterion}")
    print("\nTimer continues." if resumed else "\nTimer started.")


def _show_profile(profile: dict, ranks: list[dict], achievements: list[dict], scenarios: list[dict]) -> None:
    _rule("CKA LAB // PILOT PROFILE")
    progress = rank_progress(profile["xp"], ranks)
    print(f"\nRank             {profile['rank']}")
    print(f"Total XP         {profile['xp']}")
    print(f"Missions         {len(profile['missionHistory'])}")
    print(f"First attempts   {profile['firstAttemptWins']}")
    print(f"Hints used       {profile['hintCount']}")
    print(f"Current streak   {profile['currentStreak']} day(s)")
    print(f"Best streak      {profile['bestStreak']} day(s)")
    if progress["nextRank"]:
        remaining = progress["nextMinimumXp"] - profile["xp"]
        print(f"\nNext rank        {progress['nextRank']} ({remaining} XP)")
    else:
        print("\nNext rank        maximum rank reached")
    print(progress["bar"])
    names = {item["id"]: item["name"] for item in achievements}
    earned = [names.get(item, item) for item in profile["achievements"]]
    print("\nAchievements")
    print("  " + (", ".join(earned) if earned else "none yet"))
    titles = {item["id"]: item["title"] for item in scenarios}
    print("\nRecent missions")
    if not profile["missionHistory"]:
        print("  none yet")
    for item in profile["missionHistory"][-5:][::-1]:
        title = titles.get(item["scenarioId"], item["scenarioId"])
        print(f"  {title} — {_duration(item['completionSeconds'])}, {item['xpAwarded']} XP")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cka-trainer")
    parser.add_argument("--runtime-dir", type=Path, default=REPO / ".cka-factory")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("status", "validate", "hint", "solution", "reset", "lab-up", "lab-down"):
        subparsers.add_parser(command)
    profile = subparsers.add_parser("profile")
    profile.add_argument("--json", action="store_true", dest="as_json")
    mission = subparsers.add_parser("mission")
    mission.add_argument("--mode", choices=sorted(SELECTION_MODES), default="mixed")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    profile = load_or_create_profile(args.runtime_dir)
    study_path = args.runtime_dir / "learner-state.json"
    if not study_path.is_file():
        study_path = REPO / "trainer/config/learner-state.default.json"
    scenario_root = Path(os.environ.get("CKA_TRAINER_SCENARIO_ROOT", REPO / "scenarios"))
    scenarios = discover_scenarios(scenario_root)
    ranks = load_catalogue(REPO / "trainer/config/ranks.json", "ranks")
    achievements = load_catalogue(REPO / "trainer/config/achievements.json", "achievements")
    profile["rank"] = rank_for_xp(profile["xp"], ranks)

    if args.command == "status":
        study = load_study_state(study_path)
        kubeconfig = args.runtime_dir / "kubeconfig"
        cluster_status = "NOT PROVISIONED"
        node_status = "0 / 2"
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
                    cluster_status = "READY"
                    node_status = "2 / 2"
                else:
                    cluster_status = "UNAVAILABLE"
                    node_status = f"{sum(' Ready ' in f' {line} ' for line in lines)} / 2"
            except (FileNotFoundError, subprocess.TimeoutExpired):
                cluster_status = "UNAVAILABLE"
                node_status = "? / 2"
        active_path = args.runtime_dir / "active-mission.json"
        active_name = "none"
        if active_path.is_file():
            active = json.loads(active_path.read_text(encoding="utf-8"))
            active_name = _scenario_by_id(scenarios, active["scenarioId"])["title"]
        next_action = "make mission  # resume active mission" if active_name != "none" else (
            "make mission" if cluster_status == "READY" else "make lab-up"
        )
        _rule("CKA LAB // MISSION CONTROL")
        print(f"\nCluster      {cluster_status}")
        print(f"Nodes        {node_status}")
        print(f"Mission      {active_name}")
        print(f"Rank         {profile['rank']}")
        print(f"XP           {profile['xp']}")
        print(f"Scenarios    {len(scenarios)}")
        print(f"Study state  weak: {len(study['weakTopics'])} | ready: {len(study['readyForPractice'])}")
        print(f"Next         {next_action}")
    elif args.command == "profile":
        if args.as_json:
            print(json.dumps(profile, indent=2))
        else:
            _show_profile(profile, ranks, achievements, scenarios)
    elif args.command == "mission":
        study = load_study_state(study_path)
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
                _show_mission(active_scenario, resumed=True)
                return 0
        if not scenarios:
            print(f"mission mode {args.mode}: no scenarios available; awaiting curriculum")
            return 0
        scenario = select_scenario(scenarios, study, profile, args.mode)
        if os.environ.get("CKA_FACTORY_DRY_RUN") == "1":
            _show_mission(scenario)
            print("Dry run: mission was not injected and no timer was saved.")
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
        _show_mission(scenario)
    elif args.command in {"lab-up", "lab-down"}:
        if os.environ.get("CKA_FACTORY_DRY_RUN") == "1":
            print(f"{args.command}: factory command available (dry run)")
        else:
            try:
                subprocess.run(
                    [REPO / "scripts/lab-factory.sh", args.command, args.runtime_dir],
                    cwd=REPO,
                    check=True,
                )
            except subprocess.CalledProcessError as error:
                print(
                    f"{args.command}: factory setup stopped with exit status {error.returncode}",
                    file=sys.stderr,
                )
                return error.returncode
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
                print("MISSION FAILED — not yet complete")
                _rule("MISSION NOT YET COMPLETE")
                print("\nChecks       ✗ Validator has not confirmed all success criteria")
                print(f"Attempt      {active['attempts']}")
                print(f"Time         {_duration(_elapsed(active))}")
                print("\nNext         keep investigating or run make hint")
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
            _rule("MISSION COMPLETE")
            print(f"\n{scenario['title']}\n")
            print(f"Time:         {_duration(result['completionSeconds'])}")
            print(f"Hints:        {active['hintCount']}")
            print(f"Attempts:     {active['attempts']}")
            print(f"XP:           +{result['xpAwarded']}")
            print(f"Total XP:     {profile['xp']}")
            for achievement in result["achievements"]:
                print(f"\n🏆 ACHIEVEMENT UNLOCKED\n   {achievement.upper()}")
            if result["oldRank"] != result["newRank"]:
                print(f"\nLEVEL UP\n{result['oldRank']}\n     ↓\n{result['newRank']}")
            print(f"\nCurrent rank: {result['newRank']}")
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
                    load_study_state(study_path),
                    profile,
                    "mixed",
                )
                print(f"\nRecommended next: {recommendation['title']}")
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
