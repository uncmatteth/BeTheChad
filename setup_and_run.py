#!/usr/bin/env python
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

def is_venv_activated():
    """Check if a virtual environment is activated."""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def setup_virtual_env():
    """Set up a virtual environment."""
    print_step("Setting up virtual environment")
    
    if is_venv_activated():
        print("Virtual environment is already activated.")
        return True
    
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        if not run_command([sys.executable, "-m", "venv", "venv"]):
            print("Failed to create virtual environment.")
            return False
    
    # Activate the virtual environment
    if platform.system() == "Windows":
        activate_script = os.path.join("venv", "Scripts", "activate")
        activate_cmd = f"{activate_script} && python -c \"import sys; print('Activated:', sys.prefix)\""
        run_command(activate_cmd, shell=True)
        # We need to return a new script to run with the activated environment
        return f"{activate_script} && python {__file__} --continue"
    else:
        activate_script = os.path.join("venv", "bin", "activate")
        activate_cmd = f"source {activate_script} && python -c \"import sys; print('Activated:', sys.prefix)\""
        run_command(activate_cmd, shell=True)
        # We need to return a new script to run with the activated environment
        return f"source {activate_script} && python {__file__} --continue"

def install_dependencies():
    """Install dependencies from requirements.txt."""
    print_step("Installing dependencies")
    
    if not os.path.exists("requirements.txt"):
        print("requirements.txt not found. Creating basic requirements...")
        with open("requirements.txt", "w") as f:
            f.write("""Flask==2.2.3
Flask-SQLAlchemy==3.0.3
Flask-Migrate==4.0.4
Flask-Login==0.6.2
Flask-WTF==1.1.1
Flask-Cors==3.0.10
SQLAlchemy==2.0.5
python-dotenv==1.0.0
""")
    
    # Instead of installing all requirements at once, install them individually and skip problematic ones
    with open("requirements.txt", "r") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    all_succeeded = True
    for req in requirements:
        # Skip PostgreSQL-related packages
        if "psycopg2" in req:
            print(f"Skipping {req} (PostgreSQL dependency)...")
            continue
            
        print(f"Installing {req}...")
        if not run_command([sys.executable, "-m", "pip", "install", req]):
            print(f"Warning: Failed to install {req}")
            # Don't fail completely if a single package fails
            if "bcrypt" not in req and "pillow" not in req and "solana" not in req and "construct" not in req:
                all_succeeded = False
    
    return all_succeeded

def setup_database():
    """Set up the database."""
    print_step("Setting up the database")
    
    # Ensure the .env file exists with SQLite database configuration
    if not os.path.exists(".env"):
        print("Creating .env file with SQLite database configuration...")
        with open(".env", "w") as f:
            f.write("""FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=dev-key-change-in-production
""")
    else:
        # Update existing .env file to use SQLite
        with open(".env", "r") as f:
            env_content = f.read()
        
        if "DATABASE_URL=postgresql" in env_content:
            print("Updating .env to use SQLite instead of PostgreSQL...")
            env_content = env_content.replace("DATABASE_URL=postgresql", "DATABASE_URL=sqlite:///app.db")
            with open(".env", "w") as f:
                f.write(env_content)
    
    # Set environment variables
    os.environ["FLASK_APP"] = "app"
    os.environ["FLASK_ENV"] = "development"
    os.environ["DATABASE_URL"] = "sqlite:///app.db"
    
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

