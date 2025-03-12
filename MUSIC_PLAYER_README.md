# Chad Battles Music Player (Jukebox)

This document explains how to set up and use the new music player (jukebox) feature for the Chad Battles website.

## Features

- Auto-plays a random song when the website loads
- Play/pause functionality
- Skip to next or previous song
- Volume control (starts at 40% by default)
- Collapsible player interface
- Works across all pages of the website

## Installation

1. The following files have been added to your project:
   - `app/static/js/jukebox.js` - JavaScript for the music player
   - `app/static/css/jukebox.css` - CSS styles for the player
   - `app/routes/music.py` - Flask routes for serving music files
   - `register_music_blueprint.py` - Helper script to register the music blueprint

2. The layout template (`app/templates/layout.html`) has been updated to include:
   - The music player HTML structure
   - Font Awesome icons for player controls
   - CSS styles to improve text readability throughout the site

## Setup Instructions

1. Run the blueprint registration script:
   ```
   python register_music_blueprint.py
   ```

2. Make sure your music files are in the correct location:
   - The player looks for MP3 files in the `ChadBattlesWebsiteMusic` folder
   - All MP3 files in this folder will be automatically detected and playable

3. Restart your Flask application:
   ```
   python run.py
   ```

## Usage

- The player appears as a music note icon in the bottom right corner of every page
- Click the icon to expand/collapse the player controls
- Use the play/pause button to control playback
- Use the forward/backward buttons to change tracks
- Adjust the volume slider to control the sound level

## Customization

You can customize the player appearance by modifying the `app/static/css/jukebox.css` file. Key elements:

- `.jukebox-container` - The main container for the player
- `.jukebox-toggle` - The toggle button that shows/hides the player
- `.jukebox-controls` - The control panel
- `.jukebox-btn` - The player buttons

## Troubleshooting

If the music player doesn't work properly:

1. Check browser console for JavaScript errors
2. Make sure the music files are accessible at the expected path
3. Verify that the music blueprint was registered correctly in `app/__init__.py`
4. Ensure that static files are being served properly

For any issues, contact the development team for assistance. 