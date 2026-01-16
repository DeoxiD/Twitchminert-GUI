#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TwitchDropsMiner integration module for GUI
"""

import asyncio
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class DropCampaign:
    """Twitch drops campaign"""
    campaign_id: str
    game_title: str
    game_id: str
    total_rewards: int
    claimed_rewards: int
    active: bool
    created_at: str
    ends_at: str


@dataclass
class MinedDrop:
    """Mined drop information"""
    campaign_id: str
    reward_id: str
    reward_name: str
    game_title: str
    claimed: bool
    claimed_at: Optional[str] = None


class DropsMinerManager:
    """Manages Twitch Drops mining operations"""
    
    def __init__(self):
        self.campaigns: Dict[str, DropCampaign] = {}
        self.mined_drops: List[MinedDrop] = []
        self.mining_active = False
        self.current_channel = None
        self.stats = {
            "total_drops_claimed": 0,
            "total_channels_watched": 0,
            "mining_duration_seconds": 0,
            "last_update": None
        }
    
    async def start_mining(self, campaigns: List[Dict]) -> bool:
        """Start drops mining"""
        try:
            self.mining_active = True
            self.campaigns = {
                c["campaign_id"]: DropCampaign(
                    campaign_id=c["campaign_id"],
                    game_title=c["game_title"],
                    game_id=c["game_id"],
                    total_rewards=c["total_rewards"],
                    claimed_rewards=c["claimed_rewards"],
                    active=c["active"],
                    created_at=c["created_at"],
                    ends_at=c["ends_at"]
                )
                for c in campaigns
            }
            self.stats["last_update"] = datetime.now().isoformat()
            return True
        except Exception as e:
            print(f"Error starting mining: {e}")
            return False
    
    async def stop_mining(self) -> bool:
        """Stop drops mining"""
        try:
            self.mining_active = False
            return True
        except Exception as e:
            print(f"Error stopping mining: {e}")
            return False
    
    async def claim_drop(self, campaign_id: str, reward_id: str) -> bool:
        """Claim a drop reward"""
        try:
            if campaign_id in self.campaigns:
                drop = MinedDrop(
                    campaign_id=campaign_id,
                    reward_id=reward_id,
                    reward_name=f"Reward {reward_id}",
                    game_title=self.campaigns[campaign_id].game_title,
                    claimed=True,
                    claimed_at=datetime.now().isoformat()
                )
                self.mined_drops.append(drop)
                self.stats["total_drops_claimed"] += 1
                return True
            return False
        except Exception as e:
            print(f"Error claiming drop: {e}")
            return False
    
    async def switch_channel(self, channel_id: str) -> bool:
        """Switch to different channel"""
        try:
            self.current_channel = channel_id
            self.stats["total_channels_watched"] += 1
            self.stats["last_update"] = datetime.now().isoformat()
            return True
        except Exception as e:
            print(f"Error switching channel: {e}")
            return False
    
    def get_status(self) -> Dict:
        """Get current mining status"""
        return {
            "mining_active": self.mining_active,
            "current_channel": self.current_channel,
            "total_campaigns": len(self.campaigns),
            "active_campaigns": sum(1 for c in self.campaigns.values() if c.active),
            "mined_drops": len(self.mined_drops),
            "stats": self.stats
        }
    
    def get_campaigns(self) -> List[Dict]:
        """Get all campaigns"""
        return [asdict(c) for c in self.campaigns.values()]
    
    def get_mined_drops(self) -> List[Dict]:
        """Get all mined drops"""
        return [asdict(d) for d in self.mined_drops]


# Global instance
drops_miner = DropsMinerManager()
