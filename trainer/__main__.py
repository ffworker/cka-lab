from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import (
    SELECTION_MODES,
    discover_scenarios,
    load_catalogue,
    load_or_create_profile,
    load_study_state,
    rank_for_xp,
)

REPO = Path(__file__).resolve().parents[1]


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
    scenarios = discover_scenarios(REPO / "scenarios")
    ranks = load_catalogue(REPO / "trainer/config/ranks.json", "ranks")
    load_catalogue(REPO / "trainer/config/achievements.json", "achievements")
    profile["rank"] = rank_for_xp(profile["xp"], ranks)

    if args.command == "status":
        study = load_study_state(REPO / "docs/cka-shared/handoff.json")
        print(f"factory: skeleton | cluster: not provisioned | scenarios: {len(scenarios)}")
        print(f"study-state: loaded | weak: {len(study['weakTopics'])} | ready: {len(study['readyForPractice'])}")
    elif args.command == "profile":
        print(json.dumps(profile, indent=2))
    elif args.command == "mission":
        load_study_state(REPO / "docs/cka-shared/handoff.json")
        if scenarios:
            print(f"mission mode {args.mode}: selection weighting not implemented")
        else:
            print(f"mission mode {args.mode}: no scenarios available; awaiting curriculum")
    elif args.command in {"lab-up", "lab-down"}:
        action = "provision" if args.command == "lab-up" else "destroy"
        print(f"{args.command}: dry skeleton only; would {action} cka-cp01 and cka-worker01")
    else:
        print(f"{args.command}: no active mission")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
