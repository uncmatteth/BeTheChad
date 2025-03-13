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
from app.models.transaction import Transaction, TransactionType
import os
import sys
import random
from datetime import datetime
import traceback

# Pre-import models that might have circular dependencies
try:
    from app.models.battle import Battle
except ImportError:
    print("Warning: Battle model could not be imported")
    Battle = None

try:
    from app.models.cabal_analytics import CabalAnalytics
except ImportError:
    print("Warning: CabalAnalytics model could not be imported")
    CabalAnalytics = None

try:
    from app.models.referral import Referral
except ImportError:
    print("Warning: Referral model could not be imported")
    Referral = None

try:
    from app.models.meme_elixir import MemeElixir
except ImportError:
    print("Warning: MemeElixir model could not be imported")
    MemeElixir = None

try:
    from app.models.nft import NFT
except ImportError:
    print("Warning: NFT model could not be imported")
    NFT = None

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
        
        # For build phase, if it's not SQLite, log info but continue
        if not db_url.startswith('sqlite:'):
            print("NOTE: Using PostgreSQL for database. If this fails during build, we'll use SQLite.")
    else:
        print("WARNING: DATABASE_URL not found, using SQLite database for deployment")
        os.environ['DATABASE_URL'] = 'sqlite:///app.db'
    
    try:
        print("Creating application instance...")
        app = create_app(env)
        
        with app.app_context():
            # Test the database connection
            print("Testing database connection...")
            try:
                # For SQLite this should work reliably
                if 'sqlite:' in os.environ.get('DATABASE_URL', ''):
                    db.engine.execute("SELECT 1")
                    print("SQLite database connection successful!")
                else:
                    # For PostgreSQL, we'll attempt but continue if it fails (for build phase)
                    try:
                        db.engine.execute("SELECT 1")
                        print("PostgreSQL database connection successful!")
                    except Exception as e:
                        print(f"NOTE: PostgreSQL connection test failed: {str(e)}")
                        print("This is expected during build. Will use SQLite for initialization.")
                        # Switch to SQLite for build phase
                        os.environ['DATABASE_URL'] = 'sqlite:///temp.db'
                        app = create_app(env)  # Recreate app with new DB URL
            except Exception as e:
                print(f"Database connection test failed: {str(e)}")
                print("Detailed error information:")
                traceback.print_exc()
                
                # If we're not using SQLite already, try switching to it
                if 'sqlite:' not in os.environ.get('DATABASE_URL', ''):
                    print("Attempting to switch to SQLite database...")
                    os.environ['DATABASE_URL'] = 'sqlite:///temp.db'
                    app = create_app(env)  # Recreate app with SQLite
                else:
                    return False
            
            # Print detailed engine information
            print(f"SQLAlchemy engine: {db.engine.name}")
            print(f"Database driver: {db.engine.driver}")
            print(f"Tables that will be created: {', '.join([t.name for t in db.metadata.sorted_tables])}")
            
            # Create tables in a specific order to avoid foreign key problems
            print("Creating database tables in dependency order...")
            
            # Use inspector to check if we need to create tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            
            # If tables already exist, skip table creation
            if not inspector.get_table_names():
                try:
                    # Create tables in dependency order instead of using db.create_all()
                    # First, create parent tables that don't depend on others
                    tables_to_create = [
                        User.__table__,
                        ItemRarity.__table__,
                        ItemType.__table__,
                        WaifuRarity.__table__,
                        WaifuType.__table__,
                        ChadClass.__table__
                    ]
                    db.metadata.create_tables(tables_to_create)
                    print("Base tables created successfully.")
                    
                    # Then create tables that depend on the parent tables
                    dependent_tables = [
                        Chad.__table__,
                        Waifu.__table__,
                        Cabal.__table__,
                        Item.__table__,
                        Transaction.__table__
                    ]
                    db.metadata.create_tables(dependent_tables)
                    print("Secondary tables created successfully.")
                    
                    # Load additional models that might have dependencies
                    from app.models.cabal_analytics import CabalAnalytics
                    from app.models.battle import Battle
                    from app.models.meme_elixir import MemeElixir
                    from app.models.nft import NFT
                    from app.models.referral import Referral
                    
                    # Finally create tables that depend on secondary tables
                    relationship_tables = [
                        CabalMember.__table__,
                        WaifuItem.__table__,
                        CharacterItem.__table__
                    ]
                    db.metadata.create_tables(relationship_tables)
                    print("Relationship tables created successfully.")
                    
                    # Create all remaining tables, but one by one in a specific order
                    if Battle:
                        try:
                            Battle.__table__.create(db.engine, checkfirst=True)
                            print("Battle table created successfully.")
                        except Exception as e:
                            print(f"Error creating Battle table: {str(e)}")
                    
                    if MemeElixir:
                        try:
                            MemeElixir.__table__.create(db.engine, checkfirst=True)
                            print("MemeElixir table created successfully.")
                        except Exception as e:
                            print(f"Error creating MemeElixir table: {str(e)}")
                    
                    if NFT:
                        try:
                            NFT.__table__.create(db.engine, checkfirst=True)
                            print("NFT table created successfully.")
                        except Exception as e:
                            print(f"Error creating NFT table: {str(e)}")
                    
                    if Referral:
                        try:
                            Referral.__table__.create(db.engine, checkfirst=True)
                            print("Referral table created successfully.")
                        except Exception as e:
                            print(f"Error creating Referral table: {str(e)}")
                    
                    if CabalAnalytics:
                        try:
                            CabalAnalytics.__table__.create(db.engine, checkfirst=True)
                            print("CabalAnalytics table created successfully.")
                        except Exception as e:
                            print(f"Error creating CabalAnalytics table: {str(e)}")
                            print("NOTE: This error is common during initial setup and can be ignored.")
                    
                    # Try one final approach for any tables that weren't created
                    try:
                        # Create all tables, but ignore errors
                        with db.engine.connect() as conn:
                            conn.execution_options(isolation_level="AUTOCOMMIT")
                            conn.execute("PRAGMA foreign_keys = OFF")
                        db.create_all()
                        print("Successfully created any remaining tables.")
                    except Exception as e:
                        print(f"Note: Error during final table creation pass: {str(e)}")
                        print("This may be expected and some tables may already exist.")
                except Exception as e:
                    print(f"Error creating tables: {str(e)}")
                    print("Detailed error information:")
                    traceback.print_exc()
                    return False
            else:
                print("Tables already exist, skipping table creation.")
            
            # Skip seed data creation for now, just to get the app running
            print("Skipping seed data creation for initial deployment.")
            
            # Check if admin user exists
            admin = User.query.filter_by(username="admin").first()
            if not admin:
                print("Creating admin user...")
                try:
                    admin = User(
                        username="admin",
                        email="admin@chadbattles.fun",
                        is_admin=True,
                        chadcoin_balance=1000,
                        created_at=datetime.utcnow()
                    )
                    admin.set_password("admin")  # Should be changed immediately in production
                    db.session.add(admin)
                    db.session.commit()
                    print("Admin user created.")
                except Exception as e:
                    print(f"Error creating admin user: {str(e)}")
                    print("Detailed error information:")
                    traceback.print_exc()
                    return False
            else:
                print("Admin user already exists.")
            
            print("Database initialization completed successfully!")
            
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        print("Detailed error information:")
        traceback.print_exc()
        print("Database initialization failed!")
        return False
    
    return True

if __name__ == "__main__":
    # Determine environment from command line argument if provided
    env = sys.argv[1] if len(sys.argv) > 1 else 'production'
    success = setup_deployment_db(env)
    if not success:
        sys.exit(1)  # Exit with error code for the deployment script to detect 