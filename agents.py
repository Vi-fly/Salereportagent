import pandas as pd
import json
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# --- Customer Context Agent ---
def customer_context_agent(customer_id, customer_data):
    # Ensure customer_id is string and normalize
    customer_id = str(customer_id).strip().upper()
    
    customer_records = customer_data[customer_data['Customer_ID'].astype(str).str.strip().str.upper() == customer_id]
    if customer_records.empty:
        return None
    
    customer_info = customer_records.iloc[0]
    
    # Ensure numeric columns are properly handled
    try:
        total_spent = customer_records['Total_Price(USD)'].astype(float).sum()
        avg_order_value = customer_records['Total_Price(USD)'].astype(float).mean()
    except:
        total_spent = 0
        avg_order_value = 0
    
    purchase_frequency = len(customer_records)
    products_purchased = customer_records['Product'].unique().tolist()
    
    # Handle potential data issues
    try:
        annual_revenue = float(customer_info['Annual_Revenue(USD)'])
    except:
        annual_revenue = 0
    
    try:
        employees = int(customer_info['Number_of_Employees'])
    except:
        employees = 0
    
    try:
        product_usage = float(customer_info['Product_Usage(%)'])
    except:
        product_usage = 0
    
    try:
        opportunity_amount = float(customer_info['Opportunity_Amount(USD)'])
    except:
        opportunity_amount = 0
    
    profile = {
        "customer_id": customer_id,
        "company_name": str(customer_info['Customer_Name']),
        "industry": str(customer_info['Industry']),
        "annual_revenue": annual_revenue,
        "employees": employees,
        "priority_rating": str(customer_info['Customer_Priority_Rating']),
        "account_type": str(customer_info['Account_Type']),
        "location": str(customer_info['Location']),
        "current_products": str(customer_info['Current_Products']),
        "product_usage": product_usage,
        "total_spent": total_spent,
        "avg_order_value": avg_order_value,
        "purchase_frequency": purchase_frequency,
        "products_purchased": products_purchased,
        "last_activity": str(customer_info['Last_Activity_Date']),
        "opportunity_stage": str(customer_info['Opportunity_Stage']),
        "opportunity_amount": opportunity_amount,
        "competitors": str(customer_info['Competitors'])
    }
    return profile

# --- Purchase Pattern Analysis Agent ---
def purchase_pattern_agent(customer_profile, all_customer_data):
    customer_products = customer_profile['products_purchased']
    customer_id = customer_profile['customer_id'].strip().upper()
    similar_customers = all_customer_data[
        (all_customer_data['Industry'] == customer_profile['industry']) &
        (all_customer_data['Customer_ID'].astype(str).str.strip().str.upper() != customer_id)
    ]
    all_products = similar_customers['Product'].value_counts()
    frequent_products = all_products.head(10).index.tolist()
    missing_products = [p for p in frequent_products if p not in customer_products]
    customer_product_frequency = {
        product: len(all_customer_data[(all_customer_data['Customer_ID'].astype(str).str.strip().str.upper() == customer_id) & (all_customer_data['Product'] == product)])
        for product in customer_products
    }
    return {
        "frequent_products_industry": frequent_products,
        "missing_opportunities": missing_products,
        "customer_product_frequency": customer_product_frequency,
        "total_industry_customers": len(similar_customers['Customer_ID'].unique())
    }

# --- Product Affinity Agent ---
def product_affinity_agent(customer_profile, all_customer_data):
    customer_products = customer_profile['products_purchased']
    customer_id = customer_profile['customer_id'].strip().upper()
    similar_purchases = all_customer_data[all_customer_data['Product'].isin(customer_products)]
    related_customers = similar_purchases['Customer_ID'].unique()
    product_affinities = {}
    for product in customer_products:
        product_customers = all_customer_data[all_customer_data['Product'] == product]['Customer_ID'].unique()
        co_purchased = all_customer_data[all_customer_data['Customer_ID'].isin(product_customers)]['Product'].value_counts()
        co_purchased = co_purchased.drop(customer_products, errors='ignore')
        product_affinities[product] = co_purchased.head(5).to_dict()
    all_co_purchased = all_customer_data[all_customer_data['Customer_ID'].isin(related_customers)]['Product'].value_counts()
    recommendations = all_co_purchased.drop(customer_products, errors='ignore').head(10)
    return {
        "product_affinities": product_affinities,
        "top_recommendations": recommendations.to_dict(),
        "related_customer_count": len(related_customers)
    }

