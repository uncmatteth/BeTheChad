/**
 * Simple Jukebox Music Player
 * Plays MP3 files randomly with basic controls
 * Persists between page loads using localStorage
 */
// Store the current instance for global access
let jukeboxInstance = null;

class Jukebox {
    constructor(containerId, musicFiles = []) {
        this.container = document.getElementById(containerId);
        this.musicFiles = musicFiles;
        this.currentTrack = null;
        this.isPlaying = false;
        this.audio = document.getElementById('chad-jukebox-audio') || new Audio();
        this.currentTrackIndex = -1;
        this.volume = localStorage.getItem('jukebox_volume') ? parseFloat(localStorage.getItem('jukebox_volume')) : 0.4;
        this.trackInfoElement = document.getElementById('track-info');
        this.playPauseBtn = document.getElementById('play-pause-btn');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        this.volumeSlider = document.getElementById('volume-slider');
        this.playerToggle = document.getElementById('player-toggle');
        this.playerControls = document.getElementById('player-controls');
        
        console.log('Jukebox initialized with', musicFiles.length, 'music files');
        if (musicFiles.length > 0) {
            console.log('First few music files:', 
                musicFiles.slice(0, 3).map(file => file.title).join(', '), 
                '...');
        }
        
        this.setupAudioEvents();
        this.setupControlEvents();
        this.restorePlayerState();
    }
    
    setupAudioEvents() {
        // Set up event listener for when a song ends
        this.audio.addEventListener('ended', () => this.playNextRandom());
        
        // Add error listener to debug audio loading issues
        this.audio.addEventListener('error', (e) => {
            console.error('Audio error:', e);
            console.error('Error code:', this.audio.error ? this.audio.error.code : 'unknown');
            console.error('Current audio src:', this.audio.src);
            this.trackInfoElement.textContent = 'Error loading track - trying next...';
            
            // Try the next track automatically
            setTimeout(() => this.playNextRandom(), 2000);
        });
        
        // Add load start listener to show loading status
        this.audio.addEventListener('loadstart', () => {
            console.log('Audio track loading started');
            if (this.trackInfoElement) {
                this.trackInfoElement.textContent = 'Loading track...';
            }
        });
        
        // Add canplaythrough listener to know when audio is ready
        this.audio.addEventListener('canplaythrough', () => {
            console.log('Audio track loaded and can play through');
        });
        
        // Save current time periodically for state persistence
        this.audio.addEventListener('timeupdate', () => {
            if (this.audio.currentTime > 0 && this.currentTrackIndex >= 0) {
                localStorage.setItem('jukebox_currentTime', this.audio.currentTime);
            }
        });
    }
    
