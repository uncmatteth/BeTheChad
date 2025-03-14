import os
import json
from flask import Blueprint, jsonify, send_from_directory, current_app, render_template, request
from flask_login import login_required, current_user

# Create blueprint
music = Blueprint('music', __name__)

@music.route('/tracks')
def get_tracks():
    """Return a list of all music tracks"""
    tracks = []
    
    # Get music directory from the static folder
    music_dir = os.path.join(current_app.static_folder, 'music')
    
    # Get all MP3 files from the music folder
    try:
        current_app.logger.info(f"Scanning music directory: {music_dir}")
        if not os.path.exists(music_dir):
            current_app.logger.warning(f"Music directory doesn't exist: {music_dir}")
            return jsonify([])
            
        for filename in os.listdir(music_dir):
            if filename.endswith('.mp3'):
                file_path = os.path.join(music_dir, filename)
                file_size = os.path.getsize(file_path)
                
                # Skip placeholder files (less than 1MB)
                if file_size < 100 * 1024:  # Skip files smaller than 100KB
                    current_app.logger.warning(f"Skipping likely placeholder file: {filename} (size: {file_size} bytes)")
                    continue
                    
                # Create a track object
                track = {
                    'title': os.path.splitext(filename)[0].replace('_', ' '),
                    'path': f'/static/music/{filename}',
                    'filename': filename,
                    'size': file_size
                }
                tracks.append(track)
                current_app.logger.debug(f"Added track: {track['title']} ({file_size} bytes)")
        
        current_app.logger.info(f"Found {len(tracks)} valid music tracks")
    except Exception as e:
        current_app.logger.error(f"Error reading music directory: {e}")
        
    return jsonify(tracks)

@music.route('/stream/<filename>')
def stream_music(filename):
    """Stream a music file"""
    try:
        music_dir = os.path.join(current_app.static_folder, 'music')
        if not os.path.exists(os.path.join(music_dir, filename)):
            current_app.logger.error(f"Music file not found: {filename}")
            return jsonify({"error": "File not found"}), 404
            
        current_app.logger.info(f"Streaming music file: {filename}")
        return send_from_directory(music_dir, filename)
    except Exception as e:
        current_app.logger.error(f"Error streaming music file: {e}")
        return jsonify({"error": "File not found"}), 404

@music.route('/list')
def list_music():
    """Return a list of all available music files"""
    music_dir = os.path.join(current_app.static_folder, 'music')
    music_files = []
    
    # Make sure the directory exists
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
        current_app.logger.info(f"Created music directory: {music_dir}")
    
    # Get all MP3 files
    try:
        current_app.logger.info(f"Scanning music directory for /list: {music_dir}")
        file_count = 0
        valid_count = 0
        
        for filename in os.listdir(music_dir):
            file_count += 1
            if filename.lower().endswith('.mp3'):
                file_path = os.path.join(music_dir, filename)
                file_size = os.path.getsize(file_path)
                
                # Skip very small files that are likely placeholders
                if file_size < 100 * 1024:  # Skip files smaller than 100KB
                    current_app.logger.warning(f"Skipping likely placeholder file: {filename} (size: {file_size} bytes)")
                    continue
                
                # Create a music file object
                music_files.append({
                    'title': os.path.splitext(filename)[0].replace('_', ' '),
                    'path': f'/static/music/{filename}',
                    'filename': filename,
                    'size': file_size
                })
                valid_count += 1
                current_app.logger.debug(f"Added music file: {filename} ({file_size} bytes)")
        
        current_app.logger.info(f"Total files: {file_count}, Valid music files: {valid_count}")
    except Exception as e:
        current_app.logger.error(f"Error reading music directory: {e}")
    
    # Add debug information to response if requested
    if request.args.get('debug') == '1':
        return jsonify({
            'music_files': music_files,
            'debug': {
                'music_dir': music_dir,
                'dir_exists': os.path.exists(music_dir),
                'total_files': file_count if 'file_count' in locals() else 'unknown',
                'valid_files': valid_count if 'valid_count' in locals() else 'unknown'
            }
        })
    
    return jsonify(music_files)

@music.route('/player')
def player():
    """Return HTML for embedding the music player"""
    return '''
    <div id="embedded-jukebox-container"></div>
    <script src="/static/js/jukebox.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Only initialize if no existing player
            if (!document.getElementById('chad-jukebox')) {
                initJukebox('embedded-jukebox-container');
            }
        });
    </script>
    '''

@music.route('/debug')
def debug_music():
    """Debug endpoint to check music system status"""
    music_dir = os.path.join(current_app.static_folder, 'music')
    
    # Collect debug information
    debug_info = {
        'music_directory': {
            'path': music_dir,
            'exists': os.path.exists(music_dir),
            'is_dir': os.path.isdir(music_dir) if os.path.exists(music_dir) else False,
            'permission': 'readable' if os.access(music_dir, os.R_OK) else 'not readable' if os.path.exists(music_dir) else 'n/a'
        },
        'files': []
    }
    
    # Check each file
    if os.path.exists(music_dir) and os.path.isdir(music_dir):
        for filename in os.listdir(music_dir):
            file_path = os.path.join(music_dir, filename)
            file_size = os.path.getsize(file_path) if os.path.isfile(file_path) else 0
            
            debug_info['files'].append({
                'name': filename,
                'size': file_size,
                'size_readable': f"{file_size / 1024:.2f} KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.2f} MB",
                'is_mp3': filename.lower().endswith('.mp3'),
                'valid_size': file_size > 100 * 1024,  # True if > 100KB
                'path': f'/static/music/{filename}' if filename.lower().endswith('.mp3') else None
            })
    
    # Get request information
    debug_info['request'] = {
        'host': request.host,
        'url': request.url,
        'headers': dict(request.headers)
    }
    
    # Return debug information
    return jsonify(debug_info) 