"""
Setup script for deployment database initialization.
This script initializes a minimal database for deployment without blockchain dependencies.
"""
from app import create_app, db
import os
import sys
import random
from datetime import datetime
import traceback
import sqlalchemy
import uuid

def setup_deployment_db(env='production'):
    """Initialize the database with minimal required data.
    
    Args:
        env (str): The environment to run in (development, testing, production)
    """
    print(f"Starting database initialization for {env} environment...")
    
    # Check if DATABASE_URL is set and print its format (without credentials)
    if 'DATABASE_URL' in os.environ:
        db_url = os.environ['DATABASE_URL']
        # Mask the credentials in the URL for safe logging
        masked_url = db_url
        if '@' in db_url:
            # Format: postgresql://username:password@host:port/dbname
            parts = db_url.split('@')
            protocol_and_creds = parts[0].split('://')
            masked_url = f"{protocol_and_creds[0]}://****:****@{parts[1]}"
        print(f"Using DATABASE_URL: {masked_url}")
        
        # Handle postgres:// vs postgresql:// in the URL
        if db_url.startswith('postgres://'):
            fixed_url = db_url.replace('postgres://', 'postgresql://', 1)
            os.environ['DATABASE_URL'] = fixed_url
            print("Updated DATABASE_URL to use postgresql:// prefix")
    else:
        print("WARNING: DATABASE_URL not found, using SQLite database for deployment")
        os.environ['DATABASE_URL'] = 'sqlite:///app.db'
    
    try:
        print("Creating application instance...")
        app = create_app(env)
        
        with app.app_context():
            # Create all tables - ensure this is done directly with the target database
            print("Creating database tables...")
            db.create_all()
            
            # Check if the user table exists and has rows
            inspector = sqlalchemy.inspect(db.engine)
            if inspector.has_table('users'):
                user_count = db.session.query(sqlalchemy.func.count('*')).select_from(db.Model.metadata.tables['users']).scalar()
                if user_count > 0:
                    print(f"Database already initialized with {user_count} users. Skipping further initialization.")
                    return

            print("Populating database with initial data...")
            
            # Create rarities
            from app.models.item import ItemRarity
            create_rarities(ItemRarity)
            
            from app.models.waifu import WaifuRarity
            create_rarities(WaifuRarity)
            
            # Create default admin user if no users exist
            from app.models.user import User
            if User.query.count() == 0:
                create_admin_user()
            
            # Create waifu types
            create_waifu_types()
            
            # Create item types
            create_item_types()
                        
            # Commit all changes
            db.session.commit()
            print("Database initialization complete!")
            
    except Exception as e:
        print(f"ERROR: Database initialization failed: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

def create_admin_user():
    """Create an admin user for the application."""
    from app.models.user import User
    from app import db
    from werkzeug.security import generate_password_hash
    import os
    
    print("Creating admin user...")
    
    # Check if admin user already exists
    if User.query.filter_by(username='admin').first():
        print("Admin user already exists")
        return
    
    # Generate a random secure password or use environment variable
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin_' + str(uuid.uuid4())[:8])
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@chadbattles.fun',
        display_name='Admin',
        password_hash=generate_password_hash(admin_password),
        chadcoin_balance=10000,
        is_admin=True
    )
    
    # Add to session and flush (but don't commit yet)
    db.session.add(admin)
    db.session.flush()
    
    print(f"Admin user created with username: admin, password: {admin_password}")
    print("IMPORTANT: Make note of this password or set ADMIN_PASSWORD environment variable!")
    
    # Create a default Chad class
    create_default_chad_class()
    
    # Create a Chad for the admin
    create_chad_for_user(admin)


