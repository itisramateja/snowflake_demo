# Snowflake Cortex Analyst Streamlit App

A powerful Streamlit application that leverages Snowflake Cortex Analyst with a semantic layer to enable natural language analytics. Ask questions in plain English and get instant insights from your Snowflake data!

## 🌟 Features

- **Natural Language Queries**: Ask questions in plain English
- **Semantic Layer Integration**: Predefined data model for consistent analytics
- **Interactive Visualizations**: Automatic chart generation based on query results
- **SQL Generation**: See the SQL queries generated from your natural language questions
- **Data Explorer**: Browse and preview your data tables
- **Export Capabilities**: Download results as CSV files
- **Real-time Analytics**: Instant results powered by Snowflake Cortex

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  Cortex Analyst  │────│   Snowflake     │
│                 │    │                  │    │                 │
│ • Natural Lang  │    │ • Semantic Layer │    │ • Sample Data   │
│ • Visualizations│    │ • SQL Generation │    │ • Cortex AI     │
│ • Data Explorer │    │ • Query Execution│    │ • Analytics     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Snowflake account with Cortex features enabled
- Access to Snowflake sample data (TPCH_SF1)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/itisramateja/snowflake_demo.git
   cd snowflake_demo
   ```

2. **Run the setup script**:
   ```bash
   python setup.py
   ```

3. **Configure your credentials** (if not done automatically):
   ```bash
   cp .env.template .env
   # Edit .env with your Snowflake credentials
   ```

4. **Launch the Streamlit app**:
   ```bash
   streamlit run streamlit_app.py --server.port 12000 --server.address 0.0.0.0
   ```

5. **Open your browser** and navigate to the provided URL

## 📊 Semantic Model

The application uses a predefined semantic model that includes:

### Tables
- **sales_data**: Order transactions from TPCH sample data
- **customer_data**: Customer information and demographics
- **nation_data**: Geographic information

### Metrics
- **total_revenue**: Sum of all order values
- **average_order_value**: Mean order value
- **order_count**: Total number of orders
- **customer_count**: Unique customer count

### Dimensions
- **order_year**: Year of order placement
- **order_month**: Month of order placement
- **order_quarter**: Quarter of order placement

## 💬 Example Questions

Try asking these natural language questions:

### Revenue Analysis
- "What is the total revenue by year?"
- "Show me monthly revenue trends for 1995"
- "Which market segments generate the most revenue?"

### Customer Analytics
- "Show me the top 10 customers by total order value"
- "What is the customer count by nation?"
- "How is revenue distributed across market segments?"

### Order Analysis
- "How many orders were placed each month in 1995?"
- "What is the distribution of orders by priority?"
- "Show me average order value by customer segment"

### Geographic Analysis
- "Which nations have the highest total revenue?"
- "Show me revenue by region"
- "What are the top performing countries?"

## 🎨 User Interface

### Main Dashboard
- **Question Input**: Natural language query interface
- **Results Display**: Automatic data tables and visualizations
- **SQL Viewer**: See the generated SQL queries
- **Export Options**: Download results as CSV

### Sidebar Features
- **Semantic Model Info**: View available tables, metrics, and dimensions
- **Sample Questions**: Quick-start with predefined questions
- **Data Explorer**: Preview table contents
- **Connection Status**: Monitor Snowflake connection

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Snowflake Connection
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=compute_wh
SNOWFLAKE_ROLE=accountadmin
SNOWFLAKE_DATABASE=SNOWFLAKE_SAMPLE_DATA
SNOWFLAKE_SCHEMA=TPCH_SF1
```

### Semantic Model (semantic_model.yaml)
The semantic model defines:
- Table mappings to physical Snowflake tables
- Column definitions and descriptions
- Relationships between tables
- Predefined metrics and calculations
- Dimensional attributes for grouping

## 📈 Visualizations

The app automatically creates appropriate visualizations based on your data:

- **Bar Charts**: For categorical data analysis
- **Line Charts**: For time series and trends
- **Scatter Plots**: For multi-dimensional analysis
- **Metrics Cards**: For key performance indicators

## 🛠️ Development

### Project Structure
```
snowflake_demo/
├── streamlit_app.py          # Main Streamlit application
├── cortex_analyst.py         # Cortex Analyst integration
├── semantic_model.yaml       # Semantic layer definition
├── setup.py                  # Setup and installation script
├── requirements.txt          # Python dependencies
├── .env.template             # Environment variables template
└── README.md                 # This file
```

### Key Components

1. **CortexAnalyst Class**: Handles Snowflake connections and natural language processing
2. **Semantic Model**: YAML-based data model definition
3. **Streamlit UI**: Interactive web interface
4. **Visualization Engine**: Automatic chart generation

### Adding New Tables

To add new tables to the semantic model:

1. Update `semantic_model.yaml` with new table definitions
2. Define column mappings and relationships
3. Add relevant metrics and dimensions
4. Restart the application

### Customizing Visualizations

Modify the `create_visualization()` function in `streamlit_app.py` to:
- Add new chart types
- Customize styling
- Implement domain-specific visualizations

## 🔒 Security

- Environment variables for credential management
- No hardcoded passwords or sensitive information
- Secure Snowflake connection using official connectors
- Session management and proper connection cleanup

## 🐛 Troubleshooting

### Common Issues

1. **Connection Failed**
   - Verify Snowflake credentials in `.env`
   - Check network connectivity
   - Ensure warehouse is running

2. **No Data Returned**
   - Verify access to SNOWFLAKE_SAMPLE_DATA
   - Check user permissions
   - Ensure correct database/schema settings

3. **SQL Generation Errors**
   - Check Cortex feature availability
   - Verify semantic model syntax
   - Review question complexity

### Debug Mode

Enable debug logging by setting:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Resources

- [Snowflake Cortex Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Snowpark Python Documentation](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For questions or issues:
1. Check the troubleshooting section
2. Review Snowflake documentation
3. Open an issue on GitHub
4. Contact the development team

---

**Happy Analytics!** 🎉