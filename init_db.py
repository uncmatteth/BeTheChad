#!/usr/bin/env python3
"""
Database Initialization Script

This script populates the database with initial data required for the game:
- Chad Classes
- Waifu Rarities
- Waifu Types (starter waifu)
- Item Rarities
- Item Types
- Elixir Types
"""

import os
import sys
from datetime import datetime

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.chad import ChadClass
from app.models.waifu import WaifuRarity, WaifuType
from app.models.item import ItemRarity, ItemType
from app.models.meme_elixir import ElixirType

def init_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

def create_chad_classes():
    """Create the default Chad classes"""
    classes = [
        {
            'name': 'Meme Overlord',
            'description': 'Masters of internet culture and viral content.',
            'base_clout_bonus': 2,
            'base_roast_bonus': 3,
            'base_cringe_resistance_bonus': 1,
            'base_drip_bonus': 2
        },
        {
            'name': 'Crypto Knight',
            'description': 'Defenders of the blockchain and crypto enthusiasts.',
            'base_clout_bonus': 3,
            'base_roast_bonus': 1,
            'base_cringe_resistance_bonus': 3,
            'base_drip_bonus': 1
        },
        {
            'name': 'Alpha Chad',
            'description': 'The embodiment of confidence and dominance.',
            'base_clout_bonus': 2,
            'base_roast_bonus': 3,
            'base_cringe_resistance_bonus': 2,
            'base_drip_bonus': 1
        },
        {
            'name': 'Sigma Grindset',
            'description': 'Lone wolves focused on self-improvement and the grind.',
            'base_clout_bonus': 1,
            'base_roast_bonus': 2,
            'base_cringe_resistance_bonus': 3,
            'base_drip_bonus': 2
        },
        {
            'name': 'Ratio King',
            'description': 'Masters of the devastating Twitter ratio.',
            'base_clout_bonus': 3,
            'base_roast_bonus': 4,
            'base_cringe_resistance_bonus': 1,
            'base_drip_bonus': 0
        },
        {
            'name': 'Normie Chad',
            'description': 'A balanced Chad with no particular specialization.',
            'base_clout_bonus': 1,
            'base_roast_bonus': 1,
            'base_cringe_resistance_bonus': 1,
            'base_drip_bonus': 1
        }
    ]
    
    for class_data in classes:
        chad_class = ChadClass(**class_data)
        db.session.add(chad_class)
    
    db.session.commit()
    print(f"Created {len(classes)} Chad classes")

def create_waifu_rarities():
    """Create the default Waifu rarities"""
    rarities = [
        {
            'name': 'Common',
            'description': 'The most common waifu rarity',
            'base_stat_multiplier': 1.0,
            'drop_rate': 0.5
        },
        {
            'name': 'Uncommon',
            'description': 'Slightly uncommon waifus',
            'base_stat_multiplier': 1.5,
            'drop_rate': 0.3
        },
        {
            'name': 'Rare',
            'description': 'Rare waifus with good stats',
            'base_stat_multiplier': 2.0,
            'drop_rate': 0.15
        },
        {
            'name': 'Epic',
            'description': 'Very rare waifus with great stats',
            'base_stat_multiplier': 3.0,
            'drop_rate': 0.04
        },
        {
            'name': 'Legendary',
            'description': 'The rarest waifus with amazing stats',
            'base_stat_multiplier': 5.0,
            'drop_rate': 0.01
        }
    ]
    
    for rarity_data in rarities:
        rarity = WaifuRarity(**rarity_data)
        db.session.add(rarity)
    
    db.session.commit()
    print(f"Created {len(rarities)} Waifu rarities")