def setup_demo_data():
    """Set up demo data for the game."""
    print_step("Setting up demo data")
    
    # Create a script to populate demo data
    with open("setup_demo_data.py", "w") as f:
        f.write("""
from app import create_app, db
from app.models.user import User
from app.models.chad import ChadClass, Chad
from app.models.waifu import WaifuRarity, WaifuType, Waifu
from app.models.item import ItemRarity, ItemType
from app.models.location import Location, LocationType
from app.models.pve_enemy import PVEEnemy, EnemyType
from app.models.transaction import TransactionType
import random

def setup_demo_data():
    app = create_app()
    with app.app_context():
        # Create demo classes
        chad_classes = [
            ChadClass(
                name='Sigma',
                description='The lone wolf. High in roast and resistance.',
                base_clout_bonus=5,
                base_roast_bonus=8,
                base_cringe_resistance_bonus=7,
                base_drip_bonus=5
            ),
            ChadClass(
                name='Alpha',
                description='The leader. High in clout and drip.',
                base_clout_bonus=10,
                base_roast_bonus=5,
                base_cringe_resistance_bonus=5,
                base_drip_bonus=10
            ),
            ChadClass(
                name='Grindset',
                description='The hustler. Balanced stats.',
                base_clout_bonus=7,
                base_roast_bonus=7,
                base_cringe_resistance_bonus=7,
                base_drip_bonus=7
            )
        ]
        db.session.add_all(chad_classes)
        db.session.commit()
        
        # Create a demo user with X twitter mock data
        demo_user = User(
            x_id='demo_user_id',
            x_username='demo_user',
            x_displayname='Demo User',
            x_profile_image='https://example.com/profile.jpg',
            chadcoin_balance=1000
        )
        db.session.add(demo_user)
        db.session.commit()
        
        # Create a demo chad character
        demo_chad = Chad(
            user_id=demo_user.id,
            class_id=chad_classes[0].id,
            clout=10,
            roast_level=15,
            cringe_resistance=12,
            drip_factor=8,
            level=5,
            xp=250
        )
        db.session.add(demo_chad)
        db.session.commit()
        
        # Create waifu rarities
        rarities = [
            WaifuRarity(name='Common', description='Common waifu', drop_rate=0.7, min_stat_bonus=1, max_stat_bonus=3),
            WaifuRarity(name='Uncommon', description='Uncommon waifu', drop_rate=0.3, min_stat_bonus=2, max_stat_bonus=5),
            WaifuRarity(name='Rare', description='Rare waifu', drop_rate=0.1, min_stat_bonus=4, max_stat_bonus=8),
            WaifuRarity(name='Epic', description='Epic waifu', drop_rate=0.03, min_stat_bonus=6, max_stat_bonus=12),
            WaifuRarity(name='Legendary', description='Legendary waifu', drop_rate=0.01, min_stat_bonus=10, max_stat_bonus=20)
        ]
        db.session.add_all(rarities)
        db.session.commit()
        
        # Create waifu types
        waifu_types = [
            WaifuType(
                name='Tsundere',
                description='Hot and cold personality',
                rarity_id=rarities[1].id,
                base_clout_bonus=2,
                base_roast_bonus=5,
                base_cringe_resistance_bonus=2,
                base_drip_bonus=1
            ),
            WaifuType(
                name='Gamer Girl',
                description='Loves gaming',
                rarity_id=rarities[0].id,
                base_clout_bonus=1,
                base_roast_bonus=2,
                base_cringe_resistance_bonus=4,
                base_drip_bonus=2
            ),
            WaifuType(
                name='Cyberpunk',
                description='Futuristic aesthetic',
                rarity_id=rarities[2].id,
                base_clout_bonus=3,
                base_roast_bonus=3,
                base_cringe_resistance_bonus=3,
                base_drip_bonus=6
            )
        ]
        db.session.add_all(waifu_types)
        db.session.commit()
        
        # Give some waifus to the demo user
        demo_waifus = [
            Waifu(
                user_id=demo_user.id,
                chad_id=demo_chad.id,
                type_id=waifu_types[0].id,
                level=3,
                is_equipped=True
            ),
            Waifu(
                user_id=demo_user.id,
                chad_id=demo_chad.id,
                type_id=waifu_types[1].id,
                level=2
            )
        ]
        db.session.add_all(demo_waifus)
        db.session.commit()
        
        # Create item rarities and types
        item_rarities = [
            ItemRarity(name='Common', description='Common item', drop_rate=0.7, min_stat_bonus=1, max_stat_bonus=3),
            ItemRarity(name='Uncommon', description='Uncommon item', drop_rate=0.3, min_stat_bonus=2, max_stat_bonus=5),
            ItemRarity(name='Rare', description='Rare item', drop_rate=0.1, min_stat_bonus=4, max_stat_bonus=8),
            ItemRarity(name='Epic', description='Epic item', drop_rate=0.03, min_stat_bonus=6, max_stat_bonus=12),
            ItemRarity(name='Legendary', description='Legendary item', drop_rate=0.01, min_stat_bonus=10, max_stat_bonus=20)
        ]
        db.session.add_all(item_rarities)
        db.session.commit()
        
        # Create locations
        locations = [
            Location(
                name='Starter Village',
                description='The starting village for all chads',
                location_type=LocationType.STARTER.value,
                min_level=1,
                enemy_level_min=1,
                enemy_level_max=3
            ),
            Location(
                name='Gym Fields',
                description='Open fields with weak enemies',
                location_type=LocationType.FIELD.value,
                min_level=3,
                enemy_level_min=3,
                enemy_level_max=6
            ),
            Location(
                name='Dark Web Dungeon',
                description='A dangerous dungeon',
                location_type=LocationType.DUNGEON.value,
                min_level=10,
                enemy_level_min=10,
                enemy_level_max=15
            )
        ]
        db.session.add_all(locations)
        db.session.commit()
        
        # Connect locations
        locations[0].connected_locations = str(locations[1].id)
        locations[1].connected_locations = f"{locations[0].id},{locations[2].id}"
        locations[2].connected_locations = str(locations[1].id)
        db.session.commit()
        
        # Create enemies
        enemies = [
            PVEEnemy(
                name='Noob',
                description='A weak enemy',
                enemy_type=EnemyType.BASIC.value,
                level=1,
                base_power=50,
                base_hp=100,
                attack_power=10,
                defense=5,
                speed=5,
                location_id=locations[0].id
            ),
            PVEEnemy(
                name='Keyboard Warrior',
                description='A mid-level enemy',
                enemy_type=EnemyType.ELITE.value,
                level=5,
                base_power=150,
                base_hp=300,
                attack_power=30,
                defense=15,
                speed=10,
                location_id=locations[1].id
            ),
            PVEEnemy(
                name='Hacker Boss',
                description='A powerful boss',
                enemy_type=EnemyType.BOSS.value,
                level=12,
                base_power=500,
                base_hp=1000,
                attack_power=100,
                defense=50,
                speed=20,
                location_id=locations[2].id
            )
        ]
        db.session.add_all(enemies)
        db.session.commit()
        
        print("Demo data setup complete!")

if __name__ == '__main__':
    setup_demo_data()
""")
    
    # Run the script to populate demo data
    return run_command([sys.executable, "setup_demo_data.py"])

