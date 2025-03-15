"""
Flask application package.
"""
import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config_by_name
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.middleware.proxy_fix import ProxyFix
from app.extensions import db, migrate, login_manager, cache, limiter, compress
from app.utils.scheduler import init_scheduler

# Import models to ensure they are registered with SQLAlchemy
from app.models.user import User
from app.models.chad import Chad, ChadClass
from app.models.waifu import Waifu, WaifuType, WaifuRarity
from app.models.item import Item, ItemType, ItemRarity, WaifuItem, CharacterItem
from app.models.cabal import Cabal, CabalMember
from app.models.battle import Battle
from app.models.meme_elixir import MemeElixir
from app.models.transaction import Transaction
from app.models.nft import NFT

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID."""
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        # Log the error but don't crash
        current_app = app or create_app()
        current_app.logger.error(f"Error loading user {user_id}: {str(e)}")
        return None

def create_app(config_name='development'):
    """
    Application factory pattern to create the Flask app
    
    Args:
        config_name (str): Configuration environment name (development, testing, production)
    
    Returns:
        Flask app instance
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the config based on environment
    app.config.from_object(config_by_name[config_name])
    
    # Database URL handling: Ensure DATABASE_URL has priority if present
    # This ensures consistent PostgreSQL usage in all environments including migrations
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Handle Render's postgres:// vs postgresql:// URL format
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        # Override the SQLALCHEMY_DATABASE_URI with DATABASE_URL
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        
        # Log the database connection (safely)
        masked_url = database_url
        if '@' in masked_url:
            protocol_and_creds = masked_url.split('@')[0].split('://')
            masked_url = f"{protocol_and_creds[0]}://****:****@{masked_url.split('@')[1]}"
        app.logger.info(f"Using database URL: {masked_url}")
    else:
        app.logger.warning("No DATABASE_URL found in environment, using default config database.")
    
    # Fix for proxy headers when behind a reverse proxy
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    
    # Configure compression
    app.config['COMPRESS_MIMETYPES'] = [
        'text/html',
        'text/css',
        'text/xml',
        'application/json',
        'application/javascript',
        'application/x-javascript',
        'application/xml',
        'application/xml+rss',
        'text/javascript'
    ]
    app.config['COMPRESS_LEVEL'] = 6  # Default level, good balance between speed and compression
    app.config['COMPRESS_MIN_SIZE'] = 500  # Only compress responses > 500 bytes
    
    # Configure caching based on environment
    if config_name == 'production':
        app.config['CACHE_TYPE'] = 'RedisCache'
        app.config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes
    elif config_name == 'development':
        app.config['CACHE_TYPE'] = 'SimpleCache'
        app.config['CACHE_DEFAULT_TIMEOUT'] = 60  # 1 minute
    else:  # testing
        app.config['CACHE_TYPE'] = 'NullCache'  # No caching for tests
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    cache.init_app(app)
    limiter.init_app(app)
    compress.init_app(app)
    
    # Set up logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/chadbattles.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Chad Battles startup')
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register CLI commands
    register_commands(app)
    
    # Add health check route
    @app.route('/health')
    def health_check():
        try:
            # Test DB connection
            db.session.execute('SELECT 1')
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "feature_flags": {
                    "blockchain": app.config.get('ENABLE_BLOCKCHAIN', False),
                    "twitter_bot": app.config.get('ENABLE_TWITTER_BOT', False)
                }
            })
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "error": str(e)
            }), 500
    
    with app.app_context():
        # Initialize scheduler for background tasks
        if not app.config.get('TESTING'):
            init_scheduler()
    
    return app

def register_error_handlers(app):
    """Register error handlers with the Flask application."""
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

def register_blueprints(app):
    """Register Flask blueprints."""
    from app.controllers.main import main_bp
    from app.controllers.auth import auth_bp
    from app.controllers.api import api_bp
    from app.controllers.chad import chad_bp
    from app.controllers.waifu import waifu_bp
    from app.controllers.cabal import cabal_bp
    from app.controllers.cabal_analytics import analytics_bp
    from app.controllers.admin import admin_bp
    from app.controllers.battle import battle_bp
    from app.controllers.inventory import inventory_bp
    from app.controllers.wallet import wallet_bp
    from app.controllers.nft import nft_bp
    from app.controllers.squad import squad_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(chad_bp, url_prefix='/chad')
    app.register_blueprint(waifu_bp, url_prefix='/waifu')
    app.register_blueprint(cabal_bp, url_prefix='/cabal')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(battle_bp, url_prefix='/battle')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
    app.register_blueprint(nft_bp, url_prefix='/nft')
    app.register_blueprint(squad_bp)
    
    # Register music blueprint
    from app.routes.music import music
    app.register_blueprint(music, url_prefix='/music')
    
    return None

def register_commands(app):
    """Register Flask CLI commands."""
    
    @app.cli.command("init-db")
    def init_db_command():
        """Initialize the database with minimal required data."""
        try:
            from setup_deployment_db import setup_deployment_db
            config_name = app.config['ENV']
            print(f"Starting database initialization in {config_name} mode...")
            if setup_deployment_db(config_name):
                print("Database initialization completed successfully!")
            else:
                print("Database initialization failed!")
                import sys
                sys.exit(1)
        except Exception as e:
            import traceback
            print(f"Error during database initialization: {str(e)}")
            traceback.print_exc()
            import sys
            sys.exit(1)
            
    @app.cli.command("init-db-force")
    def init_db_force_command():
        """Force initialize the database by dropping all tables first."""
        try:
            print("WARNING: This will delete all data in the database!")
            print("Starting forced database initialization...")
            
            # Import the setup script here to avoid circular imports
            from setup_deployment_db import setup_deployment_db
            
            # Determine environment
            config_name = app.config['ENV']
            print(f"Using environment: {config_name}")
            
            # Run the setup script
            if setup_deployment_db(config_name):
                print("Database initialization completed successfully!")
            else:
                print("Database initialization failed!")
                import sys
                sys.exit(1)
        except Exception as e:
            import traceback
            print(f"Error during database initialization: {str(e)}")
            traceback.print_exc()
            import sys
            sys.exit(1)

# Register models
from app.models import user, chad, waifu, item, cabal, battle, meme_elixir, transaction, nft 