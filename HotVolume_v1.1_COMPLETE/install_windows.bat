@echo off
REM HotVolume Installation Script for Windows
REM This script installs dependencies and sets up the HotVolume application

echo ==========================================
echo HotVolume - Application Volume Controller v1.1
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python detected. Installing dependencies...
echo.

REM Install Python dependencies
echo Installing required packages...
pip install -r backend\requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Installation completed successfully!
echo ==========================================
echo.
echo To start HotVolume:
echo   1. Double-click 'start_hotvolume.bat'
echo   2. Or run: python run_hotvolume.py
echo.
echo The application will appear in your system tray.
echo Right-click the tray icon to access controls.
echo.
echo NEW FEATURES in v1.1:
echo   • Settings now SAVE automatically
echo   • App stays in tray when config closed
echo   • Updated for Spotify.exe (capital S)
echo.
echo Default hotkeys:
echo   Ctrl+Shift+F1/F2/F3  - Spotify controls
echo   Ctrl+Shift+F4/F5/F6  - Chrome controls  
echo   Ctrl+Shift+F7/F8/F9  - Discord controls
echo.
pause