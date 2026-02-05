# Candidate Guide

Welcome to the GenAI Skills Assessment! This guide will help you get started.

## Quick Start

### 1. Fork & Clone

```bash
# Fork this repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/genai-skills-assessment.git
cd genai-skills-assessment
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -e ".[dev]"
```

### 3. Verify Setup

```bash
# Run quality checks
black --check src/ challenges/
flake8 src/ challenges/
mypy src/ --ignore-missing-imports
pytest -v
```

## Assessment Structure

```
challenges/
├── level_1_basic/          # Python fundamentals
│   ├── git_basics.md       # Git tasks
│   ├── python_fundamentals.md
│   └── tests/              # Tests for your implementations
└── level_2_intermediate/   # GenAI challenges
    └── rag_chatbot/        # RAG pipeline implementation
```

## Workflow

1. **Read the challenge** in `challenges/level_X/`
2. **Implement** in `src/` following the instructions
3. **Run tests** to validate: `pytest -v`
4. **Check quality**: `python automated_scoring.py`
5. **Commit** with descriptive messages
6. **Push** and create a PR

## Scoring Criteria

| Category | Weight | Tools |
|----------|--------|-------|
| Code Style | 30% | flake8 |
| Type Safety | 30% | mypy |
| Formatting | 20% | black |
| Test Coverage | 10% | pytest-cov |
| Git Practices | 10% | commit quality |

## Commands Reference

```bash
# Format code
black src/ challenges/

# Check linting
flake8 src/ challenges/

# Type check
mypy src/ --ignore-missing-imports

# Run tests with coverage
pytest --cov=src --cov-report=term-missing

# Run automated scoring
python automated_scoring.py
```

## Docker (Optional)

```bash
# Run tests in container
docker compose -f docker/docker-compose.yml run assessment

# Run scoring
docker compose -f docker/docker-compose.yml run scoring
```

## Tips

- **Commit often** with meaningful messages
- **Run tests** before pushing
- **Read error messages** carefully
- **Ask questions** if stuck

Good luck! 🚀
