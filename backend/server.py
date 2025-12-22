#!/usr/bin/env python3
"""
Simple start script for the RAG Chatbot API server.
This ensures the server starts properly on Railway.
"""
import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Now import the application
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
    except ImportError as e:
        print(f"Error importing uvicorn: {e}")
        print("Make sure uvicorn is in requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)