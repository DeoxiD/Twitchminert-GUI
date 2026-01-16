# Twitchminert-GUI

**Advanced Hybrid Twitch Miner - Drops + Channel Points Automation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/) [![Flask 2.3+](https://img.shields.io/badge/Flask-2.3%2B-green.svg)](https://flask.palletsprojects.com/) [![Docker Supported](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

> Twitchminert-GUI is a modern, user-friendly **web-based interface** for Twitch channel points automation with real-time dashboard, configuration wizard, analytics, and notifications.

## ✨ Features

### 📊 Dashboard

- ✅ Real-time streamer status monitoring
- ✅ Live channel points tracking
- ✅ Session statistics and analytics
- ✅ Recent bet history
- ✅ Visual performance metrics
- ✅ REST API endpoints

### ⚙️ Configuration Wizard

- ✅ Step-by-step setup process
- ✅ Twitch OAuth authentication
- ✅ Automated followed channels import
- ✅ Customizable betting strategies (SMART, MOST_VOTED, HIGH_ODDS, PERCENTAGE)
- ✅ Follower-oriented settings
- ✅ Filtering conditions and betting limits

### 🎮 Betting System

- ✅ Multiple strategy support
  - **SMART**: Intelligent decision making based on odds and popularity
  - **MOST_VOTED**: Follow the crowd majority
  - **HIGH_ODDS**: Bet on the highest odds
  - **PERCENTAGE**: Automatic betting with fixed percentage
- ✅ Bet limits and filtering
- ✅ Tutorials and relevant recommendations

### 🌍 Additional Features

- ✅ Multi-language support (EN/LV)
- ✅ Discord integration
- ✅ Telegram notifications
- ✅ Detailed logging

## 📦 Installation

### Requirements

- Python 3.8 or newer
- pip or conda
- Git
- Modern browser

### Option 1: Python Direct Installation

```bash
# Clone the repository
git clone https://github.com/DeoxiD/Twitchminert-GUI.git
cd Twitchminert-GUI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### Option 2: Windows EXE

```bash
# Build standalone .exe file
python build_exe.py

# Run
.\dist\Twitchminert-GUI.exe
```

### Option 3: Docker

```bash
# Build Docker image
docker build -t twitchminert-gui .

# Run container
docker run -p 5000:5000 twitchminert-gui
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root directory with the following variables:

```env
# Twitch API
TWITCH_CLIENT_ID=your-client-id
TWITCH_CLIENT_SECRET=your-client-secret
TWITCH_REDIRECT_URI=http://localhost:5000/callback

# Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///twitchminert.db

# Notifications (optional)
TELEGRAM_BOT_TOKEN=your-bot-token
DISCORD_WEBHOOK_URL=your-discord-webhook
```

### OAuth Registration

1. Go to [Twitch Developer Console](https://dev.twitch.tv/console/apps)
2. Create a new application
3. Copy **Client ID** and **Client Secret**
4. Paste into `.env` file

## 🚀 Getting Started

### Run via Terminal

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows

# Run the application
python run.py

# Open in browser
http://localhost:5000
```

### Access Points

- **Dashboard**: [http://localhost:5000/](http://localhost:5000/)
- **Settings**: [http://localhost:5000/settings](http://localhost:5000/settings)
- **Logs**: [http://localhost:5000/logs](http://localhost:5000/logs)
- **API Documentation**: [http://localhost:5000/api/docs](http://localhost:5000/api/docs)

## 📁 Project Structure

```
Twitchminert-GUI/
├── core/                    # Core modules
│   ├── __init__.py
│   ├── auth.py              # Twitch OAuth authentication
│   ├── drops.py             # Drops mining module
│   ├── points.py            # Channel points module
│   ├── scheduler.py         # Task scheduler
│   └── twitch_client.py     # Twitch API client
├── web/                     # Web interface
│   ├── __init__.py
│   ├── app.py               # Flask application
│   ├── routes.py            # API routes
│   ├── templates/
│   │   └── index.html       # Main page
│   └── static/
│       ├── style.css        # Styles
│       └── script.js        # Scripts
├── .env.example             # Environment variables example
├── requirements.txt         # Python dependencies
├── run.py                   # Entry point
├── config.py                # Configuration classes
├── build_exe.py             # Windows EXE builder
└── README.md                # This documentation
```

## 🔌 API Endpoints

### Status

```
GET /api/status
# Returns miner status
```

### Configuration

```
GET /api/config
# Get current settings
POST /api/config
# Save new settings
```

### Streamers

```
GET /api/streamers
# List all streamers
POST /api/streamers
# Add new streamer
```

### Control

```
POST /api/start
# Start miner
POST /api/stop
# Stop miner
```

## 🛠️ Development

### Local Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Run linter
flake8 . --count --select=E9,F63,F7,F82 --show-source
```

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## ⚠️ Disclaimer

- This application is independent of Twitch Inc.
- You are responsible for complying with Twitch Terms of Service
- Authors are not responsible for any issues or ban risks

## 📞 Support

Have questions or issues? Open a [GitHub Issue](https://github.com/DeoxiD/Twitchminert-GUI/issues)

**Last Updated**: January 2026
