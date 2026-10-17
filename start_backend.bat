@echo off
REM Starts the Campus Doubt Desk backend (FastAPI API) on http://localhost:8000
cd /d "%~dp0"
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
