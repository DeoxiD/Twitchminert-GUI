#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitchminert-GUI - Startup Script
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Import and run the application
from app import create_app

if __name__ == '__main__':
    # Get configuration from environment
    env = os.environ.get('FLASK_ENV', 'development')
    print(f'Starting Twitchminert-GUI in {env} mode...')
    
    # Create the Flask app
    app = create_app(env)
    
    # Run the development server
    app.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=(env == 'development')
    )
