from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.waifu import Waifu, WaifuType, WaifuRarity
from app.models.item import WaifuItem
from app.models.nft import NFT

waifu_bp = Blueprint('waifu', __name__)

@waifu_bp.route('/')
@login_required
def index():
    """Waifu collection page"""
    # Get user's waifus
    waifus = current_user.waifus.all()
    
    # Get user's Chad character
    chad = current_user.chad
    
    if not chad:
        flash('You need to create a Chad character first!', 'warning')
        return redirect(url_for('main.index'))
    
    # Get equipped waifus
    equipped_waifus = [w.id for w in chad.equipped_waifus.all()]
    
    return render_template('waifu/index.html', 
                          waifus=waifus, 
                          equipped_waifus=equipped_waifus)

@waifu_bp.route('/<waifu_id>')
@login_required
def detail(waifu_id):
    """Waifu detail page"""
    # Get the waifu
    waifu = Waifu.query.get_or_404(waifu_id)
    
    # Check ownership
    if waifu.user_id != current_user.id:
        flash('You do not own this waifu', 'danger')
        return redirect(url_for('waifu.index'))
    
    # Get waifu stats
    stats = waifu.get_total_stats()
    
    # Get equipped items
    equipped_items = waifu.equipped_items.all()
    
    # Get available items
    available_items = WaifuItem.query.filter_by(
        user_id=current_user.id,
        is_equipped=False
    ).all()
    
    # Get NFT info if minted
    nft = None
    if waifu.is_minted:
        nft = NFT.query.filter_by(
            entity_type='waifu',
            waifu_id=waifu.id
        ).first()
    
    return render_template('waifu/detail.html',
                          waifu=waifu,
                          stats=stats,
                          equipped_items=equipped_items,
                          available_items=available_items,
                          nft=nft)

@waifu_bp.route('/equip', methods=['POST'])
@login_required
def equip():
    """Equip a waifu to the Chad character"""
    waifu_id = request.form.get('waifu_id')
    
    if not waifu_id:
        return jsonify({'success': False, 'message': 'No waifu specified'})
    
    # Get the waifu
    waifu = Waifu.query.get(waifu_id)
    
    if not waifu:
        return jsonify({'success': False, 'message': 'Waifu not found'})
    
    # Check ownership
    if waifu.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'You do not own this waifu'})
    
    # Get user's Chad character
    chad = current_user.chad
    
    if not chad:
        return jsonify({'success': False, 'message': 'You need to create a Chad character first'})
    
    # Try to equip the waifu
    success, message = waifu.equip(chad)
    
    return jsonify({'success': success, 'message': message})

@waifu_bp.route('/unequip', methods=['POST'])
@login_required
def unequip():
    """Unequip a waifu from the Chad character"""
    waifu_id = request.form.get('waifu_id')
    
    if not waifu_id:
        return jsonify({'success': False, 'message': 'No waifu specified'})
    
    # Get the waifu
    waifu = Waifu.query.get(waifu_id)
    
    if not waifu:
        return jsonify({'success': False, 'message': 'Waifu not found'})
    
    # Check ownership
    if waifu.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'You do not own this waifu'})
    
    # Check if waifu is equipped
    if not waifu.is_equipped:
        return jsonify({'success': False, 'message': 'This waifu is not equipped'})
    
    # Try to unequip the waifu
    success, message = waifu.unequip()
    
    return jsonify({'success': success, 'message': message})

@waifu_bp.route('/equip-item', methods=['POST'])
@login_required
def equip_item():
    """Equip an item to a waifu (permanent)"""
    waifu_id = request.form.get('waifu_id')
    item_id = request.form.get('item_id')
    
    if not waifu_id or not item_id:
        return jsonify({'success': False, 'message': 'Missing required parameters'})
    
    # Get the waifu
    waifu = Waifu.query.get(waifu_id)
    
    if not waifu:
        return jsonify({'success': False, 'message': 'Waifu not found'})
    
    # Check waifu ownership
    if waifu.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'You do not own this waifu'})
    
    # Get the item
    item = WaifuItem.query.get(item_id)
    
    if not item:
        return jsonify({'success': False, 'message': 'Item not found'})
    
    # Check item ownership
    if item.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'You do not own this item'})
    
    # Check if item is already equipped
    if item.is_equipped:
        return jsonify({'success': False, 'message': 'This item is already equipped to another waifu'})
    
    # Show warning if item is minted as NFT
    if item.is_minted:
        return jsonify({
            'success': False, 
            'message': 'This item is minted as an NFT. Equipping it will burn the NFT. Are you sure?',
            'require_confirmation': True
        })
    
    # Try to equip the item
    success, message = item.equip(waifu)
    
    return jsonify({'success': success, 'message': message})

@waifu_bp.route('/mint', methods=['POST'])
@login_required
def mint():
    """Mint a waifu as an NFT"""
    waifu_id = request.form.get('waifu_id')
    
    if not waifu_id:
        return jsonify({'success': False, 'message': 'No waifu specified'})
    
    # Get the waifu
    waifu = Waifu.query.get(waifu_id)
    
    if not waifu:
        return jsonify({'success': False, 'message': 'Waifu not found'})
    
    # Check ownership
    if waifu.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'You do not own this waifu'})
    
    # Check if already minted
    if waifu.is_minted:
        return jsonify({'success': False, 'message': 'This waifu is already minted as an NFT'})
    
    # Check if user has a wallet connected
    if not current_user.wallet_address:
        return jsonify({'success': False, 'message': 'You need to connect a wallet first'})
    
    # Redirect to the API endpoint for minting
    return jsonify({
        'success': True,
        'redirect': url_for('api.mint_nft_endpoint'),
        'data': {
            'entity_type': 'waifu',
            'entity_id': waifu.id
        }
    }) 