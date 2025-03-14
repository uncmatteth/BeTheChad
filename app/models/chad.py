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
    
    @property
    def equipped_items(self):
        """Get all equipped items for this Chad."""
        try:
            from app.models.item import Item
            from sqlalchemy.orm import Query
            
            # Return a query object that can be used with .all(), .first(), etc.
            return Query(Item, db.session()).filter(Item.chad_id == self.id, Item.is_equipped == True)
        except Exception as e:
            # Log error but return empty query
            from flask import current_app
            current_app.logger.error(f"Error getting equipped items for Chad {self.id}: {str(e)}")
            # Return an empty list-like object
            from sqlalchemy.orm.collections import InstrumentedList
            return InstrumentedList()
    
    @property
    def equipped_waifus(self):
        """Get all equipped waifus for this Chad."""
        try:
            from app.models.waifu import Waifu
            from sqlalchemy.orm import Query
            
            # Return a query object that can be used with .all(), .first(), etc.
            return Query(Waifu, db.session()).filter(Waifu.chad_id == self.id, Waifu.is_equipped == True)
        except Exception as e:
            # Log error but return empty query
            from flask import current_app
            current_app.logger.error(f"Error getting equipped waifus for Chad {self.id}: {str(e)}")
            # Return an empty list-like object
            from sqlalchemy.orm.collections import InstrumentedList
            return InstrumentedList()
    
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
    
    def get_stats_as_dict(self):
        """Return stats as a dictionary."""
        return {
            'clout': self.clout,
            'roast_level': self.roast_level,
            'cringe_resistance': self.cringe_resistance,
            'drip_factor': self.drip_factor
        }
        
    def calculate_stats(self):
        """Alias for get_total_stats() to maintain backwards compatibility."""
        return self.get_total_stats()
    
    def get_total_stats(self):
        """Calculate total stats from base + bonuses from equipped items and waifus."""
        try:
            # Create a Stats class to hold the calculated stats
            class Stats:
                def __init__(self, clout, roast_level, cringe_resistance, drip_factor):
                    self.clout = clout
                    self.roast_level = roast_level
                    self.cringe_resistance = cringe_resistance
                    self.drip_factor = drip_factor
            
            # Start with base stats
            total_clout = self.clout
            total_roast = self.roast_level
            total_cringe = self.cringe_resistance
            total_drip = self.drip_factor
            
            # Add class bonuses if available
            if hasattr(self, 'chad_class') and self.chad_class:
                total_clout += self.chad_class.base_clout_bonus or 0
                total_roast += self.chad_class.base_roast_bonus or 0
                total_cringe += self.chad_class.base_cringe_resistance_bonus or 0
                total_drip += self.chad_class.base_drip_bonus or 0
            
            # Add bonuses from equipped items
            try:
                from flask import current_app
                from app.models.item import Item
                
                equipped_items = Item.query.filter_by(chad_id=self.id, is_equipped=True).all()
                for item in equipped_items:
                    total_clout += item.clout_bonus or 0
                    total_roast += item.roast_bonus or 0
                    total_cringe += item.cringe_resistance_bonus or 0
                    total_drip += item.drip_bonus or 0
            except Exception as e:
                # Log error but continue
                from flask import current_app
                current_app.logger.error(f"Error getting equipped items for Chad {self.id}: {str(e)}")
            
            # Add bonuses from equipped waifus
            try:
                equipped_waifus = self.get_equipped_waifus()
                for waifu in equipped_waifus:
                    total_clout += waifu.clout_bonus or 0
                    total_roast += waifu.roast_bonus or 0
                    total_cringe += waifu.cringe_resistance_bonus or 0
                    total_drip += waifu.drip_bonus or 0
            except Exception as e:
                # Log error but continue
                from flask import current_app
                current_app.logger.error(f"Error getting equipped waifus for Chad {self.id}: {str(e)}")
            
            return Stats(total_clout, total_roast, total_cringe, total_drip)
        except Exception as e:
            # Return base stats if there's an error
            from flask import current_app
            current_app.logger.error(f"Error calculating total stats for Chad {self.id}: {str(e)}")
            return Stats(self.clout, self.roast_level, self.cringe_resistance, self.drip_factor)
    
    def get_equipped_waifus(self):
        """Get all equipped waifus for this Chad."""
        try:
            from app.models.waifu import Waifu
            return Waifu.query.filter_by(chad_id=self.id, is_equipped=True).all()
        except Exception as e:
            # Log error but return empty list
            from flask import current_app
            current_app.logger.error(f"Error getting equipped waifus for Chad {self.id}: {str(e)}")
            return [] 