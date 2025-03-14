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
    
    # Add potential additional music folders to check
    music_folders = [
        music_dir,  # Default location in static folder
        os.environ.get('CHAD_MUSIC_DIR', '')  # Optional environment variable for custom location
    ]
    
    # Track the total number of files processed
    total_files = 0
    valid_music_files = 0
    
    current_app.logger.info(f"Scanning music directories")
    
    for folder in music_folders:
        if not folder or not os.path.exists(folder) or not os.path.isdir(folder):
            continue
            
        current_app.logger.info(f"Checking music directory: {folder}")
        
        try:
            # Get all MP3 files from the folder
            for filename in os.listdir(folder):
                total_files += 1
                if filename.endswith('.mp3'):
                    file_path = os.path.join(folder, filename)
                    file_size = os.path.getsize(file_path)
                    
                    # Create a track object - no longer skipping small files
                    # as we want to include all music files
                    track = {
                        'title': os.path.splitext(filename)[0].replace('_', ' '),
                        'path': f'/static/music/{filename}' if folder == music_dir else f'/music/custom/{os.path.basename(filename)}',
                        'filename': filename,
                        'size': file_size
                    }
                    tracks.append(track)
                    valid_music_files += 1
                    current_app.logger.debug(f"Added track: {track['title']} ({file_size} bytes)")
        except Exception as e:
            current_app.logger.error(f"Error reading music directory {folder}: {e}")
    
    current_app.logger.info(f"Processed total of {total_files} files, found {valid_music_files} valid music files")
        
    return jsonify(tracks)

@music.route('/stream/<filename>')
def stream_music(filename):
    """Stream a music file"""
    try:
        music_dir = os.path.join(current_app.static_folder, 'music')
        if not os.path.exists(os.path.join(music_dir, filename)):
            # Try alternative music directory from environment variable
            alt_music_dir = os.environ.get('CHAD_MUSIC_DIR')
            if alt_music_dir and os.path.exists(os.path.join(alt_music_dir, filename)):
                return send_from_directory(alt_music_dir, filename)
            else:
                current_app.logger.error(f"Music file not found: {filename}")
                return jsonify({"error": "File not found"}), 404
            
        current_app.logger.info(f"Streaming music file: {filename}")
        return send_from_directory(music_dir, filename)
    except Exception as e:
        current_app.logger.error(f"Error streaming music file: {e}")
        return jsonify({"error": "File not found"}), 404

@music.route('/custom/<filename>')
def stream_custom_music(filename):
    """Stream a music file from the custom directory"""
    try:
        custom_music_dir = os.environ.get('CHAD_MUSIC_DIR')
        if not custom_music_dir or not os.path.exists(os.path.join(custom_music_dir, filename)):
            current_app.logger.error(f"Custom music file not found: {filename}")
            return jsonify({"error": "File not found"}), 404
            
        current_app.logger.info(f"Streaming custom music file: {filename}")
        return send_from_directory(custom_music_dir, filename)
    except Exception as e:
        current_app.logger.error(f"Error streaming custom music file: {e}")
        return jsonify({"error": "File not found"}), 404

@music.route('/list')
def list_music():
    """Return a list of all available music files"""
    music_files = []
    
    # Get music directory from the static folder
    music_dir = os.path.join(current_app.static_folder, 'music')
    
    # Add potential additional music folders to check
    music_folders = [
        music_dir,  # Default location in static folder
        os.environ.get('CHAD_MUSIC_DIR', '')  # Optional environment variable for custom location
    ]
    
    # Track the total number of files processed
    total_files = 0
    valid_music_files = 0
    
    for folder in music_folders:
        if not folder or not os.path.exists(folder) or not os.path.isdir(folder):
            continue
            
        current_app.logger.info(f"Checking music directory: {folder}")
        
        try:
            # Get all MP3 files from the folder
            for filename in os.listdir(folder):
                total_files += 1
                if filename.lower().endswith('.mp3'):
                    file_path = os.path.join(folder, filename)
                    file_size = os.path.getsize(file_path)
                    
                    # Create a music file object - no longer skipping small files
                    music_files.append({
                        'title': os.path.splitext(filename)[0].replace('_', ' '),
                        'path': f'/static/music/{filename}' if folder == music_dir else f'/music/custom/{os.path.basename(filename)}',
                        'filename': filename,
                        'size': file_size
                    })
                    valid_music_files += 1
                    current_app.logger.debug(f"Added music file: {filename} ({file_size} bytes)")
        except Exception as e:
            current_app.logger.error(f"Error reading music directory {folder}: {e}")
    
    current_app.logger.info(f"Total files scanned: {total_files}, Valid music files: {valid_music_files}")
    
    # Add debug information to response if requested
    if request.args.get('debug') == '1':
        return jsonify({
            'music_files': music_files,
            'debug': {
                'music_dirs': [d for d in music_folders if d],
                'dirs_exist': [os.path.exists(d) for d in music_folders if d],
                'total_files': total_files,
                'valid_files': valid_music_files
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
    custom_dir = os.environ.get('CHAD_MUSIC_DIR', '')
    
    # Collect debug information
    debug_info = {
        'music_directories': [
            {
                'path': music_dir,
                'exists': os.path.exists(music_dir),
                'is_dir': os.path.isdir(music_dir) if os.path.exists(music_dir) else False,
                'permission': 'readable' if os.access(music_dir, os.R_OK) else 'not readable' if os.path.exists(music_dir) else 'n/a',
                'file_count': len([f for f in os.listdir(music_dir) if f.lower().endswith('.mp3')]) if os.path.exists(music_dir) and os.path.isdir(music_dir) else 0
            }
        ],
        'files': []
    }
    
    # Add custom directory if set
    if custom_dir:
        debug_info['music_directories'].append({
            'path': custom_dir,
            'exists': os.path.exists(custom_dir),
            'is_dir': os.path.isdir(custom_dir) if os.path.exists(custom_dir) else False,
            'permission': 'readable' if os.access(custom_dir, os.R_OK) else 'not readable' if os.path.exists(custom_dir) else 'n/a',
            'file_count': len([f for f in os.listdir(custom_dir) if f.lower().endswith('.mp3')]) if os.path.exists(custom_dir) and os.path.isdir(custom_dir) else 0
        })
    
    # Check each file in the default music directory
    if os.path.exists(music_dir) and os.path.isdir(music_dir):
        for filename in os.listdir(music_dir):
            file_path = os.path.join(music_dir, filename)
            if os.path.isfile(file_path) and filename.lower().endswith('.mp3'):
                file_size = os.path.getsize(file_path)
                
                debug_info['files'].append({
                    'name': filename,
                    'size': file_size,
                    'size_readable': f"{file_size / 1024:.2f} KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.2f} MB",
                    'path': f'/static/music/{filename}'
                })
    
    # Get request information
    debug_info['request'] = {
        'host': request.host,
        'url': request.url,
        'headers': dict(request.headers)
    }
    
    # Return debug information
    return jsonify(debug_info) 