"""
Git practices scorer - evaluates Git usage and best practices.
"""

import subprocess
from pathlib import Path
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


class GitPracticesScorer(Scorer):
    """Scores Git best practices and usage."""
    
    name = "git_practices"
    description = "Git workflow and best practices"
    
    def __init__(self, weight: float = 0.1) -> None:
        self.weight = weight
    
    def evaluate(self, cwd: str = ".") -> ScorerResult:
        git_path = Path(cwd) / ".git"
        if not git_path.exists():
            return ScorerResult(
                name=self.name,
                score=0.0,
                message="Not a git repository",
            )
        
        scores: list[float] = []
        details: dict[str, str] = {}
        
        # Check 1: Commit history exists
        return_code, stdout, _ = run_command("git log --oneline -n 10", cwd=cwd)
        commits = [line for line in stdout.split("\n") if line.strip()]
        if len(commits) >= 5:
            scores.append(1.0)
            details["commits"] = f"{len(commits)}+ commits"
        elif len(commits) >= 1:
            scores.append(0.5)
            details["commits"] = f"{len(commits)} commits"
        else:
            scores.append(0.0)
            details["commits"] = "No commits"
        
        # Check 2: Commit message quality (not just "fix" or "update")
        return_code, stdout, _ = run_command(
            "git log --oneline -n 5 --format='%s'", cwd=cwd
        )
        messages = [line.strip() for line in stdout.split("\n") if line.strip()]
        good_messages = [
            msg for msg in messages 
            if len(msg) > 10 and msg.lower() not in ["fix", "update", "changes"]
        ]
        msg_quality = len(good_messages) / max(1, len(messages))
        scores.append(msg_quality)
        details["message_quality"] = f"{len(good_messages)}/{len(messages)} good messages"
        
        # Check 3: Branching (any branches besides main)
        return_code, stdout, _ = run_command("git branch -a", cwd=cwd)
        branches = [line.strip() for line in stdout.split("\n") if line.strip()]
        if len(branches) > 2:  # main + origin/main = 2
            scores.append(1.0)
            details["branches"] = f"{len(branches)} branches"
        elif len(branches) > 1:
            scores.append(0.7)
            details["branches"] = f"{len(branches)} branches"
        else:
            scores.append(0.3)
            details["branches"] = "Single branch"
        
        # Check 4: .gitignore exists and is non-empty
        gitignore = Path(cwd) / ".gitignore"
        if gitignore.exists() and gitignore.stat().st_size > 50:
            scores.append(1.0)
            details["gitignore"] = "Present and configured"
        elif gitignore.exists():
            scores.append(0.5)
            details["gitignore"] = "Present but minimal"
        else:
            scores.append(0.0)
            details["gitignore"] = "Missing"
        
        overall = sum(scores) / len(scores) if scores else 0.0
        
        if overall >= 0.8:
            message = "Excellent Git practices"
        elif overall >= 0.6:
            message = "Good Git practices"
        elif overall >= 0.4:
            message = "Basic Git usage"
        else:
            message = "Needs improvement"
        
        return ScorerResult(
            name=self.name,
            score=overall,
            message=message,
            details=details,
        )
