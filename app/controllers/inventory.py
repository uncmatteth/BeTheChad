from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.user import User
from app.models.waifu import Waifu, WaifuType
from app.models.item import Item, ItemType
from app.models.nft import NFT
from app.models.inventory import Inventory
from app.extensions import db
from sqlalchemy import desc
import json

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/')
@login_required
def index():
    """Render the inventory page with all user's items, waifus, and NFTs"""
    # Get user's waifus
    waifus = Waifu.query.filter_by(user_id=current_user.id).all()
    
    # Get user's items
    items = Item.query.filter_by(user_id=current_user.id).order_by(desc(Item.rarity_id)).all()
    
    # Check which entities have already been minted as NFTs
    waifu_nfts = NFT.query.filter_by(owner_id=current_user.id, entity_type='waifu').all()
    item_nfts = NFT.query.filter_by(owner_id=current_user.id, entity_type='item').all()
    chad_nft = NFT.query.filter_by(owner_id=current_user.id, entity_type='chad').first()
    
    # Create a structure to easily check which entities are already minted
    minted_nfts = {
        'waifus': [nft.entity_id for nft in waifu_nfts],
        'items': [nft.entity_id for nft in item_nfts],
        'chad': chad_nft is not None
    }
    
    return render_template(
        'inventory/index.html',
        waifus=waifus,
        items=items,
        minted_nfts=minted_nfts,
        user_has_chad_nft=minted_nfts['chad']
    )

@inventory_bp.route('/waifu/<int:waifu_id>')
@login_required
def get_waifu_details(waifu_id):
    """Get details for a specific waifu"""
    waifu = Waifu.query.filter_by(id=waifu_id, user_id=current_user.id).first()
    
    if not waifu:
        return jsonify({'success': False, 'message': 'Waifu not found or does not belong to you'}), 404
    
    # Get equipped items for this waifu
    equipped_items = Item.query.filter_by(waifu_id=waifu.id, is_equipped=True).all()
    
    # Check if this waifu has been minted as an NFT
    nft = NFT.query.filter_by(entity_type='waifu', entity_id=waifu_id).first()
    
    # Render waifu details partial template
    html = render_template(
        'inventory/partials/waifu_details.html',
        waifu=waifu,
        equipped_items=equipped_items,
        is_nft=nft is not None,
        nft=nft
    )
    
    return jsonify({'success': True, 'html': html})

@inventory_bp.route('/waifu/<int:waifu_id>/equip', methods=['POST'])
@login_required
def equip_waifu(waifu_id):
    """Equip a waifu for battle"""
    waifu = Waifu.query.filter_by(id=waifu_id, user_id=current_user.id).first()
    
    if not waifu:
        return jsonify({'success': False, 'message': 'Waifu not found or does not belong to you'}), 404
    
    # Logic for equipping waifus (may need to unequip others depending on game rules)
    # For now, just set is_equipped to True
    
    # First unequip any currently equipped waifu of the same type
    currently_equipped = Waifu.query.filter_by(
        user_id=current_user.id, 
        waifu_type_id=waifu.waifu_type_id, 
        is_equipped=True
    ).all()
    
    for equipped_waifu in currently_equipped:
        if equipped_waifu.id != waifu_id:
            equipped_waifu.is_equipped = False
    
    waifu.is_equipped = True
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'{waifu.waifu_type.name} equipped for battle!'
    })

@inventory_bp.route('/waifu/<int:waifu_id>/unequip', methods=['POST'])
@login_required
def unequip_waifu(waifu_id):
    """Unequip a waifu from battle"""
    waifu = Waifu.query.filter_by(id=waifu_id, user_id=current_user.id).first()
    
    if not waifu:
        return jsonify({'success': False, 'message': 'Waifu not found or does not belong to you'}), 404
    
    if not waifu.is_equipped:
        return jsonify({'success': False, 'message': 'This waifu is not currently equipped'}), 400
    
    waifu.is_equipped = False
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'{waifu.waifu_type.name} unequipped from battle'
    })

@inventory_bp.route('/item/<int:item_id>')
@login_required
def get_item_details(item_id):
    """Get details for a specific item"""
    item = Item.query.filter_by(id=item_id, user_id=current_user.id).first()
    
    if not item:
        return jsonify({'success': False, 'message': 'Item not found or does not belong to you'}), 404
    
    # Check if this item has been minted as an NFT
    nft = NFT.query.filter_by(entity_type='item', entity_id=item_id).first()
    
    # Render item details partial template
    html = render_template(
        'inventory/partials/item_details.html',
        item=item,
        is_nft=nft is not None,
        nft=nft
    )
    
    return jsonify({'success': True, 'html': html})

