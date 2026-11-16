from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

import os
import json
import asyncio

load_dotenv()

BRANCH = 'live-mcp'
BASE_BRANCH = 'main'
FILE_PATH = 'live_mcp.txt'

async def call(tool, args):
    response = await tool.ainvoke(args)
    text = response[0]['text']
    try:
        text = json.loads(text)
    except json.JSONDecodeError:
        pass

    print(f"\n--- {tool.name} ---\n{text}")
    return text

async def main():

    client = MultiServerMCPClient({
        'github': {
            'transport': 'streamable_http',
            'url': 'https://api.githubcopilot.com/mcp/',
            'headers': {
                'Authorization': f"Bearer {os.environ['GITHUB_PERSONAL_ACCESS_TOKEN']}"
            },
        }
    })

    tools = await client.get_tools()

    tools_by_name = {}
    for tool in tools:
        tools_by_name[tool.name] = tool


    me = await call(tools_by_name['get_me'], {})
    owner = me['login']

    # Create the repo
    repo = 'MCP-Youtube-Test'
    await call(tools_by_name['create_repository'], {
        'name': repo, 
        'description': 'This is just for testing',
        'private': True, 
        'autoInit': True
    })

    target = {'owner': owner, 'repo': repo}

    # Create Branch
    await call(tools_by_name['create_branch'], {
        **target, 'branch': BRANCH,
        'from_branch': BASE_BRANCH})

    # Create File
    created = await call(tools_by_name['create_or_update_file'], {
        **target,
        'branch': BRANCH,
        'path': FILE_PATH,
        'content': '# Live MCP\n\nThis file was created through the GitHub MCP server.\n',
        'message': 'Add live_mcp.txt',
    })

    #Create PR
    pr = await call(tools_by_name['create_pull_request'], {
        **target,
        'title': 'Live MCP demo',
        'head': BRANCH,
        'base': BASE_BRANCH,
        'body': 'Opened through the GitHub MCP server.',
    })
    pr_number = pr['number'] if isinstance(pr, dict) and 'number' in pr else int(pr['url'].rstrip('/').split('/')[-1])

    # Update PR
    await call(tools_by_name['update_pull_request'], {
        **target,
        'pullNumber': pr_number,
        'title': 'Live MCP demo (updated)',
        'body': 'Opened and updated through the GitHub MCP server.',
    })

    # Make PR in Pending State
    await call(tools_by_name['pull_request_review_write'], {
        **target,
        'pullNumber': pr_number,
        'method': 'create'
    })

    # Add a comment to Pending Review
    await call(tools_by_name['add_comment_to_pending_review'], {
        **target,
        'pullNumber': pr_number,
        'path': FILE_PATH,
        'line': 3,
        'side': 'RIGHT',
        'subjectType': 'LINE',
        'body': 'Looks good. Nice use of the GitHub MCP server.',
    })

    # Submit the pending review so the comment becomes visible
    await call(tools_by_name['pull_request_review_write'], {
        **target,
        'pullNumber': pr_number,
        'method': 'submit_pending',
        'event': 'COMMENT',
        'body': 'Review submitted through the GitHub MCP server.',
    })

if __name__ == "__main__":
    asyncio.run(main())