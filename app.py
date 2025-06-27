import streamlit as st
import pandas as pd
from pipeline import build_pipeline
import json

st.set_page_config(
    page_title="B2B Sales Analyst AI",
    page_icon="📊",
    layout="wide"
)

st.title("🤖 B2B Sales Analyst AI")
st.markdown("Analyze customer data for cross-sell and upsell opportunities")

# File upload
uploaded_file = st.file_uploader(
    "Upload your customer data CSV file",
    type=['csv'],
    help="Upload a CSV file with columns: customer_id, product_name, purchase_date, amount, category"
)

if uploaded_file is not None:
    try:
        # Load data
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Data loaded successfully! Found {len(df)} records")
        
        # Show data preview
        with st.expander("📋 Data Preview"):
            st.dataframe(df.head())
            st.write(f"**Columns:** {list(df.columns)}")
        
        # Customer selection
        if 'customer_id' in df.columns:
            customer_ids = df['customer_id'].unique()
            selected_customer = st.selectbox(
                "Select a customer to analyze:",
                customer_ids,
                help="Choose a customer ID to generate personalized recommendations"
            )
            
            if st.button("🚀 Generate Analysis", type="primary"):
                with st.spinner("Analyzing customer data..."):
                    try:
                        # Build and run pipeline
                        pipeline = build_pipeline(df)
                        
                        # Initialize state
                        initial_state = {
                            'customer_id': selected_customer,
                            'customer_profile': {},
                            'pattern_analysis': {},
                            'affinity_analysis': {},
                            'scored_opportunities': [],
                            'research_report': ''
                        }
                        
                        # Run pipeline
                        result = pipeline.invoke(initial_state)
                        
                        # Display results
                        st.success("✅ Analysis complete!")
                        
                        # Customer Profile
                        with st.expander("👤 Customer Profile", expanded=True):
                            profile = result['customer_profile']
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Purchases", profile.get('total_purchases', 0))
                            with col2:
                                st.metric("Total Spent", f"${profile.get('total_spent', 0):,.2f}")
                            with col3:
                                st.metric("Avg Order Value", f"${profile.get('avg_order_value', 0):,.2f}")
                            
                            st.write("**Purchase History:**")
                            st.write(profile.get('purchase_history', 'No data'))
                        
                        # Pattern Analysis
                        with st.expander("📈 Purchase Patterns"):
                            patterns = result['pattern_analysis']
                            st.write("**Seasonal Trends:**")
                            st.write(patterns.get('seasonal_trends', 'No patterns detected'))
                            
                            st.write("**Purchase Frequency:**")
                            st.write(patterns.get('frequency_analysis', 'No data'))
                        
                        # Product Affinity
                        with st.expander("🔗 Product Affinity"):
                            affinity = result['affinity_analysis']
                            st.write("**Top Categories:**")
                            st.write(affinity.get('top_categories', 'No data'))
                            
                            st.write("**Product Relationships:**")
                            st.write(affinity.get('product_relationships', 'No data'))
                        
                        # Scored Opportunities
                        with st.expander("🎯 Scored Opportunities"):
                            opportunities = result['scored_opportunities']
                            if opportunities:
                                for i, opp in enumerate(opportunities, 1):
                                    st.write(f"**{i}. {opp['product']}**")
                                    st.write(f"   Score: {opp['score']}/10")
                                    st.write(f"   Reasoning: {opp['reasoning']}")
                                    st.write("---")
                            else:
                                st.write("No opportunities identified")
                        
                        # Research Report
                        with st.expander("📋 Research Report", expanded=True):
                            st.markdown(result['research_report'])
                        
                        # Download results
                        results_data = {
                            'customer_id': selected_customer,
                            'profile': result['customer_profile'],
                            'patterns': result['pattern_analysis'],
                            'affinity': result['affinity_analysis'],
                            'opportunities': result['scored_opportunities'],
                            'report': result['research_report']
                        }
                        
                        st.download_button(
                            label="📥 Download Analysis Results",
                            data=json.dumps(results_data, indent=2),
                            file_name=f"analysis_{selected_customer}.json",
                            mime="application/json"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        st.exception(e)
        else:
            st.error("❌ CSV file must contain a 'customer_id' column")
            
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        st.write("Please ensure your CSV file has the correct format with columns: customer_id, product_name, purchase_date, amount, category")

else:
    st.info("📁 Please upload a CSV file to begin analysis")
    
    # Sample data format
    st.markdown("### 📋 Expected CSV Format")
    sample_data = {
        'customer_id': ['CUST001', 'CUST001', 'CUST002'],
        'product_name': ['Product A', 'Product B', 'Product C'],
        'purchase_date': ['2024-01-15', '2024-02-20', '2024-01-10'],
        'amount': [1000.00, 2500.00, 1500.00],
        'category': ['Software', 'Hardware', 'Services']
    }
    st.dataframe(pd.DataFrame(sample_data)) 