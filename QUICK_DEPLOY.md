# Quick Deployment Guide for Chad Battles

This guide will help you deploy Chad Battles on Render.com's free tier as quickly as possible.

## 1. Fix Database Relationship Issues

✅ We've already fixed the SQLAlchemy relationship issue between User and Transaction models.

## 2. Push Your Code to GitHub

Make sure your GitHub repository is up to date:

```bash
# From your local repository
git add .
git commit -m "Fix database relationships and prepare for Render deployment"
git push origin main  # or your default branch
```

## 3. Deploy to Render

1. Sign up for a free account at [Render](https://render.com/)
2. From your dashboard, click "New +" and select "Blueprint"
3. Connect your GitHub account when prompted
4. Select your Chad Battles repository
5. Render will automatically detect your `render.yaml` file
6. Click "Apply" to start creating the services

## 4. Set Environment Variables (Very Important!)

Once your web service is created:

1. Click on the web service name in the dashboard
2. Go to the "Environment" tab
3. Add these critical variables:
   - `SECRET_KEY`: Generate a secure random string
   - `TWITTER_API_KEY`: Your Twitter API key
   - `TWITTER_API_SECRET`: Your Twitter API secret
   - `TWITTER_ACCESS_TOKEN`: Your Twitter access token
   - `TWITTER_ACCESS_TOKEN_SECRET`: Your Twitter access token secret
   - `TWITTER_BEARER_TOKEN`: Your Twitter bearer token

## 5. Initialize the Database

After deployment is complete:

1. Click on your web service in the dashboard
2. Go to the "Shell" tab
3. Run these commands:

```bash
flask db init
flask db migrate
flask db upgrade
```

## 6. Verify Deployment

1. Wait for the deployment to complete (check the status in the "Events" tab)
2. Click on the URL at the top of your web service page
3. Your application should now be running!

## Domain Setup (Optional)

1. Purchase your domain (like chadbattles.fun) from any domain registrar
2. In Render dashboard, go to your web service
3. Navigate to "Settings" > "Custom Domain"
4. Follow Render's instructions to set up DNS for your domain

## Need Help?

If you encounter issues:
1. Check the service logs in Render dashboard
2. Make sure all environment variables are set correctly
3. Verify that the database connection is working
4. Check if there are any issues with the Twitter API integration

Remember, your free tier app will spin down after 15 minutes of inactivity and take a few seconds to spin up when accessed again. 