import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional
import json
from datetime import datetime
from app.config.settings import settings


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    """
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = record.session_id

        return json.dumps(log_entry)


def setup_logging():
    """
    Set up comprehensive logging configuration for the application.
    """
    # Create formatters
    if settings.DEBUG:
        # Detailed formatter for development
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
        )
        json_formatter = JSONFormatter()
    else:
        # JSON formatter for production
        json_formatter = JSONFormatter()

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)

    # Remove default handlers to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if settings.DEBUG:
        console_handler.setFormatter(detailed_formatter)
    else:
        console_handler.setFormatter(json_formatter)
    console_handler.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    root_logger.addHandler(console_handler)

    # File handler for general logs
    if not settings.DEBUG:  # Only use file logging in production
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(json_formatter)
        file_handler.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)

        # Separate file handler for errors
        error_handler = RotatingFileHandler(
            'logs/error.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_handler.setFormatter(json_formatter)
        error_handler.setLevel(logging.ERROR)
        root_logger.addHandler(error_handler)

    # Set specific log levels for different loggers
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)  # Reduce access log noise
    logging.getLogger('sqlalchemy.engine').setLevel(
        logging.INFO if settings.DEBUG else logging.WARNING
    )
    logging.getLogger('qdrant_client').setLevel(logging.INFO)
    logging.getLogger('openai').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.WARNING)  # Reduce HTTP client logs


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Name of the logger

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    return logger


class LogContext:
    """
    Context manager for adding contextual information to logs.
    """
    def __init__(self, **kwargs):
        self.context = kwargs
        self.logger = get_logger(__name__)

    def __enter__(self):
        # In a real implementation with context propagation, we would add context here
        # For now, we'll just log the context being entered
        self.logger.debug(f"Entering log context: {self.context}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(
                f"Exception in context {self.context}: {exc_type.__name__}: {exc_val}",
                exc_info=(exc_type, exc_val, exc_tb)
            )
        self.logger.debug(f"Exiting log context: {self.context}")


def log_api_call(endpoint: str, method: str, user_id: Optional[str] = None, session_id: Optional[str] = None):
    """
    Decorator to log API calls with contextual information.

    Args:
        endpoint: API endpoint being called
        method: HTTP method (GET, POST, etc.)
        user_id: Optional user identifier
        session_id: Optional session identifier
    """
    def decorator(func):
        import functools
        from fastapi import Request

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request if available
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            logger = get_logger(f"api.{endpoint.replace('/', '_')}")

            # Log the API call
            extra = {
                'endpoint': endpoint,
                'method': method,
            }
            if user_id:
                extra['user_id'] = user_id
            if session_id:
                extra['session_id'] = session_id
            if request and hasattr(request, 'client'):
                extra['client_ip'] = request.client.host if request.client else 'unknown'

            logger.info(f"API call started: {method} {endpoint}", extra=extra)

            start_time = datetime.utcnow()
            try:
                result = await func(*args, **kwargs)
                duration = (datetime.utcnow() - start_time).total_seconds()

                logger.info(
                    f"API call completed: {method} {endpoint}, duration: {duration:.3f}s",
                    extra={**extra, 'duration': duration}
                )
                return result
            except Exception as e:
                duration = (datetime.utcnow() - start_time).total_seconds()
                logger.error(
                    f"API call failed: {method} {endpoint}, duration: {duration:.3f}s, error: {str(e)}",
                    extra={**extra, 'duration': duration},
                    exc_info=True
                )
                raise

        return wrapper
    return decorator


# Initialize logging when module is imported
setup_logging()