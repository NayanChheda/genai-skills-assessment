"""
Unit tests for the scoring module.
"""

import pytest
from pathlib import Path

from src.scoring.base import Scorer, ScorerResult
from src.scoring.engine import ScoringEngine, ScoringReport


class DummyScorer(Scorer):
    """A simple scorer for testing."""
    
    name = "dummy"
    
    def __init__(self, score: float = 1.0, weight: float = 1.0) -> None:
        self.score = score
        self.weight = weight
    
    def evaluate(self, cwd: str = ".") -> ScorerResult:
        return ScorerResult(
            name=self.name,
            score=self.score,
            message=f"Dummy score: {self.score}",
        )


class FailingScorer(Scorer):
    """A scorer that always fails for testing error handling."""
    
    name = "failing"
    weight = 1.0
    
    def evaluate(self, cwd: str = ".") -> ScorerResult:
        raise ValueError("Intentional test failure")


class TestScorerResult:
    """Tests for ScorerResult dataclass."""
    
    def test_percentage(self) -> None:
        result = ScorerResult(name="test", score=0.85, message="Good")
        assert result.percentage == 85.0
    
    def test_percentage_zero(self) -> None:
        result = ScorerResult(name="test", score=0.0, message="None")
        assert result.percentage == 0.0
    
    def test_percentage_full(self) -> None:
        result = ScorerResult(name="test", score=1.0, message="Perfect")
        assert result.percentage == 100.0


class TestScoringEngine:
    """Tests for ScoringEngine."""
    
    def test_empty_engine(self) -> None:
        engine = ScoringEngine()
        report = engine.run()
        assert report.overall_score == 0.0
        assert len(report.results) == 0
    
    def test_single_scorer(self) -> None:
        engine = ScoringEngine()
        engine.add_scorer(DummyScorer(score=0.8))
        report = engine.run()
        assert report.overall_score == 80.0
        assert len(report.results) == 1
    
    def test_multiple_scorers_equal_weight(self) -> None:
        engine = ScoringEngine()
        engine.add_scorer(DummyScorer(score=1.0, weight=1.0))
        engine.add_scorer(DummyScorer(score=0.5, weight=1.0))
        report = engine.run()
        # (1.0 * 1.0 + 0.5 * 1.0) / 2.0 = 0.75
        assert report.overall_score == 75.0
    
    def test_weighted_scoring(self) -> None:
        engine = ScoringEngine()
        engine.add_scorer(DummyScorer(score=1.0, weight=0.7))
        engine.add_scorer(DummyScorer(score=0.0, weight=0.3))
        report = engine.run()
        # (1.0 * 0.7 + 0.0 * 0.3) / 1.0 = 0.7
        assert report.overall_score == 70.0
    
    def test_failing_scorer_handled(self) -> None:
        engine = ScoringEngine()
        engine.add_scorer(FailingScorer())
        report = engine.run()
        assert report.overall_score == 0.0
        assert len(report.results) == 1
        assert "failed" in report.results[0]["message"].lower()
    
    def test_chaining(self) -> None:
        engine = (
            ScoringEngine()
            .add_scorer(DummyScorer(score=1.0))
            .add_scorer(DummyScorer(score=0.5))
        )
        assert len(engine.scorers) == 2
    
    def test_save_report(self, tmp_path: Path) -> None:
        engine = ScoringEngine()
        engine.add_scorer(DummyScorer(score=0.9))
        output_path = str(tmp_path / "results.json")
        report = engine.run(output_path=output_path)
        
        assert Path(output_path).exists()
        
        import json
        with open(output_path) as f:
            data = json.load(f)
        assert data["overall_score"] == 90.0


class TestScoringReport:
    """Tests for ScoringReport."""
    
    def test_to_dict(self) -> None:
        report = ScoringReport(
            timestamp="2024-01-01T00:00:00",
            context="test",
            overall_score=85.0,
            results=[],
        )
        d = report.to_dict()
        assert d["timestamp"] == "2024-01-01T00:00:00"
        assert d["context"] == "test"
        assert d["overall_score"] == 85.0
    
    def test_to_json(self) -> None:
        report = ScoringReport(
            timestamp="2024-01-01T00:00:00",
            context="test",
            overall_score=85.0,
            results=[],
        )
        json_str = report.to_json()
        assert '"overall_score": 85.0' in json_str
