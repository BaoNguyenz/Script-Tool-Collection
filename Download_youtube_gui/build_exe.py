"""
Build Script for YouTube Downloader GUI
Packages the application into a standalone .exe with FFmpeg bundled
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def find_ffmpeg():
    """Find FFmpeg binaries from conda environment or system PATH"""
    # Check conda environment first
    conda_prefix = os.environ.get('CONDA_PREFIX')
    if conda_prefix:
        ffmpeg_dir = Path(conda_prefix) / 'Library' / 'bin'
        ffmpeg_exe = ffmpeg_dir / 'ffmpeg.exe'
        ffprobe_exe = ffmpeg_dir / 'ffprobe.exe'
        
        if ffmpeg_exe.exists() and ffprobe_exe.exists():
            print(f"[OK] Found FFmpeg in conda: {ffmpeg_dir}")
            return ffmpeg_dir, [ffmpeg_exe, ffprobe_exe]
    
    # Check system PATH
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        ffmpeg_dir = Path(ffmpeg_path).parent
        ffmpeg_exe = ffmpeg_dir / 'ffmpeg.exe'
        ffprobe_exe = ffmpeg_dir / 'ffprobe.exe'
        
        if ffmpeg_exe.exists() and ffprobe_exe.exists():
            print(f"[OK] Found FFmpeg in PATH: {ffmpeg_dir}")
            return ffmpeg_dir, [ffmpeg_exe, ffprobe_exe]
    
    print("[ERROR] FFmpeg not found!")
    print("Please install FFmpeg: conda install -c conda-forge ffmpeg")
    sys.exit(1)


def find_customtkinter():
    """Find CustomTkinter package location for assets"""
    try:
        import customtkinter
        ctk_path = Path(customtkinter.__file__).parent
        print(f"[OK] Found CustomTkinter: {ctk_path}")
        return ctk_path
    except ImportError:
        print("[ERROR] CustomTkinter not found!")
        print("Please install: pip install customtkinter")
        sys.exit(1)


def build_exe():
    """Build the executable using PyInstaller"""
    print("\n" + "="*50)
    print("  YouTube Downloader - Build Script")
    print("="*50 + "\n")
    
    # Find dependencies
    ffmpeg_dir, ffmpeg_files = find_ffmpeg()
    ctk_path = find_customtkinter()
    
    # Prepare PyInstaller command
    script_dir = Path(__file__).parent.resolve()
    main_script = script_dir / "youtube_downloader_gui.py"
    
    if not main_script.exists():
        print(f"[ERROR] Main script not found: {main_script}")
        sys.exit(1)
    
    # Build add-data arguments
    add_data = []
    
    # Add FFmpeg binaries
    for ff_file in ffmpeg_files:
        add_data.append(f'--add-binary={ff_file};ffmpeg')
    
    # Add CustomTkinter assets
    add_data.append(f'--add-data={ctk_path};customtkinter')
    
    # Check for custom icon
    icon_file = script_dir / 'icon.ico'
    icon_arg = []
    if icon_file.exists():
        print(f"[OK] Found custom icon: {icon_file}")
        icon_arg = [f'--icon={icon_file}']
        # Also bundle icon.ico as data so the window icon works when running .exe
        add_data.append(f'--add-data={icon_file};.')
    else:
        print("[INFO] No custom icon found (place 'icon.ico' in project folder to use)")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=YouTubeDownloader',
        '--clean',
        '--noconfirm',
        *icon_arg,
        *add_data,
        str(main_script)
    ]
    
    print("\n[BUILD] Running PyInstaller...")
    print(f"Command: {' '.join(cmd)}\n")
    
    # Run PyInstaller
    result = subprocess.run(cmd, cwd=script_dir)
    
    if result.returncode == 0:
        exe_path = script_dir / 'dist' / 'YouTubeDownloader.exe'
        print("\n" + "="*50)
        print("  BUILD SUCCESSFUL!")
        print("="*50)
        print(f"\n[OK] Executable created: {exe_path}")
        print(f"[OK] File size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        print("\nYou can now distribute YouTubeDownloader.exe")
    else:
        print("\n[ERROR] Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()
