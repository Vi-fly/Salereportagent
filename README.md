# 🤖 B2B Sales Analyst AI

A sophisticated AI-powered system for analyzing customer data and generating cross-sell/upsell recommendations using LangGraph and modular agents.

## 🚀 Features

- **Modular Agent Architecture**: Separate specialized agents for different analysis tasks
- **Customer Profiling**: Comprehensive customer behavior analysis
- **Purchase Pattern Recognition**: Seasonal trends and frequency analysis
- **Product Affinity Mapping**: Identify product relationships and preferences
- **Opportunity Scoring**: AI-powered scoring of cross-sell/upsell opportunities
- **Research Report Generation**: Detailed, actionable recommendations
- **Streamlit Web Interface**: User-friendly web application
- **Data Export**: Download analysis results in JSON format

## 🏗️ Architecture

The system uses a pipeline of specialized agents:

1. **Customer Context Agent**: Analyzes customer profile and purchase history
2. **Purchase Pattern Agent**: Identifies seasonal trends and buying patterns
3. **Product Affinity Agent**: Maps product relationships and preferences
4. **Opportunity Scoring Agent**: Scores potential cross-sell/upsell opportunities
5. **Recommendation Report Agent**: Generates comprehensive research reports

## 📋 Requirements

- Python 3.8+
- LangGraph 0.0.40
- Streamlit
- Pandas
- OpenAI API key (for LLM functionality)

## 🛠️ Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd b2b-sales-analyst-ai
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 🚀 Usage

### Running the Streamlit App

1. **Start the application**:
```bash
streamlit run app.py
```

2. **Upload your data**:
   - Use the provided `sample_data.csv` for testing
   - Or upload your own CSV file with the required columns

3. **Select a customer**:
   - Choose a customer ID from the dropdown
   - Click "Generate Analysis" to start the pipeline

4. **Review results**:
   - Customer profile metrics
   - Purchase pattern analysis
   - Product affinity mapping
   - Scored opportunities
   - Comprehensive research report

### Expected CSV Format

Your CSV file should contain these columns:
- `customer_id`: Unique identifier for each customer
- `product_name`: Name of the purchased product
- `purchase_date`: Date of purchase (YYYY-MM-DD format)
- `amount`: Purchase amount (numeric)
- `category`: Product category

Example:
```csv
customer_id,product_name,purchase_date,amount,category
CUST001,Enterprise Software,2024-01-15,5000.00,Software
CUST001,Cloud Storage,2024-02-20,1200.00,Software
```

## 📁 Project Structure

```
b2b-sales-analyst-ai/
├── agents.py              # Modular agent implementations
├── pipeline.py            # LangGraph pipeline definition
├── app.py                 # Streamlit web application
├── sample_data.csv        # Sample data for testing
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # This file
```

## 🔧 Configuration

### Agent Configuration

Each agent can be customized in `agents.py`:

- **Analysis depth**: Modify prompts for more detailed analysis
- **Scoring criteria**: Adjust opportunity scoring algorithms
- **Report format**: Customize report structure and content

### Pipeline Configuration

The pipeline in `pipeline.py` can be modified to:

- Add new analysis steps
- Change the order of operations
- Add conditional logic based on data characteristics

## 📊 Output Format

The system generates comprehensive analysis including:

### Customer Profile
- Total purchases and spending
- Average order value
- Purchase history summary

### Pattern Analysis
- Seasonal buying trends
- Purchase frequency patterns
- Growth trajectory

### Product Affinity
- Top product categories
- Product relationship mapping
- Cross-category preferences

### Scored Opportunities
- Ranked list of recommendations
- Confidence scores (1-10)
- Detailed reasoning for each opportunity

### Research Report
- Executive summary
- Detailed analysis
- Actionable recommendations
- Risk assessment

## 🔍 Example Output

```json
{
  "customer_id": "CUST001",
  "profile": {
    "total_purchases": 3,
    "total_spent": 9200.00,
    "avg_order_value": 3066.67
  },
  "opportunities": [
    {
      "product": "Advanced Analytics Suite",
      "score": 8.5,
      "reasoning": "Customer shows strong interest in data tools"
    }
  ],
  "report": "Comprehensive analysis and recommendations..."
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed correctly
2. **API Key Issues**: Verify your OpenAI API key is set in `.env`
3. **Data Format**: Check that your CSV has the required columns
4. **Memory Issues**: For large datasets, consider data sampling

### Error Messages

- `Customer not found`: Verify customer ID exists in your data
- `Column not found`: Check CSV column names match expected format
- `API rate limit`: Wait and retry, or check API key validity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the error logs
3. Open an issue on GitHub
4. Contact the development team

## 🔮 Future Enhancements

- **Real-time Data Integration**: Connect to live CRM systems
- **Advanced ML Models**: Implement predictive analytics
- **Multi-language Support**: Add internationalization
- **API Endpoints**: Create REST API for integration
- **Dashboard Analytics**: Add interactive charts and graphs
- **Automated Alerts**: Set up notification systems for opportunities 