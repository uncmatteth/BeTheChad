"""
Chad model for Chad Battles.
"""
from app.extensions import db
from datetime import datetime

class ChadClass(db.Model):
    """Chad class model for different character types."""
    __tablename__ = 'chad_classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    base_clout_bonus = db.Column(db.Integer, default=0)
    base_roast_bonus = db.Column(db.Integer, default=0)
    base_cringe_resistance_bonus = db.Column(db.Integer, default=0)
    base_drip_bonus = db.Column(db.Integer, default=0)
    
    # Relationships
    chads = db.relationship('Chad', backref='chad_class', lazy='dynamic')
    
    def __repr__(self):
        return f'<ChadClass {self.name}>'

class Chad(db.Model):
    """Chad character model for player characters."""
    __tablename__ = 'chads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('chad_classes.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    avatar_locked = db.Column(db.Boolean, default=False)
    
    # Stats
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    clout = db.Column(db.Integer, default=10)
    roast_level = db.Column(db.Integer, default=10)
    cringe_resistance = db.Column(db.Integer, default=10)
    drip_factor = db.Column(db.Integer, default=10)
    
    # Battle stats
    battles_won = db.Column(db.Integer, default=0)
    battles_lost = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Chad {self.name} (Level {self.level})>'
    
    def add_xp(self, amount):
        """Add XP to the Chad and level up if necessary."""
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
        """Level up the Chad and increase stats."""
        self.level += 1
        
        # Increase stats based on class
        self.clout += 2 + self.chad_class.base_clout_bonus // 5
        self.roast_level += 2 + self.chad_class.base_roast_bonus // 5
        self.cringe_resistance += 2 + self.chad_class.base_cringe_resistance_bonus // 5
        self.drip_factor += 2 + self.chad_class.base_drip_bonus // 5
        
        return True
    
    def get_xp_for_next_level(self):
        """Calculate XP needed for the next level."""
        return 100 * self.level + 50 * (self.level - 1) ** 2
    
    def get_total_stats(self):
        """Get total stats including bonuses from equipped items and waifus."""
        total_clout = self.clout
        total_roast = self.roast_level
        total_cringe = self.cringe_resistance
        total_drip = self.drip_factor
        
        # Add bonuses from equipped items
        from app.models.item import Item
        equipped_items = Item.query.filter_by(chad_id=self.id, is_equipped=True).all()
        for item in equipped_items:
            total_clout += item.clout_bonus or 0
            total_roast += item.roast_bonus or 0
            total_cringe += item.cringe_resistance_bonus or 0
            total_drip += item.drip_bonus or 0
        
        # Add bonuses from equipped waifus
        from app.models.waifu import Waifu
        equipped_waifus = Waifu.query.filter_by(chad_id=self.id, is_equipped=True).all()
        for waifu in equipped_waifus:
            total_clout += waifu.clout_bonus or 0
            total_roast += waifu.roast_bonus or 0
            total_cringe += waifu.cringe_resistance_bonus or 0
            total_drip += waifu.drip_bonus or 0
        
        # Create a stats object
        class Stats:
            def __init__(self, clout, roast, cringe, drip):
                self.clout = clout
                self.roast_level = roast
                self.cringe_resistance = cringe
                self.drip_factor = drip
        
        return Stats(total_clout, total_roast, total_cringe, total_drip) 