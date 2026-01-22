#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostics Integration Module for Twitchminert-GUI
Integrates logging, error tracking, and database inspection into unified interface
"""

import logging
from typing import Optional, Dict, Any
from logging_utils import setup_logging, ContextLogger, log_performance
from db_inspector import DatabaseInspector, QueryBuilder
from error_tracker import ErrorTracker, DiagnosticReport


class DiagnosticsManager:
    """
    Unified diagnostics manager combining all diagnostic tools
    """
    
    def __init__(self, db_session=None, log_dir: str = 'logs'):
        """
        Initialize diagnostics manager
        
        Args:
            db_session: SQLAlchemy session for database operations
            log_dir: Directory for log files
        """
        # Setup logging
        self.logger = setup_logging(log_dir=log_dir)
        self.logger.info('DiagnosticsManager initialized')
        
        # Initialize error tracking
        self.error_tracker = ErrorTracker(max_errors=100)
        self.diagnostic_report = DiagnosticReport(self.error_tracker)
        
        # Initialize database inspection if session provided
        self.db_inspector = None
        self.query_builder = QueryBuilder()
        if db_session:
            self.db_inspector = DatabaseInspector(db_session)
            self.logger.debug('Database inspector initialized')
    
    def create_context_logger(self, context_name: str) -> ContextLogger:
        """
        Create a context logger for operation tracking
        
        Args:
            context_name: Name of the operation/context
        
        Returns:
            ContextLogger instance
        """
        return ContextLogger(context_name)
    
    def track_error(self, exception: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Track an exception and return error context
        
        Args:
            exception: The exception to track
            context: Optional context data
        
        Returns:
            Error context dictionary
        """
        error_context = self.error_tracker.track_exception(exception, context)
        return error_context.to_dict()
    
    def get_database_health(self) -> Dict[str, Any]:
        """
        Get database health status
        
        Returns:
            Health check result
        """
        if not self.db_inspector:
            return {'status': 'error', 'message': 'Database inspector not initialized'}
        
        return self.db_inspector.health_check()
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics
        
        Returns:
            Database statistics
        """
        if not self.db_inspector:
            return {'error': 'Database inspector not initialized'}
        
        return self.db_inspector.get_database_stats()
    
    def execute_query(self, query_string: str) -> list:
        """
        Execute SQL query
        
        Args:
            query_string: SQL query to execute
        
        Returns:
            Query results
        """
        if not self.db_inspector:
            self.logger.error('Database inspector not initialized')
            return []
        
        return self.db_inspector.execute_raw_query(query_string)
    
    def get_error_summary(self) -> Dict[str, Any]:
        """
        Get summary of tracked errors
        
        Returns:
            Error summary
        """
        return self.error_tracker.get_error_summary()
    
    def generate_diagnostic_report(self, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate comprehensive diagnostic report
        
        Args:
            filename: Optional filename to save report
        
        Returns:
            Diagnostic report
        """
        report = self.diagnostic_report.generate_report()
        
        if filename:
            self.diagnostic_report.save_report(filename)
            self.logger.info(f'Diagnostic report saved to {filename}')
        
        return report
    
    def get_recent_errors(self, count: int = 10) -> list:
        """
        Get recent tracked errors
        
        Args:
            count: Number of errors to return
        
        Returns:
            List of error contexts
        """
        errors = self.error_tracker.get_recent_errors(count)
        return [error.to_dict() for error in errors]
    
    def log_info(self, message: str, **kwargs) -> None:
        """Log info message"""
        self.logger.info(f'{message} | {kwargs}' if kwargs else message)
    
    def log_warning(self, message: str, **kwargs) -> None:
        """Log warning message"""
        self.logger.warning(f'{message} | {kwargs}' if kwargs else message)
    
    def log_error(self, message: str, **kwargs) -> None:
        """Log error message"""
        self.logger.error(f'{message} | {kwargs}' if kwargs else message)
    
    def log_debug(self, message: str, **kwargs) -> None:
        """Log debug message"""
        self.logger.debug(f'{message} | {kwargs}' if kwargs else message)


if __name__ == '__main__':
    import json
    
    # Initialize diagnostics
    diag = DiagnosticsManager(log_dir='logs')
    
    # Test logging
    diag.log_info('Diagnostics system started', version='1.0')
    
    # Test error tracking
    try:
        x = 1 / 0
    except Exception as e:
        error_info = diag.track_error(e, {'user_id': 'test_user', 'action': 'division'})
        diag.log_error('Caught exception', error_type=error_info['error_type'])
    
    # Test context logger
    ctx = diag.create_context_logger('test_operation')
    ctx.info('Operation starting', user_id='test_user')
    ctx.log_summary()
    
    # Generate report
    report = diag.generate_diagnostic_report('diagnostic_report.json')
    diag.log_info('Diagnostic report generated', report_size=len(str(report)))
    
    # Print summary
    print('\nError Summary:')
    print(json.dumps(diag.get_error_summary(), indent=2, default=str))
    
    print('\nRecent Errors:')
    print(json.dumps(diag.get_recent_errors(5), indent=2, default=str))
