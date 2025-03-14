"""
Test suite for the music system functionality.
Tests both backend routes and frontend player functionality.
"""
import os
import pytest
import json
from flask import url_for
from unittest.mock import patch, MagicMock
from app import create_app
from app.extensions import db, cache

@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['MUSIC_DIR'] = os.path.join(os.path.dirname(__file__), 'test_music')
    
    # Create test music directory if it doesn't exist
    if not os.path.exists(app.config['MUSIC_DIR']):
        os.makedirs(app.config['MUSIC_DIR'])
    
    # Create a test context
    with app.app_context():
        yield app
    
    # Clean up test music directory
    if os.path.exists(app.config['MUSIC_DIR']):
        for file in os.listdir(app.config['MUSIC_DIR']):
            os.remove(os.path.join(app.config['MUSIC_DIR'], file))
        os.rmdir(app.config['MUSIC_DIR'])

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def test_music_files(app):
    """Create test music files."""
    music_dir = app.config['MUSIC_DIR']
    files = {
        'test1.mp3': b'fake mp3 content',
        'test2.m4a': b'fake m4a content',
        'test3.txt': b'not a music file'
    }
    
    for filename, content in files.items():
        with open(os.path.join(music_dir, filename), 'wb') as f:
            f.write(content)
    
    return files

def test_list_tracks(client, test_music_files):
    """Test the /music/tracks endpoint."""
    response = client.get('/music/tracks')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2  # Only .mp3 and .m4a files
    
    # Verify response format
    for track in data:
        assert set(track.keys()) == {'title', 'path', 'filename', 'size', 'type'}
        assert track['type'] in ['mp3', 'm4a']
        assert track['size'] > 0

def test_stream_music(client, test_music_files):
    """Test the music streaming endpoint."""
    # Test successful streaming
    response = client.get('/music/stream/test1.mp3')
    assert response.status_code == 200
    assert response.data == b'fake mp3 content'
    
    # Test range request
    response = client.get('/music/stream/test1.mp3', headers={'Range': 'bytes=0-4'})
    assert response.status_code == 206
    assert response.data == b'fake '
    assert 'Content-Range' in response.headers
    
    # Test non-existent file
    response = client.get('/music/stream/nonexistent.mp3')
    assert response.status_code == 404

def test_file_type_validation(client, test_music_files):
    """Test file type validation."""
    # Try to access non-music file
    response = client.get('/music/stream/test3.txt')
    assert response.status_code == 404

def test_rate_limiting(client, test_music_files):
    """Test rate limiting on music endpoints."""
    # Make multiple requests to trigger rate limiting
    for _ in range(35):  # Exceeds the 30 per minute limit
        response = client.get('/music/tracks')
    
    # The next request should be rate limited
    response = client.get('/music/tracks')
    assert response.status_code == 429

def test_caching(client, test_music_files):
    """Test caching behavior."""
    # First request should not be cached
    response1 = client.get('/music/tracks')
    assert response1.status_code == 200
    
    # Second request should be cached
    with patch('app.routes.music.get_tracks') as mock_get_tracks:
        response2 = client.get('/music/tracks')
        assert response2.status_code == 200
        mock_get_tracks.assert_not_called()

def test_compression(client, test_music_files):
    """Test response compression."""
    response = client.get('/music/tracks', headers={
        'Accept-Encoding': 'gzip, deflate'
    })
    assert response.status_code == 200
    assert response.headers.get('Content-Encoding') == 'gzip'

def test_cors_headers(client):
    """Test CORS headers on music endpoints."""
    response = client.get('/music/tracks')
    assert response.headers.get('Access-Control-Allow-Origin') == '*'
    assert 'GET, OPTIONS' in response.headers.get('Access-Control-Allow-Methods')

def test_error_handling(client):
    """Test error handling in music routes."""
    # Test invalid range header
    response = client.get('/music/stream/test1.mp3', headers={'Range': 'invalid'})
    assert response.status_code == 400
    
    # Test missing file
    response = client.get('/music/stream/nonexistent.mp3')
    assert response.status_code == 404
    assert b'File not found' in response.data

def test_frontend_player(client):
    """Test frontend player functionality."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'jukebox.js' in response.data 