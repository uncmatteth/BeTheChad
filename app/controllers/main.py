"""
Main controller for Chad Battles.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User
from app.models.chad import Chad
from app.models.waifu import Waifu
from app.models.battle import Battle
from app.models.cabal import Cabal, CabalMember
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page route"""
    try:
        # Get user stats if logged in
        if current_user.is_authenticated:
            try:
                chad = current_user.chad
                
                # Get recent battles
                recent_battles = Battle.query.filter(
                    (Battle.initiator_id == chad.id) | (Battle.target_id == chad.id)
                ).order_by(Battle.created_at.desc()).limit(5).all()
                
                # Check if user is in a cabal
                cabal_member = CabalMember.query.filter_by(chad_id=chad.id).first()
                cabal = cabal_member.cabal if cabal_member else None
                
                # Get upcoming cabal battles if in a cabal
                upcoming_battles = []
                if cabal:
                    upcoming_battles = CabalBattle.query.filter_by(
                        cabal_id=cabal.id,
                        completed=False
                    ).filter(
                        CabalBattle.scheduled_at > datetime.utcnow()
                    ).order_by(CabalBattle.scheduled_at).limit(3).all()
            
                return render_template('index.html', 
                                    chad=chad, 
                                    recent_battles=recent_battles,
                                    cabal=cabal,
                                    upcoming_battles=upcoming_battles)
            except Exception as e:
                # If there's an error with getting user data, log it but still show the page
                current_app.logger.error(f"Error loading user data for authenticated user {current_user.id}: {str(e)}")
                flash("There was an issue loading your profile data. Please try again later.", "warning")
                return render_template('index.html')
        
        return render_template('index.html')
    except Exception as e:
        # Catch any other exceptions
        current_app.logger.error(f"Unexpected error in index route: {str(e)}")
        flash("An unexpected error occurred. Our team has been notified.", "danger")
        return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Render the user dashboard with their character, waifus, and battles."""
    try:
        # Attempt to get the user's Chad
        try:
            chad = Chad.query.filter_by(user_id=current_user.id).first()
            if not chad:
                current_app.logger.warning(f"No Chad found for user {current_user.id}")
                flash("You don't have a character yet. Let's create one!", "warning")
                return redirect(url_for('auth.create_character'))
        except Exception as e:
            current_app.logger.error(f"Error retrieving Chad for user {current_user.id}: {str(e)}")
            flash("There was an error retrieving your character. Please try again.", "danger")
            return render_template('dashboard.html', chad=None, error=True)
        
        # Get character stats
        try:
            stats = chad.get_total_stats()
        except Exception as e:
            current_app.logger.error(f"Error getting stats for Chad {chad.id}: {str(e)}")
            # Create a default stats object if get_total_stats fails
            class DefaultStats:
                def __init__(self):
                    self.clout = chad.clout
                    self.roast_level = chad.roast_level
                    self.cringe_resistance = chad.cringe_resistance
                    self.drip_factor = chad.drip_factor
            stats = DefaultStats()
        
        try:
            # Get equipped waifus
            equipped_waifus = chad.get_equipped_waifus()
        except Exception as e:
            current_app.logger.error(f"Error getting equipped waifus for Chad {chad.id}: {str(e)}")
            equipped_waifus = []
        
        try:
            # Get recent battles
            from app.models.battle import Battle
            battles = Battle.query.filter(
                (Battle.initiator_id == chad.id) | (Battle.opponent_id == chad.id)
            ).order_by(Battle.created_at.desc()).limit(5).all()
        except Exception as e:
            current_app.logger.error(f"Error getting battles for Chad {chad.id}: {str(e)}")
            battles = []
        
        # Get user's squad - this is optional
        squad = None
        try:
            # Try to import the Squad module
            try:
                from app.models.squad import Squad
                squad = Squad.query.join(Squad.members).filter_by(chad_id=chad.id).first()
            except ImportError:
                current_app.logger.warning("Squad module not available, skipping squad functionality")
            except Exception as e:
                current_app.logger.error(f"Error getting squad for Chad {chad.id}: {str(e)}")
        except Exception as e:
            current_app.logger.error(f"Error in squad processing: {str(e)}")

        return render_template(
            'dashboard.html',
            chad=chad,
            stats=stats,
            equipped_waifus=equipped_waifus,
            battles=battles,
            squad=squad
        )
    except Exception as e:
        current_app.logger.error(f"Error rendering dashboard: {str(e)}")
        import traceback
        current_app.logger.error(traceback.format_exc())
        flash("There was an error loading your dashboard. The team has been notified.", "danger")
        return render_template('dashboard.html', chad=None, error=True)

@main_bp.route('/battle-history')
@login_required
def battle_history():
    """Show the user's battle history."""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get the user's Chad character
    chad = current_user.chad
    
    if not chad:
        flash("You need to create a character first.", "warning")
        return redirect(url_for('main.dashboard'))
    
    # Get all battles for this user
    battles_query = Battle.query.filter(
        (Battle.initiator_id == chad.id) | (Battle.opponent_id == chad.id)
    ).order_by(Battle.created_at.desc())
    
    # Paginate the results
    pagination = battles_query.paginate(page=page, per_page=per_page, error_out=False)
    battles = pagination.items
    
    # Get battles filtered by result
    won_battles = Battle.query.filter_by(winner_id=chad.id).order_by(Battle.completed_at.desc()).limit(10).all()
    
    lost_battles = Battle.query.filter(
        ((Battle.initiator_id == chad.id) | (Battle.opponent_id == chad.id)) &
        (Battle.winner_id != chad.id) &
        (Battle.status == 'completed')
    ).order_by(Battle.completed_at.desc()).limit(10).all()
    
    ongoing_battles = Battle.query.filter(
        ((Battle.initiator_id == chad.id) | (Battle.opponent_id == chad.id)) &
        ((Battle.status == 'pending') | (Battle.status == 'in_progress'))
    ).order_by(Battle.created_at.desc()).all()
    
    return render_template(
        'main/battle_history.html',
        chad=chad,
        battles=battles,
        won_battles=won_battles,
        lost_battles=lost_battles,
        ongoing_battles=ongoing_battles,
        pagination=pagination
    )

