import os
import sys
import subprocess
import platform
import time
import webbrowser

def print_step(message):
    """Print a formatted step message."""
    print("\n" + "="*80)
    print(f"  {message}")
    print("="*80)

def run_command(command):
    """Run a command and print its output."""
    print(f"> {command}")
    try:
        process = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(process.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(e.stdout)
        print(e.stderr)
        return False

def setup_env():
    """Set up the environment variables."""
    print_step("Setting up environment")
    
    # Create .env file
    with open('.env', 'w') as f:
        f.write("""FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=dev-key-for-testing-only
""")
    
    # Set environment variables
    os.environ["FLASK_APP"] = "app"
    os.environ["FLASK_ENV"] = "development"
    os.environ["DATABASE_URL"] = "sqlite:///app.db"
    
    return True

def install_dependencies():
    """Install dependencies."""
    print_step("Installing dependencies")
    
    # Install each dependency individually using the full path to pip
    dependencies = [
        "Flask==2.2.3",
        "Flask-SQLAlchemy==3.0.3",
        "Flask-Migrate==4.0.4",
        "Flask-Login==0.6.2",
        "Flask-WTF==1.1.1",
        "Flask-Cors==3.0.10",
        "SQLAlchemy==2.0.5",
        "python-dotenv==1.0.0",
        "Werkzeug==2.2.3",
        "itsdangerous==2.1.2",
        "Jinja2==3.1.2",
        "click==8.1.3",
        "alembic==1.10.2"
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        result = run_command(f"{sys.executable} -m pip install {dep}")
        if not result:
            print(f"Warning: Failed to install {dep}, but continuing with setup...")
    
    return True

def activate_venv():
    """Activate the virtual environment."""
    print_step("Activating virtual environment")
    
    if platform.system() == "Windows":
        activate_script = os.path.join("venv", "Scripts", "activate")
        os.system(f"{activate_script}")
    else:
        activate_script = os.path.join("venv", "bin", "activate")
        os.system(f"source {activate_script}")
    
    return True

def setup_database():
    """Set up the database."""
    print_step("Setting up the database")
    
    # Create a simple app.py file if it doesn't exist
    if not os.path.exists("app.py"):
        with open("app.py", "w") as f:
            f.write("""from app import create_app

app = create_app()
""")
    
    # Initialize the database
    run_command("python -m flask db init")
    run_command("python -m flask db migrate -m 'Initial migration'")
    run_command("python -m flask db upgrade")
    
    return True

def setup_demo_data():
    """Set up demo data."""
    print_step("Setting up demo data")
    
    # Create a simple script to populate demo data
    with open("setup_demo_data.py", "w") as f:
        f.write("""
from app import create_app, db

def setup_demo_data():
    app = create_app()
    with app.app_context():
        # Here we would normally populate demo data
        # For now, we'll just print a success message
        print("Demo data would be set up here.")
        print("For now, you can explore the app structure.")

if __name__ == '__main__':
    setup_demo_data()
""")
    
    # Run the script
    run_command("python setup_demo_data.py")
    
    return True

def run_server():
    """Run the development server."""
    print_step("Starting the development server")
    
    # Open the browser
    webbrowser.open("http://127.0.0.1:5000")
    
    # Run the server
    run_command("python -m flask run")
    
    return True

def main():
    """Main function."""
    print("""
===============================================================================
                    CHAD BATTLES SETUP SCRIPT (LITE VERSION)
===============================================================================

This script will set up a simplified version of Chad Battles for development:
1. Install core dependencies (SQLite version)
2. Set up the database
3. Set up minimal demo data
4. Start the development server

The app will open in your browser automatically.
""")
    
    if setup_env() and install_dependencies() and setup_database() and setup_demo_data():
        run_server()
    else:
        print("\nSetup failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 