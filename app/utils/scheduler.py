"""
Background task scheduler for the application.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import logging

# Create a global scheduler instance
scheduler = BackgroundScheduler()

def init_scheduler():
    """Initialize the background task scheduler."""
    if not scheduler.running:
        try:
            # Start the scheduler
            scheduler.start()
            
            # Register shutdown function
            atexit.register(lambda: scheduler.shutdown())
            
            # Log scheduler start
            logging.info("Background scheduler started")
            
            # Add scheduled tasks here
            # Example: scheduler.add_job(func=task_function, trigger=IntervalTrigger(hours=24), id='daily_task')
            
            return True
        except Exception as e:
            logging.error(f"Error starting scheduler: {e}")
            return False
    return True

def add_scheduled_task(func, interval_seconds, task_id=None):
    """
    Add a task to the scheduler.
    
    Args:
        func: The function to execute
        interval_seconds: Interval in seconds between executions
        task_id: Unique identifier for the task
    
    Returns:
        bool: True if task was added successfully, False otherwise
    """
    try:
        scheduler.add_job(
            func=func,
            trigger=IntervalTrigger(seconds=interval_seconds),
            id=task_id or f"task_{func.__name__}",
            replace_existing=True
        )
        return True
    except Exception as e:
        logging.error(f"Error adding scheduled task: {e}")
        return False 