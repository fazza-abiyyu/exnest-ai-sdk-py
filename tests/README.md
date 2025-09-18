# ExnestAI Python SDK Tests

This directory contains the test suite for the ExnestAI Python SDK.

## Running Tests

To run the tests, use the following command from the project root:

```bash
python -m pytest tests/ -v
```

## Test Structure

- `test_exnestai.py` - Main test file with tests for both the wrapper and client classes
- `conftest.py` - pytest configuration file

## Dependencies

The test suite requires the following dependencies:

- pytest
- pytest-asyncio

These are included in the project's [requirements.txt](file:///Users/fazza_abiyyu/Documents/Projects/Express/exnest-ai-sdk-py/requirements.txt) file.