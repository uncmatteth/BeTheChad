"""
Music controller for Chad Battles.
Handles music playback functionality.
"""
from flask import Blueprint, jsonify, current_app, send_from_directory, request
import os
import random
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

music_bp = Blueprint('music', __name__, url_prefix='/music')

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