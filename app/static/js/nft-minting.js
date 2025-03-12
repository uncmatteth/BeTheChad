// NFT Minting Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize minting buttons
    initMintButtons();
    
    // Initialize the minting modal
    initMintModal();
    
    // Initialize wallet notification handling
    initWalletNotifications();
});

// Initialize minting buttons
function initMintButtons() {
    document.querySelectorAll('.mint-nft-button').forEach(button => {
        button.addEventListener('click', function(e) {
            const entityType = this.dataset.entityType;
            const entityId = this.dataset.entityId;
            
            // Show the minting confirmation modal
            showMintConfirmation(entityType, entityId);
        });
    });
}

// Initialize the minting modal
function initMintModal() {
    // Close modal buttons
    document.querySelectorAll('.close-mint-modal').forEach(button => {
        button.addEventListener('click', function() {
            document.getElementById('mintNftModal').classList.remove('show');
            document.getElementById('mintNftModal').style.display = 'none';
            document.querySelector('.modal-backdrop').remove();
            document.body.classList.remove('modal-open');
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
        });
    });
    
    // Confirm minting button
    document.getElementById('confirmMintButton')?.addEventListener('click', function() {
        const entityType = this.dataset.entityType;
        const entityId = this.dataset.entityId;
        
        // Show loading spinner
        this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Minting...';
        this.disabled = true;
        
        // Call the mint API
        mintNFT(entityType, entityId);
    });
}

// Show minting confirmation modal
function showMintConfirmation(entityType, entityId) {
    const modal = document.getElementById('mintNftModal');
    const confirmButton = document.getElementById('confirmMintButton');
    const entityNameElement = document.getElementById('entityName');
    const mintWarningElement = document.getElementById('mintWarning');
    
    // Set the entity type and ID
    confirmButton.dataset.entityType = entityType;
    confirmButton.dataset.entityId = entityId;
    
    // Update modal content based on entity type
    let entityName = '';
    let warningText = '';
    
    switch(entityType) {
        case 'chad':
            entityName = 'Chad character';
            warningText = 'Warning: Minting your Chad will lock its current avatar. Future level ups and equipment changes will not affect the NFT image.';
            break;
        case 'waifu':
            entityName = 'Waifu';
            warningText = 'Warning: Make sure your Waifu has all desired equipment before minting!';
            break;
        case 'item':
            entityName = 'Item';
            warningText = '';
            break;
    }
    
    entityNameElement.textContent = entityName;
    mintWarningElement.textContent = warningText;
    
    // Reset confirm button
    confirmButton.innerHTML = 'Confirm Mint';
    confirmButton.disabled = false;
    
    // Show the modal
    modal.classList.add('show');
    modal.style.display = 'block';
    document.body.classList.add('modal-open');
    document.body.style.overflow = 'hidden';
    document.body.style.paddingRight = '15px';
    
    // Add backdrop
    const backdrop = document.createElement('div');
    backdrop.classList.add('modal-backdrop', 'fade', 'show');
    document.body.appendChild(backdrop);
}

// Function to mint an NFT
function mintNFT(entityType, entityId) {
    fetch('/api/mint_nft', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            entity_type: entityType,
            entity_id: entityId
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Failed to mint NFT');
            });
        }
        return response.json();
    })
    .then(data => {
        // Success - show success notification
        showNotification('success', 'NFT successfully minted!', 'Your NFT has been successfully minted to your wallet. View it in your NFT collection.');
        
        // Close the modal
        document.querySelector('.close-mint-modal').click();
        
        // Update UI to show minted status
        updateMintedStatus(entityType, entityId);
        
        // Reload page after 2 seconds to reflect changes
        setTimeout(() => {
            window.location.reload();
        }, 2000);
    })
    .catch(error => {
        // Error - show error notification
        showNotification('error', 'Minting Failed', error.message);
        
        // Reset confirm button
        const confirmButton = document.getElementById('confirmMintButton');
        confirmButton.innerHTML = 'Confirm Mint';
        confirmButton.disabled = false;
        
        // Close the modal
        document.querySelector('.close-mint-modal').click();
    });
}

// Update UI to show minted status
function updateMintedStatus(entityType, entityId) {
    const button = document.querySelector(`.mint-nft-button[data-entity-type="${entityType}"][data-entity-id="${entityId}"]`);
    if (button) {
        button.outerHTML = `
            <button class="btn btn-sm btn-success" disabled>
                <i class="fas fa-check me-1"></i> Minted
            </button>
        `;
    }
}

// Initialize wallet notification handling
function initWalletNotifications() {
    // Listen for wallet connection events
    document.addEventListener('walletConnected', function(e) {
        // Enable all mint buttons when wallet is connected
        document.querySelectorAll('.mint-nft-button[disabled]').forEach(button => {
            button.removeAttribute('disabled');
            button.removeAttribute('title');
        });
    });
    
    // Listen for wallet disconnection events
    document.addEventListener('walletDisconnected', function(e) {
        // Disable all mint buttons when wallet is disconnected
        document.querySelectorAll('.mint-nft-button').forEach(button => {
            button.setAttribute('disabled', 'true');
            button.setAttribute('title', 'Connect wallet to mint NFT');
        });
    });
}

// Function to show notifications
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