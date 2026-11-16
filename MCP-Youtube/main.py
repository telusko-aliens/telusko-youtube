from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from datetime import date
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

@tool
def get_current_date() -> str:
    """Return today's date in ISO format (YYYY-MM-DD)."""
    return date.today().isoformat()

@tool
def multiply(num1 :int, num2 :int) -> int:
    """Multiply two integers and return the result."""
    return num1 * num2

tools = {
    'get_current_date': get_current_date,
    'multiply': multiply
}

def main():
    llm = ChatOpenAI(model='gpt-4o-mini')

    llm_with_tools = llm.bind_tools(list(tools.values()))
    
    messages = []
    
    user_input = input("User: ")
    messages.append(HumanMessage(content=user_input))

    response = llm_with_tools.invoke(user_input) 
    messages.append(response)
    print(response)

    for tool_call in response.tool_calls:
        tool_response = tools[tool_call['name']].invoke(tool_call['args'])
        messages.append(ToolMessage(content=tool_response, tool_call_id=tool_call['id']) )

    response = llm_with_tools.invoke(messages)
    print(f'AI: {response.content}')

if __name__ == "__main__":
    main()