    setupControlEvents() {
        // Set up play/pause button
        if (this.playPauseBtn) {
            this.playPauseBtn.addEventListener('click', () => this.togglePlay());
        }
        
        // Set up next button
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.playNextRandom());
        }
        
        // Set up previous button
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.playPrevious());
        }
        
        // Set up volume slider
        if (this.volumeSlider) {
            this.volumeSlider.value = this.volume * 100; // Set initial volume slider position
            this.volumeSlider.addEventListener('input', (e) => {
                const volume = e.target.value / 100;
                this.setVolume(volume);
                localStorage.setItem('jukebox_volume', volume);
            });
        }
        
        // Set up player toggle
        if (this.playerToggle) {
            this.playerToggle.addEventListener('click', () => this.togglePlayerVisibility());
        }
        
        // Close player button
        const closePlayer = document.getElementById('close-player');
        if (closePlayer) {
            closePlayer.addEventListener('click', () => this.togglePlayerVisibility());
        }
        
        // Handle page unload to save state
        window.addEventListener('beforeunload', () => this.savePlayerState());
    }
    
    togglePlayerVisibility() {
        if (this.playerControls) {
            this.playerControls.classList.toggle('active');
            localStorage.setItem('jukebox_visible', this.playerControls.classList.contains('active'));
        }
    }
    
    loadMusicFiles() {
        // This function can be used to load music files from the server
        if (this.musicFiles.length === 0) {
            console.warn('No music files provided, player may not work');
            if (this.trackInfoElement) {
                this.trackInfoElement.textContent = 'No music files available';
            }
        }
    }
    
    togglePlay() {
        if (!this.isPlaying) {
            if (this.currentTrackIndex === -1) {
                // Load the previously playing track if available
                const savedIndex = localStorage.getItem('jukebox_trackIndex');
                if (savedIndex !== null && this.musicFiles.length > 0) {
                    this.playTrack(parseInt(savedIndex, 10) % this.musicFiles.length);
                } else {
                    this.playNextRandom();
                }
            } else {
                this.audio.play()
                    .then(() => {
                        console.log('Playback resumed successfully');
                    })
                    .catch(error => {
                        console.error('Error resuming playback:', error);
                    });
                this.isPlaying = true;
                this.updatePlayPauseButton(true);
                localStorage.setItem('jukebox_playing', 'true');
            }
        } else {
            // If already playing, this acts as pause
            this.audio.pause();
            this.isPlaying = false;
            this.updatePlayPauseButton(false);
            localStorage.setItem('jukebox_playing', 'false');
        }
    }
    
    updatePlayPauseButton(isPlaying) {
        if (this.playPauseBtn) {
            const icon = this.playPauseBtn.querySelector('i');
            if (icon) {
                if (isPlaying) {
                    icon.className = 'fas fa-pause';
                } else {
                    icon.className = 'fas fa-play';
                }
            }
        }
    }
    
    stop() {
        this.audio.pause();
        this.audio.currentTime = 0;
        this.isPlaying = false;
        this.updatePlayPauseButton(false);
        if (this.trackInfoElement) {
            this.trackInfoElement.textContent = 'Music stopped';
        }
        localStorage.setItem('jukebox_playing', 'false');
    }
    
    setVolume(volume) {
        this.volume = volume;
        this.audio.volume = volume;
        console.log('Volume set to:', volume);
    }
    
    playPrevious() {
        if (this.musicFiles.length === 0) return;
        
        if (this.currentTrackIndex > 0) {
            this.currentTrackIndex--;
        } else {
            this.currentTrackIndex = this.musicFiles.length - 1;
        }
        
        this.playTrack(this.currentTrackIndex);
    }
    
    playNextRandom() {
        if (this.musicFiles.length === 0) {
            console.warn('No music files available to play');
            if (this.trackInfoElement) {
                this.trackInfoElement.textContent = 'No music files available';
            }
            return;
        }
        
        // Choose a random track, but not the same one that's currently playing
        let newIndex;
        if (this.musicFiles.length === 1) {
            newIndex = 0;
        } else {
            do {
                newIndex = Math.floor(Math.random() * this.musicFiles.length);
            } while (newIndex === this.currentTrackIndex && this.musicFiles.length > 1);
        }
        
        this.playTrack(newIndex);
    }
    
    playTrack(index) {
        if (index < 0 || index >= this.musicFiles.length) return;
        
        this.currentTrackIndex = index;
        this.currentTrack = this.musicFiles[this.currentTrackIndex];
        
        console.log('Playing track:', this.currentTrack.title);
        
        // Update the audio source
        this.audio.src = this.currentTrack.path;
        
        // Set the volume
        this.audio.volume = this.volume;
        
        // Update the display
        if (this.trackInfoElement) {
            this.trackInfoElement.textContent = `Now playing: ${this.currentTrack.title}`;
        }
        
        // Save current track to localStorage
        localStorage.setItem('jukebox_trackIndex', this.currentTrackIndex);
        localStorage.setItem('jukebox_trackPath', this.currentTrack.path);
        localStorage.setItem('jukebox_trackTitle', this.currentTrack.title);
        
        // Play the track
        this.audio.play()
            .then(() => {
                console.log('Audio playback started successfully');
                this.isPlaying = true;
                this.updatePlayPauseButton(true);
                localStorage.setItem('jukebox_playing', 'true');
            })
            .catch(error => {
                console.error('Error playing audio:', error);
                if (this.trackInfoElement) {
                    this.trackInfoElement.textContent = `Error playing: ${this.currentTrack.title}`;
                }
                // Try the next track automatically
                setTimeout(() => this.playNextRandom(), 2000);
            });
    }
    
    // Method to set new music files
    setMusicFiles(musicFiles) {
        this.musicFiles = musicFiles;
        console.log(`Updated music files. Now have ${musicFiles.length} tracks.`);
    }
    
    // Save player state to localStorage
    savePlayerState() {
        if (this.isPlaying) {
            localStorage.setItem('jukebox_playing', 'true');
            localStorage.setItem('jukebox_currentTime', this.audio.currentTime);
        } else {
            localStorage.setItem('jukebox_playing', 'false');
        }
        localStorage.setItem('jukebox_trackIndex', this.currentTrackIndex);
        if (this.currentTrack) {
            localStorage.setItem('jukebox_trackPath', this.currentTrack.path);
            localStorage.setItem('jukebox_trackTitle', this.currentTrack.title);
        }
    }
    
    // Restore player state from localStorage
    restorePlayerState() {
        if (this.musicFiles.length === 0) return;
        
        const wasPlaying = localStorage.getItem('jukebox_playing') === 'true';
        const savedIndex = localStorage.getItem('jukebox_trackIndex');
        const savedTime = localStorage.getItem('jukebox_currentTime');
        const isVisible = localStorage.getItem('jukebox_visible') !== 'false';
        
        // Set player visibility state
        if (this.playerControls) {
            if (isVisible) {
                this.playerControls.classList.add('active');
            } else {
                this.playerControls.classList.remove('active');
            }
        }
        
        if (savedIndex !== null && this.musicFiles.length > 0) {
            const trackIndex = parseInt(savedIndex, 10) % this.musicFiles.length;
            this.currentTrackIndex = trackIndex;
            this.currentTrack = this.musicFiles[trackIndex];
            
            // Set the audio source
            this.audio.src = this.currentTrack.path;
            
            // Set the volume
            this.audio.volume = this.volume;
            
            // Set the current time
            if (savedTime !== null) {
                this.audio.currentTime = parseFloat(savedTime);
            }
            
            // Update display
            if (this.trackInfoElement && this.currentTrack) {
                this.trackInfoElement.textContent = `Now playing: ${this.currentTrack.title}`;
            }
            
            // If it was playing, resume playback
            if (wasPlaying) {
                this.audio.play()
                    .then(() => {
                        console.log('Restored playback successfully');
                        this.isPlaying = true;
                        this.updatePlayPauseButton(true);
                    })
                    .catch(error => {
                        console.error('Error restoring playback:', error);
                        this.isPlaying = false;
                        this.updatePlayPauseButton(false);
                    });
            } else {
                this.isPlaying = false;
                this.updatePlayPauseButton(false);
            }
        }
    }
}

