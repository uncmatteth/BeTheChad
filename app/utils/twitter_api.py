"""
Twitter API utilities for social media integration.
This is a mock implementation for development purposes.
"""
import logging
import os
import tweepy
from datetime import datetime, timedelta
import random
import time

# Set up logging
logger = logging.getLogger(__name__)

def get_twitter_api():
    """
    Get a Twitter API client.
    
    Returns:
        tweepy.API: Twitter API client or None if configuration is missing
    """
    try:
        # Get Twitter API credentials from environment variables
        api_key = os.environ.get('TWITTER_API_KEY')
        api_secret = os.environ.get('TWITTER_API_SECRET')
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        
        # Check if credentials are available
        if not all([api_key, api_secret, access_token, access_token_secret]):
            logger.warning("Twitter API credentials not found in environment variables")
            return None
        
        # Set up authentication
        auth = tweepy.OAuth1UserHandler(
            api_key, api_secret, access_token, access_token_secret
        )
        
        # Create API client
        api = tweepy.API(auth)
        
        return api
    except Exception as e:
        logger.error(f"Error creating Twitter API client: {e}")
        return None

def get_user_profile(username):
    """Get a user's profile data from Twitter"""
    try:
        api = get_twitter_api()
        if not api:
            return None
        
        user = api.get_user(screen_name=username)
        return user._json
    except Exception as e:
        logger.error(f"Error getting user profile for {username}: {str(e)}")
        return None

def get_user_tweets(username, count=50):
    """Get a user's recent tweets"""
    try:
        api = get_twitter_api()
        if not api:
            return []
        
        tweets = api.user_timeline(screen_name=username, count=count, tweet_mode='extended')
        return [tweet._json for tweet in tweets]
    except Exception as e:
        logger.error(f"Error getting tweets for {username}: {str(e)}")
        return []

def analyze_tweets(tweets):
    """Analyze a user's tweets to determine their Chad Class and stats"""
    # Count occurrences of various keywords
    keyword_counts = {}
    keywords = [
        'meme', 'pepe', 'wojak', 'crypto', 'nft', 'hodl', 'moon', 'alpha', 'chad',
        'based', 'sigma', 'ratio', 'king', 'gigachad', 'normie', 'gm', 'wagmi',
        'ngmi', 'bullish', 'bearish', 'fud', 'dyor', 'btc', 'eth', 'solana',
        'defi', 'staking', 'gym', 'debate', 'investing', 'diamond hands'
    ]
    
    for tweet in tweets:
        text = tweet.get('text', '').lower()
        created_at = datetime.strptime(tweet.get('created_at', ''), '%a %b %d %H:%M:%S +0000 %Y')
        
        # Process each keyword
        for keyword in keywords:
            if keyword in text:
                if keyword not in keyword_counts:
                    keyword_counts[keyword] = {
                        'count': 0,
                        'timestamps': []
                    }
                keyword_counts[keyword]['count'] += 1
                keyword_counts[keyword]['timestamps'].append(created_at)
    
    # Check for account age and tweet distribution
    account_age, tweet_distribution, is_suspicious = analyze_account_behavior(tweets, keyword_counts)
    
    # Determine Chad Class based on keyword frequencies, account age, and distribution
    chad_class = determine_chad_class(keyword_counts, account_age, tweet_distribution, is_suspicious)
    
    # Calculate base stats based on keyword frequencies and engagement
    base_stats = calculate_base_stats(tweets, keyword_counts)
    
    return {
        'chad_class': chad_class,
        'base_stats': base_stats,
        'keyword_analysis': {k: v['count'] for k, v in keyword_counts.items()},
        'account_metadata': {
            'age_days': account_age,
            'distribution_score': tweet_distribution,
            'suspicious_activity': is_suspicious
        }
    }

