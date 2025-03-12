# Scheduled Tasks Documentation

This document provides information about the scheduled tasks implemented for the Cabal feature in the Chad Battles application.

## Overview

The application includes a background scheduler that runs periodic tasks to enhance the Cabal feature. These tasks include:

1. **Weekly Cabal Recap** - Sends a summary of the week's activities to cabal leaders
2. **Daily Cabal Rankings Update** - Updates the power and rank of all cabals

## Task Details

### Weekly Cabal Recap

**Schedule**: Every Sunday at 9:00 AM UTC

**Purpose**: This task generates a weekly recap of cabal activities and shares it with cabal leaders. It also posts the top cabals on the leaderboard to Twitter.

**Functionality**:
- Generates a leaderboard of the top 10 cabals
- Shares the top 3 cabals on Twitter
- For each cabal in the top 10:
  - Calculates battle statistics (wins/losses) for the past week
  - Counts new members and referrals from the past week
  - Sends a personalized recap to the cabal leader via Twitter
  - Includes tips based on the cabal's performance

**Implementation**: `send_weekly_cabal_recap()` in `app/utils/scheduled_tasks.py`

### Daily Cabal Rankings Update

**Schedule**: Every day at 3:00 AM UTC

**Purpose**: This task updates the power and rank of all cabals to ensure the leaderboard is current.

**Functionality**:
- Retrieves all active cabals
- Recalculates the total power of each cabal
- Updates the rank of each cabal on the leaderboard

**Implementation**: `update_cabal_rankings()` in `app/utils/scheduled_tasks.py`

## Twitter Integration

The scheduled tasks use Twitter integration to share information with users. This integration is implemented in `app/utils/twitter_api.py`.

### Features

- **Weekly Leaderboard Tweets**: Posts the top 3 cabals on the leaderboard each week
- **Personalized Recaps**: Sends personalized recaps to cabal leaders
- **Achievement Sharing**: Shares cabal achievements such as level-ups and battle wins

### Configuration

To enable Twitter integration, the following environment variables must be set:

```
TWITTER_CONSUMER_KEY=your_consumer_key
TWITTER_CONSUMER_SECRET=your_consumer_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

These credentials can be obtained by creating a Twitter Developer account and registering an application.

## Scheduler Configuration

The scheduler is configured in `app/utils/scheduler.py` and is initialized when the application starts.

### Integration with Flask

To integrate the scheduler with the Flask application, the following code is added to the application factory function:

```python
with app.app_context():
    # Initialize scheduler for background tasks
    if not app.config.get('TESTING'):
        init_scheduler()
```

This ensures that the scheduler only runs in non-testing environments.

## Testing

The scheduled tasks can be tested using the test cases in `tests/test_scheduled_tasks.py`. These tests use mocking to simulate the behavior of the tasks without actually interacting with external services like Twitter.

## Troubleshooting

If the scheduled tasks are not running as expected, check the following:

1. Ensure the application is running and the scheduler has been initialized
2. Check the logs for any error messages related to the scheduler
3. Verify that the Twitter API credentials are correctly configured
4. For testing purposes, you can modify the CronTrigger in `scheduler.py` to run more frequently

## Future Enhancements

Potential enhancements for the scheduled tasks include:

1. Adding more personalized recommendations based on cabal performance
2. Implementing direct message functionality for more private communications
3. Adding more metrics to the weekly recap, such as member contribution statistics
4. Creating a notification system for important cabal events 