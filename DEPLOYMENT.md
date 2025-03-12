# Deploying Chad Battles

This document provides instructions for deploying the Chad Battles application to Render.com.

## Prerequisites

1. **Twitter Developer Account**
   - Create a Twitter Developer account at [developer.twitter.com](https://developer.twitter.com/)
   - Create a project and app
   - Set app permissions to "Read and Write"
   - Generate API keys and tokens

2. **GitHub Account**
   - Create a GitHub account at [github.com](https://github.com/)
   - Create a new repository
   - Push your code to the repository

3. **Render Account**
   - Create a Render account at [render.com](https://render.com/)
   - Connect your GitHub account

## Deployment Steps

### 1. Deploy to Render using the Blueprint

The easiest way to deploy is using the Render Blueprint:

1. Fork this repository to your GitHub account
2. Log in to your Render account
3. Click on the "New" button and select "Blueprint"
4. Connect your GitHub account and select your forked repository
5. Render will automatically create all the services defined in the `render.yaml` file
6. Add your Twitter API credentials in the environment variables

### 2. Manual Deployment

If you prefer to deploy manually:

#### Create a PostgreSQL Database

1. In Render dashboard, go to "New" → "PostgreSQL"
2. Name it "chad-battles-db"
3. Use the free plan
4. Create the database and note the connection details

#### Deploy the Web Service

1. In Render dashboard, go to "New" → "Web Service"
2. Connect your GitHub repository
3. Name it "chad-battles"
4. Set the environment to "Python"
5. Set the build command: `pip install -r requirements.txt && flask db upgrade`
6. Set the start command: `gunicorn run:app`
7. Add environment variables:
   - `FLASK_APP`: run.py
   - `FLASK_ENV`: production
   - `SECRET_KEY`: (generate a random string)
   - `DATABASE_URL`: (from your PostgreSQL database)
   - `TWITTER_API_KEY`: (your Twitter API key)
   - `TWITTER_API_SECRET`: (your Twitter API secret)
   - `TWITTER_ACCESS_TOKEN`: (your Twitter access token)
   - `TWITTER_ACCESS_TOKEN_SECRET`: (your Twitter access token secret)
   - `TWITTER_BEARER_TOKEN`: (your Twitter bearer token)
8. Deploy the service

#### Set Up the Twitter Bot Cron Job

1. In Render dashboard, go to "New" → "Cron Job"
2. Connect your GitHub repository
3. Name it "twitter-bot"
4. Set the schedule to `*/5 * * * *` (every 5 minutes)
5. Set the build command: `pip install -r requirements.txt`
6. Set the start command: `python twitter_bot.py`
7. Add the same environment variables as the web service
8. Create the cron job

## Troubleshooting

If you encounter any issues during deployment:

1. **Database Migration Errors**
   - Check the build logs for specific error messages
   - You may need to manually run migrations

2. **Twitter API Errors**
   - Verify your API credentials are correct
   - Check that your Twitter Developer account has the necessary permissions

3. **Application Errors**
   - Check the logs in the Render dashboard
   - You may need to adjust environment variables or configuration

## Updating the Application

To update the deployed application:

1. Push changes to your GitHub repository
2. Render will automatically detect the changes and redeploy

## Monitoring

Monitor your application using:

1. Render's built-in logs and metrics
2. Set up alerts for service outages
3. Regularly check the Twitter bot's functionality 