# api/routers/chat_router.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.dependencies import verify_vip

# Import the LangChain Agent Engine
from services.ai_generator.handler import invoke_sleep_coach

router = APIRouter(tags=["2. VIP AI Agent"])

class ChatRequest(BaseModel):
    user_id: str
    query: str

@router.post("/")
async def chat_with_agent(req: ChatRequest, is_vip: bool = Depends(verify_vip)):
    """
    AI Chat endpoint. Protected by the verify_vip dependency.
    Invokes the LangChain Agentic Workflow to generate actionable insights.
    """
    print(f"[Gateway] Routing query from VIP user {req.user_id} to LangChain Agent...")
    
    # Execute the LLM chain (Blocking call for MVP, can be async later)
    agent_reply = invoke_sleep_coach(user_id=req.user_id, query=req.query)
    
    return {
        "status": "success", 
        "agent_reply": agent_reply
    }