#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Database Operations for Twitchminert-GUI
Handles user tokens, drops, campaigns with real SQLite indexes
"""

from datetime import datetime, timedelta
from sqlalchemy import and_, or_, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


class DatabaseOperations:
    """
    Real database operations with indexes for Twitch drops and user tokens
    """
    
    def __init__(self, db):
        self.db = db
    
    # ========== USER OPERATIONS ==========
    
    def create_user(self, twitch_id: str, twitch_login: str, display_name: str,
                   access_token: str, refresh_token: str = None,
                   token_expires_at: datetime = None, email: str = None) -> any:
        """
        Create new user with Twitch OAuth tokens
        Uses real indexes on twitch_id and twitch_login
        """
        try:
            from models_real import User
            
            user = User(
                twitch_id=twitch_id,
                twitch_login=twitch_login,
                display_name=display_name,
                access_token=access_token,
                refresh_token=refresh_token,
                token_expires_at=token_expires_at or (datetime.utcnow() + timedelta(hours=4)),
                email=email,
                is_active=True
            )
            
            self.db.session.add(user)
            self.db.session.commit()
            logger.info(f"Created user: {twitch_login} (ID: {twitch_id})")
            return user
        
        except IntegrityError:
            self.db.session.rollback()
            logger.warning(f"User already exists: {twitch_id}")
            return None
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error creating user: {e}")
            return None
    
    def get_user_by_twitch_id(self, twitch_id: str) -> any:
        """
        Fast lookup using real index on twitch_id column
        """
        try:
            from models_real import User
            return User.query.filter_by(twitch_id=twitch_id).first()
        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            return None
    
    def update_user_tokens(self, user_id: int, access_token: str, 
                          refresh_token: str = None, expires_in: int = 3600) -> bool:
        """
        Update OAuth tokens with real token expiration
        """
        try:
            from models_real import User
            
            user = User.query.get(user_id)
            if not user:
                return False
            
            user.access_token = access_token
            if refresh_token:
                user.refresh_token = refresh_token
            user.token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
            user.updated_at = datetime.utcnow()
            
            self.db.session.commit()
            logger.info(f"Updated tokens for user {user_id}")
            return True
        
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error updating tokens: {e}")
            return False
    
    def get_users_needing_token_refresh(self, limit: int = 10) -> list:
        """
        Get users whose tokens need refresh
        Uses index on token_expires_at
        """
        try:
            from models_real import User
            
            # Tokens within 1 hour of expiry
            cutoff_time = datetime.utcnow() + timedelta(hours=1)
            
            users = User.query.filter(
                and_(
                    User.is_active == True,
                    User.token_expires_at <= cutoff_time
                )
            ).limit(limit).all()
            
            return users
        
        except Exception as e:
            logger.error(f"Error retrieving users for refresh: {e}")
            return []
    
    # ========== DROP OPERATIONS ==========
    
    def add_drop(self, twitch_drop_id: str, campaign_id: int, user_id: int,
                drop_name: str, drop_value: str = None, entitlement_id: str = None,
                required_minutes: int = 0, available_at: datetime = None,
                expires_at: datetime = None) -> any:
        """
        Add drop with real Twitch drop ID (indexed)
        """
        try:
            from models_real import Drop
            
            drop = Drop(
                twitch_drop_id=twitch_drop_id,  # Real index
                entitlement_id=entitlement_id,  # Real index
                campaign_id=campaign_id,
                user_id=user_id,  # Composite index with twitch_drop_id
                drop_name=drop_name,
                drop_value=drop_value,
                required_minutes_watched=required_minutes,
                drop_available_at=available_at or datetime.utcnow(),
                drop_expires_at=expires_at or (datetime.utcnow() + timedelta(days=30)),
                is_claimable=False,
                is_claimed=False
            )
            
            self.db.session.add(drop)
            self.db.session.commit()
            logger.info(f"Added drop: {twitch_drop_id}")
            return drop
        
        except IntegrityError:
            self.db.session.rollback()
            logger.warning(f"Drop already exists: {twitch_drop_id}")
            return None
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error adding drop: {e}")
            return None
    
    def get_claimable_drops(self, user_id: int) -> list:
        """
        Get claimable drops using real indexes on is_claimable and dates
        """
        try:
            from models_real import Drop
            
            now = datetime.utcnow()
            drops = Drop.query.filter(
                and_(
                    Drop.user_id == user_id,
                    Drop.is_claimable == True,  # Index on is_claimable
                    Drop.is_claimed == False,  # Index on is_claimed
                    Drop.drop_available_at <= now,  # Index on dates
                    Drop.drop_expires_at >= now
                )
            ).all()
            
            return drops
        
        except Exception as e:
            logger.error(f"Error retrieving claimable drops: {e}")
            return []
    
    def claim_drop(self, drop_id: int) -> bool:
        """
        Mark drop as claimed
        """
        try:
            from models_real import Drop
            
            drop = Drop.query.get(drop_id)
            if not drop:
                return False
            
            drop.is_claimed = True
            drop.claimed_at = datetime.utcnow()
            drop.updated_at = datetime.utcnow()
            
            self.db.session.commit()
            logger.info(f"Claimed drop: {drop.twitch_drop_id}")
            return True
        
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error claiming drop: {e}")
            return False
    
    def get_user_drops_by_status(self, user_id: int, claimed: bool = True) -> list:
        """
        Get user drops by claim status using indexes
        """
        try:
            from models_real import Drop
            
            drops = Drop.query.filter(
                and_(
                    Drop.user_id == user_id,
                    Drop.is_claimed == claimed  # Index on is_claimed
                )
            ).order_by(Drop.claimed_at.desc()).all()
            
            return drops
        
        except Exception as e:
            logger.error(f"Error retrieving drops: {e}")
            return []
    
    # ========== CAMPAIGN OPERATIONS ==========
    
    def add_campaign(self, twitch_campaign_id: str, campaign_title: str,
                    game_id: str, game_name: str, status: str = 'ACTIVE',
                    start_date: datetime = None, end_date: datetime = None,
                    channel_ids: list = None) -> any:
        """
        Add drop campaign using indexes
        """
        try:
            from models_real import Campaign
            
            campaign = Campaign(
                twitch_campaign_id=twitch_campaign_id,  # Real index
                campaign_title=campaign_title,
                game_id=game_id,  # Real index
                game_name=game_name,
                status=status,  # Real index
                start_date=start_date or datetime.utcnow(),
                end_date=end_date or (datetime.utcnow() + timedelta(days=30)),
                channel_ids=channel_ids or []
            )
            
            self.db.session.add(campaign)
            self.db.session.commit()
            logger.info(f"Added campaign: {twitch_campaign_id}")
            return campaign
        
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error adding campaign: {e}")
            return None
    
    def get_active_campaigns(self) -> list:
        """
        Get active campaigns using indexes
        """
        try:
            from models_real import Campaign
            
            now = datetime.utcnow()
            campaigns = Campaign.query.filter(
                and_(
                    Campaign.status == 'ACTIVE',  # Index on status
                    Campaign.start_date <= now,
                    Campaign.end_date >= now
                )
            ).all()
            
            return campaigns
        
        except Exception as e:
            logger.error(f"Error retrieving campaigns: {e}")
            return []
    
    # ========== CHANNEL STATS OPERATIONS ==========
    
    def update_channel_stats(self, user_id: int, channel_id: str, channel_name: str,
                           drops_available: int = 0, drops_claimed: int = 0,
                           points_balance: int = 0) -> bool:
        """
        Update or create channel stats using composite index
        """
        try:
            from models_real import ChannelStats
            
            stats = ChannelStats.query.filter_by(
                user_id=user_id,
                channel_id=channel_id  # Uses composite index
            ).first()
            
            if not stats:
                stats = ChannelStats(
                    user_id=user_id,
                    channel_id=channel_id,
                    channel_name=channel_name
                )
                self.db.session.add(stats)
            
            stats.total_drops_available = drops_available
            stats.total_drops_claimed = drops_claimed
            stats.channel_points_balance = points_balance
            stats.last_checked = datetime.utcnow()
            stats.updated_at = datetime.utcnow()
            
            self.db.session.commit()
            logger.info(f"Updated stats for {channel_name}")
            return True
        
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Error updating channel stats: {e}")
            return False
    
    def get_user_channel_stats(self, user_id: int) -> list:
        """
        Get all channel stats for user using indexes
        """
        try:
            from models_real import ChannelStats
            
            stats = ChannelStats.query.filter_by(
                user_id=user_id  # Index on user_id
            ).all()
            
            return stats
        
        except Exception as e:
            logger.error(f"Error retrieving channel stats: {e}")
            return []
    
    # ========== STATISTICS ==========
    
    def get_drop_statistics(self, user_id: int) -> dict:
        """
        Get drop statistics using indexed queries
        """
        try:
            from models_real import Drop
            
            total = Drop.query.filter_by(user_id=user_id).count()
            claimed = Drop.query.filter_by(user_id=user_id, is_claimed=True).count()
            available = Drop.query.filter(
                and_(
                    Drop.user_id == user_id,
                    Drop.is_claimed == False,
                    Drop.is_claimable == True
                )
            ).count()
            
            return {
                'total_drops': total,
                'claimed_drops': claimed,
                'available_drops': available,
                'claim_percentage': (claimed / total * 100) if total > 0 else 0
            }
        
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}


if __name__ == '__main__':
    logger.info("Database operations module loaded")
