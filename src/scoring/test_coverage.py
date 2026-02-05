"""
Test coverage scorer using pytest.
"""

import subprocess
from typing import Tuple

from src.scoring.base import Scorer, ScorerResult


def run_command(cmd: str, cwd: str = ".") -> Tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=cwd,
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


class PytestCoverageScorer(Scorer):
    """Scores test coverage using pytest-cov."""
    
    name = "test_coverage"
    description = "Test coverage with pytest"
    
    def __init__(
        self, 
        weight: float = 0.1, 
        source: str = "src",
        threshold: float = 0.0,  # Minimum expected coverage
    ) -> None:
        self.weight = weight
        self.source = source
        self.threshold = threshold
    
    def evaluate(self, cwd: str = ".") -> ScorerResult:
        return_code, stdout, stderr = run_command(
            f"pytest --cov={self.source} --cov-report=term-missing -q",
            cwd=cwd,
        )
        
        # Parse coverage from output
        lines = stdout.split("\n")
        coverage_line = [line for line in lines if "TOTAL" in line]
        
        if coverage_line:
            try:
                parts = coverage_line[0].split()
                coverage_percent = float(parts[-1].replace("%", ""))
                score = max(0.0, coverage_percent / 100)
                
                return ScorerResult(
                    name=self.name,
                    score=score,
                    message=f"{coverage_percent:.1f}% coverage",
                    details={"coverage_percent": str(coverage_percent)},
                )
            except (ValueError, IndexError):
                pass
        
        # Could not parse coverage
        if return_code != 0:
            return ScorerResult(
                name=self.name,
                score=0.0,
                message="Tests failed (expected for incomplete implementations)",
                details={"status": "tests_failed"},
            )
        
        return ScorerResult(
            name=self.name,
            score=0.0,
            message="No coverage data available",
            details={"status": "no_coverage"},
        )
