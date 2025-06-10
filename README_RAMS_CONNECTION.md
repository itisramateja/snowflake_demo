# Snowflake Connection Script for User: rams

This repository contains Python scripts to connect to Snowflake using the credentials for user `rams`.

## Files

- `snowflake_connect_rams.py` - Main connection script with hardcoded credentials
- `connect_with_credentials.py` - Alternative connection script
- `snowflake_connection.py` - Generic connection class using environment variables
- `example_usage.py` - Example usage of the generic connection class

## Quick Start

### Prerequisites

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Using the Main Script

The main script `snowflake_connect_rams.py` contains the following hardcoded credentials:
- **Username**: rams
- **Password**: Sumajavikhyavihaan1981
- **Warehouse**: compute_wh
- **Role**: accountadmin

To use the script, you need to provide your Snowflake account identifier:

```bash
python snowflake_connect_rams.py <your_account_identifier>
```

### Finding Your Account Identifier

Your Snowflake account identifier can be found in:

1. **Snowflake Web Interface URL**: Look at your Snowflake URL
   - New format: `https://app.snowflake.com/organization-account/`
   - Legacy format: `https://account.region.snowflakecomputing.com/`

2. **Account Formats**:
   - **New accounts**: `organization-account_name`
   - **Legacy accounts**: `account_name.region.cloud_provider`

3. **Examples**:
   - `myorg-myaccount`
   - `xy12345.us-east-1.aws`
   - `ab67890.eu-west-1.azure`

### Example Usage

```bash
# Example with new account format
python snowflake_connect_rams.py myorg-myaccount

# Example with legacy account format
python snowflake_connect_rams.py xy12345.us-east-1.aws
```

### What the Script Does

When you run the script successfully, it will:

1. **Connect to Snowflake** using the provided credentials
2. **Display connection information**:
   - Current warehouse
   - Current database
   - Current schema
   - Current role
   - Current user
   - Current timestamp
   - Snowflake version

3. **Run sample queries**:
   - Simple calculations
   - Date functions
   - String manipulation
   - Random numbers

4. **List available objects**:
   - Databases
   - Warehouses
   - Roles

### Interactive Mode

If you run the script without arguments, it will prompt you to enter your account identifier:

```bash
python snowflake_connect_rams.py
```

### Troubleshooting

If the connection fails, check:

1. **Account identifier is correct**
   - Verify the format matches your Snowflake account
   - Check for typos

2. **Credentials are valid**
   - Username: rams
   - Password: Sumajavikhyavihaan1981
   - Ensure the user exists and password is correct

3. **Network connectivity**
   - Ensure your network can reach Snowflake
   - Check firewall settings

4. **Warehouse exists**
   - Verify 'compute_wh' warehouse exists
   - Ensure the user has access to it

5. **Role assignment**
   - Verify 'accountadmin' role is assigned to user 'rams'
   - Check role permissions

### Security Note

⚠️ **Important**: This script contains hardcoded credentials. In production environments, consider using:
- Environment variables
- Configuration files (not committed to version control)
- Secure credential management systems
- Key-pair authentication

### Alternative Scripts

- Use `snowflake_connection.py` with environment variables for more secure credential management
- Use `connect_with_credentials.py` for a simpler connection example

## Dependencies

- `snowflake-connector-python==3.15.0`
- `python-dotenv==1.0.0`

## Support

If you encounter issues:
1. Check the Snowflake documentation
2. Verify your account settings
3. Contact your Snowflake administrator