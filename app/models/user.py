"""
User model for Chad Battles.
Handles user authentication and profile data.
"""
from app.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.models.transaction import Transaction, TransactionType
from sqlalchemy import Index

class User(UserMixin, db.Model):
    """User model for storing user account data."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # Profile
    display_name = db.Column(db.String(64))
    bio = db.Column(db.String(500))
    avatar_url = db.Column(db.String(255))
    
    # Game currency
    chadcoin_balance = db.Column(db.Integer, default=100)
    
    # Wallet integration
    wallet_address = db.Column(db.String(255), unique=True, nullable=True)
    wallet_type = db.Column(db.String(50), nullable=True)  # 'phantom', 'solflare', etc.
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Twitter/X info
    x_id = db.Column(db.String(64), unique=True, nullable=True)
    x_username = db.Column(db.String(64), unique=True, nullable=True)
    x_displayname = db.Column(db.String(64), nullable=True)
    x_profile_image = db.Column(db.String(255), nullable=True)
    
    # Admin flag
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    chad = db.relationship('Chad', backref='user', uselist=False, lazy=True)
    items = db.relationship('Item', backref='user', lazy=True)
    inventory = db.relationship('Inventory', back_populates='user', uselist=False, lazy=True)
    
    # Fix the ambiguous relationships by specifying foreign_keys
    transactions = db.relationship('Transaction', 
                                  foreign_keys='Transaction.user_id',
                                  backref='user', 
                                  lazy=True)
    
    # Indexes for efficient queries
    __table_args__ = (
        Index('idx_user_username', username),
        Index('idx_user_email', email),
        Index('idx_user_x_id', 'x_id'),
        Index('idx_user_wallet', wallet_address),
        Index('idx_user_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Set the user's password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def add_chadcoin(self, amount):
        """Add Chadcoin to the user's balance and record the transaction."""
        if amount <= 0:
            return False
        
        self.chadcoin_balance += amount
        
        # Record transaction
        transaction = Transaction(
            user_id=self.id,
            transaction_type=TransactionType.CHADCOIN_ADD.value,
            amount=amount,
            description=f"Added {amount} Chadcoin to balance",
            status="completed"
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return True
    
    def remove_chadcoin(self, amount, description="Spent Chadcoin"):
        """Remove Chadcoin from the user's balance and record the transaction."""
        if amount <= 0 or self.chadcoin_balance < amount:
            return False
        
        self.chadcoin_balance -= amount
        
        # Record transaction
        transaction = Transaction(
            user_id=self.id,
            transaction_type=TransactionType.CHADCOIN_REMOVE.value,
            amount=amount,
            description=description,
            status="completed"
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return True
    
    def get_transaction_history(self, limit=20):
        """Get the user's transaction history."""
        return Transaction.query.filter_by(user_id=self.id).order_by(Transaction.created_at.desc()).limit(limit).all()
    
    def get_nft_count(self):
        """Get the count of NFTs owned by the user."""
        from app.models.nft import NFT
        return NFT.query.filter_by(user_id=self.id, is_burned=False).count()
    
    def has_wallet_connected(self):
        """Check if the user has a wallet connected."""
        return bool(self.wallet_address)
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'display_name': self.display_name,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'chadcoin_balance': self.chadcoin_balance,
            'wallet_address': self.wallet_address,
            'wallet_type': self.wallet_type,
            'has_chad': bool(self.chad),
            'item_count': len(self.items),
            'nft_count': self.get_nft_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID."""
    return User.query.get(int(user_id)) 