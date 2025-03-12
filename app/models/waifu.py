"""
Waifu model for Chad Battles.
"""
from app.extensions import db
from datetime import datetime

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
    """Waifu model for companion characters."""
    __tablename__ = 'waifus'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chad_id = db.Column(db.Integer, db.ForeignKey('chads.id'), nullable=True)
    waifu_type_id = db.Column(db.Integer, db.ForeignKey('waifu_types.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    is_equipped = db.Column(db.Boolean, default=False)
    
    # Stats
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    clout_bonus = db.Column(db.Integer, default=0)
    roast_bonus = db.Column(db.Integer, default=0)
    cringe_resistance_bonus = db.Column(db.Integer, default=0)
    drip_bonus = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Waifu {self.name} (Level {self.level})>'
    
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