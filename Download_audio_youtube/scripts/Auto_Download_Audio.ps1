# YouTube Audio Downloader - Interactive Loop

Write-Host "`n"
Write-Host "========================================"
Write-Host "  YOUTUBE AUDIO DOWNLOADER"
Write-Host "========================================"
Write-Host ""

$scriptPath = Join-Path $PSScriptRoot "..\download_audio.py"

while ($true) {
    Write-Host "[AUDIO] Paste URL (hoac 'exit' de thoat): " -NoNewline
    $url = Read-Host
    
    # Check exit
    if ($url -eq "exit" -or $url -eq "quit" -or $url -eq "q") {
        Write-Host "`nTam biet!`n"
        break
    }
    
    # Validate URL
    if ([string]::IsNullOrWhiteSpace($url)) {
        Write-Host "[ERROR] URL trong!`n"
        continue
    }
    
    if ($url -notmatch "youtube\.com|youtu\.be") {
        Write-Host "[ERROR] URL khong hop le!`n"
        continue
    }
    
    # Choose format
    Write-Host "`n[FORMAT] Chon dinh dang:"
    Write-Host "   [1] MP3 320kbps (khuyến nghị - universal)"
    Write-Host "   [2] FLAC (lossless - audiophile)"
    Write-Host "   [3] WAV (lossless - production)"
    Write-Host "   [4] ALAC (Apple Lossless)"
    Write-Host "   [5] OPUS (modern, high quality)"
    Write-Host "   [6] M4A (AAC)"
    Write-Host "Chon (1-6, Enter = 1): " -NoNewline
    $formatChoice = Read-Host
    
    $format = switch ($formatChoice) {
        "2" { "flac" }
        "3" { "wav" }
        "4" { "alac" }
        "5" { "opus" }
        "6" { "m4a" }
        default { "mp3" }
    }
    
    # Choose quality (for lossy formats)
    $quality = "best"
    if ($format -eq "mp3" -or $format -eq "opus" -or $format -eq "m4a") {
        Write-Host "`n[QUALITY] Chon chat luong:"
        Write-Host "   [1] best (khuyến nghị)"
        Write-Host "   [2] 320 kbps"
        Write-Host "   [3] 256 kbps"
        Write-Host "   [4] 192 kbps"
        Write-Host "Chon (1-4, Enter = 1): " -NoNewline
        $qualityChoice = Read-Host
        
        $quality = switch ($qualityChoice) {
            "2" { "320" }
            "3" { "256" }
            "4" { "192" }
            default { "best" }
        }
    }
    
    # Download
    Write-Host "`n========================================"
    Write-Host "  DOWNLOADING..."
    Write-Host "========================================`n"
    
    try {
        & python $scriptPath $url --format $format --quality $quality
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n[SUCCESS] Hoan thanh!`n"
            
            # Ask to open folder
            Write-Host "Mo thu muc? (Y/N): " -NoNewline
            $open = Read-Host
            if ($open -eq "Y" -or $open -eq "y") {
                Start-Process "explorer.exe" -ArgumentList (Join-Path (Split-Path $PSScriptRoot -Parent) "output_audio")
            }
        }
    }
    catch {
        Write-Host "`n[ERROR] That bai!"
    }
    
    Write-Host ""
}