@inventory_bp.route('/item/<int:item_id>/equip', methods=['POST'])
@login_required
def equip_item(item_id):
    """Equip an item to the user's active chad or waifu"""
    item = Item.query.filter_by(id=item_id, user_id=current_user.id).first()
    
    if not item:
        return jsonify({'success': False, 'message': 'Item not found or does not belong to you'}), 404
    
    # Get target entity to equip the item to (from request data)
    data = request.json
    target_type = data.get('target_type', 'chad')  # Default to chad
    target_id = data.get('target_id')
    
    if target_type == 'waifu' and target_id:
        # Equipping to a waifu
        waifu = Waifu.query.filter_by(id=target_id, user_id=current_user.id).first()
        if not waifu:
            return jsonify({'success': False, 'message': 'Waifu not found or does not belong to you'}), 404
        
        # Unequip any existing item of the same type from this waifu
        existing_items = Item.query.filter_by(
            user_id=current_user.id, 
            waifu_id=waifu.id, 
            item_type_id=item.item_type_id, 
            is_equipped=True
        ).all()
        
        for existing_item in existing_items:
            if existing_item.id != item_id:
                existing_item.is_equipped = False
                existing_item.waifu_id = None
        
        # Equip this item to the waifu
        item.is_equipped = True
        item.waifu_id = waifu.id
        item.chad_id = None  # Unequip from chad if equipped
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'{item.item_type.name} equipped to {waifu.waifu_type.name}'
        })
    
    else:
        # Equipping to the user's chad
        if not current_user.chad:
            return jsonify({'success': False, 'message': 'You need to create a Chad character first'}), 400
        
        # Unequip any existing item of the same type
        existing_items = Item.query.filter_by(
            user_id=current_user.id, 
            chad_id=current_user.chad.id, 
            item_type_id=item.item_type_id, 
            is_equipped=True
        ).all()
        
        for existing_item in existing_items:
            if existing_item.id != item_id:
                existing_item.is_equipped = False
                existing_item.chad_id = None
        
        # Equip this item
        item.is_equipped = True
        item.chad_id = current_user.chad.id
        item.waifu_id = None  # Unequip from waifu if equipped
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'{item.item_type.name} equipped to your Chad'
        })

@inventory_bp.route('/item/<int:item_id>/unequip', methods=['POST'])
@login_required
def unequip_item(item_id):
    """Unequip an item from any equipped entity"""
    item = Item.query.filter_by(id=item_id, user_id=current_user.id).first()
    
    if not item:
        return jsonify({'success': False, 'message': 'Item not found or does not belong to you'}), 404
    
    if not item.is_equipped:
        return jsonify({'success': False, 'message': 'This item is not currently equipped'}), 400
    
    # Determine what the item was equipped to for the message
    equipped_to = "your Chad" if item.chad_id else "your waifu"
    
    # Unequip the item
    item.is_equipped = False
    item.chad_id = None
    item.waifu_id = None
    
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'{item.item_type.name} unequipped from {equipped_to}'
    })

@inventory_bp.route('/nft/<int:nft_id>')
@login_required
def get_nft_details(nft_id):
    """Get details for a specific NFT"""
    nft = NFT.query.filter_by(id=nft_id, owner_id=current_user.id).first()
    
    if not nft:
        return jsonify({'success': False, 'message': 'NFT not found or does not belong to you'}), 404
    
    # Load NFT metadata
    try:
        metadata_path = nft.metadata_uri.replace('https://chadbattles.com/static/', 'app/static/')
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
    except Exception as e:
        metadata = {
            "name": "Unknown NFT",
            "description": "Metadata not found",
            "image": "/static/img/placeholder.png",
            "attributes": []
        }
        current_app.logger.error(f"Error loading NFT metadata: {str(e)}")
    
    # Get the entity details
    entity = nft.get_entity()
    
    # Render NFT details partial template
    html = render_template(
        'inventory/partials/nft_details.html',
        nft=nft,
        metadata=metadata,
        entity=entity
    )
    
    return jsonify({'success': True, 'html': html, 'metadata': metadata})

@inventory_bp.route('/check-minted', methods=['POST'])
@login_required
def check_minted():
    """Check if an entity has already been minted as an NFT"""
    data = request.json
    entity_type = data.get('entity_type')
    entity_id = data.get('entity_id')
    
    if not entity_type or not entity_id:
        return jsonify({'success': False, 'message': 'Missing entity_type or entity_id'}), 400
    
    # Check if this entity has already been minted
    nft = NFT.query.filter_by(
        entity_type=entity_type,
        entity_id=entity_id
    ).first()
    
    return jsonify({
        'success': True,
        'is_minted': nft is not None,
        'nft_id': nft.id if nft else None
    }) 