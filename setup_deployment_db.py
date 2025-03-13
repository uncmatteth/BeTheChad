"""
Setup script for deployment database initialization.
This script initializes a minimal database for deployment without blockchain dependencies.
"""
from app import create_app, db
from app.models.user import User
from app.models.chad import Chad, ChadClass
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
    
    # Set a default SQLite database URI if DATABASE_URL is not set
    if 'DATABASE_URL' not in os.environ:
        print("DATABASE_URL not found, using SQLite database for deployment")
        os.environ['DATABASE_URL'] = 'sqlite:///app.db'
    
    try:
        app = create_app(env)
        
        with app.app_context():
            print("Creating database tables...")
            # Create tables
            db.create_all()
            print("Tables created successfully.")
            
            # Check if we need to add seed data
            if ItemRarity.query.count() == 0:
                print("Adding seed data for rarities and types...")
                
                # Create item rarities
                print("Creating ItemRarity entries...")
                common = ItemRarity(name="Common", description="Common items with basic stats", drop_rate=0.6, min_stat_bonus=1, max_stat_bonus=3)
                rare = ItemRarity(name="Rare", description="Rare items with improved stats", drop_rate=0.3, min_stat_bonus=2, max_stat_bonus=5)
                epic = ItemRarity(name="Epic", description="Epic items with powerful stats", drop_rate=0.09, min_stat_bonus=3, max_stat_bonus=8)
                legendary = ItemRarity(name="Legendary", description="Legendary items with amazing stats", drop_rate=0.01, min_stat_bonus=5, max_stat_bonus=12)

                db.session.add_all([common, rare, epic, legendary])
                db.session.commit()
                
                # Create waifu rarities
                print("Creating WaifuRarity entries...")
                waifu_common = WaifuRarity(name="Common", description="Common waifus", drop_rate=0.6, min_stat_bonus=1, max_stat_bonus=3)
                waifu_rare = WaifuRarity(name="Rare", description="Rare waifus", drop_rate=0.3, min_stat_bonus=2, max_stat_bonus=5)
                waifu_epic = WaifuRarity(name="Epic", description="Epic waifus", drop_rate=0.09, min_stat_bonus=3, max_stat_bonus=8)
                waifu_legendary = WaifuRarity(name="Legendary", description="Legendary waifus", drop_rate=0.01, min_stat_bonus=5, max_stat_bonus=12)

                db.session.add_all([waifu_common, waifu_rare, waifu_epic, waifu_legendary])
                db.session.commit()
                
                # Create chad classes
                print("Creating ChadClass entries...")
                sigma = ChadClass(name="Sigma", description="The lone wolf who follows his own path.", 
                               base_clout_bonus=10, base_roast_bonus=8, base_cringe_resistance_bonus=7, base_drip_bonus=5)
                alpha = ChadClass(name="Alpha", description="The classic leader of the pack.", 
                               base_clout_bonus=7, base_roast_bonus=10, base_cringe_resistance_bonus=5, base_drip_bonus=8)
                giga = ChadClass(name="Giga", description="Absolute unit of a Chad.", 
                              base_clout_bonus=8, base_roast_bonus=5, base_cringe_resistance_bonus=10, base_drip_bonus=7)

                db.session.add_all([sigma, alpha, giga])
                db.session.commit()

                # Create item types
                print("Creating ItemType entries...")
                weapon = ItemType(name="Weapon", description="Increases roast power", 
                                 rarity_id=common.id, slot="weapon", 
                                 base_clout_bonus=1, base_roast_bonus=3, 
                                 base_cringe_resistance_bonus=0, base_drip_bonus=1,
                                 is_character_item=True)
                                 
                armor = ItemType(name="Armor", description="Increases cringe resistance", 
                                rarity_id=common.id, slot="armor", 
                                base_clout_bonus=1, base_roast_bonus=0, 
                                base_cringe_resistance_bonus=3, base_drip_bonus=1,
                                is_character_item=True)
                                
                accessory = ItemType(name="Accessory", description="Increases drip factor", 
                                    rarity_id=rare.id, slot="accessory", 
                                    base_clout_bonus=2, base_roast_bonus=0, 
                                    base_cringe_resistance_bonus=0, base_drip_bonus=3,
                                    is_character_item=True)
                
                db.session.add_all([weapon, armor, accessory])
                db.session.commit()
                
                # Create waifu types
                print("Creating WaifuType entries...")
                tsundere = WaifuType(name="Tsundere", description="Harsh outside, sweet inside",
                                   rarity_id=waifu_common.id,
                                   base_clout_bonus=1, base_roast_bonus=3, 
                                   base_cringe_resistance_bonus=0, base_drip_bonus=1)
                                   
                kuudere = WaifuType(name="Kuudere", description="Cool and collected",
                                  rarity_id=waifu_common.id,
                                  base_clout_bonus=1, base_roast_bonus=0, 
                                  base_cringe_resistance_bonus=3, base_drip_bonus=1)
                                  
                dandere = WaifuType(name="Dandere", description="Shy and quiet",
                                  rarity_id=waifu_common.id,
                                  base_clout_bonus=0, base_roast_bonus=0, 
                                  base_cringe_resistance_bonus=3, base_drip_bonus=2)
                                  
                deredere = WaifuType(name="Deredere", description="Totally love-struck",
                                   rarity_id=waifu_rare.id,
                                   base_clout_bonus=2, base_roast_bonus=0, 
                                   base_cringe_resistance_bonus=0, base_drip_bonus=3)
                
                db.session.add_all([tsundere, kuudere, dandere, deredere])
                db.session.commit()
                
                print("Seed data creation complete.")
            else:
                print("Seed data already exists, skipping creation.")
            
            # Check if admin user exists
            admin = User.query.filter_by(username="admin").first()
            if not admin:
                print("Creating admin user...")
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
            else:
                print("Admin user already exists.")
            
            print("Database initialization complete!")
            return True
            
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()
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