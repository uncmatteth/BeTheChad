"""
Wallet controller for Chad Battles.
Handles wallet connections and blockchain operations.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User
from app.utils.solana_api import get_wallet_balance, verify_wallet_ownership
import json
import logging

logger = logging.getLogger(__name__)

wallet_bp = Blueprint('wallet', __name__, url_prefix='/wallet')

@wallet_bp.route('/')
@login_required
def index():
    """Wallet dashboard."""
    # Get connected wallet information if available
    wallet_info = None
    if current_user.wallet_address:
        wallet_info = {
            'address': current_user.wallet_address,
            'type': current_user.wallet_type or 'Unknown',
            'balance': None
        }
        try:
            wallet_info['balance'] = get_wallet_balance(current_user.wallet_address)
        except Exception as e:
            logger.error(f"Error fetching wallet balance: {str(e)}")
            wallet_info['balance_error'] = "Could not fetch balance"
    
    return render_template('wallet/index.html', wallet_info=wallet_info)

@wallet_bp.route('/connect', methods=['GET', 'POST'])
@login_required
def connect():
    """Connect a wallet."""
    if request.method == 'POST':
        wallet_address = request.form.get('wallet_address')
        wallet_type = request.form.get('wallet_type', 'unknown')
        signature = request.form.get('signature')
        
        if not wallet_address:
            flash('No wallet address provided', 'danger')
            return redirect(url_for('wallet.connect'))
        
        # Check if another user already has this wallet address
        existing_user = User.query.filter(
            User.wallet_address == wallet_address, 
            User.id != current_user.id
        ).first()
        
        if existing_user:
            flash('This wallet address is already connected to another account', 'danger')
            return redirect(url_for('wallet.connect'))
        
        # In a production environment, verify the signature
        # This is a simplified implementation for development
        try:
            if not verify_wallet_ownership(wallet_address, signature):
                flash('Could not verify wallet ownership', 'danger')
                return redirect(url_for('wallet.connect'))
        except Exception as e:
            logger.error(f"Error verifying wallet ownership: {str(e)}")
            flash('Error verifying wallet ownership', 'danger')
            return redirect(url_for('wallet.connect'))
        
        # Update the user's wallet information
        current_user.wallet_address = wallet_address
        current_user.wallet_type = wallet_type
        db.session.commit()
        
        flash(f'{wallet_type.capitalize()} wallet connected successfully', 'success')
        return redirect(url_for('wallet.index'))
    
    return render_template('wallet/connect.html')

@wallet_bp.route('/disconnect', methods=['POST'])
@login_required
def disconnect():
    """Disconnect a wallet."""
    if not current_user.wallet_address:
        flash('No wallet is currently connected', 'warning')
        return redirect(url_for('wallet.index'))
    
    # Store the wallet type for the success message
    wallet_type = current_user.wallet_type or 'Unknown'
    
    # Update the user's wallet information
    current_user.wallet_address = None
    current_user.wallet_type = None
    db.session.commit()
    
    flash(f'{wallet_type.capitalize()} wallet disconnected successfully', 'success')
    return redirect(url_for('wallet.index'))

@wallet_bp.route('/api/connect', methods=['POST'])
@login_required
def api_connect():
    """API endpoint for connecting a wallet."""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    wallet_address = data.get('wallet_address')
    wallet_type = data.get('wallet_type', 'unknown')
    signature = data.get('signature')
    
    if not wallet_address:
        return jsonify({'success': False, 'message': 'No wallet address provided'}), 400
    
    # Check if another user already has this wallet address
    existing_user = User.query.filter(
        User.wallet_address == wallet_address, 
        User.id != current_user.id
    ).first()
    
    if existing_user:
        return jsonify({'success': False, 'message': 'This wallet address is already connected to another account'}), 400
    
    # In a production environment, verify the signature
    # This is a simplified implementation for development
    try:
        if not verify_wallet_ownership(wallet_address, signature):
            return jsonify({'success': False, 'message': 'Could not verify wallet ownership'}), 400
    except Exception as e:
        logger.error(f"Error verifying wallet ownership: {str(e)}")
        return jsonify({'success': False, 'message': 'Error verifying wallet ownership'}), 500
    
    # Update the user's wallet information
    current_user.wallet_address = wallet_address
    current_user.wallet_type = wallet_type
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'{wallet_type.capitalize()} wallet connected successfully',
        'wallet_address': wallet_address,
        'wallet_type': wallet_type
    })

@wallet_bp.route('/api/disconnect', methods=['POST'])
@login_required
def api_disconnect():
    """API endpoint for disconnecting a wallet."""
    if not current_user.wallet_address:
        return jsonify({'success': False, 'message': 'No wallet is currently connected'}), 400
    
    # Store the wallet type for the success message
    wallet_type = current_user.wallet_type or 'Unknown'
    
    # Update the user's wallet information
    current_user.wallet_address = None
    current_user.wallet_type = None
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'{wallet_type.capitalize()} wallet disconnected successfully'
    })

@wallet_bp.route('/api/status')
@login_required
def api_status():
    """API endpoint for getting wallet status."""
    if not current_user.wallet_address:
        return jsonify({
            'connected': False,
            'message': 'No wallet connected'
        })
    
    wallet_balance = None
    try:
        wallet_balance = get_wallet_balance(current_user.wallet_address)
    except Exception as e:
        logger.error(f"Error fetching wallet balance: {str(e)}")
    
    return jsonify({
        'connected': True,
        'wallet_address': current_user.wallet_address,
        'wallet_type': current_user.wallet_type or 'Unknown',
        'balance': wallet_balance
    }) 