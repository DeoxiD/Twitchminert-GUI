"""Extended database operations for Drop and Campaign models."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import and_

from models import Drop, Campaign
from config import db, logger


class DropOps:
    """Database operations for Drop model."""

    @staticmethod
    def create(
        campaign_id: int,
        drop_id: str,
        reward_name: str,
        reward_description: str = None,
        **kwargs
    ) -> Optional[Drop]:
        """Create new individual drop reward."""
        try:
            drop = Drop(
                campaign_id=campaign_id,
                drop_id=drop_id,
                reward_name=reward_name,
                reward_description=reward_description,
                **kwargs
            )
            db.session.add(drop)
            db.session.commit()
            logger.info(f"Created drop {drop_id} for campaign {campaign_id}")
            return drop
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Drop {drop_id} already exists")
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error creating drop: {e}")
            return None

    @staticmethod
    def get_pending_drops(campaign_id: int) -> List[Drop]:
        """Get all pending drops for a campaign."""
        try:
            return Drop.query.filter(
                and_(
                    Drop.campaign_id == campaign_id,
                    Drop.status == 'PENDING'
                )
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching pending drops: {e}")
            return []

    @staticmethod
    def mark_claimed(
        drop_id: int,
        mining_duration: int = 0
    ) -> Optional[Drop]:
        """Mark drop as claimed with mining duration."""
        try:
            drop = Drop.query.get(drop_id)
            if drop:
                drop.claimed = True
                drop.status = 'CLAIMED'
                drop.claimed_at = datetime.utcnow()
                drop.mining_duration_seconds = mining_duration
                drop.updated_at = datetime.utcnow()
                db.session.commit()
                logger.info(f"Marked drop {drop_id} as claimed")
                return drop
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error updating drop: {e}")
            return None

    @staticmethod
    def get_claimed_drops(campaign_id: int) -> List[Drop]:
        """Get all claimed drops for a campaign."""
        try:
            return Drop.query.filter(
                and_(
                    Drop.campaign_id == campaign_id,
                    Drop.status == 'CLAIMED'
                )
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching claimed drops: {e}")
            return []

    @staticmethod
    def update_drop_status(drop_id: int, status: str) -> Optional[Drop]:
        """Update drop status."""
        try:
            drop = Drop.query.get(drop_id)
            if drop:
                drop.status = status
                drop.updated_at = datetime.utcnow()
                db.session.commit()
                logger.info(f"Updated drop {drop_id} status to {status}")
                return drop
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error updating drop status: {e}")
            return None

    @staticmethod
    def delete_drop(drop_id: int) -> bool:
        """Delete a drop."""
        try:
            drop = Drop.query.get(drop_id)
            if drop:
                db.session.delete(drop)
                db.session.commit()
                logger.info(f"Deleted drop {drop_id}")
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error deleting drop: {e}")
            return False


class CampaignOps:
    """Database operations for Campaign model."""

    @staticmethod
    def get_active_campaigns() -> List[Campaign]:
        """Get all active campaigns."""
        try:
            return Campaign.query.filter(
                Campaign.status == 'ACTIVE'
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching active campaigns: {e}")
            return []

    @staticmethod
    def get_campaign_drops(
        campaign_id: int,
        status: str = None
    ) -> List[Drop]:
        """Get drops for a campaign, optionally filtered by status."""
        try:
            query = Drop.query.filter(Drop.campaign_id == campaign_id)
            if status:
                query = query.filter(Drop.status == status)
            return query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching campaign drops: {e}")
            return []

    @staticmethod
    def update_campaign_status(
        campaign_id: int,
        status: str
    ) -> Optional[Campaign]:
        """Update campaign status."""
        try:
            campaign = Campaign.query.get(campaign_id)
            if campaign:
                campaign.status = status
                campaign.updated_at = datetime.utcnow()
                db.session.commit()
                logger.info(f"Updated campaign {campaign_id} status to {status}")
                return campaign
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error updating campaign: {e}")
            return None

    @staticmethod
    def get_campaign_stats(campaign_id: int) -> dict:
        """Get statistics for a campaign."""
        try:
            total_drops = Drop.query.filter(
                Drop.campaign_id == campaign_id
            ).count()
            claimed_drops = Drop.query.filter(
                and_(
                    Drop.campaign_id == campaign_id,
                    Drop.status == 'CLAIMED'
                )
            ).count()
            pending_drops = Drop.query.filter(
                and_(
                    Drop.campaign_id == campaign_id,
                    Drop.status == 'PENDING'
                )
            ).count()
            
            return {
                'total': total_drops,
                'claimed': claimed_drops,
                'pending': pending_drops,
                'claim_rate': (claimed_drops / total_drops * 100) if total_drops > 0 else 0
            }
        except SQLAlchemyError as e:
            logger.error(f"Error calculating campaign stats: {e}")
            return {}
