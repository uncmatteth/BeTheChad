# Chad Battles Deployment Checklist

## Files to Verify

- [x] `app/models/item.py`: Contains the `WaifuItem` and `CharacterItem` classes
- [x] `config.py`: Contains feature flags for blockchain and Twitter bot
- [x] `render.yaml`: Updated to use `requirements_deployment.txt` and proper app path
- [x] `Dockerfile`: Updated to use `requirements_deployment.txt` and setup script
- [x] `requirements_deployment.txt`: Contains all dependencies except blockchain
- [x] `setup_deployment_db.py`: Properly initializes the database
- [x] `app/routes/auth.py`: Contains authentication routes
- [x] `app/routes/main.py`: Contains main application routes with robust error handling for leaderboard
- [x] `app/models/battle.py`: Contains Battle model with get_leaderboard method
- [x] `app/models/cabal.py`: Contains Cabal model with get_top_cabals method
- [x] `app/models/waifu.py`: Contains Waifu model with get_collector_stats method
- [x] `app/models/referral.py`: Contains Referral model with explicit primaryjoin relationships

## Pre-Deployment Steps

- [x] Run the app locally with feature flags disabled to test
- [x] Verify models have proper inheritance and polymorphic identity
- [x] Check that all imports work without errors
- [x] Verify database initialization script creates all required tables
- [x] Test that the app works without blockchain features
- [x] Verify leaderboard works with empty database tables

## Deployment Steps

- [x] Commit all changes to GitHub
- [x] Create new web service on Render
- [x] Set all required environment variables
- [x] Enable automatic deployments from GitHub
- [x] Monitor build and deployment logs

## Post-Deployment Verification

- [x] Access the deployed application
- [x] Verify database was created correctly
- [x] Create test user and verify functionality
- [x] Check admin features
- [x] Verify error handling

## Current Issues (Last Updated: March 18, 2025)

### Database Issues
- [x] **Critical**: Database switches between SQLite and PostgreSQL during different operations
- [ ] Some tables not being created in PostgreSQL (users, cabals)
- [x] Database migration script not applying correctly to PostgreSQL
- [x] Migrations are being applied to SQLite temp.db but not PostgreSQL
- [x] Referral model foreign key relationship fixed with explicit primaryjoin

### Template Issues
- [x] Missing templates: 
  - [x] chad/index.html
  - [x] base.html
  - [x] wallet/connect.html
  - [x] leaderboard.html (added with robust error handling)

### Feature Issues
- [x] Music player doesn't find music files
  - [x] Fixed: Updated routes to use `/home/chadszv/public_html/music` on the hosting server
  - [x] Added fallback to hardcoded tracks if API fails
  - [x] Support for additional audio formats (.wav, .ogg)
- [x] Twitter OAuth callback URL not approved for the application
  - [x] Fixed: Added environment-aware callback URLs
  - [x] Updated Twitter developer dashboard configuration
- [x] Battle feature showing errors (missing target_id attribute)
  - [x] Fixed: Added target_id attribute to Battle model
- [x] Leaderboard displaying errors when database is empty
  - [x] Fixed: Added robust error handling and fallback to empty tables
- [ ] Waifu module errors when trying to display user's waifus
- [x] Cabal feature errors due to missing tables and attributes
  - [x] Fixed: Added total_power attribute to Cabal model

### Code Issues
- [x] Model relationship issues:
  - [x] `InstrumentedList` object has no attribute 'all'
  - [x] `Battle` has no attribute 'target_id'
  - [x] `Cabal` has no attribute 'total_power'
  - [x] Referral model self-referential foreign key fixed with explicit primaryjoin
- [ ] Health check endpoint rate limit being exceeded

### Route Structure Issues
- [x] Missing route files in app/routes directory
  - [x] Fixed: Created auth.py and main.py in app/routes
  - [x] Updated app/__init__.py to use new route structure
  - [x] Added robust error handling to leaderboard route

## Next Steps Priority List

1. Fix database configuration to ensure:
   - [x] PostgreSQL is used consistently throughout the application
   - [x] All migrations are applied to PostgreSQL, not SQLite
   - [ ] All tables are created properly in the PostgreSQL database

2. Fix template issues:
   - [x] Ensure all required templates are present and accessible
   - [x] Add robust error handling to all templates

3. Fix music player:
   - [x] Update music routes to use existing audio files on hosting server (`/home/chadszv/public_html/music`)
   - [x] Add fallback to hardcoded tracks if API fails
   - [x] Support additional audio formats (.wav, .ogg)
   - [x] Update paths and references to properly access the music files

4. Fix Twitter OAuth:
   - [x] Configure proper callback URL in Twitter developer dashboard
   - [x] Update app configuration with correct Twitter API credentials
   - [x] Implement environment-specific callback URLs

5. Fix model relationship issues:
   - [x] Update models to fix attribute and method errors
   - [x] Fix Referral model with explicit primaryjoin relationships
   - [ ] Create missing tables and attributes

## Backup Plan

- [x] Have the static landing page ready for immediate deployment
- [x] Prepare rollback process if deployment fails
- [x] Have database backup before making any changes

## Further Development Tasks

- [ ] Set up monitoring
- [ ] Configure regular backups
- [ ] Create admin user management tools
- [ ] Plan for gradual re-enabling of features
- [x] Document any issues encountered for future reference

## Deployment Troubleshooting

If deployment fails:
1. Check Render logs for specific error messages
2. Verify all required route files exist in app/routes directory
3. Ensure models have all attributes referenced in controllers
4. Check for missing Python modules in requirements_deployment.txt
5. Verify database connection string is correctly formatted
6. Clear build cache on Render if necessary 
7. Check for self-referential foreign keys that need explicit primaryjoin 