#!/usr/bin/env python3
"""
Explore DEVELOPMENT Database Objects in Snowflake
This script connects to Snowflake and explores the DEVELOPMENT database structure.
"""

import snowflake.connector
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SnowflakeDatabaseExplorer:
    """Snowflake database explorer for user rams."""
    
    def __init__(self):
        """Initialize the connector with credentials."""
        self.connection_params = {
            'user': 'rams',
            'password': 'Sumajavikhyavihaan1981',
            'warehouse': 'compute_wh',
            'role': 'accountadmin',
            'account': 'ORULGHI-VKC36291',
            'database': 'DEVELOPMENT'  # Connect directly to DEVELOPMENT database
        }
        
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to Snowflake."""
        try:
            logger.info("Connecting to Snowflake DEVELOPMENT database...")
            logger.info(f"User: {self.connection_params['user']}")
            logger.info(f"Database: {self.connection_params['database']}")
            logger.info(f"Warehouse: {self.connection_params['warehouse']}")
            logger.info(f"Role: {self.connection_params['role']}")
            
            self.connection = snowflake.connector.connect(**self.connection_params)
            self.cursor = self.connection.cursor()
            
            logger.info("✅ Successfully connected to Snowflake DEVELOPMENT database!")
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
    
    def explore_database_structure(self):
        """Explore the complete structure of the DEVELOPMENT database."""
        print("\n" + "="*80)
        print("EXPLORING DEVELOPMENT DATABASE STRUCTURE")
        print("="*80)
        
        # Get current context
        print("\n📍 Current Context:")
        try:
            result = self.execute_query("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()")
            if result:
                db, schema, warehouse = result[0]
                print(f"  Database: {db}")
                print(f"  Schema: {schema}")
                print(f"  Warehouse: {warehouse}")
        except Exception as e:
            print(f"  Error getting context: {str(e)}")
        
        # List all schemas in DEVELOPMENT database
        print("\n📂 Schemas in DEVELOPMENT database:")
        try:
            result = self.execute_query("SHOW SCHEMAS IN DATABASE DEVELOPMENT")
            if result:
                print(f"  Found {len(result)} schemas:")
                for i, schema in enumerate(result, 1):
                    schema_name = schema[1]  # Schema name is typically in column 1
                    created_on = schema[0] if len(schema) > 0 else "N/A"
                    print(f"    {i}. {schema_name} (Created: {created_on})")
                    
                    # For each schema, get its objects
                    self.explore_schema_objects(schema_name)
            else:
                print("  No schemas found or insufficient privileges")
        except Exception as e:
            print(f"  Error listing schemas: {str(e)}")
    
    def explore_schema_objects(self, schema_name):
        """Explore objects within a specific schema."""
        print(f"\n    🔍 Objects in schema '{schema_name}':")
        
        # Tables
        try:
            result = self.execute_query(f"SHOW TABLES IN SCHEMA DEVELOPMENT.{schema_name}")
            if result and len(result) > 0:
                print(f"      📋 Tables ({len(result)}):")
                for table in result[:10]:  # Show first 10 tables
                    table_name = table[1]
                    table_type = table[3] if len(table) > 3 else "TABLE"
                    rows = table[4] if len(table) > 4 else "N/A"
                    print(f"        • {table_name} ({table_type}) - Rows: {rows}")
                if len(result) > 10:
                    print(f"        ... and {len(result) - 10} more tables")
            else:
                print("      📋 Tables: None found")
        except Exception as e:
            print(f"      📋 Tables: Error - {str(e)}")
        
        # Views
        try:
            result = self.execute_query(f"SHOW VIEWS IN SCHEMA DEVELOPMENT.{schema_name}")
            if result and len(result) > 0:
                print(f"      👁️ Views ({len(result)}):")
                for view in result[:10]:  # Show first 10 views
                    view_name = view[1]
                    print(f"        • {view_name}")
                if len(result) > 10:
                    print(f"        ... and {len(result) - 10} more views")
            else:
                print("      👁️ Views: None found")
        except Exception as e:
            print(f"      👁️ Views: Error - {str(e)}")
        
        # Functions
        try:
            result = self.execute_query(f"SHOW FUNCTIONS IN SCHEMA DEVELOPMENT.{schema_name}")
            if result and len(result) > 0:
                print(f"      ⚙️ Functions ({len(result)}):")
                for func in result[:5]:  # Show first 5 functions
                    func_name = func[1] if len(func) > 1 else func[0]
                    print(f"        • {func_name}")
                if len(result) > 5:
                    print(f"        ... and {len(result) - 5} more functions")
            else:
                print("      ⚙️ Functions: None found")
        except Exception as e:
            print(f"      ⚙️ Functions: Error - {str(e)}")
        
        # Procedures
        try:
            result = self.execute_query(f"SHOW PROCEDURES IN SCHEMA DEVELOPMENT.{schema_name}")
            if result and len(result) > 0:
                print(f"      🔧 Procedures ({len(result)}):")
                for proc in result[:5]:  # Show first 5 procedures
                    proc_name = proc[1] if len(proc) > 1 else proc[0]
                    print(f"        • {proc_name}")
                if len(result) > 5:
                    print(f"        ... and {len(result) - 5} more procedures")
            else:
                print("      🔧 Procedures: None found")
        except Exception as e:
            print(f"      🔧 Procedures: Error - {str(e)}")
        
        # Sequences
        try:
            result = self.execute_query(f"SHOW SEQUENCES IN SCHEMA DEVELOPMENT.{schema_name}")
            if result and len(result) > 0:
                print(f"      🔢 Sequences ({len(result)}):")
                for seq in result[:5]:  # Show first 5 sequences
                    seq_name = seq[1] if len(seq) > 1 else seq[0]
                    print(f"        • {seq_name}")
                if len(result) > 5:
                    print(f"        ... and {len(result) - 5} more sequences")
            else:
                print("      🔢 Sequences: None found")
        except Exception as e:
            print(f"      🔢 Sequences: Error - {str(e)}")
    
    def get_detailed_table_info(self, schema_name, table_name):
        """Get detailed information about a specific table."""
        print(f"\n📊 Detailed info for table {schema_name}.{table_name}:")
        
        try:
            # Get table structure
            result = self.execute_query(f"DESCRIBE TABLE DEVELOPMENT.{schema_name}.{table_name}")
            if result:
                print("  Columns:")
                for col in result:
                    col_name = col[0]
                    col_type = col[1]
                    nullable = col[2]
                    default = col[3] if col[3] else "None"
                    print(f"    • {col_name}: {col_type} (Nullable: {nullable}, Default: {default})")
            
            # Get row count
            result = self.execute_query(f"SELECT COUNT(*) FROM DEVELOPMENT.{schema_name}.{table_name}")
            if result:
                row_count = result[0][0]
                print(f"  Row count: {row_count:,}")
            
            # Get sample data (first 3 rows)
            result = self.execute_query(f"SELECT * FROM DEVELOPMENT.{schema_name}.{table_name} LIMIT 3")
            if result:
                print("  Sample data (first 3 rows):")
                for i, row in enumerate(result, 1):
                    print(f"    Row {i}: {row}")
                    
        except Exception as e:
            print(f"  Error getting table details: {str(e)}")
    
    def interactive_exploration(self):
        """Allow interactive exploration of specific objects."""
        print("\n" + "="*80)
        print("INTERACTIVE EXPLORATION")
        print("="*80)
        print("You can now explore specific objects in more detail.")
        print("Available commands:")
        print("  1. Enter 'schema.table' to get detailed table information")
        print("  2. Enter 'quit' to exit")
        print("  3. Enter 'help' for more options")
        
        while True:
            try:
                user_input = input("\nEnter command: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                elif user_input.lower() == 'help':
                    print("Available commands:")
                    print("  - schema.table : Get detailed info about a table")
                    print("  - quit/exit/q : Exit interactive mode")
                elif '.' in user_input:
                    parts = user_input.split('.')
                    if len(parts) == 2:
                        schema_name, table_name = parts
                        self.get_detailed_table_info(schema_name.upper(), table_name.upper())
                    else:
                        print("Invalid format. Use: schema.table")
                else:
                    print("Invalid command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting interactive mode...")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def close(self):
        """Close the Snowflake connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("✅ Connection closed successfully")

def main():
    """Main function to explore DEVELOPMENT database."""
    
    print("="*80)
    print("SNOWFLAKE DEVELOPMENT DATABASE EXPLORER")
    print("="*80)
    
    # Create explorer and attempt connection
    explorer = SnowflakeDatabaseExplorer()
    
    try:
        if explorer.connect():
            # Explore database structure
            explorer.explore_database_structure()
            
            # Interactive exploration
            explorer.interactive_exploration()
            
            print("\n" + "="*80)
            print("EXPLORATION COMPLETED!")
            print("="*80)
            
        else:
            print("\n❌ Connection failed. Please check your credentials and network connectivity.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Exploration interrupted by user")
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    
    finally:
        # Always close the connection
        explorer.close()

if __name__ == "__main__":
    main()