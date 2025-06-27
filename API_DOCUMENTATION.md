# B2B Sales Analyst AI API Documentation

## Overview
The B2B Sales Analyst AI API provides AI-powered customer analysis and recommendation generation for B2B sales teams. It analyzes customer data to identify cross-sell and upsell opportunities and generates comprehensive research reports.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, no authentication is required. All endpoints are publicly accessible.

## Endpoints

### 1. Root Endpoint
**GET** `/`

Returns basic API information and status.

**Response:**
```json
{
  "message": "B2B Sales Analyst AI API",
  "version": "1.0.0",
  "status": "running",
  "pipeline_type": "Simple",
  "available_customers": 5,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 2. Health Check
**GET** `/health`

Returns the health status of the API and pipeline.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "pipeline_ready": true,
  "data_loaded": true,
  "pipeline_type": "Simple",
  "available_customers": 5
}
```

### 3. Get Customers
**GET** `/customers`

Returns a list of all available customers with basic information.

**Response:**
```json
{
  "customers": [
    {
      "customer_id": "C001",
      "company_name": "Edge Communications",
      "industry": "Electronics",
      "priority_rating": "Medium",
      "total_spent": 11250.0
    }
  ],
  "total_count": 5,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 4. Get Recommendations
**GET** `/recommendation`

**Parameters:**
- `customer_id` (required): The customer ID to analyze (e.g., "C001", "C002")
- `include_profile` (optional): Whether to include customer profile in response (default: false)

**Example Request:**
```
GET /recommendation?customer_id=C001&include_profile=true
```

**Response:**
```json
{
  "customer_id": "C001",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "research_report": "# B2B Sales Analysis Report\n## Edge Communications\n\n### Executive Summary\nThis analysis identifies 3 opportunities for Edge Communications...",
  "recommendations": [
    {
      "product": "Safety Gear",
      "type": "Cross-sell",
      "score": 0.85,
      "reason": "Frequently purchased in industry; High co-purchase affinity; High priority customer"
    }
  ],
  "summary": {
    "total_recommendations": 3,
    "cross_sell_count": 2,
    "upsell_count": 1,
    "top_recommendation_score": 0.85
  },
  "customer_profile": {
    "customer_id": "C001",
    "company_name": "Edge Communications",
    "industry": "Electronics",
    "annual_revenue": 139000000,
    "employees": 1000,
    "priority_rating": "Medium",
    "total_spent": 11250.0,
    "purchase_frequency": 6,
    "products_purchased": ["Drill Bits", "Protective Gloves", "Generators"]
  }
}
```

### 5. Reload Data
**POST** `/reload`

Reloads the customer data and reinitializes the pipeline.

**Response:**
```json
{
  "message": "Data reloaded successfully",
  "status": "success"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Customer ID is required"
}
```

### 404 Not Found
```json
{
  "detail": "Customer C999 not found. Available customers: ['C001', 'C002', 'C003', 'C004', 'C005']"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Processing error: Failed to generate customer profile"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Pipeline not initialized. Please check server logs."
}
```

## Usage Examples

### Python
```python
import requests

# Get all customers
response = requests.get("http://localhost:8000/customers")
customers = response.json()

# Get recommendations for a customer
response = requests.get("http://localhost:8000/recommendation?customer_id=C001")
recommendations = response.json()

print(f"Found {recommendations['summary']['total_recommendations']} opportunities")
```

### cURL
```bash
# Get recommendations
curl "http://localhost:8000/recommendation?customer_id=C001"

# Get recommendations with profile
curl "http://localhost:8000/recommendation?customer_id=C001&include_profile=true"

# Get all customers
curl "http://localhost:8000/customers"
```

### JavaScript
```javascript
// Get recommendations
fetch('http://localhost:8000/recommendation?customer_id=C001')
  .then(response => response.json())
  .then(data => {
    console.log('Recommendations:', data.recommendations);
    console.log('Report:', data.research_report);
  });
```

## Data Format

### Customer Data Structure
The API expects customer data in CSV format with the following columns:
- `Customer_ID`: Unique customer identifier
- `Product`: Product name
- `Quantity`: Purchase quantity
- `Unit Price(USD)`: Price per unit
- `Total_Price(USD)`: Total purchase amount
- `Purchase_Date`: Date of purchase
- `Customer_Name`: Company name
- `Industry`: Industry sector
- `Annual_Revenue(USD)`: Annual revenue
- `Number_of_Employees`: Employee count
- `Customer_Priority_Rating`: Priority level
- `Account_Type`: Account classification
- `Location`: Geographic location
- `Current_Products`: Current product usage
- `Product_Usage(%)`: Usage percentage
- `Last_Activity_Date`: Last activity date
- `Opportunity_Stage`: Sales stage
- `Opportunity_Amount(USD)`: Opportunity value
- `Competitors`: Competitor information

## Rate Limiting
Currently, no rate limiting is implemented. However, it's recommended to:
- Limit requests to reasonable frequency
- Cache results when possible
- Use the `/health` endpoint to check service status

## Performance
- Typical response time: 2-5 seconds
- Depends on data size and complexity
- LLM API calls may add latency

## Troubleshooting

### Common Issues

1. **"Pipeline not initialized"**
   - Check if the CSV file exists
   - Verify CSV format and column names
   - Check server logs for errors

2. **"Customer not found"**
   - Verify customer ID exists in data
   - Check for case sensitivity (IDs are normalized to uppercase)
   - Use `/customers` endpoint to see available IDs

3. **"Processing error"**
   - Check GROQ API key configuration
   - Verify internet connectivity for LLM calls
   - Check server logs for detailed error messages

### Debugging
- Use `/health` endpoint to check system status
- Check server console for detailed error logs
- Use `/customers` endpoint to verify data loading

## Support
For issues or questions:
1. Check the server logs
2. Verify your data format
3. Test with the provided test script: `python test_api.py` 