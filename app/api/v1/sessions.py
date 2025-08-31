"""
Session management API endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.schemas import (
    SessionCreate, 
    SessionResponse, 
    SessionDetailResponse, 
    SessionListResponse,
    ChatRequest
)
from app.services.computer_use.agent_service import ComputerUseAgentService

router = APIRouter()
agent_service = ComputerUseAgentService()


@router.post("/", response_model=SessionResponse)
async def create_session(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new computer use agent session"""
    try:
        session = await agent_service.create_session(session_data, db)
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.get("/", response_model=SessionListResponse)
async def list_sessions(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    db: AsyncSession = Depends(get_db)
):
    """List all sessions with pagination"""
    try:
        result = await agent_service.list_sessions(db, page, size)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list sessions: {str(e)}")


@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed session information including messages and events"""
    try:
        result = await agent_service.get_session_history(session_id, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session: {str(e)}")


@router.post("/{session_id}/chat")
async def chat_with_session(
    session_id: str,
    chat_request: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    """Send a message to an active session"""
    try:
        # This endpoint will be used for WebSocket connections
        # For now, return a message indicating WebSocket should be used
        return {
            "message": "Please use WebSocket connection for real-time chat",
            "websocket_url": f"/ws/chat/{session_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process chat: {str(e)}")


@router.delete("/{session_id}")
async def close_session(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Close an active session"""
    try:
        success = await agent_service.close_session(session_id, db)
        if success:
            return {"message": "Session closed successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to close session: {str(e)}")


@router.get("/{session_id}/status")
async def get_session_status(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get current session status"""
    try:
        result = await agent_service.get_session_history(session_id, db)
        return {
            "session_id": session_id,
            "status": result["session"].status,
            "created_at": result["session"].created_at,
            "updated_at": result["session"].updated_at,
            "completed_at": result["session"].completed_at
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session status: {str(e)}")
