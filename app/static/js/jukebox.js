/**
 * Simple Jukebox Music Player
 * Plays MP3 files randomly with basic controls
 */
class Jukebox {
    constructor(containerId, musicFiles = []) {
        this.container = document.getElementById(containerId);
        this.musicFiles = musicFiles;
        this.currentTrack = null;
        this.isPlaying = false;
        this.audio = new Audio();
        this.currentTrackIndex = -1;
        
        // Set up event listener for when a song ends
        this.audio.addEventListener('ended', () => this.playNextRandom());
        
        // Create the player if container exists
        if (this.container) {
            this.createPlayer();
        } else {
            console.error(`Container with ID ${containerId} not found`);
        }
    }
    
    createPlayer() {
        // Create player UI
        this.container.innerHTML = `
            <div class="jukebox-player">
                <div class="jukebox-title">Chad Battles Jukebox</div>
                <div class="jukebox-controls">
                    <button id="jukebox-play" class="jukebox-btn">▶ Play</button>
                    <button id="jukebox-stop" class="jukebox-btn">■ Stop</button>
                    <button id="jukebox-next" class="jukebox-btn">⏭ Next</button>
                </div>
                <div id="jukebox-now-playing" class="jukebox-now-playing">Select a track to begin</div>
            </div>
        `;
        
        // Add some basic styling
        const style = document.createElement('style');
        style.textContent = `
            .jukebox-player {
                background-color: #333;
                border-radius: 10px;
                padding: 15px;
                color: white;
                font-family: Arial, sans-serif;
                width: 300px;
            }
            .jukebox-title {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
                text-align: center;
            }
            .jukebox-controls {
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
            }
            .jukebox-btn {
                background-color: #555;
                border: none;
                color: white;
                padding: 8px 12px;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .jukebox-btn:hover {
                background-color: #777;
            }
            .jukebox-now-playing {
                font-size: 14px;
                text-align: center;
                font-style: italic;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
        `;
        document.head.appendChild(style);
        
        // Add event listeners
        document.getElementById('jukebox-play').addEventListener('click', () => this.play());
        document.getElementById('jukebox-stop').addEventListener('click', () => this.stop());
        document.getElementById('jukebox-next').addEventListener('click', () => this.playNextRandom());
    }
    
    loadMusicFiles() {
        // This function can be used to load music files from the server
        // For now, we'll just use the provided array
        if (this.musicFiles.length === 0) {
            // If no music files provided, use a default set
            console.warn('No music files provided, using default empty array');
        }
    }
    
    play() {
        if (!this.isPlaying) {
            if (this.currentTrackIndex === -1) {
                this.playNextRandom();
            } else {
                this.audio.play();
                this.isPlaying = true;
                document.getElementById('jukebox-play').textContent = '⏸ Pause';
            }
        } else {
            // If already playing, this acts as pause
            this.audio.pause();
            this.isPlaying = false;
            document.getElementById('jukebox-play').textContent = '▶ Play';
        }
    }
    
    stop() {
        this.audio.pause();
        this.audio.currentTime = 0;
        this.isPlaying = false;
        document.getElementById('jukebox-play').textContent = '▶ Play';
        document.getElementById('jukebox-now-playing').textContent = 'Music stopped';
    }
    
    playNextRandom() {
        if (this.musicFiles.length === 0) {
            document.getElementById('jukebox-now-playing').textContent = 'No music files available';
            return;
        }
        
        // Choose a random track, but not the same one that's currently playing
        let newIndex;
        if (this.musicFiles.length === 1) {
            newIndex = 0;
        } else {
            do {
                newIndex = Math.floor(Math.random() * this.musicFiles.length);
            } while (newIndex === this.currentTrackIndex);
        }
        
        this.currentTrackIndex = newIndex;
        this.currentTrack = this.musicFiles[this.currentTrackIndex];
        
        // Update the audio source
        this.audio.src = this.currentTrack.path;
        
        // Update the display
        document.getElementById('jukebox-now-playing').textContent = `Now playing: ${this.currentTrack.title}`;
        
        // Play the track
        this.audio.play();
        this.isPlaying = true;
        document.getElementById('jukebox-play').textContent = '⏸ Pause';
    }
    
    // Method to set new music files
    setMusicFiles(musicFiles) {
        this.musicFiles = musicFiles;
        // If we're already playing, stop the current track
        if (this.isPlaying) {
            this.stop();
        }
        this.currentTrackIndex = -1;
    }
}

// Function to initialize the jukebox with music files from the server
function initJukebox(containerId) {
    // Create an AJAX request to get the music files
    fetch('/music/list')
        .then(response => response.json())
        .then(data => {
            const jukebox = new Jukebox(containerId, data);
            window.jukebox = jukebox; // Make it globally accessible
        })
        .catch(error => {
            console.error('Error loading music files:', error);
            // Initialize with empty array as fallback
            const jukebox = new Jukebox(containerId, []);
            window.jukebox = jukebox;
        });
} 