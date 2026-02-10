import os
from anthropic import Anthropic

from mcp_servers import MCPManager


def _get_claude_client() -> Anthropic:
    """Returns configured Anthropic client."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return Anthropic(api_key=api_key)


async def run_agent(
    manager: MCPManager,
    user_message: str,
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 4096,
    on_tool_call: callable = None
) -> str:
    """
    Runs the Claude agentic loop with MCP tools.
    
    Args:
        manager: Connected MCPManager instance
        user_message: User's input message
        model: Claude model to use
        max_tokens: Maximum tokens in response
        on_tool_call: Optional callback(tool_name, tool_input) for logging
        
    Returns:
        Claude's final text response
    """
    client = _get_claude_client()
    tools = manager.get_tools()
    messages = [{"role": "user", "content": user_message}]
    
    while True:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            tools=tools,
            messages=messages
        )
        
        # Check if Claude wants to use tools
        if response.stop_reason == "tool_use":
            # Add Claude's response to conversation
            messages.append({"role": "assistant", "content": response.content})
            
            # Execute each tool call
            tool_results = []
            for content in response.content:
                if content.type == "tool_use":
                    tool_name = content.name
                    tool_input = content.input
                    
                    # Optional callback for logging/UI updates
                    if on_tool_call:
                        on_tool_call(tool_name, tool_input)
                    
                    # Execute tool via MCP
                    result_text = await manager.call_tool(tool_name, tool_input)
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content.id,
                        "content": result_text
                    })
            
            # Send results back to Claude
            messages.append({"role": "user", "content": tool_results})
        
        else:
            # Claude finished - extract final text response
            final_response = ""
            for content in response.content:
                if hasattr(content, "text"):
                    final_response += content.text
            
            return final_response