# 🛠️ Script Tools Collection

A collection of 4 powerful Python tools for media processing and content creation.

## 📦 Tools Overview

| Tool | Purpose | Environment | Key Features |
|------|---------|-------------|--------------|
| [**YouTube Downloader**](#-youtube-downloader) | Download audio/video with CLI or GUI | `youtube_dl` | MP3/FLAC/1080p/720p, GUI + CLI |
| [**Remove Background**](#-remove-background-images) | AI background removal | `rembg_tool` | GPU accelerated, Batch processing |
| [**Subtitle Generator**](#-subtitle-generator) | Generate & translate subtitles | `subtitle_generator` | EN transcription, VI translation |

---

## 🚀 Quick Start

### Prerequisites

- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- NVIDIA GPU (optional, for GPU-accelerated tools)

### Installation

#### 1. YouTube Downloader (Audio + Video + GUI)

```powershell
# Navigate to YouTube Downloader
cd e:\Script\YouTube_Downloader

# Create environment
conda env create -f environment.yml

# Activate environment
conda activate youtube_dl

# Launch GUI (easiest)
cd gui
python youtube_downloader_gui.py

# Or use CLI
cd cli
python download_audio.py "YOUTUBE_URL" --format mp3 --quality 320
python download_video.py "YOUTUBE_URL" --quality 1080p
```

#### 2. Remove Background Tool

```powershell
cd e:\Script\Remove_background_images

# Create environment
conda env create -f environment.yml
conda activate rembg_tool

# Place images in input/ folder, then run:
python remove_bg.py
```

#### 3. Subtitle Generator

```powershell
cd e:\Script\Subtitle_generator

# Create environment
conda env create -f environment.yml
conda activate subtitle_generator

# Place video/audio in input/ folder, then:
python transcribe_en.py       # Generate English subtitles
python translate_vi_qwen.py   # Translate to Vietnamese
```

---

## 📖 Detailed Documentation

### 🎬 YouTube Downloader

**Location**: `YouTube_Downloader/`  
**Environment**: `youtube_dl`

**Features**:
- **🎵 Audio**: MP3, FLAC, WAV, ALAC, OPUS, M4A (up to 320kbps)
- **🎬 Video**: MP4 (best, 1080p, 720p, 480p, 360p)
- **🖥️ GUI**: Modern dark mode interface with real-time progress
- **⌨️ CLI**: Command-line for batch downloads and automation
- **📦 Batch**: Download multiple files from text file

**Quick Start**:

```powershell
# Setup (one-time)
cd YouTube_Downloader
conda env create -f environment.yml
conda activate youtube_dl

# Launch GUI (recommended for beginners)
cd gui
python youtube_downloader_gui.py

# Or use CLI (advanced users)
cd cli
python download_audio.py "URL" --format mp3 --quality 320
python download_video.py "URL" --quality 1080p
python download_audio.py --batch urls.txt
```

📄 **Full Guide**: [YouTube_Downloader/README.md](YouTube_Downloader/README.md)

---

### 🖼️ Remove Background (Images)

**Location**: `Remove_background_images/`  
**Environment**: `rembg_tool`

**Features**:
- **GPU accelerated** (CUDA support)
- AI-powered background removal (U2-Net)
- Batch processing
- Preserves folder structure
- PNG output with transparency

**Performance**:
- GPU (CUDA): ~1.0s/image ⚡
- CPU: ~17s/image

**Usage**:
```powershell
# 1. Place images in input/ folder
# 2. Run tool:
python remove_bg.py

# 3. Check output/ folder for results
```

📄 **Full Guide**: [Remove_background_images/README.md](Remove_background_images/README.md)

---

### 📝 Subtitle Generator

**Location**: `Subtitle_generator/`  
**Environment**: `subtitle_generator`

**Features**:
- **English transcription** using Whisper large-v3
- **Vietnamese translation** with 2 options:
  - **Qwen2.5** (offline, high quality, context-aware)
  - **NLLB** (offline, fast, basic quality)
- Continuous timing adjustment
- Word-level refinement

**Workflow**:
```powershell
# Step 1: Generate English subtitles
python transcribe_en.py
# Output: video_en.srt

# Step 2: Translate to Vietnamese
python translate_vi_qwen.py    # High quality (recommended)
# OR
python translate_vi.py         # Fast (basic quality)
# Output: video_vi.srt
```

📄 **Full Guide**: [Subtitle_generator/README.md](Subtitle_generator/README.md)

---

## 🔧 Environment Setup Summary

| Environment | Tools | Dependencies | GPU Required |
|-------------|-------|--------------|--------------|
| `youtube_dl` | YouTube Downloader (CLI + GUI) | yt-dlp, ffmpeg, customtkinter | ❌ No |
| `rembg_tool` | Remove Background | rembg, CUDA 12.1, cuDNN | ✅ Optional (17x faster) |
| `subtitle_generator` | Subtitle Generator | PyTorch, stable-ts, CUDA 12.1 | ✅ Recommended |

**Why 3 separate environments?**
- Different CUDA requirements (PyTorch vs ONNX Runtime)
- Avoid dependency conflicts
- Optimized for each use case

---

## 💡 Common Troubleshooting

### ffmpeg not found
```powershell
# Using conda (recommended)
conda install -c conda-forge ffmpeg

# Or download from: https://www.gyan.dev/ffmpeg/builds/
```

### GPU not detected
```powershell
# Check GPU
nvidia-smi

# For Remove Background Tool, see:
#   Remove_background_images/README.md → Troubleshooting

# For Subtitle Generator, PyTorch should auto-detect GPU
```

### yt-dlp errors
```powershell
# Update yt-dlp
pip install --upgrade yt-dlp
```

---

## 📂 Project Structure

```
e:\Script\
├── README.md                          # This file
│
├── YouTube_Downloader/
│   ├── environment.yml               # Environment config
│   ├── README.md                     # YouTube downloader docs
│   ├── cli/                          # Command-line tools
│   │   ├── download_audio.py
│   │   └── download_video.py
│   ├── gui/                          # GUI application
│   │   └── youtube_downloader_gui.py
│   ├── output_audio/                 # Audio downloads
│   └── output_video/                 # Video downloads
│
├── Remove_background_images/
│   ├── environment.yml
│   ├── remove_bg.py
│   ├── README.md
│   └── input/ & output/
│
└── Subtitle_generator/
    ├── environment.yml
    ├── transcribe_en.py
    ├── translate_vi_qwen.py
    ├── README.md
    └── input/ & output/
```

---

## 📝 License

Free to use for personal and commercial projects.

## 🙏 Credits

- **yt-dlp**: https://github.com/yt-dlp/yt-dlp
- **rembg**: https://github.com/danielgatis/rembg
- **stable-ts**: https://github.com/jianfch/stable-ts
- **Qwen2.5**: https://github.com/QwenLM/Qwen2.5
- **NLLB**: Meta AI's No Language Left Behind

---

**Made with ❤️ for content creators and media processors**
