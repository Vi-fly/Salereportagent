"""
Simple pipeline implementation without LangGraph for compatibility
"""
from agents import (
    customer_context_agent,
    purchase_pattern_agent,
    product_affinity_agent,
    opportunity_scoring_agent,
    recommendation_report_agent
)
from typing import Dict
import pandas as pd

class SimplePipeline:
    def __init__(self, customer_data: pd.DataFrame):
        self.customer_data = customer_data
    
    def run(self, customer_id: str) -> Dict:
        """Run the complete pipeline for a customer"""
        
        # Step 1: Customer Context
        customer_profile = customer_context_agent(customer_id, self.customer_data)
        if not customer_profile:
            raise ValueError(f"Customer {customer_id} not found")
        
        # Step 2: Purchase Pattern Analysis
        pattern_analysis = purchase_pattern_agent(customer_profile, self.customer_data)
        
        # Step 3: Product Affinity Analysis
        affinity_analysis = product_affinity_agent(customer_profile, self.customer_data)
        
        # Step 4: Opportunity Scoring
        scored_opportunities = opportunity_scoring_agent(
            customer_profile, pattern_analysis, affinity_analysis
        )
        
        # Step 5: Recommendation Report
        research_report = recommendation_report_agent(
            customer_profile, pattern_analysis, affinity_analysis, scored_opportunities
        )
        
        return {
            'customer_id': customer_id,
            'customer_profile': customer_profile,
            'pattern_analysis': pattern_analysis,
            'affinity_analysis': affinity_analysis,
            'scored_opportunities': scored_opportunities,
            'research_report': research_report
        } 