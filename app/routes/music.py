import os
import json
from datetime import timedelta
from flask import Blueprint, jsonify, send_from_directory, current_app, render_template, request, Response
from flask_login import login_required, current_user
from app.extensions import limiter, cache
import re

# Create blueprint
music = Blueprint('music', __name__)

# Apply rate limiting to the entire blueprint
@music.before_request
def before_request():
    """Add CORS and Cache headers to all responses"""
    if request.method == 'OPTIONS':
        return Response('', 204, headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '86400'  # 24 hours
        })

@music.after_request
def after_request(response):
    """Add CORS and Cache headers to all responses"""
    # Add CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    
    # Add caching headers for successful GET requests
    if request.method == 'GET' and response.status_code == 200:
        # Cache audio files for 1 day
        if response.mimetype.startswith('audio/'):
            response.headers['Cache-Control'] = 'public, max-age=86400'
        # Cache JSON responses for 5 minutes
        elif response.mimetype == 'application/json':
            response.headers['Cache-Control'] = 'public, max-age=300'
    
    return response

@music.route('/tracks')
@limiter.limit("30 per minute")
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_tracks():
    """Return a list of all music tracks"""
    tracks = []
    
    # Define music directories to check
    music_folders = [
        '/public_html/music',  # Primary location on nameserver
        os.path.join(current_app.static_folder, 'music'),  # Fallback location
        os.environ.get('CHAD_MUSIC_DIR', '')  # Optional environment variable location
    ]
    
    # Track the total number of files processed
    total_files = 0
    valid_music_files = 0
    
    current_app.logger.info(f"Scanning music directories")
    
    for folder in music_folders:
        if not folder or not os.path.exists(folder) or not os.path.isdir(folder):
            current_app.logger.warning(f"Music directory not found or not accessible: {folder}")
            continue
            
        current_app.logger.info(f"Checking music directory: {folder}")
        
        try:
            # Get all audio files from the folder
            for filename in os.listdir(folder):
                total_files += 1
                if filename.lower().endswith(('.mp3', '.m4a')):
                    file_path = os.path.join(folder, filename)
                    file_size = os.path.getsize(file_path)
                    
                    # Create a track object with the correct path
                    track = {
                        'title': os.path.splitext(filename)[0].replace('_', ' '),
                        'path': f'/music/{filename}',  # Use direct path since files are in public_html/music
                        'filename': filename,
                        'size': file_size,
                        'type': os.path.splitext(filename)[1][1:].lower()
                    }
                    tracks.append(track)
                    valid_music_files += 1
                    current_app.logger.debug(f"Added track: {track['title']} ({file_size} bytes)")
        except Exception as e:
            current_app.logger.error(f"Error reading music directory {folder}: {e}")
    
    current_app.logger.info(f"Processed total of {total_files} files, found {valid_music_files} valid music files")
    
    if not tracks:
        current_app.logger.warning("No music files found in any directory")
        
    return jsonify(tracks)

@music.route('/stream/<filename>')
@limiter.limit("100 per hour")
def stream_music(filename):
    """Stream a music file with support for range requests"""
    try:
        music_dir = os.path.join(current_app.static_folder, 'music')
        file_path = None
        
        # Check main music directory
        if os.path.exists(os.path.join(music_dir, filename)):
            file_path = os.path.join(music_dir, filename)
        else:
            # Try alternative music directory
            alt_music_dir = os.environ.get('CHAD_MUSIC_DIR')
            if alt_music_dir and os.path.exists(os.path.join(alt_music_dir, filename)):
                file_path = os.path.join(alt_music_dir, filename)
        
        if not file_path:
            current_app.logger.error(f"Music file not found: {filename}")
            return jsonify({"error": "File not found"}), 404
            
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Handle range request
        range_header = request.headers.get('Range')
        
        if range_header:
            byte1, byte2 = 0, None
            match = re.search(r'(\d+)-(\d*)', range_header)
            groups = match.groups()
            
            if groups[0]:
                byte1 = int(groups[0])
            if groups[1]:
                byte2 = int(groups[1])
            
            if byte2 is None:
                byte2 = file_size - 1
            
            length = byte2 - byte1 + 1
            
            resp = Response(
                partial_file_sender(file_path, byte1, byte2),
                206,
                mimetype=get_mime_type(filename),
                direct_passthrough=True
            )
            
            resp.headers.add('Content-Range', f'bytes {byte1}-{byte2}/{file_size}')
            resp.headers.add('Accept-Ranges', 'bytes')
            resp.headers.add('Content-Length', str(length))
            return resp
        
        return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))
        
    except Exception as e:
        current_app.logger.error(f"Error streaming music file: {e}")
        return jsonify({"error": "File not found"}), 404

def get_mime_type(filename):
    """Get the MIME type based on file extension"""
    if filename.lower().endswith('.mp3'):
        return 'audio/mpeg'
    elif filename.lower().endswith('.m4a'):
        return 'audio/mp4'
    return 'application/octet-stream'

def partial_file_sender(file_path, byte1=0, byte2=None):
    """Generator to send partial file content"""
    file_size = os.path.getsize(file_path)
    
    if byte2 is None:
        byte2 = file_size - 1
    
    with open(file_path, 'rb') as f:
        f.seek(byte1)
        chunk_size = 8192
        remaining = byte2 - byte1 + 1
        
        while True:
            if remaining <= 0:
                break
            chunk = f.read(min(chunk_size, remaining))
            if not chunk:
                break
            remaining -= len(chunk)
            yield chunk

@music.route('/custom/<filename>')
@limiter.limit("100 per hour")
def stream_custom_music(filename):
    """Stream a music file from the custom directory with range request support"""
    try:
        custom_music_dir = os.environ.get('CHAD_MUSIC_DIR')
        if not custom_music_dir or not os.path.exists(os.path.join(custom_music_dir, filename)):
            current_app.logger.error(f"Custom music file not found: {filename}")
            return jsonify({"error": "File not found"}), 404
            
        file_path = os.path.join(custom_music_dir, filename)
        return stream_music(filename)
        
    except Exception as e:
        current_app.logger.error(f"Error streaming custom music file: {e}")
        return jsonify({"error": "File not found"}), 404

@music.route('/player')
@limiter.limit("60 per hour")
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
@limiter.limit("10 per minute")
@login_required  # Require authentication for debug endpoint
def debug_music():
    """Debug endpoint to check music system status"""
    if not current_app.debug:
        return jsonify({"error": "Debug endpoint only available in development"}), 403
        
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
                'file_count': len([f for f in os.listdir(music_dir) if f.lower().endswith(('.mp3', '.m4a'))]) if os.path.exists(music_dir) and os.path.isdir(music_dir) else 0
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
            'file_count': len([f for f in os.listdir(custom_dir) if f.lower().endswith(('.mp3', '.m4a'))]) if os.path.exists(custom_dir) and os.path.isdir(custom_dir) else 0
        })
    
    # Check each file in the default music directory
    if os.path.exists(music_dir) and os.path.isdir(music_dir):
        for filename in os.listdir(music_dir):
            file_path = os.path.join(music_dir, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.mp3', '.m4a')):
                file_size = os.path.getsize(file_path)
                
                debug_info['files'].append({
                    'name': filename,
                    'size': file_size,
                    'size_readable': f"{file_size / 1024:.2f} KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.2f} MB",
                    'path': f'/static/music/{filename}',
                    'type': os.path.splitext(filename)[1][1:].lower()
                })
    
    # Get request information
    debug_info['request'] = {
        'host': request.host,
        'url': request.url,
        'headers': dict(request.headers)
    }
    
    return jsonify(debug_info) 