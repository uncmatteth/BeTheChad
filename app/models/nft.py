"""
NFT model for Chad Battles.
Handles NFT data storage and interactions.
"""
from app.extensions import db
from datetime import datetime
import enum
import json
from flask import url_for, current_app
import os

class NFTEntityType(enum.Enum):
    """Enum for NFT entity types."""
    CHAD = 'chad'
    WAIFU = 'waifu'
    ITEM = 'item'

class NFT(db.Model):
    """NFT model for storing NFT data."""
    __tablename__ = 'nfts'
    
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    
    # Blockchain data
    mint_transaction_hash = db.Column(db.String(255), nullable=True)
    mint_block_number = db.Column(db.Integer, nullable=True)
    burn_transaction_hash = db.Column(db.String(255), nullable=True)
    burn_block_number = db.Column(db.Integer, nullable=True)
    is_burned = db.Column(db.Boolean, default=False)
    
    # Metadata
    metadata_uri = db.Column(db.String(255), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('nfts', lazy=True))
    transactions = db.relationship('Transaction', backref='nft', lazy=True)
    
    def __repr__(self):
        return f'<NFT {self.token_id} ({self.entity_type} {self.entity_id})>'
    
    def get_entity(self):
        """Get the entity associated with this NFT."""
        if self.entity_type == NFTEntityType.CHAD.value:
            from app.models.chad import Chad
            return Chad.query.get(self.entity_id)
        elif self.entity_type == NFTEntityType.WAIFU.value:
            from app.models.waifu import Waifu
            return Waifu.query.get(self.entity_id)
        elif self.entity_type == NFTEntityType.ITEM.value:
            from app.models.item import Item
            return Item.query.get(self.entity_id)
        return None
    
    def generate_metadata(self):
        """Generate metadata for this NFT."""
        from app.utils.solana_api import generate_metadata
        
        entity = self.get_entity()
        if not entity:
            current_app.logger.error(f"Entity not found for NFT {self.token_id}")
            return None
        
        return generate_metadata(self.entity_type, entity, self.token_id)
    
    def calculate_burn_value(self):
        """Calculate the Chadcoin value for burning this NFT."""
        entity = self.get_entity()
        if not entity:
            return 0
        
        if self.entity_type == NFTEntityType.CHAD.value:
            # Chad value based on level
            base_value = 100  # Base value for a Chad
            level_bonus = entity.level * 10  # 10 Chadcoin per level
            return base_value + level_bonus
        
        elif self.entity_type == NFTEntityType.WAIFU.value:
            # Waifu value based on rarity
            rarity = entity.waifu_type.rarity.name.lower()
            if rarity == 'common':
                return 25
            elif rarity == 'rare':
                return 50
            elif rarity == 'epic':
                return 100
            elif rarity == 'legendary':
                return 200
            return 25  # Default for unknown rarity
        
        elif self.entity_type == NFTEntityType.ITEM.value:
            # Item value based on rarity
            rarity = entity.item_type.rarity.name.lower()
            if rarity == 'common':
                return 10
            elif rarity == 'rare':
                return 25
            elif rarity == 'epic':
                return 50
            elif rarity == 'legendary':
                return 100
            return 10  # Default for unknown rarity
        
        return 0
    
    def to_dict(self):
        """Convert NFT to dictionary."""
        return {
            'id': self.id,
            'token_id': self.token_id,
            'user_id': self.user_id,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'mint_transaction_hash': self.mint_transaction_hash,
            'mint_block_number': self.mint_block_number,
            'burn_transaction_hash': self.burn_transaction_hash,
            'burn_block_number': self.burn_block_number,
            'is_burned': self.is_burned,
            'metadata_uri': self.metadata_uri,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def save_metadata(self):
        """Save metadata to a file and update the metadata URI."""
        metadata = self.generate_metadata()
        if not metadata:
            return False
        
        # Ensure the metadata directory exists
        metadata_dir = os.path.join(os.environ.get('METADATA_DIR', 'metadata'), self.entity_type)
        os.makedirs(metadata_dir, exist_ok=True)
        
        # Save the metadata to a file
        metadata_path = os.path.join(metadata_dir, f"{self.token_id}.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Update the metadata URI
        self.metadata_uri = f"/metadata/{self.entity_type}/{self.token_id}.json"
        db.session.commit()
        
        return True
    
    @classmethod
    def get_user_nfts(cls, user_id):
        """Get all NFTs owned by a user."""
        return cls.query.filter_by(user_id=user_id, is_burned=False).all()
    
    @classmethod
    def get_by_token_id(cls, token_id):
        """Get an NFT by its token ID."""
        return cls.query.filter_by(token_id=token_id).first() 