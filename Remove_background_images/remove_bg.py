"""
Background Removal Tool
Remove backgrounds from images using rembg with GPU acceleration
"""
import sys
from pathlib import Path
from typing import Tuple
from PIL import Image
from rembg import remove
from tqdm import tqdm
import time

from utils import (
    print_banner,
    get_all_images,
    ensure_output_path,
    format_duration,
    get_file_size_mb
)


def check_gpu_availability():
    """
    Check if GPU (CUDA) is available for acceleration
    
    Returns:
        Tuple of (is_available, device_name)
    """
    try:
        import onnxruntime as ort
        providers = ort.get_available_providers()
        if 'CUDAExecutionProvider' in providers:
            return True, "CUDA GPU"
        else:
            return False, "CPU"
    except Exception as e:
        return False, f"CPU (Error: {str(e)})"


def process_image(input_path: Path, output_path: Path) -> Tuple[bool, float]:
    """
    Remove background from a single image
    
    Args:
        input_path: Path to input image
        output_path: Path to save output image
        
    Returns:
        Tuple of (success, processing_time)
    """
    try:
        start_time = time.time()
        
        # Load image
        input_image = Image.open(input_path)
        
        # Remove background
        output_image = remove(input_image)
        
        # Save output as PNG
        output_image.save(output_path, 'PNG')
        
        processing_time = time.time() - start_time
        return True, processing_time
        
    except Exception as e:
        print(f"\n❌ Error processing {input_path.name}: {str(e)}")
        return False, 0.0


def process_batch(input_folder: Path, output_folder: Path):
    """
    Process all images in input folder
    
    Args:
        input_folder: Path to input folder
        output_folder: Path to output folder
    """
    # Get all images
    images = get_all_images(input_folder)
    
    if not images:
        print(f"\n❌ No images found in '{input_folder}'")
        print(f"   Supported formats: PNG, JPG, JPEG, BMP, WEBP")
        return
    
    print(f"\n📁 Found {len(images)} image(s) to process")
    
    # Check GPU availability
    gpu_available, device_name = check_gpu_availability()
    print(f"🖥️  Device: {device_name}")
    if gpu_available:
        print("⚡ GPU acceleration enabled - Processing will be faster!")
    print()
    
    # Process images
    successful = 0
    failed = 0
    total_time = 0.0
    total_size_before = 0.0
    total_size_after = 0.0
    
    for input_path, relative_path in tqdm(images, desc="Processing images", unit="img"):
        output_path = ensure_output_path(relative_path, output_folder)
        
        # Track file size
        size_before = get_file_size_mb(input_path)
        total_size_before += size_before
        
        # Process image
        success, proc_time = process_image(input_path, output_path)
        
        if success:
            successful += 1
            total_time += proc_time
            size_after = get_file_size_mb(output_path)
            total_size_after += size_after
        else:
            failed += 1
    
    # Print summary
    print("\n" + "="*60)
    print("📊 PROCESSING SUMMARY")
    print("="*60)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed:     {failed}")
    print(f"📁 Total:      {len(images)}")
    
    if successful > 0:
        avg_time = total_time / successful
        print(f"\n⏱️  Average time per image: {format_duration(avg_time)}")
        print(f"⏱️  Total processing time:  {format_duration(total_time)}")
        print(f"\n💾 Total input size:  {total_size_before:.2f} MB")
        print(f"💾 Total output size: {total_size_after:.2f} MB")
        
        if total_size_before > 0:
            size_ratio = (total_size_after / total_size_before) * 100
            print(f"📉 Size change: {size_ratio:.1f}%")
    
    print("="*60)
    print(f"\n✨ Output saved to: {output_folder.absolute()}")


def main():
    """Main execution function"""
    print_banner()
    
    # Setup paths
    script_dir = Path(__file__).parent
    input_folder = script_dir / "input"
    output_folder = script_dir / "output"
    
    # Create folders if they don't exist
    input_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)
    
    # Check if input folder has any images
    if not any(input_folder.iterdir()):
        print("❌ Error: 'input' folder is empty!")
        print("\n📝 Usage:")
        print("   1. Place images or folders in 'input' folder")
        print("   2. Run this script")
        print("   3. Check 'output' folder for results")
        print("\n💡 Supported formats: PNG, JPG, JPEG, BMP, WEBP")
        sys.exit(1)
    
    # Process images
    try:
        process_batch(input_folder, output_folder)
    except KeyboardInterrupt:
        print("\n\n⚠️  Processing interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
