# Chad Battles - Cabal Feature Finalization

This document provides comprehensive documentation for the finalized Cabal feature in the Chad Battles game.

## Overview

The Cabal feature allows players to form groups and compete against other cabals in battles, earn rewards, and climb the leaderboard. The feature includes group management, officer roles, battle scheduling, and analytics.

## Features

### Core Functionality
- **Cabal Creation and Management**: Players can create cabals, invite members, and manage their cabals.
- **Leadership and Officers**: Each cabal has a leader and can appoint officers to specialized roles.
- **Battle System**: Cabals can schedule battles against other cabals and earn rewards.
- **Leaderboard**: Cabals are ranked based on their power and battle performance.
- **Referral System**: Players can earn rewards by referring new members to their cabals.

### Enhanced Features
- **Analytics Dashboard**: Track cabal performance over time with visualizations.
- **Weekly Recaps**: Automated weekly recap emails and tweets for cabal leaders.
- **Scheduled Tasks**: Background tasks keep rankings updated and send notifications.
- **Caching System**: Performance optimizations for frequently accessed data.

## Technical Implementation

### Database Models

#### Core Models
- **Cabal**: Main model representing a cabal with properties like name, description, power, etc.
- **CabalMember**: Represents a player's membership in a cabal.
- **CabalOfficerRole**: Represents officer roles within a cabal.
- **CabalVote**: Tracks votes for cabal leadership changes.
- **CabalBattle**: Stores information about battles between cabals.

#### Enhanced Models
- **Referral**: Tracks member referrals and associated bonuses.
- **CabalAnalytics**: Records historical metrics for cabals.

### Controllers

- **CabalController**: Handles core cabal operations like creation, joining, leaving, etc.
- **CabalBattleController**: Manages battle scheduling, participation, and results.
- **CabalAnalyticsController**: Provides analytics dashboards and data endpoints.

### Scheduled Tasks

- **Weekly Recap**: Sends weekly summaries to cabal leaders.
- **Rankings Update**: Recalculates cabal power and updates rankings daily.
- **Analytics Recording**: Creates daily snapshots of cabal metrics.

### Optimization Techniques

- **Database Indexes**: Added indexes to improve query performance.
- **Caching**: Implemented caching for leaderboard and cabal data.
- **Batch Processing**: Background tasks handle intensive operations.

## Configuration

### Environment Variables

```
# Twitter API credentials for scheduled tasks
TWITTER_CONSUMER_KEY=your_consumer_key
TWITTER_CONSUMER_SECRET=your_consumer_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret

# Caching configuration
ENABLE_CACHING=true
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://localhost:6379/0
```

### Scheduler Configuration

The scheduler is configured to run the following tasks:
- Weekly recap: Sundays at 9:00 AM UTC
- Rankings update: Daily at 3:00 AM UTC

## Deployment Considerations

### Database Migrations

Run the following migrations to update the database schema:
```
flask db upgrade
```

### Caching

The application uses Redis for caching. Make sure Redis is installed and running:
```
# Ubuntu/Debian
sudo apt-get install redis-server

# CentOS/RHEL
sudo yum install redis

# MacOS
brew install redis
```

### Background Tasks

The scheduler uses APScheduler to run background tasks. Make sure the application stays running to execute these tasks.

## Testing

### Unit Tests

- `tests/test_cabal_model.py`: Tests for the Cabal model.
- `tests/test_cabal_routes.py`: Tests for the Cabal controller routes.
- `tests/test_scheduled_tasks.py`: Tests for the scheduled tasks.

### Manual Testing

- `tools/test_scheduled_tasks.py`: A script to manually test the scheduled tasks.
- `tools/test_scheduler_mock.py`: A script to test the scheduler with mock tasks.

## Security Considerations

- **CSRF Protection**: All forms include CSRF tokens.
- **Permission System**: Role-based access control for cabal features.
- **Input Validation**: All user input is validated and sanitized.
- **Rate Limiting**: API endpoints have rate limiting to prevent abuse.

## Performance Optimizations

- **Efficient Queries**: Optimized database queries using indexes.
- **Caching**: Frequently accessed data is cached to reduce database load.
- **Asynchronous Processing**: Heavy operations are handled in background jobs.

## Maintenance and Monitoring

- **Analytics**: Track cabal metrics over time to identify trends.
- **Error Logging**: Comprehensive error logging for troubleshooting.
- **Automated Tests**: Regular test execution to catch regressions.

## Conclusion

The Cabal feature is now fully implemented with robust functionality, optimization, and testing. The feature provides an engaging social aspect to the Chad Battles game, allowing players to form communities and compete together.

With the addition of analytics, scheduled tasks, and performance optimizations, the feature is now complete and ready for production use. The documentation, testing, and code quality ensure long-term maintainability and provide a solid foundation for future enhancements. 