# Chad Battles Deployment Checklist

## Files to Verify

- [ ] `app/models/item.py`: Contains the `WaifuItem` and `CharacterItem` classes
- [ ] `config.py`: Contains feature flags for blockchain and Twitter bot
- [ ] `render.yaml`: Updated to use `requirements_deployment.txt` and proper app path
- [ ] `Dockerfile`: Updated to use `requirements_deployment.txt` and setup script
- [ ] `requirements_deployment.txt`: Contains all dependencies except blockchain
- [ ] `setup_deployment_db.py`: Properly initializes the database

## Pre-Deployment Steps

- [ ] Run the app locally with feature flags disabled to test
- [ ] Verify models have proper inheritance and polymorphic identity
- [ ] Check that all imports work without errors
- [ ] Verify database initialization script creates all required tables
- [ ] Test that the app works without blockchain features

## Deployment Steps

- [ ] Commit all changes to GitHub
- [ ] Create new web service on Render
- [ ] Set all required environment variables
- [ ] Enable automatic deployments from GitHub
- [ ] Monitor build and deployment logs

## Post-Deployment Verification

- [ ] Access the deployed application
- [ ] Verify database was created correctly
- [ ] Create test user and verify functionality
- [ ] Check admin features
- [ ] Verify error handling

## Common Issues to Watch For

- [ ] SQLAlchemy model inheritance problems
- [ ] Database connection issues
- [ ] Missing dependencies in requirements file
- [ ] Incorrect import paths
- [ ] File permission issues with static directories

## Backup Plan

- [ ] Have the static landing page ready for immediate deployment
- [ ] Prepare rollback process if deployment fails
- [ ] Have database backup before making any changes

## Next Steps

- [ ] Set up monitoring
- [ ] Configure regular backups
- [ ] Create admin user management tools
- [ ] Plan for gradual re-enabling of features
- [ ] Document any issues encountered for future reference 