#!/usr/bin/env python3
"""
Get detailed information about PATIENTS schema objects
"""

import snowflake.connector
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_snowflake():
    """Connect to Snowflake DEVELOPMENT database."""
    connection_params = {
        'user': 'rams',
        'password': 'Sumajavikhyavihaan1981',
        'warehouse': 'compute_wh',
        'role': 'accountadmin',
        'account': 'ORULGHI-VKC36291',
        'database': 'DEVELOPMENT',
        'schema': 'PATIENTS'
    }
    
    try:
        connection = snowflake.connector.connect(**connection_params)
        cursor = connection.cursor()
        logger.info("✅ Connected to DEVELOPMENT.PATIENTS")
        return connection, cursor
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        return None, None

def execute_query(cursor, query):
    """Execute a query and return results."""
    try:
        logger.info(f"Executing: {query}")
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        return None

def main():
    print("="*80)
    print("DETAILED PATIENTS SCHEMA EXPLORATION")
    print("="*80)
    
    connection, cursor = connect_to_snowflake()
    if not connection:
        return
    
    try:
        # Get all data from PATIENTS table
        print("\n📋 PATIENTS Table - All Data:")
        result = execute_query(cursor, "SELECT * FROM PATIENTS ORDER BY ID")
        if result:
            print("  ID | NAME")
            print("  ---|-----")
            for row in result:
                print(f"  {row[0]:2} | {row[1]}")
        
        # Get PATIENTS_VIEW definition
        print("\n👁️ PATIENTS_VIEW Details:")
        result = execute_query(cursor, "SHOW VIEWS LIKE 'PATIENTS_VIEW'")
        if result:
            view_info = result[0]
            print(f"  View Name: {view_info[1]}")
            print(f"  Created On: {view_info[0]}")
            print(f"  Owner: {view_info[5] if len(view_info) > 5 else 'N/A'}")
        
        # Get data from PATIENTS_VIEW
        print("\n👁️ PATIENTS_VIEW - Data:")
        result = execute_query(cursor, "SELECT * FROM PATIENTS_VIEW ORDER BY ID")
        if result:
            # Get column names first
            cursor.execute("DESCRIBE VIEW PATIENTS_VIEW")
            columns = cursor.fetchall()
            
            # Print header
            header = " | ".join([col[0] for col in columns])
            print(f"  {header}")
            print("  " + "-" * len(header))
            
            # Print data
            for row in result:
                row_str = " | ".join([str(val) for val in row])
                print(f"  {row_str}")
        
        # Get view definition (DDL)
        print("\n👁️ PATIENTS_VIEW - Definition:")
        result = execute_query(cursor, "SELECT GET_DDL('VIEW', 'PATIENTS_VIEW')")
        if result:
            ddl = result[0][0]
            print("  View DDL:")
            print("  " + "="*60)
            for line in ddl.split('\n'):
                print(f"  {line}")
            print("  " + "="*60)
        
        # Check the sequence
        print("\n🔢 DEVELOPMENT Sequence Details:")
        result = execute_query(cursor, "SHOW SEQUENCES LIKE 'DEVELOPMENT'")
        if result:
            seq_info = result[0]
            print(f"  Sequence Name: {seq_info[1]}")
            print(f"  Current Value: {seq_info[4] if len(seq_info) > 4 else 'N/A'}")
            print(f"  Increment: {seq_info[5] if len(seq_info) > 5 else 'N/A'}")
        
        # Get next value from sequence
        result = execute_query(cursor, "SELECT DEVELOPMENT.NEXTVAL")
        if result:
            print(f"  Next Value: {result[0][0]}")
        
        print("\n" + "="*80)
        print("PATIENTS SCHEMA EXPLORATION COMPLETED!")
        print("="*80)
        
    finally:
        cursor.close()
        connection.close()
        logger.info("✅ Connection closed")

if __name__ == "__main__":
    main()