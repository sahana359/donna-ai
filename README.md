# Donna AI

AI-powered Personal Assistant with Voice Interface and Productivity Integrations

## Overview

Donna AI is an intelligent voice-activated personal assistant that integrates with the OMI wearable device and provides comprehensive productivity management through Google Calendar, Notion, and Gmail integrations. The system consists of a FastAPI backend powered by Claude AI (Anthropic) and a native iOS SwiftUI application for chat interactions.

## Architecture

The project follows a **client-server architecture** with three main components:

```
┌─────────────────┐
│   OMI Device    │  (Voice Input via Webhook)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│          Backend (FastAPI)                  │
│  ┌───────────────────────────────────────┐  │
│  │  Webhook Handler                      │  │
│  │  - Receives transcript segments       │  │
│  │  - Trigger detection ("Hey Donna")    │  │
│  │  - Debounce processing                │  │
│  └───────────────────────────────────────┘  │
│                    │                         │
│                    ▼                         │
│  ┌───────────────────────────────────────┐  │
│  │  AI Agent (Claude via Anthropic)     │  │
│  │  - Agentic loop with tool calls       │  │
│  │  - Conversation history management    │  │
│  └───────────────────────────────────────┘  │
│                    │                         │
│                    ▼                         │
│  ┌───────────────────────────────────────┐  │
│  │  MCP Manager (Model Context Protocol) │  │
│  │  - Google Calendar Integration        │  │
│  │  - Notion Workspace Integration       │  │
│  │  - Gmail Integration                  │  │
│  │  - Tool execution via stdio           │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
         ▲
         │
┌────────┴────────┐
│   iOS App       │  (SwiftUI Chat Interface)
│   - ChatView    │
│   - ChatService │
└─────────────────┘
```

## Components

### Backend (`/backend`)

The backend is built with **FastAPI** (Python 3.13+) and provides the core intelligence layer.

#### Key Modules:

1. **`main.py`** - FastAPI application entry point
   - Initializes the FastAPI server
   - Configures routes and middleware
   - Runs on port 8000 (configurable)

2. **`routes/`** - API endpoint handlers
   - **`webhook.py`** - Receives transcript segments from OMI device
     - Accumulates segments per session
     - Detects trigger phrase ("Hey Donna")
     - Implements debounce timer (10 seconds)
     - Extracts instructions after trigger
   - **`chat.py`** - Direct chat endpoint for manual interaction
     - Manages per-session conversation history
     - Limits history to last 20 messages
   - **`health.py`** - Health check endpoint
   - **`root.py`** - API information endpoint
   - **`test.py`** - Development testing interface with web UI

3. **`ai/`** - AI agent implementation
   - **`agent.py`** - Claude AI integration
     - Implements agentic loop with tool use
     - Manages conversation context
     - Executes MCP tools via Claude
     - Uses `claude-3-5-haiku-20241022` model

4. **`mcp_servers/`** - Model Context Protocol integration
   - **`manager.py`** - MCP server lifecycle management
     - Connects to MCP servers via stdio
     - Loads available tools
     - Executes tool calls
   - **`servers/calendar.py`** - Google Calendar server configuration
     - Connects to `@cocal/google-calendar-mcp` via npx
     - Requires OAuth credentials
   - **`servers/notion.py`** - Notion workspace server configuration
     - Connects to `@modelcontextprotocol/server-notion` via npx
     - Requires Notion API token
   - **`servers/gmail.py`** - Gmail server configuration
     - Connects to `@modelcontextprotocol/server-gmail` via npx
     - Requires OAuth credentials

5. **`models/`** - Pydantic data models
   - **`transcript_segment.py`** - OMI transcript segment model
   - **`webhook_response.py`** - Webhook response model

6. **`utils.py`** - Utility functions
   - Logging with immediate flush

#### API Endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check status |
| POST | `/webhook` | Receives transcript segments from OMI device |
| POST | `/chat` | Direct chat with AI assistant |
| GET | `/test?dev=true` | Development testing interface |

#### Dependencies:

- **fastapi** (0.128.4+) - Web framework
- **anthropic** (0.79.0+) - Claude AI API client
- **mcp** (1.26.0+) - Model Context Protocol SDK
- **httpx** (0.28.1+) - HTTP client for async requests
- **uvicorn** (0.40.0+) - ASGI server
- **python-dotenv** (1.2.1+) - Environment variable management

### UI (`/ui`)

Native iOS application built with **SwiftUI** for direct chat interaction.

#### Key Components:

1. **`uiApp.swift`** - SwiftUI app entry point

2. **`Views/`**
   - **`ContentView.swift`** - Root view (contains ChatView)
   - **`ChatView.swift`** - Main chat interface
     - Message list with ScrollView
     - Auto-scroll to latest message
     - Loading indicator with ThinkingBubble
     - Message input with MessageInputBar
   - **`MessageBubble.swift`** - Individual message display
   - **`MessageInputBar.swift`** - Text input component
   - **`ThinkingBubble.swift`** - Loading indicator

