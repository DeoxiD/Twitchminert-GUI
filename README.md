# 🎮 Twitchminert-GUI

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-blue)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue-3.0%2B-brightgreen)](https://vuejs.org/)

**Advanced GUI Control Panel for Twitchminert** - A modern, user-friendly web-based interface for managing Twitch Channel Points automation with configuration wizard, real-time dashboard, analytics, and notifications.

## 🌟 Features

### 📊 Dashboard
- Real-time streamer status monitoring
- Live channel points tracking
- Session statistics and analytics
- Recent betting activities
- Visual performance indicators

### ⚙️ Configuration Wizard
- Step-by-step setup process
- Twitch OAuth authentication
- Automated follower list import
- Customizable betting strategies (SMART, MOST_VOTED, HIGH_ODDS, PERCENTAGE)
- Per-streamer settings configuration
- Filter conditions and bet limits

### 🎰 Betting System
- Multiple strategies support:
  - **SMART**: Intelligent decision-making based on odds and popularity
  - **MOST_VOTED**: Follow the majority
  - **HIGH_ODDS**: Bet on highest odds
  - **PERCENTAGE**: Use displayed percentages
- Customizable stake percentages
- Stealth mode for realistic betting
- Bet filtering and validation

### 🔔 Notifications
- Telegram bot integration
- Discord webhook support
- Custom webhook endpoints
- Event-based notifications
- Selective event filtering

### 📈 Analytics
- Interactive points history charts
- Event annotations (streamer online/offline, wins/losses)
- Performance metrics
- Dark/Light theme toggle
- Time range selection

### 🔐 Security
- Secure credential storage
- OAuth2 authentication
- HTTPS support
- Session management
- Cookie-based authentication

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14+ (for frontend development)
- pip or conda

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/DeoxiD/Twitchminert-GUI.git
cd Twitchminert-GUI
```

#### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Frontend Setup (Optional for development)
```bash
cd frontend
npm install
npm run build
```

#### 4. Run the application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📋 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
TWITCH_CLIENT_ID=your-twitch-client-id
TWITCH_CLIENT_SECRET=your-twitch-client-secret
TELEGRAM_BOT_TOKEN=your-telegram-token
DISCORD_WEBHOOK_URL=your-discord-webhook
```

### API Endpoints

#### Configuration
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration
- `POST /api/config/validate` - Validate configuration
- `GET /api/export-config` - Export config as JSON
- `POST /api/import-config` - Import config from JSON

#### Streamers
- `GET /api/streamers` - Get all streamers
- `POST /api/streamers` - Add new streamer
- `PUT /api/streamers/<username>` - Update streamer settings
- `DELETE /api/streamers/<username>` - Remove streamer

#### Status & Testing
- `GET /api/status` - Get system status
- `POST /api/test-notification` - Test notification sending

## 🎯 Usage

### First Time Setup
1. Open http://localhost:5000 in your browser
2. Click "New Configuration" to start the wizard
3. Enter your Twitch credentials
4. Select streamers to monitor (manually or import from followers)
5. Configure betting strategies and preferences
6. Set up notifications (optional)
7. Review and save configuration

### Managing Configurations
- Save multiple configurations
- Import/Export JSON configs
- Load previous configurations
- Real-time validation

### Dashboard Features
- Monitor active streamers in real-time
- View betting history
- Track points earned
- See active sessions
- Download logs

## 📁 Project Structure

```
Twitchminert-GUI/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── configs/              # Configuration storage
│   └── default_config.json
├── static/               # Static files (CSS, JS)
│   ├── css/
│   └── js/
├── templates/            # HTML templates
│   └── index.html
├── logs/                 # Application logs
└── frontend/            # Vue.js frontend (optional)
    ├── src/
    ├── public/
    └── package.json
```

## 🛠️ Development

### Running in Debug Mode
```bash
FLASK_ENV=development python app.py
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Testing
```bash
pytest tests/
```

## 📚 API Documentation

### Configuration Object
```json
{
  "twitch": {
    "username": "string",
    "password": "string",
    "claim_drops_startup": boolean
  },
  "priority": ["STREAK", "DROPS", "ORDER"],
  "streamer_settings": {
    "make_predictions": boolean,
    "follow_raid": boolean,
    "claim_drops": boolean,
    "watch_streak": boolean,
    "community_goals": boolean,
    "chat": "ONLINE|OFFLINE|ALWAYS|NEVER"
  },
  "bet_settings": {
    "strategy": "SMART|MOST_VOTED|HIGH_ODDS|PERCENTAGE",
    "percentage": number,
    "percentage_gap": number,
    "max_points": number,
    "stealth_mode": boolean,
    "delay_mode": "FROM_START|FROM_END|PERCENTAGE",
    "delay": number,
    "minimum_points": number
  },
  "streamers": [{"username": "string", "settings": {}}],
  "blacklist": ["string"]
}
```

## 🔗 Integration with Twitchminert

This GUI generates a `run.py` configuration file compatible with the original Twitchminert script:

```bash
python run.py
```

The generated configuration includes:
- All betting strategies
- Streamer lists and settings
- Notification integrations
- Priority-based execution
- Analytics configuration

## ⚠️ Disclaimer

This project is an unofficial tool and comes with no warranty. Use at your own risk. Twitch may restrict or ban accounts using automation tools. This is for educational purposes only.

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🙋 Support

- Issues: [GitHub Issues](https://github.com/DeoxiD/Twitchminert-GUI/issues)
- Discussions: [GitHub Discussions](https://github.com/DeoxiD/Twitchminert-GUI/discussions)
- Original Twitchminert: [GitHub](https://github.com/rdavydov/Twitch-Channel-Points-Miner-v2)

## 🔗 Related Projects

- [Twitchminert](https://github.com/rdavydov/Twitch-Channel-Points-Miner-v2) - Original Twitch Channel Points Miner
- [Twitch-Channel-Points-Miner](https://github.com/gottagofaster236/Twitch-Channel-Points-Miner)

## 📞 Credits

Developed by [@DeoxiD](https://github.com/DeoxiD)

Based on:
- [Twitch-Channel-Points-Miner-v2](https://github.com/rdavydov/Twitch-Channel-Points-Miner-v2) by [@rdavydov](https://github.com/rdavydov)
- [TwitchAutoCollect-AutoBet](https://github.com/ClementRoyer/TwitchAutoCollect-AutoBet) by [@ClementRoyer](https://github.com/ClementRoyer)

---

**Last Updated**: January 16, 2026
**Version**: 1.0.0 (Beta)


### 🎯 Twitch Drops Mining

- Automatic Twitch drops campaign discovery
- Stream-less drop mining (bandwidth efficient)
- Game priority and exclusion lists
- Sharded websocket connection for 199+ channels
- Automatic channel switching
- Drop claims and inventory management
- Campaign validation and drop campaign filtering

## 🔗 Related Projects

- [TwitchDropsMiner](https://github.com/DevilXD/TwitchDropsMiner) - Advanced Twitch drops mining
- [Twitchminert](https://github.com/rdavydov/Twitch-Channel-Points-Miner-v2) - Original Twitch Channel Points Miner

## 🚀 New v2 Features

- **Hybrid Mining System**: Now supports both Channel Points AND Drops mining in one unified interface
- **Drops Dashboard**: Real-time drops campaign tracking and management
- **Async/Await Operations**: Fully asynchronous operations for better performance
- **Modern Web Interface**: Flask + Vue.js modern responsive UI
- **Rest API**: Full REST API for all operations
- **Multi-Account Support**: Manage multiple accounts simultaneously
- **WebSocket Integration**: Real-time updates and streaming

---

**Last Updated**: January 16, 2026  
**Version**: 2.0.0 (Hybrid Mining)
