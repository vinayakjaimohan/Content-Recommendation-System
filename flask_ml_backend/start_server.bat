@echo off
echo ========================================
echo Flask ML Backend Startup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Python found. Starting Flask server...
echo.

REM Install dependencies if needed
echo Installing/checking dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask ML Backend...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python start_server.py

pause 