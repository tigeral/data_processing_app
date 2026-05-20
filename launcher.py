"""
Desktop launcher: starts the FastAPI backend and opens the app in an Edge app-mode window.
When the window is closed the backend server shuts down cleanly.
Used both as a dev convenience script and as the entry point for the packaged Windows exe.
"""
import shutil
import sys
import tempfile
import time
import threading
import webbrowser
import urllib.request
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}"
STARTUP_TIMEOUT = 15  # seconds to wait for backend to become ready

# When bundled by PyInstaller all files are extracted to sys._MEIPASS.
# When running from source use the project root.
_IS_BUNDLED = hasattr(sys, "_MEIPASS")
_BUNDLE_ROOT = Path(sys._MEIPASS) if _IS_BUNDLED else Path(__file__).parent

# With console=False PyInstaller builds sys.stdout/stderr are None.
# Redirect to a log file so uvicorn's logging doesn't crash the server thread.
if sys.stdout is None or sys.stderr is None:
    _log_path = _BUNDLE_ROOT / "app.log"
    _log_file = open(_log_path, "w", buffering=1, encoding="utf-8")
    if sys.stdout is None:
        sys.stdout = _log_file
    if sys.stderr is None:
        sys.stderr = _log_file

# Make backend importable when running from source.
# In the bundle PyInstaller already archived backend modules.
if not _IS_BUNDLED:
    _backend_dir = _BUNDLE_ROOT / "backend"
    if str(_backend_dir) not in sys.path:
        sys.path.insert(0, str(_backend_dir))

_server = None  # uvicorn.Server instance, set in _run_server()


def _backend_ready() -> bool:
    try:
        urllib.request.urlopen(f"{URL}/docs", timeout=1)
        return True
    except Exception:
        return False


def _run_server() -> None:
    global _server
    import uvicorn
    from main import app  # importable via sys.path (source) or archive (bundle)
    config = uvicorn.Config(app, host=HOST, port=PORT, log_level="info")
    _server = uvicorn.Server(config)
    _server.run()


def _find_edge() -> str | None:
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    return shutil.which("msedge")


def _open_app_window() -> None:
    """Open Edge in app mode and block until the window is closed."""
    import subprocess

    edge = _find_edge()
    if not edge:
        # Edge not found — fall back to the default browser (no shutdown-on-close)
        print("WARNING: Microsoft Edge not found. Opening in default browser.")
        webbrowser.open(URL)
        return

    # Isolated profile so we can track exactly this process.
    profile_dir = Path(tempfile.gettempdir()) / "data-processing-app-profile"
    proc = subprocess.Popen([
        edge,
        f"--app={URL}",
        "--window-size=1280,800",
        f"--user-data-dir={profile_dir}",
    ])
    proc.wait()  # blocks until the window is closed


def main() -> None:
    already_running = _backend_ready()

    if not already_running:
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

    _open_app_window()  # blocks until window is closed (or browser tab is opened)

    # Window closed — signal uvicorn to stop
    if _server is not None:
        _server.should_exit = True
        if not already_running:
            t.join(timeout=5)


if __name__ == "__main__":
    main()
