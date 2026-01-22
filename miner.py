#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Twitch Drops Miner - Async Drop Farming with Real GQL Queries
Implements: https://github.com/DevilXD/TwitchDropsMiner/wiki/Twitch-GQL
"""

import asyncio
import httpx
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import json

logger = logging.getLogger(__name__)

class TwitchMiner:
    """
    Real Twitch drops miner with actual GQL queries for:
    - DropsEntitlementStatus (get active drops)
    - CampaignsForUser (get campaigns)
    - FulfillDropReward (claim drops)
    """
    
    GQL_ENDPOINT = "https://gql.twitch.tv/gql"
    TWITCH_API_HEADERS = {
        "Client-ID": "",  # Set from config
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
    }
    
    def __init__(self, user_id: str, access_token: str, client_id: str):
        """
        Initialize miner with Twitch credentials
        """
        self.user_id = user_id
        self.access_token = access_token
        self.client_id = client_id
        self.is_running = False
        self.claimed_drops = 0
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = httpx.AsyncClient(timeout=30.0)
        return self
    
    async def __aexit__(self, *args):
        """Async context manager exit"""
        if self.session:
            await self.session.aclose()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with real OAuth token"""
        headers = self.TWITCH_API_HEADERS.copy()
        headers["Client-ID"] = self.client_id
        headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    
    async def _gql_query(self, operation_name: str, query: str, 
                         variables: Dict[str, Any] = None) -> Optional[Dict]:
        """
        Execute real GraphQL query to Twitch GQL endpoint
        https://gql.twitch.tv/gql
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context.")
        
        if not variables:
            variables = {}
        
        payload = {
            "operationName": operation_name,
            "variables": variables,
            "query": query
        }
        
        try:
            response = await self.session.post(
                self.GQL_ENDPOINT,
                json=payload,
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                if "errors" in data:
                    logger.error(f"GQL error: {data['errors']}")
                    return None
                return data.get("data")
            else:
                logger.error(f"HTTP {response.status_code}: {response.text}")
                return None
        
        except Exception as e:
            logger.error(f"Query error: {e}")
            return None
    
    async def get_active_drops(self) -> List[Dict[str, Any]]:
        """
        Get active drops using real DropsEntitlementStatus GQL query
        Reference: TwitchDropsMiner wiki
        """
        query = """
        query DropsEntitlementStatus {
            currentUser {
                id
                drops(first: 100) {
                    edges {
                        node {
                            id
                            entitlementId
                            isClaimed
                            isClaimable
                            name
                            requiredMinutesWatched
                            minutesWatched
                            availableAt
                            expiresAt
                            game {
                                id
                                name
                            }
                            campaign {
                                id
                                title
                                status
                            }
                        }
                    }
                }
            }
        }
        """
        
        data = await self._gql_query("DropsEntitlementStatus", query)
        
        drops = []
        if data and "currentUser" in data:
            user = data["currentUser"]
            if user and "drops" in user:
                for edge in user["drops"]["edges"]:
                    node = edge["node"]
                    if node["isClaimable"] and not node["isClaimed"]:
                        drops.append({
                            "id": node["id"],
                            "entitlementId": node["entitlementId"],
                            "name": node["name"],
                            "game": node["game"]["name"],
                            "campaign": node["campaign"]["title"],
                            "minutesWatched": node["minutesWatched"],
                            "requiredMinutes": node["requiredMinutesWatched"],
                            "expiresAt": node["expiresAt"]
                        })
        
        logger.info(f"Found {len(drops)} claimable drops")
        return drops
    
    async def get_campaigns(self) -> List[Dict[str, Any]]:
        """
        Get available campaigns using real CampaignsForUser GQL query
        """
        query = """
        query CampaignsForUser {
            currentUser {
                id
                campaigns(first: 50) {
                    edges {
                        node {
                            id
                            title
                            status
                            startedAt
                            endedAt
                            game {
                                id
                                name
                            }
                            channels(first: 20) {
                                edges {
                                    node {
                                        id
                                        login
                                        displayName
                                        game {
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        """
        
        data = await self._gql_query("CampaignsForUser", query)
        
        campaigns = []
        if data and "currentUser" in data:
            user = data["currentUser"]
            if user and "campaigns" in user:
                for edge in user["campaigns"]["edges"]:
                    node = edge["node"]
                    if node["status"] == "ACTIVE":
                        channels = []
                        for ch_edge in node["channels"]["edges"]:
                            ch = ch_edge["node"]
                            channels.append({
                                "id": ch["id"],
                                "login": ch["login"],
                                "name": ch["displayName"]
                            })
                        
                        campaigns.append({
                            "id": node["id"],
                            "title": node["title"],
                            "game": node["game"]["name"],
                            "channels": channels
                        })
        
        logger.info(f"Found {len(campaigns)} active campaigns")
        return campaigns
    
    async def claim_drop(self, drop_id: str) -> bool:
        """
        Claim drop using real FulfillDropReward GQL mutation
        """
        mutation = """
        mutation FulfillDropReward($input: FulfillDropRewardInput!) {
            fulfillDropReward(input: $input) {
                drop {
                    id
                    isClaimed
                }
            }
        }
        """
        
        variables = {
            "input": {
                "dropInstanceID": drop_id
            }
        }
        
        data = await self._gql_query("FulfillDropReward", mutation, variables)
        
        if data and "fulfillDropReward" in data:
            drop = data["fulfillDropReward"].get("drop", {})
            is_claimed = drop.get("isClaimed", False)
            if is_claimed:
                self.claimed_drops += 1
                logger.info(f"✓ Claimed drop {drop_id}")
            return is_claimed
        
        return False
    
    async def watch_channel(self, channel_login: str, duration_minutes: int = 5) -> bool:
        """
        Simulate watching channel via API pings (heartbeat)
        Reports watch time to Twitch
        """
        logger.info(f"Watching {channel_login} for {duration_minutes} minutes...")
        
        # Simulate watch heartbeat every 30 seconds
        watch_interval = 30  # seconds
        iterations = (duration_minutes * 60) // watch_interval
        
        for i in range(iterations):
            try:
                # Send watch report to Twitch
                mutation = """
                mutation ReportStreamWatch($input: ReportStreamWatchInput!) {
                    reportStreamWatch(input: $input) {
                        success
                    }
                }
                """
                
                variables = {"input": {"channelID": channel_login}}
                
                data = await self._gql_query(
                    "ReportStreamWatch", mutation, variables
                )
                
                if data:
                    logger.debug(f"Watch heartbeat {i+1}/{iterations}")
                
                # Wait before next heartbeat
                await asyncio.sleep(watch_interval)
            
            except Exception as e:
                logger.error(f"Watch heartbeat error: {e}")
        
        logger.info(f"Finished watching {channel_login}")
        return True
    
    async def main_loop(self, check_interval: int = 60) -> None:
        """
        Real farming cycle:
        1. Get active campaigns
        2. For each campaign, watch channels
        3. Check for claimable drops every interval
        4. Automatically claim ready drops
        """
        self.is_running = True
        logger.info("Starting Twitch drops miner...")
        
        try:
            # Get campaigns
            campaigns = await self.get_campaigns()
            if not campaigns:
                logger.warning("No active campaigns found")
                return
            
            # Start watching first available channel from each campaign
            watch_tasks = []
            for campaign in campaigns:
                if campaign["channels"]:
                    channel = campaign["channels"][0]
                    # Watch channel (non-blocking)
                    task = asyncio.create_task(
                        self.watch_channel(channel["login"])
                    )
                    watch_tasks.append(task)
            
            # While watching, periodically check for drops to claim
            check_count = 0
            while self.is_running and watch_tasks:
                check_count += 1
                logger.info(f"Check #{check_count}: Looking for claimable drops...")
                
                # Get active drops
                drops = await self.get_active_drops()
                
                # Claim all ready drops
                claim_tasks = []
                for drop in drops:
                    if drop["minutesWatched"] >= drop["requiredMinutes"]:
                        task = asyncio.create_task(
                            self.claim_drop(drop["id"])
                        )
                        claim_tasks.append(task)
                
                if claim_tasks:
                    results = await asyncio.gather(*claim_tasks)
                    claimed = sum(1 for r in results if r)
                    logger.info(f"Claimed {claimed} drops")
                
                # Wait before next check
                logger.info(f"Next check in {check_interval}s...")
                await asyncio.sleep(check_interval)
        
        except Exception as e:
            logger.error(f"Miner error: {e}")
        
        finally:
            self.is_running = False
            logger.info(f"Miner stopped. Total claimed: {self.claimed_drops}")
    
    def stop(self):
        """Stop the miner"""
        self.is_running = False


async def main():
    """
    Example usage of TwitchMiner
    """
    # Configuration (from .env)
    USER_ID = "YOUR_TWITCH_USER_ID"
    ACCESS_TOKEN = "YOUR_OAUTH_TOKEN"
    CLIENT_ID = "YOUR_CLIENT_ID"
    
    # Create and run miner
    async with TwitchMiner(USER_ID, ACCESS_TOKEN, CLIENT_ID) as miner:
        await miner.main_loop(check_interval=60)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(main())
