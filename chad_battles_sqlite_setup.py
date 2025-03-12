#!/usr/bin/env python
import os
import sys
import subprocess
import time
import webbrowser

def print_header():
    print("\n" + "="*80)
    print("                  CHAD BATTLES SQLITE SETUP")
    print("="*80)
    print("""
This script will set up Chad Battles with SQLite instead of PostgreSQL:
1. Configure the database to use SQLite 
2. Initialize the database
3. Start the game
""")

def print_step(message):
    print("\n" + "="*80)
    print(f"  {message}")
    print("="*80)

def run_command(command, shell=False):
    print(f"> {command if isinstance(command, str) else ' '.join(command)}")
    try:
        if shell:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, 
                                      stderr=subprocess.STDOUT, universal_newlines=True)
        else:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                      stderr=subprocess.STDOUT, universal_newlines=True)
            
        for line in process.stdout:
            print(line.strip())
        
        process.wait()
        return process.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def setup_env_for_sqlite():
    print_step("Setting up environment for SQLite")
    
    # Create .env file with SQLite configuration
    with open('.env', 'w') as f:
        f.write("""FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=dev-key-change-in-production
""")
    
    # Set environment variables
    os.environ["FLASK_APP"] = "app"
    os.environ["FLASK_ENV"] = "development"
    os.environ["DATABASE_URL"] = "sqlite:///app.db"
    
    return True

def setup_database():
    print_step("Setting up SQLite database")
    
    # Initialize the database
    run_command([sys.executable, "-m", "flask", "db", "init"])
    run_command([sys.executable, "-m", "flask", "db", "migrate", "-m", "Initial migration"])
    run_command([sys.executable, "-m", "flask", "db", "upgrade"])
    
    return True

def run_server():
    print_step("Starting the game server")
    
    # Run the Flask app
    server_process = subprocess.Popen([sys.executable, "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"])
    
    # Give the server a moment to start
    time.sleep(3)
    
    # Open the browser
    webbrowser.open("http://localhost:5000")
    
    try:
        # Keep the server running until Ctrl+C
        print("\nGame server is running. Press Ctrl+C to stop.")
        server_process.wait()
    except KeyboardInterrupt:
        server_process.terminate()
        print("\nGame server stopped.")

def install_dependencies():
    print_step("Installing required dependencies")
    
    # List of dependencies needed for SQLite setup
    dependencies = [
        "flask==2.2.3",
        "flask-sqlalchemy==3.0.3",
        "flask-migrate==4.0.4",
        "flask-login==0.6.2",
        "flask-wtf==1.1.1",
        "flask-cors==3.0.10",
        "flask-restful==0.3.10",
        "flask-caching==2.0.2",
        "sqlalchemy==2.0.5",
        "alembic==1.10.2",
        "python-dotenv==1.0.0",
        "werkzeug==2.2.3",
        "tweepy==4.14.0",
        "python-twitter-v2==0.8.1"
    ]
    
    # Install each dependency individually
    success = True
    for dep in dependencies:
        print(f"Installing {dep}...")
        if not run_command([sys.executable, "-m", "pip", "install", dep]):
            print(f"Warning: Failed to install {dep}")
            success = False
    
    return success

def main():
    print_header()
    
    # First install dependencies
    if install_dependencies():
        if setup_env_for_sqlite():
            if setup_database():
                run_server()
            else:
                print("Failed to set up the database. Please check the errors above.")
        else:
            print("Failed to set up the environment. Please check the errors above.")
    else:
        print("Failed to install dependencies. Please check the errors above.")

if __name__ == "__main__":
    main() 