"""
Scoring Engine - Orchestrates all scorers and produces final results.
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.scoring.base import Scorer, ScorerResult


@dataclass
class ScoringReport:
    """Complete scoring report."""
    
    timestamp: str
    context: str
    overall_score: float
    results: list[dict[str, object]]
    
    def to_dict(self) -> dict[str, object]:
        """Convert to dictionary."""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    def save(self, path: str = "scoring_results.json") -> None:
        """Save report to file."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())


class ScoringEngine:
    """
    Orchestrates multiple scorers to produce a comprehensive assessment.
    
    Example:
        engine = ScoringEngine()
        engine.add_scorer(BlackFormattingScorer(weight=0.2))
        engine.add_scorer(Flake8LintScorer(weight=0.3))
        report = engine.run()
    """
    
    def __init__(self, context: str = "assessment") -> None:
        self.context = context
        self.scorers: list[Scorer] = []
    
    def add_scorer(self, scorer: Scorer) -> "ScoringEngine":
        """Add a scorer to the engine. Returns self for chaining."""
        self.scorers.append(scorer)
        return self
    
    def run(self, cwd: str = ".", output_path: Optional[str] = None) -> ScoringReport:
        """
        Run all scorers and produce a report.
        
        Args:
            cwd: Working directory for evaluation.
            output_path: Optional path to save results JSON.
            
        Returns:
            ScoringReport with all results and overall score.
        """
        results: list[ScorerResult] = []
        total_weight = 0.0
        weighted_score = 0.0
        
        for scorer in self.scorers:
            try:
                result = scorer.evaluate(cwd)
                results.append(result)
                weighted_score += result.score * scorer.weight
                total_weight += scorer.weight
            except Exception as e:
                # Handle scorer failures gracefully
                results.append(ScorerResult(
                    name=scorer.name,
                    score=0.0,
                    message=f"Scorer failed: {str(e)}",
                ))
                total_weight += scorer.weight
        
        overall = weighted_score / total_weight if total_weight > 0 else 0.0
        
        report = ScoringReport(
            timestamp=datetime.now().isoformat(),
            context=self.context,
            overall_score=round(overall * 100, 2),
            results=[
                {
                    "name": r.name,
                    "score": r.percentage,
                    "message": r.message,
                    "details": r.details,
                }
                for r in results
            ],
        )
        
        if output_path:
            report.save(output_path)
        
        return report
    
    def print_report(self, report: ScoringReport) -> None:
        """Print a formatted report to stdout."""
        print("=" * 60)
        print("ASSESSMENT SCORING REPORT")
        print("=" * 60)
        print(f"Timestamp: {report.timestamp}")
        print(f"Context: {report.context}")
        print("-" * 60)
        
        for result in report.results:
            name = str(result["name"]).replace("_", " ").title()
            score = result["score"]
            message = result["message"]
            print(f"{name:<25}: {score}% - {message}")
        
        print("=" * 60)
        print(f"Overall Score: {report.overall_score}%")
        print("=" * 60)
