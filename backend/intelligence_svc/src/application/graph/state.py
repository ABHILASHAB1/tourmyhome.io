from typing import TypedDict, Annotated, List, Dict
import operator

class AgentState(TypedDict):
    """
    The state of the LangGraph state machine.
    """
    messages: Annotated[List[Dict[str, str]], operator.add]
    intent: str
    filters: Dict[str, str]
    retrieved_listings: List[Dict[str, str]]
    final_response: str
