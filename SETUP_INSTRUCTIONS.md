# Chad Battles Setup Instructions

This document provides instructions for setting up and running the Chad Battles application.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Twitter Developer Account with API credentials
- Solana wallet for NFT operations (optional for development)

## Installation Steps

1. **Clone the repository** (if you're using version control):
   ```
   git clone https://github.com/yourusername/chad-battles.git
   cd chad-battles
   ```

2. **Create and activate a virtual environment**:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Create environment variables file** (.env in the project root):
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-change-in-production

   # Twitter API credentials
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET=your_twitter_api_secret
   TWITTER_ACCESS_TOKEN=your_twitter_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

   # Solana configuration (optional for development)
   SOLANA_RPC_URL=https://api.devnet.solana.com
   SOLANA_PRIVATE_KEY=your_solana_private_key

   # Database URLs
   DEV_DATABASE_URI=sqlite:///dev.db
   TEST_DATABASE_URI=sqlite:///test.db
   DATABASE_URI=postgresql://username:password@localhost/chad_battles_prod
   ```

5. **Initialize the database**:
   ```
   # Create the database tables
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

   # Populate the database with initial data
   python init_db.py
   ```

6. **Create static asset directories**:
   ```
   mkdir -p app/static/img/{chad,waifu,item,elixir}
   ```

## Running the Application

1. **Start the Flask development server**:
   ```
   flask run
   ```

   The application will be available at http://127.0.0.1:5000/

2. **Run the Twitter bot** (in a separate terminal):
   ```
   python twitter_bot.py
   ```

## Development Workflow

1. **Create a new branch for features** (if using Git):
   ```
   git checkout -b feature/my-new-feature
   ```

2. **Run tests**:
   ```
   pytest
   ```

3. **Database migrations** (when changing models):
   ```
   flask db migrate -m "Description of changes"
   flask db upgrade
   ```

## Deployment

For production deployment:

1. Set `FLASK_ENV=production` in your environment or .env file
2. Use a production WSGI server like Gunicorn:
   ```
   gunicorn run:app
   ```

3. Configure Nginx as a reverse proxy

4. Set up proper database credentials for the production database

## Environments

The application supports different environments:

- **Development**: Uses SQLite by default (`DEV_DATABASE_URI`)
- **Testing**: Uses a separate SQLite database (`TEST_DATABASE_URI`)
- **Production**: Uses PostgreSQL (`DATABASE_URI`)

## Troubleshooting

- **Twitter API Issues**: Ensure your API credentials are correct and your app has the required permissions
- **Database Errors**: Check connection strings and make sure the database exists
- **Image Loading Errors**: Verify that the static asset directories exist and contain the expected files

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [Solana Documentation](https://docs.solana.com/) 