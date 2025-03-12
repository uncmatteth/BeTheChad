/**
 * Wallet integration for Chad Battles
 * Handles wallet connections and interactions with the Solana blockchain
 */

// Wallet connection status
let walletConnected = false;
let walletAddress = '';
let walletType = '';

// DOM elements
const connectButtons = document.querySelectorAll('.wallet-connect-btn');
const disconnectButtons = document.querySelectorAll('.wallet-disconnect-btn');
const walletAddressElements = document.querySelectorAll('.wallet-address');
const walletStatusElements = document.querySelectorAll('.wallet-status');
const walletBalanceElements = document.querySelectorAll('.wallet-balance');
const walletTypeElements = document.querySelectorAll('.wallet-type');
const connectWalletSection = document.getElementById('connect-wallet-section');
const connectedWalletSection = document.getElementById('connected-wallet-section');
const walletModal = document.getElementById('wallet-modal');
const walletModalClose = document.querySelector('.wallet-modal-close');
const copyAddressButtons = document.querySelectorAll('.copy-address-btn');

// Initialize wallet integration
document.addEventListener('DOMContentLoaded', () => {
    // Check if wallet is already connected
    checkWalletStatus();
    
    // Set up event listeners
    setupEventListeners();
});

/**
 * Set up event listeners for wallet interactions
 */
function setupEventListeners() {
    // Connect wallet buttons
    connectButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const walletType = button.getAttribute('data-wallet-type');
            connectWallet(walletType);
        });
    });
    
    // Disconnect wallet buttons
    disconnectButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            disconnectWallet();
        });
    });
    
    // Copy address buttons
    copyAddressButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            copyWalletAddress();
        });
    });
    
    // Modal close button
    if (walletModalClose) {
        walletModalClose.addEventListener('click', () => {
            closeWalletModal();
        });
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (walletModal && e.target === walletModal) {
            closeWalletModal();
        }
    });
}

/**
 * Check if wallet is already connected
 */
async function checkWalletStatus() {
    try {
        const response = await fetch('/api/wallet/status');
        const data = await response.json();
        
        if (data.success && data.connected) {
            walletConnected = true;
            walletAddress = data.wallet_address;
            walletType = data.wallet_type;
            
            updateWalletUI(true, data.wallet_address, data.wallet_type, data.balance);
        } else {
            updateWalletUI(false);
        }
    } catch (error) {
        console.error('Error checking wallet status:', error);
        updateWalletUI(false);
    }
}

/**
 * Connect to a wallet
 * @param {string} type - Wallet type (phantom, solflare, etc.)
 */
async function connectWallet(type) {
    // Show loading modal
    showWalletModal('Connecting to wallet...', true);
    
    try {
        // Check if wallet is available
        if (type === 'phantom' && !window.solana) {
            showWalletModal('Phantom wallet not detected. Please install the Phantom extension.', false);
            return;
        } else if (type === 'solflare' && !window.solflare) {
            showWalletModal('Solflare wallet not detected. Please install the Solflare extension.', false);
            return;
        }
        
        // Connect to wallet based on type
        let wallet;
        let address;
        
        if (type === 'phantom') {
            wallet = window.solana;
            try {
                const response = await wallet.connect();
                address = response.publicKey.toString();
            } catch (err) {
                showWalletModal('Failed to connect to Phantom wallet. Please try again.', false);
                return;
            }
        } else if (type === 'solflare') {
            wallet = window.solflare;
            try {
                await wallet.connect();
                address = wallet.publicKey.toString();
            } catch (err) {
                showWalletModal('Failed to connect to Solflare wallet. Please try again.', false);
                return;
            }
        } else if (type === 'demo') {
            // Demo mode for development
            address = document.getElementById('demo-wallet-address').value;
            if (!address) {
                showWalletModal('Please enter a demo wallet address.', false);
                return;
            }
        }
        
        // Send wallet info to server
        const response = await fetch('/api/wallet/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                wallet_address: address,
                wallet_type: type
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            walletConnected = true;
            walletAddress = data.wallet_address;
            walletType = data.wallet_type;
            
            updateWalletUI(true, data.wallet_address, data.wallet_type, data.balance);
            showWalletModal('Wallet connected successfully!', false);
            
            // Redirect to wallet page after a short delay
            setTimeout(() => {
                window.location.href = '/wallet';
            }, 1500);
        } else {
            showWalletModal(`Failed to connect wallet: ${data.message}`, false);
        }
    } catch (error) {
        console.error('Error connecting wallet:', error);
        showWalletModal('An error occurred while connecting the wallet. Please try again.', false);
    }
}

