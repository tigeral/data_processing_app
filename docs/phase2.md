# Phase 2 — Native Desktop App (Windows)

## Goal

Package the Data Processing App as a standalone Windows desktop application. A user with no Python or Node.js installed should be able to install and run the app from a single installer file. The app should open in a dedicated window and shut down cleanly when that window is closed.

## Deliverables

1. `launcher.py` — starts the FastAPI backend in-process and opens the app in an Edge app-mode window.
2. `backend/main.py` updated — serves compiled frontend static files when `frontend/dist/` is present.
3. `installer/app.spec` — PyInstaller spec producing a `--onedir` bundle.
4. `installer/setup.iss` — Inno Setup script producing `DataProcessingApp-setup.exe`.
5. `scripts/build-windows.bat` — one-command build pipeline: frontend → PyInstaller → Inno Setup.
6. Desktop shortcut and Start Menu entry created by the installer.
7. Clean uninstall via Windows Settings > Apps.

## Files Changed

| File | Change |
|---|---|
| `launcher.py` | New — desktop launcher and server lifecycle manager |
| `backend/main.py` | Added StaticFiles mount for `frontend/dist/` |
| `installer/app.spec` | New — PyInstaller bundle spec |
| `installer/setup.iss` | New — Inno Setup installer script |
| `scripts/build-windows.bat` | New — full build pipeline |
| `scripts/start-backend.bat` | Updated to activate venv before starting uvicorn |
| `requirements.txt` | Added `pyinstaller`, `aiofiles` |
| `README.md` | Added build instructions and stop-script section |

## Architecture: Desktop Packaging

The packaged application uses a **launcher + embedded server** model with no bundled browser:

```
DataProcessingApp.exe  (launcher.py, compiled by PyInstaller)
        |
        |-- starts --> uvicorn.Server (in-process thread)
        |                    |
        |                    |-- serves --> FastAPI app
        |                                       |
        |                                       +-- /api/v1/*   (REST endpoints)
        |                                       +-- /           (frontend/dist static files)
        |
        |-- opens --> msedge --app=http://localhost:8000
                          (chrome-less window, no address bar)
        |
        +-- on window close --> server.should_exit = True --> clean shutdown
```

### Key Design Decisions

#### 1. PyInstaller `--onedir` over `--onefile`

`--onefile` extracts the entire bundle to a temp directory on every launch, which is slow and can trigger Windows Defender. `--onedir` extracts once at install time — launch is fast and the file layout is transparent to the OS.

#### 2. In-process uvicorn instead of subprocess

The initial implementation spawned uvicorn as `subprocess.Popen(["uvicorn", ...])`. This failed in a PyInstaller bundle for two reasons:
- `uvicorn` is a Python package, not a standalone executable — no `uvicorn.exe` exists in the bundle.
- `__file__`-based path resolution for the backend directory is wrong under `sys._MEIPASS`.

**Fix**: run uvicorn via `uvicorn.Server` in a `threading.Thread`. The server instance is kept in module scope so `server.should_exit = True` can be called from the main thread after the window closes.

#### 3. Edge app mode instead of pywebview

pywebview was the first choice because it wraps the system WebView2 (already on Win10/11) with a clean Python API. However, pywebview's Windows backends depend on `pythonnet`, which has no prebuilt wheel for Python 3.14.

**Decision**: use `msedge --app=URL --user-data-dir=<isolated-profile>` instead. The `--app` flag opens Edge in a chrome-less window without tabs or address bar, giving a native-app appearance. The isolated `--user-data-dir` ensures the launched process is tracked independently of any other open Edge windows.

**Revisit** when pythonnet adds Python 3.14 wheel support — pywebview would give better control over the window (title, icon, frameless mode, JS bridge).

#### 4. `sys.stdout/stderr` redirect in windowed builds

PyInstaller with `console=False` sets `sys.stdout` and `sys.stderr` to `None`. Any code that writes to these streams (including uvicorn's startup logging and Python's `logging` module) raises `AttributeError: 'NoneType' object has no attribute 'write'`, silently killing the server thread before it binds to any port.

**Fix**: at the top of `launcher.py`, before starting the server thread, redirect `None` streams to `app.log` in the bundle root directory.

#### 5. `frontend/dist` path in bundled mode

`backend/main.py` originally resolved the frontend dist path as `Path(__file__).parent.parent / "frontend" / "dist"`. In a PyInstaller bundle, `__file__` for a compiled module points inside `sys._MEIPASS`, so the relative path calculation lands outside the bundle.

**Fix**: use `Path(sys._MEIPASS) / "frontend" / "dist"` when `sys._MEIPASS` is set.

#### 6. Python modules vs. data files in PyInstaller

The original `app.spec` listed `backend/app/` in the `datas` section. PyInstaller `datas` copies files as raw data — they are not importable as Python modules. Python source files must be found via `pathex` (static analysis) or declared in `hiddenimports` (dynamic imports).

**Fix**: removed `backend/app` from `datas`; added `main`, `app.api.drops`, `app.schemas.drop` to `hiddenimports` to cover imports that happen inside functions and are invisible to PyInstaller's static analyser.

## Bugs Fixed

| Issue | Root Cause | Fix |
|---|---|---|
| `FileNotFoundError` on launch (issue #1) | Subprocess approach tried to run `uvicorn.exe` which does not exist in the bundle | Replaced with `uvicorn.Server` in a thread |
| Exe silently does nothing (`console=False`) | `sys.stdout/stderr` are `None` in windowed builds; uvicorn startup log crashed the server thread | Redirect null streams to `app.log` before starting the thread |
| Frontend returns 404 after packaging | `frontend/dist` path calculation was wrong under `sys._MEIPASS` | Use `sys._MEIPASS` directly when bundled |

## Known Limitations

- **Edge required**: the app-mode window depends on Microsoft Edge. If Edge is not installed, the app falls back to opening the default browser, and closing the browser tab does not stop the backend.
- **WebView2 Runtime**: Edge's WebView2 rendering engine is pre-installed on Windows 11 and all machines with a recent Edge update. Very old Windows 10 installations may need to install the WebView2 Runtime separately.
- **No window icon**: the exe and installer have no custom icon. A `.ico` file can be provided in a later phase by setting `icon=` in `app.spec` and `installer/setup.iss`.
- **macOS / Linux packaging**: deferred. The launcher's `_find_edge()` function is Windows-only.

## Prerequisites for Building

- Python 3.11+ in a virtual environment with `requirements.txt` installed
- Node.js 20+ and npm
- [Inno Setup 6](https://jrsoftware.org/isinfo.php) with `iscc` in `PATH`

## Build Command

```bat
scripts\build-windows.bat
```

Output: `dist\installer\DataProcessingApp-setup.exe`
