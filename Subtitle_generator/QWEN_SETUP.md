# Qwen2.5 với Ollama - Setup Guide

## ✨ Ưu điểm Qwen2.5:

- ✅ **100% Offline**: Không cần API, không cần internet
- ✅ **Context-aware**: LLM hiểuđối thoại, chọn đại từ đúng
- ✅ **Free unlimited**: Không giới hạn
- ✅ **Privacy**: Data không rời khỏi máy bạn
- ✅ **Quality**: Gần bằng GPT-4/Gemini cho tiếng Việt
- ✅ **Fast với GPU**: ~3-5s per batch

## 📥 Bước 1: Cài Ollama

### Windows:

1. Download: **https://ollama.ai/download/windows**
2. Chạy installer `OllamaSetup.exe`
3. Cài đặt theo hướng dẫn
4. Ollama sẽ **tự động chạy** sau khi cài

### Verify:

Mở PowerShell:
```powershell
ollama --version
```

Phải hiển thị version → OK!

## 🤖 Bước 2: Pull Qwen2.5 Model

### Option 1: Qwen2.5 7B (Khuyến nghị)
**Size**: ~4.7GB  
**VRAM**: ~6GB  
**Speed**: Fast  
**Quality**: Rất tốt  

```bash
ollama pull qwen2.5:7b
```

### Option 2: Qwen2.5 14B (Chất lượng cao hơn)
**Size**: ~9GB  
**VRAM**: ~12GB  
**Speed**: Slower  
**Quality**: Xuất sắc  

```bash
ollama pull qwen2.5:14b
```

### Option 3: Qwen2.5 3B (Nhanh, VRAM thấp)
**Size**: ~2GB  
**VRAM**: ~3GB  
**Speed**: Very fast  
**Quality**: Tốt  

```bash
ollama pull qwen2.5:3b
```

**Khuyến nghị**: Dùng **7B** - balance tốt nhất!

⏱️ **Lưu ý**: Download mất 5-15 phút tùy tốc độ mạng.

## ⚙️ Bước 3: Config Model (Optional)

Nếu muốn dùng model khác, edit `translate_vi_qwen.py` dòng 18:

```python
QWEN_MODEL = "qwen2.5:7b"   # Default
# QWEN_MODEL = "qwen2.5:14b"  # Better quality
# QWEN_MODEL = "qwen2.5:3b"   # Faster
```

## 🚀 Bước 4: Chạy Script

```bash
python translate_vi_qwen.py
```

Script sẽ:
1. Check Ollama đang chạy
2. Check model đã pull chưa
3. Dịch từng batch subtitle với context
4. Tạo file `*_vi.srt`

## 📊 Performance

**Video 1 giờ** (~100 subtitles, 20 batches):

| GPU | Time | Note |
|-----|------|------|
| RTX 4090 | ~1-2 min | Very fast |
| RTX 3060 | ~2-3 min | Fast |
| GTX 1660 | ~3-5 min | Good |
| CPU only | ~10-20 min | Slow but works |

## 🔧 Troubleshooting

### "Ollama is not running"
```bash
# Check if Ollama service is running
# Windows: Task Manager → Services → Ollama
# Or restart:
ollama serve
```

### "Model not found"
```bash
# List installed models
ollama list

# Pull missing model
ollama pull qwen2.5:7b
```

### Chậm quá?
- Thử model nhỏ hơn: `qwen2.5:3b`
- Giảm `BATCH_SIZE` trong script xuống 3
- Check GPU có được dùng không

### Out of memory?
- Dùng model nhỏ hơn: `qwen2.5:3b`
- Close apps khác
- Giảm `BATCH_SIZE`

## 🆚 So sánh với các phương pháp khác

| Method | Quality | Pronoun | Offline | Speed | Cost |
|--------|---------|---------|---------|-------|------|
| **Qwen2.5** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ⚡⚡⚡ | Free |
| NLLB | ⭐⭐⭐ | ⭐⭐ | ✅ | ⚡⚡⚡ | Free |
| DeepL API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | ⚡⚡⚡ | 500K |
| Gemini API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ⚡⚡ | 1M |

## 💡 Tips

### Cải thiện chất lượng:
1. **Dùng model lớn hơn** → 14B tốt hơn 7B
2. **Giảm temperature** → Edit script dòng 107: `"temperature": 0.1`
3. **Tăng context** → Edit `BATCH_SIZE` lên 8-10

### Tăng tốc độ:
1. **Dùng model nhỏ** → 3B nhanh gấp đôi
2. **Tăng batch size** → Ít API calls hơn
3. **Ensure GPU** → Check Ollama dùng GPU

## 📝 Model Size vs VRAM

| Model | Model Size | Min VRAM | Ideal VRAM |
|-------|-----------|----------|------------|
| 3B | ~2GB | 3GB | 6GB |
| 7B | ~4.7GB | 6GB | 8GB |
| 14B | ~9GB | 10GB | 12GB |

**Nếu không đủ VRAM** → Ollama tự động dùng CPU (chậm hơn nhưng vẫn work!)

## 🎯 Khuyến nghị

**Best setup**:
- Model: `qwen2.5:7b`
- GPU: RTX 3060 trở lên (8GB+ VRAM)
- Batch size: 5
- Temperature: 0.3

**Cho sẽ kết quả tương đương Gemini/GPT-4 nhưng hoàn toàn OFFLINE!** 🚀