3. **`Services/`**
   - **`ChatService.swift`** - Backend API client
     - Sends POST requests to `/chat` endpoint
     - Handles JSON encoding/decoding
     - Default backend URL: `http://127.0.0.1:8000`

4. **`Models/`**
   - **`Message.swift`** - Message data model
     - Unique ID, content, sender flag, timestamp

### OMI Device Integration

The system integrates with the **OMI wearable device** which:
- Captures voice input continuously
- Transcribes speech in real-time
- Sends transcript segments via webhook
- Provides speaker identification
- Includes timing information (start/end)

#### Trigger Mechanism:

1. User says **"Hey Donna"** or **"Hi Donna"** or **"Hello Donna"**
2. Webhook accumulates segments per session
3. When trigger detected, starts 10-second debounce timer
4. Each new segment resets the timer
5. After 10 seconds of silence, extracts instruction after trigger
6. Sends instruction to `/chat` endpoint for processing

### AI Agent with MCP Tools

The AI agent uses **Claude** with the **Model Context Protocol (MCP)** for tool integration:

#### Agentic Loop:
1. Receives user message with conversation history
2. Calls Claude API with available MCP tools
3. If Claude requests tool use:
   - Executes tool via MCP Manager
   - Returns result to Claude
   - Continues loop
4. If Claude provides final response:
   - Returns text to user
   - Updates conversation history

#### Available Tools:

**Via Google Calendar MCP Server** (`@cocal/google-calendar-mcp`):
- Create calendar events
- List events
- Update events
- Delete events
- Search calendar
- Check availability

**Via Notion MCP Server** (`@modelcontextprotocol/server-notion`):
- Create pages and databases
- Update page content
- Search workspace
- Query databases
- Add comments
- Manage blocks

**Via Gmail MCP Server** (`@modelcontextprotocol/server-gmail`):
- Send emails
- Read emails
- Search inbox
- Create drafts
- Manage labels
- Archive/delete messages

## Setup and Installation

### Prerequisites

- **Python 3.13+**
- **Node.js and npm** (for MCP servers)
- **Xcode** (for iOS app development)
- **Google OAuth credentials** (for Calendar and Gmail access)
- **Notion API token** (for Notion workspace access)
- **Anthropic API key** (for Claude AI)

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies using `uv`:
   ```bash
   uv sync
   ```
   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file with required environment variables:
   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_OAUTH_CREDENTIALS=your_google_oauth_credentials_json
   NOTION_API_TOKEN=your_notion_integration_token
   GMAIL_OAUTH_CREDENTIALS=your_gmail_oauth_credentials_json
   PORT=8000
   HOST=0.0.0.0
   ```

4. Run the backend server:
   ```bash
   python main.py
   ```
   Or with uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### iOS App Setup

1. Navigate to UI directory:
   ```bash
   cd ui
   ```

2. Open the Xcode project:
   ```bash
   open ui.xcodeproj
   ```

3. Update backend URL in `ChatView.swift` if needed (default: `http://127.0.0.1:8000`)

4. Build and run the app in Xcode (⌘R)

### OMI Device Setup

1. Configure your OMI device with the webhook URL:
   ```
   https://your-server.com/webhook?uid=your_user_id
   ```

2. The device will automatically send transcript segments as you speak

3. Use the trigger phrase "Hey Donna" followed by your instruction

## Usage

### Using the iOS App

1. Launch the Donna AI app on your iOS device
2. Type your message in the input field
3. Tap send or press return
4. View AI response in the chat interface

### Using Voice with OMI Device

1. Wear your OMI device
2. Say: "Hey Donna, [your instruction]"
   - Example: "Hey Donna, schedule a meeting tomorrow at 2pm"
   - Example: "Hey Donna, send an email to john@example.com about the project"
   - Example: "Hey Donna, create a note in Notion about today's meeting"
3. Wait for processing (10-second silence detection)
4. AI will execute the task using available tools

### Development Testing

Access the test interface at:
```
http://localhost:8000/test?dev=true&uid=test_user_123
```

Features:
- Simulate voice commands without OMI device
- Test webhook processing
- View activity logs
- Quick example commands

### API Usage

#### Chat Endpoint

**Example 1: Schedule a Calendar Event**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Schedule a meeting tomorrow at 2pm",
    "session_id": "user123"
  }'
```

Response:
```json
{
  "text": "I've scheduled the meeting for tomorrow at 2pm."
}
```

**Example 2: Send an Email**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Send an email to john@example.com with subject Project Update",
    "session_id": "user123"
  }'
```

Response:
```json
{
  "text": "I've sent the email to john@example.com with the subject Project Update."
}
```

**Example 3: Create a Notion Page**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a new note in Notion about our team meeting",
    "session_id": "user123"
  }'
```

Response:
```json
{
  "text": "I've created a new page in Notion with notes about your team meeting."
}
```

#### Webhook Endpoint (OMI Device)

```bash
curl -X POST "http://localhost:8000/webhook?uid=user123&session_id=session456" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "text": "Hey Donna schedule a meeting",
      "speaker": "SPEAKER_00",
      "is_user": true,
      "start": 0.0,
      "end": 3.5
    }
  ]'
