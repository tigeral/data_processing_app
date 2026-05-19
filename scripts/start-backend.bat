@echo off
cd /d "%~dp0.."
call .venv\Scripts\activate
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
