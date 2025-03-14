# Chad Battles

A blockchain-enabled battle game where users create Chads, join Cabals, and compete in epic battles.

## Current Status

The application is now successfully deployed on Render.com and is operational.

- ✅ Core functionality: User accounts, Chads, Cabals, and Battles
- ✅ Database: PostgreSQL with proper initialization
- ✅ Twitter Integration: Login and bot functionality
- ✅ Rendering: All templates working correctly
- ✅ Music Player: 104 tracks with fully functional controls

For detailed deployment status and progress, see [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md).
For music player verification status, see [MUSIC_PLAYER_VERIFICATION.md](MUSIC_PLAYER_VERIFICATION.md).

## Features

- **Character Creation**: Create and customize your Chad characters
- **Cabals**: Join or create your own Cabal to battle with others
- **Battles**: Engage in epic battles with other Cabals
- **Inventory System**: Collect and equip items to boost your Chad's stats
- **Twitter Integration**: Login with Twitter and interact with the game via Twitter
- **Music Player**: Enjoy 104 "Be the Chad" tracks while using the site

## Getting Started

### For Users

1. Visit [ChadBattles.fun](https://chadbattles.fun)
2. Login with your Twitter account
3. Create your first Chad character
4. Join a Cabal or create your own
5. Start battling!
6. Enjoy the background music or toggle it on/off as needed

### For Developers

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the environment variables (see `.env.example`)
4. Initialize the database: `flask init-db`
5. Run the development server: `flask run`
6. For quick testing with music player: `play_with_music.bat` (Windows)

## Documentation

- [Deployment Guide](DEPLOYMENT.md)
- [Fixed Deployment Guide](FIXED_DEPLOYMENT_GUIDE.md)
- [Deployment Status](DEPLOYMENT_STATUS.md)
- [API Documentation](docs/api.md)
- [Music Player Information](MUSIC_PLAYER_README.md)
- [Music Player Verification](MUSIC_PLAYER_VERIFICATION.md)

## Recent Updates

- Added 104 "Be the Chad" MP3 files for the music player
- Fixed all issues in the WEBSITE_ISSUES_CHECKLIST.md
- Improved Twitter command format and authentication flow
- Added proper wallet connection modal with icons

## Contact

For more information, contact: admin@chadbattles.fun 