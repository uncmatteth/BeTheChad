"""
Script to register the music blueprint in the Flask application.
Run this script to update the __init__.py file.
"""

import os
import re

# Path to the app/__init__.py file
INIT_FILE = os.path.join('app', '__init__.py')

def register_music_blueprint():
    """
    Add the music blueprint import and registration to the __init__.py file
    """
    if not os.path.exists(INIT_FILE):
        print(f"Error: {INIT_FILE} not found.")
        return False
    
    with open(INIT_FILE, 'r') as f:
        content = f.read()
    
    # Check if music blueprint is already registered
    if 'from app.routes.music import music' in content:
        print("Music blueprint already registered.")
        return True
    
    # Add import for music blueprint
    import_pattern = re.compile(r'# Import route blueprints.*?\n', re.DOTALL)
    if import_pattern.search(content):
        new_imports = import_pattern.search(content).group(0)
        new_imports += 'from app.routes.music import music\n'
        content = import_pattern.sub(new_imports, content)
    else:
        # If no import pattern found, add imports before create_app function
        create_app_pattern = re.compile(r'def create_app.*?:', re.DOTALL)
        if create_app_pattern.search(content):
            imports = 'from app.routes.music import music\n\n'
            content = create_app_pattern.sub(imports + create_app_pattern.search(content).group(0), content)
    
    # Add blueprint registration
    register_pattern = re.compile(r'# Register blueprints.*?\n', re.DOTALL)
    if register_pattern.search(content):
        new_registrations = register_pattern.search(content).group(0)
        new_registrations += '    app.register_blueprint(music, url_prefix="/music")\n'
        content = register_pattern.sub(new_registrations, content)
    else:
        # If no register pattern found, add registration after app creation
        app_creation_pattern = re.compile(r'app = Flask.*?\n', re.DOTALL)
        if app_creation_pattern.search(content):
            registration = '\n    # Register music blueprint\n    app.register_blueprint(music, url_prefix="/music")\n'
            content = app_creation_pattern.sub(app_creation_pattern.search(content).group(0) + registration, content)
    
    # Write updated content back to file
    with open(INIT_FILE, 'w') as f:
        f.write(content)
    
    print(f"Music blueprint registered in {INIT_FILE}")
    return True

if __name__ == "__main__":
    register_music_blueprint() 