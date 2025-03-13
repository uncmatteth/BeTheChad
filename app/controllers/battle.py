"""
Battle controller for Chad Battles.
This is a simplified implementation for deployment.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.battle import Battle

battle_bp = Blueprint('battle', __name__, url_prefix='/battles')

@battle_bp.route('/')
def index():
    """Battle index page"""
    return render_template('battle/index.html')

@battle_bp.route('/history')
@login_required
def history():
    """Show battle history"""
    return render_template('battle/history.html')

@battle_bp.route('/details/<int:battle_id>')
@login_required
def details(battle_id):
    """Show battle details"""
    battle = Battle.query.get_or_404(battle_id)
    return render_template('battle/details.html', battle=battle) 