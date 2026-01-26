@echo off
REM YouTube Downloader GUI Launcher
REM This script activates the conda environment and launches the GUI

echo ========================================
echo   YouTube Downloader GUI
echo ========================================
echo.

REM Activate conda environment
call conda activate youtube_dl

REM Check if activation was successful
if errorlevel 1 (
    echo [ERROR] Failed to activate 'youtube_dl' environment
    echo.
    echo Please create the environment first:
    echo   conda env create -f youtube_dl_environment.yml
    echo.
    pause
    exit /b 1
)

echo [OK] Environment activated
echo.

REM Change to script directory
cd /d "%~dp0"

REM Launch GUI
echo Launching YouTube Downloader GUI...
echo.
python youtube_downloader_gui.py

REM If python fails
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to launch GUI
    echo.
    echo Please ensure dependencies are installed:
    echo   conda activate youtube_dl
    echo   pip install customtkinter pillow
    echo.
    pause
    exit /b 1
)

pause
