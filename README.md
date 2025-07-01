# Snowflake Cortex Analyst Demo

This repository contains a comprehensive Snowflake demonstration project featuring a **Streamlit application with Cortex Analyst integration** and semantic layer capabilities.

## 🌟 Features

- **🤖 Natural Language Analytics**: Ask questions in plain English and get instant insights
- **📊 Interactive Streamlit Dashboard**: Beautiful, responsive web interface
- **🧠 Snowflake Cortex Integration**: Powered by AI for intelligent query generation
- **🗂️ Semantic Layer**: Predefined data model for consistent analytics
- **📈 Automatic Visualizations**: Charts and graphs generated automatically
- **💾 Data Export**: Download results as CSV files
- **🎯 Demo Mode**: Try it without Snowflake credentials using mock data

## 🚀 Quick Start

### Option 1: Demo Mode (No Credentials Required)
```bash
# Clone and setup
git clone https://github.com/itisramateja/snowflake_demo.git
cd snowflake_demo
pip install -r requirements.txt

# Launch demo with mock data
python launch.py --mode demo
```

### Option 2: Production Mode (Requires Snowflake)
```bash
# Setup environment
python launch.py --setup

# Configure credentials in .env file
# Then launch production app
python launch.py --mode production
```

## Getting Started

This project demonstrates how to connect to Snowflake using Python and perform advanced analytics with natural language queries.

### Prerequisites

- Python 3.7 or higher
- Snowflake account with appropriate credentials
- Access to a Snowflake warehouse, database, and schema

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/itisramateja/snowflake_demo.git
   cd snowflake_demo
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Snowflake credentials:
   ```bash
   cp .env.template .env
   ```
   
   Edit the `.env` file and fill in your Snowflake connection details:
   ```
   SNOWFLAKE_ACCOUNT=your_account_identifier
   SNOWFLAKE_USER=your_username
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_WAREHOUSE=your_warehouse
   SNOWFLAKE_DATABASE=your_database
   SNOWFLAKE_SCHEMA=your_schema
   SNOWFLAKE_ROLE=your_role
   ```

### Usage

#### Test Connection

To test your Snowflake connection:

```bash
python snowflake_connection.py
```

#### Run Examples

To see example usage of the Snowflake connection:

```bash
python example_usage.py
```

### Files Description

#### Core Applications
- `streamlit_app.py`: **Main Streamlit application** with Cortex Analyst integration
- `demo_app.py`: **Demo version** that works without Snowflake credentials
- `cortex_analyst.py`: Cortex Analyst integration with semantic layer support
- `launch.py`: **Easy launcher** for both demo and production modes

#### Data & Configuration
- `semantic_model.yaml`: **Semantic layer definition** for consistent analytics
- `.env.template`: Template for Snowflake connection credentials
- `requirements.txt`: Python dependencies including Streamlit and Snowpark

#### Legacy/Utilities
- `snowflake_connection.py`: Basic connection class for Snowflake
- `example_usage.py`: Example script demonstrating basic connection usage
- `setup.py`: Environment setup and validation script

#### Documentation
- `STREAMLIT_README.md`: Detailed Streamlit app documentation
- `DEPLOYMENT_GUIDE.md`: Complete deployment and configuration guide
- `.gitignore`: Git ignore file to prevent committing sensitive data

### Features

#### Streamlit Application
- ✅ **Natural Language Queries**: Ask questions in plain English
- ✅ **Interactive Dashboard**: Beautiful, responsive web interface
- ✅ **Automatic Visualizations**: Charts generated based on data
- ✅ **Semantic Layer**: Consistent data model and definitions
- ✅ **Data Export**: Download results as CSV files
- ✅ **Demo Mode**: Try without Snowflake credentials

#### Core Functionality
- ✅ **Secure Connection**: Environment variable-based authentication
- ✅ **Error Handling**: Comprehensive logging and error management
- ✅ **Query Execution**: Both basic and advanced SQL operations
- ✅ **Connection Management**: Proper resource cleanup
- ✅ **Snowpark Integration**: Modern Snowflake Python connector

### Security Notes

- Never commit your `.env` file to version control
- The `.env` file is already included in `.gitignore`
- Use strong passwords and follow your organization's security policies