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
import logging

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
    try:
        # In a real implementation, this would redirect to Twitter OAuth
        # For now, we'll simulate a successful login with a demo user
        
        # Check if we're using SQLite or PostgreSQL
        db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
        is_sqlite = 'sqlite' in db_url
        is_postgresql = 'postgresql' in db_url
        
        current_app.logger.info(f"Database URL type: {'SQLite' if is_sqlite else 'PostgreSQL' if is_postgresql else 'Unknown'}")
        
        # Check if the users table exists
        try:
            # Check if demo user exists using raw SQL to bypass ORM validation
            if is_sqlite:
                # SQLite query
                result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users'").fetchone()
                if result[0] == 0:
                    # Table doesn't exist yet, create it
                    current_app.logger.warning("Users table not found in SQLite database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password_hash TEXT,
                            x_id TEXT UNIQUE,
                            x_username TEXT UNIQUE,
                            x_displayname TEXT,
                            x_profile_image TEXT,
                            chadcoin_balance INTEGER DEFAULT 100,
                            is_admin BOOLEAN DEFAULT FALSE,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    db.session.commit()
            elif is_postgresql:
                # PostgreSQL query
                result = db.session.execute("SELECT to_regclass('public.users')").fetchone()
                if result[0] is None:
                    # Table doesn't exist yet, create it
                    current_app.logger.warning("Users table not found in PostgreSQL database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(64) UNIQUE NOT NULL,
                            email VARCHAR(120) UNIQUE NOT NULL,
                            password_hash VARCHAR(128),
                            x_id VARCHAR(64) UNIQUE,
                            x_username VARCHAR(64) UNIQUE,
                            x_displayname VARCHAR(64),
                            x_profile_image VARCHAR(255),
                            chadcoin_balance INTEGER DEFAULT 100,
                            is_admin BOOLEAN DEFAULT FALSE,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    db.session.commit()
            
            # Check if demo user exists
            result = db.session.execute("SELECT id, username, email, password_hash, x_username, chadcoin_balance, is_admin FROM users WHERE x_username = 'demo_user'").fetchone()
            
            if not result:
                # Create a demo user with direct SQL
                current_app.logger.info("Creating demo user...")
                
                # Different syntax for SQLite vs PostgreSQL for BOOLEAN type
                is_admin_value = "1" if is_sqlite else "TRUE"
                timestamp_value = "CURRENT_TIMESTAMP" if is_postgresql else "datetime('now')"
                
                query = f"""
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
                        {is_admin_value},
                        {timestamp_value},
                        {timestamp_value}
                    )
                """
                
                db.session.execute(query, {'x_id': str(uuid.uuid4())})
                db.session.commit()
                
                # Get the newly created user
                result = db.session.execute("SELECT id, username, email, password_hash, x_username, chadcoin_balance, is_admin FROM users WHERE x_username = 'demo_user'").fetchone()
            
            # Manually create a User instance with minimal attributes
            current_app.logger.info(f"Logging in demo user with id: {result[0]}")
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
            
        except Exception as e:
            current_app.logger.error(f"Error during database operations: {str(e)}")
            flash(f"Login error: Database issue. Please contact support.", 'danger')
            return redirect(url_for('auth.login'))
            
    except Exception as e:
        current_app.logger.error(f"Unexpected error in twitter_login: {str(e)}")
        flash(f"Login error: {str(e)}", 'danger')
        return redirect(url_for('auth.login'))

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