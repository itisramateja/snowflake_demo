# Snowflake Cortex Analyst Deployment Guide

This guide provides step-by-step instructions for deploying and using the Snowflake Cortex Analyst Streamlit application.

## 📋 Prerequisites

### Snowflake Requirements
- Snowflake account with Cortex features enabled
- Access to `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1` database
- User with appropriate permissions:
  - `USAGE` on warehouse
  - `USAGE` on database and schema
  - `SELECT` on tables
  - `USAGE` on Cortex functions (if using AI features)

### System Requirements
- Python 3.7 or higher
- Internet connection for package installation
- Web browser for accessing the Streamlit interface

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/itisramateja/snowflake_demo.git
cd snowflake_demo

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Credentials

```bash
# Copy the environment template
cp .env.template .env

# Edit the .env file with your Snowflake credentials
nano .env  # or use your preferred editor
```

**Required .env configuration:**
```bash
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_ROLE=your_role
SNOWFLAKE_DATABASE=SNOWFLAKE_SAMPLE_DATA
SNOWFLAKE_SCHEMA=TPCH_SF1
```

### 3. Test Connection

```bash
# Run the setup script to verify everything works
python setup.py

# Or test the connection manually
python cortex_analyst.py
```

### 4. Launch the Application

```bash
# For demo mode (no credentials required)
streamlit run demo_app.py --server.port 8501

# For production mode (requires Snowflake credentials)
streamlit run streamlit_app.py --server.port 8501
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SNOWFLAKE_ACCOUNT` | Your Snowflake account identifier | Yes | - |
| `SNOWFLAKE_USER` | Username for authentication | Yes | - |
| `SNOWFLAKE_PASSWORD` | Password for authentication | Yes | - |
| `SNOWFLAKE_WAREHOUSE` | Warehouse to use for queries | Yes | - |
| `SNOWFLAKE_ROLE` | Role to assume | Yes | - |
| `SNOWFLAKE_DATABASE` | Database name | No | `SNOWFLAKE_SAMPLE_DATA` |
| `SNOWFLAKE_SCHEMA` | Schema name | No | `TPCH_SF1` |

### Semantic Model Configuration

The semantic model is defined in `semantic_model.yaml`. You can customize:

- **Tables**: Add new logical tables and their mappings
- **Columns**: Define column descriptions and data types
- **Relationships**: Specify how tables are related
- **Metrics**: Add calculated fields and aggregations
- **Dimensions**: Define grouping and filtering attributes

Example table definition:
```yaml
tables:
  - name: "my_sales_data"
    description: "Custom sales data table"
    base_table: "MY_DATABASE.MY_SCHEMA.SALES"
    columns:
      - name: "sale_id"
        description: "Unique sale identifier"
        data_type: "NUMBER"
        expr: "SALE_ID"
```

## 🌐 Deployment Options

### Local Development

```bash
# Run locally with auto-reload
streamlit run streamlit_app.py --server.runOnSave true
```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t snowflake-cortex-analyst .
docker run -p 8501:8501 --env-file .env snowflake-cortex-analyst
```

### Cloud Deployment

#### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Add environment variables in the Streamlit Cloud dashboard
4. Deploy automatically

#### AWS/GCP/Azure
- Use container services (ECS, Cloud Run, Container Instances)
- Set environment variables through the cloud platform
- Configure load balancing and SSL if needed

## 🔒 Security Best Practices

### Credential Management
- Never commit `.env` files to version control
- Use cloud-native secret management services in production
- Rotate passwords regularly
- Use service accounts with minimal required permissions

### Network Security
- Deploy behind a VPN or private network when possible
- Use HTTPS in production
- Implement authentication/authorization if needed
- Monitor access logs

### Snowflake Security
- Use role-based access control (RBAC)
- Enable multi-factor authentication (MFA)
- Monitor query history and usage
- Set up network policies if required

## 📊 Usage Examples

### Basic Questions
```
"What is the total revenue by year?"
"Show me the top 10 customers by order value"
"What is the average order value by market segment?"
```

### Time-based Analysis
```
"How many orders were placed each month in 1995?"
"Show me quarterly revenue trends"
"What are the monthly sales patterns?"
```

### Geographic Analysis
```
"Which nations have the highest revenue?"
"Show me customer distribution by country"
"What is the revenue by region?"
```

### Customer Analysis
```
"Who are our most valuable customers?"
"What is the customer count by market segment?"
"Show me customer lifetime value distribution"
```

## 🛠️ Troubleshooting

### Common Issues

#### Connection Errors
```
Error: Failed to connect to Snowflake
```
**Solutions:**
- Verify credentials in `.env` file
- Check network connectivity
- Ensure warehouse is running
- Verify account identifier format

#### Permission Errors
```
Error: Insufficient privileges to operate on table
```
**Solutions:**
- Check user permissions
- Verify role assignments
- Ensure access to sample data
- Contact Snowflake administrator

#### Query Errors
```
Error: SQL compilation error
```
**Solutions:**
- Check semantic model configuration
- Verify table and column names
- Review generated SQL in the app
- Test queries manually in Snowflake

#### Performance Issues
```
Queries taking too long to execute
```
**Solutions:**
- Scale up warehouse size
- Optimize query patterns
- Add appropriate filters
- Consider data partitioning

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check Streamlit logs:
```bash
streamlit run streamlit_app.py --logger.level debug
```

### Getting Help

1. Check the application logs
2. Review Snowflake query history
3. Test individual components:
   ```bash
   python cortex_analyst.py
   python snowflake_connection.py
   ```
4. Consult Snowflake documentation
5. Open an issue on GitHub

## 📈 Performance Optimization

### Query Optimization
- Use appropriate warehouse sizes
- Implement query result caching
- Add filters to reduce data volume
- Use clustering keys for large tables

### Application Optimization
- Cache Streamlit components with `@st.cache_data`
- Implement connection pooling
- Use async operations where possible
- Optimize visualization rendering

### Monitoring
- Track query performance metrics
- Monitor warehouse usage
- Set up alerts for errors
- Log user interactions

## 🔄 Maintenance

### Regular Tasks
- Update dependencies monthly
- Review and rotate credentials quarterly
- Monitor usage patterns
- Update semantic model as data changes

### Backup and Recovery
- Backup semantic model configurations
- Document custom modifications
- Test disaster recovery procedures
- Maintain environment documentation

## 📚 Additional Resources

- [Snowflake Cortex Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Snowpark Python Guide](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)
- [TPCH Sample Data Reference](https://docs.snowflake.com/en/user-guide/sample-data-tpch)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

---

**Need help?** Open an issue on GitHub or contact the development team.