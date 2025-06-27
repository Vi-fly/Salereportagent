import streamlit as st
import pandas as pd
import json
import os

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

st.set_page_config(page_title="B2B Sales Analyst AI", page_icon="🤖", layout="wide")
st.title("🤖 B2B Sales Analyst AI (Streamlit)")
st.markdown("""
This app analyzes customer data and generates cross-sell/upsell recommendations and a research report.
""")

# Load data with error handling
@st.cache_data
def load_data():
    try:
        from data_loader import load_customer_data_csv
        data = load_customer_data_csv('customer_data.csv')
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load unique customer IDs only
@st.cache_data
def load_customer_ids():
    try:
        from data_loader import load_customer_data_csv
        data = load_customer_data_csv('customer_data.csv')
        return sorted(data['Customer_ID'].unique().tolist())
    except Exception as e:
        st.error(f"Error loading customer IDs: {e}")
        return []

# Load specific customer data
@st.cache_data
def load_customer_data(customer_id):
    try:
        from data_loader import load_customer_data_csv
        data = load_customer_data_csv('customer_data.csv')
        customer_data = data[data['Customer_ID'] == customer_id]
        return customer_data
    except Exception as e:
        st.error(f"Error loading customer data: {e}")
        return None

# Load pipeline with error handling
@st.cache_resource
def load_pipeline():
    try:
        from pipeline import build_pipeline
        customer_data = load_data()
        if customer_data is not None:
            pipeline = build_pipeline(customer_data)
            return pipeline, True  # LangGraph
    except Exception as e:
        st.warning(f"LangGraph failed, using simple pipeline: {e}")
        try:
            from simple_pipeline import SimplePipeline
            customer_data = load_data()
            if customer_data is not None:
                pipeline = SimplePipeline(customer_data)
                return pipeline, False  # Simple
        except Exception as e2:
            st.error(f"Both pipelines failed: {e2}")
            return None, None
    return None, None

# Load customer IDs and pipeline
customer_ids = load_customer_ids()
pipeline, use_langgraph = load_pipeline()

if not customer_ids:
    st.error("Failed to load customer IDs. Please check if customer_data.csv exists.")
    st.stop()

if pipeline is None:
    st.error("Failed to initialize pipeline.")
    st.stop()

# Sidebar
st.sidebar.header("Configuration")
st.sidebar.write(f"Pipeline type: {'LangGraph' if use_langgraph else 'Simple'}")

# Get unique customer IDs
selected_customer = st.sidebar.selectbox("Select Customer ID", customer_ids)

# Load customer data only when selected
customer_data = None
customer_info = None
if selected_customer:
    customer_data = load_customer_data(selected_customer)
    if customer_data is not None and not customer_data.empty:
        customer_info = customer_data.iloc[0]

# Show customer info
if customer_info is not None:
    st.sidebar.markdown(f"**Selected Customer:** {customer_info['Customer_Name']}")
    st.sidebar.markdown(f"**Industry:** {customer_info['Industry']}")

if st.sidebar.button("🚀 Run Analysis", type="primary"):
    if customer_data is None:
        st.error("Please select a customer first.")
    else:
        with st.spinner("Running AI analysis..."):
            try:
                if use_langgraph:
                    result = pipeline.invoke({"customer_id": selected_customer})
                else:
                    result = pipeline.run(selected_customer)
                
                # Store results in session state
                st.session_state.analysis_results = result
                st.success("✅ Analysis complete!")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")
                import traceback
                st.code(traceback.format_exc())
                st.stop()