def create_starter_waifus():
    """Create the starter waifus for each Chad class"""
    common_rarity = WaifuRarity.query.filter_by(name='Common').first()
    
    starter_waifus = [
        {
            'name': 'Starter Waifu',
            'description': 'A basic waifu to start your journey',
            'image_url': '/static/img/waifu/starter-waifu.png',
            'rarity_id': common_rarity.id,
            'base_clout_bonus': 1,
            'base_roast_bonus': 1,
            'base_cringe_resistance_bonus': 1,
            'base_drip_bonus': 1
        },
        {
            'name': 'Meme Chan',
            'description': 'Perfect for Meme Overlords',
            'image_url': '/static/img/waifu/meme-chan.png',
            'rarity_id': common_rarity.id,
            'base_clout_bonus': 1,
            'base_roast_bonus': 2,
            'base_cringe_resistance_bonus': 0,
            'base_drip_bonus': 1
        },
        {
            'name': 'Crypto Girl',
            'description': 'Perfect for Crypto Knights',
            'image_url': '/static/img/waifu/crypto-girl.png',
            'rarity_id': common_rarity.id,
            'base_clout_bonus': 2,
            'base_roast_bonus': 0,
            'base_cringe_resistance_bonus': 2,
            'base_drip_bonus': 0
        },
        {
            'name': 'Alpha Waifu',
            'description': 'Perfect for Alpha Chads',
            'image_url': '/static/img/waifu/alpha-waifu.png',
            'rarity_id': common_rarity.id,
            'base_clout_bonus': 1,
            'base_roast_bonus': 2,
            'base_cringe_resistance_bonus': 1,
            'base_drip_bonus': 0
        },
        {
            'name': 'Sigma Waifu',
            'description': 'Perfect for Sigma Grindsets',
            'image_url': '/static/img/waifu/sigma-waifu.png',
            'rarity_id': common_rarity.id,
            'base_clout_bonus': 0,
            'base_roast_bonus': 1,
            'base_cringe_resistance_bonus': 2,
            'base_drip_bonus': 1
        },
        {
            'name': 'Ratio Waifu',
            'description': 'Perfect for Ratio Kings',
            'image_url': '/static/img/waifu/ratio-waifu.png',
            'rarity_id': common_rarity.id,
            'base_clout_bonus': 2,
            'base_roast_bonus': 2,
            'base_cringe_resistance_bonus': 0,
            'base_drip_bonus': 0
        }
    ]
    
    for waifu_data in starter_waifus:
        waifu_type = WaifuType(**waifu_data)
        db.session.add(waifu_type)
    
    db.session.commit()
    print(f"Created {len(starter_waifus)} starter Waifu types")

def create_item_rarities():
    """Create the default Item rarities"""
    rarities = [
        {
            'name': 'Common',
            'description': 'The most common item rarity',
            'base_stat_multiplier': 1.0,
            'drop_rate': 0.5
        },
        {
            'name': 'Uncommon',
            'description': 'Slightly uncommon items',
            'base_stat_multiplier': 1.5,
            'drop_rate': 0.3
        },
        {
            'name': 'Rare',
            'description': 'Rare items with good stats',
            'base_stat_multiplier': 2.0,
            'drop_rate': 0.15
        },
        {
            'name': 'Epic',
            'description': 'Very rare items with great stats',
            'base_stat_multiplier': 3.0,
            'drop_rate': 0.04
        },
        {
            'name': 'Legendary',
            'description': 'The rarest items with amazing stats',
            'base_stat_multiplier': 5.0,
            'drop_rate': 0.01
        }
    ]
    
    for rarity_data in rarities:
        rarity = ItemRarity(**rarity_data)
        db.session.add(rarity)
    
    db.session.commit()
    print(f"Created {len(rarities)} Item rarities")