@main_bp.route('/battle/<int:battle_id>')
@login_required
def battle_detail(battle_id):
    """Show details for a specific battle."""
    battle = Battle.query.get_or_404(battle_id)
    
    # Check if the user is a participant in this battle
    chad = current_user.chad
    if chad.id != battle.initiator_id and chad.id != battle.opponent_id:
        flash("You don't have permission to view this battle.", "danger")
        return redirect(url_for('main.battle_history'))
    
    return render_template('main/battle_detail.html', battle=battle, chad=chad)

@main_bp.route('/accept-battle/<int:battle_id>', methods=['POST'])
@login_required
def accept_battle(battle_id):
    """Accept a battle challenge."""
    battle = Battle.query.get_or_404(battle_id)
    
    # Check if the user is the opponent and battle is pending
    chad = current_user.chad
    if chad.id != battle.opponent_id or battle.status != 'pending':
        flash("Invalid battle or you don't have permission to accept it.", "danger")
        return redirect(url_for('main.battle_history'))
    
    # Update battle status
    battle.status = 'in_progress'
    db.session.commit()
    
    # TODO: Trigger battle simulation in background task
    
    flash("You've accepted the battle challenge!", "success")
    return redirect(url_for('main.battle_detail', battle_id=battle.id))

@main_bp.route('/decline-battle/<int:battle_id>', methods=['POST'])
@login_required
def decline_battle(battle_id):
    """Decline a battle challenge."""
    battle = Battle.query.get_or_404(battle_id)
    
    # Check if the user is the opponent and battle is pending
    chad = current_user.chad
    if chad.id != battle.opponent_id or battle.status != 'pending':
        flash("Invalid battle or you don't have permission to decline it.", "danger")
        return redirect(url_for('main.battle_history'))
    
    # Update battle status
    battle.status = 'canceled'
    db.session.commit()
    
    flash("You've declined the battle challenge.", "info")
    return redirect(url_for('main.battle_history'))

@main_bp.route('/leaderboard')
def leaderboard():
    """Global leaderboard route"""
    # Get top 10 chads by clout
    top_chads = Chad.query.order_by(Chad.clout.desc()).limit(10).all()
    
    # Get top 5 cabals
    top_cabals = Cabal.query.order_by(Cabal.total_power.desc()).limit(5).all()
    
    # Get the current user's chad rank if logged in
    user_rank = None
    if current_user.is_authenticated:
        # Count number of chads with more clout than current user
        user_rank = Chad.query.filter(Chad.clout > current_user.chad.clout).count() + 1
    
    return render_template('leaderboard.html', 
                          top_chads=top_chads,
                          top_cabals=top_cabals,
                          user_rank=user_rank)

