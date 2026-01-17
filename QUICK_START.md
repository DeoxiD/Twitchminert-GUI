# 🚀 Quick Start Guide - Twitchminert-GUI

## ✅ Priekšnosacījumi

Pirms sākšanas pārliecinies, ka tev ir:

- **Python 3.8+** instalēts
- **Git** instalēts
- **Twitch Developer Account** (bezmaksas)
- Moderna pārlūkprogramma (Chrome, Firefox, Edge)

## 📦 Instalācija

### 1. Klonē repozitoriju

```bash
git clone https://github.com/DeoxiD/Twitchminert-GUI.git
cd Twitchminert-GUI
```

### 2. Izveido virtuālo vidi

**Windows:**
```bash
python -m venv venv
venv\\Scripts\\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalē dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Twitch API Konfigurācija

### 1. Reģistrē aplikāciju Twitch Developer Console

1. Apmeklē [https://dev.twitch.tv/console/apps](https://dev.twitch.tv/console/apps)
2. Klikšķini uz **"Register Your Application"**
3. Aizpildi formu:
   - **Name**: `Twitchminert-GUI` (vai jebkuru citu nosaukumu)
   - **OAuth Redirect URLs**: `http://localhost:5000/auth/callback`
   - **Category**: Izvēlies "Application Integration"
4. Klikšķini **"Create"**
5. Kopē **Client ID** un ģenerē jaunu **Client Secret**

### 2. Konfigurē .env failu

1. Kopē piemēra failu:
```bash
cp .env.example .env
```

2. Rediģē `.env` failu un aizpildi savus datus:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_APP=app.py

# Secret Key (ģenerē drošu atslēgu)
SECRET_KEY=tava-droša-atslēga-šeit

# Twitch API Credentials
TWITCH_CLIENT_ID=tavs-client-id-šeit
TWITCH_CLIENT_SECRET=tavs-client-secret-šeit
TWITCH_REDIRECT_URI=http://localhost:5000/auth/callback

# Database
DATABASE_URL=sqlite:///twitchminert.db
```

### 3. Ģenerē drošu SECRET_KEY (izvēles)

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🚀 Palaišana

### Standarta metode

```bash
python run.py
```

### Alternatīvā metode

```bash
python app.py
```

### Ar Docker

```bash
docker-compose up --build
```

## 🎯 Piekļuve aplikācijai

Pēc palaišanas, atver pārlūkprogrammu un dodies uz:

**Dashboard**: [http://localhost:5000](http://localhost:5000)

Tev vajadzētu redzēt galveno lapu ar OAuth2 autentifikācijas pogu.

## 🔐 Autentifikācija

1. Klikšķini uz **"Login with Twitch"** pogas
2. Autorizē aplikāciju (pirmo reizi)
3. Tiks automātiski novirzīts atpakaļ uz dashboard
4. Tagad vari sākt izmantot aplikāciju!

## 📊 Funkciju pārskats

### Dashboard (Galvenā lapa)
- Real-time streamer statuss
- Channel points tracking
- Session statistika
- Recent bet history

### Settings (Iestatījumi)
- Betting strategy konfigurācija
- Follower import
- Notification settings

### Logs (Logfaili)
- Real-time logging
- Error tracking

## ⚠️ Biežākās problēmas

### Port 5000 jau ir aizņemts

Mainīt portu `.env` failā:
```env
FLASK_PORT=5001
```

### Import kļūdas

Pārliecinies, ka virtual environment ir aktivizēta un visas dependencies ir instalētas:
```bash
pip install -r requirements.txt
```

### Template not found

Pārliecinies, ka esi projekta saknes mapē un ka `web/templates/` mape eksistē.

### OAuth callback nestrādā

Pārbaudi vai Twitch Developer Console ir pareizi iestatīts redirect URI: `http://localhost:5000/auth/callback`

## 📚 Papildu resursi

- [README.md](README.md) - Pilna dokumentācija
- [SETUP_WINDOWS.md](SETUP_WINDOWS.md) - Windows specifiskā setup instrukcija
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

## 🐛 Support

Ja rodas problēmas, izveido Issue GitHub repozitorijā:
[https://github.com/DeoxiD/Twitchminert-GUI/issues](https://github.com/DeoxiD/Twitchminert-GUI/issues)

---

**Veiksmīgu mining! 🎉**
