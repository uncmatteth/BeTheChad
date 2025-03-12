from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from flask_wtf.csrf import CSRFProtect, generate_csrf
from app import db, cache
from app.models.cabal import Cabal, CabalMember, CabalOfficerRole, CabalVote, CabalBattle, CabalBattleParticipant
from datetime import datetime, timedelta
import re
from werkzeug.utils import escape
import bleach

cabal_bp = Blueprint('cabal', __name__)

# Helper function for input validation
def validate_uuid(uuid_str):
    """Validate a UUID string format"""
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return re.match(uuid_pattern, uuid_str, re.I) is not None

def sanitize_input(input_str):
    """Sanitize user input to prevent XSS"""
    if input_str is None:
        return ''
    return bleach.clean(input_str.strip(), tags=[], strip=True)

@cabal_bp.route('/')
@login_required
def index():
    """Display the user's cabal"""
    cabals = Cabal.query.filter_by(leader_id=current_user.chad.id).all()
    
    # Also check if user is a member of a cabal
    cabal_member = CabalMember.query.filter_by(chad_id=current_user.chad.id).first()
    if cabal_member:
        cabal = cabal_member.cabal
        
        # Get officers
        officers = {}
        for role_type in ['clout', 'roast_level', 'cringe_resistance', 'drip_factor']:
            officer_role = cabal.get_officer(role_type)
            if officer_role:
                from app.models.chad import Chad
                officer_chad = Chad.query.get(officer_role.chad_id)
                if officer_chad:
                    from app.models.user import User
                    officer_user = User.query.filter_by(chad_id=officer_chad.id).first()
                    officers[role_type] = {
                        'id': officer_chad.id,
                        'name': officer_chad.name,
                        'username': officer_user.twitter_handle if officer_user else 'Unknown',
                        'title': cabal.get_officer_title(role_type)
                    }
        
        # Get vote counts for leader removal
        leader_removal_votes = CabalVote.query.filter_by(
            cabal_id=cabal.id,
            vote_type='remove_leader',
            target_id=cabal.leader_id
        ).count()
        
        active_members_count = cabal.get_active_member_count()
        removal_vote_percentage = (leader_removal_votes / active_members_count * 100) if active_members_count > 0 else 0
        
        # Get scheduled battles
        upcoming_battles = CabalBattle.query.filter_by(
            cabal_id=cabal.id,
            completed=False
        ).filter(
            CabalBattle.scheduled_at > datetime.utcnow()
        ).order_by(CabalBattle.scheduled_at).all()
        
        # Check if user has voted for leader removal
        user_voted = CabalVote.query.filter_by(
            cabal_id=cabal.id,
            voter_id=current_user.chad.id,
            vote_type='remove_leader',
            target_id=cabal.leader_id
        ).first() is not None
        
        # Add current datetime for template
        now = datetime.utcnow()
        
        # Get leader information
        from app.models.chad import Chad
        from app.models.user import User
        
        leader = Chad.query.get(cabal.leader_id)
        if leader:
            leader.user = User.query.filter_by(chad_id=leader.id).first()
        
        cabal.leader = leader
        
        return render_template('cabal/index.html', 
                              cabal=cabal,
                              officers=officers,
                              leader_removal_votes=leader_removal_votes,
                              removal_vote_percentage=removal_vote_percentage,
                              upcoming_battles=upcoming_battles,
                              user_voted=user_voted,
                              is_leader=(cabal.leader_id == current_user.chad.id),
                              now=now)
    
    return render_template('cabal/index.html', cabal=None)

