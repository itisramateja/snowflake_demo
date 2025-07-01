#!/usr/bin/env python3
"""
Snowflake Cortex Analyst Integration Module

This module provides functionality to interact with Snowflake Cortex Analyst
using a semantic layer for natural language queries.
"""

import os
import json
import yaml
import pandas as pd
from typing import Dict, List, Any, Optional
from snowflake.snowpark import Session
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CortexAnalyst:
    """Class to handle Snowflake Cortex Analyst operations with semantic layer."""
    
    def __init__(self, semantic_model_path: str = "semantic_model.yaml"):
        """Initialize the Cortex Analyst with semantic model."""
        load_dotenv()
        
        self.connection_params = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE', 'SNOWFLAKE_SAMPLE_DATA'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA', 'TPCH_SF1'),
            'role': os.getenv('SNOWFLAKE_ROLE')
        }
        
        self.session = None
        self.semantic_model = None
        self.semantic_model_path = semantic_model_path
        
        # Load semantic model
        self._load_semantic_model()
    
    def _load_semantic_model(self):
        """Load the semantic model from YAML file."""
        try:
            with open(self.semantic_model_path, 'r') as file:
                self.semantic_model = yaml.safe_load(file)
            logger.info(f"Semantic model loaded from {self.semantic_model_path}")
        except Exception as e:
            logger.error(f"Failed to load semantic model: {str(e)}")
            self.semantic_model = None
    
    def connect(self) -> bool:
        """Establish connection to Snowflake using Snowpark."""
        try:
            # Validate required parameters
            required_params = ['account', 'user', 'password']
            missing_params = [param for param in required_params 
                            if not self.connection_params.get(param)]
            
            if missing_params:
                raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")
            
            logger.info("Connecting to Snowflake via Snowpark...")
            self.session = Session.builder.configs(self.connection_params).create()
            logger.info("Successfully connected to Snowflake!")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {str(e)}")
            return False
    
    def get_semantic_context(self) -> str:
        """Generate semantic context for Cortex Analyst."""
        if not self.semantic_model:
            return ""
        
        context = f"Semantic Model: {self.semantic_model.get('name', 'Unknown')}\n"
        context += f"Description: {self.semantic_model.get('description', '')}\n\n"
        
        # Add table information
        context += "Available Tables:\n"
        for table in self.semantic_model.get('tables', []):
            context += f"- {table['name']}: {table['description']}\n"
            context += f"  Base Table: {table['base_table']}\n"
            context += "  Columns:\n"
            for col in table.get('columns', []):
                context += f"    - {col['name']}: {col['description']} ({col['data_type']})\n"
            context += "\n"
        
        # Add metrics information
        context += "Available Metrics:\n"
        for metric in self.semantic_model.get('metrics', []):
            context += f"- {metric['name']}: {metric['description']}\n"
        
        # Add dimensions information
        context += "\nAvailable Dimensions:\n"
        for dim in self.semantic_model.get('dimensions', []):
            context += f"- {dim['name']}: {dim['description']}\n"
        
        return context
    
    def natural_language_to_sql(self, question: str) -> str:
        """Convert natural language question to SQL using predefined patterns."""
        if not self.session:
            raise Exception("No active session. Please connect first.")
        
        question_lower = question.lower()
        
        # Define common query patterns
        if "total revenue" in question_lower and "year" in question_lower:
            return """
            SELECT 
                YEAR(o.O_ORDERDATE) as order_year,
                SUM(o.O_TOTALPRICE) as total_revenue
            FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
            GROUP BY YEAR(o.O_ORDERDATE)
            ORDER BY order_year
            """
        
        elif "top" in question_lower and "customer" in question_lower:
            limit = 10
            if "top 5" in question_lower:
                limit = 5
            elif "top 20" in question_lower:
                limit = 20
            
            return f"""
            SELECT 
                c.C_NAME as customer_name,
                SUM(o.O_TOTALPRICE) as total_order_value,
                COUNT(o.O_ORDERKEY) as order_count
            FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
            JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER c ON o.O_CUSTKEY = c.C_CUSTKEY
            GROUP BY c.C_NAME
            ORDER BY total_order_value DESC
            LIMIT {limit}
            """
        
        elif "average order value" in question_lower and "market segment" in question_lower:
            return """
            SELECT 
                c.C_MKTSEGMENT as market_segment,
                AVG(o.O_TOTALPRICE) as average_order_value,
                COUNT(o.O_ORDERKEY) as order_count
            FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
            JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER c ON o.O_CUSTKEY = c.C_CUSTKEY
            GROUP BY c.C_MKTSEGMENT
            ORDER BY average_order_value DESC
            """
        
        elif "orders" in question_lower and "month" in question_lower and "1995" in question_lower:
            return """
            SELECT 
                MONTH(O_ORDERDATE) as order_month,
                MONTHNAME(O_ORDERDATE) as month_name,
                COUNT(O_ORDERKEY) as order_count,
                SUM(O_TOTALPRICE) as total_revenue
            FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
            WHERE YEAR(O_ORDERDATE) = 1995
            GROUP BY MONTH(O_ORDERDATE), MONTHNAME(O_ORDERDATE)
            ORDER BY order_month
            """
        
        elif "nation" in question_lower and "revenue" in question_lower:
            return """
            SELECT 
                n.N_NAME as nation_name,
                SUM(o.O_TOTALPRICE) as total_revenue,
                COUNT(o.O_ORDERKEY) as order_count,
                AVG(o.O_TOTALPRICE) as average_order_value
            FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
            JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER c ON o.O_CUSTKEY = c.C_CUSTKEY
            JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.NATION n ON c.C_NATIONKEY = n.N_NATIONKEY
            GROUP BY n.N_NAME
            ORDER BY total_revenue DESC
            """
        
        elif "priority" in question_lower and "order" in question_lower:
            return """
            SELECT 
                O_ORDERPRIORITY as order_priority,
                COUNT(O_ORDERKEY) as order_count,
                SUM(O_TOTALPRICE) as total_revenue,
                AVG(O_TOTALPRICE) as average_order_value
            FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
            GROUP BY O_ORDERPRIORITY
            ORDER BY order_count DESC
            """
        
        elif "quarter" in question_lower and "revenue" in question_lower:
            return """
            SELECT 
                YEAR(O_ORDERDATE) as order_year,
                QUARTER(O_ORDERDATE) as order_quarter,
                SUM(O_TOTALPRICE) as total_revenue,
                COUNT(O_ORDERKEY) as order_count
            FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
            GROUP BY YEAR(O_ORDERDATE), QUARTER(O_ORDERDATE)
            ORDER BY order_year, order_quarter
            """
        
        elif "customer count" in question_lower and "nation" in question_lower:
            return """
            SELECT 
                n.N_NAME as nation_name,
                COUNT(DISTINCT c.C_CUSTKEY) as customer_count,
                SUM(c.C_ACCTBAL) as total_account_balance
            FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER c
            JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.NATION n ON c.C_NATIONKEY = n.N_NATIONKEY
            GROUP BY n.N_NAME
            ORDER BY customer_count DESC
            """
        
        elif "market segment" in question_lower and "revenue" in question_lower:
            return """
            SELECT 
                c.C_MKTSEGMENT as market_segment,
                SUM(o.O_TOTALPRICE) as total_revenue,
                COUNT(o.O_ORDERKEY) as order_count,
                COUNT(DISTINCT c.C_CUSTKEY) as customer_count
            FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
            JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER c ON o.O_CUSTKEY = c.C_CUSTKEY
            GROUP BY c.C_MKTSEGMENT
            ORDER BY total_revenue DESC
            """
        
        elif "monthly sales" in question_lower or "sales trends" in question_lower:
            return """
            SELECT 
                YEAR(O_ORDERDATE) as order_year,
                MONTH(O_ORDERDATE) as order_month,
                MONTHNAME(O_ORDERDATE) as month_name,
                SUM(O_TOTALPRICE) as total_revenue,
                COUNT(O_ORDERKEY) as order_count
            FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
            WHERE YEAR(O_ORDERDATE) BETWEEN 1992 AND 1998
            GROUP BY YEAR(O_ORDERDATE), MONTH(O_ORDERDATE), MONTHNAME(O_ORDERDATE)
            ORDER BY order_year, order_month
            """
        
        else:
            # Default query - show basic order statistics
            return """
            SELECT 
                COUNT(O_ORDERKEY) as total_orders,
                SUM(O_TOTALPRICE) as total_revenue,
                AVG(O_TOTALPRICE) as average_order_value,
                MIN(O_ORDERDATE) as earliest_order,
                MAX(O_ORDERDATE) as latest_order
            FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
            """
    
    def execute_query(self, sql_query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame."""
        if not self.session:
            raise Exception("No active session. Please connect first.")
        
        try:
            logger.info(f"Executing query: {sql_query}")
            result = self.session.sql(sql_query).to_pandas()
            return result
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return pd.DataFrame()
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Ask a natural language question and get results."""
        try:
            # Generate SQL from natural language
            sql_query = self.natural_language_to_sql(question)
            
            if not sql_query:
                return {
                    'success': False,
                    'error': 'Failed to generate SQL query',
                    'sql': None,
                    'data': pd.DataFrame()
                }
            
            # Execute the query
            data = self.execute_query(sql_query)
            
            return {
                'success': True,
                'sql': sql_query,
                'data': data,
                'question': question
            }
            
        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'sql': None,
                'data': pd.DataFrame()
            }
    
    def get_sample_questions(self) -> List[str]:
        """Get sample questions that can be asked."""
        return [
            "What is the total revenue by year?",
            "Show me the top 10 customers by total order value",
            "What is the average order value by market segment?",
            "How many orders were placed each month in 1995?",
            "Which nations have the highest total revenue?",
            "What is the distribution of orders by priority?",
            "Show me revenue trends by quarter",
            "What is the customer count by nation?",
            "Which market segments generate the most revenue?",
            "What are the monthly sales trends?"
        ]
    
    def get_table_preview(self, table_name: str, limit: int = 10) -> pd.DataFrame:
        """Get a preview of data from a specific table."""
        if not self.session:
            raise Exception("No active session. Please connect first.")
        
        # Find the base table for the given logical table name
        base_table = None
        for table in self.semantic_model.get('tables', []):
            if table['name'] == table_name:
                base_table = table['base_table']
                break
        
        if not base_table:
            raise ValueError(f"Table {table_name} not found in semantic model")
        
        try:
            query = f"SELECT * FROM {base_table} LIMIT {limit}"
            return self.execute_query(query)
        except Exception as e:
            logger.error(f"Error getting table preview: {str(e)}")
            return pd.DataFrame()
    
    def close(self):
        """Close the Snowflake session."""
        if self.session:
            self.session.close()
            logger.info("Session closed.")

def test_cortex_analyst():
    """Test the Cortex Analyst functionality."""
    analyst = CortexAnalyst()
    
    if analyst.connect():
        print("✅ Connection successful!")
        
        # Test semantic context
        context = analyst.get_semantic_context()
        print(f"Semantic Context Length: {len(context)} characters")
        
        # Test sample question
        question = "What is the total revenue by year?"
        result = analyst.ask_question(question)
        
        if result['success']:
            print(f"✅ Question processed successfully!")
            print(f"Generated SQL: {result['sql']}")
            print(f"Result shape: {result['data'].shape}")
        else:
            print(f"❌ Question processing failed: {result['error']}")
        
        analyst.close()
    else:
        print("❌ Connection failed!")

if __name__ == "__main__":
    test_cortex_analyst()