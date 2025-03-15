/**
 * Enhanced Jukebox Music Player
 * Plays MP3 and M4A files with advanced controls
 */
class Jukebox {
    constructor(containerId, musicFiles = []) {
        this.container = document.getElementById(containerId);
        this.musicFiles = musicFiles;
        this.currentTrack = null;
        this.isPlaying = false;
        this.audio = new Audio();
        this.currentTrackIndex = -1;
        this.volume = localStorage.getItem('jukebox_volume') || 0.7;
        this.isMuted = localStorage.getItem('jukebox-muted') === 'true';
        this.isShuffleEnabled = true; // Always shuffle for Chad Battles
        
        // Set initial volume
        this.audio.volume = this.isMuted ? 0 : this.volume;
        
        // Set up event listeners
        this.audio.addEventListener('ended', () => this.playNextRandom());
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.audio.addEventListener('error', (e) => this.handleError(e));
        
        // Create the player if container exists
        if (this.container) {
            this.createPlayer();
            this.loadState();
            // Start playing automatically
            if (this.musicFiles.length > 0) {
                this.playNextRandom();
            }
        } else {
            console.error(`Container with ID ${containerId} not found`);
        }
    }
    
    createPlayer() {
        // Create player UI with volume control and progress bar
        this.container.innerHTML = `
            <div class="jukebox-player" id="chad-jukebox">
                <div class="jukebox-title">Chad Battles Jukebox</div>
                <div class="jukebox-progress">
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                    <div class="progress-time">
                        <span class="current-time">0:00</span>
                        <span class="total-time">0:00</span>
                    </div>
                </div>
                <div class="jukebox-controls">
                    <button id="jukebox-play" class="jukebox-btn">▶ Play</button>
                    <button id="jukebox-stop" class="jukebox-btn">■ Stop</button>
                    <button id="jukebox-next" class="jukebox-btn">⏭ Next</button>
                    <div class="volume-control">
                        <span class="volume-icon">🔊</span>
                        <input type="range" id="volume-slider" min="0" max="100" value="${this.volume * 100}">
                    </div>
                </div>
                <div id="jukebox-now-playing" class="jukebox-now-playing">Loading music...</div>
            </div>
        `;
        
        // Add enhanced styling
        const style = document.createElement('style');
        style.textContent = `
            .jukebox-player {
                background-color: #333;
                border-radius: 10px;
                padding: 15px;
                color: white;
                font-family: Arial, sans-serif;
                width: 300px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .jukebox-title {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
                text-align: center;
            }
            .jukebox-progress {
                margin-bottom: 15px;
            }
            .progress-bar {
                background-color: #555;
                height: 6px;
                border-radius: 3px;
                cursor: pointer;
                position: relative;
            }
            .progress-fill {
                background-color: #4CAF50;
                height: 100%;
                border-radius: 3px;
                width: 0%;
                transition: width 0.1s;
            }
            .progress-time {
                display: flex;
                justify-content: space-between;
                font-size: 12px;
                margin-top: 5px;
            }
            .jukebox-controls {
                display: flex;
                justify-content: space-between;
                align-items: center;
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
            .volume-control {
                display: flex;
                align-items: center;
                gap: 5px;
            }
            .volume-icon {
                font-size: 16px;
                cursor: pointer;
            }
            #volume-slider {
                width: 80px;
                height: 4px;
            }
            .jukebox-now-playing {
                font-size: 14px;
                text-align: center;
                font-style: italic;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                padding: 5px;
                background-color: #444;
                border-radius: 5px;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            .fade-in {
                animation: fadeIn 0.3s ease-in;
            }
        `;
        document.head.appendChild(style);
        
        // Add event listeners
        document.getElementById('jukebox-play').addEventListener('click', () => this.play());
        document.getElementById('jukebox-stop').addEventListener('click', () => this.stop());
        document.getElementById('jukebox-next').addEventListener('click', () => this.playNextRandom());
        
        // Volume control
        const volumeSlider = document.getElementById('volume-slider');
        volumeSlider.addEventListener('input', (e) => {
            this.setVolume(e.target.value / 100);
        });
        
        // Progress bar
        const progressBar = this.container.querySelector('.progress-bar');
        progressBar.addEventListener('click', (e) => {
            const rect = progressBar.getBoundingClientRect();
            const pos = (e.clientX - rect.left) / rect.width;
            this.seekTo(pos);
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT') return;
            switch(e.key) {
                case ' ':
                    e.preventDefault();
                    this.play();
                    break;
                case 'n':
                    this.playNextRandom();
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    this.setVolume(Math.min(1, this.volume + 0.1));
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    this.setVolume(Math.max(0, this.volume - 0.1));
                    break;
            }
        });
    }
    
    setVolume(value) {
        this.volume = Math.max(0, Math.min(1, value));
        this.audio.volume = this.isMuted ? 0 : this.volume;
        document.getElementById('volume-slider').value = this.volume * 100;
        localStorage.setItem('jukebox_volume', this.volume);
        this.updateMuteButton();
    }
    
    seekTo(position) {
        if (this.audio.duration) {
            this.audio.currentTime = position * this.audio.duration;
        }
    }
    
