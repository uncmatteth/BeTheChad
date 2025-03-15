"""
Waifu model for Chad Battles.
"""
from app.extensions import db
from datetime import datetime
import uuid

class WaifuRarity(db.Model):
    """Waifu rarity model for different rarity levels."""
    __tablename__ = 'waifu_rarities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    drop_rate = db.Column(db.Float, default=0.0)
    min_stat_bonus = db.Column(db.Integer, default=1)
    max_stat_bonus = db.Column(db.Integer, default=5)
    
    # Relationships
    waifu_types = db.relationship('WaifuType', backref='rarity', lazy='dynamic')
    
    def __repr__(self):
        return f'<WaifuRarity {self.name}>'

class WaifuType(db.Model):
    """Waifu type model for different waifu types."""
    __tablename__ = 'waifu_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    rarity_id = db.Column(db.Integer, db.ForeignKey('waifu_rarities.id'), nullable=False)
    base_clout_bonus = db.Column(db.Integer, default=0)
    base_roast_bonus = db.Column(db.Integer, default=0)
    base_cringe_resistance_bonus = db.Column(db.Integer, default=0)
    base_drip_bonus = db.Column(db.Integer, default=0)
    
    # Relationships
    waifus = db.relationship('Waifu', backref='waifu_type', lazy='dynamic')
    
    def __repr__(self):
        return f'<WaifuType {self.name} ({self.rarity.name})>'

class Waifu(db.Model):
    """
    Waifu model for tracking collected waifus
    """
    __tablename__ = 'waifus'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    rarity = db.Column(db.String(50), nullable=False, default='common')
    type = db.Column(db.String(50), nullable=False, default='standard')
    waifu_type_id = db.Column(db.Integer, db.ForeignKey('waifu_types.id'), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    power = db.Column(db.Integer, nullable=False, default=0)
    intelligence = db.Column(db.Integer, nullable=False, default=0)
    charisma = db.Column(db.Integer, nullable=False, default=0)
    luck = db.Column(db.Integer, nullable=False, default=0)
    
    # Ownership tracking
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('chads.id'), nullable=True)
    acquired_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('waifus', lazy=True))
    owner = db.relationship('Chad', foreign_keys=[owner_id], backref='waifus')
    
    def __repr__(self):
        return f'<Waifu {self.id}: {self.name} ({self.rarity})>'
    
    @classmethod
    def get_user_waifus(cls, user_id):
        """Get all waifus for a user"""
        return cls.query.filter(cls.owner_id == user_id).all()
    
    @classmethod
    def get_collector_stats(cls, limit=10):
        """
        Get top collectors' stats for the leaderboard
        
        Returns:
            list: List of tuples (chad_id, username, class_name, waifu_count, rare_count)
        """
        from app.models.chad import Chad
        from app.models.user import User
        from sqlalchemy import func, case
        
        try:
            # Get stats from database
            query = db.session.query(
                Chad.id,
                User.username,
                Chad.chad_class,
                func.count(cls.id).label('waifu_count'),
                func.sum(case([(cls.rarity.in_(['rare', 'legendary', 'mythic']), 1)], else_=0)).label('rare_count')
            ).join(
                User, Chad.id == User.chad_id
            ).join(
                cls, cls.owner_id == Chad.id
            ).group_by(
                Chad.id, User.username, Chad.chad_class
            ).order_by(
                func.count(cls.id).desc(), 
                func.sum(case([(cls.rarity.in_(['rare', 'legendary', 'mythic']), 1)], else_=0)).desc()
            ).limit(limit)
            
            result = query.all()
            return result
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error getting collector stats: {str(e)}")
            return []
    
    def add_xp(self, amount):
        """Add XP to the Waifu and level up if necessary."""
        if amount <= 0:
            return False
        
        self.xp += amount
        
        # Check for level up
        xp_needed = self.get_xp_for_next_level()
        while self.xp >= xp_needed:
            self.level_up()
            xp_needed = self.get_xp_for_next_level()
        
        db.session.commit()
        return True
    
    def level_up(self):
        """Level up the Waifu and increase stats."""
        self.level += 1
        
        # Increase stats based on waifu type
        self.clout_bonus += 1 + self.waifu_type.base_clout_bonus // 10
        self.roast_bonus += 1 + self.waifu_type.base_roast_bonus // 10
        self.cringe_resistance_bonus += 1 + self.waifu_type.base_cringe_resistance_bonus // 10
        self.drip_bonus += 1 + self.waifu_type.base_drip_bonus // 10
        
        return True
    
    def get_xp_for_next_level(self):
        """Calculate XP needed for the next level."""
        return 80 * self.level + 40 * (self.level - 1) ** 2
    
    def equip(self, chad_id):
        """Equip the Waifu to a Chad."""
        # Unequip any currently equipped waifus of the same type
        currently_equipped = Waifu.query.filter_by(
            chad_id=chad_id,
            is_equipped=True,
            waifu_type_id=self.waifu_type_id
        ).all()
        
        for waifu in currently_equipped:
            waifu.is_equipped = False
        
        # Equip this waifu
        self.chad_id = chad_id
        self.is_equipped = True
        db.session.commit()
        
        return True
    
    def unequip(self):
        """Unequip the Waifu."""
        self.chad_id = None
        self.is_equipped = False
        db.session.commit()
        
        return True 