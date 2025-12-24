from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api_router import api_router
from app.config.settings import get_settings
from app.config.qdrant import qdrant_config
from app.core.exceptions import add_exception_handlers
from app.config.config_manager import config_manager, validate_deployment_config
from app.utils.performance import add_performance_monitoring
import asyncio
import logging


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Validate configuration before starting
    if not validate_deployment_config():
        raise ValueError("Configuration validation failed")

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config_manager.get("logging.level", "INFO")),
        format=config_manager.get("logging.format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    app = FastAPI(
        title="RAG Chatbot API",
        description="API for Retrieval-Augmented Generation Chatbot with book intelligence",
        version="0.1.0",
        debug=get_settings().DEBUG,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for development
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add performance monitoring middleware
    add_performance_monitoring(app)

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")

    # Add custom exception handlers
    add_exception_handlers(app)

    @app.on_event("startup")
    async def startup_event():
        """Initialize Qdrant collection on startup."""
        await qdrant_config.initialize_collection(vector_size=1024)  # Use 1024 dimensions for Cohere embeddings

    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup operations on shutdown."""
        logging.info("Application shutting down")

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    @app.get("/config")
    async def config_check():
        """Return basic configuration information (without sensitive data)."""
        return {
            "status": "healthy",
            "debug": settings.DEBUG,
            "llm_provider": config_manager.get("llm.provider"),
            "database_configured": bool(config_manager.get("database.url")),
            "qdrant_configured": bool(config_manager.get("qdrant.url"))
        }

    @app.get("/")
    async def root():
        return {"status": "server is running"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=get_settings().HOST,
        port=get_settings().PORT,
        reload=get_settings().DEBUG,
    )