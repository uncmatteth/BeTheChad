from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
import logging

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