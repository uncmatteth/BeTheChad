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

def create_app(test_config=None):
    """
    Application factory pattern to create the Flask app
    
    Args:
        test_config (dict): Configuration for testing
    
    Returns:
        Flask app instance
    """
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure logging
    configure_logging(app)
    
    # Log startup information
    app.logger.info("Starting application")
    
    # Load configuration
    load_config(app, test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception as e:
        app.logger.error(f"Failed to create instance path: {e}")
    
    # Initialize extensions
    initialize_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Add health check endpoint
    @app.route('/health')
    def health_check():
        try:
            # Test database connection
            db_ok = False
            try:
                db.session.execute('SELECT 1')
                db_ok = True
            except Exception as e:
                app.logger.warning(f"Database health check failed: {e}")
            
            return jsonify({
                'status': 'ok',
                'message': 'Application is running',
                'database': 'connected' if db_ok else 'error'
            })
        except Exception as e:
            app.logger.error(f"Health check failed: {e}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    with app.app_context():
        # Initialize scheduler for background tasks
        if not app.config.get('TESTING'):
            init_scheduler()
    
    return app

def load_config(app, test_config):
    """Load the configuration for the Flask application."""
    app.logger.info("Loading configuration")
    
    try:
        if test_config is None:
            # Load the instance config, if it exists, when not testing
            app.config.from_pyfile('config.py', silent=True)
            
            # Try to get environment from env var
            env = os.environ.get('FLASK_ENV', 'development')
            app.logger.info(f"Environment: {env}")
            
            # Load environment-specific config
            if env == 'production':
                app.logger.info("Loading production config")
                app.config.from_object('config.ProductionConfig')
            elif env == 'testing':
                app.logger.info("Loading testing config")
                app.config.from_object('config.TestingConfig')
            else:
                app.logger.info("Loading development config")
                app.config.from_object('config.DevelopmentConfig')
            
            # Priority order for DATABASE_URL:
            # 1. Environment variable DATABASE_URL (for Render.com and other hosting)
            # 2. Config file setting
            # 3. Default SQLite database
            if 'DATABASE_URL' in os.environ:
                db_url = os.environ.get('DATABASE_URL')
                # Fix for Render.com - replace postgres:// with postgresql://
                if db_url.startswith('postgres://'):
                    db_url = db_url.replace('postgres://', 'postgresql://', 1)
                    app.logger.info("Fixed DATABASE_URL format (postgres:// -> postgresql://)")
                
                app.config['SQLALCHEMY_DATABASE_URI'] = db_url
                app.logger.info(f"Using DATABASE_URL from environment: {mask_password(db_url)}")
        else:
            # Load the test config if passed in
            app.logger.info("Loading test configuration")
            app.config.from_mapping(test_config)
    except Exception as e:
        app.logger.error(f"Error loading configuration: {e}")
        # Use a safe fallback configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/fallback.db'
        app.config['SECRET_KEY'] = os.urandom(24)
        app.logger.warning("Using fallback configuration due to error")

def mask_password(url):
    """Mask password in database URL for logging."""
    if not url or '//' not in url:
        return url
    
    try:
        # Format: dialect+driver://username:password@host:port/database
        parts = url.split('@')
        if len(parts) < 2:
            return url
        
        credentials = parts[0].split('//')
        if len(credentials) < 2:
            return url
        
        user_pass = credentials[1].split(':')
        if len(user_pass) < 2:
            return url
        
        # Replace password with asterisks
        masked_url = f"{credentials[0]}//{user_pass[0]}:******@{parts[1]}"
        return masked_url
    except Exception:
        # If anything goes wrong, return a completely masked URL
        return "******"

def initialize_extensions(app):
    """Initialize Flask extensions."""
    app.logger.info("Initializing extensions")
    
    try:
        # Initialize SQLAlchemy
        app.logger.info("Initializing SQLAlchemy")
        db.init_app(app)
        
        # Initialize Flask-Migrate
        app.logger.info("Initializing Flask-Migrate")
        migrate.init_app(app, db)
        
        # Initialize Flask-Login
        app.logger.info("Initializing Flask-Login")
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'
        
        # Initialize Flask-Limiter
        app.logger.info("Initializing Flask-Limiter")
        limiter.init_app(app)
        
        # Initialize Flask-Caching
        app.logger.info("Initializing Flask-Caching")
        cache.init_app(app)
        
        # Initialize user loader
        from app.models.user import User
        
        @login_manager.user_loader
        def load_user(user_id):
            try:
                return User.query.get(int(user_id))
            except Exception as e:
                app.logger.error(f"Error loading user {user_id}: {e}")
                return None
        
    except Exception as e:
        app.logger.error(f"Error initializing extensions: {e}")

def register_blueprints(app):
    """Register Flask blueprints."""
    app.logger.info("Registering blueprints")
    
    try:
        # Import blueprints
        from app.routes.auth import auth as auth_blueprint
        from app.routes.main import main as main_blueprint
        from app.routes.music import music as music_blueprint
        from app.routes.admin import admin as admin_blueprint
        
        # Register blueprints
        app.logger.info("Registering auth blueprint")
        app.register_blueprint(auth_blueprint)
        
        app.logger.info("Registering main blueprint")
        app.register_blueprint(main_blueprint)
        
        app.logger.info("Registering music blueprint")
        app.register_blueprint(music_blueprint)
        
        app.logger.info("Registering admin blueprint")
        app.register_blueprint(admin_blueprint)
        
        # Additional blueprint registrations
        try:
            # These blueprints might not be essential, so we handle them separately
            from app.routes.wallet import wallet as wallet_blueprint
            app.register_blueprint(wallet_blueprint)
            app.logger.info("Registered wallet blueprint")
        except ImportError as e:
            app.logger.warning(f"Could not register wallet blueprint: {e}")
            
        try:
            from app.routes.api import api as api_blueprint
            app.register_blueprint(api_blueprint)
            app.logger.info("Registered API blueprint")
        except ImportError as e:
            app.logger.warning(f"Could not register API blueprint: {e}")
            
    except Exception as e:
        app.logger.error(f"Error registering blueprints: {e}")

def register_error_handlers(app):
    """Register error handlers."""
    app.logger.info("Registering error handlers")
    
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": "Not found", "message": "The requested resource was not found"}), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(f"Internal server error: {e}")
        return jsonify({"error": "Internal server error", "message": "An unexpected error occurred"}), 500
    
    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": "Forbidden", "message": "You don't have permission to access this resource"}), 403

def configure_logging(app):
    """Configure logging for the application."""
    # Set the logging level
    app.logger.setLevel(logging.INFO)
    
    # Create a handler for logging to stderr
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    app.logger.addHandler(stream_handler)
    
    # In production, also log to a file
    if os.environ.get('FLASK_ENV') == 'production':
        try:
            log_dir = os.path.join(app.instance_path, 'logs')
            os.makedirs(log_dir, exist_ok=True)
            file_handler = RotatingFileHandler(
                os.path.join(log_dir, 'app.log'),
                maxBytes=10485760,  # 10MB
                backupCount=3
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            app.logger.addHandler(file_handler)
        except Exception as e:
            app.logger.error(f"Could not configure file logging: {e}")

# Register models
from app.models import user, chad, waifu, item, cabal, battle, meme_elixir, transaction, nft 