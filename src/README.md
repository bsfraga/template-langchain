# `src` Directory

This directory contains the main source code of the LangChain Template project. It follows the modern Python project structure with `src` layout, which offers several advantages:

- Avoids import conflicts during development
- Facilitates package distribution
- Improves code organization

## Contents

The `src` directory contains the following:

| Item | Type | Description |
|------|------|-------------|
| `langchain_template/` | Directory | Main project package containing all business logic, APIs, and models |

## Package Structure

The `langchain_template` package is organized in a modular way, following Python development best practices. It contains modules for configuration, API, CLI, models, and utilities.

## Development

When developing in this directory, follow these practices:

1. Maintain a modular and well-organized structure
2. Add docstrings to all modules, classes, and functions
3. Use static typing to improve code safety
4. Follow Python naming conventions (snake_case for functions and variables, PascalCase for classes)

## Imports

To import modules from this package during development, use:

```python
from langchain_template import [module]
```

Or for specific imports:

```python
from langchain_template.models.base import LLMManager
``` 