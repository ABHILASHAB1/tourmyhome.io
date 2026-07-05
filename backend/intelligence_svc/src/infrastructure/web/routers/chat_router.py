from fastapi import APIRouter, Depends, HTTPException, status
from src.infrastructure.web.schemas import ChatRequest, ChatResponse
from src.application.use_cases.process_chat import ProcessChatUseCase
from src.infrastructure.database.redis_repo_impl import RedisChatRepository
import uuid

# Mock dependency for getting Redis client
def get_redis():
    pass

router = APIRouter(prefix="/api/v1/search", tags=["search"])

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest, 
    redis_client = Depends(get_redis)
):
    try:
        repo = RedisChatRepository(redis_client)
        use_case = ProcessChatUseCase(repo)
        
        session_id = request.session_id
        if session_id == "new":
            session_id = str(uuid.uuid4())
            
        chat_session = await use_case.execute(
            session_id=session_id,
            user_message=request.message
        )
        
        # Extract the latest assistant message
        ai_msg = "Error generating response"
        if chat_session.messages and chat_session.messages[-1]["role"] == "assistant":
            ai_msg = chat_session.messages[-1]["content"]

        return ChatResponse(
            session_id=chat_session.id,
            ai_response_text=ai_msg,
            suggested_listings=[] # Populated by Qdrant in real implementation
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
