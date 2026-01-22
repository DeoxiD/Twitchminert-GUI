#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitchminert-GUI - Advanced GUI Control Panel for Twitchminert
Main Flask Application with OAuth2 Integration
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path
import logging
from functools import wraps

# Import local modules
from config import config
from models import db
from core.auth import TwitchAuthManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global auth manager instance
auth_manager = None

def require_json(f):
    """Decorator to validate JSON content type"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return jsonify({'status': 'error', 'message': 'Content-Type must be application/json'}), 400
        return f(*args, **kwargs)
    return decorated


def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__, template_folder='web/templates', static_folder='web/static')    
    # Load configuration
    app.config.from_object(config.get(config_name, config['default']))
    
    # Ensure required config values exist
    app.config.setdefault('SECRET_KEY', os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'))
    app.config.setdefault('TWITCH_CLIENT_ID', os.environ.get('TWITCH_CLIENT_ID', ''))
    app.config.setdefault('TWITCH_CLIENT_SECRET', os.environ.get('TWITCH_CLIENT_SECRET', ''))
    app.config.setdefault('TWITCH_REDIRECT_URI', os.environ.get('TWITCH_REDIRECT_URI', 'http://localhost:5000/auth/callback'))
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Initialize OAuth manager
    global auth_manager
    data_dir = Path.cwd() / 'data'
    data_dir.mkdir(exist_ok=True)
    
    auth_manager = TwitchAuthManager(
        client_id=app.config['TWITCH_CLIENT_ID'],
        client_secret=app.config['TWITCH_CLIENT_SECRET'],
        redirect_uri=app.config['TWITCH_REDIRECT_URI'],
        data_dir=data_dir
    )
    
    # Try to load existing session
    auth_manager.load_session()
    
    # Create database tables
    with app.app_context():
        try:
                db.create_all()
                logger.info("Database tables created successfully")
        except Exception as e:
                logger.warning(f"Database tables may already exist: {e}")    # Register routes   
    # Register routes
    register_api_routes(app)
    register_auth_routes(app)
    register_web_routes(app)
    
    return app


def register_api_routes(app):
    """Register API endpoints"""
    
    @app.route('/api/config', methods=['GET'])
    def get_config():
        """Get configuration"""
        if not auth_manager.is_authenticated():
            return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
        
        try:
            return jsonify({'status': 'success', 'message': 'Configuration retrieved'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/config', methods=['POST'])
    def save_config():
        """Save configuration"""
        if not auth_manager.is_authenticated():
            return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
        
        try:
            data = request.get_json()
            return jsonify({'status': 'success', 'message': 'Configuration saved'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/streamers', methods=['GET'])
    def get_streamers():
        """Get streamers list"""
        if not auth_manager.is_authenticated():
            return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
        
        try:
            return jsonify({'status': 'success', 'streamers': []}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/streamers', methods=['POST'])
    def add_streamer():
        """Add new streamer"""
        if not auth_manager.is_authenticated():
            return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
        
        try:
            data = request.get_json()
            return jsonify({'status': 'success', 'message': 'Streamer added'}), 201
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/dashboard', methods=['GET'])
    def get_dashboard():
        """Get dashboard data"""
        if not auth_manager.is_authenticated():
            return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
        
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
    
    @app.route('/api/user', methods=['GET'])
    def get_user():
        """Get authenticated user information"""
        if not auth_manager.is_authenticated():
            return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
        
        try:
            user_info = auth_manager.get_user_info()
            if user_info:
                return jsonify({
                    'status': 'success',
                    'user': user_info
                }), 200
            else:
                return jsonify({'status': 'error', 'message': 'Failed to get user info'}), 500
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/status', methods=['GET'])
    def get_status():
        """System status endpoint"""
        try:
            return jsonify({
                'status': 'online',
                'version': '2.0.0',
                'authenticated': auth_manager.is_authenticated()
            }), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500


def register_auth_routes(app):
    """Register authentication routes"""
    
    @app.route('/auth/login', methods=['GET'])
    def login():
        """Initiate OAuth2 login flow"""
        try:
            # Check if already authenticated
            if auth_manager.is_authenticated():
                return redirect('/')
            
            # Get OAuth authorization URL
            auth_url = auth_manager.get_auth_url()
            return redirect(auth_url)
        except Exception as e:
            logger.error(f'Login error: {str(e)}')
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/auth/callback', methods=['GET'])
    def auth_callback():
        """Handle OAuth2 callback"""
        try:
            code = request.args.get('code')
            state = request.args.get('state')
            error = request.args.get('error')
            
            if error:
                logger.error(f'OAuth error: {error}')
                return render_template('index.html', error='Authentication failed')
            
            if not code or not state:
                return render_template('index.html', error='Invalid callback parameters')
            
            # Exchange code for tokens
            if auth_manager.handle_callback(code, state):
                session['authenticated'] = True
                logger.info('OAuth authentication successful')
                return redirect('/')
            else:
                return render_template('index.html', error='Failed to authenticate')
        except Exception as e:
            logger.error(f'Callback error: {str(e)}')
            return render_template('index.html', error='Authentication error')
    
    @app.route('/auth/logout', methods=['GET', 'POST'])
    def logout():
        """Logout and revoke tokens"""
        try:
            auth_manager.revoke_token()
            session.clear()
            logger.info('User logged out')
            return redirect('/')
        except Exception as e:
            logger.error(f'Logout error: {str(e)}')
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/auth/status', methods=['GET'])
    def auth_status():
        """Check authentication status"""
        return jsonify({
            'authenticated': auth_manager.is_authenticated()
        }), 200


def register_web_routes(app):
    """Register web page routes"""
    
    @app.route('/', methods=['GET'])
    def index():
        """Main page"""
        try:
            authenticated = auth_manager.is_authenticated()
            user_info = None
            
            if authenticated:
                user_info = auth_manager.get_user_info()
            
            return render_template('index.html', 
                                 authenticated=authenticated, 
                                 user=user_info)
        except Exception as e:
            logger.error(f'Error loading index: {str(e)}')
            return render_template('index.html', error=str(e))
    
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
