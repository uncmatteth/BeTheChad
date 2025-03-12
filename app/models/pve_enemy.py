import uuid
from datetime import datetime
from enum import Enum
from app import db
from sqlalchemy.dialects.postgresql import JSONB

class EnemyType(Enum):
    """Types of enemies in the game"""
    BASIC = "basic"  # Regular enemies
    ELITE = "elite"  # Elite enemies with special abilities
    MINI_BOSS = "mini_boss"  # Mini bosses
    BOSS = "boss"  # Full bosses
    RAID_BOSS = "raid_boss"  # Raid bosses requiring team effort

class PVEEnemy(db.Model):
    """PVE enemy model for AI opponents in battles"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic information
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    enemy_type = db.Column(db.String(20), nullable=False)
    
    # Gameplay stats
    level = db.Column(db.Integer, default=1)
    base_power = db.Column(db.Integer, nullable=False)
    base_hp = db.Column(db.Integer, nullable=False)
    
    # Attack stats
    attack_power = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    
    # Special abilities
    abilities = db.Column(JSONB)  # [{"name": "Ability Name", "description": "What it does", "cooldown": 2}, ...]
    
    # Rewards
    xp_reward_base = db.Column(db.Integer, default=10)
    coin_reward_base = db.Column(db.Integer, default=20)
    min_level_to_defeat = db.Column(db.Integer, default=1)  # Recommended minimum level
    
    # Drop chances
    item_drop_chance = db.Column(db.Float, default=0.1)  # 0-1 chance to drop an item
    rare_item_drop_chance = db.Column(db.Float, default=0.01)  # 0-1 chance to drop a rare item
    
    # Metadata
    is_active = db.Column(db.Boolean, default=True)
    location_id = db.Column(db.String(36), db.ForeignKey('location.id'))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    location = db.relationship('Location', backref='enemies')
    possible_drops = db.relationship('ItemType', secondary='enemy_drops')
    
    def __repr__(self):
        return f'<PVEEnemy {self.name} (Lvl {self.level} {self.enemy_type})>'
    
    def calculate_battle_power(self):
        """Calculate the total battle power of this enemy"""
        # Base power increases with level
        level_multiplier = 1 + (self.level * 0.1)  # 10% increase per level
        
        # Enemy type affects power
        type_multiplier = {
            EnemyType.BASIC.value: 1.0,
            EnemyType.ELITE.value: 1.3,
            EnemyType.MINI_BOSS.value: 1.7,
            EnemyType.BOSS.value: 2.5,
            EnemyType.RAID_BOSS.value: 4.0
        }.get(self.enemy_type, 1.0)
        
        # Ability count affects power
        ability_bonus = len(self.abilities) * 50 if self.abilities else 0
        
        # Calculate total power
        total_power = (self.base_power * level_multiplier * type_multiplier) + ability_bonus
        
        return int(total_power)
    
    def calculate_effective_hp(self):
        """Calculate effective hit points based on base HP, level and defense"""
        level_multiplier = 1 + (self.level * 0.15)  # 15% increase per level
        defense_bonus = self.defense * 0.5  # Each point of defense adds effective HP
        
        return int(self.base_hp * level_multiplier + defense_bonus)
    
    def get_scaled_rewards(self, player_level):
        """Get scaled rewards based on player level difference"""
        # Calculate level difference
        level_diff = self.level - player_level
        
        # Scale rewards
        if level_diff > 5:  # Much higher level enemy
            xp_mult = 2.0
            coin_mult = 2.5
        elif level_diff > 2:  # Higher level enemy
            xp_mult = 1.5
            coin_mult = 1.8
        elif level_diff >= 0:  # Similar level
            xp_mult = 1.0
            coin_mult = 1.0
        elif level_diff > -5:  # Lower level
            xp_mult = max(0.2, 1.0 + (level_diff * 0.1))  # At least 20% rewards
            coin_mult = max(0.2, 1.0 + (level_diff * 0.1))
        else:  # Much lower level
            xp_mult = 0.1
            coin_mult = 0.1
            
        xp_reward = int(self.xp_reward_base * xp_mult)
        coin_reward = int(self.coin_reward_base * coin_mult)
        
        return {
            "xp": xp_reward,
            "coins": coin_reward,
            "item_drop_chance": self.calculate_adjusted_drop_chance(player_level)
        }
    
    def calculate_adjusted_drop_chance(self, player_level):
        """Calculate adjusted drop chance based on player level"""
        # Higher level players have reduced drop chances for low-level enemies
        level_diff = player_level - self.level
        
        if level_diff <= 0:  # Player is lower or equal level
            drop_chance = self.item_drop_chance
            rare_drop_chance = self.rare_item_drop_chance
        else:
            # Reduce drop chance by 10% for each level above the enemy, minimum 10%
            drop_mult = max(0.1, 1.0 - (level_diff * 0.1))
            drop_chance = self.item_drop_chance * drop_mult
            rare_drop_chance = self.rare_item_drop_chance * drop_mult
        
        return {
            "normal": drop_chance,
            "rare": rare_drop_chance
        }
    
    def get_possible_drop_items(self, player_level):
        """Get a list of possible drop items based on player level"""
        from app.models.item import ItemType
        
        # Get items appropriate for this enemy's level range
        min_item_level = max(1, self.level - 2)
        max_item_level = self.level + 3
        
        # Adjust based on player level if needed
        if player_level > self.level + 5:
            # For much higher level players, reduce the quality of drops
            max_item_level = min(max_item_level, player_level - 3)
        
        # Query for appropriate items
        suitable_items = ItemType.query.filter(
            ItemType.min_level <= max_item_level,
            ItemType.max_level >= min_item_level
        ).all()
        
        return suitable_items
    
    @classmethod
    def create_enemy(cls, name, enemy_type, level, base_stats, abilities=None, location_id=None):
        """Create a new enemy with appropriate stats for its level and type"""
        # Validate enemy type
        if enemy_type not in [e.value for e in EnemyType]:
            raise ValueError(f"Invalid enemy type: {enemy_type}")
            
        # Define base multipliers by enemy type
        type_multipliers = {
            EnemyType.BASIC.value: {
                "power": 1.0,
                "hp": 1.0,
                "attack": 1.0,
                "defense": 1.0,
                "speed": 1.0,
                "xp_reward": 1.0,
                "coin_reward": 1.0
            },
            EnemyType.ELITE.value: {
                "power": 1.3,
                "hp": 1.5,
                "attack": 1.3,
                "defense": 1.3,
                "speed": 1.1,
                "xp_reward": 1.5,
                "coin_reward": 1.7
            },
            EnemyType.MINI_BOSS.value: {
                "power": 1.7,
                "hp": 2.5,
                "attack": 1.5,
                "defense": 1.7,
                "speed": 0.9,
                "xp_reward": 2.0,
                "coin_reward": 2.5
            },
            EnemyType.BOSS.value: {
                "power": 2.5,
                "hp": 4.0,
                "attack": 2.0,
                "defense": 2.0,
                "speed": 1.0,
                "xp_reward": 3.0,
                "coin_reward": 4.0
            },
            EnemyType.RAID_BOSS.value: {
                "power": 4.0,
                "hp": 10.0,
                "attack": 3.0,
                "defense": 3.0,
                "speed": 1.2,
                "xp_reward": 5.0,
                "coin_reward": 10.0
            }
        }
        
        # Get multipliers for this enemy type
        multipliers = type_multipliers.get(enemy_type, type_multipliers[EnemyType.BASIC.value])
        
        # Scale base stats by level and type
        level_power_scaling = 10
        level_hp_scaling = 20
        level_attack_scaling = 5
        level_defense_scaling = 5
        level_speed_scaling = 2
        
        scaled_power = (base_stats.get("power", 100) + (level * level_power_scaling)) * multipliers["power"]
        scaled_hp = (base_stats.get("hp", 200) + (level * level_hp_scaling)) * multipliers["hp"]
        scaled_attack = (base_stats.get("attack", 50) + (level * level_attack_scaling)) * multipliers["attack"]
        scaled_defense = (base_stats.get("defense", 40) + (level * level_defense_scaling)) * multipliers["defense"]
        scaled_speed = (base_stats.get("speed", 30) + (level * level_speed_scaling)) * multipliers["speed"]
        
        # Scale rewards
        xp_reward = (10 + (level * 3)) * multipliers["xp_reward"]
        coin_reward = (20 + (level * 5)) * multipliers["coin_reward"]
        
        # Scale drop chances
        base_drop_chance = 0.1 + (level * 0.01)  # Increases slightly with level
        base_rare_drop = 0.01 + (level * 0.002)   # Increases slightly with level
        
        if enemy_type == EnemyType.ELITE.value:
            base_drop_chance += 0.1
            base_rare_drop += 0.02
        elif enemy_type == EnemyType.MINI_BOSS.value:
            base_drop_chance += 0.2
            base_rare_drop += 0.05
        elif enemy_type == EnemyType.BOSS.value:
            base_drop_chance += 0.4
            base_rare_drop += 0.1
        elif enemy_type == EnemyType.RAID_BOSS.value:
            base_drop_chance = 1.0  # Guaranteed drop
            base_rare_drop += 0.3
        
        # Create enemy
        enemy = cls(
            name=name,
            description=f"A level {level} {enemy_type} enemy",
            enemy_type=enemy_type,
            level=level,
            base_power=int(scaled_power),
            base_hp=int(scaled_hp),
            attack_power=int(scaled_attack),
            defense=int(scaled_defense),
            speed=int(scaled_speed),
            abilities=abilities or [],
            xp_reward_base=int(xp_reward),
            coin_reward_base=int(coin_reward),
            min_level_to_defeat=max(1, level - 3),
            item_drop_chance=min(1.0, base_drop_chance),
            rare_item_drop_chance=min(0.5, base_rare_drop),
            location_id=location_id
        )
        
        db.session.add(enemy)
        db.session.commit()
        
        return enemy
        
# Association table for enemy drops
enemy_drops = db.Table('enemy_drops',
    db.Column('enemy_id', db.String(36), db.ForeignKey('pve_enemy.id'), primary_key=True),
    db.Column('item_type_id', db.String(36), db.ForeignKey('item_type.id'), primary_key=True),
    db.Column('drop_chance', db.Float, default=0.1),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
) 