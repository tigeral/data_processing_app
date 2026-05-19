"""
Desktop launcher: starts the FastAPI backend and opens the app in the default browser.
Used both as a dev convenience script and as the entry point for the packaged Windows exe.
"""
import subprocess
import sys
import time
import webbrowser
import urllib.request
import urllib.error
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}"
STARTUP_TIMEOUT = 15  # seconds to wait for backend to become ready


def _backend_ready() -> bool:
    try:
        urllib.request.urlopen(f"{URL}/docs", timeout=1)
        return True
    except Exception:
        return False


def _find_uvicorn() -> str:
    # When bundled by PyInstaller, uvicorn is in the same directory as the exe
    bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    candidate = bundle_dir / "uvicorn.exe"
    if candidate.is_file():
        return str(candidate)
    return "uvicorn"


def main() -> None:
    if _backend_ready():
        print(f"Backend already running at {URL}, opening browser.")
        webbrowser.open(URL)
        return

    backend_dir = Path(__file__).parent / "backend"
    uvicorn = _find_uvicorn()

    proc = subprocess.Popen(
        [uvicorn, "main:app", "--host", HOST, "--port", str(PORT)],
        cwd=str(backend_dir),
    )

    print(f"Waiting for backend on {URL}...")
    deadline = time.monotonic() + STARTUP_TIMEOUT
    while time.monotonic() < deadline:
        if _backend_ready():
            break
        time.sleep(0.3)
    else:
        proc.terminate()
        sys.exit(f"ERROR: Backend did not start within {STARTUP_TIMEOUT}s.")

    webbrowser.open(URL)
    print(f"App running at {URL}. Close this window to stop the server.")

    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()


if __name__ == "__main__":
    main()
