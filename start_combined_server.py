#!/usr/bin/env python3
"""
Combined server that runs both FastAPI backend and Streamlit frontend
in a single process for single URL deployment.
"""

import os
import sys
import threading
import time
import subprocess
import signal
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting FastAPI backend...")
    
    # Import and start FastAPI app
    from backend.api import app
    import uvicorn
    
    # Run backend on internal port
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

def start_frontend():
    """Start the Streamlit frontend."""
    print("🎨 Starting Streamlit frontend...")
    
    # Set backend URL to local backend
    os.environ["BACKEND_URL"] = "http://127.0.0.1:8000"
    
    # Get port from environment (Render sets this)
    port_env = os.environ.get("PORT", "10000")
    # Handle case where PORT might be literal '$PORT' string
    if port_env == "$PORT":
        port = 10000
    else:
        try:
            port = int(port_env)
        except ValueError:
            print(f"⚠️ Invalid PORT value '{port_env}', using default 10000")
            port = 10000
    
    # Start Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    subprocess.run(cmd)

def main():
    """Main function to coordinate both servers."""
    print("🌟 Starting MindfulCompanion - Single URL Deployment")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(8)
    
    # Check if backend is responding
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is ready!")
        else:
            print("⚠️ Backend may not be fully ready, but proceeding...")
    except Exception as e:
        print(f"⚠️ Backend check failed: {e}, but proceeding...")
    
    # Start frontend (this will block and handle the main port)
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down gracefully...")
        sys.exit(0)

if __name__ == "__main__":
    main()
