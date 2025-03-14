"""
Test suite for the frontend jukebox functionality.
Tests the JavaScript jukebox player using pytest-selenium.
"""
import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
    
    # Create a test context
    with app.app_context():
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

@pytest.fixture
def selenium_app(app, test_music_files, live_server):
    """Start live server with test app."""
    live_server.start()
    return live_server.url

def test_jukebox_initialization(selenium, selenium_app):
    """Test jukebox player initialization."""
    selenium.get(selenium_app)
    
    # Wait for jukebox to initialize
    player = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jukebox-player"))
    )
    
    # Check player elements
    assert player.is_displayed()
    assert selenium.find_element(By.CLASS_NAME, "play-button").is_displayed()
    assert selenium.find_element(By.CLASS_NAME, "stop-button").is_displayed()
    assert selenium.find_element(By.CLASS_NAME, "next-button").is_displayed()
    assert selenium.find_element(By.CLASS_NAME, "volume-slider").is_displayed()
    assert selenium.find_element(By.CLASS_NAME, "progress-bar").is_displayed()

def test_player_controls(selenium, selenium_app):
    """Test player control functionality."""
    selenium.get(selenium_app)
    
    # Wait for player to initialize
    player = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jukebox-player"))
    )
    
    # Test play button
    play_button = selenium.find_element(By.CLASS_NAME, "play-button")
    play_button.click()
    assert "playing" in player.get_attribute("class")
    
    # Test stop button
    stop_button = selenium.find_element(By.CLASS_NAME, "stop-button")
    stop_button.click()
    assert "playing" not in player.get_attribute("class")
    
    # Test next button
    next_button = selenium.find_element(By.CLASS_NAME, "next-button")
    current_track = selenium.find_element(By.CLASS_NAME, "track-title").text
    next_button.click()
    WebDriverWait(selenium, 10).until(
        lambda s: s.find_element(By.CLASS_NAME, "track-title").text != current_track
    )

def test_volume_control(selenium, selenium_app):
    """Test volume control functionality."""
    selenium.get(selenium_app)
    
    # Wait for player to initialize
    WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jukebox-player"))
    )
    
    # Test volume slider
    volume_slider = selenium.find_element(By.CLASS_NAME, "volume-slider")
    initial_volume = volume_slider.get_attribute("value")
    
    # Change volume using slider
    actions = ActionChains(selenium)
    actions.click_and_hold(volume_slider).move_by_offset(50, 0).release().perform()
    
    assert volume_slider.get_attribute("value") != initial_volume

def test_progress_bar(selenium, selenium_app):
    """Test progress bar functionality."""
    selenium.get(selenium_app)
    
    # Wait for player to initialize
    WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jukebox-player"))
    )
    
    # Start playback
    play_button = selenium.find_element(By.CLASS_NAME, "play-button")
    play_button.click()
    
    # Wait for progress
    progress_bar = selenium.find_element(By.CLASS_NAME, "progress-bar")
    initial_time = progress_bar.get_attribute("value")
    
    WebDriverWait(selenium, 10).until(
        lambda s: s.find_element(By.CLASS_NAME, "progress-bar").get_attribute("value") != initial_time
    )

def test_keyboard_shortcuts(selenium, selenium_app):
    """Test keyboard shortcut functionality."""
    selenium.get(selenium_app)
    
    # Wait for player to initialize
    player = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jukebox-player"))
    )
    
    # Test space bar for play/pause
    selenium.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)
    assert "playing" in player.get_attribute("class")
    
    selenium.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)
    assert "playing" not in player.get_attribute("class")
    
    # Test 'N' key for next track
    current_track = selenium.find_element(By.CLASS_NAME, "track-title").text
    selenium.find_element(By.TAG_NAME, "body").send_keys('n')
    WebDriverWait(selenium, 10).until(
        lambda s: s.find_element(By.CLASS_NAME, "track-title").text != current_track
    )

def test_error_recovery(selenium, selenium_app):
    """Test error recovery functionality."""
    selenium.get(selenium_app)
    
    # Wait for player to initialize
    player = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jukebox-player"))
    )
    
    # Simulate error by trying to play non-existent track
    selenium.execute_script("""
        const audio = document.querySelector('audio');
        audio.dispatchEvent(new Event('error'));
    """)
    
    # Check if player automatically moves to next track
    WebDriverWait(selenium, 10).until(
        lambda s: "error" not in player.get_attribute("class")
    ) 