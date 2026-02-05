#!/usr/bin/env python3
"""
Automated Scoring CLI

A thin wrapper around the modular scoring engine for backward compatibility.
Run with: python automated_scoring.py [--output PATH]
"""

import argparse
import os
import sys

# Set up encoding for subprocesses
os.environ["PYTHONIOENCODING"] = "utf-8"

from src.scoring import (
    ScoringEngine,
    BlackFormattingScorer,
    Flake8LintScorer,
    MypyTypeScorer,
    PytestCoverageScorer,
    GitPracticesScorer,
)


def create_default_engine() -> ScoringEngine:
    """Create scoring engine with default configuration."""
    engine = ScoringEngine(context="assessment_repository")
    
    # Add scorers with weights matching original implementation
    engine.add_scorer(BlackFormattingScorer(weight=0.2, paths="src/ challenges/"))
    engine.add_scorer(Flake8LintScorer(weight=0.3, paths="src/ challenges/"))
    engine.add_scorer(MypyTypeScorer(weight=0.3, paths="src/"))
    engine.add_scorer(PytestCoverageScorer(weight=0.1, source="src"))
    engine.add_scorer(GitPracticesScorer(weight=0.1))
    
    return engine


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run automated code quality assessment"
    )
    parser.add_argument(
        "--output", "-o",
        default="scoring_results.json",
        help="Output file for scoring results (default: scoring_results.json)",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress detailed output",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=60.0,
        help="Minimum passing score percentage (default: 60)",
    )
    parser.add_argument(
        "--assessment-mode",
        action="store_true",
        help="Run in assessment mode (more lenient on failures)",
    )
    
    args = parser.parse_args()
    
    if not args.quiet:
        print("Running automated code assessment...")
        print("Note: Low coverage is expected in assessment repositories")
        print("=" * 60)
    
    engine = create_default_engine()
    report = engine.run(cwd=".", output_path=args.output)
    
    if not args.quiet:
        engine.print_report(report)
    
    # Exit based on threshold
    if report.overall_score < args.threshold:
        if not args.quiet:
            print(f"Warning: Score {report.overall_score}% below threshold ({args.threshold}%)")
        sys.exit(1)
    else:
        if not args.quiet:
            print("Success: Assessment meets requirements")
        sys.exit(0)


if __name__ == "__main__":
    main()
