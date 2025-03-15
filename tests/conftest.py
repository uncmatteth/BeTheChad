import os
import pytest
from app import create_app
from app.extensions import db as _db
from config import TestingConfig

@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    _app = create_app(TestingConfig)
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'TEST_DATABASE_URI',
        'postgresql://postgres:postgres@localhost/chad_battles_test'
    )
    
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