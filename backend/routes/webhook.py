"""
Webhook route - Receives transcript segments from OMI device
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Request, Query, HTTPException

from models import WebhookResponse
from utils import log
from collections import defaultdict
from routes.chat import chat, ChatRequest
import re

router = APIRouter()
session_segments: Dict[str, List[Dict]] = defaultdict(list)


@router.post("/webhook", response_model=WebhookResponse)
async def webhook(
    request: Request,
    uid: str = Query(..., description="User ID from OMI"),
    session_id: Optional[str] = Query(None, description="Session ID from OMI (optional)")
):
    """
    Webhook endpoint to receive transcript segments from OMI device.
    
    OMI device sends POST requests with transcript segments as the user speaks.
    This endpoint receives and processes these segments.
    """
    try:
        # Parse payload from OMI
        payload = await request.json()
        log(f"📥 Received webhook")
        
        # Handle both formats: array of segments or dict with segments key
        segments: List[Dict[str, Any]] = []
        if isinstance(payload, list):
            segments = payload
        elif isinstance(payload, dict):
            segments = payload.get("segments", [])
            # If session_id in payload but not in query, use it
            if not session_id and "session_id" in payload:
                session_id = payload["session_id"]
        
        # Use consistent session_id per user if not provided
        if not session_id:
            session_id = f"omi_session_{uid}"
        
        log(f"📊 Received {len(segments)} segment(s) for session: {session_id} from uid: {uid[:10]}")
        
        # Log segment details (first 3 segments for debugging)
        if segments:
            for i, seg in enumerate(segments[:3]):
                text = seg.get('text', 'NO TEXT') if isinstance(seg, dict) else str(seg)
                log(f"   Segment {i+1}: {text}")
        
        session_segments[session_id].extend(segments)
    
        # Check for trigger in accumulated text
        full_text = " ".join(s.get("text", "") for s in session_segments[session_id])
        
        if re.search(r"hey[\s,\.]*donna", full_text.lower()):
            log(f"Hi Donna detected 🤖🤖🤖🤖")
            chat_request = ChatRequest(message=full_text)
            log(f"🤖 Sending Chat request: {chat_request.message}")
            chat_response = await chat(chat_request)
            log(f"🤖 Chat response: {chat_response.message}")
        
        # Process accumulated context
        # TODO: In next iteration, we'll:
        # 1. Accumulate segments per session
        # 2. Detect "Hey, donna" trigger
        # 3. Extract content after trigger
        # 4. Call Claude agent
        
        # For now, just acknowledge receipt
        return WebhookResponse(
            status="ok",
            message="Segments received",
            session_id=session_id,
            processed_segments=len(segments)
        )
        
    except Exception as e:
        log(f"❌ Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")
