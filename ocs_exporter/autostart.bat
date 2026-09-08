@echo off
REM Starts OCS Exporter in autostart mode using the compiled executable.
REM Must be placed in the SAME folder as the .exe.
REM Can be launched manually, placed in the Windows Startup folder,
REM or triggered by a Scheduled Task.

setlocal
set "APPDIR=%~dp0"

REM If the server needs a few seconds after login before the
REM network to OCS is ready, uncomment the following line (seconds):
REM timeout /t 20 /nobreak >nul

start "" "%APPDIR%OCSExporter.exe" --autostart