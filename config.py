#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitchminert-GUI Configuration with Real Twitch OAuth Integration
Handles environment loading, token validation, and Twitch API scopes
"""

import os
import secrets
import logging
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import requests

# Setup logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
ENV_PATH = Path(__file__).parent / '.env'
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    logger.warning(f".env file not found at {ENV_PATH}")


class TwitchOAuthValidator:
    """
    Validates Twitch OAuth credentials and tokens
    """
    
    # Required Twitch OAuth scopes for full functionality
    REQUIRED_SCOPES = [
        "analytics:read:extensions",
        "analytics:read:games",
        "bits:read",
        "channel:edit:commercial",
        "channel:manage:broadcast",
        "channel:manage:content_moderation",
        "channel:manage:polls",
        "channel:manage:predictions",
        "channel:manage:raids",
        "channel:manage:redemptions",
        "channel:manage:teams",
        "channel:read:goals",
        "channel:read:hype_train",
        "channel:read:polls",
        "channel:read:predictions",
        "channel:read:stream_key",
        "channel:read:subscriptions",
        "channel:read:teams",
        "clips:edit",
        "moderation:read",
        "user:edit",
        "user:read:email",
        "user:read:follows",
        "user:manage:blocked_users",
    ]
    
    OAUTH_ENDPOINT = "https://id.twitch.tv/oauth2/validate"
    
    @staticmethod
    def validate_credentials(client_id: str, client_secret: str) -> bool:
        """
        Validate Twitch Client ID and Secret format
        """
        if not client_id or not isinstance(client_id, str):
            logger.error("TWITCH_CLIENT_ID not set or invalid")
            return False
        
        if not client_secret or not isinstance(client_secret, str):
            logger.error("TWITCH_CLIENT_SECRET not set or invalid")
            return False
        
        # Twitch Client ID is typically 30 characters
        if len(client_id) < 20:
            logger.warning(f"TWITCH_CLIENT_ID seems too short: {len(client_id)} chars")
        
        # Twitch Client Secret is typically 30+ characters
        if len(client_secret) < 20:
            logger.warning(f"TWITCH_CLIENT_SECRET seems too short: {len(client_secret)} chars")
        
        return True
    
    @staticmethod
    def validate_token(token: str, client_id: str) -> bool:
        """
        Validate Twitch OAuth token with Twitch API
        Real validation using https://id.twitch.tv/oauth2/validate
        """
        if not token:
            return False
        
        try:
            response = requests.get(
                TwitchOAuthValidator.OAUTH_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Client-ID": client_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                expires_in = data.get("expires_in", 0)
                
                if expires_in > 0:
                    logger.info(f"Token is valid. Expires in {expires_in} seconds")
                    return True
                else:
                    logger.warning("Token is expired")
                    return False
            else:
                logger.error(f"Token validation failed: {response.status_code}")
                return False
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Token validation request error: {e}")
            return False


class Config:
    """
    Base configuration for Twitchminert-GUI
    """
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    
    # Flask Settings
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # REAL TWITCH OAUTH CONFIGURATION
    TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID', '')
    TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET', '')
    TWITCH_REDIRECT_URI = os.environ.get('TWITCH_REDIRECT_URI', 'http://localhost:5000/auth/callback')
    TWITCH_GQL_URL = os.environ.get('TWITCH_GQL_URL', 'https://gql.twitch.tv/gql')
    
    # OAuth Scopes
    TWITCH_OAUTH_SCOPES = TwitchOAuthValidator.REQUIRED_SCOPES
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///twitchminert.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = int(os.environ.get('DB_POOL_SIZE', 10))
    SQLALCHEMY_MAX_OVERFLOW = int(os.environ.get('DB_MAX_OVERFLOW', 20))
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/twitchminert.log')
    
    # Mining Configuration
    MINING_INTERVAL = int(os.environ.get('MINING_INTERVAL', 60))
    DROP_CHECK_INTERVAL = int(os.environ.get('DROP_CHECK_INTERVAL', 30))
    POINTS_CHECK_INTERVAL = int(os.environ.get('POINTS_CHECK_INTERVAL', 120))
    WATCH_HEARTBEAT_INTERVAL = int(os.environ.get('WATCH_HEARTBEAT_INTERVAL', 300))
    
    # Auto Features
    AUTO_CLAIM_DROPS = os.environ.get('AUTO_CLAIM_DROPS', 'true').lower() == 'true'
    AUTO_PLACE_BETS = os.environ.get('AUTO_PLACE_BETS', 'false').lower() == 'true'
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = int(os.environ.get('RATE_LIMIT_REQUESTS', 60))
    RATE_LIMIT_WINDOW = int(os.environ.get('RATE_LIMIT_WINDOW', 60))
    RETRY_ATTEMPTS = int(os.environ.get('RETRY_ATTEMPTS', 5))
    RETRY_BACKOFF_FACTOR = float(os.environ.get('RETRY_BACKOFF_FACTOR', 2))
    
    # WebSocket Configuration
    ENABLE_WEBSOCKET = os.environ.get('ENABLE_WEBSOCKET', 'true').lower() == 'true'
    WEBSOCKET_HOST = os.environ.get('WEBSOCKET_HOST', '0.0.0.0')
    WEBSOCKET_PORT = int(os.environ.get('WEBSOCKET_PORT', 5001))
    
    # Data & Cache
    DATA_DIR = Path(os.environ.get('DATA_DIR', './data'))
    DATA_DIR.mkdir(exist_ok=True)
    
    # Session Timeout (minutes)
    SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT', 1440))
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get(
        'CORS_ORIGINS',
        'http://localhost:3000,http://localhost:5000'
    ).split(',')
    
    # Notifications
    DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL', '')
    NOTIFY_DROP_CLAIMED = os.environ.get('NOTIFY_DROP_CLAIMED', 'true').lower() == 'true'
    NOTIFY_ON_ERROR = os.environ.get('NOTIFY_ON_ERROR', 'true').lower() == 'true'
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration on startup
        """
        logger.info("Validating Twitchminert-GUI configuration...")
        
        # Validate Twitch credentials
        if not TwitchOAuthValidator.validate_credentials(cls.TWITCH_CLIENT_ID, cls.TWITCH_CLIENT_SECRET):
            logger.error("Twitch OAuth credentials validation failed")
            return False
        
        logger.info(f"✓ Twitch Client ID: {cls.TWITCH_CLIENT_ID[:10]}...")
        logger.info(f"✓ Twitch Redirect URI: {cls.TWITCH_REDIRECT_URI}")
        logger.info(f"✓ Database URL: {cls.SQLALCHEMY_DATABASE_URI}")
        logger.info(f"✓ Required OAuth Scopes: {len(cls.TWITCH_OAUTH_SCOPES)} scopes")
        logger.info("✓ Configuration validation successful")
        
        return True


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


# Initialize configuration on module load
if __name__ == '__main__':
    # Test configuration
    cfg = Config()
    if cfg.validate():
        print("\n✓ Configuration is valid and ready for use")
    else:
        print("\n✗ Configuration validation failed")
        exit(1)
