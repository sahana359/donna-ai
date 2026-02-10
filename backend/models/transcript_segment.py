"""
Transcript Segment Model
Represents a single transcript segment from OMI device
"""
from typing import Optional
from pydantic import BaseModel


class TranscriptSegment(BaseModel):
    """Single transcript segment from OMI device."""
    text: str
    speaker: Optional[str] = None
    speakerId: Optional[int] = None
    is_user: Optional[bool] = True
    start: Optional[float] = None
    end: Optional[float] = None
