"""
Permissions utilities for controlling access to features.

This module provides decorators and functions for checking permissions,
such as requiring cabal membership or officer status.
"""

import logging
from functools import wraps
from flask import abort, request, current_app
from flask_login import current_user

logger = logging.getLogger(__name__)

def require_cabal_membership(f):
    """
    Decorator to require cabal membership for a route.
    
    Args:
        f: The route function to decorate
        
    Returns:
        The decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in (should be handled by login_required)
        if not current_user.is_authenticated:
            return abort(401)
        
        # Get cabal_id from route params
        cabal_id = kwargs.get('cabal_id')
        if not cabal_id:
            return abort(400, "Cabal ID is required")
        
        # Check if user's chad is a member of the cabal
        from app.models.cabal import CabalMember
        
        # Get user's chad ID
        chad_id = current_user.chad_id
        if not chad_id:
            return abort(400, "User does not have a Chad character")
        
        # Check membership
        member = CabalMember.query.filter_by(
            cabal_id=cabal_id,
            chad_id=chad_id,
            is_active=True
        ).first()
        
        if not member:
            return abort(403, "You are not a member of this cabal")
        
        # Pass the member object to the route
        kwargs['member'] = member
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_cabal_officer(f):
    """
    Decorator to require cabal officer status for a route.
    
    Args:
        f: The route function to decorate
        
    Returns:
        The decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in (should be handled by login_required)
        if not current_user.is_authenticated:
            return abort(401)
        
        # Get cabal_id from route params
        cabal_id = kwargs.get('cabal_id')
        if not cabal_id:
            return abort(400, "Cabal ID is required")
        
        # Get user's chad ID
        chad_id = current_user.chad_id
        if not chad_id:
            return abort(400, "User does not have a Chad character")
        
        # Check if user is cabal leader
        from app.models.cabal import Cabal
        
        cabal = Cabal.query.get(cabal_id)
        if not cabal:
            return abort(404, "Cabal not found")
        
        if cabal.leader_id == chad_id:
            # User is leader, pass cabal to route
            kwargs['cabal'] = cabal
            return f(*args, **kwargs)
        
        # Check if user is an officer
        from app.models.cabal import CabalOfficerRole
        
        officer = CabalOfficerRole.query.filter_by(
            cabal_id=cabal_id,
            chad_id=chad_id
        ).first()
        
        if not officer:
            return abort(403, "You must be a cabal leader or officer to access this feature")
        
        # Pass the officer object to the route
        kwargs['officer'] = officer
        kwargs['cabal'] = cabal
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_cabal_leader(f):
    """
    Decorator to require cabal leader status for a route.
    
    Args:
        f: The route function to decorate
        
    Returns:
        The decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in (should be handled by login_required)
        if not current_user.is_authenticated:
            return abort(401)
        
        # Get cabal_id from route params
        cabal_id = kwargs.get('cabal_id')
        if not cabal_id:
            return abort(400, "Cabal ID is required")
        
        # Get user's chad ID
        chad_id = current_user.chad_id
        if not chad_id:
            return abort(400, "User does not have a Chad character")
        
        # Check if user is cabal leader
        from app.models.cabal import Cabal
        
        cabal = Cabal.query.get(cabal_id)
        if not cabal:
            return abort(404, "Cabal not found")
        
        if cabal.leader_id != chad_id:
            return abort(403, "You must be the cabal leader to access this feature")
        
        # Pass the cabal object to the route
        kwargs['cabal'] = cabal
        
        return f(*args, **kwargs)
    
    return decorated_function 