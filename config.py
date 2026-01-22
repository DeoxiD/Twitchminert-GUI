import os
import secrets
from datetime import timedelta


class Config:
    """Base configuration"""
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Twitch API Configuration
    TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID', '')
    TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET', '')
    TWITCH_REDIRECT_URI = os.environ.get('TWITCH_REDIRECT_URI', 'http://localhost:5000/auth/callback')
    TWITCH_GQL_URL = os.environ.get('TWITCH_GQL_URL', 'https://gql.twitch.tv/gql')
    
    # Notifications Configuration
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
    DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL', '')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///twitchminert.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.environ.get('DB_POOL_SIZE', 10)),
        'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', 3600)),
        'pool_pre_ping': True,
    }
    
    # Rate Limiting Configuration
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = '100/hour'
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    CORS_CREDENTIALS = True
    
    # Upload Configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(os.path.dirname(__file__), 'uploads'))
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_UPLOAD_SIZE', 16 * 1024 * 1024))
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'json', 'csv'}
    
    # Application Configuration
    ITEMS_PER_PAGE = 20
    JSON_SORT_KEYS = False
    PREFERRED_URL_SCHEME = 'https'
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False
    PREFERRED_URL_SCHEME = 'http'
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000', 'http://127.0.0.1:3000']


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    def __init__(self):
        super().__init__()
        # Validate production settings
        if self.SECRET_KEY.startswith('dev-secret-key'):
            raise ValueError('⚠️  Production SECRET_KEY must be set via environment variable!')
        if not self.TWITCH_CLIENT_ID:
            raise ValueError('⚠️  TWITCH_CLIENT_ID environment variable is required!')
        if not self.TWITCH_CLIENT_SECRET:
            raise ValueError('⚠️  TWITCH_CLIENT_SECRET environment variable is required!')
        if any('localhost' in origin for origin in self.CORS_ORIGINS):
            raise ValueError('⚠️  Production CORS_ORIGINS cannot include localhost!')


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