```

Response:
```json
{
  "status": "ok",
  "message": "Segments received",
  "session_id": "session456",
  "processed_segments": 1
}
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | API key for Claude AI | Yes |
| `GOOGLE_OAUTH_CREDENTIALS` | JSON credentials for Google Calendar | Yes |
| `GMAIL_OAUTH_CREDENTIALS` | JSON credentials for Gmail access | Yes |
| `NOTION_API_TOKEN` | API token for Notion workspace | Yes |
| `PORT` | Backend server port | No (default: 8000) |
| `HOST` | Backend server host | No (default: 0.0.0.0) |

### Conversation History

- Maximum 20 messages per session (configurable in `chat.py`)
- Stored in-memory (resets on server restart)
- First message always starts with user role

### Debounce Timer

- 10 seconds of silence after trigger phrase (configurable in `webhook.py`)
- Resets on each new segment
- Prevents premature processing

## Features

✅ **Voice Activation** - Trigger with "Hey Donna" or similar phrases  
✅ **Calendar Management** - Create, list, update, delete events via Google Calendar  
✅ **Email Management** - Send, read, search emails via Gmail  
✅ **Note Taking** - Create pages, search content, manage databases in Notion  
✅ **Conversation Context** - Multi-turn conversations with history  
✅ **OMI Device Integration** - Real-time voice transcript processing  
✅ **iOS Native App** - SwiftUI chat interface  
✅ **Agentic AI** - Claude with tool-use capabilities  
✅ **MCP Integration** - Extensible tool system with multiple services  
✅ **Development Testing** - Web-based test interface  
✅ **Session Management** - Per-user conversation tracking  

## Technology Stack

**Backend:**
- Python 3.13+
- FastAPI (Web Framework)
- Anthropic Claude AI (LLM)
- Model Context Protocol (Tool Integration)
- Google Calendar API (via MCP)
- Gmail API (via MCP)
- Notion API (via MCP)
- Uvicorn (ASGI Server)

**Frontend:**
- SwiftUI (iOS Framework)
- Swift 5.9+
- URLSession (HTTP Client)

**Integration:**
- OMI Wearable Device
- Webhook-based real-time transcription
- OAuth 2.0 (Google Authentication)
- Notion API (Workspace Integration)

## Project Structure

```
donna-ai/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── ai/
│   │   ├── agent.py           # Claude AI agent with agentic loop
│   │   └── __init__.py
│   ├── routes/
│   │   ├── webhook.py         # OMI webhook handler
│   │   ├── chat.py            # Chat endpoint
│   │   ├── health.py          # Health check
│   │   ├── root.py            # API info
│   │   ├── test.py            # Test interface
│   │   └── __init__.py
│   ├── mcp_servers/
│   │   ├── manager.py         # MCP connection manager
│   │   ├── servers/
│   │   │   ├── calendar.py    # Google Calendar config
│   │   │   ├── gmail.py       # Gmail config
│   │   │   ├── notion.py      # Notion config
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── models/
│   │   ├── transcript_segment.py
│   │   ├── webhook_response.py
│   │   └── __init__.py
│   ├── utils.py               # Utility functions
│   ├── pyproject.toml         # Python dependencies
│   └── README.md              # Backend documentation
├── ui/
│   ├── ui/
│   │   ├── uiApp.swift        # App entry point
│   │   ├── ContentView.swift  # Root view
│   │   ├── Views/
│   │   │   ├── ChatView.swift
│   │   │   ├── MessageBubble.swift
│   │   │   ├── MessageInputBar.swift
│   │   │   └── ThinkingBubble.swift
│   │   ├── Services/
│   │   │   └── ChatService.swift
│   │   └── Models/
│   │       └── Message.swift
│   └── ui.xcodeproj/          # Xcode project
└── README.md                  # This file

```

## Development

### Running Tests

Backend:
```bash
cd backend
# Test interface available at /test?dev=true
curl http://localhost:8000/health
```

### Adding New MCP Servers

1. Create new server configuration in `backend/mcp_servers/servers/`
2. Update `manager.py` to include new server
3. Claude will automatically discover new tools

### Extending Functionality

- Add new routes in `backend/routes/`
- Add new AI capabilities via MCP tools
- Customize trigger phrases in `webhook.py`
- Extend iOS UI with new views

## Version

Current version: **0.1.0**

## License

[Add your license information here]

## Credits

- Built with [Anthropic Claude](https://www.anthropic.com/)
- Integrates with [OMI Device](https://www.omi.me/)
- Uses [Model Context Protocol](https://modelcontextprotocol.io/)
- Google Calendar integration via [@cocal/google-calendar-mcp](https://github.com/cocal-io/google-calendar-mcp)
- Gmail integration via [@modelcontextprotocol/server-gmail](https://github.com/modelcontextprotocol/servers/tree/main/src/gmail)
- Notion integration via [@modelcontextprotocol/server-notion](https://github.com/modelcontextprotocol/servers/tree/main/src/notion)
