import logging
import re
from datetime import datetime, timedelta
from app import db
from app.models.user import User
from app.models.chad import Chad, ChadClass
from app.models.waifu import Waifu, WaifuType, WaifuRarity
from app.models.battle import Battle
from app.utils.twitter_api import (
    get_user_profile, get_user_tweets, analyze_tweets, 
    calculate_clout, post_reply
)
import json
import random

logger = logging.getLogger(__name__)

# Command patterns
CREATE_CHARACTER_PATTERN = re.compile(r'CREATE\s+CHARACTER', re.IGNORECASE)
FIGHT_REQUEST_PATTERN = re.compile(r'.*@(\w+).*CHALLENGE\s+TO\s+BATTLE', re.IGNORECASE)
CHECK_STATS_PATTERN = re.compile(r'CHECK\s+STATS', re.IGNORECASE)
JOIN_CABAL_PATTERN = re.compile(r'JOIN\s+CABAL\s+([A-Za-z0-9_\s]+)', re.IGNORECASE)
CREATE_CABAL_PATTERN = re.compile(r'CREATE\s+CABAL\s+([A-Za-z0-9_\s]+)', re.IGNORECASE)
APPOINT_OFFICER_PATTERN = re.compile(r'APPOINT\s+@(\w+)\s+AS\s+(CLOUT|ROAST|CRINGE|DRIP)\s+OFFICER', re.IGNORECASE)
SCHEDULE_BATTLE_PATTERN = re.compile(r'BATTLE\s+CABAL\s+([A-Za-z0-9_\s]+)', re.IGNORECASE)
VOTE_REMOVE_LEADER_PATTERN = re.compile(r'VOTE\s+REMOVE\s+CABAL\s+LEADER', re.IGNORECASE)
OPT_IN_BATTLE_PATTERN = re.compile(r'JOIN\s+NEXT\s+CABAL\s+BATTLE', re.IGNORECASE)
HELP_PATTERN = re.compile(r'HELP', re.IGNORECASE)

def handle_mention(tweet):
    """Process mentions and route to appropriate handler"""
    try:
        tweet_id = tweet.get('id_str')
        user_screen_name = tweet.get('user', {}).get('screen_name')
        text = tweet.get('full_text', tweet.get('text', ''))
        
        # Check which command pattern matches
        if CREATE_CHARACTER_PATTERN.search(text):
            return handle_create_character(tweet_id, user_screen_name)
        elif FIGHT_REQUEST_PATTERN.search(text):
            match = FIGHT_REQUEST_PATTERN.search(text)
            opponent_name = match.group(1) if match else None
            return handle_fight_request(tweet_id, user_screen_name, opponent_name)
        elif CHECK_STATS_PATTERN.search(text):
            return handle_check_stats(tweet_id, user_screen_name)
        elif JOIN_CABAL_PATTERN.search(text):
            match = JOIN_CABAL_PATTERN.search(text)
            cabal_name = match.group(1).strip() if match else None
            return handle_join_cabal(tweet_id, user_screen_name, cabal_name)
        elif CREATE_CABAL_PATTERN.search(text):
            match = CREATE_CABAL_PATTERN.search(text)
            cabal_name = match.group(1).strip() if match else None
            return handle_create_cabal(tweet_id, user_screen_name, cabal_name)
        elif APPOINT_OFFICER_PATTERN.search(text):
            match = APPOINT_OFFICER_PATTERN.search(text)
            officer_name = match.group(1)
            officer_type = match.group(2).lower()
            return handle_appoint_officer(tweet_id, user_screen_name, officer_name, officer_type)
        elif SCHEDULE_BATTLE_PATTERN.search(text):
            match = SCHEDULE_BATTLE_PATTERN.search(text)
            opponent_cabal_name = match.group(1).strip() if match else None
            return handle_schedule_battle(tweet_id, user_screen_name, opponent_cabal_name)
        elif VOTE_REMOVE_LEADER_PATTERN.search(text):
            return handle_vote_remove_leader(tweet_id, user_screen_name)
        elif OPT_IN_BATTLE_PATTERN.search(text):
            return handle_opt_in_battle(tweet_id, user_screen_name)
        elif HELP_PATTERN.search(text):
            return handle_help(tweet_id, user_screen_name)
        else:
            # Unknown command
            reply = f"@{user_screen_name} I don't understand that command. Try 'HELP @RollMasterChad' for a list of commands."
            post_reply(reply, tweet_id)
            return False
    except Exception as e:
        logger.error(f"Error handling mention: {str(e)}")
        return False

