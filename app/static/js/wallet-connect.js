/**
 * Wallet connection functionality for Chad Battles
 * Handles connecting to different wallet providers
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find wallet-related elements
    const connectWalletBtn = document.getElementById('connect-wallet-btn');
    const walletModal = document.getElementById('connectWalletModal');
    
    // Initialize the wallet modal if Bootstrap is available
    let walletModalInstance = null;
    if (typeof bootstrap !== 'undefined' && walletModal) {
        walletModalInstance = new bootstrap.Modal(walletModal);
    }
    
    // Add event listener to the connect wallet button if it exists
    if (connectWalletBtn) {
        connectWalletBtn.addEventListener('click', function() {
            if (walletModalInstance) {
                walletModalInstance.show();
            }
        });
    }
    
    // Add event listeners to wallet options
    const walletOptions = document.querySelectorAll('.wallet-option');
    walletOptions.forEach(option => {
        option.addEventListener('click', function() {
            const walletType = this.getAttribute('onclick').match(/'([^']+)'/)[1];
            connectWallet(walletType);
        });
    });
});

// Function to handle wallet connections
function connectWallet(walletType) {
    console.log(`Connecting to ${walletType} wallet...`);
    
    // Close the modal if it's open
    const walletModal = document.getElementById('connectWalletModal');
    if (walletModal) {
        const modalInstance = bootstrap.Modal.getInstance(walletModal);
        if (modalInstance) {
            modalInstance.hide();
        }
    }
    
    // Show connection status to user
    showConnectionStatus(`Connecting to ${walletType}...`);
    
    // Simulate connection process
    setTimeout(() => {
        // In a real implementation, this would connect to the actual wallet
        // For now, we'll just show success and redirect to a demo wallet page
        const demoAddress = generateDemoAddress(walletType);
        showConnectionStatus(`Connected to ${walletType}!`);
        
        // Redirect to wallet connection handler with demo data
        submitWalletConnection(walletType, demoAddress);
    }, 1500);
}

// Generate a demo wallet address
function generateDemoAddress(walletType) {
    const prefix = walletType === 'phantom' ? 'Ph' : 
                  walletType === 'solflare' ? 'So' : 
                  walletType === 'metamask' ? 'Me' : 'Ma';
    const randomPart = Math.random().toString(36).substring(2, 10);
    return `${prefix}${randomPart}...${randomPart.substring(0, 4)}`;
}

// Show connection status to the user
function showConnectionStatus(message) {
    // Create or update status element
    let statusEl = document.getElementById('wallet-connection-status');
    if (!statusEl) {
        statusEl = document.createElement('div');
        statusEl.id = 'wallet-connection-status';
        statusEl.className = 'wallet-status-popup';
        document.body.appendChild(statusEl);
    }
    
    statusEl.textContent = message;
    statusEl.classList.add('visible');
    
    // Hide after a delay
    setTimeout(() => {
        statusEl.classList.remove('visible');
    }, 3000);
}

// Submit wallet connection to backend
function submitWalletConnection(walletType, address) {
    // Create a form to submit the wallet connection
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/wallet/connect';
    form.style.display = 'none';
    
    // Add wallet type
    const typeInput = document.createElement('input');
    typeInput.type = 'hidden';
    typeInput.name = 'wallet_type';
    typeInput.value = walletType;
    form.appendChild(typeInput);
    
    // Add wallet address
    const addressInput = document.createElement('input');
    addressInput.type = 'hidden';
    addressInput.name = 'wallet_address';
    addressInput.value = address;
    form.appendChild(addressInput);
    
    // Add demo signature
    const signatureInput = document.createElement('input');
    signatureInput.type = 'hidden';
    signatureInput.name = 'signature';
    signatureInput.value = 'demo_signature_' + Date.now();
    form.appendChild(signatureInput);
    
    // Submit the form
    document.body.appendChild(form);
    form.submit();
}

// Available wallet types
const WALLET_TYPES = {
    'phantom': {
        name: 'Phantom',
        icon: '/static/img/wallets/phantom.png',
        checkAvailable: () => window.solana && window.solana.isPhantom
    },
    'solflare': {
        name: 'Solflare',
        icon: '/static/img/wallets/solflare.png',
        checkAvailable: () => window.solflare
    },
    'metamask': {
        name: 'Metamask', 
        icon: '/static/img/wallets/metamask.png',
        checkAvailable: () => window.ethereum && window.ethereum.isMetaMask
    },
    'magic_eden': {
        name: 'Magic Eden',
        icon: '/static/img/wallets/magic_eden.png',
        checkAvailable: () => window.magicEden
    },
    'slope': {
        name: 'Slope',
        icon: '/static/img/wallets/slope.png',
        checkAvailable: () => window.Slope
    }
};

// Initialize wallet connections
function initWalletConnections() {
    // Check if the user is already connected and listen for account changes
    checkExistingWalletConnection();
}

// Check for existing wallet connection
function checkExistingWalletConnection() {
    // For Phantom
    if (window.solana && window.solana.isPhantom) {
        window.solana.on('connect', () => {
            console.log('Phantom wallet connected');
            // Dispatch wallet connected event
            document.dispatchEvent(new CustomEvent('walletConnected', { detail: { type: 'phantom' } }));
        });
        
        window.solana.on('disconnect', () => {
            console.log('Phantom wallet disconnected');
            // Dispatch wallet disconnected event
            document.dispatchEvent(new CustomEvent('walletDisconnected', { detail: { type: 'phantom' } }));
        });
    }
    
    // For Solflare
    if (window.solflare) {
        window.solflare.on('connect', () => {
            console.log('Solflare wallet connected');
            // Dispatch wallet connected event
            document.dispatchEvent(new CustomEvent('walletConnected', { detail: { type: 'solflare' } }));
        });
        
        window.solflare.on('disconnect', () => {
            console.log('Solflare wallet disconnected');
            // Dispatch wallet disconnected event
            document.dispatchEvent(new CustomEvent('walletDisconnected', { detail: { type: 'solflare' } }));
        });
    }
    
    // For Metamask (if using Solana on Metamask)
    if (window.ethereum && window.ethereum.isMetaMask) {
        window.ethereum.on('connect', () => {
            console.log('Metamask wallet connected');
            // Dispatch wallet connected event
            document.dispatchEvent(new CustomEvent('walletConnected', { detail: { type: 'metamask' } }));
        });
        
        window.ethereum.on('disconnect', () => {
            console.log('Metamask wallet disconnected');
            // Dispatch wallet disconnected event
            document.dispatchEvent(new CustomEvent('walletDisconnected', { detail: { type: 'metamask' } }));
        });
    }
}

// Show wallet connection modal
function showWalletModal() {
    // Create modal if it doesn't exist
    let walletModalEl = document.getElementById('walletModal');
    
    if (!walletModalEl) {
        const modalHTML = `
            <div class="modal fade" id="walletModal" tabindex="-1" aria-labelledby="walletModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header bg-dark text-white">
                            <h5 class="modal-title" id="walletModalLabel">Connect Wallet</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <p>Select a wallet to connect:</p>
                            <div class="list-group wallet-list">
                                <!-- Wallet options will be populated here -->
                            </div>
                            <div class="mt-3 small text-muted">
                                <p>Note: Connecting your wallet allows you to mint NFTs and trade them on the Solana blockchain.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Append modal to body
        const modalContainer = document.createElement('div');
        modalContainer.innerHTML = modalHTML;
        document.body.appendChild(modalContainer);
        
        walletModalEl = document.getElementById('walletModal');
    }
    
    // Populate wallet options
    const walletList = walletModalEl.querySelector('.wallet-list');
    walletList.innerHTML = '';
    
    Object.entries(WALLET_TYPES).forEach(([key, wallet]) => {
        const isAvailable = wallet.checkAvailable();
        
        const walletOption = document.createElement('a');
        walletOption.href = '#';
        walletOption.className = `list-group-item list-group-item-action d-flex align-items-center ${!isAvailable ? 'disabled' : ''}`;
        walletOption.innerHTML = `
            <img src="${wallet.icon}" alt="${wallet.name}" width="32" height="32" class="me-3">
            <div>
                <h6 class="mb-0">${wallet.name}</h6>
                <small class="text-muted">${isAvailable ? 'Available' : 'Not detected'}</small>
            </div>
        `;
        
        if (isAvailable) {
            walletOption.addEventListener('click', (e) => {
                e.preventDefault();
                connectWallet(key);
                walletModal.hide();
            });
        }
        
        walletList.appendChild(walletOption);
    });
    
    // Show modal
    const walletModal = new bootstrap.Modal(walletModalEl);
    walletModal.show();
}

// Disconnect wallet
async function disconnectWallet() {
    if (!confirm('Are you sure you want to disconnect your wallet?')) {
        return;
    }
    
    try {
        // Disconnect from provider (if applicable)
        if (window.solana && window.solana.isConnected) {
            await window.solana.disconnect();
        }
        
        if (window.solflare && window.solflare.isConnected) {
            await window.solflare.disconnect();
        }
        
        // Clear wallet connection from server
        await fetch('/api/disconnect_wallet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        // Show success notification
        showNotification('success', 'Wallet Disconnected', 'Successfully disconnected your wallet.');
        
        // Refresh the page to update UI
        setTimeout(() => {
            window.location.reload();
        }, 1500);
    } catch (error) {
        console.error('Error disconnecting wallet:', error);
        showNotification('error', 'Disconnection Failed', `Failed to disconnect wallet: ${error.message || 'Unknown error'}`);
    }
}

// Save wallet connection to server
async function saveWalletConnection(walletAddress, walletType) {
    const response = await fetch('/api/connect_wallet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            wallet_address: walletAddress,
            wallet_type: walletType
        })
    });
    
    if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Failed to save wallet connection');
    }
    
    return await response.json();
}

// Function to show notifications (reusing from nft-minting.js)
function showNotification(type, title, message) {
    const notificationContainer = document.getElementById('notificationContainer');
    if (!notificationContainer) {
        // Create container if it doesn't exist
        const container = document.createElement('div');
        container.id = 'notificationContainer';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `toast align-items-center text-white bg-${type === 'success' ? 'success' : 'danger'} border-0`;
    notification.setAttribute('role', 'alert');
    notification.setAttribute('aria-live', 'assertive');
    notification.setAttribute('aria-atomic', 'true');
    
    notification.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <strong>${title}</strong><br>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Add to container
    document.getElementById('notificationContainer').appendChild(notification);
    
    // Initialize and show toast
    const toast = new bootstrap.Toast(notification, {
        autohide: true,
        delay: 5000
    });
    toast.show();
    
    // Remove after hiding
    notification.addEventListener('hidden.bs.toast', function() {
        notification.remove();
    });
} 