/**
 * Disconnect the wallet
 */
async function disconnectWallet() {
    try {
        const response = await fetch('/api/wallet/disconnect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            walletConnected = false;
            walletAddress = '';
            walletType = '';
            
            updateWalletUI(false);
            
            // Also disconnect from the wallet provider if possible
            if (window.solana && walletType === 'phantom') {
                try {
                    await window.solana.disconnect();
                } catch (err) {
                    console.error('Error disconnecting from Phantom:', err);
                }
            } else if (window.solflare && walletType === 'solflare') {
                try {
                    await window.solflare.disconnect();
                } catch (err) {
                    console.error('Error disconnecting from Solflare:', err);
                }
            }
            
            // Redirect to wallet page after a short delay
            setTimeout(() => {
                window.location.href = '/wallet';
            }, 1000);
        } else {
            alert(`Failed to disconnect wallet: ${data.message}`);
        }
    } catch (error) {
        console.error('Error disconnecting wallet:', error);
        alert('An error occurred while disconnecting the wallet. Please try again.');
    }
}

/**
 * Update the UI based on wallet connection status
 * @param {boolean} connected - Whether the wallet is connected
 * @param {string} address - Wallet address
 * @param {string} type - Wallet type
 * @param {number} balance - Wallet balance
 */
function updateWalletUI(connected, address = '', type = '', balance = 0) {
    if (connected) {
        // Update wallet address display
        walletAddressElements.forEach(element => {
            element.textContent = formatWalletAddress(address);
            element.setAttribute('title', address);
            element.setAttribute('data-address', address);
        });
        
        // Update wallet type display
        walletTypeElements.forEach(element => {
            element.textContent = formatWalletType(type);
        });
        
        // Update wallet balance display
        walletBalanceElements.forEach(element => {
            element.textContent = `${balance.toFixed(2)} SOL`;
        });
        
        // Update status display
        walletStatusElements.forEach(element => {
            element.textContent = 'Connected';
            element.classList.remove('text-danger');
            element.classList.add('text-success');
        });
        
        // Show/hide sections
        if (connectWalletSection) connectWalletSection.style.display = 'none';
        if (connectedWalletSection) connectedWalletSection.style.display = 'block';
        
        // Enable NFT-related buttons
        document.querySelectorAll('.requires-wallet').forEach(element => {
            element.classList.remove('disabled');
            element.removeAttribute('disabled');
        });
    } else {
        // Reset wallet display
        walletAddressElements.forEach(element => {
            element.textContent = 'Not connected';
            element.removeAttribute('title');
            element.removeAttribute('data-address');
        });
        
        // Reset wallet type display
        walletTypeElements.forEach(element => {
            element.textContent = '';
        });
        
        // Reset wallet balance display
        walletBalanceElements.forEach(element => {
            element.textContent = '0.00 SOL';
        });
        
        // Update status display
        walletStatusElements.forEach(element => {
            element.textContent = 'Not connected';
            element.classList.remove('text-success');
            element.classList.add('text-danger');
        });
        
        // Show/hide sections
        if (connectWalletSection) connectWalletSection.style.display = 'block';
        if (connectedWalletSection) connectedWalletSection.style.display = 'none';
        
        // Disable NFT-related buttons
        document.querySelectorAll('.requires-wallet').forEach(element => {
            element.classList.add('disabled');
            element.setAttribute('disabled', 'disabled');
        });
    }
}

/**
 * Format wallet address for display (truncate middle)
 * @param {string} address - Full wallet address
 * @returns {string} Formatted address
 */
function formatWalletAddress(address) {
    if (!address) return '';
    if (address.length <= 12) return address;
    
    return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
}

