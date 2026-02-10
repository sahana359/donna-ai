"""
Chat route - Simple chat endpoint
"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    text: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    text: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that accepts text and returns a response.
    
    Args:
        request: ChatRequest containing text string
        
    Returns:
        ChatResponse with greeting message
    """
    return ChatResponse(text="Hi, I'm donna-ai-backend!")
