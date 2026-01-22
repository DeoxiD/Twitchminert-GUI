#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Twitchminert-GUI Database Models
Handles User tokens, Twitch drops, campaigns, and channel statistics
"""

from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, UniqueConstraint, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
import logging

logger = logging.getLogger(__name__)

# SQLAlchemy instance
db = SQLAlchemy()


class User(db.Model):
    """
    User model with real Twitch OAuth tokens and credentials
    """
    __tablename__ = 'users'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Real Twitch user identification
    twitch_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    twitch_login = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    profile_image_url = db.Column(db.Text, nullable=True)
    
    # Real OAuth tokens
    access_token = db.Column(db.Text, nullable=False)  # Refresh-able bearer token
    refresh_token = db.Column(db.Text, nullable=True)  # Token refresh
    token_expires_at = db.Column(db.DateTime, nullable=False)
    
    # Email and user info
    email = db.Column(db.String(255), nullable=True, index=True)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_mining = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sessions = relationship('StreamingSession', backref='user', lazy=True, cascade='all, delete-orphan')
    drops_earned = relationship('Drop', backref='user', lazy=True, cascade='all, delete-orphan')
    channel_stats = relationship('ChannelStats', backref='user', lazy=True, cascade='all, delete-orphan')
    tracked_campaigns = relationship('Campaign', backref='tracked_by_user', lazy=True, secondary='user_campaign')
    
    # Real index for Twitch ID lookups
    __table_args__ = (
        Index('idx_twitch_id', 'twitch_id'),
        Index('idx_twitch_login', 'twitch_login'),
        Index('idx_is_active', 'is_active'),
        UniqueConstraint('twitch_id', name='uq_twitch_id'),
    )
    
    def is_token_expired(self) -> bool:
        """Check if OAuth token is expired"""
        return datetime.utcnow() >= self.token_expires_at
    
    def needs_token_refresh(self) -> bool:
        """Check if token needs refresh (within 1 hour of expiry)"""
        return datetime.utcnow() >= (self.token_expires_at - timedelta(hours=1))
    
    def __repr__(self):
        return f'<User {self.twitch_login} (ID: {self.twitch_id})>'


class Campaign(db.Model):
    """
    Real Twitch drop campaigns with game and channel info
    """
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Real Twitch campaign identification
    twitch_campaign_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    campaign_title = db.Column(db.String(255), nullable=False)
    
    # Game info
    game_id = db.Column(db.String(50), nullable=False, index=True)
    game_name = db.Column(db.String(100), nullable=False)
    
    # Campaign details
    image_url = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    # Campaign status and timing
    status = db.Column(db.String(50), default='ACTIVE', index=True)  # ACTIVE, ENDED, UPCOMING
    start_date = db.Column(db.DateTime, nullable=False, index=True)
    end_date = db.Column(db.DateTime, nullable=False, index=True)
    
    # Channels involved (JSON array of channel IDs)
    channel_ids = db.Column(JSON, nullable=False, default=[])  # List of participating channels
    
    # Campaign drops count
    total_drops = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    drops = relationship('Drop', backref='campaign', lazy=True, cascade='all, delete-orphan')
    
    # Real indexes for campaign lookups
    __table_args__ = (
        Index('idx_twitch_campaign_id', 'twitch_campaign_id'),
        Index('idx_game_id', 'game_id'),
        Index('idx_campaign_status', 'status'),
        Index('idx_campaign_dates', 'start_date', 'end_date'),
    )
    
    def is_active(self) -> bool:
        """Check if campaign is currently active"""
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date and self.status == 'ACTIVE'
    
    def __repr__(self):
        return f'<Campaign {self.campaign_title} (ID: {self.twitch_campaign_id})>'


class Drop(db.Model):
    """
    Real Twitch drops with claim status and Twitch drop IDs
    """
    __tablename__ = 'drops'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Real Twitch drop identification
    twitch_drop_id = db.Column(db.String(100), unique=True, nullable=False, index=True)  # Real Twitch ID
    entitlement_id = db.Column(db.String(100), nullable=True, index=True)  # Entitlement ID
    
    # Drop details
    drop_name = db.Column(db.String(255), nullable=False)
    drop_value = db.Column(db.String(100), nullable=True)  # e.g., "Prime Gaming Loot"
    
    # Campaign and game info
    campaign_id = db.Column(db.Integer, ForeignKey('campaigns.id'), nullable=False, index=True)
    
    # User who earned drop
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Drop claim status
    is_claimed = db.Column(db.Boolean, default=False, index=True)
    is_claimable = db.Column(db.Boolean, default=False, index=True)
    
    # Required watch time and actual watch time
    required_minutes_watched = db.Column(db.Integer, default=0)
    minutes_watched = db.Column(db.Integer, default=0)
    
    # Drop timing
    drop_available_at = db.Column(db.DateTime, nullable=False, index=True)
    drop_expires_at = db.Column(db.DateTime, nullable=False, index=True)
    
    # Claim information
    claimed_at = db.Column(db.DateTime, nullable=True, index=True)
    claim_error = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Real indexes for drop lookups
    __table_args__ = (
        Index('idx_twitch_drop_id', 'twitch_drop_id'),
        Index('idx_entitlement_id', 'entitlement_id'),
        Index('idx_user_drop', 'user_id', 'twitch_drop_id'),
        Index('idx_is_claimed', 'is_claimed'),
        Index('idx_is_claimable', 'is_claimable'),
        Index('idx_drop_dates', 'drop_available_at', 'drop_expires_at'),
        UniqueConstraint('twitch_drop_id', name='uq_twitch_drop_id'),
    )
    
    def can_claim(self) -> bool:
        """Check if drop can be claimed"""
        now = datetime.utcnow()
        return (
            not self.is_claimed and
            self.is_claimable and
            self.drop_available_at <= now <= self.drop_expires_at and
            self.minutes_watched >= self.required_minutes_watched
        )
    
    def is_expired(self) -> bool:
        """Check if drop is expired"""
        return datetime.utcnow() > self.drop_expires_at
    
    def __repr__(self):
        return f'<Drop {self.drop_name} (ID: {self.twitch_drop_id})>'


class StreamingSession(db.Model):
    """
    Track streaming sessions for watching drops
    """
    __tablename__ = 'streaming_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Channel being watched
    channel_id = db.Column(db.String(50), nullable=False, index=True)
    channel_name = db.Column(db.String(100), nullable=False)
    
    # Session timing
    started_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ended_at = db.Column(db.DateTime, nullable=True)
    
    # Watch time tracking (in minutes)
    total_minutes_watched = db.Column(db.Integer, default=0)
    
    # Drops earned during session
    drops_earned = db.Column(db.Integer, default=0)
    
    # Session status
    is_active = db.Column(db.Boolean, default=True, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_user_session', 'user_id', 'started_at'),
        Index('idx_channel_session', 'channel_id', 'started_at'),
    )
    
    def get_duration(self) -> timedelta:
        """Get session duration"""
        end = self.ended_at or datetime.utcnow()
        return end - self.started_at
    
    def __repr__(self):
        return f'<StreamingSession user={self.user_id} channel={self.channel_name}>'


class ChannelStats(db.Model):
    """
    Track channel-specific statistics
    """
    __tablename__ = 'channel_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Channel identification
    channel_id = db.Column(db.String(50), nullable=False, index=True)
    channel_name = db.Column(db.String(100), nullable=False)
    
    # Statistics
    total_drops_available = db.Column(db.Integer, default=0)
    total_drops_claimed = db.Column(db.Integer, default=0)
    total_watch_time_minutes = db.Column(db.Integer, default=0)
    
    # Points tracking
    channel_points_balance = db.Column(db.Integer, default=0)
    channel_points_earned = db.Column(db.Integer, default=0)
    
    # Last checked
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'channel_id', name='uq_user_channel'),
        Index('idx_user_channel', 'user_id', 'channel_id'),
    )
    
    def __repr__(self):
        return f'<ChannelStats user={self.user_id} channel={self.channel_name}>'


# User-Campaign association (many-to-many)
user_campaign = db.Table(
    'user_campaign',
    db.Column('user_id', db.Integer, ForeignKey('users.id'), primary_key=True),
    db.Column('campaign_id', db.Integer, ForeignKey('campaigns.id'), primary_key=True),
    db.Column('tracked_at', db.DateTime, default=datetime.utcnow),
    Index('idx_user_campaign', 'user_id', 'campaign_id'),
)


if __name__ == '__main__':
    logger.info("Database models defined successfully")
