# PyInstaller spec file for Data Processing App
# Run from the project root: pyinstaller installer/app.spec

import sys
from pathlib import Path

ROOT = Path(SPECPATH).parent
BACKEND = ROOT / "backend"
FRONTEND_DIST = ROOT / "frontend" / "dist"

a = Analysis(
    [str(ROOT / "launcher.py")],
    # pathex lets PyInstaller resolve imports from backend/ (main.py, app/)
    pathex=[str(BACKEND)],
    binaries=[],
    # Only non-Python data files go here; Python sources are resolved via pathex/imports
    datas=[
        (str(FRONTEND_DIST), "frontend/dist"),
    ],
    hiddenimports=[
        # backend modules imported dynamically inside _run_server()
        "main",
        "app",
        "app.api",
        "app.api.drops",
        "app.schemas",
        "app.schemas.drop",
        # uvicorn internals not detected by static analysis
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.auto",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.websockets",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.lifespan",
        "uvicorn.lifespan.on",
        # required by FastAPI StaticFiles
        "aiofiles",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="DataProcessingApp",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # no terminal window in production
    icon=None,      # replace with path to .ico file when available
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="DataProcessingApp",
)
