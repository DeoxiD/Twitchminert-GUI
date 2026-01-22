# Logging and Diagnostics Guide

Comprehensive logging snippets and SQL query inspection utilities for Twitchminert-GUI debugging and monitoring.

## Table of Contents

1. [Logging Configuration](#logging-configuration)
2. [Print/Logging Statements by Module](#printlogging-statements-by-module)
3. [Database Operations Inspection](#database-operations-inspection)
4. [SQL Query Examples](#sql-query-examples)
5. [Error Tracking and Debugging](#error-tracking-and-debugging)
6. [Performance Monitoring](#performance-monitoring)

---

## Logging Configuration

### Setup in app.py

```python
import logging
import sys
from datetime import datetime

# Enhanced logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/twitchminert_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
```

### Log Levels Reference

- **DEBUG** (10): Detailed diagnostic information
- **INFO** (20): Confirmation that things are working as expected
- **WARNING** (30): Warning about potential issues
- **ERROR** (40): Error has occurred but system can continue
- **CRITICAL** (50): Serious error, system may not continue

---

## Print/Logging Statements by Module

### app.py - Flask Application

#### OAuth Callback with Enhanced Logging

```python
logger.info(f'Auth callback - Code: {bool(code)}, State: {bool(state)}')
if error:
    logger.error(f'OAuth error: {error}')
    return render_template('index.html', error='Auth failed')
if auth_manager.handle_callback(code, state):
    logger.info('OAuth successful')
    session['authenticated'] = True
    return redirect('/')
else:
    logger.error('Token exchange failed')
    return render_template('index.html', error='Failed')
```

### drops_miner.py - Mining Operations

```python
async def _mining_loop(self):
    iteration = 0
    while self.status == MinerStatus.RUNNING:
        try:
            iteration += 1
            logger.info(f'Mining iteration {iteration}')
            logger.debug(f'Status: {self.status.value}, Campaigns: {len(self.campaigns)}')
            
            fresh_campaigns = await self.miner_wrapper.get_campaigns()
            logger.info(f'Retrieved {len(fresh_campaigns)} campaigns')
            
            for campaign in fresh_campaigns:
                logger.debug(f'{campaign.game_title}: {campaign.claimed_rewards}/{campaign.total_rewards}')
                self.campaigns[campaign.campaign_id] = campaign
            
            await asyncio.sleep(300)
        except Exception as e:
            logger.exception(f'Mining loop error: {str(e)}')
            await asyncio.sleep(30)
```

---

## Database Operations Inspection

### SQL Inspection via Python

```python
from app import create_app, db
from sqlalchemy import text

app = create_app('development')

with app.app_context():
    # View configurations
    configs = Configuration.query.all()
    logger.info(f'Total configs: {len(configs)}')
    for cfg in configs:
        logger.debug(f'  ID: {cfg.id}, User: {cfg.user_id}, Active: {cfg.is_active}')
    
    # Raw SQL query
    result = db.session.execute(text('SELECT COUNT(*) FROM configuration')).scalar()
    logger.info(f'Configuration table rows: {result}')
```

---

## Troubleshooting Guide

### Common Issues

| Issue | Log Check | Solution |
|-------|-----------|----------|
| OAuth fails | `OAuth error:` | Verify client ID/secret |
| DB error | `SQLAlchemy error` | Check .env database URL |
| No campaigns | `Retrieved 0 campaigns` | Check Twitch credentials |
| Drops not claimed | `Drop claim error` | Verify drop IDs |
| Mining loop stuck | No iteration logs | Check exception handling |

---

Last Updated: 2026-01-22
