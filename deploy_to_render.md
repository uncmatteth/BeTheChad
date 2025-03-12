# Deploying Chad Battles to Render (Free Tier)

This guide will walk you through deploying the Chad Battles application to Render's free tier platform.

## Prerequisites

1. A GitHub account with your Chad Battles repository
2. A Render.com account (free, no credit card required)

## Deployment Steps

### 1. Push Your Code to GitHub

Make sure your repository contains all necessary files:
- All application code
- requirements.txt
- Procfile
- render.yaml

### 2. Create a New Web Service on Render

1. Log in to your [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" and select "Blueprint" (to use your render.yaml configuration)
3. Connect your GitHub repository
4. Select the repository where Chad Battles is stored
5. Render will detect the render.yaml file and display your services
6. Click "Apply" to create all services defined in the render.yaml

### 3. Configure Environment Variables

In addition to the variables specified in render.yaml, you'll need to set these:
1. From your dashboard, click on the created web service
2. Navigate to "Environment" tab
3. Add the following environment variables:
   - FLASK_APP=run.py
   - FLASK_ENV=production
   - SECRET_KEY (generate a random string)
   - Set up any Twitter API credentials if you're using Twitter integration

### 4. Set Up the Database

The render.yaml file already configures a PostgreSQL database, but you need to initialize it:

1. Once the database is created, go to your web service
2. In the "Shell" tab, run:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

### 5. Test Your Deployment

1. After deployment completes, click the URL of your web service
2. Verify the application is working correctly

## Free Tier Limitations

1. **Spin Down**: Free services will spin down after 15 minutes of inactivity and will spin up when a new request comes in (may take a few seconds)
2. **Database Retention**: Free PostgreSQL databases have a 90-day data retention limit
3. **Compute Hours**: Limited to 750 hours per month across all services
4. **Storage**: Limited to 3GB of storage total

## Custom Domain Setup (Optional)

1. Purchase your domain (like chadbattles.fun) from a domain registrar
2. In your Render dashboard, click on your web service
3. Go to "Settings" and scroll to "Custom Domain"
4. Add your domain and follow Render's instructions to configure DNS settings

## Troubleshooting

If your app isn't deploying correctly:

1. Check the logs in the Render dashboard
2. Verify all environment variables are set correctly
3. Make sure your code runs locally with `gunicorn run:app`
4. If database errors occur, check the connection string in the environment variables

For more detailed information, visit the [Render Documentation](https://render.com/docs). 