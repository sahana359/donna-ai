"""
Webhook route - Receives transcript segments from OMI device
"""
import asyncio
import re
import traceback
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Request, Query, HTTPException

from models import WebhookResponse
from utils import log
from collections import defaultdict
from routes.chat import chat, ChatRequest

router = APIRouter()

session_segments: Dict[str, List[Dict]] = defaultdict(list)
session_timers: Dict[str, asyncio.Task] = {}
DEBOUNCE_SECONDS = 10
TRIGGER_PATTERN = re.compile(
    r"(hey|hi|hello)[\s,.\-]*(donna|dona)",
    re.IGNORECASE,
)


async def _debounce_and_process(session_id: str):
    """Wait for silence, then extract instruction after trigger and send to chat."""
    try:
        await asyncio.sleep(DEBOUNCE_SECONDS)
    except asyncio.CancelledError:
        # Timer was reset by a new webhook call — exit silently
        return

    # Timer expired — 5 seconds of silence
    segments = session_segments.pop(session_id, [])
    session_timers.pop(session_id, None)

    if not segments:
        return

    full_text = " ".join(s.get("text", "") for s in segments)
    match = TRIGGER_PATTERN.search(full_text)
    if not match:
        return

    # Extract everything AFTER the trigger phrase
    instruction = full_text[match.end():].strip()
    if not instruction:
        log(f"Trigger detected for session {session_id} but no instruction followed — skipping")
        return

    log(f"Processing instruction for session {session_id}: {instruction}")
    try:
        chat_response = await chat(ChatRequest(message=instruction))
        log(f"Chat response for session {session_id}: {chat_response.text}")
    except Exception as e:
        log(f"Error processing chat for session {session_id}: {e}")
        traceback.print_exc()


@router.post("/webhook", response_model=WebhookResponse)
async def webhook(
    request: Request,
    uid: str = Query(..., description="User ID from OMI"),
    session_id: Optional[str] = Query(None, description="Session ID from OMI (optional)")
):
    """
    Webhook endpoint to receive transcript segments from OMI device.

    OMI device sends POST requests with transcript segments as the user speaks.
    Segments are accumulated per session. When a trigger phrase ("Hey Donna") is
    detected, debounce timer starts. Each new segment resets the timer.
    After time runs out the instruction following the trigger is sent to /chat.
    """
    try:
        payload = await request.json()

        segments: List[Dict[str, Any]] = []
        if isinstance(payload, list):
            segments = payload
        elif isinstance(payload, dict):
            segments = payload.get("segments", [])
            if not session_id and "session_id" in payload:
                session_id = payload["session_id"]

        if not session_id:
            session_id = f"omi_session_{uid}"

        log(f"Received {len(segments)} segment(s) for session: {session_id}")

        session_segments[session_id].extend(segments)
        if segments:
            for i, seg in enumerate(segments):
                log(f" Segment {i+1}: {seg.get('text', '')}")
        # Check for trigger in accumulated text
        full_text = " ".join(s.get("text", "") for s in session_segments[session_id])
        if TRIGGER_PATTERN.search(full_text):
            log(f"Trigger detected for session {session_id}, (re)starting debounce timer")

            # Cancel existing timer if one is running
            existing = session_timers.get(session_id)
            if existing and not existing.done():
                existing.cancel()

            # Start a fresh 5-second debounce timer as a background task
            session_timers[session_id] = asyncio.create_task(
                _debounce_and_process(session_id)
            )

        return WebhookResponse(
            status="ok",
            message="Segments received",
            session_id=session_id,
            processed_segments=len(segments)
        )

    except Exception as e:
        log(f"Error processing webhook: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")
