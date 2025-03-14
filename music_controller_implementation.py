"""
Updated Music controller for Chad Battles.
This version supports both local and external MP3 files.
"""
from flask import Blueprint, jsonify, current_app, send_from_directory, request
import os
import random
import logging
import requests
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

music_bp = Blueprint('music', __name__, url_prefix='/music')

# Configuration for external music hosting
MUSIC_BASE_URL = os.environ.get('MUSIC_BASE_URL', 'https://chadbattles.fun/music')

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

@music_bp.route('/info')
def music_info():
    """Display information about the music configuration."""
    music_files = get_music_files()
    info = {
        "music_base_url": MUSIC_BASE_URL,
        "using_external_hosting": bool(MUSIC_BASE_URL),
        "track_count": len(music_files),
        "first_few_tracks": [track.get('title', 'Unknown') for track in music_files[:5]] if music_files else [],
        "environment": current_app.config.get('ENV', 'development')
    }
    return jsonify(info)

def get_music_files():
    """Get a list of all music files."""
    # Check if we're using external hosting
    if MUSIC_BASE_URL:
        try:
            # Try to fetch tracks.json from external host
            response = requests.get(f"{MUSIC_BASE_URL}/tracks.json", timeout=5)
            if response.status_code == 200:
                tracks = response.json().get('tracks', [])
                logger.info(f"Loaded {len(tracks)} tracks from external source")
                
                # Randomize order
                random.shuffle(tracks)
                return tracks
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
            tracks = [
                {
                    'title': f"Be the Chad {i}",
                    'file': f"be-the-chad-{i}.mp3",
                    'path': f"{MUSIC_BASE_URL}/be-the-chad-{i}.mp3"
                }
                for i in range(1, 105)  # 104 tracks
            ]
            random.shuffle(tracks)
            return tracks
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
                
                # Use external URL if configured, otherwise use local path
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
            tracks = [
                {
                    'title': f"Be the Chad {i}",
                    'file': f"be-the-chad-{i}.mp3",
                    'path': f"{MUSIC_BASE_URL}/be-the-chad-{i}.mp3"
                }
                for i in range(1, 105)  # 104 tracks
            ]
            random.shuffle(tracks)
            return tracks
        return [] 