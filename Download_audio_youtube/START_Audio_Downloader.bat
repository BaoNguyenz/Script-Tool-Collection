@echo off
REM Easy launcher for Audio Downloader

title YouTube Audio Downloader
color 0A

echo ========================================
echo   Starting Audio Downloader...
echo ========================================
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0scripts\Auto_Download_Audio.ps1"

pause
