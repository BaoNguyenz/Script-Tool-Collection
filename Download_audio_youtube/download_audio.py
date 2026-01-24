"""
YouTube Audio Downloader - Professional Quality
Download nhac/audio tu YouTube voi chat luong cao nhat

Features:
- Nhieu format: MP3, WAV, FLAC, ALAC, OPUS, M4A
- Chat luong cao nhat (lossless)
- Download 1 hoac nhieu file cung luc
- Batch download tu file text

Usage:
    python download_audio.py "URL"
    python download_audio.py "URL" --format flac
    python download_audio.py --batch urls.txt
"""

import argparse
import sys
from pathlib import Path
from yt_dlp import YoutubeDL
from typing import List


def download_audio(url: str, output_format: str = "mp3", quality: str = "best", 
                   output_dir: str = "./output_audio") -> bool:
    """
    Download audio tu YouTube voi chat luong cao
    
    Args:
        url: URL cua video YouTube
        output_format: Format audio ('mp3', 'flac', 'wav', 'alac', 'opus', 'm4a')
        quality: Chat luong ('best', '320', '256', '192')
        output_dir: Thu muc luu file
        
    Returns:
        True neu thanh cong, False neu that bai
    """
    # Tao thu muc output
    Path(output_dir).mkdir(exist_ok=True)
    
    # Quality mapping
    quality_map = {
        'best': '0',      # Best available
        '320': '320K',    # 320 kbps
        '256': '256K',    # 256 kbps  
        '192': '192K',    # 192 kbps
        '128': '128K',    # 128 kbps
    }
    
    audio_quality = quality_map.get(quality, '0')
    
    # Format-specific config
    format_config = {
        'mp3': {
            'codec': 'mp3',
            'quality': audio_quality,
            'preferredquality': audio_quality,
        },
        'flac': {
            'codec': 'flac',
            'quality': '0',  # Lossless
        },
        'wav': {
            'codec': 'wav',
            'quality': '0',  # Lossless
        },
        'alac': {
            'codec': 'alac',
            'quality': '0',  # Lossless (Apple Lossless)
        },
        'opus': {
            'codec': 'opus',
            'quality': audio_quality,
        },
        'm4a': {
            'codec': 'aac',
            'quality': audio_quality,
        }
    }
    
    config = format_config.get(output_format, format_config['mp3'])
    
    # yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'quiet': False,
        'no_warnings': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': config['codec'],
            'preferredquality': config.get('preferredquality', '0'),
        }],
        'postprocessor_args': [
            '-ar', '48000',  # 48kHz sample rate
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,
    }
    
    try:
        print("\n" + "=" * 70)
        print(f"[AUDIO] Dang tai: {url}")
        print(f"[FORMAT] {output_format.upper()}")
        print(f"[QUALITY] {quality} ({audio_quality if audio_quality != '0' else 'Best/Lossless'})")
        print(f"[OUTPUT] {output_dir}")
        print("=" * 70 + "\n")
        
        with YoutubeDL(ydl_opts) as ydl:
            # Get info
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            duration = info.get('duration_string', 'N/A')
            uploader = info.get('uploader', 'Unknown')
            
            print(f"[TITLE] {title}")
            print(f"[CHANNEL] {uploader}")
            print(f"[DURATION] {duration}")
            print("=" * 70 + "\n")
            
            # Download
            print("[DOWNLOADING] Please wait...")
            ydl.download([url])
            
            print("\n" + "=" * 70)
            print("[SUCCESS] DOWNLOAD THANH CONG!")
            print("=" * 70)
            print(f"[FILE] {output_dir}/{title}.{output_format}")
            print("=" * 70 + "\n")
            
            return True
            
    except Exception as e:
        print("\n" + "=" * 70)
        print("[ERROR] LOI KHI TAI AUDIO")
        print("=" * 70)
        print(f"Chi tiet: {str(e)}\n")
        
        if "ffmpeg" in str(e).lower():
            print("[FIX] Cai ffmpeg:")
            print("  Download: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")
            print("  Xem: INSTALL_FFMPEG.md\n")
        else:
            print("[SUGGEST]")
            print("  - Kiem tra URL")
            print("  - Kiem tra Internet")
            print("  - Thu format khac: --format m4a")
            print("  - Update: pip install --upgrade yt-dlp\n")
        
        return False


