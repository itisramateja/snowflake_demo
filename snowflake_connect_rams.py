#!/usr/bin/env python3
"""
Snowflake Connection Script for User: rams

This script connects to Snowflake using the provided credentials:
- Username: rams
- Password: Sumajavikhyavihaan1981
- Warehouse: compute_wh
- Role: accountadmin

To use this script, you need to:
1. Replace 'YOUR_ACCOUNT_IDENTIFIER' with your actual Snowflake account identifier
2. Run the script: python snowflake_connect_rams.py
"""

import snowflake.connector
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SnowflakeConnector:
    """Snowflake connection class for user rams."""
    
    def __init__(self, account_identifier=None):
        """Initialize the connector with credentials."""
        self.connection_params = {
            'user': 'rams',
            'password': 'Sumajavikhyavihaan1981',
            'warehouse': 'compute_wh',
            'role': 'accountadmin'
        }
        
        if account_identifier:
            self.connection_params['account'] = account_identifier
        
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to Snowflake."""
        try:
            if 'account' not in self.connection_params:
                raise ValueError("Account identifier is required. Please provide your Snowflake account identifier.")
            
            logger.info("Connecting to Snowflake...")
            logger.info(f"User: {self.connection_params['user']}")
            logger.info(f"Warehouse: {self.connection_params['warehouse']}")
            logger.info(f"Role: {self.connection_params['role']}")
            
            self.connection = snowflake.connector.connect(**self.connection_params)
            self.cursor = self.connection.cursor()
            
            logger.info("✅ Successfully connected to Snowflake!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Snowflake: {str(e)}")
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
    
    def get_connection_info(self):
        """Get current connection information."""
        info = {}
        
        try:
            # Current warehouse
            result = self.execute_query("SELECT CURRENT_WAREHOUSE()")
            info['warehouse'] = result[0][0] if result else None
            
            # Current database
            result = self.execute_query("SELECT CURRENT_DATABASE()")
            info['database'] = result[0][0] if result else None
            
            # Current schema
            result = self.execute_query("SELECT CURRENT_SCHEMA()")
            info['schema'] = result[0][0] if result else None
            
            # Current role
            result = self.execute_query("SELECT CURRENT_ROLE()")
            info['role'] = result[0][0] if result else None
            
            # Current user
            result = self.execute_query("SELECT CURRENT_USER()")
            info['user'] = result[0][0] if result else None
            
            # Current timestamp
            result = self.execute_query("SELECT CURRENT_TIMESTAMP()")
            info['timestamp'] = result[0][0] if result else None
            
            # Snowflake version
            result = self.execute_query("SELECT CURRENT_VERSION()")
            info['version'] = result[0][0] if result else None
            
        except Exception as e:
            logger.error(f"Error getting connection info: {str(e)}")
        
        return info
    
    def run_sample_queries(self):
        """Run some sample queries to test the connection."""
        print("\n" + "="*70)
        print("RUNNING SAMPLE QUERIES")
        print("="*70)
        
        # Sample queries
        queries = [
            ("Simple calculation", "SELECT 42 * 7 AS result"),
            ("Current timestamp", "SELECT CURRENT_TIMESTAMP() AS current_time"),
            ("Random number", "SELECT RANDOM() AS random_number"),
            ("String manipulation", "SELECT UPPER('hello snowflake') AS uppercase_text"),
            ("Date functions", "SELECT DATEADD(day, 30, CURRENT_DATE()) AS thirty_days_later")
        ]
        
        for description, query in queries:
            print(f"\n{description}:")
            result = self.execute_query(query)
            if result:
                print(f"  Result: {result[0][0]}")
            else:
                print("  Failed to execute query")
    
    def list_objects(self):
        """List available databases, warehouses, and other objects."""
        print("\n" + "="*70)
        print("LISTING AVAILABLE OBJECTS")
        print("="*70)
        
        # List databases
        try:
            print("\nDatabases:")
            result = self.execute_query("SHOW DATABASES")
            if result:
                for i, db in enumerate(result[:10]):  # Show first 10
                    print(f"  {i+1}. {db[1]}")  # Database name is typically in column 1
                if len(result) > 10:
                    print(f"  ... and {len(result) - 10} more databases")
            else:
                print("  No databases found or insufficient privileges")
        except Exception as e:
            print(f"  Error listing databases: {str(e)}")
        
        # List warehouses
        try:
            print("\nWarehouses:")
            result = self.execute_query("SHOW WAREHOUSES")
            if result:
                for i, wh in enumerate(result[:10]):  # Show first 10
                    print(f"  {i+1}. {wh[0]} (State: {wh[1]})")  # Name and state
                if len(result) > 10:
                    print(f"  ... and {len(result) - 10} more warehouses")
            else:
                print("  No warehouses found or insufficient privileges")
        except Exception as e:
            print(f"  Error listing warehouses: {str(e)}")
        
        # List roles
        try:
            print("\nRoles:")
            result = self.execute_query("SHOW ROLES")
            if result:
                for i, role in enumerate(result[:10]):  # Show first 10
                    print(f"  {i+1}. {role[1]}")  # Role name is typically in column 1
                if len(result) > 10:
                    print(f"  ... and {len(result) - 10} more roles")
            else:
                print("  No roles found or insufficient privileges")
        except Exception as e:
            print(f"  Error listing roles: {str(e)}")
    
    def close(self):
        """Close the Snowflake connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("✅ Connection closed successfully")

