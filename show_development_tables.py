#!/usr/bin/env python3
"""
Show all tables in the development database

This script connects to Snowflake and displays all tables in the development database.
"""

import os
import snowflake.connector
from dotenv import load_dotenv
import pandas as pd

def connect_to_snowflake():
    """Connect to Snowflake using environment variables."""
    load_dotenv()
    
    connection_params = {
        'account': os.getenv('SNOWFLAKE_ACCOUNT'),
        'user': os.getenv('SNOWFLAKE_USER'),
        'password': os.getenv('SNOWFLAKE_PASSWORD'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
        'database': os.getenv('SNOWFLAKE_DATABASE', 'development'),
        'role': os.getenv('SNOWFLAKE_ROLE')
    }
    
    # Validate required parameters
    required_params = ['account', 'user', 'password']
    missing_params = [param for param in required_params if not connection_params.get(param)]
    
    if missing_params:
        raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")
    
    print("🔗 Connecting to Snowflake...")
    print(f"   Account: {connection_params['account']}")
    print(f"   User: {connection_params['user']}")
    print(f"   Database: {connection_params['database']}")
    print(f"   Warehouse: {connection_params['warehouse']}")
    print(f"   Role: {connection_params['role']}")
    print("-" * 60)
    
    try:
        connection = snowflake.connector.connect(**connection_params)
        print("✅ Successfully connected to Snowflake!")
        return connection
    except Exception as e:
        print(f"❌ Failed to connect to Snowflake: {str(e)}")
        return None

def show_all_tables_in_development(connection):
    """Show all tables in the development database."""
    cursor = connection.cursor()
    
    try:
        # First, make sure we're using the development database
        print("\n🔄 Setting database to 'development'...")
        cursor.execute("USE DATABASE development")
        
        # Get current database to confirm
        cursor.execute("SELECT CURRENT_DATABASE()")
        current_db = cursor.fetchone()[0]
        print(f"✅ Current database: {current_db}")
        
        # Get all schemas in the development database
        print("\n📋 Getting all schemas in development database...")
        cursor.execute("SHOW SCHEMAS IN DATABASE development")
        schemas = cursor.fetchall()
        
        if not schemas:
            print("❌ No schemas found in development database")
            return
        
        print(f"📁 Found {len(schemas)} schemas:")
        for schema in schemas:
            print(f"   - {schema[1]}")  # Schema name is typically in the second column
        
        # Get all tables across all schemas
        print(f"\n📊 Getting all tables in development database...")
        all_tables = []
        
        for schema in schemas:
            schema_name = schema[1]
            try:
                cursor.execute(f"SHOW TABLES IN SCHEMA development.{schema_name}")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_info = {
                        'schema': schema_name,
                        'table_name': table[1],  # Table name
                        'table_type': table[3] if len(table) > 3 else 'TABLE',  # Table type
                        'created_on': table[0] if len(table) > 0 else None,  # Created date
                        'database': 'development'
                    }
                    all_tables.append(table_info)
                    
            except Exception as e:
                print(f"⚠️  Warning: Could not access schema {schema_name}: {str(e)}")
                continue
        
        if not all_tables:
            print("❌ No tables found in development database")
            return
        
        # Display results
        print(f"\n🎉 Found {len(all_tables)} tables in development database:")
        print("=" * 80)
        
        # Group by schema for better organization
        tables_by_schema = {}
        for table in all_tables:
            schema = table['schema']
            if schema not in tables_by_schema:
                tables_by_schema[schema] = []
            tables_by_schema[schema].append(table)
        
        for schema_name, tables in tables_by_schema.items():
            print(f"\n📁 Schema: {schema_name} ({len(tables)} tables)")
            print("-" * 40)
            for i, table in enumerate(tables, 1):
                print(f"   {i:2d}. {table['table_name']} ({table['table_type']})")
        
        # Create a summary table using pandas for better formatting
        print(f"\n📈 Summary Table:")
        print("=" * 80)
        
        df = pd.DataFrame(all_tables)
        if not df.empty:
            # Display summary by schema
            schema_summary = df.groupby('schema').size().reset_index(name='table_count')
            print("\nTables by Schema:")
            for _, row in schema_summary.iterrows():
                print(f"   {row['schema']}: {row['table_count']} tables")
            
            # Display all tables in a formatted way
            print(f"\nAll Tables (Total: {len(all_tables)}):")
            for i, (_, row) in enumerate(df.iterrows(), 1):
                print(f"   {i:2d}. {row['schema']}.{row['table_name']} ({row['table_type']})")
        
        return all_tables
        
    except Exception as e:
        print(f"❌ Error retrieving tables: {str(e)}")
        return None
    finally:
        cursor.close()

def main():
    """Main function to connect and show tables."""
    try:
        # Connect to Snowflake
        connection = connect_to_snowflake()
        if not connection:
            return
        
        # Show all tables in development database
        tables = show_all_tables_in_development(connection)
        
        if tables:
            print(f"\n✅ Successfully retrieved {len(tables)} tables from development database")
        else:
            print("\n❌ No tables found or error occurred")
            
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()
            print("\n🔒 Connection closed")

if __name__ == "__main__":
    main()