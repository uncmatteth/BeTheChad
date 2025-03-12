#!/usr/bin/env python3
"""
Chad Battles Application Entry Point
"""

import os
from app import create_app

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Run the application in debug mode
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) 