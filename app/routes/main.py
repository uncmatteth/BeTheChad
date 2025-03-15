from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db, limiter
import logging

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
def leaderboard():
    """Leaderboard page"""
    try:
        # This is a simplified version for deployment
        # In the full version, we would query the database for top users
        return render_template('main/leaderboard.html')
    except Exception as e:
        logger.error(f"Error loading leaderboard: {str(e)}")
        flash('Error loading leaderboard', 'danger')
        return redirect(url_for('main.index'))

@main.route('/faq')
def faq():
    """FAQ page"""
    return render_template('main/faq.html')

@main.route('/terms')
def terms():
    """Terms of service page"""
    return render_template('main/terms.html')

@main.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('main/privacy.html')

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