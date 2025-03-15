import os
import json
from datetime import timedelta
from flask import Blueprint, jsonify, send_from_directory, current_app, render_template, request, Response, redirect
from flask_login import login_required, current_user
from app.extensions import limiter, cache
import re

# Create blueprint
music = Blueprint('music', __name__, url_prefix='/music')

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
    
    # Namecheap server path
    music_folder = '/home/chadszv/public_html/music'
    
    # For development environment
    if current_app.config.get('FLASK_ENV') != 'production':
        music_folder = os.path.join(current_app.static_folder, 'music')
        current_app.logger.info(f"Development environment detected, using local path: {music_folder}")
    else:
        current_app.logger.info(f"Production environment detected, using Namecheap path: {music_folder}")
    
    current_app.logger.info(f"Scanning music directory: {music_folder}")
    
    # In production, we can't directly access the Namecheap server files
    # So we'll create entries based on known files
    if current_app.config.get('FLASK_ENV') == 'production':
        current_app.logger.info("Production environment: Using direct URLs to Namecheap server files")
        
        # Get the list of music files from the server
        try:
            # This is a hardcoded list of known files on the Namecheap server
            # We're using direct URLs that will work from the browser
            for i in range(1, 104):  # Assuming files are numbered from 1 to 103
                file_name = f"Be the Chad ({i}).m4a"
                tracks.append({
                    'title': f"Be the Chad {i}",
                    'path': f"https://chadbattles.fun/music/{file_name}",
                    'filename': file_name,
                    'size': 2000000,  # Approximate size
                    'type': 'm4a'
                })
            
            current_app.logger.info(f"Added {len(tracks)} tracks from Namecheap server")
        except Exception as e:
            current_app.logger.error(f"Error creating track list: {str(e)}")
    else:
        # For development, we can scan the local directory
        if os.path.exists(music_folder) and os.path.isdir(music_folder):
            try:
                for filename in os.listdir(music_folder):
                    if filename.lower().endswith(('.mp3', '.m4a', '.wav', '.ogg')):
                        file_path = os.path.join(music_folder, filename)
                        file_size = os.path.getsize(file_path)
                        
                        # For local development
                        path = f'/static/music/{filename}'
                        
                        track = {
                            'title': os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' '),
                            'path': path,
                            'filename': filename,
                            'size': file_size,
                            'type': os.path.splitext(filename)[1][1:].lower()
                        }
                        tracks.append(track)
                        current_app.logger.debug(f"Added track: {track['title']}")
            except Exception as e:
                current_app.logger.error(f"Error reading music directory {music_folder}: {str(e)}")
        else:
            current_app.logger.warning(f"Music directory not found: {music_folder}")
    
    current_app.logger.info(f"Returning {len(tracks)} tracks")
    return jsonify(tracks)

@music.route('/stream/<filename>')
@limiter.limit("100 per hour")
def stream_music(filename):
    """Stream a music file with support for range requests"""
    try:
        # Log the requested file
        current_app.logger.info(f"Streaming request for music file: {filename}")
        
        # Sanitize filename to prevent directory traversal
        filename = os.path.basename(filename)
        
        # In production, redirect to the Namecheap server URL
        if current_app.config.get('FLASK_ENV') == 'production':
            return redirect(f"https://chadbattles.fun/music/{filename}")
        
        # For development, serve from local directory
        music_dir = os.path.join(current_app.static_folder, 'music')
        if os.path.exists(os.path.join(music_dir, filename)):
            return send_from_directory(music_dir, filename)
        else:
            current_app.logger.error(f"Music file not found: {filename}")
            return jsonify({"error": "File not found"}), 404
            
    except Exception as e:
        current_app.logger.error(f"Error streaming music file {filename}: {str(e)}")
        return jsonify({"error": str(e)}), 500

def get_mime_type(filename):
    """Get the MIME type based on file extension"""
    if filename.lower().endswith('.mp3'):
        return 'audio/mpeg'
    elif filename.lower().endswith('.m4a'):
        return 'audio/mp4'
    elif filename.lower().endswith('.wav'):
        return 'audio/wav'
    elif filename.lower().endswith('.ogg'):
        return 'audio/ogg'
    return 'application/octet-stream'

def partial_file_sender(file_path, byte1=0, byte2=None):
    """Generator to send partial file content"""
    file_size = os.path.getsize(file_path)
    
    if byte2 is None:
        byte2 = file_size - 1
    
    length = byte2 - byte1 + 1
    
    with open(file_path, 'rb') as f:
        f.seek(byte1)
        while True:
            chunk_size = min(8192, length)
            if chunk_size <= 0:
                break
            data = f.read(chunk_size)
            if not data:
                break
            length -= len(data)
            yield data

