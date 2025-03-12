"""
Tests for NFT functionality in Chad Battles.
"""
import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.nft import NFT
from app.models.transaction import Transaction
import json
import uuid

class NFTTestCase(unittest.TestCase):
    """Test case for NFT functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        # Create test database
        db.create_all()
        
        # Create test user with wallet
        self.test_user = User(
            username='test_user',
            email='test@example.com',
            wallet_address='test_wallet_address',
            wallet_type='phantom'
        )
        self.test_user.set_password('password')
        db.session.add(self.test_user)
        
        # Create recipient user with wallet
        self.recipient_user = User(
            username='recipient_user',
            email='recipient@example.com',
            wallet_address='recipient_wallet_address',
            wallet_type='phantom'
        )
        self.recipient_user.set_password('password')
        db.session.add(self.recipient_user)
        
        db.session.commit()
        
        # Login test user
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.test_user.id
    
    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    @patch('app.controllers.nft.mint_nft_on_chain')
    def test_mint_nft(self, mock_mint_nft_on_chain):
        """Test minting an NFT."""
        # Mock the on-chain minting
        mock_mint_nft_on_chain.return_value = {
            'success': True,
            'token_id': 'test_token_id',
            'transaction_id': 'test_transaction_id',
            'block_number': 12345678
        }
        
        # Mint an NFT
        response = self.client.post('/api/mint-nft', json={
            'entity_type': 'chad',
            'entity_id': 1
        })
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('token_id', data)
        
        # Check database
        nft = NFT.query.filter_by(token_id='test_token_id').first()
        self.assertIsNotNone(nft)
        self.assertEqual(nft.owner_id, self.test_user.id)
        self.assertEqual(nft.entity_type, 'chad')
        self.assertEqual(nft.entity_id, 1)
        self.assertFalse(nft.is_burned)
        
        # Check transaction
        transaction = Transaction.query.filter_by(transaction_hash='test_transaction_id').first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.user_id, self.test_user.id)
        self.assertEqual(transaction.transaction_type, 'mint')
        self.assertEqual(transaction.token_id, 'test_token_id')
    
    @patch('app.controllers.nft.burn_nft_on_chain')
    def test_burn_nft(self, mock_burn_nft_on_chain):
        """Test burning an NFT."""
        # Create an NFT
        nft = NFT(
            token_id='test_token_id',
            owner_id=self.test_user.id,
            entity_type='chad',
            entity_id=1,
            metadata_uri='ipfs://test',
            is_burned=False
        )
        db.session.add(nft)
        db.session.commit()
        
        # Mock the on-chain burning
        mock_burn_nft_on_chain.return_value = {
            'success': True,
            'transaction_id': 'test_burn_transaction_id',
            'block_number': 12345678
        }
        
        # Burn the NFT
        response = self.client.post('/api/burn-nft', json={
            'token_id': 'test_token_id'
        })
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Check database
        nft = NFT.query.filter_by(token_id='test_token_id').first()
        self.assertIsNotNone(nft)
        self.assertTrue(nft.is_burned)
        
        # Check transaction
        transaction = Transaction.query.filter_by(transaction_hash='test_burn_transaction_id').first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.user_id, self.test_user.id)
        self.assertEqual(transaction.transaction_type, 'burn')
        self.assertEqual(transaction.token_id, 'test_token_id')
    
    @patch('app.controllers.api.transfer_nft')
    def test_transfer_nft(self, mock_transfer_nft):
        """Test transferring an NFT."""
        # Create an NFT
        nft = NFT(
            token_id='test_token_id',
            owner_id=self.test_user.id,
            entity_type='chad',
            entity_id=1,
            metadata_uri='ipfs://test',
            is_burned=False
        )
        db.session.add(nft)
        db.session.commit()
        
        # Mock the on-chain transfer
        mock_transfer_nft.return_value = {
            'success': True,
            'transaction_id': 'test_transfer_transaction_id',
            'block_number': 12345678
        }
        
        # Transfer the NFT
        response = self.client.post('/api/transfer-nft', json={
            'token_id': 'test_token_id',
            'to_address': 'recipient_wallet_address'
        })
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Check database
        nft = NFT.query.filter_by(token_id='test_token_id').first()
        self.assertIsNotNone(nft)
        self.assertEqual(nft.owner_id, self.recipient_user.id)
        
        # Check transaction
        transaction = Transaction.query.filter_by(transaction_hash='test_transfer_transaction_id').first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.user_id, self.test_user.id)
        self.assertEqual(transaction.transaction_type, 'transfer')
        self.assertEqual(transaction.token_id, 'test_token_id')
        self.assertEqual(transaction.recipient_id, self.recipient_user.id)
    
    def test_get_nfts(self):
        """Test getting user's NFTs."""
        # Create some NFTs
        nft1 = NFT(
            token_id='test_token_id_1',
            owner_id=self.test_user.id,
            entity_type='chad',
            entity_id=1,
            metadata_uri='ipfs://test1',
            is_burned=False
        )
        nft2 = NFT(
            token_id='test_token_id_2',
            owner_id=self.test_user.id,
            entity_type='chad',
            entity_id=2,
            metadata_uri='ipfs://test2',
            is_burned=False
        )
        nft3 = NFT(
            token_id='test_token_id_3',
            owner_id=self.recipient_user.id,
            entity_type='chad',
            entity_id=3,
            metadata_uri='ipfs://test3',
            is_burned=False
        )
        db.session.add_all([nft1, nft2, nft3])
        db.session.commit()
        
        # Get user's NFTs
        response = self.client.get('/api/user-nfts')
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['nfts']), 2)
        
        # Check NFT data
        nft_ids = [nft['token_id'] for nft in data['nfts']]
        self.assertIn('test_token_id_1', nft_ids)
        self.assertIn('test_token_id_2', nft_ids)
        self.assertNotIn('test_token_id_3', nft_ids)
    
    def test_get_nft_metadata(self):
        """Test getting NFT metadata."""
        # Create an NFT
        nft = NFT(
            token_id='test_token_id',
            owner_id=self.test_user.id,
            entity_type='chad',
            entity_id=1,
            metadata_uri='ipfs://test',
            is_burned=False
        )
        db.session.add(nft)
        db.session.commit()
        
        # Mock metadata
        with patch('app.controllers.nft.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'name': 'Test NFT',
                'description': 'Test description',
                'image': 'https://test.com/image.png',
                'attributes': [
                    {'trait_type': 'Level', 'value': 10}
                ]
            }
            mock_get.return_value = mock_response
            
            # Get NFT metadata
            response = self.client.get(f'/api/nft-metadata/test_token_id')
            
            # Check response
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['metadata']['name'], 'Test NFT')
            self.assertEqual(data['metadata']['description'], 'Test description')

if __name__ == '__main__':
    unittest.main() 