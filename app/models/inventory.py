"""
Inventory model for Chad Battles.
Handles user inventory management.
"""
from app.extensions import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func

class Inventory(db.Model):
    """Inventory model for storing user inventory data."""
    __tablename__ = 'inventories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='inventory', uselist=False)
    
    def __repr__(self):
        return f'<Inventory {self.id} (User: {self.user_id})>'
    
    @hybrid_property
    def total_items(self):
        """Return the total number of items in the user's inventory"""
        from app.models.item import Item
        return Item.query.filter_by(user_id=self.user_id).count()
    
    @hybrid_property
    def total_waifus(self):
        """Return the total number of waifus in the user's inventory"""
        from app.models.waifu import Waifu
        return Waifu.query.filter_by(user_id=self.user_id).count()
    
    @hybrid_property
    def total_nfts(self):
        """Return the total number of NFTs in the user's inventory"""
        from app.models.nft import NFT
        return NFT.query.filter_by(user_id=self.user_id).count()
    
    @hybrid_property
    def equipped_items(self):
        """Return all equipped items in the user's inventory"""
        from app.models.item import Item
        return Item.query.filter_by(user_id=self.user_id, is_equipped=True).all()
    
    @hybrid_property
    def unequipped_items(self):
        """Return all unequipped items in the user's inventory"""
        from app.models.item import Item
        return Item.query.filter_by(user_id=self.user_id, is_equipped=False).all()
    
    @hybrid_property
    def equipped_waifus(self):
        """Return all equipped waifus in the user's inventory"""
        from app.models.waifu import Waifu
        return Waifu.query.filter_by(user_id=self.user_id, is_equipped=True).all()
    
    @hybrid_property
    def unequipped_waifus(self):
        """Return all unequipped waifus in the user's inventory"""
        from app.models.waifu import Waifu
        return Waifu.query.filter_by(user_id=self.user_id, is_equipped=False).all()
    
    def get_items_by_type(self, item_type_id):
        """Return all items of a specific type in the user's inventory"""
        from app.models.item import Item
        return Item.query.filter_by(user_id=self.user_id, item_type_id=item_type_id).all()
    
    def get_waifus_by_type(self, waifu_type_id):
        """Return all waifus of a specific type in the user's inventory"""
        from app.models.waifu import Waifu
        return Waifu.query.filter_by(user_id=self.user_id, waifu_type_id=waifu_type_id).all()
    
    def get_nfts_by_type(self, entity_type):
        """Return all NFTs of a specific entity type in the user's inventory"""
        from app.models.nft import NFT
        return NFT.query.filter_by(user_id=self.user_id, entity_type=entity_type).all()
    
    def equip_item(self, item_id, target_type='chad', target_id=None):
        """
        Equip an item to a character (chad or waifu)
        
        Args:
            item_id: The ID of the item to equip
            target_type: Either 'chad' or 'waifu'
            target_id: The ID of the waifu to equip to (only needed if target_type is 'waifu')
            
        Returns:
            (success, message) tuple
        """
        from app.models.item import Item
        from app.models.waifu import Waifu
        
        item = Item.query.filter_by(id=item_id, user_id=self.user_id).first()
        
        if not item:
            return False, "Item not found or does not belong to you"
        
        if target_type == 'waifu' and target_id:
            # Equipping to a waifu
            waifu = Waifu.query.filter_by(id=target_id, user_id=self.user_id).first()
            
            if not waifu:
                return False, "Waifu not found or does not belong to you"
            
            # Unequip any existing item of the same type from this waifu
            existing_items = Item.query.filter_by(
                user_id=self.user_id, 
                waifu_id=waifu.id, 
                item_type_id=item.item_type_id, 
                is_equipped=True
            ).all()
            
            for existing_item in existing_items:
                if existing_item.id != item_id:
                    existing_item.is_equipped = False
                    existing_item.waifu_id = None
            
            # Equip this item to the waifu
            item.is_equipped = True
            item.waifu_id = waifu.id
            item.chad_id = None  # Unequip from chad if equipped
            
            db.session.commit()
            
            return True, f"{item.item_type.name} equipped to {waifu.waifu_type.name}"
        
        else:
            # Equipping to the user's chad
            if not self.user.chad:
                return False, "You need to create a Chad character first"
            
            # Unequip any existing item of the same type
            existing_items = Item.query.filter_by(
                user_id=self.user_id, 
                chad_id=self.user.chad.id, 
                item_type_id=item.item_type_id, 
                is_equipped=True
            ).all()
            
            for existing_item in existing_items:
                if existing_item.id != item_id:
                    existing_item.is_equipped = False
                    existing_item.chad_id = None
            
            # Equip this item
            item.is_equipped = True
            item.chad_id = self.user.chad.id
            item.waifu_id = None  # Unequip from waifu if equipped
            
            db.session.commit()
            
            return True, f"{item.item_type.name} equipped to your Chad"
    
    def unequip_item(self, item_id):
        """
        Unequip an item from any equipped entity
        
        Args:
            item_id: The ID of the item to unequip
            
        Returns:
            (success, message) tuple
        """
        from app.models.item import Item
        
        item = Item.query.filter_by(id=item_id, user_id=self.user_id).first()
        
        if not item:
            return False, "Item not found or does not belong to you"
        
        if not item.is_equipped:
            return False, "This item is not currently equipped"
        
        # Determine what the item was equipped to for the message
        equipped_to = "your Chad" if item.chad_id else "your waifu"
        
        # Unequip the item
        item.is_equipped = False
        item.chad_id = None
        item.waifu_id = None
        
        db.session.commit()
        
        return True, f"{item.item_type.name} unequipped from {equipped_to}"
    
    def equip_waifu(self, waifu_id):
        """
        Equip a waifu for battle
        
        Args:
            waifu_id: The ID of the waifu to equip
            
        Returns:
            (success, message) tuple
        """
        from app.models.waifu import Waifu
        
        waifu = Waifu.query.filter_by(id=waifu_id, user_id=self.user_id).first()
        
        if not waifu:
            return False, "Waifu not found or does not belong to you"
        
        # First unequip any currently equipped waifu of the same type
        currently_equipped = Waifu.query.filter_by(
            user_id=self.user_id, 
            waifu_type_id=waifu.waifu_type_id, 
            is_equipped=True
        ).all()
        
        for equipped_waifu in currently_equipped:
            if equipped_waifu.id != waifu_id:
                equipped_waifu.is_equipped = False
        
        waifu.is_equipped = True
        db.session.commit()
        
        return True, f"{waifu.waifu_type.name} equipped for battle!"
    
    def unequip_waifu(self, waifu_id):
        """
        Unequip a waifu from battle
        
        Args:
            waifu_id: The ID of the waifu to unequip
            
        Returns:
            (success, message) tuple
        """
        from app.models.waifu import Waifu
        
        waifu = Waifu.query.filter_by(id=waifu_id, user_id=self.user_id).first()
        
        if not waifu:
            return False, "Waifu not found or does not belong to you"
        
        if not waifu.is_equipped:
            return False, "This waifu is not currently equipped"
        
        waifu.is_equipped = False
        db.session.commit()
        
        return True, f"{waifu.waifu_type.name} unequipped from battle" 