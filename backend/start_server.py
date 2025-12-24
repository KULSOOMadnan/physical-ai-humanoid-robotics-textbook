#!/usr/bin/env python3
"""
Start script for Railway deployment
"""
import os

# Set required environment variables BEFORE any imports to handle settings validation
required_vars = {
    'DATABASE_URL': os.environ.get('DATABASE_URL', 'sqlite:///./test.db'),
    'QDRANT_URL': os.environ.get('QDRANT_URL', 'http://localhost:6333'),
    'QDRANT_API_KEY': os.environ.get('QDRANT_API_KEY', 'dummy-key'),
    'OPENROUTER_API_KEY': os.environ.get('OPENROUTER_API_KEY', 'dummy-key'),
    'COHERE_API_KEY': os.environ.get('COHERE_API_KEY', 'dummy-key'),
    'DEBUG': os.environ.get('DEBUG', 'True')
}

for key, value in required_vars.items():
    os.environ.setdefault(key, value)

# Now continue with the rest of the application
import sys
import subprocess

def install_requirements():
    """Install packages from the Railway-specific requirements file"""
    try:
        current_dir = os.getcwd()
        print(f"Current working directory: {current_dir}")

        # Use the Railway-specific requirements file without hashes
        requirements_path = "./requirements_railway.txt"

        if not os.path.exists(requirements_path):
            print(f"requirements_railway.txt not found at: {requirements_path}")
            return False

        print(f"Found requirements_railway.txt at: {requirements_path}")

        # Install packages from the Railway requirements file
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])

        print("Successfully installed requirements for Railway deployment")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        return False
    except Exception as e:
        print(f"Error finding or installing requirements: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_railway_app():
    """Create a FastAPI app instance without problematic startup events"""
    # Import after setting environment variables
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from app.api.v1.api_router import api_router
    from app.config.settings import settings
    from app.core.exceptions import add_exception_handlers
    from app.config.config_manager import config_manager
    from app.utils.performance import add_performance_monitoring
    import logging

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config_manager.get("logging.level", "INFO")),
        format=config_manager.get("logging.format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    app = FastAPI(
        title="RAG Chatbot API",
        description="API for Retrieval-Augmented Generation Chatbot with book intelligence",
        version="0.1.0",
        debug=settings.DEBUG,
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

    # Add routes (without the startup event that connects to Qdrant)
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

def main():
    """Main entry point for Railway deployment"""
    print("Starting application...")

    # Install requirements if needed
    if not install_requirements():
        print("Could not install requirements, exiting...")
        sys.exit(1)

    # Add current directory to path (since backend is root in Railway)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    print(f"Added current directory to path: {current_dir}")

    # Import and create the app without the problematic startup event
    try:
        print("Creating FastAPI application...")
        app = create_railway_app()
        print("Successfully created the application")
    except ImportError as e:
        print(f"Error importing application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Start the server
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"  # Always use 0.0.0.0 for Railway
    print(f"Starting server on {host}:{port}")

    try:
        import uvicorn
        print("Uvicorn imported successfully")

        # Run with minimal configuration to avoid startup issues
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            reload=False,
            workers=1
        )
        print("Server started successfully")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()