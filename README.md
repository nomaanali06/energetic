**Author: Noman Ali**

# 🚀 Energetic Backend - Computer Use Agent Session Management


A scalable backend system for managing computer use agent sessions, built with FastAPI and integrated with Anthropic's computer use tools. This project replaces the experimental Streamlit interface with a robust, production-ready backend that provides real-time streaming, session management, and database persistence.

## 🎯 Project Overview

This project demonstrates a scalable architecture for AI agents that can control computers like humans do - taking screenshots, clicking buttons, typing text, and navigating software interfaces. The system provides:

- **Session Management**: Create, manage, and track computer use agent sessions
- **Real-time Streaming**: WebSocket-based communication for live progress updates
- **VNC Integration**: Connect to virtual machines for desktop interaction
- **Database Persistence**: Store chat history and session data
- **RESTful APIs**: Clean, documented endpoints for all operations
- **Modern Frontend**: Simple HTML/JS interface for testing and demonstration

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   PostgreSQL    │
│   (HTML/JS)     │◄──►│   Backend       │◄──►│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Anthropic     │
                       │ Computer Use    │
                       │   Tools         │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   VNC Server    │
                       │  (Ubuntu VM)    │
                       └─────────────────┘
```

## 🚀 Features

### Core Functionality
- **Session Management**: Create, list, and manage computer use agent sessions
- **Real-time Chat**: WebSocket-based communication with streaming responses
- **Tool Execution**: Execute computer use tools (bash, screenshots, file operations)
- **Progress Tracking**: Monitor tool execution and agent progress in real-time
- **History Persistence**: Store all interactions and results in PostgreSQL

### Technical Features
- **FastAPI Backend**: Modern, fast Python web framework with automatic API documentation
- **WebSocket Support**: Real-time bidirectional communication
- **Database Integration**: SQLAlchemy ORM with PostgreSQL
- **Docker Support**: Complete containerization for easy deployment
- **Rate Limiting**: Built-in protection against abuse
- **Health Checks**: Monitoring and health status endpoints

## 📋 Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose**
- **PostgreSQL 15+** (or use Docker)
- **Anthropic API Key** (for computer use agent functionality)

## 🛠️ Installation & Setup

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd energetic-backend
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

3. **Start the services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs
   - VNC: localhost:5900
   - noVNC: http://localhost:6080

### Option 2: Local Development

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb energetic_db
   
   # Set environment variables
   export DATABASE_URL="postgresql://username:password@localhost:5432/energetic_db"
   export ANTHROPIC_API_KEY="your_api_key_here"
   ```

3. **Run the application**
   ```bash
   python -m app.main
   ```

## 🔌 API Endpoints

### Session Management

#### Create Session
```http
POST /api/v1/sessions/
Content-Type: application/json

{
  "title": "Search weather in Dubai",
  "system_prompt": "Custom system prompt (optional)",
  "model_name": "claude-sonnet-4-20250514",
  "tool_version": "computer_use_20250124"
}
```

#### List Sessions
```http
GET /api/v1/sessions/?page=1&size=10
```

#### Get Session Details
```http
GET /api/v1/sessions/{session_id}
```

#### Close Session
```http
DELETE /api/v1/sessions/{session_id}
```

### WebSocket Endpoints

#### Chat WebSocket
```javascript
const ws = new WebSocket(`ws://localhost:8000/ws/chat/${sessionId}`);

// Send message
ws.send(JSON.stringify({
  type: 'chat',
  data: { message: 'Search the weather in Dubai' }
}));

// Receive streaming updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

#### VNC Status WebSocket
```javascript
const vncWs = new WebSocket(`ws://localhost:8000/ws/vnc/${sessionId}`);
```

## 💻 Usage Examples

### Example 1: Search Weather in Dubai

1. **Create a new session**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/sessions/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Search weather in Dubai"}'
   ```

2. **Connect via WebSocket and send message**
   ```javascript
   const ws = new WebSocket('ws://localhost:8000/ws/chat/SESSION_ID');
   
   ws.onopen = () => {
     ws.send(JSON.stringify({
       type: 'chat',
       data: { message: 'Search the weather in Dubai' }
     }));
   };
   
   ws.onmessage = (event) => {
     const data = JSON.parse(event.data);
     if (data.type === 'content') {
       console.log('Agent response:', data.data.content);
     }
   };
   ```

3. **Monitor progress in real-time**
   - The agent will open Firefox
   - Navigate to Google
   - Search for "weather in Dubai"
   - Provide a summarized result

### Example 2: Search Weather in San Francisco

Follow the same process with a new session and the message "Search the weather in San Francisco". Both sessions will be stored independently with full history.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Required |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/energetic_db` |
| `DEBUG` | Enable debug mode | `false` |
| `VNC_HOST` | VNC server hostname | `localhost` |
| `VNC_PORT` | VNC server port | `5900` |

### Database Schema

The system automatically creates the following tables:
- `sessions`: Session metadata and status
- `messages`: Chat messages and interactions
- `computer_use_events`: Tool execution events and results

## 🐳 Docker Deployment

### Production Deployment

1. **Build the production image**
   ```bash
   docker build -t energetic-backend:latest .
   ```

2. **Run with production settings**
   ```bash
   docker run -d \
     -p 8000:8000 \
     -e ANTHROPIC_API_KEY=your_key \
     -e DATABASE_URL=your_db_url \
     -e DEBUG=false \
     energetic-backend:latest
   ```

### Scaling

The system is designed to scale horizontally:
- Multiple backend instances behind a load balancer
- Shared PostgreSQL database
- Redis for session caching
- Nginx for reverse proxy and rate limiting

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

### API Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test session creation
curl -X POST "http://localhost:8000/api/v1/sessions/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Session"}'
```

## 📊 Monitoring & Health Checks

### Health Endpoints
- `GET /health` - Application health status
- `GET /api/v1/health` - API health status

### Metrics (Optional)
Enable Prometheus metrics by setting `ENABLE_METRICS=true` in your environment.

## 🔒 Security Considerations

- **API Key Protection**: Never expose your Anthropic API key
- **Rate Limiting**: Built-in protection against abuse
- **CORS Configuration**: Configure allowed origins for production
- **Input Validation**: All inputs are validated using Pydantic schemas
- **SQL Injection Protection**: SQLAlchemy ORM prevents injection attacks

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running
   - Verify connection string in `.env`
   - Ensure database exists

2. **WebSocket Connection Failed**
   - Check backend is running on port 8000
   - Verify CORS settings
   - Check firewall settings

3. **VNC Connection Issues**
   - Ensure VNC container is running
   - Check ports 5900 and 6080 are accessible
   - Verify VNC password if set

### Logs

Check container logs:
```bash
# Backend logs
docker-compose logs backend

# Database logs
docker-compose logs postgres

# VNC logs
docker-compose logs vnc
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Anthropic** for the computer use tools and API
- **FastAPI** for the excellent web framework
- **SQLAlchemy** for database ORM
- **Docker** for containerization

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the API documentation at `/api/docs`
3. Open an issue in the repository

---

**Built with ❤️ for the CambioML Senior Backend/DevOps Engineer Coding Challenge**
