from langgraph.graph import StateGraph, END
from agents import (
    customer_context_agent,
    purchase_pattern_agent,
    product_affinity_agent,
    opportunity_scoring_agent,
    recommendation_report_agent
)
from typing import Dict, TypedDict, Annotated
import pandas as pd

class AgentState(TypedDict):
    customer_id: str
    customer_profile: Dict
    pattern_analysis: Dict
    affinity_analysis: Dict
    scored_opportunities: list
    research_report: str

def build_pipeline(customer_data: pd.DataFrame):
    workflow = StateGraph(AgentState)

    # Step 1: Customer Context
    def context_node(state: AgentState) -> AgentState:
        profile = customer_context_agent(state['customer_id'], customer_data)
        if not profile:
            raise ValueError(f"Customer {state['customer_id']} not found")
        return {**state, 'customer_profile': profile}

    # Step 2: Purchase Pattern
    def pattern_node(state: AgentState) -> AgentState:
        pattern = purchase_pattern_agent(state['customer_profile'], customer_data)
        return {**state, 'pattern_analysis': pattern}

    # Step 3: Product Affinity
    def affinity_node(state: AgentState) -> AgentState:
        affinity = product_affinity_agent(state['customer_profile'], customer_data)
        return {**state, 'affinity_analysis': affinity}

    # Step 4: Opportunity Scoring
    def scoring_node(state: AgentState) -> AgentState:
        scored = opportunity_scoring_agent(
            state['customer_profile'],
            state['pattern_analysis'],
            state['affinity_analysis']
        )
        return {**state, 'scored_opportunities': scored}

    # Step 5: Recommendation Report
    def report_node(state: AgentState) -> AgentState:
        report = recommendation_report_agent(
            state['customer_profile'],
            state['pattern_analysis'],
            state['affinity_analysis'],
            state['scored_opportunities']
        )
        return {**state, 'research_report': report}

    # Add nodes to graph
    workflow.add_node("context", context_node)
    workflow.add_node("pattern", pattern_node)
    workflow.add_node("affinity", affinity_node)
    workflow.add_node("scoring", scoring_node)
    workflow.add_node("report", report_node)

    # Define edges
    workflow.add_edge("context", "pattern")
    workflow.add_edge("pattern", "affinity")
    workflow.add_edge("affinity", "scoring")
    workflow.add_edge("scoring", "report")
    workflow.add_edge("report", END)

    # Set entry point
    workflow.set_entry_point("context")

    return workflow.compile() 