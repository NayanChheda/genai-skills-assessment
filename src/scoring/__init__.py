"""
Scoring Engine Package

A modular, extensible scoring system for code assessments.
"""

from src.scoring.base import Scorer, ScorerResult
from src.scoring.engine import ScoringEngine
from src.scoring.code_quality import (
    BlackFormattingScorer,
    Flake8LintScorer,
    MypyTypeScorer,
)
from src.scoring.test_coverage import PytestCoverageScorer
from src.scoring.git_practices import GitPracticesScorer

__all__ = [
    "Scorer",
    "ScorerResult",
    "ScoringEngine",
    "BlackFormattingScorer",
    "Flake8LintScorer",
    "MypyTypeScorer",
    "PytestCoverageScorer",
    "GitPracticesScorer",
]
