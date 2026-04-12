import asyncio
import json
import sys
from typing import Any

from tools import AVAILABLE_TOOLS


class AgentMCPServer:
    """MCP Server providing AI agent tools"""
    
    def __init__(self):
        self.server = Server("ai-agent-mcp")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP event handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools"""
            tools = []
            for tool_name, tool_info in AVAILABLE_TOOLS.items():
                tool = Tool(
                    name=tool_name,
                    description=tool_info["description"],
                    inputSchema={
                        "type": "object",
                        "properties": {
                            param: {"type": "string", "description": desc}
                            for param, desc in tool_info["params"].items()
                        },
                        "required": list(tool_info["params"].keys())
                    }
                )
                tools.append(tool)
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent | ToolResponse]:
            """Execute a tool"""
            if name not in AVAILABLE_TOOLS:
                return [
                    TextContent(
                        type="text",
                        text=f"Tool '{name}' not found"
                    )
                ]
            
            tool_info = AVAILABLE_TOOLS[name]
            func = tool_info["func"]
            
            try:
                result = await func(**arguments)
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )
                ]
            except Exception as e:
                return [
                    TextContent(
                        type="text",
                        text=f"Error calling tool '{name}': {str(e)}"
                    )
                ]
    
    async def run(self, transport):
        """Run the MCP server"""
        await self.server.run(transport)


async def main():
    """Main entry point"""
    from mcp.server import StdioServerTransport
    
    server = AgentMCPServer()
    transport = StdioServerTransport()
    
    print("Starting AI Agent MCP Server...", file=sys.stderr)
    await server.run(transport)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shutdown", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)
