import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

import structlog

def configure_logging(
    log_level: str = "INFO", 
    log_file: Optional[str] = None
) -> structlog.BoundLogger:
    """
    Configura logging estruturado com suporte a console e arquivo.
    
    Args:
        log_level (str): Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (Optional[str]): Caminho para arquivo de log
    
    Returns:
        structlog.BoundLogger: Logger configurado
    """
    # Configuração do logger base
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper())
    )

    # Configuração do structlog
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ]

    # Configuração de handlers
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        handlers.append(file_handler)

    # Configuração final
    structlog.configure(
        processors=shared_processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()

# Logger global
logger = configure_logging()

# Convenience functions
def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)

def set_log_level(level: int) -> None:
    """Set the log level for the default logger."""
    logger.setLevel(level) 