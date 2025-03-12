from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.chad import Chad, ChadClass
from app.models.item import CharacterItem
from app.utils.twitter_api import get_user_tweets, analyze_tweets, calculate_clout

chad_bp = Blueprint('chad', __name__)

@chad_bp.route('/')
@login_required
def index():
    """Chad character page"""
    # Get user's Chad character
    chad = current_user.chad
    
    if not chad:
        flash('You need to create a Chad character first!', 'warning')
        return redirect(url_for('main.index'))
    
    # Get character stats
    stats = chad.calculate_stats()
    
    # Get equipped items
    equipped_items = chad.equipped_items.all()
    
    # Get equipped waifus
    equipped_waifus = chad.equipped_waifus.all()
    
    # Get all user's items that can be equipped by Chad
    available_items = CharacterItem.query.filter_by(
        user_id=current_user.id,
        is_equipped=False
    ).all()
    
    return render_template('chad/index.html',
                          chad=chad,
                          stats=stats,
                          equipped_items=equipped_items,
                          equipped_waifus=equipped_waifus,
                          available_items=available_items)

@chad_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new Chad character"""
    # Check if user already has a Chad character
    if current_user.chad:
        flash('You already have a Chad character!', 'warning')
        return redirect(url_for('chad.index'))
    
    if request.method == 'POST':
        # Create character from X/Twitter profile
        try:
            # Get user tweets for analysis
            tweets = get_user_tweets(current_user.x_username)
            if not tweets:
                flash('Couldn\'t analyze your tweets. Make sure your account is public.', 'danger')
                return render_template('chad/create.html')
            
            # Analyze tweets to determine character class and stats
            analysis = analyze_tweets(tweets)
            
            # Calculate Clout stat
            clout = calculate_clout(current_user.x_id)
            
            # Get or create Chad Class
            chad_class = ChadClass.query.filter_by(name=analysis['chad_class']).first()
            if not chad_class:
                # Create default class
                chad_class = ChadClass(
                    name=analysis['chad_class'],
                    description=f"Masters of {analysis['chad_class']} energy",
                    base_clout_bonus=1,
                    base_roast_bonus=1,
                    base_cringe_resistance_bonus=1,
                    base_drip_bonus=1
                )
                db.session.add(chad_class)
                db.session.commit()
            
            # Create Chad character
            base_stats = analysis['base_stats']
            chad = Chad(
                user_id=current_user.id,
                class_id=chad_class.id,
                clout=clout or base_stats['clout'],
                roast_level=base_stats['roast_level'],
                cringe_resistance=base_stats['cringe_resistance'],
                drip_factor=base_stats['drip_factor']
            )
            db.session.add(chad)
            db.session.commit()
            
            flash('Your Chad character has been created!', 'success')
            return redirect(url_for('chad.index'))
        
        except Exception as e:
            flash(f'Error creating character: {str(e)}', 'danger')
            return render_template('chad/create.html')
    
    return render_template('chad/create.html')

@chad_bp.route('/equip-item', methods=['POST'])
@login_required
def equip_item():
    """Equip an item to the Chad character"""
    item_id = request.form.get('item_id')
    
    if not item_id:
        return jsonify({'success': False, 'message': 'No item specified'})
    
    # Get the item
    item = CharacterItem.query.get(item_id)
    
    if not item:
        return jsonify({'success': False, 'message': 'Item not found'})
    
    # Check ownership
    if item.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'You do not own this item'})
    
    # Get user's Chad character
    chad = current_user.chad
    
    if not chad:
        return jsonify({'success': False, 'message': 'You need to create a Chad character first'})
    
    # Try to equip the item
    success, message = item.equip(chad)
    
    return jsonify({'success': success, 'message': message})

@chad_bp.route('/unequip-item', methods=['POST'])
@login_required
def unequip_item():
    """Unequip an item from the Chad character"""
    item_id = request.form.get('item_id')
    
    if not item_id:
        return jsonify({'success': False, 'message': 'No item specified'})
    
    # Get the item
    item = CharacterItem.query.get(item_id)
    
    if not item:
        return jsonify({'success': False, 'message': 'Item not found'})
    
    # Check ownership
    if item.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'You do not own this item'})
    
    # Check if item is equipped
    if not item.is_equipped:
        return jsonify({'success': False, 'message': 'This item is not equipped'})
    
    # Try to unequip the item
    success, message = item.unequip()
    
    return jsonify({'success': success, 'message': message})

@chad_bp.route('/refresh-stats', methods=['POST'])
@login_required
def refresh_stats():
    """Refresh Chad character stats based on X/Twitter profile"""
    # Get user's Chad character
    chad = current_user.chad
    
    if not chad:
        return jsonify({'success': False, 'message': 'You need to create a Chad character first'})
    
    try:
        # Get user tweets for analysis
        tweets = get_user_tweets(current_user.x_username)
        if not tweets:
            return jsonify({'success': False, 'message': 'Couldn\'t analyze your tweets. Make sure your account is public.'})
        
        # Analyze tweets to determine character class and stats
        analysis = analyze_tweets(tweets)
        
        # Calculate Clout stat
        clout = calculate_clout(current_user.x_id)
        
        # Update Chad character
        chad.clout = clout or chad.clout
        
        # Update class if it has changed significantly
        new_class_name = analysis['chad_class']
        if new_class_name != chad.chad_class.name:
            # Check if the new class exists
            new_class = ChadClass.query.filter_by(name=new_class_name).first()
            if not new_class:
                # Create new class
                new_class = ChadClass(
                    name=new_class_name,
                    description=f"Masters of {new_class_name} energy",
                    base_clout_bonus=1,
                    base_roast_bonus=1,
                    base_cringe_resistance_bonus=1,
                    base_drip_bonus=1
                )
                db.session.add(new_class)
                db.session.commit()
            
            # Update Chad's class
            chad.class_id = new_class.id
        
        db.session.commit()
        
        # Get updated stats
        stats = chad.calculate_stats()
        
        return jsonify({
            'success': True,
            'message': 'Stats refreshed successfully',
            'stats': stats,
            'class': chad.chad_class.name
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error refreshing stats: {str(e)}'}) 