def run_server():
    """Run the Flask development server."""
    print_step("Starting the Flask server")
    
    # Check if the app directory exists
    if not os.path.exists("app"):
        print("Error: 'app' directory not found. Make sure you're in the ChadBattles directory.")
        return False
    
    # Open browser
    print("Opening web browser...")
    webbrowser.open("http://127.0.0.1:5000")
    
    # Run the Flask server
    print("Starting Flask server...")
    os.environ["FLASK_APP"] = "app"
    os.environ["FLASK_ENV"] = "development"
    return run_command([sys.executable, "-m", "flask", "run", "--debugger", "--reload"])

def main():
    """Main setup function."""
    print("""
===============================================================================
                          CHAD BATTLES SETUP SCRIPT                            
===============================================================================

This script will set up everything you need to run Chad Battles:
1. Create and activate a virtual environment
2. Install required dependencies
3. Set up the database
4. Set up demo data
5. Start the game server

The game will open in your web browser automatically.
""")
    
    if "--continue" not in sys.argv:
        # First, set up the virtual environment
        next_command = setup_virtual_env()
        if isinstance(next_command, str):
            print(f"\nNow run: {next_command}")
            return
        
    # Continue with setup in the activated environment
    if not install_dependencies():
        print("Failed to install dependencies.")
        return
    
    if not setup_database():
        print("Failed to set up database.")
        return
    
    if not setup_demo_data():
        print("Failed to set up demo data.")
        return
    
    # Run the server
    if not run_server():
        print("Failed to start the server.")
        return

if __name__ == "__main__":
    main() 