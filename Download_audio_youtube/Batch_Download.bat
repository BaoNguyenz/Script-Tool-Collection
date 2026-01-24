@echo off
REM YouTube Audio Downloader - Batch Mode
REM Supports batch download from text file

title YouTube Audio Downloader
color 0A

echo ============================================================
echo        YOUTUBE AUDIO DOWNLOADER - BATCH MODE
echo ============================================================
echo.

REM Check if urls.txt exists
if not exist urls.txt (
    echo [INFO] File urls.txt chua ton tai.
    echo [INFO] Tao file urls.txt mau...
    echo.
    (
        echo # YouTube Audio URLs - Moi dong 1 URL
        echo # Vi du:
        echo # https://www.youtube.com/watch?v=VIDEO_ID1
        echo # https://www.youtube.com/watch?v=VIDEO_ID2
        echo.
    ) > urls.txt
    echo [SUCCESS] Da tao file urls.txt
    echo [ACTION] Hay them URLs vao file urls.txt roi chay lai script nay.
    echo.
    notepad urls.txt
    pause
    exit
)

echo [BATCH] Tim thay file urls.txt
echo.

REM Choose format
echo [FORMAT] Chon dinh dang:
echo   [1] MP3 320kbps (mac dinh)
echo   [2] FLAC (lossless)
echo   [3] WAV (lossless)
echo   [4] ALAC (Apple Lossless)
echo   [5] OPUS
echo   [6] M4A
echo.
set /p FORMAT_CHOICE="Chon (1-6): "

set AUDIO_FORMAT=mp3
if "%FORMAT_CHOICE%"=="2" set AUDIO_FORMAT=flac
if "%FORMAT_CHOICE%"=="3" set AUDIO_FORMAT=wav
if "%FORMAT_CHOICE%"=="4" set AUDIO_FORMAT=alac
if "%FORMAT_CHOICE%"=="5" set AUDIO_FORMAT=opus
if "%FORMAT_CHOICE%"=="6" set AUDIO_FORMAT=m4a

echo.
echo [INFO] Format: %AUDIO_FORMAT%
echo ============================================================
echo   BAT DAU TAI...
echo ============================================================
echo.

REM Run batch download
python download_audio.py --batch urls.txt --format %AUDIO_FORMAT% --quality 320

echo.
echo ============================================================
echo   HOAN THANH!
echo ============================================================
echo.

REM Ask to open folder
set /p OPEN_FOLDER="Mo thu muc output_audio? (Y/N): "
if /i "%OPEN_FOLDER%"=="Y" explorer output_audio

pause
