#!/usr/bin/env python3
"""
Chad Battles Twitter Bot

This script monitors the @RollMasterChad Twitter/X account for mentions and processes commands.
It should be run as a scheduled task (e.g., every 5 minutes) to check for new mentions.
It can also be used to manually trigger game stats tweets.
"""

import os
import sys
import time
import logging
import argparse
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("chad_bot")

# Add the project directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.utils.twitter_api import monitor_mentions
from app.utils.bot_commands import handle_mention
from app.models.user import User
from app.utils.scheduled_tasks import post_game_stats_update, post_promotional_tweet

def process_mentions(since_id=None):
    """Process mentions from Twitter/X"""
    logger.info(f"Checking for mentions since ID: {since_id}")
    
    # Get mentions from Twitter API
    mentions = monitor_mentions(since_id)
    
    if not mentions:
        logger.info("No new mentions found")
        return since_id
    
    logger.info(f"Found {len(mentions)} new mentions")
    
    # Sort mentions by ID (chronological order)
    mentions.sort(key=lambda x: int(x.get('id_str', '0')))
    
    # Process each mention
    for mention in mentions:
        tweet_id = mention.get('id_str')
        user_screen_name = mention.get('user', {}).get('screen_name')
        
        logger.info(f"Processing mention {tweet_id} from @{user_screen_name}")
        
        # Handle the mention
        try:
            handle_mention(mention)
        except Exception as e:
            logger.error(f"Error handling mention {tweet_id}: {str(e)}")
    
    # Return the highest ID for next time
    return mentions[-1].get('id_str')

def save_since_id(since_id):
    """Save the since_id to a file"""
    with open("last_mention_id.txt", "w") as f:
        f.write(since_id)

def load_since_id():
    """Load the since_id from a file"""
    try:
        with open("last_mention_id.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def main():
    """Main function to run the bot"""
    parser = argparse.ArgumentParser(description="Chad Battles Twitter Bot")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--interval", type=int, default=300, help="Check interval in seconds (default: 300)")
    parser.add_argument("--stats-tweet", action="store_true", help="Post a game stats tweet and exit")
    parser.add_argument("--promo-tweet", action="store_true", help="Post a promotional tweet and exit")
    args = parser.parse_args()
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Check if database needs initialization
        try:
            user_count = User.query.count()
            logger.info(f"Database connected. {user_count} users found.")
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            logger.info("Make sure to run database migrations first.")
            return
            
        # Check if the user wants to post a stats tweet
        if args.stats_tweet:
            logger.info("Posting a game stats tweet...")
            success = post_game_stats_update()
            if success:
                logger.info("Game stats tweet posted successfully!")
            else:
                logger.error("Failed to post game stats tweet.")
            return
            
        # Check if the user wants to post a promotional tweet
        if args.promo_tweet:
            logger.info("Posting a promotional tweet...")
            success = post_promotional_tweet()
            if success:
                logger.info("Promotional tweet posted successfully!")
            else:
                logger.error("Failed to post promotional tweet.")
            return
        
        # Load the last processed mention ID
        since_id = load_since_id()
        
        if args.once:
            # Run once
            new_since_id = process_mentions(since_id)
            if new_since_id and new_since_id != since_id:
                save_since_id(new_since_id)
        else:
            # Run continuously
            logger.info(f"Starting bot loop. Checking every {args.interval} seconds.")
            
            try:
                while True:
                    new_since_id = process_mentions(since_id)
                    if new_since_id and new_since_id != since_id:
                        since_id = new_since_id
                        save_since_id(since_id)
                    
                    logger.info(f"Sleeping for {args.interval} seconds...")
                    time.sleep(args.interval)
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                raise

if __name__ == "__main__":
    main() 