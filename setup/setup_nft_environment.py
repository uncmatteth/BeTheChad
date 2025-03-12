#!/usr/bin/env python
"""
NFT Environment Setup Script

This script sets up the necessary directories and configurations for the NFT system
to work properly across all environments (dev, test, prod).

Usage:
  python setup_nft_environment.py [--env {dev|test|prod}]
"""

import os
import sys
import argparse
import logging
import json
import shutil
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("nft-setup")

# Constants
ENVIRONMENTS = ['dev', 'test', 'prod']
ENTITY_TYPES = ['chad', 'waifu', 'item']
PLACEHOLDER_IMAGE = "placeholder_nft.png"

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Setup NFT environment.')
    parser.add_argument('--env', choices=ENVIRONMENTS, default='dev',
                        help='Environment to set up (default: dev)')
    return parser.parse_args()

def setup_metadata_directories(base_path, env):
    """Set up metadata directories for NFT storage."""
    logger.info(f"Setting up metadata directories for {env} environment")
    
    # Create base static directory
    static_dir = base_path / 'app' / 'static'
    metadata_dir = static_dir / 'metadata'
    
    # Create metadata directory if it doesn't exist
    if not metadata_dir.exists():
        metadata_dir.mkdir(parents=True)
        logger.info(f"Created metadata directory: {metadata_dir}")
    
    # Create entity-specific directories
    for entity_type in ENTITY_TYPES:
        entity_dir = metadata_dir / entity_type
        if not entity_dir.exists():
            entity_dir.mkdir(parents=True)
            logger.info(f"Created {entity_type} metadata directory: {entity_dir}")
    
    return metadata_dir

def setup_placeholders(static_dir):
    """Set up placeholder images and metadata."""
    logger.info("Setting up placeholder images and metadata")
    
    # Create placeholders directory
    placeholders_dir = static_dir / 'img' / 'placeholders'
    if not placeholders_dir.exists():
        placeholders_dir.mkdir(parents=True)
        logger.info(f"Created placeholders directory: {placeholders_dir}")
    
    # Check if placeholder image exists
    placeholder_image_path = placeholders_dir / PLACEHOLDER_IMAGE
    if not placeholder_image_path.exists():
        # Copy a basic placeholder image or create one
        try:
            # Try to copy from src/img/placeholders if it exists
            src_placeholder = Path('src') / 'img' / 'placeholders' / PLACEHOLDER_IMAGE
            if src_placeholder.exists():
                shutil.copy(src_placeholder, placeholder_image_path)
                logger.info(f"Copied placeholder image from {src_placeholder} to {placeholder_image_path}")
            else:
                # Note: In a real scenario, we'd create a proper image
                # For this setup script, we just log a warning
                logger.warning(f"Placeholder image not found at {src_placeholder}. Please add it manually.")
        except Exception as e:
            logger.error(f"Error setting up placeholder image: {str(e)}")
    
    # Create placeholder metadata for each entity type
    for entity_type in ENTITY_TYPES:
        placeholder_metadata = {
            "name": f"Placeholder {entity_type.capitalize()} NFT",
            "description": f"This is a placeholder {entity_type} NFT metadata file.",
            "image": f"/static/img/placeholders/{PLACEHOLDER_IMAGE}",
            "attributes": [
                {
                    "trait_type": "Type",
                    "value": "Placeholder"
                }
            ],
            "external_url": "https://chadbattles.com"
        }
        
        placeholder_file = static_dir / 'metadata' / entity_type / 'placeholder.json'
        if not placeholder_file.exists():
            with open(placeholder_file, 'w') as f:
                json.dump(placeholder_metadata, f, indent=2)
            logger.info(f"Created placeholder metadata file: {placeholder_file}")

def setup_env_config(base_path, env):
    """Update environment configuration for NFT support."""
    logger.info(f"Updating {env} environment configuration")
    
    # Define environment-specific configuration
    env_configs = {
        'dev': {
            'NFT_ENABLED': True,
            'NFT_METADATA_BASE_URL': 'http://localhost:5000/static/metadata',
            'NFT_ROYALTY_PERCENTAGE': 1.0,
            'CHADCOIN_ENABLED': True,
            'NFT_MINT_COOLDOWN_SECONDS': 60
        },
        'test': {
            'NFT_ENABLED': True,
            'NFT_METADATA_BASE_URL': 'https://test.chadbattles.com/static/metadata',
            'NFT_ROYALTY_PERCENTAGE': 1.0,
            'CHADCOIN_ENABLED': True,
            'NFT_MINT_COOLDOWN_SECONDS': 60
        },
        'prod': {
            'NFT_ENABLED': True,
            'NFT_METADATA_BASE_URL': 'https://chadbattles.com/static/metadata',
            'NFT_ROYALTY_PERCENTAGE': 1.0,
            'CHADCOIN_ENABLED': True,
            'NFT_MINT_COOLDOWN_SECONDS': 300
        }
    }
    
    # Get the config for the specified environment
    env_config = env_configs.get(env, env_configs['dev'])
    
    # Path to .env file
    env_file_path = base_path / '.env'
    if not env_file_path.exists():
        logger.warning(f".env file not found at {env_file_path}. Creating a new one.")
        with open(env_file_path, 'w') as f:
            f.write("# Environment Configuration\n")
    
    # Read current .env file
    with open(env_file_path, 'r') as f:
        lines = f.readlines()
    
    # Update or add NFT configuration
    updated_lines = []
    nft_config_section = False
    nft_config_added = {key: False for key in env_config}
    
    for line in lines:
        if line.strip() == "# NFT Configuration":
            nft_config_section = True
        
        # Check if line contains any of our config keys
        skip_line = False
        for key in env_config:
            if line.strip().startswith(key + '='):
                # Update existing config
                updated_lines.append(f"{key}={env_config[key]}\n")
                nft_config_added[key] = True
                skip_line = True
                break
        
        if not skip_line:
            updated_lines.append(line)
    
    # Add NFT section if not present
    if not nft_config_section:
        updated_lines.append("\n# NFT Configuration\n")
    
    # Add any missing config values
    for key, value in env_config.items():
        if not nft_config_added[key]:
            updated_lines.append(f"{key}={value}\n")
    
    # Write updated .env file
    with open(env_file_path, 'w') as f:
        f.writelines(updated_lines)
    
    logger.info(f"Updated .env file with NFT configuration for {env} environment")

def main():
    """Main function to run the setup script."""
    args = parse_args()
    env = args.env
    
    logger.info(f"Starting NFT environment setup for {env}")
    
    # Get base path (project root)
    base_path = Path(__file__).resolve().parent.parent
    logger.info(f"Project base path: {base_path}")
    
    # Setup metadata directories
    metadata_dir = setup_metadata_directories(base_path, env)
    
    # Setup placeholder images and metadata
    setup_placeholders(base_path / 'app' / 'static')
    
    # Update environment configuration
    setup_env_config(base_path, env)
    
    logger.info(f"NFT environment setup complete for {env}")
    logger.info("You may need to restart the application for changes to take effect.")

if __name__ == "__main__":
    main() 