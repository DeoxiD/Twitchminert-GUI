#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Logging Utilities for Twitchminert-GUI
Provides comprehensive logging with file rotation, context tracking, and performance monitoring
"""

import logging
import logging.handlers
import sys
import time
import traceback
import json
from datetime import datetime
from pathlib import Path
from functools import wraps
from typing import Optional, Dict, Any, Callable


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for terminal output"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[41m', # Red background
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(log_dir: str = 'logs', level: int = logging.DEBUG) -> logging.Logger:
    """
    Configure and return logger with file and console handlers
    
    Args:
        log_dir: Directory for log files
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    # Create logs directory
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('twitchminert')
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_path / f"twitchminert_{datetime.now().strftime('%Y%m%d')}.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(log_format, datefmt=date_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


def log_performance(threshold: float = 1.0) -> Callable:
    """
    Decorator to log function execution time and warn if threshold exceeded
    
    Args:
        threshold: Time in seconds to consider operation as slow
    
    Example:
        @log_performance(threshold=2.0)
        def slow_function():
            time.sleep(1.5)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger('twitchminert')
            func_name = func.__name__
            start_time = time.time()
            
            logger.debug(f'Starting {func_name} with args={args[:2]}..., kwargs={list(kwargs.keys())}')
            
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                
                if elapsed > threshold:
                    logger.warning(f'{func_name} took {elapsed:.3f}s (SLOW - threshold: {threshold}s)')
                else:
                    logger.debug(f'{func_name} completed in {elapsed:.3f}s')
                
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f'{func_name} failed after {elapsed:.3f}s: {type(e).__name__}')
                logger.debug(f'Exception details: {str(e)}')
                raise
        
        return wrapper
    return decorator


def log_exception(func: Callable) -> Callable:
    """
    Decorator to log full exception details including traceback and context
    
    Example:
        @log_exception
        def risky_function():
            raise ValueError('Something went wrong')
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger('twitchminert')
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f'Exception in {func.__name__}: {type(e).__name__}: {str(e)}')
            logger.debug(f'Traceback:\n{traceback.format_exc()}')
            raise
    return wrapper


class ContextLogger:
    """
    Logger wrapper that tracks request/operation context throughout execution
    Useful for tracing issues across multiple functions
    """
    
    def __init__(self, context_name: str):
        self.logger = logging.getLogger('twitchminert')
        self.context_name = context_name
        self.context_data: Dict[str, Any] = {}
        self.start_time = time.time()
    
    def set_context(self, key: str, value: Any) -> None:
        """Set context value"""
        self.context_data[key] = value
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with context"""
        full_msg = f"[{self.context_name}] {message}"
        if kwargs:
            full_msg += f" | Context: {json.dumps(kwargs, default=str)}"
        self.logger.debug(full_msg)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message with context"""
        full_msg = f"[{self.context_name}] {message}"
        if kwargs:
            full_msg += f" | {json.dumps(kwargs, default=str)}"
        self.logger.info(full_msg)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with context"""
        full_msg = f"[{self.context_name}] {message}"
        if kwargs:
            full_msg += f" | {json.dumps(kwargs, default=str)}"
        self.logger.warning(full_msg)
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs) -> None:
        """Log error message with context and optional exception"""
        full_msg = f"[{self.context_name}] {message}"
        if exception:
            full_msg += f" | Exception: {type(exception).__name__}: {str(exception)}"
        if kwargs:
            full_msg += f" | {json.dumps(kwargs, default=str)}"
        self.logger.error(full_msg)
    
    def get_elapsed(self) -> float:
        """Get elapsed time since context creation"""
        return time.time() - self.start_time
    
    def log_summary(self) -> None:
        """Log summary of context execution"""
        elapsed = self.get_elapsed()
        self.info(f"Context '{self.context_name}' completed", elapsed_seconds=f"{elapsed:.2f}")


if __name__ == '__main__':
    # Test logging setup
    logger = setup_logging()
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    
    # Test performance logging
    @log_performance(threshold=0.1)
    def test_function():
        time.sleep(0.15)
        return 'Done'
    
    result = test_function()
    logger.info(f'Test result: {result}')
    
    # Test context logger
    ctx_logger = ContextLogger('test_operation')
    ctx_logger.set_context('user_id', '12345')
    ctx_logger.info('Starting operation', user_id='12345', action='test')
    ctx_logger.log_summary()
