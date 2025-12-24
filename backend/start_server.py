#!/usr/bin/env python3
"""
Start script for Railway deployment
"""
import os
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

        # Install the current package in non-editable mode
        subprocess.check_call([sys.executable, "-m", "pip", "install", "."])

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