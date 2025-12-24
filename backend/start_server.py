#!/usr/bin/env python3
"""
Start script for Railway deployment
"""
import os
import sys
import subprocess

def install_requirements():
    """Install packages from requirements.txt"""
    try:
        # Determine the correct path to requirements.txt
        # When Railway runs the script, it may be in a different directory
        current_dir = os.getcwd()
        print(f"Current working directory: {current_dir}")

        # Try multiple possible paths for requirements.txt
        possible_paths = [
            "./requirements.txt",  # Relative to current directory
            "./backend/requirements.txt",  # Relative to project root
            "/app/backend/requirements.txt",  # Common in containerized environments
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "requirements.txt"),  # From script location
            os.path.abspath(os.path.join(os.path.dirname(__file__), "requirements.txt"))  # Same directory as script
        ]

        requirements_path = None
        for path in possible_paths:
            if os.path.exists(path):
                requirements_path = path
                print(f"Found requirements.txt at: {path}")
                break

        if requirements_path is None:
            print("Could not find requirements.txt in any of the expected locations:")
            for path in possible_paths:
                print(f"  - {path}")
            return False

        # Install packages from requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("Successfully installed requirements from requirements.txt")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements from requirements.txt: {e}")
        return False
    except Exception as e:
        print(f"Error finding or installing requirements: {e}")
        return False

def main():
    """Main entry point for Railway deployment"""
    print("Starting application...")

    # Install requirements if needed
    if not install_requirements():
        print("Could not install requirements, exiting...")
        sys.exit(1)

    # Add project directory to path
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_dir)
    print(f"Added project directory to path: {project_dir}")

    # Import and create the app
    try:
        from app.main import create_app
        app = create_app()
        print("Successfully imported and created the application")
    except ImportError as e:
        print(f"Error importing application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Start the server
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting server on {host}:{port}")

    try:
        import uvicorn
        print("Uvicorn imported successfully")

        # Run with reload=False and proper logging
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            reload=False,
            timeout_graceful_shutdown=5,
            timeout_keep_alive=5
        )
        print("Server started successfully")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()