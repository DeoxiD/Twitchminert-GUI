# Twitchminert-GUI

**Advanced Hybrid Twitch Miner - Drops + Channel Points Automation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask 2.3+](https://img.shields.io/badge/Flask-2.3%2B-green.svg)](https://flask.palletsprojects.com/)
[![Docker Supported](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

> Twitchminert-GUI ir moderns, lietotājiem draudzīgs **web-bazēts interfeiss** Twitch kanālu punktu automatizācijai ar reāllaika vadības paneļi, konfigurācijas vedni, analītiku un paziņojumiem.

---

## ✨ Funkcionalitāte

### 📊 Vadības panelis
- ✅ Reāllaika strīmera statusa uzraudzīšana
- ✅ Tiešraides kanāla punktu sliedzība
- ✅ Sesijas statistika un analītika
- ✅ Nesenie derības ieraksti
- ✅ Vizuālie veiktspējas rādītāji
- ✅ REST API galapunkti

### ⚙️ Konfigurācijas vednis
- ✅ Soli pa solim iestatīšanas process
- ✅ Twitch OAuth autentifikācija
- ✅ Automatizēts sekotāju saraksta imports
- ✅ Pielāgojamas derības stratēģijas (SMART, MOST_VOTED, HIGH_ODDS, PERCENTAGE)
- ✅ Uz sekotāju orientēti iestatījumi
- ✅ Filtrēšanas nosacījumi un derības ierobežojumi

### 🎮 Derību sistēma
- ✅ Vairākas stratēģijas atbalsts
  - **SMART**: Intelektuāls lēmuma pieņemšana, pamatojoties uz izpeļņu un populāritāti
  - **MOST_VOTED**: Sekot pūļa vairākumam
  - **HIGH_ODDS**: Derības ar augstākajiem izpeļņiem
  - **PERCENTAGE**: Automātiskā likme ar fiksētu procentu
- ✅ Derību ierobežojumi un filtrēšana
- ✅ Tūtoriales un galvenie attiecīgie ņu ieteikumi

### 🌍 Papildus Funkcionalitāte
- ✅ Daudzvalodu atbalsts (EN/LV)
- ✅ Gaisa brāļu savienošana
- ✅ Drošai paziņošanai
- ✅ Detalizēta žurnalizācija

---

## 📦 Instalācija

### Prasības
- Python 3.8 vai jaunāks
- pip vai conda
- Git
- Modernis pārlūks

### Opcija 1: Python tiešā instalācija

```bash
# Klonējiet repozitoriju
git clone https://github.com/DeoxiD/Twitchminert-GUI.git
cd Twitchminert-GUI

# Izveidojiet virtuālo vidi
python -m venv venv

# Aktivizējiet virtuālo vidi
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalējiet atkarības
pip install -r requirements.txt

# Palaidiet lietojumprogrammu
python run.py
```

### Opcija 2: Windows EXE

```bash
# Izveidojiet autonomu .exe failu
python build_exe.py

# Palaidiet
.\dist\Twitchminert-GUI.exe
```

### Opcija 3: Docker

```bash
# Izveidojiet Docker attēlu
docker build -t twitchminert-gui .

# Palaidiet konteineri
docker run -p 5000:5000 twitchminert-gui
```

---

## ⚙️ Konfigurācija

### Vides mainīgie

Izveidojiet `.env` failu projekta saknes direktorijā ar šādiem mainīgajiem:

```env
# Twitch API
TWITCH_CLIENT_ID=jūsu-klienta-id
TWITCH_CLIENT_SECRET=jūsu-klienta-noslēpums
TWITCH_REDIRECT_URI=http://localhost:5000/callback

# Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=jūsu-slepens-atslega

# Datu bāze
DATABASE_URL=sqlite:///twitchminert.db

# Paziņojumi (opcija)
TELEGRAM_BOT_TOKEN=jūsu-bota-pilnvara
DISCORD_WEBHOOK_URL=jūsu-discord-webhook
```

### OAuth Reģistrācija

1. Dodieties uz [Twitch Developer Console](https://dev.twitch.tv/console/apps)
2. Izveidojiet jaunu lietojumprogrammu
3. Nokopējiet **Client ID** un **Client Secret**
4. Ievietojiet `.env` failā

---

## 🚀 Sākšana

### Palaist caur termināli

```bash
# Aktivizējiet virtuālo vidi
venv\Scripts\activate  # Windows

# Palaidiet lietojumprogrammu
python run.py

# Pārlūkā atvērt
http://localhost:5000
```

### Atrašanās vieta

- **Vadības panelis**: http://localhost:5000/
- **Iestatījumi**: http://localhost:5000/settings
- **Žurnāls**: http://localhost:5000/logs
- **API dokumentācija**: http://localhost:5000/api/docs

---

## 📁 Projekta Struktūra

```
Twitchminert-GUI/
├── core/                    # Galvenās modulis
│   ├── __init__.py
│   ├── auth.py             # Twitch OAuth autentifikācija
│   ├── drops.py            # Drops ieguves modulis
│   ├── points.py           # Kanāla punktu modulis
│   ├── scheduler.py        # Uzdevumu plānotājs
│   └── twitch_client.py    # Twitch API klients
├── web/                     # Web interfeiss
│   ├── __init__.py
│   ├── app.py              # Flask lietojumprogramma
│   ├── routes.py           # API maršruti
│   ├── templates/
│   │   └── index.html      # Galvenā lapā
│   └── static/
│       ├── style.css       # Stili
│       └── script.js       # Skriptošana
├── .env.example            # Vides maiņības paraugs
├── requirements.txt        # Python atkarības
├── run.py                  # Ieejas punkts
├── config.py               # Konfigurācijas klasės
├── build_exe.py            # Windows EXE veidošana
└── README.md               # Šī dokumentācija
```

---

## 🔌 API Galapunkti

### Status
```bash
GET /api/status
# Atgriež maineris status
```

### Konfigurācija
```bash
GET /api/config
# Iegūst pašreizējos iestatījumus

POST /api/config
# Saglabā jaunus iestatījumus
```

### Strīmeri
```bash
GET /api/streamers
# Saraksts ar visiem strīmēriem

POST /api/streamers
# Pievieno jaunu strīmeri
```

### Vadības
```bash
POST /api/start
# Palaist maineris

POST /api/stop
# Apturēt maineris
```

---

## 🛠️ Attīstība

### Vietējā iestatīšana

```bash
# Instalējiet attīstības atkarības
pip install -r requirements-dev.txt

# Palaidiet testus
python -m pytest

# Palaist linter
flake8 . --count --select=E9,F63,F7,F82 --show-source
```

---

## 📜 Licenzija

MIT License - Skatiet [LICENSE](LICENSE) failu detalizētai informācijai.

---

## 🤝 Ieguldījums

Ieguldījumi ir svārsti! Skatiet [CONTRIBUTING.md](CONTRIBUTING.md) norādījumi.

---

## ⚠️ Atrunas

- Šī lietojumprogramma ir neatkarīga no Twitch Inc.
- Jūs esat atbildīgs par Twitch Pakalpojuma Noteikumu ievērošanu
- Autori nav atbildīgi par jebkādiem problēmām vai ban riskiem

---

## 📞 Atbalsts

Jautājumi vai problēmas? Atvērt [GitHub Issues](https://github.com/DeoxiD/Twitchminert-GUI/issues)

---

**Pēdējais atjauninājums**: 2026. gada janvāris
