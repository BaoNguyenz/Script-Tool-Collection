"""
YouTube Video Downloader - SIMPLE VERSION
Tải video YouTube CÔNG KHAI đơn giản - KHÔNG CẦN cookies

Sử dụng:
    python download_simple.py "https://www.youtube.com/watch?v=VIDEO_ID"
    python download_simple.py "https://www.youtube.com/watch?v=VIDEO_ID" --quality 720p
"""

import argparse
import sys
from yt_dlp import YoutubeDL
from pathlib import Path


def download_video(url: str, quality: str = "best", output_dir: str = "./SXTK") -> bool:
    """
    Tải video YouTube công khai - CỰC KỲ ĐƠN GIẢN
    
    Args:
        url: URL của video YouTube
        quality: Chất lượng video ('best', '1080p', '720p', '480p', '360p')
        output_dir: Thư mục lưu video
        
    Returns:
        True nếu thành công, False nếu thất bại
    """
    # Tạo thư mục output nếu chưa có
    Path(output_dir).mkdir(exist_ok=True)
    
    # Mapping chất lượng đơn giản
    quality_map = {
        'best': 'bestvideo+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
    }
    
    video_format = quality_map.get(quality, 'best')
    
    # Cấu hình yt-dlp - ĐƠN GIẢN, HIỆU QUẢ
    ydl_opts = {
        'format': video_format,
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
    }
    
    try:
        print("\n" + "=" * 60)
        print(f"🎬 Tải video: {url}")
        print(f"📊 Chất lượng: {quality}")
        print(f"📂 Lưu tại: {output_dir}")
        print("=" * 60 + "\n")
        
        with YoutubeDL(ydl_opts) as ydl:
            # Lấy thông tin video
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown')
            duration = info.get('duration_string', 'N/A')
            
            print(f"📹 Tên: {video_title}")
            print(f"⏱️  Thời lượng: {duration}")
            print("=" * 60 + "\n")
            
            # Tải video
            ydl.download([url])
            
            print("\n" + "=" * 60)
            print("✅ TẢI XUỐNG THÀNH CÔNG!")
            print("=" * 60)
            print(f"📂 File đã lưu tại: {output_dir}")
            print("=" * 60 + "\n")
            
            return True
            
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ LỖI KHI TẢI VIDEO")
        print("=" * 60)
        print(f"Chi tiết: {str(e)}\n")
        
        # Gợi ý
        if "members" in str(e).lower() or "private" in str(e).lower():
            print("💡 Video này có thể là:")
            print("   • Video riêng tư (Private)")
            print("   • Video chỉ dành cho thành viên (Members-only)")
            print("")
            print("→ Để tải video members-only, dùng:")
            print("  python download_members_only.py --url \"URL\" --cookies \"cookies.txt\"")
            print("")
        else:
            print("💡 Gợi ý:")
            print("   • Kiểm tra URL có đúng không")
            print("   • Kiểm tra kết nối Internet")
            print("   • Thử lại sau vài phút")
            print("   • Cập nhật yt-dlp: pip install --upgrade yt-dlp")
            print("")
        
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Tải video YouTube công khai - CỰC KỲ ĐƠN GIẢN",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:

  # Tải video chất lượng tốt nhất (mặc định)
  python download_simple.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  
  # Tải video chất lượng 720p
  python download_simple.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --quality 720p
  
  # Chỉ định thư mục khác
  python download_simple.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output "D:/Videos"

Lưu ý:
  • Script này CHỈ dành cho video CÔNG KHAI (public)
  • KHÔNG CẦN cookies hay đăng nhập
  • Nếu video là members-only, dùng: download_members_only.py
        """
    )
    
    parser.add_argument(
        'url',
        type=str,
        help='URL của video YouTube cần tải'
    )
    
    parser.add_argument(
        '--quality',
        type=str,
        default='best',
        choices=['best', '1080p', '720p', '480p', '360p'],
        help='Chất lượng video (mặc định: best)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='./output_download',
        help='Thư mục lưu video (mặc định: ./output_download)'
    )
    
    args = parser.parse_args()
    
    # Kiểm tra URL
    if not args.url or 'youtube.com' not in args.url and 'youtu.be' not in args.url:
        print("\n❌ URL không hợp lệ!")
        print("URL phải là link YouTube, ví dụ:")
        print("  https://www.youtube.com/watch?v=VIDEO_ID")
        print("  https://youtu.be/VIDEO_ID\n")
        sys.exit(1)
    
    # Tải video
    success = download_video(args.url, args.quality, args.output)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
