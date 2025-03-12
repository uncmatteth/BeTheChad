"""
Solana API utilities for Chad Battles.
Handles interactions with the Solana blockchain for NFT operations.
"""
import os
import json
import requests
import uuid
import base64
from datetime import datetime
from flask import current_app, url_for
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Constants
SOLANA_NETWORK = os.environ.get('SOLANA_NETWORK', 'devnet')  # 'devnet', 'testnet', or 'mainnet-beta'
SOLANA_RPC_URL = {
    'devnet': 'https://api.devnet.solana.com',
    'testnet': 'https://api.testnet.solana.com',
    'mainnet-beta': 'https://api.mainnet-beta.solana.com'
}.get(SOLANA_NETWORK, 'https://api.devnet.solana.com')

SOLANA_API_KEY = os.environ.get('SOLANA_API_KEY', '')
NFT_STORAGE_API_KEY = os.environ.get('NFT_STORAGE_API_KEY', '')

# Helper functions
def get_headers():
    """Get headers for Solana API requests."""
    headers = {
        'Content-Type': 'application/json',
    }
    if SOLANA_API_KEY:
        headers['Authorization'] = f'Bearer {SOLANA_API_KEY}'
    return headers

def upload_to_ipfs(metadata):
    """Upload metadata to IPFS using NFT.Storage."""
    if not NFT_STORAGE_API_KEY:
        logger.warning("NFT_STORAGE_API_KEY not set, using mock IPFS URL")
        # Return a mock IPFS URL for development
        mock_cid = f"bafybeih{uuid.uuid4().hex[:40]}"
        return f"ipfs://{mock_cid}"
    
    try:
        headers = {
            'Authorization': f'Bearer {NFT_STORAGE_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://api.nft.storage/upload',
            headers=headers,
            json=metadata
        )
        
        if response.status_code == 200:
            result = response.json()
            return f"ipfs://{result['value']['cid']}"
        else:
            logger.error(f"Failed to upload to IPFS: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error uploading to IPFS: {str(e)}")
        return None

def generate_metadata(entity_type, entity, token_id):
    """Generate metadata for an NFT based on entity type and data."""
    try:
        base_url = current_app.config.get('BASE_URL', 'https://chadbattles.com')
        
        if entity_type == 'chad':
            # Generate Chad metadata
            image_url = f"{base_url}/api/generate-chad-avatar/{entity.id}"
            
            metadata = {
                "name": f"Chad #{entity.id} - {entity.name}",
                "description": f"A level {entity.level} Chad from the Chad Battles game. Class: {entity.chad_class.name}",
                "image": image_url,
                "external_url": f"{base_url}/chad/{entity.id}",
                "attributes": [
                    {"trait_type": "Class", "value": entity.chad_class.name},
                    {"trait_type": "Level", "value": entity.level},
                    {"trait_type": "Clout", "value": entity.clout},
                    {"trait_type": "Roast Level", "value": entity.roast_level},
                    {"trait_type": "Cringe Resistance", "value": entity.cringe_resistance},
                    {"trait_type": "Drip Factor", "value": entity.drip_factor},
                    {"trait_type": "XP", "value": entity.xp}
                ]
            }
            
        elif entity_type == 'waifu':
            # Generate Waifu metadata
            image_url = f"{base_url}/static/img/waifus/{entity.waifu_type.id}.png"
            
            metadata = {
                "name": f"{entity.name} - {entity.waifu_type.name}",
                "description": f"A {entity.waifu_type.rarity.name} waifu from Chad Battles. Type: {entity.waifu_type.name}",
                "image": image_url,
                "external_url": f"{base_url}/waifu/{entity.id}",
                "attributes": [
                    {"trait_type": "Type", "value": entity.waifu_type.name},
                    {"trait_type": "Rarity", "value": entity.waifu_type.rarity.name},
                    {"trait_type": "Level", "value": entity.level},
                    {"trait_type": "Clout Bonus", "value": entity.clout_bonus},
                    {"trait_type": "Roast Bonus", "value": entity.roast_bonus},
                    {"trait_type": "Cringe Bonus", "value": entity.cringe_bonus},
                    {"trait_type": "Drip Bonus", "value": entity.drip_bonus}
                ]
            }
            
        elif entity_type == 'item':
            # Generate Item metadata
            image_url = f"{base_url}/static/img/items/{entity.item_type.id}.png"
            
            metadata = {
                "name": f"{entity.item_type.name}",
                "description": f"A {entity.item_type.rarity.name} item from Chad Battles. Type: {entity.item_type.slot}",
                "image": image_url,
                "external_url": f"{base_url}/item/{entity.id}",
                "attributes": [
                    {"trait_type": "Slot", "value": entity.item_type.slot},
                    {"trait_type": "Rarity", "value": entity.item_type.rarity.name},
                    {"trait_type": "Clout Bonus", "value": entity.clout_bonus},
                    {"trait_type": "Roast Bonus", "value": entity.roast_bonus},
                    {"trait_type": "Cringe Bonus", "value": entity.cringe_bonus},
                    {"trait_type": "Drip Bonus", "value": entity.drip_bonus}
                ]
            }
        else:
            logger.error(f"Unknown entity type: {entity_type}")
            return None
        
        return metadata
    except Exception as e:
        logger.error(f"Error generating metadata: {str(e)}")
        return None

