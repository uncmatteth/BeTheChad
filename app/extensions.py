"""
Flask extensions module.
This module contains all Flask extensions used by the application.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'}) 