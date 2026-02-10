"""
Webhook Response Model
Response from webhook endpoint
"""
from typing import Optional
from pydantic import BaseModel


class WebhookResponse(BaseModel):
    """Response from webhook endpoint."""
    status: str
    message: Optional[str] = None
    session_id: Optional[str] = None
    processed_segments: Optional[int] = None
