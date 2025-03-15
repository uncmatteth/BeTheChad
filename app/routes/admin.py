from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User
from app.models.appeal import Appeal
from functools import wraps
import logging

admin = Blueprint('admin', __name__, url_prefix='/admin')
logger = logging.getLogger(__name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard"""
    pending_appeals_count = Appeal.query.filter_by(status='pending').count()
    total_users = User.query.count()
    
    return render_template('admin/index.html',
                         pending_appeals_count=pending_appeals_count,
                         total_users=total_users)

@admin.route('/appeals')
@login_required
@admin_required
def appeals():
    """List all appeals"""
    status = request.args.get('status', 'pending')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    query = Appeal.query
    if status != 'all':
        query = query.filter_by(status=status)
    
    appeals = query.order_by(Appeal.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/appeals.html',
                         appeals=appeals,
                         current_status=status)

@admin.route('/appeals/<int:appeal_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def appeal_detail(appeal_id):
    """View and process an appeal"""
    appeal = Appeal.query.get_or_404(appeal_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        reason = request.form.get('reason')
        
        try:
            if action == 'approve':
                appeal.approve(current_user, reason)
                flash('Appeal approved successfully.', 'success')
            elif action == 'reject':
                appeal.reject(current_user, reason)
                flash('Appeal rejected successfully.', 'danger')
            else:
                flash('Invalid action.', 'warning')
                
            db.session.commit()
            logger.info(f"Appeal {appeal_id} {action}d by admin {current_user.username}")
            
            return redirect(url_for('admin.appeals'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error processing appeal {appeal_id}: {str(e)}")
            flash(f'Error processing appeal: {str(e)}', 'danger')
    
    return render_template('admin/appeal_detail.html', appeal=appeal)

@admin.route('/users')
@login_required
@admin_required
def users():
    """List all users"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/users.html', users=users)

@admin.route('/users/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    """View user details"""
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_detail.html', user=user) 