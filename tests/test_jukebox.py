"""
Test suite for the frontend jukebox functionality.
Tests the JavaScript jukebox player using pytest-flask.
"""
import os
import pytest
from flask import url_for
from app import create_app

@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['MUSIC_DIR'] = os.path.join(os.path.dirname(__file__), 'test_music')
    
    # Create test music directory if it doesn't exist
    if not os.path.exists(app.config['MUSIC_DIR']):
        os.makedirs(app.config['MUSIC_DIR'])
    
    yield app
    
    # Clean up test music directory
    if os.path.exists(app.config['MUSIC_DIR']):
        for file in os.listdir(app.config['MUSIC_DIR']):
            os.remove(os.path.join(app.config['MUSIC_DIR'], file))
        os.rmdir(app.config['MUSIC_DIR'])

@pytest.fixture
def test_music_files(app):
    """Create test music files."""
    music_dir = app.config['MUSIC_DIR']
    files = {
        'test1.mp3': b'fake mp3 content',
        'test2.m4a': b'fake m4a content'
    }
    
    for filename, content in files.items():
        with open(os.path.join(music_dir, filename), 'wb') as f:
            f.write(content)
    
    return files

@pytest.mark.webtest
def test_jukebox_initialization(client, test_music_files):
    """Test jukebox player initialization."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'jukebox-player' in response.data
    assert b'play-button' in response.data
    assert b'stop-button' in response.data
    assert b'next-button' in response.data
    assert b'volume-slider' in response.data
    assert b'progress-bar' in response.data

@pytest.mark.webtest
def test_track_list(client, test_music_files):
    """Test track list endpoint."""
    response = client.get('/tracks')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert any(track['filename'] == 'test1.mp3' for track in data)
    assert any(track['filename'] == 'test2.m4a' for track in data)

@pytest.mark.webtest
def test_stream_music(client, test_music_files):
    """Test music streaming endpoint."""
    response = client.get('/stream/test1.mp3')
    assert response.status_code == 200
    assert response.data == b'fake mp3 content'
    
    response = client.get('/stream/test2.m4a')
    assert response.status_code == 200
    assert response.data == b'fake m4a content'
    
    response = client.get('/stream/nonexistent.mp3')
    assert response.status_code == 404

@pytest.mark.webtest
def test_rate_limiting(client, test_music_files):
    """Test rate limiting on music endpoints."""
    # Test track list rate limiting
    for _ in range(30):
        response = client.get('/tracks')
        assert response.status_code == 200
    response = client.get('/tracks')
    assert response.status_code == 429  # Too Many Requests
    
    # Test streaming rate limiting
    for _ in range(100):
        response = client.get('/stream/test1.mp3')
        assert response.status_code == 200
    response = client.get('/stream/test1.mp3')
    assert response.status_code == 429  # Too Many Requests 