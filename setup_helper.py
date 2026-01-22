#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Helper and Installation Utilities for Twitchminert-GUI
Automated setup, environment validation, and configuration helpers
"""

import os
import sys
import subprocess
import platform
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

logger = logging.getLogger(__name__)


class EnvironmentValidator:
    """
    Validates system environment and dependencies
    """
    
    def __init__(self):
        self.issues: List[str] = []
        self.warnings: List[str] = []
        self.logger = logging.getLogger(__name__)
    
    def check_python_version(self, min_version: Tuple[int, int, int] = (3, 8, 0)) -> bool:
        """
        Check if Python version meets minimum requirements
        
        Args:
            min_version: Minimum required Python version
        
        Returns:
            True if version is adequate
        """
        current = sys.version_info[:3]
        if current < min_version:
            msg = f'Python {".".join(map(str, current))} found, minimum {".".join(map(str, min_version))} required'
            self.issues.append(msg)
            self.logger.error(msg)
            return False
        
        self.logger.info(f'Python version OK: {".".join(map(str, current))}')
        return True
    
    def check_command_exists(self, command: str) -> bool:
        """
        Check if a command is available in PATH
        
        Args:
            command: Command name to check
        
        Returns:
            True if command exists
        """
        if shutil.which(command):
            self.logger.debug(f'Command found: {command}')
            return True
        
        msg = f'Command not found: {command}'
        self.issues.append(msg)
        self.logger.warning(msg)
        return False
    
    def check_required_commands(self) -> Dict[str, bool]:
        """
        Check for commonly required commands
        
        Returns:
            Dictionary of command availability
        """
        commands = ['git', 'pip', 'python3']
        results = {cmd: self.check_command_exists(cmd) for cmd in commands}
        
        self.logger.info(f'Commands check complete: {results}')
        return results
    
    def check_file_exists(self, filepath: str) -> bool:
        """
        Check if file exists
        
        Args:
            filepath: Path to file
        
        Returns:
            True if file exists
        """
        path = Path(filepath)
        exists = path.exists()
        
        if exists:
            self.logger.debug(f'File exists: {filepath}')
        else:
            msg = f'Required file not found: {filepath}'
            self.issues.append(msg)
            self.logger.warning(msg)
        
        return exists
    
    def check_directory_writable(self, dirpath: str) -> bool:
        """
        Check if directory is writable
        
        Args:
            dirpath: Path to directory
        
        Returns:
            True if writable
        """
        path = Path(dirpath)
        path.mkdir(parents=True, exist_ok=True)
        
        test_file = path / '.write_test'
        try:
            test_file.touch()
            test_file.unlink()
            self.logger.debug(f'Directory writable: {dirpath}')
            return True
        except Exception as e:
            msg = f'Directory not writable: {dirpath} - {str(e)}'
            self.issues.append(msg)
            self.logger.error(msg)
            return False
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Get system information
        
        Returns:
            Dictionary with system info
        """
        info = {
            'python_version': f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}',
            'platform': platform.system(),
            'platform_release': platform.release(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor() or 'Unknown'
        }
        
        self.logger.info(f'System info: {info}')
        return info
    
    def validate_all(self) -> Tuple[bool, Dict[str, any]]:
        """
        Run all validation checks
        
        Returns:
            Tuple of (success boolean, results dictionary)
        """
        self.logger.info('Starting environment validation...')
        
        results = {
            'python_version': self.check_python_version(),
            'commands': self.check_required_commands(),
            'system_info': self.get_system_info(),
            'issues': self.issues,
            'warnings': self.warnings
        }
        
        success = len(self.issues) == 0
        self.logger.info(f'Validation complete: success={success}, issues={len(self.issues)}')
        
        return success, results


