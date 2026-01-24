# 🎵 YouTube Audio Downloader

Download high-quality audio from YouTube with multiple format support.

## ✨ Features

- **Multiple Formats**: MP3, FLAC, WAV, ALAC, OPUS, M4A
- **Quality Options**: 320kbps, 256kbps, 192kbps, best/lossless
- **Batch Download**: Process multiple URLs from text file
- **Professional Quality**: Up to lossless audio extraction

## 🔧 Setup

### Shared Environment (youtube_dl)

This tool shares an environment with [Download_video_youtube](../Download_video_youtube/).

```powershell
# From Script directory
cd e:\Script

# Create environment (only once)
conda env create -f youtube_dl_environment.yml

# Activate
conda activate youtube_dl
```

## 🚀 Usage

### Single Download

```powershell
# MP3 320kbps (recommended for most users)
python download_audio.py "https://www.youtube.com/watch?v=VIDEO_ID" --format mp3 --quality 320

# FLAC lossless (audiophile quality)
python download_audio.py "URL" --format flac

# WAV uncompressed (production use)
python download_audio.py "URL" --format wav

# ALAC (Apple Lossless for iOS/Mac)
python download_audio.py "URL" --format alac
```

### Batch Download

Create a text file `urls.txt`:
```
https://www.youtube.com/watch?v=VIDEO_ID1
https://www.youtube.com/watch?v=VIDEO_ID2
# This is a comment
https://www.youtube.com/watch?v=VIDEO_ID3
```

Run batch download:
```powershell
python download_audio.py --batch urls.txt --format mp3 --quality 320
```

## 📋 Format Guide

| Format | Quality | File Size | Best For |
|--------|---------|-----------|----------|
| **MP3** | 320kbps | Medium | Universal compatibility |
| **FLAC** | Lossless | Large | Audiophile listening |
| **WAV** | Lossless | Very Large | Production/editing |
| **ALAC** | Lossless | Large | Apple ecosystem |
| **OPUS** | Variable | Small | Modern codec, good quality |
| **M4A** | 256kbps | Medium | Apple devices |

## 🎯 Quality Settings

- `best` - Highest quality available (default)
- `320` - 320 kbps (highest for MP3)
- `256` - 256 kbps
- `192` - 192 kbps
- `128` - 128 kbps

**Note**: Lossless formats (FLAC, WAV, ALAC) always use maximum quality regardless of setting.

## 📂 Output

Files are saved to `output_audio/` by default:
```
output_audio/
├── Song Title 1.mp3
├── Song Title 2.flac
└── Song Title 3.wav
```

Custom output directory:
```powershell
python download_audio.py "URL" --output "D:/Music"
```

## 🔧 Troubleshooting

### ffmpeg not found

**Solution**:
```powershell
conda activate youtube_dl
conda install -c conda-forge ffmpeg
```

### yt-dlp update needed

```powershell
conda activate youtube_dl
pip install --upgrade yt-dlp
```

### Download fails

- Check URL is valid YouTube link
- Verify internet connection
- Try different format/quality
- Update yt-dlp (see above)

## 📖 Full Documentation

See main [Script README](../README.md) for:
- Environment setup details
- Other tools in collection
- Common troubleshooting

---

**Part of the Script Tools Collection** | [All Tools](../README.md)
