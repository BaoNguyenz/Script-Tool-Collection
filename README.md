# 🛠️ Script Tools Collection

A collection of 4 powerful Python tools for media processing and content creation.

## 📦 Tools Overview

| Tool | Purpose | Environment | Key Features |
|------|---------|-------------|--------------|
| [**YouTube Downloader GUI**](#-youtube-downloader-gui) | Download audio/video with modern GUI | `youtube_dl` | MP3/FLAC/1080p/720p, Real-time progress |
| [**Remove Background**](#-remove-background-images) | AI background removal | `rembg_tool` | GPU accelerated, Batch processing |
| [**Subtitle Generator**](#-subtitle-generator) | Generate & translate subtitles | `subtitle_generator` | EN transcription, VI translation |

---

## 🚀 Quick Start

### Prerequisites

- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- NVIDIA GPU (optional, for GPU-accelerated tools)

### Installation

#### 1. YouTube Downloader GUI

```powershell
# Navigate to YouTube Downloader GUI
cd e:\Script\Download_youtube_gui

# Create environment
conda env create -f environment.yml

# Activate environment
conda activate youtube_dl

# Launch GUI
python youtube_downloader_gui.py

# Or double-click launcher
Launch_YouTube_Downloader.bat
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

### 🖥️ YouTube Downloader GUI

**Location**: `Download_youtube_gui/`  
**Environment**: `youtube_dl`

**Features**:
- **🎵 Audio Mode**: MP3, FLAC, WAV, M4A, OPUS (up to 320kbps)
- **🎬 Video Mode**: MP4 (best, 1080p, 720p, 480p, 360p)
- **🎨 Modern UI**: Dark mode interface with CustomTkinter
- **📊 Real-time Progress**: Visual progress bar with speed/ETA
- **🖱️ Easy to Use**: No command line needed, point and click
- **⚙️ Quality Selection**: Dropdown menus for format and quality

**Quick Start**:

```powershell
# Setup (one-time)
cd Download_youtube_gui
conda env create -f environment.yml
conda activate youtube_dl

# Launch GUI
python youtube_downloader_gui.py

# Or double-click
Launch_YouTube_Downloader.bat
```

**How to Use**:
1. Select mode: 🎵 Audio or 🎬 Video
2. Paste YouTube URL
3. Choose format and quality from dropdowns
4. Select output directory
5. Click Download button
6. Watch real-time progress

📄 **Full Guide**: [Download_youtube_gui/README_GUI.md](Download_youtube_gui/README_GUI.md)

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
| `youtube_dl` | YouTube Downloader GUI | yt-dlp, ffmpeg, customtkinter | ❌ No |
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
├── Download_youtube_gui/
│   ├── environment.yml               # Conda environment
│   ├── README_GUI.md                 # GUI documentation
│   ├── youtube_downloader_gui.py    # Main GUI application
│   └── Launch_YouTube_Downloader.bat # Quick launcher
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