def create_item_types():
    """Create default Item types"""
    common_rarity = ItemRarity.query.filter_by(name='Common').first()
    uncommon_rarity = ItemRarity.query.filter_by(name='Uncommon').first()
    rare_rarity = ItemRarity.query.filter_by(name='Rare').first()
    
    # Character items
    character_items = [
        {
            'name': 'Ratio Hammer',
            'description': 'Increases your ability to ratio opponents',
            'image_url': '/static/img/item/ratio-hammer.png',
            'rarity_id': uncommon_rarity.id,
            'is_character_item': True,
            'base_clout_bonus': 0,
            'base_roast_bonus': 3,
            'base_cringe_resistance_bonus': 0,
            'base_drip_bonus': 0
        },
        {
            'name': 'Drip Shades',
            'description': 'Increases your swag and style',
            'image_url': '/static/img/item/drip-shades.png',
            'rarity_id': common_rarity.id,
            'is_character_item': True,
            'base_clout_bonus': 1,
            'base_roast_bonus': 0,
            'base_cringe_resistance_bonus': 0,
            'base_drip_bonus': 2
        },
        {
            'name': 'Cringe Shield',
            'description': 'Protects against cringe attacks',
            'image_url': '/static/img/item/cringe-shield.png',
            'rarity_id': uncommon_rarity.id,
            'is_character_item': True,
            'base_clout_bonus': 0,
            'base_roast_bonus': 0,
            'base_cringe_resistance_bonus': 3,
            'base_drip_bonus': 0
        },
        {
            'name': 'Clout Goggles',
            'description': 'Increases your influence and reputation',
            'image_url': '/static/img/item/clout-goggles.png',
            'rarity_id': rare_rarity.id,
            'is_character_item': True,
            'base_clout_bonus': 5,
            'base_roast_bonus': 0,
            'base_cringe_resistance_bonus': 0,
            'base_drip_bonus': 2
        }
    ]
    
    # Waifu items
    waifu_items = [
        {
            'name': 'Meme Book',
            'description': 'Teaches your waifu the art of memes',
            'image_url': '/static/img/item/meme-book.png',
            'rarity_id': common_rarity.id,
            'is_character_item': False,
            'base_clout_bonus': 0,
            'base_roast_bonus': 2,
            'base_cringe_resistance_bonus': 0,
            'base_drip_bonus': 0
        },
        {
            'name': 'Cute Ribbon',
            'description': 'Increases your waifu\'s style',
            'image_url': '/static/img/item/cute-ribbon.png',
            'rarity_id': common_rarity.id,
            'is_character_item': False,
            'base_clout_bonus': 0,
            'base_roast_bonus': 0,
            'base_cringe_resistance_bonus': 0,
            'base_drip_bonus': 2
        },
        {
            'name': 'Crown of Drip',
            'description': 'Significantly increases your waifu\'s style',
            'image_url': '/static/img/item/crown-of-drip.png',
            'rarity_id': rare_rarity.id,
            'is_character_item': False,
            'base_clout_bonus': 2,
            'base_roast_bonus': 0,
            'base_cringe_resistance_bonus': 0,
            'base_drip_bonus': 5
        }
    ]
    
    for item_data in character_items + waifu_items:
        item_type = ItemType(**item_data)
        db.session.add(item_type)
    
    db.session.commit()
    print(f"Created {len(character_items)} character items and {len(waifu_items)} waifu items")

def create_elixir_types():
    """Create default Elixir types"""
    elixirs = [
        {
            'name': 'Mega Clout Boost',
            'description': 'Greatly increases your Clout for one battle',
            'image_url': '/static/img/elixir/mega-clout-boost.png',
            'duration': 0,  # One-time use
            'price': 50,
            'clout_boost': 50,
            'roast_boost': 0,
            'cringe_resistance_boost': 0,
            'drip_boost': 0,
            'is_percentage': True
        },
        {
            'name': 'Roast Enhancer',
            'description': 'Increases your Roast Level for one battle',
            'image_url': '/static/img/elixir/roast-enhancer.png',
            'duration': 0,  # One-time use
            'price': 50,
            'clout_boost': 0,
            'roast_boost': 50,
            'cringe_resistance_boost': 0,
            'drip_boost': 0,
            'is_percentage': True
        },
        {
            'name': 'Anti-Cringe Potion',
            'description': 'Boosts your Cringe Resistance for 24 hours',
            'image_url': '/static/img/elixir/anti-cringe-potion.png',
            'duration': 24,
            'price': 75,
            'clout_boost': 0,
            'roast_boost': 0,
            'cringe_resistance_boost': 25,
            'drip_boost': 0,
            'is_percentage': True
        },
        {
            'name': 'Drip Enhancer',
            'description': 'Increases your Drip Factor for 24 hours',
            'image_url': '/static/img/elixir/drip-enhancer.png',
            'duration': 24,
            'price': 75,
            'clout_boost': 0,
            'roast_boost': 0,
            'cringe_resistance_boost': 0,
            'drip_boost': 25,
            'is_percentage': True
        },
        {
            'name': 'All Stats Boost',
            'description': 'Increases all stats by 10% for 24 hours',
            'image_url': '/static/img/elixir/all-stats-boost.png',
            'duration': 24,
            'price': 100,
            'clout_boost': 10,
            'roast_boost': 10,
            'cringe_resistance_boost': 10,
            'drip_boost': 10,
            'is_percentage': True
        }
    ]
    
    for elixir_data in elixirs:
        elixir_type = ElixirType(**elixir_data)
        db.session.add(elixir_type)
    
    db.session.commit()
    print(f"Created {len(elixirs)} elixir types")

if __name__ == "__main__":
    init_database() 