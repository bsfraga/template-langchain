# LangChain Template Project

A modular template for building LLM-powered applications using LangChain, Instructor, and Pydantic. This template provides a solid foundation for developing AI applications with structured outputs and type safety.

## Features

- 🚀 Modern Python project structure with src layout
- 🔧 Configuration management using Pydantic and environment variables
- 🤖 LLM integration with LangChain and OpenAI
- 📝 Structured outputs using Instructor and Pydantic models
- 🌐 FastAPI implementation for REST API
- 💻 CLI interface using Typer
- ✨ Type hints and documentation throughout
- 🧪 Example test suite setup

## Project Structure

```
src/langchain_template/
├── __init__.py           # Package initialization
├── config.py            # Configuration management
├── api.py              # FastAPI implementation
├── cli.py             # Command-line interface
├── models/
│   ├── __init__.py
│   ├── base.py        # Base LLM integration
│   └── schemas.py     # Response schemas
└── tests/
    ├── __init__.py
    ├── test_api.py
    └── test_models.py
```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/langchain-template.git
   cd langchain-template
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Copy the example environment file and configure your settings:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key and other settings.

## Usage

### API Server

Start the FastAPI server:

```bash
uvicorn langchain_template.api:app --reload
```

The API will be available at `http://localhost:8000` with interactive documentation at `/docs`.

Example API requests:

```bash
# Analyze text
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a sample text for analysis"}'

# Generate content
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a blog post about AI", "context": {"tone": "professional"}}'
```

### Command Line Interface

The package provides a CLI for direct interaction:

```bash
# Analyze text
langchain-template analyze "This is a sample text for analysis"

# Generate content with context
langchain-template generate "Write a blog post about AI" -c context.json
```

## Development

### Running Tests

```bash
pytest
```

### Code Quality

The project uses several tools to maintain code quality:

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Type checking
mypy src

# Linting
ruff src tests
```

## Customization

### Adding New Models

1. Define your response schema in `models/schemas.py`:
   ```python
   class YourSchema(BaseModel):
       field1: str
       field2: int
   ```

2. Use the schema with the LLMManager:
   ```python
   manager = LLMManager[YourSchema](YourSchema)
   result = await manager.generate_response("Your prompt")
   ```

### Environment Variables

Key configuration options in `.env`:

- `OPENAI_API_KEY`: Your OpenAI API key
- `MODEL_NAME`: LLM model to use (default: gpt-3.5-turbo)
- `TEMPERATURE`: Model temperature (0-1)
- `MAX_TOKENS`: Maximum tokens for responses
- `DEBUG`: Enable debug mode
- `LOG_LEVEL`: Logging level

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 