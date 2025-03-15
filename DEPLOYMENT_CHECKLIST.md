# Chad Battles Deployment Checklist

## Files to Verify

- [x] `app/models/item.py`: Contains the `WaifuItem` and `CharacterItem` classes
- [x] `config.py`: Contains feature flags for blockchain and Twitter bot
- [x] `render.yaml`: Updated to use `requirements_deployment.txt` and proper app path
- [x] `Dockerfile`: Updated to use `requirements_deployment.txt` and setup script
- [x] `requirements_deployment.txt`: Contains all dependencies except blockchain
- [x] `setup_deployment_db.py`: Properly initializes the database

## Pre-Deployment Steps

- [x] Run the app locally with feature flags disabled to test
- [x] Verify models have proper inheritance and polymorphic identity
- [x] Check that all imports work without errors
- [x] Verify database initialization script creates all required tables
- [x] Test that the app works without blockchain features

## Deployment Steps

- [x] Commit all changes to GitHub
- [x] Create new web service on Render
- [x] Set all required environment variables
- [x] Enable automatic deployments from GitHub
- [x] Monitor build and deployment logs

## Post-Deployment Verification

- [x] Access the deployed application
- [ ] Verify database was created correctly
- [x] Create test user and verify functionality
- [ ] Check admin features
- [x] Verify error handling

## Current Issues (Last Updated: March 14, 2025)

### Database Issues
- [x] **Critical**: Database switches between SQLite and PostgreSQL during different operations
- [ ] Some tables not being created in PostgreSQL (users, cabals)
- [x] Database migration script not applying correctly to PostgreSQL
- [x] Migrations are being applied to SQLite temp.db but not PostgreSQL

### Template Issues
- [x] Missing templates: 
  - [x] chad/index.html
  - [x] base.html
  - [x] wallet/connect.html

### Feature Issues
- [x] Music player doesn't find music files
  - [x] Fixed: Updated routes to use `/home/chadszv/public_html/music` on the hosting server
  - [x] Added fallback to `app/static/music` for local development
- [ ] Twitter OAuth callback URL not approved for the application
- [ ] Battle feature showing errors (missing target_id attribute)
- [ ] Waifu module errors when trying to display user's waifus
- [ ] Cabal feature errors due to missing tables and attributes

### Code Issues
- [ ] Model relationship issues:
  - [ ] `InstrumentedList` object has no attribute 'all'
  - [ ] `Battle` has no attribute 'target_id'
  - [ ] `Cabal` has no attribute 'total_power'
- [ ] Health check endpoint rate limit being exceeded

## Next Steps Priority List

1. Fix database configuration to ensure:
   - [x] PostgreSQL is used consistently throughout the application
   - [x] All migrations are applied to PostgreSQL, not SQLite
   - [ ] All tables are created properly in the PostgreSQL database

2. Fix template issues:
   - [x] Ensure all required templates are present and accessible

3. Fix music player:
   - [x] Update music routes to use existing audio files on hosting server (`/home/chadszv/public_html/music`)
   - [x] Maintain fallback to `app/static/music` for local development
   - [x] Update paths and references to properly access the music files

4. Fix Twitter OAuth:
   - [ ] Configure proper callback URL in Twitter developer dashboard
   - [ ] Update app configuration with correct Twitter API credentials

5. Fix model relationship issues:
   - [ ] Update models to fix attribute and method errors
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
- [ ] Document any issues encountered for future reference 