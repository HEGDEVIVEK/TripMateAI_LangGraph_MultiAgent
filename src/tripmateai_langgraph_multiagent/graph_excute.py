import os
import uuid
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from tripmateai_langgraph_multiagent.graphSchema import graph_schema

from tripmateai_langgraph_multiagent.agents.aviation_node import aviation_agent_node
from tripmateai_langgraph_multiagent.agents.hotel_node import hotel_agent_node
from tripmateai_langgraph_multiagent.agents.sightseeing_node import sightseeing_agent_node
from tripmateai_langgraph_multiagent.agents.itinerary_node import itinerary_agent_node

from tripmateai_langgraph_multiagent.databse import get_postgres_conn
from langgraph.checkpoint.postgres import PostgresSaver

conn = get_postgres_conn()
print(conn)
checkpointer = PostgresSaver(conn)
checkpointer.setup()

graph = StateGraph(graph_schema)

graph.add_node("aviation_agent_node", aviation_agent_node)
graph.add_node("hotel_agent_node", hotel_agent_node)
graph.add_node("sightseeing_agent_node", sightseeing_agent_node)
graph.add_node("itinerary_agent_node", itinerary_agent_node)

graph.add_edge(START, "aviation_agent_node")
graph.add_edge(START, "hotel_agent_node")
graph.add_edge(START, "sightseeing_agent_node")

graph.add_edge(["aviation_agent_node", "hotel_agent_node", "sightseeing_agent_node"], "itinerary_agent_node")

graph.add_edge("itinerary_agent_node", END)

final_graph = graph.compile(checkpointer=checkpointer)

final_graph.get_graph().draw_mermaid_png(
    output_file_path="tripmate_ai_graph.png"
)

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
        "flight_result" : [],
        "hotel_result" : "",
        "sightseeing_result" : "",
        "itinerary_result" : ""
    },
    config=config
    )

    final_answer = result["messages"][-1].content

    return {
        "thread_id" : thread_id,
        "user_query" : result["user_query"],
        "final_answer" : final_answer,
        "flight_result" : result["flight_result"],
        "hotel_result" : result["hotel_result"],
        "sightseeing_result" : result["sightseeing_result"],
        "itinerary_result" : result["itinerary_result"],
    }