def analyze_account_behavior(tweets, keyword_counts):
    """Analyze account age and tweet distribution for suspicious patterns"""
    from datetime import datetime, timedelta
    
    # Get current time
    now = datetime.utcnow()
    
    # Calculate account age
    if tweets and len(tweets) > 0:
        # Get the earliest tweet
        created_at_str = min(tweets, key=lambda x: x.get('created_at', '')).get('created_at', '')
        if created_at_str:
            created_at = datetime.strptime(created_at_str, '%a %b %d %H:%M:%S +0000 %Y')
            account_age = (now - created_at).days
        else:
            account_age = 0
    else:
        account_age = 0
    
    # Analyze keyword distribution over time
    is_suspicious = False
    tweet_distribution = 1.0  # 1.0 means evenly distributed
    
    # Check for suspicious patterns
    if keyword_counts:
        # Check if all keywords were used in the last week
        recent_threshold = now - timedelta(days=7)
        
        # Count keywords with timestamps
        keywords_with_timestamps = [k for k, v in keyword_counts.items() if 'timestamps' in v and v['timestamps']]
        
        if keywords_with_timestamps:
            # Calculate percentage of keywords that only appear in recent tweets
            recent_only_keywords = 0
            for keyword, data in keyword_counts.items():
                if 'timestamps' in data and data['timestamps']:
                    if all(ts > recent_threshold for ts in data['timestamps']):
                        recent_only_keywords += 1
            
            if recent_only_keywords > 0:
                recent_keyword_percentage = recent_only_keywords / len(keywords_with_timestamps)
                
                # If more than 80% of keywords only appear in recent tweets, flag as suspicious
                if recent_keyword_percentage > 0.8 and len(keywords_with_timestamps) > 3:
                    is_suspicious = True
                    tweet_distribution = 0.2
                elif recent_keyword_percentage > 0.5:
                    tweet_distribution = 0.5
    
    return account_age, tweet_distribution, is_suspicious

def determine_chad_class(keyword_counts, account_age=None, tweet_distribution=None, is_suspicious=False):
    """Determine the user's Chad Class based on keyword frequencies and account behavior"""
    # First handle special cases
    
    # Format keyword_counts if it's the new format
    if isinstance(keyword_counts, dict) and all(isinstance(v, dict) for v in keyword_counts.values()):
        keyword_counts_simple = {k: v['count'] for k, v in keyword_counts.items()}
    else:
        keyword_counts_simple = keyword_counts
    
    # 1. If suspicious pattern detected, assign Clown class
    if is_suspicious:
        return "Clown"
    
    # 2. If very new account with few tweets, assign Newbie class
    if account_age is not None and account_age < 30:
        return "Newbie"
    
    # 3. Check for Blockchain Detective (rare class)
    blockchain_detective_keywords = ['onchain', 'blockchain', 'detective', 'investigation', 'forensics', 'sleuth']
    blockchain_detective_score = sum(keyword_counts_simple.get(keyword, 0) for keyword in blockchain_detective_keywords)
    
    if blockchain_detective_score >= 10 and account_age and account_age > 365:
        # Only assign if they have been active for over a year and have significant relevant content
        return "Blockchain Detective"
    
    # Define class criteria for regular classes
    class_criteria = {
        'Meme Overlord': ['meme', 'pepe', 'wojak'],
        'Crypto Knight': ['crypto', 'nft', 'hodl', 'moon'],
        'Alpha Chad': ['alpha', 'chad', 'based'],
        'Sigma Grindset': ['sigma', 'based', 'grind'],
        'Ratio King': ['ratio', 'based', 'chad'],
        'KOL': ['opinion', 'leader', 'influence', 'trend'],
        'Tech Bro': ['startup', 'disrupt', 'scale', 'tech'],
        'Gym Rat': ['gym', 'protein', 'lift', 'gains'],
        'Debate Lord': ['debate', 'argument', 'logic', 'fallacy'],
        'Diamond Hands': ['hodl', 'diamond', 'hands', 'hold'],
        'Lore Master': ['lore', 'history', 'knowledge', 'facts']
    }
    
    # Score each class
    class_scores = {}
    for class_name, keywords in class_criteria.items():
        score = sum(keyword_counts_simple.get(keyword, 0) for keyword in keywords)
        
        # Apply tweet distribution factor if available
        if tweet_distribution is not None:
            score *= tweet_distribution
            
        class_scores[class_name] = score
    
    # Find the highest scoring class
    top_class = max(class_scores.items(), key=lambda x: x[1])
    
    # Default to "Normie Chad" if no strong class preference
    if top_class[1] < 3:
        return "Normie Chad"
    
    return top_class[0]

