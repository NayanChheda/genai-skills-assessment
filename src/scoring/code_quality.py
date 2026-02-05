"""
Code quality scorers - formatting, linting, type checking.
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


class BlackFormattingScorer(Scorer):
    """Scores code formatting using Black."""
    
    name = "formatting"
    description = "Code formatting with Black"
    
    def __init__(self, weight: float = 0.2, paths: str = "src/") -> None:
        self.weight = weight
        self.paths = paths
    
    def evaluate(self, cwd: str = ".") -> ScorerResult:
        return_code, stdout, stderr = run_command(
            f"black --check {self.paths}", cwd=cwd
        )
        
        if return_code == 0:
            return ScorerResult(
                name=self.name,
                score=1.0,
                message="Perfect formatting",
            )
        
        # Count files needing reformatting
        lines = stdout.split("\n") + stderr.split("\n")
        files_count = len([
            line for line in lines 
            if "would reformat" in line.lower()
        ])
        
        if files_count == 0:
            files_count = 1  # At least one issue if return_code != 0
        
        score = max(0.0, 1 - (files_count / 10))
        return ScorerResult(
            name=self.name,
            score=score,
            message=f"{files_count} file(s) need formatting",
            details={"files_to_format": str(files_count)},
        )


class Flake8LintScorer(Scorer):
    """Scores code quality using flake8 linting."""
    
    name = "linting"
    description = "Code style with flake8"
    
    def __init__(
        self, 
        weight: float = 0.3, 
        paths: str = "src/",
        max_complexity: int = 10,
    ) -> None:
        self.weight = weight
        self.paths = paths
        self.max_complexity = max_complexity
    
    def evaluate(self, cwd: str = ".") -> ScorerResult:
        return_code, stdout, stderr = run_command(
            f"flake8 {self.paths} --count --max-complexity={self.max_complexity}",
            cwd=cwd,
        )
        
        if return_code == 0:
            return ScorerResult(
                name=self.name,
                score=1.0,
                message="No style issues",
            )
        
        # Last line of flake8 output is the count
        lines = stdout.strip().split("\n")
        try:
            violation_count = int(lines[-1]) if lines[-1].isdigit() else 10
        except (ValueError, IndexError):
            violation_count = 10
        
        score = max(0.0, 1 - (violation_count / 100))
        return ScorerResult(
            name=self.name,
            score=score,
            message=f"{violation_count} style violation(s)",
            details={"violation_count": str(violation_count)},
        )


class MypyTypeScorer(Scorer):
    """Scores type checking using mypy."""
    
    name = "type_checking"
    description = "Type safety with mypy"
    
    def __init__(self, weight: float = 0.3, paths: str = "src/") -> None:
        self.weight = weight
        self.paths = paths
    
    def evaluate(self, cwd: str = ".") -> ScorerResult:
        return_code, stdout, stderr = run_command(
            f"mypy {self.paths} --ignore-missing-imports", cwd=cwd
        )
        
        if return_code == 0:
            return ScorerResult(
                name=self.name,
                score=1.0,
                message="No type issues",
            )
        
        # Count error lines
        error_count = len([
            line for line in stdout.split("\n") 
            if "error:" in line
        ])
        
        if error_count == 0:
            error_count = 1
        
        score = max(0.0, 1 - (error_count / 50))
        return ScorerResult(
            name=self.name,
            score=score,
            message=f"{error_count} type error(s)",
            details={"error_count": str(error_count)},
        )
