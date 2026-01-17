#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twitchminert-GUI - EXE Builder Script
Builds a Windows executable using PyInstaller
"""

import os
import sys
import PyInstaller.__main__
from pathlib import Path

def build_exe():
    """Build standalone EXE using PyInstaller"""
    
    # Project root
    project_root = Path(__file__).parent
    
    # PyInstaller options
    options = [
        'run.py',
        '--name=Twitchminert-GUI',
        '--onefile',
        '--windowed',
        '--icon=NONE',
        f'--distpath={project_root / "dist"}',
        f'--workpath={project_root / "build"}',
        f'--specpath={project_root / "build"}',
        '--hidden-import=flask_cors',
        '--hidden-import=flask_sqlalchemy',
        '--hidden-import=flask_jwt_extended',
        '--collect-all=flask',
        '--collect-all=jinja2',
        '--collect-all=click',
        '--collect-all=werkzeug',
    ]
    
    print('Building Twitchminert-GUI EXE...')
    print('This may take a few minutes...')
    print()
    
    try:
        PyInstaller.__main__.run(options)
        print()
        print('✓ Build successful!')
        print(f'EXE location: {project_root / "dist" / "Twitchminert-GUI.exe"}')
        print()
        print('You can now run: .\\dist\\Twitchminert-GUI.exe')
        
    except Exception as e:
        print(f'✗ Build failed: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print('PyInstaller is not installed!')
        print('Install it with: pip install pyinstaller')
        sys.exit(1)
    
    build_exe()
