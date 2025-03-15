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
        os.path.join(current_app.static_folder, 'music'),  # Primary location
        os.environ.get('CHAD_MUSIC_DIR', '')  # Optional environment variable location
    ]
    
    # Track the total number of files processed
    total_files = 0
    valid_music_files = 0
    
    current_app.logger.info(f"Scanning music directories")
    
    found_music_directory = False
    
    for folder in music_folders:
        if not folder or not os.path.exists(folder) or not os.path.isdir(folder):
            current_app.logger.warning(f"Music directory not found or not accessible: {folder}")
            continue
            
        found_music_directory = True
        current_app.logger.info(f"Checking music directory: {folder}")
        
        try:
            # Get all audio files from the folder
            for filename in os.listdir(folder):
                total_files += 1
                if filename.lower().endswith(('.mp3', '.m4a')):
                    file_path = os.path.join(folder, filename)
                    file_size = os.path.getsize(file_path)
                    
                    # Determine path based on directory
                    if folder == os.path.join(current_app.static_folder, 'music'):
                        # If in static/music folder, use /static/music path for web access
                        path = f'/static/music/{filename}'
                    else:
                        # For custom directory, use the custom music endpoint
                        path = f'/music/custom/{filename}'
                    
                    # Create a track object with the correct path
                    track = {
                        'title': os.path.splitext(filename)[0].replace('_', ' '),
                        'path': path,
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
        # Create default placeholder tracks if no real music is found
        if not found_music_directory:
            current_app.logger.warning("No music directories found. Using placeholder tracks.")
            tracks = [
                {
                    'title': 'Demo Track 1',
                    'path': '/static/audio/placeholder.mp3',
                    'filename': 'placeholder.mp3',
                    'size': 0,
                    'type': 'mp3'
                },
                {
                    'title': 'Demo Track 2',
                    'path': '/static/audio/placeholder2.mp3',
                    'filename': 'placeholder2.mp3',
                    'size': 0,
                    'type': 'mp3'
                }
            ]
        else:
            current_app.logger.warning("Music directories found but no music files. Add .mp3 or .m4a files.")
        
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
    
    # Collect file information
    for dir_info in debug_info['music_directories']:
        if dir_info['exists'] and dir_info['is_dir'] and dir_info['permission'] == 'readable':
            folder = dir_info['path']
            for filename in os.listdir(folder):
                if filename.lower().endswith(('.mp3', '.m4a')):
                    file_path = os.path.join(folder, filename)
                    file_size = os.path.getsize(file_path)
                    debug_info['files'].append({
                        'name': filename,
                        'path': file_path,
                        'size': file_size,
                        'type': os.path.splitext(filename)[1][1:].lower()
                    })
    
    return jsonify(debug_info)

@music.route('/create_sample')
@login_required
def create_sample():
    """Create sample music files for testing (dev only)"""
    if not current_app.debug:
        return jsonify({"error": "This endpoint is only available in development mode"}), 403
    
    music_dir = os.path.join(current_app.static_folder, 'music')
    
    # Make sure music directory exists
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
    
    # Create sample text files that simulate music files for testing
    sample_files = [
        {'name': 'sample_track_1.mp3', 'content': 'This is a sample MP3 file for testing'},
        {'name': 'sample_track_2.mp3', 'content': 'Another sample MP3 file for testing'},
        {'name': 'lofi_beats.mp3', 'content': 'A simulated lofi music file for testing'},
        {'name': 'electronic_vibes.m4a', 'content': 'A simulated M4A file for testing'}
    ]
    
    for sample in sample_files:
        file_path = os.path.join(music_dir, sample['name'])
        with open(file_path, 'w') as f:
            f.write(sample['content'])
    
    return jsonify({
        "success": True, 
        "message": f"Created {len(sample_files)} sample files in {music_dir}",
        "files": [s['name'] for s in sample_files]
    }) 