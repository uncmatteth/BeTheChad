#!/usr/bin/env python
"""
Mock implementation of the scheduler for testing.

This script demonstrates how the scheduler works by using mock tasks
that don't depend on the actual database models.

Usage:
    python tools/test_scheduler_mock.py

Example:
    python tools/test_scheduler_mock.py
"""

import sys
import logging
from datetime import datetime
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def mock_weekly_recap():
    """Mock implementation of the weekly recap task."""
    logger.info("TASK: Running mock weekly recap...")
    logger.info("TASK: Generating leaderboard...")
    logger.info("TASK: Sending to cabal leaders...")
    logger.info("TASK: Weekly recap completed")

def mock_rankings_update():
    """Mock implementation of the rankings update task."""
    logger.info("TASK: Running mock rankings update...")
    logger.info("TASK: Recalculating cabal powers...")
    logger.info("TASK: Updating leaderboard ranks...")
    logger.info("TASK: Rankings update completed")

def init_mock_scheduler():
    """
    Initialize a mock scheduler with short intervals for testing.
    
    Returns:
        BackgroundScheduler: The initialized scheduler
    """
    logger.info("Initializing mock scheduler...")
    
    scheduler = BackgroundScheduler()
    
    # Schedule weekly recap to run every 10 seconds
    scheduler.add_job(
        mock_weekly_recap,
        IntervalTrigger(seconds=10),
        id='mock_weekly_recap',
        name='Mock Weekly Recap',
        replace_existing=True
    )
    
    # Schedule rankings update to run every 5 seconds
    scheduler.add_job(
        mock_rankings_update,
        IntervalTrigger(seconds=5),
        id='mock_rankings_update',
        name='Mock Rankings Update',
        replace_existing=True
    )
    
    # Start the scheduler
    try:
        scheduler.start()
        logger.info("Mock scheduler started successfully")
    except Exception as e:
        logger.error(f"Error starting mock scheduler: {str(e)}")
    
    # Shut down the scheduler when exiting
    atexit.register(lambda: scheduler.shutdown())
    
    return scheduler

def main():
    """Main function to run the mock scheduler."""
    logger.info("Starting mock scheduler test...")
    
    try:
        # Initialize the scheduler
        scheduler = init_mock_scheduler()
        
        # Run for 15 seconds to demonstrate scheduled tasks
        logger.info("Running scheduler for 15 seconds...")
        logger.info("Press Ctrl+C to stop earlier")
        
        try:
            # Wait for 15 seconds or until interrupted
            time.sleep(15)
        except KeyboardInterrupt:
            logger.info("Test interrupted by user")
        
        # Shut down the scheduler
        logger.info("Shutting down scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully")
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 