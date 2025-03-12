"""
API controller for Chad Battles.
Handles API endpoints for NFT operations and wallet interactions.
"""
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
import json
import os
from app.extensions import db, cache
from app.models.nft import NFT, NFTEntityType
from app.models.transaction import Transaction, TransactionType
from app.models.user import User
from app.models.chad import Chad
from app.models.waifu import Waifu
from app.models.item import Item
from app.models.meme_elixir import MemeElixir
from app.utils.solana_api import mint_nft_on_chain, burn_nft_on_chain, verify_wallet_ownership, get_wallet_balance, upload_to_ipfs, transfer_nft

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/mint-nft', methods=['POST'])
@login_required
def mint_nft():
    """Mint an NFT for a waifu, item, or chad."""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    entity_type = data.get('entity_type')
    entity_id = data.get('entity_id')
    
    if not entity_type or not entity_id:
        return jsonify({'success': False, 'message': 'Entity type and ID are required'}), 400
    
    # Check if wallet is connected
    if not current_user.wallet_address:
        return jsonify({'success': False, 'message': 'You need to connect a wallet first'}), 403
    
    # Validate entity type
    if entity_type not in [e.value for e in NFTEntityType]:
        return jsonify({'success': False, 'message': f'Invalid entity type: {entity_type}'}), 400
    
    # Get entity
    entity = None
    if entity_type == NFTEntityType.CHAD.value:
        entity = Chad.query.filter_by(id=entity_id, user_id=current_user.id).first()
    elif entity_type == NFTEntityType.WAIFU.value:
        entity = Waifu.query.filter_by(id=entity_id, user_id=current_user.id).first()
    elif entity_type == NFTEntityType.ITEM.value:
        entity = Item.query.filter_by(id=entity_id, user_id=current_user.id).first()
    
    if not entity:
        return jsonify({'success': False, 'message': f'Entity not found or not owned by you'}), 404
    
    # Check if entity is already minted
    existing_nft = NFT.query.filter_by(
        entity_type=entity_type,
        entity_id=entity_id,
        is_burned=False
    ).first()
    
    if existing_nft:
        return jsonify({'success': False, 'message': 'This entity is already minted as an NFT'}), 400
    
    try:
        # Generate metadata
        from app.utils.solana_api import generate_metadata
        metadata = generate_metadata(entity_type, entity, None)
        if not metadata:
            return jsonify({'success': False, 'message': 'Failed to generate metadata'}), 500
        
        # Upload metadata to IPFS
        metadata_uri = upload_to_ipfs(metadata)
        if not metadata_uri:
            return jsonify({'success': False, 'message': 'Failed to upload metadata to IPFS'}), 500
        
        # Mint NFT on-chain
        mint_result = mint_nft_on_chain(current_user.wallet_address, metadata_uri, entity_type, entity_id)
        
        if not mint_result.get('success', False):
            return jsonify({'success': False, 'message': 'Failed to mint NFT on blockchain'}), 500
        
        # Create NFT record
        nft = NFT(
            token_id=mint_result.get('token_id'),
            user_id=current_user.id,
            entity_type=entity_type,
            entity_id=entity_id,
            mint_transaction_hash=mint_result.get('transaction_id'),
            mint_block_number=mint_result.get('block_number'),
            metadata_uri=metadata_uri
        )
        
        db.session.add(nft)
        
        # Record transaction
        transaction = Transaction(
            user_id=current_user.id,
            nft_id=nft.id,
            transaction_type=TransactionType.NFT_MINT.value,
            amount=0,
            description=f"Minted {entity_type} NFT",
            transaction_hash=mint_result.get('transaction_id'),
            block_number=mint_result.get('block_number'),
            status="completed"
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'NFT minted successfully',
            'nft': nft.to_dict(),
            'transaction_hash': mint_result.get('transaction_id')
        })
        
    except Exception as e:
        current_app.logger.error(f"Error minting NFT: {str(e)}")
        return jsonify({'success': False, 'message': f'Error minting NFT: {str(e)}'}), 500

@api_bp.route('/burn-nft', methods=['POST'])
@login_required
def burn_nft():
    """Burn an NFT and receive Chadcoin."""
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

@api_bp.route('/wallet/connect', methods=['POST'])
@login_required
def connect_wallet():
    """Connect a wallet to the user's account."""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    wallet_address = data.get('wallet_address')
    wallet_type = data.get('wallet_type')
    signature = data.get('signature')
    message = data.get('message', 'Verify Chad Battles Wallet')
    
    if not wallet_address or not wallet_type:
        return jsonify({'success': False, 'message': 'Wallet address and type are required'}), 400
    
    # Check if wallet is already connected to another account
    existing_user = User.query.filter(
        User.wallet_address == wallet_address,
        User.id != current_user.id
    ).first()
    
    if existing_user:
        return jsonify({'success': False, 'message': 'This wallet is already connected to another account'}), 400
    
    # Verify wallet ownership
    if signature:
        verification = verify_wallet_ownership(wallet_address, signature, message)
        if not verification.get('success', False):
            return jsonify({'success': False, 'message': verification.get('message', 'Failed to verify wallet ownership')}), 400
    
    # Update user's wallet information
    current_user.wallet_address = wallet_address
    current_user.wallet_type = wallet_type
    db.session.commit()
    
    # Get wallet balance
    balance_info = get_wallet_balance(wallet_address)
    
    return jsonify({
        'success': True,
        'message': 'Wallet connected successfully',
        'wallet_address': wallet_address,
        'wallet_type': wallet_type,
        'balance': balance_info.get('balance', 0) if balance_info.get('success', False) else 0
    })

