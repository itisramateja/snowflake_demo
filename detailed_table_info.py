#!/usr/bin/env python3
"""
Detailed table information for development database

This script connects to Snowflake and provides detailed information about tables
in the development database including column details, row counts, etc.
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
    
    try:
        connection = snowflake.connector.connect(**connection_params)
        print("✅ Connected to Snowflake successfully!")
        return connection
    except Exception as e:
        print(f"❌ Failed to connect to Snowflake: {str(e)}")
        return None

def get_table_details(connection, schema_name, table_name):
    """Get detailed information about a specific table."""
    cursor = connection.cursor()
    
    try:
        # Get column information
        cursor.execute(f"DESCRIBE TABLE development.{schema_name}.{table_name}")
        columns = cursor.fetchall()
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM development.{schema_name}.{table_name}")
        row_count = cursor.fetchone()[0]
        
        # Get table size information
        cursor.execute(f"""
            SELECT 
                table_name,
                row_count,
                bytes,
                ROUND(bytes/1024/1024, 2) as size_mb
            FROM information_schema.tables 
            WHERE table_schema = '{schema_name}' 
            AND table_name = '{table_name}'
            AND table_catalog = 'DEVELOPMENT'
        """)
        size_info = cursor.fetchone()
        
        return {
            'columns': columns,
            'row_count': row_count,
            'size_info': size_info
        }
        
    except Exception as e:
        print(f"⚠️  Error getting details for {schema_name}.{table_name}: {str(e)}")
        return None
    finally:
        cursor.close()

def show_detailed_table_info(connection):
    """Show detailed information about all tables in development database."""
    cursor = connection.cursor()
    
    try:
        # Set database
        cursor.execute("USE DATABASE development")
        
        # Get all tables
        cursor.execute("SHOW TABLES IN DATABASE development")
        all_tables_raw = cursor.fetchall()
        
        # Parse table information
        tables = []
        for table_raw in all_tables_raw:
            # Extract schema and table name from the raw data
            # The format might vary, but typically: [created_on, name, database_name, schema_name, kind, comment, ...]
            if len(table_raw) >= 4:
                table_info = {
                    'created_on': table_raw[0],
                    'table_name': table_raw[1],
                    'database_name': table_raw[2],
                    'schema_name': table_raw[3],
                    'kind': table_raw[4] if len(table_raw) > 4 else 'TABLE'
                }
                tables.append(table_info)
        
        if not tables:
            print("❌ No tables found in development database")
            return
        
        print(f"\n🔍 Detailed Information for {len(tables)} tables in DEVELOPMENT database:")
        print("=" * 100)
        
        for i, table in enumerate(tables, 1):
            schema_name = table['schema_name']
            table_name = table['table_name']
            
            print(f"\n{i}. Table: {schema_name}.{table_name}")
            print("-" * 60)
            print(f"   Database: {table['database_name']}")
            print(f"   Schema: {schema_name}")
            print(f"   Type: {table['kind']}")
            print(f"   Created: {table['created_on']}")
            
            # Get detailed information
            details = get_table_details(connection, schema_name, table_name)
            
            if details:
                print(f"   Row Count: {details['row_count']:,}")
                
                if details['size_info']:
                    size_mb = details['size_info'][3] if details['size_info'][3] else 0
                    print(f"   Size: {size_mb} MB")
                
                # Show column information
                if details['columns']:
                    print(f"   Columns ({len(details['columns'])}):")
                    for col in details['columns']:
                        col_name = col[0]
                        col_type = col[1]
                        col_nullable = "NULL" if col[2] == "Y" else "NOT NULL"
                        print(f"     - {col_name}: {col_type} ({col_nullable})")
                
                # Show sample data
                try:
                    sample_cursor = connection.cursor()
                    sample_cursor.execute(f"SELECT * FROM development.{schema_name}.{table_name} LIMIT 3")
                    sample_data = sample_cursor.fetchall()
                    
                    if sample_data:
                        print(f"   Sample Data (first 3 rows):")
                        column_names = [desc[0] for desc in sample_cursor.description]
                        
                        # Create a simple table display
                        for j, row in enumerate(sample_data, 1):
                            print(f"     Row {j}:")
                            for k, (col_name, value) in enumerate(zip(column_names, row)):
                                # Truncate long values
                                str_value = str(value)
                                if len(str_value) > 50:
                                    str_value = str_value[:47] + "..."
                                print(f"       {col_name}: {str_value}")
                    
                    sample_cursor.close()
                    
                except Exception as e:
                    print(f"     ⚠️  Could not retrieve sample data: {str(e)}")
            
            print()  # Add spacing between tables
        
        return tables
        
    except Exception as e:
        print(f"❌ Error retrieving detailed table information: {str(e)}")
        return None
    finally:
        cursor.close()

def main():
    """Main function to connect and show detailed table information."""
    try:
        # Connect to Snowflake
        connection = connect_to_snowflake()
        if not connection:
            return
        
        # Show detailed table information
        tables = show_detailed_table_info(connection)
        
        if tables:
            print(f"✅ Successfully retrieved detailed information for {len(tables)} tables")
        else:
            print("❌ No tables found or error occurred")
            
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()
            print("🔒 Connection closed")

if __name__ == "__main__":
    main()