def calculate_base_stats(tweets, keyword_counts):
    """Calculate base stats based on Twitter activity and keywords"""
    # Initialize stats
    clout = 0
    roast_level = 5
    cringe_resistance = 5
    drip_factor = 5
    
    # Calculate engagement metrics
    total_likes = sum(tweet.get('favorite_count', 0) for tweet in tweets)
    total_retweets = sum(tweet.get('retweet_count', 0) for tweet in tweets)
    
    # Calculate average engagement per tweet
    if tweets:
        avg_likes = total_likes / len(tweets)
        avg_retweets = total_retweets / len(tweets)
    else:
        avg_likes = 0
        avg_retweets = 0
    
    # Adjust stats based on engagement
    roast_level += min(5, int(avg_retweets / 10))
    drip_factor += min(5, int(avg_likes / 20))
    
    # Adjust stats based on keywords
    roast_level += min(3, keyword_counts.get('ratio', 0))
    cringe_resistance += min(3, keyword_counts.get('based', 0))
    drip_factor += min(3, keyword_counts.get('alpha', 0) + keyword_counts.get('sigma', 0))
    
    # Clout calculation will happen separately using follower network analysis
    
    return {
        'clout': clout,
        'roast_level': roast_level,
        'cringe_resistance': cringe_resistance,
        'drip_factor': drip_factor
    }

def calculate_clout(user_id):
    """Calculate Clout stat based on follower network strength"""
    try:
        api = get_twitter_api()
        if not api:
            return 0
        
        # Get user followers (limited to 200 by Twitter API)
        followers = api.get_followers(user_id=user_id, count=200)
        
        # Sum the follower counts of followers (measure of network influence)
        total_followers_of_followers = sum(follower.followers_count for follower in followers)
        
        # Normalize the value
        clout = min(100, int(total_followers_of_followers / 10000))
        
        return clout
    except Exception as e:
        logger.error(f"Error calculating clout for user {user_id}: {str(e)}")
        return 5  # Default value

def post_tweet(message):
    """
    Post a tweet with the given message.
    
    Args:
        message (str): The message to tweet
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        api = get_twitter_api()
        if not api:
            logger.warning("Cannot post tweet: Twitter API not initialized")
            return False
        
        # Ensure the message is within Twitter's character limit (280 characters)
        if len(message) > 280:
            message = message[:277] + "..."
        
        # Post the tweet
        api.update_status(message)
        logger.info(f"Tweet posted successfully: {message[:50]}...")
        return True
    except Exception as e:
        logger.error(f"Error posting tweet: {str(e)}")
        return False

def post_reply(message, in_reply_to_status_id):
    """Post a reply to a tweet"""
    try:
        api = get_twitter_api()
        if not api:
            return None
        
        tweet = api.update_status(message, in_reply_to_status_id=in_reply_to_status_id)
        return tweet._json.get('id_str')
    except Exception as e:
        logger.error(f"Error posting reply: {str(e)}")
        return None

def monitor_mentions(since_id=None):
    """Monitor and process @RollMasterChad mentions"""
    try:
        api = get_twitter_api()
        if not api:
            return []
        
        if since_id:
            mentions = api.mentions_timeline(since_id=since_id, tweet_mode='extended')
        else:
            # If no since_id, just get the last 24 hours of mentions
            since_time = datetime.utcnow() - timedelta(hours=24)
            mentions = []
            
            for tweet in tweepy.Cursor(api.mentions_timeline, tweet_mode='extended').items(100):
                # Stop if we reach tweets older than 24 hours
                created_at = tweet.created_at
                if created_at < since_time:
                    break
                mentions.append(tweet)
        
        return [mention._json for mention in mentions]
    except Exception as e:
        logger.error(f"Error monitoring mentions: {str(e)}")
        return []

def create_tweet(message):
    """
    Create a tweet with the given message.
    
    Args:
        message (str): The message to tweet
        
    Returns:
        str: The ID of the created tweet, or None if there was an error
    """
    try:
        api = get_twitter_api()
        if not api:
            return None
        
        tweet = api.update_status(message)
        return tweet._json.get('id_str')
    except Exception as e:
        logger.error(f"Error creating tweet: {str(e)}")
        return None

def share_cabal_creation(cabal_name, creator_name):
    """
    Mock function to share cabal creation on Twitter.
    
    Args:
        cabal_name (str): Name of the cabal
        creator_name (str): Name of the creator
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock sharing cabal creation: {cabal_name} created by {creator_name}")
    return True