@api_bp.route('/wallet/disconnect', methods=['POST'])
@login_required
def disconnect_wallet():
    """Disconnect a wallet from the user's account."""
    if not current_user.wallet_address:
        return jsonify({'success': False, 'message': 'No wallet connected'}), 400
    
    # Clear wallet information
    current_user.wallet_address = None
    current_user.wallet_type = None
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Wallet disconnected successfully'
    })

@api_bp.route('/wallet/status', methods=['GET'])
@login_required
def wallet_status():
    """Get the status of the user's wallet."""
    if not current_user.wallet_address:
        return jsonify({
            'success': True,
            'connected': False,
            'message': 'No wallet connected'
        })
    
    # Get wallet balance
    balance_info = get_wallet_balance(current_user.wallet_address)
    
    return jsonify({
        'success': True,
        'connected': True,
        'wallet_address': current_user.wallet_address,
        'wallet_type': current_user.wallet_type,
        'balance': balance_info.get('balance', 0) if balance_info.get('success', False) else 0
    })

@api_bp.route('/generate-chad-avatar/<int:chad_id>', methods=['GET'])
def generate_chad_avatar(chad_id):
    """Generate an avatar for a Chad character."""
    chad = Chad.query.get_or_404(chad_id)
    
    # Check if the Chad is minted as an NFT
    nft = NFT.query.filter_by(
        entity_type=NFTEntityType.CHAD.value,
        entity_id=chad_id,
        is_burned=False
    ).first()
    
    # If the Chad is minted as an NFT, the avatar is locked
    if nft:
        # Return the existing avatar
        avatar_path = os.path.join('app', 'static', 'img', 'chads', f'{chad_id}.png')
        if os.path.exists(avatar_path):
            with open(avatar_path, 'rb') as f:
                avatar_data = f.read()
            return jsonify({
                'success': True,
                'avatar': avatar_data.decode('utf-8'),
                'is_locked': True
            })
    
    # Generate a new avatar based on Chad's attributes
    # This would typically call an avatar generation service
    # For now, we'll just return a placeholder
    
    return jsonify({
        'success': True,
        'avatar': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==',
        'is_locked': False
    })

@api_bp.route('/activate-elixir', methods=['POST'])
@login_required
def activate_elixir():
    """Activate a Meme Elixir for a character"""
    elixir_id = request.json.get('elixir_id')
    chad_id = request.json.get('chad_id')
    
    if not elixir_id or not chad_id:
        return jsonify({'success': False, 'message': 'Missing required parameters'})
    
    # Get the elixir
    elixir = MemeElixir.query.get(elixir_id)
    
    if not elixir:
        return jsonify({'success': False, 'message': 'Elixir not found'})
    
    # Check ownership
    if elixir.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'You do not own this elixir'})
    
    # Check if already activated
    if elixir.is_activated:
        return jsonify({'success': False, 'message': 'This elixir is already activated'})
    
    # Get the character
    chad = Chad.query.get(chad_id)
    
    if not chad:
        return jsonify({'success': False, 'message': 'Character not found'})
    
    # Check if user owns the character
    if not (chad.user_id == current_user.id):
        return jsonify({'success': False, 'message': 'You do not own this character'})
    
    # Activate the elixir
    success, msg = elixir.activate(chad_id)
    
    if not success:
        return jsonify({'success': False, 'message': msg})
    
    return jsonify({
        'success': True,
        'message': msg
    })

@api_bp.route('/user-stats', methods=['GET'])
@login_required
def user_stats():
    """Get user stats"""
    # Get the user's character
    chad = Chad.query.filter_by(user_id=current_user.id).first()
    
    if not chad:
        return jsonify({'success': False, 'message': 'No character found'})
    
    # Get total stats
    stats = chad.get_total_stats()
    
    return jsonify({
        'success': True,
        'stats': stats,
        'level': chad.level,
        'xp': chad.xp,
        'battles_won': chad.battles_won,
        'battles_lost': chad.battles_lost
    })

@api_bp.route('/transfer-nft', methods=['POST'])
@login_required
def transfer_nft():
    """Transfer an NFT to another user."""
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    token_id = data.get('token_id')
    to_address = data.get('to_address')
    
    if not token_id or not to_address:
        return jsonify({'success': False, 'message': 'Token ID and destination address are required'}), 400
    
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
    
    # Find the recipient user by wallet address
    recipient = User.query.filter_by(wallet_address=to_address).first()
    if not recipient:
        return jsonify({'success': False, 'message': 'Recipient not found in the system'}), 404
    
    try:
        # Transfer NFT on-chain
        transfer_result = transfer_nft(current_user.wallet_address, to_address, token_id)
        
        if not transfer_result.get('success', False):
            return jsonify({'success': False, 'message': 'Failed to transfer NFT on blockchain'}), 500
        
        # Update ownership in database
        old_owner_id = nft.user_id
        nft.user_id = recipient.id
        
        # Record transaction
        transaction = Transaction(
            user_id=current_user.id,
            nft_id=nft.id,
            transaction_type=TransactionType.NFT_TRANSFER.value,
            amount=0,
            description=f"Transferred {nft.entity_type} NFT to {recipient.username}",
            transaction_hash=transfer_result.get('transaction_id'),
            block_number=transfer_result.get('block_number'),
            from_user_id=old_owner_id,
            to_user_id=recipient.id,
            status="completed"
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'NFT transferred successfully to {recipient.username}',
            'transaction_hash': transfer_result.get('transaction_id')
        })
        
    except Exception as e:
        current_app.logger.error(f"Error transferring NFT: {str(e)}")
        return jsonify({'success': False, 'message': f'Error transferring NFT: {str(e)}'}), 500 