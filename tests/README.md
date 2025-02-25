# `tests` Directory

This directory contains the automated tests for the LangChain Template project, using the pytest framework.

## Directory Structure

| File | Description |
|------|-------------|
| `__init__.py` | Test package initialization file (empty) |
| `test_api.py` | Tests for the REST API endpoints |
| `test_models.py` | Tests for models and schemas |

## Main Components

### API Tests (test_api.py)

Contains tests for the REST API endpoints implemented in `langchain_template.api`:

- `test_analyze_text`: Tests the `/analyze` endpoint for text analysis
- `test_generate_content`: Tests the `/generate` endpoint for content generation
- `test_analyze_text_error`: Tests error handling in the `/analyze` endpoint

The tests use the FastAPI test client and mock the `LLMManager` to isolate API tests from LLM integration logic.

### Model Tests (test_models.py)

Contains tests for the schemas defined in `langchain_template.models.schemas`:

- `test_text_analysis_schema`: Tests the validation of the `TextAnalysis` schema
- `test_content_generation_schema`: Tests the validation of the `ContentGeneration` schema

The tests verify both valid and invalid cases to ensure that schema validation works correctly.

## Running Tests

To run all tests:

```bash
pytest
```

To run specific tests:

```bash
# Run only API tests
pytest tests/test_api.py

# Run only model tests
pytest tests/test_models.py

# Run a specific test
pytest tests/test_api.py::test_analyze_text
```

To run tests with coverage report:

```bash
pytest --cov=langchain_template
```

## Adding New Tests

When adding new features to the project, follow these guidelines for creating tests:

1. Create unit tests for each component
2. Use fixtures to share setup between tests
3. Mock external dependencies (like LLMs) to isolate tests
4. Test both success and error cases
5. Keep tests independent from each other

## Best Practices

- Keep tests fast and independent
- Use descriptive names for test functions
- Document the purpose of each test
- Avoid external dependencies in tests
- Maintain high code coverage 