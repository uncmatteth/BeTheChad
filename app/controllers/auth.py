"""
Authentication controller for Chad Battles.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, login_manager
from app.models.user import User
from app.utils.twitter_api import get_user_profile
from datetime import datetime
import os
import tweepy
import uuid

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID."""
    return User.query.get(int(user_id))

@auth_bp.route('/login')
def login():
    """Login page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/register')
def register():
    """Registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/register.html')

@auth_bp.route('/twitter-login')
def twitter_login():
    """Initiate Twitter login."""
    # In a real implementation, this would redirect to Twitter OAuth
    # For now, we'll simulate a successful login with a demo user
    
    # Check if demo user exists using raw SQL to bypass ORM validation
    result = db.session.execute("SELECT id, username, email, password_hash, x_username, chadcoin_balance, is_admin FROM users WHERE x_username = 'demo_user'").fetchone()
    
    if not result:
        # Create a demo user with direct SQL
        db.session.execute("""
            INSERT INTO users (
                username, 
                email, 
                password_hash, 
                x_id, 
                x_username, 
                x_displayname, 
                x_profile_image, 
                chadcoin_balance, 
                is_admin,
                created_at,
                updated_at
            ) VALUES (
                'demo_user', 
                'demo@example.com', 
                'pbkdf2:sha256:150000$abc123$abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789', 
                :x_id, 
                'demo_user', 
                'Demo User', 
                'https://example.com/profile.jpg', 
                1000, 
                true,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )
        """, {'x_id': str(uuid.uuid4())})
        db.session.commit()
        
        # Get the newly created user
        result = db.session.execute("SELECT id, username, email, password_hash, x_username, chadcoin_balance, is_admin FROM users WHERE x_username = 'demo_user'").fetchone()
    
    # Manually create a User instance with minimal attributes
    demo_user = User(
        id=result[0],
        username=result[1], 
        email=result[2], 
        password_hash=result[3],
        x_username=result[4],
        chadcoin_balance=result[5],
        is_admin=result[6]
    )
    
    # Log in the demo user
    login_user(demo_user)
    flash('You have been logged in as a demo user.', 'success')
    
    return redirect(url_for('main.dashboard'))

@auth_bp.route('/connect-wallet', methods=['POST'])
@login_required
def connect_wallet():
    """Connect a Solana wallet to the user account"""
    wallet_address = request.form.get('wallet_address')
    wallet_type = request.form.get('wallet_type', 'unknown')
    signature = request.form.get('signature')
    
    if not wallet_address:
        return jsonify({'success': False, 'message': 'No wallet address provided'})
    
    # Check if another user already has this wallet address
    existing_user = User.query.filter(
        User.wallet_address == wallet_address, 
        User.id != current_user.id
    ).first()
    
    if existing_user:
        return jsonify({'success': False, 'message': 'This wallet address is already connected to another account'})
    
    # In a real implementation, you would verify the signature
    # For now, we'll just update the user's wallet address
    
    current_user.wallet_address = wallet_address
    current_user.wallet_type = wallet_type
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'{wallet_type.capitalize()} wallet connected successfully'}) 