#!/usr/bin/env python3
"""
Script to show databases in Snowflake account for user: rams
"""

import snowflake.connector
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_snowflake():
    """Connect to Snowflake and return connection and cursor."""
    connection_params = {
        'user': 'rams',
        'password': 'Sumajavikhyavihaan1981',
        'warehouse': 'compute_wh',
        'role': 'accountadmin',
        'account': 'ORULGHI-VKC36291'
    }
    
    try:
        connection = snowflake.connector.connect(**connection_params)
        cursor = connection.cursor()
        logger.info("✅ Successfully connected to Snowflake!")
        return connection, cursor
    except Exception as e:
        logger.error(f"❌ Failed to connect to Snowflake: {str(e)}")
        return None, None

def show_databases(cursor):
    """Show detailed information about databases."""
    print("\n" + "="*80)
    print("DATABASES IN YOUR SNOWFLAKE ACCOUNT")
    print("="*80)
    
    try:
        # Get detailed database information
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        
        if not databases:
            print("No databases found.")
            return
        
        # Print header
        print(f"{'#':<3} {'Database Name':<25} {'Owner':<15} {'Created':<20} {'Comment':<30}")
        print("-" * 80)
        
        # Print each database
        for i, db in enumerate(databases, 1):
            name = db[1] if len(db) > 1 else "N/A"
            owner = db[2] if len(db) > 2 else "N/A"
            created = db[0] if len(db) > 0 else "N/A"
            comment = db[6] if len(db) > 6 else ""
            
            # Format created date if it's a datetime object
            if hasattr(created, 'strftime'):
                created = created.strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"{i:<3} {name:<25} {owner:<15} {str(created):<20} {comment:<30}")
        
        print(f"\nTotal databases: {len(databases)}")
        
    except Exception as e:
        logger.error(f"Error showing databases: {str(e)}")

def show_database_details(cursor):
    """Show additional details for each database."""
    print("\n" + "="*80)
    print("DETAILED DATABASE INFORMATION")
    print("="*80)
    
    try:
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        
        for db in databases:
            db_name = db[1] if len(db) > 1 else "Unknown"
            print(f"\n📁 Database: {db_name}")
            print("-" * 40)
            
            # Try to get schemas for this database
            try:
                cursor.execute(f"SHOW SCHEMAS IN DATABASE {db_name}")
                schemas = cursor.fetchall()
                print(f"   Schemas ({len(schemas)}):")
                for schema in schemas[:5]:  # Show first 5 schemas
                    schema_name = schema[1] if len(schema) > 1 else "Unknown"
                    print(f"     • {schema_name}")
                if len(schemas) > 5:
                    print(f"     ... and {len(schemas) - 5} more schemas")
                    
            except Exception as e:
                print(f"   Could not access schemas: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error showing database details: {str(e)}")

def main():
    """Main function."""
    print("🔍 Connecting to Snowflake to show databases...")
    
    connection, cursor = connect_to_snowflake()
    if not connection or not cursor:
        return
    
    try:
        # Show databases
        show_databases(cursor)
        
        # Show detailed information
        show_database_details(cursor)
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
    
    finally:
        # Close connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        logger.info("✅ Connection closed")

if __name__ == "__main__":
    main()