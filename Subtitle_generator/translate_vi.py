#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vietnamese Translation Script
Translate English subtitles to Vietnamese using NLLB
"""

import sys
from pathlib import Path
from subtitle_utils import get_nllb_translator, translate_subtitle_nllb_cached

# Configuration
OUTPUT_DIR = Path(__file__).parent / "output"

# NLLB settings
NLLB_MODEL = "facebook/nllb-200-distilled-600M"  # Or "facebook/nllb-200-3.3B" for better quality
DEVICE = "cuda"  # Will auto-fallback to CPU if CUDA not available
BATCH_SIZE = 8  # Number of subtitles to translate at once


def print_banner():
    """Print script banner"""
    print("=" * 70)
    print("  Vietnamese Translation")
    print("  EN → VI using NLLB-200")
    print(f"  Model: {NLLB_MODEL.split('/')[-1]}")
    print("=" * 70)
    print()


def get_en_files():
    """Get all English subtitle files"""
    if not OUTPUT_DIR.exists():
        print(f"[ERROR] Output directory not found: {OUTPUT_DIR}")
        return []
    
    en_files = list(OUTPUT_DIR.glob("*_en.srt"))
    return sorted(en_files)


def main():
    """Main execution function"""
    print_banner()
    
    # Get English subtitle files
    print("[SCANNING] Looking for English subtitles...")
    en_files = get_en_files()
    
    if not en_files:
        print("[ERROR] No English subtitle files (*_en.srt) found in 'output/' directory!")
        print("[INFO] Run 'python transcribe_en.py' first to generate English subtitles.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"[INFO] Found {len(en_files)} English subtitle(s):")
    
    # Check which files need translation
    files_to_translate = []
    for i, en_file in enumerate(en_files, 1):
        vi_file = en_file.parent / en_file.name.replace("_en.srt", "_vi.srt")
        if vi_file.exists():
            print(f"  {i}. {en_file.name} - SKIP (VI subtitle exists)")
        else:
            print(f"  {i}. {en_file.name} - PENDING")
            files_to_translate.append(en_file)
    
    if not files_to_translate:
        print("\n[INFO] All files have already been translated!")
        print("[INFO] Delete *_vi.srt files from 'output/' to retranslate them.")
        input("\nPress Enter to exit...")
        sys.exit(0)
    
    print(f"\n[INFO] {len(files_to_translate)} file(s) to translate")
    
    # Load NLLB model
    print("\n" + "=" * 70)
    print("[LOADING] NLLB Translation Model...")
    print("=" * 70)
    print(f"[INFO] Model: {NLLB_MODEL}")
    print(f"[INFO] Device: {DEVICE}")
    print("[INFO] This may take a few minutes on first run (downloading model)...")
    print()
    
    try:
        nllb_translator = get_nllb_translator(NLLB_MODEL, DEVICE)
        print("[SUCCESS] NLLB model loaded!")
    except Exception as e:
        print(f"[ERROR] Failed to load NLLB model: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Translate files
    print("\n" + "=" * 70)
    print(f"[TRANSLATING] Processing {len(files_to_translate)} file(s)...")
    print("=" * 70)
    print()
    
    results = []
    
    for i, en_file in enumerate(files_to_translate, 1):
        vi_file = en_file.parent / en_file.name.replace("_en.srt", "_vi.srt")
        
        print(f"\n{'=' * 70}")
        print(f"[FILE {i}/{len(files_to_translate)}]")
        print(f"{'=' * 70}")
        print(f"[INPUT] {en_file.name}")
        print(f"[OUTPUT] {vi_file.name}")
        print()
        
        try:
            translate_subtitle_nllb_cached(
                str(en_file),
                str(vi_file),
                nllb_translator,
                batch_size=BATCH_SIZE
            )
            print(f"[SUCCESS] Translation complete!")
            results.append((en_file.name, True))
        except Exception as e:
            print(f"[ERROR] Translation failed: {e}")
            import traceback
            traceback.print_exc()
            results.append((en_file.name, False))
    
    # Print summary
    print("\n" + "=" * 70)
    print("  TRANSLATION COMPLETE!")
    print("=" * 70)
    
    successful = sum(1 for _, success in results if success)
    failed = len(results) - successful
    
    print(f"\n[SUMMARY]")
    print(f"  Total files: {len(results)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    
    print(f"\n[OUTPUT] Vietnamese subtitles saved to: {OUTPUT_DIR}")
    
    # Show detailed results
    if results:
        print("\n[DETAILED RESULTS]")
        for filename, success in results:
            status = "✓ SUCCESS" if success else "✗ FAILED"
            vi_filename = filename.replace("_en.srt", "_vi.srt")
            print(f"  {status} - {filename} → {vi_filename}")
    
    print("\n" + "=" * 70)
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
