"""
Desktop launcher: starts the FastAPI backend and opens the app in the default browser.
Used both as a dev convenience script and as the entry point for the packaged Windows exe.
"""
import sys
import time
import threading
import webbrowser
import urllib.request
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}"
STARTUP_TIMEOUT = 15  # seconds to wait for backend to become ready

# When bundled by PyInstaller, all files are extracted to sys._MEIPASS.
# When running from source, use the project root.
_BUNDLE_ROOT = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(__file__).parent
_BACKEND_DIR = _BUNDLE_ROOT / "backend"

# Make backend package importable (required in both bundled and source modes).
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))


def _backend_ready() -> bool:
    try:
        urllib.request.urlopen(f"{URL}/docs", timeout=1)
        return True
    except Exception:
        return False


def _run_server() -> None:
    import uvicorn
    from main import app  # backend/main.py is on sys.path via _BACKEND_DIR
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


def main() -> None:
    if _backend_ready():
        print(f"Backend already running at {URL}, opening browser.")
        webbrowser.open(URL)
        return

    t = threading.Thread(target=_run_server, daemon=True)
    t.start()

    print(f"Waiting for backend on {URL}...")
    deadline = time.monotonic() + STARTUP_TIMEOUT
    while time.monotonic() < deadline:
        if _backend_ready():
            break
        time.sleep(0.3)
    else:
        sys.exit(f"ERROR: Backend did not start within {STARTUP_TIMEOUT}s.")

    webbrowser.open(URL)
    print(f"App running at {URL}. Press Ctrl+C to stop.")

    try:
        t.join()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
