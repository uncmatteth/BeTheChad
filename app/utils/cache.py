"""
Caching utilities for performance optimization.

This module provides functions for caching frequently accessed data,
such as cabal leaderboards and user stats.
"""

import logging
from functools import wraps
from datetime import datetime, timedelta
from flask import current_app

logger = logging.getLogger(__name__)

def cached_leaderboard(f):
    """
    Decorator to cache cabal leaderboard data.
    
    The leaderboard data is cached for 1 hour to improve performance.
    
    Args:
        f: The function to cache (typically Cabal.get_leaderboard)
        
    Returns:
        The cached result if available, otherwise the result of calling the function
    """
    cache_key = 'cabal_leaderboard'
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if caching is enabled
        if not current_app.config.get('ENABLE_CACHING', False):
            return f(*args, **kwargs)
        
        # Get the cache instance
        cache = current_app.extensions.get('cache')
        if not cache:
            return f(*args, **kwargs)
        
        # Try to get from cache
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.debug(f"Cache hit for {cache_key}")
            return cached_data
        
        # Call the original function
        result = f(*args, **kwargs)
        
        # Store in cache with 1 hour expiration
        cache.set(cache_key, result, timeout=3600)
        logger.debug(f"Cache miss for {cache_key}, stored new data")
        
        return result
    
    return decorated_function

def cached_cabal_data(cabal_id):
    """
    Decorator factory to cache cabal-specific data.
    
    Args:
        cabal_id: The ID of the cabal to cache data for
        
    Returns:
        A decorator function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if caching is enabled
            if not current_app.config.get('ENABLE_CACHING', False):
                return f(*args, **kwargs)
            
            # Get the cache instance
            cache = current_app.extensions.get('cache')
            if not cache:
                return f(*args, **kwargs)
            
            # Generate a cache key specific to this cabal and function
            cache_key = f"cabal_{cabal_id}_{f.__name__}"
            
            # Try to get from cache
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_data
            
            # Call the original function
            result = f(*args, **kwargs)
            
            # Store in cache with 5 minute expiration
            cache.set(cache_key, result, timeout=300)
            logger.debug(f"Cache miss for {cache_key}, stored new data")
            
            return result
        
        return decorated_function
    
    return decorator

def invalidate_cabal_cache(cabal_id):
    """
    Invalidate all cached data for a specific cabal.
    
    This should be called whenever a cabal's data is modified.
    
    Args:
        cabal_id: The ID of the cabal to invalidate cache for
    """
    # Check if caching is enabled
    if not current_app.config.get('ENABLE_CACHING', False):
        return
    
    # Get the cache instance
    cache = current_app.extensions.get('cache')
    if not cache:
        return
    
    # Clear specific cache keys
    cache_prefix = f"cabal_{cabal_id}_"
    # Note: This is a simplification - in a real implementation,
    # you would need to keep track of all cache keys used for a cabal
    # or use a cache backend that supports pattern-based deletion
    
    # Also invalidate the leaderboard cache
    cache.delete('cabal_leaderboard')
    logger.debug(f"Invalidated cache for cabal {cabal_id} and the leaderboard") 