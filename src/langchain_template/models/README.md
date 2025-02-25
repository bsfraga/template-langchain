# `models` Directory

This directory contains the models, schemas, and integrations with LLMs (Large Language Models) used in the LangChain Template project.

## Directory Structure

| File | Description |
|------|-------------|
| `__init__.py` | Package initialization file (empty) |
| `base.py` | Base class implementation for LLM integration |
| `schemas.py` | Pydantic schema definitions for response validation and structuring |

## Main Components

### LLMManager (base.py)

The `LLMManager` class is the central component for interacting with LLMs. It:

- Is a generic class that accepts a response model type (`T`)
- Uses the `instructor` package to patch the OpenAI client, enabling structured validation
- Manages communication with the LLM and processes responses
- Implements error handling and logging

Usage example:

```python
from langchain_template.models.base import LLMManager
from langchain_template.models.schemas import TextAnalysis

# Initialize the manager with a specific response model
manager = LLMManager[TextAnalysis](TextAnalysis)

# Generate a structured response
result = manager.generate_response("Analyze the following text: ...")
```

### Schemas (schemas.py)

Defines Pydantic models to structure and validate LLM responses:

1. `TextAnalysis`: Schema for text analysis with fields:
   - `sentiment`: Text sentiment (string)
   - `confidence`: Confidence score (float between 0 and 1)
   - `key_points`: List of key points from the text
   - `summary`: Optional text summary

2. `ContentGeneration`: Schema for content generation with fields:
   - `title`: Generated content title
   - `content`: Generated content body
   - `tags`: List of related tags
   - `metadata`: Additional metadata (dictionary)

Both schemas implement validators that log debug information during validation.

## Extension

To add new response models:

1. Define a new schema in `schemas.py`:
   ```python
   class NewResponseType(BaseModel):
       field1: str
       field2: int
       # ...
   ```

2. Use the new schema with the `LLMManager`:
   ```python
   manager = LLMManager[NewResponseType](NewResponseType)
   result = manager.generate_response("Your prompt here")
   ```

## Instructor Integration

The project uses the `instructor` package to ensure that LLM responses are correctly structured and validated according to the defined Pydantic schemas. This provides:

- Consistent and typed responses
- Automatic validation
- Better development experience with autocomplete and type checking 