def handle_create_character(tweet_id, username):
    """Handle the create character command"""
    try:
        # Check if user already exists
        user = User.query.filter_by(x_username=username).first()
        if user and user.chad:
            reply = f"@{username} You already have a Chad character! Check your stats with CHECK STATS @RollMasterChad"
            post_reply(reply, tweet_id)
            return False
        
        # Get user profile from Twitter
        profile = get_user_profile(username)
        if not profile:
            reply = f"@{username} Failed to fetch your X profile. Please try again later."
            post_reply(reply, tweet_id)
            return False
        
        # Get user tweets for analysis
        tweets = get_user_tweets(username)
        if not tweets:
            reply = f"@{username} Couldn't analyze your tweets. Make sure your account is public and try again."
            post_reply(reply, tweet_id)
            return False
        
        # Analyze tweets to determine character class and stats
        analysis = analyze_tweets(tweets)
        
        # Create or update User record
        if not user:
            user = User(
                x_id=profile.get('id_str'),
                x_username=profile.get('screen_name'),
                x_displayname=profile.get('name'),
                x_profile_image=profile.get('profile_image_url_https'),
                x_followers_count=profile.get('followers_count', 0),
                x_following_count=profile.get('friends_count', 0),
                last_login=datetime.utcnow()
            )
            db.session.add(user)
            db.session.commit()
        
        # Calculate Clout stat
        clout = calculate_clout(profile.get('id_str'))
        
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
            user_id=user.id,
            class_id=chad_class.id,
            clout=clout or base_stats['clout'],
            roast_level=base_stats['roast_level'],
            cringe_resistance=base_stats['cringe_resistance'],
            drip_factor=base_stats['drip_factor']
        )
        db.session.add(chad)
        db.session.commit()
        
        # Get a starter waifu
        starter_waifu_type = WaifuType.query.filter_by(name="Starter Waifu").first()
        if not starter_waifu_type:
            # Create a default starter waifu type if none exists
            starter_rarity = WaifuRarity.query.filter_by(name="Common").first()
            if not starter_rarity:
                starter_rarity = WaifuRarity(
                    name="Common",
                    description="The most common waifu rarity",
                    base_stat_multiplier=1.0,
                    drop_rate=0.5
                )
                db.session.add(starter_rarity)
                db.session.commit()
            
            starter_waifu_type = WaifuType(
                name="Starter Waifu",
                description="A basic waifu to start your journey",
                rarity_id=starter_rarity.id,
                base_clout_bonus=1,
                base_roast_bonus=1,
                base_cringe_resistance_bonus=1,
                base_drip_bonus=1
            )
            db.session.add(starter_waifu_type)
            db.session.commit()
        
        # Create the starter waifu instance
        starter_waifu = Waifu(
            waifu_type_id=starter_waifu_type.id,
            user_id=user.id
        )
        db.session.add(starter_waifu)
        db.session.commit()
        
        # Equip the starter waifu
        starter_waifu.equip(chad)
        
        # Send a success response
        reply = (
            f"@{username} Your Chad character has been created! ðŸŽ‰\n\n"
            f"Class: {chad_class.name}\n"
            f"Clout: {chad.clout}\n"
            f"Roast Level: {chad.roast_level}\n"
            f"Cringe Resistance: {chad.cringe_resistance}\n"
            f"Drip Factor: {chad.drip_factor}\n\n"
            f"You received a Starter Waifu! Check your stats with CHECK STATS @RollMasterChad"
        )
        post_reply(reply, tweet_id)
        
        return True
    except Exception as e:
        logger.error(f"Error creating character for {username}: {str(e)}")
        reply = f"@{username} You need to create a character first with 'CREATE CHARACTER @RollMasterChad'"
        post_reply(reply, tweet_id)
        return False

