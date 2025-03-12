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
    let audio = new Audio();
    
    // Initialize UI
    initJukeboxUI();
    
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
            document.getElementById('jukebox-play').textContent = '▶';
        } else {
            if (currentTrackIndex === -1) {
                playNextTrack();
            } else {
                audio.play();
                isPlaying = true;
                document.getElementById('jukebox-play').textContent = '⏸';
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
        audio.volume = parseFloat(document.getElementById('jukebox-volume').value);
        
        // Play the track
        audio.play()
            .then(() => {
                isPlaying = true;
                document.getElementById('jukebox-play').textContent = '⏸';
            })
            .catch(error => {
                console.error('Error playing track:', error);
            });
    }
    
    /**
     * Set the volume
     */
    function setVolume() {
        const volumeValue = document.getElementById('jukebox-volume').value;
        audio.volume = parseFloat(volumeValue);
    }
}); 