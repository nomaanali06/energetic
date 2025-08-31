"""
Computer Use Agent Service
Simplified version for demo purposes
"""

import asyncio
import uuid
from datetime import datetime
from typing import AsyncGenerator, Dict, Any, Optional, Callable

from app.core.config import settings
from app.models.session import Session, Message, ComputerUseEvent
from app.models.schemas import SessionCreate, MessageCreate, ComputerUseEventCreate


class ComputerUseAgentService:
    """Service for managing computer use agent sessions"""
    
    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.tool_version = "computer_use_20250124"  # Demo version
        
        # Simplified system prompt for demo
        self.system_prompt = f"""<SYSTEM_CAPABILITY>
* You are utilising an Ubuntu virtual machine with internet access.
* You can feel free to install Ubuntu applications with your bash tool. Use curl instead of wget.
* To open firefox, please just click on the firefox icon. Note, firefox-esr is what is installed on your system.
* The current date is {datetime.today().strftime('%A, %B %-d, %Y')}.
</SYSTEM_CAPABILITY>"""

    async def create_session(self, session_data: SessionCreate, db_session) -> Session:
        """Create a new computer use agent session"""
        session_id = str(uuid.uuid4())
        
        # Create session in database
        db_session_obj = Session(
            session_id=session_id,
            title=session_data.title or "New Computer Use Session",
            system_prompt=session_data.system_prompt or self.system_prompt,
            model_name=session_data.model_name or settings.ANTHROPIC_MODEL,
            tool_version=session_data.tool_version or str(self.tool_version),
            status="active"
        )
        
        db_session.add(db_session_obj)
        await db_session.commit()
        await db_session.refresh(db_session_obj)
        
        # Store session in memory for active management
        self.active_sessions[session_id] = {
            "db_session": db_session_obj,
            "messages": [],
            "status": "active",
            "created_at": datetime.utcnow()
        }
        
        return db_session_obj

    async def send_message(
        self, 
        session_id: str, 
        user_message: str, 
        db_session,
        progress_callback: Optional[Callable] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Send a message to the computer use agent and stream the response (demo version)"""
        
        # Check if session is in memory, if not load from database
        if session_id not in self.active_sessions:
            from sqlalchemy import select
            
            # Try to load session from database
            session_stmt = select(Session).where(Session.session_id == session_id)
            session_result = await db_session.execute(session_stmt)
            db_session_obj = session_result.scalar_one_or_none()
            
            if not db_session_obj:
                raise ValueError(f"Session {session_id} not found")
            
            # Add to active sessions
            self.active_sessions[session_id] = {
                "db_session": db_session_obj,
                "messages": [],
                "status": "active",
                "created_at": datetime.utcnow()
            }
        
        session_info = self.active_sessions[session_id]
        
        # Store user message
        user_msg = Message(
            session_id=session_info["db_session"].id,
            role="user",
            content=user_message,
            message_type="text"
        )
        db_session.add(user_msg)
        await db_session.commit()
        
        # Simulate agent response for demo
        if "weather" in user_message.lower() and "dubai" in user_message.lower():
            # Simulate weather search for Dubai
            yield {
                "type": "content",
                "data": {
                    "role": "assistant",
                    "content": "I'll help you search for the weather in Dubai. Let me open Firefox and search for this information.",
                    "message_type": "text"
                }
            }
            
            await asyncio.sleep(1)
            
            yield {
                "type": "tool_call",
                "data": {
                    "tool_name": "open_firefox",
                    "input": "Opening Firefox browser"
                }
            }
            
            await asyncio.sleep(1)
            
            yield {
                "type": "tool_call",
                "data": {
                    "tool_name": "navigate_to_google",
                    "input": "Navigating to Google search"
                }
            }
            
            await asyncio.sleep(1)
            
            yield {
                "type": "tool_call",
                "data": {
                    "tool_name": "search_weather",
                    "input": "Searching for weather in Dubai"
                }
            }
            
            await asyncio.sleep(1)
            
            yield {
                "type": "content",
                "data": {
                    "role": "assistant",
                    "content": "Based on my search, the current weather in Dubai is sunny with a temperature of 35°C (95°F). The humidity is around 45% and there's a light breeze from the northwest.",
                    "message_type": "text"
                }
            }
            
        elif "weather" in user_message.lower() and "san francisco" in user_message.lower():
            # Simulate weather search for San Francisco
            yield {
                "type": "content",
                "data": {
                    "role": "assistant",
                    "content": "I'll help you search for the weather in San Francisco. Let me open Firefox and search for this information.",
                    "message_type": "text"
                }
            }
            
            await asyncio.sleep(1)
            
            yield {
                "type": "tool_call",
                "data": {
                    "tool_name": "open_firefox",
                    "input": "Opening Firefox browser"
                }
            }
            
            await asyncio.sleep(1)
            
            yield {
                "type": "tool_call",
                "data": {
                    "tool_name": "navigate_to_google",
                    "input": "Navigating to Google search"
                }
            }
            
            await asyncio.sleep(1)
            
            yield {
                "type": "tool_call",
                "data": {
                    "tool_name": "search_weather",
                    "input": "Searching for weather in San Francisco"
                }
            }
            
            await asyncio.sleep(1)
            
            yield {
                "type": "content",
                "data": {
                    "role": "assistant",
                    "content": "Based on my search, the current weather in San Francisco is partly cloudy with a temperature of 18°C (64°F). The humidity is around 70% and there's a moderate wind from the west.",
                    "message_type": "text"
                }
            }
            
        else:
            yield {
                "type": "content",
                "data": {
                    "role": "assistant",
                    "content": "I understand your request. For this demo, I'm simulating the computer use agent behavior. Try asking about the weather in Dubai or San Francisco to see the full workflow.",
                    "message_type": "text"
                }
            }
        
        # Store assistant message
        assistant_msg = Message(
            session_id=session_info["db_session"].id,
            role="assistant",
            content="Demo response completed",
            message_type="text"
        )
        db_session.add(assistant_msg)
        await db_session.commit()
        
        # Mark session as completed
        session_info["db_session"].status = "completed"
        session_info["db_session"].completed_at = datetime.utcnow()
        await db_session.commit()
        
        yield {
            "type": "complete",
            "data": {"status": "completed"}
        }

    # Simplified tool execution for demo
    async def _execute_tool_call(self, *args, **kwargs):
        """Placeholder for tool execution (demo version)"""
        pass

    async def get_session_history(self, session_id: str, db_session) -> Dict[str, Any]:
        """Get complete session history including messages and events"""
        
        from sqlalchemy import select
        
        # Get session by session_id (not by id)
        session_stmt = select(Session).where(Session.session_id == session_id)
        session_result = await db_session.execute(session_stmt)
        session = session_result.scalar_one_or_none()
        
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Get messages
        messages_stmt = select(Message).where(
            Message.session_id == session.id
        ).order_by(Message.timestamp)
        messages_result = await db_session.execute(messages_stmt)
        messages = messages_result.scalars().all()
        
        # Get events
        events_stmt = select(ComputerUseEvent).where(
            ComputerUseEvent.session_id == session.id
        ).order_by(ComputerUseEvent.timestamp)
        events_result = await db_session.execute(events_stmt)
        events = events_result.scalars().all()
        
        return {
            "session": session,
            "messages": messages,
            "events": events
        }

    async def list_sessions(self, db_session, page: int = 1, size: int = 10) -> Dict[str, Any]:
        """List all sessions with pagination"""
        
        from sqlalchemy import select, func
        
        # Get total count
        count_stmt = select(func.count(Session.id))
        total_result = await db_session.execute(count_stmt)
        total = total_result.scalar()
        
        # Get paginated sessions
        sessions_stmt = select(Session).order_by(
            Session.created_at.desc()
        ).offset((page - 1) * size).limit(size)
        sessions_result = await db_session.execute(sessions_stmt)
        sessions = sessions_result.scalars().all()
        
        return {
            "sessions": sessions,
            "total": total,
            "page": page,
            "size": size
        }

    async def close_session(self, session_id: str, db_session) -> bool:
        """Close an active session"""
        
        if session_id not in self.active_sessions:
            return False
        
        session_info = self.active_sessions[session_id]
        session_info["db_session"].status = "cancelled"
        await db_session.commit()
        
        del self.active_sessions[session_id]
        return True