def share_cabal_level_up(cabal_name, new_level):
    """
    Mock function to share cabal level up on Twitter.
    
    Args:
        cabal_name (str): Name of the cabal
        new_level (int): New level of the cabal
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock sharing cabal level up: {cabal_name} reached level {new_level}")
    return True

def share_battle_result(winner_name, loser_name, battle_type="PvP"):
    """
    Mock function to share battle result on Twitter.
    
    Args:
        winner_name (str): Name of the winner
        loser_name (str): Name of the loser
        battle_type (str): Type of battle (PvP, PvE)
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock sharing battle result: {winner_name} defeated {loser_name} in {battle_type} battle")
    return True

def share_cabal_achievement(cabal_name, achievement_name):
    """
    Mock function to share cabal achievement on Twitter.
    
    Args:
        cabal_name (str): Name of the cabal
        achievement_name (str): Name of the achievement
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Mock sharing cabal achievement: {cabal_name} earned {achievement_name}")
    return True

def generate_referral_link(cabal_id, invite_code, referrer_username):
    """
    Generate a referral link for a cabal with tracking.
    
    Args:
        cabal_id (str): The ID of the cabal
        invite_code (str): The invite code for the cabal
        referrer_username (str): The Twitter username of the referrer
        
    Returns:
        str: A formatted referral link
    """
    base_url = os.getenv('APP_URL', 'https://chadbattles.com')
    referral_url = f"{base_url}/cabal/join?code={invite_code}&ref={referrer_username}"
    return referral_url

def share_referral_invitation(cabal_name, referrer_username, invite_code, cabal_id):
    """
    Share a tweet with a referral link to join a cabal.
    
    Args:
        cabal_name (str): The name of the cabal
        referrer_username (str): The Twitter username of the referrer
        invite_code (str): The invite code for the cabal
        cabal_id (str): The ID of the cabal
        
    Returns:
        str: The ID of the created tweet, or None if there was an error
    """
    referral_link = generate_referral_link(cabal_id, invite_code, referrer_username)
    message = f"🔗 Join my cabal '{cabal_name}' in #ChadBattles! Use this link to get started: {referral_link} #GamersUnite #CryptoGaming"
    return create_tweet(message)

def share_weekly_leaderboard(cabal_data):
    """
    Share the weekly cabal leaderboard on Twitter.
    
    Args:
        cabal_data (list): List of dictionaries containing cabal information
            Each dictionary should have 'name', 'level', 'power', and 'rank' keys
            
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not cabal_data or len(cabal_data) < 1:
            logger.warning("Cannot share leaderboard: No cabal data provided")
            return False
        
        # Format the current date
        current_date = datetime.utcnow().strftime("%B %d, %Y")
        
        # Create the leaderboard message
        message = f"🏆 Chad Battles Weekly Cabal Leaderboard - {current_date} 🏆\n\n"
        
        # Add the top cabals to the message
        for i, cabal in enumerate(cabal_data[:3]):  # Top 3 cabals
            if i == 0:
                message += f"🥇 #{cabal['rank']} {cabal['name']} - Level {cabal['level']} - {cabal['power']} Power\n"
            elif i == 1:
                message += f"🥈 #{cabal['rank']} {cabal['name']} - Level {cabal['level']} - {cabal['power']} Power\n"
            elif i == 2:
                message += f"🥉 #{cabal['rank']} {cabal['name']} - Level {cabal['level']} - {cabal['power']} Power\n"
        
        # Add hashtags
        message += "\n#ChadBattles #Cabal #WeeklyLeaderboard"
        
        # Post the tweet
        return post_tweet(message)
    except Exception as e:
        logger.error(f"Error sharing weekly leaderboard: {str(e)}")
        return False