# Display results if available
if st.session_state.analysis_results and customer_data is not None:
    result = st.session_state.analysis_results
    
    # Tabs for output
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Customer Profile", "🎯 Recommendations", "📝 Research Report", "📈 Data Overview"])
    
    with tab1:
        st.subheader("Customer Profile")
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Annual Revenue", f"${result['customer_profile']['annual_revenue']:,}")
        with col2:
            st.metric("Total Spent", f"${result['customer_profile']['total_spent']:,}")
        with col3:
            st.metric("Purchase Frequency", result['customer_profile']['purchase_frequency'])
        with col4:
            st.metric("Priority Rating", result['customer_profile']['priority_rating'])
        
        # Detailed profile
        st.subheader("Detailed Information")
        profile = result['customer_profile']
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Company:** {profile['company_name']}")
            st.write(f"**Industry:** {profile['industry']}")
            st.write(f"**Location:** {profile['location']}")
            st.write(f"**Employees:** {profile['employees']:,}")
        
        with col2:
            st.write(f"**Account Type:** {profile['account_type']}")
            st.write(f"**Current Products:** {profile['current_products']}")
            st.write(f"**Product Usage:** {profile['product_usage']}%")
            st.write(f"**Competitors:** {profile['competitors']}")
        
        # Products purchased
        st.subheader("Products Purchased")
        products = profile['products_purchased']
        if products:
            for product in products:
                st.write(f"• {product}")
        else:
            st.info("No products found.")
    
    with tab2:
        st.subheader("AI-Generated Recommendations")
        
        recs = result['scored_opportunities']
        if recs:
            # Summary metrics
            cross_sell_count = len([r for r in recs if r['type'] == 'Cross-sell'])
            upsell_count = len([r for r in recs if r['type'] == 'Upsell'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Opportunities", len(recs))
            with col2:
                st.metric("Cross-sell", cross_sell_count)
            with col3:
                st.metric("Upsell", upsell_count)
            
            # Display recommendations
            for i, rec in enumerate(recs):
                # Color code based on score
                if rec['score'] >= 0.7:
                    color = "🟢"
                elif rec['score'] >= 0.4:
                    color = "🟡"
                else:
                    color = "🔴"
                
                st.markdown(f"### {color} {rec['product']}")
                st.write(f"**Type:** {rec['type']} | **Score:** {rec['score']:.2f}")
                st.write(f"**Reason:** {rec['reason']}")
                st.markdown("---")
            
            # Download button
            st.download_button(
                label="📥 Download Recommendations as JSON",
                data=json.dumps(recs, indent=2),
                file_name=f"recommendations_{selected_customer}.json",
                mime="application/json"
            )
        else:
            st.info("No recommendations found for this customer.")
    
    with tab3:
        st.subheader("Research Report")
        st.markdown(result['research_report'])
        
        # Download full report
        full_report = {
            "research_report": result['research_report'],
            "recommendations": result['scored_opportunities']
        }
        st.download_button(
            label="📥 Download Full Report as JSON",
            data=json.dumps(full_report, indent=2),
            file_name=f"full_report_{selected_customer}.json",
            mime="application/json"
        )
    
    with tab4:
        st.subheader("Data Overview")
        
        # Customer's purchase history
        if customer_data is not None and not customer_data.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Purchase History")
                # Convert dates
                customer_data['Purchase_Date'] = pd.to_datetime(customer_data['Purchase_Date'])
                customer_data = customer_data.sort_values('Purchase_Date')
                
                # Show recent purchases
                st.write("**Recent Purchases:**")
                for _, row in customer_data.head(5).iterrows():
                    try:
                        price = float(row['Total_Price(USD)'])
                        st.write(f"• {row['Product']} - ${price:,} ({row['Purchase_Date'].strftime('%Y-%m-%d')})")
                    except (ValueError, TypeError):
                        st.write(f"• {row['Product']} - ${row['Total_Price(USD)']} ({row['Purchase_Date'].strftime('%Y-%m-%d')})")
            
            with col2:
                st.subheader("Industry Comparison")
                if customer_info is not None:
                    # Load industry data only when needed
                    @st.cache_data
                    def load_industry_data(industry):
                        from data_loader import load_customer_data_csv
                        data = load_customer_data_csv('customer_data.csv')
                        return data[data['Industry'] == industry]
                    
                    industry_data = load_industry_data(customer_info['Industry'])
                    if not industry_data.empty:
                        top_products = industry_data['Product'].value_counts().head(5)
                        st.write("**Top Products in Industry:**")
                        for product, count in top_products.items():
                            st.write(f"• {product} ({count} purchases)")
                    else:
                        st.info("No industry data available.")
        else:
            st.info("No customer data available.")

else:
    st.info("👆 Select a customer and click 'Run Analysis' to get started!") 