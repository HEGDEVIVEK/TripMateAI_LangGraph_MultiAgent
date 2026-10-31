import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

aviationstack_api = os.environ.get("AVIATIONSTACK_API_KEY")


async def get_aviationstack_mcp_tool():
    
    flight_mcp_client = MultiServerMCPClient(
    {
        "Aviationstack MCP": {
            "transport": "stdio",
            "command": "uvx",
            "args": ["aviationstack-mcp"],
            "env": {"AVIATION_STACK_API_KEY": aviationstack_api}
        }
    })

    tools = await flight_mcp_client.get_tools()

    for tool in tools:
        if(tool.name == "list_airports"):
            result = await tool.ainvoke({
                    "limit": 5,
                    "offset": 0,
                    "search": "Bengaluru"
                })
            print(result)
            break


