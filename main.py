from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from data_loader import load_customer_data_csv
from typing import Optional, Dict, Any
import os
import traceback
from datetime import datetime

app = FastAPI(
    title="B2B Sales Analyst AI API",
    description="AI-powered B2B sales analysis and recommendation system using LangGraph",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
customer_data = None
pipeline = None

def initialize_pipeline():
    """Initialize the LangGraph pipeline"""
    global customer_data, pipeline
    
    try:
        from pipeline import build_pipeline
        customer_data = load_customer_data_csv(os.getenv('CSV_PATH', 'customer_data.csv'))
        pipeline = build_pipeline(customer_data)
        print("✅ LangGraph pipeline built successfully")
        return True
    except Exception as e:
        print(f"❌ LangGraph pipeline failed: {e}")
        customer_data = None
        pipeline = None
        return False

# Initialize on startup
initialize_pipeline()

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "B2B Sales Analyst AI API",
        "version": "1.0.0",
        "status": "running",
        "pipeline_type": "LangGraph",
        "available_customers": len(customer_data['Customer_ID'].unique()) if customer_data is not None else 0,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/recommendation")
def get_recommendation(
    customer_id: str = Query(..., description="Customer ID to analyze (e.g., C001, C002)"),
    include_profile: bool = Query(False, description="Include customer profile in response")
):
    """
    Get AI-generated recommendations and research report for a customer using LangGraph pipeline.
    
    Args:
        customer_id: The customer ID to analyze
        include_profile: Whether to include customer profile in response
    
    Returns:
        JSON with research report and recommendations
    """
    # Validate pipeline
    if not pipeline or customer_data is None or customer_data.empty:
        raise HTTPException(
            status_code=503, 
            detail="LangGraph pipeline not initialized. Please check server logs."
        )
    
    # Validate customer_id
    if not customer_id or not customer_id.strip():
        raise HTTPException(
            status_code=400, 
            detail="Customer ID is required"
        )
    
    # Normalize customer_id
    customer_id = customer_id.strip().upper()
    
    # Check if customer exists
    customer_exists = customer_data[
        customer_data['Customer_ID'].astype(str).str.strip().str.upper() == customer_id
    ].shape[0] > 0
    
    if not customer_exists:
        available_customers = sorted(customer_data['Customer_ID'].unique().tolist())
        raise HTTPException(
            status_code=404, 
            detail=f"Customer {customer_id} not found. Available customers: {available_customers}"
        )
    
    try:
        # Run the LangGraph pipeline
        initial_state = {"customer_id": customer_id}
        result = pipeline.invoke(initial_state)
        
        # Validate result
        if not result or not result.get('customer_profile'):
            raise HTTPException(
                status_code=500, 
                detail="Failed to generate customer profile"
            )
        
        # Prepare response
        response = {
            "customer_id": customer_id,
            "timestamp": datetime.now().isoformat(),
            "pipeline_type": "LangGraph",
            "research_report": result.get('research_report', ''),
            "recommendations": result.get('scored_opportunities', []),
            "summary": {
                "total_recommendations": len(result.get('scored_opportunities', [])),
                "cross_sell_count": len([r for r in result.get('scored_opportunities', []) if r.get('type') == 'Cross-sell']),
                "upsell_count": len([r for r in result.get('scored_opportunities', []) if r.get('type') == 'Upsell']),
                "top_recommendation_score": max([r.get('score', 0) for r in result.get('scored_opportunities', [])]) if result.get('scored_opportunities') else 0
            }
        }
        
        # Include customer profile if requested
        if include_profile:
            response["customer_profile"] = result.get('customer_profile')
        
        return JSONResponse(response)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        print(f"Error processing request for customer {customer_id}: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Processing error: {str(e)}"
        )

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "pipeline_ready": pipeline is not None,
        "data_loaded": customer_data is not None and not customer_data.empty,
        "pipeline_type": "LangGraph",
        "available_customers": len(customer_data['Customer_ID'].unique()) if customer_data is not None else 0
    }

@app.get("/customers")
def get_customers():
    """Get list of available customers"""
    if customer_data is None or customer_data.empty:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    customers = []
    for customer_id in sorted(customer_data['Customer_ID'].unique()):
        customer_info = customer_data[customer_data['Customer_ID'] == customer_id].iloc[0]
        customers.append({
            "customer_id": customer_id,
            "company_name": customer_info.get('Customer_Name', ''),
            "industry": customer_info.get('Industry', ''),
            "priority_rating": customer_info.get('Customer_Priority_Rating', ''),
            "total_spent": float(customer_data[customer_data['Customer_ID'] == customer_id]['Total_Price(USD)'].sum())
        })
    
    return {
        "customers": customers,
        "total_count": len(customers),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/reload")
def reload_data():
    """Reload data and reinitialize LangGraph pipeline"""
    try:
        success = initialize_pipeline()
        if success:
            return {"message": "LangGraph pipeline reloaded successfully", "status": "success"}
        else:
            raise HTTPException(status_code=500, detail="Failed to reload LangGraph pipeline")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reload error: {str(e)}")