"""
Chat route - Simple chat endpoint
"""
from fastapi import APIRouter
from pydantic import BaseModel
from mcp_servers import MCPManager
from ai import run_agent


router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    text: str



@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that processes user message through Claude with MCP tools.
    """
    print(f"Received chat request: {request.message}")
    
    manager = MCPManager()
    
    async with manager.connect():
        response = await run_agent(
            manager=manager,
            user_message=request.message
        )
    
    return ChatResponse(text=response)
