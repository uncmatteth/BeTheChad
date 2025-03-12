import logging
from datetime import datetime, timedelta
from app import db
from app.models.cabal import Cabal, CabalMember, CabalBattle
from app.models.user import User
from app.models.chad import Chad
from app.utils.twitter_api import share_weekly_leaderboard, post_tweet
from app.models.referral import Referral
from app.models.cabal_analytics import CabalAnalytics

logger = logging.getLogger(__name__)

def send_weekly_cabal_recap():
    """
    Send weekly recap of cabal activities.
    
    This function:
    1. Generates the leaderboard of top cabals
    2. Shares the leaderboard on Twitter
    3. Sends personalized recaps to cabal leaders
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get the top cabals
        top_cabals = Cabal.get_leaderboard(limit=10)
        
        if not top_cabals or len(top_cabals) < 3:
            logger.warning("Not enough cabals for leaderboard")
            return False
        
        # Format cabal data for the leaderboard tweet
        cabal_data = []
        for cabal in top_cabals[:3]:  # Top 3 for the tweet
            cabal_data.append({
                'name': cabal.name,
                'level': cabal.level,
                'power': int(cabal.total_power),
                'rank': cabal.rank
            })
        
        # Share the weekly leaderboard on Twitter
        share_weekly_leaderboard(cabal_data)
        
        # Calculate the start of the previous week
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        
        # Process each cabal
        for cabal in top_cabals:
            # Get battles from the past week
            battles = CabalBattle.query.filter(
                CabalBattle.cabal_id == cabal.id,
                CabalBattle.completed == True,
                CabalBattle.scheduled_at >= week_ago
            ).all()
            
            # Count wins and losses
            wins = sum(1 for battle in battles if battle.result == 'win')
            losses = sum(1 for battle in battles if battle.result == 'loss')
            
            # Get new members from the past week
            new_members = CabalMember.query.filter(
                CabalMember.cabal_id == cabal.id,
                CabalMember.joined_at >= week_ago
            ).count()
            
            # Get referrals from the past week
            referrals = Referral.query.filter(
                Referral.cabal_id == cabal.id,
                Referral.created_at >= week_ago
            ).count()
            
            # Get the cabal leader
            leader_chad = Chad.query.get(cabal.leader_id)
            if leader_chad:
                leader_user = User.query.filter_by(chad_id=leader_chad.id).first()
                if leader_user and leader_user.twitter_handle:
                    # Create personalized recap for the leader
                    message = f"📊 Weekly Cabal Recap for {cabal.name} 📊\n\n"
                    message += f"🏆 Current Rank: #{cabal.rank}\n"
                    message += f"⚔️ Battles: {wins} wins, {losses} losses\n"
                    message += f"👥 New Members: {new_members}\n"
                    message += f"🔗 Referrals: {referrals}\n\n"
                    
                    # Add leaderboard position if in top 10
                    position = next((i+1 for i, c in enumerate(top_cabals) if c.id == cabal.id), None)
                    if position:
                        if position == 1:
                            message += "🥇 Your cabal is #1 on the leaderboard! Congratulations!\n\n"
                        elif position <= 3:
                            message += f"🏅 Your cabal is #{position} on the leaderboard! Keep it up!\n\n"
                        else:
                            message += f"📈 Your cabal is #{position} on the leaderboard.\n\n"
                    
                    # Add tips based on cabal's performance
                    if wins == 0 and battles:
                        message += "💡 Tip: Try appointing officers to boost your cabal's power in battles.\n"
                    if new_members == 0:
                        message += "💡 Tip: Share your referral link to recruit new members and earn rewards.\n"
                    
                    # Send the recap as a direct message to the leader
                    # Note: Direct messages require additional Twitter API permissions
                    # For now, we'll just post a tweet mentioning the leader
                    post_tweet(f"@{leader_user.twitter_handle} {message}")
        
        return True
    except Exception as e:
        logger.error(f"Error sending weekly cabal recap: {str(e)}")
        return False

def update_cabal_rankings():
    """
    Update the rankings of all cabals.
    
    This function:
    1. Recalculates the total power of each cabal
    2. Updates their rank on the leaderboard
    3. Records analytics data for each cabal
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get all active cabals
        cabals = Cabal.query.filter_by(is_active=True).all()
        
        # Update power and rank for each cabal
        for cabal in cabals:
            # Recalculate total power
            cabal.calculate_total_power()
            
            # Update rank
            cabal.update_rank()
            
            # Record analytics snapshot
            CabalAnalytics.create_snapshot(cabal.id)
        
        # Commit all changes
        db.session.commit()
        
        return True
    except Exception as e:
        logger.error(f"Error updating cabal rankings: {str(e)}")
        db.session.rollback()
        return False

