#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Error Tracking and Diagnostics Module for Twitchminert-GUI
Provides comprehensive error tracking, context collection, and diagnostics utilities
"""

import logging
import traceback
import json
import sys
import platform
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import os


@dataclass
class ErrorContext:
    """
    Captures full error context for debugging
    """
    timestamp: str
    error_type: str
    error_message: str
    file_path: str
    function_name: str
    line_number: int
    stack_trace: str
    user_context: Dict[str, Any]
    system_info: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2, default=str)


class ErrorTracker:
    """
    Comprehensive error tracking and diagnostics
    """
    
    def __init__(self, max_errors: int = 100):
        """
        Initialize error tracker
        
        Args:
            max_errors: Maximum number of errors to track in memory
        """
        self.logger = logging.getLogger('twitchminert')
        self.errors: List[ErrorContext] = []
        self.max_errors = max_errors
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Collect system information for debugging
        
        Returns:
            Dictionary with system information
        """
        return {
            'python_version': platform.python_version(),
            'platform': platform.system(),
            'platform_release': platform.release(),
            'processor': platform.processor(),
            'python_implementation': platform.python_implementation(),
            'working_directory': os.getcwd()
        }
    
    def track_exception(self, exception: Exception, user_context: Optional[Dict[str, Any]] = None) -> ErrorContext:
        """
        Track an exception with full context
        
        Args:
            exception: The exception to track
            user_context: Optional user-provided context data
        
        Returns:
            ErrorContext object
        """
        tb = traceback.extract_tb(exception.__traceback__)
        frame = tb[-1]  # Get last frame
        
        context = ErrorContext(
            timestamp=datetime.now().isoformat(),
            error_type=type(exception).__name__,
            error_message=str(exception),
            file_path=frame.filename,
            function_name=frame.name,
            line_number=frame.lineno,
            stack_trace=traceback.format_exc(),
            user_context=user_context or {},
            system_info=self.get_system_info()
        )
        
        # Store error
        self.errors.append(context)
        if len(self.errors) > self.max_errors:
            self.errors.pop(0)
        
        # Log error
        self.logger.error(
            f'Exception tracked: {context.error_type} in {context.function_name} '
            f'({context.file_path}:{context.line_number})'
        )
        self.logger.debug(f'Error context: {context.to_json()}')
        
        return context
    
    def get_recent_errors(self, count: int = 10) -> List[ErrorContext]:
        """
        Get recent tracked errors
        
        Args:
            count: Number of recent errors to return
        
        Returns:
            List of ErrorContext objects
        """
        return self.errors[-count:]
    
    def get_error_summary(self) -> Dict[str, Any]:
        """
        Get summary of tracked errors
        
        Returns:
            Summary statistics
        """
        summary = {
            'total_errors': len(self.errors),
            'error_types': {},
            'most_common_error': None,
            'earliest_error': None,
            'latest_error': None
        }
        
        if self.errors:
            # Count error types
            for error in self.errors:
                error_type = error.error_type
                summary['error_types'][error_type] = summary['error_types'].get(error_type, 0) + 1
            
            # Find most common
            if summary['error_types']:
                summary['most_common_error'] = max(summary['error_types'].items(), key=lambda x: x[1])[0]
            
            summary['earliest_error'] = self.errors[0].timestamp
            summary['latest_error'] = self.errors[-1].timestamp
        
        return summary
    
    def clear_errors(self) -> None:
        """
        Clear all tracked errors
        """
        self.errors.clear()
        self.logger.info('Error tracker cleared')


class DiagnosticReport:
    """
    Generate comprehensive diagnostic reports
    """
    
    def __init__(self, error_tracker: ErrorTracker):
        """
        Initialize diagnostic report generator
        
        Args:
            error_tracker: ErrorTracker instance
        """
        self.error_tracker = error_tracker
        self.logger = logging.getLogger('twitchminert')
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive diagnostic report
        
        Returns:
            Diagnostic report dictionary
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'system_info': self.error_tracker.get_system_info(),
            'error_summary': self.error_tracker.get_error_summary(),
            'recent_errors': [
                error.to_dict() for error in self.error_tracker.get_recent_errors(5)
            ]
        }
        
        self.logger.info('Diagnostic report generated')
        return report
    
    def generate_report_json(self) -> str:
        """
        Generate report as JSON string
        
        Returns:
            JSON report
        """
        report = self.generate_report()
        return json.dumps(report, indent=2, default=str)
    
    def save_report(self, filename: str) -> bool:
        """
        Save diagnostic report to file
        
        Args:
            filename: Path to save report
        
        Returns:
            True if successful
        """
        try:
            report_json = self.generate_report_json()
            with open(filename, 'w') as f:
                f.write(report_json)
            self.logger.info(f'Diagnostic report saved to {filename}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to save diagnostic report: {e}')
            return False


if __name__ == '__main__':
    # Test error tracking
    logging.basicConfig(level=logging.DEBUG)
    
    tracker = ErrorTracker()
    
    try:
        # Simulate error
        x = 1 / 0
    except Exception as e:
        context = tracker.track_exception(e, {'user_id': '12345', 'action': 'test'})
        print(f'Tracked error: {context.error_type}')
    
    # Generate diagnostic report
    report_gen = DiagnosticReport(tracker)
    report = report_gen.generate_report()
    print(f'\nDiagnostic Report:')
    print(json.dumps(report, indent=2, default=str))
    
    # Get summary
    summary = tracker.get_error_summary()
    print(f'\nError Summary: {summary}')
