// Main JavaScript for Chad Battles

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Handle Waifu equip/unequip actions
    setupWaifuActions();
    
    // Handle Item equip/unequip actions
    setupItemActions();
    
    // Handle wallet connection
    setupWalletConnection();
    
    // Handle NFT minting
    setupNFTMinting();
    
    // Handle Elixir activation
    setupElixirActivation();
});

// Set up Waifu equip/unequip actions
function setupWaifuActions() {
    // Equip Waifu
    document.querySelectorAll('.equip-waifu-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const waifuId = this.dataset.waifuId;
            
            fetch('/waifu/equip', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `waifu_id=${waifuId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update UI to show waifu is equipped
                    this.innerHTML = 'Unequip';
                    this.classList.remove('btn-pixel');
                    this.classList.add('btn-danger-pixel');
                    this.classList.remove('equip-waifu-btn');
                    this.classList.add('unequip-waifu-btn');
                    
                    // Show success message
                    showAlert('success', data.message);
                } else {
                    showAlert('danger', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('danger', 'An error occurred');
            });
        });
    });
    
    // Unequip Waifu
    document.querySelectorAll('.unequip-waifu-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const waifuId = this.dataset.waifuId;
            
            fetch('/waifu/unequip', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `waifu_id=${waifuId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update UI to show waifu is not equipped
                    this.innerHTML = 'Equip';
                    this.classList.remove('btn-danger-pixel');
                    this.classList.add('btn-pixel');
                    this.classList.remove('unequip-waifu-btn');
                    this.classList.add('equip-waifu-btn');
                    
                    // Show success message
                    showAlert('success', data.message);
                } else {
                    showAlert('danger', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('danger', 'An error occurred');
            });
        });
    });
}

