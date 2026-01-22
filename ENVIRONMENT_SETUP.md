# Environment Setup Guide for Twitchminert-GUI

This guide provides step-by-step instructions for setting up the development environment on both Windows and Linux/macOS systems.

## Prerequisites

- Python 3.11 or higher
- Git (optional, for cloning the repository)
- pip (Python package manager)

---

## Windows Setup

### Step 1: Create Virtual Environment
```batch
py -3.11 -m venv venv
```

**Alternative (if py command is not available):**
```batch
python -m venv venv
```

### Step 2: Activate Virtual Environment
```batch
venv\Scripts\activate
```

You should see `(venv)` appear in your command prompt.

### Step 3: Install Dependencies
```batch
pip install -r requirements.txt
```

### Step 4: Verify Installation
```batch
pip list
python --version
```

---

## Linux / macOS Setup

### Step 1: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 2: Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` appear in your shell prompt.

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
pip list
python3 --version
```

---

## Running the Application

Once the virtual environment is activated and dependencies are installed:

### Windows
```batch
python app.py
```

### Linux / macOS
```bash
python3 app.py
```

---

## Deactivating Virtual Environment

When you're done working, deactivate the virtual environment:

### Windows
```batch
venv\Scripts\deactivate
```

### Linux / macOS
```bash
deactivate
```

---

## Troubleshooting

### Windows: `venv\Scripts\activate` doesn't work
Try using the batch file instead:
```batch
venv\Scripts\activate.bat
```

Or use PowerShell:
```powershell
venv\Scripts\Activate.ps1
```

### Python version not found
Make sure Python 3.11+ is installed and added to your PATH.
Check your Python version:
```bash
python --version  # Windows
python3 --version  # Linux/macOS
```

### Permission denied on Linux/macOS
If you get permission errors, try:
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

### pip install fails
Upgrade pip first:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Additional Information

- **Virtual Environment**: Isolates project dependencies from your system Python
- **requirements.txt**: Contains all project dependencies and their versions
- **Python 3.11+**: Required for compatibility with modern Flask and SQLAlchemy features

For more information, see the project README.md file.
