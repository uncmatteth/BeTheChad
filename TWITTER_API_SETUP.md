# Twitter API Setup Guide

## Required URLs for Developer Portal

When setting up your Twitter API credentials in the developer portal, you need to provide the following URLs:

### App Info

- **Callback URL / Redirect URI**: 
  - Production: `https://chadbattles.fun/auth/twitter-callback`
  - Development: `http://localhost:5000/auth/twitter-callback`

### Website URL
- `https://chadbattles.fun`

### Terms of Service URL
- `https://chadbattles.fun/terms`

### Privacy Policy URL
- `https://chadbattles.fun/privacy`

## Organization Information

- **Organization Name**: Chad Battles: A Game on X by Uncle Matt
- **Organization URL**: `https://chadbattles.fun`

## App Permissions

Make sure you enable the following permissions:
- Read and write: Read Posts and profile information
- Read users follows list
- Request email from users

## App Type
- Select "Web App, Automated App or Bot"
- Authentication type: OAuth 2.0

## Environment Variables

Ensure the following environment variables are set in your `.env` file:

```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

For security, never commit these values to your repository.

## Development vs. Production

If you're testing locally, update your `.env` file to use the local callback URL:
```
TWITTER_CALLBACK_URL=http://localhost:5000/auth/twitter-callback
```

For production:
```
TWITTER_CALLBACK_URL=https://chadbattles.fun/auth/twitter-callback
```

## Twitter Bot Naming

Ensure your Twitter bot account (@RollMasterChad) has a display name that includes "bot" to comply with Twitter's requirements for automated accounts. 