from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from src.application.graph.state import AgentState
from src.core.prompts import INTENT_SYSTEM_PROMPT, EXTRACT_SYSTEM_PROMPT, GENERATION_SYSTEM_PROMPT
import json

# Initialize the LLM (requires OPENAI_API_KEY environment variable)
llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

def analyze_intent_node(state: AgentState) -> dict:
    """Analyzes if the user wants to search or chat."""
    last_msg = state["messages"][-1]["content"]
    
    messages = [
        SystemMessage(content=INTENT_SYSTEM_PROMPT),
        HumanMessage(content=last_msg)
    ]
    response = llm.invoke(messages)
    
    intent = response.content.strip().lower()
    if intent not in ["search", "chat"]:
        intent = "chat" # Default fallback
        
    return {"intent": intent}

def extract_filters_node(state: AgentState) -> dict:
    """Extracts JSON filters from the query."""
    last_msg = state["messages"][-1]["content"]
    
    messages = [
        SystemMessage(content=EXTRACT_SYSTEM_PROMPT),
        HumanMessage(content=last_msg)
    ]
    # In production, we'd use function calling / structured output here.
    # For now, parsing raw JSON block if present.
    response = llm.invoke(messages)
    
    try:
        filters = json.loads(response.content)
    except:
        filters = {"keywords": last_msg}
        
    return {"filters": filters}

def retrieve_listings_node(state: AgentState) -> dict:
    """Mocks fetching vectors from Qdrant based on filters."""
    # TODO: Connect to QdrantClient
    mock_listings = [
        {"id": "123", "title": "Modern Apartment in Riyadh", "price_sar": 55000},
        {"id": "456", "title": "Luxury Villa in Jeddah", "price_sar": 120000}
    ]
    return {"retrieved_listings": mock_listings}

def generate_response_node(state: AgentState) -> dict:
    """Synthesizes the final response to the user."""
    context_str = json.dumps(state.get("retrieved_listings", []), indent=2)
    sys_prompt = GENERATION_SYSTEM_PROMPT.format(retrieved_context=context_str)
    
    # We pass the conversation history
    lc_messages = [SystemMessage(content=sys_prompt)]
    for msg in state["messages"]:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        # ignoring assistant history for this simple boilerplate to save tokens
        
    response = llm.invoke(lc_messages)
    
    return {"final_response": response.content}