def create_default_chad_class():
    """Create default Chad classes."""
    from app.models.chad import ChadClass
    from app import db
    
    print("Creating default Chad classes...")
    
    # Check if classes already exist
    if ChadClass.query.count() > 0:
        print("Chad classes already exist")
        return
    
    # Create default classes
    classes = [
        ChadClass(
            name='Sigma',
            description='Lone wolves with exceptional focus and determination.',
            base_clout_bonus=15,
            base_roast_bonus=10,
            base_cringe_resistance_bonus=15,
            base_drip_bonus=10
        ),
        ChadClass(
            name='Alpha',
            description='Natural leaders with charisma and confidence.',
            base_clout_bonus=20,
            base_roast_bonus=15,
            base_cringe_resistance_bonus=10,
            base_drip_bonus=15
        ),
        ChadClass(
            name='Gigachad',
            description='Legendary individuals with unparalleled status.',
            base_clout_bonus=25,
            base_roast_bonus=25,
            base_cringe_resistance_bonus=25,
            base_drip_bonus=25
        ),
        ChadClass(
            name='Meme Overlord',
            description='Masters of internet culture who weaponize viral content.',
            base_clout_bonus=20,
            base_roast_bonus=25,
            base_cringe_resistance_bonus=10,
            base_drip_bonus=15
        ),
        ChadClass(
            name='Crypto Knight',
            description='Digital asset warriors who live by the blockchain.',
            base_clout_bonus=15,
            base_roast_bonus=15,
            base_cringe_resistance_bonus=20,
            base_drip_bonus=20
        ),
        ChadClass(
            name='Ratio King',
            description='Social media tacticians who dominate conversations.',
            base_clout_bonus=25,
            base_roast_bonus=20,
            base_cringe_resistance_bonus=15,
            base_drip_bonus=10
        ),
        ChadClass(
            name='Normie Chad',
            description='Balanced individuals who excel in conventional situations.',
            base_clout_bonus=15,
            base_roast_bonus=15,
            base_cringe_resistance_bonus=15,
            base_drip_bonus=15
        ),
        # New classes
        ChadClass(
            name='KOL',
            description='Key Opinion Leaders who shape trends and influence the masses.',
            base_clout_bonus=30,
            base_roast_bonus=15,
            base_cringe_resistance_bonus=10,
            base_drip_bonus=25
        ),
        ChadClass(
            name='Tech Bro',
            description='Startup enthusiasts who disrupt industries and scale exponentially.',
            base_clout_bonus=20,
            base_roast_bonus=10,
            base_cringe_resistance_bonus=15,
            base_drip_bonus=25
        ),
        ChadClass(
            name='Gym Rat',
            description='Fitness devotees who maximize physical potential and protein intake.',
            base_clout_bonus=15,
            base_roast_bonus=20,
            base_cringe_resistance_bonus=20,
            base_drip_bonus=15
        ),
        ChadClass(
            name='Debate Lord',
            description='Masters of rhetoric who never lose an argument, online or offline.',
            base_clout_bonus=10,
            base_roast_bonus=30,
            base_cringe_resistance_bonus=25,
            base_drip_bonus=5
        ),
        ChadClass(
            name='Diamond Hands',
            description='Unshakeable investors who never sell, regardless of market conditions.',
            base_clout_bonus=25,
            base_roast_bonus=15,
            base_cringe_resistance_bonus=30,
            base_drip_bonus=10
        ),
        ChadClass(
            name='Lore Master',
            description='Knowledge keepers with encyclopedic understanding of niche subjects.',
            base_clout_bonus=15,
            base_roast_bonus=25,
            base_cringe_resistance_bonus=20,
            base_drip_bonus=10
        ),
        # Anti-gaming system classes
        ChadClass(
            name='Clown',
            description='Detected trying to game the system. Nice try, but we see through your act.',
            base_clout_bonus=5,
            base_roast_bonus=5,
            base_cringe_resistance_bonus=0,
            base_drip_bonus=0
        ),
        ChadClass(
            name='Newbie',
            description='Fresh to the scene with potential yet to be realized.',
            base_clout_bonus=10,
            base_roast_bonus=10,
            base_cringe_resistance_bonus=10,
            base_drip_bonus=10
        ),
        # Special rare class
        ChadClass(
            name='Blockchain Detective',
            description='Elite on-chain sleuths with proven track records of digital investigation.',
            base_clout_bonus=35,
            base_roast_bonus=20,
            base_cringe_resistance_bonus=35,
            base_drip_bonus=20
        )
    ]
    
    # Add all classes to session (but don't commit yet)
    for chad_class in classes:
        db.session.add(chad_class)
    
    # Flush to get IDs but don't commit yet
    db.session.flush()
    print(f"Created {len(classes)} Chad classes")


