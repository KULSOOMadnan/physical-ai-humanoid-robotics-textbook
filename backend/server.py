#!/usr/bin/env python3
"""
Simple start script for the RAG Chatbot API server.
This ensures the server starts properly on Railway.
"""
import os
import sys
from app.main import create_app

# Create the application
app = create_app()

# For Railway deployment, we'll use a simple approach
if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))

    # For Railway, we'll use uvicorn if available
    try:
        import uvicorn
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            reload=False,
            log_level="info"
        )
    except ImportError:
        print("uvicorn not available, make sure it's in requirements.txt")
        sys.exit(1)