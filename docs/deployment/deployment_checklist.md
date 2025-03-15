# Chad Battles - Deployment Checklist

This document provides a comprehensive checklist for deploying the Chad Battles game to production.

## Pre-Deployment Checks

### Code Quality
- [ ] All linting issues resolved
- [ ] Code follows established patterns and conventions
- [ ] No debug print statements or commented-out code
- [ ] All TODOs addressed or documented for future work

### Testing
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing of critical user flows completed
- [ ] Edge cases tested (e.g., high load, invalid inputs)
- [ ] Security testing completed (e.g., CSRF, XSS, SQL injection)
- [ ] Test all templates with empty data to ensure proper error handling

### Database
- [ ] All migrations created and tested
- [ ] Indexes created for performance-critical queries
- [ ] Database backup strategy in place
- [ ] Database scaling strategy documented
- [ ] Check for self-referential foreign keys that need explicit primaryjoin

### Documentation
- [ ] API documentation updated
- [ ] Code documentation (docstrings) complete
- [ ] Deployment guide updated
- [ ] User documentation updated
- [ ] Troubleshooting guide updated with common issues and solutions

## Deployment Steps

### Environment Setup
- [ ] Production environment variables configured
- [ ] Secret management solution in place
- [ ] SSL certificates obtained and configured
- [ ] Domain names configured
- [ ] Nameserver music directory verified (`/home/chadszv/public_html/music`)

### Database Deployment
- [ ] Production database created
- [ ] Run migrations: `flask db upgrade`
- [ ] Verify database schema
- [ ] Seed initial data if needed
- [ ] Test with empty tables to ensure error handling works

### Application Deployment
- [ ] Deploy application code
- [ ] Configure web server (Gunicorn, uWSGI, etc.)
- [ ] Configure reverse proxy (Nginx, Apache, etc.)
- [ ] Set up static file serving
- [ ] Verify music routes are properly configured

### Caching and Background Tasks
- [ ] Redis server configured
- [ ] APScheduler configured for production
- [ ] Verify scheduled tasks are running
- [ ] Configure proper cache timeouts for audio files

### Monitoring and Logging
- [ ] Logging configured
- [ ] Error tracking set up (e.g., Sentry)
- [ ] Performance monitoring in place
- [ ] Alerts configured for critical issues
- [ ] Database error logging implemented

## Post-Deployment Checks

### Functionality Verification
- [ ] User registration and login works
- [ ] Chad creation and customization works
- [ ] Battle system functions correctly
- [ ] Marketplace transactions work
- [ ] Cabal creation and management works
- [ ] Referral system works
- [ ] Twitter integration works
- [ ] Leaderboard displays correctly (even with empty data)
- [ ] Music player functions properly with all supported formats

### Performance Verification
- [ ] Page load times acceptable
- [ ] Database query performance acceptable
- [ ] API response times acceptable
- [ ] Caching working as expected
- [ ] Music streaming performance optimal

### Security Verification
- [ ] CSRF protection working
- [ ] Authentication working correctly
- [ ] Authorization checks in place
- [ ] Rate limiting functioning
- [ ] File type validation working

## Rollback Plan

In case of critical issues, follow these steps to rollback:

1. Identify the issue and determine if rollback is necessary
2. If database schema changes were made:
   - Run `flask db downgrade` to revert to previous schema
3. Revert to previous application code version
4. Restart application servers
5. Verify functionality after rollback
6. Communicate status to stakeholders

## Maintenance Tasks

### Regular Maintenance
- [ ] Database backups scheduled
- [ ] Log rotation configured
- [ ] Monitoring alerts tested
- [ ] SSL certificate renewal process documented
- [ ] Check for unused audio files on server

### Scaling Considerations
- [ ] Horizontal scaling strategy documented
- [ ] Database scaling strategy documented
- [ ] Caching strategy documented
- [ ] Load balancing configuration documented
- [ ] Audio file streaming optimization strategy documented

## Known Issues and Workarounds

- **Referral Model Relationships**: Self-referential foreign keys in the Referral model require explicit primaryjoin conditions.
- **Empty Database Tables**: All templates and routes must handle empty data gracefully with proper error handling.
- **Music File Access**: Always use hardcoded fallbacks for music tracks in case API or filesystem access fails.
- **UTF-8 Encoding**: Handle potential UTF-8 encoding issues in leaderboard and database operations.

## Final Approval

- [ ] Product owner approval
- [ ] Technical lead approval
- [ ] Security team approval
- [ ] Operations team approval

## Deployment Schedule

- Deployment window: [DATE] [TIME] - [DATE] [TIME]
- Expected downtime: [DURATION]
- Team members on call: [NAMES]
- Communication plan: [DETAILS]

---

This checklist should be reviewed and updated before each deployment to ensure all necessary steps are covered. 