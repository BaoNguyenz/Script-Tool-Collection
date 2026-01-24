"""
Utility functions for background removal tool
"""
from pathlib import Path
from typing import List, Tuple
import time


# Supported image formats
SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.bmp', '.webp'}


def print_banner():
    """Print tool banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║         Background Removal Tool - rembg v2.0            ║
║              GPU Accelerated (CUDA Support)              ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)


def is_image_file(path: Path) -> bool:
    """
    Check if file is a supported image format
    
    Args:
        path: Path to file
        
    Returns:
        True if file is a supported image format
    """
    return path.suffix.lower() in SUPPORTED_FORMATS


def get_all_images(input_path: Path) -> List[Tuple[Path, Path]]:
    """
    Recursively find all images in input path
    
    Args:
        input_path: Path to input file or folder
        
    Returns:
        List of tuples (input_file_path, relative_path)
    """
    images = []
    
    if input_path.is_file():
        if is_image_file(input_path):
            images.append((input_path, input_path.name))
    elif input_path.is_dir():
        for file_path in input_path.rglob('*'):
            if file_path.is_file() and is_image_file(file_path):
                relative_path = file_path.relative_to(input_path)
                images.append((file_path, relative_path))
    
    return images


def ensure_output_path(relative_path: Path, output_base: Path) -> Path:
    """
    Create output directory structure and return output file path
    
    Args:
        relative_path: Relative path from input folder
        output_base: Base output directory
        
    Returns:
        Full output file path with .png extension
    """
    output_path = output_base / relative_path
    output_path = output_path.with_suffix('.png')  # Always save as PNG for transparency
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "1m 23s" or "45.2s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"


def get_file_size_mb(path: Path) -> float:
    """
    Get file size in megabytes
    
    Args:
        path: Path to file
        
    Returns:
        File size in MB
    """
    return path.stat().st_size / (1024 * 1024)