def handle_fight_request(tweet_id, username, opponent_name):
    """Handle a fight request by immediately starting the battle"""
    try:
        # Check if both users have characters
        initiator = User.query.filter_by(x_username=username).first()
        opponent = User.query.filter_by(x_username=opponent_name).first()
        
        if not initiator or not initiator.chad:
            reply = f"@{username} You need to create a character first with 'MAKE ME A CHAD @RollMasterChad'"
            post_reply(reply, tweet_id)
            return False
        
        if not opponent or not opponent.chad:
            reply = f"@{username} @{opponent_name} doesn't have a Chad character yet!"
            post_reply(reply, tweet_id)
            return False
        
        # Check if there's already a pending or active battle
        existing_battle = Battle.query.filter(
            db.or_(
                db.and_(Battle.initiator_id==initiator.chad.id, Battle.opponent_id==opponent.chad.id),
                db.and_(Battle.initiator_id==opponent.chad.id, Battle.opponent_id==initiator.chad.id)
            ),
            Battle.status.in_(['pending', 'in_progress'])
        ).first()
        
        if existing_battle:
            reply = f"@{username} There's already an active battle between you and @{opponent_name}!"
            post_reply(reply, tweet_id)
            return False
        
        # Create a new battle
        battle = Battle(
            initiator_id=initiator.chad.id,
            opponent_id=opponent.chad.id,
            initiator_chad_id=initiator.chad.id,
            opponent_chad_id=opponent.chad.id,
            status='in_progress',  # Start immediately instead of 'pending'
            challenge_tweet_id=tweet_id,
            started_at=datetime.utcnow()
        )
        db.session.add(battle)
        db.session.commit()
        
        # Initialize battle log
        battle.battle_log = json.dumps([{
            "turn": 0,
            "timestamp": datetime.utcnow().isoformat(),
            "event": "battle_started",
            "description": f"Battle between {initiator.chad.name} and {opponent.chad.name} has begun!"
        }])
        db.session.commit()
        
        # Perform automatic battle simulation
        battle_result = simulate_battle(battle)
        
        # Send battle notification and results
        reply = (
            f"⚔️ BATTLE STARTED! ⚔️\n\n"
            f"@{username} has challenged @{opponent_name} to a Chad Battle!\n\n"
            f"{battle_result}\n\n"
            f"Type CHECK STATS @RollMasterChad to see your updated stats!"
        )
        post_reply(reply, tweet_id)
        
        return True
    except Exception as e:
        logger.error(f"Error handling fight request from {username} to {opponent_name}: {str(e)}")
        reply = f"@{username} Sorry, there was an error processing your battle challenge. Please try again later."
        post_reply(reply, tweet_id)
        return False

