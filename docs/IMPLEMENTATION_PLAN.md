# GenAI Skills Assessment Project Documentation

## Project Overview

**Objective**  
Build an open-source repository template for assessing candidates and groups on three critical skills:  
- Git hands-on collaboration (branching, merging, conflict resolution, advanced workflows)  
- Python coding standards (code style, testing, documentation, refactoring)  
- Generative AI (GenAI) development techniques (RAG pipelines, prompt engineering, fine-tuning, multi-agent systems, optimization, and production troubleshooting)

The platform will support individual and group assessments, real-time competitions with natural git conflicts, and community-driven challenge contributions. All development should use free and open source tools only.

***

## Implementation Plan (Step-by-Step)

### **Phase 1: Scaffold Core Repository (Weeks 1–2)**
**Goal:** Lay out the foundational structure and configurations

1. Create a new GitHub repository (mark as template for cloning)
2. Scaffold directory structure:
   ```
   genai-skills-assessment/
   ├── challenges/
   │   └── level_1_basic/
   │       ├── git_basics.md
   │       ├── python_fundamentals.md
   │       └── tests/
   ├── docs/
   │   └── README.md
   ├── .github/
   │   ├── workflows/
   │   │   └── ci.yml
   │   └── ISSUE_TEMPLATE/
   ├── requirements.txt
   ├── .env.example
   └── README.md
   ```
3. Write clear documentation about the project’s purpose, how to use the template, and next steps.  
4. Add basic challenge files (`git_basics.md`, `python_fundamentals.md`) and blank unit tests.  
5. Add free Python tooling to `requirements.txt`: `black`, `flake8`, `mypy`, `pytest`  
6. Set up a free CI pipeline using GitHub Actions (`ci.yml`) to run linters, formatters, type checking, and tests on pushes/PRs.  
7. Add a CONTRIBUTING.md guide for community/participant involvement.

***

### **Phase 2: Automated Scoring and Infrastructure (Weeks 3–4)**
**Goal:** Ensure every submission is automatically validated for code style, correctness, and coverage.

1. Enhance the CI pipeline:
   - Add pytest coverage checks.
   - Fail PRs if style, formatting, typing, or coverage requirements are not met.
2. Develop `automated_scoring.py` script to generate code quality scores based on lint/test/coverage results.
3. Add functional pre-written tests for both Python and Git tasks (e.g., a script to check merge conflict resolution).
4. Add documentation for how scoring works and what candidates must do to achieve a perfect score.

***

### **Phase 3: Intermediate Challenge Scaffolding (Weeks 5–7)**
**Goal:** Create RAG, prompt engineering, and retrieval exercise stubs

1. Under `challenges/level_2_intermediate`:
   - Add folders for RAG chatbot, vector database integration, prompt templates, and retrieval logic (with partially completed code).
   - Include mock datasets/documents for GenAI exercises.
2. Document expected inputs/outputs and provide instructions.
3. Add baseline unit and integration tests for GenAI functions.

***

### **Phase 4: Advanced GenAI Challenge Scaffolding (Weeks 8–10)**
**Goal:** Build fine-tuning and multi-agent system pipelines

1. Under `challenges/level_3_advanced`:
   - Add PEFT/LoRA fine-tuning stub with sample data for training.
   - Create multi-agent orchestration skeleton code (retriever/summarizer agents, communication logic).
2. Set up more complex test scripts and documentation for usage and expected outputs.

***

### **Phase 5: Group Competition & Real-Time Features (Weeks 11–13)**
**Goal:** Support simultaneous candidate sessions with real Git conflict monitoring

1. Write `group_setup.py`: Initialize unique repos/branches per participant, randomize datasets/prompts for fairness.
2. Add `.github/workflows/conflict-monitor.yml` to log and score real-time git conflicts (merge, rebase, conflict resolution duration).
3. Document procedures for running group challenges, collecting scores, and monitoring fairness.

***

### **Phase 6: Anti-Cheat Enforcement & Fairness (Weeks 14–16)**
**Goal:** Protect integrity and credibility of assessments

1. Implement `plagiarism_detector.py` using open-source tools (e.g., OpenAI embeddings or SentenceTransformers).
2. Require `prompts.log` (commit log of all AI/copilot interactions for transparency).
3. Set branch protection rules in GitHub:
   - No force pushes to main/master
   - Require PR approvals
   - Check for large/suspicious diffs
4. Create randomized challenge parameters for each participant.
5. Write extra docs about anti-cheat mechanisms, enforcement policy, and expected ethical conduct.

***

### **Phase 7: Community Enablement & Public Launch (Weeks 17–18+)**
**Goal:** Open to contributions and ongoing improvement

1. Finalize and publish `CONTRIBUTING.md`, issue/pull request templates, and Discussion guidelines.
2. Use MkDocs or plain Markdown for project and technical documentation.
3. Publicize repo on social platforms, developer forums, and open source sites.
4. Organize online sprints or hackathons; invite feedback for continuous challenge improvement.
5. Monitor and approve community-contributed challenge templates with peer review.

***

## **Minor Details to Track**

- Always use free/open-source tools (GitHub, Cookiecutter, linters, test frameworks).
- Document every folder, file, and config in a dedicated `docs` section.
- For every new challenge, provide expected solution steps, input/output examples, and scoring breakdown.
- For each test/check, describe what it does and why it’s included (in docs and code comments).
- All changes/additions must go through proper PR review and CI checks.
- Keep project roadmap and progress tracking up to date in `docs/IMPLEMENTATION_PLAN.md`.

***

## Final Note

This documentation is stored at `docs/IMPLEMENTATION_PLAN.md` and referenced in the main README.
