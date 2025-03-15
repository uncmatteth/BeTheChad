import os
import pytest
from app import create_app
from app.extensions import db as _db
from config import TestingConfig
import subprocess
import sqlalchemy
from sqlalchemy import create_engine, text

def create_test_db():
    """Create the test database if it doesn't exist."""
    db_name = "chad_battles_test"
    connection_string = f"postgresql://postgres:postgres@localhost/postgres"
    
    # Create connection to default database
    engine = create_engine(connection_string)
    
    with engine.connect() as conn:
        # Disconnect all active connections to database if exists
        conn.execution_options(isolation_level="AUTOCOMMIT")
        
        # Check if database exists
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
        exists = result.scalar()
        
        if not exists:
            print(f"Creating test database '{db_name}'...")
            conn.execute(text(f"CREATE DATABASE {db_name}"))
            print(f"Database '{db_name}' created successfully!")
        else:
            print(f"Test database '{db_name}' already exists.")

def drop_test_db():
    """Drop the test database if it exists."""
    db_name = "chad_battles_test"
    connection_string = f"postgresql://postgres:postgres@localhost/postgres"
    
    # Create connection to default database
    engine = create_engine(connection_string)
    
    with engine.connect() as conn:
        # Disconnect all active connections to database if exists
        conn.execution_options(isolation_level="AUTOCOMMIT")
        
        # Check if database exists
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
        exists = result.scalar()
        
        if exists:
            print(f"Closing all connections to '{db_name}'...")
            conn.execute(text(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{db_name}'
                AND pid <> pg_backend_pid()
            """))
            
            print(f"Dropping test database '{db_name}'...")
            conn.execute(text(f"DROP DATABASE {db_name}"))
            print(f"Database '{db_name}' dropped successfully!")
        else:
            print(f"Test database '{db_name}' does not exist.")

@pytest.fixture(scope='session', autouse=True)
def setup_test_db():
    """Set up the test database before all tests."""
    # Clean up and create a fresh database
    drop_test_db()
    create_test_db()
    yield
    # Clean up after tests
    drop_test_db()

@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    _app = create_app(TestingConfig)
    _app.config['TESTING'] = True
    # Temporarily use SQLite for tests
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    # Other test settings
    _app.config['WTF_CSRF_ENABLED'] = False
    
    # Create app context
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()

@pytest.fixture(scope='session')
def db(app):
    """Create database for the tests."""
    with app.app_context():
        _db.create_all()
        
    yield _db
    
    # Clean up
    with app.app_context():
        _db.session.close()
        _db.drop_all()

@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test runner for the app's Click commands."""
    return app.test_cli_runner() 