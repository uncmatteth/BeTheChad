import os
import sys
import shutil
import json

def ensure_directory(path):
    """Make sure a directory exists"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")

def create_metadata_directories():
    """Create directories for NFT metadata and images"""
    # Create metadata directories
    metadata_dir = os.path.join('app', 'static', 'metadata')
    ensure_directory(metadata_dir)
    
    # Create subdirectories for each entity type
    for entity_type in ['chad', 'waifu', 'item']:
        ensure_directory(os.path.join(metadata_dir, entity_type))
    
    # Create images directory
    nft_images_dir = os.path.join('app', 'static', 'img', 'nft')
    ensure_directory(nft_images_dir)
    
    # Create placeholder image if it doesn't exist
    placeholder_image = os.path.join('app', 'static', 'img', 'placeholder.png')
    if not os.path.exists(placeholder_image):
        # Create a simple placeholder image file
        with open(placeholder_image, 'w') as f:
            f.write("This is a placeholder for an image file")
        print(f"Created placeholder image at: {placeholder_image}")

def setup_wallets_directory():
    """Set up wallets directory for blockchain interaction"""
    wallets_dir = os.path.join('app', 'static', 'wallets')
    ensure_directory(wallets_dir)
    
    # Create a sample wallet file for development
    sample_wallet = os.path.join(wallets_dir, 'dev_wallet.json')
    if not os.path.exists(sample_wallet):
        wallet_data = {
            "public_key": "sample_public_key",
            "private_key": "sample_private_key",
            "environment": "development"
        }
        with open(sample_wallet, 'w') as f:
            json.dump(wallet_data, f, indent=2)
        print(f"Created sample wallet file at: {sample_wallet}")

def main():
    print("Setting up the environment for Chad Battles...")
    
    # Create necessary directories
    create_metadata_directories()
    setup_wallets_directory()
    
    print("\nEnvironment setup complete!")
    print("\nYou can now run the application with:")
    print("python run.py")

if __name__ == "__main__":
    main() 