"""
Special setup script for Render.com deployment.
This script handles database initialization safely for deployment.
"""
import os
import sys
import time
import sqlalchemy
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Wait for PostgreSQL to be fully available (common issue with fresh deployments)
def wait_for_postgres():
    """Wait for PostgreSQL to become available."""
    from sqlalchemy import create_engine
    from sqlalchemy.exc import OperationalError
    import psycopg2
    
    logger.info("Checking PostgreSQL connection...")
    
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        logger.error("No DATABASE_URL environment variable found")
        return False
    
    # Handle postgres:// vs postgresql:// in the URL
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
        logger.info("Updated DATABASE_URL to use postgresql:// prefix")
    
    retries = 5
    retry_interval = 3  # seconds
    
    # Print DB URL (obscured password)
    masked_url = db_url
    if '@' in db_url:
        # Format: postgresql://username:password@host:port/dbname
        parts = db_url.split('@')
        protocol_and_creds = parts[0].split('://')
        masked_url = f"{protocol_and_creds[0]}://****:****@{parts[1]}"
    logger.info(f"Using DATABASE_URL: {masked_url}")
    
    for i in range(retries):
        try:
            logger.info(f"Connection attempt {i+1}/{retries}...")
            
            # Try connecting with psycopg2 directly first
            try:
                parsed = sqlalchemy.engine.url.make_url(db_url)
                user = parsed.username
                password = parsed.password
                host = parsed.host
                port = parsed.port or 5432
                database = parsed.database
                
                logger.info(f"Connecting to PostgreSQL at {host}:{port}/{database}")
                
                conn = psycopg2.connect(
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                    database=database
                )
                conn.close()
                logger.info("PostgreSQL connection successful!")
                return True
            except Exception as e:
                logger.warning(f"Direct psycopg2 connection failed: {e}")
            
            # Try SQLAlchemy as fallback
            engine = create_engine(db_url)
            connection = engine.connect()
            connection.close()
            logger.info("PostgreSQL connection successful!")
            return True
        except (OperationalError, psycopg2.OperationalError) as e:
            logger.warning(f"PostgreSQL not available yet: {e}")
            if i < retries - 1:
                logger.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
    
    logger.error(f"Failed to connect to PostgreSQL after {retries} attempts")
    return False

def init_database():
    """Initialize the database and run migrations."""
    if not wait_for_postgres():
        logger.error("Could not establish PostgreSQL connection")
        sys.exit(1)
    
    logger.info("Initializing database...")
    
    try:
        from app import create_app, db
        from flask_migrate import upgrade
        
        app = create_app('production')
        
        with app.app_context():
            # Create all tables
            logger.info("Creating database tables...")
            db.create_all()
            
            # Run migrations
            logger.info("Running migrations...")
            upgrade()
            
            # Check if basic data needs to be added
            from app.models.user import User
            if User.query.count() == 0:
                logger.info("No users found, running initial data setup...")
                from setup_deployment_db import setup_deployment_db
                setup_deployment_db('production')
            else:
                logger.info(f"Database already contains {User.query.count()} users. Skipping initial data setup.")
            
        logger.info("Database initialization completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during database initialization: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    init_database() 