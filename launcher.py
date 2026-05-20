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
_IS_BUNDLED = hasattr(sys, "_MEIPASS")
_BUNDLE_ROOT = Path(sys._MEIPASS) if _IS_BUNDLED else Path(__file__).parent

# With console=False PyInstaller builds, sys.stdout and sys.stderr are None.
# Uvicorn and logging write to stderr on startup — redirect to a log file to
# prevent AttributeError crashes that would silently kill the server thread.
if sys.stdout is None or sys.stderr is None:
    _log_path = _BUNDLE_ROOT / "app.log"
    _log_file = open(_log_path, "w", buffering=1, encoding="utf-8")
    if sys.stdout is None:
        sys.stdout = _log_file
    if sys.stderr is None:
        sys.stderr = _log_file

# Make backend importable when running from source (in the bundle, PyInstaller
# already compiled and archived backend modules, so no sys.path change needed).
if not _IS_BUNDLED:
    _backend_dir = _BUNDLE_ROOT / "backend"
    if str(_backend_dir) not in sys.path:
        sys.path.insert(0, str(_backend_dir))


def _backend_ready() -> bool:
    try:
        urllib.request.urlopen(f"{URL}/docs", timeout=1)
        return True
    except Exception:
        return False


def _run_server() -> None:
    import uvicorn
    from main import app  # backend/main.py is importable via sys.path (source) or archive (bundle)
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
