import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

async def get_tavily_search_mcp_tool(search_query : str | None = None):
    tvaily_search_mcp_tool = None

    tavily_api = os.environ.get("TAVILY_API_KEY")

    if not tavily_api:
        raise ValueError("TAVILY_API_KEY is not set")

    mcp_client = MultiServerMCPClient(
        {
            "tavily": {
                "transport": "http",
                "url": f"https://mcp.tavily.com/mcp?tavilyApiKey={tavily_api}",
            }
        }
    )

    tools = await mcp_client.get_tools()
    
    for tool in tools:
        if tool.name == "tavily_search":
            tvaily_search_mcp_tool = tool
            break

    if search_query:
        result = await tvaily_search_mcp_tool.ainvoke({"query" : search_query})
        return result