@echo off
REM YouTube Video Downloader - Interactive Batch Script
REM Double-click to run and paste URL

title YouTube Video Downloader
color 0A

:START
cls
echo ============================================================
echo        YOUTUBE VIDEO DOWNLOADER
echo ============================================================
echo.

REM Prompt for URL
set /p VIDEO_URL="Paste URL video (hoac 'exit' de thoat): "

REM Check if user wants to exit
if /i "%VIDEO_URL%"=="exit" goto END
if "%VIDEO_URL%"=="" goto START

echo.
echo ============================================================
echo   DANG TAI VIDEO...
echo ============================================================
echo.

REM Run Python script
python download_simple.py "%VIDEO_URL%"

echo.
echo ============================================================
echo.
pause

REM Ask if user wants to download another
set /p CONTINUE="Tai video khac? (Y/N): "
if /i "%CONTINUE%"=="Y" goto START
if /i "%CONTINUE%"=="y" goto START

:END
echo.
echo Cam on da su dung!
timeout /t 2 >nul
exit