def create_chad_for_user(user):
    """Create a Chad character for a user."""
    from app.models.chad import Chad, ChadClass
    from app import db
    
    print(f"Creating Chad for user: {user.username}")
    
    # Check if user already has a Chad
    if hasattr(user, 'chad') and user.chad:
        print(f"User {user.username} already has a Chad")
        return
    
    # Get Gigachad class (or create it if not exists)
    gigachad_class = ChadClass.query.filter_by(name='Gigachad').first()
    if not gigachad_class:
        # If we don't have classes yet, create them
        create_default_chad_class()
        gigachad_class = ChadClass.query.filter_by(name='Gigachad').first()
    
    # Create Chad for user
    chad = Chad(
        user_id=user.id,
        class_id=gigachad_class.id,
        name=f"{user.username}'s Chad",
        level=10,
        xp=500,
        clout=50,
        roast_level=50,
        cringe_resistance=50,
        drip_factor=50
    )
    
    # Add to session (but don't commit yet)
    db.session.add(chad)
    db.session.flush()
    print(f"Created Chad for user {user.username}")


def create_rarities(rarity_model):
    """Create item or waifu rarities."""
    from app import db
    
    model_name = rarity_model.__name__
    print(f"Creating {model_name} rarities...")
    
    # Check if rarities already exist
    if rarity_model.query.count() > 0:
        print(f"{model_name} rarities already exist")
        return
    
    # Create rarities
    rarities = [
        rarity_model(
            name='Common',
            description='Most frequently found items, basic stats.',
            drop_rate=0.7,
            min_stat_bonus=1,
            max_stat_bonus=5
        ),
        rarity_model(
            name='Uncommon',
            description='Less common items with decent stats.',
            drop_rate=0.2,
            min_stat_bonus=3,
            max_stat_bonus=10
        ),
        rarity_model(
            name='Rare',
            description='Hard to find items with good stats.',
            drop_rate=0.07,
            min_stat_bonus=5,
            max_stat_bonus=15
        ),
        rarity_model(
            name='Epic',
            description='Very rare items with excellent stats.',
            drop_rate=0.02,
            min_stat_bonus=10,
            max_stat_bonus=20
        ),
        rarity_model(
            name='Legendary',
            description='Extremely rare items with exceptional stats.',
            drop_rate=0.01,
            min_stat_bonus=15,
            max_stat_bonus=30
        )
    ]
    
    # Add all rarities to session
    for rarity in rarities:
        db.session.add(rarity)
    
    # Flush to get IDs but don't commit yet
    db.session.flush()
    print(f"Created {len(rarities)} {model_name} rarities")


def create_waifu_types():
    """Create waifu types."""
    from app.models.waifu import WaifuType, WaifuRarity
    from app import db
    
    print("Creating waifu types...")
    
    # Check if waifu types already exist
    if WaifuType.query.count() > 0:
        print("Waifu types already exist")
        return
    
    # Get rarities
    rarities = {r.name: r for r in WaifuRarity.query.all()}
    if not rarities:
        print("No rarities found, skipping waifu type creation")
        return
    
    # Create some default waifu types
    waifu_types = [
        WaifuType(
            name='Yandere',
            description='Intensely devoted and a bit dangerous.',
            rarity_id=rarities['Epic'].id,
            clout_bonus=15,
            roast_bonus=20,
            cringe_resistance_bonus=5,
            drip_bonus=10
        ),
        WaifuType(
            name='Tsundere',
            description='Tough on the outside, sweet on the inside.',
            rarity_id=rarities['Rare'].id,
            clout_bonus=10,
            roast_bonus=15,
            cringe_resistance_bonus=10,
            drip_bonus=10
        ),
        WaifuType(
            name='Gamer Girl',
            description='Loves games and competitive play.',
            rarity_id=rarities['Uncommon'].id,
            clout_bonus=12,
            roast_bonus=8,
            cringe_resistance_bonus=15,
            drip_bonus=5
        ),
        WaifuType(
            name='E-Girl',
            description='Internet personality with a unique aesthetic.',
            rarity_id=rarities['Common'].id,
            clout_bonus=10,
            roast_bonus=5,
            cringe_resistance_bonus=5,
            drip_bonus=15
        ),
        WaifuType(
            name='A.I. Waifu',
            description='Advanced artificial intelligence companion.',
            rarity_id=rarities['Legendary'].id,
            clout_bonus=25,
            roast_bonus=25,
            cringe_resistance_bonus=20,
            drip_bonus=20
        )
    ]
    
    # Add all waifu types to session
    for waifu_type in waifu_types:
        db.session.add(waifu_type)
    
    # Flush to get IDs but don't commit yet
    db.session.flush()
    print(f"Created {len(waifu_types)} waifu types")


