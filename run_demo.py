"""
RescuePath AI - Master Application Launcher.
Starts the FastAPI Backend and Vite React Frontend concurrently,
then launches your default web browser to the interactive dashboard.
"""

import sys
import os
import subprocess
import time
import webbrowser
import signal

def main():
    print("=" * 70)
    print("  RESCUEPATH AI — SEQUENTIAL & SPATIAL DATA MINING PLATFORM")
    print("  CSE3068 Academic Project Demo Launcher")
    print("=" * 70)

    project_root = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(project_root, "frontend")

    # 1. Start FastAPI Backend
    print("\n[1/3] Initializing FastAPI SSDM Backend Service on http://127.0.0.1:8000 ...")
    backend_cmd = [
        sys.executable, "-m", "uvicorn", 
        "backend.app.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000"
    ]
    backend_proc = subprocess.Popen(backend_cmd, cwd=project_root)

    # Allow backend 2 seconds to initialize
    time.sleep(2)

    # 2. Start Vite Frontend
    print("[2/3] Launching Vite React GIS Dashboard on http://localhost:5173 ...")
    # On Windows, use shell=True for npm
    frontend_proc = subprocess.Popen(
        "npm run dev", 
        cwd=frontend_dir, 
        shell=True
    )

    time.sleep(3)

    # 3. Open Browser
    url = "http://localhost:5173"
    print(f"[3/3] Opening interactive dashboard in your browser: {url}")
    print("\n" + "=" * 70)
    print("  RescuePath AI is now LIVE!")
    print(f"  - Web Dashboard:    {url}")
    print("  - Backend API Docs: http://127.0.0.1:8000/docs")
    print("  Press Ctrl+C in this terminal to gracefully terminate all services.")
    print("=" * 70 + "\n")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        # Keep running until user terminates
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping RescuePath AI platform services...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("Shutdown complete. Good luck with your project review!")

if __name__ == "__main__":
    main()
