#!/usr/bin/env python
"""
Chad Battles Music Player Verification Script

This script performs checks on the music player implementation to verify that it's working correctly.
It checks for the existence of music files, proper API endpoints, and other critical functionality.
"""

import os
import sys
import json
import requests
from urllib.parse import urljoin
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"music_player_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_LOCAL_URL = "http://localhost:5000"
DEFAULT_PROD_URL = "https://chadbattles.fun"
EXPECTED_MUSIC_FILES_COUNT = 104  # We should have 104 "Be the Chad" MP3 files


def check_local_music_files():
    """Check if the music files exist locally in the expected directory."""
    music_dir = os.path.join("app", "static", "music")
    
    if not os.path.exists(music_dir):
        logger.error(f"Music directory not found: {music_dir}")
        return False
    
    mp3_files = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
    
    logger.info(f"Found {len(mp3_files)} MP3 files in {music_dir}")
    
    # Check if we have the expected number of files
    if len(mp3_files) < EXPECTED_MUSIC_FILES_COUNT:
        logger.warning(f"Expected {EXPECTED_MUSIC_FILES_COUNT} music files, but found {len(mp3_files)}")
        return False
    
    # Check for "Be the Chad" naming pattern
    chad_files = [f for f in mp3_files if "Be the Chad" in f]
    logger.info(f"Found {len(chad_files)} 'Be the Chad' MP3 files")
    
    return len(chad_files) >= EXPECTED_MUSIC_FILES_COUNT


def check_music_list_endpoint(base_url):
    """Check if the /music/list endpoint returns the expected data."""
    try:
        endpoint = urljoin(base_url, "/music/list")
        logger.info(f"Checking music list endpoint: {endpoint}")
        
        response = requests.get(endpoint, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"Endpoint returned status code {response.status_code}")
            return False
        
        data = response.json()
        
        if not isinstance(data, list):
            logger.error(f"Expected a list of music files, got {type(data)}")
            return False
        
        logger.info(f"Endpoint returned {len(data)} music files")
        
        # Check if we have the expected number of files
        if len(data) < EXPECTED_MUSIC_FILES_COUNT:
            logger.warning(f"Expected {EXPECTED_MUSIC_FILES_COUNT} music files, but found {len(data)}")
        
        # Check if the data structure is correct
        if data and not all(isinstance(item, dict) and 'title' in item and 'path' in item for item in data):
            logger.error("Data structure is incorrect")
            return False
        
        return True
    except Exception as e:
        logger.error(f"Error checking music list endpoint: {e}")
        return False


def check_individual_music_file(base_url):
    """Check if we can access an individual music file."""
    try:
        # First get the list of music files
        list_endpoint = urljoin(base_url, "/music/list")
        response = requests.get(list_endpoint, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"Music list endpoint returned status code {response.status_code}")
            return False
        
        data = response.json()
        
        if not data:
            logger.error("No music files found")
            return False
        
        # Try to access the first music file
        first_file = data[0]
        file_path = first_file.get('path')
        
        if not file_path:
            logger.error("No path found for the first music file")
            return False
        
        # Convert relative path to absolute URL
        if file_path.startswith('/'):
            file_url = urljoin(base_url, file_path)
        else:
            file_url = urljoin(base_url, '/' + file_path)
        
        logger.info(f"Checking access to music file: {file_url}")
        
        file_response = requests.head(file_url, timeout=10)
        
        if file_response.status_code != 200:
            logger.error(f"Music file returned status code {file_response.status_code}")
            return False
        
        # Check content type
        content_type = file_response.headers.get('Content-Type', '')
        if 'audio' not in content_type.lower():
            logger.warning(f"Expected audio content type, got {content_type}")
        
        logger.info(f"Successfully accessed music file: {file_url}")
        return True
    except Exception as e:
        logger.error(f"Error checking individual music file: {e}")
        return False


def check_debug_endpoint(base_url):
    """Check if the music debug endpoint is working."""
    try:
        endpoint = urljoin(base_url, "/music/debug")
        logger.info(f"Checking music debug endpoint: {endpoint}")
        
        response = requests.get(endpoint, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"Debug endpoint returned status code {response.status_code}")
            return False
        
        data = response.json()
        
        # Check if debug info contains the expected keys
        expected_keys = ['version', 'timestamp', 'env', 'dirs', 'files']
        missing_keys = [key for key in expected_keys if key not in data]
        
        if missing_keys:
            logger.warning(f"Debug endpoint is missing some expected keys: {missing_keys}")
        
        logger.info("Successfully accessed music debug endpoint")
        return True
    except Exception as e:
        logger.error(f"Error checking debug endpoint: {e}")
        return False


def run_verification(base_url=DEFAULT_LOCAL_URL):
    """Run all verification checks and return the results."""
    logger.info(f"Starting music player verification against {base_url}")
    
    results = {
        "local_files": check_local_music_files(),
        "music_list_endpoint": check_music_list_endpoint(base_url),
        "individual_music_file": check_individual_music_file(base_url),
        "debug_endpoint": check_debug_endpoint(base_url)
    }
    
    # Calculate overall success
    success = all(results.values())
    
    logger.info(f"Verification completed with {'SUCCESS' if success else 'FAILURE'}")
    logger.info(f"Results: {json.dumps(results, indent=2)}")
    
    return success, results


def main():
    """Main function to run the verification script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Verify Chad Battles Music Player functionality')
    parser.add_argument('--local', action='store_true', help='Check against local development server')
    parser.add_argument('--prod', action='store_true', help='Check against production server')
    parser.add_argument('--url', type=str, help='Custom base URL to check against')
    
    args = parser.parse_args()
    
    # Determine which URL to use
    base_url = DEFAULT_LOCAL_URL
    env_name = "local development"
    
    if args.prod:
        base_url = DEFAULT_PROD_URL
        env_name = "production"
    elif args.url:
        base_url = args.url
        env_name = f"custom URL: {args.url}"
    
    logger.info(f"Verifying music player on {env_name}")
    
    success, results = run_verification(base_url)
    
    # Update the verification document with results
    try:
        update_verification_document(results)
    except Exception as e:
        logger.error(f"Failed to update verification document: {e}")
    
    # Return success or failure exit code
    sys.exit(0 if success else 1)


def update_verification_document(results):
    """Update the MUSIC_PLAYER_VERIFICATION.md document with the verification results."""
    verification_file = "MUSIC_PLAYER_VERIFICATION.md"
    
    if not os.path.exists(verification_file):
        logger.warning(f"Verification document not found: {verification_file}")
        return
    
    try:
        with open(verification_file, 'r') as f:
            content = f.read()
        
        # Add verification results to the Notes section
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        results_text = f"\n### Verification Results ({timestamp})\n\n"
        results_text += "| Check | Result |\n"
        results_text += "|-------|--------|\n"
        
        for check, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            results_text += f"| {check.replace('_', ' ').title()} | {status} |\n"
        
        # Find the Notes section and add our results
        if "## Notes and Findings" in content:
            updated_content = content.replace(
                "## Notes and Findings", 
                "## Notes and Findings\n" + results_text
            )
        else:
            # If no Notes section, add it at the end
            updated_content = content + "\n## Notes and Findings\n" + results_text
        
        with open(verification_file, 'w') as f:
            f.write(updated_content)
        
        logger.info(f"Updated verification document: {verification_file}")
    except Exception as e:
        logger.error(f"Error updating verification document: {e}")
        raise


if __name__ == "__main__":
    main() 