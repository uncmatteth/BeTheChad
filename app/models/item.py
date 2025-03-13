"""
Item model for Chad Battles.
"""
from app.extensions import db
from datetime import datetime

class ItemRarity(db.Model):
    """Item rarity model for different rarity levels."""
    __tablename__ = 'item_rarities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    drop_rate = db.Column(db.Float, default=0.0)
    min_stat_bonus = db.Column(db.Integer, default=1)
    max_stat_bonus = db.Column(db.Integer, default=5)
    
    # Relationships
    item_types = db.relationship('ItemType', backref='rarity', lazy='dynamic')
    
    def __repr__(self):
        return f'<ItemRarity {self.name}>'

class ItemType(db.Model):
    """Item type model for different item types."""
    __tablename__ = 'item_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    rarity_id = db.Column(db.Integer, db.ForeignKey('item_rarities.id'), nullable=False)
    slot = db.Column(db.String(50), nullable=False)  # head, body, accessory, etc.
    base_clout_bonus = db.Column(db.Integer, default=0)
    base_roast_bonus = db.Column(db.Integer, default=0)
    base_cringe_resistance_bonus = db.Column(db.Integer, default=0)
    base_drip_bonus = db.Column(db.Integer, default=0)
    is_character_item = db.Column(db.Boolean, default=True)
    
    # Relationships
    items = db.relationship('Item', backref='item_type', lazy='dynamic')
    
    def __repr__(self):
        return f'<ItemType {self.name} ({self.rarity.name})>'

class Item(db.Model):
    """Item model for equippable items."""
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chad_id = db.Column(db.Integer, db.ForeignKey('chads.id'), nullable=True)
    waifu_id = db.Column(db.Integer, db.ForeignKey('waifus.id'), nullable=True)
    item_type_id = db.Column(db.Integer, db.ForeignKey('item_types.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    is_equipped = db.Column(db.Boolean, default=False)
    
    # Type column for inheritance
    type = db.Column(db.String(50))
    
    # Stats
    clout_bonus = db.Column(db.Integer, default=0)
    roast_bonus = db.Column(db.Integer, default=0)
    cringe_resistance_bonus = db.Column(db.Integer, default=0)
    drip_bonus = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'item'
    }
    
    def __repr__(self):
        return f'<Item {self.name}>'
    
    def equip_to_chad(self, chad_id):
        """Equip the item to a Chad."""
        # Unequip any currently equipped items of the same slot
        currently_equipped = Item.query.filter_by(
            chad_id=chad_id,
            is_equipped=True
        ).join(ItemType).filter(
            ItemType.slot == self.item_type.slot
        ).all()
        
        for item in currently_equipped:
            item.is_equipped = False
            item.chad_id = None
            item.waifu_id = None
        
        # Equip this item
        self.chad_id = chad_id
        self.waifu_id = None
        self.is_equipped = True
        db.session.commit()
        
        return True
    
    def equip_to_waifu(self, waifu_id):
        """Equip the item to a Waifu."""
        # Unequip any currently equipped items of the same slot
        currently_equipped = Item.query.filter_by(
            waifu_id=waifu_id,
            is_equipped=True
        ).join(ItemType).filter(
            ItemType.slot == self.item_type.slot
        ).all()
        
        for item in currently_equipped:
            item.is_equipped = False
            item.chad_id = None
            item.waifu_id = None
        
        # Equip this item
        self.waifu_id = waifu_id
        self.chad_id = None
        self.is_equipped = True
        db.session.commit()
        
        return True
    
    def unequip(self):
        """Unequip the item."""
        self.chad_id = None
        self.waifu_id = None
        self.is_equipped = False
        db.session.commit()
        
        return True

class WaifuItem(Item):
    """Item specifically for waifus."""
    __mapper_args__ = {
        'polymorphic_identity': 'waifu_item',
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def create(cls, user_id, item_type_id, name=None):
        """Factory method to create a new waifu item."""
        item_type = ItemType.query.get(item_type_id)
        if not item_type:
            return None
            
        item = cls(
            user_id=user_id,
            item_type_id=item_type_id,
            name=name or item_type.name,
            clout_bonus=item_type.base_clout_bonus,
            roast_bonus=item_type.base_roast_bonus,
            cringe_resistance_bonus=item_type.base_cringe_resistance_bonus,
            drip_bonus=item_type.base_drip_bonus
        )
        db.session.add(item)
        db.session.commit()
        return item

class CharacterItem(Item):
    """Item specifically for chad characters."""
    __mapper_args__ = {
        'polymorphic_identity': 'character_item',
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def create(cls, user_id, item_type_id, name=None):
        """Factory method to create a new character item."""
        item_type = ItemType.query.get(item_type_id)
        if not item_type:
            return None
            
        item = cls(
            user_id=user_id,
            item_type_id=item_type_id,
            name=name or item_type.name,
            clout_bonus=item_type.base_clout_bonus,
            roast_bonus=item_type.base_roast_bonus,
            cringe_resistance_bonus=item_type.base_cringe_resistance_bonus,
            drip_bonus=item_type.base_drip_bonus
        )
        db.session.add(item)
        db.session.commit()
        return item 