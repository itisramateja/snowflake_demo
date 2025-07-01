#!/usr/bin/env python3
"""
Demo Streamlit App for Snowflake Cortex Analyst with Semantic Layer

This is a demonstration version that works without actual Snowflake credentials.
It shows the UI and functionality using mock data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, date
import numpy as np
import random

# Page configuration
st.set_page_config(
    page_title="Snowflake Cortex Analyst Demo",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .sql-code {
        background-color: #f1f3f4;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
    .demo-banner {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def generate_mock_data(question: str) -> dict:
    """Generate mock data based on the question type."""
    question_lower = question.lower()
    
    if "total revenue" in question_lower and "year" in question_lower:
        years = list(range(1992, 1999))
        revenues = [random.uniform(50000000, 150000000) for _ in years]
        data = pd.DataFrame({
            'order_year': years,
            'total_revenue': revenues
        })
        sql = """
        SELECT 
            YEAR(o.O_ORDERDATE) as order_year,
            SUM(o.O_TOTALPRICE) as total_revenue
        FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
        GROUP BY YEAR(o.O_ORDERDATE)
        ORDER BY order_year
        """
        
    elif "top" in question_lower and "customer" in question_lower:
        customers = [f"Customer_{i:03d}" for i in range(1, 11)]
        values = sorted([random.uniform(100000, 500000) for _ in customers], reverse=True)
        orders = [random.randint(5, 25) for _ in customers]
        data = pd.DataFrame({
            'customer_name': customers,
            'total_order_value': values,
            'order_count': orders
        })
        sql = """
        SELECT 
            c.C_NAME as customer_name,
            SUM(o.O_TOTALPRICE) as total_order_value,
            COUNT(o.O_ORDERKEY) as order_count
        FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
        JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER c ON o.O_CUSTKEY = c.C_CUSTKEY
        GROUP BY c.C_NAME
        ORDER BY total_order_value DESC
        LIMIT 10
        """
        
    elif "market segment" in question_lower:
        segments = ['AUTOMOBILE', 'BUILDING', 'FURNITURE', 'MACHINERY', 'HOUSEHOLD']
        if "revenue" in question_lower:
            revenues = [random.uniform(20000000, 80000000) for _ in segments]
            orders = [random.randint(10000, 50000) for _ in segments]
            customers = [random.randint(5000, 15000) for _ in segments]
            data = pd.DataFrame({
                'market_segment': segments,
                'total_revenue': revenues,
                'order_count': orders,
                'customer_count': customers
            })
        else:
            avg_values = [random.uniform(30000, 80000) for _ in segments]
            orders = [random.randint(10000, 50000) for _ in segments]
            data = pd.DataFrame({
                'market_segment': segments,
                'average_order_value': avg_values,
                'order_count': orders
            })
        sql = """
        SELECT 
            c.C_MKTSEGMENT as market_segment,
            SUM(o.O_TOTALPRICE) as total_revenue,
            COUNT(o.O_ORDERKEY) as order_count
        FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
        JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER c ON o.O_CUSTKEY = c.C_CUSTKEY
        GROUP BY c.C_MKTSEGMENT
        ORDER BY total_revenue DESC
        """
        
    elif "nation" in question_lower and "revenue" in question_lower:
        nations = ['UNITED STATES', 'GERMANY', 'FRANCE', 'JAPAN', 'UNITED KINGDOM', 
                  'CANADA', 'BRAZIL', 'RUSSIA', 'INDIA', 'CHINA']
        revenues = sorted([random.uniform(5000000, 25000000) for _ in nations], reverse=True)
        orders = [random.randint(1000, 8000) for _ in nations]
        avg_values = [rev/ord for rev, ord in zip(revenues, orders)]
        data = pd.DataFrame({
            'nation_name': nations,
            'total_revenue': revenues,
            'order_count': orders,
            'average_order_value': avg_values
        })
        sql = """
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
        
    elif "month" in question_lower and "1995" in question_lower:
        months = list(range(1, 13))
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        orders = [random.randint(800, 1500) for _ in months]
        revenues = [ord * random.uniform(40000, 80000) for ord in orders]
        data = pd.DataFrame({
            'order_month': months,
            'month_name': month_names,
            'order_count': orders,
            'total_revenue': revenues
        })
        sql = """
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
        
    else:
        # Default statistics
        data = pd.DataFrame({
            'metric': ['Total Orders', 'Total Revenue', 'Average Order Value'],
            'value': [1500000, 229577310.42, 152.93]
        })
        sql = """
        SELECT 
            COUNT(O_ORDERKEY) as total_orders,
            SUM(O_TOTALPRICE) as total_revenue,
            AVG(O_TOTALPRICE) as average_order_value
        FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
        """
    
    return {
        'success': True,
        'sql': sql,
        'data': data,
        'question': question
    }

def create_visualization(data: pd.DataFrame, question: str):
    """Create appropriate visualization based on the data and question."""
    if data.empty:
        return None
    
    # Determine the best visualization type based on data characteristics
    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Create visualization based on data structure
    if len(data.columns) == 2:
        x_col, y_col = data.columns[0], data.columns[1]
        
        if data[x_col].dtype in ['object', 'category'] and pd.api.types.is_numeric_dtype(data[y_col]):
            # Bar chart for categorical vs numeric
            fig = px.bar(data, x=x_col, y=y_col, title=f"Analysis: {question}")
            fig.update_layout(xaxis_tickangle=-45)
            return fig
        
        elif pd.api.types.is_numeric_dtype(data[x_col]) and pd.api.types.is_numeric_dtype(data[y_col]):
            # Line chart for numeric vs numeric (assuming time series)
            fig = px.line(data, x=x_col, y=y_col, title=f"Trend Analysis: {question}")
            return fig
    
    elif len(data.columns) > 2:
        # Multi-column data - create a more complex visualization
        if len(numeric_cols) >= 2:
            # Scatter plot for multiple numeric columns
            fig = px.scatter(data, x=numeric_cols[0], y=numeric_cols[1], 
                           color=categorical_cols[0] if categorical_cols else None,
                           title=f"Multi-dimensional Analysis: {question}")
            return fig
        elif len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
            # Grouped bar chart
            fig = px.bar(data, x=categorical_cols[0], y=numeric_cols[0],
                        color=categorical_cols[1] if len(categorical_cols) > 1 else None,
                        title=f"Grouped Analysis: {question}")
            return fig
    
    # Default: simple bar chart with first two columns
    if len(data.columns) >= 2:
        fig = px.bar(data, x=data.columns[0], y=data.columns[1], 
                    title=f"Data Visualization: {question}")
        return fig
    
    return None

def display_metrics(data: pd.DataFrame):
    """Display key metrics from the data."""
    if data.empty:
        return
    
    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        cols = st.columns(min(len(numeric_cols), 4))
        for i, col in enumerate(numeric_cols[:4]):
            with cols[i]:
                if data[col].dtype in ['int64', 'float64']:
                    value = data[col].sum() if 'count' in col.lower() else data[col].mean()
                    st.metric(
                        label=col.replace('_', ' ').title(),
                        value=f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"
                    )

def get_sample_questions():
    """Get sample questions for the demo."""
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

def get_semantic_model_info():
    """Get semantic model information for display."""
    return {
        'name': 'Sales Analytics Semantic Model',
        'description': 'A semantic model for sales data analysis using Snowflake Cortex Analyst',
        'tables': [
            {'name': 'sales_data', 'description': 'Main sales transaction data'},
            {'name': 'customer_data', 'description': 'Customer information'},
            {'name': 'nation_data', 'description': 'Nation/country information'}
        ],
        'metrics': [
            {'name': 'total_revenue', 'description': 'Total revenue from all orders'},
            {'name': 'average_order_value', 'description': 'Average value per order'},
            {'name': 'order_count', 'description': 'Total number of orders'},
            {'name': 'customer_count', 'description': 'Total number of unique customers'}
        ]
    }

def main():
    """Main Streamlit application."""
    
    # Demo banner
    st.markdown("""
    <div class="demo-banner">
        <h3>🎯 Demo Mode</h3>
        <p>This is a demonstration of the Snowflake Cortex Analyst Streamlit App using mock data. 
        To use with real Snowflake data, configure your credentials in the .env file and run streamlit_app.py</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">❄️ Snowflake Cortex Analyst</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Natural Language Analytics with Semantic Layer (Demo)</div>', 
                unsafe_allow_html=True)
    
    st.success("✅ Demo mode active - using mock data for demonstration")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Semantic Model Info
        with st.expander("📊 Semantic Model", expanded=False):
            semantic_model = get_semantic_model_info()
            st.write(f"**Name:** {semantic_model['name']}")
            st.write(f"**Description:** {semantic_model['description']}")
            
            # Tables
            st.write("**Available Tables:**")
            for table in semantic_model['tables']:
                st.write(f"• {table['name']}")
            
            # Metrics
            st.write("**Available Metrics:**")
            for metric in semantic_model['metrics']:
                st.write(f"• {metric['name']}")
        
        # Sample Questions
        st.header("💡 Sample Questions")
        sample_questions = get_sample_questions()
        
        for i, question in enumerate(sample_questions[:5]):
            if st.button(f"📝 {question}", key=f"sample_{i}"):
                st.session_state.user_question = question
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🤖 Ask Your Question")
        
        # Question input
        user_question = st.text_area(
            "Enter your question in natural language:",
            value=st.session_state.get('user_question', ''),
            height=100,
            placeholder="e.g., What is the total revenue by year?"
        )
        
        # Clear the session state after using it
        if 'user_question' in st.session_state:
            del st.session_state.user_question
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            analyze_btn = st.button("🔍 Analyze", type="primary")
        with col_btn2:
            clear_btn = st.button("🗑️ Clear")
        
        if clear_btn:
            st.rerun()
        
        if analyze_btn and user_question:
            with st.spinner("🧠 Processing your question..."):
                result = generate_mock_data(user_question)
            
            if result['success']:
                st.markdown('<div class="success-message">✅ Analysis completed successfully!</div>', 
                           unsafe_allow_html=True)
                
                # Display generated SQL
                with st.expander("🔍 Generated SQL Query", expanded=False):
                    st.code(result['sql'], language='sql')
                
                # Display metrics
                if not result['data'].empty:
                    st.subheader("📊 Key Metrics")
                    display_metrics(result['data'])
                    
                    # Display data table
                    st.subheader("📋 Results")
                    st.dataframe(result['data'], use_container_width=True)
                    
                    # Create visualization
                    fig = create_visualization(result['data'], user_question)
                    if fig:
                        st.subheader("📈 Visualization")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Download option
                    csv = result['data'].to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ No data returned from the query.")
            else:
                st.markdown(f'<div class="error-message">❌ Error: {result["error"]}</div>', 
                           unsafe_allow_html=True)
    
    with col2:
        st.header("📊 Data Explorer")
        
        # Table preview
        table_names = ['sales_data', 'customer_data', 'nation_data']
        selected_table = st.selectbox("Select a table to preview:", table_names)
        
        if selected_table:
            st.subheader(f"Preview: {selected_table}")
            
            # Generate mock preview data
            if selected_table == 'sales_data':
                preview_data = pd.DataFrame({
                    'order_key': [1, 2, 3, 4, 5],
                    'customer_key': [101, 102, 103, 104, 105],
                    'order_status': ['O', 'F', 'O', 'P', 'F'],
                    'total_price': [45000.50, 32000.75, 67000.25, 28000.00, 55000.80],
                    'order_date': ['1995-01-15', '1995-02-20', '1995-03-10', '1995-04-05', '1995-05-12']
                })
            elif selected_table == 'customer_data':
                preview_data = pd.DataFrame({
                    'customer_key': [101, 102, 103, 104, 105],
                    'customer_name': ['Customer_001', 'Customer_002', 'Customer_003', 'Customer_004', 'Customer_005'],
                    'nation_key': [1, 2, 3, 1, 2],
                    'market_segment': ['AUTOMOBILE', 'BUILDING', 'FURNITURE', 'MACHINERY', 'HOUSEHOLD'],
                    'account_balance': [5000.50, 7500.25, 3200.75, 9800.00, 4500.30]
                })
            else:  # nation_data
                preview_data = pd.DataFrame({
                    'nation_key': [1, 2, 3, 4, 5],
                    'nation_name': ['UNITED STATES', 'GERMANY', 'FRANCE', 'JAPAN', 'UNITED KINGDOM'],
                    'region_key': [1, 1, 1, 2, 1]
                })
            
            st.dataframe(preview_data, use_container_width=True)
        
        # Connection info
        st.header("🔗 Connection Info")
        st.info("""
        **Mode:** Demo Mode  
        **Database:** SNOWFLAKE_SAMPLE_DATA  
        **Schema:** TPCH_SF1  
        **Status:** Mock Data Active
        """)
        
        # Demo instructions
        st.header("🚀 Getting Started")
        st.markdown("""
        **To use with real Snowflake data:**
        
        1. Configure your `.env` file with Snowflake credentials
        2. Run `streamlit run streamlit_app.py`
        3. Ask questions in natural language
        4. Get instant insights from your data!
        
        **Demo Features:**
        - Natural language query interface
        - Automatic SQL generation
        - Interactive visualizations
        - Data export capabilities
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit and Snowflake Cortex Analyst | "
        "Powered by Semantic Layer Technology | "
        "**Demo Mode - Using Mock Data**"
    )

if __name__ == "__main__":
    main()