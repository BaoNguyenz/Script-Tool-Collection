@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ============================================================
echo   Vietnamese Subtitle Generator - Environment Setup
echo ============================================================
echo.
echo This script will:
echo   1. Create a new conda environment: subtitle_generator
echo   2. Install Python 3.10
echo   3. Install PyTorch with CUDA support (if available)
echo   4. Install stable-ts and all dependencies
echo   5. Install FFmpeg
echo.
echo Please wait, this may take several minutes...
echo ============================================================
echo.

REM Check if conda environment already exists
call conda env list | findstr /C:"subtitle_generator" >nul
if %ERRORLEVEL% EQU 0 (
    echo [WARNING] Environment 'subtitle_generator' already exists!
    echo.
    choice /C YN /M "Do you want to remove and recreate it? (Y/N)"
    if !ERRORLEVEL! EQU 2 (
        echo.
        echo [INFO] Setup cancelled by user.
        pause
        exit /b 0
    )
    echo.
    echo [INFO] Removing existing environment...
    call conda env remove -n subtitle_generator -y
    echo.
)

echo ============================================================
echo [STEP 1/5] Creating conda environment with Python 3.10...
echo ============================================================
call conda create -n subtitle_generator python=3.10 -y
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to create conda environment!
    pause
    exit /b 1
)
echo [SUCCESS] Conda environment created!
echo.

echo ============================================================
echo [STEP 2/5] Activating environment...
echo ============================================================
call conda activate subtitle_generator
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to activate environment!
    pause
    exit /b 1
)
echo [SUCCESS] Environment activated!
echo.

echo ============================================================
echo [STEP 3/5] Installing PyTorch with CUDA support...
echo ============================================================
echo [INFO] Detecting GPU availability...
nvidia-smi >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [INFO] NVIDIA GPU detected! Installing PyTorch with CUDA 12.1...
    call conda install pytorch torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
) else (
    echo [INFO] No NVIDIA GPU detected. Installing CPU-only PyTorch...
    call conda install pytorch torchaudio cpuonly -c pytorch -y
)
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install PyTorch!
    pause
    exit /b 1
)
echo [SUCCESS] PyTorch installed!
echo.

echo ============================================================
echo [STEP 4/5] Installing stable-ts and dependencies...
echo ============================================================
call pip install stable-ts
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install stable-ts!
    pause
    exit /b 1
)
echo [SUCCESS] stable-ts installed!
echo.

echo ============================================================
echo [STEP 5/5] Installing FFmpeg...
echo ============================================================
call conda install ffmpeg -c conda-forge -y
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install FFmpeg!
    pause
    exit /b 1
)
echo [SUCCESS] FFmpeg installed!
echo.

echo ============================================================
echo   SETUP COMPLETE!
echo ============================================================
echo.
echo Your environment is ready to use!
echo.
echo To activate the environment, run:
echo   conda activate subtitle_generator
echo.
echo Then run the subtitle generator:
echo   python generate_subtitles.py
echo.
echo ============================================================
pause
endlocal
