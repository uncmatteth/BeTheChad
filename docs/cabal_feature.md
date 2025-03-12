# Cabal Feature Documentation

## Overview
The Cabal feature allows users to form groups (Cabals) with other players in Chad Battles. This social gameplay mechanic enhances user engagement by providing stat bonuses, group battles, leadership mechanics, and a competitive leaderboard system.

## Models

### Cabal Model
The main `Cabal` model represents a group of players and has the following key fields:
- `id`: Unique identifier (UUID)
- `name`: Cabal name (unique)
- `description`: Description text
- `leader_id`: Reference to the Chad who leads the cabal
- `invite_code`: Unique code for joining the cabal
- `level` and `xp`: Progression tracking
- `battles_won` and `battles_lost`: Battle statistics
- `total_power`: Calculated battle power for leaderboards
- `rank`: Current position on the leaderboard

Key methods include:
- `add_member`, `remove_member`: Manage cabal membership
- `change_leader`: Transfer leadership to another member
- `appoint_officer`: Assign special roles to members
- `vote_to_remove_leader`: Democratic leadership removal
- `calculate_total_power`: Compute cabal's battle strength
- `schedule_battle`: Arrange battles with other cabals
- `disband`: Remove the cabal and all related data

### CabalMember Model
Tracks membership in a cabal with fields:
- `cabal_id` and `chad_id`: References to the cabal and member
- `is_active`: Member activity status
- `battles_participated`: Battle participation count
- `daily_battles`: Tracks daily battle participation (max 5)
- `contribution_score`: Points based on participation
- `joined_at`: Membership start date

### CabalOfficerRole Model
Defines officer positions within a cabal:
- `cabal_id` and `chad_id`: References to the cabal and officer
- `role_type`: The type of officer role (`clout`, `roast_level`, `cringe_resistance`, `drip_factor`)
- Each officer grants 50% of their primary stat to all cabal members

### CabalVote Model
Tracks votes for leadership changes:
- `vote_type`: Type of vote (e.g., `remove_leader`)
- `voter_id`: Who cast the vote
- `target_id`: Who the vote affects
- Leader removal requires 3/4 of officers or active members to vote

### CabalBattle Model
Manages battles between cabals:
- `cabal_id` and `opponent_cabal_id`: The two cabals involved
- `scheduled_at`: When the battle occurs
- `completed` and `result`: Battle outcome tracking
- `week_number`: For enforcing the 3-battle weekly limit

### CabalBattleParticipant Model
Tracks which members participate in battles:
- `battle_id`, `chad_id`, `cabal_id`: References to battle and participant
- Members must opt in to participate and receive rewards
- Limited to 5 battles per day per member

## Controllers

### Main Routes
- `index`: Display user's cabal info and membership status
- `create`: Create a new cabal
- `join`: Join an existing cabal via invite code
- `leave`: Leave current cabal
- `disband`: Disband a cabal (leader only)

### Member Management
- `remove_member`: Remove a member from the cabal (leader only)
- `promote_leader`: Transfer leadership to another member
- `appoint_officer`: Assign an officer role to a member
- `remove_officer`: Remove an officer from their role
- `vote_remove_leader`: Vote to remove the current leader

### Battle System
- `schedule_battle`: Schedule a battle with another cabal
- `opt_into_battle`: Opt into participating in an upcoming battle
- `all_battles`: View all upcoming and past battles
- `leaderboard`: Display the top cabals by power

## Templates

### Core Templates
- `index.html`: Main cabal view showing leadership, officers, and status
- `create.html`: Form for creating a new cabal
- `join.html`: Interface for joining a cabal via invite code

### Battle Templates
- `schedule_battle.html`: Form for scheduling battles
- `all_battles.html`: List of upcoming and past battles
- `leaderboard.html`: Ranking of cabals by power

## Twitter Bot Commands

The following Twitter commands allow users to interact with the Cabal system:

1. **Create Cabal**
   - Pattern: `CREATE CABAL (name) @RollMasterChad`
   - Function: `handle_create_cabal`
   - Creates a new cabal with the user as leader

2. **Appoint Officer**
   - Pattern: `APPOINT @(username) AS (role) OFFICER @RollMasterChad`
   - Function: `handle_appoint_officer`
   - Roles: CLOUT, ROAST, CRINGE, DRIP
   - Appoints a cabal member to an officer position

3. **Schedule Battle**
   - Pattern: `BATTLE CABAL (name) @RollMasterChad`
   - Function: `handle_schedule_battle`
   - Schedules a battle with another cabal

4. **Vote to Remove Leader**
   - Pattern: `VOTE REMOVE CABAL LEADER @RollMasterChad`
   - Function: `handle_vote_remove_leader`
   - Casts a vote to remove the current cabal leader

5. **Opt Into Battle**
   - Pattern: `JOIN NEXT CABAL BATTLE @RollMasterChad`
   - Function: `handle_opt_in_battle`
   - Opts the user into participating in their cabal's next scheduled battle

## Cabal Mechanics

### Leadership Structure
- **Lord of the Shill**: The cabal leader who grants +0.1 to all stats for all members
- **Officers**:
  - **Clout Commander**: Grants 50% of their Clout stat to all members
  - **Roast Master**: Grants 50% of their Roast Level stat to all members
  - **Cringe Shield**: Grants 50% of their Cringe Resistance stat to all members
  - **Drip Director**: Grants 50% of their Drip Factor stat to all members

### Battle System
- Cabals can schedule up to 3 battles per week
- Individual members can participate in up to 5 battles per day
- Members must opt in to participate in battles
- Battle power calculation includes:
  - Base stats of all participating members
  - Officer bonuses (50% of their corresponding stat)
  - Leader bonus (+0.1 to all stats)
  - Level bonus (5% per cabal level)
  - Possible debuffs (10% reduction if active)

### Rewards
- **Victory**:
  - Cabal XP: 200-500 XP based on opponent level
  - Member XP: 50-100 XP per participating member
  - Chadcoin: 25-75 per participating member
  - Item chance: 15% chance for rare items
- **Defeat**:
  - Cabal XP: 50-100 XP for effort
  - Member XP: 10-25 XP per participating member

## Limitations and Constraints
- Maximum cabal size: 69 members
- Weekly battle limit: 3 battles per cabal
- Daily member battle limit: 5 battles per member
- Leader removal: Requires 3/4 majority of officers or active members
- Officers cannot be the cabal leader simultaneously
- Members can only belong to one cabal at a time

## Usage Examples

### Creating a Cabal
```
@ChadBot CREATE CABAL MemeTeam
```
Response: "Cabal 'MemeTeam' created! You are now the Lord of the Shill. Share your invite code 'A1B2C3' with others to build your cabal."

### Appointing an Officer
```
@ChadBot APPOINT @user123 AS CLOUT OFFICER
```
Response: "@user123 appointed as Clout Commander! They now grant 50% of their Clout to all cabal members."

### Scheduling a Battle
```
@ChadBot BATTLE CABAL RivalTeam
```
Response: "Battle scheduled against 'RivalTeam' for tomorrow at 20:00 UTC! Encourage your members to opt in with 'JOIN NEXT CABAL BATTLE'."

## Testing
- Unit tests: `tests/test_cabal_model.py`
- Route tests: `tests/test_cabal_routes.py`
- Bot command tests: `tests/test_bot_commands.py` 