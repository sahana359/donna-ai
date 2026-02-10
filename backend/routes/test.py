"""
Test interface route - Development testing interface
"""
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

router = APIRouter()


def get_test_css() -> str:
    """Returns CSS styles for test interface."""
    return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            background: #1a1d21;
            color: #d1d2d3;
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
            animation: fadeIn 0.5s ease-out;
        }
        
        .container {
            max-width: 650px;
            margin: 0 auto;
            animation: fadeIn 0.6s ease-out;
        }
        
        .header-success {
            background: #232529;
            padding: 40px 24px;
            border-radius: 8px;
            margin-bottom: 24px;
            border: 1px solid #2c2d30;
            text-align: center;
        }
        
        h1 {
            color: #ffffff;
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 12px;
        }
        
        h2 {
            color: #ffffff;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 15px;
            border-bottom: 1px solid #2c2d30;
            padding-bottom: 10px;
        }
        
        h3 {
            color: #ffffff;
            font-size: 19px;
            font-weight: 700;
            margin-bottom: 12px;
        }
        
        p {
            color: #9ca0a5;
            margin-bottom: 24px;
            font-size: 16px;
        }
        
        .card {
            background: #232529;
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 16px;
            border: 1px solid #2c2d30;
            transition: border-color 0.2s;
        }
        
        .card:hover {
            border-color: #1d9bd1;
        }
        
        .btn {
            display: inline-block;
            padding: 10px 20px;
            border-radius: 4px;
            text-decoration: none;
            font-weight: 700;
            font-size: 15px;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            margin: 8px 8px 8px 0;
            text-align: center;
            line-height: 20px;
        }
        
        .btn-primary {
            background: #007a5a;
            color: #ffffff;
        }
        
        .btn-primary:hover {
            background: #148567;
        }
        
        .btn-secondary {
            background: transparent;
            color: #d1d2d3;
            border: 1px solid #545454;
        }
        
        .btn-secondary:hover {
            background: #2c2d30;
        }
        
        .btn-block {
            display: block;
            width: 100%;
            margin: 10px 0;
        }
        
        input[type="text"], textarea {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #545454;
            border-radius: 4px;
            font-size: 15px;
            font-family: inherit;
            background: #1a1d21;
            color: #d1d2d3;
            transition: all 0.2s;
        }
        
        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: #1d9bd1;
            box-shadow: 0 0 0 3px rgba(29, 155, 209, 0.3);
        }
        
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        .input-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 700;
            color: #d1d2d3;
            font-size: 15px;
        }
        
        .example {
            background: #1a1d21;
            padding: 16px 18px;
            border-radius: 6px;
            margin: 12px 0;
            font-size: 15px;
            cursor: pointer;
            border: 1px solid #2c2d30;
            color: #d1d2d3;
            transition: all 0.2s;
            line-height: 1.6;
        }
        
        .example:hover {
            border-color: #1d9bd1;
            background: #232529;
        }
        
        .status {
            padding: 15px;
            border-radius: 6px;
            margin: 15px 0;
            font-weight: 500;
            display: none;
            border: 1px solid;
        }
        
        .status.info {
            background: rgba(29, 155, 209, 0.15);
            color: #1d9bd1;
            border-color: #1d9bd1;
        }
        
        .status.recording {
            background: rgba(236, 178, 46, 0.15);
            color: #ecb22e;
            border-color: #ecb22e;
        }
        
        .status.success {
            background: rgba(0, 122, 90, 0.15);
            color: #2eb67d;
            border-color: #007a5a;
        }
        
        .status.error {
            background: rgba(224, 30, 90, 0.15);
            color: #e01e5a;
            border-color: #e01e5a;
        }
        
        .log {
            background: #1a1d21;
            border: 1px solid #2c2d30;
            border-radius: 6px;
            padding: 15px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            margin-top: 15px;
        }
        
        .log-entry {
            padding: 5px 0;
            border-bottom: 1px solid #2c2d30;
            color: #d1d2d3;
        }
        
        .timestamp {
            color: #9ca0a5;
            margin-right: 10px;
        }
        
        @media (max-width: 480px) {
            body {
                padding: 12px;
            }
            
            .card {
                padding: 18px;
            }
            
            h1 {
                font-size: 26px;
            }
        }
    """


@router.get("/test")
async def test_interface(uid: str = Query("test_user_123"), dev: str = Query(None)):
    """Development testing interface for testing webhook without OMI device."""
    if not dev or dev != "true":
        return HTMLResponse(content=f"""
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Not Found</title>
                <style>{get_test_css()}</style>
            </head>
            <body>
                <div class="container">
                    <div class="card" style="margin-top: 40px; padding: 40px 24px; text-align: center;">
                        <h1 style="font-size: 48px; margin-bottom: 16px;">404</h1>
                        <h2 style="border-bottom: none; padding-bottom: 0;">Page Not Found</h2>
                        <p style="margin-bottom: 24px;">The page you're looking for doesn't exist.</p>
                        <a href="/" class="btn btn-primary">Go to Homepage</a>
                    </div>
                </div>
            </body>
        </html>
        """, status_code=404)
    
    return HTMLResponse(content=f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Donna AI - Test Interface</title>
            <style>
                {get_test_css()}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header-success">
                    <h1>🧪 Test Interface</h1>
                    <p>Test webhook endpoint without OMI device</p>
                </div>

                <div class="card">
                    <h2>Test Webhook</h2>
                    <div class="input-group">
                        <label>User ID (UID):</label>
                        <input type="text" id="uid" value="{uid}">
                    </div>
                    <div class="input-group">
                        <label>What would you say to OMI:</label>
                        <textarea id="voiceInput" rows="5" placeholder='Example: "Hey, donna schedule a meeting tomorrow at 2pm"'></textarea>
                    </div>
                    <button class="btn btn-primary btn-block" onclick="sendCommand()">🎤 Send Command</button>
                    <button class="btn btn-secondary btn-block" onclick="clearLogs()">🗑️ Clear Logs</button>
                    
                    <div id="status" class="status"></div>
                </div>

                <div class="card">
                    <h3>Quick Examples (Click to use)</h3>
                    <div class="example" onclick="useExample(this)">
                        Hey, donna schedule a meeting tomorrow at 2pm
                    </div>
                    <div class="example" onclick="useExample(this)">
                        Hey, donna send an email to john@example.com about the project
                    </div>
                    <div class="example" onclick="useExample(this)">
                        Hey, donna create a note in Notion about today's meeting
                    </div>
                </div>

                <div class="card">
                    <h2>Activity Log</h2>
                    <div id="log" class="log">
                        <div class="log-entry">
                            <span class="timestamp">Ready</span>
                            <span>Waiting for commands...</span>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                const sessionId = 'test_session_' + Date.now();
                
                function addLog(message) {{
                    const log = document.getElementById('log');
                    const entry = document.createElement('div');
                    entry.className = 'log-entry';
                    const time = new Date().toLocaleTimeString();
                    entry.innerHTML = `<span class="timestamp">[${{time}}]</span><span>${{message}}</span>`;
                    log.insertBefore(entry, log.firstChild);
                }}
                
                function setStatus(message, type = 'info') {{
                    const status = document.getElementById('status');
                    status.textContent = message;
                    status.className = 'status ' + type;
                    status.style.display = 'block';
                }}
                
                async function sendCommand() {{
                    const uid = document.getElementById('uid').value;
                    const voiceInput = document.getElementById('voiceInput').value;
                    
                    if (!uid || !voiceInput) {{
                        alert('Please enter both User ID and voice command');
                        return;
                    }}
                    
                    setStatus('🎤 Processing command...', 'recording');
                    addLog('📤 Sending: "' + voiceInput.substring(0, 100) + '..."');
                    
                    try {{
                        const segments = [{{
                            text: voiceInput,
                            speaker: "SPEAKER_00",
                            speakerId: 0,
                            is_user: true,
                            start: 0.0,
                            end: 5.0
                        }}];
                        
                        const response = await fetch(`/webhook?session_id=${{sessionId}}&uid=${{uid}}`, {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify(segments)
                        }});
                        
                        const data = await response.json();
                        
                        if (response.ok) {{
                            setStatus('✅ ' + (data.message || 'Command received'), 'success');
                            addLog('✅ ' + JSON.stringify(data, null, 2));
                        }} else {{
                            setStatus('❌ Error: ' + (data.detail || 'Unknown error'), 'error');
                            addLog('❌ Error: ' + (data.detail || 'Unknown error'));
                        }}
                    }} catch (error) {{
                        setStatus('❌ Network error', 'error');
                        addLog('❌ Network error: ' + error.message);
                    }}
                }}
                
                function useExample(element) {{
                    document.getElementById('voiceInput').value = element.textContent.trim();
                    addLog('📝 Example loaded');
                }}
                
                function clearLogs() {{
                    document.getElementById('log').innerHTML = '<div class="log-entry"><span class="timestamp">Cleared</span><span>Logs cleared</span></div>';
                    setStatus('');
                }}
            </script>
        </body>
    </html>
    """)
