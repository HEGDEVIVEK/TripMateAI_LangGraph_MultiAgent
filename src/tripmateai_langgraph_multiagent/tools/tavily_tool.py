from langchain_core.tools import tool
import os
from dotenv import load_dotenv
load_dotenv()

if os.environ.get("TAVILY_API_KEY"):
    print("bro it is working")


from langchain_tavily import TavilySearch

tavily_search = TavilySearch(
    max_results=3,
    topic="general",
    search_depth="basic"
)

@tool
def tavily_search_tool(question:str):
    """
    Perform a web search using Tavily Search.
    """
    result = tavily_search.invoke(question)
    all_result = []
    for res in result["results"]:
        title = res["title"].strip()
        url = res["url"].strip()
        content = res["content"].strip()
        all_result.append(f"Title: {title}\nURL: {url}\nContent: {content}")
    return "\n\n".join(all_result)