// Set up Item equip/unequip actions
function setupItemActions() {
    // Equip Item
    document.querySelectorAll('.equip-item-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            
            fetch('/chad/equip-item', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `item_id=${itemId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update UI to show item is equipped
                    this.innerHTML = 'Unequip';
                    this.classList.remove('btn-pixel');
                    this.classList.add('btn-danger-pixel');
                    this.classList.remove('equip-item-btn');
                    this.classList.add('unequip-item-btn');
                    
                    // Show success message
                    showAlert('success', data.message);
                } else {
                    showAlert('danger', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('danger', 'An error occurred');
            });
        });
    });
    
    // Unequip Item
    document.querySelectorAll('.unequip-item-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            
            fetch('/chad/unequip-item', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `item_id=${itemId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update UI to show item is not equipped
                    this.innerHTML = 'Equip';
                    this.classList.remove('btn-danger-pixel');
                    this.classList.add('btn-pixel');
                    this.classList.remove('unequip-item-btn');
                    this.classList.add('equip-item-btn');
                    
                    // Show success message
                    showAlert('success', data.message);
                } else {
                    showAlert('danger', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('danger', 'An error occurred');
            });
        });
    });
    
    // Equip Waifu Item
    document.querySelectorAll('.equip-waifu-item-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            const waifuId = this.dataset.waifuId;
            
            // Confirm before equipping waifu item (permanent action)
            if (confirm('Are you sure you want to equip this item to the waifu? This action is permanent and the item cannot be removed.')) {
                fetch('/waifu/equip-item', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: `item_id=${itemId}&waifu_id=${waifuId}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Remove the item from the UI
                        const itemCard = this.closest('.card');
                        itemCard.remove();
                        
                        // Show success message
                        showAlert('success', data.message);
                    } else {
                        if (data.require_confirmation) {
                            // Ask for additional confirmation if item is minted as NFT
                            if (confirm(data.message)) {
                                // Submit with confirmed flag
                                fetch('/waifu/equip-item', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/x-www-form-urlencoded',
                                        'X-Requested-With': 'XMLHttpRequest'
                                    },
                                    body: `item_id=${itemId}&waifu_id=${waifuId}&confirmed=true`
                                })
                                .then(response => response.json())
                                .then(confirmData => {
                                    if (confirmData.success) {
                                        // Remove the item from the UI
                                        const itemCard = this.closest('.card');
                                        itemCard.remove();
                                        
                                        // Show success message
                                        showAlert('success', confirmData.message);
                                    } else {
                                        showAlert('danger', confirmData.message);
                                    }
                                });
                            }
                        } else {
                            showAlert('danger', data.message);
                        }
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('danger', 'An error occurred');
                });
            }
        });
    });
}

// Set up wallet connection
function setupWalletConnection() {
    const connectWalletBtn = document.getElementById('connect-wallet-btn');
    if (connectWalletBtn) {
        connectWalletBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Show wallet selection modal
            showWalletModal();
        });
    }
}

// Show wallet selection modal
function showWalletModal() {
    // Create modal HTML
    const modalHTML = `
    <div class="modal fade" id="walletModal" tabindex="-1" aria-labelledby="walletModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="walletModalLabel">Connect Wallet</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>Choose a wallet to connect:</p>
            <div class="wallet-options">
              <button class="btn btn-wallet" data-wallet="phantom">
                <img src="/static/images/wallets/phantom.png" alt="Phantom" width="30">
                Phantom
              </button>
              <button class="btn btn-wallet" data-wallet="solflare">
                <img src="/static/images/wallets/solflare.png" alt="Solflare" width="30">
                Solflare
              </button>
              <button class="btn btn-wallet" data-wallet="metamask">
                <img src="/static/images/wallets/metamask.png" alt="Metamask" width="30">
                Metamask
              </button>
              <button class="btn btn-wallet" data-wallet="magiceden">
                <img src="/static/images/wallets/magiceden.png" alt="Magic Eden" width="30">
                Magic Eden
              </button>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
          </div>
        </div>
      </div>
    </div>
    `;
    
    // Add modal to DOM if it doesn't exist
    if (!document.getElementById('walletModal')) {
        const modalContainer = document.createElement('div');
        modalContainer.innerHTML = modalHTML;
        document.body.appendChild(modalContainer);
        
        // Add event listeners to wallet buttons
        document.querySelectorAll('.btn-wallet').forEach(button => {
            button.addEventListener('click', function() {
                const walletType = this.getAttribute('data-wallet');
                connectWallet(walletType);
                // Close the modal
                const walletModal = bootstrap.Modal.getInstance(document.getElementById('walletModal'));
                walletModal.hide();
            });
        });
    }
    
    // Show the modal
    const walletModal = new bootstrap.Modal(document.getElementById('walletModal'));
    walletModal.show();
}

// Connect to wallet
function connectWallet(walletType) {
    let provider;
    
    // Check if wallet is installed
    switch(walletType) {
        case 'phantom':
            provider = window.solana;
            if (!provider || !provider.isPhantom) {
                showAlert('danger', 'Phantom wallet is not installed. Please install it first.');
                window.open('https://phantom.app/', '_blank');
                return;
            }
            break;
        case 'solflare':
            provider = window.solflare;
            if (!provider || !provider.isSolflare) {
                showAlert('danger', 'Solflare wallet is not installed. Please install it first.');
                window.open('https://solflare.com/', '_blank');
                return;
            }
            break;
        case 'metamask':
            // For Solana support in Metamask, using web3.js
            if (!window.ethereum) {
                showAlert('danger', 'Metamask is not installed. Please install it first.');
                window.open('https://metamask.io/', '_blank');
                return;
            }
            connectMetamaskToSolana();
            return;
        case 'magiceden':
            // For Magic Eden wallet adapter
            if (!window.magicEden) {
                showAlert('danger', 'Magic Eden wallet is not available. Please install it first.');
                window.open('https://magiceden.io/wallet', '_blank');
                return;
            }
            connectMagicEden();
            return;
        default:
            showAlert('danger', 'Unknown wallet type');
            return;
    }
    
    // Connect to wallet
    provider.connect()
        .then(({ publicKey }) => {
            const walletAddress = publicKey.toString();
            
            // Update wallet address in the database
            fetch('/auth/connect-wallet', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `wallet_address=${walletAddress}&wallet_type=${walletType}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showAlert('success', 'Wallet connected successfully');
                    
                    // Update UI to show connected wallet
                    updateWalletUI(walletType, walletAddress);
                } else {
                    showAlert('danger', data.message);
                }
            });
        })
        .catch(error => {
            console.error('Error connecting to wallet:', error);
            showAlert('danger', 'Failed to connect to wallet');
        });
}

// Connect to Metamask for Solana
function connectMetamaskToSolana() {
    // Using Metamask's Solana support
    if (window.ethereum) {
        window.ethereum.request({ method: 'eth_requestAccounts' })
            .then(accounts => {
                // For this demo, we'll use a derived Solana address
                const ethereumAddress = accounts[0];
                const walletAddress = 'Solana' + ethereumAddress.substring(2, 10) + '...';
                
                // Update wallet address in the database
                fetch('/auth/connect-wallet', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: `wallet_address=${walletAddress}&wallet_type=metamask`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Show success message
                        showAlert('success', 'Metamask connected successfully');
                        
                        // Update UI to show connected wallet
                        updateWalletUI('metamask', walletAddress);
                    } else {
                        showAlert('danger', data.message);
                    }
                });
            })
            .catch(error => {
                console.error('Error connecting to Metamask:', error);
                showAlert('danger', 'Failed to connect to Metamask');
            });
    }
}

