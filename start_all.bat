@echo off
REM Starts the backend and the frontend in two windows, then opens the chat page in your browser.
cd /d "%~dp0"
start "Campus Doubt Desk - backend" cmd /k start_backend.bat
start "Campus Doubt Desk - frontend" cmd /k start_frontend.bat
timeout /t 4 /nobreak >nul
start "" http://localhost:5500
