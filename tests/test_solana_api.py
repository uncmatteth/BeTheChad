"""
Tests for Solana API utilities in Chad Battles.
"""
import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from app.extensions import db
from app.utils.solana_api import (
    get_headers, 
    upload_to_ipfs, 
    generate_metadata,
    verify_wallet_ownership,
    get_wallet_balance,
    mint_nft_on_chain,
    burn_nft_on_chain,
    transfer_nft
)
import json
import uuid

class SolanaAPITestCase(unittest.TestCase):
    """Test case for Solana API utilities."""
    
    def setUp(self):
        """Set up the test environment."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Tear down the test environment."""
        self.app_context.pop()
    
    def test_get_headers(self):
        """Test get_headers function."""
        headers = get_headers()
        self.assertIn('Content-Type', headers)
        self.assertEqual(headers['Content-Type'], 'application/json')
    
    @patch('app.utils.solana_api.NFT_STORAGE_API_KEY', '')
    def test_upload_to_ipfs_mock(self):
        """Test upload_to_ipfs function with mock IPFS."""
        metadata = {"name": "Test NFT", "description": "Test description"}
        ipfs_uri = upload_to_ipfs(metadata)
        self.assertIsNotNone(ipfs_uri)
        self.assertTrue(ipfs_uri.startswith('ipfs://'))
    
    @patch('app.utils.solana_api.requests.post')
    @patch('app.utils.solana_api.NFT_STORAGE_API_KEY', 'mock_api_key')
    def test_upload_to_ipfs_real(self, mock_post):
        """Test upload_to_ipfs function with mocked API response."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'value': {'cid': 'bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq'}
        }
        mock_post.return_value = mock_response
        
        metadata = {"name": "Test NFT", "description": "Test description"}
        ipfs_uri = upload_to_ipfs(metadata)
        
        self.assertEqual(ipfs_uri, 'ipfs://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq')
        mock_post.assert_called_once()
    
    def test_verify_wallet_ownership(self):
        """Test verify_wallet_ownership function."""
        result = verify_wallet_ownership('mock_wallet_address', 'mock_signature', 'mock_message')
        self.assertTrue(result['success'])
    
    def test_get_wallet_balance(self):
        """Test get_wallet_balance function."""
        result = get_wallet_balance('mock_wallet_address')
        self.assertTrue(result['success'])
        self.assertEqual(result['balance'], 10.0)  # Mock balance in devnet mode
    
    def test_mint_nft_on_chain(self):
        """Test mint_nft_on_chain function."""
        result = mint_nft_on_chain('mock_wallet_address', 'mock_metadata_uri', 'chad', 1)
        self.assertTrue(result['success'])
        self.assertIn('token_id', result)
        self.assertIn('transaction_id', result)
        self.assertEqual(result['block_number'], 12345678)  # Mock block number
    
    def test_burn_nft_on_chain(self):
        """Test burn_nft_on_chain function."""
        result = burn_nft_on_chain('mock_wallet_address', 'mock_token_id')
        self.assertTrue(result['success'])
        self.assertIn('transaction_id', result)
        self.assertEqual(result['block_number'], 12345678)  # Mock block number
    
    def test_transfer_nft(self):
        """Test transfer_nft function."""
        result = transfer_nft('mock_from_wallet', 'mock_to_wallet', 'mock_token_id')
        self.assertTrue(result['success'])
        self.assertIn('transaction_id', result)
        self.assertEqual(result['block_number'], 12345678)  # Mock block number
    
    @patch('app.utils.solana_api.current_app')
    def test_generate_metadata_chad(self, mock_current_app):
        """Test generate_metadata function for Chad entity."""
        # Mock current_app and entity
        mock_current_app.config.get.return_value = 'https://chadbattles.com'
        
        mock_entity = MagicMock()
        mock_entity.id = 1
        mock_entity.name = 'TestChad'
        mock_entity.level = 10
        mock_entity.xp = 1000
        mock_entity.clout = 100
        mock_entity.roast_level = 50
        mock_entity.cringe_resistance = 75
        mock_entity.drip_factor = 80
        
        mock_chad_class = MagicMock()
        mock_chad_class.name = 'TestClass'
        mock_entity.chad_class = mock_chad_class
        
        metadata = generate_metadata('chad', mock_entity, 'token123')
        
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata['name'], 'Chad #1 - TestChad')
        self.assertEqual(metadata['description'], 'A level 10 Chad from the Chad Battles game. Class: TestClass')
        self.assertEqual(metadata['image'], 'https://chadbattles.com/api/generate-chad-avatar/1')
        self.assertEqual(len(metadata['attributes']), 7)  # 7 attributes

if __name__ == '__main__':
    unittest.main() 