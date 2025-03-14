from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models.chad import Chad
import uuid
import os

# Create blueprint
squad_bp = Blueprint('squad', __name__, url_prefix='/squad')

# Create Squad model class in memory
class Squad:
    def __init__(self, id, name, description, leader_id, invite_code, level=1, xp=0, battles_won=0, battles_lost=0, created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.leader_id = leader_id
        self.invite_code = invite_code
        self.level = level
        self.xp = xp
        self.battles_won = battles_won
        self.battles_lost = battles_lost
        self.created_at = created_at
        self.members = []  # This will be populated separately

class SquadMember:
    def __init__(self, id, squad_id, chad_id, is_active=True, joined_at=None):
        self.id = id
        self.squad_id = squad_id
        self.chad_id = chad_id
        self.is_active = is_active
        self.joined_at = joined_at
        self.chad = None  # This will be populated separately

@squad_bp.route('/')
@login_required
def index():
    """Squad management page"""
    # Get user's Chad character
    chad = Chad.query.filter_by(user_id=current_user.id).first()
    
    if not chad:
        flash('You need to create a Chad character first!', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Get user's squad if they're in one
    # Note: In a real implementation, this would fetch from the database
    # For now, we'll just show the squad creation UI
    squad = None
    
    return render_template('squad/index.html', squad=squad, chad=chad)

@squad_bp.route('/create', methods=['POST'])
@login_required
def create():
    """Create a new squad"""
    # Get user's Chad character
    chad = Chad.query.filter_by(user_id=current_user.id).first()
    
    if not chad:
        flash('You need to create a Chad character first!', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Get form data
    name = request.form.get('name')
    description = request.form.get('description')
    
    if not name:
        flash('Squad name is required', 'danger')
        return redirect(url_for('squad.index'))
    
    # In a real implementation, this would create a squad in the database
    # For now, just flash a message
    flash(f'Squad "{name}" created successfully! This is a placeholder.', 'success')
    return redirect(url_for('squad.index'))

@squad_bp.route('/join', methods=['GET'])
@login_required
def join():
    """Join a squad using a invite code from a URL"""
    # Get the invite code from the query parameters
    code = request.args.get('code')
    
    if not code:
        flash('Invalid invite link', 'danger')
        return redirect(url_for('squad.index'))
    
    # In a real implementation, this would find the squad and add the user
    # For now, just flash a message
    flash(f'Joined squad with code {code}! This is a placeholder.', 'success')
    return redirect(url_for('squad.index'))

@squad_bp.route('/join-with-code', methods=['POST'])
@login_required
def join_with_code():
    """Join a squad using an invite code from the form"""
    # Get the invite code from the form
    invite_code = request.form.get('invite_code')
    
    if not invite_code:
        flash('Invite code is required', 'danger')
        return redirect(url_for('squad.index'))
    
    # In a real implementation, this would find the squad and add the user
    # For now, just flash a message
    flash(f'Joined squad with code {invite_code}! This is a placeholder.', 'success')
    return redirect(url_for('squad.index'))

@squad_bp.route('/leave', methods=['POST'])
@login_required
def leave():
    """Leave the current squad"""
    # In a real implementation, this would remove the user from their squad
    # For now, just flash a message
    flash('Left squad! This is a placeholder.', 'success')
    return redirect(url_for('squad.index'))

@squad_bp.route('/edit/<int:squad_id>', methods=['GET', 'POST'])
@login_required
def edit(squad_id):
    """Edit a squad"""
    # In a real implementation, this would edit the squad in the database
    flash('Squad updated! This is a placeholder.', 'success')
    return redirect(url_for('squad.index'))

@squad_bp.route('/battles/<int:squad_id>')
@login_required
def battles(squad_id):
    """View squad battles"""
    # In a real implementation, this would show the squad's battles
    return render_template('squad/battles.html', squad_id=squad_id)

@squad_bp.route('/remove-member/<int:member_id>', methods=['POST'])
@login_required
def remove_member(member_id):
    """Remove a member from the squad"""
    # In a real implementation, this would remove the member from the squad
    flash('Member removed! This is a placeholder.', 'success')
    return redirect(url_for('squad.index'))

@squad_bp.route('/activate-member/<int:member_id>', methods=['POST'])
@login_required
def activate_member(member_id):
    """Activate an inactive member"""
    # In a real implementation, this would activate the member
    flash('Member activated! This is a placeholder.', 'success')
    return redirect(url_for('squad.index')) 