import asyncio
from tripmateai_langgraph_multiagent.mcp_client.tavily_mcp import get_tavily_search_mcp_tool

result = asyncio.run(get_tavily_search_mcp_tool("hotel near madgaon railway station"))
print(result)