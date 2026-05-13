import asyncio
import json
import sys
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

from tools import AVAILABLE_TOOLS


def build_tool_schema(tool_info: dict) -> dict:
    """Build JSON schema for tool input"""
    properties = {}
    
    for param, desc in tool_info["params"].items():
        properties[param] = {
            "type": "string",
            "description": desc
        }
    
    return {
        "type": "object",
        "properties": properties,
    }


async def main():
    """Main entry point"""
    server = Server("ai-agent-mcp")
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List all available tools"""
        tools = []
        for tool_name, tool_info in AVAILABLE_TOOLS.items():
            tool = Tool(
                name=tool_name,
                description=tool_info["description"],
                inputSchema=build_tool_schema(tool_info)
            )
            tools.append(tool)
        return tools
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Execute a tool"""
        if name not in AVAILABLE_TOOLS:
            return [
                TextContent(
                    type="text",
                    text=f"Tool '{name}' not found. Available tools: {', '.join(AVAILABLE_TOOLS.keys())}"
                )
            ]
        
        tool_info = AVAILABLE_TOOLS[name]
        func = tool_info["func"]
        
        try:
            filtered_args = {
                k: v for k, v in arguments.items() 
                if k in tool_info["params"]
            }
            
            #call the tool function with the provided arguments
            result = await func(**filtered_args)
            
            #convert result to JSON string for display
            if isinstance(result, dict) or isinstance(result, list):
                result_text = json.dumps(result, indent=2)
            else:
                result_text = str(result)
            
            return [
                TextContent(
                    type="text",
                    text=result_text
                )
            ]
        except TypeError as e:
            #handle missing required arguments
            return [
                TextContent(
                    type="text",
                    text=f"Error: Invalid arguments for '{name}'. {str(e)}\nExpected parameters: {list(tool_info['params'].keys())}"
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=f"Error calling tool '{name}': {str(e)}"
                )
            ]
    
    print("Starting AI Agent MCP Server...", file=sys.stderr)
    print(f"Available tools: {list(AVAILABLE_TOOLS.keys())}", file=sys.stderr)
    
    initialization_options = server.create_initialization_options()
    async with stdio_server() as (input_stream, output_stream):
        await server.run(input_stream, output_stream, initialization_options)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shutdown", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
