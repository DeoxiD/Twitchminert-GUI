import hashlib
import hmac
import json
from datetime import datetime, timedelta
from functools import wraps
from flask import current_app, request, jsonify
import aiohttp
import asyncio

def generate_secret_hash(username, client_id, client_secret):
    """Generate secret hash for Twitch API"""
    message = bytes(username + client_id, 'utf-8')
    secret = bytes(client_secret, 'utf-8')
    secret_hash = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return secret_hash

def validate_token(token):
    """Validate JWT token"""
    try:
        import jwt
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except Exception as e:
        return None

def token_required(f):
    """Decorator to require valid token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        payload = validate_token(token)
        if not payload:
            return jsonify({'message': 'Invalid token'}), 401
        
        request.user_id = payload.get('user_id')
        return f(*args, **kwargs)
    return decorated_function

async def fetch_twitch_api(url, headers, method='GET', json_data=None):
    """Async Twitch API request"""
    async with aiohttp.ClientSession() as session:
        try:
            if method == 'GET':
                async with session.get(url, headers=headers) as resp:
                    return await resp.json()
            elif method == 'POST':
                async with session.post(url, headers=headers, json=json_data) as resp:
                    return await resp.json()
        except Exception as e:
            current_app.logger.error(f'Twitch API error: {str(e)}')
            return None

def get_twitch_headers():
    """Get Twitch API headers"""
    return {
        'Client-ID': current_app.config.get('TWITCH_CLIENT_ID'),
        'Authorization': f"Bearer {current_app.config.get('TWITCH_CLIENT_SECRET')}"
    }

async def send_notification(notification_type, data):
    """Send notification to Discord/Telegram"""
    try:
        if notification_type == 'discord':
            webhook_url = current_app.config.get('DISCORD_WEBHOOK_URL')
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    await session.post(webhook_url, json=data)
        elif notification_type == 'telegram':
            # Telegram implementation
            pass
    except Exception as e:
        current_app.logger.error(f'Notification error: {str(e)}')

def format_time_ago(date_obj):
    """Format time difference"""
    if not date_obj:
        return 'Unknown'
    
    diff = datetime.utcnow() - date_obj
    if diff.days > 0:
        return f'{diff.days}d ago'
    elif diff.seconds > 3600:
        return f'{diff.seconds // 3600}h ago'
    elif diff.seconds > 60:
        return f'{diff.seconds // 60}m ago'
    else:
        return 'just now'

def safe_dict_get(data, path, default=None):
    """Safely get nested dict values"""
    keys = path.split('.')
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        else:
            return default
    return data if data is not None else default
