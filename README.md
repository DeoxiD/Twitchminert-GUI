# 🎮 Twitchminert-GUI

**Advanced GUI Control Panel for Twitchminert & TwitchDropsMiner**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask 2.3+](https://img.shields.io/badge/Flask-2.3%2B-green.svg)](https://flask.palletsprojects.com/)
[![Docker Supported](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

> A modern, user-friendly **web-based interface** for managing Twitch Channel Points automation with real-time dashboard, configuration wizard, analytics, and notifications.

---

## ✨ Features

### 📊 Dashboard
- ✅ Real-time streamer status monitoring
- ✅ Live channel points tracking
- ✅ Session statistics and analytics
- ✅ Recent betting activities
- ✅ Visual performance indicators

### ⚙️ Configuration Wizard
- ✅ Step-by-step setup process
- ✅ Twitch OAuth authentication
- ✅ Automated follower list import
- ✅ Customizable betting strategies (SMART, MOST_VOTED, HIGH_ODDS, PERCENTAGE)
- ✅ Per-streamer settings configuration
- ✅ Filter conditions and bet limits

### 🎰 Betting System
- ✅ Multiple strategies support
  - **SMART**: Intelligent decision-making based on odds and popularity
  - **MOST_VOTED**: Follow the majority
  - **HIGH_ODDS**: Bet on highest odds
  - **PERCENTAGE**: Use displayed percentages
- ✅ Customizable stake percentages
- ✅ Stealth mode for realistic betting
- ✅ Bet filtering and validation

### 🔔 Notifications
- ✅ Telegram bot integration
- ✅ Discord webhook support
- ✅ Custom webhook endpoints
- ✅ Event-based notifications

### 📈 Analytics
- ✅ Interactive points history charts
- ✅ Event annotations (streamer online/offline, wins/losses)
- ✅ Performance metrics
- ✅ Dark/Light theme toggle

### 🔐 Security
- ✅ Secure credential storage
- ✅ OAuth2 authentication
- ✅ HTTPS support
- ✅ Session management

### 🎯 Twitch Drops Mining
- ✅ Automatic Twitch drops campaign discovery
- ✅ Stream-less drop mining (bandwidth efficient)
- ✅ Game priority and exclusion lists
- ✅ Automatic channel switching
- ✅ Campaign validation and filtering

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **pip** (Usually comes with Python)
- **Git** ([Download](https://git-scm.com/))

### Installation

#### Option 1: Python Direct
```bash
git clone https://github.com/DeoxiD/Twitchminert-GUI.git
cd Twitchminert-GUI
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\\Scripts\\activate  # Windows

pip install -r requirements.txt
python run.py
```

#### Option 2: Windows EXE
```bash
python build_exe.py
.\\dist\\Twitchminert-GUI.exe
```

#### Option 3: Docker
```bash
docker-compose up -d
# Access at http://localhost:5000
```

---

## 📋 Configuration

### Environment Variables
Create `.env` file:
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
TWITCH_CLIENT_ID=your-client-id
TWITCH_CLIENT_SECRET=your-client-secret
TELEGRAM_BOT_TOKEN=optional-telegram-token
DISCORD_WEBHOOK_URL=optional-discord-webhook
```

### API Endpoints
- `GET /api/status` - System status
- `GET /api/config` - Get configuration
- `POST /api/config` - Save configuration
- `GET /api/streamers` - List streamers
- `POST /api/streamers` - Add streamer
- `GET /api/dashboard` - Dashboard data
- `POST /api/test-notification` - Test notifications

---

## 📁 Project Structure

```
Twitchminert-GUI/
├── .github/workflows/        # GitHub Actions CI/CD
├── .vscode/                  # VS Code settings
├── app.py                    # Flask application
├── config.py                 # Configuration classes
├── models.py                 # Database models
├── utils.py                  # Utility functions
├── drops_miner.py            # TwitchDropsMiner integration
├── run.py                    # Startup script
├── build_exe.py              # PyInstaller builder
├── Dockerfile                # Docker container
├── docker-compose.yml        # Docker Compose
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── SETUP_WINDOWS.md          # Windows setup guide
└── LICENSE                   # MIT License
```

---

## 🛠️ Development

### Running in Debug Mode
```bash
FLASK_ENV=development python run.py
```

### Running Tests
```bash
pytest tests/ -v
```

### Building Docker Image
```bash
docker build -t twitchminert-gui:latest .
docker run -p 5000:5000 twitchminert-gui:latest
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## ⚠️ Disclaimer

This project is an unofficial tool and comes with no warranty. Use at your own risk. Twitch may restrict or ban accounts using this software. The authors are not responsible for any consequences.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/DeoxiD/Twitchminert-GUI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/DeoxiD/Twitchminert-GUI/discussions)

---

## 🔗 Related Projects

- [Twitchminert](https://github.com/rdavydov/Twitch-Channel-Points-Miner-v2) - Original Twitch Channel Points Miner
- [TwitchDropsMiner](https://github.com/DevilXD/TwitchDropsMiner) - Advanced Twitch drops mining
- [Twitch-Channel-Points-Miner](https://github.com/gottagofaster236/Twitch-Channel-Points-Miner) - Alternative implementation

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 📞 Credits

**Developed by**: [@DeoxiD](https://github.com/DeoxiD)

**Based on**:
- [Twitch-Channel-Points-Miner-v2](https://github.com/rdavydov/Twitch-Channel-Points-Miner-v2) by [@rdavydov](https://github.com/rdavydov)
- [TwitchDropsMiner](https://github.com/DevilXD/TwitchDropsMiner) by [@DevilXD](https://github.com/DevilXD)

---

**Version**: 2.0.0 (Hybrid Mining)  
**Last Updated**: January 16, 2026  
**Status**: ✅ Active Development

---

<div align="center">
  <p><strong>Made with ❤️ for the Twitch community</strong></p>
  <p><a href="https://github.com/DeoxiD/Twitchminert-GUI">⭐ Star us on GitHub!</a></p>
</div>
