from fastmcp import FastMCP
from datetime import date

mcp = FastMCP('MCPStdioServer')

@mcp.tool
def greet(name: str) -> str:
    '''This is Greet Tool, and based on the name, it going to greet the user'''
    return f'Hello {name}, Welcome to telusko! How are you doing today?'

@mcp.tool
def addition(num1 :int, num2 :int) -> int:
    """Add two integers and return the result."""
    return num1 + num2

if __name__ == "__main__":
    mcp.run(transport='http', host='127.0.0.1', port=8000,  show_banner=False)