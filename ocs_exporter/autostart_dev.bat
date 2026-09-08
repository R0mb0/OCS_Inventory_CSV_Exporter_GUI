@echo off
REM Starts OCS Exporter in autostart mode using the Python source code
REM (to be used BEFORE compiling the app into an .exe).
REM Works fine whether launched manually, placed in the Windows Startup
REM folder, or triggered by a Scheduled Task.

setlocal
set "APPDIR=%~dp0"
cd /d "%APPDIR%"

REM If the server needs a few seconds after login before the
REM network to OCS is ready, uncomment the following line (seconds):
REM timeout /t 20 /nobreak >nul

start "" py "%APPDIR%main.py" --autostart