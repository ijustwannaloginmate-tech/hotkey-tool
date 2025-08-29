@echo off
REM HotVolume Startup Script
REM Starts the HotVolume application

echo Starting HotVolume...
python run_hotvolume.py

REM If the script reaches here, there was likely an error
echo.
echo HotVolume has exited. 
echo Check the console output above for any error messages.
echo.
pause