#!/usr/bin/env python3
"""
Test the B2B Sales Analyst AI API endpoints
"""

import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing B2B Sales Analyst AI API")
    print("=" * 50)
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            root_data = response.json()
            print("✅ Root endpoint works")
            print(f"   - Message: {root_data['message']}")
            print(f"   - Version: {root_data['version']}")
            print(f"   - Pipeline: {root_data['pipeline_type']}")
            print(f"   - Available customers: {root_data['available_customers']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check passed")
            print(f"   - Status: {health_data['status']}")
            print(f"   - Pipeline ready: {health_data['pipeline_ready']}")
            print(f"   - Data loaded: {health_data['data_loaded']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test customers endpoint
    try:
        response = requests.get(f"{base_url}/customers")
        if response.status_code == 200:
            customers_data = response.json()
            print("✅ Customers endpoint works")
            print(f"   - Total customers: {customers_data['total_count']}")
            print(f"   - Available customers: {[c['customer_id'] for c in customers_data['customers']]}")
            
            # Get first customer for testing
            if customers_data['customers']:
                test_customer = customers_data['customers'][0]['customer_id']
                print(f"   - Testing with customer: {test_customer}")
            else:
                print("❌ No customers available for testing")
                return False
        else:
            print(f"❌ Customers endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Customers endpoint error: {e}")
        return False
    
    # Test recommendation endpoint
    try:
        print(f"\n🔍 Testing recommendation for customer: {test_customer}")
        response = requests.get(f"{base_url}/recommendation?customer_id={test_customer}")
        if response.status_code == 200:
            rec_data = response.json()
            print("✅ Recommendation endpoint works")
            print(f"   - Customer ID: {rec_data['customer_id']}")
            print(f"   - Report length: {len(rec_data['research_report'])} chars")
            print(f"   - Total recommendations: {rec_data['summary']['total_recommendations']}")
            print(f"   - Cross-sell opportunities: {rec_data['summary']['cross_sell_count']}")
            print(f"   - Upsell opportunities: {rec_data['summary']['upsell_count']}")
            print(f"   - Top recommendation score: {rec_data['summary']['top_recommendation_score']:.2f}")
            
            # Show first recommendation
            if rec_data['recommendations']:
                first_rec = rec_data['recommendations'][0]
                print(f"   - Top recommendation: {first_rec['product']} (Score: {first_rec['score']:.2f})")
                print(f"   - Type: {first_rec['type']}")
                print(f"   - Reason: {first_rec['reason']}")
        else:
            print(f"❌ Recommendation endpoint failed: {response.status_code}")
            print(f"   - Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Recommendation endpoint error: {e}")
        return False
    
    # Test recommendation with profile
    try:
        print(f"\n📊 Testing recommendation with profile for customer: {test_customer}")
        response = requests.get(f"{base_url}/recommendation?customer_id={test_customer}&include_profile=true")
        if response.status_code == 200:
            rec_data = response.json()
            print("✅ Recommendation with profile works")
            if 'customer_profile' in rec_data:
                profile = rec_data['customer_profile']
                print(f"   - Company: {profile['company_name']}")
                print(f"   - Industry: {profile['industry']}")
                print(f"   - Annual Revenue: ${profile['annual_revenue']:,}")
                print(f"   - Total Spent: ${profile['total_spent']:,}")
                print(f"   - Purchase Frequency: {profile['purchase_frequency']}")
            else:
                print("   - No profile included in response")
        else:
            print(f"❌ Recommendation with profile failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Recommendation with profile error: {e}")
    
    # Test invalid customer
    try:
        print(f"\n🚫 Testing invalid customer ID")
        response = requests.get(f"{base_url}/recommendation?customer_id=INVALID")
        if response.status_code == 404:
            print("✅ Invalid customer handling works")
            error_data = response.json()
            print(f"   - Error: {error_data['detail']}")
        else:
            print(f"❌ Invalid customer handling failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Invalid customer test error: {e}")
    
    print("\n🎉 API testing completed successfully!")
    return True

def test_performance():
    """Test API performance"""
    base_url = "http://localhost:8000"
    
    print("\n⚡ Performance Testing")
    print("=" * 30)
    
    # Get a test customer
    try:
        response = requests.get(f"{base_url}/customers")
        if response.status_code == 200:
            customers_data = response.json()
            test_customer = customers_data['customers'][0]['customer_id']
            
            # Test response time
            start_time = time.time()
            response = requests.get(f"{base_url}/recommendation?customer_id={test_customer}")
            end_time = time.time()
            
            if response.status_code == 200:
                response_time = end_time - start_time
                print(f"✅ Recommendation response time: {response_time:.2f} seconds")
                
                if response_time < 5.0:
                    print("   - Performance: Good (< 5 seconds)")
                elif response_time < 10.0:
                    print("   - Performance: Acceptable (< 10 seconds)")
                else:
                    print("   - Performance: Slow (> 10 seconds)")
            else:
                print("❌ Performance test failed")
        else:
            print("❌ Could not get test customer for performance test")
    except Exception as e:
        print(f"❌ Performance test error: {e}")

if __name__ == "__main__":
    success = test_api()
    if success:
        test_performance()
    else:
        print("\n❌ API testing failed. Please check if the server is running.")
        print("Start the server with: uvicorn main:app --reload --host 0.0.0.0 --port 8000") 