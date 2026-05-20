# Feature: WebView Application Window

## Description

Replace the default-browser launch with a dedicated application window using pywebview. The window embeds a WebView2 (Chromium-based) renderer, giving the app a native desktop feel without bundling a full browser. When the window is closed, the backend server shuts down cleanly.

## User Stories

- As a user, I want the app to open in its own window so it feels like a native desktop application, not a browser tab.
- As a user, I want closing the window to fully stop the application so no background processes remain.
- As a user, I want the window to have a proper title and a reasonable default size so it is usable immediately on launch.

## Acceptance Criteria

1. Launching `DataProcessingApp.exe` opens a dedicated application window (not the system browser).
2. The window title is "Data Processing App".
3. The default window size is 1280×800; minimum size is 800×600.
4. The DropZone UI is visible and functional inside the window.
5. Closing the window terminates the uvicorn backend process within 5 seconds.
6. No orphaned Python processes remain after the window is closed (verified via Task Manager).
7. The packaged exe builds and runs without errors on Windows 10/11 with WebView2 Runtime installed.

## UI / Interaction Notes

- Standard OS window chrome (title bar, minimize, maximize, close buttons).
- No custom menu bar or toolbar for Phase 2 — just the embedded web content.

## Technical Notes

- **Approach**: Microsoft Edge in app mode (`msedge --app=URL --window-size=WxH --user-data-dir=...`). Opens a chrome-less window (no address bar, no tabs) that looks and feels like a native desktop window. No additional Python dependencies required.
- **Prerequisite**: Microsoft Edge must be present on the target machine. It is pre-installed on all Windows 10 (1803+) and Windows 11 machines.
- **Isolated profile**: `--user-data-dir` points to a temp directory so this Edge instance is tracked as a distinct process, independent of any other open Edge windows.
- **Shutdown flow**: `launcher.py` starts uvicorn via `uvicorn.Server` (instead of `uvicorn.run`) so `server.should_exit = True` can be called after the window closes. `subprocess.Popen.wait()` blocks until the Edge window is closed, then control returns and the server is signalled.
- **Fallback**: if Edge is not found, the app opens in the default browser (no shutdown-on-close in fallback mode).
- **Why not pywebview**: pywebview's Windows backends depend on `pythonnet`, which has no prebuilt wheel for Python 3.14. Revisit when pythonnet adds 3.14 support.

## Out of Scope

- Custom window chrome or frameless mode.
- System tray icon (deferred to Phase 7).
- macOS/Linux webview backends.
- pywebview integration (blocked on pythonnet Python 3.14 support).

## Implementation Notes

Used Edge app mode (`msedge --app=URL`) instead of pywebview because pythonnet (required by pywebview's Windows backends) has no prebuilt wheel for Python 3.14.

`uvicorn.run()` replaced with `uvicorn.Server` + `server.should_exit = True` to enable clean programmatic shutdown after the window closes. `subprocess.Popen.wait()` on the Edge process provides the blocking "window open" signal.
