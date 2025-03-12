"""
Scheduler Integration Guide

This file provides instructions on how to integrate the scheduler with your Flask application.
Follow these steps to ensure the scheduler starts when your application initializes.

Integration Steps:
-----------------

1. In your app/__init__.py file, add the following import:
   ```python
   from app.utils.scheduler import init_scheduler
   ```

2. In your create_app function, add the following code before returning the app:
   ```python
   with app.app_context():
       # Initialize scheduler for background tasks
       if not app.config.get('TESTING'):
           init_scheduler()
   ```

3. Make sure you have the APScheduler package installed:
   ```
   pip install apscheduler
   ```

4. Add APScheduler to your requirements.txt file:
   ```
   apscheduler==3.10.1
   ```

Example Integration:
------------------

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from app.utils.scheduler import init_scheduler

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    with app.app_context():
        # Initialize scheduler for background tasks
        if not app.config.get('TESTING'):
            init_scheduler()
    
    return app
```

Testing the Scheduler:
--------------------

To test that the scheduler is working correctly:

1. Start your Flask application
2. Check the logs for the message "Scheduler started successfully"
3. You can temporarily modify the CronTrigger in scheduler.py to run more frequently for testing

Note: The scheduler will not run in testing environments to avoid interference with tests.
""" 