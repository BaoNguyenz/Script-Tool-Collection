@echo off
REM Run PowerShell script - Double-click this file
REM This is a wrapper to run Auto_Download.ps1

title YouTube Video Downloader
color 0A

echo ========================================
echo   Starting YouTube Downloader...
echo ========================================
echo.

REM Run PowerShell script from scripts folder
powershell.exe -ExecutionPolicy Bypass -File "%~dp0scripts\Auto_Download.ps1"

pause
