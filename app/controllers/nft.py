"""
NFT controller for Chad Battles.
Handles NFT listing, viewing, and transaction history.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
import json
import os
from app.extensions import db, cache
from app.models.nft import NFT, NFTEntityType
from app.models.transaction import Transaction, TransactionType
from app.utils.solana_api import mint_nft_on_chain, burn_nft_on_chain, transfer_nft

nft_bp = Blueprint('nft', __name__, url_prefix='/nft')

@nft_bp.route('/')
@login_required
def index():
    """List all NFTs owned by the current user."""
    nfts = NFT.query.filter_by(user_id=current_user.id, is_burned=False).all()
    nft_data = []
    
    for nft in nfts:
        # Get entity details
        entity = nft.get_entity()
        
        # Get metadata
        metadata = nft.generate_metadata()
        if not metadata:
            metadata = {
                "name": f"Unknown NFT #{nft.token_id}",
                "description": "Metadata not found",
                "image": url_for('static', filename='img/placeholder.png'),
                "attributes": []
            }
        
        # Add to list
        nft_data.append({
            'id': nft.id,
            'token_id': nft.token_id,
            'entity_type': nft.entity_type,
            'entity': entity,
            'metadata': metadata,
            'created_at': nft.created_at,
            'updated_at': nft.updated_at
        })
    
    # Group NFTs by type
    grouped_nfts = {
        'chad': [],
        'waifu': [],
        'item': []
    }
    
    for nft in nft_data:
        if nft['entity_type'] in grouped_nfts:
            grouped_nfts[nft['entity_type']].append(nft)
    
    return render_template('nft/index.html', 
                         grouped_nfts=grouped_nfts,
                         nft_count=len(nfts))

@nft_bp.route('/<token_id>')
def view(token_id):
    """View a specific NFT."""
    nft = NFT.query.filter_by(token_id=token_id).first_or_404()
    
    # Check if user is owner
    is_owner = current_user.is_authenticated and nft.user_id == current_user.id
    
    # Get entity details
    entity = nft.get_entity()
    
    # Get metadata
    metadata = nft.generate_metadata()
    if not metadata:
        metadata = {
            "name": f"Unknown NFT #{nft.token_id}",
            "description": "Metadata not found",
            "image": url_for('static', filename='img/placeholder.png'),
            "attributes": []
        }
    
    # Calculate Chadcoin reward for burning
    chadcoin_reward = nft.calculate_burn_value() if not nft.is_burned else 0
    
    # Get transaction history for this NFT
    transactions = Transaction.query.filter_by(nft_id=nft.id).order_by(Transaction.created_at.desc()).all()
    
    return render_template('nft/view.html', 
                          nft=nft,
                          entity=entity,
                          metadata=metadata,
                          is_owner=is_owner,
                          chadcoin_reward=chadcoin_reward,
                          transactions=transactions)

@nft_bp.route('/transactions')
@login_required
def transactions():
    """View NFT transaction history."""
    # Get minting transactions
    mint_transactions = Transaction.query.filter_by(
        user_id=current_user.id,
        transaction_type=TransactionType.NFT_MINT.value
    ).order_by(Transaction.created_at.desc()).all()
    
    # Get burning transactions
    burn_transactions = Transaction.query.filter_by(
        user_id=current_user.id,
        transaction_type=TransactionType.NFT_BURN.value
    ).order_by(Transaction.created_at.desc()).all()
    
    # Get transfer transactions
    transfer_transactions = Transaction.query.filter_by(
        user_id=current_user.id,
        transaction_type=TransactionType.NFT_TRANSFER.value
    ).order_by(Transaction.created_at.desc()).all()
    
    # Combine all transactions
    all_transactions = mint_transactions + burn_transactions + transfer_transactions
    
    # Sort by date (newest first)
    all_transactions.sort(key=lambda x: x.created_at, reverse=True)
    
    return render_template(
        'nft/transactions.html',
        transactions=all_transactions,
        mint_count=len(mint_transactions),
        burn_count=len(burn_transactions),
        transfer_count=len(transfer_transactions)
    )

@nft_bp.route('/api/burn', methods=['POST'])
@login_required
def burn_nft():
    """Burn an NFT to receive Chadcoin."""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    token_id = data.get('token_id')
    if not token_id:
        return jsonify({'success': False, 'message': 'Token ID is required'}), 400
    
    # Check if wallet is connected
    if not current_user.wallet_address:
        return jsonify({'success': False, 'message': 'You need to connect a wallet first'}), 403
    
    # Find the NFT
    nft = NFT.query.filter_by(token_id=token_id, is_burned=False).first()
    if not nft:
        return jsonify({'success': False, 'message': 'NFT not found or already burned'}), 404
    
    # Check ownership
    if nft.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'You do not own this NFT'}), 403
    
    # Calculate reward
    chadcoin_reward = nft.calculate_burn_value()
    
    try:
        # Burn NFT on-chain
        burn_result = burn_nft_on_chain(current_user.wallet_address, token_id)
        
        if not burn_result.get('success', False):
            return jsonify({'success': False, 'message': 'Failed to burn NFT on blockchain'}), 500
        
        # Mark NFT as burned
        nft.is_burned = True
        nft.burn_transaction_hash = burn_result.get('transaction_id')
        nft.burn_block_number = burn_result.get('block_number')
        
        # Add Chadcoin to user's balance
        current_user.add_chadcoin(chadcoin_reward)
        
        # Record transaction
        transaction = Transaction(
            user_id=current_user.id,
            nft_id=nft.id,
            transaction_type=TransactionType.NFT_BURN.value,
            amount=chadcoin_reward,
            description=f"Burned {nft.entity_type} NFT for {chadcoin_reward} Chadcoin",
            transaction_hash=burn_result.get('transaction_id'),
            block_number=burn_result.get('block_number'),
            status="completed"
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'NFT burned successfully. You received {chadcoin_reward} Chadcoin.',
            'chadcoin_reward': chadcoin_reward,
            'new_balance': current_user.chadcoin_balance,
            'transaction_hash': burn_result.get('transaction_id')
        })
        
    except Exception as e:
        current_app.logger.error(f"Error burning NFT: {str(e)}")
        return jsonify({'success': False, 'message': f'Error burning NFT: {str(e)}'}), 500

@nft_bp.route('/metadata/<token_id>')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_metadata(token_id):
    """Get metadata for a specific NFT - public endpoint for blockchain integration."""
    nft = NFT.query.filter_by(token_id=token_id).first()
    
    if not nft:
        return jsonify({
            'error': 'NFT not found',
            'status': 404
        }), 404
    
    # Generate metadata
    metadata = nft.generate_metadata()
    if not metadata:
        return jsonify({
            'error': 'Failed to generate metadata',
            'status': 500
        }), 500
    
    return jsonify(metadata) 