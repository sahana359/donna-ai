"""
Root route - API information
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "app": "Donna AI Backend",
        "version": "0.1.0",
        "status": "active",
        "endpoints": {
            "webhook": "POST /webhook?uid=<user_id>&session_id=<session_id>",
            "health": "GET /health",
            "test": "GET /test?dev=true&uid=<user_id>"
        }
    }
