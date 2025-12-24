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
        current_dir = os.getcwd()
        print(f"Current working directory: {current_dir}")

        # The issue is with the editable install '-e .' in requirements.txt and hash verification
        # We need to install packages differently to avoid these issues
        requirements_path = "./requirements.txt"

        if not os.path.exists(requirements_path):
            print(f"requirements.txt not found at: {requirements_path}")
            return False

        print(f"Found requirements.txt at: {requirements_path}")

        # Install without hash verification to avoid the hash issues
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-deps", "-r", requirements_path])

        # Then install dependencies separately to resolve any missing dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", "--no-deps", "uvicorn[standard]"])

        print("Successfully installed requirements from requirements.txt")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements from requirements.txt: {e}")
        # Try alternative approach without hash verification
        try:
            print("Trying alternative installation method...")
            # Install with --force-reinstall and --no-cache-dir to avoid hash issues
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", "--no-cache-dir", "--no-deps", "-e", "."])
            print("Successfully installed with alternative method")
            return True
        except subprocess.CalledProcessError as e2:
            print(f"Alternative installation also failed: {e2}")
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