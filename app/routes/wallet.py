from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db, limiter
from app.models.user import User
from app.models.transaction import Transaction
import logging

# Create blueprint
wallet = Blueprint('wallet', __name__)
logger = logging.getLogger(__name__)

@wallet.route('/wallet')
@login_required
def index():
    """Wallet overview page"""
    try:
        # Get user's transactions
        transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).limit(10).all()
        return render_template('wallet/index.html', transactions=transactions)
    except Exception as e:
        logger.error(f"Error loading wallet: {str(e)}")
        flash('Error loading wallet data', 'danger')
        return redirect(url_for('main.dashboard'))

@wallet.route('/wallet/transactions')
@login_required
def transactions():
    """Transaction history page"""
    try:
        # Get all user's transactions with pagination
        page = request.args.get('page', 1, type=int)
        per_page = 20
        transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).paginate(page=page, per_page=per_page)
        return render_template('wallet/transactions.html', transactions=transactions)
    except Exception as e:
        logger.error(f"Error loading transaction history: {str(e)}")
        flash('Error loading transaction history', 'danger')
        return redirect(url_for('wallet.index'))

@wallet.route('/wallet/send', methods=['GET', 'POST'])
@login_required
@limiter.limit("10 per minute")
def send():
    """Send Chadcoin to another user"""
    if request.method == 'POST':
        try:
            recipient_username = request.form.get('recipient')
            amount = request.form.get('amount', type=float)
            
            # Basic validation
            if not recipient_username or not amount:
                flash('Recipient and amount are required', 'danger')
                return redirect(url_for('wallet.send'))
                
            if amount <= 0:
                flash('Amount must be greater than zero', 'danger')
                return redirect(url_for('wallet.send'))
                
            # Check user has enough balance
            if current_user.chadcoin_balance < amount:
                flash('Insufficient balance', 'danger')
                return redirect(url_for('wallet.send'))
                
            # Find recipient
            recipient = User.query.filter_by(username=recipient_username).first()
            if not recipient:
                flash('Recipient not found', 'danger')
                return redirect(url_for('wallet.send'))
                
            if recipient.id == current_user.id:
                flash('Cannot send to yourself', 'danger')
                return redirect(url_for('wallet.send'))
                
            # Process transaction
            current_user.chadcoin_balance -= amount
            recipient.chadcoin_balance += amount
            
            # Record transaction
            sender_tx = Transaction(
                user_id=current_user.id,
                amount=-amount,
                description=f"Sent to {recipient.username}",
                transaction_type="transfer_out"
            )
            
            recipient_tx = Transaction(
                user_id=recipient.id,
                amount=amount,
                description=f"Received from {current_user.username}",
                transaction_type="transfer_in"
            )
            
            db.session.add(sender_tx)
            db.session.add(recipient_tx)
            db.session.commit()
            
            flash(f'Successfully sent {amount} Chadcoin to {recipient.username}', 'success')
            return redirect(url_for('wallet.index'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error processing transaction: {str(e)}")
            flash('Error processing transaction', 'danger')
            return redirect(url_for('wallet.send'))
    
    return render_template('wallet/send.html')
    
@wallet.route('/api/wallet/balance')
@login_required
@limiter.limit("20 per minute")
def get_balance():
    """API endpoint to get current balance"""
    return jsonify({
        'balance': current_user.chadcoin_balance,
        'username': current_user.username
    }) 