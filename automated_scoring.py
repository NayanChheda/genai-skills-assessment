# automated_scoring.py
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple, TypedDict


def run_command(cmd: str, cwd: str = ".") -> Tuple[int, str, str]:
    """Run a command and return result."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=cwd
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


# automated_scoring.py (update calculate_coverage_score function)
def calculate_coverage_score() -> Tuple[float, str]:
    """Calculate test coverage score - handle pytest failures gracefully."""
    try:
        return_code, stdout, stderr = run_command(
            "pytest --cov=src --cov-report=term-missing"
        )

        # Even if pytest fails, try to parse coverage from the output
        lines = stdout.split("\n")
        coverage_line = [line for line in lines if "TOTAL" in line]

        if coverage_line:
            parts = coverage_line[0].split()
            try:
                coverage_percent = float(parts[-1].replace("%", ""))
                normalized_score = max(0.0, coverage_percent / 100)
                return normalized_score, f"Coverage: {coverage_percent}%"
            except (ValueError, IndexError):
                pass

        # If we can't parse coverage, return 0 with appropriate message
        if return_code != 0:
            return 0.0, "Tests failed (expected - implementations missing)"
        else:
            return 0.0, "No coverage data available"

    except Exception:
        return 0.0, "Coverage check failed"


def calculate_style_score() -> Tuple[float, str]:
    """Calculate code style score."""
    return_code, stdout, stderr = run_command("flake8 src/ --count --max-complexity=10")

    if return_code == 0:
        return 1.0, "No style issues"

    # Count violations
    violation_count = int(stdout.strip()) if stdout.strip().isdigit() else 10
    score = max(0.0, 1 - (violation_count / 100))
    return score, f"Style violations: {violation_count}"


def calculate_type_check_score() -> Tuple[float, str]:
    """Calculate type checking score."""
    return_code, stdout, stderr = run_command("mypy src/")

    if return_code == 0:
        return 1.0, "No type issues"

    # Count type errors from output
    error_count = len([line for line in stdout.split("\n") if "error:" in line])
    score = max(0.0, 1 - (error_count / 50))
    return score, f"Type errors: {error_count}"


def calculate_formatting_score() -> Tuple[float, str]:
    """Calculate code formatting score."""
    return_code, stdout, stderr = run_command("black --check src/")

    if return_code == 0:
        return 1.0, "Perfect formatting"

    # Count files that need reformatting
    files_count = len(
        [line for line in stdout.split("\n") if "would be reformatted" in line]
    )
    score = max(0.0, 1 - (files_count / 10))
    return score, f"Files needing formatting: {files_count}"


def calculate_git_score() -> Tuple[float, str]:
    """Calculate Git practices score using the enhanced validation."""
    if not Path(".git").exists():
        return 0.0, "Not a git repository"

    try:
        # Run the comprehensive Git assessment
        return_code, stdout, stderr = run_command(
            "python challenges/level_1_basic/validate_git_tasks.py"
        )

        if return_code == 0:
            # Git assessment passed with good practices
            return 0.9, "Excellent Git practices"
        elif return_code == 1:
            # Git assessment failed or needs improvement
            # Let's get more detailed info by running specific checks

            # Check if at least we have some commits
            return_code, stdout, stderr = run_command("git log --oneline -n 5")
            commits = [line for line in stdout.split("\n") if line.strip()]

            if commits:
                # Basic Git repository with some activity
                return 0.6, "Basic Git practices (needs improvement)"
            else:
                return 0.3, "Minimal Git usage"
        else:
            return 0.5, "Git repository exists (full assessment unavailable)"

    except Exception:
        # Fallback: check if it's a Git repo at all
        return_code, stdout, stderr = run_command("git status")
        if return_code == 0:
            return 0.7, "Git repository detected (basic assessment)"
        else:
            return 0.0, "Not a valid Git repository"


# Define type for scoring results
class ScoreResults(TypedDict):
    """Type definition for scoring results."""

    timestamp: str
    context: str
    note: str
    scores: dict[str, float]
    details: dict[str, str]


def main() -> None:
    """Main scoring function - updated for assessment context."""
    print("Running automated code assessment...")
    print("Note: Low coverage is expected in assessment repositories")
    print("=" * 60)

    # Calculate various scores
    coverage_score, coverage_msg = calculate_coverage_score()
    style_score, style_msg = calculate_style_score()
    type_score, type_msg = calculate_type_check_score()
    format_score, format_msg = calculate_formatting_score()
    git_score, git_msg = calculate_git_score()

    # Adjusted weights for assessment context
    # Less weight on coverage since implementations are missing
    final_score = (
        coverage_score * 0.1
        + style_score * 0.3
        + type_score * 0.3
        + format_score * 0.2
        + git_score * 0.1
    )

    # Prepare results with proper typing
    results: ScoreResults = {
        "timestamp": datetime.now().isoformat(),
        "context": "assessment_repository",
        "note": "Low coverage expected - candidates must implement solutions",
        "scores": {
            "coverage": round(coverage_score * 100, 2),
            "code_style": round(style_score * 100, 2),
            "type_checking": round(type_score * 100, 2),
            "formatting": round(format_score * 100, 2),
            "git_practices": round(git_score * 100, 2),
            "overall": round(final_score * 100, 2),
        },
        "details": {
            "coverage": coverage_msg,
            "code_style": style_msg,
            "type_checking": type_msg,
            "formatting": format_msg,
            "git_practices": git_msg,
        },
    }

    # Save results to file
    with open("scoring_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Print results
    print("\n" + "=" * 60)
    print("ASSESSMENT REPOSITORY - CODE QUALITY RESULTS")
    print("=" * 60)

    # Access the scores dictionary directly
    for category, score in results["scores"].items():
        print(f"{category.replace('_', ' ').title():<20}: {score}%")

    print("=" * 60)
    print(f"Overall Score: {results['scores']['overall']}%")

    # More lenient threshold for assessment templates
    if final_score < 0.6:
        print("⚠️  Score below recommended threshold (60%) - review recommended")
        sys.exit(1)
    else:
        print("✅ Repository structure meets assessment requirements")
        sys.exit(0)


if __name__ == "__main__":
    main()
