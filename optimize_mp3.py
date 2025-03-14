#!/usr/bin/env python3
"""
MP3 Optimization Script for Chad Battles
This script optimizes MP3 files to 160kbps and prepares them for hosting.
"""
import os
import subprocess
import json
import argparse
from pathlib import Path

def check_ffmpeg():
    """Check if ffmpeg is installed."""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def optimize_mp3(input_dir, output_dir, bitrate='160k'):
    """Optimize MP3 files in the input directory and save to output directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get list of MP3 files
    mp3_files = [f for f in input_path.glob('*.mp3') if f.is_file()]
    
    if not mp3_files:
        print(f"No MP3 files found in {input_dir}")
        return []
    
    print(f"Found {len(mp3_files)} MP3 files. Optimizing...")
    
    processed_files = []
    
    for i, mp3_file in enumerate(mp3_files, 1):
        output_file = output_path / mp3_file.name
        
        # Get original file size
        original_size = mp3_file.stat().st_size
        
        # Run ffmpeg to optimize the file
        cmd = [
            'ffmpeg', 
            '-i', str(mp3_file), 
            '-codec:a', 'libmp3lame', 
            '-b:a', bitrate, 
            '-y',  # Overwrite output files
            str(output_file)
        ]
        
        print(f"[{i}/{len(mp3_files)}] Processing {mp3_file.name}...", end="", flush=True)
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            # Get new file size
            new_size = output_file.stat().st_size
            size_reduction = (1 - (new_size / original_size)) * 100
            
            print(f" Done! Size reduced from {original_size/1024/1024:.2f}MB to {new_size/1024/1024:.2f}MB ({size_reduction:.1f}% reduction)")
            
            # Add to processed files list
            processed_files.append({
                "file": mp3_file.name,
                "original_size": original_size,
                "optimized_size": new_size,
                "reduction_percent": size_reduction
            })
        else:
            print(f" Failed! Error: {result.stderr.decode()}")
    
    return processed_files

def create_tracks_json(files, output_dir, base_url):
    """Create a tracks.json file for the processed MP3 files."""
    output_path = Path(output_dir)
    tracks = []
    
    for file_info in files:
        filename = file_info["file"]
        # Extract title from filename
        title = Path(filename).stem.replace('_', ' ').title()
        
        tracks.append({
            "title": title,
            "file": filename,
            "path": f"{base_url}/{filename}"
        })
    
    # Create tracks.json
    tracks_file = output_path / "tracks.json"
    with open(tracks_file, "w") as f:
        json.dump({"tracks": tracks}, f, indent=2)
    
    print(f"Created tracks.json with {len(tracks)} tracks")
    
    return str(tracks_file)

def main():
    parser = argparse.ArgumentParser(description="Optimize MP3 files for Chad Battles")
    parser.add_argument("--input", "-i", default="app/static/music", help="Input directory containing MP3 files")
    parser.add_argument("--output", "-o", default="optimized_mp3", help="Output directory for optimized files")
    parser.add_argument("--bitrate", "-b", default="160k", help="Target bitrate (default: 160k)")
    parser.add_argument("--base-url", "-u", default="https://chadbattles.fun/music", help="Base URL for tracks in tracks.json")
    
    args = parser.parse_args()
    
    # Check if ffmpeg is installed
    if not check_ffmpeg():
        print("Error: ffmpeg is not installed. Please install it and try again.")
        print("Windows: https://www.gyan.dev/ffmpeg/builds/")
        print("Mac: brew install ffmpeg")
        print("Linux: sudo apt-get install ffmpeg")
        return
    
    # Process files
    print(f"Optimizing MP3 files from {args.input} to {args.output} at {args.bitrate} bitrate")
    processed_files = optimize_mp3(args.input, args.output, args.bitrate)
    
    if processed_files:
        # Create tracks.json
        tracks_json = create_tracks_json(processed_files, args.output, args.base_url)
        
        # Calculate overall statistics
        total_original = sum(f["original_size"] for f in processed_files)
        total_optimized = sum(f["optimized_size"] for f in processed_files)
        total_reduction = (1 - (total_optimized / total_original)) * 100
        
        # Print summary
        print("\nOptimization Complete!")
        print(f"Total files processed: {len(processed_files)}")
        print(f"Original total size: {total_original/1024/1024:.2f}MB")
        print(f"Optimized total size: {total_optimized/1024/1024:.2f}MB")
        print(f"Overall reduction: {total_reduction:.1f}%")
        print(f"\nOutput files are in: {os.path.abspath(args.output)}")
        print(f"tracks.json created: {tracks_json}")
        print("\nNext steps:")
        print("1. Upload the optimized files to your NameCheap hosting")
        print("2. Configure Cloudflare for better performance")
        print("3. Test the website with the new MP3 locations")

if __name__ == "__main__":
    main() 