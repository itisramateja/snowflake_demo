#!/usr/bin/env python3
"""
Snowflake Connection Script with Direct Credentials

This script connects to Snowflake using the provided credentials:
- Username: rams
- Password: Sumajavikhyavihaan1981
- Warehouse: compute_wh
- Role: accountadmin
"""

import snowflake.connector
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_snowflake():
    """Connect to Snowflake with the specified credentials."""
    
    # Connection parameters
    connection_params = {
        'user': 'rams',
        'password': 'Sumajavikhyavihaan1981',
        'warehouse': 'compute_wh',
        'role': 'accountadmin'
        # Note: account parameter is required but not provided
        # You'll need to add your Snowflake account identifier
        # 'account': 'your_account_identifier'
    }
    
    try:
        logger.info("Attempting to connect to Snowflake...")
        
        # Note: You need to add the account parameter
        # The account identifier is typically in the format: organization-account_name
        # or for legacy accounts: account_name.region.cloud_provider
        print("⚠️  WARNING: Account identifier is required but not provided.")
        print("Please add your Snowflake account identifier to the connection_params.")
        print("Example formats:")
        print("  - For new accounts: 'organization-account_name'")
        print("  - For legacy accounts: 'account_name.region.cloud_provider'")
        print("  - Example: 'myorg-myaccount' or 'xy12345.us-east-1.aws'")
        
        # Uncomment and modify the following lines once you have the account identifier:
        # connection = snowflake.connector.connect(**connection_params)
        # cursor = connection.cursor()
        # logger.info("✅ Successfully connected to Snowflake!")
        # return connection, cursor
        
        return None, None
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to Snowflake: {str(e)}")
        return None, None

def test_connection_and_queries(connection, cursor):
    """Test the connection with some basic queries."""
    
    if not connection or not cursor:
        print("No valid connection available for testing.")
        return
    
    try:
        print("\n" + "="*60)
        print("CONNECTION INFORMATION")
        print("="*60)
        
        # Get current warehouse
        cursor.execute("SELECT CURRENT_WAREHOUSE()")
        warehouse = cursor.fetchone()[0]
        print(f"Current Warehouse: {warehouse}")
        
        # Get current role
        cursor.execute("SELECT CURRENT_ROLE()")
        role = cursor.fetchone()[0]
        print(f"Current Role: {role}")
        
        # Get current user
        cursor.execute("SELECT CURRENT_USER()")
        user = cursor.fetchone()[0]
        print(f"Current User: {user}")
        
        # Get current timestamp
        cursor.execute("SELECT CURRENT_TIMESTAMP()")
        timestamp = cursor.fetchone()[0]
        print(f"Current Timestamp: {timestamp}")
        
        # Get Snowflake version
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()[0]
        print(f"Snowflake Version: {version}")
        
        print("\n" + "="*60)
        print("BASIC QUERIES")
        print("="*60)
        
        # Simple calculation
        cursor.execute("SELECT 10 * 5 AS calculation")
        result = cursor.fetchone()[0]
        print(f"10 * 5 = {result}")
        
        # Show databases (if accessible)
        try:
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"\nAvailable Databases: {len(databases)}")
            for db in databases[:5]:  # Show first 5
                print(f"  - {db[1]}")  # Database name is typically in the second column
            if len(databases) > 5:
                print(f"  ... and {len(databases) - 5} more databases")
        except Exception as e:
            print(f"Could not list databases: {str(e)}")
        
        # Show warehouses (if accessible)
        try:
            cursor.execute("SHOW WAREHOUSES")
            warehouses = cursor.fetchall()
            print(f"\nAvailable Warehouses: {len(warehouses)}")
            for wh in warehouses[:5]:  # Show first 5
                print(f"  - {wh[0]}")  # Warehouse name is typically in the first column
            if len(warehouses) > 5:
                print(f"  ... and {len(warehouses) - 5} more warehouses")
        except Exception as e:
            print(f"Could not list warehouses: {str(e)}")
        
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}")

def main():
    """Main function to demonstrate Snowflake connection."""
    
    print("Snowflake Connection Script")
    print("="*60)
    print("Credentials:")
    print(f"  Username: rams")
    print(f"  Password: {'*' * len('Sumajavikhyavihaan1981')}")
    print(f"  Warehouse: compute_wh")
    print(f"  Role: accountadmin")
    print("="*60)
    
    # Attempt connection
    connection, cursor = connect_to_snowflake()
    
    if connection and cursor:
        # Test the connection
        test_connection_and_queries(connection, cursor)
        
        # Close connection
        cursor.close()
        connection.close()
        logger.info("✅ Connection closed successfully")
    else:
        print("\n❌ Connection failed. Please check the following:")
        print("1. Add your Snowflake account identifier")
        print("2. Verify your credentials are correct")
        print("3. Ensure your network can reach Snowflake")
        print("4. Check if the warehouse and role exist and are accessible")

if __name__ == "__main__":
    main()