@main_bp.route('/how-to-play')
def how_to_play():
    """Show the how to play guide."""
    return render_template('main/how_to_play.html')

@main_bp.route('/about')
def about():
    """Show the about page."""
    return render_template('main/about.html')

@main_bp.route('/waifu-collection')
@login_required
def waifu_collection():
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
    
    return render_template('waifu_collection.html', 
                          waifus=waifus, 
                          equipped_waifus=equipped_waifus)

@main_bp.route('/equip-waifu', methods=['POST'])
@login_required
def equip_waifu():
    """API endpoint to equip a waifu"""
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

@main_bp.route('/unequip-waifu', methods=['POST'])
@login_required
def unequip_waifu():
    """API endpoint to unequip a waifu"""
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

@main_bp.route('/profile/<chad_id>')
def profile(chad_id):
    """View a chad's profile"""
    chad = Chad.query.get_or_404(chad_id)
    
    # Find the User associated with this Chad to display Twitter handle
    user = User.query.filter_by(chad_id=chad.id).first()
    
    # Get recent battles
    recent_battles = Battle.query.filter(
        (Battle.initiator_id == chad.id) | (Battle.target_id == chad.id)
    ).order_by(Battle.created_at.desc()).limit(10).all()
    
    # Get battle stats
    battle_stats = {
        'total': len(recent_battles),
        'wins': sum(1 for b in recent_battles if 
                    (b.initiator_id == chad.id and b.result == 'initiator_win') or
                    (b.target_id == chad.id and b.result == 'target_win')),
        'losses': sum(1 for b in recent_battles if 
                      (b.initiator_id == chad.id and b.result == 'target_win') or
                      (b.target_id == chad.id and b.result == 'initiator_win'))
    }
    
    # If the user hasn't fought any battles, avoid division by zero
    if battle_stats['total'] > 0:
        battle_stats['win_rate'] = (battle_stats['wins'] / battle_stats['total']) * 100
    else:
        battle_stats['win_rate'] = 0
    
    # Get cabal info if applicable
    cabal_member = CabalMember.query.filter_by(chad_id=chad.id).first()
    cabal = cabal_member.cabal if cabal_member else None
    
    return render_template('profile.html', 
                          chad=chad, 
                          user=user,
                          battle_stats=battle_stats,
                          recent_battles=recent_battles,
                          cabal=cabal)

@main_bp.route('/tweets/<chad_id>')
def tweets(chad_id):
    """View a chad's tweets"""
    chad = Chad.query.get_or_404(chad_id)
    
    # Find the User associated with this Chad to display Twitter handle
    user = User.query.filter_by(chad_id=chad.id).first()
    
    # Get recent tweets
    tweets = Tweet.query.filter_by(chad_id=chad.id).order_by(Tweet.created_at.desc()).all()
    
    return render_template('tweets.html', 
                          chad=chad, 
                          user=user,
                          tweets=tweets)
    
@main_bp.route('/battles')
def battles():
    """Global recent battles"""
    # Get most recent battles
    recent_battles = Battle.query.order_by(Battle.created_at.desc()).limit(20).all()
    
    # Get current user's recent battles if logged in
    user_battles = []
    if current_user.is_authenticated:
        user_battles = Battle.query.filter(
            (Battle.initiator_id == current_user.chad.id) | 
            (Battle.target_id == current_user.chad.id)
        ).order_by(Battle.created_at.desc()).limit(5).all()
    
    return render_template('battles.html', 
                          recent_battles=recent_battles,
                          user_battles=user_battles)

@main_bp.route('/battle/<battle_id>')
def view_battle(battle_id):
    """View a specific battle"""
    battle = Battle.query.get_or_404(battle_id)
    
    # Get initiator and target chads
    initiator = Chad.query.get(battle.initiator_id)
    target = Chad.query.get(battle.target_id)
    
    # Get users for Twitter handles
    initiator_user = User.query.filter_by(chad_id=initiator.id).first()
    target_user = User.query.filter_by(chad_id=target.id).first()
    
    return render_template('battle_detail.html', 
                          battle=battle,
                          initiator=initiator,
                          target=target,
                          initiator_user=initiator_user,
                          target_user=target_user) 