def simulate_battle(battle):
    """Simulate a battle automatically"""
    try:
        # Get the participants
        initiator_chad = battle.initiator_chad
        opponent_chad = battle.opponent_chad
        
        # Basic simulation based on stats
        initiator_stats = initiator_chad.get_total_stats()
        opponent_stats = opponent_chad.get_total_stats()
        
        initiator_power = sum(initiator_stats.values())
        opponent_power = sum(opponent_stats.values())
        
        # Add some randomness (60% stats, 40% luck)
        initiator_roll = (initiator_power * 0.6) + (random.random() * initiator_power * 0.4)
        opponent_roll = (opponent_power * 0.6) + (random.random() * opponent_power * 0.4)
        
        # Determine winner
        if initiator_roll > opponent_roll:
            winner = initiator_chad
            loser = opponent_chad
            battle.winner_id = initiator_chad.user_id
            battle.loser_id = opponent_chad.user_id
        else:
            winner = opponent_chad
            loser = initiator_chad
            battle.winner_id = opponent_chad.user_id
            battle.loser_id = initiator_chad.user_id
        
        # Update battle status
        battle.status = 'completed'
        battle.completed_at = datetime.utcnow()
        
        # Add final battle log entry
        log = json.loads(battle.battle_log) if battle.battle_log else []
        log.append({
            "turn": 1,
            "timestamp": datetime.utcnow().isoformat(),
            "event": "battle_ended",
            "description": f"{winner.name} defeated {loser.name}!"
        })
        battle.battle_log = json.dumps(log)
        
        # Award XP
        winner_xp = random.randint(50, 100)
        loser_xp = random.randint(10, 30)
        
        winner.add_xp(winner_xp)
        loser.add_xp(loser_xp)
        
        # Award Chadcoin
        from app.models.transaction import Transaction
        winner_reward = random.randint(100, 200)
        winner.user.add_chadcoin(winner_reward)
        
        # Record transaction
        Transaction.record_chadcoin_transaction(
            user_id=winner.user_id,
            amount=winner_reward,
            description=f"Battle reward for defeating {loser.name}",
            related_entity=('chad', winner.id)
        )
        
        db.session.commit()
        
        # Generate battle summary
        return (
            f"🔥 {winner.name} has defeated {loser.name}! 🔥\n"
            f"\n"
            f"📊 BATTLE STATS:\n"
            f"• {winner.name}: {winner_xp} XP gained, {winner_reward} Chadcoin earned\n"
            f"• {loser.name}: {loser_xp} XP gained (for effort)\n"
            f"\n"
            f"The battle was fierce, but {winner.name}'s superior {max(winner.get_total_stats().items(), key=lambda x: x[1])[0].replace('_', ' ')} won the day!"
        )
    except Exception as e:
        logger.error(f"Error simulating battle {battle.id}: {str(e)}")
        return "The battle couldn't be completed due to technical difficulties. Both Chads walked away unharmed."

def handle_check_stats(tweet_id, username):
    """Handle stats check request"""
    try:
        user = User.query.filter_by(x_username=username).first()
        if not user or not user.chad:
            reply = f"@{username} You need to create a character first with 'CREATE CHARACTER @RollMasterChad'"
            post_reply(reply, tweet_id)
            return False
        
        chad = user.chad
        stats = chad.calculate_stats()
        
        # Get equipped waifus
        equipped_waifus = chad.equipped_waifus.all()
        waifu_names = [w.waifu_type.name for w in equipped_waifus]
        
        # Create stats message
        reply = (
            f"@{username} Your Chad Stats:\n\n"
            f"Class: {chad.chad_class.name}\n"
            f"Level: {chad.level}\n"
            f"Clout: {stats['clout']}\n"
            f"Roast Level: {stats['roast_level']}\n"
            f"Cringe Resistance: {stats['cringe_resistance']}\n"
            f"Drip Factor: {stats['drip_factor']}\n\n"
            f"Battles Won: {chad.battles_won}\n"
            f"Battles Lost: {chad.battles_lost}\n"
        )
        
        if waifu_names:
            reply += f"\nEquipped Waifus: {', '.join(waifu_names)}"
        
        if chad.cabal_membership and chad.cabal_membership.cabal:
            cabal = chad.cabal_membership.cabal
            reply += f"\n\nCabal: {cabal.name} (Level {cabal.level})"
        
        post_reply(reply, tweet_id)
        return True
    except Exception as e:
        logger.error(f"Error checking stats for {username}: {str(e)}")
        reply = f"@{username} Sorry, there was an error checking your stats. Please try again later."
        post_reply(reply, tweet_id)
        return False