def get_game_stats():
    """
    Get interesting game statistics for automated tweets.
    
    Returns:
        dict: Dictionary containing various game statistics
    """
    from app.models.user import User
    from app.models.chad import Chad
    from app.models.waifu import Waifu
    from app.models.battle import Battle
    from app.models.cabal import Cabal
    from app.models.nft import NFT
    from sqlalchemy import func
    
    stats = {}
    
    try:
        # User stats
        stats['user_count'] = User.query.count()
        stats['active_users'] = User.query.filter(
            User.last_login >= datetime.utcnow() - timedelta(days=1)
        ).count()
        
        # Chad stats
        stats['chad_count'] = Chad.query.count()
        average_chad_level = db.session.query(func.avg(Chad.level)).scalar()
        stats['avg_chad_level'] = round(average_chad_level, 1) if average_chad_level else 0
        stats['highest_level_chad'] = Chad.query.order_by(Chad.level.desc()).first()
        
        # Waifu stats
        stats['waifu_count'] = Waifu.query.count()
        
        # Battle stats
        stats['total_battles'] = Battle.query.filter_by(status='completed').count()
        stats['recent_battles'] = Battle.query.filter(
            Battle.status == 'completed',
            Battle.completed_at >= datetime.utcnow() - timedelta(days=1)
        ).count()
        
        # Cabal stats
        stats['cabal_count'] = Cabal.query.count()
        stats['top_cabals'] = Cabal.get_leaderboard(limit=3)
        
        # NFT stats
        if NFT.__table__.exists(db.engine):
            stats['nft_count'] = NFT.query.count()
            stats['recent_nfts'] = NFT.query.filter(
                NFT.created_at >= datetime.utcnow() - timedelta(days=1)
            ).count()
        else:
            stats['nft_count'] = 0
            stats['recent_nfts'] = 0
            
    except Exception as e:
        logger.error(f"Error getting game stats: {str(e)}")
    
    return stats

def generate_automated_tweet():
    """
    Generate an automated tweet with interesting game statistics.
    
    Returns:
        str: The tweet message
    """
    # Get game stats
    stats = get_game_stats()
    
    # Generate a variety of tweet templates
    templates = [
        # General stats
        "🎮 CHAD BATTLES UPDATE 🎮\n\nWe've now got {user_count} users battling it out with {chad_count} Chads and {waifu_count} waifus collected! {recent_battles} battles happened in the last 24hrs. Are you in the action yet?",
        
        # Battle focus
        "⚔️ BATTLE REPORT ⚔️\n\n{recent_battles} battles have raged in the last 24 hours, with a total of {total_battles} battles fought since launch! The Chads are getting stronger, averaging level {avg_chad_level}. How's your battle record looking?",
        
        # Cabal focus
        "🏆 CABAL LEADERBOARD 🏆\n\nThere are now {cabal_count} cabals competing for dominance! Current leaders:\n\n{top_cabals_list}\n\nIs your cabal on the rise?",
        
        # NFT focus (if enabled)
        "💎 NFT UPDATE 💎\n\n{nft_count} total NFTs have been minted so far, with {recent_nfts} new ones in the last 24 hours! Don't miss out on minting your Chad, waifu, or rare item as an NFT!",
        
        # Highest level chad
        "👑 CHAD SPOTLIGHT 👑\n\nThe highest level Chad in the game is now level {highest_chad_level}! Think you can dethrone them? Get grinding, chads!",
        
        # Active users
        "🔥 CHAD BATTLES IS LIT 🔥\n\n{active_users} Chads have been battling in the last 24 hours! The competition is heating up with {recent_battles} recent battles. Don't get left behind!"
    ]
    
    # Filter out templates we can't use (e.g., NFT if count is 0)
    valid_templates = templates.copy()
    if stats.get('nft_count', 0) == 0:
        valid_templates = [t for t in valid_templates if "NFT UPDATE" not in t]
        
    if stats.get('cabal_count', 0) == 0:
        valid_templates = [t for t in valid_templates if "CABAL LEADERBOARD" not in t]
    
    # Choose a random template
    template = random.choice(valid_templates)
    
    # Format top cabals if needed
    top_cabals_list = ""
    if "CABAL LEADERBOARD" in template and stats.get('top_cabals'):
        for i, cabal in enumerate(stats.get('top_cabals', [])[:3]):
            medals = ["🥇", "🥈", "🥉"]
            top_cabals_list += f"{medals[i]} {cabal.name} (Level {cabal.level})\n"
    
    # Format highest level chad if needed
    highest_chad_level = 0
    if stats.get('highest_level_chad'):
        highest_chad_level = stats.get('highest_level_chad').level
    
    # Fill in the template
    message = template.format(
        user_count=stats.get('user_count', 0),
        chad_count=stats.get('chad_count', 0),
        waifu_count=stats.get('waifu_count', 0),
        total_battles=stats.get('total_battles', 0),
        recent_battles=stats.get('recent_battles', 0),
        avg_chad_level=stats.get('avg_chad_level', 0),
        cabal_count=stats.get('cabal_count', 0),
        nft_count=stats.get('nft_count', 0),
        recent_nfts=stats.get('recent_nfts', 0),
        top_cabals_list=top_cabals_list,
        highest_chad_level=highest_chad_level,
        active_users=stats.get('active_users', 0)
    )
    
    return message

