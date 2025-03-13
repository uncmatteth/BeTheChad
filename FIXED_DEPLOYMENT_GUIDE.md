# Chad Battles: Fixed Deployment Guide

This guide outlines the steps to deploy Chad Battles with the fixes implemented to resolve the dependency issues and model errors.

## Summary of Changes

1. **Fixed Model Classes**
   - Added missing `WaifuItem` and `CharacterItem` classes to `app/models/item.py`
   - Added necessary inheritance structure with polymorphic identity

2. **Dependency Management**
   - Created `requirements_deployment.txt` without problematic Solana packages
   - Updated `render.yaml` and `Dockerfile` to use this file

3. **Feature Flags**
   - Added feature flags in `config.py` to disable blockchain and Twitter bot features
   - Updated environment variable settings in deployment files

4. **Database Initialization**
   - Created `setup_deployment_db.py` for initializing a minimal database in production

5. **Configuration Updates**
   - Updated path references from `run.py:app` to `app:create_app()`
   - Set proper environment variables

## Deployment Options

### Option 1: Deploy to Render using GitHub

1. **Commit all changes**
   ```bash
   git add app/models/item.py config.py render.yaml Dockerfile requirements_deployment.txt setup_deployment_db.py
   git commit -m "Fix deployment issues with models and configuration"
   git push
   ```

2. **Create new Render web service**
   - Log in to Render.com
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select "Use render.yaml from repository" option
   - Click "Create Web Service"

3. **Monitor the deployment**
   - Watch the deployment logs for any errors
   - If successful, you will see "Build successful" and "App is live"

### Option 2: Deploy to Render using Docker

1. **Build the Docker image locally**
   ```bash
   docker build -t chad-battles .
   ```

2. **Test the image locally**
   ```bash
   docker run -p 5000:5000 -e DATABASE_URL=sqlite:///dev.db chad-battles
   ```

3. **Create a new web service on Render**
   - Select "Docker" as the environment
   - Connect to your GitHub repository
   - Leave the build command empty (uses Dockerfile)
   - Add environment variables:
     - `DATABASE_URL`: (your PostgreSQL connection string)
     - `SECRET_KEY`: (a secure random string)
     - `ENABLE_BLOCKCHAIN`: false
     - `ENABLE_TWITTER_BOT`: false

### Option 3: Deploy Static Landing Page First

If you encounter persistent issues, deploy the static landing page first:

1. **Create a new static site on Render**
   - Click "New" → "Static Site"
   - Connect your GitHub repository
   - Set publish directory to `/` (the root)
   - Click "Create Static Site"

2. **Set up custom domain**
   - Go to the "Settings" tab in your Render dashboard
   - Click "Add Custom Domain"
   - Follow the instructions to set up your domain with Render's nameservers

## Database Migrations

If you're using an existing database, you'll need to run migrations:

1. **Initialize migrations (if not already done)**
   ```bash
   flask db init
   ```

2. **Create a migration for the model changes**
   ```bash
   flask db migrate -m "Add WaifuItem and CharacterItem models"
   ```

3. **Apply the migration**
   ```bash
   flask db upgrade
   ```

## Post-Deployment Steps

1. **Verify the application**
   - Check that all pages load correctly
   - Confirm database tables are created properly
   - Test basic functionality

2. **Create an admin user**
   - Use the admin creation function in `setup_deployment_db.py`
   - Or create one manually through the Flask shell

3. **Secure your deployment**
   - Change any default passwords
   - Set up proper HTTPS (done automatically by Render)
   - Consider setting up monitoring

## Troubleshooting

### Database Issues
- **Error**: "Table not found"
  - **Solution**: Ensure migrations have been run properly
  - **Alternative**: Use `db.create_all()` in a Flask shell

### Package Issues
- **Error**: "Cannot import module"
  - **Solution**: Check if all required packages are in `requirements_deployment.txt`
  - **Alternative**: Install missing packages manually on the server

### Model Issues
- **Error**: "Cannot import WaifuItem"
  - **Solution**: Verify that the `WaifuItem` class is correctly defined in `app/models/item.py`
  - **Alternative**: Check that the class is correctly imported in `app/models/__init__.py`

## Re-enabling Features

Once the basic application is running, you can gradually re-enable features:

1. **Twitter Bot**
   - Set `ENABLE_TWITTER_BOT=true` in environment variables
   - Add proper Twitter API credentials
   - Uncomment the Twitter bot cron job in `render.yaml`

2. **Blockchain Features**
   - Set `ENABLE_BLOCKCHAIN=true` in environment variables
   - Add Solana packages to your requirements
   - Configure blockchain environment variables

## Maintaining the Deployment

1. **Regular updates**
   - Push changes to GitHub and Render will auto-deploy
   - Monitor deployment logs for any issues

2. **Database backups**
   - Render provides automatic backups for PostgreSQL databases
   - Consider manual backups for critical data

3. **Monitoring**
   - Set up uptime monitoring
   - Configure error alerts

## Next Steps for Development

1. **Refactor blockchain integration**
   - Make it more modular and optional
   - Better error handling for blockchain operations

2. **Improve testing**
   - Add comprehensive tests for all features
   - Include deployment smoke tests

3. **Documentation**
   - Keep this deployment guide updated
   - Document APIs and internal functionality 