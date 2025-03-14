# Twitter OAuth Setup for Chad Battles

This document provides step-by-step instructions for setting up Twitter OAuth for the Chad Battles application.

## Prerequisites

1. A Twitter Developer account (apply at [developer.twitter.com](https://developer.twitter.com/) if you don't have one)
2. A Twitter Developer App created for Chad Battles

## Setting Up Your Twitter Developer App

1. Log in to the [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Navigate to your "Projects & Apps" > Select your Chad Battles app
3. Go to the "Settings" > "Edit" section
4. Under "App permissions", ensure "Read" is selected at minimum
5. Under "Authentication settings":
   - Enable OAuth 1.0a
   - Set "App type" to "Web App"
   - Set Website URL to your main site URL (e.g., https://chadbattles.fun)

## Configuring Callback URLs

This is critical to make Twitter login work! You must add all possible callback URLs to your app:

1. In your Twitter Developer Portal > App Settings > Authentication settings
2. Add the following callback URLs:
   - `https://chadbattles.fun/auth/twitter-callback`
   - `https://chad-battles-grdu.onrender.com/auth/twitter-callback`
   - Any local development URLs (e.g., `http://localhost:5000/auth/twitter-callback`)
3. Save your settings

## Environment Variables

The application needs the following environment variables to use Twitter OAuth:

```
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_OAUTH_CLIENT_ID=your_oauth2_client_id_here
TWITTER_OAUTH_CLIENT_SECRET=your_oauth2_client_secret_here
```

### Setting These Variables

#### For Local Development

Add these to your `.env` file (which should never be committed to Git).

#### For Deployment on Render

Add these in the Render Dashboard:
1. Navigate to your service
2. Click "Environment"
3. Add each key-value pair
4. Click "Save Changes"
5. Redeploy your application

## Testing the Setup

1. Visit your site (https://chadbattles.fun)
2. Click "Login with X"
3. You should be redirected to Twitter to authorize the app
4. After authorization, you should be redirected back to the site and logged in

## Troubleshooting

If you encounter the error "Callback URL not approved for this client application", it means the callback URL being used is not in the list of approved callback URLs in your Twitter Developer App settings. Make sure to add all possible callback URLs as mentioned above.

For any other issues, check the application logs for detailed error messages. 