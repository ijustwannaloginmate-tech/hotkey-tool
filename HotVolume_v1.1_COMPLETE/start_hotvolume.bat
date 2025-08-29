@echo off
REM HotVolume Startup Script v1.1
REM Starts the HotVolume application

echo Starting HotVolume v1.1...
echo Look for the volume icon in your system tray!
echo.
python run_hotvolume.py

REM If the script reaches here, there was likely an error
echo.
echo HotVolume has exited. 
echo Check the console output above for any error messages.
echo.
pause