from src.core.entities.chat_session import ChatSession
from src.application.interfaces.chat_repository import ChatRepository
from src.application.graph.workflow import build_graph

class ProcessChatUseCase:
    """Use case for processing a new chat message via LangGraph state machine."""
    
    def __init__(self, repo: ChatRepository):
        self.repo = repo
        self.graph = build_graph()
        
    async def execute(self, session_id: str, user_message: str) -> ChatSession:
        # Load existing session or create new
        session = await self.repo.get_by_id(session_id)
        if not session:
            session = ChatSession(id=session_id)
            
        session.add_message("user", user_message)
        
        # Invoke LangGraph
        initial_state = {"messages": session.messages}
        
        # In production this should be awaited if graph is async, but LangGraph invoke is sync
        # unless using ainvoke()
        final_state = self.graph.invoke(initial_state)
        
        # Update session with outputs
        session.user_intent = final_state.get("intent", "unknown")
        session.extracted_filters = final_state.get("filters", {})
        session.add_message("assistant", final_state.get("final_response", "Error generating response."))
        
        # Save updated state
        await self.repo.save(session)
        
        return session