// Function to initialize the jukebox with music files from the server
function initJukebox() {
    console.log('Initializing jukebox, fetching music from /music/list');
    
    // Create an AJAX request to get the music files
    fetch('/music/list')
        .then(response => {
            console.log('Music list response status:', response.status);
            if (!response.ok) {
                throw new Error(`Server returned ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Music files received:', data);
            if (!Array.isArray(data)) {
                console.error('Expected array of music files but got:', typeof data);
                data = [];
            }
            
            jukeboxInstance = new Jukebox('chad-jukebox', data);
            window.jukebox = jukeboxInstance; // Make it globally accessible
            
            // If there are music files, update the track-info element
            if (data.length > 0) {
                const trackInfo = document.getElementById('track-info');
                if (trackInfo) {
                    trackInfo.textContent = 'Ready to play. Click play to start.';
                }
            }
        })
        .catch(error => {
            console.error('Error loading music files:', error);
            // Initialize with empty array as fallback
            jukeboxInstance = new Jukebox('chad-jukebox', []);
            window.jukebox = jukeboxInstance;
            
            // Show error in the track-info element
            const trackInfo = document.getElementById('track-info');
            if (trackInfo) {
                trackInfo.textContent = 'Error loading music. Please try again later.';
            }
        });
}

// Initialize jukebox when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing jukebox');
    initJukebox();
}); 