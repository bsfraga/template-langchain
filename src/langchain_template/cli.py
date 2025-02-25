"""Command-line interface for the LLM service."""

import json
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from .models.base import LLMManager
from .models.schemas import ContentGeneration, TextAnalysis
from .logger import get_logger

logger = get_logger(__name__)

app = typer.Typer(
    name="langchain-template",
    help="CLI for LLM-powered text analysis and generation",
)
console = Console()

logger.info("CLI application initialized")


def display_result(result: dict) -> None:
    """Display results in a formatted panel."""
    logger.debug(f"Displaying result: {result}")
    console.print(
        Panel(
            json.dumps(result, indent=2),
            title="LLM Response",
            border_style="blue",
        )
    )


@app.command()
def analyze(
    text: str = typer.Argument(..., help="Text to analyze"),
) -> None:
    """Analyze text using the LLM."""
    logger.info("Starting text analysis command")
    logger.debug(f"Input text: {text[:100]}...")  # Log first 100 chars
    
    try:
        logger.debug("Initializing LLM manager for analysis")
        manager = LLMManager[TextAnalysis](TextAnalysis)
        
        logger.info("Sending analysis request to LLM")
        result = manager.generate_response(
            f"Analyze the following text: {text}"
        )
        
        logger.info("Analysis completed successfully")
        logger.debug(f"Analysis result: {result}")
        display_result(result.model_dump())
        
    except Exception as e:
        logger.error(f"Error during text analysis: {str(e)}", exc_info=True)
        console.print(f"[red]Error: {str(e)}[/red]")


@app.command()
def generate(
    prompt: str = typer.Argument(..., help="Prompt for content generation"),
    context_file: Optional[str] = typer.Option(
        None,
        "--context",
        "-c",
        help="Path to JSON file with generation context",
    ),
) -> None:
    """Generate content using the LLM."""
    logger.info("Starting content generation command")
    logger.debug(f"Generation prompt: {prompt}")
    logger.debug(f"Context file: {context_file}")
    
    try:
        context = {}
        if context_file:
            logger.debug(f"Loading context from file: {context_file}")
            with open(context_file) as f:
                context = json.load(f)
            logger.debug(f"Loaded context: {context}")
        
        logger.debug("Initializing LLM manager for generation")
        manager = LLMManager[ContentGeneration](ContentGeneration)
        
        prompt_text = f"Generate content based on: {prompt}\nContext: {context}"
        logger.info("Sending generation request to LLM")
        result = manager.generate_response(prompt_text)
        
        logger.info("Content generation completed successfully")
        logger.debug(f"Generated content: {result}")
        display_result(result.model_dump())
        
    except Exception as e:
        logger.error(f"Error during content generation: {str(e)}", exc_info=True)
        console.print(f"[red]Error: {str(e)}[/red]")


if __name__ == "__main__":
    logger.debug("Running CLI application")
    app() 