    updateProgress() {
        if (!this.audio.duration) return;
        
        const progressFill = this.container.querySelector('.progress-fill');
        const currentTime = this.container.querySelector('.current-time');
        const totalTime = this.container.querySelector('.total-time');
        
        const progress = (this.audio.currentTime / this.audio.duration) * 100;
        progressFill.style.width = `${progress}%`;
        
        currentTime.textContent = this.formatTime(this.audio.currentTime);
        totalTime.textContent = this.formatTime(this.audio.duration);
    }
    
    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    handleError(error) {
        console.error('Audio playback error:', error);
        const nowPlaying = document.getElementById('jukebox-now-playing');
        nowPlaying.textContent = 'Error playing track. Trying next...';
        setTimeout(() => this.playNextRandom(), 2000);
    }
    
    loadState() {
        const savedState = localStorage.getItem('jukebox_state');
        if (savedState) {
            const state = JSON.parse(savedState);
            if (state.currentTrackIndex >= 0 && state.currentTrackIndex < this.musicFiles.length) {
                this.currentTrackIndex = state.currentTrackIndex;
                this.currentTrack = this.musicFiles[this.currentTrackIndex];
                this.audio.src = this.currentTrack.path;
                if (state.currentTime) {
                    this.audio.currentTime = state.currentTime;
                }
                document.getElementById('jukebox-now-playing').textContent = 
                    `Now playing: ${this.currentTrack.title}`;
            }
        }
    }
    
    saveState() {
        const state = {
            currentTrackIndex: this.currentTrackIndex,
            currentTime: this.audio.currentTime
        };
        localStorage.setItem('jukebox_state', JSON.stringify(state));
    }
    
    play() {
        if (!this.isPlaying) {
            if (this.currentTrackIndex === -1) {
                this.playNextRandom();
            } else {
                this.audio.play()
                    .then(() => {
                        this.isPlaying = true;
                        document.getElementById('jukebox-play').textContent = '⏸ Pause';
                    })
                    .catch(error => this.handleError(error));
            }
        } else {
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
        this.updateProgress();
    }
    
    playNextRandom() {
        if (this.musicFiles.length === 0) {
            document.getElementById('jukebox-now-playing').textContent = 'No music files available';
            return;
        }
        
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
        
        this.audio.src = this.currentTrack.path;
        document.getElementById('jukebox-now-playing').textContent = 
            `Now playing: ${this.currentTrack.title}`;
        
        this.audio.play()
            .then(() => {
                this.isPlaying = true;
                document.getElementById('jukebox-play').textContent = '⏸ Pause';
                this.saveState();
            })
            .catch(error => this.handleError(error));
    }
    
    setMusicFiles(musicFiles) {
        this.musicFiles = musicFiles;
        if (this.isPlaying) {
            this.stop();
        }
        this.currentTrackIndex = -1;
        localStorage.removeItem('jukebox_state');
    }
    
    updateMuteButton() {
        if (this.isMuted) {
            document.getElementById('volume-slider').disabled = true;
            document.getElementById('volume-slider').value = 0;
            document.getElementById('volume-slider').style.background = '#555';
            document.getElementById('volume-slider').style.cursor = 'not-allowed';
            document.getElementById('volume-icon').textContent = '🔇';
        } else {
            document.getElementById('volume-slider').disabled = false;
            document.getElementById('volume-slider').value = this.volume * 100;
            document.getElementById('volume-slider').style.background = 'linear-gradient(to right, #4CAF50, #45a049)';
            document.getElementById('volume-slider').style.cursor = 'pointer';
            this.setVolume(this.volume);
        }
    }
}

// Function to initialize the jukebox with music files from the server
function initJukebox(containerId) {
    fetch('/music/tracks')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to fetch tracks: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Loaded music tracks response:', data);
            
            if (!data || data.length === 0) {
                console.warn('No tracks returned from the server, using fallback tracks');
                
                // Use fallback direct URLs to the music files on the server
                const fallbackTracks = [];
                
                // Add hardcoded tracks that point directly to the Namecheap server
                for (let i = 1; i <= 103; i++) {
                    fallbackTracks.push({
                        title: `Be the Chad ${i}`,
                        path: `https://chadbattles.fun/music/Be the Chad (${i}).m4a`,
                        filename: `Be the Chad (${i}).m4a`,
                        size: 2000000,
                        type: 'm4a'
                    });
                }
                
                console.log(`Created ${fallbackTracks.length} fallback tracks`);
                const jukebox = new Jukebox(containerId, fallbackTracks);
                window.jukebox = jukebox;
                return;
            }
            
            console.log(`Loaded ${data.length} music tracks`);
            const jukebox = new Jukebox(containerId, data);
            window.jukebox = jukebox;
        })
        .catch(error => {
            console.error('Error loading music files:', error);
            
            // Use fallback direct URLs in case of error
            const fallbackTracks = [];
            
            // Add hardcoded tracks that point directly to the Namecheap server
            for (let i = 1; i <= 103; i++) {
                fallbackTracks.push({
                    title: `Be the Chad ${i}`,
                    path: `https://chadbattles.fun/music/Be the Chad (${i}).m4a`,
                    filename: `Be the Chad (${i}).m4a`,
                    size: 2000000,
                    type: 'm4a'
                });
            }
            
            console.log(`Created ${fallbackTracks.length} fallback tracks due to error`);
            const container = document.getElementById(containerId);
            
            if (container) {
                const jukebox = new Jukebox(containerId, fallbackTracks);
                window.jukebox = jukebox;
            } else {
                console.error(`Container #${containerId} not found`);
            }
        });
}

// Initialize jukebox when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing jukebox');
    initJukebox('chad-jukebox');
}); 