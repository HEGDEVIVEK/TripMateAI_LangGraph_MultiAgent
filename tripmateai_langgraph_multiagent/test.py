import asyncio
from tripmateai_langgraph_multiagent.mcp_client.tavily_mcp import get_tavily_search_mcp_tool
from tripmateai_langgraph_multiagent.mcp_client.flight_mcp import get_aviationstack_mcp_tool
from tripmateai_langgraph_multiagent.mcp_client.weather_mcp import get_weather_mcp_tool
from tripmateai_langgraph_multiagent.mcp_client.weather_mcp import get_weather
from pprint import pprint

# data = get_weather("Sirsi")
# pprint(data)

data = asyncio.run(get_weather_mcp_tool("Sirsi"))
print(data)