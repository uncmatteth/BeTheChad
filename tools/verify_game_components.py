#!/usr/bin/env python
"""
Verification script for Chad Battles game components.

This script checks that all key components of the game are working correctly:
- Database models and relationships
- Controllers and routes
- Scheduled tasks
- Caching
- Twitter integration

Usage:
    python tools/verify_game_components.py

"""
import os
import sys
import time
import logging
from datetime import datetime

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_database_models():
    """Check that all database models are properly defined and can be instantiated."""
    from app import db
    from app.models.user import User
    from app.models.chad import Chad
    from app.models.waifu import Waifu
    from app.models.item import Item
    from app.models.cabal import Cabal, CabalMember, CabalOfficerRole
    from app.models.battle import Battle
    from app.models.transaction import Transaction
    from app.models.referral import Referral
    from app.models.cabal_analytics import CabalAnalytics
    
    logger.info("Checking database models...")
    
    # Check that all models have the expected attributes
    models = [
        (User, ['id', 'username', 'email', 'password_hash', 'chad_id']),
        (Chad, ['id', 'name', 'level', 'xp', 'class_type']),
        (Waifu, ['id', 'name', 'rarity', 'power', 'owner_id']),
        (Item, ['id', 'name', 'type', 'rarity', 'stat_boost']),
        (Cabal, ['id', 'name', 'description', 'leader_id', 'created_at']),
        (CabalMember, ['id', 'cabal_id', 'chad_id', 'role', 'joined_at']),
        (Battle, ['id', 'attacker_id', 'defender_id', 'winner_id', 'battle_date']),
        (Transaction, ['id', 'user_id', 'amount', 'transaction_type', 'created_at']),
        (Referral, ['id', 'referrer_id', 'referred_id', 'cabal_id', 'created_at']),
        (CabalAnalytics, ['id', 'cabal_id', 'timestamp', 'member_count', 'total_power'])
    ]
    
    for model_class, expected_attrs in models:
        model_name = model_class.__name__
        logger.info(f"Checking {model_name}...")
        
        # Check that the model has a __tablename__ attribute
        if not hasattr(model_class, '__tablename__'):
            logger.error(f"{model_name} does not have a __tablename__ attribute")
            return False
        
        # Check that the model has all expected attributes
        for attr in expected_attrs:
            if not hasattr(model_class, attr):
                logger.error(f"{model_name} does not have attribute '{attr}'")
                return False
    
    logger.info("All database models look good!")
    return True

def check_controllers():
    """Check that all controllers are properly defined and routes are accessible."""
    from app import create_app
    from flask import url_for
    
    logger.info("Checking controllers and routes...")
    
    # Create a test app
    app = create_app('testing')
    
    # Define the routes to check
    routes_to_check = [
        ('main.index', {}),
        ('auth.login', {}),
        ('auth.register', {}),
        ('chad_bp.profile', {}),
        ('marketplace_bp.index', {}),
        ('waifu_bp.collection', {}),
        ('cabal_bp.index', {}),
        ('cabal_bp.all_battles', {}),
        ('analytics_bp.dashboard', {'cabal_id': 'test'})
    ]
    
    with app.test_request_context():
        for route, kwargs in routes_to_check:
            try:
                url = url_for(route, **kwargs)
                logger.info(f"Route {route} maps to URL {url}")
            except Exception as e:
                logger.error(f"Error checking route {route}: {str(e)}")
                return False
    
    logger.info("All controllers and routes look good!")
    return True

def check_scheduled_tasks():
    """Check that scheduled tasks are properly defined."""
    from app.utils.scheduled_tasks import send_weekly_cabal_recap, update_cabal_rankings
    
    logger.info("Checking scheduled tasks...")
    
    # Check that the scheduled task functions exist
    if not callable(send_weekly_cabal_recap):
        logger.error("send_weekly_cabal_recap is not callable")
        return False
    
    if not callable(update_cabal_rankings):
        logger.error("update_cabal_rankings is not callable")
        return False
    
    # Check that the scheduler is properly configured
    from app.utils.scheduler import init_scheduler
    
    if not callable(init_scheduler):
        logger.error("init_scheduler is not callable")
        return False
    
    logger.info("All scheduled tasks look good!")
    return True

def check_caching():
    """Check that caching is properly configured."""
    from app import create_app, cache
    
    logger.info("Checking caching...")
    
    # Create a test app
    app = create_app('testing')
    
    with app.app_context():
        # Check that the cache is initialized
        if not hasattr(cache, 'get') or not callable(cache.get):
            logger.error("Cache is not properly initialized")
            return False
        
        # Test setting and getting a value from the cache
        test_key = f"test_key_{int(time.time())}"
        test_value = f"test_value_{datetime.now()}"
        
        try:
            cache.set(test_key, test_value, timeout=10)
            retrieved_value = cache.get(test_key)
            
            if retrieved_value != test_value:
                logger.error(f"Cache test failed: expected {test_value}, got {retrieved_value}")
                return False
        except Exception as e:
            logger.error(f"Error testing cache: {str(e)}")
            return False
    
    logger.info("Caching looks good!")
    return True

def check_twitter_integration():
    """Check that Twitter integration is properly configured."""
    from app.utils.twitter_api import post_tweet, share_weekly_leaderboard
    
    logger.info("Checking Twitter integration...")
    
    # Check that the Twitter API functions exist
    if not callable(post_tweet):
        logger.error("post_tweet is not callable")
        return False
    
    if not callable(share_weekly_leaderboard):
        logger.error("share_weekly_leaderboard is not callable")
        return False
    
    # We won't actually post to Twitter in this test
    logger.info("Twitter integration functions look good!")
    return True

def main():
    """Run all verification checks."""
    logger.info("Starting verification of Chad Battles game components...")
    
    checks = [
        ("Database Models", check_database_models),
        ("Controllers", check_controllers),
        ("Scheduled Tasks", check_scheduled_tasks),
        ("Caching", check_caching),
        ("Twitter Integration", check_twitter_integration)
    ]
    
    results = []
    
    for name, check_func in checks:
        logger.info(f"Running check: {name}")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"Error during {name} check: {str(e)}")
            results.append((name, False))
    
    # Print summary
    logger.info("\n" + "=" * 50)
    logger.info("VERIFICATION RESULTS")
    logger.info("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "PASSED" if result else "FAILED"
        logger.info(f"{name}: {status}")
        if not result:
            all_passed = False
    
    logger.info("=" * 50)
    if all_passed:
        logger.info("All checks passed! The game is ready for deployment.")
        return 0
    else:
        logger.error("Some checks failed. Please fix the issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 