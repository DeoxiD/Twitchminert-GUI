# Typical Workflow - Twitchminert-GUI

Step-by-step guide to get started with Twitchminert-GUI and manage your Twitch drops mining.

---

## 📋 Pre-Flight Checklist

Before starting, ensure you have:
- ✅ Python 3.8+ installed (or Docker)
- ✅ Git repository cloned
- ✅ Twitch account(s) to authorize
- ✅ Twitch Developer credentials
- ✅ About 5-10 minutes for initial setup

---

## 🚀 Complete Workflow

### Phase 1: Initial Setup (First Time Only)

#### Step 1.1: Fill Environment Configuration (.env)

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your favorite editor
nano .env
# OR
vim .env
```

**Required fields to fill:**

```env
# Flask/Security Configuration
SECRET_KEY=generate-a-random-key-here
FLASK_ENV=development

# Twitch OAuth Configuration
TWITCH_CLIENT_ID=your-client-id-from-twitch-console
TWITCH_CLIENT_SECRET=your-client-secret-from-twitch-console
TWITCH_REDIRECT_URI=http://localhost:5000/auth/callback

# Optional Configuration
PORT=5000
DATABASE_URL=sqlite:///twitchminert.db
FLASK_DEBUG=True  # Only for development
```

**Getting Twitch Credentials:**
1. Go to [Twitch Developer Console](https://dev.twitch.tv/console/apps)
2. Create a new application
3. Copy **Client ID** and generate **Client Secret**
4. Add OAuth Redirect URI: `http://localhost:5000/auth/callback`
5. Paste credentials into `.env`

---

#### Step 1.2: Initialize Database (If Needed)

The database is automatically created on first run, but you can manually initialize:

**Local Mode:**
```bash
# Database will be created automatically
# If you need to reset/initialize manually:
python -c "from app import create_app, db; app = create_app(); db.create_all()"
```

**Docker Mode:**
```bash
# Database initialization is automatic
# Docker container handles setup
```

**Database Contents:**
- User accounts and OAuth tokens
- Streamer configurations
- Drop mining history
- Channel points tracking
- Bet history
- Application settings

---

#### Step 1.3: Start Backend Service

**Option A: Local Python**
```bash
# Install dependencies first
pip install -r requirements.txt

# Start the application
python run.py

# OR directly with Flask
python app.py

# Expected output:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

**Option B: Docker**
```bash
# Start all services
docker compose up -d

# Check if running
docker compose ps

# View logs
docker compose logs -f app
```

**Verify Backend is Running:**
- Check for no errors in terminal
- Backend should respond to: `curl http://localhost:5000/api/status`
- Expected response: `{"status":"online","version":"2.0.0"}`

---

### Phase 2: Web Interface Setup

#### Step 2.1: Access Web GUI

**Open Browser:**
```
http://localhost:5000
```

**First Load:**
- You should see the login page
- You will be prompted to authorize with Twitch
- Click **"Login with Twitch"** button

---

#### Step 2.2: Authorize Twitch Account(s)

**OAuth Flow:**
1. Click **"Login with Twitch"** button
2. You will be redirected to Twitch
3. Log in with your Twitch account
4. Authorize the application to access your account
5. You will be redirected back to the GUI
6. Dashboard should now be accessible

**What Gets Authorized:**
- ✅ Read channel information
- ✅ Read user information
- ✅ Access drops campaigns
- ✅ Claim drops on your behalf
- ✅ View channel points

**Managing Multiple Accounts:**
- Go to **Settings** → **Twitch Accounts**
- Click **Add Account** to authorize another Twitch account
- Each account gets its own mining session
- Can run mining on multiple accounts simultaneously

---

#### Step 2.3: Configure Miner Settings

**Navigate to Settings:**
```
http://localhost:5000/settings
```

**Configure These Sections:**

**1. Mining Preferences**
- Auto-claim drops: ON/OFF
- Auto-switch channels: ON/OFF
- Mining check interval: 5 minutes (default)
- Idle timeout: 30 minutes

**2. Streamer List**
- Add target streamers to watch
- Set game preferences
- Enable/disable specific streamers

**3. Notification Settings**
- Email notifications (optional)
- Discord webhook (optional)
- Telegram notifications (optional)

**4. Bet Configuration**
- Enable channel points betting
- Bet amount per prediction
- Confidence threshold

**5. Database Settings**
- Database location (auto-configured)
- Backup frequency

---

### Phase 3: Active Mining Sessions

#### Step 3.1: Start Mining Session

**From Dashboard:**
1. Go to **http://localhost:5000**
2. View available Twitch drops campaigns
3. Click **Start Mining** button
4. Confirm streamer selection
5. Mining session begins

**What Happens:**
- ✅ Application connects to Twitch
- ✅ Discovers available drops campaigns
- ✅ Automatically watches streams
- ✅ Tracks watch time for each campaign
- ✅ Claims drops when eligible
- ✅ Switches channels automatically

**Monitor Mining Progress:**
- **Dashboard** shows real-time stats:
  - Active campaigns
  - Watch time per campaign
  - Drops claimed
  - Current channel
  - Session duration

---

#### Step 3.2: View Logs and Progress

**Access Logs Page:**
```
http://localhost:5000/logs
```

**Available Log Views:**
- **Mining Logs**: Campaign discovery and drops claimed
- **Authentication Logs**: OAuth token events
- **Error Logs**: Any issues encountered
- **Activity Logs**: Channel switches and API calls

