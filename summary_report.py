#!/usr/bin/env python3
"""
Snowflake Development Database Summary Report

This script generates a comprehensive summary of your Snowflake development database.
"""

import os
import snowflake.connector
from dotenv import load_dotenv
from datetime import datetime

def generate_summary_report():
    """Generate a comprehensive summary report."""
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
        cursor = connection.cursor()
        
        print("🏢 SNOWFLAKE DEVELOPMENT DATABASE SUMMARY REPORT")
        print("=" * 80)
        print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Connection Information
        print("🔗 CONNECTION INFORMATION")
        print("-" * 40)
        print(f"Account: {connection_params['account']}")
        print(f"User: {connection_params['user']}")
        print(f"Warehouse: {connection_params['warehouse']}")
        print(f"Database: {connection_params['database']}")
        print(f"Role: {connection_params['role']}")
        print()
        
        # Set database
        cursor.execute("USE DATABASE development")
        
        # Current context
        cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_WAREHOUSE(), CURRENT_ROLE()")
        context = cursor.fetchone()
        print("📍 CURRENT CONTEXT")
        print("-" * 40)
        print(f"Current Database: {context[0]}")
        print(f"Current Warehouse: {context[1]}")
        print(f"Current Role: {context[2]}")
        print()
        
        # Schemas
        cursor.execute("SHOW SCHEMAS IN DATABASE development")
        schemas = cursor.fetchall()
        print("📁 SCHEMAS")
        print("-" * 40)
        print(f"Total Schemas: {len(schemas)}")
        for schema in schemas:
            print(f"  • {schema[1]}")
        print()
        
        # Tables
        cursor.execute("SHOW TABLES IN DATABASE development")
        tables = cursor.fetchall()
        print("📊 TABLES")
        print("-" * 40)
        print(f"Total Tables: {len(tables)}")
        
        if tables:
            print("\nTable Details:")
            for i, table in enumerate(tables, 1):
                schema_name = table[3]
                table_name = table[1]
                created_on = table[0]
                table_type = table[4] if len(table) > 4 else 'TABLE'
                
                print(f"\n  {i}. {schema_name}.{table_name}")
                print(f"     Type: {table_type}")
                print(f"     Created: {created_on}")
                
                # Get row count
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM development.{schema_name}.{table_name}")
                    row_count = cursor.fetchone()[0]
                    print(f"     Rows: {row_count:,}")
                except:
                    print(f"     Rows: Unable to determine")
                
                # Get column count
                try:
                    cursor.execute(f"DESCRIBE TABLE development.{schema_name}.{table_name}")
                    columns = cursor.fetchall()
                    print(f"     Columns: {len(columns)}")
                    
                    # Show column details
                    print(f"     Column Details:")
                    for col in columns:
                        col_name = col[0]
                        col_type = col[1]
                        nullable = "NULL" if col[2] == "Y" else "NOT NULL"
                        print(f"       - {col_name}: {col_type} ({nullable})")
                        
                except:
                    print(f"     Columns: Unable to determine")
        
        print()
        print("📈 SUMMARY STATISTICS")
        print("-" * 40)
        print(f"Total Schemas: {len(schemas)}")
        print(f"Total Tables: {len(tables)}")
        
        # Calculate total rows across all tables
        total_rows = 0
        accessible_tables = 0
        for table in tables:
            try:
                schema_name = table[3]
                table_name = table[1]
                cursor.execute(f"SELECT COUNT(*) FROM development.{schema_name}.{table_name}")
                row_count = cursor.fetchone()[0]
                total_rows += row_count
                accessible_tables += 1
            except:
                continue
        
        print(f"Total Rows (across {accessible_tables} accessible tables): {total_rows:,}")
        
        # Schema breakdown
        schema_table_count = {}
        for table in tables:
            schema_name = table[3]
            schema_table_count[schema_name] = schema_table_count.get(schema_name, 0) + 1
        
        print(f"\nTables by Schema:")
        for schema, count in schema_table_count.items():
            print(f"  • {schema}: {count} tables")
        
        print()
        print("✅ REPORT COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")

if __name__ == "__main__":
    generate_summary_report()