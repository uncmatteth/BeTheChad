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
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        current_app.logger.error(f"Error loading user {user_id}: {str(e)}")
        return None

@auth_bp.route('/login')
def login():
    """Login page."""
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        return render_template('auth/login.html')
    except Exception as e:
        # Log the error
        current_app.logger.error(f"Error in login route: {str(e)}")
        # Clear the session to prevent corruption
        session.clear()
        # Flash a user-friendly message
        flash('An error occurred during login. Please try again.', 'danger')
        # Return to the index page
        return redirect(url_for('main.index'))

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
                # SQLite query to check if users table exists
                result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users'").fetchone()
                if result[0] == 0:
                    # Table doesn't exist yet, create it with ALL columns from the User model
                    current_app.logger.warning("Users table not found in SQLite database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username VARCHAR(64) UNIQUE NOT NULL,
                            email VARCHAR(120) UNIQUE NOT NULL,
                            password_hash VARCHAR(128),
                            display_name VARCHAR(64),
                            bio VARCHAR(500),
                            avatar_url VARCHAR(255),
                            chadcoin_balance INTEGER DEFAULT 100,
                            wallet_address VARCHAR(255) UNIQUE,
                            wallet_type VARCHAR(50),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            last_login TIMESTAMP,
                            x_id VARCHAR(64) UNIQUE,
                            x_username VARCHAR(64) UNIQUE,
                            x_displayname VARCHAR(64),
                            x_profile_image VARCHAR(255),
                            is_admin BOOLEAN DEFAULT 0
                        )
                    """)
                    db.session.commit()
                
                # Check if chad_classes table exists
                result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='chad_classes'").fetchone()
                if result[0] == 0:
                    # Create chad_classes table
                    current_app.logger.warning("chad_classes table not found in SQLite database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS chad_classes (
                            id INTEGER PRIMARY KEY,
                            name VARCHAR(50) UNIQUE NOT NULL,
                            description TEXT NOT NULL,
                            base_clout_bonus INTEGER DEFAULT 0,
                            base_roast_bonus INTEGER DEFAULT 0,
                            base_cringe_resistance_bonus INTEGER DEFAULT 0,
                            base_drip_bonus INTEGER DEFAULT 0
                        )
                    """)
                    # Insert default chad classes
                    db.session.execute("""
                        INSERT INTO chad_classes (name, description, base_clout_bonus, base_roast_bonus, 
                                              base_cringe_resistance_bonus, base_drip_bonus)
                        VALUES ('Sigma', 'The lone wolf with exceptional independence', 5, 3, 5, 2),
                               ('Alpha', 'The natural leader with commanding presence', 4, 4, 3, 4),
                               ('Gigachad', 'The ultimate form of masculinity', 5, 5, 5, 5)
                    """)
                    db.session.commit()
                
                # Check if chads table exists
                result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='chads'").fetchone()
                if result[0] == 0:
                    # Create chads table
                    current_app.logger.warning("chads table not found in SQLite database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS chads (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            class_id INTEGER NOT NULL,
                            name VARCHAR(50) NOT NULL,
                            avatar_locked BOOLEAN DEFAULT 0,
                            level INTEGER DEFAULT 1,
                            xp INTEGER DEFAULT 0,
                            clout INTEGER DEFAULT 10,
                            roast_level INTEGER DEFAULT 10,
                            cringe_resistance INTEGER DEFAULT 10,
                            drip_factor INTEGER DEFAULT 10,
                            battles_won INTEGER DEFAULT 0,
                            battles_lost INTEGER DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id),
                            FOREIGN KEY (class_id) REFERENCES chad_classes (id)
                        )
                    """)
                    db.session.commit()
                
                # Check if items table exists
                result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='items'").fetchone()
                if result[0] == 0:
                    # Create items table
                    current_app.logger.warning("items table not found in SQLite database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS items (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            chad_id INTEGER,
                            waifu_id INTEGER,
                            item_type_id INTEGER NOT NULL,
                            name VARCHAR(50) NOT NULL,
                            is_equipped BOOLEAN DEFAULT 0,
                            type VARCHAR(50),
                            clout_bonus INTEGER DEFAULT 0,
                            roast_bonus INTEGER DEFAULT 0,
                            cringe_resistance_bonus INTEGER DEFAULT 0,
                            drip_bonus INTEGER DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id),
                            FOREIGN KEY (chad_id) REFERENCES chads (id)
                        )
                    """)
                    db.session.commit()
                
                # Check if battles table exists
                result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='battles'").fetchone()
                if result[0] == 0:
                    # Create battles table
                    current_app.logger.warning("battles table not found in SQLite database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS battles (
                            id INTEGER PRIMARY KEY,
                            battle_type VARCHAR(20) NOT NULL,
                            status VARCHAR(20) NOT NULL,
                            initiator_id INTEGER NOT NULL,
                            initiator_chad_id INTEGER NOT NULL,
                            opponent_id INTEGER,
                            opponent_chad_id INTEGER,
                            npc_opponent_id INTEGER,
                            wager_amount INTEGER DEFAULT 0,
                            turn_count INTEGER DEFAULT 0,
                            current_turn INTEGER DEFAULT 0,
                            winner_id INTEGER,
                            loser_id INTEGER,
                            battle_log TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            started_at TIMESTAMP,
                            completed_at TIMESTAMP,
                            FOREIGN KEY (initiator_id) REFERENCES users (id),
                            FOREIGN KEY (initiator_chad_id) REFERENCES chads (id),
                            FOREIGN KEY (opponent_id) REFERENCES users (id),
                            FOREIGN KEY (opponent_chad_id) REFERENCES chads (id),
                            FOREIGN KEY (winner_id) REFERENCES users (id),
                            FOREIGN KEY (loser_id) REFERENCES users (id)
                        )
                    """)
                    db.session.commit()
                
                # Check if inventories table exists
                result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='inventories'").fetchone()
                if result[0] == 0:
                    # Create inventories table
                    current_app.logger.warning("inventories table not found in SQLite database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS inventories (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                    db.session.commit()
                
                # Check if waifus table exists
                result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='waifus'").fetchone()
                if result[0] == 0:
                    # Create waifu_rarities table first if it doesn't exist
                    rarity_result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='waifu_rarities'").fetchone()
                    if rarity_result[0] == 0:
                        current_app.logger.warning("waifu_rarities table not found in SQLite database, creating it...")
                        db.session.execute("""
                            CREATE TABLE IF NOT EXISTS waifu_rarities (
                                id INTEGER PRIMARY KEY,
                                name VARCHAR(50) UNIQUE NOT NULL,
                                description TEXT NOT NULL,
                                drop_rate FLOAT DEFAULT 0.0,
                                min_stat_bonus INTEGER DEFAULT 1,
                                max_stat_bonus INTEGER DEFAULT 5
                            )
                        """)
                        # Insert default rarities
                        db.session.execute("""
                            INSERT INTO waifu_rarities (name, description, drop_rate, min_stat_bonus, max_stat_bonus)
                            VALUES 
                                ('Common', 'Common waifus with minimal bonuses', 0.6, 1, 3),
                                ('Rare', 'Rare waifus with decent bonuses', 0.3, 2, 5),
                                ('Epic', 'Epic waifus with strong bonuses', 0.08, 3, 7),
                                ('Legendary', 'Legendary waifus with powerful bonuses', 0.02, 5, 10)
                        """)
                        db.session.commit()

                    # Create waifu_types table if it doesn't exist
                    types_result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='waifu_types'").fetchone()
                    if types_result[0] == 0:
                        current_app.logger.warning("waifu_types table not found in SQLite database, creating it...")
                        db.session.execute("""
                            CREATE TABLE IF NOT EXISTS waifu_types (
                                id INTEGER PRIMARY KEY,
                                name VARCHAR(50) UNIQUE NOT NULL,
                                description TEXT NOT NULL,
                                rarity_id INTEGER NOT NULL,
                                base_clout_bonus INTEGER DEFAULT 0,
                                base_roast_bonus INTEGER DEFAULT 0,
                                base_cringe_resistance_bonus INTEGER DEFAULT 0,
                                base_drip_bonus INTEGER DEFAULT 0,
                                FOREIGN KEY (rarity_id) REFERENCES waifu_rarities (id)
                            )
                        """)
                        # Insert default types
                        db.session.execute("""
                            INSERT INTO waifu_types (name, description, rarity_id, base_clout_bonus, base_roast_bonus, base_cringe_resistance_bonus, base_drip_bonus)
                            VALUES 
                                ('Tsundere', 'Cold on the outside, warm on the inside', 2, 1, 3, 1, 1),
                                ('Childhood Friend', 'Known you since forever', 1, 2, 1, 2, 1),
                                ('Gamer Girl', 'Loves video games and tech', 2, 1, 2, 2, 1)
                        """)
                        db.session.commit()
                    
                    # Create waifus table
                    current_app.logger.warning("waifus table not found in SQLite database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS waifus (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            chad_id INTEGER,
                            waifu_type_id INTEGER NOT NULL,
                            name VARCHAR(50) NOT NULL,
                            is_equipped BOOLEAN DEFAULT 0,
                            level INTEGER DEFAULT 1,
                            xp INTEGER DEFAULT 0,
                            clout_bonus INTEGER DEFAULT 0,
                            roast_bonus INTEGER DEFAULT 0,
                            cringe_resistance_bonus INTEGER DEFAULT 0,
                            drip_bonus INTEGER DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id),
                            FOREIGN KEY (chad_id) REFERENCES chads (id),
                            FOREIGN KEY (waifu_type_id) REFERENCES waifu_types (id)
                        )
                    """)
                    db.session.commit()
                
                # Check if item_rarities table exists
                result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='item_rarities'").fetchone()
                if result[0] == 0:
                    # Create item_rarities table
                    current_app.logger.warning("item_rarities table not found in SQLite database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS item_rarities (
                            id INTEGER PRIMARY KEY,
                            name VARCHAR(50) UNIQUE NOT NULL,
                            description TEXT NOT NULL,
                            drop_rate FLOAT DEFAULT 0.0,
                            min_stat_bonus INTEGER DEFAULT 1,
                            max_stat_bonus INTEGER DEFAULT 5
                        )
                    """)
                    # Insert default rarities
                    db.session.execute("""
                        INSERT INTO item_rarities (name, description, drop_rate, min_stat_bonus, max_stat_bonus)
                        VALUES 
                            ('Common', 'Common items with minimal bonuses', 0.6, 1, 3),
                            ('Rare', 'Rare items with decent bonuses', 0.3, 2, 5),
                            ('Epic', 'Epic items with strong bonuses', 0.08, 3, 7),
                            ('Legendary', 'Legendary items with powerful bonuses', 0.02, 5, 10)
                    """)
                    db.session.commit()
                
                # Check if item_types table exists
                result = db.session.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='item_types'").fetchone()
                if result[0] == 0:
                    # Create item_types table
                    current_app.logger.warning("item_types table not found in SQLite database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS item_types (
                            id INTEGER PRIMARY KEY,
                            name VARCHAR(50) UNIQUE NOT NULL,
                            description TEXT NOT NULL,
                            rarity_id INTEGER NOT NULL,
                            slot VARCHAR(50) NOT NULL,
                            base_clout_bonus INTEGER DEFAULT 0,
                            base_roast_bonus INTEGER DEFAULT 0,
                            base_cringe_resistance_bonus INTEGER DEFAULT 0,
                            base_drip_bonus INTEGER DEFAULT 0,
                            is_character_item BOOLEAN DEFAULT 1,
                            FOREIGN KEY (rarity_id) REFERENCES item_rarities (id)
                        )
                    """)
                    # Insert default types
                    db.session.execute("""
                        INSERT INTO item_types (name, description, rarity_id, slot, base_clout_bonus, base_roast_bonus, base_cringe_resistance_bonus, base_drip_bonus, is_character_item)
                        VALUES 
                            ('Snapback Cap', 'A stylish cap for your Chad', 1, 'head', 1, 0, 0, 2, 1),
                            ('Designer Shades', 'Luxury sunglasses', 2, 'accessory', 2, 0, 1, 3, 1),
                            ('Gold Chain', 'Bling for your neck', 2, 'neck', 3, 0, 0, 2, 1)
                    """)
                    db.session.commit()
            
            elif is_postgresql:
                # PostgreSQL query to check if users table exists
                result = db.session.execute("SELECT to_regclass('public.users')").fetchone()
                if result[0] is None:
                    # Table doesn't exist yet, create it with ALL columns from the User model
                    current_app.logger.warning("Users table not found in PostgreSQL database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(64) UNIQUE NOT NULL,
                            email VARCHAR(120) UNIQUE NOT NULL,
                            password_hash VARCHAR(128),
                            display_name VARCHAR(64),
                            bio VARCHAR(500),
                            avatar_url VARCHAR(255),
                            chadcoin_balance INTEGER DEFAULT 100,
                            wallet_address VARCHAR(255) UNIQUE,
                            wallet_type VARCHAR(50),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            last_login TIMESTAMP,
                            x_id VARCHAR(64) UNIQUE,
                            x_username VARCHAR(64) UNIQUE,
                            x_displayname VARCHAR(64),
                            x_profile_image VARCHAR(255),
                            is_admin BOOLEAN DEFAULT TRUE
                        )
                    """)
                    db.session.commit()
                
                # Check if chad_classes table exists
                result = db.session.execute("SELECT to_regclass('public.chad_classes')").fetchone()
                if result[0] is None:
                    # Create chad_classes table
                    current_app.logger.warning("chad_classes table not found in PostgreSQL database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS chad_classes (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(50) UNIQUE NOT NULL,
                            description TEXT NOT NULL,
                            base_clout_bonus INTEGER DEFAULT 0,
                            base_roast_bonus INTEGER DEFAULT 0,
                            base_cringe_resistance_bonus INTEGER DEFAULT 0,
                            base_drip_bonus INTEGER DEFAULT 0
                        )
                    """)
                    # Insert default chad classes
                    db.session.execute("""
                        INSERT INTO chad_classes (name, description, base_clout_bonus, base_roast_bonus, 
                                              base_cringe_resistance_bonus, base_drip_bonus)
                        VALUES ('Sigma', 'The lone wolf with exceptional independence', 5, 3, 5, 2),
                               ('Alpha', 'The natural leader with commanding presence', 4, 4, 3, 4),
                               ('Gigachad', 'The ultimate form of masculinity', 5, 5, 5, 5)
                    """)
                    db.session.commit()
                
                # Check if chads table exists
                result = db.session.execute("SELECT to_regclass('public.chads')").fetchone()
                if result[0] is None:
                    # Create chads table
                    current_app.logger.warning("chads table not found in PostgreSQL database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS chads (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            class_id INTEGER NOT NULL,
                            name VARCHAR(50) NOT NULL,
                            avatar_locked BOOLEAN DEFAULT FALSE,
                            level INTEGER DEFAULT 1,
                            xp INTEGER DEFAULT 0,
                            clout INTEGER DEFAULT 10,
                            roast_level INTEGER DEFAULT 10,
                            cringe_resistance INTEGER DEFAULT 10,
                            drip_factor INTEGER DEFAULT 10,
                            battles_won INTEGER DEFAULT 0,
                            battles_lost INTEGER DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id),
                            FOREIGN KEY (class_id) REFERENCES chad_classes (id)
                        )
                    """)
                    db.session.commit()
                
                # Check if items table exists
                result = db.session.execute("SELECT to_regclass('public.items')").fetchone()
                if result[0] is None:
                    # Create items table
                    current_app.logger.warning("items table not found in PostgreSQL database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS items (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            chad_id INTEGER,
                            waifu_id INTEGER,
                            item_type_id INTEGER NOT NULL,
                            name VARCHAR(50) NOT NULL,
                            is_equipped BOOLEAN DEFAULT FALSE,
                            type VARCHAR(50),
                            clout_bonus INTEGER DEFAULT 0,
                            roast_bonus INTEGER DEFAULT 0,
                            cringe_resistance_bonus INTEGER DEFAULT 0,
                            drip_bonus INTEGER DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id),
                            FOREIGN KEY (chad_id) REFERENCES chads (id)
                        )
                    """)
                    db.session.commit()
                
                # Check if battles table exists
                result = db.session.execute("SELECT to_regclass('public.battles')").fetchone()
                if result[0] is None:
                    # Create battles table
                    current_app.logger.warning("battles table not found in PostgreSQL database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS battles (
                            id SERIAL PRIMARY KEY,
                            battle_type VARCHAR(20) NOT NULL,
                            status VARCHAR(20) NOT NULL,
                            initiator_id INTEGER NOT NULL,
                            initiator_chad_id INTEGER NOT NULL,
                            opponent_id INTEGER,
                            opponent_chad_id INTEGER,
                            npc_opponent_id INTEGER,
                            wager_amount INTEGER DEFAULT 0,
                            turn_count INTEGER DEFAULT 0,
                            current_turn INTEGER DEFAULT 0,
                            winner_id INTEGER,
                            loser_id INTEGER,
                            battle_log TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            started_at TIMESTAMP,
                            completed_at TIMESTAMP,
                            FOREIGN KEY (initiator_id) REFERENCES users (id),
                            FOREIGN KEY (initiator_chad_id) REFERENCES chads (id),
                            FOREIGN KEY (opponent_id) REFERENCES users (id),
                            FOREIGN KEY (opponent_chad_id) REFERENCES chads (id),
                            FOREIGN KEY (winner_id) REFERENCES users (id),
                            FOREIGN KEY (loser_id) REFERENCES users (id)
                        )
                    """)
                    db.session.commit()
                
                # Check if inventories table exists
                result = db.session.execute("SELECT to_regclass('public.inventories')").fetchone()
                if result[0] is None:
                    # Create inventories table
                    current_app.logger.warning("inventories table not found in PostgreSQL database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS inventories (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                    db.session.commit()
                
                # Check if waifus table exists
                result = db.session.execute("SELECT to_regclass('public.waifus')").fetchone()
                if result[0] is None:
                    # Create waifu_rarities table first if it doesn't exist
                    rarity_result = db.session.execute("SELECT to_regclass('public.waifu_rarities')").fetchone()
                    if rarity_result[0] is None:
                        current_app.logger.warning("waifu_rarities table not found in PostgreSQL database, creating it...")
                        db.session.execute("""
                            CREATE TABLE IF NOT EXISTS waifu_rarities (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(50) UNIQUE NOT NULL,
                                description TEXT NOT NULL,
                                drop_rate FLOAT DEFAULT 0.0,
                                min_stat_bonus INTEGER DEFAULT 1,
                                max_stat_bonus INTEGER DEFAULT 5
                            )
                        """)
                        # Insert default rarities
                        db.session.execute("""
                            INSERT INTO waifu_rarities (name, description, drop_rate, min_stat_bonus, max_stat_bonus)
                            VALUES 
                                ('Common', 'Common waifus with minimal bonuses', 0.6, 1, 3),
                                ('Rare', 'Rare waifus with decent bonuses', 0.3, 2, 5),
                                ('Epic', 'Epic waifus with strong bonuses', 0.08, 3, 7),
                                ('Legendary', 'Legendary waifus with powerful bonuses', 0.02, 5, 10)
                        """)
                        db.session.commit()

                    # Create waifu_types table if it doesn't exist
                    types_result = db.session.execute("SELECT to_regclass('public.waifu_types')").fetchone()
                    if types_result[0] is None:
                        current_app.logger.warning("waifu_types table not found in PostgreSQL database, creating it...")
                        db.session.execute("""
                            CREATE TABLE IF NOT EXISTS waifu_types (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(50) UNIQUE NOT NULL,
                                description TEXT NOT NULL,
                                rarity_id INTEGER NOT NULL,
                                base_clout_bonus INTEGER DEFAULT 0,
                                base_roast_bonus INTEGER DEFAULT 0,
                                base_cringe_resistance_bonus INTEGER DEFAULT 0,
                                base_drip_bonus INTEGER DEFAULT 0,
                                FOREIGN KEY (rarity_id) REFERENCES waifu_rarities (id)
                            )
                        """)
                        # Insert default types
                        db.session.execute("""
                            INSERT INTO waifu_types (name, description, rarity_id, base_clout_bonus, base_roast_bonus, base_cringe_resistance_bonus, base_drip_bonus)
                            VALUES 
                                ('Tsundere', 'Cold on the outside, warm on the inside', 2, 1, 3, 1, 1),
                                ('Childhood Friend', 'Known you since forever', 1, 2, 1, 2, 1),
                                ('Gamer Girl', 'Loves video games and tech', 2, 1, 2, 2, 1)
                        """)
                        db.session.commit()
                    
                    # Create waifus table
                    current_app.logger.warning("waifus table not found in PostgreSQL database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS waifus (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            chad_id INTEGER,
                            waifu_type_id INTEGER NOT NULL,
                            name VARCHAR(50) NOT NULL,
                            is_equipped BOOLEAN DEFAULT FALSE,
                            level INTEGER DEFAULT 1,
                            xp INTEGER DEFAULT 0,
                            clout_bonus INTEGER DEFAULT 0,
                            roast_bonus INTEGER DEFAULT 0,
                            cringe_resistance_bonus INTEGER DEFAULT 0,
                            drip_bonus INTEGER DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id),
                            FOREIGN KEY (chad_id) REFERENCES chads (id),
                            FOREIGN KEY (waifu_type_id) REFERENCES waifu_types (id)
                        )
                    """)
                    db.session.commit()
                
                # Check if item_rarities table exists
                result = db.session.execute("SELECT to_regclass('public.item_rarities')").fetchone()
                if result[0] is None:
                    # Create item_rarities table
                    current_app.logger.warning("item_rarities table not found in PostgreSQL database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS item_rarities (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(50) UNIQUE NOT NULL,
                            description TEXT NOT NULL,
                            drop_rate FLOAT DEFAULT 0.0,
                            min_stat_bonus INTEGER DEFAULT 1,
                            max_stat_bonus INTEGER DEFAULT 5
                        )
                    """)
                    # Insert default rarities
                    db.session.execute("""
                        INSERT INTO item_rarities (name, description, drop_rate, min_stat_bonus, max_stat_bonus)
                        VALUES 
                            ('Common', 'Common items with minimal bonuses', 0.6, 1, 3),
                            ('Rare', 'Rare items with decent bonuses', 0.3, 2, 5),
                            ('Epic', 'Epic items with strong bonuses', 0.08, 3, 7),
                            ('Legendary', 'Legendary items with powerful bonuses', 0.02, 5, 10)
                    """)
                    db.session.commit()
                
                # Check if item_types table exists
                result = db.session.execute("SELECT to_regclass('public.item_types')").fetchone()
                if result[0] is None:
                    # Create item_types table
                    current_app.logger.warning("item_types table not found in PostgreSQL database, creating it...")
                    db.session.execute("""
                        CREATE TABLE IF NOT EXISTS item_types (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(50) UNIQUE NOT NULL,
                            description TEXT NOT NULL,
                            rarity_id INTEGER NOT NULL,
                            slot VARCHAR(50) NOT NULL,
                            base_clout_bonus INTEGER DEFAULT 0,
                            base_roast_bonus INTEGER DEFAULT 0,
                            base_cringe_resistance_bonus INTEGER DEFAULT 0,
                            base_drip_bonus INTEGER DEFAULT 0,
                            is_character_item BOOLEAN DEFAULT TRUE,
                            FOREIGN KEY (rarity_id) REFERENCES item_rarities (id)
                        )
                    """)
                    # Insert default types
                    db.session.execute("""
                        INSERT INTO item_types (name, description, rarity_id, slot, base_clout_bonus, base_roast_bonus, base_cringe_resistance_bonus, base_drip_bonus, is_character_item)
                        VALUES 
                            ('Snapback Cap', 'A stylish cap for your Chad', 1, 'head', 1, 0, 0, 2, TRUE),
                            ('Designer Shades', 'Luxury sunglasses', 2, 'accessory', 2, 0, 1, 3, TRUE),
                            ('Gold Chain', 'Bling for your neck', 2, 'neck', 3, 0, 0, 2, TRUE)
                    """)
                    db.session.commit()
            
            # Check if demo user exists - include all fields we'll need
            result = db.session.execute("""
                SELECT id, username, email, password_hash, display_name, bio, avatar_url, 
                       chadcoin_balance, wallet_address, wallet_type, x_username, x_id, 
                       x_displayname, x_profile_image, is_admin 
                FROM users WHERE x_username = 'demo_user'
            """).fetchone()
            
            if not result:
                # Create a demo user with direct SQL - include all fields
                current_app.logger.info("Creating demo user...")
                
                # Different syntax for SQLite vs PostgreSQL for BOOLEAN type
                is_admin_value = "1" if is_sqlite else "TRUE"
                timestamp_value = "CURRENT_TIMESTAMP" if is_postgresql else "datetime('now')"
                
                query = f"""
                    INSERT INTO users (
                        username, 
                        email, 
                        password_hash,
                        display_name,
                        bio,
                        avatar_url, 
                        chadcoin_balance,
                        wallet_address,
                        wallet_type,
                        x_id, 
                        x_username, 
                        x_displayname, 
                        x_profile_image, 
                        is_admin,
                        created_at,
                        updated_at
                    ) VALUES (
                        'demo_user', 
                        'demo@example.com', 
                        'pbkdf2:sha256:150000$abc123$abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789',
                        'Demo User',
                        'This is a demo user for Chad Battles.',
                        'https://example.com/avatar.jpg', 
                        1000,
                        NULL,
                        NULL, 
                        :x_id, 
                        'demo_user', 
                        'Demo User', 
                        'https://example.com/profile.jpg', 
                        {is_admin_value},
                        {timestamp_value},
                        {timestamp_value}
                    )
                """
                
                db.session.execute(query, {'x_id': str(uuid.uuid4())})
                db.session.commit()
                
                # Get the newly created user with all fields
                result = db.session.execute("""
                    SELECT id, username, email, password_hash, display_name, bio, avatar_url, 
                           chadcoin_balance, wallet_address, wallet_type, x_username, x_id, 
                           x_displayname, x_profile_image, is_admin 
                    FROM users WHERE x_username = 'demo_user'
                """).fetchone()
            
            # Get user ID from result
            user_id = result[0]
            
            # Check if user already has a Chad
            chad_exists = db.session.execute(f"SELECT COUNT(*) FROM chads WHERE user_id = {user_id}").fetchone()[0]
            
            # Create a Chad for the user if they don't have one
            if not chad_exists:
                current_app.logger.info(f"Creating demo Chad for user {user_id}")
                
                # Get the Gigachad class id
                class_result = db.session.execute("SELECT id FROM chad_classes WHERE name = 'Gigachad'").fetchone()
                if not class_result:
                    # If Gigachad class doesn't exist, get any class
                    class_result = db.session.execute("SELECT id FROM chad_classes LIMIT 1").fetchone()
                
                if class_result:
                    class_id = class_result[0]
                    
                    # Create a new Chad for the user
                    chad_query = f"""
                        INSERT INTO chads (
                            user_id,
                            class_id,
                            name,
                            level,
                            clout,
                            roast_level,
                            cringe_resistance,
                            drip_factor,
                            created_at,
                            updated_at
                        ) VALUES (
                            {user_id},
                            {class_id},
                            'DemoChad',
                            5,
                            15,
                            15,
                            15,
                            15,
                            {timestamp_value},
                            {timestamp_value}
                        )
                    """
                    db.session.execute(chad_query)
                    db.session.commit()
                    current_app.logger.info(f"Created Chad for user {user_id}")
                    
                    # Create an inventory for the user if it doesn't exist
                    inventory_exists = db.session.execute(f"SELECT COUNT(*) FROM inventories WHERE user_id = {user_id}").fetchone()[0]
                    if not inventory_exists:
                        inventory_query = f"""
                            INSERT INTO inventories (
                                user_id,
                                created_at,
                                updated_at
                            ) VALUES (
                                {user_id},
                                {timestamp_value},
                                {timestamp_value}
                            )
                        """
                        db.session.execute(inventory_query)
                        db.session.commit()
                        current_app.logger.info(f"Created inventory for user {user_id}")
            
            # Manually create a User instance with all required attributes
            current_app.logger.info(f"Logging in demo user with id: {result[0]}")
            demo_user = User(
                id=result[0],
                username=result[1], 
                email=result[2], 
                password_hash=result[3],
                display_name=result[4],
                bio=result[5],
                avatar_url=result[6],
                chadcoin_balance=result[7],
                wallet_address=result[8],
                wallet_type=result[9],
                x_username=result[10],
                x_id=result[11],
                x_displayname=result[12],
                x_profile_image=result[13],
                is_admin=result[14]
            )
            
            # Log in the demo user
            login_user(demo_user)
            flash('You have been logged in as a demo user.', 'success')
            
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            current_app.logger.error(f"Error during database operations: {str(e)}")
            import traceback
            current_app.logger.error(traceback.format_exc())
            flash(f"Login error: Database issue. Please contact support.", 'danger')
            return redirect(url_for('auth.login'))
            
    except Exception as e:
        current_app.logger.error(f"Unexpected error in twitter_login: {str(e)}")
        import traceback
        current_app.logger.error(traceback.format_exc())
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