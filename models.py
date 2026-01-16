#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLAlchemy database models with complete CRUD support
"""
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Index, event
import json

db = SQLAlchemy()

# ==================== Configuration Model ====================

class Configuration(db.Model):
    """Configuration model for storing user settings"""
    __tablename__ = 'configurations'
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_is_active', 'is_active'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False, default='Default')
    config_data = db.Column(db.JSON, nullable=False)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('Session', backref='configuration', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'config_data': self.config_data,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Configuration {self.user_id}>'

# ==================== Streamer Model ====================

class Streamer(db.Model):
    """Streamer model with enhanced tracking"""
    __tablename__ = 'streamers'
    __table_args__ = (
        Index('idx_username', 'username'),
        Index('idx_twitch_id', 'twitch_id'),
        Index('idx_is_online', 'is_online'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False, index=True)
    twitch_id = db.Column(db.String(255), unique=True, index=True)
    display_name = db.Column(db.String(255))
    profile_image_url = db.Column(db.String(500))
    is_online = db.Column(db.Boolean, default=False, index=True)
    followers_count = db.Column(db.Integer, default=0)
    game_name = db.Column(db.String(255))
    last_seen = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    betting_activities = db.relationship('BettingActivity', backref='streamer', lazy='dynamic', cascade='all, delete-orphan')
    drops_campaigns = db.relationship('DropsCampaign', secondary='streamer_campaigns', backref='streamers')
    
    @hybrid_property
    def total_bets_count(self):
        return db.session.query(BettingActivity).filter_by(streamer_id=self.id).count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'twitch_id': self.twitch_id,
            'display_name': self.display_name,
            'profile_image_url': self.profile_image_url,
            'is_online': self.is_online,
            'followers_count': self.followers_count,
            'game_name': self.game_name,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'total_bets': self.total_bets_count
        }
    
    def __repr__(self):
        return f'<Streamer {self.username}>'

# ==================== Betting Activity Model ====================

class BettingActivity(db.Model):
    """Betting activity log with enhanced tracking"""
    __tablename__ = 'betting_activities'
    __table_args__ = (
        Index('idx_streamer_id', 'streamer_id'),
        Index('idx_outcome', 'outcome'),
        Index('idx_created_at', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    streamer_id = db.Column(db.Integer, db.ForeignKey('streamers.id'), nullable=False, index=True)
    points_bet = db.Column(db.Integer, nullable=False)
    outcome = db.Column(db.String(50), nullable=False)  # WIN, LOSE, PENDING, CANCELLED
    points_won = db.Column(db.Integer, default=0)
    bet_type = db.Column(db.String(100))  # CHANNEL_POINTS, DROPS, etc.
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    resolved_at = db.Column(db.DateTime)
    
    @hybrid_property
    def roi(self):
        """Return on investment calculation"""
        if self.points_bet == 0:
            return 0
        return round(((self.points_won - self.points_bet) / self.points_bet) * 100, 2)
    
    @hybrid_property
    def is_resolved(self):
        return self.outcome in ['WIN', 'LOSE', 'CANCELLED']
    
    def to_dict(self):
        return {
            'id': self.id,
            'streamer_id': self.streamer_id,
            'streamer': self.streamer.to_dict() if self.streamer else None,
            'points_bet': self.points_bet,
            'outcome': self.outcome,
            'points_won': self.points_won,
            'roi': self.roi,
            'bet_type': self.bet_type,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }
    
    def __repr__(self):
        return f'<BettingActivity {self.id} - {self.outcome}>'

# ==================== Drops Campaign Model ====================

class DropsCampaign(db.Model):
    """Twitch drops campaign tracking"""
    __tablename__ = 'drops_campaigns'
    __table_args__ = (
        Index('idx_campaign_id', 'campaign_id'),
        Index('idx_status', 'status'),
        Index('idx_game_name', 'game_name'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    campaign_name = db.Column(db.String(255), nullable=False)
    game_name = db.Column(db.String(255), nullable=False, index=True)
    game_id = db.Column(db.String(255))
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='ACTIVE', index=True)  # ACTIVE, PENDING, EXPIRED
    total_rewards = db.Column(db.Integer, default=0)
    claimed_rewards = db.Column(db.Integer, default=0)
    priority = db.Column(db.Integer, default=0)  # Higher priority = watch first
    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    drops = db.relationship('Drop', backref='campaign', lazy='dynamic', cascade='all, delete-orphan')
    mining_sessions = db.relationship('MiningSession', backref='campaign', lazy='dynamic', cascade='all, delete-orphan')
    
    @hybrid_property
    def is_active(self):
        now = datetime.utcnow()
        if self.starts_at and self.ends_at:
            return self.starts_at <= now <= self.ends_at
        return self.status == 'ACTIVE'
    
    @hybrid_property
    def unclaimed_rewards(self):
        return max(0, self.total_rewards - self.claimed_rewards)
    
    @hybrid_property
    def progress_percentage(self):
        if self.total_rewards == 0:
            return 0
        return round((self.claimed_rewards / self.total_rewards) * 100, 2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'campaign_name': self.campaign_name,
            'game_name': self.game_name,
            'game_id': self.game_id,
            'description': self.description,
            'status': self.status,
            'total_rewards': self.total_rewards,
            'claimed_rewards': self.claimed_rewards,
            'unclaimed_rewards': self.unclaimed_rewards,
            'progress_percentage': self.progress_percentage,
            'priority': self.priority,
            'starts_at': self.starts_at.isoformat() if self.starts_at else None,
            'ends_at': self.ends_at.isoformat() if self.ends_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<DropsCampaign {self.game_name}>'

# ==================== Drop Model ====================

class Drop(db.Model):
    """Individual drop tracking"""
    __tablename__ = 'drops'
    __table_args__ = (
        Index('idx_campaign_id', 'campaign_id'),
        Index('idx_status', 'status'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('drops_campaigns.id'), nullable=False, index=True)
    drop_id = db.Column(db.String(255), unique=True, nullable=False)
    reward_name = db.Column(db.String(255), nullable=False)
    reward_description = db.Column(db.Text)
    status = db.Column(db.String(50), default='PENDING')  # PENDING, IN_PROGRESS, CLAIMED, FAILED, EXPIRED
    claimed = db.Column(db.Boolean, default=False)
    claimed_at = db.Column(db.DateTime)
    mining_duration_seconds = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'drop_id': self.drop_id,
            'reward_name': self.reward_name,
            'reward_description': self.reward_description,
            'status': self.status,
            'claimed': self.claimed,
            'claimed_at': self.claimed_at.isoformat() if self.claimed_at else None,
            'mining_duration_seconds': self.mining_duration_seconds,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Drop {self.reward_name}>'

# ==================== Mining Session Model ====================

class MiningSession(db.Model):
    """Mining session tracking with aggregated stats"""
    __tablename__ = 'mining_sessions'
    __table_args__ = (
        Index('idx_campaign_id', 'campaign_id'),
        Index('idx_session_key', 'session_key'),
        Index('idx_started_at', 'started_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    session_key = db.Column(db.String(255), unique=True, nullable=False, index=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('drops_campaigns.id'), nullable=False, index=True)
    user_id = db.Column(db.String(255), nullable=False)
    total_drops_claimed = db.Column(db.Integer, default=0)
    total_drops_attempted = db.Column(db.Integer, default=0)
    total_mining_duration_seconds = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ended_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    @hybrid_property
    def duration_seconds(self):
        end = self.ended_at or datetime.utcnow()
        return int((end - self.started_at).total_seconds())
    
    @hybrid_property
    def success_rate(self):
        if self.total_drops_attempted == 0:
            return 0
        return round((self.total_drops_claimed / self.total_drops_attempted) * 100, 2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_key': self.session_key,
            'campaign_id': self.campaign_id,
            'user_id': self.user_id,
            'total_drops_claimed': self.total_drops_claimed,
            'total_drops_attempted': self.total_drops_attempted,
            'total_mining_duration_seconds': self.total_mining_duration_seconds,
            'success_rate': self.success_rate,
            'duration_seconds': self.duration_seconds,
            'started_at': self.started_at.isoformat(),
            