@cabal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new cabal"""
    if request.method == 'POST':
        # CSRF validation
        if 'csrf_token' not in request.form or not CSRFProtect().validate_csrf(request.form['csrf_token']):
            flash('CSRF token validation failed. Please try again.', 'danger')
            return redirect(url_for('cabal.create'))
            
        # Get form data with proper validation
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        # Enhanced validation
        if not name:
            flash('Cabal name is required', 'danger')
            return redirect(url_for('cabal.create'))
            
        # Check for malicious content
        if '<script' in name.lower() or '<script' in description.lower():
            flash('Invalid characters detected in input', 'danger')
            return redirect(url_for('cabal.create'))
        
        # Validate against regex patterns
        name_pattern = r'^[A-Za-z0-9\s\-_\.]{1,50}$'
        if not re.match(name_pattern, name):
            flash('Cabal name can only contain alphanumeric characters, spaces, hyphens, underscores, and periods', 'danger')
            return redirect(url_for('cabal.create'))
        
        # Sanitize inputs - use bleach instead of escape for better sanitization
        name = bleach.clean(name, tags=[], strip=True)
        description = bleach.clean(description, tags=[], strip=True)
        
        # Check length constraints
        if len(name) > 50:
            flash('Cabal name must be 50 characters or less', 'danger')
            return redirect(url_for('cabal.create'))
            
        if len(description) > 500:
            flash('Description must be 500 characters or less', 'danger')
            return redirect(url_for('cabal.create'))
        
        # Check if user is already in a cabal
        existing_membership = CabalMember.query.filter_by(chad_id=current_user.chad.id).first()
        if existing_membership:
            flash('You are already in a cabal', 'danger')
            return redirect(url_for('cabal.index'))
        
        # Check if cabal name is taken
        existing_cabal = Cabal.query.filter_by(name=name).first()
        if existing_cabal:
            flash('A cabal with this name already exists', 'danger')
            return redirect(url_for('cabal.create'))
        
        # Use a transaction to ensure data consistency
        try:
            cabal = Cabal(
                name=name,
                description=description,
                leader_id=current_user.chad.id
            )
            
            db.session.add(cabal)
            
            # Create the first member entry (the leader)
            success, message = cabal.add_member(current_user.chad.id)
            if not success:
                db.session.rollback()
                flash(f'Failed to add leader as member: {message}', 'danger')
                return redirect(url_for('cabal.create'))
            
            # Commit the transaction
            db.session.commit()
            
            flash('Cabal created successfully!', 'success')
            return redirect(url_for('cabal.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('cabal.create'))
    
    return render_template('cabal/create.html')

@cabal_bp.route('/join', methods=['GET', 'POST'])
@login_required
def join():
    """Join a cabal using an invite code"""
    if not current_user.chad:
        flash('You need to create a character first', 'danger')
        return redirect(url_for('main.index'))
    
    existing_membership = CabalMember.query.filter_by(chad_id=current_user.chad.id).first()
    if existing_membership:
        flash('You are already in a cabal', 'danger')
        return redirect(url_for('cabal.index'))
    
    if request.method == 'POST':
        # CSRF validation
        if 'csrf_token' not in request.form or not CSRFProtect().validate_csrf(request.form['csrf_token']):
            flash('CSRF token validation failed. Please try again.', 'danger')
            return redirect(url_for('cabal.index'))
            
        # Get and clean invite code with enhanced validation
        invite_code_raw = request.form.get('invite_code', '').strip()
        
        # Initial validation
        if not invite_code_raw:
            flash('Invite code is required', 'danger')
            return redirect(url_for('cabal.index'))
        
        # Check for potential script injection
        if '<' in invite_code_raw or '>' in invite_code_raw:
            flash('Invalid characters in invite code', 'danger')
            return redirect(url_for('cabal.index'))
            
        # Sanitize and normalize - uppercase for consistency
        invite_code = bleach.clean(invite_code_raw, tags=[], strip=True).upper()
        
        # Strict format validation with regex
        if not re.match(r'^[A-Z0-9]{6}$', invite_code):
            flash('Invalid invite code format - must be 6 alphanumeric characters', 'danger')
            return redirect(url_for('cabal.index'))
        
        # Find the cabal
        cabal = Cabal.query.filter_by(invite_code=invite_code).first()
        if not cabal:
            flash('Invalid invite code - cabal not found', 'danger')
            return redirect(url_for('cabal.index'))
        
        # Check for referrer
        referrer_username = request.form.get('referrer', '').strip()
        referrer_id = None
        
        if referrer_username:
            # Sanitize referrer username
            referrer_username = sanitize_input(referrer_username)
            
            # Find the referrer user
            from app.models.user import User
            referrer_user = User.query.filter_by(twitter_handle=referrer_username).first()
            
            if referrer_user and referrer_user.chad:
                referrer_id = referrer_user.chad.id
        
        # Use transaction management
        try:
            # Add the user to the cabal
            success, message = cabal.add_member(current_user.chad.id)
            
            if not success:
                flash(message, 'danger')
                return redirect(url_for('cabal.index'))
            
            # Award referral bonus if applicable
            if referrer_id:
                # Check if referrer is in the same cabal
                referrer_membership = CabalMember.query.filter_by(
                    cabal_id=cabal.id,
                    chad_id=referrer_id
                ).first()
                
                if referrer_membership:
                    # Award contribution points to referrer
                    referrer_membership.increase_contribution(50)
                    
                    # Award XP to the cabal
                    cabal.add_xp(100)
                    
                    # Award chadcoin to referrer
                    from app.models.transaction import Transaction, TransactionType
                    Transaction.create(
                        transaction_type=TransactionType.REFERRAL_BONUS.value,
                        amount=50,
                        to_user_id=referrer_user.id,
                        description=f"Referral bonus for {current_user.username} joining {cabal.name}"
                    )
                    
                    # Log the referral
                    from app.models.referral import Referral
                    referral = Referral(
                        referrer_id=referrer_id,
                        referred_id=current_user.chad.id,
                        cabal_id=cabal.id
                    )
                    db.session.add(referral)
            
            # Commit changes
            db.session.commit()
            
            flash(f'You have successfully joined {cabal.name}!', 'success')
            return redirect(url_for('cabal.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error joining cabal: {str(e)}', 'danger')
            return redirect(url_for('cabal.index'))
    
    # Handle GET with code param (from invitation link)
    code = request.args.get('code')
    referrer = request.args.get('ref')
    
    if code:
        # Sanitize and validate input
        code_clean = bleach.clean(code.strip(), tags=[], strip=True).upper()
        
        # Validate format
        if not re.match(r'^[A-Z0-9]{6}$', code_clean):
            flash('Invalid invite code format - must be 6 alphanumeric characters', 'danger')
            return redirect(url_for('cabal.index'))
        
        # Find the cabal
        cabal = Cabal.query.filter_by(invite_code=code_clean).first()
        if not cabal:
            flash('Invalid invite code - cabal not found', 'danger')
            return redirect(url_for('cabal.index'))
        
        # Check for referrer
        referrer_id = None
        if referrer:
            # Sanitize referrer username
            referrer_clean = sanitize_input(referrer)
            
            # Find the referrer user
            from app.models.user import User
            referrer_user = User.query.filter_by(twitter_handle=referrer_clean).first()
            
            if referrer_user and referrer_user.chad:
                referrer_id = referrer_user.chad.id
        
        # Use transaction management
        try:
            # Add the user to the cabal
            success, message = cabal.add_member(current_user.chad.id)
            
            if not success:
                flash(message, 'danger')
                return redirect(url_for('cabal.index'))
            
            # Award referral bonus if applicable
            if referrer_id:
                # Check if referrer is in the same cabal
                referrer_membership = CabalMember.query.filter_by(
                    cabal_id=cabal.id,
                    chad_id=referrer_id
                ).first()
                
                if referrer_membership:
                    # Award contribution points to referrer
                    referrer_membership.increase_contribution(50)
                    
                    # Award XP to the cabal
                    cabal.add_xp(100)
                    
                    # Award chadcoin to referrer
                    from app.models.transaction import Transaction, TransactionType
                    Transaction.create(
                        transaction_type=TransactionType.REFERRAL_BONUS.value,
                        amount=50,
                        to_user_id=referrer_user.id,
                        description=f"Referral bonus for {current_user.username} joining {cabal.name}"
                    )
                    
                    # Log the referral
                    from app.models.referral import Referral
                    referral = Referral(
                        referrer_id=referrer_id,
                        referred_id=current_user.chad.id,
                        cabal_id=cabal.id
                    )
                    db.session.add(referral)
            
            # Commit changes
            db.session.commit()
            
            flash(f'You have successfully joined {cabal.name}!', 'success')
            return redirect(url_for('cabal.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error joining cabal: {str(e)}', 'danger')
            return redirect(url_for('cabal.index'))
    
    return redirect(url_for('cabal.index'))

@cabal_bp.route('/<cabal_id>/leave')
@login_required
def leave(cabal_id):
    """Leave a cabal"""
    cabal = Cabal.query.get_or_404(cabal_id)
    
    # Cannot leave if you're the leader
    if cabal.leader_id == current_user.chad.id:
        flash('The cabal leader cannot leave. Disband the cabal or transfer leadership first.', 'danger')
        return redirect(url_for('cabal.index'))
    
    # Use transaction management
    try:
        success, message = cabal.remove_member(current_user.chad.id)
        
        if not success:
            flash(message, 'danger')
            return redirect(url_for('cabal.index'))
            
        # Commit changes
        db.session.commit()
        
        flash('You have left the cabal', 'success')
        return redirect(url_for('cabal.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error leaving cabal: {str(e)}', 'danger')
        return redirect(url_for('cabal.index'))

@cabal_bp.route('/<cabal_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(cabal_id):
    """Edit cabal details"""
    # Validate cabal_id
    if not validate_uuid(cabal_id):
        flash('Invalid cabal ID format', 'danger')
        return redirect(url_for('cabal.index'))
        
    cabal = get_cabal_by_id(cabal_id)
    if not cabal:
        flash('Cabal not found', 'danger')
        return redirect(url_for('cabal.index'))
    
    # Only the leader can edit the cabal
    if cabal.leader_id != current_user.chad.id:
        flash('Only the cabal leader can edit cabal details', 'danger')
        return redirect(url_for('cabal.index'))
    
    if request.method == 'POST':
        # CSRF validation
        if 'csrf_token' not in request.form or not CSRFProtect().validate_csrf(request.form['csrf_token']):
            flash('CSRF token validation failed. Please try again.', 'danger')
            return redirect(url_for('cabal.edit', cabal_id=cabal_id))
            
        # Get and validate form data
        name_raw = request.form.get('name', '').strip()
        description_raw = request.form.get('description', '').strip()
        
        # Enhanced validation
        if not name_raw:
            flash('Cabal name is required', 'danger')
            return redirect(url_for('cabal.edit', cabal_id=cabal_id))
            
        # Check for potentially malicious content
        if '<script' in name_raw.lower() or '<script' in description_raw.lower():
            flash('Invalid characters detected in input', 'danger')
            return redirect(url_for('cabal.edit', cabal_id=cabal_id))
        
        # Validate name against pattern
        name_pattern = r'^[A-Za-z0-9\s\-_\.]{1,50}$'
        if not re.match(name_pattern, name_raw):
            flash('Cabal name can only contain alphanumeric characters, spaces, hyphens, underscores, and periods', 'danger')
            return redirect(url_for('cabal.edit', cabal_id=cabal_id))
        
        # Sanitize inputs
        name = bleach.clean(name_raw, tags=[], strip=True)
        description = bleach.clean(description_raw, tags=[], strip=True)
        
        # Check length constraints
        if len(name) > 50:
            flash('Cabal name must be 50 characters or less', 'danger')
            return redirect(url_for('cabal.edit', cabal_id=cabal_id))
            
        if len(description) > 500:
            flash('Description must be 500 characters or less', 'danger')
            return redirect(url_for('cabal.edit', cabal_id=cabal_id))
        
        # Check for name conflicts with other cabals
        existing_cabal = Cabal.query.filter(Cabal.name == name, Cabal.id != cabal.id).first()
        if existing_cabal:
            flash('A cabal with this name already exists', 'danger')
            return redirect(url_for('cabal.edit', cabal_id=cabal_id))
        
        # Use a transaction to ensure data consistency
        try:
            cabal.name = name
            cabal.description = description
            
            # Commit the transaction
            db.session.commit()
            
            # Invalidate the cache for this cabal
            invalidate_cabal_cache(cabal_id)
            
            flash('Cabal updated successfully', 'success')
            return redirect(url_for('cabal.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating cabal: {str(e)}', 'danger')
            return redirect(url_for('cabal.edit', cabal_id=cabal_id))
    
    return render_template('cabal/edit.html', cabal=cabal)

@cabal_bp.route('/<cabal_id>/battles')
@login_required
def battles(cabal_id):
    """View cabal battles"""
    cabal = Cabal.query.get_or_404(cabal_id)
    
    from app.models.battle import Battle
    battles = Battle.get_cabal_battle_history(cabal_id)
    
    return render_template('cabal/battles.html', cabal=cabal, battles=battles)

@cabal_bp.route('/<cabal_id>/remove_member')
@login_required
def remove_member(cabal_id):
    """Remove a member from the cabal"""
    # Validate cabal_id
    if not validate_uuid(cabal_id):
        flash('Invalid cabal ID format', 'danger')
        return redirect(url_for('cabal.index'))
        
    cabal = Cabal.query.get_or_404(cabal_id)
    
    # Only leader can remove members
    if cabal.leader_id != current_user.chad.id:
        flash('Only the cabal leader can remove members', 'danger')
        return redirect(url_for('cabal.index'))
    
    chad_id = request.args.get('chad_id')
    if not chad_id:
        flash('Member ID is required', 'danger')
        return redirect(url_for('cabal.index'))
    
    # Validate UUID format
    if not validate_uuid(chad_id):
        flash('Invalid member ID format', 'danger')
        return redirect(url_for('cabal.index'))
    
    # Use transaction management
    try:
        success, message = cabal.remove_member(chad_id)
        
        if not success:
            flash(message, 'danger')
            return redirect(url_for('cabal.index'))
            
        # Commit changes
        db.session.commit()
        
        flash('Member removed successfully', 'success')
        return redirect(url_for('cabal.index'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error removing member: {str(e)}', 'danger')
        return redirect(url_for('cabal.index'))

@cabal_bp.route('/<cabal_id>/promote_leader')
@login_required
def promote_leader(cabal_id):
    """Promote a member to cabal leader"""
    cabal = Cabal.query.get_or_404(cabal_id)
    
    # Only current leader can promote
    if cabal.leader_id != current_user.chad.id:
        flash('Only the cabal leader can promote members', 'danger')
        return redirect(url_for('cabal.index'))
    
    chad_id = request.args.get('chad_id')
    if not chad_id:
        flash('Member ID is required', 'danger')
        return redirect(url_for('cabal.index'))
    
    # Validate UUID format
    if not validate_uuid(chad_id):
        flash('Invalid member ID format', 'danger')
        return redirect(url_for('cabal.index'))
    
    success, message = cabal.change_leader(chad_id)
    
    if success:
        flash('Leadership transferred successfully', 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('cabal.index'))

@cabal_bp.route('/<cabal_id>/disband')
@login_required
def disband(cabal_id):
    """Disband the cabal"""
    cabal = Cabal.query.get_or_404(cabal_id)
    
    # Only leader can disband
    if cabal.leader_id != current_user.chad.id:
        flash('Only the cabal leader can disband the cabal', 'danger')
        return redirect(url_for('cabal.index'))
    
    success, message = cabal.disband()
    
    if success:
        flash('Cabal disbanded successfully', 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('cabal.index'))

@cabal_bp.route('/<cabal_id>/appoint_officer', methods=['POST'])
@login_required
def appoint_officer(cabal_id):
    """Appoint an officer to a specific role in the cabal"""
    # Validate cabal_id
    if not validate_uuid(cabal_id):
        flash('Invalid cabal ID format', 'danger')
        return redirect(url_for('cabal.index'))
        
    cabal = Cabal.query.get_or_404(cabal_id)
    
    # Only the cabal leader can appoint officers
    if cabal.leader_id != current_user.chad.id:
        flash('Only the Lord of the Shill can appoint officers', 'danger')
        return redirect(url_for('cabal.index'))
    
    # CSRF validation
    if 'csrf_token' not in request.form or not CSRFProtect().validate_csrf(request.form['csrf_token']):
        flash('CSRF token validation failed. Please try again.', 'danger')
        return redirect(url_for('cabal.index'))
        
    # Get and validate form data
    chad_id_raw = request.form.get('chad_id', '').strip()
    role_type_raw = request.form.get('role_type', '').strip()
    
    # Basic validation
    if not chad_id_raw or not role_type_raw:
        flash('Member ID and role type are required', 'danger')
        return redirect(url_for('cabal.index'))
    
    # Sanitize inputs
    chad_id = sanitize_input(chad_id_raw)
    role_type = sanitize_input(role_type_raw)
    
    # Validate UUID format for chad_id with enhanced regex
    if not validate_uuid(chad_id):
        flash('Invalid member ID format', 'danger')
        return redirect(url_for('cabal.index'))
    
    # Validate role_type with strict inclusion check
    valid_roles = ['clout', 'roast_level', 'cringe_resistance', 'drip_factor']
    if role_type not in valid_roles:
        flash('Invalid role type', 'danger')
        return redirect(url_for('cabal.index'))
        
    # Additional validation to ensure the chad exists and is a member
    member = CabalMember.query.filter_by(cabal_id=cabal_id, chad_id=chad_id).first()
    if not member:
        flash('Selected member is not in your cabal', 'danger')
        return redirect(url_for('cabal.index'))
        
    # Use transaction management
    try:
        success, message = cabal.appoint_officer(chad_id, role_type)
        
        if success:
            db.session.commit()
            flash(message, 'success')
        else:
            flash(message, 'danger')
        
        return redirect(url_for('cabal.index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error appointing officer: {str(e)}', 'danger')
        return redirect(url_for('cabal.index'))

@cabal_bp.route('/<cabal_id>/remove_officer/<role_type>')
@login_required
def remove_officer(cabal_id, role_type):
    """Remove an officer from their role"""
    cabal = Cabal.query.get_or_404(cabal_id)
    
    # Only leader can remove officers
    if cabal.leader_id != current_user.chad.id:
        flash('Only the Lord of the Shill can remove officers', 'danger')
        return redirect(url_for('cabal.index'))
    
    # Validate role_type
    valid_roles = ['clout', 'roast_level', 'cringe_resistance', 'drip_factor']
    if role_type not in valid_roles:
        flash('Invalid role type', 'danger')
        return redirect(url_for('cabal.index'))
    
    success, message = cabal.remove_officer(role_type)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('cabal.index'))

@cabal_bp.route('/<cabal_id>/vote_remove_leader')
@login_required
def vote_remove_leader(cabal_id):
    """Vote to remove the current cabal leader"""
    cabal = Cabal.query.get_or_404(cabal_id)
    
    # Leader can't vote to remove themselves
    if cabal.leader_id == current_user.chad.id:
        flash('You cannot vote to remove yourself as leader', 'danger')
        return redirect(url_for('cabal.index'))
    
    success, message = cabal.vote_to_remove_leader(current_user.chad.id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('cabal.index'))

@cabal_bp.route('/<cabal_id>/schedule_battle', methods=['GET', 'POST'])
@login_required
def schedule_battle(cabal_id):
    """Schedule a battle with another cabal"""
    # Validate cabal_id
    if not validate_uuid(cabal_id):
        flash('Invalid cabal ID format', 'danger')
        return redirect(url_for('cabal.index'))
        
    now = datetime.utcnow()
    cabal = Cabal.query.get_or_404(cabal_id)
    
    # Only the leader can schedule battles
    if cabal.leader_id != current_user.chad.id:
        flash('Only the Lord of the Shill can schedule battles', 'danger')
        return redirect(url_for('cabal.index'))
    
    if request.method == 'POST':
        # CSRF validation
        if 'csrf_token' not in request.form or not CSRFProtect().validate_csrf(request.form['csrf_token']):
            flash('CSRF token validation failed. Please try again.', 'danger')
            return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))
            
        # Get and validate form data
        opponent_cabal_id_raw = request.form.get('opponent_cabal_id', '').strip()
        battle_date_raw = request.form.get('battle_date', '').strip()
        battle_time_raw = request.form.get('battle_time', '').strip()
        
        # Basic validation for required fields
        if not opponent_cabal_id_raw or not battle_date_raw or not battle_time_raw:
            flash('All fields are required', 'danger')
            return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))
        
        # Sanitize inputs
        opponent_cabal_id = sanitize_input(opponent_cabal_id_raw)
        battle_date = sanitize_input(battle_date_raw)
        battle_time = sanitize_input(battle_time_raw)
        
        # Validate UUID format for opponent_cabal_id
        if opponent_cabal_id != "random" and not validate_uuid(opponent_cabal_id):
            flash('Invalid opponent cabal ID format', 'danger')
            return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))
        
        # Enhanced validation for date and time formats
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        time_pattern = r'^\d{2}:\d{2}$'
        
        if not re.match(date_pattern, battle_date):
            flash('Invalid date format. Use YYYY-MM-DD', 'danger')
            return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))
            
        if not re.match(time_pattern, battle_time):
            flash('Invalid time format. Use HH:MM in 24-hour format', 'danger')
            return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))
        
        # Additional validation for date range and logical consistency
        try:
            year, month, day = map(int, battle_date.split('-'))
            hour, minute = map(int, battle_time.split(':'))
            
            # Verify date components are in valid ranges
            if not (1 <= month <= 12 and 1 <= day <= 31 and 0 <= hour <= 23 and 0 <= minute <= 59):
                flash('Invalid date or time values', 'danger')
                return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))
                
            # Create datetime object for scheduled time
            scheduled_at = datetime(year, month, day, hour, minute)
            
            # Ensure battle is scheduled in the future
            if scheduled_at <= now:
                flash('Battles must be scheduled in the future', 'danger')
                return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))
                
            # Ensure battle is not scheduled too far in the future (e.g., max 2 weeks)
            max_future = now + timedelta(days=14)
            if scheduled_at > max_future:
                flash('Battles cannot be scheduled more than 2 weeks in advance', 'danger')
                return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))
                
        except ValueError:
            flash('Invalid date or time values', 'danger')
            return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))
        
        # Check if opponent cabal exists
        opponent_cabal = Cabal.query.get(opponent_cabal_id)
        if not opponent_cabal:
            flash('Opponent cabal not found', 'danger')
            return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))
        
        # Schedule the battle
        success, message = cabal.schedule_battle(opponent_cabal_id, scheduled_at)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('cabal.index'))
        else:
            flash(message, 'danger')
            return redirect(url_for('cabal.schedule_battle', cabal_id=cabal_id))
    
    # Get all other cabals for the opponent selection dropdown
    other_cabals = Cabal.query.filter(Cabal.id != cabal_id).all()
    
    # Get battle count for this week
    battles_this_week = CabalBattle.count_battles_this_week(cabal_id)
    battles_remaining = 3 - battles_this_week
    
    # Add current datetime for template
    now = datetime.utcnow()
    
    return render_template('cabal/schedule_battle.html', 
                          cabal=cabal, 
                          other_cabals=other_cabals,
                          battles_this_week=battles_this_week,
                          battles_remaining=battles_remaining,
                          now=now)

@cabal_bp.route('/battle/<battle_id>/opt_in')
@login_required
def opt_into_battle(battle_id):
    """Opt into participating in a cabal battle"""
    battle = CabalBattle.query.get_or_404(battle_id)
    
    # Check if user is in the cabal
    cabal_member = CabalMember.query.filter_by(
        chad_id=current_user.chad.id,
        cabal_id=battle.cabal_id
    ).first()
    
    if not cabal_member:
        flash('You are not a member of this cabal', 'danger')
        return redirect(url_for('cabal.index'))
    
    # Try to opt in
    success, message = cabal_member.opt_into_battle(battle_id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('cabal.index'))

@cabal_bp.route('/battles')
@login_required
def all_battles():
    """View all upcoming cabal battles"""
    # Get user's cabal
    cabal_member = CabalMember.query.filter_by(chad_id=current_user.chad.id).first()
    
    if not cabal_member:
        flash('You are not a member of a cabal', 'danger')
        return redirect(url_for('cabal.index'))
    
    # Get upcoming battles for user's cabal
    upcoming_battles = CabalBattle.query.filter_by(
        cabal_id=cabal_member.cabal_id,
        completed=False
    ).filter(
        CabalBattle.scheduled_at > datetime.utcnow()
    ).order_by(CabalBattle.scheduled_at).all()
    
    # Get past battles
    past_battles = CabalBattle.query.filter_by(
        cabal_id=cabal_member.cabal_id,
        completed=True
    ).order_by(CabalBattle.scheduled_at.desc()).limit(10).all()
    
    # Check which battles the user has opted into
    opted_battles = set()
    for battle in upcoming_battles:
        participant = CabalBattleParticipant.query.filter_by(
            battle_id=battle.id,
            chad_id=current_user.chad.id
        ).first()
        
        if participant:
            opted_battles.add(battle.id)
    
    # Add current datetime for template
    now = datetime.utcnow()
    
    return render_template('cabal/all_battles.html',
                          cabal=cabal_member.cabal,
                          upcoming_battles=upcoming_battles,
                          past_battles=past_battles,
                          opted_battles=opted_battles,
                          now=now)

@cabal_bp.route('/leaderboard')
def leaderboard():
    """Display the cabal leaderboard"""
    # Get top 20 cabals by power
    top_cabals = Cabal.get_leaderboard(limit=20)
    
    # For each cabal, get the leader's name
    from app.models.chad import Chad
    from app.models.user import User
    
    cabal_data = []
    for cabal in top_cabals:
        # Update rank
        cabal.update_rank()
        
        # Get leader
        leader_chad = Chad.query.get(cabal.leader_id)
        if leader_chad:
            leader_user = User.query.filter_by(chad_id=leader_chad.id).first()
            leader_name = leader_chad.name
            leader_username = leader_user.twitter_handle if leader_user else 'Unknown'
        else:
            leader_name = 'Unknown'
            leader_username = 'Unknown'
        
        cabal_data.append({
            'id': cabal.id,
            'name': cabal.name,
            'rank': cabal.rank,
            'level': cabal.level,
            'power': int(cabal.total_power),
            'member_count': cabal.member_count,
            'leader_name': leader_name,
            'leader_username': leader_username,
            'battles_won': cabal.battles_won,
            'battles_lost': cabal.battles_lost,
            'win_rate': round((cabal.battles_won / (cabal.battles_won + cabal.battles_lost) * 100) if (cabal.battles_won + cabal.battles_lost) > 0 else 0, 1)
        })
    
    return render_template('cabal/leaderboard.html', cabals=cabal_data) 