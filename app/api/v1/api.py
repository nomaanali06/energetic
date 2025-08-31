"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1 import sessions

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])

# Add health check endpoint
@api_router.get("/health")
async def health_check():
    """API health check"""
    return {"status": "healthy", "api_version": "v1"}
