@echo off
setlocal
cd /d "%~dp0.."

echo [1/3] Building frontend...
cd frontend
call npm run build
if errorlevel 1 ( echo ERROR: Frontend build failed. & exit /b 1 )
cd ..

echo [2/3] Running PyInstaller...
call .venv\Scripts\activate
pip install pyinstaller >nul 2>&1
pyinstaller installer\app.spec --clean --noconfirm
if errorlevel 1 ( echo ERROR: PyInstaller failed. & exit /b 1 )

echo [3/3] Creating installer...
where iscc >nul 2>&1
if errorlevel 1 (
    echo WARNING: Inno Setup ^(iscc^) not found in PATH. Skipping installer step.
    echo          Install Inno Setup from https://jrsoftware.org/isinfo.php and re-run.
) else (
    iscc installer\setup.iss
    if errorlevel 1 ( echo ERROR: Inno Setup failed. & exit /b 1 )
    echo Installer created: dist\installer\DataProcessingApp-setup.exe
)

echo Done. Packaged app: dist\DataProcessingApp\DataProcessingApp.exe
