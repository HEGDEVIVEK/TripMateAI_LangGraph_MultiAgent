import os
import uuid

from langchain_core.messages import HumanMessage
from tripmateai_langgraph_multiagent.final_graph import final_graph

# final_graph.get_graph().draw_mermaid_png(output_file_path="tripmate_ai_graph.png")
# config = {"configurable": {"thread_id": "test_user"}}
# print(final_graph.get_state(config))

def run_tripMate_agent(user_query : str, thread_id:str | None = None):
    if not thread_id:
        thread_id = f"user_{uuid.uuid4().hex}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
 
    result = final_graph.invoke({
        "messages": [HumanMessage(content=user_query)],
        "user_query": user_query,
        "flight_result" : "",
        "weather_result" : "",
        "hotel_result" : "",
        "sightseeing_result" : "",
        "itinerary_result" : ""
    },
    config=config
    )

    return {
        "thread_id" : thread_id,
        "messages" : result["messages"]
    }