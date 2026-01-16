#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database operations for all models - Complete CRUD implementation
Provides comprehensive Create, Read, Update, Delete operations for all database models
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy import and_, or_, desc, asc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

from models import (
    db, Configuration, Streamer, BettingActivity, 
    DropsCampaign, Drop, MiningSession, Session
)

logger = logging.getLogger(__name__)


# ==================== Configuration Operations ====================

class ConfigurationOps:
    """Database operations for Configuration model"""
    
    @staticmethod
    def create(user_id: str, name: str, config_data: Dict, is_active: bool = True) -> Optional[Configuration]:
        """Create new configuration"""
        try:
            config = Configuration(
                user_id=user_id,
                name=name,
                config_data=config_data,
                is_active=is_active
            )
            db.session.add(config)
            db.session.commit()
            logger.info(f"Created configuration for user {user_id}")
            return config
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Configuration for user {user_id} already exists")
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error creating configuration: {e}")
            return None
    
    @staticmethod
    def get_by_id(config_id: int) -> Optional[Configuration]:
        """Get configuration by ID"""
        return Configuration.query.get(config_id)
    
    @staticmethod
    def get_by_user_id(user_id: str) -> Optional[Configuration]:
        """Get configuration by user ID"""
        return Configuration.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def get_all_active() -> List[Configuration]:
        """Get all active configurations"""
        return Configuration.query.filter_by(is_active=True).all()
    
    @staticmethod
    def update(config_id: int, **kwargs) -> Optional[Configuration]:
        """Update configuration"""
        try:
            config = Configuration.query.get(config_id)
            if not config:
                return None
            
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
            
            config.updated_at = datetime.utcnow()
            db.session.commit()
            logger.info(f"Updated configuration {config_id}")
            return config
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error updating configuration: {e}")
            return None
    
    @staticmethod
    def delete(config_id: int) -> bool:
        """Delete configuration"""
        try:
            config = Configuration.query.get(config_id)
            if not config:
                return False
            
            db.session.delete(config)
            db.session.commit()
            logger.info(f"Deleted configuration {config_id}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error deleting configuration: {e}")
            return False


# ==================== Streamer Operations ====================

class StreamerOps:
    """Database operations for Streamer model"""
    
    @staticmethod
    def create(username: str, **kwargs) -> Optional[Streamer]:
        """Create new streamer"""
        try:
            streamer = Streamer(username=username, **kwargs)
            db.session.add(streamer)
            db.session.commit()
            logger.info(f"Created streamer {username}")
            return streamer
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Streamer {username} already exists")
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error creating streamer: {e}")
            return None
    
    @staticmethod
    def get_all(**kwargs) -> List[Streamer]:
        """Get all streamers with optional filters"""
        query = Streamer.query
        if 'is_online' in kwargs:
            query = query.filter_by(is_online=kwargs['is_online'])
        return query.all()
    
    @staticmethod
    def get_by_username(username: str) -> Optional[Streamer]:
        """Get streamer by username"""
        return Streamer.query.filter_by(username=username).first()
    
    @staticmethod
    def update_online_status(streamer_id: int, is_online: bool) -> Optional[Streamer]:
        """Update streamer online status"""
        try:
            streamer = Streamer.query.get(streamer_id)
            if streamer:
                streamer.is_online = is_online
                streamer.last_seen = datetime.utcnow()
                db.session.commit()
                return streamer
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error updating streamer status: {e}")
            return None


# See additional operations in database_operations_ext.py for:
# - BettingActivityOps
# - DropsCampaignOps
# - DropOps 
# - MiningSessionOps
# - SessionOps
# - DatabaseManager (transaction handling, bulk operations)
