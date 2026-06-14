#!/usr/bin/env python3
"""Convert grades with the modified Bavarian formula."""

from __future__ import annotations

import argparse


def convert(best: float, pass_grade: float, score: float, high_is_good: bool) -> float:
    if high_is_good:
        if not best > pass_grade:
            raise ValueError("--best must be greater than --pass for high-is-good scales")
        german = 1 + 3 * (best - score) / (best - pass_grade)
    else:
        if not best < pass_grade:
            raise ValueError("--best must be less than --pass for low-is-good scales")
        german = 1 + 3 * (score - best) / (pass_grade - best)
    return max(1.0, min(4.0, german))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate a German grade using the modified Bavarian formula."
    )
    parser.add_argument("--best", type=float, required=True, help="Best possible grade on the source scale")
    parser.add_argument("--pass", dest="pass_grade", type=float, required=True, help="Lowest passing grade on the source scale")
    parser.add_argument("--score", type=float, required=True, help="Applicant's grade on the source scale")
    parser.add_argument(
        "--direction",
        choices=("high-is-good", "low-is-good"),
        required=True,
        help="Whether higher source grades are better, or lower source grades are better",
    )
    args = parser.parse_args()

    german = convert(
        best=args.best,
        pass_grade=args.pass_grade,
        score=args.score,
        high_is_good=args.direction == "high-is-good",
    )
    print(f"{german:.2f}")


if __name__ == "__main__":
    main()
