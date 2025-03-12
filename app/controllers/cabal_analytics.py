"""
Controllers for cabal analytics.

This module provides endpoints for displaying analytics data for cabals.
"""

import logging
from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import login_required, current_user
from app.models.cabal import Cabal, CabalMember
from app.models.chad import Chad
from app.models.cabal_analytics import CabalAnalytics
from app.utils.permissions import require_cabal_membership

logger = logging.getLogger(__name__)

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/cabal/<cabal_id>')
@login_required
@require_cabal_membership
def cabal_analytics(cabal_id):
    """
    Display analytics for a specific cabal.
    
    Args:
        cabal_id (str): The ID of the cabal to display analytics for
    
    Returns:
        HTML: The analytics dashboard for the cabal
    """
    cabal = Cabal.query.get_or_404(cabal_id)
    
    # Get latest analytics snapshot
    latest = CabalAnalytics.get_latest(cabal_id)
    
    # Get last 30 days of history
    history = CabalAnalytics.get_history(cabal_id, days=30)
    
    # Prepare data for charts
    dates = [record.timestamp.strftime('%Y-%m-%d') for record in history]
    power_data = [float(record.total_power) for record in history]
    member_data = [record.member_count for record in history]
    rank_data = [record.rank for record in history]
    
    return render_template(
        'cabal/analytics.html',
        cabal=cabal,
        latest=latest,
        dates=dates,
        power_data=power_data,
        member_data=member_data,
        rank_data=rank_data
    )

@analytics_bp.route('/api/cabal/<cabal_id>/history')
@login_required
@require_cabal_membership
def cabal_history_api(cabal_id):
    """
    API endpoint to get historical analytics data for a cabal.
    
    Args:
        cabal_id (str): The ID of the cabal to get history for
    
    Returns:
        JSON: Historical analytics data
    """
    days = request.args.get('days', 30, type=int)
    if days > 365:
        days = 365  # Limit to 1 year of history
    
    history = CabalAnalytics.get_history(cabal_id, days=days)
    
    # Format data for API response
    data = {
        'dates': [record.timestamp.strftime('%Y-%m-%d') for record in history],
        'power': [float(record.total_power) for record in history],
        'members': [record.member_count for record in history],
        'active_members': [record.active_member_count for record in history],
        'rank': [record.rank for record in history],
        'battles_won': [record.battles_won for record in history],
        'battles_lost': [record.battles_lost for record in history],
        'referrals': [record.referrals for record in history]
    }
    
    return jsonify(data)

@analytics_bp.route('/api/cabal/<cabal_id>/latest')
@login_required
@require_cabal_membership
def cabal_latest_api(cabal_id):
    """
    API endpoint to get the latest analytics snapshot for a cabal.
    
    Args:
        cabal_id (str): The ID of the cabal to get latest data for
    
    Returns:
        JSON: Latest analytics data
    """
    latest = CabalAnalytics.get_latest(cabal_id)
    if not latest:
        abort(404)
    
    # Format data for API response
    data = {
        'timestamp': latest.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'member_count': latest.member_count,
        'active_member_count': latest.active_member_count,
        'total_power': float(latest.total_power),
        'rank': latest.rank,
        'battles_won': latest.battles_won,
        'battles_lost': latest.battles_lost,
        'referrals': latest.referrals
    }
    
    return jsonify(data) 