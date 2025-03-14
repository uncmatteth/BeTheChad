import os
import json
from flask import Blueprint, jsonify, send_from_directory, current_app, render_template
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
        for filename in os.listdir(music_dir):
            if filename.endswith('.mp3'):
                # Create a track object
                track = {
                    'title': os.path.splitext(filename)[0],
                    'path': f'/static/music/{filename}',
                    'filename': filename
                }
                tracks.append(track)
    except Exception as e:
        current_app.logger.error(f"Error reading music directory: {e}")
        
    return jsonify(tracks)

@music.route('/stream/<filename>')
def stream_music(filename):
    """Stream a music file"""
    try:
        music_dir = os.path.join(current_app.static_folder, 'music')
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
    
    # Get all MP3 files
    try:
        for filename in os.listdir(music_dir):
            if filename.lower().endswith('.mp3'):
                # Create a music file object
                music_files.append({
                    'title': os.path.splitext(filename)[0].replace('_', ' '),
                    'path': f'/static/music/{filename}',
                    'filename': filename
                })
    except Exception as e:
        current_app.logger.error(f"Error reading music directory: {e}")
    
    return jsonify(music_files)

@music.route('/player')
def player():
    """Return HTML for embedding the music player"""
    return '''
    <div id="jukebox-container"></div>
    <script src="/static/js/jukebox.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            initJukebox('jukebox-container');
        });
    </script>
    '''

@music.route('/demo')
def demo():
    """Show a demo page for the music player"""
    return render_template('music_demo.html') 