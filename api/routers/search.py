from fastapi import APIRouter
import uuid
import schemas.search as schemas
from ai.agents.search_agent import agent_executor

router = APIRouter(
    prefix="/api/v1/search",
    tags=["ai_search"],
)

@router.post("/chat", response_model=schemas.ChatResponse)
def chat_with_ai(request: schemas.ChatRequest):
    """
    Interact with the SouqAI LangGraph Agent.
    Pass a `session_id` in the request to maintain conversation history.
    """
    # 1. Generate a new session ID if none is provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # 2. Configure the LangGraph thread to load/save memory for this specific session
    config = {"configurable": {"thread_id": session_id}}
    
    # 3. Invoke the graph with the user's message
    result = agent_executor.invoke(
        {"messages": [("user", request.query)]},
        config=config
    )
    
    # 4. Extract the final AI response from the state messages
    final_message = result["messages"][-1].content
    
    return schemas.ChatResponse(
        response=final_message,
        session_id=session_id
    )
