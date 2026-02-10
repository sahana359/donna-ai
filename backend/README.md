# Donna AI Backend

FastAPI backend for Donna AI Voice Assistant MVP.

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Create `.env` file:**
   ```bash
   # Copy example (if available) or create manually
   # Required variables:
   HOST=0.0.0.0
   PORT=8000
   ANTHROPIC_API_KEY=your_key_here
   ```

3. **Run the server:**
   ```bash
   uv run python main.py
   # Or
   uv run uvicorn main:app --reload
   ```

4. **Test locally:**
   - Visit `http://localhost:8000/test?dev=true` in your browser
   - Type commands in the web interface to simulate OMI device
   - See real-time logs and responses

## Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /webhook?uid=<user_id>&session_id=<session_id>` - Receive transcript segments from OMI device
- `GET /test?dev=true&uid=<user_id>` - Test interface for local development (simulates OMI device)

## Development

The webhook endpoint currently:
- Receives transcript segments from OMI device
- Logs segment information
- Returns acknowledgment

Next iterations will add:
- Segment accumulation per session
- "Hey, donna" trigger detection
- Claude agent integration
