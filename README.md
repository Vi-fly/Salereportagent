# 🤖 B2B Sales Analyst AI

An intelligent B2B sales analysis system powered by AI agents that provides comprehensive customer insights, opportunity identification, and actionable recommendations.

## 🚀 Features

### 5 AI Agents Working Together:

1. **Customer Context Agent** - Extracts comprehensive customer profiles from data
2. **Purchase Pattern Analysis Agent** - Identifies product purchase frequency and missing opportunities
3. **Product Affinity Agent** - Suggests related/co-purchased products
4. **Opportunity Scoring Agent** - Scores cross-sell and upsell opportunities
5. **Recommendation Report Agent** - Generates natural language research reports

### Key Capabilities:

- 📊 **Customer Profile Analysis** - Deep insights into customer behavior and characteristics
- 🎯 **Opportunity Identification** - AI-powered cross-sell and upsell recommendations
- 📈 **Data Visualization** - Interactive charts and graphs
- 📝 **Research Reports** - Professional business reports with actionable insights
- 📥 **JSON Export** - Download recommendations in structured format
- 🎨 **Beautiful UI** - Modern, responsive interface built with Streamlit

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd b2b-sales-analyst-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the root directory
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```

## 🚀 Usage

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Select a customer ID** from the dropdown in the sidebar

4. **Click "Run Analysis"** to start the AI-powered analysis

5. **Explore the results** across 5 different tabs:
   - 📋 Customer Profile
   - 📊 Analysis Results
   - 🎯 Recommendations
   - 📝 Research Report
   - 📈 Visualizations

## 📊 Data Structure

The system expects a CSV file (`customer_data.csv`) with the following columns:

- `Customer ID` - Unique customer identifier
- `Product` - Product name
- `Quantity` - Purchase quantity
- `Unit Price (USD)` - Price per unit
- `Total Price (USD)` - Total transaction value
- `Purchase Date` - Date of purchase
- `Customer Name` - Company name
- `Industry` - Customer industry
- `Annual Revenue (USD)` - Company annual revenue
- `Number of Employees` - Company size
- `Customer Priority Rating` - Customer priority level
- `Account Type` - Account classification
- `Location` - Customer location
- `Current Products` - Currently used products
- `Product Usage (%)` - Product utilization percentage
- `Cross-Sell Synergy` - Cross-selling opportunities
- `Last Activity Date` - Last customer interaction
- `Opportunity Stage` - Sales opportunity stage
- `Opportunity Amount (USD)` - Opportunity value
- `Opportunity Type` - Type of opportunity
- `Competitors` - Known competitors
- `Activity Status` - Activity status
- `Activity Priority` - Activity priority level
- `Activity Type` - Type of activity
- `Product SKU` - Product stock keeping unit

## 🤖 AI Agents Explained

### 1. Customer Context Agent
- **Purpose**: Extract customer profile from CSV or DB
- **Input**: customer_id
- **Output**: Customer profile dictionary
- **Function**: Analyzes customer data to create comprehensive profiles including purchase history, company information, and behavioral patterns

### 2. Purchase Pattern Analysis Agent
- **Purpose**: Identify product purchase frequency and missing opportunities
- **Input**: Customer products
- **Output**: Frequent & missing product sets
- **Function**: Compares customer purchases with industry patterns to identify gaps and opportunities

### 3. Product Affinity Agent
- **Purpose**: Suggest related/co-purchased products
- **Input**: Customer products
- **Output**: Related product suggestions
- **Function**: Uses co-purchase analysis to find products that are frequently bought together

### 4. Opportunity Scoring Agent
- **Purpose**: Score cross-sell and upsell opportunities
- **Input**: Prior agents' data
- **Output**: Scored product list with rationale
- **Function**: Applies scoring algorithms to rank opportunities based on multiple factors

### 5. Recommendation Report Agent
- **Purpose**: Generate natural language research report & recommendations
- **Input**: Scored opportunities
- **Output**: Research report text
- **Function**: Creates professional business reports using AI language models

## 📤 Output Format

The system generates recommendations in the following JSON format:

```json
{
  "research_report": "<comprehensive business report>",
  "recommendations": [
    {
      "product": "Product Name",
      "type": "Cross-sell|Upsell|New Opportunity",
      "score": 0.85,
      "reason": "Detailed rationale for recommendation"
    }
  ]
}
```

## 🎯 Scoring System

Opportunities are scored from 0 to 1 based on:

- **Industry Relevance** (30%) - How common the product is in the customer's industry
- **Product Affinity** (20%) - Co-purchase patterns with existing products
- **Customer Priority** (20%) - Customer's priority rating
- **Revenue Potential** (15%) - Customer's annual revenue
- **Purchase Behavior** (15%) - Historical purchase frequency

## 🔧 Configuration

### Environment Variables:
- `GROQ_API_KEY` - Your Groq API key for AI model access

### Customization:
- Modify agent logic in `agents.py`
- Adjust scoring weights in `OpportunityScoringAgent`
- Customize UI styling in `app.py`

## 📈 Performance

- **Real-time Analysis**: Complete analysis runs in seconds
- **Scalable**: Handles large customer datasets efficiently
- **Caching**: Results cached for improved performance
- **Error Handling**: Graceful fallbacks if API calls fail

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

## 🔮 Future Enhancements

- [ ] Integration with CRM systems
- [ ] Real-time data streaming
- [ ] Advanced machine learning models
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] API endpoints for external integration 