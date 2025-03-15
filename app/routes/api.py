from flask import Blueprint, jsonify, request, g
from flask_login import login_required, current_user
from app.extensions import db, limiter
from app.models.user import User
from app.models.chad import Chad, ChadClass
from app.models.waifu import Waifu
from app.models.item import Item
import logging

# Create blueprint
api = Blueprint('api', __name__)
logger = logging.getLogger(__name__)

# Middleware to log API requests
@api.before_request
def before_request():
    g.start_time = request.time

@api.after_request
def after_request(response):
    if hasattr(g, 'start_time'):
        diff = request.time - g.start_time
        logger.info(f"API request to {request.path} took {diff:.4f}s")
    return response

# Error handlers
@api.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@api.errorhandler(500)
def server_error(error):
    logger.error(f"API server error: {str(error)}")
    return jsonify({'error': 'Server error'}), 500

# API routes
@api.route('/api/user/me')
@login_required
@limiter.limit("60 per minute")
def get_current_user():
    """Get current user data"""
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'display_name': current_user.display_name,
        'chadcoin_balance': current_user.chadcoin_balance,
        'created_at': current_user.created_at.isoformat() if current_user.created_at else None
    })

@api.route('/api/chad/me')
@login_required
@limiter.limit("60 per minute")
def get_current_chad():
    """Get current user's chad data"""
    try:
        chad = Chad.query.filter_by(user_id=current_user.id).first()
        if not chad:
            return jsonify({'error': 'Chad not found'}), 404
            
        chad_class = ChadClass.query.get(chad.class_id)
        
        return jsonify({
            'id': chad.id,
            'name': chad.name,
            'level': chad.level,
            'xp': chad.xp,
            'class': {
                'id': chad_class.id,
                'name': chad_class.name,
                'description': chad_class.description
            },
            'stats': {
                'clout': chad.clout,
                'roast_level': chad.roast_level,
                'cringe_resistance': chad.cringe_resistance,
                'drip_factor': chad.drip_factor
            }
        })
    except Exception as e:
        logger.error(f"Error fetching chad data: {str(e)}")
        return jsonify({'error': 'Error fetching chad data'}), 500

@api.route('/api/chad/classes')
@limiter.limit("30 per minute")
def get_chad_classes():
    """Get all chad classes"""
    try:
        classes = ChadClass.query.all()
        return jsonify({
            'classes': [
                {
                    'id': cls.id,
                    'name': cls.name,
                    'description': cls.description,
                    'base_stats': {
                        'clout': cls.base_clout_bonus,
                        'roast': cls.base_roast_bonus,
                        'cringe_resistance': cls.base_cringe_resistance_bonus,
                        'drip': cls.base_drip_bonus
                    }
                }
                for cls in classes
            ]
        })
    except Exception as e:
        logger.error(f"Error fetching chad classes: {str(e)}")
        return jsonify({'error': 'Error fetching chad classes'}), 500

@api.route('/api/waifus/me')
@login_required
@limiter.limit("30 per minute")
def get_user_waifus():
    """Get current user's waifus"""
    try:
        waifus = Waifu.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'waifus': [
                {
                    'id': waifu.id,
                    'name': waifu.name,
                    'type_id': waifu.type_id,
                    'rarity_id': waifu.rarity_id,
                    'level': waifu.level,
                    'bonuses': {
                        'clout': waifu.clout_bonus,
                        'roast': waifu.roast_bonus,
                        'cringe_resistance': waifu.cringe_resistance_bonus,
                        'drip': waifu.drip_bonus
                    }
                }
                for waifu in waifus
            ]
        })
    except Exception as e:
        logger.error(f"Error fetching waifus: {str(e)}")
        return jsonify({'error': 'Error fetching waifus'}), 500

@api.route('/api/items/me')
@login_required
@limiter.limit("30 per minute")
def get_user_items():
    """Get current user's items"""
    try:
        items = Item.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'items': [
                {
                    'id': item.id,
                    'name': item.name,
                    'type_id': item.type_id,
                    'rarity_id': item.rarity_id,
                    'is_equipped': item.is_equipped,
                    'bonuses': {
                        'clout': item.clout_bonus,
                        'roast': item.roast_bonus,
                        'cringe_resistance': item.cringe_resistance_bonus,
                        'drip': item.drip_bonus
                    }
                }
                for item in items
            ]
        })
    except Exception as e:
        logger.error(f"Error fetching items: {str(e)}")
        return jsonify({'error': 'Error fetching items'}), 500

@api.route('/api/leaderboard')
@limiter.limit("10 per minute")
def get_leaderboard():
    """Get leaderboard data"""
    try:
        # Get top 25 chads by level
        top_chads = db.session.query(
            Chad, User.username
        ).join(
            User, Chad.user_id == User.id
        ).order_by(
            Chad.level.desc(),
            Chad.xp.desc()
        ).limit(25).all()
        
        return jsonify({
            'leaderboard': [
                {
                    'rank': index + 1,
                    'chad_id': chad.id,
                    'chad_name': chad.name,
                    'username': username,
                    'level': chad.level,
                    'class_id': chad.class_id,
                    'score': (chad.level * 100) + (chad.clout + chad.roast_level + chad.cringe_resistance + chad.drip_factor)
                }
                for index, (chad, username) in enumerate(top_chads)
            ]
        })
    except Exception as e:
        logger.error(f"Error fetching leaderboard: {str(e)}")
        return jsonify({'error': 'Error fetching leaderboard'}), 500 