def batch_download(file_path: str, output_format: str = "mp3", 
                   quality: str = "best", output_dir: str = "./output_audio") -> None:
    """
    Download nhieu audio tu file text chua danh sach URLs
    
    Args:
        file_path: Duong dan file text chua URLs (moi dong 1 URL)
        output_format: Format audio
        quality: Chat luong
        output_dir: Thu muc luu
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not urls:
            print("[ERROR] File rong hoac khong co URL hop le!")
            return
        
        print("\n" + "=" * 70)
        print(f"[BATCH] Tim thay {len(urls)} URLs")
        print("=" * 70 + "\n")
        
        success_count = 0
        fail_count = 0
        
        for i, url in enumerate(urls, 1):
            print(f"\n>>> [{i}/{len(urls)}] Processing: {url}")
            
            if download_audio(url, output_format, quality, output_dir):
                success_count += 1
            else:
                fail_count += 1
            
            print("-" * 70)
        
        # Summary
        print("\n" + "=" * 70)
        print("[BATCH SUMMARY]")
        print("=" * 70)
        print(f"Total: {len(urls)}")
        print(f"Success: {success_count}")
        print(f"Failed: {fail_count}")
        print("=" * 70 + "\n")
        
    except FileNotFoundError:
        print(f"[ERROR] Khong tim thay file: {file_path}")
    except Exception as e:
        print(f"[ERROR] Loi doc file: {e}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="YouTube Audio Downloader - Professional Quality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Vi du su dung:

  # Download MP3 320kbps (khuyến nghị cho đa số)
  python download_audio.py "https://www.youtube.com/watch?v=VIDEO_ID" --format mp3 --quality 320
  
  # Download FLAC (lossless - audiophile)
  python download_audio.py "URL" --format flac
  
  # Download WAV (lossless - cho production)
  python download_audio.py "URL" --format wav
  
  # Download ALAC (Apple Lossless)
  python download_audio.py "URL" --format alac
  
  # Batch download tu file
  python download_audio.py --batch urls.txt --format mp3 --quality 320

Format ho tro:
  mp3  - Universal, tuong thich tot nhat (320kbps = gan lossless)
  flac - Lossless, audiophile favorite (file lon)
  wav  - Lossless, uncompressed (file rat lon, dung cho production)
  alac - Apple Lossless (cho iOS/Mac)
  opus - Modern codec, chat luong cao, file nho
  m4a  - AAC, tot cho Apple devices

Quality (chi ap dung cho lossy formats):
  best - Tot nhat co san
  320  - 320 kbps (cao nhat cho MP3)
  256  - 256 kbps
  192  - 192 kbps
  128  - 128 kbps

File format cho batch download (urls.txt):
  https://www.youtube.com/watch?v=VIDEO_ID1
  https://www.youtube.com/watch?v=VIDEO_ID2
  # Comment
  https://www.youtube.com/watch?v=VIDEO_ID3
        """
    )
    
    # Single or batch mode
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        'url',
        nargs='?',
        type=str,
        help='URL cua video YouTube'
    )
    group.add_argument(
        '--batch',
        type=str,
        metavar='FILE',
        help='File text chua danh sach URLs (moi dong 1 URL)'
    )
    
    parser.add_argument(
        '--format',
        type=str,
        default='mp3',
        choices=['mp3', 'flac', 'wav', 'alac', 'opus', 'm4a'],
        help='Dinh dang audio (mac dinh: mp3)'
    )
    
    parser.add_argument(
        '--quality',
        type=str,
        default='best',
        choices=['best', '320', '256', '192', '128'],
        help='Chat luong audio (mac dinh: best)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='./output_audio',
        help='Thu muc luu file audio (mac dinh: ./output_audio)'
    )
    
    args = parser.parse_args()
    
    # Batch or single download
    if args.batch:
        batch_download(args.batch, args.format, args.quality, args.output)
    else:
        # Validate URL
        if not args.url or ('youtube.com' not in args.url and 'youtu.be' not in args.url):
            print("\n[ERROR] URL khong hop le!")
            print("URL phai la link YouTube, vi du:")
            print("  https://www.youtube.com/watch?v=VIDEO_ID")
            print("  https://youtu.be/VIDEO_ID\n")
            sys.exit(1)
        
        success = download_audio(args.url, args.format, args.quality, args.output)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