def post_game_stats_update():
    """
    Post game statistics update to Twitter.
    
    This function:
    1. Generates a tweet with interesting game statistics
    2. Posts the tweet to the @RollMasterChad account
    3. Stores the tweet ID for later reply processing
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from app.utils.twitter_api import post_automated_stats_tweet
        from app.models.tweet_tracker import TweetTracker
        from app import db
        import time
        
        # Post the automated stats tweet
        result = post_automated_stats_tweet()
        
        if not result:
            logger.error("Failed to post automated stats tweet")
            return False
        
        logger.info("Successfully posted game stats update to Twitter")
        
        # Wait a moment for Twitter to process the tweet
        time.sleep(2)
        
        # Store the tweet ID for processing replies later
        # This requires checking the most recent tweet from our account
        from app.utils.twitter_api import get_twitter_api
        api = get_twitter_api()
        
        if api:
            try:
                # Get our own timeline
                tweets = api.user_timeline(screen_name="RollMasterChad", count=1)
                if tweets:
                    latest_tweet = tweets[0]
                    tweet_id = latest_tweet.id_str
                    
                    # Store this tweet ID in our database
                    tracker = TweetTracker(
                        tweet_id=tweet_id,
                        tweet_type="stats_update",
                        replied_to=False,
                        created_at=datetime.utcnow()
                    )
                    
                    db.session.add(tracker)
                    db.session.commit()
                    
                    logger.info(f"Stored stats tweet ID {tweet_id} for reply processing")
            except Exception as e:
                logger.error(f"Error retrieving or storing tweet ID: {str(e)}")
        
        return True
    except Exception as e:
        logger.error(f"Error posting game stats update: {str(e)}")
        return False

def process_tweet_replies():
    """
    Process replies to our previously posted automated tweets.
    
    This function:
    1. Retrieves recent automated tweets that haven't been processed for replies
    2. Checks for replies to these tweets
    3. Responds to selected replies
    4. Marks the tweets as processed
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from app.utils.twitter_api import handle_automated_tweet_replies
        from app.models.tweet_tracker import TweetTracker
        from app import db
        
        # Get tweets that haven't been processed for replies yet
        # Only process tweets from the last 48 hours to avoid rate limits
        two_days_ago = datetime.utcnow() - timedelta(days=2)
        pending_tweets = TweetTracker.query.filter_by(
            replied_to=False
        ).filter(
            TweetTracker.created_at >= two_days_ago
        ).order_by(
            TweetTracker.created_at.desc()
        ).limit(2).all()
        
        if not pending_tweets:
            logger.info("No pending tweets to process for replies")
            return True
        
        logger.info(f"Processing replies for {len(pending_tweets)} recent tweets")
        
        # Process each tweet
        for tweet in pending_tweets:
            replies_processed = handle_automated_tweet_replies(tweet.tweet_id)
            logger.info(f"Processed {replies_processed} replies for tweet {tweet.tweet_id}")
            
            # Mark as processed
            tweet.replied_to = True
            db.session.commit()
            
            # Sleep to respect rate limits
            if len(pending_tweets) > 1:
                time.sleep(30)
        
        return True
    except Exception as e:
        logger.error(f"Error processing tweet replies: {str(e)}")
        return False

def post_promotional_tweet():
    """
    Post a promotional tweet about how to play the game.
    
    This function:
    1. Generates a promotional tweet with instructions on playing the game
    2. Occasionally includes donation information
    3. Posts the tweet to the @RollMasterChad account
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from app.utils.twitter_api import post_promotional_tweet as post_promo
        
        # Post the promotional tweet
        result = post_promo()
        
        if result:
            logger.info("Successfully posted promotional tweet")
        else:
            logger.error("Failed to post promotional tweet")
            
        return result
    except Exception as e:
        logger.error(f"Error posting promotional tweet: {str(e)}")
        return False 