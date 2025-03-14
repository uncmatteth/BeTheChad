# Chad Battles MP3 Optimization and Hosting Migration Guide

This document provides detailed instructions for implementing the MP3 optimization and hosting migration plan for Chad Battles.

## Current Implementation

Currently, the Chad Battles app serves music through the following components:

1. **Server-side endpoint:** `/music/list` in `app/controllers/music.py`
   ```python
   @music_bp.route('/list')
   def list_music():
       """List all available music files."""
       try:
           # Set cache headers to reduce server load - cache for 1 hour
           cache_timeout = 3600  # seconds (1 hour)
           response = jsonify(get_music_files())
           response.headers['Cache-Control'] = f'public, max-age={cache_timeout}'
           response.headers['Expires'] = (datetime.utcnow() + timedelta(seconds=cache_timeout)).strftime('%a, %d %b %Y %H:%M:%S GMT')
           return response
       except Exception as e:
           logger.error(f"Error listing music files: {str(e)}")
           return jsonify({"error": str(e), "message": "Could not list music files"}), 500
   ```

2. **File discovery function:** `get_music_files()` in `app/controllers/music.py`
   ```python
   def get_music_files():
       """Get a list of all music files."""
       music_dir = os.path.join(current_app.static_folder, 'music')
       
       # Check if directory exists
       if not os.path.exists(music_dir):
           logger.warning(f"Music directory not found: {music_dir}")
           return []
       
       music_files = []
       skipped_files = []
       
       try:
           # Count total files for logging
           total_files = 0
           
           for file in os.listdir(music_dir):
               total_files += 1
               file_path = os.path.join(music_dir, file)
               
               # Only include .mp3 files and exclude battle.mp3 and menu.mp3 (placeholders)
               if file.endswith('.mp3') and file not in ['battle.mp3', 'menu.mp3']:
                   # Extract title from filename
                   title = os.path.splitext(file)[0].replace('_', ' ').title()
                   
                   music_files.append({
                       'title': title,
                       'file': file,
                       'path': f'/static/music/{file}'
                   })
               else:
                   skipped_files.append(file)
           
           # Log results
           logger.info(f"Processed {total_files} files in music directory")
           logger.info(f"Added {len(music_files)} valid music files")
           
           if skipped_files:
               logger.info(f"Skipped {len(skipped_files)} files: {', '.join(skipped_files[:5])}...")
           
           # Randomize order
           random.shuffle(music_files)
           
           return music_files
       except Exception as e:
           logger.error(f"Error processing music directory {music_dir}: {str(e)}")
           return []
   ```

3. **Client-side jukebox implementation:** `app/static/js/jukebox.js`
   - Fetches music files via a call to `/music/list` 
   - Plays audio using the HTML5 Audio API
   - Stores player state in localStorage
   - Key excerpt:
     ```javascript
     // Inside initJukebox function
     fetch('/music/list')
         .then(response => response.json())
         .then(data => {
             const jukebox = new Jukebox(containerId, data);
             window.jukebox = jukebox; // Make it globally accessible
         })
     ```

## Implementation Steps

### 1. Install Required Dependencies

First, make sure we have the right dependencies for handling external requests:

```bash
pip install requests
```

Add this to requirements.txt if it's not already there:

```
requests>=2.25.1
```

### 2. Update the Music Controller

In `app/controllers/music.py`, modify the following:

1. Add environment variable support:
```python
import requests
import os

# Add this near the top of the file
MUSIC_BASE_URL = os.environ.get('MUSIC_BASE_URL', 'https://chadbattles.fun/music')
```

