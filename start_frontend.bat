@echo off
REM Serves the chat page (frontend) on http://localhost:5500. It calls the backend on port 8000.
cd /d "%~dp0"
python -m http.server 5500 --bind 127.0.0.1 --directory static
