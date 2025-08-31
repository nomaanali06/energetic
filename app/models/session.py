"""
Database models for session management
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class Session(Base):
    """Session model for managing computer use agent tasks"""
    
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(500), nullable=True)
    status = Column(String(50), default="active")  # active, completed, failed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Computer use agent specific fields
    system_prompt = Column(Text, nullable=True)
    model_name = Column(String(100), nullable=True)
    tool_version = Column(String(100), nullable=True)
    
    # Relationships
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    computer_use_events = relationship("ComputerUseEvent", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Session(id={self.id}, session_id='{self.session_id}', status='{self.status}')>"


class Message(Base):
    """Message model for chat interactions"""
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    role = Column(String(50), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Message metadata
    message_type = Column(String(50), default="text")  # text, tool_call, tool_result, error
    message_metadata = Column(JSON, nullable=True)  # Additional message data
    
    # Relationships
    session = relationship("Session", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}', type='{self.message_type}')>"


class ComputerUseEvent(Base):
    """Computer use event model for tracking tool executions"""
    
    __tablename__ = "computer_use_events"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    event_type = Column(String(100), nullable=False)  # tool_call, tool_result, screenshot, etc.
    tool_name = Column(String(100), nullable=True)
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    duration_ms = Column(Integer, nullable=True)
    
    # Relationships
    session = relationship("Session", back_populates="computer_use_events")
    
    def __repr__(self):
        return f"<ComputerUseEvent(id={self.id}, type='{self.event_type}', tool='{self.tool_name}')>"


class User(Base):
    """User model for future authentication"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"
