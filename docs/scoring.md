# docs/SCORING.md

# docs/SCORING.md (add this section)

## Assessment Repository Context

This scoring system is designed for assessment repositories where:

1. **Test files are provided** but implementation is missing
2. **0% coverage is expected** initially
3. **Candidates must implement** the solutions

### Scoring Adjustments for Assessment Mode

- **Coverage weight reduced**: From 30% to 10% of total score
- **Code style weight increased**: From 20% to 30%  
- **Type checking weight increased**: From 20% to 30%
- **Passing threshold lowered**: From 70% to 60%

### For Candidates

Your goal is to:
1. Implement the missing functionality in the `src/` directory
2. Maintain high code quality standards
3. Achieve high test coverage through your implementations
4. Follow Git best practices

The scoring will become stricter as you add implementations.

# Automated Scoring System

## Overview

The automated scoring system evaluates code quality across multiple dimensions:

1. **Test Coverage (30%)**: Measures how much of the code is covered by tests
2. **Code Style (20%)**: Adherence to PEP8 and flake8 standards
3. **Type Checking (20%)**: Proper use of type annotations
4. **Formatting (20%)**: Consistent code formatting with Black
5. **Git Practices (10%)**: Proper use of version control

## Scoring Details

### Test Coverage
- Perfect score: 100% coverage
- Minimum requirement: 70% coverage
- Measured using pytest-cov

### Code Style
- Perfect score: No flake8 violations
- Each violation reduces score by 1% (up to 100 violations)

### Type Checking
- Perfect score: No mypy errors
- Each error reduces score by 2% (up to 50 errors)

### Code Formatting
- Perfect score: All files properly formatted with Black
- Each unformatted file reduces score by 10% (up to 10 files)

### Git Practices
- Evaluates commit message quality and branch management
- Based on analysis of recent commit history

## Running the Scoring System

```bash
# Run the automated scoring
python automated_scoring.py

# View results
cat scoring_results.json