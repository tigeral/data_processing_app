@echo off
for /f "tokens=5" %%a in ('netstat -ano ^| findstr "127.0.0.1:8000 "') do (
    taskkill /PID %%a /T /F >nul 2>&1
)
echo Backend stopped.
