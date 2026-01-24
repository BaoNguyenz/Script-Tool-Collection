# Background Removal Tool

A simple, powerful tool for removing image backgrounds using AI with **GPU acceleration** support.

## ✨ Features

- 🚀 **GPU Accelerated** - Uses CUDA for 10x faster processing
- 📁 **Batch Processing** - Process single images, multiple images, or entire folders
- 🎯 **High Quality** - Uses state-of-the-art AI model (U2-Net)
- 📊 **Progress Tracking** - Real-time progress bars and statistics
- 🔄 **Structure Preservation** - Maintains folder structure in output
- 💾 **PNG Output** - Transparent backgrounds preserved

## 📋 Requirements

- NVIDIA GPU with CUDA support (optional, will fall back to CPU)
- Conda or Miniconda

## 🚀 Quick Start

### 1. Create Conda Environment

```powershell
cd e:\Script\Remove_background_images
conda env create -f environment.yml
conda activate rembg_tool
```

### 2. Add Images to Input Folder

Place your images (or folders containing images) in the `input` folder:

```
Remove_background_images/
├── input/
│   ├── photo1.jpg
│   ├── photo2.png
│   └── my_folder/
│       └── photo3.jpg
```

### 3. Run the Tool

```powershell
python remove_bg.py
```

### 4. Get Results

Processed images will be in the `output` folder with transparent backgrounds:

```
Remove_background_images/
├── output/
│   ├── photo1.png
│   ├── photo2.png
│   └── my_folder/
│       └── photo3.png
```

## 📖 Supported Formats

**Input**: PNG, JPG, JPEG, BMP, WEBP  
**Output**: PNG (with transparency)

## 🎯 Usage Examples

### Process Single Image

```powershell
# Place one image in input/
input/
└── portrait.jpg

# Run script
python remove_bg.py

# Result
output/
└── portrait.png  # Background removed!
```

### Process Multiple Images

```powershell
# Place multiple images in input/
input/
├── image1.jpg
├── image2.jpg
└── image3.png

# Run script
python remove_bg.py

# Result
output/
├── image1.png
├── image2.png
└── image3.png
```

### Process Folder with Subfolders

```powershell
# Place folder with images in input/
input/
└── products/
    ├── category1/
    │   ├── item1.jpg
    │   └── item2.jpg
    └── category2/
        └── item3.jpg

# Run script
python remove_bg.py

# Result (structure preserved!)
output/
└── products/
    ├── category1/
    │   ├── item1.png
    │   └── item2.png
    └── category2/
        └── item3.png
```

## ⚡ Performance

### GPU vs CPU Speed Comparison

| Device | Images/sec | 1000 images |
|--------|------------|-------------|
| NVIDIA RTX 3060 (GPU) | ~10-15 | ~1-2 min |
| Intel i7 (CPU) | ~1-2 | ~8-15 min |

**💡 Tip**: GPU processing is **10x faster** than CPU!

## 🔧 Troubleshooting

### GPU Not Detected

**Symptom**: Script shows "Device: CPU" even though you have NVIDIA GPU

**Solutions**:
1. **Check CUDA Installation**:
   ```powershell
   nvidia-smi  # Should show your GPU
   ```

2. **Reinstall CUDA-enabled ONNX Runtime**:
   ```powershell
   pip uninstall onnxruntime onnxruntime-gpu
   pip install onnxruntime-gpu
   ```

3. **Check CUDA Version Compatibility**:
   - ONNX Runtime GPU requires CUDA 11.x or 12.x
   - Download from: https://developer.nvidia.com/cuda-downloads

### "No module named 'rembg'"

**Solution**:
```powershell
conda activate rembg_tool
pip install rembg[gpu]
```

### Out of Memory (GPU)

**Solution**: Process fewer images at a time, or use CPU mode:
```powershell
# Uninstall GPU version
pip uninstall onnxruntime-gpu

# Install CPU version
pip install onnxruntime
```

### Low Quality Results

**Tips**:
- Use high-resolution input images (at least 1024px)
- Ensure good contrast between subject and background
- Avoid very complex backgrounds

## 🛠️ Advanced Configuration

### Use Different AI Model

Edit `remove_bg.py` to use different models:

```python
from rembg import remove

# Default: u2net (best quality)
output = remove(input_image)

# Fast mode: u2netp (faster, slightly lower quality)
output = remove(input_image, model_name='u2netp')

# Human portraits: isnet-general-use
output = remove(input_image, model_name='isnet-general-use')
```

### Process Only Specific Formats

Edit `utils.py`:

```python
# Only process PNG and JPG
SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg'}
```

## 📊 Output Information

The script provides detailed statistics:

```
Processing Summary:
✅ Successful: 150
❌ Failed:     0
📁 Total:      150

⏱️  Average time per image: 0.8s
⏱️  Total processing time:  2m 5.0s

💾 Total input size:  245.50 MB
💾 Total output size: 189.20 MB
📉 Size change: 77.1%
```

## 🔍 Project Structure

```
Remove_background_images/
├── input/              # Place your images here
├── output/             # Processed images appear here
├── remove_bg.py        # Main script
├── utils.py            # Utility functions
├── environment.yml     # Conda environment
└── README.md          # This file
```

## 🤝 Similar Tools

This tool follows the same workflow as the Subtitle Generator:
- `e:\Script\Subtitle_generator` - Generate and translate subtitles
- `e:\Script\Download_video_youtube` - Download YouTube videos
- `e:\Script\Remove_background_images` - Remove image backgrounds

## 📝 License

Free to use for personal and commercial projects.

## 🙏 Credits

- **rembg**: https://github.com/danielgatis/rembg
- **U2-Net Model**: https://github.com/xuebinqin/U-2-Net
- **ONNX Runtime**: https://onnxruntime.ai/

---

**Made with ❤️ for fast and easy background removal**
