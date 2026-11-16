from langchain_mcp_adapters.client import MultiServerMCPClient
from pathlib import Path
import sys
import asyncio

SERVER_PATH = Path(__file__).parent / "mcp_server_stdio.py"

client = MultiServerMCPClient({
    'client': {
        'transport': 'stdio',
        'command': sys.executable,
        'args': [str(SERVER_PATH)]
    }
})

async def main():
    tools = await client.get_tools()
    print(tools)

    first_tool = tools[0]
    response = await first_tool.ainvoke({})
    print(response)

if __name__ == "__main__":
    asyncio.run(main())