#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Subtitle Processing Utilities
- Timing adjustment for continuous display
- NLLB translation from English to Vietnamese
"""

import srt
from pathlib import Path
from datetime import timedelta
from typing import List, Optional
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


def adjust_continuous_timing(srt_path: str, gap_ms: int = 10) -> None:
    """
    Điều chỉnh timing để subtitle nối đuôi nhau (loại bỏ gaps).
    
    Args:
        srt_path: Đường dẫn file .srt
        gap_ms: Khoảng cách tối thiểu giữa subtitles (milliseconds)
    
    Logic:
        - Với mỗi subtitle i, kéo end_time ra đến start_time của subtitle i+1
        - Trừ đi gap_ms để tránh chồng lấn
        - Subtitle cuối cùng giữ nguyên
    """
    # Read SRT file
    with open(srt_path, 'r', encoding='utf-8') as f:
        subtitles = list(srt.parse(f.read()))
    
    if len(subtitles) <= 1:
        return  # Nothing to adjust
    
    # Adjust timing
    gap_delta = timedelta(milliseconds=gap_ms)
    
    for i in range(len(subtitles) - 1):
        current = subtitles[i]
        next_sub = subtitles[i + 1]
        
        # Calculate new end time: next subtitle start - gap
        new_end = next_sub.start - gap_delta
        
        # Only adjust if:
        # 1. New end time is after current end (extending, not shortening)
        # 2. New end time is before next start (no overlap)
        if new_end > current.end and new_end < next_sub.start:
            current.end = new_end
    
    # Write back to file
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(subtitles))


def translate_subtitle_nllb(
    srt_path: str,
    output_path: str,
    model_name: str = "facebook/nllb-200-distilled-600M",
    device: str = "cuda",
    batch_size: int = 8,
    progress_callback: Optional[callable] = None
) -> None:
    """
    Dịch subtitle từ EN → VI bằng NLLB.
    
    Args:
        srt_path: Đường dẫn file .srt tiếng Anh
        output_path: Đường dẫn output file .srt tiếng Việt
        model_name: NLLB model name
        device: 'cuda' hoặc 'cpu'
        batch_size: Số subtitle dịch cùng lúc
        progress_callback: Function(current, total) để track progress
    
    Logic:
        - Load NLLB model và tokenizer
        - Parse file .srt
        - Dịch từng batch subtitle text (giữ nguyên timestamps)
        - Ghi file .srt mới
    """
    print(f"[INFO] Loading NLLB model: {model_name}")
    
    # Load model and tokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            src_lang="eng_Latn"
        )
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        model = model.to(device)
        model.eval()
        print(f"[SUCCESS] Model loaded on {device}")
    except Exception as e:
        if device == "cuda":
            print(f"[WARNING] Failed to load on CUDA: {e}")
            print("[INFO] Falling back to CPU...")
            device = "cpu"
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            model.eval()
            print("[SUCCESS] Model loaded on CPU")
        else:
            raise
    
    # Read SRT file
    with open(srt_path, 'r', encoding='utf-8') as f:
        subtitles = list(srt.parse(f.read()))
    
    if not subtitles:
        print("[WARNING] No subtitles found in file")
        return
    
    total = len(subtitles)
    print(f"[INFO] Translating {total} subtitle(s)...")
    
    # Translate in batches
    for i in range(0, total, batch_size):
        batch = subtitles[i:i + batch_size]
        texts = [sub.content for sub in batch]
        
        # Tokenize
        inputs = tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(device)
        
        # Translate
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids("vie_Latn"),
            max_length=512,
            num_beams=5,
            early_stopping=True
        )
        
        # Decode
        translations = tokenizer.batch_decode(
            translated_tokens,
            skip_special_tokens=True
        )
        
        # Update subtitle content (keep timing)
        for j, translation in enumerate(translations):
            batch[j].content = translation
        
        # Progress callback
        if progress_callback:
            progress_callback(min(i + batch_size, total), total)
        else:
            print(f"  Progress: {min(i + batch_size, total)}/{total}")
    
    # Write translated subtitles
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(subtitles))
    
    print(f"[SUCCESS] Vietnamese subtitle saved to: {output_path}")


# Cache for loaded models to avoid reloading
_nllb_model_cache = {}


def get_nllb_translator(model_name: str, device: str):
    """
    Get cached NLLB translator or create new one.
    Returns (model, tokenizer, device)
    """
    cache_key = f"{model_name}_{device}"
    
    if cache_key not in _nllb_model_cache:
        print(f"[INFO] Loading NLLB model: {model_name}")
        
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                src_lang="eng_Latn"
            )
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            model = model.to(device)
            model.eval()
            actual_device = device
            print(f"[SUCCESS] Model loaded on {device}")
        except Exception as e:
            if device == "cuda":
                print(f"[WARNING] Failed to load on CUDA: {e}")
                print("[INFO] Falling back to CPU...")
                tokenizer = AutoTokenizer.from_pretrained(
                    model_name,
                    src_lang="eng_Latn"
                )
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                model.eval()
                actual_device = "cpu"
                print("[SUCCESS] Model loaded on CPU")
            else:
                raise
        
        _nllb_model_cache[cache_key] = (model, tokenizer, actual_device)
    
    return _nllb_model_cache[cache_key]


def translate_subtitle_nllb_cached(
    srt_path: str,
    output_path: str,
    translator_cache: tuple,
    batch_size: int = 8
) -> None:
    """
    Dịch subtitle sử dụng cached translator.
    
    Args:
        srt_path: Đường dẫn file .srt tiếng Anh
        output_path: Đường dẫn output file .srt tiếng Việt
        translator_cache: Tuple (model, tokenizer, device) từ get_nllb_translator()
        batch_size: Số subtitle dịch cùng lúc
    """
    model, tokenizer, device = translator_cache
    
    # Read SRT file
    with open(srt_path, 'r', encoding='utf-8') as f:
        subtitles = list(srt.parse(f.read()))
    
    if not subtitles:
        print("[WARNING] No subtitles found in file")
        return
    
    total = len(subtitles)
    
    # Translate in batches
    for i in range(0, total, batch_size):
        batch = subtitles[i:i + batch_size]
        texts = [sub.content for sub in batch]
        
        # Tokenize
        inputs = tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(device)
        
        # Translate
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids("vie_Latn"),
            max_length=512,
            num_beams=5,
            early_stopping=True
        )
        
        # Decode
        translations = tokenizer.batch_decode(
            translated_tokens,
            skip_special_tokens=True
        )
        
        # Update subtitle content (keep timing)
        for j, translation in enumerate(translations):
            batch[j].content = translation
    
    # Write translated subtitles
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(subtitles))