def main():
    """Main function to demonstrate Snowflake connection."""
    
    print("="*70)
    print("SNOWFLAKE CONNECTION SCRIPT FOR USER: RAMS")
    print("="*70)
    print("Credentials:")
    print(f"  Username: rams")
    print(f"  Password: {'*' * 20}")
    print(f"  Warehouse: compute_wh")
    print(f"  Role: accountadmin")
    print("="*70)
    
    # Check if account identifier is provided as command line argument
    account_identifier = None
    if len(sys.argv) > 1:
        account_identifier = sys.argv[1]
        print(f"Using account identifier: {account_identifier}")
    else:
        print("\n⚠️  IMPORTANT: Account identifier is required!")
        print("Usage: python snowflake_connect_rams.py <account_identifier>")
        print("\nAccount identifier formats:")
        print("  - New accounts: 'organization-account_name'")
        print("  - Legacy accounts: 'account_name.region.cloud_provider'")
        print("  - Examples: 'myorg-myaccount' or 'xy12345.us-east-1.aws'")
        print("\nYou can find your account identifier in:")
        print("  1. Snowflake web interface URL")
        print("  2. Welcome email from Snowflake")
        print("  3. Account admin settings")
        
        # Ask user for input
        account_identifier = input("\nEnter your account identifier: ").strip()
        if not account_identifier:
            print("❌ Account identifier is required. Exiting.")
            return
    
    # Create connector and attempt connection
    connector = SnowflakeConnector(account_identifier)
    
    try:
        if connector.connect():
            # Get and display connection information
            print("\n" + "="*70)
            print("CONNECTION INFORMATION")
            print("="*70)
            
            info = connector.get_connection_info()
            for key, value in info.items():
                print(f"{key.capitalize()}: {value}")
            
            # Run sample queries
            connector.run_sample_queries()
            
            # List available objects
            connector.list_objects()
            
            print("\n" + "="*70)
            print("CONNECTION TEST COMPLETED SUCCESSFULLY!")
            print("="*70)
            
        else:
            print("\n❌ Connection failed. Please check:")
            print("1. Your account identifier is correct")
            print("2. Your credentials are valid")
            print("3. Your network can reach Snowflake")
            print("4. The warehouse 'compute_wh' exists and is accessible")
            print("5. The role 'accountadmin' is assigned to user 'rams'")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Connection interrupted by user")
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    
    finally:
        # Always close the connection
        connector.close()

if __name__ == "__main__":
    main()