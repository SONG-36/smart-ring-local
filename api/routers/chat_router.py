from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.dependencies import verify_vip

router = APIRouter(prefix="/api/chat", tags=["2. VIP AI Agent"])

class ChatRequest(BaseModel):
    user_id: str
    query: str

# Core logic: is_vip: bool = Depends(verify_vip) acts as the sentinel.
# FastAPI executes verify_vip first. If it raises an exception, execution stops here.
@router.post("/")
async def chat_with_agent(req: ChatRequest, is_vip: bool = Depends(verify_vip)):
    """
    AI Chat endpoint. Protected by the verify_vip dependency.
    Only accessible if the user passes the Paywall.
    """
    return {
        "status": "success", 
        "agent_reply": f"Premium VIP User {req.user_id}, your query is: '{req.query}'. LangChain engine mounting (Stage 3 integration pending)..."
    }