class EnvFileManager:
    """
    Manages .env file creation and validation
    """
    
    def __init__(self, env_path: str = '.env'):
        self.env_path = Path(env_path)
        self.logger = logging.getLogger(__name__)
    
    def create_env_template(self) -> str:
        """
        Create .env template with required variables
        
        Returns:
            Template content
        """
        template = """# Twitchminert-GUI Environment Configuration
# Copy this to .env and fill in your values

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=False
SECRET_KEY=change-me-in-production
PORT=5000

# Twitch OAuth Configuration
TWITCH_CLIENT_ID=your_client_id_here
TWITCH_CLIENT_SECRET=your_client_secret_here
TWITCH_REDIRECT_URI=http://localhost:5000/auth/callback

# Database Configuration
DATABASE_URL=sqlite:///twitchminert.db
# Alternative for PostgreSQL: postgresql://user:password@localhost/twitchminert

# Logging Configuration
LOG_LEVEL=INFO
LOG_DIR=logs

# API Configuration
API_TIMEOUT=30
API_RETRIES=3

# Miner Configuration
MINING_CHECK_INTERVAL=300
MINING_TIMEOUT=3600
"""
        return template
    
    def env_file_exists(self) -> bool:
        """
        Check if .env file exists
        
        Returns:
            True if .env exists
        """
        exists = self.env_path.exists()
        self.logger.info(f'.env file exists: {exists}')
        return exists
    
    def create_env_file(self, overwrite: bool = False) -> bool:
        """
        Create .env file from template
        
        Args:
            overwrite: Whether to overwrite existing file
        
        Returns:
            True if successful
        """
        if self.env_path.exists() and not overwrite:
            self.logger.warning('.env file already exists, skipping creation')
            return True
        
        try:
            template = self.create_env_template()
            self.env_path.write_text(template)
            self.logger.info(f'Created .env file: {self.env_path}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to create .env file: {str(e)}')
            return False
    
    def validate_env_file(self) -> Tuple[bool, List[str]]:
        """
        Validate that required variables are in .env
        
        Returns:
            Tuple of (valid, missing_vars)
        """
        required_vars = [
            'FLASK_ENV',
            'TWITCH_CLIENT_ID',
            'TWITCH_CLIENT_SECRET',
            'DATABASE_URL'
        ]
        
        if not self.env_file_exists():
            self.logger.error('.env file not found')
            return False, required_vars
        
        env_content = self.env_path.read_text()
        missing = [var for var in required_vars if var not in env_content]
        
        if missing:
            self.logger.warning(f'Missing variables in .env: {missing}')
        else:
            self.logger.info('.env file validation passed')
        
        return len(missing) == 0, missing


class DependencyInstaller:
    """
    Handles dependency installation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def install_requirements(self, requirements_file: str = 'requirements.txt') -> bool:
        """
        Install Python requirements
        
        Args:
            requirements_file: Path to requirements.txt
        
        Returns:
            True if installation successful
        """
        if not Path(requirements_file).exists():
            self.logger.error(f'Requirements file not found: {requirements_file}')
            return False
        
        try:
            self.logger.info(f'Installing requirements from {requirements_file}...')
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
            self.logger.info('Requirements installed successfully')
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f'Failed to install requirements: {str(e)}')
            return False
    
    def upgrade_pip(self) -> bool:
        """
        Upgrade pip to latest version
        
        Returns:
            True if upgrade successful
        """
        try:
            self.logger.info('Upgrading pip...')
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
            self.logger.info('Pip upgraded successfully')
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f'Failed to upgrade pip: {str(e)}')
            return False


class QuickSetup:
    """
    Automated quick setup wizard
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validator = EnvironmentValidator()
        self.env_manager = EnvFileManager()
        self.installer = DependencyInstaller()
    
    def run_setup(self, interactive: bool = True) -> bool:
        """
        Run complete setup process
        
        Args:
            interactive: Whether to prompt for input
        
        Returns:
            True if setup successful
        """
        self.logger.info('=== Twitchminert-GUI Quick Setup ===')
        
        # Step 1: Validate environment
        self.logger.info('Step 1: Validating environment...')
        success, results = self.validator.validate_all()
        if not success:
            self.logger.error('Environment validation failed. Please address the issues above.')
            return False
        
        # Step 2: Create .env file
        self.logger.info('Step 2: Setting up environment variables...')
        if not self.env_manager.env_file_exists():
            self.env_manager.create_env_file()
            self.logger.warning('Please edit .env file with your Twitch API credentials')
        
        # Step 3: Install dependencies
        self.logger.info('Step 3: Installing dependencies...')
        self.installer.upgrade_pip()
        if not self.installer.install_requirements():
            self.logger.error('Dependency installation failed')
            return False
        
        self.logger.info('=== Setup complete! ===')
        return True


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    setup = QuickSetup()
    success = setup.run_setup()
    
    if success:
        print('\nSetup completed successfully!')
        print('Next steps:')
        print('1. Edit .env file with your Twitch credentials')
        print('2. Run: python run.py')
    else:
        print('\nSetup failed. Please check the errors above.')
        sys.exit(1)
