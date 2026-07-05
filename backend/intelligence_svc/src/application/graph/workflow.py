from langgraph.graph import StateGraph, END
from src.application.graph.state import AgentState
from src.application.graph.nodes import (
    analyze_intent_node,
    extract_filters_node,
    retrieve_listings_node,
    generate_response_node
)

def build_graph() -> StateGraph:
    """Builds and compiles the LangGraph state machine."""
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("analyze_intent", analyze_intent_node)
    workflow.add_node("extract_filters", extract_filters_node)
    workflow.add_node("retrieve_listings", retrieve_listings_node)
    workflow.add_node("generate_response", generate_response_node)

    # Set Entry Point
    workflow.set_entry_point("analyze_intent")

    # Define Conditional Edges
    def route_intent(state: AgentState) -> str:
        if state.get("intent") == "search":
            return "extract_filters"
        return "generate_response" # skip retrieval if just chatting

    workflow.add_conditional_edges(
        "analyze_intent",
        route_intent,
        {
            "extract_filters": "extract_filters",
            "generate_response": "generate_response"
        }
    )

    # Standard Edges
    workflow.add_edge("extract_filters", "retrieve_listings")
    workflow.add_edge("retrieve_listings", "generate_response")
    workflow.add_edge("generate_response", END)

    # Compile
    return workflow.compile()
