# 🪟 Twitchminert-GUI - Windows Setup & EXE Build Guide

## ✅ Quick Start - Jau Sagatavots EXE

Ja vēlies tikai PALAIST aplikāciju bez izstrādes:

1. Lejupielādi **Twitchminert-GUI.exe** no [Releases](https://github.com/DeoxiD/Twitchminert-GUI/releases)
2. Dubultklikšķis uz .exe faila
3. Aplikācija atveras automātiski!

## 📋 Prasības (ja vēli pats veidot EXE)

- **Python 3.8+** ([lejupielāde](https://www.python.org/downloads/))
- **pip** (parasti nāk ar Python)
- **Windows OS** (7, 8, 10, 11)
- **4GB RAM** (ieteicams)
- **500MB brīvā vieta**

## 🚀 Instalācija un EXE Veidošana

### 1. Lejupielāde

```bash
git clone https://github.com/DeoxiD/Twitchminert-GUI.git
cd Twitchminert-GUI
```

Vai lejupielādi ZIP failu un izpaki to.

### 2. Piezīme - Python

```bash
python --version
```

Jāparāda **Python 3.8+**. Ja nē, instalē no [python.org](https://www.python.org/downloads/)

### 3. Virtuālā Vide (IETEICAMS)

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Instalē Atkarības

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### 5. Veidē EXE

```bash
python build_exe.py
```

**Gaidi ~3-5 minūtes** (PyInstaller veido standalone exe)

### 6. Palaisk EXE

```bash
.\dist\Twitchminert-GUI.exe
```

Vai atvērt `dist` mapi un dubultklikšķis uz `Twitchminert-GUI.exe`

## ⚙️ Konfigurācija

### Pirmajā Palaišanā:

1. EXE izveidos `.env` failu
2. Atvērt `.env` ar Notepad un ievadīt:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
TWITCH_CLIENT_ID=your-client-id
TWITCH_CLIENT_SECRET=your-client-secret
```

3. Pārstartēt aplikāciju

## 🔧 Problēmu Atrisināšana

### "python: command not found"

Python nav PATH. Instalē no [python.org](https://www.python.org/downloads/) un atzīmē "Add Python to PATH"

### "ModuleNotFoundError"

Instalē atkarības:
```bash
pip install -r requirements.txt
```

### EXE ir liels (~200MB)

Tas ir normāli! PyInstaller iekļauj visu Python runtime.

### Antivirusy Zvēr Brīdinājums

PyInstaller EXE dažreiz uzskatās par aizdomīgu (false positive). Ja uzticies projektam, pievienot izņēmumam.

## 📦 EXE Skaņošana

### Veidot ar OpenGL Atbalstu

```bash
python build_exe.py --windowed
```

### Veidot Debug Versiju

```bash
python build_exe.py --debug
```

## 🌐 Tīkla Konfigurācija

Ja izmanto firewall:

1. Atļaut **Twitchminert-GUI.exe** caur firewall
2. Pormāts: **5000** (vai `FLASK_PORT` vidē)

## 📝 Atkārtotas Veidošanas Pavediens

Ja mainīji kodu:

```bash
# Iztīri vecus build
rmdir /s build dist *.spec

# Veidē jaunu
python build_exe.py
```

## ✨ Ieteiktie Iestatījumi

**Production Versija:**
```env
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

**Development Versija:**
```env
FLASK_ENV=development
FLASK_DEBUG=True
```

## 🎯 Turpmākas Darbības

Pēc EXE iedarbības:

1. Atveri http://localhost:5000
2. Pierakstīties (default kredenciāli)
3. Konfigurēt Twitch kredenciālus
4. Sākt Twitchminert migrāciju!

---

**Nepieciešama Palīdzība?** Atvērt [Issues](https://github.com/DeoxiD/Twitchminert-GUI/issues)
