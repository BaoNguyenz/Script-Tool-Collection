"""
Script kiểm tra cookies và tải video members-only
Hướng dẫn từng bước để khắc phục lỗi 403 Forbidden
"""

import subprocess
import sys
from pathlib import Path

def test_cookies(cookies_file: str, video_url: str):
    """Kiểm tra xem cookies có hoạt động với video không"""
    
    cookies_path = Path(cookies_file)
    if not cookies_path.exists():
        print(f"❌ Không tìm thấy file cookies: {cookies_file}")
        return False
    
    print("🔍 Đang kiểm tra cookies...")
    print(f"📂 File: {cookies_path.absolute()}")
    print(f"🎬 Video: {video_url}")
    print("=" * 60)
    
    # Test xem có thể lấy thông tin video không
    cmd = [
        "yt-dlp",
        "--cookies", str(cookies_path),
        "--skip-download",  # Chỉ test, không tải
        "--print", "%(title)s | %(duration_string)s | %(availability)s",
        video_url
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Cookies hoạt động!")
            print(f"📹 {result.stdout.strip()}")
            return True
        else:
            print("❌ Cookies KHÔNG hoạt động!")
            print(f"Lỗi: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi test: {e}")
        return False


def download_direct(video_url: str, cookies_file: str, quality: str = "720p"):
    """Tải video trực tiếp bằng yt-dlp (không qua script Python)"""
    
    quality_map = {
        'best': 'bestvideo+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
    }
    
    format_str = quality_map.get(quality, quality)
    output_dir = Path(__file__).parent / "SXTK"
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n🎬 Tải video: {video_url}")
    print(f"📊 Chất lượng: {quality}")
    print(f"📂 Lưu tại: {output_dir}")
    print("=" * 60)
    
    cmd = [
        "yt-dlp",
        "--cookies", cookies_file,
        "--format", format_str,
        "--merge-output-format", "mp4",
        "--fragment-retries", "10",
        "--extractor-retries", "3",
        "--skip-unavailable-fragments",
        "--concurrent-fragments", "4",  # Tải đồng thời 4 fragments
        "--output", str(output_dir / "%(title)s.%(ext)s"),
        "--no-playlist",
        video_url
    ]
    
    print("📥 Đang tải...")
    print(f"💡 Lệnh: {' '.join(cmd)}\n")
    
    try:
        # Chạy trực tiếp, hiển thị output real-time
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("\n✅ Tải xuống thành công!")
            return True
        else:
            print(f"\n❌ Tải xuống thất bại với exit code: {result.returncode}")
            return False
            
    except KeyboardInterrupt:
        print("\n⚠️ Người dùng hủy bỏ")
        return False
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        return False


def print_instructions():
    """In hướng dẫn xuất cookies đúng cách"""
    print("\n" + "=" * 60)
    print("📖 HƯỚNG DẪN XUẤT COOKIES ĐÚNG CÁCH")
    print("=" * 60)
    print("""
⚠️  ĐỂ TẢI VIDEO MEMBERS-ONLY, BẠN PHẢI:

1️⃣  Mở trình duyệt (Chrome/Edge/Firefox)
2️⃣  Đăng nhập YouTube với tài khoản có membership
3️⃣  QUAN TRỌNG: Truy cập video và BẤM PLAY, để video chạy 5-10 giây
4️⃣  TRONG KHI VIDEO ĐANG PHÁT, xuất cookies:

   Cách A - Dùng extension (Dễ nhất):
   ----------------------------------------
   • Cài: https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc
   • Click icon extension → Export
   • Lưu thành: www.youtube.com_cookies.txt

   Cách B - Dùng yt-dlp:
   ----------------------------------------
   • Mở PowerShell MỚI
   • Chạy: yt-dlp --cookies-from-browser chrome --cookies www.youtube.com_cookies.txt "https://www.youtube.com"

5️⃣  Copy file cookies vào thư mục này
6️⃣  Chạy script NGAY (trong 10 phút)

⏱️  Cookies chỉ có hiệu lực 5-15 phút cho video members-only!
    """)
    print("=" * 60 + "\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test cookies và tải video members-only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:

  # Test cookies
  python test_and_download.py --test --cookies "www.youtube.com_cookies.txt" --url "https://www.youtube.com/watch?v=YlH0mw5qIfo"

  # Tải video trực tiếp
  python test_and_download.py --download --cookies "www.youtube.com_cookies.txt" --url "https://www.youtube.com/watch?v=YlH0mw5qIfo" --quality 720p

  # Hiển thị hướng dẫn
  python test_and_download.py --help-cookies
        """
    )
    
    parser.add_argument('--test', action='store_true', help='Test cookies')
    parser.add_argument('--download', action='store_true', help='Tải video')
    parser.add_argument('--help-cookies', action='store_true', help='Hiển thị hướng dẫn xuất cookies')
    parser.add_argument('--cookies', type=str, default='www.youtube.com_cookies.txt', help='File cookies')
    parser.add_argument('--url', type=str, help='URL video')
    parser.add_argument('--quality', type=str, default='720p', choices=['best', '1080p', '720p', '480p', '360p'], help='Chất lượng')
    
    args = parser.parse_args()
    
    if args.help_cookies:
        print_instructions()
        sys.exit(0)
    
    if not args.url and (args.test or args.download):
        print("❌ Thiếu --url")
        parser.print_help()
        sys.exit(1)
    
    if args.test:
        print("\n🧪 CHẠY CHẾ ĐỘ TEST COOKIES")
        print("=" * 60)
        success = test_cookies(args.cookies, args.url)
        if success:
            print("\n✅ Cookies hợp lệ! Bạn có thể tải video.")
            print("💡 Chạy lại với --download để tải video")
        else:
            print("\n❌ Cookies không hợp lệ hoặc đã hết hạn!")
            print_instructions()
        sys.exit(0 if success else 1)
    
    if args.download:
        print("\n📥 CHẠY CHẾ ĐỘ TẢI VIDEO")
        print("=" * 60)
        success = download_direct(args.url, args.cookies, args.quality)
        sys.exit(0 if success else 1)
    
    # Mặc định: hiển thị hướng dẫn
    parser.print_help()
    print_instructions()