def generate_reply_to_stats_tweet(mention):
    """
    Generate a reply to a user who responded to an automated stats tweet.
    Uses Chad's personality to respond to user questions or comments.
    
    Args:
        mention (dict): The Twitter mention data
        
    Returns:
        str: The reply message
    """
    user_screen_name = mention.get('user', {}).get('screen_name', 'user')
    text = mention.get('full_text', mention.get('text', '')).lower()
    
    # Look for keywords to determine the type of reply needed
    
    # Common questions or comments and their responses
    responses = {
        'how do i': [
            f"@{user_screen_name} Just tweet 'MAKE ME A CHAD @RollMasterChad' to get started! Check out the available commands with 'HELP @RollMasterChad'. Simple enough even for a beta to understand!",
            f"@{user_screen_name} Even a virgin NPC could figure it out! Tweet 'MAKE ME A CHAD @RollMasterChad' and let the chadness begin!"
        ],
        'when will': [
            f"@{user_screen_name} Soon™ bro, patience is a Chad virtue. The grindset never stops, and neither does our development.",
            f"@{user_screen_name} When it's ready, king. Quality updates for quality Chads only!"
        ],
        'why is': [
            f"@{user_screen_name} Because that's how sigma grindset works. You wouldn't get it unless you're on that chad wavelength.",
            f"@{user_screen_name} That's just how the Chad hierarchy works. Question the system? That's beta talk."
        ],
        'this is cool': [
            f"@{user_screen_name} Based take, Chad. Keep that energy up!",
            f"@{user_screen_name} Of course it is! Created by Chads, for Chads. No cap."
        ],
        'looks awesome': [
            f"@{user_screen_name} Appreciate the support, king! Your W has been noted in the Chad ledger.",
            f"@{user_screen_name} Real recognizes real. You've got that Chad energy."
        ]
    }
    
    # Default responses if no keywords match
    default_responses = [
        f"@{user_screen_name} That's what a true Chad would say! Keep the sigma grindset going!",
        f"@{user_screen_name} Based take. Join the battle and prove your Chad status!",
        f"@{user_screen_name} Virgin comment vs Chad response. Tweet 'MAKE ME A CHAD @RollMasterChad' to join!",
        f"@{user_screen_name} Nice try, but your Cringe Resistance needs to be higher for that take.",
        f"@{user_screen_name} Real Chads don't ask questions, they just dominate. Join now and show us what you've got!"
    ]
    
    # Check for keywords and select a response
    for keyword, reply_options in responses.items():
        if keyword in text:
            return random.choice(reply_options)
    
    # If no keywords match, use a default response
    return random.choice(default_responses)

def post_automated_stats_tweet():
    """
    Generate and post an automated tweet with game statistics.
    Should be called by a scheduled task.
    
    Returns:
        bool: True if the tweet was posted successfully, False otherwise
    """
    try:
        # Generate tweet content
        message = generate_automated_tweet()
        
        # Post the tweet
        result = post_tweet(message)
        
        if result:
            logger.info("Automated stats tweet posted successfully")
        else:
            logger.error("Failed to post automated stats tweet")
            
        return result
    except Exception as e:
        logger.error(f"Error posting automated stats tweet: {str(e)}")
        return False

