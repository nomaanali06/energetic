# System Sequence Diagram

## Session Creation and Computer Use Agent Interaction Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant DB as Database
    participant A as Anthropic API
    participant V as VNC Server

    Note over U,V: Session Creation Flow
    
    U->>F: Click "Start New Agent Task"
    F->>B: POST /api/v1/sessions/
    B->>DB: Create session record
    DB-->>B: Session created
    B-->>F: Session response
    F-->>U: Show new session

    Note over U,V: Chat Interaction Flow
    
    U->>F: Type message "Search weather in Dubai"
    F->>B: WebSocket: /ws/chat/{session_id}
    B->>DB: Store user message
    B->>A: Send message to Claude
    A-->>B: Stream response chunks
    
    loop Streaming Response
        B->>F: WebSocket: content chunk
        F-->>U: Display streaming text
    end
    
    Note over U,V: Tool Execution Flow
    
    A->>B: Tool call: open_firefox
    B->>V: Execute tool via VNC
    V-->>B: Tool result
    B->>DB: Store tool event
    B->>F: WebSocket: tool_result
    F-->>U: Show tool execution
    
    A->>B: Tool call: navigate_to_google
    B->>V: Execute tool via VNC
    V-->>B: Tool result
    B->>DB: Store tool event
    B->>F: WebSocket: tool_result
    F-->>U: Show tool execution
    
    A->>B: Tool call: search_weather
    B->>V: Execute tool via VNC
    V-->>B: Tool result
    B->>DB: Store tool event
    B->>F: WebSocket: tool_result
    F-->>U: Show tool execution
    
    A-->>B: Task completed
    B->>DB: Update session status
    B->>F: WebSocket: complete
    F-->>U: Show completion message
```

## Key Components Interaction

### 1. Session Management
- User creates new session via REST API
- Backend stores session metadata in PostgreSQL
- Frontend displays session in sidebar

### 2. Real-time Communication
- WebSocket connection established for each session
- Bidirectional communication for chat and progress updates
- Streaming responses from Anthropic API

### 3. Tool Execution
- Anthropic API determines required tools
- Backend executes tools via VNC connection
- Results stored in database and streamed to frontend

### 4. Progress Tracking
- Each tool execution tracked as event
- Real-time updates via WebSocket
- Complete history stored in database

## Data Flow

```
User Input → Frontend → WebSocket → Backend → Anthropic API
                                 ↓
                            Tool Execution
                                 ↓
                            VNC Server
                                 ↓
                            Tool Results
                                 ↓
                            Database Storage
                                 ↓
                            WebSocket Streaming
                                 ↓
                            Frontend Display
```

## Error Handling

- Database connection failures
- WebSocket disconnections
- Tool execution errors
- API rate limiting
- VNC connection issues

Each error type has appropriate fallback behavior and user notification.
