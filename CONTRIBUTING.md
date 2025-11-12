# Contributing to Distinction Engine

## Development Workflow

### Setup

1. Fork and clone the repository
2. Create a virtual environment and install dependencies:

```bash
python3 setup_env.py
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

### Making Changes

1. Create a new branch for your work:
   - `feature/feature-name` for new functionality
   - `test/hypothesis-name` for new tests
   - `fix/issue-description` for bug fixes

2. Follow the project's commenting standards (see `COMMENTING_STANDARD.md`)

3. Add tests for any new functionality in the `tests/` directory

### Before Pushing

Run the status check script to ensure all tests pass:

```bash
python tools/status_check.py
```

This runs the same checks used by GitHub Actions for pull request validation.

### Pull Requests

1. Push your branch to your fork
2. Open a pull request against the main repository
3. Ensure all GitHub Actions checks pass
4. Wait for review

## Guidelines

**Testing**: All contributions must pass the automated test suite. Add tests for new functionality.

**Core Engine**: Modifications to `engine/distinction.py` require rigorous justification and validation.

**Code Standards**: Follow commenting standards defined in `COMMENTING_STANDARD.md`. Use professional, concise docstrings and output text.

**Testing Standards**: Follow falsification methodology defined in `TESTING_STANDARD.md`. Design tests to attack hypotheses, not validate them.

**Scope**: Keep pull requests focused on a single feature or fix.

## Writing New Tests

When adding new research tests, use `tests/test_example.py` as a template and follow `TESTING_STANDARD.md` for methodology. The example demonstrates:

- Professional module and method docstrings
- Clear falsification targets
- Standard helper methods (`_build_graph`, `_evolve_substrate`)
- Concise output text without emojis or informal language
- Proper assertion messages starting with "FALSIFIED:"

Structure your test to include:
1. Clear hypothesis statement
2. Specific falsification condition
3. Measurement methodology
4. Professional output reporting

## Running Tests

Run all tests:
```bash
python -m pytest tests/ -v
```

Run specific test:
```bash
python -m pytest tests/test_geometry.py -v
```