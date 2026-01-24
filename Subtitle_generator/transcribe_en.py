#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
English Subtitle Generator
Pipeline: Transcribe (EN) → Refine → Adjust Timing
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Tuple
import stable_whisper
from subtitle_utils import adjust_continuous_timing

# Configuration
INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"

# Supported video/audio formats
SUPPORTED_FORMATS = {
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm',  # Video
    '.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma'   # Audio
}

# Whisper settings
MODEL_NAME = "large-v3"
LANGUAGE = "en"
DEVICE = "cuda"  # Will auto-fallback to CPU if CUDA not available

# Timing settings
TIMING_GAP_MS = 10  # Gap between subtitles in milliseconds


def print_banner():
    """Print script banner"""
    print("=" * 70)
    print("  English Subtitle Generator")
    print("  Pipeline: Transcribe (EN) → Refine → Adjust Timing")
    print(f"  Model: {MODEL_NAME} | Language: English")
    print("=" * 70)
    print()


def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Output directory: {OUTPUT_DIR}")


def get_input_files() -> List[Path]:
    """Scan input directory for supported video/audio files"""
    if not INPUT_DIR.exists():
        print(f"[ERROR] Input directory not found: {INPUT_DIR}")
        print("[INFO] Please create 'input/' folder and add your video/audio files.")
        return []
    
    files = [
        f for f in INPUT_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_FORMATS
    ]
    
    return sorted(files)


def load_model():
    """Load Whisper model"""
    print("\n" + "=" * 70)
    print("[STEP 1/3] Loading Whisper model...")
    print("=" * 70)
    print(f"[INFO] Model: {MODEL_NAME}")
    print(f"[INFO] Device: {DEVICE}")
    print("[INFO] Precision: FP16 (auto when using CUDA)")
    print("[INFO] This may take a few minutes on first run (downloading model)...")
    
    try:
        model = stable_whisper.load_model(
            name=MODEL_NAME,
            device=DEVICE
        )
        print("[SUCCESS] Model loaded successfully!")
        return model
    except RuntimeError as e:
        if "CUDA" in str(e):
            print("[WARNING] CUDA not available, falling back to CPU...")
            model = stable_whisper.load_model(
                name=MODEL_NAME,
                device="cpu"
            )
            print("[SUCCESS] Model loaded on CPU!")
            return model
        else:
            raise


def transcribe_file(model, input_file: Path) -> Tuple[bool, float, Path]:
    """
    Transcribe a single file to English subtitle
    
    Returns:
        (success: bool, duration: float, output_file: Path)
    """
    print(f"\n[PROCESSING] {input_file.name}")
    
    start_time = time.time()
    en_output = OUTPUT_DIR / f"{input_file.stem}_en.srt"
    
    try:
        # STEP 1: Transcribe
        print("[STEP 1/3] Transcribing (English)...")
        result = model.transcribe(
            audio=str(input_file),
            language=LANGUAGE,
            
            # Quality settings
            word_timestamps=True,
            beam_size=5,
            best_of=5,
            temperature=0.0,
            
            # Context awareness
            condition_on_previous_text=True,
            patience=1.5,
            
            # VAD (Voice Activity Detection)
            vad=True,
            suppress_silence=True,
            
            # Thresholds
            no_speech_threshold=0.5,
            compression_ratio_threshold=2.2,
            logprob_threshold=-0.8,
            
            # Regroup for better segments
            regroup=True,
        )
        
        # STEP 2: Refine timestamps
        print("[STEP 2/3] Refining timestamps...")
        model.refine(
            audio=str(input_file),
            result=result,
            rel_prob_decrease=0.3,
            abs_prob_decrease=0.05,
            word_level=True,
            precision=0.1,
            inplace=True
        )
        
        # Save English subtitle
        result.to_srt_vtt(
            str(en_output),
            word_level=False
        )
        
        # STEP 3: Adjust timing for continuous display
        print(f"[STEP 3/3] Adjusting timing (gap={TIMING_GAP_MS}ms)...")
        adjust_continuous_timing(str(en_output), gap_ms=TIMING_GAP_MS)
        
        duration = time.time() - start_time
        print(f"[OUTPUT] {en_output.name}")
        print(f"[SUCCESS] Completed in {duration:.2f} seconds")
        return True, duration, en_output
        
    except Exception as e:
        duration = time.time() - start_time
        print(f"[ERROR] Failed after {duration:.2f} seconds")
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False, duration, en_output


def main():
    """Main execution function"""
    print_banner()
    
    # Ensure output directory exists
    ensure_output_dir()
    
    # Get input files
    print("\n" + "=" * 70)
    print("[SCANNING] Looking for video/audio files in input directory...")
    print("=" * 70)
    input_files = get_input_files()
    
    if not input_files:
        print("[ERROR] No supported video/audio files found in 'input/' directory!")
        print(f"[INFO] Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"[INFO] Found {len(input_files)} file(s):")
    
    # Check which files already have EN subtitles
    files_to_process = []
    for i, f in enumerate(input_files, 1):
        en_output = OUTPUT_DIR / f"{f.stem}_en.srt"
        if en_output.exists():
            print(f"  {i}. {f.name} - SKIP (EN subtitle exists)")
        else:
            print(f"  {i}. {f.name} - PENDING")
            files_to_process.append(f)
    
    if not files_to_process:
        print("\n[INFO] All files have already been transcribed!")
        print("[INFO] Delete *_en.srt files from 'output/' to reprocess them.")
        input("\nPress Enter to exit...")
        sys.exit(0)
    
    print(f"\n[INFO] {len(files_to_process)} file(s) to process")
    
    # Load Whisper model
    model = load_model()
    
    # Process each file
    print("\n" + "=" * 70)
    print(f"[STEP 2/3] Processing {len(files_to_process)} file(s)...")
    print("=" * 70)
    print()
    
    results = []
    total_start = time.time()
    
    for i, input_file in enumerate(files_to_process, 1):
        print(f"\n{'=' * 70}")
        print(f"[FILE {i}/{len(files_to_process)}]")
        print(f"{'=' * 70}")
        
        success, duration, output_file = transcribe_file(model, input_file)
        results.append((input_file.name, success, duration))
    
    # Print summary
    total_duration = time.time() - total_start
    print("\n" + "=" * 70)
    print("  PROCESSING COMPLETE!")
    print("=" * 70)
    
    successful = sum(1 for _, success, _ in results if success)
    failed = len(results) - successful
    
    print(f"\n[SUMMARY]")
    print(f"  Total files: {len(results)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total time: {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)")
    
    if successful > 0:
        avg_time = sum(d for _, s, d in results if s) / successful
        print(f"  Average time per file: {avg_time:.2f} seconds")
    
    print(f"\n[OUTPUT] English subtitles saved to: {OUTPUT_DIR}")
    
    # Show detailed results
    if results:
        print("\n[DETAILED RESULTS]")
        for filename, success, duration in results:
            status = "✓ SUCCESS" if success else "✗ FAILED"
            print(f"  {status} - {filename} ({duration:.2f}s)")
    
    print("\n" + "=" * 70)
    print("[NEXT STEP] Run 'python translate_vi.py' or 'python translate_vi_qwen.py' to translate to Vietnamese")
    print("=" * 70)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Process interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
