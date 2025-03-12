#!/usr/bin/env python
"""
Manual test script for scheduled tasks.

This script allows you to manually trigger the scheduled tasks to verify they work correctly.
It should be run from the command line with the appropriate Flask application context.

Usage:
    python tools/test_scheduled_tasks.py [task_name]

Arguments:
    task_name: Optional. The name of the task to run. If not provided, all tasks will be run.
               Valid values: 'recap', 'rankings'

Example:
    python tools/test_scheduled_tasks.py recap
"""

import sys
import os
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the tasks
from app.utils.scheduled_tasks import send_weekly_cabal_recap, update_cabal_rankings
from app import create_app

def run_weekly_recap():
    """Run the weekly cabal recap task."""
    logger.info("Running weekly cabal recap task...")
    start_time = datetime.now()
    
    try:
        result = send_weekly_cabal_recap()
    except Exception as e:
        logger.error(f"Error in weekly recap: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        result = False
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    if result:
        logger.info(f"Weekly cabal recap completed successfully in {duration:.2f} seconds")
    else:
        logger.error(f"Weekly cabal recap failed after {duration:.2f} seconds")
    
    return result

def run_rankings_update():
    """Run the cabal rankings update task."""
    logger.info("Running cabal rankings update task...")
    start_time = datetime.now()
    
    try:
        result = update_cabal_rankings()
    except Exception as e:
        logger.error(f"Error in rankings update: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        result = False
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    if result:
        logger.info(f"Cabal rankings update completed successfully in {duration:.2f} seconds")
    else:
        logger.error(f"Cabal rankings update failed after {duration:.2f} seconds")
    
    return result

def main():
    """Main function to run the specified task(s)."""
    logger.info("Starting scheduled tasks test...")
    
    try:
        # Create the Flask app and push an application context
        app = create_app()
        
        with app.app_context():
            # Check if a specific task was requested
            if len(sys.argv) > 1:
                task_name = sys.argv[1].lower()
                
                if task_name == 'recap':
                    run_weekly_recap()
                elif task_name == 'rankings':
                    run_rankings_update()
                else:
                    logger.error(f"Unknown task: {task_name}")
                    logger.info("Valid tasks: 'recap', 'rankings'")
                    return 1
            else:
                # Run all tasks directly
                logger.info("Running all scheduled tasks...")
                
                recap_result = run_weekly_recap()
                rankings_result = run_rankings_update()
                
                if recap_result and rankings_result:
                    logger.info("All tasks completed successfully")
                else:
                    logger.warning("Some tasks failed")
                    return 1
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 