/**
 * Format wallet type for display (capitalize)
 * @param {string} type - Wallet type
 * @returns {string} Formatted type
 */
function formatWalletType(type) {
    if (!type) return '';
    
    // Special case for specific wallets
    if (type.toLowerCase() === 'phantom') return 'Phantom';
    if (type.toLowerCase() === 'solflare') return 'Solflare';
    if (type.toLowerCase() === 'magic_eden') return 'Magic Eden';
    
    // Default: capitalize first letter
    return type.charAt(0).toUpperCase() + type.slice(1);
}

/**
 * Copy wallet address to clipboard
 */
function copyWalletAddress() {
    const address = document.querySelector('.wallet-address').getAttribute('data-address');
    if (!address) return;
    
    navigator.clipboard.writeText(address).then(() => {
        // Show toast notification
        const toast = document.getElementById('copy-toast');
        if (toast) {
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        } else {
            alert('Address copied to clipboard!');
        }
    }).catch(err => {
        console.error('Failed to copy address:', err);
        alert('Failed to copy address to clipboard');
    });
}

/**
 * Show wallet connection modal
 * @param {string} message - Message to display
 * @param {boolean} loading - Whether to show loading spinner
 */
function showWalletModal(message, loading = false) {
    if (!walletModal) return;
    
    const messageElement = walletModal.querySelector('.wallet-modal-message');
    const spinnerElement = walletModal.querySelector('.wallet-modal-spinner');
    
    if (messageElement) messageElement.textContent = message;
    if (spinnerElement) spinnerElement.style.display = loading ? 'block' : 'none';
    
    walletModal.style.display = 'block';
}

/**
 * Close wallet connection modal
 */
function closeWalletModal() {
    if (!walletModal) return;
    walletModal.style.display = 'none';
}

/**
 * Mint an NFT
 * @param {string} entityType - Entity type (chad, waifu, item)
 * @param {number} entityId - Entity ID
 */
async function mintNFT(entityType, entityId) {
    if (!walletConnected) {
        alert('Please connect your wallet first.');
        return;
    }
    
    try {
        const response = await fetch('/api/mint-nft', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                entity_type: entityType,
                entity_id: entityId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`NFT minted successfully! Transaction hash: ${data.transaction_hash}`);
            // Reload page after a short delay
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            alert(`Failed to mint NFT: ${data.message}`);
        }
    } catch (error) {
        console.error('Error minting NFT:', error);
        alert('An error occurred while minting the NFT. Please try again.');
    }
}

/**
 * Burn an NFT
 * @param {string} tokenId - NFT token ID
 */
async function burnNFT(tokenId) {
    if (!walletConnected) {
        alert('Please connect your wallet first.');
        return;
    }
    
    // Confirm before burning
    if (!confirm('Are you sure you want to burn this NFT? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/api/burn-nft', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                token_id: tokenId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`NFT burned successfully! You received ${data.chadcoin_reward} Chadcoin.`);
            // Reload page after a short delay
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            alert(`Failed to burn NFT: ${data.message}`);
        }
    } catch (error) {
        console.error('Error burning NFT:', error);
        alert('An error occurred while burning the NFT. Please try again.');
    }
}

/**
 * Transfer an NFT to another user
 * @param {string} tokenId - NFT token ID
 * @param {string} toAddress - Recipient wallet address
 */
async function transferNFT(tokenId, toAddress) {
    if (!walletConnected) {
        alert('Please connect your wallet first.');
        return;
    }
    
    if (!toAddress) {
        alert('Please enter a recipient wallet address.');
        return;
    }
    
    // Confirm before transferring
    if (!confirm(`Are you sure you want to transfer this NFT to ${toAddress}? This action cannot be undone.`)) {
        return;
    }
    
    try {
        const response = await fetch('/api/transfer-nft', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                token_id: tokenId,
                to_address: toAddress
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`NFT transferred successfully! Transaction hash: ${data.transaction_hash}`);
            // Reload page after a short delay
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            alert(`Failed to transfer NFT: ${data.message}`);
        }
    } catch (error) {
        console.error('Error transferring NFT:', error);
        alert('An error occurred while transferring the NFT. Please try again.');
    }
} 