def handle_join_cabal(tweet_id, username, cabal_name):
    """Handle join cabal request"""
    try:
        # Get user by twitter handle
        from app.models.cabal import Cabal
        from app.models.user import User
        
        user = User.query.filter_by(twitter_handle=username).first()
        
        if not user or not user.chad:
            return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."
        
        # Check if user is already in a cabal
        if user.chad.cabal_membership:
            return f"@{username} You're already in the cabal '{user.chad.cabal_membership.cabal.name}'! Leave your current cabal first."
        
        # Find the cabal
        cabal = Cabal.query.filter_by(name=cabal_name).first()
        if not cabal:
            return f"@{username} The cabal '{cabal_name}' doesn't exist. Create it with CREATE NEW CABAL name @RollMasterChad"
        
        # Try to join the cabal
        success, message = cabal.add_member(user.chad.id)
        
        if success:
            return f"@{username} You have successfully joined the cabal '{cabal_name}'!"
        else:
            return f"@{username} Unable to join cabal: {message}"
    except Exception as e:
        logger.error(f"Error handling join cabal request from {username}: {str(e)}")
        return f"@{username} Sorry, there was an error joining the cabal. Please try again later."

def handle_create_cabal(tweet_id, username, cabal_name):
    """Handle create cabal request"""
    try:
        from app.models.cabal import Cabal
        from app.models.user import User
        
        user = User.query.filter_by(twitter_handle=username).first()
        
        if not user or not user.chad:
            return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."
        
        # Check if user is already in a cabal
        if user.chad.cabal_membership:
            return f"@{username} You're already in the cabal '{user.chad.cabal_membership.cabal.name}'! Leave your current cabal first."
        
        # Check if the cabal name already exists
        existing_cabal = Cabal.query.filter_by(name=cabal_name).first()
        if existing_cabal:
            return f"@{username} The cabal '{cabal_name}' already exists! Try joining it with JOIN CABAL name @RollMasterChad"
        
        # Create the cabal
        cabal = Cabal(
            name=cabal_name,
            description=f"Cabal led by {username}",
            leader_id=user.chad.id
        )
        db.session.add(cabal)
        db.session.commit()
        
        # Add user as member
        from app.models.cabal import CabalMember
        member = CabalMember(
            cabal_id=cabal.id,
            chad_id=user.chad.id,
            is_active=True
        )
        db.session.add(member)
        db.session.commit()
        
        return f"@{username} Successfully created cabal '{cabal_name}'! Invite others to join with JOIN CABAL name @RollMasterChad"
        
    except Exception as e:
        logger.error(f"Error creating cabal for {username}: {str(e)}")
        return f"@{username} Sorry, there was an error creating the cabal. Please try again later."

def handle_appoint_officer(tweet_id, username, officer_name, officer_type):
    """Handle appointing a cabal officer"""
    try:
        from app.models.cabal import Cabal, CabalMember
        from app.models.user import User
        
        # Map the officer type from the tweet to the database role type
        role_type_map = {
            'clout': 'clout',
            'roast': 'roast_level',
            'cringe': 'cringe_resistance',
            'drip': 'drip_factor'
        }
        
        # Convert the officer type to the correct database role type
        role_type = role_type_map.get(officer_type.lower())
        if not role_type:
            return f"@{username} Invalid officer type. Must be CLOUT, ROAST, CRINGE, or DRIP."
        
        # Get the appointer (cabal leader)
        leader_user = User.query.filter_by(twitter_handle=username).first()
        
        if not leader_user or not leader_user.chad:
            return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."
        
        # Check if user is a cabal leader
        cabal = Cabal.query.filter_by(leader_id=leader_user.chad.id).first()
        
        if not cabal:
            return f"@{username} You are not the Lord of the Shill for any cabal."
        
        # Find the officer user
        officer_user = User.query.filter_by(twitter_handle=officer_name).first()
        
        if not officer_user or not officer_user.chad:
            return f"@{username} The user @{officer_name} does not have a character in the game."
        
        # Check if the officer is in the leader's cabal
        member = CabalMember.query.filter_by(
            cabal_id=cabal.id,
            chad_id=officer_user.chad.id
        ).first()
        
        if not member:
            return f"@{username} @{officer_name} is not a member of your cabal."
        
        # Appoint the officer
        success, message = cabal.appoint_officer(officer_user.chad.id, role_type)
        
        if success:
            officer_title = cabal.get_officer_title(role_type)
            return f"@{username} @{officer_name} has been appointed as {officer_title} of your cabal."
        else:
            return f"@{username} Unable to appoint officer: {message}"
    except Exception as e:
        logger.error(f"Error appointing officer from {username}: {str(e)}")
        return f"@{username} Sorry, there was an error appointing the officer. Please try again later."