# --- Opportunity Scoring Agent ---
def opportunity_scoring_agent(customer_profile, pattern_analysis, affinity_analysis):
    opportunities = []
    for product in pattern_analysis['missing_opportunities']:
        score = 0.0
        reason = []
        if product in pattern_analysis['frequent_products_industry']:
            score += 0.3
            reason.append("Frequently purchased in industry")
        if product in affinity_analysis['top_recommendations']:
            score += 0.2
            reason.append("High co-purchase affinity")
        if customer_profile['priority_rating'] == 'High':
            score += 0.2
            reason.append("High priority customer")
        if customer_profile['annual_revenue'] > 100000000:
            score += 0.15
            reason.append("High revenue potential")
        if customer_profile['purchase_frequency'] > 5:
            score += 0.15
            reason.append("Frequent purchaser")
        opportunities.append({
            "product": product,
            "type": "Cross-sell",
            "score": min(score, 1.0),
            "reason": "; ".join(reason)
        })
    for product in customer_profile['products_purchased']:
        current_frequency = pattern_analysis['customer_product_frequency'].get(product, 0)
        if current_frequency > 0:
            score = 0.0
            reason = []
            if customer_profile['product_usage'] < 80:
                score += 0.3
                reason.append("Low product usage indicates expansion opportunity")
            if current_frequency < 3:
                score += 0.2
                reason.append("Low purchase frequency suggests upsell potential")
            if customer_profile['priority_rating'] == 'High':
                score += 0.2
                reason.append("High priority customer")
            if customer_profile['annual_revenue'] > 100000000:
                score += 0.15
                reason.append("High revenue potential")
            if customer_profile['opportunity_stage'] in ['Prospecting', 'Qualification']:
                score += 0.15
                reason.append("Active opportunity stage")
            if score > 0.3:
                opportunities.append({
                    "product": f"{product} (Expansion)",
                    "type": "Upsell",
                    "score": min(score, 1.0),
                    "reason": "; ".join(reason)
                })
    opportunities.sort(key=lambda x: x['score'], reverse=True)
    return opportunities

# --- Recommendation Report Agent ---
def recommendation_report_agent(customer_profile, pattern_analysis, affinity_analysis, scored_opportunities):
    # Ensure products_purchased contains only strings
    products_purchased_str = [str(product) for product in customer_profile['products_purchased']]
    
    prompt = f"""
    As a B2B sales analyst, generate a comprehensive research report for {customer_profile['company_name']}.
    Customer Profile:
    - Company: {customer_profile['company_name']}
    - Industry: {customer_profile['industry']}
    - Annual Revenue: ${customer_profile['annual_revenue']:,}
    - Employees: {customer_profile['employees']}
    - Priority Rating: {customer_profile['priority_rating']}
    - Total Spent: ${customer_profile['total_spent']:,}
    - Purchase Frequency: {customer_profile['purchase_frequency']}
    - Current Products: {customer_profile['current_products']}
    - Products Purchased: {', '.join(products_purchased_str)}
    Analysis Results:
    - Missing Opportunities: {pattern_analysis['missing_opportunities']}
    - Top Recommendations: {list(affinity_analysis['top_recommendations'].keys())[:5]}
    - Scored Opportunities: {len(scored_opportunities)} opportunities identified
    Generate a professional research report with:
    1. Title
    2. Introduction
    3. Customer Overview
    4. Data Analysis
    5. Recommendations
    6. Conclusion
    Make it business-focused and actionable.
    """
    
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a senior B2B sales analyst with expertise in customer analysis and opportunity identification."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        report = response.choices[0].message.content
    except Exception as e:
        report = f"Research report could not be generated: {e}"
    return report