@music.route('/custom/<filename>')
@limiter.limit("100 per hour")
def stream_custom_music(filename):
    """Stream music from a custom location defined in environment variable"""
    try:
        # Sanitize filename to prevent directory traversal
        filename = os.path.basename(filename)
        
        # Get music directory from environment variable or use a fallback
        music_dir = os.environ.get('CHAD_MUSIC_DIR')
        if not music_dir or not os.path.exists(music_dir):
            music_dir = os.path.join(os.path.dirname(current_app.root_path), 'music')
            if not os.path.exists(music_dir):
                return jsonify({"error": "Custom music directory not configured"}), 404
        
        return send_from_directory(music_dir, filename)
    except Exception as e:
        current_app.logger.error(f"Error streaming custom music file {filename}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@music.route('/player')
@limiter.limit("60 per hour")
def player():
    """Music player page"""
    return render_template('music/player.html')

@music.route('/debug')
@limiter.limit("10 per minute")
@login_required  # Require authentication for debug endpoint
def debug_music():
    """Debug endpoint to check music configuration"""
    try:
        if not current_user.is_admin:
            return jsonify({"error": "Admin access required"}), 403
            
        debug_info = {
            "app_root": current_app.root_path,
            "static_folder": current_app.static_folder,
            "music_dirs": []
        }
        
        # Check various music directory locations
        music_dirs = [
            {"name": "static/music", "path": os.path.join(current_app.static_folder, 'music')},
            {"name": "project_root/music", "path": os.path.join(os.path.dirname(current_app.root_path), 'music')},
            {"name": "CHAD_MUSIC_DIR", "path": os.environ.get('CHAD_MUSIC_DIR', 'Not set')},
            {"name": "hosting_server", "path": '/home/chadszv/public_html/music'}
        ]
        
        # Check each directory
        for dir_info in music_dirs:
            dir_path = dir_info["path"]
            dir_exists = os.path.exists(dir_path) if dir_path else False
            is_dir = os.path.isdir(dir_path) if dir_exists else False
            
            dir_debug = {
                "name": dir_info["name"],
                "path": dir_path,
                "exists": dir_exists,
                "is_directory": is_dir,
                "files": []
            }
            
            # If directory exists, list files
            if dir_exists and is_dir:
                try:
                    files = os.listdir(dir_path)
                    music_files = [f for f in files if f.lower().endswith(('.mp3', '.m4a', '.wav', '.ogg'))]
                    
                    for music_file in music_files[:10]:  # Limit to first 10 files
                        file_path = os.path.join(dir_path, music_file)
                        file_info = {
                            "name": music_file,
                            "size": os.path.getsize(file_path),
                            "last_modified": os.path.getmtime(file_path)
                        }
                        dir_debug["files"].append(file_info)
                        
                    dir_debug["file_count"] = len(files)
                    dir_debug["music_file_count"] = len(music_files)
                except Exception as e:
                    dir_debug["error"] = str(e)
            
            debug_info["music_dirs"].append(dir_debug)
            
        # Create static/music if it doesn't exist
        if not os.path.exists(os.path.join(current_app.static_folder, 'music')):
            try:
                os.makedirs(os.path.join(current_app.static_folder, 'music'), exist_ok=True)
                debug_info["created_static_music"] = True
            except Exception as e:
                debug_info["create_static_music_error"] = str(e)
                
        return jsonify(debug_info)
    except Exception as e:
        current_app.logger.error(f"Error in debug endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@music.route('/health')
def health_check():
    """Health check endpoint for the music service"""
    # Check if we can access the static music directory
    static_music = os.path.join(current_app.static_folder, 'music')
    static_music_exists = os.path.exists(static_music) and os.path.isdir(static_music)
    
    # Check if we can access a custom music directory
    custom_music = os.environ.get('CHAD_MUSIC_DIR')
    custom_music_exists = False
    if custom_music:
        custom_music_exists = os.path.exists(custom_music) and os.path.isdir(custom_music)
        
    # Check if any music directory is available
    any_music_dir_available = static_music_exists or custom_music_exists
    
    # Return health status
    return jsonify({
        "status": "healthy" if any_music_dir_available else "degraded",
        "static_music_available": static_music_exists,
        "custom_music_available": custom_music_exists,
        "timestamp": datetime.now().isoformat()
    }) 