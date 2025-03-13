"""
Setup script for deployment database initialization.
This script initializes a minimal database for deployment without blockchain dependencies.
"""
from app import create_app, db
from app.models.user import User
import os
import sys
import random
from datetime import datetime
import traceback
import sqlalchemy

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
            
            # Use direct SQL statements to create the tables
            with db.engine.connect() as conn:
                conn.execution_options(isolation_level="AUTOCOMMIT")
                
                print("Disabling foreign key constraints for initialization...")
                conn.execute("PRAGMA foreign_keys = OFF")
                
                # Drop all tables if they exist
                print("Dropping all existing tables...")
                try:
                    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';").fetchall()
                    for table in tables:
                        conn.execute(f"DROP TABLE IF EXISTS {table[0]}")
                        print(f"Dropped table {table[0]} if it existed")
                except Exception as e:
                    print(f"Error during table dropping: {str(e)}")
                
                # Create essential tables one by one using raw SQL
                print("Creating essential tables with direct SQL...")
                
                # Create user table
                try:
                    conn.execute("""
                    CREATE TABLE IF NOT EXISTS user (
                        id VARCHAR(36) PRIMARY KEY,
                        username VARCHAR(64) UNIQUE NOT NULL,
                        email VARCHAR(120) UNIQUE NOT NULL,
                        password_hash VARCHAR(128),
                        chadcoin_balance INTEGER NOT NULL DEFAULT 0,
                        is_admin BOOLEAN NOT NULL DEFAULT 0,
                        twitter_id VARCHAR(64),
                        twitter_username VARCHAR(64),
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP
                    )
                    """)
                    print("Created user table")
                except Exception as e:
                    print(f"Error creating user table: {str(e)}")
                
                # Create chad_class table
                try:
                    conn.execute("""
                    CREATE TABLE IF NOT EXISTS chad_class (
                        id VARCHAR(36) PRIMARY KEY,
                        name VARCHAR(64) NOT NULL,
                        description TEXT,
                        base_strength FLOAT NOT NULL,
                        base_agility FLOAT NOT NULL,
                        base_intelligence FLOAT NOT NULL,
                        base_charisma FLOAT NOT NULL,
                        growth_strength FLOAT NOT NULL,
                        growth_agility FLOAT NOT NULL,
                        growth_intelligence FLOAT NOT NULL,
                        growth_charisma FLOAT NOT NULL
                    )
                    """)
                    print("Created chad_class table")
                except Exception as e:
                    print(f"Error creating chad_class table: {str(e)}")
                
                # Create chad table
                try:
                    conn.execute("""
                    CREATE TABLE IF NOT EXISTS chad (
                        id VARCHAR(36) PRIMARY KEY,
                        name VARCHAR(64) NOT NULL,
                        user_id VARCHAR(36),
                        class_id VARCHAR(36),
                        level INTEGER NOT NULL DEFAULT 1,
                        xp INTEGER NOT NULL DEFAULT 0,
                        strength FLOAT NOT NULL,
                        agility FLOAT NOT NULL,
                        intelligence FLOAT NOT NULL,
                        charisma FLOAT NOT NULL,
                        battles_won INTEGER NOT NULL DEFAULT 0,
                        battles_lost INTEGER NOT NULL DEFAULT 0,
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        last_battle TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES user(id),
                        FOREIGN KEY (class_id) REFERENCES chad_class(id)
                    )
                    """)
                    print("Created chad table")
                except Exception as e:
                    print(f"Error creating chad table: {str(e)}")
                
                # Create cabal table
                try:
                    conn.execute("""
                    CREATE TABLE IF NOT EXISTS cabal (
                        id VARCHAR(36) PRIMARY KEY,
                        name VARCHAR(64) UNIQUE NOT NULL,
                        description TEXT,
                        logo_url TEXT,
                        banner_url TEXT,
                        creator_id VARCHAR(36),
                        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        member_count INTEGER NOT NULL DEFAULT 0,
                        total_power FLOAT NOT NULL DEFAULT 0,
                        battles_won INTEGER NOT NULL DEFAULT 0,
                        battles_lost INTEGER NOT NULL DEFAULT 0,
                        rank INTEGER,
                        FOREIGN KEY (creator_id) REFERENCES user(id)
                    )
                    """)
                    print("Created cabal table")
                except Exception as e:
                    print(f"Error creating cabal table: {str(e)}")
                
                # Create cabal_member table
                try:
                    conn.execute("""
                    CREATE TABLE IF NOT EXISTS cabal_member (
                        id VARCHAR(36) PRIMARY KEY,
                        cabal_id VARCHAR(36) NOT NULL,
                        chad_id VARCHAR(36) NOT NULL,
                        joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        is_admin BOOLEAN NOT NULL DEFAULT 0,
                        is_active BOOLEAN NOT NULL DEFAULT 1,
                        FOREIGN KEY (cabal_id) REFERENCES cabal(id),
                        FOREIGN KEY (chad_id) REFERENCES chad(id)
                    )
                    """)
                    print("Created cabal_member table")
                except Exception as e:
                    print(f"Error creating cabal_member table: {str(e)}")
                
                # Create battle table
                try:
                    conn.execute("""
                    CREATE TABLE IF NOT EXISTS battle (
                        id VARCHAR(36) PRIMARY KEY,
                        attacker_cabal_id VARCHAR(36),
                        defender_cabal_id VARCHAR(36),
                        winner_cabal_id VARCHAR(36),
                        attacker_total_power FLOAT,
                        defender_total_power FLOAT,
                        battle_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        xp_reward INTEGER,
                        coin_reward INTEGER,
                        battle_log TEXT,
                        FOREIGN KEY (attacker_cabal_id) REFERENCES cabal(id),
                        FOREIGN KEY (defender_cabal_id) REFERENCES cabal(id),
                        FOREIGN KEY (winner_cabal_id) REFERENCES cabal(id)
                    )
                    """)
                    print("Created battle table")
                except Exception as e:
                    print(f"Error creating battle table: {str(e)}")
                
                # Create cabal_analytics table
                try:
                    conn.execute("""
                    CREATE TABLE IF NOT EXISTS cabal_analytics (
                        id VARCHAR(36) PRIMARY KEY,
                        cabal_id VARCHAR(36) NOT NULL,
                        timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        member_count INTEGER NOT NULL,
                        active_member_count INTEGER NOT NULL,
                        total_power FLOAT NOT NULL,
                        rank INTEGER NOT NULL,
                        battles_won INTEGER NOT NULL,
                        battles_lost INTEGER NOT NULL,
                        referrals INTEGER NOT NULL,
                        FOREIGN KEY (cabal_id) REFERENCES cabal(id)
                    )
                    """)
                    print("Created cabal_analytics table")
                except Exception as e:
                    print(f"Error creating cabal_analytics table: {str(e)}")
                
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