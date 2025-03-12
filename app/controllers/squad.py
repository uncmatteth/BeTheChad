from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models.cabal import Cabal, CabalMember

cabal_bp = Blueprint('cabal', __name__)

@cabal_bp.route('/')
@login_required
def index():
    """Display the user's cabal"""
    cabals = Cabal.query.filter_by(user_id=current_user.id).all()
    return render_template('cabal/index.html', cabals=cabals)

@cabal_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new cabal"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Cabal name is required', 'danger')
            return redirect(url_for('cabal.create'))
        
        cabal = Cabal(
            user_id=current_user.id,
            name=name,
            description=description
        )
        
        db.session.add(cabal)
        db.session.commit()
        
        flash('Cabal created successfully', 'success')
        return redirect(url_for('cabal.index'))
    
    return render_template('cabal/create.html') 