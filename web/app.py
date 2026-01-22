from flask import Flask
from flask_cors import CORS
import os
import logging
from database_operations import DropOps, CampaignOps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask application instance
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

# Error handling middleware
@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request"""
    return {'status': 'error', 'message': 'Bad request'}, 400

@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 Unauthorized"""
    return {'status': 'error', 'message': 'Unauthorized'}, 401

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found"""
    return {'status': 'error', 'message': 'Resource not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error"""
    logger.error(f"Internal server error: {str(error)}")
    return {'status': 'error', 'message': 'Internal server error'}, 500

# Enable CORS for API endpoints
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Import routes after app creation to avoid circular imports
from . import routes

logger.info("Flask web app initialized successfully")
