/**
 * Simple Jukebox Player for Chad Battles
 * 
 * Plays background music from a list of MP3 files
 * with basic controls (play/pause, next, volume)
 */
document.addEventListener('DOMContentLoaded', function() {
    // Player state
    let musicFiles = [];
    let currentTrackIndex = -1;
    let isPlaying = false;
    let audio = document.getElementById('chad-jukebox-audio') || new Audio();
    
    // Check if we already have a jukebox on the page
    const existingJukebox = document.getElementById('chad-jukebox');
    
    // Initialize UI only if there isn't already a jukebox
    if (!existingJukebox) {
        initJukeboxUI();
    } else {
        // Use existing UI elements
        const playBtn = document.getElementById('play-pause-btn');
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        const volumeSlider = document.getElementById('volume-slider');
        
        // Add event listeners to existing controls
        if (playBtn) playBtn.addEventListener('click', togglePlay);
        if (nextBtn) nextBtn.addEventListener('click', playNextTrack);
        if (prevBtn) prevBtn.addEventListener('click', playPrevTrack);
        if (volumeSlider) volumeSlider.addEventListener('input', setVolume);
        
        // Add event listener for when a song ends
        audio.addEventListener('ended', playNextTrack);
    }
    
    // Load music files
    loadMusicFiles();
    
    /**
     * Create and add the jukebox UI to the page
     */
    function initJukeboxUI() {
        // Create jukebox container
        const jukeboxWrapper = document.createElement('div');
        jukeboxWrapper.className = 'jukebox-wrapper';
        jukeboxWrapper.innerHTML = `
            <div class="jukebox-controls">
                <button id="jukebox-prev" class="jukebox-btn">⏮</button>
                <button id="jukebox-play" class="jukebox-btn">▶</button>
                <button id="jukebox-next" class="jukebox-btn">⏭</button>
                <input type="range" id="jukebox-volume" class="jukebox-volume" min="0" max="1" step="0.1" value="0.7">
            </div>
        `;
        
        // Add to document
        document.body.appendChild(jukeboxWrapper);
        
        // Add event listeners
        document.getElementById('jukebox-play').addEventListener('click', togglePlay);
        document.getElementById('jukebox-next').addEventListener('click', playNextTrack);
        document.getElementById('jukebox-prev').addEventListener('click', playPrevTrack);
        document.getElementById('jukebox-volume').addEventListener('input', setVolume);

        // Add event listener for when a song ends
        audio.addEventListener('ended', playNextTrack);
    }
    
    /**
     * Load the list of music files from the server
     */
    function loadMusicFiles() {
        fetch('/music/list')
            .then(response => response.json())
            .then(data => {
                musicFiles = data;
                if (musicFiles.length > 0) {
                    // Auto-play first track if there are tracks
                    setTimeout(() => {
                        playNextTrack();
                    }, 2000);
                }
            })
            .catch(error => {
                console.error('Error loading music files:', error);
            });
    }
    
    /**
     * Toggle play/pause
     */
    function togglePlay() {
        if (musicFiles.length === 0) {
            return;
        }
        
        if (isPlaying) {
            audio.pause();
            isPlaying = false;
            
            // Update UI - check which button exists
            const playBtn = document.getElementById('jukebox-play');
            const playPauseBtn = document.getElementById('play-pause-btn');
            
            if (playBtn) {
                playBtn.textContent = '▶';
            }
            if (playPauseBtn) {
                playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
            }
        } else {
            if (currentTrackIndex === -1) {
                playNextTrack();
            } else {
                audio.play();
                isPlaying = true;
                
                // Update UI - check which button exists
                const playBtn = document.getElementById('jukebox-play');
                const playPauseBtn = document.getElementById('play-pause-btn');
                
                if (playBtn) {
                    playBtn.textContent = '⏸';
                }
                if (playPauseBtn) {
                    playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                }
            }
        }
    }
    
    /**
     * Play the previous track
     */
    function playPrevTrack() {
        if (musicFiles.length === 0) {
            return;
        }
        
        if (currentTrackIndex > 0) {
            currentTrackIndex--;
        } else {
            currentTrackIndex = musicFiles.length - 1;
        }
        
        playTrack(musicFiles[currentTrackIndex]);
    }
    
    /**
     * Play the next track
     */
    function playNextTrack() {
        if (musicFiles.length === 0) {
            return;
        }
        
        // Choose the next track
        if (currentTrackIndex >= musicFiles.length - 1) {
            currentTrackIndex = 0;
        } else {
            currentTrackIndex++;
        }
        
        playTrack(musicFiles[currentTrackIndex]);
    }
    
    /**
     * Play a specific track
     */
    function playTrack(track) {
        // Update the audio source
        audio.src = track.path;
        
        // Get volume from correct volume control
        const volumeSlider = document.getElementById('volume-slider');
        const volumeControl = document.getElementById('jukebox-volume');
        
        if (volumeSlider) {
            audio.volume = parseFloat(volumeSlider.value) / 100;
        } else if (volumeControl) {
            audio.volume = parseFloat(volumeControl.value);
        } else {
            audio.volume = 0.7; // Default volume
        }
        
        // Update track info if element exists
        const trackInfo = document.getElementById('track-info');
        if (trackInfo) {
            trackInfo.textContent = track.title || 'Unknown Track';
        }
        
        // Play the track
        audio.play()
            .then(() => {
                isPlaying = true;
                
                // Update UI - check which button exists
                const playBtn = document.getElementById('jukebox-play');
                const playPauseBtn = document.getElementById('play-pause-btn');
                
                if (playBtn) {
                    playBtn.textContent = '⏸';
                }
                if (playPauseBtn) {
                    playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                }
            })
            .catch(error => {
                console.error('Error playing track:', error);
            });
    }
    
    /**
     * Set the volume
     */
    function setVolume() {
        // Get volume from correct volume control
        const volumeSlider = document.getElementById('volume-slider');
        const volumeControl = document.getElementById('jukebox-volume');
        
        if (volumeSlider) {
            audio.volume = parseFloat(volumeSlider.value) / 100;
        } else if (volumeControl) {
            audio.volume = parseFloat(volumeControl.value);
        }
    }
}); 