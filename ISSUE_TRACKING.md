# Chad Battles Issue Tracking

This document provides a detailed breakdown of all known issues in the Chad Battles application as of March 14, 2025.

## Database Issues

| Issue | Description | Status | Priority |
|-------|-------------|--------|----------|
| SQLite/PostgreSQL inconsistency | Application switches between databases during operations | 🔴 Active | Critical |
| Missing tables in PostgreSQL | Some tables not being created in PostgreSQL | 🔴 Active | Critical |
| Migration script failures | Migration scripts not applying correctly to PostgreSQL | 🔴 Active | Critical |
| Foreign key constraints | Foreign key constraints causing issues during table creation | 🟢 Resolved | High |
| Missing user fields | User model missing required fields in database | 🟡 In Progress | High |

## Template Issues

| Issue | Description | Status | Priority |
|-------|-------------|--------|----------|
| Missing `chad/index.html` | Template needed for Chad page | 🔴 Active | High |
| Missing `base.html` | Base template not found | 🔴 Active | Critical |
| Missing `wallet/connect.html` | Template for wallet connection not found | 🔴 Active | High |
| Template inheritance issues | Templates not inheriting correctly | 🔴 Active | Medium |

## Feature Issues

### Music Player

| Issue | Description | Status | Priority |
|-------|-------------|--------|----------|
| Missing music directory | `/public_html/music` not found | 🔴 Active | Medium |
| No music files available | Player shows error about missing files | 🔴 Active | Medium |
| Music route returning empty array | `/music/tracks` returns empty list | 🟡 In Progress | Medium |

### Twitter Integration

| Issue | Description | Status | Priority |
|-------|-------------|--------|----------|
| OAuth callback URL | "Callback URL not approved for this client application" | 🔴 Active | Medium |
| Twitter API credentials | May need updating in environment variables | 🔴 Active | Medium |

### Battle System

| Issue | Description | Status | Priority |
|-------|-------------|--------|----------|
| Missing `target_id` attribute | Error: "Battle has no attribute 'target_id'" | 🔴 Active | High |
| Battle history errors | Loading user battle data fails | 🔴 Active | Medium |

### Waifu System

| Issue | Description | Status | Priority |
|-------|-------------|--------|----------|
| Relationship method errors | "'InstrumentedList' object has no attribute 'all'" | 🔴 Active | Medium |
| Waifu page loading failure | Page fails to load completely | 🔴 Active | Medium |

### Cabal System

| Issue | Description | Status | Priority |
|-------|-------------|--------|----------|
| Missing cabals table | "no such table: cabals" | 🔴 Active | Medium |
| Missing attribute | "Cabal has no attribute 'total_power'" | 🔴 Active | Medium |
| Cabal creation failure | Cannot create new cabals | 🔴 Active | Low |

### Leaderboard

| Issue | Description | Status | Priority |
|-------|-------------|--------|----------|
| Cabal model attribute errors | Missing attributes for leaderboard display | 🔴 Active | Low |
| Leaderboard loading failure | Page fails to load | 🔴 Active | Low |

## Performance Issues

| Issue | Description | Status | Priority |
|-------|-------------|--------|----------|
| Health check rate limiting | Rate limit exceeded frequently | 🔴 Active | Low |
| Template rendering performance | Some pages slow to render | 🟡 Monitoring | Low |

## Next Steps

The following issues should be addressed in order of priority:

1. **Critical Database Issues**
   - Ensure consistent PostgreSQL usage
   - Fix migrations to create all tables properly

2. **Missing Templates**
   - Create or restore critical templates (especially base.html)
   - Fix template inheritance issues

3. **Core Feature Fixes**
   - Fix user profile and authentication issues
   - Address battle system errors
   - Fix waifu system relationship errors

4. **Secondary Features**
   - Add music files and fix player
   - Configure Twitter OAuth properly
   - Address cabal and leaderboard issues

## Issue Status Legend

- 🔴 **Active**: Issue confirmed and needs to be fixed
- 🟡 **In Progress**: Work has started on fixing this issue
- 🟢 **Resolved**: Issue has been fixed
- 🔵 **Monitoring**: Issue appears fixed but needs monitoring

## Updating This Document

When working on issues, please update this document with your progress:

1. Change the status as appropriate
2. Add notes about solutions or workarounds
3. Update the date at the bottom of the document

*Last updated: March 14, 2025* 