// Connect to Magic Eden wallet
function connectMagicEden() {
    // Simulated Magic Eden wallet connection
    const walletAddress = 'MagicEden' + Math.random().toString(36).substring(2, 10);
    
    // Update wallet address in the database
    fetch('/auth/connect-wallet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: `wallet_address=${walletAddress}&wallet_type=magiceden`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message
            showAlert('success', 'Magic Eden wallet connected successfully');
            
            // Update UI to show connected wallet
            updateWalletUI('magiceden', walletAddress);
        } else {
            showAlert('danger', data.message);
        }
    });
}

// Update wallet UI
function updateWalletUI(walletType, walletAddress) {
    const connectWalletBtn = document.getElementById('connect-wallet-btn');
    if (connectWalletBtn) {
        // Update button text and disable it
        connectWalletBtn.innerHTML = `${walletType.charAt(0).toUpperCase() + walletType.slice(1)} Connected`;
        connectWalletBtn.disabled = true;
        
        // Add wallet address to the page
        const walletDisplay = document.createElement('p');
        walletDisplay.className = 'mt-2 small';
        walletDisplay.textContent = `Connected: ${walletAddress.substring(0, 6)}...${walletAddress.substring(walletAddress.length - 4)}`;
        connectWalletBtn.parentNode.appendChild(walletDisplay);
        
        // Refresh the page sections that require wallet connection
        if (document.getElementById('nft-section')) {
            document.getElementById('nft-section').classList.remove('d-none');
        }
    }
}

// Set up NFT minting
function setupNFTMinting() {
    document.querySelectorAll('.mint-nft-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const entityType = this.dataset.entityType;
            const entityId = this.dataset.entityId;
            
            // Show minting in progress
            this.innerHTML = 'Minting...';
            this.disabled = true;
            
            fetch('/api/mint-nft', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    entity_type: entityType,
                    entity_id: entityId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showAlert('success', data.message);
                    
                    // Update button to show minted status
                    this.innerHTML = 'Minted';
                    this.classList.remove('btn-pixel');
                    this.classList.add('btn-success-pixel');
                    this.disabled = true;
                    
                    // Add NFT badge to the card
                    const card = this.closest('.card');
                    const badge = document.createElement('div');
                    badge.className = 'nft-badge';
                    badge.textContent = 'NFT';
                    card.appendChild(badge);
                } else {
                    // Reset button
                    this.innerHTML = 'Mint as NFT';
                    this.disabled = false;
                    
                    showAlert('danger', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                
                // Reset button
                this.innerHTML = 'Mint as NFT';
                this.disabled = false;
                
                showAlert('danger', 'An error occurred during minting');
            });
        });
    });
}

// Set up Elixir activation
function setupElixirActivation() {
    document.querySelectorAll('.activate-elixir-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const elixirId = this.dataset.elixirId;
            
            // Show activation in progress
            this.innerHTML = 'Activating...';
            this.disabled = true;
            
            fetch('/api/activate-elixir', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    elixir_id: elixirId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showAlert('success', data.message);
                    
                    // Update button to show activated status
                    this.innerHTML = 'Activated';
                    this.classList.remove('btn-pixel');
                    this.classList.add('btn-success-pixel');
                    this.disabled = true;
                } else {
                    // Reset button
                    this.innerHTML = 'Activate';
                    this.disabled = false;
                    
                    showAlert('danger', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                
                // Reset button
                this.innerHTML = 'Activate';
                this.disabled = false;
                
                showAlert('danger', 'An error occurred during activation');
            });
        });
    });
}

// Helper function to show alerts
function showAlert(type, message) {
    const alertsContainer = document.createElement('div');
    alertsContainer.className = 'alert-container position-fixed top-0 end-0 p-3';
    alertsContainer.style.zIndex = '9999';
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.role = 'alert';
    
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertsContainer.appendChild(alert);
    document.body.appendChild(alertsContainer);
    
    // Remove alert after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => {
            alertsContainer.remove();
        }, 300);
    }, 5000);
} 