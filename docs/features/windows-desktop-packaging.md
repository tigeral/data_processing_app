# Feature: Windows Desktop Packaging

## Description

Package the Data Processing App as a standalone Windows desktop application. The installer bundles the Python backend (via PyInstaller), the compiled React frontend (served as static files by FastAPI), and a launcher executable that starts the backend process and opens the app in the default browser. No Electron or embedded browser — the system browser is used.

## User Stories

- As a user, I want to install the app on Windows with a standard installer so I do not need Python or Node.js installed.
- As a user, I want to launch the app from a desktop shortcut so I do not need to run terminal commands.
- As a user, I want the app to open in my browser automatically when I launch it.
- As a user, I want to uninstall the app cleanly through Windows settings.

## Acceptance Criteria

1. Running the installer (`DataProcessingApp-setup.exe`) completes without errors on a clean Windows machine with no Python or Node.js installed.
2. After installation, a desktop shortcut and a Start Menu entry are created.
3. Double-clicking the shortcut starts the backend server and opens `http://localhost:8000` in the default browser within 5 seconds.
4. The DropZone UI is visible and functional in the browser after launch.
5. Closing the browser does not stop the backend process; a system tray icon or taskbar entry remains.
6. The app can be fully uninstalled via Windows Settings > Apps, leaving no orphaned files.
7. The installer and uninstaller are signed-free but do not trigger Windows Defender false positives (PyInstaller `--onedir` mode preferred over `--onefile`).

## UI / Interaction Notes

- No new UI is added to the app itself in this phase.
- The launcher is a background process — no splash screen required for Phase 2.
- A system tray icon (simple, no menu) is acceptable but not required for Phase 2.

## Technical Notes

- **Frontend build**: `npm run build` in `frontend/` produces `frontend/dist/`. FastAPI serves this as a `StaticFiles` mount at `/`.
- **Backend bundling**: PyInstaller with `--onedir` bundles `backend/main.py` and all dependencies into a `dist/backend/` folder. The `frontend/dist/` directory is included as a data dependency.
- **Launcher**: A small Python script (`launcher.py`) at project root that starts the uvicorn subprocess and then calls `webbrowser.open("http://localhost:8000")` after a short readiness poll. PyInstaller also bundles the launcher as a separate exe (`DataProcessingApp.exe`).
- **Installer**: Inno Setup script (`installer/setup.iss`) packages `dist/backend/` and produces `DataProcessingApp-setup.exe`.
- **Port conflict**: If port 8000 is already in use, the launcher should log an error and exit gracefully.
- **Open decision**: Whether to add a system tray icon (requires `pystray` + `Pillow`) is deferred to Phase 7 UI polish.

## Out of Scope

- macOS and Linux packaging (later phases).
- Auto-update mechanism.
- Code signing of the installer or executable.
- Custom browser (Electron/Tauri/CEF).
- Backend running as a Windows Service.

## Implementation Notes

> This section is filled in after implementation.
