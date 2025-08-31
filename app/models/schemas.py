"""
Pydantic schemas for API requests and responses
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class SessionStatus(str, Enum):
    """Session status enumeration"""
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MessageRole(str, Enum):
    """Message role enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageType(str, Enum):
    """Message type enumeration"""
    TEXT = "text"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ERROR = "error"


class EventStatus(str, Enum):
    """Computer use event status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# Base schemas
class SessionBase(BaseModel):
    """Base session schema"""
    title: Optional[str] = None
    system_prompt: Optional[str] = None
    model_name: Optional[str] = None
    tool_version: Optional[str] = None


class MessageBase(BaseModel):
    """Base message schema"""
    role: MessageRole
    content: str
    message_type: MessageType = MessageType.TEXT
    metadata: Optional[Dict[str, Any]] = None


class ComputerUseEventBase(BaseModel):
    """Base computer use event schema"""
    event_type: str
    tool_name: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    status: EventStatus = EventStatus.PENDING
    error_message: Optional[str] = None


# Create schemas
class SessionCreate(SessionBase):
    """Schema for creating a new session"""
    pass


class MessageCreate(MessageBase):
    """Schema for creating a new message"""
    pass


class ComputerUseEventCreate(ComputerUseEventBase):
    """Schema for creating a new computer use event"""
    pass


# Response schemas
class SessionResponse(SessionBase):
    """Schema for session responses"""
    id: int
    session_id: str
    status: SessionStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MessageResponse(MessageBase):
    """Schema for message responses"""
    id: int
    session_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ComputerUseEventResponse(ComputerUseEventBase):
    """Schema for computer use event responses"""
    id: int
    session_id: int
    timestamp: datetime
    duration_ms: Optional[int] = None
    
    class Config:
        from_attributes = True


# Detailed response schemas
class SessionDetailResponse(SessionResponse):
    """Detailed session response with related data"""
    messages: List[MessageResponse] = []
    computer_use_events: List[ComputerUseEventResponse] = []


# Request schemas
class ChatRequest(BaseModel):
    """Schema for chat requests"""
    message: str = Field(..., min_length=1, max_length=10000)
    stream: bool = Field(default=True, description="Enable real-time streaming")


class SessionListResponse(BaseModel):
    """Schema for session list responses"""
    sessions: List[SessionResponse]
    total: int
    page: int
    size: int


# WebSocket schemas
class WebSocketMessage(BaseModel):
    """Schema for WebSocket messages"""
    type: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StreamChunk(BaseModel):
    """Schema for streaming response chunks"""
    type: str  # message, tool_call, tool_result, error, complete
    data: Dict[str, Any]
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