**Log File Locations:**
- Local: `./logs/twitchminert.log`
- Docker: `/app/logs/twitchminert.log`

**Common Log Messages:**
```
[INFO] Campaign discovered: Elden Ring Drops
[INFO] Drop claimed: 50 channel points
[INFO] Switching to channel: example_streamer
[WARNING] Token expiring soon, refreshing...
[ERROR] Failed to claim drop: Invalid credentials
```

**Inspect Detailed Logs:**
```bash
# Local
tail -f logs/twitchminert.log

# Docker
docker compose logs -f app | grep -i mining
```

---

#### Step 3.3: View Drop Progress

**Drop Progress Tracking:**

**In Dashboard:**
- See all active campaigns
- Progress bars for each campaign
- Claimed rewards count
- Time remaining for campaign
- Next drop milestone

**Statistics Display:**
- Total drops claimed (session)
- Total points earned
- Channels watched
- Current watch time
- Success rate

**Campaign Details:**
- Game title
- Campaign name
- Duration remaining
- Reward value
- Claim status
- Required watch time

---

#### Step 3.4: Pause/Stop Mining

**Pause Mining (Keep Running):**
1. Click **Pause** button on dashboard
2. Application continues but doesn't claim drops
3. Watch time still accumulates
4. Click **Resume** to continue

**Stop Mining Session:**
1. Click **Stop** button
2. Current stream connection closes
3. Data is saved
4. Application remains running
5. Can start new session anytime

**Restart Mining:**
1. Click **Start Mining** again
2. Reconnect to Twitch
3. Resume dropped campaigns

---

## 📊 Real-Time Monitoring

### Dashboard Metrics

**Active Now:**
```
Active Campaigns: 3
Total Watch Time: 4 hours 23 minutes
Drop Claims Today: 12
Channel Points Earned: 2,500
```

**Current Session:**
- Active streamer
- Watch progress
- Upcoming drop
- Estimated claim time

**Performance:**
- Success rate
- Average claim time
- Uptime percentage

---

### API Endpoints (For Advanced Users)

**Status Check:**
```bash
curl http://localhost:5000/api/status
```

**Get Mining Status:**
```bash
curl http://localhost:5000/api/dashboard
```

**Get User Info:**
```bash
curl http://localhost:5000/api/user
```

**Get Streamers:**
```bash
curl http://localhost:5000/api/streamers
```

**API Documentation:**
```
http://localhost:5000/api/docs
```

---

## ⚙️ Advanced: Multiple Sessions

### Running Multiple Accounts

**Setup:**
1. Authorize multiple Twitch accounts in Settings
2. Create separate mining profiles for each
3. Assign different streamers to each profile

**Example Configuration:**
```
Account 1 (Main): Watch Elden Ring streams
Account 2 (Alt): Watch Baldur's Gate 3 streams
Account 3 (Farm): Watch promotional streams
```

**Benefits:**
- Multiple drops earned simultaneously
- Different reward tiers per account
- Independent mining sessions
- Spread watch time across games

---

## 🔧 Troubleshooting During Mining

### Common Issues

**Issue: "Not Authenticated"**
- Solution: Reauthorize in Settings → Re-login

**Issue: Drops Not Claiming**
- Check logs for errors
- Verify Twitch credentials are valid
- Ensure drops campaign is active

**Issue: Server Not Responding**
- Restart backend: `python run.py`
- Check port 5000 is available
- View logs for startup errors

**Issue: Database Locked**
- Restart application
- Check no other instances running
- Verify file permissions

---

## 📱 Session Management

### Save and Resume

**Auto-Save:**
- Mining progress auto-saves every minute
- Logs are continuously written
- Settings persist automatically

**Manual Save:**
- Click **Save Settings** in dashboard
- Export mining data (Settings → Export)

**Resume After Restart:**
1. Restart backend
2. Authenticate again
3. Mining history is preserved
4. Can resume previous campaigns

---

## 🎯 Typical Daily Routine

### Morning (Start of Day)
```
1. Start backend (python run.py)
2. Open browser (localhost:5000)
3. Authenticate if needed
4. Check for new campaigns in dashboard
5. Click "Start Mining"
6. Application runs in background
```

### Throughout Day
```
1. Check dashboard periodically
2. Monitor logs for errors
3. Observe drop progress
4. Add new streamers if campaigns appear
```

### Evening (End of Day)
```
1. Review mining statistics
2. Check drops claimed
3. Optional: Stop mining
4. Can leave running for overnight campaigns
5. Export logs if needed
```

---

## ✅ Success Checklist

- [ ] `.env` file configured with Twitch credentials
- [ ] Backend started without errors
- [ ] Web GUI accessible at localhost:5000
- [ ] Twitch account authorized
- [ ] Mining settings configured
- [ ] Mining session started
- [ ] Logs visible and error-free
- [ ] Drop progress showing on dashboard
- [ ] First drops claimed successfully

---

## 📞 Need Help?

- **Logs**: Check `/logs/twitchminert.log` for detailed error messages
- **Web UI**: Settings → Support for common issues
- **API Docs**: View interactive API at `/api/docs`
- **GitHub Issues**: Report bugs on [GitHub Issues](https://github.com/DeoxiD/Twitchminert-GUI/issues)

---

**Last Updated:** January 22, 2026
**Version:** 0.0.1-alpha
**Support:** Open a GitHub issue for help
