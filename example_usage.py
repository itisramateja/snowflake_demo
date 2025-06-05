#!/usr/bin/env python3
"""
Example usage of Snowflake connection

This script demonstrates how to use the SnowflakeConnection class
to connect to Snowflake and perform basic operations.
"""

from snowflake_connection import SnowflakeConnection

def main():
    """Main function demonstrating Snowflake operations."""
    
    # Create connection instance
    sf = SnowflakeConnection()
    
    try:
        # Connect to Snowflake
        if not sf.connect():
            print("Failed to connect to Snowflake. Please check your credentials.")
            return
        
        print("🎉 Successfully connected to Snowflake!")
        print("-" * 50)
        
        # Display connection information
        print("Connection Information:")
        print(f"  Warehouse: {sf.get_current_warehouse()}")
        print(f"  Database: {sf.get_current_database()}")
        print(f"  Schema: {sf.get_current_schema()}")
        print("-" * 50)
        
        # Example 1: Show current timestamp
        print("Example 1: Current timestamp")
        result = sf.execute_query("SELECT CURRENT_TIMESTAMP()")
        if result:
            print(f"  Current timestamp: {result[0][0]}")
        
        # Example 2: Show version
        print("\nExample 2: Snowflake version")
        result = sf.execute_query("SELECT CURRENT_VERSION()")
        if result:
            print(f"  Snowflake version: {result[0][0]}")
        
        # Example 3: List tables
        print("\nExample 3: Tables in current schema")
        tables = sf.show_tables()
        if tables:
            print(f"  Found {len(tables)} tables:")
            for table in tables[:5]:  # Show first 5 tables
                print(f"    - {table[1]}")  # Table name is usually in the second column
            if len(tables) > 5:
                print(f"    ... and {len(tables) - 5} more tables")
        else:
            print("  No tables found in current schema")
        
        # Example 4: Simple calculation
        print("\nExample 4: Simple calculation")
        result = sf.execute_query("SELECT 2 + 2 AS result")
        if result:
            print(f"  2 + 2 = {result[0][0]}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Always close the connection
        sf.close()
        print("\n✅ Connection closed successfully")

if __name__ == "__main__":
    main()