2. Update the `get_music_files()` function:
```python
def get_music_files():
    """Get a list of all music files."""
    # Check if we're using external hosting
    if MUSIC_BASE_URL:
        try:
            # Try to fetch tracks.json from external host
            response = requests.get(f"{MUSIC_BASE_URL}/tracks.json", timeout=5)
            if response.status_code == 200:
                logger.info(f"Loaded {len(response.json().get('tracks', []))} tracks from external source")
                return response.json().get('tracks', [])
            else:
                logger.warning(f"Failed to load tracks from external source: {response.status_code}")
                # Fall back to local files if they exist
        except Exception as e:
            logger.error(f"Error fetching tracks from external source: {str(e)}")
            # Fall back to local files if they exist
    
    # Original local file implementation as fallback
    music_dir = os.path.join(current_app.static_folder, 'music')
    
    # Check if directory exists
    if not os.path.exists(music_dir):
        logger.warning(f"Music directory not found: {music_dir}")
        
        # If both external and local fail, generate a hardcoded list
        if MUSIC_BASE_URL:
            logger.info(f"Generating fallback track list from MUSIC_BASE_URL pattern")
            return [
                {
                    'title': f"Be the Chad {i}",
                    'path': f"{MUSIC_BASE_URL}/be-the-chad-{i}.mp3"
                }
                for i in range(1, 105)  # 104 tracks
            ]
        return []
    
    music_files = []
    skipped_files = []
    
    try:
        # Count total files for logging
        total_files = 0
        
        for file in os.listdir(music_dir):
            total_files += 1
            
            # Only include .mp3 files and exclude battle.mp3 and menu.mp3 (placeholders)
            if file.endswith('.mp3') and file not in ['battle.mp3', 'menu.mp3']:
                # Extract title from filename
                title = os.path.splitext(file)[0].replace('_', ' ').title()
                
                # Use external URL if configured
                path = f"{MUSIC_BASE_URL}/{file}" if MUSIC_BASE_URL else f"/static/music/{file}"
                
                music_files.append({
                    'title': title,
                    'file': file,
                    'path': path
                })
            else:
                skipped_files.append(file)
        
        # Log results
        logger.info(f"Processed {total_files} files in music directory")
        logger.info(f"Added {len(music_files)} valid music files")
        
        if skipped_files:
            logger.info(f"Skipped {len(skipped_files)} files: {', '.join(skipped_files[:5])}...")
        
        # Randomize order
        random.shuffle(music_files)
        
        return music_files
    except Exception as e:
        logger.error(f"Error processing music directory {music_dir}: {str(e)}")
        
        # If local files fail but we have MUSIC_BASE_URL, generate a fallback list
        if MUSIC_BASE_URL:
            logger.info(f"Generating fallback track list from MUSIC_BASE_URL pattern")
            return [
                {
                    'title': f"Be the Chad {i}",
                    'path': f"{MUSIC_BASE_URL}/be-the-chad-{i}.mp3"
                }
                for i in range(1, 105)  # 104 tracks
            ]
        return []
```

3. Add a new endpoint for info/debugging:
```python
@music_bp.route('/info')
def music_info():
    """Display information about the music configuration."""
    info = {
        "music_base_url": MUSIC_BASE_URL,
        "using_external_hosting": bool(MUSIC_BASE_URL),
        "track_count": len(get_music_files()),
        "environment": current_app.config.get('ENV', 'development')
    }
    return jsonify(info)
```

### 3. Update Environment Configuration

1. Update `.env` file:
```
MUSIC_BASE_URL=https://chadbattles.fun/music
```

2. Update `render.yaml` to include the environment variable:
```yaml
env:
  - key: MUSIC_BASE_URL
    value: https://chadbattles.fun/music
```

### 4. Create the tracks.json File

Create this file to be uploaded to the NameCheap server (in the `/public_html/music/` directory):

```json
{
  "tracks": [
    {
      "title": "Be the Chad 1",
      "file": "be-the-chad-1.mp3",
      "path": "https://chadbattles.fun/music/be-the-chad-1.mp3"
    },
    {
      "title": "Be the Chad 2",
      "file": "be-the-chad-2.mp3",
      "path": "https://chadbattles.fun/music/be-the-chad-2.mp3"
    },
    // Repeat for all 104 tracks
  ]
}
```

### 5. Update Jukebox.js (if needed)

In most cases, the current client-side player won't need changes because the server is already returning the correct format. However, if you encounter issues, you might need to add resilience to absolute URLs:

```javascript
// In the playTrack method, add this check
playTrack(index) {
    if (this.musicFiles.length === 0) return;
    
    if (index >= 0 && index < this.musicFiles.length) {
        this.currentTrackIndex = index;
        this.currentTrack = this.musicFiles[this.currentTrackIndex];
        
        // Add resilience to both relative and absolute paths
        let trackPath = this.currentTrack.path;
        if (trackPath && !trackPath.startsWith('http') && !trackPath.startsWith('/')) {
            trackPath = '/' + trackPath;
        }
        
        this.audio.src = trackPath;
        // ...rest of the method...
    }
}
```

### 6. Create the Optimization Script

Create a Python script `optimize_mp3.py` in the root directory to help optimize the MP3 files:

```python
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
```

### 7. Testing and Verification

After implementing these changes, follow this testing process:

1. **Local Testing**:
   - Set `MUSIC_BASE_URL=https://chadbattles.fun/music` in your .env file
   - Start the Flask app: `python run.py`
   - Open the app in a browser and verify the music player works

2. **Deployment Testing**:
   - Commit and push your changes to GitHub
   - Verify the application deploys successfully to Render.com
   - Check the music player on the live site

3. **Performance Testing**:
   - Compare page load times before and after the changes
   - Verify music player starts quickly
   - Test on mobile devices and slower connections

### 8. Cleanup After Successful Verification

Once everything is working correctly:

1. Update `.gitignore` to exclude MP3 files:
```
# MP3 files (now hosted externally)
app/static/music/*.mp3
```

2. Remove the MP3 files from the repository:
```bash
git rm -r --cached app/static/music/*.mp3
git commit -m "Remove MP3 files from repository, now hosted externally"
git push
```

## Implementation Timeline

- Code changes: ~1 hour
- MP3 optimization: ~1 hour
- NameCheap setup: ~30 minutes
- Cloudflare setup: ~30 minutes
- Testing and verification: ~1 hour

Total estimated time: ~4 hours 