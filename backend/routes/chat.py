"""
Chat route - Simple chat endpoint
"""
from typing import Optional, Dict
from collections import defaultdict
from fastapi import APIRouter
from pydantic import BaseModel
from mcp_servers import MCPManager
from ai import run_agent


router = APIRouter()

# Per-session conversation history (in-memory)
session_conversations: Dict[str, list] = defaultdict(list)
MAX_HISTORY_MESSAGES = 20  # ~3-4 conversation turns with tool calls


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    text: str



@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that processes user message through Claude with MCP tools.
    If session_id is provided, retains conversation history across requests.
    """
    print(f"Received chat request: {request.message}")

    # Look up existing history for this session
    history = []
    if request.session_id:
        history = list(session_conversations[request.session_id])

    manager = MCPManager()

    async with manager.connect():
        response, updated_messages = await run_agent(
            manager=manager,
            user_message=request.message,
            history=history,
        )

    # Save updated messages back to session (trimmed)
    if request.session_id:
        # Trim to last N messages, ensuring first message has role "user"
        trimmed = updated_messages[-MAX_HISTORY_MESSAGES:]
        while trimmed and trimmed[0].get("role") != "user":
            trimmed = trimmed[1:]
        session_conversations[request.session_id] = trimmed

    return ChatResponse(text=response)
