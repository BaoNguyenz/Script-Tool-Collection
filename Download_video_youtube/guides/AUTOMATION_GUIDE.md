# 🎬 TỰ ĐỘNG HÓA DOWNLOAD VIDEO YOUTUBE

Tôi đã tạo **3 phương án** để bạn tải video YouTube CỰC KỲ ĐƠN GIẢN - chỉ cần paste URL!

---

## 🚀 KHUYẾN NGHỊ: Dùng Auto_Download.ps1 (Dễ nhất)

### Cách dùng:

1. **Double-click** file [`Auto_Download.ps1`](./Auto_Download.ps1)
2. Paste URL video
3. Chọn chất lượng (hoặc Enter = best)
4. **XONG!**

Sau khi download xong, bạn có thể:
- Tiếp tục paste URL mới → Tải tiếp
- Gõ `exit` → Thoát

**Video sẽ không đóng** - bạn có thể tải liên tục nhiều video!

---

## 🎯 CÁC PHƯƠNG ÁN

### 1. Auto_Download.ps1 - Interactive Loop ⭐ KHUYẾN NGHỊ

**File:** [`Auto_Download.ps1`](./Auto_Download.ps1)

**Đặc điểm:**
- ✅ CỰC KỲ ĐƠN GIẢN
- ✅ Tải liên tục nhiều video
- ✅ Chọn chất lượng ngay trong script
- ✅ Tự động mở folder sau khi tải

**Cách dùng:**
```powershell
# Double-click file Auto_Download.ps1
# Hoặc chạy trong PowerShell:
.\Auto_Download.ps1
```

---

### 2. Quick_Download.bat - Batch File

**File:** [`Quick_Download.bat`](./Quick_Download.bat)

**Đặc điểm:**
- ✅ Đơn giản nhất (chỉ double-click)
- ✅ Không cần mở PowerShell
- ✅ Tải liên tục

**Cách dùng:**
```
Double-click Quick_Download.bat
```

---

### 3. YouTube_Downloader_GUI.ps1 - Giao diện đồ họa

**File:** [`YouTube_Downloader_GUI.ps1`](./YouTube_Downloader_GUI.ps1)

**Đặc điểm:**
- ✅ Giao diện đẹp, dễ dùng
- ✅ Dropdown chọn chất lượng
- ✅ Button click để tải
- ✅ Hiển thị status realtime

**Cách dùng:**
```powershell
# Double-click file YouTube_Downloader_GUI.ps1
# Hoặc:
.\YouTube_Downloader_GUI.ps1
```

**Screenshot:**
```
┌─────────────────────────────────────────┐
│   🎬 YOUTUBE VIDEO DOWNLOADER           │
├─────────────────────────────────────────┤
│ Paste URL video YouTube:                │
│ ┌─────────────────────────────────────┐ │
│ │ https://www.youtube.com/watch?v=... │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Chất lượng:                             │
│ ┌──────────┐                            │
│ │ best  ▼ │                            │
│ └──────────┘                            │
│                                         │
│        ┌──────────────────┐             │
│        │  📥 TẢI VIDEO    │             │
│        └──────────────────┘             │
│                                         │
│       Sẵn sàng tải video...             │
└─────────────────────────────────────────┘
```

---

## 🎯 SO SÁNH

| Phương án | Độ dễ | Tính năng | Giao diện | Khuyến nghị |
|-----------|-------|-----------|-----------|-------------|
| **Auto_Download.ps1** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Terminal | ✅ **Tốt nhất cho đa số** |
| Quick_Download.bat | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Terminal | Đơn giản nhất |
| YouTube_Downloader_GUI.ps1 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | GUI đồ họa | Cho người thích giao diện |

---

## 📖 HƯỚNG DẪN CHI TIẾT

### Auto_Download.ps1 (Khuyến nghị)

**Bước 1:** Double-click `Auto_Download.ps1`

**Bước 2:** Paste URL (Ctrl+V)
```
📺 Paste URL video: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Bước 3:** Chọn chất lượng (Enter = best)
```
📊 Chọn chất lượng:
   [1] best (mặc định)
   [2] 1080p
   [3] 720p
Chọn: 1
```

**Bước 4:** Đợi tải xong
```
✅ THÀNH CÔNG!
Mở thư mục? (Y/N): Y
```

**Bước 5:** Tiếp tục tải video khác hoặc gõ `exit`

---

### Quick_Download.bat

**Bước 1:** Double-click `Quick_Download.bat`

**Bước 2:** Paste URL
```
Paste URL video: https://www.youtube.com/watch?v=VIDEO_ID
```

**Bước 3:** Đợi tải xong

**Bước 4:** Chọn tải tiếp (Y) hoặc thoát (N)

---

### YouTube_Downloader_GUI.ps1

**Bước 1:** Double-click `YouTube_Downloader_GUI.ps1`

**Bước 2:** Cửa sổ GUI hiện ra

**Bước 3:** Paste URL vào textbox

**Bước 4:** Chọn quality từ dropdown

**Bước 5:** Click nút **"📥 TẢI VIDEO"**

**Bước 6:** Đợi download xong → Popup hỏi mở folder

---

## ⚙️ Cấu hình nâng cao

### Thay đổi thư mục lưu mặc định

Edit file script và đổi:
```powershell
# Trong Auto_Download.ps1 hoặc các file khác
# Tìm dòng:
& python $scriptPath $url --quality $quality

# Thay bằng:
& python $scriptPath $url --quality $quality --output "D:\Videos"
```

### Tạo Desktop Shortcut

**Cách 1: Kéo thả**
- Kéo file `.ps1` hoặc `.bat` lên Desktop
- Windows tự tạo shortcut

**Cách 2: Thủ công**
1. Right-click Desktop → New → Shortcut
2. Browse đến file `.ps1` hoặc `.bat`
3. Đặt tên: "YouTube Downloader"
4. Done!

---

## 🆘 Troubleshooting

**Lỗi: "Cannot run script"**

PowerShell bị chặn execution policy:
```powershell
# Mở PowerShell Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Chạy lại script
```

**Lỗi: "python not found"**

Python chưa trong PATH:
```powershell
# Thêm Python vào PATH
# Hoặc edit script, thay 'python' bằng đường dẫn đầy đủ:
& "C:\Users\VU\anaconda3\python.exe" $scriptPath ...
```

**Lỗi: "ffmpeg not found"**

Xem: [`INSTALL_FFMPEG.md`](./INSTALL_FFMPEG.md)

---

## 💡 Tips & Tricks

### Tip 1: Pin vào Taskbar

Kéo shortcut vào Taskbar → Click 1 cái là mở!

### Tip 2: Hotkey

Right-click shortcut → Properties → Shortcut key → Chọn phím tắt (VD: Ctrl+Alt+Y)

### Tip 3: Tải playlist

Paste URL playlist vào bất kỳ script nào → Tải hết tất cả video!

---

## 🎯 TÓM TẮT

**Cách NHANH NHẤT:**
1. Double-click `Auto_Download.ps1`
2. Paste URL
3. Enter
4. XONG!

**Không cần:**
- ❌ Gõ lệnh
- ❌ Mở terminal thủ công
- ❌ Nhớ syntax
- ❌ Code gì cả

**Chỉ cần:**
- ✅ Copy URL
- ✅ Paste vào script
- ✅ Đợi download

Đơn giản vậy thôi! 🎉
