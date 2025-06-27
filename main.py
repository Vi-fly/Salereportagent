from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from data_loader import load_customer_data_csv
import os
import traceback

app = FastAPI(title="B2B Sales Analyst AI API")

# Try to use LangGraph first, fallback to simple pipeline
try:
    from pipeline import build_pipeline
    customer_data = load_customer_data_csv(os.getenv('CSV_PATH', 'customer_data.csv'))
    pipeline = build_pipeline(customer_data)
    use_langgraph = True
    print("✅ LangGraph pipeline built successfully")
except Exception as e:
    print(f"⚠️ LangGraph failed, using simple pipeline: {e}")
    try:
        from simple_pipeline import SimplePipeline
        customer_data = load_customer_data_csv(os.getenv('CSV_PATH', 'customer_data.csv'))
        pipeline = SimplePipeline(customer_data)
        use_langgraph = False
        print("✅ Simple pipeline initialized")
    except Exception as e2:
        print(f"❌ Both pipelines failed: {e2}")
        customer_data = None
        pipeline = None
        use_langgraph = None

@app.get("/")
def read_root():
    return {
        "message": "B2B Sales Analyst AI API", 
        "status": "running",
        "pipeline_type": "LangGraph" if use_langgraph else "Simple" if use_langgraph is False else "None"
    }

@app.get("/recommendation")
def get_recommendation(customer_id: str):
    if not pipeline or customer_data is None or customer_data.empty:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    try:
        # Run the pipeline
        if use_langgraph:
            initial_state = {"customer_id": customer_id}
            result = pipeline.invoke(initial_state)
        else:
            result = pipeline.run(customer_id)
        
        if not result.get('customer_profile'):
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return JSONResponse({
            "research_report": result['research_report'],
            "recommendations": result['scored_opportunities']
        })
    except Exception as e:
        print(f"Error processing request: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "pipeline_ready": pipeline is not None,
        "data_loaded": customer_data is not None and not customer_data.empty,
        "pipeline_type": "LangGraph" if use_langgraph else "Simple" if use_langgraph is False else "None"
    }