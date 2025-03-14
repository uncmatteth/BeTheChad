# Setting Up Twitter OAuth for Chad Battles

This guide walks through the process of setting up Twitter OAuth for the Chad Battles application, which is required for user authentication and the Twitter bot functionality.

## Why Twitter OAuth?

Chad Battles uses Twitter (X) for:
1. User authentication
2. Bot commands for in-game actions (battles, character creation, etc.)
3. Automated tweets (leaderboards, promotional content)

## Step 1: Create a Twitter Developer Account

1. Go to [Twitter Developer Platform](https://developer.twitter.com/)
2. Sign in with the Twitter account you want to use for the bot (@RollMasterChad)
3. Apply for a developer account if you don't have one
4. Once approved, create a new Project

## Step 2: Create a Twitter App

1. In your Twitter Developer Portal, go to "Projects & Apps"
2. Click "Create App"
3. Name your app (e.g., "Chad Battles")
4. After creation, you'll get your API keys and tokens

## Step 3: Configure App Permissions

1. Go to your app settings
2. Navigate to the "User authentication settings" section
3. Set up OAuth 2.0 with the following settings:
   - **Type of App**: Web App
   - **Callback URI**: `https://your-app-url.com/auth/twitter-callback` (or `http://localhost:5000/auth/twitter-callback` for local development)
   - **Website URL**: Your app's main URL
   - **Permissions**: Read and Write

## Step 4: Obtain API Keys and Tokens

You'll need the following credentials:

1. **API Key** (Consumer Key)
2. **API Secret** (Consumer Secret)
3. **Access Token**
4. **Access Token Secret**
5. **Bearer Token**

Keep these credentials secure - never commit them to your repository!

## Step 5: Configure Environment Variables

Add these credentials to your environment variables:

```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

### For Local Development:
- Add these to your `.env` file (not committed to Git)

### For Render.com Deployment:
1. In the Render dashboard, go to your service
2. Navigate to the "Environment" tab
3. Add each variable with its corresponding value
4. Click "Save Changes"

## Step 6: Test the Integration

1. Start your application
2. Try to log in with Twitter
3. Verify that the authentication flow works correctly
4. Test the bot commands

## Troubleshooting

### Common Issues:

1. **401 Unauthorized errors**: Check that your API keys and tokens are correct
2. **Callback URL errors**: Ensure the callback URL in your Twitter app settings exactly matches your application's callback URL
3. **Read/write permissions**: Make sure your app has the necessary permissions
4. **Rate limiting**: Twitter API has rate limits that might affect your application

If you're still having issues, check the application logs for detailed error messages.

## Production Considerations

When moving to production:
1. Use a dedicated Twitter developer account
2. Monitor API usage to avoid hitting rate limits
3. Implement proper error handling for API failures
4. Consider implementing a queue system for scheduled tweets to handle API downtime 