import os
import sys
import subprocess

print("="*80)
print("CHAD BATTLES - SWITCH TO SQLITE")
print("="*80)
print("This script will configure Chad Battles to use SQLite instead of PostgreSQL.")

# Create .env file with SQLite configuration
print("\nCreating .env file with SQLite configuration...")
with open('.env', 'w') as f:
    f.write("""FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=dev-key-change-in-production
""")

print("Setting environment variables...")
os.environ["FLASK_APP"] = "app"
os.environ["FLASK_ENV"] = "development"
os.environ["DATABASE_URL"] = "sqlite:///app.db"

print("\nConfiguration complete!")
print("\nYou can now run the game using:")
print("python run.py")
print("\nOr continue the setup with:")
print("python setup_and_run.py --continue") 