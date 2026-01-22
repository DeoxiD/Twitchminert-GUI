#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Inspector and Query Utilities for Twitchminert-GUI
Provides SQL query execution, database inspection, and diagnostic tools
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from sqlalchemy import text, inspect, MetaData
from sqlalchemy.orm import Session
import json


class DatabaseInspector:
    """
    Database inspection and diagnostic utilities
    """
    
    def __init__(self, db_session: Session):
        """
        Initialize inspector with database session
        
        Args:
            db_session: SQLAlchemy session object
        """
        self.session = db_session
        self.logger = logging.getLogger('twitchminert')
    
    def get_table_names(self) -> List[str]:
        """
        Get all table names in database
        
        Returns:
            List of table names
        """
        try:
            inspector = inspect(self.session.bind)
            tables = inspector.get_table_names()
            self.logger.debug(f'Found {len(tables)} tables in database')
            return tables
        except Exception as e:
            self.logger.error(f'Error getting table names: {e}')
            return []
    
    def get_table_row_count(self, table_name: str) -> int:
        """
        Get row count for specific table
        
        Args:
            table_name: Name of the table
        
        Returns:
            Number of rows in table
        """
        try:
            query = text(f'SELECT COUNT(*) FROM {table_name}')
            result = self.session.execute(query).scalar()
            self.logger.debug(f'Table {table_name}: {result} rows')
            return result or 0
        except Exception as e:
            self.logger.error(f'Error counting rows in {table_name}: {e}')
            return -1
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get overall database statistics
        
        Returns:
            Dictionary with table statistics
        """
        stats = {}
        tables = self.get_table_names()
        total_rows = 0
        
        for table in tables:
            count = self.get_table_row_count(table)
            stats[table] = count
            if count >= 0:
                total_rows += count
        
        self.logger.info(f'Database stats: {len(tables)} tables, {total_rows} total rows')
        return stats
    
    def execute_raw_query(self, query_string: str) -> List[Tuple]:
        """
        Execute raw SQL query
        
        Args:
            query_string: SQL query to execute
        
        Returns:
            List of result tuples
        """
        try:
            self.logger.debug(f'Executing query: {query_string[:100]}...')
            query = text(query_string)
            result = self.session.execute(query)
            rows = result.fetchall()
            self.logger.info(f'Query returned {len(rows)} rows')
            return rows
        except Exception as e:
            self.logger.error(f'Query execution error: {e}')
            return []
    
    def get_table_schema(self, table_name: str) -> Dict[str, str]:
        """
        Get column names and types for table
        
        Args:
            table_name: Name of the table
        
        Returns:
            Dictionary mapping column names to types
        """
        try:
            inspector = inspect(self.session.bind)
            columns = inspector.get_columns(table_name)
            schema = {col['name']: str(col['type']) for col in columns}
            self.logger.debug(f'Table {table_name} schema: {list(schema.keys())}')
            return schema
        except Exception as e:
            self.logger.error(f'Error getting schema for {table_name}: {e}')
            return {}
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform database health check
        
        Returns:
            Health check results
        """
        health = {
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'tables': {},
            'errors': []
        }
        
        try:
            tables = self.get_table_names()
            if not tables:
                health['status'] = 'error'
                health['errors'].append('No tables found')
                return health
            
            for table in tables:
                count = self.get_table_row_count(table)
                health['tables'][table] = count
            
            health['status'] = 'healthy'
            self.logger.info(f'Database health check: {health["status"]}')
        except Exception as e:
            health['status'] = 'error'
            health['errors'].append(str(e))
            self.logger.error(f'Health check error: {e}')
        
        return health


class QueryBuilder:
    """
    Helper class to build and log SQL queries
    """
    
    def __init__(self):
        self.logger = logging.getLogger('twitchminert')
        self.queries: List[str] = []
    
    def select_all(self, table: str, limit: Optional[int] = None) -> str:
        """
        Build SELECT query
        
        Args:
            table: Table name
            limit: Optional row limit
        
        Returns:
            SQL query string
        """
        query = f'SELECT * FROM {table}'
        if limit:
            query += f' LIMIT {limit}'
        self.queries.append(query)
        self.logger.debug(f'Built query: {query}')
        return query
    
    def count(self, table: str) -> str:
        """
        Build COUNT query
        
        Args:
            table: Table name
        
        Returns:
            SQL query string
        """
        query = f'SELECT COUNT(*) as count FROM {table}'
        self.queries.append(query)
        return query
    
    def get_by_column(self, table: str, column: str, value: Any) -> str:
        """
        Build WHERE query
        
        Args:
            table: Table name
            column: Column name
            value: Column value to match
        
        Returns:
            SQL query string
        """
        value_str = f"'{value}'" if isinstance(value, str) else str(value)
        query = f'SELECT * FROM {table} WHERE {column} = {value_str}'
        self.queries.append(query)
        self.logger.debug(f'Built WHERE query: {query}')
        return query
    
    def aggregate(self, table: str, agg_column: str, group_column: str) -> str:
        """
        Build aggregation query
        
        Args:
            table: Table name
            agg_column: Column to aggregate (COUNT, SUM, etc)
            group_column: Column to group by
        
        Returns:
            SQL query string
        """
        query = f'SELECT {group_column}, COUNT(*) as count FROM {table} GROUP BY {group_column}'
        self.queries.append(query)
        return query
    
    def get_history(self) -> List[str]:
        """
        Get all built queries
        
        Returns:
            List of queries
        """
        return self.queries
    
    def clear_history(self) -> None:
        """
        Clear query history
        """
        self.queries.clear()


if __name__ == '__main__':
    import sys
    from models import db
    from app import create_app
    
    # Example usage
    app = create_app('development')
    
    with app.app_context():
        logger = logging.getLogger('twitchminert')
        logger.info('Starting database inspection...')
        
        inspector = DatabaseInspector(db.session)
        
        # Get health check
        health = inspector.health_check()
        logger.info(f'Health Check: {json.dumps(health, indent=2)}')
        
        # Get table stats
        stats = inspector.get_database_stats()
        logger.info(f'Database Stats: {stats}')
        
        # Query builder example
        builder = QueryBuilder()
        query = builder.select_all('configuration', limit=5)
        logger.info(f'Sample query: {query}')
        
        # Execute query
        try:
            results = inspector.execute_raw_query(query)
            logger.info(f'Query returned {len(results)} results')
        except Exception as e:
            logger.error(f'Query failed: {e}')
