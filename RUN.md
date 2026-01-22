# Quick Start Guide - Twitchminert-GUI

Simple instructions to run Twitchminert-GUI locally or with Docker.

---

## 🚀 Quick Start

### Option 1: Local Python Mode

#### Prerequisites
- Python 3.8+
- pip (Python package manager)

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: Configure Environment Variables
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` and add your Twitch credentials:
```env
SECRET_KEY=your-secret-key-here
TWITCH_CLIENT_ID=your-twitch-client-id
TWITCH_CLIENT_SECRET=your-twitch-client-secret
TWITCH_REDIRECT_URI=http://localhost:5000/auth/callback
FLASK_ENV=development
```

#### Step 3: Run the Application
```bash
python run.py
```

Or alternatively:
```bash
python app.py
```

#### Step 4: Open in Browser
```
http://localhost:5000
```

**Access Points:**
- Main Dashboard: `http://localhost:5000/`
- Settings: `http://localhost:5000/settings`
- Logs: `http://localhost:5000/logs`
- API Docs: `http://localhost:5000/api/docs`

---

### Option 2: Docker Mode

#### Prerequisites
- Docker
- Docker Compose

#### Step 1: Configure Environment
Edit `.env` file with your Twitch credentials (same as above)

#### Step 2: Start Services
```bash
docker compose up -d
```

#### Step 3: Open in Browser
```
http://localhost:5000
```

#### View Logs
```bash
docker compose logs -f app
```

#### Stop Services
```bash
docker compose down
```

---

### Option 3: Windows EXE (Pre-built)

1. Download the latest release from [Releases](https://github.com/DeoxiD/Twitchminert-GUI/releases)
2. Extract the `.zip` file
3. Run `Twitchminert-GUI.exe`
4. Open browser to `http://localhost:5000`

---

## 🔑 Getting Twitch Credentials

1. Go to [Twitch Developer Console](https://dev.twitch.tv/console/apps)
2. Log in with your Twitch account
3. Click "+ Create Application"
4. Fill in the form:
   - Application Name: `Twitchminert-GUI`
   - Application Category: `Analytics`
   - OAuth Redirect URLs: `http://localhost:5000/auth/callback`
5. Accept the terms and create
6. Click "Manage" to view your credentials
7. Copy `Client ID` and `Client Secret` to `.env` file

---

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | None | Flask secret key (generate new for production) |
| `TWITCH_CLIENT_ID` | Yes | None | Twitch API Client ID |
| `TWITCH_CLIENT_SECRET` | Yes | None | Twitch API Client Secret |
| `TWITCH_REDIRECT_URI` | No | `http://localhost:5000/auth/callback` | OAuth redirect URL |
| `FLASK_ENV` | No | `development` | Set to `production` for production |
| `PORT` | No | `5000` | Server port |
| `DATABASE_URL` | No | `sqlite:///twitchminert.db` | Database connection string |

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Change port in .env
PORT=5001
# Then access at http://localhost:5001
```

### Module Not Found Error
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Docker Connection Issues
```bash
# Check service status
docker compose ps

# View logs
docker compose logs app

# Rebuild containers
docker compose up -d --build
```

### OAuth Authentication Failed
1. Verify `TWITCH_CLIENT_ID` and `TWITCH_CLIENT_SECRET` are correct
2. Check `TWITCH_REDIRECT_URI` matches in Twitch console
3. Ensure OAuth URL in Twitch console: `http://localhost:5000/auth/callback`

---

## 📊 Accessing Different Sections

| URL | Purpose |
|-----|----------|
| `http://localhost:5000/` | Main Dashboard |
| `http://localhost:5000/settings` | Application Settings |
| `http://localhost:5000/logs` | Logs Viewer |
| `http://localhost:5000/api/docs` | API Documentation |
| `http://localhost:5000/api/status` | System Status |
| `http://localhost:5000/api/user` | User Information |

---

## 🐳 Docker Commands Reference

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Rebuild images
docker compose up -d --build

# Execute command in container
docker compose exec app bash

# Check service status
docker compose ps
```

---

## 📝 Notes

- Development mode auto-reloads on file changes
- Production deployment requires proper `.env` configuration
- Database is automatically created on first run
- OAuth tokens are stored securely
- API rate limiting is enabled in production

---

## 🔗 Additional Resources

- [Full README](README.md)
- [Code Review & Improvements](CODE_REVIEW_IMPROVEMENTS.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Environment Setup](ENVIRONMENT_SETUP.md)
- [Docker Setup](DOCKER_SETUP.md)
- [Twitch API Documentation](https://dev.twitch.tv/docs)

---

**Last Updated:** January 22, 2026
**Version:** 0.0.1-alpha
