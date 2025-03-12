#!/usr/bin/env python
import os
import sys
import subprocess
import platform
import time
import webbrowser
import shutil

def print_step(message):
    """Print a formatted step message."""
    print("\n" + "="*80)
    print(f"  {message}")
    print("="*80)

def run_command(command, shell=False):
    """Run a command and print its output."""
    print(f"> {command if isinstance(command, str) else ' '.join(command)}")
    try:
        if shell:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        else:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            
        for line in process.stdout:
            print(line.strip())
        
        process.wait()
        return process.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def setup_sqlite_env():
    """Set up the environment for SQLite."""
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

def install_dependencies():
    """Install dependencies using the SQLite requirements."""
    print_step("Installing dependencies (SQLite version)")
    
    # Use our SQLite-specific requirements
    if not os.path.exists("requirements_sqlite.txt"):
        print("Error: requirements_sqlite.txt not found.")
        return False
    
    return run_command([sys.executable, "-m", "pip", "install", "-r", "requirements_sqlite.txt"])

def setup_database():
    """Set up the database."""
    print_step("Setting up the database (SQLite)")
    
    # Initialize the database
    print("Initializing database...")
    if not os.path.exists("migrations"):
        if not run_command([sys.executable, "-m", "flask", "db", "init"]):
            print("Warning: Failed to initialize database, but continuing...")
    
    # Create a migration
    print("Creating database migration...")
    if not run_command([sys.executable, "-m", "flask", "db", "migrate", "-m", "Initial migration"]):
        print("Warning: Failed to create migration, but continuing...")
    
    # Apply the migration
    print("Applying database migration...")
    return run_command([sys.executable, "-m", "flask", "db", "upgrade"])

def run_server():
    """Run the server."""
    print_step("Starting the game server")
    
    # Check if run.py exists, if not create a simple one
    if not os.path.exists("run.py"):
        with open("run.py", "w") as f:
            f.write("""from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
""")
    
    # Start the server
    server_process = subprocess.Popen([sys.executable, "run.py"])
    
    # Give the server a moment to start
    time.sleep(3)
    
    # Open the browser
    webbrowser.open("http://localhost:5000")
    
    try:
        print("\nGame server is running. Press Ctrl+C to stop.")
        server_process.wait()
    except KeyboardInterrupt:
        server_process.terminate()
        print("\nGame server stopped.")

def main():
    print("\n" + "="*80)
    print("                          CHAD BATTLES SQLITE SETUP")
    print("="*80)
    print("""
This script will set up Chad Battles with SQLite instead of PostgreSQL:
1. Configure the environment to use SQLite
2. Install required dependencies
3. Set up the database
4. Start the game server

The game will open in your web browser automatically.
""")
    
    # First, setup environment
    if setup_sqlite_env():
        # Then install dependencies
        if install_dependencies():
            # Then setup database
            if setup_database():
                # Finally run the server
                run_server()
            else:
                print("Failed to set up the database. Please check the errors above.")
        else:
            print("Failed to install dependencies. Please check the errors above.")
    else:
        print("Failed to set up the environment. Please check the errors above.")

if __name__ == "__main__":
    main() 