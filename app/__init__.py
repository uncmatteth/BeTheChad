import os
from flask import Flask, render_template
from app.extensions import db, migrate, login_manager, cache
from config import config_by_name
from app.utils.scheduler import init_scheduler

def create_app(config_name='development'):
    """
    Application factory pattern to create the Flask app
    
    Args:
        config_name (str): Configuration environment name (development, testing, production)
    
    Returns:
        Flask app instance
    """
    app = Flask(__name__)
    
    # Load the config based on environment
    app.config.from_object(config_by_name[config_name])
    
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
    cache.init_app(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
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
    
    # Register music blueprint
    from app.routes.music import music
    app.register_blueprint(music, url_prefix='/music')
    
    return None

# Register models
from app.models import user, chad, waifu, item, cabal, battle, meme_elixir, transaction, nft 