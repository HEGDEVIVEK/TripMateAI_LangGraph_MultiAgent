from tripmateai_langgraph_multiagent.tools.tavily_tool import tavily_search_tool
from tripmateai_langgraph_multiagent.tools.flight_tool import aviationStack_tool

# result = tavily_search_tool.invoke("3 Best Hotels in Bengaluru.")
# print(result)

result = aviationStack_tool("Flights from Bengaluru to Delhi.")
print(result)

