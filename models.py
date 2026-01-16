from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Configuration(db.Model):
    """Configuration model for storing user settings"""
    __tablename__ = 'configurations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False, default='Default')
    config_data = db.Column(db.JSON, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'config_data': self.config_data,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Streamer(db.Model):
    """Streamer model"""
    __tablename__ = 'streamers'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    twitch_id = db.Column(db.String(255), unique=True)
    display_name = db.Column(db.String(255))
    profile_image_url = db.Column(db.String(500))
    is_online = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'twitch_id': self.twitch_id,
            'display_name': self.display_name,
            'profile_image_url': self.profile_image_url,
            'is_online': self.is_online
        }

class BettingActivity(db.Model):
    """Betting activity log"""
    __tablename__ = 'betting_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    streamer_id = db.Column(db.Integer, db.ForeignKey('streamers.id'))
    points_bet = db.Column(db.Integer)
    outcome = db.Column(db.String(50))  # WIN, LOSE, PENDING
    points_won = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    streamer = db.relationship('Streamer', backref='betting_activities')
    
    def to_dict(self):
        return {
            'id': self.id,
            'streamer_id': self.streamer_id,
            'points_bet': self.points_bet,
            'outcome': self.outcome,
            'points_won': self.points_won,
            'created_at': self.created_at.isoformat()
        }

class DropsCampaign(db.Model):
    """Twitch drops campaign"""
    __tablename__ = 'drops_campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.String(255), unique=True, nullable=False)
    campaign_name = db.Column(db.String(255))
    game_name = db.Column(db.String(255))
    status = db.Column(db.String(50))  # ACTIVE, PENDING, EXPIRED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'campaign_name': self.campaign_name,
            'game_name': self.game_name,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Session(db.Model):
    """Session tracking"""
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_key = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.String(255))
    total_points_earned = db.Column(db.Integer, default=0)
    total_bets = db.Column(db.Integer, default=0)
    winning_bets = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_key': self.session_key,
            'user_id': self.user_id,
            'total_points_earned': self.total_points_earned,
            'total_bets': self.total_bets,
            'winning_bets': self.winning_bets,
            'started_at': self.started_at.isoformat(),
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'is_active': self.is_active
        }