def create_item_types():
    """Create item types."""
    from app.models.item import ItemType, ItemRarity
    from app import db
    
    print("Creating item types...")
    
    # Check if item types already exist
    if ItemType.query.count() > 0:
        print("Item types already exist")
        return
    
    # Get rarities
    rarities = {r.name: r for r in ItemRarity.query.all()}
    if not rarities:
        print("No rarities found, skipping item type creation")
        return
    
    # Create some default item types
    item_types = [
        # Character items
        ItemType(
            name='Bitcoin Cap',
            description='Shows your crypto enthusiasm.',
            rarity_id=rarities['Common'].id,
            slot='head',
            base_clout_bonus=5,
            base_roast_bonus=0,
            base_cringe_resistance_bonus=0,
            base_drip_bonus=5,
            is_character_item=True
        ),
        ItemType(
            name='Diamond Hands',
            description='HODL with style.',
            rarity_id=rarities['Epic'].id,
            slot='accessory',
            base_clout_bonus=15,
            base_roast_bonus=5,
            base_cringe_resistance_bonus=10,
            base_drip_bonus=10,
            is_character_item=True
        ),
        ItemType(
            name='Meme Shirt',
            description='The freshest memes printed on cotton.',
            rarity_id=rarities['Uncommon'].id,
            slot='body',
            base_clout_bonus=5,
            base_roast_bonus=10,
            base_cringe_resistance_bonus=5,
            base_drip_bonus=5,
            is_character_item=True
        ),
        
        # Waifu items
        ItemType(
            name='Kawaii Bow',
            description='Cute accessory for your waifu.',
            rarity_id=rarities['Common'].id,
            slot='head',
            base_clout_bonus=3,
            base_roast_bonus=0,
            base_cringe_resistance_bonus=2,
            base_drip_bonus=5,
            is_character_item=False
        ),
        ItemType(
            name='Battle Armor',
            description='Protection with style.',
            rarity_id=rarities['Rare'].id,
            slot='body',
            base_clout_bonus=8,
            base_roast_bonus=5,
            base_cringe_resistance_bonus=12,
            base_drip_bonus=5,
            is_character_item=False
        ),
        ItemType(
            name='Magical Amulet',
            description='Contains mysterious powers.',
            rarity_id=rarities['Legendary'].id,
            slot='accessory',
            base_clout_bonus=20,
            base_roast_bonus=15,
            base_cringe_resistance_bonus=15,
            base_drip_bonus=15,
            is_character_item=False
        )
    ]
    
    # Add all item types to session
    for item_type in item_types:
        db.session.add(item_type)
    
    # Flush to get IDs but don't commit yet
    db.session.flush()
    print(f"Created {len(item_types)} item types")


if __name__ == "__main__":
    # Get environment from command line or default to production
    env = sys.argv[1] if len(sys.argv) > 1 else 'production'
    if env not in ['development', 'testing', 'production']:
        print(f"Invalid environment: {env}")
        print("Usage: python setup_deployment_db.py [development|testing|production]")
        sys.exit(1)
        
    setup_deployment_db(env) 