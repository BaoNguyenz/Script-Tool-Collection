# YouTube Video Downloader - Interactive PowerShell GUI
# Double-click to run

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Create form
$form = New-Object System.Windows.Forms.Form
$form.Text = "YouTube Video Downloader"
$form.Size = New-Object System.Drawing.Size(600, 400)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false
$form.BackColor = [System.Drawing.Color]::FromArgb(240, 240, 240)

# Title label
$titleLabel = New-Object System.Windows.Forms.Label
$titleLabel.Location = New-Object System.Drawing.Point(20, 20)
$titleLabel.Size = New-Object System.Drawing.Size(560, 40)
$titleLabel.Text = "🎬 YOUTUBE VIDEO DOWNLOADER"
$titleLabel.Font = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
$titleLabel.TextAlign = "MiddleCenter"
$form.Controls.Add($titleLabel)

# URL label
$urlLabel = New-Object System.Windows.Forms.Label
$urlLabel.Location = New-Object System.Drawing.Point(20, 80)
$urlLabel.Size = New-Object System.Drawing.Size(560, 20)
$urlLabel.Text = "Paste URL video YouTube:"
$urlLabel.Font = New-Object System.Drawing.Font("Arial", 10)
$form.Controls.Add($urlLabel)

# URL textbox
$urlTextBox = New-Object System.Windows.Forms.TextBox
$urlTextBox.Location = New-Object System.Drawing.Point(20, 105)
$urlTextBox.Size = New-Object System.Drawing.Size(560, 30)
$urlTextBox.Font = New-Object System.Drawing.Font("Arial", 10)
$form.Controls.Add($urlTextBox)

# Quality label
$qualityLabel = New-Object System.Windows.Forms.Label
$qualityLabel.Location = New-Object System.Drawing.Point(20, 145)
$qualityLabel.Size = New-Object System.Drawing.Size(200, 20)
$qualityLabel.Text = "Chất lượng:"
$qualityLabel.Font = New-Object System.Drawing.Font("Arial", 10)
$form.Controls.Add($qualityLabel)

# Quality combobox
$qualityComboBox = New-Object System.Windows.Forms.ComboBox
$qualityComboBox.Location = New-Object System.Drawing.Point(20, 170)
$qualityComboBox.Size = New-Object System.Drawing.Size(200, 30)
$qualityComboBox.DropDownStyle = "DropDownList"
$qualityComboBox.Items.AddRange(@("best", "1080p", "720p", "480p", "360p"))
$qualityComboBox.SelectedIndex = 0
$qualityComboBox.Font = New-Object System.Drawing.Font("Arial", 10)
$form.Controls.Add($qualityComboBox)

# Download button
$downloadButton = New-Object System.Windows.Forms.Button
$downloadButton.Location = New-Object System.Drawing.Point(200, 220)
$downloadButton.Size = New-Object System.Drawing.Size(200, 40)
$downloadButton.Text = "📥 TẢI VIDEO"
$downloadButton.Font = New-Object System.Drawing.Font("Arial", 12, [System.Drawing.FontStyle]::Bold)
$downloadButton.BackColor = [System.Drawing.Color]::FromArgb(76, 175, 80)
$downloadButton.ForeColor = [System.Drawing.Color]::White
$downloadButton.FlatStyle = "Flat"
$form.Controls.Add($downloadButton)

# Status label
$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.Location = New-Object System.Drawing.Point(20, 280)
$statusLabel.Size = New-Object System.Drawing.Size(560, 60)
$statusLabel.Text = "Sẵn sàng tải video..."
$statusLabel.Font = New-Object System.Drawing.Font("Arial", 9)
$statusLabel.TextAlign = "MiddleCenter"
$form.Controls.Add($statusLabel)

# Download button click event
$downloadButton.Add_Click({
        $url = $urlTextBox.Text.Trim()
    
        if ([string]::IsNullOrWhiteSpace($url)) {
            [System.Windows.Forms.MessageBox]::Show("Vui lòng nhập URL video!", "Lỗi", "OK", "Warning")
            return
        }
    
        if ($url -notmatch "youtube\.com|youtu\.be") {
            [System.Windows.Forms.MessageBox]::Show("URL không hợp lệ! Vui lòng nhập link YouTube.", "Lỗi", "OK", "Warning")
            return
        }
    
        $quality = $qualityComboBox.SelectedItem
        $statusLabel.Text = "⏳ Đang tải video... Vui lòng đợi!"
        $statusLabel.ForeColor = [System.Drawing.Color]::Blue
        $form.Refresh()
    
        try {
            # Run download script
            $scriptPath = Join-Path $PSScriptRoot "download_simple.py"
            $process = Start-Process -FilePath "python" -ArgumentList "`"$scriptPath`" `"$url`" --quality $quality" -NoNewWindow -Wait -PassThru
        
            if ($process.ExitCode -eq 0) {
                $statusLabel.Text = "✅ TẢI XUỐNG THÀNH CÔNG! File đã lưu tại: .\output_download\"
                $statusLabel.ForeColor = [System.Drawing.Color]::Green
            
                # Ask to open folder
                $result = [System.Windows.Forms.MessageBox]::Show("Tải xuống thành công!`n`nMở thư mục chứa file?", "Thành công", "YesNo", "Information")
                if ($result -eq "Yes") {
                    Start-Process "explorer.exe" -ArgumentList (Join-Path $PSScriptRoot "output_download")
                }
            
                # Clear URL
                $urlTextBox.Clear()
            }
            else {
                $statusLabel.Text = "❌ LỖI! Vui lòng kiểm tra URL hoặc kết nối Internet."
                $statusLabel.ForeColor = [System.Drawing.Color]::Red
            }
        }
        catch {
            $statusLabel.Text = "❌ LỖI: $_"
            $statusLabel.ForeColor = [System.Drawing.Color]::Red
        }
    })

# Enable paste with Ctrl+V
$urlTextBox.Add_KeyDown({
        if ($_.Control -and $_.KeyCode -eq "V") {
            $urlTextBox.Paste()
        }
    })

# Show form
$form.ShowDialog()
