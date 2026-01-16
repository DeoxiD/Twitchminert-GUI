# 🪟 Twitchminert-GUI - Windows Setup & EXE Build Guide

## ✅ Quick Start - Pre-Built EXE

If you just want to RUN the application without development:

1. Download **Twitchminert-GUI.exe** from [Releases](https://github.com/DeoxiD/Twitchminert-GUI/releases)
2. Double-click the .exe file
3. Application starts automatically!

## 📋 Requirements (if you want to build EXE yourself)

- **Python 3.8+** ([download](https://www.python.org/downloads/))
- **pip** (usually comes with Python)
- **Windows OS** (7, 8, 10, 11)
- **4GB RAM** (recommended)
- **500MB free space**

## 🚀 Installation and EXE Building

### 1. Download

```bash
git clone https://github.com/DeoxiD/Twitchminert-GUI.git
cd Twitchminert-GUI
```

Or download ZIP file and extract it.

### 2. Check Python

```bash
python --version
```

Should show **Python 3.8+**. If not, install from [python.org](https://www.python.org/downloads/)

### 3. Virtual Environment (RECOMMENDED)

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### 5. Build EXE

```bash
python build_exe.py
```

**Wait ~3-5 minutes** (PyInstaller builds standalone exe)

### 6. Run EXE

```bash
.\dist\Twitchminert-GUI.exe
```

Or open `dist` folder and double-click `Twitchminert-GUI.exe`

## ⚙️ Configuration After Installation

After starting the application:

1. Open http://localhost:5000 in your browser
2. Follow the configuration wizard
3. Enter your Twitch credentials
4. Select your preferred betting strategy
5. Start mining!

## 🔧 Troubleshooting

### Python not found

- Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation
- Restart your computer after installation

### EXE fails to start

- Try running as Administrator
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Windows Defender didn't block the file (add to exceptions)

### Port 5000 is already in use

- Change the port in `config.py` line: `app.run(port=5000)` → `app.run(port=5001)`

## 📝 Building from Source (Advanced)

For developers who want to modify the code:

1. Follow steps 1-4 above
2. Edit files in the `web/` and `core/` directories
3. Run locally: `python run.py`
4. Build EXE when ready: `python build_exe.py`

## 📄 Notes

- The EXE is standalone and doesn't require Python to be installed
- All configuration is stored in `.env` file
- Logs are saved in the `logs/` folder
- Database is SQLite and stored as `twitchminert.db`

## 🆘 Support

Have issues? Check [GitHub Issues](https://github.com/DeoxiD/Twitchminert-GUI/issues)

**Last Updated**: January 2026
