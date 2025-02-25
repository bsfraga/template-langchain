# `langchain_template` Package

This is the main package of the LangChain Template project, which implements a modular application for interaction with LLMs (Large Language Models) using LangChain, Instructor, and Pydantic.

## Package Structure

| File/Directory | Type | Description |
|----------------|------|-------------|
| `__init__.py` | File | Package initialization, contains version and metadata |
| `api.py` | File | REST API implementation using FastAPI |
| `cli.py` | File | Command-line interface using Typer |
| `config.py` | File | Configuration management using Pydantic |
| `logger.py` | File | Logging configuration and utilities |
| `models/` | Directory | Subpackage containing models, schemas, and LLM integrations |

## Main Components

### API (api.py)

Implements a REST API using FastAPI with endpoints for:
- Text analysis (`/analyze`)
- Content generation (`/generate`)

The API uses the models defined in `models/schemas.py` for validation and response structuring.

### CLI (cli.py)

Provides a command-line interface using Typer with commands for:
- Text analysis (`analyze`)
- Content generation (`generate`)

The CLI uses the same models and logic as the API, but with a different interface.

### Configuration (config.py)

Defines the `Settings` class using Pydantic to manage application configurations, including:
- LLM configurations (API key, model, temperature)
- Application configurations (debug, log level)
- API configurations (host, port, workers)
- Database configurations (optional)
- Custom model configurations (max tokens, response format)

Configurations are loaded from environment variables and/or a `.env` file.

### Logger (logger.py)

Configures the application's logging system with:
- Console and file logging
- Log file rotation
- Custom formatting
- Configurable log levels

## Usage

To use this package in other modules:

```python
# Import configurations
from langchain_template.config import get_settings

# Use the LLM manager
from langchain_template.models.base import LLMManager
from langchain_template.models.schemas import TextAnalysis

# Initialize and use the LLM
manager = LLMManager[TextAnalysis](TextAnalysis)
result = manager.generate_response("Your prompt here")
``` 