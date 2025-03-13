# Chad Battles

A blockchain-enabled battle game where users create Chads, join Cabals, and compete in epic battles.

## Current Status

The application is now successfully deployed on Render.com and is operational.

- ✅ Core functionality: User accounts, Chads, Cabals, and Battles
- ✅ Database: PostgreSQL with proper initialization
- ✅ Twitter Integration: Login and bot functionality
- ✅ Rendering: All templates working correctly

For detailed deployment status and progress, see [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md).

## Features

- **Character Creation**: Create and customize your Chad characters
- **Cabals**: Join or create your own Cabal to battle with others
- **Battles**: Engage in epic battles with other Cabals
- **Inventory System**: Collect and equip items to boost your Chad's stats
- **Twitter Integration**: Login with Twitter and interact with the game via Twitter

## Getting Started

### For Users

1. Visit [ChadBattles.fun](https://chadbattles.fun)
2. Login with your Twitter account
3. Create your first Chad character
4. Join a Cabal or create your own
5. Start battling!

### For Developers

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up the environment variables (see `.env.example`)
4. Initialize the database: `flask init-db`
5. Run the development server: `flask run`

## Documentation

- [Deployment Guide](DEPLOYMENT.md)
- [Fixed Deployment Guide](FIXED_DEPLOYMENT_GUIDE.md)
- [Deployment Status](DEPLOYMENT_STATUS.md)
- [API Documentation](docs/api.md)

## Contact

For more information, contact: admin@chadbattles.fun 