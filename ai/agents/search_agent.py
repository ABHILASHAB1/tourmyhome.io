import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated, TypedDict

from ai.vector_store import search_similar

# 1. Define the Graph State
class AgentState(TypedDict):
    # 'messages' holds the conversational history
    messages: Annotated[list, add_messages]

# 2. Define the Agent Node Logic
def call_model(state: AgentState):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        # Fallback if no API key is provided
        return {"messages": ["System: Please add GEMINI_API_KEY to your .env file."]}
        
    messages = state["messages"]
    
    # Get the latest user query from the message history
    user_query = messages[-1].content
    
    # Semantic Search RAG
    print(f"Agent executing semantic search for: {user_query}")
    results = search_similar(user_query, limit=3)
    
    context = ""
    for hit in results:
        payload = hit.payload
        context += f"- {payload['title']} (Price: {payload['price_sar']} SAR)\n"

    if not context:
        context = "No relevant listings found in the database."
        
    # Inject Context via System Prompt
    system_prompt = SystemMessage(content=f"""
    You are 'SouqAI', the elite conversational search assistant for SouqAI KSA.
    Your goal is to help users find exactly what they are looking for based ONLY on the provided database context.
    
    <rules>
    1. NEVER guess or invent inventory or prices.
    2. If the user refers to something discussed earlier, answer using your chat history.
    3. Keep responses concise and friendly.
    </rules>
    
    <database_context>
    {context}
    </database_context>
    """)
    
    # We combine the new system prompt + the entire conversation history
    # so the LLM remembers previous turns AND has fresh DB context.
    full_prompt = [system_prompt] + messages
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=api_key)
    response = llm.invoke(full_prompt)
    
    # Return the new message to append to the state
    return {"messages": [response]}

# 3. Build and Compile the Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# Initialize a simple in-memory checkpointer to save conversation states across API calls
memory = MemorySaver()

# Compile the graph
agent_executor = workflow.compile(checkpointer=memory)
