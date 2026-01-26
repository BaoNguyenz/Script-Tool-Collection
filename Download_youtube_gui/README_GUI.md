# YouTube Downloader GUI

Modern, user-friendly graphical interface for downloading YouTube videos and audio.

## ✨ Features

- **🎵 Audio Mode**: Download as MP3, FLAC, WAV, M4A, OPUS
- **🎬 Video Mode**: Download in 1080p, 720p, 480p, 360p
- **📊 Real-time Progress**: Visual progress bar with speed and ETA
- **🎨 Modern UI**: Beautiful dark mode interface with CustomTkinter
- **🖱️ Easy to Use**: No command line needed, point and click
- **📁 Custom Output**: Choose where to save your files

---

## 🖼️ Screenshots

### Audio Download Mode
![Audio Mode](assets/screenshot_audio.png)

### Video Download Mode
![Video Mode](assets/screenshot_video.png)

---

## 🚀 Quick Start

### Installation

```powershell
# Navigate to Script directory
cd Download_youtube_gui

# Update environment (adds GUI dependencies)
conda env create -f environment.yml

# Activate environment
conda activate youtube_dl
```

### Launch GUI

**Option 1: Double-click launcher** (Easiest)
```
Download_youtube_gui\Launch_YouTube_Downloader.bat
```

**Option 2: Command line**
```powershell
conda activate youtube_dl
cd Download_youtube_gui
python youtube_downloader_gui.py
```

---

## 📖 How to Use

### Download Audio

1. **Select Mode**: Choose "🎵 Audio" radio button
2. **Enter URL**: Paste YouTube URL
3. **Choose Format**: Select MP3, FLAC, WAV, etc.
4. **Select Quality**: Choose 320kbps, 256kbps, or best
5. **Set Output**: Browse to select save location
6. **Download**: Click "Download" button
7. **Wait**: Watch progress bar until complete

### Download Video

1. **Select Mode**: Choose "🎬 Video" radio button
2. **Enter URL**: Paste YouTube URL
3. **Choose Quality**: Select 1080p, 720p, 480p, etc.
4. **Set Output**: Browse to select save location
5. **Download**: Click "Download" button
6. **Wait**: Watch progress bar until complete

---

## 🎯 Format Options

### Audio Mode

| Format | Quality Options | File Size | Best For |
|--------|----------------|-----------|----------|
| **MP3** | 320kbps, 256kbps, 192kbps, 128kbps | Medium | Universal compatibility |
| **FLAC** | Lossless | Large | Audiophile quality |
| **WAV** | Lossless | Very Large | Professional editing |
| **M4A** | 256kbps | Medium | Apple devices |
| **OPUS** | Variable | Small | Modern codec |

### Video Mode

| Quality | Resolution | File Size | Best For |
|---------|------------|-----------|----------|
| **1080p** | 1920x1080 | Large | Full HD |
| **720p** | 1280x720 | Medium | HD quality |
| **480p** | 854x480 | Small | Standard quality |
| **360p** | 640x360 | Very Small | Low bandwidth |

---

## 🔧 Features Explained

### Real-time Progress

- **Progress Bar**: Visual representation of download progress
- **Speed**: Current download speed in MB/s
- **ETA**: Estimated time remaining
- **Title Bar**: Shows progress percentage during download

### Status Log

- **Real-time Updates**: See what's happening at each step
- **Error Messages**: Clear, helpful error descriptions
- **Download Info**: Video title, format, quality displayed

### Smart UI

- **Dynamic Options**: Format/quality options change based on mode
- **Thread Safety**: GUI remains responsive during downloads
- **Error Handling**: Validates URLs and shows helpful messages

---

## 🆚 GUI vs Command Line

| Feature | Command Line | GUI App |
|---------|--------------|---------|
| **Ease of Use** | Remember commands | Point and click |
| **URL Input** | Type carefully | Copy & paste |
| **Quality Selection** | Flags like `--quality 720p` | Dropdown menu |
| **Progress** | Text percentage | Visual progress bar |
| **Errors** | Technical messages | User-friendly dialogs |
| **Learning Curve** | Moderate | Instant |

---

## 🔧 Requirements

Installed automatically with `youtube_dl_environment.yml`:

- Python 3.10
- yt-dlp (YouTube downloader)
- customtkinter (Modern UI framework)
- pillow (Image support)
- ffmpeg (Audio/video processing)

---

## 🆘 Troubleshooting

### GUI doesn't launch

```powershell
# Ensure environment is activated
conda activate youtube_dl

# Install missing dependencies
pip install customtkinter pillow

# Try launching directly
python youtube_downloader_gui.py
```

### "Invalid URL" error

- Ensure URL contains `youtube.com` or `youtu.be`
- Example valid URLs:
  - `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
  - `https://youtu.be/dQw4w9WgXcQ`

### ffmpeg errors

```powershell
conda activate youtube_dl
conda install -c conda-forge ffmpeg
```

### Download freezes

- Check internet connection
- Try a different video
- Update yt-dlp: `pip install --upgrade yt-dlp`

---

## 🔄 Updating

```powershell
# Update environment
conda env update -n youtube_dl -f youtube_dl_environment.yml --prune

# Update yt-dlp
conda activate youtube_dl
pip install --upgrade yt-dlp
```

---

## 📂 Project Structure

```
Download_youtube_gui/
├── youtube_downloader_gui.py      # Main GUI application
├── Launch_YouTube_Downloader.bat  # Windows launcher
└── README_GUI.md                  # This file
```

---

## 💡 Tips

1. **Batch Downloads**: Download one at a time for best reliability
2. **Quality**: For audio, 320kbps is near-lossless for most listeners
3. **Storage**: FLAC/WAV files are much larger than MP3
4. **Network**: Faster internet = faster downloads
5. **Playlists**: Not supported yet, download videos individually

---

## 🚀 Future Features (Planned)

- [ ] Batch download queue
- [ ] Playlist support
- [ ] Download history
- [ ] Thumbnail preview
- [ ] Auto-update checker
- [ ] Custom filename templates

---

## 📖 Related Tools

See main [Script README](../README.md) for other tools:
- Command-line audio downloader
- Command-line video downloader
- Background removal tool
- Subtitle generator

---

**Part of the Script Tools Collection** | [All Tools](../README.md)
