#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitchminert-GUI - Advanced GUI Control Panel for Twitchminert
Main Flask Application
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Import local modules
from config import config
from models import db
from utils import token_required

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Load configuration
    app.config.from_object(config.get(config_name, config['default']))
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    JWTManager(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    register_blueprints(app)
    register_routes(app)
    
    return app

def register_blueprints(app):
    """Register Flask blueprints"""
    # Configuration endpoints
    @app.route('/api/config', methods=['GET'])
    @token_required
    def get_config():
        try:
            return jsonify({'status': 'success', 'message': 'Configuration retrieved'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/config', methods=['POST'])
    @token_required
    def save_config():
        try:
            data = request.get_json()
            return jsonify({'status': 'success', 'message': 'Configuration saved'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    # Streamer endpoints
    @app.route('/api/streamers', methods=['GET'])
    @token_required
    def get_streamers():
        try:
            return jsonify({'status': 'success', 'streamers': []}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/streamers', methods=['POST'])
    @token_required
    def add_streamer():
        try:
            data = request.get_json()
            return jsonify({'status': 'success', 'message': 'Streamer added'}), 201
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    # Dashboard endpoint
    @app.route('/api/dashboard', methods=['GET'])
    @token_required
    def get_dashboard():
        try:
            dashboard_data = {
                'status': 'success',
                'active_streamers': 0,
                'total_points': 0,
                'bets_placed': 0,
                'wins': 0,
                'recent_activities': []
            }
            return jsonify(dashboard_data), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    # Status endpoint
    @app.route('/api/status', methods=['GET'])
    def get_status():
        try:
            return jsonify({'status': 'online', 'version': '2.0.0'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

def register_routes(app):
    """Register main routes"""
    
    @app.route('/', methods=['GET'])
    def index():
        """Main page"""
        try:
            return render_template('index.html')
        except Exception as e:
            logger.error(f'Error loading index: {str(e)}')
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/auth/login', methods=['POST'])
    def login():
        """User login endpoint"""
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            # TODO: Implement actual authentication
            if username and password:
                access_token = create_access_token(identity=username)
                session['user_id'] = username
                return jsonify({
                    'status': 'success',
                    'access_token': access_token,
                    'message': 'Login successful'
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid credentials'
                }), 401
        except Exception as e:
            logger.error(f'Login error: {str(e)}')
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/auth/logout', methods=['POST'])
    def logout():
        """User logout endpoint"""
        try:
            session.clear()
            return jsonify({
                'status': 'success',
                'message': 'Logout successful'
            }), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '2.0.0'
        }), 200
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'status': 'error', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal server error: {str(error)}')
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get configuration from environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Create application
    app = create_app(env)
    
    # Run development server
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=(env == 'development')
    )
