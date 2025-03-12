"""
Transaction model for Chad Battles.
Handles transaction records for Chadcoin and NFT operations.
"""
from app.extensions import db
from datetime import datetime
import enum

class TransactionType(enum.Enum):
    """Enum for transaction types."""
    CHADCOIN_ADD = 'chadcoin_add'
    CHADCOIN_REMOVE = 'chadcoin_remove'
    CHADCOIN_TRANSFER = 'chadcoin_transfer'
    NFT_MINT = 'nft_mint'
    NFT_BURN = 'nft_burn'
    NFT_TRANSFER = 'nft_transfer'
    ITEM_PURCHASE = 'item_purchase'
    WAIFU_PURCHASE = 'waifu_purchase'
    BATTLE_REWARD = 'battle_reward'
    BATTLE_ENTRY = 'battle_entry'
    ELIXIR_PURCHASE = 'elixir_purchase'
    ELIXIR_USE = 'elixir_use'

class Transaction(db.Model):
    """Transaction model for storing transaction records."""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nft_id = db.Column(db.Integer, db.ForeignKey('nfts.id'), nullable=True)
    transaction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    
    # For transfers
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # For blockchain transactions
    transaction_hash = db.Column(db.String(255), nullable=True)
    block_number = db.Column(db.Integer, nullable=True)
    
    # Status
    status = db.Column(db.String(50), default='pending')  # pending, completed, failed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    from_user = db.relationship('User', foreign_keys=[from_user_id], backref='sent_transactions')
    to_user = db.relationship('User', foreign_keys=[to_user_id], backref='received_transactions')
    
    def __repr__(self):
        return f'<Transaction {self.id}: {self.transaction_type} {self.amount}>'
    
    def is_nft_transaction(self):
        """Check if this is an NFT-related transaction."""
        return self.transaction_type in [
            TransactionType.NFT_MINT.value,
            TransactionType.NFT_BURN.value,
            TransactionType.NFT_TRANSFER.value
        ]
    
    def is_chadcoin_transaction(self):
        """Check if this is a Chadcoin-related transaction."""
        return self.transaction_type in [
            TransactionType.CHADCOIN_ADD.value,
            TransactionType.CHADCOIN_REMOVE.value,
            TransactionType.CHADCOIN_TRANSFER.value
        ]
    
    def to_dict(self):
        """Convert transaction to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nft_id': self.nft_id,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'description': self.description,
            'from_user_id': self.from_user_id,
            'to_user_id': self.to_user_id,
            'transaction_hash': self.transaction_hash,
            'block_number': self.block_number,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def record_chadcoin_transaction(cls, user_id, amount, description, related_entity=None):
        """
        Record a Chadcoin transaction.
        
        Args:
            user_id: The ID of the user
            amount: The amount of Chadcoin (positive for earned, negative for spent)
            description: Description of the transaction
            related_entity: Optional tuple of (entity_type, entity_id) for related entity
        
        Returns:
            The created Transaction object
        """
        transaction = cls(
            user_id=user_id,
            transaction_type=TransactionType.CHADCOIN_ADD.value if amount > 0 else TransactionType.CHADCOIN_REMOVE.value,
            amount=abs(amount),  # Store as positive value
            description=description
        )
        
        # Add related entity if provided
        if related_entity:
            entity_type, entity_id = related_entity
            if entity_type == 'chad':
                transaction.chad_id = entity_id
            elif entity_type == 'waifu':
                transaction.waifu_id = entity_id
            elif entity_type == 'item':
                transaction.item_id = entity_id
            elif entity_type == 'nft':
                transaction.nft_id = entity_id
        
        db.session.add(transaction)
        db.session.commit()
        
        return transaction
    
    @classmethod
    def record_nft_transaction(cls, user_id, nft_id, transaction_type, amount=0, description=None, 
                              transaction_hash=None, block_number=None, status="completed"):
        """
        Record an NFT transaction.
        
        Args:
            user_id: The ID of the user
            nft_id: The ID of the NFT
            transaction_type: The type of transaction (mint, burn, transfer)
            amount: The amount of Chadcoin involved (if any)
            description: Description of the transaction
            transaction_hash: The blockchain transaction hash
            block_number: The blockchain block number
            status: The status of the transaction
        
        Returns:
            The created Transaction object
        """
        transaction = cls(
            user_id=user_id,
            nft_id=nft_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            transaction_hash=transaction_hash,
            block_number=block_number,
            status=status
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return transaction 