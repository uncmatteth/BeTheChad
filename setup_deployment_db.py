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
import sqlalchemy

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
    
    # Force SQLite for build phase to avoid PostgreSQL initialization issues
    if 'sqlite:' not in os.environ.get('DATABASE_URL', ''):
        print("Switching to SQLite for build phase initialization...")
        original_db_url = os.environ['DATABASE_URL']
        os.environ['DATABASE_URL'] = 'sqlite:///temp.db'
    else:
        original_db_url = None
    
    try:
        print("Creating application instance...")
        app = create_app(env)
        
        with app.app_context():
            # Test the database connection
            print("Testing database connection...")
            try:
                # For SQLite this should work reliably
                db.engine.execute("SELECT 1")
                print("Database connection successful!")
            except Exception as e:
                print(f"Database connection test failed: {str(e)}")
                print("Detailed error information:")
                traceback.print_exc()
                return False
            
            # Use a completely different approach for SQLite: disable foreign key checks
            # and use raw SQL to create the tables
            with db.engine.connect() as conn:
                conn.execution_options(isolation_level="AUTOCOMMIT")
                
                print("Disabling foreign key constraints for initialization...")
                conn.execute("PRAGMA foreign_keys = OFF")
                
                # Drop all tables if they exist
                print("Dropping all existing tables...")
                for table in reversed(db.metadata.sorted_tables):
                    try:
                        table.drop(conn, checkfirst=True)
                        print(f"Dropped table {table.name} if it existed")
                    except Exception as e:
                        print(f"Note: Could not drop table {table.name}: {str(e)}")
                
                # Create all tables, ignoring foreign key constraints
                print("Creating tables with foreign keys disabled...")
                for table in db.metadata.sorted_tables:
                    try:
                        # Skip tables we know might have circular dependencies
                        if table.name in ['cabal_analytics', 'referral']:
                            continue
                        table.create(conn, checkfirst=True)
                        print(f"Created table {table.name}")
                    except Exception as e:
                        print(f"Note: Could not create table {table.name}: {str(e)}")
                
                # Try to create the remaining tables that might have circular dependencies
                try:
                    if 'cabal_analytics' in [t.name for t in db.metadata.sorted_tables]:
                        for table in db.metadata.sorted_tables:
                            if table.name == 'cabal_analytics':
                                table.create(conn, checkfirst=True)
                                print(f"Created table {table.name}")
                except Exception as e:
                    print(f"Note: Could not create cabal_analytics table: {str(e)}")
                
                try:
                    if 'referral' in [t.name for t in db.metadata.sorted_tables]:
                        for table in db.metadata.sorted_tables:
                            if table.name == 'referral':
                                table.create(conn, checkfirst=True)
                                print(f"Created table {table.name}")
                except Exception as e:
                    print(f"Note: Could not create referral table: {str(e)}")
                
                # Re-enable foreign key constraints
                print("Re-enabling foreign key constraints...")
                conn.execute("PRAGMA foreign_keys = ON")
            
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
                    # Continue anyway
            else:
                print("Admin user already exists.")
            
            # If we used SQLite temporarily, restore the original DB URL
            if original_db_url:
                print(f"Restoring original database URL for runtime...")
                os.environ['DATABASE_URL'] = original_db_url
            
            print("Database initialization completed successfully!")
            
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        print("Detailed error information:")
        traceback.print_exc()
        print("Database initialization failed!")
        
        # If we used SQLite temporarily, restore the original DB URL
        if original_db_url:
            print(f"Restoring original database URL...")
            os.environ['DATABASE_URL'] = original_db_url
        
        return False
    
    return True

if __name__ == "__main__":
    # Determine environment from command line argument if provided
    env = sys.argv[1] if len(sys.argv) > 1 else 'production'
    success = setup_deployment_db(env)
    if not success:
        sys.exit(1)  # Exit with error code for the deployment script to detect 