# Gamification

The game layer rewards completing real cluster work. It does not replace the validator and does not maintain a second learning-state system.

## Ranks

| Rank | Minimum XP |
| --- | ---: |
| YAML Goblin | 0 |
| Pod Whisperer | 250 |
| CrashLoop Exorcist | 600 |
| DNS Detective | 1,000 |
| RBAC Sheriff | 1,600 |
| Scheduler Sorcerer | 2,400 |
| etcd Necromancer | 3,400 |
| Control Plane Commander | 5,000 |

The catalogue source is `trainer/config/ranks.json`.

## Achievements

| Achievement | Rule |
| --- | --- |
| No Hint Hero | Complete a mission without hints. |
| Phoenix Protocol | Reset and then complete a mission. |
| One Shot, One Pod | Validate successfully on the first attempt. |
| Kubectl Hat Trick | Complete missions on three study days in a row. |
| Against the Clock | Finish within the scenario's target time. |
| Cluster Regular | Complete ten missions. |

The catalogue source is `trainer/config/achievements.json`.

## What is recorded

A successful validation updates:

- XP and current rank;
- total attempts and hint usage;
- current and best study streak;
- first-attempt wins;
- total completion time;
- unlocked achievements;
- mission history with completion time and awarded XP.

Resetting an unfinished mission preserves its accumulated attempts and hint use. Cleaning a completed mission removes the practice objects but keeps the earned profile history.

## Privacy and portability

The profile is `.cka-factory/profile.json`. It is local, ignored by Git, and separate for each clone or user. CKA Lab does not currently provide profile sync, a leaderboard, or a hosted account system.
