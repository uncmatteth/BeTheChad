# Chad Battles Twitter Bot

This document provides an overview of the Chad Battles Twitter Bot and its functionality.

## Overview

The Chad Battles Twitter Bot (`@RollMasterChad`) serves three main purposes:

1. **Responding to user commands** - Players can interact with the game directly through Twitter
2. **Posting scheduled game updates** - Sharing game statistics, leaderboards, and other information
3. **Engaging with the community** - Responding to replies on its posts in the style of Roll Master Chad

## Command Functionality

Users can interact with the Chad Battles game directly through Twitter by including specific commands and mentioning `@RollMasterChad`:

| Command | Description |
|---------|-------------|
| `MAKE ME A CHAD @RollMasterChad` | Create a new Chad character based on your Twitter profile |
| `CHALLENGE @username TO BATTLE @RollMasterChad` | Challenge another user to an immediate battle |
| `CHECK STATS @RollMasterChad` | View your character's stats |
| `JOIN CABAL [cabal_name] @RollMasterChad` | Join an existing cabal |
| `CREATE CABAL [cabal_name] @RollMasterChad` | Create a new cabal |
| `HELP @RollMasterChad` | Get a list of available commands |

Additional cabal-related commands:
- `APPOINT @username AS [CLOUT|ROAST|CRINGE|DRIP] OFFICER @RollMasterChad`
- `BATTLE CABAL [cabal_name] @RollMasterChad`
- `VOTE REMOVE CABAL LEADER @RollMasterChad`
- `JOIN NEXT CABAL BATTLE @RollMasterChad`

## Battle System

The battle system is designed for fast-paced gameplay:

1. When a player challenges another player, the battle starts immediately
2. No acceptance is required - battles are simulated automatically
3. Results are posted instantly with statistics about XP and rewards
4. Both players gain XP, but the winner receives more XP and Chadcoin

This design keeps the game moving quickly and ensures players always get immediate feedback when they participate in battles.

## Automated Tweets

The bot automatically posts the following types of tweets:

1. **Game Stats Updates** - Posted twice a week (Monday and Thursday at 5:00 PM UTC)
   - Current user count and active users
   - Number of Chads, waifus, and battles
   - Recent NFT activity
   - Highest level Chad character

2. **Promotional Tweets** - Posted twice a week (Wednesday and Saturday at 3:00 PM UTC)
   - Instructions on how to start playing
   - Basic command information
   - Game features and highlights
   - Occasionally includes donation information

3. **Weekly Cabal Recap** - Posted every Sunday at 9:00 AM UTC
   - Leaderboard of top cabals
   - Recent battle statistics
   - Cabal recruitment information

4. **Personalized Cabal Recaps** - Sent to cabal leaders
   - Current ranking
   - Battle record
   - New members and referrals
   - Tips for improvement

## User Engagement

The bot automatically responds to select replies on its tweets using Roll Master Chad's distinctive personality:

- Prioritizes replies with questions or high engagement
- Responds with helpful information for questions about getting started
- Uses Chad-style language with terms like "sigma," "based," "W," etc.
- Limits responses to avoid rate limits (maximum 3 replies per tweet)
- Only processes tweets from the last 48 hours

## Rate Limit Management

To avoid hitting Twitter API rate limits, the bot:

1. Checks for new mentions every 5 minutes
2. Posts stats tweets only twice a week
3. Processes a maximum of 3 replies per tweet
4. Prioritizes recent and engaging replies
5. Uses sleep intervals between API calls

## Running the Bot

The Twitter bot can be run in several modes:

### Continuous Mode

```bash
python twitter_bot.py
```

This will continuously check for new mentions every 5 minutes (default).

### Single Run Mode

```bash
python twitter_bot.py --once
```

This will check for new mentions once and then exit.

### Manual Stats Tweet

```bash
python twitter_bot.py --stats-tweet
```

This will post a game stats tweet immediately and then exit.

### Manual Promotional Tweet

```bash
python twitter_bot.py --promo-tweet
```

This will post a promotional tweet immediately and then exit.

### Custom Interval

```bash
python twitter_bot.py --interval 600
```

This will check for new mentions every 10 minutes (600 seconds).

## Technical Implementation

The Twitter bot consists of several components:

1. **Main Bot Script** (`twitter_bot.py`) - Monitors mentions and processes commands
2. **Twitter API Utilities** (`app/utils/twitter_api.py`) - Handles Twitter API interactions
3. **Bot Commands** (`app/utils/bot_commands.py`) - Processes user commands
4. **Scheduled Tasks** (`app/utils/scheduled_tasks.py`) - Handles automated tweets
5. **Scheduler** (`app/utils/scheduler.py`) - Schedules automated tasks

## Environment Variables

The following environment variables are required:

```
TWITTER_CONSUMER_KEY=your_twitter_api_key
TWITTER_CONSUMER_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
```

## Donations

The Chad Battles project accepts Solana donations to support server costs and ongoing development:

- **Donation Address**: `CyMubCiSr5iYZR48nJHRhF1dkggN5fbuoRzWrK5pex2a`

Donations help maintain:
- Server hosting
- Twitter bot operation
- Development of new features
- Community management

Promotional tweets will occasionally include the donation address.

## Troubleshooting

### Common Issues

1. **Rate Limit Exceeded**
   - Increase the check interval (`--interval` parameter)
   - Check rate limit status using Twitter API's `/application/rate_limit_status`

2. **Authentication Errors**
   - Verify your Twitter API credentials
   - Ensure your app has the necessary read/write permissions

3. **Tweet IDs Not Being Saved**
   - Check that the database migration for the `tweet_tracker` table has been applied
   - Verify database connection

4. **Mentions Not Being Processed**
   - Check the `last_mention_id.txt` file and ensure it's being updated
   - Test the bot with the `--once` flag and check the logs

## Future Enhancements

Planned enhancements to the Twitter bot include:

1. Image generation for battle results
2. Support for more complex commands
3. Periodic trending topic engagement
4. Integration with other social media platforms
5. Hashtag campaigns for user acquisition 