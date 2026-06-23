#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert Audio files (MP3, WAV, etc.) to Black Screen MP4 Videos
So that subtitles (.srt) can be displayed in VLC Media Player
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Configuration
INPUT_DIR = Path(__file__).parent / "input"

# Supported audio extensions (excluding video formats)
AUDIO_FORMATS = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma'}

def check_ffmpeg() -> bool:
    """Check if ffmpeg is available in the system or environment"""
    return shutil.which("ffmpeg") is not None

def convert_audio_to_mp4(audio_path: Path) -> bool:
    """
    Convert a single audio file to a black screen MP4 video using ffmpeg
    """
    output_path = audio_path.with_suffix(".mp4")
    
    print(f"\n[CONVERTING] {audio_path.name} -> {output_path.name}")
    
    # FFmpeg command to generate a black screen (640x360) matching the audio length
    # Using AAC audio codec for maximum compatibility
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "color=c=black:s=640x360",
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        str(output_path)
    ]
    
    try:
        # Run FFmpeg command silently
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[SUCCESS] Created: {output_path.name}")
            return True
        else:
            print(f"[ERROR] FFmpeg failed for {audio_path.name}")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
        return False

def main():
    print("=" * 70)
    print("  Audio to Black Screen MP4 Converter")
    print("  Purpose: Create MP4 videos from audio files to play with subtitles")
    print("=" * 70)
    
    if not check_ffmpeg():
        print("\n[ERROR] ffmpeg was not found on your system or active Conda environment!")
        print("[INFO] Please make sure you have activated the conda environment:")
        print("       conda activate subtitle_generator")
        input("\nPress Enter to exit...")
        sys.exit(1)
        
    if not INPUT_DIR.exists():
        print(f"\n[ERROR] Input directory not found: {INPUT_DIR}")
        input("\nPress Enter to exit...")
        sys.exit(1)
        
    # Scan for audio files
    audio_files = [
        f for f in INPUT_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in AUDIO_FORMATS
    ]
    
    if not audio_files:
        print(f"\n[INFO] No audio files found in: {INPUT_DIR}")
        print(f"Supported audio formats: {', '.join(sorted(AUDIO_FORMATS))}")
        input("\nPress Enter to exit...")
        sys.exit(0)
        
    print(f"\n[INFO] Found {len(audio_files)} audio file(s) to process:")
    
    files_to_process = []
    for i, f in enumerate(audio_files, 1):
        target_mp4 = f.with_suffix(".mp4")
        if target_mp4.exists():
            print(f"  {i}. {f.name} - SKIP (MP4 already exists)")
        else:
            print(f"  {i}. {f.name} - PENDING")
            files_to_process.append(f)
            
    if not files_to_process:
        print("\n[INFO] All audio files already have corresponding MP4 videos.")
        input("\nPress Enter to exit...")
        sys.exit(0)
        
    print(f"\n[INFO] Start converting {len(files_to_process)} file(s)...")
    
    success_count = 0
    for f in files_to_process:
        if convert_audio_to_mp4(f):
            success_count += 1
            
    print("\n" + "=" * 70)
    print("  CONVERSION PROCESS COMPLETED!")
    print("=" * 70)
    print(f"  Total processed: {len(files_to_process)}")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {len(files_to_process) - success_count}")
    print(f"\n[NEXT STEP] Open the new .mp4 files in VLC and drag-drop the .srt subtitles.")
    print("=" * 70)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Cancelled by user.")
        sys.exit(0)
