import uuid
from datetime import datetime
from enum import Enum
from app import db

class LocationType(Enum):
    """Types of locations in the game"""
    STARTER = "starter"  # Beginner areas
    TOWN = "town"        # Town/hub areas
    FIELD = "field"      # Standard field areas
    DUNGEON = "dungeon"  # Dungeon areas with tougher enemies
    ELITE = "elite"      # Elite areas with rare drops
    RAID = "raid"        # Raid areas for group battles
    EVENT = "event"      # Temporary event areas

class Location(db.Model):
    """Location model for defining game areas"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic information
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    location_type = db.Column(db.String(20), nullable=False)
    
    # Requirements
    min_level = db.Column(db.Integer, default=1)  # Minimum player level to access
    required_quest_id = db.Column(db.String(36), db.ForeignKey('quest.id'))  # Quest required to unlock
    required_item_id = db.Column(db.String(36), db.ForeignKey('item_type.id'))  # Item required to access
    
    # Gameplay properties
    enemy_level_min = db.Column(db.Integer, default=1)
    enemy_level_max = db.Column(db.Integer, default=5)
    enemy_density = db.Column(db.Float, default=1.0)  # Higher = more enemies
    rare_encounter_chance = db.Column(db.Float, default=0.1)  # Chance for rare encounters
    
    # Connections to other locations
    connected_locations = db.Column(db.Text)  # Comma-separated list of location IDs
    
    # Visual properties
    image_url = db.Column(db.String(255))
    background_color = db.Column(db.String(20), default="#94c9f0")  # Default light blue
    theme_music_url = db.Column(db.String(255))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_event_location = db.Column(db.Boolean, default=False)
    event_start_date = db.Column(db.DateTime)
    event_end_date = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    required_quest = db.relationship('Quest', foreign_keys=[required_quest_id])
    required_item = db.relationship('ItemType', foreign_keys=[required_item_id])
    
    def __repr__(self):
        return f'<Location {self.name} ({self.location_type})>'
    
    def is_accessible_by_player(self, user):
        """Check if a player can access this location"""
        from app.models.chad import Chad
        
        # Get player's character
        character = Chad.query.filter_by(user_id=user.id, is_active=True).first()
        if not character:
            return False, "No active character found"
            
        # Check level requirement
        if character.level < self.min_level:
            return False, f"Minimum level {self.min_level} required to access {self.name}"
            
        # Check quest requirement
        if self.required_quest_id:
            from app.models.quest import QuestStatus, UserQuest
            completed = UserQuest.query.filter_by(
                user_id=user.id, 
                quest_id=self.required_quest_id,
                status=QuestStatus.COMPLETED.value
            ).first()
            
            if not completed:
                quest_name = self.required_quest.name if self.required_quest else "a specific quest"
                return False, f"You need to complete {quest_name} to access {self.name}"
                
        # Check item requirement
        if self.required_item_id:
            from app.models.inventory import Inventory
            has_item = Inventory.query.filter_by(
                user_id=user.id, 
                item_type_id=self.required_item_id,
                is_consumed=False
            ).first()
            
            if not has_item:
                item_name = self.required_item.name if self.required_item else "a specific item"
                return False, f"You need {item_name} to access {self.name}"
                
        # Check if this is an active event location
        if self.is_event_location:
            now = datetime.utcnow()
            if self.event_start_date and now < self.event_start_date:
                return False, f"This event location is not yet available"
                
            if self.event_end_date and now > self.event_end_date:
                return False, f"This event location is no longer available"
                
        # All checks passed
        return True, "Location is accessible"
    
    def get_enemies(self, player_level=None, limit=10):
        """Get enemies in this location, potentially scaled to player level"""
        from app.models.pve_enemy import PVEEnemy
        
        # Get base enemies for this location
        enemies = PVEEnemy.query.filter_by(
            location_id=self.id,
            is_active=True
        ).all()
        
        # If no player level provided, return unmodified enemies
        if not player_level:
            return enemies[:limit] if limit else enemies
        
        # Scale enemy choice based on player level
        import random
        
        # Calculate adjustment based on player level vs. location level range
        level_diff = player_level - self.enemy_level_min
        
        # For very high level players in low level areas, chance for higher level enemies
        if level_diff > 10:
            elite_chance = min(0.5, level_diff * 0.03)  # Max 50% chance for elites
            boss_chance = min(0.2, level_diff * 0.01)   # Max 20% chance for bosses
            
            # Try to find elite/boss enemies
            from app.models.pve_enemy import EnemyType
            
            if random.random() < boss_chance:
                boss_enemies = [e for e in enemies if e.enemy_type in 
                               [EnemyType.BOSS.value, EnemyType.MINI_BOSS.value]]
                if boss_enemies:
                    # Include at least one boss in the mix
                    result = [random.choice(boss_enemies)]
                    remaining = random.sample(enemies, min(limit-1, len(enemies)))
                    result.extend(remaining)
                    return result[:limit]
                    
            elif random.random() < elite_chance:
                elite_enemies = [e for e in enemies if e.enemy_type == EnemyType.ELITE.value]
                if elite_enemies:
                    # Include at least one elite in the mix
                    result = [random.choice(elite_enemies)]
                    remaining = random.sample(enemies, min(limit-1, len(enemies)))
                    result.extend(remaining)
                    return result[:limit]
        
        # Normal distribution of enemies
        if limit and len(enemies) > limit:
            return random.sample(enemies, limit)
        return enemies
    
    def get_connected_locations(self):
        """Get list of connected locations"""
        if not self.connected_locations:
            return []
            
        location_ids = self.connected_locations.split(',')
        return Location.query.filter(Location.id.in_(location_ids)).all()
    
    @classmethod
    def get_starting_location(cls):
        """Get the default starting location for new players"""
        return cls.query.filter_by(
            location_type=LocationType.STARTER.value,
            is_active=True
        ).first()
    
    @classmethod
    def get_active_event_locations(cls):
        """Get all currently active event locations"""
        now = datetime.utcnow()
        return cls.query.filter(
            cls.is_event_location == True,
            cls.is_active == True,
            cls.event_start_date <= now,
            db.or_(
                cls.event_end_date == None,
                cls.event_end_date >= now
            )
        ).all()
    
    @classmethod
    def create_location(cls, name, location_type, description=None, min_level=1,
                       enemy_level_min=1, enemy_level_max=5, **kwargs):
        """Create a new location"""
        # Validate location type
        if location_type not in [lt.value for lt in LocationType]:
            raise ValueError(f"Invalid location type: {location_type}")
            
        location = cls(
            name=name,
            description=description or f"A {location_type} area",
            location_type=location_type,
            min_level=min_level,
            enemy_level_min=enemy_level_min,
            enemy_level_max=enemy_level_max,
            **kwargs
        )
        
        db.session.add(location)
        db.session.commit()
        
        return location 