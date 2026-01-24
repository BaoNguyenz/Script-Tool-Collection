# 🎬 YouTube Video Downloader

Download public YouTube videos in various quality options.

## ✨ Features

- **Quality Options**: best, 1080p, 720p, 480p, 360p
- **Auto-merge**: Automatically combines video + audio
- **MP4 Output**: Universal format compatibility
- **Simple & Fast**: No cookies or authentication needed

## 🔧 Setup

### Shared Environment (youtube_dl)

This tool shares an environment with [Download_audio_youtube](../Download_audio_youtube/).

```powershell
# From Script directory
cd e:\Script

# Create environment (only once)
conda env create -f youtube_dl_environment.yml

# Activate
conda activate youtube_dl
```

## 🚀 Usage

### Basic Download

```powershell
# Best quality (default)
python download_simple.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 1080p Full HD
python download_simple.py "URL" --quality 1080p

# 720p HD
python download_simple.py "URL" --quality 720p

# Custom output directory
python download_simple.py "URL" --output "D:/Videos"
```

## 📋 Quality Options

| Quality | Resolution | Best For |
|---------|------------|----------|
| `best` | Highest available | Maximum quality (default) |
| `1080p` | 1920x1080 | Full HD viewing |
| `720p` | 1280x720 | HD, smaller files |
| `480p` | 854x480 | Standard quality |
| `360p` | 640x360 | Low bandwidth |

## ⚠️ Important Notes

### This tool is for PUBLIC videos only

- ✅ Works: Public videos
- ❌ Does NOT work: Private videos, Members-only videos

### For Members-Only Videos

If you need to download members-only content, use:
```powershell
python download_members_only.py --url "URL" --cookies "cookies.txt"
```

See [EXTENSION_GUIDE.md](EXTENSION_GUIDE.md) for cookie extraction instructions.

## 📂 Output

Files are saved to `output_download/` by default:
```
output_download/
├── Video Title 1.mp4
├── Video Title 2.mp4
└── Video Title 3.mp4
```

## 🔧 Troubleshooting

### "Video unavailable" or "Private video"

This typically means:
- Video is private
- Video is members-only
- Video requires authentication

**Solution**: Use `download_members_only.py` with cookies

### ffmpeg not found

```powershell
conda activate youtube_dl
conda install -c conda-forge ffmpeg
```

### yt-dlp errors

```powershell
conda activate youtube_dl
pip install --upgrade yt-dlp
```

### Slow download speed

- Try lower quality: `--quality 720p`
- Check your internet connection
- Try again during off-peak hours

## 📖 Full Documentation

See main [Script README](../README.md) for:
- Environment setup details
- Other tools in collection
- Common troubleshooting

---

**Part of the Script Tools Collection** | [All Tools](../README.md)
