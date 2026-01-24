"""
Script hỗ trợ xuất cookies từ trình duyệt cho yt-dlp
Sử dụng để tải video YouTube members-only
"""

import subprocess
import sys
from pathlib import Path

def export_cookies(browser: str = "chrome", output_file: str = "youtube_cookies.txt"):
    """
    Xuất cookies từ trình duyệt sử dụng yt-dlp
    
    Args:
        browser: Tên trình duyệt ('chrome', 'firefox', 'edge', 'opera', 'safari')
        output_file: Tên file cookies đầu ra
    """
    try:
        output_path = Path(output_file).absolute()
        
        print(f"Đang xuất cookies từ {browser}...")
        print(f"File sẽ được lưu tại: {output_path}")
        print("=" * 60)
        
        # Lệnh xuất cookies
        cmd = [
            "yt-dlp",
            "--cookies-from-browser", browser,
            "--cookies", str(output_path),
            "https://www.youtube.com"
        ]
        
        # Chạy lệnh
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            if output_path.exists():
                print(f"✓ Xuất cookies thành công!")
                print(f"✓ File cookies: {output_path}")
                print("\nBây giờ bạn có thể sử dụng:")
                print(f'python download_youtube.py --url "YOUR_URL" --cookies "{output_file}"')
            else:
                print("⚠ Lệnh chạy thành công nhưng không tìm thấy file cookies")
                print(f"Stderr: {result.stderr}")
        else:
            print(f"✗ Lỗi khi xuất cookies:")
            print(f"Error: {result.stderr}")
            print("\nGợi ý:")
            print(f"1. Đảm bảo bạn đã đăng nhập {browser}")
            print("2. Đóng tất cả cửa sổ của trình duyệt và thử lại")
            print("3. Thử trình duyệt khác (chrome, firefox, edge)")
            
    except FileNotFoundError:
        print("✗ Không tìm thấy yt-dlp!")
        print("Hãy cài đặt: pip install yt-dlp")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Lỗi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Xuất cookies từ trình duyệt cho yt-dlp",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  # Xuất cookies từ Chrome (mặc định)
  python export_cookies.py
  
  # Xuất cookies từ Firefox
  python export_cookies.py --browser firefox
  
  # Xuất cookies từ Edge
  python export_cookies.py --browser edge
  
  # Chỉ định tên file khác
  python export_cookies.py --output my_cookies.txt
        """
    )
    
    parser.add_argument(
        '--browser',
        type=str,
        default='chrome',
        choices=['chrome', 'firefox', 'edge', 'opera', 'safari', 'chromium', 'brave'],
        help='Trình duyệt cần xuất cookies (mặc định: chrome)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='youtube_cookies.txt',
        help='Tên file cookies đầu ra (mặc định: youtube_cookies.txt)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("XUẤT COOKIES TỪ TRÌNH DUYỆT CHO YT-DLP")
    print("=" * 60)
    print()
    
    export_cookies(args.browser, args.output)
