"""
Create test database for running tests.
Run this script before running pytest if the test database doesn't exist.
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_test_database():
    """Create the test database if it doesn't exist."""
    db_name = "chad_battles_test"
    db_user = "postgres"
    db_password = "postgres"
    db_host = "localhost"
    
    # Override with environment variables if they exist
    if os.getenv('TEST_DATABASE_URI'):
        # Parse the database URI
        db_uri = os.getenv('TEST_DATABASE_URI')
        if '@' in db_uri and ':' in db_uri:
            # Extract the credentials and host from the URI
            # Format: postgresql://user:password@host/dbname
            credentials = db_uri.split('@')[0].split('//')[1]
            host_part = db_uri.split('@')[1]
            
            if ':' in credentials:
                db_user, db_password = credentials.split(':')
            
            if '/' in host_part:
                db_host = host_part.split('/')[0]
                db_name = host_part.split('/')[1]
    
    print(f"Attempting to create test database '{db_name}' on host '{db_host}' with user '{db_user}'")
    
    # Connect to the PostgreSQL server
    conn = psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_password
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Create a cursor
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()
    
    if not exists:
        print(f"Creating database '{db_name}'...")
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created successfully!")
    else:
        print(f"Database '{db_name}' already exists.")
    
    # Close the connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_test_database() 