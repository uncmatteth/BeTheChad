# CHAD BATTLES - Complete Game Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Twitter Commands](#twitter-commands)
4. [Battles](#battles)
5. [Waifus](#waifus)
6. [Items](#items)
7. [Marketplace](#marketplace)
8. [Leaderboards](#leaderboards)
9. [Technical Setup](#technical-setup)

## Introduction

Chad Battles is a Twitter-integrated game where you control a "Chad" character and battle other Chads. The game combines traditional RPG elements with social media integration, allowing you to command your Chad through Twitter posts.

## Getting Started

### Creating Your Chad

1. **Login with Twitter**: Visit the [Chad Battles website](http://localhost:5000) and click "Login with X"
2. **Create Your Character**: Tweet "MAKE ME A CHAD @RollMasterChad" to create your character
3. **Choose a Chad Class**: Select from:
   - **Sigma**: The lone wolf. High in roast and resistance.
   - **Alpha**: The leader. High in clout and drip.
   - **Grindset**: The hustler. Balanced stats.
4. **Initial Setup**: Your Chad starts with basic stats and 1000 Chadcoin

### Understanding Stats

- **Clout**: Determines your influence and status
- **Roast Level**: Your ability to attack others
- **Cringe Resistance**: Your defense against attacks
- **Drip Factor**: Affects item effectiveness and appearance

## Twitter Commands

You control your Chad by tweeting specific commands. All commands must include the hashtag `#ChadBattles` to be recognized by the system.

### Basic Commands

| Command | Example Tweet | Description |
|---------|--------------|-------------|
| create character | "MAKE ME A CHAD @RollMasterChad" | Creates your Chad character |
| stats | "SHOW MY STATS @RollMasterChad" | Shows your current stats |
| inventory | "SHOW MY INVENTORY @RollMasterChad" | Lists your items |
| waifus | "SHOW MY WAIFUS @RollMasterChad" | Lists your waifus |
| balance | "SHOW MY BALANCE @RollMasterChad" | Shows your Chadcoin amount |
| leaderboard | "SHOW THE LEADERBOARD @RollMasterChad" | Shows top players |

### Battle Commands

| Command | Example Tweet | Description |
|---------|--------------|-------------|
| battle @user | "I'm going to CRUSH @username! CHALLENGE TO BATTLE @RollMasterChad" | Initiates a battle |
| accept | "I ACCEPT THE BATTLE @RollMasterChad" | Accepts a battle |
| attack | "I USE SAVAGE ROAST @RollMasterChad" | Standard attack in battle |
| special | "I USE SIGMA MOVE @RollMasterChad" | Special move (costs energy) |
| flee | "I WANT TO FLEE @RollMasterChad" | Attempt to escape battle (may fail) |

### Marketplace Commands

| Command | Example Tweet | Description |
|---------|--------------|-------------|
| shop | "SHOW ME THE SHOP @RollMasterChad" | View available items |
| buy item_name | "I WANT TO BUY Premium Shades @RollMasterChad" | Purchase an item |
| sell item_id | "Selling item #123 #ChadBattles" | Sell an item |
| equip item_id | "Equip item #123 #ChadBattles" | Equip an item to your Chad |

## Battles

Battles in Chad Battles are turn-based encounters between two players.

### Battle Flow

1. **Challenge**: One player challenges another with the battle command
2. **Acceptance**: The challenged player must accept
3. **Turn-Based Combat**: Players alternate turns using commands
4. **Victory**: Achieved when opponent's HP reaches 0
5. **Rewards**: Winner receives Chadcoin and XP

### Battle Strategies

- **Class Matchups**: Different Chad classes have advantages against others
- **Waifu Bonuses**: Your equipped waifu provides stat bonuses
- **Item Effects**: Equipped items can change battle dynamics
- **Special Moves**: Use your class's special moves for powerful effects

## Waifus

Waifus are companions that boost your Chad's abilities.

### Waifu Types

- **Tsundere**: Boosts Roast
- **Gamer Girl**: Improves Cringe Resistance
- **Cyberpunk**: Enhances Drip

### Obtaining Waifus

Waifus can be:
- Purchased from the marketplace
- Won from special events
- Earned from battles

### Waifu Management

- You can only have one equipped waifu at a time
- Waifus can be leveled up with use
- Higher rarity waifus provide better bonuses

## Items

Items enhance your Chad's abilities and appearance.

### Item Categories

- **Hats**: Improve Clout
- **Shades**: Boost Roast
- **Outfits**: Enhance Drip
- **Accessories**: Various effects

### Item Rarity

Items come in different rarities:
- **Common**: Basic stat boosts
- **Uncommon**: Better stat boosts
- **Rare**: Significant stat boosts
- **Epic**: Major stat boosts and special effects
- **Legendary**: Massive stat boosts and unique effects

## Marketplace

The marketplace is where you can buy and sell items and waifus.

### Currency

- **Chadcoin**: The main currency, earned from battles and activities

### Trading

- Players can sell items to each other
- Prices fluctuate based on demand
- Special limited-time offers appear periodically

## Leaderboards

Leaderboards track the top players in different categories.

### Leaderboard Types

- **Battle Wins**: Most battles won
- **Clout**: Highest clout stat
- **Chadcoin**: Richest players
- **Total Level**: Highest combined level (Chad + Waifus)

## Technical Setup

### Running the Game

1. **Local Development**:
   ```
   cd C:\ChadBattlesClean
   .\run_music_player.bat
   ```

2. **Accessing the Game**:
   - Open your browser and go to: `http://localhost:5000`

### Adding Music

To add background music to the game:

1. Place MP3 files in `C:\ChadBattlesClean\app\static\music`
2. Restart the application or refresh the page

### Twitter Bot Integration

The game includes a Twitter bot that responds to commands:

1. Twitter bot credentials are configured in the `.env` file:
   ```
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_SECRET=your_access_token_secret
   ```

2. To run the Twitter bot:
   ```
   python twitter_bot.py
   ```

3. The bot will automatically respond to tweets containing #ChadBattles

---

Enjoy your Chad Battles experience! If you encounter any issues, please report them on our GitHub repository. 