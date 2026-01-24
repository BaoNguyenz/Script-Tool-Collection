# YouTube Video Downloader - Simple Interactive Loop
# Chay lien tuc, chi can paste URL va Enter

Write-Host "`n"
Write-Host "========================================"
Write-Host "  YOUTUBE VIDEO DOWNLOADER - AUTO MODE"
Write-Host "========================================"
Write-Host ""

$scriptPath = Join-Path (Split-Path $PSScriptRoot -Parent) "download_simple.py"

while ($true) {
    Write-Host "[VIDEO] Paste URL video (hoac 'exit' de thoat): " -NoNewline
    $url = Read-Host
    
    # Check exit
    if ($url -eq "exit" -or $url -eq "quit" -or $url -eq "q") {
        Write-Host "`nTam biet!`n"
        break
    }
    
    # Validate URL
    if ([string]::IsNullOrWhiteSpace($url)) {
        Write-Host "[ERROR] URL trong! Vui long nhap lai.`n"
        continue
    }
    
    if ($url -notmatch "youtube\.com|youtu\.be") {
        Write-Host "[ERROR] URL khong hop le! Phai la link YouTube.`n"
        continue
    }
    
    # Ask for quality
    Write-Host "`n[QUALITY] Chon chat luong (Enter = best):"
    Write-Host "   [1] best (mac dinh)"
    Write-Host "   [2] 1080p"
    Write-Host "   [3] 720p"
    Write-Host "   [4] 480p"
    Write-Host "   [5] 360p"
    Write-Host "Chon (1-5): " -NoNewline
    $qualityChoice = Read-Host
    
    $quality = switch ($qualityChoice) {
        "2" { "1080p" }
        "3" { "720p" }
        "4" { "480p" }
        "5" { "360p" }
        default { "best" }
    }
    
    # Download
    Write-Host "`n========================================"
    Write-Host "  DANG TAI VIDEO ($quality)..."
    Write-Host "========================================`n"
    
    try {
        & python $scriptPath $url --quality $quality
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n========================================"
            Write-Host "  [SUCCESS] THANH CONG!"
            Write-Host "========================================`n"
            
            # Ask to open folder
            Write-Host "Mo thu muc chua file? (Y/N): " -NoNewline
            $openFolder = Read-Host
            if ($openFolder -eq "Y" -or $openFolder -eq "y") {
                Start-Process "explorer.exe" -ArgumentList (Join-Path $PSScriptRoot "output_download")
            }
        }
        else {
            Write-Host "`n[ERROR] TAI THAT BAI!"
        }
    }
    catch {
        Write-Host "`n[ERROR] LOI: $_"
    }
    
    Write-Host ""
}
