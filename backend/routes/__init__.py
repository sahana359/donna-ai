"""
Routes package for Donna AI Backend
Registers all API routers
"""
from fastapi import APIRouter

from .webhook import router as webhook_router
from .health import router as health_router
from .test import router as test_router
from .root import router as root_router

# Create main router
api_router = APIRouter()

# Include all route routers
api_router.include_router(webhook_router)
api_router.include_router(health_router)
api_router.include_router(test_router)
api_router.include_router(root_router)

__all__ = ["api_router"]
