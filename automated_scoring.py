import subprocess


def run_command(name: str, command: list[str], points: int) -> tuple[int, str]:
    """Run a command and return (score, output)."""
    result = subprocess.run(command, capture_output=True, text=True)
    success = result.returncode == 0
    earned = points if success else 0
    return earned, result.stdout + result.stderr


def main():
    # Scoring configuration
    commands = [
        ("black", ["python", "-m", "black", "--check", "."], 20),
        ("flake8", ["python", "-m", "flake8", "."], 20),
        ("mypy", ["python", "-m", "mypy", "."], 20),
        (
            "pytest+coverage",
            [
                "python",
                "-m",
                "pytest",
                "--maxfail=1",
                "--disable-warnings",
                "--cov=.",
                "--cov-fail-under=20",
                "-q",
            ],
            40,
        ),
    ]

    total_score = 0
    print("\n=== Automated Scoring Report ===")

    for name, cmd, pts in commands:
        score, output = run_command(name, cmd, pts)
        total_score += score
        print(f"{name}: {score} / {pts}")
        if score < pts:
            print(f"--- {name} output ---\n{output}\n")

    print(f"TOTAL SCORE: {total_score}/100")


if __name__ == "__main__":
    main()
