import os
import json
import unittest
import tempfile
from unittest.mock import patch, MagicMock
from datetime import datetime

from app import create_app, db
from app.models.user import User
from app.models.chad import Chad, ChadClass
from app.models.waifu import Waifu, WaifuType
from app.models.item import Item, ItemType
from app.models.nft import NFT
from app.models.transaction import Transaction
from app.models.rarity import Rarity
from app.utils.nft_helpers import (
    ensure_metadata_dirs, 
    create_metadata_file, 
    create_chad_metadata, 
    create_waifu_metadata, 
    create_item_metadata,
    get_nft_value
)


class NFTSystemTest(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        # Create a test app with a test database
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create a test client
        self.client = self.app.test_client(use_cookies=True)
        
        # Create all tables
        db.create_all()
        
        # Create a temporary directory for static files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app.static_folder = self.temp_dir.name
        
        # Set up test data
        self._create_test_data()
    
    def tearDown(self):
        """Clean up after test."""
        # Clean up database
        db.session.remove()
        db.drop_all()
        
        # Clean up temporary directory
        self.temp_dir.cleanup()
        
        # Remove app context
        self.app_context.pop()
    
    def _create_test_data(self):
        """Create test data for the tests."""
        # Create rarities
        rarities = {
            'common': Rarity(name='Common', value=1),
            'rare': Rarity(name='Rare', value=2),
            'epic': Rarity(name='Epic', value=3),
            'legendary': Rarity(name='Legendary', value=4)
        }
        for rarity in rarities.values():
            db.session.add(rarity)
        
        # Create chad classes
        chad_classes = {
            'sigma': ChadClass(name='Sigma', description='Lone wolf'),
            'gigachad': ChadClass(name='Gigachad', description='Ultimate chad'),
            'neet': ChadClass(name='NEET', description='Not in Education, Employment or Training')
        }
        for chad_class in chad_classes.values():
            db.session.add(chad_class)
        
        # Create waifu types
        waifu_types = {
            'catgirl': WaifuType(
                name='Catgirl', 
                description='Cute girl with cat ears', 
                rarity=rarities['common'],
                base_clout=10,
                base_roast_level=5,
                base_cringe_resistance=15,
                base_drip_factor=10
            ),
            'goth': WaifuType(
                name='Goth', 
                description='Dark and mysterious', 
                rarity=rarities['rare'],
                base_clout=15,
                base_roast_level=20,
                base_cringe_resistance=10,
                base_drip_factor=15
            ),
            'gamer': WaifuType(
                name='Gamer', 
                description='Pro gamer girl', 
                rarity=rarities['epic'],
                base_clout=20,
                base_roast_level=15,
                base_cringe_resistance=20,
                base_drip_factor=5
            )
        }
        for waifu_type in waifu_types.values():
            db.session.add(waifu_type)
        
        # Create item types
        item_types = {
            'fedora': ItemType(
                name='Fedora', 
                description='A classy hat', 
                rarity=rarities['common'],
                slot='head',
                base_clout_bonus=5,
                base_roast_bonus=0,
                base_cringe_resistance_bonus=0,
                base_drip_bonus=5
            ),
            'gaming_headset': ItemType(
                name='Gaming Headset', 
                description='For pro gamers', 
                rarity=rarities['rare'],
                slot='head',
                base_clout_bonus=10,
                base_roast_bonus=5,
                base_cringe_resistance_bonus=0,
                base_drip_bonus=5
            ),
            'designer_shirt': ItemType(
                name='Designer Shirt', 
                description='Expensive fashion', 
                rarity=rarities['epic'],
                slot='body',
                base_clout_bonus=15,
                base_roast_bonus=0,
                base_cringe_resistance_bonus=5,
                base_drip_bonus=20
            )
        }
        for item_type in item_types.values():
            db.session.add(item_type)
        
        db.session.commit()
        
        # Create users
        self.test_user = User(
            username='testuser',
            email='test@example.com',
            password='password',
            wallet_address='test_wallet_address',
            wallet_type='phantom'
        )
        db.session.add(self.test_user)
        db.session.commit()
        
        # Create a chad for the test user
        self.test_chad = Chad(
            user=self.test_user,
            name='TestChad',
            avatar='testchad.png',
            chad_class=chad_classes['sigma'],
            level=5,
            xp=500,
            is_active=True
        )
        db.session.add(self.test_chad)
        
        # Create a waifu for the test user
        self.test_waifu = Waifu(
            user=self.test_user,
            waifu_type=waifu_types['catgirl'],
            is_equipped=True,
            clout=waifu_types['catgirl'].base_clout,
            roast_level=waifu_types['catgirl'].base_roast_level,
            cringe_resistance=waifu_types['catgirl'].base_cringe_resistance,
            drip_factor=waifu_types['catgirl'].base_drip_factor
        )
        db.session.add(self.test_waifu)
        
        # Create an item for the test user
        self.test_item = Item(
            user=self.test_user,
            item_type=item_types['fedora'],
            is_equipped=False,
            clout_bonus=item_types['fedora'].base_clout_bonus,
            roast_bonus=item_types['fedora'].base_roast_bonus,
            cringe_resistance_bonus=item_types['fedora'].base_cringe_resistance_bonus,
            drip_bonus=item_types['fedora'].base_drip_bonus
        )
        db.session.add(self.test_item)
        
        db.session.commit()
    
    def test_metadata_directory_creation(self):
        """Test that metadata directories are created properly."""
        # Ensure metadata directories exist
        result = ensure_metadata_dirs()
        self.assertTrue(result)
        
        # Check if the directories were created
        base_dir = os.path.join(self.app.static_folder, 'metadata')
        self.assertTrue(os.path.exists(base_dir))
        
        for entity_type in ['chad', 'waifu', 'item']:
            entity_dir = os.path.join(base_dir, entity_type)
            self.assertTrue(os.path.exists(entity_dir))
    
    def test_metadata_creation(self):
        """Test creation of metadata files."""
        # Create test metadata
        test_metadata = {
            'name': 'Test NFT',
            'description': 'A test NFT',
            'image': '/static/img/test.png',
            'attributes': [
                {
                    'trait_type': 'Test Trait',
                    'value': 'Test Value'
                }
            ]
        }
        
        # Ensure directories exist
        ensure_metadata_dirs()
        
        # Create metadata file
        success, uri, error = create_metadata_file('chad', 1, test_metadata, 'test_token_id')
        
        # Check result
        self.assertTrue(success)
        self.assertIsNotNone(uri)
        self.assertIsNone(error)
        
        # Check if file was created
        expected_path = os.path.join(self.app.static_folder, 'metadata', 'chad', 'test_token_id.json')
        self.assertTrue(os.path.exists(expected_path))
        
        # Check file contents
        with open(expected_path, 'r') as f:
            saved_metadata = json.load(f)
        
        self.assertEqual(saved_metadata['name'], test_metadata['name'])
        self.assertEqual(saved_metadata['description'], test_metadata['description'])
        self.assertEqual(saved_metadata['image'], test_metadata['image'])
        self.assertEqual(saved_metadata['attributes'], test_metadata['attributes'])
        self.assertIn('version', saved_metadata)
        self.assertIn('created_at', saved_metadata)
    
    def test_chad_metadata_generation(self):
        """Test generation of Chad metadata."""
        # Generate Chad metadata
        metadata = create_chad_metadata(self.test_chad)
        
        # Check basic metadata structure
        self.assertEqual(metadata['name'], self.test_chad.name)
        self.assertIn('description', metadata)
        self.assertIn('image', metadata)
        self.assertIn('attributes', metadata)
        
        # Check attributes
        attribute_types = [attr['trait_type'] for attr in metadata['attributes']]
        self.assertIn('Class', attribute_types)
        self.assertIn('Level', attribute_types)
        self.assertIn('Clout', attribute_types)
        self.assertIn('Roast Level', attribute_types)
        self.assertIn('Cringe Resistance', attribute_types)
        self.assertIn('Drip Factor', attribute_types)
    
    def test_waifu_metadata_generation(self):
        """Test generation of Waifu metadata."""
        # Generate Waifu metadata
        metadata = create_waifu_metadata(self.test_waifu)
        
        # Check basic metadata structure
        self.assertEqual(metadata['name'], self.test_waifu.waifu_type.name)
        self.assertIn('description', metadata)
        self.assertIn('image', metadata)
        self.assertIn('attributes', metadata)
        
        # Check attributes
        attribute_types = [attr['trait_type'] for attr in metadata['attributes']]
        self.assertIn('Type', attribute_types)
        self.assertIn('Rarity', attribute_types)
        self.assertIn('Clout', attribute_types)
        self.assertIn('Roast Level', attribute_types)
        self.assertIn('Cringe Resistance', attribute_types)
        self.assertIn('Drip Factor', attribute_types)
    
    def test_item_metadata_generation(self):
        """Test generation of Item metadata."""
        # Generate Item metadata
        metadata = create_item_metadata(self.test_item)
        
        # Check basic metadata structure
        self.assertEqual(metadata['name'], self.test_item.item_type.name)
        self.assertIn('description', metadata)
        self.assertIn('image', metadata)
        self.assertIn('attributes', metadata)
        
        # Check attributes
        attribute_types = [attr['trait_type'] for attr in metadata['attributes']]
        self.assertIn('Type', attribute_types)
        self.assertIn('Rarity', attribute_types)
        self.assertIn('Slot', attribute_types)
        
        # Check stat bonuses
        if self.test_item.clout_bonus:
            self.assertIn('Clout Bonus', attribute_types)
        if self.test_item.drip_bonus:
            self.assertIn('Drip Bonus', attribute_types)
    
    def test_nft_minting(self):
        """Test minting of NFTs."""
        # Login as test user
        with self.client as client:
            with client.session_transaction() as session:
                session['user_id'] = self.test_user.id
            
            # Test minting a Chad NFT
            response = client.post('/api/mint_nft', json={
                'entity_type': 'chad',
                'entity_id': self.test_chad.id
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertIn('nft_id', data)
            
            # Check that NFT was recorded in database
            chad_nft = NFT.query.filter_by(
                entity_type='chad',
                entity_id=self.test_chad.id
            ).first()
            
            self.assertIsNotNone(chad_nft)
            self.assertEqual(chad_nft.owner_id, self.test_user.id)
            self.assertIsNotNone(chad_nft.token_id)
            self.assertIsNotNone(chad_nft.metadata_uri)
            
            # Check that transaction was recorded
            transaction = Transaction.query.filter_by(
                user_id=self.test_user.id,
                transaction_type='mint',
                nft_id=chad_nft.id
            ).first()
            
            self.assertIsNotNone(transaction)
    
    def test_nft_value_calculation(self):
        """Test calculation of NFT value for burning."""
        # Create test NFTs
        chad_nft = NFT(
            owner=self.test_user,
            entity_type='chad',
            entity_id=self.test_chad.id,
            token_id='test_chad_token_id',
            metadata_uri='/static/metadata/chad/test_chad_token_id.json',
            is_burned=False
        )
        db.session.add(chad_nft)
        
        waifu_nft = NFT(
            owner=self.test_user,
            entity_type='waifu',
            entity_id=self.test_waifu.id,
            token_id='test_waifu_token_id',
            metadata_uri='/static/metadata/waifu/test_waifu_token_id.json',
            is_burned=False
        )
        db.session.add(waifu_nft)
        
        item_nft = NFT(
            owner=self.test_user,
            entity_type='item',
            entity_id=self.test_item.id,
            token_id='test_item_token_id',
            metadata_uri='/static/metadata/item/test_item_token_id.json',
            is_burned=False
        )
        db.session.add(item_nft)
        
        db.session.commit()
        
        # Test value calculation
        chad_value = get_nft_value(chad_nft)
        waifu_value = get_nft_value(waifu_nft)
        item_value = get_nft_value(item_nft)
        
        # Check values
        # Chad value: 100 base * level 5 = 500
        self.assertEqual(chad_value, 500)
        
        # Waifu value: 50 base * Common (1x) = 50
        self.assertEqual(waifu_value, 50)
        
        # Item value: 25 base * Common (1x) = 25
        self.assertEqual(item_value, 25)
    
    @patch('app.models.nft.NFT.burn_on_chain')
    def test_nft_burning(self, mock_burn_on_chain):
        """Test burning of NFTs."""
        # Setup mock
        mock_burn_on_chain.return_value = True, 'test_burn_transaction_id', None
        
        # Create a test NFT
        test_nft = NFT(
            owner=self.test_user,
            entity_type='chad',
            entity_id=self.test_chad.id,
            token_id='test_token_id',
            metadata_uri='/static/metadata/chad/test_token_id.json',
            is_burned=False
        )
        db.session.add(test_nft)
        db.session.commit()
        
        # Login as test user
        with self.client as client:
            with client.session_transaction() as session:
                session['user_id'] = self.test_user.id
            
            # Test burning the NFT
            response = client.post(f'/api/burn_nft/{test_nft.id}')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            
            # Check that NFT was marked as burned
            burned_nft = NFT.query.get(test_nft.id)
            self.assertTrue(burned_nft.is_burned)
            self.assertIsNotNone(burned_nft.burned_at)
            self.assertIsNotNone(burned_nft.burn_transaction_id)
            
            # Check that a transaction was recorded
            transaction = Transaction.query.filter_by(
                user_id=self.test_user.id,
                transaction_type='burn',
                nft_id=test_nft.id
            ).first()
            
            self.assertIsNotNone(transaction)
            
            # Check that the user received Chadcoin
            self.assertGreater(self.test_user.chadcoin_balance, 0)
    
    def test_nft_metadata_loading(self):
        """Test loading of NFT metadata."""
        # Create test metadata
        test_metadata = {
            'name': 'Test NFT',
            'description': 'A test NFT',
            'image': '/static/img/test.png',
            'attributes': [
                {
                    'trait_type': 'Test Trait',
                    'value': 'Test Value'
                }
            ]
        }
        
        # Ensure directories exist
        ensure_metadata_dirs()
        
        # Create metadata file
        metadata_dir = os.path.join(self.app.static_folder, 'metadata', 'chad')
        os.makedirs(metadata_dir, exist_ok=True)
        
        metadata_path = os.path.join(metadata_dir, 'test_token_id.json')
        with open(metadata_path, 'w') as f:
            json.dump(test_metadata, f)
        
        # Create an NFT
        test_nft = NFT(
            owner=self.test_user,
            entity_type='chad',
            entity_id=self.test_chad.id,
            token_id='test_token_id',
            metadata_uri='/static/metadata/chad/test_token_id.json',
            is_burned=False
        )
        db.session.add(test_nft)
        db.session.commit()
        
        # Login as test user
        with self.client as client:
            with client.session_transaction() as session:
                session['user_id'] = self.test_user.id
            
            # Test viewing the NFT
            response = client.get(f'/nft/{test_nft.id}')
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(test_metadata['name'].encode(), response.data)
            self.assertIn(test_metadata['description'].encode(), response.data)


if __name__ == '__main__':
    unittest.main() 