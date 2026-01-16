from flask import render_template, jsonify, request
from . import app
from datetime import datetime


# Dashboard route - Main page
@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html')


# Settings page
@app.route('/settings')
def settings():
    """Render the settings page"""
    return render_template('settings.html')


# Logs page
@app.route('/logs')
def logs():
    """Render the logs page"""
    return render_template('logs.html')


# API: Get status
@app.route('/api/status')
def get_status():
    """Get miner status"""
    return jsonify({
        'status': 'running',
        'uptime': '2 hours',
        'points_earned': 1250,
        'last_update': datetime.now().isoformat()
    })


# API: Get configuration
@app.route('/api/config', methods=['GET', 'POST'])
def config():
    """Get or update configuration"""
    if request.method == 'POST':
        # Update configuration
        data = request.get_json()
        return jsonify({'success': True, 'message': 'Configuration updated'})
    
    # Get current configuration
    return jsonify({
        'strategy': 'SMART',
        'auto_claim': True,
        'min_odds': 1.5,
        'max_bet': 100
    })


# API: Get streamers
@app.route('/api/streamers')
def get_streamers():
    """Get list of all streamers"""
    return jsonify({
        'streamers': [
            {'id': 1, 'name': 'streamer1', 'status': 'online'},
            {'id': 2, 'name': 'streamer2', 'status': 'offline'}
        ]
    })


# API: Add new streamer
@app.route('/api/streamers', methods=['POST'])
def add_streamer():
    """Add new streamer"""
    data = request.get_json()
    return jsonify({'success': True, 'message': 'Streamer added'})


# API: Start miner
@app.route('/api/start', methods=['POST'])
def start_miner():
    """Start the miner"""
    return jsonify({'success': True, 'message': 'Miner started'})


# API: Stop miner
@app.route('/api/stop', methods=['POST'])
def stop_miner():
    """Stop the miner"""
    return jsonify({'success': True, 'message': 'Miner stopped'})


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Server error'}), 500
