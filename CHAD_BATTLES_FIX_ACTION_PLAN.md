# Chad Battles: Deployment Fix Action Plan

This document provides a step-by-step plan to fix the deployment issues with the Chad Battles application.

## Issue 1: Missing Item Model Classes

### Problem
The application is failing with `ImportError: cannot import name 'WaifuItem' from 'app.models.item'` because the `app/models/item.py` file is missing the `WaifuItem` and `CharacterItem` classes that are imported in `app/models/__init__.py`.

### Solution
1. Edit `app/models/item.py` to add the missing classes:

```python
class WaifuItem(Item):
    """Item specifically for waifus."""
    __mapper_args__ = {
        'polymorphic_identity': 'waifu_item',
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def create(cls, user_id, item_type_id, name=None):
        """Factory method to create a new waifu item."""
        item_type = ItemType.query.get(item_type_id)
        if not item_type:
            return None
            
        item = cls(
            user_id=user_id,
            item_type_id=item_type_id,
            name=name or item_type.name,
            clout_bonus=item_type.base_clout_bonus,
            roast_bonus=item_type.base_roast_bonus,
            cringe_resistance_bonus=item_type.base_cringe_resistance_bonus,
            drip_bonus=item_type.base_drip_bonus
        )
        db.session.add(item)
        db.session.commit()
        return item

class CharacterItem(Item):
    """Item specifically for chad characters."""
    __mapper_args__ = {
        'polymorphic_identity': 'character_item',
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def create(cls, user_id, item_type_id, name=None):
        """Factory method to create a new character item."""
        item_type = ItemType.query.get(item_type_id)
        if not item_type:
            return None
            
        item = cls(
            user_id=user_id,
            item_type_id=item_type_id,
            name=name or item_type.name,
            clout_bonus=item_type.base_clout_bonus,
            roast_bonus=item_type.base_roast_bonus,
            cringe_resistance_bonus=item_type.base_cringe_resistance_bonus,
            drip_bonus=item_type.base_drip_bonus
        )
        db.session.add(item)
        db.session.commit()
        return item
```

2. Also, add a `type` column to the `Item` class to support inheritance:

```python
# Add to the Item class definition
type = db.Column(db.String(50))
__mapper_args__ = {
    'polymorphic_on': type,
    'polymorphic_identity': 'item'
}
```

## Issue 2: Configuration Issues

### Problem
The `render.yaml` and `Dockerfile` are using incorrect paths for the Flask application.

### Solution
1. Update `render.yaml`:
```yaml
# Change
- startCommand: "gunicorn run:app"
# To
- startCommand: "gunicorn 'app:create_app()'"
```

2. Update `Dockerfile`:
```dockerfile
# Change
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
# To
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
```

3. Update `FLASK_APP` environment variable:
```
# Change
FLASK_APP=run.py
# To
FLASK_APP=app
```

## Issue 3: Dependency Conflicts

### Problem
The Solana blockchain packages (`solders==0.14.5`) are causing installation problems in the deployment environment.

### Solution
1. Create a separate deployment-specific requirements file:

```
# requirements_deployment.txt
Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-Migrate==3.1.0
Flask-Login==0.5.0
Flask-WTF==0.15.1
Werkzeug==2.0.2
SQLAlchemy==1.4.25
gunicorn==20.1.0
psycopg2-binary==2.9.1
python-dotenv==0.19.1
requests==2.26.0
Jinja2==3.0.2
Flask-Caching==1.10.1
redis==4.0.2
pytest==6.2.5
# Add other essential packages but exclude Solana/blockchain packages
```

2. Update `render.yaml` to use this file:
```yaml
- buildCommand: "pip install -r requirements_deployment.txt && python setup_minimal.py --non-interactive"
```

## Issue 4: Database Initialization

### Problem
The application needs proper database initialization in the production environment.

### Solution
1. Create a simplified database initialization script:

```python
# setup_deployment_db.py
from app import create_app, db
from app.models import User, Chad, Waifu, Item, Cabal, Battle, MemeElixir, Transaction
import os

app = create_app('production')

with app.app_context():
    # Create tables
    db.create_all()
    
    # Add basic data
    # ... minimal setup code without blockchain dependencies
    
    print("Database initialized successfully!")
```

2. Update the build command in `render.yaml`:
```yaml
- buildCommand: "pip install -r requirements_deployment.txt && python setup_deployment_db.py"
```

## Issue 5: Feature Flags

### Problem
Some features (like blockchain integration) may need to be disabled temporarily.

### Solution
1. Add feature flags in `config.py`:

```python
class Config:
    # ... existing code ...
    ENABLE_BLOCKCHAIN = os.environ.get('ENABLE_BLOCKCHAIN', 'false').lower() == 'true'
    ENABLE_TWITTER_BOT = os.environ.get('ENABLE_TWITTER_BOT', 'false').lower() == 'true'
```

2. Use these flags in the code:

```python
# In blockchain-related code
if current_app.config['ENABLE_BLOCKCHAIN']:
    # Blockchain code here
else:
    # Alternative implementation or just return a placeholder
```

3. Update `render.yaml` to set these flags:
```yaml
envVars:
  - key: ENABLE_BLOCKCHAIN
    value: false
  - key: ENABLE_TWITTER_BOT
    value: false
```

## Deployment Steps

1. **Fix Code Issues**
   - Implement missing model classes
   - Update application configs
   - Add feature flags

2. **Update Deployment Files**
   - Create simplified requirements file
   - Update render.yaml
   - Update Dockerfile

3. **Commit Changes**
   ```
   git add app/models/item.py config.py render.yaml Dockerfile requirements_deployment.txt setup_deployment_db.py
   git commit -m "Fix deployment issues with models and configuration"
   git push
   ```

4. **Deploy to Render**
   - Use the Render dashboard to deploy
   - Monitor logs for errors
   - Gradually enable features once the base app is working

5. **Testing**
   - Test core functionality without blockchain features
   - Verify database migrations work correctly
   - Check application performance

## Fallback Plan

If deployment continues to fail, implement the static landing page approach:

1. Deploy the `index.html` landing page as a static site on Render
2. Set up custom domain
3. Continue troubleshooting the main application 