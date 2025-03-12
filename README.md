# Chad Battles

A blockchain-integrated, waifu-collecting battle game with meme-inspired characters, NFT functionality, and social gameplay through the Cabal system.

## Easy Setup (Automatic)

We've created a simple setup script that will automatically install and configure everything you need to play Chad Battles.

### Windows

1. Open Command Prompt or PowerShell
2. Navigate to the ChadBattles directory:
   ```
   cd path\to\ChadBattles
   ```
3. Run the setup script:
   ```
   python setup_and_run.py --continue
   ```
4. Follow the instructions in the terminal
5. The game will automatically open in your web browser

### macOS/Linux

1. Open Terminal
2. Navigate to the ChadBattles directory:
   ```
   cd path/to/ChadBattles
   ```
3. Run the setup script:
   ```
   python setup_and_run.py
   ```
4. Follow the instructions in the terminal
5. The game will automatically open in your web browser

## Manual Setup

If you prefer to set things up manually, follow these steps:

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```
   flask db upgrade
   ```

4. Start the development server:
   ```
   flask run
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Game Features

### Core Gameplay
- Create and level up your Chad character
- Collect waifus to boost your stats
- Battle other players (PVP) or AI enemies (PVE)
- Form cabals with other players for group battles
- Explore different locations with unique enemies

### Enhanced Cabal System
- Create or join cabals (guilds) with other players
- Appoint officers with specialized roles
- Participate in cabal vs cabal battles
- Climb the cabal leaderboard rankings
- View detailed analytics of your cabal's performance
- Receive weekly recaps of your cabal's activities
- Earn rewards through the referral system

### Referral System
- Invite friends to join your cabal using personalized referral links
- Earn Chadcoin and contribution points for each successful referral
- Unlock milestone bonuses for reaching referral targets
- Share achievements on Twitter to attract more members

### NFT Integration
- Mint your Chad characters, waifus, and items as NFTs on Solana
- Lock-in character appearance and stats at the time of minting
- Burn NFTs to receive Chadcoin rewards based on rarity and level
- Trade NFTs on third-party Solana marketplaces
- Track your NFT transaction history
- Connect multiple wallet types: Phantom, Solflare, Metamask, Magic Eden, and Slope
- 1% royalty on all NFT transactions to support game development

### Character Progression
- Level up your Chad and waifus
- Equip items to boost your stats
- Complete battles to earn XP and Chadcoin

## Demo Account

The setup script includes a demo account with the following credentials:
- Username: demo_user
- Character: Level 5 Sigma Chad
- Waifus: 2 starter waifus
- Chadcoin: 1000

Use this account to explore the game and test its features without needing to connect to external services.

## Development

### Environment Variables
- `FLASK_APP`: Set to "app"
- `FLASK_ENV`: "development" or "production"
- `DATABASE_URL`: Database connection string (SQLite by default)
- `SECRET_KEY`: Secret key for session security
- `TWITTER_CONSUMER_KEY`: Twitter API consumer key
- `TWITTER_CONSUMER_SECRET`: Twitter API consumer secret
- `TWITTER_ACCESS_TOKEN`: Twitter API access token
- `TWITTER_ACCESS_TOKEN_SECRET`: Twitter API access token secret
- `ENABLE_CACHING`: Set to "true" to enable caching
- `CACHE_TYPE`: Cache backend type (e.g., "redis")
- `CACHE_REDIS_URL`: Redis connection URL for caching

### Testing
Run tests using pytest:
```
pytest
```

For specific test modules:
```
pytest tests/test_cabal_model.py
```

## Troubleshooting

### Common Issues

1. **Virtual environment not activating**
   - Make sure Python is installed and in your PATH
   - Try using the absolute path to Python when creating the venv

2. **Database migration errors**
   - Delete the migrations folder and database file, then reinitialize:
     ```
     flask db init
     flask db migrate
     flask db upgrade
     ```

3. **Flask command not found**
   - Make sure Flask is installed: `pip install Flask`
   - Try using `python -m flask` instead of `flask`

4. **Browser doesn't open automatically**
   - Open your browser manually and navigate to: http://127.0.0.1:5000

5. **Scheduled tasks not running**
   - Ensure Redis is installed and running
   - Check that APScheduler is properly configured
   - Verify that the application is running with the scheduler enabled

For additional help or to report issues, please open a GitHub issue or contact the development team.

## Features

- **Character Creation**: Your X profile becomes a unique Chad character with special abilities
- **Waifu Collection**: Collect and upgrade rare waifus that boost your stats
- **Battle System**: Challenge other players and win their waifus
- **Cabal Mechanics**: Form cabals with other players for group battles
- **Referral System**: Invite friends to join your cabal and earn rewards
- **Analytics Dashboard**: Track your cabal's performance with detailed metrics
- **Blockchain Integration**: Mint waifus as NFTs and trade them on third-party marketplaces
- **Twitter Bot**: Interact with the game directly through Twitter commands

## Getting Started

See the [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) file for detailed installation and setup instructions.

## Tech Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLAlchemy with PostgreSQL
- **Caching**: Redis for performance optimization
- **Scheduled Tasks**: APScheduler for background jobs
- **Blockchain**: Solana for NFT operations (supports Phantom, Solflare, Metamask, and Magic Eden wallets)
- **Social Integration**: Twitter API

## Project Structure

```
ChadBattles/
├── app/                    # Main application directory
│   ├── controllers/        # Route controllers
│   ├── models/             # Database models
│   ├── services/           # Business logic services
│   ├── static/             # Static assets (CSS, JS, images)
│   ├── templates/          # HTML templates
│   └── utils/              # Utility functions
├── migrations/             # Database migrations
├── tests/                  # Test suite
├── twitter_bot/            # Twitter bot functionality
├── blockchain/             # Blockchain integration
├── docs/                   # Documentation
├── .env.example            # Example environment variables
├── requirements.txt        # Python dependencies
└── run.py                  # Application entry point
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Special thanks to all the meme creators who inspired this project
- The Flask team for an awesome framework
- The Solana ecosystem for NFT capabilities 

## Environments

### Development
- Local SQLite database for quick development
- Simulated wallet connections for testing
- Automatic reload of code changes
- Comprehensive error logging

### Testing
- Separate test database to avoid corrupting development data
- Mock wallet and blockchain interactions
- Automated test suite for all major functionality
- Continuous integration to catch regressions

### Production
- PostgreSQL database for scalability and reliability
- Real blockchain connections using Solana
- Redis caching for improved performance
- Error monitoring and reporting
- Regular database backups

## Documentation

- [Setup Instructions](SETUP_INSTRUCTIONS.md): Detailed guide for installing and configuring the game
- [NFT System](docs/nft_system.md): Documentation of the NFT system architecture and functionality
- [Cabal System](docs/cabal_system.md): Overview of the cabal mechanics and social features
- [API Documentation](docs/api.md): Details of the REST API endpoints
- [Wallet Integration](docs/wallet_integration.md): Guide for wallet connections and blockchain interactions 