#!/usr/bin/env python3
"""
Streamlit App for Snowflake Cortex Analyst with Semantic Layer

This application provides a user-friendly interface to interact with 
Snowflake Cortex Analyst using natural language queries.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
from cortex_analyst import CortexAnalyst
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Snowflake Cortex Analyst",
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
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_analyst():
    """Initialize and cache the Cortex Analyst instance."""
    analyst = CortexAnalyst()
    if analyst.connect():
        return analyst
    else:
        return None

def create_visualization(data: pd.DataFrame, question: str):
    """Create appropriate visualization based on the data and question."""
    if data.empty:
        return None
    
    # Determine the best visualization type based on data characteristics
    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = data.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Convert date-like strings to datetime if possible
    for col in data.columns:
        if 'date' in col.lower() or 'year' in col.lower() or 'month' in col.lower():
            try:
                data[col] = pd.to_datetime(data[col])
                if col not in date_cols:
                    date_cols.append(col)
            except:
                pass
    
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
        
        elif 'date' in x_col.lower() or 'year' in x_col.lower():
            # Time series chart
            fig = px.line(data, x=x_col, y=y_col, title=f"Time Series: {question}")
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

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<div class="main-header">❄️ Snowflake Cortex Analyst</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Natural Language Analytics with Semantic Layer</div>', 
                unsafe_allow_html=True)
    
    # Initialize analyst
    with st.spinner("Initializing Cortex Analyst..."):
        analyst = initialize_analyst()
    
    if not analyst:
        st.error("❌ Failed to connect to Snowflake. Please check your credentials in the .env file.")
        st.stop()
    
    st.success("✅ Connected to Snowflake successfully!")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Semantic Model Info
        with st.expander("📊 Semantic Model", expanded=False):
            if analyst.semantic_model:
                st.write(f"**Name:** {analyst.semantic_model.get('name', 'N/A')}")
                st.write(f"**Description:** {analyst.semantic_model.get('description', 'N/A')}")
                
                # Tables
                st.write("**Available Tables:**")
                for table in analyst.semantic_model.get('tables', []):
                    st.write(f"• {table['name']}")
                
                # Metrics
                st.write("**Available Metrics:**")
                for metric in analyst.semantic_model.get('metrics', []):
                    st.write(f"• {metric['name']}")
        
        # Sample Questions
        st.header("💡 Sample Questions")
        sample_questions = analyst.get_sample_questions()
        
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
                result = analyst.ask_question(user_question)
            
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
        if analyst.semantic_model:
            table_names = [table['name'] for table in analyst.semantic_model.get('tables', [])]
            selected_table = st.selectbox("Select a table to preview:", table_names)
            
            if selected_table:
                with st.spinner(f"Loading preview for {selected_table}..."):
                    try:
                        preview_data = analyst.get_table_preview(selected_table, limit=5)
                        if not preview_data.empty:
                            st.subheader(f"Preview: {selected_table}")
                            st.dataframe(preview_data, use_container_width=True)
                        else:
                            st.warning("No data available for preview.")
                    except Exception as e:
                        st.error(f"Error loading preview: {str(e)}")
        
        # Connection info
        st.header("🔗 Connection Info")
        if analyst.session:
            try:
                current_db = analyst.session.get_current_database()
                current_schema = analyst.session.get_current_schema()
                current_warehouse = analyst.session.get_current_warehouse()
                
                st.info(f"""
                **Database:** {current_db}  
                **Schema:** {current_schema}  
                **Warehouse:** {current_warehouse}
                """)
            except:
                st.info("Connection details not available")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit and Snowflake Cortex Analyst | "
        "Powered by Semantic Layer Technology"
    )

if __name__ == "__main__":
    main()