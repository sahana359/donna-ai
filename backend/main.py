"""
Donna AI Backend - FastAPI Server
Receives transcript segments from OMI device via webhook
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI

from routes import api_router
from utils import log

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Donna AI Backend",
    description="AI Voice Assistant MVP - OMI Integration",
    version="0.1.0"
)

# Include all routes
app.include_router(api_router)


# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    log("=" * 50)
    log("Donna AI Backend")
    log("=" * 50)
    log(f"Starting server on {host}:{port}")
    log("=" * 50)
    
    uvicorn.run("main:app", host=host, port=port, reload=True)
