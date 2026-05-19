@echo off
for /f "tokens=5" %%a in ('netstat -ano ^| findstr "[::1]:5173 "') do (
    taskkill /PID %%a /T /F >nul 2>&1
)
echo Frontend stopped.
