#!/usr/bin/env python3
"""
Test the API endpoints
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing B2B Sales Analyst AI API")
    print("=" * 40)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check passed")
            print(f"   - Status: {health_data['status']}")
            print(f"   - Pipeline: {health_data['pipeline_type']}")
            print(f"   - Data loaded: {health_data['data_loaded']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            root_data = response.json()
            print("✅ Root endpoint works")
            print(f"   - Message: {root_data['message']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test recommendation endpoint
    try:
        response = requests.get(f"{base_url}/recommendation?customer_id=C001")
        if response.status_code == 200:
            rec_data = response.json()
            print("✅ Recommendation endpoint works")
            print(f"   - Report length: {len(rec_data['research_report'])} chars")
            print(f"   - Recommendations: {len(rec_data['recommendations'])}")
            
            # Show first recommendation
            if rec_data['recommendations']:
                first_rec = rec_data['recommendations'][0]
                print(f"   - Top recommendation: {first_rec['product']} (Score: {first_rec['score']:.2f})")
        else:
            print(f"❌ Recommendation endpoint failed: {response.status_code}")
            print(f"   - Response: {response.text}")
    except Exception as e:
        print(f"❌ Recommendation endpoint error: {e}")
    
    print("\n🎉 API testing completed!")
    return True

if __name__ == "__main__":
    test_api() 