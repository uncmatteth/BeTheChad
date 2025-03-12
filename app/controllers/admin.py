"""
Admin controller for Chad Battles.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def check_admin():
    """Check if the current user is an admin."""
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('You do not have permission to access the admin area.', 'danger')
        return redirect(url_for('main.index'))

@admin_bp.route('/')
@login_required
def index():
    """Admin dashboard."""
    return render_template('admin/index.html')

@admin_bp.route('/users')
@login_required
def users():
    """User management."""
    from app.models.user import User
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/stats')
@login_required
def stats():
    """Game statistics."""
    from app.models.user import User
    from app.models.chad import Chad
    from app.models.waifu import Waifu
    from app.models.item import Item
    from app.models.cabal import Cabal
    from app.models.battle import Battle
    from app.models.nft import NFT
    
    stats = {
        'user_count': User.query.count(),
        'chad_count': Chad.query.count(),
        'waifu_count': Waifu.query.count(),
        'item_count': Item.query.count(),
        'cabal_count': Cabal.query.count(),
        'battle_count': Battle.query.count(),
        'nft_count': NFT.query.count()
    }
    
    return render_template('admin/stats.html', stats=stats) 