def handle_schedule_battle(tweet_id, username, opponent_cabal_name):
    """Handle scheduling a cabal battle"""
    try:
        from app.models.cabal import Cabal
        from app.models.user import User
        
        # Get the cabal leader
        leader_user = User.query.filter_by(twitter_handle=username).first()
        
        if not leader_user or not leader_user.chad:
            return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."
        
        # Check if user is a cabal leader
        cabal = Cabal.query.filter_by(leader_id=leader_user.chad.id).first()
        
        if not cabal:
            return f"@{username} You are not the Lord of the Shill for any cabal."
        
        # Find the opponent cabal
        opponent_cabal = Cabal.query.filter_by(name=opponent_cabal_name).first()
        
        if not opponent_cabal:
            return f"@{username} The cabal '{opponent_cabal_name}' does not exist."
        
        # Check if this is our own cabal
        if cabal.id == opponent_cabal.id:
            return f"@{username} You cannot battle your own cabal."
        
        # Check if we can schedule more battles this week
        if not cabal.can_schedule_battle():
            return f"@{username} Your cabal has already scheduled the maximum 3 battles this week."
        
        # Schedule the battle for 24 hours from now
        battle_time = datetime.utcnow() + timedelta(hours=24)
        success, message = cabal.schedule_battle(opponent_cabal.id, battle_time)
        
        if success:
            # Get opponent cabal leader for the mention
            from app.models.chad import Chad
            opponent_leader = Chad.query.get(opponent_cabal.leader_id)
            opponent_user = User.query.filter_by(chad_id=opponent_leader.id).first()
            opponent_username = opponent_user.twitter_handle if opponent_user else "Unknown"
            
            return f"@{username} Battle with '{opponent_cabal_name}' scheduled! @{opponent_username} your cabal has been challenged to battle in 24 hours. Members can opt in with JOIN NEXT CABAL BATTLE @RollMasterChad"
        else:
            return f"@{username} Unable to schedule battle: {message}"
    except Exception as e:
        logger.error(f"Error scheduling battle from {username}: {str(e)}")
        return f"@{username} Sorry, there was an error scheduling the battle. Please try again later."

def handle_vote_remove_leader(tweet_id, username):
    """Handle voting to remove a cabal leader"""
    try:
        from app.models.cabal import CabalMember
        from app.models.user import User
        
        # Get the voter
        voter_user = User.query.filter_by(twitter_handle=username).first()
        
        if not voter_user or not voter_user.chad:
            return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."
        
        # Check if voter is in a cabal
        cabal_member = CabalMember.query.filter_by(chad_id=voter_user.chad.id).first()
        
        if not cabal_member:
            return f"@{username} You are not a member of any cabal."
        
        # Check if voter is the leader (can't vote against themselves)
        if cabal_member.cabal.leader_id == voter_user.chad.id:
            return f"@{username} You cannot vote to remove yourself as leader."
        
        # Cast the vote
        success, message = cabal_member.cabal.vote_to_remove_leader(voter_user.chad.id)
        
        if success:
            # If the message indicates the leader was removed, a new leader was appointed
            if "is now the leader" in message:
                return f"@{username} Your vote was successful! {message}"
            else:
                # Get current vote count and percentage
                from app.models.cabal import CabalVote
                votes = CabalVote.query.filter_by(
                    cabal_id=cabal_member.cabal.id,
                    vote_type='remove_leader',
                    target_id=cabal_member.cabal.leader_id
                ).count()
                
                active_members = cabal_member.cabal.get_active_member_count()
                percentage = (votes / active_members * 100) if active_members > 0 else 0
                
                return f"@{username} Your vote to remove the cabal leader has been recorded. Current status: {votes} votes ({percentage:.1f}% of active members)."
        else:
            return f"@{username} Unable to vote: {message}"
    except Exception as e:
        logger.error(f"Error processing vote from {username}: {str(e)}")
        return f"@{username} Sorry, there was an error processing your vote. Please try again later."

