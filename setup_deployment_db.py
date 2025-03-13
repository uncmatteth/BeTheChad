"""
Setup script for deployment database initialization.
This script initializes a minimal database for deployment without blockchain dependencies.
"""
from app import create_app, db
from app.models.user import User
from app.models.chad import Chad, ChadClass, ChadRarity
from app.models.waifu import Waifu, WaifuType, WaifuRarity
from app.models.item import Item, ItemType, ItemRarity, WaifuItem, CharacterItem
from app.models.cabal import Cabal, CabalMember
import os
import sys
import random
from datetime import datetime

def setup_deployment_db(env='production'):
    """Initialize the database with minimal required data.
    
    Args:
        env (str): The environment to run in (development, testing, production)
    """
    print(f"Starting database initialization for {env} environment...")
    
    try:
        app = create_app(env)
        
        with app.app_context():
            # Create tables
            db.create_all()
            print("Tables created successfully.")
            
            # Check if we need to add seed data
            if ChadRarity.query.count() == 0:
                print("Adding seed data for item types...")
                
                # Create item rarities
                common = ItemRarity(name="Common", description="Common items with basic stats", drop_rate=0.6, min_stat_bonus=1, max_stat_bonus=3)
                rare = ItemRarity(name="Rare", description="Rare items with improved stats", drop_rate=0.3, min_stat_bonus=2, max_stat_bonus=5)
                epic = ItemRarity(name="Epic", description="Epic items with powerful stats", drop_rate=0.09, min_stat_bonus=3, max_stat_bonus=8)
                legendary = ItemRarity(name="Legendary", description="Legendary items with amazing stats", drop_rate=0.01, min_stat_bonus=5, max_stat_bonus=12)

                db.session.add_all([common, rare, epic, legendary])
                db.session.commit()
                
                # Create waifu rarities
                waifu_common = WaifuRarity(name="Common", description="Common waifus", drop_rate=0.6, min_stat_bonus=1, max_stat_bonus=3)
                waifu_rare = WaifuRarity(name="Rare", description="Rare waifus", drop_rate=0.3, min_stat_bonus=2, max_stat_bonus=5)
                waifu_epic = WaifuRarity(name="Epic", description="Epic waifus", drop_rate=0.09, min_stat_bonus=3, max_stat_bonus=8)
                waifu_legendary = WaifuRarity(name="Legendary", description="Legendary waifus", drop_rate=0.01, min_stat_bonus=5, max_stat_bonus=12)

                db.session.add_all([waifu_common, waifu_rare, waifu_epic, waifu_legendary])
                db.session.commit()
                
                # Create chad classes
                sigma = ChadClass(name="Sigma", description="The lone wolf who follows his own path.", 
                               base_clout=10, base_roast=8, base_cringe_resistance=7, base_drip=5)
                alpha = ChadClass(name="Alpha", description="The classic leader of the pack.", 
                               base_clout=7, base_roast=10, base_cringe_resistance=5, base_drip=8)
                giga = ChadClass(name="Giga", description="Absolute unit of a Chad.", 
                              base_clout=8, base_roast=5, base_cringe_resistance=10, base_drip=7)

                db.session.add_all([sigma, alpha, giga])
                db.session.commit()
                
                # Create chad rarities
                chad_common = ChadRarity(name="Normie", description="Just a regular Chad", drop_rate=0.7)
                chad_rare = ChadRarity(name="Based", description="A based Chad", drop_rate=0.25)
                chad_epic = ChadRarity(name="Elite", description="An elite Chad", drop_rate=0.05)

                db.session.add_all([chad_common, chad_rare, chad_epic])
                db.session.commit()
                
                # Create waifu types
                waifu_types = [
                    WaifuType(name="Tsundere", description="Cold outside, warm inside", 
                           rarity_id=waifu_common.id, 
                           base_clout_bonus=1, base_roast_bonus=3, 
                           base_cringe_resistance_bonus=0, base_drip_bonus=1),
                           
                    WaifuType(name="Kuudere", description="Cool and collected", 
                           rarity_id=waifu_common.id, 
                           base_clout_bonus=1, base_roast_bonus=0, 
                           base_cringe_resistance_bonus=3, base_drip_bonus=1),
                           
                    WaifuType(name="Yandere", description="Obsessively in love", 
                           rarity_id=waifu_rare.id, 
                           base_clout_bonus=0, base_roast_bonus=4, 
                           base_cringe_resistance_bonus=2, base_drip_bonus=0),
                           
                    WaifuType(name="Deredere", description="Completely love-struck", 
                           rarity_id=waifu_common.id, 
                           base_clout_bonus=2, base_roast_bonus=0, 
                           base_cringe_resistance_bonus=0, base_drip_bonus=3),
                           
                    WaifuType(name="Dandere", description="Shy and quiet", 
                           rarity_id=waifu_common.id, 
                           base_clout_bonus=0, base_roast_bonus=0, 
                           base_cringe_resistance_bonus=4, base_drip_bonus=1),
                           
                    WaifuType(name="Goddess", description="Divine beauty", 
                           rarity_id=waifu_legendary.id, 
                           base_clout_bonus=5, base_roast_bonus=3, 
                           base_cringe_resistance_bonus=3, base_drip_bonus=5)
                ]
                
                db.session.add_all(waifu_types)
                db.session.commit()
                
                # Create item types
                # Character items
                headwear = ItemType(name="Sigma Headphones", description="Noise cancelling for ignoring society",
                              rarity_id=rare.id, slot="head", is_character_item=True,
                              base_clout_bonus=2, base_roast_bonus=0, 
                              base_cringe_resistance_bonus=3, base_drip_bonus=1)
                              
                sunglasses = ItemType(name="Chad Shades", description="For looking cool in any situation",
                                rarity_id=common.id, slot="face", is_character_item=True,
                                base_clout_bonus=1, base_roast_bonus=0, 
                                base_cringe_resistance_bonus=1, base_drip_bonus=3)
                                
                jacket = ItemType(name="Based Jacket", description="Show everyone you're based",
                            rarity_id=rare.id, slot="body", is_character_item=True,
                            base_clout_bonus=3, base_roast_bonus=2, 
                            base_cringe_resistance_bonus=0, base_drip_bonus=3)
                
                # Waifu items
                hair_ribbon = ItemType(name="Cute Ribbon", description="Adorable hair accessory",
                                rarity_id=common.id, slot="head", is_character_item=False,
                                base_clout_bonus=0, base_roast_bonus=0, 
                                base_cringe_resistance_bonus=1, base_drip_bonus=2)
                                
                pendant = ItemType(name="Heart Pendant", description="Lovely necklace",
                             rarity_id=rare.id, slot="neck", is_character_item=False,
                             base_clout_bonus=2, base_roast_bonus=0, 
                             base_cringe_resistance_bonus=0, base_drip_bonus=3)
                
                db.session.add_all([headwear, sunglasses, jacket, hair_ribbon, pendant])
                db.session.commit()
                
                print("Database initialized with seed data.")
            else:
                print("Seed data already exists.")
            
            # Create admin user if it doesn't exist
            admin = User.query.filter_by(username="admin").first()
            if not admin:
                admin = User(
                    username="admin",
                    email="admin@chadbattles.fun",
                    is_admin=True,
                    is_verified=True,
                    chadcoin_balance=1000,
                    created_at=datetime.utcnow()
                )
                admin.set_password("admin")  # Should be changed immediately in production
                db.session.add(admin)
                db.session.commit()
                print("Admin user created.")
            
            print("Database initialization complete!")
            return True
            
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        return False

if __name__ == "__main__":
    # Get environment from command line if provided
    env = 'production'
    if len(sys.argv) > 1:
        env = sys.argv[1]
    
    success = setup_deployment_db(env)
    
    if not success:
        print("Database initialization failed!")
        sys.exit(1)
    else:
        print("Database initialization completed successfully!") 