def handle_automated_tweet_replies(tweet_id):
    """
    Handle replies to an automated tweet.
    
    Args:
        tweet_id (str): The ID of the automated tweet
        
    Returns:
        int: Number of replies processed
    """
    try:
        api = get_twitter_api()
        if not api:
            return 0
        
        # Get replies to the tweet
        replies = []
        for tweet in tweepy.Cursor(api.search_tweets, 
                                  q=f"to:RollMasterChad", 
                                  since_id=tweet_id,
                                  tweet_mode='extended').items(20):
            # Check if it's a reply to our specific tweet
            if tweet.in_reply_to_status_id_str == tweet_id:
                replies.append(tweet._json)
        
        logger.info(f"Found {len(replies)} replies to automated tweet {tweet_id}")
        
        # Process only a subset of replies to avoid rate limits
        # Prioritize replies with questions or popular replies
        priority_replies = []
        
        for reply in replies:
            text = reply.get('full_text', reply.get('text', '')).lower()
            favorite_count = reply.get('favorite_count', 0)
            
            # Check if it contains a question or has engagement
            has_question = '?' in text
            is_popular = favorite_count >= 3
            
            if has_question or is_popular:
                priority_replies.append(reply)
        
        # Limit to 3 replies to avoid rate limits
        replies_to_process = priority_replies[:3]
        
        # Generate and post replies
        replies_posted = 0
        for reply in replies_to_process:
            reply_text = generate_reply_to_stats_tweet(reply)
            reply_id = reply.get('id_str')
            
            # Post the reply
            if post_reply(reply_text, reply_id):
                replies_posted += 1
                # Sleep to avoid rate limits
                time.sleep(2)
        
        logger.info(f"Responded to {replies_posted} replies to automated tweet {tweet_id}")
        return replies_posted
        
    except Exception as e:
        logger.error(f"Error handling replies to automated tweet: {str(e)}")
        return 0

def generate_promotional_tweet():
    """
    Generate a promotional tweet that tells people how to play the game.
    
    Returns:
        str: The tweet message
    """
    import random
    
    # List of promotional tweet templates
    promo_templates = [
        "🎮 WANNA BE A CHAD? 🎮\n\nTweet 'MAKE ME A CHAD @RollMasterChad' to get started! Your Twitter profile will be transformed into a unique Chad for battle. Collect waifus, join cabals, and dominate! #ChadBattles",
        
        "⚔️ HOW TO START CHAD BATTLES ⚔️\n\n1. Tweet 'MAKE ME A CHAD @RollMasterChad'\n2. Get your character stats based on your Twitter\n3. Challenge others with 'I'm going to CRUSH @opponent! CHALLENGE TO BATTLE @RollMasterChad'\n\nIt's that simple! #GamingOnTwitter",
        
        "👑 BECOME THE ULTIMATE CHAD 👑\n\nJoin thousands of players in Chad Battles!\n\n- Collect rare waifus\n- Form powerful cabals\n- Battle other Chads\n- Mint NFTs\n\nStart by tweeting 'MAKE ME A CHAD @RollMasterChad' #ChadBattles",
        
        "🔥 NEW TO CHAD BATTLES? 🔥\n\nHere's how to start your chad journey:\n\n1️⃣ Tweet 'MAKE ME A CHAD @RollMasterChad'\n2️⃣ Collect waifus & items\n3️⃣ Challenge others to battles\n4️⃣ Join or create a cabal\n\nBecome the ultimate chad! #GamersUnite",
        
        "💪 TIRED OF BEING A BETA? 💪\n\nStart your sigma grindset in #ChadBattles!\n\nTweet 'MAKE ME A CHAD @RollMasterChad' to transform your profile into a powerful Chad! Battle others, collect waifus, and dominate the leaderboards!",
        
        "🏆 CHAD BATTLES COMMANDS 🏆\n\nHere are some basic commands:\n\n'MAKE ME A CHAD @RollMasterChad'\n'CHECK STATS @RollMasterChad'\n'HELP @RollMasterChad'\n\nReady to prove your chad status? #TwitterGaming"
    ]
    
    # Randomly select a template
    template = random.choice(promo_templates)
    
    # Sometimes add donation information (1 in 3 chance)
    if random.randint(1, 3) == 1:
        donation_message = "\n\n💰 Support Chad Battles: Send SOL to CyMubCiSr5iYZR48nJHRhF1dkggN5fbuoRzWrK5pex2a"
        
        # Check if adding this would exceed Twitter's character limit
        if len(template) + len(donation_message) <= 280:
            template += donation_message
    
    return template

def post_promotional_tweet():
    """
    Generate and post a promotional tweet about how to play the game.
    Should be called by a scheduled task.
    
    Returns:
        bool: True if the tweet was posted successfully, False otherwise
    """
    try:
        # Generate tweet content
        message = generate_promotional_tweet()
        
        # Post the tweet
        result = post_tweet(message)
        
        if result:
            logger.info("Promotional tweet posted successfully")
        else:
            logger.error("Failed to post promotional tweet")
            
        return result
    except Exception as e:
        logger.error(f"Error posting promotional tweet: {str(e)}")
        return False 