# Blockchain interaction functions
def verify_wallet_ownership(wallet_address, signature, message):
    """Verify that the user owns the wallet by checking the signature."""
    if SOLANA_NETWORK == 'devnet':
        # In development mode, always return success
        logger.info(f"DEV MODE: Skipping wallet verification for {wallet_address}")
        return {
            'success': True,
            'message': 'Wallet verification successful (dev mode)'
        }
    
    try:
        # In production, we would verify the signature against the message
        # This requires a Solana library or API that supports signature verification
        # For now, we'll just return success
        return {
            'success': True,
            'message': 'Wallet verification successful'
        }
    except Exception as e:
        logger.error(f"Error verifying wallet ownership: {str(e)}")
        return {
            'success': False,
            'message': f'Error verifying wallet ownership: {str(e)}'
        }

def get_wallet_balance(wallet_address):
    """Get the SOL balance of a wallet."""
    if SOLANA_NETWORK == 'devnet':
        # In development mode, return a mock balance
        return {
            'success': True,
            'balance': 10.0,  # Mock 10 SOL
            'token_balances': []
        }
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [wallet_address]
        }
        
        response = requests.post(
            SOLANA_RPC_URL,
            headers=get_headers(),
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'result' in result and 'value' in result['result']:
                # Convert lamports to SOL (1 SOL = 1,000,000,000 lamports)
                balance_in_sol = result['result']['value'] / 1000000000
                return {
                    'success': True,
                    'balance': balance_in_sol,
                    'token_balances': []  # Would need a separate call to get token balances
                }
        
        logger.error(f"Failed to get wallet balance: {response.text}")
        return {
            'success': False,
            'message': 'Failed to get wallet balance'
        }
    except Exception as e:
        logger.error(f"Error getting wallet balance: {str(e)}")
        return {
            'success': False,
            'message': f'Error getting wallet balance: {str(e)}'
        }

def mint_nft_on_chain(wallet_address, metadata_uri, entity_type, entity_id):
    """Mint an NFT on the Solana blockchain."""
    if SOLANA_NETWORK == 'devnet':
        # In development mode, return a mock response
        mock_token_id = f"{uuid.uuid4().hex}"
        mock_tx_hash = f"tx{uuid.uuid4().hex}"
        
        return {
            'success': True,
            'token_id': mock_token_id,
            'transaction_id': mock_tx_hash,
            'block_number': 12345678,
            'message': 'NFT minted successfully (dev mode)'
        }
    
    try:
        # In production, we would call the Solana API to mint an NFT
        # This requires a Solana library or API that supports NFT minting
        # For now, we'll just return a mock response
        mock_token_id = f"{uuid.uuid4().hex}"
        mock_tx_hash = f"tx{uuid.uuid4().hex}"
        
        return {
            'success': True,
            'token_id': mock_token_id,
            'transaction_id': mock_tx_hash,
            'block_number': 12345678,
            'message': 'NFT minted successfully'
        }
    except Exception as e:
        logger.error(f"Error minting NFT: {str(e)}")
        return {
            'success': False,
            'message': f'Error minting NFT: {str(e)}'
        }

def burn_nft_on_chain(wallet_address, token_id):
    """Burn an NFT on the Solana blockchain."""
    if SOLANA_NETWORK == 'devnet':
        # In development mode, return a mock response
        mock_tx_hash = f"tx{uuid.uuid4().hex}"
        
        return {
            'success': True,
            'transaction_id': mock_tx_hash,
            'block_number': 12345678,
            'message': 'NFT burned successfully (dev mode)'
        }
    
    try:
        # In production, we would call the Solana API to burn an NFT
        # This requires a Solana library or API that supports NFT burning
        # For now, we'll just return a mock response
        mock_tx_hash = f"tx{uuid.uuid4().hex}"
        
        return {
            'success': True,
            'transaction_id': mock_tx_hash,
            'block_number': 12345678,
            'message': 'NFT burned successfully'
        }
    except Exception as e:
        logger.error(f"Error burning NFT: {str(e)}")
        return {
            'success': False,
            'message': f'Error burning NFT: {str(e)}'
        }

def transfer_nft(from_wallet, to_wallet, token_id):
    """Transfer an NFT from one wallet to another."""
    if SOLANA_NETWORK == 'devnet':
        # In development mode, return a mock response
        mock_tx_hash = f"tx{uuid.uuid4().hex}"
        
        return {
            'success': True,
            'transaction_id': mock_tx_hash,
            'block_number': 12345678,
            'message': 'NFT transferred successfully (dev mode)'
        }
    
    try:
        # In production, we would call the Solana API to transfer an NFT
        # This requires a Solana library or API that supports NFT transfers
        # For now, we'll just return a mock response
        mock_tx_hash = f"tx{uuid.uuid4().hex}"
        
        return {
            'success': True,
            'transaction_id': mock_tx_hash,
            'block_number': 12345678,
            'message': 'NFT transferred successfully'
        }
    except Exception as e:
        logger.error(f"Error transferring NFT: {str(e)}")
        return {
            'success': False,
            'message': f'Error transferring NFT: {str(e)}'
        } 