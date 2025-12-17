from fastapi import HTTPException, status
from typing import Optional
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGException(HTTPException):
    """
    Base exception class for RAG-related errors.
    """
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)
        logger.error(f"RAGException: {detail}")


class ContentProcessingError(RAGException):
    """
    Exception raised when there's an error processing book content.
    """
    def __init__(self, detail: str = "Error processing book content"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetrievalError(RAGException):
    """
    Exception raised when there's an error retrieving content from vector store.
    """
    def __init__(self, detail: str = "Error retrieving content from vector store"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerationError(RAGException):
    """
    Exception raised when there's an error generating a response.
    """
    def __init__(self, detail: str = "Error generating response"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContextInsufficientError(RAGException):
    """
    Exception raised when the context is insufficient to answer a query.
    """
    def __init__(self, detail: str = "Insufficient context to answer the query"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class SessionNotFoundError(RAGException):
    """
    Exception raised when a session is not found.
    """
    def __init__(self, detail: str = "Session not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class ValidationError(RAGException):
    """
    Exception raised when input validation fails.
    """
    def __init__(self, detail: str = "Input validation failed"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


# Custom exception handlers for FastAPI
def add_exception_handlers(app):
    """
    Add custom exception handlers to the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    @app.exception_handler(RAGException)
    async def handle_rag_exception(request, exc):
        logger.error(f"RAGException: {exc.detail} | Path: {request.url.path} | Method: {request.method}")
        return {
            "status_code": exc.status_code,
            "detail": exc.detail,
            "error_type": exc.__class__.__name__
        }

    @app.exception_handler(ContentProcessingError)
    async def handle_content_processing_error(request, exc):
        logger.error(f"ContentProcessingError: {exc.detail} | Path: {request.url.path} | Method: {request.method}")
        return {
            "status_code": exc.status_code,
            "detail": exc.detail,
            "error_type": exc.__class__.__name__
        }

    @app.exception_handler(RetrievalError)
    async def handle_retrieval_error(request, exc):
        logger.error(f"RetrievalError: {exc.detail} | Path: {request.url.path} | Method: {request.method}")
        return {
            "status_code": exc.status_code,
            "detail": exc.detail,
            "error_type": exc.__class__.__name__
        }

    @app.exception_handler(GenerationError)
    async def handle_generation_error(request, exc):
        logger.error(f"GenerationError: {exc.detail} | Path: {request.url.path} | Method: {request.method}")
        return {
            "status_code": exc.status_code,
            "detail": exc.detail,
            "error_type": exc.__class__.__name__
        }

    @app.exception_handler(ContextInsufficientError)
    async def handle_context_insufficient_error(request, exc):
        logger.info(f"ContextInsufficientError: {exc.detail} | Path: {request.url.path} | Method: {request.method}")
        return {
            "status_code": exc.status_code,
            "detail": exc.detail,
            "error_type": exc.__class__.__name__
        }

    @app.exception_handler(SessionNotFoundError)
    async def handle_session_not_found_error(request, exc):
        logger.warning(f"SessionNotFoundError: {exc.detail} | Path: {request.url.path} | Method: {request.method}")
        return {
            "status_code": exc.status_code,
            "detail": exc.detail,
            "error_type": exc.__class__.__name__
        }

    @app.exception_handler(ValidationError)
    async def handle_validation_error(request, exc):
        logger.warning(f"ValidationError: {exc.detail} | Path: {request.url.path} | Method: {request.method}")
        return {
            "status_code": exc.status_code,
            "detail": exc.detail,
            "error_type": exc.__class__.__name__
        }