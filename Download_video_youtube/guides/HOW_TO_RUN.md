# Cach Chay File PowerShell (.ps1)

## Van de: Double-click file .ps1 KHONG TU DONG CHAY

Windows **KHONG** tu dong chay file `.ps1` khi double-click vi ly do bao mat.

---

## Giai phap: 3 cach de chay

### Cach 1: DOUBLE-CLICK FILE .BAT (DE NHAT)

**File:** `START_Downloader.bat`

Toi da tao file `.bat` de chay script PowerShell cho ban.

**Cach dung:**
```
Double-click: START_Downloader.bat
```

XONG! File .bat se tu dong chay Auto_Download.ps1

---

### Cach 2: Right-click file .ps1

1. Right-click file `Auto_Download.ps1`
2. Chon: **"Run with PowerShell"**

Neu khong co tuy chon nay:
- Chon "Open with"
- Chon "PowerShell"
- Tick "Always use this app"

---

### Cach 3: Chay trong PowerShell

```powershell
# Mo PowerShell trong thu muc
cd E:\Script\Download_video_youtube

# Chay script
.\Auto_Download.ps1
```

---

## Neu gap loi "Execution Policy"

**Loi:**
```
File cannot be loaded because running scripts is disabled
```

**Giai phap:**

### Option 1: Dung file .BAT (khong can sua gi)
```
Double-click: START_Downloader.bat
```

### Option 2: Mo khoa PowerShell (1 lan duy nhat)

```powershell
# Mo PowerShell Administrator
# Right-click PowerShell icon -> Run as Administrator

# Chay lenh:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Chon: Y (Yes)
```

Sau khi chay lenh nay, file .ps1 se chay binh thuong.

---

## Tom tat

**DE NHAT:**
```
Double-click: START_Downloader.bat
```

Khong can:
- Sua execution policy
- Right-click
- Mo PowerShell thu cong

Chi can double-click file .BAT!
