# GenAI Skills Assessment

[![CI Pipeline](https://github.com/NayanChheda/genai-skills-assessment/actions/workflows/ci.yml/badge.svg)](https://github.com/NayanChheda/genai-skills-assessment/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An open-source assessment platform to evaluate candidates on **Python**, **Git**, and **Generative AI** skills.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/NayanChheda/genai-skills-assessment.git
cd genai-skills-assessment
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run checks
pytest -v && python automated_scoring.py
```

## Assessment Areas

| Level | Focus | Folder |
|-------|-------|--------|
| Basic | Python fundamentals, Git basics | `challenges/level_1_basic/` |
| Intermediate | RAG pipelines, prompts, vector DBs | `challenges/level_2_intermediate/` |

## Project Structure

```
├── challenges/         # Assessment challenges by level
├── src/               # Core library code
│   ├── basics/        # Python utility functions
│   └── scoring/       # Modular scoring engine
├── tests/             # Centralized test suite
├── docker/            # Container support
├── docs/              # Documentation
└── automated_scoring.py  # CLI for running assessments
```

## For Candidates

See **[Candidate Guide](docs/CANDIDATE_GUIDE.md)** for setup and workflow.

## For Administrators

### Run Assessment Scoring

```bash
# Local
python automated_scoring.py

# Docker
docker compose -f docker/docker-compose.yml run scoring
```

### GitHub Actions

- **CI Pipeline**: Runs on every push/PR (lint, test, score)
- **Scoring Workflow**: Manual trigger for candidate assessment

## Development

```bash
# Format
black src/ challenges/

# Lint
flake8 src/ challenges/

# Type check
mypy src/ --ignore-missing-imports

# Test
pytest --cov=src -v
```

## Documentation

- [Candidate Guide](docs/CANDIDATE_GUIDE.md) - Getting started for candidates
- [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) - Project roadmap
- [Contributing](CONTRIBUTING.md) - How to contribute

## License

MIT License - See [LICENSE](LICENSE) for details.
