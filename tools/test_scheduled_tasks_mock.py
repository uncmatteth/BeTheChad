#!/usr/bin/env python
"""
Mock implementation of scheduled tasks for testing.

This script provides a mock implementation of the scheduled tasks
without depending on the actual database models.

Usage:
    python tools/test_scheduled_tasks_mock.py [task_name]

Arguments:
    task_name: Optional. The name of the task to run. If not provided, all tasks will be run.
               Valid values: 'recap', 'rankings'

Example:
    python tools/test_scheduled_tasks_mock.py recap
"""

import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def mock_weekly_cabal_recap():
    """
    Mock implementation of the weekly cabal recap task.
    
    Returns:
        bool: True to indicate success
    """
    logger.info("Starting mock weekly cabal recap...")
    
    # Simulate generating leaderboard data
    mock_cabals = [
        {'name': 'Alpha Squad', 'level': 10, 'power': 5000, 'rank': 1},
        {'name': 'Beta Brigade', 'level': 8, 'power': 4200, 'rank': 2},
        {'name': 'Gamma Gang', 'level': 7, 'power': 3800, 'rank': 3}
    ]
    
    # Log the mock leaderboard
    logger.info("Generated mock leaderboard:")
    for i, cabal in enumerate(mock_cabals):
        logger.info(f"  #{i+1}: {cabal['name']} (Level {cabal['level']}, Power {cabal['power']})")
    
    # Simulate sharing leaderboard on Twitter
    logger.info("Simulating Twitter share of leaderboard...")
    logger.info("Tweet would contain: 'Chad Battles Weekly Cabal Leaderboard'")
    
    # Simulate processing cabals and sending recaps
    logger.info("Simulating sending recaps to cabal leaders...")
    for cabal in mock_cabals:
        logger.info(f"  Sending recap to leader of {cabal['name']}...")
        logger.info(f"  Recap would include: rank #{cabal['rank']}, level {cabal['level']}, power {cabal['power']}")
    
    logger.info("Mock weekly cabal recap completed successfully")
    return True

def mock_update_cabal_rankings():
    """
    Mock implementation of the cabal rankings update task.
    
    Returns:
        bool: True to indicate success
    """
    logger.info("Starting mock cabal rankings update...")
    
    # Simulate retrieving cabals
    mock_cabals = [
        {'name': 'Alpha Squad', 'members': 25, 'officers': 4},
        {'name': 'Beta Brigade', 'members': 18, 'officers': 3},
        {'name': 'Gamma Gang', 'members': 15, 'officers': 2},
        {'name': 'Delta Force', 'members': 10, 'officers': 1}
    ]
    
    # Simulate recalculating power and updating ranks
    logger.info(f"Recalculating power and ranks for {len(mock_cabals)} cabals...")
    for i, cabal in enumerate(mock_cabals):
        # Calculate mock power based on members and officers
        power = cabal['members'] * 100 + cabal['officers'] * 500
        logger.info(f"  {cabal['name']}: {cabal['members']} members, {cabal['officers']} officers = {power} power (Rank #{i+1})")
    
    logger.info("Mock cabal rankings update completed successfully")
    return True

def main():
    """Main function to run the specified task(s)."""
    logger.info("Starting mock scheduled tasks test...")
    
    try:
        # Check if a specific task was requested
        if len(sys.argv) > 1:
            task_name = sys.argv[1].lower()
            
            if task_name == 'recap':
                mock_weekly_cabal_recap()
            elif task_name == 'rankings':
                mock_update_cabal_rankings()
            else:
                logger.error(f"Unknown task: {task_name}")
                logger.info("Valid tasks: 'recap', 'rankings'")
                return 1
        else:
            # Run all tasks
            logger.info("Running all mock scheduled tasks...")
            
            recap_result = mock_weekly_cabal_recap()
            rankings_result = mock_update_cabal_rankings()
            
            if recap_result and rankings_result:
                logger.info("All mock tasks completed successfully")
            else:
                logger.warning("Some mock tasks failed")
                return 1
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 