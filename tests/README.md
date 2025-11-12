 To run multiple or all tests in the /tests/ directory:

  Run ALL tests:
  source venv/bin/activate && python -m pytest tests/

  Run all tests with verbose output:
  source venv/bin/activate && python -m pytest tests/ -v

  Run all tests and show print statements:
  source venv/bin/activate && python -m pytest tests/ -v -s

  Run specific multiple tests:
  source venv/bin/activate && python -m pytest tests/test_geometry.py
  tests/test_time.py -v

  Run tests matching a pattern:
  # Run all tests with "geometry" in the filename
  source venv/bin/activate && python -m pytest tests/ -k geometry -v

  # Run all tests with "time" or "space" in the filename
  source venv/bin/activate && python -m pytest tests/ -k "time or space" -v

  Run tests and stop at first failure:
  source venv/bin/activate && python -m pytest tests/ -v -x

  Run tests in parallel (faster, if you have pytest-xdist installed):
  source venv/bin/activate && python -m pytest tests/ -v -n auto

  The most common command you'll use is probably:
  source venv/bin/activate && python -m pytest tests/ -v

  This will discover and run all test files in the tests directory that match the
  pattern test_*.py.