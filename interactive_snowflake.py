#!/usr/bin/env python3
"""
Interactive Snowflake Query Tool

This script provides an interactive interface to query your Snowflake database.
"""

import os
import snowflake.connector
from dotenv import load_dotenv
import pandas as pd

class SnowflakeInteractive:
    def __init__(self):
        """Initialize the interactive Snowflake connection."""
        load_dotenv()
        
        self.connection_params = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE', 'development'),
            'role': os.getenv('SNOWFLAKE_ROLE')
        }
        
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Connect to Snowflake."""
        try:
            print("🔗 Connecting to Snowflake...")
            self.connection = snowflake.connector.connect(**self.connection_params)
            self.cursor = self.connection.cursor()
            print("✅ Successfully connected to Snowflake!")
            
            # Set database to development
            self.cursor.execute("USE DATABASE development")
            print("📂 Using DEVELOPMENT database")
            
            return True
        except Exception as e:
            print(f"❌ Failed to connect: {str(e)}")
            return False
    
    def execute_query(self, query):
        """Execute a SQL query and return results."""
        if not self.cursor:
            print("❌ No active connection. Please connect first.")
            return None
        
        try:
            print(f"🔍 Executing: {query}")
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            
            if results:
                # Create a pandas DataFrame for better display
                df = pd.DataFrame(results, columns=columns)
                print(f"✅ Query executed successfully. Found {len(results)} rows.")
                print("\nResults:")
                print("-" * 60)
                print(df.to_string(index=False))
            else:
                print("✅ Query executed successfully. No rows returned.")
            
            return results
            
        except Exception as e:
            print(f"❌ Error executing query: {str(e)}")
            return None
    
    def show_quick_commands(self):
        """Show available quick commands."""
        commands = {
            '1': 'SHOW TABLES IN DATABASE development',
            '2': 'SELECT * FROM development.patients.patients LIMIT 10',
            '3': 'SELECT * FROM development.patients.patients_backup LIMIT 10',
            '4': 'SELECT COUNT(*) FROM development.patients.patients',
            '5': 'SELECT COUNT(*) FROM development.patients.patients_backup',
            '6': 'DESCRIBE TABLE development.patients.patients',
            '7': 'DESCRIBE TABLE development.patients.patients_backup',
            '8': 'SHOW SCHEMAS IN DATABASE development',
            '9': 'SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()',
            '10': 'SELECT * FROM development.patients.patients WHERE id <= 3'
        }
        
        print("\n📋 Quick Commands:")
        print("=" * 60)
        for num, cmd in commands.items():
            print(f"{num:2s}. {cmd}")
        print("  q. Quit")
        print("  h. Show this help")
        print("  c. Custom query")
        
        return commands
    
    def run_interactive(self):
        """Run the interactive session."""
        if not self.connect():
            return
        
        print("\n🎉 Welcome to Interactive Snowflake Query Tool!")
        print("=" * 60)
        
        commands = self.show_quick_commands()
        
        while True:
            try:
                print("\n" + "─" * 60)
                choice = input("Enter command number, 'c' for custom query, 'h' for help, or 'q' to quit: ").strip().lower()
                
                if choice == 'q':
                    print("👋 Goodbye!")
                    break
                elif choice == 'h':
                    commands = self.show_quick_commands()
                elif choice == 'c':
                    custom_query = input("Enter your SQL query: ").strip()
                    if custom_query:
                        self.execute_query(custom_query)
                elif choice in commands:
                    self.execute_query(commands[choice])
                else:
                    print("❌ Invalid choice. Enter 'h' for help.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {str(e)}")
    
    def close(self):
        """Close the connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("🔒 Connection closed")

def main():
    """Main function."""
    sf = SnowflakeInteractive()
    try:
        sf.run_interactive()
    finally:
        sf.close()

if __name__ == "__main__":
    main()