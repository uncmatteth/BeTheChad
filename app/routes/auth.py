from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
import logging
import os
import tweepy
from datetime import datetime

# Create blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth')
logger = logging.getLogger(__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            logger.info(f"User {username} logged in successfully")
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            logger.warning(f"Failed login attempt for username: {username}")
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate input
        if not username or not email or not password:
            flash('All fields are required', 'danger')
            return render_template('auth/register.html')
            
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('auth/register.html')
            
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return render_template('auth/register.html')
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('auth/register.html')
        
        # Create new user
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now log in.', 'success')
            logger.info(f"New user registered: {username}")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during registration: {str(e)}")
            flash('An error occurred during registration', 'danger')
    
    return render_template('auth/register.html')

@auth.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html')

@auth.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    if request.method == 'POST':
        display_name = request.form.get('display_name')
        bio = request.form.get('bio')
        
        try:
            current_user.display_name = display_name
            current_user.bio = bio
            db.session.commit()
            flash('Profile updated successfully', 'success')
            return redirect(url_for('auth.profile'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating profile: {str(e)}")
            flash('An error occurred while updating your profile', 'danger')
    
    return render_template('auth/edit_profile.html')

@auth.route('/appeal-class', methods=['POST'])
@login_required
def appeal_class():
    """Handle class appeal requests for the Blockchain Detective class"""
    if not current_user.chad:
        flash('You need to create a Chad character first', 'warning')
        return redirect(url_for('auth.profile'))
    
    # Check if already Blockchain Detective
    if current_user.chad.chad_class.name == 'Blockchain Detective':
        flash('You already have the Blockchain Detective class', 'info')
        return redirect(url_for('auth.profile'))
    
    # Check if user has appealed within the last month
    from datetime import datetime, timedelta
    from app.models.appeal import ClassAppeal
    
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    recent_appeal = ClassAppeal.query.filter_by(
        user_id=current_user.id,
        created_at=one_month_ago
    ).first()
    
    if recent_appeal:
        flash('You can only submit one appeal per month. Please try again later.', 'warning')
        return redirect(url_for('auth.profile'))
    
    # Get form data
    experience = request.form.get('blockchain_experience')
    contributions = request.form.get('blockchain_contributions')
    evidence = request.form.get('blockchain_evidence')
    
    # Validate input
    if not experience or not contributions or not evidence:
        flash('All fields are required', 'danger')
        return redirect(url_for('auth.profile'))
    
    # Record the appeal
    try:
        from app.models.appeal import ClassAppeal
        
        # Create appeal record
        appeal = ClassAppeal(
            user_id=current_user.id,
            chad_id=current_user.chad.id,
            current_class=current_user.chad.chad_class.name,
            requested_class='Blockchain Detective',
            experience=experience,
            contributions=contributions,
            evidence=evidence,
            status='pending'
        )
        
        db.session.add(appeal)
        db.session.commit()
        
        # Notify admins (would implement email/notification system)
        logger.info(f"New class appeal from {current_user.username} for Blockchain Detective class")
        
        flash('Your class appeal has been submitted for review. You will be notified of the decision.', 'success')
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error submitting class appeal: {str(e)}")
        flash('An error occurred while submitting your appeal', 'danger')
    
    return redirect(url_for('auth.profile'))

@auth.route('/twitter-login')
def twitter_login():
    """Initiate Twitter login."""
    try:
        # First check if Twitter credentials are configured
        api_key = os.environ.get('TWITTER_API_KEY')
        api_secret = os.environ.get('TWITTER_API_SECRET')
        
        if not api_key or not api_secret:
            logger.error("Twitter API credentials not configured")
            flash('Twitter login is not configured. Please try again later.', 'danger')
            return redirect(url_for('auth.login'))
        
        try:
            # Get environment-specific callback URL
            if os.environ.get('FLASK_ENV') == 'development':
                callback_url = os.environ.get('DEV_CALLBACK_URL', 'http://127.0.0.1:5000/auth/twitter-callback')
            else:
                callback_url = os.environ.get('PROD_CALLBACK_URL', 'https://chadbattles.fun/auth/twitter-callback')
            
            # Create OAuth handler with callback
            auth = tweepy.OAuth1UserHandler(
                api_key, api_secret,
                callback=callback_url
            )
            
            # Get request token
            redirect_url = auth.get_authorization_url()
            
            # Store request token in session for verification in callback
            session['request_token'] = auth.request_token
            
            # Log callback URL for debugging
            logger.info(f"Using callback URL: {callback_url}")
            
            # Redirect to Twitter authorization URL
            return redirect(redirect_url)
        except Exception as e:
            logger.error(f"Twitter OAuth error: {str(e)}")
            flash('Error connecting to Twitter. Please try again.', 'danger')
            return redirect(url_for('auth.login'))
            
    except Exception as e:
        logger.error(f"Unexpected error in twitter_login: {str(e)}")
        flash('An error occurred. Please try again.', 'danger')
        return redirect(url_for('auth.login'))

@auth.route('/twitter-callback')
def twitter_callback():
    """Handle Twitter OAuth callback."""
    try:
        # Get OAuth verifier from the callback
        oauth_verifier = request.args.get('oauth_verifier')
        
        # Check if we have a request token in session
        request_token = session.get('request_token')
        
        if not oauth_verifier or not request_token:
            flash('Authentication failed: Missing OAuth parameters', 'danger')
            logger.error(f"Twitter callback missing parameters: verifier={oauth_verifier}, token={request_token}")
            return redirect(url_for('auth.login'))
        
        try:
            # Get Twitter API credentials
            api_key = os.environ.get('TWITTER_API_KEY')
            api_secret = os.environ.get('TWITTER_API_SECRET')
            
            # Set up auth handler with request token
            auth = tweepy.OAuth1UserHandler(api_key, api_secret)
            auth.request_token = request_token
            
            # Get access token
            access_token, access_token_secret = auth.get_access_token(oauth_verifier)
            
            # Create API instance
            api = tweepy.API(auth)
            
            # Get user profile
            twitter_user = api.verify_credentials()
            
            if not twitter_user:
                flash('Could not verify Twitter credentials', 'danger')
                return redirect(url_for('auth.login'))
            
            # Get or create user
            user = User.query.filter_by(x_id=twitter_user.id_str).first()
            
            if not user:
                # Create new user
                user = User(
                    x_id=twitter_user.id_str,
                    x_username=twitter_user.screen_name,
                    x_displayname=twitter_user.name,
                    x_profile_image=twitter_user.profile_image_url_https,
                    username=f"user_{twitter_user.id_str}",  # Generate a username
                    email=f"{twitter_user.screen_name}@example.com",  # Placeholder email
                    chadcoin_balance=100  # Starting balance
                )
                db.session.add(user)
                db.session.commit()
                
                # Log the new user creation
                logger.info(f"Created new user from Twitter: {twitter_user.screen_name}")
                flash('Account created successfully!', 'success')
            else:
                # Update existing user data
                user.x_username = twitter_user.screen_name
                user.x_displayname = twitter_user.name
                user.x_profile_image = twitter_user.profile_image_url_https
                db.session.commit()
            
            # Login the user
            login_user(user)
            
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Clear session request token
            if 'request_token' in session:
                del session['request_token']
            
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            logger.error(f"Twitter API error in callback: {str(e)}")
            flash('Error processing Twitter authentication', 'danger')
            return redirect(url_for('auth.login'))
            
    except Exception as e:
        logger.error(f"Error in Twitter callback: {str(e)}")
        flash('Authentication failed. Please try again.', 'danger')
        return redirect(url_for('auth.login')) 