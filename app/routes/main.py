from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db, limiter, cache
import logging
from app.models.user import User
from app.models.chad import Chad, ChadClass
from app.models.waifu import Waifu
from app.models.inventory import Inventory
from app.models.battle import Battle
import json
import traceback
from datetime import datetime

# Create blueprint
main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/')
def index():
    """Homepage route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/health')
def health():
    """Health check endpoint for deployment monitoring."""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@main.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    return render_template('main/dashboard.html')

@main.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')

@main.route('/how-to-play')
def how_to_play():
    """How to play page"""
    return render_template('main/how_to_play.html')

@main.route('/leaderboard')
@cache.cached(timeout=300)  # Cache for 5 minutes
@limiter.limit("30/minute")
def leaderboard():
    """Show leaderboard page"""
    try:
        # Import here to avoid circular imports
        from app.models.chad import Chad
        from app.models.waifu import Waifu
        from app.models.cabal import Cabal
        
        # Try to get battle leaderboard
        try:
            battle_leaderboard = Battle.get_leaderboard(limit=10)
        except Exception as e:
            logger.error(f"Error loading battle leaderboard: {str(e)}")
            battle_leaderboard = []
            
        # Try to get waifu leaderboard (top collectors)
        try:
            waifu_leaderboard = []
            waifu_stats = Waifu.get_collector_stats(limit=10)
            for i, (chad_id, username, class_name, waifu_count, rare_count) in enumerate(waifu_stats, 1):
                waifu_leaderboard.append({
                    'rank': i,
                    'chad_id': chad_id,
                    'chad_name': username,
                    'class_name': class_name,
                    'waifu_count': waifu_count,
                    'rare_count': rare_count,
                    'score': waifu_count * 5 + rare_count * 20
                })
        except Exception as e:
            logger.error(f"Error loading waifu leaderboard: {str(e)}")
            waifu_leaderboard = []
            
        # Try to get cabal leaderboard
        try:
            cabal_leaderboard = []
            cabal_stats = Cabal.get_top_cabals(limit=10)
            for i, (cabal_id, cabal_name, member_count, total_power) in enumerate(cabal_stats, 1):
                cabal_leaderboard.append({
                    'rank': i,
                    'cabal_id': cabal_id,
                    'cabal_name': cabal_name,
                    'member_count': member_count,
                    'total_power': total_power,
                    'avg_power': total_power / member_count if member_count > 0 else 0
                })
        except Exception as e:
            logger.error(f"Error loading cabal leaderboard: {str(e)}")
            cabal_leaderboard = []
        
        # Add rank to battle leaderboard
        for i, entry in enumerate(battle_leaderboard, 1):
            entry['rank'] = i
            
        return render_template(
            'main/leaderboard.html',
            battle_leaderboard=battle_leaderboard,
            waifu_leaderboard=waifu_leaderboard,
            cabal_leaderboard=cabal_leaderboard
        )
        
    except Exception as e:
        logger.error(f"Error loading leaderboard: {str(e)}\n{traceback.format_exc()}")
        # Return empty leaderboards
        return render_template(
            'main/leaderboard.html',
            battle_leaderboard=[],
            waifu_leaderboard=[],
            cabal_leaderboard=[]
        )

@main.route('/faq')
def faq():
    """FAQ page"""
    return render_template('main/faq.html')

@main.route('/terms')
def terms():
    """Terms of service page"""
    return render_template('main/terms.html', now=datetime.now())

@main.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('main/privacy.html', now=datetime.now())

@main.route('/contact')
def contact():
    """Contact page"""
    return render_template('main/contact.html')

@main.route('/search')
@limiter.limit("10 per minute")
def search():
    """Search functionality"""
    query = request.args.get('q', '')
    if not query or len(query) < 3:
        return jsonify({'error': 'Search query must be at least 3 characters'}), 400
        
    # This is a simplified version for deployment
    # In the full version, we would search the database
    results = []
    return jsonify({'results': results})

@main.route('/notifications')
@login_required
@limiter.limit("30 per minute")
def notifications():
    """User notifications"""
    return render_template('main/notifications.html')

@main.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('main/profile.html', user=current_user) 