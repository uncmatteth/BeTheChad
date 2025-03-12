"""
Tests for Wallet functionality in Chad Battles.
"""
import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.nft import NFT, NFTEntityType
from app.models.transaction import Transaction, TransactionType
import json
import uuid
from flask import url_for

class WalletTestCase(unittest.TestCase):
    """Test case for Wallet functionality."""
    
    def setUp(self):
        """Set up the test environment."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        # Create test database
        db.create_all()
        
        # Create test user
        self.test_user = User(
            username='test_user',
            email='test@example.com'
        )
        self.test_user.set_password('password')
        db.session.add(self.test_user)
        db.session.commit()
        
        # Login test user
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.test_user.id
    
    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    @patch('app.controllers.wallet.verify_wallet_ownership')
    def test_wallet_connect(self, mock_verify_ownership):
        """Test connecting a wallet."""
        # Mock the verification
        mock_verify_ownership.return_value = {
            'success': True,
            'message': 'Wallet verified successfully'
        }
        
        # Connect wallet
        response = self.client.post('/api/connect-wallet', json={
            'wallet_address': 'test_wallet_address',
            'wallet_type': 'phantom',
            'signature': 'test_signature',
            'message': 'test_message'
        })
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Check database
        user = User.query.get(self.test_user.id)
        self.assertEqual(user.wallet_address, 'test_wallet_address')
        self.assertEqual(user.wallet_type, 'phantom')
    
    def test_wallet_disconnect(self):
        """Test disconnecting a wallet."""
        # Set up a connected wallet
        self.test_user.wallet_address = 'test_wallet_address'
        self.test_user.wallet_type = 'phantom'
        db.session.commit()
        
        # Disconnect wallet
        response = self.client.post('/api/disconnect-wallet')
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Check database
        user = User.query.get(self.test_user.id)
        self.assertIsNone(user.wallet_address)
        self.assertIsNone(user.wallet_type)
    
    @patch('app.controllers.wallet.get_wallet_balance')
    def test_wallet_status(self, mock_get_balance):
        """Test getting wallet status."""
        # Set up a connected wallet
        self.test_user.wallet_address = 'test_wallet_address'
        self.test_user.wallet_type = 'phantom'
        db.session.commit()
        
        # Mock the balance check
        mock_get_balance.return_value = {
            'success': True,
            'balance': 10.5
        }
        
        # Get wallet status
        response = self.client.get('/api/status')
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['is_connected'])
        self.assertEqual(data['wallet_address'], 'test_wallet_address')
        self.assertEqual(data['wallet_type'], 'phantom')
        self.assertEqual(data['balance'], 10.5)
    
    def test_wallet_status_not_connected(self):
        """Test getting wallet status when not connected."""
        # Get wallet status
        response = self.client.get('/api/status')
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertFalse(data['is_connected'])
    
    def test_wallet_transactions(self):
        """Test getting wallet transactions."""
        # Set up a connected wallet
        self.test_user.wallet_address = 'test_wallet_address'
        self.test_user.wallet_type = 'phantom'
        db.session.commit()
        
        # Create some transactions
        transaction1 = Transaction(
            user_id=self.test_user.id,
            transaction_hash='tx_hash_1',
            transaction_type='mint',
            token_id='token_1',
            timestamp='2023-01-01T12:00:00Z',
            block_number=12345678
        )
        transaction2 = Transaction(
            user_id=self.test_user.id,
            transaction_hash='tx_hash_2',
            transaction_type='burn',
            token_id='token_2',
            timestamp='2023-01-02T12:00:00Z',
            block_number=12345679
        )
        db.session.add_all([transaction1, transaction2])
        db.session.commit()
        
        # Get transactions
        response = self.client.get('/api/transactions')
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['transactions']), 2)
        
        # Check transaction data
        tx_hashes = [tx['transaction_hash'] for tx in data['transactions']]
        self.assertIn('tx_hash_1', tx_hashes)
        self.assertIn('tx_hash_2', tx_hashes)
    
    def test_wallet_no_transactions(self):
        """Test getting wallet transactions when there are none."""
        # Set up a connected wallet
        self.test_user.wallet_address = 'test_wallet_address'
        self.test_user.wallet_type = 'phantom'
        db.session.commit()
        
        # Get transactions
        response = self.client.get('/api/transactions')
        
        # Check response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['transactions']), 0)
    
    def test_wallet_templates(self):
        """Test accessing wallet templates."""
        # Test wallet index template
        response = self.client.get('/wallet')
        self.assertEqual(response.status_code, 200)
        
        # Test wallet connect template
        response = self.client.get('/wallet/connect')
        self.assertEqual(response.status_code, 200)
        
        # Test wallet transactions template
        response = self.client.get('/wallet/transactions')
        self.assertEqual(response.status_code, 200)
    
    @patch('app.controllers.wallet.verify_wallet_ownership')
    def test_invalid_wallet_connection(self, mock_verify_ownership):
        """Test connecting an invalid wallet."""
        # Mock the verification to fail
        mock_verify_ownership.return_value = {
            'success': False,
            'message': 'Invalid signature'
        }
        
        # Connect wallet
        response = self.client.post('/api/connect-wallet', json={
            'wallet_address': 'test_wallet_address',
            'wallet_type': 'phantom',
            'signature': 'invalid_signature',
            'message': 'test_message'
        })
        
        # Check response
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid signature')
        
        # Check database - wallet should not be connected
        user = User.query.get(self.test_user.id)
        self.assertIsNone(user.wallet_address)
        self.assertIsNone(user.wallet_type)
    
    def test_missing_wallet_connection_params(self):
        """Test connecting a wallet with missing parameters."""
        # Connect wallet with missing wallet_type
        response = self.client.post('/api/connect-wallet', json={
            'wallet_address': 'test_wallet_address',
            'signature': 'test_signature',
            'message': 'test_message'
        })
        
        # Check response
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('wallet_type', data['message'].lower())
    
    def test_mint_nft(self):
        """Test minting an NFT."""
        # First connect a wallet and create test data
        wallet_address = f'testwallet{uuid.uuid4().hex[:10]}'
        self.test_user.wallet_address = wallet_address
        self.test_user.wallet_type = 'phantom'
        
        # Create test Chad for the user
        from app.models.chad import Chad, ChadClass
        chad_class = ChadClass(name='TestClass', description='Test class')
        db.session.add(chad_class)
        db.session.commit()
        
        chad = Chad(user_id=self.test_user.id, name='TestChad', class_id=chad_class.id)
        db.session.add(chad)
        db.session.commit()
        
        # Mint NFT
        response = self.client.post('/api/mint-nft', json={
            'entity_type': NFTEntityType.CHAD.value,
            'entity_id': chad.id
        })
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        
        # Check NFT in database
        nft = NFT.query.filter_by(user_id=self.test_user.id, entity_type=NFTEntityType.CHAD.value).first()
        self.assertIsNotNone(nft)
        self.assertEqual(nft.entity_id, chad.id)
        
        # Check transaction in database
        transaction = Transaction.query.filter_by(
            user_id=self.test_user.id,
            transaction_type=TransactionType.NFT_MINT.value
        ).first()
        self.assertIsNotNone(transaction)
    
    def test_burn_nft(self):
        """Test burning an NFT."""
        # First connect a wallet and create test NFT
        wallet_address = f'testwallet{uuid.uuid4().hex[:10]}'
        self.test_user.wallet_address = wallet_address
        self.test_user.wallet_type = 'phantom'
        
        # Create test NFT
        token_id = f'token{uuid.uuid4().hex[:10]}'
        nft = NFT(
            token_id=token_id,
            user_id=self.test_user.id,
            entity_type=NFTEntityType.CHAD.value,
            entity_id=1,  # Dummy ID
            is_burned=False
        )
        db.session.add(nft)
        db.session.commit()
        
        # Override the calculate_burn_value method for testing
        def mock_calculate_burn_value(self):
            return 50
        
        NFT.calculate_burn_value = mock_calculate_burn_value
        
        # Burn NFT
        response = self.client.post('/api/burn-nft', json={
            'token_id': token_id
        })
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        
        # Check NFT in database
        nft = NFT.query.filter_by(token_id=token_id).first()
        self.assertTrue(nft.is_burned)
        
        # Check user's Chadcoin balance
        user = User.query.filter_by(id=self.test_user.id).first()
        self.assertEqual(user.chadcoin_balance, 150)  # 100 (initial) + 50 (burn reward)
        
        # Check transaction in database
        transaction = Transaction.query.filter_by(
            user_id=self.test_user.id,
            transaction_type=TransactionType.NFT_BURN.value
        ).first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.amount, 50)
    
    def test_transfer_nft(self):
        """Test transferring an NFT."""
        # Create another user
        recipient = User(
            username='recipient',
            email='recipient@example.com',
            wallet_address=f'recipientwallet{uuid.uuid4().hex[:10]}'
        )
        db.session.add(recipient)
        db.session.commit()
        
        # First connect a wallet and create test NFT
        wallet_address = f'testwallet{uuid.uuid4().hex[:10]}'
        self.test_user.wallet_address = wallet_address
        self.test_user.wallet_type = 'phantom'
        
        # Create test NFT
        token_id = f'token{uuid.uuid4().hex[:10]}'
        nft = NFT(
            token_id=token_id,
            user_id=self.test_user.id,
            entity_type=NFTEntityType.CHAD.value,
            entity_id=1,  # Dummy ID
            is_burned=False
        )
        db.session.add(nft)
        db.session.commit()
        
        # Transfer NFT
        response = self.client.post('/api/transfer-nft', json={
            'token_id': token_id,
            'to_address': recipient.wallet_address
        })
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        
        # Check NFT in database
        nft = NFT.query.filter_by(token_id=token_id).first()
        self.assertEqual(nft.user_id, recipient.id)
        
        # Check transaction in database
        transaction = Transaction.query.filter_by(
            user_id=self.test_user.id,
            transaction_type=TransactionType.NFT_TRANSFER.value
        ).first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.from_user_id, self.test_user.id)
        self.assertEqual(transaction.to_user_id, recipient.id)

if __name__ == '__main__':
    unittest.main() 