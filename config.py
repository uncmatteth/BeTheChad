import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    
    # Feature flags
    ENABLE_BLOCKCHAIN = os.getenv('ENABLE_BLOCKCHAIN', 'false').lower() == 'true'
    ENABLE_TWITTER_BOT = os.getenv('ENABLE_TWITTER_BOT', 'false').lower() == 'true'
    
    # Twitter API settings
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    
    # Solana blockchain settings
    SOLANA_RPC_URL = os.getenv('SOLANA_RPC_URL', 'https://api.devnet.solana.com')
    SOLANA_PRIVATE_KEY = os.getenv('SOLANA_PRIVATE_KEY')
    SOLANA_PUBLIC_KEY = os.getenv('SOLANA_PUBLIC_KEY')
    
    # NFT marketplace settings
    NFT_MINT_FEE = int(os.getenv('NFT_MINT_FEE', 50))
    NFT_MARKETPLACE_FEE_PERCENT = float(os.getenv('NFT_MARKETPLACE_FEE_PERCENT', 2.5))
    
    # App settings
    CHADCOIN_STARTER_BALANCE = int(os.getenv('CHADCOIN_STARTER_BALANCE', 100))
    MAX_WAIFUS_EQUIPPED = int(os.getenv('MAX_WAIFUS_EQUIPPED', 3))
    BATTLE_XP_REWARD = int(os.getenv('BATTLE_XP_REWARD', 25))
    CHADCOIN_BATTLE_REWARD = int(os.getenv('CHADCOIN_BATTLE_REWARD', 10))
    MAX_CABAL_SIZE = int(os.getenv('MAX_CABAL_SIZE', 69))


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///dev.db')
    # Enable blockchain in development by default for testing
    ENABLE_BLOCKCHAIN = os.getenv('ENABLE_BLOCKCHAIN', 'true').lower() == 'true'


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///test.db')
    WTF_CSRF_ENABLED = False  # Disable CSRF protection in tests
    # Disable features in testing by default
    ENABLE_BLOCKCHAIN = False
    ENABLE_TWITTER_BOT = False


class ProductionConfig(Config):
    """Production configuration."""
    # Use DATABASE_URL for Render PostgreSQL or fall back to PROD_DATABASE_URI or SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', os.getenv('PROD_DATABASE_URI', 'sqlite:///app.db'))
    
    # Handle Render's postgres:// vs postgresql:// URL format
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    # Add these for production-specific environment
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
    ELASTICSEARCH_USERNAME = os.getenv('ELASTICSEARCH_USERNAME')
    ELASTICSEARCH_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD')
    
    # Redis cache configuration (when implemented)
    REDIS_URL = os.getenv('REDIS_URL')
    
    # For production, explicitly get feature flags from environment
    ENABLE_BLOCKCHAIN = os.getenv('ENABLE_BLOCKCHAIN', 'false').lower() == 'true'
    ENABLE_TWITTER_BOT = os.getenv('ENABLE_TWITTER_BOT', 'false').lower() == 'true'


# Configuration dictionary mapping
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 