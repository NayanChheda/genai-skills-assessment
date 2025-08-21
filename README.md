# GenAI Skills Assessment (Template)

An open-source template to assess candidates and groups on:
- **Git collaboration** (branching, merging, conflict resolution, workflows)
- **Python coding standards** (style, tests, docs, refactoring)
- **Generative AI** development (RAG, prompts, fine-tuning, multi-agent, optimization)

> This repo is designed as a **template**—fork/clone and adapt it to your needs. All tools are free & open-source.

## Quick Start

```bash
# 1) Create & activate a virtual environment
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

# 2) Install dev tools
pip install -r requirements.txt

# 3) Run quality checks
black --check .
flake8 .
mypy .
pytest -q
```

## Repository Structure

```
genai-skills-assessment/
├── challenges/
│   └── level_1_basic/
│       ├── git_basics.md
│       ├── python_fundamentals.md
│       └── tests/
├── docs/
│   ├── README.md
│   └── IMPLEMENTATION_PLAN.md
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       ├── feature_request.md
│       └── config.yml
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Docs

- Start here: `docs/README.md`
- Full roadmap/plan: `docs/IMPLEMENTATION_PLAN.md`

## License

Choose one that fits your org (e.g., MIT, Apache‑2.0). Add `LICENSE` later.
