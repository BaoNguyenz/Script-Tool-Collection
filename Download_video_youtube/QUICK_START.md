# QUICK START GUIDE

## 🚀 3 Bước Đơn Giản

### Bước 1: Chuẩn Bị (Làm 1 Lần)

```powershell
# Cài yt-dlp
pip install yt-dlp

# Cài ffmpeg (xem INSTALL_FFMPEG.md)
```

### Bước 2: Tải Video

**Double-click:**
```
START_Downloader.bat
```

### Bước 3: Paste URL và Enter

```
[VIDEO] Paste URL video: https://www.youtube.com/watch?v=VIDEO_ID
[QUALITY] Chon chat luong: 1
```

**XONG!** Video lưu tại: `output_download/`

---

## 📋 Command Line

```powershell
# Tải video best quality
python download_simple.py "URL"

# Chọn chất lượng
python download_simple.py "URL" --quality 720p

# Chỉ định folder
python download_simple.py "URL" --output "D:/Videos"
```

---

## 🎯 Chọn Quality

| Option | Quality | Khi nào dùng |
|--------|---------|--------------|
| `best` | Tốt nhất | Khuyến nghị |
| `1080p` | Full HD | Màn hình lớn |
| `720p` | HD | Cân bằng |
| `480p` | SD | Tiết kiệm |

---

## ⚡ Tips

- **Playlist:** Paste URL playlist → Tải hết
- **Shorts:** Hỗ trợ YouTube Shorts
- **Automation:** Dùng `START_Downloader.bat` cho nhiều video

---

Xem thêm: [README.md](../README.md)
