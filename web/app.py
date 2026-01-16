from flask import Flask
from flask_cors import CORS
import os

# Create Flask application instance
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Enable CORS for API endpoints
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Import routes after app creation to avoid circular imports
from . import routes
