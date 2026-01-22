# Debugging & Diagnostics Guide

## When User Reports Errors: ALWAYS Ask For

### 1. Stack Trace
- Complete error message and full stack trace
- When the error occurs (startup, mining, login, etc.)

### 2. System Information
- OS: Windows / macOS / Linux (which distro?)
- Python version: (run: python --version)
- Architecture: 32-bit or 64-bit
- Python installation method

### 3. Deployment Method
- Docker or Bare-metal Python?
- If Docker: version (docker --version)
- If Docker: Docker Compose version
- Any custom environment variables?

### 4. Command Used
- Exact command to start application
- Full console output from startup to error
- Did you run pip install -r requirements.txt?
- Fresh install or upgraded version?

### 5. Logs
- Full console output
- logs/twitchminert.log content
- Browser console errors (F12)
- docker-compose logs -f app (if Docker)

---

## Issue Localization to Specific Files

### STARTUP ERRORS (Before Port 5000)
Likely: config.py or app.py

Check in order:
1. config.py - Configuration loading and validation
2. app.py (create_app function) - Flask initialization  
3. requirements.txt - Dependency conflicts
4. .env file - Missing or malformed

**Debug Commands:**
```bash
python --version  # Should be 3.8+
pip show flask flask-cors sqlalchemy
python -c "from config import config; print(config)"
python -c "from app import app; print(app)"
```

---

### OAUTH / AUTHENTICATION ERRORS
Likely: core/auth.py, config.py, app.py

Check these files:
1. config.py - TWITCH_CLIENT_ID/SECRET validation
2. core/auth.py - OAuth2AuthenticationManager
3. app.py - /auth/login and /auth/callback routes

**Questions to Ask:**
- Are TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET in .env?
- Are they correct from Twitch Developer Console?
- Does TWITCH_REDIRECT_URI match exactly? (http://localhost:5000/auth/callback)
- Does it match Twitch console OAuth Redirect URLs exactly?

**Debug Commands:**
```bash
echo $TWITCH_CLIENT_ID
echo $TWITCH_CLIENT_SECRET
python -c "import os; print(os.environ.get('TWITCH_CLIENT_ID'))"
docker-compose exec app printenv | grep TWITCH
```

---

### DATABASE ERRORS
Likely: database_operations.py, models.py, config.py

Check these files:
1. database_operations.py - DB CRUD operations
2. database_operations_ext.py - Extended operations
3. models.py - SQLAlchemy model definitions
4. config.py - SQLALCHEMY_DATABASE_URI

**Questions to Ask:**
- Is another instance running?
- Is database file readable/writable?
- Is DATABASE_URL set correctly in .env?
- Do you have disk space?

**Debug Commands:**
```bash
ls -lah twitchminert.db
ls -la | grep .db
python -c "from app import db, create_app; app = create_app(); db.create_all()"
docker-compose exec app ls -lah /app/twitchminert.db
```

---

### MINING / DROPS ERRORS  
Likely: drops_miner.py or TwitchDropsMiner integration

Check these files:
1. drops_miner.py - Mining logic and campaign discovery
2. database_operations.py - CampaignOps operations
3. config.py - TWITCH_GQL_URL setting

**Questions to Ask:**
- Are you authenticated?
- Are there active drop campaigns right now?
- Is Twitch API responding?
- Are credentials still valid?

**This might be TwitchDropsMiner issue, not GUI:**
- Check: https://github.com/DevilXD/TwitchDropsMiner
- Check: https://status.twitch.tv
- Verify GraphQL endpoint is accessible

---

### WEB GUI ERRORS (500 errors)
Likely: app.py routes, templates, CORS

Check these files:
1. app.py - Flask routes and error handlers
2. web/templates/*.html - Template rendering
3. config.py - CORS_ORIGINS setting
4. requirements.txt - Flask/Jinja2 versions

**Debug Steps:**
1. Check browser console (F12) for JavaScript errors
2. Check Network tab for failed requests
3. Check terminal for Python errors
4. Check logs/twitchminert.log

---

### DOCKER-SPECIFIC ERRORS
Likely: docker-compose.yml or port conflicts

**Diagnosis Commands:**
```bash
docker-compose ps
docker-compose logs app
netstat -tulpn | grep 5000
lsof -i :5000
docker-compose exec app cat /app/.env
docker-compose down && docker-compose up --build -d
```

---

## Repository Structure for Debugging

```
Twitchminert-GUI/
├── app.py                    # Flask routes (CRITICAL)
├── config.py                 # Configuration (CRITICAL)
├── run.py                    # Startup script
├── models.py                 # Database schema
├── database_operations.py    # DB CRUD
├── drops_miner.py            # Mining logic (CRITICAL)
├── core/auth.py              # OAuth authentication
├── web/templates/            # HTML templates
├── logs/twitchminert.log     # Application logs
└── docker-compose.yml        # Docker config
```

---

## Common Error Patterns & Solutions

**ModuleNotFoundError**
→ Solution: pip install --upgrade -r requirements.txt

**Connection refused**
→ Solution: lsof -i :5000 (check if running)

**Permission denied**  
→ Solution: chmod 755 twitchminert.db

**CORS error**
→ Solution: Check config.py CORS_ORIGINS

**OAuth state mismatch**
→ Solution: Clear browser cookies, verify .env

---

## Error Report Template

```
## Error Description
[What's the issue?]

## Stack Trace  
[Full stack trace]

## System Info
- OS: [Windows/macOS/Linux]
- Python: [version]
- Deployment: [Docker/Bare-metal]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Logs
[Relevant log excerpts]
```

---

## Pre-Report Checklist

- [ ] Python 3.8+ installed
- [ ] pip install -r requirements.txt done
- [ ] .env file exists with Twitch credentials
- [ ] Port 5000 is available
- [ ] No other instances running
- [ ] Logs directory writable
- [ ] Database file writable
- [ ] Tried restarting app
- [ ] If Docker: ran docker-compose up --build

---

**Last Updated:** January 22, 2026
