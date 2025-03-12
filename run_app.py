#!/usr/bin/env python
"""
Simple script to run the Chad Battles application
"""

import os
from app import create_app

# Create the application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    print("Starting Chad Battles application...")
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000) 