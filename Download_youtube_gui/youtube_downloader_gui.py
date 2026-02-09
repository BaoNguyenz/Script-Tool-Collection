"""
YouTube Downloader GUI - Modern Interface
Download audio and video from YouTube with a beautiful, easy-to-use interface
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from pathlib import Path
from yt_dlp import YoutubeDL
import sys
import os
import re


def get_ffmpeg_path():
    """Get FFmpeg path - works for both source and bundled .exe"""
    if getattr(sys, 'frozen', False):
        # Running as bundled .exe
        base_path = Path(sys._MEIPASS)
        ffmpeg_dir = base_path / 'ffmpeg'
        if ffmpeg_dir.exists():
            return str(ffmpeg_dir)
    return None  # Use system PATH


def is_valid_youtube_url(url):
    """Check if URL is a valid YouTube URL (supports all formats)"""
    youtube_patterns = [
        r'(https?://)?(www\.)?youtube\.com/watch\?v=',
        r'(https?://)?(www\.)?youtube\.com/shorts/',
        r'(https?://)?(www\.)?youtube\.com/embed/',
        r'(https?://)?(www\.)?youtube\.com/live/',
        r'(https?://)?(www\.)?youtube\.com/v/',
        r'(https?://)?youtu\.be/',
        r'(https?://)?(www\.)?music\.youtube\.com/watch\?v=',
        r'(https?://)?(m\.)?youtube\.com/watch\?v=',
    ]
    for pattern in youtube_patterns:
        if re.search(pattern, url):
            return True
    return False

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class YouTubeDownloaderGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("YouTube Downloader")
        self.window.geometry("700x600")
        self.window.resizable(False, False)
        
        # Default settings
        self.download_mode = "audio"  # audio or video
        self.output_path = str(Path.home() / "Downloads")
        self.is_downloading = False
        self.cancel_download = False  # Flag to cancel download
        self.current_ydl = None  # Reference to current YoutubeDL instance
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup all UI components"""
        # Title
        title = ctk.CTkLabel(
            self.window,
            text="🎬 YouTube Downloader",
            font=("Roboto", 28, "bold")
        )
        title.pack(pady=20)
        
        # Mode selection frame
        mode_frame = ctk.CTkFrame(self.window)
        mode_frame.pack(pady=10, padx=40, fill="x")
        
        mode_label = ctk.CTkLabel(mode_frame, text="Mode:", font=("Roboto", 14))
        mode_label.pack(side="left", padx=10)
        
        self.mode_var = ctk.StringVar(value="audio")
        
        audio_radio = ctk.CTkRadioButton(
            mode_frame,
            text="🎵 Audio",
            variable=self.mode_var,
            value="audio",
            command=self.on_mode_change,
            font=("Roboto", 13)
        )
        audio_radio.pack(side="left", padx=10)
        
        video_radio = ctk.CTkRadioButton(
            mode_frame,
            text="🎬 Video",
            variable=self.mode_var,
            value="video",
            command=self.on_mode_change,
            font=("Roboto", 13)
        )
        video_radio.pack(side="left", padx=10)
        
        # URL input
        url_frame = ctk.CTkFrame(self.window)
        url_frame.pack(pady=10, padx=40, fill="x")
        
        url_label = ctk.CTkLabel(url_frame, text="YouTube URL:", font=("Roboto", 13))
        url_label.pack(anchor="w", padx=10, pady=5)
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="https://www.youtube.com/watch?v=...",
            height=40,
            font=("Roboto", 12)
        )
        self.url_entry.pack(fill="x", padx=10, pady=5)
        
        # Format and Quality selection
        options_frame = ctk.CTkFrame(self.window)
        options_frame.pack(pady=10, padx=40, fill="x")
        
        # Format dropdown
        format_label = ctk.CTkLabel(options_frame, text="Format:", font=("Roboto", 13))
        format_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.format_var = ctk.StringVar(value="mp3")
        self.format_dropdown = ctk.CTkOptionMenu(
            options_frame,
            values=["mp3", "flac", "wav", "m4a"],
            variable=self.format_var,
            width=150,
            font=("Roboto", 12)
        )
        self.format_dropdown.grid(row=0, column=1, padx=10, pady=5)
        
        # Quality dropdown
        quality_label = ctk.CTkLabel(options_frame, text="Quality:", font=("Roboto", 13))
        quality_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        self.quality_var = ctk.StringVar(value="best")
        self.quality_dropdown = ctk.CTkOptionMenu(
            options_frame,
            values=["best", "320", "256", "192"],
            variable=self.quality_var,
            width=150,
            font=("Roboto", 12)
        )
        self.quality_dropdown.grid(row=0, column=3, padx=10, pady=5)
        
        # Output directory
        output_frame = ctk.CTkFrame(self.window)
        output_frame.pack(pady=10, padx=40, fill="x")
        
        output_label = ctk.CTkLabel(output_frame, text="Save to:", font=("Roboto", 13))
        output_label.pack(anchor="w", padx=10, pady=5)
        
        output_path_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        output_path_frame.pack(fill="x", padx=10, pady=5)
        
        self.output_entry = ctk.CTkEntry(
            output_path_frame,
            height=35,
            font=("Roboto", 11)
        )
        self.output_entry.insert(0, self.output_path)
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ctk.CTkButton(
            output_path_frame,
            text="Browse",
            width=100,
            command=self.browse_output,
            font=("Roboto", 12)
        )
        browse_btn.pack(side="left")
        
        # Buttons frame (Download + Cancel)
        buttons_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        buttons_frame.pack(pady=15, padx=40, fill="x")
        
        # Download button
        self.download_btn = ctk.CTkButton(
            buttons_frame,
            text="⬇ Download",
            height=45,
            font=("Roboto", 16, "bold"),
            command=self.start_download,
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        )
        self.download_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="✖ Cancel",
            height=45,
            font=("Roboto", 16, "bold"),
            command=self.cancel_current_download,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            state="disabled"
        )
        self.cancel_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.window, height=20)
        self.progress_bar.pack(pady=10, padx=40, fill="x")
        self.progress_bar.set(0)
        
        # Status text
        self.status_text = ctk.CTkTextbox(
            self.window,
            height=150,
            font=("Consolas", 11),
            wrap="word"
        )
        self.status_text.pack(pady=10, padx=40, fill="both", expand=True)
        self.log("Ready to download 🚀")
        
    def on_mode_change(self):
        """Handle mode change between audio and video"""
        mode = self.mode_var.get()
        self.download_mode = mode
        
        if mode == "audio":
            # Audio mode options
            self.format_dropdown.configure(values=["mp3", "flac", "wav", "m4a", "opus"])
            self.format_var.set("mp3")
            self.quality_dropdown.configure(values=["best", "320", "256", "192", "128"])
            self.quality_var.set("320")
        else:
            # Video mode options
            self.format_dropdown.configure(values=["mp4"])
            self.format_var.set("mp4")
            self.quality_dropdown.configure(values=["best", "1080p", "720p", "480p", "360p"])
            self.quality_var.set("best")
            
        self.log(f"Mode changed to: {mode.upper()}")
    
    def browse_output(self):
        """Browse for output directory"""
        folder = filedialog.askdirectory(initialdir=self.output_path)
        if folder:
            self.output_path = folder
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, folder)
            self.log(f"Output directory: {folder}")
    
    def log(self, message):
        """Add message to status text"""
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")
    
    def progress_hook(self, d):
        """Progress callback for yt-dlp"""
        # Check for cancel
        if self.cancel_download:
            raise Exception("Download cancelled by user")
        
        if d['status'] == 'downloading':
            try:
                # Calculate progress percentage
                if 'total_bytes' in d:
                    progress = d['downloaded_bytes'] / d['total_bytes']
                elif 'total_bytes_estimate' in d:
                    progress = d['downloaded_bytes'] / d['total_bytes_estimate']
                else:
                    progress = 0
                
                # Update progress bar
                self.progress_bar.set(progress)
                
                # Speed and ETA
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                
                if speed and eta:
                    speed_mb = speed / 1024 / 1024
                    self.window.title(f"Downloading... {progress*100:.1f}% | {speed_mb:.1f} MB/s | ETA: {eta}s")
                    
            except Exception as e:
                if self.cancel_download:
                    raise
                
        elif d['status'] == 'finished':
            self.progress_bar.set(1.0)
            self.window.title("YouTube Downloader")
    
    def download_worker(self):
        """Worker thread for downloading"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            self.reset_download_state()
            return
        
        if not is_valid_youtube_url(url):
            messagebox.showerror("Error", "Invalid YouTube URL\n\nSupported formats:\n• youtube.com/watch?v=...\n• youtu.be/...\n• youtube.com/shorts/...\n• music.youtube.com/...")
            self.reset_download_state()
            return
        
        output_dir = self.output_entry.get()
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        
        try:
            self.log(f"\n{'='*50}")
            self.log(f"Starting download...")
            self.log(f"URL: {url}")
            self.log(f"Mode: {self.download_mode.upper()}")
            
            if self.download_mode == "audio":
                self.download_audio(url, output_dir)
            else:
                self.download_video(url, output_dir)
                
        except Exception as e:
            if self.cancel_download:
                self.log("\n⚠️ Download cancelled by user")
            else:
                self.log(f"\n❌ Error: {str(e)}")
                messagebox.showerror("Download Error", str(e))
        finally:
            self.reset_download_state()
            self.cancel_btn.configure(text="✖ Cancel")
    
    def download_audio(self, url, output_dir):
        """Download audio"""
        format_codec = self.format_var.get()
        quality = self.quality_var.get()
        
        quality_map = {'best': '0', '320': '320K', '256': '256K', '192': '192K', '128': '128K'}
        audio_quality = quality_map.get(quality, '0')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'noplaylist': True,  # Download single video only, not playlist
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format_codec,
                'preferredquality': audio_quality,
            }],
            'progress_hooks': [self.progress_hook],
        }
        
        # Add FFmpeg path if bundled
        ffmpeg_path = get_ffmpeg_path()
        if ffmpeg_path:
            ydl_opts['ffmpeg_location'] = ffmpeg_path
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            self.log(f"Title: {title}")
            self.log(f"Format: {format_codec.upper()}")
            self.log(f"Quality: {quality}")
            self.log(f"\nDownloading...")
            
            ydl.download([url])
            
        self.log(f"\n✅ Download complete!")
        self.log(f"Saved to: {output_dir}")
        messagebox.showinfo("Success", f"Download complete!\n\nSaved to:\n{output_dir}")
    
    def download_video(self, url, output_dir):
        """Download video"""
        quality = self.quality_var.get()
        
        quality_map = {
            'best': 'bestvideo+bestaudio/best',
            '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
            '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
        }
        
        video_format = quality_map.get(quality, 'best')
        
        ydl_opts = {
            'format': video_format,
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'noplaylist': True,  # Download single video only, not playlist
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'prefer_ffmpeg': True,
            'progress_hooks': [self.progress_hook],
        }
        
        # Add FFmpeg path if bundled
        ffmpeg_path = get_ffmpeg_path()
        if ffmpeg_path:
            ydl_opts['ffmpeg_location'] = ffmpeg_path
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            self.log(f"Title: {title}")
            self.log(f"Quality: {quality}")
            self.log(f"\nDownloading...")
            
            ydl.download([url])
            
        self.log(f"\n✅ Download complete!")
        self.log(f"Saved to: {output_dir}")
        messagebox.showinfo("Success", f"Download complete!\n\nSaved to:\n{output_dir}")
    
    def start_download(self):
        """Start download in separate thread"""
        if self.is_downloading:
            return
        
        self.is_downloading = True
        self.cancel_download = False
        self.download_btn.configure(state="disabled", text="⏳ Downloading...")
        self.cancel_btn.configure(state="normal")
        
        # Run download in thread to prevent UI freeze
        thread = threading.Thread(target=self.download_worker, daemon=True)
        thread.start()
    
    def reset_download_state(self):
        """Reset UI state after download completes or is cancelled"""
        self.is_downloading = False
        self.cancel_download = False
        self.current_ydl = None
        self.download_btn.configure(state="normal", text="⬇ Download")
        self.cancel_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.window.title("YouTube Downloader")
    
    def cancel_current_download(self):
        """Cancel the current download"""
        if self.is_downloading:
            self.cancel_download = True
            self.log("\n⚠️ Cancelling download...")
            self.cancel_btn.configure(state="disabled", text="Cancelling...")
            
            # Try to abort the YoutubeDL instance
            if self.current_ydl:
                try:
                    self.current_ydl.params['abort'] = True
                except:
                    pass
    
    def run(self):
        """Run the application"""
        self.window.mainloop()


if __name__ == "__main__":
    app = YouTubeDownloaderGUI()
    app.run()
