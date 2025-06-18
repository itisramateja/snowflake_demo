#!/usr/bin/env python3
"""
Script to show tables in the PATIENTS schema of DEVELOPMENT database
"""

import snowflake.connector
import logging

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

def show_patients_tables(cursor):
    """Show all tables in the PATIENTS schema."""
    print("\n" + "="*80)
    print("TABLES IN DEVELOPMENT.PATIENTS SCHEMA")
    print("="*80)
    
    try:
        # Set the context to the DEVELOPMENT database and PATIENTS schema
        cursor.execute("USE DATABASE DEVELOPMENT")
        cursor.execute("USE SCHEMA PATIENTS")
        
        # Show tables in the PATIENTS schema
        cursor.execute("SHOW TABLES IN SCHEMA DEVELOPMENT.PATIENTS")
        tables = cursor.fetchall()
        
        if not tables:
            print("No tables found in DEVELOPMENT.PATIENTS schema.")
            return
        
        # Print header
        print(f"{'#':<3} {'Table Name':<30} {'Owner':<15} {'Created':<20} {'Rows':<10} {'Bytes':<12}")
        print("-" * 80)
        
        # Print each table
        for i, table in enumerate(tables, 1):
            name = table[1] if len(table) > 1 else "N/A"
            owner = table[5] if len(table) > 5 else "N/A"
            created = table[0] if len(table) > 0 else "N/A"
            rows = table[3] if len(table) > 3 else "N/A"
            bytes_size = table[4] if len(table) > 4 else "N/A"
            
            # Format created date if it's a datetime object
            if hasattr(created, 'strftime'):
                created = created.strftime('%Y-%m-%d %H:%M')
            
            print(f"{i:<3} {name:<30} {owner:<15} {str(created):<20} {str(rows):<10} {str(bytes_size):<12}")
        
        print(f"\nTotal tables: {len(tables)}")
        
    except Exception as e:
        logger.error(f"Error showing tables: {str(e)}")

def show_table_details(cursor):
    """Show detailed information about each table including columns."""
    print("\n" + "="*80)
    print("DETAILED TABLE INFORMATION")
    print("="*80)
    
    try:
        # Get tables again
        cursor.execute("SHOW TABLES IN SCHEMA DEVELOPMENT.PATIENTS")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[1] if len(table) > 1 else "Unknown"
            print(f"\n📋 Table: {table_name}")
            print("-" * 50)
            
            # Get column information for this table
            try:
                cursor.execute(f"DESCRIBE TABLE DEVELOPMENT.PATIENTS.{table_name}")
                columns = cursor.fetchall()
                
                if columns:
                    print(f"   Columns ({len(columns)}):")
                    print(f"   {'Column Name':<25} {'Data Type':<20} {'Nullable':<10}")
                    print("   " + "-" * 55)
                    
                    for col in columns:
                        col_name = col[0] if len(col) > 0 else "Unknown"
                        col_type = col[1] if len(col) > 1 else "Unknown"
                        nullable = "YES" if (len(col) > 2 and col[2] == "Y") else "NO"
                        print(f"   {col_name:<25} {col_type:<20} {nullable:<10}")
                else:
                    print("   No column information available")
                    
                # Get sample row count
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM DEVELOPMENT.PATIENTS.{table_name}")
                    count_result = cursor.fetchone()
                    row_count = count_result[0] if count_result else 0
                    print(f"   Total Rows: {row_count:,}")
                except Exception as e:
                    print(f"   Could not get row count: {str(e)}")
                    
            except Exception as e:
                print(f"   Could not describe table: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error showing table details: {str(e)}")

def show_sample_data(cursor):
    """Show sample data from each table (first 3 rows)."""
    print("\n" + "="*80)
    print("SAMPLE DATA FROM TABLES")
    print("="*80)
    
    try:
        cursor.execute("SHOW TABLES IN SCHEMA DEVELOPMENT.PATIENTS")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[1] if len(table) > 1 else "Unknown"
            print(f"\n🔍 Sample data from {table_name}:")
            print("-" * 50)
            
            try:
                cursor.execute(f"SELECT * FROM DEVELOPMENT.PATIENTS.{table_name} LIMIT 3")
                sample_data = cursor.fetchall()
                
                if sample_data:
                    # Get column names
                    cursor.execute(f"DESCRIBE TABLE DEVELOPMENT.PATIENTS.{table_name}")
                    columns = cursor.fetchall()
                    col_names = [col[0] for col in columns] if columns else []
                    
                    # Print column headers
                    if col_names:
                        header = " | ".join([f"{name[:15]:<15}" for name in col_names[:5]])  # Show first 5 columns
                        print(f"   {header}")
                        print("   " + "-" * len(header))
                        
                        # Print sample rows
                        for row in sample_data:
                            row_str = " | ".join([f"{str(val)[:15]:<15}" for val in row[:5]])  # Show first 5 columns
                            print(f"   {row_str}")
                    else:
                        print("   Could not get column names")
                else:
                    print("   No data found in table")
                    
            except Exception as e:
                print(f"   Could not get sample data: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error showing sample data: {str(e)}")

def main():
    """Main function."""
    print("🔍 Connecting to Snowflake to show PATIENTS tables...")
    
    connection, cursor = connect_to_snowflake()
    if not connection or not cursor:
        return
    
    try:
        # Show tables
        show_patients_tables(cursor)
        
        # Show detailed information
        show_table_details(cursor)
        
        # Show sample data
        show_sample_data(cursor)
        
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