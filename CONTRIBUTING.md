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
   - `test/hypothesis-name` for new research tests
   - `experiment/experiment-name` for application demonstrations
   - `fix/issue-description` for bug fixes

2. Follow the project's commenting standards (see `COMMENTING_STANDARD.md`)

3. New theoretical claims should be validated through tests in the `tests/` directory. Practical applications demonstrating validated properties belong in `experiments/`

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

**Testing**: All contributions must pass the automated test suite. Add tests for theoretical claims.

**Experiments**: Demonstrations should illustrate practical applications of validated engine properties. Experiments demonstrate what can be built using the engine, tests validate the engine's fundamental properties.

**Core Engine**: Modifications to `engine/distinction.py` require rigorous justification and validation.

**Code Standards**: Follow commenting standards defined in `COMMENTING_STANDARD.md`. Use professional, concise docstrings and output text.

**Testing Standards**: Follow falsification methodology defined in `TESTING_STANDARD.md`. Design tests to attack hypotheses, not validate them.

**Scope**: Keep pull requests focused on a single test, experiment, or fix.

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

## Writing Experiments

Experiments demonstrate practical applications built on validated engine properties. Use `experiments/translation_demo.py` as a reference. Experiments should:

- Demonstrate a concrete application of engine properties validated by tests
- Follow the same commenting standards (see `COMMENTING_STANDARD.md`)
- Use professional, concise output without emojis or dramatic formatting
- Include module-level docstrings explaining what property is being demonstrated
- Provide clear, matter-of-fact result reporting
- Be executable standalone with `python experiments/experiment_name.py`

Experiments differ from tests:
- **Tests** falsify theoretical claims about the engine itself
- **Experiments** demonstrate what can be built using validated engine properties

## Running Tests

Run all tests:
```bash
python -m pytest tests/ -v
```

Run specific test:
```bash
python -m pytest tests/test_geometry.py -v
```