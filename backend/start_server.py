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
        # Install packages from requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Successfully installed requirements from requirements.txt")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install requirements from requirements.txt")
        return False

def main():
    """Main entry point for Railway deployment"""
    # Get project directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)  # Change to project directory

    # Install requirements if needed
    if not install_requirements():
        print("Could not install requirements, exiting...")
        sys.exit(1)

    # Add project directory to path
    sys.path.insert(0, project_dir)

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
    print(f"Starting server on port {port}")

    try:
        import uvicorn
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()