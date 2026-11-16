# MCP-Youtube

Source code for the Telusko MCP (Model Context Protocol) video. It shows how to build MCP servers with FastMCP and connect to them from a LangChain client.

## Setup

1. Install [uv](https://docs.astral.sh/uv/) and Python 3.14 or later.
2. Install the dependencies:

   ```
   uv sync
   ```

3. Copy `.env.example` to `.env` and add your own keys:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GITHUB_PERSONAL_ACCESS_TOKEN=your_github_personal_access_token_here
   ```

   The GitHub token is only needed for `github_mcp_client.py`.

## Files

| File | What it does |
| --- | --- |
| `main.py` | Tool calling with LangChain only, without MCP |
| `mcp_server_stdio.py` | MCP server over stdio (`get_current_date`, `multiply`) |
| `mcp_server_http.py` | MCP server over HTTP on port 8000 (`greet`, `addition`) |
| `client.py` | Minimal client that lists the stdio server tools and calls one |
| `client_stdio.py` | LLM client using the stdio server |
| `client_http.py` | LLM client using the HTTP server |
| `client_combined.py` | LLM client using both servers together |
| `github_mcp_client.py` | Client for the remote GitHub MCP server |

## Running

Run any file with uv:

```
uv run main.py
uv run client_stdio.py
```

The stdio server is started by the client automatically. For `client_http.py` and `client_combined.py`, start the HTTP server first in another terminal:

```
uv run mcp_server_http.py
```

Note: `github_mcp_client.py` creates a private repository named `MCP-Youtube-Test` in your GitHub account, along with a branch, a file and a pull request.
