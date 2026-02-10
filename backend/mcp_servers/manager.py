from contextlib import asynccontextmanager
from typing import Any
from mcp import ClientSession
from mcp.client.stdio import stdio_client

from .servers import get_calendar_server_params


class MCPManager:
    """Manages MCP server connections and tool operations."""
    
    def __init__(self):
        self._session: ClientSession | None = None
        self._tools: list[dict] = []
    
    @asynccontextmanager
    async def connect(self):
        """
        Async context manager for MCP connection lifecycle.
        
        Usage:
            manager = MCPManager()
            async with manager.connect():
                tools = manager.get_tools()
                result = await manager.call_tool("tool_name", {"arg": "value"})
        """
        server_params = get_calendar_server_params()
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                self._session = session
                await self._load_tools()
                
                try:
                    yield self
                finally:
                    self._session = None
                    self._tools = []
    
    async def _load_tools(self) -> None:
        """Fetches available tools from connected MCP server."""
        if not self._session:
            raise RuntimeError("Not connected to MCP server")
        
        tools_response = await self._session.list_tools()
        self._tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
            for tool in tools_response.tools
        ]
    
    def get_tools(self) -> list[dict]:
        """Returns list of available tools in Anthropic API format."""
        return self._tools
    
    async def call_tool(self, tool_name: str, tool_input: dict[str, Any]) -> str:
        """
        Executes a tool and returns the result as text.
        
        Args:
            tool_name: Name of the tool to execute
            tool_input: Arguments to pass to the tool
            
        Returns:
            Tool execution result as string
        """
        if not self._session:
            raise RuntimeError("Not connected to MCP server")
        
        result = await self._session.call_tool(tool_name, tool_input)
        
        # Extract text from result content
        result_text = ""
        for item in result.content:
            if hasattr(item, "text"):
                result_text += item.text
        
        return result_text