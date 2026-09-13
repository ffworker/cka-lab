from __future__ import annotations

import argparse
import json
import os
import subprocess
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
        load_study_state(REPO / "docs/cka-shared/handoff.json")
        if scenarios:
            print(f"mission mode {args.mode}: selection weighting not implemented")
        else:
            print(f"mission mode {args.mode}: no scenarios available; awaiting curriculum")
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
        print(f"{args.command}: no active mission")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
