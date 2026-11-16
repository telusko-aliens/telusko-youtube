from fastmcp import FastMCP
from datetime import date

mcp = FastMCP('MCPStdioServer')

@mcp.tool
def get_current_date() -> str:
    """Return today's date in ISO format (YYYY-MM-DD)."""
    return date.today().isoformat()

@mcp.tool
def multiply(num1 :int, num2 :int) -> int:
    """Multiply two integers and return the result."""
    return num1 * num2

if __name__ == "__main__":
    mcp.run(transport='stdio', show_banner=False)