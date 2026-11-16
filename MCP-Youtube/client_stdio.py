from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

from pathlib import Path
import sys
import asyncio

load_dotenv()

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

    llm = ChatOpenAI(model='gpt-4o-mini')
    llm_with_tools = llm.bind_tools(tools)

    messages = []

    user_input = input("User: ")
    messages.append(HumanMessage(content=user_input))

    response = llm_with_tools.invoke(user_input) 
    messages.append(AIMessage(content=response.content, tool_calls=response.tool_calls))

    tools_by_name = {}
    for tool in tools:
        tools_by_name[tool.name] = tool

    for tool_call in response.tool_calls:
        tool = tools_by_name[tool_call["name"]]
        tool_response = await tool.ainvoke(tool_call['args'])
        messages.append(ToolMessage(content=tool_response, tool_call_id=tool_call['id']))

    final_response = await llm_with_tools.ainvoke(messages)
    print(f'AI: {final_response.content}')
    


if __name__ == "__main__":
    asyncio.run(main())