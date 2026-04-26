"""
Headless experiment runner for reproducible Werewolf AI evaluations.
"""

import argparse
import csv
import json
import random
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Dict, List

from engine import GameEngine

SUPPORTED_PROFILES = [
    "standard",
    "baseline_random",
    "baseline_majority",
    "ablation_no_memory",
    "ablation_role_agnostic",
]


def run_single_match(num_players: int, profile: str, seed: int) -> Dict[str, object]:
    """Run a single headless match and return a metrics snapshot."""
    random.seed(seed)
    game = GameEngine(num_players=num_players, ai_profile=profile)
    while not game.winner:
        game.advance_phase()
    summary = game.match_summary()
    summary["seed"] = seed
    return summary


def aggregate_results(results: List[Dict[str, object]]) -> Dict[str, object]:
    """Aggregate per-match outputs into report-level metrics."""
    winner_counts = Counter(result["winner"] for result in results)
    village_wins = winner_counts.get("Village", 0)
    werewolf_wins = winner_counts.get("Werewolves", 0)
    role_keys = sorted(
        {
            role
            for result in results
            for role in result["role_survival_rate"].keys()
        }
    )
    role_survival = {
        role: mean(result["role_survival_rate"].get(role, 0.0) for result in results)
        for role in role_keys
    }

    return {
        "matches": len(results),
        "village_win_rate": village_wins / len(results) if results else 0.0,
        "werewolf_win_rate": werewolf_wins / len(results) if results else 0.0,
        "average_days": mean(result["day_number"] for result in results) if results else 0.0,
        "average_total_phases": mean(result["total_phases"] for result in results) if results else 0.0,
        "average_vote_accuracy": mean(result["vote_accuracy"] for result in results) if results else 0.0,
        "average_false_accusation_rate": mean(
            result["false_accusation_rate"] for result in results
        )
        if results
        else 0.0,
        "average_role_survival_rate": role_survival,
        "winner_counts": dict(winner_counts),
    }


def write_match_csv(results: List[Dict[str, object]], path: Path) -> None:
    """Write per-match metrics to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "match_id",
                "seed",
                "ai_profile",
                "winner",
                "num_players",
                "day_number",
                "total_phases",
                "vote_accuracy",
                "false_accusation_rate",
            ],
        )
        writer.writeheader()
        for index, result in enumerate(results, start=1):
            writer.writerow(
                {
                    "match_id": index,
                    "seed": result["seed"],
                    "ai_profile": result["ai_profile"],
                    "winner": result["winner"],
                    "num_players": result["num_players"],
                    "day_number": result["day_number"],
                    "total_phases": result["total_phases"],
                    "vote_accuracy": f"{result['vote_accuracy']:.6f}",
                    "false_accusation_rate": f"{result['false_accusation_rate']:.6f}",
                }
            )


def run_experiments(
    num_matches: int,
    num_players: int,
    profile: str,
    seed: int,
) -> Dict[str, object]:
    """Run a batch of experiments and return both per-match and aggregate outputs."""
    results = [
        run_single_match(num_players=num_players, profile=profile, seed=seed + index)
        for index in range(num_matches)
    ]
    aggregate = aggregate_results(results)
    return {
        "profile": profile,
        "seed": seed,
        "num_matches": num_matches,
        "num_players": num_players,
        "aggregate": aggregate,
        "matches": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run reproducible headless Werewolf AI experiments."
    )
    parser.add_argument("--matches", type=int, default=200, help="Number of games to run.")
    parser.add_argument("--players", type=int, default=8, help="Players per game (6-12).")
    parser.add_argument(
        "--profile",
        type=str,
        default="standard",
        choices=SUPPORTED_PROFILES,
        help="AI profile to evaluate.",
    )
    parser.add_argument("--seed", type=int, default=1234, help="Base RNG seed.")
    parser.add_argument(
        "--json-out",
        type=str,
        default="results/summary.json",
        help="Output JSON summary path.",
    )
    parser.add_argument(
        "--csv-out",
        type=str,
        default="results/matches.csv",
        help="Output CSV matches path.",
    )
    parser.add_argument(
        "--timeline-out",
        type=str,
        default="results/timeline.json",
        help="Output timeline JSON path for replay summary.",
    )
    args = parser.parse_args()

    output = run_experiments(
        num_matches=max(1, args.matches),
        num_players=max(6, min(12, args.players)),
        profile=args.profile,
        seed=args.seed,
    )

    json_path = Path(args.json_out)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    write_match_csv(output["matches"], Path(args.csv_out))
    Path(args.timeline_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.timeline_out).write_text(
        json.dumps(
            [
                {
                    "match_id": index,
                    "seed": result["seed"],
                    "winner": result["winner"],
                    "timeline": result["timeline"],
                }
                for index, result in enumerate(output["matches"], start=1)
            ],
            indent=2,
        ),
        encoding="utf-8",
    )

    print(json.dumps(output["aggregate"], indent=2))


if __name__ == "__main__":
    main()
