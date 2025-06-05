#!/usr/bin/env python3
"""
Snowflake Connection Module

This module provides functionality to connect to Snowflake and execute queries.
"""

import os
import snowflake.connector
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SnowflakeConnection:
    """Class to handle Snowflake database connections and operations."""
    
    def __init__(self):
        """Initialize the Snowflake connection with environment variables."""
        load_dotenv()
        
        self.connection_params = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
            'role': os.getenv('SNOWFLAKE_ROLE')
        }
        
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to Snowflake."""
        try:
            # Validate required parameters
            required_params = ['account', 'user', 'password']
            missing_params = [param for param in required_params if not self.connection_params.get(param)]
            
            if missing_params:
                raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")
            
            logger.info("Connecting to Snowflake...")
            self.connection = snowflake.connector.connect(**self.connection_params)
            self.cursor = self.connection.cursor()
            logger.info("Successfully connected to Snowflake!")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {str(e)}")
            return False
    
    def execute_query(self, query):
        """Execute a SQL query and return results."""
        if not self.cursor:
            logger.error("No active connection. Please connect first.")
            return None
        
        try:
            logger.info(f"Executing query: {query}")
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return None
    
    def get_current_warehouse(self):
        """Get the current warehouse."""
        result = self.execute_query("SELECT CURRENT_WAREHOUSE()")
        return result[0][0] if result else None
    
    def get_current_database(self):
        """Get the current database."""
        result = self.execute_query("SELECT CURRENT_DATABASE()")
        return result[0][0] if result else None
    
    def get_current_schema(self):
        """Get the current schema."""
        result = self.execute_query("SELECT CURRENT_SCHEMA()")
        return result[0][0] if result else None
    
    def show_tables(self):
        """Show all tables in the current schema."""
        return self.execute_query("SHOW TABLES")
    
    def close(self):
        """Close the Snowflake connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Connection closed.")

def test_connection():
    """Test the Snowflake connection."""
    sf = SnowflakeConnection()
    
    if sf.connect():
        print("✅ Connection successful!")
        
        # Test basic queries
        print(f"Current Warehouse: {sf.get_current_warehouse()}")
        print(f"Current Database: {sf.get_current_database()}")
        print(f"Current Schema: {sf.get_current_schema()}")
        
        # Show tables
        tables = sf.show_tables()
        if tables:
            print(f"Found {len(tables)} tables in current schema")
        else:
            print("No tables found or unable to retrieve table list")
        
        sf.close()
    else:
        print("❌ Connection failed!")

if __name__ == "__main__":
    test_connection()