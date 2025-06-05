# Snowflake Demo

This repository contains a Snowflake demonstration project with Python connectivity.

## Getting Started

This project demonstrates how to connect to Snowflake using Python and perform basic operations.

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

- `snowflake_connection.py`: Main connection class with methods for connecting to Snowflake
- `example_usage.py`: Example script demonstrating how to use the connection
- `.env.template`: Template for environment variables
- `requirements.txt`: Python dependencies
- `.gitignore`: Git ignore file to prevent committing sensitive data

### Features

- ✅ Secure connection using environment variables
- ✅ Error handling and logging
- ✅ Basic query execution
- ✅ Connection management (open/close)
- ✅ Example usage patterns

### Security Notes

- Never commit your `.env` file to version control
- The `.env` file is already included in `.gitignore`
- Use strong passwords and follow your organization's security policies