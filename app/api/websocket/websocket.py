"""
WebSocket endpoints for real-time communication
"""

import json
import asyncio
from typing import Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.computer_use.agent_service import ComputerUseAgentService
from app.models.schemas import ChatRequest

websocket_router = APIRouter()
agent_service = ComputerUseAgentService()

# Store active WebSocket connections
active_connections: Dict[str, WebSocket] = {}


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Connect a new WebSocket client"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        """Disconnect a WebSocket client"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
    
    async def send_message(self, session_id: str, message: Dict[str, Any]):
        """Send a message to a specific WebSocket client"""
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
            except Exception:
                # Remove broken connection
                self.disconnect(session_id)


manager = ConnectionManager()


@websocket_router.websocket("/chat/{session_id}")
async def websocket_chat(
    websocket: WebSocket,
    session_id: str
):
    """WebSocket endpoint for real-time chat with computer use agent"""
    
    await manager.connect(websocket, session_id)
    
    try:
        # Send connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connection",
            "data": {
                "message": "Connected to computer use agent",
                "session_id": session_id
            }
        }))
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "chat":
                user_message = message_data.get("data", {}).get("message", "")
                
                if not user_message:
                    continue
                
                # Send acknowledgment
                await websocket.send_text(json.dumps({
                    "type": "ack",
                    "data": {
                        "message": "Message received",
                        "user_message": user_message
                    }
                }))
                
                # Process message with computer use agent
                async def progress_callback(chunk: Dict[str, Any]):
                    """Callback for streaming progress updates"""
                    await websocket.send_text(json.dumps(chunk))
                
                try:
                    # Get database session
                    from app.core.database import AsyncSessionLocal
                    async with AsyncSessionLocal() as db:
                        # Stream the agent response
                        async for chunk in agent_service.send_message(
                            session_id, 
                            user_message, 
                            db, 
                            progress_callback
                        ):
                            await websocket.send_text(json.dumps(chunk))
                            
                except Exception as e:
                    # Send error message
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "data": {
                            "error": f"Failed to process message: {str(e)}"
                        }
                    }))
            
            elif message_data.get("type") == "ping":
                # Respond to ping with pong
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "data": {"timestamp": asyncio.get_event_loop().time()}
                }))
                
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        # Send error and disconnect
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "data": {
                    "error": f"WebSocket error: {str(e)}"
                }
            }))
        except:
            pass
        finally:
            manager.disconnect(session_id)


@websocket_router.websocket("/vnc/{session_id}")
async def websocket_vnc(
    websocket: WebSocket,
    session_id: str
):
    """WebSocket endpoint for VNC connection status"""
    
    await manager.connect(websocket, session_id)
    
    try:
        # Send VNC connection info
        await websocket.send_text(json.dumps({
            "type": "vnc_info",
            "data": {
                "vnc_host": "localhost",  # This should come from config
                "vnc_port": 5901,
                "vnc_url": f"vnc://localhost:5901"
            }
        }))
        
        while True:
            # Keep connection alive and handle VNC-related messages
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "vnc_status":
                # Send VNC status update
                await websocket.send_text(json.dumps({
                    "type": "vnc_status",
                    "data": {
                        "status": "connected",
                        "session_id": session_id
                    }
                }))
                
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "data": {
                    "error": f"VNC WebSocket error: {str(e)}"
                }
            }))
        except:
            pass
        finally:
            manager.disconnect(session_id)
