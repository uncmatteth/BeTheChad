# Cabal Feature QA Checklist

## Setup and Prerequisites
- [ ] Environment variables are correctly set (MAX_CABAL_SIZE=69)
- [ ] Database migration for Cabal tables has been applied
- [ ] Test database has sample cabal data for testing
- [ ] User accounts with different roles exist for testing

## Model Testing

### Cabal Model
- [ ] Creation with valid parameters works correctly
- [ ] Invite code is generated automatically
- [ ] Ensure total power is calculated correctly
- [ ] Verify cabal level progression with XP
- [ ] Check rank updates on leaderboard

### Membership
- [ ] Adding members works correctly
- [ ] Removing members works correctly
- [ ] Members can't be in multiple cabals
- [ ] Membership limit (69) is enforced
- [ ] Leader can't be removed via regular removal

### Officers
- [ ] Appointing officers with all role types works
- [ ] Removing officers works correctly
- [ ] Leader can't be an officer
- [ ] Officer stat bonuses are calculated correctly
- [ ] Replacing an officer with a new one works

### Voting
- [ ] Voting to remove leader records votes correctly
- [ ] Leader removal requires 3/4 majority
- [ ] Can't vote twice for leader removal
- [ ] Leader removal assigns new leader correctly
- [ ] Votes are cleared after successful removal

### Battles
- [ ] Battle scheduling works correctly
- [ ] Weekly battle limit (3) is enforced
- [ ] Member daily battle limit (5) is enforced
- [ ] Opting into battles works correctly
- [ ] Battle power calculation is accurate
- [ ] XP and rewards are distributed correctly

## Controller Testing

### Core Routes
- [ ] Index page displays correct cabal info
- [ ] Create cabal form works correctly
- [ ] Joining via invite code works
- [ ] Leaving a cabal works correctly
- [ ] Disbanding a cabal removes all related records

### Member Management
- [ ] Removing members works via controller
- [ ] Promoting members to leader works
- [ ] Appointment of officers works via forms
- [ ] Voting for leader removal works via controller
- [ ] Only leader can access restricted actions

### Battle System
- [ ] Battle scheduling form works correctly
- [ ] Battle opt-in functionality works
- [ ] All battles view shows correct information
- [ ] Leaderboard displays cabals in correct order
- [ ] Battle status updates correctly

## Template Testing

### Core Pages
- [ ] Index page shows all required information
- [ ] Create cabal form has all necessary fields
- [ ] Member list displays correctly
- [ ] Officer section shows roles and bonuses
- [ ] Leader information is clearly displayed

### Battle Pages
- [ ] Schedule battle form has opponent and time fields
- [ ] All battles page shows upcoming and past battles
- [ ] Battle opt-in buttons work correctly
- [ ] Battle countdown displays correctly
- [ ] Leaderboard shows ranks and stats correctly

### UI/UX Testing
- [ ] Mobile layout works on all pages
- [ ] Progress bars display correctly
- [ ] User actions (buttons, forms) are intuitive
- [ ] Error messages are clear and helpful
- [ ] Success messages confirm actions
- [ ] Modals work correctly on all devices
- [ ] Styling is consistent across all pages

## Twitter Bot Command Testing

### Create Cabal
- [ ] `CREATE CABAL name` creates a cabal correctly
- [ ] Proper response is returned
- [ ] Invalid names are handled correctly
- [ ] Users in existing cabals get appropriate error

### Appoint Officer
- [ ] `APPOINT @username AS CLOUT OFFICER` works
- [ ] All officer roles can be assigned
- [ ] Invalid usernames are handled correctly
- [ ] Non-leaders receive appropriate error
- [ ] Non-members can't be appointed

### Schedule Battle
- [ ] `BATTLE CABAL name` schedules battles correctly
- [ ] Invalid cabal names are handled correctly
- [ ] Battle limit is enforced correctly
- [ ] Proper response with battle info is returned

### Vote to Remove Leader
- [ ] `VOTE REMOVE CABAL LEADER` records votes correctly
- [ ] Leaders can't vote against themselves
- [ ] Non-members receive appropriate error
- [ ] Vote confirmation is sent correctly

### Opt Into Battle
- [ ] `JOIN NEXT CABAL BATTLE` opts user into battles correctly
- [ ] Daily battle limit is enforced
- [ ] Non-members receive appropriate error
- [ ] Proper confirmation is returned

## Security Testing

- [ ] CSRF protection is in place for all forms
- [ ] Routes have proper authentication checks
- [ ] Leader-only actions are restricted correctly
- [ ] SQL injection is prevented in all queries
- [ ] XSS vulnerabilities are mitigated
- [ ] Rate limiting is applied to Twitter commands
- [ ] Invite codes are sufficiently random

## Performance Testing

- [ ] Cabal power calculation is efficient with many members
- [ ] Leaderboard sorting is efficient with many cabals
- [ ] Page load times are reasonable on all pages
- [ ] Database queries are optimized
- [ ] Caching is implemented where appropriate

## Edge Case Testing

- [ ] Handling cabals with no members
- [ ] Handling battles with no participants
- [ ] Handling leader leaving/deletion
- [ ] Handling simultaneous votes/actions
- [ ] Handling invalid/malformed Twitter commands
- [ ] Handling database transaction failures
- [ ] Handling time zone differences in battle scheduling

## Scheduled Tasks Testing

- [ ] **Weekly Cabal Recap**
  - [ ] Verify the scheduler initializes correctly when the application starts
  - [ ] Confirm the weekly recap task runs at the scheduled time
  - [ ] Check that the leaderboard is correctly generated and shared on Twitter
  - [ ] Verify personalized recaps are sent to cabal leaders
  - [ ] Ensure the recap includes accurate battle statistics, member counts, and referral counts
  - [ ] Confirm that appropriate tips are included based on cabal performance

- [ ] **Daily Cabal Rankings Update**
  - [ ] Verify the daily rankings update task runs at the scheduled time
  - [ ] Confirm that cabal power is recalculated correctly
  - [ ] Check that cabal ranks are updated appropriately
  - [ ] Ensure database changes are committed successfully

- [ ] **Twitter Integration**
  - [ ] Verify Twitter API credentials are correctly configured
  - [ ] Confirm tweets are posted successfully
  - [ ] Check that tweets respect the character limit
  - [ ] Ensure error handling works correctly when Twitter API is unavailable
  - [ ] Verify the content of leaderboard tweets is formatted correctly
  - [ ] Confirm achievement sharing works for various achievement types

## Final Verification

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All linter warnings are addressed
- [ ] Documentation is complete and accurate
- [ ] Code is reviewed by at least one other developer
- [ ] Manual testing confirms all functionality works
- [ ] Responsive design works on all target devices
- [ ] Performance meets expectations

## Notes

- Record any bugs or issues found during testing
- Document any workarounds or limitations
- Track test coverage metrics
- Note any areas needing improvement in future iterations 