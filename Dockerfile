# Stage 1: Build dependencies
FROM python:3.9-slim AS builder

WORKDIR /app

# Copy only the files needed for installing dependencies
COPY pyproject.toml .
COPY README.md .

# Install build dependencies and project dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    "langchain>=0.1.5" \
    "langchain-core>=0.1.15" \
    "langchain-community>=0.0.13" \
    "langchain-openai>=0.0.5" \
    "instructor>=0.4.5" \
    "pydantic>=2.5.3" \
    "pydantic-settings>=2.1.0" \
    "python-dotenv>=1.0.1" \
    "fastapi>=0.109.0" \
    "uvicorn>=0.27.0" \
    "typer>=0.9.0" \
    "eval-type-backport>=0.2.2"

# Stage 2: Runtime image
FROM python:3.9-slim

WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ /app/src/
COPY pyproject.toml .
COPY README.md .

# Create a directory for logs
RUN mkdir -p /app/logs && \
    chmod -R 755 /app/logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose the API port (default: 8000)
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "uvicorn", "src.langchain_template.api:app", "--host", "0.0.0.0", "--port", "8000"] 