# Twitchminert-GUI + TwitchDropsMiner Integration Guide

## Overview

Twitchminert-GUI is a web-based management interface that can coordinate with TwitchDropsMiner to provide centralized monitoring, configuration, and log aggregation. This guide explains the integration architecture without replicating TwitchDropsMiner's internal logic.

## Understanding TwitchDropsMiner

Based on [TwitchDropsMiner's public documentation](https://github.com/DevilXD/TwitchDropsMiner), the miner:

- **Monitors stream metadata** - Fetches stream status every few seconds without downloading video/audio
- **Manages drops campaigns** - Discovers, prioritizes, and switches between eligible drop-earning streams
- **Uses WebSocket connections** - Maintains real-time channel status updates (up to 199 channels concurrently)
- **Stores session cookies** - Persists login sessions in `cookies.jar`
- **Maintains inventory** - Tracks claimed and unclaimed drops
- **Operates independently** - Can run standalone without external UI

---

## Integration Architecture

### Component Interaction Model

```
┌─────────────────────────────────────────────────────┐
│  Twitchminert-GUI (Web Interface)                   │
│  ┌──────────────────────────────────────────────┐  │
│  │ Configuration Management                      │  │
│  │ - Launch parameters                           │  │
│  │ - Priority lists                              │  │
│  │ - Game selection                              │  │
│  └────────────────┬─────────────────────────────┘  │
│                   │ API/IPC                        │
└───────────────────┼────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│  TwitchDropsMiner (Background Process)              │
│  ┌──────────────────────────────────────────────┐  │
│  │ Drop Mining Engine                            │  │
│  │ - Stream monitoring                           │  │
│  │ - Channel switching                           │  │
│  │ - Drop claiming logic                         │  │
│  │ - Session management                          │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
         │              │              │
         ▼              ▼              ▼
     Logs      Configuration    Status Updates
```

---

## Configuration Management

### Configuration File Structure

TwitchDropsMiner uses configuration files to control behavior. Twitchminert-GUI should support:

#### Priority List Format
The miner accepts game priority lists that determine which streams to watch:

```json
{
  "priority_list": [
    "game_name_1",
    "game_name_2"
  ],
  "priority_mode": "normal",  // or "random"
  "exclusion_list": [
    "excluded_game"
  ]
}
```

#### Game Selection
Games available for mining based on:
- Account's linked campaigns on Twitch.tv/drops/campaigns
- Current drop campaigns metadata
- Stream availability

### GUI Configuration Wizard Features

**Account Setup:**
- OAuth2 Twitch authentication (handled by miner)
- Linked account status verification
- Cookie/session management

**Game Prioritization:**
- Select from available campaigns
- Set mining priority order
- Configure game exclusions
- Adjust priority mode (standard or randomized)

**Mining Parameters:**
- Maximum concurrent monitored channels (up to 199)
- Channel switching behavior
- Stream metadata refresh interval
- Auto-start settings

---

## Launch Parameters

### Standard TwitchDropsMiner Invocation

```bash
# Windows - from executable
TwitchDropsMiner.exe

# Linux - from AppImage or PyInstaller
./TwitchDropsMiner-x86_64.AppImage

# From source
python -m main  # Requires Python 3.10+
```

### GUI-Controlled Launch

Twitchminert-GUI can manage miner process lifecycle:

#### Start Command
```bash
# Basic start with saved configuration
./TwitchDropsMiner

# With environment variables for mining paths
MINER_CONFIG_PATH=/path/to/config \
MINER_DATA_PATH=/path/to/data \
./TwitchDropsMiner
```

#### Process Management
The GUI should handle:
- Process spawning with working directory
- Graceful shutdown signals
- Restart on configuration changes
- Resource monitoring (CPU, memory)
- Exit code interpretation

### Configuration File Locations

TwitchDropsMiner searches for configuration in these locations (from miner docs):
- Current working directory
- User's home directory
- Miner installation directory

**Recommended structure for GUI integration:**
```
~/.twitchminert/
├── config/
│   ├── settings.json        # Priority list, game selection
│   └── advanced.json        # Mining parameters
├── data/
│   ├── cookies.jar          # Session storage (TDM)
│   └── inventory.json       # Drop tracking
└── logs/
    ├── mining_YYYY-MM-DD.log
    └── miner_output.log
```

---

## Log Capture and Analysis

### Log Output Format

TwitchDropsMiner generates logs containing:
- Stream metadata fetch results
- Channel switching events
- Drop progress updates
- Error conditions
- Session authentication status

### GUI Log Aggregation Strategy

#### Real-Time Monitoring
```python
# Pseudo-code for log streaming
class MinerLogCapture:
    def __init__(self, miner_process):
        self.process = miner_process
        self.log_stream = miner_process.stdout
    
    def capture_logs(self):
        """Stream logs from miner process"""
        while self.process.poll() is None:
            line = self.log_stream.readline()
            if line:
                self.parse_and_store(line)
    
    def parse_and_store(self, log_line):
        """Extract relevant info from log"""
        # Parse timestamps, events, status
        # Store to database for analytics
```

#### Log Parsing
Extract key events:
- **Stream switches**: "Switching from channel_X to channel_Y"
- **Drop progress**: "Drop progress: X seconds / Y total"
- **Campaign updates**: "New campaigns available: [...]"
- **Errors/Warnings**: Connection issues, auth failures

#### Persistent Storage
Store parsed logs in database:
```json
{
  "timestamp": "2026-01-22T19:30:00Z",
  "event_type": "stream_switch",
  "from_channel": "channel_a",
  "to_channel": "channel_b",
  "reason": "higher_priority_game",
  "duration_seconds": 3600
}
```

### Dashboard Display
Show real-time:
- Current mining channel
- Active drop progress
- Campaign status
- Session health
- Recent event log

---

## Monitoring and Status Tracking

### Miner Health Metrics

#### Session Status
- Login state (authenticated / not authenticated)
- Last successful authentication
- Session expiry prediction
- Cookie validity

#### Mining Activity
```json
{
  "mining_status": "active",
  "current_channel": "streamername",
  "current_drop": {
    "campaign_id": "xyz",
    "game_name": "Example Game",
    "progress_seconds": 1800,
    "total_seconds": 3600,
    "status": "in_progress"
  },
  "channels_monitored": 45,
  "pending_drops": 3,
  "claimed_drops": 12
}
```

#### Error Tracking
Monitor for:
- WebSocket connection failures
- Stream metadata fetch errors
- Authentication timeouts
- Campaign data sync issues
- Process crashes

### Monitoring Endpoints

Gui can implement polling API to retrieve state:

```python
# Read miner status from log files or IPC
@app.route('/api/miner/status')
def get_miner_status():
    return {
        'running': is_miner_running(),
        'pid': get_miner_pid(),
        'memory_mb': get_process_memory(),
        'uptime_seconds': get_uptime(),
        'last_activity': get_last_log_timestamp(),
        'current_mining': parse_latest_logs()
    }
```

---

## Data Exchange Mechanisms

### File-Based IPC

#### Configuration Updates
1. GUI writes config to temp file
2. Miner reads and applies changes
3. Miner restarts or reconfigures
4. GUI polls for confirmation

```python
# Configuration push
config = {
    'priority_list': ['Game A', 'Game B'],
    'exclusion_list': [],
    'priority_mode': 'normal'
}
write_config(config, miner_config_path)
signal_miner_to_reload()
```

#### Status Retrieval
Read from miner's output files:
- Last log entry timestamp
- Current channel being watched
- Campaign metadata cache
- Inventory status

### Process Communication

#### Signals (Unix/Linux)
```bash
# Graceful shutdown
kill -TERM $MINER_PID

# Reload configuration
kill -HUP $MINER_PID  # if supported

# Query status
kill -USR1 $MINER_PID  # custom signal handling
```

#### Standard I/O
- Capture stdout/stderr during process lifecycle
- Parse structured output if available
- Log to database for analysis

---

## Best Practices for Integration

### Security
1. **Never expose session cookies** - Keep `cookies.jar` private
2. **Validate all inputs** - Sanitize game names, configuration
3. **Rate limit API calls** - Don't overwhelm miner process
4. **Secure IPC** - Use file permissions for config files
5. **Audit logging** - Track configuration changes from GUI

### Reliability
1. **Process management** - Implement watchdog for miner crashes
2. **Graceful degradation** - GUI works if miner unavailable
3. **State synchronization** - Don't assume stale status
4. **Error recovery** - Retry failed operations with backoff
5. **Resource limits** - Monitor memory/CPU usage

### User Experience
1. **Status indicators** - Clear mining state visualization
2. **Configuration validation** - Warn before invalid setups
3. **Log filtering** - Show relevant events, hide noise
4. **Performance metrics** - Display drops/hour, session uptime
5. **Help documentation** - Explain miner concepts in GUI

---

## Troubleshooting Integration Issues

### Miner Process Won't Start
- Verify Python 3.10+ installed (if running from source)
- Check executable permissions
- Review working directory and paths
- Examine stderr for error messages

### Configuration Changes Not Applied
- Restart miner after config updates
- Verify config file format is valid JSON
- Check miner logs for parse errors
- Ensure proper file permissions

### Status Not Updating
- Confirm miner process is running (`ps aux | grep Miner`)
- Check log file paths are accessible
- Verify log parsing regex patterns
- Look for miner silent failures

### Session Expires Unexpectedly
- Review cookies.jar for expiry timestamps
- Check network connectivity to Twitch
- Monitor for authentication errors in logs
- Consider automatic re-authentication flow

---

## References

- [TwitchDropsMiner GitHub](https://github.com/DevilXD/TwitchDropsMiner)
- [TwitchDropsMiner Wiki - Setup & Running](https://github.com/DevilXD/TwitchDropsMiner/wiki/Setting-up-the-environment,-building-and-running)
- [TwitchDropsMiner README](https://github.com/DevilXD/TwitchDropsMiner/blob/master/README.md)
- [Twitch Drops Campaign System](https://www.twitch.tv/drops/campaigns)

---

## Disclaimer

This documentation is based on TwitchDropsMiner's public documentation and does not replicate, reverse-engineer, or expose internal implementation details. The integration approach respects the miner's design goals and operates through public interfaces and documented behavior.
