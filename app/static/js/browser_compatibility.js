/**
 * Browser Compatibility Helper
 * Utility functions to detect browser features and handle compatibility issues
 */

const BrowserCompat = {
    // Check if HTML5 Audio is supported
    checkAudio: function() {
        const audio = document.createElement('audio');
        const canPlay = {
            mp3: !!audio.canPlayType && audio.canPlayType('audio/mpeg;').replace(/no/, ''),
            wav: !!audio.canPlayType && audio.canPlayType('audio/wav; codecs="1"').replace(/no/, ''),
            ogg: !!audio.canPlayType && audio.canPlayType('audio/ogg; codecs="vorbis"').replace(/no/, '')
        };
        
        return {
            supported: !!audio.canPlayType,
            formats: canPlay
        };
    },
    
    // Check local storage availability
    checkLocalStorage: function() {
        try {
            const storage = window.localStorage;
            const x = '__storage_test__';
            storage.setItem(x, x);
            storage.removeItem(x);
            return true;
        } catch(e) {
            return e instanceof DOMException && (
                // Everything except Firefox
                e.code === 22 ||
                // Firefox
                e.code === 1014 ||
                // Test name field too, because code might not be present
                e.name === 'QuotaExceededError' ||
                e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
                // Acknowledge QuotaExceededError only if there's something already stored
                (window.localStorage && window.localStorage.length !== 0);
        }
    },
    
    // Check WebCrypto API for wallet signing
    checkWebCrypto: function() {
        return typeof window.crypto !== 'undefined' && typeof window.crypto.subtle !== 'undefined';
    },
    
    // Check for Promise support
    checkPromises: function() {
        return typeof Promise !== 'undefined';
    },
    
    // Check for Fetch API support
    checkFetch: function() {
        return 'fetch' in window;
    },
    
    // Check for CSS Grid support
    checkCssGrid: function() {
        return window.CSS && CSS.supports && CSS.supports('display', 'grid');
    },
    
    // Check for WebGL support (for potential future graphics)
    checkWebGL: function() {
        try {
            const canvas = document.createElement('canvas');
            return !!(window.WebGLRenderingContext && 
                     (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
        } catch(e) {
            return false;
        }
    },
    
    // Check for mobile device
    isMobile: function() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    },
    
    // Get browser name and version
    getBrowser: function() {
        const ua = navigator.userAgent;
        let browser = "Unknown";
        let version = "Unknown";
        
        // Opera
        if (ua.indexOf("Opera") > -1 || ua.indexOf("OPR") > -1) {
            browser = "Opera";
            version = ua.match(/(Opera|OPR)\/([0-9]+\.[0-9]+)/)[2];
        }
        // Edge
        else if (ua.indexOf("Edg") > -1) {
            browser = "Edge";
            version = ua.match(/Edg\/([0-9]+\.[0-9]+)/)[1];
        }
        // Chrome
        else if (ua.indexOf("Chrome") > -1) {
            browser = "Chrome";
            version = ua.match(/Chrome\/([0-9]+\.[0-9]+)/)[1];
        }
        // Safari
        else if (ua.indexOf("Safari") > -1) {
            browser = "Safari";
            version = ua.match(/Version\/([0-9]+\.[0-9]+)/)[1];
        }
        // Firefox
        else if (ua.indexOf("Firefox") > -1) {
            browser = "Firefox";
            version = ua.match(/Firefox\/([0-9]+\.[0-9]+)/)[1];
        }
        // IE
        else if (ua.indexOf("MSIE") > -1 || ua.indexOf("Trident") > -1) {
            browser = "Internet Explorer";
            version = ua.match(/(MSIE |rv:)([0-9]+\.[0-9]+)/)[2];
        }
        
        return { name: browser, version: version };
    },
    
    // Run all checks and return a compatibility report
    getFullReport: function() {
        const audio = this.checkAudio();
        const browser = this.getBrowser();
        
        return {
            browser: browser,
            audio: audio,
            localStorage: this.checkLocalStorage(),
            webCrypto: this.checkWebCrypto(),
            promises: this.checkPromises(),
            fetch: this.checkFetch(),
            cssGrid: this.checkCssGrid(),
            webgl: this.checkWebGL(),
            mobile: this.isMobile()
        };
    },
    
    // Log compatibility issues to console
    logCompatibilityIssues: function() {
        const report = this.getFullReport();
        console.log("Browser Compatibility Report:", report);
        
        if (!report.audio.supported) {
            console.warn("HTML5 Audio not supported - music player will be disabled");
        } else {
            const formats = report.audio.formats;
            if (!formats.mp3 && !formats.ogg) {
                console.warn("No supported audio formats detected - music playback may not work");
            }
        }
        
        if (!report.localStorage) {
            console.warn("LocalStorage not available - settings will not persist between sessions");
        }
        
        if (!report.webCrypto) {
            console.warn("WebCrypto API not available - wallet functionality may be limited");
        }
        
        if (!report.promises || !report.fetch) {
            console.warn("Modern JavaScript features missing - application may not function correctly");
        }
        
        if (!report.cssGrid) {
            console.warn("CSS Grid not supported - layout may appear broken");
        }
        
        return report;
    }
};

// Auto-run compatibility check when loaded
document.addEventListener('DOMContentLoaded', function() {
    const compatReport = BrowserCompat.logCompatibilityIssues();
    
    // Add compatibility issues banner if needed
    if (!compatReport.audio.supported || 
        !compatReport.localStorage || 
        !compatReport.promises || 
        !compatReport.fetch) {
        
        const banner = document.createElement('div');
        banner.className = 'compat-warning';
        banner.innerHTML = `
            <strong>Browser Compatibility Warning</strong>
            <p>Your browser may not support all features of Chad Battles. For the best experience, use the latest version of Chrome, Firefox, Edge, or Safari.</p>
            <button id="dismiss-compat-warning">Dismiss</button>
        `;
        
        document.body.insertBefore(banner, document.body.firstChild);
        
        document.getElementById('dismiss-compat-warning').addEventListener('click', function() {
            banner.style.display = 'none';
        });
    }
}); 