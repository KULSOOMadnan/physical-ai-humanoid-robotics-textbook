#!/usr/bin/env python3
"""
Start script for Railway deployment
"""
import os
import sys
import subprocess
import importlib.util

def install_uvicorn():
    """Install uvicorn if not available"""
    try:
        import uvicorn
        return True
    except ImportError:
        print("Installing uvicorn...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "uvicorn[standard]"])
        try:
            import uvicorn
            return True
        except ImportError:
            print("Failed to install or import uvicorn")
            return False

def main():
    """Main entry point for Railway deployment"""
    # Install uvicorn if needed
    if not install_uvicorn():
        print("Could not install uvicorn, exiting...")
        sys.exit(1)

    # Add project directory to path
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_dir)

    # Import and create the app
    try:
        from app.main import create_app
        app = create_app()
    except ImportError as e:
        print(f"Error importing application: {e}")
        sys.exit(1)

    # Start the server
    port = int(os.environ.get("PORT", 8000))

    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()