def handle_opt_in_battle(tweet_id, username):
    """Handle opting into a cabal battle"""
    try:
        from app.models.cabal import CabalMember, CabalBattle
        from app.models.user import User
        
        # Get the user
        user = User.query.filter_by(twitter_handle=username).first()
        
        if not user or not user.chad:
            return f"@{username} You need to create a character first. Use CREATE CHARACTER @RollMasterChad to get started."
        
        # Check if user is in a cabal
        cabal_member = CabalMember.query.filter_by(chad_id=user.chad.id).first()
        
        if not cabal_member:
            return f"@{username} You are not a member of any cabal."
        
        # Find the next scheduled battle for this cabal
        next_battle = CabalBattle.query.filter_by(
            cabal_id=cabal_member.cabal.id,
            completed=False
        ).filter(
            CabalBattle.scheduled_at > datetime.utcnow()
        ).order_by(CabalBattle.scheduled_at).first()
        
        if not next_battle:
            return f"@{username} Your cabal does not have any upcoming battles scheduled."
        
        # Opt into the battle
        success, message = cabal_member.opt_into_battle(next_battle.id)
        
        if success:
            # Get opponent cabal name
            from app.models.cabal import Cabal
            opponent_cabal = Cabal.query.get(next_battle.opponent_cabal_id)
            opponent_name = opponent_cabal.name if opponent_cabal else "Unknown"
            
            battle_time = next_battle.scheduled_at.strftime("%Y-%m-%d %H:%M UTC")
            
            return f"@{username} You have successfully opted into the battle against '{opponent_name}' scheduled for {battle_time}. Prepare for glory!"
        else:
            return f"@{username} Unable to opt into battle: {message}"
    except Exception as e:
        logger.error(f"Error opting into battle from {username}: {str(e)}")
        return f"@{username} Sorry, there was an error opting into the battle. Please try again later."

def handle_help(tweet_id, username):
    """Handle help request"""
    try:
        help_message = f"""@{username} Chad Battles Commands:

• CREATE CHARACTER @RollMasterChad - Create a new character
• CHECK STATS @RollMasterChad - Check your character's stats
• I'm going to CRUSH @opponent! CHALLENGE TO BATTLE @RollMasterChad - Challenge someone to battle

Cabal Commands:
• CREATE CABAL name @RollMasterChad - Create a new cabal
• JOIN CABAL name @RollMasterChad - Join an existing cabal
• APPOINT @member AS CLOUT/ROAST/CRINGE/DRIP OFFICER @RollMasterChad - Appoint a cabal officer
• BATTLE CABAL name @RollMasterChad - Schedule a battle with another cabal
• JOIN NEXT CABAL BATTLE @RollMasterChad - Opt into your cabal's next battle
• VOTE REMOVE CABAL LEADER @RollMasterChad - Vote to remove your cabal's leader

Visit https://chadbattles.com for more info!"""
        
        return help_message
    except Exception as e:
        logger.error(f"Error generating help for {username}: {str(e)}")
        return f"@{username} Sorry, there was an error generating help. Please try again later." 