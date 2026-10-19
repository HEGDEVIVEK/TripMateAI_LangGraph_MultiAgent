import json
import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP
from langchain_mcp_adapters.client import MultiServerMCPClient

mcp = FastMCP("weather mcp")

@mcp.tool()
def get_weather(city : str):
    """Get current weather for a city."""
    weather_mcp_api = os.environ.get("WEATHER_API_KEY")
    response = requests.get("https://api.openweathermap.org/data/2.5/weather",params={
        "q" : city,
        "appid" : weather_mcp_api,
        "units" : "metric"
    })

    data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "weather": data["weather"][0]["description"],
    }


async def get_weather_mcp_tool(city : str):
  
    weather_mcp_client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [str(Path(__file__).resolve())],
                "env": {
                    "WEATHER_API_KEY": os.environ["WEATHER_API_KEY"],
                },  
            }
        }
    )
    
    tools = await weather_mcp_client.get_tools()
    
    for tool in tools:
        if tool.name == "get_weather":
            result = await tool.ainvoke({"city" : city})
            weather_data = json.loads(result[0]["text"])
            return weather_data

if __name__ == "__main__":
    mcp.run(transport="stdio")