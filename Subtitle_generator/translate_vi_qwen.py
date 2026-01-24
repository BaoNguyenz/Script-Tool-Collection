#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vietnamese Translation Script - Qwen2.5
Offline LLM-based translation with context awareness
"""

import sys
import srt
from pathlib import Path
import requests
import json

# Configuration
OUTPUT_DIR = Path(__file__).parent / "output"

# Ollama settings
OLLAMA_API_URL = "http://localhost:11434/api/generate"
QWEN_MODEL = "qwen2.5:7b"  # Or qwen2.5:14b for better quality
BATCH_SIZE = 5  # Number of subtitles per translation call


def print_banner():
    """Print script banner"""
    print("=" * 70)
    print("  Vietnamese Translation - Qwen2.5")
    print("  Offline LLM with context awareness")
    print(f"  Model: {QWEN_MODEL}")
    print("=" * 70)
    print()


def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            return True, model_names
        return False, []
    except:
        return False, []


def get_en_files():
    """Get all English subtitle files"""
    if not OUTPUT_DIR.exists():
        print(f"[ERROR] Output directory not found: {OUTPUT_DIR}")
        return []
    
    en_files = list(OUTPUT_DIR.glob("*_en.srt"))
    return sorted(en_files)


def load_subtitles(srt_path: str):
    """Load subtitles from file"""
    with open(srt_path, 'r', encoding='utf-8') as f:
        return list(srt.parse(f.read()))


def save_subtitles(subtitles, srt_path: str):
    """Save subtitles to file"""
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(subtitles))


def create_translation_prompt(subtitle_batch, context=""):
    """Create context-aware translation prompt for Qwen"""
    
    # Build subtitle list
    subtitle_texts = []
    for i, sub in enumerate(subtitle_batch, 1):
        subtitle_texts.append(f"{i}. {sub.content}")
    
    batch_text = "\n".join(subtitle_texts)
    
    context_part = ""
    if context:
        context_part = f"""
PREVIOUS CONTEXT (for continuity):
{context}

"""
    
    prompt = f"""You are a professional Vietnamese translator. Translate the following English subtitles to natural Vietnamese.

CRITICAL RULES:
1. Pay attention to speaker gender and relationship for pronouns (anh/chị/em/cô/bác)
2. Use natural, conversational Vietnamese
3. Maintain the same numbering (1., 2., etc.)
4. Keep names and technical terms appropriate
5. Make it sound like native Vietnamese speakers

{context_part}ENGLISH SUBTITLES:
{batch_text}

VIETNAMESE TRANSLATION (numbers + Vietnamese text only):"""
    
    return prompt


def translate_with_qwen(subtitle_batch, context=""):
    """Translate batch using Qwen via Ollama"""
    
    prompt = create_translation_prompt(subtitle_batch, context)
    
    try:
        payload = {
            "model": QWEN_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # Lower for consistency
                "top_p": 0.9,
                "top_k": 40,
            }
        }
        
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "")
        else:
            print(f"[ERROR] Ollama API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")
        return None


def parse_qwen_response(response_text, subtitle_batch):
    """Parse Qwen response and update subtitles"""
    
    lines = response_text.strip().split('\n')
    translations = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Remove numbering if present
        if '. ' in line and line[0].isdigit():
            parts = line.split('. ', 1)
            if len(parts) == 2:
                translation = parts[1]
            else:
                translation = line
        else:
            translation = line
        
        # Skip if it looks like English (basic check)
        if translation and not all(ord(c) < 128 for c in translation):
            translations.append(translation)
    
    # Update subtitle content
    for i, sub in enumerate(subtitle_batch):
        if i < len(translations):
            sub.content = translations[i]


def translate_file_qwen(en_file: Path, vi_file: Path):
    """Translate subtitle file using Qwen"""
    
    print(f"[INPUT] {en_file.name}")
    print(f"[OUTPUT] {vi_file.name}")
    print()
    
    # Load subtitles
    print("[LOADING] Reading subtitle file...")
    subtitles = load_subtitles(str(en_file))
    total = len(subtitles)
    print(f"[INFO] Found {total} subtitle(s)")
    print()
    
    # Translate in batches with context
    print("[TRANSLATING] Using Qwen2.5 with context awareness...")
    print(f"[INFO] This may take a while (~{total//BATCH_SIZE * 3} seconds)")
    print()
    
    context = ""
    
    for i in range(0, total, BATCH_SIZE):
        batch = subtitles[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"  [{batch_num}/{total_batches}] Translating {len(batch)} subtitle(s)...", end=" ", flush=True)
        
        # Translate
        response = translate_with_qwen(batch, context)
        
        if response:
            parse_qwen_response(response, batch)
            print("✓")
            
            # Update context (last 2 subtitles)
            if len(batch) >= 2:
                context = f"{batch[-2].content}\n{batch[-1].content}"
            elif len(batch) == 1:
                context = batch[-1].content
        else:
            print("✗ (keeping original)")
    
    # Save translated subtitles
    print()
    print("[SAVING] Writing Vietnamese subtitle file...")
    save_subtitles(subtitles, str(vi_file))
    print(f"[SUCCESS] Translation complete!")


def main():
    """Main execution function"""
    print_banner()
    
    # Check Ollama
    print("[CHECKING] Verifying Ollama installation...")
    is_running, models = check_ollama()
    
    if not is_running:
        print("[ERROR] Ollama is not running!")
        print()
        print("Please install and start Ollama:")
        print("  1. Download from: https://ollama.ai")
        print("  2. Install and run Ollama")
        print("  3. Pull Qwen model: ollama pull qwen2.5:7b")
        print()
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"[SUCCESS] Ollama is running!")
    print(f"[INFO] Available models: {', '.join(models) if models else 'none'}")
    
    # Check if Qwen model is available
    if QWEN_MODEL not in models:
        print(f"\n[WARNING] Model '{QWEN_MODEL}' not found!")
        print(f"\nPlease pull the model first:")
        print(f"  ollama pull {QWEN_MODEL}")
        print()
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"[SUCCESS] Model '{QWEN_MODEL}' ready!")
    print()
    
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
    print()
    
    # Translate files
    print("=" * 70)
    print(f"[TRANSLATING] Processing {len(files_to_translate)} file(s)...")
    print("=" * 70)
    print()
    
    results = []
    
    for i, en_file in enumerate(files_to_translate, 1):
        vi_file = en_file.parent / en_file.name.replace("_en.srt", "_vi.srt")
        
        print(f"\n{'=' * 70}")
        print(f"[FILE {i}/{len(files_to_translate)}]")
        print(f"{'=' * 70}")
        
        try:
            translate_file_qwen(en_file, vi_file)
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
